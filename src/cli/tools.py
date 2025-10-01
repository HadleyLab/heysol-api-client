"""
MCP tools-related CLI commands.
"""

import typer

from .common import format_json_output, get_client_from_context

app = typer.Typer()


@app.command("list")
def tools_list(ctx: typer.Context) -> None:
    """List MCP tools."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    tools_list = client.get_available_tools()
    typer.echo(format_json_output(tools_list, pretty))
    client.close()


if __name__ == "__main__":
    app()
