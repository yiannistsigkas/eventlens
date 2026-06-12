"""
EventLens daily runner — fetch, score, track, report, then print an
operational summary of what changed this run.

    python scripts/run_daily.py
"""

import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
SNAPSHOT_LOG = os.path.join(ROOT, "data", "processed", "snapshots.jsonl")
RESOLUTIONS_LOG = os.path.join(ROOT, "data", "validation", "resolutions.jsonl")
BRIER_VIEW = os.path.join(ROOT, "data", "validation", "brier_rows.json")
REPORT_MD = os.path.join(ROOT, "data", "validation", "validation_report.md")

STEPS = [
    "fetch_polymarket_markets.py",
    "score_markets.py",
    "resolution_tracker.py",
    "validation_report.py",
]


def count_lines(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def brier_count():
    try:
        with open(BRIER_VIEW, encoding="utf-8") as f:
            return json.load(f).get("n_rows", 0)
    except (OSError, ValueError):
        return 0


def raw_snapshots():
    return set(glob.glob(os.path.join(ROOT, "data", "raw", "raw_snapshot_*.json")))


def main():
    before = {
        "raw": raw_snapshots(),
        "scored": count_lines(SNAPSHOT_LOG),
        "resolved": count_lines(RESOLUTIONS_LOG),
        "brier": brier_count(),
    }

    for step in STEPS:
        print(f"\n========== {step} ==========", flush=True)
        result = subprocess.run([sys.executable, os.path.join(SCRIPTS, step)], cwd=ROOT)
        if result.returncode != 0:
            raise SystemExit(f"{step} failed with exit code {result.returncode}; aborting daily run.")

    new_raw = sorted(raw_snapshots() - before["raw"])
    n_scored = count_lines(SNAPSHOT_LOG) - before["scored"]
    n_resolved_new = count_lines(RESOLUTIONS_LOG) - before["resolved"]
    n_brier = brier_count()

    print("\n========== Daily summary ==========")
    print(f"  New raw snapshot:         {os.path.basename(new_raw[0]) if new_raw else 'NONE'}")
    print(f"  New scored rows appended: {n_scored}")
    print(f"  New resolved markets:     {n_resolved_new} (total {count_lines(RESOLUTIONS_LOG)})")
    print(f"  Brier rows:               {n_brier} ({n_brier - before['brier']:+d} this run)")
    print(f"  Validation report:        {os.path.relpath(REPORT_MD, ROOT)}")


if __name__ == "__main__":
    main()
