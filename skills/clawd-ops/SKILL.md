# clawd-ops - Unified Operations Toolkit

A comprehensive operations toolkit for the OpenClaw workspace that integrates system health monitoring, environment setup, asset testing, and daily checks into a single cohesive skill.

## Commands

### `clawd-ops health`
Run comprehensive system health checks including network connectivity, system resources, processes, and external assets.

**Example:**
```bash
clawd-ops health
```

### `clawd-ops setup-env`
Set up and activate the development environment by activating the virtual environment and configuring PYTHONPATH.

**Example:**
```bash
source <(clawd-ops setup-env)
```

### `clawd-ops test-assets`
Test critical infrastructure assets including API keys, file paths, network connectivity, and LLM endpoints.

**Example:**
```bash
clawd-ops test-assets
```

### `clawd-ops daily-check`
Run comprehensive daily project health checks including git status, code quality, tests, documentation, and standards compliance.

**Example:**
```bash
clawd-ops daily-check
```

### `clawd-ops daily-check-telegram`
Run daily checks and send results via Telegram notification.

**Example:**
```bash
clawd-ops daily-check-telegram
```

## Integration Details

This skill integrates the following existing and new components:

1. **Environment Setup** (`scripts/setup_env.sh`)
   - Activates the `.venv` virtual environment
   - Sets up proper PYTHONPATH for the workspace
   - Handles both bash and zsh shell compatibility

2. **System Health Monitoring** (`scripts/infrastructure/guardian.py`)
   - Network connectivity checks (8.8.8.8, api.telegram.org, api.openai.com)
   - System resource monitoring (CPU load, memory usage, disk space)
   - Process monitoring
   - Critical alerting via Telegram for system issues

3. **Asset Testing** (`scripts/ops/test_assets.py`)
   - API key validation for OpenRouter, DeepSeek, and local LLM
   - File path verification for critical project files
   - Network connectivity testing to essential services
   - Configuration file validation

4. **Daily Checks** (Integrated from `scripts/daily_check.sh` and `scripts/daily_check_telegram.py`)
   - Git repository status and commit history
   - Code quality analysis (Ruff linter, MyPy type checker)
   - Test suite status and coverage
   - Documentation audit (README.md, PRD.md, etc.)
   - Code metrics and TODO/FIXME tracking
   - Standards compliance and improvement recommendations

## Requirements

- Python 3.8+
- Virtual environment at `.venv/`
- Required Python packages: python-dotenv
- Environment variables configured in `.env` file:
  - `OPENROUTER_API_KEY`
  - `DEEPSEEK_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## Usage Examples

### Basic Health Check
```bash
clawd-ops health
```

### Set up Development Environment
```bash
# In bash/zsh
source <(clawd-ops setup-env)

# Or execute directly
eval "$(clawd-ops setup-env)"
```

### Comprehensive Asset Testing
```bash
clawd-ops test-assets --verbose
```

### Daily Project Audit
```bash
# Console output only
clawd-ops daily-check

# With Telegram notification
clawd-ops daily-check-telegram
```

## Error Handling

The skill provides clear error messages and exit codes:
- Exit code 0: Success
- Exit code 1: Warning conditions detected
- Exit code 2: Critical failures or configuration errors

## Maintenance

Reports are automatically saved to:
- Health reports: `memory/reports/health_latest.json`
- Daily check reports: `memory/daily-check-YYYY-MM-DD.md`

Critical system issues trigger automatic Telegram alerts when properly configured.