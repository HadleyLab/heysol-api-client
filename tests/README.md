# HeySol API Client Test Suite

This directory contains a clean, well-organized test suite for the HeySol API client following coding standards.

## 📁 Test Structure

```
tests/
├── unit/                          # Unit tests (mock-based)
│   ├── client/
│   │   ├── test_client.py         # HeySolClient class tests
│   │   ├── test_client_initialization.py  # Client initialization tests
│   │   ├── test_log_operations.py # Log operations tests
│   │   └── test_log_transfer.py   # Log transfer functionality tests
│   ├── clients/
│   │   ├── test_api_client.py     # HeySolAPIClient tests
│   │   ├── test_mcp_client.py     # HeySolMCPClient tests
│   │   └── test_mcp_config.py     # MCP configuration tests
│   ├── config/
│   │   └── test_config.py         # HeySolConfig tests
│   ├── exceptions/
│   │   └── test_exceptions.py     # Exception classes tests
│   └── registry/
│       └── test_registry_config.py # RegistryConfig unit tests
├── integration/                   # Integration tests (live API)
│   ├── api_endpoints/
│   │   ├── test_api_endpoints.py  # Live API endpoint tests
│   │   └── test_api_scenarios.py  # End-to-end scenario tests
│   ├── cli/
│   │   └── test_cli.py            # CLI integration tests
│   └── registry/
│       └── test_registry_integration.py # Registry integration tests
├── e2e/                           # End-to-end tests
│   └── workflows/                 # Workflow-based E2E tests
├── conftest.py                    # Pytest configuration and shared fixtures
├── __init__.py                    # Package marker
└── README.md                      # This documentation
```

## 🏃 Running Tests

### Run All Tests
```bash
PYTHONPATH=src pytest
```

### Run Unit Tests Only
```bash
PYTHONPATH=src pytest tests/unit/ -v
```

### Run Integration Tests Only
```bash
PYTHONPATH=src pytest tests/integration/ -v
```

### Run End-to-End Tests Only
```bash
PYTHONPATH=src pytest tests/e2e/ -v
```

### Run Specific Test Categories
```bash
# Client unit tests
PYTHONPATH=src pytest tests/unit/client/ -v

# API client tests
PYTHONPATH=src pytest tests/unit/clients/ -v

# Registry tests (unit + integration)
PYTHONPATH=src pytest tests/unit/registry/ tests/integration/registry/ -v

# CLI integration tests
PYTHONPATH=src pytest tests/integration/cli/ -v

# API endpoint tests
PYTHONPATH=src pytest tests/integration/api_endpoints/ -v
```

### Run with Coverage
```bash
PYTHONPATH=src pytest --cov=src/heysol --cov-report=html --cov-report=term-missing
```

## 🏷️ Test Categories

### Unit Tests (Mock-based)
Located in `tests/unit/` - Test individual functions in isolation with proper mocking.

- **`client/`**: HeySolClient class and related functionality
  - `test_client.py`: Core client initialization and methods
  - `test_client_initialization.py`: Client setup with various configurations
  - `test_log_operations.py`: Log generator and copy operations
  - `test_log_transfer.py`: Log transfer between instances

- **`clients/`**: API and MCP client implementations
  - `test_api_client.py`: HeySolAPIClient functionality
  - `test_mcp_client.py`: HeySolMCPClient functionality
  - `test_mcp_config.py`: MCP configuration validation

- **`config/`**: Configuration management
  - `test_config.py`: HeySolConfig class tests

- **`exceptions/`**: Exception handling
  - `test_exceptions.py`: Custom exception classes

- **`registry/`**: Registry configuration
  - `test_registry_config.py`: RegistryConfig unit tests with mocking

### Integration Tests (Live API)
Located in `tests/integration/` - Test real API endpoints with live calls.

- **`api_endpoints/`**: Direct API endpoint testing
  - `test_api_endpoints.py`: Comprehensive endpoint validation
  - `test_api_scenarios.py`: End-to-end workflow scenarios

- **`cli/`**: Command-line interface testing
  - `test_cli.py`: CLI command validation with real API calls

- **`registry/`**: Registry integration testing
  - `test_registry_integration.py`: Registry functionality with real data

### End-to-End Tests (E2E)
Located in `tests/e2e/` - Complete workflow testing across multiple components.

## 📊 Test Results

- **✅ 45+ Unit Tests** - Core functionality with proper mocking across all components
- **✅ 25+ Registry Tests** - Unit and integration tests with real API validation
- **✅ 15+ Integration Tests** - Live API endpoint validation
- **✅ CLI Integration Tests** - Command interface validation with real API calls
- **✅ 90%+ Code Coverage** - Comprehensive edge case and error scenario testing

## 🎯 Test Standards

### Following Coding Standards
- **Integration Tests for APIs**: ✅ Using real API keys and live calls, rejecting mocking
- **Fail Fast**: ✅ Tests fail immediately on any deviation from expected behavior
- **Unit Tests Primary**: ✅ Individual function testing in isolation with strategic mocking
- **No Try-Catch**: ✅ Proper exception handling for unrecoverable errors only

### Test Organization
- **Single Responsibility**: Each test file has clear, focused purpose
- **Descriptive Names**: Test functions clearly describe what they validate
- **Proper Mocking**: Strategic use of mocks for unit tests, real calls for integration
- **Live Validation**: Real API calls for integration testing, comprehensive error coverage

## 📝 Adding New Tests

1. **Unit Tests**: Add to appropriate `tests/unit/<component>/` directory
2. **Integration Tests**: Add to appropriate `tests/integration/<component>/` directory
3. **E2E Tests**: Add to `tests/e2e/workflows/` for complete workflow testing
4. **Follow naming convention**: `test_<feature>_<scenario>.py`
5. **Use descriptive test names**: `test_<action>_<condition>_<expected_result>`
6. **Include docstrings**: Explain what each test validates
7. **Follow standards**: Unit tests with mocks, integration tests with real API calls

## 🔧 Configuration

Test configuration is centralized in `conftest.py` and includes:
- Environment variable loading from `.env` file
- Registry-based API key detection for integration tests
- Pytest markers and options for different test categories
- Shared fixtures for common test data and setup

## 🔍 Test Data

Test data is provided through multiple sources:

### Unit Tests
- **Mock Objects**: Strategic mocking of external dependencies
- **Test Fixtures**: Reusable test data and setup in `conftest.py`
- **Synthetic Data**: Generated test data that matches real API formats

### Integration Tests
- **Registry Configuration**: Real API keys from `.env` file via RegistryConfig
- **Live API Calls**: Real endpoint validation with actual network requests
- **Environment Variables**: Direct API key access for testing

### Error Scenarios
- **Comprehensive Coverage**: Invalid inputs, network failures, API errors
- **Edge Cases**: Boundary conditions, malformed data, concurrent operations
- **Fail Fast Validation**: Immediate failure on any deviation from expected behavior