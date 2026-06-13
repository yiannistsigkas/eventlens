"""
Read the latest raw snapshot, compute EventLens v0.2 trust subscores, append
score rows to the processed JSONL log, and export scored_markets.json.

HARD RULE: final outcomes and Brier data never appear in this file's inputs.
Scores are ex-ante by construction.
"""

import glob
import json
import os
import re
import statistics
from collections import Counter
from datetime import datetime, timezone

SCORE_VERSION = "v0.2"      # v0.2: stronger resolution heuristic + horizon fields
RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
SNAPSHOT_LOG = os.path.join(PROCESSED_DIR, "snapshots.jsonl")   # append-only
DASHBOARD_JSON = os.path.join("data", "scored_markets.json")    # latest view only
CALIBRATION_TABLE_PATH = os.path.join("data", "validation", "calibration_table.json")

WEIGHTS = {"liquidity": 30, "concentration": 25, "resolution": 25, "calibration": 20}

# --- Category calibration baseline ------------------------------------------
# resolution_tracker.py rebuilds calibration_table.json from resolved-market
# Brier stats per category. Until samples accumulate the global prior
# dominates via shrinkage.
GLOBAL_PRIOR_BRIER = 0.10
SHRINKAGE_K = 50            # weight_category = n / (n + K)


def load_calibration_table():
    try:
        with open(CALIBRATION_TABLE_PATH, encoding="utf-8") as f:
            table = json.load(f)
        return table if isinstance(table, dict) else {}
    except (OSError, ValueError):
        return {}


CALIBRATION_TABLE = load_calibration_table()


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


def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def days_to_resolution(end_date, observed_at):
    """Negative = observed AFTER the deadline (stale unresolved market).
    Any post-deadline observation returns <= -1 so rounding can never
    disguise an expired market as a 0-7d one."""
    end, obs = parse_ts(end_date), parse_ts(observed_at)
    if end is None or obs is None:
        return None
    days = (end - obs).total_seconds() / 86400
    if days < 0:
        return min(round(days), -1)
    return round(days)


def horizon_bucket(days):
    if days is None:
        return None
    if days < 0:
        return "expired_unresolved"
    if days <= 7:
        return "0-7d"
    if days <= 30:
        return "8-30d"
    if days <= 90:
        return "31-90d"
    return "90d+"


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


def spread_missing_reason(book, fallback_bid=None, fallback_ask=None, fetch_status=None):
    """Explain why a two-sided spread cannot be observed without changing scoring."""
    bid, ask = best_bid_ask(book, fallback_bid, fallback_ask)
    if bid is not None and ask is not None:
        return None
    if fetch_status in ("request_failed", "invalid_json", "unexpected_shape"):
        return f"orderbook_{fetch_status}"
    if bid is None and ask is None:
        return "empty_book"
    if bid is None:
        return "missing_bid"
    return "missing_ask"


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


def _holder_candidates(holders_raw, yes_token_id=None):
    """Locate the list of holder dicts inside whatever shape the Data API returned.
    Current shape: [{"token": <id>, "holders": [{"amount": ...}, ...]}, ...] — one
    entry per outcome token. Prefer the entry matching the YES token we scored;
    older flat-list and dict-wrapped shapes still work."""
    if isinstance(holders_raw, list):
        token_entries = [
            e for e in holders_raw if isinstance(e, dict) and isinstance(e.get("holders"), list)
        ]
        if token_entries:
            if yes_token_id is not None:
                for e in token_entries:
                    if str(e.get("token")) == str(yes_token_id):
                        return e["holders"]
            return token_entries[0]["holders"]
        return holders_raw
    if isinstance(holders_raw, dict):
        for v in holders_raw.values():
            if isinstance(v, list):
                return v
    return None


def concentration_score(holders_raw, yes_token_id=None):
    """Real score if holders data parsed; explicit placeholder otherwise.
    Returns (score, reason, is_placeholder)."""
    shares = []
    if holders_raw:
        candidates = _holder_candidates(holders_raw, yes_token_id)
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
UNVERIFIABLE_OR_METAPHYSICAL = re.compile(
    r"\b(Jesus|Christ|God|alien|aliens|UFO|prophecy|rapture|miracle)\b", re.I
)
SUBJECTIVE_CONSENSUS = re.compile(
    r"\b(credible reporting|credible sources|widely accepted|general consensus|mainstream media)\b", re.I
)


def resolution_clarity_score(resolution_text, question, price=None, days_to_res=None):
    """v0.2 keyword heuristic. The question is not just 'is there a source?'
    but 'can this market resolve cleanly under plausible edge cases?'.
    Flags carry stable ids and their penalty so attribution survives label
    rewording (v0.2.1 taxonomy; penalties unchanged from v0.2)."""
    text = (resolution_text or "").strip()
    flags, penalty = [], 0

    def flag(fid, pts, label):
        nonlocal penalty
        penalty += pts
        flags.append({"id": fid, "penalty": pts, "label": label})

    if len(text) < 80:
        flag("RES_TEXT_SHORT", 25, "Resolution text very short — criteria likely underspecified")
    if not SOURCE_WORDS.search(text):
        flag("NO_SOURCE_HIERARCHY", 20, "No explicit resolution source / source hierarchy")
    if UNVERIFIABLE_OR_METAPHYSICAL.search(question or "") or UNVERIFIABLE_OR_METAPHYSICAL.search(text):
        flag("UNVERIFIABLE_SUBJECT", 25, "Subject matter hard to verify objectively (metaphysical/paranormal)")
    if SUBJECTIVE_CONSENSUS.search(text):
        flag("SUBJECTIVE_CONSENSUS", 15, "Resolution depends on subjective consensus of reporting")
    if AMBIGUOUS_TRIGGERS.search(question or "") or AMBIGUOUS_TRIGGERS.search(text):
        flag("AMBIGUOUS_TRIGGER", 15, "Potentially ambiguous trigger language (announce/resign/expected)")
    if INSIDER_CATEGORIES.search(question or ""):
        flag("INSIDER_RISK", 15, "Insider-risk category (corporate action / personnel / injury)")
    if price is not None and days_to_res is not None and price < 0.01 and days_to_res > 180:
        flag("LONGSHOT_DISTANT", 10, "Deep longshot (<1c) with distant deadline — edge cases rarely tested")
    if "ET" not in text and "UTC" not in text and re.search(r"\bby\b", (question or ""), re.I):
        flag("DEADLINE_TZ_UNCLEAR", 5, "Deadline present but time zone not clearly stated")
    score = clamp(100 - penalty)
    reason = flags[0]["label"] if flags else "No heuristic resolution-risk flags"
    return score, reason, flags


# --- Market type (metadata only — never enters scoring) ------------------------

SPORTS_PROP_PAT = re.compile(
    r"(O/U|over/under|spread|exact score|home runs?|odd/even|1st \d|innings|"
    r"\d\+ (goals?|assists?|shots?|points?|rebounds?)|map \d|quadra kill|roshan|match o/u)", re.I
)
CRYPTO_PRICE_PAT = re.compile(r"\b(up or down|bitcoin|ethereum|solana|xrp|bnb|doge|price of)\b", re.I)
ELECTION_PAT = re.compile(r"\b(election|nomination|nominee|president|presidential|primary|primaries|senate|governor)\b", re.I)


def classify_market_type(question, category):
    q = question or ""
    cat = (category or "").lower()
    if "crypto" in cat or cat in ("bitcoin", "ethereum") or CRYPTO_PRICE_PAT.search(q):
        return "crypto_price"
    if ELECTION_PAT.search(q):
        return "election"
    if cat == "sports" or SPORTS_PROP_PAT.search(q):
        return "sports_prop" if SPORTS_PROP_PAT.search(q) else "sports_outcome"
    if INSIDER_CATEGORIES.search(q):
        return "corporate_personnel_event"
    if UNVERIFIABLE_OR_METAPHYSICAL.search(q):
        return "unverifiable_event"
    return "news_event"


def validation_eligibility(market, price):
    """Return an ex-ante eligibility decision and stable reason codes."""
    reasons = []
    end_dt = parse_ts(market.get("end_date"))
    obs_dt = parse_ts(market.get("observed_at"))
    outcome_labels = market.get("outcome_labels")
    outcome_token_ids = market.get("outcome_token_ids")

    if price is None or not 0 <= price <= 1:
        reasons.append("PRICE_MISSING_OR_INVALID")
    if end_dt is None or obs_dt is None or obs_dt >= end_dt:
        reasons.append("NOT_OBSERVED_BEFORE_DEADLINE")
    for field in ("market_id", "condition_id", "question"):
        if not market.get(field):
            reasons.append(f"MISSING_{field.upper()}")

    # Older raw snapshots predate these fields. They came from the same binary
    # Gamma market endpoint, so retain them with an explicit legacy inference.
    if outcome_labels is not None and len(outcome_labels) != 2:
        reasons.append("NOT_BINARY_OUTCOME")
    if outcome_token_ids is not None and len(outcome_token_ids) != 2:
        reasons.append("NOT_BINARY_TOKEN_SET")

    source = "explicit_binary_metadata" if outcome_labels is not None else "legacy_inference"
    return not reasons, reasons, source


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


def existing_snapshot_keys():
    keys = set()
    if not os.path.exists(SNAPSHOT_LOG):
        return keys
    with open(SNAPSHOT_LOG, encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except (TypeError, ValueError):
                continue
            keys.add((str(row.get("market_id")), row.get("score_version"), row.get("observed_at")))
    return keys


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
        spread_reason = spread_missing_reason(
            m.get("orderbook"),
            m.get("best_bid"),
            m.get("best_ask"),
            m.get("orderbook_fetch_status"),
        )
        d2r = days_to_resolution(m.get("end_date"), m.get("observed_at"))
        market_type = classify_market_type(m.get("question"), m.get("category"))
        validation_eligible, validation_ineligible_reasons, eligibility_source = validation_eligibility(m, mid)

        liq, liq_reason = liquidity_score(
            spread_c,
            book_depth_within(m.get("orderbook"), mid, 0.01),
            book_depth_within(m.get("orderbook"), mid, 0.05),
            safe_float(m.get("volume_usd"), 0.0),
            safe_float(m.get("liquidity_usd"), 0.0),
        )
        conc, conc_reason, conc_placeholder = concentration_score(m.get("holders_raw"), m.get("yes_token_id"))
        res, res_reason, res_flags = resolution_clarity_score(
            m.get("resolution_text"), m.get("question"), price=mid, days_to_res=d2r
        )
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
                "sample_bucket": m.get("sample_bucket"),
                "market_type": market_type,
                "price": round(mid, 4) if mid is not None else None,
                "spread_cents": round(spread_c, 2) if spread_c is not None else None,
                "spread_is_missing": spread_c is None,  # one-sided books are themselves a quality signal
                "spread_missing_reason": spread_reason,
                "volume_usd": m.get("volume_usd"),
                "end_date": m.get("end_date"),
                "days_to_resolution": d2r,
                "horizon_bucket": horizon_bucket(d2r),
                "liquidity_score": liq,
                "concentration_score": conc,
                "concentration_is_placeholder": conc_placeholder,
                "resolution_clarity_score": res,
                "resolution_flags": res_flags,
                "resolution_llm_analyzed": False,  # still a keyword heuristic in v0.2; flips true when the LLM analyzer lands
                "category_calibration_score": cal,
                "calibration_confidence": cal_conf,
                "calibration_sample_n": cal_n,
                "composite_trust_score": trust,
                "drivers": drivers,
                "score_version": SCORE_VERSION,
                "validation_eligible": validation_eligible,
                "validation_ineligible_reasons": validation_ineligible_reasons,
                "validation_eligibility_source": eligibility_source,
                "observed_at": m.get("observed_at"),
                "scored_at": scored_at,
                # Final outcome / Brier fields live in validation tables ONLY,
                # filled by resolution_tracker.py — never here.
            }
        )

    # Append-only score log, idempotent if a run is retried on the same raw
    # snapshot and score version.
    seen_keys = existing_snapshot_keys()
    new_rows = [
        row for row in rows
        if (str(row.get("market_id")), row.get("score_version"), row.get("observed_at")) not in seen_keys
    ]
    with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
        for row in new_rows:
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
    res_scores = [r["resolution_clarity_score"] for r in rows]
    d2rs = [r["days_to_resolution"] for r in rows if r["days_to_resolution"] is not None]
    hbuckets = Counter(r["horizon_bucket"] for r in rows if r["horizon_bucket"])
    cats = Counter(str(r["category"]) for r in rows)
    missing_spread_reasons = Counter(
        r["spread_missing_reason"] for r in rows if r["spread_is_missing"]
    )
    print("\nDiagnostics")
    print(f"  Rows scored:                {n}")
    print(f"  Missing price:              {sum(r['price'] is None for r in rows)}")
    print(f"  Missing spread:             {sum(r['spread_is_missing'] for r in rows)}")
    for reason, count in sorted(missing_spread_reasons.items()):
        print(f"    {reason:<25} {count}")
    print(f"  Concentration placeholders: {sum(r['concentration_is_placeholder'] for r in rows)}")
    print(f"  Category = 'Other':         {sum(r['category'] == 'Other' for r in rows)}")
    if n:
        print(f"  Trust score avg:            {sum(trusts)/n:.1f}")
        print(f"  Trust score min/max:        {min(trusts)} / {max(trusts)}")
        if n > 1:
            trust_sd = statistics.stdev(trusts)
            res_sd = statistics.stdev(res_scores)
            print(f"  Trust score stdev:          {trust_sd:.1f}")
            print(f"  Resolution score stdev:     {res_sd:.1f}")
        if d2rs:
            print(f"  Days to resolution:         min {min(d2rs)} / median {statistics.median(d2rs):.0f} / max {max(d2rs)}")
        print("  Horizon buckets:")
        for hb in ("0-7d", "8-30d", "31-90d", "90d+", "expired_unresolved"):
            if hb != "expired_unresolved" or hbuckets.get(hb):
                print(f"    {hb:<7} {hbuckets.get(hb, 0)}")
        print("  Categories:")
        for cat, cnt in cats.most_common():
            print(f"    {cat:<22} {cnt}")

        # Tripwires — keep the methodology honest.
        if n > 1 and trust_sd < 8:
            print("  WARNING: trust stdev < 8 — scores may lack discriminating power")
        if n > 1 and res_sd == 0:
            print("  WARNING: resolution stdev = 0 — heuristic not discriminating")
        if d2rs and sum(d > 180 for d in d2rs) / len(d2rs) > 0.70:
            print("  WARNING: >70% of markets resolve after 180 days — validation will be slow")
        if cats and cats.most_common(1)[0][1] / n > 0.50:
            print(f"  WARNING: >50% of markets from one category ({cats.most_common(1)[0][0]})")

    rows.sort(key=lambda r: r["composite_trust_score"], reverse=True)
    print(f"\n{'Trust':>5}  {'Liq':>3} {'Con':>3} {'Res':>3} {'Cal':>3}  Question")
    for r in rows[:15]:
        print(
            f"{r['composite_trust_score']:>5}  {r['liquidity_score']:>3} {r['concentration_score']:>3} "
            f"{r['resolution_clarity_score']:>3} {r['category_calibration_score']:>3}  {str(r['question'])[:60]}"
        )
    print(f"\nAppended {len(new_rows)} rows -> {SNAPSHOT_LOG} ({len(rows) - len(new_rows)} already recorded)")
    print(f"Dashboard feed -> {DASHBOARD_JSON}")


if __name__ == "__main__":
    main()
