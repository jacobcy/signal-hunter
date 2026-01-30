#!/bin/bash
# Signal Hunter 测试运行脚本
# Usage: ./run-tests.sh [unit|integration|all]

set -e

echo "🧪 Signal Hunter Test Runner"
echo "============================"

# 检查参数
TEST_TYPE="${1:-all}"

# 激活虚拟环境
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# 安装测试依赖
echo "📦 检查测试依赖..."
pip install -q pytest pytest-asyncio pytest-cov ruff mypy pre-commit 2>/dev/null || true

# 运行代码格式检查
echo ""
echo "🔍 运行代码格式检查 (Ruff)..."
ruff check src/ || true
ruff format --check src/ || true

# 运行类型检查
echo ""
echo "🔍 运行类型检查 (MyPy)..."
mypy src/ --ignore-missing-imports || true

# 运行测试
echo ""
echo "🧪 运行测试..."

if [ "$TEST_TYPE" = "unit" ]; then
    echo "运行单元测试..."
    pytest tests/unit/ -v --tb=short --cov=src --cov-report=term-missing
elif [ "$TEST_TYPE" = "integration" ]; then
    echo "运行集成测试..."
    pytest tests/integration/ -v --tb=short
else
    echo "运行所有测试..."
    pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
fi

echo ""
echo "✅ 测试完成！"
