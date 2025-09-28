#!/usr/bin/env python3
"""
Comprehensive Unit Tests for HeySol API Client

Tests all uncovered functions following coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
- Validation at Entry: Validate inputs immediately at function boundaries
"""

import pytest
from unittest.mock import Mock, patch

from heysol.client import HeySolClient
from heysol.clients.api_client import HeySolAPIClient
from heysol.clients.mcp_client import HeySolMCPClient
from heysol.config import HeySolConfig
from heysol.exceptions import HeySolError, ValidationError


class TestHeySolClientComprehensive:
    """Comprehensive tests for HeySolClient class."""

    def test_client_initialization_with_mcp_preference(self):
        """Test client initialization with MCP preference."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            assert client.prefer_mcp is True
            assert client.mcp_available is True

    def test_client_initialization_mcp_fallback(self):
        """Test client initialization with MCP fallback on failure."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Simulate MCP initialization failure
            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                skip_mcp_init=False
            )

            # Should fallback gracefully
            assert client.mcp_available is False
            assert client.mcp_client is None

    def test_ingest_with_mcp_fallback(self):
        """Test ingest method with MCP fallback."""
        with patch('heysol.client.HeySolAPIClient') as mock_api, \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Setup mocks
            mock_api_instance = Mock()
            mock_api_instance.ingest.return_value = {"success": True}
            mock_api.return_value = mock_api_instance

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp_instance.ingest_via_mcp.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            result = client.ingest("test message")

            # Should fallback to API
            assert result == {"success": True}
            mock_api_instance.ingest.assert_called_once()

    def test_search_with_mcp_fallback(self):
        """Test search method with MCP fallback."""
        with patch('heysol.client.HeySolAPIClient') as mock_api, \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Setup mocks
            mock_api_instance = Mock()
            mock_api_instance.search.return_value = {"episodes": []}
            mock_api.return_value = mock_api_instance

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp_instance.search_via_mcp.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            result = client.search("test query")

            # Should fallback to API
            assert result == {"episodes": []}
            mock_api_instance.search.assert_called_once()

    def test_get_spaces_with_mcp_fallback(self):
        """Test get_spaces method with MCP fallback."""
        with patch('heysol.client.HeySolAPIClient') as mock_api, \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Setup mocks
            mock_api_instance = Mock()
            mock_api_instance.get_spaces.return_value = [{"id": "1", "name": "test"}]
            mock_api.return_value = mock_api_instance

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp_instance.get_spaces_via_mcp.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            result = client.get_spaces()

            # Should fallback to API
            assert result == [{"id": "1", "name": "test"}]
            mock_api_instance.get_spaces.assert_called_once()

    def test_get_user_profile_with_mcp_fallback(self):
        """Test get_user_profile method with MCP fallback."""
        with patch('heysol.client.HeySolAPIClient') as mock_api, \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Setup mocks
            mock_api_instance = Mock()
            mock_api_instance.get_user_profile.return_value = {"id": "1", "name": "test"}
            mock_api.return_value = mock_api_instance

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp_instance.get_user_profile_via_mcp.side_effect = Exception("MCP failed")
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            result = client.get_user_profile()

            # Should fallback to API
            assert result == {"id": "1", "name": "test"}
            mock_api_instance.get_user_profile.assert_called_once()

    def test_move_logs_to_instance_preview_mode(self):
        """Test move_logs_to_instance in preview mode."""
        with patch('heysol.client.HeySolAPIClient') as mock_api:

            mock_api_instance = Mock()
            mock_api_instance.get_logs_by_source.return_value = {
                "logs": [{"id": "1"}, {"id": "2"}],
                "total_count": 2
            }
            mock_api.return_value = mock_api_instance

            source_client = HeySolClient(api_key="source-key", skip_mcp_init=True)
            target_client = HeySolClient(api_key="target-key", skip_mcp_init=True)

            result = source_client.move_logs_to_instance(
                target_client=target_client,
                source="test-source",
                confirm=False  # Preview mode
            )

            assert result["operation"] == "move_preview"
            assert result["logs_to_move"] == 2
            assert "Preview: Would move" in result["message"]

    def test_preferred_access_method(self):
        """Test get_preferred_access_method functionality."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            # Test with MCP preferred and available
            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key="rc_pat_test_key_1234567890abcdef",
                prefer_mcp=True,
                skip_mcp_init=False
            )

            method = client.get_preferred_access_method("ingest")
            assert method == "mcp"

            # Test with MCP not available
            mock_mcp_instance.is_mcp_available.return_value = False
            method = client.get_preferred_access_method("ingest")
            assert method == "direct_api"

    def test_client_close(self):
        """Test client close method."""
        with patch('heysol.client.HeySolAPIClient') as mock_api, \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_api_instance = Mock()
            mock_mcp_instance = Mock()
            mock_api.return_value = mock_api_instance
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(api_key="rc_pat_test_key_1234567890abcdef", skip_mcp_init=False)

            # Should not raise exception
            client.close()

            mock_mcp_instance.close.assert_called_once()
            mock_api_instance.close.assert_called_once()


class TestHeySolAPIClientComprehensive:
    """Comprehensive tests for HeySolAPIClient class."""

    def test_api_client_initialization_with_timeout(self):
        """Test API client initialization with custom timeout."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config_instance.timeout = 30
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            assert client.timeout == 30

    def test_api_key_validation_success(self):
        """Test API key validation with successful response."""
        with patch('heysol.clients.api_client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

                # Should not raise exception
                assert client.api_key == "rc_pat_test_key_1234567890abcdef"

    def test_api_key_validation_failure(self):
        """Test API key validation with authentication failure."""
        with patch('heysol.clients.api_client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "invalid-key"
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                with pytest.raises(ValidationError, match="Invalid API key"):
                    HeySolAPIClient(api_key="invalid-key", base_url="https://test.com")

    def test_is_valid_id_format(self):
        """Test ID format validation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            # Valid IDs
            assert client._is_valid_id_format("valid-id-123") is True
            assert client._is_valid_id_format("cmg2ulh5r06kanx1vn3sshzrx") is True

            # Invalid IDs
            assert client._is_valid_id_format("") is False
            assert client._is_valid_id_format("   ") is False
            assert client._is_valid_id_format("invalid") is False
            assert client._is_valid_id_format("test") is False
            assert client._is_valid_id_format("ab") is False  # Too short

    def test_make_request_with_absolute_url(self):
        """Test _make_request with absolute URL."""
        with patch('heysol.clients.api_client.requests.request') as mock_request, \
             patch('heysol.clients.api_client.HeySolConfig') as mock_config:

            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            result = client._make_request("GET", "https://absolute-url.com/endpoint")

            assert result == {"success": True}
            mock_request.assert_called_once()
            # Verify absolute URL was used
            call_args = mock_request.call_args
            assert call_args[1]["url"] == "https://absolute-url.com/endpoint"

    def test_ingest_with_empty_message(self):
        """Test ingest method with empty message."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Message is required"):
                client.ingest("")

    def test_copy_log_entry_with_missing_content(self):
        """Test copy_log_entry with log entry missing content."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            # Log entry without content
            log_entry = {"id": "1", "source": "test"}

            with pytest.raises(ValidationError, match="must contain message content"):
                client.copy_log_entry(log_entry)

    def test_search_with_empty_query(self):
        """Test search method with empty query."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Search query is required"):
                client.search("")

    def test_create_space_with_empty_name(self):
        """Test create_space method with empty name."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Space name is required"):
                client.create_space("")

    def test_get_episode_facts_with_empty_id(self):
        """Test get_episode_facts method with empty episode ID."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Episode ID is required"):
                client.get_episode_facts("")

    def test_get_specific_log_with_empty_id(self):
        """Test get_specific_log method with empty log ID."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Log ID is required"):
                client.get_specific_log("")

    def test_get_specific_log_with_invalid_format(self):
        """Test get_specific_log method with invalid ID format."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Invalid log ID format"):
                client.get_specific_log("invalid")

    def test_get_space_details_with_empty_id(self):
        """Test get_space_details method with empty space ID."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Space ID is required"):
                client.get_space_details("")

    def test_get_space_details_with_invalid_format(self):
        """Test get_space_details method with invalid space ID format."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Invalid space ID format"):
                client.get_space_details("test")

    def test_update_space_without_fields(self):
        """Test update_space method without any fields to update."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="At least one field must be provided"):
                client.update_space("space-id")

    def test_delete_space_without_confirm(self):
        """Test delete_space method without confirmation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="requires confirmation"):
                client.delete_space("space-id", confirm=False)

    def test_register_webhook_without_url(self):
        """Test register_webhook method without URL."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Webhook URL is required"):
                client.register_webhook("", events=["test"], secret="secret")

    def test_register_webhook_without_secret(self):
        """Test register_webhook method without secret."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Webhook secret is required"):
                client.register_webhook("https://test.com", events=["test"], secret="")

    def test_get_webhook_with_empty_id(self):
        """Test get_webhook method with empty webhook ID."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Webhook ID is required"):
                client.get_webhook("")

    def test_get_webhook_with_invalid_format(self):
        """Test get_webhook method with invalid webhook ID format."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Invalid webhook ID format"):
                client.get_webhook("invalid")

    def test_update_webhook_validation(self):
        """Test update_webhook method validation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            # Test empty webhook ID
            with pytest.raises(ValidationError, match="Webhook ID is required"):
                client.update_webhook("", "https://test.com", ["test"], "secret")

            # Test empty URL
            with pytest.raises(ValidationError, match="Webhook URL is required"):
                client.update_webhook("webhook-id", "", ["test"], "secret")

            # Test empty events
            with pytest.raises(ValidationError, match="Webhook events are required"):
                client.update_webhook("webhook-id", "https://test.com", [], "secret")

            # Test empty secret
            with pytest.raises(ValidationError, match="Webhook secret is required"):
                client.update_webhook("webhook-id", "https://test.com", ["test"], "")

    def test_delete_webhook_without_confirm(self):
        """Test delete_webhook method without confirmation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="requires confirmation"):
                client.delete_webhook("webhook-id", confirm=False)

    def test_delete_log_entry_with_empty_id(self):
        """Test delete_log_entry method with empty log ID."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key="rc_pat_test_key_1234567890abcdef", base_url="https://test.com")

            with pytest.raises(ValidationError, match="Log ID is required"):
                client.delete_log_entry("")


class TestHeySolMCPClientComprehensive:
    """Comprehensive tests for HeySolMCPClient class."""

    def test_mcp_client_initialization_success(self):
        """Test MCP client initialization with successful session."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            # Mock successful initialization response
            init_response = Mock()
            init_response.status_code = 200
            init_response.raise_for_status.return_value = None
            init_response.json.return_value = {"result": {"capabilities": {}}}
            init_response.headers = {"Mcp-Session-Id": "session-123"}

            # Mock successful tools list response
            tools_response = Mock()
            tools_response.status_code = 200
            tools_response.raise_for_status.return_value = None
            tools_response.json.return_value = {"tools": [{"name": "test_tool"}]}

            mock_post.side_effect = [init_response, tools_response]

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

                assert client.session_id == "session-123"
                assert "test_tool" in client.tools
                assert client.is_mcp_available() is True

    def test_mcp_client_initialization_failure(self):
        """Test MCP client initialization with failure."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception("Server error")
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                with pytest.raises(HeySolError, match="Failed to initialize MCP session"):
                    HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

    def test_ensure_mcp_available_with_tool_check(self):
        """Test ensure_mcp_available with specific tool check."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            # Mock MCP as unavailable
            client.session_id = None
            client.tools = {}

            with pytest.raises(HeySolError, match="MCP is not available"):
                client.ensure_mcp_available()

            # Setup MCP as available but tool not found
            client.session_id = "session-123"
            client.tools = {"existing_tool": {}}

            with pytest.raises(HeySolError, match="MCP tool 'nonexistent' is not available"):
                client.ensure_mcp_available("nonexistent")

    def test_call_tool_success(self):
        """Test successful tool call."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"result": {"success": True}}
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"test_tool": {"name": "test_tool"}}

                result = client.call_tool("test_tool", param1="value1")

                assert result == {"success": True}
                mock_post.assert_called_once()

    def test_call_tool_mcp_unavailable(self):
        """Test tool call when MCP is unavailable."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            # Mock MCP as unavailable
            client.session_id = None
            client.tools = {}

            with pytest.raises(HeySolError, match="MCP is not available"):
                client.call_tool("test_tool")

    def test_delete_logs_by_source_without_confirm(self):
        """Test delete_logs_by_source without confirmation."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            with pytest.raises(ValidationError, match="requires confirmation"):
                client.delete_logs_by_source("test-source", confirm=False)

    def test_delete_logs_by_source_empty_source(self):
        """Test delete_logs_by_source with empty source."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            with pytest.raises(ValidationError, match="Source is required"):
                client.delete_logs_by_source("", confirm=True)

    def test_get_logs_by_source_empty_source(self):
        """Test get_logs_by_source with empty source."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            with pytest.raises(ValidationError, match="Source is required"):
                client.get_logs_by_source("")

    def test_refresh_tools(self):
        """Test refresh_tools method."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"tools": [{"name": "refreshed_tool"}]}
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"old_tool": {}}

                client.refresh_tools()

                assert "refreshed_tool" in client.tools
                assert "old_tool" not in client.tools
                mock_post.assert_called_once()

    def test_get_session_info(self):
        """Test get_session_info method."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = "rc_pat_test_key_1234567890abcdef"
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key="rc_pat_test_key_1234567890abcdef", mcp_url="https://mcp.test.com")

            # Test with MCP available
            client.session_id = "session-123"
            client.tools = {"tool1": {}, "tool2": {}}

            info = client.get_session_info()

            assert info["session_id"] == "session-123"
            assert info["mcp_url"] == "https://mcp.test.com"
            assert info["tools_count"] == 2
            assert info["is_available"] is True

            # Test with MCP unavailable
            client.session_id = None
            client.tools = {}

            info = client.get_session_info()

            assert info["session_id"] is None
            assert info["tools_count"] == 0
            assert info["is_available"] is False