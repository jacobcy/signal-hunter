#!/bin/bash
# Skill Manager - HR Tool for Configuring AI Team Skills
# Usage: ./skill-manager.sh <command> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${SCRIPT_DIR}/../../.venv/bin/python"

show_help() {
    echo "Skill Manager - HR Tool for AI Team Skill Configuration"
    echo ""
    echo "Usage: ./skill-manager.sh <command> [options]"
    echo ""
    echo "HR Commands:"
    echo "  onboard <role>         Onboard new AI team member (dev, qa, ops, analyst, editor, pm, hr)"
    echo "  configure-project      Configure all skills for entire project"
    echo "  verify <role>          Verify skills for specific role"
    echo "  verify-all             Verify all roles have required skills"
    echo "  update-team            Update all team skills to latest"
    echo "  audit-report           Generate HR audit report for Boss"
    echo "  list                   List all installed skills"
    echo "  help                   Show this help"
    echo ""
    echo "Examples:"
    echo "  ./skill-manager.sh onboard dev          # HR onboards new Dev"
    echo "  ./skill-manager.sh configure-project    # HR sets up entire project"
    echo "  ./skill-manager.sh verify qa            # HR verifies QA skills"
    echo "  ./skill-manager.sh audit-report         # HR generates audit for Boss"
    echo ""
    echo "Skill Manifest: config/skill-manifest.yaml"
    echo "Report Output:  memory/reports/skill-audit-YYYY-MM-DD.md"
}

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

case "$1" in
    onboard)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a role${NC}"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        echo -e "${YELLOW}👋 HR Onboarding: $2${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --onboard "$2"
        ;;
    configure-project)
        echo -e "${YELLOW}🏗️  HR Configuring Project${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --configure-project
        ;;
    verify)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please specify a role${NC}"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        echo -e "${YELLOW}🔍 HR Verifying: $2${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --verify "$2"
        ;;
    verify-all)
        echo -e "${YELLOW}🔍 HR Verifying All Roles${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --verify-all
        ;;
    update-team)
        echo -e "${YELLOW}🔄 HR Updating Team Skills${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --update-team
        ;;
    audit-report)
        echo -e "${YELLOW}📊 HR Generating Audit Report${NC}"
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --audit-report
        ;;
    list)
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --list
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
