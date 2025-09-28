#!/usr/bin/env python3
"""
Unit Tests for HeySolClient class

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

from heysol.client import HeySolClient

# Use a properly formatted test API key (50+ characters to pass validation)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef1234567890ab"


class TestHeySolClient:
    """Unit tests for HeySolClient class."""

    def test_client_initialization_with_mcp_preference(self):
        """Test client initialization with MCP preference."""
        with patch("heysol.client.HeySolAPIClient"), patch(
            "heysol.client.HeySolMCPClient"
        ) as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(api_key=TEST_API_KEY, prefer_mcp=True, skip_mcp_init=False)

            assert client.prefer_mcp is True
            assert client.mcp_available is True

    def test_client_initialization_mcp_fallback(self):
        """Test client initialization with MCP fallback on failure."""
        with patch("heysol.client.HeySolAPIClient"), patch(
            "heysol.client.HeySolMCPClient"
        ) as mock_mcp:

            # Simulate MCP initialization failure
            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(api_key=TEST_API_KEY, skip_mcp_init=False)

            # Should fallback gracefully
            assert client.mcp_available is False
            assert client.mcp_client is None

    def test_preferred_access_method(self):
        """Test get_preferred_access_method functionality."""
        with patch("heysol.client.HeySolAPIClient"), patch(
            "heysol.client.HeySolMCPClient"
        ) as mock_mcp:

            # Test with MCP preferred and available
            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(api_key=TEST_API_KEY, prefer_mcp=True, skip_mcp_init=False)

            method = client.get_preferred_access_method("ingest")
            assert method == "mcp"

            # Test with MCP not available
            mock_mcp_instance.is_mcp_available.return_value = False
            method = client.get_preferred_access_method("ingest")
            assert method == "direct_api"

    def test_client_close(self):
        """Test client close method."""
        with patch("heysol.client.HeySolAPIClient") as mock_api, patch(
            "heysol.client.HeySolMCPClient"
        ) as mock_mcp:

            mock_api_instance = Mock()
            mock_mcp_instance = Mock()
            mock_api.return_value = mock_api_instance
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(api_key=TEST_API_KEY, skip_mcp_init=False)

            # Should not raise exception
            client.close()

            mock_mcp_instance.close.assert_called_once()
            mock_api_instance.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
