## 2026-04-12 08:51 — Parse scenario outline syntax

Implemented the "Parse scenario outline syntax" scenario by adding a test to `tests/test_check_bdd_coverage.py` with the BDD marker comment. The test verifies that `parse_scenarios()` correctly extracts "Scenario Outline:" entries the same way it handles regular "Scenario:" entries. The implementation already existed in the regex pattern `r"Scenario(?:\s+Outline)?:\s*(.+)"` which optionally matches " Outline" after "Scenario", so the test passed immediately without requiring code changes.
