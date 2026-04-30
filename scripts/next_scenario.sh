#!/bin/bash
# Output the name of the next uncovered scenario, skipping any that are locked.
#
# Usage:
#   bash scripts/next_scenario.sh [bdd_file]
#
# Prints one line: the scenario name.
# Exits 0 if a scenario is found, 1 if all scenarios are covered or locked.

BDD_FILE="${1:-BDD.md}"

if [ ! -f "$BDD_FILE" ]; then
    echo "ERROR: $BDD_FILE not found" >&2
    exit 1
fi

mkdir -p locks

# Capture uncovered list into a temp file to avoid pipe-subshell exit issues
UNCOVERED=$(python3 scripts/check_bdd_coverage.py "$BDD_FILE" 2>/dev/null \
    | grep "UNCOVERED:" \
    | sed 's/.*UNCOVERED: //')

if [ -z "$UNCOVERED" ]; then
    echo "STATUS: all_covered"
    exit 1
fi

while IFS= read -r scenario; do
    [ -z "$scenario" ] && continue

    slug=$(echo "$scenario" \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[^a-z0-9]/-/g' \
        | sed 's/-\+/-/g' \
        | sed 's/^-//;s/-$//')
    lockfile="locks/${slug}.lock"

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
        [ "$is_live" = "live" ] && continue
    fi

    echo "NEXT_SCENARIO: $scenario"
    exit 0
done <<< "$UNCOVERED"

echo "STATUS: all_locked"
exit 1
