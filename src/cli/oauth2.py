"""
OAuth2-related CLI commands.
"""

from typing import Optional

import typer

from ..heysol import HeySolError
from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("authorize")
def oauth2_authorize(
    redirect_uri: Optional[str] = typer.Option(None, help="Redirect URI"),
    scope: Optional[str] = typer.Option(None, help="OAuth2 scope"),
    api_key: Optional[str] = typer.Option(
        None, help="HeySol API key (overrides environment variable)"
    ),
    base_url: Optional[str] = typer.Option(None, help="Base URL for API (overrides default)"),
    pretty: bool = typer.Option(True, help="Pretty print JSON output"),
    skip_mcp: bool = typer.Option(False, help="Skip MCP initialization"),
):
    """OAuth2 authorization endpoint."""
    try:
        # Use global credentials
        resolved_api_key, resolved_base_url = get_auth_from_global()
        if api_key:
            resolved_api_key = api_key
        if base_url:
            resolved_base_url = base_url

        client = create_client(api_key=resolved_api_key, base_url=resolved_base_url)
        # This would typically redirect to OAuth2 authorization URL
        # For now, we'll show the authorization URL
        auth_url = f"{client.base_url}/oauth2/authorize"
        if redirect_uri:
            auth_url += f"?redirect_uri={redirect_uri}"
        if scope:
            auth_url += f"&scope={scope}"

        result = {"authorization_url": auth_url, "redirect_uri": redirect_uri, "scope": scope}
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("token")
def oauth2_token(
    grant_type: str = typer.Option("authorization_code", help="OAuth2 grant type"),
    code: Optional[str] = typer.Option(None, help="Authorization code"),
    redirect_uri: Optional[str] = typer.Option(None, help="Redirect URI"),
    client_id: Optional[str] = typer.Option(None, help="OAuth2 client ID"),
    client_secret: Optional[str] = typer.Option(None, help="OAuth2 client secret"),
    api_key: Optional[str] = typer.Option(
        None, help="HeySol API key (overrides environment variable)"
    ),
    base_url: Optional[str] = typer.Option(None, help="Base URL for API (overrides default)"),
    pretty: bool = typer.Option(True, help="Pretty print JSON output"),
    skip_mcp: bool = typer.Option(False, help="Skip MCP initialization"),
):
    """OAuth2 token endpoint."""
    try:
        # Use global credentials
        resolved_api_key, resolved_base_url = get_auth_from_global()
        if api_key:
            resolved_api_key = api_key
        if base_url:
            resolved_base_url = base_url

        client = create_client(api_key=resolved_api_key, base_url=resolved_base_url)

        # Prepare token request data
        token_data = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        if code:
            token_data["code"] = code
        if redirect_uri:
            token_data["redirect_uri"] = redirect_uri

        # Make token request
        token_url = f"{client.base_url}/oauth2/token"
        import requests

        response = requests.post(
            token_url,
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        result = response.json()
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("userinfo")
def oauth2_userinfo(
    access_token: Optional[str] = typer.Option(None, help="Access token"),
    api_key: Optional[str] = typer.Option(
        None, help="HeySol API key (overrides environment variable)"
    ),
    base_url: Optional[str] = typer.Option(None, help="Base URL for API (overrides default)"),
    pretty: bool = typer.Option(True, help="Pretty print JSON output"),
    skip_mcp: bool = typer.Option(False, help="Skip MCP initialization"),
):
    """OAuth2 user info endpoint."""
    try:
        # Use global credentials
        resolved_api_key, resolved_base_url = get_auth_from_global()
        if api_key:
            resolved_api_key = api_key
        if base_url:
            resolved_base_url = base_url

        client = create_client(api_key=resolved_api_key, base_url=resolved_base_url)

        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        userinfo_url = f"{client.base_url}/oauth2/userinfo"
        import requests

        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


@app.command("introspect")
def oauth2_introspect(
    token: str,
    token_type: str = typer.Option("access_token", help="Token type"),
    client_id: Optional[str] = typer.Option(None, help="OAuth2 client ID"),
    client_secret: Optional[str] = typer.Option(None, help="OAuth2 client secret"),
    api_key: Optional[str] = typer.Option(
        None, help="HeySol API key (overrides environment variable)"
    ),
    base_url: Optional[str] = typer.Option(None, help="Base URL for API (overrides default)"),
    pretty: bool = typer.Option(True, help="Pretty print JSON output"),
    skip_mcp: bool = typer.Option(False, help="Skip MCP initialization"),
):
    """OAuth2 token introspection endpoint."""
    try:
        # Use global credentials
        resolved_api_key, resolved_base_url = get_auth_from_global()
        if api_key:
            resolved_api_key = api_key
        if base_url:
            resolved_base_url = base_url

        client = create_client(api_key=resolved_api_key, base_url=resolved_base_url)

        # Prepare introspection request data
        introspect_data = {
            "token": token,
            "token_type_hint": token_type,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        # Make introspection request
        introspect_url = f"{client.base_url}/oauth2/introspect"
        import requests

        response = requests.post(
            introspect_url,
            data=introspect_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        result = response.json()
        typer.echo(format_json_output(result, pretty))
    except HeySolError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    app()
