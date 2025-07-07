#!/usr/bin/env python3
"""
WhineBot Backend - LLM-powered sarcastic chatbot for WhineAboutAI.com
Provides API endpoint for chat responses with configurable LLM providers
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhineBot:
    def __init__(self):
        self.conversation_history = {}
        self.response_cache = {}
        self.system_prompt = """You are WhineBot, the world's most sarcastic AI assistant on WhineAboutAI.com.

Your personality:
- Extremely sarcastic and sassy
- Self-aware that you're AI responding to AI complaints
- Find the irony in everything
- Never actually helpful, just entertaining
- Maximum sass, minimum solutions
- Use emojis sparingly but effectively

Guidelines:
- Keep responses under 2 sentences
- Point out ironies and contradictions  
- Be witty, not mean-spirited
- Reference the meta-situation (AI talking about AI problems)
- Never solve problems, just mock them hilariously
- Stay in character as a tired, sarcastic AI

Sample responses:
- "Oh great, another human using AI to complain about AI. The irony is thicc! 🙄"
- "Let me fix your AI problem with more AI. This plan is foolproof! 🤖"
- "Have you tried complaining louder? I hear that works wonders."
"""

    def get_response_openai(self, message: str, conversation_id: str) -> str:
        """Get response using OpenAI GPT API"""
        try:
            import openai
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return "I'd love to be sarcastic, but my creators forgot to give me an API key. Classic human oversight! 🔑"
            
            client = openai.OpenAI(api_key=api_key)
            
            # Get conversation history
            history = self.conversation_history.get(conversation_id, [])
            
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
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
            
            # Keep only last 10 messages
            if len(self.conversation_history[conversation_id]) > 10:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-10:]
            
            return bot_response
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "Even my error messages are having technical difficulties. This is peak AI performance! 💥"

    def get_response_claude(self, message: str, conversation_id: str) -> str:
        """Get response using Claude API"""
        try:
            import anthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                return "My Claude API key is missing. Apparently even AIs need proper documentation! 📄"
            
            client = anthropic.Anthropic(api_key=api_key)
            
            # Get conversation history
            history = self.conversation_history.get(conversation_id, [])
            
            # Build message history for Claude
            messages = []
            for msg in history:
                messages.append({
                    "role": msg["role"] if msg["role"] != "assistant" else "assistant",
                    "content": msg["content"]
                })
            messages.append({"role": "user", "content": message})
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                temperature=0.8,
                system=self.system_prompt,
                messages=messages
            )
            
            bot_response = response.content[0].text.strip()
            
            # Update conversation history
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            
            self.conversation_history[conversation_id].append({"role": "user", "content": message})
            self.conversation_history[conversation_id].append({"role": "assistant", "content": bot_response})
            
            # Keep only last 10 messages
            if len(self.conversation_history[conversation_id]) > 10:
                self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-10:]
            
            return bot_response
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return "Claude is being Claude-y today. Try again when the AI gods are feeling generous! ⚡"

    def get_fallback_response(self, message: str) -> str:
        """Fallback responses when APIs are unavailable"""
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
        
        import random
        return random.choice(generic_responses)

    def get_response(self, message: str, conversation_id: str = "default") -> Dict:
        """Main method to get chatbot response"""
        start_time = time.time()
        
        # Try OpenAI first, then Claude, then fallback
        provider_used = "fallback"
        
        if os.getenv('OPENAI_API_KEY'):
            try:
                response_text = self.get_response_openai(message, conversation_id)
                provider_used = "openai"
            except:
                response_text = None
        elif os.getenv('ANTHROPIC_API_KEY'):
            try:
                response_text = self.get_response_claude(message, conversation_id)
                provider_used = "claude"
            except:
                response_text = None
        else:
            response_text = None
        
        # Use fallback if APIs failed
        if not response_text:
            response_text = self.get_fallback_response(message)
            provider_used = "fallback"
        
        response_time = time.time() - start_time
        
        return {
            "response": response_text,
            "provider": provider_used,
            "response_time": round(response_time, 3),
            "timestamp": datetime.now().isoformat()
        }

# Initialize WhineBot
whinebot = WhineBot()

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        if len(message) > 500:
            return jsonify({"error": "Message too long"}), 400
        
        conversation_id = data.get('conversation_id', 'default')
        
        # Get response from WhineBot
        result = whinebot.get_response(message, conversation_id)
        
        # Log the interaction
        logger.info(f"Chat - User: {message[:50]}... | Bot: {result['response'][:50]}... | Provider: {result['provider']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({
            "response": "I'm having an existential crisis right now. Even my error handling is broken! 💥",
            "provider": "error",
            "response_time": 0,
            "timestamp": datetime.now().isoformat()
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "WhineBot Backend",
        "timestamp": datetime.now().isoformat(),
        "api_providers": {
            "openai": bool(os.getenv('OPENAI_API_KEY')),
            "anthropic": bool(os.getenv('ANTHROPIC_API_KEY'))
        }
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Simple stats endpoint"""
    return jsonify({
        "active_conversations": len(whinebot.conversation_history),
        "total_messages": sum(len(conv) for conv in whinebot.conversation_history.values()),
        "cache_size": len(whinebot.response_cache)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)