#!/usr/bin/env python3
"""
Unit Tests for HeySol exceptions

Following coding standards:
- Unit Tests Primary: Test individual functions in isolation
- Fail Fast: Tests must fail immediately on any deviation from expected behavior
- No Try-Catch: Exceptions are for unrecoverable errors only
"""

# Add the src directory to Python path
import sys
from pathlib import Path

import pytest

src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from heysol.exceptions import HeySolError, ValidationError


class TestHeySolExceptions:
    """Unit tests for HeySol exceptions."""

    def test_validation_error_initialization(self):
        """Test ValidationError initialization."""
        error = ValidationError("Test validation error")

        assert str(error) == "Test validation error"
        assert isinstance(error, Exception)
        assert isinstance(error, HeySolError)

    def test_heysol_error_initialization(self):
        """Test HeySolError initialization."""
        error = HeySolError("Test HeySol error")

        assert str(error) == "Test HeySol error"
        assert isinstance(error, Exception)

    def test_exception_inheritance(self):
        """Test exception class inheritance."""
        assert issubclass(ValidationError, Exception)
        assert issubclass(HeySolError, Exception)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
