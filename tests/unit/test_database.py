"""Unit tests for database module."""
import pytest
from datetime import datetime
from src.core.database import Database
from src.models.schemas import Signal, SignalType


class TestDatabase:
    """Test cases for Database operations."""

    def test_init_creates_tables(self, temp_db_path: str) -> None:
        """Test that initialization creates required tables."""
        import os
        os.environ["DB_PATH"] = temp_db_path
        
        db = Database()
        # Should not raise any errors
        assert db is not None
        db.close()

    def test_save_and_retrieve_signal(self, temp_db_path: str) -> None:
        """Test saving and retrieving a signal."""
        import os
        os.environ["DB_PATH"] = temp_db_path
        
        db = Database()
        
        signal = Signal(
            ticker="TEST",
            signal_type=SignalType.BULLISH,
            source_name="TestSource",
            raw_text="Test signal text",
            url="https://test.com",
            timestamp=datetime.now(),
            confidence=0.9
        )
        
        db.save_signal(signal)
        signals = db.get_recent_signals(hours=24)
        
        assert len(signals) >= 1
        assert any(s.ticker == "TEST" for s in signals)
        
        db.close()

    def test_duplicate_prevention(self, temp_db_path: str) -> None:
        """Test that duplicate signals are prevented."""
        import os
        os.environ["DB_PATH"] = temp_db_path
        
        db = Database()
        
        signal = Signal(
            ticker="DUP",
            signal_type=SignalType.NEUTRAL,
            source_name="DupSource",
            raw_text="Duplicate test",
            url="https://dup.com",
            timestamp=datetime.now(),
            confidence=0.5
        )
        
        # Save twice
        db.save_signal(signal)
        db.save_signal(signal)
        
        signals = db.get_recent_signals(hours=24)
        dup_signals = [s for s in signals if s.ticker == "DUP"]
        
        # Should only have one
        assert len(dup_signals) == 1
        
        db.close()

    def test_alert_deduplication(self, temp_db_path: str) -> None:
        """Test alert deduplication logic."""
        import os
        os.environ["DB_PATH"] = temp_db_path
        
        db = Database()
        
        # Record an alert
        db.record_alert("AAPL")
        
        # Should be alerted recently
        assert db.is_alerted_recently("AAPL", hours=24) is True
        
        # Different ticker should not be alerted
        assert db.is_alerted_recently("TSLA", hours=24) is False
        
        db.close()
