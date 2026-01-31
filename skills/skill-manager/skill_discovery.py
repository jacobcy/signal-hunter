#!/usr/bin/env python3
"""
Skill Discovery - HR tool for discovering new OpenClaw skills

Usage:
    python skill_discovery.py --category finance    # Search by category
    python skill_discovery.py --keyword "test"      # Search by keyword
    python skill_discovery.py --list-categories     # List all categories
    python skill_discovery.py --recommend <role>    # Recommend for role
    python skill_discovery.py --trending            # Show trending skills

This is an HR tool for discovering and evaluating new skills for the AI team.
"""

import argparse
import re
import sys
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


def search_by_category(category_query: str):
    """Search skills by category name."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    # Find matching categories (case-insensitive partial match)
    matching = {
        cat: skills for cat, skills in categories.items()
        if category_query.lower() in cat.lower()
    }
    
    if not matching:
        print(f"\n⚠️  No categories matching '{category_query}'")
        print("\nUse --list-categories to see all available categories")
        return
    
    print(f"\n🔍 Skills in categories matching '{category_query}':")
    print("=" * 70)
    
    for category, skills in matching.items():
        print(f"\n📁 {category} ({len(skills)} skills)")
        print("-" * 70)
        for skill in skills[:10]:  # Show first 10
            print(f"  • {skill['name']:<25} - {skill['description'][:50]}...")
        if len(skills) > 10:
            print(f"  ... and {len(skills) - 10} more")


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


def generate_skill_report():
    """Generate comprehensive skill landscape report for HR."""
    content = fetch_awesome_list()
    categories = parse_categories(content)
    
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("📊 SKILL DISCOVERY REPORT (HR)")
    report_lines.append("Source: awesome-openclaw-skills")
    report_lines.append("=" * 70)
    
    report_lines.append(f"\n📈 OVERVIEW")
    report_lines.append(f"   Total Categories: {len(categories)}")
    report_lines.append(f"   Total Skills: {sum(len(s) for s in categories.values())}")
    
    report_lines.append(f"\n📚 TOP CATEGORIES BY SIZE")
    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    for cat, skills in sorted_cats[:10]:
        report_lines.append(f"   {cat:<35} {len(skills):3} skills")
    
    report_lines.append(f"\n🎯 HIGH-VALUE SKILLS FOR OUR TEAM")
    
    # Key skills we might need
    key_categories = [
        'Coding Agents & IDEs',
        'DevOps & Cloud', 
        'Git & GitHub',
        'Finance',
        'AI & LLMs',
        'Search & Research'
    ]
    
    for cat_name in key_categories:
        for cat, skills in categories.items():
            if cat_name.lower() in cat.lower():
                report_lines.append(f"\n   {cat}:")
                for skill in skills[:3]:
                    report_lines.append(f"      • {skill['name']}")
    
    report_lines.append("\n" + "=" * 70)
    report_lines.append("💡 HR RECOMMENDATIONS")
    report_lines.append("   1. Review Finance category for trading-related skills")
    report_lines.append("   2. Check DevOps & Cloud for deployment automation")
    report_lines.append("   3. Explore AI & LLMs for advanced capabilities")
    report_lines.append("=" * 70)
    
    report = "\n".join(report_lines)
    print(report)
    
    # Save report
    from pathlib import Path
    from datetime import datetime
    report_dir = Path("memory/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"skill-discovery-{datetime.now().strftime('%Y-%m-%d')}.md"
    report_file.write_text(report)
    print(f"\n💾 Report saved to: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="HR Skill Discovery - Find new OpenClaw skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for testing-related skills
  python skill_discovery.py --keyword "test"
  
  # List all Finance skills
  python skill_discovery.py --category "Finance"
  
  # Get recommendations for Dev role
  python skill_discovery.py --recommend dev
  
  # Generate full discovery report
  python skill_discovery.py --report
        """
    )
    
    parser.add_argument(
        "--category",
        metavar="NAME",
        help="Search skills by category (e.g., 'Finance', 'DevOps')"
    )
    parser.add_argument(
        "--keyword",
        metavar="WORD",
        help="Search skills by keyword in name/description"
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available categories"
    )
    parser.add_argument(
        "--recommend",
        metavar="ROLE",
        choices=['dev', 'qa', 'ops', 'analyst', 'editor', 'pm', 'hr'],
        help="Recommend skills for a role (dev/qa/ops/analyst/editor/pm/hr)"
    )
    parser.add_argument(
        "--trending",
        action="store_true",
        help="Show trending/recent skills"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate comprehensive discovery report"
    )
    
    args = parser.parse_args()
    
    if args.list_categories:
        list_categories()
    elif args.category:
        search_by_category(args.category)
    elif args.keyword:
        search_by_keyword(args.keyword)
    elif args.recommend:
        recommend_for_role(args.recommend)
    elif args.trending:
        show_trending()
    elif args.report:
        generate_skill_report()
    else:
        parser.print_help()
        print("\n\n💡 Quick Start:")
        print("  python skill_discovery.py --list-categories")
        print("  python skill_discovery.py --keyword ")


if __name__ == "__main__":
    main()
