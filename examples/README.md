# 🎯 HeySol API Client Examples

Comprehensive collection of examples demonstrating HeySol API client capabilities with multiple implementation approaches.

## 📋 Overview

This directory contains **pedantic, comprehensive examples** that fully expose the HeySol API client's capabilities. Each example is provided in **three formats** following the quickstart pattern:

- **`.sh`** - Shell script (automated execution)
- **`.py`** - Python script (detailed demonstration)
- **`.ipynb`** - Jupyter notebook (interactive, pedantic walkthrough)

## 🚀 Quick Start

All examples require:
1. **API Key**: Get from [https://core.heysol.ai/settings/api](https://core.heysol.ai/settings/api)
2. **Environment**: Set `HEYSOL_API_KEY` or create `.env` file
3. **Installation**: `pip install heysol-api-client`

## 📚 Available Examples

### 1. 🎬 Quick Start Examples
**Location**: Root directory
- **[`../quick_start.sh`](../quick_start.sh)** - Complete setup in under 5 minutes
- **[`../quick_start.py`](../quick_start.py)** - Python API walkthrough
- **[`../quick_start.ipynb`](../quick_start.ipynb)** - Interactive notebook guide

### 2. 🔧 API Endpoints Demo
**Demonstrates**: Direct API operations, space management, data ingestion, search, knowledge graph, log management

| Format | File | Description |
|--------|------|-------------|
| **Shell** | [`api_endpoints_demo.sh`](api_endpoints_demo.sh) | Automated API endpoint testing |
| **Python** | [`api_endpoints_demo.py`](api_endpoints_demo.py) | Comprehensive API operations |
| **Notebook** | [`api_endpoints_demo.ipynb`](api_endpoints_demo.ipynb) | Interactive API exploration |

**Key Features Covered**:
- ✅ Direct API client initialization and validation
- ✅ Complete space management (CRUD operations)
- ✅ Data ingestion with metadata and session tracking
- ✅ Multiple search types (semantic, knowledge graph)
- ✅ Comprehensive log management
- ✅ Bulk operations for efficiency
- ✅ Robust error handling patterns
- ✅ Advanced features and status checking

**Run Commands**:
```bash
# Shell script
bash examples/api_endpoints_demo.sh

# Python script
python examples/api_endpoints_demo.py

# Jupyter notebook
jupyter notebook examples/api_endpoints_demo.ipynb
```

### 3. 📦 Client Types Demo
**Demonstrates**: Comparison of unified, API-only, and MCP-only clients

| Format | File | Description |
|--------|------|-------------|
| **Shell** | [`client_types_demo.sh`](client_types_demo.sh) | Automated client comparison |
| **Python** | [`client_types_demo.py`](client_types_demo.py) | Detailed client analysis |
| **Notebook** | [`client_types_demo.ipynb`](client_types_demo.ipynb) | Interactive client exploration |

**Key Features Covered**:
- ✅ All three client types (unified, API, MCP)
- ✅ Feature availability comparison
- ✅ Performance testing and benchmarking
- ✅ MCP-specific features (when available)
- ✅ Unified client fallback behavior
- ✅ Use case recommendations
- ✅ Real-world usage patterns

**Run Commands**:
```bash
# Shell script
bash examples/client_types_demo.sh

# Python script
python examples/client_types_demo.py

# Jupyter notebook
jupyter notebook examples/client_types_demo.ipynb
```

### 4. 🎯 Comprehensive Client Demo
**Demonstrates**: Complete client lifecycle and advanced scenarios

| Format | File | Description |
|--------|------|-------------|
| **Python** | [`comprehensive_client_demo.py`](comprehensive_client_demo.py) | Full capabilities showcase |
| **Notebook** | [`comprehensive_client_demo.ipynb`](comprehensive_client_demo.ipynb) | Interactive walkthrough |
| **Shell** | `comprehensive_client_demo.sh` | *(Coming soon)* |

**Key Features Covered**:
- ✅ Multi-client initialization and management
- ✅ Multi-space organization for data governance
- ✅ Comprehensive data ingestion with rich metadata
- ✅ Advanced search scenarios and query optimization
- ✅ Cross-client operations capability
- ✅ Performance analysis and optimization
- ✅ Production-ready patterns and best practices

**Run Commands**:
```bash
# Python script
python examples/comprehensive_client_demo.py
```

### 5. 🛡️ Error Handling Demo
**Demonstrates**: Robust error handling patterns and recovery strategies

| Format | File | Description |
|--------|------|-------------|
| **Python** | [`error_handling_demo.py`](error_handling_demo.py) | Error handling patterns |
| **Notebook** | [`error_handling_demo.ipynb`](error_handling_demo.ipynb) | Interactive error handling |
| **Shell** | `error_handling_demo.sh` | *(Coming soon)* |

**Key Features Covered**:
- ✅ Network error handling and recovery
- ✅ Authentication error patterns
- ✅ Validation error scenarios
- ✅ Rate limiting and retry logic
- ✅ Graceful degradation strategies
- ✅ Error recovery mechanisms
- ✅ Comprehensive logging and monitoring

**Run Commands**:
```bash
# Python script
python examples/error_handling_demo.py
```

### 6. 📋 Log Management Demo
**Demonstrates**: Advanced log management and monitoring

| Format | File | Description |
|--------|------|-------------|
| **Python** | [`log_management_demo.py`](log_management_demo.py) | Log analysis and monitoring |
| **Notebook** | [`log_management_demo.ipynb`](log_management_demo.ipynb) | Interactive log management |
| **Shell** | `log_management_demo.sh` | *(Coming soon)* |

**Key Features Covered**:
- ✅ Comprehensive log retrieval and filtering
- ✅ Source-based log analysis
- ✅ Performance monitoring and insights
- ✅ Health checking based on log patterns
- ✅ Error tracking and debugging
- ✅ Audit trail maintenance
- ✅ Log-based compliance reporting

**Run Commands**:
```bash
# Python script
python examples/log_management_demo.py
```

## 🎯 Learning Path

### Beginner Level
1. **Start Here**: [`../quick_start.py`](../quick_start.py) - Basic setup and operations
2. **API Basics**: [`api_endpoints_demo.py`](api_endpoints_demo.py) - Core API operations
3. **Client Types**: [`client_types_demo.py`](client_types_demo.py) - Understanding client options

### Intermediate Level
4. **Error Handling**: [`error_handling_demo.py`](error_handling_demo.py) - Robust error patterns
5. **Log Management**: [`log_management_demo.py`](log_management_demo.py) - Monitoring and debugging

### Advanced Level
6. **Comprehensive Demo**: [`comprehensive_client_demo.py`](comprehensive_client_demo.py) - Production patterns

## 💡 Key Concepts Demonstrated

### Client Architecture
- **Unified Client**: Best of both worlds with automatic fallback
- **Direct API Client**: High performance, no external dependencies
- **MCP Client**: Advanced features and tool discovery

### Core Operations
- **Space Management**: Organize data with logical separation
- **Data Ingestion**: Add content with rich metadata
- **Search Operations**: Semantic search with multiple parameters
- **Log Management**: Monitor operations and debug issues

### Advanced Features
- **Knowledge Graph**: Entity relationship exploration
- **Bulk Operations**: Efficient batch processing
- **Error Handling**: Production-ready error patterns
- **Performance Monitoring**: System health and optimization

### Production Patterns
- **Health Checking**: Monitor system status
- **Audit Trails**: Compliance and tracking
- **Graceful Degradation**: Fallback mechanisms
- **Resource Management**: Proper cleanup and optimization

## 🔧 Development Workflow

### For New Features
1. **Test with API Client**: Start with direct API operations
2. **Add Error Handling**: Implement robust error patterns
3. **Test with Unified Client**: Ensure compatibility
4. **Add Logging**: Monitor operations and performance
5. **Document**: Update examples and documentation

### For Production Deployment
1. **Choose Client Type**: Based on requirements
2. **Implement Monitoring**: Use log management patterns
3. **Add Health Checks**: Monitor system status
4. **Error Handling**: Implement comprehensive error recovery
5. **Performance Optimization**: Use bulk operations when possible

## 📖 Documentation References

- **API Documentation**: https://core.heysol.ai/
- **MCP Protocol**: Model Context Protocol specification
- **Python Client**: Full API reference in code
- **Best Practices**: Production patterns in examples

## 🤝 Contributing

When adding new examples:
1. Follow the **triple format** pattern (.sh, .py, .ipynb)
2. Include **comprehensive error handling**
3. Add **performance considerations**
4. Document **production use cases**
5. Update this **README** with new examples

## 🎉 What Makes These Examples Special

### Comprehensive Coverage
- **Full API Surface**: Every major API endpoint covered
- **Error Scenarios**: All common error patterns demonstrated
- **Performance Patterns**: Optimization techniques shown
- **Production Ready**: Real-world usage patterns

### Multiple Formats
- **Shell Scripts**: Automated testing and CI/CD integration
- **Python Scripts**: Detailed examples with explanations
- **Notebooks**: Interactive, educational walkthroughs

### Learning Focus
- **Pedantic**: Step-by-step explanations of every concept
- **Practical**: Real-world usage patterns and examples
- **Progressive**: From basic to advanced concepts
- **Comprehensive**: Complete coverage of capabilities

---

**Ready to explore HeySol? Start with the [quick start](../quick_start.py) and work through the examples in order! 🚀**