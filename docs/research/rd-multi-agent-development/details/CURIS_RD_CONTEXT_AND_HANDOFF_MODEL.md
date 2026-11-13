# CURIS RD — CONTEXT AND HANDOFF MODEL

**Authority Class**: RESEARCH
**Status**: Draft → Review
**证据**：Claude Code agent-teams 官方文档（teammate 不继承 lead 历史；mailbox；blockedBy）（L3）；Agent Orchestrator `architecture.md` + `session.go` + `conversation/native_checkpoint`（L2）；Codex 官方工程文章（AGENTS.md 作为地图 / docs 作为系统记录 / exec-plans）（L4）；claude-squad / worktrunk / container-use 源码（L2）。

---

## 0. 本文件要解决的唯一问题

用户 §15 的原话：

> 不要再把这四个都叫 Context。最终给明确术语和生命周期。

本文件给出 **四个互不重叠的 Context 类型**、**各自的存储位置与生命周期**、以及**它们之间的合法转移（Handoff）**。

---

## 1. 四层 Context（术语定版提案）

| 层 | 名称 | 一句话定义 | 时间尺度 |
|---|---|---|---|
| C1 | **Project Context** | 这个**项目长期是什么**：目标、架构、仓库、指令、决策、知识、历史、团队 | **月-年**（项目生命周期） |
| C2 | **Work Context** | 这**一件工作要达成什么**：需求、相关文件、依赖、期望结果、验收标准 | **小时-天**（Work 生命周期） |
| C3 | **Execution Context** | 这**一次执行运行时发生了什么**：prompt、Provider、沙箱、进程、日志、工具状态 | **分钟-小时**（一次运行） |
| C4 | **Conversation Context** | **CEO ↔ Employee 的持续工作关系**：说过什么、答应过什么、为什么这样决定 | **月-年**（关系生命周期，跨 Work） |

> **关键澄清**：四者是**包含关系不是并列关系**——Project ⊃ Work ⊃ Execution，而 Conversation **横向跨越**全部（一个人可以在多个 Work、多个 Project 上与同一个 Employee 对话）。

---

## 2. 逐层规格

### C1 — Project Context（项目长期上下文）

**这是什么**：项目的"**系统记录（system of record）**"。

| 项 | 内容 |
|---|---|
| **装什么** | ①目标与范围 ②架构与关键决策（ADR/裁定）③仓库与目录约定 ④项目指令（"地图"）⑤知识与参考 ⑥历史（已完成的工作、走过的弯路）⑦团队（谁在这个项目里承担什么） |
| **权威载体（关键结论）** | **必须首先落在仓库里**（随代码版本化）。Codex 官方实践：`AGENTS.md` **约 100 行、只当地图**；真相在结构化 `docs/`；进行中的计划在 `docs/exec-plans/{active,completed}` + `tech-debt-tracker.md`；由 **linters + CI 机械校验**保持新鲜；**周期性 doc-gardening agent** 扫描陈旧文档并开修复 PR。 |
| **Curis 侧载体** | ①仓库内文件（`AGENTS.md` 式地图 + `docs/` 真相）②Curis 侧的 `ProjectContextRecord`（指针 + 摘要 + 新鲜度），**不复制仓库内容** |
| **谁写** | 人的决策 + Product/Architect 类 Employee 的产出（**经 Gate 后**入 Canonical） |
| **谁读** | 全部 Employee（**应该是每次启动都注入**） |
| **生命周期** | 与项目同寿命；Workspace 销毁**不影响**它 |
| **反模式** | ❌ 把 Project Context 放进"某个 Conversation"里（Conversation 会被 `archive`/`compact`，项目记忆不能依赖它）；❌ 做成"一个巨大的指令文件"（Codex 官方实测失败：上下文被挤占、静默腐烂、无法机械校验） |

**判据（可直接搬用 Codex 原文）**：
> "give Codex a map, not a 1,000-page instruction manual"
> "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."

### C2 — Work Context（工作上下文）

**这是什么**：**一件 Work 的完整定义**。它是 Curis 的**核心自有对象**（成熟系统里对应 AO 的 session、Copilot 的 issue+PR、Claude Code 的 task）。

| 项 | 内容 |
|---|---|
| **装什么** | ①目标（要达成什么，可验证）②需求/验收标准 ③**相关文件与契约**（预计会碰的范围）④依赖（前置 Work / 前置决策）⑤**执行策略**（用哪个 Provider、哪个 Workspace 策略）⑥结果约定（产出形态、必须通过的测试） |
| **不装什么** | ❌ prompt（那是 C3）❌ 日志（C3）❌ 与 CEO 的对话全文（C4） |
| **谁写** | Leader 类 Employee 拆解 + 人或 Gate 批准；也可由人直接创建 |
| **谁读** | 执行该 Work 的 Provider 会话（**作为启动输入**）；Review 方；CEO 看进度 |
| **生命周期** | 创建 → 执行 → 收口 → **归档**（长期保留为"项目历史"的一部分，即转化为 C1 素材） |
| **存储** | Curis 侧的**持久事实**（不是派生视图）。参照 AO：`SessionKind`、`Branch`、`WorkspacePath`、`DiffBaseSHA/Ref`、`activity_state`、`is_terminated` 才是 durable；状态如 `working/mergeable` **读取时计算**。 |
| **依赖语义的证据** | Claude Code：`blockedBy`——"a pending task with unresolved dependencies cannot be claimed until those dependencies are completed"，完成时**自动解锁**。Curis 应采纳此语义（并注意其已知缺陷：**teammate 有时忘记标记完成 → 依赖被卡住**，所以 Curis 必须有超时/人工兜底）。 |

### C3 — Execution Context（执行上下文）

**这是什么**：**某一次 Provider 会话运行**的运行时事实。

| 项 | 内容 |
|---|---|
| **装什么** | ①实际发给 Provider 的 prompt（含注入的 C1/C2 摘要）②Provider 标识与版本 ③Workspace 路径与 base SHA ④进程/会话 id ⑤工具调用序列与事件流 ⑥stdout/stderr/日志指针 ⑦权限档位（沙箱/审批策略）⑧token/成本 |
| **生命周期** | **最短**：一次运行。运行结束即冻结为**只读记录**（用于恢复、审计、复现） |
| **存储** | 事件流（append-only）——**OpenHands 的 EventLog 是最完整的参考**：单一真相源、可增量确定性 replay；AO 的 `activity_state` 五态 + `conversation checkpoint` 是轻量版参考 |
| **谁读** | 恢复逻辑、审计、Cost 统计；**默认不注入给下一个 Execution**（见 §3） |
| **反模式** | ❌ 把 Execution 日志当作"下一个 agent 的上下文"——日志是**证据**不是**输入**；❌ 让 Execution Context 无限增长（用 Provider 自己的 compaction：Codex `/compact`、OpenHands Condenser） |

### C4 — Conversation Context（对话上下文）

**这是什么**：**Employee 与 CEO 的持续工作关系**。这是 Curis 相对全部开源项目的**结构性差异点**——它们都没有"员工"这个长期身份。

| 项 | 内容 |
|---|---|
| **装什么** | ①对话历史与结论 ②已承诺事项 ③被解释过的取舍与理由 ④附件（截图/文档）⑤该 Employee 的"工作习惯"（用户偏好） |
| **不装什么** | ❌ 代码真相（在 C1）❌ 任务定义（在 C2）❌ 运行日志（在 C3） |
| **生命周期** | 与"这个 Employee 在这个项目上"的关系同寿命；**跨 Work 持续**；Project 归档后仍应保留（问责记录） |
| **谁读** | 该 Employee 自身；CEO；**默认不被 Provider 会话读取** |
| **关键约束（有证据支持）** | Claude Code 官方明确：**teammate 加载项目上下文（CLAUDE.md/MCP/skills）与 spawn prompt，但不继承 lead 的 conversation history**。→ **"上下文不自动继承"是被验证过的正确默认**。Curis 应把"Employee 的对话历史"与"Provider 的输入"**显式隔开**，由 C2 定义"这次要给 Provider 什么"。 |

---

## 3. Handoff 模型（回应用户 §9-Handoff、§15、§17）

### 3.1 交接的三种性质（必须先分类，否则会做错）

| 类型 | 定义 | 成熟系统的做法 | Curis 应当采纳 |
|---|---|---|---|
| **H-A 同 Work 内换执行体**（Provider A → Provider B，或崩溃后重启） | 任务不变、上下文继续 | Codex `resume` / `fork`；AO `agent_switching.go` + `native_checkpoint` + `interface_transition`（**同一会话在 TUI/ Chat 间持久交接，两控制器绝不同时存活**） | ✅ **必须支持**（Provider 可替换的落地形态）；交接物 = **C3 检查点 + C2 不变** |
| **H-B Work → Work**（A 完成后 B 开始，可能不同 Employee/Provider） | 任务变更，但需要 A 的成果 | 全部系统都走 **PR / diff / commit**；AO 用 orchestrator 综合后**主动向 worker 递上下文** | ✅ **必须支持**；交接物 = **收口后的 diff/commit 或明确的结构化结果**，**不是聊天记录** |
| **H-C Work → Canonical**（成果进入项目真相） | 不是"给下一个 agent"，而是"进项目" | AO 的 `mergeable/merged`；Copilot 的 PR + 人审批；Claude Code **无自动 merge** | ✅ 建模为 **Gate（Decision）**，与 Curis 既有 `Decision 内嵌 Banner` 对齐 |

### 3.2 交接物清单（定版提案）

| 交接类型 | 交接物 | 明确不要传的东西 |
|---|---|---|
| H-A | ①`base_ref/SHA` ②已产生的 diff（未提交部分需先 commit 或 stash）③**C3 检查点**（可 resume 的会话句柄或事件流位置）④当前进度摘要（**结构化**：已完成/未完成/阻塞点） | ❌ 原始日志全文 ❌ 完整对话历史 |
| H-B | ①**commit / diff**（首选）②涉及的文件清单 ③测试结果 ④**未解决项与已知风险** ⑤（可选）`handoff_artifact`（结构化摘要文件） | ❌ "based on your findings" 式模糊指令——Codex/Claude 官方都把"delegation without understanding"列为反模式 |
| H-C | ①diff/commit ②验收证据 ③Decision 记录 | — |

### 3.3 关键差异：三种"消息"语义不要混用

| 机制 | 语义 | 可靠性 | Curis 用途 |
|---|---|---|---|
| **Diff / Commit / Patch** | 变更的**权威表示** | 高（git 保证） | H-B / H-C 主通道 |
| **Artifact 文件**（AO `handoff_artifact`；Claude Code subagent "returns a summary"） | 结构化**摘要** | 中（可丢失/可过期） | H-B 辅助；**必须可追溯到 diff** |
| **Message / Mailbox**（Claude Code `inboxes/{agent}.json`；AO 的 orchestrator 指令） | **协调信号**（"去做 X"、"我卡住了"） | 中→高（Claude Code 规则：**写成功才算已发送**） | 运行中的协调、升级、请求 |
| **Shared Task State**（Claude Code 共享 task list，文件锁认领） | **工作分配状态** | ⚠️ 低（**官方承认状态会滞后**） | 仅在需要"多个执行体抢任务"时使用；**Curis 应保留人工/超时兜底** |

### 3.4 一个必须接受的事实

> **跨 Provider 的标准交接协议目前不存在。**

证据：AO 用 30+ 适配器 + 自己的 `handoff_artifact`；Claude Code 用 mailbox（**只能是 Claude 会话之间**）；Codex 用 patch/apply；container-use 用 git 分支。**没有两个系统之间能直接互相交接。**

→ **Curis 的定位出现**：**Curis 应当是"跨 Provider 交接的归一化层"**——把任何 Provider 的产出统一为 `WorkResult = {diff, files, test_evidence, unresolved, logs_pointer}`，再交给下一个 Provider。**这是 Curis 真正需要自己做的少数几件事之一。**

---

## 4. 责任映射（回应用户 §2、§17）

### 4.1 三层模型的定版

```
Employee（长期组织身份 / Responsibility Holder）
   │  拥有：Constitution（职责）、Conversation（与 CEO 的持续关系）、Decision 权责
   │  不拥有：任何工程资产
   ↓ 承担
Work（有目标、可验收的执行单元）
   │  拥有：Work Context（C2）、验收标准、生命周期
   │  不拥有：代码真相（只是引用 Canonical Project）
   ↓ 被分配
Assignment（一次执行指派）
   │  拥有：Workspace（消耗品）+ 一个 Provider 会话
   ↓ 调用
Coding Agent Provider（Codex / Claude Code / OpenHands / Aider / …：可替换执行能力）
   ↓ 产出
WorkResult（diff + 证据 + 未解决项）
   ↓ 经
Verification（另一 Provider 会话 或 人）
   ↓ 经
Decision Gate（CEO / 预授权规则）
   ↓
Canonical Project（唯一工程真相）
```

**这条链与用户 §2 的候选关系一致**，但补了三个此前缺失的环节：**WorkResult 的归一化**、**Workspace 的归属**（属于 Assignment 不属于 Work）、**Gate 的位置**（在 Verification 之后、Canonical 之前）。

### 4.2 明确否决的三种映射

| 否决 | 理由 |
|---|---|
| ❌ 1 Employee = 1 Agent Process | 用户已明确"不要预设"。证据：Claude Code teammate 是"独立的完整会话"，但**一个 session 只能有一个 team、lead 固定**——把身份等同于进程会把 Curis 锁进单一 Provider 的会话模型 |
| ❌ 1 Work = 1 Agent | Claude Code 一个 task 可由多个 teammate 协作；AO 一个 session 可发生 `agent_switching`（换 Provider）；Codex 一个 thread 可 `fork` |
| ❌ Employee 拥有代码 | 违反 I1/I3；且会让"Employee 离职"变成"代码失踪" |

### 4.3 三种合法形态（用户 §17 要求"不要预设"）

**形态 1：1 Employee → N Work（并行）**
```
Architecture Employee ──┬─ Work A ─→ Assignment ─→ Workspace A ─→ Claude Code
                        └─ Work B ─→ Assignment ─→ Workspace B ─→ Codex
```
证据：AO 的 orchestrator 会话可 spawn/redirect 多个 worker；Claude Code lead 可派多个 teammate + **teammate 自领下一个未阻塞任务**。

**形态 2：1 Work → N Provider（同一成果多方竞争或分工）**
```
Work C ─┬─ Assignment 1 ─→ Workspace C1 ─→ Codex        ┐
        ├─ Assignment 2 ─→ Workspace C2 ─→ Claude Code  ├→ 择优 / 合并
        └─ Assignment 3 ─→ Workspace C3 ─→ OpenHands     ┘
```
证据：Orca 的 **"Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner"**（README 原文）；Codex 官方"同一 diff 请多个 reviewer agent 各自审查"。

**形态 3：1 Work → N Provider 串行（分工接力）**
```
Work D ─→ Assignment 1（Codex：实现）─→ WorkResult ─→ Assignment 2（Claude Code：补测试）─→ …
```
证据：Codex `resume/fork`；AO `agent_switching` + `interface_transition`（**同一会话换 Provider 而不中断工作**）。

> **产品含义**：RD 的"Employee Work Surface"**不能**是"一个员工一个终端"，而应是"**一个员工手持一份 Work 清单，每份 Work 可有一个或多个执行槽位**"。

---

## 5. Leader 模型（回应用户 §18）

### 5.1 成熟系统里"Leader 类角色"的真实分工

| 角色 | 在哪个系统里存在 | 实际承担 | 证据 |
|---|---|---|---|
| **Planner / Orchestrator** | AO 的 `SessionKind=orchestrator` 持久规划 agent | 产品方向、技术策略、优先级、工作排序；**组合规划历史 + 仓库上下文 + 实时状态**；把计划拆成任务并 spawn worker | README + `domain/session.go` |
| **Manager / Lead** | Claude Code 的 **team lead** | 生成 teammates、创建任务、指派或允许自领、收权限冒泡、发起 shutdown；**固定不可换** | 官方文档 |
| **Supervisor** | OpenHands / Copilot 的"平台层" | 提供 workspace、workflow、governance、审计与预算（**是平台不是 agent**） | OpenHands blog |
| **Reviewer** | Codex（`codex review`、agent-to-agent 审查）；AO（`adapters/reviewer/`）；Claude Code（cross-check workflow） | 对 diff 做审查并给出结构化意见 | 各官方文档 |
| **Workflow script** | Claude Code dynamic workflows | **由脚本（而非模型逐轮判断）持有计划**；适合"太大、需要多轮交叉校验"的任务 | 官方文档 |
| **Doc-gardening agent** | Codex 官方实践 | 定期扫描陈旧文档、更新质量分级、开重构 PR | 官方文章 |

### 5.2 Curis Leader 应当负责什么（提案 + 哪些必须自动、哪些必须 Gate）

| 职责 | 建议 | 自动 / Gate |
|---|---|---|
| 目标理解（把 CEO 的话变成可验收目标） | ✅ 负责 | ⚠️ **Gate**：目标被误读的代价最高，第一次必须人确认 |
| Work Breakdown（拆成 Work） | ✅ 负责 | 自动（可撤销），但**拆解结果应在 Employee Work Surface 可见** |
| Assignment（派给谁/哪个 Provider） | ✅ 负责 | 自动（有默认 Provider + 显式覆盖） |
| Dependency（Work 之间的阻塞关系） | ✅ 负责 | 自动；**必须带超时兜底**（Claude Code 的"任务状态滞后卡住依赖"是已发生的失败模式） |
| Priority | ✅ 负责 | 自动排序 + **人可插队** |
| Provider Selection | ✅ 负责（但受"能力可替换"约束） | 自动（依据：Provider 能力/成本/可用性）+ 人可覆盖 |
| Review Routing（谁审） | ✅ 负责 | 自动（默认"换一个 Provider 审"），**高风险 Work 强制人审** |
| Failure Escalation（升级） | ✅ 负责 | 自动升级 + **硬性 Gate**：③/④ 类失败必须上人 |
| Progress Synthesis（向 CEO 汇报） | ✅ 负责 | 自动（三段式：结论→原因→建议） |
| **写 Canonical Branch** | ❌ **不负责** | **必须 Gate**（违反 I3 / I6） |
| **改变项目范围/架构** | ❌ 不负责 | **必须 Gate**（L2 Gate 语义） |

### 5.3 Leader 的三个"不做"（防止 Leader 退化成超级 agent）

1. **不做理解的手工替代**——Codex 与 Claude Code 官方都把"never delegates understanding"列为反模式原文；Leader 必须**自己综合**再下发精确规格（含文件路径、行号、确切改动）。
2. **不做执行的最后一道**——Leader 不写代码。Claude Code 的 coordinator 也明确"worker 不能看到对话，每个 prompt 必须自包含"。
3. **不做状态的真源**——Leader 产出的是**指令与摘要**；状态必须来自事实（git / Provider 会话 / Workspace 登记表），参照 AO"状态读取时派生、绝不存储"。

---

## 6. 遗留未知

| # | 未知 | 建议 |
|---|---|---|
| U10 | Project Context 的"地图文件"在 Curis 中叫什么、放在哪 | 建议沿用仓库内约定（`AGENTS.md` 式的 Curis 项目地图），Curis 侧只存指针 |
| U11 | Conversation 归档后是否仍注入给 Employee | 建议**注入摘要，不注入全文**（Codex `/compact` 同思路） |
| U12 | WorkResult 的归一化 schema 由谁定 | 建议 Curis 定义（这是 Curis 自有能力的核心之一），但**必须能无损承载任意 Provider 的 diff** |
| U13 | 是否允许 Leader 自动创建 Work 而不经人 | 建议：**允许，但首次/高风险需 Gate**；且 Work 清单必须随时可见可撤销 |
