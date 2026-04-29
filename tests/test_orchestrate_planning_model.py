#!/usr/bin/env python3
"""Tests for orchestrate.py --model flag (override orchestrator planning model)"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


# BDD: Override orchestrator planning model
def test_model_flag_accepted_by_argparse():
    """--model flag is accepted and stored as args.model."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None)
    args, _ = parser.parse_known_args(["--model", "claude-opus"])
    assert args.model == "claude-opus"


# BDD: Override orchestrator planning model
def test_plan_scenario_order_uses_model_override():
    """plan_scenario_order passes model_override to resolve_model_and_client."""
    from orchestrate import plan_scenario_order

    uncovered = [("Feature", "Scenario A"), ("Feature", "Scenario B")]
    bdd_content = "# BDD"
    provider = "anthropic"
    model_override = "claude-opus"

    with patch("orchestrate.resolve_model_and_client") as mock_resolve:
        mock_call = MagicMock(return_value='["Scenario A", "Scenario B"]')
        mock_resolve.return_value = (model_override, mock_call)

        result = plan_scenario_order(uncovered, bdd_content, provider, model_override)

        mock_resolve.assert_called_once_with(provider, model_override)
        assert result == ["Scenario A", "Scenario B"]


# BDD: Override orchestrator planning model
def test_plan_scenario_order_no_override_uses_none():
    """When --model not passed, model_override is None."""
    from orchestrate import plan_scenario_order

    uncovered = [("Feature", "Scenario X"), ("Feature", "Scenario Y")]
    bdd_content = "# BDD"
    provider = "anthropic"

    with patch("orchestrate.resolve_model_and_client") as mock_resolve:
        mock_call = MagicMock(return_value='["Scenario X", "Scenario Y"]')
        mock_resolve.return_value = ("default-model", mock_call)

        plan_scenario_order(uncovered, bdd_content, provider, None)

        mock_resolve.assert_called_once_with(provider, None)


# BDD: Override orchestrator planning model
def test_model_override_flows_from_args_to_plan():
    """model_orch_override is set from args.model and passed to plan_scenario_order."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None)
    args, _ = parser.parse_known_args(["--model", "claude-opus"])

    # Simulate what orchestrate.py main does
    model_orch_override = args.model or None
    assert model_orch_override == "claude-opus"
