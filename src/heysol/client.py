from __future__ import annotations

from typing import Any, Dict, Iterator, List, cast

from . import operations
from .clients.api_client import HeySolAPIClient
from .clients.mcp_client import HeySolMCPClient
from .config import HeySolConfig
from .exceptions import HeySolError, ValidationError
from .models.responses import SearchResult


class HeySolClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        mcp_url: str | None = None,
        config: HeySolConfig | None = None,
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
        self.mcp_client: HeySolMCPClient | None = None
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
    def from_env(cls) -> HeySolClient:
        """Create client from environment variables."""
        config = HeySolConfig.from_env()
        return cls(config=config)

    # Core memory operations with MCP fallback
    def ingest(
        self,
        message: str,
        source: str | None = None,
        space_id: str | None = None,
        session_id: str | None = None,
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
        space_ids: List[str] | None = None,
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

    def get_spaces(self) -> List[Dict[str, Any]]:
        """Get spaces with MCP fallback support."""
        if self.mcp_available and self.prefer_mcp and self.mcp_client is not None:
            try:
                result = self.mcp_client.get_spaces_via_mcp()
                # Handle different response formats from MCP
                if isinstance(result, dict) and "spaces" in result:
                    spaces_data = result["spaces"]
                    if isinstance(spaces_data, list):
                        # Convert to expected format
                        return [space for space in spaces_data if isinstance(space, dict)]
                # Handle direct list response
                if isinstance(result, list):  # type: ignore[unreachable]
                    # Convert to expected format
                    return [space for space in result if isinstance(space, dict)]  # type: ignore[unreachable]
            except Exception:
                # Fallback to API
                pass
        return self.api_client.get_spaces()

    def create_space(self, name: str, description: str = "") -> Dict[str, Any]:
        space_id = self.api_client.create_space(name, description)
        return {"space_id": space_id, "name": name, "description": description}

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
        self,
        query: str,
        space_id: str | None = None,
        limit: int = 10,
        depth: int = 2,
    ) -> Dict[str, Any]:
        return self.api_client.search_knowledge_graph(query, space_id, limit, depth)

    def add_data_to_ingestion_queue(
        self,
        data: Any,
        space_id: str | None = None,
        priority: str = "normal",
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return self.api_client.add_data_to_ingestion_queue(data, space_id, priority, tags, metadata)

    def get_episode_facts(
        self,
        episode_id: str,
        limit: int = 100,
        offset: int = 0,
        include_metadata: bool = True,
    ) -> Dict[str, Any]:
        return self.api_client.get_episode_facts(episode_id, limit, offset, include_metadata)

    def get_ingestion_logs(
        self,
        space_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
        status: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Dict[str, Any]:
        logs = self.api_client.get_ingestion_logs(
            space_id, limit, offset, status, start_date, end_date
        )
        return {"logs": logs, "total_count": len(logs)}

    def get_specific_log(self, log_id: str) -> Dict[str, Any]:
        return self.api_client.get_specific_log(log_id)

    def check_ingestion_status(
        self, run_id: str | None = None, space_id: str | None = None
    ) -> Dict[str, Any]:
        return self.api_client.check_ingestion_status(run_id, space_id)

    def bulk_space_operations(
        self,
        intent: str,
        space_id: str | None = None,
        statement_ids: List[str] | None = None,
        space_ids: List[str] | None = None,
    ) -> Dict[str, Any]:
        return self.api_client.bulk_space_operations(intent, space_id, statement_ids, space_ids)

    def get_space_details(
        self, space_id: str, include_stats: bool = True, include_metadata: bool = True
    ) -> Dict[str, Any]:
        return self.api_client.get_space_details(space_id, include_stats, include_metadata)

    def update_space(
        self,
        space_id: str,
        name: str | None = None,
        description: str | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return self.api_client.update_space(space_id, name, description, metadata)

    def delete_space(self, space_id: str, confirm: bool = False) -> Dict[str, Any]:
        return self.api_client.delete_space(space_id, confirm)

    def register_webhook(
        self, url: str, events: List[str] | None = None, secret: str = ""
    ) -> Dict[str, Any]:
        return self.api_client.register_webhook(url, events, secret)

    def list_webhooks(
        self,
        space_id: str | None = None,
        active: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Any]:
        return self.api_client.list_webhooks(space_id, active, limit, offset)

    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        return self.api_client.get_webhook(webhook_id)

    def update_webhook(
        self,
        webhook_id: str,
        url: str,
        events: List[str],
        secret: str = "",
        active: bool = True,
    ) -> Dict[str, Any]:
        return self.api_client.update_webhook(webhook_id, url, events, secret, active)

    def delete_webhook(self, webhook_id: str, confirm: bool = False) -> Dict[str, Any]:
        return self.api_client.delete_webhook(webhook_id, confirm)

    def delete_log_entry(self, log_id: str) -> Dict[str, Any]:
        return self.api_client.delete_log_entry(log_id)

    def copy_log_entry(
        self,
        log_entry: Dict[str, Any],
        new_source: str | None = None,
        new_space_id: str | None = None,
        new_session_id: str | None = None,
        override_metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return self.api_client.copy_log_entry(
            log_entry=log_entry,
            new_source=new_source,
            new_space_id=new_space_id,
            new_session_id=new_session_id,
            override_metadata=override_metadata,
        )

    def iter_ingestion_logs(
        self,
        space_id: str | None = None,
        status: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Iterator[Any]:
        return self.api_client.iter_ingestion_logs(
            space_id=space_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )

    def get_logs_by_source(
        self,
        source: str,
        space_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
        status: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Dict[str, Any]:
        logs = self.api_client.get_logs_by_source(
            source=source,
            space_id=space_id,
            limit=limit,
            offset=offset,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        return {"logs": logs, "total_count": len(logs)}

    def move_logs_to_instance(
        self,
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
        return operations.move_logs_to_instance(
            source_client=self,
            target_client=target_client,
            source=source,
            space_id=space_id,
            limit=limit,
            confirm=confirm,
            delete_after_move=delete_after_move,
            target_source=target_source,
            target_space_id=target_space_id,
            target_session_id=target_session_id,
        )

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
