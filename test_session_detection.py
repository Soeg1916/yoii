#!/usr/bin/env python3
"""
Test session string detection for debugging Render deployment
"""

import os
from config import Config

def test_session_detection():
    """Test if session string is properly detected"""
    print("=== Session Detection Test ===")
    
    # Test with mock session string
    test_session = "1BVtsOG8BuG5dWTgczEdHqQEj7FVJEXpLy8E0oS7Q7OvVZK7k8B4xkD"
    os.environ['TELEGRAM_SESSION'] = test_session
    
    # Load config
    config = Config()
    
    print(f"Environment Variable: {os.getenv('TELEGRAM_SESSION')[:20]}...")
    print(f"Config Session String: {config.session_string[:20] if config.session_string else 'None'}...")
    print(f"Session Detected: {'YES' if config.session_string else 'NO'}")
    
    # Clean up
    del os.environ['TELEGRAM_SESSION']
    
    return config.session_string is not None

if __name__ == "__main__":
    success = test_session_detection()
    print(f"\nTest Result: {'PASS' if success else 'FAIL'}")