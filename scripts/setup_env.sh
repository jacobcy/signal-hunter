#!/bin/bash
# Environment Setup Script for OpenClaw Ops
# This script activates the virtual environment and sets up PYTHONPATH

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Activate virtual environment
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at $PROJECT_DIR/.venv"
    echo "   Please run 'python -m venv .venv' and install dependencies first"
fi

# Set PYTHONPATH to include project root and src directory
export PYTHONPATH="$PROJECT_DIR:$PROJECT_DIR/src:$PYTHONPATH"
echo "✅ PYTHONPATH set to: $PYTHONPATH"

# Export project directory for other scripts
export OPENCLAW_PROJECT_DIR="$PROJECT_DIR"

echo "✅ Environment setup complete"