#!/usr/bin/env python3
"""
Unit Tests for HeySolMCPClient class

Following coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add the src directory to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from heysol.clients.mcp_client import HeySolMCPClient
from heysol.exceptions import HeySolError

# Use a properly formatted test API key (50+ characters to pass validation)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef1234567890ab"


class TestHeySolMCPClient:
    """Unit tests for HeySolMCPClient class."""

    def test_mcp_client_initialization_success(self):
        """Test MCP client initialization with successful session."""
        with patch("heysol.clients.mcp_client.requests.post") as mock_post:
            # Mock successful initialization response
            init_response = Mock()
            init_response.status_code = 200
            init_response.raise_for_status.return_value = None
            init_response.json.return_value = {"result": {"capabilities": {}}}
            init_response.headers = {"Mcp-Session-Id": "session-123"}
            init_response.headers.get.return_value = "application/json"

            # Mock successful tools list response
            tools_response = Mock()
            tools_response.status_code = 200
            tools_response.raise_for_status.return_value = None
            tools_response.json.return_value = {"tools": [{"name": "test_tool"}]}

            mock_post.side_effect = [init_response, tools_response]

            with patch("heysol.clients.mcp_client.HeySolConfig") as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                assert client.session_id == "session-123"
                assert "test_tool" in client.tools
                assert client.is_mcp_available() is True

    def test_mcp_client_initialization_failure(self):
        """Test MCP client initialization with failure."""
        with patch("heysol.clients.mcp_client.requests.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception("Server error")
            mock_post.return_value = mock_response

            with patch("heysol.clients.mcp_client.HeySolConfig") as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                with pytest.raises(HeySolError, match="Failed to initialize MCP session"):
                    HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

    def test_call_tool_mcp_unavailable(self):
        """Test tool call when MCP is unavailable."""
        with patch("heysol.clients.mcp_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

            # Mock MCP as unavailable
            client.session_id = None
            client.tools = {}

            with pytest.raises(HeySolError, match="MCP is not available"):
                client.call_tool("test_tool")


if __name__ == "__main__":
    pytest.main([__file__])
