# 视频转 Markdown 技术参考

## 安装依赖

使用 uv 安装 Python 依赖：

```bash
uv sync --extra video
```

## 工具链说明

### yt-dlp

[yt-dlp](https://github.com/yt-dlp/yt-dlp) 是 youtube-dl 的活跃分支，支持众多视频网站。

#### 支持的网站

- YouTube
- Bilibili
- Twitter/X
- TikTok/抖音
- Vimeo
- 更多: 运行 `yt-dlp --list-extractors`

#### 常用命令

```bash
# 仅下载音频
yt-dlp -x --audio-format mp3 <URL>

# 获取视频信息（不下载）
yt-dlp --dump-json --no-download <URL>

# 下载字幕（如果有）
yt-dlp --write-sub --sub-lang zh,en <URL>
```

### FFmpeg

[FFmpeg](https://ffmpeg.org/) 用于音视频处理，yt-dlp 依赖它进行格式转换。

#### 安装方式

| 平台 | 命令 |
|------|------|
| Windows | `winget install FFmpeg` |
| macOS | `brew install ffmpeg` |
| Ubuntu | `sudo apt install ffmpeg` |

### OpenAI Whisper

[Whisper](https://github.com/openai/whisper) 是 OpenAI 开源的语音识别模型。

#### 模型对比

| 模型 | 大小 | 内存需求 | 相对速度 | 适用场景 |
|------|------|----------|----------|----------|
| tiny | 39M | ~1GB | 32x | 快速测试 |
| base | 74M | ~1GB | 16x | 日常使用 |
| small | 244M | ~2GB | 6x | 较高准确度 |
| medium | 769M | ~5GB | 2x | 高准确度 |
| large | 1550M | ~10GB | 1x | 最高准确度 |

#### 支持语言

Whisper 支持 99 种语言，包括：
- 中文 (zh)
- 英语 (en)
- 日语 (ja)
- 韩语 (ko)
- 等等

完整列表: `whisper --help`

## 输出格式详解

### 时间戳格式

使用 `HH:MM:SS` 格式:

```
[00:00:00] 视频开头内容
[00:01:30] 一分三十秒处的内容
[01:00:00] 一小时处的内容
```

### Markdown 结构

```markdown
# 视频标题

> 来源: [链接](URL)
> 时长: MM:SS
> 提取时间: YYYY-MM-DD

## 完整字幕

带时间戳的完整转录内容...

---

## 要点摘要

（由 LLM 生成）
```

## 性能优化

### GPU 加速

如果有 NVIDIA GPU，Whisper 会自动使用 CUDA 加速：

```bash
# 检查 PyTorch CUDA 支持
python -c "import torch; print(torch.cuda.is_available())"
```

### 长视频处理

对于长视频（>1小时），建议：

1. 使用 `base` 或 `small` 模型平衡速度和准确度
2. 确保有足够的磁盘空间存储临时文件
3. 考虑分段处理

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Unable to download` | 网络问题或视频不可用 | 检查 URL 和网络连接 |
| `ffmpeg not found` | FFmpeg 未安装 | 安装 FFmpeg |
| `CUDA out of memory` | GPU 内存不足 | 使用较小的模型或 CPU 模式 |

### 强制使用 CPU

```python
# 在代码中指定
model = whisper.load_model("base", device="cpu")
```

## 扩展功能

### 提取现有字幕

如果视频已有字幕，可以直接提取：

```bash
# 下载自动字幕
yt-dlp --write-auto-sub --sub-lang zh --skip-download <URL>

# 下载人工字幕
yt-dlp --write-sub --sub-lang zh --skip-download <URL>
```

### 批量处理

```bash
# 从文件读取 URL 列表
for url in $(cat urls.txt); do
    uv run video_to_markdown.py "$url"
done
```

## 参考链接

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg 官网](https://ffmpeg.org/)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Whisper 模型说明](https://github.com/openai/whisper#available-models-and-languages)
