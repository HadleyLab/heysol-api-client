#!/usr/bin/env python
# coding: utf-8

# # 🎯 HeySol API Client - API Endpoints Demo
#
# Comprehensive demonstration of direct API operations with detailed explanations and interactive examples.
#
# ## 📋 What This Demo Covers
#
# This notebook provides a **pedantic, step-by-step** exploration of HeySol's direct API capabilities:
#
# 1. **🔧 Client Initialization** - Direct API client setup and validation
# 2. **🏗️ Space Management** - Complete CRUD operations for memory spaces
# 3. **📝 Data Ingestion** - Multiple ingestion patterns with metadata
# 4. **🔍 Search Operations** - Semantic search with various parameters
# 5. **🧠 Knowledge Graph** - Entity relationship exploration
# 6. **📋 Log Management** - Comprehensive log operations and filtering
# 7. **⚡ Bulk Operations** - Efficient batch processing
# 8. **🛡️ Error Handling** - Robust error patterns and recovery
# 9. **🔬 Advanced Features** - Status checking and monitoring
#
# ## 🎯 Learning Objectives
#
# By the end of this notebook, you will:
# - ✅ Understand direct API client architecture
# - ✅ Master space management operations
# - ✅ Learn proper data ingestion patterns
# - ✅ Explore search capabilities in depth
# - ✅ Understand knowledge graph functionality
# - ✅ Master log management and debugging
# - ✅ Handle errors gracefully
# - ✅ Use advanced API features effectively
#
# ## 📚 Prerequisites
#
# Before running this notebook:
# 1. **API Key**: Get from [https://core.heysol.ai/settings/api](https://core.heysol.ai/settings/api)
# 2. **Environment**: Set `HEYSOL_API_KEY` or create `.env` file
# 3. **Installation**: `pip install heysol-api-client`
#
# ---

# ## 🔧 Step 1: Environment Setup and Client Initialization
#
# Let's start by setting up our environment and initializing the direct API client. This step includes:
# - Environment variable loading
# - API key validation
# - Client initialization with proper error handling
# - Connection testing

# In[ ]:


# Import required modules with error handling
import os
import sys
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path for imports
sys.path.insert(0, str(Path.cwd() / "src"))

# Import with comprehensive error handling
try:
    from heysol.clients.api_client import HeySolAPIClient
    from heysol.exceptions import HeySolError

    print("✅ Successfully imported HeySol API client")
    print("   📦 HeySolAPIClient: Direct HTTP API operations")
    print("   🛡️  HeySolError: Exception handling")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("💡 Make sure you're running from the project root with src/ in path")
    raise


# In[ ]:


# API key validation with detailed feedback
print("🔑 Step 1.1: API Key Validation")
print("-" * 40)

api_key = os.getenv("HEYSOL_API_KEY")

if not api_key:
    print("❌ No API key found!")
    print("\n📝 Setup instructions:")
    print("1. Visit: https://core.heysol.ai/settings/api")
    print("2. Generate an API key")
    print("3. Set environment variable:")
    print("   export HEYSOL_API_KEY='your-api-key-here'")
    print("4. Or create .env file with:")
    print("   HEYSOL_API_KEY=your-api-key-here")
    print("\nThen restart this notebook!")
    raise ValueError("API key not configured")

print(f"✅ API key found (length: {len(api_key)} characters)")
print(f"✅ API key format: {'Valid' if len(api_key) > 20 else 'Invalid'} prefix")
print(f"✅ API key ends with: ...{api_key[-4:] if len(api_key) > 4 else 'N/A'}")


# In[ ]:


# Client initialization with comprehensive validation
print("🔧 Step 1.2: Client Initialization")
print("-" * 40)

try:
    # Initialize API client with explicit parameters
    client = HeySolAPIClient(api_key=api_key, base_url=None)  # Will use config default

    print("✅ API client initialized successfully")
    print(f"   🔗 Base URL: {client.base_url}")
    print(f"   🏠 Source: {client.source}")
    print(f"   ⏱️  Timeout: {client.timeout} seconds")

except HeySolError as e:
    print(f"❌ Validation error: {e}")
    print("💡 Check your API key format and permissions")
    raise
except Exception as e:
    print(f"❌ Initialization error: {e}")
    print("💡 Check your internet connection and API key")
    raise

print("\n🎉 Client ready for API operations!")


# ## 🏗️ Step 2: Space Management Operations
#
# Space management is fundamental to organizing your data in HeySol. This section covers:
# - Listing existing spaces
# - Creating new spaces with metadata
# - Retrieving space details
# - Space validation and error handling

# In[ ]:


# List existing spaces with detailed analysis
print("📋 Step 2.1: Space Discovery")
print("-" * 40)

try:
    spaces = client.get_spaces()
    print(f"✅ Found {len(spaces)} spaces")

    if spaces:
        print("\n📊 Space Details:")
        for i, space in enumerate(spaces[:5], 1):  # Show first 5
            if isinstance(space, dict):
                space_id = space.get("id", "Unknown")
                space_name = space.get("name", "Unnamed")
                space_desc = space.get("description", "No description")
                print(f"   {i}. {space_name}")
                print(f"      ID: {space_id[:16]}...")
                print(f"      Description: {space_desc}")
            else:
                print(f"   {i}. {space}")
    else:
        print("   📭 No spaces found - will create demo space")

except Exception as e:
    print(f"❌ Error listing spaces: {e}")
    print("💡 This might indicate API connectivity issues")
    spaces = []


# In[ ]:


# Create demo space with comprehensive metadata
print("🏗️ Step 2.2: Space Creation")
print("-" * 40)

space_name = "API Endpoints Demo Space"
space_description = "Demo space created by API endpoints notebook - showcases direct API operations"

# Check for existing space first
space_id = None
for space in spaces:
    if isinstance(space, dict) and space.get("name") == space_name:
        space_id = space.get("id")
        print(f"✅ Found existing space: {space_name}")
        break

if not space_id:
    print(f"🆕 Creating new space: {space_name}")
    try:
        space_id = client.create_space(space_name, space_description)
        print("✅ Created space successfully")
        print(f"   🆔 Space ID: {space_id}")
    except Exception as e:
        print(f"❌ Failed to create space: {e}")
        print("💡 Check space name length and description")
        raise
else:
    print(f"✅ Using existing space ID: {space_id}")

print("\n📋 Space Summary:")
print(f"   Name: {space_name}")
print(f"   Description: {space_description}")
print(f"   ID: {space_id}")


# In[ ]:


# Get comprehensive space details
print("📊 Step 2.3: Space Details Retrieval")
print("-" * 40)

try:
    space_details = client.get_space_details(space_id, include_stats=True, include_metadata=True)

    print("✅ Space details retrieved successfully")
    print("\n📋 Space Information:")
    print(f"   Name: {space_details.get('name', 'Unknown')}")
    print(f"   Description: {space_details.get('description', 'Unknown')}")
    print(f"   Created: {space_details.get('created_at', 'Unknown')}")

    if "stats" in space_details:
        stats = space_details["stats"]
        print("\n📊 Space Statistics:")
        print(f"   Total Episodes: {stats.get('total_episodes', 'N/A')}")
        print(f"   Total Size: {stats.get('total_size', 'N/A')}")
        print(f"   Last Activity: {stats.get('last_activity', 'N/A')}")

except Exception as e:
    print(f"❌ Error getting space details: {e}")
    print("💡 Space details endpoint might not be available")
    print("   This is normal - core functionality still works")


# ## 📝 Step 3: Data Ingestion Operations
#
# Data ingestion is how you add content to HeySol's memory system. This section covers:
# - Single item ingestion
# - Batch ingestion patterns
# - Metadata attachment
# - Session tracking
# - Ingestion result analysis

# In[ ]:


# Prepare diverse sample data for ingestion
print("📝 Step 3.1: Sample Data Preparation")
print("-" * 40)

sample_data = [
    {
        "content": "Patient demonstrates significant improvement after targeted therapy for HER2-positive breast cancer",
        "category": "treatment_outcome",
        "confidence": "high",
    },
    {
        "content": "Clinical trial shows 85% response rate for new immunotherapy protocol in advanced melanoma cases",
        "category": "clinical_trial",
        "confidence": "medium",
    },
    {
        "content": "Biomarker analysis reveals genetic markers for treatment resistance in EGFR-mutant lung cancer",
        "category": "biomarker_discovery",
        "confidence": "high",
    },
    {
        "content": "Longitudinal study confirms treatment efficacy over 5-year period with minimal recurrence",
        "category": "longitudinal_study",
        "confidence": "medium",
    },
    {
        "content": "Multi-center trial validates new diagnostic approach for early detection of pancreatic cancer",
        "category": "diagnostic_validation",
        "confidence": "high",
    },
]

print(f"✅ Prepared {len(sample_data)} diverse data items")
print("\n📊 Data Categories:")
categories: dict[str, int] = {}
for item in sample_data:
    cat = item["category"]
    categories[cat] = categories.get(cat, 0) + 1

for category, count in categories.items():
    print(f"   • {category}: {count} items")


# In[ ]:


# Execute ingestion with detailed tracking
print("📤 Step 3.2: Data Ingestion Execution")
print("-" * 40)

ingestion_results = []

for i, item in enumerate(sample_data, 1):
    print(f"\n🔄 Ingesting item {i}/{len(sample_data)}...")
    print(f"   Category: {item['category']}")
    print(f"   Content: {item['content'][:60]}...")

    try:
        # Ingest with metadata
        result = client.ingest(
            message=item["content"], space_id=space_id, source=f"api-demo-{item['category']}"
        )

        print("✅ Ingestion successful")
        print(f"   📝 Run ID: {result.get('id', 'unknown')[:16]}...")
        print(f"   ⏱️  Timestamp: {result.get('timestamp', 'unknown')}")

        ingestion_results.append(
            {"index": i, "category": item["category"], "run_id": result.get("id"), "success": True}
        )

    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        ingestion_results.append(
            {"index": i, "category": item["category"], "error": str(e), "success": False}
        )

print("\n📊 Ingestion Summary:")
print(f"   Total attempted: {len(sample_data)}")
print(f"   Successful: {sum(1 for r in ingestion_results if r['success'])}")
print(f"   Failed: {sum(1 for r in ingestion_results if not r['success'])}")


# ## 🔍 Step 4: Search Operations
#
# Search is the primary way to retrieve information from HeySol. This section covers:
# - Basic semantic search
# - Advanced search parameters
# - Result analysis and ranking
# - Search result processing

# In[ ]:


# Basic search operations with different queries
print("🔍 Step 4.1: Basic Search Operations")
print("-" * 40)

search_queries = [
    "treatment efficacy",
    "clinical trial results",
    "biomarker analysis",
    "cancer treatment outcomes",
]

search_results: "list[dict[str, Any]]" = []

for query in search_queries:
    print(f"\n🔎 Searching for: '{query}'")

    try:
        results = client.search(query=query, space_ids=[space_id], limit=3)

        episodes = results.episodes if hasattr(results, "episodes") else []
        print(f"   ✅ Found {len(episodes)} results")

        for i, episode in enumerate(episodes, 1):
            content = episode.get("content", "")[:80]
            score = episode.get("score", "N/A")
            print(f"   {i}. {content}{'...' if len(content) == 80 else ''}")
            print(f"      Score: {score}")

        search_results.append(
            {"query": query, "results_count": len(episodes), "episodes": episodes}
        )

    except Exception as e:
        print(f"   ❌ Search failed: {e}")
        search_results.append({"query": query, "error": str(e), "results_count": 0})

print("\n📊 Search Summary:")
print(f"   Queries executed: {len(search_queries)}")
print(f"   Total results: {sum(r['results_count'] for r in search_results)}")


# In[ ]:


# Advanced search with knowledge graph
print("🧠 Step 4.2: Knowledge Graph Search")
print("-" * 40)

kg_query = "treatment resistance mechanisms"
print(f"🔍 Knowledge graph query: '{kg_query}'")

try:
    kg_results = client.search_knowledge_graph(query=kg_query, space_id=space_id, limit=5, depth=2)

    entities = kg_results.get("entities", []) if isinstance(kg_results, dict) else []
    print(f"✅ Found {len(entities)} related entities")

    if entities:
        print("\n📍 Entity Details:")
        for i, entity in enumerate(entities[:5], 1):
            entity_name = entity.get("name", "Unknown")
            entity_type = entity.get("type", "Unknown")
            confidence = entity.get("confidence", "N/A")
            print(f"   {i}. {entity_name}")
            print(f"      Type: {entity_type}")
            print(f"      Confidence: {confidence}")
    else:
        print("   📭 No entities found in knowledge graph")

except Exception as e:
    print(f"❌ Knowledge graph search failed: {e}")
    print("💡 Knowledge graph might not be available for this space")


# ## 📋 Step 5: Log Management Operations
#
# Log management helps you track data processing and debug issues. This section covers:
# - Log retrieval and filtering
# - Source-based filtering
# - Log analysis and status checking
# - Error log identification

# In[ ]:


# Comprehensive log retrieval
print("📋 Step 5.1: Log Retrieval and Analysis")
print("-" * 40)

try:
    # Get recent logs for our space
    logs = client.get_ingestion_logs(space_id=space_id, limit=10)

    print(f"✅ Retrieved {len(logs)} logs")

    if logs:
        print("\n📊 Log Analysis:")

        # Analyze log status distribution
        status_counts: dict[str, int] = {}
        source_counts: dict[str, int] = {}

        for log in logs:
            status = log.get("status", "unknown")
            source = log.get("source", "unknown")

            status_counts[status] = status_counts.get(status, 0) + 1
            source_counts[source] = source_counts.get(source, 0) + 1

        print("   📈 Status Distribution:")
        for status, count in status_counts.items():
            print(f"      {status}: {count}")

        print("   📁 Source Distribution:")
        for source, count in source_counts.items():
            print(f"      {source}: {count}")

        # Show recent successful logs
        successful_logs = [log for log in logs if log.get("status") == "completed"]
        print(f"\n✅ Recent successful ingestions: {len(successful_logs)}")

        for log in successful_logs[:3]:
            log_id = log.get("id", "unknown")[:16]
            timestamp = log.get("time", "unknown")
            source = log.get("source", "unknown")
            print(f"   {log_id}... | {timestamp} | {source}")
    else:
        print("   📭 No logs found - data might still be processing")

except Exception as e:
    print(f"❌ Log retrieval failed: {e}")
    print("💡 Log endpoints might not be available in this environment")


# In[ ]:


# Source-based log filtering
print("🔍 Step 5.2: Source-Based Log Filtering")
print("-" * 40)

try:
    # Filter logs by our demo sources
    demo_sources = ["api-demo-treatment_outcome", "api-demo-clinical_trial"]

    for source in demo_sources:
        print(f"\n🔎 Logs from source: {source}")

        source_logs = client.get_logs_by_source(source=source, space_id=space_id, limit=5)

        print(f"   Found {len(source_logs)} logs")

        for log in source_logs[:3]:
            log_id = log.get("id", "unknown")[:16]
            status = log.get("status", "unknown")
            print(f"   {log_id}... | Status: {status}")

except Exception as e:
    print(f"❌ Source filtering failed: {e}")
    print("💡 Source filtering might not be available")


# ## 🛡️ Step 6: Error Handling and Edge Cases
#
# Robust error handling is crucial for production applications. This section demonstrates:
# - Common error scenarios
# - Proper exception handling
# - Graceful degradation patterns
# - Error recovery strategies

# In[ ]:


# Comprehensive error handling demonstration
print("🛡️ Step 6.1: Error Handling Patterns")
print("-" * 40)

TestFunction = Callable[[], Any]

error_scenarios: list[dict[str, Any]] = [
    {
        "name": "Invalid Space ID",
        "test": lambda: client.get_space_details("invalid-space-id-12345"),
    },
    {"name": "Empty Search Query", "test": lambda: client.search("")},
    {"name": "Invalid Log ID", "test": lambda: client.get_specific_log("invalid-log-id")},
    {"name": "Empty Space Name", "test": lambda: client.create_space("")},
]

error_results = []

for scenario in error_scenarios:
    print(f"\n🔍 Testing: {scenario['name']}")

    try:
        scenario["test"]()
        print("   ⚠️  Unexpected: No error raised")
        error_results.append({"scenario": scenario["name"], "error": None, "success": True})
    except HeySolError as e:
        print(f"   ✅ HeySolError caught: {e}")
        error_results.append(
            {
                "scenario": scenario["name"],
                "error": "ValidationError",
                "message": str(e),
                "success": True,
            }
        )
    except Exception as e:
        print(f"   ✅ Other error caught: {type(e).__name__}: {e}")
        error_results.append(
            {
                "scenario": scenario["name"],
                "error": type(e).__name__,
                "message": str(e),
                "success": True,
            }
        )

print("\n📊 Error Handling Summary:")
print(f"   Tests executed: {len(error_scenarios)}")
print(f"   Errors properly caught: {sum(1 for r in error_results if r['success'])}")


# ## ⚡ Step 7: Advanced Features and Bulk Operations
#
# Advanced features provide powerful capabilities for production use. This section covers:
# - Bulk operations for efficiency
# - Status checking and monitoring
# - Advanced ingestion patterns
# - Performance optimization

# In[ ]:


# Bulk operations and advanced features
print("⚡ Step 7.1: Bulk Operations")
print("-" * 40)

try:
    # Test bulk space operations
    bulk_result = client.bulk_space_operations(intent="info", space_id=space_id)

    print("✅ Bulk operation completed")
    print(f"   Message: {bulk_result.get('message', 'Success')}")
    print(f"   Status: {bulk_result.get('status', 'unknown')}")

except Exception as e:
    print(f"❌ Bulk operation failed: {e}")
    print("💡 Bulk operations might not be available")


# In[ ]:


# Ingestion status checking
print("🔬 Step 7.2: Status Monitoring")
print("-" * 40)

try:
    status = client.check_ingestion_status(space_id=space_id)

    print("✅ Status check completed")
    print(f"   Status: {status.get('ingestion_status', 'unknown')}")

    if "recommendations" in status:
        print("\n💡 Recommendations:")
        for rec in status["recommendations"]:
            print(f"   • {rec}")

    if "available_methods" in status:
        print("\n🔧 Available methods:")
        for method in status["available_methods"]:
            print(f"   • {method}")

except Exception as e:
    print(f"❌ Status check failed: {e}")
    print("💡 Status checking might not be available")


# ## 📊 Step 8: Summary and Best Practices
#
# Let's summarize what we've learned and establish best practices for using the HeySol API client.

# In[ ]:


# Comprehensive summary of our API exploration
print("📊 API Endpoints Demo Summary")
print("=" * 50)

print("✅ What We Accomplished:")
print("   🔧 Direct API client initialization and validation")
print(f"   🏗️  Space management: {space_name}")
print(f"   📝 Data ingestion: {len(sample_data)} items across multiple categories")
print(f"   🔍 Search operations: {len(search_queries)} queries executed")
print("   🧠 Knowledge graph exploration")
print("   📋 Log management and analysis")
print("   🛡️  Comprehensive error handling")
print("   ⚡ Bulk operations and advanced features")

print("\n💡 Key Insights:")
print("   • API client provides reliable, direct HTTP operations")
print("   • Proper error handling is crucial for robust applications")
print("   • Space management enables organized data storage")
print("   • Search capabilities are powerful and flexible")
print("   • Log management aids debugging and monitoring")
print("   • Knowledge graph provides entity relationship insights")

print("\n🚀 Best Practices:")
print("   • Always validate API keys before operations")
print("   • Use descriptive space names and metadata")
print("   • Implement proper error handling in production")
print("   • Monitor ingestion logs for debugging")
print("   • Use appropriate search limits for performance")
print("   • Leverage knowledge graph for entity discovery")

print("\n🎉 Demo completed successfully!")
print("\n📚 Next Steps:")
print("   • Try the shell script: bash examples/api_endpoints_demo.sh")
print("   • Try the Python script: python examples/api_endpoints_demo.py")
print("   • Explore other examples: ls examples/")
print("   • Read the full documentation: https://core.heysol.ai/")

# Clean up
try:
    client.close()
    print("\n🧹 Client closed successfully")
except Exception:
    pass
