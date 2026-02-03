# Task Manager Skill

This skill automates the complete RWP (Role-Workflow-Project) loop for task management, from issue creation through development, testing, merging, and notification.

## Description

The `task-manager` skill provides two main capabilities:

1. **Task Creation & Workflow**: Given a task description, it orchestrates the complete workflow:
   - **Create Issue**: Generate and submit a GitHub Issue with proper formatting and labels
   - **Develop**: Assign the task to Dev (Claude) for implementation
   - **Test**: Assign the implemented feature to QA (Codex) for testing
   - **Merge**: Push the tested changes to GitHub
   - **Notify**: Send a completion notification to stakeholders

2. **Task Listing**: Query and display current tasks with their status by:
   - Querying GitHub Issues labeled with `task-manager`
   - Cross-referencing with local memory logs for granular status
   - Presenting a clean, formatted list with status and links

This skill leverages existing skills like `github`, `claude-team`, `codex-orchestration`, and `message` to orchestrate workflows and manage task visibility.

## Usage

```bash
openclaw task-manager "Implement feature X"
```

### Examples

**Basic usage:**
```bash
openclaw task-manager "Add user authentication to the dashboard"
```

**With specific project context:**
```bash
openclaw task-manager "Fix bug in payment processing module - affects checkout flow"
```

**Feature implementation:**
```bash
openclaw task-manager "Implement dark mode toggle in settings panel"
```

## Workflow Details

### Step 1: Create Issue
- Generates a well-structured GitHub issue with:
  - Clear title based on task description
  - Detailed description with acceptance criteria
  - Appropriate labels (feature/bug/enhancement)
  - Priority assignment based on keywords
- Returns issue number for tracking

### Step 2: Development Phase
- Assigns issue to Claude (Dev team)
- Provides context and requirements
- Sets expectations for implementation approach
- Tracks progress and handles clarifications

### Step 3: Testing Phase
- Once development is complete, assigns to Codex (QA team)
- Provides test scenarios and acceptance criteria
- Ensures comprehensive test coverage
- Validates against original requirements

### Step 4: Merge Process
- Reviews and approves pull request
- Handles any merge conflicts
- Ensures proper version control practices
- Updates issue status to closed

### Step 5: Notification
- Sends completion notification with:
  - Summary of implemented feature
  - Link to merged pull request
  - Any relevant documentation updates
  - Next steps if applicable

## Dependencies

This skill requires the following skills to be available:
- `github`: For issue creation and repository management
- `claude-team`: For development assignments and implementation
- `codex-orchestration`: For testing and quality assurance
- `message`: For notifications and status updates

## Configuration

The skill can be configured via environment variables or configuration files to specify:
- Default repository owner and name
- Team member assignments
- Notification channels
- Label conventions
- Priority rules