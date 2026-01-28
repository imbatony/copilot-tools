# Hooks 编写指令

适用于 `.github/hooks/` 目录下的 Hook 配置开发。

## Hook 概述

Hook 是在 Agent 执行流程的关键节点执行的自定义脚本。

## 文件位置

Hook 配置文件: `.github/hooks/*.json`

## Hook 类型

| 类型 | 触发时机 | 用途 |
|------|---------|------|
| `sessionStart` | 会话开始 | 初始化环境、记录日志 |
| `sessionEnd` | 会话结束 | 清理资源、生成报告 |
| `userPromptSubmitted` | 用户提交 prompt | 记录请求、使用分析 |
| `preToolUse` | 工具执行前 | 安全检查、权限验证 |
| `postToolUse` | 工具执行后 | 记录结果、性能监控 |
| `errorOccurred` | 发生错误 | 错误日志、告警通知 |

## 配置格式

```json
{
  "version": 1,
  "hooks": {
    "hookType": [
      {
        "type": "command",
        "bash": "脚本路径或命令 (Unix)",
        "powershell": "脚本路径或命令 (Windows)",
        "cwd": "工作目录（相对于仓库根）",
        "env": {
          "KEY": "value"
        },
        "timeoutSec": 30
      }
    ]
  }
}
```

## 字段说明

| 字段 | 必需 | 说明 |
|------|------|------|
| `type` | ✅ | 必须为 `"command"` |
| `bash` | ✅ (Unix) | Bash 脚本或命令 |
| `powershell` | ✅ (Windows) | PowerShell 脚本或命令 |
| `cwd` | ❌ | 工作目录，相对于仓库根 |
| `env` | ❌ | 环境变量 |
| `timeoutSec` | ❌ | 超时时间（默认 30 秒） |

## preToolUse 特殊返回值

`preToolUse` hook 可以控制工具执行：

- 输出 `APPROVED`: 允许执行
- 输出 `DENIED: 原因`: 拒绝执行

```powershell
# 允许
Write-Output "APPROVED"

# 拒绝
Write-Output "DENIED: 不允许执行此命令"
```

## 脚本编写原则

### 性能

- 执行时间控制在 5 秒以内
- 使用异步日志记录
- 缓存昂贵的计算结果

### 安全

- 验证和清理输入
- 使用正确的 shell 转义
- 不记录敏感信息
- 设置合适的文件权限

### 可靠性

- 设置适当的超时
- 处理网络调用失败
- 提供清晰的错误信息

## 脚本模板

### PowerShell

```powershell
# scripts/hook-script.ps1

# 确保日志目录存在
$logDir = Join-Path $PSScriptRoot ".." "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 从 stdin 读取 JSON 输入
$inputData = $input | Out-String

# 记录日志
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path (Join-Path $logDir "hook.log") -Value "[$timestamp] Hook executed"

# 返回结果（仅 preToolUse 需要）
Write-Output "APPROVED"
```

### Bash

```bash
#!/bin/bash
# scripts/hook-script.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
LOG_FILE="$LOG_DIR/hook.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 从 stdin 读取 JSON 输入
INPUT=$(cat)

# 记录日志
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Hook executed" >> "$LOG_FILE"

# 返回结果（仅 preToolUse 需要）
echo "APPROVED"
```

## 示例配置

参见: `.github/hooks/session-hooks.json`
