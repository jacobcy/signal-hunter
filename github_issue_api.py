"""
GitHub Issue API - Simple importable functions for creating GitHub issues
"""

import subprocess
from typing import List, Optional, Tuple


def create_github_issue(title: str, body: str, repo: Optional[str] = None, labels: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Create a GitHub issue using the gh CLI
    
    Args:
        title (str): Title of the issue
        body (str): Body/description of the issue
        repo (str, optional): Repository in format owner/repo. If None, uses current directory
        labels (List[str], optional): List of labels to apply to the issue
    
    Returns:
        Tuple[bool, str]: (success: bool, output_or_error_message: str)
    """
    try:
        # Build the command
        cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]
        
        # Add repository if specified
        if repo:
            cmd.extend(['--repo', repo])
        
        # Add labels if specified
        if labels:
            cmd.extend(['--label', ','.join(labels)])
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        return True, result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        return False, f"Error creating issue: {e.stderr.strip()}"
    except FileNotFoundError:
        return False, "GitHub CLI ('gh') not found. Please install it first."


def create_issue_with_confirmation(title: str, body: str, repo: Optional[str] = None, labels: Optional[List[str]] = None) -> bool:
    """
    Create a GitHub issue with error handling and basic confirmation
    
    Args:
        title (str): Title of the issue
        body (str): Body/description of the issue
        repo (str, optional): Repository in format owner/repo. If None, uses current directory
        labels (List[str], optional): List of labels to apply to the issue
    
    Returns:
        bool: True if issue was created successfully, False otherwise
    """
    success, result = create_github_issue(title, body, repo, labels)
    
    if success:
        print(f"✓ Issue created successfully: {result}")
        return True
    else:
        print(f"✗ Failed to create issue: {result}")
        return False