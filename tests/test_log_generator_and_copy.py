"""
Tests for the new log generator and metadata-preserving copy functionality.

Tests the memory-efficient log processing, metadata preservation, and CLI integration.
Follows coding standards: unit tests primary, integration tests for APIs, fail fast.
"""

from unittest.mock import Mock, patch

import pytest

from heysol import HeySolClient
from heysol.exceptions import ValidationError


class TestLogGenerator:
    """Test the iter_ingestion_logs generator functionality."""

    def test_iter_ingestion_logs_basic(self):
        """Test basic generator functionality."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.iter_ingestion_logs.return_value = iter([
                {"id": "1", "source": "test"},
                {"id": "2", "source": "test"},
                {"id": "3", "source": "test"}
            ])
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            logs = list(client.iter_ingestion_logs())

            assert len(logs) == 3
            assert logs[0]["id"] == "1"
            assert logs[1]["id"] == "2"
            assert logs[2]["id"] == "3"

    def test_iter_ingestion_logs_with_filters(self):
        """Test generator with status and space filters."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.iter_ingestion_logs.return_value = iter([
                {"id": "1", "source": "test", "status": "COMPLETED"}
            ])
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            logs = list(client.iter_ingestion_logs(status="COMPLETED"))

            assert len(logs) == 1
            assert logs[0]["id"] == "1"
            assert logs[0]["status"] == "COMPLETED"

    def test_iter_ingestion_logs_empty_result(self):
        """Test generator with no data."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.iter_ingestion_logs.return_value = iter([])
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            logs = list(client.iter_ingestion_logs())

            assert len(logs) == 0


class TestLogSourceFiltering:
    """Test the get_logs_by_source method with generator."""

    def test_get_logs_by_source_basic(self):
        """Test basic source filtering."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.get_logs_by_source.return_value = [
                {"id": "1", "source": "kilo-code"},
                {"id": "3", "source": "kilo-code"},
            ]
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            result = client.get_logs_by_source("kilo-code")

            assert len(result) == 2
            assert result[0]["source"] == "kilo-code"
            assert result[1]["source"] == "kilo-code"

    def test_get_logs_by_source_with_limit(self):
        """Test source filtering with limit."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.get_logs_by_source.return_value = [
                {"id": "1", "source": "test"},
                {"id": "2", "source": "test"},
            ]
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            result = client.get_logs_by_source("test", limit=2)

            assert len(result) == 2
            assert result[0]["id"] == "1"
            assert result[1]["id"] == "2"

    def test_get_logs_by_source_with_offset(self):
        """Test source filtering with offset."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.get_logs_by_source.return_value = [
                {"id": "2", "source": "test"},
            ]
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()
            result = client.get_logs_by_source("test", offset=1, limit=1)

            assert len(result) == 1
            assert result[0]["id"] == "2"

    def test_get_logs_by_source_invalid_source(self):
        """Test source filtering with empty source fails fast."""
        client = HeySolClient()

        with pytest.raises(ValidationError, match="Source is required"):
            client.get_logs_by_source("")


class TestMetadataPreservingCopy:
    """Test the copy_log_entry method for metadata preservation."""

    def test_copy_log_entry_basic(self):
        """Test basic copy functionality with metadata preservation."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.copy_log_entry.return_value = {"success": True, "id": "new-log-id"}
            mock_api_class.return_value = mock_api_instance

            original_log = {
                "id": "original-id",
                "source": "kilo-code",
                "ingestText": "Test message",
                "time": "2025-09-27T13:20:13.507Z",
                "data": {
                    "type": "CONVERSATION",
                    "source": "kilo-code",
                    "metadata": {"priority": "high"},
                    "sessionId": "session-123",
                    "episodeBody": "Test message",
                    "referenceTime": "2025-09-27T13:20:13.496Z",
                },
            }

            client = HeySolClient()
            result = client.copy_log_entry(original_log, new_source="test-copy")

            assert result["success"] is True
            assert result["id"] == "new-log-id"

            # Verify the API call was made with correct parameters
            mock_api_instance.copy_log_entry.assert_called_once()
            call_args = mock_api_instance.copy_log_entry.call_args
            assert call_args[1]["new_source"] == "test-copy"

    def test_copy_log_entry_with_overrides(self):
        """Test copy with metadata overrides."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.copy_log_entry.return_value = {"success": True}
            mock_api_class.return_value = mock_api_instance

            original_log = {
                "source": "kilo-code",
                "ingestText": "Test message",
                "data": {"metadata": {"original": "value"}, "sessionId": "old-session"},
            }

            client = HeySolClient()
            result = client.copy_log_entry(
                original_log,
                new_source="new-source",
                new_session_id="new-session",
                override_metadata={"priority": "high", "category": "test"},
            )

            assert result["success"] is True

            # Verify the API call was made with correct parameters
            mock_api_instance.copy_log_entry.assert_called_once()
            call_args = mock_api_instance.copy_log_entry.call_args
            assert call_args[1]["new_source"] == "new-source"
            assert call_args[1]["new_session_id"] == "new-session"
            assert call_args[1]["override_metadata"] == {"priority": "high", "category": "test"}

    def test_copy_log_entry_missing_content(self):
        """Test copy fails fast with missing content."""
        client = HeySolClient()

        with pytest.raises(ValidationError, match="Log entry must contain message content"):
            client.copy_log_entry({"id": "test"})

    def test_copy_log_entry_empty_log(self):
        """Test copy fails fast with empty log."""
        client = HeySolClient()

        with pytest.raises(ValidationError, match="Log entry is required"):
            client.copy_log_entry(None)


class TestIntegrationWithLiveAPI:
    """Integration tests using live API calls as per coding standards."""

    def test_get_logs_by_source_integration(self):
        """Test source filtering with live API."""
        client = HeySolClient()

        try:
            # Test with existing source
            result = client.get_logs_by_source("kilo-code", limit=5)
            assert isinstance(result, list)

            # All returned logs should have the correct source
            for log in result:
                assert log.get("source") == "kilo-code"

        finally:
            client.close()

    def test_iter_ingestion_logs_integration(self):
        """Test generator with live API."""
        client = HeySolClient()

        try:
            count = 0
            sources = set()

            for log in client.iter_ingestion_logs():
                count += 1
                sources.add(log.get("source", "unknown"))

                if count >= 10:  # Limit for testing
                    break

            assert count > 0
            assert len(sources) > 0

        finally:
            client.close()

    def test_copy_log_entry_integration(self):
        """Test metadata-preserving copy with live API."""
        client = HeySolClient()

        try:
            # Get an existing log to copy
            logs = client.get_logs_by_source("kilo-code", limit=1)
            if logs:
                original_log = logs[0]

                # Copy the log
                result = client.copy_log_entry(original_log, new_source="test-copy-integration")

                assert result is not None

        finally:
            client.close()


class TestErrorHandling:
    """Test error handling follows fail-fast principles."""

    def test_invalid_source_raises_error(self):
        """Test that invalid source raises ValidationError immediately."""
        client = HeySolClient()

        with pytest.raises(ValidationError):
            client.get_logs_by_source("")

    def test_copy_with_invalid_log_raises_error(self):
        """Test that copy with invalid log fails fast."""
        client = HeySolClient()

        with pytest.raises(ValidationError):
            client.copy_log_entry({})

    def test_generator_handles_api_errors(self):
        """Test that generator handles API errors appropriately."""
        with patch("heysol.client.HeySolAPIClient") as mock_api_class:
            mock_api_instance = Mock()
            mock_api_instance.get_ingestion_logs.side_effect = Exception("API Error")
            mock_api_class.return_value = mock_api_instance

            client = HeySolClient()

            with pytest.raises(Exception):
                list(client.iter_ingestion_logs())
