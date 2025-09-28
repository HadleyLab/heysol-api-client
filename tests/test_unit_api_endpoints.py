#!/usr/bin/env python3
"""
Configuration validation tests for HeySol API Client.

Tests configuration validation following fail-fast principles.
"""

from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_config_initialization():
    """Test HeySolConfig initialization with valid values."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
        mcp_url="https://core.heysol.ai/api/v1/mcp",
    )

    assert config.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
    assert config.base_url == "https://core.heysol.ai/api/v1"
    assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp"


def test_config_initialization_defaults():
    """Test HeySolConfig initialization with default values."""
    config = HeySolConfig()

    assert config.api_key is None
    assert config.base_url == "https://core.heysol.ai/api/v1"
    assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp?source=heysol-api-client"


def test_config_initialization_with_timeout():
    """Test HeySolConfig initialization with timeout."""
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=30)

    assert config.timeout == 30


def test_config_initialization_with_source():
    """Test HeySolConfig initialization with source."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890", source="test-source"
    )

    assert config.source == "test-source"


def test_exception_types():
    """Test that expected exception types are available."""
    from heysol.exceptions import HeySolError

    assert ValidationError is not None
    assert issubclass(ValidationError, Exception)
    assert HeySolError is not None
    assert issubclass(HeySolError, Exception)
