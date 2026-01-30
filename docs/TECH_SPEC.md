# Tech Specification

## 1. Technology Stack
*   **Runtime**: Python 3.12+
*   **Web Client**: `httpx` (Async), `playwright` (Fallback)
*   **Data Validation**: `pydantic` v2
*   **CLI**: `typer`
*   **Logging**: `loguru`
*   **Testing**: `pytest`, `pytest-asyncio`
*   **Linting/Formatting**: `ruff`

## 2. Architecture Diagram (Textual)
```mermaid
graph TD
    A[Scheduler/CLI] -->|Trigger| B(Engine)
    B -->|Read Sources| C[Memory/DB]
    B -->|Dispatch Tasks| D{Platform Router}
    D -->|twitter.com| E[TwitterAdapter]
    D -->|substack.com| F[SubstackAdapter]
    D -->|Generic| G[BaseWebAdapter]
    E & F & G -->|Fetch Strategy| H{Fetcher (HTTPX/Playwright)}
    H -->|Raw Content| I[Parser Factory]
    I -->|Standardized Text| J[Signal Extractor]
    J -->|Signal Objects| K[Resonance Detector]
    K -->|Alerts| L[Telegram Notifier]
```

## 3. Data Models (Preliminary)

### 3.1 Source
```python
class PlatformType(str, Enum):
    TWITTER = "twitter"
    SUBSTACK = "substack"
    WECHAT = "wechat"
    GENERIC = "generic"

class Source(BaseModel):
    name: str
    url: HttpUrl
    platform: PlatformType
    weight: float = 1.0
    # ...
```

### 3.2 Signal
```python
class Signal(BaseModel):
    ticker: str          # e.g., "NVDA"
    sentiment: Literal["BULLISH", "BEARISH", "NEUTRAL"]
    source_id: str
    raw_text: str
    timestamp: datetime
```

## 4. Error Handling & Self-Healing
*   **Level 1 (Network)**: `httpx.ConnectError` -> Retry 3 times with backoff.
*   **Level 2 (Parsing)**: `AttributeError` (selector not found) -> Trigger `Snapshot` -> Alert Admin -> Fallback to visual LLM extraction (future).
*   **Level 3 (System)**: Unhandled Exception -> Log to file + Telegram Alert -> Safe Exit.

## 5. Development Standards
*   **Commits**: `feat: add fetcher`, `fix: parser logic`, `docs: update PRD`.
*   **Async**: All I/O bound operations must be `async def`.
*   **Type Hints**: 100% coverage required. No `Any` unless strictly necessary.
