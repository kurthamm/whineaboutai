#!/usr/bin/env python3
"""
Automated Media Campaign Scheduler
Manages follow-up campaigns and tracks timing
"""

import json
import datetime
import logging
import os
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('campaign_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CampaignType(Enum):
    INITIAL = "initial"
    FOLLOW_UP_1 = "follow_up_1"
    FOLLOW_UP_2 = "follow_up_2"
    QUARTERLY = "quarterly"
    SEASONAL = "seasonal"
    EVENT_DRIVEN = "event_driven"

@dataclass
class Campaign:
    campaign_id: str
    campaign_type: CampaignType
    template: str
    target_groups: List[str]  # ["tech_press", "mainstream", "policy"]
    scheduled_date: datetime.datetime
    executed: bool = False
    results: Dict = None

class CampaignScheduler:
    """Manages and schedules media campaigns"""
    
    def __init__(self, config_file: str = "campaign_schedule.json"):
        self.config_file = config_file
        self.campaigns = []
        self.load_campaigns()
        
    def load_campaigns(self):
        """Load existing campaign schedule"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for campaign_data in data.get('campaigns', []):
                        campaign = Campaign(
                            campaign_id=campaign_data['campaign_id'],
                            campaign_type=CampaignType(campaign_data['campaign_type']),
                            template=campaign_data['template'],
                            target_groups=campaign_data['target_groups'],
                            scheduled_date=datetime.datetime.fromisoformat(campaign_data['scheduled_date']),
                            executed=campaign_data.get('executed', False),
                            results=campaign_data.get('results')
                        )
                        self.campaigns.append(campaign)
        except Exception as e:
            logger.error(f"Error loading campaigns: {e}")
            self.campaigns = []
    
    def save_campaigns(self):
        """Save campaign schedule to file"""
        try:
            data = {
                'campaigns': [],
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            for campaign in self.campaigns:
                campaign_data = {
                    'campaign_id': campaign.campaign_id,
                    'campaign_type': campaign.campaign_type.value,
                    'template': campaign.template,
                    'target_groups': campaign.target_groups,
                    'scheduled_date': campaign.scheduled_date.isoformat(),
                    'executed': campaign.executed,
                    'results': campaign.results
                }
                data['campaigns'].append(campaign_data)
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving campaigns: {e}")
    
    def schedule_initial_follow_ups(self, initial_date: datetime.datetime = None):
        """Schedule the complete follow-up campaign sequence"""
        
        if initial_date is None:
            initial_date = datetime.datetime.now()
        
        # First follow-up: 3 weeks after initial
        follow_up_1 = Campaign(
            campaign_id=f"followup1_{initial_date.strftime('%Y%m%d')}",
            campaign_type=CampaignType.FOLLOW_UP_1,
            template="site_update",
            target_groups=["tech_press", "mainstream"],
            scheduled_date=initial_date + datetime.timedelta(weeks=3)
        )
        
        # Second follow-up: 7 weeks after initial
        follow_up_2 = Campaign(
            campaign_id=f"followup2_{initial_date.strftime('%Y%m%d')}",
            campaign_type=CampaignType.FOLLOW_UP_2,
            template="viral_story",  # Different angle
            target_groups=["policy", "mainstream"],
            scheduled_date=initial_date + datetime.timedelta(weeks=7)
        )
        
        # Quarterly follow-up: 12 weeks after initial
        quarterly = Campaign(
            campaign_id=f"quarterly_{initial_date.strftime('%Y%m%d')}",
            campaign_type=CampaignType.QUARTERLY,
            template="announcement",
            target_groups=["tech_press", "mainstream", "policy"],
            scheduled_date=initial_date + datetime.timedelta(weeks=12)
        )
        
        self.campaigns.extend([follow_up_1, follow_up_2, quarterly])
        self.save_campaigns()
        
        logger.info(f"Scheduled 3 follow-up campaigns starting from {initial_date}")
        return [follow_up_1, follow_up_2, quarterly]
    
    def get_due_campaigns(self, check_date: datetime.datetime = None) -> List[Campaign]:
        """Get campaigns that are due to be executed"""
        if check_date is None:
            check_date = datetime.datetime.now()
        
        due_campaigns = []
        for campaign in self.campaigns:
            if (not campaign.executed and 
                campaign.scheduled_date <= check_date):
                due_campaigns.append(campaign)
        
        return due_campaigns
    
    def execute_campaign(self, campaign: Campaign) -> bool:
        """Execute a specific campaign"""
        try:
            logger.info(f"Executing campaign: {campaign.campaign_id}")
            
            # Determine target emails based on groups
            target_emails = self.get_target_emails(campaign.target_groups)
            
            # Build command
            cmd = [
                'python3', 'media_alert.py',
                '--anonymous',
                '--template', campaign.template,
                '--emails'
            ] + target_emails
            
            # Execute the campaign
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                campaign.executed = True
                campaign.results = {
                    'execution_date': datetime.datetime.now().isoformat(),
                    'targets_count': len(target_emails),
                    'status': 'success',
                    'output': result.stdout
                }
                logger.info(f"Campaign {campaign.campaign_id} executed successfully")
                self.save_campaigns()
                return True
            else:
                logger.error(f"Campaign {campaign.campaign_id} failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing campaign {campaign.campaign_id}: {e}")
            return False
    
    def get_target_emails(self, target_groups: List[str]) -> List[str]:
        """Get email addresses for target groups"""
        
        # Load contacts
        try:
            with open('media_contacts.json', 'r') as f:
                contacts_data = json.load(f)
        except:
            logger.error("Could not load media contacts")
            return []
        
        emails = []
        group_mapping = {
            "tech_press": ["TechCrunch", "The Verge", "Wired", "Ars Technica", "VentureBeat", 
                          "Mashable", "Gizmodo", "Engadget", "MIT Technology Review"],
            "mainstream": ["CNN", "New York Times", "Wall Street Journal", "Washington Post", 
                          "Reuters", "AP News", "NPR"],
            "policy": ["Axios", "Platformer", "The Information"]
        }
        
        for outlet in contacts_data.get('media_contacts', []):
            outlet_name = outlet.get('outlet', '')
            
            for group in target_groups:
                if outlet_name in group_mapping.get(group, []):
                    for contact in outlet.get('contacts', []):
                        email = contact.get('email')
                        if email and email not in emails:
                            emails.append(email)
        
        return emails
    
    def check_and_execute_due_campaigns(self):
        """Check for and execute any due campaigns"""
        due_campaigns = self.get_due_campaigns()
        
        if not due_campaigns:
            logger.info("No campaigns due for execution")
            return 0
        
        executed_count = 0
        for campaign in due_campaigns:
            if self.execute_campaign(campaign):
                executed_count += 1
        
        logger.info(f"Executed {executed_count} of {len(due_campaigns)} due campaigns")
        return executed_count
    
    def list_campaigns(self):
        """List all scheduled campaigns"""
        print("Scheduled Media Campaigns:")
        print("=" * 60)
        
        for campaign in sorted(self.campaigns, key=lambda c: c.scheduled_date):
            status = "✅ EXECUTED" if campaign.executed else "⏳ PENDING"
            print(f"{campaign.campaign_id}")
            print(f"  Type: {campaign.campaign_type.value}")
            print(f"  Template: {campaign.template}")
            print(f"  Scheduled: {campaign.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Groups: {', '.join(campaign.target_groups)}")
            print(f"  Status: {status}")
            if campaign.results:
                print(f"  Results: {campaign.results.get('targets_count', 0)} targets")
            print()
    
    def add_event_driven_campaign(self, template: str, target_groups: List[str], 
                                 execute_date: datetime.datetime, campaign_id: str = None):
        """Add a campaign triggered by external events"""
        
        if campaign_id is None:
            campaign_id = f"event_{execute_date.strftime('%Y%m%d_%H%M')}"
        
        campaign = Campaign(
            campaign_id=campaign_id,
            campaign_type=CampaignType.EVENT_DRIVEN,
            template=template,
            target_groups=target_groups,
            scheduled_date=execute_date
        )
        
        self.campaigns.append(campaign)
        self.save_campaigns()
        
        logger.info(f"Added event-driven campaign: {campaign_id}")
        return campaign

def main():
    """Command-line interface for campaign scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Media Campaign Scheduler")
    parser.add_argument('--check', action='store_true', help='Check and execute due campaigns')
    parser.add_argument('--schedule-followups', action='store_true', help='Schedule initial follow-up campaigns')
    parser.add_argument('--list', action='store_true', help='List all campaigns')
    parser.add_argument('--add-event', help='Add event-driven campaign (template name)')
    parser.add_argument('--groups', nargs='+', default=['tech_press'], help='Target groups for event campaign')
    parser.add_argument('--date', help='Date for event campaign (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    scheduler = CampaignScheduler()
    
    if args.check:
        scheduler.check_and_execute_due_campaigns()
    
    elif args.schedule_followups:
        campaigns = scheduler.schedule_initial_follow_ups()
        print(f"Scheduled {len(campaigns)} follow-up campaigns")
        for campaign in campaigns:
            print(f"  {campaign.campaign_id}: {campaign.scheduled_date.strftime('%Y-%m-%d')}")
    
    elif args.list:
        scheduler.list_campaigns()
    
    elif args.add_event:
        if args.date:
            execute_date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        else:
            execute_date = datetime.datetime.now()
        
        campaign = scheduler.add_event_driven_campaign(
            template=args.add_event,
            target_groups=args.groups,
            execute_date=execute_date
        )
        print(f"Added event campaign: {campaign.campaign_id}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()