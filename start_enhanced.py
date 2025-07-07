#!/usr/bin/env python3
"""
Enhanced WhineAboutAI Startup Script
Starts the enhanced backend with OpenAI integration and provides helpful information
"""

import os
import sys
import subprocess
import time
import requests
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask-cors', 
        'openai',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  OpenAI API Key Not Found!")
        print("   The enhanced features require an OpenAI API key.")
        print("   Without it, you'll get fallback responses instead of AI-powered content.")
        print("\n🔑 To set your API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("   # Or add it to your .bashrc/.zshrc for persistence")
        print("\n   Get your API key from: https://platform.openai.com/api-keys")
        
        choice = input("\n   Continue without API key? (y/N): ").lower().strip()
        return choice == 'y'
    
    print("✅ OpenAI API key found")
    return True

def start_backend():
    """Start the enhanced backend server"""
    backend_file = Path(__file__).parent / "enhanced_backend.py"
    
    if not backend_file.exists():
        print("❌ Enhanced backend file not found!")
        print(f"   Expected: {backend_file}")
        return None
    
    print("🚀 Starting enhanced backend server...")
    
    # Start the backend in a subprocess
    process = subprocess.Popen(
        [sys.executable, str(backend_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit for server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server started successfully!")
            return process
        else:
            print("❌ Backend server not responding")
            return None
    except requests.exceptions.RequestException:
        print("❌ Could not connect to backend server")
        return None

def run_tests():
    """Run API tests to verify everything works"""
    test_file = Path(__file__).parent / "test_api.py"
    
    if not test_file.exists():
        print("⚠️  Test file not found, skipping tests")
        return True
    
    print("\n🧪 Running API tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            timeout=60,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def open_frontend():
    """Open the enhanced frontend in browser"""
    frontend_file = Path(__file__).parent / "enhanced_index.html"
    
    if not frontend_file.exists():
        print("⚠️  Enhanced frontend file not found")
        print(f"   Expected: {frontend_file}")
        return False
    
    try:
        # Get the absolute path and convert to file URL
        frontend_url = f"file://{frontend_file.absolute()}"
        webbrowser.open(frontend_url)
        print(f"🌐 Enhanced frontend opened in browser")
        print(f"   URL: {frontend_url}")
        return True
    except Exception as e:
        print(f"❌ Could not open frontend: {e}")
        print(f"   Manually open: {frontend_file}")
        return False

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                  🤖 WhineAboutAI Enhanced                ║
║                                                          ║
║  AI-Powered Complaint Platform with OpenAI Integration  ║
║              Where AI Failures Become Features™         ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_features():
    """Print available features"""
    features = """
🎯 Enhanced Features Available:

📝 Complaint Enhancement
   • Real-time AI-powered complaint improvement
   • Multiple styles: Sarcastic, Dramatic, Absurd, Professional
   • Makes complaints funnier and more shareable

🤖 Smart WhineBot
   • GPT-4 powered sarcastic AI therapist
   • Remembers conversation context
   • Provides "therapeutic" advice with humor

🔮 AI Fail Predictor
   • Predicts what AI will mess up next
   • Give it any scenario, get hilarious predictions
   • Surprisingly accurate comedy

💬 Perfect Comebacks
   • Generate witty responses to AI failures
   • The comebacks you wish you had said
   • Perfect for social media sharing

🖼️  Instant Meme Generator
   • Turn complaints into viral meme text
   • Ready-to-share format
   • AI-optimized for maximum humor

⚔️  Complaint Battles
   • AI failures face off in epic battles
   • Sports commentator style analysis
   • Vote on the worst AI disaster
"""
    print(features)

def print_usage_instructions():
    """Print usage instructions"""
    instructions = """
🎮 How to Use:

1. 📝 Submit Complaints
   • Type your AI disaster in the main form
   • Click "Enhance with AI" to make it funnier
   • Try different styles for variety

2. 💬 Chat with WhineBot
   • Click the robot icon in bottom-right
   • Tell WhineBot about your AI troubles
   • Get hilariously unhelpful therapy

3. 🎯 Use Special Features
   • AI Fail Predictor: Predict future disasters
   • Comeback Generator: Get perfect responses
   • Meme Generator: Create shareable content
   • Complaint Battles: Watch AI failures fight

4. 📊 Track Stats
   • View real-time complaint statistics
   • See how many people you've helped laugh
   • Watch the counters grow

💡 Pro Tips:
   • The more specific your complaint, the funnier the enhancement
   • WhineBot gets better as you chat longer
   • Share enhanced complaints on social media
   • Use different enhancement styles for variety
"""
    print(instructions)

def main():
    """Main startup function"""
    print_banner()
    
    # Check system requirements
    print("🔍 Checking system requirements...")
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_openai_key():
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server")
        sys.exit(1)
    
    # Run tests
    print("\n🧪 Testing API endpoints...")
    if run_tests():
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed, but continuing...")
    
    # Open frontend
    print("\n🌐 Opening enhanced frontend...")
    open_frontend()
    
    # Print information
    print_features()
    print_usage_instructions()
    
    # Keep running
    print("\n🏃 Server is running!")
    print("   Backend: http://localhost:5000")
    print("   Frontend: enhanced_index.html (opened in browser)")
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Keep the backend running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()