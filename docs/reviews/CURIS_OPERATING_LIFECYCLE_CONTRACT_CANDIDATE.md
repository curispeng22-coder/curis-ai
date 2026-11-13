# CURIS OPERATING LIFECYCLE CONTRACT CANDIDATE

**Authority Class:** REVIEW  
**Status:** Frozen  
**Disposition:** CEO ACCEPTED / APPROVED CANDIDATE — NOT IMPLEMENTED / NOT RUNTIME ACCEPTED  
**Date:** 2026-08-20  
**Source:** `CURIS_AUTONOMOUS_BUSINESS_OPERATION_SYNTHESIS.md` + Codex / WorkBuddy research  
**Implementation:** Not authorized by this document

> CEO 已接受本合同作为 Product Authority 的 Operating Lifecycle approved candidate。它把产品语义、运行语义、证据门禁和失败恢复写在同一张契约里，供后续 Product → Runtime → UI → Code 使用；它不代表 Runtime 已实现或被 Runtime Acceptance 接受，也不新增 Runtime Primitive，不覆盖 Frozen Product Truth。

## 1. Contract invariants

1. **Product responsibility is continuous.** 一个已接受的 Operating Responsibility 默认继续，直到 Goal 终止或显式 PAUSE / STOP。
2. **Every runtime Cycle is bounded.** 每个 Cycle 必须有起点、范围、结果/证据和终止结论；禁止 `while(true)`、永久 Agent Session 或永不结束的 Cycle。
3. **Continuation is explicit.** CONTINUE / ADJUST 才能创建或安排 exactly one next Cycle；沉默不是继续授权。
4. **One active Cycle.** 同一 Workspace Operating Scope 同时最多一个 active Cycle；重复 Trigger 只合并，不复制执行。
5. **Pinned truth.** Cycle 固定 Goal、Strategy、Plan、Operating Definition 版本；新版本默认影响下一 Cycle，实时撤销/权限失效除外。
6. **Existing execution is reused.** Work、Assignment、Responsibility Router、Provider Task/Session、Employee、Result、Evidence、Decision、Handoff 和已有 Recovery 继续承担执行。
7. **Evidence precedes learning.** 没有满足 Evaluation Contract 的 Result/Evidence，只能 CONTINUE（若计划允许）、WAIT 或 ESCALATE，不能自主 ADJUST Strategy。
8. **Approved Strategy Envelope.** Leader 只能在已批准 Strategy Boundary 内自主调整 hypothesis、tactic、cadence、experiment、resource allocation、Work priority、content/execution mix 与 bounded Plan；不得改变 Goal、Success Contract、Positioning、Target Audience、Business/Monetization Model、protected Strategy Boundary、material Budget 或 high-impact / irreversible external commitment。
9. **Scope is canonical.** Operating Scope 只能解析到已有 Company/Department/Business/Workspace canonical identity；不得用 free-form `business_ref` 建第二套关系。

## 2. Product mental model vs Runtime state

### 2.1 产品心智（CEO 可理解）

```text
经营意图
→ 目标与边界
→ 负责人提出策略
→ 本轮计划
→ 团队工作
→ 真实结果
→ 复盘与学习
→ 下一步决定
→ 继续 / 调整 / 等待 / 升级 / 暂停 / 停止
```

Sense、Research、Diagnosis 是 Strategy 前的子动作；Execution/Result 使用既有 Team Operating 与结果体系；Next Cycle 是 Decision 的去向，不是第八个常驻页面。

### 2.2 Runtime 最小阶段

| 阶段 | 进入条件 | 退出条件 | 主要责任 |
|---|---|---|---|
| `TRIGGER_CLAIMED` | Trigger 有稳定 key、scope 未暂停/停止 | claim 成功或被合并 | 领取、去重、权限/预算预检 |
| `CYCLE_STARTED` | 没有其他 active Cycle | Goal/Strategy/Operating Definition 已 pin | 建立 bounded boundary |
| `SENSED` | 当前 Truth refs 与 freshness 已读取 | Situation Snapshot 固化 | 只保留引用和摘要，不吞入全历史 |
| `PLANNED` | Plan、Result Contract、预算、Review 条件已明确 | Plan release 或等待补缺口 | Leader 负责计划；CEO Gate 只在授权范围要求时出现 |
| `OPERATING` | Plan 已释放到既有 Work/Assignment | Work terminal、失败、等待或取消 | 复用 Team Operating/Employee execution |
| `REVIEWING` | 必需 Result terminal，或明确记录 late/missing | Review 完成 | Evidence→Signal→Interpretation→Review |
| `DECIDING` | Review 有足够证据或明确不确定性 | Decision 已应用且当前边界关闭 | 形成 Next-cycle Decision |
| `WAITING` | WAIT/ESCALATE/人工决定/外部数据待回 | nextCheckAt、回调或 CEO/Leader 输入 | durable wait，不从进程内存恢复 |
| `PAUSED` | PAUSE 已授权 | 显式 resume 或 STOP | 无自动唤醒 |
| `STOPPED` | STOP、Goal 达成或不可逆终止 | 只读历史；新 Goal 需新授权 | 保留所有 Result/Evidence/Learning |

这些是候选 Runtime 语义，不等于要求创建同名表、页面或新状态枚举；实现应优先映射现有 CYCLE/transition/audit 机制。

**Cycle Close ≠ Operating Stop：** Cycle Close 是每个 bounded Cycle 的正常 terminal，不代表 Business、Workspace 或 Operating Responsibility 停止。`PAUSE` 暂停 Operating Series，保留 Goal、Strategy、Responsibility、History，并要求显式 Resume；`STOP` 终止当前 Operating Responsibility / Goal Series，只能由 CEO 或事先明确授权的 terminal policy 触发。一次没有 Work、一次失败、一次 Review 或一次 Cycle terminal 都不得自动 STOP 整个经营责任。

## 3. Canonical truth classification

分类含义：A = 已有 canonical object；B = 已有对象增加字段/引用；C = scope/Cycle 内版本化真相；D = 可重算派生投影；E = 临时 AI 推理；F = 后续研究/非 V1。

| 概念 | 分类 | 是否持久化 | 权威 Owner | 候选承载 | 纪律 |
|---|---|---|---|---|---|
| Operating Responsibility | A | 是，复用 Assignment/Holder | scoped Leader/Assignment | Employee×Role×Scope reference | Holder ≠ Executor；交接写入日志 |
| Intent | B/C | 是，版本或 scope ref | CEO | Company/Business/Workspace intent ref | Cycle pin；不建自由文本 Task |
| Goal | B/C | 是，版本化 | CEO / 受授权 Leader | Product Truth + Cycle goal ref | 达成/替代/停止显式记录 |
| Strategy | C | 是，紧凑版本化 | Leader；受保护变更由 CEO | Business/Workspace Strategy + Cycle ref | 调整必须有证据、预期效果、窗口 |
| Situation Snapshot | B/C | 是，按 Cycle | Lifecycle Controller | Cycle child data/ref | 摘要+source/freshness；不存全会话 |
| Operating Plan | B/C | 释放版本持久化 | Leader | Cycle plan/ref → Work/Assignment | 释放后不可静默变更 |
| Operating Cycle | A | 是，复用现有 CYCLE | scoped Leader | 既有 CYCLE | bounded、terminal、single active |
| Result | A | 是 | producing Assignment / acceptance owner | Result/Artifact/Outcome | 生产者不可单独接受受保护结果 |
| Evidence | A | 是 | source owner / verifier | Evidence/Receipt | scope、来源、时效、验证状态 |
| Signal | D，决策使用时 B | 通常派生；使用时固化 | 系统派生，来源 owner 不变 | Review 内 material signal | formula/window/baseline/source 必须可追 |
| Interpretation | E → Review field | 仅 Review 前后按需保留 | Leader/Reviewer | Review 字段 | 不接受的推理不能改策略 |
| Review | B/C | 是 | scoped Leader；保护指标需独立 reviewer | Cycle review/ref | 证据覆盖与不确定性审计 |
| Learning | C | 仅 accepted learning | Leader；Company policy 需 CEO | Review accepted learning/artifact | append-only、适用范围/置信度/失效期 |
| Next-cycle Decision | B/C | 是 | Leader 或 CEO，按 autonomy policy | Decision/Decision Packet/Cycle event | 动作、证据、owner、nextCheckAt、前后 Cycle refs |
| Operating Control State | B/D | 必要字段/派生 | Lifecycle Controller | scope projection + Cycle | 不默认新实体；可由既有状态重算 |

> 概念存在不等于建表。只有改变执行、审计、幂等或后续判断的事实才需要持久化；页面、报表和 Assistant 只是 projection。

## 4. Operating Cycle contract

### 4.1 Start

一个 Cycle 只能由三类 V1 Trigger 进入：

1. **Result-driven**：accepted Result 产生稳定 trigger key，唤醒 Review/下一轮；重复 Result 不重复创建。
2. **Scheduled review**：`nextCheckAt` 到期，检查迟到数据、卡住工作或复盘节奏；它不是永久 Agent loop。
3. **Leader / CEO initiated**：新 Goal、显式 resume、紧急调整或人工决定，必须复用同一 claim/authority path。

Trigger 是进入检查的邀请，不是绕过 Scope、Permission、Budget 或 CEO Gate 的授权。generic external event 暂不作为通用 V1 规则引擎；threshold 在 V1 先分类 Signal，不直接启动执行。

### 4.2 Plan release

Leader 基于当前 Goal/Strategy、Situation Snapshot、accepted Learning 与适用 Signals 生成 bounded Plan。Plan 至少说明：责任、交付、Result Contract、预算/权限、Review 条件、风险与回退。Plan release 后使用现有 Work/Assignment；Lifecycle Controller 不直接调用 Provider 或 Tool。

### 4.3 Review and learning

```text
Result / Evidence
→ Signal（来源、公式、窗口、基线、样本、不确定性）
→ Interpretation（假设、替代解释、混杂因素）
→ Authorized Review
→ accepted / rejected Learning
→ Strategy / Plan version change
```

AI 的自我总结不等于 Learning。接受 Learning 至少需要：Evidence refs、Scope、观察窗口、适用范围、置信度/不确定性、授权 Reviewer、可证伪条件；不得静默覆盖旧学习。

### 4.4 Evaluation Contract

每个 Goal/Strategy 版本必须可引用 Evaluation Contract：

- outcome metric 与允许的 proxy；
- source authority、独立验证要求；
- observation window、freshness；
- minimum sample / independent windows；
- baseline、comparison、可比性；
- materiality threshold、confounders；
- adjustment cooldown；
- 风险/不可逆条件及 CEO Gate；
- budget、permission、external commitment limits；
- 成功、失败、数据不足、需复核的阈值。

没有 Evaluation Contract，可以执行已批准 Plan 并报告 Result，但不能声称 Strategy 有效，也不能静默修改 Strategy。

## 5. Next-cycle Decision contract

| Decision | 谁能决定 | 最低证据/理由 | 当前 Cycle | 下一步 | nextCheckAt / Packet |
|---|---|---|---|---|---|
| `CONTINUE` | Leader；受保护范围可需 CEO | 结果达到继续条件，或策略未需改变 | 关闭为 completed/reviewed | 同 Strategy/Plan lineage 创建 exactly one next Cycle | 可选 cadence；记录 Decision Packet/ref |
| `ADJUST` | Leader 仅在 Approved Strategy Envelope 内；越界需 CEO | Evidence→Signal→Review，明确 changed assumption、预期效果、窗口 | 关闭并固化变更 | 新 Strategy/Plan version + exactly one next Cycle | 写新 review window；必须 Packet |
| `WAIT` | Leader / system policy；高风险需 CEO | 数据不足、外部依赖、Review未可用、待回执 | 关闭当前运行边界为 waiting | 不创建 active Cycle | 必须 nextCheckAt 或明确事件；Packet 可选/按策略 |
| `ESCALATE` | Leader 触发；CEO/授权代理决定 | 超权限、风险、冲突、连续失败、CEO gate | 进入 waiting decision | 不创建未批准的下一 Cycle | Packet 必须；提醒/升级 cadence |
| `PAUSE` | CEO 或被授权 Leader | 明确暂停范围/理由/恢复条件 | 关闭当前执行并保留历史 | 不自动唤醒 | 无 nextCheckAt，显式 resume 才可 |
| `STOP` | CEO，或事先明确授权的 terminal policy | 成功合同达成、不可逆终止、风险无法接受 | 终止 Operating Responsibility / Goal Series | 不创建新 Goal/Cycle | immutable decision；Packet/审计必存 |

每种 Decision 都必须记录：actor、authority policy、evidence refs、reason、current Cycle close result、next Cycle/scope ref、nextCheckAt、idempotency key。崩溃或重启后读取已应用 Decision；若 next Cycle 还未创建，使用 deterministic successor key create-or-read，绝不重复执行。

## 6. Autonomy and CEO boundary

### 6.1 Responsibility split

| 决策层 | CEO | Leader |
|---|---|---|
| Goal / Direction | 定义、修改、终止 | 解释和分解，不改成功定义 |
| Strategy | Strategy Gate、保护性变更 | 仅在 Approved Strategy Envelope 内提出/执行调整 |
| 日常 Plan / Staffing | 仅高风险或超预算 | 自主配置既有 Employee/Capability |
| 普通执行 | 不逐步批准 | 按 policy 自治 |
| Result Review | 关键/高影响结果 | 负责日常复盘与证据准备 |
| Risk / external side effect | 高影响、不可逆、触钱/法/品牌/客户 | 低风险政策内动作 |
| Pause/Stop | 保护性暂停/终止 | 在授权范围触发并上报 |

### 6.2 Four policy levels

| Level | 允许 | 典型例子 |
|---|---|---|
| `AUTO` | 低风险、可逆、权限内，无需即时人审 | 已批准策略内研究、草稿生成、内部整理 |
| `AUTO_WITH_AUDIT` | 可自动执行，但必须留下完整证据和结果 | 已授权账号内的低风险发布/同步（具体由 Domain contract 定义） |
| `CEO_GATE` | 先形成 Decision Packet，再等 CEO | 改定位/Goal、花费预算、公开发布、外部承诺、品牌/法律风险 |
| `FORBIDDEN` | 当前能力或权限禁止 | 读不到授权数据、绕过撤销、秘密/越权、无限循环 |

V1 先使用静态 policy；“信任梯度”只是后续研究方向，不允许系统仅凭审批历史自发升级自治级别。

### 6.3 Strategy Adjustment Boundary

**Leader 可自主调整（仅限 Approved Strategy Envelope）：** hypothesis、tactic、cadence、experiment、resource allocation、Work priority、content mix / execution mix、bounded Plan。前提是 Goal、Success Contract、Positioning、Target Audience、Business/Monetization Model、protected Strategy Boundary、material Budget 与 high-impact / irreversible external commitment 均不改变，并且 Evaluation Contract 允许、已有 Evidence / Review 支撑。

**必须 CEO Gate：** Goal、Success Contract、Positioning、Target Audience、Business Model / Monetization Model、protected Strategy Boundary、material Budget，以及任何 high-impact / irreversible external commitment 的改变。`ADJUST` 不是 Leader 修改任意 Strategy 的通行证。

## 7. Context contract

每次 Leader/Employee 调用收到 typed、reference-first、summary-first 的 Cycle Context：scope/cycle refs、pinned Goal/Strategy/Plan、适用 Learning、Signals、Result/Decision metadata、retrieval hints。默认目标 **1,750–4,500 tokens，p95 < 6,000**，作为后续 Acceptance Target 而不是 Current Product Truth。

禁止默认携带完整历史 Conversation、全部 Cycle、Evidence body、所有 Employee session、raw Provider traces、过期 Strategy/Plan。需要时按 Input Contract traceable retrieve-on-demand；上下文增长应为 O(1)，历史 metadata 在外部可查询。

## 8. Failure and recovery contract

| 失败 | 保留什么 | 系统动作 | CEO/Leader恢复 |
|---|---|---|---|
| Provider / Capability 缺失 | Cycle、Owner、缺口、无 Result | bounded retry或 WAIT；不伪造 Executor | 能力中心/供给修复后从原 Stage 返回 |
| Result Contract / provenance 失败 | 原 Work/Failure、原始证据 | Return/Review/WAIT；不推进下一轮 | 修复输出契约或重新绑定负责人 |
| Leader crash / Runtime restart | pinned refs、claim、Work keys | lease 过期后 reclaim；恢复当前 Cycle | 无需重建；不以新 Cycle 隐藏状态 |
| Late data / duplicate callback | 原 Review、来源、时间 | WAIT或补充 amendment；相同回调幂等，冲突 fail-closed | Review 重新评估，但不覆盖旧事实 |
| CEO silence / Review unavailable | Decision Packet、提醒节奏 | WAITING_DECISION；不默认放行高风险 | CEO/授权代理决定，或明确 expiry policy |
| Repeated strategy failure / no new data | failed windows、unknown、学习候选 | ESCALATE/PAUSE/WAIT，不反复改策略 | CEO修 Goal/Strategy/资源或停止 |
| Permission revoked / budget exhausted | 撤销/消耗证据、历史结果 | 立即 fail-closed，停止新 Work | 重新授权、缩小范围、PAUSE/STOP |
| Goal achieved | 成功合同、guardrail、Evidence | STOP 当前 series；不隐式创建新 Goal | CEO/Policy确认后另起新的经营责任 |
| Trigger storm | 所有 trigger refs | 一个 scope claim 合并同类 trigger | 按优先级一次 Review，冲突交 CEO |

## 9. Bootstrap Plane vs Operating Plane

### Bootstrap Plane

```text
CEO Intent
→ Research / Strategy proposal
→ CEO Strategy Gate
→ Company OS 结构方案
→ Department / Business / Workspace / Leader / Team 创建或复用
```

Bootstrap 负责建立可经营的 canonical identity 与最小责任承载；它不被 Operating Lifecycle Controller 接管，也不允许 Lifecycle 自己创建组织。

### Operating Plane

```text
已建立 Business / Workspace
→ Operating Responsibility
→ bounded Cycle
→ Team Operating / Employee execution
→ Result / Evidence
→ Review / Learning
→ Next-cycle Decision
```

Product Operating Scope 可以在 Business 层聚合 Goal/Strategy/Result；V1 Runtime Execution Scope 先限定 Workspace。Business-scope Provider Execution 未实现时必须显示真实缺口，不能以 Business 页面存在冒充执行可用。

## 10. Domain proof and V1 claim

### 10.1 首批证明

- **XHS / 内容增长：** Result 是发布/回执/互动/外部指标，Strategy 是定位、内容假设和节奏；需要明确手动回填与外部来源新鲜度。
- **RD / 产品研发：** Result 是 build/test/review/可用性证据，Strategy 是产品方向/优先级/能力交付；不能把“多写代码”当产品成功。
- **客服/事件驱动：** 作为未来 adversarial validation，验证 event pull、steady-state ESCALATE 和公开风险，不作为 V1 泛化承诺。

### 10.1.1 Domain proof levels

- **Primary Autonomous E2E Domain：** 至少一个真实 Domain 连续完成 ≥2 个 Operating Cycles：Goal → Strategy → Plan → Team Operating → real Employee execution → Result / Evidence → Review → accepted Learning → CONTINUE / ADJUST → next Cycle → second Result，并验证 restart、duplicate trigger、late result、WAIT / ESCALATE 与 CEO Gate。
- **Cross-domain Contract Proof：** 第二个 Domain 证明同一 Lifecycle 可以驱动不同 Strategy semantics、Team Operating、Result Contract、Signal、Evaluation Contract 和 risk gate。允许真实 Runtime + controlled/replay evidence，但不得用 fake Result、fake Analytics 或 static UI 冒充 Autonomous E2E，也不要求 V1 同时打穿全部外部 Connector。

### 10.2 V1 正确宣称

> 在一个已经配置并授权的 Workspace 中，AI Leader 可以围绕一个持久 Goal 和 Strategy，自主启动有界经营周期，调度真实 AI Employees 完成工作，根据可验证 Result / Evidence 进行复盘，并在授权范围内决定继续、调整、等待或升级，从而持续进入下一经营周期。

### 10.3 V1 MUST

- Intent 接收与 Goal 捕获；
- Leader 先研究并提出 Strategy options；
- CEO Strategy Gate 是首轮唯一强制高杠杆触点；
- 至少一轮真实自治 Cycle；
- Result/Evidence Review 与 accepted Learning；
- CONTINUE/ADJUST 的显式下一轮；
- CEO 风险/策略/不可逆 Gate；
- 失败、重启、重复触发、迟到数据、CEO silence 的可恢复事实；
- 至少一个 Primary Autonomous E2E Domain 的连续双 Cycle 证据，以及第二个 Domain 的 Cross-domain Contract Proof；XHS + RD 是首批候选，不得把两个静态/回放结果都写成 Autonomous E2E。

### 10.4 V1 MUST NOT

- 自主改 Goal 或成功标准；
- 无限 Agent/Workflow/while(true)；
- 多业务跨策略协同的泛化承诺；
- 未有权限/回执的自动发布、付款、部署、签约；
- 用 AI 自报或单一 proxy 证明策略有效；
- 用新增 Task/Workflow/Employee/Result/Analytics Runtime 绕过现有底座；
- 在 Business Provider Execution 未成立时伪造 Business-scope 执行；
- 以静态页面、单个 API 200 或测试通过宣称自主经营完成。

## 11. Acceptance gates for a future implementation Issue

实现前必须另有正式 Issue，至少锁定：

1. 首个 Execution Scope = Workspace 及其 canonical parent resolver；
2. Goal/Strategy/Plan 当前权威、版本、冻结和覆盖规则；
3. 现有 CYCLE transition 与 Team Operating 不回归；
4. Trigger claim/idempotency/restart 事务边界；
5. XHS 与 RD 各自 Evaluation Contract 和外部数据回退；
6. CEO autonomy policy、budget、permission、external side-effect gate；
7. Review/Learning 独立证据和不确定性规则；
8. isolated SQLite、restart、Browser/Desktop、duplicate/late callback、CEO silence、至少 100 次 replay 的证据门槛。

本候选合同不授权开始上述实现；Canonical Business Spine 的已授权实现仍按其独立 Issue/Stop Gate 执行。

## 12. STOP STATE

```text
CURIS AUTONOMOUS BUSINESS OPERATION
— CEO ACCEPTED
— OPERATING LIFECYCLE APPROVED CANDIDATE
— LEADER STRATEGY ENVELOPE DEFINED
— CYCLE CLOSE / PAUSE / STOP SEPARATED
— V1 DOMAIN PROOF LEVELS DEFINED
— PRODUCT AUTHORITY RECONCILED
— IMPLEMENTATION NOT YET AUTHORIZED
— STOP
```
