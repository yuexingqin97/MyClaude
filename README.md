# MyClaude

个人 Claude Code AI Skill 学习与开发项目。

## 这是什么？

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是 Anthropic 推出的终端 AI 编程助手，支持通过 **自定义 Skill** 扩展能力。本项目用于学习和实践 Skill 开发——将重复性的多步骤工作流封装为可复用的 AI 技能。

## 已开发的 Skill

### 1. myriad-mind（大衍决）

```
链接丢进去 → 神识一扫 → 结构化笔记出炉
```

将视频/文章/音频炼化为学习笔记的全自动 pipeline：

```
视频链接 → 下载 → 字幕提取 → 关键帧截图 → AI 摘要 → 英译中 → Mermaid 图表 → 术语表 → 扩展资源 → 评论区精华 → 笔记出炉
文章链接 → 抓取正文 → AI 摘要 → 英译中 → Mermaid 图表 → 术语表 → 扩展资源 → 笔记出炉
```

**触发条件：** 提供视频链接（B站/YouTube/抖音/小红书）、文章链接（知乎/CSDN/掘金/Wiki）、或本地 `.mp4`/`.mp3`/`.wav` 文件。

**核心能力：**
- 📝 AI 摘要 + 核心要点 + 结构化笔记
- 🖼️ 关键帧截图内嵌（视频模式）
- 🧜 Mermaid 图表自动绘制（架构图/流程图/时序图等）
- 🌐 英文自动翻译为中英对照
- 📖 推荐阅读时长 + 难度评级 + 可靠性评级
- 🔗 视频时间戳可点击跳转
- 💬 评论区精华提取（视频模式）
- 📚 扩展学习资源推荐（官方文档/相关视频/知乎/GitHub/Wiki）
- 📋 文档元信息（生成时间/模型/Token 消耗）

**技术栈：** Python 3.12 · ffmpeg · yt-dlp · faster-whisper · Claude API

**扩展功能（相比上游 [imlewc/video-to-subtitle-summary-skill](https://github.com/imlewc/video-to-subtitle-summary-skill)）：**
- 🖼️ 关键帧截图，自动嵌入到对应知识点旁边
- 🌐 英文视频自动翻译为中英对照
- 🧜 Mermaid 图表自动生成
- 📄 文章学习模式（知乎/CSDN/Wiki 等）
- ⭐ 阅读时长/难度/可靠性评级
- 💬 评论区精华提取
- 📚 扩展学习资源推荐
- 📋 文档生成元信息

详见 [`myriad-mind/`](./myriad-mind/)

## 项目结构

```
MyClaude/
├── .claude/                       # Claude Code 项目配置
│   └── settings.local.json        # 权限 & hook 配置
├── myriad-mind/                   # 大衍决 Skill 源码
│   ├── SKILL.md                   # Skill 定义（触发条件、流程）
│   ├── scripts/                   # Python 脚本
│   │   ├── download_video_candidates.py
│   │   ├── transcribe_faster_whisper.py
│   │   ├── extract_keyframes.py   # 关键帧截图
│   │   ├── download_youtube_subtitles.py
│   │   └── list_ai_douyin_tasks.py
│   ├── docs/                      # 文档 & 环境配置指南
│   └── tests/                     # 测试用例
├── Docs/                          # Skill 输出产物
│   ├── 视频字幕总结Skill实现方案.md   # 技术架构 & 实现方案
│   ├── Bevy学习笔记/               # 示例笔记
│   └── Unreal学习笔记/             # 示例笔记
└── README.md                      # 本文件
```

## 快速开始

### 环境要求

- **Claude Code** CLI（`claude` 命令）
- **Python 3.12+**
- **ffmpeg**（字幕提取、关键帧截图）
- **yt-dlp**（在线视频下载）
- **faster-whisper**（本地语音识别，可选）
- **AI Douyin API Key**（抖音/小红书/B站视频处理，可选）

### 安装 & 使用

```bash
# 1. 安装 Claude Code
# 参考：https://docs.anthropic.com/en/docs/claude-code/overview

# 2. 克隆本项目
git clone git@github.com:yuexingqin97/MyClaude.git
cd MyClaude

# 3. 部署 Skill
cp -r myriad-mind/ ~/.claude/skills/myriad-mind/

# 4. 安装依赖
pip install faster-whisper yt-dlp ffmpeg-python pillow
# 配置 .env（参考 myriad-mind/.env.example）

# 5. 在 Claude Code 中使用
claude
# 输入：帮我总结这个视频 https://www.bilibili.com/video/BV14UzWBLEXD
# 输入：帮我总结这篇文章 https://zhuanlan.zhihu.com/p/xxxxx
```

## Skill 开发心得

写一篇完整记录，详见 [skill-dev-journal.md](./skill-dev-journal.md)（待补充）。要点速览：

1. **Skill 是 Markdown + 脚本的组合** — `SKILL.md` 定义触发条件和流程，`scripts/` 负责具体执行
2. **权限配置很重要** — 需要在 `.claude/settings.json` 中 allow 脚本所需的 bash 命令
3. **截图内嵌比单独章节好** — 学习笔记中，把关键帧放在对应知识点旁边，阅读体验远胜于集中展示
4. **先跑通再优化** — 手动验证每一步的输入输出，确保每个脚本独立可用

## 待办

- [ ] 更多 Skill：代码审查助手、PR 摘要生成器……
- [ ] 完善开发心得文档

## License

MIT
