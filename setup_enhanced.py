#!/usr/bin/env python3
"""
Enhanced WhineAboutAI Setup Script
Installs dependencies and configures the enhanced version
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║              🤖 WhineAboutAI Enhanced Setup               ║
║                                                          ║
║    Setting up AI-powered complaint platform...          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_requirements():
    """Install required packages"""
    requirements_file = Path(__file__).parent / "requirements_enhanced.txt"
    
    if not requirements_file.exists():
        print("❌ Requirements file not found!")
        return False
    
    print("📦 Installing required packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("   Try running: pip install -r requirements_enhanced.txt")
        return False

def setup_environment_file():
    """Create a template .env file"""
    env_file = Path(__file__).parent / ".env.template"
    
    env_content = """# WhineAboutAI Enhanced Configuration
# Copy this file to .env and fill in your values

# OpenAI API Key (Required for AI features)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# Optional: Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Optional: Enhanced features
WHINEBOT_MODEL=gpt-4
WHINEBOT_MAX_TOKENS=200
WHINEBOT_TEMPERATURE=0.8

# Optional: Rate limiting (requests per minute)
RATE_LIMIT_PER_MINUTE=60

# Optional: Logging level
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Environment template created: {env_file}")
        print("   Copy to .env and add your OpenAI API key")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def make_scripts_executable():
    """Make Python scripts executable on Unix systems"""
    if platform.system() in ['Linux', 'Darwin']:  # Linux or macOS
        scripts = [
            'enhanced_backend.py',
            'start_enhanced.py', 
            'test_api.py',
            'setup_enhanced.py'
        ]
        
        for script in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                try:
                    os.chmod(script_path, 0o755)
                    print(f"✅ Made {script} executable")
                except Exception as e:
                    print(f"⚠️  Could not make {script} executable: {e}")

def create_quick_start_script():
    """Create a quick start script"""
    if platform.system() == 'Windows':
        script_name = "quick_start.bat"
        script_content = """@echo off
echo Starting WhineAboutAI Enhanced...
python start_enhanced.py
pause
"""
    else:
        script_name = "quick_start.sh"
        script_content = """#!/bin/bash
echo "Starting WhineAboutAI Enhanced..."
python3 start_enhanced.py
"""
    
    script_path = Path(__file__).parent / script_name
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        if platform.system() != 'Windows':
            os.chmod(script_path, 0o755)
        
        print(f"✅ Quick start script created: {script_name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create quick start script: {e}")
        return False

def verify_setup():
    """Verify the setup is complete"""
    print("\n🔍 Verifying setup...")
    
    # Check if all files exist
    required_files = [
        'enhanced_backend.py',
        'enhanced_index.html',
        'start_enhanced.py',
        'test_api.py',
        'requirements_enhanced.txt'
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = Path(__file__).parent / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_name in missing_files:
            print(f"   - {file_name}")
        return False
    
    # Test imports
    try:
        import flask
        import flask_cors
        import openai
        import requests
        print("✅ All required packages can be imported")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("✅ Setup verification complete!")
    return True

def print_next_steps():
    """Print what to do next"""
    next_steps = """
🎯 Setup Complete! Next Steps:

1. 🔑 Configure OpenAI API Key
   • Get your API key from: https://platform.openai.com/api-keys
   • Set environment variable:
     export OPENAI_API_KEY="your-key-here"
   • Or copy .env.template to .env and edit it

2. 🚀 Start the Application
   • Run: python start_enhanced.py
   • Or use the quick start script

3. 🧪 Test Everything Works
   • The startup script will run tests automatically
   • Or manually run: python test_api.py

4. 🌐 Open Frontend
   • Will open automatically in your browser
   • Or manually open: enhanced_index.html

📚 Documentation:
   • README.md - Project overview
   • docs/SIMPLE_REDESIGN.md - Feature details
   • docs/API.md - API documentation

🎮 Try These Features:
   • Complaint Enhancement - Make complaints funnier
   • Smart WhineBot - AI therapy for AI problems  
   • AI Fail Predictor - Predict future disasters
   • Meme Generator - Create viral content

💡 Tips:
   • The more specific your complaints, the funnier the AI enhancement
   • WhineBot gets better with longer conversations
   • Share enhanced complaints on social media for best results

🆘 Need Help?
   • Check the logs if something doesn't work
   • Make sure your OpenAI API key is valid
   • Ensure you have internet connection for API calls
"""
    print(next_steps)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Package installation failed, but continuing...")
    
    # Setup environment
    setup_environment_file()
    
    # Make scripts executable
    make_scripts_executable()
    
    # Create quick start script
    create_quick_start_script()
    
    # Verify setup
    if verify_setup():
        print("\n🎉 Setup completed successfully!")
        print_next_steps()
    else:
        print("\n❌ Setup verification failed")
        print("   Please check the errors above and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()