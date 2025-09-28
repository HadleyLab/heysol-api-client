#!/usr/bin/env python3
"""
Unit Tests for HeySolAPIClient class

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

from heysol.clients.api_client import HeySolAPIClient
from heysol.exceptions import ValidationError

# Use a properly formatted test API key (50+ characters to pass validation)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef1234567890ab"


class TestHeySolAPIClient:
    """Unit tests for HeySolAPIClient class."""

    def test_api_client_initialization_with_timeout(self):
        """Test API client initialization with custom timeout."""
        with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config_instance.timeout = 30
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            assert client.timeout == 30

    def test_api_key_validation_success(self):
        """Test API key validation with successful response."""
        with patch("heysol.clients.api_client.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                # Should not raise exception
                assert client.api_key == TEST_API_KEY

    def test_is_valid_id_format(self):
        """Test ID format validation."""
        with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            # Valid IDs
            assert client._is_valid_id_format("valid-id-123") is True
            assert client._is_valid_id_format("cmg2ulh5r06kanx1vn3sshzrx") is True

            # Invalid IDs
            assert client._is_valid_id_format("") is False
            assert client._is_valid_id_format("   ") is False
            assert client._is_valid_id_format("invalid") is False
            assert client._is_valid_id_format("test") is False
            assert client._is_valid_id_format("ab") is False  # Too short

    def test_ingest_with_empty_message(self):
        """Test ingest method with empty message."""
        with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="Message is required"):
                client.ingest("")

    def test_search_with_empty_query(self):
        """Test search method with empty query."""
        with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="Search query is required"):
                client.search("")

    def test_create_space_with_empty_name(self):
        """Test create_space method with empty name."""
        with patch("heysol.clients.api_client.HeySolConfig") as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="Space name is required"):
                client.create_space("")


if __name__ == "__main__":
    pytest.main([__file__])
