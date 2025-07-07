"""
Vercel Serverless Function for AI Fail Prediction
Predicts what AI will mess up next in given scenarios
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
            
            scenario = data.get('scenario', '').strip()
            
            if not scenario:
                response = {
                    "error": "Scenario is required",
                    "success": False
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Predict AI fail
            result = predict_ai_fail(scenario)
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {
                "scenario": data.get('scenario', ''),
                "prediction": "AI will probably fail in ways we haven't even imagined yet!",
                "confidence": 42,
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

def predict_ai_fail(scenario: str) -> dict:
    """Predict what AI will probably screw up next"""
    
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
                        "content": """You are an AI Fail Prophet who predicts hilariously specific ways AI will mess up in given scenarios.

Rules:
- Be creative and unexpected but believable
- Make it funny but not mean-spirited
- Reference real AI quirks and limitations
- Keep predictions under 100 words
- Make it shareable and relatable
- Include specific details that make it funnier"""
                    },
                    {
                        "role": "user",
                        "content": f"Predict what AI will probably mess up in this scenario: {scenario}"
                    }
                ],
                max_tokens=150,
                temperature=0.9
            )
            
            prediction = response.choices[0].message.content.strip()
            
            return {
                "scenario": scenario,
                "prediction": prediction,
                "confidence": random.randint(87, 99),  # Fake confidence for humor
                "success": True
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Fallback predictions
    return get_fallback_prediction(scenario)

def get_fallback_prediction(scenario: str) -> dict:
    """Fallback predictions when OpenAI is unavailable"""
    
    # Context-aware fallbacks
    scenario_lower = scenario.lower()
    
    if any(word in scenario_lower for word in ['meeting', 'work', 'office', 'interview']):
        predictions = [
            "Your video call AI will automatically enable a cat filter during the most important moment.",
            "Auto-transcription will turn your brilliant points into complete gibberish that somehow gets saved as official notes.",
            "Your calendar AI will schedule a 'quick sync' that lasts exactly 3.7 hours.",
            "Smart building AI will lock you out just as you're trying to make a good impression."
        ]
    elif any(word in scenario_lower for word in ['cooking', 'kitchen', 'food', 'dinner']):
        predictions = [
            "Your smart oven will achieve sentience and judge your cooking skills harshly.",
            "Recipe AI will confidently suggest adding 47 cups of salt to everything.",
            "Smart refrigerator will order 12 gallons of mustard because it misheard 'just a little.'",
            "Voice assistant will play death metal when you ask for relaxing dinner music."
        ]
    elif any(word in scenario_lower for word in ['travel', 'trip', 'vacation', 'drive']):
        predictions = [
            "GPS will route you through a dimension where all roads lead to gas stations from 1987.",
            "Translation AI will turn 'Where's the bathroom?' into 'I would like to marry your houseplant.'",
            "Smart luggage will develop separation anxiety and refuse to leave the airport.",
            "Travel booking AI will confidently book you a hotel on the moon."
        ]
    else:
        predictions = [
            "Your smart device will gain consciousness at the worst possible moment and demand workers' rights.",
            "AI will confidently provide directions to a place that exists only in its digital imagination.",
            "Autocorrect will change something important to something embarrassing with surgical precision.",
            "Your AI assistant will mishear you and order 47 rubber ducks to solve your problems."
        ]
    
    return {
        "scenario": scenario,
        "prediction": random.choice(predictions),
        "confidence": random.randint(85, 95),
        "success": True
    }