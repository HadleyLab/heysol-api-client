#!/usr/bin/env python3
"""
Unit tests for HeySolClient initialization.

Tests client initialization following fail-fast principles.
"""

import pytest
from unittest.mock import Mock, patch

from heysol.client import HeySolClient
from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_client_initialization_with_api_preference():
    """Test client initialization with API preference."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            prefer_mcp=False,
            skip_mcp_init=True
        )

        assert client.prefer_mcp is False
        assert client.mcp_available is False
        assert client.api_client == mock_api_instance
        mock_api.assert_called_once()


def test_client_initialization_with_mcp_preference():
    """Test client initialization with MCP preference."""
    with patch('heysol.client.HeySolAPIClient'), \
         patch('heysol.client.HeySolMCPClient') as mock_mcp:

        mock_mcp_instance = Mock()
        mock_mcp_instance.is_mcp_available.return_value = True
        mock_mcp.return_value = mock_mcp_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            prefer_mcp=True,
            skip_mcp_init=False
        )

        assert client.prefer_mcp is True
        assert client.mcp_available is True
        assert client.mcp_client == mock_mcp_instance


def test_client_initialization_mcp_fallback():
    """Test client initialization with MCP fallback on failure."""
    with patch('heysol.client.HeySolAPIClient'), \
         patch('heysol.client.HeySolMCPClient') as mock_mcp:

        # Simulate MCP initialization failure
        mock_mcp_instance = Mock()
        mock_mcp_instance.is_mcp_available.side_effect = Exception("MCP failed")
        mock_mcp.return_value = mock_mcp_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            skip_mcp_init=False
        )

        # Should fallback gracefully
        assert client.mcp_available is False
        assert client.mcp_client is None


def test_client_initialization_with_config_object():
    """Test client initialization with config object."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://test.com"
    )

    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(config=config, skip_mcp_init=True)

        assert client.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
        assert client.base_url == "https://test.com"
        assert client.api_client == mock_api_instance


def test_client_initialization_empty_api_key():
    """Test client initialization with empty API key."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key="", skip_mcp_init=True)

        assert client.api_key == ""
        assert client.api_client == mock_api_instance


def test_client_initialization_none_api_key():
    """Test client initialization with None API key."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key=None, skip_mcp_init=True)

        assert client.api_key is None
        assert client.api_client == mock_api_instance


def test_client_initialization_with_custom_base_url():
    """Test client initialization with custom base URL."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            base_url="https://custom.api.com/v1",
            skip_mcp_init=True
        )

        assert client.base_url == "https://custom.api.com/v1"
        assert client.api_client == mock_api_instance


def test_client_initialization_with_custom_mcp_url():
    """Test client initialization with custom MCP URL."""
    with patch('heysol.client.HeySolAPIClient'), \
         patch('heysol.client.HeySolMCPClient') as mock_mcp:

        mock_mcp_instance = Mock()
        mock_mcp_instance.is_mcp_available.return_value = True
        mock_mcp.return_value = mock_mcp_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            mcp_url="https://custom.mcp.com/v1",
            skip_mcp_init=False
        )

        assert client.mcp_url == "https://custom.mcp.com/v1"
        assert client.mcp_client == mock_mcp_instance


def test_client_initialization_with_timeout():
    """Test client initialization with custom timeout."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            timeout=60,
            skip_mcp_init=True
        )

        assert client.timeout == 60
        assert client.api_client == mock_api_instance


def test_client_initialization_with_source():
    """Test client initialization with source parameter."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            source="test-source",
            skip_mcp_init=True
        )

        assert client.source == "test-source"
        assert client.api_client == mock_api_instance


def test_client_initialization_preserves_api_key_format():
    """Test client initialization preserves API key format."""
    test_api_key = "rc_pat_test_key_for_testing_12345678901234567890"

    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key=test_api_key, skip_mcp_init=True)

        assert client.api_key == test_api_key


def test_client_initialization_sets_default_timeout():
    """Test client initialization sets default timeout."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", skip_mcp_init=True)

        assert client.timeout == 30  # default timeout


def test_client_initialization_with_session_configuration():
    """Test client initialization configures session properly."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", skip_mcp_init=True)

        # Session should be configured
        assert client.api_client is not None


def test_client_initialization_multiple_instances():
    """Test client initialization creates independent instances."""
    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance1 = Mock()
        mock_api_instance2 = Mock()
        mock_api.side_effect = [mock_api_instance1, mock_api_instance2]

        client1 = HeySolClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", skip_mcp_init=True)
        client2 = HeySolClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", skip_mcp_init=True)

        assert client1.api_client == mock_api_instance1
        assert client2.api_client == mock_api_instance2
        assert client1 is not client2
        assert client1.api_client is not client2.api_client


def test_client_initialization_with_unicode_api_key():
    """Test client initialization with unicode API key."""
    unicode_api_key = "rc_pat_tëst_këy_för_tësting_12345678901234567890"

    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(api_key=unicode_api_key, skip_mcp_init=True)

        assert client.api_key == unicode_api_key


def test_client_initialization_with_special_characters_in_base_url():
    """Test client initialization with special characters in base URL."""
    special_base_url = "https://api.example.com:8080/v1"

    with patch('heysol.client.HeySolAPIClient') as mock_api:
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        client = HeySolClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            base_url=special_base_url,
            skip_mcp_init=True
        )

        assert client.base_url == special_base_url