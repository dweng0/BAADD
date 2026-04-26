from src.ports.config_reader import EnvironmentConfigReader
from typing import Protocol

# Note: Although the Plan defined this as a function, it's cleaner to define
# the signature using type hints against the Protocol.
def detect_provider(config_reader: EnvironmentConfigReader) -> str:
    """
    Checks environment keys in priority order and determines the active provider.
    Priority: Anthropic > OpenAI (based on test case requirement).
    """
    anthropic_key = config_reader.get_key("ANTHROPIC_API_KEY")
    if anthropic_key:
        return "anthropic"

    openai_key = config_reader.get_key("OPENAI_API_KEY")
    if openai_key:
        return "openai"

    # Fallback or error handling not specified, but assuming one must be found for the test to pass.
    raise ValueError("No active API provider key found.")