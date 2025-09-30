"""
High-level operations for the HeySol client, such as data transfers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from .client import HeySolClient


def move_logs_to_instance(
    source_client: HeySolClient,
    target_client: HeySolClient,
    source: str | None = None,
    space_id: str | None = None,
    limit: int = 10000,
    confirm: bool = False,
    delete_after_move: bool = True,
    target_source: str | None = None,
    target_space_id: str | None = None,
    target_session_id: str | None = None,
) -> Dict[str, Any]:
    """Move logs to target instance (copy + delete)."""
    # First copy the logs
    copy_result = _transfer_logs_to_instance(
        source_client=source_client,
        target_client=target_client,
        source=source or "*",
        space_id=space_id,
        limit=limit,
        confirm=confirm,
        operation="copy",
        delete_after_transfer=False,  # Don't delete during copy phase
        target_source=target_source,
        target_space_id=target_space_id,
        target_session_id=target_session_id,
    )

    # If this was a preview, return the preview result
    if not confirm:
        return {
            "operation": "move_preview",
            "logs_to_move": copy_result.get("logs_to_transfer", 0),
            "total_count": copy_result.get("total_count", 0),
            "message": f"Preview: Would move {copy_result.get('logs_to_transfer', 0)} logs",
            "source": source or "*",
            "target_instance": target_client.base_url,
        }

    # If delete_after_move is False, this is actually just a copy operation
    if not delete_after_move:
        return copy_result

    # Perform the delete phase for actual move
    logs_result = source_client.get_logs_by_source(
        source=source or "*", space_id=space_id, limit=limit
    )

    logs = logs_result.get("logs", [])

    deleted_count = 0
    for log in logs:
        try:
            source_client.delete_log_entry(log["id"])
            deleted_count += 1
        except Exception:
            # Continue with other deletions even if one fails
            continue

    return {
        "operation": "move",
        "transferred_count": copy_result.get("transferred_count", 0),
        "deleted_count": deleted_count,
        "total_attempted": len(logs),
        "source_instance": source_client.base_url,
        "target_instance": target_client.base_url,
        "message": f"Moved {copy_result.get('transferred_count', 0)} logs",
    }


def _transfer_logs_to_instance(
    source_client: HeySolClient,
    target_client: HeySolClient,
    source: str,
    space_id: str | None = None,
    limit: int = 10000,
    confirm: bool = False,
    operation: str = "move",
    delete_after_transfer: bool = True,
    target_source: str | None = None,
    target_space_id: str | None = None,
    target_session_id: str | None = None,
) -> Dict[str, Any]:
    """Internal method to transfer logs between instances."""
    # Get logs by source
    logs_result = source_client.get_logs_by_source(source=source, space_id=space_id, limit=limit)

    logs = logs_result.get("logs", [])
    total_count = logs_result.get("total_count", len(logs))

    if not confirm:
        # Preview mode
        return {
            "operation": f"{operation}_preview",
            "logs_to_transfer": len(logs),
            "total_count": total_count,
            "message": f"Preview: Would {operation} {len(logs)} logs",
            "source": source,
            "target_instance": target_client.base_url,
        }

    # Perform actual transfer
    transferred_count = 0
    deleted_count = 0

    for log in logs:
        try:
            # Extract message content
            message_content = log.get("ingestText") or log.get("data", {}).get("episodeBody")
            if not message_content:
                continue

            # Extract original metadata and timestamp to preserve them
            original_data = log.get("data", {})
            original_metadata = original_data.get("metadata", {})
            original_reference_time = original_data.get("referenceTime") or log.get("time")
            original_session_id = original_data.get("sessionId") or target_session_id

            # Determine target source - use target_source param, or target client's default source
            final_target_source = target_source or target_client.api_client.source

            # Use direct API call to preserve all fields including timestamp
            payload: Dict[str, Any] = {
                "episodeBody": message_content,
                "referenceTime": original_reference_time,
                "metadata": original_metadata,
                "source": final_target_source,
                "sessionId": original_session_id,
            }
            if target_space_id:
                payload["spaceId"] = target_space_id

            target_client.api_client._make_request("POST", "add", data=payload)
            transferred_count += 1

            # Delete from source if move operation
            if delete_after_transfer and operation == "move":
                source_client.delete_log_entry(log["id"])
                deleted_count += 1

        except Exception:
            # Continue with other logs even if one fails
            continue

    return {
        "operation": operation,
        "transferred_count": transferred_count,
        "total_attempted": len(logs),
        "deleted_count": deleted_count if operation == "move" else None,
        "source_instance": source_client.api_client.base_url,
        "target_instance": target_client.api_client.base_url,
        "message": f"{'Moved' if operation == 'move' else 'Copied'} {transferred_count} logs",
    }
