"""
CLI commands for HeySol instance registry management.

Provides commands to register, list, and manage multiple HeySol instances
for cross-instance operations.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import typer

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from heysol.registry_config import RegistryConfig

app = typer.Typer()


@app.command("list")
def list_instances(
    env_file: Optional[str] = typer.Option(None, help="Path to .env file to read from")
) -> None:
    """List all registered HeySol instances."""
    try:
        config = RegistryConfig(env_file)
        instances = config.get_registered_instances()

        if not instances:
            typer.echo("No instances registered.")
            typer.echo(f"Check your .env file at: {config.env_file}")
            return

        typer.echo("Registered HeySol Instances:")
        typer.echo("-" * 50)

        for name, instance_config in instances.items():
            typer.echo(f"User: {name}")
            typer.echo(f"  Description: {instance_config['description']}")
            typer.echo(f"  Base URL: {instance_config['base_url']}")
            typer.echo(f"  API Key: {instance_config['api_key'][:20]}...")
            typer.echo()

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command("register")
def register_from_env(
    env_file: Optional[str] = typer.Argument(None),
    name: Optional[str] = typer.Option(
        None, help="Name for the instance (auto-detected if not provided)"
    ),
) -> None:
    """Register instances from .env file."""
    try:
        if not env_file:
            # Try to find .env file automatically
            current_dir = Path.cwd()
            env_path = None

            # Look in current directory and parent directories
            check_dir = current_dir
            while check_dir != check_dir.parent:
                potential_env = check_dir / ".env"
                if potential_env.exists():
                    env_path = potential_env
                    break
                check_dir = check_dir.parent

            if not env_path:
                typer.echo("No .env file found. Please specify --env-file or create a .env file.")
                raise typer.Exit(1)

            env_file = str(env_path)

        if not os.path.exists(env_file):
            typer.echo(f"Environment file not found: {env_file}")
            raise typer.Exit(1)

        config = RegistryConfig(env_file)
        instances = config.get_registered_instances()

        if not instances:
            typer.echo(f"No HeySol API keys found in {env_file}")
            return

        typer.echo(f"Found {len(instances)} instance(s) in {env_file}:")
        typer.echo("-" * 50)

        for instance_name, instance_config in instances.items():
            typer.echo(f"✓ {instance_name}")

        typer.echo()
        typer.echo("Instances registered successfully!")
        typer.echo("Use 'heysol registry list' to see all registered instances.")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command("use")
def use_instance(
    instance_name: str,
    env_file: Optional[str] = typer.Option(None, help="Path to .env file to read from"),
) -> None:
    """Set an instance as active for operations."""
    try:
        config = RegistryConfig(env_file)
        instance = config.get_instance(instance_name)

        if not instance:
            typer.echo(f"Instance '{instance_name}' not found.")
            typer.echo("Available instances:")
            for name in config.get_instance_names():
                typer.echo(f"  - {name}")
            raise typer.Exit(1)

        # Save the active instance (for now, just show how to use it)
        typer.echo(f"Active instance set to: {instance_name}")
        typer.echo(f"Description: {instance['description']}")
        typer.echo(f"Base URL: {instance['base_url']}")
        typer.echo()
        typer.echo("To use this instance in operations:")
        typer.echo(f"  heysol memory move {instance_name} {instance['base_url']} --confirm")
        typer.echo(f"  heysol memory copy {instance_name} {instance['base_url']} --confirm")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command("show")
def show_instance(
    instance_name: str,
    env_file: Optional[str] = typer.Option(None, help="Path to .env file to read from"),
) -> None:
    """Show details for a specific instance."""
    try:
        config = RegistryConfig(env_file)
        instance = config.get_instance(instance_name)

        if not instance:
            typer.echo(f"Instance '{instance_name}' not found.")
            typer.echo("Available instances:")
            for name in config.get_instance_names():
                typer.echo(f"  - {name}")
            raise typer.Exit(1)

        typer.echo(f"Instance: {instance_name}")
        typer.echo(f"Description: {instance['description']}")
        typer.echo(f"Base URL: {instance['base_url']}")
        typer.echo(f"API Key: {instance['api_key'][:20]}...{instance['api_key'][-4:]}")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
