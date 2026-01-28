---
name: weather-query
description: >-
  查询天气信息的技能。获取指定城市的当前天气、温度、湿度、风速，并提供穿衣和出行建议。
  当用户询问天气、气温、是否下雨、穿什么衣服、出行建议等问题时使用此技能。
  支持中英文城市名称查询。
license: MIT
compatibility: Requires uv (or Python 3.8+) and internet access
metadata:
  author: copilot-tools
  version: "1.0.0"
  api: wttr.in
allowed-tools: Bash(uv:*) Bash(python:*) Read
---

# 天气查询技能

获取指定城市的实时天气信息，包括温度、湿度、风速等，并根据天气状况提供穿衣和出行建议。

## 使用方法

使用 uv 运行 Python 脚本（推荐）：

```bash
uv run scripts/weather.py <城市名>
```

或者直接使用 Python：

```bash
python scripts/weather.py <城市名>
```

### 示例

```bash
# 查询北京天气
uv run scripts/weather.py 北京

# 查询上海天气
uv run scripts/weather.py Shanghai

# 查询天气预报（未来3天）
uv run scripts/weather.py 深圳 --forecast

# 输出 JSON 格式
uv run scripts/weather.py 北京 --json
```

## 输出格式

脚本输出 JSON 格式数据，包含以下字段：

```json
{
  "city": "城市名",
  "date": "日期",
  "temperature": "当前温度",
  "feels_like": "体感温度",
  "humidity": "湿度",
  "wind_speed": "风速",
  "weather_desc": "天气描述",
  "temp_range": {"min": "最低温", "max": "最高温"},
  "sunrise": "日出时间",
  "sunset": "日落时间",
  "dressing_advice": "穿衣建议",
  "travel_advice": "出行建议"
}
```

## 详细文档

- 查看 [references/REFERENCE.md](references/REFERENCE.md) 获取 API 详细说明
- 查看 [scripts/weather.py](scripts/weather.py) 获取脚本源码

## 常见场景

| 用户问题 | 处理方式 |
|---------|---------|
| "今天天气怎么样" | 查询用户所在城市或询问城市 |
| "北京明天会下雨吗" | 使用 `--forecast` 查询预报 |
| "我应该穿什么衣服" | 根据温度返回穿衣建议 |
| "适合出门吗" | 根据天气状况返回出行建议 |
