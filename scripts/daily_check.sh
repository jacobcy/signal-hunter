#!/bin/bash
# Daily Project Health Check & Standards Audit
# Signal Hunter v0.2.0

set -e

PROJECT_DIR="/Users/Jacob/clawd"
REPORT_FILE="/tmp/daily_check_report.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

cd "$PROJECT_DIR"

# Initialize report
cat > "$REPORT_FILE" << EOF
📊 Signal Hunter Daily Report
📅 $TIMESTAMP
═══════════════════════════════════════

EOF

# 1. Check Git Status
echo "🔍 Checking Git Status..." >> "$REPORT_FILE"
if [ -d .git ]; then
    UNCOMMITTED=$(git status --short | wc -l)
    echo "  Uncommitted files: $UNCOMMITTED" >> "$REPORT_FILE"
    
    if [ $UNCOMMITTED -gt 0 ]; then
        echo "  ⚠️ WARNING: $UNCOMMITTED uncommitted changes" >> "$REPORT_FILE"
        git status --short | head -5 >> "$REPORT_FILE"
    else
        echo "  ✅ All changes committed" >> "$REPORT_FILE"
    fi
    
    # Check last commit
    LAST_COMMIT=$(git log -1 --format="%h - %s (%ar)")
    echo "  Last commit: $LAST_COMMIT" >> "$REPORT_FILE"
else
    echo "  ❌ Not a git repository" >> "$REPORT_FILE"
fi

# 2. Code Quality Checks
echo "" >> "$REPORT_FILE"
echo "🔬 Code Quality Analysis" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

# Activate venv
source .venv/bin/activate 2>/dev/null || true

# Ruff check
echo "  Running Ruff linter..." >> "$REPORT_FILE"
RUFF_ERRORS=$(ruff check src/ 2>/dev/null | wc -l || echo "0")
if [ "$RUFF_ERRORS" -gt 0 ]; then
    echo "  ⚠️ Ruff found $RUFF_ERRORS issues" >> "$REPORT_FILE"
    ruff check src/ 2>/dev/null | head -3 >> "$REPORT_FILE"
else
    echo "  ✅ Ruff: No issues" >> "$REPORT_FILE"
fi

# MyPy check
echo "  Running MyPy type checker..." >> "$REPORT_FILE"
MYPY_ERRORS=$(mypy --ignore-missing-imports src/ 2>/dev/null | grep -c "error:" || echo "0")
if [ "$MYPY_ERRORS" -gt 0 ]; then
    echo "  ⚠️ MyPy found $MYPY_ERRORS type errors" >> "$REPORT_FILE"
    mypy src/ --ignore-missing-imports 2>/dev/null | grep "error:" | head -3 >> "$REPORT_FILE"
else
    echo "  ✅ MyPy: No type errors" >> "$REPORT_FILE"
fi

# 3. Test Status
echo "" >> "$REPORT_FILE"
echo "🧪 Test Status" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

if [ -d "tests" ]; then
    TEST_COUNT=$(find tests -name "test_*.py" | wc -l)
    echo "  Test files: $TEST_COUNT" >> "$REPORT_FILE"
    
    # Run tests if they exist
    if [ $TEST_COUNT -gt 0 ]; then
        pytest tests/ -q --tb=no 2>/dev/null | tail -5 >> "$REPORT_FILE" || echo "  ⚠️ Some tests failed" >> "$REPORT_FILE"
    else
        echo "  ⚠️ No test files found" >> "$REPORT_FILE"
    fi
else
    echo "  ❌ tests/ directory missing" >> "$REPORT_FILE"
fi

# 4. Documentation Check
echo "" >> "$REPORT_FILE"
echo "📚 Documentation Audit" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

DOC_FILES=("README.md" "docs/PRD.md" "docs/TECH_SPEC.md" "docs/ENGINEERING.md" "SKILL.md")
for doc in "${DOC_FILES[@]}"; do
    if [ -f "$doc" ]; then
        LINES=$(wc -l < "$doc")
        echo "  ✅ $doc ($LINES lines)" >> "$REPORT_FILE"
    else
        echo "  ❌ $doc missing" >> "$REPORT_FILE"
    fi
done

# 5. Code Metrics
echo "" >> "$REPORT_FILE"
echo "📈 Code Metrics" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

PYTHON_FILES=$(find src -name "*.py" | wc -l)
TOTAL_LINES=$(find src -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')

echo "  Python files: $PYTHON_FILES" >> "$REPORT_FILE"
echo "  Total lines: $TOTAL_LINES" >> "$REPORT_FILE"

# Check for TODO/FIXME comments
TODO_COUNT=$(grep -r "TODO\|FIXME" src/ 2>/dev/null | wc -l || echo "0")
echo "  TODO/FIXME items: $TODO_COUNT" >> "$REPORT_FILE"

# 6. Standards Improvement Analysis
echo "" >> "$REPORT_FILE"
echo "💡 Standards Analysis & Recommendations" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

# Identify gaps
ISSUES=0

if [ "$RUFF_ERRORS" -gt 10 ]; then
    echo "  🔧 HIGH: Code style issues ($RUFF_ERRORS). Run 'ruff check src/ --fix'" >> "$REPORT_FILE"
    ((ISSUES++))
fi

if [ "$MYPY_ERRORS" -gt 5 ]; then
    echo "  🔧 HIGH: Type coverage incomplete. Add type hints." >> "$REPORT_FILE"
    ((ISSUES++))
fi

if [ "$TEST_COUNT" -lt 5 ]; then
    echo "  🔧 MEDIUM: Test coverage low ($TEST_COUNT files). Add unit tests." >> "$REPORT_FILE"
    ((ISSUES++))
fi

if [ ! -f ".github/workflows/ci.yml" ]; then
    echo "  🔧 MEDIUM: No CI/CD pipeline. Add GitHub Actions." >> "$REPORT_FILE"
    ((ISSUES++))
fi

if [ ! -f "CONTRIBUTING.md" ]; then
    echo "  🔧 LOW: CONTRIBUTING.md missing. Copy from SKILL.md." >> "$REPORT_FILE"
    ((ISSUES++))
fi

if [ $TODO_COUNT -gt 5 ]; then
    echo "  🔧 LOW: $TODO_COUNT TODOs pending. Review and prioritize." >> "$REPORT_FILE"
    ((ISSUES++))
fi

# Redundancy check
echo "" >> "$REPORT_FILE"
echo "🎯 Redundancy Check" >> "$REPORT_FILE"
echo "─────────────────────────────────────" >> "$REPORT_FILE"

# Check for duplicate code patterns
echo "  Checking for repeated code patterns..." >> "$REPORT_FILE"
if grep -r "logger.info.*Starting" src/ 2>/dev/null | wc -l | grep -q "[3-9]"; then
    echo "  📋 NOTE: Consider extracting common logging patterns" >> "$REPORT_FILE"
fi

# Check config duplication
if [ -f ".env" ] && [ -f "config.yaml" ]; then
    echo "  📋 NOTE: Config split between .env and config.yaml - document which goes where" >> "$REPORT_FILE"
fi

# Summary
echo "" >> "$REPORT_FILE"
echo "═══════════════════════════════════════" >> "$REPORT_FILE"
if [ $ISSUES -eq 0 ]; then
    echo "✅ All standards met! Project is healthy." >> "$REPORT_FILE"
else
    echo "⚠️ Found $ISSUES improvement areas." >> "$REPORT_FILE"
fi
echo "═══════════════════════════════════════" >> "$REPORT_FILE"

# Output for Telegram
cat "$REPORT_FILE"

# Cleanup
rm "$REPORT_FILE"
