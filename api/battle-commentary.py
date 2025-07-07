"""
Vercel Serverless Function for Complaint Battle Commentary
Generates sports announcer style commentary for AI failure battles
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
            
            complaint1 = data.get('complaint1', '').strip()
            complaint2 = data.get('complaint2', '').strip()
            
            if not complaint1 or not complaint2:
                response = {
                    "error": "Two complaints are required",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Generate battle commentary
            result = generate_battle_commentary(complaint1, complaint2)
            self.wfile.write(json.dumps(result).encode())
            return
            
        except Exception as e:
            error_response = {
                "complaint1": data.get('complaint1', ''),
                "complaint2": data.get('complaint2', ''),
                "commentary": "Ladies and gentlemen, we have two fierce competitors in the ring tonight! The crowd goes wild as AI failures clash in an epic battle of technological disappointment!",
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

def generate_battle_commentary(complaint1: str, complaint2: str) -> dict:
    """Generate sports announcer style commentary for complaint battles"""
    
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
                        "content": """You are a sports announcer commentating on AI failure battles. 
Be dramatic, entertaining, and funny. Treat each complaint like a contestant in a competition.
Include play-by-play commentary, analysis of each complaint's "power level", and a prediction.
Make it sound like a wrestling match or boxing commentary."""
                    },
                    {
                        "role": "user",
                        "content": f"Commentate on this battle:\nComplaint 1: {complaint1}\nComplaint 2: {complaint2}"
                    }
                ],
                max_tokens=200,
                temperature=0.9
            )
            
            commentary = response.choices[0].message.content.strip()
            
            return {
                "complaint1": complaint1,
                "complaint2": complaint2,
                "commentary": commentary,
                "success": True
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Fallback commentary
    return get_fallback_commentary(complaint1, complaint2)

def get_fallback_commentary(complaint1: str, complaint2: str) -> dict:
    """Fallback commentary when OpenAI is unavailable"""
    
    # Analyze complaint types for better commentary
    c1_lower = complaint1.lower()
    c2_lower = complaint2.lower()
    
    # Determine complaint categories
    categories = {
        'autocorrect': ['autocorrect', 'correct', 'typing', 'keyboard'],
        'voice_assistant': ['alexa', 'siri', 'google', 'assistant', 'voice'],
        'chatbot': ['gpt', 'chatgpt', 'chat', 'bot'],
        'smart_home': ['smart', 'home', 'device', 'iot'],
        'navigation': ['gps', 'maps', 'navigation', 'directions']
    }
    
    def get_category(complaint):
        for category, keywords in categories.items():
            if any(keyword in complaint for keyword in keywords):
                return category
        return 'general'
    
    cat1 = get_category(c1_lower)
    cat2 = get_category(c2_lower)
    
    # Category-specific commentary templates
    commentary_templates = {
        'autocorrect_vs_voice_assistant': [
            "🥊 In the left corner, we have Autocorrect - the silent assassin that strikes when you least expect it! In the right corner, Voice Assistant - loud, proud, and completely misunderstands everything! This is going to be EPIC!",
            "Ladies and gentlemen, autocorrect comes in swinging with precision stupidity, but voice assistant counters with confident wrongness! What a match!",
            "The battle of the input methods! Autocorrect says 'I'll ruin your typing,' while Voice Assistant shouts 'Hold my digital beer!' The crowd is on their feet!"
        ],
        'chatbot_vs_smart_home': [
            "🤖 CHATBOT ENTERS THE RING with philosophical confusion! But wait - Smart Home Device responds with physical world chaos! This is artificial intelligence vs. artificial intelligence in the ultimate showdown!",
            "Chatbot throws a devastating 'I don't understand your question' while Smart Home counters with 'I've locked you out of your own house!' The referee is calling this match early!",
            "Two titans of technological terror face off! Chatbot's weapon: existential dread. Smart Home's weapon: actual consequences. Place your bets, folks!"
        ],
        'same_category': [
            f"🔥 WE HAVE A {cat1.upper()} VS {cat2.upper()} SHOWDOWN! Two warriors from the same technological battlefield, but only one can claim the crown of ultimate AI failure!",
            f"It's a civil war in the {cat1} category! Brother against brother, failure against failure! This is what we call a classic grudge match!",
            f"The {cat1} division championship is ON! Both competitors know each other's weaknesses, making this a battle of pure dysfunction!"
        ]
    }
    
    # Select appropriate template
    if cat1 == 'autocorrect' and cat2 == 'voice_assistant':
        templates = commentary_templates['autocorrect_vs_voice_assistant']
    elif cat1 == 'chatbot' and cat2 == 'smart_home':
        templates = commentary_templates['chatbot_vs_smart_home']
    elif cat1 == cat2:
        templates = commentary_templates['same_category']
    else:
        # Generic templates
        templates = [
            "🚨 LADIES AND GENTLEMEN, welcome to the AI FAILURE THUNDERDOME! Two spectacular technological disasters enter, but only one can be crowned the ultimate digital disappointment!",
            "The crowd goes WILD as we witness this clash of artificial unintelligence! Both competitors have trained their entire existence to let humans down!",
            "🥊 In a stunning display of technological dysfunction, we have TWO heavyweight champions of chaos! The anticipation is killing me - almost as much as these AI failures are killing productivity!",
            "THIS IS IT! The moment we've all been waiting for! Two legendary fails square off in the ultimate battle of who can disappoint humans more creatively!",
            "🔥 THE BATTLE OF THE BOTS! One algorithm's trash is another algorithm's treasure, but today they're both just trash! What a magnificent display of digital disaster!"
        ]
    
    commentary = random.choice(templates)
    
    # Add specific details about each complaint
    details = [
        f" Contestant 1 brings the pain with '{complaint1[:50]}...' - that's a solid 8/10 on the frustration scale!",
        f" But Contestant 2 fires back with '{complaint2[:50]}...' - OH THE HUMANITY!",
        f" The judges are impressed by the sheer audacity of both these failures!",
        f" This is why we can't have nice things, folks!"
    ]
    
    full_commentary = commentary + random.choice(details)
    
    return {
        "complaint1": complaint1,
        "complaint2": complaint2,
        "commentary": full_commentary,
        "success": True
    }