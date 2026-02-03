# Bug Manager Skill

This skill automates the complete RWP (Role-Workflow-Project) loop for bug management, from issue creation through development, testing, merging, and notification.

## Description

The `bug-manager` skill provides two main capabilities:

1. **Bug Creation & Workflow**: Given a bug report, it orchestrates the complete workflow:
   - **Create Issue**: Generate and submit a GitHub Issue with `bug` label
   - **Develop**: Assign the bug to Dev (Claude) for fixing
   - **Test**: Assign the fixed bug to QA (Codex) for verification
   - **Merge**: Push the verified fix to GitHub
   - **Notify**: Send a completion notification to stakeholders

2. **Bug Listing**: Query and display current bugs with their status by:
   - Querying GitHub Issues labeled with `bug`
   - Cross-referencing with local memory logs for granular status
   - Presenting a clean, formatted list with status and links

3. **Auto-Fix**: Automatically scan open bugs and attempt to fix them in sequence using the same RWP loop.

This skill leverages existing skills like `github`, `claude-team`, `codex-orchestration`, and `message` to orchestrate workflows and manage bug visibility.

## Usage

```bash
openclaw bug-manager "Report bug description"
```

### Examples

**Basic usage:**
```bash
openclaw bug-manager "Login button not working on mobile devices"
```

**With specific project context:**
```bash
openclaw bug-manager "Memory leak in data processing module causing application crashes"
```

**List all bugs:**
```bash
openclaw bug-manager list
```

**Auto-fix all open bugs:**
```bash
openclaw bug-manager auto-fix
```

## Workflow Details

### Step 1: Create Issue
- Generates a well-structured GitHub issue with:
  - Clear title based on bug description
  - Detailed description with reproduction steps
  - Appropriate labels (`bug`, `priority-high/medium/low`)
  - Priority assignment based on severity keywords
- Returns issue number for tracking

### Step 2: Development Phase
- Assigns issue to Claude (Dev team)
- Provides context and reproduction steps
- Sets expectations for fix approach
- Tracks progress and handles clarifications

### Step 3: Testing Phase
- Once development is complete, assigns to Codex (QA team)
- Provides test scenarios and verification criteria
- Ensures comprehensive test coverage for the bug fix
- Validates against original reproduction steps

### Step 4: Merge Process
- Reviews and approves pull request
- Handles any merge conflicts
- Ensures proper version control practices
- Updates issue status to closed

### Step 5: Notification
- Sends completion notification with:
  - Summary of fixed bug
  - Link to merged pull request
  - Verification results
  - Any relevant documentation updates

### Auto-Fix Feature
- Scans all open bugs with `bug` label
- Prioritizes bugs based on severity/priority
- Processes each bug through the complete RWP loop
- Continues until all open bugs are addressed or encounters a blocking issue

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
- Auto-fix behavior (max concurrent fixes, priority thresholds)