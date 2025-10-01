import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, cast
import typer

# Add the parent directory to Python path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from heysol import HeySolClient, HeySolConfig


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


def create_client(api_key: str, base_url: str = "https://core.heysol.ai/api/v1", source: Optional[str] = None, skip_mcp: bool = False) -> HeySolClient:
    """Create a HeySol client with the provided credentials."""
    if not api_key:
        raise ValueError("API key is required.")
    
    config = load_config(api_key=api_key, base_url=base_url, source=source)
    
    return HeySolClient(config=config, skip_mcp_init=skip_mcp)


# Removed deprecated get_auth_from_context() function
# Use get_auth_from_global() instead for authentication


def get_client_from_context(ctx: typer.Context) -> HeySolClient:
    """Get HeySolClient from context."""
    state = ctx.obj
    if not state or not state.api_key:
        typer.echo("API key is required. Use --api-key or --user option.", err=True)
        raise typer.Exit(1)

    return create_client(
        api_key=state.api_key,
        base_url=state.base_url,
        source=state.source,
        skip_mcp=state.skip_mcp,
    )


def get_auth_from_global() -> "tuple[str, str]":
    """
    Get resolved API key and base URL from global state.

    Raises:
        typer.Exit: If authentication is not provided.
    """
    import typer
    from . import state

    if not state.api_key:
        typer.echo("API key is required. Use --api-key or --user option.", err=True)
        raise typer.Exit(1)

    return state.api_key, cast(str, state.base_url)


def format_json_output(data: Any, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(data, indent=2, default=str)
    return json.dumps(data, default=str)
