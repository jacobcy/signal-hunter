import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Optional
from loguru import logger
from src.models.schemas import Signal, SignalType
import threading

DB_PATH = "memory/signals.db"

class Database:
    def __init__(self):
        # 使用线程本地存储，确保每个线程有自己的连接
        self._local = threading.local()
        self._init_tables()
    
    def _get_connection(self):
        """获取或创建线程本地数据库连接"""
        if not hasattr(self._local, 'conn'):
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _init_tables(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Signals Table
        cursor.execute('''
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
        # Alerts History Table (For deduplication)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

    def save_signal(self, signal: Signal):
        """保存信号到数据库"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 避免重复
            cursor.execute('''
                SELECT id FROM signals 
                WHERE ticker = ? AND source_name = ? AND timestamp > datetime(?, '-1 hour')
            ''', (signal.ticker, signal.source_name, signal.timestamp))
            
            if cursor.fetchone():
                return

            cursor.execute('''
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
            conn.commit()
            logger.debug(f"💾 Saved signal: {signal.ticker} from {signal.source_name}")
                
        except Exception as e:
            logger.error(f"Database error in save_signal: {e}")

    def get_recent_signals(self, hours: int = 24) -> List[Signal]:
        """获取最近信号"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT * FROM signals WHERE timestamp > ? ORDER BY timestamp DESC
            ''', (time_threshold,))
            
            rows = cursor.fetchall()
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
            logger.error(f"Database error in get_recent_signals: {e}")
            return []

    def is_alerted_recently(self, ticker: str, hours: int = 24) -> bool:
        """检查是否最近已报警"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            time_threshold = datetime.now() - timedelta(hours=hours)
            cursor.execute('''
                SELECT id FROM alerts WHERE ticker = ? AND timestamp > ?
            ''', (ticker, time_threshold))
            return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Database error in is_alerted_recently: {e}")
            return False

    def record_alert(self, ticker: str):
        """记录报警"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO alerts (ticker, timestamp) VALUES (?, ?)', (ticker, datetime.now()))
            conn.commit()
        except Exception as e:
            logger.error(f"Database error in record_alert: {e}")

    def close(self):
        """关闭数据库连接（线程安全）"""
        if hasattr(self._local, 'conn') and self._local.conn:
            try:
                self._local.conn.close()
            except Exception as e:
                logger.error(f"Error closing database connection: {e}")
            finally:
                delattr(self._local, 'conn')
