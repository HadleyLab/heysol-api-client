#!/usr/bin/env python3
"""
Unit Tests for HeySolConfig class

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

from heysol.config import HeySolConfig

# Use a properly formatted test API key (50+ characters to pass validation)
TEST_API_KEY = "rc_pat_test_key_1234567890abcdef1234567890abcdef1234567890ab"


class TestHeySolConfig:
    """Unit tests for HeySolConfig class."""

    def test_config_initialization(self):
        """Test HeySolConfig initialization with valid values."""
        config = HeySolConfig(
            api_key=TEST_API_KEY,
            base_url="https://core.heysol.ai/api/v1",
            mcp_url="https://core.heysol.ai/api/v1/mcp",
        )

        assert config.api_key == TEST_API_KEY
        assert config.base_url == "https://core.heysol.ai/api/v1"
        assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp"

    def test_config_initialization_defaults(self):
        """Test HeySolConfig initialization with default values."""
        config = HeySolConfig()

        assert config.api_key is None
        assert config.base_url == "https://core.heysol.ai/api/v1"
        assert config.mcp_url == "https://core.heysol.ai/api/v1/mcp?source=heysol-api-client"

    def test_config_initialization_with_timeout(self):
        """Test HeySolConfig initialization with timeout."""
        config = HeySolConfig(api_key=TEST_API_KEY, timeout=30)

        assert config.timeout == 30

    def test_config_initialization_with_source(self):
        """Test HeySolConfig initialization with source."""
        config = HeySolConfig(api_key=TEST_API_KEY, source="test-source")

        assert config.source == "test-source"


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
