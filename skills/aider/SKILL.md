---
name: aider
description: AI pair programmer in your terminal. Use for rapid code editing, config auditing, and data analysis.
metadata: {"clawdbot":{"emoji":"👨‍💻","requires":{"bins":["aider"]}}}
---

# Aider (The Analyst/Architect)

Aider is a command-line AI coding assistant that works directly with your local git repo.

**Role in Trinity:** **Analyst / Ops / Tool Smith**
- **Auditing:** Scanning `skills/` or config files for errors.
- **Analysis:** Reading logs and summarizing data.
- **Refactoring:** Making broad changes across multiple files.

## Basic Usage

Run Aider in a background process (recommended) or interactive PTY.

**⚠️ IMPORTANT:** Use the dedicated virtual environment path: `/Users/Jacob/aider-env/bin/aider`

```bash
# Start Aider in a specific directory
bash workdir:~/project background:true command:"/Users/Jacob/aider-env/bin/aider --message 'Audit the config files'"
```

## Common Flags

- `--message "..."` / `-m "..."`: Provide the prompt and run immediately (non-interactive mode).
- `--yes`: Always say yes to suggestions (use with caution, or for read-only tasks).
- `--read <file>`: Read a file into context (readonly).
- `--file <file>`: Add a file to the chat (editable).

## Workflows

### 1. Skill/Config Audit (The "Analyst" Job)

Use Aider to scan directories and report on consistency.

```bash
# Audit skills directory
bash workdir:~/.openclaw/skills background:true command:"/Users/Jacob/aider-env/bin/aider --message 'Scan all SKILL.md files. Check if their <location> paths exist. Report broken links.' --yes"
```

### 2. Log Analysis

```bash
# Analyze recent logs
bash workdir:~/clawd/logs background:true command:"/Users/Jacob/aider-env/bin/aider --read error.log --message 'Summarize the top 3 recurring errors in this log file.' --yes"
```

### 3. Quick Refactor

```bash
bash workdir:~/project background:true command:"/Users/Jacob/aider-env/bin/aider --file src/main.py --message 'Refactor the login function to use async/await' --yes"
```

## Best Practices

- **Context is Key:** Use `--read` for files you want Aider to see but not touch.
- **Git Safety:** Aider automatically commits changes. Ensure you are on a safe branch or clean state.
- **Architect Mode:** Use `aider --architect` (if supported) for high-level reasoning before editing.
