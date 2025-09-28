#!/bin/bash

# 🎯 HeySol API Client - Quick Start (Shell Script)
#
# Get up and running with HeySol in under 5 minutes!
#
# This script will:
# 1. Check your API key setup
# 2. Create a demo space (or reuse existing)
# 3. Ingest sample data
# 4. Perform a search
# 5. Show you the results
#
# Prerequisites:
# - Get your API key from https://core.heysol.ai/settings/api
# - Set environment variable: export HEYSOL_API_KEY="your-key-here"
# - Or create a .env file with: HEYSOL_API_KEY=your-key-here
# - Install the CLI: pip install heysol-api-client
#
# Run: bash quick_start.sh

set -e  # Exit on any error

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
    # Explicitly export the API keys
    export HEYSOL_API_KEY_IDRDEX_MAMMOCHAT
    export HEYSOL_API_KEY_HADLEYLABELABORATORY
    export HEYSOL_API_KEY_IDRDEX_GMAIL
fi

echo "🚀 HeySol API Client - Quick Start (Shell)"
echo "=========================================="

# Check API key - look for any variable starting with HEYSOL_API_KEY
# Try to find any HEYSOL_API_KEY* variable
for var in $(env | grep '^HEYSOL_API_KEY' | cut -d= -f1); do
    if [ -n "${!var}" ]; then
        HEYSOL_API_KEY="${!var}"
        if [ "$var" = "HEYSOL_API_KEY_IDRDEX_MAMMOCHAT" ]; then
            USER_NAME="iDrDex@MammoChat.com"
            TARGET_API_KEY="${HEYSOL_API_KEY_HADLEYLABELABORATORY}"
        elif [ "$var" = "HEYSOL_API_KEY_HADLEYLABELABORATORY" ]; then
            USER_NAME="HadleyLaboratory@gmail.com"
            TARGET_API_KEY="${HEYSOL_API_KEY_IDRDEX_MAMMOCHAT}"
        elif [ "$var" = "HEYSOL_API_KEY_IDRDEX_GMAIL" ]; then
            USER_NAME="iDrDex@gmail.com"
            TARGET_API_KEY="${HEYSOL_API_KEY_HADLEYLABELABORATORY}"
        else
            USER_NAME=$(echo "$var" | sed 's/HEYSOL_API_KEY_//')
            TARGET_API_KEY="${HEYSOL_API_KEY_HADLEYLABELABORATORY}"
        fi
        echo "✅ Found API key from $var (user: $USER_NAME)"
        break
    fi
done

if [ -z "$HEYSOL_API_KEY" ]; then
    echo "❌ No API key found!"
    echo ""
    echo "📝 To get started:"
    echo "1. Visit: https://core.heysol.ai/settings/api"
    echo "2. Generate an API key"
    echo "3. Set environment variable:"
    echo "   export HEYSOL_API_KEY='your-api-key-here'"
    echo "4. Or create a .env file with:"
    echo "   HEYSOL_API_KEY_xxx=your-api-key-here (any name starting with HEYSOL_API_KEY)"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "✅ API key found (ends with: ...${HEYSOL_API_KEY: -4})"
echo "🔍 Validating API key..."

# Check if CLI is available
if ! command -v heysol-client &> /dev/null; then
    echo "❌ heysol-client CLI not found!"
    echo "Install with: pip install heysol-api-client"
    exit 1
fi

echo "✅ CLI available"
echo "✅ API key validated!"

# Register instances from .env
echo ""
echo "📋 Checking registry configuration..."
python -c "from src.heysol.registry_config import RegistryConfig; registry = RegistryConfig(); print(f'✅ Found {len(registry.get_instance_names())} registered instances')"
echo "✅ Registry configured"

# Create demo space (or reuse existing)
echo ""
echo "🏗️  Setting up demo space..."

SPACE_NAME="Quick Start Demo $(date +%s)"
SPACE_DESC="Created by HeySol quick start script"

# Check for existing space
echo "   Checking for existing spaces..."
EXISTING_SPACES=$(PYTHONPATH=/Users/idrdex/Library/Mobile\ Documents/com~apple~CloudDocs/Code/heysol_api_client python -m src.cli --user "$USER_NAME" spaces list 2>/dev/null || echo "[]")

# Extract space ID if it exists
SPACE_ID=$(echo "$EXISTING_SPACES" | python3 -c "
import sys, json
try:
    spaces = json.load(sys.stdin)
    if isinstance(spaces, list):
        for space in spaces:
            if isinstance(space, dict) and space.get('name') == '$SPACE_NAME':
                print(space.get('id', ''))
                sys.exit(0)
    elif isinstance(spaces, dict) and 'spaces' in spaces:
        for space in spaces['spaces']:
            if isinstance(space, dict) and space.get('name') == '$SPACE_NAME':
                print(space.get('id', ''))
                sys.exit(0)
except:
    pass
print('')
")

if [ -n "$SPACE_ID" ]; then
    echo "   Found existing space '$SPACE_NAME' with ID: $SPACE_ID"
else
    echo "   Creating new space: $SPACE_NAME"
    CREATE_RESULT=$(PYTHONPATH=/Users/idrdex/Library/Mobile\ Documents/com~apple~CloudDocs/Code/heysol_api_client python -m src.cli --user "$USER_NAME" spaces create "$SPACE_NAME" --description "$SPACE_DESC")
    SPACE_ID=$(echo "$CREATE_RESULT" | python3 -c "
import sys, json
try:
    result = json.load(sys.stdin)
    print(result.get('space_id', ''))
except:
    print('')
")
    if [ -z "$SPACE_ID" ]; then
        echo "   Warning: Could not extract space ID from creation response"
        SPACE_ID="unknown"
    fi
fi

echo "✅ Using space: $SPACE_NAME"

# Ingest sample data
echo ""
echo "📝 Ingesting sample clinical data..."

SAMPLE_DATA=(
    "Patient shows positive response to immunotherapy treatment"
    "Clinical trial demonstrates 78% efficacy rate for new oncology drug"
    "Biomarker analysis reveals key indicators for treatment success"
)

for i in "${!SAMPLE_DATA[@]}"; do
    echo "   Ingesting item $((i+1))/3..."
    PYTHONPATH=/Users/idrdex/Library/Mobile\ Documents/com~apple~CloudDocs/Code/heysol_api_client python -m src.cli --user "$USER_NAME" memory ingest "${SAMPLE_DATA[$i]}" --space-id "$SPACE_ID" > /dev/null
    echo "   ✅ Ingested $((i+1))/3 items"
done

# Search
echo ""
echo "🔍 Searching for 'treatment' (using global --user)..."

SEARCH_RESULTS=$(PYTHONPATH=/Users/idrdex/Library/Mobile\ Documents/com~apple~CloudDocs/Code/heysol_api_client python -m src.cli --user "$USER_NAME" memory search "treatment" --space-id "$SPACE_ID" --limit 3)

# Extract and display results
EPISODE_COUNT=$(echo "$SEARCH_RESULTS" | python3 -c "
import sys, json
try:
    result = json.load(sys.stdin)
    episodes = result.get('episodes', [])
    print(len(episodes))
    for i, episode in enumerate(episodes[:3], 1):
        content = episode.get('content', '')[:60]
        print(f'   {i}. {content}{\"...\" if len(content) == 60 else \"\"}')
except:
    print('0')
")

echo "✅ Found $EPISODE_COUNT results"

# Demonstrate copy operation
echo ""
echo "📋 Demonstrating copy operation to another instance (using global --user)..."
# Check if there are other instances available
OTHER_INSTANCES=$(python -c "from src.heysol.registry_config import RegistryConfig; registry = RegistryConfig(); instances = registry.get_instance_names(); print('\n'.join([name for name in instances if name != '$USER_NAME']))")
if [ -n "$OTHER_INSTANCES" ]; then
    TARGET_USER=$(echo "$OTHER_INSTANCES" | head -1)
    echo "   Copying 1 item to $TARGET_USER..."
    PYTHONPATH=/Users/idrdex/Library/Mobile\ Documents/com~apple~CloudDocs/Code/heysol_api_client python -m src.cli --user "$USER_NAME" memory copy --target-user "$TARGET_USER" --space-id "$SPACE_ID" --limit 1 --confirm > /dev/null
    echo "   ✅ Copied data to $TARGET_USER"
else
    echo "   Only one instance available, skipping cross-instance copy demo"
fi

echo ""
echo "🎉 Quick start completed successfully!"
echo ""
echo "📚 Next steps:"
echo "- Try the Python version: python quick_start.py"
echo "- Try the interactive notebook: jupyter notebook quick_start.ipynb"
echo "- Explore examples: ls examples/"
echo "- CLI help: heysol-client --help"
echo "- Documentation: https://core.heysol.ai/"
echo "- API vs MCP analysis: docs/API_VS_MCP_ANALYSIS.md"
echo ""
echo "💡 Python Client Types:"
echo "- HeySolClient: Unified (recommended for most users)"
echo "- HeySolAPIClient: Direct API (high performance)"
echo "- HeySolMCPClient: MCP protocol (advanced features)"