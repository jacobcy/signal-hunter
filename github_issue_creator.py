#!/usr/bin/env python3
"""
GitHub Issue Creator - A simple utility to create GitHub issues via command line
"""

import subprocess
import sys
import argparse
import os


def create_github_issue(title, body, repo=None, labels=None):
    """
    Create a GitHub issue using the gh CLI
    
    Args:
        title (str): Title of the issue
        body (str): Body/description of the issue
        repo (str, optional): Repository in format owner/repo. If None, uses current directory
        labels (list, optional): List of labels to apply to the issue
    
    Returns:
        tuple: (success: bool, output: str)
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


def main():
    parser = argparse.ArgumentParser(description='Create a GitHub issue')
    parser.add_argument('--title', required=True, help='Title of the issue')
    parser.add_argument('--body', required=True, help='Body of the issue')
    parser.add_argument('--repo', help='Repository (owner/repo format). Defaults to current directory repo.')
    parser.add_argument('--labels', nargs='*', help='Labels to apply to the issue')
    
    args = parser.parse_args()
    
    success, output = create_github_issue(args.title, args.body, args.repo, args.labels)
    
    if success:
        print(output)
        sys.exit(0)
    else:
        print(output, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()