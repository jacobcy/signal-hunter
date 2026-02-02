# Proposal: Autonomous System Health & Evolution Strategy

## 1. 核心理念 (Core Concept)
不仅仅是“报错”，而是“进化”。系统应具备自我诊断能力，并根据外部情报（X 报告）主动进化（增加新技能）。

## 2. 架构设计 (Architecture)

### A. The Inspector (诊断器)
一个 Python 脚本 (`scripts/system_health.py`)，用于执行确定性的硬指标检查。
*   **API 探针:** 轮询所有 Key (DeepSeek, Gemini, Notion, etc.) 的 `/models` 或 `/me` 接口，验证连通性和余额（如果支持）。
*   **组件状态:** 检查 OpenClaw Gateway, Signal Hunter Bot, Aider 环境是否存活。
*   **版本审计:** 检查 `git status` (是否有未提交代码), `brew outdated` (关键工具是否过时)。
*   **输出:** 生成 `memory/health_report.json` 和 `memory/health_report.md`。

### B. The Strategist (战略家)
一个定期触发的 Agent 任务 (Cron Job)，负责“思考”和“决策”。
*   **输入:**
    1.  `memory/health_report.md` (来自诊断器)
    2.  `memory/signal_hunter_daily.md` (来自 Twitter 舆情)
*   **决策逻辑:**
    *   *系统亚健康?* -> 自动修复配置或生成修复工单。
    *   *Twitter 热点出现 "MCP Server"?* -> 检查当前技能库 -> 发现缺失 -> **建议安装 `mcp-manager` 技能**。
    *   *Twitter 热点出现 "DeepSeek V3"?* -> 检查当前 API 配置 -> 发现是 V2 -> **建议更新模型配置**。

## 3. 实施步骤 (Implementation Plan)

### 第一阶段：基础设施 (Infrastructure)
1.  **编写 `scripts/system_health.py`:**
    *   实现 API 连通性测试函数。
    *   实现 OpenClaw 配置文件校验。
    *   集成到现有的 `daily_check.sh` 流程中。

### 第二阶段：技能封装 (Skill Integration)
1.  **创建 `skills/system-admin`:**
    *   将脚本封装为 Tool。
    *   增加 `upgrade_system` (自动 `git pull`, `brew upgrade`) 能力。
    *   增加 `install_new_skill` (通过 `clawdhub` 搜索并安装新能力) 能力。

### 第三阶段：自动化闭环 (Automation)
1.  **配置 Cron Job:**
    *   每天早晨 8:50 (在 Signal Hunter 简报之后)。
    *   执行任务：阅读两份报告 -> 综合分析 -> 发送 Telegram 决策简报。

## 4. 预期效果 (Expected Outcome)
您将收到类似这样的早报：
> **✅ 系统健康度: 98%**
> - 所有 API 在线，DeepSeek 响应延迟略高 (1.2s)。
> - Aider 版本落后 (0.86 -> 0.88)。
>
> **🚀 进化建议:**
> - 昨日推特热议 "Browser Use" 库。
> - 我们目前只有基础 `browser` 工具。
> - **建议：** 是否尝试安装 `browser-use` 增强版技能？

## 5. 立即行动 (Next Step)
我建议先从 **编写 `scripts/system_health.py`** 开始，这就为您构建第一道防线。

**您同意这个方案吗？** 如果同意，我将开始编写健康检查脚本。
