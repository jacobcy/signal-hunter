# Task 006: Modularize Reporting & Notification System

## 🎯 Objective
Refactor the current monolithic reporting logic into atomic, reusable modules to improve maintainability and testability.
Address the user's feedback: "Module Splitting (Notification as a component, Report Generation as a module)" and "Strict Testing".

## 🏗️ Architecture Refactor

### 1. `src/utils/teleporter.py` (The Transporter)
**Responsibility:** Purely handles the *delivery* mechanism to Telegram.
- **Input:** `target_id`, `message_text`.
- **Logic:**
  - Auto-load `.env` (robustness).
  - Try primary method (httpx/src.notifier).
  - Fallback method (urllib).
  - Retry logic (simple 3-attempt loop).
- **Status:** Atomic component.

### 2. `src/utils/reporter.py` (The Scribe)
**Responsibility:** Handles the *formatting* and *content structure*.
- **Class `ReportBuilder`**:
  - `build_mission_update(task, agent, status, problem, solution, next_steps)`
  - `build_market_signal(signal, reason, audit)`
  - `build_ai_brief(headline, deep_dive, kol_sentiment, system_audit)`
- **Logic:** Returns a formatted string (Markdown).

### 3. Update `scripts/utils/notify_progress.py` (The CLI)
**Responsibility:** Command-line interface only.
- **Logic:**
  - Parse args (including new fields: `--problem`, `--solution`, `--next`).
  - Call `ReportBuilder` to format.
  - Call `Teleporter` to send.

## 🤖 Assigned Roles
- **Dev (0xCAFE):** Implement `teleporter.py`, `reporter.py`, and refactor `notify_progress.py`.
- **QA (Bugsy):** Create `tests/test_reporting.py` to verify formatting and mock-send logic.

## 🚀 Execution Plan
1.  **Dev** creates the modules in `src/utils/`.
2.  **Dev** updates the CLI script.
3.  **QA** runs the test suite.
4.  **Dev** triggers a "Task 006 Complete" report using the NEW system to demonstrate its capability.
