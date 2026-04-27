#!/usr/bin/env python3
"""Tests for scripts/add_bdd_markers.py"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from add_bdd_markers import detect_comment_prefix

# BDD: Detect JavaScript comment prefix
def test_detect_javascript_comment_prefix():
    assert detect_comment_prefix("file.test.js") == "//"
