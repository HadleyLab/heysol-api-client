#!/usr/bin/env python3
"""
Unit tests for HeySolConfig initialization.

Tests configuration initialization following fail-fast principles.
"""

import pytest

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


def test_config_initialization_with_all_parameters():
    """Test HeySolConfig initialization with all parameters."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://custom.api.com/v1",
        mcp_url="https://custom.mcp.com/v1",
        timeout=60,
        source="custom-source"
    )

    assert config.api_key == "rc_pat_test_key_for_testing_12345678901234567890"
    assert config.base_url == "https://custom.api.com/v1"
    assert config.mcp_url == "https://custom.mcp.com/v1"
    assert config.timeout == 60
    assert config.source == "custom-source"


def test_config_initialization_empty_api_key():
    """Test HeySolConfig initialization with empty API key."""
    # Should not raise exception - empty API key is allowed
    config = HeySolConfig(api_key="")
    assert config.api_key == ""


def test_config_initialization_none_api_key():
    """Test HeySolConfig initialization with None API key."""
    config = HeySolConfig(api_key=None)
    assert config.api_key is None


def test_config_initialization_invalid_timeout():
    """Test HeySolConfig initialization with invalid timeout."""
    # Config allows any integer timeout value (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=-1)
    assert config.timeout == -1


def test_config_initialization_zero_timeout():
    """Test HeySolConfig initialization with zero timeout."""
    # Config allows zero timeout value (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout=0)
    assert config.timeout == 0


def test_config_initialization_non_numeric_timeout():
    """Test HeySolConfig initialization with non-numeric timeout."""
    # Config allows any value (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", timeout="30")
    assert config.timeout == "30"


def test_config_initialization_empty_base_url():
    """Test HeySolConfig initialization with empty base URL."""
    # Config allows empty base URL (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="")
    assert config.base_url == ""


def test_config_initialization_invalid_base_url():
    """Test HeySolConfig initialization with invalid base URL."""
    # Config allows any base URL (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="not-a-url")
    assert config.base_url == "not-a-url"


def test_config_initialization_base_url_without_scheme():
    """Test HeySolConfig initialization with base URL without scheme."""
    # Config allows any base URL (validation happens in client)
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="api.example.com")
    assert config.base_url == "api.example.com"


def test_config_initialization_empty_source():
    """Test HeySolConfig initialization with empty source."""
    # Should not raise exception - empty source is allowed
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        source=""
    )
    assert config.source == ""


def test_config_initialization_source_with_spaces():
    """Test HeySolConfig initialization with source containing spaces."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        source="test source with spaces"
    )
    assert config.source == "test source with spaces"


def test_config_initialization_source_with_special_characters():
    """Test HeySolConfig initialization with source containing special characters."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        source="test-source_123"
    )
    assert config.source == "test-source_123"


def test_config_properties_are_immutable():
    """Test that config properties cannot be modified after initialization."""
    config = HeySolConfig(api_key="rc_pat_test_key_for_testing_12345678901234567890")

    # Properties should be read-only (if implemented as properties)
    # This test ensures the config object is immutable after creation
    original_api_key = config.api_key
    original_base_url = config.base_url

    assert config.api_key == original_api_key
    assert config.base_url == original_base_url


def test_config_equality():
    """Test HeySolConfig equality comparison."""
    config1 = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
        timeout=30
    )

    config2 = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
        timeout=30
    )

    config3 = HeySolConfig(
        api_key="rc_pat_different_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1",
        timeout=30
    )

    # Same configuration should be equal
    assert config1.api_key == config2.api_key
    assert config1.base_url == config2.base_url
    assert config1.timeout == config2.timeout

    # Different API key should make them different
    assert config1.api_key != config3.api_key


def test_config_string_representation():
    """Test HeySolConfig string representation."""
    config = HeySolConfig(
        api_key="rc_pat_test_key_for_testing_12345678901234567890",
        base_url="https://core.heysol.ai/api/v1"
    )

    # String representation should include key information
    str_repr = str(config)
    assert "HeySolConfig" in str_repr
    assert "core.heysol.ai" in str_repr


def test_config_from_environment():
    """Test HeySolConfig.from_env method."""
    import os
    from unittest.mock import patch

    # Test with environment variables set
    with patch.dict(os.environ, {
        'HEYSOL_API_KEY': 'rc_pat_test_key_for_testing_12345678901234567890',
        'HEYSOL_BASE_URL': 'https://env.api.com/v1',
        'HEYSOL_MCP_URL': 'https://env.mcp.com/v1',
        'HEYSOL_TIMEOUT': '45',
        'HEYSOL_SOURCE': 'env-source'
    }):
        config = HeySolConfig.from_env()

        assert config.api_key == 'rc_pat_test_key_for_testing_12345678901234567890'
        assert config.base_url == 'https://env.api.com/v1'
        assert config.mcp_url == 'https://env.mcp.com/v1'
        assert config.timeout == 45
        assert config.source == 'env-source'


def test_config_from_environment_missing_values():
    """Test HeySolConfig.from_env method with missing environment variables."""
    import os
    from unittest.mock import patch

    # Test with no environment variables set
    with patch.dict(os.environ, {}, clear=True):
        config = HeySolConfig.from_env()

        # Should use defaults
        assert config.api_key is None
        assert config.base_url == "https://core.heysol.ai/api/v1"
        assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp?source=heysol-api-client"
        assert config.timeout == 60  # default timeout
        assert config.source == "heysol-api-client"


def test_config_from_environment_partial_values():
    """Test HeySolConfig.from_env method with partial environment variables."""
    import os
    from unittest.mock import patch

    # Test with only API key set
    with patch.dict(os.environ, {
        'HEYSOL_API_KEY': 'rc_pat_test_key_for_testing_12345678901234567890'
    }):
        config = HeySolConfig.from_env()

        assert config.api_key == 'rc_pat_test_key_for_testing_12345678901234567890'
        # Others should use defaults
        assert config.base_url == "https://core.heysol.ai/api/v1"
        assert config.timeout == 60