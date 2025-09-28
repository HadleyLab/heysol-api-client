# Changelog

All notable changes to the HeySol API Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-09-28

### Added
- **CLI Enhancement**: Added `logs get-by-source` command for filtering logs by source identifier
- **CLI Enhancement**: Added `logs sources` command to list all unique sources from memory logs
- **Log Management**: Enhanced log filtering capabilities with dedicated source-based queries
- **Documentation**: Refreshed all documentation for GitHub presentation
- **Version Alignment**: Synchronized version numbers across all configuration files

### Changed
- **CLI Commands**: Renamed log commands to follow API naming conventions:
  - `logs delete` now deletes a specific log entry by ID (single item)
  - `logs delete-by-source` now deletes logs by source (batch operation)

## [0.9.1] - 2025-09-24

### Added
- **CLI Tool**: Complete command-line interface for all operations (`heysol-client`)
- **Source Filtering**: MCP-based source filtering for logs and search operations
- **MCP Protocol Support**: Full Model Context Protocol integration with 100+ tools
- **Memory Management**: Ingest, search, and manage memory spaces
- **Space Operations**: Complete CRUD operations for memory spaces
- **Log Management**: Get, list, and delete ingestion logs with source filtering
- **User Profile**: Get current user profile information
- **Error Handling**: Comprehensive exception hierarchy with retry mechanisms
- **Configuration**: Flexible configuration via environment variables, files, or parameters

### Features
- **Source-Aware Operations**: All operations support source identification and filtering
- **MCP Integration**: Primary access method with fallback to direct API
- **Lean Design**: Minimal dependencies, performant, and maintainable codebase
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive README, API docs, and usage examples

### CLI Commands
- `heysol-client profile` - Get user profile
- `heysol-client spaces list` - List spaces
- `heysol-client spaces create "name"` - Create space
- `heysol-client ingest "message"` - Ingest data
- `heysol-client search "query"` - Search memory
- `heysol-client logs list` - List logs
- `heysol-client logs get-by-source "source"` - Get logs by source
- `heysol-client logs delete-by-source "source" --confirm` - Delete logs by source
- `heysol-client tools` - List MCP tools

### Examples
- `source_filtering_demo.py` - Comprehensive source filtering operations
- `cli_source_filtering_demo.py` - CLI usage demonstration
- `basic_usage.py` - Basic client operations
- `log_management.py` - Log management operations

### Technical Details
- **Python**: 3.8+ support
- **Dependencies**: requests, aiohttp, python-dotenv
- **License**: MIT
- **Packaging**: PyPI ready with complete metadata

---

**HeySol API Client** - A production-ready Python client for the HeySol API with MCP protocol support and comprehensive CLI tooling.