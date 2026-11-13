# Curis Research — Cursor（Anysphere）Function Inventory

- **Status**: Draft
- **Authority Class**: RESEARCH（仅为竞品研究证据，不构成 Curis 任何 Authority，不得用于改写 Product Blueprint / Master Map）
- **Date**: 2026-09-12
- **Scope**: Cursor 桌面应用（Editor + Agents Window 双界面）为主，覆盖 Agent 面板、Chat surfaces、Agent 能力、模型、Worktree/Workspace、结果评审、Settings 全量清单、Automations、运行状态、视觉观察，以及 OBSERVATION → PATTERN → CURIS GAP 记录。
- **Method**: 官方文档（cursor.com/docs、cursor.com/help、cursor.com/changelog、cursor.com blog、cursor.com/pricing、cursor.com 首页）为主，官方论坛（forum.cursor.com）与第三方报道为辅。逐节标注来源 URL。无法从来源确认的字段标 `UNKNOWN`；凭截图/间接证据推断的字段标 `APPROXIMATE`。
- **Note**: 本文只做 OBSERVATION → PATTERN → CURIS GAP 记录，**不决定** Curis 架构。
- **Time context**: 研究时点（2026-09）Cursor 最新版本为 3.x 系列（Cursor 3 于 2026-04-02 发布，Agents Window GA；Cursor 2.0 于 2025-10-29 发布多 Agent 界面与 Composer 模型；2026-08 Cursor 宣布并入 SpaceX）。

---

## 1. Overview（产品概览）

### 1.1 Cursor 是什么

- 官方定位（首页原文）："**Cursor is your coding agent for building ambitious software**"，出品方为 Anysphere, Inc.，自称"an applied research team focused on building the future of software development"。
- 本质是一个 **AI-native 的 VS Code 系代码编辑器**：与 VS Code 共享默认快捷键、设置、主题，使用 **Open VSX** 扩展市场（不是微软 Marketplace），一键导入 VS Code 的 extensions / themes / settings / keybindings。【来源：cursor.com/help/getting-started/migrate-vscode】
- 2025-10 Cursor 2.0 起，产品从"编辑器为中心"转向"**Agent 为中心**"：新界面 "centered around agents rather than files"，可随时切回 classic IDE。【来源：cursor.com/blog/2-0】
- 2026-04 Cursor 3：**Agents Window** GA，成为"agent-first interface"，与 Editor 并列的第二种主界面。【来源：cursor.com/docs/agent/agents-window】
- 2026-08-14 官方博客宣布 "Cursor is now a part of SpaceX"；Composer 模型与 SpaceXAI 联合训练。【来源：cursor.com 首页、cursor.com/docs/models-and-pricing】

### 1.2 产品形态矩阵

| 形态 | 平台 | 说明 |
|---|---|---|
| Desktop IDE | macOS（首页明示 "Download for macOS"；Windows/Linux 下载存在但首页未点名，标 APPROXIMATE） | VS Code 系；Editor + Agents Window 双界面 |
| CLI | 终端（`curl https://cursor.com/install -fsS \| bash`） | 可 headless、ACP、GitHub Actions |
| Web | cursor.com/agents（Android 走 Chrome PWA "Install App"） | 云端 Agent 管理 |
| Mobile | iOS 原生 app（iOS 26.0+ / iPadOS 26.0+，英语）；Android "planned" | 云 Agent 追踪/跟进/PR review |
| Integrations | Slack（@cursor）、GitHub/GitLab/Bitbucket/Azure DevOps（PR/issue 评论 @cursor）、Linear（@cursor）、Microsoft Teams、Jira、Notion | |

【来源：cursor.com 首页、cursor.com/docs/cloud-agent、cursor.com/docs/cloud-agent/mobile】

### 1.3 定价（官方口径）

| Plan | 价格 | 要点 |
|---|---|---|
| Hobby | 免费 | 有限 Agent 请求；可用 Composer |
| Start | ₹649/月（仅印度） | 仅 Cursor Models，固定 medium effort，不可 Fast |
| Pro（Individual） | $20/月 | 更高 Agent 上限、frontier 模型、Cloud Agents、MCP/skills/hooks |
| Pro+ | $60/月 | 高频 Agent 用户 |
| Ultra | $200/月 | 高强度用户 |
| Teams Standard | $40/用户/月 | 中央计费、admin 控制、Team marketplace（rules/skills/plugins）、共享上下文云 Agent、automations、Bugbot、团队隐私模式、SAML/OIDC SSO |
| Teams Premium | $120/用户/月 | 5x Standard Agent 上限 |
| Enterprise | 定制 | 池化用量、发票/PO、SCIM、repo/模型/MCP 访问控制、auto-run/browser/network 控制、audit logs、service accounts、AI code tracking API |

- **Usage-based pricing**：每个 plan 含一定模型用量，超出后按需计费（in arrears），按各模型 API 价率；Teams/Enterprise 对第三方模型请求加收 **Cursor Token Rate $0.25/M tokens**（含 Auto 路由与 BYOK）。【来源：cursor.com/pricing、cursor.com/docs/models-and-pricing】
- Cloud Agent 计费按 API 价率按 token 计（首次使用时设置 spend limit）。【来源：cursor.com/docs/cloud-agent】
- Max Mode（legacy plans）按 API 价 +20% 计费。【来源：cursor.com/docs/models-and-pricing】

---

## 2. App Shell & Navigation（应用外壳与导航）

### 2.1 双界面模型（Cursor 3+ 最重要结构事实）

Cursor 桌面端有**两个并列的主界面**，可同时保持打开：

| 界面 | 打开方式 | 定位 |
|---|---|---|
| **Editor（IDE）** | `Cmd+Shift+P` → "Open IDE"（从 Agents Window 切回） | 经典 VS Code 式编辑：扩展、分屏、多文件并览 |
| **Agents Window** | `Cmd+Shift+P` → "Open Agents Window" | agent-first：跨 repo 管理多个并行 agent、diffs view、cloud agents |

【来源：cursor.com/docs/agent/agents-window】

### 2.2 Editor 外壳（VS Code 派生，标 APPROXIMATE）

以下为 VS Code 基础外壳元素，Cursor 继承（官方文档不逐项描述，标 **APPROXIMATE**，依据 migrate-vscode 页"shares the same default shortcuts as VS Code"与 VS Code 常识）：

- **Activity Bar**（最左竖条：Explorer / Search / Source Control / Run / Extensions + Cursor 注入的入口）
- **Sidebars**（Primary sidebar + Secondary sidebar）
- **Editor area**：多 tab、多 group 分屏、breadcrumbs
- **Panels**：Terminal（`Ctrl+\``）、Output（`Cmd+Shift+U`，含 "MCP Logs"、"Worktrees Setup" 等专属 channel）、Problems、Debug Console
- **Command Palette**：`Cmd/Ctrl+Shift+P`（官方文档多处用它启动功能，如 "Open Agents Window"、"Terminal: Select Default Profile"）
- **设置 UI**：VS Code 风格 Settings UI + settings.json；Cursor 另有自己的 **Cursor Settings**（`Cmd/Ctrl+Shift+J`）独立面板（见 §8）
- **底部状态栏**：含 **Tab 状态指示器**（右下角，点击直达 Tab 设置）【来源：cursor.com/help/ai-features/tab】

### 2.3 Cursor 注入的导航/入口

| 入口 | 快捷键 / 路径 | 说明 |
|---|---|---|
| Agent 面板（side pane） | `Cmd+I` | 本地 Agent 主界面 |
| Agent/Chat（以选区为上下文） | `Cmd+L`（选中代码后） | 打开 Agent 并携带选区 |
| Inline Edit | `Cmd+K` | 行内编辑（见 §3.2） |
| Cursor Settings | `Cmd+Shift+J` | 独立于 VS Code Settings 的产品设置 |
| Agents Window | `Cmd+Shift+P` → "Open Agents Window" | 多 Agent 界面 |
| Agents Window 内文件查找 | `Cmd+P`（单文件）/ `Cmd+Shift+F`（全局搜索） | 不离开 Agents Window 查看/编辑文件 |
| Mode 切换 | `Shift+Tab`（chat input 内轮换模式） | Agent/Ask/Plan/Debug 轮换；input 内也有 mode picker dropdown |
| Side Chat | `/side` 或 `Shift+Cmd+S`（Win：`Shift+Ctrl+S`） | 子对话（见 §3.6） |
| 键盘哲学 | — | 继承 VS Code 全套 keybindings + Cursor 专属快捷键；"keyboard-first" 体现在 Tab 接受补全、Shift+Tab 切模式、Cmd+Enter 插队、Enter 队列等密集键盘交互 |

【来源：cursor.com/docs/agent/overview、cursor.com/docs/agent/agents-window、cursor.com/help/customization/keyboard-shortcuts】

---

## 3. Chat Surfaces（对话/交互面）

### 3.1 Agent 面板（本地 Composer/Agent）

- 位置：Editor side pane（`Cmd+I`）；结构为 **Instructions（system prompt + rules）+ Tools + Model** 三件套；无每任务 tool-call 次数硬上限。【来源：cursor.com/docs/agent/overview】
- **消息队列（Queue）**：Agent 工作中可继续输入，`Enter` 入队；队列消息显示在当前任务下方、**可拖拽排序**、按序执行。`Cmd+Enter` = "send immediately, bypassing the queue"，消息附着到最近一条 user message 并追加到 tool results。**Steer**：点 "Send now" 或按两次 `Enter`，在下一个 tool call 边界送达（cursor.com/agents 已有，Agents Window 滚动发布；**Tab** 把消息排到本轮结束后）。【来源：cursor.com/docs/agent/overview】
- **/goal**：设定长生命周期目标（如 `/goal fix all flaky tests and make CI green`），Agent 持续工作直到完成；可与 Custom Modes 和内置 `/loop` skill 组合（滚动发布）。【来源：cursor.com/docs/agent/overview】
- **Plan Mode**：Agent 先提澄清问题 → 研究 codebase → 生成可编辑的实施 plan（chat 内或 markdown 文件）→ 点击 "build" 执行。Plan 默认存 home 目录，可 "Save to workspace"。`Shift+Tab` 可切到 Plan；prompt 复杂时自动建议 Plan Mode。【来源：cursor.com/docs/agent/plan-mode】
- **Debug Mode**：针对难复现 bug，收集运行时证据（第四种内置模式）。【来源：cursor.com/help/ai-features/agent】
- **Custom Modes**：自定义模式（2026-08 改为 pinned "always on" skills 形态）。【来源：cursor.com/changelog、cursor.com/docs/agent/overview】
- **Side Chats（子对话）**：`/side` / 选中 chat 内文本或 diff → "Ask in Side Chat" / `Shift+Cmd+S`。挂在父 agent 上、用父线程历史作隐藏参考上下文、有自己的可见 transcript；默认偏只读（读/搜/答）；follow-up 不回流父线程；**不是 fork**（fork 才是复制对话）；用 `@` 在主线程引用 side chat 拉回上下文；点 X 归档不删除；不可嵌套；Cloud Agents 暂不支持。【来源：cursor.com/help/ai-features/side-chats】

### 3.2 Inline Edit（Cmd+K）

1. 选中代码 → `Cmd/Ctrl+K` → 输入指令 → `Return` 原地应用；
2. 可继续追加 follow-up 指令再 `Return` 迭代；
3. **Quick Question**：`Opt/Alt+Return` 切换为提问模式（只问不改）；要采纳建议时输入 "do it" 再 `Return`；
4. 复杂/多文件编辑：选中代码按 `Cmd/Ctrl+L` 转入 Agent。
- User Rules 明确**不**应用于 Inline Edit。【来源：cursor.com/help/ai-features/inline-edit、cursor.com/docs/rules】

### 3.3 Tab Autocomplete

- 基于最近编辑、上下文代码与 linter 错误生成补全，以**灰色 ghost text** 显示在光标前方。
- 快捷键：`Tab` 接受全部；`Esc`（或继续打字）拒绝；`Cmd/Ctrl+→` 逐词接受；可在 Keyboard Shortcuts 里搜 "Accept Cursor Tab Suggestions" 改键。
- **Jump-in-file**：接受后按 `Tab` 跳到预测的下一个编辑位置；跨文件编辑会"在编辑器底部出现 portal window"跳到另一文件。
- 支持多行编辑、补 import、跨文件联动修改。
- 设置：右下角 Tab 状态指示器，或 Cursor Settings > **Tab**：**Snooze**（限时关闭）、**Disable globally**、**Disable per extension**（如 markdown/JSON）。
- Rules 不影响 Tab。【来源：cursor.com/help/ai-features/tab、cursor.com/docs/rules】

### 3.4 Chat Modes 汇总

| Mode | 能否改文件 | 用途 |
|---|---|---|
| **Agent** | 是 | 默认；建功能/重构/修 bug；可派 subagents |
| **Ask** | 否（只读） | 理解代码、探索架构 |
| **Plan** | 批准 plan 后可 | 先审方案再动手 |
| **Debug** | 是 | 难复现 bug，取运行时证据 |
| （历史）**Manual** | 是 | 旧版手控编辑模式；现文档已不列（标 APPROXIMATE：仅存于旧版本/论坛） |
| **Custom Modes** | 自定 | 用户自建模式（现与 pinned skills 合流） |

- 切换：`Shift+Tab` 轮换或 mode picker dropdown；**每个 mode 独立上下文**（切换即新 context window）；Project/User/Team Rules 在所有 mode 均生效。【来源：cursor.com/help/ai-features/agent、cursor.com/docs/agent/plan-mode】

### 3.5 Cloud Agents（原 Background Agents）与多端

- 定义：与本地 Agent 同一套 fundamentals，但跑在隔离 VM（完整 dev 环境：克隆 repo、依赖、secrets、启动命令、网络）。
- 启动入口（官方枚举）：**Cursor for iOS**、**Cursor Web**（cursor.com/agents）、**Cursor Desktop**（agent input 下方 dropdown 选 **Cloud**）、**Slack**（`@cursor`）、**GitHub/Bitbucket**（PR/issue 评论 `@cursor`）、**Linear**（`@cursor`）、**API**。
- 管理员需先接入 source control（GitHub/GitLab/Bitbucket Cloud/Azure DevOps）；2026-08 起支持**无 repo 起步**（先 prompt 后存入 Cursor Origin repo，浏览器端口转发预览，Vercel 发布）。
- Agent 在独立分支工作，完成后 push 回 repo 交接；环境可由 agent 引导配置、snapshot 或 `.cursor/environment.json` + Dockerfile 定义；"Builds" 后台准备环境。
- **Remote desktop control**：可接管云端 agent 的桌面进行测试再交还；移动端可把桌面 session 交给云 agent loop（`/remote-control`，工具调用仍留在本机）。
- **Artifacts**：截图、视频、日志；模型为精选集合，可选 context window 大小。
- 分享：agent URL 分享后为只读，需 repo 权限；admin 可开 **team follow-ups**。
- 【来源：cursor.com/docs/cloud-agent、cursor.com/changelog】

### 3.6 Mobile App（iOS/iPad）

- 追踪云 Agent：实时 chat 流、follow-up、**subagent cards**（点开看子 transcript）；锁屏 **Live Activities / Dynamic Island** 最多追踪 8 个 agent；agent 结束一轮有 push 通知。
- PR review/merge：读 diff/commits/deployments/approvals/comments/checks；改 reviewer、让 agent 修 comment 或挂掉的 check、squash merge、auto-merge 开关、mark ready、update branch、publish、close。
- 语音听写（live transcription）；Design Mode（贴图/截图上指点、圈画）；每 run 可选 MCP servers；cache-first 打开。
- iPad：sidebar 多 agent 并览、side-by-side review、全宽 diff、Apple Pencil 圈画。
- 跨设备：任何端启动的 agent 自动出现在移动 inbox；`Move to Cloud` 把本地 IDE session 推上云；移动端启动的 agent 在桌面 Cloud Agents panel 显示并带 `source: iosApp` 标记。
- 【来源：cursor.com/docs/cloud-agent/mobile】

### 3.7 多 Agent 并行

- Editor 内：多 agent 同时跑，靠 **git worktrees 或 remote machines** 隔离互不干扰；官方称"多模型同时做同一问题再选最优"显著提升结果。【来源：cursor.com/blog/2-0】
- `/best-of-n sonnet,gpt,composer <task>`：同一任务跨多模型各开一个 worktree 并行跑，只比较、由用户选胜者并自行 apply/commit。【来源：cursor.com/docs/configuration/worktrees】
- Agents Window：multi-workspace、并行 cloud agents、local↔cloud handoff、`/in-cloud`（下一任务交给云 VM/分支）、`/autopilot`（PR 交给云 agent 自主迭代到 merge）。【来源：cursor.com/docs/agent/agents-window、cursor.com/docs/subagents】
- **Cursor Projects**（2026-09-10，beta）：面向更大工程的协调层——coordinator agent 规划并"delegates it to agents that implement it"，可运行数千 subagents；云端执行、跨机共享上下文、订阅 Slack 频道/定时/PR 监控。【来源：cursor.com/changelog】

---

## 4. Agent Capabilities（Agent 能力）

### 4.1 内置 Tools（官方枚举名）

| Tool | 行为 |
|---|---|
| **Search files and folders** | 按名搜索、读目录结构、找关键词/模式（底层为 "Instant Grep"，自称大 repo 上快于 ripgrep，自动运行） |
| **Web** | 生成查询并执行 web 搜索 |
| **Fetch Rules** | 按类型与描述取用 rules |
| **Read files** | 读文件；支持图片（.png/.jpg/.gif/.webp/.svg）供视觉模型 |
| **Edit files** | 建议并自动应用编辑 |
| **Run shell commands** | 执行命令并监控输出 |
| **Browser** | 截图、测 app、验证视觉改动；导航页面并与元素交互 |
| **Image generation** | 文生图/参考图生成；默认存 `assets/`，chat 内联展示 |
| **Ask questions** | 澄清提问；等待回复期间 agent 继续干活 |
| **Canvas / Terminal / Browser tools** | 另有独立文档页（terminal profile 可经 "Terminal: Select Default Profile" 选择） |

【来源：cursor.com/docs/agent/overview、cursor.com/docs/agent/tools/search】

### 4.2 权限（Run Modes / Approvals & Execution）

- 配置位置：**Cursor Settings > Agents > Approvals & Execution**（桌面端）。

| 模式 | 行为 | Sandbox | Classifier |
|---|---|---|---|
| **Auto-review** | allowlist 内立即执行；其余 shell 命令尽量进 sandbox；不能 sandbox 的交给 classifier 判定 | 有（shell） | 有（Claude 4.5 Haiku 或 GPT-5.4 Mini，Cursor 托管） |
| **Allowlist** | 仅 allowlist 动作自动执行；支持的 shell 命令可 sandbox | 可选 | 无 |
| **Run Everything** | 所有 tool call 自动执行 | 无 | 无 |

- v3.5（2026-05-22）弃用 **Ask Every Time** 与 **Run in Sandbox** 两个旧模式（分别并入空 allowlist 的 Allowlist 与启用 sandbox 的 Allowlist）。
- **permissions.json**（`~/.cursor/permissions.json` 全机 + `<project>/.cursor/permissions.json` 项目，两 scope 合并）：字段为 `allow_instructions` / `block_instructions`——**自然语言指令**（如 "Every AWS CLI command should go through approval first."）；可直接叫 agent 改它。
- **sandbox.json**（同两级位置，project 优先）：网络域名、额外可读写路径、临时目录写、共享 build cache。团队策略与硬编码规则本地不可削弱。
- **Sandbox 默认**：workspace 可读写；受保护路径（`.git/config`、`.git/hooks`、`.vscode`、`.cursorignore`、Cursor 敏感配置）；网络默认封禁（三档：sandbox.json Only / sandbox.json + Defaults（默认）/ Allow All）；`/tmp` 可写。macOS 用 Seatbelt（`sandbox-exec`）；Linux 用 Landlock+seccomp（kernel 6.2+）。
- **Layered hard protections**（无论何种 mode 都强制审批）：**Browser Protection**（Browser tool 不自动跑）、**File-Deletion Protection**（阻止自动删除含 `rm`）、**External-File Protection**（阻止 workspace 外自动写）。
- **Enterprise**：web dashboard 控制用户可用 mode、sandbox 网络规则、全队 Auto-review 配置；团队设置优先于个人/项目配置；"Auto-review is not a security boundary"（官方原话）。
- MCP tool 调用走同一 Run Modes（Auto-review 模式下 allowlisted MCP 工具立即跑，其余过 classifier）。
- 【来源：cursor.com/docs/agent/security/run-modes、cursor.com/docs/mcp】

### 4.3 Checkpoints

- 在"显著改动之前"对 codebase 拍快照，覆盖所有被改文件；chat timeline 中点击 checkpoint 即可预览与 restore。
- UI：历史请求上的 **Restore Checkpoint** 按钮；hover 消息时的 **+ 按钮**。
- Restore 只回滚**文件**，消息保留在对话里；checkpoint 存本地、独立于 Git、明确"不用于永久版本控制"。【来源：cursor.com/docs/agent/overview】

### 4.4 结果评审（Diffs / Accept-Reject / Agent Review）

- Agent 改动以 diff 呈现（编辑器内 diff + Agents Window 的 **New diffs view**——不离开 Cursor 即可 review/commit/manage PR）。
- **Agent Review**（Bugbot 内置版）：Cursor Settings > Agents > "Agent Review"（Cursor 3.11 起移到 Git & PRs > Pull Requests）；规则来自 repo 里的 **BUGBOT.md**。触发方式：**Automatic**（启用后每次 commit 后自动跑）、slash 命令 **`/agent-review`**、**Source Control tab**（对比本地全部改动 vs main）。深度档位：**Quick**（快/便宜，小 diff）与 **Deep**（慢/贵，复杂逻辑/安全敏感/大重构）。【来源：cursor.com/docs/agent/agent-review、cursor.com/docs/agent/agents-window】
- 移动端 PR review/merge 见 §3.6。【来源：cursor.com/docs/cloud-agent/mobile】

### 4.5 Subagents（子代理）

- 主 agent 可委派专用 AI 助手；各在**独立 context window** 中运行，结果回传。覆盖 editor、CLI、Cloud Agents。
- 执行模式：**Foreground**（阻塞父 agent 等结果）/ **Background**（立即返回，独立跑）。
- **内置三个**（无需配置自动使用）：**Explore**（代码库搜索分析，用快模型做约 10 路并行搜索）、**Bash**（串 shell 命令并隔离冗长输出）、**Browser**（经 MCP 控制浏览器，过滤 DOM/截图噪声）。
- 调用：自动委派（按 description）；显式 `/name`（如 `/debugger investigate this error`）或自然语言点名；并行（"…in parallel" 触发多个 Task tool 调用）；隔离副本（本地 git worktree 或专属云 VM/分支，防文件编辑冲突）；**Cloud**：`/in-cloud`、`/autopilot`；**Resume**：每次执行返回 agent ID，可 "Resume agent abc123…"。
- 配置文件：`.cursor/agents/`（项目）、`~/.cursor/agents/`（用户），兼容 `.claude/agents/` 与 `.codex/agents/`；项目覆盖用户，`.cursor/` 赢同名冲突。格式：markdown + YAML frontmatter，字段：`name`、`description`、`model`（默认 `inherit`，支持括号参数如 `claude-opus-5[effort=high,context=300k]`）、`readonly`（默认 false，挡文件编辑与状态变更命令）、`is_background`（默认 false）。
- 限制：2.5 起 subagent 可再开 subagent 但**只许一层**嵌套；MCP 工具继承父级（cloud subagent 例外）；background subagent 输出写 `~/.cursor/subagents/` 供父级读进度。
- 成本警告：5 个并行 subagent ≈ 5x token。
- 【来源：cursor.com/docs/subagents】

### 4.6 MCP

- 配置位置：项目 `.cursor/mcp.json`；全局 `~/.cursor/mcp.json`；另可经扩展 API `vscode.cursor.mcp.registerServer()` 动态注册。
- **配置字段**：
  - STDIO：`type`（必填，"stdio"）、`command`（必填，PATH 或全路径）、`args`、`env`（支持插值）、`envFile`（仅 STDIO）；
  - Remote（HTTP/SSE）：`url`、`headers`（如 `"Authorization": "Bearer ${env:MY_SERVICE_TOKEN}"`）、`auth`（静态 OAuth 对象）；
  - 插值语法：`${env:NAME}`、`${userHome}`、`${workspaceFolder}`、`${workspaceFolderBasename}`、`${pathSeparator}` / `${/}`，作用于 `command/args/env/url/headers`。
- **OAuth**：`auth` 对象字段 `CLIENT_ID`（必填）、`CLIENT_SECRET`（可选）、`scopes`（可省，经 `/.well-known/oauth-authorization-server` 发现）；固定 redirect URL：Web/Agents `https://www.cursor.com/agents/mcp/oauth/callback`、Desktop `http://localhost:8787/callback`。
- 协议支持：Tools、Prompts、Resources、Roots、Elicitation、**MCP Apps 扩展**（工具可返回交互式 UI）。
- 管理 UI：**Customize** 页；一键安装经 **Cursor Marketplace**；Customize 中 toggle 启停（禁用即不加载）；调试经 Output panel（`Cmd+Shift+U`）→ "MCP Logs"。
- 审批：默认逐次询问（点工具名旁箭头可看参数）；Auto-review 下 allowlisted MCP 工具自动跑；**Enterprise MCP Allowlist**：命令模式批 stdio、URL 模式批 remote、per-server 工具 allowlist（空=全部允许）；per-server 网络控制（Allow all / Allowlist / Deny all / No sandbox）+ User MCP Network Denylist。
- 团队分发：Dashboard > Integrations & MCP 共享 Team MCP servers；"Add to Team Marketplace"。
- 行为：自动按需调用 `Available Tools`（含 Plan Mode）；chat 内可展开参数/响应；可返回 base64 图片进 chat；单 server 崩溃不拖累其他 server。
- 【来源：cursor.com/docs/mcp】

### 4.7 Rules（规则系统）

| 类型 | 存放 | 管理入口 | 备注 |
|---|---|---|---|
| **Project Rules** | `.cursor/rules/*.mdc`（必须 .mdc，纯 .md 被忽略） | 版本控制 | 支持 nested |
| **User Rules** | 全局 | **Customize → Rules** | 仅 Agent/Chat 生效；**不适用于 Cmd+K Inline Edit** |
| **Team Rules** | Dashboard 管理 | Team/Enterprise | 自由文本 + glob；可强制成员不可禁用 |
| **AGENTS.md** | 项目根（可子目录嵌套） | 普通 markdown | 与父级指令合并，更具体者优先 |

- **应用行为四档**（frontmatter 组合决定）：
  - `alwaysApply: true` → **Always Apply**（每会话注入）；
  - `alwaysApply: false` + `globs` → **Apply to Specific Files**（匹配文件进上下文时附加）；
  - `alwaysApply: false` + `description` → **Apply Intelligently**（Agent 按 description 自取）；
  - 均无 → **Apply Manually**（仅 `@rule` 引用）。
- frontmatter 字段名：`alwaysApply`、`description`、`globs`（逗号分隔 glob）。
- 创建：chat 内 `/create-rule`，或 Customize → Rules → Add Rule（可从 GitHub 导入 Remote Rules 到 `.cursor/rules/imported/<repoName>`）。
- **优先级：Team Rules → Project Rules → User Rules**（合并，前者冲突胜出）。
- 最佳实践：单条 <500 行、拆分、用 `@filename` 引用、不重复 linter 已知规则、入库；Rules 不影响 Tab。
- 【来源：cursor.com/docs/rules】

### 4.8 Memories（记忆）

- AI 在工作中**自动保存**重要上下文为 memory；可让 AI "记住" 某信息自动入档。
- 管理位置：**Settings > Rules & Memories**（新版；旧版在 Rules 下）——查看、编辑、删除每条 memory。
- 与 Rules 的区别：rules 是用户手写指令，memories 是自动生成的情境记忆（官方论坛确认 memory 非 project-specific，即目前是**用户级**而非项目级——社区反馈点）。【来源：forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149】
- Automations 场景：memories 作为工具跨 run 持久化（默认存 **MEMORIES.md**，默认开启可关，可在工具配置 UI 编辑；官方警示不可信输入可注入虚假 memories）。【来源：cursor.com/docs/cloud-agent/automations】
- 字段级细节（memory 条目结构、上限、触发策略）：**UNKNOWN**（官方文档未公开）。

### 4.9 Context（@-mentions、索引、Docs）

- **@-mentions 官方清单**：
  - `@file` / `@folder`（选中文件夹后打 `/` 可继续下钻）
  - `@Terminals`（终端输出作上下文）
  - `@Chats`（历史对话作上下文）
  - `@Commit (Diff of Working State)`（未提交改动）/ `@Branch (Diff with Main)`（整分支 diff）
  - `@Browser`（内置浏览器上下文）
  - （历史版本还有 `@Docs`、`@Web`、`@Code`、`@Rules` 等——现帮助页未列，标 APPROXIMATE）
- 官方指引：已知相关文件就 mention（如组件+测试一起）；不确定就别提，Agent 自己搜。【来源：cursor.com/help/customization/context】
- **Codebase indexing（历史机制）**：本地 chunk → 服务器 embedding → **Merkle tree（SHA-256 per 文件/目录哈希）** 增量同步（约每 5 分钟）；`.cursorignore` 排除文件（`.env`、`.git/` 默认忽略）。**新版已移除 codebase indexing 设置 UI**，转向本地检索（Instant Grep 等），语义索引 deprecated。【来源：cursor.com/blog/secure-codebase-indexing、forum.cursor.com/t/what-do-you-think-about-cursor-removing-the-codebase-indexing-settings/165899、cursor.com/help/customization/ignore-files】
- 现行检索：**Instant Grep**——Cursor 自研搜索引擎，"outperforms ripgrep on large codebases"，自动运行无配置。【来源：cursor.com/docs/agent/tools/search】

---

## 5. Models（模型）

### 5.1 模型选择器

- 双池结构：**Cursor Models**（第一方：Grok 4.6 / Grok 4.5 / Composer 2.5，各带 Fast 变体；与 SpaceXAI 联训）与 **Other Models**（第三方按 API 价率：Anthropic Claude 系、Google Gemini 3.x、OpenAI GPT-5.x 系（含 5.6 Sol/Terra/Luna、Codex）、Moonshot Kimi K2.7/K3、Z.ai GLM 5.2、Meta Muse Spark 1.3）。两池每月重置。
- 部分模型 "Hidden by default"，需手动在 selector 中显出。
- **Auto（Cursor Router）**：三档优化模式 **Cost / Balance / Intelligence**，按档为每个 Auto 请求选模型；按被路由模型 list 价计费，第三方路由加 $0.25/M Token Rate（Teams/Enterprise）。
- 每模型可带参数（subagent 括号语法可见）：`effort`、`context`、`fast` 等。
- 【来源：cursor.com/docs/models-and-pricing、cursor.com/docs/cursor-router】

### 5.2 Custom API Keys（BYOK）

- 支持 BYOK；Token Rate "applies on top of model API pricing for included usage, on-demand usage, and BYOK usage"（Teams/Enterprise）。
- BYOK 下 **zero data retention 不适用**（走用户自己 provider 的政策）。【来源：cursor.com/docs/models-and-pricing、cursor.com/help/security-and-privacy/privacy】
- Provider 配置 UI 字段（key 输入、base URL 覆盖、启用开关等）：官方帮助页有 api-keys 专页但本次未展开抓取，字段细节 **UNKNOWN**。【来源：cursor.com/help/models-and-usage/api-keys】

### 5.3 Per-model 特性与用量显示

- **Max Mode**：legacy plans 专属，API +20%；Opus、Fable、GPT-5.3 Codex、GPT-5.5 等必需。
- **Thinking** 变体：legacy 计价下算 2 请求。
- **Context window**：多款模型最高 1M 无附加费；GPT-5.4/5.5/5.6 的 1M long context 按 2x input 价；Claude 4 Sonnet 超 200k 双倍价。
- **Fast mode**：如 GPT-5 Fast 2x 价；云 Agent 用 "curated selection"，可选 context window 大小。
- **用量显示**：usage visible in editor settings and the dashboard（编辑器内 + cursor.com dashboard 两处）；per-token 价目表公开（如 Grok 4.6 $2 in/$6 out；Composer 2.5 $0.5/$2.5；Claude Sonnet 4.5-4.7 $3/$15；Opus $5/$25；GPT-5 $1.25/$10 等）；区域数据驻留加价 10%。
- 【来源：cursor.com/docs/models-and-pricing、cursor.com/docs/cloud-agent】

---

## 6. Projects / Workspace 概念

### 6.1 工作区

- 基础单位：VS Code 式 workspace（打开文件夹/多根 workspace）——官方文档不专门描述，标 **APPROXIMATE**。
- **Multi-workspace（Agents Window）**：一个窗口内对**所有项目**发起/管理 agent。
- **Worktrees**：Agent 在隔离 git checkout 中工作，主 checkout 不受影响。
  - 创建：Agents Window 内启动/移入 agent 即自动建 checkout（UI 原生 worktrees 仅限 Agents Window）；IDE 走 Worktree Skills 命令；CLI 亦支持。
  - 命令：`/worktree`（本会话剩余部分进独立 checkout）、`/best-of-n`（多模型各一 worktree）、`/apply-worktree`（结果带回主 checkout）、`/delete-worktree`。
  - 结果出口：继续在里面干活 / 建 commit / 开 PR / 带回主 workspace；agent 可直接 "Commit and push these changes, then open a PR"。
  - 配置 `.cursor/worktrees.json`：键 `setup-worktree-unix` / `setup-worktree-windows` / `setup-worktree`（值=顺序 shell 命令数组或脚本路径），`$ROOT_WORKTREE_PATH` 引用主 checkout。
  - 清理设置（3.5+）：`cursor.worktreeCleanupIntervalHours`、`cursor.worktreeMaxCount`（默认 25，机器级共享）。
  - 【来源：cursor.com/docs/configuration/worktrees】
- **Cursor Projects**（2026-09，beta）：feature/migration/整 app 级大工程容器，coordinator agent 规划并派发实现 agent（可数千 subagents），云端执行、跨机共享上下文、可订阅 Slack 频道/定时/PR 监控。【来源：cursor.com/changelog】

### 6.2 Git / Source Control 集成

- Editor：Source Control tab（含 Agent Review 入口）、commit/push/PR 流；agent 可直接 commit、push、开 PR。
- 远端：GitHub、GitLab、Azure DevOps、Bitbucket；**Cursor Origin**（2026-08，自家代码托管 early beta）：Origin repos、GitHub 镜像同步（GitHub 仍是 synced repo 的 source of truth）、在 Cursor 内 PR review/merge、Vercel/Depot/Buildkite 集成。
- Cloud Agent：独立分支 → push 交接；PR 评论/审批身份为 `cursor` bot（私有 automation 用本人 GitHub 账号）。
- 【来源：cursor.com/docs/agent/agents-window、cursor.com/changelog、cursor.com/docs/cloud-agent/automations】

---

## 7. Results / Artifacts（结果与产物）

| 产物 | 呈现 | 备注 |
|---|---|---|
| **Diffs** | 编辑器内联 diff + Agents Window **diffs view**（review/commit/manage PR 一站） | Tab 补全为灰色 ghost text（另一类"预览后接受"） |
| **Checkpoints** | chat timeline 内点击预览/restore；Restore Checkpoint 按钮、hover + 按钮 | 只回滚文件不回滚消息；本地存储、独立于 Git |
| **Accept/Reject** | Agent 编辑自动 apply 后靠 diff + checkpoint 评审；Cmd+K 行内 diff 接受/拒绝 | 官方未给统一 accept/reject 字段清单，标 UNKNOWN |
| **Best-of-n** | 多 worktree 并行结果对比，用户手动选胜者 apply/commit | 【cursor.com/docs/configuration/worktrees】 |
| **Cloud Agent Artifacts** | 截图、视频、日志；PR/diff/deployment/checks 面板（含移动端）；环境信息 hover repo 名可见所用 Build | 【cursor.com/docs/cloud-agent】 |
| **Background 进度** | Web/移动端实时 chat 流、subagent cards、锁屏 Live Activities（≤8 agents）、"Worked for 14m 22s" 式工时汇总、部署摘要、按周/月的任务列表、repo 级 "All Repos" task board（首页 demo 中有 **In Progress / Ready for Review** 两列看板） | 后两者来自首页 demo 描述，标 APPROXIMATE |
| **Image generation** | chat 内联展示，文件落 `assets/` | 【cursor.com/docs/agent/overview】 |

---

## 8. Settings 全量清单（Cursor Settings，`Cmd/Ctrl+Shift+J`）

> 说明：Cursor 的设置面板经历过多次重组（旧版有 Features / Indexing 等节；0.48+ 改 tab 布局；近期又把 Indexing 移除）。以下按当前文档可证 + 历史文档/论坛佐证枚举；无法证实的标 UNKNOWN/APPROXIMATE。【来源：cursor.com/help/security-and-privacy/privacy、forum.cursor.com 相关帖、daily.dev 指南】

### 8.1 General（通用）
- **Account**：登录/账户管理；**VS Code Import**（一键导入 extensions/themes/settings/keybindings）。【来源：cursor.com/help/getting-started/migrate-vscode】
- **Privacy Mode**：开关（见 8.12）；团队/企业默认开启、admin 可强制不可关。【来源：cursor.com/help/security-and-privacy/privacy】

### 8.2 Editor（编辑器）
- 继承 VS Code Settings UI（settings.json）；Cursor 专属编辑器项（如 Tab ghost text 行为、inline diff 呈现）官方无字段级文档，**UNKNOWN**。【APPROXIMATE】

### 8.3 Chat / Agent
- 旧版有 Chat 节（chat 内规则/markdown 行为等）；当前可见的 Agent 设置集中在：
- **Agents 节**（官方可证字段）：
  - **Approvals & Execution**：run mode 选择（Auto-review / Allowlist / Run Everything）+ 相关 sandbox/网络档位。
  - **Agent Review**：自动 review 开关、深度档（Quick/Deep）（3.11 起迁往 Git & PRs > Pull Requests）。
  - **Remote Control**：桌面 session 交给云 agent loop 的开关（3.9.8+）。
  - 【来源：cursor.com/docs/agent/security/run-modes、cursor.com/docs/agent/agent-review、cursor.com/docs/cloud-agent/mobile】

### 8.4 Tab
- 入口：状态栏 Tab 指示器或 Cursor Settings > **Tab**。
- 字段：**Snooze**（限时暂停）、**Disable globally**、**Disable per extension**（按文件扩展名）；快捷键 remap 在 Keyboard Shortcuts 搜 "Accept Cursor Tab Suggestions"。
- 模型选择等深字段：**UNKNOWN**。【来源：cursor.com/help/ai-features/tab】

### 8.5 Rules & Memories（Customize → Rules）
- Project Rules 列表（Add Rule、导入 Remote Rules from GitHub → `.cursor/rules/imported/<repoName>`）；User Rules（全局文本）；**Memories** 列表（查看/编辑/删除）。
- frontmatter：`alwaysApply` / `description` / `globs`。
- 【来源：cursor.com/docs/rules、forum.cursor.com/t/about-cursors-memory-record-feature/107355】

### 8.6 Models
- 模型启用/隐藏（"Hidden by default" 手动显出）、两池展示、Auto 路由模式（Cost/Balance/Intelligence）、BYOK API keys（细节 UNKNOWN）、用量/余额显示（editor settings + dashboard）。
- Team 侧：Team Settings → **Models**（模型访问控制，Auto-review 依赖的 classifier 模型被禁时 Auto-review 灰掉）。
- 【来源：cursor.com/docs/models-and-pricing、cursor.com/docs/agent/security/run-modes】

### 8.7 MCP / Customize
- **Customize** 页统一管理：**MCP servers**（toggle 启停、OAuth 连接）、**Plugins**、**Skills**、**Hooks**（`.cursor/hooks.json`：`beforeSubmitPrompt`、`preToolUse`、`beforeShellExecution`、`afterFileEdit`、`subagentStart`/`subagentStop`、`preCompact`、`afterAgentResponse`/`afterAgentThought`、`stop`）、**Marketplace**（含团队 marketplace）。
- 【来源：cursor.com/docs/mcp、cursor.com/docs/cloud-agent、cursor.com/docs/customize-cursor】

### 8.8 Indexing & Docs
- 旧版：Codebase Indexing 开关 + Docs（@Docs 自建文档索引）——**新版已移除该设置 UI**（语义索引 deprecated，转向 Instant Grep 本地检索）。当前 Docs 自定义功能状态：**UNKNOWN**（官方新文档未列）。【来源：forum.cursor.com/t/what-do-you-think-about-cursor-removing-the-codebase-indexing-settings/165899】

### 8.9 Privacy
- **Privacy Mode** 开关（General 节内，`Cmd+Shift+J` → General）；Team/Enterprise 默认开、可强制；Legacy Privacy Mode（云存储限制版）用户需单向升级到 Privacy Mode 才能用云 Agent/移动端。
- 数据面：sub-processors 列表（trust.cursor.com/subprocessors）、ZDR 例外（BYOK、个别需 admin 批准的模型）。
- 【来源：cursor.com/help/security-and-privacy/privacy、cursor.com/docs/cloud-agent/mobile】

### 8.10 Beta
- 存在于历史版本设置中（experimental features 汇集）；当前字段清单 **UNKNOWN**（官方文档未公开）。【APPROXIMATE，依据社区指南】

### 8.11 Account / Usage / Dashboard（Web）
- cursor.com **dashboard**：Usage（per-model token 用量、spend limits/spend alerts、overages、invoices）、Cloud Agents（secrets、environments、self-hosted machines/pools）、Team 管理（members、SSO/SAML/SCIM、analytics、audit logs、repo blocklists、billing groups）、Automations 页、Marketplace。
- 【来源：cursor.com/pricing、cursor.com/docs/cloud-agent、cursor.com/docs 交互面】

### 8.12 Shortcuts / Themes / Updates
- **Keyboard Shortcuts**：VS Code 式 Keyboard Shortcuts UI（可搜改 Cursor 专属键，如 Tab 接受键）。
- **Themes**：主题随 VS Code 导入（Open VSX 生态）；主题市场现状 **UNKNOWN**。【来源：cursor.com/help/customization/themes】
- **Updates**：VS Code 式自动更新（桌面端）；细节字段 **UNKNOWN**。

---

## 9. Automation（后台自动化）

**Automations** = 云 Agent 的定时/事件触发运行（官方文档：cursor.com/docs/cloud-agent/automations；帮助页：cursor.com/help/ai-features/automations）。

- **创建入口（4 个）**：Agents Window、cursor.com/automations、**`/automate` skill**（自然语言描述工作流，Cursor 自动配 trigger/instructions/tools）、Marketplace 模板。
- **核心步骤**：选 trigger → 写 instruction prompt →（可选）启用工具（Send to Slack、Comment on PR、MCP tools）→ 选 repo scope（none/单/多）→ Save & activate。
- **Triggers（可多个，任一命中即跑）**：
  - **Scheduled**：预设或 **cron 表达式**；只延后不提前。
  - **Source control**（GitHub/GitLab/Bitbucket Cloud）：draft opened、PR opened、PR pushed、PR merged、push to branch、comment added；GitHub 另有 PR/issue label changed、CI completed、issue comment、PR review comment、PR review submitted、review thread updated、workflow run completed；GitLab 加 PR approved；Bitbucket 加 PR approved。fork PR 不触发（PR merged 例外）。
  - **Slack**（仅公开频道）：新消息（默认顶层消息，可加 keyword/regex 过滤）、emoji reaction、channel created。
  - **Webhook**：自动生成私有 HTTP endpoint + API key，POST 即启动 run。
  - **Linear**：issue created、status changed、end of cycle。
  - **Sentry**：issue created/updated/any event。
  - **PagerDuty**：incident triggered/acknowledged/resolved/any event。
- **工具集**：PR creation（repo-backed 默认开）、Comment on PR（顶层+行内；开 approvals 时可 approve/request changes/dismiss）、Request reviewers（用 git/memory 找领域专家）、Send to Slack（固定或 agent 自选频道）、Read Slack channels、MCP server（暴露全部工具）、**Memories**（MEMORIES.md 跨 run 持久）、**Computer use**（浏览器操作/截图录像，默认开）。
- **配置字段**：Model、Repositories（none / 单 repo+branch / multi-repo）、Permissions（**Private**（creator 管理，计费 creator）/ **Team Visible**（团队可见，creator 身份跑）/ **Team Owned**（仅 admin 管理，跑在共享 team service account，计费团队池））、Triggers、Tools、Prompt。
- **托管 agents**：Automations 页内置 Bugbot、Security Agents、PR Routing & Approval。
- **身份**：GitHub 侧动作以 `cursor` 身份（Team-owned/团队 PR）；私有 automation 以用户本人账号；Slack 消息来自 Cursor bot。
- 另有 2026-08 的 **subscriptions** 概念（云 agent 订阅 PR/Slack thread/定时任务长期监控）与 **/loop** skill、**/goal** 长目标。【来源：cursor.com/changelog、cursor.com/docs/agent/overview】
- 【来源：cursor.com/docs/cloud-agent/automations】

---

## 10. States（运行状态处理）

| 状态 | 处理方式 | 来源/标注 |
|---|---|---|
| **Thinking** | chat 内流式展示推理；Debug mode 显式收集运行时证据 | 【APPROXIMATE：官方不逐帧描述 UI】 |
| **Streaming** | 实时 token 流；编辑以增量 diff 呈现；移动端"watch the chat stream" | 【cursor.com/docs/cloud-agent/mobile】 |
| **Tool running** | 每 tool call 可展开参数/响应（MCP）；auto 审批失败/拒绝时标记错误，单 server 失败不影响其他 | 【cursor.com/docs/mcp】 |
| **Queued** | 队列消息列于活跃任务下方、可拖拽排序、按序执行；**Tab** 排队到轮次结束 | 【cursor.com/docs/agent/overview】 |
| **Steering** | "Send now"/双 `Enter` 在下一 tool call 边界注入，不打断当前动作 | 【cursor.com/docs/agent/overview】 |
| **Applying** | 编辑自动应用（Edit files tool "suggests and automatically applies edits"）；Cmd+K 为行内 accept 流 | 【cursor.com/docs/agent/overview、inline-edit】 |
| **Done/Review** | 结果进 diff review；云 Agent 产出 "Worked for Xm Ys" 工时与部署摘要；task board 有 "Ready for Review" 列（首页 demo，APPROXIMATE） | 【cursor.com 首页、docs/cloud-agent】 |
| **Error/失败** | tool call 失败标错误态；subagent 失败返回 error status，父级可 retry/resume/换路；troubleshooting 文档覆盖 agent/tab/install/network 问题 | 【cursor.com/docs/subagents、help/troubleshooting】 |
| **Pause/Interrupt** | CLI：`Ctrl+C` 暂停 /goal；CLI 中再次 `Enter` 中断 turn | 【cursor.com/docs/agent/overview】 |
| **Long-running** | 云 Agent 可跑数小时/天；push 通知每轮结束；锁屏 Live Activities（≤8） | 【cursor.com/docs/cloud-agent/mobile】 |
| **Idle/background** | background subagent 持续把状态写 `~/.cursor/subagents/`；可 "Resume agent <id>" | 【cursor.com/docs/subagents】 |

---

## 11. Visual / Interaction 观察（官方截图/演示，**APPROXIMATE**）

以下来自官网可访问文本与 demo 描述，**未逐像素核实**，全部标 APPROXIMATE：

1. **首页 Desktop demo**：一个 agent **任务看板**，含 "**In Progress**" 与 "**Ready for Review**" 两列，卡片如 "Build Landing Page"、"Plan Mission Control"、"Bioinformatics Tools"——呈现"多 agent 并行 + 状态列"的信息架构。
2. **Cloud agents demo**：任务列表按 **week/month** 分组；单 agent 卡片报告 "**Worked for 14m 22s**" 与 **deployment summary**——强调可量化的执行摘要。
3. **Slack demo**：agent（@cursor）在频道内回复，附 "**View PR / Open in Cursor / Open in Web**" 三动作按钮——跨端深链模式。
4. **首页品牌**："subtle, solid brand background"、极简科技风；官方配色/字体规范未公开（UNKNOWN）。历史品牌为深色主题为主（社区共识，APPROXIMATE）。
5. **移动端**：锁屏 Live Activities + Dynamic Island 显示多 agent 进度；iPad 上 side-by-side review 与全宽 diff。
6. **Editor**：灰色 ghost text（Tab）；行内 diff 高亮；底部状态栏 Tab 指示器。
7. **Agents Window**：agent 列表 + diffs view + 并行 agent 卡片；细节布局（列宽/分组维度）官方截图未完整公开，UNKNOWN。

---

## 12. OBSERVATION → PATTERN → CURIS GAP（模式与候选差距记录）

> 本节仅记录模式（Pattern）与候选差距（Candidate Gap），**不决定** Curis 架构。Curis 为非编码的桌面 AI "Company OS"，需判断哪些模式可迁移。

### 12.1 可迁移模式（Pattern）

| # | OBSERVATION（Cursor 事实） | PATTERN（抽象） | 迁移评估（对非编码 Company OS） |
|---|---|---|---|
| P1 | 三档 Run Modes（Auto-review/Allowlist/Run Everything）+ 自然语言 `allow_instructions`/`block_instructions` + sandbox + 不可绕过的硬保护（删除/外部写/浏览器三道闸） | **分层权限门控**：模式档位 × 自然语言规则 × 强制红线三层，而非单选开关 | **强可迁移**。Curis 的 agent 执行同样需要"自动/询问/禁止"档位 + 白名单语义 + 破坏性动作硬闸（如删除文件、对外发送） |
| P2 | Auto-review 用小模型 classifier 判定命令安全性，官方自警 "not a security boundary" | **LLM 审批器**是 UX 而非安全边界；安全靠 sandbox 与硬规则 | 可迁移：Curis 可用轻量模型预判动作风险，但须明示其非安全边界 |
| P3 | Checkpoint（显著改动前快照、本地、独立于 Git、restore 只回滚不删对话） | **时间线级撤销**：结果可整体回退且对话史保留 | **强可迁移**：Company OS 的 agent 产物（文档/数据/流程变更）同样需要 checkpoint/restore |
| P4 | diff review + Agent Review（Quick/Deep 两档自动评审、BUGBOT.md 规则化评审标准、commit 后自动触发） | **以"差异"为单位的结果评审** + 可配置的自动评审 | 部分迁移：非编码场景的"diff"是文档/记录/计划版本差异；自动评审可变成"合规/质量 review agent" |
| P5 | Rules 系统：4 种应用方式（Always/Intelligently/Glob/Manual）+ frontmatter + 三级优先（Team→Project→User）+ 可强制团队规则 | **规则文件工程化**：作用域、触发方式、优先级、强制力皆有显式模型 | **强可迁移**：Curis 的公司规则/SOP 可完全复用该模型 |
| P6 | Memories 自动捕获 + 集中管理（Rules & Memories 同区）+ 官方警示不可信输入可注入虚假 memories | **自动记忆 + 用户可编辑 + 注入风险提示** | **强可迁移**：Company OS 需要组织级/个人级记忆；注入防护是公开设计点 |
| P7 | Cloud/Background Agents：多端（desktop/web/mobile/Slack/PR 评论/API）启动、隔离 VM、独立分支、URL 分享只读、team follow-ups | **长任务的脱离式执行与随处跟进** | **强可迁移**：Curis 后台 agent 应可在桌面发起、移动/网页跟进、结果可分享审阅 |
| P8 | Automations：cron/事件 triggers（SCM/Slack/Linear/Sentry/PagerDuty/webhook）、`/automate` 自然语言建自动化、Private/Team Visible/Team Owned 三档归属与计费身份 | **事件驱动 agent 工作流** + 自然语言创建 + 归属/身份模型 | **强可迁移**：Company OS 的"例行动作/监听事件"即是 automations；三档归属对应个人/可见/组织所有 |
| P9 | 任务看板（In Progress / Ready for Review）+ 工时摘要 + 按周/月任务列表 + Live Activities（≤8）+ 每轮 push | **多 agent 进度的仪表化呈现**：状态列、可量化工时、系统级通知 | **强可迁移**：Curis 需要跨 agent 的进度总览与"待我审阅"队列 |
| P10 | Queue + steer（不打断、下一边界注入、可拖拽排序、Cmd+Enter 插队） | **对运行中 agent 的非破坏式介入** | **强可迁移**：长任务的"追加指示不重跑"是核心 UX |
| P11 | Plan Mode：澄清问题 → 研究 → 可编辑 plan → 批准后 build；plan 可存 workspace 供团队复用 | **先批准方案再执行**的强制门 | **强可迁移**：Company OS 的高风险动作应有 plan→approve→execute 门 |
| P12 | Side chats：挂靠父线程、隐藏参考上下文、只读倾向、可 @ 拉回 | **旁路问答不打扰主任务** | **强可迁移**：主流程执行中随时可开只读小问 |
| P13 | @-mentions（文件/文件夹/终端/历史对话/分支 diff/浏览器） | **显式上下文注入语法**，与 agent 自主检索互补 | 可迁移：Curis 的 @-mention 对象换成文档/人员/系统/数据视图 |
| P14 | Worktree/best-of-n：任务级隔离副本 + 多模型竞标选优 | **并行方案对比择优** | 部分迁移：隔离"副本"对应草稿空间；多方案竞标对决策类任务很有价值 |
| P15 | 双池模型 + Auto 路由三档（Cost/Balance/Intelligence）+ 公开 per-token 价目 + 用量双端可见 | **模型即资源池**：档位化路由 + 成本透明 | 可迁移：Curis 同样应提供模型档位与用量/成本显示 |
| P16 | MCP 统一外部工具协议 + Marketplace 一键装 + per-server 网络管控 | **标准化工具接入与治理** | 可迁移：Curis 连接企业系统（日历/邮件/CRM）可借 MCP 或等价协议 |
| P17 | Subagents：context 隔离、专用 description 驱动委派、只许一层嵌套、可 resume by ID | **分层委派的上下文卫生学** | **强可迁移**：主 agent 不被子任务噪声污染是长任务稳定性的关键 |
| P18 | 无 repo 起步 → 后存 Origin repo；GitHub mirror 且"GitHub 仍是 source of truth" | **先干活后落库 + 外部系统仍是真相源** | 可迁移：Curis 临时任务可先执行后归档，且不抢夺现有系统（如 Notion/Drive）的真相源地位 |

### 12.2 不宜直接迁移 / 代码域特有（Non-transferable）

| # | OBSERVATION | 不迁移理由 |
|---|---|---|
| N1 | Tab autocomplete（ghost text、jump-in-file、跨文件 portal） | 深度绑定代码编辑器形态；Company OS 无连续文本编辑主场景（除非做文档编写器） |
| N2 | git worktree / 分支 / PR merge 流水 | 代码版本控制专属；Curis 需要的是文档/记录版本模型 |
| N3 | Merkle tree codebase indexing | 面向代码文件树；Curis 更适合文档/知识库索引（且 Cursor 自己也已 deprecated 语义索引转向本地检索） |
| N4 | Cmd+K inline edit、terminal profile、Open VSX 扩展 | IDE 形态专属 |
| N5 | Tech debt 式 "fix flaky tests" 的 /goal 示例 | 目标语义需换成业务流程目标，机制本身可借鉴（见 P 系） |

### 12.3 Candidate Curis Gaps（候选差距，仅登记）

- **G1（权限门控）**：若 Curis 尚无"档位 × 白名单 × 硬红线"三层权限模型，这是 Cursor 最成熟的参照（P1/P2）。
- **G2（结果评审队列）**：Cursor 的 "Ready for Review" 看板 + diff 评审 + 自动 review 双档（P4/P9），映射为 Curis 的"agent 产物待审队列"。
- **G3（Checkpoint/Resume）**：时间线快照 + restore 不丢对话 + agent ID resume（P3、§4.5）。
- **G4（Rules/Memories 一体化）**：规则四档应用 + 团队强制 + 自动记忆可编辑（P5/P6）。
- **G5（Automations/订阅）**：cron + 事件 triggers + 自然语言建自动化 + Private/Visible/Owned 归属（P8）。
- **G6（多端跟进）**：桌面发起 → 移动/网页跟进 → push/Live Activities（P7/P9）。
- **G7（非破坏介入）**：queue/steer/side chat（P10/P12）。
- **G8（成本透明）**：双池 + 路由档位 + 用量双端显示（P15）。
- 以上均为**候选记录**，是否成为 Curis 需求由 Product Definition 流程决定。

---

## 13. Sources（来源清单）

**官方文档（cursor.com/docs）**
- https://cursor.com/docs （文档首页、模型表）
- https://cursor.com/docs/agent/overview （Agent、tools、checkpoints、queue、/goal）
- https://cursor.com/docs/agent/plan-mode （Plan Mode）
- https://cursor.com/docs/agent/agents-window （Agents Window）
- https://cursor.com/docs/agent/agent-review （Agent Review）
- https://cursor.com/docs/agent/security/run-modes （Run Modes、permissions.json、sandbox）
- https://cursor.com/docs/agent/tools/search （Instant Grep）
- https://cursor.com/docs/subagents （Subagents）
- https://cursor.com/docs/mcp （MCP 配置/字段/OAuth/审批）
- https://cursor.com/docs/rules （Rules）
- https://cursor.com/docs/configuration/worktrees （Worktrees）
- https://cursor.com/docs/cloud-agent （Cloud Agents）
- https://cursor.com/docs/cloud-agent/automations （Automations）
- https://cursor.com/docs/cloud-agent/mobile （Mobile）
- https://cursor.com/docs/models-and-pricing （模型/双池/价目/Token Rate）

**官方帮助（cursor.com/help）**
- https://cursor.com/help/ai-features/agent （四种 mode 对比）
- https://cursor.com/help/ai-features/tab （Tab）
- https://cursor.com/help/ai-features/inline-edit （Cmd+K）
- https://cursor.com/help/ai-features/side-chats （Side Chats）
- https://cursor.com/help/customization/context （@-mentions）
- https://cursor.com/help/customization/ignore-files （.cursorignore）
- https://cursor.com/help/getting-started/migrate-vscode （VS Code 迁移/导入）
- https://cursor.com/help/security-and-privacy/privacy （Privacy Mode）

**官方其他**
- https://cursor.com/ （首页：定位、下载、demo 看板）
- https://cursor.com/pricing （Plan 与 usage-based pricing）
- https://cursor.com/changelog （Cursor Projects、self-hosted、Origin、subscriptions、Custom Modes 等）
- https://cursor.com/blog/2-0 （Cursor 2.0：Composer、多 Agent 界面）
- https://cursor.com/blog/secure-codebase-indexing （Merkle tree 索引）

**论坛/第三方（APPROXIMATE/佐证）**
- https://forum.cursor.com/t/about-cursors-memory-record-feature/107355 （Memories 管理位置）
- https://forum.cursor.com/t/rules-vs-memories-and-global-vs-project/137149 （Memories 用户级范围）
- https://forum.cursor.com/t/what-do-you-think-about-cursor-removing-the-codebase-indexing-settings/165899 （Indexing 设置移除）
- https://daily.dev/blog/setup-cursor-first-time/ （General > Account 导入入口佐证）
- https://www.threads.com/@testingcatalog/post/DKULXvQNX1G （Rules & Memories 设置重组佐证）

**未证实/UNKNOWN 汇总**：BYOK 配置 UI 字段、Tab 模型选择字段、Beta 节字段清单、memory 条目结构与上限、@Docs 现状、统一 accept/reject 字段清单、Cursor 品牌设计规范、Agents Window 截图级布局。
