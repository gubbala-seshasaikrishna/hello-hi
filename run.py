#!/usr/bin/env python3
"""
LLM Chat Application Launcher
This script starts the FastAPI server with the Llama 3.2 1B model.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import transformers
        import torch
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        return False

def get_local_ip():
    """Get local IP address for network access"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print("🚀 Starting LLM Chat Application with Llama 3.2 1B")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend.py").exists():
        print("❌ backend.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Check if static files exist
    if not Path("static/index.html").exists():
        print("❌ Frontend files not found. Please ensure static/index.html exists.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Get network info
    local_ip = get_local_ip()
    port = 8000
    
    print(f"\n📱 Access URLs:")
    print(f"   Local:    http://localhost:{port}")
    print(f"   Network:  http://{local_ip}:{port}")
    print(f"\n🔗 For iOS access, use the Network URL on your phone")
    print(f"   Make sure your phone and computer are on the same Wi-Fi network")
    print(f"\n📋 You can add this to your iPhone home screen:")
    print(f"   1. Open Safari and go to http://{local_ip}:{port}")
    print(f"   2. Tap the Share button")
    print(f"   3. Select 'Add to Home Screen'")
    print(f"\n⚡ Starting server...")
    print("   Model loading may take a few minutes on first run")
    print("   Press Ctrl+C to stop\n")
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend:app",
            "--host", "0.0.0.0",
            "--port", str(port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()