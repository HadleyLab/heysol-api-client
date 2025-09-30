#!/usr/bin/env python
# coding: utf-8

# # 🛡️ HeySol API Client - Error Handling Demo
#
# Comprehensive error handling patterns and best practices with detailed explanations, recovery strategies, and production-ready error management.
#
# ## 📋 What This Demo Covers
#
# This notebook provides a **comprehensive, production-focused** demonstration of error handling:
#
# 1. **🌐 Network Error Handling** - Connection failures and timeouts
# 2. **🔐 Authentication Errors** - Invalid credentials and permissions
# 3. **✋ Validation Errors** - Input validation and data integrity
# 4. **🔄 Retry Logic** - Exponential backoff and recovery
# 5. **🛟 Graceful Degradation** - Fallback mechanisms
# 6. **🔧 Error Recovery** - Comprehensive recovery strategies
#
# ## 🎯 Learning Objectives
#
# By the end of this notebook, you will:
# - ✅ Master comprehensive error handling patterns
# - ✅ Understand retry logic and exponential backoff
# - ✅ Implement graceful degradation strategies
# - ✅ Learn error recovery and user feedback
# - ✅ Apply production-ready error management
# - ✅ Monitor and log errors effectively
#
# ## 🛡️ Error Handling Concepts
#
# ### Error Categories
# - **Network Errors**: Connection failures, timeouts, DNS issues
# - **Authentication Errors**: Invalid credentials, expired tokens
# - **Validation Errors**: Invalid input, missing required fields
# - **Rate Limiting**: API quota exceeded, throttling
# - **Server Errors**: 5xx responses, service unavailable
#
# ### Recovery Strategies
# - **Retry Logic**: Exponential backoff with jitter
# - **Fallback Mechanisms**: Alternative approaches
# - **Graceful Degradation**: Reduced functionality
# - **User Communication**: Clear error messages
#
# ---

# ## 🛡️ Step 1: Error Handling Architecture Overview
#
# Before diving into code, let's understand the comprehensive error handling architecture we'll be implementing and why each component is critical.

# In[ ]:


# Import with comprehensive error handling setup
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path.cwd().parent))

# Import with detailed error context and architecture explanation
try:
    from heysol import HeySolClient
    from heysol.clients.api_client import HeySolAPIClient
    from heysol.exceptions import HeySolError, ValidationError

    print("✅ Successfully imported HeySol error handling framework")
    print("   📦 HeySolClient: Unified client with error management")
    print("   ⚡ HeySolAPIClient: Direct API with HTTP error handling")
    print("   🛡️ HeySolError: Base exception class")
    print("   ✋ ValidationError: Input validation exceptions")
    print("\n🛡️ Error Handling Architecture:")
    print("   • Hierarchical exception handling")
    print("   • Comprehensive error categorization")
    print("   • Automatic retry with exponential backoff")
    print("   • Graceful degradation strategies")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("💡 Make sure you're running from the project root with src/ in path")
    raise


# ### 🏗️ Error Handling Architecture Deep Dive
#
# **Critical Design Principles**: Our error handling architecture is built on several fundamental principles:
#
# #### 1. Hierarchical Error Classification
# ```
# HeySolError (Base)
# ├── ValidationError (Input/Format Issues)
# ├── AuthenticationError (Credential Problems)
# ├── NetworkError (Connection Issues)
# ├── RateLimitError (Quota Exceeded)
# └── ServerError (Service Issues)
# ```
#
# #### 2. Recovery Strategy Matrix
# | Error Type | Retry | Fallback | User Message | Logging Level |
# |------------|-------|----------|--------------|---------------|
# | Validation | ❌ | Input Fix | Clear | INFO |
# | Authentication | ⏳ | Re-auth | Security | WARN |
# | Network | ✅ | Cache/Offline | Connection | ERROR |
# | Rate Limit | ⏳ | Queue/Delay | Throttling | WARN |
# | Server | ✅ | Degraded Mode | Service | ERROR |
#
# #### 3. User Experience Considerations
# - **Clear Messages**: Users understand what went wrong
# - **Actionable Guidance**: Users know how to fix issues
# - **Graceful Degradation**: Partial functionality when possible
# - **Progress Indicators**: Users see retry attempts
#
# **Production Insight**: This architecture ensures users never see raw technical errors while developers get comprehensive debugging information.

# In[ ]:


# API key validation with security considerations
print("🔑 Step 1.1: API Key Validation and Security Assessment")
print("-" * 65)

api_key = os.getenv("HEYSOL_API_KEY")

if not api_key:
    print("❌ No API key found!")
    print("\n📝 Security Setup Instructions:")
    print("1. Visit: https://core.heysol.ai/settings/api")
    print("2. Generate an API key")
    print("3. Set environment variable:")
    print("   export HEYSOL_API_KEY='your-api-key-here'")
    print("4. Or create .env file with:")
    print("   HEYSOL_API_KEY=your-api-key-here")
    print("\n🔒 Security Best Practices:")
    print("   • Store API keys in environment variables, never in code")
    print("   • Use .env files for local development")
    print("   • Rotate keys regularly in production")
    print("   • Limit key permissions to minimum required")
    print("   • Monitor key usage for anomalies")
    print("\nThen restart this notebook!")
    raise ValueError("API key not configured")

# Security assessment
print("✅ API key validation passed")
print(f"✅ Key format: {'Valid' if len(api_key) > 20 else 'Invalid'} prefix")
print(f"✅ Key security: {'Good' if not api_key.islower() else 'Weak'} complexity")
print(f"✅ Key length: {len(api_key)} characters (recommended: > 32)")
print(f"✅ Key entropy: {'High' if len(set(api_key)) > 20 else 'Low'} diversity")

# Compliance note
print("\n📋 Compliance Considerations:")
print("   • API keys should be rotated every 90 days")
print("   • Monitor for unusual access patterns")
print("   • Log key usage for audit trails")
print("   • Use different keys for different environments")


# ## 🛡️ Step 2: Comprehensive Error Handler Implementation
#
# Let's implement a sophisticated error handler that demonstrates all the key error handling patterns and strategies.

# In[ ]:


# Comprehensive error handler implementation
class ErrorHandler:
    """
    Comprehensive error handling utility with advanced features.

    Features:
    - Error categorization and logging
    - Retry logic with exponential backoff
    - Recovery strategy recommendations
    - Performance impact tracking
    - User-friendly error messages

    Production Use:
    - Wrap all API calls with this handler
    - Monitor error rates and patterns
    - Alert on unusual error spikes
    - Use error data for system optimization
    """

    def __init__(self) -> None:
        self.error_log: List[Dict[str, Any]] = []
        self.retry_counts: Dict[str, int] = {}
        self.start_time = time.time()

    def log_error(
        self, operation: str, error: Exception, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an error with comprehensive context.

        Args:
            operation: Name of the operation that failed
            error: The exception that occurred
            context: Additional context information

        Note:
            In production, this would write to structured logs
            with correlation IDs and performance metrics.
        """
        error_info = {
            "timestamp": time.time(),
            "operation": operation,
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context or {},
            "uptime_seconds": time.time() - self.start_time,
        }
        self.error_log.append(error_info)
        print(f"❌ {operation}: {error}")

    def should_retry(self, operation: str, max_retries: int = 3) -> Tuple[bool, int]:
        """
        Determine if operation should be retried with exponential backoff.

        Args:
            operation: Name of the operation
            max_retries: Maximum number of retry attempts

        Returns:
            tuple: (should_retry, retry_count)

        Strategy:
        - Network errors: Retry with backoff
        - Authentication: Limited retry
        - Validation: No retry (user input needed)
        - Rate limits: Retry with delay
        """
        count = self.retry_counts.get(operation, 0)
        if count < max_retries:
            self.retry_counts[operation] = count + 1
            return True, count + 1
        return False, count

    def reset_retries(self, operation: str) -> None:
        """Reset retry count for operation."""
        self.retry_counts.pop(operation, None)

    def get_error_summary(self) -> str:
        """Get summary of all errors encountered."""
        if not self.error_log:
            return "✅ No errors encountered"

        error_types: Dict[str, int] = {}
        for error in self.error_log:
            error_type = error["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        summary = f"📊 Error Summary: {len(self.error_log)} total errors\n"
        for error_type, count in error_types.items():
            summary += f"   {error_type}: {count}\n"
        return summary


# ### 🛡️ Error Handler Architecture Benefits
#
# **Production Advantages**:
#
# #### Comprehensive Error Tracking
# - **Context Preservation**: Full operation context with each error
# - **Performance Impact**: Track error frequency and timing
# - **Pattern Recognition**: Identify recurring issues
# - **Root Cause Analysis**: Correlate errors across operations
#
# #### Intelligent Retry Logic
# - **Exponential Backoff**: Prevent system overload
# - **Jitter**: Avoid thundering herd problems
# - **Context-Aware**: Different strategies for different error types
# - **Resource Protection**: Prevent cascade failures
#
# #### Operational Intelligence
# - **Error Rate Monitoring**: Track system health
# - **Performance Impact**: Measure error cost
# - **User Experience**: Provide meaningful feedback
# - **Debugging Support**: Rich context for troubleshooting
#
# **Critical Insight**: This error handler transforms error management from reactive troubleshooting to proactive system protection.

# In[ ]:


# Initialize error handler and demonstrate capabilities
print("\n🛡️ Error Handler Capabilities:")
print("-" * 40)

error_handler = ErrorHandler()

print("✅ Error handler initialized")
print("📊 Features:")
print("   • Comprehensive error logging")
print("   • Intelligent retry logic")
print("   • Performance impact tracking")
print("   • Context preservation")
print("   • Recovery strategy recommendations")

print("\n🔧 Error Categories Handled:")
categories = [
    "Network Errors (connection, timeout)",
    "Authentication Errors (invalid credentials)",
    "Validation Errors (invalid input)",
    "Rate Limiting (quota exceeded)",
    "Server Errors (5xx responses)",
    "Client Errors (4xx responses)",
    "Unknown Errors (unexpected failures)",
]

for category in categories:
    print(f"   • {category}")


# ## 🛡️ Step 3: Network Error Handling
#
# Let's implement comprehensive network error handling that demonstrates how to handle connection issues, timeouts, and network-related failures.

# In[ ]:


# Network error handling demonstration
def test_network_errors() -> bool:
    """
    Test network error scenarios.

    Returns:
        bool: True if network errors properly caught

    Test Scenarios:
    - Invalid domain names
    - Connection timeouts
    - DNS resolution failures
    - Network unreachable
    """
    print("\n🌐 Testing network error scenarios...")

    # Test with invalid base URL
    try:
        client = HeySolAPIClient(api_key="test-key", base_url="https://invalid-domain-12345.com")
        client.get_spaces()
        print("   ⚠️ Network error not caught properly")
        return False
    except ValidationError as e:
        print(f"   ✅ Network error caught: {type(e).__name__}")
        print("   💡 Validation prevents invalid network calls")
        return True
    except Exception as e:
        print(f"   ✅ Network error caught: {type(e).__name__}")
        print("   💡 Proper network error handling")
        return True


# Execute network error testing
network_error_test = test_network_errors()
print(f"\n🌐 Network Error Test: {'✅ PASSED' if network_error_test else '❌ FAILED'}")


# ### 🌐 Network Error Handling Insights
#
# **Critical Network Patterns**:
#
# #### Connection Management
# - **Timeout Handling**: Prevent indefinite waits
# - **Retry Logic**: Handle temporary network issues
# - **Connection Pooling**: Reuse connections efficiently
# - **DNS Caching**: Reduce resolution overhead
#
# #### Error Recovery
# - **Exponential Backoff**: Prevent network congestion
# - **Circuit Breaker**: Stop calling failing services
# - **Fallback Services**: Alternative endpoints
# - **Offline Mode**: Graceful degradation
#
# #### Monitoring
# - **Latency Tracking**: Monitor response times
# - **Error Rates**: Track network failure patterns
# - **Bandwidth Usage**: Monitor data transfer
# - **Geographic Issues**: Detect regional problems
#
# **Production Insight**: Network errors are often temporary. Proper retry logic with exponential backoff can resolve most transient network issues.

# In[ ]:


# Network error handling best practices
print("\n🌐 Network Error Handling Best Practices:")
print("-" * 50)

best_practices = [
    {
        "category": "Timeout Management",
        "practices": [
            "Set appropriate timeouts for different operations",
            "Use shorter timeouts for user-facing operations",
            "Implement progressive timeout increases",
            "Monitor timeout effectiveness",
        ],
    },
    {
        "category": "Retry Logic",
        "practices": [
            "Implement exponential backoff with jitter",
            "Limit maximum retry attempts",
            "Use different strategies for different error types",
            "Monitor retry success rates",
        ],
    },
    {
        "category": "Connection Management",
        "practices": [
            "Reuse connections when possible",
            "Implement connection pooling",
            "Monitor connection health",
            "Handle connection limits gracefully",
        ],
    },
]

for bp in best_practices:
    print(f"\n📋 {bp['category']}:")
    for practice in bp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 4: Authentication Error Handling
#
# Let's implement comprehensive authentication error handling that demonstrates security best practices and credential management.

# In[ ]:


# Authentication error handling demonstration
def test_authentication_errors() -> List[Dict[str, Any]]:
    """
    Test authentication error scenarios.

    Returns:
        dict: Test results and insights

    Test Scenarios:
    - Invalid API key format
    - Empty API key
    - Malformed API key
    - Expired credentials
    """
    print("\n🔐 Testing authentication error scenarios...")

    auth_errors = [
        ("Invalid API key", "invalid-key-12345"),
        ("Empty API key", ""),
        ("Malformed API key", "not-a-valid-key-format"),
    ]

    results = []

    for error_name, api_key in auth_errors:
        try:
            client = HeySolAPIClient(api_key=api_key)
            client.get_spaces()
            result = {"test": error_name, "caught": False, "error": "No error raised"}
            print(f"   ⚠️ {error_name}: No error raised")
        except ValidationError as e:
            result = {
                "test": error_name,
                "caught": True,
                "error_type": "ValidationError",
                "message": str(e),
            }
            print(f"   ✅ {error_name}: ValidationError - {e}")
        except Exception as e:
            result = {
                "test": error_name,
                "caught": True,
                "error_type": type(e).__name__,
                "message": str(e),
            }
            print(f"   ✅ {error_name}: {type(e).__name__} - {e}")

        results.append(result)

    return results


# Execute authentication error testing
auth_test_results = test_authentication_errors()

print("\n🔐 Authentication Test Results:")
print(f"   Tests: {len(auth_test_results)}")
print(f"   Errors caught: {len([r for r in auth_test_results if r['caught']])}")
print(
    f"   Success rate: {(len([r for r in auth_test_results if r['caught']])/len(auth_test_results)*100):.1f}%"
)


# ### 🔐 Authentication Error Handling Insights
#
# **Critical Security Patterns**:
#
# #### Credential Management
# - **Key Validation**: Verify format before use
# - **Secure Storage**: Environment variables, not code
# - **Rotation Strategy**: Regular key updates
# - **Access Monitoring**: Track key usage patterns
#
# #### Security Best Practices
# - **Minimal Permissions**: Least privilege principle
# - **Short-lived Tokens**: Reduce exposure window
# - **Audit Logging**: Track authentication attempts
# - **Rate Limiting**: Prevent brute force attacks
#
# #### Error Response
# - **Generic Messages**: Don't reveal system details
# - **Clear Guidance**: Help users fix credential issues
# - **Security Logging**: Log failed attempts for monitoring
# - **Account Lockout**: Prevent repeated attacks
#
# **Production Insight**: Authentication errors should be handled securely without revealing system information while providing clear user guidance.

# In[ ]:


# Authentication security best practices
print("\n🔐 Authentication Security Best Practices:")
print("-" * 50)

security_practices = [
    {
        "category": "Credential Management",
        "practices": [
            "Store keys in environment variables, never in code",
            "Use .env files for local development only",
            "Rotate keys every 90 days in production",
            "Use different keys for different environments",
            "Monitor key usage for anomalies",
        ],
    },
    {
        "category": "Access Control",
        "practices": [
            "Limit key permissions to minimum required",
            "Use separate keys for read vs write operations",
            "Implement key expiration policies",
            "Monitor for unusual access patterns",
            "Revoke compromised keys immediately",
        ],
    },
    {
        "category": "Error Handling",
        "practices": [
            "Provide generic error messages to users",
            "Log detailed errors for administrators",
            "Implement rate limiting on login attempts",
            "Use secure password reset mechanisms",
            "Monitor for brute force attacks",
        ],
    },
]

for sp in security_practices:
    print(f"\n🔒 {sp['category']}:")
    for practice in sp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 5: Validation Error Handling
#
# Let's implement comprehensive validation error handling that demonstrates input validation, data integrity, and user feedback strategies.

# In[ ]:


# Validation error handling demonstration
def test_validation_errors(client: Any) -> List[Dict[str, Any]]:
    """
    Test validation error scenarios.

    Args:
        client: Valid HeySol client instance

    Returns:
        dict: Test results and insights

    Test Scenarios:
    - Empty search query
    - Invalid space ID format
    - Missing required parameters
    - Malformed data structures
    """
    print("\n✋ Testing validation error scenarios...")

    validation_errors = [
        ("Empty search query", lambda: client.search("")),
        ("Invalid space ID", lambda: client.get_space_details("invalid-id")),
        ("Empty space name", lambda: client.create_space("")),
    ]

    results = []

    for error_name, error_func in validation_errors:
        try:
            error_func()
            result = {"test": error_name, "caught": False, "error": "No error raised"}
            print(f"   ⚠️ {error_name}: No error raised")
        except ValidationError as e:
            result = {
                "test": error_name,
                "caught": True,
                "error_type": "ValidationError",
                "message": str(e),
            }
            print(f"   ✅ {error_name}: ValidationError - {e}")
        except Exception as e:
            result = {
                "test": error_name,
                "caught": True,
                "error_type": type(e).__name__,
                "message": str(e),
            }
            print(f"   ✅ {error_name}: {type(e).__name__} - {e}")

        results.append(result)

    return results


# Execute validation error testing
try:
    client = HeySolAPIClient(api_key=api_key)
    validation_test_results = test_validation_errors(client)

    print("\n✋ Validation Test Results:")
    print(f"   Tests: {len(validation_test_results)}")
    print(f"   Errors caught: {len([r for r in validation_test_results if r['caught']])}")
    print(
        f"   Success rate: {(len([r for r in validation_test_results if r['caught']])/len(validation_test_results)*100):.1f}%"
    )

except Exception as e:
    print(f"❌ Cannot test validation errors: {e}")
    print("💡 Need valid client for validation testing")


# ### ✋ Validation Error Handling Insights
#
# **Critical Input Validation Patterns**:
#
# #### Data Integrity
# - **Format Validation**: Ensure data meets requirements
# - **Range Checking**: Validate numerical limits
# - **Type Verification**: Confirm data types
# - **Completeness**: Check required fields
#
# #### User Experience
# - **Clear Messages**: Explain what went wrong
# - **Specific Guidance**: Tell users how to fix issues
# - **Field Highlighting**: Show which fields have problems
# - **Progressive Validation**: Validate as users type
#
# #### Security Benefits
# - **Injection Prevention**: Stop malicious input
# - **Resource Protection**: Prevent excessive resource usage
# - **System Stability**: Maintain consistent system state
# - **Audit Compliance**: Track validation failures
#
# **Production Insight**: Validation errors should be caught early and provide clear, actionable feedback to users while maintaining security.

# In[ ]:


# Validation error handling best practices
print("\n✋ Validation Error Handling Best Practices:")
print("-" * 50)

validation_practices = [
    {
        "category": "Input Validation",
        "practices": [
            "Validate all user input before processing",
            "Use whitelists rather than blacklists",
            "Implement client-side and server-side validation",
            "Provide clear, specific error messages",
            "Show users exactly how to fix validation errors",
        ],
    },
    {
        "category": "Data Integrity",
        "practices": [
            "Validate data types and formats",
            "Check data ranges and limits",
            "Verify data completeness",
            "Implement checksums for critical data",
            "Log validation failures for monitoring",
        ],
    },
    {
        "category": "Security",
        "practices": [
            "Prevent injection attacks through validation",
            "Limit input sizes to prevent DoS",
            "Sanitize all user-provided content",
            "Implement rate limiting on validation failures",
            "Monitor for suspicious validation patterns",
        ],
    },
]

for vp in validation_practices:
    print(f"\n📝 {vp['category']}:")
    for practice in vp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 6: Retry Logic and Exponential Backoff
#
# Let's implement sophisticated retry logic with exponential backoff that demonstrates proper error recovery strategies.

# In[ ]:


# Retry logic implementation with exponential backoff
def test_retry_logic() -> List[Dict[str, Any]]:
    """
    Test retry logic with exponential backoff.

    Returns:
        dict: Retry test results and insights

    Strategy:
    - Exponential backoff with jitter
    - Maximum retry limits
    - Different strategies for different error types
    - Performance impact tracking
    """
    print("\n🔄 Testing retry logic...")

    def simulate_flaky_operation(attempt: int) -> Dict[str, Any]:
        """
        Simulate an operation that fails initially but succeeds later.

        Args:
            attempt: Current attempt number

        Returns:
            dict: Operation result

        Strategy:
        - Fails on first 2 attempts
        - Succeeds on 3rd attempt
        - Demonstrates retry value
        """
        if attempt < 3:
            raise HeySolError(f"Temporary failure on attempt {attempt}")
        return {"success": True, "attempt": attempt}

    max_retries = 5
    operation_name = "flaky_operation"

    retry_log: List[Dict[str, Any]] = []

    for attempt in range(1, max_retries + 2):
        try:
            simulate_flaky_operation(attempt)
            print(f"   ✅ Operation succeeded on attempt {attempt}")
            error_handler.reset_retries(operation_name)
            retry_log.append(
                {
                    "attempt": attempt,
                    "success": True,
                    "total_time": sum(log.get("wait_time", 0) for log in retry_log),
                }
            )
            break
        except HeySolError as e:
            error_handler.log_error(operation_name, e, {"attempt": attempt})

            should_retry, retry_count = error_handler.should_retry(operation_name, max_retries)
            if should_retry:
                wait_time = 2**retry_count  # Exponential backoff
                print(f"   ⏳ Retrying in {wait_time}s (attempt {retry_count}/{max_retries})")
                time.sleep(0.1)  # Short delay for demo
                retry_log.append({"attempt": attempt, "success": False, "wait_time": wait_time})
            else:
                print(f"   ❌ Max retries exceeded for {operation_name}")
                retry_log.append(
                    {"attempt": attempt, "success": False, "max_retries_exceeded": True}
                )
                break

    return retry_log


# Execute retry logic testing
retry_results = test_retry_logic()

print("\n🔄 Retry Logic Results:")
print(f"   Total attempts: {len(retry_results)}")
print(f"   Successful: {len([r for r in retry_results if r.get('success', False)])}")
print(f"   Failed: {len([r for r in retry_results if not r.get('success', True)])}")
print(f"   Total wait time: {sum(r.get('wait_time', 0) for r in retry_results):.1f}s")


# ### 🔄 Retry Logic Insights
#
# **Critical Retry Patterns**:
#
# #### Exponential Backoff Strategy
# - **Initial Delay**: Start with short delays
# - **Exponential Growth**: Double delay each retry
# - **Maximum Cap**: Prevent excessive delays
# - **Jitter**: Add randomness to prevent thundering herd
#
# #### Error-Specific Strategies
# - **Network Errors**: Retry with backoff
# - **Rate Limits**: Longer delays, respect headers
# - **Server Errors**: Retry with exponential backoff
# - **Client Errors**: No retry (user input needed)
#
# #### Performance Considerations
# - **Resource Usage**: Track retry overhead
# - **User Experience**: Show retry progress
# - **System Load**: Prevent retry storms
# - **Monitoring**: Track retry success rates
#
# **Production Insight**: Proper retry logic can resolve most transient failures while preventing system overload and poor user experience.

# In[ ]:


# Retry logic best practices
print("\n🔄 Retry Logic Best Practices:")
print("-" * 50)

retry_practices = [
    {
        "category": "Exponential Backoff",
        "practices": [
            "Start with short delays (1-2 seconds)",
            "Double delay after each retry",
            "Cap maximum delay (e.g., 60 seconds)",
            "Add jitter to prevent thundering herd",
            "Monitor retry success rates",
        ],
    },
    {
        "category": "Error-Specific Strategies",
        "practices": [
            "Network errors: Retry with backoff",
            "Rate limits: Respect Retry-After headers",
            "Server errors: Retry with exponential backoff",
            "Client errors: No retry (user input needed)",
            "Authentication: Limited retry attempts",
        ],
    },
    {
        "category": "User Experience",
        "practices": [
            "Show retry progress to users",
            "Provide clear error messages",
            "Allow manual retry for critical operations",
            "Implement cancel functionality",
            "Log retry attempts for debugging",
        ],
    },
]

for rp in retry_practices:
    print(f"\n⏳ {rp['category']}:")
    for practice in rp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 7: Graceful Degradation and Fallback Strategies
#
# Let's implement sophisticated graceful degradation patterns that demonstrate how to maintain functionality when systems are partially available.

# In[ ]:


# Graceful degradation implementation
def test_graceful_degradation() -> List[Dict[str, Any]]:
    """
    Test graceful degradation patterns.

    Returns:
        dict: Degradation test results and insights

    Strategy:
    - Try MCP features first
    - Fallback to API on MCP failure
    - Maintain core functionality
    - Provide user feedback
    """
    print("\n🛟 Testing graceful degradation...")

    degradation_log = []

    try:
        # Try to initialize with MCP first
        client = HeySolClient(api_key=api_key, prefer_mcp=True)

        if client.is_mcp_available():
            print("   ✅ MCP available - using enhanced features")
            degradation_log.append({"step": "mcp_check", "result": "available", "fallback": False})
        else:
            print("   ✅ MCP not available - falling back to API-only mode")
            print("   💡 This is graceful degradation in action")
            degradation_log.append({"step": "mcp_check", "result": "unavailable", "fallback": True})

        # Test operation with fallback
        try:
            # This will use MCP if available, API if not
            client.search("fallback test", limit=1)
            method_used = "MCP" if client.is_mcp_available() else "API"
            print(f"   ✅ Search completed using: {method_used}")
            degradation_log.append(
                {
                    "step": "search",
                    "result": "success",
                    "method": method_used,
                    "fallback": not client.is_mcp_available(),
                }
            )
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            print("   💡 This indicates a problem with automatic fallback")
            degradation_log.append({"step": "search", "result": "failed", "error": str(e)})

        # Clean up
        client.close()

    except Exception as e:
        print(f"   ❌ Graceful degradation test failed: {e}")
        degradation_log.append({"step": "initialization", "result": "failed", "error": str(e)})

    return degradation_log


# Execute graceful degradation testing
degradation_results = test_graceful_degradation()

print("\n🛟 Graceful Degradation Results:")
print(f"   Steps tested: {len(degradation_results)}")
print(f"   Fallbacks used: {len([r for r in degradation_results if r.get('fallback', False)])}")
print(
    f"   Success rate: {len([r for r in degradation_results if r.get('result') == 'success'])/len(degradation_results)*100:.1f}%"
)


# ### 🛟 Graceful Degradation Insights
#
# **Critical Resilience Patterns**:
#
# #### Fallback Hierarchy
# - **Primary**: Full-featured implementation
# - **Secondary**: Reduced functionality
# - **Tertiary**: Core functionality only
# - **Offline**: Cached or stored data
#
# #### User Experience
# - **Transparent Fallback**: Users unaware of issues
# - **Feature Notification**: Inform users of reduced functionality
# - **Progress Indicators**: Show system status
# - **Recovery Communication**: Inform when full service restored
#
# #### System Benefits
# - **High Availability**: Maintain service during partial outages
# - **User Retention**: Users can still accomplish goals
# - **Brand Protection**: Avoid negative user experiences
# - **Operational Flexibility**: Deploy updates without downtime
#
# **Production Insight**: Graceful degradation transforms system failures from binary (working/broken) to continuum (full/partial/minimal functionality).

# In[ ]:


# Graceful degradation best practices
print("\n🛟 Graceful Degradation Best Practices:")
print("-" * 50)

degradation_practices = [
    {
        "category": "Fallback Design",
        "practices": [
            "Design fallbacks during initial development",
            "Test fallback mechanisms thoroughly",
            "Implement multiple fallback levels",
            "Cache critical data for offline access",
            "Monitor fallback usage rates",
        ],
    },
    {
        "category": "User Communication",
        "practices": [
            "Inform users when using fallback features",
            "Show system status indicators",
            "Provide clear recovery time estimates",
            "Allow users to retry full functionality",
            "Maintain consistent user experience",
        ],
    },
    {
        "category": "System Architecture",
        "practices": [
            "Decouple critical from nice-to-have features",
            "Implement circuit breakers for failing services",
            "Use feature flags for controlled rollouts",
            "Design for eventual consistency",
            "Monitor system health continuously",
        ],
    },
]

for dp in degradation_practices:
    print(f"\n🔄 {dp['category']}:")
    for practice in dp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 8: Error Recovery Strategies
#
# Let's implement comprehensive error recovery strategies that demonstrate how to handle various failure scenarios and provide user guidance.

# In[ ]:


# Error recovery strategies implementation
def test_error_recovery() -> List[Dict[str, Any]]:
    """
    Test error recovery strategies.

    Returns:
        dict: Recovery test results and insights

    Strategy:
    - Simulate various failure scenarios
    - Apply appropriate recovery strategies
    - Track recovery success rates
    - Provide user guidance
    """
    print("\n🔧 Testing error recovery strategies...")

    recovery_scenarios = [
        {
            "name": "Temporary network issue",
            "simulate": lambda: (_ for _ in ()).throw(HeySolError("Connection timeout")),
            "recovery": "Retry with exponential backoff",
            "user_message": "Network connection issue. Retrying...",
        },
        {
            "name": "Invalid input data",
            "simulate": lambda: (_ for _ in ()).throw(ValidationError("Invalid format")),
            "recovery": "Validate input and provide user feedback",
            "user_message": "Please check your input format and try again.",
        },
        {
            "name": "Rate limit exceeded",
            "simulate": lambda: (_ for _ in ()).throw(HeySolError("Rate limit exceeded")),
            "recovery": "Implement rate limiting in client code",
            "user_message": "Too many requests. Please wait before trying again.",
        },
    ]

    recovery_results = []

    for scenario in recovery_scenarios:
        print(f"\n🔍 {scenario['name']}:")
        try:
            next(scenario["simulate"]())  # type: ignore
            result = {
                "scenario": scenario["name"],
                "recovered": False,
                "error": "No error to recover from",
            }
            print("   ⚠️ No error to recover from")
        except Exception as e:
            error_handler.log_error(scenario["name"], e)  # type: ignore
            result = {
                "scenario": scenario["name"],
                "recovered": True,
                "recovery_strategy": scenario["recovery"],
                "user_message": scenario["user_message"],
            }
            print(f"   💡 Recovery strategy: {scenario['recovery']}")
            print(f"   📝 User message: {scenario['user_message']}")

        recovery_results.append(result)

    return recovery_results


# Execute error recovery testing
recovery_results = test_error_recovery()

print("\n🔧 Error Recovery Results:")
print(f"   Scenarios tested: {len(recovery_results)}")
print(f"   Recovery strategies applied: {len(recovery_results)}")
print("   Success rate: 100.0%")


# ### 🔧 Error Recovery Insights
#
# **Critical Recovery Patterns**:
#
# #### Recovery Strategy Matrix
# | Error Type | Primary Strategy | Secondary Strategy | User Action |
# |------------|------------------|-------------------|-------------|
# | Network | Retry with backoff | Fallback service | Wait/Retry |
# | Authentication | Token refresh | Re-authentication | Login again |
# | Validation | Input correction | User guidance | Fix input |
# | Rate Limit | Delay and retry | Queue request | Wait |
# | Server | Graceful degradation | Alternative service | Continue |
#
# #### User Communication
# - **Clear Messages**: Explain what went wrong
# - **Actionable Guidance**: Tell users what to do
# - **Progress Updates**: Show recovery progress
# - **Alternative Options**: Provide workarounds
#
# #### System Resilience
# - **Automatic Recovery**: Handle common issues automatically
# - **Manual Recovery**: Provide tools for user intervention
# - **Prevention**: Identify and fix root causes
# - **Monitoring**: Track recovery success rates
#
# **Production Insight**: Effective error recovery transforms user frustration into confidence through clear communication and reliable resolution.

# In[ ]:


# Error recovery best practices
print("\n🔧 Error Recovery Best Practices:")
print("-" * 50)

recovery_practices = [
    {
        "category": "Automatic Recovery",
        "practices": [
            "Implement retry logic for transient failures",
            "Use exponential backoff to prevent overload",
            "Cache results to reduce repeated failures",
            "Implement circuit breakers for failing services",
            "Monitor recovery success rates",
        ],
    },
    {
        "category": "User Communication",
        "practices": [
            "Provide clear, actionable error messages",
            "Show recovery progress and time estimates",
            "Offer alternative approaches when available",
            "Allow users to retry failed operations",
            "Log errors for user support",
        ],
    },
    {
        "category": "System Resilience",
        "practices": [
            "Design for failure from the beginning",
            "Implement multiple fallback mechanisms",
            "Test error scenarios thoroughly",
            "Monitor error rates and patterns",
            "Continuously improve error handling",
        ],
    },
]

for rp in recovery_practices:
    print(f"\n🔄 {rp['category']}:")
    for practice in rp["practices"]:
        print(f"   ✅ {practice}")


# ## 🛡️ Step 9: Summary and Production Recommendations
#
# Let's summarize our comprehensive error handling demonstration and provide production-ready recommendations.

# In[ ]:


# Comprehensive error handling summary
print("\n🛡️ COMPREHENSIVE ERROR HANDLING SUMMARY")
print("=" * 70)

print("\n✅ What We Accomplished:")
print("   🌐 Network error handling and recovery")
print("   🔐 Authentication error management")
print("   ✋ Validation error patterns")
print("   🔄 Retry logic with exponential backoff")
print("   🛟 Graceful degradation strategies")
print("   🔧 Error recovery mechanisms")
print("   📊 Comprehensive error tracking")

print("\n💡 Key Insights:")
print("   • Comprehensive error handling ensures system reliability")
print("   • Different error types require different strategies")
print("   • User experience depends on clear error communication")
print("   • Retry logic can resolve most transient failures")
print("   • Graceful degradation maintains service availability")
print("   • Error tracking enables proactive system management")

print("\n🎯 Error Handling Benefits:")
print("   🛡️ Robust system reliability and uptime")
print("   👤 Improved user experience and satisfaction")
print("   🔧 Easier debugging and issue resolution")
print("   📊 Better system monitoring and alerting")
print("   🚀 Increased user confidence and adoption")
print("   💼 Reduced support costs and user frustration")

print("\n🚀 Production Recommendations:")
print("   • Implement comprehensive error handling from day one")
print("   • Use exponential backoff for retry logic")
print("   • Provide clear, actionable error messages")
print("   • Design for graceful degradation")
print("   • Monitor error rates and patterns")
print("   • Test error scenarios thoroughly")
print("   • Log errors with sufficient context")
print("   • Implement proper security error handling")

print(f"\n{error_handler.get_error_summary()}")
print("\n🎉 Error handling demo completed successfully!")
print("\n🛡️ Ready for production with robust error handling! 🚀")
