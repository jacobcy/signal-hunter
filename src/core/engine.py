import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from src.models.schemas import Source, PlatformType, Signal, MarketAlert, DiversityMetrics
from src.core.fetcher import FetcherFactory
from src.core.processor import SignalProcessor
from src.core.database import Database
from src.core.diversity_analyzer import DiversityAnalyzer
from src.utils.notifier import send_telegram_alert

class Engine:
    def __init__(self):
        self.sources: List[Source] = []
        self.current_batch_signals: List[Signal] = []
        self.diversity_analyzer: Optional[DiversityAnalyzer] = None

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
                
                # New format with category
                if len(clean_parts) >= 5:
                    category_str = clean_parts[3].lower()
                    weight = float(clean_parts[4])
                else:
                    category_str = "mainstream"  # Default
                    weight = float(clean_parts[3]) if len(clean_parts) > 3 else 1.0
                
                # Map strings to Enums
                try:
                    platform = PlatformType(platform_str)
                except ValueError:
                    platform = PlatformType.GENERIC
                
                try:
                    from src.models.schemas import SourceCategory
                    category = SourceCategory(category_str)
                except ValueError:
                    category = SourceCategory.MAINSTREAM
                
                source = Source(name=name, url=url, platform=platform, category=category, weight=weight)
                self.sources.append(source)
            
            # Initialize diversity analyzer with loaded sources
            self.diversity_analyzer = DiversityAnalyzer(self.sources)
            
            logger.info(f"📚 Loaded {len(self.sources)} sources from memory.")
            logger.info(f"🎯 Diversity analysis enabled with {len(self.sources)} sources.")
                
        except Exception as e:
            logger.error(f"❌ Failed to load sources: {e}")

    async def run_cycle(self):
        logger.info("🚀 Starting Signal Hunter Cycle...")
        logger.debug("Creating Database instance...")
        
        # Initialize async database
        db = Database()
        logger.debug("Initializing database tables...")
        await db.init_tables()
        logger.debug("Database initialized successfully")
        
        try:
            # 1. Fetch & Process
            tasks = []
            for source in self.sources:
                tasks.append(self._process_source(source))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Flatten results and save to DB (async)
            logger.debug(f"Processing {len(results)} fetch results...")
            for res in results:
                if isinstance(res, list):
                    for sig in res:
                        self.current_batch_signals.append(sig)
                        logger.debug(f"Saving signal: {sig.ticker} from {sig.source_name}")
                        saved = await db.save_signal(sig)
                        logger.debug(f"Signal saved: {saved}")
                elif isinstance(res, Exception):
                    logger.error(f"Fetch error: {res}")
            
            # 2. Diversity-Aware Signal Analysis (Anti-Echo Chamber)
            alert_count = await self._analyze_with_diversity(db)
            
            if alert_count == 0:
                logger.info("✅ No significant signals found (diversity analysis complete).")
            
            logger.info("🏁 Cycle complete.")
        except Exception as e:
            logger.exception(f"Cycle failed: {e}")
            raise
        finally:
            await db.close()

    async def _process_source(self, source: Source) -> List[Signal]:
        try:
            adapter = FetcherFactory.get_adapter(source)
            raw_data = await adapter.fetch()
            signals = SignalProcessor.process(source, raw_data)
            return signals
        except Exception as e:
            logger.error(f"💥 Error processing {source.name}: {e}")
            return []

    async def _analyze_with_diversity(self, db) -> int:
        """
        Analyze signals with diversity metrics to prevent echo chamber amplification.
        
        New Logic:
        - Echo Chamber Alert: Low diversity + high consensus (DANGER)
        - Contrarian Opportunity: Strong minority view with conviction (OPPORTUNITY)
        - Extreme Consensus: >80% agreement (REVERSAL WARNING)
        - Traditional Resonance: Only alert if diversity > 0.3
        
        Returns number of alerts sent.
        """
        if not self.diversity_analyzer:
            logger.warning("Diversity analyzer not initialized, falling back to basic resonance.")
            return await self._legacy_resonance_check(db)
        
        # Load signals from DB (24h window)
        recent_signals = await db.get_recent_signals(hours=24)
        
        # Group by ticker
        ticker_signals: Dict[str, List[Signal]] = {}
        for sig in recent_signals:
            if sig.ticker not in ticker_signals:
                ticker_signals[sig.ticker] = []
            ticker_signals[sig.ticker].append(sig)
        
        alerts_sent = 0
        
        for ticker, signals in ticker_signals.items():
            # Check if already alerted
            is_alerted = await db.is_alerted_recently(ticker)
            if is_alerted:
                logger.debug(f"🤫 Suppressing alert for {ticker} (already sent)")
                continue
            
            # Analyze diversity metrics
            metrics = self.diversity_analyzer.analyze(ticker, signals)
            
            # Route to appropriate alert type based on diversity context
            if metrics.is_extreme_consensus:
                # EXTREME RISK: Everyone agrees - reversal likely
                await self._send_extreme_consensus_alert(ticker, signals, metrics)
                await db.record_alert(ticker)
                alerts_sent += 1
                
            elif metrics.is_echo_chamber:
                # ECHO CHAMBER: Low diversity, herd mentality
                await self._send_echo_chamber_alert(ticker, signals, metrics)
                await db.record_alert(ticker)
                alerts_sent += 1
                
            elif metrics.contrarian_opportunity:
                # CONTRARIAN OPPORTUNITY: Strong minority view
                await self._send_contrarian_alert(ticker, signals, metrics)
                await db.record_alert(ticker)
                alerts_sent += 1
                
            elif metrics.cross_platform_divergence:
                # PLATFORM DIVERGENCE: Different platforms disagree
                await self._send_divergence_alert(ticker, signals, metrics)
                await db.record_alert(ticker)
                alerts_sent += 1
                
            elif metrics.diversity_score >= 0.3 and len(set(s.source_name for s in signals)) >= 2:
                # HEALTHY RESONANCE: Diverse sources agreeing (old logic, but stricter)
                await self._send_healthy_resonance_alert(ticker, signals, metrics)
                await db.record_alert(ticker)
                alerts_sent += 1
            else:
                logger.debug(f"ℹ️ {ticker}: No significant pattern (diversity: {metrics.diversity_score:.2f})")
        
        return alerts_sent
    
    async def _send_extreme_consensus_alert(self, ticker: str, signals: List[Signal], metrics: DiversityMetrics):
        """Alert when >80% consensus - reversal warning."""
        majority = "BULLISH" if metrics.bullish_count > metrics.bearish_count else "BEARISH"
        
        msg = f"🚨 *EXTREME CONSENSUS RISK: {ticker}*\n"
        msg += f"⚠️ {metrics.consensus_ratio*100:.0f}% {majority} - Reversal Likely!\n"
        msg += "-------------------\n"
        msg += f"📊 Diversity Score: {metrics.diversity_score:.2f} (Extreme)\n"
        msg += f"🎯 Signals: {metrics.total_signals} total\n"
        msg += f"   🟢 Bullish: {metrics.bullish_count}\n"
        msg += f"   🔴 Bearish: {metrics.bearish_count}\n"
        msg += "-------------------\n"
        msg += "💡 *Insight*: When everyone agrees, everyone is wrong.\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        await send_telegram_alert(msg)
        logger.warning(f"🚨 Extreme consensus alert sent for {ticker}")
    
    async def _send_echo_chamber_alert(self, ticker: str, signals: List[Signal], metrics: DiversityMetrics):
        """Alert for echo chamber detection."""
        majority = "BULLISH" if metrics.bullish_count > metrics.bearish_count else "BEARISH"
        
        msg = f"📢 *ECHO CHAMBER WARNING: {ticker}*\n"
        msg += f"⚠️ Herd mentality detected ({metrics.consensus_ratio*100:.0f}% {majority})\n"
        msg += "-------------------\n"
        msg += f"📊 Diversity Score: {metrics.diversity_score:.2f} (Low)\n"
        msg += f"🎯 Sources agree too much - limited perspective\n"
        msg += "-------------------\n"
        msg += "💡 *Insight*: Diversify your information diet.\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        await send_telegram_alert(msg)
        logger.warning(f"📢 Echo chamber alert sent for {ticker}")
    
    async def _send_contrarian_alert(self, ticker: str, signals: List[Signal], metrics: DiversityMetrics):
        """Alert for contrarian opportunity."""
        # Find minority signals
        if metrics.bullish_count < metrics.bearish_count:
            minority_type = "BULLISH"
            minority_signals = [s for s in signals if s.signal_type.value == "BULLISH"]
        else:
            minority_type = "BEARISH"
            minority_signals = [s for s in signals if s.signal_type.value == "BEARISH"]
        
        msg = f"🎯 *CONTRARIAN OPPORTUNITY: {ticker}*\n"
        msg += f"💎 Strong {minority_type} view in {metrics.consensus_ratio*100:.0f}% opposite market\n"
        msg += "-------------------\n"
        msg += f"📊 Contrarian Index: {metrics.contrarian_index:.2f}\n"
        msg += f"🎯 Minority View:\n"
        for s in minority_signals[:2]:
            msg += f"   • {s.source_name}: {s.raw_text[:40]}...\n"
        msg += "-------------------\n"
        msg += "💡 *Insight*: The crowd is wrong at extremes.\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        await send_telegram_alert(msg)
        logger.info(f"🎯 Contrarian alert sent for {ticker}")
    
    async def _send_divergence_alert(self, ticker: str, signals: List[Signal], metrics: DiversityMetrics):
        """Alert for cross-platform sentiment divergence."""
        msg = f"📊 *PLATFORM DIVERGENCE: {ticker}*\n"
        msg += "⚠️ Different platforms show different sentiments\n"
        msg += "-------------------\n"
        msg += f"🎯 Mainstream: {metrics.mainstream_sentiment.value if metrics.mainstream_sentiment else 'N/A'}\n"
        msg += f"🎯 Contrarian: {metrics.contrarian_sentiment.value if metrics.contrarian_sentiment else 'N/A'}\n"
        msg += "-------------------\n"
        msg += "💡 *Insight*: Smart money vs retail divergence.\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        await send_telegram_alert(msg)
        logger.info(f"📊 Divergence alert sent for {ticker}")
    
    async def _send_healthy_resonance_alert(self, ticker: str, signals: List[Signal], metrics: DiversityMetrics):
        """Alert for healthy resonance (diverse sources agreeing)."""
        msg = f"✅ *HEALTHY RESONANCE: {ticker}*\n"
        msg += f"📊 Diverse sources reaching consensus\n"
        msg += "-------------------\n"
        msg += f"🎯 Diversity Score: {metrics.diversity_score:.2f} (Good)\n"
        msg += f"📈 Consensus: {metrics.consensus_ratio*100:.0f}%\n"
        for s in signals[:3]:
            icon = "🟢" if s.signal_type.value == "BULLISH" else "🔴" if s.signal_type.value == "BEARISH" else "⚪️"
            msg += f"{icon} {s.source_name}\n"
        msg += "-------------------\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        await send_telegram_alert(msg)
        logger.info(f"✅ Healthy resonance alert sent for {ticker}")
    
    async def _legacy_resonance_check(self, db) -> int:
        """Fallback to old logic if diversity analyzer unavailable."""
        recent_signals = await db.get_recent_signals(hours=24)
        ticker_counts: Dict[str, List[Signal]] = {}
        
        for sig in recent_signals:
            if sig.ticker not in ticker_counts:
                ticker_counts[sig.ticker] = []
            ticker_counts[sig.ticker].append(sig)
        
        alerts_sent = 0
        for ticker, sigs in ticker_counts.items():
            is_alerted = await db.is_alerted_recently(ticker)
            if is_alerted:
                continue
            
            sources_involved = set(s.source_name for s in sigs)
            if len(sources_involved) >= 2:
                msg = f"🚨 *信号共振: {ticker}*\n"
                for s in sigs[:3]:
                    icon = "🟢" if s.signal_type.value == "BULLISH" else "🔴"
                    msg += f"{icon} {s.source_name}\n"
                await send_telegram_alert(msg)
                await db.record_alert(ticker)
                alerts_sent += 1
        
        return alerts_sent
