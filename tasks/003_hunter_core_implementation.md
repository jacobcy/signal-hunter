# Task 003: Implement Layer 2 Capability (The Hunter Core)

## 🎯 Objective
Implement **Layer 2** of the Trinity Framework: **The Hunter (Info Scout)**.
Refactor the existing ad-hoc "AI Briefing" logic into a configurable, generic information gathering engine.

## 🤖 Assigned Roles (Parallel Execution)
- **Dev (0xCAFE):** Implement the `InfoScout` class and configuration loader.
- **QA (Bugsy):** Verify the scout can fetch and parse data from mock sources.
- **Researcher (Birdie):** Define the initial configuration (topics/sources) for AI & Crypto.

## 📋 Requirements (Dev)

### 1. Structure
- Directory: `src/hunter/`
- Config: `config/hunter.yaml` (Define topics, keywords, sources)

### 2. Core Logic (`src/hunter/scout.py`)
- **Class `InfoScout`**:
  - `__init__(config_path)`: Load configuration.
  - `hunt(topic)`: Execute search/fetch for a specific topic.
  - `generate_brief(data)`: Summarize findings (using LLM or simple formatting).
- **Sources (Modular):**
  - Adapter pattern for sources: `BraveSearch`, `Twitter/X` (via Bird tool), `RSS` (via Miniflux or raw).
  - *Start with `BraveSearch` and `Bird` (Twitter) as primary adapters.*

### 3. Configuration (`config/hunter.yaml`)
Example structure:
```yaml
topics:
  ai_daily:
    keywords: ["AI tools", "LLM news", "Python agents"]
    sources: ["brave", "twitter"]
    schedule: "daily"
  crypto_signals:
    keywords: ["Bitcoin breakout", "ETH upgrades", "Solana memecoin"]
    sources: ["twitter"]
    schedule: "hourly"
```

### 4. Output
- JSON structured data: `memory/daily/hunter_{topic}_{date}.json`
- Human readable summary: Returned string for Telegram broadcasting.

## 🧪 Verification (QA)
- Test config loading.
- Mock the `web_search` and `bird` tool calls (do not actually spend tokens/credits in unit tests).
- Verify JSON output format.

## 🚀 Execution Plan
1.  **Dev** implements `src/hunter/` and `config/hunter.yaml`.
2.  **QA** writes `tests/test_hunter.py`.
3.  **Dev** creates a CLI entry point: `python -m src.hunter.main --topic ai_daily`.
