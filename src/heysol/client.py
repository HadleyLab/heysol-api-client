from typing import Any, Dict, Iterator, List, Optional, cast

from .clients.api_client import HeySolAPIClient
from .clients.mcp_client import HeySolMCPClient
from .config import HeySolConfig
from .exceptions import HeySolError, ValidationError
from .models import SearchResult


class HeySolClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        mcp_url: Optional[str] = None,
        config: Optional[HeySolConfig] = None,
        prefer_mcp: bool = False,
        skip_mcp_init: bool = False,
    ):
        """
        Initialize the unified HeySol client with both API and MCP support.

        Args:
            api_key: HeySol API key (required for authentication)
            base_url: Base URL for API endpoints (optional, uses config default)
            mcp_url: MCP endpoint URL (optional, uses config default if not provided)
            config: HeySolConfig object (optional, overrides individual parameters)
            prefer_mcp: Whether to prefer MCP over direct API when both are available
            skip_mcp_init: Whether to skip MCP initialization (useful for testing)
        """
        if config is None:
            config = HeySolConfig.from_env()

        if api_key is None:
            api_key = config.api_key
        if not base_url:
            base_url = config.base_url
        if not mcp_url:
            mcp_url = config.mcp_url

        if not api_key:
            raise ValidationError("API key is required")

        self.api_key = api_key
        self.base_url = base_url
        self.mcp_url = mcp_url
        self.prefer_mcp = prefer_mcp
        self.config = config

        # Initialize API client (always available)
        self.api_client = HeySolAPIClient(api_key=api_key, base_url=base_url, config=config)

        # Initialize MCP client (optional, with graceful fallback)
        self.mcp_client: Optional[HeySolMCPClient] = None
        self.mcp_available = False

        if not skip_mcp_init:
            try:
                self.mcp_client = HeySolMCPClient(api_key=api_key, mcp_url=mcp_url, config=config)
                self.mcp_available = self.mcp_client.is_mcp_available()
            except Exception as e:
                # Graceful degradation - MCP is optional
                print(f"Warning: MCP initialization failed: {e}")
                print("Continuing with API-only mode")
                self.mcp_client = None
                self.mcp_available = False

    @classmethod
    def from_env(cls) -> "HeySolClient":
        """Create client from environment variables."""
        config = HeySolConfig.from_env()
        return cls(config=config)

    # Core memory operations with MCP fallback
    def ingest(
        self,
        message: str,
        source: Optional[str] = None,
        space_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Ingest data with automatic MCP fallback."""
        if self.mcp_available and self.prefer_mcp and self.mcp_client is not None:
            try:
                return self.mcp_client.ingest_via_mcp(message, source, space_id, session_id)
            except Exception:
                # Fallback to API
                pass
        return self.api_client.ingest(message, space_id, session_id, source)

    def search(
        self,
        query: str,
        space_ids: Optional[List[str]] = None,
        limit: int = 10,
        include_invalidated: bool = False,
    ) -> SearchResult:
        """Search with automatic MCP fallback."""
        if self.mcp_available and self.prefer_mcp and self.mcp_client is not None:
            try:
                response = self.mcp_client.search_via_mcp(query, space_ids, limit)
                return SearchResult(**response)
            except Exception:
                # Fallback to API
                pass
        return self.api_client.search(query, space_ids, limit, include_invalidated)

    def get_spaces(self) -> List[Any]:
        """Get spaces with MCP fallback support."""
        if self.mcp_available and self.prefer_mcp and self.mcp_client is not None:
            try:
                result = self.mcp_client.get_spaces_via_mcp()
                # Handle different response formats from MCP
                if isinstance(result, dict):
                    return cast(List[Any], result.get("spaces", result))
                return cast(List[Any], result)
            except Exception:
                # Fallback to API
                pass
        return self.api_client.get_spaces()

    def create_space(self, name: str, description: str = "") -> Optional[str]:
        return self.api_client.create_space(name, description)

    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile with MCP fallback support."""
        if self.mcp_available and self.prefer_mcp and self.mcp_client is not None:
            try:
                return self.mcp_client.get_user_profile_via_mcp()
            except Exception:
                # Fallback to API
                pass
        return self.api_client.get_user_profile()

    def search_knowledge_graph(
        self, query: str, space_id: Optional[str] = None, limit: int = 10, depth: int = 2
    ) -> Dict[str, Any]:
        return self.api_client.search_knowledge_graph(query, space_id, limit, depth)

    def add_data_to_ingestion_queue(
        self,
        data: Any,
        space_id: Optional[str] = None,
        priority: str = "normal",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.api_client.add_data_to_ingestion_queue(data, space_id, priority, tags, metadata)

    def get_episode_facts(
        self, episode_id: str, limit: int = 100, offset: int = 0, include_metadata: bool = True
    ) -> Dict[str, Any]:
        return self.api_client.get_episode_facts(episode_id, limit, offset, include_metadata)

    def get_ingestion_logs(
        self,
        space_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Any]:
        return self.api_client.get_ingestion_logs(
            space_id, limit, offset, status, start_date, end_date
        )

    def get_specific_log(self, log_id: str) -> Dict[str, Any]:
        return self.api_client.get_specific_log(log_id)

    def check_ingestion_status(
        self, run_id: Optional[str] = None, space_id: Optional[str] = None
    ) -> Dict[str, Any]:
        return self.api_client.check_ingestion_status(run_id, space_id)

    def bulk_space_operations(
        self,
        intent: str,
        space_id: Optional[str] = None,
        statement_ids: Optional[List[str]] = None,
        space_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        return self.api_client.bulk_space_operations(intent, space_id, statement_ids, space_ids)

    def get_space_details(
        self, space_id: str, include_stats: bool = True, include_metadata: bool = True
    ) -> Dict[str, Any]:
        return self.api_client.get_space_details(space_id, include_stats, include_metadata)

    def update_space(
        self,
        space_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.api_client.update_space(space_id, name, description, metadata)

    def delete_space(self, space_id: str, confirm: bool = False) -> Dict[str, Any]:
        return self.api_client.delete_space(space_id, confirm)

    def register_webhook(
        self, url: str, events: Optional[List[str]] = None, secret: str = ""
    ) -> Dict[str, Any]:
        return self.api_client.register_webhook(url, events, secret)

    def list_webhooks(
        self,
        space_id: Optional[str] = None,
        active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Any]:
        return self.api_client.list_webhooks(space_id, active, limit, offset)

    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        return self.api_client.get_webhook(webhook_id)

    def update_webhook(
        self, webhook_id: str, url: str, events: List[str], secret: str = "", active: bool = True
    ) -> Dict[str, Any]:
        return self.api_client.update_webhook(webhook_id, url, events, secret, active)

    def delete_webhook(self, webhook_id: str, confirm: bool = False) -> Dict[str, Any]:
        return self.api_client.delete_webhook(webhook_id, confirm)

    def delete_log_entry(self, log_id: str) -> Dict[str, Any]:
        return self.api_client.delete_log_entry(log_id)

    def copy_log_entry(
        self,
        log_entry: Dict[str, Any],
        new_source: Optional[str] = None,
        new_space_id: Optional[str] = None,
        new_session_id: Optional[str] = None,
        override_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Copy a log entry with all metadata preserved, allowing selective field overrides.

        This method preserves all original metadata fields (timestamps, session IDs, etc.)
        while allowing you to override specific fields like source, space, or session.

        Args:
            log_entry: The original log entry to copy (from get_specific_log or get_ingestion_logs)
            new_source: Optional new source identifier (preserves original if None)
            new_space_id: Optional new space ID (preserves original if None)
            new_session_id: Optional new session ID (preserves original if None)
            override_metadata: Optional metadata fields to override (merges with original)

        Returns:
            The response from the copy operation

        Example:
            # Get a log entry
            log = client.get_specific_log("log-id-123")

            # Copy it with a new source
            copied = client.copy_log_entry(log, new_source="my-new-source")

            # Copy with metadata override
            copied = client.copy_log_entry(log, override_metadata={"priority": "high"})
        """
        return self.api_client.copy_log_entry(
            log_entry=log_entry,
            new_source=new_source,
            new_space_id=new_space_id,
            new_session_id=new_session_id,
            override_metadata=override_metadata,
        )

    def iter_ingestion_logs(
        self,
        space_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Iterator[Any]:
        """Generator that yields ingestion logs for memory-efficient processing.

        Args:
            space_id: Optional space ID to filter logs
            status: Optional status filter
            start_date: Optional start date filter
            end_date: Optional end date filter

        Yields:
            Individual log entries as they are fetched
        """
        return self.api_client.iter_ingestion_logs(
            space_id=space_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )

    def get_logs_by_source(
        self,
        source: str,
        space_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Any]:
        return self.api_client.get_logs_by_source(
            source=source,
            space_id=space_id,
            limit=limit,
            offset=offset,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )

    def move_logs_to_instance(
        self,
        target_client: "HeySolClient",
        source: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 10000,
        confirm: bool = False,
        delete_after_move: bool = True,
        target_source: Optional[str] = None,
        target_space_id: Optional[str] = None,
        target_session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Move logs to target instance (copy + delete)."""
        # First copy the logs
        copy_result = self._transfer_logs_to_instance(
            source_client=self,
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
        logs_result = self.get_logs_by_source(source=source or "*", space_id=space_id, limit=limit)
        logs = logs_result.get("logs", []) if isinstance(logs_result, dict) else logs_result

        deleted_count = 0
        for log in logs:
            try:
                self.delete_log_entry(log["id"])
                deleted_count += 1
            except Exception:
                # Continue with other deletions even if one fails
                continue

        return {
            "operation": "move",
            "transferred_count": copy_result.get("transferred_count", 0),
            "deleted_count": deleted_count,
            "total_attempted": len(logs),
            "source_instance": self.base_url,
            "target_instance": target_client.base_url,
            "message": f"Moved {copy_result.get('transferred_count', 0)} logs",
        }

    @staticmethod
    def _transfer_logs_to_instance(
        source_client: "HeySolClient",
        target_client: "HeySolClient",
        source: str,
        space_id: Optional[str] = None,
        limit: int = 10000,
        confirm: bool = False,
        operation: str = "move",
        delete_after_transfer: bool = True,
        target_source: Optional[str] = None,
        target_space_id: Optional[str] = None,
        target_session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Internal method to transfer logs between instances."""
        # Get logs by source
        logs_result = source_client.get_logs_by_source(
            source=source, space_id=space_id, limit=limit
        )

        logs = logs_result.get("logs", []) if isinstance(logs_result, dict) else logs_result
        total_count = (
            logs_result.get("total_count", len(logs))
            if isinstance(logs_result, dict)
            else len(logs)
        )

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
                payload = {
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

    def close(self) -> None:
        """Close the client and clean up resources."""
        if self.mcp_client:
            self.mcp_client.close()
        self.api_client.close()

    # MCP-specific methods
    def is_mcp_available(self) -> bool:
        """Check if MCP is available and initialized."""
        return self.mcp_available and self.mcp_client is not None

    def get_available_tools(self) -> Dict[str, Any]:
        """Get available MCP tools."""
        if not self.is_mcp_available() or self.mcp_client is None:
            return {}
        return self.mcp_client.get_available_tools()

    def get_tool_names(self) -> List[str]:
        """Get list of available MCP tool names."""
        if not self.is_mcp_available() or self.mcp_client is None:
            return []
        return self.mcp_client.get_tool_names()

    def call_tool(self, tool_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Call an MCP tool directly."""
        if not self.is_mcp_available() or self.mcp_client is None:
            raise HeySolError("MCP is not available")
        return self.mcp_client.call_tool(tool_name, **kwargs)

    def get_preferred_access_method(self, operation: str) -> str:
        """Get the preferred access method for an operation."""
        if self.prefer_mcp and self.is_mcp_available():
            return "mcp"
        return "direct_api"

    def get_session_info(self) -> Dict[str, Any]:
        """Get MCP session information."""
        if not self.is_mcp_available() or self.mcp_client is None:
            return {"mcp_available": False}
        return self.mcp_client.get_session_info()
