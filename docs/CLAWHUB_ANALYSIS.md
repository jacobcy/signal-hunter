# ClawHub 深度分析
## OpenClaw 官方技能注册中心

**来源**: https://github.com/openclaw/clawhub  
**官网**: https://clawhub.ai  
**Soul注册**: https://onlycrabs.ai

---

## 核心发现

### 1. ClawHub 是官方技能商店
- **功能**: 发布、版本管理、搜索基于文本的 agent skills
- **内容**: SKILL.md + 支持文件
- **搜索**: 基于 OpenAI embeddings 的向量搜索（非关键词）
- **CLI**: `clawhub sync` 用于安装和同步

### 2. OnlyCrabs.ai - SOUL.md 注册中心
- **功能**: AI 人格/灵魂的注册和共享
- **内容**: SOUL.md 文件（我们的 AGENTS.md/SOUL.md 体系）
- **用途**: 共享 AI 角色设定、工作方式、协作规范

### 3. 技能发布格式

标准的 SKILL.md 格式：
```markdown
---
name: skill-name
description: What this skill does
metadata: {
  "clawdbot": {
    "nix": {
      "plugin": "github:org/repo?dir=path",
      "systems": ["aarch64-darwin"]
    }
  }
}
---

# skill-name

## When to Use
...

## Commands
...
```

### 4. Nix 插件支持
ClawHub 支持 Nix 打包的技能，可以将 CLI 二进制、配置、skill pack 打包在一起。

### 5. 技术栈
- **前端**: TanStack Start (React + Vite/Nitro)
- **后端**: Convex (DB + 文件存储 + HTTP actions)
- **认证**: Convex Auth (GitHub OAuth)
- **搜索**: OpenAI embeddings (text-embedding-3-small) + Convex 向量搜索

---

## 对我们 AI 团队的启示

### 1. 我们的 skill-manager 符合官方标准
- 我们创建的 SKILL.md 格式与 ClawHub 兼容
- 可以发布到 clawhub.ai 供社区使用

### 2. SOUL.md 可以发布到 OnlyCrabs.ai
- 我们的 SOUL.md、AGENTS.md、USER.md 体系
- 可以打包发布，共享我们的 AI 协作模式

### 3. 技能发现方式
- **当前**: 通过 awesome-openclaw-skills GitHub 列表
- **未来**: 直接通过 clawhub.ai 向量搜索
- **优势**: 语义搜索比关键词更准确

### 4. 安装方式确认
```bash
# 官方 CLI 安装
npx clawdhub@latest install <skill-name>

# 我们的 HR skill-manager 封装
./skill-manager.sh onboard <role>
```

---

## 战略建议

### 短期：利用现有生态
1. 从 awesome-openclaw-skills 列表安装必要 skills
2. 使用我们的 skill-manager 进行角色管理
3. 保持 SKILL.md 格式与 ClawHub 兼容

### 中期：贡献社区
1. 将我们的 skill-manager 发布到 clawhub.ai
2. 分享我们的 SOUL.md 到 onlycrabs.ai
3. 建立公司在 OpenClaw 生态的影响力

### 长期：建立私有 Registry
1. 参考 ClawHub 架构搭建内部技能仓库
2. 管理商业敏感/专有的内部 skills
3. 与 ClawHub 保持兼容，可选发布到公有 registry

---

## 关键资源

| 资源 | 链接 | 用途 |
|------|------|------|
| **技能商店** | https://clawhub.ai | 发现和安装 skills |
| **灵魂注册** | https://onlycrabs.ai | 发布 SOUL.md |
| **技能列表** | https://github.com/VoltAgent/awesome-openclaw-skills | GitHub 列表 |
| **CLI 工具** | `npx clawdhub@latest` | 安装 skills |
| **规范文档** | https://github.com/openclaw/clawhub/docs/spec.md | 技术规范 |

---

## 下一步行动

**HR 建议**:
1. 继续通过 awesome-openclaw-skills 发现和安装 skills
2. 监控 ClawHub 的正式发布和 API 变化
3. 准备将我们的 skill-manager 发布到社区
4. 评估是否需要搭建私有技能仓库

**技术选型确认**:
- ✅ 我们的 skill-manager 架构符合官方标准
- ✅ SKILL.md 格式与 ClawHub 兼容
- ✅ 可以继续使用现有安装方式
- ✅ 未来可无缝迁移到 clawhub.ai
