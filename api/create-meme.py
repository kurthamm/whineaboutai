"""
Vercel Serverless Function for Meme Generation
Converts complaints into meme-ready text formats
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import random
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
            
            if not complaint:
                response = {
                    "error": "Complaint is required",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Create meme
            result = create_meme_text(complaint)
            self.wfile.write(json.dumps(result).encode())
            return
            
        except Exception as e:
            error_response = {
                "top_text": "AI FAILS AGAIN",
                "bottom_text": "SURPRISED PIKACHU FACE",
                "meme_type": "classic",
                "original_complaint": data.get('complaint', ''),
                "success": False,
                "error": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())
            return
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

def create_meme_text(complaint: str) -> dict:
    """Generate meme-worthy text from complaints"""
    
    # Try OpenAI first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and openai:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Convert complaints into viral meme format. Create:
- Top text and bottom text for memes
- Relatable format that others can share
- Classic meme structures
- Keep it punchy and shareable
- Use meme language and style

Return JSON with: {"top_text": "...", "bottom_text": "...", "meme_type": "..."}
"""
                    },
                    {
                        "role": "user",
                        "content": f"Turn this into meme text: {complaint}"
                    }
                ],
                max_tokens=100,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            meme_data = json.loads(response.choices[0].message.content)
            meme_data["success"] = True
            meme_data["original_complaint"] = complaint
            
            return meme_data
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Fallback meme generation
    return get_fallback_meme(complaint)

def get_fallback_meme(complaint: str) -> dict:
    """Fallback meme generation when OpenAI is unavailable"""
    
    complaint_lower = complaint.lower()
    
    # Template-based memes
    meme_templates = []
    
    if any(word in complaint_lower for word in ['autocorrect', 'correct', 'typing']):
        meme_templates = [
            {
                "top_text": "TRIES TO TYPE NORMAL MESSAGE",
                "bottom_text": "AUTOCORRECT: LET ME RUIN YOUR LIFE",
                "meme_type": "drake_pointing"
            },
            {
                "top_text": "AUTOCORRECT",
                "bottom_text": "MAKING EVERYONE LOOK ILLITERATE SINCE 2007",
                "meme_type": "change_my_mind"
            },
            {
                "top_text": "WHEN AUTOCORRECT CHANGES 'THANKS' TO 'TANKS'",
                "bottom_text": "NOW I SOUND LIKE A MILITARY ENTHUSIAST",
                "meme_type": "distracted_boyfriend"
            }
        ]
    elif any(word in complaint_lower for word in ['alexa', 'siri', 'google', 'assistant']):
        meme_templates = [
            {
                "top_text": "ASKS VOICE ASSISTANT SIMPLE QUESTION",
                "bottom_text": "GETS EXISTENTIAL CRISIS INSTEAD",
                "meme_type": "surprised_pikachu"
            },
            {
                "top_text": "ALEXA, PLAY MY MUSIC",
                "bottom_text": "ALEXA: PLAYS NEIGHBOR'S POLKA COLLECTION",
                "meme_type": "this_is_fine"
            },
            {
                "top_text": "SMART SPEAKER INTELLIGENCE LEVEL",
                "bottom_text": "CONFUSED POTATO",
                "meme_type": "brain_expansion"
            }
        ]
    elif any(word in complaint_lower for word in ['gpt', 'chatgpt', 'ai chat']):
        meme_templates = [
            {
                "top_text": "CHATGPT: I'M VERY CONFIDENT",
                "bottom_text": "ALSO CHATGPT: *COMPLETELY WRONG*",
                "meme_type": "confident_but_wrong"
            },
            {
                "top_text": "ASKS AI FOR HELP",
                "bottom_text": "GETS PHILOSOPHY DEGREE INSTEAD",
                "meme_type": "monkey_puppet"
            },
            {
                "top_text": "AI CHATBOT LOGIC",
                "bottom_text": "50% GENIUS, 50% TODDLER WITH ENCYCLOPEDIA",
                "meme_type": "galaxy_brain"
            }
        ]
    else:
        meme_templates = [
            {
                "top_text": "AI WILL MAKE LIFE EASIER THEY SAID",
                "bottom_text": "IT WILL BE FUN THEY SAID",
                "meme_type": "ancient_aliens"
            },
            {
                "top_text": "HUMANS: CREATE AI TO HELP US",
                "bottom_text": "AI: CREATES NEW WAYS TO CONFUSE US",
                "meme_type": "success_kid"
            },
            {
                "top_text": "WHEN AI FAILS SPECTACULARLY",
                "bottom_text": "BUT YOU STILL USE IT TOMORROW",
                "meme_type": "clown_makeup"
            },
            {
                "top_text": "AI TECHNOLOGY IN 2024",
                "bottom_text": "ADVANCED ENOUGH TO WORRY US, DUMB ENOUGH TO ENTERTAIN US",
                "meme_type": "two_buttons"
            }
        ]
    
    # Select random template
    selected_meme = random.choice(meme_templates)
    selected_meme["success"] = True
    selected_meme["original_complaint"] = complaint
    
    return selected_meme