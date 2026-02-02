#!/usr/bin/env python3
"""
Monitoring script to track the status of Dev and Analyst components
for the GitHub issue creation pipeline.
"""

import os
import time
from datetime import datetime

def check_dev_component():
    """
    Check if the Dev component (creation script) is ready.
    This is a placeholder function that should be updated based on actual implementation.
    """
    # Look for common indicators of a completed dev script
    potential_locations = [
        './github_issue_creator.py',
        './scripts/github_issue_creator.py',
        './dev/github_issue_creator.py',
        './claude_dev/github_issue_creator.py'
    ]
    
    for location in potential_locations:
        if os.path.exists(location):
            print(f"Dev component found at: {location}")
            return True
    
    # Additional checks could be added here based on your specific implementation
    return False

def check_analyst_component():
    """
    Check if the Analyst component (templates) is ready.
    This is a placeholder function that should be updated based on actual implementation.
    """
    # Look for common indicators of templates
    potential_locations = [
        './templates/',
        './issue_templates/',
        './github_templates/',
        './claude_analyst/templates/',
        './templates/github_issues/'  # Specific path discovered in the project
    ]
    
    for location in potential_locations:
        if os.path.exists(location) and os.path.isdir(location):
            # Check if there are any template files
            files = os.listdir(location)
            template_files = [f for f in files if '.md' in f or '.txt' in f or '.yaml' in f or '.json' in f]
            if template_files:
                print(f"Analyst templates found at: {location}")
                print(f"Template files: {template_files}")
                return True
    
    # Special check for the specific template directory we found
    if os.path.exists('./templates/github_issues/') and os.path.isdir('./templates/github_issues/'):
        files = os.listdir('./templates/github_issues/')
        template_files = [f for f in files if '.md' in f or '.txt' in f or '.yaml' in f or '.json' in f]
        if template_files:
            print(f"Analyst templates found at: ./templates/github_issues/")
            print(f"Template files: {template_files}")
            return True
    
    return False

def monitor_components():
    """
    Main monitoring function that checks both components and reports status.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting component monitoring...")
    
    dev_ready = check_dev_component()
    analyst_ready = check_analyst_component()
    
    print("\nComponent Status:")
    print(f"Dev Component (Creation Script): {'READY' if dev_ready else 'NOT READY'}")
    print(f"Analyst Component (Templates): {'READY' if analyst_ready else 'NOT READY'}")
    
    if dev_ready and analyst_ready:
        print("\n🎉 Both components are ready! System is ready for testing.")
        return True
    else:
        print("\n⏳ Waiting for components to be completed...")
        return False

if __name__ == "__main__":
    # For now, just run once to check current status
    # In a real implementation, this might run continuously or be triggered periodically
    monitor_components()