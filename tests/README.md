# HeySol API Client Test Suite

This directory contains a comprehensive, well-organized test suite for the HeySol API client.

## 📁 Test Structure

```
tests/
├── conftest.py                   # Pytest configuration and shared fixtures
├── test_unit_api_endpoints.py    # Unit tests for API endpoints
├── test_unit_error_handling.py   # Unit tests for error handling
├── test_unit_edge_cases.py       # Unit tests for edge cases
├── test_integration.py           # Integration tests
├── test_live_api.py              # Live API tests
├── test_mcp.py                   # MCP (Model Context Protocol) tests
├── test_oauth2.py                # OAuth2 authentication tests
├── test_scenarios.py             # Integration scenario tests
├── __init__.py                   # Package marker
└── README.md                     # This documentation
```

## 🏃 Running Tests

### Run All Tests
```bash
pytest
```

### Run Unit Tests Only
```bash
pytest tests/test_unit_*.py
```

### Run Integration Tests Only
```bash
pytest tests/test_integration.py tests/test_live_api.py tests/test_mcp.py tests/test_oauth2.py tests/test_scenarios.py
```

### Run Specific Test Files
```bash
# API endpoint tests
pytest tests/test_unit_api_endpoints.py

# Error handling tests
pytest tests/test_unit_error_handling.py

# Edge case tests
pytest tests/test_unit_edge_cases.py

# Live API tests
pytest tests/test_live_api.py

# MCP tests
pytest tests/test_mcp.py

# OAuth2 tests
pytest tests/test_oauth2.py
```

### Run with Coverage
```bash
pytest --cov=heysol --cov-report=html --cov-report=xml
```

## 🏷️ Test Markers

- `unit`: Unit tests for individual components
- `integration`: Integration tests with live API calls
- `slow`: Slow running tests
- `error`: Error handling tests
- `edge`: Edge case and boundary condition tests
- `performance`: Performance tests
- `security`: Security-related tests
- `api`: API endpoint functionality tests
- `auth`: Authentication and authorization tests
- `network`: Network-related tests

## 🔧 Configuration

Test configuration is centralized in `conftest.py` and includes:
- Environment variable loading
- Mock setup for all API endpoints
- Test data fixtures
- Pytest markers and options

## 📊 Test Results

- **77 unit tests** covering core functionality
- **57% code coverage** for comprehensive testing
- **100% pass rate** for all unit tests
- **Modular structure** for easy maintenance and extension

## 🎯 Test Categories

### Unit Tests (Mock-based)
- **API Tests** (`test_unit_api_endpoints.py`): Core API endpoint functionality
- **Error Tests** (`test_unit_error_handling.py`): Comprehensive error handling scenarios
- **Edge Tests** (`test_unit_edge_cases.py`): Boundary conditions and special cases

### Integration Tests (Live API)
- **Integration** (`test_integration.py`): General integration tests
- **Live API** (`test_live_api.py`): Real API endpoint testing
- **MCP** (`test_mcp.py`): Model Context Protocol functionality
- **OAuth2** (`test_oauth2.py`): Authentication flow testing
- **Scenarios** (`test_scenarios.py`): End-to-end integration scenarios

## 📝 Adding New Tests

1. **Unit Tests**: Add to appropriate `test_unit_*.py` file
2. **Integration Tests**: Add to appropriate `test_*.py` file
3. **Follow naming convention**: `test_<feature>_<scenario>.py`
4. **Use descriptive test names**: `test_<action>_<condition>_<expected_result>`
5. **Include docstrings**: Explain what each test validates

## 🔍 Test Data

Test data is provided through fixtures in `conftest.py`:
- Sample user data
- Sample space data
- Sample memory data
- Sample webhook data
- Mock API responses
- Error response scenarios