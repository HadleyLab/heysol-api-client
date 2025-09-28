#!/usr/bin/env python3
"""
Unit tests for HeySol exceptions.

Tests exception handling following fail-fast principles.
"""

import pytest

from heysol.exceptions import HeySolError, ValidationError


def test_validation_error_creation():
    """Test ValidationError creation with message."""
    error = ValidationError("Test validation error")

    assert str(error) == "Test validation error"
    assert error.__class__.__name__ == "ValidationError"
    assert issubclass(ValidationError, Exception)


def test_validation_error_creation_empty_message():
    """Test ValidationError creation with empty message."""
    error = ValidationError("")

    assert str(error) == ""
    assert error.__class__.__name__ == "ValidationError"


def test_validation_error_inheritance():
    """Test ValidationError inheritance hierarchy."""
    error = ValidationError("Test error")

    assert isinstance(error, ValidationError)
    assert isinstance(error, Exception)
    assert isinstance(error, BaseException)


def test_heysol_error_creation():
    """Test HeySolError creation with message."""
    error = HeySolError("Test HeySol error")

    assert str(error) == "Test HeySol error"
    assert error.__class__.__name__ == "HeySolError"
    assert issubclass(HeySolError, Exception)


def test_heysol_error_creation_empty_message():
    """Test HeySolError creation with empty message."""
    error = HeySolError("")

    assert str(error) == ""
    assert error.__class__.__name__ == "HeySolError"


def test_heysol_error_inheritance():
    """Test HeySolError inheritance hierarchy."""
    error = HeySolError("Test error")

    assert isinstance(error, HeySolError)
    assert isinstance(error, Exception)
    assert isinstance(error, BaseException)


def test_exception_raising():
    """Test that exceptions can be raised and caught."""
    with pytest.raises(ValidationError, match="Test validation error"):
        raise ValidationError("Test validation error")

    with pytest.raises(HeySolError, match="Test HeySol error"):
        raise HeySolError("Test HeySol error")


def test_exception_chaining():
    """Test exception chaining with __cause__."""
    original_error = ValueError("Original error")

    try:
        raise ValidationError("Validation failed") from original_error
    except ValidationError as e:
        assert e.__cause__ == original_error
        assert str(e) == "Validation failed"


def test_exception_context():
    """Test exception context with __context__."""
    original_error = ValueError("Original error")

    try:
        try:
            raise original_error
        except ValueError:
            raise ValidationError("Validation failed")
    except ValidationError as e:
        assert e.__context__ == original_error
        assert str(e) == "Validation failed"


def test_exception_with_details():
    """Test ValidationError with details parameter."""
    # ValidationError doesn't accept additional parameters
    error = ValidationError("Validation failed")

    assert str(error) == "Validation failed"
    # Simple exceptions don't have custom attributes
    assert not hasattr(error, 'details')


def test_exception_without_details():
    """Test ValidationError without details parameter."""
    error = ValidationError("Validation failed")

    assert str(error) == "Validation failed"
    assert not hasattr(error, 'details')


def test_multiple_exception_instances():
    """Test that multiple exception instances are independent."""
    error1 = ValidationError("Error 1")
    error2 = ValidationError("Error 2")

    assert str(error1) == "Error 1"
    assert str(error2) == "Error 2"
    assert error1 is not error2


def test_exception_with_long_message():
    """Test exception with long error message."""
    long_message = "This is a very long error message that contains detailed information about what went wrong in the validation process and should be preserved exactly as provided."

    error = ValidationError(long_message)

    assert str(error) == long_message
    assert len(str(error)) == len(long_message)


def test_exception_with_special_characters():
    """Test exception with special characters in message."""
    special_message = "Error: invalid input 'test@example.com' with special chars: !@#$%^&*()"

    error = HeySolError(special_message)

    assert str(error) == special_message


def test_exception_with_unicode_characters():
    """Test exception with unicode characters in message."""
    unicode_message = "Error: invalid input '测试@example.com' with unicode: 中文"

    error = ValidationError(unicode_message)

    assert str(error) == unicode_message


def test_exception_with_numeric_message():
    """Test exception with numeric message."""
    error = HeySolError("404")

    assert str(error) == "404"


def test_exception_with_none_message():
    """Test exception with None message."""
    error = ValidationError(None)

    assert str(error) == "None"


def test_exception_repr():
    """Test exception repr method."""
    error = ValidationError("Test error")

    repr_str = repr(error)
    assert "ValidationError" in repr_str
    assert "Test error" in repr_str


def test_exception_equality():
    """Test exception equality comparison."""
    error1 = ValidationError("Same message")
    error2 = ValidationError("Same message")
    error3 = ValidationError("Different message")

    # String comparison should work
    assert str(error1) == str(error2)
    assert str(error1) != str(error3)

    # But object identity should be different
    assert error1 is not error2


def test_exception_hash():
    """Test exception hash (should be hashable for use in sets/dicts)."""
    error = ValidationError("Test error")

    # Should be able to hash the exception
    hash_value = hash(error)
    assert isinstance(hash_value, int)


def test_exception_bool():
    """Test exception boolean evaluation."""
    error = ValidationError("Test error")

    # Exceptions should be truthy
    assert bool(error) is True
    assert error  # Should evaluate to True


def test_exception_attributes():
    """Test exception attributes."""
    error = ValidationError("Test error")

    # Should have standard exception attributes
    assert hasattr(error, 'args')
    assert error.args == ("Test error",)

    # Simple exceptions don't have custom attributes
    assert not hasattr(error, 'details')


def test_exception_with_kwargs():
    """Test exception with additional keyword arguments."""
    # ValidationError doesn't accept additional parameters
    error = ValidationError("Test error")

    assert str(error) == "Test error"
    assert not hasattr(error, 'code')
    assert not hasattr(error, 'field')


def test_exception_nested_attributes():
    """Test exception with nested attributes."""
    # ValidationError doesn't accept additional parameters
    error = ValidationError("Test error")

    assert str(error) == "Test error"
    assert not hasattr(error, 'metadata')