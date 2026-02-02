# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Signal Hunter is an async Python-based financial intelligence system that monitors financial KOLs (Key Opinion Leaders) across social media platforms to extract trading signals and generate market intelligence reports.

## Common Development Commands

### Installation & Setup
```bash
# Install Python 3.12+ dependencies
pip install -e .
pip install -e ".[dev]"  # Include dev dependencies

# Install Playwright browsers for scraping
playwright install chromium

# Install pre-commit hooks
pre-commit install
```

### Running the System
```bash
# Run main signal hunter engine
python src/main.py run

# Run Telegram bot (runs continuously)
python src/bot_runner.py

# Test Twitter/X adapter with specific handle
python src/main.py test-bird vista8

# Run scheduled tasks programmatically
python src/scheduler.py
```

### Testing & Quality Checks
```bash
# Run all tests with coverage
./run-tests.sh

# Run specific test types
./run-tests.sh unit
./run-tests.sh integration

# Manual test commands
pytest tests/ -v --cov=src --cov-report=term-missing

# Code quality checks
ruff check src/
ruff format src/
mypy src/ --ignore-missing-imports

# Pre-commit checks (runs automatically on commit)
pre-commit run --all-files
```

## Architecture Overview

### Core Pipeline Flow
1. **Engine** (`src/core/engine.py`): Central orchestrator that manages the entire signal processing pipeline
2. **Fetcher Factory** (`src/core/fetcher.py`): Platform-specific adapters (Twitter/X, WeChat, etc.) fetch content
3. **Signal Processor** (`src/core/processor.py`): Extracts signals from content using NLP/keyword analysis
4. **Diversity Analyzer** (`src/core/diversity_analyzer.py`): Detects echo chambers and contrarian opportunities
5. **Database** (`src/core/database.py`): SQLite-based async storage for signals and diversity metrics
6. **Notifier** (`src/utils/notifier.py`): Telegram alerts for significant market signals

### Key Data Models
- **Signal**: Individual trading signal with ticker, direction, confidence, sentiment score
- **DiversityMetrics**: Analytics for detecting market consensus patterns across sources
- **MarketAlert**: High-priority alerts for echo chambers, contrarian opportunities, etc.
- **Source**: Configured KOL sources with categories (mainstream/contrarian/institutional/technical/etc)

### Source Management
Sources are configured in `memory/bloggers.md` with format: `| Name | URL | Platform | Category | Weight |`
- Categories: mainstream, contrarian, institutional, retail, technical, fundamental
- Weights: 1.0-10.0 scale for signal importance

### Configuration Files
- `config.yaml`: Bot tokens, scanning intervals, keyword weights
- `pyproject.toml`: Python dependencies, tool configurations (ruff, pytest, mypy)
- `.env`: Sensitive credentials (loaded via python-dotenv)

### Telegram Bot Commands
- `/scan` - Force immediate scan of all sources
- `/digest` - Generate 24h activity summary
- `/status` - Check system health and counts
- `/add <Name> <URL>` - Add new source interactively

## Key Implementation Patterns

### Async/Await Everywhere
The entire system uses asyncio. Database operations, API calls, and content fetching are all async.

### Type Safety
Pydantic models with strict validation. MyPy configured for strict type checking.

### Testing
- Unit tests for individual components
- Integration tests for end-to-end workflows
- pytest-asyncio for async test support
- conftest.py provides shared test fixtures

### Error Handling
- Uses loguru for structured logging with rotation
- Graceful degradation when sources fail
- Return_exceptions=True in gather() for parallel processing

### Signal Processing Logic
Signals are extracted using:
1. Blacklist filtering (tech terms to avoid false positives)
2. Keyword matching (bullish/bearish terms with weights)
3. Confidence scoring based on keyword density and source reliability
4. Sentiment scoring (-1.0 to 1.0) for market direction

### Diversity Analysis
Detects market conditions:
- Echo Chamber: diversity_score < 0.3 (high risk)
- Extreme Consensus: Single sentiment > 80% dominance
- Contrarian Opportunity: Minority view exists with strong contrarian_index
- Cross-Platform Divergence: Different sentiments across platforms

## Development Environment

### Required Environment Variables
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHANNEL_ID=-100xxxxxxx  # Channel for alerts

# AI APIs (for sentiment/summarization)
OPENAI_API_KEY=sk-your-key
DEEPSEEK_API_KEY=your-key  # Alternative to OpenAI
```

### File Permissions
Some scripts need executable permissions:
```bash
chmod +x run-tests.sh deploy-to-github.sh scripts/*.sh
```

### Database
SQLite database is auto-created at runtime. Schema managed via SQLAlchemy in `src/core/database.py`.

### Logging
Structured logs with rotation (10MB files, 7-day retention) in `logs/` directory. Console output uses emoji indicators for readability.

### Code Style
- Ruff for formatting (100 char line limit)
- Double quotes for strings
- Type hints on all public functions
- Docstrings for class-level documentation