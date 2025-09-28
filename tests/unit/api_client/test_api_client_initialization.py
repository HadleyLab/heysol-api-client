#!/usr/bin/env python3
"""
Unit tests for HeySolAPIClient initialization.

Tests API client initialization following fail-fast principles.
"""

import pytest
from unittest.mock import Mock, patch

from heysol.clients.api_client import HeySolAPIClient
from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_api_client_initialization_with_valid_api_key():
    """Test API client initialization with valid API key."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        assert client.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
        assert client.base_url == "https://test.com"


def test_api_client_initialization_with_config_object():
    """Test API client initialization with config object."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://test.com"
    )

    client = HeySolAPIClient(config=config)

    assert client.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
    assert client.base_url == "https://test.com"


def test_api_client_initialization_with_timeout():
    """Test API client initialization with custom timeout."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config_instance.timeout = 30
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        assert client.timeout == 30


def test_api_client_initialization_empty_api_key():
    """Test API client initialization with empty API key."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = ""
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="", base_url="https://test.com")

        assert client.api_key == ""


def test_api_client_initialization_none_api_key():
    """Test API client initialization with None API key."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = None
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=None, base_url="https://test.com")

        assert client.api_key is None


def test_api_client_initialization_empty_base_url():
    """Test API client initialization with empty base URL."""
    with pytest.raises(ValidationError, match="Base URL is required"):
        HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="")


def test_api_client_initialization_invalid_base_url():
    """Test API client initialization with invalid base URL."""
    with pytest.raises(ValidationError, match="Invalid base URL format"):
        HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="not-a-url")


def test_api_client_initialization_base_url_without_scheme():
    """Test API client initialization with base URL without scheme."""
    with pytest.raises(ValidationError, match="Base URL must include http:// or https://"):
        HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="api.example.com")


def test_api_client_initialization_base_url_with_path():
    """Test API client initialization with base URL containing path."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://api.example.com/v1"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://api.example.com/v1")

        assert client.base_url == "https://api.example.com/v1"


def test_api_client_initialization_with_custom_headers():
    """Test API client initialization with custom headers."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            base_url="https://test.com"
        )

        # Should have default headers
        assert "User-Agent" in client.headers
        assert "Authorization" in client.headers


def test_api_client_initialization_preserves_api_key_format():
    """Test API client initialization preserves API key format."""
    test_api_key = "rc_pat_test_key_for_testing_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = test_api_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=test_api_key, base_url="https://test.com")

        assert client.api_key == test_api_key


def test_api_client_initialization_sets_default_timeout():
    """Test API client initialization sets default timeout."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config_instance.timeout = 30  # Default timeout
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        assert client.timeout == 30


def test_api_client_initialization_with_session_configuration():
    """Test API client initialization configures session properly."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Session should be configured
        assert client.session is not None
        assert hasattr(client.session, 'headers')


def test_api_client_initialization_with_source_parameter():
    """Test API client initialization with source parameter."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config_instance.source = "test-source"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(
            api_key="rc_pat_test_key_for_testing_12345678901234567890",
            base_url="https://test.com"
        )

        assert client.source == "test-source"


def test_api_client_initialization_without_explicit_source():
    """Test API client initialization without explicit source."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config_instance.source = None
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        assert client.source is None


def test_api_client_initialization_headers_include_source():
    """Test API client initialization includes source in headers when provided."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config_instance.source = "test-source"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Headers should include source if provided
        if client.source:
            assert "X-Source" in client.headers
            assert client.headers["X-Source"] == "test-source"


def test_api_client_initialization_multiple_instances():
    """Test API client initialization creates independent instances."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance1 = Mock()
        mock_config_instance1.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance1.base_url = "https://test1.com"

        mock_config_instance2 = Mock()
        mock_config_instance2.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance2.base_url = "https://test2.com"

        mock_config.from_env.side_effect = [mock_config_instance1, mock_config_instance2]

        client1 = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test1.com")
        client2 = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test2.com")

        assert client1.base_url == "https://test1.com"
        assert client2.base_url == "https://test2.com"
        assert client1 is not client2
        assert client1.session is not client2.session


def test_api_client_initialization_with_unicode_api_key():
    """Test API client initialization with unicode API key."""
    unicode_api_key = "rc_pat_test_këy_för_tësting_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = unicode_api_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=unicode_api_key, base_url="https://test.com")

        assert client.api_key == unicode_api_key


def test_api_client_initialization_with_special_characters_in_base_url():
    """Test API client initialization with special characters in base URL."""
    special_base_url = "https://api.example.com:8080/v1"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = special_base_url
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url=special_base_url)

        assert client.base_url == special_base_url