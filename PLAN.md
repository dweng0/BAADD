# PLAN.md

## 1. Units

### Unit: is_partial_word_match
*   **Signature:** `is_partial_word_match(test_name: str, scenario_description: str) -> bool`
*   **File:** `scripts/coverage_checker.py`
*   **Description:** Checks if the test name partially matches any word in the scenario description by performing tokenized substring comparisons.
*   **Dependency Injection Point:** None (inputs are direct parameters).

## 2. Test strategy

*   **Test file path:** `tests/test_coverage_detection.py`
*   **Exact test function name:** `test_partial_name_matching_success`
*   **BDD marker:** `# BDD: Detect coverage via partial name matching`
*   **What the test injects:** The required input strings (the specific test name and scenario description).
*   **What it asserts:** That `is_partial_word_match()` returns `True` given the specific inputs.

## 3. Acceptance criteria

*   [ ] BDD marker present on line immediately above test function, exact match
*   [ ] Test fails before implementation (red)
*   [ ] Test passes after implementation (green)
*   [ ] Full test suite still passes
*   [ ] `python3 scripts/check_bdd_coverage.py BDD.md` shows [x] for this scenario

## 4. Out of scope

*   The full integration with the coverage detection pipeline (i.e., how test names are gathered from the filesystem).
*   The implementation of `check_coverage()` wrapper function; only the core matching logic within it is required.