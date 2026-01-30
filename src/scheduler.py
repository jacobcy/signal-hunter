import asyncio
import os
import signal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from src.core.engine import Engine

# Configure Logger to write to file as well, since this is a daemon
logger.add("logs/scheduler.log", rotation="10 MB", retention="7 days")

async def scheduled_job():
    """The job wrapper to run the engine"""
    try:
        logger.info("⏰ Scheduler Trigger: Starting Scan Cycle...")
        engine = Engine()
        engine.load_sources_from_memory()
        await engine.run_cycle()
        logger.info("✅ Scheduler Trigger: Cycle Finished.")
    except Exception as e:
        logger.exception(f"❌ Scheduler Cycle Failed: {e}")

async def main():
    logger.info("🤖 Signal Hunter Scheduler Initializing...")
    
    scheduler = AsyncIOScheduler()
    
    # Schedule to run every 60 minutes
    # You can change this to minutes=30 or hours=1
    scheduler.add_job(scheduled_job, 'interval', minutes=60)
    
    scheduler.start()
    logger.success("🚀 Scheduler Started! (Interval: 60 mins)")
    
    # Run once immediately upon start
    await scheduled_job()
    
    # Keep the main thread alive to let the AsyncIOScheduler run
    # Handle graceful shutdown
    stop_event = asyncio.Event()
    
    def signal_handler():
        logger.info("🛑 Stopping Scheduler...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    await stop_event.wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
