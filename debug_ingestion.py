#!/usr/bin/env python3
"""
Debug script to investigate API ingestion 400 errors.
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path.cwd()))

from src.heysol.clients.api_client import HeySolAPIClient
from src.heysol.models.requests import IngestRequest

def debug_ingestion():
    """Debug the ingestion API call."""
    print("🔍 Debugging API Ingestion Issues")
    print("=" * 50)

    # Load API key - try multiple sources
    api_key = os.getenv("HEYSOL_API_KEY")
    if not api_key:
        # Try loading from .env file directly
        env_path = Path(".env")
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("HEYSOL_API_KEY")

    if not api_key:
        print("❌ No API key found")
        print("   Checked: environment variable and .env file")
        return

    print(f"✅ API key loaded (ends with: ...{api_key[-10:]})")

    # Create client
    try:
        client = HeySolAPIClient(api_key=api_key)
        print("✅ API client created")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return

    # Create request model
    try:
        request = IngestRequest(
            episodeBody="Test message for debugging",
            source="debug-script",
            sessionId="",
            spaceId=None,
        )
        print("✅ IngestRequest model created")
        print(f"   Payload: {request.model_dump(by_alias=True)}")
    except Exception as e:
        print(f"❌ Request model creation failed: {e}")
        return

    # Try the API call
    try:
        print("\n🔄 Attempting API call...")
        payload = request.model_dump(by_alias=True)
        print(f"   Final payload: {json.dumps(payload, indent=2)}")

        # Test the client's ingest method instead of manual request
        print("🔄 Testing client's ingest method...")
        try:
            result = client.ingest("Test message for debugging", source="debug-script")
            print(f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Client ingest failed: {e}")
            # Now make manual request to see the actual API error
            import requests

            url = client.base_url.rstrip("/") + "/add"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": client._get_authorization_header(),
            }

            # Test the exclude_none behavior
            test_payload = request.model_dump(by_alias=True, exclude_none=True)
            print(f"   Payload after exclude_none: {json.dumps(test_payload, indent=2)}")
            if test_payload.get("spaceId") is None:
                test_payload.pop("spaceId", None)
                print(f"   Payload after manual removal: {json.dumps(test_payload, indent=2)}")

            print(f"   URL: {url}")
            print(f"   Headers: {json.dumps({k: v[:50] + '...' if len(v) > 50 else v for k, v in headers.items()}, indent=2)}")

            response = requests.post(
                url=url,
                json=test_payload,  # Use the cleaned payload
                headers=headers,
                timeout=client.timeout,
            )

            print(f"   Response status: {response.status_code}")
            print(f"   Response headers: {dict(response.headers)}")

            if response.status_code >= 400:
                print(f"❌ Error response: {response.text}")
            else:
                print(f"✅ Success response: {response.json()}")

    except Exception as e:
        print(f"❌ API call failed: {e}")

if __name__ == "__main__":
    debug_ingestion()