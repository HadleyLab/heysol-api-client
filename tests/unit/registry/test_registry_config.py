#!/usr/bin/env python3
"""
Unit Tests for RegistryConfig class with proper mocking

Following coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

import json

# Add the src directory to Python path
import sys
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from heysol.exceptions import HeySolError
from heysol.registry_config import RegistryConfig


class TestRegistryConfig:
    """Unit tests for RegistryConfig class with proper mocking."""

    def test_registry_config_initialization_with_env_file(self):
        """Test RegistryConfig initialization with specific env file."""
        with patch("os.path.exists") as mock_exists, patch(
            "heysol.registry_config.load_dotenv"
        ) as mock_load:

            mock_exists.return_value = True

            config = RegistryConfig(env_file="/path/to/.env")

            assert config.env_file == "/path/to/.env"
            mock_load.assert_called_once_with("/path/to/.env")

    def test_registry_config_initialization_missing_env_file(self):
        """Test RegistryConfig initialization with missing env file."""
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            with pytest.raises(HeySolError, match="Configuration file not found"):
                RegistryConfig(env_file="/nonexistent/.env")

    def test_load_instances_from_missing_config_file(self):
        """Test loading instances from missing config file."""
        with patch("os.path.exists") as mock_exists, patch("os.path.dirname") as mock_dirname:

            mock_exists.return_value = False
            mock_dirname.return_value = "/test/dir"

            with pytest.raises(HeySolError, match="Configuration file not found"):
                RegistryConfig()

    def test_load_instances_from_config_success(self):
        """Test successful loading of instances from config."""
        config_content = {
            "instances": {
                "test_instance": {
                    "api_key_env_var": "TEST_API_KEY",
                    "base_url": "https://test.com/api/v1",
                    "description": "Test instance",
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "test-api-key-value"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            assert "test_instance" in instances
            assert instances["test_instance"]["api_key"] == "test-api-key-value"
            assert instances["test_instance"]["base_url"] == "https://test.com/api/v1"
            assert instances["test_instance"]["description"] == "Test instance"

    def test_load_instances_with_default_api_key_handling(self):
        """Test loading instances with default HEYSOL_API_KEY handling."""
        config_content = {
            "instances": {
                "default_instance": {
                    "api_key_env_var": "HEYSOL_API_KEY",
                    "base_url": "https://default.com/api/v1",
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json, patch(
            "heysol.registry_config.HeySolConfig"
        ) as mock_heysol_config:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = None  # No env var set

            # Mock HeySolConfig to return API key
            mock_config_instance = mock_heysol_config.from_env.return_value
            mock_config_instance.api_key = "config-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            assert "default_instance" in instances
            assert instances["default_instance"]["api_key"] == "config-api-key"

    def test_load_instances_skip_missing_env_vars(self):
        """Test that instances with missing env vars are skipped."""
        config_content = {
            "instances": {
                "instance_with_key": {
                    "api_key_env_var": "EXISTING_KEY",
                    "base_url": "https://test.com/api/v1",
                },
                "instance_without_key": {
                    "api_key_env_var": "MISSING_KEY",
                    "base_url": "https://test2.com/api/v1",
                },
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.side_effect = lambda key: "api-key" if key == "EXISTING_KEY" else None

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should only include instance with existing env var
            assert "instance_with_key" in instances
            assert "instance_without_key" not in instances
            assert len(instances) == 1

    def test_load_instances_missing_api_key_env_var(self):
        """Test loading instances with missing api_key_env_var configuration."""
        config_content = {
            "instances": {
                "bad_instance": {
                    "base_url": "https://test.com/api/v1"
                    # Missing api_key_env_var
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch("json.load") as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content

            with pytest.raises(HeySolError, match="Missing api_key_env_var"):
                RegistryConfig()

    def test_load_instances_invalid_json(self):
        """Test loading instances with invalid JSON."""
        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch("json.load") as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

            with pytest.raises(HeySolError, match="Failed to load instances"):
                RegistryConfig()

    def test_get_instance_names(self):
        """Test get_instance_names method."""
        config_content = {
            "instances": {
                "instance1": {"api_key_env_var": "KEY1"},
                "instance2": {"api_key_env_var": "KEY2"},
                "instance3": {"api_key_env_var": "KEY3"},
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "dummy-key"

            config = RegistryConfig()

            names = config.get_instance_names()

            assert set(names) == {"instance1", "instance2", "instance3"}
            assert len(names) == 3

    def test_get_instance(self):
        """Test get_instance method."""
        config_content = {
            "instances": {
                "test_instance": {
                    "api_key_env_var": "TEST_KEY",
                    "base_url": "https://test.com/api/v1",
                    "description": "Test instance",
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            # Test existing instance
            instance = config.get_instance("test_instance")
            assert instance is not None
            assert instance["api_key"] == "test-api-key"
            assert instance["base_url"] == "https://test.com/api/v1"

            # Test non-existing instance
            instance = config.get_instance("nonexistent")
            assert instance is None

    def test_get_registered_instances_immutable(self):
        """Test that get_registered_instances returns a copy."""
        config_content = {
            "instances": {
                "test_instance": {
                    "api_key_env_var": "TEST_KEY",
                    "base_url": "https://test.com/api/v1",
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances1 = config.get_registered_instances()
            instances2 = config.get_registered_instances()

            # Should be different objects (copies)
            assert instances1 is not instances2
            assert instances1 == instances2

            # Modifying one should not affect the other
            # Test copy behavior by adding a new key-value pair
            original_length = len(instances1)
            test_instance = {"api_key": "test", "base_url": "test", "description": "test"}
            instances1["test_key"] = test_instance
            assert len(instances1) == original_length + 1
            assert len(instances2) == original_length  # Other dict should be unchanged

    def test_load_instances_default_base_url(self):
        """Test loading instances with default base URL."""
        config_content = {
            "instances": {
                "instance_no_url": {
                    "api_key_env_var": "TEST_KEY"
                    # No base_url specified
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should use default base URL
            assert instances["instance_no_url"]["base_url"] == "https://core.heysol.ai/api/v1"

    def test_load_instances_default_description(self):
        """Test loading instances with default description."""
        config_content = {
            "instances": {
                "instance_no_desc": {
                    "api_key_env_var": "TEST_KEY",
                    "base_url": "https://test.com/api/v1",
                    # No description specified
                }
            }
        }

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch(
            "os.getenv"
        ) as mock_getenv, patch(
            "json.load"
        ) as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should use instance name as default description
            assert instances["instance_no_desc"]["description"] == "instance_no_desc"

    def test_load_instances_empty_config(self):
        """Test loading instances with empty config."""
        config_content: dict = {"instances": {}}

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch("json.load") as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should return empty dict
            assert instances == {}

    def test_load_instances_no_instances_key(self):
        """Test loading instances with missing instances key."""
        config_content = {"other_key": "value"}

        with patch("os.path.exists") as mock_exists, patch(
            "os.path.dirname"
        ) as mock_dirname, patch("builtins.open", mock_open()), patch("json.load") as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should return empty dict when no instances key
            assert instances == {}


if __name__ == "__main__":
    pytest.main([__file__])
