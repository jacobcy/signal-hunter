#!/usr/bin/env python3
"""
Teleporter Module - Pure Transport Layer
Handles delivery mechanisms to Telegram with fallback strategies.
"""

import os
import json
import asyncio
from typing import Optional
from loguru import logger


def load_env_file():
    """Load environment variables from .env file in project root."""
    try:
        # Try to import python-dotenv first
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # Fallback implementation to manually parse .env file
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))
        if os.path.exists(env_path):
            with open(env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        os.environ[key] = value


class Teleporter:
    """Handles the delivery mechanism to Telegram."""
    
    def __init__(self):
        load_env_file()
        
    async def send_message(self, message_text: str, target_id: Optional[str] = None) -> bool:
        """
        Send a message to Telegram with retry logic and fallback methods.
        
        Args:
            message_text: The text content to send
            target_id: Optional target ID, defaults to env var
            
        Returns:
            bool: Success status
        """
        # Use provided target_id or fall back to environment variable
        chat_id = target_id or os.getenv("TELEGRAM_CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")
        
        if not chat_id:
            logger.error("❌ TELEGRAM_CHANNEL_ID or TELEGRAM_CHAT_ID not set")
            return False
            
        # Try primary method first (httpx)
        success = await self._send_with_httpx(message_text, chat_id)
        
        if not success:
            # Fallback to urllib
            success = self._send_with_urllib(message_text, chat_id)
            
        return success
    
    async def _send_with_httpx(self, message_text: str, chat_id: str) -> bool:
        """Primary method: Send message using httpx."""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set")
            return False

        # Wrap the entire message in a code block to avoid Markdown parsing issues
        message_text_formatted = f"```{message_text}```"
            
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text_formatted,
            "parse_mode": "MarkdownV2"
        }
        
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload)
                
                if resp.status_code == 200:
                    logger.info("✅ Message sent successfully via httpx")
                    return True
                else:
                    logger.error(f"❌ Failed to send via httpx. Status: {resp.status_code}, Response: {resp.text}")
                    return False
        except ImportError:
            logger.warning("⚠️ httpx not available, falling back to urllib")
            return False
        except Exception as e:
            logger.error(f"❌ Error sending via httpx: {e}")
            return False

    def _send_with_urllib(self, message_text: str, chat_id: str) -> bool:
        """Fallback method: Send message using urllib."""
        import urllib.request

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set")
            return False

        # Wrap the entire message in a code block to avoid Markdown parsing issues
        message_text_formatted = f"```{message_text}```"

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text_formatted,
            "parse_mode": "MarkdownV2"
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    logger.info("✅ Message sent successfully via urllib")
                    return True
                else:
                    logger.error(f"❌ Failed to send via urllib. Status: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Exception in urllib sender: {e}")
            return False

    async def send_with_retry(self, message_text: str, target_id: Optional[str] = None, max_attempts: int = 3) -> bool:
        """
        Send message with retry logic.
        
        Args:
            message_text: The text content to send
            target_id: Optional target ID, defaults to env var
            max_attempts: Maximum number of retry attempts
            
        Returns:
            bool: Success status
        """
        for attempt in range(1, max_attempts + 1):
            if attempt > 1:
                logger.info(f"🔄 Retry attempt {attempt}/{max_attempts}")
                
            success = await self.send_message(message_text, target_id)
            
            if success:
                return True
                
            # Wait before retry (exponential backoff could be implemented here)
            if attempt < max_attempts:
                await asyncio.sleep(2 ** attempt)  # 2, 4, 8 seconds etc.
        
        logger.error("❌ All retry attempts failed")
        return False
