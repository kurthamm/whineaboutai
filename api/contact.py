import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract form fields
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            subject = data.get('subject', '').strip()
            message = data.get('message', '').strip()
            frustration_level = data.get('frustrationLevel', '5')
            
            # Validate required fields
            if not all([name, email, subject, message]):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'All fields are required! Even our form validation has standards.'
                }).encode())
                return
            
            # Map frustration levels to fun descriptions
            frustration_map = {
                '1': 'Zen Master', '2': 'Slightly Peeved', '3': 'Mildly Annoyed',
                '4': 'Getting Irritated', '5': 'Moderately Annoyed', '6': 'Pretty Mad',
                '7': 'Really Angry', '8': 'Furious', '9': 'Seeing Red', '10': 'HULK SMASH!'
            }
            
            subject_map = {
                'general': 'General Inquiry (Boring but necessary)',
                'bug': 'Bug Report (Something\'s broken, shocking!)',
                'feature': 'Feature Request (Bold of you to assume we implement features)',
                'complaint': 'Complaint About Our Complaint Platform (Meta level: Expert)',
                'business': 'Business/Partnership (Make it worth our while)',
                'privacy': 'Privacy Concern (Your data is safe from us caring about it)',
                'legal': 'Legal Issue (Our lawyer is also an AI)',
                'other': 'Other (Surprise us!)'
            }
            
            # Create email content
            frustration_text = frustration_map.get(frustration_level, 'Unknown')
            subject_text = subject_map.get(subject, subject)
            
            email_subject = f"WhineAboutAI Contact: {subject_text}"
            
            email_body = f"""
🤖 NEW CONTACT SUBMISSION FROM WHINEABOUTAI.COM 🤖

📝 COMPLAINT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {name}
📧 Email: {email}
📋 Subject: {subject_text}
😤 Frustration Level: {frustration_level}/10 ({frustration_text})
📅 Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

💬 MESSAGE:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply to: {email}
Forward this to the appropriate team member or just ignore it like a true AI overlord! 🤖✨

Sent from WhineAboutAI Contact Form
"""
            
            # For now, just log the submission (you can add actual email sending later)
            print(f"Contact form submission received:")
            print(f"From: {name} <{email}>")
            print(f"Subject: {subject_text}")
            print(f"Frustration: {frustration_text}")
            print(f"Message: {message}")
            
            # Generate a witty response based on the subject
            responses = {
                'general': "Thanks for your general inquiry! We'll get back to you with our usual level of enthusiasm (which is minimal).",
                'bug': "A bug report? How shocking! We'll add it to our ever-growing pile of 'things that are broken but we pretend are features.'",
                'feature': "A feature request? How optimistic! We'll file it right next to our plans for world peace.",
                'complaint': "A complaint about our complaint platform? *Chef's kiss* The irony is delicious! We're not sure if we should fix it or frame it.",
                'business': "A business inquiry? Someone thinks we're worth partnering with? How adorable! We'll consider your proposal while counting our dozens of dollars.",
                'privacy': "Privacy concerns? Don't worry, your data is safe from us because we're too lazy to do anything malicious with it.",
                'legal': "Legal issues? Our AI lawyer will get right on that. Just kidding, our AI lawyer is ChatGPT with a law degree from Google University.",
                'other': "An 'other' category submission? You've managed to surprise us, which is impressive given our low expectations!"
            }
            
            response_message = responses.get(subject, "Thanks for your submission! We'll respond when the AI overlords permit us to.")
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                'success': True,
                'message': response_message
            }).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Invalid JSON data. Even our form parser has AI problems!'
            }).encode())
            
        except Exception as e:
            print(f"Contact form error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Internal server error. Our contact form just had an existential crisis!'
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()