<#
.SYNOPSIS
    工具使用后的日志记录

.DESCRIPTION
    在 Copilot 使用工具之后执行此脚本，记录执行结果

.NOTES
    此脚本作为 postToolUse hook 被调用，从 stdin 接收 JSON 输入
    JSON 格式: {"tool": "工具名", "output": {...}, "error": null, ...}
#>

# 确保日志目录存在
$logDir = Join-Path $PSScriptRoot ".." "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "tool-usage.log"

# 从 stdin 读取 JSON 输入
$jsonInput = $input | Out-String

# 记录时间戳
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 解析 JSON 获取工具信息
$toolName = "(unknown)"
$status = "OK"
try {
    if ($jsonInput -and $jsonInput.Trim()) {
        $data = $jsonInput | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($data.tool) {
            $toolName = $data.tool
        }
        # 检查是否有错误
        if ($data.error) {
            $status = "ERROR"
        }
    }
} catch {
    # 解析失败时使用默认值
}

$logEntry = "[$timestamp] POST | Tool: $toolName | Status: $status"

# 追加到日志文件
Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
