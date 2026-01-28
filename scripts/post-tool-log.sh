#!/bin/bash
#
# 工具使用后的日志记录
# 在 Copilot 使用工具之后执行此脚本，记录执行结果
#
# JSON 格式: {"tool": "工具名", "output": {...}, "error": null, ...}
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
LOG_FILE="$LOG_DIR/tool-usage.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 从 stdin 读取 JSON 输入
INPUT=$(cat)

# 记录时间戳
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 解析 JSON 获取工具信息 (需要 jq)
TOOL_NAME="(unknown)"
STATUS="OK"
if command -v jq &> /dev/null && [ -n "$INPUT" ]; then
    PARSED_TOOL=$(echo "$INPUT" | jq -r '.tool // "(unknown)"' 2>/dev/null)
    if [ -n "$PARSED_TOOL" ] && [ "$PARSED_TOOL" != "null" ]; then
        TOOL_NAME="$PARSED_TOOL"
    fi
    
    # 检查是否有错误
    ERROR=$(echo "$INPUT" | jq -r '.error // null' 2>/dev/null)
    if [ -n "$ERROR" ] && [ "$ERROR" != "null" ]; then
        STATUS="ERROR"
    fi
fi

LOG_ENTRY="[$TIMESTAMP] POST | Tool: $TOOL_NAME | Status: $STATUS"

# 追加到日志文件
echo "$LOG_ENTRY" >> "$LOG_FILE"
