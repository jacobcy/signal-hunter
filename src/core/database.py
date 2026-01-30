import aiosqlite
from datetime import datetime, timedelta
from typing import List, Optional
from loguru import logger
from src.models.schemas import Signal, SignalType

DB_PATH = "memory/signals.db"

class Database:
    """Async SQLite database manager using aiosqlite."""
    
    async def init_tables(self):
        """Initialize database tables."""
        async with aiosqlite.connect(DB_PATH) as conn:
            conn.row_factory = aiosqlite.Row
            # Signals Table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    raw_text TEXT,
                    url TEXT,
                    timestamp DATETIME,
                    confidence REAL
                )
            ''')
            # Alerts Table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await conn.commit()
            logger.debug("Database tables initialized")
    
    async def save_signal(self, signal: Signal) -> bool:
        """Save signal to database. Returns True if saved, False if duplicate."""
        try:
            async with aiosqlite.connect(DB_PATH) as conn:
                conn.row_factory = aiosqlite.Row
                # Check for duplicates
                cursor = await conn.execute('''
                    SELECT id FROM signals 
                    WHERE ticker = ? AND source_name = ? 
                    AND timestamp > datetime(?, '-1 hour')
                ''', (signal.ticker, signal.source_name, signal.timestamp))
                
                if await cursor.fetchone():
                    return False  # Skip duplicate
                
                # Insert signal
                await conn.execute('''
                    INSERT INTO signals (ticker, signal_type, source_name, raw_text, url, timestamp, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    signal.ticker,
                    signal.signal_type.value,
                    signal.source_name,
                    signal.raw_text,
                    str(signal.url),
                    signal.timestamp,
                    signal.confidence
                ))
                await conn.commit()
                logger.debug(f"Saved signal: {signal.ticker} from {signal.source_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving signal: {e}")
            return False
    
    async def get_recent_signals(self, hours: int = 24) -> List[Signal]:
        """Get signals from last N hours."""
        try:
            async with aiosqlite.connect(DB_PATH) as conn:
                conn.row_factory = aiosqlite.Row
                time_threshold = datetime.now() - timedelta(hours=hours)
                
                cursor = await conn.execute('''
                    SELECT * FROM signals 
                    WHERE timestamp > ? 
                    ORDER BY timestamp DESC
                ''', (time_threshold,))
                
                rows = await cursor.fetchall()
                signals = []
                for row in rows:
                    signals.append(Signal(
                        ticker=row['ticker'],
                        signal_type=SignalType(row['signal_type']),
                        source_name=row['source_name'],
                        raw_text=row['raw_text'],
                        url=row['url'],
                        timestamp=datetime.fromisoformat(row['timestamp']) if isinstance(row['timestamp'], str) else row['timestamp'],
                        confidence=row['confidence']
                    ))
                return signals
                
        except Exception as e:
            logger.error(f"Error getting signals: {e}")
            return []
    
    async def is_alerted_recently(self, ticker: str, hours: int = 24) -> bool:
        """Check if ticker was alerted recently."""
        try:
            async with aiosqlite.connect(DB_PATH) as conn:
                conn.row_factory = aiosqlite.Row
                time_threshold = datetime.now() - timedelta(hours=hours)
                cursor = await conn.execute('''
                    SELECT id FROM alerts 
                    WHERE ticker = ? AND timestamp > ?
                ''', (ticker, time_threshold))
                return await cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking alert status: {e}")
            return False
    
    async def record_alert(self, ticker: str) -> None:
        """Record that alert was sent for ticker."""
        try:
            async with aiosqlite.connect(DB_PATH) as conn:
                await conn.execute(
                    'INSERT INTO alerts (ticker, timestamp) VALUES (?, ?)',
                    (ticker, datetime.now())
                )
                await conn.commit()
        except Exception as e:
            logger.error(f"Error recording alert: {e}")
    
    async def close(self):
        """Cleanup (no-op for aiosqlite - connections auto-close)."""
        pass
