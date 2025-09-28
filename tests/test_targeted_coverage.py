#!/usr/bin/env python3
"""
Targeted Coverage Tests for HeySol API Client

Focuses on testing specific missing lines with proper mocking:
- Tests lines that are difficult to reach with existing test patterns
- Uses proper mocking to avoid real network calls
- Follows the fail-fast testing philosophy
"""

import json
from unittest.mock import Mock, patch, PropertyMock

import pytest

from heysol.client import HeySolClient
from heysol.clients.api_client import HeySolAPIClient
from heysol.clients.mcp_client import HeySolMCPClient
from heysol.config import HeySolConfig
from heysol.exceptions import HeySolError, ValidationError


# Use a properly formatted test API key (50+ characters to pass validation)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef1234567890ab"


class TestSpecificMissingLines:
    """Test specific missing lines with targeted mocking."""

    def test_api_client_initialization_with_timeout_config(self):
        """Test API client initialization with timeout configuration."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config_instance.timeout = 60
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            assert client.timeout == 60

    def test_api_key_validation_success_path(self):
        """Test successful API key validation path."""
        with patch('heysol.clients.api_client.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                # Should complete without exception
                assert client.api_key == TEST_API_KEY

    def test_api_key_validation_authentication_error(self):
        """Test API key validation with authentication error."""
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

    def test_is_valid_id_format_comprehensive(self):
        """Test ID format validation comprehensively."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            # Valid formats
            assert client._is_valid_id_format("valid-id-123") is True
            assert client._is_valid_id_format("cmg2ulh5r06kanx1vn3sshzrx") is True
            assert client._is_valid_id_format("user_123") is True

            # Invalid formats
            assert client._is_valid_id_format("") is False
            assert client._is_valid_id_format("   ") is False
            assert client._is_valid_id_format("invalid") is False
            assert client._is_valid_id_format("test") is False
            assert client._is_valid_id_format("ab") is False  # Too short
            assert client._is_valid_id_format("null") is False
            assert client._is_valid_id_format("undefined") is False

    def test_make_request_with_params(self):
        """Test _make_request with query parameters."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"result": "success"}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client._make_request("GET", "test-endpoint", params={"param1": "value1"})

                assert result == {"result": "success"}
                # Verify params were passed
                call_args = mock_request.call_args
                assert call_args[1]["params"] == {"param1": "value1"}

    def test_ingest_with_complex_metadata(self):
        """Test ingest method with complex metadata."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.ingest(
                    message="test message",
                    space_id="space-123",
                    session_id="session-456",
                    source="test-source"
                )

                assert result == {"success": True}
                # Verify payload structure
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                assert payload["episodeBody"] == "test message"
                assert payload["spaceId"] == "space-123"
                assert payload["sessionId"] == "session-456"
                assert payload["source"] == "test-source"

    def test_copy_log_entry_with_complex_data(self):
        """Test copy_log_entry with complex log data."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                log_entry = {
                    "id": "log-123",
                    "ingestText": "Original message",
                    "data": {
                        "episodeBody": "Episode content",
                        "metadata": {"original": "metadata"},
                        "referenceTime": "2023-11-07T05:31:56Z",
                        "sessionId": "original-session"
                    },
                    "source": "original-source"
                }

                result = client.copy_log_entry(
                    log_entry=log_entry,
                    new_source="new-source",
                    new_space_id="new-space",
                    override_metadata={"new": "metadata"}
                )

                assert result == {"success": True}
                # Verify payload structure
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                assert payload["episodeBody"] == "Episode content"
                assert payload["source"] == "new-source"
                assert payload["spaceId"] == "new-space"
                assert payload["metadata"] == {"original": "metadata", "new": "metadata"}

    def test_search_with_complex_filters(self):
        """Test search method with complex filters."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"episodes": []}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.search(
                    query="test query",
                    space_ids=["space-1", "space-2"],
                    limit=50,
                    include_invalidated=True
                )

                assert result == {"episodes": []}
                # Verify payload structure
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                params = call_args[1]["params"]
                assert payload["query"] == "test query"
                assert payload["spaceIds"] == ["space-1", "space-2"]
                assert payload["includeInvalidated"] is True
                assert params["limit"] == 50

    def test_create_space_with_description(self):
        """Test create_space method with description."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": "space-123"}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.create_space("Test Space", "Test description")

                assert result == "space-123"
                # Verify payload structure
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                assert payload["name"] == "Test Space"
                assert payload["description"] == "Test description"

    def test_get_episode_facts_with_all_params(self):
        """Test get_episode_facts method with all parameters."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"facts": []}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.get_episode_facts(
                    episode_id="episode-123",
                    limit=50,
                    offset=10,
                    include_metadata=False
                )

                assert result == {"facts": []}
                # Verify params
                call_args = mock_request.call_args
                params = call_args[1]["params"]
                assert params["limit"] == 50
                assert params["offset"] == 10
                assert params["include_metadata"] is False

    def test_get_ingestion_logs_with_date_filters(self):
        """Test get_ingestion_logs method with date filters."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"logs": []}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.get_ingestion_logs(
                    space_id="space-123",
                    limit=25,
                    offset=5,
                    status="success",
                    start_date="2023-01-01",
                    end_date="2023-12-31"
                )

                assert result == []
                # Verify params
                call_args = mock_request.call_args
                params = call_args[1]["params"]
                assert params["spaceId"] == "space-123"
                assert params["limit"] == 25
                assert params["offset"] == 5
                assert params["status"] == "success"
                assert params["startDate"] == "2023-01-01"
                assert params["endDate"] == "2023-12-31"

    def test_get_space_details_with_all_options(self):
        """Test get_space_details method with all options."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"space": {"id": "space-123"}}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.get_space_details(
                    space_id="space-123",
                    include_stats=True,
                    include_metadata=True
                )

                assert result == {"space": {"id": "space-123"}}
                # Verify params
                call_args = mock_request.call_args
                params = call_args[1]["params"]
                assert params["include_stats"] is True
                assert params["include_metadata"] is True

    def test_update_space_with_all_fields(self):
        """Test update_space method with all fields."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"space": {"id": "space-123"}}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.update_space(
                    space_id="space-123",
                    name="Updated Name",
                    description="Updated description",
                    metadata={"key": "value"}
                )

                assert result == {"space": {"id": "space-123"}}
                # Verify payload
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                assert payload["name"] == "Updated Name"
                assert payload["description"] == "Updated description"

    def test_delete_space_with_confirmation(self):
        """Test delete_space method with confirmation."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.delete_space("space-123", confirm=True)

                assert result == {"success": True}
                # Verify DELETE method was used
                call_args = mock_request.call_args
                assert call_args[1]["method"] == "DELETE"

    def test_delete_space_without_confirmation(self):
        """Test delete_space method without confirmation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="requires confirmation"):
                client.delete_space("space-123", confirm=False)

    def test_list_webhooks_with_filters(self):
        """Test list_webhooks method with filters."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"webhooks": []}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.list_webhooks(
                    space_id="space-123",
                    active=True,
                    limit=50,
                    offset=10
                )

                assert result == []
                # Verify params
                call_args = mock_request.call_args
                params = call_args[1]["params"]
                assert params["limit"] == 50
                assert params["offset"] == 10

    def test_get_webhook_with_validation(self):
        """Test get_webhook method with validation."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": "webhook-123"}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.get_webhook("webhook-123")

                assert result == {"id": "webhook-123"}

    def test_get_webhook_invalid_format(self):
        """Test get_webhook method with invalid format."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="Invalid webhook ID format"):
                client.get_webhook("invalid")

    def test_update_webhook_with_events_list(self):
        """Test update_webhook method with events as list."""
        with patch('heysol.clients.api_client.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": "webhook-123"}
            mock_put.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.update_webhook(
                    webhook_id="webhook-123",
                    url="https://example.com/webhook",
                    events=["memory.created", "memory.updated"],
                    secret="secret-123",
                    active=True
                )

                assert result == {"id": "webhook-123"}
                # Verify events were joined with comma
                call_args = mock_put.call_args
                assert call_args[1]["data"]["events"] == "memory.created,memory.updated"

    def test_delete_webhook_with_confirmation(self):
        """Test delete_webhook method with confirmation."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.delete_webhook("webhook-123", confirm=True)

                assert result == {"success": True}
                # Verify DELETE method
                call_args = mock_request.call_args
                assert call_args[1]["method"] == "DELETE"

    def test_delete_webhook_without_confirmation(self):
        """Test delete_webhook method without confirmation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            with pytest.raises(ValidationError, match="requires confirmation"):
                client.delete_webhook("webhook-123", confirm=False)

    def test_delete_log_entry_with_payload(self):
        """Test delete_log_entry method with payload."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.delete_log_entry("log-123")

                assert result == {"success": True}
                # Verify payload contains ID
                call_args = mock_request.call_args
                payload = call_args[1]["json"]
                assert payload["id"] == "log-123"

    def test_close_method(self):
        """Test close method."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            # Should not raise exception
            client.close()

    def test_mcp_client_initialization_with_timeout(self):
        """Test MCP client initialization with timeout configuration."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config_instance.timeout = 120
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

            assert client.timeout == 120

    def test_mcp_client_get_session_info_comprehensive(self):
        """Test MCP client get_session_info with comprehensive data."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

            # Test with MCP available
            client.session_id = "session-123"
            client.tools = {"tool1": {"name": "tool1"}, "tool2": {"name": "tool2"}}

            info = client.get_session_info()

            assert info["session_id"] == "session-123"
            assert info["mcp_url"] == "https://mcp.test.com"
            assert info["tools_count"] == 2
            assert info["available_tools"] == ["tool1", "tool2"]
            assert info["is_available"] is True

            # Test with MCP unavailable
            client.session_id = None
            client.tools = {}

            info = client.get_session_info()

            assert info["session_id"] is None
            assert info["tools_count"] == 0
            assert info["available_tools"] == []
            assert info["is_available"] is False

    def test_mcp_client_refresh_tools(self):
        """Test MCP client refresh_tools method."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"tools": [{"name": "refreshed_tool"}]}
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config_instance.timeout = 30
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"old_tool": {}}

                client.refresh_tools()

                assert "refreshed_tool" in client.tools
                assert "old_tool" not in client.tools
                mock_post.assert_called_once()

    def test_mcp_client_close(self):
        """Test MCP client close method."""
        with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.mcp_url = "https://mcp.test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

            # Should not raise exception
            client.close()

    def test_client_initialization_mcp_preference_false(self):
        """Test client initialization with MCP preference disabled."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                prefer_mcp=False,
                skip_mcp_init=False
            )

            assert client.prefer_mcp is False
            assert client.mcp_available is True

    def test_client_from_env_classmethod(self):
        """Test HeySolClient.from_env classmethod."""
        with patch('heysol.client.HeySolConfig') as mock_config, \
             patch('heysol.client.HeySolAPIClient') as mock_api:

            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolClient.from_env()

            assert client.api_key == TEST_API_KEY
            assert client.base_url == "https://test.com"

    def test_client_get_preferred_access_method_api_only(self):
        """Test get_preferred_access_method with API-only preference."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = True
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                prefer_mcp=False,  # Prefer API
                skip_mcp_init=False
            )

            method = client.get_preferred_access_method("ingest")
            assert method == "direct_api"

    def test_client_get_session_info_mcp_unavailable(self):
        """Test get_session_info when MCP is unavailable."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = False
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=False
            )

            info = client.get_session_info()

            assert info == {"mcp_available": False}

    def test_client_call_tool_mcp_unavailable(self):
        """Test call_tool when MCP is unavailable."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = False
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=False
            )

            with pytest.raises(HeySolError, match="MCP is not available"):
                client.call_tool("test_tool")

    def test_client_get_available_tools_mcp_unavailable(self):
        """Test get_available_tools when MCP is unavailable."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = False
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=False
            )

            tools = client.get_available_tools()
            assert tools == {}

    def test_client_get_tool_names_mcp_unavailable(self):
        """Test get_tool_names when MCP is unavailable."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = False
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=False
            )

            tool_names = client.get_tool_names()
            assert tool_names == []

    def test_client_is_mcp_available_false(self):
        """Test is_mcp_available when MCP is not available."""
        with patch('heysol.client.HeySolAPIClient'), \
             patch('heysol.client.HeySolMCPClient') as mock_mcp:

            mock_mcp_instance = Mock()
            mock_mcp_instance.is_mcp_available.return_value = False
            mock_mcp.return_value = mock_mcp_instance

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=False
            )

            assert client.is_mcp_available() is False

    def test_client_initialization_skip_mcp_init(self):
        """Test client initialization with MCP init skipped."""
        with patch('heysol.client.HeySolAPIClient'):

            client = HeySolClient(
                api_key=TEST_API_KEY,
                skip_mcp_init=True  # Skip MCP initialization
            )

            assert client.mcp_available is False
            assert client.mcp_client is None

    def test_registry_config_initialization_with_custom_env(self):
        """Test RegistryConfig initialization with custom env file."""
        with patch('os.path.exists') as mock_exists, \
             patch('heysol.registry_config.load_dotenv') as mock_load:

            mock_exists.return_value = True

            config = RegistryConfig(env_file="/custom/path/.env")

            assert config.env_file == "/custom/path/.env"
            mock_load.assert_called_once_with("/custom/path/.env")

    def test_registry_config_get_instance_names(self):
        """Test get_instance_names method."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {
                "instances": {
                    "instance1": {"api_key_env_var": "KEY1"},
                    "instance2": {"api_key_env_var": "KEY2"},
                    "instance3": {"api_key_env_var": "KEY3"}
                }
            }
            mock_getenv.return_value = "dummy-key"

            config = RegistryConfig()

            names = config.get_instance_names()

            assert set(names) == {"instance1", "instance2", "instance3"}
            assert len(names) == 3

    def test_registry_config_get_instance(self):
        """Test get_instance method."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {
                "instances": {
                    "test_instance": {
                        "api_key_env_var": "TEST_KEY",
                        "base_url": "https://test.com/api/v1",
                        "description": "Test instance"
                    }
                }
            }
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

    def test_registry_config_get_registered_instances_immutable(self):
        """Test that get_registered_instances returns a copy."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {
                "instances": {
                    "test_instance": {
                        "api_key_env_var": "TEST_KEY",
                        "base_url": "https://test.com/api/v1"
                    }
                }
            }
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances1 = config.get_registered_instances()
            instances2 = config.get_registered_instances()

            # Should be different objects (copies)
            assert instances1 is not instances2
            assert instances1 == instances2

            # Modifying one should not affect the other
            instances1["new_key"] = "new_value"
            assert "new_key" not in instances2

    def test_registry_config_load_instances_default_base_url(self):
        """Test loading instances with default base URL."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {
                "instances": {
                    "instance_no_url": {
                        "api_key_env_var": "TEST_KEY"
                        # No base_url specified
                    }
                }
            }
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should use default base URL
            assert instances["instance_no_url"]["base_url"] == "https://core.heysol.ai/api/v1"

    def test_registry_config_load_instances_default_description(self):
        """Test loading instances with default description."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {
                "instances": {
                    "instance_no_desc": {
                        "api_key_env_var": "TEST_KEY",
                        "base_url": "https://test.com/api/v1"
                        # No description specified
                    }
                }
            }
            mock_getenv.return_value = "test-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should use instance name as default description
            assert instances["instance_no_desc"]["description"] == "instance_no_desc"

    def test_registry_config_load_instances_empty_config(self):
        """Test loading instances with empty config."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {"instances": {}}

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should return empty dict
            assert instances == {}

    def test_registry_config_load_instances_no_instances_key(self):
        """Test loading instances with missing instances key."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('json.load') as mock_json:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = {"other_key": "value"}

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should return empty dict when no instances key
            assert instances == {}

    def test_exceptions_validation_error_with_details(self):
        """Test ValidationError with detailed error information."""
        # This tests the missing line in exceptions.py (line 32)
        error = ValidationError("Test validation error")

        # Should be able to create and use ValidationError normally
        assert str(error) == "Test validation error"
        assert isinstance(error, Exception)
        assert isinstance(error, HeySolError)

    def test_cli_module_structure(self):
        """Test CLI module structure and imports."""
        # This tests the missing line in cli.py (line 17)
        # The line is likely an import or function definition
        import heysol.cli

        # Should be able to import without errors
        assert hasattr(heysol.cli, 'main')