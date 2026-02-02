# GitHub Issue Creation Pipeline Testing

## Overview
This directory contains the testing framework for the automated GitHub issue creation pipeline that integrates Claude Dev and Analyst agents.

## Components

### 1. Test Plan (`test_plan_github_issues.md`)
- Documents the planned test cases and expected outcomes
- Outlines the verification strategy for the pipeline

### 2. Component Monitor (`monitor_components.py`)
- Monitors the status of Dev and Analyst components
- Checks if the creation script and templates are ready

### 3. Test Executor (`execute_tests.py`)
- Contains the implementation of all planned test cases
- Provides the test execution framework

## Test Cases

### TC-1: Create an Epic using the new system
- Verifies that the system can create an Epic issue type with proper formatting

### TC-2: Create a Task using the new system
- Verifies that the system can create a Task issue type with proper formatting

### TC-3: Verify the created issue follows the template and contains correct information
- Ensures created issues adhere to templates and contain accurate information

## How to Execute Tests

### Step 1: Check Component Status
Before running tests, verify that both Dev and Analyst components are ready:

```bash
python monitor_components.py
```

Wait until both components show as "READY".

### Step 2: Execute Tests
Once both components are ready, run the full test suite:

```bash
python execute_tests.py
```

### Step 3: Review Results
Check the test execution summary to see pass/fail status of each test case.

## Next Steps
1. Wait for Dev to finish the creation script
2. Wait for Analyst to finish the templates
3. Run the monitoring script to confirm readiness
4. Execute the test suite
5. Review and report results