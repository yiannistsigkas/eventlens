"""
Check that EventLens raw data collection is still running.

This is intentionally independent of run_daily.py: it must still warn when the
daily pipeline or its scheduler stops running.
"""

import argparse
import glob
import json
import os
import subprocess
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RAW_DIR = os.path.join(ROOT, "data", "raw")
DEFAULT_MAX_AGE_HOURS = 36.0


def parse_ts(value):
    if not value:
        return None
    text = str(value).strip().replace(" ", "T", 1).replace("Z", "+00:00")
    if text.endswith("+00"):
        text += ":00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def latest_snapshot(raw_dir):
    paths = sorted(glob.glob(os.path.join(raw_dir, "raw_snapshot_*.json")), reverse=True)
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, ValueError):
            continue
        fetched_at = parse_ts(payload.get("fetched_at")) if isinstance(payload, dict) else None
        if fetched_at is not None:
            return path, fetched_at
    return None, None


def freshness_status(raw_dir=DEFAULT_RAW_DIR, max_age_hours=DEFAULT_MAX_AGE_HOURS, now=None):
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    path, fetched_at = latest_snapshot(raw_dir)
    if path is None:
        return {
            "ok": False,
            "reason": "no_valid_snapshot",
            "age_hours": None,
            "snapshot": None,
        }
    age_hours = (now - fetched_at).total_seconds() / 3600.0
    return {
        "ok": age_hours <= max_age_hours,
        "reason": "fresh" if age_hours <= max_age_hours else "snapshot_stale",
        "age_hours": age_hours,
        "snapshot": path,
        "fetched_at": fetched_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def notify(message):
    escaped = message.replace("\\", "\\\\").replace('"', '\\"')
    script = f'display notification "{escaped}" with title "EventLens data warning"'
    subprocess.run(["/usr/bin/osascript", "-e", script], check=False)


def main():
    parser = argparse.ArgumentParser(description="Warn if EventLens raw data is stale.")
    parser.add_argument("--raw-dir", default=DEFAULT_RAW_DIR)
    parser.add_argument("--max-age-hours", type=float, default=DEFAULT_MAX_AGE_HOURS)
    parser.add_argument("--notify", action="store_true", help="Send a macOS notification on failure.")
    args = parser.parse_args()

    status = freshness_status(args.raw_dir, args.max_age_hours)
    if status["ok"]:
        print(
            f"EventLens data fresh: {status['age_hours']:.1f}h old "
            f"({os.path.basename(status['snapshot'])})"
        )
        return 0

    if status["reason"] == "no_valid_snapshot":
        message = f"No valid raw snapshot found in {args.raw_dir}"
    else:
        message = (
            f"Newest raw snapshot is {status['age_hours']:.1f}h old "
            f"(limit {args.max_age_hours:.1f}h)"
        )
    print(f"WARNING: {message}")
    if args.notify:
        notify(message)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
