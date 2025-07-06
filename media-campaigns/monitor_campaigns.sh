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
