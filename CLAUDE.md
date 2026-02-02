# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL: Git Worktree Development Mode

**IMPORTANT**: This repository uses Git worktrees for multi-agent parallel development. DO NOT use standard `git merge` or `git checkout` commands. Always use worktree-specific workflows as described below.

### Current Worktree Setup
This worktree (`/Users/Jacob/clawd-claude`) is configured for the **claude** branch. You cannot switch branches here - use other worktree directories for different branches.

### Worktree-Specific Git Commands
✅ **CORRECT**: `git push origin claude:main`  # Push to remote main
❌ **WRONG**:  `git merge main`               # Will fail in worktree
❌ **WRONG**:  `git checkout main`             # Will fail in worktree

For branch synchronization, always use **push-pull workflow** between worktrees.

## Git Worktree 开发模式（多代理并发专用术语）

### 核心概念
- **工作树锁定**: 每个工作树固定绑定一个分支，不能切换
- **推送合并**: 通过 `git push` 到远程分支实现间接合并
- **跨树同步**: 在其他工作树中 `git pull` 获取更新
- **代理隔离**: 多代理在不同工作树中并行开发，避免直接冲突

### 必须使用的专业术语

#### 操作术语
- **"推送同步"** (Push-Sync)：使用 `git push origin branch:target` 推送更改
- **"拉取更新"** (Pull-Update)：在其他工作树中执行 `git pull origin branch`
- **"跨树通知"** (Cross-Tree Notification)：告知其他代理推送了更改
- **"工作树隔离"** (Worktree Isolation)：当前工作树独立于其他代理的环境

#### 禁止术语（会导致错误）
- ❌ 不要使用 "切换分支"
- ❌ 不要使用 "合并分支"
- ❌ 不要使用 "检出代码"
- ❌ 不要假设可以 `git merge` 或 `git checkout`

### 标准工作流程

1. **当前代理完成任务**
   ```bash
   git add .
   git commit -m "描述: 具体更改内容"
   git push origin 分支名:目标分支
   ```

2. **通知其他代理**（通过用户或系统）

003e "已完成推送同步，请在主工作树执行拉取更新"

3. **其他代理同步**
   ```bash
   # 在主工作树或其他相关工作树中
   git pull origin 目标分支
   ```

### 代理间一致性协议

- **推送后立即通知**：完成更改后必须告知其他代理
- **明确目标分支**：总是指定具体的源分支和目标分支
- **状态确认**：确认其他代理已接收更新
- **冲突预防**：避免多代理同时修改相同文件

### 当前工作树配置
- **当前位置**: `/Users/Jacob/clawd-claude`
- **绑定分支**: `claude`
- **可推送至**: `main`（生产分支）、`claude`（保持同步）
- **其他工作树**: `/Users/Jacob/clawd` (main分支主工作空间)

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