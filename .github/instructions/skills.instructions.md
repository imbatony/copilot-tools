# Skill 编写指令

适用于 `.github/skills/` 目录下的 Agent Skill 开发。

## 遵循规范

所有 Skill 必须遵循 [Agent Skills 官方规范](https://agentskills.io/specification)。

详细指南参见: `.github/skills/SKILL_GUIDELINES.md`

## 目录结构

```
.github/skills/
├── SKILL_GUIDELINES.md      # 编写指南（本项目参考）
└── skill-name/              # 技能目录
    ├── SKILL.md             # 必需 - 技能定义
    ├── scripts/             # 可执行脚本
    │   └── main.py
    └── references/          # 参考文档
        └── REFERENCE.md
```

## SKILL.md 必需字段

```yaml
---
name: skill-name           # 小写字母 + 连字符，与目录名一致
description: >-            # 详细描述，包含触发关键词
  技能功能描述...
license: MIT               # 许可证
compatibility: 环境要求    # 运行时依赖
metadata:
  author: copilot-tools
  version: "1.0.0"
allowed-tools: Bash(uv:*) Read
---
```

## name 字段规则

- 1-64 字符
- 仅小写字母、数字、连字符
- 不能以 `-` 开头或结尾
- 不能有连续 `--`
- **必须与目录名一致**

## description 编写要点

1. 明确说明技能功能
2. 描述使用场景
3. 包含触发关键词（用户可能问的问题）

示例：
```yaml
description: >-
  查询天气信息的技能。获取指定城市的当前天气、温度、湿度，
  并提供穿衣和出行建议。当用户询问天气、气温、是否下雨、
  穿什么衣服等问题时使用此技能。
```

## 脚本编写原则

1. **使用 Python + uv**: 统一运行环境
2. **支持 JSON 输出**: 便于程序解析
3. **清晰的帮助信息**: 使用 argparse
4. **错误处理**: 提供有用的错误提示
5. **标准库优先**: 减少外部依赖

## 运行脚本

```bash
# 使用 uv 运行
uv run .github/skills/skill-name/scripts/main.py

# 带参数运行
uv run .github/skills/skill-name/scripts/main.py --help
```

## 创建新 Skill 步骤

1. 创建目录结构
2. 编写 SKILL.md（frontmatter + 说明）
3. 实现脚本（scripts/）
4. 添加参考文档（references/）
5. 测试运行
