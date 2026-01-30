"""Unit tests for signal processor module."""
import pytest
from src.core.processor import SignalProcessor
from src.models.schemas import Source, Signal, SignalType, PlatformType


class TestSignalProcessor:
    """Test cases for SignalProcessor."""

    def test_extract_ticker_with_dollar_sign(self) -> None:
        """Test extracting ticker with $ prefix."""
        text = "看好 $NVDA 财报"
        tickers = SignalProcessor._extract_tickers(text)
        assert "NVDA" in tickers

    def test_extract_ticker_without_dollar_sign(self) -> None:
        """Test extracting ticker without $ prefix."""
        text = "AAPL 今天表现不错"
        tickers = SignalProcessor._extract_tickers(text)
        assert "AAPL" in tickers

    def test_extract_chinese_stock_code(self) -> None:
        """Test extracting Chinese stock code (6 digits)."""
        text = "600519 茅台业绩超预期"
        tickers = SignalProcessor._extract_tickers(text)
        assert "600519" in tickers

    def test_blacklist_filter(self) -> None:
        """Test that blacklist words are filtered out."""
        text = "使用 API 调用 GPT 模型"
        tickers = SignalProcessor._extract_tickers(text)
        # API and GPT should be in blacklist
        assert "API" not in tickers
        assert "GPT" not in tickers

    def test_sentiment_bullish(self) -> None:
        """Test bullish sentiment detection."""
        text = "强烈看好，买入机会！"
        score = SignalProcessor._calculate_sentiment(text)
        assert score > 0

    def test_sentiment_bearish(self) -> None:
        """Test bearish sentiment detection."""
        text = "看空，准备卖出止损"
        score = SignalProcessor._calculate_sentiment(text)
        assert score < 0

    def test_sentiment_neutral(self) -> None:
        """Test neutral sentiment detection."""
        text = "今天天气不错"
        score = SignalProcessor._calculate_sentiment(text)
        assert score == 0

    def test_process_empty_data(self) -> None:
        """Test processing empty data."""
        source = Source(name="Test", url="https://test.com", platform=PlatformType.GENERIC)
        result = SignalProcessor.process(source, [])
        assert result == []

    def test_process_valid_signal(self) -> None:
        """Test processing valid signal data."""
        source = Source(name="Test", url="https://test.com", platform=PlatformType.GENERIC)
        raw_data = [{
            "full_text": "看好 $TSLA，目标价 $300",
            "url": "https://test.com/1",
            "created_at": "2026-01-30 10:00:00"
        }]
        
        signals = SignalProcessor.process(source, raw_data)
        
        assert len(signals) > 0
        assert signals[0].ticker == "TSLA"
        assert signals[0].source_name == "Test"
