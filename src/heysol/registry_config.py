"""
HeySol Registry Configuration.

Configuration system that reads API keys from environment variables
specified in config.json for cross-instance operations.
"""

import os
from typing import Dict, List, Optional

# Load environment variables from .env file
try:
    # Find .env file in current directory or parent directories
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    current_dir = Path.cwd()
    env_file = None

    # Look for .env file starting from current directory and walking up
    check_dir = current_dir
    while check_dir != check_dir.parent:
        potential_env = check_dir / ".env"
        if potential_env.exists():
            env_file = potential_env
            break
        check_dir = check_dir.parent

    if env_file:
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv not available, continue without it

from .config import HeySolConfig
from .exceptions import HeySolError


class RegistryConfig:
    """Configuration for HeySol instance registry."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize registry configuration from config.json."""
        self.env_file = env_file
        self.instances = self._load_instances_from_config()

    def _load_instances_from_config(self) -> Dict[str, Dict[str, str]]:
        """Load instances from config.json using environment variables."""
        config_file = os.path.join(os.path.dirname(__file__), "config.json")

        if not os.path.exists(config_file):
            raise HeySolError(f"Configuration file not found: {config_file}")

        # Load environment variables from specified .env file or find automatically
        if self.env_file:
            if os.path.exists(self.env_file):
                load_dotenv(self.env_file)
            else:
                raise HeySolError(f"Specified .env file not found: {self.env_file}")
        else:
            # Find .env file automatically (existing logic)
            current_dir = Path.cwd()
            env_file = None

            # Look for .env file starting from current directory and walking up
            check_dir = current_dir
            while check_dir != check_dir.parent:
                potential_env = check_dir / ".env"
                if potential_env.exists():
                    env_file = potential_env
                    break
                check_dir = check_dir.parent

            if env_file:
                load_dotenv(env_file)
                self.env_file = str(env_file)

        instances = {}

        try:
            import json

            with open(config_file, "r") as f:
                config_data = json.load(f)

            for instance_name, instance_config in config_data.get("instances", {}).items():
                api_key_env_var = instance_config.get("api_key_env_var")
                if not api_key_env_var:
                    raise HeySolError(f"Missing api_key_env_var for instance: {instance_name}")

                api_key = os.getenv(api_key_env_var)

                # Special handling for default HEYSOL_API_KEY
                if api_key_env_var == "HEYSOL_API_KEY" and not api_key:
                    # Try to get from HeySolConfig which loads .env
                    try:
                        config = HeySolConfig.from_env()
                        api_key = config.api_key
                    except Exception:
                        pass

                if not api_key:
                    # Skip instances that don't have their environment variables set
                    continue

                instances[instance_name] = {
                    "api_key": api_key,
                    "base_url": instance_config.get("base_url", "https://core.heysol.ai/api/v1"),
                    "description": instance_config.get("description", instance_name),
                }

        except Exception as e:
            raise HeySolError(f"Failed to load instances from {config_file}: {e}")

        return instances

    def get_registered_instances(self) -> Dict[str, Dict[str, str]]:
        """Get all registered instances."""
        return self.instances.copy()

    def get_instance_names(self) -> List[str]:
        """Get list of registered instance names."""
        return list(self.instances.keys())

    def get_instance(self, name: str) -> Optional[Dict[str, str]]:
        """Get instance configuration by name."""
        return self.instances.get(name)
