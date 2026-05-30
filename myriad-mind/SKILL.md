---
name: myriad-mind
description: 大衍决 — 神识一扫，万物皆可为笔记。丢入视频链接、文章 URL、本地文件或整个目录，自动炼化为结构化学习笔记（AI 摘要 + Mermaid 图表 + 术语表 + 扩展资源 + 评论区精华）。英译中、关键帧截图、阅读时长/难度/可靠性评级，一炉出丹。Trigger on video URLs (bilibili, YouTube, douyin, xiaohongshu), article URLs (zhihu, CSDN, juejin, wiki, weixin), local files (.mp4/.mp3/.wav/.md/.txt), directories, or AI Douyin task history.
args: <url_or_path> - 视频链接/文章链接/GitHub仓库/本地文件/本地目录（必需）
---

# 大衍决 (Myriad Mind) — 内容学习笔记技能

## Overview

将视频（抖音、小红书、B 站、YouTube 等）、文章（知乎、CSDN、Wiki 等）或本地视频/音频文件转化为 AI 摘要 + 结构化学习笔记。英文内容会自动翻译为中文。视频额外支持关键帧截图和评论区精华提取。

**核心流程：**
- **在线视频：** 获取视频信息 → 下载/抓字幕 → ASR → 截关键帧 → AI 总结 → 翻译 → 生成笔记
- **在线文章：** 抓取文章内容 → AI 总结 → 翻译（如需）→ 生成笔记
- **本地文件：** 提取音频 → ASR → 截关键帧 → AI 总结 → 翻译 → 生成笔记
- **代码项目：** 扫描结构 → 灵力估算 → 关键文件 → 架构分析 → Mermaid 图 → 阅读指南

默认使用本地 `faster-whisper`，也支持通过环境变量切换到火山引擎 VC API。
YouTube 优先使用 `yt-dlp` 直接抓取人工字幕或自动字幕；只有没有可用字幕时，才需要下载音视频并回退到 ASR。

## When to Use

- 用户提供**视频链接**（抖音、小红书、B 站、YouTube 等），要求提取字幕或生成总结
- 用户提供**文章链接**（知乎、CSDN、掘金、Wiki、公众号等），要求总结或生成学习笔记
- 用户提供本地视频/音频文件路径，要求转字幕或生成总结
- 用户要求查看自己的 AI Douyin 历史任务、最近任务、任务列表
- 用户希望学习一个内容：提取文本、截图关键内容（视频）、生成学习笔记
- 内容为英文时，自动翻译为中文并保留中英对照

**不适用于：** 实时语音识别、直播字幕

## 外部依赖

| 依赖 | 用途 | 必需 |
| --- | --- | --- |
| **AI Douyin API Key** | 推荐的视频解析/下载代理；注册后可用免费额度，成功解析下载直链后扣 1 积分 | 仅抖音/小红书/B 站需要 |
| **TikHub API** | 可选高级/自托管方案：使用自己的 TikHub Token 直接解析 | 可选 |
| **Python 3.9+** | 运行 `faster-whisper` helper | 仅 `ASR_BACKEND=faster-whisper` 时需要 |
| **faster-whisper** | 本地语音转文字 | 仅 `ASR_BACKEND=faster-whisper` 时需要 |
| **字节跳动 VC API** | 云端语音转文字 | 仅 `ASR_BACKEND=volcengine` 时需要 |
| **FFmpeg** | 从视频提取音频 | ✅（音频文件可跳过） |
| **yt-dlp** | 下载 B 站视频；抓取 YouTube 字幕 | 仅 B 站或 YouTube 需要 |
| **jq** | 解析 AI Douyin/TikHub JSON 响应 | 在线视频模式需要 |

## 环境变量

通过环境变量读取，支持以下任意方式配置：

**方式一：.env 文件（推荐）** — 在 skill 目录下创建 `.env` 文件：

```bash
ASR_BACKEND="faster-whisper"
VIDEO_INFO_PROVIDER="ai-douyin"
AI_DOUYIN_API_BASE="https://ai-douyin.top9.cc"
AI_DOUYIN_API_KEY="your_ai_douyin_api_key"
TIKHUB_TOKEN=""

FW_MODEL_SIZE="small"
FW_DEVICE="auto"
FW_COMPUTE_TYPE=""
FW_PYTHON=""

BYTEDANCE_VC_TOKEN="your_token"
BYTEDANCE_VC_APPID="your_appid"

CLEANUP_TEMP="true"

NOTE_METADATA="true"
NOTE_OUTPUT_DIR=""

# 功能开关（全部默认开启，设为 false 关闭对应功能）
ENABLE_KEYFRAMES="true"
ENABLE_MERMAID="true"
ENABLE_RESOURCES="true"
ENABLE_COMMENTS="true"
ENABLE_READING_INFO="true"

ENABLE_ESTIMATION="true"

DEBUG_METADATA="false"

# 收尾 / Post-processing
AUTO_UPDATE_PANEL="true"
AUTO_SUGGEST_NEXT="true"
```

**方式二：Shell 配置** — 添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export ASR_BACKEND="faster-whisper"
export VIDEO_INFO_PROVIDER="ai-douyin"
export AI_DOUYIN_API_BASE="https://ai-douyin.top9.cc"
export AI_DOUYIN_API_KEY="your_ai_douyin_api_key"
export TIKHUB_TOKEN=""

export FW_MODEL_SIZE="small"
export FW_DEVICE="auto"
export FW_COMPUTE_TYPE=""
export FW_PYTHON=""

export BYTEDANCE_VC_TOKEN="your_token"
export BYTEDANCE_VC_APPID="your_appid"

export CLEANUP_TEMP="true"

export NOTE_METADATA="true"
export NOTE_OUTPUT_DIR=""

# 功能开关（全部默认开启，设为 false 关闭对应功能）
export ENABLE_KEYFRAMES="true"
export ENABLE_MERMAID="true"
export ENABLE_RESOURCES="true"
export ENABLE_COMMENTS="true"
export ENABLE_READING_INFO="true"

export ENABLE_ESTIMATION="true"

export DEBUG_METADATA="false"

# 收尾 / Post-processing
export AUTO_UPDATE_PANEL="true"
export AUTO_SUGGEST_NEXT="true"
```

说明：
- `ASR_BACKEND`：可选，默认 `faster-whisper`
- `VIDEO_INFO_PROVIDER`：可选，默认 `ai-douyin`；可改为 `tikhub` 使用自有 TikHub Token
- `AI_DOUYIN_API_BASE` / `AI_DOUYIN_API_KEY`：推荐的视频解析代理；抖音/小红书/B 站需要；YouTube 不需要
- `TIKHUB_TOKEN`：可选高级/自托管方案；当 `VIDEO_INFO_PROVIDER=tikhub` 时需要
- `FW_MODEL_SIZE` / `FW_DEVICE` / `FW_COMPUTE_TYPE`：仅 `faster-whisper` 后端使用
- `FW_PYTHON`：可选，指定安装了 `faster-whisper` 的 Python；留空时优先使用安装 helper 创建的默认 venv，再回退系统 `python3`
- `BYTEDANCE_VC_TOKEN` / `BYTEDANCE_VC_APPID`：仅 `volcengine` 后端使用
- `CLEANUP_TEMP`：可选，默认 `true`。流程完成后自动清理 `/tmp/video_analysis/{VIDEO_ID}/` 临时文件（视频、音频、字幕、截图）。设为 `false` 保留文件用于调试
- `NOTE_METADATA`：可选，默认 `true`。在文档末尾附加生成元信息（生成时间、模型、Token 消耗等）。设为 `false` 不输出
- `NOTE_OUTPUT_DIR`：可选，默认为空。学习笔记输出目录。留空则输出到当前工作目录（`pwd`）下；设值则输出到指定路径。支持绝对路径（`D:/Notes`）或相对路径（`./大衍决残卷`）。示例：`NOTE_OUTPUT_DIR="D:/Project/MyClaude/大衍决残卷"`

**功能开关（全部默认 `true`，可按需关闭）：**

| 配置项 | 控制功能 | 关闭后效果 |
| --- | --- | --- |
| `ENABLE_KEYFRAMES` | 步骤 3.5 截图提取 + 步骤 7 截图嵌入 | 跳过截图提取，笔记纯文字 + Mermaid |
| `ENABLE_MERMAID` | 步骤 7 笔记中 Mermaid 图表绘制 | 不生成 Mermaid 图表，纯文字描述 |
| `ENABLE_RESOURCES` | 步骤 7 扩展学习资源推荐 | 笔记不包含"扩展学习资源"章节 |
| `ENABLE_COMMENTS` | 步骤 7.2 评论区精华提取 | 跳过评论获取，笔记不包含"评论区精华" |
| `ENABLE_READING_INFO` | 步骤 7 阅读时长 / 难度 / 可靠性评级 | 笔记不显示阅读信息和评级行 |
| `CLEANUP_TEMP` | 步骤 8 自动清理临时文件 | 保留 /tmp/video_analysis/ 中间产物 |
| `ENABLE_ESTIMATION` | 步骤 0.7 处理前灵力预估 + 确认 | 跳过预估直接处理 |
| `AUTO_UPDATE_PANEL` | 笔记生成后自动更新修为面板 | 不自动更新 |
| `AUTO_SUGGEST_NEXT` | 工作结束后提供学习路线推荐 | 不提示 |
| `DEBUG_METADATA` | 元信息中附加调试信息（工具调用/决策链路） | 仅基础元信息（默认 false） |
| `NOTE_METADATA` | 笔记末尾生成元信息页脚 | 不输出文档元信息 |

> 安装与运行时说明见 [AI Douyin 配置指南](./docs/ai-douyin-setup.md)、[TikHub 申请指南](./docs/tikhub-setup.md)、[faster-whisper 安装指南](./docs/faster-whisper-setup.md) 和 [火山引擎开通指南](./docs/bytedance-vc-setup.md)

## 执行步骤

### 步骤 0：判断输入类型

根据用户输入判断处理模式：

- **在线视频模式**：输入为 URL
  - **抖音/TikTok**：`douyin.com`、`v.douyin.com`、`tiktok.com`
  - **小红书**：`xiaohongshu.com`、`xhslink.com`
  - **B 站**：`bilibili.com`、`b23.tv`
  - **YouTube**：`youtube.com`、`youtu.be`
- **在线文章模式**：输入为文章/文档 URL → 跳转到 [文章学习模式](#文章学习模式)
  - **知乎**：`zhuanlan.zhihu.com`、`zhihu.com/question/`、`zhihu.com/answer/`
  - **CSDN**：`blog.csdn.net`、`csdn.net`
  - **掘金**：`juejin.cn/post/`、`juejin.im/post/`
  - **简书**：`jianshu.com/p/`
  - **微信公众号**：`mp.weixin.qq.com/s/`
  - **Wiki/百科**：`wikipedia.org`、`wiki.` 开头域名
  - **通用博客/技术文档**：URL 路径看起来是文章（如 `/blog/`、`/post/`、`/article/`、`/docs/`）
  - **不确定时**：先用 WebFetch 试探抓取，如果返回的是文章内容而非视频页面，按文章模式处理
- **本地文件模式**：输入为本地文件路径
  - 本地**视频**文件（`.mp4`、`.mov`、`.avi`、`.mkv` 等）→ 从步骤 3（提取音频）开始
  - 本地**音频**文件（`.mp3`、`.wav`、`.m4a`、`.flac` 等）→ 跳过步骤 3，直接从步骤 4（转写）开始
  - 本地**文档**文件（`.md`、`.txt`、`.pdf`、`.rst` 等）→ 直接读取内容，按 [本地文档模式](#本地文档模式) 处理
- **本地目录模式**：输入为本地目录路径
  - 扫描目录下所有支持的文件（`.md`/`.mp4`/`.mp3`/`.wav`/`.mov`/`.txt`/`.pdf` 等，递归最多 2 层）
  - 每个文件按对应模式处理（视频→视频流程，文档→文档流程）
  - 生成**一份合并的学习笔记**，按文件分段，标注每个文件的原始路径
  - 目录下 `.md` 文件可能是已有的学习笔记，读取后可提炼/合并/补充
- **代码项目模式**：输入为代码目录或 GitHub 仓库 URL → 跳转到 [代码项目分析模式](#代码项目分析模式)
  - **GitHub URL**：`github.com/{owner}/{repo}` 或 `github.com/{owner}/{repo}/tree/{branch}`
  - **本地代码目录**：目录中主要是代码文件（`.py`/`.js`/`.ts`/`.rs`/`.go`/`.java`/`.c`/`.cpp`/`.h` 等），而非 `.md`/`.mp4` 等学习资料
  - 判定逻辑：如果目录中代码文件占比 > 50%，按代码项目处理，而非本地目录模式
- **搜索模式**：输入含 `search` / `搜索` / `找一下` / `有没有` 等关键词 → 跳转到 [搜索模式](#搜索模式)
  - 触发词：`/myriad-mind search 关键词`、`搜索笔记`、`找一下XXX`、`有没有关于XXX的笔记`
- **对比模式**：用户输入包含 `compare` / `对比` / `比较` 等关键词 → 跳转到 [对比模式](#对比模式)
  - 触发词：`/myriad-mind compare A B`、`对比一下`、`比较这两篇`、`哪个讲得好`
- **修为面板模式**：用户输入为修为面板相关关键词 → 跳转到 [修为面板模式](#修为面板模式)
  - 触发词：`修为面板`、`知识图谱`、`学习地图`、`我的知识`、`学习总结`、`knowledge map`、`修炼等级`

### 步骤 0.5：读取后端配置

先读取 `ASR_BACKEND`，未配置时默认使用 `faster-whisper`：

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
ENV_FILE="$SKILL_DIR/.env"

read_env() {
  local key="$1"
  if [ -f "$ENV_FILE" ]; then
    grep "^${key}=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'"
  else
    printenv "$key"
  fi
}

ASR_BACKEND="$(read_env ASR_BACKEND)"
[ -z "$ASR_BACKEND" ] && ASR_BACKEND="faster-whisper"

echo "ASR_BACKEND=$ASR_BACKEND"
```

支持值：
- `faster-whisper`
- `volcengine`

### 步骤 0.6：环境检查（必须首先执行）

在开始任何处理之前，先检查当前模式和当前字幕后端需要的依赖。

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
ENV_FILE="$SKILL_DIR/.env"

read_env() {
  local key="$1"
  if [ -f "$ENV_FILE" ]; then
    grep "^${key}=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'"
  else
    printenv "$key"
  fi
}

ASR_BACKEND="$(read_env ASR_BACKEND)"
[ -z "$ASR_BACKEND" ] && ASR_BACKEND="faster-whisper"
VIDEO_INFO_PROVIDER="$(read_env VIDEO_INFO_PROVIDER)"
[ -z "$VIDEO_INFO_PROVIDER" ] && VIDEO_INFO_PROVIDER="ai-douyin"
AI_DOUYIN_API_BASE="$(read_env AI_DOUYIN_API_BASE)"
[ -z "$AI_DOUYIN_API_BASE" ] && AI_DOUYIN_API_BASE="https://ai-douyin.top9.cc"
AI_DOUYIN_API_KEY="$(read_env AI_DOUYIN_API_KEY)"
TIKHUB_TOKEN="$(read_env TIKHUB_TOKEN)"
BYTEDANCE_VC_TOKEN="$(read_env BYTEDANCE_VC_TOKEN)"
BYTEDANCE_VC_APPID="$(read_env BYTEDANCE_VC_APPID)"
FW_PYTHON="$(read_env FW_PYTHON)"
[ -z "$FW_PYTHON" ] && [ -x "$HOME/.cache/myriad-mind/faster-whisper-venv/bin/python" ] && FW_PYTHON="$HOME/.cache/myriad-mind/faster-whisper-venv/bin/python"
[ -z "$FW_PYTHON" ] && FW_PYTHON="python3"

MISSING=""

if [ "{INPUT_MODE}" = "url" ]; then
  if [ "{PLATFORM}" = "douyin" ] || [ "{PLATFORM}" = "xiaohongshu" ] || [ "{PLATFORM}" = "bilibili" ]; then
    if [ "$VIDEO_INFO_PROVIDER" = "ai-douyin" ]; then
      [ -z "$AI_DOUYIN_API_KEY" ] && MISSING="$MISSING AI_DOUYIN_API_KEY"
    elif [ "$VIDEO_INFO_PROVIDER" = "tikhub" ]; then
      [ -z "$TIKHUB_TOKEN" ] && MISSING="$MISSING TIKHUB_TOKEN"
    else
      MISSING="$MISSING invalid_VIDEO_INFO_PROVIDER"
    fi
  fi
  if [ "$VIDEO_INFO_PROVIDER" = "ai-douyin" ] || [ "$VIDEO_INFO_PROVIDER" = "tikhub" ]; then
    command -v jq >/dev/null 2>&1 || MISSING="$MISSING jq"
  fi
  if [ "{PLATFORM}" = "bilibili" ] || [ "{PLATFORM}" = "youtube" ]; then
    command -v yt-dlp >/dev/null 2>&1 || MISSING="$MISSING yt-dlp"
  fi
fi

if [ "{NEEDS_FFMPEG}" = "yes" ] && [ "{PLATFORM}" != "youtube" ]; then
  command -v ffmpeg >/dev/null 2>&1 || MISSING="$MISSING ffmpeg"
fi

if [ "$ASR_BACKEND" = "faster-whisper" ]; then
  command -v "$FW_PYTHON" >/dev/null 2>&1 || [ -x "$FW_PYTHON" ] || MISSING="$MISSING FW_PYTHON"
  "$FW_PYTHON" - <<'PY' >/dev/null 2>&1 || MISSING="$MISSING faster-whisper"
import faster_whisper
import ctranslate2
PY
elif [ "$ASR_BACKEND" = "volcengine" ]; then
  [ -z "$BYTEDANCE_VC_TOKEN" ] && MISSING="$MISSING BYTEDANCE_VC_TOKEN"
  [ -z "$BYTEDANCE_VC_APPID" ] && MISSING="$MISSING BYTEDANCE_VC_APPID"
else
  MISSING="$MISSING invalid_ASR_BACKEND"
fi

if [ -n "$MISSING" ]; then
  echo "ERROR: 缺少必需依赖或配置:$MISSING"
  echo "ASR_BACKEND=$ASR_BACKEND VIDEO_INFO_PROVIDER=$VIDEO_INFO_PROVIDER"
  echo "ASR_BACKEND 可选值: faster-whisper / volcengine"
  echo "VIDEO_INFO_PROVIDER 可选值: ai-douyin / tikhub"
  exit 1
else
  echo "OK: 运行依赖已就绪 (ASR_BACKEND=$ASR_BACKEND)"
fi
```

如果检查失败：
- `ASR_BACKEND=faster-whisper`：优先运行 `python3 "$SKILL_DIR/scripts/install_faster_whisper.py"`，或参考 [docs/faster-whisper-setup.md](./docs/faster-whisper-setup.md)
- `ASR_BACKEND=volcengine`：参考 [docs/bytedance-vc-setup.md](./docs/bytedance-vc-setup.md)
- `AI_DOUYIN_API_KEY`：注册 [AI Douyin](https://ai-douyin.top9.cc) 领取免费额度并创建 API Key；余额不足时充值积分，或改用 `VIDEO_INFO_PROVIDER=tikhub` + `TIKHUB_TOKEN`

### 步骤 0.7：灵力预估（所有模式通用 — 必须在处理前执行）

在开始任何实际处理之前，先根据输入估算资源消耗并征求用户确认。

#### 估算规则

| 输入类型 | 时间估算 | Token 估算 | 说明 |
| --- | --- | --- | --- |
| 🎬 视频 < 10 分钟 | ~3 分钟 | 20,000-40,000 | 短小视频，直接处理 |
| 🎬 视频 10-30 分钟 | ~6 分钟 | 30,000-60,000 | 中等视频 |
| 🎬 视频 30-60 分钟 | ~10 分钟 | 50,000-80,000 | 较长，建议确认 |
| 🎬 视频 > 60 分钟 | ~15 分钟 | 80,000-150,000 | 很长，**必须确认** |
| 📄 文章 < 5,000 字 | ~1 分钟 | 10,000-20,000 | 短文，直接处理 |
| 📄 文章 5,000-15,000 字 | ~2 分钟 | 20,000-40,000 | 中等文章 |
| 📄 文章 > 15,000 字 | ~4 分钟 | 40,000-80,000 | 长文 |
| 📂 目录（N 个文件） | ~N × 3 分钟 | N × 30,000 | 每个文件单独估算 |
| 💻 代码项目 | 见 CODE2 | 见 CODE2 | 已有灵力评估 |
| 🗺️ 修为面板 | ~2 分钟 | 15,000-25,000 | 扫描已有笔记 |

**额外消耗因素：**
- 需要 ASR 转写：+ 视频时长 × 0.5（faster-whisper CPU 模式约为视频时长的 30-50%）
- 需要下载视频：+ 1-3 分钟（取决于网速和视频大小）
- 需要提取关键帧：+ 30 秒
- 英文内容需翻译：+ Token × 1.3
- 启用评论区：+ 5,000-10,000 tokens

#### 确认阈值

| 预估 Token | 行为 |
| --- | --- |
| < 30,000 | 🟢 直接执行，无需确认（仅告知预估） |
| 30,000-80,000 | 🟡 提示预估后直接执行 |
| > 80,000 | 🔴 **必须用户确认后才执行** |

#### 确认提示模板

```text
🔮 灵力预估

| 项目 | 估算 |
| --- | --- |
| 输入类型 | {视频/文章/目录/代码} |
| 预估耗时 | 约 X 分钟 |
| 预估 Token | 约 XX,000 tokens |
| 主要消耗 | {ASR 转写 / 长篇字幕 / 多文件扫描 / ...} |
| 启用功能 | {截图/Mermaid/资源推荐/评论区/...} |

是否继续？回复"确认"或提出修改（如"跳过评论区""只看核心模块"）。
```

#### 快速调整选项

如果用户觉得消耗太高，提供快速缩减方案：
- **省流模式**：`ENABLE_KEYFRAMES=false ENABLE_COMMENTS=false` → 省 30-40%
- **速览模式**：只生成摘要 + 核心概念 + 术语表，跳过详细笔记 → 省 60-70%
- **自定义**：用户指定要关闭的功能

### 步骤 1：获取视频信息/下载直链（仅在线视频模式）

根据 URL 域名识别平台：

| 平台 | URL 特征 | 默认处理方式 |
| --- | --- | --- |
| 抖音/TikTok | `douyin.com`、`v.douyin.com`、`tiktok.com` | `AI Douyin` 代理解析下载直链；可选 TikHub |
| 小红书 | `xiaohongshu.com`、`xhslink.com` | `AI Douyin` 代理解析下载直链；可选 TikHub |
| B 站 | `bilibili.com`、`b23.tv` | `AI Douyin` 代理解析下载直链；必要时可回退 `yt-dlp` |
| YouTube | `youtube.com`、`youtu.be` | 不调用 AI Douyin/TikHub，直接进入步骤 2 抓字幕 |

#### 默认推荐：AI Douyin 代理

AI Douyin 适合不想单独注册 TikHub 的用户。注册 [https://ai-douyin.top9.cc](https://ai-douyin.top9.cc) 后领取免费额度并创建 API Key，成功解析下载直链后扣 1 积分；失败不扣。余额不足时接口返回 HTTP `402` / `insufficient balance`。

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
ENV_FILE="$SKILL_DIR/.env"
read_env() {
  local key="$1"
  if [ -f "$ENV_FILE" ]; then
    grep "^${key}=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'"
  else
    printenv "$key"
  fi
}

AI_DOUYIN_API_BASE="$(read_env AI_DOUYIN_API_BASE)"
[ -z "$AI_DOUYIN_API_BASE" ] && AI_DOUYIN_API_BASE="https://ai-douyin.top9.cc"
AI_DOUYIN_API_KEY="$(read_env AI_DOUYIN_API_KEY)"

# API Base 支持填 https://ai-douyin.top9.cc 或 https://ai-douyin.top9.cc/api/v1
case "$AI_DOUYIN_API_BASE" in
  */api/v1) AI_DOUYIN_DOWNLOAD_URL_ENDPOINT="$AI_DOUYIN_API_BASE/video/download-url" ;;
  */api) AI_DOUYIN_DOWNLOAD_URL_ENDPOINT="$AI_DOUYIN_API_BASE/v1/video/download-url" ;;
  *) AI_DOUYIN_DOWNLOAD_URL_ENDPOINT="${AI_DOUYIN_API_BASE%/}/api/v1/video/download-url" ;;
esac

curl -sS -w '\n%{http_code}' -X POST "$AI_DOUYIN_DOWNLOAD_URL_ENDPOINT" \
  -H "X-API-Key: $AI_DOUYIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg url "{ORIGINAL_URL}" '{url: $url}')" \
  > /tmp/video_analysis/download_url_response.txt

HTTP_CODE=$(tail -n1 /tmp/video_analysis/download_url_response.txt)
sed '$d' /tmp/video_analysis/download_url_response.txt > /tmp/video_analysis/download_url.json

if [ "$HTTP_CODE" = "402" ]; then
  echo "ERROR: AI Douyin 余额不足（insufficient balance）。请到 https://ai-douyin.top9.cc 购买积分，或改用 VIDEO_INFO_PROVIDER=tikhub + TIKHUB_TOKEN。"
  exit 1
elif [ "$HTTP_CODE" = "401" ]; then
  echo "ERROR: AI Douyin API Key 缺失或无效。请检查 AI_DOUYIN_API_KEY。"
  exit 1
elif [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
  echo "ERROR: AI Douyin 解析失败 (HTTP $HTTP_CODE)"
  cat /tmp/video_analysis/download_url.json
  exit 1
fi

VIDEO_URL=$(jq -r '.download_url // empty' /tmp/video_analysis/download_url.json)
VIDEO_URL_COUNT=$(jq -r '(.download_urls // [.download_url] | map(select(. != null and . != "")) | length)' /tmp/video_analysis/download_url.json)
EXTRACTED_URL=$(jq -r '.extracted_url // empty' /tmp/video_analysis/download_url.json)
DOWNLOAD_COST=$(jq -r '.cost // 1' /tmp/video_analysis/download_url.json)
[ -z "$VIDEO_URL" ] && echo "ERROR: 未返回 download_url" && cat /tmp/video_analysis/download_url.json && exit 1
```

提取关键字段：

```bash
jq '{download_url, download_urls_count: (.download_urls // [] | length), extracted_url, cost}' /tmp/video_analysis/download_url.json
```

#### 可选视频接口获取方案：自有 TikHub Token

当 `VIDEO_INFO_PROVIDER=tikhub` 时，使用自己的 TikHub Token 直接解析。注意不要把真实 Token 写入日志或回复。

**抖音/TikTok：**

```bash
curl -s -X GET "https://api.tikhub.io/api/v1/hybrid/video_data?url={ENCODED_URL}&minimal=true" \
  -H "Authorization: Bearer your_tikhub_api_token" \
  -H "Accept: application/json"
```

优先提取无水印地址：

```bash
jq -r '.data.video_data.nwm_video_url // .data.video.play_addr.url_list[0] // empty'
```

**小红书：**

```bash
curl -s -X GET "https://api.tikhub.io/api/v1/xiaohongshu/web/get_note_info_v7?share_text={ENCODED_URL}" \
  -H "Authorization: Bearer your_tikhub_api_token" \
  -H "Accept: application/json"
```

**B 站：**

```bash
curl -s -X GET "https://api.tikhub.io/api/v1/bilibili/web/fetch_one_video_v3?url={ENCODED_URL}" \
  -H "Authorization: Bearer your_tikhub_api_token" \
  -H "Accept: application/json"
```

> B 站如未获得可下载直链，可在步骤 2 中使用 `yt-dlp` 下载。

### 步骤 1.5：查询用户自己的 AI Douyin 历史任务（按需）

当用户要求查看自己的历史 task / 最近任务 / 任务列表时，调用 AI Douyin 的 `GET /api/v1/tasks`。该接口使用 `X-API-Key` 认证，只返回当前 API Key 对应用户自己的任务。

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"

python3 "$SKILL_DIR/scripts/list_ai_douyin_tasks.py" \
  --page 1 \
  --page-size 20
```

可选筛选：

```bash
python3 "$SKILL_DIR/scripts/list_ai_douyin_tasks.py" --status completed --page 1 --page-size 10
python3 "$SKILL_DIR/scripts/list_ai_douyin_tasks.py" --search "关键词" --json
```

脚本默认读取 `$SKILL_DIR/.env` 或环境变量中的 `AI_DOUYIN_API_BASE` / `AI_DOUYIN_API_KEY`。输出给用户时不要展示真实 API Key。

### 步骤 2：下载视频（仅在线视频模式）

根据平台使用不同的下载方式：

**YouTube（优先直接抓字幕，不下载视频）：**

```bash
mkdir -p /tmp/video_analysis/{VIDEO_ID}
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
python3 "$SKILL_DIR/scripts/download_youtube_subtitles.py" \
  "https://www.youtube.com/watch?v={VIDEO_ID}" \
  --output-dir /tmp/video_analysis/{VIDEO_ID} \
  --languages zh-Hans,zh-Hant,zh,en
```

输出文件固定为：
- `/tmp/video_analysis/{VIDEO_ID}/subtitle.srt`
- `/tmp/video_analysis/{VIDEO_ID}/text.txt`

如果命令提示没有可用字幕，再使用 `yt-dlp` 下载音频或视频，并从步骤 3 继续走 `ASR_BACKEND`。

**抖音 / TikTok / 小红书 / B 站（已有 `VIDEO_URL` 下载直链时）：**

```bash
mkdir -p /tmp/video_analysis/{VIDEO_ID}
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
python3 "$SKILL_DIR/scripts/download_video_candidates.py" \
  --response-json /tmp/video_analysis/download_url.json \
  --output /tmp/video_analysis/{VIDEO_ID}/video.mp4 \
  --timeout 30
```

**B 站（没有下载直链时回退）：**

```bash
mkdir -p /tmp/video_analysis/{BVID}
yt-dlp -o /tmp/video_analysis/{BVID}/video.mp4 "https://www.bilibili.com/video/{BVID}/"
```

### 步骤 3：提取音频（本地音频文件可跳过）

> 本地文件模式下，如果输入是本地视频文件，将 `{VIDEO_ID}` 替换为文件名（不含扩展名），输入路径替换为实际视频路径。

```bash
ffmpeg -i /tmp/video_analysis/{VIDEO_ID}/video.mp4 -q:a 0 -map a -y /tmp/video_analysis/{VIDEO_ID}/audio.mp3
```

### 步骤 3.5：提取关键帧截图（学习模式）

> 仅当存在视频文件时执行。如果只有音频文件（`.mp3`、`.wav` 等），跳过此步骤。

使用 ffmpeg 按固定时间间隔截取关键帧画面，用于后续学习笔记中展示视频中的关键内容（如 PPT 幻灯片、代码截图、图表等）。

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"

# 读取截图配置
ENV_FILE="$SKILL_DIR/.env"
KF_INTERVAL="30"
KF_MAX_FRAMES="50"
KF_MODE="interval"

if [ -f "$ENV_FILE" ]; then
  _val=$(grep "^KF_INTERVAL=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  [ -n "$_val" ] && KF_INTERVAL="$_val"
  _val=$(grep "^KF_MAX_FRAMES=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  [ -n "$_val" ] && KF_MAX_FRAMES="$_val"
  _val=$(grep "^KF_MODE=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  [ -n "$_val" ] && KF_MODE="$_val"
fi

python3 "$SKILL_DIR/scripts/extract_keyframes.py" \
  --video /tmp/video_analysis/{VIDEO_ID}/video.mp4 \
  --output-dir /tmp/video_analysis/{VIDEO_ID} \
  --interval "$KF_INTERVAL" \
  --max-frames "$KF_MAX_FRAMES" \
  --mode "$KF_MODE"
```

输出文件：
- `/tmp/video_analysis/{VIDEO_ID}/frames/frame_0001_00m30s.png`
- `/tmp/video_analysis/{VIDEO_ID}/frames/frame_0002_01m00s.png`
- ...
- `/tmp/video_analysis/{VIDEO_ID}/frames/keyframes.json` — 截图索引文件

**如果 ffmpeg 找不到**：Windows 下尝试检查 `C:\Users\{USER}\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe`；macOS: `brew install ffmpeg`；Linux: `sudo apt install ffmpeg`。

### 步骤 4：根据 `ASR_BACKEND` 选择字幕后端

如果平台是 YouTube 且步骤 2 已成功生成 `subtitle.srt` 和 `text.txt`，跳过本步骤，直接进入步骤 5 总结。

#### 方案 A：`ASR_BACKEND=faster-whisper`（默认）

helper 路径：

```bash
$SKILL_DIR/scripts/transcribe_faster_whisper.py
```

执行命令：

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
FW_PYTHON="${FW_PYTHON:-$HOME/.cache/myriad-mind/faster-whisper-venv/bin/python}"
[ -x "$FW_PYTHON" ] || FW_PYTHON="python3"
"$FW_PYTHON" "$SKILL_DIR/scripts/transcribe_faster_whisper.py" \
  /tmp/video_analysis/{VIDEO_ID}/audio.mp3 \
  --output-dir /tmp/video_analysis/{VIDEO_ID}
```

说明：
- helper 会自动读取 `FW_MODEL_SIZE`、`FW_DEVICE`、`FW_COMPUTE_TYPE`
- 当 `FW_DEVICE=auto` 时，只有检测到 NVIDIA/CUDA 才会使用 `device="cuda"`
- 输出文件固定为：
  - `/tmp/video_analysis/{VIDEO_ID}/subtitle.srt`
  - `/tmp/video_analysis/{VIDEO_ID}/text.txt`

#### 方案 B：`ASR_BACKEND=volcengine`

提交任务：

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
ENV_FILE="$SKILL_DIR/.env"
if [ -f "$ENV_FILE" ]; then
  BYTEDANCE_VC_TOKEN=$(grep "^BYTEDANCE_VC_TOKEN=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  BYTEDANCE_VC_APPID=$(grep "^BYTEDANCE_VC_APPID=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
else
  BYTEDANCE_VC_TOKEN="$BYTEDANCE_VC_TOKEN"
  BYTEDANCE_VC_APPID="$BYTEDANCE_VC_APPID"
fi

curl -s -X POST "https://openspeech.bytedance.com/api/v1/vc/submit?appid=$BYTEDANCE_VC_APPID&language=zh-CN&words_per_line=20&max_lines=2" \
  -H "Content-Type: audio/mpeg" \
  -H "Authorization: Bearer;$BYTEDANCE_VC_TOKEN" \
  --data-binary @/tmp/video_analysis/{VIDEO_ID}/audio.mp3
```

轮询结果：

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.codex/skills/myriad-mind}"
[ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/myriad-mind"
ENV_FILE="$SKILL_DIR/.env"
if [ -f "$ENV_FILE" ]; then
  BYTEDANCE_VC_TOKEN=$(grep "^BYTEDANCE_VC_TOKEN=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  BYTEDANCE_VC_APPID=$(grep "^BYTEDANCE_VC_APPID=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
else
  BYTEDANCE_VC_TOKEN="$BYTEDANCE_VC_TOKEN"
  BYTEDANCE_VC_APPID="$BYTEDANCE_VC_APPID"
fi

curl -s "https://openspeech.bytedance.com/api/v1/vc/query?appid=$BYTEDANCE_VC_APPID&id={TASK_ID}" \
  -H "Authorization: Bearer;$BYTEDANCE_VC_TOKEN"
```

结果处理：

```bash
jq -r '.utterances[].text' subtitle.json | tr '\n' ' ' > /tmp/video_analysis/{VIDEO_ID}/text.txt
```

生成 SRT：

```python
import json

with open('subtitle.json', 'r') as f:
    data = json.load(f)

def ms_to_srt(ms):
    h, m, s, millis = ms//3600000, (ms%3600000)//60000, (ms%60000)//1000, ms%1000
    return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"

with open('/tmp/video_analysis/{VIDEO_ID}/subtitle.srt', 'w') as f:
    for i, u in enumerate(data['utterances'], 1):
        f.write(f"{i}\n{ms_to_srt(u['start_time'])} --> {ms_to_srt(u['end_time'])}\n{u['text']}\n\n")
```

### 步骤 5：AI 生成总结

直接由 Claude 完成，无需调用第三方总结 API。

读取 `text.txt` 后生成。

总结时应一并提供以下上下文：
- **原视频标题**：如果是在线视频，优先使用平台返回的原始标题字段
  - 抖音/TikTok：优先 `desc`
  - 小红书：优先 `title`
  - B 站：优先 `title`
- **兜底标题**：如果没有明确标题，可使用文件名或视频 ID 作为参考标识
- **字幕说明**：明确告诉 Claude，正文可能来自 YouTube 字幕、自动字幕或语音识别，可能存在同音字、断句、专有名词识别错误；在不偏离原意的前提下，可以结合原视频标题和上下文做适度修正

推荐直接使用如下提示方式：

```text
以下是一个视频的分析素材，请基于这些信息生成总结：

原视频标题：{ORIGINAL_TITLE}
来源平台：{PLATFORM}
作者：{AUTHOR}
说明：下面的正文来自平台字幕、自动字幕或语音识别，可能存在少量识别误差、断句问题或专有名词错误。请以原视频标题和上下文为参考，在不改变原意的前提下做适度修正，再完成总结。

语音识别文本：
{TEXT_CONTENT}

请输出：
1. AI生成标题：简洁概括，不超过30字；可以参考原视频标题，但不要机械照抄，必要时可根据正文纠正明显错误
2. AI摘要：提炼主要观点和关键信息，200-300字
3. 核心要点：输出3-5条结构化要点
```

如果原视频标题与正文明显冲突：
- 优先以正文主旨为准
- 保留“可能因语音识别存在误差”的判断，不要凭空补充未出现的信息

1. **标题**：简洁概括，不超过 30 字
2. **摘要**：主要观点和关键信息，200-300 字
3. **要点**：核心观点的结构化列表

### 步骤 6：语言检测与翻译

检测字幕文本的语言。如果主要内容是英文，则翻译为中文并保留中英对照。

**检测逻辑**：读取 `text.txt`，统计中文字符占比。如果中文字符占比低于 30%，判定为英文内容。

**翻译处理**：直接由 Claude 完成，无需调用第三方翻译 API。

```text
以下是一段视频的字幕文本，语言为英文。请将其翻译为中文，并保留原文对照。

翻译要求：
1. 准确传达原文含义，不要意译或添加额外内容
2. 保留技术术语的英文原文（括号标注），如：反向传播（backpropagation）
3. 长句子可适当拆分为短句
4. 输出格式为：每段先英文原文，后中文翻译

原文：
{TEXT_CONTENT}
```

将翻译结果保存到 `/tmp/video_analysis/{VIDEO_ID}/translated_text.txt`，格式如下：

```
[EN] Original English sentence here.
[CN] 这里的中文翻译。

[EN] Another English sentence.
[CN] 另一句中文翻译。
```

如果是中文视频，跳过翻译步骤，直接进入步骤 7。

### 步骤 7：生成学习笔记

整合字幕文本、翻译（如有）、关键帧截图和 AI 摘要，生成结构化学习笔记。

> 如果步骤 3.5 生成了关键帧截图，Claude 应使用视觉能力分析每张截图的内容，将其融入笔记。

#### 步骤 7.0：时间戳可点击链接（重要）

**所有时间戳必须生成可点击的跳转链接**，方便读者直接跳转到视频对应位置。根据平台使用不同 URL 格式：

| 平台 | 时间戳链接格式 | 示例 |
| --- | --- | --- |
| **B 站** | `{原始链接}?t={总秒数}` | `https://www.bilibili.com/video/BV14UzWBLEXD/?t=180` |
| **YouTube** | `https://www.youtube.com/watch?v={VIDEO_ID}&t={总秒数}` | `https://www.youtube.com/watch?v=abc123&t=180` |
| **抖音** | 短视频无需时间戳，用原始链接即可 | `https://v.douyin.com/xxxxx/` |
| **小红书** | 短视频无需时间戳，用原始链接即可 | `https://xhslink.com/xxxxx/` |
| **本地文件** | `[HH:MM:SS](file:///绝对路径?t={总秒数})` | `[3:00](file:///D:/Videos/tutorial.mp4?t=180)` |

**转换规则：**
- SRT 时间戳格式 `HH:MM:SS,mmm` → 总秒数 = `HH*3600 + MM*60 + SS`
- 笔记中每个段落标题的时间范围，起始时间转为可点击链接，结束时间保留为纯文本
- 截图旁边的时间戳同样生成可点击链接

#### 步骤 7.1：截图选择决策规则（重要）

视频每隔 `KF_INTERVAL` 秒截一张图，通常会有几十张。**Claude 必须逐一审视每张截图**，按以下标准决定是否放入笔记。

**前置校验：截图必须和字幕交叉对照**

每张截图都带有时间戳（文件名 `frame_XXXX_HHhMMmSSs.png`），**必须先定位到字幕中对应时间段的文字内容**，再判断截图价值：

> 截图时间戳 → 查字幕 SRT 中同时间段的内容 → 判断"画面 + 字幕"组合是否有信息增量

| 字幕 + 画面组合 | 决策 | 典型场景 |
| --- | --- | --- |
| 实质性内容 + 信息画面 | ✅ **保留** | 讲代码逻辑时展示代码、讲架构时展示图表 |
| 实质性内容 + 静态人脸 | ❌ **跳过** | 讲师在讲但画面只有脸，没有辅助视觉 |
| 闲聊/过渡 + 任何画面 | ❌ **跳过** | 开场白、个人介绍、下节预告，"大家好我是XXX" |
| 无字幕时间段 + 任何画面 | ❌ **跳过** | 沉默、片尾、广告段 |
| 字幕讨论 A 话题 + 画面是 B 话题的 PPT | ❌ **跳过** | 画面和语音不同步，会产生误导 |

**画面内容决策表（通过前置校验后）：**

| 截图内容 | 决策 | 说明 |
| --- | --- | --- |
| PPT 标题页/大纲/目录 | ✅ **保留** | 帮助读者建立全局认知 |
| 代码/配置截图 | ✅ **保留** | 核心学习内容，必须配合文字说明 |
| 架构图/流程图/图表 | ✅ **保留** | 如果图表复杂则截图，简单关系优先用 Mermaid |
| 运行效果/演示画面 | ✅ **保留** | 让读者知道代码跑起来什么样 |
| 编辑器界面操作 | ✅ **保留** | 帮助读者复现操作步骤 |
| 数据表格/对比表 | ✅ **保留** | 数据密集，文字无法替代 |
| 纯黑屏/过渡动画 | ❌ **跳过** | 无信息量 |
| 静态人脸/说话画面 | ❌ **跳过** | 人像不传达技术信息 |
| 与前后截图高度相似 | ❌ **跳过** | 只保留最有代表性的一张（同一页 PPT 截了多张，只留第一张） |
| 纯文字段落（无图） | ❌ **跳过** | 文字内容已在字幕中 |
| 空桌面/无关窗口 | ❌ **跳过** | 无信息量 |
| 模糊/低质量画面 | ❌ **跳过** | 看不清不如不放 |

**截图使用规则（必须遵守）：**

1. **内嵌到对应知识点旁边**：截图放在详细笔记中对应知识点的正下方，**不要集中放在单独的"关键画面"章节**。读者看到文字描述时应该能同时看到相关画面。
2. **每张截图配时间戳链接**：截图下方用 `> 📸 [截图于 M:SS](链接?t=秒数)` 格式标注，让读者点击跳转到视频对应位置。
3. **截图和 Mermaid 互补**：截图展示视频真实画面（PPT、代码、界面），Mermaid 展示抽象逻辑关系（架构、流程、状态），两者不重复。如果视频里的架构图很简单，**只用 Mermaid 重新绘制**，不放截图。
4. **复制到目标目录**：将选中的截图复制到 `{OUTPUT_DIR}/assets/{VIDEO_ID}/`，笔记中使用相对路径引用（如 `assets/{VIDEO_ID}/frame_0005.png`）。
5. **清理未使用的截图**：复制完成后，删除 `frames/` 目录中所有未被笔记引用的截图文件，避免占用磁盘空间。

#### 步骤 7.2：提取评论区精华讨论

视频评论区经常有高质量的补充信息——作者本人的勘误、观众的实战经验、额外的资源链接。**Claude 应尝试获取评论区内容**，从中筛选有价值的讨论纳入笔记。

**获取评论：**

**B 站：**

```bash
# 从步骤 1 的 AI Douyin 响应中获取 aid（av 号）或 oid
# B 站评论 API（按热度排序，取前 30 条）
curl -s "https://api.bilibili.com/x/v2/reply/main?oid={AID}&type=1&ps=30&sort=1" \
  -H "User-Agent: Mozilla/5.0" \
  > /tmp/video_analysis/{VIDEO_ID}/comments.json

# 解析热门评论
jq -r '.data.replies[]? | "[\(.member.uname)] \(.content.message) | 👍\(.like) | 回复数:\(.rcount) | rpid:\(.rpid)"' \
  /tmp/video_analysis/{VIDEO_ID}/comments.json
```

**YouTube：**

```bash
# 使用 yt-dlp 提取评论（需要 YouTube 未屏蔽的环境）
yt-dlp --write-comments --skip-download \
  -o "/tmp/video_analysis/{VIDEO_ID}/comments" \
  "https://www.youtube.com/watch?v={VIDEO_ID}"

# 或直接 dump JSON 信息（含评论）
yt-dlp --dump-json --skip-download \
  "https://www.youtube.com/watch?v={VIDEO_ID}" \
  > /tmp/video_analysis/{VIDEO_ID}/video_info.json
```

**抖音/小红书：** 评论获取受限，跳过此步骤。

**筛选标准（精细化挑选，宁缺毋滥）：**

| 评论类型 | 决策 | 示例 |
| --- | --- | --- |
| 作者本人的勘误/补充 | ✅ **必选** | "00:15 处口误，应该是 XXX" |
| 补充技术细节/原理 | ✅ **优先** | "这里用 XXX 是因为底层...（详见链接）" |
| 观众的高质量提问 + 回答 | ✅ **优先** | "为什么要 XXX 而不是 YYY？→ 因为 ZZZ" |
| 分享额外资源/链接 | ✅ **保留** | "配套代码已上传 GitHub：..." |
| 实战经验/踩坑分享 | ✅ **保留** | "实际项目中遇到 X 问题，解决方案是..." |
| 表达感谢/鼓励 | ❌ **跳过** | "讲得真好""三连了" |
| 纯提问无人回答 | ❌ **跳过** | "XXX 怎么配置？"（没有回复） |
| 无意义表情/灌水 | ❌ **跳过** | "第一""前排" |
| 内容质量低的争论 | ❌ **跳过** | 人身攻击、偏题争论 |

**输出要求：**

从评论中精选 **3-6 条**有价值的讨论，按以下格式放入笔记：

```markdown
## 七、评论区精华讨论

> 💬 以下内容精选自视频评论区，已附跳转链接，可点击查看原文上下文。

### [👤 用户名](评论跳转链接) 👍 点赞数

评论内容摘要或原文引用...

> 编辑注：这条评论补充了 XXX，值得注意。

---
```

**评论跳转链接格式：**
- **B 站**：`https://www.bilibili.com/video/{BVID}/?replyTo={rpid}#reply{rpid}`
- **YouTube**：`https://www.youtube.com/watch?v={VIDEO_ID}&lc={comment_id}`
- 只对选中的评论生成链接，不需要覆盖所有

**筛选原则：**
1. **补充价值优先**：评论能补充视频未涉及的信息 > 重复视频内容的评论
2. **宁缺毋滥**：没有高质量评论就跳过整个章节，不要硬凑
3. **尊重隐私**：引用时只写用户名，不泄露头像等个人信息
4. **保持中立**：即使评论观点与视频相左，只要有理有据就纳入

#### 步骤 7.3：知识关系图（ENABLE_MERMAID=true 时生成）

每篇笔记末尾应有一张 **知识关系图**，用 Mermaid 呈现本课核心概念的关联结构。

**图：本课知识关系图**

格式要求：
- 中心节点为视频/文章主题（用 🎯 emoji 标记）
- 一级分支为核心概念（3-5 个）
- 二级分支为每个概念下的关键知识点
- 虚线连接相关概念（跨分支关系）
- 标注前置知识（📥）和后续扩展方向（📤）

```mermaid
graph TD
    CENTER[🎯 本课主题] --> C1[核心概念1]
    CENTER --> C2[核心概念2]
    CENTER --> C3[核心概念3]
    C1 --> C1A[关键知识点A]
    C1 --> C1B[关键知识点B]
    C2 --> C2A[关键知识点C]
    C2 --> C2B[关键知识点D]
    C3 --> C3A[关键知识点E]
    C1B -.->|关联| C2A
    C3A -.->|关联| C1A
    PRE[📥 前置: 需要了解XXX] -.-> CENTER
    CENTER -.-> NEXT[📤 下一步: 可以学习YYY]
```

**放在笔记中的位置：** 总结与思考之后、扩展学习资源之前（作为"五.5"或独立为"八"）。

#### 步骤 7.4：教程操作模式（自动检测）

当视频是**操作型教程**（如 UE 蓝图连线、软件配置、环境搭建、工具使用等"一步步带着做"的内容）时，额外生成操作流程可视化。

**自动检测标准：**

| 信号 | 说明 |
| --- | --- |
| 标题含教程关键词 | `教程`、`入门`、`实战`、`配置`、`搭建`、`上手`、`tutorial`、`how to`、`step by step` |
| 内容特征 | 大量"点击→选择→拖拽→输入→运行"等操作动词 |
| 字幕密度 | 短句多，操作指令密集（"先点这里""然后打开XXX"） |

如果检测命中 ≥2 项，启用教程模式。

**教程模式额外输出：**

在笔记中（核心概念之后、详细笔记之前）插入 **操作流程总览**：

````markdown
## 📋 操作流程总览

> 💡 点击流程图中的 ▶ 图标可跳转到视频对应操作步骤

```mermaid
flowchart TD
    STEP1[▶ 0:00<br/>打开项目] --> STEP2[▶ 3:15<br/>创建蓝图类]
    STEP2 --> STEP3[▶ 6:30<br/>添加组件]
    STEP3 --> STEP4A[▶ 10:00<br/>配置参数]
    STEP3 --> STEP4B[▶ 12:00<br/>连线逻辑]
    STEP4A --> STEP5[▶ 15:30<br/>编译运行]
    STEP4B --> STEP5
    STEP5 --> STEP6[▶ 18:00<br/>调试测试]
    
    click STEP1 "https://www.bilibili.com/video/BVxxx/?t=0"
    click STEP2 "https://www.bilibili.com/video/BVxxx/?t=195"
    click STEP3 "https://www.bilibili.com/video/BVxxx/?t=390"
    click STEP4A "https://www.bilibili.com/video/BVxxx/?t=600"
    click STEP4B "https://www.bilibili.com/video/BVxxx/?t=720"
    click STEP5 "https://www.bilibili.com/video/BVxxx/?t=930"
    click STEP6 "https://www.bilibili.com/video/BVxxx/?t=1080"
```
````

**流程图生成规则：**
1. 从字幕中提取关键操作步骤（5-10 步为宜，不超过 15 步）
2. 每个节点标注：`步骤描述 + 时间戳`，时间戳转为可点击链接（使用 Mermaid `click` 语法）
3. 有分支操作时用分叉节点（如配置参数 vs 连线逻辑可并行进行）
4. 每步对应的关键截图放在流程图下方，用时间戳链接格式

**截图增强：**
教程模式下，`ENABLE_KEYFRAMES=true` 时降低截图间隔（将 `KF_INTERVAL` 临时设为 15-20 秒），更密集地捕获操作画面。截图紧跟在对应步骤下方：

```markdown
### 步骤 1：打开项目 [▶ 0:00](https://www.bilibili.com/video/BVxxx/?t=0)

![操作界面](assets/BVxxx/frame_0003.png)
> 📸 [截图于 1:30](https://www.bilibili.com/video/BVxxx/?t=90) — 项目创建界面
```

**笔记生成提示：**

```text
请基于以下视频素材生成一份结构化学习笔记：

视频标题：{TITLE}
作者：{AUTHOR}
时长：{DURATION}
来源：{PLATFORM}
原始链接：{ORIGINAL_URL}

字幕文本（已翻译/原文）：
{TEXT_CONTENT}

AI 摘要：
{AI_SUMMARY}

关键帧截图（{FRAME_COUNT} 张）：
{列出 keyframes.json 中的文件和时间戳}

请生成以下内容：
0. **阅读信息**：推荐阅读时长 + 难度评级（见下方说明）
1. 核心概念（3-5 个最重要的概念）
2. 详细笔记（按内容逻辑分段，每段标注时间范围）
3. 关键画面描述（分析截图内容，标注时间点）
4. 关键术语表（英文术语 → 中文翻译 → 简要说明）
5. 总结与思考
6. 扩展学习资源（推荐进一步学习的方向和链接）
7. 评论区精华讨论（精选 3-6 条有价值的评论，附跳转链接；无高质量评论则跳过）
8. 知识关系图（Mermaid 图，展示本课核心概念及其关联结构）

**阅读时长计算（三步法）：**

**第一步：基础阅读时间**
- 中文阅读速度基准：400 字/分钟
- 统计笔记正文总字数（不含代码块、Mermaid 图表、表格），除以 400

**第二步：图表浏览时间**
- 每个 Mermaid 图：+15 秒
- 每张截图：+10 秒
- 每个代码块：按行数 × 2 秒（阅读代码比读文字慢）

**第三步：难度系数修正**

内容越难，读者需要越多的暂停、思考、回读时间：

| 难度 | 系数 | 说明 |
| --- | --- | --- |
| 🌱 入门 | ×1.0 | 概念介绍、工具入门，读起来轻松 |
| 🌿 进阶 | ×1.3 | 有实现细节和原理，需要停下来理解 |
| 🌳 深入 | ×1.6 | 源码级密度，每段都可能需要反复读 |

**公式：**

```
阅读时长 = (基础分钟 + 图表分钟 + 代码分钟) × 难度系数
```

结果四舍五入到整数，最少标 1 分钟。

**计算示例：**

> 正文 6000 字 → 基础 15 分钟
> 5 个 Mermaid (+75s) + 5 张截图 (+50s) + 3 个代码块共 30 行 (+60s) → 图表约 3 分钟
> 难度 🌿 进阶 → ×1.3
> (15 + 3) × 1.3 = 23.4 → **约 23 分钟**

对比不加系数：18 分钟。进阶内容多了 5 分钟的理解缓冲，更贴近真实体验。

**难度评级标准：**

| 等级 | 图标 | 判断依据 |
| --- | --- | --- |
| ⭐ 入门 | 🌱 | 面向零基础，无需前置知识，纯概念介绍或工具入门 |
| ⭐⭐ 进阶 | 🌿 | 需要一定基础（了解基本概念），涉及具体实现或原理分析 |
| ⭐⭐⭐ 深入 | 🌳 | 面向有经验者，涉及源码解读、底层机制、性能优化、架构设计 |

**评级依据（综合判断，选最主要的一项）：**
1. 内容的前置知识要求（无 → 入门，需要基础 → 进阶，需要经验 → 深入）
2. 视频本身的定位（新手教程 → 入门，技术分享 → 进阶，源码解析 → 深入）
3. 术语密度和技术深度（概念介绍为主 → 入门，实现细节为主 → 进阶，底层原理为主 → 深入）

**内容可靠性评估与标注：**

视频作者不一定总是对的——可能基于旧版本、个人偏好、或记忆偏差。笔记应帮助读者**分辨哪些内容可靠、哪些需要自行验证**。

**可靠性评级：**

| 评级 | 图标 | 判断依据 |
| --- | --- | --- |
| ⭐⭐⭐ 可信 | 🟢 | 内容与官方文档一致，无明显错误或过时信息 |
| ⭐⭐ 参考 | 🟡 | 大部分正确，有少量过时 API/版本差异/表述不够精确 |
| ⭐ 谨慎 | 🟠 | 有争议内容、明显过时信息、或与官方文档冲突 |
| ⚠ 仅作了解 | 🔴 | 有已知事实错误，仅供了解思路，不可直接套用 |

**评级依据（不是挑剔，是帮助读者）：**
1. **版本匹配**：视频发布时间 vs 当前最新版本，API/功能是否有变更
2. **官方一致性**：视频中的说法是否和官方文档、源码行为一致
3. **争议内容**：是否存在"个人观点包装成事实"的表述
4. **遗漏风险**：是否有重要警告/边界条件被省略（可能导致读者踩坑）
5. **宽容原则**：小口误、非核心细节不扣分；只有在影响理解和实践时才降级

**过时/错误内容标注方式：**

在笔记中对应位置用引用块标注，语气尊重、对事不对人：

```markdown
> ⚠️ **版本差异**：视频中使用 XXX API（v0.17），当前最新版（v0.18）已改为 YYY。详见[官方迁移指南](URL)。

> 💡 **补充说明**：视频中提到 XXX，实际上在开启 YYY feature 后行为会不同。这里补充完整上下文。

> ⚠️ **注意**：视频中说"XXX 一定导致 YYY"，但官方文档指出在 ZZZ 条件下可能是另一种结果。建议对照官方文档验证。
```

**标注原则：**
1. **标注而非批判**：说"视频基于 v0.17，v0.18 已变更"而不是"作者说错了"
2. **给出正确来源**：每个标注附带官方文档/源码链接，让读者自己判断
3. **不过度标注**：只标注影响实践的差异，不动不动就标。通常一篇 55 分钟视频笔记有 1-3 个标注就够了
4. **小错误不标**：口误、拼写错误等不影响理解的不要标，显得吹毛求疵

**重要格式要求：**
- 笔记开头紧接视频信息后，添加阅读信息、难度评级、可靠性评级和标签
- 格式：`> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶 | 可靠性：🟡 参考`
- 下一行：`> 🏷️ #Rust #Bevy #ECS #源码分析`

**标签提取规则：**
每篇笔记自动提取 3-6 个标签，按以下维度：
| 维度 | 示例 |
| --- | --- |
| 技术栈 | `#Rust` `#C++` `#Python` `#UnrealEngine` |
| 框架/库 | `#Bevy` `#UE5` `#React` |
| 主题 | `#ECS` `#渲染` `#反射` `#AI` `#物理` |
| 内容类型 | `#教程` `#源码分析` `#入门` `#原理` |
| 难度 | `#进阶` `#入门` `#深入` |

标签统一格式 `#关键词`，中英文均可，用于后续搜索和修为面板统计。
- 如果可靠性为 🟢 可信且无任何需要标注的内容，可以省略可靠性标注
- 所有时间戳必须做成可点击的 Markdown 链接，格式为 [MM:SS](视频链接?t=总秒数)
- 每个笔记段落的标题格式：### [▶ MM:SS](链接?t=秒数) - MM:SS | 段落标题
- 截图下方的时间标注同样需要可点击链接
- 示例：### [▶ 3:00](https://www.bilibili.com/video/BV14UzWBLEXD/?t=180) - 8:00 | Query 与 System 参数

**Mermaid 图表要求（必须遵守）：**

视频内容经常涉及架构、流程、数据关系等概念，纯文字描述不够直观。**Claude 必须主动绘制 Mermaid 图表**来可视化关键概念。以下是不同类型内容的 Mermaid 使用指南：

| 内容类型 | 推荐图表类型 | 示例场景 |
| --- | --- | --- |
| 架构/组件关系 | `graph TD` / `flowchart` | 系统架构、模块依赖、ECS 层级 |
| 流程/步骤 | `flowchart LR` / `flowchart TD` | 算法流程、操作步骤、Pipeline |
| 数据流/管道 | `graph LR` | 数据从输入到输出的流动 |
| 时序/步骤关系 | `sequenceDiagram` | 多个阶段的时间顺序 |
| 状态转换 | `stateDiagram-v2` | 状态机、生命周期 |
| 类/结构层级 | `classDiagram` | 继承关系、trait 实现 |
| 时间线 | `timeline` | 版本演进、历史发展 |
| 对比/选择 | `graph TD` 含分支 | 不同方案的对比选择 |

**使用规则：**
1. **主动绘制，不要等用户要求**：只要内容有可可视化的结构，就主动生成 Mermaid 图表
2. **图表紧跟在相关文字之后**：先文字描述，再图表示意，互相补充
3. **每个核心概念至少配一个图**：如视频讲解了 3 个主要主题，每个主题至少有一个 Mermaid 图
4. **图表要带标题**：用加粗文字给每个图标注名称，如 **图：ECS 架构层级关系**
5. **截图和 Mermaid 配合使用**：截图展示视频画面，Mermaid 展示抽象关系，两者互补不重复
6. **避免过于简单的图**：少于 3 个节点的图没有价值，直接用文字描述即可

**示例：**

```markdown
### [▶ 15:30](https://www.bilibili.com/video/BVxxx/?t=930) - 20:00 | ECS 架构核心概念

这段讲解了 Bevy 中 Entity、Component、System 三者的关系：

**图：ECS 三者关系**

` + "```" + `mermaid
graph TD
    E[Entity 实体] -->|包含| C1[Component A]
    E -->|包含| C2[Component B]
    E -->|包含| C3[Component C]
    S[System 系统] -->|查询| C1
    S -->|查询| C2
    S -->|修改| C3
` + "```" + `

- Entity 只是一个 ID，本身不存储数据
- Component 是纯数据，不包含逻辑
- System 包含所有逻辑，通过 Query 筛选感兴趣的 Entity
```

**输出示例（B 站）：**

```markdown
### [▶ 3:00](https://www.bilibili.com/video/BV14UzWBLEXD/?t=180) - 8:00 | Query 与 System 参数

![System 参数代码](assets/BV14UzWBLEXD/frame_0005.png)

- Query 由 `QueryData` + `QueryFilter` 组成
- System 参数宽松：可混合 Query、Resource、Commands
```

**扩展学习资源要求：**

每篇学习笔记末尾应包含"扩展学习资源"章节，推荐用户下一步可以学习的内容。**Claude 必须主动搜索和推荐**，根据视频主题从以下信息来源中选取 5-8 个高质量链接。

| 资源类型 | 搜索方向 | 示例 |
| --- | --- | --- |
| **官方文档** | 视频涉及的技术/框架官方文档入口 | Bevy Book、UE5 官方文档、Rust 官方指南 |
| **同作者/频道视频** | 发布者的其他相关教程（同系列优先） | 同一 B 站 UP 主的系列下一集、同一 YouTube 频道的 Playlist |
| **知乎/中文文章** | 知乎上相关主题的高赞文章 | 配套原理讲解、源码分析系列 |
| **GitHub 仓库** | 视频中提到的开源项目、官方示例仓库 | `bevyengine/bevy`、视频配套示例代码 |
| **Wiki/百科** | 维基百科或技术 Wiki 的相关条目 | ECS 架构、四元数数学原理 |
| **社区/论坛** | Reddit、Stack Overflow、Bevy Discord 等 | 相关讨论帖、常见问题 |

**搜索与筛选要求：**

1. **不要凭空编造链接**：每个推荐必须有明确的标题和可访问的 URL，基于训练数据中确认存在的资源
2. **优先官方和权威来源**：官方文档 > 知名社区文章 > 个人博客
3. **标注推荐理由**：每个链接配一行简短说明（10-20 字），告诉读者为什么值得看
4. **按关联度排序**：和视频内容直接相关的排前面，延伸阅读排后面
5. **同系列视频优先**：如果视频是系列的一部分（如"第一课"），优先推荐系列的下一集
6. **如果没有足够资源可推荐**：至少提供官方文档入口和原视频发布者空间/频道链接，不要为了凑数而编造

**输出格式：**

```markdown
## 六、扩展学习资源

### 📖 官方文档
- [文档标题](URL) — 一句话推荐理由

### 🎬 相关视频
- [视频标题](URL) — UP主：XXX，一句话推荐理由

### 📝 文章/知乎
- [文章标题](URL) — 一句话推荐理由

### 🐙 GitHub 仓库
- [仓库名](URL) — 一句话推荐理由

### 📚 延伸阅读
- [标题](URL) — 一句话推荐理由
```

**文档末尾元数据（根据 `NOTE_METADATA` 配置）：**

当 `NOTE_METADATA=true`（默认）时，在笔记最末尾添加生成元信息：

```markdown
---

> 📋 **文档元信息**
>
> | 项目 | 内容 |
> | --- | --- |
> | 文档版本 | v1.0 |
> | 生成时间 | 2026-05-30 18:30 CST |
> | 生成耗时 | 约 3 分钟 |
> | 生成模型 | Claude Opus 4.8 |
> | Token 消耗 | 约 45,000 tokens |
> | Skill 版本 | myriad-mind v2.0 |
> | 原始资源 | [原视频标题](原始链接) |
>
> ⚡ 本文档由 AI 自动生成，内容基于视频字幕和截图分析，可能存在遗漏或识别误差。建议结合原视频对照学习。
>
> ### 更新日志
>
> | 版本 | 日期 | 变更说明 |
> | --- | --- | --- |
> | v1.0 | 2026-05-30 | 初始生成 |
```

**元数据说明：**
- **文档版本**：从 v1.0 开始，每次重新生成或大幅更新递增大版本（v1.0 → v2.0），小修改递增大版本（v2.0 → v2.1）
- **生成时间**：当前系统时间，格式 `YYYY-MM-DD HH:MM TZ`
- **生成耗时**：从用户输入到文档落盘的墙钟时间（估算，不含视频下载/ASR 等前置步骤）
- **生成模型**：当前使用的 Claude 模型名称
- **Token 消耗**：本次对话的估算 token 用量（输入 + 输出，取整到千位）
- **原始资源**：用户输入的原始 URL 或文件路径（不是内部缓存路径！）
- **更新日志**：每次重新生成文档时，追加一条变更记录。格式：`版本 | 日期 | 做了什么变更`
  - 如果是小更新（修复错别字、补充截图等）→ v1.0 → v1.1
  - 如果是重新生成（用新版 skill 完整重写）→ v1.0 → v2.0
  - 变更说明要具体："补充了第 3-5 节 Mermaid 图表""基于 myriad-mind v2.0 重新生成，新增知识关系图和扩展资源"

**调试信息（`DEBUG_METADATA=true` 时输出，默认关闭）：**

当启用调试模式时，在元信息末尾追加处理链路记录：

```markdown
> 🔧 **调试信息 / Debug Trace**
>
> | 步骤 | 工具 | 耗时 | Token | 说明 |
> | --- | --- | --- | --- | --- |
> | 输入识别 | 步骤 0 | ~2s | - | 识别为 B站视频 / YouTube / 知乎文章 / ... |
> | 数据读取 | Bash (cat) | ~5s | 5,000 | 从缓存读取字幕（XX KB）/ WebFetch 抓取 |
> | 截图分析 | Read (PNG) | ~15s | 3,000 | 读取 N 张截图，选中 M 张 |
> | 语言检测 | Claude | ~3s | 500 | 中文 → 跳过 / 英文 → 翻译 |
> | 教程检测 | 步骤 7.4 | ~2s | 200 | 命中 → 启用教程模式 / 未命中 |
> | 笔记生成 | Claude (Write) | ~90s | 35,000 | 生成结构化笔记正文 |
> | 图表绘制 | Claude (Mermaid) | ~30s | 5,000 | 生成 X 张 Mermaid 图表 |
> | 资源推荐 | Claude | ~15s | 3,000 | 推荐 N 条扩展资源 |
> | 评论获取 | curl / yt-dlp | ~20s | 2,000 | 获取 N 条，筛选 M 条 / 跳过 |
> | 截图嵌入 | Edit | ~5s | 500 | 将截图引用插入正文 |
> | 输出写入 | Write | ~2s | - | 写入 {路径} |
> | **合计** | | **~X 分钟** | **~XX,000** | |
>
> 决策链路：{INPUT} → 步骤0({MODE}) → 步骤0.7({TOKEN}) → {KEY_DECISIONS} → 步骤7 生成笔记 → 步骤8 {CLEANUP_ACTION}
```

**调试信息字段说明：**
- **耗时**：近似墙钟时间（含 IO 等待），秒/分钟
- **Token**：该步骤估算 token（输入+输出），"-" 表示可忽略
- **合计**：总耗时和 token，应与元信息中"生成耗时""Token 消耗"接近

**输出路径决定逻辑：**

```bash
# 读取 NOTE_OUTPUT_DIR 配置
NOTE_OUTPUT_DIR="${NOTE_OUTPUT_DIR:-}"

if [ -n "$NOTE_OUTPUT_DIR" ]; then
  # 用户指定了目录 → 使用指定目录
  OUTPUT_BASE="$NOTE_OUTPUT_DIR"
else
  # 未指定 → 使用当前工作目录
  OUTPUT_BASE="$(pwd)"
fi

# 按主题分子目录（从视频/文章标题自动提取）
# 示例：OUTPUT_BASE/Bevy学习笔记/LearnEcs.md
OUTPUT_PATH="$OUTPUT_BASE/{SUBJECT_DIR}/{FILENAME}.md"
```

**路径规则：**
- 笔记先写入 `/tmp/video_analysis/{VIDEO_ID}/learning_notes.md`（中间产物）
- 最终复制到 `$OUTPUT_PATH`（按 NOTE_OUTPUT_DIR 配置）
- 子目录名从内容自动推断（如 Bevy 相关 → `Bevy学习笔记/`，Unreal 相关 → `Unreal学习笔记/`）
- 如果目标目录不存在，自动创建（`mkdir -p`）
- CLEANUP_TEMP=true 时删除 `/tmp/` 中间文件

### 步骤 8：清理临时文件

流程完成后，根据 `CLEANUP_TEMP` 配置决定是否清理临时文件。

```bash
CLEANUP_TEMP="${CLEANUP_TEMP:-true}"

if [ "$CLEANUP_TEMP" = "true" ]; then
  rm -rf /tmp/video_analysis/{VIDEO_ID}
  echo "已清理临时文件: /tmp/video_analysis/{VIDEO_ID}"
else
  echo "保留临时文件（CLEANUP_TEMP=false）: /tmp/video_analysis/{VIDEO_ID}"
fi
```

**说明：**
- `CLEANUP_TEMP=true`（默认）：删除 `/tmp/video_analysis/{VIDEO_ID}/` 整个目录，释放磁盘空间
- `CLEANUP_TEMP=false`：保留所有中间产物（视频、音频、字幕、截图），方便调试排查问题
- `download_url.json` / `download_url_response.txt` 等非视频专属文件，在所有任务完成后一并清理

### 步骤 9：收尾 — 更新修为面板 + 学习建议

笔记写入完成后，根据配置执行收尾工作。

#### 9.1 自动更新修为面板（`AUTO_UPDATE_PANEL`）

```bash
AUTO_UPDATE_PANEL="${AUTO_UPDATE_PANEL:-true}"

if [ "$AUTO_UPDATE_PANEL" = "true" ]; then
  PANEL_PATH="${NOTE_OUTPUT_DIR:-$(pwd)}/修为面板.md"
  
  if [ -f "$PANEL_PATH" ]; then
    echo "📊 更新修为面板..."
    # 触发修为面板模式：重新扫描笔记目录，刷新成就/统计/仪表盘
    # Claude 应读取现有修为面板，追加新笔记信息，更新所有统计数据
  else
    echo "💡 尚未创建修为面板，是否现在创建？"
    echo "   [Y] 创建 — 生成完整的修为面板（成就+统计+知识地图）"
    echo "   [N] 跳过 — 下次再说"
    # 等待用户响应
  fi
fi
```

**更新逻辑：**
- 修为面板存在 → 自动刷新：追加新笔记到知识全景，更新成就进度，刷新统计数字
- 修为面板不存在 → 提示用户创建（默认 Y），一次性生成完整面板
- `AUTO_UPDATE_PANEL=false` → 跳过，不打扰

#### 9.2 学习路线推荐（`AUTO_SUGGEST_NEXT`）

```bash
AUTO_SUGGEST_NEXT="${AUTO_SUGGEST_NEXT:-true}"

if [ "$AUTO_SUGGEST_NEXT" = "true" ]; then
  echo ""
  echo "🧭 是否需要学习路线推荐？"
  echo "   基于你当前的知识结构 + 行业热门技术栈，我可以推荐下一步学习方向。"
  echo "   [Y] 推荐 — 分析现有笔记，给出个性化学习路线"
  echo "   [N] 跳过 — 完成"
  # 等待用户响应
  
  if [ 用户选择 Y ]; then
    # Claude 分析当前知识结构：
    # 1. 已覆盖领域及深度
    # 2. 明显知识缺口
    # 3. 行业热门方向（结合时效性）
    # 4. 输出排序后的推荐列表，每条附理由
  fi
fi
```

**推荐逻辑：**
1. 扫描所有笔记，提取技术栈标签和难度分布
2. 识别知识缺口（如"学了 ECS 但没学 Bevy 3D 渲染"）
3. 结合行业趋势（如 AI Agent、Rust 服务端、游戏引擎脚本语言等）
4. 输出 Top 3-5 推荐方向，每条标注：
   - 推荐理由（基于现有知识结构的衔接性）
   - 建议资源（视频/文章/官方文档）
   - 预估学习时间

**输出格式：**

```markdown
🧭 学习路线推荐

基于你当前的 {N} 篇笔记（{技术栈列表}），建议下一步：

1. ⭐ **{方向}** — 你已经掌握了 {前置A} 和 {前置B}，这个方向是自然延续
   - 📖 建议资源：...
   - ⏰ 预估时间：约 X 小时

2. ...
```

#### 配置说明

| 配置项 | 默认 | 说明 |
| --- | --- | --- |
| `AUTO_UPDATE_PANEL` | true | 笔记生成后自动更新修为面板 |
| `AUTO_SUGGEST_NEXT` | true | 工作结束后提供学习路线推荐 |

---

## 文章学习模式

当步骤 0 识别输入为文章/文档 URL 时，跳过视频相关步骤（1-4、7.2），走简化流程。

### 文章处理步骤

#### A1. 抓取文章内容

使用 `WebFetch` 工具抓取文章页面，提取：

```text
请从以下页面提取：
1. 文章标题
2. 作者（如有）
3. 发布日期（如有）
4. 正文内容（保留代码块和技术术语原文）
5. 文章中包含的图片/图表的 URL 列表（如有）
```

将提取的内容保存到 `/tmp/video_analysis/{ARTICLE_ID}/article.md`。

#### A2. 语言检测与翻译

同步骤 6。检测文章语言，英文内容翻译为中英对照。中文文章跳过翻译。

#### A3. AI 生成总结

同步骤 5。直接由 Claude 基于文章内容生成标题、摘要和核心要点。

#### A4. 生成学习笔记

核心流程同步骤 7，但有以下差异：

| 视频模式 | 文章模式 |
| --- | --- |
| 内容来源 = 字幕文本 | 内容来源 = 文章原文 |
| 有时间戳，生成可点击链接 | **无时间戳**，按文章段落结构组织 |
| 有关键帧截图（ENABLE_KEYFRAMES） | **无截图**，ENABLE_KEYFRAMES 自动忽略 |
| 有评论区精华（ENABLE_COMMENTS） | **无评论区**，ENABLE_COMMENTS 自动忽略 |
| 可靠性评级参考视频时效 | 可靠性评级参考文章时效 + 来源权威性 |

**文章笔记结构：**

```text
请基于以下文章内容生成一份结构化学习笔记：

文章标题：{TITLE}
作者：{AUTHOR}
发布日期：{DATE}
来源：{URL}

文章正文：
{ARTICLE_CONTENT}

请生成以下内容：
0. 阅读信息：推荐阅读时长 + 难度评级（ENABLE_READING_INFO）
1. 核心概念（3-5 个最重要的概念）
2. 详细笔记（按文章段落/章节逻辑分段，不标注时间）
3. 关键图表描述（如果文章含图表的 URL，分析其内容）
4. 关键术语表（英文术语 → 中文翻译 → 简要说明）
5. 总结与思考
6. 扩展学习资源（ENABLE_RESOURCES）：官方文档、相关文章、GitHub 仓库等

**格式要求：**
- 不生成时间戳链接（文章无视频时间轴）
- ENABLE_MERMAID=true 时主动绘制 Mermaid 图表
- ENABLE_READING_INFO=true 时在开头标注阅读时长和难度
- ENABLE_RESOURCES=true 时在末尾附加扩展学习资源
- 章节用"##"编号，段落标题直接用"### 段落主题"（无需 ▶ 和时间）
```

**文章可靠性评级：**

文章的可靠性判断额外考虑：
- **来源权威性**：官方文档 > 知名博客 > 个人博客 > 匿名文章
- **时效性**：发布日期距今越久，越需要对照最新文档验证
- **引用链**：文章是否引用了官方来源、学术论文、源码

#### A5. 清理

同步骤 8。文章模式不产生视频/音频文件，仅清理抓取缓存。

**文章输出格式：**

```markdown
# {文章标题} — 学习笔记

> 📺 来源：{原文链接} | 作者：{AUTHOR} | 发布日期：{DATE}
>
> 💡 原文可点击链接查看

---

> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶 | 可靠性：🟡 参考

## 一、AI 摘要

...

## 二、核心概念

...

## 三、详细笔记

...（按文章段落逻辑组织，无时间戳）

## 四、关键术语表

...

## 五、总结与思考

...

## 六、扩展学习资源

...

---

> 📋 **文档元信息**（ENABLE_METADATA=true 时输出）
```

**文章模式专用说明：**
- `ARTICLE_ID` = 文章 URL 的域名 + 路径哈希（如 `zhihu_p123456`），用于临时文件目录命名
- 文章中的图片/图表 URL 可以在笔记中用 `![描述](URL)` 直接引用（不需要下载）
- 如果文章是系列的一部分（如知乎专栏），在扩展资源中推荐系列其他文章

---

## 本地文档模式

当步骤 0 识别输入为本地文档文件（`.md`/`.txt`/`.pdf`/`.rst` 等）时使用。比文章模式更简单——不需要 WebFetch，直接用 Read 工具读取文件内容。

### 本地文档处理

#### LD1. 读取文件

```bash
# 读取文件内容（Claude 直接用 Read 工具）
# 提取文件名作为标题，路径作为来源标识
```

#### LD2. 语言检测与翻译

同步骤 6。英文内容翻译为中英对照。

#### LD3. AI 生成总结

同步骤 5。基于文档内容生成摘要和要点。

#### LD4. 生成学习笔记

流程同文章模式 A4，**必须标注原始文件路径**。

**笔记头部格式：**

```markdown
# {文件名} — 学习笔记

> 📂 原始资源：`{绝对路径}`
>
> 📅 文件类型：本地 Markdown / 文本文档 / PDF

> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶
```

---

## 本地目录模式

当步骤 0 识别输入为目录路径时使用。扫描目录下所有支持的文件，逐个处理后生成合并笔记。

### 目录处理流程

#### DIR1. 扫描目录

```bash
# 递归扫描（最多 2 层），列出所有支持的文件
find "{DIR_PATH}" -maxdepth 2 -type f \( \
  -name "*.md" -o -name "*.txt" -o -name "*.pdf" \
  -o -name "*.mp4" -o -name "*.mov" -o -name "*.avi" -o -name "*.mkv" \
  -o -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" -o -name "*.flac" \
\) | sort
```

#### DIR2. 逐个处理

对每个文件按对应模式处理：
- `.md`/`.txt`/`.pdf` → 本地文档模式
- `.mp4`/`.mov`/`.avi`/`.mkv` → 视频模式（从步骤 3 开始）
- `.mp3`/`.wav`/`.m4a`/`.flac` → 音频模式（从步骤 4 开始）

#### DIR3. 合并输出

生成**一份合并的学习笔记**，结构：

```markdown
# {目录名} — 学习笔记合集

> 📂 原始目录：`{绝对路径}`
>
> 📊 扫描结果：共 N 个文件（M 个视频 + K 个文档 + L 个音频）

> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶

## 📑 目录

1. [文件名1](#文件1锚点) — 类型 | 一句话概括
2. [文件名2](#文件2锚点) — 类型 | 一句话概括
...

---

## 文件1标题

> 📂 原始资源：`{绝对路径}`

...（该文件的完整笔记内容）...

---

## 文件2标题

> 📂 原始资源：`{绝对路径}`

...（该文件的完整笔记内容）...
```

**目录模式注意事项：**
- 每个文件的笔记标注 `📂 原始资源：{绝对路径}`，方便回溯
- 如果某个文件处理失败（如视频下载失败），在笔记中标注 `⚠️ 处理失败：{原因}`，不阻断其他文件
- 目录下的 `.md` 可能已是之前生成的学习笔记——此时跳过或提取摘要，避免笔记套娃
- 按文件名字母顺序排列（或按修改时间排序）

---

## 代码项目分析模式

当步骤 0 识别输入为代码项目（GitHub URL 或本地代码目录）时使用。分析项目功能、代码结构、核心模块关系，生成 Mermaid 架构图，输出代码阅读指南。

### 代码分析处理流程

#### CODE1. 扫描项目结构

```bash
# 如果是 GitHub URL，先 clone 到临时目录
if [[ "{INPUT}" =~ ^https?://github\.com/ ]]; then
  git clone --depth 1 "{INPUT}" /tmp/video_analysis/{PROJECT_NAME}
  PROJECT_PATH="/tmp/video_analysis/{PROJECT_NAME}"
else
  PROJECT_PATH="{INPUT}"
fi

# 扫描项目结构（排除 node_modules/.git/target 等）
find "$PROJECT_PATH" -maxdepth 3 -not -path '*/node_modules/*' \
  -not -path '*/.git/*' -not -path '*/target/*' \
  -not -path '*/__pycache__/*' -not -path '*/vendor/*' \
  | head -200
```

#### CODE2. ⚠️ 灵力评估（Token 估算 — 必须执行）

**在读取任何代码文件之前，必须先估算 token 消耗并向用户确认！**

```bash
# 统计代码文件数量和总大小
CODE_FILES=$(find "$PROJECT_PATH" -type f \( \
  -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.rs" -o -name "*.go" \
  -o -name "*.java" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \
  -o -name "*.toml" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" \
  -o -name "*.sh" -o -name "*.sql" -o -name "*.proto" \
  \) -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' \
  -not -path '*/__pycache__/*' | wc -l)

TOTAL_SIZE=$(find "$PROJECT_PATH" -type f \( \
  -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.rs" -o -name "*.go" \
  -o -name "*.java" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \
  \) -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' \
  -exec du -ch {} + | tail -1 | cut -f1)

echo "代码文件数: $CODE_FILES | 代码总量: $TOTAL_SIZE"
```

**灵力等级判定：**

| 项目规模 | 文件数 | 预估 Token | 操作 |
| --- | --- | --- | --- |
| 🟢 小型 | < 30 个 | < 30,000 | 直接分析，无需确认 |
| 🟡 中型 | 30-100 个 | 30,000-80,000 | 提示用户后直接执行 |
| 🟠 大型 | 100-300 个 | 80,000-200,000 | **必须确认**，提示可能消耗大量灵力 |
| 🔴 巨型 | > 300 个 | > 200,000 | **必须确认**，建议只分析核心模块 |

**确认提示模板（🟠 大型 / 🔴 巨型）：**

```text
⚠️ 灵力预警：该项目包含 {N} 个代码文件，预估需要消耗约 {TOKEN} tokens 进行完整分析。

完整分析会：
- 读取所有源文件
- 分析项目架构和模块关系
- 绘制 Mermaid 架构图
- 生成代码阅读指南

建议选项：
1. 【完整分析】— 消耗约 {TOKEN} tokens，生成完整报告
2. 【核心模块】— 只分析主要源码目录，跳过测试/示例/文档，约节省 40-60% 灵力
3. 【快速概览】— 只读 README + 配置文件 + 目录结构，生成简要概览，约节省 80% 灵力
4. 【自定义】— 你指定要重点分析的目录或文件

请选择（1/2/3/4）：
```

#### CODE3. 核心文件读取

**策略**：先读项目元信息文件（README、Cargo.toml、package.json、go.mod 等），理解项目定位，再按目录结构逐模块读取核心代码。

优先级顺序：
1. `README.md` / `README` — 项目说明
2. 构建配置文件（`Cargo.toml`/`package.json`/`go.mod`/`CMakeLists.txt` 等）
3. 主入口文件（`main.rs`/`main.py`/`index.js`/`main.go` 等）
4. 核心模块目录（`src/`/`lib/`/`core/` 等）中的关键文件
5. 测试目录（`tests/`/`__tests__/` 等）— 可跳过以省灵力
6. 配置文件（`config/`/`*.yaml`/`*.toml` 等）

#### CODE4. 生成代码分析报告

**报告结构：**

```markdown
# {项目名} — 代码分析报告

> 📂 原始资源：{GitHub URL 或本地路径}
>
> 🔮 灵力消耗：约 XX,XXX tokens

> ⚠️ 本报告由 AI 基于代码阅读生成，可能存在理解偏差。建议搭配源码阅读使用。

## 一、项目概览

**这个项目是干什么的？**（用 2-3 句话概括）

| 项目 | 内容 |
| --- | --- |
| 项目名 | xxx |
| 语言/框架 | Rust / Python / TypeScript... |
| 构建工具 | Cargo / npm / Go modules... |
| 代码规模 | N 个文件，约 X KB |
| 许可证 | MIT / Apache-2.0... |

## 二、核心架构

**图：项目整体架构**

` + "```" + `mermaid
graph TD
    ...
` + "```" + `

## 三、目录结构

` + "```" + `
project/
├── src/           # 核心源码 — 负责 XXX
│   ├── main.rs    # 入口 — 启动流程
│   ├── lib.rs     # 库入口 — 公共 API
│   └── ...
├── tests/         # 测试
└── Cargo.toml     # 依赖配置
` + "```" + `

## 四、核心模块详解

### 模块 A（`src/xxx.rs`）

**图：模块 A 内部流程**

` + "```" + `mermaid
flowchart TD
    ...
` + "```" + `

- 功能说明
- 关键函数/类型
- 与其他模块的关系

### 模块 B...

## 五、依赖关系

**图：模块间依赖关系**

` + "```" + `mermaid
graph LR
    A --> B
    B --> C
    ...
` + "```" + `

## 六、关键入口与数据流

- 程序从哪里开始执行
- 数据如何流经各模块
- 关键 API / 接口

## 七、代码阅读建议

- 建议的阅读顺序（从哪开始看）
- 哪些模块可以先跳过
- 值得深入学习的设计模式/技巧

## 八、学习资源推荐

> 📌 仅当分析的是**知名开源项目**（如 React、Bevy、Kubernetes 等）时生成此章节。小众/个人项目跳过。

**图：项目生态学习路径**

` + "```" + `mermaid
graph LR
    PROJ[{项目名}] --> DOC[官方文档]
    PROJ --> BOOK[推荐书籍]
    PROJ --> TUTORIAL[教程/视频]
    PROJ --> COMMUNITY[社区/论坛]
    PROJ --> RELATED[相关项目]
` + "```" + `

### 📖 官方资源
- [官方文档](URL) — 第一手资料，建议从 Getting Started 开始
- [API 参考](URL) — 查阅具体接口
- [官方示例](URL) — 最佳实践参考

### 📚 推荐书籍/文章
- [书名/文章标题](URL) — 适合人群 + 一句话推荐理由
- [源码剖析系列](URL) — 如果存在知名的源码解读系列

### 🎬 视频教程
- 推荐 1-3 个高质量的视频/系列教程

### 💬 社区
- 官方 Discord/Slack/论坛
- 知乎/Reddit 相关讨论

### 🔗 相关项目
- 基于此项目的知名衍生项目
- 类似方向的其他开源项目（对比参考）
```

**知名项目判定标准：**
- GitHub Stars > 5,000 → 视为知名项目，生成完整推荐
- GitHub Stars 1,000-5,000 → 精简推荐（仅官方资源 + 1-2 条）
- GitHub Stars < 1,000 → 跳过此章节，或只给官方文档链接
- 如果是纯本地项目（非 GitHub），跳过此章节

### 代码分析专用说明

- GitHub clone 使用 `--depth 1` 节省带宽，分析完成后根据 `CLEANUP_TEMP` 决定是否删除
- 配置文件（`.toml`/`.json`/`.yaml`）提供依赖和项目元信息，必须阅读
- 测试文件通常可以跳过，除非用户明确要求分析测试
- **如果项目没有 README**：从入口文件和配置文件推断项目功能，标注 `⚠️ 项目无 README，以下分析基于代码推断`
- **Mermaid 图表**：至少包含整体架构图 + 模块依赖关系图，复杂项目加上关键流程的时序图
- **知识关系图**：在报告末尾添加代码架构全景关系图（代码分析模式专用，不同于学习笔记的知识关系图）

---

## 搜索模式

当用户输入包含 `search` / `搜索` / `找一下` / `有没有` 等关键词时启用。全文搜索已有学习笔记。

### 触发方式

```
/myriad-mind search ECS
搜索笔记 渲染管线
找一下 State Tree
有没有关于反射的文章
```

### SCH1. 搜索范围

```bash
SEARCH_DIR="${NOTE_OUTPUT_DIR:-$(pwd)}"
KEYWORD="{用户输入的关键词}"

# 在所有 .md 笔记中搜索（排除实现方案等非笔记文件）
grep -rin "$KEYWORD" "$SEARCH_DIR" \
  --include="*.md" \
  --exclude="*实现方案*" \
  --exclude="*修为面板*" \
  -C 2
```

### SCH2. 输出格式

```markdown
# 🔍 搜索结果："{关键词}"

> 📅 搜索时间：2026-05-31 | 📊 共命中 N 处

| # | 笔记 | 匹配片段 | 标签 |
| --- | --- | --- | --- |
| 1 | [笔记标题](路径) | "...匹配上下文..." | `#Rust` `#ECS` |
| 2 | ... | ... | ... |

## 相关推荐

如果未找到精确匹配，建议：
- 尝试**近义词**：ECS ↔ Entity Component System
- 查看 [修为面板](路径) 获取全局知识地图
- 搜索关键词作为标签可能更快定位
```

### SCH3. 搜索策略

- **精确匹配优先**：标题完全匹配 → 正文匹配 → 标签匹配
- **模糊容错**：中英文互搜（搜"渲染"也能匹配"Rendering"标题）
- **上下文展示**：每个命中展示前后 30 字上下文
- **排序**：按相关性（标题 > 正文高频 > 正文低频）

---

## 对比模式

当用户输入包含 `compare` / `对比` / `比较` / `哪个讲得好` 等关键词时启用。并排对比两个内容来源的核心观点、覆盖范围、讲解风格。

### 触发方式

```
/myriad-mind compare 笔记A.md 笔记B.md        # 对比两篇已有笔记
/myriad-mind compare URL_A URL_B              # 下载并对比两个视频/文章
对比一下 Bevy ECS 和 UE5 类型系统              # 按关键词搜索已有笔记
哪个讲得好：BV14UzWBLEXD vs BVxxxxx           # 对比两个B站视频
```

### CMP1. 识别对比对象

支持三种输入方式：
| 输入 | 处理 |
| --- | --- |
| 两个文件路径 | 直接读取已有笔记 |
| 两个 URL | 分别下载/处理，生成临时笔记后对比 |
| 关键词 | 在 NOTE_OUTPUT_DIR 下搜索匹配的笔记标题 |

### CMP2. 分析维度

对两篇笔记从以下维度逐一对比：

| 维度 | 权重 | 评分方式 |
| --- | --- | --- |
| **内容深度** | ⭐⭐⭐ | 概念讲解的深入程度、是否涉及底层原理 |
| **覆盖广度** | ⭐⭐⭐ | 涵盖的子主题数量、是否有遗漏 |
| **讲解结构** | ⭐⭐ | 逻辑是否清晰、是否有层次递进 |
| **实战价值** | ⭐⭐ | 是否有可操作的代码/示例、能否直接应用 |
| **图示质量** | ⭐ | 截图/Mermaid 图表是否有效辅助理解 |
| **时效性** | ⭐ | 内容是否过时、API 是否最新 |

### CMP3. 输出格式

```markdown
# 🔬 内容对比：{标题A} vs {标题B}

> 📅 对比时间：2026-05-31

## 基本信息

| 项目 | 📘 A: {标题} | 📙 B: {标题} |
| --- | --- | --- |
| 作者 | {作者A} | {作者B} |
| 时长/字数 | {时长A} | {时长B} |
| 难度 | 🌿 进阶 | 🌱 入门 |
| 来源 | {平台A} | {平台B} |
| 可靠性 | 🟡 参考 | 🟢 可信 |

## 核心观点对比

| 主题 | A 的观点 | B 的观点 | 差异 |
| --- | --- | --- | --- |
| {主题1} | ... | ... | A 更深入 / B 有补充 / 一致 |
| {主题2} | ... | ❌ 未涉及 | A 独家覆盖 |
| ... | | | |

## 维度评分

| 维度 | A 得分 | B 得分 | 胜出 |
| --- | --- | --- | --- |
| 内容深度 | ⭐⭐⭐⭐ | ⭐⭐⭐ | A |
| 覆盖广度 | ⭐⭐⭐ | ⭐⭐⭐⭐ | B |
| 讲解结构 | ⭐⭐⭐⭐ | ⭐⭐⭐ | A |
| 实战价值 | ⭐⭐ | ⭐⭐⭐⭐ | B |
| 图示质量 | ⭐⭐⭐ | ⭐⭐⭐ | 平 |
| 时效性 | ⭐⭐⭐ | ⭐⭐⭐⭐ | B |
| **综合** | **19/30** | **22/30** | **B** |

## 覆盖范围热力图

` + "```" + `mermaid
%% 展示两个视频/文章的主题覆盖范围
graph LR
    subgraph A["📘 {A标题}"]
        A1["✅ ECS 基础"]
        A2["✅ Query 详解"]
        A3["✅ Schedule"]
        A4["❌ 实战项目"]
    end
    subgraph B["📙 {B标题}"]
        B1["✅ ECS 基础"]
        B2["❌ Query 浅"]
        B3["✅ Schedule"]
        B4["✅ 完整 Demo"]
    end
` + "```" + `

## 学习建议

### 如果你想深入理解原理 → 选 **A**
{理由}

### 如果你想快速上手实践 → 选 **B**  
{理由}

### 🏆 最佳组合
先看 **{B}** 建立直观认知 + 实操，再读 **{A}** 补原理细节。两者互补效果最佳。
```

### CMP4. 评分规则

- **主观评分**：AI 基于内容分析给出 1-5 星，非绝对客观
- **综合得分**：六个维度加权求和（深度×3 + 广度×3 + 结构×2 + 实战×2 + 图示×1 + 时效×1）
- **鼓励互补**：即使一方胜出，也推荐"组合拳"学习路径
- **不捧不踩**：标注差异而非优劣，尊重不同创作者的教学风格

---

## 修为面板模式

当用户输入为"修为面板""knowledge map""学习地图""我的知识图谱"等关键词时，扫描 `Docs/` 目录下所有已有学习笔记，生成**跨主题知识关系图**。

### 触发方式

```
/myriad-mind 修为面板
/修为面板
看看我的知识图谱
生成学习地图
```

### KM1. 扫描已有笔记

```bash
# 扫描 Docs 目录下所有 .md 学习笔记
find "D:/Project/MyClaude/Docs" -name "*.md" -not -name "*实现方案*" | sort
```

### KM2. 提取每篇笔记的元信息

读取每篇笔记的标题、核心概念、难度评级，构建知识索引：

```text
对以下笔记列表，提取每篇的：
1. 笔记标题
2. 2-3 个核心主题词
3. 难度（入门/进阶/深入）
4. 前置依赖（学习这篇之前需要先了解什么）
5. 技术栈标签（如 Rust, Bevy, UE5, ECS 等）
```

### KM3. 生成修为面板

基于提取的元信息，生成一张跨主题 Mermaid 图：

**图：个人修为面板（My Knowledge Map）**

```mermaid
graph TD
    subgraph 游戏引擎["游戏引擎"]
        UE5["UE5 类型系统\n🌿 进阶"] --> UE5_ST["State Tree\n🌿 进阶"]
    end
    subgraph Rust生态["Rust 生态"]
        BEVY_ECS["Bevy ECS\n🌿 进阶"] --> BEVY_2D["Bevy 2D\n🌿 进阶"]
    end
    RUST["📥 Rust 基础"] -.-> BEVY_ECS
    CPP["📥 C++基础"] -.-> UE5
    BEVY_ECS -.->|"ECS 思想可迁移"| UE5
    UE5_ST -.->|"AI 行为设计"| NEXT_AI["📤 行为树/GOAP"]
    BEVY_2D -.->|"渲染管线"| NEXT_GFX["📤 图形学"]

    click BEVY_ECS "./Bevy学习笔记/LearnEcs.md" "打开笔记"
    click BEVY_2D "./Bevy学习笔记/Learn2D.md" "打开笔记"
    click UE5 "./Unreal学习笔记/LearnUE5TypeSystem.md" "打开笔记"
    click UE5_ST "./Unreal学习笔记/LearnStateTree.md" "打开笔记"
```

> ⚠️ **Mermaid 语法注意**：节点标签中不能出现 `|` 字符（Mermaid 关键字），用 `·` 替代。缩进用 tab。换行用 `\n`（不用 `<br/>`，quoted 标签内 `<br/>` 不解析）。subgraph 标签和 edge label 含特殊字符时加双引号。**所有图表首行加 `%%{init: {'theme': 'dark'}}%%`** 以保证浅色/深色背景下均可读。**知识全景图必须给每个笔记节点加 `click` 指令**，用相对路径（`./子目录/笔记.md`），让读者能从图谱直接跳转到笔记。：节点标签中不能出现 `|` 字符（Mermaid 关键字），用 `·` 替代。缩进用 tab。换行用 `\n`（不用 `<br/>`，quoted 标签内 `<br/>` 不解析）。subgraph 标签和 edge label 含特殊字符时加双引号。**所有图表首行加 `%%{init: {'theme': 'dark'}}%%`** 以保证浅色/深色背景下均可读。

**生成规则：**
1. 用 `subgraph` 按技术栈/领域分组（Rust 生态、Unreal、前端、AI 等）
2. 每个节点格式：`ID[标题<br/>难度 emoji]`
3. 虚线标注跨领域关联（如 ECS 概念可跨引擎迁移）
4. 标注 📥 前置知识缺口和 📤 后续学习方向
5. 已完成的用实线框，建议下一步的用虚线框

### KM4. 输出格式

```markdown
# 🗺️ 我的修为面板

> 📅 生成时间：2026-05-31 | 📊 共收录 N 篇学习笔记 | 🕐 累计学习 X 小时

## ⚡ 修炼等级 / Cultivation Level

**当前境界：{境界名}** — 进度 {X}% 到下一级

` + "```" + `
▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱ {45}% 筑基 → 金丹
` + "```" + `

| 境界 | 要求 | 进度 | 状态 |
| --- | --- | --- | --- |
| 🔹 炼气期 | 1-4 篇笔记 | {X}/4 | {✅/🔓} |
| 🔹 筑基期 | 5-14 篇，≥2 个技术栈 | {X}/14 | {🔓} |
| 🔹 金丹期 | 15-29 篇，≥3 个技术栈，≥1 篇深入 | {X}/29 | {🔒} |
| 🔹 元婴期 | 30-49 篇，≥4 个技术栈，≥3 篇深入 | {X}/49 | {🔒} |
| 🔹 化神期 | 50-99 篇，≥5 个技术栈，≥5 篇深入 | {X}/99 | {🔒} |
| 🔹 大乘期 | 100+ 篇，全领域覆盖 | {X}/100 | {🔒} |
| 🔹 渡劫飞升 | 贡献笔记到社区 / 开源分享 | 0/1 | {🔒} |

**等级计算公式：**

```
修为值 = 笔记数 × 10 + 进阶笔记 × 5 + 深入笔记 × 10 + 技术栈数 × 8 + 累计小时数 × 2

修为值映射：
  0-40   → 炼气期    81-140 → 金丹期    291-490 → 化神期
  41-80  → 筑基期   141-290 → 元婴期    491+   → 大乘期
```

## 🏷️ 标签云 / Tag Cloud

` + "```" + `
#Rust(2) #Bevy(2) #ECS(1) #2D(1) #UnrealEngine(2) #C++(1)
#反射(1) #AI(1) #StateTree(1) #源码分析(1) #入门(1) #进阶(3)
` + "```" + `

> 💡 标签后的数字表示出现次数，字号越大 = 该领域积累越深

## 🏆 修炼成就 / Achievement

| 成就 | 进度 | 说明 |
| --- | --- | --- |
| 📝 初入道途 | 1/1 ✅ | 生成第一篇学习笔记 |
| 📚 博览群书 | 4/5 | 累计 5 篇笔记 |
| 🎯 专精一道 | 3/5 | 同一领域 5 篇（当前：Rust/Bevy 2 篇） |
| 🌿 融会贯通 | 2/3 | 3 个不同技术栈（当前：Rust, UE） |
| ⏰ 持之以恒 | 3.5/10 | 累计学习 10 小时 |
| 🔮 神识外放 | 0/1 | 贡献笔记到社区 / 分享链接 |

## 知识全景

` + "```" + `mermaid
graph TD
    ...
` + "```" + `

## 📊 学习面板 / Dashboard

### 技术栈分布

` + "```" + `mermaid
pie title 知识领域覆盖
    "Rust / Bevy" : 2
    "Unreal Engine" : 2
    "待探索" : 5
` + "```" + `

### 技能深度矩阵

` + "```" + `mermaid
quadrantChart
    title 技能深度 vs 广度
    x-axis 广度低 --> 广度高
    y-axis 入门 --> 精通
    quadrant-1 全能型
    quadrant-2 专家型
    quadrant-3 新手区
    quadrant-4 博学型
    "Bevy ECS": [0.4, 0.55]
    "Bevy 2D": [0.35, 0.5]
    "UE5 类型系统": [0.5, 0.7]
    "UE5 State Tree": [0.3, 0.4]
    "Rust 基础 📥": [0.2, 0.3]
    "C++ 基础 📥": [0.2, 0.3]
` + "```" + `

### 学习统计

| 维度 | 数据 |
| --- | --- |
| 📝 总笔记数 | N 篇 |
| 🕐 累计学习时长 | X 小时（视频时长 + 阅读时长） |
| 🏷️ 技术栈覆盖 | Rust, Bevy, Unreal Engine, C++ |
| 🌱🌿🌳 难度分布 | 入门 X / 进阶 Y / 深入 Z |
| 📅 最近学习 | {最新笔记标题} ({日期}) |
| 🔥 最长连续 | X 天（从第一次笔记至今） |

### 学习趋势

### 学习里程碑

` + "```" + `mermaid
timeline
    title 知识积累时间线
    YYYY-MM-DD : 初入道途 : 第一篇笔记
              : 第二篇笔记
    YYYY-MM-DD : 小有成就 : 第 N 篇笔记
    未来可期   : 下一突破 : 目标描述
` + "```" + `

| 月份 | 新增 | 累计 | 进度 |
| --- | --- | --- | --- |
| {月} | N 篇 | N | ████████████░░░░░░░░ XX% |

## 建议学习路径

基于现有知识结构，推荐的下一步学习方向：

1. **{方向1}** — 因为掌握了 {前置A} 和 {前置B}，可以进阶学习...
2. **{方向2}** — 补充 {缺口} 领域的知识...
3. ...

## 跨领域关联

- 💡 ECS 架构思想在 {Bevy} 和 {Unity DOTS} 中都有应用
- 💡 渲染管线概念在 {Bevy 2D} 和 {OpenGL 基础} 中相通
- ...
```

### 成就系统说明

成就自动计算，基于 Docs 目录下的笔记元信息：
- **自动解锁**：统计满足条件即显示 ✅
- **进度追踪**：显示当前进度和下一级目标
- 成就列表可根据实际笔记内容动态扩展
- `quadrantChart` 中的技能位置由 AI 根据难度和广度估算
- 学习趋势改用 `timeline` + 进度表格，兼容所有 Mermaid 版本

### KM5. 触发词检测

在步骤 0 中增加检测逻辑：
- 用户输入包含"修为面板""知识图谱""学习地图""knowledge map""my knowledge"等 → 进入修为面板模式
- 用户输入"我学了什么""学习总结""知识总结" → 进入修为面板模式

### KM6. 修炼统计（DEBUG_METADATA=true 时）

修为面板每次更新时，在末尾追加调试统计。**累计 Token 跨会话累加**，分功能模块统计。

**统计维度：**
- **累计总览**：总 Token、更新次数、首次/最近更新日期
- **分功能统计**：笔记生成、知识全景、仪表盘、等级、标签、成就、搜索、路线推荐——每项独立累计
- **会话记录**：每次更新一条，标注日期 + 变更 + Token
- **分步调试**：同普通笔记的调试信息格式

**累加规则：**
- 每次 `AUTO_UPDATE_PANEL=true` 触发更新时，新增一条会话记录
- 累计 Token = 之前累计 + 本次消耗
- 分功能 Token 按本次操作归类累加（如本次只更新了标签云 → 标签项 +本次 Token）
- 面板版本号递增大版本或小版本（见元信息版本规则）

## 输出格式

### 视频模式

```markdown
## 视频分析结果

### 视频信息

| 项目 | 内容 |
| --- | --- |
| 视频ID | xxx |
| 作者 | xxx |
| 时长 | xxx |
| 来源平台 | B站 / YouTube / 抖音 / 本地文件 / 本地目录 |
| 原始资源 | url 或本地路径 |

> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶 | 可靠性：🟡 参考
> 🏷️ #标签1 #标签2 #标签3

### AI生成标题

xxx

### AI摘要

xxx

### 核心要点

1. xxx
2. xxx

### 生成文件

- 视频: /tmp/video_analysis/{ID}/video.mp4
- 音频: /tmp/video_analysis/{ID}/audio.mp3
- SRT字幕: /tmp/video_analysis/{ID}/subtitle.srt
- 纯文本: /tmp/video_analysis/{ID}/text.txt
- 关键帧截图: /tmp/video_analysis/{ID}/frames/ (含 keyframes.json 索引)
- 翻译文本: /tmp/video_analysis/{ID}/translated_text.txt (英文时)
- 评论区数据: /tmp/video_analysis/{ID}/comments.json (如有)
- 学习笔记: /tmp/video_analysis/{ID}/learning_notes.md
```

### 文章模式

```markdown
# {文章标题} — 学习笔记

> 📺 来源：{原文链接} | 作者：{AUTHOR} | 发布日期：{DATE}

> 📖 推荐阅读时长：XX 分钟 | 难度：🌿 进阶 | 可靠性：🟡 参考

### AI摘要
...

### 核心要点
...

### 生成文件

- 原文缓存: /tmp/video_analysis/{ID}/article.md
- 翻译文本: /tmp/video_analysis/{ID}/translated_text.txt (英文时)
- 学习笔记: /tmp/video_analysis/{ID}/learning_notes.md
```

## 常见问题

| 问题 | 解决方案 |
| --- | --- |
| **缺少环境变量** | 先确认 `ASR_BACKEND`；抖音/小红书/B站默认需要 `AI_DOUYIN_API_KEY`，自有 TikHub 模式需要 `TIKHUB_TOKEN`；火山后端需要 `BYTEDANCE_VC_TOKEN` 和 `BYTEDANCE_VC_APPID` |
| `ASR_BACKEND` 无效 | 只支持 `faster-whisper` 和 `volcengine` |
| `faster-whisper` 导入失败 | 执行 `python3 "$SKILL_DIR/scripts/install_faster_whisper.py"`，安装 helper 会先测速 PyPI 镜像并创建独立 venv；自定义 venv 时设置 `FW_PYTHON=/path/to/venv/bin/python` |
| 火山 API 认证失败 | Authorization 必须是 `Bearer;token`（分号无空格） |
| 首次运行较慢 | `faster-whisper` 首次会下载模型，等待下载完成后重试 |
| CUDA 环境不可用 | `FW_DEVICE=auto` 会自动回退到 CPU；只有 NVIDIA/CUDA 才走 GPU |
| 视频下载失败 | AI Douyin 返回 401 时检查 API Key；402 时充值积分或切换 TikHub；直链下载加 `User-Agent`；B 站可回退 `yt-dlp` |
| FFmpeg 找不到 | macOS: `brew install ffmpeg` / Linux: `sudo apt install ffmpeg` / Windows: `choco install ffmpeg` |
| yt-dlp 找不到 | macOS: `brew install yt-dlp` / 通用: `python3 -m pip install -U yt-dlp`（B 站 / YouTube 需要） |
