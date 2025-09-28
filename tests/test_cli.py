#!/usr/bin/env python3
"""
Lean CLI Tests - HeySol API Client

Integration tests using real API calls. No mocking.
Tests fail fast on any deviation from expected behavior.
"""

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

# Add the parent directory to the Python path to import the CLI
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli import app


class TestCLI:
    """Integration tests for CLI functionality using real API calls."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_cli_help(self, runner):
        """Test CLI help output."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "HeySol API Client CLI" in result.output

    def test_cli_invalid_command(self, runner):
        """Test CLI with invalid command fails fast."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_cli_registry_list(self, runner):
        """Test registry list command."""
        result = runner.invoke(app, ["registry", "list"])
        assert result.exit_code == 0
        assert "Registered HeySol Instances" in result.output

    def test_cli_memory_help(self, runner):
        """Test memory command help."""
        result = runner.invoke(app, ["memory", "--help"])
        assert result.exit_code == 0
        assert "Memory operations" in result.output

    def test_cli_memory_move_missing_confirm(self, runner):
        """Test memory move fails fast without confirm."""
        result = runner.invoke(app, ["memory", "move", "--target-user", "test@example.com"])
        assert result.exit_code == 1
        assert "Move operation requires --confirm flag" in result.output

    def test_cli_memory_copy_missing_confirm(self, runner):
        """Test memory copy fails fast without confirm."""
        result = runner.invoke(app, ["memory", "copy", "--target-user", "test@example.com"])
        assert result.exit_code == 1
        assert "Copy operation requires --confirm flag" in result.output

    def test_cli_spaces_delete_missing_confirm(self, runner):
        """Test spaces delete fails fast without confirm."""
        result = runner.invoke(app, ["spaces", "delete", "space-123"])
        assert result.exit_code == 1
        assert "Space deletion requires --confirm flag" in result.output

    def test_cli_logs_delete_missing_confirm(self, runner):
        """Test logs delete fails fast without confirm."""
        result = runner.invoke(app, ["logs", "delete", "log-123"])
        assert result.exit_code == 1
        assert "Deletion requires --confirm flag" in result.output

    def test_cli_webhooks_delete_missing_confirm(self, runner):
        """Test webhooks delete fails fast without confirm."""
        result = runner.invoke(app, ["webhooks", "delete", "webhook-123"])
        assert result.exit_code == 1
        assert "Webhook deletion requires --confirm flag" in result.output
