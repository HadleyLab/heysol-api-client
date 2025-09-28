"""
MCP tools-related CLI commands.
"""

import typer

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("list")
def tools_list():
    """List MCP tools."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    tools_list = client.get_available_tools()
    typer.echo(format_json_output(tools_list, pretty))
    client.close()


if __name__ == "__main__":
    app()
