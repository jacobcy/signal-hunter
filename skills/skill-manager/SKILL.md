# skill-manager

**Owner: HR (Human Resources)**  
**Purpose: Configure OpenClaw skills for AI team members per project**

This is an HR-exclusive skill for managing the capability infrastructure of AI team members. HR uses this to equip each role with the necessary tools for specific projects.

---

## HR Responsibility

As HR, you are the **Skill Administrator** for the AI team:
- **Onboarding**: Equip new AI members with required skills for their role
- **Project Setup**: Configure project-specific skill sets
- **Maintenance**: Update skills when new capabilities are needed
- **Audit**: Regular skill inventory and gap analysis
- **Policy**: Define which skills each role can/cannot use

---

## When HR Uses This Skill

1. **New AI Member Onboarding**
   ```
   New Dev joining → HR installs dev skill preset
   ```

2. **New Project Initialization**
   ```
   New project starts → HR configures project skill requirements
   ```

3. **Skill Updates**
   ```
   New version available → HR updates team skills
   ```

4. **Quarterly Skill Audit**
   ```
   Review all roles → HR checks skill coverage → Report to boss
   ```

---

## Project-Level Skill Configuration

HR creates `skill-manifest.yaml` for each project:

```yaml
# /Users/Jacob/clawd/config/skill-manifest.yaml
# HR-managed: Project skill requirements

project: Signal Hunter
version: "0.3.0"
last_updated: "2026-01-31"
updated_by: "HR"

# Installation scope
installation:
  mode: global  # global | workspace | local
  # global: ~/.openclaw/skills/ (recommended for shared teams)
  # workspace: <project>/skills/ (project-specific)

# Role skill assignments
roles:
  pm:
    required:
      - claude-team          # Multi-agent orchestration
      - codex-orchestration  # Task scheduling
      - model-usage          # Cost monitoring
    optional:
      - prompt-log           # Session analysis
    
  dev:
    required:
      - coding-agent         # Multi-IDE support
      - conventional-commits # Commit formatting
      - github               # GitHub operations
      - github-pr            # PR management
    optional:
      - gitload              # Partial repo download
    
  qa:
    required:
      - github-pr            # PR testing
    optional:
      - pytest               # When available
      - coverage             # When available
    
  ops:
    required:
      - linux-service-triage # Service diagnostics
      - deploy-agent         # Deployment automation
    optional:
      - cron                 # Scheduled monitoring
    
  analyst:
    required:
      - browser              # Web scraping
      - canvas               # Visualization
    optional:
      - finance              # Financial data APIs
    
  editor:
    required:
      - frontend-design      # UI/UX design
    optional:
      - ui-audit             # Interface review
      - ux-audit             # UX evaluation
    
  hr:
    required:
      - skill-manager        # Self-reference: skill management
      - agentlens            # Codebase understanding
      - perry-workspaces     # Workspace management
    optional:
      - deepwiki             # Documentation query

# Policy: Skill restrictions
policy:
  dev:
    forbidden: []  # Dev can use most skills
  qa:
    forbidden: ["deploy-agent"]  # QA cannot deploy to production
  ops:
    forbidden: []  # Ops has broad access
```

---

## HR Commands

### 1. Discover New Skills (Skill Discovery)
```bash
# HR discovers skills by category
cd /Users/Jacob/clawd && .venv/bin/python skills/skill-manager/skill_discovery.py --category "Finance"

# HR searches skills by keyword
cd /Users/Jacob/clawd && .venv/bin/python skills/skill-manager/skill_discovery.py --keyword "test"

# HR lists all available categories
cd /Users/Jacob/clawd && .venv/bin/python skills/skill-manager/skill_discovery.py --list-categories

# HR gets recommendations for a role
cd /Users/Jacob/clawd && .venv/bin/python skills/skill-manager/skill_discovery.py --recommend analyst

# HR generates discovery report
cd /Users/Jacob/clawd && .venv/bin/python skills/skill-manager/skill_discovery.py --report
```

### 2. Onboard New AI Member
```bash
# HR equips a new team member with their role skills
cd /Users/Jacob/clawd && ./skills/skill-manager/skill-manager.sh onboard <role>

# Example: Onboard new Dev
./skills/skill-manager/skill-manager.sh onboard dev
```

### 3. Configure Project Skills
```bash
# HR reads skill-manifest.yaml and installs all required skills
cd /Users/Jacob/clawd && ./skills/skill-manager/skill-manager.sh configure-project

# This installs ALL skills for ALL roles defined in manifest
```

### 4. Verify Role Skill Compliance
```bash
# HR checks if a role has all required skills
cd /Users/Jacob/clawd && ./skills/skill-manager/skill-manager.sh verify <role>

# Example: Verify Dev compliance
./skills/skill-manager/skill-manager.sh verify dev
```

### 5. Update All Team Skills
```bash
# HR updates all installed skills to latest versions
cd /Users/Jacob/clawd && ./skills/skill-manager/skill-manager.sh update-team
```

### 6. Quarterly Skill Audit (HR → Boss Report)
```bash
# HR generates comprehensive skill audit for boss
cd /Users/Jacob/clawd && ./skills/skill-manager/skill-manager.sh audit-report

# Output: Report showing skill coverage, gaps, recommendations
```

---

## HR Workflow: New Project Setup

```
Boss: "Start new project: Signal Hunter v0.4"
    ↓
HR: Create skill-manifest.yaml
    - Define required skills per role
    - Set installation mode (global/workspace)
    - Document skill policies
    ↓
HR: Execute skill configuration
    ./skill-manager.sh configure-project
    ↓
HR: Verify all roles equipped
    ./skill-manager.sh verify-all
    ↓
HR: Report to Boss
    "✅ All 7 roles equipped with 24 skills for v0.4"
    ↓
木木: Begin task dispatch with fully-equipped team
```

---

## HR Workflow: Quarterly Skill Audit

```
HR: Run quarterly audit
    ./skill-manager.sh audit-report
    ↓
HR: Analyze results
    - Check skill coverage by role
    - Identify missing required skills
    - Review optional skill adoption
    - Assess new skill needs
    ↓
HR: Generate report for Boss
    📊 Skill Audit Report Q1 2026
    
    Coverage: 18/24 required skills (75%)
    Gaps:
      - QA: pytest not yet available
      - Analyst: finance skills pending
    
    Recommendations:
      1. Install new finance skills for Analyst
      2. Update all skills to v2.x
      3. Evaluate new claude-team features
    ↓
Boss: Review and approve recommendations
    ↓
HR: Execute approved changes
```

---

## Skill Inventory Management

### Global vs Workspace Installation

**Global (`~/.openclaw/skills/`)** - HR Default Choice
- ✅ All projects share same skills
- ✅ Consistent team capability
- ✅ Easier maintenance
- ✅ Recommended for most teams

**Workspace (`<project>/skills/`)** - HR Special Cases
- ✅ Project-specific skill versions
- ✅ Isolation between projects
- ⚠️ More maintenance overhead
- Use when: Skill version conflicts between projects

**HR Decision Matrix:**
| Scenario | HR Recommendation |
|----------|-------------------|
| Single AI team, multiple projects | Global installation |
| Different projects need different skill versions | Workspace installation |
| Experimental/temporary project | Local installation |

---

## Skill Policy Enforcement

HR defines and enforces skill policies:

```yaml
# skill-policy.yaml - HR-managed
policies:
  principle_of_least_privilege:
    description: "Roles only get skills they need"
    enforcement: strict
    
  production_safety:
    description: "QA cannot have deploy skills"
    rules:
      - role: qa
        forbidden: ["deploy-agent", "linux-service-triage"]
      - role: dev
        forbidden: ["deploy-agent"]  # Dev code, Ops deploy
```

---

## Integration with AI Team Architecture

### HR Skill Manifest Location
```
/Users/Jacob/clawd/
├── config/
│   └── skill-manifest.yaml      # ← HR-managed
├── skills/
│   └── skill-manager/           # ← HR's tool
│       ├── SKILL.md
│       └── install_skills.py
└── docs/
    └── AI_TEAM_ARCHITECTURE.md  # ← References HR skill management
```

### HR Reporting to Boss

**Weekly Skill Status (HR → Boss):**
```
📋 Skill Management Report (HR)
Week: 2026-W05

✅ Onboarded: 1 new Dev (5 skills installed)
✅ Updated: 3 skills to latest versions
⚠️ Pending: pytest skill not yet available in registry
📊 Coverage: 18/24 required skills (75%)

Action Items:
1. Monitor pytest availability
2. Plan Q1 skill audit for next week
```

---

## HR Onboarding Checklist

For new AI team members:

- [ ] Define role responsibilities with Boss
- [ ] Review skill-manifest.yaml for role requirements
- [ ] Install required skills using skill-manager
- [ ] Verify skill functionality (test each tool)
- [ ] Document any skill gaps or issues
- [ ] Brief AI member on available skills
- [ ] Add to quarterly audit schedule

---

## Troubleshooting (HR Guide)

### Skill Not in Registry
```bash
# HR searches for alternative skills
npx clawdhub@latest search <keyword>

# Or checks awesome-openclaw-skills repo
# https://github.com/VoltAgent/awesome-openclaw-skills
```

### Installation Permission Denied
```bash
# HR switches to workspace installation
# Edit skill-manifest.yaml:
installation:
  mode: workspace  # Instead of global
```

### Skill Version Conflict
```bash
# HR pins specific version in manifest
roles:
  dev:
    required:
      - name: github
        version: "^2.0.0"  # Semantic versioning
```

---

## Best Practices for HR

1. **Document Everything**: Every skill change in skill-manifest.yaml
2. **Version Control**: Commit skill-manifest.yaml changes to git
3. **Regular Audits**: Monthly skill inventory, quarterly full audit
4. **Policy First**: Define policies before installing skills
5. **Test Before Deploy**: Verify skills work in test environment
6. **Gradual Rollout**: Pilot new skills with one role before team-wide
7. **Keep Manifest Updated**: Remove unused skills, add new requirements

---

## Related Resources

- **Awesome Skills**: https://github.com/VoltAgent/awesome-openclaw-skills
- **ClawdHub Registry**: https://clawdhub.com
- **AI Team Architecture**: `docs/AI_TEAM_ARCHITECTURE.md`
- **Skill Development**: https://docs.openclaw.ai/skills
