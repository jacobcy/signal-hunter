# Signal Hunter v0.3.0 - Anti-Echo Architecture Design

## Problem Diagnosis (From Zhihu Article)

Current v0.2.0 architecture has critical flaws:

1. **Echo Chamber Amplification**: "Resonance" (>=2 sources agreeing) rewards confirmation bias
2. **Homogeneous Source Risk**: Monitoring similar bloggers creates information silo
3. **No Contrarian View**: System ignores minority opinions that often predict reversals
4. **Extreme Consensus Blindness**: When ALL sources agree, risk is highest but system is silent

## New Architecture: Diversity-First Signal Processing

### Core Principle
> "The value of a signal is inversely proportional to its consensus level"

### New Metrics

| Metric | Description | Alert Trigger |
|--------|-------------|---------------|
| **Diversity Score** | (Bullish + Bearish) / Total | Score < 0.3 = Echo Chamber Warning |
| **Contrarian Index** | Weighted sentiment of minority views | Extreme values predict reversal |
| **Consensus Risk** | % of sources with same sentiment | >80% = Extreme Risk Alert |
| **Cross-Platform Spread** | Variance across Twitter/WeChat/Web | Low variance = Silo detected |

### New Processing Pipeline

```
Raw Signals
    ↓
[Sentiment Classifier] → Bullish / Bearish / Neutral
    ↓
[Diversity Analyzer] → Diversity Score, Contrarian Index
    ↓
[Consensus Detector] → Consensus Risk Level
    ↓
[Signal Ranker] → Weight = f(Diversity, Contrarian, Contrarian, Timeliness)
    ↓
[Alert Router] → Different alerts for different consensus levels
```

### Alert Types

1. **Diversity Alert**: "⚠️ Echo Chamber: 5/5 sources bullish on NVDA (Diversity Score: 0.0)"
2. **Contrarian Opportunity**: "🎯 Contrarian Signal: @BearishBob predicts TSLA crash while 90% are bullish"
3. **Consensus Risk**: "🚨 EXTREME RISK: 100% consensus on BTC - Historical reversal indicator"
4. **Cross-Platform Divergence**: "📊 Twitter bullish (80%) vs WeChat bearish (60%) on AAPL"

## Implementation Plan

### Phase 1: Data Model Extension
- Add Sentiment enum: BULLISH, BEARISH, NEUTRAL, CONTRARIAN
- Add DiversityMetrics model
- Add SourceCategory tags (Mainstream, Contrarian, Institutional, Retail)

### Phase 2: Diversity Analyzer Module
- Calculate real-time diversity scores
- Identify contrarian sources dynamically
- Track sentiment momentum shifts

### Phase 3: Smart Alert System
- Route different consensus levels to different alert channels
- Suppress echo-chamber "resonance" alerts
- Boost contrarian minority signals

### Phase 4: Source Quality Scoring
- Track accuracy of each source historically
- Weight contrarian sources higher when they are correct
- Detect and warn about deteriorating source quality

## Success Criteria

- [ ] System detects when >3 sources have identical sentiment
- [ ] Contrarian signals (minority view) get separate high-priority channel
- [ ] Diversity Score shown in every daily digest
- [ ] Extreme consensus (>80%) triggers risk warning, not buy signal
- [ ] Cross-platform sentiment divergence detected and reported
