"""
Comprehensive integration tests for all CLI help commands and subcommands.

Tests that all CLI help commands display correctly and handle help flags properly.
Converted from test_all_help.py for pytest integration.
"""

import pytest
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def run_help_command(cmd, cwd):
    """Run a help command and return the result."""
    try:
        # Split the command string into a list for subprocess.run
        cmd_list = cmd.split()
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10
        )
        return {
            'command': cmd,
            'returncode': result.returncode,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            'command': cmd,
            'returncode': -1,
            'stdout': '',
            'stderr': 'Timeout'
        }
    except Exception as e:
        return {
            'command': cmd,
            'returncode': -1,
            'stdout': '',
            'stderr': str(e)
        }


class TestAllCLIHelp:
    """Comprehensive tests for all CLI help commands."""

    @pytest.mark.parametrize("cmd", [
        './heysol-cli --help',
        './heysol-cli memory --help',
        './heysol-cli logs --help',
        './heysol-cli spaces --help',
        './heysol-cli profile --help',
        './heysol-cli registry --help',
        './heysol-cli tools --help',
        './heysol-cli webhooks --help'
    ])
    def test_main_command_helps(self, cmd, project_root):
        """Test main command group help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        # Check that help was displayed successfully
        assert 'Usage:' in result['stdout'], f"Command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli memory ingest --help',
        './heysol-cli memory search --help',
        './heysol-cli memory search-graph --help',
        './heysol-cli memory queue --help',
        './heysol-cli memory episode --help',
        './heysol-cli memory move --help',
        './heysol-cli memory copy --help',
        './heysol-cli memory copy-by-id --help'
    ])
    def test_memory_subcommand_helps(self, cmd, project_root):
        """Test memory subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Memory command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Memory command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli logs list --help',
        './heysol-cli logs delete --help',
        './heysol-cli logs delete-by-source --help',
        './heysol-cli logs get --help',
        './heysol-cli logs get-by-source --help',
        './heysol-cli logs status --help',
        './heysol-cli logs copy --help',
        './heysol-cli logs sources --help'
    ])
    def test_logs_subcommand_helps(self, cmd, project_root):
        """Test logs subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Logs command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Logs command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli spaces list --help',
        './heysol-cli spaces create --help',
        './heysol-cli spaces get --help',
        './heysol-cli spaces update --help',
        './heysol-cli spaces delete --help',
        './heysol-cli spaces bulk-ops --help'
    ])
    def test_spaces_subcommand_helps(self, cmd, project_root):
        """Test spaces subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Spaces command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Spaces command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli profile get --help'
    ])
    def test_profile_subcommand_helps(self, cmd, project_root):
        """Test profile subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Profile command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Profile command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli registry register --help',
        './heysol-cli registry list --help',
        './heysol-cli registry show --help',
        './heysol-cli registry use --help'
    ])
    def test_registry_subcommand_helps(self, cmd, project_root):
        """Test registry subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Registry command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Registry command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli tools list --help'
    ])
    def test_tools_subcommand_helps(self, cmd, project_root):
        """Test tools subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Tools command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Tools command '{cmd}' exited with non-zero code: {result['returncode']}"

    @pytest.mark.parametrize("cmd", [
        './heysol-cli webhooks create --help',
        './heysol-cli webhooks list --help',
        './heysol-cli webhooks get --help',
        './heysol-cli webhooks update --help',
        './heysol-cli webhooks delete --help'
    ])
    def test_webhooks_subcommand_helps(self, cmd, project_root):
        """Test webhooks subcommand help displays."""
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print(f"{'='*60}")

        result = run_help_command(cmd, project_root)

        # Print the help output as a courtesy
        if result['stdout']:
            print("Help Output:")
            print(result['stdout'])
        if result['stderr']:
            print("Stderr:")
            print(result['stderr'])

        assert 'Usage:' in result['stdout'], f"Webhooks command '{cmd}' failed to show usage: {result['stderr']}"
        assert result['returncode'] == 0, f"Webhooks command '{cmd}' exited with non-zero code: {result['returncode']}"

    def test_all_help_commands_summary(self, project_root):
        """Test that all help commands work and provide a summary."""
        print(f"\n{'='*60}")
        print("COMPREHENSIVE HELP COMMAND SUMMARY TEST")
        print(f"{'='*60}")

        # Define all command groups
        command_groups = {
            'main': [
                './heysol-cli --help',
                './heysol-cli memory --help',
                './heysol-cli logs --help',
                './heysol-cli spaces --help',
                './heysol-cli profile --help',
                './heysol-cli registry --help',
                './heysol-cli tools --help',
                './heysol-cli webhooks --help'
            ],
            'memory': [
                './heysol-cli memory ingest --help',
                './heysol-cli memory search --help',
                './heysol-cli memory search-graph --help',
                './heysol-cli memory queue --help',
                './heysol-cli memory episode --help',
                './heysol-cli memory move --help',
                './heysol-cli memory copy --help',
                './heysol-cli memory copy-by-id --help'
            ],
            'logs': [
                './heysol-cli logs list --help',
                './heysol-cli logs delete --help',
                './heysol-cli logs delete-by-source --help',
                './heysol-cli logs get --help',
                './heysol-cli logs get-by-source --help',
                './heysol-cli logs status --help',
                './heysol-cli logs copy --help',
                './heysol-cli logs sources --help'
            ],
            'spaces': [
                './heysol-cli spaces list --help',
                './heysol-cli spaces create --help',
                './heysol-cli spaces get --help',
                './heysol-cli spaces update --help',
                './heysol-cli spaces delete --help',
                './heysol-cli spaces bulk-ops --help'
            ],
            'profile': [
                './heysol-cli profile get --help'
            ],
            'registry': [
                './heysol-cli registry register --help',
                './heysol-cli registry list --help',
                './heysol-cli registry show --help',
                './heysol-cli registry use --help'
            ],
            'tools': [
                './heysol-cli tools list --help'
            ],
            'webhooks': [
                './heysol-cli webhooks create --help',
                './heysol-cli webhooks list --help',
                './heysol-cli webhooks get --help',
                './heysol-cli webhooks update --help',
                './heysol-cli webhooks delete --help'
            ]
        }

        all_commands = []
        for group in command_groups.values():
            all_commands.extend(group)

        total_commands = len(all_commands)
        results = []

        print(f"Testing {total_commands} total help commands...\n")

        for i, cmd in enumerate(all_commands, 1):
            print(f"[{i:2d}/{total_commands}] Testing: {cmd}")
            result = run_help_command(cmd, project_root)
            results.append(result)

            # Print the help output as a courtesy
            if result['stdout']:
                print("  Help Output:")
                for line in result['stdout'].split('\n')[:5]:  # Show first 5 lines
                    print(f"    {line}")
                if len(result['stdout'].split('\n')) > 5:
                    print("    ...")
            if result['stderr']:
                print(f"  Stderr: {result['stderr'][:100]}...")
            print()

        # Assertions
        passed = sum(1 for r in results if 'Usage:' in r['stdout'])
        failed = total_commands - passed

        print(f"{'='*60}")
        print("📊 FINAL TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Commands: {total_commands}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print()

        if failed > 0:
            print("❌ Failed Commands:")
            for result in results:
                if 'Usage:' not in result['stdout']:
                    print(f"  - {result['command']}")
                    if result['stderr']:
                        print(f"    Error: {result['stderr'][:100]}...")
            print()

        assert failed == 0, f"{failed} out of {total_commands} help commands failed. Check stderr for details."

        # Additional check: Ensure no timeouts or errors
        for result in results:
            assert result['returncode'] == 0, f"Command '{result['command']}' failed with code {result['returncode']}: {result['stderr']}"
            assert 'Timeout' not in result['stderr'], f"Command '{result['command']}' timed out"


class TestCLIPolish:
    """Test CLI polish and help output quality."""

    def test_main_help_polish(self, project_root):
        """Test main help output is polished and professional."""
        result = run_help_command('./heysol-cli --help', project_root)

        # Verify clean, concise structure
        assert 'HeySol API Client CLI' in result['stdout']
        assert 'Authentication: Use --api-key' in result['stdout']
        assert 'Get API key from: https://core.heysol.ai/settings/api' in result['stdout']

        # Verify no verbose setup instructions
        assert 'Setup:' not in result['stdout']
        assert '1. Get your API key' not in result['stdout']
        assert '2. Set environment variable' not in result['stdout']

        # Verify professional formatting
        assert '╭─ Options ────────────────────────────────────────────────────────────────────╮' in result['stdout']
        assert '╭─ Commands ───────────────────────────────────────────────────────────────────╮' in result['stdout']

    def test_command_descriptions_polish(self, project_root):
        """Test command descriptions follow Typer best practices."""
        commands = [
            ('./heysol-cli memory --help', 'Memory operations: ingest, search, queue, and episode management'),
            ('./heysol-cli logs --help', 'Manage ingestion logs, status, and log operations'),
            ('./heysol-cli spaces --help', 'Space management: create, list, update, delete, and bulk operations'),
            ('./heysol-cli profile --help', 'User profile and API health check operations'),
            ('./heysol-cli registry --help', 'Manage registered HeySol instances and authentication'),
            ('./heysol-cli tools --help', 'List MCP tools and integrations'),
            ('./heysol-cli webhooks --help', 'Webhook management: create, list, update, delete webhooks')
        ]

        for cmd, expected_desc in commands:
            result = run_help_command(cmd, project_root)
            assert expected_desc in result['stdout'], f"Command '{cmd}' missing proper description"

    def test_subcommand_help_completeness(self, project_root):
        """Test subcommand help outputs are complete and well-formatted."""
        subcommands = [
            './heysol-cli memory ingest --help',
            './heysol-cli memory search --help',
            './heysol-cli logs list --help',
            './heysol-cli spaces create --help',
            './heysol-cli profile get --help',
            './heysol-cli registry register --help',
            './heysol-cli webhooks create --help'
        ]

        for cmd in subcommands:
            result = run_help_command(cmd, project_root)

            # Verify proper structure
            assert 'Usage:' in result['stdout']
            assert '╭─' in result['stdout'] or 'Options:' in result['stdout'] or 'Arguments:' in result['stdout']

            # Verify no formatting errors
            assert 'Error' not in result['stderr']
            assert result['returncode'] == 0

    def test_help_consistency_across_modules(self, project_root):
        """Test help formatting is consistent across all CLI modules."""
        all_commands = [
            './heysol-cli --help',
            './heysol-cli memory --help',
            './heysol-cli logs --help',
            './heysol-cli spaces --help',
            './heysol-cli profile --help',
            './heysol-cli registry --help',
            './heysol-cli tools --help',
            './heysol-cli webhooks --help'
        ]

        for cmd in all_commands:
            result = run_help_command(cmd, project_root)

            # Verify consistent formatting elements
            lines = result['stdout'].split('\n')

            # Check for proper section headers (if sections exist)
            section_headers = [line for line in lines if '╭─' in line or '├─' in line or '╰─' in line]
            if section_headers:
                # Verify consistent formatting
                for header in section_headers:
                    assert '─' in header, f"Inconsistent header format in {cmd}"

            # Verify no malformed output
            assert len(result['stdout']) > 50, f"Help output too short for {cmd}"
            assert result['returncode'] == 0

    def test_help_accessibility_and_clarity(self, project_root):
        """Test help outputs are accessible and clear for users."""
        test_commands = [
            './heysol-cli --help',
            './heysol-cli memory ingest --help',
            './heysol-cli logs list --help'
        ]

        for cmd in test_commands:
            result = run_help_command(cmd, project_root)

            # Verify readability
            assert 'Usage:' in result['stdout'], f"Missing usage section in {cmd}"

            # Check for clear option descriptions
            if 'Options:' in result['stdout']:
                # Ensure options have descriptions
                lines = result['stdout'].split('\n')
                in_options = False
                has_descriptions = False

                for line in lines:
                    if '╭─ Options' in line or 'Options:' in line:
                        in_options = True
                    elif in_options and (line.strip() == '' or '╰─' in line):
                        break
                    elif in_options and '│' in line and 'TEXT' in line:
                        has_descriptions = True

                if in_options:
                    assert has_descriptions, f"Options section missing descriptions in {cmd}"

            # Verify no confusing or unclear content
            assert 'TODO' not in result['stdout']
            assert 'FIXME' not in result['stdout']
            assert 'Error' not in result['stdout'] or 'Error' in result['stderr']