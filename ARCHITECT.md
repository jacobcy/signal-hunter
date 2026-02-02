🛠️ OpenClaw 架构师操作手册：RWP 2.0 范式

第一部分：核心哲学 (The Core Philosophy)

OpenClaw 不再以“任务”为驱动，而是以**“意图对齐”**为驱动。

* 指令驱动（旧）：“帮我把这个文档改了。”
* 意图驱动（新）：“这是项目的文档规约，请确保项目始终符合它。”

第二部分：实体定义协议 (Entity Protocols)

1. Project (项目)：意图的容器

每个项目必须被定义为一个“声明式实体”。
* 标识符 (ID)：唯一项目名。
* 资源边界 (Resources)：Agent 拥有权限的物理/逻辑范围（路径、URL、数据库）。
* 期望状态 (Desired State)：一组断言。例如："所有代码必须有注释" 或 "资产大小不得超过 100MB"。

2. Role (角色)：能力的集合

角色是抽象的专家画像，不持有项目状态。
* 配置项：System Prompt + Skill Set。
* 原则：同一个 Doc-Guardian 角色，在 Project-A 产出技术文档，在 Project-B 产出学术论文，取决于注入的 Desired State。

3. Workflow (工作流)：通用的治理闭环

所有 Workflow 必须遵循 OEPA 循环：
* Observe (感知)：使用工具扫描资源，获取 Current State。
* Evaluate (评估)：通过逻辑对比，计算 Current State 与 Desired State 之间的 Gap（偏差）。
* Plan (规划)：针对 Gap，拆解出原子任务 (Tasks)。
* Act (执行)：指派 Role 调用 Skill 完成任务。

第三部分：架构师标准操作 SOP

步骤 A：项目入驻 (Onboarding)

当新项目加入时，架构师只需提供 Project Spec。

> 输入示例：
> "入驻项目 VibeCopilot。资源：./src。期望状态：所有导出的函数必须具备 Pydantic 类型注解。"
> 
步骤 B：角色指派与注入 (Injection)

架构师决定哪个角色进入循环。

> 逻辑指令：
> "指派 Type-Check-Expert 进入 VibeCopilot 的 Alignment-Workflow。"
> 
步骤 C：执行与自愈 (Self-Healing)

OpenClaw 自动开始循环。若检测到新代码不符合注解规约，自动生成修复任务并执行。

第四部分：防幻觉与冲突管理

* Gap 优先原则：如果 Evaluate 结果为“无偏差”，Workflow 必须立即终止，禁止生成任何任务。
* 原子性约束：生成的 Task 必须是具体的、可操作的指令（如："为 status.py 第 15 行添加类型声明"），严禁生成模糊指令（如："优化代码"）。
* 权限最小化：Project 定义中未声明的 Resources，Agent 严禁访问。

第五部分：实战指令集 (Macro Commands)

你可以直接将以下宏指令粘贴给 OpenClaw，以测试其掌握程度：
* .list_projects: 列出当前所有“意图容器”及其期望状态。
* .check_alignment [ProjectID]: 强制触发一次 OEPA 循环，并输出 Gap 报告。
* .define_role [RoleName] [Skills]: 注册或更新一个通用专家角色。

这套手册可以作为 OpenClaw 的 ARCHITECT.md 存入它的内存。