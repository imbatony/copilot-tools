# Agent Skills 完全指南：从入门到精通

> 基于 GitHub Copilot CLI 视角，结合实际项目经验的 Agent Skills 教程

## 目录

1. [什么是 Agent Skills](#什么是-agent-skills)
2. [为什么选择 Agent Skills](#为什么选择-agent-skills)
3. [快速开始](#快速开始)
4. [不同工具的配置位置](#不同工具的配置位置)
5. [SKILL.md 规范详解](#skillmd-规范详解)
6. [目录结构](#目录结构)
7. [实战案例](#实战案例)
8. [高级技巧](#高级技巧)
9. [最佳实践](#最佳实践)
10. [资源与社区](#资源与社区)

---

## 什么是 Agent Skills

Agent Skills 是一个开放标准，用于定义 AI Agent 的专业能力。简单来说，它是一个包含指令、脚本和资源的文件夹，Agent 可以根据需要动态加载这些内容，以提升在特定任务上的表现。

### 核心概念

```
Skill = 指令 (Instructions) + 脚本 (Scripts) + 资源 (Resources)
```

- **指令**: 告诉 Agent 如何执行任务的 Markdown 文档
- **脚本**: Agent 可以调用的可执行代码
- **资源**: 模板、数据文件、参考文档等

### 工作原理

```
用户提问 → Agent 匹配 Skill (根据 description) → 加载 SKILL.md → 执行指令/脚本 → 返回结果
```

1. **启动时**: Agent 只加载每个 Skill 的 `name` 和 `description`（约 100 tokens）
2. **激活时**: 根据用户问题匹配相关 Skill，加载完整 `SKILL.md`
3. **执行时**: 按需加载 `scripts/`、`references/`、`assets/` 中的文件

---

## 为什么选择 Agent Skills

### 对比传统 Prompt Engineering

| 特性 | 传统 Prompt | Agent Skills |
|------|------------|--------------|
| 可复用性 | 需要每次复制粘贴 | 一次编写，自动调用 |
| 组织性 | 分散在对话中 | 结构化文件目录 |
| 可维护性 | 难以版本控制 | Git 友好 |
| 可移植性 | 绑定特定工具 | 跨工具通用 |
| 上下文效率 | 始终占用 token | 按需加载 |

### 支持的工具

Agent Skills 是一个[开放标准](https://agentskills.io)，目前支持：

- **GitHub Copilot** (CLI、Coding Agent、VS Code)
- **Claude** (Claude Code、Claude.ai)
- **OpenCode**
- **Cursor**（部分支持）
- **Codex**（部分支持）

---

## 快速开始

### 第一个 Skill：Hello World

创建目录和文件：

```bash
mkdir -p .github/skills/hello-world
```

创建 `.github/skills/hello-world/SKILL.md`：

```markdown
---
name: hello-world
description: 一个简单的示例技能。当用户说"你好"或需要问候时使用。
---

# Hello World 技能

当用户需要问候时，使用以下格式回复：

## 回复模板

"你好！我是 Copilot，很高兴为你服务。今天有什么我可以帮助你的吗？"

## 注意事项

- 保持友好和专业
- 根据上下文调整语气
```

完成！现在当你在 Copilot CLI 中说"你好"，它会自动使用这个 Skill。

### 验证 Skill

在 GitHub Copilot CLI 中：

```bash
# 查看已加载的 Skills
/skills list

# 查看某个 Skill 的详情
/skills info hello-world
```

---

## 不同工具的配置位置

> ⚠️ **重要**: 这是不同工具之间的主要差异

### GitHub Copilot

| 作用范围 | 路径 |
|---------|------|
| 项目级 Skills | `.github/skills/` 或 `.claude/skills/` |
| 个人级 Skills | `~/.copilot/skills/` 或 `~/.claude/skills/` |

GitHub Copilot 同时支持两种路径格式，保持与 Claude 的兼容性。

### Claude (Claude Code)

| 作用范围 | 路径 |
|---------|------|
| 项目级 Skills | `.claude/skills/` |
| 个人级 Skills | `~/.claude/skills/` |

### OpenCode

| 作用范围 | 路径 |
|---------|------|
| 项目级 Skills | `.opencode/skills/` 或 `.github/skills/` |
| 个人级 Skills | `~/.opencode/skills/` |

### 路径优先级（GitHub Copilot）

```
1. ~/.copilot/skills/     (个人 Skills，最高优先级)
2. ~/.claude/skills/      (个人 Claude Skills)
3. .github/skills/        (项目 Skills)
4. .claude/skills/        (项目 Claude Skills)
```

### 推荐策略

| 场景 | 推荐路径 | 原因 |
|------|---------|------|
| 团队共享的项目规范 | `.github/skills/` | 可以纳入版本控制 |
| 个人工具和偏好 | `~/.copilot/skills/` | 跨项目通用 |
| 跨工具兼容 | `.github/skills/` | 多数工具都支持 |

---

## SKILL.md 规范详解

### 文件结构

```markdown
---
# YAML Frontmatter (必需)
name: skill-name
description: 技能描述
---

# Markdown Body (技能指令)
```

### Frontmatter 字段

#### 必需字段

| 字段 | 约束 | 说明 |
|------|------|------|
| `name` | 1-64 字符 | 技能标识符 |
| `description` | 1-1024 字符 | 功能描述和触发词 |

#### 可选字段

| 字段 | 约束 | 说明 |
|------|------|------|
| `license` | - | 许可证 |
| `compatibility` | 1-500 字符 | 环境要求 |
| `metadata` | key-value | 自定义元数据 |
| `allowed-tools` | 空格分隔列表 | 预授权工具（实验性） |

### name 字段规则

```yaml
# ✅ 有效
name: weather-query
name: pdf-processing
name: code-review

# ❌ 无效
name: Weather-Query    # 不能有大写
name: -pdf             # 不能以 - 开头
name: pdf--processing  # 不能有连续 --
name: pdf_processing   # 不能有下划线
```

**关键规则**: `name` 必须与目录名一致！

### description 字段技巧

`description` 是 Agent 决定是否使用 Skill 的关键。写好 description 的要点：

1. **说明功能**: 这个 Skill 能做什么
2. **使用场景**: 什么情况下应该使用
3. **触发关键词**: 用户可能问的问题

```yaml
# ✅ 好的 description
description: >-
  查询天气信息的技能。获取指定城市的当前天气、温度、湿度、风速，
  并提供穿衣和出行建议。当用户询问天气、气温、是否下雨、
  穿什么衣服、出行建议等问题时使用此技能。支持中英文城市名称。

# ❌ 差的 description
description: 查询天气。
```

### allowed-tools 字段（实验性）

预授权 Skill 可以使用的工具，避免每次执行都需要确认：

```yaml
# 允许使用 uv 运行 Python
allowed-tools: Bash(uv:*) Read

# 允许使用 MCP 工具（使用实际工具名称，非通配符）
allowed-tools: upsertBlinko searchBlinko updateBlinko deleteBlinko

# 允许 git 命令
allowed-tools: Bash(git:*)
```

> **注意**: MCP 工具的 `allowed-tools` 需要使用实际的工具名称（如 `upsertBlinko`），
> 而不是带前缀的通配符（如 `mcp_blinko_*`）。可以通过 `/mcp show <server-name>` 查看实际工具名称。

---

## 目录结构

### 完整结构

```
skill-name/
├── SKILL.md              # 必需 - 技能定义和指令
├── scripts/              # 可选 - 可执行脚本
│   ├── main.py
│   ├── helper.sh
│   └── utils.js
├── references/           # 可选 - 参考文档
│   ├── REFERENCE.md
│   ├── api-guide.md
│   └── faq.md
└── assets/               # 可选 - 静态资源
    ├── templates/
    │   └── report.md
    └── data/
        └── cities.json
```

### 各目录用途

#### scripts/

存放 Agent 可以执行的脚本。支持的语言取决于环境，常见选择：

- **Python** (推荐): 跨平台，标准库丰富
- **Bash/Shell**: Unix-like 系统
- **PowerShell**: Windows 系统
- **Node.js**: 前端相关任务

脚本编写原则：
- 自包含，尽量使用标准库
- 提供清晰的帮助信息 (`--help`)
- 支持 JSON 输出 (`--json`)
- 良好的错误处理

#### references/

存放详细文档，Agent 按需读取：
- 保持每个文件专注于单一主题
- 避免放入完整 `SKILL.md` 的冗长内容
- 常见文件：`REFERENCE.md`、`API.md`、`FAQ.md`

#### assets/

存放静态资源：
- 模板文件
- 配置模板
- 数据文件
- 图片/图表

### 渐进式披露

Skill 的设计支持分层加载，优化 token 使用：

| 加载阶段 | 内容 | Token 消耗 |
|---------|------|-----------|
| 启动时 | `name` + `description` | ~100 tokens |
| 激活时 | 完整 `SKILL.md` | < 5000 tokens (建议) |
| 执行时 | scripts/references/assets | 按需 |

**建议**: 主 `SKILL.md` 控制在 500 行以内。

---

## 实战案例

### 案例 1: 天气查询 Skill

本项目中的 `weather-query` Skill 展示了一个完整的技能实现。

#### 目录结构

```
weather-query/
├── SKILL.md
├── scripts/
│   └── weather.py
└── references/
    └── REFERENCE.md
```

#### SKILL.md

```markdown
---
name: weather-query
description: >-
  查询天气信息的技能。获取指定城市的当前天气、温度、湿度、风速，并提供穿衣和出行建议。
  当用户询问天气、气温、是否下雨、穿什么衣服、出行建议等问题时使用此技能。
  支持中英文城市名称查询。
license: MIT
compatibility: Requires uv (or Python 3.8+) and internet access
metadata:
  author: copilot-tools
  version: "1.0.0"
  api: wttr.in
allowed-tools: Bash(uv:*) Bash(python:*) Read
---

# 天气查询技能

获取指定城市的实时天气信息，包括温度、湿度、风速等，并根据天气状况提供穿衣和出行建议。

## 使用方法

使用 uv 运行 Python 脚本（推荐）：

\`\`\`bash
uv run scripts/weather.py <城市名>
\`\`\`

### 示例

\`\`\`bash
# 查询北京天气
uv run scripts/weather.py 北京

# 查询天气预报（未来3天）
uv run scripts/weather.py 深圳 --forecast

# 输出 JSON 格式
uv run scripts/weather.py 北京 --json
\`\`\`

## 常见场景

| 用户问题 | 处理方式 |
|---------|---------|
| "今天天气怎么样" | 查询用户所在城市或询问城市 |
| "北京明天会下雨吗" | 使用 `--forecast` 查询预报 |
| "我应该穿什么衣服" | 根据温度返回穿衣建议 |
```

#### 脚本设计要点

`scripts/weather.py` 的关键设计：

```python
#!/usr/bin/env python3
"""天气查询脚本"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="查询天气信息")
    parser.add_argument("city", help="城市名称")
    parser.add_argument("--forecast", "-f", action="store_true", help="显示预报")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    # 获取天气数据...
    result = fetch_weather(args.city)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))

if __name__ == "__main__":
    main()
```

### 案例 2: 月报生成 Skill

`monthly-report` Skill 展示了一个纯文本指令型技能（无脚本）。

```markdown
---
name: monthly-report
description: >-
  月报工作汇总技能。将工作事项转换为专业的月报格式，每项工作一句话，
  按重要程度排序。格式：动词开头 + 具体内容 + 业务目标 + 量化指标。
  当用户需要写月报、总结工作、汇总成果时使用此技能。
---

# 月报工作汇总

将工作事项转换为专业的一句话汇总，按重要程度排序。

## 格式要求

\`\`\`
[Action Verb] + [Product/Feature] + [Technical Details], [enabling/achieving] + [Business Goal] + [Metrics].
\`\`\`

## 示例

\`\`\`
Shipped Hera Automation Desk v1.3.0 with Azure Monitor + OpenTelemetry integration, 
enabling end-to-end observability to drive data-informed workflow optimization.
\`\`\`

## 详细指南

查看 [references/REFERENCE.md](references/REFERENCE.md) 获取完整案例和写作指南。
```

### 案例 3: 笔记管理 Skill (MCP 集成)

`note-management` Skill 展示了如何与 MCP 服务集成。

```markdown
---
name: note-management
description: >-
  笔记管理技能，使用 Blinko MCP 服务进行个人笔记和闪念的管理。
  支持创建闪念、笔记、待办事项，搜索笔记，分享笔记，每日回顾等功能。
  当用户询问笔记、记录想法、闪念、备忘、待办、搜索笔记等问题时使用此技能。
license: MIT
compatibility: 需要配置 Blinko MCP Server 和 BLINKO_TOKEN 环境变量
metadata:
  author: copilot-tools
  version: "2.0.0"
  mcp-server: blinko
  mcp-package: mcp-server-blinko@0.0.9
allowed-tools: upsert_blinko_flash_note upsert_blinko_note upsert_blinko_todo search_blinko_notes share_blinko_note review_blinko_daily_notes clear_blinko_recycle_bin
---

# 笔记管理技能

使用 [mcp-server-blinko](https://github.com/BryceWG/mcp-server-blinko) 管理个人笔记和闪念。

## 可用工具

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `upsert_blinko_flash_note` | 创建闪念 | 快速记录想法、灵感 |
| `upsert_blinko_note` | 创建笔记 | 详细记录内容、备忘 |
| `upsert_blinko_todo` | 创建待办 | 记录待办事项、任务 |
| `search_blinko_notes` | 搜索笔记 | 查找之前的记录 |
| `share_blinko_note` | 分享笔记 | 分享或取消分享笔记 |
| `review_blinko_daily_notes` | 每日回顾 | 获取今日待回顾笔记 |

## 配置要求

在 `~/.copilot/mcp-config.json` 中添加：

\`\`\`json
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
\`\`\`
```

---

## 高级技巧

### 1. 多语言脚本支持

根据操作系统提供不同脚本：

```
scripts/
├── run.py          # 跨平台 Python
├── run.sh          # Unix/macOS
└── run.ps1         # Windows PowerShell
```

在 `SKILL.md` 中说明：

```markdown
## 运行脚本

**跨平台 (推荐)**:
\`\`\`bash
uv run scripts/run.py
\`\`\`

**Windows**:
\`\`\`powershell
.\scripts\run.ps1
\`\`\`

**Unix/macOS**:
\`\`\`bash
./scripts/run.sh
\`\`\`
```

### 2. 链式 Skill 调用

在 `SKILL.md` 中引导 Agent 组合使用多个 Skill：

```markdown
## 复杂场景

如果需要生成带天气信息的日报：
1. 先使用 `weather-query` 获取天气数据
2. 再使用 `monthly-report` 格式化输出
```

### 3. 动态内容生成

利用脚本生成动态内容：

```python
# scripts/generate.py
import json
from datetime import datetime

def main():
    result = {
        "generated_at": datetime.now().isoformat(),
        "content": generate_content()
    }
    print(json.dumps(result, ensure_ascii=False))
```

### 4. 环境变量管理

敏感信息通过环境变量传递：

```yaml
compatibility: 需要设置 API_KEY 环境变量
```

在脚本中读取：

```python
import os

api_key = os.environ.get("API_KEY")
if not api_key:
    print("错误: 请设置 API_KEY 环境变量", file=sys.stderr)
    sys.exit(1)
```

### 5. 验证工具

使用官方工具验证 Skill 格式：

```bash
npx skills-ref validate ./my-skill
```

---

## 最佳实践

### 命名规范

| 组件 | 规范 | 示例 |
|------|------|------|
| 目录名 | 小写字母 + 连字符 | `weather-query` |
| 脚本名 | 小写 + 下划线/连字符 | `weather.py`, `run-task.sh` |
| 参考文档 | 大写 + 下划线 | `REFERENCE.md`, `API_GUIDE.md` |

### Description 编写清单

- [ ] 说明技能功能（做什么）
- [ ] 描述使用场景（何时用）
- [ ] 包含触发关键词（用户怎么问）
- [ ] 说明输入/输出格式
- [ ] 100-500 字符为宜

### 脚本编写清单

- [ ] 支持 `--help` 参数
- [ ] 支持 `--json` 输出格式
- [ ] 错误输出到 stderr
- [ ] 返回有意义的退出码
- [ ] 处理边界情况
- [ ] 尽量使用标准库

### 文档组织

```
主 SKILL.md (< 500 行)
├── 快速开始
├── 使用示例
├── 常见场景表格
└── 链接到 references/ 的详细文档

references/REFERENCE.md
├── 详细 API 说明
├── 配置指南
└── 故障排除
```

### Token 优化

1. **精简主文件**: SKILL.md < 5000 tokens
2. **分层文档**: 详细内容放 references/
3. **按需资源**: 大文件放 assets/
4. **避免冗余**: 不要复制粘贴相同内容

---

## 资源与社区

### 官方资源

| 资源 | 链接 |
|------|------|
| Agent Skills 规范 | https://agentskills.io/specification |
| GitHub Copilot 文档 | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills |
| Anthropic Skills 仓库 | https://github.com/anthropics/skills |
| Awesome Claude Skills | https://github.com/ComposioHQ/awesome-claude-skills |

### 社区资源

| 资源 | 说明 |
|------|------|
| [tech-shrimp/agent-skills-examples](https://github.com/tech-shrimp/agent-skills-examples) | 中文 Skills 示例 |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | GitHub 官方 Skills 合集 |

### Anthropic 官方 Skills 示例

```
skills/
├── algorithmic-art    # 算法艺术生成
├── brand-guidelines   # 品牌指南
├── canvas-design      # 画布设计
├── docx               # Word 文档处理
├── pdf                # PDF 处理
├── pptx               # PPT 处理
├── xlsx               # Excel 处理
├── mcp-builder        # MCP 服务器生成
├── webapp-testing     # Web 应用测试
└── skill-creator      # Skill 创建向导
```

### 验证和调试

```bash
# 验证 Skill 格式
npx skills-ref validate ./my-skill

# 在 Copilot CLI 中查看
/skills list
/skills info <skill-name>

# 重新加载 Skills
/skills reload
```

---

## 常见问题

### Q: Skill 没有被识别？

检查：
1. `name` 是否与目录名一致
2. `SKILL.md` 文件名是否正确（必须是大写）
3. 目录位置是否正确

### Q: 脚本无法执行？

检查：
1. 脚本是否有执行权限 (`chmod +x`)
2. `allowed-tools` 是否包含所需工具
3. 依赖是否已安装

### Q: 如何调试 Skill？

1. 使用 `/skills info <name>` 查看 Skill 详情
2. 在对话中明确提及 Skill 名称
3. 检查 Agent 的响应是否引用了 Skill

### Q: 多个 Skill 冲突？

- 使用更具体的 `description`
- 避免 `description` 中使用相同的触发词
- 在对话中明确指定要使用的 Skill

---

## 总结

Agent Skills 是一个强大且灵活的扩展机制：

1. **简单** - 只需 `SKILL.md` 即可开始
2. **可移植** - 一次编写，多工具运行
3. **高效** - 按需加载，优化 token
4. **可扩展** - 支持脚本、MCP 集成

开始创建你自己的 Skill 吧！

---

*本文档基于 [Agent Skills 规范](https://agentskills.io/specification) 和实际项目经验编写。*
*最后更新: 2026-01*
