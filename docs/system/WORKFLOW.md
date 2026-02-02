# WORKFLOW.md - The AI Development Lifecycle

## 1. Inception (可行性研究)
**Actors:** User + PM + Analyst
- **Trigger:** User has an idea (e.g., "Add crypto tracking").
- **Action:**
  - PM analyzes intent.
  - Analyst checks data availability (e.g., "Do we have an API for this?").
  - **Output:** Feasibility Report (Go/No-Go).

## 2. Definition (产品定义)
**Actors:** PM + Analyst
- **Action:** Create a Product Requirement Document (PRD).
- **PRD Content:**
  - **Goal:** One-line objective.
  - **User Stories:** "As a user, I want..."
  - **Technical Specs:** API endpoints, data structures.
  - **Success Metrics:** "Script runs without error and outputs JSON."
- **Output:** `tasks/XXX_task_name.md`.

## 3. Approval (批准)
**Actors:** User + PM
- **Action:** PM presents PRD to User.
- **Output:** `APPROVED` signal.

## 4. Preparation (技能准备)
**Actors:** PM + Ops + Scout
- **Action:**
  - Check if we have required skills (`openclaw skills list`).
  - If missing, Scout finds the best tool/library.
  - Ops installs dependencies (`pip install`, `brew install`).
- **Output:** Environment ready.

## 5. Construction (开发)
**Actors:** Dev (0xCAFE)
- **Tool:** Aider / Codex
- **Action:**
  - Read PRD (`tasks/XXX.md`).
  - Write code in `scripts/` or `src/`.
  - Local unit testing.
- **Output:** Source code committed to git feature branch.

## 6. Verification (测试 & 验收)
**Actors:** QA (Bugsy)
- **Tool:** OpenCode
- **Action:**
  - Pull branch.
  - Run `pytest` or execution script.
  - Verify output matches PRD.
- **Output:** Test Report (Pass/Fail).

## 7. Delivery & Monitoring (交付 & 监控)
**Actors:** Ops (Daemon)
- **Action:**
  - Merge to `main`.
  - Deploy (if service).
  - Add to `scripts/system_health.py` monitoring list.
  - Schedule Cron Job (if periodic).
- **Output:** Live system.

## 8. Evolution (持续进化)
**Actors:** Researcher + Analyst
- **Trigger:** Weekly Cron.
- **Action:** Scan for updates/better tools.
- **Output:** Update Proposal.
