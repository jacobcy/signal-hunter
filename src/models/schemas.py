from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field

class PlatformType(str, Enum):
    TWITTER = "twitter"
    SUBSTACK = "substack"
    WECHAT = "wechat"
    GENERIC = "generic"

class Source(BaseModel):
    name: str
    url: HttpUrl
    platform: PlatformType = Field(default=PlatformType.GENERIC)
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
