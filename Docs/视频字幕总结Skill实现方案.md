# video-to-subtitle-summary 实现方案

## 概述

将短视频平台（抖音、小红书、B 站、YouTube）或本地视频/音频文件，自动转为带时间戳可点击跳转的结构化学习笔记。整个流程由 Claude Code Skill 驱动，组合多个外部工具和脚本完成。

---

## 整体架构

```
用户输入 URL/本地文件
        │
        ▼
   步骤 0/0.5/0.6：输入判断 + 配置读取 + 环境检查
        │
   ┌────┴──────────┬──────────────┐
   ▼               ▼              ▼
抖音/小红书       B站           YouTube          本地文件
   │               │              │                │
   │ AI Douyin     │ AI Douyin    │ yt-dlp         │
   │ 解析下载直链   │ 解析下载直链  │ 优先抓字幕     │
   │               │              │                │
   ▼               ▼              ▼                ▼
下载视频.mp4 ──── 下载视频.mp4   有字幕→跳ASR   提取音频.mp3
   │               │           无字幕→下载音频     │
   └───────┬───────┘              │                │
           │                      │                │
           └──────────┬───────────┘                │
                      ▼                            │
              提取音频 ffmpeg (步骤3)               │
                      │                            │
              关键帧截图 (步骤3.5) ←────────────────┘
                      │
              ┌───────┴───────┐
              ▼               ▼
        faster-whisper    火山引擎 VC
         (本地 CPU/GPU)   (云端 API)
              │               │
              └───────┬───────┘
                      ▼
              subtitle.srt + text.txt
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    AI 摘要       英译中检测    生成学习笔记
   (Claude)      (Claude)     (Claude + 截图)
   (步骤5)        (步骤6)      (步骤7)
```

---

## 核心依赖与角色

| 组件 | 用途 | 必需 | 备注 |
|------|------|------|------|
| **AI Douyin** (`ai-douyin.top9.cc`) | 解析抖音/小红书/B站视频的下载直链 | 仅国内平台 | 第三方代理，免费额度 |
| **TikHub** | 可选：自有 Token 直接解析 | 否 | 替代 AI Douyin 的高级方案 |
| **yt-dlp** | B站回退下载；抓取 YouTube 字幕 | B站/YouTube | YouTube 优先直接拿官方字幕 |
| **ffmpeg** | 视频→MP3 音频提取；关键帧截图 | 是 | 音频文件可跳过 |
| **faster-whisper** | 本地离线语音识别（默认 ASR 后端） | 是（默认） | 免费、隐私、CPU 可运行 |
| **火山引擎 VC** | 云端语音识别（可选 ASR 后端） | 否 | 精度更高，需付费 |
| **Claude** | AI 摘要、英译中、生成笔记 | 是 | Skill 载体，无需额外 API |
| **jq** | 解析 AI Douyin/TikHub 的 JSON 响应 | 仅在线模式 | 命令行 JSON 处理 |

---

## AI Douyin 详解

### 它是什么

AI Douyin (`ai-douyin.top9.cc`) 是一个**第三方代理服务**，不是官方 API。它的唯一作用是：**将抖音/小红书/B站的短链或网页 URL，解析成可直接下载的 .mp4 直链**。

### 为什么要用它

抖音、小红书、B站的视频地址有以下特点：

- **动态加密签名**：URL 中包含时效性 token，无法直接从网页链接构造下载地址
- **反爬机制**：直接 `curl` 会返回验证页面或 403
- **302 多层跳转**：短链 → 中间页 → 真实 CDN 地址

AI Douyin 帮你完成了这些跳转和解析，对外暴露一个简单的 REST API。

### 调用方式

```
POST https://ai-douyin.top9.cc/api/v1/video/download-url
Header: X-API-Key: {your_api_key}
Body:   {"url": "https://v.douyin.com/xxxxx/"}

Response:
{
  "download_url": "https://cdn-douyin.com/xxx/video.mp4",
  "download_urls": [...],        ← 可能有多个备用链接
  "title": "视频标题",
  "author": "作者名",
  "extracted_url": "https://...", ← 解析后的真实页面
  "cost": 1                       ← 消耗积分（成功才扣）
}
```

### 积分机制

- 注册送免费额度
- **成功解析并返回下载直链** → 扣 1 积分
- 解析失败（HTTP 非 200/链接过期等） → **不扣积分**
- 余额不足时返回 HTTP `402` + `"insufficient balance"`
- HTTP `401` → API Key 无效或缺失

### 替代方案

设置 `VIDEO_INFO_PROVIDER=tikhub`，用自己的 TikHub API Token 直接调用 TikHub 的解析端点，不经过 AI Douyin。

---

## ASR 语音识别后端

### 方案 A：faster-whisper（默认）

```
audio.mp3 → transcribe_faster_whisper.py → subtitle.srt + text.txt
```

**实现细节：**

- 自动检测硬件：NVIDIA GPU 存在 → `device="cuda"` + `compute_type="float16"`
- 无 GPU → `device="cpu"` + `compute_type="int8"`
- 默认模型 `small`（~466MB），首次运行自动从 HuggingFace 下载
- 模型大小可配：`FW_MODEL_SIZE=tiny|base|small|medium|large-v3`

**优点：** 免费、离线、隐私保护
**缺点：** CPU 模式较慢（~1:1 实时比），GPU 模式需 CUDA 环境

### 方案 B：火山引擎 VC（可选）

```
audio.mp3 → POST 火山提交任务 → 轮询 GET 结果 → subtitle.json → SRT
```

**优点：** 精度更高，不消耗本地算力
**缺点：** 需要付费开通、需要网络

---

## 扩展功能（基于上游新增）

### 1. 关键帧截图（步骤 3.5）

**脚本：** `scripts/extract_keyframes.py`

```python
# 核心原理：调用 ffmpeg 按固定间隔截帧
ffmpeg -i video.mp4 -vf "fps=1/{interval}" output/frame_%04d.png
```

**配置项：**

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `KF_INTERVAL` | 30 | 截图间隔（秒） |
| `KF_MAX_FRAMES` | 50 | 最大截图数 |
| `KF_MODE` | `interval` | 截图模式（`interval`=固定间隔，`scene`=场景变化） |

**输出：**
- `frames/frame_0001.png` ... `frame_NNNN.png` — 截图文件
- `frames/keyframes.json` — 时间戳索引（含 `timestamp_seconds` + `timestamp_label`）

### 2. 英译中（步骤 6）

由 Claude 完成，检测逻辑：

```
中文占比 < 30% → 判定为英文内容 → 翻译为中英对照
```

翻译格式：
```
[EN] Original English sentence here.
[CN] 这里的中文翻译。
```

技术术语保留英文原文并括号标注，如：反向传播（backpropagation）

### 3. 结构化学习笔记 + 可点击时间戳（步骤 7）

整合字幕、翻译、截图、AI 摘要，由 Claude 生成结构化 Markdown 笔记。

**时间戳可点击链接规则：**

| 平台 | URL 格式 | 示例 |
|------|---------|------|
| B 站 | `{原链接}?t={总秒数}` | `https://www.bilibili.com/video/BVxxx/?t=180` |
| YouTube | `youtube.com/watch?v={id}&t={秒数}` | `https://www.youtube.com/watch?v=abc&t=180` |
| 本地文件 | `file:///绝对路径?t={秒数}` | `file:///D:/videos/t.mp4?t=180` |

**笔记格式示例：**
```markdown
### [▶ 3:00](https://www.bilibili.com/video/BVxxx/?t=180) - 8:00 | 段落标题

![截图描述](assets/BVxxx/frame_0005.png)
> 📸 [截图于 4:00](https://www.bilibili.com/video/BVxxx/?t=240)

- 知识点要点...
```

---

## 数据流转

```
/tmp/video_analysis/{VIDEO_ID}/
├── video.mp4                 ← 步骤2: 下载的原始视频（或本地文件）
├── download_url.json         ← 步骤1: AI Douyin API 原始响应
├── download_url_response.txt ← 步骤1: API 响应含 HTTP 状态码
├── audio.mp3                 ← 步骤3: ffmpeg 提取的音频
├── subtitle.srt              ← 步骤4: ASR 生成的时间戳字幕
├── text.txt                  ← 步骤4: 纯文本字幕（供 AI 总结）
├── downloaded_subtitle.srt   ← 步骤2: 仅 YouTube，yt-dlp 直接抓取
├── frames/                   ← 步骤3.5: 关键帧截图
│   ├── frame_0001.png
│   ├── frame_0002.png
│   └── keyframes.json        ← [{file, timestamp_seconds, timestamp_label}, ...]
├── translated_text.txt       ← 步骤6: 英译中结果（仅英文视频）
└── learning_notes.md         ← 步骤7: 最终结构化学习笔记
```

所有中间文件保留在 `/tmp` 便于排查和复用。

---

## 环境变量一览

| 变量 | 可选值 | 默认值 | 说明 |
|------|--------|--------|------|
| `ASR_BACKEND` | `faster-whisper` / `volcengine` | `faster-whisper` | 语音识别后端 |
| `VIDEO_INFO_PROVIDER` | `ai-douyin` / `tikhub` | `ai-douyin` | 视频解析代理 |
| `AI_DOUYIN_API_BASE` | URL | `https://ai-douyin.top9.cc` | AI Douyin 服务地址 |
| `AI_DOUYIN_API_KEY` | string | — | AI Douyin API Key（国内平台必须） |
| `TIKHUB_TOKEN` | string | — | TikHub Token（可选高级方案） |
| `FW_MODEL_SIZE` | `tiny`/`small`/`medium`/`large-v3` | `small` | Whisper 模型大小 |
| `FW_DEVICE` | `auto`/`cuda`/`cpu` | `auto` | 推理设备 |
| `FW_COMPUTE_TYPE` | `int8`/`float16`/... | `""` (自动) | 精度类型 |
| `FW_PYTHON` | path | 自动查找 | Python 解释器路径 |
| `BYTEDANCE_VC_TOKEN` | string | — | 火山引擎 Token |
| `BYTEDANCE_VC_APPID` | string | — | 火山引擎 AppID |
| `KF_INTERVAL` | number | `30` | 截图间隔（秒） |
| `KF_MAX_FRAMES` | number | `50` | 最大截图数 |
| `KF_MODE` | `interval` / `scene` | `interval` | 截图模式 |

---

## 关键技术决策

| 决策 | 原因 |
|------|------|
| 默认用 faster-whisper 而非云服务 | 免费、离线、隐私，降低使用门槛 |
| YouTube 优先抓字幕不下载视频 | YouTube 官方字幕质量通常优于 ASR，且省流量和时间 |
| AI Douyin 作为默认代理而非直接 TikHub | 降低配置门槛，用户无需单独申请 TikHub |
| Commands 的概念贯穿步骤设计 | 每个步骤输出固定文件路径，下游步骤直接读取，解耦 |
| Claude 做 AI 总结/翻译而非第三方 API | Skill 本身跑在 Claude Code 里，零额外成本 |
| 截图内嵌到知识点旁边 | 阅读体验完胜独立"关键画面"章节 |
| 时间戳做成可点击链接 | 读者可直接跳转到视频对应位置，闭环学习体验 |
