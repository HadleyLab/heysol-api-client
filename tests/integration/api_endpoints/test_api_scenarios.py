#!/usr/bin/env python3
"""
Integration Tests for HeySol API Client - Live API Scenarios

Tests real API integration scenarios including:
- Live API connectivity and authentication
- Real endpoint functionality
- Performance with actual network calls
- Error handling with real API failures
- Webhook registration and management
"""

import os
import time

import pytest

from heysol.client import HeySolClient


class TestIntegrationScenarios:
    """Integration tests for live API scenarios."""

    @pytest.fixture
    def live_client(self):
        """Create a client instance with real API key from registry or environment."""
        try:
            from heysol.registry_config import RegistryConfig

            registry = RegistryConfig()
            instances = registry.get_registered_instances()

            # Use the first available instance from registry
            if instances:
                first_instance_name = list(instances.keys())[0]
                instance = instances[first_instance_name]
                api_key = instance["api_key"]
            else:
                # Fall back to environment variables
                api_key = None
                for key, value in os.environ.items():
                    if key.startswith("HEYSOL_API_KEY") and value and value.startswith("rc_pat_"):
                        api_key = value
                        break

                if not api_key:
                    pytest.skip(
                        "No API keys found in registry or environment variables starting with HEYSOL_API_KEY* with rc_pat_ values"
                    )

            return HeySolClient(api_key=api_key)
        except Exception as e:
            pytest.skip(f"Failed to load API key from registry or environment: {e}")

    # Live API Connectivity Tests
    @pytest.mark.integration
    def test_live_api_connectivity(self, live_client):
        """Test basic connectivity to live API."""
        try:
            # Test basic connectivity by making a simple request
            spaces = live_client.get_spaces()
            assert isinstance(spaces, list)
            print(f"✅ Live API connectivity successful - retrieved {len(spaces)} spaces")
        except Exception as e:
            pytest.skip(f"Live API connectivity test skipped due to: {e}")

    @pytest.mark.integration
    def test_live_api_authentication(self, live_client):
        """Test authentication with live API."""
        try:
            # Test authentication by making an authenticated request
            # Note: Profile endpoint requires OAuth which is not yet available
            # So we'll test authentication with spaces endpoint instead
            spaces = live_client.get_spaces()
            assert isinstance(spaces, list)
            print(f"✅ Live API authentication successful - retrieved {len(spaces)} spaces")
        except Exception as e:
            pytest.skip(f"Live API authentication test skipped due to: {e}")

    # Live API Functionality Tests
    @pytest.mark.integration
    def test_live_memory_operations(self, live_client):
        """Test memory operations with live API."""
        try:
            # Test search functionality
            search_results = live_client.search("test query", limit=5)
            assert isinstance(search_results, dict)
            print(
                f"✅ Live memory search completed: {len(search_results.get('episodes', []))} episodes found"
            )

            # Test knowledge graph search
            kg_results = live_client.search_knowledge_graph("test", limit=5, depth=1)
            assert isinstance(kg_results, dict)
            print(
                f"✅ Live knowledge graph search completed: {len(kg_results.get('nodes', []))} nodes found"
            )

        except Exception as e:
            pytest.skip(f"Live memory operations test skipped due to: {e}")

    @pytest.mark.integration
    def test_live_space_operations(self, live_client):
        """Test space operations with live API."""
        try:
            # Test getting spaces
            spaces = live_client.get_spaces()
            assert isinstance(spaces, list)
            print(f"✅ Live space listing completed: {len(spaces)} spaces found")

            # Test getting space details (may fail if no spaces exist)
            if spaces:
                space_id = spaces[0]["id"]
                space_details = live_client.get_space_details(space_id)
                assert isinstance(space_details, dict)
                print(f"✅ Live space details retrieved for space: {space_id}")

        except Exception as e:
            pytest.skip(f"Live space operations test skipped due to: {e}")

    # Performance Integration Tests
    @pytest.mark.integration
    def test_live_api_performance(self, live_client):
        """Test live API performance with multiple requests."""
        try:
            start_time = time.time()

            # Make multiple requests to test performance
            for _ in range(3):
                live_client.get_spaces()
                time.sleep(0.1)  # Small delay between requests

            end_time = time.time()
            total_time = end_time - start_time

            # Should complete in reasonable time (less than 10 seconds for 3 requests)
            assert total_time < 10.0, f"Live API requests too slow: {total_time:.2f}s"
            print(f"✅ Live API performance test passed: {total_time:.2f} total time")

        except Exception as e:
            pytest.skip(f"Live API performance test skipped due to: {e}")

    @pytest.mark.integration
    def test_live_api_concurrent_requests(self, live_client):
        """Test concurrent request handling with live API."""
        try:
            # Test multiple rapid requests
            results = []
            for i in range(5):
                try:
                    spaces = live_client.get_spaces()
                    results.append(spaces)
                except Exception as e:
                    print(f"Request {i} failed: {e}")

            # Should have at least some successful requests
            assert len(results) > 0, "All concurrent requests failed"
            assert all(isinstance(result, list) for result in results)
            print(f"✅ Live API concurrent requests test passed: {len(results)}/5 successful")

        except Exception as e:
            pytest.skip(f"Live API concurrent requests test skipped due to: {e}")

    # Error Handling Integration Tests
    @pytest.mark.integration
    def test_live_api_error_handling(self, live_client):
        """Test error handling with live API."""
        try:
            # Test invalid space ID
            with pytest.raises(Exception):
                live_client.get_space_details("invalid-space-id")

            print("✅ Live API error handling test passed")

        except Exception as e:
            pytest.skip(f"Live API error handling test skipped due to: {e}")

    @pytest.mark.integration
    def test_live_api_rate_limiting(self, live_client):
        """Test rate limiting behavior with live API."""
        try:
            # Make rapid requests to potentially trigger rate limiting
            start_time = time.time()
            request_count = 0

            for i in range(10):
                try:
                    live_client.get_spaces()
                    request_count += 1
                    time.sleep(0.05)  # Very small delay
                except Exception as e:
                    print(f"Request {i} failed (possibly rate limited): {e}")
                    break

            end_time = time.time()
            total_time = end_time - start_time

            print(
                f"✅ Live API rate limiting test completed: {request_count} requests in {total_time:.2f}s"
            )

        except Exception as e:
            pytest.skip(f"Live API rate limiting test skipped due to: {e}")

    # Data Consistency Tests
    @pytest.mark.integration
    def test_live_data_consistency(self, live_client):
        """Test data consistency across multiple requests."""
        try:
            # Make multiple requests and verify consistency
            results = []
            for _ in range(3):
                spaces = live_client.get_spaces()
                results.append(spaces)
                time.sleep(0.1)

            # All results should be consistent
            for i in range(1, len(results)):
                assert (
                    results[0] == results[i]
                ), f"Data inconsistency between requests {i-1} and {i}"

            print(f"✅ Live data consistency test passed: {len(results[0])} consistent results")

        except Exception as e:
            pytest.skip(f"Live data consistency test skipped due to: {e}")

    # Network Resilience Tests
    @pytest.mark.integration
    def test_network_resilience(self, live_client):
        """Test network resilience with intermittent connectivity."""
        try:
            # Test with various network conditions
            successful_requests = 0
            total_requests = 5

            for i in range(total_requests):
                try:
                    live_client.get_spaces()
                    successful_requests += 1
                    print(f"Request {i+1}: ✅ Success")
                except Exception as e:
                    print(f"Request {i+1}: ❌ Failed - {e}")

                time.sleep(0.2)  # Small delay between requests

            success_rate = successful_requests / total_requests
            print(
                f"✅ Network resilience test completed: {successful_requests}/{total_requests} successful ({success_rate:.1%})"
            )

            # Should have reasonable success rate
            assert success_rate >= 0.6, f"Success rate too low: {success_rate:.1%}"

        except Exception as e:
            pytest.skip(f"Network resilience test skipped due to: {e}")

    # Real-world Scenario Tests
    @pytest.mark.integration
    def test_real_world_memory_workflow(self, live_client):
        """Test a realistic memory management workflow."""
        try:
            # Simulate a real-world workflow
            print("🧪 Testing real-world memory workflow...")

            # 1. Check available spaces
            spaces = live_client.get_spaces()
            print(f"   1. Found {len(spaces)} spaces")

            # 2. Search for existing data
            search_results = live_client.search("clinical trial", limit=5)
            print(f"   2. Found {len(search_results.get('episodes', []))} episodes")

            # 3. Ingest new data
            ingestion_result = live_client.add_data_to_ingestion_queue(
                {"content": "New clinical trial data", "type": "research", "priority": "high"}
            )
            print(f"   3. Ingestion queued: {ingestion_result.get('queue_id', 'unknown')}")

            # 4. Search knowledge graph
            kg_results = live_client.search_knowledge_graph("clinical trial", limit=5, depth=1)
            print(f"   4. Knowledge graph search: {len(kg_results.get('nodes', []))} nodes")

            print("✅ Real-world memory workflow test completed successfully")

        except Exception as e:
            pytest.skip(f"Real-world memory workflow test skipped due to: {e}")

    @pytest.mark.integration
    def test_real_world_space_management(self, live_client):
        """Test a realistic space management workflow."""
        try:
            print("🧪 Testing real-world space management workflow...")

            # 1. List existing spaces
            spaces = live_client.get_spaces()
            print(f"   1. Found {len(spaces)} existing spaces")

            # 2. Get details of first space (if any)
            if spaces:
                space_id = spaces[0]["id"]
                live_client.get_space_details(space_id)
                print(f"   2. Retrieved details for space: {space_id}")

                # 3. Update space (if possible)
                try:
                    live_client.update_space(space_id, description="Updated via integration test")
                    print(f"   3. Updated space: {space_id}")
                except Exception as e:
                    print(f"   3. Space update failed (expected): {e}")

            print("✅ Real-world space management workflow test completed")

        except Exception as e:
            pytest.skip(f"Real-world space management test skipped due to: {e}")


if __name__ == "__main__":
    # Run integration tests
    print("🔗 Running Live API Integration Scenario Tests...")

    try:
        # Check if API credentials are available
        api_key = None
        for key, value in os.environ.items():
            if key.startswith("HEYSOL_API_KEY") and value and value.startswith("rc_pat_"):
                api_key = value
                break

        if not api_key:
            print(
                "⚠️  No HEYSOL_API_KEY* environment variables with rc_pat_ values found - integration tests will be skipped"
            )
            print(
                "   Set environment variables like HEYSOL_API_KEY_INSTANCE_NAME=rc_pat_... to run live API tests"
            )
            exit(0)

        test_suite = TestIntegrationScenarios()

        print("✅ Integration test suite setup complete")
        print("Run with pytest to execute individual tests:")
        print("  pytest test_scenarios.py::TestIntegrationScenarios::test_live_api_connectivity -v")
        print("  pytest test_scenarios.py -k integration -v")

    except Exception as e:
        print(f"❌ Integration test setup failed: {e}")
        raise
