"""
Profile-related CLI commands.
"""

import time
from typing import Any

import typer

from .common import format_json_output, get_client_from_context

app = typer.Typer()


@app.command("get")
def profile_get(ctx: typer.Context) -> None:
    """Get user profile."""
    client = get_client_from_context(ctx)
    profile = client.get_user_profile()
    typer.echo(format_json_output(profile, True))
    client.close()


@app.command("health")
def profile_health(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed health check results"
    )
) -> None:
    """Check API health by testing all endpoints."""
    from heysol.health_check import HeySolHealthChecker
    
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    checker = HeySolHealthChecker(api_key=client.api_key)
    result = checker.run_comprehensive_health_check()

    # Print human-readable summary
    checker.print_health_report(result)

    # Only show JSON if verbose is True (for programmatic use)
    if verbose:
        # Convert dataclass to dict for JSON serialization
        import dataclasses
        result_dict = dataclasses.asdict(result)

        typer.echo()
        typer.echo("Raw JSON output:")
        typer.echo(format_json_output(result_dict, pretty))


if __name__ == "__main__":
    app()
