#!/usr/bin/env python3
"""
Skill Manager - Install and manage OpenClaw skills for AI team members.

Usage:
    python install_skills.py --role dev      # Install all skills for dev role
    python install_skills.py --verify dev    # Verify skills for dev role
    python install_skills.py --update        # Update all installed skills
    python install_skills.py --list          # List all installed skills
    python install_skills.py --audit         # Full skill audit report
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional

# Role-based skill presets
ROLE_SKILLS: Dict[str, List[str]] = {
    "pm": [
        "claude-team",
        "codex-orchestration",
        "model-usage",
        "prompt-log",
        "session-logs",
        "cron",
        "deepwiki",
    ],
    "dev": [
        "coding-agent",
        "conventional-commits",
        "github",
        "github-pr",
        "gitload",
    ],
    "qa": [
        "github-pr",
        # "pytest",  # Add when available
        # "coverage",
    ],
    "ops": [
        "linux-service-triage",
        "deploy-agent",
        "cron",
    ],
    "analyst": [
        "browser",
        "canvas",
        # "finance",  # Search for financial skills
    ],
    "editor": [
        "frontend-design",
        "ui-audit",
        "ux-audit",
    ],
    "hr": [
        "agentlens",
        "perry-workspaces",
        "deepwiki",
    ],
}

SKILL_DIRS = [
    Path.home() / ".openclaw" / "skills",  # Global
    Path("skills"),  # Workspace
]


def run_command(cmd: List[str], check: bool = False) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def install_skill(skill: str, mode: str = "global") -> bool:
    """Install a single skill using clawdhub CLI."""
    print(f"  📦 Installing {skill}...", end=" ")
    
    cmd = ["npx", "clawdhub@latest", "install", skill]
    if mode == "local":
        cmd.append("--local")
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print("✅")
        return True
    else:
        print(f"❌ ({stderr[:50]}...)")
        return False


def install_role_skills(role: str, mode: str = "global") -> Dict[str, bool]:
    """Install all skills for a specific role."""
    if role not in ROLE_SKILLS:
        print(f"❌ Unknown role: {role}")
        print(f"Available roles: {', '.join(ROLE_SKILLS.keys())}")
        return {}
    
    skills = ROLE_SKILLS[role]
    print(f"\n🎯 Installing {len(skills)} skills for role: {role.upper()}")
    print("=" * 50)
    
    results = {}
    for skill in skills:
        results[skill] = install_skill(skill, mode)
    
    print("=" * 50)
    success_count = sum(results.values())
    print(f"\n✅ {success_count}/{len(skills)} skills installed successfully")
    
    if success_count < len(skills):
        failed = [s for s, ok in results.items() if not ok]
        print(f"❌ Failed: {', '.join(failed)}")
    
    return results


def verify_role_skills(role: str) -> Dict[str, bool]:
    """Verify all skills for a role are installed."""
    if role not in ROLE_SKILLS:
        print(f"❌ Unknown role: {role}")
        return {}
    
    skills = ROLE_SKILLS[role]
    print(f"\n🔍 Verifying skills for role: {role.upper()}")
    print("=" * 50)
    
    results = {}
    for skill in skills:
        installed = is_skill_installed(skill)
        status = "✅" if installed else "❌"
        print(f"  {status} {skill}")
        results[skill] = installed
    
    print("=" * 50)
    installed_count = sum(results.values())
    print(f"\n{installed_count}/{len(skills)} skills verified")
    
    return results


def is_skill_installed(skill: str) -> bool:
    """Check if a skill is installed in any skill directory."""
    for skill_dir in SKILL_DIRS:
        if (skill_dir / skill).exists():
            return True
    return False


def list_installed_skills() -> List[str]:
    """List all installed skills."""
    skills = set()
    
    print("\n📋 Installed Skills")
    print("=" * 50)
    
    for skill_dir in SKILL_DIRS:
        if skill_dir.exists():
            print(f"\n📁 {skill_dir}:")
            for item in skill_dir.iterdir():
                if item.is_dir():
                    print(f"  ✅ {item.name}")
                    skills.add(item.name)
        else:
            print(f"\n📁 {skill_dir}: (not found)")
    
    print("=" * 50)
    print(f"\nTotal unique skills: {len(skills)}")
    
    return sorted(skills)


def update_all_skills() -> Dict[str, bool]:
    """Update all installed skills to latest versions."""
    installed = list_installed_skills()
    
    if not installed:
        print("\n⚠️ No skills installed")
        return {}
    
    print(f"\n🔄 Updating {len(installed)} skills...")
    print("=" * 50)
    
    results = {}
    for skill in installed:
        print(f"\n📦 Updating {skill}...")
        results[skill] = install_skill(skill)
    
    print("=" * 50)
    success_count = sum(results.values())
    print(f"\n✅ {success_count}/{len(installed)} skills updated")
    
    return results


def audit_skills() -> Dict:
    """Generate a full audit report of all skills."""
    print("\n🔍 Skill Audit Report")
    print("=" * 60)
    
    audit = {
        "installed": [],
        "by_role": {},
        "missing_by_role": {},
    }
    
    # Get all installed skills
    for skill_dir in SKILL_DIRS:
        if skill_dir.exists():
            for item in skill_dir.iterdir():
                if item.is_dir():
                    audit["installed"].append({
                        "name": item.name,
                        "location": str(skill_dir),
                        "has_skill_md": (item / "SKILL.md").exists(),
                    })
    
    # Check each role
    for role, skills in ROLE_SKILLS.items():
        installed = [s for s in skills if is_skill_installed(s)]
        missing = [s for s in skills if not is_skill_installed(s)]
        
        audit["by_role"][role] = installed
        audit["missing_by_role"][role] = missing
    
    # Print report
    print(f"\n📊 Total installed skills: {len(audit['installed'])}")
    
    print("\n📋 Skills by Role:")
    for role, skills in ROLE_SKILLS.items():
        installed = audit["by_role"][role]
        missing = audit["missing_by_role"][role]
        status = "✅" if not missing else "⚠️"
        print(f"\n  {status} {role.upper()}: {len(installed)}/{len(skills)} skills")
        if missing:
            for m in missing:
                print(f"      ❌ Missing: {m}")
    
    print("\n" + "=" * 60)
    
    return audit


def main():
    parser = argparse.ArgumentParser(
        description="Manage OpenClaw skills for AI team members"
    )
    parser.add_argument(
        "--role",
        choices=list(ROLE_SKILLS.keys()),
        help="Install skills for a specific role"
    )
    parser.add_argument(
        "--verify",
        choices=list(ROLE_SKILLS.keys()),
        help="Verify skills for a specific role"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update all installed skills"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all installed skills"
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Generate full skill audit report"
    )
    parser.add_argument(
        "--mode",
        choices=["global", "workspace", "local"],
        default="global",
        help="Installation mode (default: global)"
    )
    
    args = parser.parse_args()
    
    if args.role:
        results = install_role_skills(args.role, args.mode)
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.verify:
        results = verify_role_skills(args.verify)
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.update:
        results = update_all_skills()
        sys.exit(0)
    
    elif args.list:
        list_installed_skills()
        sys.exit(0)
    
    elif args.audit:
        audit_skills()
        sys.exit(0)
    
    else:
        parser.print_help()
        print("\n\nAvailable roles:")
        for role, skills in ROLE_SKILLS.items():
            print(f"  {role}: {', '.join(skills[:3])}...")


if __name__ == "__main__":
    main()
