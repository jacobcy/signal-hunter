# Issue Draft: Implement Basic User Management System

## Description
We need to implement the core user management logic defined in **PRD-002**. This involves creating a Python class to handle user state, persistence, and role-based permission checks.

## Requirements
1.  **Data Store**:
    -   Use `memory/users.json` to store user data.
    -   Ensure thread-safe reads/writes if possible (or simple file locking).
2.  **`UserManager` Class**:
    -   Methods: `get_user(id)`, `create_user(id, metadata)`, `update_role(id, role)`, `check_permission(id, action)`.
3.  **Roles**:
    -   `OWNER`: All permissions.
    -   `CONTRIBUTOR`: Can use `/report`, `/feature`.
    -   `SUBSCRIBER`: Can use `/start`, `/help`.
4.  **Integration Points**:
    -   The main agent loop needs to check `user_manager.get_user(sender_id)` before processing commands.

## Acceptance Criteria
-   [ ] A new user sending `/start` is added to `users.json` as `SUBSCRIBER`.
-   [ ] A `CONTRIBUTOR` can successfully log a report (mocked logging is fine for now).
-   [ ] An `OWNER` can promote a user via function call.
-   [ ] Unit tests cover user creation and permission checks.

---

## Task Assignments

### 1. Development
*   **Assignee**: Dev (Claude)
*   **File**: `src/auth/user_manager.py`
*   **Instructions**: Implement the `UserManager` class. Focus on robust JSON handling (loading/saving) and clean permission logic. Don't worry about the actual Telegram/Discord integration yet; just the logic layer.

### 2. Quality Assurance
*   **Assignee**: QA (Codex)
*   **File**: `tests/auth/test_user_manager.py`
*   **Instructions**: Write `pytest` cases.
    -   Test creating a new user.
    -   Test persistence (save to disk, reload, ensure data matches).
    -   Test permission denials (e.g., Subscriber trying to access Owner command).
