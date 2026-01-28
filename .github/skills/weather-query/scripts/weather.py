#!/usr/bin/env python3
"""
天气查询脚本

使用 wttr.in API 获取指定城市的天气信息，并输出 JSON 格式结果。

用法:
    python weather.py <城市名> [--forecast] [--json] [--lang LANG]

示例:
    python weather.py 北京
    python weather.py Shanghai --forecast
    python weather.py 深圳 --json
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional


def get_dressing_advice(temperature: int) -> str:
    """根据温度返回穿衣建议"""
    if temperature < 0:
        return "羽绒服、棉服、围巾、手套、帽子"
    elif temperature < 10:
        return "厚外套、毛衣、保暖内衣"
    elif temperature < 15:
        return "薄外套、卫衣、长裤"
    elif temperature < 20:
        return "长袖衬衫、薄毛衣、休闲裤"
    elif temperature < 25:
        return "T恤、薄长裤、休闲装"
    elif temperature < 30:
        return "短袖、短裤、透气衣物"
    else:
        return "轻薄短袖、短裤、注意防晒"


def get_travel_advice(weather_desc: str) -> str:
    """根据天气描述返回出行建议"""
    desc = weather_desc.lower()
    
    if any(word in desc for word in ["晴", "sunny", "clear"]):
        return "适合户外活动，注意防晒"
    elif any(word in desc for word in ["阴", "cloudy", "overcast"]):
        return "适合出行，温度适宜"
    elif any(word in desc for word in ["小雨", "light rain", "drizzle", "patchy"]):
        return "建议携带雨具"
    elif any(word in desc for word in ["大雨", "暴雨", "heavy rain", "storm", "thunder"]):
        return "建议减少外出"
    elif any(word in desc for word in ["雪", "snow"]):
        return "注意保暖和防滑"
    elif any(word in desc for word in ["雾", "霾", "fog", "haze", "mist"]):
        return "建议佩戴口罩，减少户外活动"
    else:
        return "天气正常，适合出行"


def fetch_weather(city: str, lang: str = "zh") -> Optional[dict]:
    """从 wttr.in API 获取天气数据"""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1&lang={lang}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.URLError as e:
        print(f"网络错误: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"数据解析错误: {e}", file=sys.stderr)
        return None


def parse_weather_data(data: dict, city: str) -> dict:
    """解析天气数据并生成结构化输出"""
    current = data.get("current_condition", [{}])[0]
    today = data.get("weather", [{}])[0]
    astronomy = today.get("astronomy", [{}])[0] if today.get("astronomy") else {}
    
    temperature = int(current.get("temp_C", 0))
    weather_desc = current.get("weatherDesc", [{"value": "未知"}])[0].get("value", "未知")
    
    result = {
        "city": city,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "temperature": temperature,
        "feels_like": int(current.get("FeelsLikeC", temperature)),
        "humidity": int(current.get("humidity", 0)),
        "wind_speed": int(current.get("windspeedKmph", 0)),
        "weather_desc": weather_desc,
        "temp_range": {
            "min": int(today.get("mintempC", 0)),
            "max": int(today.get("maxtempC", 0))
        },
        "sunrise": astronomy.get("sunrise", ""),
        "sunset": astronomy.get("sunset", ""),
        "dressing_advice": get_dressing_advice(temperature),
        "travel_advice": get_travel_advice(weather_desc)
    }
    
    return result


def parse_forecast_data(data: dict, city: str) -> list:
    """解析未来天气预报数据"""
    forecasts = []
    weather_list = data.get("weather", [])
    
    for day in weather_list:
        hourly = day.get("hourly", [{}])
        # 取中午12点的数据作为代表
        noon_data = hourly[4] if len(hourly) > 4 else hourly[0] if hourly else {}
        
        weather_desc = noon_data.get("weatherDesc", [{"value": "未知"}])[0].get("value", "未知")
        temperature = int(noon_data.get("tempC", 0))
        
        forecasts.append({
            "date": day.get("date", ""),
            "temp_range": {
                "min": int(day.get("mintempC", 0)),
                "max": int(day.get("maxtempC", 0))
            },
            "weather_desc": weather_desc,
            "humidity": int(noon_data.get("humidity", 0)),
            "dressing_advice": get_dressing_advice(temperature),
            "travel_advice": get_travel_advice(weather_desc)
        })
    
    return {"city": city, "forecasts": forecasts}


def format_output(result: dict, json_output: bool = False) -> str:
    """格式化输出结果"""
    if json_output:
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    if "forecasts" in result:
        # 预报模式
        lines = [
            f"\n🌤️ {result['city']} 未来天气预报",
            "━" * 40
        ]
        for f in result["forecasts"]:
            lines.extend([
                f"\n📅 {f['date']}",
                f"🌡️ 温度: {f['temp_range']['min']}°C ~ {f['temp_range']['max']}°C",
                f"🌤️ 天气: {f['weather_desc']}",
                f"💧 湿度: {f['humidity']}%",
                f"👔 穿衣: {f['dressing_advice']}"
            ])
        return "\n".join(lines)
    else:
        # 当前天气模式
        r = result
        return f"""
🌤️ {r['city']} 天气
{'━' * 40}

📅 日期: {r['date']}
🌡️ 温度: {r['temperature']}°C (体感温度: {r['feels_like']}°C)
📊 今日温度范围: {r['temp_range']['min']}°C ~ {r['temp_range']['max']}°C
💧 湿度: {r['humidity']}%
💨 风速: {r['wind_speed']} km/h
🌤️ 天气状况: {r['weather_desc']}
🌅 日出: {r['sunrise']}
🌇 日落: {r['sunset']}

{'━' * 40}
👔 穿衣建议: {r['dressing_advice']}
🚗 出行建议: {r['travel_advice']}
"""


def main():
    parser = argparse.ArgumentParser(
        description="查询天气信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python weather.py 北京
  python weather.py Shanghai --forecast
  python weather.py 深圳 --json
        """
    )
    parser.add_argument("city", help="要查询的城市名称（支持中英文）")
    parser.add_argument("--forecast", "-f", action="store_true", help="显示未来天气预报")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--lang", "-l", default="zh", help="语言代码（默认: zh）")
    
    args = parser.parse_args()
    
    # 获取天气数据
    data = fetch_weather(args.city, args.lang)
    if not data:
        print(f"❌ 无法获取 {args.city} 的天气信息", file=sys.stderr)
        sys.exit(1)
    
    # 检查是否为有效数据
    if "current_condition" not in data:
        print(f"❌ 未找到城市: {args.city}", file=sys.stderr)
        sys.exit(1)
    
    # 解析数据
    if args.forecast:
        result = parse_forecast_data(data, args.city)
    else:
        result = parse_weather_data(data, args.city)
    
    # 输出结果
    print(format_output(result, args.json))


if __name__ == "__main__":
    import urllib.parse
    main()
