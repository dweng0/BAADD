#!/usr/bin/env python3
"""Tests for scripts/add_bdd_markers.py"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from add_bdd_markers import detect_comment_prefix, has_existing_marker, add_marker_to_file


# BDD: Detect comment prefix by file extension
def test_detect_comment_prefix_by_file_extension():
    """Detect comment prefix by file extension."""
    assert detect_comment_prefix("file.py") == "#"


# BDD: Detect JavaScript comment prefix
def test_detect_javascript_comment_prefix():
    assert detect_comment_prefix("file.test.js") == "//"


# BDD: Skip if marker already exists
def test_skip_if_marker_already_exists():
    """If a BDD marker already exists above the target line, add_marker_to_file returns None."""
    content = "# BDD: Login with valid credentials\ndef test_login_with_valid_credentials():\n    pass\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(content)
        f.flush()
        tmp_path = f.name

    try:
        # Line index 1 is the "def test_login..." line; line index 0 has the marker
        result = add_marker_to_file(tmp_path, line_index=1, scenario_name="Login with valid credentials", prefix="#")
        assert result is None, f"Expected None (marker already exists), got: {result!r}"

        # Verify file was not modified
        with open(tmp_path) as f:
            assert f.read() == content, "File content should be unchanged"
    finally:
        os.unlink(tmp_path)
