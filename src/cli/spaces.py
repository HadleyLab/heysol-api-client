"""
Space-related CLI commands.
"""

from typing import List, Optional

import typer

from heysol import HeySolError

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("list")
def spaces_list() -> None:
    """List available spaces."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    try:
        client = create_client(api_key=api_key, base_url=base_url)
        spaces_list = client.get_spaces()
        typer.echo(format_json_output(spaces_list, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("create")
def spaces_create(
    name: str, description: Optional[str] = typer.Option(None, help="Space description")
) -> None:
    """Create a new space."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    try:
        client = create_client(api_key=api_key, base_url=base_url)
        result = client.create_space(name, description or "")
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("get")
def spaces_get(
    space_id: str,
    include_stats: bool = typer.Option(True, help="Include statistics"),
    include_metadata: bool = typer.Option(True, help="Include metadata"),
) -> None:
    """Get space details."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    try:
        client = create_client(api_key=api_key, base_url=base_url)
        details = client.get_space_details(space_id, include_stats, include_metadata)
        typer.echo(format_json_output(details, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("update")
def spaces_update(
    space_id: str,
    name: Optional[str] = typer.Option(None, help="New space name"),
    description: Optional[str] = typer.Option(None, help="New space description"),
    metadata: Optional[str] = typer.Option(None, help="JSON metadata string"),
) -> None:
    """Update space properties."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    parsed_metadata = None
    if metadata:
        try:
            import json

            parsed_metadata = json.loads(metadata)
        except json.JSONDecodeError as e:
            typer.echo(f"Invalid JSON metadata: {e}", err=True)
            raise typer.Exit(1)

    try:
        client = create_client(api_key=api_key, base_url=base_url)
        result = client.update_space(
            space_id=space_id, name=name, description=description, metadata=parsed_metadata
        )
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("bulk-ops")
def spaces_bulk_ops(
    intent: str,
    space_id: Optional[str] = typer.Option(None, help="Target space ID"),
    statement_ids: Optional[List[str]] = typer.Option(
        None, help="Statement IDs (can specify multiple)"
    ),
    space_ids: Optional[List[str]] = typer.Option(None, help="Space IDs (can specify multiple)"),
) -> None:
    """Perform bulk operations on spaces."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    try:
        client = create_client(api_key=api_key, base_url=base_url)
        result = client.bulk_space_operations(
            intent=intent,
            space_id=space_id,
            statement_ids=statement_ids,
            space_ids=space_ids,
        )
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("delete")
def spaces_delete(
    space: str, confirm: bool = typer.Option(False, help="Confirm deletion (required)")
) -> None:
    """Delete a space by ID or name."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    if not confirm:
        typer.echo("Space deletion requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    try:
        client = create_client(api_key=api_key, base_url=base_url)

        # Resolve space name to ID if needed
        space_id = space
        if not space.startswith("cm"):  # Assume IDs start with 'cm', names don't
            spaces_list = client.get_spaces()
            for s in spaces_list:
                if s.get("name") == space:
                    space_id = s.get("id", "")
                    break
            else:
                typer.echo(f"Space '{space}' not found", err=True)
                raise typer.Exit(1)

        result = client.delete_space(space_id=space_id, confirm=confirm)
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    app()
