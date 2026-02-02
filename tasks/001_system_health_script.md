# Task 001: Implement Layer 1 Infrastructure (System Health Guardian)

## 🎯 Objective
Implement **Layer 1** of the Trinity Framework: The **System Health Guardian**.
This script (`scripts/infrastructure/guardian.py`) will serve as the foundation, ensuring system survivability and asset availability.

## 🤖 Assigned Roles (Parallel Execution)
- **Dev (0xCAFE):** Build the `guardian.py` script and necessary shell wrappers.
- **QA (Bugsy):** Create test cases and verify the script's output and alerting mechanisms.

## 📋 Requirements (Dev)

### 1. Structure
- Create directory: `scripts/infrastructure/`
- Move/Rename logic from old `scripts/daily_check.sh` if useful, but primary focus is Python-based `guardian.py`.

### 2. Functional Checks (`guardian.py`)
The script must validate the following **Vital Signs**:
1.  **Connectivity:** Ping Gateway (`google.com` or `8.8.8.8`).
2.  **Process Status:** Is `openclaw` running? (Port 18789 check).
3.  **Asset/API Validation:**
    - **Telegram:** Verify Bot Token validity (`getMe`).
    - **LLM Providers:** Simple probe (1 token) to primary model (DeepSeek/Gemini).
    - **Notion:** Simple probe (if configured).
4.  **Resources:** Disk usage (>90% alert), Memory.

### 3. Output & Alerting
- **Console:** Rich text summary (Green/Red).
- **Report:** Save JSON status to `memory/reports/health_latest.json`.
- **Alert:** If CRITICAL failure (e.g., Network Down, API Invalid), send Telegram Alert immediately via `src.utils.notifier`.

## 🧪 Verification (QA)
- **Test Suite:** `tests/test_guardian.py`
- **Cases:**
    - Mock successful API responses -> Expect Green status.
    - Mock network failure -> Expect Red status + Alert trigger.
    - Mock disk full -> Expect Warning.

## 🚀 Execution Plan
1.  **Dev** starts implementing `scripts/infrastructure/guardian.py`.
2.  **QA** starts writing `tests/test_guardian.py` (TDD approach or parallel).
3.  **Dev** integrates `src.utils.notifier`.
4.  **QA** runs validation.
