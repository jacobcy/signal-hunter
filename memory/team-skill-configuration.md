# AI团队技能配置方案
## HR制定 - 2026-01-31

### 新增角色：网络研究员 (Web Researcher)

**角色定位**：专门负责外部信息获取、网络浏览、社交媒体监控

**核心职责**：
- 网页搜索与信息提取
- 社交媒体监控（Twitter/X, LinkedIn, Telegram）
- 竞品动态追踪
- 新闻和RSS监控
- 外部API数据获取

**专属Skills**：
- brave-search - 网页搜索（已有）✅
- kagi-search - Kagi搜索API
- tavily - AI优化搜索
- bird - X/Twitter CLI
- linkedin-cli - LinkedIn自动化
- himalaya - 邮件管理
- telegram-usage - Telegram监控
- miniflux-news - RSS新闻聚合

---

### 完整团队技能配置

#### 1. 木木（AI项目经理）
**现状**：2/7 skills (29%)
**补充计划**：
- ~~claude-team~~ - 需要iTerm2（暂时跳过）
- ~~codex-orchestration~~ - 需要Codex CLI（暂时跳过）
- model-usage - 成本监控（如可用）
- session-logs - 日志分析
- brave-search - 快速搜索 ✅

**替代方案**：使用现有全局skills + 网络研究员协作

#### 2. Dev（程序员）- 已完备 ✅
**状态**：5/5 (100%)
**已安装**：
- conventional-commits ✅
- github-pr ✅
- coding-agent ✅
- github ✅
- gitload ✅

#### 3. QA（测试工程师）- 已完备 ✅
**状态**：1/1 (100%)
**已安装**：
- github-pr ✅

**扩展建议**：
- 等待pytest skill可用

#### 4. Ops（运营经理）- 已完备 ✅
**状态**：3/3 (100%)
**已安装**：
- linux-service-triage ✅
- cron ✅
- deploy-agent ✅

**扩展建议**：
- cloudflare - Cloudflare管理
- coolify - 部署平台

#### 5. Analyst（数据分析师）- 已完备 ✅
**状态**：2/2 (100%)
**已安装**：
- browser ✅
- canvas ✅

**扩展建议**：
- exa - 神经搜索
- tavily - AI搜索

#### 6. Editor（编辑）- 已完备 ✅
**状态**：3/3 (100%)
**已安装**：
- frontend-design ✅
- ui-audit ✅
- ux-audit ✅

#### 7. HR（人力资源）- 已完备 ✅
**状态**：3/3 (100%)
**已安装**：
- agentlens ✅
- deepwiki ✅
- perry-workspaces ✅

#### 8. Web Researcher（网络研究员）- 新增角色
**必需Skills**：
- brave-search - 网页搜索（已全局安装）✅
- bird - X/Twitter监控
- himalaya - 邮件管理
- linkedin-cli - LinkedIn自动化
- telegram-usage - Telegram监控
- miniflux-news - RSS聚合

---

### 全局安装清单（立即执行）

**通信类**：
```bash
# 外部交互核心
bird              # X/Twitter CLI
himalaya          # 邮件IMAP/SMTP
linkedin-cli      # LinkedIn自动化
telegram-usage    # Telegram监控
```

**搜索类**：
```bash
# 增强搜索
kagi-search       # Kagi搜索API
tavily            # AI优化搜索
exa               # 神经搜索
```

**监控类**：
```bash
# 信息监控
miniflux-news     # RSS新闻
clawdbot-release-check  # 版本检查
```

**Signal Hunter专项**：
```bash
# 交易相关
ibkr-trading      # Interactive Brokers
```

---

### 安装优先级

**P0（立即）：网络研究员核心技能**
- bird, himalaya, linkedin-cli, telegram-usage

**P1（今日）：增强搜索**
- kagi-search, tavily, exa

**P2（本周）：监控与专项**
- miniflux-news, ibkr-trading, cloudflare

---

### 协作流程示例

**场景1：监控Twitter信号源**
```
老板: "监控@elonmusk的最新推文"
  ↓
木木: 派遣网络研究员
  ↓
Web Researcher: 使用bird技能获取推文
  ↓
Analyst: 分析推文情绪和关键词
  ↓
木木: 整合报告给老板
```

**场景2：竞品调研**
```
老板: "调研竞争对手新产品"
  ↓
木木: 并行派遣:
  - Web Researcher: 网页搜索+新闻监控
  - Analyst: 数据收集和可视化
  - Editor: 撰写调研报告
  ↓
木木: 整合所有产出
```

---

### 预期效果

1. **外部信息获取**：专门的网络研究员角色，持续监控外部动态
2. **技能覆盖**：从71% → 90%+
3. **协作能力**：各角色可以独立执行专业任务
4. **扩展性**：新角色可以灵活增减

---

### 成本考量

**API Keys可能需要**：
- Kagi Search API
- Tavily API
- Exa AI API
- Brave Search API

**建议**：先安装skills，配置API keys后功能完全可用
