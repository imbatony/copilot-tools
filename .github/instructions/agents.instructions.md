# Agent 编写指令

适用于 `.github/agents/` 目录下的自定义 Agent 开发。

## Agent 概述

Agent 是 Copilot 的专门化版本，针对特定任务优化。

## 文件位置

- 仓库级 Agent: `.github/agents/`
- 用户级 Agent: `~/.copilot/agents/`

## Agent 文件格式

Agent 使用 Markdown 文件定义，包含 YAML frontmatter：

```markdown
---
name: agent-name
description: Agent 的简短描述
---

# Agent 名称

详细的 Agent 说明和工作流程...
```

## 必需字段

| 字段 | 说明 |
|------|------|
| `name` | Agent 标识符，用于调用 |
| `description` | 简短描述，帮助用户选择 |

## 内容结构

### 推荐结构

```markdown
---
name: example-agent
description: 示例 Agent
---

# Agent 名称

你是一个专门的助手，擅长...

## 能力范围

1. 能力一
2. 能力二
3. 能力三

## 工作流程

1. 首先...
2. 然后...
3. 最后...

## 响应格式

描述输出格式模板...

## 可用工具

列出 Agent 可以使用的工具和 Skill...

## 错误处理

说明如何处理异常情况...
```

## 编写原则

1. **明确角色**: 清晰定义 Agent 的专业领域
2. **具体流程**: 提供步骤化的工作流程
3. **格式模板**: 定义一致的输出格式
4. **工具关联**: 说明可用的 Skill 和工具
5. **边界情况**: 处理错误和异常

## 使用 Agent

在 Copilot CLI 中：

```bash
# 交互式选择
/agent

# 直接调用
使用 weather agent 查询北京天气

# 命令行指定
copilot --agent=weather --prompt "查询北京天气"
```

## 与 Skill 配合

Agent 可以调用 Skill 来执行特定任务：

```markdown
## 可用工具

优先使用以下工具获取天气数据：
1. Weather Query Skill
2. Shell 命令调用 API
```

## 示例 Agent

参见: `.github/agents/weather-agent.md`
