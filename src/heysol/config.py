import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_BASE_URL = "https://core.heysol.ai/api/v1"
DEFAULT_SOURCE = "heysol-api-client"
DEFAULT_MCP_URL = f"https://core.heysol.ai/api/v1/mcp?source={DEFAULT_SOURCE}"
DEFAULT_PROFILE_URL = "https://core.heysol.ai/api/profile"


@dataclass
class HeySolConfig:
    api_key: Optional[str] = None
    base_url: str = DEFAULT_BASE_URL
    mcp_url: str = DEFAULT_MCP_URL
    profile_url: str = DEFAULT_PROFILE_URL
    source: str = DEFAULT_SOURCE
    timeout: int = 60

    @classmethod
    def from_env(cls) -> "HeySolConfig":
        timeout_str = os.getenv("HEYSOL_TIMEOUT")
        timeout = int(timeout_str) if timeout_str else 60
        return cls(
            api_key=os.getenv("HEYSOL_API_KEY"),
            base_url=os.getenv("HEYSOL_BASE_URL") or DEFAULT_BASE_URL,
            mcp_url=os.getenv("HEYSOL_MCP_URL") or DEFAULT_MCP_URL,
            profile_url=os.getenv("HEYSOL_PROFILE_URL") or DEFAULT_PROFILE_URL,
            source=os.getenv("HEYSOL_SOURCE") or DEFAULT_SOURCE,
            timeout=timeout,
        )
