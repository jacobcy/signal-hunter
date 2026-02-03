#!/bin/bash
# Skill Manager - Unified entry point for OpenClaw skill management
# Usage: ./skill-manager.sh <command> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${SCRIPT_DIR}/../../.venv/bin/python"

show_help() {
    echo "Skill Manager - Unified tool for OpenClaw skill management"
    echo ""
    echo "Usage: ./skill-manager.sh <command> [options]"
    echo ""
    echo "Skill Discovery Commands:"
    echo "  search <keyword>       Search for skills by keyword"
    echo "  create <skill-name>    Scaffold a new skill"
    echo "  list-categories        List all available skill categories"
    echo ""
    echo "Skill Management Commands:"
    echo "  onboard <role>         Onboard new AI team member (dev, qa, ops, analyst, editor, pm, hr)"
    echo "  configure-project      Configure all skills for entire project"
    echo "  verify <role>          Verify skills for specific role"
    echo "  verify-all             Verify all roles have required skills"
    echo "  update-team            Update all team skills to latest"
    echo "  audit-report           Generate HR audit report for Boss"
    echo "  list                   List all installed skills"
    echo ""
    echo "Auto-Update Commands:"
    echo "  auto-update            Check for and apply updates to installed skills"
    echo "  auto-update --dry-run  Check for updates without applying them"
    echo ""
    echo "Examples:"
    echo "  ./skill-manager.sh search finance     # Search for finance-related skills"
    echo "  ./skill-manager.sh create my-skill   # Create a new skill named 'my-skill'"
    echo "  ./skill-manager.sh onboard dev       # Onboard new Dev team member"
    echo "  ./skill-manager.sh auto-update       # Update all installed skills"
    echo ""
}

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

case "$1" in
    search)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a keyword to search for${NC}"
            exit 1
        fi
        "$PYTHON" "${SCRIPT_DIR}/skill_discovery.py" search "$2"
        ;;
    create)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a skill name${NC}"
            exit 1
        fi
        "$PYTHON" "${SCRIPT_DIR}/skill_discovery.py" create "$2"
        ;;
    list-categories)
        "$PYTHON" "${SCRIPT_DIR}/skill_discovery.py" list-categories
        ;;
    onboard)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a role${NC}"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        echo -e "${YELLOW}👋 Onboarding: $2${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --onboard "$2"
        ;;
    configure-project)
        echo -e "${YELLOW}🏗️  Configuring Project${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --configure-project
        ;;
    verify)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a role${NC}"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        echo -e "${YELLOW}🔍 Verifying: $2${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --verify "$2"
        ;;
    verify-all)
        echo -e "${YELLOW}🔍 Verifying All Roles${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --verify-all
        ;;
    update-team)
        echo -e "${YELLOW}🔄 Updating Team Skills${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --update-team
        ;;
    audit-report)
        echo -e "${YELLOW}📊 Generating Audit Report${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --audit-report
        ;;
    list)
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --list
        ;;
    auto-update)
        if [ "$2" = "--dry-run" ]; then
            echo -e "${YELLOW}🔍 Checking for updates (dry run)${NC}"
            "$PYTHON" "${SCRIPT_DIR}/auto_update_skills.py" --dry-run
        else
            echo -e "${YELLOW}🔄 Checking for and applying updates${NC}"
            "$PYTHON" "${SCRIPT_DIR}/auto_update_skills.py"
        fi
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac