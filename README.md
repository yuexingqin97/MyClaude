# MyClaude

个人 Claude Code AI Skill 学习与开发项目。

## 这是什么？

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是 Anthropic 推出的终端 AI 编程助手，支持通过 **自定义 Skill** 扩展能力。本项目用于学习和实践 Skill 开发——将重复性的多步骤工作流封装为可复用的 AI 技能。

## 已开发的 Skill

### 1. video-to-subtitle-summary

将视频/音频转为学习笔记的全自动 pipeline：

```
视频链接/本地文件 → 下载 → 字幕提取 → 关键帧截图 → AI 摘要 → 英译中 → 结构化笔记
```

**触发条件：** 提供抖音/小红书/B站/YouTube 链接，或本地 `.mp4`/`.mp3`/`.wav` 文件。

**技术栈：** Python 3.12 · ffmpeg · yt-dlp · faster-whisper · Claude API

**扩展功能（相比上游 [imlewc/valley](https://github.com/imlewc/video-to-subtitle-summary-skill)）：**
- 🖼️ 关键帧截图，自动嵌入到对应知识点旁边
- 🌐 英文视频自动翻译为中英对照
- 📝 整合字幕+截图+翻译+摘要的 Markdown 学习笔记

详见 [`video-to-subtitle-summary-skill/`](./video-to-subtitle-summary-skill/)

## 项目结构

```
MyClaude/
├── .claude/                          # Claude Code 项目配置
│   └── settings.local.json           # 权限 & hook 配置
├── video-to-subtitle-summary-skill/  # Skill 源码
│   ├── SKILL.md                      # Skill 定义（触发条件、流程）
│   ├── scripts/                      # Python 脚本
│   │   ├── download_video_candidates.py
│   │   ├── transcribe_faster_whisper.py
│   │   ├── extract_keyframes.py      # 关键帧截图
│   │   ├── download_youtube_subtitles.py
│   │   └── list_ai_douyin_tasks.py
│   ├── docs/                         # 文档 & 环境配置指南
│   └── tests/                        # 测试用例
├── Docs/                                     # Skill 输出产物
│   ├── 视频字幕总结Skill实现方案.md              # 技术架构 & 实现方案
│   └── Bevy学习笔记/LearnEcs.md                # 示例：Bevy ECS 教程学习笔记
└── README.md                         # 本文件
```

## 快速开始

### 环境要求

- **Claude Code** CLI（`claude` 命令）
- **Python 3.12+**
- **ffmpeg**（字幕提取、关键帧截图）
- **yt-dlp**（在线视频下载）
- **faster-whisper**（本地语音识别，可选）
- **AI Douyin API Key**（抖音视频处理，可选）

### 安装 & 使用

```bash
# 1. 安装 Claude Code
# 参考：https://docs.anthropic.com/en/docs/claude-code/overview

# 2. 克隆本项目
git clone git@github.com:yuexingqin97/MyClaude.git
cd MyClaude

# 3. 部署 Skill
cp -r video-to-subtitle-summary-skill/ ~/.claude/skills/video-to-subtitle-summary/

# 4. 安装依赖
pip install faster-whisper yt-dlp ffmpeg-python pillow
# 配置 .env（参考 video-to-subtitle-summary-skill/.env.example）

# 5. 在 Claude Code 中使用
claude
# 输入：帮我总结这个视频 https://www.bilibili.com/video/BV14UzWBLEXD
```

## Skill 开发心得

写一篇完整记录，详见 [skill-dev-journal.md](./skill-dev-journal.md)（待补充）。要点速览：

1. **Skill 是 Markdown + 脚本的组合** — `SKILL.md` 定义触发条件和流程，`scripts/` 负责具体执行
2. **权限配置很重要** — 需要在 `.claude/settings.json` 中 allow 脚本所需的 bash 命令
3. **截图内嵌比单独章节好** — 学习笔记中，把关键帧放在对应知识点旁边，阅读体验远胜于集中展示
4. **先跑通再优化** — 手动验证每一步的输入输出，确保每个脚本独立可用

## 待办

- [ ] 安装 CUDA 库启用 GPU 加速 whisper
- [ ] 更多 Skill：代码审查助手、PR 摘要生成器……
- [ ] 完善开发心得文档

## License

MIT
