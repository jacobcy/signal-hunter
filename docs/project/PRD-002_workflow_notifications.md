# PRD-002: Workflow Notification System

## 🎯 Objective
Establish a robust, automated mechanism to broadcast "Mission Accomplished" reports to the Telegram channel upon the completion of significant tasks (PRD tasks).
This ensures external collaborators are kept in the loop regarding project progress without manual intervention.

## 🏗️ Architecture: The "Town Crier" Pattern

### 1. The Trigger (Who calls it?)
- **Actors:** Dev, QA, Ops, Analyst.
- **Trigger Point:** At the end of any `sessions_spawn` sub-agent task that results in a material change or completion.
- **Method:** Sub-agents will invoke a standardized script/tool `scripts/utils/notify_progress.py` (to be created).

### 2. The Messenger (The Script)
**Script:** `scripts/utils/notify_progress.py`
- **Input:**
  - `--task`: Task ID (e.g., "Task 003").
  - `--status`: "Success" / "Failed" / "In Progress".
  - `--message`: Human-readable summary of what was done.
  - `--agent`: Role name (e.g., "Dev (0xCAFE)").
- **Logic:**
  - Formats a standard "Mission Report" card.
  - Validates Channel ID (retries or alerts PM if missing).
  - Sends via `src.utils.notifier`.

### 3. The Protocol (SOP Update)
Update `WORKFLOW.md` (and `MEMORY.md` best practices) to include:
> "Every sub-agent completing a PRD task MUST call the notification script as their final action."

## 📝 Message Template
```text
🚀 **Mission Update: [Task Name]**

👤 **Agent:** [Role Name]
✅ **Status:** [Success/Failure]

📝 **Report:**
[Brief summary of what was accomplished]

#OpenClaw #DevUpdate
```

## 📅 Execution Plan (Task 004)
1.  **Dev:** Create `scripts/utils/notify_progress.py`.
2.  **Ops:** Verify it works with the Bot/Channel.
3.  **PM:** Enforce this step in future task instructions.
