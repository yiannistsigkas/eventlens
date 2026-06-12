# =============================================================================
# EventLens v0.1 — Polymarket data pipeline (patched for first live run)
# Split this bundle into separate files exactly as marked:
#   scripts/fetch_polymarket_markets.py
#   scripts/score_markets.py
#   README_eventlens_pipeline.md (bottom comment block)
#
# Patches in this revision:
#   1. safe_float() used for ALL conversions of raw API fields
#   2. Unexpected API shapes are dumped to data/debug/ (one sample per kind
#      per run) so parsers can be adapted from evidence, not guesses
#   3. Diagnostics summary after scoring, including trust-score spread check
#
# Run order:
#   python scripts/fetch_polymarket_markets.py
#   python scripts/score_markets.py
# =============================================================================


# =============================================================================
# FILE: scripts/fetch_polymarket_markets.py
# =============================================================================
"""
Fetch active Polymarket markets, order books, and (best-effort) top holders.
Writes one append-only raw snapshot file per run. No scoring happens here.

Public endpoints (no auth):
  Gamma API   https://gamma-api.polymarket.com/markets
  CLOB API    https://clob.polymarket.com/book
  Data API    https://data-api.polymarket.com/holders
Field names drift over time — parsing is defensive, and unexpected shapes are
saved to data/debug/ for inspection.
"""

import json
import os
import time
from datetime import datetime, timezone

import requests

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
DATA_API = "https://data-api.polymarket.com"

RAW_DIR = os.path.join("data", "raw")
DEBUG_DIR = os.path.join("data", "debug")
N_MARKETS = 50
REQUEST_PAUSE_S = 0.25
TIMEOUT_S = 30

_DEBUG_SAVED = set()  # one debug sample per kind per run is enough


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_float(x, default=None):
    """Convert API field to float without crashing on '', None, junk, or wrong types."""
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def dump_debug(kind: str, payload):
    """Save one sample of an unexpected API response per kind per run."""
    if kind in _DEBUG_SAVED:
        return
    _DEBUG_SAVED.add(kind)
    os.makedirs(DEBUG_DIR, exist_ok=True)
    path = os.path.join(DEBUG_DIR, f"{kind}_{utc_now().replace(':', '')}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"kind": kind, "saved_at": utc_now(), "payload": payload}, f, ensure_ascii=False, default=str)
        print(f"  [debug] sample saved -> {path}")
    except OSError as exc:
        print(f"  [debug] could not save sample: {exc}")


def parse_maybe_json(value):
    """Gamma returns some list fields (outcomePrices, clobTokenIds) as JSON strings."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
    return value


def fetch_active_markets(limit: int = 150) -> list:
    params = {
        "active": "true",
        "closed": "false",
        "limit": limit,
        "order": "volumeNum",
        "ascending": "false",
    }
    resp = requests.get(f"{GAMMA_API}/markets", params=params, timeout=TIMEOUT_S)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("markets"), list):
        return data["markets"]
    dump_debug("gamma_markets_unexpected_shape", data)
    return []


def fetch_orderbook(token_id: str):
    try:
        resp = requests.get(f"{CLOB_API}/book", params={"token_id": token_id}, timeout=TIMEOUT_S)
        resp.raise_for_status()
        book = resp.json()
        if not isinstance(book, dict) or ("bids" not in book and "asks" not in book):
            dump_debug("clob_book_unexpected_shape", book)
        return book
    except requests.RequestException as exc:
        print(f"  [warn] orderbook fetch failed for {token_id[:16]}…: {exc}")
        return None
    except ValueError:
        dump_debug("clob_book_not_json", resp.text[:2000])
        return None


def fetch_top_holders(condition_id: str):
    """Best-effort; scoring falls back to a placeholder if this is unusable."""
    try:
        resp = requests.get(
            f"{DATA_API}/holders", params={"market": condition_id, "limit": 10}, timeout=TIMEOUT_S
        )
        resp.raise_for_status()
        holders = resp.json()
        if not isinstance(holders, (list, dict)):
            dump_debug("holders_unexpected_shape", holders)
        return holders
    except requests.RequestException as exc:
        print(f"  [warn] holders fetch failed for {condition_id[:16]}…: {exc}")
        return None
    except ValueError:
        dump_debug("holders_not_json", resp.text[:2000])
        return None


def build_snapshot() -> dict:
    ts = utc_now()
    print(f"EventLens fetch @ {ts}")
    markets = fetch_active_markets()
    print(f"Gamma returned {len(markets)} active markets; keeping top {N_MARKETS} usable.")

    records = []
    for m in markets:
        if len(records) >= N_MARKETS:
            break
        if not isinstance(m, dict):
            dump_debug("gamma_market_row_unexpected", m)
            continue

        token_ids = parse_maybe_json(m.get("clobTokenIds")) or []
        prices = parse_maybe_json(m.get("outcomePrices")) or []
        if not token_ids or not m.get("endDate"):
            continue  # need a tradeable book and a deadline to be scoreable

        yes_token = str(token_ids[0])
        book = fetch_orderbook(yes_token)
        time.sleep(REQUEST_PAUSE_S)
        holders = fetch_top_holders(m.get("conditionId", "")) if m.get("conditionId") else None
        time.sleep(REQUEST_PAUSE_S)

        records.append(
            {
                "market_id": str(m.get("id")),
                "condition_id": m.get("conditionId"),
                "question": m.get("question"),
                "slug": m.get("slug"),
                "category": (str(m.get("category") or "Other")).strip() or "Other",
                "resolution_text": m.get("description"),
                "end_date": m.get("endDate"),
                "created_at": m.get("createdAt"),
                "yes_price_gamma": safe_float(prices[0]) if prices else None,
                "best_bid": safe_float(m.get("bestBid")),
                "best_ask": safe_float(m.get("bestAsk")),
                "volume_usd": safe_float(m.get("volumeNum"), default=safe_float(m.get("volume"), 0.0)),
                "liquidity_usd": safe_float(m.get("liquidityNum"), default=safe_float(m.get("liquidity"), 0.0)),
                "yes_token_id": yes_token,
                "orderbook": book,        # full book preserved — depth computed at scoring time
                "holders_raw": holders,   # may be None; concentration falls back gracefully
                "observed_at": ts,
            }
        )
        print(f"  [{len(records):>2}] {str(m.get('question'))[:70]}")

    return {
        "snapshot_type": "raw",
        "platform": "Polymarket",
        "fetched_at": ts,
        "n_markets": len(records),
        "markets": records,
    }


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    snapshot = build_snapshot()
    # Append-only: filename carries the timestamp; never overwrite a prior file.
    fname = f"raw_snapshot_{snapshot['fetched_at'].replace(':', '').replace('-', '')}.json"
    path = os.path.join(RAW_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False)
    print(f"\nWrote {snapshot['n_markets']} markets -> {path}")


if __name__ == "__main__":
    main()


# =============================================================================
# FILE: scripts/score_markets.py
# =============================================================================
"""
Read the latest raw snapshot, compute EventLens v0.1 trust subscores, append
score rows to the processed JSONL log, and export scored_markets.json.

HARD RULE: final outcomes and Brier data never appear in this file's inputs.
Scores are ex-ante by construction.
"""

import glob
import json
import os
import re
import statistics
from datetime import datetime, timezone

SCORE_VERSION = "v0.1"
RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
SNAPSHOT_LOG = os.path.join(PROCESSED_DIR, "snapshots.jsonl")   # append-only
DASHBOARD_JSON = os.path.join("data", "scored_markets.json")    # latest view only

WEIGHTS = {"liquidity": 30, "concentration": 25, "resolution": 25, "calibration": 20}

# --- Category calibration baseline ------------------------------------------
# Starts EMPTY by design. resolution_tracker.py (v0.2) fills resolved-market
# Brier stats per category. Until then the global prior dominates via shrinkage.
GLOBAL_PRIOR_BRIER = 0.10
SHRINKAGE_K = 50            # weight_category = n / (n + K)
CALIBRATION_TABLE = {}


def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, round(x)))


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_float(x, default=None):
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


# --- Microstructure features --------------------------------------------------

def book_depth_within(book, mid, pct):
    """USD depth (both sides) within ±pct of mid price."""
    if not book or mid is None:
        return None
    lo, hi = mid * (1 - pct), mid * (1 + pct)
    depth = 0.0
    for side in ("bids", "asks"):
        for lvl in book.get(side, []) or []:
            if not isinstance(lvl, dict):
                continue
            price = safe_float(lvl.get("price"))
            size = safe_float(lvl.get("size"))
            if price is None or size is None:
                continue
            if lo <= price <= hi:
                depth += price * size
    return depth


def best_bid_ask(book, fallback_bid=None, fallback_ask=None):
    bid, ask = None, None
    if book and isinstance(book, dict):
        bid_prices = [safe_float(l.get("price")) for l in (book.get("bids") or []) if isinstance(l, dict)]
        ask_prices = [safe_float(l.get("price")) for l in (book.get("asks") or []) if isinstance(l, dict)]
        bid_prices = [p for p in bid_prices if p is not None]
        ask_prices = [p for p in ask_prices if p is not None]
        bid = max(bid_prices) if bid_prices else None
        ask = min(ask_prices) if ask_prices else None
    bid = bid if bid is not None else safe_float(fallback_bid)
    ask = ask if ask is not None else safe_float(fallback_ask)
    return bid, ask


# --- Subscores ----------------------------------------------------------------

def liquidity_score(spread_cents, depth_1pct, depth_5pct, volume_usd, liquidity_usd):
    """40% spread, 30% depth, 20% volume, 10% liquidity parameter."""
    if spread_cents is None:
        spread_pts = 30  # unknown spread: penalize but don't zero out
    else:
        spread_pts = clamp(100 - spread_cents * 12)          # 0c->100, ~8c->~4
    d1 = depth_1pct or 0.0
    d5 = depth_5pct or 0.0
    depth_pts = clamp(min(d1 / 5000.0, 1.0) * 60 + min(d5 / 25000.0, 1.0) * 40)
    volume_pts = clamp(min((volume_usd or 0) / 1_000_000.0, 1.0) * 100)
    liq_pts = clamp(min((liquidity_usd or 0) / 100_000.0, 1.0) * 100)
    score = 0.40 * spread_pts + 0.30 * depth_pts + 0.20 * volume_pts + 0.10 * liq_pts
    reason = (
        f"Spread {spread_cents:.1f}c, ±1% depth ${d1:,.0f}, ±5% depth ${d5:,.0f}"
        if spread_cents is not None
        else "Spread unobserved; depth/volume only"
    )
    return clamp(score), reason


def concentration_score(holders_raw):
    """Real score if holders data parsed; explicit placeholder otherwise.
    Returns (score, reason, is_placeholder)."""
    shares = []
    if holders_raw:
        candidates = holders_raw if isinstance(holders_raw, list) else None
        if candidates is None and isinstance(holders_raw, dict):
            for v in holders_raw.values():
                if isinstance(v, list):
                    candidates = v
                    break
        if candidates:
            amounts = []
            for h in candidates:
                if isinstance(h, dict):
                    for key in ("amount", "shares", "balance", "size"):
                        if key in h:
                            val = safe_float(h[key])
                            if val is not None:
                                amounts.append(val)
                            break
            total = sum(amounts)
            if total > 0:
                shares = sorted((a / total for a in amounts), reverse=True)

    if not shares:
        return 50, "Holder data unavailable — placeholder score (low confidence)", True

    largest = shares[0]
    top5 = sum(shares[:5])
    score = 100 - clamp(largest * 130) * 0.6 - clamp(max(top5 - 0.5, 0) * 160) * 0.4
    reason = f"Largest tracked holder ≈ {largest:.0%}, top-5 ≈ {top5:.0%} of tracked exposure"
    return clamp(score), reason, False


AMBIGUOUS_TRIGGERS = re.compile(
    r"\b(announce[sd]?|resign[s]?|intend[s]?|plan[s]?|expected|reportedly|widely|rumor)\b", re.I
)
SOURCE_WORDS = re.compile(
    r"\b(resolution source|will resolve|according to|official|consensus of (credible )?reporting)\b", re.I
)
INSIDER_CATEGORIES = re.compile(
    r"\b(acquisition|merger|resign|fired|steps? down|appoint|injur|indict|arrest)\b", re.I
)


def resolution_clarity_score(resolution_text, question):
    """v0.1 keyword heuristic. Same penalty schema the v0.2 LLM analyzer will use."""
    text = (resolution_text or "").strip()
    flags, penalty = [], 0
    if len(text) < 80:
        penalty += 25
        flags.append("Resolution text very short — criteria likely underspecified")
    if not SOURCE_WORDS.search(text):
        penalty += 20
        flags.append("No explicit resolution source / source hierarchy")
    if AMBIGUOUS_TRIGGERS.search(question or "") or AMBIGUOUS_TRIGGERS.search(text):
        penalty += 15
        flags.append("Potentially ambiguous trigger language (announce/resign/expected)")
    if INSIDER_CATEGORIES.search(question or ""):
        penalty += 15
        flags.append("Insider-risk category (corporate action / personnel / injury)")
    if "ET" not in text and "UTC" not in text and re.search(r"\bby\b", (question or ""), re.I):
        penalty += 5
        flags.append("Deadline present but time zone not clearly stated")
    score = clamp(100 - penalty)
    reason = flags[0] if flags else "No heuristic resolution-risk flags"
    return score, reason, flags


def category_calibration_score(category):
    """Shrinkage-blended category Brier -> score. Low confidence at small n."""
    entry = CALIBRATION_TABLE.get(category, {"brier": GLOBAL_PRIOR_BRIER, "n": 0})
    n = entry.get("n", 0)
    w = n / (n + SHRINKAGE_K)
    blended_brier = w * entry["brier"] + (1 - w) * GLOBAL_PRIOR_BRIER
    score = clamp(100 - blended_brier * 350)
    confidence = "high" if n >= 100 else "medium" if n >= 30 else "low"
    reason = f"Blended category Brier {blended_brier:.3f} (n={n} resolved, shrinkage w={w:.2f})"
    return score, reason, confidence, n


def composite(subscores):
    """100 minus weighted deductions; identical math to the dashboard drivers panel."""
    total_ded = 0
    drivers = []
    for dim, (sub, reason) in subscores.items():
        ded = round(WEIGHTS[dim] * (100 - sub) / 100)
        total_ded += ded
        drivers.append(
            {"dimension": dim.capitalize(), "deduction": ded, "max_deduction": WEIGHTS[dim], "reason": reason}
        )
    return clamp(100 - total_ded), drivers


# --- Main ---------------------------------------------------------------------

def latest_raw_snapshot():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "raw_snapshot_*.json")))
    if not files:
        raise SystemExit("No raw snapshots found. Run fetch_polymarket_markets.py first.")
    with open(files[-1], encoding="utf-8") as f:
        return json.load(f), files[-1]


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    raw, raw_path = latest_raw_snapshot()
    scored_at = utc_now()
    print(f"Scoring {raw['n_markets']} markets from {os.path.basename(raw_path)} (model {SCORE_VERSION})")

    rows = []
    for m in raw["markets"]:
        bid, ask = best_bid_ask(m.get("orderbook"), m.get("best_bid"), m.get("best_ask"))
        mid = (bid + ask) / 2 if bid is not None and ask is not None else safe_float(m.get("yes_price_gamma"))
        spread_c = (ask - bid) * 100 if bid is not None and ask is not None else None

        liq, liq_reason = liquidity_score(
            spread_c,
            book_depth_within(m.get("orderbook"), mid, 0.01),
            book_depth_within(m.get("orderbook"), mid, 0.05),
            safe_float(m.get("volume_usd"), 0.0),
            safe_float(m.get("liquidity_usd"), 0.0),
        )
        conc, conc_reason, conc_placeholder = concentration_score(m.get("holders_raw"))
        res, res_reason, res_flags = resolution_clarity_score(m.get("resolution_text"), m.get("question"))
        cal, cal_reason, cal_conf, cal_n = category_calibration_score(m.get("category"))

        trust, drivers = composite(
            {
                "liquidity": (liq, liq_reason),
                "concentration": (conc, conc_reason),
                "resolution": (res, res_reason),
                "calibration": (cal, cal_reason),
            }
        )

        rows.append(
            {
                "market_id": m["market_id"],
                "condition_id": m.get("condition_id"),
                "platform": "Polymarket",
                "question": m.get("question"),
                "category": m.get("category"),
                "url": f"https://polymarket.com/market/{m.get('slug')}" if m.get("slug") else None,
                "price": round(mid, 4) if mid is not None else None,
                "spread_cents": round(spread_c, 2) if spread_c is not None else None,
                "volume_usd": m.get("volume_usd"),
                "end_date": m.get("end_date"),
                "liquidity_score": liq,
                "concentration_score": conc,
                "concentration_is_placeholder": conc_placeholder,
                "resolution_clarity_score": res,
                "resolution_flags": res_flags,
                "resolution_llm_analyzed": False,  # flips true in v0.2
                "category_calibration_score": cal,
                "calibration_confidence": cal_conf,
                "calibration_sample_n": cal_n,
                "composite_trust_score": trust,
                "drivers": drivers,
                "score_version": SCORE_VERSION,
                "observed_at": m.get("observed_at"),
                "scored_at": scored_at,
                # Final outcome / Brier fields live in validation tables ONLY,
                # filled by resolution_tracker.py — never here.
            }
        )

    # Append-only score log.
    with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Latest dashboard view (a view, not the record — overwriting is fine here).
    with open(DASHBOARD_JSON, "w", encoding="utf-8") as f:
        json.dump(
            {"score_version": SCORE_VERSION, "generated_at": scored_at, "markets": rows},
            f, ensure_ascii=False, indent=2,
        )

    # --- Diagnostics ----------------------------------------------------------
    n = len(rows)
    trusts = [r["composite_trust_score"] for r in rows]
    print("\nDiagnostics")
    print(f"  Rows scored:                {n}")
    print(f"  Missing price:              {sum(r['price'] is None for r in rows)}")
    print(f"  Missing spread:             {sum(r['spread_cents'] is None for r in rows)}")
    print(f"  Concentration placeholders: {sum(r['concentration_is_placeholder'] for r in rows)}")
    print(f"  Category = 'Other':         {sum(r['category'] == 'Other' for r in rows)}")
    if n:
        print(f"  Trust score avg:            {sum(trusts)/n:.1f}")
        print(f"  Trust score min/max:        {min(trusts)} / {max(trusts)}")
        if n > 1:
            sd = statistics.stdev(trusts)
            print(f"  Trust score stdev:          {sd:.1f}" + ("   [WARNING: <8 — scores may lack discriminating power]" if sd < 8 else ""))

    rows.sort(key=lambda r: r["composite_trust_score"], reverse=True)
    print(f"\n{'Trust':>5}  {'Liq':>3} {'Con':>3} {'Res':>3} {'Cal':>3}  Question")
    for r in rows[:15]:
        print(
            f"{r['composite_trust_score']:>5}  {r['liquidity_score']:>3} {r['concentration_score']:>3} "
            f"{r['resolution_clarity_score']:>3} {r['category_calibration_score']:>3}  {str(r['question'])[:60]}"
        )
    print(f"\nAppended {len(rows)} rows -> {SNAPSHOT_LOG}")
    print(f"Dashboard feed -> {DASHBOARD_JSON}")


if __name__ == "__main__":
    main()


# =============================================================================
# FILE: README_eventlens_pipeline.md
# =============================================================================
# # EventLens v0.1 pipeline (Polymarket)
#
# ## Setup
#     pip install requests
#     mkdir -p data/raw data/processed data/debug scripts
#
# ## Run (daily, manually or via cron)
#     python scripts/fetch_polymarket_markets.py
#     python scripts/score_markets.py
#
# ## Outputs
# - data/raw/raw_snapshot_<ts>.json   — exact market state as observed (append-only)
# - data/processed/snapshots.jsonl    — one scored row per market per run (append-only)
# - data/scored_markets.json          — latest scores for the dashboard (a view)
# - data/debug/                       — samples of unexpected API responses
#
# ## Methodology rules (do not break these)
# 1. Scores are ex-ante: computed and timestamped strictly before resolution.
#    Final outcomes and Brier errors never enter scoring inputs.
# 2. Nothing historical is overwritten. Formula changes increment score_version.
# 3. Placeholders are explicit (concentration_is_placeholder,
#    resolution_llm_analyzed=False).
# 4. Category calibration uses shrinkage (n/(n+50)) toward a global prior and
#    reports confidence; low-confidence until resolved samples accumulate.
#
# ## After first run, inspect
# - diagnostics block in score output (placeholders, nulls, 'Other' count,
#   trust-score spread — stdev < 8 means weak discriminating power)
# - data/debug/ for any saved API-shape samples
#
# ## v0.2 roadmap (next: resolution_tracker.py)
# - detect resolved markets, store outcomes in data/validation/, compute Brier
#   per historical snapshot, populate CALIBRATION_TABLE from real data
# - LLM resolution analyzer replacing the keyword heuristic (same schema)
# - wallet-level concentration from on-chain OrderFilled events (do not infer
#   trade direction from the public book feed)
# =============================================================================