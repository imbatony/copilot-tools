# MCP 服务器配置指令

适用于 Model Context Protocol (MCP) 服务器的配置和使用。

## MCP 概述

MCP 服务器为 Copilot 提供额外的数据源和工具能力。

## 配置文件位置

- 用户级配置: `~/.copilot/mcp-config.json`
- 可通过环境变量 `XDG_CONFIG_HOME` 更改位置

## 配置格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "命令",
      "args": ["参数列表"],
      "env": {
        "ENV_VAR": "value"
      },
      "disabled": false,
      "alwaysAllow": ["tool-name"]
    }
  }
}
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `command` | 启动 MCP 服务器的命令 |
| `args` | 命令参数数组 |
| `env` | 环境变量 |
| `disabled` | 是否禁用此服务器 |
| `alwaysAllow` | 自动允许的工具列表 |

## 常用 MCP 服务器

### GitHub MCP Server

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

### Filesystem MCP Server

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
  }
}
```

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
