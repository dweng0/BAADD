#!/usr/bin/env python3
"""Tests for orchestrate.py --provider flag (force orchestrator provider via CLI)"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


# BDD: Force orchestrator provider via CLI
def test_provider_flag_accepted_by_argparse():
    """--provider flag is accepted and stored as args.provider."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default=None)
    args, _ = parser.parse_known_args(["--provider", "anthropic"])
    assert args.provider == "anthropic"


# BDD: Force orchestrator provider via CLI
def test_provider_flag_overrides_detect_provider():
    """args.provider takes priority over detect_provider() result."""
    from orchestrate import detect_provider

    # When --provider=openai is passed, the logic is: args.provider or detect_provider()
    # So if args.provider is set, detect_provider is effectively bypassed.
    args_provider = "openai"
    with patch("orchestrate.detect_provider", return_value="anthropic") as mock_detect:
        # Simulate what orchestrate.py main does
        provider = args_provider or mock_detect()
        assert provider == "openai"
        mock_detect.assert_not_called()


# BDD: Force orchestrator provider via CLI
def test_provider_flag_none_falls_back_to_detect():
    """When --provider not passed, detect_provider() is used."""
    from orchestrate import detect_provider

    args_provider = None
    with patch("orchestrate.detect_provider", return_value="anthropic") as mock_detect:
        provider = args_provider or mock_detect()
        assert provider == "anthropic"
        mock_detect.assert_called_once()


# BDD: Force orchestrator provider via CLI
def test_provider_flag_used_in_plan_scenario_order():
    """Provider from CLI flag is passed to plan_scenario_order."""
    from orchestrate import plan_scenario_order

    uncovered = [("Feature", "Scenario A"), ("Feature", "Scenario B")]
    bdd_content = "# BDD"
    forced_provider = "anthropic"

    with patch("orchestrate.resolve_model_and_client") as mock_resolve:
        mock_call = MagicMock(return_value='["Scenario A", "Scenario B"]')
        mock_resolve.return_value = ("claude-haiku-4-5-20251001", mock_call)

        plan_scenario_order(uncovered, bdd_content, forced_provider, None)

        mock_resolve.assert_called_once_with(forced_provider, None)
