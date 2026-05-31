# 大衍决 (Myriad Mind) — 版本记录

## 版本号规则

`主版本.功能版本.修复版本`（如 `2.1.0`）

- **主版本**：重大架构变更、不兼容改动
- **功能版本**：新功能、流程改进、规则优化
- **修复版本**：bug 修复、文档勘误、配置微调

---

## v2.1.0 (2026-05-31)

### 截图系统改良 — 字幕引导 + 结构化审查 + 调试信息

**截图提取 (`extract_keyframes.py`)：**
- 移除 `interval`/`scene`/`both` 三模式，改为单一 `smart` 模式
- 新增字幕引导截图：`--timestamps` 参数接受 Claude 分析字幕后推荐的时间点
- 三层优先级：`guided`(字幕引导) > `scene`(场景检测) > `gap`(间隔保底)
- 修复 scene 模式时间戳不准的 bug（用 ffmpeg showinfo 获取精确 PTS）
- `keyframes.json` 新增 `trigger`/`scene_score` 字段

**SKILL.md 步骤调整：**
- 流水线重排：ASR 前移，截图后移
  - 步骤 3（提取音频）
  - 步骤 4（ASR 转写）
  - **新增** 步骤 4.5（Claude 分析字幕 → 推荐截图时间点 JSON）
  - **新增** 步骤 4.7（精准截图：引导时间点 + scene 检测 + gap 兜底）
- 步骤 7.1 重写：类型标签 + 评分体系 + 强制审查表 + 自检清单 + 异常处理
- 教程模式：改用 `KF_SCENE_THRESHOLD`/`KF_MAX_GAP` 调节截图密度
- 调试信息新增四维度：截图来源追踪、流水线耗时、内容来源标注、决策链路

**配置变更 (`.env`)：**
- 移除：`KF_INTERVAL`、`KF_MODE`
- 新增：`KF_SCENE_THRESHOLD`(0.25)、`KF_MAX_GAP`(120)、`KF_MIN_GAP`(3)
- `KF_MAX_FRAMES` 默认从 50 降到 40

---

## v2.0.0 (2026-05-25)

### 初始公开版本

- 完整的视频/文章/本地文件/代码项目/批量学习笔记生成流程
- 支持 B 站/YouTube/抖音/小红书/知乎/CSDN 等平台
- ASR 后端：faster-whisper + 火山引擎 VC API
- 视频解析代理：AI Douyin + TikHub
- 内置 Mermaid 图表、术语表、评论区精华、扩展学习资源
- 修为面板（成就系统 + 知识全景图 + 学习统计）
- 英文内容自动中英对照翻译
- 多种功能开关（ENABLE_KEYFRAMES / ENABLE_MERMAID / ENABLE_COMMENTS 等）
