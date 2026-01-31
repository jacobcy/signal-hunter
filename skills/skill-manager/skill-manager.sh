#!/bin/bash
# Skill Manager Wrapper Script
# Quick commands for managing OpenClaw skills

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${SCRIPT_DIR}/../../.venv/bin/python"

show_help() {
    echo "Skill Manager - Manage OpenClaw skills for AI team"
    echo ""
    echo "Usage: ./skill-manager.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  install <role>     Install skills for a role (dev, qa, ops, analyst, editor, pm, hr)"
    echo "  verify <role>      Verify skills for a role"
    echo "  update             Update all installed skills"
    echo "  list               List all installed skills"
    echo "  audit              Full skill audit report"
    echo "  help               Show this help"
    echo ""
    echo "Examples:"
    echo "  ./skill-manager.sh install dev      # Install all dev skills"
    echo "  ./skill-manager.sh verify qa        # Verify QA skills are installed"
    echo "  ./skill-manager.sh audit            # Full team skill audit"
}

case "$1" in
    install)
        if [ -z "$2" ]; then
            echo "❌ Error: Please specify a role"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --role "$2"
        ;;
    verify)
        if [ -z "$2" ]; then
            echo "❌ Error: Please specify a role"
            echo "Available roles: dev, qa, ops, analyst, editor, pm, hr"
            exit 1
        fi
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --verify "$2"
        ;;
    update)
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --update
        ;;
    list)
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --list
        ;;
    audit)
        "$PYTHON" "${SCRIPT_DIR}/install_skills.py" --audit
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
