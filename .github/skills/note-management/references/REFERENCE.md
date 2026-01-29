# Blinko MCP Server 参考文档

## 概述

[mcp-server-blinko](https://github.com/BryceWG/mcp-server-blinko) 是一个 MCP 服务器，用于与 [Blinko](https://github.com/blinko-space/blinko) 笔记服务交互。

## MCP 配置

- **类型**: stdio (本地 npx 进程)
- **包名**: `mcp-server-blinko@0.0.9`
- **环境变量**: `BLINKO_DOMAIN`, `BLINKO_API_KEY`

## 可用工具详情

### upsert_blinko_flash_note

创建闪念 (type 0)，用于快速记录想法和灵感。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `content` | string | ✓ | 闪念内容 |

**返回**: 成功消息和创建的笔记 ID

**示例场景**:
```
用户: 快速记一下，明天要买咖啡
工具调用: upsert_blinko_flash_note(content="明天要买咖啡")
```

### upsert_blinko_note

创建笔记 (type 1)，用于详细记录内容。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `content` | string | ✓ | 笔记内容 |

**返回**: 成功消息和创建的笔记 ID

**示例场景**:
```
用户: 记录一下今天的会议纪要：讨论了Q2计划...
工具调用: upsert_blinko_note(content="今天的会议纪要：讨论了Q2计划...")
```

### upsert_blinko_todo

创建待办事项 (type 2)。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `content` | string | ✓ | 待办内容 |

**返回**: 成功消息和创建的待办 ID

**示例场景**:
```
用户: 添加待办：完成项目报告
工具调用: upsert_blinko_todo(content="完成项目报告")
```

### search_blinko_notes

搜索笔记，支持多种过滤条件。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `searchText` | string | ✓ | 搜索关键词 |
| `size` | number | ✗ | 返回结果数量 (默认: 5) |
| `type` | number | ✗ | 笔记类型: -1=全部, 0=闪念, 1=笔记 |
| `isArchived` | boolean | ✗ | 搜索已归档笔记 |
| `isRecycle` | boolean | ✗ | 搜索回收站笔记 |
| `isUseAiQuery` | boolean | ✗ | 使用 AI 搜索 (默认: true) |
| `startDate` | string | ✗ | 开始日期 (ISO 格式) |
| `endDate` | string | ✗ | 结束日期 (ISO 格式) |
| `hasTodo` | boolean | ✗ | 仅搜索包含待办的笔记 |

**返回**: 匹配笔记列表，包含 ID、内容和时间戳

**示例场景**:
```
用户: 搜索关于项目的笔记
工具调用: search_blinko_notes(searchText="项目", size=10)
```

### share_blinko_note

分享笔记或取消分享。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `noteId` | number | ✓ | 笔记 ID |
| `password` | string | ✗ | 6位分享密码 |
| `isCancel` | boolean | ✗ | 是否取消分享 (默认: false) |

**返回**: 分享状态、密码 (如果设置)、分享链接

**示例场景**:
```
用户: 分享笔记 123，设置密码 666666
工具调用: share_blinko_note(noteId=123, password="666666")
```

### review_blinko_daily_notes

获取今日待回顾的笔记。

**参数**: 无

**返回**: 今日回顾笔记列表，包含 ID 和内容

**示例场景**:
```
用户: 今天有什么要回顾的吗
工具调用: review_blinko_daily_notes()
```

### clear_blinko_recycle_bin

清空回收站，永久删除所有已删除的笔记。

**参数**: 无

**示例场景**:
```
用户: 清空回收站
工具调用: clear_blinko_recycle_bin()
```

## 配置说明

### 获取 API Key

1. 登录 Blinko 管理界面
2. 进入设置 -> API 设置
3. 生成新的 API Key

### 环境变量配置

```powershell
# Windows
[Environment]::SetEnvironmentVariable("BLINKO_TOKEN", "your-api-key", "User")

# Linux/macOS
export BLINKO_TOKEN="your-api-key"
```

### MCP 配置文件

位置: `~/.copilot/mcp-config.json`

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

### BLINKO_DOMAIN 格式

支持多种格式：
- 纯域名: `myblinko.com`, `localhost:3000`
- 完整 URL: `https://myblinko.com`, `http://localhost:3000`

## 相关链接

- [mcp-server-blinko](https://github.com/BryceWG/mcp-server-blinko) - MCP 服务器
- [Blinko](https://github.com/blinko-space/blinko) - Blinko 笔记服务
- [MCP 协议规范](https://modelcontextprotocol.io/)
