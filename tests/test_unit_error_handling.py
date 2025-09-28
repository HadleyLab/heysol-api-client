#!/usr/bin/env python3
"""
Configuration validation tests for HeySol API Client.

Tests configuration validation following fail-fast principles.
"""

from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_validation_error_initialization():
    """Test ValidationError initialization fails immediately."""
    error_message = "Test validation error"
    validation_error = ValidationError(error_message)

    assert str(validation_error) == error_message
    assert validation_error.args[0] == error_message


def test_heysol_error_initialization():
    """Test HeySolError initialization fails immediately."""
    from heysol.exceptions import HeySolError

    error_message = "Test HeySol error"
    heysol_error = HeySolError(error_message)

    assert str(heysol_error) == error_message
    assert heysol_error.args[0] == error_message


def test_config_initialization_with_valid_values():
    """Test HeySolConfig initialization with valid string values."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
        mcp_url="https://core.heysol.ai/api/v1/mcp",
    )

    assert config.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
    assert config.base_url == "https://core.heysol.ai/api/v1"
    assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp"


def test_config_initialization_with_timeout():
    """Test HeySolConfig initialization with timeout value."""
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=30)

    assert config.timeout == 30


def test_config_initialization_with_source():
    """Test HeySolConfig initialization with source value."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890", source="test-source"
    )

    assert config.source == "test-source"


def test_exception_inheritance():
    """Test exception class inheritance."""
    from heysol.exceptions import HeySolError

    assert issubclass(ValidationError, Exception)
    assert issubclass(HeySolError, Exception)


def test_exception_error_messages():
    """Test exception error message formatting."""
    validation_error = ValidationError("Test message")
    assert str(validation_error) == "Test message"

    from heysol.exceptions import HeySolError

    heysol_error = HeySolError("Another test message")
    assert str(heysol_error) == "Another test message"


def test_multiple_validation_errors():
    """Test that multiple validation errors can be created."""
    error1 = ValidationError("Error 1")
    error2 = ValidationError("Error 2")
    error3 = ValidationError("Error 3")

    assert str(error1) == "Error 1"
    assert str(error2) == "Error 2"
    assert str(error3) == "Error 3"


def test_config_initialization_edge_cases():
    """Test HeySolConfig initialization edge cases."""
    long_url = "https://example.com/" + "x" * 1000
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url=long_url,
        mcp_url=long_url,
    )

    assert config.base_url == long_url
    assert config.mcp_url == long_url
