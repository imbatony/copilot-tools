# MCP 服务器配置指令

适用于 Model Context Protocol (MCP) 服务器的配置和使用。

## MCP 概述

MCP 服务器为 Copilot 提供额外的数据源和工具能力。

## 配置文件位置

- 用户级配置: `~/.copilot/mcp-config.json`
- 可通过环境变量 `XDG_CONFIG_HOME` 更改位置

## 服务器类型

MCP 服务器支持两种连接类型：

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **stdio** | 本地进程，通过标准输入输出通信 | 本地命令行工具 |
| **sse** | 远程服务器，通过 Server-Sent Events 通信 | 远程 API 服务 |
| **http** | 远程服务器，通过 HTTP 通信 | 远程 API 服务 |

## 配置格式

### stdio 类型（本地进程）

```json
{
  "mcpServers": {
    "server-name": {
      "command": "命令",
      "args": ["参数列表"],
      "env": {
        "ENV_VAR": "value"
      },
      "tools": ["*"],
      "disabled": false,
      "alwaysAllow": ["tool-name"]
    }
  }
}
```

### sse/http 类型（远程服务器）

```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse",
      "url": "https://example.com/sse",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      },
      "tools": ["*"],
      "disabled": false
    }
  }
}
```

## 字段说明

### 通用字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `tools` | ✓ | 工具列表，`["*"]` 表示启用所有工具，`[]` 禁用所有工具 |
| `disabled` | ✗ | 是否禁用此服务器 |
| `alwaysAllow` | ✗ | 自动允许的工具列表 |

### stdio 类型专用字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `command` | ✓ | 启动 MCP 服务器的命令 |
| `args` | ✓ | 命令参数数组 |
| `env` | ✗ | 环境变量 |

### sse/http 类型专用字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `type` | ✓ | 服务器类型：`"sse"` 或 `"http"` |
| `url` | ✓ | 服务器 URL |
| `headers` | ✗ | HTTP 请求头（用于认证等） |

## 常用 MCP 服务器

### GitHub MCP Server

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
    },
    "tools": ["*"]
  }
}
```

### Filesystem MCP Server

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
    "tools": ["*"]
  }
}
```

### 远程 SSE 服务器

```json
{
  "remote-api": {
    "type": "sse",
    "url": "https://api.example.com/mcp/sse",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    },
    "tools": ["*"]
  }
}
```

### Blinko 笔记服务

参考: [mcp-server-blinko](https://github.com/BryceWG/mcp-server-blinko)

```json
{
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
```

**支持的工具:**
- `upsert_blinko_flash_note` - 创建闪念
- `upsert_blinko_note` - 创建笔记
- `upsert_blinko_todo` - 创建待办事项
- `search_blinko_notes` - 搜索笔记
- `share_blinko_note` - 分享笔记
- `review_blinko_daily_notes` - 获取今日回顾
- `clear_blinko_recycle_bin` - 清空回收站

## 添加 MCP 服务器

### 方法 1: 在 Copilot CLI 中

```
/mcp add
```

按提示填写服务器信息。

### 方法 2: 编辑配置文件

直接编辑 `~/.copilot/mcp-config.json`。

## 管理 MCP 服务器

在 Copilot CLI 中：

```
# 查看已配置的服务器
/mcp

# 添加服务器
/mcp add

# 查看服务器工具
/mcp tools
```

## 工具权限

### 命令行控制

```bash
# 允许特定 MCP 服务器的所有工具
copilot --allow-tool 'My-MCP-Server'

# 允许特定工具
copilot --allow-tool 'My-MCP-Server(tool_name)'

# 拒绝特定工具
copilot --deny-tool 'My-MCP-Server(tool_name)'
```

## 环境变量

使用 `${VAR_NAME}` 语法引用环境变量：

```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}"
  }
}
```

## 示例配置

参见: `config/mcp-config.example.json`

## 安全注意事项

1. 不要在配置文件中明文存储敏感信息
2. 使用环境变量传递 API Key 和 Token
3. 定期审查已配置的 MCP 服务器
4. 谨慎使用 `alwaysAllow` 选项
