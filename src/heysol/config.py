"""
Configuration module for HeySol API client.

This module provides configuration management using Pydantic models
for automatic validation and type safety.
"""

# Re-export the Pydantic config model for backward compatibility
from .models import HeySolConfig

# Keep constants for backward compatibility
DEFAULT_BASE_URL = "https://core.heysol.ai/api/v1"
DEFAULT_SOURCE = "heysol-api-client"
DEFAULT_MCP_URL = f"https://core.heysol.ai/api/v1/mcp?source={DEFAULT_SOURCE}"
DEFAULT_PROFILE_URL = "https://core.heysol.ai/api/profile"

__all__ = [
    "HeySolConfig",
    "DEFAULT_BASE_URL",
    "DEFAULT_SOURCE",
    "DEFAULT_MCP_URL",
    "DEFAULT_PROFILE_URL",
]
