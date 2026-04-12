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


# BDD: Parse scenario outline syntax
def test_parse_scenario_outline_syntax():
    """Test that Scenario Outline is treated the same as Scenario."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("---\n")
        f.write("language: python\n")
        f.write("---\n")
        f.write("\n")
        f.write("Feature: Authentication\n")
        f.write("    Scenario: Login with valid credentials\n")
        f.write("    Scenario Outline: Login with <role>\n")
        f.write("        Given a user with role <role>\n")
        f.write("        When they attempt to login\n")
        f.write("        Then access is granted\n")
        f.write("\n")
        f.write("    Examples:\n")
        f.write("        | role  |\n")
        f.write("        | admin |\n")
        f.write("        | user  |\n")
        f.flush()

        scenarios = parse_scenarios(f.name)

        # Should find both regular Scenario and Scenario Outline
        assert len(scenarios) == 2
        assert scenarios[0] == ("Authentication", "Login with valid credentials")
        assert scenarios[1] == ("Authentication", "Login with <role>")

        os.unlink(f.name)
