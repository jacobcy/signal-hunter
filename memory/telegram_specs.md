# Telegram Infrastructure Specifications

## 🤖 Bot Identity
- **Name:** `@mmcmy2018_news_bot`
- **Role:** Broadcaster & Notifier
- **Permissions:** Must be **Administrator** in target channels to post messages.

## 📢 Channels & Groups Topology

### The Distinction
- **Channel:** Broadcast tool. One-to-many.
    - *Behavior:* Messages sent here by Admin Bot appear to all subscribers.
    - *Direction:* Channel posts -> Auto-forwarded to Linked Group (if any).
- **Group (Discussion):** Many-to-many chat.
    - *Behavior:* Messages sent here stay here. They **DO NOT** appear in the Channel (unless manually forwarded).

### 🎯 Target Configuration
- **Primary Target ID:** `-1003848721376`
- **Type:** **Channel** (Confirmed via ID Sniffer).
- **Linked Group:** Unknown/Not used for broadcast.

### 🛠 Protocol (The "Happy Path")
1.  **Target:** Always target the **Channel ID** (`-1003848721376`).
2.  **Requirement:** Bot MUST be an **Admin** in the Channel.
3.  **Result:** Message appears in Channel -> Users see notification -> (Optional) Auto-forwards to discussion group.

### ⚠️ Common Errors
- `chat not found`:
    1.  Bot is not a member.
    2.  Bot is not Admin (cannot "see" or "post" in channel).
    3.  ID is incorrect.
    4.  Network/Proxy issue preventing Telegram API access.

## 📝 Reporting Standards
- **Task Reports:** Sent to Channel via `notify_progress.py`.
- **Market Signals:** Sent to Channel via Hunter/Analyst pipeline.
- **AI Briefings:** Sent to Channel via Hunter/Analyst pipeline.
