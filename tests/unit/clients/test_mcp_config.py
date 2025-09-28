"""
Configuration validation tests for HeySol API Client.

Tests configuration validation following fail-fast principles.
"""

from heysol.config import DEFAULT_MCP_URL


def test_mcp_url_configuration():
    """Test that MCP URL is correctly configured."""
    from heysol.config import DEFAULT_SOURCE

    expected_url = f"https://core.heysol.ai/api/v1/mcp?source={DEFAULT_SOURCE}"
    assert DEFAULT_MCP_URL == expected_url


def test_mcp_availability_checks():
    """Test MCP availability checking logic."""
    from heysol.clients.mcp_client import HeySolMCPClient

    client = HeySolMCPClient.__new__(HeySolMCPClient)

    # Test with no session
    client.session_id = None
    client.tools = {}
    assert not client.is_mcp_available()

    # Test with session but no tools
    client.session_id = "session-only"
    client.tools = {}
    assert not client.is_mcp_available()

    # Test with tools but no session
    client.session_id = None
    client.tools = {"test": "tool"}
    assert not client.is_mcp_available()

    # Test with both session and tools
    client.session_id = "full-session"
    client.tools = {"test": "tool"}
    assert client.is_mcp_available()
