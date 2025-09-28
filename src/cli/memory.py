"""
Memory-related CLI commands.
"""

from typing import List, Optional

import typer

from ..heysol import HeySolClient

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer(help="Memory operations")


@app.command("ingest")
def memory_ingest(
    message: Optional[str] = typer.Argument(None, help="Message to ingest"),
    file: Optional[str] = typer.Option(None, help="File containing message to ingest"),
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    session_id: Optional[str] = typer.Option(None, help="Session ID"),
):
    """Ingest data into memory."""
    if not message and not file:
        typer.echo("Message or file is required", err=True)
        raise typer.Exit(1)

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    final_message = message
    if file:
        with open(file, "r", encoding="utf-8") as f:
            final_message = f.read()

    if not final_message:
        typer.echo("Message or file is required", err=True)
        raise typer.Exit(1)

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.ingest(message=final_message, space_id=space_id, session_id=session_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("search")
def memory_search(
    query: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    limit: int = typer.Option(10, help="Result limit"),
    include_invalidated: bool = typer.Option(False, help="Include invalidated results"),
):
    """Search memory."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.search(
        query=query,
        space_ids=[space_id] if space_id else None,
        limit=limit,
        include_invalidated=include_invalidated,
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("search-graph")
def memory_search_graph(
    query: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    limit: int = typer.Option(10, help="Result limit"),
    depth: int = typer.Option(2, help="Graph search depth"),
    include_metadata: bool = typer.Option(True, help="Include metadata"),
):
    """Search knowledge graph."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.search_knowledge_graph(
        query=query,
        space_id=space_id,
        limit=limit,
        depth=depth,
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("queue")
def memory_queue(
    data: Optional[str] = typer.Argument(None, help="Data to queue"),
    file: Optional[str] = typer.Option(None, help="File containing data to queue"),
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    priority: str = typer.Option("normal", help="Priority level"),
    tags: Optional[List[str]] = typer.Option(None, help="Tags (can specify multiple)"),
    metadata: Optional[str] = typer.Option(None, help="JSON metadata string"),
):
    """Add data to ingestion queue."""
    if not data and not file:
        typer.echo("Data or file is required", err=True)
        raise typer.Exit(1)

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    final_data = data
    if file:
        with open(file, "r", encoding="utf-8") as f:
            final_data = f.read()

    parsed_metadata = None
    if metadata:
        import json

        parsed_metadata = json.loads(metadata)

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.add_data_to_ingestion_queue(
        data=final_data,
        space_id=space_id,
        priority=priority,
        tags=tags,
        metadata=parsed_metadata,
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("episode")
def memory_episode(
    episode_id: str,
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
    include_metadata: bool = typer.Option(True, help="Include metadata"),
):
    """Get episode facts."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.get_episode_facts(
        episode_id=episode_id, limit=limit, offset=offset, include_metadata=include_metadata
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("move")
def memory_move(
    target_user: str = typer.Option(..., help="Target user instance name from registry"),
    target_api_key: Optional[str] = typer.Option(
        None, help="Target HeySol API key (if not using registry)"
    ),
    target_base_url: Optional[str] = typer.Option(
        None, help="Target base URL for API (if not using registry)"
    ),
    target_source: Optional[str] = typer.Option(
        None, help="Target source identifier for moved logs"
    ),
    target_space_id: Optional[str] = typer.Option(None, help="Target space ID for moved logs"),
    target_session_id: Optional[str] = typer.Option(None, help="Target session ID for moved logs"),
    source_filter: Optional[str] = typer.Option(
        None, help="Source identifier to filter logs (optional)"
    ),
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs (optional)"),
    confirm: bool = typer.Option(False, help="Actually perform the move operation"),
    keep_source: bool = typer.Option(False, help="Keep logs in source after move"),
):
    """Move logs to target instance (copy + delete)."""
    if not confirm:
        typer.echo("Move operation requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    source_api_key, source_base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    from ..heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    if target_user not in registry.get_instance_names():
        typer.echo(
            f"Target user '{target_user}' not found in registry. Use 'heysol registry list' to see available users.",
            err=True,
        )
        raise typer.Exit(1)
    target_instance = registry.get_instance(target_user)
    if not target_instance:
        typer.echo(f"Target user '{target_user}' not found in registry.", err=True)
        raise typer.Exit(1)
    # At this point target_instance is guaranteed to be not None
    target_api_key = target_instance["api_key"]  # type: ignore
    target_base_url = target_instance["base_url"]  # type: ignore

    source_client = create_client(api_key=source_api_key, base_url=source_base_url)
    target_client = create_client(api_key=target_api_key, base_url=target_base_url)

    result = source_client.move_logs_to_instance(
        target_client=target_client,
        source=source_filter,
        space_id=space_id,
        target_source=target_source,
        target_space_id=target_space_id,
        target_session_id=target_session_id,
        confirm=confirm,
        delete_after_move=not keep_source,
    )
    typer.echo("Move operation completed.")
    typer.echo(format_json_output(result, pretty))
    source_client.close()
    target_client.close()


@app.command("copy")
def memory_copy(
    target_user: str = typer.Option(..., help="Target user instance name from registry"),
    target_space_id: Optional[str] = typer.Option(None, help="Target space ID for copied logs"),
    target_session_id: Optional[str] = typer.Option(None, help="Target session ID for copied logs"),
    source_filter: Optional[str] = typer.Option(
        None, help="Source identifier to filter logs (optional)"
    ),
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs (optional)"),
    limit: int = typer.Option(10, help="Maximum number of logs to copy (default: 10)"),
    confirm: bool = typer.Option(False, help="Actually perform the copy operation"),
):
    """Copy logs to target instance."""
    if not confirm:
        typer.echo("Copy operation requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    source_api_key, source_base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    from ..heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    if target_user not in registry.get_instance_names():
        typer.echo(
            f"Target user '{target_user}' not found in registry. Use 'heysol registry list' to see available users.",
            err=True,
        )
        raise typer.Exit(1)
    target_instance = registry.get_instance(target_user)
    if not target_instance:
        typer.echo(f"Target user '{target_user}' not found in registry.", err=True)
        raise typer.Exit(1)
    # At this point target_instance is guaranteed to be not None
    target_api_key = target_instance["api_key"]  # type: ignore
    target_base_url = target_instance["base_url"]  # type: ignore

    source_client = create_client(api_key=source_api_key, base_url=source_base_url)
    target_client = create_client(api_key=target_api_key, base_url=target_base_url)

    result = HeySolClient._transfer_logs_to_instance(
        source_client=source_client,
        target_client=target_client,
        source=source_filter or "*",
        space_id=space_id,
        limit=limit,
        confirm=confirm,
        operation="copy",
        delete_after_transfer=False,
        target_source=None,
        target_space_id=target_space_id,
        target_session_id=target_session_id,
    )
    typer.echo("Copy operation completed.")
    typer.echo(format_json_output(result, pretty))
    source_client.close()
    target_client.close()


@app.command("copy-by-id")
def memory_copy_by_id(
    log_id: str,
    target_user: str = typer.Option(..., help="Target user instance name from registry"),
    target_space_id: Optional[str] = typer.Option(None, help="Target space ID for copied log"),
    target_session_id: Optional[str] = typer.Option(None, help="Target session ID for copied log"),
    target_source: Optional[str] = typer.Option(
        None, help="Target source identifier (optional, defaults to original)"
    ),
    confirm: bool = typer.Option(False, help="Actually perform the copy operation"),
):
    """Copy a specific log by ID to target instance."""
    source_api_key, source_base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    from ..heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    if target_user not in registry.get_instance_names():
        typer.echo(
            f"Target user '{target_user}' not found in registry. Use 'heysol registry list' to see available users.",
            err=True,
        )
        raise typer.Exit(1)
    target_instance = registry.get_instance(target_user)
    if not target_instance:
        typer.echo(f"Target user '{target_user}' not found in registry.", err=True)
        raise typer.Exit(1)
    # At this point target_instance is guaranteed to be not None
    target_api_key = target_instance["api_key"]  # type: ignore
    target_base_url = target_instance["base_url"]  # type: ignore

    source_client = create_client(api_key=source_api_key, base_url=source_base_url)
    target_client = create_client(api_key=target_api_key, base_url=target_base_url)

    source_log = source_client.get_specific_log(log_id=log_id)
    message_content = source_log.get("ingestText") or source_log.get("data", {}).get("episodeBody")
    if not message_content:
        typer.echo(f"Could not extract message content from log {log_id}", err=True)
        raise typer.Exit(1)

    final_target_source = target_source or source_log.get("source")

    if not confirm:
        typer.echo(
            f"Preview: Would copy log {log_id} with source '{final_target_source}' to target instance"
        )
        typer.echo(f"Message preview: {message_content[:100]}...")
        return

    result = target_client.ingest(
        message=message_content,
        space_id=target_space_id,
        session_id=target_session_id,
        source=final_target_source,
    )

    typer.echo(f"Successfully copied log {log_id} to target instance.")
    typer.echo(format_json_output(result, pretty))
    source_client.close()
    target_client.close()


if __name__ == "__main__":
    app()
