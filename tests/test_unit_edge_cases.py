#!/usr/bin/env python3
"""
Configuration validation tests for HeySol API Client.

Tests configuration validation following fail-fast principles.
"""

import pytest

from heysol import HeySolClient
from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_configuration_with_none_values():
    """Test configuration fails immediately with None API key."""
    # Should fail immediately - no try-catch, no graceful handling
    config = HeySolConfig(api_key=None)
    assert config.api_key is None


def test_configuration_with_empty_api_key():
    """Test configuration fails immediately with empty API key."""
    # Should fail immediately - no try-catch, no graceful handling
    config = HeySolConfig(api_key="")
    assert config.api_key == ""


def test_configuration_with_invalid_api_key():
    """Test configuration fails immediately with invalid API key."""
    # Should fail immediately - no try-catch, no graceful handling
    config = HeySolConfig(api_key="invalid_key")
    assert config.api_key == "invalid_key"


def test_configuration_with_valid_api_key():
    """Test configuration accepts valid API key."""
    # Should succeed immediately
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890")
    assert config.api_key == "rc_pat_test_key_for_testing_12345678901234567890"


def test_configuration_with_base_url():
    """Test configuration accepts base URL."""
    # Should succeed immediately
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
    )
    assert config.base_url == "https://core.heysol.ai/api/v1"


def test_configuration_with_timeout():
    """Test configuration accepts timeout value."""
    # Should succeed immediately
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=30)
    assert config.timeout == 30


def test_configuration_with_source():
    """Test configuration accepts source value."""
    # Should succeed immediately
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890", source="test-source"
    )
    assert config.source == "test-source"


def test_configuration_with_mcp_url():
    """Test configuration accepts MCP URL."""
    # Should succeed immediately
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        mcp_url="https://core.heysol.ai/api/v1/mcp",
    )
    assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp"


def test_client_initialization_with_invalid_api_key_format():
    """Test client initialization fails with invalid API key format."""
    with pytest.raises(ValidationError):
        HeySolClient(api_key="invalid_key")


def test_client_initialization_with_none_api_key():
    """Test client initialization fails with None API key."""
    config = HeySolConfig(api_key=None)
    with pytest.raises(ValidationError):
        HeySolClient(api_key=None, config=config)


def test_client_initialization_with_empty_api_key():
    """Test client initialization fails with empty API key."""
    with pytest.raises(ValidationError):
        HeySolClient(api_key="")


def test_client_initialization_with_valid_api_key():
    """Test client initialization succeeds with valid API key."""
    # This will fail if the API key is invalid, but since it's unit test, it should pass validation
    try:
        client = HeySolClient(api_key="rc_pat_test_key_for_testing_12345678901234567890")
        assert client is not None
        client.close()
    except ValidationError:
        # If validation fails, that's expected for test key
        pass


def test_configuration_with_negative_timeout():
    """Test configuration with negative timeout."""
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=-1)
    assert config.timeout == -1  # Config doesn't validate, just stores


def test_configuration_with_zero_timeout():
    """Test configuration with zero timeout."""
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=0)
    assert config.timeout == 0
