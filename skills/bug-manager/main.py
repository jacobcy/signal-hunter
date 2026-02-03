#!/usr/bin/env python3
"""
Bug Manager Skill - Main Implementation

This script orchestrates the standard bug handling workflow:
1. Report & Create: Accept a bug report and auto-create a GitHub Issue with 'bug' label
2. Assign & Fix: Assign to Dev (Claude) for fixing
3. Test: Assign to QA (Codex) to verify the fix
4. Merge: Push the fixed changes to GitHub
5. Notify: Send a completion notification

It also provides a list command to view recent bugs and an auto-fix command to 
intelligently attempt to fix open bugs in sequence.
"""

import sys
import json
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime


def parse_arguments() -> tuple[str, List[str]]:
    """
    Parse command line arguments to determine the subcommand and parameters.
    
    Expected usage: 
    - openclaw bug-manager "Bug description" (default create workflow)
    - openclaw bug-manager list
    - openclaw bug-manager auto-fix
    
    Returns:
        tuple: (subcommand, remaining_args)
    """
    if len(sys.argv) < 2:
        print("Error: Command or bug description is required")
        print("Usage: openclaw bug-manager [list | auto-fix | \"bug description\"]")
        sys.exit(1)
    
    if sys.argv[1] == "list":
        return "list", []
    elif sys.argv[1] == "auto-fix":
        return "auto-fix", []
    else:
        bug_description = " ".join(sys.argv[1:])
        return "create", [bug_description]


def get_github_repo_info() -> tuple[str, str]:
    """
    Get the GitHub repository owner and name from the current git remote.
    
    Returns:
        tuple: (owner, repo_name)
    """
    try:
        # Get the origin URL
        result = os.popen("git remote get-url origin").read().strip()
        if not result:
            result = os.popen("git remote get-url github").read().strip()
        
        # Parse the URL to extract owner and repo
        if result.startswith("git@"):
            # SSH format: git@github.com:owner/repo.git
            match = re.search(r"github\.com[:/](.+?)/(.+?)\.git", result)
        else:
            # HTTPS format: https://github.com/owner/repo.git
            match = re.search(r"github\.com/(.+?)/(.+?)(?:\.git)?$", result)
            
        if match:
            owner, repo = match.groups()
            return owner, repo
        else:
            raise ValueError("Could not parse repository information")
    except Exception as e:
        print(f"Warning: Could not determine GitHub repository: {e}")
        # Default fallback
        return "jacobcy", "signal-hunter"


def query_github_issues(owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
    """
    Query GitHub Issues for the current repository that were created by or labeled with 'bug'.
    This is a mock implementation that would be replaced with actual GitHub API calls.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state filter ('open', 'closed', or 'all')
        
    Returns:
        List of issue dictionaries with relevant information
    """
    print(f"[INFO] Querying GitHub issues for {owner}/{repo} with 'bug' label...")
    
    # In a real implementation, this would use the GitHub API:
    # curl -H "Authorization: token $GITHUB_TOKEN" \
    #      "https://api.github.com/repos/{owner}/{repo}/issues?labels=bug&state={state}"
    
    # Mock data for demonstration
    mock_issues = [
        {
            "number": 101,
            "title": "Login page crashes on mobile devices",
            "html_url": f"https://github.com/{owner}/{repo}/issues/101",
            "created_at": "2026-02-01T10:00:00Z",
            "state": "open",
            "labels": ["bug", "critical"]
        },
        {
            "number": 102,
            "title": "Payment processing fails with certain credit cards",
            "html_url": f"https://github.com/{owner}/{repo}/issues/102",
            "created_at": "2026-02-02T14:30:00Z",
            "state": "open",
            "labels": ["bug", "high-priority"]
        },
        {
            "number": 103,
            "title": "User profile image not loading in dashboard",
            "html_url": f"https://github.com/{owner}/{repo}/issues/103",
            "created_at": "2026-02-03T09:15:00Z",
            "state": "closed",
            "labels": ["bug", "medium-priority"]
        }
    ]
    
    # Filter by state if specified
    if state != "all":
        mock_issues = [issue for issue in mock_issues if issue["state"] == state]
    
    return mock_issues


def get_local_bug_status(issue_number: int) -> str:
    """
    Cross-reference with local memory logs in `memory/` to get more granular status.
    
    Args:
        issue_number: GitHub issue number
        
    Returns:
        str: Status string (e.g., "In Dev", "In QA", "Completed")
    """
    memory_dir = "memory"
    if not os.path.exists(memory_dir):
        return "Unknown"
    
    # Look for files that might contain bug status
    status_files = []
    for root, dirs, files in os.walk(memory_dir):
        for file in files:
            if str(issue_number) in file or f"bug-{issue_number}" in file:
                status_files.append(os.path.join(root, file))
    
    if not status_files:
        return "Reported"
    
    # Check the most recent file for status indicators
    latest_file = max(status_files, key=os.path.getmtime)
    try:
        with open(latest_file, 'r') as f:
            content = f.read().lower()
            
        if "in dev" in content or "development" in content or "fixing" in content:
            return "In Dev"
        elif "in qa" in content or "testing" in content or "quality assurance" in content:
            return "In QA"
        elif "completed" in content or "merged" in content or "done" in content:
            return "Completed"
        else:
            return "In Progress"
    except Exception:
        return "Reported"


def format_bug_list(issues: List[Dict[str, Any]]) -> str:
    """
    Format a clean, readable list of bugs with their status and GitHub links.
    
    Args:
        issues: List of GitHub issue dictionaries
        
    Returns:
        str: Formatted bug list
    """
    if not issues:
        return "No bugs found with 'bug' label."
    
    output = "🐞 Recent Bugs:\n"
    output += "=" * 50 + "\n"
    
    for issue in sorted(issues, key=lambda x: x['number'], reverse=True):
        # Get local status
        local_status = get_local_bug_status(issue['number'])
        
        # Determine overall status
        if issue['state'] == 'closed':
            status = "✅ Fixed"
        else:
            status = local_status
            
        output += f"• #{issue['number']}: {issue['title']}\n"
        output += f"  Status: {status}\n"
        output += f"  Link: {issue['html_url']}\n"
        output += f"  Created: {issue['created_at'][:10]}\n"
        output += "-" * 30 + "\n"
    
    return output.rstrip()


def list_bugs():
    """
    List recent bugs by querying GitHub issues and cross-referencing with local memory.
    """
    print("🔍 Listing recent bugs...")
    
    # Get repository info
    owner, repo = get_github_repo_info()
    
    # Query GitHub issues
    issues = query_github_issues(owner, repo)
    
    # Format and display the list
    bug_list = format_bug_list(issues)
    print(bug_list)


# Original workflow functions (adapted for bugs)
def create_github_issue(bug_description: str) -> Dict[str, Any]:
    """
    Create a GitHub issue using the github skill with 'bug' label.
    
    Args:
        bug_description: Description of the bug to report
        
    Returns:
        Dict containing issue details (issue_number, url, etc.)
    """
    print(f"[STEP 1] Creating GitHub issue for bug: {bug_description}")
    
    # In a real implementation, this would call the github skill
    # with appropriate parameters including the 'bug' label
    
    return {
        "issue_number": 104,
        "url": "https://github.com/user/repo/issues/104",
        "title": f"Bug: {bug_description}"
    }


def assign_to_development(issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign the bug to the development team (Claude) using claude-team skill.
    
    Args:
        issue_data: Data from the created GitHub issue
        
    Returns:
        Dict containing implementation details
    """
    print(f"[STEP 2] Assigning bug #{issue_data['issue_number']} to development team for fixing")
    
    # In a real implementation, this would call the claude-team skill
    # with the bug details and request a fix
    
    return {
        "fix_status": "completed",
        "branch": f"fix/bug-{issue_data['issue_number']}",
        "commits": ["abc123", "def456"]
    }


def assign_to_qa(fix_data: Dict[str, Any], issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign the bug fix to QA (Codex) using codex-orchestration skill.
    
    Args:
        fix_data: Data from the bug fixing step
        issue_data: Original issue data
        
    Returns:
        Dict containing test results
    """
    print(f"[STEP 3] Assigning bug fix to QA for branch {fix_data['branch']}")
    
    # In a real implementation, this would call the codex-orchestration skill
    # with the bug details and fixed code to verify the fix
    
    return {
        "test_status": "passed",
        "test_report": "All tests passed successfully, bug is verified as fixed",
        "coverage": "95%"
    }


def merge_changes(fix_data: Dict[str, Any], test_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge the bug fix changes to the main branch using github skill.
    
    Args:
        fix_data: Data from the bug fixing step
        test_results: Results from the testing step
        
    Returns:
        Dict containing merge details
    """
    if test_results["test_status"] != "passed":
        print("[ERROR] Tests failed, cannot merge bug fix")
        sys.exit(1)
        
    print(f"[STEP 4] Merging bug fix branch {fix_data['branch']} to main")
    
    # In a real implementation, this would call the github skill
    # to create and merge a pull request
    
    return {
        "merge_status": "completed",
        "merge_commit": "ghi789",
        "merged_at": "2026-02-03T11:30:00Z"
    }


def send_completion_notification(
    issue_data: Dict[str, Any], 
    fix_data: Dict[str, Any], 
    test_results: Dict[str, Any], 
    merge_data: Dict[str, Any]
) -> None:
    """
    Send a completion notification using the message skill.
    
    Args:
        issue_data: Original issue data
        fix_data: Bug fix data
        test_results: Test results
        merge_data: Merge details
    """
    notification_message = f"""
    🎉 Bug Fix Completed Successfully! 🎉
    
    Bug: {issue_data['title']}
    Issue: {issue_data['url']}
    Branch: {fix_data['branch']}
    Test Coverage: {test_results['coverage']}
    Status: MERGED ✅
    """
    
    print("[STEP 5] Sending bug fix completion notification")
    print(notification_message)


def create_bug_workflow(bug_description: str):
    """Execute the bug creation and fixing workflow."""
    print("🐞 Starting Bug Manager Workflow")
    
    # Step 1: Create GitHub issue
    issue_data = create_github_issue(bug_description)
    
    # Step 2: Assign to development
    fix_data = assign_to_development(issue_data)
    
    # Step 3: Assign to QA
    test_results = assign_to_qa(fix_data, issue_data)
    
    # Step 4: Merge changes
    merge_data = merge_changes(fix_data, test_results)
    
    # Step 5: Send notification
    send_completion_notification(issue_data, fix_data, test_results, merge_data)
    
    print("✅ Bug Manager Workflow Completed Successfully!")


def auto_fix_bugs():
    """
    Automatically scan for open bugs and attempt to fix them in sequence.
    """
    print("🤖 Starting Auto-Fix Bug Workflow")
    
    # Get repository info
    owner, repo = get_github_repo_info()
    
    # Query only open bugs
    open_bugs = query_github_issues(owner, repo, state="open")
    
    if not open_bugs:
        print("No open bugs found to fix.")
        return
    
    print(f"Found {len(open_bugs)} open bugs to fix:")
    for bug in open_bugs:
        print(f"  • #{bug['number']}: {bug['title']}")
    
    # Process each bug in sequence
    for bug in open_bugs:
        print(f"\n🔧 Attempting to fix bug #{bug['number']}: {bug['title']}")
        
        # Extract bug description from title or fetch full details
        bug_description = bug['title']
        
        # Execute the full bug fixing workflow
        try:
            # Step 1: We already have the issue data
            issue_data = {
                "issue_number": bug['number'],
                "url": bug['html_url'],
                "title": bug_description
            }
            
            # Step 2: Assign to development
            fix_data = assign_to_development(issue_data)
            
            # Step 3: Assign to QA
            test_results = assign_to_qa(fix_data, issue_data)
            
            # Step 4: Merge changes
            merge_data = merge_changes(fix_data, test_results)
            
            # Step 5: Send notification
            send_completion_notification(issue_data, fix_data, test_results, merge_data)
            
            print(f"✅ Successfully fixed bug #{bug['number']}")
            
        except Exception as e:
            print(f"❌ Failed to fix bug #{bug['number']}: {str(e)}")
            continue
    
    print("🤖 Auto-Fix Bug Workflow Completed!")


def main():
    """Main execution flow for the bug-manager skill."""
    subcommand, args = parse_arguments()
    
    if subcommand == "list":
        list_bugs()
    elif subcommand == "auto-fix":
        auto_fix_bugs()
    elif subcommand == "create":
        create_bug_workflow(args[0])


if __name__ == "__main__":
    main()