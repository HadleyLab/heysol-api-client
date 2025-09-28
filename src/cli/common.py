import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from ..heysol import HeySolClient, HeySolConfig


def load_config(
    api_key: Optional[str] = None, base_url: Optional[str] = None, source: Optional[str] = None
) -> HeySolConfig:
    config = HeySolConfig.from_env()
    if api_key:
        config.api_key = api_key
    if base_url:
        config.base_url = base_url
    if source:
        config.source = source
    if not config.api_key:
        config.api_key = os.getenv("HEYSOL_API_KEY")
    return config


def create_client(api_key: str, base_url: str = "https://core.heysol.ai/api/v1") -> HeySolClient:
    """Create a HeySol client with the provided credentials."""
    if not api_key:
        raise ValueError("API key is required.")
    return HeySolClient(api_key=api_key, base_url=base_url)


def get_auth_from_context(ctx) -> "tuple[str, str]":
    """Get resolved API key and base URL from Typer context.

    Raises:
        ValueError: If authentication is not provided.
    """
    # This function is deprecated, use get_auth_from_global() instead
    api_key = ctx.obj.get("api_key")
    base_url = ctx.obj.get("base_url")

    if not api_key:
        raise ValueError("API key is required. Use --api-key or --user option.")

    return api_key, base_url


def get_auth_from_global() -> "tuple[str, str]":
    """Get resolved API key and base URL from global state.

    Raises:
        typer.Exit: If authentication is not provided.
    """
    import typer

    # Import the global variables from the main CLI
    from . import _global_api_key, _global_base_url

    if not _global_api_key:
        typer.echo("API key is required. Use --api-key or --user option.", err=True)
        raise typer.Exit(1)

    return _global_api_key, _global_base_url or "https://core.heysol.ai/api/v1"


def format_json_output(data: Any, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(data, indent=2, default=str)
    return json.dumps(data, default=str)
