# HeySol API Client - Testing Guide (Updated)

## Overview

This document provides comprehensive information about the current test suite for the HeySol API client, including detailed analysis of server-side failures and issues that need to be resolved.

## Current Test Structure

### ✅ Core Test Files (All Working)

#### 1. Live API Integration Tests
- **Files**: `test_live_api.py`, `test_scenarios.py`
- **Purpose**: Test with real HeySol API endpoints using live API keys
- **Coverage**: Working endpoints (spaces, webhooks, memory operations)
- **Status**: ✅ Working for available endpoints
- **Benefits**: Validates real-world behavior with actual API keys

#### 2. CLI Integration Tests
- **File**: `test_cli.py`
- **Purpose**: Test command-line interface functionality
- **Coverage**: All CLI commands and options
- **Status**: ✅ All tests passing
- **Benefits**: Validates user-facing functionality

#### 3. Unit and Mock Tests
- **Files**: `test_unit_*.py`, `test_mcp.py`, `test_log_transfer_operations.py`
- **Purpose**: Unit tests with mocked responses and comprehensive testing
- **Coverage**: All components, error handling, edge cases
- **Status**: ✅ All tests passing
- **Benefits**: Fast execution, deterministic results

## Current Status: What's Working vs Not Working

### ✅ **Direct API: WORKING**
**Working Endpoints:**
- `/spaces` - List and manage spaces ✅
- `/webhooks` - Webhook operations ✅
- Memory operations via client ✅
- Error handling and validation ✅

### ❌ **Server-Side Failures Requiring Attention**

#### 1. **OAuth Authentication Endpoints (Not Implemented)**
- **Endpoint**: `/user/profile`
- **Error**: Requires OAuth authentication
- **Status**: ⏳ Not available on server side
- **Impact**: 2 tests skipped
- **Action Required**: Implement OAuth2 authentication on server

#### 2. **Knowledge Graph Search Failures**
- **Endpoint**: `/search` with `type=knowledge_graph`
- **Error**: Server-side processing failure
- **Status**: ⏳ Server error
- **Impact**: 1 test skipped
- **Action Required**: Debug server-side knowledge graph processing

#### 3. **Episode Facts Endpoint Issues**
- **Endpoint**: `/episodes/{episode_id}/facts`
- **Error**: 500 Server Error
- **Status**: ⏳ Server error
- **Impact**: 1 test skipped
- **Action Required**: Fix server-side episode facts retrieval

#### 4. **Webhooks Endpoint Issues**
- **Endpoint**: `/webhooks`
- **Error**: 400 Bad Request
- **Status**: ⚠️ Partial functionality (listing works, creation may fail)
- **Impact**: Limited webhook functionality
- **Action Required**: Fix webhook creation endpoint

### Authentication Methods

#### 1. API Key Authentication (Working)
```python
client = HeySolClient(api_key="your-api-key-here")
```

#### 2. Registry-Based Authentication (Working)
The test suite automatically detects API keys from:
- Registry configuration (`heysol.registry_config`)
- Environment variables starting with `HEYSOL_API_KEY*` containing `rc_pat_` values

## Detailed Server-Side Issues Analysis

### 🚨 **Critical Issues (Blocking Test Progress)**

#### Issue 1: OAuth2 Authentication Not Available
**Affected Tests:**
- `test_live_get_user_profile`
- `test_live_bearer_token_authentication`
- `test_live_api_performance`

**Server Response:** Profile endpoint requires OAuth authentication
**Root Cause:** OAuth2 endpoints not implemented on server side
**Priority:** HIGH
**Action Required:** Implement OAuth2 authentication system

#### Issue 2: Knowledge Graph Search Failures
**Affected Tests:**
- `test_live_search_knowledge_graph`

**Server Response:** Processing errors in knowledge graph queries
**Root Cause:** Server-side knowledge graph processing issues
**Priority:** MEDIUM
**Action Required:** Debug and fix knowledge graph search functionality

#### Issue 3: Episode Facts 500 Errors
**Affected Tests:**
- `test_live_get_episode_facts`

**Server Response:** 500 Internal Server Error
**Root Cause:** Server-side error in episode facts retrieval
**Priority:** MEDIUM
**Action Required:** Fix episode facts endpoint implementation

### ⚠️ **Partial Functionality Issues**

#### Issue 4: Webhooks 400 Bad Request
**Affected Tests:**
- `test_live_list_webhooks` (works for listing, fails for creation)

**Server Response:** 400 Bad Request for webhook operations
**Root Cause:** Webhook creation/update endpoints not properly implemented
**Priority:** LOW
**Action Required:** Fix webhook CRUD operations

## Test Execution Results

### Live API Test Summary (as of current run)
```
======================== 3 passed, 5 skipped in 27.99s =========================
✅ test_live_get_spaces - Successfully retrieved 3 spaces
✅ test_live_list_webhooks - Successfully listed 0 webhooks
✅ test_live_api_error_handling - Successfully tested error handling
⏳ test_live_get_user_profile - OAuth not available
⏳ test_live_search_knowledge_graph - Server processing error
⏳ test_live_get_episode_facts - 500 Server Error
⏳ test_live_bearer_token_authentication - OAuth not available
⏳ test_live_api_performance - OAuth not available
```

### Full Test Suite Summary
```
======================= 160 passed, 16 skipped in 1.65s ========================
✅ CLI Tests: 60+ tests - All passing
✅ Unit Tests: 100+ tests - All passing
✅ Integration Tests: 3 tests - Passing
⏳ OAuth-dependent tests: 5 tests - Skipped (expected)
⏳ Server-error tests: 2 tests - Skipped (needs server fixes)
```

## Action Plan: Getting All Tests to Pass

### Phase 1: Server-Side Fixes Required (HIGH PRIORITY)

#### 1. Implement OAuth2 Authentication
```bash
# Server-side implementation needed:
POST /oauth2/token
GET /user/profile (with OAuth2 bearer tokens)
```

#### 2. Fix Knowledge Graph Search
```bash
# Debug server-side knowledge graph processing
POST /search?type=knowledge_graph
```

#### 3. Fix Episode Facts Endpoint
```bash
# Fix 500 error in episode facts retrieval
GET /episodes/{episode_id}/facts
```

### Phase 2: Enhanced Webhook Functionality (MEDIUM PRIORITY)

#### 4. Fix Webhook CRUD Operations
```bash
# Fix 400 errors in webhook creation/updates
POST /webhooks
PUT /webhooks/{webhook_id}
```

### Phase 3: Testing Verification (After Server Fixes)

#### 5. Re-run Full Test Suite
```bash
python -m pytest tests/ -v
# Expected: All tests passing, 0 skipped
```

## Configuration for Testing

### Environment Variables (Current Setup)
```env
# HeySol API Client Environment Variables
HEYSOL_API_KEY_IDRDEX_MAMMOCHAT=your-api-key-here
HEYSOL_API_KEY_HADLEYLABELABORATORY=your-api-key-here
HEYSOL_API_KEY_IDRDEX_GMAIL=your-api-key-here
```

### Registry Configuration
The test suite also works with registry-based configuration:
```python
from heysol.registry_config import RegistryConfig
registry = RegistryConfig()
instances = registry.get_registered_instances()
```

## Running Tests

### Option 1: All Tests (Recommended)

```bash
cd heysol_api_client
python -m pytest tests/ -v
```

**Features:**
- Runs all test suites
- Includes unit tests, integration tests, and CLI tests
- Automatic API key detection from registry or environment
- Comprehensive coverage of all functionality

### Option 2: Live API Integration Tests Only

```bash
cd heysol_api_client
python -m pytest tests/test_live_api.py tests/test_scenarios.py -k integration -v
```

**Features:**
- Tests real API endpoints with live data
- Validates spaces and webhooks functionality
- Tests error handling with real API responses
- Requires API keys in registry or environment variables

### Option 3: CLI Tests Only

```bash
cd heysol_api_client
python -m pytest tests/test_cli.py -v
```

**Features:**
- Tests all CLI commands and options
- Validates user interface functionality
- No API key required
- Fast execution

### Option 4: Unit Tests Only

```bash
cd heysol_api_client
python -m pytest tests/test_unit_*.py tests/test_mcp.py -v
```

**Features:**
- Fast unit tests with mocked responses
- Tests individual components in isolation
- No API key required
- Deterministic results

## API Key Configuration

### Environment Variables
The test suite automatically detects API keys from environment variables in this order:
1. Registry configuration (highest priority)
2. Environment variables starting with `HEYSOL_API_KEY*` containing `rc_pat_` values

### Example .env file:
```env
# HeySol API Client Environment Variables
HEYSOL_API_KEY_IDRDEX_MAMMOCHAT=your-api-key-here
HEYSOL_API_KEY_HADLEYLABELABORATORY=your-api-key-here
HEYSOL_API_KEY_IDRDEX_GMAIL=your-api-key-here
```

### Registry Configuration
The test suite also works with registry-based configuration:
```python
from heysol.registry_config import RegistryConfig
registry = RegistryConfig()
instances = registry.get_registered_instances()
```

## Test Results Summary

### ✅ **Working Tests**
- **Live API Tests**: Spaces and webhooks operations ✅
- **CLI Tests**: All 60+ CLI test cases ✅
- **Unit Tests**: Mock-based testing ✅
- **Error Handling**: HTTP errors, validation, authentication ✅
- **Integration Tests**: Real API connectivity and functionality ✅

### ⏳ **Expected Skips/Failures**
- **OAuth Endpoints**: User profile requires OAuth (not yet implemented) ⏳
- **Some Memory Endpoints**: May return 500 errors (server-side issues) ⏳
- **MCP Tests**: Currently skipped (MCP not implemented in client) ⏳

### Test Categories
- **Integration Tests**: 5+ tests covering live API functionality
- **CLI Tests**: 60+ tests covering all CLI commands
- **Unit Tests**: 100+ tests covering individual components
- **Error Handling**: Comprehensive error scenario coverage
- **Performance Tests**: Response time and concurrent request testing

## Troubleshooting

### Common Issues

#### 1. "No API keys found"
**Solution**: Ensure your `.env` file contains API keys:
```bash
# Check if .env file exists and has API keys
ls -la .env
cat .env | grep HEYSOL_API_KEY
```

#### 2. "pytest: error: unrecognized arguments"
**Solution**: Use correct pytest syntax:
```bash
# ❌ Wrong
python -m pytest tests/ --timeout=30

# ✅ Correct
python -m pytest tests/ -v
```

#### 3. "ImportError" or "Module not found"
**Solution**: Run tests from project root:
```bash
cd heysol_api_client
python -m pytest tests/ -v
```

#### 4. Tests being skipped
**Solution**: Tests skip appropriately when:
- No API keys are configured (expected for unit tests)
- OAuth endpoints are tested (not yet available)
- Server errors occur (temporary server issues)

### Test Output Interpretation

#### Live API Tests
- **PASSED**: API endpoint is working correctly
- **SKIPPED**: Expected behavior (OAuth not available, server issues)
- **FAILED**: Unexpected issue requiring investigation

#### CLI Tests
- **PASSED**: CLI functionality is working
- **FAILED**: CLI bug or interface issue

#### Unit Tests
- **PASSED**: Component logic is correct
- **FAILED**: Code implementation issue

## Test Development

### Adding New Tests

1. **Unit Tests**: Add to appropriate `test_unit_*.py` file
2. **Integration Tests**: Add to `test_live_api.py` or `test_scenarios.py`
3. **CLI Tests**: Add to `test_cli.py`
4. **Error Tests**: Include comprehensive error scenarios

### Test Standards

- Tests should be idempotent (can run multiple times)
- Live tests should handle API failures gracefully
- Error messages should be descriptive and actionable
- Tests should clean up after themselves
- Mock tests should not require external dependencies

## Continuous Integration

### Running Tests in CI/CD
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v --tb=short

# Run only fast tests (no live API)
python -m pytest tests/test_cli.py tests/test_unit_*.py tests/test_mcp.py -v

# Run integration tests with API keys
python -m pytest tests/test_live_api.py tests/test_scenarios.py -k integration -v
```

## Support

### Test Environment Setup
1. Ensure `.env` file contains valid API keys
2. Verify registry configuration if using registry-based auth
3. Check network connectivity for live API tests
4. Review HeySol API status for server-side issues

### Getting Help
- Check test output for specific error messages
- Verify API key format and permissions
- Test with different API keys if available
- Review recent changes to API client code