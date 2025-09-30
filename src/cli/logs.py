"""
Log-related CLI commands.
"""

from typing import Optional

import typer

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("list")
def logs_list(
    space_id: Optional[str] = typer.Option(None, help="Space ID"),
    source: Optional[str] = typer.Option(None, help="Filter by source"),
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
    status: Optional[str] = typer.Option(None, help="Filter by status"),
    start_date: Optional[str] = typer.Option(None, help="Start date filter"),
    end_date: Optional[str] = typer.Option(None, help="End date filter"),
) -> None:
    """Get ingestion logs."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    if space_id:
        spaces = client.get_spaces()
        space_ids = [space["id"] for space in spaces]
        if space_id not in space_ids:
            typer.echo(
                f"Invalid space ID '{space_id}'. Available space IDs: {', '.join(space_ids)}",
                err=True,
            )
            raise typer.Exit(1)

    logs_list = client.get_ingestion_logs(
        space_id=space_id,
        limit=limit,
        offset=offset,
        status=None,
        start_date=start_date,
        end_date=end_date,
    )

    if status:
        logs_list = [log for log in logs_list if log.get("status") == status]

    if source:
        logs_list = [log for log in logs_list if log.get("source") == source]

    typer.echo(format_json_output(logs_list, pretty))
    client.close()


@app.command("delete")
def logs_delete(
    log_id: str, confirm: bool = typer.Option(False, help="Confirm deletion (required)")
) -> None:
    """Delete a specific log entry by ID."""
    if not confirm:
        typer.echo("Deletion requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.delete_log_entry(log_id=log_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("delete-by-source")
def logs_delete_by_source(
    source: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs"),
    confirm: bool = typer.Option(False, help="Confirm deletion (required)"),
    limit: int = typer.Option(1000, help="Maximum logs to process"),
) -> None:
    """Delete logs by source (batch operation)."""
    if not confirm:
        typer.echo("Deletion requires --confirm flag for safety", err=True)
        raise typer.Exit(1)

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    if space_id:
        spaces = client.get_spaces()
        space_ids = [space["id"] for space in spaces]
        if space_id not in space_ids:
            typer.echo(
                f"Invalid space ID '{space_id}'. Available space IDs: {', '.join(space_ids)}",
                err=True,
            )
            raise typer.Exit(1)

    typer.echo(f"Fetching logs to find source '{source}'...")
    logs_list = client.get_ingestion_logs(space_id=space_id, limit=limit, offset=0)

    source_logs = [log for log in logs_list if log.get("source") == source]

    if not source_logs:
        typer.echo(
            format_json_output(
                {"message": f"No logs found for source '{source}'", "deleted": 0}, pretty
            )
        )
        client.close()
        return

    typer.echo(f"Found {len(source_logs)} logs for source '{source}'. Deleting...")

    deleted_count = 0
    failed_count = 0

    for log in source_logs:
        try:
            # Show informative details before deletion
            message_preview = (
                log.get("message", "")[:100] + "..."
                if len(log.get("message", "")) > 100
                else log.get("message", "")
            )
            metadata = log.get("metadata", {})
            created_at = log.get("created_at", "unknown")
            typer.echo(f"Deleting log {log['id']}:")
            typer.echo(f"  Message: {message_preview}")
            typer.echo(f"  Created: {created_at}")
            if metadata:
                typer.echo(f"  Metadata: {metadata}")
            typer.echo("")

            client.delete_log_entry(log_id=log["id"])
            deleted_count += 1
            typer.echo(f"✓ Successfully deleted log {log['id']}")
            typer.echo("-" * 50)
        except Exception as e:
            failed_count += 1
            typer.echo(f"✗ Failed to delete log {log['id']}: {str(e)}")
            typer.echo("-" * 50)

    result = {
        "source": source,
        "total_found": len(source_logs),
        "deleted": deleted_count,
        "failed": failed_count,
        "message": f"Batch deletion completed for source '{source}'",
    }

    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("get")
def logs_get(log_id: str) -> None:
    """Get a specific log by ID."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    result = client.get_specific_log(log_id=log_id)
    typer.echo(format_json_output(result, pretty))
    client.close()


@app.command("get-by-source")
def logs_get_by_source(
    source: str,
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs"),
    limit: int = typer.Option(100, help="Result limit"),
    offset: int = typer.Option(0, help="Result offset"),
    status: Optional[str] = typer.Option(None, help="Filter by status"),
    start_date: Optional[str] = typer.Option(None, help="Start date filter"),
    end_date: Optional[str] = typer.Option(None, help="End date filter"),
) -> None:
    """Get logs filtered by source using efficient streaming."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    if space_id:
        spaces = client.get_spaces()
        space_ids = [space["id"] for space in spaces]
        if space_id not in space_ids:
            typer.echo(
                f"Invalid space ID '{space_id}'. Available space IDs: {', '.join(space_ids)}",
                err=True,
            )
            raise typer.Exit(1)

    # Use the new get_logs_by_source method that uses the generator
    filtered_logs = client.get_logs_by_source(
        source=source,
        space_id=space_id,
        limit=limit,
        offset=offset,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )

    typer.echo(format_json_output(filtered_logs, pretty))
    client.close()


@app.command("status")
def logs_status(
    space_id: Optional[str] = typer.Option(None, help="Space ID to check status for"),
    run_id: Optional[str] = typer.Option(None, help="Run ID from ingestion response"),
) -> None:
    """Check ingestion processing status."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    if space_id:
        spaces = client.get_spaces()
        space_ids = [space["id"] for space in spaces]
        if space_id not in space_ids:
            typer.echo(
                f"Invalid space ID '{space_id}'. Available space IDs: {', '.join(space_ids)}",
                err=True,
            )
            raise typer.Exit(1)

    status_info = client.check_ingestion_status(run_id=run_id, space_id=space_id)
    typer.echo(format_json_output(status_info, pretty))
    client.close()


@app.command("copy")
def logs_copy(
    log_id: str,
    new_source: Optional[str] = typer.Option(
        None, help="New source identifier (preserves original if not specified)"
    ),
    new_space_id: Optional[str] = typer.Option(
        None, help="New space ID (preserves original if not specified)"
    ),
    new_session_id: Optional[str] = typer.Option(
        None, help="New session ID (preserves original if not specified)"
    ),
    override_metadata: Optional[str] = typer.Option(
        None, help='JSON string of metadata fields to override (e.g., \'{"priority":"high"}\')'
    ),
) -> None:
    """Copy a log entry with all metadata preserved, allowing selective field overrides."""
    import json

    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    # Get the original log entry
    try:
        original_log = client.get_specific_log(log_id=log_id)
    except Exception as e:
        typer.echo(f"Failed to retrieve log entry {log_id}: {str(e)}", err=True)
        raise typer.Exit(1)

    # Parse override metadata if provided
    parsed_override_metadata = None
    if override_metadata:
        try:
            parsed_override_metadata = json.loads(override_metadata)
        except json.JSONDecodeError as e:
            typer.echo(f"Invalid JSON for override-metadata: {str(e)}", err=True)
            raise typer.Exit(1)

    # Perform the copy operation
    try:
        result = client.copy_log_entry(
            log_entry=original_log,
            new_source=new_source,
            new_space_id=new_space_id,
            new_session_id=new_session_id,
            override_metadata=parsed_override_metadata,
        )
        typer.echo(format_json_output(result, pretty))
    except Exception as e:
        typer.echo(f"Failed to copy log entry: {str(e)}", err=True)
        raise typer.Exit(1)
    finally:
        client.close()


@app.command("sources")
def logs_sources(
    space_id: Optional[str] = typer.Option(None, help="Space ID to filter logs"),
    limit: int = typer.Option(1000, help="Result limit for source extraction"),
    offset: int = typer.Option(0, help="Result offset"),
    status: Optional[str] = typer.Option(None, help="Filter by status"),
    start_date: Optional[str] = typer.Option(None, help="Start date filter"),
    end_date: Optional[str] = typer.Option(None, help="End date filter"),
) -> None:
    """List unique sources from memory logs."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    if space_id:
        spaces = client.get_spaces()
        space_ids = [space["id"] for space in spaces]
        if space_id not in space_ids:
            typer.echo(
                f"Invalid space ID '{space_id}'. Available space IDs: {', '.join(space_ids)}",
                err=True,
            )
            raise typer.Exit(1)

    logs_list = client.get_ingestion_logs(
        space_id=space_id,
        limit=limit,
        offset=offset,
        status=None,
        start_date=start_date,
        end_date=end_date,
    )

    if status:
        logs_list = [log for log in logs_list if log.get("status") == status]

    sources = set()
    for log in logs_list:
        if "source" in log:
            sources.add(log["source"])

    unique_sources = sorted(list(sources))
    result = {"sources": unique_sources, "count": len(unique_sources)}

    typer.echo(format_json_output(result, pretty))
    client.close()


if __name__ == "__main__":
    app()
