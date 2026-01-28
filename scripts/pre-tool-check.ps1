<#
.SYNOPSIS
    工具使用前的安全检查

.DESCRIPTION
    在 Copilot 使用工具之前执行此脚本，进行安全检查

.NOTES
    此脚本作为 preToolUse hook 被调用，从 stdin 接收 JSON 输入
    JSON 格式: {"tool": "工具名", "input": {...}, ...}
    返回 "APPROVED" 表示允许，返回 "DENIED: 原因" 表示拒绝
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
$toolInput = ""
try {
    if ($jsonInput -and $jsonInput.Trim()) {
        $data = $jsonInput | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($data.tool) {
            $toolName = $data.tool
        }
        # 获取工具输入的简要描述
        if ($data.input) {
            $inputStr = $data.input | ConvertTo-Json -Compress -Depth 1
            if ($inputStr.Length -gt 80) {
                $inputStr = $inputStr.Substring(0, 80) + "..."
            }
            $toolInput = " | Input: $inputStr"
        }
    }
} catch {
    # 解析失败时使用默认值
}

$logEntry = "[$timestamp] PRE  | Tool: $toolName$toolInput"

# 追加到日志文件
Add-Content -Path $logFile -Value $logEntry -Encoding UTF8

# 基本安全检查示例
# 可以在这里添加自定义的安全规则
# 例如：拒绝危险命令
# if ($toolName -eq "bash" -and $data.input.command -match "rm -rf") {
#     Write-Output "DENIED: 不允许执行危险的删除命令"
#     exit 0
# }

# 默认允许执行
Write-Output "APPROVED"
