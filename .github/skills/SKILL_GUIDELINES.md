# Agent Skills 编写指南

本文档基于 [GitHub Copilot Agent Skills 官方文档](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) 和 [Agent Skills 规范](https://agentskills.io/specification)，用于指导新 Skill 的编写。

> **💡 推荐做法：** 在创建新技能时，请优先使用 **skill-creator** 技能来辅助创建。只需向 Copilot 描述你想要的技能功能，skill-creator 会引导你完成整个创建流程，确保符合规范要求。

## 官方规范要点

根据 GitHub 官方文档，技能需要满足以下要求：

### 存储位置

- **项目技能**：存储在仓库的 `.github/skills` 或 `.claude/skills` 目录下
- **个人技能**：存储在用户主目录的 `~/.copilot/skills` 或 `~/.claude/skills` 目录下

### 必需元素

1. **SKILL.md 文件**（必需）：技能定义文件，必须命名为 `SKILL.md`
2. **YAML frontmatter**（必需）：包含 `name` 和 `description` 字段
3. **Markdown 正文**（必需）：技能的详细指令、示例和指南

### 支持的工具

Agent Skills 是一个开放标准，支持：
- GitHub Copilot (Coding Agent、CLI、VS Code Insiders)
- Claude (Claude Code)
- 其他兼容 Agent Skills 规范的工具

## 目录结构

每个 Skill 是一个独立目录，**目录名必须与 `name` 字段一致**：

```
skill-name/
├── SKILL.md              # 必需 - 技能定义文件
├── scripts/              # 可选 - 可执行脚本
│   ├── main.py
│   └── helper.sh
├── references/           # 可选 - 参考文档
│   ├── REFERENCE.md
│   └── api-guide.md
└── assets/               # 可选 - 静态资源
    ├── templates/
    └── data/
```

## SKILL.md 格式

### Frontmatter（必需）

```yaml
---
name: skill-name
description: >-
  技能的详细描述，说明功能和使用场景。
  应包含触发关键词，帮助 Agent 识别何时使用此技能。
license: MIT
compatibility: 环境要求说明（可选）
metadata:
  author: your-name
  version: "1.0.0"
allowed-tools: Bash(uv:*) Read
---
```

### 字段说明

| 字段 | 必需 | 要求 |
|------|------|------|
| `name` | ✅ | 1-64 字符，仅小写字母、数字、连字符，不能以 `-` 开头/结尾，不能有连续 `--` |
| `description` | ✅ | 1-1024 字符，描述功能和使用场景，包含触发关键词 |
| `license` | ❌ | 许可证名称或文件引用 |
| `compatibility` | ❌ | 1-500 字符，环境要求（运行时、依赖、网络等） |
| `metadata` | ❌ | 自定义键值对 |
| `allowed-tools` | ❌ | 空格分隔的预授权工具列表（实验性） |

### name 字段规则

✅ 有效示例：
```yaml
name: weather-query
name: pdf-processing
name: code-review
```

❌ 无效示例：
```yaml
name: Weather-Query    # 不能有大写
name: -pdf             # 不能以 - 开头
name: pdf--processing  # 不能有连续 --
```

### description 字段规则

✅ 好的示例：
```yaml
description: >-
  查询天气信息的技能。获取指定城市的当前天气、温度、湿度、风速，
  并提供穿衣和出行建议。当用户询问天气、气温、是否下雨、
  穿什么衣服等问题时使用此技能。
```

❌ 差的示例：
```yaml
description: 查询天气。
```

## Body 内容

Frontmatter 之后是 Markdown 正文，包含技能的详细说明。

### 推荐结构

```markdown
# 技能名称

简短描述技能功能。

## 使用方法

如何调用此技能的脚本或工具。

## 示例

具体的使用示例和预期输出。

## 详细文档

链接到 references/ 目录中的详细文档。

## 常见场景

列出用户可能的问题和对应的处理方式。
```

### 文件引用

使用相对路径引用其他文件：

```markdown
查看 [详细文档](references/REFERENCE.md) 了解 API 说明。

运行脚本：
scripts/weather.py
```

## Scripts 目录

### Python 脚本模板

```python
#!/usr/bin/env python3
"""
脚本描述

用法:
    uv run scripts/example.py <参数>

示例:
    uv run scripts/example.py --help
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="脚本描述")
    parser.add_argument("input", help="输入参数")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    # 业务逻辑
    result = {"status": "success"}
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"结果: {result}")


if __name__ == "__main__":
    main()
```

### 脚本编写原则

1. **自包含**: 尽量使用标准库，减少外部依赖
2. **错误处理**: 提供清晰的错误信息
3. **边界情况**: 处理各种异常输入
4. **输出格式**: 支持 JSON 输出便于程序解析

## References 目录

存放详细的技术文档，Agent 按需加载：

- `REFERENCE.md` - 主要技术参考
- 领域特定文档（如 `api-guide.md`、`faq.md`）

### 保持文档精简

- 每个文件专注一个主题
- 主 SKILL.md 控制在 500 行以内
- 详细内容放到 references/

## Assets 目录

存放静态资源：

- 模板文件
- 配置模板
- 数据文件
- 图片/图表

## 渐进式披露

Skill 结构设计支持按需加载：

1. **元数据** (~100 tokens): `name` 和 `description` 在启动时加载
2. **指令** (<5000 tokens): 激活时加载完整 SKILL.md
3. **资源** (按需): scripts/、references/、assets/ 在需要时加载

## 验证工具

使用官方验证工具检查 Skill 格式：

```bash
npx skills-ref validate ./my-skill
```

## 示例：创建新 Skill

> **推荐方式：** 使用 skill-creator 技能创建新技能，只需告诉 Copilot 你想要创建什么技能即可。

### 使用 skill-creator（推荐）

直接向 Copilot 描述你的需求：

```
我想创建一个用于查询天气的技能
```

skill-creator 会：
1. 通过具体示例理解你的需求
2. 规划可重用的技能内容
3. 初始化技能目录结构
4. 编辑和完善技能内容
5. 验证并打包技能

### 手动创建

如需手动创建，按以下步骤操作：
   ```bash
   mkdir -p .github/skills/my-skill/{scripts,references}
   ```

2. 创建 SKILL.md：
   ```markdown
   ---
   name: my-skill
   description: 我的技能描述，说明功能和使用场景。
   license: MIT
   metadata:
     author: my-name
     version: "1.0.0"
   ---

   # 我的技能

   技能说明...
   ```

3. 添加脚本（可选）：
   ```bash
   touch .github/skills/my-skill/scripts/main.py
   ```

4. 添加参考文档（可选）：
   ```bash
   touch .github/skills/my-skill/references/REFERENCE.md
   ```

## 参考链接

- [GitHub Copilot Agent Skills 官方文档](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Agent Skills 官方规范](https://agentskills.io/specification)
- [Agent Skills 介绍](https://agentskills.io/what-are-skills)
- [Anthropic Skills 仓库](https://github.com/anthropics/skills)
- [Awesome Copilot 社区集合](https://github.com/github/awesome-copilot)
