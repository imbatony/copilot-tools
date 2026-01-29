# Copilot Tools

基于 GitHub Copilot CLI 的日常生活和工作辅助工具集。

## 项目概述

本项目通过定制 GitHub Copilot CLI，添加自定义 instructions、agents、skills、hooks 和 MCP 服务器，来提升日常工作效率。

## 功能特性

- 🌤️ **天气查询**: 快速查询任意城市的天气信息
- 📋 **自定义 Instructions**: 为 Copilot 提供项目特定的上下文
- 🤖 **自定义 Agents**: 专门用于特定任务的 AI 代理
- 🎯 **Skills**: 增强 Copilot 执行特定任务的能力
- 🪝 **Hooks**: 在关键节点执行自定义脚本
- 🔌 **MCP 服务器**: 扩展 Copilot 的数据源和工具

## 目录结构

```
copilot-tools/
├── .github/
│   ├── copilot-instructions.md     # 全局自定义指令
│   ├── instructions/               # 专项指令
│   │   ├── python.instructions.md
│   │   ├── skills.instructions.md
│   │   ├── agents.instructions.md
│   │   ├── hooks.instructions.md
│   │   └── mcp.instructions.md
│   ├── agents/
│   │   └── weather-agent.md        # 天气查询 Agent
│   ├── skills/
│   │   ├── SKILL_GUIDELINES.md     # Skill 编写规范
│   │   └── weather-query/
│   │       ├── SKILL.md            # 天气查询技能定义
│   │       ├── scripts/
│   │       │   └── weather.py      # Python 脚本
│   │       └── references/
│   │           └── REFERENCE.md    # 技术参考文档
│   └── hooks/
│       └── session-hooks.json      # Hook 配置
├── scripts/                        # Hook 脚本
│   ├── log-prompt.ps1
│   ├── log-prompt.sh
│   ├── pre-tool-check.ps1
│   └── pre-tool-check.sh
├── config/
│   └── mcp-config.example.json     # MCP 配置示例
├── logs/                           # 日志目录 (自动创建)
├── pyproject.toml                  # uv 项目配置
└── README.md
```

## 快速开始

### 前置条件

1. 安装 [uv](https://docs.astral.sh/uv/) (Python 包管理器):
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. 安装 GitHub Copilot CLI:
   ```bash
   gh extension install github/gh-copilot
   ```

3. 确保已登录 GitHub 并拥有 Copilot 许可证

### 使用天气查询功能

1. 进入项目目录:
   ```bash
   cd copilot-tools
   ```

2. 启动 Copilot CLI:
   ```bash
   copilot
   ```

3. 询问天气:
   ```
   今天北京天气怎么样？
   ```

### 直接使用脚本

```bash
# 查询当前天气
uv run .github/skills/weather-query/scripts/weather.py 北京

# JSON 格式输出
uv run .github/skills/weather-query/scripts/weather.py 上海 --json

# 查询天气预报
uv run .github/skills/weather-query/scripts/weather.py 深圳 --forecast
```

## 自定义配置

### 添加自定义指令

编辑 `.github/copilot-instructions.md` 文件，添加项目特定的指令。

### 创建新的 Agent

在 `.github/agents/` 目录下创建新的 Markdown 文件:

```markdown
---
name: my-agent
description: 我的自定义 Agent 描述
---

# 我的 Agent

Agent 的详细说明和工作流程...
```

### 创建新的 Skill

1. 在 `.github/skills/` 下创建新目录
2. 创建 `SKILL.md` 文件，定义技能

```markdown
---
name: my-skill
description: 技能描述，说明何时使用此技能
---

# 技能说明

技能的详细使用说明...
```

### 配置 MCP 服务器

MCP (Model Context Protocol) 服务器为 Copilot 提供额外的数据源和工具能力。

1. 复制配置示例:
   ```bash
   cp config/mcp-config.example.json ~/.copilot/mcp-config.json
   ```

2. 编辑配置文件，例如添加 Blinko 笔记服务:
   ```json
   {
     "mcpServers": {
       "blinko": {
         "command": "npx",
         "args": ["-y", "mcp-server-blinko@0.0.9"],
         "env": {
           "BLINKO_DOMAIN": "http://your-blinko-server:1111",
           "BLINKO_API_KEY": "${BLINKO_TOKEN}"
         },
         "tools": ["*"]
       }
     }
   }
   ```

   > **注意**: `tools: ["*"]` 表示启用所有工具，`tools: []` 会禁用所有工具。

3. 或者在 Copilot CLI 中使用:
   ```
   /mcp add
   ```

详细配置说明参见 [mcp.instructions.md](.github/instructions/mcp.instructions.md)。

### 配置 Hooks

编辑 `.github/hooks/session-hooks.json` 文件，添加自定义 hooks。

支持的 hook 类型:
- `sessionStart`: 会话开始时
- `sessionEnd`: 会话结束时
- `userPromptSubmitted`: 用户提交 prompt 时
- `preToolUse`: 工具使用前
- `postToolUse`: 工具使用后

## 常用命令

在 Copilot CLI 中:

| 命令 | 说明 |
|------|------|
| `/agent` | 选择自定义 Agent |
| `/mcp` | 管理 MCP 服务器 |
| `/context` | 查看上下文使用情况 |
| `/compact` | 压缩对话历史 |
| `/review` | 审查代码变更 |

## 天气 API

本项目使用 [wttr.in](https://wttr.in) 免费天气 API，无需 API Key。

支持的查询:
- 当前天气
- 天气预报 (未来3天)
- 天气描述

## 贡献指南

欢迎提交 Issues 和 Pull Requests！

## 许可证

MIT License
