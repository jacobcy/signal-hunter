# PRD-001: The Trinity Framework Refactor

## 🎯 Strategic Vision
Refactor the project into a three-layer architecture to support sustainable growth and autonomous trading.

## 🏗️ The Three Layers

### Layer 1: Infrastructure (The Foundation)
**Goal:** Guarantee system survivability and asset availability.
**Component:** `System Health Guardian`
- **Scope:**
  - API Token validation (Telegram, LLMs, Notion).
  - Server resources (Disk, Memory, Process).
  - Service status (Cron jobs, Gateway).
- **Deliverable:** A "Green/Red" status dashboard sent daily (or on alert).
- **Current State:** Partially exists in `scripts/daily_check.sh` (confused with Hunter).
- **Action:** Extract & harden into `scripts/infrastructure/guardian.py`.

### Layer 2: Capability (The Hunter)
**Goal:** Universal information monitoring and briefing.
**Component:** `Info Scout` (General Purpose Monitor)
- **Scope:**
  - Source agnostic: X (Twitter), RSS, News sites.
  - Topic agnostic: Configurable "Watchlists" (e.g., "AI Tech", "Crypto Macro", "Meme Coins").
  - Output: Summarized briefings (Daily Brief, Flash Alerts).
- **Deliverable:** A configurable tool that accepts `(Source, Keyword, Schedule)` and outputs `Report`.
- **Current State:** Exists as "Daily AI Briefing" cron job (hardcoded).
- **Action:** Refactor into a configurable module `src/hunter/scout.py` with support for multiple "Missions".

### Layer 3: Application (The Analyst)
**Goal:** Profit generation via signal extraction.
**Component:** `Signal Analyzer`
- **Scope:**
  - Consumes raw data from Layer 2 (The Hunter).
  - Applies logic/models to identify trading opportunities.
  - Outputs: Buy/Sell signals, Trend analysis.
- **Deliverable:** Actionable trading signals sent to the specific channel.
- **Current State:** Non-existent / Concept phase.
- **Action:** Design the interface to consume Hunter's data.

## 📅 Execution Plan

### Phase 1: Separation & Hardening (Infrastructure)
1.  Rename `daily_check.sh` to `scripts/infrastructure/health_check.sh`.
2.  Strip out "content" logic from health checks.
3.  Implement `guardian.py` for API/Asset validation (Task 001).

### Phase 2: The Hunter Core (Capability)
1.  Create `src/hunter/` directory.
2.  Abstract the current "AI Briefing" logic into a generic class `InfoScout`.
3.  Config file `hunter_config.yaml` to define topics (Topic A: AI, Topic B: Crypto).

### Phase 3: Signal Logic (Application)
1.  Define the criteria for a "Trade Signal" vs just "News".
2.  Build the analyzer pipeline.

## 👥 Role Alignment
- **Ops (Daemon):** Owns Layer 1 (Infrastructure).
- **Researcher (Birdie):** Owns Layer 2 (The Hunter - Configuration).
- **Analyst (Lens):** Owns Layer 3 (The Signal Logic).
- **Dev (0xCAFE):** Builds the code for all layers.
- **PM (Mumu):** Orchestrates the data flow between layers.
