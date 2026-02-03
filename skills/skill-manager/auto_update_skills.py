#!/usr/bin/env python3
"""
Auto Update Skills - Automatically check for and update installed OpenClaw skills

Usage:
    python auto_update_skills.py --check          # Check for updates without installing
    python auto_update_skills.py --update         # Check and install available updates
    python auto_update_skills.py --force          # Force reinstall all skills
    python auto_update_skills.py --list           # List all installed skills with sources
    python auto_update_skills.py --help           # Show help

This script checks installed skills against their source repositories (GitHub, Clawhub, etc.)
and can automatically update them to the latest versions.
"""

import argparse
import subprocess
import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import hashlib

# Skill directories to check
SKILL_DIRS = [
    Path.home() / ".openclaw" / "skills",  # Global
    Path("skills"),  # Workspace
]

# Cache file for update status
CACHE_FILE = Path("memory") / "skill_update_cache.json"

# Color constants
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def color_text(text: str, color: str) -> str:
    """Apply color to text if output is a terminal."""
    if sys.stdout.isatty():
        return f"{color}{text}{NC}"
    return text


def run_command(cmd: List[str], check: bool = False, timeout: int = 30) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def get_installed_skills() -> List[Dict]:
    """Get list of all installed skills with their metadata."""
    skills = []
    
    for skill_dir in SKILL_DIRS:
        if not skill_dir.exists():
            continue
            
        for item in skill_dir.iterdir():
            if not item.is_dir():
                continue
                
            skill_info = {
                'name': item.name,
                'path': str(item),
                'location': 'global' if 'home' in str(skill_dir) else 'workspace',
                'source': None,
                'version': None,
                'last_updated': None
            }
            
            # Try to get source from package.json or SKILL.md
            package_json = item / "package.json"
            skill_md = item / "SKILL.md"
            
            if package_json.exists():
                try:
                    pkg_data = json.loads(package_json.read_text())
                    skill_info['source'] = pkg_data.get('repository', {}).get('url')
                    skill_info['version'] = pkg_data.get('version')
                except (json.JSONDecodeError, KeyError):
                    pass
                    
            elif skill_md.exists():
                content = skill_md.read_text()
                # Look for GitHub URL or Clawhub reference
                github_match = re.search(r'https?://github\.com/[^)\s]+', content)
                if github_match:
                    skill_info['source'] = github_match.group(0)
                    
                # Look for version info
                version_match = re.search(r'version[:\s]+([^\n]+)', content, re.IGNORECASE)
                if version_match:
                    skill_info['version'] = version_match.group(1).strip()
            
            # Get last modified time
            try:
                stat = item.stat()
                skill_info['last_updated'] = datetime.fromtimestamp(stat.st_mtime)
            except OSError:
                pass
                
            skills.append(skill_info)
    
    return sorted(skills, key=lambda x: x['name'])


def is_github_repo(url: str) -> bool:
    """Check if URL is a GitHub repository."""
    return url and ('github.com' in url)


def get_github_latest_commit(repo_url: str) -> Optional[str]:
    """Get the latest commit hash from a GitHub repository."""
    if not repo_url.endswith('.git'):
        repo_url = repo_url.rstrip('/') + '.git'
    
    # Extract owner/repo from URL
    match = re.search(r'github\.com/([^/]+)/([^/.]+)', repo_url)
    if not match:
        return None
        
    owner, repo = match.groups()
    
    # Use GitHub API to get latest commit
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/main"
    
    try:
        import urllib.request
        import urllib.error
        
        req = urllib.request.Request(api_url)
        req.add_header('User-Agent', 'OpenClaw-Skill-Manager')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('sha', '')[:8]  # First 8 chars of commit hash
            
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError):
        # Fallback: try git ls-remote
        try:
            exit_code, stdout, stderr = run_command([
                'git', 'ls-remote', repo_url, 'HEAD'
            ], timeout=15)
            
            if exit_code == 0 and stdout.strip():
                return stdout.split()[0][:8]
        except:
            pass
    
    return None


def get_clawhub_latest_version(skill_name: str) -> Optional[str]:
    """Get the latest version from Clawhub for a skill."""
    try:
        # This is a simplified approach - in reality, you'd need to query Clawhub's API
        # For now, we'll assume that if we can install it, there might be an update
        exit_code, stdout, stderr = run_command([
            'npx', 'clawdhub@latest', 'info', skill_name
        ], timeout=15)
        
        if exit_code == 0:
            # Parse version from output (this is approximate)
            version_match = re.search(r'version[:\s]+([^\n]+)', stdout, re.IGNORECASE)
            if version_match:
                return version_match.group(1).strip()
    except:
        pass
    
    return None


def check_skill_for_update(skill: Dict) -> Dict:
    """Check if a skill has updates available."""
    result = {
        'name': skill['name'],
        'current_version': skill.get('version'),
        'latest_version': None,
        'has_update': False,
        'source_type': 'unknown',
        'error': None
    }
    
    source = skill.get('source')
    if not source:
        # Try to determine source type
        if skill['name'] and 'clawdhub' in str(SKILL_DIRS):  # Simplified assumption
            result['source_type'] = 'clawhub'
            latest = get_clawhub_latest_version(skill['name'])
            if latest:
                result['latest_version'] = latest
                result['has_update'] = latest != skill.get('version')
        return result
    
    if is_github_repo(source):
        result['source_type'] = 'github'
        try:
            latest_commit = get_github_latest_commit(source)
            if latest_commit:
                result['latest_version'] = latest_commit
                # For GitHub, we compare by checking if local has the latest commit
                # This is simplified - in practice, you'd need to fetch and compare
                result['has_update'] = True  # Always assume update available for GitHub
        except Exception as e:
            result['error'] = str(e)
    else:
        result['source_type'] = 'other'
    
    return result


def load_update_cache() -> Dict:
    """Load the update cache from file."""
    if not CACHE_FILE.exists():
        return {}
    
    try:
        return json.loads(CACHE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_update_cache(cache: Dict):
    """Save the update cache to file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, default=str))


def should_check_for_updates(skill_name: str, cache: Dict, force: bool = False) -> bool:
    """Check if we should check for updates for this skill."""
    if force:
        return True
        
    last_check = cache.get(skill_name, {}).get('last_check')
    if not last_check:
        return True
        
    # Don't check more than once per day
    last_check_time = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
    if datetime.now() - last_check_time > timedelta(days=1):
        return True
        
    return False


def update_skill(skill_name: str, location: str = 'global') -> bool:
    """Update a single skill using clawdhub CLI."""
    print(f"  📦 Updating {skill_name}...", end=" ")
    
    cmd = ["npx", "clawdhub@latest", "install", skill_name]
    if location == 'workspace':
        cmd.append("--local")
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        print(color_text("✅", GREEN))
        return True
    else:
        print(color_text(f"❌ ({stderr[:50]}...)", RED))
        return False


def check_for_updates(force: bool = False) -> List[Dict]:
    """Check all installed skills for updates."""
    print(color_text("🔍 Checking for skill updates...", BLUE))
    print("=" * 60)
    
    skills = get_installed_skills()
    if not skills:
        print(color_text("⚠️  No skills found", YELLOW))
        return []
    
    cache = load_update_cache()
    update_results = []
    
    for skill in skills:
        print(f"\n📋 Checking {skill['name']} ({skill['location']})")
        
        if not should_check_for_updates(skill['name'], cache, force):
            print("  ⏭️  Skipped (checked recently)")
            # Use cached result if available
            cached_result = cache.get(skill['name'], {})
            if cached_result.get('has_update'):
                update_results.append({
                    'name': skill['name'],
                    'current_version': cached_result.get('current_version'),
                    'latest_version': cached_result.get('latest_version'),
                    'has_update': True,
                    'source_type': cached_result.get('source_type', 'cached'),
                    'error': None
                })
            continue
        
        result = check_skill_for_update(skill)
        update_results.append(result)
        
        # Update cache
        cache[skill['name']] = {
            'last_check': datetime.now().isoformat(),
            'has_update': result['has_update'],
            'current_version': result['current_version'],
            'latest_version': result['latest_version'],
            'source_type': result['source_type']
        }
        
        if result['error']:
            print(f"  ❌ Error: {result['error']}")
        elif result['has_update']:
            current = result['current_version'] or 'unknown'
            latest = result['latest_version'] or 'newer'
            print(f"  🆕 Update available: {current} → {latest}")
        else:
            print("  ✅ Up to date")
    
    save_update_cache(cache)
    return update_results


def perform_updates(update_results: List[Dict]) -> Dict[str, bool]:
    """Perform updates on skills that have updates available."""
    if not update_results:
        print(color_text("⚠️  No update results to process", YELLOW))
        return {}
    
    skills_to_update = [r for r in update_results if r['has_update']]
    if not skills_to_update:
        print(color_text("✅ All skills are up to date!", GREEN))
        return {}
    
    print(color_text(f"\n🔄 Updating {len(skills_to_update)} skills...", BLUE))
    print("=" * 60)
    
    # Get skill locations to determine install mode
    installed_skills = {skill['name']: skill for skill in get_installed_skills()}
    update_results_dict = {}
    
    for result in skills_to_update:
        skill_name = result['name']
        skill_info = installed_skills.get(skill_name, {})
        location = skill_info.get('location', 'global')
        
        success = update_skill(skill_name, location)
        update_results_dict[skill_name] = success
    
    print("=" * 60)
    success_count = sum(update_results_dict.values())
    print(f"\n✅ {success_count}/{len(skills_to_update)} skills updated successfully")
    
    if success_count < len(skills_to_update):
        failed = [name for name, ok in update_results_dict.items() if not ok]
        print(color_text(f"❌ Failed updates: {', '.join(failed)}", RED))
    
    return update_results_dict


def force_reinstall_all() -> Dict[str, bool]:
    """Force reinstall all skills."""
    print(color_text("🔄 Force reinstalling all skills...", BLUE))
    print("=" * 60)
    
    skills = get_installed_skills()
    if not skills:
        print(color_text("⚠️  No skills found", YELLOW))
        return {}
    
    results = {}
    for skill in skills:
        success = update_skill(skill['name'], skill['location'])
        results[skill['name']] = success
    
    print("=" * 60)
    success_count = sum(results.values())
    print(f"\n✅ {success_count}/{len(skills)} skills reinstalled successfully")
    
    return results


def list_skills_with_sources():
    """List all installed skills with their source information."""
    print(color_text("📋 Installed Skills with Sources", BLUE))
    print("=" * 80)
    
    skills = get_installed_skills()
    if not skills:
        print(color_text("⚠️  No skills found", YELLOW))
        return
    
    for skill in skills:
        print(f"\n📦 {skill['name']}")
        print(f"   Location: {skill['location']}")
        print(f"   Path: {skill['path']}")
        if skill.get('source'):
            print(f"   Source: {skill['source']}")
        if skill.get('version'):
            print(f"   Version: {skill['version']}")
        if skill.get('last_updated'):
            age = datetime.now() - skill['last_updated']
            if age.days > 0:
                print(f"   Last updated: {age.days} days ago")
            else:
                print(f"   Last updated: today")
    
    print(f"\n{len(skills)} skills total")


def main():
    parser = argparse.ArgumentParser(
        description="Auto Update Skills - Check and update installed OpenClaw skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check for updates without installing
  python auto_update_skills.py --check
  
  # Check and install available updates
  python auto_update_skills.py --update
  
  # Force reinstall all skills
  python auto_update_skills.py --force
  
  # List all installed skills with sources
  python auto_update_skills.py --list
        """
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for updates without installing (default behavior)"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Check for updates and install available ones"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstall all skills (ignores update status)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all installed skills with source information"
    )
    
    parser.add_argument(
        "--force-check",
        action="store_true",
        help="Force check for updates even if checked recently"
    )
    
    args = parser.parse_args()
    
    # Default behavior is to check
    if not any([args.check, args.update, args.force, args.list]):
        args.check = True
    
    try:
        if args.list:
            list_skills_with_sources()
            
        elif args.force:
            force_reinstall_all()
            
        elif args.update:
            update_results = check_for_updates(force=args.force_check)
            perform_updates(update_results)
            
        elif args.check:
            check_for_updates(force=args.force_check)
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(color_text("\n\n⚠️  Operation cancelled by user", YELLOW))
        sys.exit(1)
    except Exception as e:
        print(color_text(f"\n❌ Error: {e}", RED))
        sys.exit(1)


if __name__ == "__main__":
    main()