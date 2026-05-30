# Unreal Engine State Tree 完全入门 — 课程 #1

> 📺 来源：[YouTube TrmXseIPU3k](https://www.youtube.com/watch?v=TrmXseIPU3k) | 作者：LeafBranchGames | 系列：State Tree Course
>
> 💡 点击 ▶ 图标可跳转到视频对应位置 | 英文视频，中英对照翻译

---

## 一、AI 摘要

本视频是 Unreal Engine State Tree 系列教程第一课，系统讲解 State Tree 的核心概念和编辑器界面。

State Tree 是 UE 中一个结合了**行为树（Behavior Tree）**和**状态机（State Machine）**优点的 AI 框架。它既保留了行为树的层级选择逻辑，又引入了状态机的灵活转换能力。

核心内容涵盖：
- **插件启用**：`GameplayStateTree` + `StateTree` 两个插件
- **两种 Schema**：`StateTreeComponent`（运行在 Actor 上，无需 AI Controller）vs `StateTreeAIComponent`（运行在 AI Controller 上）
- **上下文变量（Context Variables）**：自动提供给 Task 的引用（Actor/AIController）
- **参数（Parameters）**：只读配置变量（当前运行时修改有 Bug，可能在未来修复）
- **状态类型**：State、Group、Linked、Linked Asset 四种
- **选择行为**：Try Select Children In Order、Try Enter、Try Follow Transitions、None
- **子树与链接资产**：通过 Linked Asset 实现模块化可复用的 AI 逻辑

---

## 二、核心概念

### 1. State Tree = Behavior Tree + State Machine

```
State Tree 的核心设计哲学：

Behavior Tree（行为树）               State Machine（状态机）
    │                                       │
    ├─ 层级式任务选择                        ├─ 状态间自由转换
    ├─ Selector/Sequence 组合               ├─ Enter/Exit 条件
    └─ 必须运行在 AI Controller 上           └─ 灵活的状态生命周期
                    │                       │
                    └───────────┬───────────┘
                                ▼
                          State Tree
                    （两者结合，即可运行在普通 Actor 上）
```

### 2. 两种 Schema 对比

| 特性 | StateTreeComponent | StateTreeAIComponent |
|------|-------------------|---------------------|
| 运行对象 | Actor（任意） | AI Controller |
| 需要 AI Controller | ❌ 不需要 | ✅ 需要 |
| 上下文变量 | Actor Class | Actor Class + AI Controller Class |
| 适用场景 | 任何需要状态逻辑的对象 | 控制多个 Pawn 的通用 AI |
| 典型用例 | 门/机关/道具行为 | 动物 AI（巡逻+逃跑） |

### 3. State 四种类型

| 类型 | 说明 | 用途 |
|------|------|------|
| **State** | 标准状态，可含子状态 + Task | 绝大多数情况 |
| **Group** | 不含 Task 的 State，纯组织用 | 分类/重定向到子状态 |
| **Linked** | 链接到子树（Sub Tree） | 运行标记为 Sub Tree 的状态 |
| **Linked Asset** | 链接到外部 State Tree 资产 | 模块化复用（推荐） |

### 4. 选择行为（Selection Behavior）

| 行为 | 逻辑 |
|------|------|
| **Try Select Children In Order** | 按顺序尝试进入子状态（= 行为树默认逻辑） |
| **Try Enter** | 仅进入当前状态，不激活子状态 |
| **Try Follow Transitions** | 优先执行转换条件，不启动自身 Task |
| **None** | 不可选择（极少使用） |

### 5. 关键概念：父子状态激活

> 当子状态被激活时，**所有父状态也同时被视为激活**。这意味着父状态的 Task 和子状态的 Task 会并发运行。哪个先完成，哪个就触发 Transition。

---

## 三、详细笔记（按时间顺序）

### [▶ 0:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=0s) - 3:00 | State Tree 简介与插件启用

> [EN] State trees are a combination of State machines and behavior trees.
> [CN] State Tree 是状态机（State Machine）和行为树（Behavior Tree）的结合体。

- 启用插件：`Edit → Plugins`，搜索 `StateTree`，启用两个插件：
  - `GameplayStateTree`
  - `StateTree`
- 重启编辑器后生效
- State Tree 默认行为类似行为树，但提供**更灵活的转换机制**

### [▶ 3:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=180s) - 6:00 | 创建 State Tree + Schema 区别

> [EN] The only difference is the schema that it uses.
> [CN] 唯一区别是它们使用的 Schema（架构）。

- 创建路径：`Artificial Intelligence → State Tree`
- 两种 Schema：
  - **StateTreeComponent Schema**：运行在 Actor 的 Component 上，**不需要 AI Controller**（这是相比行为树的最大优势）
  - **StateTreeAIComponent Schema**：运行在 AI Controller 上，适合多个 Pawn 共享同一控制器的场景
- 可以**随时在编辑器中切换** Schema

### [▶ 6:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=360s) - 9:00 | 上下文变量（Context Variables）

> [EN] Context variables are variables that we can automatically supply into our tasks.
> [CN] 上下文变量是可以自动提供给 Task 的变量。

- `StateTreeComponent`：只有 `Actor Class`
- `StateTreeAIComponent`：有 `Actor Class` + `AI Controller Class`
- **缩小 Actor Class 范围**（如指定为 `StateTreeCharacter`）：可在 Task 中直接访问该类的特定变量
- 保持 Generic（通用）：可在多种 Actor 上复用

### [▶ 9:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=540s) - 12:00 | 参数（Parameters）—— 重要警告

> [EN] These are meant to mostly just be set once and then not be touched anymore.
> [CN] 这些参数设定后基本不应该再被修改。

- Parameters = State Tree 的"配置变量"，类似行为树的 Blackboard
- **⚠️ 重大警告**：运行时设置 Parameters 在打包版本中可能**崩溃**（当前版本 Bug）
- 安全做法：只在编辑器中设置初始值，运行时**只读不写**
- 可以在 Component 上为每个实例设置不同的默认值（如 `Walk Distance = 1500`）

### [▶ 12:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=720s) - 15:00 | 状态类型详解

> [EN] A group is effectively just a state without tasks.
> [CN] Group 实际上就是一个没有 Task 的 State。

- **State**：最常用，含 Task + 子状态 + 转换条件
- **Group**：纯组织结构，重定向到子状态，不含 Task
- **Linked**：链接到**内部子树**（标记为 Sub Tree 的状态）
- **Linked Asset**：链接到**外部 State Tree 资产**（推荐，模块化最佳）
- 颜色主题（Theme）：纯粹的可视化标记，不影响逻辑（如红=愤怒，黄=恐惧）

### [▶ 15:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=900s) - 18:00 | 选择行为 + 父子激活机制

> [EN] When a child state is selected, it also counts as the parent state being selected.
> [CN] 当子状态被选中时，父状态也同时被视为选中状态。

- **Try Select Children In Order**：按顺序尝试子状态 → 行为树默认行为
- **Try Enter**：直接进入当前状态，**跳过所有子状态**
- **Try Follow Transitions**：优先执行转换，有可用转换则不运行自身 Task
- **None**：状态不可选（作者也不知道为什么要用）
- **关键机制**：父状态 + 子状态的 Task **并发运行**，先完成的先触发转换

### [▶ 18:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=1080s) - 22:00 | Sub Tree 与 Linked Asset

> [EN] You can make many more modular small pieces using linked assets.
> [CN] 使用 Linked Asset 可以创建更多模块化的小组件。

- **Sub Tree**：标记某个状态为子树，用 Linked 状态引用
- **Linked Asset**（推荐）：链接到**完全独立**的 State Tree 资产
  - 子树执行完毕（标记 Success/Failure）→ 当前状态标记完成
  - 典型用例：巡逻（Patrol）= 找点 → 走过去 → 等待 → 循环
  - 多个角色共享同一个 Patrol State Tree

### [▶ 22:00](https://www.youtube.com/watch?v=TrmXseIPU3k&t=1320s) - 24:00 | 实战演示：第一个 State Tree

- 创建 `StateTreeCharacter`（Character 子类）
- 添加 `StateTreeComponent`
- 在 State Tree 中设置 Actor Class 为 `StateTreeCharacter`
- 添加 `Debug Text` Task，文本设为 `"hello"`
- 将角色放入关卡，运行即可看到 Debug 文字 → 证明 State Tree 在运行 ✅

---

## 四、关键术语表

| 英文术语 | 中文翻译 | 简要说明 |
|---------|---------|---------|
| State Tree | 状态树 | UE 中结合行为树和状态机的 AI 框架 |
| Behavior Tree | 行为树 | UE 传统的 AI 逻辑框架 |
| State Machine | 状态机 | 状态间按条件转换的逻辑模型 |
| Schema | 架构/模式 | 定义 State Tree 运行的上下文数据类型 |
| Context Variable | 上下文变量 | 自动注入到 Task 中的引用（Actor 等） |
| Parameter | 参数 | State Tree 级别的只读配置变量 |
| Selection Behavior | 选择行为 | 决定如何进入子状态的策略 |
| Transition | 转换/过渡 | 状态之间的跳转条件 |
| Sub Tree | 子树 | 被标记为可被链接引用的状态 |
| Linked Asset | 链接资产 | 引用外部 State Tree 资产作为子状态 |
| AI Controller | AI 控制器 | UE 中控制 Pawn 行为的控制器类 |
| Pawn | 兵卒 | UE 中可被控制的游戏对象基类 |

---

## 五、总结与思考

### State Tree vs Behavior Tree 决策指南

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 需要 AI Controller 控制 Pawn | 都可以 | State Tree 也可以跑在 AI Controller 上 |
| 普通 Actor 需要 AI 逻辑 | **State Tree** | 行为树**必须** AI Controller |
| 高度模块化复用 | **State Tree** | Linked Asset 天然支持 |
| 团队已熟悉行为树 | 渐进迁移 | State Tree 默认行为 = 行为树 |
| 打包项目，参数需运行时修改 | **暂时避免 State Tree** | 当前版本有 Bug |

### 关键要点

1. State Tree = 行为树的层级选择 + 状态机的自由转换
2. **普通 Actor 即可使用**（不需要 AI Controller），这是相比行为树的最大优势
3. Parameters 只读是当前最佳实践，等待 Epic 修复运行时修改的 Bug
4. Linked Asset 是实现模块化 AI 的关键：巡逻/战斗/逃跑各自独立
5. 父状态在子状态激活时**也视为激活**，Task 并发执行
