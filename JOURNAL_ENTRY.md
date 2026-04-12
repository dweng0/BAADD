## 2026-04-12 09:32 — Load BDD config before session

Implemented the "Load BDD config before session" scenario for the Evolution Script feature. The scenario verifies that evolve.sh properly loads BDD configuration from BDD.md before starting a session, setting LANGUAGE, BUILD_CMD, and TEST_CMD as environment variables.

The implementation already existed in parse_bdd_config.py and evolve.sh (which calls `eval "$(python3 scripts/parse_bdd_config.py BDD.md)"`). I added a test in tests/test_evolve.py that verifies the parse_bdd_config.py script outputs correct shell variable assignments and that sourcing these in bash properly sets the environment variables. The test includes the required BDD marker comment for coverage detection.
