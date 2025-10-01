"""
HeySol MCP Client - Model Context Protocol operations.

This module provides an MCP (Model Context Protocol) client for JSON-RPC based
interactions with HeySol services. MCP provides tool discovery, session management,
and enhanced protocol features.
"""

import json
import uuid
from typing import Any, Dict, List, Optional, cast

import requests

from ..config import HeySolConfig
from ..exceptions import HeySolError, ValidationError, validate_api_key_format


class HeySolMCPClient:
    """
    MCP (Model Context Protocol) client for HeySol services.

    This client handles JSON-RPC protocol interactions, tool discovery,
    and session management. Use this when you need dynamic tool access,
    session-based operations, or enhanced protocol features.

    Key differences from API client:
    - JSON-RPC protocol instead of REST
    - Tool discovery and dynamic method calling
    - Session management with initialization
    - SSE (Server-Sent Events) support for streaming
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        mcp_url: Optional[str] = None,
        config: Optional[HeySolConfig] = None,
    ):
        """
        Initialize the HeySol MCP client.

        Args:
            api_key: HeySol API key (required for authentication)
            mcp_url: MCP endpoint URL (optional, uses config default if not provided)
            config: HeySolConfig object (optional, overrides individual parameters)
        """
        # Use provided config or load from environment
        if config is None:
            config = HeySolConfig.from_env()

        # Use provided values or fall back to config
        if api_key is None:
            api_key = config.api_key
        if not mcp_url:
            mcp_url = config.mcp_url

        # Validate authentication
        if not api_key:
            raise ValidationError("API key is required")

        # Validate API key format and legitimacy
        validate_api_key_format(api_key)
        self._validate_api_key(api_key, mcp_url)

        self.api_key = api_key
        self.mcp_url = mcp_url
        self.source = config.source
        self.timeout = config.timeout
        self.session_id: Optional[str] = None
        self.tools: Dict[str, Any] = {}

        # Initialize MCP session
        self._initialize_session()

    @classmethod
    def from_env(cls) -> "HeySolMCPClient":
        """
        Create MCP client from environment variables.

        Returns:
            HeySolMCPClient: Configured MCP client instance
        """
        config = HeySolConfig.from_env()
        return cls(config=config)

    def _validate_api_key(self, api_key: str, mcp_url: str) -> None:
        """
        Validate API key by making a test MCP call.

        Args:
            api_key: The API key to validate
            mcp_url: The MCP URL for API calls

        Raises:
            ValidationError: If the API key is invalid or authentication fails
        """

        try:
            # Make a test MCP request (initialize without full session setup)
            test_payload = {
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4()),
                "method": "initialize",
                "params": {
                    "protocolVersion": "1.0.0",
                    "capabilities": {"tools": True},
                    "clientInfo": {"name": "heysol-mcp-client", "version": "1.0.0"},
                },
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream, */*",
                "Authorization": f"Bearer {api_key}",
            }

            response = requests.post(
                url=mcp_url,
                json=test_payload,
                headers=headers,
                timeout=10,  # Short timeout for validation
            )

            # Check for authentication errors
            if response.status_code == 401:
                raise ValidationError("Invalid API key or authentication failed")
            elif response.status_code == 403:
                raise ValidationError("API key does not have required permissions")
            elif response.status_code >= 400:
                # For other client errors, assume key is invalid
                # Add debug logging
                print(f"DEBUG: MCP validation failed - Status: {response.status_code}")
                print(f"DEBUG: Response headers: {dict(response.headers)}")
                try:
                    print(f"DEBUG: Response content: {response.text[:500]}")
                except Exception:
                    print("DEBUG: Could not read response content")
                raise ValidationError(f"API key validation failed: HTTP {response.status_code}")

            # If we get here, check the JSON response for errors
            response.raise_for_status()

            # Parse the response to check for JSON-RPC errors
            try:
                msg = response.json()
                if "error" in msg:
                    raise ValidationError(f"MCP protocol error: {msg['error']}")
            except ValueError:
                # If not JSON, assume it's valid (server might return different format)
                pass

        except requests.exceptions.RequestException as e:
            if "401" in str(e) or "403" in str(e):
                raise ValidationError("Invalid API key or authentication failed") from e
            else:
                # For network/other errors, we'll allow the key for now
                # The actual MCP calls will fail later if the key is truly invalid
                print(f"DEBUG: Network error during MCP validation: {e}")
                pass

    def _get_authorization_header(self) -> str:
        """Get the authorization header using API key."""
        if not self.api_key:
            raise HeySolError("No API key available for authentication")
        return f"Bearer {self.api_key}"

    def _get_mcp_headers(self) -> Dict[str, str]:
        """Get MCP-specific headers."""
        headers = {
            "Authorization": self._get_authorization_header(),
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream, */*",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        return headers

    def _parse_mcp_response(self, response: requests.Response) -> Any:
        """Parse MCP JSON-RPC response."""
        content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip()

        if content_type == "application/json":
            msg = response.json()
        elif content_type == "text/event-stream":
            msg = None
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data:"):
                    msg = json.loads(line[5:].strip())
                    break
            if msg is None:
                raise HeySolError("No JSON in SSE stream")
        else:
            raise HeySolError(f"Unexpected Content-Type: {content_type}")

        if isinstance(msg, dict) and "error" in msg:
            raise HeySolError(f"MCP error: {msg['error']}")

        if isinstance(msg, dict):
            return msg.get("result", msg)
        return msg

    def _mcp_request(
        self, method: str, params: Optional[Dict[str, Any]] = None, stream: bool = False
    ) -> Any:
        """Make an MCP JSON-RPC request."""
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params or {},
        }

        response = requests.post(
            self.mcp_url,
            json=payload,
            headers=self._get_mcp_headers(),
            timeout=self.timeout,
            stream=stream,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise HeySolError(f"HTTP error: {response.status_code} - {response.text}")

        return self._parse_mcp_response(response)

    def _initialize_session(self) -> None:
        """Initialize MCP session and discover available tools."""
        # Initialize session
        init_payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0.0",
                "capabilities": {"tools": True},
                "clientInfo": {"name": "heysol-mcp-client", "version": "1.0.0"},
            },
        }

        try:
            response = requests.post(
                self.mcp_url,
                json=init_payload,
                headers=self._get_mcp_headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = self._parse_mcp_response(response)
            self.session_id = response.headers.get("Mcp-Session-Id") or self.session_id
        except Exception as e:
            raise HeySolError(f"Failed to initialize MCP session: {e}")

        # List available tools
        tools_payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/list",
            "params": {},
        }

        response = requests.post(
            self.mcp_url, json=tools_payload, headers=self._get_mcp_headers(), timeout=self.timeout
        )
        response.raise_for_status()
        result = self._parse_mcp_response(response)
        self.tools = {t["name"]: t for t in result.get("tools", [])}

    def is_mcp_available(self) -> bool:
        """Check if MCP is available and initialized."""
        return bool(self.session_id and self.tools)

    def ensure_mcp_available(self, tool_name: Optional[str] = None) -> None:
        """Ensure MCP is available and optionally check for specific tool."""
        if not self.is_mcp_available():
            raise HeySolError("MCP is not available. Please check your MCP configuration.")

        if tool_name and tool_name not in self.tools:
            raise HeySolError(
                f"MCP tool '{tool_name}' is not available. Available tools: {list(self.tools.keys())}"
            )

    def get_available_tools(self) -> Dict[str, Any]:
        """Get information about available MCP tools."""
        return self.tools.copy()

    def get_tool_names(self) -> List[str]:
        """Return a sorted list of available MCP tool names."""
        return sorted(self.tools.keys())

    def call_tool(self, tool_name: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Call an MCP tool dynamically.

        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        self.ensure_mcp_available(tool_name)

        # Use tools/call method for dynamic tool invocation
        params = {"name": tool_name, "arguments": kwargs}

        return cast(Dict[str, Any], self._mcp_request("tools/call", params))

    # Memory operations via MCP tools
    def ingest_via_mcp(
        self,
        message: str,
        source: Optional[str] = None,
        space_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Ingest data using MCP memory_ingest tool."""
        params = {"message": message}
        if source:
            params["source"] = source
        if space_id:
            params["space_id"] = space_id
        if session_id:
            params["session_id"] = session_id

        return self.call_tool("memory_ingest", **params)

    def search_via_mcp(
        self,
        query: str,
        space_ids: Optional[List[str]] = None,
        limit: int = 10,
        valid_at: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search memories using MCP memory_search tool."""
        params: Dict[str, Any] = {"query": query}
        if space_ids:
            params["spaceIds"] = space_ids
        if limit:
            params["limit"] = limit
        if valid_at:
            params["validAt"] = valid_at
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        return self.call_tool("memory_search", **params)

    def get_spaces_via_mcp(self) -> Dict[str, Any]:
        """Get spaces using MCP (if available)."""
        # Note: This might not have a direct MCP equivalent
        # Could use memory_search with specific parameters
        try:
            return self.call_tool("get_spaces")
        except HeySolError:
            raise HeySolError("get_spaces tool not available via MCP")

    def ingest(
        self,
        message: str,
        space_id: Optional[str] = None,
        source: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ingest data using MCP protocol.

        Args:
            message: Content to ingest
            space_id: Target space ID for ingestion
            source: Source identifier for the data
            session_id: Session ID for tracking

        Returns:
            Ingestion result with run ID and metadata
        """
        return self.ingest_via_mcp(
            message=message,
            space_id=space_id,
            source=source,
            session_id=session_id,
        )

    def search(
        self,
        query: str,
        space_ids: Optional[List[str]] = None,
        limit: int = 10,
        valid_at: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search memories using MCP protocol.

        Args:
            query: Search query string
            space_ids: List of space IDs to search in
            limit: Maximum number of results to return
            valid_at: Point-in-time reference for temporal queries
            start_time: Start time for time-bounded searches
            end_time: End time for time-bounded searches

        Returns:
            Search results with episodes and metadata
        """
        return self.search_via_mcp(
            query=query,
            space_ids=space_ids,
            limit=limit,
            valid_at=valid_at,
            start_time=start_time,
            end_time=end_time,
        )

    def get_spaces(self) -> List[Dict[str, Any]]:
        """
        Get available memory spaces using MCP protocol.

        Returns:
            List of space information dictionaries
        """
        try:
            result = self.get_spaces_via_mcp()
            # Handle different response formats
            if isinstance(result, dict):
                spaces = result.get("spaces", [])
                if isinstance(spaces, list):
                    return spaces
                # Try to get spaces from different response structure
                data = result.get("data", [])
                if isinstance(data, list):
                    return data
            elif isinstance(result, list):
                return result
            return []
        except HeySolError:
            # Fallback: try to get spaces via memory_get_spaces tool
            try:
                result = self.get_memory_spaces_via_mcp()
                if isinstance(result, dict):
                    # Handle MCP response format: content[0].text contains JSON string
                    content = result.get("content", [])
                    if isinstance(content, list) and len(content) > 0:
                        item = content[0]
                        if isinstance(item, dict):
                            text_content = item.get("text", "")
                            if text_content:
                                try:
                                    # Parse the JSON string in the text field
                                    parsed = json.loads(text_content)
                                    if isinstance(parsed, list):
                                        return parsed
                                except json.JSONDecodeError:
                                    pass
                    # Fallback to direct spaces field
                    spaces = result.get("spaces", [])
                    if isinstance(spaces, list):
                        return spaces
                return []
            except HeySolError:
                raise HeySolError("Unable to retrieve spaces via MCP")

    # Advanced MCP-only operations
    def delete_logs_by_source(
        self, source: str, space_id: Optional[str] = None, confirm: bool = False
    ) -> Dict[str, Any]:
        """Delete all logs with a specific source using MCP."""
        if not source:
            raise ValidationError("Source is required")

        if not confirm:
            raise ValidationError("Log deletion by source requires confirmation (confirm=True)")

        # First, search for logs with the specified source
        search_params = {
            "query": "*",  # Search all logs
            "spaceIds": [space_id] if space_id else [],
            "includeInvalidated": False,
        }

        try:
            # Use MCP search to find logs with the specified source
            search_result = self.call_tool("memory_search", **search_params)

            # Filter logs by source
            logs_to_delete = []
            if isinstance(search_result, dict) and "episodes" in search_result:
                for episode in search_result["episodes"]:
                    if episode.get("source") == source:
                        logs_to_delete.append(episode)

            if not logs_to_delete:
                return {"message": f"No logs found with source '{source}'", "deleted_count": 0}

            # Delete each log
            deleted_count = 0
            errors = []

            for log in logs_to_delete:
                try:
                    # Use MCP to delete the log
                    delete_params = {"id": log.get("id")}
                    self.call_tool("memory_delete", **delete_params)
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"Failed to delete log {log.get('id')}: {e}")

            return {
                "message": f"Deleted {deleted_count} logs with source '{source}'",
                "deleted_count": deleted_count,
                "total_found": len(logs_to_delete),
                "errors": errors,
            }

        except Exception as e:
            raise HeySolError(f"Failed to delete logs by source: {e}")

    def get_logs_by_source(
        self, source: str, space_id: Optional[str] = None, limit: int = 100
    ) -> Dict[str, Any]:
        """Get all logs with a specific source."""
        if not source:
            raise ValidationError("Source is required")

        # Use MCP search to find logs with the specified source
        search_params = {
            "query": "*",  # Search all logs
            "spaceIds": [space_id] if space_id else [],
            "includeInvalidated": False,
        }

        search_result = self.call_tool("memory_search", **search_params)

        # Filter logs by source
        filtered_logs = []
        if isinstance(search_result, dict) and "episodes" in search_result:
            for episode in search_result["episodes"]:
                if episode.get("source") == source:
                    filtered_logs.append(episode)

        return {
            "logs": filtered_logs[:limit],
            "total_count": len(filtered_logs),
            "source": source,
            "space_id": space_id,
        }

    def get_user_profile_via_mcp(self) -> Dict[str, Any]:
        """Get user profile using MCP (if available)."""
        try:
            return self.call_tool("get_user_profile")
        except HeySolError:
            raise HeySolError("get_user_profile tool not available via MCP")

    def get_memory_spaces_via_mcp(self) -> Dict[str, Any]:
        """Get memory spaces using MCP (if available)."""
        try:
            return self.call_tool("memory_get_spaces")
        except HeySolError:
            raise HeySolError("memory_get_spaces tool not available via MCP")

    # GitHub operations (if MCP server provides them)
    def github_list_notifications(self, **kwargs: Any) -> Dict[str, Any]:
        """List GitHub notifications via MCP."""
        return self.call_tool("github_list_notifications", **kwargs)

    def github_create_issue(self, **kwargs: Any) -> Dict[str, Any]:
        """Create GitHub issue via MCP."""
        return self.call_tool("github_create_issue", **kwargs)

    def github_search_repositories(self, **kwargs: Any) -> Dict[str, Any]:
        """Search GitHub repositories via MCP."""
        return self.call_tool("github_search_repositories", **kwargs)

    # Session management
    def get_session_info(self) -> Dict[str, Any]:
        """Get current MCP session information."""
        return {
            "session_id": self.session_id,
            "mcp_url": self.mcp_url,
            "tools_count": len(self.tools),
            "available_tools": list(self.tools.keys()),
            "is_available": self.is_mcp_available(),
        }

    def refresh_tools(self) -> None:
        """Refresh the list of available MCP tools."""
        tools_payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/list",
            "params": {},
        }

        response = requests.post(
            self.mcp_url, json=tools_payload, headers=self._get_mcp_headers(), timeout=self.timeout
        )
        response.raise_for_status()
        result = self._parse_mcp_response(response)
        self.tools = {t["name"]: t for t in result.get("tools", [])}

    def close(self) -> None:
        """Close the MCP client and clean up resources."""
        # Currently no resources to clean up, but method provided for API compatibility
        pass
