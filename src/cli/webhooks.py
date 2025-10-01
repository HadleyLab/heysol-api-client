"""
Webhook-related CLI commands.
"""

from typing import List, Optional

import typer

from .common import format_json_output, get_client_from_context

app = typer.Typer()


@app.command("create")
def webhooks_create(
    ctx: typer.Context,
    url: str,
    secret: str = typer.Option(..., help="Webhook secret"),
    events: Optional[List[str]] = typer.Option(
        None, help="Events to subscribe to (can specify multiple)"
    ),
) -> None:
    """Create a new webhook."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.register_webhook(url=url, events=events, secret=secret)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("get")
def webhooks_get(ctx: typer.Context, webhook_id: str) -> None:
    """Get webhook details."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.get_webhook(webhook_id=webhook_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("list")
def webhooks_list(
    ctx: typer.Context,
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    active: Optional[bool] = typer.Option(None, help="Filter by active status"),
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
) -> None:
    """List webhooks."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.list_webhooks(space_id=space_id, active=active, limit=limit, offset=offset)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("update")
def webhooks_update(
    ctx: typer.Context,
    webhook_id: str,
    url: str,
    events: List[str] = typer.Option(..., help="Events to subscribe to (can specify multiple)"),
    secret: str = typer.Option(..., help="Webhook secret"),
    active: bool = typer.Option(True, help="Webhook active status"),
) -> None:
    """Update webhook properties."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.update_webhook(
        webhook_id=webhook_id, url=url, events=events, secret=secret, active=active
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("delete")
def webhooks_delete(
    ctx: typer.Context,
    webhook_id: str,
    confirm: bool = typer.Option(False, help="Confirm deletion (required)"),
) -> None:
    """Delete a webhook."""
    if not confirm:
        typer.echo("Webhook deletion requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.delete_webhook(webhook_id=webhook_id, confirm=confirm)
    typer.echo(format_json_output(result, pretty))
    client.close()


if __name__ == "__main__":
    app()
