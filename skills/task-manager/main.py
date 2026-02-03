#!/usr/bin/env python3
"""
Task Manager Skill - Main Implementation

This script orchestrates the standard task workflow:
1. Create Issue: Generate and submit a GitHub Issue
2. Develop: Assign to Dev (Claude) for implementation
3. Test: Assign to QA (Codex) for testing
4. Merge: Push changes to GitHub
5. Notify: Send a completion notification

It also provides a list command to view recent tasks.
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
    - openclaw task-manager "Implement feature X" (default create workflow)
    - openclaw task-manager list
    
    Returns:
        tuple: (subcommand, remaining_args)
    """
    if len(sys.argv) < 2:
        print("Error: Command or task description is required")
        print("Usage: openclaw task-manager [list | \"task description\"]")
        sys.exit(1)
    
    if sys.argv[1] == "list":
        return "list", []
    else:
        task_description = " ".join(sys.argv[1:])
        return "create", [task_description]


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


def query_github_issues(owner: str, repo: str) -> List[Dict[str, Any]]:
    """
    Query GitHub Issues for the current repository that were created by or labeled with 'task-manager'.
    This is a mock implementation that would be replaced with actual GitHub API calls.
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        List of issue dictionaries with relevant information
    """
    print(f"[INFO] Querying GitHub issues for {owner}/{repo} with 'task-manager' label...")
    
    # In a real implementation, this would use the GitHub API:
    # curl -H "Authorization: token $GITHUB_TOKEN" \
    #      "https://api.github.com/repos/{owner}/{repo}/issues?labels=task-manager&state=all"
    
    # Mock data for demonstration
    mock_issues = [
        {
            "number": 123,
            "title": "Implement user authentication system",
            "html_url": f"https://github.com/{owner}/{repo}/issues/123",
            "created_at": "2026-02-01T10:00:00Z",
            "state": "open",
            "labels": ["task-manager", "feature"]
        },
        {
            "number": 124,
            "title": "Fix payment processing bug",
            "html_url": f"https://github.com/{owner}/{repo}/issues/124",
            "created_at": "2026-02-02T14:30:00Z",
            "state": "closed",
            "labels": ["task-manager", "bug"]
        },
        {
            "number": 125,
            "title": "Add dark mode toggle",
            "html_url": f"https://github.com/{owner}/{repo}/issues/125",
            "created_at": "2026-02-03T09:15:00Z",
            "state": "open",
            "labels": ["task-manager", "enhancement"]
        }
    ]
    
    return mock_issues


def get_local_task_status(issue_number: int) -> str:
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
    
    # Look for files that might contain task status
    status_files = []
    for root, dirs, files in os.walk(memory_dir):
        for file in files:
            if str(issue_number) in file or f"task-{issue_number}" in file:
                status_files.append(os.path.join(root, file))
    
    if not status_files:
        return "Created"
    
    # Check the most recent file for status indicators
    latest_file = max(status_files, key=os.path.getmtime)
    try:
        with open(latest_file, 'r') as f:
            content = f.read().lower()
            
        if "in dev" in content or "development" in content or "implementing" in content:
            return "In Dev"
        elif "in qa" in content or "testing" in content or "quality assurance" in content:
            return "In QA"
        elif "completed" in content or "merged" in content or "done" in content:
            return "Completed"
        else:
            return "In Progress"
    except Exception:
        return "Created"


def format_task_list(issues: List[Dict[str, Any]]) -> str:
    """
    Format a clean, readable list of tasks with their status and GitHub links.
    
    Args:
        issues: List of GitHub issue dictionaries
        
    Returns:
        str: Formatted task list
    """
    if not issues:
        return "No tasks found with 'task-manager' label."
    
    output = "📋 Recent Tasks:\n"
    output += "=" * 50 + "\n"
    
    for issue in sorted(issues, key=lambda x: x['number'], reverse=True):
        # Get local status
        local_status = get_local_task_status(issue['number'])
        
        # Determine overall status
        if issue['state'] == 'closed':
            status = "✅ Completed"
        else:
            status = local_status
            
        output += f"• #{issue['number']}: {issue['title']}\n"
        output += f"  Status: {status}\n"
        output += f"  Link: {issue['html_url']}\n"
        output += f"  Created: {issue['created_at'][:10]}\n"
        output += "-" * 30 + "\n"
    
    return output.rstrip()


def list_tasks():
    """
    List recent tasks by querying GitHub issues and cross-referencing with local memory.
    """
    print("🔍 Listing recent tasks...")
    
    # Get repository info
    owner, repo = get_github_repo_info()
    
    # Query GitHub issues
    issues = query_github_issues(owner, repo)
    
    # Format and display the list
    task_list = format_task_list(issues)
    print(task_list)


# Original workflow functions (unchanged)
def create_github_issue(task_description: str) -> Dict[str, Any]:
    """
    Create a GitHub issue using the github skill.
    
    Args:
        task_description: Description of the task to implement
        
    Returns:
        Dict containing issue details (issue_number, url, etc.)
    """
    print(f"[STEP 1] Creating GitHub issue for: {task_description}")
    
    return {
        "issue_number": 123,
        "url": "https://github.com/user/repo/issues/123",
        "title": f"Task: {task_description}"
    }


def assign_to_development(issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign the task to the development team (Claude) using claude-team skill.
    
    Args:
        issue_data: Data from the created GitHub issue
        
    Returns:
        Dict containing implementation details
    """
    print(f"[STEP 2] Assigning to development team for issue #{issue_data['issue_number']}")
    
    return {
        "implementation_status": "completed",
        "branch": f"feature/task-{issue_data['issue_number']}",
        "commits": ["abc123", "def456"]
    }


def assign_to_qa(impl_data: Dict[str, Any], issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign the implemented feature to QA (Codex) using codex-orchestration skill.
    
    Args:
        impl_data: Data from the implementation step
        issue_data: Original issue data
        
    Returns:
        Dict containing test results
    """
    print(f"[STEP 3] Assigning to QA for branch {impl_data['branch']}")
    
    return {
        "test_status": "passed",
        "test_report": "All tests passed successfully",
        "coverage": "95%"
    }


def merge_changes(impl_data: Dict[str, Any], test_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge the changes to the main branch using github skill.
    
    Args:
        impl_data: Data from the implementation step
        test_results: Results from the testing step
        
    Returns:
        Dict containing merge details
    """
    if test_results["test_status"] != "passed":
        print("[ERROR] Tests failed, cannot merge")
        sys.exit(1)
        
    print(f"[STEP 4] Merging branch {impl_data['branch']} to main")
    
    return {
        "merge_status": "completed",
        "merge_commit": "ghi789",
        "merged_at": "2026-02-03T11:30:00Z"
    }


def send_completion_notification(
    issue_data: Dict[str, Any], 
    impl_data: Dict[str, Any], 
    test_results: Dict[str, Any], 
    merge_data: Dict[str, Any]
) -> None:
    """
    Send a completion notification using the message skill.
    
    Args:
        issue_data: Original issue data
        impl_data: Implementation data
        test_results: Test results
        merge_data: Merge details
    """
    notification_message = f"""
    🎉 Task Completed Successfully! 🎉
    
    Task: {issue_data['title']}
    Issue: {issue_data['url']}
    Branch: {impl_data['branch']}
    Test Coverage: {test_results['coverage']}
    Status: MERGED ✅
    """
    
    print("[STEP 5] Sending completion notification")
    print(notification_message)


def create_task_workflow(task_description: str):
    """Execute the original task creation workflow."""
    print("🚀 Starting Task Manager Workflow")
    
    # Step 1: Create GitHub issue
    issue_data = create_github_issue(task_description)
    
    # Step 2: Assign to development
    impl_data = assign_to_development(issue_data)
    
    # Step 3: Assign to QA
    test_results = assign_to_qa(impl_data, issue_data)
    
    # Step 4: Merge changes
    merge_data = merge_changes(impl_data, test_results)
    
    # Step 5: Send notification
    send_completion_notification(issue_data, impl_data, test_results, merge_data)
    
    print("✅ Task Manager Workflow Completed Successfully!")


def main():
    """Main execution flow for the task-manager skill."""
    subcommand, args = parse_arguments()
    
    if subcommand == "list":
        list_tasks()
    elif subcommand == "create":
        create_task_workflow(args[0])


if __name__ == "__main__":
    main()