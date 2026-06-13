"""
EventLens v0.2 — resolution tracker.

Detects resolved markets among previously scored snapshots, records outcomes
append-only in data/validation/resolutions.jsonl, computes ex-ante Brier per
historical snapshot row, and rebuilds the category calibration table consumed
by score_markets.py.

HARD RULES:
- Outcomes live in data/validation/ ONLY. This script never writes to
  data/raw/ or data/processed/, so scoring inputs stay ex-ante.
- A snapshot row joins a Brier outcome only if observed_at is strictly
  before the market's close time.
- resolutions.jsonl is the append-only record; brier_rows.json and
  calibration_table.json are derived views, regenerated each run.
"""

import json
import os
from datetime import datetime, timezone

import requests

GAMMA_API = "https://gamma-api.polymarket.com"
SNAPSHOT_LOG = os.path.join("data", "processed", "snapshots.jsonl")
VALIDATION_DIR = os.path.join("data", "validation")
RESOLUTIONS_LOG = os.path.join(VALIDATION_DIR, "resolutions.jsonl")        # append-only
BRIER_VIEW = os.path.join(VALIDATION_DIR, "brier_rows.json")               # regenerated view
CALIBRATION_JSON = os.path.join(VALIDATION_DIR, "calibration_table.json")  # regenerated view

BATCH_SIZE = 20
TIMEOUT_S = 30
RESOLUTION_EPSILON = 1e-6


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
    """Gamma emits both '2026-06-12T22:40:52Z' and '2026-06-12 22:40:52+00'."""
    if not s:
        return None
    s = str(s).strip().replace(" ", "T", 1).replace("Z", "+00:00")
    if s.endswith("+00"):
        s += ":00"
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def parse_maybe_json(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
    return value


def load_snapshot_rows():
    rows = []
    if not os.path.exists(SNAPSHOT_LOG):
        raise SystemExit("No score log found. Run score_markets.py first.")
    with open(SNAPSHOT_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_recorded_resolutions():
    recorded = {}
    if os.path.exists(RESOLUTIONS_LOG):
        with open(RESOLUTIONS_LOG, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    recorded[rec["market_id"]] = rec
    return recorded


def fetch_markets_by_id(ids):
    out = []
    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i + BATCH_SIZE]
        resp = requests.get(
            f"{GAMMA_API}/markets", params=[("id", mid) for mid in batch], timeout=TIMEOUT_S
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            out.extend(data)
    return out


def collapsed_binary_outcome(prices):
    """Return the first outcome as 0/1 when both prices cleanly collapse."""
    if not isinstance(prices, list) or len(prices) != 2:
        return None
    first, second = safe_float(prices[0]), safe_float(prices[1])
    if first is None or second is None:
        return None
    if abs(first - 1.0) <= RESOLUTION_EPSILON and abs(second) <= RESOLUTION_EPSILON:
        return 1.0
    if abs(first) <= RESOLUTION_EPSILON and abs(second - 1.0) <= RESOLUTION_EPSILON:
        return 0.0
    return None


def extract_resolution(m):
    """Return a resolution record if the market resolved cleanly, else None.
    Resolved = closed with both binary outcome prices collapsed to 1/0."""
    if not isinstance(m, dict) or not m.get("closed"):
        return None
    prices = parse_maybe_json(m.get("outcomePrices")) or []
    primary_outcome = collapsed_binary_outcome(prices)
    if primary_outcome is None:
        return None  # closed but not (yet) cleanly resolved — try again next run
    labels = parse_maybe_json(m.get("outcomes")) or []
    closed_time = m.get("closedTime") or m.get("umaEndDate") or m.get("endDate")
    if parse_ts(closed_time) is None:
        return None
    return {
        "market_id": str(m.get("id")),
        "condition_id": m.get("conditionId"),
        "question": m.get("question"),
        "outcome_primary": primary_outcome,
        "outcome_yes": primary_outcome,  # backward-compatible alias
        "primary_outcome_label": labels[0] if len(labels) == 2 else None,
        "winning_outcome_label": labels[0 if primary_outcome == 1.0 else 1] if len(labels) == 2 else None,
        "closed_time": closed_time,
        "detected_at": utc_now(),
    }


def snapshot_validation_eligibility(row):
    """Read the frozen decision, or deterministically infer it for legacy rows."""
    if "validation_eligible" in row:
        return bool(row["validation_eligible"]), row.get("validation_eligibility_source", "explicit")

    price = safe_float(row.get("price"))
    observed_at = parse_ts(row.get("observed_at"))
    end_date = parse_ts(row.get("end_date"))
    eligible = bool(
        price is not None and 0 <= price <= 1
        and observed_at is not None and end_date is not None and observed_at < end_date
        and row.get("market_id") and row.get("condition_id") and row.get("question")
    )
    return eligible, "legacy_inference"


def main():
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    rows = load_snapshot_rows()
    recorded = load_recorded_resolutions()

    tracked_ids = sorted({r["market_id"] for r in rows})
    pending = [mid for mid in tracked_ids if mid not in recorded]
    print(f"Tracking {len(tracked_ids)} markets ({len(recorded)} already resolved, {len(pending)} pending)")

    new_resolutions = []
    if pending:
        for m in fetch_markets_by_id(pending):
            rec = extract_resolution(m)
            if rec:
                new_resolutions.append(rec)

    if new_resolutions:
        with open(RESOLUTIONS_LOG, "a", encoding="utf-8") as f:
            for rec in new_resolutions:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                recorded[rec["market_id"]] = rec
    print(f"Newly resolved this run: {len(new_resolutions)}  (total resolved: {len(recorded)})")

    # --- Ex-ante Brier join ----------------------------------------------------
    brier_rows = []
    for r in rows:
        res = recorded.get(r["market_id"])
        validation_eligible, eligibility_source = snapshot_validation_eligibility(r)
        if not res or not validation_eligible or r.get("price") is None:
            continue
        t_close = parse_ts(res["closed_time"])
        t_obs = parse_ts(r.get("observed_at"))
        if t_close is None or t_obs is None or t_obs >= t_close:
            continue  # not ex-ante relative to close — never count it
        brier_rows.append(
            {
                "market_id": r["market_id"],
                "question": r.get("question"),
                "category": r.get("category"),
                "market_type": r.get("market_type"),
                "sample_bucket": r.get("sample_bucket"),
                "horizon_bucket": r.get("horizon_bucket"),
                "score_version": r.get("score_version"),
                "observed_at": r.get("observed_at"),
                "closed_time": res["closed_time"],
                "price": r["price"],
                "outcome_primary": res.get("outcome_primary", res["outcome_yes"]),
                "outcome_yes": res["outcome_yes"],
                "primary_outcome_label": res.get("primary_outcome_label"),
                "winning_outcome_label": res.get("winning_outcome_label"),
                "brier": (r["price"] - res["outcome_yes"]) ** 2,
                "composite_trust_score": r.get("composite_trust_score"),
                "spread_is_missing": r.get("spread_is_missing"),
                "spread_missing_reason": r.get("spread_missing_reason"),
                "validation_eligible": True,
                "validation_eligibility_source": eligibility_source,
            }
        )
    with open(BRIER_VIEW, "w", encoding="utf-8") as f:
        json.dump({"generated_at": utc_now(), "n_rows": len(brier_rows), "rows": brier_rows}, f,
                  ensure_ascii=False, indent=2)
    print(f"Brier rows (ex-ante snapshot x resolved market): {len(brier_rows)} -> {BRIER_VIEW}")

    # --- Calibration table ------------------------------------------------------
    # One observation per resolved market (its latest pre-close snapshot), so
    # frequently snapshotted markets don't dominate their category's Brier.
    latest_per_market = {}
    for br in brier_rows:
        cur = latest_per_market.get(br["market_id"])
        if cur is None or br["observed_at"] > cur["observed_at"]:
            latest_per_market[br["market_id"]] = br
    by_cat = {}
    for br in latest_per_market.values():
        by_cat.setdefault(str(br["category"]), []).append(br["brier"])
    table = {cat: {"brier": sum(bs) / len(bs), "n": len(bs)} for cat, bs in sorted(by_cat.items())}
    with open(CALIBRATION_JSON, "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=2)
    print(f"Calibration table: {len(table)} categories -> {CALIBRATION_JSON}")
    for cat, entry in table.items():
        print(f"  {cat:<22} brier {entry['brier']:.4f}  n={entry['n']}")


if __name__ == "__main__":
    main()
