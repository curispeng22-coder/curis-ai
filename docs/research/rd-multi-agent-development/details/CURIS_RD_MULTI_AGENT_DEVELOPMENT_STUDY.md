# CURIS RD — MULTI-AGENT SOFTWARE DEVELOPMENT ORCHESTRATION STUDY

**Authority Class**: RESEARCH（**非 Authority；不得作为 Current Product/Implementation Truth**）
**Status**: Review — `RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW`
**日期**: 2026-09-19
**范围**: 只研究"多个 Coding Agent 长期协同开发同一个项目"这件事在成熟系统里如何组织，并翻译成 Curis 产品与 Runtime 需求。
**未做**: 未修改 Curis Authority / Runtime / Code / RD HTML / Figma / Frontend / Backend；未 commit；未 push。

---

## 0. 一页结论（先给结论）

1. **Curis RD 本质上是 "Multi-Agent Software Development Orchestration"，但它真正缺的不是编排器，而是"组织与问责层"。**
   编排、隔离、并行、审查、沙箱这些事，**要么 Provider 已经做好（Codex/Claude Code/Copilot/OpenHands），要么开源项目已经做好（Agent Orchestrator / container-use / worktrunk）**。Curis 不该重做。
   开源项目里**一个都没有**的是：**长期组织身份（Employee）、责任归属、跨 Provider 的结果归一、独立验证、产品化 Decision Gate、跨会话的长期运营状态**。**这才是 Curis 的 Owned 范围。**

2. **长期 Project Working Space 的唯一正确答案是：Canonical Project Root（唯一）+ 每个 Work 一个隔离 Workspace（消耗品）。**
   Project Root 是**资产**，Workspace 是**消耗品**。二者不能混为一谈。

3. **多 Agent 绝不应共享同一个 Working Tree。** 本领域 **10/10** 成熟实现无一例外。

4. **隔离原语选 git worktree（默认）；容器作为"按 Work 显式升级"的可选档位。** 不选 Provider-native 工作区（会把 Curis 锁死在某一家）。

5. **Codex 与 Claude Code 已经把"单机多 agent 并行"做成了产品原语**，但它们各自的协作层都是**自家封闭的**；Curis 只能在它们之上做**归一化**，不能把组织层建立在任一家的协作语义上。

6. **没有任何系统解决了"跨 Provider 交接"。** 这是 Curis 少数的真实空位，也是 CO7（WorkResult 归一化）的正当性来源。

---

## 1. 交付物索引

| # | 文件 | 内容 |
|---|---|---|
| 01 | `CURIS_RD_MULTI_AGENT_DEVELOPMENT_STUDY.md` | 本文件（入口 + 24 问终答 + 术语表） |
| 02 | `CURIS_RD_MULTI_AGENT_OPEN_SOURCE_DEEP_DIVES.md` | 10 个项目逐项深挖（12 维）+ 落选对照组 |
| 03 | `CURIS_RD_MULTI_AGENT_COMPARISON_MATRIX.md` | 元数据存活度 / 三轴对照 / 12 维覆盖 / 隔离代价 / 可复用性九项评分 |
| 04 | `CURIS_RD_PROJECT_WORKING_SPACE_MODEL.md` | Option A/B/C/D + 推荐 D + WorkspaceRecord + 生命周期 |
| 05 | `CURIS_RD_AGENT_WORKSPACE_AND_GIT_MODEL.md` | Branch/Worktree/Clone/Sandbox 职责拆解；冲突三层防线；文件归属；Git/GitHub 分工 |
| 06 | `CURIS_RD_CONTEXT_AND_HANDOFF_MODEL.md` | Context 四分层（Project/Work/Execution/Conversation）+ Handoff 三类 + 责任映射 + Leader 模型 |
| 07 | `CURIS_RD_PROVIDER_ORCHESTRATION_MODEL.md` | 本机 Provider 实测 + ProviderDescriptor + 四槽适配 + 路由 + 中途替换四层级 |
| 08 | `CURIS_RD_FAILURE_RECOVERY_AND_LONG_RUNNING_MODEL.md` | 失败 10 分类 + 状态"事实 vs 派生" + 三层检查点 + 长期保存边界 |
| 09 | `CURIS_RD_CURIS_OWNED_VS_PROVIDER_OWNED.md` | 五类能力拆分（Curis 11 / Provider 12 / Orchestrator 6 / Git 9 / Human Gate 7）+ 绝不重造清单 |
| 10 | `CURIS_RD_PRODUCT_TRANSLATION_IMPACT.md` | RD 产品表达 6 项影响（含原型源码级证据）+ Runtime 需求 R1–R12 + 是否可进入视觉修订 |
| 11 | `RESEARCH_JOURNAL.md` | 方法、执行记录、检索式、纠正与止损、已知限制 |
| — | `evidence/E01–E07` | 元数据 / Codex CLI 实测 / AO 架构与适配层源码 / 会话状态模型 / claude-squad worktree 源码 / 克隆清单 |

**实验目录（git 未跟踪）**：`RD_MULTI_AGENT_RESEARCH_LAB/{repos,experiments}`——含 5 个 shallow clone（AO / claude-squad / container-use / worktrunk / parallel-code）。

---

## 2. 术语表（本研究的定版语义）

> 这些术语是**提案**（`Authority Class: RESEARCH`），供 CEO 裁定后再进入产品表达。

| 术语 | 定义 | 不是什么 |
|---|---|---|
| **Canonical Project Root** | 项目的唯一工程真相目录（含 `.git`、源码、文档、测试、配置、项目指令） | 不是"某个员工的工作目录" |
| **Repository** | Canonical Root 内的 git 仓库 | 不是"云端仓库"（v1 本地） |
| **Canonical Branch** | 被认定为"已收口"的分支（本地即 `main`） | 不是"默认分支"的别名——强调"只有过 Gate 的才能进" |
| **Workspace** | 一次 Work 的隔离工作目录（从 Canonical Root 派生） | 不是 Workspace（Curis 组织层的工作空间）；**不是** IDE/Terminal |
| **Working Tree** | git 意义上的某个分支的检出 | **禁止多个执行体共享同一个** |
| **Work** | 一个有目标、可验收的执行单元 | 不是"任务列表里的一条待办"（它带验收标准、所有权、结算） |
| **Assignment** | 一次执行指派（Work → Provider 会话） | 不是"Employee 的岗位" |
| **Provider** | 可替换的 coding agent 执行能力（Codex / Claude Code / OpenHands / Aider…） | **不是** Employee（Provider 无长期身份、无问责） |
| **WorkResult** | Provider 产出的归一化结果 `{diff, files, test_evidence, unresolved, logs_pointer}` | 不是聊天记录、不是日志 |
| **Verification** | 独立于执行的验收（默认换一个 Provider 验） | 不是"agent 说自己完成了" |
| **Gate / Decision** | 进入 Canonical 或改变范围的**显式**批准点 | 不是"人点了 PR merge"这种隐式动作 |
| **Project Context (C1)** | 项目长期是什么（目标/架构/仓库/指令/决策/知识/历史/团队） | 不是"上下文窗口里的内容" |
| **Work Context (C2)** | 这一件工作要达成什么（需求/相关文件/依赖/期望结果/验收） | 不是 prompt |
| **Execution Context (C3)** | 这一次运行发生了什么（prompt/Provider/沙箱/进程/日志/工具状态） | **不是**下一个 agent 的输入（是证据） |
| **Conversation Context (C4)** | CEO ↔ Employee 的持续工作关系 | 不是运行日志、不是代码真相 |
| **Durable Fact** | 必须持久化的事实（活动态、终止态、绑定、检查点、Workspace 记录、Gate 记录） | 不是可派生的展示状态 |
| **Derived Status** | 读取时计算、**绝不存储**的展示状态 | 不是真源 |
| **no_signal** | 活着但拿不到任何活动回调 → **拒绝乐观** | 不是 idle |

---

## 3. 方法摘要

- **广度**：8 组 GitHub 检索式（`gh search repos --sort stars`）→ 候选池 60+。
- **元数据核验**：`gh api repos/...` 逐个取 stars/forks/pushed_at/license/archived/open_issues（**取代搜索摘要**，纠正了 2 处错误）。
- **源码深挖**：shallow clone 5 个编排器/隔离工具；读 architecture/源码/adapters（L2）。
- **官方文档**：Claude Code（agents / worktrees / agent-teams）、GitHub Copilot cloud agent、OpenAI "Harness engineering"（L3/L4）。
- **本机实测**：Codex CLI 0.144.6 全量 `--help` / `features list` / config（L1）。
- **明确未做**：未跑端到端多 Agent 真机实验（见 11 号文档 §4，已如实标注全部相关限制）。

---

## 4. 二十四个终答

### Q1. Curis RD 本质上是否应该被理解为 Multi-Agent Development Orchestration？

**是，但更准确的说法是 "Multi-Agent Development **Operating**"，而不是 "Orchestration"。**
- 是 Orchestration：因为它确实要面对"多个执行体围绕同一个长期项目并行工作"的全部工程问题（隔离、歧义、冲突、交接、恢复）。
- 但不止 Orchestration：编排问题**已被解决**（Provider + 开源 Orchestrator）。Curis 的增量在**组织层**——Responsibility、Accountability、Decision、长期运营状态。
- **判据**：如果 Curis 只做编排，它永远追不上 AO/Orca；如果 Curis 只做组织而不解决"执行体如何安全并行"，它的自动化就是空话。**两者都要，但自有部分在后者。**

### Q2. 长期 Project Working Space 应该是什么？

**Canonical Project Root（唯一，长期）+ 每个 Work 一个隔离 Workspace（消耗品）。**
详见 04 号文档。**Project Root 是资产，Workspace 是消耗品**——这是本模型最重要的区分。

### Q3. Agent 生成的代码/文档最终归属哪里？

**先在 Workspace 产生 → 经 Gate 进入 Canonical Branch。**
- 唯一例外：被显式授权的**窄通道**（如项目文档勘误）可直接入 Canonical，但仍需 Gate。
- 证据：**没有任何成熟系统允许执行体直接写 canonical 工作树**；Claude Code 用不可关闭的强制校验阻止；Copilot 在平台层禁止推 `main`。
- 详见 05 号文档 §4。

### Q4. 多 Agent 是否应该直接共享同一个 Working Tree？

**绝对不应该。** 10/10 成熟实现无一例外。共享的是 **repo 与 `.git` object store**，不是工作目录。
不变量 I2。

### Q5. Branch / Worktree / Clone / Sandbox 哪个更适合？

**它们不是四选一，而是三层不同职责：**
- **Branch** = 变化线（git 天然负责）；
- **Worktree / Clone / Container** = 执行位（在哪个目录里改）；
- **Sandbox = 权限边界**（进程能碰什么）。

**裁定的组合**：`Branch（命名 work/<work_id>-slug + 记录 base SHA）` + `Worktree（默认执行位）` + `Sandbox（优先复用 Provider 权限档，必要时容器）`。
**Clone 不作为默认**（磁盘翻倍 + 基线漂移 + 合并代价）。
证据：Claude Code / AO / Orca / claude-squad / worktrunk / parallel-code / vibe-kanban 全部用 worktree；container-use / Copilot / OpenHands / SWE-ReX 用容器。
⚠️ **重要更正**：Codex 官方明确"**worktree 隔离不保护密钥**"——关键在权限，不在隔离强度。

### Q6. Codex 当前已经解决哪些问题？

**已解决（L1 本机实测 + L4 官方）**：单机可编程 agent 运行时（`exec`）｜非交互代码审查（`review`）｜diff 落地（`apply` / `cloud apply`）｜会话生命周期（`resume` / `fork` / `archive` / `unarchive`）｜沙箱三档 + 审批三档｜`-C` 指定工作根 + `--add-dir`｜可被别的框架当 MCP server 调用｜**多 agent 已是 stable 特性（`multi_agent`）**｜`computer_use`/`browser_use` 均 stable｜hooks stable｜自动 compaction｜桌面 App 的 Local/Worktree 线程模型｜云任务（可指定分支/SHA，产出 diff）｜官方实测单任务可跑 6 小时+｜官方工程实践（AGENTS.md 当地图 + docs 系统记录 + exec-plans + doc-gardening agent）。

**未解决**：**程序化创建隔离工作区**（CLI **没有** `--worktree`——L1 证伪第三方博客）｜跨 Provider 交接｜项目级长期编排｜组织与问责。

### Q7. Claude Code 当前已经解决哪些问题？

**已解决（L3 官方文档；本机未安装 CLI）**：worktree 一等公民（`--worktree`，落 `.claude/worktrees/<name>/`，默认分支 `worktree-<name>`）｜**不可关闭的强制隔离校验**（阻止编辑主 checkout、阻止 cwd/git 重定向回主 checkout）｜subagents（可 `isolation: worktree`）｜agent teams（共享任务列表 + **文件锁认领** + mailbox + **blockedBy 依赖自动解锁** + 权限冒泡）｜agent view（派发即自动搬进 worktree）｜cross-session messaging｜`/batch`（5–30 个 worktree 隔离 subagent 各开 PR）｜CLAUDE.md 项目记忆｜hooks。

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
- `Untrivial-ai/agent-orchestrator` 是**唯一同时满足**"真操作 repo / 真多 agent / 真并行 / 长期项目状态 / Provider 无关 / local-first / Apache-2.0 / 活跃 / 可嵌入（本地 daemon + CLI + REST/SSE）"九项**的候选。
- 但：①它的外围（GitHub 绑定、Cloud、pricing、telemetry、mobile bridge）**超出 Curis v1 边界**；②它是"工程师管理台"，Curis 需要的是"组织与问责"；③依赖它意味着 Curis 运行时跟着它的发布节奏走。
- **建议**：**借架构，不借运行时**。真正采用与否属 **L2 Gate**，需 CEO 裁定。

### Q10. Curis 应该自己拥有哪些能力？

**11 项**（详见 09 号文档）：Employee 身份与职责｜Employee ↔ Conversation 持续关系｜Work 的定义与生命周期｜Assignment（Work → Provider）｜Workspace 分配与回收｜Provider 抽象与路由（四槽）｜**WorkResult 归一化**｜**Verification（独立于执行）**｜Decision Gate｜长期运营状态｜升级与例外处理。

### Q11. Employee 与 Agent Process 如何映射？

**不映射为 1:1。** 正确映射是三层：
```
Employee（长期身份 / 责任归属）
  ↳ Work（可验收的执行单元）
      ↳ Assignment（一次执行指派 = Workspace + 一个 Provider 会话）
          ↳ Provider（可替换的执行能力）
```
- Employee **不拥有**工程资产；Work **不拥有**代码真相（只引用 Canonical Project）。
- **明确否决**：1 Employee = 1 Agent Process / 1 Work = 1 Agent / Employee 拥有代码。

### Q12. 一个 Employee 多个 Work 如何执行？

**每个 Work 独立走完整的 Assignment → Workspace → Provider 链路，彼此隔离。**
证据：AO 的 orchestrator 会话可 spawn/redirect 多个 worker；Claude Code lead 可派多个 teammate + teammate **自领下一个未阻塞任务**。
**产品含义**：Employee Work Surface **不能是"一个员工一个终端"**，而应是"**一个员工手持 Work 清单，每份 Work 一个或多个执行槽位**"。

### Q13. 一个 Work 多个 Agent 如何执行？

**两种合法形态**：
- **并行竞争（择优）**：同一 Work 派生 N 个 Workspace，各跑不同 Provider，比较后择优。证据：**Orca README 原文** "Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner"。
- **串行接力（分工）**：Work → Assignment 1（实现）→ WorkResult → Assignment 2（补测试）→ …。证据：Codex `resume/fork`；AO `agent_switching` + `interface_transition`（**同一会话换 Provider 不中断，且"两个控制器绝不同时存活"**）。

### Q14. Context 如何分成 Project / Work / Execution / Conversation？

**四层定版**（详见 06 号文档）：

| 层 | 一句话 | 时间尺度 | 存储 |
|---|---|---|---|
| **C1 Project** | 项目长期是什么 | 月-年 | **仓库内文件**（地图 + docs + exec-plans）+ Curis 侧指针 |
| **C2 Work** | 这一件工作要达成什么 | 小时-天 | Curis 持久事实（自包含，**不含 prompt/日志**） |
| **C3 Execution** | 这一次运行发生了什么 | 分钟-小时 | append-only 事件流（**证据，不是输入**） |
| **C4 Conversation** | CEO ↔ Employee 的持续关系 | 月-年（跨 Work） | Curis 持久记录（**默认不注入 Provider**） |

**关系**：C1 ⊃ C2 ⊃ C3；C4 横向跨越全部。
**最重要的两条约束**：
- Claude Code 官方证实"**teammate 加载项目上下文但不继承 lead 对话历史**" → **上下文不会自动继承，这是正确的默认**。
- Codex 官方证实"**AGENTS.md 应当是地图不是百科全书**"；"从 agent 视角看，它运行期间无法在上下文中访问的东西就不存在"。

### Q15. Agent 之间如何 Handoff？

**三种交接必须先分类**：
| 类型 | 交接物 | 机制 |
|---|---|---|
| **H-A 同 Work 换执行体** | C3 检查点 + C2 不变 + 先 commit | Provider `resume`/`fork`；AO `interface_transition` |
| **H-B Work → Work** | **commit / diff** + 文件清单 + 测试结果 + 未解决项（**不是聊天记录**） | AO 的 orchestrator 综合后主动递上下文 |
| **H-C Work → Canonical** | diff + 验收证据 + Decision 记录 | Gate |

**不要混用三种"消息"语义**：diff/commit（权威）≠ Artifact 摘要（可过期）≠ Message/Mailbox（协调信号）≠ Shared Task State（**会滞后**）。
**必须接受的事实**：**跨 Provider 标准交接协议不存在** → 这正是 Curis 的 Owned 空位（CO7）。

### Q16. 并行修改冲突如何处理？

**三层防线，且必须诚实说明各层边界**：
| 层 | 能防 | **不能防** |
|---|---|---|
| L1 结构隔离（worktree/container per Work） | 同文件并发写覆盖 | **语义冲突**（各自测试都过） |
| L2 认领锁（任务级） | 同一任务被重复认领 | **文件写冲突**（Claude Code 官方原文："Locking applies to task claiming, not file writes."） |
| L3 收口检测（merge + 测试/CI） | 真实冲突在收口暴露 | **不会提前发现** |

**应做**：按**所有权**切分 Work（Codex 官方建议）+ 分配时做**文件集重叠预警** + 收口强制测试 + 把冲突当**正常状态**（AO 的 `changes_requested`/`ci_failed` 都是正常看板列）。
**不应做**：文件锁防写冲突（会把并行退化成串行）｜提前精确冲突预测（本领域无先例）。

### Q17. Review / Test / Merge 由谁负责？

| 环节 | 默认 | 高风险时 |
|---|---|---|
| **Review** | **换一个 Provider 的会话**来审（AO 的 `adapters/reviewer` 就是同一套适配器的另一份） | 强制人审 |
| **Test** | 项目自身工具链；**由执行体触发**，**由 Verification 收集结论** | 同上 |
| **Merge** | **必须过 Gate**（不是执行的自然结尾） | 人 Gate |

**重要**：Curis **不建模**"PR 作为唯一通道"——v1 是单机本地自用，**Decision Gate 才是通道**。

### Q18. Agent 失败以后如何恢复？

**失败分 10 类**（详见 08 号文档），恢复按**最便宜的先试**：
`P1 会话级 resume` → `P2 分支级（已 commit 的分支 + base SHA）` → `P3 工作区级（未提交变更，只作参考）` → `P4 用自包含的 C2 重跑`。

**四类失败禁止自动恢复**：
- `blocked`（待批准）：**AO 明文禁止向 blocked 会话注入输入**；
- `waiting_for_user`（需人）：沿用既有状态名，禁重试登录/绕 CAPTCHA/切账号；
- `effect_unknown`（写后未知）：禁盲目重放（既有 G4）；
- `no_signal`（无法判定）：**显示"无信号"而不是乐观 idle**。

**关键事实（F10）**：Claude Code 官方承认 **"teammates sometimes fail to mark tasks as completed"** → **agent 自报完成不可靠** → 因此 **Verification 必须独立于执行**，且依赖必须有**超时兜底**。

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

**依赖四件事，缺一不可**：①**会话可恢复**（P1/P2 检查点）②**状态可观测**（持久事实 + 派生状态 + `no_signal`）③**上下文可压缩**（Provider compaction）④**决策不丢**（Gate/Decision 持久）。

**长期保存 vs 临时的判据**：**"如果第二天需要它才能继续工作，它就是长期；如果丢了只会损失时间，它就是临时。"**
- 长期：Canonical Root、仓库内项目地图与 docs、**Decision 记录**、**Conversation**、已归档 Work 与 WorkResult。
- 临时：Execution Context、Workspace 目录、Provider 会话进程。

**v1 边界必须明确**：**单机场景下"关机 agent 还在跑"是不成立的**——Curis v1 **不应承诺**这个能力（Copilot 的云执行是唯一"关机也跑"的形态，属 L2 Gate）。

### Q21. Git / GitHub 应该承担什么？

**Git 承担 9 项（Curis 绝不重造）**：版本控制、分支、worktree（隔离底座）、diff/patch、merge/rebase、**冲突检测（唯一权威）**、历史/reflog、hooks、ignore。
**GitHub（或任何远端）承担（可选）**：远端备份/多机同步、PR 作为评审界面、CI、branch protection、issue 作为任务源。
**v1 态度**：**本地 git 必需；远端可选；PR 不是必需通道**（Curis 的 Gate 是产品内对象）。

### Q22. 哪些东西绝对不要由 Curis 重新开发？

**11 项**（详见 09 号文档 §6）：Multi-Agent Coding Framework｜版本控制语义｜工作区隔离原语｜diff/patch 格式｜agent 内部上下文压缩｜Provider 内部 subagent/agent-teams 机制｜浏览器/桌面自动化引擎｜代码审查模型｜测试框架｜知识库系统（可借 Codex 的 linters+CI+doc-gardening 实践）｜把 GitHub PR 做成 v1 必需通道。

### Q23. 当前 RD HTML 哪些产品表达可能因此需要修改？

**6 项，其中 3 项是结构性的**（详见 10 号文档）：

| # | 问题 | 严重度 |
|---|---|---|
| IMPACT-1 | **Provider 被画成了 Conversation 的发言者**（原型里有 `who: 'provider', name: 'Claude Code'`）——**与原型自己的原则文案"Employee 是责任归属者，Provider 是能力提供方"自相矛盾** | 🔴 最高 |
| IMPACT-2 | **"两个并行 Work 互不干扰"是断言，全文 `worktree`/`branch` 出现 0 次**——没有任何东西支撑这句话 | 🔴 高 |
| IMPACT-3 | **状态挂在 Provider 上**（`provider:'Claude Code', status:'needs_ceo'`）——状态应由 Work/事实派生；且 Provider 不可能"需要 CEO" | 🔴 高 |
| IMPACT-4 | 缺少 **WorkResult / Verification** 两个对象 | 🟡 中 |
| IMPACT-5 | "不画 Git"这条原则**过粗**——应改为"不做 git 工具，但必须让『这次改动从哪来、在哪做、与谁隔离』可见" | 🟡 中 |
| IMPACT-6 | 缺少 **Work → Work 接力**的表达（"重新派发"≠"接力"） | 🟢 低-中 |

**已对齐的部分（好消息）**：Provider 作为能力提供方的定位、`work.provider` 字段、并行 Work 的叙事、`needs_ceo`/Decision 的存在、"不画 IDE/Terminal/CI"的原则——**方向都是对的**。

### Q24. 是否已经足够进入 RD 定向视觉修订？

**研究层面已足够；建议先取 CEO 一次裁定，再进入视觉修订。** 理由见 10 号文档 §6：
1. 底层工作模型已成形（Workspace 模型 / Context 四分层 / 能力拆分 / 交接与恢复），**不会再因"机制不清"反复推翻视觉**。
2. 但有 **6 项产品表达需先裁定**（其中 3 项会直接改变 Conversation 主面与 Work 卡片表达）——**先改视觉再裁定等于返工**。
3. 本轮被明确要求"不做 UI"。

**建议的 Gate 表述**：是否接受 ①Provider 退出 Conversation 主面（改为 WorkResult 对象）②Work 增加"隔离位置（分支/基线）"只读表达 ③状态归 Work 且必须能表达 `no_signal` ④Workspace 采 Option D（worktree 默认，容器预留）⑤Provider 四槽适配层与 WorkResult 归一化列入 Runtime P0。

---

## 5. 状态与下一 Gate

```
RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW
```

**交付清单**：11 份文档 + `evidence/E01–E07`（7 份真实证据）✅
**实验目录**：`RD_MULTI_AGENT_RESEARCH_LAB/`（5 个 shallow clone，git 未跟踪）✅
**停止条件达成**：开源项目筛选 ✅ · Deep Dive ✅ · 源码/必要验证 ✅ · Multi-Agent Runtime 模型 ✅ · Project Working Space 模型 ✅ · Curis Translation Impact ✅

**STOP。** 等待 CEO 裁定 §4-Q23 的 6 项产品表达与 §4-Q24 的 Gate 表述后，再开 RD 定向视觉修订。

---

## 6. 必须一并提交的三条限制（不得省略）

1. **未做端到端多 Agent 真机实验**——全部"吞吐/冲突率"类结论均来自公开资料并已标注等级，**未在本机验证**。
2. **Claude Code 本机未安装** → 其全部结论为 **L3 官方文档**，无 L1 实测。
3. **Orca / vibe-kanban 仅做到 README + 元数据级**（L3/L4），未做源码深挖；`stablyai/orca` 存在 **6 个月 7.2 万星 + 6,323 未处理 issue** 的异常组合，**其 star 数不作为质量证据**。
