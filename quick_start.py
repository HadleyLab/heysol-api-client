#!/usr/bin/env python
# coding: utf-8

# # 🎯 HeySol API Client - Quick Start
#
# Get up and running with HeySol in under 5 minutes!
#
# This notebook will guide you through:
# 1. ✅ API key setup and validation
# 2. 🔧 CLI initialization and registry setup
# 3. 🏗️ Creating a demo space
# 4. 📝 Ingesting sample clinical data
# 5. 🔍 Performing searches
# 6. 📊 Viewing results
#
# ## 📋 Prerequisites
#
# Before running this notebook, ensure you have:
#
# 1. **A valid HeySol API key** from [https://core.heysol.ai/settings/api](https://core.heysol.ai/settings/api)
# 2. **Set the environment variable**: `export HEYSOL_API_KEY="your-key-here"`
# 3. **Or create a `.env` file** with: `HEYSOL_API_KEY_xxx=your-key-here` (any name starting with HEYSOL_API_KEY)
# 4. **Install the package**: `pip install heysol-api-client`
#
# ## 🚀 Let's Get Started!

# In[1]:


# Import required modules
import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Import HeySol clients
try:
    from src.heysol import HeySolAPIClient, HeySolClient, HeySolMCPClient

    print("✅ HeySol clients imported successfully!")
    print("   📦 HeySolClient (unified with API + MCP)")
    print("   ⚡ HeySolAPIClient (direct API only)")
    print("   🎯 HeySolMCPClient (MCP protocol only)")
except ImportError as e:
    print("❌ Failed to import HeySol client.")
    print("💡 Install with: pip install heysol-api-client")
    print(f"   Error: {e}")
    raise


# ## 🔑 Step 1: API Key Validation
#
# First, let's check that your API key is properly configured. The system will validate your key format and test it against the API.

# In[2]:


# Check and validate API key
print("🔑 Checking API key configuration...")

api_key = os.getenv("HEYSOL_API_KEY")
if not api_key:
    print("❌ No API key found!")
    print("\n📝 To get started:")
    print("1. Visit: https://core.heysol.ai/settings/api")
    print("2. Generate an API key")
    print("3. Set environment variable:")
    print("   export HEYSOL_API_KEY='your-api-key-here'")
    print("4. Or create a .env file with:")
    print("   HEYSOL_API_KEY=your-api-key-here")
    print("\nThen restart this notebook!")
    raise ValueError("API key not configured")

print(f"✅ API key found (ends with: ...{api_key[-4:]})")
print("🔍 Validating API key...")

# The validation will happen automatically when we create clients below


# ## 🔧 Step 2: Client Types Demonstration
#
# HeySol provides three client types. Let's explore each one and see which features are available with your setup.

# In[3]:


# Demonstrate different client types
print("🔧 Demonstrating HeySol client types...")
print("=" * 50)

# 1. Unified client (recommended for most users)
print("\n📦 1. Unified Client (API + MCP with automatic fallback)")
unified_client: Optional[HeySolClient] = None
try:
    unified_client = HeySolClient(api_key=api_key)
    print("   ✅ Created successfully")
    print(f"   🎯 MCP Available: {unified_client.is_mcp_available()}")
    print(f"   🔄 Using: {unified_client.get_preferred_access_method('search')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# 2. Direct API client (for high performance)
print("\n⚡ 2. Direct API Client (high performance, no MCP overhead)")
api_client: Optional[HeySolAPIClient] = None
try:
    api_client = HeySolAPIClient(api_key=api_key)
    print("   ✅ Created successfully")
    print("   🚀 Always available, direct HTTP API calls")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# 3. MCP-only client (for advanced features)
print("\n🎯 3. MCP Client (dynamic tools & advanced features)")
mcp_client: Optional[HeySolMCPClient] = None
try:
    mcp_client = HeySolMCPClient(api_key=api_key)
    tools = mcp_client.get_available_tools()
    print("   ✅ Created successfully")
    print(f"   🛠️ Available tools: {len(tools)}")
except Exception as e:
    print(f"   ⚠️ MCP not available: {e}")
    print("   💡 This is normal if MCP server is not running")

print("\n✅ Client demonstration complete!")
print("💡 Unified client is recommended for most use cases")


# ## 🏗️ Step 3: Create Demo Space
#
# Spaces are containers for organizing your data in HeySol. Let's create a demo space for our examples.

# In[4]:


# Create or reuse demo space
print("🏗️ Setting up demo space...")

space_name = "Quick Start Demo"
space_description = "Created by HeySol quick start notebook"

# Use unified client for the demo
client = unified_client or api_client
if not client:
    raise ValueError("No working client available")

# Check for existing spaces
print(f"   🔍 Checking for existing space: '{space_name}'...")
existing_spaces = client.get_spaces()
space_id: Optional[str] = None

for space in existing_spaces:
    if isinstance(space, dict) and space.get("name") == space_name:
        space_id = space.get("id")
        if space_id:
            print(f"   ✅ Found existing space: {space_id[:16]}...")
        break

# Create new space if needed
if not space_id:
    print(f"   🆕 Creating new space: '{space_name}'...")
    space_id = client.create_space(space_name, space_description)
    if space_id:
        print(f"   ✅ Created space: {space_id}")

print(f"\n📊 Ready to use space: {space_name}")
print(f"   ID: {space_id}")
print(f"   Description: {space_description}")


# ## 📝 Step 4: Ingest Sample Data
#
# Now let's add some sample clinical data to HeySol. This data will be processed and made searchable.

# In[5]:


# Ingest sample clinical data
print("📝 Ingesting sample clinical data...")
print("=" * 50)

sample_data = [
    "Patient shows positive response to immunotherapy treatment",
    "Clinical trial demonstrates 78% efficacy rate for new oncology drug",
    "Biomarker analysis reveals key indicators for treatment success",
]

print(f"   📋 Will ingest {len(sample_data)} items")

for i, data in enumerate(sample_data, 1):
    print(f"   🔄 Ingesting item {i}/{len(sample_data)}...")
    try:
        result = client.ingest(data, space_id=space_id)
        print(f"   ✅ Item {i} ingested successfully")

        # Show run ID if available
        if isinstance(result, dict) and "run_id" in result:
            print(f"      Run ID: {result['run_id']}")

    except Exception as e:
        print(f"   ❌ Item {i} failed: {e}")

print("\n✅ Sample data ingestion complete!")
print("💡 Data is being processed in the background and will be searchable soon")


# ## 🔍 Step 5: Perform Search
#
# Let's search for the data we just ingested. HeySol uses semantic search to find relevant information.

# In[6]:


# Search for ingested data
print("🔍 Searching for clinical data...")
print("=" * 40)

search_query = "treatment"
print(f"   🔎 Query: '{search_query}'")
if space_id:
    print(f"   📍 Space: {space_name} ({space_id[:16]}...)")
else:
    print(f"   📍 Space: {space_name} (no space ID)")

try:
    # Perform search
    space_ids = [space_id] if space_id else None
    results = client.search(search_query, space_ids=space_ids, limit=5)

    # Handle different result formats (dict from API, string from MCP)
    if isinstance(results, dict):
        episodes = results.get("episodes", [])
        print(f"\n✅ Search completed! Found {len(episodes)} results")

        if episodes:
            print("\n📋 Results:")
            for i, episode in enumerate(episodes, 1):
                content = episode.get("content", "")[:80]
                score = episode.get("score", "N/A")
                print(f"   {i}. {content}{'...' if len(content) == 80 else ''}")
                print(f"      Score: {score}")
        else:
            print("\n📭 No results found yet")
            print("💡 Data may still be processing. Try again in a moment.")
    else:
        # MCP might return a string or other format
        print(f"\n✅ Search completed! Result: {str(results)[:200]}{'...' if len(str(results)) > 200 else ''}")
        print("💡 MCP search returned non-dict format")

except Exception as e:
    print(f"❌ Search failed: {e}")
    print("💡 This might be normal if data is still being processed")


# ## 📊 Step 6: View Results & Summary
#
# Let's get a summary of what we've accomplished and explore next steps.

# In[7]:


# Display summary and next steps
print("📊 HeySol Quick Start Summary")
print("=" * 40)

print("✅ What we accomplished:")
print("   🔑 Validated API key")
print("   🔧 Demonstrated client types")
print(f"   🏗️ Created/used space: {space_name}")
print(f"   📝 Ingested {len(sample_data)} data items")
print("   🔍 Performed semantic search")

print("\n📚 Next Steps:")
print("   📖 Explore examples: ls examples/")
print("   🖥️ Try the CLI: heysol-client --help")
print("   📚 Read docs: https://core.heysol.ai/")
print("   🔬 API vs MCP analysis: docs/API_VS_MCP_ANALYSIS.md")

print("\n💡 Client Types:")
print("   📦 HeySolClient: Unified (recommended for most users)")
print("   ⚡ HeySolAPIClient: Direct API (high performance)")
print("   🎯 HeySolMCPClient: MCP protocol (advanced features)")

# Clean up
print("\n🧹 Cleaning up...")
try:
    if unified_client:
        unified_client.close()
    if api_client:
        api_client.close()
    if mcp_client:
        mcp_client.close()
    print("✅ Clients closed successfully")
except Exception as e:
    print(f"⚠️ Cleanup warning: {e}")

print("\n🎉 Quick start completed successfully!")
print("🚀 You're now ready to use HeySol!")
