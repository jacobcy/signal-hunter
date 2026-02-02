# MEMORY.md - Long Term Memory

## 🌍 Core Directives
- **Team Structure:** Defined in `TEAM.md`.
- **Capabilities:** Defined in `CAPABILITIES.md`.
- **Workflow:** Defined in `WORKFLOW.md`.
- **Assets:** Managed in `memory/api_assets.md`.

## 🧠 Strategic Context
- **Goal:** Build a profitable, autonomous signal hunting and trading system.
- **Current Phase:** Infrastructure Hardening & Capability Expansion.
- **Philosophy:** "Active Evolution" - The system monitors itself and suggests upgrades.

## 📜 Key Decisions
- **2026-02-01:**
  - Solidified full "AI Squad" persona model with six roles (PM, Dev, QA, Ops, Analyst, Researcher) as defined in `TEAM.md`.
  - Adopted strict "Task Delegation" workflow where the PM orchestrates and delegates to all specialized agents.
  - Prioritized `scripts/system_health.py` as the "conscience" of the system.
  - Established `aider` (DeepSeek) as the primary coding engine in `~/aider-env`.
- **2026-02-02:**
  - **Framework Refactor:** Adopted "The Trinity Framework" (PRD-001): Layer 1 Infrastructure (Guardian), Layer 2 Capability (Hunter), Layer 3 Application (Analyst).
  - **Standard Operating Procedure (SOP):** Solidified the parallel, non-blocking development model.
    - **Delegation:** PM delegates to sub-agents (Dev/QA/Ops) for execution.
    - **Parallelism:** Dev writes code while QA writes tests; no blocking.
    - **Verification:** Tools (skills/API) must be validated before use.
    - **Focus:** Main session remains responsive for high-level direction and monitoring.
  - **Case Study (Success):** Signal Hunter Channel Fix (Task 002) & Guardian Implementation (Task 001) successfully demonstrated this pattern.
  - **Communication:** Telegram Channel `-1003848721376` is the designated primary channel for both system alerts and signal broadcasting (for now).
  - Confirmed the RWP (Role-Workflow-Project) paradigm as the foundational framework for all operations. The concrete AI Development Lifecycle in `WORKFLOW.md` is an implementation of the abstract RWP Observe-Evaluate-Plan-Act loop.
  - Aligned `MEMORY.md` with `TEAM.md` and `WORKFLOW.md` to resolve knowledge conflicts.
  - Established periodic self-audit workflow for assets, documents, and skills to eliminate redundancy, resolve conflicts, and prevent hallucinations. Scheduled via cron for weekly/monthly runs.
  - Implemented a daily AI briefing, scheduled for 9 AM. Task assigned to Researcher (Birdie) to monitor external dynamics and suggest skill updates, ensuring continuous evolution.
  - Created `STRUCTURE.md` and restructured workspace directories for clarity, maintainability, and to reduce information entropy. All files migrated to defined paths; audits will now validate against this structure.

## 🛠️ Active Projects
1.  **Layer 1 (Guardian):** Implemented (v1.0). Ready for deployment.
2.  **Layer 2 (Hunter):** Next up (PRD-001 Phase 2).
3.  **Signal Hunter:** (Legacy) to be refactored into Layer 2/3.

## ⚠️ Watchlist
- **Telegram Channel ID:** Found (`-1003848721376`).
- **Claude:** No direct key. Using surrogates.
