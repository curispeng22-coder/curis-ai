# CURIS RD — PROVIDER ORCHESTRATION MODEL

**Authority Class**: RESEARCH
**Status**: Draft → Review
**证据**：`E04`（AO `adapters/agent` 30+ 适配器 / `adapters/reviewer` 同构清单 / `adapters/workspace` 三策略 / `adapters/runtime` 四实现）、`E02`（本机 Codex 能力实测）、Claude Code agents/agent-teams 官方文档（L3）、OpenHands ACP 接入外部 agent（L4）、container-use "no vendor lock-in"（L2）。

---

## 0. 核心结论

1. **Provider 可替换性已经被真实工程解决过，有可直接读的参考实现**：Agent Orchestrator 的 `backend/internal/adapters/agent/` 下**平铺 30 个 Provider 适配器**，`adapters/reviewer/` **用同一套清单**做"换一个 Provider 来评审"。这不是理论，是已合并进主干的代码结构。
2. **可替换性的关键不是"支持很多 Provider"，而是"把 Provider 差异收敛到一个极薄的适配边界"**。AO 的做法：每个 Provider 一个目录（`agentbase` 提供公共骨架），差异只体现在**启动方式、活动信号（activity）来源、hooks 注入方式**三处。
3. **Provider 应当被抽象成 4 个可独立替换的槽位**（研究新增，证据来自 AO 的 adapter 分层）：

| 槽位 | 职责 | AO 的对应目录 |
|---|---|---|
| **Agent Slot** | 谁来写代码 | `adapters/agent/*` |
| **Reviewer Slot** | 谁来评审 | `adapters/reviewer/*` |
| **Workspace Slot** | 在哪写 | `adapters/workspace/{gitworktree,router,scratch}` |
| **Runtime Slot** | 用什么承载进程/终端 | `adapters/runtime/{tmux,conpty,ptyexec,runtimeselect}` |

> **这四槽分离是 Curis "能力可替换不写死"的直接落地形态**——而不是笼统的"支持多家模型"。

---

## 1. 本机 Provider 真实现状（L1 实测，2026-09-19）

| Provider | 本机状态 | 关键可用能力 | Curis 可用性 |
|---|---|---|---|
| **Codex CLI** | ✅ 已装 `codex-cli 0.144.6`（`/Users/yy/.local/bin/codex`） | `exec`（非交互）/ `review` / `apply`（diff → `git apply`）/ `resume` / `fork` / `archive` / `sandbox` / `mcp-server`（**可被编排**）/ `cloud`（实验）/ `-C` 指定工作根 / `-s` 沙箱档 / `-a` 审批档 / `--add-dir`；feature flags：`multi_agent` **stable**、`computer_use` stable、`browser_use` stable、`hooks` stable、`memories` experimental | ✅ **首选 Worker**；`-C <workspace>` 即可接入任何 Workspace |
| **Claude Code** | ❌ 本机**未安装** | 官方文档：`--worktree`、subagents、agent teams、agent view、cross-session messaging、`/batch` | ⚠️ 需安装后才可实测；其 worktree 与 agent teams **是该 Provider 私有语义** |
| **OpenHands** | ❌ 未安装 | SDK/API、三档 Workspace、**ACP 可接外部 agent** | ⚠️ 体量大（88k★ 平台），v1 不建议引入 |
| **Aider / OpenCode / Goose** | ❌ 未安装 | 均为成熟 CLI Provider | ⚠️ 备选池（AO 已为它们写适配器） |
| **OpenAI 兼容 / 本地模型** | 部分（Codex `--oss --local-provider {lmstudio,ollama}`） | 本地推理 | ⚠️ 可选 |

**结论**：Curis v1 的**唯一已验证可用 Provider 是 Codex CLI**；Claude Code 是**必须支持但当前无法实测**的第二个 Provider。这决定了 v1 的 Provider 抽象**必须按"至少两个 Provider"设计**，否则会不知不觉写死成 Codex-only。

---

## 2. Provider 抽象层设计（提案，非 Authority）

### 2.1 ProviderDescriptor（能力声明，而不是假设）

| 字段 | 含义 | 为什么必需（证据） |
|---|---|---|
| `provider_id` / `display_name` | 标识 | — |
| `kind` | `cli` / `sdk` / `cloud` | Codex 同时有三种形态 |
| `launch_mode` | `interactive_tui` / `headless_exec` / `both` | Codex 有 `exec`（非交互）；Claude Code 有 `-p`；agent teams **要求交互式会话**（官方原文：非交互 `-p` 模式不会 spawn teammates） |
| `workspace_binding` | `cwd` / `flag(-C)` / `provider_native_worktree` / `container` | Codex 用 `-C`；Claude Code 用 `--worktree`（**且只它自己认**）；container-use 用容器 |
| `resume_support` | `none` / `session_id` / `checkpoint` | Codex `resume/fork`；Claude Code `/resume` **不恢复 in-process teammate** |
| `context_source` | 读哪些项目上下文文件（如 `AGENTS.md` / `CLAUDE.md`） | Codex 读 `AGENTS.md`（含 `AGENTS.override.md`）；Claude Code 读 `CLAUDE.md` |
| `permission_model` | 沙箱档 / 审批档 / 是否可跳过 | Codex `-s` + `-a`；Claude Code permission modes + `dontAsk` 不被 teammate 继承 |
| `verification_hook` | 如何注入"完成前必须跑测试" | Codex `hooks`（stable）；Claude Code hooks |
| `activity_signal` | 运行状态如何被外部观测 | AO 为此单列 `activitydispatch` / `activitystate` / `hooksjson` / `hookutil` |
| `multi_agent_support` | 是否 Provider 自身就带多 agent | Codex `multi_agent` **stable**；Claude Code agent teams **experimental，默认关闭** |
| `result_contract` | 产出如何取回 | Codex `apply`（patch）；Claude Code 无自动 PR（官方明确） |

### 2.2 四条硬规则（防止 Provider 泄漏进产品语义）

| # | 规则 | 反面案例（真实存在） |
|---|---|---|
| R1 | **Curis 的任何产品概念不得以 Provider 命名**（不得出现"Codex 会话"作为 UI 一级对象） | Claude Code 的 "Agent Teams" 是**它自己的**协作层，其 workers **必须是 Claude 会话**——若 Curis 直接采用，就等于把研发部门锁死 |
| R2 | **不得依赖 Provider 私有的 Workspace 机制作为唯一隔离实现** | Codex 的 Worktree 是 **App 线程级选择，CLI 无 `--worktree`**（L1 实测）；Claude Code 的 worktree 落在 `.claude/worktrees/` 且只有它认 |
| R3 | **不得让 Provider 的协作层成为 Curis 的组织层** | agent teams 的 lead/teammate/task-list 是**运行期协作**，不是 Curis 的 Employee/Work |
| R4 | **Provider 差异必须收敛在适配层；上层只见 WorkResult** | 否则每加一个 Provider 都要改产品 |

### 2.3 路由策略（依据什么选 Provider）

| 依据 | 说明 | 优先级 |
|---|---|---|
| **用户显式指定** | Employee/Work 上可绑 Provider | 最高（覆盖一切） |
| **能力要求** | 需要 `computer_use` / 需要长时无人值守 / 需要强沙箱 | 高 |
| **可用性** | 未安装 / 未登录 / 额度耗尽 → 自动降级 | 高 |
| **工作类型** | 写密集（单一实现）vs 读密集（调研、测试生成、批量审查） | 中（OpenHands 官方建议：**读密集才适合 fan-out**） |
| **成本** | token/订阅额度 | 低（本领域已有证据：多 agent 消耗可达普通对话 **15 倍**；有报告称 3 个并行 agent 约 $30–40/日） |
| **成本非判据的部分** | 隔离强度、可信度 | 按既有裁定，"成本非判据"的领域应谨慎套用 |

---

## 3. 中途替换 Provider（回应用户 §10、§24-19）

### 3.1 可替换的四个层级（难度递增）

| 层级 | 含义 | 是否可行 | 机制 |
|---|---|---|---|
| **L-a 换 Reviewer** | 同一份 diff 换一个 Provider 审 | ✅ **完全可行** | diff 是 Provider 无关的；AO 的 `adapters/reviewer` 正是这么做 |
| **L-b 换 Executor（同一 Work，从零重跑）** | 同一 Work 换 Provider 重新执行 | ✅ 可行 | 只需 C2（Work Context）自包含 + Workspace 重建 |
| **L-c 换 Executor（同一 Workspace 接力）** | A 做一半，B 接着做 | ⚠️ **部分可行** | 需要：A 已 `commit`（未提交变更不可靠）+ base SHA 一致 + **结构化进度摘要**。证据：AO 的 `agent_switching` / `interface_transition`（同一会话在 TUI↔Chat 间持久交接，**且明确"两个控制器绝不同时存活"**）；Codex `resume/fork` |
| **L-d 换 Provider（会话状态无损迁移）** | 把 A 的**运行中会话**交棒给 B | ❌ **不存在** | 跨 Provider 无标准会话格式；**世界上没有系统做到** |

### 3.2 因此 Curis 的正确设计

> **把"可替换"的保证放在 L-a / L-b / L-c，而不是承诺 L-d。**

具体：
- **L-a 必须内建**：Review 默认由"**与执行者不同的 Provider**"承担（AO 的 reviewer adapter 就是同一清单的另一份实例）。
- **L-b 必须内建**：Work Context 必须**自包含**（不依赖"上一个会话还记得什么"）。
- **L-c 尽力而为**：提供"接力"能力，但**必须要求前一个 Provider 先 commit**，并把"C3 检查点"降级为"最佳努力"（能 resume 就 resume，不能就重跑）。
- **L-d 明确记录为 UNKNOWN 且不承诺**。

### 3.3 替换时必须处理的落地细节（来自真实实现的教训）

| 细节 | 来源 | Curis 处理 |
|---|---|---|
| 未提交变更无法跨界 | 通用 git 事实 | 替换前**强制 commit 或 stash**（并记录） |
| Provider 的权限档不同 | Codex `-s/-a` vs Claude Code permission modes | 替换后**权限档必须重新声明**，不得沿用（防"降级后权限升级"） |
| Provider 的项目上下文文件名不同 | `AGENTS.md` vs `CLAUDE.md` | Curis 必须有**单一项目地图源** + 每 Provider 的投射（README 里提醒："Changes to package.json must include package-lock.json"这类项目约定应在地图里） |
| 替换会导致"活动信号"读不到 | AO 的 `StatusNoSignal` 专为此存在 | 替换后**必须进入"待确认"状态而不是乐观 idle** |
| 被中途替换的旧 Provider 进程可能仍活着 | AO `Runtime Reaper` / `dockerreap` / claude-squad 的 tmux 残留问题 | **替换必须先终止旧执行体**，并验证终止 |

---

## 4. 安全与权限（Provider 侧的必读事实）

| 事实 | 来源 | Curis 含义 |
|---|---|---|
| Codex 支持 `read-only` / `workspace-write` / `danger-full-access` 三档沙箱 + `untrusted` / `on-request` / `never` 三档审批 | L1 本机 `--help` | **Curis 应把它作为"执行权限档位"暴露给用户**，而不是默认 `danger-full-access` |
| 本机 config 实测为 `sandbox="danger-full-access"` | L1 | ⚠️ 这是**用户当前的真实配置**，Curis 不得静默继承为产品默认 |
| **worktree/容器隔离不能保护密钥** | Codex 官方原文 | 凭据治理必须独立于 Workspace 隔离；沿用 Curis 既有硬约束（密钥只驻 `.env`，DB 只存 `credential_ref`） |
| Copilot：agent 只能推 `copilot/*`，agent PR 的 Actions 需人批准才运行 | 官方文档 | 本地等价物 = **分支所有权 + Gate**；且"agent 不得触碰凭据"应是硬规则 |
| Claude Code：teammate 不能替人批准权限、被拒后不能转手绕过 | 官方文档 | **权限冒泡必须真的到人**，不能由 agent 之间"互相批准" |

---

## 5. 结论性回答（用户 §11、§12、§24-6/7/19）

| 问题 | 回答 |
|---|---|
| **Codex 当前已经解决什么** | 单机可编程 agent 运行时（`exec`）、非交互代码审查（`review`）、diff 落地（`apply`/`cloud apply`）、会话生命周期（`resume`/`fork`/`archive`）、沙箱与审批档位、可被别的框架当 MCP server 调用、**多 agent 已是 stable 特性**、桌面 App 内的 Local/Worktree 线程模型、云任务（可指定分支/SHA）、6 小时级长时运行（官方实测）。**未解决**：程序化创建隔离工作区（CLI 无 `--worktree`）、跨 Provider 交接、项目级长期编排。 |
| **Claude Code 当前已经解决什么** | worktree 一等公民（`.claude/worktrees/`）+ **不可关闭的强制隔离校验**、subagents、agent teams（共享任务列表 + 文件锁认领 + mailbox + **blockedBy 依赖自动解锁**）、agent view（派发即自动搬进 worktree）、cross-session messaging、`/batch`（5–30 个 worktree 隔离 subagent 各开 PR）、CLAUDE.md 项目记忆、hooks。**未解决**：Provider 中立（workers 必须是 Claude 会话）、自动 merge/PR、`/resume` 不恢复 in-process teammate、任务状态滞后会卡依赖。 |
| **哪些开源项目真正值得复用** | ① **Agent Orchestrator**（唯一九项全满足，含 agent/reviewer/workspace/runtime 四槽适配层）② **container-use**（隔离层可独立成 MCP 工具）③ **worktrunk**（worktree 生命周期与 hooks 的成熟约定）④ OpenHands（事件流 replay + ACP 接外部 agent 的思路）。 |
| **是否存在可直接作为 Curis 底层 Orchestrator 的项目** | **部分存在**：`Untrivial-ai/agent-orchestrator` 是**唯一同时满足"真操作 repo / 真多 agent / 真并行 / 长期项目状态 / Provider 无关 / local-first / Apache-2.0 / 活跃 / 可嵌入（本地 daemon + CLI + REST/SSE）"九项**的候选。**但**它是"工程师管理台"形态，外围（GitHub 绑定、Cloud、pricing、telemetry、mobile bridge）**超出 Curis v1 边界**；且 Curis 需要的"组织与问责"层它没有。→ **建议结论：作为"参考架构 + 可借用的适配层设计"，而不是作为被依赖的运行时依赖。**（真正采用与否，属 L2 Gate，需 CEO 裁定） |
| **Provider 能否中途替换** | L-a/L-b/L-c 可以（且必须支持）；**L-d（无损迁移运行中会话）不存在**。 |
