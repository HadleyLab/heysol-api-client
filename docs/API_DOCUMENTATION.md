# HeySol API Client - Technical Documentation

## Quick Start

### Single Instance Setup

```python
from heysol import HeySolClient

# Initialize with API key
client = HeySolClient(api_key="your-api-key")

# Get user profile
profile = client.get_user_profile()

# Create a memory space
space_id = client.create_space("Research", "Clinical trial data")

# Ingest data
client.ingest("New clinical findings", space_id=space_id, tags=["research"])

# Search memories
results = client.search("clinical trial", limit=5)
```

### Multi-Instance Registry Setup (NEW!)

```python
from heysol.registry_config import RegistryConfig

# Load registry from .env file
registry = RegistryConfig()

# List all registered instances
instances = registry.get_registered_instances()
print(f"Found {len(instances)} instances")

# Get specific instance
instance = registry.get_instance("iDrDex@MammoChat.com")
print(f"API Key: {instance['api_key'][:20]}...")

# Use instance for operations
from heysol import HeySolClient
client = HeySolClient(api_key=instance["api_key"], base_url=instance["base_url"])
```

## API Access Methods

### ✅ **Direct API (RECOMMENDED)**
- **Access**: `https://core.heysol.ai/api/v1/{endpoint}`
- **Protocol**: Standard REST API with Bearer token authentication
- **Status**: ✅ **Lean and reliable**

### ✅ **MCP Protocol (Fully Integrated)**
- **Access**: `https://core.heysol.ai/api/v1/mcp`
- **Protocol**: Server-Sent Events with JSON-RPC
- **Tools**: 100+ available (memory, spaces, GitHub integration)
- **Status**: ✅ **Fully integrated with automatic fallback**
- **Usage**: `client.call_tool("tool_name", **params)` or automatic via `prefer_mcp=True`

## Authentication

All API requests require authentication using a Bearer token:

```python
from heysol import HeySolClient

client = HeySolClient(api_key="your-api-key-here")
```

The client automatically handles token authentication for all API calls.


## API Reference

### Registry Operations (NEW!)

| Method | Description |
|--------|-------------|
| `RegistryConfig()` | Load registry from .env file |
| `get_registered_instances()` | Get all registered instances |
| `get_instance(name)` | Get instance configuration by name |
| `get_instance_names()` | Get list of registered instance names |
| `add_instance(name, api_key, base_url, description)` | Add new instance to registry |
| `remove_instance(name)` | Remove instance from registry |
| `save_to_env()` | Save current instances back to .env file |

### User Operations

| Method | Endpoint | Status | Description |
|--------|----------|--------|-------------|
| `get_user_profile()` | `GET /profile` (OAuth only) | ❌ **OAuth Required** | Get current user profile (OAuth not yet available) |

### Memory Operations

| Method | Endpoint | Status | Description |
|--------|----------|--------|-------------|
| `search()` | `POST /search` | ✅ **Working** | Search memories |
| `ingest()` | `POST /add` | ✅ **Working** | Ingest data |
| `search_knowledge_graph()` | `POST /search` | ✅ **Working** | Search knowledge graph |
| `get_episode_facts()` | `GET /episodes/{id}/facts` | ✅ **Working** | Get episode facts |
| `get_ingestion_logs()` | `GET /logs` | ✅ **Working** | Get ingestion logs |
| `get_specific_log()` | `GET /logs/{id}` | ✅ **Working** | Get specific log |
| `check_ingestion_status()` | `GET /logs` | ✅ **Working** | Check ingestion status |
| `delete_log_entry()` | `DELETE /logs/{id}` | ✅ **Working** | Delete log entry |
| `move_logs_to_instance()` | Custom | ✅ **Working** | Move logs to another instance |
| `copy_logs_to_instance()` | Custom | ✅ **Working** | Copy logs to another instance |

### Space Operations

| Method | Endpoint | Status | Description |
|--------|----------|--------|-------------|
| `get_spaces()` | `GET /spaces` | ✅ **Working** | List spaces |
| `create_space()` | `POST /spaces` | ✅ **Working** | Create space |
| `get_space_details()` | `GET /spaces/{id}` | ✅ **Working** | Get space details |
| `update_space()` | `PUT /spaces/{id}` | ❌ **Not Supported** | Update space (API limitation - returns 400 "No updates provided") |
| `delete_space()` | `DELETE /spaces/{id}` | ✅ **Working** | Delete space |
| `bulk_space_operations()` | `PUT /spaces` | ✅ **Working** | Bulk operations |

**Note**: The `update_space()` endpoint is not currently supported by the HeySol API. Attempts to update space name or description return HTTP 400 with error "No updates provided", regardless of payload format. Spaces are immutable once created.

### Webhook Operations

| Method | Endpoint | Status | Description |
|--------|----------|--------|-------------|
| `register_webhook()` | `POST /webhooks` | ✅ **Working** | Register webhook |
| `list_webhooks()` | `GET /webhooks` | ✅ **Working** | List webhooks |
| `get_webhook()` | `GET /webhooks/{id}` | ✅ **Working** | Get webhook |
| `update_webhook()` | `PUT /webhooks/{id}` | ✅ **Working** | Update webhook |
| `delete_webhook()` | `DELETE /webhooks/{id}` | ✅ **Working** | Delete webhook |

## Error Handling

```python
from heysol import HeySolError, ValidationError, AuthenticationError

try:
    result = client.search("query")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid input: {e}")
except HeySolError as e:
    print(f"API error: {e}")
```

## Registry System (NEW!)

The HeySol API Client includes a powerful registry system for managing multiple HeySol instances using email-based identifiers.

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

## CLI Interface

The HeySol API client includes a comprehensive command-line interface for all operations:

### Setup and Configuration

```bash
# Setup API key (single instance)
export HEYSOL_API_KEY="your-api-key-here"

# Setup multiple instances via registry
heysol registry register  # Load from .env file
heysol registry list      # View all instances
```

### User Operations

```bash
# Profile endpoint requires OAuth (not yet available)
# heysol profile get

# Note: Profile operations require OAuth authentication which is not yet
# available on the server side. This feature will be enabled when OAuth
# is implemented.
```

### Space Management

```bash
heysol spaces list
heysol spaces create "Research Space" --description "Clinical data"
heysol spaces get <space-id>
heysol spaces update <space-id> --name "Updated Name"
heysol spaces delete <space-id> --confirm
```

### Memory Operations

```bash
# Registry-aware operations (NEW!)
heysol memory ingest iDrDex@MammoChat.com "Clinical findings" --space-id <space-id>
heysol memory search iDrDex@MammoChat.com "cancer research" --limit 10
heysol memory search-graph iDrDex@MammoChat.com "treatment outcomes" --depth 3
heysol memory queue iDrDex@MammoChat.com "Batch data" --tags clinical research
heysol memory episode iDrDex@MammoChat.com <episode-id>

# Cross-instance operations (NEW!)
heysol memory copy iDrDex@MammoChat.com HadleyLaboratory@gmail.com --confirm
heysol memory move iDrDex@gmail.com iDrDex@MammoChat.com --confirm
```

### Log Management

```bash
heysol logs list --source "heysol-api-client" --status success
heysol logs get <log-id>
heysol logs status --space-id <space-id> --run-id <run-id>
heysol logs delete "source-name" --confirm
heysol logs delete-entry <log-id> --confirm
```

### Webhook Management

```bash
heysol webhooks create "https://myapp.com/webhook" --secret "secret"
heysol webhooks list
heysol webhooks update <webhook-id> "https://new-url.com" --events memory.created
heysol webhooks delete <webhook-id> --confirm
```

### MCP Tools (NEW!)

```bash
# List available MCP tools
heysol tools list

# Use MCP with preference
python -c "
from heysol import HeySolClient
client = HeySolClient(prefer_mcp=True)
tools = client.get_available_tools()
print(f'Available tools: {list(tools.keys())}')
"
```

## MCP Integration

The HeySol client now includes full MCP (Model Context Protocol) integration with automatic fallback:

### Features
- **Automatic Fallback**: Falls back to direct API if MCP is unavailable
- **Tool Discovery**: Dynamic discovery of available MCP tools
- **Session Management**: Automatic MCP session handling
- **Performance Optimization**: Intelligent routing based on availability

### Usage Examples

```python
from heysol import HeySolClient

# Create client with MCP preference
client = HeySolClient(prefer_mcp=True)

# Check MCP availability
print(f"MCP Available: {client.is_mcp_available()}")

# Get available tools
tools = client.get_available_tools()
print(f"Available tools: {list(tools.keys())}")

# Automatic routing - uses MCP if available, API if not
result = client.ingest("Clinical data...")
result = client.search("cancer research")

# Direct MCP tool usage
if client.is_mcp_available():
    github_issues = client.call_tool("github_list_notifications")
    memory_result = client.call_tool("memory_ingest", message="Patient data")
```

### Configuration

```python
# Environment variables
export HEYSOL_MCP_URL="https://core.heysol.ai/api/v1/mcp?source=MyApp"
export HEYSOL_API_KEY="your-api-key"

# Client configuration
client = HeySolClient(
    prefer_mcp=True,           # Prefer MCP over API
    skip_mcp_init=False,       # Initialize MCP (default: False)
    mcp_url="custom-mcp-url"   # Custom MCP endpoint
)
```

### Tool Categories

MCP provides access to 100+ tools across several categories:

- **Memory Operations**: `memory_ingest`, `memory_search`, `memory_get_spaces`
- **GitHub Integration**: `github_create_issue`, `github_list_notifications`, `github_search_repositories`
- **Space Management**: `space_create`, `space_list`, `space_delete`
- **User Management**: `user_profile`, `user_preferences`
- **Advanced Features**: `knowledge_graph_search`, `batch_operations`

## Practical Examples

### Memory Management

```python
# Create and manage memory spaces
space_id = client.create_space("Clinical Research", "Cancer trial data")
client.ingest("New treatment shows 85% efficacy", space_id=space_id, tags=["clinical", "treatment"])

# Search with filters
results = client.search("cancer treatment", space_id=space_id, limit=10)
for episode in results.get("episodes", []):
    print(f"- {episode.get('content', '')}")

# Get knowledge graph connections
kg_results = client.search_knowledge_graph("treatment efficacy", limit=5, depth=2)
```

### Space Operations

```python
# List all spaces
spaces = client.get_spaces()
print(f"Found {len(spaces)} spaces")

# Get space details
space_details = client.get_space_details(space_id)
print(f"Space: {space_details.get('name')}")

# Update space
client.update_space(space_id, name="Updated Research", description="Updated description")

# Delete space (requires confirmation)
client.delete_space(space_id, confirm=True)
```

### User Profile

```python
# Get current user profile (requires OAuth - not yet available)
# profile = client.get_user_profile()
# print(f"User: {profile.get('name', 'Unknown')}")
# print(f"Email: {profile.get('email', 'Not provided')}")

# Note: Profile endpoint requires OAuth authentication which is not yet
# available on the server side. This feature will be enabled when OAuth
# is implemented.
```

### Status Checking

```python
# Check ingestion processing status
status = client.check_ingestion_status(run_id="run-123", space_id="space-456")
print(f"Status: {status.get('ingestion_status')}")
print(f"Available methods: {status.get('available_methods', [])}")

# CLI status checking
heysol logs status --space-id <space-id> --run-id <run-id>
```

### Registry System Examples

```python
# Load and use registry
from heysol.registry_config import RegistryConfig

registry = RegistryConfig()

# List all instances
instances = registry.get_registered_instances()
for name, config in instances.items():
    print(f"{name}: {config['description']}")

# Get specific instance
instance = registry.get_instance("iDrDex@MammoChat.com")
client = HeySolClient(api_key=instance["api_key"], base_url=instance["base_url"])

# Cross-instance operations
source_instance = registry.get_instance("iDrDex@gmail.com")
target_instance = registry.get_instance("HadleyLaboratory@gmail.com")

source_client = HeySolClient(api_key=source_instance["api_key"])
target_client = HeySolClient(api_key=target_instance["api_key"])

# Copy logs between instances
result = source_client.copy_logs_to_instance(
    target_client=target_client,
    source="kilo-code",
    confirm=True
)
```

### CLI Registry Examples

```bash
# Registry management
heysol registry list
heysol registry show iDrDex@MammoChat.com
heysol registry use iDrDex@MammoChat.com

# Cross-instance operations
heysol memory copy iDrDex@MammoChat.com HadleyLaboratory@gmail.com --confirm
heysol memory move iDrDex@gmail.com iDrDex@MammoChat.com --confirm
heysol memory search iDrDex@MammoChat.com "cancer research" --limit 10
```


## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=heysol

# Run specific test categories
pytest -m "unit"    # Unit tests only
pytest -m "slow"    # Integration tests
```

## Support

- **Primary Method**: Direct API (`https://core.heysol.ai/api/v1/{endpoint}`)
- **Authentication**: Bearer token with API key
- **Issues**: Check API key and network connectivity first

---

*Documentation updated for lean, direct API implementation.*