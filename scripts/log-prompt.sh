#!/bin/bash
#
# 记录用户提交的 prompt
# 当用户在 Copilot CLI 中提交 prompt 时，此脚本会记录相关信息
#
# JSON 格式: {"prompt": "用户输入的内容", ...}
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
LOG_FILE="$LOG_DIR/prompts.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 从 stdin 读取 JSON 输入
INPUT=$(cat)

# 记录时间戳
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 尝试解析 JSON 获取 prompt 内容 (需要 jq)
PROMPT_TEXT="(unknown)"
if command -v jq &> /dev/null && [ -n "$INPUT" ]; then
    PARSED=$(echo "$INPUT" | jq -r '.prompt // "(unknown)"' 2>/dev/null)
    if [ -n "$PARSED" ] && [ "$PARSED" != "null" ]; then
        # 截取前 100 个字符，移除换行符
        PROMPT_TEXT=$(echo "$PARSED" | head -c 100 | tr '\n' ' ')
        if [ ${#PARSED} -gt 100 ]; then
            PROMPT_TEXT="${PROMPT_TEXT}..."
        fi
    fi
fi

LOG_ENTRY="[$TIMESTAMP] PROMPT: $PROMPT_TEXT"

# 追加到日志文件
echo "$LOG_ENTRY" >> "$LOG_FILE"
