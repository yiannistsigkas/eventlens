#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/launchd/com.eventlens.freshness.plist"
TARGET="$HOME/Library/LaunchAgents/com.eventlens.freshness.plist"
DOMAIN="gui/$(id -u)"

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
launchctl bootout "$DOMAIN/com.eventlens.freshness" 2>/dev/null || true
install -m 0644 "$SOURCE" "$TARGET"
launchctl bootstrap "$DOMAIN" "$TARGET"
launchctl kickstart -k "$DOMAIN/com.eventlens.freshness"

echo "Installed com.eventlens.freshness (daily at 21:05, stale after 36h)."
launchctl print "$DOMAIN/com.eventlens.freshness" |
    grep -E "state =|program =|runs =|last exit code" || true
