#!/usr/bin/env python3
"""
视频转 Markdown 工具

从在线视频提取字幕内容，生成带时间戳的字幕和 Markdown 文档。
优先下载视频自带字幕，无字幕时才使用 Whisper 语音识别。

用法:
    uv run video_to_markdown.py <视频URL> [选项]

示例:
    uv run video_to_markdown.py "https://www.youtube.com/watch?v=xxxxx"
    uv run video_to_markdown.py "https://www.bilibili.com/video/BVxxxxx" --model medium
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional


def check_dependencies(need_whisper: bool = False) -> list[str]:
    """检查必需的依赖工具"""
    missing = []
    
    # 检查 yt-dlp
    if shutil.which("yt-dlp") is None:
        missing.append("yt-dlp")
    
    # 检查 ffmpeg
    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg")
    
    # 仅在需要时检查 whisper
    if need_whisper:
        try:
            import whisper  # noqa: F401
        except ImportError:
            missing.append("openai-whisper")
    
    return missing


def get_video_info(url: str) -> dict:
    """获取视频信息"""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"获取视频信息失败: {result.stderr}")
    
    return json.loads(result.stdout)


def download_subtitles(url: str, output_dir: str, lang: Optional[str] = None) -> Optional[str]:
    """
    尝试下载视频字幕
    
    优先级：
    1. 指定语言的人工字幕
    2. 指定语言的自动字幕
    3. 中文字幕 (zh, zh-Hans, zh-CN)
    4. 英文字幕 (en)
    5. 任意可用字幕
    
    Returns:
        字幕文件路径，如果没有字幕则返回 None
    """
    # 语言优先级列表
    if lang:
        lang_priority = [lang]
    else:
        lang_priority = ["zh", "zh-Hans", "zh-CN", "zh-TW", "en", "en-US", "ja", "ko"]
    
    # 先尝试下载人工字幕
    for try_lang in lang_priority:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--sub-lang", try_lang,
            "--sub-format", "vtt/srt/ass/best",
            "--skip-download",
            "--no-playlist",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 查找下载的字幕文件
        for file in os.listdir(output_dir):
            if file.endswith((".vtt", ".srt", ".ass")):
                print(f"找到人工字幕: {file}", file=sys.stderr)
                return os.path.join(output_dir, file)
    
    # 尝试下载自动生成字幕
    for try_lang in lang_priority:
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", try_lang,
            "--sub-format", "vtt/srt/best",
            "--skip-download",
            "--no-playlist",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        for file in os.listdir(output_dir):
            if file.endswith((".vtt", ".srt", ".ass")):
                print(f"找到自动字幕: {file}", file=sys.stderr)
                return os.path.join(output_dir, file)
    
    # 最后尝试获取任意字幕
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-format", "vtt/srt/best",
        "--skip-download",
        "--no-playlist",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    subprocess.run(cmd, capture_output=True, text=True)
    
    for file in os.listdir(output_dir):
        if file.endswith((".vtt", ".srt", ".ass")):
            print(f"找到字幕: {file}", file=sys.stderr)
            return os.path.join(output_dir, file)
    
    return None


def parse_vtt(content: str) -> list[dict]:
    """解析 VTT 字幕文件"""
    segments = []
    
    # 移除 VTT 头部
    lines = content.strip().split("\n")
    
    current_start = None
    current_text = []
    
    time_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})")
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行和 WEBVTT 头
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            if current_start is not None and current_text:
                text = " ".join(current_text).strip()
                # 移除 VTT 标签
                text = re.sub(r"<[^>]+>", "", text)
                if text:
                    segments.append({
                        "start": current_start,
                        "text": text
                    })
            current_start = None
            current_text = []
            continue
        
        # 解析时间戳行
        if " --> " in line:
            # 保存之前的段落
            if current_start is not None and current_text:
                text = " ".join(current_text).strip()
                text = re.sub(r"<[^>]+>", "", text)
                if text:
                    segments.append({
                        "start": current_start,
                        "text": text
                    })
            
            # 解析新的时间戳
            time_parts = line.split(" --> ")
            match = time_pattern.match(time_parts[0])
            if match:
                h, m, s, ms = map(int, match.groups())
                current_start = h * 3600 + m * 60 + s + ms / 1000
            current_text = []
        elif current_start is not None and not line.isdigit():
            current_text.append(line)
    
    # 处理最后一段
    if current_start is not None and current_text:
        text = " ".join(current_text).strip()
        text = re.sub(r"<[^>]+>", "", text)
        if text:
            segments.append({
                "start": current_start,
                "text": text
            })
    
    return segments


def parse_srt(content: str) -> list[dict]:
    """解析 SRT 字幕文件"""
    segments = []
    
    # SRT 格式：序号、时间戳、文本、空行
    blocks = re.split(r"\n\n+", content.strip())
    
    time_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 2:
            # 找到时间戳行
            for i, line in enumerate(lines):
                if " --> " in line:
                    match = time_pattern.match(line)
                    if match:
                        h, m, s, ms = map(int, match.groups())
                        start = h * 3600 + m * 60 + s + ms / 1000
                        text = " ".join(lines[i+1:]).strip()
                        if text:
                            segments.append({
                                "start": start,
                                "text": text
                            })
                    break
    
    return segments


def parse_subtitle_file(file_path: str) -> list[dict]:
    """解析字幕文件"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    if file_path.endswith(".vtt"):
        return parse_vtt(content)
    elif file_path.endswith(".srt"):
        return parse_srt(content)
    elif file_path.endswith(".ass"):
        # ASS 格式较复杂，简单提取文本
        segments = []
        for line in content.split("\n"):
            if line.startswith("Dialogue:"):
                parts = line.split(",", 9)
                if len(parts) >= 10:
                    # 解析时间
                    time_str = parts[1].strip()
                    try:
                        h, m, s = time_str.split(":")
                        start = int(h) * 3600 + int(m) * 60 + float(s)
                        text = parts[9].strip()
                        # 移除 ASS 标签
                        text = re.sub(r"\{[^}]+\}", "", text)
                        if text:
                            segments.append({"start": start, "text": text})
                    except ValueError:
                        pass
        return segments
    
    return []


def download_audio(url: str, output_dir: str) -> tuple[str, dict]:
    """使用 yt-dlp 下载视频的音频轨道"""
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    
    # 获取视频信息
    video_info = get_video_info(url)
    
    # 下载音频
    download_cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_template,
        "--no-playlist",
        url
    ]
    
    print(f"正在下载音频: {video_info.get('title', 'Unknown')}", file=sys.stderr)
    
    result = subprocess.run(download_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"下载音频失败: {result.stderr}")
    
    for file in os.listdir(output_dir):
        if file.endswith(".mp3"):
            return os.path.join(output_dir, file), video_info
    
    raise RuntimeError("未找到下载的音频文件")


def transcribe_audio(audio_path: str, model_name: str = "base", language: Optional[str] = None) -> list[dict]:
    """使用 Whisper 进行语音识别"""
    import whisper
    
    print(f"正在加载 Whisper 模型: {model_name}", file=sys.stderr)
    model = whisper.load_model(model_name)
    
    print("正在进行语音识别...", file=sys.stderr)
    
    options = {"verbose": False}
    if language:
        options["language"] = language
    
    result = model.transcribe(audio_path, **options)
    
    segments = []
    for segment in result["segments"]:
        segments.append({
            "start": segment["start"],
            "text": segment["text"].strip()
        })
    
    return segments


def format_timestamp(seconds: float) -> str:
    """将秒数转换为时间戳格式 HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 3600:
        return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"
    return format_timestamp(seconds)


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除控制字符
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    # 截断过长的文件名
    if len(filename) > 200:
        filename = filename[:200]
    return filename.strip()


def generate_markdown(
    video_info: dict,
    segments: list[dict],
    url: str,
    output_path: Optional[str] = None
) -> str:
    """
    生成 Markdown 文档
    
    Returns:
        str: 生成的 Markdown 内容
    """
    title = video_info.get("title", "未知标题")
    duration = video_info.get("duration", 0)
    
    lines = [
        f"# {title}",
        "",
        f"> 来源: [{url}]({url})",
        f"> 时长: {format_duration(duration)}",
        f"> 提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 完整字幕",
        "",
    ]
    
    # 添加字幕内容
    for segment in segments:
        timestamp = format_timestamp(segment["start"])
        text = segment["text"]
        lines.append(f"[{timestamp}] {text}")
    
    lines.extend([
        "",
        "---",
        "",
        "## 要点摘要",
        "",
        "（请根据上述字幕内容，分析并生成结构化的要点摘要）",
        "",
    ])
    
    content = "\n".join(lines)
    
    # 写入文件
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已保存到: {output_path}", file=sys.stderr)
    
    return content


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从在线视频提取字幕内容，生成 Markdown 文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "https://www.youtube.com/watch?v=xxxxx"
  %(prog)s "https://www.bilibili.com/video/BVxxxxx" --lang zh
  %(prog)s "https://..." --output notes.md --force-whisper
        """
    )
    
    parser.add_argument("url", help="视频 URL")
    parser.add_argument(
        "--model", "-m",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper 模型大小，仅在无字幕时使用 (默认: base)"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径 (默认: <视频标题>.md)"
    )
    parser.add_argument(
        "--lang", "-l",
        help="优先下载的字幕语言代码，如 zh, en, ja"
    )
    parser.add_argument(
        "--force-whisper",
        action="store_true",
        help="强制使用 Whisper 语音识别，忽略视频自带字幕"
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="保留下载的音频文件"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="输出 JSON 格式（包含元数据和字幕）"
    )
    
    args = parser.parse_args()
    
    # 先检查基本依赖（yt-dlp, ffmpeg）
    missing = check_dependencies(need_whisper=False)
    if missing:
        print(f"错误: 缺少必需的依赖: {', '.join(missing)}", file=sys.stderr)
        print("\n请安装缺少的依赖:", file=sys.stderr)
        print("  uv sync --extra video", file=sys.stderr)
        print("  winget install FFmpeg  # Windows", file=sys.stderr)
        return 1
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # 获取视频信息
            print("正在获取视频信息...", file=sys.stderr)
            video_info = get_video_info(args.url)
            print(f"视频标题: {video_info.get('title', 'Unknown')}", file=sys.stderr)
            
            segments = None
            subtitle_source = None
            
            # 优先尝试下载字幕（除非强制使用 Whisper）
            if not args.force_whisper:
                print("正在尝试下载字幕...", file=sys.stderr)
                subtitle_path = download_subtitles(args.url, temp_dir, args.lang)
                
                if subtitle_path:
                    print("正在解析字幕文件...", file=sys.stderr)
                    segments = parse_subtitle_file(subtitle_path)
                    if segments:
                        subtitle_source = "downloaded"
                        print(f"成功提取 {len(segments)} 条字幕", file=sys.stderr)
            
            # 如果没有字幕，使用 Whisper
            if segments is None or len(segments) == 0:
                print("未找到可用字幕，将使用 Whisper 进行语音识别...", file=sys.stderr)
                
                # 检查 Whisper 依赖
                missing = check_dependencies(need_whisper=True)
                if "openai-whisper" in missing:
                    print("错误: 需要安装 openai-whisper", file=sys.stderr)
                    print("  uv sync --extra video", file=sys.stderr)
                    return 1
                
                # 下载音频
                audio_path, _ = download_audio(args.url, temp_dir)
                
                # 语音识别
                segments = transcribe_audio(audio_path, args.model, args.lang)
                subtitle_source = "whisper"
                
                # 保留音频文件
                if args.keep_audio:
                    title = sanitize_filename(video_info.get("title", "video"))
                    audio_dest = f"{title}.mp3"
                    shutil.copy(audio_path, audio_dest)
                    print(f"音频已保存到: {audio_dest}", file=sys.stderr)
            
            # 确定输出路径
            if args.output:
                output_path = args.output
            else:
                title = sanitize_filename(video_info.get("title", "video"))
                output_path = f"{title}.md"
            
            # 生成 Markdown
            content = generate_markdown(video_info, segments, args.url, output_path)
            
            # 输出结果
            if args.json:
                result = {
                    "title": video_info.get("title"),
                    "url": args.url,
                    "duration": video_info.get("duration"),
                    "subtitle_source": subtitle_source,
                    "output_file": output_path,
                    "segments": segments
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(content)
            
            print(f"\n字幕来源: {'视频自带字幕' if subtitle_source == 'downloaded' else 'Whisper 语音识别'}", file=sys.stderr)
            return 0
            
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
