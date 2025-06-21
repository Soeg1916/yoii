#!/usr/bin/env python3
"""
Test configuration and validate setup
"""

import os
import sys
from config import Config

def test_configuration():
    """Test configuration loading and validation"""
    print("Testing Telegram Monitor Configuration...")
    print("=" * 50)
    
    try:
        # Test with environment variables (cloud deployment scenario)
        os.environ['TELEGRAM_API_ID'] = '12345678'
        os.environ['TELEGRAM_API_HASH'] = 'test_hash'
        os.environ['TELEGRAM_SESSION'] = 'test_session'
        os.environ['TARGET_CHANNELS'] = 'Sport_433et,channel2,channel3'
        os.environ['COMMENT_MESSAGES'] = 'hey this is me|Hello everyone!'
        
        config = Config()
        
        print(f"✓ API ID: {config.api_id}")
        print(f"✓ API Hash: {config.api_hash[:10] if config.api_hash else 'None'}...")
        print(f"✓ Session String: {config.session_string[:20] if config.session_string else 'None'}...")
        print(f"✓ Target Channels: {config.target_channels}")
        print(f"✓ Comment Messages: {config.comment_messages}")
        print(f"✓ Rate Limit: {config.max_comments_per_hour} comments/hour")
        print(f"✓ Comment Delay: {config.comment_delay_min}-{config.comment_delay_max} seconds")
        
        # Test validation
        is_valid = config.validate()
        print(f"✓ Configuration Valid: {is_valid}")
        
        print("\n" + "=" * 50)
        print("Configuration test completed successfully!")
        
        # Clean up test environment variables
        for key in ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_SESSION', 
                   'TARGET_CHANNELS', 'COMMENT_MESSAGES']:
            if key in os.environ:
                del os.environ[key]
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)