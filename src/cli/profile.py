"""
Profile-related CLI commands.
"""

import time
from typing import Any

import typer

from .common import create_client, format_json_output, get_auth_from_global

app = typer.Typer()


@app.command("get")
def profile_get():
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
):
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

    # Test MCP availability and tools
    try:
        mcp_available = client.is_mcp_available()
        if mcp_available:
            # Test MCP tools
            try:
                tools = client.get_available_tools()
                tool_names = client.get_tool_names()
                results["checks"]["mcp"] = {
                    "status": "healthy",
                    "message": f"MCP available with {len(tools)} tools",
                }
                if verbose:
                    session_info = client.get_session_info()
                    results["checks"]["mcp"]["details"] = {
                        "session_info": session_info,
                        "tools_count": len(tools),
                        "tool_names": tool_names,
                    }
            except Exception as e:
                results["checks"]["mcp"] = {
                    "status": "degraded",
                    "message": f"MCP available but tools failed: {str(e)}",
                }
        else:
            results["checks"]["mcp"] = {"status": "degraded", "message": "MCP unavailable"}
    except Exception as e:
        results["checks"]["mcp"] = {
            "status": "unhealthy",
            "message": f"Failed to check MCP: {str(e)}",
        }

    # Test space operations (create/update/delete)
    try:
        if spaces_data and len(spaces_data) > 0:
            # Try to create a test space
            test_space_name = f"Health Check Test - {int(time.time())}"
            try:
                space_id = client.create_space(test_space_name, "Health check test space")
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
        status_icon = (
            "✅" if check["status"] == "healthy" else "⚠️" if check["status"] == "degraded" else "❌"
        )
        endpoint_name = endpoint.replace("_", " ").title()
        typer.echo(f"{status_icon} {endpoint_name}: {check['message']}")

        # Show additional details for failures in verbose mode
        if check["status"] != "healthy" and verbose:
            typer.echo(f"   Details: {check.get('message', 'No additional details')}")

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

    # Only show JSON if pretty is True (for programmatic use)
    if pretty:
        typer.echo()
        typer.echo("Raw JSON output:")
        typer.echo(format_json_output(results, pretty))


if __name__ == "__main__":
    app()
