"""Pytest configuration for Signal Hunter."""
import pytest
import asyncio
from typing import Generator
import os
import tempfile
import shutil

# Ensure test environment
os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
os.environ["TELEGRAM_CHAT_ID"] = "123456"
os.environ["DEEPSEEK_API_KEY"] = "test_key"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_db_path() -> Generator[str, None, None]:
    """Provide a temporary database path."""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_signals.db")
    yield db_path
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_tweet_data() -> dict:
    """Sample Twitter data for testing."""
    return {
        "full_text": "看好 $NVDA 财报，目标价上调到 $800 🚀",
        "url": "https://x.com/test/status/123456",
        "created_at": "2026-01-30 10:00:00"
    }


@pytest.fixture
def sample_signal_data() -> dict:
    """Sample signal data for testing."""
    return {
        "ticker": "NVDA",
        "signal_type": "BULLISH",
        "source_name": "TestBot",
        "raw_text": "看好 $NVDA 财报",
        "url": "https://test.com",
        "confidence": 0.8
    }
