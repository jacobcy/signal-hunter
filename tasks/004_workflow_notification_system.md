# Task 004: Implement Workflow Notification System

## 🎯 Objective
Create the "Town Crier" system (`scripts/utils/notify_progress.py`) to standardize and automate external progress reporting to the Telegram channel.

## 🤖 Assigned Roles
- **Dev (0xCAFE):** Develop the notification script.
- **Ops (Daemon):** Verify channel connectivity and permissions (fix previous `chat not found` error).

## 📋 Requirements (Dev)

### 1. Script: `scripts/utils/notify_progress.py`
- **Arguments:**
    - `--task` (str): Task ID/Name.
    - `--agent` (str): Agent Role Name.
    - `--status` (str): SUCCESS / FAILED.
    - `--content` (str): The report body.
- **Function:**
    - Format a Telegram message using the standard template (defined in PRD-002).
    - Use `src.utils.notifier.send_telegram_alert` (or implement direct HTTP call if simpler/more robust).
    - Handle errors gracefully (print to stderr but don't crash caller).

### 2. Message Template
```text
🚀 **Mission Update: {task}**

👤 **Agent:** {agent}
✅ **Status:** {status}

📝 **Report:**
{content}

#OpenClaw #DevUpdate
```

## 🔍 Ops Validation (Critical)
- **Diagnose:** Why did `Analyst-Lens` fail with `chat not found` for ID `-1003848721376`?
- **Fix:** Ensure Bot `@mmcmy2018_news_bot` is an **Administrator** in the channel.
- **Verify:** Run the new script manually to send a test "Hello World" to the channel.

## 🚀 Execution Plan
1.  **Dev** creates the script.
2.  **Ops** runs diagnosis and verification.
3.  **Dev** commits the script.
