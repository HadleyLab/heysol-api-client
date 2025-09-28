"""
Webhook-related CLI commands.
"""

from typing import List, Optional

import typer

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("create")
def webhooks_create(
    url: str,
    secret: str = typer.Option(..., help="Webhook secret"),
    events: Optional[List[str]] = typer.Option(
        None, help="Events to subscribe to (can specify multiple)"
    ),
):
    """Create a new webhook."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.register_webhook(url=url, events=events, secret=secret)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("get")
def webhooks_get(webhook_id: str):
    """Get webhook details."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.get_webhook(webhook_id=webhook_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("list")
def webhooks_list(
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    active: Optional[bool] = typer.Option(None, help="Filter by active status"),
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
):
    """List webhooks."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.list_webhooks(space_id=space_id, active=active, limit=limit, offset=offset)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("update")
def webhooks_update(
    webhook_id: str,
    url: str,
    events: List[str] = typer.Option(..., help="Events to subscribe to (can specify multiple)"),
    secret: str = typer.Option(..., help="Webhook secret"),
    active: bool = typer.Option(True, help="Webhook active status"),
):
    """Update webhook properties."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.update_webhook(
        webhook_id=webhook_id, url=url, events=events, secret=secret, active=active
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("delete")
def webhooks_delete(
    webhook_id: str, confirm: bool = typer.Option(False, help="Confirm deletion (required)")
):
    """Delete a webhook."""
    if not confirm:
        typer.echo("Webhook deletion requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.delete_webhook(webhook_id=webhook_id, confirm=confirm)
    typer.echo(format_json_output(result, pretty))
    client.close()


if __name__ == "__main__":
    app()
