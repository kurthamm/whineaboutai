#!/usr/bin/env python3
"""
Campaign Analytics and Tracking System
Tracks campaign performance and website metrics
"""

import json
import requests
import datetime
import logging
from typing import Dict, List, Optional
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CampaignMetrics:
    campaign_id: str
    emails_sent: int
    execution_date: datetime.datetime
    website_visits_before: int = 0
    website_visits_after: int = 0
    referral_traffic: Dict = None
    social_mentions: int = 0
    media_coverage: List = None

class CampaignAnalytics:
    """Track and analyze campaign performance"""
    
    def __init__(self, analytics_file: str = "campaign_analytics.json"):
        self.analytics_file = analytics_file
        self.metrics = []
        self.load_analytics()
    
    def load_analytics(self):
        """Load existing analytics data"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
                for metric_data in data.get('metrics', []):
                    metric = CampaignMetrics(
                        campaign_id=metric_data['campaign_id'],
                        emails_sent=metric_data['emails_sent'],
                        execution_date=datetime.datetime.fromisoformat(metric_data['execution_date']),
                        website_visits_before=metric_data.get('website_visits_before', 0),
                        website_visits_after=metric_data.get('website_visits_after', 0),
                        referral_traffic=metric_data.get('referral_traffic', {}),
                        social_mentions=metric_data.get('social_mentions', 0),
                        media_coverage=metric_data.get('media_coverage', [])
                    )
                    self.metrics.append(metric)
        except FileNotFoundError:
            self.metrics = []
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            self.metrics = []
    
    def save_analytics(self):
        """Save analytics data"""
        try:
            data = {
                'metrics': [],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            for metric in self.metrics:
                metric_data = {
                    'campaign_id': metric.campaign_id,
                    'emails_sent': metric.emails_sent,
                    'execution_date': metric.execution_date.isoformat(),
                    'website_visits_before': metric.website_visits_before,
                    'website_visits_after': metric.website_visits_after,
                    'referral_traffic': metric.referral_traffic or {},
                    'social_mentions': metric.social_mentions,
                    'media_coverage': metric.media_coverage or []
                }
                data['metrics'].append(metric_data)
            
            with open(self.analytics_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def record_campaign_execution(self, campaign_id: str, emails_sent: int):
        """Record when a campaign was executed"""
        
        # Get baseline website metrics before impact
        baseline_visits = self.get_website_baseline()
        
        metric = CampaignMetrics(
            campaign_id=campaign_id,
            emails_sent=emails_sent,
            execution_date=datetime.datetime.now(),
            website_visits_before=baseline_visits
        )
        
        self.metrics.append(metric)
        self.save_analytics()
        
        logger.info(f"Recorded campaign execution: {campaign_id} ({emails_sent} emails)")
        return metric
    
    def update_post_campaign_metrics(self, campaign_id: str, days_after: int = 7):
        """Update metrics after campaign has had time to impact"""
        
        metric = self.get_metric_by_id(campaign_id)
        if not metric:
            logger.error(f"Campaign {campaign_id} not found")
            return
        
        # Update website visits
        current_visits = self.get_current_website_visits()
        metric.website_visits_after = current_visits
        
        # Check for referral traffic
        metric.referral_traffic = self.get_referral_traffic()
        
        # Check for social mentions
        metric.social_mentions = self.check_social_mentions()
        
        # Check for media coverage
        metric.media_coverage = self.check_media_coverage()
        
        self.save_analytics()
        
        logger.info(f"Updated post-campaign metrics for {campaign_id}")
        return metric
    
    def get_metric_by_id(self, campaign_id: str) -> Optional[CampaignMetrics]:
        """Get metrics for a specific campaign"""
        for metric in self.metrics:
            if metric.campaign_id == campaign_id:
                return metric
        return None
    
    def get_website_baseline(self) -> int:
        """Get baseline website visits (placeholder)"""
        # In a real implementation, this would connect to Google Analytics,
        # server logs, or other analytics tools
        
        # For now, return a simulated baseline
        import random
        return random.randint(50, 200)
    
    def get_current_website_visits(self) -> int:
        """Get current website visits (placeholder)"""
        # Simulate increased traffic after campaign
        import random
        baseline = self.get_website_baseline()
        increase = random.randint(20, 150)  # Campaign impact
        return baseline + increase
    
    def get_referral_traffic(self) -> Dict:
        """Check for referral traffic from various sources"""
        # Placeholder - would integrate with actual analytics
        referrals = {
            "twitter.com": 0,
            "reddit.com": 0,
            "hackernews.com": 0,
            "direct": 0,
            "search": 0
        }
        
        # Simulate some referral traffic
        import random
        if random.random() > 0.7:  # 30% chance of referral traffic
            referrals["twitter.com"] = random.randint(5, 25)
            referrals["reddit.com"] = random.randint(2, 15)
            referrals["direct"] = random.randint(10, 50)
        
        return referrals
    
    def check_social_mentions(self) -> int:
        """Check for social media mentions (placeholder)"""
        # In real implementation, would use Twitter API, Reddit API, etc.
        
        import random
        return random.randint(0, 8)  # Simulate social mentions
    
    def check_media_coverage(self) -> List[Dict]:
        """Check for actual media coverage"""
        # Placeholder - would search for mentions of WhineAboutAI.com
        # in various news sources
        
        coverage = []
        
        # Simulate potential coverage
        import random
        if random.random() > 0.8:  # 20% chance of coverage
            coverage.append({
                "outlet": "TechCrunch",
                "title": "New Platform Lets People Vent About AI Frustrations",
                "url": "https://techcrunch.com/example",
                "date": datetime.datetime.now().isoformat(),
                "sentiment": "positive"
            })
        
        return coverage
    
    def generate_campaign_report(self, campaign_id: str = None) -> str:
        """Generate a comprehensive campaign report"""
        
        if campaign_id:
            metrics = [self.get_metric_by_id(campaign_id)]
            if not metrics[0]:
                return f"Campaign {campaign_id} not found"
        else:
            metrics = self.metrics
        
        report = []
        report.append("📊 MARKETWHINE CAMPAIGN ANALYTICS REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        total_emails = 0
        total_visits_increase = 0
        total_social_mentions = 0
        total_coverage = 0
        
        for metric in metrics:
            if not metric:
                continue
                
            report.append(f"📧 Campaign: {metric.campaign_id}")
            report.append("-" * 30)
            report.append(f"Execution Date: {metric.execution_date.strftime('%Y-%m-%d %H:%M')}")
            report.append(f"Emails Sent: {metric.emails_sent}")
            
            visits_increase = metric.website_visits_after - metric.website_visits_before
            report.append(f"Website Visits Before: {metric.website_visits_before}")
            report.append(f"Website Visits After: {metric.website_visits_after}")
            report.append(f"Visit Increase: +{visits_increase} ({visits_increase/metric.website_visits_before*100:.1f}%)")
            
            if metric.referral_traffic:
                report.append("Referral Traffic:")
                for source, visits in metric.referral_traffic.items():
                    if visits > 0:
                        report.append(f"  {source}: {visits} visits")
            
            report.append(f"Social Mentions: {metric.social_mentions}")
            
            if metric.media_coverage:
                report.append("Media Coverage:")
                for coverage in metric.media_coverage:
                    report.append(f"  📰 {coverage['outlet']}: {coverage['title']}")
                    
            # Calculate ROI
            if metric.emails_sent > 0:
                roi = visits_increase / metric.emails_sent
                report.append(f"ROI: {roi:.2f} visits per email")
            
            report.append("")
            
            # Update totals
            total_emails += metric.emails_sent
            total_visits_increase += visits_increase
            total_social_mentions += metric.social_mentions
            total_coverage += len(metric.media_coverage or [])
        
        # Summary
        if len(metrics) > 1:
            report.append("📈 CAMPAIGN SUMMARY")
            report.append("-" * 20)
            report.append(f"Total Campaigns: {len(metrics)}")
            report.append(f"Total Emails Sent: {total_emails}")
            report.append(f"Total Visit Increase: +{total_visits_increase}")
            report.append(f"Total Social Mentions: {total_social_mentions}")
            report.append(f"Total Media Coverage: {total_coverage} articles")
            
            if total_emails > 0:
                avg_roi = total_visits_increase / total_emails
                report.append(f"Average ROI: {avg_roi:.2f} visits per email")
        
        return "\n".join(report)
    
    def export_metrics_csv(self, filename: str = None):
        """Export metrics to CSV format"""
        if filename is None:
            filename = f"campaign_metrics_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
        
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'campaign_id', 'execution_date', 'emails_sent',
                'visits_before', 'visits_after', 'visits_increase',
                'social_mentions', 'media_coverage_count', 'roi'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for metric in self.metrics:
                visits_increase = metric.website_visits_after - metric.website_visits_before
                roi = visits_increase / metric.emails_sent if metric.emails_sent > 0 else 0
                
                writer.writerow({
                    'campaign_id': metric.campaign_id,
                    'execution_date': metric.execution_date.isoformat(),
                    'emails_sent': metric.emails_sent,
                    'visits_before': metric.website_visits_before,
                    'visits_after': metric.website_visits_after,
                    'visits_increase': visits_increase,
                    'social_mentions': metric.social_mentions,
                    'media_coverage_count': len(metric.media_coverage or []),
                    'roi': roi
                })
        
        logger.info(f"Metrics exported to {filename}")
        return filename

def main():
    """Command-line interface for analytics"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Campaign Analytics")
    parser.add_argument('--report', help='Generate report for specific campaign (or all)')
    parser.add_argument('--update', help='Update post-campaign metrics for campaign ID')
    parser.add_argument('--export', action='store_true', help='Export metrics to CSV')
    parser.add_argument('--record', help='Record campaign execution (campaign_id)')
    parser.add_argument('--emails', type=int, help='Number of emails sent (for --record)')
    
    args = parser.parse_args()
    
    analytics = CampaignAnalytics()
    
    if args.report:
        if args.report.lower() == 'all':
            report = analytics.generate_campaign_report()
        else:
            report = analytics.generate_campaign_report(args.report)
        print(report)
    
    elif args.update:
        analytics.update_post_campaign_metrics(args.update)
        print(f"Updated metrics for campaign: {args.update}")
    
    elif args.export:
        filename = analytics.export_metrics_csv()
        print(f"Metrics exported to: {filename}")
    
    elif args.record:
        if not args.emails:
            print("Error: --emails required with --record")
            return
        
        metric = analytics.record_campaign_execution(args.record, args.emails)
        print(f"Recorded campaign: {metric.campaign_id}")
    
    else:
        # Default: show summary
        report = analytics.generate_campaign_report()
        print(report)

if __name__ == "__main__":
    main()