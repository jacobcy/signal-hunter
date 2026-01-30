# Signal Hunter 工程约束规范 (Engineering Constraints)

## 1. 代码质量约束

### 1.1 类型安全 (Type Safety)
- **强制要求**: 所有函数必须有类型提示 (Type Hints)
- **禁止**: 使用 `Any` 类型（除非与外部库交互）
- **工具**: mypy 严格模式检查

### 1.2 代码风格 (Code Style)
- **工具**: Ruff (替代 flake8 + black)
- **行长度**: 100字符
- **引号**: 双引号优先
- **导入**: 强制排序，禁止循环导入

### 1.3 文档规范
- **模块**: 每个文件必须有模块级docstring
- **函数**: 公共函数必须有docstring + 类型提示
- **复杂逻辑**: 必须添加行内注释

## 2. 架构约束

### 2.1 分层架构 (Layered Architecture)
```
src/
├── models/      # 数据模型 (Pure Pydantic)
├── core/        # 业务逻辑 (无IO)
├── adapters/    # 外部接口 (Twitter/Web/DB)
├── utils/       # 工具函数
└── config/      # 配置管理
```
**约束**:
- `models/` 禁止导入任何其他层
- `core/` 只能通过接口依赖外部服务
- `adapters/` 实现具体IO，可被mock

### 2.2 依赖方向
```
config → models → core → adapters → utils
```
**禁止**: 反向依赖（如adapter直接调用core的具体实现）

### 2.3 异常层级
```
BaseSignalHunterError
├── ConfigError
├── FetchError
├── ParseError
├── DatabaseError
└── NotifyError
```
**约束**: 每个模块必须抛出/捕获特定异常，禁止裸`except:`

## 3. 测试约束

### 3.1 测试覆盖
- **单元测试**: 所有`core/`模块必须>=80%覆盖率
- **集成测试**: 关键流程（扫描→处理→通知）必须有端到端测试
- **Mock规范**: 外部IO必须mock，禁止真实网络/DB调用

### 3.2 测试结构
```
tests/
├── unit/           # 单元测试
├── integration/    # 集成测试
├── fixtures/       # 测试数据
└── conftest.py     # pytest配置
```

## 4. Git约束

### 4.1 提交规范 (Conventional Commits)
```
<type>(<scope>): <subject>

<body>

<footer>
```
**类型**: feat, fix, docs, style, refactor, test, chore

### 4.2 分支策略
- `main`: 生产分支，禁止直接推送
- `develop`: 开发分支
- `feat/*`: 功能分支
- `fix/*`: 修复分支

### 4.3 预提交钩子
- ruff格式检查
- mypy类型检查
- pytest单元测试

## 5. 配置约束

### 5.1 敏感信息
- **禁止**: 将API Key、密码等提交到Git
- **工具**: git-secrets扫描
- **文件**: `.env`必须存在于.gitignore

### 5.2 环境隔离
- 开发/测试/生产配置分离
- 配置验证（pydantic-settings）

## 6. 性能约束

### 6.1 响应时间
- 单次扫描 < 60s（50个源）
- 数据库查询 < 100ms
- 内存占用 < 200MB

### 6.2 资源限制
- 并发数控制（防止被封）
- 连接池管理（数据库/HTTP）

## 7. 当前违规清单 (TODO)

- [ ] 添加mypy配置
- [ ] 补充单元测试
- [ ] 统一异常层级
- [ ] 添加pre-commit hooks
- [ ] 创建CONTRIBUTING.md
