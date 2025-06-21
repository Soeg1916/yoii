"""
Configuration management for Telegram Monitor
Handles loading and validation of configuration parameters
"""

import configparser
import os
import logging
from typing import List, Optional

class Config:
    """Configuration manager for the Telegram Monitor application"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        
        # Default configuration values
        self.api_id: Optional[int] = None
        self.api_hash: Optional[str] = None
        self.phone_number: Optional[str] = None
        self.session_name: str = "telegram_monitor_session"
        self.session_string: Optional[str] = None
        self.target_channels: List[str] = []
        self.comment_messages: List[str] = []
        self.comment_delay_min: int = 5
        self.comment_delay_max: int = 15
        self.max_comments_per_hour: int = 10
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables"""
        # Load from config file if it exists
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self._load_from_file()
        else:
            self.logger.warning(f"Config file {self.config_file} not found, using environment variables and defaults")
        
        # Override with environment variables
        self._load_from_env()
        
        # Interactive configuration if needed
        if not self.api_id or not self.api_hash:
            self._interactive_config()
    
    def _load_from_file(self):
        """Load configuration from INI file"""
        try:
            # API Configuration
            if self.config.has_section('api'):
                self.api_id = self.config.getint('api', 'api_id', fallback=None)
                self.api_hash = self.config.get('api', 'api_hash', fallback=None)
                self.phone_number = self.config.get('api', 'phone_number', fallback=None)
                self.session_name = self.config.get('api', 'session_name', fallback=self.session_name)
            
            # Monitor Configuration
            if self.config.has_section('monitor'):
                # Load target channels (new multi-channel format)
                if self.config.has_option('monitor', 'target_channels'):
                    channels = self.config.get('monitor', 'target_channels')
                    self.target_channels = [ch.strip() for ch in channels.split(',') if ch.strip()]
                elif self.config.has_option('monitor', 'target_channel'):  # Backward compatibility
                    self.target_channels = [self.config.get('monitor', 'target_channel')]
                
                # Load comment messages
                messages_str = self.config.get('monitor', 'comment_messages', fallback='')
                if messages_str:
                    self.comment_messages = [msg.strip() for msg in messages_str.split('|') if msg.strip()]
                
                self.comment_delay_min = self.config.getint('monitor', 'comment_delay_min', fallback=self.comment_delay_min)
                self.comment_delay_max = self.config.getint('monitor', 'comment_delay_max', fallback=self.comment_delay_max)
                self.max_comments_per_hour = self.config.getint('monitor', 'max_comments_per_hour', fallback=self.max_comments_per_hour)
                
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # API credentials from environment
        api_id_env = os.getenv('TELEGRAM_API_ID')
        if api_id_env:
            try:
                self.api_id = int(api_id_env)
            except ValueError:
                self.logger.error("Invalid TELEGRAM_API_ID in environment")
        
        if os.getenv('TELEGRAM_API_HASH'):
            self.api_hash = os.getenv('TELEGRAM_API_HASH')
        
        if os.getenv('TELEGRAM_PHONE'):
            self.phone_number = os.getenv('TELEGRAM_PHONE')
        
        target_channels_env = os.getenv('TARGET_CHANNELS')
        if target_channels_env:
            self.target_channels = [ch.strip() for ch in target_channels_env.split(',') if ch.strip()]
        elif os.getenv('TARGET_CHANNEL'):  # Backward compatibility
            target_channel = os.getenv('TARGET_CHANNEL')
            if target_channel:
                self.target_channels = [target_channel]
        
        comment_messages_env = os.getenv('COMMENT_MESSAGES')
        if comment_messages_env:
            self.comment_messages = [msg.strip() for msg in comment_messages_env.split('|') if msg.strip()]
        
        telegram_session = os.getenv('TELEGRAM_SESSION')
        if telegram_session and telegram_session.strip():
            self.session_string = telegram_session.strip()
            self.logger.info("Session string loaded from environment variables")
        else:
            self.logger.warning("TELEGRAM_SESSION environment variable not found or empty")
    
    def _interactive_config(self):
        """Interactive configuration for missing required values"""
        # Skip interactive config if running in cloud environment
        if os.getenv('RENDER') or os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('DYNO'):
            self.logger.error("Missing required environment variables for cloud deployment")
            self.logger.error("Required: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION")
            return
            
        print("\n=== Telegram Monitor Configuration ===")
        
        if not self.api_id:
            while True:
                try:
                    api_id_input = input("Enter your Telegram API ID: ").strip()
                    self.api_id = int(api_id_input)
                    break
                except ValueError:
                    print("Please enter a valid numeric API ID")
                except (EOFError, KeyboardInterrupt):
                    self.logger.error("Configuration cancelled by user")
                    return
        
        if not self.api_hash:
            self.api_hash = input("Enter your Telegram API Hash: ").strip()
        
        if not self.phone_number:
            self.phone_number = input("Enter your phone number (with country code, e.g., +1234567890): ").strip()
        
        if not self.target_channels:
            channels_input = input("Enter target channels (comma-separated, e.g., Sport_433et,channel2): ").strip()
            if channels_input:
                self.target_channels = [ch.strip() for ch in channels_input.split(',') if ch.strip()]
        
        if not self.comment_messages:
            print("\nEnter comment messages (one per line, empty line to finish):")
            messages = []
            while True:
                msg = input("> ").strip()
                if not msg:
                    break
                messages.append(msg)
            
            if messages:
                self.comment_messages = messages
            else:
                self.comment_messages = ["Thanks for sharing!", "Great post!", "Interesting content!"]
        
        # Save configuration
        self._save_config()
    
    def _save_config(self):
        """Save current configuration to file"""
        try:
            # Create config sections
            if not self.config.has_section('api'):
                self.config.add_section('api')
            if not self.config.has_section('monitor'):
                self.config.add_section('monitor')
            
            # API section
            self.config.set('api', 'api_id', str(self.api_id))
            self.config.set('api', 'api_hash', self.api_hash)
            if self.phone_number:
                self.config.set('api', 'phone_number', self.phone_number)
            self.config.set('api', 'session_name', self.session_name)
            
            # Monitor section
            if self.target_channels:
                self.config.set('monitor', 'target_channels', ','.join(self.target_channels))
            if self.comment_messages:
                self.config.set('monitor', 'comment_messages', ' | '.join(self.comment_messages))
            self.config.set('monitor', 'comment_delay_min', str(self.comment_delay_min))
            self.config.set('monitor', 'comment_delay_max', str(self.comment_delay_max))
            self.config.set('monitor', 'max_comments_per_hour', str(self.max_comments_per_hour))
            
            # Write to file
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
            self.logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        errors = []
        
        if not self.api_id:
            errors.append("API ID is required")
        
        if not self.api_hash:
            errors.append("API Hash is required")
        
        if not self.target_channels:
            errors.append("At least one target channel is required")
        
        if not self.comment_messages:
            errors.append("At least one comment message is required")
        
        if self.comment_delay_min < 1:
            errors.append("Comment delay minimum must be at least 1 second")
        
        if self.comment_delay_max < self.comment_delay_min:
            errors.append("Comment delay maximum must be greater than minimum")
        
        if self.max_comments_per_hour < 1:
            errors.append("Max comments per hour must be at least 1")
        
        if errors:
            for error in errors:
                self.logger.error(f"Configuration error: {error}")
            return False
        
        return True
    
    def get_channel_usernames(self) -> List[str]:
        """Get formatted channel usernames"""
        formatted_channels = []
        for channel in self.target_channels:
            channel = channel.strip()
            if not channel.startswith('@'):
                channel = f"@{channel}"
            formatted_channels.append(channel)
        return formatted_channels
