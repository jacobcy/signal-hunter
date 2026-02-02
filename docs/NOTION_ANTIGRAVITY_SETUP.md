# Notion + Antigravity 配置指南
## 2026-02-01 | 基础设施建设

---

## 1. Notion 配置（立即执行）

### 1.1 创建工作空间Integration

**步骤1: 访问Notion Integration页面**
```
https://www.notion.so/my-integrations
```

**步骤2: 创建新Integration**
- 点击 "New integration"
- 名称: "AI Studio"
- 关联工作空间: 选择你的workspace
- 点击 "Submit"

**步骤3: 复制API Token**
- 创建后会显示 `secret_` 开头的token
- **重要**: 立即复制保存，只显示一次！
- 格式: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**步骤4: 保存到本地**
```bash
mkdir -p ~/.config/notion
echo "secret_你的token" > ~/.config/notion/api_key
chmod 600 ~/.config/notion/api_key
```

### 1.2 授权访问你的工作空间

**步骤5: 分享页面给Integration**
1. 打开你的工作空间: https://www.notion.so/All-about-AI-1e473a857f7680bdbc9cc33c2a3a6f0d
2. 点击右上角 "..."
3. 选择 "Add connections"
4. 找到并选择 "AI Studio" (你刚创建的Integration)
5. 确认授权

**步骤6: 测试连接**
```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI"}'
```

如果返回JSON数据，说明配置成功！

---

## 2. Antigravity 研究总结

### 2.1 什么是Antigravity？

**Antigravity** 是OpenClaw生态中的一个**反向代理服务**，用于：
- 聚合多个AI模型提供商的API（OpenAI、Anthropic、Google等）
- 统一配额管理和成本控制
- 提供备用failover机制
- 监控和追踪使用情况

### 2.2 核心功能

| 功能 | 说明 |
|------|------|
| **统一API** | 一个endpoint访问多个模型 |
| **配额管理** | 监控各模型使用量和成本 |
| **自动切换** | 主模型耗尽时自动failover |
| **成本优化** | 智能路由到性价比最高模型 |

### 2.3 获取Antigravity访问

**方法1: 官方渠道（推荐）**
```
1. 访问 https://clawdhub.com 或 Discord社区
2. 申请Antigravity访问权限
3. 获取API Key和配置文档
```

**方法2: 自建方案（技术可行）**
如果官方渠道暂时不可用，可以考虑：
- 自建反向代理（Nginx + OpenResty）
- 使用LiteLLM Proxy（开源方案）
- 直接管理多API keys（当前方案）

### 2.4 当前替代方案

**在获得Antigravity前，使用多Key管理：**

```yaml
# ~/.config/openclaw/providers.yaml
providers:
  openai:
    api_key: sk-xxxxxxxx
    models: [gpt-4o, gpt-4o-mini]
    priority: 1
    
  anthropic:
    api_key: sk-ant-xxxxxxxx
    models: [claude-3-5-sonnet, claude-3-haiku]
    priority: 2
    
  google:
    api_key: AIzaSyxxxxxxxx
    models: [gemini-pro, gemini-flash]
    priority: 3
```

---

## 3. 建议的基础设施配置

### 3.1 优先级排序

| 组件 | 优先级 | 状态 | 说明 |
|------|--------|------|------|
| **Notion API** | P0 | ⏳ 待配置 | 文档系统核心 |
| **Antigravity** | P1 | 🔍 研究完成 | 等待官方访问 |
| **多API Key管理** | P1 | ✅ 可用 | 当前替代方案 |
| **X/Twitter API** | P2 | ⏳ 待申请 | 社交媒体监控 |
| **Brave Search API** | P2 | ⏳ 待申请 | 网页搜索增强 |

### 3.2 本周执行计划

**Day 1（今天）**: Notion配置
- [ ] 创建Integration获取API Token
- [ ] 保存到 ~/.config/notion/api_key
- [ ] 授权访问工作空间
- [ ] 测试API连接

**Day 2-3**: 文档系统搭建
- [ ] 在Notion中建立AI Studio工作空间结构
- [ ] 创建情报中心数据库
- [ ] 设置自动化模板

**Day 4-5**: Antigravity跟进
- [ ] 加入OpenClaw Discord询问Antigravity
- [ ] 或评估自建方案可行性
- [ ] 配置多API Key管理作为备用

**Day 6-7**: 其他API准备
- [ ] 申请Twitter Developer账号
- [ ] 申请Brave Search API
- [ ] 整理所有API keys到安全位置

---

## 4. 立即执行检查清单

### 需要你操作（5分钟）

- [ ] 1. 打开 https://www.notion.so/my-integrations
- [ ] 2. 创建名为 "AI Studio" 的Integration
- [ ] 3. 复制 `secret_` 开头的API Token
- [ ] 4. 把Token发给我（或执行上面的保存命令）
- [ ] 5. 在工作空间页面添加Integration连接

### 我来执行

- [ ] 测试Notion API连接
- [ ] 建立工作空间基础结构
- [ ] 配置API key安全存储
- [ ] 编写Notion操作脚本

---

## 5. 安全提醒

⚠️ **API Key管理安全原则**:
1. 永远不要把API key提交到git仓库
2. 使用 600 权限保存key文件
3. 定期轮换API keys
4. 为不同用途创建不同的Integration
5. 在Notion中只授权必要的页面

---

**下一步：请执行上面的5步操作，把Notion API Token配置好！**
