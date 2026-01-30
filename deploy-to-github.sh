#!/bin/bash
# Signal Hunter - GitHub 推送脚本
# 由木木同学自动生成

echo "🚀 Signal Hunter GitHub 推送助手"
echo "=================================="
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查目录
cd "$(dirname "$0")" || exit 1

# 配置 Git（如果未配置）
if [ -z "$(git config --global user.name)" ]; then
    echo -e "${YELLOW}配置 Git 用户名...${NC}"
    git config --global user.name "jacobcy"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo -e "${YELLOW}配置 Git 邮箱...${NC}"
    git config --global user.email "your-email@example.com"
fi

# 确保 .env 不会被提交
echo "检查敏感文件保护..."
if ! grep -q "^.env$" .gitignore 2>/dev/null; then
    echo ".env" >> .gitignore
    echo -e "${GREEN}✅ 已添加 .env 到 .gitignore（API Key 不会被泄露）${NC}"
fi

# 添加所有文件到 Git
echo ""
echo "📦 添加文件到 Git..."
git add -A

# 检查是否有变更
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️ 没有新的变更需要提交${NC}"
else
    # 提交
    echo "💾 创建提交..."
    git commit -m "feat: Signal Hunter v0.2.0 - Complete trading signal system

- Multi-platform data collection (Twitter/Bird, Web/HTTPX, WeChat/Sogou)
- SQLite persistence with thread-safe connections
- DeepSeek AI integration for daily digest generation  
- Telegram Bot with interactive commands (/scan, /digest, /status, /add)
- Resonance detection with 24h window and deduplication
- Channel broadcast support for monetization
- YAML configuration system
- Git version control with Conventional Commits"
    
    echo -e "${GREEN}✅ 代码已提交到本地仓库${NC}"
fi

# 检查远程仓库
echo ""
echo "🔗 检查 GitHub 远程仓库..."

if ! git remote | grep -q origin; then
    echo -e "${YELLOW}添加 GitHub 远程仓库...${NC}"
    git remote add origin https://github.com/jacobcy/signal-hunter.git
fi

# 检查 GitHub CLI 是否可用
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✅ GitHub CLI 已安装${NC}"
    
    # 检查是否已登录
    if gh auth status &>/dev/null; then
        echo -e "${GREEN}✅ 已登录 GitHub${NC}"
        
        # 检查仓库是否存在
        if ! gh repo view jacobcy/signal-hunter &>/dev/null; then
            echo ""
            echo -e "${YELLOW}📝 在 GitHub 上创建仓库...${NC}"
            gh repo create signal-hunter --private --description "AI-powered financial signal monitoring system" --source=. --push
            
            if [ $? -eq 0 ]; then
                echo ""
                echo -e "${GREEN}🎉 成功！仓库已创建并推送${NC}"
                echo -e "访问: ${GREEN}https://github.com/jacobcy/signal-hunter${NC}"
                exit 0
            fi
        else
            echo "仓库已存在，直接推送..."
        fi
    fi
fi

# 如果 GitHub CLI 方式失败，使用标准 Git 推送
echo ""
echo "📤 推送到 GitHub..."
echo -e "${YELLOW}提示: 如果要求输入密码，请使用 Personal Access Token${NC}"
echo -e "${YELLOW}创建 Token: https://github.com/settings/tokens${NC}"
echo ""

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 推送成功！${NC}"
    echo -e "访问: ${GREEN}https://github.com/jacobcy/signal-hunter${NC}"
else
    echo ""
    echo -e "${RED}❌ 推送失败${NC}"
    echo ""
    echo "手动解决方案:"
    echo "1. 打开 https://github.com/new"
    echo "2. 创建名为 'signal-hunter' 的私有仓库"
    echo "3. 运行: git remote add origin https://github.com/jacobcy/signal-hunter.git"
    echo "4. 运行: git push -u origin main"
fi
