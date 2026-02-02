# CAPABILITIES.md - Core Team Capabilities

To ensure stability and evolution, we maintain these 4 core capabilities.

## 1. Skill Manager (技能管理)
**Owner:** 👁️ Birdie (Scout) + 🔧 Daemon (Ops)
**Objective:** Maintain and expand the team's toolbelt.
- **Scan:** Birdie monitors X/GitHub for new AI tools (e.g., "Browser Use", "MCP").
- **Evaluate:** Lens checks if it solves a current pain point.
- **Install:** Daemon runs `npm install` or `brew install`.
- **Develop:** If no tool exists, Dev builds a custom Skill (API wrapper).

## 2. Knowledge Base Manager (知识库管理)
**Owner:** 🧠 Lens (Analyst)
**Objective:** Single Source of Truth (Notion > Local Files).
- **Platform:** Notion (Page: `1e47...`)
- **Structure:**
  - `Team Resources`: Mirrors `TEAM.md`, `WORKFL
  OW.md`, `api_assets.md`.
  - `Project Docs`: PRDs, Tech Specs.
  - `Intelligence Hub`: Signal Hunter reports.
- **Action:** Sync local markdown changes to Notion daily.

## 3. Asset Manager (资产与健康管理)
**Owner:** 🔧 Daemon (Ops)
**Objective:** Keep the engine running.
- **Inventory:** Maintain `memory/api_assets.md` (Keys, Tokens, Balances).
- **Health:** Run `scripts/system_health.py` daily.
- **Alert:** Notify via Telegram if an API dies or disk is full.

## 4. Project Manager (项目管理)
**Owner:** 🌲 Mumu (PM)
**Objective:** Deliver value efficiently.
- **Workflow:** Enforce `WORKFLOW.md` (Inception -> Delivery).
- **Tracking:** Maintain "Project Docs" in Notion with status (To Do / In Progress / Done).
- **Reporting:** Daily morning briefing to User.
