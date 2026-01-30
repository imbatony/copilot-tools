---
name: video-to-markdown
description: >-
  视频转 Markdown 技能。从在线视频（YouTube、Bilibili 等）提取语音内容，
  生成带时间戳的字幕文本和结构化 Markdown 文档。当用户需要视频总结、
  视频笔记、提取视频内容、分析视频要点时使用此技能。
  支持长视频处理，输出包含完整字幕和结构化要点。
license: MIT
compatibility: >-
  需要安装 yt-dlp、FFmpeg 和 openai-whisper。
  Python 3.8+ 和 uv 包管理器。
metadata:
  author: copilot-tools
  version: "1.1.0"
  tools:
    - yt-dlp
    - ffmpeg
    - whisper
allowed-tools: Bash(uv:*) Bash(python:*) Bash(yt-dlp:*) Bash(ffmpeg:*) Read
---

# 视频转 Markdown 技能

从在线视频提取语音内容，生成结构化的 Markdown 文档，包含完整字幕和时间戳。

## 文件存储规范

| 文件类型 | 存储位置 | 说明 |
|---------|---------|------|
| 临时字幕文件 | `tmp/video-to-markdown/docs/` | 脚本生成的原始字幕 Markdown（含完整时间戳字幕） |
| 最终总结文档 | `docs/video-to-markdown/` | 经 LLM 分析后的摘要文档，**不含完整字幕**，与临时文件同名 |

> ⚠️ **重要**: 
> - 脚本输出的字幕文件统一保存到 `tmp/video-to-markdown/docs/` 目录
> - LLM 生成摘要后，将**仅包含摘要的文档**保存到 `docs/video-to-markdown/` 目录，保持同名
> - 最终总结文档**不需要保留完整字幕**，只保留结构化摘要

## 工作流程

1. **获取视频信息**: 使用 yt-dlp 获取视频元数据
2. **下载字幕（优先）**: 尝试下载视频自带的人工/自动字幕
3. **语音识别（备用）**: 如果没有字幕，使用 Whisper 进行语音识别
4. **生成临时文件**: 输出带时间戳的 Markdown 到 `tmp/video-to-markdown/docs/`
5. **LLM 分析**: 根据字幕内容生成要点摘要
6. **保存最终文档**: 将摘要文档（不含字幕）保存到 `docs/video-to-markdown/`，保持同名

> 💡 **优先使用视频自带字幕**：YouTube、Bilibili 等平台的视频大多有字幕，直接下载比语音识别更快更准确。

## 使用方法

### 步骤 1: 提取字幕

```bash
# 切换到 skill 目录
cd .github/skills/video-to-markdown

# 提取字幕到临时目录
uv run scripts/video_to_markdown.py <视频URL> --output ../../../tmp/video-to-markdown/docs/<文件名>.md
```

### 步骤 2: 生成摘要

脚本输出字幕内容后，LLM 应根据字幕内容生成结构化摘要。

### 步骤 3: 保存最终文档

将包含字幕和摘要的完整文档保存到 `docs/video-to-markdown/` 目录，保持与临时文件同名。

### 示例

```bash
# 从 YouTube 视频提取字幕（保存到临时目录）
uv run scripts/video_to_markdown.py "https://www.youtube.com/watch?v=xxxxx" \
  --output ../../../tmp/video-to-markdown/docs/视频标题.md

# 从 Bilibili 视频提取字幕
uv run scripts/video_to_markdown.py "https://www.bilibili.com/video/BVxxxxx" \
  --output ../../../tmp/video-to-markdown/docs/视频标题.md

# 指定优先下载中文字幕
uv run scripts/video_to_markdown.py "https://..." --lang zh

# 强制使用 Whisper 语音识别
uv run scripts/video_to_markdown.py "https://..." --force-whisper --model medium
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 视频 URL（必需） | - |
| `--lang` | 优先下载的字幕语言（如 zh, en, ja） | 自动选择 |
| `--model` | Whisper 模型，仅在无字幕时使用 | base |
| `--output` | 输出文件路径（建议使用 `tmp/video-to-markdown/docs/`） | `<video_title>.md` |
| `--force-whisper` | 强制使用语音识别，忽略自带字幕 | False |
| `--keep-audio` | 保留下载的音频文件 | False |
| `--json` | 输出 JSON 格式 | False |

## 输出格式

生成的 Markdown 文件结构：

```markdown
# 视频标题

> 来源: [原始链接](URL)
> 时长: HH:MM:SS
> 提取时间: YYYY-MM-DD

## 完整字幕

[00:00:00] 字幕内容...
[00:00:05] 字幕内容...
...

---

## 要点摘要

（由 LLM 根据字幕内容生成）
```

## 依赖工具

### 安装 Python 依赖

使用 uv 安装视频处理相关依赖：

```bash
uv sync --extra video
```

### 安装 FFmpeg

FFmpeg 需要单独安装（非 Python 包）：

```bash
# Windows (winget)
winget install FFmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### 验证安装

```bash
uv run yt-dlp --version
ffmpeg -version
uv run whisper --help
```

## 详细文档

- 查看 [references/REFERENCE.md](references/REFERENCE.md) 获取技术细节
- 查看 [scripts/video_to_markdown.py](scripts/video_to_markdown.py) 获取源码

## 常见场景

| 用户问题 | 处理方式 |
|---------|---------|
| "帮我总结这个视频" | 提取字幕后生成要点摘要 |
| "这个视频讲了什么" | 提取字幕并分析主要内容 |
| "把视频转成文字" | 提取完整字幕文本 |
| "视频太长，帮我提炼要点" | 提取字幕后生成结构化摘要 |

## 注意事项

1. **字幕优先**: 脚本会优先下载视频自带字幕，比语音识别更快更准确
2. **语言选择**: 使用 `--lang zh` 优先下载中文字幕
3. **Whisper 备用**: 仅在视频无字幕时才使用 Whisper，可用 `--force-whisper` 强制启用
4. **模型选择**: base 模型速度快但准确度一般，medium/large 更准确但更慢
5. **网络要求**: 下载视频和字幕需要网络，Whisper 本地运行无需网络
