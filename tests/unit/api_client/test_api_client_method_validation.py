#!/usr/bin/env python3
"""
Unit tests for HeySolAPIClient method validation.

Tests API client method input validation following fail-fast principles.
"""

import pytest
from unittest.mock import Mock, patch

from heysol.clients.api_client import HeySolAPIClient
from heysol.exceptions import ValidationError


def test_ingest_with_empty_message():
    """Test ingest method with empty message."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Message is required"):
            client.ingest("")


def test_ingest_with_whitespace_only_message():
    """Test ingest method with whitespace-only message."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Message is required"):
            client.ingest("   ")


def test_ingest_with_none_message():
    """Test ingest method with None message."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Message is required"):
            client.ingest(None)


def test_ingest_with_valid_message():
    """Test ingest method with valid message."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.ingest("valid message")
        assert result == {"success": True}


def test_search_with_empty_query():
    """Test search method with empty query."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Search query is required"):
            client.search("")


def test_search_with_whitespace_only_query():
    """Test search method with whitespace-only query."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Search query is required"):
            client.search("   ")


def test_search_with_none_query():
    """Test search method with None query."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Search query is required"):
            client.search(None)


def test_search_with_valid_query():
    """Test search method with valid query."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"episodes": []}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.search("valid query")
        assert result == {"episodes": []}


def test_create_space_with_empty_name():
    """Test create_space method with empty name."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Space name is required"):
            client.create_space("")


def test_create_space_with_whitespace_only_name():
    """Test create_space method with whitespace-only name."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Space name is required"):
            client.create_space("   ")


def test_create_space_with_none_name():
    """Test create_space method with None name."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Space name is required"):
            client.create_space(None)


def test_create_space_with_valid_name():
    """Test create_space method with valid name."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "space-123"}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.create_space("valid space name")
        assert result == {"id": "space-123"}


def test_get_episode_facts_with_empty_id():
    """Test get_episode_facts method with empty episode ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Episode ID is required"):
            client.get_episode_facts("")


def test_get_episode_facts_with_invalid_format():
    """Test get_episode_facts method with invalid ID format."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Invalid episode ID format"):
            client.get_episode_facts("invalid")


def test_get_episode_facts_with_valid_id():
    """Test get_episode_facts method with valid ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"facts": []}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.get_episode_facts("valid-episode-id")
        assert result == {"facts": []}


def test_get_specific_log_with_empty_id():
    """Test get_specific_log method with empty log ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Log ID is required"):
            client.get_specific_log("")


def test_get_specific_log_with_invalid_format():
    """Test get_specific_log method with invalid ID format."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Invalid log ID format"):
            client.get_specific_log("invalid")


def test_get_specific_log_with_valid_id():
    """Test get_specific_log method with valid ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"log": {"id": "log-123"}}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.get_specific_log("valid-log-id")
        assert result == {"log": {"id": "log-123"}}


def test_get_space_details_with_empty_id():
    """Test get_space_details method with empty space ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Space ID is required"):
            client.get_space_details("")


def test_get_space_details_with_invalid_format():
    """Test get_space_details method with invalid space ID format."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Invalid space ID format"):
            client.get_space_details("test")


def test_get_space_details_with_valid_id():
    """Test get_space_details method with valid ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"space": {"id": "space-123"}}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.get_space_details("valid-space-id")
        assert result == {"space": {"id": "space-123"}}


def test_update_space_without_fields():
    """Test update_space method without any fields to update."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="At least one field must be provided"):
            client.update_space("space-id")


def test_update_space_with_empty_name():
    """Test update_space method with empty name."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Space name cannot be empty"):
            client.update_space("space-id", name="")


def test_update_space_with_valid_fields():
    """Test update_space method with valid fields."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"space": {"id": "space-123", "name": "updated"}}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.update_space("space-id", name="updated name")
        assert result == {"space": {"id": "space-123", "name": "updated"}}


def test_delete_space_without_confirm():
    """Test delete_space method without confirmation."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="requires confirmation"):
            client.delete_space("space-id", confirm=False)


def test_delete_space_with_confirm():
    """Test delete_space method with confirmation."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.delete_space("space-id", confirm=True)
        assert result == {"success": True}


def test_register_webhook_without_url():
    """Test register_webhook method without URL."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Webhook URL is required"):
            client.register_webhook("", events=["test"], secret="secret")


def test_register_webhook_without_secret():
    """Test register_webhook method without secret."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Webhook secret is required"):
            client.register_webhook("https://test.com", events=["test"], secret="")


def test_register_webhook_without_events():
    """Test register_webhook method without events."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Webhook events are required"):
            client.register_webhook("https://test.com", events=[], secret="secret")


def test_register_webhook_with_valid_parameters():
    """Test register_webhook method with valid parameters."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "webhook-123"}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.register_webhook("https://test.com", events=["test"], secret="secret")
        assert result == {"id": "webhook-123"}


def test_get_webhook_with_empty_id():
    """Test get_webhook method with empty webhook ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Webhook ID is required"):
            client.get_webhook("")


def test_get_webhook_with_invalid_format():
    """Test get_webhook method with invalid webhook ID format."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Invalid webhook ID format"):
            client.get_webhook("invalid")


def test_get_webhook_with_valid_id():
    """Test get_webhook method with valid ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"webhook": {"id": "webhook-123"}}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.get_webhook("valid-webhook-id")
        assert result == {"webhook": {"id": "webhook-123"}}


def test_update_webhook_validation():
    """Test update_webhook method validation."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

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


def test_update_webhook_with_valid_parameters():
    """Test update_webhook method with valid parameters."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"webhook": {"id": "webhook-123"}}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.update_webhook("webhook-id", "https://test.com", ["test"], "secret")
        assert result == {"webhook": {"id": "webhook-123"}}


def test_delete_webhook_without_confirm():
    """Test delete_webhook method without confirmation."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="requires confirmation"):
            client.delete_webhook("webhook-id", confirm=False)


def test_delete_webhook_with_confirm():
    """Test delete_webhook method with confirmation."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.delete_webhook("webhook-id", confirm=True)
        assert result == {"success": True}


def test_delete_log_entry_with_empty_id():
    """Test delete_log_entry method with empty log ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Log ID is required"):
            client.delete_log_entry("")


def test_delete_log_entry_with_invalid_format():
    """Test delete_log_entry method with invalid ID format."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        with pytest.raises(ValidationError, match="Invalid log ID format"):
            client.delete_log_entry("invalid")


def test_delete_log_entry_with_valid_id():
    """Test delete_log_entry method with valid ID."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception
        result = client.delete_log_entry("valid-log-id")
        assert result == {"success": True}


def test_copy_log_entry_with_missing_content():
    """Test copy_log_entry with log entry missing content."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Log entry without content
        log_entry = {"id": "1", "source": "test"}

        with pytest.raises(ValidationError, match="must contain message content"):
            client.copy_log_entry(log_entry)


def test_copy_log_entry_with_empty_content():
    """Test copy_log_entry with log entry with empty content."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Log entry with empty content
        log_entry = {"id": "1", "source": "test", "content": ""}

        with pytest.raises(ValidationError, match="must contain message content"):
            client.copy_log_entry(log_entry)


def test_copy_log_entry_with_valid_content():
    """Test copy_log_entry with valid content."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config, \
         patch('heysol.clients.api_client.requests.request') as mock_request:

        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Log entry with valid content
        log_entry = {"id": "1", "source": "test", "content": "valid message"}

        # Should not raise exception
        result = client.copy_log_entry(log_entry)
        assert result == {"success": True}