# CLAUDE.md — MyClaude 项目

## Claude 可以访问的范围

Claude 可以读写此项目下所有文件，包括：
- `myriad-mind/` — 大衍决 Skill 源码
- `大衍决残卷/` — 生成的笔记输出
- 其他任何需要 AI 辅助的文件

Claude 可以通过 memory 系统（`C:/Users/Yxqin/.claude/projects/D--Project-MyClaude/memory/`）跨会话保持项目状态。

## 项目组成

### 大衍决 (Myriad Mind) Skill

- 源码：`myriad-mind/`
- 部署：`~/.claude/skills/myriad-mind/`
- 笔记输出：`大衍决残卷/`
- 6 个 Python 脚本：`myriad-mind/scripts/`
- 详细状态：见 memory 文件 `myriad-mind.md`

### 独立 App：大衍决 App

已将 Skill 的独立 App 开发拆分到新项目：

📂 **`D:/Project/myriad-mind-app/`**

- 桌面端：Tauri 2.x (Rust + React)
- 移动端：React Native Expo
- 当前阶段：架构设计完成，待编码
- 有自己的 CLAUDE.md 和 `.claude/` 记忆系统

Claude 可以在这两个项目之间自由切换、对比代码、复用逻辑。

## 常用路径

| 路径 | 说明 |
|------|------|
| `D:/Project/MyClaude/` | MyClaude 项目根目录 |
| `D:/Project/MyClaude/myriad-mind/` | Skill 源码 |
| `D:/Project/MyClaude/大衍决残卷/` | 笔记输出目录 |
| `D:/Project/myriad-mind-app/` | 独立 App 项目 |
| `~/.claude/skills/myriad-mind/` | Skill 部署位置 |
