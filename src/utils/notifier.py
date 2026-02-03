import os
from loguru import logger
from .teleporter import Teleporter

# Initialize teleporter instance
_teleporter = Teleporter()

async def send_telegram_alert(message: str):
    """
    Send a message to the configured Telegram Channel (for alerts/digests).
    Uses Teleporter which has fallback to urllib if httpx fails.
    """
    # Load environment variables if not already loaded
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            # Manual loading as fallback
            env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
            if os.path.exists(env_path):
                with open(env_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            os.environ[key] = value
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    # Prefer Channel ID for alerts, fallback to Chat ID (Admin DM)
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.warning("🚫 Telegram credentials missing. Skipping alert.")
        return

    # Use Teleporter with retry logic
    success = await _teleporter.send_with_retry(message, chat_id)
    
    if success:
        logger.info("📢 Telegram alert sent successfully.")
    else:
        logger.error("❌ Failed to send Telegram alert after all retries.")