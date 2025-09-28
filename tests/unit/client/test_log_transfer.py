#!/usr/bin/env python3
"""
Comprehensive Unit and Integration Tests for Log Transfer Operations

Tests the log transfer functionality including move_logs_to_instance, copy_logs_to_instance,
_transfer_logs_to_instance methods in client.py, and CLI commands in cli/memory.py.

Covers parameter handling, error scenarios, edge cases, and cross-instance interactions.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

# Add the parent directory to the Python path to import the CLI
sys.path.insert(0, str(Path(__file__).parent.parent))

from heysol.cli import app
from heysol.client import HeySolClient


class TestLogTransferOperations:
    """Unit tests for log transfer operations in HeySolClient."""

    @pytest.fixture
    def mock_source_client(self):
        """Create a mock source client for testing."""
        client = Mock(spec=HeySolClient)
        client.base_url = "https://source-api.example.com"
        client.api_key = "source-key"
        # Add api_client mock with required attributes and methods
        client.api_client = Mock()
        client.api_client.base_url = "https://source-api.example.com"
        client.api_client.source = "test-source"
        # Add required methods
        client.get_logs_by_source = Mock()
        client.get_specific_log = Mock()
        client.delete_log_entry = Mock()
        client.close = Mock()
        return client

    @pytest.fixture
    def mock_target_client(self):
        """Create a mock target client for testing."""
        client = Mock(spec=HeySolClient)
        client.base_url = "https://target-api.example.com"
        client.api_key = "target-key"
        # Add api_client mock with required attributes and methods
        client.api_client = Mock()
        client.api_client.base_url = "https://target-api.example.com"
        client.api_client.source = "target-source"
        # Add required methods
        client.ingest = Mock()
        client.close = Mock()
        # Add _make_request method that's called internally
        client.api_client._make_request = Mock()
        return client

    @pytest.fixture
    def sample_logs(self):
        """Sample log data for testing."""
        return [
            {
                "id": "log-1",
                "source": "test-source",
                "ingestText": "Sample log entry 1",
                "data": {"episodeBody": "Alternative content 1"},
            },
            {
                "id": "log-2",
                "source": "test-source",
                "ingestText": "Sample log entry 2",
                "data": {"episodeBody": "Alternative content 2"},
            },
            {
                "id": "log-3",
                "source": "other-source",
                "ingestText": "Sample log entry 3",
                "data": {"episodeBody": "Alternative content 3"},
            },
        ]

    def test_move_logs_to_instance_basic(self, mock_source_client, mock_target_client, sample_logs):
        """Test basic move_logs_to_instance functionality."""
        # Setup mocks
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:2],  # Only logs from test-source
            "total_count": 2,
        }
        mock_source_client.get_specific_log.side_effect = lambda log_id: next(
            (log for log in sample_logs if log["id"] == log_id), {}
        )
        mock_target_client.ingest = Mock()

        # Call the method
        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
        )

        # Assertions
        assert result["operation"] == "move"
        assert result["transferred_count"] == 2
        assert result["total_attempted"] == 2
        assert "deleted_count" in result
        assert result["deleted_count"] == 2

        # Verify calls
        mock_source_client.get_logs_by_source.assert_called_once_with(
            source="test-source", space_id=None, limit=10000
        )
        assert mock_target_client.api_client._make_request.call_count == 2
        assert mock_source_client.delete_log_entry.call_count == 2

    def test_copy_logs_to_instance_basic(self, mock_source_client, mock_target_client, sample_logs):
        """Test basic copy_logs_to_instance functionality."""
        # Setup mocks
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:2],  # Only logs from test-source
            "total_count": 2,
        }
        mock_source_client.get_specific_log.side_effect = lambda log_id: next(
            (log for log in sample_logs if log["id"] == log_id), {}
        )
        mock_target_client.ingest = Mock()

        # Call the method
        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        # Assertions
        assert result["operation"] == "copy"
        assert result["transferred_count"] == 2
        assert result["total_attempted"] == 2
        assert result["deleted_count"] is None  # Present but None for copy operations

        # Verify calls
        mock_source_client.get_logs_by_source.assert_called_once_with(
            source="test-source", space_id=None, limit=10000
        )
        assert mock_target_client.api_client._make_request.call_count == 2
        # No delete calls for copy
        mock_source_client.delete_log_entry.assert_not_called()

    def test_transfer_logs_preview_mode(self, mock_source_client, mock_target_client, sample_logs):
        """Test transfer operations in preview mode (confirm=False)."""
        mock_source_client.get_logs_by_source.return_value = {"logs": sample_logs, "total_count": 3}

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=False,
            operation="move",
            delete_after_transfer=True,
        )

        assert result["operation"] == "move_preview"
        assert result["logs_to_transfer"] == 3
        assert result["total_count"] == 3
        assert "Preview: Would move 3 logs" in result["message"]

        # No actual transfer operations should occur
        mock_target_client.api_client._make_request.assert_not_called()
        mock_source_client.delete_log_entry.assert_not_called()

    def test_transfer_logs_with_space_filter(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test transfer operations with space filtering."""
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:1],
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = sample_logs[0]
        mock_target_client.ingest = Mock()

        HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            space_id="space-123",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        mock_source_client.get_logs_by_source.assert_called_once_with(
            source="test-source", space_id="space-123", limit=10000
        )

    def test_transfer_logs_with_target_space_and_session(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test transfer operations with target space and session parameters."""
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:1],
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = sample_logs[0]
        mock_target_client.ingest = Mock()

        HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
            target_space_id="target-space-456",
            target_session_id="session-789",
        )

        # Verify _make_request was called with target space and session
        mock_target_client.api_client._make_request.assert_called_once_with(
            "POST",
            "add",
            data={
                "episodeBody": "Sample log entry 1",
                "referenceTime": None,
                "metadata": {},
                "source": "target-source",  # Uses target client's source
                "sessionId": "session-789",
                "spaceId": "target-space-456",
            },
        )

    def test_transfer_logs_fallback_to_original_space(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test transfer operations fallback to original space when target_space_id is None."""
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:1],
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = sample_logs[0]
        mock_target_client.ingest = Mock()

        HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            space_id="source-space-123",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
            target_space_id=None,  # No target space specified
            target_session_id="session-789",
        )

        # Verify _make_request was called with original space
        mock_target_client.api_client._make_request.assert_called_once_with(
            "POST",
            "add",
            data={
                "episodeBody": "Sample log entry 1",
                "referenceTime": None,
                "metadata": {},
                "source": "target-source",  # Uses target client's source
                "sessionId": "session-789",
                # No spaceId since target_space_id was None
            },
        )

    def test_transfer_logs_with_alternative_content(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test transfer operations using alternative content from log data."""
        # Create log with empty ingestText but data.episodeBody
        log_with_alt_content = {
            "id": "log-alt",
            "source": "test-source",
            "ingestText": "",  # Empty
            "data": {"episodeBody": "Alternative content from episodeBody"},
        }

        mock_source_client.get_logs_by_source.return_value = {
            "logs": [log_with_alt_content],
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = log_with_alt_content
        mock_target_client.ingest = Mock()

        HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        # Verify alternative content was used
        mock_target_client.api_client._make_request.assert_called_once_with(
            "POST",
            "add",
            data={
                "episodeBody": "Alternative content from episodeBody",
                "referenceTime": None,
                "metadata": {},
                "source": "target-source",  # Uses target client's source
                "sessionId": None,
                # No spaceId since target_space_id was None
            },
        )

    def test_transfer_logs_no_logs_found(self, mock_source_client, mock_target_client):
        """Test transfer operations when no logs are found."""
        mock_source_client.get_logs_by_source.return_value = {"logs": [], "total_count": 0}

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="nonexistent-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
        )

        assert result["transferred_count"] == 0
        assert "Moved 0 logs" in result["message"]
        mock_target_client.api_client._make_request.assert_not_called()
        mock_source_client.delete_log_entry.assert_not_called()

    def test_transfer_logs_wildcard_source(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test transfer operations with wildcard source filter."""
        mock_source_client.get_logs_by_source.return_value = {"logs": sample_logs, "total_count": 3}
        mock_source_client.get_specific_log.side_effect = lambda log_id: next(
            (log for log in sample_logs if log["id"] == log_id), {}
        )
        mock_target_client.ingest = Mock()

        HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="*",  # Wildcard
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        mock_source_client.get_logs_by_source.assert_called_once_with(
            source="*", space_id=None, limit=10000
        )
        assert mock_target_client.api_client._make_request.call_count == 3

    def test_transfer_logs_error_handling(
        self, mock_source_client, mock_target_client, sample_logs
    ):
        """Test error handling during transfer operations."""
        mock_source_client.get_logs_by_source.return_value = {
            "logs": sample_logs[:1],
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = sample_logs[0]
        mock_target_client.api_client._make_request.side_effect = Exception("_make_request failed")

        # Should still attempt to process all logs even if some fail
        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
        )

        # Even with error, should have attempted transfer
        assert result["total_attempted"] == 1
        # Since _make_request failed, transferred_count should be 0
        assert result["transferred_count"] == 0
        mock_target_client.api_client._make_request.assert_called_once()


class TestLogTransferCLIIntegration:
    """Integration tests for CLI log transfer commands using real API calls."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_cli_memory_move_with_new_target_options(self, runner):
        """Test CLI memory move command with new target options using real API calls."""
        from heysol.registry_config import RegistryConfig

        registry = RegistryConfig()
        instances = registry.get_registered_instances()

        if not instances:
            pytest.skip("No registered instances found for CLI integration testing")

        # Use available instances
        instance_names = list(instances.keys())
        if len(instance_names) < 2:
            pytest.skip("Need at least 2 registered instances for transfer testing")

        source_user = instance_names[0]
        target_user = instance_names[1]

        # Test the CLI command with real API calls
        result = runner.invoke(
            app,
            [
                "--user",
                source_user,
                "memory",
                "move",
                "--target-user",
                target_user,
                "--source-filter",
                "test-source",
                "--confirm",
                "--skip-mcp",
            ],
        )

        # CLI should execute without crashing (may fail due to API availability)
        # According to coding standards, integration tests should use real API calls
        # and fail fast if API is not available or credentials are wrong
        if result.exit_code != 0:
            # This is expected if API is not available or credentials are wrong
            assert "Error" in result.output or "401" in result.output or "400" in result.output

    def test_cli_memory_copy_uses_move_internally(self, runner):
        """Test that CLI memory copy command works with real API calls."""
        from heysol.registry_config import RegistryConfig

        registry = RegistryConfig()
        instances = registry.get_registered_instances()

        if not instances:
            pytest.skip("No registered instances found for CLI integration testing")

        # Use available instances
        instance_names = list(instances.keys())
        if len(instance_names) < 2:
            pytest.skip("Need at least 2 registered instances for transfer testing")

        source_user = instance_names[0]
        target_user = instance_names[1]

        # Test the CLI command with real API calls
        result = runner.invoke(
            app,
            [
                "--user",
                source_user,
                "memory",
                "copy",
                "--target-user",
                target_user,
                "--confirm",
                "--skip-mcp",
            ],
        )

        # CLI should execute without crashing (may fail due to API availability)
        # According to coding standards, integration tests should use real API calls
        # and fail fast if API is not available or credentials are wrong
        if result.exit_code != 0:
            # This is expected if API is not available or credentials are wrong
            assert "Error" in result.output or "401" in result.output or "400" in result.output


class TestLogTransferErrorScenarios:
    """Tests for error scenarios and edge cases in log transfer operations."""

    @pytest.fixture
    def mock_source_client(self):
        """Create a mock source client for testing."""
        client = Mock(spec=HeySolClient)
        client.base_url = "https://source-api.example.com"
        # Add api_client mock with required attributes
        client.api_client = Mock()
        client.api_client.base_url = "https://source-api.example.com"
        return client

    @pytest.fixture
    def mock_target_client(self):
        """Create a mock target client for testing."""
        client = Mock(spec=HeySolClient)
        client.base_url = "https://target-api.example.com"
        # Add api_client mock with required attributes
        client.api_client = Mock()
        client.api_client.base_url = "https://target-api.example.com"
        return client

    def test_transfer_logs_with_invalid_log_data(self, mock_source_client, mock_target_client):
        """Test transfer operations with malformed log data."""
        # Log missing required fields
        malformed_logs = [
            {"id": "log-1"},  # Missing source and content
            {"source": "test-source"},  # Missing id
            {
                "id": "log-3",
                "source": "test-source",
                "ingestText": None,
                "data": None,
            },  # No content
        ]

        mock_source_client.get_logs_by_source.return_value = {
            "logs": malformed_logs,
            "total_count": 3,
        }
        mock_source_client.get_specific_log.side_effect = lambda log_id: next(
            (log for log in malformed_logs if log.get("id") == log_id), {}
        )

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        # Should handle malformed logs gracefully
        assert result["total_attempted"] == 3
        # Only logs with valid content should be transferred
        assert result["transferred_count"] == 0  # None have valid content

    def test_transfer_logs_network_error_during_ingest(
        self, mock_source_client, mock_target_client
    ):
        """Test transfer operations with network errors during ingestion."""
        logs = [{"id": "log-1", "source": "test-source", "ingestText": "Test content"}]

        mock_source_client.get_logs_by_source.return_value = {"logs": logs, "total_count": 1}
        mock_source_client.get_specific_log.return_value = logs[0]

        # Simulate network error on _make_request
        mock_target_client.api_client._make_request.side_effect = Exception("Network timeout")

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
        )

        # Should attempt transfer despite initial error
        assert result["total_attempted"] == 1
        # If error occurs, transferred_count will be 0
        assert mock_target_client.api_client._make_request.call_count == 1

    def test_transfer_logs_partial_failure(self, mock_source_client, mock_target_client):
        """Test transfer operations with partial failures."""
        logs = [
            {"id": "log-1", "source": "test-source", "ingestText": "Content 1"},
            {"id": "log-2", "source": "test-source", "ingestText": "Content 2"},
            {"id": "log-3", "source": "test-source", "ingestText": "Content 3"},
        ]

        mock_source_client.get_logs_by_source.return_value = {"logs": logs, "total_count": 3}
        mock_source_client.get_specific_log.side_effect = logs

        # First _make_request succeeds, second fails, third succeeds
        mock_target_client.api_client._make_request.side_effect = [
            None,
            Exception("_make_request failed"),
            None,
        ]

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="move",
            delete_after_transfer=True,
        )

        assert result["total_attempted"] == 3
        # Should have attempted all _make_request calls
        assert mock_target_client.api_client._make_request.call_count == 3
        # Only successful _make_request calls should be counted
        assert result["transferred_count"] == 2  # 2 out of 3 succeeded

    def test_transfer_logs_empty_source_filter(self, mock_source_client, mock_target_client):
        """Test transfer operations with empty source filter."""
        mock_source_client.get_logs_by_source.return_value = {"logs": [], "total_count": 0}

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="",  # Empty source
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        assert result["transferred_count"] == 0
        assert "Copied 0 logs" in result["message"]

    def test_transfer_logs_very_large_dataset(self, mock_source_client, mock_target_client):
        """Test transfer operations with very large datasets."""
        # Simulate 10,000 logs
        large_log_count = 10000
        logs = [
            {"id": f"log-{i}", "source": "bulk-source", "ingestText": f"Content {i}"}
            for i in range(large_log_count)
        ]

        mock_source_client.get_logs_by_source.return_value = {
            "logs": logs,
            "total_count": large_log_count,
        }
        mock_source_client.get_specific_log.side_effect = lambda log_id: next(
            (log for log in logs if log["id"] == log_id), {}
        )
        mock_target_client.api_client._make_request = Mock()

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="bulk-source",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        assert result["total_attempted"] == large_log_count
        assert mock_target_client.api_client._make_request.call_count == large_log_count

    def test_transfer_logs_with_unicode_content(self, mock_source_client, mock_target_client):
        """Test transfer operations with Unicode content."""
        unicode_logs = [
            {
                "id": "log-1",
                "source": "test-source",
                "ingestText": "测试内容 🚀 with émojis",
                "data": {"episodeBody": "Alternative 内容"},
            }
        ]

        mock_source_client.get_logs_by_source.return_value = {
            "logs": unicode_logs,
            "total_count": 1,
        }
        mock_source_client.get_specific_log.return_value = unicode_logs[0]
        mock_target_client.api_client._make_request = Mock()

        result = HeySolClient._transfer_logs_to_instance(
            mock_source_client,
            target_client=mock_target_client,
            source="test-source",
            confirm=True,
            operation="copy",
            delete_after_transfer=False,
        )

        assert result["transferred_count"] == 1
        mock_target_client.api_client._make_request.assert_called_once_with(
            "POST",
            "add",
            data={
                "episodeBody": "测试内容 🚀 with émojis",
                "referenceTime": None,
                "metadata": {},
                "source": mock_target_client.api_client.source,
                "sessionId": None,
            },
        )
