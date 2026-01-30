# Product Requirement Document (PRD)

## 1. Project Overview
**Project Name**: Signal Hunter (Moltbot)
**Version**: 0.1.0-draft
**Status**: Draft
**Owner**: 老板 (The Boss)
**Architect**: 木木同学 (Mumu)

### 1.1 Objective
构建一个具备高鲁棒性的自动化情报监控系统。核心任务是监控指定财经博主/信源（`memory/bloggers.md`），自动抓取、清洗内容，提取明确的股票交易信号。当多个信源对同一标的产生观点共振（Resonance）时，通过 Telegram 发送高优先级警报。

### 1.2 Core Value
*   **Zero-Token Default**: 默认运行模式下完全基于规则和逻辑，不消耗 LLM Token。
*   **Self-Healing**: 具备分级容错机制（HTTP -> Headless Browser -> Vision AI），当 DOM 结构变更导致解析失败时，能自动升级手段进行修复或报警。
*   **Asynchronous High-Performance**: 全链路异步架构，支持高并发信源监控。

## 2. User Stories
*   **As a Trader**, 我希望系统能每小时自动检查一次列表中的博主，这样我不错过任何盘中机会。
*   **As a Developer**, 我希望系统日志清晰（Loguru），并且报错时能自动保留现场（HTML/Screenshot），方便 debug。
*   **As a Boss**, 我希望只有在多个大 V 同时看多某只股票时才打扰我，减少噪音。

## 3. Functional Requirements

### 3.1 Source Management
*   **Input**: 读取 `memory/bloggers.md` (Format: `Name | URL | Platform | Weight`).
*   **Multi-Platform Support**: 系统需通过适配器模式支持不同平台的数据抓取：
    *   **Generic Web**: 通用 HTML 解析（默认）。
    *   **Twitter/X**: 针对性解析（需处理动态加载）。
    *   **Substack/Newsletter**: 邮件订阅源或网页归档。
    *   **WeChat/公众号**: 搜狗入口或网页版解析。
*   **Validation**: 校验 URL 有效性，自动剔除死链。

### 3.2 Crawler Engine (The Harvester)
*   **Architecture**: 基于接口的适配器模式 (Adapter Pattern)。根据 URL 特征自动分发给对应的 Fetcher。
*   **Parsing**: `BeautifulSoup4` + `lxml` 提取核心文本。

### 3.3 Signal Processor (The Brain - Zero Token)
*   **Keyword Matching**: 基于预定义词库（如 "买入", "加仓", "目标价", 股票代码正则 `[A-Z]{2,4}`）提取信号。
*   **Standardization**: 将非结构化文本转化为 `Signal` 对象 (Pydantic Model)。

### 3.4 Resonance Detector (The Filter)
*   **Logic**: 
    *   Time Window: 过去 24 小时内。
    *   Threshold: 同一标的出现 >= 2 次独立信源提及。
*   **Output**: 生成 `Alert` 对象。

### 3.5 Notification System
*   **Channel**: Telegram Bot API.
*   **Format**: 
    ```text
    🚨 信号共振报警: [NVDA]
    ...
    ```
*   **Interactive Commands**:
    *   `/status`: 系统健康检查。
    *   `/scan`: 强制手动扫描。
    *   `/add`: 添加新信源。
    *   `/digest`: 生成过去 24 小时的情报汇总（日报）。

## 4. Non-Functional Requirements
*   **Performance**: 单次全量扫描 < 60s (for 50 sources).
*   **Reliability**: 失败重试 3 次 (Exponential Backoff)。
*   **Maintainability**: 类型安全 (Type Hints), 100% 格式化 (Ruff).

## 5. Directory Structure Plan
```text
.
├── config/                 # 配置文件 (settings.toml)
├── docs/                   # 文档 (PRD, Tech Spec)
├── logs/                   # 运行日志
├── memory/                 # 数据存储 (bloggers.md, sqlite db)
├── src/
│   ├── __init__.py
│   ├── core/               # 核心逻辑
│   │   ├── engine.py       # 调度引擎
│   │   ├── fetcher.py      # 爬虫 (HTTPX/Playwright)
│   │   └── parser.py       # 解析器
│   ├── models/             # Pydantic 数据模型
│   │   ├── signal.py
│   │   └── source.py
│   ├── utils/              # 工具函数
│   │   ├── logger.py
│   │   └── notifier.py
│   └── main.py             # 入口文件 (Typer CLI)
├── tests/                  # Pytest 测试用例
├── .gitignore
├── pyproject.toml          # 依赖管理 & Ruff 配置
└── README.md
```

## 6. Phase 1 Deliverables
1.  Initialize Git Repository.
2.  `pyproject.toml` configuration.
3.  `docs/PRD.md` (This file).
4.  `docs/TECH_SPEC.md` (Next step).
