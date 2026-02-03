# Skill Manager

The Skill Manager is a comprehensive tool for discovering, installing, creating, and managing OpenClaw skills.

## Commands

### Discovery Commands

- **Search for skills**:  
  `./skill-manager.sh search <keyword>`  
  Search for skills by keyword in name, description, or category.

- **List categories**:  
  `./skill-manager.sh list-categories`  
  Display all available skill categories with counts.

- **Show trending skills**:  
  `./skill-manager.sh trending`  
  Display recently added skills.

- **Get role recommendations**:  
  `./skill-manager.sh recommend <role>`  
  Get skill recommendations for specific roles (dev, qa, ops, analyst, editor, pm, hr).

### Management Commands

- **Onboard team member**:  
  `./skill-manager.sh onboard <role>`  
  Install all required skills for a specific role.

- **Configure project**:  
  `./skill-manager.sh configure-project`  
  Install all skills required for the entire project.

- **Verify skills**:  
  `./skill-manager.sh verify <role>`  
  Verify that all required skills for a role are installed.

- **Verify all roles**:  
  `./skill-manager.sh verify-all`  
  Verify that all roles have their required skills installed.

- **List installed skills**:  
  `./skill-manager.sh list`  
  List all currently installed skills.

### Creation Commands

- **Create new skill**:  
  `./skill-manager.sh create <skill-name>`  
  Scaffold a new skill with the standard directory structure and files.

### Update Commands

- **Update team skills**:  
  `./skill-manager.sh update-team`  
  Update all installed skills to their latest versions.

- **Auto-update skills**:  
  `./skill-manager.sh auto-update`  
  Check for updates to installed skills from their source repositories and apply them.

### Reporting Commands

- **Generate audit report**:  
  `./skill-manager.sh audit-report`  
  Generate a comprehensive audit report of skill compliance.

- **Generate discovery report**:  
  `./skill-manager.sh discovery-report`  
  Generate a detailed report of available skills for HR evaluation.

## Usage Examples

```bash
# Search for finance-related skills
./skill-manager.sh search finance

# Onboard a new developer
./skill-manager.sh onboard dev

# Create a new custom skill
./skill-manager.sh create my-custom-skill

# Update all installed skills
./skill-manager.sh auto-update

# Generate an audit report for management
./skill-manager.sh audit-report
```

## Cron Integration

The auto-update feature can be scheduled via cron for regular maintenance:

```bash
# Update skills every day at 2 AM
0 2 * * * /path/to/skill-manager.sh auto-update
```

## File Structure

- `skill_discovery.py`: Handles skill discovery and searching functionality
- `install_skills.py`: Manages installation and verification of skills
- `auto_update_skills.py`: Checks for and applies updates to installed skills
- `skill-manager.sh`: Unified entry point script that integrates all functionality