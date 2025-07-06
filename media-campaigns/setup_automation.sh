#!/bin/bash
"""
Linux Server Automation Setup Script
Sets up cron jobs and system automation for media campaigns
"""

echo "🚀 Setting up MarketWhine Media Campaign Automation..."

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Working directory: $SCRIPT_DIR"

# Make scripts executable
echo "📋 Making scripts executable..."
chmod +x "$SCRIPT_DIR/media_alert.py"
chmod +x "$SCRIPT_DIR/campaign_scheduler.py"
chmod +x "$SCRIPT_DIR/anonymous_email.py"

# Create log directory
echo "📁 Creating log directory..."
mkdir -p "$SCRIPT_DIR/logs"

# Test the campaign scheduler
echo "🧪 Testing campaign scheduler..."
cd "$SCRIPT_DIR"
python3 campaign_scheduler.py --list

# Schedule initial follow-up campaigns
echo "📅 Scheduling follow-up campaigns..."
python3 campaign_scheduler.py --schedule-followups

# Create systemd service for campaign checking
echo "⚙️ Creating systemd service..."

sudo tee /etc/systemd/system/marketwhine-campaigns.service > /dev/null <<EOF
[Unit]
Description=MarketWhine Campaign Checker
After=network.target

[Service]
Type=oneshot
User=$(whoami)
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/campaign_scheduler.py --check
StandardOutput=append:$SCRIPT_DIR/logs/campaign_service.log
StandardError=append:$SCRIPT_DIR/logs/campaign_service.log

[Install]
WantedBy=multi-user.target
EOF

# Create systemd timer for regular execution
echo "⏰ Creating systemd timer..."

sudo tee /etc/systemd/system/marketwhine-campaigns.timer > /dev/null <<EOF
[Unit]
Description=Run MarketWhine campaign checker daily
Requires=marketwhine-campaigns.service

[Timer]
OnCalendar=daily
RandomizedDelaySec=3600
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start the timer
echo "🔄 Enabling systemd timer..."
sudo systemctl daemon-reload
sudo systemctl enable marketwhine-campaigns.timer
sudo systemctl start marketwhine-campaigns.timer

# Create manual cron job backup (optional)
echo "📋 Setting up cron job backup..."

# Add to current user's crontab
CRON_JOB="0 9 * * * cd $SCRIPT_DIR && /usr/bin/python3 campaign_scheduler.py --check >> logs/cron.log 2>&1"

# Check if cron job already exists
if ! crontab -l 2>/dev/null | grep -q "campaign_scheduler.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added (runs daily at 9 AM)"
else
    echo "ℹ️ Cron job already exists"
fi

# Create campaign monitoring script
echo "📊 Creating monitoring script..."

cat > "$SCRIPT_DIR/monitor_campaigns.sh" << 'EOF'
#!/bin/bash
# Campaign monitoring script

echo "=== MarketWhine Campaign Status ==="
echo "Date: $(date)"
echo

cd "$(dirname "$0")"

echo "🏃 Running campaign check..."
python3 campaign_scheduler.py --check

echo
echo "📋 Current campaign schedule:"
python3 campaign_scheduler.py --list

echo
echo "📊 Recent campaign logs:"
tail -20 campaign_scheduler.log 2>/dev/null || echo "No logs found"

echo
echo "⚙️ Systemd timer status:"
sudo systemctl status marketwhine-campaigns.timer --no-pager -l

echo
echo "📅 Next scheduled runs:"
sudo systemctl list-timers marketwhine-campaigns.timer --no-pager
EOF

chmod +x "$SCRIPT_DIR/monitor_campaigns.sh"

# Create quick campaign launcher
echo "🚀 Creating quick campaign launcher..."

cat > "$SCRIPT_DIR/launch_campaign.sh" << 'EOF'
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
EOF

chmod +x "$SCRIPT_DIR/launch_campaign.sh"

# Test the setup
echo "🧪 Testing automation setup..."
sudo systemctl status marketwhine-campaigns.timer --no-pager

echo
echo "🎉 MarketWhine Automation Setup Complete!"
echo "========================================="
echo
echo "📋 What was set up:"
echo "✅ Campaign scheduler with follow-up automation"
echo "✅ Systemd service and timer (runs daily)"
echo "✅ Backup cron job (runs daily at 9 AM)"
echo "✅ Monitoring and launcher scripts"
echo
echo "🔧 Available commands:"
echo "  ./monitor_campaigns.sh     - Check campaign status"
echo "  ./launch_campaign.sh       - Launch immediate campaign"
echo "  python3 campaign_scheduler.py --list  - List all campaigns"
echo
echo "📅 Scheduled follow-ups:"
echo "  - 3 weeks: Site update campaign"
echo "  - 7 weeks: Second viral campaign"
echo "  - 12 weeks: Quarterly update"
echo
echo "⏰ Automation:"
echo "  - Checks daily for due campaigns"
echo "  - Logs to logs/ directory"
echo "  - Uses anonymous email system"
echo
echo "🏃 To check status now:"
echo "  ./monitor_campaigns.sh"