#!/usr/bin/env python3
"""
Skill Manager - HR tool for configuring OpenClaw skills for AI team members.

HR Usage:
    python install_skills.py --onboard dev      # Onboard new Dev team member
    python install_skills.py --configure-project # Configure all project skills
    python install_skills.py --verify dev       # Verify Dev skill compliance
    python install_skills.py --verify-all       # Verify all roles
    python install_skills.py --update-team      # Update all team skills
    python install_skills.py --audit-report     # Generate HR audit report
    python install_skills.py --list             # List installed skills

This is an HR-exclusive tool for managing AI team capability infrastructure.
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


def onboard_role(role: str) -> bool:
    """HR onboards a new AI team member with required skills."""
    print(f"\n👋 HR Onboarding: {role.upper()}")
    print("=" * 60)
    print(f"Equipping new {role} with required skills...")
    
    results = install_role_skills(role)
    success = all(results.values())
    
    print("\n" + "=" * 60)
    if success:
        print(f"✅ Onboarding complete! {role.upper()} is ready.")
        print(f"\n📋 Next steps:")
        print(f"   1. Brief {role} on available skills")
        print(f"   2. Test each skill functionality")
        print(f"   3. Add to quarterly audit schedule")
    else:
        print(f"⚠️ Onboarding incomplete. Check errors above.")
    
    return success


def configure_project() -> Dict[str, bool]:
    """HR configures all skills for the entire project."""
    print("\n🏗️  HR Configuring Project: Signal Hunter")
    print("=" * 60)
    print("Installing all required skills for all roles...")
    print()
    
    all_results = {}
    for role in ROLE_SKILLS.keys():
        print(f"\n📦 Configuring {role.upper()}...")
        results = install_role_skills(role)
        all_results[role] = all(results.values())
    
    print("\n" + "=" * 60)
    success_count = sum(all_results.values())
    total_roles = len(all_results)
    print(f"\n✅ Project configuration: {success_count}/{total_roles} roles equipped")
    
    for role, success in all_results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {role.upper()}")
    
    return all_results


def verify_all_roles() -> Dict[str, bool]:
    """HR verifies all roles have required skills."""
    print("\n🔍 HR Verifying All Roles")
    print("=" * 60)
    
    all_results = {}
    for role in ROLE_SKILLS.keys():
        results = verify_role_skills(role)
        all_results[role] = all(results.values())
    
    print("\n" + "=" * 60)
    compliant = sum(all_results.values())
    total = len(all_results)
    print(f"\n✅ Compliance: {compliant}/{total} roles fully equipped")
    
    return all_results


def generate_audit_report() -> str:
    """HR generates comprehensive audit report for Boss."""
    from datetime import datetime
    
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("📊 SKILL AUDIT REPORT (HR → Boss)")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append("Project: Signal Hunter")
    report_lines.append("=" * 70)
    
    # Get all installed skills
    installed_skills = set()
    for skill_dir in SKILL_DIRS:
        if skill_dir.exists():
            for item in skill_dir.iterdir():
                if item.is_dir():
                    installed_skills.add(item.name)
    
    report_lines.append(f"\n📈 OVERVIEW")
    report_lines.append(f"   Total installed skills: {len(installed_skills)}")
    report_lines.append(f"   Total required skills: {sum(len(skills) for skills in ROLE_SKILLS.values())}")
    
    report_lines.append(f"\n📋 ROLE COMPLIANCE")
    
    compliant_roles = 0
    gaps = []
    
    for role, required_skills in ROLE_SKILLS.items():
        installed = [s for s in required_skills if s in installed_skills]
        missing = [s for s in required_skills if s not in installed_skills]
        
        coverage = len(installed) / len(required_skills) * 100 if required_skills else 0
        status = "✅" if coverage == 100 else "⚠️"
        
        report_lines.append(f"\n   {status} {role.upper()}")
        report_lines.append(f"      Coverage: {len(installed)}/{len(required_skills)} ({coverage:.0f}%)")
        
        if missing:
            gaps.append((role, missing))
            for m in missing:
                report_lines.append(f"      ❌ Missing: {m}")
        else:
            compliant_roles += 1
    
    report_lines.append(f"\n🎯 SUMMARY")
    report_lines.append(f"   Compliant roles: {compliant_roles}/{len(ROLE_SKILLS)}")
    report_lines.append(f"   Overall coverage: {(len(installed_skills) / sum(len(s) for s in ROLE_SKILLS.values())) * 100:.0f}%")
    
    if gaps:
        report_lines.append(f"\n⚠️  GAPS IDENTIFIED")
        for role, missing in gaps:
            report_lines.append(f"   {role}: {', '.join(missing)}")
    
    report_lines.append(f"\n💡 HR RECOMMENDATIONS")
    if gaps:
        report_lines.append("   1. Install missing required skills")
        report_lines.append("   2. Check ClawdHub registry for unavailable skills")
    else:
        report_lines.append("   ✅ All roles fully equipped")
    report_lines.append("   3. Schedule next audit for next week")
    
    report_lines.append("\n" + "=" * 70)
    
    report = "\n".join(report_lines)
    print(report)
    
    # Save report
    report_dir = Path("memory/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"skill-audit-{datetime.now().strftime('%Y-%m-%d')}.md"
    report_file.write_text(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="HR Skill Manager - Configure OpenClaw skills for AI team",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
HR Commands:
  --onboard <role>       Onboard new AI team member
  --configure-project    Configure all project skills
  --verify <role>        Verify role skill compliance
  --verify-all           Verify all roles
  --update-team          Update all team skills
  --audit-report         Generate HR audit report for Boss
  --list                 List installed skills

Examples:
  # HR onboarding new Dev
  python install_skills.py --onboard dev

  # HR configuring entire project
  python install_skills.py --configure-project

  # HR quarterly audit
  python install_skills.py --audit-report
        """
    )
    
    # HR commands
    parser.add_argument(
        "--onboard",
        choices=list(ROLE_SKILLS.keys()),
        help="HR: Onboard new AI team member with role skills"
    )
    parser.add_argument(
        "--configure-project",
        action="store_true",
        help="HR: Configure all skills for entire project"
    )
    parser.add_argument(
        "--verify",
        choices=list(ROLE_SKILLS.keys()),
        help="HR: Verify skills for a specific role"
    )
    parser.add_argument(
        "--verify-all",
        action="store_true",
        help="HR: Verify all roles have required skills"
    )
    parser.add_argument(
        "--update-team",
        action="store_true",
        help="HR: Update all installed skills to latest"
    )
    parser.add_argument(
        "--audit-report",
        action="store_true",
        help="HR: Generate comprehensive audit report for Boss"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all installed skills"
    )
    
    # Legacy commands (backward compatibility)
    parser.add_argument(
        "--role",
        choices=list(ROLE_SKILLS.keys()),
        help=argparse.SUPPRESS  # Hidden, use --onboard instead
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help=argparse.SUPPRESS  # Hidden, use --update-team instead
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help=argparse.SUPPRESS  # Hidden, use --audit-report instead
    )
    parser.add_argument(
        "--mode",
        choices=["global", "workspace", "local"],
        default="global",
        help="Installation mode (default: global)"
    )
    
    args = parser.parse_args()
    
    # HR commands
    if args.onboard:
        success = onboard_role(args.onboard)
        sys.exit(0 if success else 1)
    
    elif args.configure_project:
        results = configure_project()
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.verify:
        results = verify_role_skills(args.verify)
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.verify_all:
        results = verify_all_roles()
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.update_team:
        results = update_all_skills()
        sys.exit(0)
    
    elif args.audit_report:
        generate_audit_report()
        sys.exit(0)
    
    elif args.list:
        list_installed_skills()
        sys.exit(0)
    
    # Legacy command support
    elif args.role:
        results = install_role_skills(args.role, args.mode)
        sys.exit(0 if all(results.values()) else 1)
    
    elif args.update:
        results = update_all_skills()
        sys.exit(0)
    
    elif args.audit:
        audit_skills()
        sys.exit(0)
    
    else:
        parser.print_help()
        print("\n\n📋 Available Roles:")
        for role, skills in ROLE_SKILLS.items():
            print(f"  {role:12} : {len(skills)} skills")


if __name__ == "__main__":
    main()
