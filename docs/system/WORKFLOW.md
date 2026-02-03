# WORKFLOW.md - The Trinity Workflow

## 🔄 The Cycle (Observe - Evaluate - Plan - Act)

### Phase 1: Definition (PM)
1. User provides intent.
2. PM creates/updates a PRD in `tasks/`.
3. PM selects the right "Squad" members.

### Phase 2: Execution (The Trinity Split)

#### Track A: Development (Claude)
- **Role:** Lead Dev.
- **Action:** Reads PRD, writes implementation code in `src/`.
- **Tool:** `claude-code` or `sessions_spawn(model="claude")`.

#### Track B: Verification (Codex)
- **Role:** QA Engineer.
- **Action:** Reads PRD, writes unit/integration tests in `tests/`.
- **Tool:** `codex-orchestration` or `sessions_spawn(model="gpt-4")`.

#### Track C: Support & Audit (Aider/DeepSeek)
- **Role:** Analyst / Tool Smith.
- **Action:** 
    - Scans `skills/` for misconfigurations.
    - Analyzes data logs from `logs/`.
    - Fixes environment issues blocking Dev/QA.
- **Tool:** `aider` CLI.

### Phase 3: Convergence
1. Tests run against implementation.
2. If Pass -> PM merges/deploys.
3. If Fail -> Feedback loop to Dev (Claude).

## 🛠 Tool Optimization Protocol
- **Audit:** Aider regularly scans `skills/` to ensure paths are correct and dependencies are met.
- **Usage:** Prefer specific skills (e.g., `github`, `files`) over generic shell commands when possible to reduce error rates.
