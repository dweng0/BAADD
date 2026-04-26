import os
from src.ports.config_reader import EnvironmentConfigReader

class OSEnvironmentConfigReader:
    """Implements EnvironmentConfigReader by querying OS environment variables."""
    def get_key(self, key_name: str) -> Optional[str]:
        return os.environ.get(key_name)