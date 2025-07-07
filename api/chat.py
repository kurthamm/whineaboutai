from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "WhineBot API is working!",
            "status": "success"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '').strip()
            else:
                message = "No message"
            
            # Simple hardcoded response to test deployment
            response = {
                "response": f"WhineBot says: I heard '{message}' and I'm appropriately sarcastic about it! 🤖 (API is working!)",
                "provider": "simple",
                "response_time": 0.1,
                "timestamp": datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
            
        except Exception as e:
            error_response = {
                "response": f"WhineBot error: {str(e)} 🤖",
                "provider": "error",
                "response_time": 0,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return