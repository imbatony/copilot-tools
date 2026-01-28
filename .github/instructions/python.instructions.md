# Python 开发指令

适用于本项目中所有 Python 代码的编写规范。

## 运行环境

- 使用 `uv` 作为包管理器和运行时
- Python 版本: 3.8+
- 优先使用标准库，减少外部依赖

## 代码风格

### 基本规范

- 遵循 PEP 8 代码风格
- 行长度限制: 100 字符
- 使用 4 空格缩进
- 使用 UTF-8 编码

### 命名规范

```python
# 变量和函数: snake_case
user_name = "test"
def get_weather_data():
    pass

# 类名: PascalCase
class WeatherClient:
    pass

# 常量: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.example.com"

# 私有成员: 前缀下划线
_internal_cache = {}
def _parse_response():
    pass
```

### 类型注解

始终添加类型注解：

```python
from typing import Optional, List, Dict

def fetch_weather(city: str, lang: str = "zh") -> Optional[dict]:
    """获取天气数据"""
    pass

def parse_data(items: List[str]) -> Dict[str, int]:
    """解析数据"""
    pass
```

### 文档字符串

使用 Google 风格的 docstring：

```python
def get_dressing_advice(temperature: int) -> str:
    """根据温度返回穿衣建议。

    Args:
        temperature: 当前温度（摄氏度）

    Returns:
        穿衣建议字符串

    Raises:
        ValueError: 如果温度超出合理范围
    """
    pass
```

## 脚本结构

### 标准模板

```python
#!/usr/bin/env python3
"""
脚本简短描述

详细说明...

用法:
    uv run script.py <参数>
"""

import argparse
import json
import sys
from typing import Optional


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(description="脚本描述")
    parser.add_argument("input", help="输入参数")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    try:
        # 业务逻辑
        result = process(args.input)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result))
        
        return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## 错误处理

### 使用明确的异常类型

```python
# 好
try:
    response = fetch_data(url)
except urllib.error.URLError as e:
    print(f"网络错误: {e}", file=sys.stderr)
except json.JSONDecodeError as e:
    print(f"数据解析错误: {e}", file=sys.stderr)

# 避免
try:
    response = fetch_data(url)
except Exception:
    print("出错了")
```

### 提供有用的错误信息

```python
if not city:
    print("错误: 请提供城市名称", file=sys.stderr)
    sys.exit(1)
```

## 输出格式

### 支持多种输出格式

```python
def format_output(result: dict, json_output: bool = False) -> str:
    if json_output:
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        return f"结果: {result['value']}"
```

### 使用 stderr 输出错误

```python
import sys

# 正常输出到 stdout
print(result)

# 错误输出到 stderr
print("错误信息", file=sys.stderr)
```

## 运行命令

```bash
# 运行脚本
uv run scripts/example.py

# 运行测试
uv run pytest

# 代码检查
uv run ruff check .
```
