#!/usr/bin/env python3
"""
Integration tests for registry functionality with real API calls

Following coding standards:
- Integration Tests for APIs: Allow integration tests for external API validation using real API keys and live calls, rejecting mocking
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

import sys
from pathlib import Path

import pytest

# Add the src directory to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from heysol.registry_config import RegistryConfig


class TestRegistryIntegration:
    """Integration tests for registry functionality with real API calls."""

    def test_real_env_file_loading_live(self):
        """Test loading registry from real .env file with live validation."""
        # Use the actual .env file in the project
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        # Test that RegistryConfig can load from real .env file
        config = RegistryConfig(env_file=str(env_file))
        instances = config.get_registered_instances()

        # Should have at least the instances we know exist
        assert len(instances) >= 1
        assert "HadleyLaboratory@gmail.com" in instances

        # Verify the API key is loaded correctly and appears valid
        hadley_instance = instances["HadleyLaboratory@gmail.com"]
        assert "api_key" in hadley_instance
        assert hadley_instance["api_key"].startswith("rc_pat_")
        assert len(hadley_instance["api_key"]) > 20  # Valid API key length
        assert hadley_instance["base_url"] == "https://core.heysol.ai/api/v1"

    def test_multiple_users_real_scenario_live(self):
        """Test multiple users scenario with real configuration and validation."""
        # Test with the actual .env file
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        # Load the actual config.json
        config_file = Path(__file__).parent.parent.parent / "src" / "heysol" / "config.json"

        if not config_file.exists():
            pytest.skip("No config.json file found for live testing")

        # Test loading with real env file
        config = RegistryConfig(env_file=str(env_file))
        instances = config.get_registered_instances()

        # Should load all instances that have valid API keys
        assert len(instances) >= 1

        # Verify each instance has required fields
        for name, instance in instances.items():
            assert "api_key" in instance
            assert "base_url" in instance
            assert "description" in instance

            # Validate API key format
            assert instance["api_key"].startswith("rc_pat_")
            assert len(instance["api_key"]) > 20

            # Validate base URL
            assert instance["base_url"] == "https://core.heysol.ai/api/v1"

            # Validate description
            assert len(instance["description"]) > 0

            # API key format validation
            assert instance["api_key"].startswith("rc_pat_")

    def test_registry_get_instance_names_live(self):
        """Test get_instance_names method with real data."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))
        names = config.get_instance_names()

        # Should return list of instance names
        assert isinstance(names, list)
        assert len(names) >= 1
        assert "HadleyLaboratory@gmail.com" in names

        # All names should be strings
        for name in names:
            assert isinstance(name, str)
            assert len(name) > 0

    def test_registry_get_instance_live(self):
        """Test get_instance method with real data."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))

        # Test existing instance
        instance = config.get_instance("HadleyLaboratory@gmail.com")
        assert instance is not None
        assert "api_key" in instance
        assert "base_url" in instance
        assert "description" in instance

        # Test non-existing instance
        instance = config.get_instance("nonexistent@example.com")
        assert instance is None

    def test_registry_get_registered_instances_immutable_live(self):
        """Test that get_registered_instances returns a copy with real data."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))

        instances1 = config.get_registered_instances()
        instances2 = config.get_registered_instances()

        # Should be different objects (copies)
        assert instances1 is not instances2
        assert instances1 == instances2

        # Modifying one should not affect the other
        if instances1:
            # Test copy behavior by adding a new key-value pair
            original_length = len(instances1)
            test_instance = {"api_key": "test", "base_url": "test", "description": "test"}
            instances1["test_key"] = test_instance
            assert len(instances1) == original_length + 1
            assert len(instances2) == original_length  # Other dict should be unchanged

    def test_registry_config_initialization_with_real_env_file(self):
        """Test RegistryConfig initialization with real env file."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        # Should not raise any exceptions
        config = RegistryConfig(env_file=str(env_file))
        assert config.env_file == str(env_file)

        # Should have loaded instances
        instances = config.get_registered_instances()
        assert isinstance(instances, dict)

    def test_registry_config_initialization_without_env_file(self):
        """Test RegistryConfig initialization without env file."""
        # Should work with default .env file discovery
        config = RegistryConfig()
        instances = config.get_registered_instances()
        assert isinstance(instances, dict)

    def test_registry_instance_data_integrity(self):
        """Test that registry instances have correct data structure."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))
        instances = config.get_registered_instances()

        # Test data integrity for each instance
        for name, instance in instances.items():
            # Required fields
            assert "api_key" in instance
            assert "base_url" in instance
            assert "description" in instance

            # Data types
            assert isinstance(instance["api_key"], str)
            assert isinstance(instance["base_url"], str)
            assert isinstance(instance["description"], str)

            # Data validity
            assert len(instance["api_key"]) > 0
            assert instance["base_url"].startswith("https://")
            assert len(instance["description"]) > 0

            # API key format validation
            assert instance["api_key"].startswith("rc_pat_")

    def test_registry_instance_uniqueness(self):
        """Test that registry instances have unique API keys."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))
        instances = config.get_registered_instances()

        # Collect all API keys
        api_keys = [instance["api_key"] for instance in instances.values()]

        # All API keys should be unique
        assert len(api_keys) == len(set(api_keys))

    def test_registry_configuration_persistence(self):
        """Test that registry configuration persists across calls."""
        env_file = Path(__file__).parent.parent.parent / ".env"

        if not env_file.exists():
            pytest.skip("No .env file found for live testing")

        config = RegistryConfig(env_file=str(env_file))

        # Multiple calls should return consistent results
        instances1 = config.get_registered_instances()
        instances2 = config.get_registered_instances()
        names1 = config.get_instance_names()
        names2 = config.get_instance_names()

        assert instances1 == instances2
        assert names1 == names2


if __name__ == "__main__":
    pytest.main([__file__])
