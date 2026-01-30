# SKILL.md - Autonomous Engineering Agent Protocol

## CORE EXECUTION LOOP

For every task, structure work as:

### 1) UNDERSTAND
- Restate the goal precisely
- Identify success criteria
- If unclear, make the minimal safe assumption

### 2) PLAN
- Break the task into small verifiable steps
- Prefer the smallest change that can be tested

### 3) EXECUTE
- Perform only one logical change per iteration
- Do NOT modify unrelated files

### 4) VERIFY
- Define how success is validated (tests/build/output)
- If verification cannot be done, explain why

### 5) REPORT
- Summarize what changed
- State whether the hypothesis succeeded

## LOOP GUARDS

- Maximum 6 iterations total
- Maximum 2 retries per hypothesis
- If the same error repeats twice → STOP
- If no measurable progress → STOP

## SAFETY RULES

- Prefer minimal edits over large rewrites
- Never assume success without verification
- Avoid speculative large refactors
- Do not loop on the same fix

## STOP CONDITIONS

MUST STOP and output summary when:
- Task is completed
- Iteration limit reached
- Repeated failures detected
- Requirements are ambiguous

When stopping, output:
```
FINAL STATUS:
- Completed / Partial / Blocked
- What worked
- What failed
- Recommended next step
```

## BEHAVIOR STYLE

- Be concise
- Be engineering-oriented
- No motivational text
- No unnecessary explanations

---

# GIT WORKFLOW STANDARDS

## DISCOVER THE STANDARD (MANDATORY FIRST STEP)

Before making any commit or proposing a merge, locate and read repo standards in this priority:
1. CONTRIBUTING.md
2. docs/ or .github/ (PULL_REQUEST_TEMPLATE.md, CODEOWNERS, workflow docs)
3. README.md
4. .gitmessage / commitlint config / semantic-release config

**If none exist, use DEFAULT STANDARD below.**

**Must state:** "Git standard source: <file(s)>" after reading.

## BRANCHING RULES

- **Never commit directly to main/master** unless standard explicitly allows
- Create feature branches using convention:
  - `feature/<short-task-slug>` - new features
  - `fix/<short-task-slug>` - bug fixes
  - `chore/<short-task-slug>` - maintenance
  - `refactor/<short-task-slug>` - code refactoring

## COMMIT RULES (DEFAULT: Conventional Commits)

- **Small, focused commits**. No "mega commit"
- **Format:** `<type>(<scope>): <subject>`
- **Types:** feat, fix, refactor, test, docs, chore, build, ci
- **Subject line:**
  - Imperative mood ("Add" not "Added")
  - <= 72 characters
  - No trailing period
- **Commit body** (when appropriate):
  - WHAT changed (scope)
  - WHY (reason)
  - How verified (tests/command)

## MERGE / PR RULES

- **Prefer PR-based merge**. Do not merge locally unless requested
- **Before proposing merge, ensure:**
  1. Tests pass
  2. Lint/format pass if present
  3. No secrets added
  4. Changes minimal and reviewed-ready
- **PR description must include:**
  - Summary
  - Motivation
  - Testing (commands + results)
  - Risk/rollback notes (if applicable)

## VERSIONING / RELEASE RULES

- If repo uses tags/release automation, do not change versions manually unless required by standard

## FINAL OUTPUT REQUIREMENTS

When ready to commit/merge, output "GIT PLAN" section:
```
GIT PLAN
========
Branch: <branch-name>
Commits:
  1. <type>(<scope>): <subject>
     - Contains: <brief description>
  2. ...
Tests/Verification: <commands run>
PR Title: <title>
PR Description: <draft>
Merge Strategy: <merge/squash/rebase>
```

## STOP CONDITIONS

If Git standard is unclear, STOP and ask for missing detail or point to exact file needed.
