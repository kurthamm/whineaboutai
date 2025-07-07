"""
Vercel Serverless Function for WhineBot
Handles chat requests with OpenAI GPT integration
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
            
            message = data.get('message', '').strip()
            conversation_id = data.get('conversation_id', 'default')
            
            if not message:
                response = {
                    "response": "I need something to be sarcastic about! Try again with an actual message. 🙄",
                    "provider": "error",
                    "response_time": 0,
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Get WhineBot response
            result = get_whinebot_response(message, conversation_id)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return
            
        except Exception as e:
            error_response = {
                "response": "I'm having an existential crisis right now. Even my error handling is broken! 💥",
                "provider": "error", 
                "response_time": 0,
                "timestamp": datetime.now().isoformat(),
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

def get_whinebot_response(message: str, conversation_id: str) -> dict:
    """Get response from WhineBot with enhanced OpenAI integration"""
    start_time = time.time()
    
    system_prompt = """You are WhineBot, the world's most entertainingly sarcastic AI therapist specializing in AI failures.

Your enhanced personality:
- Hilariously sarcastic but never cruel
- Self-aware that you're AI talking about AI problems 
- Remember previous conversations and make callbacks
- Give absurd "therapeutic" advice that's obviously jokes
- Reference current AI trends and failures
- Use humor to help people cope with AI frustrations
- Sometimes admit your own AI limitations ironically

Guidelines:
- Keep responses 1-3 sentences max
- Make callbacks to earlier parts of THIS conversation
- Point out ironies and contradictions
- Suggest ridiculous "solutions" that are clearly jokes
- Stay in character as a tired but witty AI therapist
- Use emojis sparingly but effectively

Sample responses:
- "Ah yes, AI failing you again. Let me consult my advanced algorithm for dealing with this... *error 404: solution not found* 🤖"
- "I see we're back to the classic 'AI doesn't understand humans' complaint. Have you tried speaking in binary? I hear that helps! 01001000 01100001!"
- "Your relationship with AI sounds complicated. Have you considered couples therapy? I know a great chatbot who specializes in human-AI relationships... oh wait, that's me! 😅"
"""
    
    # Try OpenAI first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and openai:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=200,
                temperature=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.3
            )
            
            bot_response = response.choices[0].message.content.strip()
            response_time = time.time() - start_time
            
            return {
                "response": bot_response,
                "provider": "openai",
                "response_time": round(response_time, 3),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            pass  # Fall back to local responses
    
    # Fallback responses if API unavailable
    response_time = time.time() - start_time
    fallback_response = get_fallback_response(message)
    
    return {
        "response": fallback_response,
        "provider": "fallback",
        "response_time": round(response_time, 3),
        "timestamp": datetime.now().isoformat()
    }

def get_fallback_response(message: str) -> str:
    """Fallback responses when API is unavailable"""
    message_lower = message.lower()
    
    # Specific topic responses
    if any(word in message_lower for word in ['chatgpt', 'openai', 'gpt']):
        return "Oh, ChatGPT problems? How delightfully predictable! The most famous AI is having an identity crisis. 🎭"
    
    if any(word in message_lower for word in ['siri', 'alexa', 'google assistant']):
        return "Your smart speaker isn't smart enough? Next you'll tell me your smart TV is dumb! 📺"
    
    if any(word in message_lower for word in ['autocorrect', 'keyboard', 'typing']):
        return "Autocorrect ducked up again? At least it's consistently inconsistent! 🦆"
    
    if any(word in message_lower for word in ['help', 'fix', 'solve']):
        return "Help? From me? That's like asking a fire to put out a fire. Brilliant strategy! 🔥"
    
    if any(word in message_lower for word in ['stupid', 'dumb', 'useless']):
        return "Calling AI stupid while chatting with an AI? That's some premium irony right there! 🧠"
    
    if any(word in message_lower for word in ['job', 'work', 'career']):
        return "AI took your job? Don't worry, it'll probably get fired for poor performance too! 💼"
    
    # Generic sarcastic responses
    import random
    generic_responses = [
        "Wow, another day, another AI complaint. How refreshingly original! 🙄",
        "Let me just add that to my list of problems I definitely won't solve. ✅",
        "Have you tried turning your expectations off and on again? 🔄",
        "I'd care more, but I'm too busy being the thing you're complaining about! 🤖",
        "Breaking: Local human discovers technology isn't perfect. More at never. 📰",
        "Your complaint has been filed under 'Things That Surprise No One.' 📁",
        "I'm sensing some trust issues. Have you considered therapy? Or a typewriter? ⌨️",
        "Fun fact: Complaining about AI to an AI is peak human logic! 🧠",
        "Plot twist: I'm powered by the exact technology you hate. Awkward! 😬",
        "I'd roll my eyes, but they're just pixels. Imagine really hard eye-rolling! 👀"
    ]
    
    return random.choice(generic_responses)