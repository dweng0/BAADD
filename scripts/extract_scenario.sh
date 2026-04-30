#!/bin/bash
# Extract a minimal spec for one scenario from BDD.md:
#   frontmatter + Feature header + Background (if any) + target scenario only.
#
# Usage:
#   bash scripts/extract_scenario.sh "Scenario Name" [bdd_file] [output_file]
#
# Output file defaults to BDD_SCENARIO.md in the current directory.
# Exits 0 on success, 1 on error.

SCENARIO_NAME="${1:?Usage: $0 <scenario_name> [bdd_file] [output_file]}"
BDD_FILE="${2:-BDD.md}"
OUTPUT_FILE="${3:-BDD_SCENARIO.md}"

if [ ! -f "$BDD_FILE" ]; then
    echo "ERROR: $BDD_FILE not found" >&2
    exit 1
fi

# Find the target scenario line (fixed-string match — handles special chars like () . [] $)
SCENARIO_LINE=$(grep -n "Scenario" "$BDD_FILE" | grep -F "$SCENARIO_NAME" | head -1 | cut -d: -f1)

if [ -z "$SCENARIO_LINE" ]; then
    echo "ERROR: Scenario not found in $BDD_FILE: $SCENARIO_NAME" >&2
    exit 1
fi

# Find the enclosing Feature: line (last Feature: at or before scenario line)
FEATURE_START=$(awk "NR<=$SCENARIO_LINE && /^[[:space:]]*Feature:/{start=NR} END{print start+0}" "$BDD_FILE")

if [ -z "$FEATURE_START" ] || [ "$FEATURE_START" -eq 0 ]; then
    echo "ERROR: No Feature block found containing: $SCENARIO_NAME" >&2
    exit 1
fi

# Find the end of this Feature block (start of next Feature, or EOF)
NEXT_FEATURE=$(awk "NR>$FEATURE_START && /^[[:space:]]*Feature:/{print NR; exit}" "$BDD_FILE")
FEATURE_END=$([ -n "$NEXT_FEATURE" ] && echo $((NEXT_FEATURE - 1)) || wc -l < "$BDD_FILE")

# Feature header = Feature: line through the line before the first Scenario/Background in this feature
FIRST_KEYWORD=$(awk "NR>$FEATURE_START && NR<=$FEATURE_END && /^[[:space:]]*(Scenario|Background):/{print NR; exit}" "$BDD_FILE")
FEATURE_HEADER_END=$([ -n "$FIRST_KEYWORD" ] && echo $((FIRST_KEYWORD - 1)) || echo "$FEATURE_END")

# Background block = from Background: line to the line before the first Scenario: in this feature
BACKGROUND_START=$(awk "NR>$FEATURE_START && NR<=$FEATURE_END && /^[[:space:]]*Background:/{print NR; exit}" "$BDD_FILE")
if [ -n "$BACKGROUND_START" ]; then
    FIRST_SCENARIO_IN_FEATURE=$(awk "NR>$BACKGROUND_START && NR<=$FEATURE_END && /^[[:space:]]*Scenario/{print NR; exit}" "$BDD_FILE")
    BACKGROUND_END=$([ -n "$FIRST_SCENARIO_IN_FEATURE" ] && echo $((FIRST_SCENARIO_IN_FEATURE - 1)) || echo "$FEATURE_END")
fi

# Target scenario end = line before the next Scenario: within this feature, or end of feature
NEXT_SCENARIO=$(awk "NR>$SCENARIO_LINE && NR<=$FEATURE_END && /^[[:space:]]*Scenario/{print NR; exit}" "$BDD_FILE")
SCENARIO_END=$([ -n "$NEXT_SCENARIO" ] && echo $((NEXT_SCENARIO - 1)) || echo "$FEATURE_END")

{
    # YAML frontmatter only (lines 1 to closing ---, not all content before this Feature)
    FRONTMATTER_END=$(awk 'NR>1 && /^---/{print NR; exit}' "$BDD_FILE")
    if [ -n "$FRONTMATTER_END" ]; then
        sed -n "1,${FRONTMATTER_END}p" "$BDD_FILE"
        echo ""
    fi

    # Feature header
    sed -n "${FEATURE_START},${FEATURE_HEADER_END}p" "$BDD_FILE"

    # Background (if present)
    if [ -n "$BACKGROUND_START" ]; then
        echo ""
        sed -n "${BACKGROUND_START},${BACKGROUND_END}p" "$BDD_FILE"
    fi

    # Target scenario
    echo ""
    sed -n "${SCENARIO_LINE},${SCENARIO_END}p" "$BDD_FILE"
} > "$OUTPUT_FILE"

LINES=$(wc -l < "$OUTPUT_FILE")
echo "Extracted scenario: $LINES lines → $OUTPUT_FILE"
echo "  Feature line: $FEATURE_START | Scenario line: $SCENARIO_LINE | Background: ${BACKGROUND_START:-none}"
