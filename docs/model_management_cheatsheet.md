# OpenClaw 模型管理备忘录

## 🔧 模型相关命令

### 查看模型状态
```bash
openclaw models status
openclaw models list
```

### 认证管理
```bash
# 查看认证状态
openclaw models auth --help

# 登录特定提供商 (需要交互式终端)
openclaw models auth login --provider <provider-name>

# 常用提供商:
# - google-gemini-cli
# - google-antigravity  
# - openrouter
# - minimax
# - moonshot
# - qwen-portal
```

### 模型配置管理
```bash
# 设置默认模型
openclaw models set <model-id>

# 管理回退模型列表
openclaw models fallbacks add <model-id>
openclaw models fallbacks remove <model-id>
openclaw models fallbacks list

# 管理模型别名
openclaw models aliases set <alias> <model-id>
openclaw models aliases remove <alias>
```

### 模型扫描 (OpenRouter)
```bash
# 扫描可用的 OpenRouter 模型
openclaw models scan
```

## 🚨 重要提醒

1. **认证过期**: OAuth 认证通常有时效性，需要定期刷新
2. **交互式登录**: 某些认证流程需要在交互式终端中完成
3. **模型可用性**: 免费模型可能不稳定，建议配置多个回退选项
4. **配置备份**: 修改配置前务必备份 ~/.openclaw/openclaw.json

## 📋 当前配置检查清单

- [ ] 检查主要模型可用性
- [ ] 验证回退模型链
- [ ] 确认认证状态
- [ ] 备份当前配置