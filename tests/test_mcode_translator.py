#!/usr/bin/env python3
"""
Unit Tests for mcode_translator module

Tests the exception classes following coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

import pytest

from heysol.mcode_translator.exceptions import (
    InstanceConflictError,
    InstanceNotFoundError,
    OperationError,
    RegistryError,
    ValidationError,
)


class TestRegistryExceptions:
    """Test registry exception classes."""

    def test_registry_error_initialization(self):
        """Test RegistryError initialization."""
        error = RegistryError("Test registry error")

        assert str(error) == "Test registry error"
        assert isinstance(error, Exception)

    def test_instance_not_found_error_initialization(self):
        """Test InstanceNotFoundError initialization."""
        error = InstanceNotFoundError("Instance not found")

        assert str(error) == "Instance not found"
        assert isinstance(error, RegistryError)
        assert isinstance(error, Exception)

    def test_operation_error_initialization(self):
        """Test OperationError initialization."""
        error = OperationError("Operation failed")

        assert str(error) == "Operation failed"
        assert isinstance(error, RegistryError)
        assert isinstance(error, Exception)

    def test_instance_conflict_error_initialization(self):
        """Test InstanceConflictError initialization."""
        error = InstanceConflictError("Instance conflict")

        assert str(error) == "Instance conflict"
        assert isinstance(error, RegistryError)
        assert isinstance(error, Exception)

    def test_validation_error_initialization(self):
        """Test ValidationError initialization."""
        error = ValidationError("Validation failed")

        assert str(error) == "Validation failed"
        assert isinstance(error, RegistryError)
        assert isinstance(error, Exception)

    def test_exception_inheritance_hierarchy(self):
        """Test exception inheritance hierarchy."""
        # Test that all registry exceptions inherit from RegistryError
        registry_error = RegistryError("base")
        instance_not_found = InstanceNotFoundError("not found")
        operation_error = OperationError("operation failed")
        instance_conflict = InstanceConflictError("conflict")
        validation_error = ValidationError("validation failed")

        # All should be instances of RegistryError
        assert isinstance(instance_not_found, RegistryError)
        assert isinstance(operation_error, RegistryError)
        assert isinstance(instance_conflict, RegistryError)
        assert isinstance(validation_error, RegistryError)

        # All should be instances of Exception
        assert isinstance(registry_error, Exception)
        assert isinstance(instance_not_found, Exception)
        assert isinstance(operation_error, Exception)
        assert isinstance(instance_conflict, Exception)
        assert isinstance(validation_error, Exception)

    def test_exception_with_empty_message(self):
        """Test exceptions with empty error messages."""
        # Should not raise exception during initialization
        error = RegistryError("")
        assert str(error) == ""

        error = InstanceNotFoundError("")
        assert str(error) == ""

    def test_exception_with_none_message(self):
        """Test exceptions with None error messages."""
        # Should not raise exception during initialization
        error = RegistryError(None)
        assert str(error) == "None"

        error = InstanceNotFoundError(None)
        assert str(error) == "None"