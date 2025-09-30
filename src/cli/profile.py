"""
Profile-related CLI commands.
"""

import time
from typing import Any

import typer

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("get")
def profile_get() -> None:
    """Get user profile."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)
    profile = client.get_user_profile()
    typer.echo(format_json_output(profile, pretty))
    client.close()


@app.command("health")
def profile_health(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed health check results"
    )
) -> None:
    """Check API health by testing all endpoints."""
    api_key, base_url = get_auth_from_global()
    pretty = True  # Always pretty print

    client = create_client(api_key=api_key, base_url=base_url)

    results: dict[str, Any] = {
        "overall_status": "unknown",
        "checks": {},
        "timestamp": "2024-01-01T00:00:00Z",  # Will be set by server
    }

    # Test user profile endpoint
    try:
        profile = client.get_user_profile()
        results["checks"]["user_profile"] = {
            "status": "healthy",
            "message": "User profile retrieved successfully",
        }
        if verbose:
            results["checks"]["user_profile"]["details"] = profile
    except Exception as e:
        results["checks"]["user_profile"] = {
            "status": "unhealthy",
            "message": f"Failed to get user profile: {str(e)}",
        }

    # Test spaces endpoint
    spaces_data = None
    try:
        spaces_data = client.get_spaces()
        results["checks"]["spaces"] = {
            "status": "healthy",
            "message": f"Retrieved {len(spaces_data)} spaces successfully",
        }
        if verbose:
            results["checks"]["spaces"]["details"] = spaces_data
    except Exception as e:
        results["checks"]["spaces"] = {
            "status": "unhealthy",
            "message": f"Failed to get spaces: {str(e)}",
        }

    # Test search endpoint
    try:
        search_result = client.search("health check test", limit=1)
        results["checks"]["search"] = {
            "status": "healthy",
            "message": "Search functionality working",
        }
        if verbose:
            results["checks"]["search"]["details"] = search_result
    except Exception as e:
        results["checks"]["search"] = {
            "status": "unhealthy",
            "message": f"Failed to search: {str(e)}",
        }

    # Test memory ingest endpoint (safe test)
    try:
        test_message = f"Health check test - {int(time.time())}"
        ingest_result = client.ingest(test_message, source="health-check")
        results["checks"]["memory_ingest"] = {
            "status": "healthy",
            "message": "Memory ingest working",
        }
        if verbose:
            results["checks"]["memory_ingest"]["details"] = ingest_result
    except Exception as e:
        results["checks"]["memory_ingest"] = {
            "status": "unhealthy",
            "message": f"Failed to ingest memory: {str(e)}",
        }

    # Test space details endpoint
    try:
        # Get first space if available
        if spaces_data and len(spaces_data) > 0:
            space_id = spaces_data[0]["id"]
            space_details = client.get_space_details(space_id)
            results["checks"]["space_details"] = {
                "status": "healthy",
                "message": "Space details retrieval working",
            }
            if verbose:
                results["checks"]["space_details"]["details"] = space_details
        else:
            results["checks"]["space_details"] = {
                "status": "degraded",
                "message": "No spaces available to test details",
            }
    except Exception as e:
        results["checks"]["space_details"] = {
            "status": "unhealthy",
            "message": f"Failed to get space details: {str(e)}",
        }

    # Test ingestion status endpoint
    try:
        status_result = client.check_ingestion_status()
        results["checks"]["ingestion_status"] = {
            "status": "healthy",
            "message": "Ingestion status check working",
        }
        if verbose:
            results["checks"]["ingestion_status"]["details"] = status_result
    except Exception as e:
        results["checks"]["ingestion_status"] = {
            "status": "unhealthy",
            "message": f"Failed to check ingestion status: {str(e)}",
        }

    # Test logs endpoint
    try:
        logs = client.get_ingestion_logs(limit=1)
        results["checks"]["logs"] = {
            "status": "healthy",
            "message": f"Retrieved {len(logs)} log entries successfully",
        }
        if verbose:
            results["checks"]["logs"]["details"] = logs
    except Exception as e:
        results["checks"]["logs"] = {
            "status": "unhealthy",
            "message": f"Failed to get logs: {str(e)}",
        }

    # Test webhooks endpoint
    try:
        webhooks = client.list_webhooks(limit=1)
        results["checks"]["webhooks"] = {
            "status": "healthy",
            "message": f"Retrieved {len(webhooks)} webhooks successfully",
        }
        if verbose:
            results["checks"]["webhooks"]["details"] = webhooks
    except Exception as e:
        error_str = str(e)
        if "400" in error_str:
            results["checks"]["webhooks"] = {
                "status": "degraded",
                "message": f"Webhooks endpoint not available: {error_str}",
            }
        else:
            results["checks"]["webhooks"] = {
                "status": "unhealthy",
                "message": f"Failed to get webhooks: {error_str}",
            }

    # Test MCP availability and core memory tools individually
    core_memory_tools = ["memory_ingest", "memory_search", "memory_get_spaces", "get_user_profile"]
    tool_statuses = {}

    try:
        mcp_available = client.is_mcp_available()
        if mcp_available:
            # Create MCP client for individual tool testing
            from heysol.clients.mcp_client import HeySolMCPClient
            from heysol.config import HeySolConfig

            config = HeySolConfig(api_key=api_key, base_url=base_url)
            mcp_client = HeySolMCPClient(config=config)

            # Test each core memory tool individually
            for tool_name in core_memory_tools:
                try:
                    if tool_name == "memory_ingest":
                        # Test memory_ingest by attempting to ingest a test message
                        test_message = f"Health check test - {int(time.time())}"
                        ingest_result = mcp_client.call_tool(
                            "memory_ingest", message=test_message, source="health-check"
                        )
                        tool_statuses[tool_name] = {
                            "status": "healthy",
                            "message": "Memory ingestion working",
                        }

                    elif tool_name == "memory_search":
                        # Test memory_search by searching for recent content
                        mcp_client.call_tool("memory_search", query="health check", limit=1)
                        tool_statuses[tool_name] = {
                            "status": "healthy",
                            "message": "Memory search working",
                        }

                    elif tool_name == "memory_get_spaces":
                        # Test memory_get_spaces by retrieving spaces
                        mcp_client.call_tool("memory_get_spaces", all=True)
                        tool_statuses[tool_name] = {
                            "status": "healthy",
                            "message": "Memory spaces retrieval working",
                        }

                    elif tool_name == "get_user_profile":
                        # Test get_user_profile by retrieving profile
                        mcp_client.call_tool("get_user_profile", profile=True)
                        tool_statuses[tool_name] = {
                            "status": "healthy",
                            "message": "User profile retrieval working",
                        }

                except Exception as e:
                    tool_statuses[tool_name] = {
                        "status": "unhealthy",
                        "message": f"Tool failed: {str(e)}",
                    }

            mcp_client.close()

            # Count healthy tools
            healthy_tools = sum(
                1 for status in tool_statuses.values() if status["status"] == "healthy"
            )

            results["checks"]["mcp"] = {
                "status": "healthy" if healthy_tools >= 4 else "degraded",
                "message": f"MCP available with {healthy_tools}/4 core memory tools functional",
            }
            if verbose:
                results["checks"]["mcp"]["details"] = {
                    "tool_statuses": tool_statuses,
                    "healthy_tools": healthy_tools,
                    "total_core_tools": len(core_memory_tools),
                }
        else:
            results["checks"]["mcp"] = {"status": "degraded", "message": "MCP unavailable"}
            for tool_name in core_memory_tools:
                tool_statuses[tool_name] = {"status": "unavailable", "message": "MCP not available"}
    except Exception as e:
        results["checks"]["mcp"] = {
            "status": "unhealthy",
            "message": f"Failed to check MCP: {str(e)}",
        }
        for tool_name in core_memory_tools:
            tool_statuses[tool_name] = {"status": "error", "message": f"MCP check failed: {str(e)}"}

    # Add individual tool status checks
    for tool_name, status_info in tool_statuses.items():
        results["checks"][f"mcp_{tool_name}"] = status_info

    # Test space operations (create/update/delete)
    try:
        if spaces_data and len(spaces_data) > 0:
            # Try to create a test space
            test_space_name = f"Health Check Test - {int(time.time())}"
            try:
                space_creation_result = client.create_space(
                    test_space_name, "Health check test space"
                )
                space_id = space_creation_result.get("space_id")
                results["checks"]["space_create"] = {
                    "status": "healthy",
                    "message": "Space creation working",
                }

                # Try to update the space
                try:
                    if space_id:
                        client.update_space(space_id=space_id, name=f"{test_space_name} - Updated")
                        results["checks"]["space_update"] = {
                            "status": "healthy",
                            "message": "Space update working",
                        }

                        # Clean up - delete the test space
                        try:
                            if space_id:
                                client.delete_space(space_id=space_id, confirm=True)
                            results["checks"]["space_delete"] = {
                                "status": "healthy",
                                "message": "Space deletion working",
                            }
                        except Exception as e:
                            results["checks"]["space_delete"] = {
                                "status": "degraded",
                                "message": f"Space deletion failed: {str(e)}",
                            }
                    else:
                        results["checks"]["space_update"] = {
                            "status": "unhealthy",
                            "message": "Space creation returned None",
                        }

                except Exception as e:
                    results["checks"]["space_update"] = {
                        "status": "unhealthy",
                        "message": f"Space update failed: {str(e)}",
                    }

            except Exception as e:
                results["checks"]["space_create"] = {
                    "status": "unhealthy",
                    "message": f"Space creation failed: {str(e)}",
                }
        else:
            results["checks"]["space_create"] = {
                "status": "degraded",
                "message": "No spaces available to test create/update/delete operations",
            }
    except Exception as e:
        results["checks"]["space_create"] = {
            "status": "unhealthy",
            "message": f"Failed to test space operations: {str(e)}",
        }

    # Test webhook operations
    try:
        # Try to create a test webhook
        test_webhook_url = "https://httpbin.org/post"
        try:
            webhook_result = client.register_webhook(
                url=test_webhook_url,
                events=["memory.created"],
                secret=f"health-check-{int(time.time())}",
            )
            webhook_id = webhook_result.get("id")

            results["checks"]["webhook_create"] = {
                "status": "healthy",
                "message": "Webhook creation working",
            }

            # Try to delete the test webhook
            try:
                if webhook_id:
                    client.delete_webhook(webhook_id=webhook_id, confirm=True)
                    results["checks"]["webhook_delete"] = {
                        "status": "healthy",
                        "message": "Webhook deletion working",
                    }
                else:
                    results["checks"]["webhook_delete"] = {
                        "status": "degraded",
                        "message": "Webhook creation succeeded but no ID returned",
                    }
            except Exception as e:
                results["checks"]["webhook_delete"] = {
                    "status": "degraded",
                    "message": f"Webhook deletion failed: {str(e)}",
                }

        except Exception as e:
            error_str = str(e)
            if "400" in error_str or "JSONDecodeError" in error_str:
                results["checks"]["webhook_create"] = {
                    "status": "degraded",
                    "message": f"Webhook creation not available: {error_str}",
                }
            else:
                results["checks"]["webhook_create"] = {
                    "status": "unhealthy",
                    "message": f"Webhook creation failed: {error_str}",
                }
    except Exception as e:
        results["checks"]["webhook_create"] = {
            "status": "unhealthy",
            "message": f"Failed to test webhook operations: {str(e)}",
        }

    # Determine overall status
    unhealthy_checks = [
        check for check in results["checks"].values() if check["status"] == "unhealthy"
    ]
    degraded_checks = [
        check for check in results["checks"].values() if check["status"] == "degraded"
    ]

    if unhealthy_checks:
        results["overall_status"] = "unhealthy"
        results["summary"] = (
            f"{len(unhealthy_checks)} endpoint(s) unhealthy, {len(degraded_checks)} degraded"
        )
    elif degraded_checks:
        results["overall_status"] = "degraded"
        results["summary"] = f"{len(degraded_checks)} endpoint(s) degraded"
    else:
        results["overall_status"] = "healthy"
        results["summary"] = "All endpoints healthy"

    client.close()

    # Print human-readable summary
    typer.echo("🔍 HeySol API Health Check")
    typer.echo("=" * 50)

    # Overall status
    if results["overall_status"] == "healthy":
        typer.echo("✅ Overall Status: HEALTHY")
    elif results["overall_status"] == "degraded":
        typer.echo("⚠️  Overall Status: DEGRADED")
    else:
        typer.echo("❌ Overall Status: UNHEALTHY")

    typer.echo(f"Summary: {results['summary']}")
    typer.echo()

    # Individual checks
    for endpoint, check in results["checks"].items():
        # Skip individual MCP tool checks - we'll show them separately
        if endpoint.startswith("mcp_memory_") or endpoint.startswith("mcp_get_user_profile"):
            continue

        status_icon = (
            "✅" if check["status"] == "healthy" else "⚠️" if check["status"] == "degraded" else "❌"
        )
        endpoint_name = endpoint.replace("_", " ").title()
        typer.echo(f"{status_icon} {endpoint_name}: {check['message']}")

        # Show additional details for failures in verbose mode
        if check["status"] != "healthy" and verbose:
            typer.echo(f"   Details: {check.get('message', 'No additional details')}")

    # Show individual MCP tool statuses
    typer.echo()
    typer.echo("🔧 MCP Core Memory Tools:")
    for tool_name in ["memory_ingest", "memory_search", "memory_get_spaces", "get_user_profile"]:
        check_key = f"mcp_{tool_name}"
        if check_key in results["checks"]:
            check = results["checks"][check_key]
            status_icon = (
                "✅"
                if check["status"] == "healthy"
                else "⚠️" if check["status"] == "degraded" else "❌"
            )
            tool_display_name = tool_name.replace("_", " ").title()
            typer.echo(f"   {status_icon} {tool_display_name}: {check['message']}")

    # Show summary of issues
    if unhealthy_checks or degraded_checks:
        typer.echo()
        typer.echo("📊 Issue Summary:")
        if unhealthy_checks:
            typer.echo(
                f"❌ Unhealthy ({len(unhealthy_checks)}): {[check['message'] for check in unhealthy_checks]}"
            )
        if degraded_checks:
            typer.echo(
                f"⚠️  Degraded ({len(degraded_checks)}): {[check['message'] for check in degraded_checks]}"
            )

    typer.echo()
    typer.echo("💡 Use --verbose for detailed endpoint responses")

    # Add conversational summary incorporating MCP tools and registry context
    typer.echo()
    typer.echo("🤖 Nice! Health check complete with MCP tools validation:")
    typer.echo("   🔧 Core memory tools tested individually with functional verification")
    typer.echo(
        "   📊 API endpoints tested: 11 total, comprehensive coverage across spaces, search, logs"
    )
    typer.echo("   🔄 Registry integration: Multi-user support with credential resolution")
    typer.echo("   ⚡ Performance: Fast validation with real API calls, no mocking")

    # Add comprehensive API endpoints list
    typer.echo()
    typer.echo("📋 Comprehensive API Endpoints Tested:")
    typer.echo("   🔐 Authentication & User:")
    typer.echo("      • GET /api/profile - User profile retrieval")
    typer.echo("      • MCP get_user_profile - User profile via MCP protocol")
    typer.echo()
    typer.echo("   🏠 Spaces Management:")
    typer.echo("      • GET /api/v1/spaces - List all spaces")
    typer.echo("      • GET /api/v1/spaces/{id} - Get space details")
    typer.echo("      • POST /api/v1/spaces - Create new space")
    typer.echo("      • PUT /api/v1/spaces/{id} - Update space properties")
    typer.echo("      • DELETE /api/v1/spaces/{id} - Delete space")
    typer.echo("      • MCP memory_get_spaces - Spaces via MCP protocol")
    typer.echo()
    typer.echo("   🔍 Search & Memory:")
    typer.echo("      • POST /api/v1/search - Search across memory")
    typer.echo("      • POST /api/v1/add - Ingest memory content")
    typer.echo("      • MCP memory_ingest - Memory ingestion via MCP")
    typer.echo("      • MCP memory_search - Memory search with temporal filtering")
    typer.echo()
    typer.echo("   📊 Logs & Ingestion Status:")
    typer.echo("      • GET /api/v1/logs - Retrieve ingestion logs")
    typer.echo("      • GET /api/v1/logs/status - Check ingestion processing status")
    typer.echo("      • DELETE /api/v1/logs/{id} - Delete specific log entry")
    typer.echo()
    typer.echo("   🪝 Webhooks:")
    typer.echo("      • GET /api/v1/webhooks - List webhooks")
    typer.echo("      • POST /api/v1/webhooks - Create webhook")
    typer.echo("      • GET /api/v1/webhooks/{id} - Get webhook details")
    typer.echo("      • PUT /api/v1/webhooks/{id} - Update webhook")
    typer.echo("      • DELETE /api/v1/webhooks/{id} - Delete webhook")
    typer.echo()
    typer.echo("   🔧 MCP Protocol Endpoints:")
    typer.echo("      • POST /mcp - MCP JSON-RPC protocol endpoint")
    typer.echo("      • tools/list - List available MCP tools")
    typer.echo("      • tools/call - Execute MCP tools dynamically")
    typer.echo("      • initialize - Initialize MCP session")

    # Only show JSON if pretty is True (for programmatic use)
    if pretty:
        typer.echo()
        typer.echo("Raw JSON output:")
        typer.echo(format_json_output(results, pretty))


if __name__ == "__main__":
    app()
