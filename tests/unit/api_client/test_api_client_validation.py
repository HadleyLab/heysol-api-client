#!/usr/bin/env python3
"""
Unit tests for HeySolAPIClient validation methods.

Tests API client validation following fail-fast principles.
"""

import pytest
from unittest.mock import Mock, patch

from heysol.clients.api_client import HeySolAPIClient
from heysol.exceptions import ValidationError


def test_is_valid_id_format_valid_ids():
    """Test _is_valid_id_format with valid ID formats."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Valid IDs
        assert client._is_valid_id_format("valid-id-123") is True
        assert client._is_valid_id_format("cmg2ulh5r06kanx1vn3sshzrx") is True
        assert client._is_valid_id_format("test_id_123") is True
        assert client._is_valid_id_format("a1b2c3d4e5f6") is True


def test_is_valid_id_format_invalid_ids():
    """Test _is_valid_id_format with invalid ID formats."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Invalid IDs
        assert client._is_valid_id_format("") is False
        assert client._is_valid_id_format("   ") is False
        assert client._is_valid_id_format("invalid") is False
        assert client._is_valid_id_format("test") is False
        assert client._is_valid_id_format("ab") is False  # Too short
        assert client._is_valid_id_format("a") is False  # Too short


def test_is_valid_id_format_edge_cases():
    """Test _is_valid_id_format with edge cases."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Edge cases
        assert client._is_valid_id_format("a") is False  # Single character
        assert client._is_valid_id_format("ab") is False  # Two characters
        assert client._is_valid_id_format("abc") is True  # Three characters - minimum valid
        assert client._is_valid_id_format("test-id_with_underscores") is True
        assert client._is_valid_id_format("test.id.with.dots") is True
        assert client._is_valid_id_format("test-id-123-456") is True


def test_is_valid_id_format_unicode_characters():
    """Test _is_valid_id_format with unicode characters."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Unicode IDs
        assert client._is_valid_id_format("tëst_ïd") is True
        assert client._is_valid_id_format("测试_id") is True
        assert client._is_valid_id_format("тест-id") is True


def test_is_valid_id_format_special_characters():
    """Test _is_valid_id_format with special characters."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Special characters
        assert client._is_valid_id_format("test@id") is True
        assert client._is_valid_id_format("test#id") is True
        assert client._is_valid_id_format("test$id") is True
        assert client._is_valid_id_format("test%id") is True
        assert client._is_valid_id_format("test&id") is True


def test_validate_api_key_format_valid_keys():
    """Test API key format validation with valid keys."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Should not raise exception for valid keys
        assert client.api_key == "rc_pat_test_key_for_testing_12345678901234567890"


def test_validate_api_key_format_invalid_length():
    """Test API key format validation with invalid length."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "short_key"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        with pytest.raises(ValidationError, match="Invalid API key length"):
            HeySolAPIClient(api_key="short_key", base_url="https://test.com")


def test_validate_api_key_format_invalid_prefix():
    """Test API key format validation with invalid prefix."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "invalid_prefix_123456789012345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        with pytest.raises(ValidationError, match="Invalid API key format"):
            HeySolAPIClient(api_key="invalid_prefix_123456789012345678901234567890", base_url="https://test.com")


def test_validate_api_key_format_empty_key():
    """Test API key format validation with empty key."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = ""
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        # Empty key should be allowed (validation happens at usage)
        client = HeySolAPIClient(api_key="", base_url="https://test.com")
        assert client.api_key == ""


def test_validate_api_key_format_none_key():
    """Test API key format validation with None key."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = None
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        # None key should be allowed (validation happens at usage)
        client = HeySolAPIClient(api_key=None, base_url="https://test.com")
        assert client.api_key is None


def test_validate_api_key_format_boundary_lengths():
    """Test API key format validation with boundary lengths."""
    # Test minimum valid length (40 characters)
    min_valid_key = "rc_pat_test_key_for_testing_1234567890"  # 40 characters

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = min_valid_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=min_valid_key, base_url="https://test.com")
        assert client.api_key == min_valid_key

    # Test maximum valid length (60 characters)
    max_valid_key = "rc_pat_test_key_for_testing_123456789012345678901234567890"  # 60 characters

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = max_valid_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=max_valid_key, base_url="https://test.com")
        assert client.api_key == max_valid_key


def test_validate_api_key_format_various_valid_prefixes():
    """Test API key format validation with various valid prefixes."""
    valid_prefixes = [
        "rc_pat_",
        "rc_svc_",
        "rc_oauth_",
        "rc_token_"
    ]

    for prefix in valid_prefixes:
        # Create a key with valid length
        valid_key = prefix + "test_key_for_testing_12345678901234567890"

        with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.api_key = valid_key
            mock_config_instance.base_url = "https://test.com"
            mock_config.from_env.return_value = mock_config_instance

            client = HeySolAPIClient(api_key=valid_key, base_url="https://test.com")
            assert client.api_key == valid_key


def test_validate_api_key_format_case_sensitivity():
    """Test API key format validation case sensitivity."""
    # Test uppercase prefix
    upper_key = "RC_PAT_TEST_KEY_FOR_TESTING_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = upper_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=upper_key, base_url="https://test.com")
        assert client.api_key == upper_key

    # Test mixed case prefix
    mixed_key = "Rc_Pat_Test_Key_For_Testing_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = mixed_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=mixed_key, base_url="https://test.com")
        assert client.api_key == mixed_key


def test_validate_api_key_format_with_unicode():
    """Test API key format validation with unicode characters."""
    unicode_key = "rc_pat_tëst_këy_för_tësting_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = unicode_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=unicode_key, base_url="https://test.com")
        assert client.api_key == unicode_key


def test_validate_api_key_format_with_special_characters():
    """Test API key format validation with special characters."""
    special_key = "rc_pat_test_key!@#$%^&*()_for_testing_12345678901234567890"

    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = special_key
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key=special_key, base_url="https://test.com")
        assert client.api_key == special_key


def test_validate_required_parameters_empty_string():
    """Test validation of required parameters with empty string."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Empty string should be considered invalid for required parameters
        assert client._validate_required("") is False
        assert client._validate_required("   ") is False
        assert client._validate_required("valid_param") is True
        assert client._validate_required(None) is False


def test_validate_required_parameters_with_none():
    """Test validation of required parameters with None."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # None should be considered invalid for required parameters
        assert client._validate_required(None) is False
        assert client._validate_required("valid_param") is True
        assert client._validate_required(0) is True  # Zero is valid
        assert client._validate_required(False) is True  # False is valid


def test_validate_required_parameters_with_whitespace():
    """Test validation of required parameters with whitespace."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Whitespace-only strings should be invalid
        assert client._validate_required("   ") is False
        assert client._validate_required("\t") is False
        assert client._validate_required("\n") is False
        assert client._validate_required(" \t \n ") is False
        assert client._validate_required(" valid ") is True  # Valid with whitespace around


def test_validate_required_parameters_with_numbers():
    """Test validation of required parameters with numeric values."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Numbers should be valid
        assert client._validate_required(0) is True
        assert client._validate_required(42) is True
        assert client._validate_required(-1) is True
        assert client._validate_required(3.14) is True


def test_validate_required_parameters_with_booleans():
    """Test validation of required parameters with boolean values."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Booleans should be valid
        assert client._validate_required(True) is True
        assert client._validate_required(False) is True


def test_validate_required_parameters_with_lists():
    """Test validation of required parameters with list values."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Lists should be valid
        assert client._validate_required([]) is True
        assert client._validate_required(["item1", "item2"]) is True
        assert client._validate_required([1, 2, 3]) is True


def test_validate_required_parameters_with_dicts():
    """Test validation of required parameters with dictionary values."""
    with patch('heysol.clients.api_client.HeySolConfig') as mock_config:
        mock_config_instance = Mock()
        mock_config_instance.api_key = "rc_pat_test_key_for_testing_12345678901234567890"
        mock_config_instance.base_url = "https://test.com"
        mock_config.from_env.return_value = mock_config_instance

        client = HeySolAPIClient(api_key="rc_pat_test_key_for_testing_12345678901234567890", base_url="https://test.com")

        # Dictionaries should be valid
        assert client._validate_required({}) is True
        assert client._validate_required({"key": "value"}) is True
        assert client._validate_required({"nested": {"key": "value"}}) is True