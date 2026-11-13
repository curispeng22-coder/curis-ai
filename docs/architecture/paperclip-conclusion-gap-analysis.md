# Paperclip 研究结论 × Curis 代码库 · 落地差距分析

> 作者：架构师 高见远（software-architect）
> 受众：主理人 齐活林（向总控决策席汇报用）
> 性质：**分析 / 差距核对**，**不含实现代码**
> 输入：用户提供的 Paperclip 研究结论（精炼版）× Curis 当前代码库**实测**（Grep/Read 全仓核对）
> 关联：既有 paperclip 映射报告 `581ed7d6`、B 层治理三件套（`b-layer-runtime-governance*.md`，commit `67a21aa4`+`e1d0b78e`+`0750026c`）
> 生成日期：2026-07-20

---

## 1. 总览表

> 判定四档：**已实现 / 部分 / 未实现 / 正确规避**。
> 「部分」一律标出已落地点与缺口；「正确规避」指结论明确要求**不**做、且代码库确实未做（保持冻结/预留）。

| # | 结论条目 | 判定 | 关键证据（文件:行） | 一句话说明 |
|---|---|---|---|---|
| M1 | 模式对比·真实运行 | **部分** | `real_rd_executor.py:447-480`（begin immediate 单次领取）、`dev_agent.py`（DevAgent 6 后端）、`evolution_event_log.py:22`（审计）、`local_rd_toolset.py:578`（git checkout 回滚） | 有 RealRD/DevAgent/审计/回滚，但**缺通用 Wake/Session/Claim** 抽象 |
| M2 | 模式对比·管理控制 | **部分** | `governance.py`（L2 Gate + `LOCKED_ACTIONS`）、`runtime_governance.py:67a21aa4`（闸已进运行时）、`decision_sink.py:0750026c`（待决策持久化） | 产品 Gate 强，约束**已部分进入运行时**（B 层闸引擎近期落地），尚未全量覆盖 |
| P0-1 | Task 原子领取与执行锁（ExecutionClaim） | **部分** | `real_rd_executor.py:447-480`、`d1_single_model_toolchain.py:179`（`_claim_once` begin immediate） | 单任务级「begin immediate 条件写」领取已存在，但**未抽象为通用 ExecutionClaim**；RealRD 的 SQLite 单次领取可保留但应提升为通用机制 |
| P0-2 | WakeRequest 与 AgentTaskSession | **未实现** | 全仓（除 docs/research）无 `agent_wakeup_requests`/`agent_task_sessions`/`WakeRequest`/`AgentTaskSession`/`coalesced_count`/`claimed_at`/`finished_at` | 无唤醒/会话表与类；`employee_sessions`（`database.py:2432`）是员工会话审计，**非** AgentTaskSession |
| P0-3 | 运行配置指纹（SHA-256） | **未实现** | 全仓（除 docs）无 `config_hash`/`run_fingerprint`；`sha256` 仅用于 `credential_vault.py:373`、`local_rd_toolset.py:754`、`workflow_runtime.py:388`（内容/预镜像哈希） | 无「去时间戳/路径噪声 + 脱敏 Secret」的**运行配置稳定指纹**；算法可直接翻译但未实现 |
| P0-4 | 恢复与异常测试用例 | **部分** | `real_rd_executor.py:459`（`issue_already_running` 防重入）、`_safe_rollback`/`git checkout` 回滚、脱敏红线 | 重复 checkout 不双执行、Secret 不进指纹/日志**基础断言可支撑**；但 Wake 幂等合并、阻塞取消唤醒依赖项**无机制可测**（依赖 P0-2） |
| P1-1 | 审批卡与阻塞决策（CEO 决策中心） | **部分** | 后端：`governance.py:271`（`apply_proposal` 接 `pending_sink`）、`runtime_governance.py` T08（G5–G8）、`decision_sink.py:0750026c`、`real_rd_executor.py:842`/`governance.py:412`/`content_workflow_runtime.py:302`（落 `b.governance.gate`）；前端：`frontend/app/ceo-office/page.js:27`（仅 overview，无审批卡读取） | **后端机制 done / 前端 pending**——闸评估+待决策持久化已实现，但 CEO 决策中心 UI 未接 `PendingDecisionStore`（归 Workspace 前端团队） |
| P1-2 | 真实运行时间线 | **未实现** | `main.py` `/api/ceo/overview`（部门/员工/工作流实例/公司包概览）、`ceo-office/page.js`（列表）、`evolution_events` 审计流 | 无「运行时间段 + 等待/阻塞/失败/恢复状态 + 按 部门→员工→工作流→执行 组织」的时间线视图 |
| P1-3 | 组织图布局算法 | **未实现** | `ceo-office/page.js`、`employees/page.js`（基础列表） | 无「树形布局 CEO→Department→Employee→Skill/Tool」呈现；复用树形算法但展示层未做 |
| P2-1 | 插件 Capability 权限模型 | **正确规避** | `USER_CAPABILITY_LEDGER.md` G9（Marketplace 冻结 L2 #4）、`governance.py`（`LOCKED_ACTIONS`） | 当前 Marketplace/Credential Vault/多租户冻结，结论明确**不应现在引入完整插件运行时** |
| P2-2 | 内部预算硬停 | **未实现** | `runtime_governance.py:147`（`token_hard_limit` 为**弹闸问用户**）、`test_b_layer_*.py` 断言全仓**无 `budget_guard`** | 仅 B 层 G4「超 token 弹闸让用户拍板」，缺**自主**的 Agent/Project 成本上限+软提醒+硬暂停（≠用户询问闸） |
| N1 | 不复制 heartbeat.ts（拆调度/领取/恢复/监控） | **正确规避** | 无 `heartbeat` 全仓匹配；`RealRDExecutor` 用户请求驱动 | 未引入长驻调度内核，符合自用 scope |
| N2 | 不迁移全套 DB/history migration | **正确规避** | 沿用既有 `evolution_events` 追加写 + `_ensure_column` 增量 | 未做 Paperclip 式全量迁移 |
| N3 | 不复制 Dashboard（任务/Agent 运维视角） | **正确规避** | `ceo-office/page.js` 为 CEO 概览，非 Agent 运维面板 | 未做任务/Agent 运维视角 Dashboard |
| N4 | 不复制 PostgreSQL/Drizzle → SQLite/FastAPI | **正确规避** | Curis 本就 SQLite/FastAPI（`database.py`、`main.py`） | 未反向引入 PG/Drizzle |
| N5 | 不复制品牌/Logo/未授权视觉资产 | **正确规避** | `frontend` 自有设计语言（`globals.css` ceo-*） | 未搬运外部品牌资产 |
| N6 | 不先做完整插件 Worker/公开服务器/多租户部署 | **正确规避** | L2 冻结（G1–G9）；`deploy/` 仅本地 | 未做公开服务器/多租户部署 |
| N7 | MIT 许可·复制源码须保留版权声明 | **正确规避** | 既有代码注释保留上游版权；本次分析零代码复制 | 合规红线已遵守 |
| I-A | Issue A·通用 Agent Execution Kernel | **建议（未落地）** | 见 §4 | 规划席建议，尚未建 Issue |
| I-B | Issue B·CEO Office 真实运行证据 | **建议（未落地）** | 见 §4 | 规划席建议，尚未建 Issue |

---

## 2. 逐项详述

### M1 · 模式对比·真实运行

- **结论要求**：Paperclip 有 Heartbeat / 任务领取 / 唤醒 / 会话续接 / 恢复；Curis 已有 RealRD、DevAgent、审计、回滚，但缺通用 Wake / Session / Claim。
- **Curis 现状**：
  - 真实运行闭环：`RealRDExecutor.run` → 读→改→测→git diff（`real_rd_executor.py`）。
  - 后端可插拔：`DevAgent` Protocol + 6 后端（`dev_agent.py`）含 Codex/WorkBuddy 真·agent。
  - 审计追加写：`EvolutionEventLog.record`（`evolution_event_log.py:22`，含 `idempotency_key` 去重 L33-39）。
  - 回滚：`LocalRDToolset` git checkout / 乐观锁 sha256（`local_rd_toolset.py:578,754`）。
  - 单任务领取：RealRD `begin immediate` 条件写（`real_rd_executor.py:453-479`）。
- **证据**：同上各行号。
- **差距**：无「通用 Task Runtime」抽象；无 Wake（唤醒合并/幂等）、无 AgentTaskSession（会话续接）、无通用 ExecutionClaim（仅 RealRD 内联实现一次领取）。
- **建议落点 Issue**：Issue A（P0-1/P0-2/P0-3）。

### M2 · 模式对比·管理控制

- **结论要求**：Curis 产品 Gate 强，但部分约束尚未进入运行时。
- **Curis 现状**：A 层 L2 Gate 七项 + `LOCKED_ACTIONS`（`governance.py`）；B 层运行时治理闸引擎**近期已落地**（`runtime_governance.py:67a21aa4`，T01–T08）、待决策持久化（`decision_sink.py:0750026c`）、四接线点落 `b.governance.gate`。
- **证据**：`governance.py`、`runtime_governance.py`、`decision_sink.py` 三个 commit；`real_rd_executor.py:842`/`governance.py:412`/`content_workflow_runtime.py:302`。
- **差距**：结论「部分约束尚未进入运行时」在撰写时成立，但 B 层闸引擎落地后，约束进入运行时的程度已显著提升；剩余缺口主要在**审批卡/阻塞决策的 UI 呈现**（见 P1-1）与**唤醒/预算硬停的自主执行**（P0-2/P2-2）。
- **建议落点 Issue**：Issue A、Issue B。

### P0-1 · Task 原子领取与执行锁（ExecutionClaim）

- **结论要求**：在通用 Task Runtime 增加 `ExecutionClaim`，用 DB 条件更新保证同一任务只有一个执行者；RealRD 当前 SQLite `BEGIN IMMEDIATE` 单次领取可保留但应抽象为通用机制。
- **Curis 现状**：`RealRDExecutor._claim_once`（`real_rd_executor.py:447-480`）使用 `begin immediate` + 「先查 started 标记、后插」实现单主占锁，重入抛 `issue_already_running`（L459-462）；D1 亦同构（`d1_single_model_toolchain.py:179`）。
- **证据**：`real_rd_executor.py:453`（begin immediate）、`:459`（issue_already_running）、`:465-479`（insert started marker）。
- **差距**：① 仅 RealRD/D1 内联实现，无跨 Task 类型的通用 `ExecutionClaim` 类/表；② 锁以 `evolution_events` started 标记承载，非独立执行锁表；③ 非常规 Task Runtime 复用。
- **建议落点 Issue**：Issue A（抽象出通用 ExecutionClaim，RealRD 单次领取保留并下沉为通用机制）。

### P0-2 · WakeRequest 与 AgentTaskSession

- **结论要求**：增加 `agent_wakeup_requests` / `agent_task_sessions` 表，含 `idempotency_key` / `coalesced_count` / `claimed_at` / `finished_at` / Agent 与任务级 session 参数；支持唤醒合并、幂等、状态跟踪、会话续接。这是从「单次调用 Agent」升级到「持续运营员工」的关键。
- **Curis 现状**：**无任何** `agent_wakeup_requests` / `agent_task_sessions` 表或 `WakeRequest` / `AgentTaskSession` 类；`idempotency_key` 仅存在于 `EvolutionEventLog.record`（`evolution_event_log.py:29`）；`employee_sessions`（`database.py:2432`）是员工会话审计绑定，与「Agent+任务级 session 续接」语义不同；`coalesced_count` / `claimed_at` / `finished_at` 全仓无匹配。
- **证据**：全仓 Grep（backend/app）对 `agent_wakeup_requests|agent_task_sessions|WakeRequest|AgentTaskSession|coalesced_count|claimed_at|finished_at` 零命中（docs/research 除外）。
- **差距**：完全未实现。这是 P0 缺口里最重的一块——直接决定「持续运营员工」能否落地。
- **建议落点 Issue**：Issue A（建两表 + 通用 session 参数 + 唤醒合并/幂等/续接）。

### P0-3 · 运行配置指纹

- **结论要求**：对实际运行配置生成稳定 SHA-256 指纹（去时间戳/路径噪声、脱敏 Secret），应用于 DevAgent 调用、工作区配置、Skill/Tool 版本、模型与适配器配置、审计与可复现执行。可直接把算法翻译成 Python。
- **Curis 现状**：`hashlib.sha256` 仅用于内容/预镜像/凭证摘要——`credential_vault.py:373`（secret→`sha256:` digest）、`local_rd_toolset.py:754`（值哈希）、`workflow_runtime.py:388`（内容 sha）、`evolution_event_log` 等。**无**「运行配置」这一稳定指纹概念，`config_hash` / `run_fingerprint` 全仓零命中。
- **证据**：Grep `config_hash|run_fingerprint` 无匹配；`sha256` 命中均非配置指纹语义。
- **差距**：完全未实现。算法可直译，但需定义「配置归一化（去噪+脱敏）→ SHA-256」的字段集合与序列化规则。
- **建议落点 Issue**：Issue A（配置指纹模块，落地到 DevAgent 调用/工作区/Skill-Tool 版本/模型适配器/审计）。

### P0-4 · 恢复与异常测试用例

- **结论要求**：借测试约束——重复 checkout 不得双执行、终止 run 必须释放锁、阻塞任务取消后唤醒依赖项、Wake 请求幂等可合并、Secret 不得进指纹和日志、非 Git 工作区明确降级或拒绝。
- **Curis 现状**：
  - 重复 checkout 不双执行：✅ `_claim_once` 重入抛 `issue_already_running`（`real_rd_executor.py:459`）。
  - 终止 run 释放锁：⚠️ 部分——锁以 evolution_events started 标记承载，回滚走 `git checkout`（`_safe_rollback`）；但「终止即释放标记」无独立测试断言。
  - Secret 不进指纹/日志：✅ 脱敏红线（异常只出 failure_code；`credential_vault` 仅存 digest）。
  - 阻塞取消唤醒依赖项 / Wake 幂等合并 / 非 Git 降级：❌ 依赖 P0-2（无 Wake/Session），机制与测试均不可存在。
- **证据**：`real_rd_executor.py:459`、脱敏红线（各 executor docstring）、`local_rd_toolset.py` sandbox 降级（`SandboxMode`）。
- **差距**：基础断言（防重入/脱敏）可支撑；Wake 相关两条测试**因 P0-2 缺失而无法编写**；非 Git 工作区降级无专门测试。
- **建议落点 Issue**：Issue A（配套 P0-1/P0-2 的异常测试套件）。

### P1-1 · 审批卡与阻塞决策（CEO 决策中心）

- **结论要求**：借鉴 Approval/Budget Incident/暂停恢复，放进 Curis「CEO 决策中心」，不照搬任务详情页。
- **Curis 现状（后端**已实质覆盖**）**：
  - B 层闸评估引擎 `runtime_governance.py`（T01–T08，`67a21aa4`）覆盖 G1–G8，含 G5–G8 治理类（计费/Marketplace/权限/核心资产）业务风险呈现。
  - 真实 `DecisionSink` 后端 `decision_sink.py`（`0750026c`）：`PendingDecisionStore`（sqlite 持久化）、`PendingDecisionSink`（非阻塞）、`resolve_decision` resolver、`get_letter` fail-closed 单一真源。
  - 三接线点（RealRDExecutor / ContentWorkflowRuntime / CompanyGovernance）接 `pending_sink` 旁路，落 `b.governance.gate` 事件（`real_rd_executor.py:842` / `governance.py:412` / `content_workflow_runtime.py:302`，commit `e1d0b78e` 修复 T08 落库）。
- **证据**：`governance.py:271`（`apply_proposal(proposal_id, decision_sink, pending_sink)`）、`:342`（_governance_present）、`:379-387`（decision_sink.ask + outcome_for_letter）；`decision_sink.py:382`（PendingDecisionSink）；`runtime_governance.py:271`（outcome_for_letter）。
- **差距（前端 pending）**：`frontend/app/ceo-office/page.js:27` 仅渲染部门/员工/工作流实例/公司包**概览**，无「审批卡」「待决策列表」「A/B/C/D 拍板」组件；全仓前端**无**读取 `PendingDecisionStore` 的代码（Grep `pending|decision|governance|gate` 于 frontend 仅命中 `gateway_ref` 与 admin 审计面板，非决策中心）。UI 呈现与 resolver 前端调用明确属 **Workspace 前端团队**（2026-07-13 裁定），本团队不主导。
- **建议落点 Issue**：Issue B（后端把待决策暴露为可读端点/投影；UI 归 Workspace 前端团队，本边界只交付数据层）。

### P1-2 · 真实运行时间线

- **结论要求**：借鉴 Work Timeline（运行时间段、等待/阻塞/失败/恢复状态、Agent/Employee 活跃证据、缩放定位），按「部门→员工→工作流→执行」组织，而非仅按 Agent Run 罗列。
- **Curis 现状**：`/api/ceo/overview`（`main.py` L3166-3219）返回部门/员工/工作流实例/公司包；`ceo-office/page.js` 渲染列表；`evolution_events` 提供审计流但无「运行状态机（waiting/blocked/failed/recovered）+ 层级组织」的时序视图。
- **证据**：`USER_CAPABILITY_LEDGER.md` B15（CEO 概览）、`ceo-office/page.js`、`evolution_event_log.py`。
- **差距**：完全未实现时间线视图（状态维度 + 层级组织 + 缩放定位）。
- **建议落点 Issue**：Issue B（后端投影：运行时间线数据，按 部门→员工→工作流→执行 组织，带状态维度）。

### P1-3 · 组织图布局算法

- **结论要求**：复用树形布局计算，但展示 CEO→Department→Employee→Skill/Tool（非 Agent→Agent）。
- **Curis 现状**：`ceo-office/page.js` 与 `employees/page.js` 为平面列表；无树形布局/组织图组件。
- **证据**：`ceo-office/page.js`、`employees/page.js`（基础列表，无层级树渲染）。
- **差距**：未实现 CEO→Department→Employee→Skill/Tool 树形组织图（含 Skill/Tool 展开）。
- **建议落点 Issue**：Issue B（后端提供层级树数据 + 前端树形布局，归 Workspace 前端团队）。

### P2-1 · 插件 Capability 权限模型

- **结论要求**：operation→capability 映射，安装+运行两阶段校验；但 Marketplace/Credential Vault/多租户当前冻结，不应现在引入完整插件运行时。
- **Curis 现状**：Marketplace / 外部生态导入冻结（`USER_CAPABILITY_LEDGER.md` G9，L2 #4）；`governance.py` `LOCKED_ACTIONS` 锁定边界；无 operation→capability 映射与两阶段校验。
- **证据**：`USER_CAPABILITY_LEDGER.md` G9、L2 冻结清单（G1–G6）。
- **差距/判定**：**正确规避**——结论明确要求「现在不引入完整插件运行时」，代码库确实未做，保持冻结。
- **建议落点 Issue**：本期不建；冻结解除时再单列。

### P2-2 · 内部预算硬停

- **结论要求**：先实现「Agent/Project 成本上限、软提醒、硬暂停」，不提前扩展为 Billing/套餐/商业结算。
- **Curis 现状**：B 层 G4 `token_hard_limit=200000`（`runtime_governance_config.json:16`）触发的是**弹闸问用户**（`runtime_governance.py:147`：`estimated_tokens > token_hard_limit` 归类 G4 让用户拍板），属「用户询问闸」而非「系统自主硬停」。paperclip 3.1 的 `budget_guard`（基于 `total_tokens` 的 `BudgetGuard` 类 + hard_stop_ratio 抛 `budget_exceeded` + git 回滚）**全仓未实现**（测试显式断言「无 budget_guard 模块」）。无 Agent/Project 级成本上限、软提醒、硬暂停。
- **证据**：`runtime_governance.py:147`、`:251-256`（G4 比对配置硬限→弹闸）、`test_b_layer_runtime_governance.py:360-371`（断言无 budget_guard）、`test_b_layer_decisionsink.py:371`（decision_sink 不依赖 budget_guard）。
- **差距**：缺**自主**预算硬停（Agent/Project 上限+软提醒+硬暂停）；现有 G4 是「问用户」而非「自主停」。注意区分：B 层治理 token 预算（问用户）= 已落地；DevAgent 成本上限（自主停）= 未实现（P2-2）。
- **建议落点 Issue**：Issue C（内部预算硬停：Agent/Project 成本上限 + 软提醒 + 硬暂停，复用 `total_tokens` 累加，fail-closed，不触 L2 商业）。

---

## 3. 特别标注：B 层治理已实质覆盖 P1-1 后端机制

**结论**：P1-1「审批卡与阻塞决策」的**后端机制已由 B 层运行时治理工作实质覆盖**，判定为 **部分（后端 done / 前端 pending）**。

| 层次 | 状态 | 证据 |
|---|---|---|
| 闸评估引擎（G1–G8，含 G5–G8 治理类业务风险呈现） | ✅ 已落地 | `runtime_governance.py`（commit `67a21aa4`，T01–T08） |
| 待决策持久化（PendingDecisionStore / Sink / resolver） | ✅ 已落地 | `decision_sink.py`（commit `0750026c`） |
| 四接线点落 `b.governance.gate` 脱敏事件 | ✅ 已落地 | `real_rd_executor.py:842` / `governance.py:412` / `content_workflow_runtime.py:302`（commit `e1d0b78e` 修 T08 落库） |
| 统一 outcome 映射（`outcome_for_letter`） | ✅ 已落地 | `runtime_governance.py:271` |
| **CEO 决策中心前端**（审批卡 UI / 读取待决策 / A-B-C-D 拍板） | ⏳ **pending** | `frontend/app/ceo-office/page.js:27` 仅 overview；前端无 `PendingDecisionStore` 读取（Grep 验证） |

> **边界明确**：UI 呈现与 resolver 前端调用属 **Workspace 前端团队**（2026-07-13 裁定本团队不主导 Workspace 端 UI）。本团队本期交付了**后端机制 + headless 测试桩 + 接线旁路（默认关闭）**，前端接入（把 `pending_id` 返前端、调 `resolve_decision`、resume 编排）属未来 Workspace 团队任务。因此 P1-1 判「部分」，不误判为「已实现」。

---

## 4. 待办 Issue 建议（收敛未实现项，呼应 Issue A/B，严守本团队边界）

> 本团队边界：**仅后端 / 不越 Workspace UI**。以下 Issue 全部为**后端数据层/机制层**交付；所有 UI 渲染（决策卡、时间线、组织图）明确归 Workspace 前端团队，不在本 Issue 内实现页面。

### Issue A · 通用 Agent Execution Kernel（后端）
- **范围**：P0-1 + P0-2 + P0-3 + P0-4 测试套件。
- **交付物（新增，全后端）**：
  1. `ExecutionClaim`：通用 Task Runtime 执行锁，DB 条件更新保证单执行者；RealRD 现有 `begin immediate` 单次领取保留并下沉为通用机制（不重写受保护文件）。
  2. `agent_wakeup_requests` 表：`idempotency_key` / `coalesced_count` / `claimed_at` / `finished_at` + 唤醒合并/幂等。
  3. `agent_task_sessions` 表：Agent 与任务级 session 参数 + 状态跟踪 + 会话续接。
  4. 运行配置指纹模块：归一化（去时间戳/路径噪声、脱敏 Secret）→ SHA-256；应用于 DevAgent 调用、工作区配置、Skill/Tool 版本、模型与适配器配置、审计与可复现执行（算法直译 Python）。
  5. 异常测试套件：重复 checkout 不双执行、终止 run 释放锁、阻塞取消唤醒依赖项、Wake 幂等可合并、Secret 不进指纹/日志、非 Git 工作区降级/拒绝。
- **不触 L2 / 红线**：通用内核基于既有 `EvolutionEventLog` 追加写 + SQLite 条件更新，零新依赖；不改 `LOCKED_ACTIONS`。
- **验收**：上述 6 类断言全绿；复用既有 `test_real_rd_executor.py` 8 passed 基线不回归。

### Issue B · CEO Office 真实运行证据（后端数据层）
- **范围**：P1-1 前端配套（后端）+ P1-2 + P1-3 的数据投影。
- **交付物（新增，全后端）**：
  1. 待决策可读端点/投影：把 `PendingDecisionStore` 暴露为 `GET /api/ceo/pending-decisions`（脱敏 `GatePrompt` 快照，供前端渲染审批卡）；resolver 端点 `POST /api/ceo/pending-decisions/{id}/resolve`（调 `resolve_decision`）。**不实现页面**。
  2. 运行时间线投影：按 `部门→员工→工作流→执行` 组织，带 waiting/blocked/failed/recovered 状态维度（数据源 = `evolution_events` + 工作流/任务状态）。
  3. 组织图层级树数据：CEO→Department→Employee→Skill/Tool 树形结构（复用既有 catalog 关系，新增树形投影 API）。
- **不越界**：仅交付 API/数据；卡片 UI、时间线可视化、树形布局渲染归 Workspace 前端团队。
- **验收**：三个端点返回结构经单测断言；不新增前端 `page.js` 渲染逻辑（UI 由前端团队接）。

### Issue C · 内部预算硬停（后端，自主执行）
- **范围**：P2-2。
- **交付物（新增，全后端）**：
  1. `BudgetGuard`（或并入通用内核）：Agent/Project 级 `cost_upper_limit` + `warn_ratio`（软提醒）+ `hard_stop`（硬暂停，fail-closed）。
  2. 数据源复用 `RealRDExecutor.total_tokens` 累加（与 B 层 G4 用户询问闸**并存不冲突**：G4 问用户、本 Issue 自主停）。
  3. 超硬限 → 脱敏 `budget_exceeded` + 既有 `_safe_rollback`（git checkout），落审计。
- **不触 L2**：仅基于 `total_tokens`，**不引入价格表/计费/套餐**（Billing/Plan/Pricing/Quota 仍冻结）。
- **验收**：单测覆盖软提醒阈值、硬停回滚、CLI 后端 `total_tokens=0` 盲视（沿用映射报告已知局限）。

> **P2-1 不建 Issue**：Marketplace/Credential Vault/多租户冻结（L2 #4），结论明确要求现在不引入完整插件运行时，保持冻结。

---

## 5. 与既有 paperclip 映射报告（`581ed7d6`）的一致性说明

| 映射报告（`581ed7d6`）结论 | 本次核对结果 | 一致性 |
|---|---|---|
| 最该吸收 3 件：① per-agent 硬预算熔断（token 基准）② Ticket 生命周期+不可变审计加固 ③ 幂等/去重 cooldown | ① 对应 P2-2——**仍未实现**（budget_guard 缺，仅 B 层 G4 用户询问闸）；② Ticket registry **未单独落地**（P0-1 仅内联 claim）；③ 幂等占锁有（`_claim_once`），cooldown 未做 | **一致**：映射报告标注的「近期可吸收」3 件，截至本次核对**仍未完全落地**（除 B 层闸引擎这一增补） |
| 明确不采用：Heartbeat 长驻调度 | N1 正确规避（无 heartbeat 全仓匹配） | **一致** |
| 明确不采用：自主执行/自动雇佣（撞 LOCKED_ACTIONS） | 仍锁定；B 层闸引擎明确「不解除 A 层锁定」（`runtime_governance.py` 测试守卫） | **一致 + 收敛**：B 层把「不采用自主执行」精确收敛为「系统决定技术、用户决定高影响业务」 |
| 部分覆盖：幂等/去重/恢复 cooldown | P0-4 部分（防重入✅、Wake 相关❌依赖 P0-2） | **一致** |
| 缺口：Goal Alignment / Budget | P2-2（Budget 硬停）未实现，与「缺口」判断一致 | **一致** |
| B 层治理增量（本次新增上下文） | `581ed7d6` 撰写时 B 层治理**尚未落地**；本次核对确认其已 commit（`67a21aa4`+`e1d0b78e`+`0750026c`）——这是 `581ed7d6` 之后**新增**的进度，非矛盾 | **演进一致**：本次报告在 `581ed7d6` 基础上补入 B 层已落地事实，并据此把 P1-1 后端判为 done |

> 一致性结论：本次差距分析**不推翻** `581ed7d6` 的任何判断，仅（1）补入 B 层治理已落地的演进事实；（2）把「研究结论精炼版」的 P0/P1/P2 逐项落到代码实测，给出更细的 已实现/部分/未实现/正确规避 判定。

---

## 6. 结论速览（给主理人 齐活林）

> 本团队边界：**仅后端 / 不越 Workspace UI**；本报告**仅分析、未写实现代码**。

**核心结论条目（模式对比 2 + P0-1~P2-2 共 9 = 11 项）**
- ✅ 已实现：**0 项**
- 🟡 部分：**5 项** —— 模式对比·真实运行、模式对比·管理控制、P0-1（单任务领取存在/无通用 ExecutionClaim）、P0-4（防重入+脱敏有/Wake 相关无）、P1-1（后端 done / 前端 pending）
- 🔴 未实现：**5 项** —— P0-2（Wake/Session）、P0-3（配置指纹）、P1-2（运行时间线）、P1-3（组织图）、P2-2（内部预算硬停）
- 🛡️ 正确规避：**1 项** —— P2-1（插件 Capability 权限模型，冻结未做）

**不建议复用 7 条（N1–N7）**：全部 **正确规避**（heartbeat / 全量 migration / Agent 运维 Dashboard / PG-Drizzle / 品牌资产 / 公开服务器多租户 / MIT 版权保留）。

**规划席建议 2 Issue（I-A / I-B）**：**未落地（建议）**——Issue A 通用 Agent Execution Kernel、Issue B CEO Office 真实运行证据；另补 Issue C 内部预算硬停（P2-2）。

**一句话给总控**：Curis 在「真实运行闭环 + 后端可插拔 + B 层治理闸（含待决策持久化）」上已实质领先 Paperclip 的同层能力；P0 缺口集中在**通用执行内核（Wake/Session/Claim/配置指纹）**——建议以 Issue A 后端一次性补齐，CEO 决策中心 UI（P1-1 前端 / P1-2 / P1-3）归 Workspace 前端团队接后端数据层（Issue B）。
