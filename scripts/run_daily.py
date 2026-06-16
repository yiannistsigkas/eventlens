"""
EventLens daily runner — fetch, score, track, report, then print an
operational summary of what changed this run.

    python scripts/run_daily.py
"""

import glob
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone

GAMMA_HOST = "gamma-api.polymarket.com"
NETWORK_WAIT_TOTAL_S = 300   # launchd may fire this on wake before the network is up
NETWORK_WAIT_INTERVAL_S = 10

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


def wait_for_network():
    """Block until the API host resolves, or give up after a cap.

    launchd fires a missed 09:00 job the instant the Mac wakes — often before
    DNS/Wi-Fi is ready, which is what made the scheduled runs abort. We poll DNS
    resolution (cheap, no HTTP) and only start once it succeeds. The scripts
    also retry at the HTTP layer, so this is the first line of defence."""
    deadline = time.monotonic() + NETWORK_WAIT_TOTAL_S
    attempt = 0
    while True:
        try:
            socket.getaddrinfo(GAMMA_HOST, 443)
            if attempt:
                print(f"  Network ready after {attempt} wait(s).")
            return True
        except socket.gaierror:
            attempt += 1
            if time.monotonic() >= deadline:
                print(f"  Network still unavailable after {NETWORK_WAIT_TOTAL_S}s — "
                      "the scripts will still retry; proceeding.")
                return False
            print(f"  Waiting for network (DNS for {GAMMA_HOST} not ready)…", flush=True)
            time.sleep(NETWORK_WAIT_INTERVAL_S)


def main():
    print("========== Network pre-flight ==========", flush=True)
    wait_for_network()

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
