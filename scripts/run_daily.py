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
from datetime import datetime, timezone

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


def git_backup(n_scored, n_resolved_new, n_brier):
    """Commit and push the day's data so the GitHub backup stays current.

    Scoped to data/ ONLY — never stages code or stray files, so it cannot
    sweep in anything unintended. Resilient by design: a backup failure
    (offline, locked keychain, auth) prints a warning but never fails the
    collection run. Data is append-only on disk regardless; an unpushed day
    simply ships on the next successful run.
    """
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def git(*args, check=True):
        return subprocess.run(["git", "-C", ROOT, *args],
                              check=check, capture_output=True, text=True)

    print("\n========== Backup (commit + push data) ==========", flush=True)
    try:
        git("add", "data")
        if subprocess.run(["git", "-C", ROOT, "diff", "--cached", "--quiet"]).returncode == 0:
            print("  No data changes to commit.")
            return
        msg = (f"Daily data {date}: +{n_scored} scored rows, "
               f"+{n_resolved_new} resolved, {n_brier} brier rows")
        git("commit", "-m", msg)
        push = git("push", check=False)
        if push.returncode == 0:
            print(f"  Committed + pushed: {msg}")
        else:
            print(f"  Committed locally; PUSH FAILED — {push.stderr.strip()[:200]}")
            print("  Data is safe locally and will push on the next successful run.")
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or str(exc)).strip()[:200]
        print(f"  WARNING: backup git step failed ({detail}). Collection data is intact.")


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

    git_backup(n_scored, n_resolved_new, n_brier)


if __name__ == "__main__":
    main()
