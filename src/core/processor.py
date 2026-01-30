import re
from typing import List
from datetime import datetime
from loguru import logger
from src.models.schemas import Source, Signal, SignalType

class SignalProcessor:
    """
    Zero-Token Signal Extractor.
    Uses Regex and Keyword Matching to identify trading signals.
    """
    
    # 基础词库 (扩充需谨慎，避免误报)
    KEYWORDS_BULLISH = [
        r"buy", r"long", r"call", r"breakout", r"moon", r"bull",
        r"买入", r"看多", r"加仓", r"突破", r"目标价", r"起飞"
    ]
    
    KEYWORDS_BEARISH = [
        r"sell", r"short", r"put", r"breakdown", r"dump", r"bear",
        r"卖出", r"看空", r"减仓", r"跌破", r"止损", r"崩盘"
    ]
    
    # 股票代码正则: $NVDA, AAPL, 600519
    # 1. $XYZ (US Crypto style)
    # 2. 6 digits (CN style)
    REGEX_TICKER = r"(\$[A-Z]{2,5})|(\b[A-Z]{2,5}\b)|(\b\d{6}\b)"

    @staticmethod
    def process(source: Source, raw_data: List[dict]) -> List[Signal]:
        signals = []
        
        for item in raw_data:
            text = item.get("full_text", "") or item.get("text", "")
            if not text:
                continue
                
            # 1. Ticker Extraction
            tickers = set()
            matches = re.finditer(SignalProcessor.REGEX_TICKER, text)
            for m in matches:
                # Cleaning: remove $ if present
                t = m.group(0).replace("$", "").upper()
                # Filter out common false positives (e.g. "THE", "AND" if regex is too loose)
                # Augmented Blacklist based on test run
                blacklist = [
                    "THE", "AND", "FOR", "AI", "CPU", "GPU", 
                    "API", "APP", "GUI", "CLI", "GPT", "LLM", "GLM", "UNIX", "PDF", "SDK", "URL", "HTTP", "WWW", "COM"
                ]
                if t not in blacklist: 
                    tickers.add(t)
            
            if not tickers:
                continue

            # 2. Sentiment Analysis (Keyword Counting)
            score = 0
            text_lower = text.lower()
            
            for kw in SignalProcessor.KEYWORDS_BULLISH:
                if re.search(kw, text_lower):
                    score += 1
            
            for kw in SignalProcessor.KEYWORDS_BEARISH:
                if re.search(kw, text_lower):
                    score -= 1
            
            # 3. Determine Signal Type
            if score > 0:
                sig_type = SignalType.BULLISH
            elif score < 0:
                sig_type = SignalType.BEARISH
            else:
                sig_type = SignalType.NEUTRAL
                
            # Only generate signals for detected tickers if sentiment is non-neutral
            # (Or maybe we want neutral for information? Let's keep neutral for now but maybe filter later)
            
            for ticker in tickers:
                # Context check: simple proximity check could be added here
                # For now, if ticker and sentiment exist in same text, we assume linkage.
                
                signal = Signal(
                    ticker=ticker,
                    signal_type=sig_type,
                    source_name=source.name,
                    raw_text=text[:200] + "...", # Truncate for storage
                    url=item.get("url") or source.url,
                    confidence=0.6 + (0.1 * abs(score)) # Basic confidence logic
                )
                signals.append(signal)
                logger.debug(f"🔍 Detected Signal: {ticker} {sig_type} from {source.name}")

        return signals
