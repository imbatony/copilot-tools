#!/bin/bash
#
# 工具使用前的安全检查
# 在 Copilot 使用工具之前执行此脚本，进行安全检查
#
# JSON 格式: {"tool": "工具名", "input": {...}, ...}
# 返回 "APPROVED" 表示允许，返回 "DENIED: 原因" 表示拒绝
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
TOOL_INPUT=""
if command -v jq &> /dev/null && [ -n "$INPUT" ]; then
    PARSED_TOOL=$(echo "$INPUT" | jq -r '.tool // "(unknown)"' 2>/dev/null)
    if [ -n "$PARSED_TOOL" ] && [ "$PARSED_TOOL" != "null" ]; then
        TOOL_NAME="$PARSED_TOOL"
    fi
    
    # 获取工具输入的简要描述
    PARSED_INPUT=$(echo "$INPUT" | jq -c '.input // {}' 2>/dev/null | head -c 80)
    if [ -n "$PARSED_INPUT" ] && [ "$PARSED_INPUT" != "{}" ]; then
        TOOL_INPUT=" | Input: ${PARSED_INPUT}"
        if [ ${#PARSED_INPUT} -ge 80 ]; then
            TOOL_INPUT="${TOOL_INPUT}..."
        fi
    fi
fi

LOG_ENTRY="[$TIMESTAMP] PRE  | Tool: $TOOL_NAME$TOOL_INPUT"

# 追加到日志文件
echo "$LOG_ENTRY" >> "$LOG_FILE"

# 基本安全检查示例
# 可以在这里添加自定义的安全规则

# 默认允许执行
echo "APPROVED"
