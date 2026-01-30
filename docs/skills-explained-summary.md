# Skills Explained 总结

> 原文: https://claude.com/blog/skills-explained

本文介绍了 Claude 的 Agent 生态系统中各个组件如何协同工作，帮助用户理解何时使用哪种工具。

---

## 核心构建模块概览

Claude 的 Agent 系统包含五个核心构建模块：

| 组件 | 提供能力 | 持久性 | 最佳用途 |
|------|---------|--------|---------|
| **Skills** | 程序性知识 | 跨对话 | 专业化技能 |
| **Prompts** | 即时指令 | 单次对话 | 快速请求 |
| **Projects** | 背景知识 | 项目内 | 集中化上下文 |
| **Subagents** | 任务委派 | 跨会话 | 专门化任务 |
| **MCP** | 工具连接 | 持续连接 | 数据访问 |

---

## 1. Skills（技能）

### 定义

Skills 是包含指令、脚本和资源的文件夹，Claude 会在相关任务时**动态发现和加载**。可以理解为专门的培训手册，赋予 Claude 特定领域的专业能力。

### 工作原理

使用 **Progressive Disclosure（渐进式披露）** 机制：

1. **元数据先加载**（约 100 tokens）：提供足够信息判断相关性
2. **完整指令按需加载**（<5k tokens）
3. **脚本/文件仅在需要时加载**

### 适用场景

- **组织工作流**: 品牌指南、合规流程、文档模板
- **领域专业知识**: Excel 公式、PDF 操作、数据分析
- **个人偏好**: 笔记系统、编码模式、研究方法

### 示例

创建品牌指南 Skill，包含公司配色、排版规则和布局规范。Claude 在创建演示文稿时会自动应用这些标准。

---

## 2. Prompts（提示词）

### 定义

用自然语言在对话中向 Claude 提供的指令。特点是**临时性、对话性、响应式**。

### 适用场景

- 一次性请求："总结这篇文章"
- 对话细化："语气改得更专业些"
- 即时上下文："分析这些数据并识别趋势"
- 临时指令："格式化为项目符号列表"

### 何时应该用 Skill 替代

如果发现自己在多个对话中**反复输入相同的 prompt**，就该创建 Skill 了。

---

## 3. Projects（项目）

### 定义

自包含的工作空间，拥有独立的对话历史和知识库。每个项目包含 200K context window，可上传文档、提供上下文和设置自定义指令。

### 适用场景

- **持久上下文**: 应该影响每次对话的背景知识
- **工作空间组织**: 为不同工作分离上下文
- **团队协作**: 共享知识和对话历史（Team/Enterprise 计划）
- **自定义指令**: 项目特定的语气、视角或方法

### 何时应该用 Skill 替代

如果发现在**多个 Projects 中复制相同的指令**，这表明应该创建 Skill。

### 核心区别

> **Projects 说 "这是你需要知道的"，Skills 说 "这是如何做事情"**
>
> Projects 提供你工作其中的知识库，Skills 提供可在任何地方使用的能力。

---

## 4. Subagents（子代理）

### 定义

专门的 AI 助手，拥有独立的 context window、自定义 system prompt 和特定的工具权限。在 Claude Code 和 Agent SDK 中可用。

### 适用场景

- **任务专门化**: 代码审查、测试生成、安全审计
- **上下文管理**: 保持主对话专注，同时分担专门工作
- **并行处理**: 多个 subagents 可同时处理不同方面
- **工具限制**: 限制特定 subagent 只能进行安全操作（如只读访问）

### 示例

```
创建一个 code-reviewer subagent，只能访问 Read、Grep、Glob 工具，
不能访问 Write 或 Edit。修改代码时自动委派给它进行质量和安全审查。
```

---

## 5. MCP（Model Context Protocol）

### 定义

一个**开放标准**，用于将 AI 助手连接到外部系统——内容仓库、业务工具、数据库和开发环境。

### 工作原理

MCP 提供连接 Claude 到工具和数据源的标准化方式。不需要为每个数据源构建自定义集成，只需对接单一协议。

### 适用场景

- **访问外部数据**: Google Drive、Slack、GitHub、数据库
- **使用业务工具**: CRM 系统、项目管理平台
- **连接开发环境**: 本地文件、IDE、版本控制
- **集成自定义系统**: 私有工具和数据源

---

## Skills vs MCP：核心区别

| 维度 | Skills | MCP |
|------|--------|-----|
| **功能** | 教 Claude **如何做某事** | 让 Claude **能够访问某处的数据** |
| **包含内容** | 指令 + 代码 + 资源 | 工具定义 |
| **加载时机** | 动态按需加载 | 始终可用 |
| **是否包含代码** | 是 | 是 |

### 组合使用

> **MCP 负责连接，Skills 负责程序性知识**

例如：
- 需要 Claude **访问**数据库或 Excel 文件 → 用 MCP
- 需要解释**如何使用**工具或遵循流程（如"查询数据库时总是先按日期范围过滤"）→ 用 Skill

**最佳实践**: 两者结合使用——MCP 提供连接能力，Skills 提供操作方法。

---

## 组合使用示例：研究代理

构建一个综合研究代理的步骤：

### 步骤 1: 设置 Project

创建 "Competitive Intelligence" 项目并上传：
- 行业报告和市场分析
- 竞争对手产品文档
- CRM 中的客户反馈
- 之前的研究摘要

### 步骤 2: 通过 MCP 连接数据源

启用 MCP 服务器：
- Google Drive（访问共享研究文档）
- GitHub（审查竞争对手开源仓库）
- Web search（实时市场信息）

### 步骤 3: 创建专门的 Skills

创建 "competitive-analysis" Skill，包含分析框架和搜索策略。

### 步骤 4: 配置 Subagents

创建专门的 subagents：
- `market-researcher`: 研究市场趋势和行业报告
- `technical-analyst`: 分析技术架构和实现方案

### 步骤 5: 激活研究代理

当你问 Claude："分析我们前三个竞争对手如何定位他们的新 AI 功能，并识别我们可以利用的差距"

**执行流程**:

1. **Project 上下文加载**: 访问上传的研究文档
2. **MCP 连接激活**: 搜索 Google Drive 和 GitHub
3. **Skills 参与**: 提供分析框架
4. **Subagents 执行**: 市场研究员收集数据，技术分析师审查实现
5. **Prompts 细化**: 你提供对话指导

---

## 常见问题

### Skills 如何工作？

使用 **Progressive Disclosure（渐进式披露）**：
1. 首先扫描 Skill 元数据（描述和摘要）识别相关匹配
2. 如果匹配，加载完整指令
3. 如果 Skill 包含可执行代码或参考文件，仅在需要时加载

这种架构意味着可以有**很多 Skills 可用而不会占满 context window**。

### Skills vs Subagents：何时用什么？

| 场景 | 选择 |
|------|------|
| 任何 Claude 实例都能加载和使用的能力 | **Skills** |
| 需要完整、自包含、独立处理工作流的代理 | **Subagents** |
| Subagent 需要专业知识 | **两者结合** |

### Skills vs Projects：何时用什么？

| 场景 | 选择 |
|------|------|
| 需要始终加载的背景知识和上下文 | **Projects** |
| 需要仅在相关时激活的程序性知识和可执行代码 | **Skills** |
| 需要持久上下文 + 专门能力 | **两者结合** |

### Subagents 能使用 Skills 吗？

**可以**。在 Claude Code 和 Agent SDK 中，subagents 可以像主代理一样访问和使用 Skills。这创造了强大的组合——专门的 subagents 利用可移植的专业知识。

---

## 快速入门

### Claude.ai 用户
- 在 Settings → Features 中启用 Skills
- 在 claude.ai/projects 创建第一个项目
- 尝试将项目知识与 Skills 结合用于分析任务

### API 开发者
- 查看 Skills endpoint [文档](https://docs.anthropic.com)
- 参考 [Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

### Claude Code 用户
- 通过 plugin marketplaces 安装 Skills
- 参考 [Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

---

## 参考链接

- [Skills 官方库](https://github.com/anthropics/skills)
- [MCP 文档](https://modelcontextprotocol.io/docs/develop/build-server)
- [Prompt 最佳实践](https://claude.com/blog/prompt-engineering-best-practices)
- [Prompt Library](https://docs.claude.com/en/prompt-library/library)
