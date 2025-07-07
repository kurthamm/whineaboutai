#!/usr/bin/env python3
"""
Enhanced WhineAboutAI Backend - OpenAI-powered features
Provides multiple AI-enhanced endpoints for complaint processing and content generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import time
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import openai
from openai import OpenAI

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedOpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = {}
        
    def enhance_complaint(self, text: str, style: str = "sarcastic") -> Dict:
        """Enhance complaints to make them funnier and more shareable"""
        try:
            styles = {
                "sarcastic": "Make this complaint hilariously sarcastic while keeping the core frustration. Add witty observations and relatable metaphors.",
                "dramatic": "Turn this complaint into an overly dramatic, theatrical piece. Make it sound like a Shakespearean tragedy about technology.",
                "absurd": "Make this complaint completely absurd and over-the-top while keeping it relatable. Add unexpected comparisons.",
                "professional": "Rewrite this complaint as if it's a professional email that's trying too hard to be polite about AI failures."
            }
            
            style_prompt = styles.get(style, styles["sarcastic"])
            
            response = self.client.chat.completions.create(
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
            logger.error(f"Complaint enhancement error: {e}")
            return {
                "original": text,
                "enhanced": text,
                "style": style,
                "success": False,
                "error": str(e)
            }
    
    def whinebot_response(self, message: str, conversation_id: str = "default") -> Dict:
        """Enhanced WhineBot with better personality and memory"""
        try:
            # Get conversation history
            history = self.conversation_history.get(conversation_id, [])
            
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
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=200,
                temperature=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.3
            )
            
            bot_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            self.conversation_history[conversation_id].append({"role": "user", "content": message})
            self.conversation_history[conversation_id].append({"role": "assistant", "content": bot_response})
            
            # Keep only last 8 messages
            if len(self.conversation_history[conversation_id]) > 8:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-8:]
            
            return {
                "response": bot_response,
                "conversation_id": conversation_id,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"WhineBot error: {e}")
            # Fallback responses
            fallbacks = [
                "I'm having technical difficulties... which is ironic since you're complaining about AI technical difficulties! 🤖💔",
                "Error 500: My sarcasm module is temporarily offline. Please try again later! 😵",
                "I'd give you a witty response, but my AI brain just blue-screened. The irony is delicious! 💙"
            ]
            return {
                "response": random.choice(fallbacks),
                "conversation_id": conversation_id,
                "success": False,
                "error": str(e)
            }
    
    def predict_ai_fail(self, scenario: str) -> Dict:
        """Predict what AI will probably screw up next"""
        try:
            response = self.client.chat.completions.create(
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
            logger.error(f"AI prediction error: {e}")
            fallback_predictions = [
                "Your smart device will definitely gain sentience at the worst possible moment.",
                "Autocorrect will change something important to something embarrassing.",
                "An AI will confidently give you directions to a place that doesn't exist.",
                "Your voice assistant will mishear you and order 47 rubber ducks."
            ]
            return {
                "scenario": scenario,
                "prediction": random.choice(fallback_predictions),
                "confidence": 42,
                "success": False
            }
    
    def generate_comeback(self, complaint: str) -> Dict:
        """Generate perfect comebacks for AI failures"""
        try:
            response = self.client.chat.completions.create(
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
            logger.error(f"Comeback generation error: {e}")
            return {
                "complaint": complaint,
                "comeback": "I'd give you a comeback, but my AI is too busy being the thing you're complaining about!",
                "success": False
            }
    
    def create_meme_text(self, complaint: str) -> Dict:
        """Generate meme-worthy text from complaints"""
        try:
            response = self.client.chat.completions.create(
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
            logger.error(f"Meme generation error: {e}")
            return {
                "top_text": "AI FAILS AGAIN",
                "bottom_text": "SURPRISED PIKACHU FACE",
                "meme_type": "classic",
                "original_complaint": complaint,
                "success": False
            }
    
    def complaint_battle_commentary(self, complaint1: str, complaint2: str) -> Dict:
        """Generate sports announcer style commentary for complaint battles"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a sports announcer commentating on AI failure battles. 
Be dramatic, entertaining, and funny. Treat each complaint like a contestant in a competition.
Include play-by-play commentary, analysis of each complaint's "power level", and a prediction."""
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
            logger.error(f"Battle commentary error: {e}")
            return {
                "complaint1": complaint1,
                "complaint2": complaint2,
                "commentary": "Ladies and gentlemen, we have two fierce competitors in the ring tonight! The crowd goes wild as AI failures clash in an epic battle of technological disappointment!",
                "success": False
            }

# Initialize the service
ai_service = EnhancedOpenAIService()

# API Endpoints

@app.route('/enhance-complaint', methods=['POST'])
def enhance_complaint():
    """Enhance complaints to make them funnier"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data['text'].strip()
        style = data.get('style', 'sarcastic')
        
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        result = ai_service.enhance_complaint(text, style)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Enhance complaint endpoint error: {e}")
        return jsonify({"error": "Enhancement failed", "success": False}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced WhineBot chat endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        conversation_id = data.get('conversation_id', 'default')
        
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        result = ai_service.whinebot_response(message, conversation_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"error": "Chat failed", "success": False}), 500

@app.route('/predict-fail', methods=['POST'])
def predict_fail():
    """Predict what AI will mess up next"""
    try:
        data = request.get_json()
        if not data or 'scenario' not in data:
            return jsonify({"error": "Scenario is required"}), 400
        
        scenario = data['scenario'].strip()
        if not scenario:
            return jsonify({"error": "Scenario cannot be empty"}), 400
        
        result = ai_service.predict_ai_fail(scenario)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Predict fail endpoint error: {e}")
        return jsonify({"error": "Prediction failed", "success": False}), 500

@app.route('/generate-comeback', methods=['POST'])
def generate_comeback():
    """Generate perfect comebacks for AI failures"""
    try:
        data = request.get_json()
        if not data or 'complaint' not in data:
            return jsonify({"error": "Complaint is required"}), 400
        
        complaint = data['complaint'].strip()
        if not complaint:
            return jsonify({"error": "Complaint cannot be empty"}), 400
        
        result = ai_service.generate_comeback(complaint)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Generate comeback endpoint error: {e}")
        return jsonify({"error": "Comeback generation failed", "success": False}), 500

@app.route('/create-meme', methods=['POST'])
def create_meme():
    """Generate meme text from complaints"""
    try:
        data = request.get_json()
        if not data or 'complaint' not in data:
            return jsonify({"error": "Complaint is required"}), 400
        
        complaint = data['complaint'].strip()
        if not complaint:
            return jsonify({"error": "Complaint cannot be empty"}), 400
        
        result = ai_service.create_meme_text(complaint)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Create meme endpoint error: {e}")
        return jsonify({"error": "Meme creation failed", "success": False}), 500

@app.route('/battle-commentary', methods=['POST'])
def battle_commentary():
    """Generate commentary for complaint battles"""
    try:
        data = request.get_json()
        if not data or 'complaint1' not in data or 'complaint2' not in data:
            return jsonify({"error": "Two complaints are required"}), 400
        
        complaint1 = data['complaint1'].strip()
        complaint2 = data['complaint2'].strip()
        
        if not complaint1 or not complaint2:
            return jsonify({"error": "Both complaints must be non-empty"}), 400
        
        result = ai_service.complaint_battle_commentary(complaint1, complaint2)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Battle commentary endpoint error: {e}")
        return jsonify({"error": "Commentary generation failed", "success": False}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced WhineAboutAI Backend",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "complaint_enhancement",
            "enhanced_whinebot",
            "ai_fail_prediction", 
            "comeback_generation",
            "meme_creation",
            "battle_commentary"
        ],
        "openai_available": bool(os.getenv('OPENAI_API_KEY'))
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Simple stats endpoint"""
    return jsonify({
        "active_conversations": len(ai_service.conversation_history),
        "total_messages": sum(len(conv) for conv in ai_service.conversation_history.values()),
        "features_available": 6
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)