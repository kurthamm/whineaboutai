#!/bin/bash
# Quick campaign launcher

echo "🚀 MarketWhine Quick Campaign Launcher"
echo "===================================="

cd "$(dirname "$0")"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <template> [target_groups]"
    echo
    echo "Available templates:"
    echo "  - viral_story"
    echo "  - site_update" 
    echo "  - announcement"
    echo "  - new_feature"
    echo "  - whistleblower"
    echo
    echo "Available target groups:"
    echo "  - tech_press"
    echo "  - mainstream"
    echo "  - policy"
    echo "  - all (default)"
    echo
    echo "Example: $0 viral_story tech_press mainstream"
    exit 1
fi

TEMPLATE=$1
shift
GROUPS=${@:-tech_press mainstream policy}

echo "Template: $TEMPLATE"
echo "Target groups: $GROUPS"
echo

read -p "Proceed with anonymous campaign? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Launching campaign..."
    
    # Add as event-driven campaign
    python3 campaign_scheduler.py --add-event "$TEMPLATE" --groups $GROUPS
    
    # Execute immediately
    python3 campaign_scheduler.py --check
    
    echo "✅ Campaign completed!"
else
    echo "❌ Campaign cancelled"
fi
