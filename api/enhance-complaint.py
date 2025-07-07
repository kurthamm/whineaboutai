"""
Vercel Serverless Function for Complaint Enhancement
Enhances complaints using OpenAI to make them funnier and more shareable
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import time
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
            
            text = data.get('text', '').strip()
            style = data.get('style', 'sarcastic')
            
            if not text:
                response = {
                    "error": "Text is required",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Enhance complaint
            result = enhance_complaint(text, style)
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {
                "original": data.get('text', ''),
                "enhanced": data.get('text', ''),
                "style": data.get('style', 'sarcastic'),
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

def enhance_complaint(text: str, style: str = "sarcastic") -> dict:
    """Enhance complaints to make them funnier and more shareable"""
    
    styles = {
        "sarcastic": "Make this complaint hilariously sarcastic while keeping the core frustration. Add witty observations and relatable metaphors.",
        "dramatic": "Turn this complaint into an overly dramatic, theatrical piece. Make it sound like a Shakespearean tragedy about technology.",
        "absurd": "Make this complaint completely absurd and over-the-top while keeping it relatable. Add unexpected comparisons.",
        "professional": "Rewrite this complaint as if it's a professional email that's trying too hard to be polite about AI failures."
    }
    
    style_prompt = styles.get(style, styles["sarcastic"])
    
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
                        "content": f"""You are a comedy writer specializing in AI failures. {style_prompt}
                        
                        Rules:
                        - Keep it under 280 characters for shareability
                        - Make it funnier than the original
                        - Don't lose the core frustration
                        - Add a unexpected twist or punchline
                        - Make it relatable to others"""
                    },
                    {
                        "role": "user",
                        "content": f"Original complaint: {text}"
                    }
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            enhanced_text = response.choices[0].message.content.strip()
            
            return {
                "original": text,
                "enhanced": enhanced_text,
                "style": style,
                "success": True
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Fallback enhancement
    return get_fallback_enhancement(text, style)

def get_fallback_enhancement(text: str, style: str) -> dict:
    """Fallback enhancement when OpenAI is unavailable"""
    import random
    
    fallback_enhancements = {
        "sarcastic": [
            f"{text} ...because apparently AI perfection is just a myth! 🙄",
            f"{text} Thanks AI, you really nailed that one! 😏",
            f"{text} ...and they say AI will take over the world! 🤖💀"
        ],
        "dramatic": [
            f"BEHOLD! {text} ...a tragedy of epic technological proportions! 🎭",
            f"In the darkest hour of digital despair: {text} ...shall we ever recover? 💔",
            f"Oh cruel fate! {text} ...why must AI torment us so? ⚡"
        ],
        "absurd": [
            f"{text} ...I blame the robot uprising that clearly started in my living room! 🤖👽",
            f"{text} ...my toaster probably orchestrated this whole thing! 🍞🔥",
            f"{text} ...somewhere, a programmer is laughing maniacally! 😈💻"
        ],
        "professional": [
            f"Dear AI Development Team, {text} I trust this matter will receive your immediate attention. Regards! 📧",
            f"Per our previous discussion with reality, {text} Please advise on next steps. Best! 💼",
            f"Following up on the incident where {text} Looking forward to your response! 📋"
        ]
    }
    
    enhancements = fallback_enhancements.get(style, fallback_enhancements["sarcastic"])
    enhanced = random.choice(enhancements)
    
    return {
        "original": text,
        "enhanced": enhanced,
        "style": style,
        "success": True
    }