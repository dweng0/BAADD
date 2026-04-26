from typing import Optional, Protocol

class EnvironmentConfigReader(Protocol):
    """Abstracts the source of configuration secrets."""
    def get_key(self, key_name: str) -> Optional[str]:
        ...