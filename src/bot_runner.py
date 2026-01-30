import logging
import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from loguru import logger
from src.core.engine import Engine
from src.models.schemas import PlatformType
from src.core.database import Database
from src.core.summarizer import Summarizer
from src.core.config import config

# Setup logging from config
log_level = config.logging.get('level', 'INFO')
log_file = config.logging.get('file', 'logs/bot.log')
logger.add(log_file, rotation=config.logging.get('max_size', '10 MB'), retention=config.logging.get('backup_count', 7))

# Global instances
engine = Engine()
summarizer = Summarizer()
last_scan_time = None
is_scanning = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_command(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Signal Hunter Help*\n"
        "-----------------------\n"
        "Available Commands:\n\n"
        "📰 /digest\n"
        "Generate a summary of the last 24h activity.\n\n"
        "🔍 /scan\n"
        "Force an immediate scan of all sources.\n\n"
        "📊 /status\n"
        "Check system health, last scan time, and signal counts.\n\n"
        "➕ /add <Name> <URL> [Platform]\n"
        "Add a new source to monitor.\n"
        "Example: `/add Elon https://x.com/elonmusk twitter`\n\n"
        "ℹ️ /help\n"
        "Show this help message."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_scan_time
    
    db = Database()
    try:
        recent_signals = await db.get_recent_signals(hours=24)
        signal_count = len(recent_signals)
    except Exception as e:
        signal_count = f"Error: {e}"
    finally:
        await db.close()

    msg = f"📊 *System Status*\n"
    msg += f"------------------\n"
    msg += f"🕒 Last Scan: {last_scan_time.strftime('%H:%M:%S') if last_scan_time else 'Never'}\n"
    msg += f"📡 Sources: {len(engine.sources) if engine.sources else 'Not loaded'}\n"
    msg += f"📈 Signals (24h): {signal_count}\n"
    msg += f"🏃 Status: {'Scanning...' if is_scanning else 'Idle'}"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')

async def digest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="📰 Generating Daily Digest with DeepSeek...")
    
    db = Database()
    try:
        signals = await db.get_recent_signals(hours=24)
        
        if not signals:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="📭 No signals or activity recorded in the last 24 hours.")
            return

        digest_text = summarizer.generate_digest(signals)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=digest_text, parse_mode='Markdown')
        
        # **强制广播到主频道**
        channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
        if channel_id:
             try:
                 await context.bot.send_message(chat_id=channel_id, text=digest_text, parse_mode='Markdown')
                 logger.info(f"📢 Broadcasted digest to channel: {channel_id}")
             except Exception as e:
                 logger.error(f"Failed to broadcast digest to channel: {e}")

    except Exception as e:
        logger.exception("Digest generation failed")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Failed to generate digest: {e}")
    finally:
        await db.close()

async def scan_job(context: ContextTypes.DEFAULT_TYPE):
    global last_scan_time, is_scanning
    
    chat_id = context.job.chat_id if context.job and context.job.chat_id else os.getenv("TELEGRAM_CHAT_ID")
    
    if is_scanning:
        if chat_id:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Scan already in progress.")
        return

    is_scanning = True
    if chat_id:
        await context.bot.send_message(chat_id=chat_id, text="🚀 Starting Scan...")
    
    try:
        engine.load_sources_from_memory()
        await engine.run_cycle()
        last_scan_time = datetime.now()
        if chat_id:
            await context.bot.send_message(chat_id=chat_id, text="✅ Scan Complete.")
    except Exception as e:
        logger.exception("Scan failed")
        if chat_id:
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Scan Failed: {str(e)}")
    finally:
        is_scanning = False

async def manual_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="⏳ Queuing manual scan...")
    context.job_queue.run_once(scan_job, when=0, chat_id=update.effective_chat.id)

async def add_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Usage: /add <Name> <URL> [Platform]")
        return

    name = args[0]
    url = args[1]
    platform = args[2] if len(args) > 2 else "generic"

    try:
        # 从配置读取现有源，添加新源
        sources = config.sources
        new_source = {'name': name, 'url': url, 'platform': platform, 'weight': 1.0}
        sources.append(new_source)
        
        # 写回配置文件
        with open("memory/bloggers.md", "a") as f:
            f.write(f"| {name} | {url} | {platform} | 1.0 |\n")
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ Added source: {name}")
        engine.load_sources_from_memory()
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Failed to add: {e}")

async def debug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sniffer function to find Chat IDs"""
    chat = update.effective_chat
    msg = f"🆔 **ID Sniffer Report**\nYour Chat ID: `{chat.id}` ({chat.type})\n"
    
    if update.message and update.message.forward_from_chat:
        fwd = update.message.forward_from_chat
        msg += f"Forwarded Source ID: `{fwd.id}` ({fwd.type}, Title: {fwd.title})"
        logger.info(f"🕵️ DETECTED FORWARD ID: {fwd.id} | Title: {fwd.title}")
    else:
        msg += "(Forward a message from your channel to see its ID)"
        
    await context.bot.send_message(chat_id=chat.id, text=msg, parse_mode='Markdown')

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in env.")
        exit(1)

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('digest', digest_command))
    application.add_handler(CommandHandler('daily', digest_command))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('scan', manual_scan))
    application.add_handler(CommandHandler('add', add_source))
    
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, debug_message))

    # 从配置读取调度设置
    interval_minutes = config.scheduler.get('interval_minutes', 60)
    first_delay = config.scheduler.get('first_run_delay_seconds', 10)
    target_chat_id = config.telegram.get('channel_id') or config.telegram.get('admin_chat_id')
    
    if target_chat_id:
        application.job_queue.run_repeating(scan_job, interval=interval_minutes*60, first=first_delay, chat_id=target_chat_id)
    
    logger.info("🤖 Bot Runner Starting Polling...")
    
    # 优雅关闭：确保旧连接断开
    def signal_handler(signum, frame):
        logger.info("🛑 Received shutdown signal. Stopping gracefully...")
        application.stop()
        exit(0)
    
    import signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("👋 Keyboard interrupt received. Stopping gracefully...")
        application.stop()
    finally:
        logger.info("🏁 Bot Runner stopped.")

# 防止快速重启冲突
import time, os
time.sleep(3)  # 启动前强制等待3秒，给旧连接清理时间
if __name__ == '__main__':
    # 主逻辑在上面
    pass

