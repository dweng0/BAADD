# Failed Pipelines

Scenarios that exhausted all retries without being accepted.

## 2026-04-12 19:44 — Read file that does not exist

### Review Feedback for Read File that Does Not Exist (Test Failure)

The test `tests/test_skill_loader.py::test_load_skills_concatenates_multiple_files` failed due to an incorrect return value from the `load_skills` function.

**Issue:** The implementation returned an empty string (`''`) when it should have concatenated and returned the contents of the mocked files.

**Specific Change Required (in `scripts/skill_loader.py`):**
*   **Wrong String (Current Behavior):** `''`
*   **Correct String (Expected Output):** `'Content of A

---
Content of B
'`

Please ensure the logic correctly iterates over all SKILL.md files and uses the provided `file_reader` to fetch their content, joining them with the "---" separator.
