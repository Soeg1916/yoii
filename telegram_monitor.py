"""
Telegram Channel Monitor
Main monitoring and commenting functionality using Telethon
"""

import asyncio
import logging
import os
import random
import time
from typing import Optional, Set
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import (
    FloodWaitError, 
    AuthKeyUnregisteredError,
    UserRestrictedError,
    ChatWriteForbiddenError,
    MessageNotModifiedError
)
from telethon.tl.types import Channel, Chat
from config import Config
from rate_limiter import RateLimiter

class TelegramMonitor:
    """Main class for monitoring Telegram channels and auto-commenting"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.client: Optional[TelegramClient] = None
        self.rate_limiter = RateLimiter(
    max_actions=100,  # 25 comments (or higher like 150, 200)
    time_window=600   # 10 minutes in seconds
)
        self.processed_messages: Set[int] = set()
        self.target_channels = {}  # channel_username -> entity mapping
        self.monitored_channels = []
        self.is_running = False
    
    async def start(self):
        """Start the monitoring process"""
        try:
            await self._initialize_client()
            await self._authenticate()
            await self._setup_target_channels()
            await self._start_monitoring()
        except Exception as e:
            self.logger.error(f"Failed to start monitor: {e}")
            raise
        finally:
            await self._cleanup()
    
    async def _initialize_client(self):
        """Initialize the Telegram client"""
        self.logger.info("Initializing Telegram client...")
        
        # Use string session if available (for cloud deployment)
        if self.config.session_string and self.config.session_string.strip():
            session = StringSession(self.config.session_string)
            self.logger.info("Using string session for cloud deployment")
        else:
            # Check if we're in a cloud environment but missing session string
            if os.getenv('RENDER') or os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('DYNO'):
                self.logger.error("Cloud deployment detected but no TELEGRAM_SESSION provided!")
                self.logger.error("Please add TELEGRAM_SESSION environment variable in your deployment settings")
                raise ValueError("Missing TELEGRAM_SESSION for cloud deployment")
            
            session = self.config.session_name
            self.logger.info("Using file session for local deployment")
        
        self.client = TelegramClient(
            session,
            self.config.api_id,
            self.config.api_hash
        )
        
        await self.client.start()
        self.logger.info("Telegram client initialized successfully")
    
    async def _authenticate(self):
        """Handle user authentication"""
        try:
            if not await self.client.is_user_authorized():
                self.logger.info("User not authorized, starting authentication...")
                
                if not self.config.phone_number:
                    self.config.phone_number = input("Enter your phone number: ")
                
                await self.client.send_code_request(self.config.phone_number)
                code = input("Enter the verification code: ")
                
                try:
                    await self.client.sign_in(self.config.phone_number, code)
                except Exception as e:
                    if "password" in str(e).lower():
                        password = input("Enter your 2FA password: ")
                        await self.client.sign_in(password=password)
                    else:
                        raise
            
            # Get user info
            me = await self.client.get_me()
            self.logger.info(f"Authenticated as: {me.first_name} (@{me.username})")
            
        except AuthKeyUnregisteredError:
            self.logger.error("Authentication key is invalid. Please delete session file and try again.")
            raise
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise
    
    async def _setup_target_channel(self):
        """Setup and validate the target channel"""
        try:
            channel_username = self.config.get_channel_username()
            self.logger.info(f"Setting up target channel: @{channel_username}")
            
            # Get channel entity
            self.target_entity = await self.client.get_entity(channel_username)
            
            # Validate channel type
            if not isinstance(self.target_entity, (Channel, Chat)):
                raise ValueError(f"Target '{channel_username}' is not a channel or group")
            
            # Check if we can access the channel
            if isinstance(self.target_entity, Channel):
                if self.target_entity.left:
                    raise ValueError(f"You have left the channel @{channel_username}")
                
                # Check permissions (handle case where permissions might be None)
                try:
                    permissions = await self.client.get_permissions(self.target_entity)
                    if permissions and not permissions.send_messages:
                        self.logger.warning("You don't have permission to send messages in this channel")
                except Exception as e:
                    self.logger.warning(f"Could not check permissions for channel: {e}")
            
            self.logger.info(f"Target channel setup complete: {self.target_entity.title}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup target channel: {e}")
            raise
    
    async def _setup_target_channels(self):
        """Setup and validate the target channels"""
        channel_usernames = self.config.get_channel_usernames()
        self.logger.info(f"Setting up {len(channel_usernames)} target channels")
        
        for channel_username in channel_usernames:
            try:
                self.logger.info(f"Setting up channel: {channel_username}")
                
                # Get channel entity
                entity = await self.client.get_entity(channel_username)
                
                # Validate channel type
                if not isinstance(entity, (Channel, Chat)):
                    self.logger.error(f"Target '{channel_username}' is not a channel or group")
                    continue
                
                # Check if we can access the channel
                if isinstance(entity, Channel):
                    if entity.left:
                        self.logger.error(f"You have left the channel '{channel_username}'")
                        continue
                    
                    # Check permissions
                    try:
                        permissions = await self.client.get_permissions(entity)
                        if permissions and not permissions.send_messages:
                            self.logger.warning(f"No send permission for {channel_username}")
                    except Exception as e:
                        self.logger.warning(f"Could not check permissions for {channel_username}: {e}")
                
                # Add to monitoring list
                self.target_channels[channel_username] = entity
                self.monitored_channels.append(channel_username)
                self.logger.info(f"Channel setup complete: {channel_username} -> {entity.title}")
                
            except Exception as e:
                self.logger.error(f"Failed to setup channel {channel_username}: {e}")
                continue
        
        if not self.monitored_channels:
            raise Exception("No channels could be set up successfully")
        
        self.logger.info(f"Successfully monitoring {len(self.monitored_channels)} channels")
    
    async def _start_monitoring(self):
        """Start monitoring the target channel for new messages"""
        self.logger.info("Starting channel monitoring...")
        self.is_running = True
        
        # Get all entities for monitoring
        entities = list(self.target_channels.values())
        
        # Register event handler for new messages from all channels
        @self.client.on(events.NewMessage(chats=entities))
        async def handle_new_message(event):
            await self._handle_new_message(event)
        
        try:
            # Keep the client running
            self.logger.info(f"Monitor is now active for {len(entities)} channels. Waiting for new messages...")
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            self.logger.info("Monitor stopped by user")
        except Exception as e:
            self.logger.error(f"Monitor error: {e}")
            raise
        finally:
            self.is_running = False
    
    async def _handle_new_message(self, event):
        """Handle new message events"""
        try:
            message = event.message
            
            # Skip if we've already processed this message
            if message.id in self.processed_messages:
                return
            
            # Skip if message is from ourselves
            if message.sender_id == (await self.client.get_me()).id:
                return
            
            # Skip if message is older than 5 minutes (to avoid commenting on old messages on startup)
            if message.date.timestamp() < (time.time() - 300):
                self.processed_messages.add(message.id)
                return
            
            # Get channel name for logging
            channel_name = "Unknown"
            try:
                chat = await event.get_chat()
                if hasattr(chat, 'title'):
                    channel_name = chat.title
                elif hasattr(chat, 'username'):
                    channel_name = f"@{chat.username}"
            except:
                pass
            
            self.logger.info(f"New message detected in {channel_name}: ID {message.id}")
            
            # Check rate limits
            if not self.rate_limiter.can_perform_action():
                self.logger.warning("Rate limit exceeded, skipping comment")
                self.processed_messages.add(message.id)
                return
            
            # Add delay before commenting to appear more natural
            delay = random.randint(self.config.comment_delay_min, self.config.comment_delay_max)
            self.logger.info(f"Waiting {delay} seconds before commenting...")
            await asyncio.sleep(delay)
            
            # Post comment
            await self._post_comment(message)
            
            # Mark as processed
            self.processed_messages.add(message.id)
            self.rate_limiter.record_action()
            
        except Exception as e:
            self.logger.error(f"Error handling new message: {e}")
    
    async def _post_comment(self, original_message):
        """Post a comment reply to the original message"""
        try:
            # Select comment message
            comment_text = random.choice(self.config.comment_messages)
            
            # Send reply to the message thread/comments
            await self.client.send_message(
                original_message.peer_id,
                comment_text,
                reply_to=original_message.id,
                comment_to=original_message.id
            )
            
            self.logger.info(f"Comment posted successfully: '{comment_text}'")
            
        except FloodWaitError as e:
            self.logger.warning(f"Rate limited by Telegram, need to wait {e.seconds} seconds")
            # Update our rate limiter to be more conservative
            await asyncio.sleep(e.seconds)
            
        except ChatWriteForbiddenError:
            self.logger.error("Cannot send messages to this chat (forbidden)")
            
        except UserRestrictedError:
            self.logger.error("User account is restricted from sending messages")
            
        except MessageNotModifiedError:
            self.logger.warning("Message was not modified (this shouldn't happen for new messages)")
            
        except Exception as e:
            self.logger.error(f"Failed to post comment: {e}")
    
    async def _cleanup(self):
        """Cleanup resources"""
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            self.logger.info("Telegram client disconnected")
