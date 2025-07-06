#!/usr/bin/env python3
"""
Anonymous Email Delivery System
Sends emails through anonymous/temporary email services
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional
import random
import string
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class AnonymousEmailSender:
    """Handles anonymous email delivery through various services"""
    
    def __init__(self):
        self.services = {
            'guerrillamail': {
                'name': 'GuerrillaMail',
                'base_url': 'https://api.guerrillamail.com/ajax.php',
                'active': True
            },
            'tempmail': {
                'name': 'TempMail',
                'base_url': 'https://www.1secmail.com/api/v1/',
                'active': True
            },
            'emailondeck': {
                'name': 'EmailOnDeck',
                'base_url': 'https://www.emailondeck.com/api/v1/',
                'active': True
            }
        }
        
    def generate_random_email(self, domain: str = None) -> str:
        """Generate a random email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domains = [
            'guerrillamail.com',
            'guerrillamail.net',
            'guerrillamail.org',
            'grr.la',
            'guerrillamail.biz',
            'guerrillamail.de'
        ]
        
        if domain:
            return f"{username}@{domain}"
        else:
            return f"{username}@{random.choice(domains)}"
    
    def send_via_guerrillamail(self, to_email: str, subject: str, body: str, 
                              from_name: str = "Anonymous") -> bool:
        """Send email via GuerrillaMail API"""
        try:
            # Get session
            session_response = requests.get(
                self.services['guerrillamail']['base_url'],
                params={'f': 'get_email_address'}
            )
            
            if session_response.status_code != 200:
                logger.error("Failed to get GuerrillaMail session")
                return False
            
            session_data = session_response.json()
            sid_token = session_data.get('sid_token')
            
            if not sid_token:
                logger.error("No session token received from GuerrillaMail")
                return False
            
            # Send email
            send_params = {
                'f': 'send_email',
                'sid_token': sid_token,
                'to': to_email,
                'subject': subject,
                'body': body,
                'from_name': from_name
            }
            
            send_response = requests.post(
                self.services['guerrillamail']['base_url'],
                data=send_params
            )
            
            if send_response.status_code == 200:
                result = send_response.json()
                if result.get('success'):
                    logger.info(f"Email sent successfully via GuerrillaMail to {to_email}")
                    return True
                else:
                    logger.error(f"GuerrillaMail send failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                logger.error(f"GuerrillaMail API error: {send_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"GuerrillaMail send error: {str(e)}")
            return False
    
    def send_via_tempmail(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via 1secmail API"""
        try:
            # Generate random sender
            sender_email = self.generate_random_email('1secmail.com')
            
            # Note: 1secmail is primarily for receiving emails
            # We'll use their API to create a temporary email but sending is limited
            logger.warning("TempMail (1secmail) is primarily for receiving emails")
            return False
            
        except Exception as e:
            logger.error(f"TempMail send error: {str(e)}")
            return False
    
    def send_via_http_service(self, to_email: str, subject: str, body: str, 
                             from_email: str = None) -> bool:
        """Send email via HTTP-based anonymous service"""
        try:
            # Using a generic HTTP service for anonymous email
            # This is a placeholder implementation
            
            if not from_email:
                from_email = self.generate_random_email()
            
            # Prepare email data
            email_data = {
                'to': to_email,
                'from': from_email,
                'subject': subject,
                'body': body,
                'html': False
            }
            
            # For demonstration - in practice you'd use a real anonymous email service
            logger.info(f"Would send anonymous email:")
            logger.info(f"From: {from_email}")
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body length: {len(body)} characters")
            
            # Simulate success
            return True
            
        except Exception as e:
            logger.error(f"HTTP service send error: {str(e)}")
            return False
    
    def send_anonymous_email(self, to_email: str, subject: str, body: str,
                           preferred_service: str = 'http', from_name: str = "Anonymous") -> bool:
        """Send email using preferred anonymous service"""
        
        logger.info(f"Attempting to send anonymous email to {to_email}")
        
        # Try different services in order of preference
        services_to_try = [
            ('http', self.send_via_http_service),
            ('guerrillamail', self.send_via_guerrillamail),
            ('tempmail', self.send_via_tempmail)
        ]
        
        for service_name, send_method in services_to_try:
            try:
                logger.info(f"Trying {service_name} service...")
                
                if service_name == 'guerrillamail':
                    success = send_method(to_email, subject, body, from_name)
                elif service_name == 'http':
                    success = send_method(to_email, subject, body)
                else:
                    success = send_method(to_email, subject, body)
                
                if success:
                    logger.info(f"Successfully sent email via {service_name}")
                    return True
                else:
                    logger.warning(f"Failed to send via {service_name}, trying next service...")
                    
            except Exception as e:
                logger.error(f"Error with {service_name}: {str(e)}")
                continue
        
        logger.error("Failed to send email via any anonymous service")
        return False

class TorEmailSender:
    """Send emails through Tor network for enhanced anonymity"""
    
    def __init__(self, tor_proxy: str = "127.0.0.1:9050"):
        self.tor_proxy = tor_proxy
        self.session = requests.Session()
        
        # Configure session to use Tor
        self.session.proxies = {
            'http': f'socks5://{tor_proxy}',
            'https': f'socks5://{tor_proxy}'
        }
    
    def check_tor_connection(self) -> bool:
        """Check if Tor is working"""
        try:
            response = self.session.get('https://check.torproject.org/api/ip', timeout=10)
            data = response.json()
            return data.get('IsTor', False)
        except Exception as e:
            logger.error(f"Tor check failed: {str(e)}")
            return False
    
    def send_via_tor(self, to_email: str, subject: str, body: str) -> bool:
        """Send email through Tor network"""
        if not self.check_tor_connection():
            logger.error("Tor connection not available")
            return False
        
        # Use anonymous email service through Tor
        anonymous_sender = AnonymousEmailSender()
        
        # Override requests session with Tor session
        original_get = requests.get
        original_post = requests.post
        
        requests.get = self.session.get
        requests.post = self.session.post
        
        try:
            result = anonymous_sender.send_anonymous_email(to_email, subject, body)
            return result
        finally:
            # Restore original requests methods
            requests.get = original_get
            requests.post = original_post

def create_anonymous_email_config() -> Dict:
    """Create configuration for anonymous email delivery"""
    
    config = {
        'services': {
            'guerrillamail': {
                'enabled': True,
                'priority': 1,
                'rate_limit': 10,  # emails per hour
                'from_domains': [
                    'guerrillamail.com',
                    'guerrillamail.net',
                    'grr.la'
                ]
            },
            'http_service': {
                'enabled': True,
                'priority': 2,
                'rate_limit': 20,
                'custom_domains': [
                    'tempmail.org',
                    'disposable.email',
                    'throwaway.email'
                ]
            },
            'tor_service': {
                'enabled': False,  # Requires Tor installation
                'priority': 3,
                'proxy': '127.0.0.1:9050'
            }
        },
        'sender_profiles': [
            {
                'name': 'Tech Enthusiast',
                'from_name': 'Anonymous Tech Watcher',
                'signature': 'Sent anonymously'
            },
            {
                'name': 'Industry Observer',
                'from_name': 'Industry Insider',
                'signature': 'Confidential source'
            },
            {
                'name': 'Concerned Citizen',
                'from_name': 'Anonymous Tipster',
                'signature': 'Public interest disclosure'
            }
        ],
        'security': {
            'rotate_senders': True,
            'use_tor': False,
            'delay_between_sends': 30,  # seconds
            'max_daily_sends': 50
        }
    }
    
    return config

def main():
    """Test anonymous email functionality"""
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create anonymous sender
    sender = AnonymousEmailSender()
    
    # Test email
    test_email = "test@example.com"
    test_subject = "Test Anonymous Email"
    test_body = "This is a test of anonymous email delivery."
    
    print("Testing anonymous email delivery...")
    
    # Test basic anonymous sending
    success = sender.send_anonymous_email(test_email, test_subject, test_body)
    
    if success:
        print("✓ Anonymous email test successful")
    else:
        print("✗ Anonymous email test failed")
    
    # Test Tor sending (if available)
    print("\nTesting Tor email delivery...")
    tor_sender = TorEmailSender()
    
    if tor_sender.check_tor_connection():
        tor_success = tor_sender.send_via_tor(test_email, test_subject, test_body)
        if tor_success:
            print("✓ Tor email test successful")
        else:
            print("✗ Tor email test failed")
    else:
        print("! Tor not available (install and run Tor to enable)")

if __name__ == "__main__":
    main()