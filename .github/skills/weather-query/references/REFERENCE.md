# 天气查询技能参考文档

本文档提供天气查询技能的详细技术参考。

## API 说明

### wttr.in API

本技能使用 [wttr.in](https://wttr.in) 免费天气 API，无需注册或 API Key。

#### 请求格式

```
GET https://wttr.in/{城市名}?format=j1&lang={语言代码}
```

#### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 城市名 | 支持中英文城市名 | `Beijing`, `北京`, `Shanghai` |
| format | 输出格式，`j1` 表示 JSON | `j1` |
| lang | 语言代码 | `zh`, `en` |

#### 响应结构

```json
{
  "current_condition": [{
    "temp_C": "10",
    "temp_F": "50",
    "humidity": "65",
    "weatherCode": "116",
    "weatherDesc": [{"value": "Partly cloudy"}],
    "windspeedKmph": "15",
    "winddirDegree": "180",
    "winddir16Point": "S",
    "FeelsLikeC": "8",
    "FeelsLikeF": "46",
    "uvIndex": "3",
    "visibility": "10",
    "visibilityMiles": "6",
    "pressure": "1015",
    "pressureInches": "30",
    "cloudcover": "50",
    "precipMM": "0.0",
    "precipInches": "0.0"
  }],
  "weather": [{
    "date": "2024-01-15",
    "maxtempC": "15",
    "mintempC": "5",
    "avgtempC": "10",
    "astronomy": [{
      "sunrise": "07:00 AM",
      "sunset": "05:30 PM",
      "moonrise": "10:00 AM",
      "moonset": "09:00 PM",
      "moon_phase": "Waxing Crescent",
      "moon_illumination": "25"
    }],
    "hourly": [
      {
        "time": "0",
        "tempC": "8",
        "weatherDesc": [{"value": "Clear"}],
        "humidity": "70",
        "windspeedKmph": "10"
      }
    ]
  }]
}
```

## 穿衣建议规则

| 温度范围 | 建议 | 说明 |
|---------|------|------|
| < 0°C | 羽绒服、棉服、围巾、手套、帽子 | 严寒天气，需全面保暖 |
| 0-10°C | 厚外套、毛衣、保暖内衣 | 寒冷天气，注意保暖 |
| 10-15°C | 薄外套、卫衣、长裤 | 凉爽天气，适当保暖 |
| 15-20°C | 长袖衬衫、薄毛衣、休闲裤 | 舒适天气，轻便穿着 |
| 20-25°C | T恤、薄长裤、休闲装 | 温暖天气，轻薄穿着 |
| 25-30°C | 短袖、短裤、透气衣物 | 炎热天气，选择透气面料 |
| > 30°C | 轻薄短袖、短裤、注意防晒 | 高温天气，注意防暑降温 |

## 出行建议规则

| 天气类型 | 关键词 | 建议 |
|---------|-------|------|
| 晴天 | sunny, clear, 晴 | 适合户外活动，注意防晒 |
| 阴天 | cloudy, overcast, 阴 | 适合出行，温度适宜 |
| 小雨 | light rain, drizzle, patchy, 小雨 | 建议携带雨具 |
| 大雨/暴雨 | heavy rain, storm, thunder, 大雨, 暴雨 | 建议减少外出 |
| 雪天 | snow, 雪 | 注意保暖和防滑 |
| 雾霾 | fog, haze, mist, 雾, 霾 | 建议佩戴口罩，减少户外活动 |

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| 网络错误 | 无法连接到 API | 检查网络连接 |
| 城市未找到 | 城市名称无效 | 使用正确的城市名称 |
| 数据解析错误 | API 返回格式异常 | 稍后重试 |

## 使用限制

- wttr.in 是免费服务，请勿滥用
- 建议缓存结果，避免频繁请求
- 高峰期可能响应较慢
