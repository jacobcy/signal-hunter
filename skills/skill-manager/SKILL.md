# skill-manager

Manage OpenClaw skills for AI team members. Install, update, verify, and configure skills by role.

## When to Use

Use this skill when you need to:
- Set up skills for a new AI team member (Dev, QA, Ops, etc.)
- Bulk install recommended skills for a specific role
- Update all skills to latest versions
- Verify skill availability for a team member
- Audit current skill installations

## Installation Scope

This skill supports three installation modes:

| Mode | Path | Use Case |
|------|------|----------|
| Global | `~/.openclaw/skills/` | Shared across all projects (Recommended for teams) |
| Workspace | `<project>/skills/` | Project-specific skills |
| Local | `./skills/` | Temporary/testing |

## Role-Based Skill Presets

### AI Project Manager (木木)
```yaml
skills:
  - claude-team          # Multi-agent orchestration
  - codex-orchestration  # Task scheduling
  - model-usage          # Cost monitoring
  - prompt-log           # Session analysis
  - session-logs         # Log search
  - cron                 # Scheduled tasks
```

### Developer (Dev)
```yaml
skills:
  - coding-agent         # Multi-IDE support
  - conventional-commits # Commit formatting
  - github               # GitHub operations
  - github-pr            # PR management
  - gitload              # Partial repo download
```

### QA Engineer (QA)
```yaml
skills:
  - pytest               # Test framework (if available)
  - coverage             # Coverage reporting
  - github-pr            # PR testing
```

### Operations (Ops)
```yaml
skills:
  - linux-service-triage # Service diagnostics
  - deploy-agent         # Deployment automation
  - cron                 # Scheduled monitoring
```

### Data Analyst (Analyst)
```yaml
skills:
  - browser              # Web scraping
  - canvas               # Visualization
  - finance              # Financial data (search)
```

### Editor
```yaml
skills:
  - frontend-design      # UI/UX design
  - ui-audit             # Interface review
  - ux-audit             # UX evaluation
```

### HR / Role Designer
```yaml
skills:
  - agentlens            # Codebase understanding
  - perry-workspaces     # Workspace management
  - deepwiki             # Documentation query
```

## Commands

### Install Skills for a Role
```bash
# Install all recommended skills for a role
cd /Users/Jacob/clawd && .venv/bin/python -c "
import subprocess
role = 'dev'  # dev, qa, ops, analyst, editor, pm, hr
skills = {
    'dev': ['conventional-commits', 'github-pr', 'gitload'],
    'qa': ['github-pr'],  # Add pytest, coverage when available
    'ops': ['linux-service-triage', 'deploy-agent'],
    'analyst': ['browser', 'canvas'],
    'editor': ['frontend-design', 'ui-audit'],
    'pm': ['deepwiki'],
    'hr': ['agentlens', 'perry-workspaces']
}.get(role, [])

for skill in skills:
    subprocess.run(['npx', 'clawdhub@latest', 'install', skill], check=False)
print(f'Installed {len(skills)} skills for {role}')
"
```

### Verify Installed Skills
```bash
# List all installed skills
cd /Users/Jacob/clawd && ls -la ~/.openclaw/skills/ 2>/dev/null || echo "No global skills installed"
cd /Users/Jacob/clawd && ls -la skills/ 2>/dev/null || echo "No workspace skills installed"
```

### Update All Skills
```bash
# Update all installed skills to latest
cd /Users/Jacob/clawd && .venv/bin/python -c "
import subprocess
import os

skill_dirs = [
    os.path.expanduser('~/.openclaw/skills/'),
    'skills/'
]

for skill_dir in skill_dirs:
    if os.path.exists(skill_dir):
        for skill in os.listdir(skill_dir):
            skill_path = os.path.join(skill_dir, skill)
            if os.path.isdir(skill_path):
                print(f'Updating {skill}...')
                subprocess.run(['npx', 'clawdhub@latest', 'install', skill], check=False)
"
```

### Check Skill Availability
```bash
# Verify specific skill is installed
cd /Users/Jacob/clawd && test -d ~/.openclaw/skills/claude-team && echo "✅ claude-team installed" || echo "❌ claude-team not found"
```

## Configuration

### skill-config.yaml
Create this file to customize role presets:

```yaml
# /Users/Jacob/clawd/config/skill-config.yaml
installation_mode: global  # global | workspace | local

roles:
  dev:
    - conventional-commits
    - github-pr
    - gitload
    
  qa:
    - github-pr
    # - pytest  # Uncomment when available
    # - coverage
    
  ops:
    - linux-service-triage
    - deploy-agent
    
  analyst:
    - browser
    - canvas
    
  editor:
    - frontend-design
    - ui-audit
    
  pm:
    - deepwiki
    
  hr:
    - agentlens
    - perry-workspaces
    
  # Custom role example
  data-engineer:
    - browser
    - canvas
    - agentlens
```

## Quick Start

### Setup New Team Member
```bash
# 1. Choose role
ROLE=dev

# 2. Install skills for role
cd /Users/Jacob/clawd && .venv/bin/python scripts/install_skills.py --role $ROLE

# 3. Verify installation
cd /Users/Jacob/clawd && .venv/bin/python scripts/install_skills.py --verify $ROLE

# 4. Report to project manager
echo "✅ $ROLE skills installed and verified"
```

## Best Practices

1. **Use Global Installation for Teams**: All AI members share same skills
2. **Pin Critical Skills**: Document required skill versions
3. **Regular Updates**: Weekly skill update checks
4. **Role Separation**: Don't install all skills to all roles (security/principle of least privilege)
5. **Verify After Install**: Always test skill functionality after installation

## Troubleshooting

### Skill Not Found
```bash
# Search for skill in registry
npx clawdhub@latest search <keyword>
```

### Installation Failed
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and retry
rm -rf ~/.clawdhub/cache
npx clawdhub@latest install <skill>
```

### Permission Denied (Global Install)
```bash
# Use workspace installation instead
cd /Users/Jacob/clawd
npx clawdhub@latest install <skill> --local
```

## Integration with AI Team

### In AI_TEAM_ARCHITECTURE.md
Reference this skill for onboarding new AI team members:

```markdown
### Role Onboarding Checklist
- [ ] Define role responsibilities
- [ ] Assign skill preset via skill-manager
- [ ] Verify skill availability
- [ ] Test first task execution
```

### In Task Orchestrator
Use skill-manager to prepare execution environment:

```python
# Before dispatching QA squad
if role == "qa":
    ensure_skills_installed(["github-pr", "pytest"])
```

## Related

- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [ClawdHub Registry](https://clawdhub.com)
- [Skill Development Guide](https://docs.openclaw.ai/skills)
