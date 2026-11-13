# CURIS RD — FAILURE RECOVERY AND LONG-RUNNING MODEL

**Authority Class**: RESEARCH
**Status**: Draft → Review
**证据**：`E05`（AO `domain/status.go` 完整状态枚举 + `activity_state` 五态 + `session.go`）、`E03`（AO architecture：durable facts vs derived status；detached per-session host）、Claude Code agent-teams 官方 limitations（L3）、Codex `resume`/`fork`/`compact`（L1+L4）、Copilot cloud agent（环境即焚）（L3）、OpenHands EventLog replay（L4/L5）、container-use "discard failures instantly"（L2）。

---

## 1. 失败分类（先分类，否则"恢复"会做错）

| 类 | 失败 | 是否可自动恢复 | 恢复手段 | 证据 |
|---|---|---|---|---|
| **F1** | Agent 崩溃 / 进程被杀 | ✅ 可 | 重启执行体；Workspace 与分支仍在 | AO `Runtime Reaper` + detached host；claude-squad `r` resume |
| **F2** | 超时（产出正确但太慢） | ⚠️ 部分 | 延长/换 Provider 重跑（L-b 替换） | Codex 官方"单任务可跑 6 小时+"说明超时阈值不能设太短 |
| **F3** | **上下文超限** | ✅ 可 | Provider 自己的 compaction | Codex `/compact` + `remote_compaction_v2`（stable）；OpenHands Condenser |
| **F4** | Provider 错误 / 限流 / 额度耗尽 | ✅ 可 | **换 Provider 重跑**（L-b） | 本领域已把"多 Provider"当常态（AO 30+ 适配器） |
| **F5** | 测试失败 | ✅ 可 | 交回同一执行体迭代（"测试失败是正常循环，不是异常"） | Copilot：agent 在**同一会话内**迭代直到测试通过 |
| **F6** | 合并冲突 | ✅ 可（但需判断） | 优先让 agent 解决（有 Provider 专长） | Copilot 官方把 "Resolve merge conflicts" 列为 agent 能力；Codex/Claude 视冲突为正常 |
| **F7** | **权限/审批阻塞**（agent 在等人批准） | ✅ 可，但**不得自动化** | 上浮给人；**绝不允许自动注入输入** | AO 原文："`blocked` is an agent stopped on a pending permission/approval decision — **automation must never inject input into a blocked session**"；Claude Code：teammate 权限请求冒泡到 lead，且"teammate 不能替人批准" |
| **F8** | **需要登录/凭据（Human Gate）** | ❌ 不可自动 | 停止 → 存位置 → 通知人 → 等人 | 沿用既有裁定：`WAITING_FOR_USER`（**不得另造状态名**）；禁重试登录/绕 CAPTCHA/切账号 |
| **F9** | **状态未知**（Hook 断了，无法判断在跑还是卡住） | ❌ 不可自动判定 | **明确显示"无信号"**，而不是乐观 idle | AO `StatusNoSignal` 原文："AO cannot tell whether the agent is working or stuck … Rendered instead of a confident idle." |
| **F10** | **执行体自我报告"完成"但实际未完成** | ❌ 不可自动信任 | **必须由外部验证**（Review / 测试 / Gate） | Claude Code 官方 limitation 原文："teammates sometimes fail to mark tasks as completed, which **blocks dependent tasks**"——**自我报告不可靠是已被承认的事实** |

> **F10 是最重要的一条**：它同时解释了为什么 Curis 需要 **Verification 环节独立于执行**、以及为什么 Work 状态**不能由 agent 自己声明**。

---

## 2. 状态模型（提案，直接借鉴 AO 的"事实 vs 派生"分离）

### 2.1 只有两类东西该被持久化

| 类别 | 内容 | Curis 对应 |
|---|---|---|
| **Durable Facts**（持久事实） | ①`activity_state`（`active / idle / waiting_input / blocked / exited`）②`is_terminated` ③执行体绑定（Provider + 会话句柄 + generation）④**接口/执行槽切换检查点** ⑤Workspace 记录（path/branch/base/lock）⑥Gate/Decision 记录 ⑦Review 与验证结果 | Curis Runtime 的持久层 |
| **Derived Status**（派生状态，读取时计算、**绝不存储**） | `working / needs_input / ci_failed / review_pending / changes_requested / approved / mergeable / needs_input / exited / idle / terminated / no_signal / pr_open / draft / merged` | **UI 展示层**（Employee Work Surface / Decision Banner） |

**理由（AO 原文）**："Display status is never stored. It is computed at read time from durable facts." → 好处：状态永不与事实不一致；不需要"状态迁移"的事务；新增一个展示状态不影响持久层。

### 2.2 关键状态语义（必须精确定义，不得含糊）

| 状态 | 精确含义 | 禁止的自动化行为 |
|---|---|---|
| `waiting_input` | agent 停在空 prompt，等下一句指令 | — |
| `blocked` | agent 停在**待批准决策**上 | **禁止注入任何输入**（AO 明文） |
| `no_signal` | 活着的会话，但**从未收到 hook 回调** | 禁止显示为 idle；禁止自动判定失败并重跑 |
| `waiting_for_user`（Curis 既有词） | 需要**人**（登录/凭据/业务决策） | 禁止重试登录、绕 CAPTCHA、切账号 |
| `effect_unknown`（Curis 既有 G4） | **写操作已发出但结果未知** | 禁止盲目重放；必须走人工确认 |

---

## 3. 恢复机制清单

### 3.1 三层检查点（按"最便宜的先试"排序）

| 层 | 检查点 | 恢复代价 | 何时使用 |
|---|---|---|---|
| **P1 会话级** | Provider 原生 `resume`（Codex `resume`；Claude Code `/resume`） | 最低 | F1/F3；且**仅当会话句柄仍有效** |
| **P2 分支级** | 已 commit 的分支 + base SHA（git 天然提供） | 低 | F1/F2/F4/F5/F6；**这是 Curis 的主力恢复层** |
| **P3 工作区级** | Workspace 目录 + diff（未 commit 的变更） | 中 | P1/P2 都不行时；**未提交变更不可靠**，只作参考 |
| **P4 重跑** | 用 C2（Work Context）自包含重建 Workspace，重跑 | 高（浪费算力） | 兜底；**要求 Work Context 自包含**（这正是"Work Context 必须自包含"的理由） |

### 3.2 恢复决策树

```
检测到 Work 未完成
├─ `blocked`（待批准）        → 上浮给人，禁止自动化          [F7]
├─ `waiting_for_user`         → 停止 + 存位置 + 通知人         [F8]
├─ `effect_unknown`           → 人工确认，禁止重放             [G4]
├─ `no_signal`                → 先探活（进程/句柄），
│                               无法判定 → 上浮人              [F9]
├─ 有有效会话句柄             → Provider resume                 [P1]
├─ 有已 commit 的分支         → 在新 Workspace checkout 继续    [P2]
├─ 只有未提交变更             → 保留 Workspace 供人判断         [P3]
└─ 什么都没有                 → 用 C2 自包含重跑                [P4]
```

### 3.3 明确"不做"的恢复

| ❌ 不做 | 理由 |
|---|---|
| 自动重放一个"写操作结果未知"的 Work | 会产生重复副作用（既有 G4 裁定） |
| 在 `blocked` / `waiting_for_user` 上自动重试 | AO 明文禁止；且会产生"绕过人审批"的实质后果 |
| 用日志（C3）重建上下文后重跑 | 日志是证据不是输入；会导致上下文噪声与幻觉 |
| 无限重试 | 多 agent 已有"token 消耗 15 倍"的公开测算；必须**限次 + 限时 + 限成本** |

---

## 4. Long-running（回应用户 §9-Long-running、§24-20）

### 4.1 什么该长期保存 / 什么只是临时

| 类别 | 内容 | 生命周期 |
|---|---|---|
| **长期保存（项目寿命）** | Canonical Project Root（含 `.git`）；仓库内的项目地图与 `docs/`（含 exec-plans 的历史）；**Decision / Gate 记录**；**Conversation Context**（问责记录）；已归档的 Work 与其 WorkResult | 月-年 |
| **中期保存（Work 寿命）** | Work Context；Workspace 记录（含 base SHA、branch）；Review/验证结论 | 小时-天（+ 保留期） |
| **临时（执行寿命，结束即冻结或销毁）** | Execution Context（prompt / 事件流 / 日志 / 工具状态）；Workspace 目录本身；Provider 会话进程 | 分钟-小时 |

**判据（一句话）**：**"如果第二天需要它才能继续工作，它就是长期；如果丢了只会损失时间，它就是临时。"**

### 4.2 "第二天如何继续"（必须能回答的具体场景）

| 场景 | 依赖什么 | 业界证据 |
|---|---|---|
| 昨天有 Work 在跑，今天想接着做 | ①Workspace 记录（path/branch/base）②分支上的 commit ③Provider 会话句柄（可能已失效） | Codex `resume`/`fork`；claude-squad `~/.claude-squad/storage.json`；AO durable facts + **detached per-session host**（daemon 重启不中断 turn） |
| 昨天有 Work 卡在等人 | Gate/Decision 记录（**必须持久**） | Claude Code mailbox 落在 `~/.claude/teams/{team}/inboxes/`；AO PR 事实表 |
| 昨天在等我做技术决策，我忘了 | **Decision 必须在产品里可见且未决** | Curis 既有 `Decision 内嵌 Banner` |
| 我关了机器，agent 还在跑吗 | 单机场景下**不会**（这正是 v1 单机本地自用的固有边界） | Copilot 的云执行是唯一"关机也跑"的形态；**Curis v1 不应承诺这个** |
| 三个月后我想知道当时为什么这么决定 | **Decision 记录 + exec-plans 历史** | Codex 官方：plans 是一等工件，active/completed 均版本化 |

### 4.3 长期运行的四个必备能力（缺一不可）

1. **会话可恢复**（P1/P2 检查点）——否则"重跑"会成为唯一手段，成本爆炸。
2. **状态可观测**（Facts 持久 + Status 派生 + **no_signal 显式化**）——否则用户会看到"假 idle"。
3. **上下文可压缩**（Provider compaction + Curis 侧摘要）——否则会撞上下文墙。
4. **决策不丢**（Gate/Decision 持久）——否则"长期项目"会在几次会话后失忆。

### 4.4 Workspace 回收与"第二天继续"的冲突（必须裁定的取舍）

| 策略 | 优点 | 风险 |
|---|---|---|
| 立即回收（Work 一结束就销毁） | 磁盘干净 | 失败产物丢失；想"接着看看"时已没了 |
| 定期回收（N 天后清扫） | 兼顾 | 与"第二天继续"冲突 |
| 按状态回收 | 精细 | 复杂度上升 |

**建议（提案）**：
- `COMPLETED + 已收口` → 立即回收（成果已在 Canonical）
- `FAILED / ABANDONED` → **保留 N 天**（默认 7 天，用户可配），并**明确标记"这是失败的 Work，产物未进入项目"**
- `WAITING / BLOCKED` → **永不自动回收**（有未完成的 Gate）
- 复用既有分支的 Workspace → **回收时不删分支**（claude-squad `isExistingBranch` 的教训）
- **运行中锁定** → 回收前必须确认锁已释放（Claude Code `git worktree lock`）

---

## 5. 可观测性要求（"失败可见"的最低标准）

| 要求 | 反面案例 |
|---|---|
| 每个 Work 必须能回答"**现在在哪一步**"（分配 / 就绪 / 执行 / 结算 / 评审 / 集成 / 回收） | Claude Code 的"任务状态滞后"会把依赖卡死而外部看不出来 |
| 每个 Work 必须能回答"**上一次外部可观测的活动是什么时候**" | 否则无法区分"在跑"与"卡住" |
| 无法判定时必须显示 **`no_signal`** | AO 明确"拒绝乐观 idle" |
| 每个失败必须落到**具名枚举**，不是一个笼统的 `error` | AO 有 15 个具名状态；Copilot 有明确的"环境已销毁"语义 |
| 任何人（或 Leader）应能只看**派生状态**就决定下一步 | AO 的 Kanban 就是纯派生的 |

---

## 6. 遗留未知

| # | 未知 | 建议 |
|---|---|---|
| U14 | Curis v1 是否需要"关机继续跑" | 建议**明确不做**（单机本地自用的固有边界）；如需，只能靠 Provider 云能力，属 L2 Gate |
| U15 | Workspace 保留期默认值 | 建议 7 天，用户可配 |
| U16 | 成本上限策略（单 Work token / 单日成本） | 建议 v1 只做**可见 + 可中止**，不做自动预算拦截 |
| U17 | 是否引入"自动重试 N 次" | 建议：**只对 F1/F4/F5 自动重试（≤2 次）**，其余一律上浮人 |
