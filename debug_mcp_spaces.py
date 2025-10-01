#!/usr/bin/env python3
"""
Debug script to investigate MCP get_spaces issues.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path.cwd()))

from src.heysol.clients.mcp_client import HeySolMCPClient

def debug_mcp_spaces():
    """Debug the MCP get_spaces functionality."""
    print("🔍 Debugging MCP get_spaces Issues")
    print("=" * 50)

    # Load API key
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
        return

    print(f"✅ API key loaded (ends with: ...{api_key[-10:]})")

    # Create MCP client
    try:
        client = HeySolMCPClient(api_key=api_key)
        print("✅ MCP client created")
        print(f"   Session ID: {client.session_id}")
        print(f"   Tools available: {len(client.tools)}")
    except Exception as e:
        print(f"❌ MCP client creation failed: {e}")
        return

    # List available tools
    print("\n🛠️ Available MCP Tools:")
    tools = client.get_available_tools()
    space_related_tools = []
    for tool_name, tool_info in tools.items():
        if 'space' in tool_name.lower() or 'memory' in tool_name.lower():
            space_related_tools.append(tool_name)
            print(f"   • {tool_name}: {tool_info.get('description', 'No description')}")

    print(f"\n📊 Space-related tools found: {len(space_related_tools)}")

    # Test get_spaces method
    print("\n🔄 Testing get_spaces method...")
    try:
        spaces = client.get_spaces()
        print(f"✅ get_spaces succeeded: {len(spaces)} spaces returned")
        if spaces:
            print("   Sample spaces:")
            for i, space in enumerate(spaces[:3]):
                if isinstance(space, dict):
                    print(f"     {i+1}. {space.get('name', space.get('id', 'Unknown'))}")
                else:
                    print(f"     {i+1}. {space}")
    except Exception as e:
        print(f"❌ get_spaces failed: {e}")

    # Test get_spaces_via_mcp directly
    print("\n🔄 Testing get_spaces_via_mcp directly...")
    try:
        result = client.get_spaces_via_mcp()
        print(f"✅ get_spaces_via_mcp succeeded: {result}")
    except Exception as e:
        print(f"❌ get_spaces_via_mcp failed: {e}")

    # Test get_memory_spaces_via_mcp directly
    print("\n🔄 Testing get_memory_spaces_via_mcp directly...")
    try:
        result = client.get_memory_spaces_via_mcp()
        print(f"✅ get_memory_spaces_via_mcp succeeded: {result}")
    except Exception as e:
        print(f"❌ get_memory_spaces_via_mcp failed: {e}")

    # Test calling tools directly
    print("\n🔄 Testing direct tool calls...")
    test_tools = ["get_spaces", "memory_get_spaces", "memory_search"]
    for tool_name in test_tools:
        if tool_name in tools:
            try:
                print(f"   Testing {tool_name}...")
                if tool_name == "memory_search":
                    result = client.call_tool(tool_name, query="test", limit=1)
                else:
                    result = client.call_tool(tool_name)
                print(f"     ✅ {tool_name} succeeded: {type(result)}")
                if isinstance(result, dict) and 'spaces' in result:
                    print(f"        Spaces found: {len(result['spaces'])}")
            except Exception as e:
                print(f"     ❌ {tool_name} failed: {e}")
        else:
            print(f"   ❌ {tool_name} not available")

if __name__ == "__main__":
    debug_mcp_spaces()