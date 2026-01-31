"""
Diversity Analyzer - Anti-Echo Chamber Signal Processing

This module analyzes signal diversity to detect:
1. Echo chambers (low diversity, high consensus)
2. Contrarian opportunities (minority views with high conviction)
3. Extreme consensus risks (when everyone agrees, danger is near)
4. Cross-platform divergences (different platforms, different views)
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from loguru import logger

from src.models.schemas import Signal, SignalType, DiversityMetrics, Source, SourceCategory


class DiversityAnalyzer:
    """Analyzes signal diversity to prevent echo chamber amplification."""
    
    # Thresholds
    ECHO_CHAMBER_THRESHOLD = 0.3  # Diversity score below this = echo chamber
    EXTREME_CONSENSUS_THRESHOLD = 0.8  # Consensus above this = extreme risk
    CONTRARIAN_OPPORTUNITY_THRESHOLD = -0.5  # Contrarian index below this = opportunity
    
    def __init__(self, sources: List[Source]):
        self.sources = {s.name: s for s in sources}
    
    def analyze(self, ticker: str, signals: List[Signal]) -> DiversityMetrics:
        """
        Analyze diversity metrics for a ticker based on recent signals.
        
        Args:
            ticker: The stock/crypto ticker
            signals: List of recent signals for this ticker
            
        Returns:
            DiversityMetrics with comprehensive diversity analysis
        """
        if not signals:
            return self._empty_metrics(ticker)
        
        # Count sentiments
        total = len(signals)
        bullish = sum(1 for s in signals if s.signal_type == SignalType.BULLISH)
        bearish = sum(1 for s in signals if s.signal_type == SignalType.BEARISH)
        neutral = sum(1 for s in signals if s.signal_type == SignalType.NEUTRAL)
        
        # Calculate diversity score (Shannon entropy normalized)
        diversity_score = self._calculate_diversity_score(bullish, bearish, neutral, total)
        
        # Calculate consensus ratio
        max_sentiment = max(bullish, bearish, neutral)
        consensus_ratio = max_sentiment / total if total > 0 else 0
        
        # Calculate contrarian index (weighted minority view)
        contrarian_index = self._calculate_contrarian_index(signals, bullish, bearish, total)
        
        # Determine risk flags
        is_echo_chamber = diversity_score < self.ECHO_CHAMBER_THRESHOLD
        is_extreme_consensus = consensus_ratio > self.EXTREME_CONSENSUS_THRESHOLD
        contrarian_opportunity = (
            contrarian_index < self.CONTRARIAN_OPPORTUNITY_THRESHOLD and 
            min(bullish, bearish) > 0  # Must have minority view
        )
        
        # Analyze by source category
        mainstream_sentiment = self._get_category_sentiment(signals, SourceCategory.MAINSTREAM)
        contrarian_sentiment = self._get_category_sentiment(signals, SourceCategory.CONTRARIAN)
        
        # Check cross-platform divergence
        cross_platform_divergence = self._detect_platform_divergence(signals)
        
        return DiversityMetrics(
            ticker=ticker,
            timestamp=datetime.now(),
            total_signals=total,
            bullish_count=bullish,
            bearish_count=bearish,
            neutral_count=neutral,
            diversity_score=diversity_score,
            consensus_ratio=consensus_ratio,
            contrarian_index=contrarian_index,
            is_echo_chamber=is_echo_chamber,
            is_extreme_consensus=is_extreme_consensus,
            contrarian_opportunity=contrarian_opportunity,
            mainstream_sentiment=mainstream_sentiment,
            contrarian_sentiment=contrarian_sentiment,
            cross_platform_divergence=cross_platform_divergence
        )
    
    def _calculate_diversity_score(self, bullish: int, bearish: int, neutral: int, total: int) -> float:
        """Calculate normalized Shannon entropy as diversity score."""
        if total == 0:
            return 0.0
        
        proportions = [bullish / total, bearish / total, neutral / total]
        proportions = [p for p in proportions if p > 0]  # Remove zeros for log
        
        import math
        entropy = -sum(p * math.log2(p) for p in proportions)
        max_entropy = math.log2(3)  # Maximum entropy for 3 categories
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _calculate_contrarian_index(self, signals: List[Signal], bullish: int, bearish: int, total: int) -> float:
        """
        Calculate contrarian index: weighted sentiment of minority view.
        Negative = contrarian bearish (opportunity to buy)
        Positive = contrarian bullish (opportunity to sell/short)
        """
        if total == 0 or bullish == bearish:
            return 0.0
        
        # Identify minority view
        if bullish > bearish:
            minority_signals = [s for s in signals if s.signal_type == SignalType.BEARISH]
            direction = -1  # Bearish minority = potential buy opportunity
        else:
            minority_signals = [s for s in signals if s.signal_type == SignalType.BULLISH]
            direction = 1  # Bullish minority = potential sell opportunity
        
        if not minority_signals:
            return 0.0
        
        # Weight by confidence and source category
        weighted_sum = 0.0
        weight_total = 0.0
        
        for signal in minority_signals:
            source = self.sources.get(signal.source_name)
            category_weight = 1.5 if source and source.category == SourceCategory.CONTRARIAN else 1.0
            combined_weight = signal.confidence * category_weight
            
            weighted_sum += combined_weight
            weight_total += combined_weight
        
        avg_confidence = weighted_sum / weight_total if weight_total > 0 else 0.0
        return direction * avg_confidence
    
    def _get_category_sentiment(self, signals: List[Signal], category: SourceCategory) -> Optional[SignalType]:
        """Get dominant sentiment for a specific source category."""
        category_signals = [
            s for s in signals 
            if self.sources.get(s.source_name) and self.sources[s.source_name].category == category
        ]
        
        if not category_signals:
            return None
        
        bullish = sum(1 for s in category_signals if s.signal_type == SignalType.BULLISH)
        bearish = sum(1 for s in category_signals if s.signal_type == SignalType.BEARISH)
        neutral = sum(1 for s in category_signals if s.signal_type == SignalType.NEUTRAL)
        
        max_count = max(bullish, bearish, neutral)
        if bullish == max_count:
            return SignalType.BULLISH
        elif bearish == max_count:
            return SignalType.BEARISH
        else:
            return SignalType.NEUTRAL
    
    def _detect_platform_divergence(self, signals: List[Signal]) -> bool:
        """Detect if different platforms have different sentiments."""
        platform_sentiments = defaultdict(list)
        
        for signal in signals:
            source = self.sources.get(signal.source_name)
            if source:
                platform_sentiments[source.platform].append(signal.signal_type)
        
        if len(platform_sentiments) < 2:
            return False
        
        # Check if dominant sentiment differs across platforms
        platform_dominant = {}
        for platform, sentiments in platform_sentiments.items():
            bullish = sentiments.count(SignalType.BULLISH)
            bearish = sentiments.count(SignalType.BEARISH)
            if bullish > bearish:
                platform_dominant[platform] = SignalType.BULLISH
            elif bearish > bullish:
                platform_dominant[platform] = SignalType.BEARISH
            else:
                platform_dominant[platform] = SignalType.NEUTRAL
        
        # Check for divergence
        sentiments = list(platform_dominant.values())
        return len(set(sentiments)) > 1
    
    def _empty_metrics(self, ticker: str) -> DiversityMetrics:
        """Return empty metrics when no signals."""
        return DiversityMetrics(
            ticker=ticker,
            timestamp=datetime.now(),
            total_signals=0,
            bullish_count=0,
            bearish_count=0,
            neutral_count=0,
            diversity_score=0.0,
            consensus_ratio=0.0,
            contrarian_index=0.0,
            is_echo_chamber=False,
            is_extreme_consensus=False,
            contrarian_opportunity=False,
            mainstream_sentiment=None,
            contrarian_sentiment=None,
            cross_platform_divergence=False
        )
    
    def rank_signals(self, signals: List[Signal], metrics: DiversityMetrics) -> List[Signal]:
        """
        Re-rank signals based on diversity context.
        
        In echo chambers: Boost contrarian signals
        In diverse markets: Weight by confidence
        In extreme consensus: Flag all as high risk
        """
        if metrics.is_echo_chamber:
            # Boost minority view signals
            majority = SignalType.BULLISH if metrics.bullish_count > metrics.bearish_count else SignalType.BEARISH
            ranked = sorted(signals, key=lambda s: (
                0 if s.signal_type != majority else 1,  # Minority first
                -s.confidence  # Then by confidence
            ))
        elif metrics.contrarian_opportunity:
            # Boost contrarian signals
            ranked = sorted(signals, key=lambda s: (
                s.sentiment_score  # Most negative (bearish) or positive (bullish) first
            ), reverse=True)
        else:
            # Normal ranking by confidence
            ranked = sorted(signals, key=lambda s: -s.confidence)
        
        return ranked
