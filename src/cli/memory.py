"""
Memory-related CLI commands.
"""

from typing import List, Optional

import typer

from .common import format_json_output, get_client_from_context

app = typer.Typer(help="Memory operations")


@app.command("ingest")
def memory_ingest(
    ctx: typer.Context,
    message: Optional[str] = typer.Argument(None, help="Message to ingest"),
    file: Optional[str] = typer.Option(None, help="File containing message to ingest"),
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    session_id: Optional[str] = typer.Option(None, help="Session ID"),
) -> None:
    """Ingest data into memory."""
    if not message and not file:
        typer.echo("Message or file is required", err=True)
        raise typer.Exit(1)

    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    final_message = message
    if file:
        with open(file, "r", encoding="utf-8") as f:
            final_message = f.read()

    if not final_message:
        typer.echo("Message or file is required", err=True)
        raise typer.Exit(1)

    result = client.ingest(message=final_message, space_id=space_id, session_id=session_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("search")
def memory_search(
    ctx: typer.Context,
    query: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    limit: int = typer.Option(10, help="Result limit"),
    include_invalidated: bool = typer.Option(False, help="Include invalidated results"),
) -> None:
    """Search memory."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

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
    ctx: typer.Context,
    query: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    limit: int = typer.Option(10, help="Result limit"),
    depth: int = typer.Option(2, help="Graph search depth"),
    include_metadata: bool = typer.Option(True, help="Include metadata"),
) -> None:
    """Search knowledge graph."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

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
    ctx: typer.Context,
    data: Optional[str] = typer.Argument(None, help="Data to queue"),
    file: Optional[str] = typer.Option(None, help="File containing data to queue"),
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    priority: str = typer.Option("normal", help="Priority level"),
    tags: Optional[List[str]] = typer.Option(None, help="Tags (can specify multiple)"),
    metadata: Optional[str] = typer.Option(None, help="JSON metadata string"),
) -> None:
    """Add data to ingestion queue."""
    if not data and not file:
        typer.echo("Data or file is required", err=True)
        raise typer.Exit(1)

    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    final_data = data
    if file:
        with open(file, "r", encoding="utf-8") as f:
            final_data = f.read()

    parsed_metadata = None
    if metadata:
        import json

        parsed_metadata = json.loads(metadata)

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
    ctx: typer.Context,
    episode_id: str,
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
    include_metadata: bool = typer.Option(True, help="Include metadata"),
) -> None:
    """Get episode facts."""
    client = get_client_from_context(ctx)
    pretty = True  # Always pretty print

    result = client.get_episode_facts(
        episode_id=episode_id, limit=limit, offset=offset, include_metadata=include_metadata
    )
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("move")
def memory_move(
    ctx: typer.Context,
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
) -> None:
    """Move logs to target instance (copy + delete)."""
    if not confirm:
        typer.echo("Move operation requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    source_client = get_client_from_context(ctx)
    pretty = True

    from heysol.registry_config import RegistryConfig

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

    target_api_key = target_instance.get("api_key")
    target_base_url = target_instance.get("base_url")

    if not target_api_key or not target_base_url:
        typer.echo(f"Target user '{target_user}' has incomplete configuration.", err=True)
        raise typer.Exit(1)

    from .common import create_client
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
    ctx: typer.Context,
    target_user: str = typer.Option(..., help="Target user instance name from registry"),
    target_space_id: Optional[str] = typer.Option(None, help="Target space ID for copied logs"),
    target_session_id: Optional[str] = typer.Option(None, help="Target session ID for copied logs"),
    source_filter: Optional[str] = typer.Option(
        None, help="Source identifier to filter logs (optional)"
    ),
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs (optional)"),
    limit: int = typer.Option(10, help="Maximum number of logs to copy (default: 10)"),
    confirm: bool = typer.Option(False, help="Actually perform the copy operation"),
) -> None:
    """Copy logs to target instance."""
    if not confirm:
        typer.echo("Copy operation requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    source_client = get_client_from_context(ctx)
    pretty = True

    from heysol.registry_config import RegistryConfig

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

    target_api_key = target_instance["api_key"]
    target_base_url = target_instance["base_url"]

    from .common import create_client
    target_client = create_client(api_key=target_api_key, base_url=target_base_url)

    result = source_client.move_logs_to_instance(
        target_client=target_client,
        source=source_filter,
        space_id=space_id,
        limit=limit,
        confirm=confirm,
        delete_after_move=False,  # This makes it a copy operation
        target_space_id=target_space_id,
        target_session_id=target_session_id,
    )
    typer.echo("Copy operation completed.")
    typer.echo(format_json_output(result, pretty))
    source_client.close()
    target_client.close()


@app.command("copy-by-id")
def memory_copy_by_id(
    ctx: typer.Context,
    log_id: str,
    target_user: str = typer.Option(..., help="Target user instance name from registry"),
    target_space_id: Optional[str] = typer.Option(None, help="Target space ID for copied log"),
    target_session_id: Optional[str] = typer.Option(None, help="Target session ID for copied log"),
    target_source: Optional[str] = typer.Option(
        None, help="Target source identifier (optional, defaults to original)"
    ),
    confirm: bool = typer.Option(False, help="Actually perform the copy operation"),
) -> None:
    """Copy a specific log by ID to target instance."""
    source_client = get_client_from_context(ctx)
    pretty = True

    from heysol.registry_config import RegistryConfig

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

    target_api_key = target_instance["api_key"]
    target_base_url = target_instance["base_url"]

    from .common import create_client
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
