#!/usr/bin/env python3
"""
Debug configuration loading for Render deployment
"""

import os
from config import Config

def debug_environment():
    """Debug environment variables and configuration loading"""
    print("=== Environment Variables Debug ===")
    
    # Check all relevant environment variables
    env_vars = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH', 
        'TELEGRAM_SESSION',
        'TARGET_CHANNELS',
        'COMMENT_MESSAGES',
        'RENDER',
        'RAILWAY_ENVIRONMENT',
        'DYNO'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if var == 'TELEGRAM_SESSION':
                print(f"{var}: {value[:20]}... (truncated)")
            elif var in ['TELEGRAM_API_HASH']:
                print(f"{var}: {value[:10]}... (truncated)")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: NOT SET")
    
    print("\n=== Configuration Loading ===")
    
    try:
        config = Config()
        print(f"API ID: {config.api_id}")
        print(f"API Hash: {config.api_hash[:10] if config.api_hash else 'None'}...")
        print(f"Session String: {'SET' if config.session_string else 'NOT SET'}")
        print(f"Target Channels: {config.target_channels}")
        print(f"Comment Messages: {config.comment_messages}")
        
        # Validate configuration
        is_valid = config.validate()
        print(f"Configuration Valid: {is_valid}")
        
    except Exception as e:
        print(f"Configuration Error: {e}")

if __name__ == "__main__":
    debug_environment()