#!/bin/bash
# Release a scenario lock by scenario name (uses same slug algorithm as claim_lock.sh).
#
# Usage:
#   bash scripts/release_lock.sh "Scenario Name"

SCENARIO_NAME="${1:?Usage: $0 <scenario_name>}"

slug=$(echo "$SCENARIO_NAME" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/-\+/-/g' \
    | sed 's/^-//;s/-$//')
lockfile="locks/${slug}.lock"

if [ -f "$lockfile" ]; then
    rm -f "$lockfile"
    echo "LOCK_RELEASED: $lockfile"
else
    echo "LOCK_NOT_FOUND: $lockfile"
fi
