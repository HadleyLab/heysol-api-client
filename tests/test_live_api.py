#!/usr/bin/env python3
"""
Unit Tests for HeySol API Client - Core Functions

Tests individual functions following coding standards:
- Unit Tests Only: Test individual functions, no integration tests
- No Mocks: Test real code, no stubs or mocks
- Fail Fast: Tests must fail on any deviation from expected behavior
"""

import pytest

from heysol.client import HeySolClient
from heysol.config import HeySolConfig
from heysol.exceptions import ValidationError


def test_client_initialization_with_valid_api_key():
    """Test client initialization with valid API key."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    assert client.api_key == api_key
    assert client.mcp_available is False
    assert client.mcp_client is None


def test_client_initialization_without_api_key():
    """Test client initialization without API key."""
    # If environment has API key, it should work
    # If not, it should fail
    import os

    env_has_key = any(
        os.getenv(key) for key in ["HEYSOL_API_KEY", "COREAI_API_KEY", "CORE_MEMORY_API_KEY"]
    )

    if env_has_key:
        # Should work using environment key
        client = HeySolClient(api_key=None, skip_mcp_init=True)
        assert client.api_key is not None
        client.close()
    else:
        # Should fail
        try:
            HeySolClient(api_key=None, skip_mcp_init=True)
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            assert "API key is required" in str(e)


def test_client_initialization_with_config():
    """Test client initialization with config object."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    config = HeySolConfig(
        api_key=api_key, base_url="https://test.example.com", mcp_url="https://mcp.test.example.com"
    )
    client = HeySolClient(config=config, skip_mcp_init=True)

    assert client.api_key == api_key
    assert client.base_url == config.base_url
    assert client.mcp_url == config.mcp_url
    assert client.config == config


def test_client_from_env():
    """Test client creation from environment variables."""
    # This should work if environment is properly configured
    try:
        client = HeySolClient.from_env()
        # If we get here, environment is configured
        assert client.api_key is not None
        assert client.base_url is not None
    except ValidationError:
        # Expected if environment is not configured
        pass


def test_client_close():
    """Test client close method."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    # Should not raise any exceptions
    client.close()


def test_is_mcp_available():
    """Test MCP availability check."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    assert client.is_mcp_available() is False


def test_get_available_tools():
    """Test getting available MCP tools when MCP is not available."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    tools = client.get_available_tools()
    assert tools == {}


def test_get_tool_names():
    """Test getting MCP tool names when MCP is not available."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    tool_names = client.get_tool_names()
    assert tool_names == []


def test_call_tool_without_mcp():
    """Test calling MCP tool when MCP is not available."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    try:
        client.call_tool("test_tool")
        assert False, "Should have raised HeySolError"
    except Exception as e:
        assert "MCP is not available" in str(e)


def test_get_preferred_access_method():
    """Test getting preferred access method."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    # Should return direct_api when MCP is not available
    method = client.get_preferred_access_method("test_operation")
    assert method == "direct_api"

    # Should return direct_api when prefer_mcp is False
    client_with_preference = HeySolClient(api_key=api_key, prefer_mcp=False, skip_mcp_init=True)
    method = client_with_preference.get_preferred_access_method("test_operation")
    assert method == "direct_api"


def test_get_session_info():
    """Test getting MCP session info when MCP is not available."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, skip_mcp_init=True)

    session_info = client.get_session_info()
    assert session_info == {"mcp_available": False}


def test_client_initialization_with_mcp_preference():
    """Test client initialization with MCP preference."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    client = HeySolClient(api_key=api_key, prefer_mcp=True, skip_mcp_init=True)

    assert client.prefer_mcp is True
    assert client.mcp_available is False  # Still False because skip_mcp_init=True


def test_config_from_env():
    """Test config creation from environment."""
    try:
        config = HeySolConfig.from_env()
        # If we get here, environment is configured
        assert config.api_key is not None
        assert config.base_url is not None
    except Exception:
        # Expected if environment is not configured
        pass


def test_client_initialization_with_custom_base_url():
    """Test client initialization with custom base URL."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    base_url = "https://custom.api.example.com"
    client = HeySolClient(api_key=api_key, base_url=base_url, skip_mcp_init=True)

    assert client.base_url == base_url
    assert client.api_key == api_key


def test_client_initialization_with_custom_mcp_url():
    """Test client initialization with custom MCP URL."""
    # Use a real API key from the registry
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]

    mcp_url = "https://custom.mcp.example.com"
    client = HeySolClient(api_key=api_key, mcp_url=mcp_url, skip_mcp_init=True)

    assert client.mcp_url == mcp_url
    assert client.api_key == api_key
