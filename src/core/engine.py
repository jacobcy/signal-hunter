import asyncio
from typing import List, Dict
from datetime import datetime
from loguru import logger
from src.models.schemas import Source, PlatformType, Signal
from src.core.fetcher import FetcherFactory
from src.core.processor import SignalProcessor
from src.core.database import Database
from src.utils.notifier import send_telegram_alert

class Engine:
    def __init__(self):
        self.sources: List[Source] = []
        # Signals list is now transient for current batch, history is in DB
        self.current_batch_signals: List[Signal] = [] 
        # 注意：不在 __init__ 中创建 Database 实例，避免异步环境中的连接问题

    def load_sources_from_memory(self):
        """
        Parses memory/bloggers.md to load sources.
        Format expected: Name | URL | Platform | Weight
        """
        try:
            with open("memory/bloggers.md", "r") as f:
                lines = f.readlines()
            
            for line in lines:
                if "|" not in line or line.strip().startswith("| Name") or "---" in line: # Skip header and separator
                    continue
                
                parts = [p.strip() for p in line.split("|")]
                # Expected: [Name, URL, Platform, Weight] or [Empty, Name, URL, Platform, Weight, Empty] depending on table format
                
                # Robust parsing for Markdown tables
                clean_parts = [p for p in parts if p]
                if len(clean_parts) < 3:
                    continue
                    
                name = clean_parts[0]
                url = clean_parts[1]
                platform_str = clean_parts[2].lower()
                weight = float(clean_parts[3]) if len(clean_parts) > 3 else 1.0
                
                # Map string to Enum
                try:
                    platform = PlatformType(platform_str)
                except ValueError:
                    platform = PlatformType.GENERIC
                
                source = Source(name=name, url=url, platform=platform, weight=weight)
                self.sources.append(source)
            
            logger.info(f"📚 Loaded {len(self.sources)} sources from memory.")
                
        except Exception as e:
            logger.error(f"❌ Failed to load sources: {e}")

    async def run_cycle(self):
        logger.info("🚀 Starting Signal Hunter Cycle...")
        
        # 每次循环创建新的数据库连接
        db = Database()
        try:
            # 1. Fetch & Process
            tasks = []
            for source in self.sources:
                tasks.append(self._process_source(source))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Flatten results and save to DB
            for res in results:
                if isinstance(res, list):
                    for sig in res:
                        self.current_batch_signals.append(sig)
                        db.save_signal(sig)
            
            # 2. Resonance Detection (using DB history)
            alert_count = await self._detect_resonance_with_db(db)
            
            if alert_count == 0:
                logger.info("✅ No new resonance found.")
            
            logger.info("🏁 Cycle complete.")
        finally:
            db.close()

    async def _process_source(self, source: Source) -> List[Signal]:
        try:
            adapter = FetcherFactory.get_adapter(source)
            raw_data = await adapter.fetch()
            signals = SignalProcessor.process(source, raw_data)
            return signals
        except Exception as e:
            logger.error(f"💥 Error processing {source.name}: {e}")
            return []

    async def _detect_resonance_with_db(self, db) -> int:
        """
        Check for resonance: >= 2 sources mentioning the same ticker in the LAST 24 HOURS.
        Returns number of alerts sent.
        """
        # Load signals from DB (24h window)
        recent_signals = db.get_recent_signals(hours=24)
        
        ticker_counts: Dict[str, List[Signal]] = {}
        alerts_sent = 0
        
        for sig in recent_signals:
            if sig.ticker not in ticker_counts:
                ticker_counts[sig.ticker] = []
            ticker_counts[sig.ticker].append(sig)
            
        # Check threshold
        for ticker, sigs in ticker_counts.items():
            # Check if we already alerted this ticker recently
            if db.is_alerted_recently(ticker):
                logger.debug(f"🤫 Suppressing alert for {ticker} (already sent in last 24h)")
                continue

            sources_involved = set(s.source_name for s in sigs)
            
            if len(sources_involved) >= 2:
                logger.warning(f"🚨 RESONANCE DETECTED FOR {ticker}!")
                
                # Format Alert
                msg = f"🚨 *信号共振报警: {ticker}*\n"
                msg += "-------------------\n"
                for s in sigs:
                    icon = "🟢" if "BULLISH" in s.signal_type else "🔴" if "BEARISH" in s.signal_type else "⚪️"
                    # Format time as relative or short
                    time_str = s.timestamp.strftime('%H:%M')
                    msg += f"{icon} *{s.source_name}* ({time_str}): {s.signal_type}\n"
                    msg += f"   \"{s.raw_text[:50]}...\"\n"
                msg += "-------------------\n"
                msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                await send_telegram_alert(msg)
                db.record_alert(ticker) # Record alert to prevent dupes
                alerts_sent += 1
            else:
                logger.debug(f"ℹ️ {ticker} mentioned by {len(sources_involved)} source(s). No resonance.")
        
        return alerts_sent
