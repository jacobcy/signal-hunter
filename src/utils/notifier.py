import os
import httpx
from loguru import logger

async def send_telegram_alert(message: str):
    """
    Send a message to the configured Telegram Channel (for alerts/digests).
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    # Prefer Channel ID for alerts, fallback to Chat ID (Admin DM)
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID") or os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.warning("🚫 Telegram credentials missing. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            logger.info("📢 Telegram alert sent successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to send Telegram alert: {e}")
