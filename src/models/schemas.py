from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

class PlatformType(str, Enum):
    TWITTER = "twitter"
    SUBSTACK = "substack"
    WECHAT = "wechat"
    GENERIC = "generic"

class SourceCategory(str, Enum):
    """Source viewpoint category for diversity tracking."""
    MAINSTREAM = "mainstream"      # Popular consensus view
    CONTRARIAN = "contrarian"      # Often opposite to consensus
    INSTITUTIONAL = "institutional" # Professional/hedge fund view
    RETAIL = "retail"              # Individual investor view
    TECHNICAL = "technical"        # Chart/indicator based
    FUNDAMENTAL = "fundamental"    # Earnings/valuation based

class Source(BaseModel):
    name: str
    url: HttpUrl
    platform: PlatformType = Field(default=PlatformType.GENERIC)
    category: SourceCategory = Field(default=SourceCategory.MAINSTREAM)
    weight: float = Field(default=1.0, ge=0.0, le=10.0)
    last_checked: Optional[datetime] = None
    selector_title: Optional[str] = None
    selector_content: Optional[str] = None
    
    class Config:
        frozen = True

class SignalType(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

class Signal(BaseModel):
    ticker: str
    signal_type: SignalType
    source_name: str
    raw_text: str
    url: HttpUrl
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0)  # -1.0 to 1.0

class DiversityMetrics(BaseModel):
    """Metrics for detecting echo chambers and contrarian opportunities."""
    ticker: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Diversity metrics
    total_signals: int
    bullish_count: int
    bearish_count: int
    neutral_count: int
    
    # Calculated scores
    diversity_score: float = Field(ge=0.0, le=1.0)  # 0 = echo chamber, 1 = maximum diversity
    consensus_ratio: float = Field(ge=0.0, le=1.0)  # % of majority sentiment
    contrarian_index: float = Field(ge=-1.0, le=1.0)  # Weighted minority sentiment
    
    # Risk assessment
    is_echo_chamber: bool  # True if diversity_score < 0.3
    is_extreme_consensus: bool  # True if consensus_ratio > 0.8
    contrarian_opportunity: bool  # True if contrarian_index < -0.5 and minority view exists
    
    # Source breakdown
    mainstream_sentiment: Optional[SignalType]
    contrarian_sentiment: Optional[SignalType]
    cross_platform_divergence: bool  # Different sentiments across platforms

class MarketAlert(BaseModel):
    """Enhanced alert with diversity context."""
    alert_type: str  # "ECHO_CHAMBER", "CONTRARIAN_OPPORTUNITY", "EXTREME_CONSENSUS", "CROSS_PLATFORM_DIVERGENCE"
    ticker: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    headline: str
    description: str
    diversity_metrics: DiversityMetrics
    related_signals: List[Signal]
    timestamp: datetime = Field(default_factory=datetime.now)
