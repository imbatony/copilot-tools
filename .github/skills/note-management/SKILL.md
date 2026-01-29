---
name: note-management
description: >-
  笔记管理技能，使用 Blinko MCP 服务进行个人笔记和闪念的管理。
  支持创建闪念、笔记、待办事项，搜索笔记，分享笔记，每日回顾等功能。
  当用户询问笔记、记录想法、闪念、备忘、待办、搜索笔记、查找记录等问题时使用此技能。
  所有操作通过 mcp-server-blinko 的工具完成。
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

此技能通过 Blinko MCP Server 提供以下工具：

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `upsert_blinko_flash_note` | 创建闪念 (type 0) | 快速记录想法、灵感 |
| `upsert_blinko_note` | 创建笔记 (type 1) | 详细记录内容、备忘 |
| `upsert_blinko_todo` | 创建待办 (type 2) | 记录待办事项、任务 |
| `search_blinko_notes` | 搜索笔记 | 查找之前的记录 |
| `share_blinko_note` | 分享笔记 | 分享或取消分享笔记 |
| `review_blinko_daily_notes` | 每日回顾 | 获取今日待回顾笔记 |
| `clear_blinko_recycle_bin` | 清空回收站 | 永久删除已删除的笔记 |

## 使用方法

直接使用 Blinko MCP 工具，Agent 会自动调用相应的 MCP 工具。

### 创建闪念

当用户说 "记录一下..."、"快速记一个想法..."、"闪念..." 时，使用 `upsert_blinko_flash_note` 工具。

### 创建笔记

当用户说 "帮我记住..."、"创建一条笔记..."、"详细记录..." 时，使用 `upsert_blinko_note` 工具。

### 创建待办

当用户说 "添加待办..."、"记一个任务..."、"todo..." 时，使用 `upsert_blinko_todo` 工具。

### 搜索笔记

当用户说 "找一下我之前记的..."、"搜索笔记..."、"我之前写过..." 时，使用 `search_blinko_notes` 工具。

### 分享笔记

当用户说 "分享这条笔记..."、"取消分享..." 时，使用 `share_blinko_note` 工具。

### 每日回顾

当用户说 "今天要回顾什么..."、"每日回顾..." 时，使用 `review_blinko_daily_notes` 工具。

## 配置要求

### MCP Server 配置

在 `~/.copilot/mcp-config.json` 中添加：

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

### 环境变量

设置 `BLINKO_TOKEN` 环境变量：

```powershell
# Windows PowerShell (永久)
[Environment]::SetEnvironmentVariable("BLINKO_TOKEN", "your-api-key", "User")
```

## 常见场景

| 用户问题 | 使用工具 | 处理方式 |
|---------|---------|---------|
| "快速记录一个想法" | upsert_blinko_flash_note | 创建闪念 |
| "记录一下今天的会议内容" | upsert_blinko_note | 创建笔记 |
| "添加一个待办：明天开会" | upsert_blinko_todo | 创建待办 |
| "我之前记过关于XX的内容" | search_blinko_notes | 搜索相关笔记 |
| "分享这条笔记给朋友" | share_blinko_note | 分享笔记 |
| "今天有什么要回顾的" | review_blinko_daily_notes | 获取今日回顾 |
| "清空回收站" | clear_blinko_recycle_bin | 永久删除 |

## 详细文档

- 查看 [references/REFERENCE.md](references/REFERENCE.md) 获取工具参数详细说明
- 查看 [mcp-server-blinko](https://github.com/BryceWG/mcp-server-blinko) 获取更多信息
