"""
Unit tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError

from heysol.models import (
    CreateSpaceRequest,
    HeySolConfig,
    IngestRequest,
    RegisterWebhookRequest,
    SearchRequest,
    UpdateSpaceRequest,
    UpdateWebhookRequest,
)


class TestHeySolConfig:
    """Test HeySolConfig model."""

    def test_valid_config(self):
        """Test valid configuration creation."""
        config = HeySolConfig(
            api_key="rc_pat_test123",
            base_url="https://api.example.com",
            source="test-source",
            timeout=30,
        )
        assert config.api_key == "rc_pat_test123"
        assert config.base_url == "https://api.example.com"
        assert config.source == "test-source"
        assert config.timeout == 30

    def test_invalid_api_key_format(self):
        """Test invalid API key format validation."""
        with pytest.raises(ValidationError, match="API key must start with 'rc_pat_'"):
            HeySolConfig(api_key="invalid_key")

    def test_timeout_validation(self):
        """Test timeout validation."""
        with pytest.raises(ValidationError):
            HeySolConfig(timeout=0)

        with pytest.raises(ValidationError):
            HeySolConfig(timeout=400)

    def test_from_env(self):
        """Test configuration from environment variables."""
        import os

        # Set environment variables
        os.environ["HEYSOL_API_KEY"] = "rc_pat_env_test"
        os.environ["HEYSOL_BASE_URL"] = "https://env.example.com"
        os.environ["HEYSOL_TIMEOUT"] = "45"

        try:
            config = HeySolConfig.from_env()
            assert config.api_key == "rc_pat_env_test"
            assert config.base_url == "https://env.example.com"
            assert config.timeout == 45
        finally:
            # Clean up
            del os.environ["HEYSOL_API_KEY"]
            del os.environ["HEYSOL_BASE_URL"]
            del os.environ["HEYSOL_TIMEOUT"]


class TestIngestRequest:
    """Test IngestRequest model."""

    def test_valid_ingest_request(self):
        """Test valid ingest request creation."""
        request = IngestRequest(
            episode_body="Test content",
            source="test-source",
            session_id="session-123",
            space_id="space-456",
        )
        assert request.episode_body == "Test content"
        assert request.source == "test-source"
        assert request.session_id == "session-123"
        assert request.space_id == "space-456"

    def test_ingest_request_validation(self):
        """Test ingest request validation."""
        with pytest.raises(ValidationError, match="episode_body"):
            IngestRequest(episode_body="", source="test")

        with pytest.raises(ValidationError, match="source"):
            IngestRequest(episode_body="content", source="")

    def test_ingest_request_defaults(self):
        """Test ingest request default values."""
        request = IngestRequest(episode_body="content", source="test")
        assert request.session_id == ""
        assert request.space_id is None
        assert request.metadata == {}


class TestSearchRequest:
    """Test SearchRequest model."""

    def test_valid_search_request(self):
        """Test valid search request creation."""
        request = SearchRequest(
            query="test query",
            space_ids=["space1", "space2"],
            include_invalidated=True,
        )
        assert request.query == "test query"
        assert request.space_ids == ["space1", "space2"]
        assert request.include_invalidated is True

    def test_search_request_validation(self):
        """Test search request validation."""
        with pytest.raises(ValidationError, match="query"):
            SearchRequest(query="", space_ids=[])

    def test_search_request_defaults(self):
        """Test search request default values."""
        request = SearchRequest(query="test")
        assert request.space_ids == []
        assert request.include_invalidated is False


class TestCreateSpaceRequest:
    """Test CreateSpaceRequest model."""

    def test_valid_create_space_request(self):
        """Test valid create space request."""
        request = CreateSpaceRequest(name="Test Space", description="A test space")
        assert request.name == "Test Space"
        assert request.description == "A test space"

    def test_create_space_validation(self):
        """Test create space request validation."""
        with pytest.raises(ValidationError, match="name"):
            CreateSpaceRequest(name="", description="test")

    def test_create_space_defaults(self):
        """Test create space request defaults."""
        request = CreateSpaceRequest(name="Test")
        assert request.description == ""


class TestUpdateSpaceRequest:
    """Test UpdateSpaceRequest model."""

    def test_valid_update_space_request(self):
        """Test valid update space request."""
        request = UpdateSpaceRequest(
            name="New Name",
            description="New description",
            metadata={"key": "value"},
        )
        assert request.name == "New Name"
        assert request.description == "New description"
        assert request.metadata == {"key": "value"}

    def test_update_space_optional_fields(self):
        """Test update space request with optional fields."""
        request = UpdateSpaceRequest(name="New Name")
        assert request.name == "New Name"
        assert request.description is None
        assert request.metadata is None


class TestRegisterWebhookRequest:
    """Test RegisterWebhookRequest model."""

    def test_valid_register_webhook_request(self):
        """Test valid register webhook request."""
        request = RegisterWebhookRequest(
            url="https://example.com/webhook",
            secret="webhook-secret-123",
        )
        assert str(request.url) == "https://example.com/webhook"
        assert request.secret == "webhook-secret-123"

    def test_register_webhook_validation(self):
        """Test register webhook request validation."""
        with pytest.raises(ValidationError, match="Input should be a valid URL"):
            RegisterWebhookRequest(url="invalid-url", secret="secret")

        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            RegisterWebhookRequest(url="https://example.com", secret="")


class TestUpdateWebhookRequest:
    """Test UpdateWebhookRequest model."""

    def test_valid_update_webhook_request(self):
        """Test valid update webhook request."""
        request = UpdateWebhookRequest(
            url="https://example.com/webhook",
            events=["push", "pull_request"],
            secret="secret-123",
            active=False,
        )
        assert str(request.url) == "https://example.com/webhook"
        assert request.events == ["push", "pull_request"]
        assert request.secret == "secret-123"
        assert request.active is False

    def test_update_webhook_events_validation(self):
        """Test update webhook events validation."""
        with pytest.raises(ValidationError, match="Events list cannot be empty"):
            UpdateWebhookRequest(
                url="https://example.com",
                events=[],
                secret="secret",
            )

    def test_update_webhook_validation(self):
        """Test update webhook request validation."""
        with pytest.raises(ValidationError, match="Input should be a valid URL"):
            UpdateWebhookRequest(url="invalid-url", events=["push"], secret="secret")

        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            UpdateWebhookRequest(url="https://example.com", events=["push"], secret="")