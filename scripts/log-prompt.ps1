<#
.SYNOPSIS
    记录用户提交的 prompt

.DESCRIPTION
    当用户在 Copilot CLI 中提交 prompt 时，此脚本会记录相关信息

.NOTES
    此脚本作为 hook 被调用，从 stdin 接收 JSON 输入
    JSON 格式: {"prompt": "用户输入的内容", ...}
#>

# 确保日志目录存在
$logDir = Join-Path $PSScriptRoot ".." "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "prompts.log"

# 从 stdin 读取 JSON 输入
$jsonInput = $input | Out-String

# 记录时间戳
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 尝试解析 JSON 获取 prompt 内容
$promptText = "(unknown)"
try {
    if ($jsonInput -and $jsonInput.Trim()) {
        $data = $jsonInput | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($data.prompt) {
            # 截取前 100 个字符，避免日志过长
            $promptText = $data.prompt
            if ($promptText.Length -gt 100) {
                $promptText = $promptText.Substring(0, 100) + "..."
            }
            # 移除换行符
            $promptText = $promptText -replace "`r`n|`n|`r", " "
        }
    }
} catch {
    # 解析失败时使用默认值
}

$logEntry = "[$timestamp] PROMPT: $promptText"

# 追加到日志文件
Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
