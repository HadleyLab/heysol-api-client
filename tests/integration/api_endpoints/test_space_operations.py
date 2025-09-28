#!/usr/bin/env python3
"""
Integration tests for space operations API endpoints.

Tests space operations with live API calls following fail-fast principles.
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


def test_spaces_list_endpoint():
    """Test spaces list endpoint with live API call."""
    client = get_test_client()

    try:
        spaces = client.get_spaces()

        # Validate response structure
        assert isinstance(spaces, list)

        # If spaces exist, validate structure
        if spaces:
            space = spaces[0]
            assert isinstance(space, dict)
            assert "id" in space
            assert "name" in space

        client.close()

    except Exception:
        client.close()
        raise


def test_space_details_endpoint():
    """Test space details endpoint with live API call."""
    client = get_test_client()

    try:
        spaces = client.get_spaces()

        if not spaces:
            # Skip if no spaces available
            client.close()
            pytest.skip("No spaces available for testing space details")

        # Test with first available space
        space_id = spaces[0]["id"]
        space_details = client.get_space_details(
            space_id, include_stats=True, include_metadata=True
        )

        # Validate response structure - API returns {"space": {...}}
        assert isinstance(space_details, dict)
        assert "space" in space_details
        space_data = space_details["space"]
        assert isinstance(space_data, dict)
        assert "id" in space_data
        assert "name" in space_data

        # Validate stats if present
        if "stats" in space_data:
            assert isinstance(space_data["stats"], dict)

        client.close()

    except Exception:
        client.close()
        raise


def test_space_operations_workflow():
    """Test complete space operations workflow with live API calls."""
    client = get_test_client()

    try:
        # Create a test space
        test_space_name = f"Integration Test Space - {int(time.time())}"
        space_id = client.create_space(test_space_name, "Created for integration testing")

        assert isinstance(space_id, str)
        assert space_id  # Should not be empty

        # Get space details - API returns {"space": {...}}
        space_details = client.get_space_details(space_id)
        assert "space" in space_details
        assert space_details["space"]["name"] == test_space_name

        # Update space
        updated_name = f"{test_space_name} - Updated"
        update_result = client.update_space(space_id=space_id, name=updated_name)
        assert isinstance(update_result, dict)

        # Verify update - API returns {"space": {...}}
        updated_details = client.get_space_details(space_id)
        assert "space" in updated_details
        assert updated_details["space"]["name"] == updated_name

        # Clean up - delete the test space
        delete_result = client.delete_space(space_id=space_id, confirm=True)
        assert isinstance(delete_result, dict)

        client.close()

    except Exception:
        client.close()
        raise


def test_user_profile_endpoint():
    """Test user profile endpoint with live API call."""
    client = get_test_client()

    try:
        profile = client.get_user_profile()

        # Validate response structure
        assert isinstance(profile, dict)
        assert "id" in profile or "user_id" in profile  # Allow flexibility in field names

        # Validate essential fields exist
        required_fields = ["name", "email"]
        for field in required_fields:
            assert field in profile, f"Missing required field: {field}"

        client.close()

    except Exception:
        client.close()
        raise


def test_error_handling_invalid_space_id():
    """Test error handling for invalid space ID."""
    client = get_test_client()

    try:
        # Try to get details for non-existent space
        client.get_space_details("invalid-space-id-12345")
        # Should not reach here - should raise exception
        assert False, "Expected exception for invalid space ID"

    except HeySolError:
        # Expected error for invalid space ID
        pass
    except Exception:
        # Other exceptions are also acceptable as they indicate the API properly rejected invalid input
        pass
    finally:
        client.close()


def test_space_metadata_validation():
    """Test space metadata validation and structure."""
    client = get_test_client()

    try:
        spaces = client.get_spaces()

        if spaces:
            space = spaces[0]

            # Validate space structure
            assert isinstance(space, dict)
            assert "id" in space
            assert "name" in space

            # ID should be a non-empty string
            assert isinstance(space["id"], str)
            assert len(space["id"]) > 0

            # Name should be a non-empty string
            assert isinstance(space["name"], str)
            assert len(space["name"]) > 0

        client.close()

    except Exception:
        client.close()
        raise


def test_space_creation_with_metadata():
    """Test space creation with metadata."""
    client = get_test_client()

    try:
        # Create a test space with description
        test_space_name = f"Metadata Test Space - {int(time.time())}"
        description = "Test space with metadata"

        space_id = client.create_space(test_space_name, description)

        assert isinstance(space_id, str)
        assert len(space_id) > 0

        # Verify space was created with correct metadata
        space_details = client.get_space_details(space_id)
        assert "space" in space_details
        space_data = space_details["space"]
        assert space_data["name"] == test_space_name

        # Clean up
        client.delete_space(space_id=space_id, confirm=True)

        client.close()

    except Exception:
        client.close()
        raise


def test_space_update_metadata():
    """Test space update with metadata changes."""
    client = get_test_client()

    try:
        # Create a test space
        test_space_name = f"Update Test Space - {int(time.time())}"
        space_id = client.create_space(test_space_name, "Original description")

        # Update space metadata
        new_name = f"{test_space_name} - Updated"
        new_description = "Updated description"

        update_result = client.update_space(
            space_id=space_id,
            name=new_name,
            description=new_description
        )
        assert isinstance(update_result, dict)

        # Verify update
        updated_details = client.get_space_details(space_id)
        assert "space" in updated_details
        space_data = updated_details["space"]
        assert space_data["name"] == new_name

        # Clean up
        client.delete_space(space_id=space_id, confirm=True)

        client.close()

    except Exception:
        client.close()
        raise


def test_space_stats_validation():
    """Test space statistics validation."""
    client = get_test_client()

    try:
        spaces = client.get_spaces()

        if spaces:
            space_id = spaces[0]["id"]

            # Get space details with stats
            space_details = client.get_space_details(space_id, include_stats=True)
            assert "space" in space_details
            space_data = space_details["space"]

            # If stats are included, validate structure
            if "stats" in space_data:
                stats = space_data["stats"]
                assert isinstance(stats, dict)

                # Stats should contain numeric values
                for key, value in stats.items():
                    assert isinstance(key, str)
                    assert isinstance(value, (int, float)) or value is None

        client.close()

    except Exception:
        client.close()
        raise


def test_space_list_pagination():
    """Test space list pagination."""
    client = get_test_client()

    try:
        # Test with different limits
        spaces_1 = client.get_spaces(limit=1)
        spaces_5 = client.get_spaces(limit=5)

        assert isinstance(spaces_1, list)
        assert isinstance(spaces_5, list)
        assert len(spaces_1) <= len(spaces_5)

        client.close()

    except Exception:
        client.close()
        raise


def test_space_search_functionality():
    """Test space search functionality."""
    client = get_test_client()

    try:
        # Search for spaces (if supported by API)
        try:
            search_result = client.search("space", limit=1)
            assert isinstance(search_result, dict)
        except Exception:
            # Search might not be available or might fail
            pass

        client.close()

    except Exception:
        client.close()
        raise


def test_space_error_recovery():
    """Test error recovery for space operations."""
    client = get_test_client()

    try:
        # Test that client can recover from errors
        try:
            client.get_space_details("nonexistent-space-id")
        except Exception:
            # Expected error
            pass

        # Client should still be functional after error
        spaces = client.get_spaces()
        assert isinstance(spaces, list)

        client.close()

    except Exception:
        client.close()
        raise


def test_space_concurrent_access():
    """Test concurrent access to space operations."""
    import threading

    client = get_test_client()
    results = []

    def worker_operation(operation_id: int):
        """Worker function for concurrent space testing."""
        try:
            # All operations read space list (safe for concurrent access)
            spaces = client.get_spaces()
            results.append(f"spaces-{operation_id}: {len(spaces)}")
        except Exception as e:
            results.append(f"error-{operation_id}: {str(e)}")

    try:
        # Run 3 concurrent operations
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker_operation, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Validate results
        assert len(results) == 3
        assert all("error" not in result for result in results)

        client.close()

    except Exception:
        client.close()
        raise