# CURIS AUTONOMOUS BUSINESS OPERATION
## CODEX × WORKBUDDY CROSS-TRACK SYNTHESIS
## ONE OPERATING LIFECYCLE CONTRACT CANDIDATE

**Authority Class:** REVIEW  
**Status:** Frozen  
**Disposition:** CEO ACCEPTED — APPROVED CANDIDATE / NOT IMPLEMENTED  
**Date:** 2026-08-20  
**Scope:** Product / Runtime semantics reconciliation; no implementation authorization  

> 本文是两条已完成研究轨道的交叉裁决，不是第三套研究，也不是 Current Product Authority。它不修改 Product Blueprint、Master Map、UI Blueprint、Frozen Shell、Runtime、Schema、数据库、代码或 Prototype。

## 1. 输入与裁决纪律

| 输入 | Authority Class | 本轮用途 |
|---|---|---|
| `docs/research/CURIS_AUTONOMOUS_OPERATION_CODEX_RESEARCH.md` | RESEARCH / Review | 复用现有 Runtime、幂等、重启、证据链与实现边界审计 |
| `docs/research/CURIS_AUTONOMOUS_OPERATION_WORKBUDDY_RESEARCH.md` | RESEARCH / Review | 复用经营责任、Leader、Strategy/Team Operating 分层与 CEO 体验判断 |
| `docs/01_Product/Curis_Product_Blueprint.html` | CURRENT / FROZEN | 检查候选合同不能覆盖的产品边界 |
| `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_AUTHORITY_REVIEW.md` | REVIEW / Frozen / CEO Accepted | 约束 Operating Scope 必须使用 canonical Business/Workspace 身份 |

裁决规则：研究可以解释为什么，但不能因为研究结论自动改写 Current；冲突不以平均折中处理，而是记录采用哪一侧、保留哪一侧的有效语义，以及需要 CEO 决定的地方。

## 2. CROSS-TRACK MATRIX

标记含义：**AGREE** 两轨核心一致；**COMPLEMENTARY** 关注层不同但可叠加；**CONFLICT** 表面或真实冲突，已裁决；**ONE-SIDED** 只有一轨提出，不能默认为 Current；**DEFER** 需要实际域/Runtime证据后再定。

| 主题 | Codex 研究 | WorkBuddy 研究 | 裁决标记 | Curis 候选结论 |
|---|---|---|---|---|
| Autonomous Operation 定义 | Company OS 上的薄 Control Plane，负责有界 Cycle 的唤醒、复盘、下一轮 | 从 Task 提升为长期经营责任，持续判断下一步 | COMPLEMENTARY | 产品语义是长期经营；Runtime 只提供有界、可恢复的生命周期控制 |
| Operating Responsibility | 既有 Assignment/Holder/Scope 可复用 | Leader 长期持有结果责任 | AGREE | Responsibility 是长期责任引用，不新建第二套 Employee/Task |
| Leader 职责 | 负责编排、Review、Decision；不执行底层工具 | Sense、Research、Strategy、Plan、监督、复盘、学习、调整、下一轮、升级 | COMPLEMENTARY | Leader 是长生命周期经营 Owner；职责跨 Cycle，但执行复用 Team Operating |
| Leader 不是 | 不是 Router/Executor/Workflow Node/CEO 替代品 | 同左 | AGREE | 直接进入产品语言和授权边界 |
| Intent | Scope ref，CEO拥有，Cycle pin | CEO提供意图与约束，系统补全经营方案 | COMPLEMENTARY | Intent 是入口与范围依据，不是自由文本 Task；最终由 CEO 确认 Goal/边界 |
| Goal | 版本化、Cycle pin、显式达成/终止 | CEO 定义结果，Leader不能改变成功定义 | AGREE | Goal 是 CEO锚点；改 Goal 必须显式 Decision Gate |
| Strategy | 版本化，变更需证据、预期效果、Review窗口 | Why/How win/本轮验证；慢循环、CEO可触达 | AGREE | Strategy 与 Team Operating 分离；策略变更有版本与门禁 |
| Plan | Cycle 内有界、不可变释放版本，映射 Work | 把策略落成执行计划 | COMPLEMENTARY | Plan 是 Cycle 输入，释放后由既有 Work/Assignment 执行 |
| Operating Cycle | 复用现有 CYCLE；每轮必须 terminal | 经营默认 CONTINUE/ADJUST | CONFLICT | Product: Responsibility 默认持续；Runtime: 每 Cycle bounded terminal；连续性只能由显式 Next-cycle Decision 建立 |
| Team Operating 关系 | 既有 Workspace-scoped Responsibility Routing / Employee execution | 团队如何把 Work 做出来 | AGREE | Lifecycle 在上层编排，不吞并 Team Operating |
| Result / Evidence | 既有 Result/Evidence/Receipt，要求 provenance/freshness | 结果是经营责任复盘的输入 | AGREE | 只接受可追溯结果；不以产出数量代替业务结果 |
| Signal | 从 Result/Evidence 派生，若参与决策需持久化公式/窗口/来源 | 外部数据和趋势用于发现机会 | COMPLEMENTARY | Signal 是可重算或已固化的指标事实，不是模型意见 |
| Review | Evidence→Signal→Interpretation→授权 Review | 复盘是 Leader责任 | AGREE | Review 必须有证据充分性、来源、不确定性与责任人 |
| Learning | 仅接受 Learning，追加、适用范围/置信度/失效期 | 学习账本沉淀有效/无效模式 | AGREE | AI summary ≠ Learning；接受 Learning 才能改变 Strategy/Plan |
| Next Cycle | 六种 durable decision，原子创建或等待 | 默认 CONTINUE/ADJUST | COMPLEMENTARY | 六种动作统一为显式 Decision；CONTINUE 也不能隐式续命 |
| Trigger | Result-driven / Scheduled / Leader-CEO initiated；通用事件 deferred | Cadence / Result / External Signal / Leader / CEO | CONFLICT | V1 只收三类入口；External generic event 需 Domain Adapter；threshold 先是 Review Signal，不直接执行 |
| CEO Decision | Goal/Strategy/risk/high-impact gate | 最小高杠杆触点，低风险不打扰 | AGREE | CEO 管方向与不可逆，高频战术由 Leader 处理 |
| Autonomy | policy / permission / budget / risk gate | tunable autonomy / trust gradient | COMPLEMENTARY | V1 使用静态 AUTO/AUTO WITH AUDIT/CEO GATE/FORBIDDEN；信任梯度是后续可验证演进，不自动升级 |
| Context / Token | reference-first，目标1,750–4,500，p95<6,000 | 对CEO隐藏内部生命周期，渐进披露 | COMPLEMENTARY | Runtime 使用精简 typed Context；产品只呈现简报、事项、决定与恢复，不暴露控制台 |
| Failure / Recovery | Provider、权限、重复回调、重启、迟到数据、CEO silence等有界恢复 | 失败应回到负责人/CEO而非静默结束 | AGREE | 失败保留责任、原因、下一步与返回入口；不伪造成功，不创建旁路流程 |
| Stop / Pause / Wait | durable distinct states | STOP是例外，经营默认继续 | CONFLICT | Product continuity≠永远运行；WAIT/PAUSE/STOP分别记录原因、恢复/终止条件 |
| V1 Scope | Workspace-scoped，Business聚合但不做 Business provider execution | 单域内容/小红书优先，单业务并发 | COMPLEMENTARY | 首个可证明闭环是已配置 Workspace；RD 与 XHS 做同一生命周期域验证，不能泛化全行业 |
| Domain validation | XHS + RD；不伪造 Analytics | XHS压力测试、RD跨域、客服反例 | COMPLEMENTARY | XHS/RD为首批证明；客服/事件驱动作为反例验证触发和升级，不纳入V1承诺 |
| Runtime reuse | 明确不新建 Task/Workflow/Employee/Result Runtime | 经营OS是Leader/Strategy层 | AGREE | 只增加生命周期控制职责：trigger claim、single active、snapshot、review、atomic continuation |

### 2.1 真实冲突与最终裁决

1. **Continue vs Cycle terminal：** 不是二选一。长期 Responsibility 默认继续；每一 Cycle 必须关闭；只有 CONTINUE/ADJUST 等显式 Decision 才能生成下一 Cycle。
2. **主动循环 vs 事件循环：** V1 用 Result、Schedule、Leader/CEO 三入口；外部通用事件不是默认 Trigger。客服研究显示事件驱动是有效反例，未来由 Domain Adapter 证明后再纳入。
3. **增长语言 vs 业务无关模型：** “增长”只属于内容域。通用不变量是向 Goal 持续改善；RD 的结果是产品可用性/交付质量，客服可是质量/成本。
4. **隐藏生命周期 vs 可审计：** CEO 默认看不到内部状态机，但展开事项、结果、决定、异常时必须可追溯；隐藏是渐进披露，不是删除事实。

## 3. 共同核心（冻结为候选合同）

### 3.1 Autonomous Operation ≠ Task Automation

Task 做完即结束；Team Operating 解决一轮 Work 如何完成；Autonomous Business Operation 则由 Leader 长期持有经营责任，基于结果和证据判断下一步。自动化吞吐量不能证明业务方向正确。

### 3.2 Leader 是 Long-lived Operating Owner

Leader 持续承担 Sense / Research / Diagnosis / Strategy / Plan / Execution supervision / Result Review / Learning / Adjustment / Next Cycle / Escalation。它不是 Router、Workflow 节点、所有工作的 Executor，也不是 CEO 替代品。Leader可以调度现有 Employee 与能力，但不能改 Goal 或成功标准。

### 3.3 Strategy 与 Team Operating 严格分层

Strategy 回答“为什么做、如何赢、这一轮验证什么”；Team Operating 回答“谁用什么能力、按什么责任和节奏把 Work 做出来”。Team Operating 可以高度自动，但不能替代策略复盘。策略层是较慢且有 Gate 的循环，执行层是较快且可自治的循环。

### 3.4 Operating Lifecycle 是薄 Control Plane

产品层：CEO Intent/Goal → Operating Responsibility → Strategy/Plan → 有界 Cycle → Result/Evidence → Review/Learning → Next-cycle Decision。  
实现层：继续复用 Company/Department/Business/Workspace canonical identity、Assignment/Router、Employee、Provider Task/Session、Result、Evidence、Decision、Handoff、既有 Recovery。

Lifecycle Controller 的最小新增责任仅为：稳定 Trigger intake/claim、单一 active Cycle、Situation Snapshot、Plan release、Review/Next-cycle Decision、原子 continuation。它不拥有 Tool、Provider、Employee、Result、Organization 创建。

## 4. Curis 不能丢的价值

- CEO 的少量高杠杆决策，而不是把 CEO 变成每步审批员。
- 经营目标、策略、责任、能力、结果和外部反馈之间的连续关系。
- 真实 Result/Evidence、来源、时效、未知与人工回填，不把 AI 自报当事实。
- 失败时责任连续：Owner、缺口、下一步、返回原阶段、有限重试/升级。
- 组织和 Workspace 复用 Company Truth；Operating Lifecycle 不能创建第二套组织或业务身份。
- 业务差异由 Domain Workspace 表达；同一 Lifecycle 骨架可以同时承载 XHS 内容增长与 RD 产品开发。

## 5. 现阶段实现边界（只登记，不授权代码）

Codex 研究确认的可复用底座包括 Workspace-scoped Responsibility Routing、真实 Employee execution、Result Contract、immutable definition、reference-first Context、restart/cancel/loop guard、Handoff/Decision/Result recovery。当前闭环仍缺：Durable Cycle Controller、Evidence-bound Review/Learning quality gate、atomic next-cycle continuation、可靠 trigger scanner/claim、XHS/RD 同一生命周期的正式 integration acceptance。

Canonical Business Spine 已获 CEO 接受并授权实现；Operating Lifecycle 候选合同必须使用其 Business/Workspace identity，不能用 free-form `business_ref`。实现顺序和 Stop Gate 由 Canonical Business Spine Issue 管理，本文件不解除其门禁。

## 6. 最终候选产品宣称

> 在一个已经配置并授权的 Workspace 中，AI Leader 可以围绕一个持久 Goal 和 Strategy，自主启动有界经营周期，调度真实 AI Employees 完成工作，根据可验证 Result / Evidence 进行复盘，并在授权范围内决定继续、调整、等待或升级，从而持续进入下一经营周期。

这不代表：任何行业都能全自动经营；AI可以修改Goal/成功标准；无限花费/发布/签约/部署；无需CEO监督；或 Business-scope Provider Execution 已完成。

## 7. CEO Accepted Contract Deltas

### 7.1 Strategy Adjustment Authority

Leader 只在 **Approved Strategy Envelope** 内自主调整：hypothesis、tactic、cadence、experiment、resource allocation、Work priority、content/execution mix 与 bounded Plan。必须同时满足：不改变 Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget 或 high-impact / irreversible external commitment；且有 Evaluation Contract 允许并有 Evidence / Review 支撑。

以下变化必须进入 CEO Gate：Goal、Success Contract、Positioning、Target Audience、Business Model / Monetization Model、protected Strategy Boundary、material Budget、高影响或不可逆外部承诺。`ADJUST` 不等于 Leader 可以修改任意 Strategy。

### 7.2 Cycle Close、PAUSE、STOP 分离

- **Cycle Close**：每个 bounded Cycle 的正常 terminal；不表示 Business、Workspace 或 Operating Responsibility 停止。
- **PAUSE**：暂停 Operating Series，保留 Goal、Strategy、Responsibility、History，需要显式 Resume。
- **STOP**：终止 Operating Responsibility / Goal Series，只能由 CEO 或事先明确授权的 terminal policy 触发。

一次没有 Work、一次失败、一次 Review 或一次 Cycle terminal，都不能自动 STOP 整个经营责任。

### 7.3 V1 Domain Proof Levels

- **Primary Autonomous E2E Domain**：至少一个真实 Domain 连续 ≥2 个 Operating Cycles，闭合 Goal → Strategy → Plan → Team Operating → real Employee execution → Result / Evidence → Review → accepted Learning → CONTINUE / ADJUST → next Cycle → second Result，并验证 restart、duplicate trigger、late result、WAIT / ESCALATE 与 CEO Gate。
- **Cross-domain Contract Proof**：第二个 Domain 证明同一 Lifecycle 可承载不同 Strategy semantics、Team Operating、Result Contract、Signal、Evaluation Contract 与 risk gate。可使用真实 Runtime + controlled/replay evidence，但不得用 fake Result、fake Analytics 或 static UI 冒充 Autonomous E2E。

### 7.4 Accepted status boundary

本综合与 `CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md` 现为 CEO Accepted / Approved Candidate；这不是 Current Product Truth 的实现证明，不是 Runtime Accepted，也不代表自主经营已完成。后续消费必须经过正式 Product → Runtime → UI → Code Issue。

## 8. CEO Review 必须裁决（已完成）

1. 已接受“长期经营语义 + bounded Cycle Runtime”的双层裁决。
2. 已接受 V1 三类 Trigger，以及将 generic external event 留给 Domain Adapter。
3. 已接受 Leader 的 Approved Strategy Envelope 与 CEO 高杠杆 Gate 边界。
4. 已接受 XHS + RD 作为首批两域证明，并区分 Primary Autonomous E2E 与 Cross-domain Contract Proof。
5. 已接受第二份合同中的状态、字段和证据门禁进入后续 Product→Runtime→UI 流程；本轮不自动消费实现。

## 8. 明确停止状态

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
