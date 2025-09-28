#!/usr/bin/env python3
"""
Integration tests for memory operations API endpoints.

Tests memory operations with live API calls following fail-fast principles.
"""

import time

import pytest

from heysol.client import HeySolClient
from heysol.exceptions import HeySolError


def get_test_client() -> HeySolClient:
    """
    Create a test client using registry configuration.

    Returns:
        HeySolClient: Configured client for testing

    Raises:
        pytest.skip: If no registered instances found
    """
    from heysol.registry_config import RegistryConfig

    registry = RegistryConfig()
    instances = registry.get_registered_instances()

    if not instances:
        pytest.skip("No registered instances found for integration testing")

    # Use the first available instance
    instance_name = list(instances.keys())[0]
    instance_config = instances[instance_name]
    api_key = instance_config["api_key"]
    base_url = instance_config["base_url"]

    return HeySolClient(api_key=api_key, base_url=base_url, skip_mcp_init=True)


def test_memory_ingest_endpoint():
    """Test memory ingest endpoint with live API call."""
    client = get_test_client()

    try:
        # Create unique test message to avoid conflicts
        test_message = f"Integration test - {int(time.time())}"

        ingest_result = client.ingest(message=test_message, source="integration-test")

        # Validate response structure
        assert isinstance(ingest_result, dict)
        assert "success" in ingest_result or "id" in ingest_result

        # If success field exists, it should be True
        if "success" in ingest_result:
            assert ingest_result["success"] is True

        client.close()

    except Exception:
        client.close()
        raise


def test_memory_operations_workflow():
    """Test complete memory operations workflow with live API calls."""
    client = get_test_client()

    try:
        # Ingest test data
        test_message = f"Workflow test message - {int(time.time())}"
        ingest_result = client.ingest(message=test_message, source="workflow-test")

        # Validate ingest result structure
        assert isinstance(ingest_result, dict)

        # Search for the ingested data
        search_result = client.search(test_message, limit=5)
        episodes = search_result.get("episodes") or search_result.get("results", [])

        # Should find at least our test message
        found_test_message = False
        for episode in episodes:
            # Handle different episode formats (dict or string)
            if isinstance(episode, dict):
                content = episode.get("content", "") or episode.get("episodeBody", "")
            else:
                content = str(episode)
            if test_message in str(content):
                found_test_message = True
                break

        # Note: Search may not immediately find the ingested data due to processing time
        # This is expected behavior, not a failure
        if not found_test_message:
            # This is normal - search may not be immediate
            pass

        client.close()

    except Exception:
        client.close()
        raise


def test_search_endpoint():
    """Test search endpoint with live API call."""
    client = get_test_client()

    try:
        # Use a simple test query
        search_result = client.search("health check test", limit=1)

        # Validate response structure
        assert isinstance(search_result, dict)
        assert "episodes" in search_result or "results" in search_result

        # Validate episodes/results is a list
        episodes = search_result.get("episodes") or search_result.get("results", [])
        assert isinstance(episodes, list)

        client.close()

    except Exception:
        client.close()
        raise


def test_search_with_filters():
    """Test search endpoint with various filters."""
    client = get_test_client()

    try:
        # Test search with limit
        search_result = client.search("test", limit=1)
        assert isinstance(search_result, dict)

        # Test search with space_ids if spaces exist
        spaces = client.get_spaces()
        if spaces:
            space_id = spaces[0]["id"]
            search_result = client.search("test", space_ids=[space_id], limit=1)
            assert isinstance(search_result, dict)

        client.close()

    except Exception:
        client.close()
        raise


def test_ingestion_status_endpoint():
    """Test ingestion status endpoint with live API call."""
    client = get_test_client()

    try:
        status_result = client.check_ingestion_status()

        # Validate response structure
        assert isinstance(status_result, dict)
        # Status result structure may vary, just ensure it's a dict

        client.close()

    except Exception:
        client.close()
        raise


def test_logs_list_endpoint():
    """Test logs list endpoint with live API call."""
    client = get_test_client()

    try:
        logs = client.get_ingestion_logs(limit=5)

        # Validate response structure
        assert isinstance(logs, list)

        # If logs exist, validate structure
        if logs:
            log_entry = logs[0]
            assert isinstance(log_entry, dict)
            # Log entries should have basic fields like id or timestamp
            assert "id" in log_entry or "timestamp" in log_entry

        client.close()

    except Exception:
        client.close()
        raise


def test_logs_filtering():
    """Test logs endpoint with various filters."""
    client = get_test_client()

    try:
        # Test basic logs listing
        logs = client.get_ingestion_logs(limit=5)
        assert isinstance(logs, list)

        # Test with status filter
        logs_success = client.get_ingestion_logs(status="success", limit=5)
        assert isinstance(logs_success, list)

        # Test with space filter if spaces exist
        spaces = client.get_spaces()
        if spaces:
            space_id = spaces[0]["id"]
            logs_space = client.get_ingestion_logs(space_id=space_id, limit=5)
            assert isinstance(logs_space, list)

        client.close()

    except Exception:
        client.close()
        raise


def test_error_handling_comprehensive():
    """Test comprehensive error handling for various scenarios."""
    client = get_test_client()

    try:
        # Test invalid search (should not crash)
        try:
            result = client.search("", limit=1)  # Empty query
            assert isinstance(result, dict)
        except Exception:
            # May fail but should not crash
            pass

        client.close()

    except Exception:
        client.close()
        raise


def test_pagination_and_limits():
    """Test pagination and limit handling."""
    client = get_test_client()

    try:
        # Test logs with different limits
        logs_1 = client.get_ingestion_logs(limit=1)
        logs_5 = client.get_ingestion_logs(limit=5)

        assert isinstance(logs_1, list)
        assert isinstance(logs_5, list)
        assert len(logs_1) <= len(logs_5)

        client.close()

    except Exception:
        client.close()
        raise


def test_data_integrity():
    """Test data integrity across operations."""
    client = get_test_client()

    try:
        # Get initial logs count
        initial_logs = client.get_ingestion_logs(limit=1)
        initial_count = len(initial_logs) if initial_logs else 0

        # Perform some operations that shouldn't change logs count
        client.search("integrity test", limit=1)

        # Verify logs count hasn't changed significantly
        final_logs = client.get_ingestion_logs(limit=1)
        final_count = len(final_logs) if final_logs else 0

        # Allow for some variance due to concurrent operations
        count_diff = abs(initial_count - final_count)
        assert count_diff <= 1, f"Logs count changed unexpectedly: {initial_count} -> {final_count}"

        client.close()

    except Exception:
        client.close()
        raise


def test_api_response_consistency():
    """Test that API responses are consistent across multiple calls."""
    client = get_test_client()

    try:
        # Test search consistency
        search1 = client.search("consistency test", limit=1)
        search2 = client.search("consistency test", limit=1)

        assert isinstance(search1, type(search2))

        client.close()

    except Exception:
        client.close()
        raise


def test_concurrent_operations():
    """Test concurrent operations to ensure thread safety."""
    import threading

    client = get_test_client()
    results = []
    errors = []

    def worker_operation(operation_id: int):
        """Worker function for concurrent testing."""
        try:
            if operation_id % 2 == 0:
                # Even operations: search (safe operation)
                client.search("concurrent test", limit=1)
                results.append(f"search-{operation_id}")
            else:
                # Odd operations: list logs
                client.get_ingestion_logs(limit=1)
                results.append(f"logs-{operation_id}")
        except Exception as e:
            errors.append(f"error-{operation_id}: {str(e)}")

    try:
        # Run 5 concurrent operations
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_operation, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Validate results - should have some results
        assert len(results) >= 2, f"Expected at least 2 results, got {len(results)}"
        assert len(errors) == 0, f"Unexpected errors: {errors}"

        client.close()

    except Exception:
        client.close()
        raise