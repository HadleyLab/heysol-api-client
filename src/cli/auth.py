"""
Shared authentication utilities for CLI commands.
"""

import functools
from typing import Optional, Tuple

import typer

from ..heysol.registry_config import RegistryConfig


def resolve_credentials(
    user: Optional[str] = None, api_key: Optional[str] = None, base_url: Optional[str] = None
) -> Tuple[str, str]:
    """
    Resolve API credentials from user registry or direct API key.

    Args:
        user: User instance name from registry
        api_key: Direct API key
        base_url: Direct base URL

    Returns:
        Tuple of (resolved_api_key, resolved_base_url)

    Raises:
        typer.Exit: If credentials cannot be resolved
    """
    if user:
        registry = RegistryConfig()
        if user not in registry.get_instance_names():
            typer.echo(
                f"User '{user}' not found in registry. Use 'heysol registry list' to see available users.",
                err=True,
            )
            raise typer.Exit(1)
        instance = registry.get_instance(user)
        if not instance:
            typer.echo(f"Failed to get instance configuration for user '{user}'", err=True)
            raise typer.Exit(1)
        resolved_api_key = instance["api_key"]
        resolved_base_url = instance["base_url"]
    elif api_key:
        resolved_api_key = api_key
        resolved_base_url = base_url or "https://core.heysol.ai/api/v1"
    else:
        typer.echo(
            "Authentication required. Use --user to specify a registry user or --api-key to provide an API key directly.",
            err=True,
        )
        raise typer.Exit(1)

    if not resolved_api_key:
        typer.echo("API key is required for authentication.", err=True)
        raise typer.Exit(1)

    return resolved_api_key, resolved_base_url


def require_auth(f):
    """
    Decorator to ensure CLI commands require authentication.

    This decorator is now deprecated as authentication is handled globally.
    Commands should use get_auth_from_global() directly.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # For backward compatibility, just call the function
        return f(*args, **kwargs)

    return wrapper
