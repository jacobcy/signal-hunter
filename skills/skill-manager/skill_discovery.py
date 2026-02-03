#!/usr/bin/env python3
"""
Skill Discovery - Discover and create OpenClaw skills

Usage:
    ./skill_discovery.py search <keyword>     # Search for skills by keyword
    ./skill_discovery.py create <skill-name>  # Scaffold a new skill
    ./skill_discovery.py list                 # List all available categories
    ./skill_discovery.py trending             # Show trending skills
    ./skill_discovery.py recommend <role>     # Get skill recommendations for a role

This tool helps you discover existing skills and create new ones for OpenClaw.
"""

import argparse
import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
from urllib.request import urlopen
from urllib.error import URLError

# Awesome list raw URL
AWESOME_LIST_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/README.md"

# Cache for fetched content
_content_cache: Optional[str] = None


def fetch_awesome_list() -> str:
    """Fetch the awesome-openclaw-skills README."""
    global _content_cache
    if _content_cache:
        return _content_cache
    
    try:
        with urlopen(AWESOME_LIST_URL, timeout=30) as response:
            _content_cache = response.read().decode('utf-8')
            return _content_cache
    except URLError as e:
        print(f"❌ Error fetching skill list: {e}")
        sys.exit(1)


def parse_categories(content: str) -> Dict[str, List[Dict]]:
    """Parse README and extract skills by category."""
    categories = {}
    current_category = None
    
    lines = content.split('\n')
    
    for line in lines:
        # Check for category header in <summary> tags
        cat_match = re.search(r'<summary><h3.*?>(.+?)</h3></summary>', line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            categories[current_category] = []
            continue
        
        # Also match plain ### headers
        if line.startswith('### ') and '<summary>' not in line:
            cat_match = re.match(r'^###\s+(.+?)(?:\s*\(\d+\))?\s*$', line)
            if cat_match:
                current_category = cat_match.group(1).strip()
                # Skip non-skill sections
                if current_category not in ['ClawHub CLI', 'Installation', 'Manual Installation', 
                                            'Table of Contents', 'License', '🤝 Contributing']:
                    categories[current_category] = []
            continue
        
        # Parse skill entry: - [name](url) - description
        if current_category and line.strip().startswith('- ['):
            skill_match = re.match(
                r'^-\s+\[(.+?)\]\((.+?)\)\s+-\s+(.+)$',
                line.strip()
            )
            if skill_match:
                name = skill_match.group(1)
                url = skill_match.group(2)
                description = skill_match.group(3)
                
                categories[current_category].append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'category': current_category
                })
    
    return categories


def list_categories():
    """List all available categories."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    print("\n📚 Available Skill Categories")
    print("=" * 60)
    
    for i, (category, skills) in enumerate(sorted(categories.items()), 1):
        print(f"{i:2}. {category:<35} ({len(skills)} skills)")
    
    print("=" * 60)
    print(f"\nTotal categories: {len(categories)}")
    print(f"Total skills: {sum(len(s) for s in categories.values())}")


def search_by_keyword(keyword: str):
    """Search skills by keyword in name or description."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    matching = []
    keyword_lower = keyword.lower()
    
    for category, skills in categories.items():
        for skill in skills:
            if (keyword_lower in skill['name'].lower() or 
                keyword_lower in skill['description'].lower() or
                keyword_lower in category.lower()):
                skill_copy = skill.copy()
                skill_copy['matched_category'] = category
                matching.append(skill_copy)
    
    if not matching:
        print(f"\n⚠️  No skills matching keyword '{keyword}'")
        return
    
    print(f"\n🔍 Skills matching '{keyword}' ({len(matching)} results):")
    print("=" * 70)
    
    for skill in matching[:20]:  # Show first 20
        print(f"\n  📦 {skill['name']}")
        print(f"     Category: {skill['matched_category']}")
        print(f"     Description: {skill['description'][:60]}...")
        print(f"     URL: {skill['url']}")
    
    if len(matching) > 20:
        print(f"\n  ... and {len(matching) - 20} more results")


def recommend_for_role(role: str):
    """Recommend skills for a specific AI team role."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    # Role to category mapping
    role_categories = {
        'dev': ['Coding Agents & IDEs', 'Git & GitHub', 'DevOps & Cloud', 
                'CLI Utilities', 'iOS & macOS Development'],
        'qa': ['Coding Agents & IDEs', 'DevOps & Cloud', 'CLI Utilities'],
        'ops': ['DevOps & Cloud', 'CLI Utilities', 'Linux Service Triage',
                'Self-Hosted & Automation'],
        'analyst': ['Search & Research', 'AI & LLMs', 'Finance',
                    'Data Analysis', 'Browser & Automation'],
        'editor': ['Web & Frontend Development', 'Image & Video Generation',
                   'Notes & PKM', 'PDF & Documents'],
        'pm': ['Productivity & Tasks', 'Communication', 'Marketing & Sales',
               'Calendar & Scheduling', 'Search & Research'],
        'hr': ['AI & LLMs', 'Productivity & Tasks', 'Personal Development',
               'Communication']
    }
    
    if role.lower() not in role_categories:
        print(f"\n⚠️  Unknown role: {role}")
        print(f"Known roles: {', '.join(role_categories.keys())}")
        return
    
    target_categories = role_categories[role.lower()]
    
    print(f"\n🎯 Skill Recommendations for {role.upper()}")
    print("=" * 70)
    print(f"Based on categories: {', '.join(target_categories)}")
    print()
    
    recommended = []
    for cat_name in target_categories:
        for cat, skills in categories.items():
            if cat_name.lower() in cat.lower():
                recommended.extend(skills[:5])  # Top 5 from each
    
    # Remove duplicates
    seen = set()
    unique = []
    for skill in recommended:
        if skill['name'] not in seen:
            seen.add(skill['name'])
            unique.append(skill)
    
    print(f"Top {min(15, len(unique))} recommendations:")
    print("-" * 70)
    
    for i, skill in enumerate(unique[:15], 1):
        print(f"{i:2}. {skill['name']:<30} - {skill['description'][:40]}...")


def show_trending():
    """Show trending/recently added skills."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    # Get all skills, sort by category (newer categories tend to be later)
    all_skills = []
    for cat, skills in categories.items():
        all_skills.extend(skills)
    
    print("\n🔥 Trending Skills (Recently Added)")
    print("=" * 70)
    print("Note: Based on category organization in awesome list")
    print()
    
    # Show last 20 skills from the list (likely newer)
    for skill in all_skills[-20:]:
        print(f"  • {skill['name']:<30} ({skill['category']})")
        print(f"    {skill['description'][:55]}...")


def create_skill_scaffold(skill_name: str):
    """Create a new skill scaffold directory structure."""
    if not skill_name or not skill_name.strip():
        print("❌ Error: Please provide a valid skill name")
        return False
    
    skill_name = skill_name.strip()
    
    # Validate skill name (basic validation)
    if not re.match(r'^[a-zA-Z0-9_-]+$', skill_name):
        print("❌ Error: Skill name can only contain letters, numbers, hyphens, and underscores")
        return False
    
    skill_dir = Path("skills") / skill_name
    
    if skill_dir.exists():
        print(f"❌ Error: Skill directory '{skill_name}' already exists")
        return False
    
    try:
        # Create the skill directory
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Create SKILL.md
        skill_md_content = f"""# {skill_name}

## Description
Brief description of what this skill does.

## Tools
List of tools provided by this skill:

- **tool_name**: Brief description of what the tool does

## Usage
How to use this skill:

```python
# Example usage
```

## Dependencies
Any dependencies required for this skill.

## Configuration
Any configuration options for this skill.
"""
        (skill_dir / "SKILL.md").write_text(skill_md_content)
        
        # Create __init__.py
        (skill_dir / "__init__.py").write_text("# Skill initialization\n")
        
        # Create main.py (optional but recommended)
        main_py_content = f'''"""
Main module for the {skill_name} skill.
"""
'''
        (skill_dir / "main.py").write_text(main_py_content)
        
        print(f"✅ Successfully created skill scaffold: {skill_name}")
        print(f"📁 Directory: {skill_dir}")
        print(f"📄 Files created:")
        print(f"   - SKILL.md (documentation)")
        print(f"   - __init__.py (package initialization)")
        print(f"   - main.py (main module)")
        print(f"\n📝 Next steps:")
        print(f"   1. Edit SKILL.md to document your skill")
        print(f"   2. Implement your tools in main.py")
        print(f"   3. Add tool definitions to your skill's __init__.py")
        print(f"   4. Test your skill locally")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating skill scaffold: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Discover and create OpenClaw skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for skills containing "finance"
  ./skill_discovery.py search finance
  
  # Create a new skill called "my-awesome-skill"
  ./skill_discovery.py create my-awesome-skill
  
  # List all available skill categories
  ./skill_discovery.py list
  
  # Get recommendations for a developer role
  ./skill_discovery.py recommend dev
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for skills by keyword')
    search_parser.add_argument('keyword', help='Keyword to search for in skill names, descriptions, or categories')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Scaffold a new skill')
    create_parser.add_argument('skill_name', help='Name of the new skill to create')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all available skill categories')
    
    # Trending command
    trending_parser = subparsers.add_parser('trending', help='Show trending/recently added skills')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get skill recommendations for a role')
    recommend_parser.add_argument('role', choices=['dev', 'qa', 'ops', 'analyst', 'editor', 'pm', 'hr'],
                                 help='Role to get recommendations for')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'search':
        search_by_keyword(args.keyword)
    elif args.command == 'create':
        create_skill_scaffold(args.skill_name)
    elif args.command == 'list':
        list_categories()
    elif args.command == 'trending':
        show_trending()
    elif args.command == 'recommend':
        recommend_for_role(args.role)


if __name__ == "__main__":
    main()