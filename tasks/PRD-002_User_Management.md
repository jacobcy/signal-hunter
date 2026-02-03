# PRD-002: User Management & Guest Contribution System (Phase 1)

## 1. Overview
This feature introduces a structured user management system to OpenClaw. It enables the agent to recognize different tiers of users (Owner, Contributors, Subscribers) and allows for controlled guest contributions (reporting bugs, requesting features) and subscription management.

## 2. User Model (3-Layer)
We define three distinct roles with specific permissions:

### 2.1. Owner (Admin)
-   **Identity**: Defined in `USER.md` or system config.
-   **Permissions**: Full access to all tools (shell, file I/O, dangerous actions).
-   **Capabilities**: Can approve/reject guest contributions, manage user roles, and override safety checks.

### 2.2. Contributor (Trusted Guest)
-   **Identity**: Verified users (whitelisted in `memory/users.json`).
-   **Permissions**: 
    -   Can submit bug reports (`/report`).
    -   Can request features (`/feature`).
    -   Can view public roadmaps or status.
    -   *Cannot* execute shell commands or modify core files directly.
-   **Goal**: Enable collaboration without exposing the host system to risk.

### 2.3. Subscriber (ReadOnly / Notification)
-   **Identity**: Users who have opted in for updates.
-   **Permissions**: 
    -   Can register (`/start` or `/subscribe`).
    -   Receives broadcast notifications (changelogs, status updates).
    -   Can unsubscribe (`/stop` or `/unsubscribe`).
-   **Goal**: passive engagement audience.

## 3. Data Schema: `memory/users.json`
This file will serve as the lightweight database for user persistence.

```json
{
  "meta": {
    "version": "1.0",
    "updatedAt": "2024-01-01T12:00:00Z"
  },
  "users": {
    "user_id_12345": {
      "username": "alice",
      "platform": "telegram",
      "role": "contributor", 
      "joinedAt": "2023-12-01T10:00:00Z",
      "lastActive": "2024-01-01T12:00:00Z",
      "subscriptions": ["broadcasts", "alerts"],
      "trustLevel": 1
    },
    "user_id_67890": {
      "username": "bob",
      "platform": "discord",
      "role": "subscriber",
      "joinedAt": "2024-01-02T15:30:00Z",
      "lastActive": "2024-01-02T15:30:00Z",
      "subscriptions": ["broadcasts"],
      "trustLevel": 0
    }
  }
}
```

## 4. Commands & Interface

### 4.1. General Commands
-   `/start` or `/register`: 
    -   Behavior: Checks if user exists. If not, creates a "Subscriber" entry. Welcomes the user.
-   `/help`:
    -   Behavior: Context-aware help. Owners see admin tools; Contributors see contribution guides; Subscribers see status commands.

### 4.2. Contribution Commands (Contributors+)
-   `/report <description>`:
    -   Behavior: Logs a bug report to `tasks/inbox.md` (or a dedicated `issues/` folder). notifies Owner.
-   `/feature <idea>`:
    -   Behavior: Logs a feature request to `tasks/inbox.md`.

### 4.3. Admin Commands (Owner Only)
-   `/promote <user_id> <role>`: Change a user's role (e.g., Subscriber -> Contributor).
-   `/ban <user_id>`: Block a user.
-   `/broadcast <message>`: Send a message to all Subscribers.

## 5. Security & Safety
-   **Input Sanitization**: All inputs from `/report` and `/feature` must be treated as untrusted text. No automatic execution.
-   **Rate Limiting**: Prevent spam from Subscribers (e.g., max 1 report per hour).
-   **Isolation**: Guest commands must never trigger `exec` or `file_write` directly. They only append to a passive log file for Owner review.

## 6. Success Metrics
-   Successfully tracking unique users in JSON.
-   Non-owner users can submit a report without crashing the bot.
-   Owner receives notification of new reports.
