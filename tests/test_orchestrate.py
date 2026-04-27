#!/usr/bin/env python3
"""Tests for orchestrate.py - orchestrator for parallel agent workers"""

import sys
import os
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from orchestrate import scenario_to_slug, get_uncovered_scenarios


# BDD: Slug truncates to 60 characters
def test_slug_truncates_to_60_characters():
    """Test that scenario_to_slug() truncates long names to max 60 characters."""
    # Create a scenario name that is very long (100+ chars)
    long_name = "This is a very long scenario name that exceeds sixty characters and should be truncated properly"
    
    slug = scenario_to_slug(long_name)
    
    # The slug should be at most 60 characters
    assert len(slug) <= 60, f"Slug length {len(slug)} exceeds 60 characters: {slug}"
    
    # The slug should still be a valid slug (lowercase, hyphens only for separators)
    assert slug == slug.lower(), "Slug should be lowercase"
    assert all(c.isalnum() or c == '-' for c in slug), "Slug should only contain alphanumeric and hyphens"


# BDD: Find uncovered scenarios for orchestration
def test_find_uncovered_scenarios_for_orchestration():
    """get_uncovered_scenarios returns all scenarios lacking test coverage."""
    bdd_content = """---
language: python
build_cmd: echo ok
test_cmd: echo ok
---

Feature: Test Feature
    Scenario: Alpha scenario one
        Given something
        Then something

    Scenario: Beta scenario two
        Given another thing
        Then another thing

    Scenario: Gamma scenario three
        Given third thing
        Then third thing

    Scenario: Delta scenario four
        Given fourth
        Then fourth

    Scenario: Epsilon scenario five
        Given fifth
        Then fifth

    Scenario: Zeta scenario six
        Given sixth
        Then sixth

    Scenario: Eta scenario seven
        Given seventh
        Then seventh

    Scenario: Theta scenario eight
        Given eighth
        Then eighth
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(bdd_content)
        bdd_path = f.name

    try:
        with patch("orchestrate.find_test_files", return_value=[]):
            result = get_uncovered_scenarios(bdd_path)
    finally:
        os.unlink(bdd_path)

    assert len(result) == 8, f"Expected 8 uncovered scenarios, got {len(result)}: {result}"
    scenario_names = [s for _, s in result]
    assert "Alpha scenario one" in scenario_names
    assert "Theta scenario eight" in scenario_names
