# CURIS RD — MULTI-AGENT OPEN SOURCE DEEP DIVES

**Authority Class**: RESEARCH
**Status**: Draft → Review
**证据等级标注**：L1 本机真实运行 / L2 源码 / L3 官方文档 / L4 官方产品说明 / L5 第三方 / L6 推断

> 本文件只写**经核验**的事实。凡是未能达到 L1/L2 的结论，均显式标注等级。
> 全部仓库元数据来自 `evidence/E01_GITHUB_REPO_METADATA.tsv`（`gh api`，2026-09-19 采集）。

---

## 0. 入选与落选

**入选深挖（10）**：Agent Orchestrator、Claude Code、Codex、GitHub Copilot cloud agent、OpenHands、container-use、claude-squad、worktrunk、parallel-code、Orca/vibe-kanban（并列编排器）。

**落选但记录理由（对照组）**：

| 项目 | stars | 最近推送 | 落选理由 |
|---|---|---|---|
| `FoundationAgents/MetaGPT` | 70.5k | 2026-01-21 | **近期活跃度低（8 个月）**；本质是"SOP 角色扮演 + 产物生成"，`roles/` 下是 architect/engineer/product_manager/qa_engineer，`actions/` 是 write_prd→design_api→write_code→write_test→run_code 的**线性流水线**，不操作真实 repo 的 branch/PR/merge。作为**语义参照**保留。 |
| `OpenBMB/ChatDev` | 34.3k | 2026-07-24 | 同上，`workflow/` + `runtime/` + `yaml_instance/` 的 chat-chain 模型，产物落到自建 workspace，非真实 SCM 协作。 |
| `SWE-agent/SWE-agent` | 20.4k | 2026-09-14 | **研究基础设施（单 agent + ACI）**，不是多 agent 编排器；但其沙箱层 `SWE-ReX`（593★）是"沙箱化执行接口"的关键参考。 |
| `microsoft/autogen` | 61.0k | 2026-04-15 | 通用多智能体**会话框架**，非仓库协作编排；且 license 字段为 `CC-BY-4.0`。 |
| `e2b-dev/E2B` | 13.9k | 2026-09-18 | 通用**沙箱基础设施**，无编排语义；可作未来云执行备选。 |
| `humanlayer/humanlayer` | 11.6k | 2026-06-19 | 聚焦 HITL 审批通道（`NOASSERTION` license），与 Curis Human Gate 相关但不足以成为编排基线。 |
| `anomalyco/opencode` | **208.4k** | 2026-09-18 | 单机开源 coding agent（极大体量）。**是 Provider，不是 Orchestrator**——这正是"被编排的 Worker"。 |
| `aaif-goose/goose` | 54.4k | 2026-09-18 | 同上，Provider/Worker 角色。 |
| `crewAIInc/crewAI` | 58.7k | 2026-09-18 | 通用角色协作框架；coding-team 案例是**用法示例**而非仓库编排实现。 |

---

## 1. Agent Orchestrator（`Untrivial-ai/agent-orchestrator`）★★★

**元数据（L1）**：12,172★ / 1,677 fork / pushed 2026-09-18 / created 2026-02-13 / Apache-2.0 / Go+TypeScript / open issues 742。
**本地证据**：`evidence/E03`、`E04`、`E05`（源码 shallow clone）。
**一句话**：一个**长期运行的本地 Go daemon**，监督多个并行 coding agent 会话，每个会话独占一个 git worktree，把"任务—会话—工作区—PR—CI—评审"绑成一个可派生状态的对象。

### 1.1 Project Model
- **Project 是长期对象**，Repo 通过 "Add Project / Clone Repository" 绑定到本地路径；daemon 持久化到 SQLite。
- **关键设计（源码级）**：`domain/session.go` 定义 `SessionKind = worker | orchestrator`——**同一套会话模型里同时存在"执行者会话"和"编排者会话"**。
- 项目关闭重开：会话是**持久事实**（SQLite + CDC 轮询 + SSE 广播），daemon 重启后经 `session_manager` 的 `agent_switching.go / interface_transition.go / native_checkpoint.go` 恢复；Codex 与 ACP Chat 进程跑在 **detached per-session host** 中，**daemon/桌面被替换时不会中断进行中的 turn**（architecture.md 原文）。

### 1.2 Agent Model
- Agent 是**可替换适配器**，不是长期身份：`backend/internal/adapters/agent/` 下平铺 30+ 适配器（aidder/amp/auggie/claudecode/cline/codex/copilot/cursor/devin/droid/goose/grok/kilocode/kimi/kiro/muse/opencode/pi/qwen/vibe/omp/agy/autohand/crush/continueagent/primeagent/kimchi…）。
- 另有 `SessionKind=orchestrator` 的**持久规划 agent**（README："project orchestrator … persistent planning and coordination agent"），它在**任务之上**工作：产品方向、技术策略、优先级、工作排序；产出计划后拆任务、派 worker、追进度。

### 1.3 Task / Work Model
- **Worker = 执行单元**：一个任务 + 一个 coding agent + 一个隔离工作区。
- 支持由 orchestrator **拆解 → 生成任务 → spawn/redirect worker**；也支持人直接 "New task"。
- 状态不是任务状态机，而是**由 PR/CI/review 事实派生的看板**（见 1.8）。

### 1.4 Workspace Model（本项最有价值的发现）
- **Project session → 隔离 git worktree；projectless standalone worker → AO 托管的普通目录工作区**（architecture.md 第 1 段原文）。即**工作区策略本身是分层的**。
- 源码级确认：`adapters/workspace/` = `gitworktree` / `router` / `scratch`——**工作区是一个可路由的策略**（"router" 说明它按项目类型选择策略）。
- `SessionMetadata`（`domain/session.go`）字段：`Permissions` / **`Branch`** / **`WorkspacePath`** / **`WorkspaceRepoPath`** / **`DiffBaseSHA`** / **`DiffBaseRef`**——即"会话"恰好携带"哪个 repo、哪个分支、哪个工作区路径、diff 从哪个 commit 起算"。
- 运行时隔离：`adapters/runtime/` = `tmux` / `conpty` / `ptyexec` / `runtimeselect`；`adapters/container/` = `dockerreap`（容器回收）。

### 1.5 Context Model
- **会话不共享上下文**：README 明确 "keeps parallel work from collapsing into one shared context"。
- 项目级上下文由 **orchestrator 会话**持有（"Its project-scoped conversation preserves goals, decisions, constraints, and earlier reasoning"），它**组合规划历史 + 仓库上下文 + 实时 AO 状态（活跃 worker、ownership、PR、CI、review）**，再**把相关上下文递给每个 worker**。
- 这是"**长期项目上下文**与**单次工作上下文**分离"的教科书实现。

### 1.6 Handoff
- `session_manager/` 下有 `chat_handoff.go`、`handoff_artifact.go`、`interface_transition*.go`（大量测试）+ `domain/session_interface_transition.go`：**同一会话可在 TUI 与 Chat 两种界面之间做"持久化交接"**，`session_interface_transitions` 是持久检查点；且明确"两个控制器绝不同时存活"。
- 另有 `conversation.go` / `native_checkpoint.go`（`ConversationCheckpointState`: legacy/empty/coordination/prompt/complete，`Origin`: human/coordination）——**把"谁产生了一次 turn"编码进持久状态**，用于判定能否 replay。
- Worker 之间不直接通信：**通过 PR / CI / review 事实 + orchestrator 综合**交接。

### 1.7 Conflict
- 结构性规避：**每 worker 一个 worktree + 一个 branch**，因此不产生工作区级冲突。
- 合并冲突被当作**正常事件上浮到看板**（`StatusCIFailed` / `StatusChangesRequested` / `needs you`），而不是靠锁。

### 1.8 Review
- `adapters/reviewer/` **与 agent 适配器同名同构**（claudecode/codex/aider/amp/auggie/cursor/devin/droid/goose/kimi…）→ **Review 也是"用某个可替换 agent 去做"**，不是内建固定审查器。
- `backend/internal/review`、`reviewgateway`、`autoreview` 三个模块 + `domain/review.go`、`domain/reviewerharness.go` → 存在**评测 harness**概念（用一个 harness 去评另一个 harness 的输出）。
- 事实来源是 SCM：`adapters/scm` + `scm-observer.md` 持续观测 PR/CI/review 事实。

### 1.9 Merge
- **不由 AO 自动 merge**：看板有 `mergeable` / `merged` 状态位，merge 动作走 GitHub 侧（PR approved → mergeable）。人的角色是 "Ready to merge" 列里做决定。

### 1.10 Failure Recovery
- `activity_state` 的五个持久取值：`active / idle / waiting_input / blocked / exited`；**`blocked` = agent 停在待批准决策上，automation 绝不可以向 blocked 会话注入输入**（architecture.md 原文）——这是防"自动绕过人类审批"的硬约束。
- `StatusNoSignal`：**当 hook 管道断了、agent 从未回调时，明确显示"无信号"，而不是乐观显示 idle**——这是"失败可见"的设计范例。
- `native_checkpoint.go` / `conversation` 检查点提供可恢复的 turn 边界；`dockerreap` 回收容器；`sessionguard` / `processalive` / `daemonmeta` 做进程级守护。

### 1.11 Long-running
- **只有 durable facts 被持久化**：`activity_state`、`is_terminated`、`session_mode` + provider handle + generation、`session_interface_transitions`、PR 三张表。
- **显示状态一律在读取时计算、绝不存储**（`working/pr_open/draft/ci_failed/review_pending/changes_requested/approved/mergeable/merged/needs_input/exited/idle/terminated/no_signal`，见 `domain/status.go`）。
- 这条对 Curis 有直接价值：**长期存事实，状态只是派生视图**。

### 1.12 Provider 可替换性
- **本项最强**：agent 与 reviewer 双份适配器清单证明"**Provider 是可插拔的**"；`agentlaunch/spec.go` + `pin.go` 决定如何拼装启动命令；`codexops` / `codex_account` / `codex_capacity` 说明它甚至可以管理**同一 Provider 的多个账号与容量**。

### 1.13 对 Curis 的取舍
**可复用（思想/契约级）**：会话即聚合根；durable facts vs derived status；worktree per work；reviewer 与 agent 同构可替换；activity_state 五态 + blocked 不可注入；no_signal 而不是乐观 idle。
**不可直接照搬**：AO 绑定 GitHub PR 流程与外向云（`cloud/`、pricing、telemetry、mobile bridge）——**超出 Curis v1 单机本地自用边界**；且它是"工程师的管理台"，而 Curis 需要的是"**组织与问责**"层。

---

## 2. Claude Code（`anthropics/claude-code` + 官方文档）★★★

**元数据（L1）**：146,239★ / 23,758 fork / pushed 2026-09-18 / license 未声明 / TypeScript。
**本地可测性**：本机 **未安装** `claude` CLI → 全部结论 = **L3 官方文档**（`code.claude.com/docs/en/agents`、`/worktrees`、`/agent-teams`）。
**一句话**：把"多 agent 并行"做成了**一套并列的官方原语**（subagents / agent view / agent teams / dynamic workflows），并且**给每条原语配了不同的隔离与通信语义**。

### 2.1 四+一条并行原语（官方定义）

| 原语 | 官方定义 | 隔离 | 协调者 |
|---|---|---|---|
| **Subagents** | "Delegated workers inside one session that do a side task in their own context and return a summary" | 可 `isolation: worktree` | Claude（单会话内委派并收集） |
| **Agent view**（`claude agents`，Research preview） | "One screen to dispatch and monitor sessions running in the background" | **派发时自动搬进自己的 worktree** | 人（派发 + 事后查看） |
| **Agent teams**（Experimental，默认关闭，`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`） | "Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead" | **不做 worktree 隔离** | Lead agent |
| **Dynamic workflows** | "A script that runs many subagents and cross-checks their results" | 随脚本 | **脚本**（不是模型的逐轮判断） |
| **`/batch`**（skill） | "split one large change into 5 to 30 worktree-isolated subagents that each open a pull request" | worktree | 打包用法，非独立协调方式 |

### 2.2 Project Model
无独立 "Project" 实体：**Project 就是"一个 git 仓库 + 该仓库的 `.claude/` 配置 + CLAUDE.md + 项目级 plugins/settings"**。长期性由**文件系统**承载（不是数据库）。

### 2.3 Agent Model
- Subagent = 会话内的工作者（`Task` tool 派生，`agent_type` / `model` / `allowed_tools` / `permission_mode` / `context` 可配；`context: fork` 继承完整对话上下文）。
- Teammate = **"a full, independent Claude Code session"**，有自己的 context window、自己的模型与 fast mode（spawn 时固定）。
- **`/fork`（复制整个会话为后台并行会话）与 `/subtask`（fork 型子代理）** 是"上下文继承"的另一条正交轴。

### 2.4 Task / Work Model（Agent Teams 最有信息量）
- 内含四件套：**Team lead（主会话） / Teammates（独立会话） / Task list（共享） / Mailbox（消息系统）**。
- 任务三态 `pending / in progress / completed`，支持 **`blockedBy` 依赖**；未满足依赖的 pending 任务**不可认领**；依赖完成后**自动解锁**。
- 认领两条路径：**lead 指派** 或 **teammate 自领**（"a teammate picks up the next unassigned, unblocked task on its own"）。
- **认领用文件锁**："Task claiming uses file locking to prevent race conditions"。

### 2.5 Workspace Model
- **Worktree** 是一等公民：`claude --worktree <name>` / `-w`；默认落在 **`.claude/worktrees/<name>/`**，默认分支名 **`worktree-<name>`**；`--worktree "#1234"` 可直接从 PR 建工作区（目录 `pr-<number>`）。
- 会话中也可让 Claude 用 `EnterWorktree` / `ExitWorktree` 工具进出。
- **强制隔离校验（不可关闭）**：阻止编辑主 checkout 文件、阻止 Bash 的 cwd 解析回主 checkout、阻止 git 重定向（`-C` / `GIT_DIR`）、阻止无法验证形状的 git 命令。这是"**隔离不是君子协定，而是机械强制**"的最好范例。
- 清理：交互退出时干净无名的自动移除、有名的询问；`-p` 非交互**不清理**（保留 lock 直到 sweep）；子代理/后台会话按 `cleanupPeriodDays` 周期清扫；运行中 `git worktree lock` 防并发清理。
- **共享什么**：repo 的 `.git`（提交写共享 object store）、项目级插件、主 checkout 的权限批准文件；**不共享**：工作目录、index、HEAD。
- 独立于 worktree 的第二条隔离路径：`isolation: "worktree"` frontmatter 让某个 subagent 永久隔离。

### 2.6 Context Model
- **Teammate 加载项目上下文（CLAUDE.md / MCP servers / skills）+ lead 的 spawn prompt，但不继承 lead 的对话历史。**
- 官方说明 lead 的 conversation history 不 carry over——**"上下文不自动继承"是刻意的设计选择**，与 Curis 的"Employee Conversation ≠ Agent Context"高度同构。
- 跨会话消息（cross-session messaging）明确假设 agent 是"**不共享上下文、只共享消息**"的。

### 2.7 Handoff
- **三种不同交接**：subagent → 返回 summary 给父会话；agent view 会话 → **只向人汇报**；agent teams teammate → **互相直接发消息**。
- Mailbox 是**每个 agent 一个 JSON 文件**：`~/.claude/teams/{team}/inboxes/{agent}.json`；发送方**只有在写入成功时才报告已发送**（写失败则报错且不发送）——这是一个值得抄的**投递语义**。
- 自动投递，lead 不需要轮询。

### 2.8 Conflict
- **官方明确承认 agent teams 不做 worktree 隔离**，因此给出的是**流程性解答**："Break the work so each teammate owns a different set of files."
- **关键区分**："Locking applies to task claiming, not file writes."（锁保护的是**任务认领**，不是**文件写入**）——即官方不假装锁能解决写冲突。
- 合并冲突被明确预期为"由 agents 自己解决"。

### 2.9 Review / Merge
- Review 由**并行 subagent / dynamic workflow 的交叉校验**承担，而非固定 reviewer；`/batch` 的产物是 **每个 subagent 一个 PR**。
- **Worktree 文档明确说明：没有内建把 worktree 变更加回主 checkout / 自动开 PR 的机制**——merge 归人（或外部 PR 流程）。

### 2.10 Failure Recovery
- 官方 Limitations（**直接照抄事实**）：
  - `/resume` 与 `/rewind` **不恢复 in-process teammates**；恢复会话后 lead 可能向**已不存在的 teammate** 发消息。
  - **Task status can lag**："teammates sometimes fail to mark tasks as completed, which blocks dependent tasks."（依赖会被卡住）
  - Shutdown 慢（要等当前请求/工具调用完成）。
  - 一个 session 只有一个 team；teammate **不能再生成 teammate**；in-process teammate **不能起后台子代理**；lead 固定不可换。
  - 权限在 spawn 时固定；`dontAsk` 模式不被继承。
  - 邮箱曾出现"格式错误导致每秒报错并阻塞投递"的 bug（v2.1.207 前）。
- 这些限制本身就是**设计输入**：Curis 若把 task 完成判定完全交给 agent 自查，会复现"状态滞后卡住依赖"。

### 2.11 Long-running
- 长期状态**落在文件系统**：`~/.claude/tasks/{team}/`、`~/.claude/teams/{team}/inboxes/`、`.claude/worktrees/`、CLAUDE.md、`.claude/settings.local.json`。
- 没有中心数据库；**"项目记忆"= 仓库内文件**。

### 2.12 Provider 可替换性
- **弱**：官方原语中"workers are Claude sessions"（原文）；要引入别的工具必须**"expose it to Claude as an MCP server"**。
- 但**外围生态已补上**：worktrunk / container-use / parallel-code / Orca / AO 都把 Claude Code 当**可替换的一个 CLI** 调用。

### 2.13 对 Curis 的取舍
**可复用**：worktree 默认目录与命名约定；"任务认领锁 ≠ 文件写锁"的诚实边界；mailbox 的投递语义（写成功才算发送）；teammate 不继承 lead 历史；`blockedBy` 依赖 + 自动解锁；强制隔离校验清单。
**不可直接采用**：Claude Code 是**单一 Provider 的封闭协作层**（workers 必须是 Claude 会话），而 Curis 的硬约束是**能力可替换不写死**。

---

## 3. Codex（`openai/codex` + 本机 CLI + OpenAI 官方工程文章）★★★

**元数据（L1）**：125,138★ / 19,405 fork / pushed 2026-09-18 / Apache-2.0 / Rust。
**本机实测（L1）**：`codex-cli 0.144.6`，见 `evidence/E02`。
**一句话**：Codex 已经**同时具备**"单机可编程 agent 运行时（CLI）"、"云任务（Cloud）"、"桌面工作台（App，含 Local vs Worktree 线程）"三层，并且**多 agent 已是正式（stable）特性**。

### 3.1 Project Model
- **Project = 一个目录**（`-C/--cd <DIR>` 指定工作根）+ **仓库内 `AGENTS.md` + `docs/` 知识库**。
- 官方工程文章（OpenAI，"Harness engineering"）给出**可执行的长期项目模型**：
  - `AGENTS.md` **只约 100 行，是"目录"不是"百科全书"**；真正的知识放在结构化 `docs/`（`design-docs/`、`exec-plans/`、`generated/`、`product-specs/`、`references/`、`QUALITY_SCORE.md`、`SECURITY.md`…）。
  - **Plans 是一等工件**："Active plans, completed plans, and known technical debt are all versioned and co-located"（`docs/exec-plans/active|completed` + `tech-debt-tracker.md`）。
  - **机械强制**：专用 linters + CI 校验知识库是否最新、交叉链接、结构正确；**周期性 "doc-gardening" agent 扫描陈旧文档并自动开修复 PR**。
  - 结论："give Codex a map, not a 1,000-page instruction manual"；"**从 agent 的视角看，它运行期间无法在上下文中访问的东西就不存在**"（agent legibility）。

### 3.2 Agent Model
- 本机 CLI 能力（L1）：`codex exec`（非交互）、`codex review`（非交互代码审查）、`codex apply`（把 agent 最新 diff 以 `git apply` 落到本地工作树）、`codex resume` / `fork` / `archive` / `delete` / `unarchive`（会话生命周期）、`codex sandbox`、`codex mcp-server`（**Codex 自身可作为 MCP server 被别的框架调用**）、`codex app-server` / `remote-control`（远程控制 app server）、`codex app`（桌面工作台）。
- **Feature flags（L1，`codex features list`）**：`multi_agent` = **stable / true**；`multi_agent_v2` = under development；`enable_fanout` = under development；`computer_use` = stable/true；`browser_use` = stable/true；`hooks` = stable/true；`plugins` = stable/true；`memories` = experimental/true；`guardian_approval` = stable/true。
- Codex App 的线程模型（L4）：新建线程时选 **Local**（直接在你的项目里工作）或 **Worktree**（创建隔离分支）。

### 3.3 Task / Work Model
- **Thread（线程）≈ Work**：官方指导"一个 thread 对应一个连贯工作单元"，长期相关的工作留在同一 thread 以保留推理轨迹，只在工作真正分叉时 `fork`；上下文变淡用 `/compact`。
- **Cloud Tasks（L3/L4）**：`codex cloud exec / status / list / apply / diff`；任务在 OpenAI 托管环境运行，可指定**每个任务的分支或 commit SHA**，产出 diff，`apply` 回本地。**setup 阶段能拿 secrets，agent 阶段 secrets 被移除**；agent 阶段默认**无外网**。

### 3.4 Workspace Model（本项最关键）
- **本地并行 = worktree**：多个 worktree、各自分支、各自 Codex 会话；App 内可在**每任务一个 worktree**中监控；**automations 也在专用 worktree 中后台运行**。
- **注意（L1 纠正）**：`codex --help` 全量 options 中**没有 `--worktree` flag**；worktree 是 **App 的线程级选择 + 手工 `git worktree`**，不是 CLI 参数。第三方博客的 `codex --worktree` 是**臆造**。
- 权限/沙箱是**会话级可配**：`-s/--sandbox {read-only, workspace-write, danger-full-access}`、`-a/--ask-for-approval {untrusted, on-request, never}`、`--add-dir`（额外可写目录）、`--dangerously-bypass-approvals-and-sandbox`（明确标注"仅用于已被外部沙箱包裹的环境"）。
- 本机 config 实测：`sandbox="danger-full-access"`——即**本机当前是"无沙箱"模式**，这一点在 Curis 里必须作为"用户可配置的执行权限档位"而不是默认值。

### 3.5 Context Model
- 三层：`AGENTS.md`（地图）+ `docs/`（系统记录）+ `exec-plans`（进行中计划的进度与决策日志）。
- 子目录规则用 `AGENTS.override.md`（官方最佳实践）。
- **长时运行证据**：官方称"我们经常看到单次 Codex 运行在单个任务上工作**超过 6 小时**（常常在人睡觉时）"。

### 3.6 Handoff
- `codex apply`（把 diff 落回本地工作树）、`codex cloud apply`（把云任务 diff 落回本地）、`codex exec resume`（续跑非交互会话）、`fork`（分叉）。
- **交接产物是 patch/diff + commit**，不是自由文本。

### 3.7 Conflict
- 官方立场（L4/L5 汇总）：**worktree 隔离是"最容易推理与 review"的方式**；**对"写密集的并行 subagent"明确建议更谨慎**，因为并发编辑会产生冲突与协调开销；**推荐按所有权（ownership）而不是按意图来切分任务**。
- 冲突检测：worktree 隔离**不解决语义冲突**（两个 worktree 各自改同一文件都能过）→ 冲突在合并时才显现。

### 3.8 Review
- `codex review`（非交互）+ `codex exec review` 是**内建的一等能力**。
- 官方工程文章描述"**自我审查循环**"：让 Codex 本地审查自己的改动，再请求本地与云端的具体 agent 审查，迭代到所有 reviewer 满意（Ralph Wiggum Loop）。
- 评审也由 agent 承担：文章明确"**把几乎全部审查推给 agent-to-agent**"，人类只做优先级、把反馈翻译成验收标准、验证结果（"Humans steer. Agents execute."）。

### 3.9 Merge
- 官方工程实践的**反直觉结论**：仓库采用**最小阻塞门禁 + 短 PR 生命周期**；测试抖动靠重跑而非无限阻塞；**agent 常用 `gh` 自己 squash & merge 自己的 PR**；后台清理任务的 PR **一分钟内审查并自动合并**。理由："在 agent 吞吐远超人类注意力时，修正便宜、等待昂贵。"

### 3.10 Failure Recovery
- `resume` / `fork` / `archive` / `unarchive` / `delete` 是**会话级恢复与保留原语**（L1 实测存在）。
- 自动 compaction（`/compact`、远程 compaction v2 stable）处理上下文超限。
- 本机 `~/.codex/` 有 `.codex-global-state.json`（2.4MB）持久会话状态 + 备份。

### 3.11 Long-running
- 长期状态：仓库内 `AGENTS.md` + `docs/` + `exec-plans`；本机 `~/.codex/` 会话存储与全局状态；Cloud 侧任务列表。
- **关键洞察**：Codex 的长期项目记忆**放在仓库里**（与代码同版本、可 review、可 CI 校验），而不是放在产品的数据库里。

### 3.12 Provider 可替换性
- **中等偏强**：
  - Codex 可作 **MCP server**（`codex mcp-server`）被别的编排器调用 → **Codex 能被编排**。
  - Codex 可 **消费 MCP servers**（本机已配 stitch / node_repl / openaiDeveloperDocs）→ **Codex 能编排别人**。
  - `--oss` / `--local-provider {lmstudio, ollama}` → 可切本地模型。
  - `remote_models` 已 removed（说明曾有远程模型路由）。

### 3.13 对 Curis 的取舍
**可复用（思想级，价值最高）**：AGENTS.md 当目录不当百科；`docs/` 作为系统记录 + exec-plans 一等工件；doc-gardening agent；"agent legibility" 判据；diff/patch 作为交接产物；review 为一等子命令；worktree per work；"没有 API ≠ 不能自动化"对应 `computer_use`/`browser_use` 已 stable。
**注意边界**：Codex Cloud 是**外部托管**（GitHub 连接、订阅），与 Curis v1 单机本地自用不完全吻合；App 的 Worktree 线程模型**不能被 CLI 调用**，若 Curis 要"程序化创建隔离工作区"，只能用 `git worktree` + `codex exec -C <path>` 自己拼。

---

## 4. GitHub Copilot cloud agent（官方文档 + GitHub Blog）★★

**可达性**：闭源；**无本机实测**。结论 = L3（GitHub Docs）+ L4（GitHub Blog）。
**一句话**：**"issue → 分支 → draft PR"的托管异步 agent**，把"隔离"下沉到**每个任务一台 GitHub Actions 临时容器**，把"门禁"下沉到**GitHub 分支保护与 PR 审批**。

| 维度 | 事实 |
|---|---|
| Project Model | Project = GitHub 仓库；长期性由 GitHub（分支、PR、issue、Actions）承载 |
| Agent Model | 异步后台 agent；任务从 issue 分配 / agents panel / VS Code / `@copilot` 评论触发；可建多个专用 custom agent |
| Task Model | **一次任务 = 一个临时容器 + 一个 `copilot/*` 分支 + 一个 draft PR**；迭代靠 PR 上的 review 评论 |
| Workspace Model | **ephemeral GitHub Actions dev container**；`copilot-setup-steps` job 定制环境；**每次迭代（含 review 评论触发的迭代）都从头起一个干净环境** |
| Context Model | 仓库 custom instructions + MCP servers + 关联 issue/PR 讨论 + **视觉模型可读 issue 里的截图** |
| Handoff | **PR 是唯一交接物**（commit + PR description + session logs） |
| Conflict | 靠分支隔离；agent **只能 push 到 `copilot/*` 分支**，**不能 push main/master 或任何其他分支** |
| Review | **人 review**；agent **创建的 PR 上的 Actions 工作流不会自动运行**——必须有写权限的人显式批准，从而避免 agent 通过 workflow 拿到 repository secrets |
| Merge | 人 merge；分支保护照常生效 |
| Failure Recovery | 环境是临时的、**会话之间无状态保留**；重跑=新环境 |
| Long-running | 仓库内 instructions + 平台侧 session logs |
| Provider 可替换性 | **不可替换**（GitHub 绑定）；但它暴露了**"agent 不得触碰 secrets / 不得自合"**的安全模式 |

**对 Curis 的价值**：**安全边界的最完整样板**——"隔离环境 + 只能推指定前缀分支 + 人审批后才跑 CI + 每次迭代重建环境"。Curis v1 若做"本地执行"，可平移为：**执行工作区与主工作区物理分离、执行者不得直接写 Canonical 分支、写后必须过人（或另一 agent）Gate**。

---

## 5. OpenHands（`OpenHands/OpenHands`）★★★

**元数据（L1）**：88,439★ / 11,616 fork / pushed 2026-09-18 / created 2024-03-13 / MIT / 821 open issues；最新 release `v1.20.0`（2026-09-17）。
**证据等级**：仓库结构与目录（L2）；官方 blog（L4）；社区深度拆解（L5，已交叉标注）。
**一句话**：最贴近 Devin 的开源自治软件工程 agent 平台，**核心是"极小的 agent 内核 + 事件流单一真相 + 可替换 Workspace（本地/容器/远程）"**。

### 5.1 架构四角色（L5 拆解，与官方仓库结构一致）
- **Agent**：无状态（Pydantic 模型），是"history → next Action"的纯函数。
- **Conversation**：持有唯一的可变状态 `ConversationState`，驱动循环，持久化 **append-only EventLog**。
- **Workspace**：三种实现 **LocalWorkspace（进程内）/ DockerWorkspace（容器）/ RemoteAPIWorkspace（HTTP）**——同一份 agent 代码跑在不同隔离档位。
- **LLM**：LiteLLM 包裹（100+ 端点），支持 Router。
- 其余（记忆压缩 Condenser、microagents/skills、子代理委派、安全审查、卡死检测）都是**挂在事件流上的辅助服务**。

### 5.2 多 Agent 委派（V1）
- 委托被当作**普通工具**：**Spawn**（按名注册子 agent，继承父 agent 的 LLM 与**共享 workspace**）与 **Delegate**（并行派发多个子 agent，**阻塞等待全部完成**）。
- 早期 `AgentDelegateAction`：通用 CodeActAgent 把浏览任务委托给专门的 BrowsingAgent。

### 5.3 其余维度速览

| 维度 | 事实 |
|---|---|
| Project Model | 无显式 Project 实体；以**会话/事件流**为中心；仓库由 workspace 挂载 |
| Workspace Model | 三档：进程内 / Docker 容器 / 远程 API；容器有资源与文件系统限制、网络受限 |
| Context Model | **Event Stream 是单一真相源**；记忆靠 Condenser 压缩；microagents 按需自动加载 |
| Handoff | 靠事件流与共享 workspace；delegate 是**阻塞式**的（不擅长长链异步协作） |
| Conflict | **并行子代理共享同一 workspace** → 结构上**没有 worktree 级隔离**，冲突靠委派粒度控制 |
| Review | 内建 action-level 安全分析 + 可插拔确认策略 + 风险标注；**不是多 agent 交叉评审** |
| Merge | 平台侧无 PR 编排语义；通过 GitHub 集成开 PR 由人在外部收口 |
| Failure Recovery | 事件流可**增量确定性 replay**；卡死检测（stuck detection）；secret 热加载与掩码 |
| Long-running | 有 SDK/API、automations、Enterprise 治理层；但事件流是**会话生命周期**，跨会话项目状态弱 |
| Provider 可替换性 | **强（在 agent 侧）**：LiteLLM 多模型 + **ACP 兼容外部 agent**（Claude Code / Codex / Gemini CLI）；官方明确"外部 agent 继续管自己的模型、工具、认证与执行，OpenHands 提供 workspace 与 workflow 层" |

### 5.4 对 Curis 的取舍
**可复用**：`Agent(纯函数) / Conversation(唯一可变状态) / Workspace(可替换隔离档) / EventLog(单一真相)` 的四角色切分，与 Curis 的"Employee 调能力"模型天然同构；事件流可 replay；**ACP 接入外部 agent 的思路正是 Curis 需要的"Provider 可替换"**。
**不可直接采用**：它是**一个 agent 平台**，不是"多人多任务的长期项目编排"；且其多 agent 是**共享 workspace 的阻塞式委派**，不满足 Curis"多个 Work 并行改同一项目"的需求。
**重要限制提示**：官方 blog 自己指出 agentic swarm 的现实约束——"**读密集任务适合 fan-out，写密集任务在多个 agent 碰共享状态时立刻冲突**"，以及多 agent 的 token 消耗约为普通对话的 **15 倍**。

---

## 6. container-use（`dagger/container-use`）★★

**元数据（L1）**：4,047★ / 205 fork / pushed 2026-09-14 / Apache-2.0 / Go；release v0.4.2（2025-08-19）。
**本地证据**：`RD_MULTI_AGENT_RESEARCH_LAB/repos/container-use`（L2）+ README + `repository/` 源码。
**一句话**：**一个 MCP server**，让任何 MCP 兼容 agent 在**每个分支一个全新容器**里工作——把"隔离"从 git worktree 升级为**容器 + 分支**。

| 维度 | 事实（README + 源码结构） |
|---|---|
| Project Model | Project = 一个仓库；**每个 agent 一个容器 + 一个 git 分支** |
| Agent Model | 不定义 agent；**对所有 MCP 兼容 agent 通用**（Claude Code / Cursor / Goose / VS Code …），"Works with any agent, model, or infrastructure — no vendor lock-in" |
| Workspace Model | 容器（Dagger 驱动）+ 独立分支；`repository/` 下有 `git.go`、`repository.go`、`flock.go`（文件锁）、`environment/`（环境生命周期） |
| Context Model | 完整命令历史 + 日志（"See complete command history and logs of what agents actually did, not just what they claim"） |
| Handoff | **标准 git 工作流**："just `git checkout <branch_name>` to review any agent's work" |
| Conflict | 容器 + 分支双重隔离；`flock.go` 用于环境级互斥 |
| Review | 由人 checkout 分支评审；env 可 `export`（有自己的 export 机制，含路径穿越修复记录 #365） |
| Merge | 走标准 git（人在主 checkout 上 merge） |
| Failure Recovery | "experiment safely, **discard failures instantly**"——失败环境直接丢弃 |
| Provider 可替换性 | **最强范式**：不绑定任何 agent，只提供隔离层 |
| 状态 | 仓库自标 **experimental**；release 停留在 2025-08（版本节奏慢） |

**对 Curis 的价值**：它证明"**隔离层可以独立于 agent 层交付**"，且**可以做成 MCP 工具让任何 Provider 复用**。对 Curis v1（单机本地），容器化是**可选档位**而非默认——因为容器带来磁盘/启动成本，而 worktree 已经解决 90% 的"互相覆盖"。

---

## 7. claude-squad（`smtg-ai/claude-squad`）★★

**元数据（L1）**：8,496★ / 618 fork / pushed 2026-08-20 / **AGPL-3.0** / Go；最新 release v1.0.20。
**本地证据（L2）**：`session/git/{worktree.go, worktree_branch.go, worktree_git.go, worktree_ops.go, diff.go}` + `session/tmux/` + `session/instance.go`。
**一句话**：**tmux + git worktree 的终端多路复用器**，把"每个 agent 一个隔离工作区"做成了极小的 Go 工具。

### 源码级事实（L2）
`session/git/worktree.go` 的 `GitWorktree` 结构体字段即完整隔离模型：

```go
type GitWorktree struct {
    repoPath         string  // Path to the repository
    worktreePath     string  // Path to the worktree
    sessionName      string  // Name of the session
    branchName       string  // Branch name for the worktree
    baseCommitSHA    string  // Base commit hash for the worktree
    isExistingBranch bool    // 若为 true，cleanup 时不删该分支
}
```

- worktree 根目录：`<configDir>/worktrees`（`getWorktreeDirectory()`）。
- 运行时隔离：`session/tmux/` → **每个会话一个 tmux 会话**。

### 其余维度
| 维度 | 事实 |
|---|---|
| Agent Model | 不定义 agent：`-p/--program` 指定任意 CLI（默认 `claude`，可 `cs -p "codex"` / `cs -p "aider …"`） |
| Task Model | 一个 session = 一个任务；菜单 `n` 新建 / `D` 删除 / `r` 恢复 / `c` Checkout（提交并暂停） / `s` 提交并 push 分支 |
| Workspace Model | **worktree per session + branch per session**；README："Each task gets its own isolated git workspace, so no conflicts" |
| Context Model | 无共享上下文；靠 tmux 会话内对话 + diff 视图 |
| Handoff | **diff 视图（`tab` 切换 preview/diff）→ 人审 → `s` push**；跨 agent 无结构化交接 |
| Conflict | 结构性隔离；无冲突检测 |
| Review | 只有"diff 预览 + 人看"；**无自动 review** |
| Merge | **手动**（README 明确提示"forgetting to merge worktrees after sessions complete"是常见坑） |
| Failure Recovery | `r` resume 暂停的会话；状态存 `~/.claude-squad/storage.json`（README 排障段）；`cs reset` 重置 |
| Long-running | 弱：**单机 TUI 会话管理**，无项目级长期状态机 |
| Provider 可替换性 | **强**：任何终端 CLI 都能跑（Claude Code / Codex / Aider / Gemini / OpenCode / Amp） |

**对 Curis 的价值**：**最小可用的"Work → Worktree → Branch → Agent CLI"四元组**，且 `isExistingBranch` 这种"是否复用既有分支"的细节，说明"**工作区清理不能想当然删分支**"。AGPL-3.0 是**采用时的法务红线**。

---

## 8. worktrunk（`max-sixty/worktrunk`）★★

**元数据（L1）**：8,002★ / 273 fork / pushed **2026-09-18**（当天）/ Rust / GitHub license 字段 `NOASSERTION`，仓库内声明 **`MIT OR Apache-2.0`**（见 `plugins/worktrunk/skills/worktrunk/SKILL.md` frontmatter）。
**本地证据（L2）**：`plugins/worktrunk/skills/worktrunk/{SKILL.md,reference/*}`。
**一句话**：**不是编排器，而是"agent 时代的 git worktree 管道"**——把 worktree 当分支一样操作。

### 源码/文档级事实（L2）
- **分支寻址**："A command that names a branch already names its worktree" → `wt switch <branch>` / `wt remove <branch>` / `wt step diff --branch <branch>`。
- `-C <path>` **只移动工作目录，不改变 worktree 选择**（文档明确列出 `wt -C ../repo.beta step diff --branch beta` 是"说两遍 beta"的错误用法）。
- **两类配置，两种权限模型**：
  - 用户配置 `~/.config/worktrunk/config.toml`（永不入库）= 个人偏好（LLM 集成、路径模板、命令设置、user hooks）；文档要求"treat it conservatively — propose changes and get consent before editing"。
  - 项目配置 `<repo>/.config/wt.toml`（**入库**）= 团队自动化（pre-start / pre-merge 等 hook），"Edit proactively — changes are versioned and reversible via git"。
- Hook 类型：`post-merge` / `post-start` / `pre-commit` / `pre-merge` / `post-switch` 等（生命周期钩子）。
- **LLM 消息生成**：`wt step commit --dry-run` 渲染 prompt、跑 LLM、打印 message 但不 commit（可验证）。
- 路径模板支持 `hash_port`（**每个 worktree 分配唯一 dev server 端口**，避免并行服务冲突）；`wt step copy-ignored` 在 worktree 间共享 `target/` 等被忽略目录，**避免每个 worktree 冷编译**。
- `wt merge` = squash + rebase onto main + fast-forward + cleanup 一条命令。

### 对 Curis 的价值（很高）
1. **"用户配置 vs 项目配置"的双层权限模型**可直接迁移为 Curis 的"个人偏好不入库 / 团队约定入库（可 review、可回滚）"。
2. **`hash_port` + `copy-ignored`** 提醒：Curis 若真做多 worktree，必须解决**端口冲突**与**依赖目录重复安装**这类"看起来小、实际天天撞"的工程问题。
3. **hook 生命周期**（pre-start / pre-merge）是 Curis "Work 生命周期"最贴地的参考。
4. license 需要法务确认（GitHub 显示 NOASSERTION）。

---

## 9. parallel-code（`johannesjo/parallel-code`）★

**元数据（L1）**：1,011★ / 137 fork / pushed 2026-09-18 / MIT / TypeScript。
**本地证据（L2）**：`AGENTS.md`、`docs/architecture-overview.html`、`docs/{browser-preview,document-workspaces,reasoning-graph,…}.md`。
**一句话**：Electron 桌面应用，**一个任务 = 一个分支 + 一个 worktree + 一个 agent CLI + 一个 GUI 会话**。

### 关键机制（L2，`AGENTS.md` + README）
- 技术栈：**SolidJS + TypeScript + Electron + node-pty**；`macOS / Linux only`（无 Windows）。
- 任务创建流程（README，L5 与仓库一致）：**建分支 → 建 worktree → 把 `node_modules` 等 gitignored 目录 symlink 进新 worktree → 在新 worktree 里 spawn agent CLI**。
  - **symlink 是关键优化**：否则每个 worktree 都要重新 `npm install`。
- 会话结束后**从侧边栏把分支 merge 回 main**。
- 快捷键即流程：`Ctrl+N` 新任务、`Ctrl+Shift+M` merge to main、`Ctrl+Shift+P` push to remote。
- 仓库内自带 **browser-preview / document-workspaces / reasoning-graph** 等探索文档（说明它在做"给 agent 一个可预览的浏览器与可协作的文档工作区"）。

**对 Curis 的价值**：**symlink 共享依赖目录**是"多 worktree 实用化"的必要细节；"GUI 里 merge 回 main"说明**人在环上的收口点可以很轻**。
**局限**：单机 GUI、无项目级长期状态、无跨 agent 交接协议、无自动 review；Windows 缺失。

---

## 10. Orca（`stablyai/orca`）与 vibe-kanban（`BloopAI/vibe-kanban`）★

### 10.1 Orca
**元数据（L1）**：**71,857★** / 4,696 fork / created 2026-03-17 / pushed 2026-09-18 / MIT / 830MB 仓库 / **6,323 open issues**。
**证据等级**：README（L3）+ 元数据（L1）。**未做源码深挖**。
**定位（README 原文）**："**Run Codex, ClaudeCode, OpenCode or Pi side-by-side — each in its own worktree, tracked in one place**"，自定位 **ADE（Agent Development Environment）**。
**已确认特性**：Parallel Worktrees（**"Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner"**，即"**同题多跑择优**"）；Terminal Splits（Ghostty 级）；Design Mode（点选 Chromium 里任意元素，把 HTML/CSS/截图送进 agent prompt）；GitHub & Linear 原生；移动端伴随应用。
**风险提示（必须记录）**：**6 个月 7.2 万星 + 6,323 个未处理 issue** 的组合异常；`git worktree` 语义清楚且 README 具体，但 star 数不构成质量证据。**结论：作为"形态证据"参考，不作为复用候选。**

### 10.2 vibe-kanban
**元数据（L1）**：28,124★ / 3,014 fork / pushed 2026-09-18 / Apache-2.0 / Rust / open issues 536；最新 release 标签 `v0.1.44-20260424091429`（2026-04-24，**release 节奏与 commit 节奏不一致**）。
**证据等级**：元数据（L1）+ 描述（L3）。**未做源码深挖**。
**定位**："Get 10X more out of Claude Code, Codex or any coding agent"；仓库结构为 Rust `crates/` + `npx-cli` + `packages/`，即**本地服务 + 前端**形态。
**对 Curis 的价值**：**"看板"作为编排的人机界面**是本领域的共识形态（AO 与它一致）；但它只解决"可视化与调度"，不解决"组织与问责"。

---

## 11. 跨项目归纳：10 条已被反复验证的事实

1. **Canonical Repository 唯一**。所有系统都是"一个仓库（或它的一个 clone）"作为唯一工程真相源。
2. **并行 = 每个 Work 一个隔离工作区**。没有任何成熟系统让两个 agent 共享同一 working tree。
3. **git worktree 是主流原语**（Orca / AO / claude-squad / Claude Code / worktrunk / parallel-code / vibe-kanban）。
4. **容器/VM 是第二档隔离**（container-use / Copilot cloud agent / OpenHands / SWE-ReX / Codex Cloud），代价是启动、磁盘与"环境即代码"的额外负担。
5. **PR（或等价 diff+review）是唯一回主干的通道**。没有系统让 agent 直接写 main。
6. **Review 的主流是"另一个 agent"+"人做最终 Gate"**；Codex 官方甚至把人从审查环节基本移除，只留优先级与验收标准。
7. **状态应当"由事实派生"，不应当"自己维护"**（AO 的 `status.go` 是最清晰的实现）。
8. **失败要有专门的枚举**：`no_signal`、`changes_requested`、`ci_failed` 这类取值存在的意义是**拒绝乐观**。
9. **上下文不会被自动继承**：Claude Code teammate 明确不继承 lead 历史；AO worker 不共享上下文。**"给下一个 agent 什么上下文"是一个显式的产品决策**。
10. **长期项目记忆放在仓库里**（AGENTS.md + docs/ + exec-plans），而不是只放在产品数据库里——这样它可 review、可回滚、可机械校验。
