#!/bin/bash
# Atomically claim a scenario lock using a consistent slug algorithm.
#
# Usage:
#   bash scripts/claim_lock.sh "Scenario Name" "<uuid-token>"
#
# Exits 0 and prints "LOCK_CLAIMED: locks/<slug>.lock" on success.
# Exits 1 and prints "LOCK_BUSY: <reason>" if the scenario is already locked.

SCENARIO_NAME="${1:?Usage: $0 <scenario_name> <token>}"
TOKEN="${2:?Usage: $0 <scenario_name> <token>}"

mkdir -p locks

slug=$(echo "$SCENARIO_NAME" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/-\+/-/g' \
    | sed 's/^-//;s/-$//')
lockfile="locks/${slug}.lock"

# Check if a live lock already exists
if [ -f "$lockfile" ]; then
    is_live=$(python3 -c "
import os, time
f='$lockfile'
if not os.path.exists(f): print('stale'); exit()
age = time.time() - os.path.getmtime(f)
pid = next((l.split('=')[1].strip() for l in open(f) if l.startswith('PID=')), '0')
live_pid = pid != '0' and os.path.exists(f'/proc/{pid}')
print('live' if live_pid or age < 7200 else 'stale')
" 2>/dev/null || echo "stale")

    if [ "$is_live" = "live" ]; then
        echo "LOCK_BUSY: $lockfile is held by another agent"
        exit 1
    fi
    rm -f "$lockfile"
fi

DATE=$(date "+%Y-%m-%d %H:%M")
if (set -o noclobber
    cat > "$lockfile" <<EOF
PID=0
TOKEN=$TOKEN
SCENARIO=$SCENARIO_NAME
DATE=$DATE
EOF
) 2>/dev/null; then
    echo "LOCK_CLAIMED: $lockfile"
    exit 0
else
    echo "LOCK_BUSY: lost race to $lockfile"
    exit 1
fi
