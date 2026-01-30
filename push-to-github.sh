#!/bin/bash
# Signal Hunter 推送脚本
# 用法：在终端运行 ./push-to-github.sh

echo "🚀 推送 Signal Hunter 到 GitHub"
echo "================================"

# 检查是否已配置 Git
git config --global user.name "jacobcy" 2>/dev/null || true
git config --global user.email "your-email@example.com" 2>/dev/null || true

# 添加远程仓库（替换为你的实际仓库地址）
git remote add origin https://github.com/jacobcy/signal-hunter.git 2>/dev/null || true

# 确保 .env 不会被推送
echo "检查 .gitignore..."
if ! grep -q "^.env$" .gitignore; then
    echo ".env" >> .gitignore
    echo "✅ 已添加 .env 到 .gitignore"
fi

# 添加所有文件
git add -A

# 提交
git commit -m "feat: Signal Hunter v0.2.0 - Complete trading signal system

- Multi-platform data collection (Twitter/Bird, Web/HTTPX, WeChat/Sogou)
- SQLite persistence with thread-safe connections  
- DeepSeek AI integration for daily digest generation
- Telegram Bot with interactive commands
- Resonance detection with 24h window and deduplication
- Channel broadcast support
- YAML configuration system
- Git version control" 2>/dev/null || echo " nothing to commit, working tree clean"

# 推送
echo "正在推送到 GitHub..."
git push -u origin master || git push -u origin main

echo ""
echo "✅ 完成！访问 https://github.com/jacobcy/signal-hunter 查看代码"
