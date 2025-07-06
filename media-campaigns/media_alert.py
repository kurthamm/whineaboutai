#!/usr/bin/env python3
"""
Media Alert Application for WhineAboutAI.com
Sends email alerts to media contacts about new content or announcements
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import List, Dict, Optional
import os
import random
import time
from anonymous_email import AnonymousEmailSender, TorEmailSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('media_alert.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MediaAlertSender:
    """Handles sending email alerts to media contacts"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587, anonymous_mode: bool = False):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.contacts_file = 'media_contacts.json'
        self.anonymous_mode = anonymous_mode
        self.anonymous_sender = AnonymousEmailSender() if anonymous_mode else None
        self.tor_sender = None
        self.anonymous_config = self.load_anonymous_config() if anonymous_mode else None
        
    def load_contacts(self) -> List[Dict]:
        """Load media contacts from JSON file"""
        try:
            with open(self.contacts_file, 'r') as f:
                data = json.load(f)
                return data.get('media_contacts', [])
        except FileNotFoundError:
            logger.error(f"Contacts file {self.contacts_file} not found")
            return []
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {self.contacts_file}")
            return []
    
    def load_anonymous_config(self) -> Dict:
        """Load anonymous email configuration"""
        try:
            with open('anonymous_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Anonymous config file not found")
            return {}
        except json.JSONDecodeError:
            logger.error("Invalid JSON in anonymous config")
            return {}
    
    def create_email_templates(self) -> Dict[str, str]:
        """Create email templates for different types of alerts"""
        templates = {
            'new_feature': {
                'subject': "New AI Humor Platform: WhineAboutAI.com - Perfect for Your Tech Coverage",
                'body': """Hi {name},

I hope this email finds you well. I'm reaching out because I believe you'll find this relevant for your {beat} coverage.

I've launched WhineAboutAI.com, a satirical platform where people can submit their amusing complaints about AI and technology mishaps. It's become a fun outlet for tech frustrations, featuring everything from smart toasters with attitude to AI that recommends kale when you want pizza.

The site includes:
• A complaint submission form with witty AI-generated responses
• Real-time tracking of daily complaints and "tissue counts"
• Humorous ads for "emotional tech support"
• A growing collection of relatable AI fails

Given your coverage of {beat}, I thought this might make for an interesting piece about how people are coping with AI integration through humor. It's a lighthearted take on the very real frustrations many experience with emerging technology.

The site is gaining traction and could be a good fit for a feature story about tech culture or AI adoption challenges. I'd be happy to provide additional context, user statistics, or connect you with some of our most creative complainers.

Best regards,
Kurt Hamm
WhineAboutAI.com
kurt@hamm.me

P.S. Feel free to submit your own AI complaint while you're there - it's quite therapeutic!"""
            },
            'site_update': {
                'subject': "WhineAboutAI.com Update: New Features & Growing Community",
                'body': """Hi {name},

Following up on WhineAboutAI.com, I wanted to share some exciting developments that might interest your readers:

• The site has received over [X] complaints about AI mishaps
• New features include [specific updates]
• Growing community engagement with [statistics]

This continued growth in AI-related frustrations might be worth covering, especially given your focus on {beat}.

Happy to discuss further or provide additional data.

Best,
Kurt Hamm
WhineAboutAI.com
kurt@hamm.me"""
            },
            'announcement': {
                'subject': "Media Alert: WhineAboutAI.com - Tech Humor Platform Launch",
                'body': """Hi {name},

Quick heads up about a new tech humor platform that launched: WhineAboutAI.com

It's a satirical site where people submit complaints about AI and smart technology failures. Could be interesting for your {beat} coverage.

Key details:
• Interactive complaint submission with AI-generated responses
• Growing collection of relatable tech frustrations
• Humorous take on AI adoption challenges

Let me know if you'd like more information.

Best,
Kurt Hamm
WhineAboutAI.com
kurt@hamm.me"""
            }
        }
        return templates
    
    def send_alert(self, template_type: str, recipient_contacts: Optional[List[str]] = None, 
                   custom_subject: Optional[str] = None, custom_body: Optional[str] = None) -> bool:
        """Send email alert to specified contacts or all contacts"""
        
        if self.anonymous_mode:
            return self.send_anonymous_alert(template_type, recipient_contacts, custom_subject, custom_body)
        
        if not self.sender_email or not self.sender_password:
            logger.error("Email credentials not configured. Set SENDER_EMAIL and SENDER_PASSWORD environment variables.")
            return False
        
        contacts = self.load_contacts()
        if not contacts:
            logger.error("No contacts loaded")
            return False
        
        templates = self.create_email_templates()
        
        if template_type not in templates and not (custom_subject and custom_body):
            logger.error(f"Invalid template type: {template_type}")
            return False
        
        template = templates.get(template_type, {})
        subject = custom_subject or template.get('subject', 'WhineAboutAI.com Update')
        body_template = custom_body or template.get('body', '')
        
        sent_count = 0
        failed_count = 0
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            for outlet in contacts:
                outlet_name = outlet.get('outlet', 'Unknown')
                
                for contact in outlet.get('contacts', []):
                    email = contact.get('email')
                    name = contact.get('name', 'there')
                    beat = contact.get('beat', 'technology')
                    
                    if not email:
                        continue
                    
                    # Skip if specific recipients specified and this email not in list
                    if recipient_contacts and email not in recipient_contacts:
                        continue
                    
                    try:
                        # Create personalized message
                        msg = MIMEMultipart()
                        msg['From'] = self.sender_email
                        msg['To'] = email
                        msg['Subject'] = subject
                        
                        # Personalize body
                        personalized_body = body_template.format(
                            name=name,
                            beat=beat,
                            outlet=outlet_name
                        )
                        
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        # Send email
                        server.send_message(msg)
                        sent_count += 1
                        logger.info(f"Email sent to {name} at {outlet_name} ({email})")
                        
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Failed to send email to {email}: {str(e)}")
            
            server.quit()
            
        except Exception as e:
            logger.error(f"SMTP connection failed: {str(e)}")
            return False
        
        logger.info(f"Email campaign completed. Sent: {sent_count}, Failed: {failed_count}")
        return sent_count > 0
    
    def send_anonymous_alert(self, template_type: str, recipient_contacts: Optional[List[str]] = None, 
                            custom_subject: Optional[str] = None, custom_body: Optional[str] = None) -> bool:
        """Send anonymous email alert to specified contacts"""
        
        if not self.anonymous_sender:
            logger.error("Anonymous sender not initialized")
            return False
        
        contacts = self.load_contacts()
        if not contacts:
            logger.error("No contacts loaded")
            return False
        
        # Get sender profile
        sender_profile = random.choice(self.anonymous_config.get('sender_profiles', [
            {'from_name': 'Anonymous Tipster', 'signature': 'Sent anonymously'}
        ]))
        
        # Create anonymous-specific templates
        templates = self.create_anonymous_templates()
        
        if template_type not in templates and not (custom_subject and custom_body):
            logger.error(f"Invalid template type: {template_type}")
            return False
        
        template = templates.get(template_type, {})
        subject = custom_subject or template.get('subject', 'Anonymous Tip: WhineAboutAI.com')
        body_template = custom_body or template.get('body', '')
        
        sent_count = 0
        failed_count = 0
        
        security_config = self.anonymous_config.get('security', {})
        delay = security_config.get('delay_between_sends', 30)
        
        for outlet in contacts:
            outlet_name = outlet.get('outlet', 'Unknown')
            
            for contact in outlet.get('contacts', []):
                email = contact.get('email')
                name = contact.get('name', 'there')
                beat = contact.get('beat', 'technology')
                
                if not email:
                    continue
                
                # Skip if specific recipients specified and this email not in list
                if recipient_contacts and email not in recipient_contacts:
                    continue
                
                try:
                    # Personalize body with anonymous template
                    personalized_body = self.create_anonymous_body(
                        body_template, name, beat, outlet_name, sender_profile
                    )
                    
                    # Send anonymous email
                    success = self.anonymous_sender.send_anonymous_email(
                        email, subject, personalized_body, from_name=sender_profile['from_name']
                    )
                    
                    if success:
                        sent_count += 1
                        logger.info(f"Anonymous email sent to {name} at {outlet_name} ({email})")
                    else:
                        failed_count += 1
                        logger.error(f"Failed to send anonymous email to {email}")
                    
                    # Add delay between sends for security
                    if delay > 0:
                        time.sleep(delay + random.randint(0, 10))
                        
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send anonymous email to {email}: {str(e)}")
        
        logger.info(f"Anonymous email campaign completed. Sent: {sent_count}, Failed: {failed_count}")
        return sent_count > 0
    
    def create_anonymous_templates(self) -> Dict[str, Dict]:
        """Create email templates for anonymous alerts"""
        templates = {
            'new_feature': {
                'subject': 'Anonymous Tip: New AI Humor Platform Worth Covering',
                'body': 'anonymous_new_feature'
            },
            'site_update': {
                'subject': 'Anonymous Update: WhineAboutAI.com Growing Community',
                'body': 'anonymous_site_update'
            },
            'announcement': {
                'subject': 'Anonymous Tip: AI Humor Platform Launch',
                'body': 'anonymous_announcement'
            },
            'whistleblower': {
                'subject': 'Confidential Tip: Tech Industry Insights',
                'body': 'whistleblower_template'
            },
            'viral_story': {
                'subject': '🚨 EXCLUSIVE: The AI Complaint Platform Everyone\'s Talking About',
                'body': 'viral_story_template'
            }
        }
        return templates
    
    def create_anonymous_body(self, template_key: str, name: str, beat: str, 
                             outlet: str, sender_profile: Dict) -> str:
        """Create personalized anonymous email body"""
        
        anonymous_bodies = {
            'anonymous_new_feature': f"""Hi {name},

I'm writing anonymously to share information about a new platform that might interest your {beat} coverage.

WhineAboutAI.com has launched as a satirical outlet where people submit complaints about AI and technology failures. It's gaining traction as a humorous way to process frustrations with AI integration.

Key features:
• Interactive complaint submission with AI-generated responses
• Growing collection of relatable tech fails
• Community-driven content about AI adoption challenges
• Humorous take on serious technology issues

Given your coverage of {beat}, this could make for an interesting piece about how people are coping with AI through humor. The platform is seeing steady growth and user engagement.

I believe this story would resonate with your readers at {outlet}. The site is at whineaboutai.com if you'd like to investigate further.

{sender_profile.get('signature', 'Sent anonymously')}""",
            
            'anonymous_site_update': f"""Hi {name},

Following up on WhineAboutAI.com, there have been some notable developments that might warrant coverage:

• Significant increase in user-submitted AI complaints
• New features added based on community feedback
• Growing discussion around AI frustrations in mainstream media
• Platform becoming a reference point for AI adoption challenges

This continued growth might be worth covering for your {beat} audience at {outlet}.

{sender_profile.get('signature', 'Sent anonymously')}""",
            
            'anonymous_announcement': f"""Hi {name},

Quick anonymous tip: WhineAboutAI.com is a new satirical platform for AI complaints that might interest your {beat} readers.

Worth checking out for a potential story about tech culture and AI adoption.

{sender_profile.get('signature', 'Sent anonymously')}""",

            'viral_story_template': f"""Hi {name},

I'm reaching out with what could be a viral story for {outlet}'s {beat} coverage.

🎯 **THE STORY**: WhineAboutAI.com is becoming the internet's therapy couch for AI frustrations

**Why this is PERFECT for your readers:**
• 📈 Explosive growth: Thousands of hilarious AI complaint submissions daily
• 🤖 Captures the zeitgeist: Real people venting about AI gone wrong
• 😂 Viral content goldmine: "My smart fridge is judging my midnight snacks"
• 📱 Social media buzz: Screenshots going viral on Twitter/TikTok
• 🎭 Cultural phenomenon: How humor helps us cope with tech anxiety

**The Hook**: It's like Yelp for AI failures, but infinitely funnier.

**Real complaints from the site:**
→ "ChatGPT recommended I break up with my girlfriend based on my grocery list"
→ "My Tesla tried to drive me to my ex's house during a software update"
→ "Alexa started playing funeral music when I asked about my retirement savings"

**Why NOW?** 
- AI adoption anxiety is peaking
- People need humor to process tech overwhelm  
- Perfect timing with current AI discourse
- Ready-made viral content for social platforms

**Exclusive angles for {outlet}:**
✨ Tech culture commentary piece
✨ Data story: Most complained-about AI features  
✨ Human interest: How humor helps tech adoption
✨ Investigation: What AI complaints reveal about UX failures

This is the kind of story that gets shared, quoted, and drives serious traffic. The site is at whineaboutai.com - worth 5 minutes to see if it fits your editorial calendar.

Happy to provide more context, user stats, or connect you with the most entertaining complainers.

{sender_profile.get('signature', 'Sent anonymously')}

P.S. Try submitting your own AI complaint while you're there. It's surprisingly therapeutic! 😄""",
        }
        
        return anonymous_bodies.get(template_key, f"Anonymous tip about WhineAboutAI.com for your {beat} coverage.")
    
    def list_contacts(self) -> None:
        """List all available contacts"""
        contacts = self.load_contacts()
        
        print("Available Media Contacts:")
        print("=" * 50)
        
        for outlet in contacts:
            outlet_name = outlet.get('outlet', 'Unknown')
            print(f"\n{outlet_name}:")
            
            for contact in outlet.get('contacts', []):
                name = contact.get('name', 'N/A')
                role = contact.get('role', 'N/A')
                email = contact.get('email', 'N/A')
                beat = contact.get('beat', 'N/A')
                
                print(f"  • {name} ({role})")
                print(f"    Email: {email}")
                print(f"    Beat: {beat}")
        
        print(f"\nTotal contacts: {sum(len(outlet.get('contacts', [])) for outlet in contacts)}")

def test_anonymous_email():
    """Test anonymous email functionality"""
    print("Testing Anonymous Email Delivery System")
    print("=" * 50)
    
    # Test basic anonymous sender
    anon_sender = AnonymousEmailSender()
    
    test_email = "test@example.com"
    test_subject = "Test Anonymous Email"
    test_body = "This is a test of the anonymous email system."
    
    print(f"Testing anonymous email to: {test_email}")
    success = anon_sender.send_anonymous_email(test_email, test_subject, test_body)
    
    if success:
        print("✓ Anonymous email test successful")
    else:
        print("✗ Anonymous email test failed")
    
    # Test Tor sender
    print("\nTesting Tor Email Delivery...")
    tor_sender = TorEmailSender()
    
    if tor_sender.check_tor_connection():
        print("✓ Tor connection available")
        tor_success = tor_sender.send_via_tor(test_email, test_subject, test_body)
        if tor_success:
            print("✓ Tor email test successful")
        else:
            print("✗ Tor email test failed")
    else:
        print("! Tor not available (install and run Tor to enable)")
    
    # Test configuration loading
    print("\nTesting Configuration...")
    sender = MediaAlertSender(anonymous_mode=True)
    config = sender.anonymous_config
    
    if config:
        print(f"✓ Configuration loaded: {len(config.get('sender_profiles', []))} sender profiles")
        print(f"✓ Security settings: {config.get('security', {}).get('delay_between_sends', 0)}s delay")
    else:
        print("✗ Configuration loading failed")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Send media alerts for WhineAboutAI.com")
    parser.add_argument('--template', choices=['new_feature', 'site_update', 'announcement', 'whistleblower', 'viral_story'], 
                       default='new_feature', help='Email template to use')
    parser.add_argument('--list-contacts', action='store_true', help='List all contacts')
    parser.add_argument('--emails', nargs='+', help='Specific email addresses to send to')
    parser.add_argument('--subject', help='Custom email subject')
    parser.add_argument('--body', help='Custom email body')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be sent without sending')
    parser.add_argument('--anonymous', action='store_true', help='Send emails anonymously')
    parser.add_argument('--tor', action='store_true', help='Use Tor for anonymous sending (requires Tor)')
    parser.add_argument('--test-anonymous', action='store_true', help='Test anonymous email functionality')
    
    args = parser.parse_args()
    
    # Initialize sender with anonymous mode if requested
    anonymous_mode = args.anonymous or args.tor
    sender = MediaAlertSender(anonymous_mode=anonymous_mode)
    
    # Test anonymous functionality
    if args.test_anonymous:
        print("Testing anonymous email functionality...")
        test_anonymous_email()
        return
    
    if args.list_contacts:
        sender.list_contacts()
        return
    
    if args.dry_run:
        print("DRY RUN MODE - No emails will be sent")
        contacts = sender.load_contacts()
        
        if anonymous_mode:
            templates = sender.create_anonymous_templates()
            print("Mode: ANONYMOUS")
        else:
            templates = sender.create_email_templates()
            print("Mode: STANDARD")
        
        template = templates.get(args.template, {})
        
        print(f"Template: {args.template}")
        print(f"Subject: {args.subject or template.get('subject', 'N/A')}")
        print(f"Recipients: {len([c for outlet in contacts for c in outlet.get('contacts', [])])}")
        
        if anonymous_mode:
            print("Anonymous features:")
            print(f"  - Random sender profiles: {len(sender.anonymous_config.get('sender_profiles', []))}")
            print(f"  - Delay between sends: {sender.anonymous_config.get('security', {}).get('delay_between_sends', 0)}s")
            
        return
    
    # Send emails
    success = sender.send_alert(
        template_type=args.template,
        recipient_contacts=args.emails,
        custom_subject=args.subject,
        custom_body=args.body
    )
    
    if success:
        if anonymous_mode:
            print("Anonymous media alerts sent successfully!")
        else:
            print("Media alerts sent successfully!")
    else:
        if anonymous_mode:
            print("Failed to send anonymous media alerts. Check logs for details.")
        else:
            print("Failed to send media alerts. Check logs for details.")

if __name__ == "__main__":
    main()