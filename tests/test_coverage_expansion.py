#!/usr/bin/env python3
"""
Coverage Expansion Tests for HeySol API Client

Focuses on testing the specific lines missing from coverage analysis:
- api_client.py: 100 missing lines
- mcp_client.py: 122 missing lines
- client.py: 26 missing lines
- registry_config.py: 7 missing lines
- exceptions.py: 1 missing line
- cli.py: 1 missing line

Tests follow coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

import json
import os
import tempfile
from unittest.mock import Mock, patch, mock_open

import pytest

from heysol.client import HeySolClient
from heysol.clients.api_client import HeySolAPIClient
from heysol.clients.mcp_client import HeySolMCPClient
from heysol.config import HeySolConfig
from heysol.exceptions import HeySolError, ValidationError
from heysol.registry_config import RegistryConfig


# Use a properly formatted test API key (40+ characters)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef12345678"


class TestAPIClientMissingLines:
    """Test missing lines in api_client.py (100 missing lines)."""

    def test_api_key_validation_network_error(self):
        """Test API key validation with network error."""
        with patch('heysol.clients.api_client.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                # Should not raise exception for network errors during validation
                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")
                assert client.api_key == TEST_API_KEY

    def test_make_request_network_error(self):
        """Test _make_request with network error."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_request.side_effect = Exception("Network error")

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                with pytest.raises(HeySolError):
                    client._make_request("GET", "test-endpoint")

    def test_ingest_with_metadata_and_tags(self):
        """Test ingest method with metadata and tags."""
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

                result = client.add_data_to_ingestion_queue(
                    data="test data",
                    space_id="space-123",
                    priority="high",
                    tags=["tag1", "tag2"],
                    metadata={"key": "value"}
                )

                assert result == {"success": True}
                # Verify the request was made with correct data
                call_args = mock_request.call_args
                assert call_args[1]["json"]["episodeBody"] == "test data"
                assert call_args[1]["json"]["spaceId"] == "space-123"

    def test_search_knowledge_graph_validation(self):
        """Test search_knowledge_graph validation."""
        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = TEST_API_KEY
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

            # Test invalid limit
            with pytest.raises(ValidationError, match="Limit must be between 1 and 100"):
                client.search_knowledge_graph("test", limit=0)

            with pytest.raises(ValidationError, match="Limit must be between 1 and 100"):
                client.search_knowledge_graph("test", limit=101)

            # Test invalid depth
            with pytest.raises(ValidationError, match="Depth must be between 1 and 5"):
                client.search_knowledge_graph("test", depth=0)

            with pytest.raises(ValidationError, match="Depth must be between 1 and 5"):
                client.search_knowledge_graph("test", depth=6)

    def test_get_ingestion_logs_empty_result(self):
        """Test get_ingestion_logs with empty result."""
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

                result = client.get_ingestion_logs(space_id="space-123", limit=10)
                assert result == []

    def test_iter_ingestion_logs_safety_break(self):
        """Test iter_ingestion_logs safety break mechanism."""
        with patch.object(HeySolAPIClient, 'get_ingestion_logs') as mock_get_logs:
            # Return full batch size to trigger continuation
            mock_get_logs.return_value = [{"id": f"log-{i}"} for i in range(1000)]

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                # Should break after max batches to prevent infinite loop
                logs_list = list(client.iter_ingestion_logs())
                # Should have exactly 1000000 logs (1000 batches * 1000 logs per batch)
                assert len(logs_list) == 1000000

    def test_get_specific_log_endpoint_failure(self):
        """Test get_specific_log when endpoint fails."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_request.side_effect = Exception("Endpoint not available")

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.get_specific_log("log-123")

                assert "error" in result
                assert result["log_id"] == "log-123"
                assert "not available" in result["note"]

    def test_check_ingestion_status_no_logs_endpoint(self):
        """Test check_ingestion_status when logs endpoint fails."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_request.side_effect = Exception("Logs endpoint not available")

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.check_ingestion_status(space_id="space-123")

                assert result["ingestion_status"] == "unknown"
                assert "logs_error" in result

    def test_check_ingestion_status_search_fails(self):
        """Test check_ingestion_status when search also fails."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            # First call (logs) fails, second call (search) fails
            mock_request.side_effect = [
                Exception("Logs failed"),
                Exception("Search failed")
            ]

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.check_ingestion_status(space_id="space-123")

                assert result["ingestion_status"] == "unknown"
                assert "logs_error" in result
                assert "search_error" in result
                assert len(result["recommendations"]) > 0

    def test_list_webhooks_endpoint_failure(self):
        """Test list_webhooks when endpoint fails."""
        with patch('heysol.clients.api_client.requests.request') as mock_request:
            mock_request.side_effect = Exception("Webhooks endpoint not available")

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.list_webhooks()
                assert result == []

    def test_register_webhook_form_data(self):
        """Test register_webhook with form data encoding."""
        with patch('heysol.clients.api_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": "webhook-123"}
            mock_post.return_value = mock_response

            with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.base_url = "https://test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolAPIClient(api_key=TEST_API_KEY, base_url="https://test.com")

                result = client.register_webhook(
                    url="https://example.com/webhook",
                    events=["memory.created"],
                    secret="test-secret-12345"
                )

                assert result == {"id": "webhook-123"}
                # Verify form data was used
                call_args = mock_post.call_args
                assert call_args[1]["data"]["url"] == "https://example.com/webhook"
                assert call_args[1]["data"]["secret"] == "test-secret-12345"

    def test_update_webhook_form_data(self):
        """Test update_webhook with form data encoding."""
        with patch('heysol.clients.api_client.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": "webhook-123", "active": True}
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
                    secret="new-secret-12345",
                    active=True
                )

                assert result == {"id": "webhook-123", "active": True}
                # Verify form data was used with events as comma-separated string
                call_args = mock_put.call_args
                assert call_args[1]["data"]["url"] == "https://example.com/webhook"
                assert call_args[1]["data"]["events"] == "memory.created,memory.updated"
                assert call_args[1]["data"]["active"] == "true"


class TestMCPClientMissingLines:
    """Test missing lines in mcp_client.py (122 missing lines)."""

    def test_mcp_request_streaming(self):
        """Test _mcp_request with streaming."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"result": {"success": True}}
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"test_tool": {}}

                result = client._mcp_request("test_method", {"param": "value"}, stream=True)

                assert result == {"success": True}
                # Verify streaming was enabled
                call_args = mock_post.call_args
                assert call_args[1]["stream"] is True

    def test_parse_mcp_response_sse(self):
        """Test _parse_mcp_response with SSE content type."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.headers = {"Content-Type": "text/event-stream"}
            mock_response.iter_lines.return_value = [
                "data: ",
                "data: {\"result\": \"test\"}",
                "data: "
            ]
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"test_tool": {}}

                result = client._parse_mcp_response(mock_response)
                assert result == "test"

    def test_parse_mcp_response_no_json_in_sse(self):
        """Test _parse_mcp_response with SSE but no JSON."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.headers = {"Content-Type": "text/event-stream"}
            mock_response.iter_lines.return_value = ["data: ", "data: not json", "data: "]
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                with pytest.raises(HeySolError, match="No JSON in SSE stream"):
                    client._parse_mcp_response(mock_response)

    def test_parse_mcp_response_unsupported_content_type(self):
        """Test _parse_mcp_response with unsupported content type."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.headers = {"Content-Type": "application/xml"}
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                with pytest.raises(HeySolError, match="Unexpected Content-Type"):
                    client._parse_mcp_response(mock_response)

    def test_mcp_request_http_error(self):
        """Test _mcp_request with HTTP error."""
        with patch('heysol.clients.mcp_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception("Server error")
            mock_response.text = "Internal server error"
            mock_post.return_value = mock_response

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"test_tool": {}}

                with pytest.raises(HeySolError, match="HTTP error: 500"):
                    client._mcp_request("test_method")

    def test_delete_logs_by_source_with_results(self):
        """Test delete_logs_by_source with actual results."""
        with patch.object(HeySolMCPClient, 'call_tool') as mock_call_tool:
            mock_call_tool.return_value = {
                "episodes": [
                    {"id": "log-1", "source": "test-source"},
                    {"id": "log-2", "source": "test-source"},
                    {"id": "log-3", "source": "other-source"}
                ]
            }

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"memory_search": {}, "memory_delete": {}}

                result = client.delete_logs_by_source("test-source", space_id="space-123", confirm=True)

                assert result["deleted_count"] == 2  # Only test-source logs
                assert result["total_found"] == 2
                assert "test-source" in result["message"]

    def test_delete_logs_by_source_no_results(self):
        """Test delete_logs_by_source with no results."""
        with patch.object(HeySolMCPClient, 'call_tool') as mock_call_tool:
            mock_call_tool.return_value = {"episodes": []}

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"memory_search": {}}

                result = client.delete_logs_by_source("test-source", confirm=True)

                assert result["deleted_count"] == 0
                assert result["total_found"] == 0
                assert "No logs found" in result["message"]

    def test_delete_logs_by_source_with_errors(self):
        """Test delete_logs_by_source with deletion errors."""
        with patch.object(HeySolMCPClient, 'call_tool') as mock_call_tool:
            # First call returns logs, second call (delete) fails
            mock_call_tool.side_effect = [
                {
                    "episodes": [
                        {"id": "log-1", "source": "test-source"},
                        {"id": "log-2", "source": "test-source"}
                    ]
                },
                Exception("Delete failed"),
                Exception("Delete failed")
            ]

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"memory_search": {}, "memory_delete": {}}

                result = client.delete_logs_by_source("test-source", confirm=True)

                assert result["deleted_count"] == 0
                assert result["total_found"] == 2
                assert len(result["errors"]) == 2

    def test_get_logs_by_source_with_results(self):
        """Test get_logs_by_source with actual results."""
        with patch.object(HeySolMCPClient, 'call_tool') as mock_call_tool:
            mock_call_tool.return_value = {
                "episodes": [
                    {"id": "log-1", "source": "test-source", "content": "content1"},
                    {"id": "log-2", "source": "test-source", "content": "content2"},
                    {"id": "log-3", "source": "other-source", "content": "content3"}
                ]
            }

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"memory_search": {}}

                result = client.get_logs_by_source("test-source", space_id="space-123", limit=10)

                assert len(result["logs"]) == 2  # Only test-source logs
                assert result["total_count"] == 2
                assert result["source"] == "test-source"
                assert result["space_id"] == "space-123"

    def test_github_tools_integration(self):
        """Test GitHub tools integration methods."""
        with patch.object(HeySolMCPClient, 'call_tool') as mock_call_tool:
            mock_call_tool.return_value = {
                "notifications": [
                    {"id": "notif-1", "title": "Test notification"}
                ]
            }

            with patch('heysol.clients.mcp_client.HeySolConfig') as mock_config:
                mock_config_instance = Mock()
                mock_config_instance.api_key = TEST_API_KEY
                mock_config_instance.mcp_url = "https://mcp.test.com"
                mock_config.from_env.return_value = mock_config_instance

                client = HeySolMCPClient(api_key=TEST_API_KEY, mcp_url="https://mcp.test.com")

                # Mock MCP as available
                client.session_id = "session-123"
                client.tools = {"github_list_notifications": {}}

                result = client.github_list_notifications(owner="test", repo="test-repo")

                assert "notifications" in result
                mock_call_tool.assert_called_with("github_list_notifications",
                                                owner="test", repo="test-repo")


class TestClientMissingLines:
    """Test missing lines in client.py (26 missing lines)."""

    def test_move_logs_to_instance_actual_move(self):
        """Test move_logs_to_instance with actual move operation."""
        with patch('heysol.client.HeySolAPIClient') as mock_api:

            # Setup source client
            mock_source_api = Mock()
            mock_source_api.get_logs_by_source.return_value = {
                "logs": [{"id": "log-1"}, {"id": "log-2"}],
                "total_count": 2
            }
            mock_source_api.base_url = "https://source.com"

            # Setup target client
            mock_target_api = Mock()
            mock_target_api.base_url = "https://target.com"
            mock_target_api._make_request.return_value = {"success": True}
            mock_target_api.source = "target-source"

            mock_api.side_effect = [mock_source_api, mock_target_api]

            source_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://source.com", skip_mcp_init=True)
            target_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://target.com", skip_mcp_init=True)

            result = source_client.move_logs_to_instance(
                target_client=target_client,
                source="test-source",
                confirm=True,
                delete_after_move=True
            )

            assert result["operation"] == "move"
            assert "transferred_count" in result
            assert "deleted_count" in result

    def test_transfer_logs_to_instance_copy_operation(self):
        """Test _transfer_logs_to_instance with copy operation."""
        with patch('heysol.client.HeySolAPIClient') as mock_api:

            # Setup source client
            mock_source_api = Mock()
            mock_source_api.get_logs_by_source.return_value = {
                "logs": [{"id": "log-1", "data": {"episodeBody": "content1"}}],
                "total_count": 1
            }
            mock_source_api.base_url = "https://source.com"

            # Setup target client
            mock_target_api = Mock()
            mock_target_api.base_url = "https://target.com"
            mock_target_api._make_request.return_value = {"success": True}
            mock_target_api.source = "target-source"

            mock_api.side_effect = [mock_source_api, mock_target_api]

            source_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://source.com", skip_mcp_init=True)
            target_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://target.com", skip_mcp_init=True)

            result = source_client._transfer_logs_to_instance(
                source_client=source_client,
                target_client=target_client,
                source="test-source",
                confirm=True,
                operation="copy"
            )

            assert result["operation"] == "copy"
            assert "transferred_count" in result
            assert result["deleted_count"] is None  # Copy operation doesn't delete

    def test_transfer_logs_with_metadata_preservation(self):
        """Test _transfer_logs_to_instance with metadata preservation."""
        with patch('heysol.client.HeySolAPIClient') as mock_api:

            # Setup source client
            mock_source_api = Mock()
            mock_source_api.get_logs_by_source.return_value = {
                "logs": [{
                    "id": "log-1",
                    "data": {
                        "episodeBody": "test content",
                        "metadata": {"original": "metadata"},
                        "referenceTime": "2023-11-07T05:31:56Z",
                        "sessionId": "session-123"
                    }
                }],
                "total_count": 1
            }
            mock_source_api.base_url = "https://source.com"

            # Setup target client
            mock_target_api = Mock()
            mock_target_api.base_url = "https://target.com"
            mock_target_api._make_request.return_value = {"success": True}
            mock_target_api.source = "target-source"

            mock_api.side_effect = [mock_source_api, mock_target_api]

            source_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://source.com", skip_mcp_init=True)
            target_client = HeySolClient(api_key=TEST_API_KEY, base_url="https://target.com", skip_mcp_init=True)

            source_client._transfer_logs_to_instance(
                source_client=source_client,
                target_client=target_client,
                source="test-source",
                confirm=True
            )

            # Verify metadata was preserved in the API call
            call_args = mock_target_api._make_request.call_args
            payload = call_args[1]["data"]
            assert payload["episodeBody"] == "test content"
            assert payload["metadata"] == {"original": "metadata"}
            assert payload["referenceTime"] == "2023-11-07T05:31:56Z"
            assert payload["sessionId"] == "session-123"


class TestRegistryConfigMissingLines:
    """Test missing lines in registry_config.py (7 missing lines)."""

    def test_load_instances_default_heysol_api_key_fallback(self):
        """Test loading instances with HEYSOL_API_KEY fallback when env var missing."""
        config_content = {
            "instances": {
                "default_instance": {
                    "api_key_env_var": "HEYSOL_API_KEY",
                    "base_url": "https://default.com/api/v1"
                }
            }
        }

        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json, \
             patch('heysol.registry_config.HeySolConfig') as mock_heysol_config:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = None  # No env var

            # Mock HeySolConfig to return API key
            mock_config_instance = mock_heysol_config.from_env.return_value
            mock_config_instance.api_key = "fallback-api-key"

            config = RegistryConfig()

            instances = config.get_registered_instances()

            assert "default_instance" in instances
            assert instances["default_instance"]["api_key"] == "fallback-api-key"

    def test_load_instances_heysol_api_key_exception_handling(self):
        """Test loading instances with HEYSOL_API_KEY exception handling."""
        config_content = {
            "instances": {
                "default_instance": {
                    "api_key_env_var": "HEYSOL_API_KEY",
                    "base_url": "https://default.com/api/v1"
                }
            }
        }

        with patch('os.path.exists') as mock_exists, \
             patch('os.path.dirname') as mock_dirname, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('os.getenv') as mock_getenv, \
             patch('json.load') as mock_json, \
             patch('heysol.registry_config.HeySolConfig') as mock_heysol_config:

            mock_exists.return_value = True
            mock_dirname.return_value = "/test"
            mock_json.return_value = config_content
            mock_getenv.return_value = None

            # Mock HeySolConfig to raise exception
            mock_heysol_config.from_env.side_effect = Exception("Config error")

            config = RegistryConfig()

            instances = config.get_registered_instances()

            # Should skip instance when config fails
            assert "default_instance" not in instances


class TestExceptionsMissingLines:
    """Test missing lines in exceptions.py (1 missing line)."""

    def test_validation_error_with_details(self):
        """Test ValidationError with detailed error information."""
        # This tests the missing line in exceptions.py (line 32)
        error = ValidationError("Test validation error")

        # Should be able to create and use ValidationError normally
        assert str(error) == "Test validation error"
        assert isinstance(error, Exception)
        assert isinstance(error, HeySolError)


class TestCLIMissingLines:
    """Test missing lines in cli.py (1 missing line)."""

    def test_cli_module_structure(self):
        """Test CLI module structure and imports."""
        # This tests the missing line in cli.py (line 17)
        # The line is likely an import or function definition
        import heysol.cli

        # Should be able to import without errors
        assert hasattr(heysol.cli, 'main')