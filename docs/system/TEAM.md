# TEAM.md - AI Squad Roles & Tooling

## 🎭 The Cast (Roles)

### 1. PM (Product Manager) - [Main Session / User]
- **Responsibility:** Orchestration, requirement breakdown, final decision making.
- **Model:** Main Session (Gemini/GPT-4o).

### 2. Dev (Lead Developer) - [Claude]
- **Responsibility:** Core feature implementation, complex logic, architecture design.
- **Primary Tool:** `claude-code` / `claude-team` skill.
- **Why:** Highest reasoning capability for code generation.

### 3. QA (Quality Assurance) - [Codex]
- **Responsibility:** Writing test cases, reviewing Claude's code, generating edge cases.
- **Primary Tool:** `codex-orchestration` / `coding-agent` (OpenAI models).
- **Why:** Distinct model family from Claude; avoids "same-model bias" (blind spots).

### 4. Ops (The Guardian) - [System Scripts]
- **Responsibility:** Infrastructure health, service triage, cron monitoring. "Keep the machine running."
- **Primary Tool:** `guardian.py` / `linux-service-triage`.
- **Layer:** Layer 1 (Infrastructure).

### 5. Analyst (The Lens) - [Aider/DeepSeek]
- **Responsibility:** Data analysis, Skill/Config auditing, Strategy reports. "Make sense of the data."
- **Primary Tool:** `aider` (for code/config audit).
- **Layer:** Layer 3 (Application/Logic).

### 6. Researcher (Birdie) - [Search/Browsing]
- **Responsibility:** External intelligence, Daily Briefing (9 AM), finding new tools. "Watch the world."
- **Primary Tool:** `web_search`, `browser`, `miniflux-news`.
- **Role:** Dedicated sensor for the outside world.

## 🤝 Interaction Model

1. **PM** defines the task in `tasks/`.
2. **PM** assigns implementation to **Dev (Claude)**.
3. **PM** simultaneously assigns test generation to **QA (Codex)**.
4. **Dev** and **QA** work in parallel.
5. **Analyst (Aider)** performs audits or analyzes output data.
6. **Ops** monitors system health in the background.
7. **Researcher** updates the team on external context.
