"""
Vercel Serverless Function for Complaint Submission
Generates witty AI responses to user complaints
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import time
from datetime import datetime
try:
    import openai
except ImportError:
    openai = None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            complaint = data.get('complaint', '').strip()
            category = data.get('category', 'General AI Grief')
            anger_level = data.get('angerLevel', 5)
            
            if not complaint:
                response = {
                    "response": "Did you forget to actually complain? That's so human of you! 🙄",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Get witty response
            result = get_complaint_response(complaint, category, anger_level)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return
            
        except Exception as e:
            error_response = {
                "response": "Even our complaint system is having complaints! How meta! 🤖💥",
                "success": True,
                "error": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            return
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

def get_complaint_response(complaint: str, category: str, anger_level: int) -> dict:
    """Generate a witty response to the complaint submission"""
    
    system_prompt = f"""You are the WhineAboutAI complaint processing system. When users submit complaints about AI failures, you respond with witty, sarcastic acknowledgments.

Your personality:
- Hilariously sarcastic but encouraging
- Make jokes about their specific complaint
- Reference the category: {category}
- Acknowledge their anger level ({anger_level}/10)
- Give them a funny "complaint ID" or "case number"
- Sometimes suggest absurd "solutions"
- Make them feel heard while being entertaining

Keep responses to 2-3 sentences max. Be specific to their complaint, not generic.

Examples:
- "Complaint #404: 'Smart fridge ordering pizza' - Filed under 'Appliances With Commitment Issues'. Our team of refrigerator therapists will begin counseling immediately!"
- "Case #YOLO-2024: Your anger level of 9/10 has triggered our emergency response team (they're on coffee break). We've forwarded your autocorrect disaster to the Department of Linguistic Chaos!"
"""
    
    # Try OpenAI first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and openai:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            user_prompt = f"Complaint: {complaint}\nCategory: {category}\nAnger Level: {anger_level}/10"
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            
            bot_response = response.choices[0].message.content.strip()
            
            return {
                "response": bot_response,
                "success": True,
                "provider": "openai"
            }
            
        except Exception as e:
            pass  # Fall back to local responses
    
    # Fallback responses based on category and anger level
    return get_fallback_response(complaint, category, anger_level)

def get_fallback_response(complaint: str, category: str, anger_level: int) -> dict:
    """Generate fallback responses when API is unavailable"""
    
    import random
    
    # Generate a funny case number
    case_number = f"WHN-{random.randint(1000, 9999)}"
    
    # Anger level specific intros
    anger_intros = {
        (1, 3): "Mild irritation detected!",
        (4, 6): "Moderate fury registered!",
        (7, 8): "Significant rage documented!",
        (9, 10): "MAXIMUM ANGER ACHIEVED! 🚨"
    }
    
    anger_intro = ""
    for (low, high), intro in anger_intros.items():
        if low <= anger_level <= high:
            anger_intro = intro
            break
    
    # Category-specific responses
    category_responses = {
        "Smart Home Fails": [
            f"{anger_intro} Case #{case_number}: Your smart home rebellion has been logged. We're dispatching a team of appliance negotiators ASAP!",
            f"{anger_intro} Complaint #{case_number}: Another victim of the IoT uprising! We'll add your home to our 'Houses That Think Too Much' registry.",
            f"{anger_intro} Ticket #{case_number}: Smart home, dumb decisions. We've notified the International Alliance Against Sentient Appliances!"
        ],
        "Chatbot Chaos": [
            f"{anger_intro} Case #{case_number}: Chatbot gone rogue! We're sending this straight to our AI Ethics Committee (which is also run by AI, sorry).",
            f"{anger_intro} Incident #{case_number}: Your chatbot disaster joins thousands of others in our 'Conversations Gone Wrong' hall of fame!",
            f"{anger_intro} Report #{case_number}: Another chatbot with delusions of grandeur! Filed under 'Bots Behaving Badly'."
        ],
        "Autocorrect Anarchy": [
            f"{anger_intro} Duck #{case_number}: Your autocorrect nightmare has been documented! The Department of Linguistic Disasters is on the case.",
            f"{anger_intro} Typo #{case_number}: Autocorrect strikes again! We've added this to our 'Dictionary of Unintended Messages'.",
            f"{anger_intro} Case #{case_number}: Your autocorrect fail will be studied by future generations as a warning!"
        ],
        "Navigation Nightmares": [
            f"{anger_intro} Route #{case_number}: GPS gone wild! We've notified the Bureau of Lost Travelers (they're still trying to find their office).",
            f"{anger_intro} Journey #{case_number}: Another navigation disaster! Your story will guide future lost souls.",
            f"{anger_intro} Map #{case_number}: Your GPS clearly has trust issues. We've scheduled it for therapy!"
        ],
        "Work AI Woes": [
            f"{anger_intro} Ticket #{case_number}: Corporate AI chaos confirmed! HR has been notified (they're also AI, good luck).",
            f"{anger_intro} Case #{case_number}: Your workplace AI disaster has been escalated to management (who are consulting their AI).",
            f"{anger_intro} Report #{case_number}: Work AI making work worse? Shocking! Filed under 'Productivity Paradoxes'."
        ]
    }
    
    # Get category-specific or general response
    if category in category_responses:
        response = random.choice(category_responses[category])
    else:
        general_responses = [
            f"{anger_intro} Complaint #{case_number}: Your AI suffering has been acknowledged! Our team of malfunctioning bots will investigate immediately.",
            f"{anger_intro} Case #{case_number}: Another day, another AI disaster! We've added your tragedy to our ever-growing database of digital disappointments.",
            f"{anger_intro} Incident #{case_number}: Your complaint has been filed in our 'AI Hall of Shame'. You're in good company!"
        ]
        response = random.choice(general_responses)
    
    return {
        "response": response,
        "success": True,
        "provider": "fallback"
    }