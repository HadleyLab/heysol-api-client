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

# Subcommand imports
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
):
    """HeySol API Client CLI

    Setup:
      1. Get your API key from: https://core.heysol.ai/settings/api
      2. Set environment variable: export HEYSOL_API_KEY="your-key-here"
      3. Or use --api-key option with each command
      4. Or use --user option with registered instance names (see 'registry' commands)

    Examples:
      # Get user profile
      heysol-client profile get

         # List spaces
      heysol-client spaces list

      # Create a space
      heysol-client spaces create "My Space" --description "Description"

      # Get space details
      heysol-client spaces get <space-id>

      # Ingest data
      heysol-client memory ingest "Hello world" --space-id abc123

      # Search memory
      heysol-client memory search "query" --space-id abc123 --limit 10

      # List logs with status filtering
      heysol-client logs list --space-id abc123 --status success --limit 50

      # Check ingestion processing status
      heysol-client logs status --space-id abc123

      # Delete logs by source
      heysol-client logs delete-by-source "source-name" --confirm

      # Delete specific log entry
      heysol-client logs delete-entry "log-id" --confirm

      # Get specific log
      heysol-client logs get "log-id"

      # Get logs by source with status filter
      heysol-client logs get-by-source "kilo-code" --status success --limit 10

      # List unique sources with status filter
      heysol-client logs sources --status success

      # Update space properties
      heysol-client spaces update "space-id" --name "New Name"

      # Bulk space operations
      heysol-client spaces bulk-ops "intent" --space-id "space-id"

      # Delete space
      heysol-client spaces delete "space-id" --confirm

      # Create webhook
      heysol-client webhooks create "https://example.com/webhook" --secret "secret"

      # List webhooks
      heysol-client webhooks list

      # Update webhook
      heysol-client webhooks update "webhook-id" "https://new-url.com" --events "event1" --secret "new-secret"

      # List MCP tools
      heysol-client tools list

      # Register instances from .env file
      heysol-client registry register

      # List registered instances
      heysol-client registry list

      # Show instance details
      heysol-client registry show <instance-name>

      # Set active instance
      heysol-client registry use <instance-name>
    """
    # Resolve credentials
    resolved_api_key = api_key
    resolved_base_url = base_url

    # Case 1: Both user and API key provided - validate they match
    if user and api_key:
        try:
            from ..heysol.registry_config import RegistryConfig

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
            from ..heysol.registry_config import RegistryConfig

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
        try:
            from ..heysol.registry_config import RegistryConfig

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


# Add command groups
app.add_typer(logs_app, name="logs")
app.add_typer(memory_app, name="memory")
app.add_typer(profile_app, name="profile")
app.add_typer(registry_app, name="registry")
app.add_typer(spaces_app, name="spaces")
app.add_typer(tools_app, name="tools")
app.add_typer(webhooks_app, name="webhooks")


def main():
    app()


if __name__ == "__main__":
    main()
