#!/usr/bin/env python3
<<<<<<< HEAD
"""Tests for agent.py provider detection"""

import os
import sys

sys.path.insert(0, "scripts")
from agent import detect_provider


# BDD: Detect Anthropic provider from API key
def test_detect_anthropic_provider_from_api_key():
    """Test that detect_provider() returns 'anthropic' when ANTHROPIC_API_KEY is set."""
    # Save original environment
    original_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    original_poppins_cfg_provider = None
    
    try:
        # Remove any existing ANTHROPIC_API_KEY
        os.environ.pop("ANTHROPIC_API_KEY", None)
        
        # Set ANTHROPIC_API_KEY
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-key"
        
        # Need to reimport to pick up the new environment variable
        # Since detect_provider uses module-level _POPPINS_CFG, we need to test differently
        # The function checks PROVIDER_PRIORITY which includes ANTHROPIC_API_KEY
        result = detect_provider()
        
        # Verify it returns 'anthropic'
        assert result == "anthropic", f"Expected 'anthropic', got '{result}'"
        
    finally:
        # Restore original environment
        if original_anthropic_key is not None:
            os.environ["ANTHROPIC_API_KEY"] = original_anthropic_key
        else:
            os.environ.pop("ANTHROPIC_API_KEY", None)
=======
"""Tests for agent.py - multi-provider AI agent"""

import os
import subprocess
import sys
import tempfile


# BDD: Detect Groq provider from API key
def test_detect_groq_provider_from_api_key():
    """Test that detect_provider() returns 'groq' when GROQ_API_KEY is set and no higher-priority keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a poppins.yml without provider setting (to test env var detection)
        poppins_path = os.path.join(tmpdir, "poppins.yml")
        with open(poppins_path, "w") as f:
            f.write("# No provider set - should fall back to env var detection\n")
            f.write("agent:\n")
            f.write("  max_iterations: 10\n")
        
        # Create scripts directory in tmpdir
        scripts_dir = os.path.join(tmpdir, "scripts")
        os.makedirs(scripts_dir)
        
        # Copy agent.py to tmpdir/scripts
        with open("scripts/agent.py", "r") as src:
            with open(os.path.join(scripts_dir, "agent.py"), "w") as dst:
                dst.write(src.read())
        
        # Copy parse_poppins_config.py to tmpdir/scripts  
        with open("scripts/parse_poppins_config.py", "r") as src:
            with open(os.path.join(scripts_dir, "parse_poppins_config.py"), "w") as dst:
                dst.write(src.read())
        
        # Create a test script that imports agent and calls detect_provider
        test_script = os.path.join(tmpdir, "test_detect.py")
        with open(test_script, "w") as f:
            f.write(f'''
import os
import sys

# Clear any existing provider-related env vars
for key in ["ANTHROPIC_API_KEY", "MOONSHOT_API_KEY", "DASHSCOPE_API_KEY", 
            "OPENAI_API_KEY", "GROQ_API_KEY", "CUSTOM_API_KEY", "CUSTOM_BASE_URL",
            "OLLAMA_HOST"]:
    os.environ.pop(key, None)

# Set only GROQ_API_KEY
os.environ["GROQ_API_KEY"] = "gsk_test_key_123"

# Add scripts to path
sys.path.insert(0, "{scripts_dir}")

# Import and call detect_provider
from agent import detect_provider
result = detect_provider()
print(result)
''')
        
        # Run the test script
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert result.stdout.strip() == "groq", f"Expected 'groq', got '{result.stdout.strip()}'"
>>>>>>> agent/detect-groq-provider-from-api-key-20260412-100308
