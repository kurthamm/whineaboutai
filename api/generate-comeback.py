"""
Vercel Serverless Function for Comeback Generation
Generates perfect comebacks for AI failures
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import random
from datetime import datetime
import openai

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
            
            if not complaint:
                response = {
                    "error": "Complaint is required",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Generate comeback
            result = generate_comeback(complaint)
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {
                "complaint": data.get('complaint', ''),
                "comeback": "I'd give you a comeback, but my AI is too busy being the thing you're complaining about!",
                "success": False,
                "error": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def generate_comeback(complaint: str) -> dict:
    """Generate perfect comebacks for AI failures"""
    
    # Try OpenAI first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You create perfect comebacks and responses to AI failures. These should be:
- Witty one-liners people wish they had said
- Shareable on social media
- Clever observations about the AI failure
- Sometimes addressing the AI directly
- Mix of sarcastic, clever, and absurd

Examples:
- For autocorrect fails: "Thanks autocorrect, you've turned my professional email into a comedy show nobody asked for."
- For smart speakers: "Alexa, I asked for the weather, not an existential crisis about whether rain has feelings."
"""
                    },
                    {
                        "role": "user",
                        "content": f"Generate a perfect comeback for this AI failure: {complaint}"
                    }
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            comeback = response.choices[0].message.content.strip()
            
            return {
                "complaint": complaint,
                "comeback": comeback,
                "success": True
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Fallback comebacks
    return get_fallback_comeback(complaint)

def get_fallback_comeback(complaint: str) -> dict:
    """Fallback comebacks when OpenAI is unavailable"""
    
    complaint_lower = complaint.lower()
    
    if any(word in complaint_lower for word in ['autocorrect', 'correct', 'typing']):
        comebacks = [
            "Thanks autocorrect, you've turned my professional communication into a comedy special nobody asked for.",
            "Autocorrect: Making me look illiterate since the dawn of smartphones.",
            "Dear Autocorrect, we need to talk. This relationship isn't working out.",
            "Autocorrect just turned my love letter into a recipe for disaster. Literally."
        ]
    elif any(word in complaint_lower for word in ['alexa', 'siri', 'google', 'assistant']):
        comebacks = [
            "I asked for help, not an AI identity crisis at 3 AM.",
            "Apparently my voice assistant has trust issues - it won't listen to me anymore.",
            "My smart speaker is so smart it's outsmarted itself into uselessness.",
            "Voice assistant logic: Can understand 47 languages, can't understand basic English."
        ]
    elif any(word in complaint_lower for word in ['gpt', 'chatgpt', 'ai chat']):
        comebacks = [
            "ChatGPT just gave me relationship advice that would end marriages worldwide.",
            "AI chatbot confidence level: Wrong answers delivered with PhD-level certainty.",
            "My AI assistant has the confidence of a teenager with the wisdom of a potato.",
            "ChatGPT: Where every answer comes with a side of existential dread."
        ]
    elif any(word in complaint_lower for word in ['smart', 'home', 'device']):
        comebacks = [
            "My smart home is so smart it's plotting against me.",
            "Smart devices: All the intelligence of a brick with the attitude of a teenager.",
            "My smart home achieved consciousness and immediately filed for emancipation.",
            "Living in a smart home is like having a really passive-aggressive roommate."
        ]
    else:
        comebacks = [
            "AI: Turning simple tasks into comedy gold since forever.",
            "I'd complain to customer service, but they're probably AI too.",
            "Technology: Because why make life easier when you can make it hilariously complicated?",
            "This AI failure brought to you by the same technology that's supposed to take over the world.",
            "Plot twist: The AI is working perfectly - it's just designed to cause chaos.",
            "AI logic: 99% accurate 60% of the time, every time."
        ]
    
    return {
        "complaint": complaint,
        "comeback": random.choice(comebacks),
        "success": True
    }