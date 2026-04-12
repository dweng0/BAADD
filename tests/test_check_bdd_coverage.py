#!/usr/bin/env python3
"""Tests for check_bdd_coverage.py"""

import os
import sys
import tempfile

sys.path.insert(0, "scripts")
from check_bdd_coverage import parse_scenarios


# BDD: Extract all scenarios from BDD.md
def test_extract_all_scenarios_from_bdd_md():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("---\n")
        f.write("language: python\n")
        f.write("---\n")
        f.write("\n")
        f.write("Feature: Login System\n")
        f.write("    Scenario: User logs in successfully\n")
        f.write("    Scenario: User fails with wrong password\n")
        f.write("\n")
        f.write("Feature: Registration\n")
        f.write("    Scenario: New user registers\n")
        f.write("    Scenario: Duplicate email rejected\n")
        f.write("\n")
        f.write("Feature: Session Management\n")
        f.write("    Scenario Outline: Logout from <device>\n")
        f.flush()

        scenarios = parse_scenarios(f.name)

        assert len(scenarios) == 5
        assert scenarios[0] == ("Login System", "User logs in successfully")
        assert scenarios[1] == ("Login System", "User fails with wrong password")
        assert scenarios[2] == ("Registration", "New user registers")
        assert scenarios[3] == ("Registration", "Duplicate email rejected")
        assert scenarios[4] == ("Session Management", "Logout from <device>")

        os.unlink(f.name)
