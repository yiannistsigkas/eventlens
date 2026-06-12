"""
Fetch a stratified sample of Polymarket markets, order books, and (best-effort)
top holders. Writes one append-only raw snapshot file per run. No scoring here.

Sampling (v0.2): the sample is built for VALIDATION SPEED, not just volume.
Top-volume-only sampling yields liquid but slow-resolving markets (World Cup
outrights, 2028 politics) that starve the Brier validation loop. Buckets:

  top_volume        30  liquid benchmark markets
  short_horizon     30  soonest-ending (<=30d) active markets — fast validation
  low_liquidity     20  thin books with some volume — stress-test trust score
  category_diverse  20  round-robin over underrepresented categories

Deduplicated by market id; every record carries its sample_bucket.

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
from datetime import datetime, timedelta, timezone

import requests

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
DATA_API = "https://data-api.polymarket.com"

RAW_DIR = os.path.join("data", "raw")
DEBUG_DIR = os.path.join("data", "debug")

BUCKET_TARGETS = [
    ("top_volume", 30),
    ("short_horizon", 30),
    ("low_liquidity", 20),
    ("category_diverse", 20),
]
VOLUME_FLOOR_USD = 100      # keeps short-horizon/low-liquidity buckets tradeable, not dead
SHORT_HORIZON_DAYS = 30
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


def extract_category(m: dict) -> str:
    """Top-level 'category' disappeared from Gamma /markets responses.
    With include_tag=true each market carries a tags list whose first label
    is the broad category ('Sports', 'Politics', 'Culture', ...)."""
    cat = (str(m.get("category") or "")).strip()
    if cat:
        return cat
    for t in m.get("tags") or []:
        if isinstance(t, dict):
            label = (str(t.get("label") or "")).strip()
            if label:
                return label
    return "Other"


def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_maybe_json(value):
    """Gamma returns some list fields (outcomePrices, clobTokenIds) as JSON strings."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
    return value


def gamma_markets(extra_params: dict, limit: int) -> list:
    params = {
        "active": "true",
        "closed": "false",
        "limit": limit,
        "include_tag": "true",  # markets no longer carry a top-level category; first tag label fills the role
    }
    params.update(extra_params)
    resp = requests.get(f"{GAMMA_API}/markets", params=params, timeout=TIMEOUT_S)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("markets"), list):
        return data["markets"]
    dump_debug("gamma_markets_unexpected_shape", data)
    return []


def gamma_markets_paged(extra_params: dict, min_usable: int, max_pages: int = 5) -> list:
    """Gamma caps limit at 100 per request; page with offset until the
    candidate list holds enough usable (non-expired, tradeable) markets."""
    out, seen, n_usable = [], set(), 0
    for page in range(max_pages):
        rows = gamma_markets({**extra_params, "offset": page * 100}, limit=100)
        if not rows:
            break
        for m in rows:
            mid = str(m.get("id")) if isinstance(m, dict) else None
            if mid is None or mid in seen:
                continue
            seen.add(mid)
            out.append(m)
            if usable(m):
                n_usable += 1
        if n_usable >= min_usable:
            break
    return out


def usable(m) -> bool:
    """Scoreable = has a tradeable book and a deadline still in the future.
    Gamma returns some 'active' markets whose endDate is already past — stale
    artifacts that can never enter validation, so exclude them from every bucket."""
    if not isinstance(m, dict):
        dump_debug("gamma_market_row_unexpected", m)
        return False
    if not (parse_maybe_json(m.get("clobTokenIds")) or []):
        return False
    end = parse_ts(m.get("endDate"))
    return end is not None and end > datetime.now(timezone.utc)


def build_sample() -> list:
    """Returns [(bucket_name, market_dict), ...] deduplicated by market id."""
    now = datetime.now(timezone.utc)
    chosen, chosen_ids = [], set()
    cat_counts = {}

    def take(bucket, candidates, target):
        n = 0
        for m in candidates:
            if n >= target:
                break
            if not usable(m):
                continue
            mid = str(m.get("id"))
            if mid in chosen_ids:
                continue
            chosen.append((bucket, m))
            chosen_ids.add(mid)
            cat = extract_category(m)
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
            n += 1
        print(f"  bucket {bucket:<17} filled {n}")

    targets = dict(BUCKET_TARGETS)

    take("top_volume",
         gamma_markets({"order": "volumeNum", "ascending": "false"}, limit=100),
         targets["top_volume"])

    take("short_horizon",
         gamma_markets({
             "order": "endDate", "ascending": "true",
             "end_date_min": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
             "end_date_max": (now + timedelta(days=SHORT_HORIZON_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "volume_num_min": VOLUME_FLOOR_USD,
         }, limit=100),
         targets["short_horizon"])

    # The lowest-liquidity "active" markets are mostly stale/expired, so this
    # bucket needs paging to find enough live ones.
    take("low_liquidity",
         gamma_markets_paged({"order": "liquidityNum", "ascending": "true",
                              "volume_num_min": VOLUME_FLOOR_USD},
                             min_usable=targets["low_liquidity"] * 2),
         targets["low_liquidity"])

    # Category-diverse: round-robin the categories least represented so far.
    pool = gamma_markets_paged({"order": "volumeNum", "ascending": "false",
                                "volume_num_min": VOLUME_FLOOR_USD},
                               min_usable=120, max_pages=3)
    by_cat = {}
    for m in pool:
        if not usable(m) or str(m.get("id")) in chosen_ids:
            continue
        by_cat.setdefault(extract_category(m), []).append(m)
    n = 0
    while n < targets["category_diverse"] and by_cat:
        cat = min(by_cat, key=lambda c: (cat_counts.get(c, 0), c))
        m = by_cat[cat].pop(0)
        if not by_cat[cat]:
            del by_cat[cat]
        chosen.append(("category_diverse", m))
        chosen_ids.add(str(m.get("id")))
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        n += 1
    print(f"  bucket category_diverse  filled {n}")

    return chosen


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
    print("Building stratified sample:")
    sample = build_sample()
    print(f"Sample size after dedup: {len(sample)}")

    records = []
    for bucket, m in sample:
        token_ids = parse_maybe_json(m.get("clobTokenIds")) or []
        outcome_labels = parse_maybe_json(m.get("outcomes")) or []
        prices = parse_maybe_json(m.get("outcomePrices")) or []

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
                "category": extract_category(m),
                "sample_bucket": bucket,
                "resolution_text": m.get("description"),
                "end_date": m.get("endDate"),
                "created_at": m.get("createdAt"),
                "outcome_labels": outcome_labels,
                "outcome_token_ids": [str(token_id) for token_id in token_ids],
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
        print(f"  [{len(records):>3}] ({bucket}) {str(m.get('question'))[:60]}")

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
