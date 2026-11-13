# CURIS RD — MULTI-AGENT SOFTWARE DEVELOPMENT ORCHESTRATION：结论汇总（单一文档）

**Authority Class**: RESEARCH（**非 Authority；不得作为 Current Product / Implementation Truth**）
**Status**: Review
**日期**: 2026-09-19
**范围**: 只研究"多个 Coding Agent 长期协同开发同一个项目"在成熟系统中如何组织，并翻译成 Curis 产品与 Runtime 需求。
**未做**: 未修改 Curis Authority / Runtime / Code / RD HTML / Figma / Frontend / Backend；未 commit；未 push。
**本文定位**: 本轮研究的**唯一入口与完整结论**。原 11 份明细文档已归档至 `details/`（见 §11），仅供追溯；**结论以本文为准**。

---

## 0. 一页结论（只需读这一段）

1. **Curis RD 的本质是 "Multi-Agent Development Operating"，而不只是 "Orchestration"。**
   编排、隔离、并行、审查、沙箱——**要么 Provider 已做好（Codex / Claude Code / Copilot / OpenHands），要么开源项目已做好（Agent Orchestrator / container-use / worktrunk）**。Curis 不该重做。
   开源项目里**一个都没有**的是：**长期组织身份（Employee）、责任归属、跨 Provider 结果归一、独立验证、产品化 Decision Gate、跨会话长期运营状态**。**这才是 Curis 的 Owned 范围。**

2. **长期 Project Working Space 的正确答案：Canonical Project Root（唯一·资产）+ 每个 Work 一个隔离 Workspace（消耗品）。** 二者不可混为一谈。

3. **多 Agent 绝不应共享同一个 Working Tree。** 本领域 **10/10** 成熟实现无一例外；共享的是 repo 与 `.git` object store。

4. **隔离原语默认 `git worktree`；容器作为"按 Work 显式升级"的可选档位；Provider-native 工作区被否决**（会把 Curis 锁死在某一家）。→ **Option D**。

5. **Codex 与 Claude Code 都已把"单机多 agent 并行"做成产品原语**，但各自的协作层都是**自家封闭的**；Curis 只能在它们之上做**归一化**，不能把组织层建立在任一家的协作语义上。

6. **没有任何系统解决"跨 Provider 交接"。** 这是 Curis 少数的真实空位，也是 WorkResult 归一化 + 独立 Verification 的正当性来源。

7. **Curis 应当拥有 11 项能力；绝不重造 11 项。**

8. **RD 原型（`RD_WORKSPACE_HTML_EXPLORATION/`）需改 6 项产品表达，其中 3 项是结构性的**（Provider 被画成对话发言者 / "并行不互干扰"无机制支撑 / 状态挂在 Provider 上）。**先取一次 CEO 裁定，再改视觉；否则返工。**

**状态**：`RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW`

---

## 0.A Global Business Working Space Boundary（上游边界，2026-09-20 追加）

> 本节是**追加的上游边界说明**，**不修改本文其他任何结论**。

**结论一句话**：**本文研究的 RD Project Working Space，是全局 Business Working Space 之下的 Development 专业特化，不是同级或替代物。**

```
Business Working Space（全局 · 每个 Business 一个，长期资产生效地）
└── Development Professional Package（RD 的专业实现）
      └── Project（RD 内部的长期项目；R1 已裁定 Project 不升格）
            └── Canonical Project Root（本文 §4.1 的唯一工程真相源）
                  └── Execution Workspace（本文 §4.1 的 per-Work 隔离工作区，消耗品）
```

**三条边界**（本文哪些结论是"专业特化"、哪些是"全局"）：

| 本文结论 | 归属层级 | 说明 |
|---|---|---|
| Canonical Project Root / per-Work 隔离 Workspace / Git Worktree / Branch / Verification / Merge Gate | **Development 专业包内部** | **不是** Curis 全局 Business 规则。Music 与 Content Growth **不需要** worktree |
| Employee / Responsibility / Work / Result / Verification / Decision / Conversation 的语义 | **全局** | 与业务类型无关 |
| "隔离原语不得由 Provider 决定"、"多执行体不得共享同一 Working Tree" | **全局原则**，在 Development 下具体化为 worktree | 其他专业包按自身需要落地 |

**两条需要与本文一并裁定的修正**（详见上游文档 §14.1 G1 / G5）：
1. 本文所用 "Workspace" 一词与既有实现中的 `workspaces` 表（运行空间）**同词异义** → 建议本文将 per-Work 隔离工作区统一改称 **Execution Workspace**。
2. 本文 §4.1 的 Option A/D 图示把 worktree 画在 Canonical Project Root **之内** → 建议改为**放在业务资产根之外**（消耗品不应污染资产树）。

**上游文档**：`../business-working-space-baseline-2026-09-20/CURIS_BUSINESS_WORKING_SPACE_BASELINE_CANDIDATE.md`（Authority Class `RESEARCH`，Candidate，非 Authority）。

---

## 1. 研究定位、方法与证据等级

### 1.1 本轮要回答的唯一 P0 问题

Curis RD 已收敛为极简形态（Project Operating Header + Employee Work Surface + Employee Conversation + Result/Utility + Decision），但底层有一个未澄清的问题：

> 多个 Coding Agent 长期协同开发同一个项目，成熟系统到底怎么组织？Curis RD 应继承什么、复用 **开源运行时** 什么、自己拥有什么、绝不重造什么？

研究纪律：**不重复造轮子 / GitHub Source First / 先研究成熟实现，再翻译成 Curis 需求。**

### 1.2 方法（六步，可复现）

| 阶段 | 动作 | 工具 | 产出 |
|---|---|---|---|
| P0 | 建研究目录 + 独立实验目录；确认 `gh` 已登录 | Bash | 目录骨架 |
| P1 | 8 组 GitHub 关键词检索（`gh search repos --sort stars`） | gh CLI | 候选池 60+ |
| P2 | 对 34 个候选逐个 `gh api repos/...` 核验元数据 | gh API | `evidence/E01` |
| P3 | shallow clone 5 个编排器/隔离工具；读 architecture/源码/adapters | git + Read | `evidence/E03–E07` |
| P4 | Claude Code / Copilot cloud agent / OpenAI 官方工程文章 | WebFetch | L3/L4 证据 |
| P5 | 本机 Codex CLI 0.144.6 全量能力探测 | codex CLI | `evidence/E02` |

检索式（可复现）：`coding agent orchestrator` / `parallel coding agents` / `git worktree ai agent` / `multi-agent software engineering` / `ai software factory agent` / `agent teams claude code` / `orchestrator agent sandbox container`（均 `--sort stars`）。

### 1.3 证据等级

`L1` 本地真实运行 → `L2` 源码 → `L3` 官方文档 → `L4` 官方产品说明 → `L5` 第三方 → `L6` 推断。
**关键架构结论一律要求 L1 + L2；GitHub README 不能替代源码验证。** 本轮已按此执行（并因此**证伪了第三方博客 1 处说法**，见 §10）。

---

## 2. 术语定版（本研究的提案语义，待 CEO 裁定后方可进入产品表达）

| 术语 | 定义 | 不是什么 |
|---|---|---|
| **Canonical Project Root** | 项目的唯一工程真相目录（含 `.git`、源码、文档、测试、配置、项目指令）。物理上只有一份 | 不是"某个员工的工作目录" |
| **Repository** | Canonical Root 内的 git 仓库，历史与对象库的唯一持有者 | 不是"云端仓库"（v1 本地） |
| **Canonical Branch** | 被认定为"已收口"的分支（本地即 `main`）。**只有过 Gate 的 Work 才能进入** | 不是"默认分支"的别名 |
| **Workspace** | **一次 Work 的隔离工作目录**，从 Canonical Root 派生，完成后再回到 Canonical | ❌ 不是 Workspace（Curis 组织层的工作空间）；❌ 不是 IDE/Terminal |
| **Working Tree** | git 意义上某个分支的检出 | **禁止多个执行体共享同一个** |
| **Work** | 一个有目标、可验收的执行单元（带验收标准、所有权、结算） | 不是"待办清单里的一条" |
| **Assignment** | 一次执行指派（Work → Provider 会话） | 不是"Employee 的岗位" |
| **Provider** | 可替换的 coding agent 执行能力（Codex / Claude Code / OpenHands / Aider…） | **不是 Employee**（无长期身份、无问责） |
| **WorkResult** | 归一化结果 `{diff, files, test_evidence, unresolved, logs_pointer}` | 不是聊天记录、不是日志 |
| **Verification** | 独立于执行的验收（默认换一个 Provider 验） | 不是"agent 说自己完成了" |
| **Gate / Decision** | 进入 Canonical 或改变范围的**显式**批准点 | 不是"人点了 PR merge"这种隐式动作 |
| **Project Context (C1)** | 项目长期是什么（目标/架构/仓库/指令/决策/知识/历史/团队） | 不是"上下文窗口里的内容" |
| **Work Context (C2)** | 这一件工作要达成什么（需求/相关文件/依赖/期望结果/验收） | 不是 prompt |
| **Execution Context (C3)** | 这一次运行发生了什么（prompt/Provider/沙箱/进程/日志/工具状态） | **不是下一个 agent 的输入**（是证据） |
| **Conversation Context (C4)** | CEO ↔ Employee 的持续工作关系 | 不是运行日志、不是代码真相 |
| **Durable Fact** | 必须持久化的事实（活动态、终止态、绑定、检查点、Workspace 记录、Gate 记录） | 不是可派生的展示状态 |
| **Derived Status** | 读取时计算、**绝不存储**的展示状态 | 不是真源 |
| **`no_signal`** | 活着但拿不到任何活动回调 → **拒绝乐观** | 不是 idle |

---

## 3. 二十四个终答

### Q1. Curis RD 本质上是否应该被理解为 Multi-Agent Development Orchestration？

**是，但更准确是 "Multi-Agent Development _Operating_"（运行/经营），不只是 Orchestration。**
- 是 Orchestration：确实要面对"多执行体围绕同一长期项目并行工作"的全部工程问题（隔离、歧义、冲突、交接、恢复）。
- 但不止：编排问题**已被解决**（Provider + 开源 Orchestrator）。Curis 的增量在**组织层**——Responsibility、Accountability、Decision、长期运营状态。
- **判据**：只做编排，永远追不上 AO/Orca；只做组织而不解决"执行体如何安全并行"，自动化就是空话。**两者都要，自有部分在后者。**

### Q2. 长期 Project Working Space 应该是什么？

**Canonical Project Root（唯一，长期）+ 每个 Work 一个隔离 Workspace（消耗品）。** → §4.1。
**Project Root 是资产，Workspace 是消耗品**——这是本模型最重要的区分。

### Q3. Agent 生成的代码/文档最终归属哪里？

**先在 Workspace 产生 → 经 Gate 进入 Canonical Branch。**
唯一例外：被**显式授权**的窄通道（如文档勘误）可直接入 Canonical，但仍需 Gate。
**证据**：没有任何成熟系统允许执行体直接写 canonical 工作树——Claude Code 用**不可关闭的强制校验**阻止；Copilot 在平台层禁止推 `main`。

### Q4. 多 Agent 是否应该直接共享同一个 Working Tree？

**绝对不应该。** 10/10 成熟实现无一例外。共享的是 **repo 与 `.git` object store**，不是工作目录。（不变量 I2）

### Q5. Branch / Worktree / Clone / Sandbox 哪个更适合？

**它们不是四选一，而是三层不同职责：**
- **Branch** = 变化线（git 天然负责）
- **Worktree / Clone / Container** = 执行位（在哪个目录里改）
- **Sandbox** = 权限边界（进程能碰什么）

**裁定组合**：`Branch（work/<work_id>-<slug> + 记录 base SHA）` + `Worktree（默认执行位）` + `Sandbox（优先复用 Provider 权限档，必要时容器）`。
**Clone 不作默认**（磁盘翻倍 + 基线漂移 + 合并代价）。
证据：Claude Code / AO / Orca / claude-squad / worktrunk / parallel-code / vibe-kanban 全部用 worktree；container-use / Copilot / OpenHands / SWE-ReX 用容器。
⚠️ **重要更正**：Codex 官方明确"**worktree 隔离不保护密钥**"——关键在**权限**，不在隔离强度。

### Q6. Codex 当前已经解决哪些问题？

**已解决（L1 本机实测 + L4 官方）**：单机可编程 agent 运行时（`exec`）｜非交互代码审查（`review`）｜diff 落地（`apply` / `cloud apply`）｜会话生命周期（`resume` / `fork` / `archive` / `unarchive`）｜沙箱三档 + 审批三档｜`-C` 指定工作根 + `--add-dir`｜可被别的框架当 MCP server 调用｜**多 agent 已是 stable 特性（`multi_agent`）**｜`computer_use` / `browser_use` 均 stable｜hooks stable｜自动 compaction｜桌面 App 的 Local / Worktree 线程模型｜云任务（可指定分支/SHA，产出 diff）｜官方实测单任务可跑 6 小时+｜官方工程实践（AGENTS.md 当地图 + docs 作系统记录 + exec-plans + doc-gardening agent）。

**未解决**：**程序化创建隔离工作区**（CLI **没有** `--worktree`——L1 证伪第三方博客）｜跨 Provider 交接｜项目级长期编排｜组织与问责。

### Q7. Claude Code 当前已经解决哪些问题？

**已解决（L3 官方文档；本机未安装）**：worktree 一等公民（`--worktree`，落 `.claude/worktrees/<name>/`，默认分支 `worktree-<name>`）｜**不可关闭的强制隔离校验**（阻止编辑主 checkout、阻止 cwd/git 重定向回主 checkout）｜subagents（可 `isolation: worktree`）｜agent teams（共享任务列表 + **文件锁认领** + mailbox + **blockedBy 依赖自动解锁** + 权限冒泡）｜agent view（派发即自动搬进 worktree）｜cross-session messaging｜`/batch`（5–30 个 worktree 隔离 subagent 各开 PR）｜CLAUDE.md 项目记忆｜hooks。

**未解决**：Provider 中立（**workers 必须是 Claude 会话**）｜无自动 merge / PR｜`/resume` **不恢复 in-process teammate**｜**任务状态会滞后并卡死依赖**｜一个 session 只能一个 team、teammate 不能再生成 teammate｜权限在 spawn 时固定。

### Q8. 哪些开源项目真正值得复用？

| 排名 | 项目 | 复用方式 |
|---|---|---|
| 1 | **`Untrivial-ai/agent-orchestrator`** | **参考架构 + 适配层设计**（唯一九项全满足）；**不建议直接依赖其运行时**（外围越界） |
| 2 | **`dagger/container-use`** | 若需容器档位，作为**可当 MCP 工具复用**的隔离层（零 agent 绑定） |
| 3 | **`max-sixty/worktrunk`** | worktree 生命周期的**约定与坑清单**（`hash_port`、`copy-ignored`、hook 生命周期）；License 需法务确认 |
| 4 | **`OpenHands`** | 事件流 replay 模型 + **ACP 接外部 agent** 的思路 |
| 5 | `smtg-ai/claude-squad` / `johannesjo/parallel-code` | **设计参照**（`isExistingBranch`、symlink 依赖目录）；**claude-squad 是 AGPL-3.0，采用红线** |

### Q9. 是否存在可以直接作为 Curis 底层 Orchestrator 的项目？

**部分存在，但不建议直接采用。**
- `Untrivial-ai/agent-orchestrator`（12.1k★，Apache-2.0）是**唯一同时满足**九项（真操作 repo / 真多 agent / 真并行 / 长期项目状态 / Provider 无关 / local-first / License 可商用 / 活跃 / 可嵌入）的候选。
- 但：①外围（GitHub 绑定、Cloud、pricing、telemetry、mobile bridge）**超出 Curis v1 边界**；②它是"工程师管理台"，Curis 要的是"组织与问责"；③依赖它意味着 Curis 运行时跟着它的发布节奏走。
- **建议**：**借架构，不借运行时**。真正采用与否属 **L2 Gate**，需 CEO 裁定。

### Q10. Curis 应该自己拥有哪些能力？

**11 项**：Employee 身份与职责｜Employee ↔ Conversation 持续关系｜Work 的定义与生命周期｜Assignment｜Workspace 分配与回收｜Provider 抽象与路由（四槽）｜**WorkResult 归一化**｜**Verification（独立于执行）**｜Decision Gate｜长期运营状态｜升级与例外处理。→ §6

### Q11. Employee 与 Agent Process 如何映射？

**不映射为 1:1。** 正确映射是四层：

```
Employee（长期身份 / 责任归属）
  ↳ Work（可验收的执行单元）
      ↳ Assignment（一次执行指派 = Workspace + 一个 Provider 会话）
          ↳ Provider（可替换的执行能力）
```
- Employee **不拥有**工程资产；Work **不拥有**代码真相（只引用 Canonical Project）。
- **明确否决**：1 Employee = 1 Agent Process ｜1 Work = 1 Agent ｜Employee 拥有代码。

### Q12. 一个 Employee 多个 Work 如何执行？

**每个 Work 独立走完整的 Assignment → Workspace → Provider 链路，彼此隔离。**
证据：AO 的 orchestrator 会话可 spawn/redirect 多个 worker；Claude Code lead 可派多个 teammate + teammate **自领下一个未阻塞任务**。
**产品含义**：Employee Work Surface **不能是"一个员工一个终端"**，而应是"**一个员工手持 Work 清单，每份 Work 一个或多个执行槽位**"。

### Q13. 一个 Work 多个 Agent 如何执行？

**两种合法形态**：
- **并行竞争（择优）**：同一 Work 派生 N 个 Workspace，各跑不同 Provider，比较后择优。证据：**Orca README 原文** "Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner"。
- **串行接力（分工）**：Work → Assignment 1（实现）→ WorkResult → Assignment 2（补测试）→ …。证据：Codex `resume/fork`；AO `agent_switching` + `interface_transition`（**同一会话换 Provider 不中断，且"两个控制器绝不同时存活"**）。

### Q14. Context 如何分成 Project / Work / Execution / Conversation？

**四层定版** → §4.3。最要紧的两条约束：
- Claude Code 官方证实"**teammate 加载项目上下文但不继承 lead 对话历史**" → **上下文不自动继承是正确的默认**。
- Codex 官方证实"**AGENTS.md 应当是地图不是百科全书**"；"从 agent 视角看，它运行期间无法在上下文中访问的东西就不存在"。

### Q15. Agent 之间如何 Handoff？

**三种交接必须先分类**：H-A（同 Work 换执行体）/ H-B（Work → Work）/ H-C（Work → Canonical）。→ §4.3
**不要混用四种"消息"语义**：diff/commit（权威）≠ Artifact 摘要（可过期）≠ Message/Mailbox（协调信号）≠ Shared Task State（**会滞后**）。
**必须接受的事实**：**跨 Provider 标准交接协议不存在** → 这正是 Curis 的 Owned 空位。

### Q16. 并行修改冲突如何处理？

**三层防线，且必须诚实说明各层边界**：

| 层 | 能防 | **不能防** |
|---|---|---|
| L1 结构隔离（worktree/container per Work） | 同文件并发写覆盖 | **语义冲突**（各自测试都过） |
| L2 认领锁（任务级） | 同一任务被重复认领 | **文件写冲突**（Claude Code 官方原文："Locking applies to task claiming, not file writes."） |
| L3 收口检测（merge + 测试/CI） | 真实冲突在收口暴露 | **不会提前发现** |

**应做**：按**所有权**切分 Work（Codex 官方建议）+ 分配时做**文件集重叠预警** + 收口强制测试 + 把冲突当**正常状态**。
**不应做**：文件锁防写冲突（会把并行退化成串行）｜提前精确冲突预测（本领域无先例）。

### Q17. Review / Test / Merge 由谁负责？

| 环节 | 默认 | 高风险时 |
|---|---|---|
| **Review** | **换一个 Provider 的会话**来审 | 强制人审 |
| **Test** | 项目自身工具链；**由执行体触发**，**由 Verification 收集结论** | 同上 |
| **Merge** | **必须过 Gate**（不是执行的自然结尾） | 人 Gate |

**重要**：Curis **不建模**"PR 作为唯一通道"——v1 是单机本地自用，**Decision Gate 才是通道**。

### Q18. Agent 失败以后如何恢复？

**失败分 10 类**（F1–F10，见 §4.4 §1），恢复按**最便宜的先试**：`P1 会话级 resume` → `P2 分支级` → `P3 工作区级` → `P4 用自包含的 C2 重跑`。
**四类失败禁止自动恢复**：`blocked`（AO 明文禁止注入输入）｜`waiting_for_user`（沿用既有状态名，禁重试登录/绕 CAPTCHA/切账号）｜`effect_unknown`（禁盲目重放，既有 G4）｜`no_signal`（**显示"无信号"而不是乐观 idle**）。
**关键事实 F10**：Claude Code 官方承认 **"teammates sometimes fail to mark tasks as completed"** → **agent 自报完成不可靠** → 因此 **Verification 必须独立于执行**，且依赖必须有**超时兜底**。

### Q19. Provider 能否中途替换？

**能，但只到第 3 级；第 4 级不存在。**

| 层级 | 可行性 |
|---|---|
| L-a 换 Reviewer | ✅ 完全可行（diff 是 Provider 无关的） |
| L-b 换 Executor（同 Work 从零重跑） | ✅ 可行（前提：Work Context 自包含） |
| L-c 换 Executor（同 Workspace 接力） | ⚠️ 部分可行（前提：**前一个 Provider 已 commit**） |
| L-d 无损迁移**运行中会话** | ❌ **世界上没有系统做到** |

**替换时必须处理**：强制 commit/stash｜**权限档必须重新声明**（防降级后权限升级）｜项目上下文文件名的 Provider 投射（`AGENTS.md` vs `CLAUDE.md`）｜**替换后进入"待确认"而不是乐观 idle**｜**必须先终止旧执行体并验证终止**。

### Q20. 项目关闭第二天如何继续？

**依赖四件事，缺一不可**：①**会话可恢复** ②**状态可观测**（持久事实 + 派生状态 + `no_signal`）③**上下文可压缩** ④**决策不丢**。
**长期 vs 临时的判据**：**"如果第二天需要它才能继续工作，它就是长期；如果丢了只会损失时间，它就是临时。"**
**v1 边界**：**单机场景下"关机 agent 还在跑"是不成立的**——Curis v1 **不应承诺**这个能力（Copilot 的云执行是唯一形态，属 L2 Gate）。

### Q21. Git / GitHub 应该承担什么？

**Git 承担 9 项（Curis 绝不重造）**：版本控制、分支、worktree（隔离底座）、diff/patch、merge/rebase、**冲突检测（唯一权威）**、历史/reflog、hooks、ignore。
**GitHub（或任何远端）承担（可选）**：远端备份/多机同步、PR 作为评审界面、CI、branch protection、issue 作为任务源。
**v1 态度**：**本地 git 必需；远端可选；PR 不是必需通道**（Curis 的 Gate 是产品内对象）。

### Q22. 哪些东西绝对不要由 Curis 重新开发？

**11 项** → §6.6。

### Q23. 当前 RD HTML 哪些产品表达可能因此需要修改？

**6 项，其中 3 项结构性** → §8。

### Q24. 是否已经足够进入 RD 定向视觉修订？

**研究层面已足够；建议先取 CEO 一次裁定，再进入视觉修订。** → §9

---

## 4. 四个核心模型

### 4.1 Project Working Space 模型

#### 4.1.1 八条不变量（任何候选方案都必须满足）

| # | 不变量 | 依据 |
|---|---|---|
| I1 | **Canonical Project Root 永远只有一份**，且是唯一工程真相源 | 全部 10 个成熟实现 |
| I2 | **同一 Working Tree 不得被两个执行体同时写入** | 全部 10 个实现无一例外 |
| I3 | **执行体不得直接写 Canonical Branch** | Copilot（只能推 `copilot/*`）；Claude Code（强制隔离校验） |
| I4 | **Workspace 是消耗品**：可销毁、可从 Canonical 重建、销毁不损失已收口成果 | container-use "discard failures instantly" |
| I5 | **每个 Workspace 必须记住自己的 Base Ref/SHA**（否则 diff 无意义） | AO `SessionMetadata.DiffBaseSHA / DiffBaseRef`（源码级） |
| I6 | **收口必须经过显式 Gate** | Copilot（人审批）；Claude Code（无自动 merge） |
| I7 | **隔离强度必须可配置**，不写死一种 | Codex `-s read-only\|workspace-write\|danger-full-access`；AO `workspace/router` |
| I8 | **Workspace 生命周期必须有 owner** | Claude Code worktree 清理规则；worktrunk `wt remove` |

#### 4.1.2 四种候选

**Option A — Single Project Root + Git Worktree per Work**
```
Canonical Project Root
├── .git/                     ← 唯一 object store，全部 worktree 共享
└── <worktree 1..N>           branch: work/W-00N-<slug>   base: <sha>
```
Context continuity 最高｜隔离中等（共享工具链/端口/依赖）｜磁盘低｜Git 复杂度中｜**Provider 兼容性最高**（任何 CLI agent 只需 `cd <worktree>`）｜恢复好｜业界验证最强。

**Option B — Canonical Repo + Sandbox / Clone per Agent Execution**
隔离最高（文件系统+进程+网络全隔离）｜**磁盘高**｜**合并复杂度高**（需 cross-repo 推送/patch）｜基线漂移风险｜业界少数派（container-use / Copilot / OpenHands / SWE-ReX）。

**Option C — Provider-native Workspace**（消费 Codex App 线程 / `claude --worktree` / OpenHands workspace）
Git 复杂度最低，但 **Merge 复杂度最高且不可控**（不同 Provider 落在不同位置、不同分支命名、不同清理规则）；**Provider 兼容性最差**——Claude Code 的 worktree 只有它自己认；**Codex 的 App worktree 甚至不能被 CLI 调用**。**与 Curis 硬约束"能力可替换不写死"直接冲突 → 必须否决。**

**Option D（研究新增，推荐）— Hybrid：Canonical Root + Worktree 默认底座 + 容器可选档位 + Provider-native 仅作加速**
```
Canonical Project Root
└── Workspace Allocator（Curis 拥有）
    ├── 默认 → git worktree（继承 Option A 全部优点）
    ├── 需要强隔离 → 容器（按 Work 显式选择）
    └── Provider 原生更优 → 允许自建，但必须登记回 Curis（Workspace Registry）
```

#### 4.1.3 推荐：Option D（以 A 为默认底座的混合模型）

理由（每条有证据）：
1. **C 必须否决**——它把"工作区形态"交给 Provider 决定，违反"能力可替换不写死"。实证：`codex --help` **不存在** `--worktree`（L1）；Claude Code worktree 锁在 `.claude/worktrees/` 且只有它认。
2. **B 不作默认**——隔离更强但磁盘与合并代价高；Curis v1 是单机本地自用，引入容器运行时是额外依赖。
3. **A 是默认底座**——本领域压倒性主流，且坑**已被三个开源项目填平**（`hash_port` 端口唯一化 / symlink 或 copy-ignored 共享依赖 / `isExistingBranch` 分支复用策略）。
4. **D = A + 按需升级**——在同一套 Workspace Registry 下允许"这个 Work 用容器"。
5. **与既有裁定不冲突**——Project **不升格**（`Company→Department→Business→Workspace` 不变），Project 仍是 RD Workspace 内的 Project Context；本模型只把"Project Context 的物理形态"定义清楚。

**Workspace 生命周期（7 步）**：
```
① ALLOCATE   Work 创建 → 分配 Workspace（决定 strategy / base_ref / branch_name）→ 生成 WorkspaceRecord
② READY      依赖就绪、端口已分配   ⚠️ 此步之前不得启动 Provider
③ RUN        Provider 会话在 Workspace 内执行
④ SETTLE     Work 结束 → 统一产出：diff + 文件清单 + 测试结果 + 日志指针
⑤ REVIEW     由"另一个 Provider 会话"或人执行
⑥ INTEGRATE  通过 Gate → 进入 Canonical Branch（未通过 → 不得进入）
⑦ RECLAIM    保留 / 销毁；锁必须先释放；被复用的既有分支不得删除
```

**WorkspaceRecord（提案字段，供 Runtime 设计参考——非 Authority）**：
`workspace_id` / `work_id` / `project_id` / `strategy(worktree|container)` / `repo_path` / `workspace_path` / `branch_name` / `base_ref` / `base_sha` / `is_reused_branch`（决定回收时是否可删） / `allocated_port` / `lock_state` / `provider_binding`（可中途替换） / `created_at` / `reclaimed_at` / `reclaim_policy`。
> 证据来源：AO `adapters/workspace/*` + `SessionMetadata`；claude-squad `branchName` / `baseCommitSHA` / `isExistingBranch`；worktrunk `hash_port`。

**明确不采纳的三种"简化"**：❌ 所有 Work 共享 Canonical Working Tree（违反 I2）｜❌ 文件锁防写冲突（Claude Code 官方证明其语义边界，且会把并行退化为串行）｜❌ 让 agent 直接 commit 到 Canonical Branch（违反 I3）。

#### 4.1.4 与 Curis v1 边界的对齐检查

| 检查项 | 结论 |
|---|---|
| 引入物理多租户 / 对外售卖？ | ❌ 无（Workspace 是本机目录） |
| 引入新版费 / 订阅依赖？ | ❌ 无（Option D 默认零外部依赖） |
| 把 Project 升格为组织层级？ | ❌ 无 |
| 引入多人真实协作？ | ❌ 无 |
| 与"能力可替换不写死"一致？ | ✅ 一致，且**优于** Option C |
| 与"全自动任务流是核心"一致？ | ✅ 一致（Workspace 分配/回收、结果归一、Gate 路由正是自动化缺口） |

### 4.2 Agent Workspace 与 Git 模型

#### 4.2.1 四种原语的真实分工

| 原语 | 关键事实 | Curis 结论 |
|---|---|---|
| **Branch** | git 天然负责变化线/提交图/冲突权威；命名约定：Claude Code `worktree-<name>`、Copilot `copilot/*` | **一律 `work/<work_id>-<slug>`** + 显式记录 base ref/SHA；**不自建分支状态机**，状态从 `git merge-base` / `rev-list` **派生** |
| **Worktree** | 共享 `.git`（object store + refs）；不共享工作目录/index/HEAD。已解决的坑：端口冲突（`hash_port`）、依赖重复安装（symlink / `copy-ignored`）、误删既有分支（`isExistingBranch`）、并发清理（`git worktree lock`）。已暴露限制：`.claude` 为 symlink 时拒绝创建；Git LFS 只拿指针；hook 的 `${CLAUDE_PROJECT_DIR}` **仍指向主 checkout** | **v1 默认执行位**；**"工作区路径"必须是一等字段**，不能从 cwd 猜 |
| **Clone** | 完全独立 remote/refs；但磁盘翻倍 + 基线漂移 + 回传靠 push/patch 易丢 base | **不作默认**；仅"放到另一台机器/容器"时用（即 Option D 容器档） |
| **Container / Sandbox** | container-use（每 agent 一容器一分支，`flock.go` 互斥）；Copilot（每任务一 Actions 容器）；OpenHands（三档）；SWE-ReX（独立沙箱执行接口）。**Codex 官方警告：worktree/容器隔离不能保护密钥** | **按 Work 显式升级的档位**；**比容器更重要的是权限档位与 push 目标限制** |

**Copilot 的安全设计（最完整样板）**：①agent **只能推 `copilot/*` 前缀分支**；②agent 创建的 PR 上 **Actions 不自动运行**，需有写权限的人显式批准（防偷 secrets）；③环境**每次迭代重建**。

#### 4.2.2 文件归属（五类）

| 文件类型 | 生成位置 | 归属判定 | 未过 Gate 时 |
|---|---|---|---|
| **Code** | **只在 Workspace 内产生** | 过 Gate → 进 Canonical Branch | 保留在 Workspace 分支，**永不进 Canonical** |
| **Docs** | 项目真相类（架构/决策/计划）**应直接入 Canonical**（走小 PR）；本次工作的产出文档在 Workspace 内产生 | 同 Code | 同 Code |
| **Tests** | 与 Code 同仓同时产生 | 同 Code（测试与实现必须同一变更集） | 同 Code |
| **Config** | ⚠️ **高敏**：机器级/凭据级配置**永不入 Workspace**（同 Copilot 的 secrets 只在 setup 阶段原则） | 项目级配置走 Code 规则；机器级由 Curis 单独管理 | — |
| **Assets** | Workspace 内可产生 | ⚠️ 需单独策略：**大文件不入 git**，用 artifact store | 保留在 Workspace |

**三条硬规则**：
1. **写 Project Root 还是 Workspace？** → **一律先写 Workspace**（唯一例外：显式授权的窄通道，且仍需 Gate）。
2. **Merge 是独立、显式的动作**，不是执行的自然结尾 → 建模为 **Gate（Decision）**，与既有 `Decision 内嵌 Banner` 对齐。
3. **失败 Execution 的文件默认保留**（worktree 的失败产物含诊断价值）→ `FAILED` 保留至保留期结束，用户可选"保留为参考"或"立即销毁"。

**Conversation 附件 / 临时 Artifact / Project 归档**：
Conversation 附件属 **C4，不入 git**，落本地 `attachments/`；若要进工程必须**显式导入** Workspace 并在变更集出现。临时 Artifact 落 Workspace 外的 artifact 目录，**同生命周期**，被 Result 引用时只存**指针**。Project 归档：Canonical Root 归档（**不物理删除 `.git`**）；Workspace 全部销毁；**Conversation 与 Decision 记录必须保留**。

#### 4.2.3 Git / GitHub 分工

**Git 天然负责（Curis 绝不重造）**：提交图｜object store（worktree 共享底座）｜diff/patch（**Provider 交出的统一结果格式**）｜merge/rebase｜**冲突检测（唯一权威）**｜reflog/历史｜worktree｜lock｜ignore｜hooks（本地强制门禁的天然位置）。

**GitHub（可选）**：远端备份/多机同步 ✅｜PR 作为评审界面 ⚠️ 可选（**Curis 内建 Decision Gate 才是必需**）｜CI ⚠️ 可选（本地测试优先）｜branch protection ⚠️（本地等价物 = 分支所有权规则 + Gate）｜Issue 作为任务源 ❌ v1 不需要。

### 4.3 Context 四分层、Handoff 与责任映射

#### 4.3.1 四层 Context（术语定版）

| 层 | 一句话定义 | 时间尺度 | 存储 / 权威载体 |
|---|---|---|---|
| **C1 Project Context** | 项目**长期是什么**：目标、架构、仓库、指令、决策、知识、历史、团队 | **月-年** | **必须首先落在仓库里**（随代码版本化）：`AGENTS.md` 式地图（**约 100 行、只当地图**）+ 结构化 `docs/` 真相 + `docs/exec-plans/{active,completed}` + `tech-debt-tracker.md`；**由 linters + CI 机械校验**；**周期性 doc-gardening agent** 扫描陈旧文档。Curis 侧只存 `ProjectContextRecord`（指针 + 摘要 + 新鲜度），**不复制仓库内容** |
| **C2 Work Context** | 这一件工作**要达成什么**：需求/验收标准/相关文件与契约/依赖/执行策略/结果约定 | **小时-天** | Curis 侧**持久事实**（**不含 prompt、不含日志、不含对话全文**）。参照 AO：`SessionKind`/`Branch`/`WorkspacePath`/`DiffBaseSHA`/`activity_state`/`is_terminated` 才是 durable。**必须自包含** |
| **C3 Execution Context** | 这一次运行**发生了什么**：prompt、Provider 版本、Workspace+base SHA、进程/会话 id、工具事件流、日志、权限档、token/成本 | **分钟-小时** | append-only 事件流（OpenHands EventLog 最完整：单一真相源、可增量确定性 replay）。结束即冻结为**只读记录**。**默认不注入给下一个 Execution——日志是证据不是输入** |
| **C4 Conversation Context** | **CEO ↔ Employee 的持续工作关系**：说过什么、答应过什么、为什么这样决定、附件、工作习惯 | **月-年（跨 Work）** | Curis 持久记录。**默认不被 Provider 会话读取**；Project 归档后仍保留（问责记录） |

**关系**：**C1 ⊃ C2 ⊃ C3**；**C4 横向跨越全部**（一个人可在多个 Work、多个 Project 上与同一 Employee 对话）。
**两条被官方证实的约束**：①Claude Code 官方——teammate 加载项目上下文与 spawn prompt，**但不继承 lead 的 conversation history** → **"上下文不自动继承"是被验证过的正确默认**；②Codex 官方——`AGENTS.md` **应当是地图不是百科全书**，"give Codex a map, not a 1,000-page instruction manual"；"**From the agent's point of view, anything it can't access in-context while running effectively doesn't exist.**"
**反模式**：❌ 把 Project Context 放进某个 Conversation（会被 archive/compact）｜❌ 做成一个巨大指令文件｜❌ 把 C3 日志当作下一个 agent 的输入。

#### 4.3.2 Handoff 三类

| 类型 | 定义 | 成熟系统做法 | Curis 应采纳 | 交接物 | 明确不传 |
|---|---|---|---|---|---|
| **H-A 同 Work 换执行体** | 任务不变、上下文继续（含崩溃重启） | Codex `resume`/`fork`；AO `agent_switching` + `native_checkpoint` + `interface_transition`（两控制器**绝不同时存活**） | ✅ **必须支持** | base SHA + 已产生 diff（先 commit/stash）+ **C3 检查点** + 结构化进度摘要 | 原始日志全文、完整对话历史 |
| **H-B Work → Work** | A 完成后 B 开始，需要 A 的成果 | 全部系统走 PR/diff/commit；AO 由 orchestrator 综合后主动递上下文 | ✅ **必须支持** | **commit/diff（首选）** + 文件清单 + 测试结果 + 未解决项与风险 | "based on your findings" 式模糊指令（Codex/Claude 官方均列为反模式） |
| **H-C Work → Canonical** | 成果进入项目真相 | AO `mergeable/merged`；Copilot PR + 人审批；Claude Code **无自动 merge** | ✅ 建模为 **Gate（Decision）** | diff/commit + 验收证据 + Decision 记录 | — |

**四种"消息"语义不要混用**：
| 机制 | 语义 | 可靠性 | Curis 用途 |
|---|---|---|---|
| Diff / Commit / Patch | 变更的**权威表示** | 高（git 保证） | H-B / H-C 主通道 |
| Artifact 文件 / summary | 结构化**摘要** | 中（可丢失/过期） | H-B 辅助；**必须可追溯到 diff** |
| Message / Mailbox | **协调信号** | 中→高（Claude Code 规则：**写成功才算已发送**） | 运行中协调、升级、请求 |
| Shared Task State | 工作分配状态 | ⚠️ **低（官方承认状态会滞后）** | 仅在"多执行体抢任务"时用；**必须保留人工/超时兜底** |

**→ Curis 的定位出现**：**Curis 应当是"跨 Provider 交接的归一化层"**——把任何 Provider 的产出统一为 `WorkResult = {diff, files, test_evidence, unresolved, logs_pointer}`，再交给下一个 Provider。**这是 Curis 真正需要自己做的少数几件事之一。**

#### 4.3.3 责任映射与三种合法形态

**四层链路**（§3-Q11）+ 三个此前缺失的环节：**WorkResult 归一化**、**Workspace 归属**（属 Assignment 不属 Work）、**Gate 位置**（Verification 之后、Canonical 之前）。

**明确否决**：❌ 1 Employee = 1 Agent Process（会把 Curis 锁进单一 Provider 的会话模型）｜❌ 1 Work = 1 Agent（一个 Work 可由多 agent 协作、可换代）｜❌ Employee 拥有代码（违反 I1/I3，且"员工离职=代码失踪"）。

**三种合法形态**：
1. **1 Employee → N Work（并行）**：证据 AO orchestrator spawn/redirect 多 worker；Claude Code lead 派多 teammate + **teammate 自领下一个未阻塞任务**。
2. **1 Work → N Provider（并行竞争/择优）**：证据 Orca README 原文；Codex 官方"同一 diff 请多个 reviewer agent 各自审查"。
3. **1 Work → N Provider（串行接力/分工）**：证据 Codex `resume/fork`；AO `agent_switching` + `interface_transition`。

> **产品含义**：RD 的 Employee Work Surface **不能**是"一个员工一个终端"，而应是"**一个员工手持一份 Work 清单，每份 Work 可有一个或多个执行槽位**"。

#### 4.3.4 Leader 模型

**成熟系统里 Leader 类角色的真实分工**：Planner/Orchestrator（AO `SessionKind=orchestrator`：组合规划历史 + 仓库上下文 + 实时状态，拆任务并 spawn worker）｜Manager/Lead（Claude Code team lead：spawn teammates、创建/指派任务、收权限冒泡、发起 shutdown，**固定不可换**）｜Supervisor（OpenHands/Copilot 的平台层：workspace、workflow、governance、审计与预算——**是平台不是 agent**）｜Reviewer（`codex review`、AO `adapters/reviewer`、Claude Code cross-check）｜Workflow script（Claude Code dynamic workflows：**由脚本而非模型逐轮判断持有计划**）｜Doc-gardening agent（Codex 官方实践）。

**Curis Leader 应负责什么**：

| 职责 | 自动 / Gate |
|---|---|
| 目标理解（把 CEO 的话变成可验收目标） | ⚠️ **首次必须 Gate**——目标被误读代价最高 |
| Work Breakdown | 自动（可撤销），但**拆解结果须在 Work Surface 可见** |
| Assignment（派给谁/哪个 Provider） | 自动（默认 Provider + 显式覆盖） |
| Dependency | 自动；**必须带超时兜底**（Claude Code 的"状态滞后卡死依赖"是已发生的失败模式） |
| Priority | 自动 + **人可插队** |
| Provider Selection | 自动（能力/成本/可用性）+ 人可覆盖 |
| Review Routing | 自动（默认"换一个 Provider 审"），**高风险强制人审** |
| Failure Escalation | 自动升级 + **硬性 Gate**：③/④ 类失败必须上人 |
| Progress Synthesis | 自动（三段式：结论→原因→建议） |
| **写 Canonical Branch** | ❌ **不负责 → 必须 Gate**（违反 I3/I6） |
| **改变项目范围 / 架构** | ❌ 不负责 → **必须 Gate**（L2 Gate 语义） |

**Leader 的三个"不做"**：①**不做理解的手工替代**——Codex/Claude 官方都把"never delegates understanding"列为反模式原文，Leader 必须**自己综合**再下发精确规格（含文件路径、行号、确切改动）；②**不做执行的最后一道**——Leader 不写代码，且"worker 看不到对话，每个 prompt 必须自包含"；③**不做状态的真源**——Leader 产出指令与摘要，状态必须来自事实（git / Provider 会话 / Workspace 登记表），参照 AO"状态读取时派生、绝不存储"。

### 4.4 失败恢复与长期运行模型

#### 4.4.1 失败十分类

| 类 | 失败 | 可自动恢复 | 手段 | 证据 |
|---|---|---|---|---|
| **F1** | Agent 崩溃 / 进程被杀 | ✅ | 重启执行体（Workspace 与分支仍在） | AO `Runtime Reaper` + detached host；claude-squad `r` |
| **F2** | 超时 | ⚠️ 部分 | 延长 / 换 Provider 重跑 | Codex 官方"单任务可跑 6 小时+"→ 阈值不能设太短 |
| **F3** | 上下文超限 | ✅ | Provider 自身 compaction | Codex `/compact` + `remote_compaction_v2`；OpenHands Condenser |
| **F4** | Provider 错误 / 限流 / 额度耗尽 | ✅ | **换 Provider 重跑（L-b）** | 多 Provider 已是常态（AO 30+ 适配器） |
| **F5** | 测试失败 | ✅ | 交回同一执行体迭代（**是正常循环不是异常**） | Copilot：同一会话内迭代直到通过 |
| **F6** | 合并冲突 | ✅（需判断） | 优先让 agent 解决 | Copilot 官方把 "Resolve merge conflicts" 列为 agent 能力 |
| **F7** | **权限 / 审批阻塞** | ✅ 但**不得自动化** | 上浮给人；**绝不自动注入输入** | AO 原文："automation must never inject input into a blocked session" |
| **F8** | **需要登录 / 凭据** | ❌ | 停止 → 存位置 → 通知人 → 等人 | 沿用 `WAITING_FOR_USER`（**不得另造状态名**） |
| **F9** | **状态未知**（hook 断） | ❌ | **显示"无信号"**，不乐观 idle | AO `StatusNoSignal` 原文："cannot tell whether the agent is working or stuck … Rendered instead of a confident idle." |
| **F10** | **自报完成但实际未完成** | ❌ | **必须外部验证** | Claude Code 官方："teammates sometimes fail to mark tasks as completed, which **blocks dependent tasks**" |

> **F10 最重要**：它同时解释为什么 Curis 需要 **Verification 独立于执行**、以及为什么 Work 状态**不能由 agent 自己声明**。

#### 4.4.2 状态模型：只有两类东西该被持久化

| 类别 | 内容 | Curis 对应 |
|---|---|---|
| **Durable Facts** | `activity_state`（`active / idle / waiting_input / blocked / exited`）｜`is_terminated`｜执行体绑定（Provider + 会话句柄 + generation）｜接口/执行槽切换检查点｜Workspace 记录（path/branch/base/lock）｜Gate/Decision 记录｜Review 与验证结果 | Curis Runtime 持久层 |
| **Derived Status**（读取时计算、**绝不存储**） | `working / needs_input / ci_failed / review_pending / changes_requested / approved / mergeable / idle / exited / terminated / no_signal / pr_open / draft / merged` | **UI 展示层** |

**理由（AO 原文）**："Display status is never stored. It is computed at read time from durable facts." → 状态永不与事实不一致；不需要状态迁移事务；新增展示状态不影响持久层。

**必须精确定义的四个状态语义**：`waiting_input`（停在空 prompt 等指令）｜`blocked`（停在**待批准决策**，**禁止注入任何输入**）｜`no_signal`（活着但从未收到 hook 回调 → 禁止显示为 idle、禁止自动判定失败重跑）｜`effect_unknown`（Curis 既有 G4：写已发出结果未知，**禁止盲目重放**）。**`waiting_for_user`（Curis 既有词）**：需要人（登录/凭据/业务决策），**禁止重试登录、绕 CAPTCHA、切账号**。

#### 4.4.3 三层检查点 + 恢复决策树

| 层 | 检查点 | 代价 | 何时用 |
|---|---|---|---|
| **P1 会话级** | Provider 原生 `resume` | 最低 | F1/F3，且**仅当会话句柄仍有效** |
| **P2 分支级** | 已 commit 的分支 + base SHA | 低 | F1/F2/F4/F5/F6 —— **Curis 主力恢复层** |
| **P3 工作区级** | Workspace 目录 + 未 commit 变更 | 中 | P1/P2 都不行；**未提交变更不可靠**，只作参考 |
| **P4 重跑** | 用**自包含的 C2** 重建 Workspace 重跑 | 高 | 兜底（这正是"Work Context 必须自包含"的理由） |

```
检测到 Work 未完成
├─ blocked / waiting_for_user / effect_unknown → 上浮给人（禁止自动化）
├─ no_signal                                   → 先探活，无法判定 → 上浮人
├─ 有有效会话句柄                              → P1 resume
├─ 有已 commit 的分支                          → P2 在新 Workspace checkout 继续
├─ 只有未提交变更                              → P3 保留 Workspace 供人判断
└─ 什么都没有                                  → P4 用自包含 C2 重跑
```

**明确"不做"的恢复**：❌ 自动重放 `effect_unknown`（重复副作用）｜❌ 在 `blocked` / `waiting_for_user` 上自动重试｜❌ 用日志（C3）重建上下文后重跑（噪声与幻觉）｜❌ 无限重试（必须**限次 + 限时 + 限成本**）。

#### 4.4.4 Long-running：什么长期保存、什么只是临时

| 类别 | 内容 | 生命周期 |
|---|---|---|
| **长期（项目寿命）** | Canonical Project Root（含 `.git`）｜仓库内项目地图与 `docs/`（含 exec-plans 历史）｜**Decision / Gate 记录**｜**Conversation Context**（问责记录）｜已归档 Work 与其 WorkResult | 月-年 |
| **中期（Work 寿命）** | Work Context｜Workspace 记录（base SHA、branch）｜Review / 验证结论 | 小时-天（+ 保留期） |
| **临时（执行寿命，结束即冻结/销毁）** | Execution Context（prompt / 事件流 / 日志 / 工具状态）｜Workspace 目录本身｜Provider 会话进程 | 分钟-小时 |

**判据**：**"如果第二天需要它才能继续工作，它就是长期；如果丢了只会损失时间，它就是临时。"**

**"第二天如何继续"的五个具体场景**：①昨天有 Work 在跑 → Workspace 记录 + 分支 commit + 会话句柄（可能已失效）；②卡在等人 → **Gate/Decision 记录必须持久**；③在等我做技术决策 → **Decision 必须在产品里可见且未决**；④**"关机 agent 还在跑吗" → 单机场景下不会**（Curis v1 不应承诺，Copilot 云执行是唯一形态，属 L2 Gate）；⑤三个月后想知道为什么这么决定 → **Decision 记录 + exec-plans 历史**。

**长期运行四个必备能力（缺一不可）**：会话可恢复｜状态可观测（Facts 持久 + Status 派生 + `no_signal` 显式化）｜上下文可压缩｜决策不丢。

**Workspace 回收策略（提案）**：`COMPLETED + 已收口` → 立即回收｜`FAILED / ABANDONED` → **保留 N 天**（默认 7 天，用户可配）并明确标记｜`WAITING / BLOCKED` → **永不自动回收**｜复用既有分支的 Workspace → **回收时不删分支**｜**运行中锁定**，回收前必须确认锁已释放。

**可观测性最低标准**：每个 Work 必须能回答"现在在哪一步"（分配/就绪/执行/结算/评审/集成/回收）与"上一次外部可观测的活动是什么时候"；无法判定时必须显示 `no_signal`；每个失败必须落到**具名枚举**（不是一个笼统 `error`）。

---

## 5. 开源项目裁决

### 5.1 深挖入选（10）与落选对照（9）

**入选深挖**：Agent Orchestrator、Claude Code、Codex、GitHub Copilot cloud agent、OpenHands、container-use、claude-squad、worktrunk、parallel-code、Orca / vibe-kanban（并列编排器）。

**落选但记录理由**：

| 项目 | stars | 最近推送 | 落选理由 |
|---|---|---|---|
| `FoundationAgents/MetaGPT` | 70.5k | 2026-01-21 | **活跃度低（8 个月）**；本质是"SOP 角色扮演 + 产物生成"（`architect/engineer/product_manager/qa_engineer` + 线性流水线 write_prd→design_api→write_code→write_test→run_code），**不操作真实 repo 的 branch/PR/merge**。仅作语义参照 |
| `OpenBMB/ChatDev` | 34.3k | 2026-07-24 | 同上，chat-chain 模型，产物落自建 workspace，非真实 SCM 协作 |
| `SWE-agent/SWE-agent` | 20.4k | 2026-09-14 | 研究基础设施（单 agent + ACI），非多 agent 编排器；但沙箱层 `SWE-ReX`（593★，MIT）是关键参考 |
| `microsoft/autogen` | 61.0k | 2026-04-15 | 通用多智能体**会话框架**，非仓库协作编排；license `CC-BY-4.0` |
| `e2b-dev/E2B` | 13.9k | 2026-09-18 | 通用沙箱基础设施，无编排语义 |
| `humanlayer/humanlayer` | 11.6k | 2026-06-19 | 聚焦 HITL 审批通道（`NOASSERTION`），与 Human Gate 相关但不足以作编排基线 |
| `anomalyco/opencode` | 208.4k | 2026-09-18 | **是 Provider，不是 Orchestrator**（即"被编排的 Worker"） |
| `aaif-goose/goose` | 54.4k | 2026-09-18 | 同上，Provider/Worker 角色 |
| `crewAIInc/crewAI` | 58.7k | 2026-09-18 | 通用角色协作框架；coding-team 案例是**用法示例**而非仓库编排实现 |

### 5.2 每个深挖项目"一句话"

| 项目 | 一句话 |
|---|---|
| **Agent Orchestrator** | 一个**长期运行的本地 Go daemon**，监督多个并行 coding agent 会话，每个会话独占一个 git worktree，把"任务—会话—工作区—PR—CI—评审"绑成一个可派生状态的对象 |
| **Claude Code** | 把"多 agent 并行"做成**一套并列官方原语**（subagents / agent view / agent teams / dynamic workflows），每条原语配不同的隔离与通信语义 |
| **Codex** | 已**同时具备**三层："单机可编程 agent 运行时（CLI）"、"云任务（Cloud）"、"桌面工作台（App，含 Local vs Worktree 线程）"，且**多 agent 已是 stable** |
| **Copilot cloud agent** | **"issue → 分支 → draft PR"的托管异步 agent**，隔离下沉到**每任务一台 GitHub Actions 临时容器**，门禁下沉到分支保护与 PR 审批 |
| **OpenHands** | 最贴近 Devin 的开源自治软件工程平台，**核心是"极小 agent 内核 + 事件流单一真相 + 可替换 Workspace（本地/容器/远程）"** |
| **container-use** | **一个 MCP server**，让任何 MCP 兼容 agent 在**每个分支一个全新容器**里工作——把隔离从 worktree 升级为**容器 + 分支** |
| **claude-squad** | **tmux + git worktree 的终端多路复用器**，把"每个 agent 一个隔离工作区"做成极小的 Go 工具（**AGPL-3.0，采用红线**） |
| **worktrunk** | **不是编排器，而是"agent 时代的 git worktree 管道"**——把 worktree 当分支一样操作 |
| **parallel-code** | Electron 桌面应用，**一个任务 = 一个分支 + 一个 worktree + 一个 agent CLI + 一个 GUI 会话** |
| **Orca / vibe-kanban** | 平铺多 agent + 单处追踪 / 看板调度；**仅 README 与元数据级（L3/L4）**，未源码深挖 |

### 5.3 编排 / 隔离 / 交接 三轴对照（关键行）

| 项目 | 真·多 Agent 对同一 repo | 隔离原语 | 交接物 | 回主干通道 | Provider 可替换 |
|---|---|---|---|---|---|
| **Agent Orchestrator** | ✅ | **git worktree**（container 用于回收） | 会话 + orchestrator 综合上下文 + `handoff_artifact` | GitHub PR（派生 mergeable/merged） | ✅✅ **30+ agent / 30+ reviewer 适配器** |
| **Claude Code** | ✅ | **git worktree** + 强制隔离校验；**agent teams 不隔离** | subagent summary / mailbox JSON / 跨会话消息 | 人手动 merge；`/batch` 各开 PR | ❌ workers 必须是 Claude 会话 |
| **Codex** | ✅ | **git worktree**（App 线程级；CLI 无 flag）+ Cloud 托管环境 | `apply`/patch/diff/commit；exec-plans | 人 squash&merge（官方实践中 agent 常自合） | ⚠️ 中等（可作 MCP server 被编排） |
| **Copilot CA** | ⚠️ 每任务独立 agent（非协作团队） | **ephemeral Actions 容器** | **PR**（commit + description + session logs） | **PR + 人审批** | ❌ 平台锁定 |
| **OpenHands** | ⚠️ 支持 delegate，但**共享 workspace** | 三档（进程内 / Docker / Remote） | 单一 EventLog（可 replay） | 走 GitHub 集成 | ✅ 强（LiteLLM + **ACP 接 Claude Code/Codex/Gemini CLI**） |
| **container-use** | ✅ 通用（任何 MCP agent） | **容器 + 每 agent 一分支** | 命令历史 + 日志 + 分支 | `git checkout <branch>` 人审后 merge | ✅✅ **完全不绑定 agent** |
| **claude-squad** | ✅ | **worktree + branch + tmux** | diff 视图 | 手动 merge | ✅ 任何终端 CLI |
| **worktrunk** | ❌ 非编排器（是 worktree 管道） | **git worktree**（分支寻址） | 无（只管生命周期 + hooks） | `wt merge`（squash+rebase+ff+cleanup） | ✅ 工具无关 |
| **parallel-code** | ✅ | **worktree + 分支 + symlink 依赖** | GUI diff 审阅 | GUI merge to main | ✅ Claude/Codex/Gemini/Copilot CLI |
| **Orca** | ✅ | **worktree per agent** | 单处追踪 + 移动通知 | 比较 diff 后 merge 胜者 | ✅ "25+" |
| **vibe-kanban** | ✅ | worktree（描述级） | 看板卡片 | 人收口 | ✅ 任意 coding agent |
| **MetaGPT / ChatDev** | ❌ 角色扮演流水线 | 自建 workspace **目录** | 文档产物 | 无 | ❌ 内部角色固定 |
| **SWE-agent** | ❌ 单 agent | **SWE-ReX 沙箱** | patch | 无 | ⚠️ 模型可换 |

### 5.4 10 条已被反复验证的事实

1. **Canonical Repository 唯一**——都是"一个仓库（或它的 clone）"作为唯一工程真相源。
2. **并行 = 每个 Work 一个隔离工作区**——没有任何成熟系统让两个 agent 共享同一 working tree。
3. **git worktree 是主流原语**（Orca / AO / claude-squad / Claude Code / worktrunk / parallel-code / vibe-kanban）。
4. **容器/VM 是第二档隔离**（container-use / Copilot / OpenHands / SWE-ReX / Codex Cloud），代价是启动、磁盘与"环境即代码"负担。
5. **PR（或等价 diff+review）是唯一回主干通道**——没有系统让 agent 直接写 main。
6. **Review 的主流是"另一个 agent"+"人做最终 Gate"**；Codex 官方甚至把人从审查环节基本移除，只留优先级与验收标准。
7. **状态应当"由事实派生"，不应当"自己维护"**（AO `status.go` 最清晰）。
8. **失败要有专门枚举**：`no_signal`、`changes_requested`、`ci_failed` 存在的意义是**拒绝乐观**。
9. **上下文不会被自动继承**——"给下一个 agent 什么上下文"是一个显式的产品决策。
10. **长期项目记忆放在仓库里**（AGENTS.md + docs/ + exec-plans），而不是只放在产品数据库里——这样它可 review、可回滚、可机械校验。

### 5.5 "可直接作为 Curis 底层 Orchestrator"候选评估（九项尺度）

尺度：①真操作 repo ②真多 agent ③真并行 ④长期项目状态 ⑤Provider 无关 ⑥local-first ⑦License 可商用非传染 ⑧活跃 ⑨可被嵌入。

| 候选 | ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | 结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Agent Orchestrator** | ✅ | ✅ | ✅ | ✅ | ✅✅ | ✅ | ✅ Apache-2.0 | ✅ | ✅ | **唯一同时满足九项**——但属"工程师管理台"形态，需剥离 GitHub/云/移动/计费外围 |
| **OpenHands** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ MIT | ✅ | ✅ | 可作**执行器与 SDK 层**；多 agent 共享 workspace，不适合"并行改同一 repo" |
| **container-use** | ✅ | ❌ | ✅ | ❌ | ✅✅ | ✅ | ✅ Apache-2.0 | ⚠️ release 停滞 | ✅ | 可作**隔离层 MCP 工具**，不能作编排器 |
| **worktrunk** | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ⚠️ NOASSERTION | ✅ | ⚠️ | 可作 **worktree 生命周期层**，或仅作设计参照 |
| **claude-squad** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ **AGPL-3.0** | ⚠️ | ⚠️ | **AGPL 是采用红线**；仅设计参照 |
| **parallel-code** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ MIT | ✅ | ❌ GUI 为主 | 设计参照（symlink 依赖方案） |
| **Orca** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ MIT | 数据异常 | ❌ | 形态参照，不作复用 |
| **vibe-kanban** | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ Apache-2.0 | ✅ | ⚠️ | 看板形态参照 |
| **Codex CLI** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ Apache-2.0 | ✅ | ✅ | **是 Worker/Provider，不是 Orchestrator** |
| **Claude Code** | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | 未声明 | ✅ | ⚠️ | **是 Provider，且自带封闭编排层** |

### 5.6 隔离原语的工程代价对照

| 原语 | 磁盘 | 创建 | 依赖安装 | git 复杂度 | 合并复杂度 | 环境一致性 | 适合场景 |
|---|---|---|---|---|---|---|---|
| 同一 working tree（**不推荐**） | 0 | 0 | 0 | 无 | 无（但会互相覆盖） | 完美 | **仅限读密集/只读调研** |
| **git worktree** | 低（共享 object store） | 秒级 | **需处理**（symlink / copy-ignored） | **中** | 中 | 高 | **默认选择** |
| 独立 clone | 高（整份历史） | 慢 | 需重装或 symlink | 低 | 高 | 中 | 需完全独立 remote / 隔离网络 |
| 容器 | 中-高（镜像层） | 中 | 镜像内预置 | 低 | 中 | **完美** | 系统级依赖、危险实验、多语言环境 |
| VM / 托管沙箱 | 云侧 | 慢 | 云侧 setup steps | 低 | 中 | 完美 | 长任务离线、跨机器 |

> `git worktree` 的真实坑已被三个项目用代码解决——`worktrunk` 的 `hash_port`（端口唯一化）与 `wt step copy-ignored`、`parallel-code` 的 **symlink gitignored 目录**、`claude-squad` 的 `isExistingBranch`。**这三条对本领域是"已解决问题"，Curis 不需重新发明，但必须知道自己会撞上。**

---

## 6. Capability Decomposition（五类能力拆分）

| 归属类 | 数量 | 一句话 |
|---|---|---|
| **Provider-owned**（Codex / Claude Code / …） | 12 项 | **执行、隔离、审查、压缩、沙箱**——已由 Provider 做好，Curis 不得重造 |
| **Orchestrator-owned**（可复用开源 Runtime） | 6 项 | **并行会话监管、worktree 生命周期、四槽适配层**——有参考实现，可借设计甚至借用 |
| **Git-owned**（git / 远端） | 9 项 | **版本控制、diff、冲突检测、历史**——git 是唯一权威 |
| **Curis-owned**（必须自己拥有） | **11 项** | **组织语义、问责、Work 编排、归一化、Gate、长期运营状态** |
| **Human Gate**（必须人介入） | 7 项 | **范围/架构/凭据/商业/权限边界/高风险合并** |

### 6.1 Curis-owned（11 项）

| # | 能力 | 为什么必须 Curis 拥有 |
|---|---|---|
| **CO1** | **Employee 身份与职责**（Responsibility Holder） | 开源项目**没有"员工"**：AO 有 worker/orchestrator 会话但**不是长期组织身份**；Claude Code teammate 是**运行期进程**；Codex thread 是**会话**。Curis Employee 跨 Work、跨会话、跨 Provider 长期存在 |
| **CO2** | **Employee ↔ Conversation 持续关系** | 类比：无。Claude Code 明确"teammate 不继承 lead 对话历史"；AO 会话上下文不跨会话。**Curis 的 Conversation 是唯一"跨 Work 的关系记忆"** |
| **CO3** | **Work 的定义与生命周期**（目标/验收/依赖/所有权/结算） | 各系统有 task/session/issue，但**都不含"验收标准 + 所有权切分 + 结算归一"**这组语义 |
| **CO4** | **Assignment（Work → Provider 指派）** | 开源系统里 agent 是"选出来的"，不是"指派给某个负责人的" |
| **CO5** | **Workspace 分配与回收** | AO 的 worktree 绑定"工程师手动建 session"；Claude Code 靠**用户敲命令**。**没有系统按"Work 语义"自动分配隔离工作区** |
| **CO6** | **Provider 抽象与路由（四槽位）** | AO 有 30+ 适配器，但**为单机工程师设计**，不含"能力/成本/可用性/用户偏好"的路由语义。Curis 需要**路由决策**，不是适配器列表 |
| **CO7** | **WorkResult 归一化**（diff + 证据 + 未解决项 + 日志指针） | **跨 Provider 交接协议不存在**。各 Provider 产物形态不同（Codex patch/apply、Claude Code 无自动 PR、container-use 分支）→ **归一化层是空位** |
| **CO8** | **Verification（独立于执行的验收）** | AO 有 reviewer 适配器，但触发是"看板有人点"；Curis 需**按 Work 定义自动触发**，且必须解决 F10 |
| **CO9** | **Decision Gate（含内嵌 Banner）** | 开源系统的 Gate 是"人点 PR merge"或"人批准权限"；**Curis 的 Gate 是产品对象**（未决决策必须可见、可追溯、可阻塞） |
| **CO10** | **长期运营状态**（项目事实持久 + 状态派生 + 审计） | AO 有 durable facts，但那是单机工程师的看板状态；Curis 需要"**为什么这么做**"的问责记录 |
| **CO11** | **升级与例外处理** | 开源系统把人当"操作员"；Curis 需要**预算/权限/范围/合规的例外路径**（对应既有 L2 Gate 7 项） |

**设计参照（不是从零想）**：CO3 ← Claude Code task（三态 + blockedBy + 自动解锁），差"验收标准/所有权/结算"｜CO5 ← AO `adapters/workspace/router` + `SessionMetadata`，差"由 Work 派生而非人建"｜CO6 ← AO `adapters/agent`，差"自动路由 + 显式覆盖"｜CO10 ← AO durable facts vs derived status（**语义同构、内容不同**）｜CO9 ← Copilot（PR + 人审批），差"Gate 是产品内对象，不依附 GitHub"。

### 6.2 Provider-owned（12 项，不得重造）

**PO1** 代码生成与编辑｜**PO2** 仓库内自主探索与定位｜**PO3** 命令执行与工具调用｜**PO4** diff / patch 的产生｜**PO5** 代码审查（同 Provider 内建，`codex review`）｜**PO6** 上下文压缩｜**PO7** 会话恢复｜**PO8** 沙箱与权限档位｜**PO9** Provider 内部的多 agent 协作｜**PO10** 测试/构建/静态检查的**执行**｜**PO11** 浏览器与桌面自动化｜**PO12** Provider 自身的 UI/终端。
> **规则**：Curis 若实现其中任何一项，就等于**在 Provider 之上做了一层更差的重复实现**，并**破坏可替换性**。

### 6.3 Orchestrator-owned（6 项，可复用/可借设计）

| # | 能力 | 参考实现 | 借什么 | 风险 |
|---|---|---|---|---|
| **OO1** | 多会话并行监管 + 状态派生 | AO（daemon + SQLite + CDC + SSE） | **架构模式**（durable facts vs derived status），**不直接依赖其运行时** | AO 外围越界 |
| **OO2** | Workspace 生命周期（worktree） | worktrunk / claude-squad / parallel-code | **约定与坑清单** | worktrunk license `NOASSERTION` 需法务；直接依赖会引入 Rust/Go 工具链 |
| **OO3** | 容器化隔离（可选档位） | container-use（MCP server，零 agent 绑定，Apache-2.0） | 若 v1 做容器档，**这是唯一"可当 MCP 工具复用"的实现** | 自标 experimental；release 停滞 |
| **OO4** | 四槽适配层设计 | AO `backend/internal/adapters/*` | **目录结构与接口切分**（"可替换"最直接的落地形态） | 适配层自身需有测试 |
| **OO5** | 事件流 + replay | OpenHands EventLog | 若要"执行可复现"，这是最完整的模型 | OpenHands 体量大 |
| **OO6** | 沙箱化执行接口 | SWE-ReX（593★，MIT） | 若要"任意命令都进沙箱"，这是**独立可复用**的层 | 研究项目，非产品 |

### 6.4 Git-owned（9 项）

GO1 版本控制（提交图，只读事实）｜GO2 分支（Curis 只定**命名约定 + 所有权规则**）｜GO3 worktree（Curis 定**分配/回收策略**）｜GO4 diff/patch（**消费为 WorkResult 的一部分**）｜GO5 merge/rebase（**触发时机由 Gate 决定**）｜GO6 **冲突检测（唯一权威；Curis 只做"文件集重叠预警"，不做冲突判定）**｜GO7 历史/reflog（审计与回滚入口）｜GO8 hooks（挂"提交前必须过测试"类规则）｜GO9 远端同步/备份/CI（可选，非 v1 必需）。

### 6.5 Human Gate（7 项）

**HG1** 范围/架构变更（属产品决策；对应固定顺序 Blueprint → Design → Code）｜**HG2** 凭据/登录（对应既有 `WAITING_FOR_USER`；禁重试登录/绕 CAPTCHA/切账号）｜**HG3** 高风险合并（不可逆/影响数据/影响发布）｜**HG4** 权限边界扩张（对应既有 L2 Gate ⑤⑥）｜**HG5** 商业/收费/新市场/Marketplace（对应既有 L2 Gate ①–④⑦）｜**HG6** `effect_unknown`（自动重放会产生重复副作用，对应既有 G4）｜**HG7** Agent 自报完成的最终确认（首次/高风险 Work，因 F10）。

### 6.6 绝不重新开发的清单（11 项）

1. **不做 Multi-Agent Coding Framework**（编排、并行、隔离、审查已由 Provider + 开源 Orchestrator 完成）
2. **不做版本控制语义**（→ git）
3. **不做工作区隔离原语**（→ `git worktree`；可选容器 → container-use 式方案）
4. **不做 diff / patch 格式**（→ git / Provider）
5. **不做 agent 内部上下文压缩**（→ Provider `compact` / Condenser）
6. **不做 Provider 内部的 subagent / agent teams 机制**（Codex `multi_agent` 已 stable）
7. **不做浏览器/桌面自动化引擎**（→ Provider `browser_use` / `computer_use`；或既有 CGAP-01 Playwright 结论）
8. **不做代码审查模型**（→ `codex review` 类能力 + 换 Provider 评审）
9. **不做测试框架**（→ 项目自身工具链）
10. **不做项目地图机械校验器以外的知识库系统**（可借 Codex 官方实践：linters + CI + doc-gardening agent）
11. **不把 GitHub PR 做成 v1 必需通道**（单机本地自用；PR 是可选远端能力）

### 6.7 与既有红线的对齐检查

v1 单机本地桌面自用 ✅ 未触碰｜暂不建设（独立 Admin / 物理多租户 / 计费订阅 / 多真实员工协作 / 深度 CRM-ERP / Marketplace 开放生态）✅ 未触碰（CO1 的 Employee 是**单机单用户**的组织语义）｜v1 允许"连接自己的外部模型/Agent/Skill/Tool"✅ **本拆分正是这条允许项的落地**（Provider 抽象 + BYOK）｜能力可替换不写死 ✅｜不得另造状态名 ✅（复用 `WAITING_FOR_USER` / `EFFECT_UNKNOWN`；新增术语均标注为**提案**）｜仅结构候选不得当 Authority ✅。

---

## 7. Provider Orchestration 模型

### 7.1 核心结论

1. **Provider 可替换性已被真实工程解决，有可直接读的参考实现**：AO `backend/internal/adapters/agent/` 下**平铺 30 个 Provider 适配器**，`adapters/reviewer/` **用同一套清单**做"换一个 Provider 来评审"。这是已合并进主干的代码结构。
2. **关键不是"支持很多 Provider"，而是"把 Provider 差异收敛到一个极薄的适配边界"**：每个 Provider 一个目录（`agentbase` 提供公共骨架），差异只体现在**启动方式、活动信号来源、hooks 注入方式**三处。
3. **Provider 应被抽象成 4 个可独立替换的槽位**：

| 槽位 | 职责 | AO 对应目录 |
|---|---|---|
| **Agent Slot** | 谁来写代码 | `adapters/agent/*` |
| **Reviewer Slot** | 谁来评审 | `adapters/reviewer/*` |
| **Workspace Slot** | 在哪写 | `adapters/workspace/{gitworktree,router,scratch}` |
| **Runtime Slot** | 用什么承载进程/终端 | `adapters/runtime/{tmux,conpty,ptyexec,runtimeselect}` |

> **这四槽分离是 Curis "能力可替换不写死"的直接落地形态**——而不是笼统的"支持多家模型"。

### 7.2 本机 Provider 真实现状（L1 实测，2026-09-19）

| Provider | 本机状态 | 关键可用能力 | Curis 可用性 |
|---|---|---|---|
| **Codex CLI** | ✅ `codex-cli 0.144.6`（`/Users/yy/.local/bin/codex`） | `exec` / `review` / `apply` / `resume` / `fork` / `archive` / `sandbox` / `mcp-server` / `cloud`(实验) / `-C` / `-s` / `-a` / `--add-dir`；feature flags：**`multi_agent` stable**、`computer_use` stable、`browser_use` stable、`hooks` stable、`memories` experimental | ✅ **首选 Worker**；`-C <workspace>` 即可接入任何 Workspace |
| **Claude Code** | ❌ 本机**未安装** | 官方文档：`--worktree`、subagents、agent teams、agent view、cross-session messaging、`/batch` | ⚠️ 需安装后才可实测；其 worktree 与 agent teams **是该 Provider 私有语义** |
| **OpenHands** | ❌ 未安装 | SDK/API、三档 Workspace、**ACP 可接外部 agent** | ⚠️ 体量大（88k★ 平台），v1 不建议引入 |
| **Aider / OpenCode / Goose** | ❌ 未安装 | 均为成熟 CLI Provider | ⚠️ 备选池（AO 已写适配器） |
| **OpenAI 兼容 / 本地模型** | 部分（`--oss --local-provider {lmstudio,ollama}`） | 本地推理 | ⚠️ 可选 |

**结论**：Curis v1 的**唯一已验证可用 Provider 是 Codex CLI**；Claude Code 是**必须支持但当前无法实测**的第二个 Provider。这决定了 v1 的 Provider 抽象**必须按"至少两个 Provider"设计**，否则会不知不觉写死成 Codex-only。

### 7.3 ProviderDescriptor（能力声明，不是假设）

| 字段 | 为什么必需（证据） |
|---|---|
| `provider_id` / `display_name` | 标识 |
| `kind`（`cli` / `sdk` / `cloud`） | Codex 同时有三种形态 |
| `launch_mode`（`interactive_tui` / `headless_exec` / `both`） | Codex 有 `exec`；Claude Code 有 `-p`；**agent teams 要求交互式会话**（非交互 `-p` 不 spawn teammates） |
| `workspace_binding`（`cwd` / `flag(-C)` / `provider_native_worktree` / `container`） | Codex 用 `-C`；Claude Code 用 `--worktree`（**且只它自己认**） |
| `resume_support`（`none` / `session_id` / `checkpoint`） | Codex `resume/fork`；Claude Code `/resume` **不恢复 in-process teammate** |
| `context_source` | Codex 读 `AGENTS.md`（含 `AGENTS.override.md`）；Claude Code 读 `CLAUDE.md` |
| `permission_model` | Codex `-s` + `-a`；Claude Code permission modes + `dontAsk` 不被 teammate 继承 |
| `verification_hook` | Codex / Claude Code 均有 hooks |
| `activity_signal` | AO 为此单列 `activitydispatch` / `activitystate` / `hooksjson` / `hookutil` |
| `multi_agent_support` | Codex **stable**；Claude Code agent teams **experimental，默认关闭** |
| `result_contract` | Codex `apply`（patch）；Claude Code **无自动 PR** |

### 7.4 四条硬规则（防止 Provider 泄漏进产品语义）

| # | 规则 | 反面案例（真实存在） |
|---|---|---|
| **R1** | **Curis 任何产品概念不得以 Provider 命名**（不得出现"Codex 会话"作为 UI 一级对象） | Claude Code 的 "Agent Teams" 是**它自己的**协作层，workers **必须是 Claude 会话** |
| **R2** | **不得依赖 Provider 私有 Workspace 机制作为唯一隔离实现** | Codex 的 Worktree 是 **App 线程级，CLI 无 `--worktree`**（L1）；Claude Code worktree 落 `.claude/worktrees/` 且只有它认 |
| **R3** | **不得让 Provider 的协作层成为 Curis 的组织层** | agent teams 的 lead/teammate/task-list 是**运行期协作**，不是 Curis 的 Employee/Work |
| **R4** | **Provider 差异必须收敛在适配层；上层只见 WorkResult** | 否则每加一个 Provider 都要改产品 |

### 7.5 路由策略

| 依据 | 优先级 |
|---|---|
| **用户显式指定**（Employee/Work 上可绑 Provider） | 最高（覆盖一切） |
| **能力要求**（需要 `computer_use` / 长时无人值守 / 强沙箱） | 高 |
| **可用性**（未安装 / 未登录 / 额度耗尽 → 自动降级） | 高 |
| **工作类型**（写密集 vs 读密集——OpenHands 官方建议：**读密集才适合 fan-out**） | 中 |
| **成本**（token/订阅额度；**成本非判据**的领域应谨慎套用既有裁定） | 低 |

> 成本参考（公开测算，非本机实测）：多 agent 消耗可达普通对话 **15 倍**；有报告称 3 个并行 agent 约 **$30–40/日**。

### 7.6 中途替换的四层级 + 落地细节

L-a 换 Reviewer ✅ 完全可行｜L-b 换 Executor（同 Work 从零重跑）✅ 可行｜L-c 换 Executor（同 Workspace 接力）⚠️ 部分可行（**需前一个 Provider 先 commit**）｜**L-d 无损迁移运行中会话 ❌ 不存在**。

> **把"可替换"的保证放在 L-a / L-b / L-c，不承诺 L-d。**

**替换时必须处理的五个真实教训**：①未提交变更无法跨界 → 强制 commit 或 stash｜②Provider 权限档不同 → **权限档必须重新声明**（防"降级后权限升级"）｜③项目上下文文件名不同（`AGENTS.md` vs `CLAUDE.md`）→ Curis 需**单一项目地图源 + 每 Provider 投射**｜④替换会读不到活动信号 → **必须进入"待确认"而不是乐观 idle**｜⑤旧 Provider 进程可能仍活着 → **替换必须先终止旧执行体并验证终止**。

### 7.7 安全与权限

Codex 三档沙箱 + 三档审批应对用户**显式暴露**，不默认全权｜本机 config 实测 `sandbox="danger-full-access"` 是**用户当前配置，不得静默继承为产品默认**｜**worktree/容器隔离不能保护密钥** → 凭据治理必须独立于 Workspace 隔离（沿用既有硬约束：密钥只驻 `.env`，DB 只存 `credential_ref`）｜Copilot 的"只能推 `copilot/*` + agent PR 的 Actions 需人批准"→ 本地等价物 = **分支所有权 + Gate**｜Claude Code"teammate 不能替人批准、被拒后不能转手绕过"→ **权限冒泡必须真的到人**，不能由 agent 互相批准。

---

## 8. 对 RD 产品表达的影响

### 8.1 评估方法（L2 证据）

本轮**未改** RD 原型，但**读取**了其源码（`RD_WORKSPACE_HTML_EXPLORATION/`，单文件 3000 行）。关键词出现次数：

| 关键词 | 次数 | 说明 |
|---|---|---|
| `provider` | 52 | 已是一等概念 |
| `Codex` | 14 | 已作为具体 Provider 出现在 mock 数据 |
| `Claude` | 13 | 同上 |
| `Git` | 12 | **只出现在"来源 GitHub API_SYNC"与"不画 Git"的原则文案中** |
| `Workspace` | 4 | **只出现在标题/文件名**（"RD Professional Workspace"），**不是工程工作区概念** |
| **`worktree`** | **0** | **完全没有** |
| **`branch`** | **0** | **完全没有** |

### 8.2 已对齐的部分（好消息）

| 原型既有表达 | 是否一致 |
|---|---|
| `Provider 是能力提供方，Employee 是责任归属者`（原型内明文原则） | ✅ **高度一致**（= CO1 核心） |
| `work.provider` 字段 + `▶ 执行` 动作（`data-action="exec-provider"`） | ✅ 方向正确：Work 上绑 Provider，不是人绑 Provider |
| `回流 Development 重新派发修复，同/异 Provider 均可` | ✅ 与"Provider 可替换（L-b）"一致 |
| `Decision / needs_ceo` 状态存在 | ✅ 与 CO9 Decision Gate 一致 |
| `不画 IDE / Terminal / Git / CI / 部署工具` | ✅ 方向对，**但需细化**（见 IMPACT-5） |

### 8.3 需要修改的 6 项（按严重度）

**IMPACT-1（🔴 最高）Provider 被画成了"对话参与者"，与自身原则矛盾**
现状：`{ who: 'provider', name: 'Claude Code', … }` / `{ who: 'provider', name: 'Codex', … }`——**Codex / Claude Code 直接以发言者身份出现在 Conversation 主面**。
冲突：CO1/CO2——Conversation 是 **CEO ↔ Employee 的持续关系**；Provider 是 **Employee 调用的能力**，不是关系的一端。且 Provider 之间**没有跨系统对话协议**，把 Provider 放进对话＝把"执行过程"冒充"组织沟通"。**UI 与原型自己的原则文案自相矛盾。**
建议：①Conversation 主面的发言者**只应是人（CEO）与 Employee**；②Provider 输出应作为 **WorkResult（附着在 Work 上的结果对象）**呈现，可由 Employee 引用（原型 `ref-diff-230` 已是正确方向）；③若要看"Provider 说了什么"，那是 **C3 日志视图（诊断用）**，不是对话流参与者。

**IMPACT-2（🔴 高）"并行 Work 互不干扰"缺机制表达，当前表述无法验证**
现状：断言"已拆成两个并行 Work … 互不干扰"，但全文 **`worktree` / `branch` 出现 0 次**——**没有任何东西告诉用户"靠什么做到互不干扰"**。
建议：Work 上应有一个**可查看的"执行位置"表达**（不是 IDE、不是文件树）：如"隔离工作区 · 分支 `work/W-231-…` · 基线 `a1b2c3d`（只读摘要）"。**不需要**展示目录树或 git 命令，但"**这一份 Work 的改动与那一份是分开的**"必须是可见事实。

**IMPACT-3（🔴 高）状态挂在 Provider 上**
现状：`provider: 'Claude Code', status: 'working'` / `provider: 'Claude Code', status: 'needs_ceo'`。
冲突：状态应由事实派生，且 **Work 状态 ≠ Provider 会话状态**；挂 Provider 会导致换 Provider 时语义断裂、同一 Provider 多 Work 无法区分；**`needs_ceo` 是组织语义，Provider 不可能"需要 CEO"**。
建议：`status` 归 **Work**；`needs_ceo` 归 **Work/Decision**；Provider 侧只保留技术事实（`activity: active / idle / blocked / exited / no_signal`），**且必须能表达 `no_signal`**。

**IMPACT-4（🟡 中）缺少 WorkResult / Verification 两个对象**
现状：只有 `ref-diff-230` 类引用与 Provider 的文字汇报，未把"结果"与"验证"建模为独立对象。
建议：在 Work 上增加两个**可展开区块**（不是新页面）：**结果（diff + 变更文件 + 未解决项）** 与 **验证（谁验的 / 验了什么 / 结论）**。

**IMPACT-5（🟡 中）"不画 Git"这条原则过粗**
✅ 正确的部分：不该做 git 工具界面（提交图、diff 编辑器、冲突解决器）。
⚠️ 会丢的部分：**分支名 / 基线 / 隔离位置**是"风险可见性"的必需信息（不变量 I5）。
建议改写为："**不做 git 工具；但必须让『这次改动从哪来、在哪做、与谁隔离』可见。**"

**IMPACT-6（🟢 低-中）缺少"Work → 下一个 Work"的接力表达**
现状：有"回流 Development 重新派发修复"，但形式是"重新派发"，**不是"接力"**。
建议：Work 的结束态应区分"**已完成待收口**"与"**已收口**"，前者可被下游 Work 引用（但**不算真相**）。

### 8.4 需要建立的 Runtime 需求（仅登记，不在本轮实现）

| # | 需求 | 优先级 |
|---|---|---|
| R1 | **Workspace 分配与回收**（Option D：worktree 默认） | P0 |
| R2 | **WorkspaceRegistry**（path/branch/base_ref/lock/reclaim_policy） | P0 |
| R3 | **Provider 四槽适配层**（agent / reviewer / workspace / runtime） | P0 |
| R4 | **WorkResult 归一化 schema** | P0 |
| R5 | **状态派生层**（持久事实 → 派生状态；含 `no_signal`） | P0 |
| R6 | **执行权限档位**（沙箱/审批档，显式选择，不默认全权） | P1 |
| R7 | **Verification 触发与记录**（默认换 Provider 验；高风险强制人验） | P1 |
| R8 | **Review 路由**（默认"换一个 Provider 审"） | P1 |
| R9 | **WorkResult 交接（H-A / H-B）** | P1 |
| R10 | **文件集重叠预警**（分配 Workspace 时提示冲突风险，**不做锁**） | P2 |
| R11 | **依赖 + 超时兜底**（防"状态滞后卡死依赖"） | P2 |
| R12 | **容器档位**（`strategy` 字段预留，v1 不实现） | P3 |

### 8.5 明确"不应进入产品"的东西

git 命令 / 分支图 / 冲突解决器｜Provider 私有概念的直译（"Agent Teams"、"subagent"、"mailbox"、"worktree lock"）｜目录树 / 文件浏览器｜"agent 说它完成了"作为完成依据（F10）｜"正在运行中"这种乐观状态（`no_signal` 教训）｜会话入口列表 / 终端面板（那是 Provider/IDE 形态，不是 Curis 的组织形态）。

---

## 9. 需要 CEO 裁定的 Gate 表述

> **是否接受：①Provider 退出 Conversation 主面（改为 WorkResult 对象）；②Work 上增加"隔离位置（分支/基线）"只读表达；③状态归 Work 且必须能表达 `no_signal`；④Workspace 采 Option D（worktree 默认，容器预留）；⑤Provider 四槽适配层与 WorkResult 归一化列入 Runtime P0。**

**是否已足够进入 RD 定向视觉修订？→ 研究层面已足够；建议先取一次裁定，再改视觉。** 三条理由：
1. 底层工作模型已成形（Workspace 模型 / Context 四分层 / 能力拆分 / 交接与恢复），**不会再因"机制不清"反复推翻视觉**。
2. **6 项产品表达需先裁定**，其中 IMPACT-1/2/3 会直接改变 Conversation 主面与 Work 卡片表达——**先改视觉再裁定＝返工**。
3. 本轮被明确要求"不做 UI"。

---

## 10. 已知限制（不得省略）

1. **未做端到端多 Agent 真机实验**——全部"吞吐/冲突率"类结论均来自公开资料并已标注等级，**未在本机验证**。未运行任何 agent、未安装依赖、未执行 demo、未创建临时测试 repo（本轮用户划定的是"研究 → 翻译成 Curis 需求"，L1 端到端跑多 Agent 属边界允许但非必需）。
2. **Claude Code 本机未安装**（`claude: NOT INSTALLED`）→ 其全部结论为 **L3 官方文档**，无 L1 实测。
3. **Orca / vibe-kanban 仅做到 README + 元数据级**（L3/L4），未源码深挖；`stablyai/orca` 存在 **6 个月 7.2 万星 + 6,323 未处理 issue** 的异常组合，**其 star 数不作为质量证据**。
4. **未验证任何项目的 License 兼容性结论**（只列出 license 事实）。`max-sixty/worktrunk` 的 GitHub license 字段为 `NOASSERTION`（仓库内声明 `MIT OR Apache-2.0`）——**若未来采用需法务确认**。`smtg-ai/claude-squad` = AGPL-3.0，**采用红线**。
5. **付费/凭据类未执行**：Devin、Google Jules、Codex Cloud、Copilot cloud agent 均为闭源或需订阅，仅以官方文档（L3/L4）评估。

**研究过程中的纠正（可复用的证伪记录）**：
| # | 现象 | 处理 |
|---|---|---|
| C1 | 第三方博客声称 `codex --worktree` 是 CLI flag | **证伪**：本机 `codex --help` 全量 options **没有** `--worktree`；worktree 是 **Codex App 的线程级选择**。**L1 覆盖 L5** |
| C2 | 搜索引擎把 `ComposioHQ/agent-orchestrator` 当主体 | **纠正**：真实仓库为 `Untrivial-ai/agent-orchestrator`（12.1k★）；**用 `gh api` 逐个核验取代搜索摘要** |
| C3 | 第三方 wiki 披露 Agent Teams 内部细节（TeammateTool 操作数、flag 名） | **降级为 L5/推断**：只用 Anthropic 官方文档能证实的部分 |
| C4 | `FoundationAgents/MetaGPT` 最近提交停在 2026-01-21 | **如实标注**：高星但近期活跃度低，不作"可直接复用 Orchestrator"候选 |
| C5 | 一批 `gh api` 命令被 SIGTERM（exit 137） | 拆分重跑；未丢证据 |
| C6 | 用户原文列出 AutoGen / Microsoft Agent Framework 等方向 | **降权**：`microsoft/autogen` 近期提交 2026-04-15 且 license 为 `CC-BY-4.0`（文档类），更适合作"多智能体会话框架"而非"仓库协作编排器" |

---

## 11. 证据与明细索引

### 11.1 证据文件（`evidence/`，7 份真实证据）

| 文件 | 内容 |
|---|---|
| `E01_GITHUB_REPO_METADATA.tsv` | 34 个候选的 stars / forks / pushed_at / license / archived / open_issues（`gh api`，2026-09-19） |
| `E02_CODEX_CLI_LOCAL_PROBE.txt` | 本机 Codex CLI 0.144.6 全量 `--help` / `features list` / config（**L1**） |
| `E03_AO_ARCHITECTURE_HEAD.md` | Agent Orchestrator `docs/architecture.md`（durable facts vs derived status） |
| `E04_AO_ADAPTER_LAYER.txt` | AO 适配层目录清单（**Provider 可替换性的源码级证据**） |
| `E05_AO_SESSION_AND_STATUS_MODEL.go.txt` | AO `domain/status.go` 状态枚举 + `domain/session.go` 会话模型 |
| `E06_CLAUDE_SQUAD_WORKTREE_MODEL.go.txt` | claude-squad worktree 源码（`isExistingBranch`） |
| `E07_CLONE_MANIFEST.txt` | 5 个 shallow clone 的体积 / HEAD / 最近提交 |

### 11.2 明细文档（`details/`，11 份，仅供追溯）

| 文件 | 内容 |
|---|---|
| `CURIS_RD_MULTI_AGENT_DEVELOPMENT_STUDY.md` | 原入口文档（24 问终答的完整版） |
| `CURIS_RD_MULTI_AGENT_OPEN_SOURCE_DEEP_DIVES.md` | 10 个项目逐项深挖（12 维）+ 落选对照组 |
| `CURIS_RD_MULTI_AGENT_COMPARISON_MATRIX.md` | 元数据存活度 / 三轴对照 / 12 维覆盖 / 隔离代价 / 九项评分 |
| `CURIS_RD_PROJECT_WORKING_SPACE_MODEL.md` | Option A/B/C/D 全文 + WorkspaceRecord + 生命周期 + 5 项遗留未知 |
| `CURIS_RD_AGENT_WORKSPACE_AND_GIT_MODEL.md` | Branch/Worktree/Clone/Sandbox 详细拆解；冲突三层防线；文件归属；Git/GitHub 分工 |
| `CURIS_RD_CONTEXT_AND_HANDOFF_MODEL.md` | Context 四分层逐层规格 + Handoff 三类 + 责任映射 + Leader 模型 |
| `CURIS_RD_PROVIDER_ORCHESTRATION_MODEL.md` | 本机 Provider 实测 + ProviderDescriptor + 四槽适配 + 路由 + 中途替换四层级 |
| `CURIS_RD_FAILURE_RECOVERY_AND_LONG_RUNNING_MODEL.md` | 失败 10 分类 + 状态事实/派生 + 三层检查点 + 长期保存边界 |
| `CURIS_RD_CURIS_OWNED_VS_PROVIDER_OWNED.md` | 五类能力拆分全文 + 绝不重造清单 + 红线对齐 |
| `CURIS_RD_PRODUCT_TRANSLATION_IMPACT.md` | RD 产品表达 6 项影响的完整论证 + Runtime 需求 R1–R12 |
| `RESEARCH_JOURNAL.md` | 方法、时间线、检索式、纠正与止损、已知限制 |

### 11.3 上游边界文档（2026-09-20 追加，非本文结论的一部分）

| 文件 | 内容 |
|---|---|
| `../business-working-space-baseline-2026-09-20/CURIS_BUSINESS_WORKING_SPACE_BASELINE_CANDIDATE.md` | **Global Business Working Space Baseline（候选）**：Business 长期资产空间定义、Shared Base + Professional Package、资产归属边界、DB/Filesystem 分工、Provision、改名/移动/归档/删除、Adopt、Context 三层映射、8 项 Gate。本文的 Project Working Space 是它的 **Development 特化**（见 §0.A） |

### 11.4 实验目录（git 未跟踪）

`RD_MULTI_AGENT_RESEARCH_LAB/{repos,experiments}`——含 5 个 shallow clone：`agent-orchestrator` / `claude-squad` / `container-use` / `worktrunk` / `parallel-code`。

### 11.5 状态

```
RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW
```

**停止条件已达成**：开源项目筛选 ✅ · Deep Dive ✅ · 源码/必要验证 ✅ · Multi-Agent Runtime 模型 ✅ · Project Working Space 模型 ✅ · Curis Translation Impact ✅

**STOP。** 等待 CEO 裁定 §9 的 5 项 Gate 表述后，再开 RD 定向视觉修订。
