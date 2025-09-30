"""
Pydantic models for HeySol API client configuration.
"""

from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Default constants
DEFAULT_BASE_URL = "https://core.heysol.ai/api/v1"
DEFAULT_SOURCE = "heysol-api-client"
DEFAULT_MCP_URL = f"https://core.heysol.ai/api/v1/mcp?source={DEFAULT_SOURCE}"
DEFAULT_PROFILE_URL = "https://core.heysol.ai/api/profile"


class HeySolConfig(BaseModel):
    """Configuration model for HeySol client initialization."""

    model_config = ConfigDict(validate_assignment=True)

    api_key: Optional[str] = Field(default=None, description="HeySol API key for authentication")
    base_url: str = Field(default=DEFAULT_BASE_URL, description="Base URL for API endpoints")
    mcp_url: str = Field(default=DEFAULT_MCP_URL, description="MCP endpoint URL")
    profile_url: str = Field(default=DEFAULT_PROFILE_URL, description="Profile endpoint URL")
    source: str = Field(default=DEFAULT_SOURCE, description="Default source identifier")
    timeout: int = Field(default=60, ge=1, le=300, description="Request timeout in seconds")

    @field_validator("api_key")
    @classmethod
    def validate_api_key_format(cls, v: str | None) -> str | None:
        """Validate API key format if provided."""
        if v is not None and not v.startswith("rc_pat_"):
            raise ValueError("API key must start with 'rc_pat_'")
        return v

    @classmethod
    def from_env(cls) -> HeySolConfig:
        """Create configuration from environment variables."""
        timeout_str = os.getenv("HEYSOL_TIMEOUT")
        timeout = int(timeout_str) if timeout_str and timeout_str.isdigit() else 60

        return cls(
            api_key=os.getenv("HEYSOL_API_KEY"),
            base_url=os.getenv("HEYSOL_BASE_URL") or DEFAULT_BASE_URL,
            mcp_url=os.getenv("HEYSOL_MCP_URL") or DEFAULT_MCP_URL,
            profile_url=os.getenv("HEYSOL_PROFILE_URL") or DEFAULT_PROFILE_URL,
            source=os.getenv("HEYSOL_SOURCE") or DEFAULT_SOURCE,
            timeout=timeout,
        )
