# myriad-mind（大衍决）🔮

> Claude Code Skill — 神识一扫，万物皆可为笔记。视频转字幕/文章总结/AI 摘要/关键帧截图/英译中/Mermaid 图表/结构化学习笔记

将视频（抖音、小红书、B 站、YouTube 等）、文章（知乎、CSDN、Wiki 等）或本地视频/音频文件，一键炼化为：
- **字幕文本**（SRT + 纯文本，视频模式）
- **AI 总结**（标题 + 摘要 + 核心要点）
- **关键帧截图**（自动按间隔截取，视频模式）
- **Mermaid 图表**（架构图/流程图/时序图/状态图）
- **中英对照翻译**（英文内容自动翻译为中文）
- **结构化学习笔记**（Markdown 格式，含术语表 + 扩展资源 + 评论区精华）

## ✨ 功能亮点

| 功能 | 说明 |
|------|------|
| 🎥 多平台支持 | 抖音、小红书、B 站、YouTube、本地视频/音频文件 |
| 📝 字幕提取 | faster-whisper 本地 ASR（免费）+ 火山引擎云端 ASR（可选） |
| 🤖 AI 总结 | Claude 直接生成标题、摘要、核心要点 |
| 📸 关键帧截图 | ffmpeg 按时间间隔 / 场景变化自动截取，生成 JSON 索引 |
| 🌐 英译中 | 检测字幕语言，英文内容自动翻译并保留中英对照 |
| 📚 学习笔记 | 整合字幕 + 截图 + 翻译 + 摘要，生成 Markdown 学习笔记 |
| 🚀 GPU 加速 | 支持 NVIDIA CUDA 加速 whisper 转写 |

## 📋 效果演示

在 Claude Code 中发送：

```
帮我学习这个B站视频：https://www.bilibili.com/video/BV1xxxxxxxxxx
```

自动输出：

```markdown
## 视频分析结果

### 视频信息
| 项目 | 内容 |
|------|------|
| 视频ID | BV1xxxxxxxxxx |
| 作者 | 某知识博主 |
| 时长 | 15:30 |
| 来源平台 | B站 |

### AI生成标题
深度解析 Transformer 架构与注意力机制

### AI摘要
视频系统讲解了 Transformer 的核心架构...

### 核心要点
1. 自注意力机制（Self-Attention）的原理与计算方式
2. 多头注意力如何捕获不同维度的语义关系
3. 位置编码的必要性及正弦编码方案

### 生成文件
- 视频: /tmp/video_analysis/BV1xxxxxxxxxx/video.mp4
- 音频: /tmp/video_analysis/BV1xxxxxxxxxx/audio.mp3
- SRT字幕: /tmp/video_analysis/BV1xxxxxxxxxx/subtitle.srt
- 纯文本: /tmp/video_analysis/BV1xxxxxxxxxx/text.txt
- 关键帧截图: /tmp/video_analysis/BV1xxxxxxxxxx/frames/
- 翻译文本: /tmp/video_analysis/BV1xxxxxxxxxx/translated_text.txt
- 学习笔记: /tmp/video_analysis/BV1xxxxxxxxxx/learning_notes.md
```

---

## 🚀 安装指南

### 前置条件

| 依赖 | 必要性 | 说明 |
|------|--------|------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | ✅ 必须 | 支持 Skill 的 Agent 环境 |
| [FFmpeg](https://ffmpeg.org/) | ✅ 必须 | 音视频处理 |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | B站/YouTube 需要 | 视频下载与字幕抓取 |
| Python 3.9+ | faster-whisper 需要 | 本地语音转文字 |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 默认 ASR 后端 | 免费，本地运行 |
| [AI Douyin](https://ai-douyin.top9.cc) API Key | 抖音/小红书/B站需要 | 视频解析代理，免费额度 |

### 第一步：安装系统依赖

**FFmpeg：**

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows（推荐使用 winget）
winget install Gyan.FFmpeg

# Windows（或使用 Chocolatey）
choco install ffmpeg
```

**yt-dlp：**

```bash
# macOS
brew install yt-dlp

# 通用（需要 Python）
pip install -U yt-dlp
```

### 第二步：克隆并安装 Skill

```bash
# 克隆仓库
git clone https://github.com/imlewc/myriad-mind-skill.git

# 复制到 Claude Code 的 skills 目录
mkdir -p ~/.claude/skills
cp -r myriad-mind-skill ~/.claude/skills/myriad-mind

# 如果使用 Codex
mkdir -p ~/.codex/skills
cp -r myriad-mind-skill ~/.codex/skills/myriad-mind
```

### 第三步：安装 faster-whisper（默认 ASR 后端）

```bash
python3 ~/.claude/skills/myriad-mind/scripts/install_faster_whisper.py
```

> 安装脚本会自动检测 PyPI 镜像速度，创建独立 venv，检测到 NVIDIA GPU 时自动启用 CUDA 加速。

### 第四步：配置环境变量

```bash
# 复制配置模板
cp ~/.claude/skills/myriad-mind/.env.example ~/.claude/skills/myriad-mind/.env
```

编辑 `.env` 文件，填入你的 API Key：

```bash
# ASR 后端（默认 faster-whisper，可选 volcengine）
ASR_BACKEND=faster-whisper

# 视频解析代理（抖音/小红书/B站需要，YouTube 不需要）
# 注册 https://ai-douyin.top9.cc 获取免费 API Key
VIDEO_INFO_PROVIDER=ai-douyin
AI_DOUYIN_API_BASE=https://ai-douyin.top9.cc
AI_DOUYIN_API_KEY=your_api_key_here

# faster-whisper 参数
FW_MODEL_SIZE=small        # tiny/base/small/medium/large-v2
FW_DEVICE=auto             # auto 自动检测 GPU
FW_COMPUTE_TYPE=           # 留空自动选择
FW_PYTHON=                 # 留空使用默认 venv

# 关键帧截图参数
KF_INTERVAL=30             # 每 N 秒截一张图
KF_MAX_FRAMES=50           # 最多截取 N 张
KF_MODE=interval           # interval=固定间隔 / scene=场景变化 / both=两者
```

### 第五步：重启 Claude Code

```bash
# 退出当前 Claude Code 会话，重新启动即可生效
```

---

## 📖 使用方法

### 在线视频

在 Claude Code 中直接发送视频链接：

```
帮我总结这个视频：https://v.douyin.com/xxxxxx/
```

```
帮我学习这个B站视频：https://www.bilibili.com/video/BVxxxxxxxxxx/
```

```
提取这个 YouTube 视频的字幕：https://www.youtube.com/watch?v=O87FdYIPeQk
```

```
帮我学习这个小红书视频：https://www.xiaohongshu.com/explore/xxxxxx
```

或使用 Skill 命令：

```
/myriad-mind https://www.bilibili.com/video/BVxxxxxxxxxx/
```

### 文章

提供文章链接：

```
帮我总结这篇知乎：https://zhuanlan.zhihu.com/p/xxxxx
```

```
/myriad-mind https://blog.csdn.net/xxx/article/details/xxxxx
```

### 本地文件

直接提供文件路径：

```
请帮我提取字幕并总结：~/Downloads/lecture.mp4
```

```
/myriad-mind ~/Desktop/recording.mp3
```

> 本地文件模式无需 AI Douyin API Key，自动跳过视频下载步骤。

### 查看历史任务

```
查看我的 AI Douyin 历史任务
```

---

## ⚙️ 配置说明

### 字幕后端

| 后端 | 环境变量值 | 说明 | 费用 |
|------|-----------|------|------|
| faster-whisper（默认） | `ASR_BACKEND=faster-whisper` | 本地 ASR，支持 GPU 加速 | 免费 |
| 火山引擎 VC | `ASR_BACKEND=volcengine` | 云端 ASR | 按量付费 |

### 视频解析代理

| 代理 | 环境变量值 | 适用平台 | 费用 |
|------|-----------|---------|------|
| AI Douyin（推荐） | `VIDEO_INFO_PROVIDER=ai-douyin` | 抖音/小红书/B站 | 免费额度，解析扣 1 积分 |
| TikHub | `VIDEO_INFO_PROVIDER=tikhub` | 抖音/小红书/B站 | 按 TikHub 套餐 |
| 无需代理 | — | YouTube | 免费（yt-dlp 直接抓字幕） |

### 关键帧截图参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `KF_INTERVAL` | 30 | 每隔多少秒截一张图 |
| `KF_MAX_FRAMES` | 50 | 最多截取多少张 |
| `KF_MODE` | interval | `interval`（固定间隔）/ `scene`（场景变化检测）/ `both`（两种都截） |

### faster-whisper 模型选择

| 模型 | 显存需求 | 速度 | 准确度 |
|------|---------|------|--------|
| tiny | ~1 GB | 最快 | 一般 |
| base | ~1 GB | 快 | 较好 |
| **small（推荐）** | ~2 GB | 适中 | 好 |
| medium | ~5 GB | 较慢 | 很好 |
| large-v2 | ~10 GB | 最慢 | 最好 |

---

## 🔧 高级配置

### 使用 TikHub 替代 AI Douyin

如果你已有 TikHub Token，可以在 `.env` 中切换：

```bash
VIDEO_INFO_PROVIDER=tikhub
TIKHUB_TOKEN=your_tikhub_token
```

### 使用火山引擎 ASR

详见 [docs/bytedance-vc-setup.md](./docs/bytedance-vc-setup.md)。

### 指定 Python 路径

如果你有独立 venv 安装了 faster-whisper：

```bash
FW_PYTHON=/path/to/your/venv/bin/python
```

---

## 📁 项目结构

```text
myriad-mind/
├── README.md                          # 本文件
├── SKILL.md                           # Skill 定义（Claude Code 读取）
├── .env.example                       # 环境变量模板
├── LICENSE                            # MIT 协议
├── scripts/
│   ├── extract_keyframes.py           # 关键帧截图脚本
│   ├── download_video_candidates.py   # 视频下载（支持多候选 URL）
│   ├── download_youtube_subtitles.py  # YouTube 字幕抓取
│   ├── install_faster_whisper.py      # faster-whisper 安装助手
│   ├── list_ai_douyin_tasks.py        # AI Douyin 历史任务查询
│   └── transcribe_faster_whisper.py   # faster-whisper 转写
├── tests/                             # 单元测试
└── docs/                              # 配置教程
    ├── ai-douyin-setup.md
    ├── tikhub-setup.md
    ├── faster-whisper-setup.md
    └── bytedance-vc-setup.md
```

---

## 💰 费用说明

| 服务 | 费用 |
|------|------|
| AI Douyin 代理 | 新用户免费额度；解析扣 1 积分/次 |
| TikHub API（可选） | 按 TikHub 套餐计费 |
| YouTube 字幕抓取 | 免费（yt-dlp 本地抓取） |
| faster-whisper | 免费（本地 CPU/GPU 运行） |
| 火山引擎 VC | 仅 `ASR_BACKEND=volcengine` 时产生费用 |
| Claude Code | 取决于你的订阅计划 |

> 默认方案（faster-whisper + AI Douyin）成本极低，基本可以零费用使用。

---

## ❓ 常见问题

| 问题 | 解决方案 |
|------|---------|
| `ffmpeg not found` | 安装 FFmpeg 并确保在 PATH 中：`brew install ffmpeg` / `winget install Gyan.FFmpeg` |
| `yt-dlp not found` | `pip install -U yt-dlp` |
| `faster-whisper` 导入失败 | 运行 `python3 scripts/install_faster_whisper.py` |
| AI Douyin 返回 402 | 免费额度用完，到 [ai-douyin.top9.cc](https://ai-douyin.top9.cc) 充值或切换 TikHub |
| AI Douyin 返回 401 | API Key 无效，检查 `.env` 中的 `AI_DOUYIN_API_KEY` |
| 首次运行很慢 | faster-whisper 首次下载模型文件，后续会使用缓存 |
| CUDA 不可用 | `FW_DEVICE=auto` 会自动回退到 CPU，不影响使用 |
| Windows 下 ffmpeg 路径问题 | 脚本会自动搜索 `WinGet\Packages` 目录 |

---

## 📄 License

[MIT](./LICENSE)

## 🙏 致谢

- 上游项目：[imlewc/myriad-mind-skill](https://github.com/imlewc/myriad-mind-skill)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — 高效本地 ASR
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 强大的视频下载工具
- [FFmpeg](https://ffmpeg.org/) — 音视频处理基石
