# GitHub Issue Creator

A simple utility to create GitHub issues programmatically using the GitHub CLI (`gh`).

## Files

- `github_issue_creator.py`: Command-line script to create GitHub issues
- `github_issue_api.py`: Importable Python module with functions to create GitHub issues
- `test_api.py`: Test script to verify the API functionality

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Authentication configured with `gh auth login`

## Usage

### Command Line

```bash
python3 github_issue_creator.py \
  --title "Issue Title" \
  --body "Issue description body" \
  --repo owner/repository \
  --labels label1 label2
```

### As a Python Module

```python
from github_issue_api import create_github_issue

success, result = create_github_issue(
    title="My Issue Title",
    body="Detailed issue description...",
    repo="owner/repository",  # Optional, defaults to current directory repo
    labels=["bug", "feature"]  # Optional
)

if success:
    print(f"Issue created: {result}")
else:
    print(f"Failed to create issue: {result}")
```

## Functions

### `create_github_issue(title, body, repo=None, labels=None)`
Creates a GitHub issue and returns a tuple of (success, output_or_error).

### `create_issue_with_confirmation(title, body, repo=None, labels=None)`
Creates a GitHub issue with built-in console feedback.

## Examples

### Create an issue in a specific repository
```python
from github_issue_api import create_github_issue

success, result = create_github_issue(
    "Bug Report: Feature X not working",
    "Detailed description of the bug...",
    repo="jacobcy/signal-hunter",
    labels=["bug", "high-priority"]
)
```

### Create an issue in the current repository
```python
success, result = create_github_issue(
    "New feature request",
    "Description of the requested feature...",
    labels=["enhancement"]
)
```