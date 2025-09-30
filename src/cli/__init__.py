#!/usr/bin/env python3
"""
Command-line interface for the HeySol API client.

This CLI provides access to HeySol API functionality including memory management,
space operations, user profile, and search capabilities.
"""

import sys
from pathlib import Path
from typing import Optional

import typer

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Subcommand imports - import after path setup
from .logs import app as logs_app
from .memory import app as memory_app
from .profile import app as profile_app
from .registry import app as registry_app
from .spaces import app as spaces_app
from .tools import app as tools_app
from .webhooks import app as webhooks_app

app = typer.Typer()

# Global state for subcommands
_global_api_key = None
_global_base_url = None
_global_source = None
_global_skip_mcp = False


@app.callback()
def cli_callback(
    api_key: Optional[str] = typer.Option(
        None, help="HeySol API key (overrides environment variable)"
    ),
    base_url: Optional[str] = typer.Option(None, help="Base URL for API (overrides default)"),
    user: Optional[str] = typer.Option(
        None, help="User instance name from registry (alternative to --api-key)"
    ),
    source: Optional[str] = typer.Option(None, help="Source identifier (overrides default)"),
    skip_mcp: bool = typer.Option(False, help="Skip MCP initialization"),
) -> None:
    """HeySol API Client CLI

    Authentication: Use --api-key, --user (registry), or HEYSOL_API_KEY env var.
    Get API key from: https://core.heysol.ai/settings/api
    """
    # Resolve credentials
    resolved_api_key = api_key
    resolved_base_url = base_url

    # Case 1: Both user and API key provided - validate they match
    if user and api_key:
        try:
            from heysol.registry_config import RegistryConfig

            registry = RegistryConfig()
            instance = registry.get_instance(user)
            if not instance:
                typer.echo(
                    f"Error resolving user '{user}': User '{user}' not found in registry. Use 'heysol registry list' to see available users.",
                    err=True,
                )
                raise typer.Exit(1)

            registry_api_key = instance["api_key"]
            if registry_api_key != api_key:
                typer.echo(
                    f"API key mismatch: Provided API key does not match the one registered for user '{user}'. Either use --user '{user}' alone or --api-key with the correct key.",
                    err=True,
                )
                raise typer.Exit(1)

            resolved_api_key = api_key
            resolved_base_url = instance["base_url"]
        except Exception as e:
            typer.echo(f"Error validating user and API key: {e}", err=True)
            raise typer.Exit(1)

    # Case 2: User provided, no API key - resolve from registry
    elif user and not api_key:
        try:
            from heysol.registry_config import RegistryConfig

            registry = RegistryConfig()
            instance = registry.get_instance(user)
            if not instance:
                typer.echo(
                    f"Error resolving user '{user}': User '{user}' not found in registry. Use 'heysol registry list' to see available users.",
                    err=True,
                )
                raise typer.Exit(1)
            resolved_api_key = instance["api_key"]
            resolved_base_url = instance["base_url"]
        except Exception as e:
            typer.echo(f"Error resolving user '{user}': {e}", err=True)
            raise typer.Exit(1)

    # Case 3: API key provided - use it directly
    elif api_key:
        resolved_api_key = api_key
        resolved_base_url = base_url

    # Case 4: Neither provided - try to get default from environment or registry
    else:
        # For help commands, don't require credentials
        if "--help" in sys.argv or "help" in sys.argv:
            resolved_api_key = "dummy-key-for-help"
            resolved_base_url = base_url or "https://core.heysol.ai/api/v1"
        else:
            try:
                from heysol.registry_config import RegistryConfig
    
                registry = RegistryConfig()
                instances = registry.get_instance_names()

                if instances:
                    # Use the first available instance as default
                    default_user = instances[0]
                    instance = registry.get_instance(default_user)
                    if instance:
                        resolved_api_key = instance["api_key"]
                        resolved_base_url = instance["base_url"]
                    else:
                        typer.echo("No valid instances found in registry.", err=True)
                        raise typer.Exit(1)
                else:
                    typer.echo(
                        "No instances registered and no API key provided. Use --user to specify a registry user or --api-key to provide an API key directly.",
                        err=True,
                    )
                    raise typer.Exit(1)

            except Exception as e:
                typer.echo(f"Error resolving default credentials: {e}", err=True)
                raise typer.Exit(1)

    # Store in global state for subcommands
    global _global_api_key, _global_base_url, _global_source, _global_skip_mcp
    _global_api_key = resolved_api_key
    _global_base_url = resolved_base_url
    _global_source = source
    _global_skip_mcp = skip_mcp


# Add command groups with detailed descriptions
app.add_typer(
    logs_app,
    name="logs",
    help="Manage ingestion logs, status, and log operations"
)
app.add_typer(
    memory_app,
    name="memory",
    help="Memory operations: ingest, search, queue, and episode management"
)
app.add_typer(
    profile_app,
    name="profile",
    help="User profile and API health check operations"
)
app.add_typer(
    registry_app,
    name="registry",
    help="Manage registered HeySol instances and authentication"
)
app.add_typer(
    spaces_app,
    name="spaces",
    help="Space management: create, list, update, delete, and bulk operations"
)
app.add_typer(
    tools_app,
    name="tools",
    help="List MCP tools and integrations"
)
app.add_typer(
    webhooks_app,
    name="webhooks",
    help="Webhook management: create, list, update, delete webhooks"
)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
