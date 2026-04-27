import os
import sys
import pytest

sys.path.insert(0, os.path.abspath("scripts"))
from agent import make_wrap_up_message, estimate_tokens, trim_context


# BDD: Wrap-up reminder content for evolve mode
def test_wrap_up_reminder_content_for_evolve_mode():
    msg = make_wrap_up_message(70, 75, "evolve")
    assert "BDD_STATUS.md" in msg
    assert "journal" in msg.lower() or "JOURNAL" in msg
    assert "commit" in msg.lower()


# BDD: Wrap-up reminder content for bootstrap mode
def test_wrap_up_reminder_content_for_bootstrap_mode():
    msg = make_wrap_up_message(70, 75, "bootstrap")
    assert ".baadd_initialized" in msg
    assert "Day 0" in msg or "journal" in msg.lower()


# BDD: Wrap-up reminder injected at threshold
def test_wrap_up_reminder_message_contains_iteration_info():
    msg = make_wrap_up_message(70, 75, "evolve")
    assert "70" in msg
    assert "75" in msg


# BDD: Estimate tokens from text
def test_estimate_tokens_from_text():
    text = "x" * 4000
    result = estimate_tokens(text)
    assert result == 1000


# BDD: Trim context when exceeding limit
def test_trim_context_when_exceeding_limit():
    messages = []
    # message 0 = initial prompt
    messages.append({"role": "user", "content": "initial prompt"})
    # add many old messages with large tool results
    for i in range(20):
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "content": "x" * 2000
            }]
        })
    limit = 100
    result = trim_context(messages, limit)
    # some tool results should be truncated
    truncated_found = False
    for msg in result[1:-12]:
        content = msg.get("content", "")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and "[... trimmed" in str(item.get("content", "")):
                    truncated_found = True
    assert truncated_found


# BDD: Preserve recent messages during trim
def test_preserve_recent_messages_during_trim():
    messages = []
    messages.append({"role": "user", "content": "initial"})
    for i in range(20):
        content = f"message_{i}_" + "x" * 2000
        messages.append({"role": "user", "content": [{"type": "tool_result", "content": content}]})

    original_last_12 = [str(m) for m in messages[-12:]]
    limit = 10
    result = trim_context(messages, limit)
    result_last_12 = [str(m) for m in result[-12:]]
    assert original_last_12 == result_last_12


# BDD: Trim only tool result content
def test_trim_only_tool_result_content():
    messages = [
        {"role": "user", "content": "initial prompt " + "x" * 2000},
    ]
    for i in range(5):
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "content": "tool output " + "x" * 2000}]
        })
    messages.append({"role": "assistant", "content": "assistant text " + "x" * 2000})
    # add protected tail messages
    for i in range(12):
        messages.append({"role": "user", "content": "recent " + str(i)})

    result = trim_context(messages, 10)
    # assistant message (not tool_result) should be untouched
    assistant_msgs = [m for m in result if m.get("role") == "assistant"]
    if assistant_msgs:
        assert "assistant text" in assistant_msgs[0]["content"]
