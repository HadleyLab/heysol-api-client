"""
HeySol API Client Library

This library provides both direct API access and MCP (Model Context Protocol) support
for interacting with HeySol services.
"""

from .client import HeySolClient
from .clients import HeySolAPIClient, HeySolMCPClient
from .config import HeySolConfig
from .exceptions import (
    AuthenticationError,
    ConnectionError,
    HeySolError,
    RateLimitError,
    ValidationError,
)

__version__ = "1.2.0"
__all__ = [
    "HeySolClient",  # Unified client with both API and MCP support
    "HeySolAPIClient",  # Direct API operations only
    "HeySolMCPClient",  # MCP protocol operations only
    "HeySolConfig",
    "HeySolError",
    "ValidationError",
    "AuthenticationError",
    "ConnectionError",
    "RateLimitError",
]
