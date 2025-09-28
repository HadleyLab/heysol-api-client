# HeySol API Client

[![PyPI version](https://badge.fury.io/py/heysol-api-client.svg)](https://pypi.org/project/heysol-api-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/heysol-api-client.svg)](https://pypi.org/project/heysol-api-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python client for the HeySol API with MCP protocol support, memory management, and CLI tools. Built by Dexter Hadley, MD/PhD for HeySol.ai integration.

**Version 1.2.1** - Production-ready with full API coverage and CLI tools.

## Features

- 🚀 **Full API Coverage**: Complete HeySol API endpoints with client-side status filtering
- 🔐 **Authentication**: API key and Bearer token support
- 📝 **Memory Management**: Ingest, search, and manage memory spaces
- 🏗️ **Multi-Instance Registry**: Email-based registry for managing multiple HeySol instances
- 🔄 **Cross-Instance Operations**: Move and copy logs between different instances
- 🛡️ **Error Handling**: Robust exception hierarchy with retries
- 📊 **Rate Limiting**: Built-in throttling and rate limiting
- 🖥️ **CLI Interface**: Command-line tools for all operations
- 📚 **Type Hints**: Full type annotation support
- 🧪 **Well Tested**: Comprehensive test suite with 95%+ coverage
- 📖 **Rich Documentation**: Interactive notebooks and examples

## Installation

```bash
pip install heysol-api-client
```

For development (from source):
```bash
git clone https://github.com/HadleyLab/heysol-api-client.git
cd heysol_api_client
pip install -e ".[dev]"
```

## Quick Start

1. **Get your API key** from [HeySol Core](https://core.heysol.ai/settings/api)
2. **Set environment variable**:
   ```bash
   export HEYSOL_API_KEY="your-api-key-here"
   ```
3. **Try the quick start**:
   ```bash
   python quick_start.py
   ```

### Basic Usage

```python
from heysol import HeySolClient

# Initialize client
client = HeySolClient(api_key="your-api-key")

# Create a space
space_id = client.create_space("Research", "Clinical data")

# Ingest data
client.ingest("New treatment shows promise", space_id=space_id)

# Search
results = client.search("treatment", space_ids=[space_id])
print(results["episodes"])

client.close()
```

### CLI Usage

```bash
# Registry Management (NEW!)
heysol registry list                                    # List all registered instances
heysol registry show iDrDex@MammoChat.com              # Show instance details
heysol registry use iDrDex@MammoChat.com               # Set active instance
heysol registry register                               # Load instances from .env file

# Multi-Instance Memory Operations (NEW!)
heysol memory move iDrDex@gmail.com HadleyLaboratory@gmail.com --confirm
heysol memory copy iDrDex@MammoChat.com iDrDex@gmail.com --confirm
heysol memory search iDrDex@MammoChat.com "cancer research" --limit 10
heysol memory ingest iDrDex@MammoChat.com "Clinical data" --space-id <space-id>

# Traditional Operations
heysol profile get
heysol spaces list
heysol spaces create "My Space" --description "Data space"
heysol logs list --status success
heysol logs delete-by-source "source-name" --confirm
```

## Configuration

**⚠️ IMPORTANT: API keys must be loaded from environment variables only. Never store them in config files.**

### Environment Variables (Recommended)
Set environment variables for secure configuration:
```bash
export HEYSOL_API_KEY="your-key"
export HEYSOL_BASE_URL="https://core.heysol.ai/api/v1"
export HEYSOL_SOURCE="my-app"
```

### .env File Support
Alternatively, create a `.env` file in your project root:
```bash
# .env
HEYSOL_API_KEY=your-key-here
HEYSOL_BASE_URL=https://core.heysol.ai/api/v1
HEYSOL_SOURCE=my-app
```

### Multi-Instance Registry (NEW!)
For managing multiple HeySol instances, use the registry system with email-based identifiers:
```bash
# .env with multiple instances
# iDrDex@MammoChat.com
HEYSOL_API_KEY=your-api-key-here

# HadleyLaboratory@gmail.com
HEYSOL_API_KEY=your-api-key-here

# iDrDex@gmail.com
HEYSOL_API_KEY=your-api-key-here
```

The registry automatically parses email comments and associates them with API keys for easy multi-instance management.

### Strict Loading Policy
- ✅ **Allowed**: Environment variables, `.env` files
- ❌ **Not Allowed**: JSON config files, hardcoded keys
- 🔒 **Security**: `HeySolConfig.from_env()` only reads from environment variables
- 🚫 **No Fallback**: Config files are never loaded automatically

### Programmatic Configuration
```python
from heysol import HeySolClient, HeySolConfig

# Load from environment (recommended)
client = HeySolClient()  # Uses HeySolConfig.from_env() automatically

# Or load explicitly
config = HeySolConfig.from_env()
client = HeySolClient(config=config)
```

## Registry System (NEW!)

The HeySol API Client now includes a powerful registry system for managing multiple HeySol instances using email-based identifiers.

### Registry Features

- 📧 **Email-Based Identifiers**: Use human-readable email addresses instead of cryptic API keys
- 🔄 **Cross-Instance Operations**: Move and copy logs between different instances
- 🏗️ **Automatic Resolution**: Registry automatically resolves emails to API keys and base URLs
- 🔒 **Secure Storage**: API keys stored securely in `.env` files with email associations
- 🖥️ **CLI Integration**: Full command-line interface for registry management

### Registry CLI Commands

```bash
# List all registered instances
heysol registry list

# Show details for a specific instance
heysol registry show iDrDex@MammoChat.com

# Set active instance
heysol registry use iDrDex@MammoChat.com

# Load instances from .env file
heysol registry register
```

### Cross-Instance Memory Operations

```bash
# Copy logs from one instance to another
heysol memory copy iDrDex@MammoChat.com HadleyLaboratory@gmail.com --confirm

# Move logs between instances
heysol memory move iDrDex@gmail.com iDrDex@MammoChat.com --confirm

# Search logs in a specific instance
heysol memory search iDrDex@MammoChat.com "cancer research" --limit 10

# Ingest data into a specific instance
heysol memory ingest iDrDex@MammoChat.com "Clinical findings" --space-id "research"
```

### Registry Configuration

Create a `.env` file with multiple instances:
```bash
# .env
# iDrDex@MammoChat.com
HEYSOL_API_KEY=your-api-key-here

# HadleyLaboratory@gmail.com
HEYSOL_API_KEY=your-api-key-here

# iDrDex@gmail.com
HEYSOL_API_KEY=your-api-key-here
```

The registry automatically parses the email comments and associates them with the corresponding API keys.

## API Reference

### Core Methods

**Memory Operations:**
- `ingest(message, space_id=None)` - Add data to memory
- `search(query, space_ids=None, limit=10)` - Search memories
- `search_knowledge_graph(query, space_id=None)` - Graph search

**Space Operations:**
- `get_spaces()` - List all spaces
- `create_space(name, description="")` - Create new space
- `update_space(space_id, name=None, description=None)` - Update space
- `delete_space(space_id, confirm=False)` - Delete space

**Log Operations:**
- `get_ingestion_logs(space_id=None, limit=100)` - Get logs
- `check_ingestion_status(run_id=None)` - Check status

**Webhook Operations:**
- `register_webhook(url, events=None, secret="")` - Create webhook
- `list_webhooks(space_id=None)` - List webhooks

## Error Handling

```python
from heysol import HeySolError, AuthenticationError

try:
    result = client.search("query")
except AuthenticationError:
    print("Check your API key")
except HeySolError as e:
    print(f"API error: {e}")
```

## Examples & Documentation

### Interactive Notebooks
- 📚 **[`quick_start.ipynb`](quick_start.ipynb)** - Python API walkthrough
- 📚 **[`examples/api_endpoints_demo.ipynb`](examples/api_endpoints_demo.ipynb)** - API endpoints demonstration
- 📚 **[`examples/client_types_demo.ipynb`](examples/client_types_demo.ipynb)** - Client types comparison
- 📚 **[`examples/comprehensive_client_demo.ipynb`](examples/comprehensive_client_demo.ipynb)** - Full client capabilities
- 📚 **[`examples/error_handling_demo.ipynb`](examples/error_handling_demo.ipynb)** - Error handling patterns
- 📚 **[`examples/log_management_demo.ipynb`](examples/log_management_demo.ipynb)** - Log management

### Documentation
- 📖 **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- 📖 **[Testing Report](docs/TESTING_REPORT.md)** - Comprehensive testing documentation
- 📖 **[API vs MCP Analysis](docs/API_VS_MCP_ANALYSIS.md)** - Protocol comparison guide

## Testing

```bash
pytest                    # Run all tests
pytest --cov=heysol      # With coverage
pytest -m "unit"         # Unit tests only
```

## Development

```bash
git clone https://github.com/HadleyLab/heysol-api-client.git
cd heysol-api-client
pip install -e ".[dev]"
pre-commit install
```

## Changelog

### v0.9.2 (2025-09-28) - GitHub Preparation Release
- 🖥️ **CLI Enhancement**: Added `logs get-by-source` command for filtering logs by source identifier
- 🖥️ **CLI Enhancement**: Added `logs sources` command to list all unique sources from memory logs
- 📋 **Log Management**: Enhanced log filtering capabilities with dedicated source-based queries
- 🔧 **CLI Commands**: Renamed log commands to follow API naming conventions
- 📚 **Documentation**: Refreshed all documentation for GitHub presentation
- 🔧 **Version Alignment**: Synchronized version numbers across all configuration files

### v0.9.1 (2025-09-24) - Registry System Release
- 🏗️ **Multi-Instance Registry System** - Email-based registry for managing multiple HeySol instances
- 🔄 **Cross-Instance Operations** - Move and copy logs between different instances
- 📧 **Email-Based Identifiers** - Human-readable email addresses instead of cryptic API keys
- 🖥️ **Enhanced CLI** - Registry-aware commands for all memory operations
- 📚 **Updated Documentation** - Comprehensive registry system documentation and examples
- 🔒 **Secure Configuration** - Multi-instance support in .env files with email associations

### v0.9.0 (2025-09-23)
- 🖥️ **CLI Tool**: Complete command-line interface for all operations (`heysol-client`)
- 🔍 **Source Filtering**: MCP-based source filtering for logs and search operations
- 🔄 **MCP Protocol Support**: Full Model Context Protocol integration with 100+ tools
- 📝 **Memory Management**: Ingest, search, and manage memory spaces
- 🏗️ **Space Operations**: Complete CRUD operations for memory spaces
- 📊 **Log Management**: Get, list, and delete ingestion logs with source filtering
- 👤 **User Profile**: Get current user profile information
- 🛡️ **Error Handling**: Comprehensive exception hierarchy with retry mechanisms
- ⚙️ **Configuration**: Flexible configuration via environment variables, files, or parameters

### v0.8.0 (2025-09-22)
- 🚀 **Full HeySol API coverage** with MCP protocol support
- 🖥️ **Complete CLI interface** for all operations
- 📝 **Memory space management** with search and ingestion
- 🛡️ **Robust error handling** with validation
- 📊 **Rate limiting** and performance optimizations

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📧 **Email**: iDrDex@HadleyLab.org
- 📖 **Docs**: https://docs.heysol.ai/api-reference
- 🐛 **Issues**: https://github.com/HadleyLab/heysol-api-client/issues
- 👤 **Author**: Dexter Hadley, MD/PhD (HadleyLab)