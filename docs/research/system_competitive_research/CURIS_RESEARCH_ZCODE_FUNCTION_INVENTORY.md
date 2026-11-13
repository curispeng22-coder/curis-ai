# CURIS_RESEARCH_ZCODE_FUNCTION_INVENTORY

> Authority Class: RESEARCH / EVIDENCE (Zcode 产品自我盘点)
> Status: INVENTORY COMPLETE
> Date: 2026-09-12
> Method: 研究者即产品本体（第一人称运行时观察 + 当前会话环境事实 + 官方文档知识）。不涉及逆向工程其他产品。字段级事实均来自运行时可直接观察的能力；无法观察的标 UNKNOWN。

---

## 1. 产品概览

- Zcode 是一个 **AI 编码 / 工作代理（coding agent + general agent）产品**，形态包括：CLI（终端内交互）、Desktop 桌面壳（Electron/Tauri 类宿主，含 sidecar 进程管理）、以及嵌入式集成（IDE 插件生态）。
- 目标用户：开发者优先，但已扩展到一般知识工作（Research / Browser / Computer Use / 文档技能）。
- 核心模型：**单一主 Agent（Main Agent）+ 可派生子 Agent（subagent）**，不是多组织模型。没有"员工/团队/领导"概念；组织语义是 **session → agent → task**。
- 权限模型：运行在用户选择的 permission mode 下；工具调用可被用户实时批准/拒绝。

## 2. App Shell & Navigation

桌面壳（ZCode Desktop）：

| 元素 | 内容 |
|---|---|
| 左侧栏 | 项目 / 会话列表（Session history）、New Session、Project 切换 |
| 顶部 | 项目/工作目录显示、模型指示、模式指示、任务列表（/tasks） |
| 主区 | 会话流（用户消息、agent 回复、工具调用卡、diff 卡、计划卡） |
| 底部/输入 | Composer（多行文本、@文件引用、/斜杠命令、图片粘贴） |
| 全局 | 通知（后台任务完成）、任务通知（task-notification 注入会话） |

CLI 形态：无 GUI shell，全部为终端文本流 + 富文本渲染（markdown、diff、表格）。

## 3. Session / Project 模型（Curis 对照核心）

| Object | 字段（可观察） | 说明 |
|---|---|---|
| Project | 工作目录路径、git 仓库状态、AGENTS.md 指令、配置文件（settings、MCP、hooks） | Project = 工作空间锚点，一切上下文按 Project 解析 |
| Session | 会话 ID、消息历史、todo list、后台任务、MCP 连接、上下文窗口状态 | 会话可 compact（上下文摘要续传）、可 resume |
| Agent | main agent + subagent types（general-purpose、Explore、judge 等），每个 subagent 有独立工具白名单与 system prompt | Agent = 能力封装，不是身份 |
| Mode | permission modes（如 plan mode、auto-approve、默认确认）、plan mode（先探索→出计划→批准→执行） | Mode 改变行为而不改变身份 |

## 4. Conversation & Composer

- 会话流是**线性日志式**：用户消息、助手文本、工具调用卡片（可折叠，显示命令与结果摘要）、计划（ExitPlanMode 的 plan 卡）、todo 渲染。
- Composer：多行输入、`/` 命令（skills 即命令）、`@` 文件引用、图片/视频粘贴、剪贴板读取。
- 消息操作：编辑历史消息重发（分支）、中断（Esc）、继续。
- 上下文管理：自动 compact（长会话摘要）、`/clear`、跨会话 handoff（ReadSessionContext 引用历史会话）。
- 通知：后台任务完成后以 task-notification 注入；桌面通知由壳层处理（具体开关字段 UNKNOWN — 由宿主系统设置控制）。

## 5. Agent 工作与进度（Curis Agent Progress Matrix 对照核心）

- **Todo list**：agent 主动维护任务清单（content/status/priority），实时渲染为 checklist —— 用户可见"正在做什么/还剩什么"。
- **工具卡**：每次工具调用产生独立卡（描述、参数摘要、结果），可展开 —— 过程透明但密集。
- **计划模式**：探索 → 计划卡（含 allowedPrompts 权限预算）→ 用户批准 → 执行。
- **后台任务**：可并行 run_in_background 的 shell/agent，完成时通知。
- **Progress**：无独立"工作台"页面；进度全部内联在会话流中。**这是与 Curis 最关键的形态差异：Zcode 把过程塞进对话流，Curis 则把 Work/Result 分离成对象。**

## 6. Research / Browser / Computer 能力

| 能力 | 内容 |
|---|---|
| WebSearch | 内置搜索工具，返回结果块，要求末尾列 Sources |
| WebFetch | URL → markdown → 小模型按 prompt 提取答案；15min 缓存 |
| Browser Use | 主 agent 专用技能：Node 内核驱动真实浏览器（导航、截图、点击、填表、验证），技能文件约束使用方式 |
| Computer Use | 桌面控制：accessibility-first（读 UI 树、语义点击、set_value），截图仅兜底；应用启动、窗口管理、剪贴板 |
| 文件 | Read（含图片/视频可视化）、Write、Edit（精确替换）、Glob/Grep 式搜索、专用工具优先于 shell |
| 任务编排 | Agent 工具派生 subagent（general-purpose / Explore 只读 / judge 视觉验收），后台并发 |

## 7. Skill / MCP / Tool / Permission 体系

- **Skills**：目录化能力包（SKILL.md + 资源），用户可安装/禁用；按触发条件自动匹配或 `/命令` 显式调用；插件可携带 skills。**有"技能市场"语义（plugin marketplace），含启用/禁用、版本缓存、来源（官方/本地）。**
- **MCP**：stdio/HTTP server 接入，工具命名空间 `mcp__server__tool`；配置在用户/项目两级；有诊断技能（diagnosing-mcp）。
- **Hooks**：工具调用生命周期钩子（PreToolUse 等），输出可作为用户反馈注入。
- **Permission**：permission mode + 每次调用可询问；`allowedPrompts` 在计划中预申报权限（如 "run tests"）；沙箱模式（sandbox）可用。
- **模型**：主模型 + 快速小模型（WebFetch 内部）；模型由会话选择，无 per-tool 模型绑定。

## 8. Settings（字段级盘点）

Zcode 配置面按作用域分层（项目 < 用户 < 企业策略），实际设置项：

| 类别 | 字段 |
|---|---|
| Agent/Model | 模型选择、系统提示注入（AGENTS.md）、思考预算（thinking level）、上下文策略（compact 阈值） |
| Permissions | permission mode 默认值、allowlist 工具与命令、sandbox 开关、hook 规则 |
| MCP | server 列表（command/url/env/headers）、启用/禁用、作用域 |
| Skills/Plugins | 已安装插件、marketplace 来源、skill 启用状态、skill 冲突优先级 |
| Editor/显示 | 主题、markdown 渲染、diff 渲染方式、终端集成 |
| Notifications | 后台任务通知、任务完成通知渠道 |
| Privacy | 遥测、会话数据保留 |
| 更新/关于 | 版本、渠道 |

注：部分设置项为推测性归纳（UNKNOWN 标记的排除），CLI 与 Desktop 的设置面不完全一致。

## 9. Desktop-specific 能力

- sidecar 进程管理（宿主拉起/监护 agent 进程，readiness gate 超时控制）。
- 本地文件系统全量访问（受权限门控）、git 集成（status/diff/commit 语义内置）。
- Keychain/凭证由宿主系统处理。
- 无自己的浏览器内核——复用系统 Chrome + CDP（Browser Use 技能）。

## 10. States（状态呈现）

| 状态 | 呈现方式 |
|---|---|
| Working | 会话流内联工具卡连续产生；无独立进度页 |
| Streaming | 文本流式输出 |
| Waiting approval | 工具卡内嵌批准按钮 / permission 提示 |
| Error | 工具卡错误结果 + agent 自行重试或报告 |
| Background done | task-notification 消息注入 |
| Compact | 系统级摘要替换历史（用户可见提示） |

## 11. 视觉观察（APPROXIMATE，基于桌面壳与终端渲染）

- 终端形态：等宽字体、低密度信息、diff 语法高亮、卡片用边框/缩进而非阴影。
- Desktop 壳：暗色优先、单窗口、左窄栏 + 主流式区，视觉语言接近 IDE 而非办公软件。
- 无品牌紫色大面积使用；强调色克制。

## 12. OBSERVATION → PATTERN → CURIS GAP 笔记

| # | OBSERVATION | PATTERN | CURIS GAP（候选，仅记录） |
|---|---|---|---|
| Z1 | Todo list 作为 agent 工作进度的第一公民 | 进度 = 结构化任务清单，而非日志 | Curis Work 执行进度若只以日志流呈现，用户无法一眼看到"计划 vs 完成" |
| Z2 | 工具调用卡片化、可折叠 | 过程透明但要可降密度 | Curis Conversation 若全量铺开 employee 工具流会像日志（这正是 CEO 担心的"Conversation 像日志"） |
| Z3 | 计划模式：先出计划+权限预算再执行 | 执行前对齐机制 | Curis Work 缺少"执行前计划确认"产品面（Runtime 有无对应机制 UNKNOWN） |
| Z4 | 权限白名单 + allowedPrompts 预申报 | 能力授权显式化、可预期 | Curis Employee 执行授权目前按 scope 模型，缺用户可理解的"这个员工能做什么"清单面 |
| Z5 | Skill = SKILL.md 目录包 + 触发条件 + /命令 | 能力包可组合、可安装、有市场 | Curis Skill 已有安装/绑定，但缺"技能如何被触发/什么时候用"的用户语言（CURRENT_STATE P1: Capability 用户语言） |
| Z6 | 后台任务 + 完成通知注入 | 并行工作不阻塞会话 | Curis 多员工并行 Work 的通知/聚合呈现缺产品面 |
| Z7 | 会话 compact / handoff | 长会话可持续性 | Curis Conversation 长期经营的记忆/摘要机制 UNKNOWN |
| Z8 | 单主 agent + 派生 subagent，无组织语义 | 工具型组织，不是公司型组织 | Curis 的 Employee/Team/Leader 模型在组织语义上 **领先** Zcode；但 Zcode 的执行透明度（工具卡/计划/权限）远成熟 |

---

## Sources

- 本体运行时观察（Zcode 当前会话：系统提示、工具清单、技能清单、配置面）。
- Zcode 官方文档知识（训练语料内）；本地 `AGENTS.md` 与 `.agents/skills/`、`.zcode/` 配置结构为项目级证据。
