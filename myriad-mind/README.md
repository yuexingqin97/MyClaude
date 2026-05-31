# myriad-mind（大衍决）🔮

> Claude Code Skill — 神识一扫，万物皆可为笔记。
>
> 视频/文章/本地文件/代码项目 → AI 摘要 + 关键帧截图 + Mermaid 图表 + 术语表 + 评论区精华 + 知识关系图 + 扩展资源，一炉出丹。
>
> **v2.1** | 9 种输入模式 | 30+ 功能 | 20+ 配置项
>
> 📁 笔记输出到 `../大衍决残卷/` —— 这是大衍决 Skill 的**实验场地**，所有炼化产物（学习笔记、截图、回顾文档）均落于此目录。其中 `LearnEcs.md` / `LearnEcs_v2.md` / `大衍决开发回顾与展望.md` 三份核心文档纳入版本控制作为效果样本，其余自动生成文件由 `.gitignore` 排除。

---

## ✨ 功能矩阵

### 输入（9 种模式）

| # | 模式 | 触发方式 |
|---|------|---------|
| 🎥 | 在线视频 | B站 / YouTube / 抖音 / 小红书 URL |
| 📝 | 在线文章 | 知乎 / CSDN / 掘金 / Wiki / 公众号 URL |
| 🎬 | 本地视频/音频 | `.mp4` / `.mov` / `.mp3` / `.wav` 文件路径 |
| 📄 | 本地文档 | `.md` / `.txt` / `.pdf` / `.rst` 文件路径 |
| 📁 | 本地目录 | 递归扫描，批量合并笔记 |
| 💻 | 代码项目 | GitHub URL 或本地代码目录 |
| 📊 | 修为面板 | `/myriad-mind 修为面板` |
| ⚖️ | 对比模式 | `/myriad-mind compare A B` |
| 🔍 | 搜索模式 | `/myriad-mind search 关键词` |

### 输出（8 大板块）

| # | 板块 | 说明 |
|---|------|------|
| 1 | AI 摘要 | 标题 + 一句话总结 + 核心要点 |
| 2 | 详细笔记 | 可点击时间戳、代码示例、结构化段落 |
| 3 | 关键帧截图 | 🎯字幕引导 + 结构化审查 + 审计追踪，内嵌知识点旁 |
| 4 | Mermaid 图表 | 架构图/流程图/时序图/状态图/类图，自动 dark theme |
| 5 | 关键术语表 | 英→中→说明，三列对照 |
| 6 | 评论区精华 | 精选高价值讨论 + 编辑注 + 跳转链接 |
| 7 | 知识关系图 | 每篇末尾的本课全景知识图谱 |
| 8 | 扩展学习资源 | 官方文档/相关视频/文章/GitHub/社区/延伸阅读 |

### 智能特性

| 特性 | 说明 |
|------|------|
| 🎯 字幕引导截图 (v2.1) | ASR 后分析字幕识别关键画面类型，反向推导最佳截图时间点 |
| 🔍 结构化截图审查 (v2.1) | 每张截图标注来源/质量评分/选中或跳过原因，完整审计追踪 |
| 💬 评论萃取 | B站/YouTube 评论自动获取→筛选→精华→嵌入笔记 |
| 🎓 教程检测 | 自动识别操作型视频，生成可点击操作流程图 |
| ⚡ 灵力预估 | 处理前估算时间+Token 消耗，超阈值确认 |
| 🏷️ 标签提取 | 自动提取 5 维度标签：技术栈/框架/主题/类型/难度 |
| 📊 可靠性评级 | 🟢🟡🟠🔴 四档，版本匹配+官方一致性+争议检测 |
| 📖 阅读元信息 | 预估阅读时长 + 难度评级 🌱🌿🌳 |
| 🔧 调试追踪 | 分步耗时 + Token + 截图来源 + 跳过原因 + 决策链路全记录 |

### 修为系统

| 组件 | 说明 |
|------|------|
| 修炼等级 | 炼气→筑基→金丹→元婴→化神→大乘→渡劫（7 级修仙体系） |
| 成就系统 | 6 项自动判定（初入仙门/博览群书/炼器大师/炼丹宗师/渡劫飞升/开宗立派） |
| 修为面板 | 知识全景 + 仪表盘 + 标签云 + 技能矩阵 + 学习里程碑 |
| 等级公式 | 笔记数×10 + 进阶×5 + 深入×10 + 技术栈×8 + 学习小时×2 |

---

## 📋 效果演示

> 以下三份文档是大衍决的**真实输出样本**，基于同一 B 站视频 [BV14UzWBLEXD](https://www.bilibili.com/video/BV14UzWBLEXD/)（~55 分钟 Bevy ECS 教程）生成。点击链接即可在 GitHub 上直接阅读渲染后的完整笔记。

### 📖 [LearnEcs_v2.md](../大衍决残卷/Bevy学习笔记/LearnEcs_v2.md) — v2.1 重制版（推荐首选阅读）

基于 **myriad-mind v2.1** 生成，最新能力展示：

- 🎯 **12 张截图**，🎯字幕引导 + 结构化审查 + 审计追踪
- 📝 **代码示例**贯穿全文，可直接复制运行
- 🧠 **10 张 Mermaid 图表**（dark theme），含知识关系全景图
- 💬 **评论区精华**，精选 B 站高价值讨论
- 🔧 **完整调试追踪**：流水线耗时 + 截图来源表 + 跳过原因 + 决策链路

### 📖 迭代对比：[LearnEcs.md (v2.0)](../大衍决残卷/Bevy学习笔记/LearnEcs.md) vs [LearnEcs_v2.md (v2.1)](../大衍决残卷/Bevy学习笔记/LearnEcs_v2.md)

同一视频的两版笔记，直观展示 skill 迭代效果：

| 维度 | v2.0 (LearnEcs.md) | v2.1 (LearnEcs_v2.md) |
|------|:--:|:--:|
| 截图 | 2 张（固定间隔） | **12 张**（字幕引导 + 审查） |
| 代码示例 | 几乎无 | 大量可运行 Rust 代码块 |
| Mermaid 图 | 8 张 | 10 张（dark theme） |
| 评论区 | 无 | 2 条精选 + 编辑注 |
| 调试追踪 | 简单耗时表 | 完整审计链（来源/评分/跳过） |
| Token | ~52K | ~75K |

### 📖 [大衍决开发回顾与展望.md](../大衍决残卷/大衍决开发回顾与展望.md) — 项目演化史

从 v0.1 到 v2.1 的完整迭代历程，涵盖 11 个版本的设计决策、功能矩阵、技术架构、成本分析、竞品对比、反思总结。适合想了解大衍决设计哲学和演化思路的读者。

---

## 🚀 安装指南

### 前置条件

| 依赖 | 必要性 | 说明 |
|------|--------|------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | ✅ 必须 | 支持 Skill 的 Agent 环境 |
| [FFmpeg](https://ffmpeg.org/) | ✅ 必须 | 音视频处理 |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | B站/YouTube 需要 | 视频下载与字幕抓取 |
| Python 3.9+ | faster-whisper 需要 | 本地语音转文字 |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 默认 ASR 后端 | 免费，本地运行，支持 CUDA |
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
# ========== ASR 后端 ==========
ASR_BACKEND=faster-whisper        # faster-whisper（免费）/ volcengine

# ========== 视频解析代理 ==========
VIDEO_INFO_PROVIDER=ai-douyin     # ai-douyin / tikhub
AI_DOUYIN_API_BASE=https://ai-douyin.top9.cc
AI_DOUYIN_API_KEY=your_api_key_here

# ========== faster-whisper 参数 ==========
FW_MODEL_SIZE=small               # tiny/base/small/medium/large-v2
FW_DEVICE=auto                    # auto 自动检测 GPU
FW_COMPUTE_TYPE=                  # 留空自动选择
FW_PYTHON=                        # 留空使用默认 venv

# ========== 截图参数 ==========
KF_INTERVAL=30                    # 每 N 秒截一张图
KF_MAX_FRAMES=50                  # 最多截取 N 张
KF_MODE=interval                  # interval / scene / both

# ========== 输出控制 ==========
NOTE_OUTPUT_DIR=./大衍决残卷       # 笔记输出目录（默认项目根目录）
CLEANUP_TEMP=true                 # 完成后清理临时文件
DRY_RUN=false                     # 调试模式，跳过下载直接用缓存

# ========== 自动化 ==========
AUTO_UPDATE_PANEL=true            # 新笔记后自动更新修为面板
AUTO_SUGGEST_NEXT=true            # 自动推荐下一步学习内容
DEBUG_METADATA=true               # 生成调试信息（分步耗时+决策链路+截图追踪）
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
帮我学习这个B站视频：https://www.bilibili.com/video/BVxxxxxxxxxx/
```

```
提取这个 YouTube 视频的字幕：https://www.youtube.com/watch?v=O87FdYIPeQk
```

```
帮我总结这个抖音视频：https://v.douyin.com/xxxxxx/
```

或使用 Skill 命令：

```
/myriad-mind https://www.bilibili.com/video/BVxxxxxxxxxx/
```

### 在线文章

```
帮我总结这篇知乎：https://zhuanlan.zhihu.com/p/xxxxx
```

```
/myriad-mind https://blog.csdn.net/xxx/article/details/xxxxx
```

### 本地文件

```
请帮我提取字幕并总结：~/Downloads/lecture.mp4
```

```
/myriad-mind ~/Desktop/recording.mp3
```

```
帮我分析这篇文档：~/Documents/rust-guide.md
```

> 本地文件模式无需 AI Douyin API Key，自动跳过视频下载步骤。

### 代码项目

```
帮我分析这个项目：https://github.com/bevyengine/bevy
```

```
/myriad-mind ~/projects/my-game/
```

> 代码分析前自动评估项目规模，超阈值会给出完整/核心/概览/自定义四个选项。

### 对比模式

```
/myriad-mind compare LearnEcs.md LearnEcs_v2.md
```

> 生成两篇笔记的结构/内容/质量/深度对比报告。

### 搜索模式

```
/myriad-mind search ECS
```

> 全文检索所有笔记，输出含上下文的相关段落。

### 修为面板

```
/myriad-mind 修为面板
```

> 展示修炼等级、成就徽章、技术栈分布、技能矩阵、学习里程碑、标签云。

---

## ⚙️ 配置说明

### 字幕后端

| 后端 | 环境变量值 | 说明 | 费用 |
|------|-----------|------|------|
| faster-whisper（默认） | `ASR_BACKEND=faster-whisper` | 本地 ASR，支持 CUDA 加速 | 免费 |
| 火山引擎 VC | `ASR_BACKEND=volcengine` | 云端 ASR | 按量付费 |

### 视频解析代理

| 代理 | 适用平台 | 费用 |
|------|---------|------|
| AI Douyin（推荐） | 抖音/小红书/B站 | 免费额度，解析扣 1 积分 |
| TikHub | 抖音/小红书/B站 | 按 TikHub 套餐 |
| 无需代理 | YouTube | 免费（yt-dlp 直接抓字幕） |

### faster-whisper 模型选择

| 模型 | 显存需求 | 速度 | 准确度 |
|------|---------|------|--------|
| tiny | ~1 GB | 最快 | 一般 |
| base | ~1 GB | 快 | 较好 |
| **small（推荐）** | ~2 GB | 适中 | 好 |
| medium | ~5 GB | 较慢 | 很好 |
| large-v2 | ~10 GB | 最慢 | 最好 |

### 输出控制

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `NOTE_OUTPUT_DIR` | `./大衍决残卷` | 笔记输出目录 |
| `CLEANUP_TEMP` | `true` | 完成后清理 `/tmp/video_analysis/` 缓存 |
| `DRY_RUN` | `false` | 调试模式，跳过下载直接用已有缓存 |
| `DEBUG_METADATA` | `true` | 生成调试信息（流水线耗时+截图审计+决策链路） |

### 自动化

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `AUTO_UPDATE_PANEL` | `true` | 新笔记自动更新修为面板统计 |
| `AUTO_SUGGEST_NEXT` | `true` | 基于知识结构自动推荐下一步学习 |
| `TUTORIAL_DETECTION` | `true` | 自动检测教程视频，启用操作流程图 |

---

## 🏗️ 技术架构

```
用户输入
    │
    ▼
步骤 0：模式识别（URL/文件/目录/关键词）
    │
    ▼
步骤 0.5：读取配置（.env）
    │
    ▼
步骤 0.7：灵力预估（时间+Token，超阈值确认）
    │
    ▼
步骤 1-4：内容获取（下载/ASR/抓取）
    │
    ▼
步骤 4.5：字幕分析（🎯引导：识别截图时间点）
    │
    ▼
步骤 4.7：截图提取（ffmpeg 精准截图）
    │
    ▼
步骤 5-6：AI 摘要 + 语言检测/翻译
    │
    ▼
步骤 7：生成笔记
    ├─ 7.1：截图审查（逐张审视→评分→筛选）
    ├─ 7.2：评论获取+筛选
    └─ 7.3：笔记生成（Mermaid+术语+资源+关系图）
    │
    ▼
步骤 8：清理临时文件
    │
    ▼
步骤 9：收尾（更新修为面板+学习建议）
```

**核心思路：** 所有"体力活"用脚本（下载/ASR/截图），所有"脑力活"用 Claude（理解/总结/画图/推荐）。人是炼气士，Claude 是炉鼎——人定方向，AI 出力。

---

## 📁 项目结构

```text
myriad-mind/
├── README.md                          # 本文件
├── SKILL.md                           # Skill 定义（Claude Code 读取，~3000 行）
├── CHANGELOG.md                       # 版本更新日志
├── .env.example                       # 环境变量模板（20+ 配置项）
├── LICENSE                            # MIT 协议
├── scripts/
│   ├── extract_keyframes.py           # 关键帧截图脚本
│   ├── download_video_candidates.py   # 视频下载（支持多候选 URL）
│   ├── download_youtube_subtitles.py  # YouTube 字幕抓取
│   ├── install_faster_whisper.py      # faster-whisper 安装助手
│   ├── list_ai_douyin_tasks.py        # AI Douyin 历史任务查询
│   └── transcribe_faster_whisper.py   # faster-whisper 转写（支持 CUDA）
├── tests/                             # 单元测试
└── docs/                              # 配置教程
    ├── ai-douyin-setup.md
    ├── tikhub-setup.md
    ├── faster-whisper-setup.md
    └── bytedance-vc-setup.md
```

---

## 📊 版本演进

| 版本 | 日期 | 关键变化 |
|------|------|---------|
| v0.1 | 05-20 | 奠基：视频→字幕→摘要 pipeline |
| v0.2 | 05-21 | 关键帧截图 + 英译中 |
| v0.3 | 05-22 | 可点击时间戳 + 字幕交叉校验截图 |
| v0.4 | 05-23 | Mermaid 图表 + 文章模式 + 扩展资源 |
| v0.5 | 05-26 | 评论区精华 + 可靠性评级 + 元信息 |
| v0.6 | 05-28 | 改名大衍决（myriad-mind） |
| v0.7 | 05-29 | 代码项目分析 + 本地目录 + 灵力预估 |
| v0.8 | 05-30 | 教程检测 + 对比模式 + 知识地图 |
| v0.9 | 05-31 | 修为面板 + 搜索 + 标签 + 修炼等级 + 收尾自动化 |
| v2.0 | 05-31 | 定型版：bug 修复 + 配置补全 + 旧笔记重生成 |
| **v2.1** | **05-31** | **截图系统改良：🎯字幕引导 + 结构化审查 + 审计追踪 + 评论区精华** |

> 详见 [CHANGELOG.md](./CHANGELOG.md)

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

> 默认方案（faster-whisper + AI Douyin）成本极低，基本可以零费用使用。一篇 55 分钟视频约消耗 5-8 万 tokens。

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
| 笔记输出到哪里 | 默认 `./大衍决残卷/`，可通过 `NOTE_OUTPUT_DIR` 自定义 |
| 如何搜索旧笔记 | `/myriad-mind search 关键词` |
| 如何对比两篇笔记 | `/myriad-mind compare A.md B.md` |

---

## 📄 License

[MIT](./LICENSE)

## 🙏 致谢

- 上游项目：[imlewc/myriad-mind-skill](https://github.com/imlewc/myriad-mind-skill)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — 高效本地 ASR
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 强大的视频下载工具
- [FFmpeg](https://ffmpeg.org/) — 音视频处理基石
