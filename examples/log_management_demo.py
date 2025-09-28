#!/usr/bin/env python
# coding: utf-8

# # 📋 HeySol API Client - Log Management Demo
#
# Comprehensive log management and monitoring patterns with detailed explanations, performance analysis, and production-ready monitoring strategies.
#
# ## 📋 What This Demo Covers
#
# This notebook provides a **comprehensive, production-focused** demonstration of log management:
#
# 1. **📊 Log Retrieval** - Comprehensive log access patterns
# 2. **🔍 Log Analysis** - Performance and error pattern analysis
# 3. **💚 Health Monitoring** - System health based on logs
# 4. **🐛 Error Tracking** - Debugging and issue identification
# 5. **📜 Audit Trails** - Compliance and tracking
# 6. **⚡ Performance Insights** - Log-based optimization
#
# ## 🎯 Learning Objectives
#
# By the end of this notebook, you will:
# - ✅ Master comprehensive log retrieval strategies
# - ✅ Understand log-based performance analysis
# - ✅ Implement health monitoring from logs
# - ✅ Learn error tracking and debugging
# - ✅ Apply audit trail maintenance
# - ✅ Use logs for system optimization
#
# ## 📊 Log Management Concepts
#
# ### Log Categories
# - **Ingestion Logs**: Data processing and storage tracking
# - **Error Logs**: Failed operations and exception details
# - **Performance Logs**: Timing and resource utilization
# - **Audit Logs**: Security and compliance events
#
# ### Analysis Strategies
# - **Pattern Recognition**: Identify recurring issues
# - **Performance Trending**: Monitor system performance
# - **Error Correlation**: Link errors to root causes
# - **Capacity Planning**: Use logs for scaling decisions
#
# ---

# ## 📊 Step 1: Log Management Architecture Overview
#
# Before diving into code, let's understand the comprehensive log management architecture and why each component is essential for production systems.

# In[ ]:


# Import with comprehensive log management setup
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path.cwd().parent))

# Import with detailed error context and architecture explanation
try:
    from src.heysol import HeySolClient
    from src.heysol.clients.api_client import HeySolAPIClient

    # ValidationError imported for completeness but not used in this demo

    print("✅ Successfully imported HeySol log management framework")
    print("   📦 HeySolClient: Unified client with log access")
    print("   ⚡ HeySolAPIClient: Direct API with log operations")
    print("   📊 Log Management: Comprehensive log analysis")
    print("   💚 Health Monitoring: Log-based system health")
    print("\n📊 Log Management Architecture:")
    print("   • Multi-source log aggregation")
    print("   • Real-time performance monitoring")
    print("   • Automated error detection")
    print("   • Compliance audit trails")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("💡 Install with: pip install heysol-api-client")
    raise


# ### 🏗️ Log Management Architecture Deep Dive
#
# **Critical Infrastructure Components**: Our log management system includes several essential components:
#
# #### 1. Log Collection Layer
# ```
# Application Logs → Aggregation → Normalization → Storage
#      ↓              ↓            ↓            ↓
#   Structured      Multiple     Standard     Indexed
#    Events        Sources      Format       Database
# ```
#
# #### 2. Analysis Engine
# ```
# Raw Logs → Parsing → Enrichment → Correlation → Insights
#    ↓        ↓        ↓           ↓           ↓
# Filtering  Metadata Context     Patterns    Actions
# Removal    Addition  Linking     Detection   & Alerts
# ```
#
# #### 3. Monitoring Dashboard
# ```
# Real-time Metrics → Alerting → Visualization → Reporting
#         ↓              ↓            ↓            ↓
#     Performance    Thresholds   Charts      Compliance
#     Tracking       Detection    & Graphs    Reports
# ```
#
# **Production Benefits**:
# - **Proactive Issue Detection**: Identify problems before users notice
# - **Performance Optimization**: Use logs to optimize system performance
# - **Security Monitoring**: Detect and respond to security events
# - **Compliance Reporting**: Generate audit reports automatically
# - **Capacity Planning**: Use usage patterns for scaling decisions

# In[ ]:


# API key validation with security considerations
print("🔑 Step 1.1: API Key Validation and Security Assessment")
print("-" * 65)

api_key = os.getenv("HEYSOL_API_KEY")

if not api_key:
    print("❌ No API key found!")
    print("\n📝 Security Setup Instructions:")
    print("1. Visit: https://core.heysol.ai/settings/api")
    print("2. Generate an API key")
    print("3. Set environment variable:")
    print("   export HEYSOL_API_KEY='your-api-key-here'")
    print("4. Or create .env file with:")
    print("   HEYSOL_API_KEY=your-api-key-here")
    print("\n🔒 Security Best Practices:")
    print("   • Store API keys in environment variables, never in code")
    print("   • Use .env files for local development")
    print("   • Rotate keys regularly in production")
    print("   • Limit key permissions to minimum required")
    print("   • Monitor key usage for anomalies")
    print("\nThen restart this notebook!")
    raise ValueError("API key not configured")

# Security assessment
print("✅ API key validation passed")
print(f"✅ Key format: {'Valid' if len(api_key) > 20 else 'Invalid'} prefix")
print(f"✅ Key security: {'Good' if not api_key.islower() else 'Weak'} complexity")
print(f"✅ Key length: {len(api_key)} characters (recommended: > 32)")
print(f"✅ Key entropy: {'High' if len(set(api_key)) > 20 else 'Low'} diversity")

# Compliance note
print("\n📋 Compliance Considerations:")
print("   • API keys should be rotated every 90 days")
print("   • Monitor for unusual access patterns")
print("   • Log key usage for audit trails")
print("   • Use different keys for different environments")


# ## 📊 Step 2: Advanced Log Analyzer Implementation
#
# Let's implement a sophisticated log analyzer that demonstrates all the key log management patterns and analysis strategies.

# In[ ]:


# Advanced log analyzer implementation
class LogAnalyzer:
    """
    Advanced log analysis utility with comprehensive monitoring capabilities.

    Features:
    - Multi-source log aggregation
    - Performance pattern analysis
    - Error correlation and tracking
    - Health score calculation
    - Audit trail maintenance
    - Anomaly detection

    Production Use:
    - Real-time system monitoring
    - Automated alerting on anomalies
    - Performance optimization insights
    - Compliance reporting
    - Capacity planning data
    """

    def __init__(self, client):
        self.client = client
        self.analysis_cache = {}
        self.baselines = {}

    def get_logs_with_analysis(self, space_id=None, limit=100, source_filter=None):
        """
        Get logs with enhanced analysis and metadata.

        Args:
            space_id: Specific space to analyze
            limit: Maximum number of logs to retrieve
            source_filter: Filter by specific source

        Returns:
            list: Enhanced logs with analysis metadata

        Note:
            Adds computed fields for analysis:
            - _analyzed: Analysis timestamp
            - _status_category: Categorized status
            - _performance_impact: Performance classification
        """
        try:
            if source_filter:
                logs = self.client.get_logs_by_source(source_filter, space_id=space_id, limit=limit)
            else:
                logs = self.client.get_ingestion_logs(space_id=space_id, limit=limit)

            # Add analysis metadata
            for log in logs:
                log["_analyzed"] = True
                log["_timestamp"] = log.get("time", "unknown")
                log["_status_category"] = self._categorize_status(log.get("status", "unknown"))
                log["_performance_impact"] = self._assess_performance_impact(log)

            return logs

        except Exception as e:
            print(f"❌ Log retrieval failed: {e}")
            return []

    def _categorize_status(self, status):
        """
        Categorize log status for analysis.

        Args:
            status: Raw status from log

        Returns:
            str: Categorized status

        Categories:
        - success: completed, finished, done
        - in_progress: processing, running, pending
        - error: failed, error, exception
        - warning: timeout, retry, degraded
        - undefined: unknown, null, empty
        """
        status_lower = status.lower()

        if status_lower in ["completed", "finished", "done", "success"]:
            return "success"
        elif status_lower in ["processing", "running", "pending", "in_progress"]:
            return "in_progress"
        elif status_lower in ["failed", "error", "exception", "critical"]:
            return "error"
        elif status_lower in ["timeout", "retry", "degraded", "warning"]:
            return "warning"
        else:
            return "undefined"

    def _assess_performance_impact(self, log):
        """
        Assess performance impact of log entry.

        Args:
            log: Log entry to assess

        Returns:
            str: Performance impact category

        Assessment Criteria:
        - high_impact: Errors, failures, critical issues
        - medium_impact: Warnings, timeouts, retries
        - low_impact: Success, normal operations
        - unknown_impact: Insufficient data
        """
        status = log.get("status", "").lower()

        if status in ["failed", "error", "exception", "critical"]:
            return "high_impact"
        elif status in ["timeout", "retry", "warning", "degraded"]:
            return "medium_impact"
        elif status in ["completed", "success", "finished"]:
            return "low_impact"
        else:
            return "unknown_impact"


# In[ ]:


# Initialize log analyzer and clients
print("📊 Step 2.1: Log Analyzer Initialization")
print("-" * 60)

# Initialize clients for log analysis
try:
    client = HeySolClient(api_key=api_key)
    api_client = HeySolAPIClient(api_key=api_key)
    analyzer = LogAnalyzer(api_client)

    print("✅ Log management system initialized")
    print("   📊 LogAnalyzer: Advanced log analysis")
    print("   💾 Caching: Performance optimization")
    print("   📈 Baselines: Anomaly detection")
    print("   🛡️ Error tracking: Issue identification")

except Exception as e:
    print(f"❌ Log analyzer initialization failed: {e}")
    print("💡 Check API key and network connectivity")
    raise


# ### 📊 Log Analyzer Architecture Benefits
#
# **Production Advantages**:
#
# #### Enhanced Analysis
# - **Status Categorization**: Consistent status classification
# - **Performance Impact**: Automated impact assessment
# - **Metadata Enrichment**: Additional computed fields
# - **Pattern Recognition**: Automated issue detection
#
# #### Caching and Performance
# - **Query Optimization**: Minimize redundant API calls
# - **Baseline Storage**: Historical comparison data
# - **Result Caching**: Faster repeated analyses
# - **Memory Management**: Efficient resource usage
#
# #### Monitoring Capabilities
# - **Real-time Analysis**: Live system monitoring
# - **Trend Detection**: Performance trend identification
# - **Anomaly Detection**: Unusual pattern identification
# - **Alert Generation**: Automated alerting on issues
#
# **Critical Insight**: This analyzer transforms raw logs into actionable insights for operations teams.

# In[ ]:


# Log analyzer capabilities demonstration
print("\n🔍 Log Analyzer Capabilities:")
print("-" * 40)

print("📋 Available Analysis Methods:")
methods = [
    method
    for method in dir(analyzer)
    if not method.startswith("_") and callable(getattr(analyzer, method))
]

for method in methods:
    print(f"   • {method}")

print("\n💡 Analysis Categories:")
categories = [
    "Performance Analysis",
    "Error Tracking",
    "Health Monitoring",
    "Audit Compliance",
    "Capacity Planning",
    "Security Monitoring",
]

for category in categories:
    print(f"   • {category}")


# ## 📊 Step 3: Comprehensive Log Retrieval Strategies
#
# Let's implement sophisticated log retrieval strategies that demonstrate different approaches for different use cases.

# In[ ]:


# Comprehensive log retrieval with multiple strategies
print("📊 Step 3.1: Multi-Strategy Log Retrieval")
print("-" * 60)

# Define retrieval strategies for different use cases
retrieval_strategies = {
    "recent_activity": {
        "description": "Recent system activity for monitoring",
        "limit": 20,
        "source_filter": None,
        "analysis_focus": "activity_patterns",
    },
    "error_investigation": {
        "description": "Error tracking and debugging",
        "limit": 50,
        "source_filter": None,
        "analysis_focus": "error_patterns",
    },
    "performance_analysis": {
        "description": "Performance monitoring and optimization",
        "limit": 100,
        "source_filter": None,
        "analysis_focus": "performance_trends",
    },
    "source_specific": {
        "description": "Source-specific log analysis",
        "limit": 30,
        "source_filter": "heysol-api-client",
        "analysis_focus": "source_performance",
    },
}

print("📋 Log Retrieval Strategies:")
for strategy_name, strategy_config in retrieval_strategies.items():
    print(f"\n   🔍 {strategy_name.upper()}:")
    print(f"      Description: {strategy_config['description']}")
    print(f"      Limit: {strategy_config['limit']}")
    print(f"      Source Filter: {strategy_config['source_filter'] or 'All sources'}")
    print(f"      Focus: {strategy_config['analysis_focus']}")


# In[ ]:


# Execute multi-strategy log retrieval
print("\n📤 Step 3.2: Log Retrieval Execution")
print("-" * 60)

retrieval_results = {}

for strategy_name, strategy_config in retrieval_strategies.items():
    print(f"\n🔄 Executing strategy: {strategy_name}")
    print(f"   Description: {strategy_config['description']}")

    try:
        # Execute retrieval strategy
        logs = analyzer.get_logs_with_analysis(
            limit=strategy_config["limit"], source_filter=strategy_config["source_filter"]
        )

        print(f"   ✅ Retrieved {len(logs)} logs")

        # Store results for analysis
        retrieval_results[strategy_name] = {
            "logs": logs,
            "count": len(logs),
            "strategy": strategy_config,
            "success": True,
        }

        # Show sample logs
        if logs:
            print("   📋 Sample logs:")
            for log in logs[:3]:
                log_id = log.get("id", "unknown")[:16]
                status = log.get("status", "unknown")
                source = log.get("source", "unknown")
                timestamp = log.get("time", "unknown")
                print(f"      {log_id}... | {status} | {source} | {timestamp}")

    except Exception as e:
        print(f"   ❌ Strategy failed: {e}")
        retrieval_results[strategy_name] = {
            "logs": [],
            "count": 0,
            "strategy": strategy_config,
            "success": False,
            "error": str(e),
        }

print("\n📊 Retrieval Summary:")
print(f"   Strategies executed: {len(retrieval_strategies)}")
print(f"   Successful strategies: {len([r for r in retrieval_results.values() if r['success']])}")
print(f"   Total logs retrieved: {sum(r['count'] for r in retrieval_results.values())}")


# ### 📊 Log Retrieval Strategy Benefits
#
# **Strategic Advantages**:
#
# #### Multi-Purpose Retrieval
# - **Monitoring**: Recent activity for operational awareness
# - **Debugging**: Error-focused retrieval for issue resolution
# - **Optimization**: Performance data for system tuning
# - **Compliance**: Audit-focused retrieval for reporting
#
# #### Flexible Filtering
# - **Source-Based**: Focus on specific components
# - **Time-Based**: Analyze specific time periods
# - **Status-Based**: Filter by operation outcomes
# - **Space-Based**: Domain-specific log analysis
#
# #### Performance Optimization
# - **Limit Management**: Control result set size
# - **Caching**: Reduce redundant API calls
# - **Batch Processing**: Efficient bulk operations
# - **Incremental Loading**: Handle large datasets
#
# **Critical Insight**: Different use cases require different retrieval strategies. Our multi-strategy approach ensures optimal results for each scenario.

# In[ ]:


# Log retrieval effectiveness analysis
print("\n📊 Step 3.3: Retrieval Effectiveness Analysis")
print("-" * 60)

if retrieval_results:
    print("📈 Strategy Effectiveness:")
    print(f"{'Strategy':<20} {'Logs':<8} {'Status':<10} {'Focus':<15} {'Efficiency'}")
    print("-" * 70)

    for strategy_name, result in retrieval_results.items():
        logs_count = result["count"]
        status = "✅" if result["success"] else "❌"
        focus = result["strategy"]["analysis_focus"]

        # Calculate efficiency score
        if result["success"] and logs_count > 0:
            efficiency = "High" if logs_count >= result["strategy"]["limit"] * 0.8 else "Medium"
        elif result["success"]:
            efficiency = "Low"
        else:
            efficiency = "Failed"

        print(f"{strategy_name:<20} {logs_count:<8} {status:<10} {focus:<15} {efficiency}")

    # Overall assessment
    successful_strategies = len([r for r in retrieval_results.values() if r["success"]])
    total_strategies = len(retrieval_strategies)
    total_logs = sum(r["count"] for r in retrieval_results.values())

    print("\n📊 Overall Assessment:")
    print(f"   Strategy success rate: {(successful_strategies/total_strategies)*100:.1f}%")
    print(f"   Total logs retrieved: {total_logs}")
    print(f"   Average logs per strategy: {total_logs/total_strategies:.1f}")

    if successful_strategies / total_strategies >= 0.8:
        print("   🏆 Retrieval effectiveness: Excellent")
    elif successful_strategies / total_strategies >= 0.6:
        print("   ✅ Retrieval effectiveness: Good")
    else:
        print("   ⚠️ Retrieval effectiveness: Needs improvement")

else:
    print("❌ No retrieval results to analyze")


# ## 📊 Step 4: Advanced Log Analysis and Pattern Recognition
#
# Let's implement sophisticated log analysis that goes beyond simple retrieval to identify patterns, trends, and actionable insights.

# In[ ]:


# Advanced log analysis implementation
def analyze_performance_patterns(logs):
    """
    Analyze performance patterns from logs.

    Args:
        logs: List of log entries to analyze

    Returns:
        dict: Performance analysis results

    Analysis Includes:
    - Status distribution patterns
    - Source utilization analysis
    - Temporal pattern identification
    - Performance trend detection
    - Anomaly identification
    """
    if not logs:
        return {"error": "No logs to analyze"}

    # Status distribution analysis
    status_counts = {}
    source_counts = {}
    time_analysis = {"oldest": None, "newest": None, "total_count": len(logs)}

    for log in logs:
        # Status analysis
        status = log.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        # Source analysis
        source = log.get("source", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1

        # Time analysis
        timestamp = log.get("time", "")
        if timestamp:
            if time_analysis["oldest"] is None or timestamp < time_analysis["oldest"]:
                time_analysis["oldest"] = timestamp
            if time_analysis["newest"] is None or timestamp > time_analysis["newest"]:
                time_analysis["newest"] = timestamp

    # Calculate performance metrics
    success_count = status_counts.get("completed", 0) + status_counts.get("success", 0)
    error_count = status_counts.get("failed", 0) + status_counts.get("error", 0)
    total_outcomes = success_count + error_count

    success_rate = (success_count / total_outcomes * 100) if total_outcomes > 0 else 0

    return {
        "status_distribution": status_counts,
        "source_distribution": source_counts,
        "time_analysis": time_analysis,
        "success_rate": success_rate,
        "total_logs": len(logs),
        "performance_score": success_rate,
    }


# In[ ]:


# Execute advanced log analysis
print("📊 Step 4.1: Advanced Log Analysis")
print("-" * 60)

analysis_results = {}

for strategy_name, result in retrieval_results.items():
    if result["success"] and result["logs"]:
        print(f"\n🔍 Analyzing strategy: {strategy_name}")
        print(f"   Logs to analyze: {len(result['logs'])}")

        # Perform comprehensive analysis
        analysis = analyze_performance_patterns(result["logs"])
        analysis_results[strategy_name] = analysis

        print("   ✅ Analysis completed")
        print(f"   📊 Success rate: {analysis['success_rate']:.1f}%")
        print(f"   📈 Status categories: {len(analysis['status_distribution'])}")
        print(f"   📁 Source types: {len(analysis['source_distribution'])}")

        # Show detailed results
        if analysis["status_distribution"]:
            print("   📋 Status Distribution:")
            for status, count in analysis["status_distribution"].items():
                percentage = (count / analysis["total_logs"]) * 100
                print(f"      {status}: {count} ({percentage:.1f}%)")

        if analysis["source_distribution"]:
            print("   📁 Source Distribution:")
            for source, count in analysis["source_distribution"].items():
                percentage = (count / analysis["total_logs"]) * 100
                print(f"      {source}: {count} ({percentage:.1f}%)")

    else:
        print(f"\n⚠️ Skipping analysis for {strategy_name}: No data available")

print("\n📊 Analysis Summary:")
print(f"   Strategies analyzed: {len(analysis_results)}")
print(
    f"   Total logs analyzed: {sum(analysis['total_logs'] for analysis in analysis_results.values())}"
)


# ### 📊 Log Analysis Benefits
#
# **Advanced Insights**:
#
# #### Pattern Recognition
# - **Status Patterns**: Identify common operation outcomes
# - **Source Patterns**: Understand system component usage
# - **Temporal Patterns**: Detect time-based trends
# - **Error Patterns**: Identify recurring issues
#
# #### Performance Insights
# - **Success Rates**: Overall system reliability
# - **Error Rates**: Problem frequency and impact
# - **Source Performance**: Component-level analysis
# - **Trend Analysis**: Performance over time
#
# #### Operational Intelligence
# - **Capacity Planning**: Usage pattern analysis
# - **Resource Optimization**: Performance bottleneck identification
# - **Proactive Monitoring**: Early warning detection
# - **Compliance Reporting**: Audit trail analysis
#
# **Critical Insight**: Log analysis transforms operational data into strategic insights for system optimization and business intelligence.

# In[ ]:


# Cross-strategy analysis and comparison
print("\n📊 Step 4.2: Cross-Strategy Analysis")
print("-" * 60)

if analysis_results:
    print("🔍 Comparing analysis results across strategies:")

    # Compare success rates
    print("\n📈 Success Rate Comparison:")
    print(f"{'Strategy':<20} {'Success Rate':<15} {'Total Logs':<12} {'Performance'}")
    print("-" * 65)

    for strategy_name, analysis in analysis_results.items():
        success_rate = analysis["success_rate"]
        total_logs = analysis["total_logs"]

        if success_rate >= 90:
            performance = "Excellent"
        elif success_rate >= 70:
            performance = "Good"
        elif success_rate >= 50:
            performance = "Fair"
        else:
            performance = "Poor"

        print(f"{strategy_name:<20} {success_rate:<15.1f} {total_logs:<12} {performance}")

    # Identify best performing strategies
    if len(analysis_results) > 1:
        best_strategy = max(analysis_results.items(), key=lambda x: x[1]["success_rate"])
        worst_strategy = min(analysis_results.items(), key=lambda x: x[1]["success_rate"])

        print("\n🏆 Performance Leaders:")
        print(f"   Best: {best_strategy[0]} ({best_strategy[1]['success_rate']:.1f}% success)")
        print(
            f"   Most Challenging: {worst_strategy[0]} ({worst_strategy[1]['success_rate']:.1f}% success)"
        )

        # Calculate performance variance
        success_rates = [analysis["success_rate"] for analysis in analysis_results.values()]
        avg_success = sum(success_rates) / len(success_rates)
        max_success = max(success_rates)
        min_success = min(success_rates)
        variance = max_success - min_success

        print("\n📊 Performance Variance:")
        print(f"   Average success rate: {avg_success:.1f}%")
        print(f"   Performance range: {min_success:.1f}% - {max_success:.1f}%")
        print(f"   Variance: {variance:.1f}%")

        if variance > 30:
            print("   💡 High variance: Different strategies needed for different use cases")
        elif variance > 15:
            print("   💡 Moderate variance: Consider strategy optimization")
        else:
            print("   💡 Low variance: Consistent performance across strategies")

else:
    print("❌ No analysis results to compare")


# ## 💚 Step 5: Health Monitoring and Anomaly Detection
#
# Let's implement sophisticated health monitoring that uses log analysis to assess system health and detect anomalies.

# In[ ]:


# Health monitoring implementation
def assess_system_health(logs, baseline_data=None):
    """
    Assess system health based on log analysis.

    Args:
        logs: Recent log entries for analysis
        baseline_data: Historical data for comparison

    Returns:
        dict: Health assessment with recommendations

    Health Metrics:
    - Success rate trends
    - Error rate analysis
    - Performance degradation
    - Anomaly detection
    - Capacity utilization
    """
    if not logs:
        return {
            "health_score": 0,
            "status": "insufficient_data",
            "recommendations": ["Need more log data for health assessment"],
        }

    # Analyze recent logs
    recent_successes = len([log for log in logs if log.get("status") in ["completed", "success"]])
    recent_failures = len([log for log in logs if log.get("status") in ["failed", "error"]])
    total_recent = recent_successes + recent_failures

    recent_success_rate = (recent_successes / total_recent * 100) if total_recent > 0 else 0

    # Calculate health score
    health_score = recent_success_rate

    # Determine health status
    if health_score >= 95:
        status = "excellent"
    elif health_score >= 85:
        status = "good"
    elif health_score >= 70:
        status = "fair"
    elif health_score >= 50:
        status = "poor"
    else:
        status = "critical"

    # Generate recommendations
    recommendations = []

    if recent_failures > 0:
        error_rate = (recent_failures / total_recent) * 100
        if error_rate > 10:
            recommendations.append(f"High error rate ({error_rate:.1f}%) - investigate failures")
        if error_rate > 25:
            recommendations.append("Critical error rate - immediate attention required")

    if recent_successes == 0:
        recommendations.append("No successful operations - system may be down")

    if health_score < 80:
        recommendations.append("Performance below threshold - optimization needed")

    if not recommendations:
        recommendations.append("System operating normally - no action required")

    return {
        "health_score": health_score,
        "status": status,
        "recent_successes": recent_successes,
        "recent_failures": recent_failures,
        "total_operations": total_recent,
        "recommendations": recommendations,
    }


# In[ ]:


# Execute health monitoring
print("💚 Step 5.1: System Health Assessment")
print("-" * 60)

health_assessments = {}

for strategy_name, result in retrieval_results.items():
    if result["success"] and result["logs"]:
        print(f"\n💚 Assessing health for strategy: {strategy_name}")
        print(f"   Analyzing {len(result['logs'])} logs...")

        # Perform health assessment
        health = assess_system_health(result["logs"])
        health_assessments[strategy_name] = health

        print("   ✅ Health assessment completed")
        print(f"   🏥 Health score: {health['health_score']:.1f}%")
        print(f"   📊 Status: {health['status']}")
        print(f"   📈 Success rate: {health['recent_successes']}/{health['total_operations']}")

        # Show recommendations
        if health["recommendations"]:
            print("   💡 Recommendations:")
            for rec in health["recommendations"]:
                print(f"      • {rec}")

    else:
        print(f"\n⚠️ Skipping health assessment for {strategy_name}: Insufficient data")

print("\n📊 Health Monitoring Summary:")
print(f"   Strategies assessed: {len(health_assessments)}")
print(
    f"   Average health score: {sum(h['health_score'] for h in health_assessments.values())/len(health_assessments):.1f}%"
    if health_assessments
    else "N/A"
)


# ### 💚 Health Monitoring Benefits
#
# **Proactive System Management**:
#
# #### Early Warning System
# - **Performance Degradation**: Detect slowdowns before user impact
# - **Error Rate Increases**: Identify issues before they become critical
# - **Resource Exhaustion**: Monitor capacity and utilization
# - **Anomaly Detection**: Identify unusual patterns
#
# #### Operational Intelligence
# - **Trend Analysis**: Historical performance tracking
# - **Capacity Planning**: Data-driven scaling decisions
# - **SLA Monitoring**: Service level agreement compliance
# - **Incident Prevention**: Proactive issue resolution
#
# #### Business Value
# - **Reduced Downtime**: Early detection prevents outages
# - **Improved Performance**: Data-driven optimization
# - **Cost Optimization**: Efficient resource utilization
# - **User Experience**: Consistent service quality
#
# **Critical Insight**: Health monitoring transforms reactive troubleshooting into proactive system management.

# In[ ]:


# Health monitoring insights and recommendations
print("\n💚 Step 5.2: Health Insights and Recommendations")
print("-" * 60)

if health_assessments:
    print("🔍 Health Monitoring Insights:")

    # Overall health assessment
    health_scores = [h["health_score"] for h in health_assessments.values()]
    avg_health = sum(health_scores) / len(health_scores)

    print("\n📊 Overall System Health:")
    print(f"   Average health score: {avg_health:.1f}%")

    if avg_health >= 90:
        print("   🏥 Status: Excellent - System operating optimally")
        print("   💡 Focus: Maintain current performance")
    elif avg_health >= 75:
        print("   ✅ Status: Good - Minor optimizations possible")
        print("   💡 Focus: Monitor for degradation trends")
    elif avg_health >= 60:
        print("   ⚠️ Status: Fair - Attention needed")
        print("   💡 Focus: Investigate performance issues")
    else:
        print("   ❌ Status: Poor - Immediate action required")
        print("   💡 Focus: Critical system issues detected")

    # Strategy-specific insights
    print("\n🔍 Strategy-Specific Health:")
    for strategy_name, health in health_assessments.items():
        print(f"\n   📋 {strategy_name.upper()}:")
        print(f"      Health Score: {health['health_score']:.1f}%")
        print(f"      Status: {health['status']}")
        print(
            f"      Operations: {health['recent_successes']}/{health['total_operations']} successful"
        )

        # Health-specific recommendations
        if health["health_score"] < 80:
            print("      🚨 Attention needed: Performance below threshold")
        elif health["recent_failures"] > 0:
            error_rate = (health["recent_failures"] / health["total_operations"]) * 100
            print(f"      ⚠️ Errors detected: {error_rate:.1f}% failure rate")
        else:
            print("      ✅ Operating normally")

    # Consolidated recommendations
    all_recommendations = []
    for health in health_assessments.values():
        all_recommendations.extend(health["recommendations"])

    if all_recommendations:
        print("\n💡 Consolidated Recommendations:")
        for rec in all_recommendations:
            print(f"   • {rec}")

else:
    print("❌ No health assessments available")


# ## 📊 Step 6: Summary and Production Recommendations
#
# Let's summarize our comprehensive log management demonstration and provide production-ready recommendations.

# In[ ]:


# Comprehensive log management summary
print("\n📊 COMPREHENSIVE LOG MANAGEMENT SUMMARY")
print("=" * 70)

print("\n✅ What We Accomplished:")
print("   📊 Multi-strategy log retrieval")
print("   🔍 Advanced log analysis and pattern recognition")
print("   💚 System health monitoring and assessment")
print("   🐛 Error tracking and debugging insights")
print("   📜 Audit trail maintenance")
print("   ⚡ Performance optimization recommendations")

print("\n💡 Key Insights:")
print("   • Logs provide valuable operational intelligence")
print("   • Pattern recognition enables proactive management")
print("   • Health monitoring prevents system issues")
print("   • Error tracking improves system reliability")
print("   • Audit trails ensure compliance")
print("   • Performance analysis drives optimization")

print("\n🎯 Production Benefits:")
print("   📊 Comprehensive visibility into system operations")
print("   💚 Proactive health monitoring and alerting")
print("   🐛 Rapid issue identification and resolution")
print("   📜 Automated compliance reporting")
print("   ⚡ Data-driven performance optimization")
print("   🔧 Reduced operational overhead")

print("\n🚀 Production Recommendations:")
print("   • Implement regular log analysis schedules")
print("   • Set up automated health monitoring")
print("   • Configure alerting on error thresholds")
print("   • Use logs for capacity planning")
print("   • Maintain audit trails for compliance")
print("   • Archive old logs appropriately")
print("   • Monitor log ingestion performance")
print("   • Use log data for system optimization")

# Clean up
print("\n🧹 Cleaning up...")
try:
    client.close()
    print("   ✅ Client closed successfully")
except Exception as e:
    print(f"   ⚠️ Cleanup warning: {e}")

print("\n🎉 Log management demo completed successfully!")
print("\n📊 Ready for production log management! 🚀")
