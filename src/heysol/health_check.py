"""
Health check utilities for HeySol API endpoints.

This module provides comprehensive health checking capabilities for all HeySol API endpoints,
including MCP protocol validation and detailed status reporting.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from .clients.api_client import HeySolAPIClient
from .clients.mcp_client import HeySolMCPClient
from .exceptions import HeySolError


@dataclass
class EndpointStatus:
    """Status information for a single API endpoint."""
    name: str
    endpoint: str
    method: str
    status: str  # 'healthy', 'degraded', 'unhealthy', 'unknown'
    response_time: float
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class HealthCheckResult:
    """Comprehensive health check results."""
    timestamp: float
    overall_status: str  # 'healthy', 'degraded', 'unhealthy'
    api_client_status: str
    mcp_client_status: str
    endpoints: List[EndpointStatus]
    summary: Dict[str, Any]


class HeySolHealthChecker:
    """
    Comprehensive health checker for HeySol API endpoints.

    Tests all available endpoints and provides detailed status reporting
    for monitoring and debugging purposes.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the health checker.

        Args:
            api_key: HeySol API key (optional, will use environment if not provided)
        """
        self.api_key = api_key
        self.api_client: Optional[HeySolAPIClient] = None
        self.mcp_client: Optional[HeySolMCPClient] = None

    def _initialize_clients(self) -> Tuple[bool, bool]:
        """Initialize API and MCP clients. Returns (api_success, mcp_success)."""
        api_success = False
        mcp_success = False

        try:
            self.api_client = HeySolAPIClient(api_key=self.api_key)
            api_success = True
        except Exception as e:
            print(f"DEBUG: API client init failed: {e}")
            self.api_client = None

        try:
            self.mcp_client = HeySolMCPClient(api_key=self.api_key)
            mcp_success = True
        except Exception as e:
            print(f"DEBUG: MCP client init failed: {e}")
            self.mcp_client = None

        return api_success, mcp_success

    def _test_api_endpoint(
        self,
        name: str,
        method_name: str,
        *args: Any,
        **kwargs: Any
    ) -> EndpointStatus:
        """Test a single API endpoint."""
        if not self.api_client:
            return EndpointStatus(
                name=name,
                endpoint=f"api:{method_name}",
                method="API",
                status="unknown",
                response_time=0.0,
                error_message="API client not available"
            )

        start_time = time.time()
        try:
            method = getattr(self.api_client, method_name)
            result = method(*args, **kwargs)
            response_time = time.time() - start_time

            # Determine status based on result
            if isinstance(result, dict) and "error" not in result:
                status = "healthy"
                details = {"result_type": type(result).__name__}
                # Check if result contains episodes (list-like content)
                if "episodes" in result:
                    episodes_list = result.get("episodes", [])
                    if isinstance(episodes_list, list):
                        details["episodes_count"] = str(len(episodes_list))
            else:
                status = "degraded"
                details = {"result": str(result)[:100]}

            return EndpointStatus(
                name=name,
                endpoint=f"api:{method_name}",
                method="API",
                status=status,
                response_time=response_time,
                details=details
            )

        except Exception as e:
            response_time = time.time() - start_time
            return EndpointStatus(
                name=name,
                endpoint=f"api:{method_name}",
                method="API",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )

    def _test_mcp_endpoint(
        self,
        name: str,
        method_name: str,
        *args: Any,
        **kwargs: Any
    ) -> EndpointStatus:
        """Test a single MCP endpoint."""
        if not self.mcp_client:
            return EndpointStatus(
                name=name,
                endpoint=f"mcp:{method_name}",
                method="MCP",
                status="unknown",
                response_time=0.0,
                error_message="MCP client not available"
            )

        start_time = time.time()
        try:
            method = getattr(self.mcp_client, method_name)
            result = method(*args, **kwargs)
            response_time = time.time() - start_time

            # Determine status based on result
            if result is not None:
                status = "healthy"
                details = {"result_type": type(result).__name__}
                # Check if result contains episodes (list-like content)
                if isinstance(result, dict) and "episodes" in result:
                    episodes_list = result.get("episodes", [])
                    if isinstance(episodes_list, list):
                        details["episodes_count"] = str(len(episodes_list))

            return EndpointStatus(
                name=name,
                endpoint=f"mcp:{method_name}",
                method="MCP",
                status=status,
                response_time=response_time,
                details=details
            )

        except Exception as e:
            response_time = time.time() - start_time
            return EndpointStatus(
                name=name,
                endpoint=f"mcp:{method_name}",
                method="MCP",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )

    def run_comprehensive_health_check(self) -> HealthCheckResult:
        """
        Run a comprehensive health check of all HeySol endpoints.

        Returns:
            HealthCheckResult: Detailed health check results
        """
        start_time = time.time()

        # Initialize clients
        api_success, mcp_success = self._initialize_clients()

        endpoints: List[EndpointStatus] = []

        # Test API endpoints
        if api_success:
            api_endpoints: List[tuple] = [
                ("Spaces Discovery", "get_spaces"),
                ("Search", "search", "test", None, 1),
                ("Ingestion", "ingest", "Health check test message"),
                ("Log Retrieval", "get_ingestion_logs"),
            ]

            for endpoint_info in api_endpoints:
                name: str = endpoint_info[0]
                method_name: str = endpoint_info[1]
                args = endpoint_info[2:] if len(endpoint_info) > 2 else ()
                status = self._test_api_endpoint(name, method_name, *args)
                endpoints.append(status)

        # Test MCP endpoints
        if mcp_success:
            mcp_endpoints: List[tuple] = [
                ("MCP Spaces", "get_spaces"),
                ("MCP Search", "search", "test", 1),
                ("MCP Ingestion", "ingest", "MCP health check test"),
                ("MCP Tools", "get_available_tools"),
            ]

            for endpoint_info in mcp_endpoints:
                mcp_name: str = endpoint_info[0]
                mcp_method_name: str = endpoint_info[1]
                args = endpoint_info[2:] if len(endpoint_info) > 2 else ()
                status = self._test_mcp_endpoint(mcp_name, mcp_method_name, *args)
                endpoints.append(status)

        # Calculate overall status
        healthy_count = sum(1 for e in endpoints if e.status == "healthy")
        degraded_count = sum(1 for e in endpoints if e.status == "degraded")
        unhealthy_count = sum(1 for e in endpoints if e.status == "unhealthy")

        if unhealthy_count > 0:
            overall_status = "unhealthy"
        elif degraded_count > 0:
            overall_status = "degraded"
        elif healthy_count > 0:
            overall_status = "healthy"
        else:
            overall_status = "unknown"

        # Create summary
        summary = {
            "total_endpoints": len(endpoints),
            "healthy_endpoints": healthy_count,
            "degraded_endpoints": degraded_count,
            "unhealthy_endpoints": unhealthy_count,
            "api_client_available": api_success,
            "mcp_client_available": mcp_success,
            "total_response_time": sum(e.response_time for e in endpoints),
            "average_response_time": sum(e.response_time for e in endpoints) / len(endpoints) if endpoints else 0,
        }

        return HealthCheckResult(
            timestamp=start_time,
            overall_status=overall_status,
            api_client_status="healthy" if api_success else "unhealthy",
            mcp_client_status="healthy" if mcp_success else "unhealthy",
            endpoints=endpoints,
            summary=summary
        )

    def print_health_report(self, result: HealthCheckResult) -> None:
        """Print a formatted health check report."""
        print("🔍 HeySol API Health Check Report")
        print("=" * 50)
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result.timestamp))}")
        print(f"Overall Status: {result.overall_status.upper()}")
        print(f"API Client: {result.api_client_status.upper()}")
        print(f"MCP Client: {result.mcp_client_status.upper()}")
        print()

        print("📊 Summary:")
        print(f"   Total Endpoints Tested: {result.summary['total_endpoints']}")
        print(f"   Healthy: {result.summary['healthy_endpoints']}")
        print(f"   Degraded: {result.summary['degraded_endpoints']}")
        print(f"   Unhealthy: {result.summary['unhealthy_endpoints']}")
        print(f"   Average Response Time: {result.summary['average_response_time']:.3f}s")
        print()

        print("🔧 Endpoint Details:")
        for endpoint in result.endpoints:
            status_emoji = {
                "healthy": "✅",
                "degraded": "⚠️",
                "unhealthy": "❌",
                "unknown": "❓"
            }.get(endpoint.status, "❓")

            print(f"   {status_emoji} {endpoint.name} ({endpoint.method})")
            print(f"   Response Time: {endpoint.response_time:.3f}s")
            if endpoint.error_message:
                print(f"      Error: {endpoint.error_message[:100]}...")
            if endpoint.details:
                for key, value in endpoint.details.items():
                    if key == "result":
                        # Skip printing the full result as it's usually too verbose
                        # We'll still show other details like result_type, count, etc.
                        continue
                    elif isinstance(value, (int, float)):
                        # Format numeric values appropriately
                        if key == "count" or key == "episodes_count":
                            print(f"      {key}: {value}")
                        else:
                            print(f"      {key}: {value:.3f}" if isinstance(value, float) else f"      {key}: {value}")
                    else:
                        print(f"      {key}: {value}")
            print()


def run_health_check(api_key: Optional[str] = None) -> HealthCheckResult:
    """
    Convenience function to run a health check.

    Args:
        api_key: HeySol API key (optional, will use environment/.env if not provided)

    Returns:
        HealthCheckResult: Health check results
    """
    # If no API key provided, try to get from environment or .env file
    if api_key is None:
        import os
        api_key = os.getenv("HEYSOL_API_KEY")
        if not api_key:
            # Try loading from .env file
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv("HEYSOL_API_KEY")
            except ImportError:
                pass  # dotenv not available

    checker = HeySolHealthChecker(api_key=api_key)
    return checker.run_comprehensive_health_check()


def print_health_check_report(api_key: Optional[str] = None) -> None:
    """
    Convenience function to run and print a health check report.

    Args:
        api_key: HeySol API key (optional)
    """
    result = run_health_check(api_key)
    checker = HeySolHealthChecker()
    checker.print_health_report(result)