# Curis 产品文档与主线程指针

Status: Frozen
Authority Class: FROZEN / TRUTH ROUTER
Updated: 2026-10-30

## Agent Navigation

New agents first use the navigation-only [CURIS Current Entrypoint](CURIS_CURRENT_ENTRYPOINT.md), then follow this Pointer’s `Current Required Input`. This file remains the sole Product Truth router; the Entrypoint does not define or duplicate product truth.

## Current Required Input

这是新 Agent 唯一默认文档入口。只按任务类型读取下列最小链；本文件后续 Reference Ledger、Research、History 与 Deferred 条目均非默认必读，且不能覆盖这里的 Current route。

<!-- CURRENT_REQUIRED_INPUTS_START -->

Implementation navigation update 2026-10-30（最新）：Owner全权继续当前EXEC任务，SDK/DoH/Finder依赖进入同批收口，真实Agent0/4、最终候选/QA/Native/安装未接受。准确信息从CURRENT_STATE、当前Issue/TASK_START与原唯一看板读取；旧UNKNOWN保留已处置，旧source08不是当前交付。仅导航更新，不改变Product/Frozen Authority。

Implementation navigation update 2026-10-30：CEO已完成当前EXEC任务的UNKNOWN处置并批准隔离Chrome扩展、本轮最多4次既有Codex额度验收；具体范围与仍待通过的技术门见当前Issue/TASK_START和CURRENT_STATE。不将历史P0处置或新授权写成能力验收。

2026-10-30 当前新增P0调查门：首轮pytest收集在守卫介入前可能读取本地.env，是否实际读取UNKNOWN；独立QA已确认无法证明为否，原配置不动、不读秘密。所有产品动态测试/App/Agent/Provider/Browser暂停；批准范围纯文本源码编辑及仅自制假文件的guard安全核验可继续。待CEO明确处置＋独立QA验证产品导入前隔离后由Owner恢复。此前模型/Package10限定接受保留，不把本轮安装/源码进度当新接受。详见当前EXEC Issue与TaskStart.currentP0；原看板仍唯一入口。


Implementation navigation update 2026-10-29：CEO已授权[员工真实执行能力长任务](<../../issues/CURIS-V1-EMPLOYEE-EXECUTION-CAPABILITIES-20261029.md>)，复用现有Agent/Skill/Browser合同，沿CURRENT_STATE及原唯一看板连续开发/QA/Native验收；本轮新增费用上限5元，旧接受保留。下方旧UX暂停为该批结束时事实。仅导航更新，不改变Product/Frozen Authority。

Implementation navigation only: [本轮同版完整动线与匹配安装签收（限定Scope）](<../../artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_DELIVERY_ACCEPTANCE_01.json>)；实现现状仍从[CURRENT_STATE](CURRENT_STATE.md)与原唯一看板读取。功能迭代已暂停；获批8处缓存清理已完成，执行回证从CURRENT_STATE与原唯一看板读取。

### Product / Design

1. [Product Blueprint](../01_Product/Curis_Product_Blueprint.html)
2. [Product Master Map](../01_Product/Curis_Product_Master_Map.md)
3. [Product UI Blueprint](../01_Product/Curis_Product_UI_Blueprint.html)
4. [Pre-Design-Research Product Structure Baseline](../01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)
5. [Product Context](../01_Product/Curis_Product_Context.md)
6. [CURIS V1 Product Freeze](../reviews/CURIS_V1_PRODUCT_FREEZE.md) — CEO-frozen V1 scope and the sole Final UI Master input set.
7. [CURIS V1 Final UI Acceptance Backlog](../reviews/CURIS_V1_FINAL_UI_ACCEPTANCE_BACKLOG.md) — the single UI acceptance list for Final UI Master.
8. 适用的 Current / Frozen shared authority：
   - [Company OS Shared Authority](../03_Design/Curis_Company_OS_Shared_Authority.md) — §10–18正式共享产品合同：能力/模型、Human Handoff、Browser、Background、Execution Recovery、工具、Backup、Settings；早期Candidate不整篇升级。
   - [Workspace Shell Contract](../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md) — 空间/Composer/Employee模式；§3.11已按CEO F1修正；§3.1A为2026-09-23 CEO接受的Shared Employee Interaction，专业对象内轻量Employee Bar＋默认隐藏讨论＋Result回Main，限定旧自动展开/员工列表/常驻Idle规则。
   - [Local Agent Computer Access ADR-0046](../07_Decisions/ADR-0046-local-agent-computer-access-authority.md) — 三档电脑访问及真实生效边界。
   - [Visual Standard V1](../03_Design/CURIS_VISUAL_STANDARD_V1.md) — 仅视觉语言；不冻结页面composition。
9. 仅在对应专业业务任务中读取：
   - [Content Growth Domain Authority](../03_Design/Curis_Content_Growth_Domain_Authority.md) — §5.4账号长期经营/逐账号效果/Provider边界，非Account execution scope。
   - [Content Growth 平台/账号本地链合同](../01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md) — 2026-10-07 CEO 确认的 Frozen 产品合同：Platform/ChannelAccount 本地模型、诚实未连接、人工回填三强制、不发出的发布核验；V1-P3 平台链 S1–S3 的唯一产品输入。
   - [RD Workspace Instance Spec](../03_Design/Curis_RD_Workspace_Instance_Spec_v1.md) — 当前仅域对象/责任与适用解剖；旧Shared/Composition服从Shell和Current UI Blueprint。

### Development / Implementation

1. [Current State](<CURRENT_STATE.md>) — 当前实现与已验边界。
2. [当前员工真实执行能力长任务 Issue](<../../issues/CURIS-V1-EMPLOYEE-EXECUTION-CAPABILITIES-20261029.md>) → [现有唯一执行看板](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>) → [Execution Backlog](<../reviews/CURIS_V1_EXECUTION_BACKLOG.md>)；只按任务 Allowed Files 进入。
3. [Development Guide](<../04_Development/Curis_Development_Guide.md>) — Git HEAD、混合工作区、RC9 Source67、Package / Native / DMG 身份分别登记；不把 HEAD 当成已提交 RC9。
4. 对应当前已交付本地版的最小输入：[RC9 Owner final receipt](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/owner-incident-20261018-01/rootf-writing-ui-owner-01/RC9_DELIVERY_RECEIPT.md>)；如需确切文件/版本再读其 Source / Package manifest 和对应 QA。接受仅限批准本地手工范围，该交付当时模型 DEFERRED、C01/真实员工 Result 正向 PENDING；CEO后续优先恢复模型，现已形成[隔离General员工DeepSeek两次真实Work/结果/用量与同版冷启有界接受](<../../artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_FINAL_MODEL_ACCEPTANCE.json>)；不是默认资料或全业务/全产品接受。CEO指定Skill的全App UX审核与获批20源码/10测试修复现已完成独立QA及同一RC3实机/冷启，见[Owner有界接受](<../../artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_FINAL_UX_ACCEPTANCE.json>)（dd99e326…）及既有Current State/唯一看板；上述局部证据保留。CEO于2026-10-27因业务入口与员工交流缺口拒收整体体验，同Task/唯一看板已重开；当前不主张日常可用、全产品或新DMG接受。
5. 仅为具体缺口追溯时读取 [Completion Reconciliation](<../reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md>) 及既有 Scope / Phase B / 单能力 Review；按原日期、原 verdict 消费，不能覆盖后续同范围已接受证据，也不能升级为当前全产品验收。

本次 A01–A03 旧入口归档已获 CEO 精确批准并完成；根三路径保留兼容指针，[归档核对](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>)沿原 Issue / 看板登记。归档任务当时模型DEFERRED；后续模型有界接受见当前Implementation route，产品接受边界不扩展。

本次只维护 Development/navigation route，依据 [文档维护决定](<../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)。上方 Product / Design 输入与领域 Frozen 合同未改。

<!-- CURRENT_REQUIRED_INPUTS_END -->

## 2026-09-15 — Product Consolidation checkpoint (historical; superseded by 2026-09-23 Product Freeze)

CEO接受Deep Reconciliation整体与F1、F2 Option A，已写回唯一Blueprint / Master Map / UI Blueprint及Shared / Domain。**TARGET PRODUCT**包含Interactive Browser、完整Model合同、opt-in Local Background、效果未知恢复、专业能力与完整Backup；**CURRENT IMPLEMENTATION**仍按下列原证据，G1-V～G6-V NOT RUN，Interactive Browser NOT VALIDATED。本登记不改CURRENT_STATE、不重新验收、不授权实现。Seven Navigation / Four-Pane / Employee / Work / Result / P7 / Usage唯一性保持。

本轮Consolidation的最终一致性当时仍待CEO Final Product Truth Review；该排期状态由上方2026-09-23 Product Freeze取代。过去高保真不是产品真相。普通UI输入只走上方Current Required链；按职责读Shared/Domain，不读整批研究补产品。

Product Truth 只能由 Product Authority 链定义；Implementation Acceptance 不得反向改写产品。`Accepted Candidate`、`Accepted`、`Frozen Implementation Acceptance` 与 Remaining Gap 按各文件原 verdict 消费，不互相升级。

## Reference Ledger — scoped records and historical checkpoints

### 2026-09-23 CEO Product Freeze — current

CEO已正式接受并冻结V1 Product Contract：Content Growth / Writing / Music；RD与E-commerce不属于V1。Content Growth、Writing、Music及Shared Employee Interaction Exploration均关闭，历史文件保留为Evidence / Decision History，不作为默认实现Authority。状态：**CURIS V1 PRODUCT FROZEN — PRODUCT EXPLORATION CLOSED — READY FOR FINAL UI MASTER**。Final UI默认输入见[Freeze](../reviews/CURIS_V1_PRODUCT_FREEZE.md)；Runtime/Capability验证继续独立，Mock / Unknown / Unverified未升级。Release仍BLOCKED。

### 2026-09-23 Shared Employee Interaction — accepted/reconciled (history)

Current入口为Blueprint → Master Map / UI Blueprint → Shell §3.1A；[Candidate](../research/shared-employee-interaction-2026-09-23/CURIS_V1_SHARED_EMPLOYEE_INTERACTION_CANDIDATE.md) / Map为Research / Decision Evidence，不是第二Authority。三业务Owner Return与Content Growth两项P1 evidence已收到。其产品冻结状态见上方当前登记；本历史条不覆盖CEO已记录的Product Freeze Decision。

### 2026-09-15 Consumed provenance — 非Current Required

- [Consolidation Review](../reviews/CURIS_PRODUCT_TRUTH_CONSOLIDATION_REVIEW.md)：本轮执行/校验/CEO来源，REVIEW，待最终Review。
- [Deep Reconciliation](../reviews/CURIS_PRODUCT_BLUEPRINT_DEEP_RECONCILIATION.md)、[Change Plan](../reviews/CURIS_PRODUCT_BLUEPRINT_CHANGE_PLAN.md)、[Target Map](../reviews/CURIS_PRODUCT_TRUTH_TARGET_MAP.md)：CEO接受后已消费，PROVENANCE / REVIEW HISTORY；不是第二产品入口。
- N1–N9、Expression V2、G1–G6 Closure及其支持材料只保Research/Implementation candidate/provenance；接受子集的唯一正式定义在当前Blueprint、Shared §10–18与Domain §5.4。未消费字段/组件/实现候选不升级。
- [Core Authority Repair](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)：原装组织/Phase A.1已由Current正文承接，Frozen CEO decision provenance；下部旧实现Gate仅历史。
- [Content Growth UX Translation](../03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md)、[CG CEO identity reconciliation](../reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md)、[RD Design Closeout](../03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md)：原scoped候选/接受来源，非普通设计必读。
- [AI Capability旧投影合同](../01_Product/AI_Capability_UI_Contract.md)、[Employee Conversation Model研究](../reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md)：保留Review与技术映射；接受产品子集消费Shared §13/18，ADR-0046既有Frozen不变。


以下保留检索与 provenance，不是新任务默认入口。带有旧 `Current` 标签的日期段只表示其登记当时的状态；若与上方 Current Required Input 或后续 supersession 冲突，以当前入口链为准。

## 2026-09-10 — Pre-Design-Research Product Structure Baseline (historical checkpoint; sequencing superseded)

Status: Frozen
Authority Class: CURRENT / PRODUCT STRUCTURE AUTHORITY
Disposition: RECORDED / CURRENT — INCLUDED IN CONTROLLED BASELINE PROMOTION
Next Gate: CURIS PRODUCT DESIGN RESEARCH — DESKTOP AI / AGENT UX

唯一结构基线：[CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](../01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)。它约束后续 Product Design Research、Final UI Master 与 Frontend Reconciliation；只记录已接受的产品结构，不新增 Product/Runtime 真源。当前 19 张 Figma 为 STRUCTURAL / IA REFERENCE，FINAL VISUAL AUTHORITY NOT APPROVED。

At that historical checkpoint, Final UI Master was paused pending research. The current sequence is recorded in the 2026-09-23 Product Freeze entry above.

## 2026-09-09 — Scope + Phase B P0 integrated closure (historical implementation checkpoint)

Status: Review
Authority Class: CURRENT / IMPLEMENTATION EVIDENCE
Disposition: IMPLEMENTED / ACCEPTED CANDIDATE
Owner: Main Development / Integration
Next Gate: CEO / ChatGPT Phase B final review

统一 COMPANY / DEPARTMENT / BUSINESS / WORKSPACE Scope 已贯通 Assignment、Conversation、Work、Execution、Context、Result、Evidence、唯一 Usage Ledger 和授权/溯源；不是 Department 豁免，不创建假 Workspace/Business/Project。支持四层执行归属 **不等于** 各层完整自主经营产品或真实云模型质量已验收。

Phase B A–E 已完成集成证据：fresh Company 正式创建路径 → 两原装部门 / 六工程员工 + 司衡 / Business=0 / 无 Key；真实责任与合法部门委托 Work；canonical Business + atomic first Generic Workspace；共享可选 Context/Utility；全局可拖动、收起、跨七区的同一 CEO Assistant。Browser、fresh packaged Desktop、正常退出/同 root restart、用户改名保持、无重复身份及 Usage 已核验。No-key 委托保持 PLANNED，不冒充执行。Result Utility 使用已有真实结果的独立副本验证，不伪造 fresh Company Result。

证据：[Scope Review](../reviews/CURIS_CANONICAL_EXECUTION_SCOPE_RECONCILIATION_REVIEW.md)（9×4 Matrix）及 [Phase B Review](../reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md)（Truth/Spatial/Assistant Maps、完整路径/hash）。最终后端120 PASS、Scope-focused40 PASS、bootstrap-focused4 PASS、前端19 PASS；lint/compile/production build/fresh Tauri package/diff check PASS。三保护 SQLite size/mtime/SHA 完全一致、integrity ok。未 stage/commit/push；mixed-source 成果全部保留，未宣称 clean committed baseline。

CORE PRODUCT / ORGANIZATION / SPATIAL MODEL: RECONCILED FOR P0 CONTRACT。
At that historical checkpoint Final UI Master was paused; the current product sequence is recorded in the 2026-09-23 Product Freeze entry above. Release remains BLOCKED.
Remaining Core P1：Global Object Search；更丰富 Leader operating entry；legacy route escapes；professional return/projection；Employee/Result 最终工作面；Knowledge reference/return UX；Capability 用户语言。位置记忆/拖动选中文字打磨、Dark/1024 为 P2。本轮不开始任何下一 Initiative。

下方同日 in-progress / Department gate / E-not-started 段落均是 **HISTORICAL CHECKPOINT — SUPERSEDED**，不得重新作为 Current blocker；Phase A.1 产品决定保持原 Authority，不被实现反向改写。


## Historical Canonical Execution Scope checkpoint — 2026-09-09

Status: Review
Authority Class: HISTORY / IMPLEMENTATION CHECKPOINT
Disposition: HISTORICAL IN PROGRESS — SUPERSEDED BY THE INTEGRATED CLOSURE ABOVE

当前依赖为统一四层Execution Scope，不再是待CEO裁决的Department-only扩展。[Scope Review](../reviews/CURIS_CANONICAL_EXECUTION_SCOPE_RECONCILIATION_REVIEW.md)记录实际数据/执行差异、74项隔离检查和剩余Identity/Context/Usage工作；正式Issue为 `issues/CURIS-CANONICAL-EXECUTION-SCOPE-RECONCILIATION-001.md`。实现支持不等于各层完整Autonomous Operating产品验收；Phase B/Final UI/Release未升级。

## Historical Phase B implementation checkpoint — 2026-09-09

Status: Review
Authority Class: HISTORY / IMPLEMENTATION CHECKPOINT
Disposition: HISTORICAL PARTIAL — SUPERSEDED BY THE INTEGRATED CLOSURE ABOVE

CEO已授权实现；当前入口为 [Phase B Review](../reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md) 和 `issues/CURIS-PHASE-B-P0-CORE-PRODUCT-RECONCILIATION-001.md`。原装部门实例可物化，但Department-scoped Employee Conversation/Work执行与后续Workspace identity复用未闭环。Final UI继续PAUSED、Release BLOCKED。下方开工授权前的记录保留为历史，不代表Phase B全未修改，也不代表已验收。

## Historical Phase A.1 registration checkpoint

先消费 [Authority Repair Phase A.1 / CEO Role Decomposition](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)：空间工程6定义/6初始实例已裁决，数据分析最低1。人数Gate已关闭；不得继续实施旧“两部门seed”合同。再按下方七项Authority顺序读取。
[Phase B P0 Implementation Contract Final Candidate](../reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md)：待CEO/ChatGPT最终Review；未开始实现。

## Historical implementation checkpoint — 2026-09-09 Phase A.1

Status: Frozen
Authority Class: HISTORY / GOVERNANCE CHECKPOINT
Disposition: HISTORICAL IMPLEMENTATION STATUS — SUPERSEDED; the CEO product decision remains in Current Product Authority.
Owner: CEO / Product Authority; Main Development registration
Source: docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md, Phase A.1.

Curis原装公司经营组织（不是纯default seed）必须在每Company形成两原装部门、真实Employee、Role/Responsibility/Assignment及合法Work Surface；用户Business可0，无Key不阻止员工物化。
CEO ROLE DECOMPOSITION已接受：空间工程freshCompany **6个官方定义→6个不同canonical Employee实例**（空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家）；不把Prototype六人名单升为定义。“牧人”未恢复可定位来源。数据分析部最低1 Company Analyst已正式确定，主要工作面Operating Intelligence；“司衡”为恢复产品称谓，不是Runtime查找键。
Definition→Company Employee Instance→Current Holder分离；原装/用户员工共用Detail/Edit，编辑不换身份，Requirement持续。缺模型或Holder必须truthful。定义存储优先复用，若需新primitive/schema先Architecture Review。

PHASE B CONTRACT: UPDATED / READY FOR REVIEW
PHASE B IMPLEMENTATION: NOT STARTED — decomposition gate CLOSED; final contract review + bounded Issue required
FINAL UI MASTER: PAUSED
RELEASE: BLOCKED
ACCEPTED CAPABILITY CHAINS: PRESERVED

P0-A现为Company bootstrap + built-in organization/Employees，P0-B现为责任+Organization/Insights/业务启用工作面；新增Edit/restart/sameidentity、无Provider创建、真实Analyst验收。P0-C/D/E保持。最低Analyst归属从旧P1合并进P0-B，避免重复任务。
Final UI resume gate：真实built-in organization、official Employees、Business activation、Four-Pane、floating Assistant验收；未来增加初始组织、两团队、Employee Detail/Edit及用户员工对照。尚未做任何实现或UI。
详见docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md。以下Phase A仅在A.1明确处被替代，其余保持。

## Historical required-authority list — superseded by Current Required Input

本轮新增最高优先级必读入口，不替代原Master Map展开路径。读取顺序：
1. [Product Blueprint](../01_Product/Curis_Product_Blueprint.html) — Frozen Product Authority
2. [Company OS Shared Authority](../03_Design/Curis_Company_OS_Shared_Authority.md) — Frozen shared definitions
3. [Workspace Shell Contract](../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md) — Frozen spatial/P1–P7
4. [Core Product Authority Repair](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md) — CURRENT / ACCEPTED CEO scoped amendments
5. [UI Blueprint](../01_Product/Curis_Product_UI_Blueprint.html) — Frozen spatial projection
6. [Visual Standard](../03_Design/CURIS_VISUAL_STANDARD_V1.md) — visual language, not page composition
7. [Current State](CURRENT_STATE.md) — implementation truth, not product authority

[Master Map](../01_Product/Curis_Product_Master_Map.md)继续展开Blueprint；不得只读implementation review。
未来Final UI工作先读Authority Repair明确supersession，再依Blueprint→Shared→Shell→UI→Visual→Inventory→Gap Review；这与上列依赖顺序不改变Authority高低关系。
[Phase B Contract](../reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md)是Review candidate，非自动开工授权。

## Historical implementation scope checkpoint — 2026-09-09 Phase A

Status: Frozen
Authority Class: HISTORY / IMPLEMENTATION SCOPE CHECKPOINT
Disposition: HISTORICAL IMPLEMENTATION STATUS — SUPERSEDED; accepted Product Authority and scoped evidence remain preserved.
Owner: Main Development / Product Authority
Source: CEO Phase A decision; docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md.
Next Gate: Phase B bounded Issue/contract review; no implementation performed in Phase A.

CORE PRODUCT MODEL: AUTHORITY REPAIRED / IMPLEMENTATION RECONCILIATION PENDING
CORE ORGANIZATION MODEL: RECONCILIATION PENDING
CORE SPATIAL MODEL: RECONCILIATION PENDING
ACCEPTED CAPABILITY CHAINS: PRESERVED
SCOPED CAPABILITY IMPLEMENTATIONS: ACCEPTED within recorded verdicts
WHOLE PRODUCT CONTRACT: NOT YET RECONCILED
FINAL UI MASTER: PAUSED / NOT READY
RELEASE: BLOCKED / PUBLICATION NOT AUTHORIZED

“PRODUCT COMPLETE / no remaining blocking P1”不再是Current整体结论。2026-09-08及更早下列checkpoint保留原证据，仅证明其scoped链；不得覆盖本节。Knowledge、Meeting Core、Conversation、General lifecycle等已验收能力不撤销，Meeting autonomy保留accepted candidate及自然multi-cycle evidence边界。
P0-A两support Departments bootstrap、P0-B组织责任承接、P0-C canonical activation seam、P0-D共享Four-Pane、P0-E浮层Assistant仍需实现对账；P0-F完成登记纠偏已在Phase A完成。详见docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md（Review candidate）。
Final UI resume gate：PHASE B CORE PRODUCT P0 RECONCILIATION ACCEPTED，至少bootstrap/组织骨架/共享壳/Assistant最低合同落地。不要按旧UI frame清单立即开工。

## Historical scoped checkpoint — 2026-09-08 Seven-area final implementation acceptance

Authority Class: HISTORY / SCOPED IMPLEMENTATION EVIDENCE. Status: Review.
Disposition: SCOPED CAPABILITY ACCEPTANCE PRESERVED; whole-product inference SUPERSEDED by 2026-09-09 Phase A.
Historical wording (not current): “PRODUCT COMPLETE / ACCEPTED WITH RECORDED P2; final CEO review required.”
Owner: Main Development. Source: CEO seven-area bounded acceptance instruction;
`docs/reviews/CURIS_V1_GLOBAL_UI_SEVEN_AREA_FINAL_ACCEPTANCE.md`, **Final verdict**;
`issues/CURIS-V1-GLOBAL-UI-SEVEN-AREA-FINAL-ACCEPTANCE-001.md`.

Seven accepted product areas now have Browser and fresh packaged native continuity
evidence, authorized real result recovery, Result Viewed persistence and stable
same-root restart/no replay. Three protected DB fingerprints unchanged, integrity=ok.
Selected backend 58 PASS; focused frontend 6 PASS; full frontend 89/95 with six
recorded legacy assertion failures. Production/package build PASS.
Historical scoped finding only: “No remaining blocking P1 identified in this acceptance.” This did not cover the complete product contract; Phase B P0/P1 gaps are current. Earlier global-UI checkpoints remain evidence, not permission to bypass the Phase B gate.

Meeting remains CORE IMPLEMENTED / AUTONOMOUS DISCUSSION ACCEPTED CANDIDATE;
final multi-cycle real-world evidence is pending and nonblocking.
Recorded P2 includes Dark/1024, full accessibility, disabled global search,
future connectors/formats, native-console certification and bounded visual/test
maintenance. No external capability or release readiness is inferred.
Next gate: CEO / ChatGPT final product review. RELEASE AUTHORIZATION: NOT GRANTED.
No staging, commit, push or publication. Do not begin another initiative.



Status: Frozen
Authority Class: FROZEN · TRUTH ROUTER

Updated: 2026-09-07

## 2026-09-08 General Workspace lifecycle — final native acceptance

Authority Class: CURRENT / IMPLEMENTATION REGISTRATION. Status: Review.
Source: CEO native404/final Desktop instructions; `issues/CURIS-V1-GENERAL-WORKSPACE-LIFECYCLE-CLOSURE-001.md`
and `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_LIFECYCLE_CLOSURE_REVIEW.md`,
**Current final verdict**. Owner: Main Development.
Disposition: **IMPLEMENTED / ACCEPTED** for bounded lifecycle and native entry;
final CEO / ChatGPT review requested, not a release authorization.

Native404 was prior isolated-fixture CEO scope mismatch, not missing routes.
New legally created Company/root proves CEO Desk→Business→Workspace.
Real DeepSeek Work A pause→restart→resume→archive/restore and Work B running
cancel passed; final two-line projection correction prevents old RUNNING
snapshots claiming a current executor. Fresh corrected package and complete
same-root restart retain Work/Task/Result/Evidence/Usage/receipt without replay.
55 backend / 15 frontend checks pass; ESLint/compile/build/package/diff pass.
Three protected DBs byte-identical, integrity ok. No stage/commit/push.

Current V1 remaining P1: **GLOBAL UI / SEVEN-AREA FINAL PRODUCT ACCEPTANCE**.
Include observed synchronous-submit control accessibility until route remount,
scope-error wording, internal labels/result titles and existing global experience
drift. No accepted area is reopened as unimplemented. General lifecycle no longer
the primary development blocker. Meeting natural multi-cycle evidence remains a
non-code follow-up; connectors/voice/Dark and distribution retain their boundaries.
NEXT RECOMMENDED V1 INITIATIVE: **GLOBAL UI / SEVEN-AREA FINAL PRODUCT ACCEPTANCE**.
Recommendation only; not started. Older dated next-initiative entries are history.

## Conversation System final productization pointer — 2026-09-07

Authority Class: CURRENT / IMPLEMENTATION POINTER. Read `issues/CURIS-V1-CONVERSATION-ATTENTION-LIFECYCLE-001.md` → `docs/reviews/CURIS_V1_CONVERSATION_ATTENTION_LIFECYCLE_REVIEW.md`, **Global productization final return**. Core System / Sidebar: IMPLEMENTED / ACCEPTED WITH RECORDED FOLLOW-UP; final CEO / ChatGPT review requested. Same event-backed topic/Employee identities, shared Composer, same Usage ledger, cross-area references, Viewed/Attention and fresh native same-root restart are verified. Final 46 backend / 8 frontend checks pass; three protected DBs unchanged. Review distinguishes actual cloud reply from manual business-result fixtures and records global Search404 / legacy wording / native console follow-up; no unqualified Console0 or fresh successful General Work execution claim.

This implementation registration does not replace Product Blueprint or grant release. Prior owner/Project-required usage gates are resolved, not current blockers. V1 next recommendation only: GENERAL WORKSPACE LIFECYCLE CLOSURE, followed by global seven-area UI/final acceptance; no next implementation started. Meeting's natural real-world multi-cycle evidence remains separate. No commit/push.

## Conversation / Attention implementation pointer — 2026-09-07 (historical scoped checkpoint)

Current correction: Employee owner and same-ledger Conversation attribution gates RESOLVED. Read Final implementation return in `docs/reviews/CURIS_V1_CONVERSATION_ATTENTION_LIFECYCLE_REVIEW.md`: IMPLEMENTED / ACCEPTED CANDIDATE, real Employee DeepSeek reply with 1082 confirmed tokens/cost UNKNOWN, no Project/Work prerequisite, shared reference/Attention and final packaged restart verified. Earlier unknown failed-call usage is preserved, not backfilled. Three protected DBs unchanged; no commit/push.

Authority Class: HISTORY / SCOPED IMPLEMENTATION CHECKPOINT. Read `issues/CURIS-V1-CONVERSATION-ATTENTION-LIFECYCLE-001.md` then the above Review. This dated checkpoint is not a Current Required Input and does not reopen its former next gate.

## 2026-09-06 Meeting Room — Current Status Registration

Authority Class: CURRENT / IMPLEMENTATION REGISTRATION. Source: CEO “MEETING ROOM CURRENT STATUS REGISTRATION” decision (2026-09-06), existing Meeting Productization and Autonomous Discussion Reviews. Disposition: implementation complete; final real-world multi-cycle acceptance remains pending. Owner: Main Development / CEO. This registration supersedes older Meeting implementation-pending, code-blocker and unqualified PARTIAL wording for current status, without changing historical evidence.

- MEETING ROOM CORE IMPLEMENTATION: IMPLEMENTED.
- MEETING AUTONOMOUS DISCUSSION: IMPLEMENTED / ACCEPTED CANDIDATE.
- VERIFIED: Meeting lifetime usage; advancement cycle budget; no budget laundering; completed execution safe reuse; restart / no replay; real cloud model; Employee SPEAK / STAY_SILENT; Proposal → P7 → CEO Decision → Work → Result; Result → Evidence → Leader re-evaluation.
- FINAL MULTI-CYCLE CLOUD ACCEPTANCE: PENDING REAL-WORLD EVIDENCE.

IMPLEMENTATION COMPLETE ≠ FINAL REAL-WORLD MULTI-CYCLE ACCEPTANCE COMPLETE. These verified mechanisms and historical cloud segments are not a claim that the final multi-cycle cloud sequence has passed. Next evidence gate: a genuinely new business fact / Result / Evidence / CEO Message, persisted through existing legal commands → new Advancement Cycle → independent bounded budget → same Meeting continues. Evidence must arise naturally in subsequent real use; no fabricated event, limit increase, history reset, replacement Meeting or token expenditure solely to obtain ACCEPTED. No current code blocker; Meeting is no longer the V1 development main blocker. No Runtime change is authorized by this registration.

Evidence / current scope: `docs/reviews/CURIS_V1_MEETING_AUTONOMOUS_DISCUSSION_REVIEW.md` and `docs/reviews/CURIS_V1_MEETING_ROOM_PRODUCTIZATION_REVIEW.md`. Remaining work is reconciled in `docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md` and `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` (2026-09-06 sections). Next recommended initiative, not started: CEO / Employee Conversation & Attention Lifecycle Closure. Distribution is technical preparation only; product release is not authorized. Older dated “next gate” entries below are historical checkpoints, not current dispatch instructions.

## 2026-09-02 MEETING ROOM UI — HISTORICAL CHECKPOINT / SUPERSEDED FOR IMPLEMENTATION

`docs/reviews/CURIS_V1_MEETING_ROOM_UI_ACCEPTANCE.md` registers Meeting Room Product and UX as `ACCEPTED` and the 1440 × 900 Light UI as `UI ACCEPTED`. Current Figma baseline: `214:3` Overview, `247:2` Start Meeting Overlay, `214:279` Active Conversation, `214:555` Decision Moment and `214:831` Responsibility + Result Continuity. Meeting creation is temporary Overlay → persistent Meeting; conversation, canonical Decision/P7, Responsibility, Work and Result remain one continuity chain. Next gate: `MEETING ROOM PRODUCTIZATION CLOSURE`; Runtime/Data implementation is not claimed.

## 2026-09-01 KNOWLEDGE LIBRARY IMPLEMENTATION — CURRENT IMPLEMENTATION TRUTH

`docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_IMPLEMENTATION_ACCEPTANCE.md` registers Knowledge Library as `IMPLEMENTED / ACCEPTED`: canonical Company / Business / Workspace scope, generic typed `Work → USES_REFERENCE → Knowledge`, bounded Context injection, reverse Used By Work, Result / Evidence projection, archive / hard-delete protection, 105-entry scale, Browser, fresh packaged Desktop, same-root restart/persistence and active SQLite safety passed. Figma `187:2 / 187:276 / 187:550 / 187:824` remains the Current Design Baseline. Unsupported formats/connectors, semantic/vector retrieval, full citation/versioning, ACL, graph, promotion, dedup, conflict and full retention remain bounded Future/P2 gaps. Next Product Completion area: `MEETING ROOM PRODUCTIZATION CLOSURE`.

## 2026-09-01 KNOWLEDGE LIBRARY PRODUCT / UX — ACCEPTED DIRECTION

`docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_ACCEPTANCE.md` registers the accepted product mind **Company Reference Space** for the user-facing `资料库`. The accepted structure is Overview, Browse/Search, Reading/Reference Detail, Select Reference From Work and Used By Work/Result. Scope language is `适用范围 / 使用范围` over Company → Business → Workspace; Source, Knowledge/Reference, Context, Evidence and Result remain distinct and reuse existing truth. Direction A/B are only interaction/retrieval references. Specific visual and implementation status are registered by the UI and Implementation acceptance records above.

## 2026-09-01 KNOWLEDGE LIBRARY UI — UI ACCEPTED

`docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_UI_ACCEPTANCE.md` registers the 1440 × 900 Light Figma baseline `187:2 / 187:276 / 187:550 / 187:824` for 资料库 Overview, Browse / Search, Reading / Reference Detail and the compact Select Reference From Work picker. Reading-first, Reference Row, explicit batched Load More, truthful count handling, lightweight Company / Business / Workspace scope selector and return-state continuity are Current UI responsibilities. Implementation status is registered above; remaining Dark / 1024, accessibility / keyboard and other bounded UI adaptations remain P2.

## 2026-09-01 TALENT & CAPABILITY — IMPLEMENTED / ACCEPTED

`docs/reviews/CURIS_V1_TALENT_CAPABILITY_IMPLEMENTATION_ACCEPTANCE.md` registers Talent & Capability, Expert Recruitment, Company Employee, Skill Installation and Employee Capability Binding as `IMPLEMENTED / ACCEPTED`. Connector truth is verified but remains honestly `未连接 / 需要授权`; external talent candidates and unsupported catalog Skill types are not promoted. Employee Avatar is `IMPLEMENTED / ACCEPTED` with the shared `employee_instances.avatar_ref` truth, eight bundled Curis Cartoon Avatar Set presets, upload or fallback, optional selection and packaged restart persistence; no separate avatar or identity store exists. Browser, fresh packaged Desktop, restart/persistence, active DB safety and scoped tests/build evidence passed. Remaining external Connector authorization/execution, external providers, unsupported Skill alignment and later avatar editing remain bounded gaps. Next Product Completion gate: `MEETING ROOM PRODUCTIZATION CLOSURE`.

## 2026-08-31 OPERATING INTELLIGENCE IMPLEMENTATION — CURRENT IMPLEMENTATION TRUTH

`docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_IMPLEMENTATION_ACCEPTANCE.md` registers Operating Intelligence as `IMPLEMENTED / ACCEPTED`: canonical analytical projection, 7/30-day and Business-scoped analysis, comparable comparison, Unknown/provenance/freshness, Artifact-backed Report, canonical P7 Decision continuity, Browser, fresh packaged Desktop, restart/persistence, focused/regression tests and active SQLite safety passed. External Outcome/Feedback connectors and automated analyst/report authoring remain bounded capability gaps; no second analytics truth or fake outcome was introduced. Next Product Completion focus: `TALENT & CAPABILITY PRODUCTIZATION CLOSURE`.

## 2026-08-31 OPERATING INTELLIGENCE UI — CURRENT ACCEPTED DESIGN BASELINE

`docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_UI_ACCEPTANCE.md` registers Operating Intelligence as Product `ACCEPTED`, UX `ACCEPTED` and UI `UI ACCEPTED` for the 1440 × 900 Light Figma baseline `172:3 / 172:277 / 172:551 / 172:825`. The accepted states are Overview, Scoped Business Analysis, Explore / Benchmark and Report / Decision Continuity. CEO Desk remains the attention / Matter surface; Operating Intelligence is the scoped deep-analysis surface and consumes canonical data without a second Truth, Result or Analytics Runtime. No P1 remains; Prototype wiring, Dark, 1024, accessibility/keyboard and real Runtime data-density verification remain P2. Implementation acceptance is registered above.

## 2026-08-31 ORGANIZATION CENTER IMPLEMENTATION — CURRENT IMPLEMENTATION TRUTH

`docs/reviews/CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md` registers Organization Center as `IMPLEMENTED / ACCEPTED`: Company Map, Business Focus and Employee Directory use canonical organization projection; fixed two-tab UI, Figma `106:3 / 106:230 / 106:457`, Browser, fresh packaged Desktop and restart/persistence passed. Active DB safety is byte-identical/integrity `ok`; no Fixture or second organization model. Remaining Dark, 1024, accessibility/keyboard, fuller Search/Filter wiring and legacy cleanup are P2. Operating Intelligence UI is now separately accepted; the next Product Completion gate is `OPERATING INTELLIGENCE PRODUCTIZATION CLOSURE`.

## 2026-08-31 ORGANIZATION CENTER UI — CURRENT ACCEPTED DESIGN BASELINE

`docs/reviews/CURIS_V1_ORGANIZATION_CENTER_UI_ACCEPTANCE.md` registers Organization Center as `UI ACCEPTED` for the 1440 × 900 Light state. The fixed two-tab structure is `公司版图 / 员工目录`; Company Map uses Department Container + Business-first + progressive Role/Staffing disclosure, and Employee Directory reads Employee → Role → Business → Department. Figma file key `2Fh7DgPPfLgdbvNtnzPnk9`, frames `106:3`, `106:230`, `106:457` are the Current Design Baseline. Implementation is now separately registered as `IMPLEMENTED / ACCEPTED` by `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md`; Dark, 1024, accessibility and interaction wiring remain P2.

## 2026-08-31 DISTRIBUTION STRATEGY — GITHUB BETA CURRENT TARGET

`docs/reviews/CURIS_V1_DISTRIBUTION_STRATEGY.md` registers the two-stage macOS
strategy. Stage A is GitHub Beta Distribution: a versioned ad-hoc DMG with SHA-256,
install/Open Anyway guidance, backup/restore and upgrade limitations; Apple Developer
Program membership, Developer ID and notarization are not beta prerequisites. Stage B,
Trusted macOS Distribution, is deferred by CEO and will require Developer ID,
notarization, stapling and stable identity when opened. Next gate:
`CURIS V1 GITHUB BETA DISTRIBUTION CLOSURE`.

## 2026-08-30 WHOLE-APP LIVE AI — IMPLEMENTED / ACCEPTED WITH RECORDED P1

`docs/reviews/CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE_REGISTRATION.md` is the current implementation registration for the Whole-App Product Gap Closure Review. The packaged, path-specific V1 vertical now proves real CEO Assistant submit, Employee/Responsibility, Work, DeepSeek execution, Result/Evidence/Artifact, P7 round-trip, automatic resume, exact-package restart, Keychain recovery and post-restart real AI with no fake data. PRODUCT GAP is CLOSED for this scope. Next distribution gate: GitHub Beta Distribution Closure. CEO Desk language/Applied Decision attention and external connectors remain recorded P1/boundaries.

## 2026-08-30 V1-P0-003 / CLOUD MODEL CONTINUITY — IMPLEMENTED / ACCEPTED

`docs/reviews/CURIS_V1_CLOUD_AI_CONTINUITY_ACCEPTANCE.md` is the current implementation acceptance record for native macOS Keychain and DeepSeek cloud continuity. It supersedes the bounded P0's earlier Partial / M3-blocked current wording with accepted save/read/delete, Health, dynamic discovery, tenant-private default, pre/post-restart real cloud calls, delete/restart-unconnected and secret-safety evidence. Scope is limited to the current Provider architecture proven through DeepSeek; trusted macOS distribution remains a deferred Stage B. Build Reliability Debt is separate.

## 2026-08-29 V1 FRONTEND BATCH 1 — IMPLEMENTED / ACCEPTED WITH RECORDED BOUNDARIES

`docs/reviews/CURIS_V1_FRONTEND_BATCH_1_IMPLEMENTATION_ACCEPTANCE.md` registers the final Browser / packaged Desktop / restart acceptance from `docs/reviews/CURIS_V1_FRONTEND_BATCH_1_FINAL_ACCEPTANCE.md`. Accepted Batch 1 scope includes App Shell, seven-area Navigation, Welcome, optional Skip / Empty Curis, CEO Display Identity, Company + canonical CEO Assistant presence, Empty Company, Model Management UI, Create Business Proposal, canonical General Business + first General Workspace, CEO Desk Operating / Attention Projection, restart recovery and packaged Desktop mainline. This is not V1 or Frontend complete. Native Keychain and current-provider cloud continuity are separately `IMPLEMENTED / ACCEPTED`; Conversation, Composer, Model Selector and 1024/Assistant layout remain Partial or P1 adaptation; Employee Avatar is superseded for current status by `docs/reviews/CURIS_V1_TALENT_CAPABILITY_IMPLEMENTATION_ACCEPTANCE.md`; Professional Workspace automatic matching/materialization remains open. Whole-App live AI is now separately `IMPLEMENTED / ACCEPTED WITH RECORDED P1` in `CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE_REGISTRATION.md`. Legacy floating `GlobalAssistant` is `LEGACY / P1 UNIFICATION REQUIRED`. Next target: General Workspace P1 Operating Closure, first priority canonical CEO Assistant / Conversation unification.

## 2026-08-28 APP ENTRY UI — CURRENT ACCEPTED UI BASELINE

`docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md` registers the Figma file [Curis V1 — App Entry & CEO Assistant Experience](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-App-Entry-CEO-Assistant-Experience), file key `2Fh7DgPPfLgdbvNtnzPnk9`, as the current App Entry UI design baseline. Product / interaction and UI are accepted; implementation remains pending engineering reconciliation. Reuse the registered 13 core Frames and shared Navigation, CEO Identity, Conversation / Composer, Model Management / Selector and truthful Empty State patterns. This acceptance does not claim Frontend, Runtime, Schema, credential or provider implementation. Older App Entry / First Run / Prototype / fixture / original Trae candidates are superseded where conflicting, with historical provenance preserved. CEO Desk now has its own accepted Operating UI baseline (`69:3`).

## 2026-08-28 CEO DESK OPERATING UI — CURRENT ACCEPTED UI BASELINE

`docs/reviews/CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md` registers Figma `2Fh7DgPPfLgdbvNtnzPnk9`, Frame `CEO Desk — Operating / Matters Present` (`69:3`), as the Current Operating Design Baseline. CEO Desk product structure, Operating Composition and Operating UI are accepted for the 1440 × 900 Light state; remaining states are Adaptation / Validation only. Implementation remains pending Engineering Reconciliation and is not claimed as implemented. Reuse the Attention-first Company State → Today Brief → Primary Matter → Watching → Important Result → Next Responsibility → on-demand Assistant reading model and the accepted App Entry shared patterns. Next: CEO Desk Implementation / Adaptation Readiness Review.

## 2026-08-28 CEO / Employee Avatar Identity Pattern — HISTORICAL REVIEW INPUT / SUPERSEDED FOR IMPLEMENTATION STATUS

共享头像规则登记见 `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`：CEO 与 AI Employee 均可上传头像、选择 Curis 预置卡通头像或跳过使用 fallback；头像可选、不阻塞创建，不影响身份、责任、能力或执行。该历史 Pattern 的实现缺口已由 `docs/reviews/CURIS_V1_TALENT_CAPABILITY_IMPLEMENTATION_ACCEPTANCE.md` 的 Employee Avatar closure supersede；当前 Employee Avatar 已为 `IMPLEMENTED / ACCEPTED`，而 CEO Avatar 的后续实现仍按其真实状态判断。

## 2026-08-27 CEO Assistant / Model Experience — REVIEW READY

`docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md` 登记 CEO Display Identity、Company 创建后的 CEO Assistant first presence，以及模型配置入口与 Conversation Model Selector 的分离；`docs/reviews/CURIS_APP_ENTRY_LIFECYCLE_CONTRACT.md` 与 `docs/reviews/CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md` 已完成窄幅对齐。模型管理继续从左下 CEO 头像进入，模型使用在 Conversation 内切换；不新增身份、配置或 Conversation 系统。当前为 Review 输入，不覆盖三份 Current Product Truth。

## 2026-08-24 CONTENT GROWTH — CEO AUTHORITY DECISION RECONCILIATION

CEO 已接受并同步三项窄范围产品决定：`Workspace` 是唯一 canonical user/product identity；`Office` 退出当前用户产品语义，仅保留历史 / implementation / migration provenance，不迁移 Runtime、Schema、`office_id` 或 `OfficeAccountBinding`；Content Growth 是 `Professional Workspace Candidate`（不是 Verified），XHS / Douyin / TikTok / YouTube / Bilibili 等是 `Channel`，具体账号是 `Channel Account`，均不等于 Workspace。全局 `Main = selected Professional Surface + Shared Work Area` 保持不变；Content Growth 的 `CEO Operating Result / 经营结果面` 仅是 Domain-scoped default selected Surface / projection，不是新的全局 Main、Dashboard Runtime 或第二套 Truth。8 Operating States / 4 Cognitive Buckets 仍是 Research / Accepted Candidate，不升格为 Product Authority、Runtime Schema 或固定 UI Contract。详见 `docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md`。

## 2026-08-22 Professional Workspace Strategy — CEO Accepted / Authority Reconciled

Current Product Truth 已正式收敛为 Verified Professional Workspace First：专业环境优先匹配 Verified Match，再做 Instance Configuration、Maintained Derived、Safe Composition；只有真实 Truth / Domain / Risk Gap 才插入 bounded Research，Generation 是 last resort。Professional / Generic、Provenance（Curis Official / Partner / Community / User-or-AI Generated）与 Assurance（Verified / Candidate / Unverified / Deprecated）三轴分离；Official、Professional、Generated 不自动等于 Verified。Business 页面是通用 Business Configuration，不是 Workspace Builder / Low-code App Builder / Workflow Builder；Workspace Engineering 是 resolution-first 的匹配、配置、组合、验证与演进能力。Professional UX / Interaction 是 Domain Operating Capability Package 的一等声明资产。Review：`docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_STRATEGY_AUTHORITY_RECONCILIATION_REVIEW.md`。

实现边界不变：Multi-Surface Workspace Package v2 foundation、Canonical Child Work foundation 与 sequential cross-professional multi-Work proof 已由既有 commits 接受；Official Library、Verified Registry、Professional Module、Generic → Professional 安全升级、Package method metadata、parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping、第三方 Package ecosystem 与完整 Domain migration 仍是 Product → Implementation Gap。本轮无新增 Runtime、Schema、DB、Frontend、Prototype、Package runtime、commit 或 push。

## 2026-08-21 Professional Workspace — CEO Accepted / Authority Reconciled

Current Product Truth 已登记：Workspace 是完整专业经营环境而非 Page；一个长期 Workspace 可有多个 Professional Surface，并由一条 canonical Operating Team responsibility boundary 贯穿；Surface 只声明 Responsibility requirement，不绑定 Employee；Four-Pane 是职责模型；Context 承担 Domain Navigation / Context，Main 显示当前 Surface，Utility 承担 Detail / Editor / Evidence / Tool；Team / Knowledge / Artifact / Work / Result / Evidence 复用 Company OS；禁止 Surface Runtime。XHS `内容增长部 / 小红书运营 / AI 科技` 中经营概览为 default candidate，Calendar 已归位为内容运营 Object View，具体菜单未冻结。Review：`docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_AUTHORITY_RECONCILIATION_REVIEW.md`。

实现边界不变：该历史条目中的旧未实现表述已由 2026-08-22 Current Truth Correction 收窄；当前应读取 Multi-Surface Workspace Package v2 foundation、Canonical Child Work foundation 与 sequential cross-professional multi-Work proof 的 accepted commits。Parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping、RD / XHS migration 与 final Package schema 仍未完成；Autonomous Operating V1 Core 不变。本次无新增 Runtime、Schema、DB、Frontend、Prototype、commit 或 push。

## 2026-08-20 Product Authority — Final Three Micro Stale Cleanup

三项窄范围语义已同步至唯一 Product Blueprint、UI Blueprint 与 Product Context：Bootstrap 示例路径、Leader 自主调整边界、CEO Assistant 的未知专业责任边界。其余产品模型与实现层保持不变。

## 2026-08-20 Product Authority — Three-Layer / Autonomous Operation Stale Path Cleanup

五项 Current Product Truth 微调已同步至唯一 Product Blueprint、Master Map、UI Blueprint 与 Product Context：首次进入、Assistant 职责、Workspace Studio Bootstrap、Work 来源与 RD/XHS/抖音示例边界统一；仅做语义清理，不改变 Package 架构、Autonomous V1、Runtime、Schema、DB 或代码。

## 2026-08-20 Three-Layer Operating Model — CEO Accepted

`docs/reviews/CURIS_THREE_LAYER_OPERATING_MODEL_RECONCILIATION.md` 已由 CEO 接受（`Authority Class: REVIEW`、`Status: Frozen`、`Disposition: CEO ACCEPTED / APPROVED ARCHITECTURE REVIEW INPUT`）。它确认 `User Surface → Employee Operating Layer → System Runtime`、Universal Business Responsibility Handoff、Unknown Business 路径、Domain Operating Capability Package 语义及不新增 Playbook；不覆盖三份 Current Product Truth，不修改 Autonomous V1、Canonical Business Spine 或实现层。

## 2026-08-20 Brand Neutrality Architecture Principle — CEO Accepted

同一已接受 Review 记录 Brand Identity（Curis）、Product Semantic Identity、Runtime / Persistent Identity 三层分离；用户文案可使用 Curis，内部语义与 canonical IDs 保持品牌中立；未来 Brand Configuration 只作为实现方向。本轮无 Rebrand、无批量 rename、无代码/Runtime/Schema/DB 变更。

## 2026-08-20 Operating Lifecycle Product Contract

CEO 已接受 Operating Lifecycle 为 **Approved Candidate / 未实现**：`docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`；交叉综合记录见 `docs/reviews/CURIS_AUTONOMOUS_BUSINESS_OPERATION_SYNTHESIS.md`。它补充 Product Blueprint / Master Map 的经营连续性语义：Responsibility 默认持续、Cycle bounded Close、PAUSE 与 STOP 分离、Approved Strategy Envelope、显式 Next-cycle Decision、Primary Autonomous E2E 与 Cross-domain Contract Proof。该候选不覆盖 Current Product Truth，不代表 Runtime Accepted，不授权代码实现。实现状态仍只读 `CURRENT_STATE.md`、正式 Issue、Accepted Review 与真实证据。

## 2026-08-20 Autonomous Operation Product Surface Mapping Review

页面表面映射见 `docs/reviews/CURIS_AUTONOMOUS_OPERATION_PRODUCT_SURFACE_MAPPING.md`。CEO 已接受其三项微调并升级为 `CEO ACCEPTED / APPROVED SURFACE MAPPING`：Business 使用 Workspace 数量与入口；Bootstrap 默认接受不完整意图并先研究/形成 Strategy Proposal；Workspace Current Operating 固定为经营状态、本轮重点、最新判断、下一步，进展由当前相关 Professional Surface 优先表达，需要关注仅条件显示。该映射仍不新增 Operating Console，不代表 UI / Runtime / Code 已实现。

## 2026-08-20 Autonomous Operating V1 Implementation Readiness

唯一未来实现 Issue：`issues/20260820_autonomous_operating_v1_implementation_001.md`；Readiness：`docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_IMPLEMENTATION_READINESS.md`。状态为 `READY AFTER CANONICAL BUSINESS SPINE ACCEPTANCE / IMPLEMENTATION NOT AUTHORIZED`。硬 Start Gate 是 Canonical Business Spine `IMPLEMENTED / ACCEPTED` 及其完整 Accepted Evidence；不得消费进行中的 Business Spine 实现，不得提前修改 Runtime、Schema、DB、Frontend 或创建 autonomous control data。

## 当前 Worktree / Development Baseline

### 2026-08-19 Current Authority Cleanup

Leadership / Responsibility cleanup has been applied to the current Product Truth and applicable page contracts: Workspace is restored in the organization chain, Workspace Leader is an explicit management responsibility, and Workflow editing is bounded to a Workspace-local inline surface. No Runtime, Schema, database or code change is implied.

本轮 Worktree Cleanup 的受保护源快照为：

- 文档同步前 HEAD：`a94bf6144bed0b2631bf0076204703580f3ed075`；
- G1 已 commit：`42db50cde54bc735d709bd603fe4d98d7f8233c8`；
- G2 XHS：`IMPLEMENTED / ACCEPTED`，但源码为 `COMMIT BLOCKED BY SHARED RUNTIME STRUCTURE`；
- G3 RD Phase 0/1：accepted bounded execution slice，源码为 `BLOCKED BY MIXED SOURCE`；
- RD long-running reliability：`ACCEPTED / CLOSED`，不等于整个 RD Phase 2A Accepted；
- Content Growth：T5 closure，T1–T4 未重做，final high-fidelity deferred；
- Workspace Engineering：Methodology / Technical Direction `Review / APPROVED CANDIDATE`；首个受控 Declarative Workspace Package substrate `P0 IMPLEMENTED / ACCEPTED`；Company OS 真实集成与最小经营循环 `P0.5 IMPLEMENTED / ACCEPTED`；
- G2、G3、Shared Runtime mixed source 和已验收但混合的 Runtime implementation 组成 `PRESERVED DEVELOPMENT BASELINE`，不得被后续开发覆盖或丢失。

最终审计记录：`docs/reviews/CURIS_WORKTREE_CLEANUP_FINAL.md`。

## 目的

这是新会话进入 Curis 产品工作时的唯一导航页。它解决“文档写到了某个
worktree、主线程找不到、旧 Blueprint 被重新引用”的问题。

## TRUTH ROUTER — 所有 Agent 必须先选路径

本文件是路由入口，不是产品定义本身，也不是历史链接的替代品。先判断任务需要哪一种 Truth：

### I NEED CURRENT PRODUCT TRUTH

按顺序读取：

1. `docs/01_Product/Curis_Product_Blueprint.html`
2. `docs/01_Product/Curis_Product_Master_Map.md`
3. `docs/01_Product/Curis_Product_UI_Blueprint.html`
4. 适用的 `docs/07_Decisions/` 与其他 `Status: Frozen` Authority

### I NEED IMPLEMENTATION TRUTH

按顺序读取：

1. `docs/00_Context/CURRENT_STATE.md`
2. 当前正式 Issue / Allowed Files
3. 当前 Accepted Review
4. Current Runtime / Code / Test / Browser / Desktop / Database Evidence

### I NEED TO KNOW WHY

读取被明确点名的 Research、Exploration、Review、Recovery Audit 或 Decision Evidence。研究解释为什么，但不覆盖 Current Authority。

### I NEED HISTORY

读取 `docs/99_Archive/` 或被明确点名的历史快照。Archive / History 不能作为普通 Product、UI 或 Development 任务的 Current Authority。

**硬规则：** 搜索、RAG 或语义检索命中任何文档后，必须先确认其 `Authority Class` 与 `Status / Disposition`。发现 Current Authority 之间冲突必须 `STOP / REPORT AUTHORITY CONFLICT`；发现 Product 与 Runtime 不一致必须登记 `PRODUCT → IMPLEMENTATION GAP`，不能自行选择、降级、冒充或补造第三种真相。

## 唯一文档位置

所有当前产品文档只写入：

`/Users/yy/Documents/Curis AI Workspace/docs/`

`/Users/yy/.codex/worktrees/*` 只可作为受控实现工作树或只读证据来源，不能成为产品真相。
未提交、未登记或只存在于其他 worktree 的文件，不得作为当前产品定义。

文档分类、命名、状态和会话交付格式统一遵守：
`docs/00_Context/PRODUCT_DOCUMENT_MIGRATION_RULES.md`

## Reference Index（已按上方 Truth Router 分层）

### Canonical path cleanup

Current Master Map 与 UI Blueprint 的唯一入口分别是 `docs/01_Product/Curis_Product_Master_Map.md` 与 `docs/01_Product/Curis_Product_UI_Blueprint.html`。仓库中仍出现的旧 `v2.0` / `v1.0` 路径只属于历史迁移记录、旧研究输入或 prototype 覆盖审计；它们不再是 Current Authority，Agent 不得从这些路径读取当前产品定义。

1. 当前事实：`docs/00_Context/CURRENT_STATE.md`
2. 冻结决策：`docs/07_Decisions/` 中 `Status: Frozen` 的文件
   - 产品重定基线：`docs/07_Decisions/ADR-0045-ordinary-user-desktop-product-rebaseline.md`
   - Local Agent Computer Access：`docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`
3. 产品入口：`docs/01_Product/Curis_Product_Context.md`
4. 唯一 Product Blueprint（v5.6、Status: Frozen；CURIS PRODUCT TRUTH — FINAL ACCEPTED；Domain UX / Visual Delta Candidate / Pending）：`docs/01_Product/Curis_Product_Blueprint.html`
   - Product Blueprint 是唯一 Product Authority；产品模型变化必须先写入这里。
5. Blueprint 升级审计工作稿：`docs/01_Product/Product_Blueprint_Upgrade_Audit.md`
6. 当前产品母版（v3.2、Frozen；CURIS PRODUCT TRUTH — FINAL ACCEPTED；Domain UX / Visual Delta Candidate / Pending；canonical path）：`docs/01_Product/Curis_Product_Master_Map.md`
   - Master Map 只展开导航、页面、字段、动作、入口和来源，不得反向创造产品规则。
6A. 三文档一致性审计（Accepted — CEO Final Product Truth Frozen）：`docs/01_Product/THREE-DOCUMENT_CONSISTENCY_AUDIT_2026-08-18.md`
   - 只审计当前三份 Current Truth；历史多轮快照已归档，不作为当前阅读入口。
6B. CEO Operating Core Recovery Audit（已接受登记）：`docs/01_Product/CEO_OPERATING_CORE_RECOVERY_AUDIT_2026-08-18.md`
   - `ACCEPTED — CEO OPERATING CORE RECOVERY BASELINE`；已被三份 Current Truth 消费，不是 Product Authority，不覆盖三份 Current Blueprint。
   - 已消费两项 CEO Confirmed Product Delta：Business Exit Lifecycle 与 CEO Operating Day Cross-day Continuity；不授权新页面、Runtime Primitive 或 Schema。
   - Data Insights + Business Analysis → 经营洞察 / Operating Intelligence 已消费为第七个一级产品空间；页面 IA / UX 消费已接受的 Operating Intelligence UX Baseline。Company Map Variant A / Department Container 已消费为产品 / 交互方向，非 Visual Design Authority。
6C. Leadership / Responsibility Assignment Product Delta（2026-08-19，已由 Final Product Truth 接受）：Leader 不是 Employee Type；Department / Business / Workspace Leader 由 `Employee × Role × Scope` Assignment 承载；Conversation 按 Assignment 隔离；Workflow Result 回到 Workspace Leader 并进入下一 Operating Cycle。Runtime 事实按 CURRENT_STATE 的 Implementation Truth 分层消费。
6D. Operating Hierarchy × Team Operating Engine Reconciliation（2026-08-20，Accepted / Frozen；2026-08-21 Multi-Surface reconciliation）：固定 `Company → Department → Business → Workspace → Team / Responsibility Assignment / Employee Workstations`；Business 至少拥有一个 Workspace，Business 页面只做 Workspace Directory / Portfolio 与聚合管理，Professional Workspace 采用 Workspace-local Domain Navigation + one or more Professional Surfaces + Shared Team Operating + Shared Employee Work Area；Workspace-scoped Responsibility Routing / Team Operating Runtime Truth 已接受并仅作为 Implementation Truth 消费，Business-scope Provider Execution、External live provider quality/cost、完整 RD/XHS migration 与 cross-layer automatic Leader escalation 仍为实现边界。
6E. Canonical Business Spine（2026-08-20，CEO Accepted / Implementation Authorized）：Business 是唯一 canonical persisted identity；`business_directions` 为 Strategy / Direction supporting object，Project 为 legacy compatibility object；`Company → Department → Business → Workspace`、原子 Business + First Workspace、`UNRESOLVED → QUARANTINED` 与 `Workspace → Business → Department → Company` Parent Resolver 已冻结为实现合同。主开发为 Frontend Baseline Promotion Integration Owner；正式实现入口为 `issues/20260820_canonical_business_spine_implementation_001.md`，Authority Review 为 `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_AUTHORITY_REVIEW.md`。实现未完成，不得以 UI 或旧 relation 冒充完成。
7. 页面地图（Review）：`docs/01_Product/Curis_Product_Page_Map_v1.0.md`
8. 产品重新推导：`docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md`
9. 人才与能力产品地图（历史文件名保留）：`docs/01_Product/Curis_Talent_Market_Product_Map.md`
10. 人才与能力集成契约（历史文件名保留）：`docs/01_Product/Curis_Talent_Market_Integration_Contract.md`
11. 人才与能力资源审计（历史文件名保留）：`docs/01_Product/Curis_Talent_Market_Resource_Audit.md`
12. 人才库扩充报告：`docs/01_Product/Talent_Library_Expansion_Report.md`
13. AI 能力现状审计（Review）：`docs/01_Product/AI_Capability_Current_State_Audit.md`
14. Model Provider Registry（Review）：`docs/01_Product/Model_Provider_Registry.md`
15. Skill / Expert Registry（Review）：`docs/01_Product/Skill_Expert_Registry.md`
16. MCP / Connector Registry（Review）：`docs/01_Product/MCP_Connector_Registry.md`
17. Agent Adapter Compatibility Registry（Review；Computer Access 动态事实）：`docs/01_Product/Agent_Adapter_Compatibility_Registry.md`
18. Agent Adapter Contract（Review；§3 Computer Access 由 ADR-0046 冻结）：`docs/01_Product/Agent_Adapter_Contract.md`
19. AI Capability UI Contract（Review；§5.6 Computer Access 由 ADR-0046 冻结）：`docs/01_Product/AI_Capability_UI_Contract.md`
20. AI 能力接入报告（Review）：`docs/01_Product/AI_Capability_Integration_Report.md`
21. Agent Computer Access Runtime Delta Plan（Review；只规划）：`docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`
22. Local Agent Computer Access Research（Deprecated；Review Record / Reference）：`docs/01_Product/Curis_Local_Agent_Computer_Access_Research.md`
23. Agent Computer Access Contract Candidate（Deprecated；Review Record / Reference）：`docs/01_Product/Curis_Agent_Computer_Access_Contract_Candidate.md`
24. Agent Adapter Permission Mapping Matrix（Deprecated；Review Record / Reference）：`docs/01_Product/Agent_Adapter_Permission_Mapping_Matrix.md`
25. 当前实现偏航审计：`docs/reviews/20260813_current_state_product_drift_audit/Curis_Current_State_and_Product_Drift_Audit.md`
26. 开发队列：`docs/01_Product/Curis_Product_Development_Queue_Pack.md`
27. 旧页面交互包（辅助）：`docs/01_Product/Curis_Product_UI_Flow_Pack.html`
28. 视觉总图（v3.0、结构检查工具）：`docs/01_Product/Curis_Product_Visual_Master_Map_v1.0.html`
29. 变更记录：`docs/08_Change_Log/CHANGE_LOG.md`
30. XHS Workspace Instance v1 实现验收：Issue
    `issues/XHS-WORKSPACE-INSTANCE-001.md`（`IMPLEMENTED / ACCEPTED`）；正式记录
    `reviews/XHS-WORKSPACE-INSTANCE-001_review.md`
31. Agent Computer Access Runtime P0 验收：Issue
    `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`（`IMPLEMENTED / ACCEPTED`）；正式记录
    `reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md`
32. Company OS Shared Authority（Frozen / APPROVED · 2026-08-16，FINAL REVIEW 确认；2026-08-20 Operating Hierarchy sync）：`docs/03_Design/Curis_Company_OS_Shared_Authority.md`（⑥ Responsibility Requirement / ⑧ Shared Employee Service Relation / ⑦ Organization Routing + Context Isolation Truth Boundary；**§9 长期 Workspace = Operating Team + Professional Workspace**，Business 聚合同类 Workspace、Workspace 为独立经营空间；每个长期 Workspace 必须有真实团队承载，Business 可聚合多个独立 Workspace 且不要求共享 Team；Department / Business / Workspace Leader 统一为普通 Employee 的 Responsibility Scope，Leader Workstation 与组织结构分层承载；该规则仅约束长期 Workspace 终态且渐进工作形态保留，空间工程可委托非唯一入口**；⑨ Lightweight Queue/Bottleneck 保持 APPROVED SHARED CANDIDATE，未 Frozen）
33. Content Growth Domain Authority（Frozen / APPROVED · 2026-08-16，CEO identity reconciliation 2026-08-24）：`docs/03_Design/Curis_Content_Growth_Domain_Authority.md`（① Workspace canonical identity；Office 仅历史 / implementation / migration provenance / legacy binding 名称；② Channel·Channel Account·legacy OfficeAccountBinding·Account Pool / ③ Content Opportunity·Intent / ④ Target Account Set / ⑤ Content Variant·Publication / Distribution Execution Policy（④ 唯一定义）/ Capability Truth boundary（§5）；Content Growth 为 Professional Workspace Candidate，CEO Operating Result 为 Domain-scoped default selected Surface / projection；具体平台 API·OAuth Scope·scheduling·ratio·duration 不 Frozen，下放 Capability Registry / Channel Facts；Operating Context 仍为 RESERVED/DEFERRED CANDIDATE）
34. Workspace Engineering Methodology Set（Review / APPROVED CANDIDATE；其引用的 Company OS Shared Authority §9 已于本次 Review 批准 Frozen）：`docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md`、`docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md`、`docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Gates_and_Acceptance.md`、`docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Expert_Handoff_Protocol.md`、`docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Content_Growth_Case_Study.md`、`docs/05_Workspace_Engineering/Curis_RD_Methodology_Gap_Review.md`
35. Workspace Engineering Runtime / Extensibility Audit（Review；当前事实）：`docs/02_Architecture/WORKSPACE_ENGINEERING_RUNTIME_AND_EXTENSIBILITY_AUDIT.md`
36. Workspace Package Technical Proposal（Review / TECHNICAL DIRECTION APPROVED CANDIDATE）：`docs/02_Architecture/WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`
37. Workspace Engineering P0 Definition（Review / P0 DEFINED）：`docs/02_Architecture/WORKSPACE_ENGINEERING_P0_DEFINITION.md`
38. Workspace Engineering P0 Implementation Plan（Review / IMPLEMENTED / ACCEPTED）：`docs/04_Development/WORKSPACE_ENGINEERING_P0_IMPLEMENTATION_PLAN.md`
39. Workspace Engineering P0 验收：Issue `issues/WORKSPACE-ENGINEERING-P0-001.md`（`IMPLEMENTED / ACCEPTED`）；正式记录 `reviews/WORKSPACE-ENGINEERING-P0-001_review.md`；Desktop 证据 `docs/reviews/workspace-engineering-p0-2026-08-16/README.md`
40. Workspace Engineering 端到端验收契约（Frozen）：`docs/02_Architecture/WORKSPACE_ENGINEERING_END_TO_END_ACCEPTANCE_CONTRACT.md`（统一标准 `Installed → Operational → Company Integrated → Operating → Evolvable`；P0.5 已验收至 Operating，不实现 Evolution）
41. Workspace Engineering P0.5 Company OS Integration Audit（Frozen / IMPLEMENTED / ACCEPTED）：`docs/02_Architecture/WORKSPACE_ENGINEERING_P05_COMPANY_INTEGRATION_AUDIT.md`（保留 P0 gap baseline，并登记真实 Core 引用、Company Integration / Operating closure）
42. Workspace Package ↔ Company OS Identity / Reference Contract（Frozen for P0.5）：`docs/02_Architecture/WORKSPACE_PACKAGE_COMPANY_OS_IDENTITY_REFERENCE_CONTRACT.md`（同一 object ID、Core 可解析关系、scope/type/lifecycle fail-closed；不修改既有 Frozen Authority）
43. Workspace Engineering P0.5 Implementation Issue：`issues/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001.md`（`IMPLEMENTED / ACCEPTED`；Handoff/P7、update/Marketplace/Evolution 明确排除）
44. Workspace Engineering P0.5 验收：正式记录 `reviews/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001_review.md`；packaged Desktop / restart / failure / SQLite 证据 `docs/reviews/workspace-engineering-p05-2026-08-16/README.md`
44A. Workspace Engineering Evolvable / Lifecycle Gap Audit（Review）：`docs/02_Architecture/WORKSPACE_ENGINEERING_EVOLVABLE_GAP_AUDIT.md`（schema-stable lifecycle substrate accepted；real migration / Team continuity / general rollback 仍为 Gap；`EVOLVABLE NOT ACCEPTED`）
44B. Workspace Engineering P1 Package Lifecycle：Issue `issues/WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001.md`（schema-stable substrate `IMPLEMENTED / ACCEPTED`）；Review `reviews/WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001_review.md`；Desktop 证据 `docs/reviews/workspace-engineering-p1-lifecycle-2026-08-17/README.md`
44C. Workspace Engineering P1.5 Transactional Migration：Audit `docs/02_Architecture/WORKSPACE_ENGINEERING_P15_TRANSACTIONAL_MIGRATION_AUDIT.md`；Issue `issues/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001.md`；Review `reviews/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001_review.md`；Desktop 证据 `docs/reviews/workspace-engineering-p15-migration-2026-08-17/README.md`（仅 reversible Package-owned JSON field rename + atomic recovery `IMPLEMENTED / ACCEPTED`；Operating Team continuity / general or irreversible migration / Full Evolvable 未验收）
45. Workspace Shell Contract & Shared Pattern（Frozen · **唯一 Shared 真源** · S1–S7 + P1–P7 + Delta-S1/S2/S3（2026-08-16）+ Delta-X9 Shared Main Composition（2026-08-17）+ Delta-X10 Shared Employee Work Area + Composer（2026-08-17）+ Delta-X12 Shared Conversation Content Block（2026-08-17）已回写）：`docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Layer 0–3：四独立 Pane + Adaptive Surface + 7 Shared Pattern + Employee Workstation/Detail/UI Status 投影/Presence；Main = Domain Business Surface + 工作区；Employee Workstation ∈ Main.WorkArea；工作区 = Employee Workstation List，编排不与 Runtime 绑定；含 Shared Employee UI Status 投影（空闲/工作中·<desc>/阻塞·<cause>）、Conversation Surface、长内容块 bounded embedded、Shared Composer Shell、Model/Agent-backed Provider 适配；§1.1 / §1.3 已完成七区 Navigation Authority Sync，与 Current Product Truth 一致）原 #48 已合并至本条目）
46. Shared Business Workspace Main Composition Closure（APPROVED · 已回写 Frozen Delta-X9 · 2026-08-17）：`docs/03_Design/CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md`（为 Shared Employee Workstation Pattern Closure 的超集扩展；Main = 业务展示区 + 工作区 Shared 规则；不建 P8、不改 P1–P7、不重定义 Workstation）**（历史审批证据 · 退出新 Agent 必读集合；规则已回写 #45 Frozen Shell Contract）**
47. Shared Employee Work Area + Composer Contract Closure（APPROVED · 修正 3 点 · 已回写 Frozen Delta-X10 · 2026-08-17）：`docs/03_Design/CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md`（固定所有 Business Workspace 共用的「工作区」+「Composer Shared Shell」：Employee Row 两行结构（点头像/姓名→Utility，无详情按钮）/ Shared Employee UI Status = Runtime Truth 投影（空闲·工作中·<desc>·阻塞·<cause>，不动 Runtime State Schema、不新增 Primitive）/ Conversation Surface 居中·自适应·可拖拽 / Composer 固定语义槽位（布局仅 Desktop 推荐）+ Provider Adaptation（Model-backed vs Agent-backed）；已据本 Closure 重制 Workspace Engineering 高保真最后一轮）**（历史审批证据 · 退出新 Agent 必读集合；规则已回写 #45 Frozen Shell Contract）**
48. → 已合并至 #45（Workspace Shell Contract & Shared Pattern · Frozen）。本条目保留为历史索引，不再作为独立权威入口；所有 Delta（X9/X10/X12）与 Shared 规则均见 #45。
48A. Pre-Design-Research Product Structure Baseline（Current / Product Structure Authority；结构记录，视觉未批准）：`docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`（Product Design Research、Final UI Master、Frontend Reconciliation 必读；七区、Company OS、原装组织、Employee、Business/Workspace、Four-Pane、Conversation、CEO Assistant、Meeting、资料库、经营洞察与 canonical scope 的共同结构输入）
49. Current UI Blueprint（唯一 UI Blueprint · Status: Frozen · CURIS PRODUCT TRUTH — FINAL ACCEPTED；Domain UX / Visual Delta Candidate / Pending）：`docs/01_Product/Curis_Product_UI_Blueprint.html`（消费 Product Blueprint 5.6 / Master Map 3.2；消费 Frozen Workspace Shell Contract、Frozen Design System 与 Operating Intelligence UX Baseline；只定义空间、IA 与交互表达，不反向修改产品模型）
49A. App Entry UI Acceptance（Frozen；UI Accepted / Figma Current Design Baseline；Implementation Pending）：`docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md`（Figma `2Fh7DgPPfLgdbvNtnzPnk9`，13 个登记 Core Frames；统一 Welcome、Empty Curis、CEO Identity、Assistant Conversation / Composer、Model Management / Selector 与 Empty State 共享模式；不代表 Frontend / Runtime / Schema 已实现）
49B. CEO Desk Operating UI Acceptance（Frozen；UI Accepted / Current Operating Design Baseline；Implementation Pending）：`docs/reviews/CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md`（Figma `69:3`；1440 × 900 Light；Operating / Matters Present；其他状态仅作 Adaptation / Validation；不代表 Frontend / Runtime 已实现）
49C. Frontend Batch 1 Implementation Acceptance（Frozen；Implemented / Accepted with Recorded Boundaries）：`docs/reviews/CURIS_V1_FRONTEND_BATCH_1_IMPLEMENTATION_ACCEPTANCE.md`（证据见 `CURIS_V1_FRONTEND_BATCH_1_FINAL_ACCEPTANCE.md`；Batch 1 主链已通过 Browser / packaged Desktop / restart；Conversation、Composer、Model Selector、Avatar、General Workspace 完整运行与 M3 Keychain 边界按记录消费；不等于 V1 / Frontend 完成）
49D. Whole-App Live AI Acceptance Registration（Frozen；Implemented / Accepted with Recorded P1）：`docs/reviews/CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE_REGISTRATION.md`（Product Gap Closure 已证明 packaged CEO/Company→Business/Workspace→Employee/Responsibility→Work→real AI→Result/Evidence/Artifact→P7→automatic resume→restart→post-restart AI；下一分发 Gate 为 GitHub Beta Distribution Closure）
49E. Distribution Strategy（Frozen；CEO Accepted）：`docs/reviews/CURIS_V1_DISTRIBUTION_STRATEGY.md`（Stage A = GitHub Beta Distribution；Stage B Trusted macOS Distribution 延后；下一 Gate 为 GitHub Beta Distribution Closure）
50. Operating Intelligence UX Baseline（**ACCEPTED / FROZEN — CONSUMED BY FINAL PRODUCT ARCHITECTURE DELTA** · 2026-08-18 CEO FINAL ACCEPTANCE · 非 Runtime/Schema Authority）：研究交付位于 `deliverables/`，不写入 `docs/` 产品真源。五轮研究（产品研究 / Analytics UX / Analyst Organization / Data Visualization Research / UX Consolidation + FINAL CLEANUP）已收口，两个产物登记为 **ACCEPTED — OPERATING INTELLIGENCE UX BASELINE**：
  - `deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_UX_CONSOLIDATION.md`（短整合说明，含 18 项冻结产品结论索引）
  - `deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html`（完整 Consolidated UX 交互探索，DEMO DATA）
  - 上游研究稿：`CURIS_OPERATING_INTELLIGENCE_RESEARCH.md`（26 节）、`CURIS_OPERATING_INTELLIGENCE_UX_RESEARCH.md`、`CURIS_OPERATING_INTELLIGENCE_VISUALIZATION_RESEARCH.md`（三条 Product Delta A/B/C 已登记）。本 Baseline 已由 **FINAL PRODUCT ARCHITECTURE DELTA** 统一消费进入 Product Blueprint / Master Map / UI Blueprint / Global Navigation 合同，并与 Company Map / Business Exit Lifecycle / CEO Operating Day Cross-day Continuity 一并收口；不改变 Frozen Shell、Runtime、Schema 或代码。
50A. Operating Intelligence UI Acceptance（Frozen；Product / UX / UI Accepted；Implementation Pending）：`docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_UI_ACCEPTANCE.md`。Figma `172:3 / 172:277 / 172:551 / 172:825`（1440 × 900 Light）是当前 UI Design Baseline，覆盖 Overview、Scoped Business Analysis、Explore / Benchmark、Report / Decision Continuity；无剩余 P1，Prototype wiring、Dark、1024、accessibility/keyboard 与真实 Runtime data-density verification 为 P2。下一 Gate 为 `OPERATING INTELLIGENCE PRODUCTIZATION CLOSURE`。
50B. Operating Intelligence Implementation Acceptance（Frozen；Implemented / Accepted）：`docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_IMPLEMENTATION_ACCEPTANCE.md`。canonical analytical projection、7/30 天与 Business scoped analysis、同口径比较、Unknown/provenance/freshness、Artifact-backed Report、canonical P7 Decision continuity、Browser、fresh packaged Desktop、同根 restart/persistence、focused/regression tests、build/package 与 active SQLite safety 均已验证。外部 Outcome/Feedback Connector 与自动分析报告 authoring 保持 bounded gap；下一 Product Completion area 为 `TALENT & CAPABILITY PRODUCTIZATION CLOSURE`。

51. Repository-wide Truth Governance：本 Pointer、根 `AGENTS.md`、`CURRENT_STATE.md`、Current 三份产品文档、Current Consistency Audit 与 `docs/99_Archive/Product/` 共同执行 Current / Implementation / Research / History 分层；历史入口只作追溯，不能覆盖 Current。

52. CEO Desk Page Contract Review Candidate（Review；`ACCEPTED CANDIDATE — READY FOR CROSS-PAGE REVIEW`；非 Product Authority）：`docs/reviews/CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md`。只消费当前三份 Frozen Product Truth、Frozen Shell 与 CEO Decision Package Pattern，定义 CEO 工作台的入口、信息职责、Matters、Decision、Result、跨日连续性、状态、返回和跨页边界；仍需 Approved Design 与正式 Issue 才能开发。

53. Business Space Page Contract Review Candidate（Review；CEO Operating Work Directory decision applied；`FINAL REVIEW REQUIRED`；非 Product Authority）：`docs/reviews/BUSINESS_SPACE_PAGE_CONTRACT_FINAL_REVIEW.md`。定义同一 Company Truth 下的 [部门] / [业务] / [工作空间] 三个直接入口、Department Work Surface、Business Work Surface、独立 Workspace、Operating Model、Staffing、Result、External Object、Create / Duplicate / Exit、状态和跨页边界；不创建第二个业务整体页面，CEO 最终接受前不得作为 UI 或开发授权。

54. Business × Office Product Clarification（Deprecated；`CEO REJECTED / SUPERSEDED BY BUSINESS × OFFICE MODEL`）：`docs/reviews/BUSINESS_ACCOUNT_WORKSPACE_PRODUCT_CLARIFICATION.md`。旧 Business-level Workspace + Account Scope 推荐仅保留为历史推导记录；该文档不再提供当前 Company → Department → Business → Workspace 入口，也未授权任何 Runtime / Schema / Code。
55. Organization Center Page Contract Review Candidate（Review；CEO consolidated hierarchy applied；非 Product Authority）：`docs/reviews/ORGANIZATION_CENTER_PAGE_CONTRACT_FINAL_REVIEW.md`。消费 Company Map Variant A / Department Container 与当前 Business × Workspace Truth，定义公司版图、员工目录、Department / Business / Workspace / Role / Staffing / Leader Scope 展开、空岗、结果、Focus、Search、Reverse Entry 与 Source Boundary；Organization Center 只负责结构与行政，Leader Workstation 属于 Business Space Work Surface；Role canonical ownership 已由 Responsibility Scope 取代，未授权 Runtime / Schema / Code。
55A. Organization Center UI / Implementation Acceptance（Frozen；UI ACCEPTED / IMPLEMENTED / ACCEPTED）：`docs/reviews/CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md`。Figma file key `2Fh7DgPPfLgdbvNtnzPnk9` frames `106:3`（公司版图 / Default）、`106:230`（Company Map / Business Focus）、`106:457`（员工目录 / Default）是 1440 × 900 Light Current Design Baseline；组织中心固定为公司版图 / 员工目录双 Tab，canonical organization projection、Browser、fresh packaged Desktop 与 restart/persistence 已验证。Dark、1024、无障碍、Search / Filter wiring 与 legacy cleanup 保持 P2。
56. Department Work Surface Shared Management Surface Contract Candidate（Review；非 Product Authority）：`docs/reviews/DEPARTMENT_WORK_SURFACE_PAGE_CONTRACT.md`。定义跨 Domain 共享的 Department Leader 管理骨架、Business Portfolio、资源、Handoff、Exception、Decision Request、Follow-up、入口/返回、状态与 Organization Center 边界；Department 不提供专业 Workflow Builder，具体业务规则、标准、Workflow 与 Role Structure 进入 Business Work Surface；Leader 是普通 Employee，不创建新 Employee 类型或 Runtime Primitive。内容增长部、研发部、小红书运营与 Curis 产品研发的最终 Domain-specific Operating Surface 需另行 UX Exploration。
57. Business Work Surface Final Structure Contract（Review；非 Product Authority）：`docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md`。定义 Business Definition → Operating Status → Workspace Directory → Business Team 的连续结构；Business 只共享 Business Introduction、Business-level Goal / Direction、通用 Rules / Configuration，不拥有统一团队运转；每个 Workspace 自己拥有团队运转、Role / Responsibility Assignment、Operating State 与 Result，Business 页面只提供目录 / 聚合投影与直接进入入口；Workspace 资源投影与 Employee Workstation 实际能力边界、Conversation-driven Truth、Definition ≠ Execution、Preset / Generic 边界与专业 Workspace 不重做规则已登记。具体 UX Visual Delta 与 Generic Workspace 需后续 Review。

当前产品方向已由 2026-08-14 的 ADR-0045、Master Map 3.0、Page Map、产品重新推导和偏航审计重构：
普通用户体验优先，七个主工作区域（含经营洞察），人才与能力内的 Market / Discover 承担能力发现，Workspace 是可内嵌成熟
AI 产品的独立数字办公室，Runtime 下沉为可靠性支撑。ADR-0045 已冻结方向；Master Map 和
Page Map 是该方向的产品展开，结论已回写至唯一 Blueprint v5.6。不得创建 Blueprint v2，
也不得用旧总装配包或旧页面包单独派发开发。

旧总装配包、旧页面交互包和旧开发队列保留为迁移辅助；当前开发顺序以 Master Map 与新的开发队列为准。
如果 Review 文档与 Frozen 决策冲突，以权威链为准，并建立修正记录。

## 产品主线程与三文档唯一维护者

- Product Architecture / Blueprint / Master Map / UI Blueprint 唯一维护者：本当前产品架构会话（由 CEO 显式接管）
- 历史产品架构线程：`019fb777-69e0-71f2-9af5-a043d0f8e5c8`（只保留历史上下文，不再独立写入三份 Current 文档）
- 主开发 / 交付线程：`019ff1ba-f696-7002-8a6c-2b357ded819c`

新产品讨论先回到产品架构线程；形成明确产品决定后，才进入开发队列并交给主开发。
体验研究只提交证据和候选机制，不直接改 Blueprint 或派发代码任务。

## 工作树纪律

- 产品文档、Blueprint、页面地图和开发队列不得只写入 worktree。
- 开发 worktree 的回交必须带 Issue、Allowed Files、Review、真实证据和目标文件路径。
- 未回交的 dirty 文件、数据库、密钥、构建产物和旧 UI 不自动迁入主目录。
- 受控迁移后，必须在本文件、CURRENT_STATE 和 CHANGE_LOG 中记录来源与取舍。

## 本次收敛事实

2026-08-18 已完成三文档 Authority Consolidation；2026-08-14 的主目录专项仍作为输入：

- Master Map 3.0（原 v2.0 文件原位升级）：确定产品模型、页面字段/动作/入口和 Workspace 契约
- Page Map：确定页面层级、壳层、检查器、返回和状态处理
- 人才与能力专项（历史文件名保留）：确定发现、招聘、组队、Skill/Connector 与设置的边界
- 当前实现审计：确认现状仍是 Runtime 工作台骨架，产品主循环尚未闭合
- 新开发队列：按首个可感知价值、CEO 工作台和独立 Workspace 结果链排序

Master Map、Page Map、人才与能力和三文档审计处于 Review 展开态；研发工作台只定义通用空间，具体研发任务由 CEO 创建。

## 三文档永久维护规则

```text
Product Blueprint（唯一 Product Authority）
→ Product Master Map（结构化/可视化展开，不是第二 Authority）
→ UI Blueprint（UI/IA 消费方，不得静默改变 Product Model）
```

- 三份文档独立存在，由同一 Product Architecture Owner 统一维护。
- 每次产品模型变化先更新 Blueprint，再同步 Master Map，最后同步 UI Blueprint。
- HTML Visual Master Map 只用于结构检查，不是第四份产品真相；高保真设计不得改变模型。
- 旧批准/冻结规则没有正式 Supersede 记录前，不得静默删除；冲突必须标记 \`REVIEW REQUIRED\`。

2026-08-16 Workspace Engineering 已完成 Methodology × Technical Closure 候选对齐：Package First、Relevant Gate 不可跳但 Lifecycle 不机械全跑、Semantic Model Before Instance。该闭环与技术方向均为 `APPROVED CANDIDATE / Review`，不是 Frozen Runtime Authority。首个受控 Declarative Workspace Package substrate 已通过真实 build-before-Package Desktop PoC，状态为 `WORKSPACE ENGINEERING P0 ACCEPTED`；P0.5 进一步以同一动态 Package 证明真实 Responsibility / Employee / Capability / Task / Execution / Evidence / Result、成功/失败反馈与完整 Desktop restart，最高验收层为 `Operating`。2026-08-17 P1 又接受了仅限 schema-identical 的本地升级/回滚 substrate；真实 schema/data migration、Operating Team continuity、general rollback 和完整 `Evolvable` 仍未实现/未验收。该结论不扩展到 arbitrary extension、Marketplace/update distribution、XHS/RD/TTK migration 或 Workspace Engineering product/UX。

## 设计文档路由（Design Agent · 2026-08-17 收敛）

> 本段为设计 Agent（含 Figma / 外部设计 Agent / 未来 Design Agent）提供明确路由。所有 Workspace Shared 规则的唯一真源是 Frozen `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（权威链 #45）。

### A. 新 Agent 必读最小集（Minimum Design Agent Reading Set）
1. **入口**：`PRODUCT_DOCUMENT_POINTER.md`（本文件）
2. **唯一 Shared 真源（Frozen）**：`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（#45）
3. **跨业务语义（Frozen）**：`Curis_Company_OS_Shared_Authority.md`
4. **视觉语言基线（Frozen）**：`docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`（Direction D / `#806BE5` / Neutral Foundation）。旧 `Curis_Design_System.md` 与 `Curis_UI_Frozen_Spec_2026-08-04.md` 仅在未被新标准 supersede 的结构、可访问性与实现兼容部分继续参考；`#32f08c` 品牌 accent 条款已由新标准取代。实现迁移只按 `docs/reviews/CURIS_VISUAL_TOKEN_MIGRATION_MAP.md` 规划，未授权执行。
5. **UI 结构消费方（Review）**：`Curis_Product_UI_Blueprint.html`（唯一 UI Blueprint，#49；只消费 #45，不新增规则）
6. **设计具体业务时只额外增加**：Current Domain Product Translation / Domain Authority

### B. 勿读 / 非必读（Deprecated · Superseded · Historical）
- **DEPRECATED（勿读）**：`Curis_Workspace_Shell.md`（草案「5 槽位」已被 Frozen Shell Contract 取代；属 Layer 4 运营变体，非权威）
- **SUPERSEDED（勿读）**：`WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md`（已被 Final IA Closure 收口替代）
- **SUPERSEDED-for-Shared-UI（勿读其 UI 规则）**：`WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`（其 Main / Context / Workstation / Conversation / Composer / Employee UI 布局规则已被 Frozen Shell Delta-X9 / X10 / X12 取代；新 Agent 不得从中消费 Shared UI 规则，须以 #45 为准；仅保留 Workspace Engineering 自身 History / Asset / Config / Retention Domain IA 证据价值，供专项参考）
- **HISTORICAL（非必读）**：`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md`（高保真重制过程记录）；`CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md`（#46）、`CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md`（#47）— 均为历史审批证据，规则已回写 #45 Frozen Shell Contract，新 Agent 无需必读
- **NOT AUTHORITY**：任何旧原型 HTML（如 `Curis_Workspace_Engineering_High_Fidelity_Remake.html`、`Curis_UI_Blueprint_Prototype.html`）仅作 **VISUAL QUALITY REFERENCE — NOT AUTHORITY**

### C. External Design Agent Handoff Set（Figma / 外部设计 Agent 默认只上传这套）
1. **Current Product Blueprint** — `docs/01_Product/Curis_Product_Blueprint.html`（v5.6 · Status: Frozen · CURIS PRODUCT TRUTH — FINAL ACCEPTED）
2. **Current UI Blueprint** — `docs/01_Product/Curis_Product_UI_Blueprint.html`（唯一 UI Blueprint · Status: Frozen · CURIS PRODUCT TRUTH — FINAL ACCEPTED；Domain UX / Visual Delta Candidate / Pending）
3. **Frozen Workspace Shell Contract / Shared Patterns** — `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen）
4. **Current Visual Language** — `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`（Frozen / CEO Selected D）；`docs/03_Design/Curis_Design_System.md` 与 `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` 的旧视觉语言/品牌 accent 条款为 Superseded，未被取代的实现兼容规则仍可参考。
5. **Visual Token Migration Map** — `docs/reviews/CURIS_VISUAL_TOKEN_MIGRATION_MAP.md`（Review；只规定迁移顺序，不执行代码迁移）

> **Trae qualification core input（仅资格测试）**：Trae 只读取 `docs/reviews/CURIS_MASTER_SHELL_VISUAL_EXECUTION_CONTRACT.md` 与 `docs/03_Design/CURIS_TRAE_VISUAL_DESIGN_RULES.md`。上述 Product/UI/Shell/Visual Standard 文件由资格测试编排方预先收敛，不要求 Trae自行重建产品或视觉方向。

> 设计具体业务时只额外增加：**Current Domain Product Translation / Domain Authority**。
> 旧原型只能作为 **VISUAL QUALITY REFERENCE — NOT AUTHORITY**。

## 2026-10-05 — bounded built-in Writing definition decision source

Status: Review · Authority Class: REVIEW / CEO DECISION PROVENANCE ROUTE. CEO明确批准精确com.curis.local.writing-authoring 0.1.0限定本地Book/Chapter编辑、人工Formal与LOCAL_DOWNLOAD合同及来源/维护/不可变版本政策。唯一登记为[Writing Review新增决定节](../reviews/CURIS_V1_DELIVERY_WRITING_CHAPTER_REVIEW.md#2026-10-05--ceo-bounded-built-in-writing-definition-publication-decision)。此指针不新建Catalog Authority，不覆盖Blueprint/Shared19，不表示入口/真实模型/native/fullWriting/fullApp已经Accepted。实施走[正式Issue](../../issues/CURIS-V1-WRITING-PRODUCT-ENTRY-001.md)与R02 bounded Approved Design；[Current State](CURRENT_STATE.md)记录实际gap。真实模型费用/系统、隔离tests/build、native及Release保持独立Gate。


## 2026-10-05 — Writing entry isolated implementation return, NOT ACCEPTED

Status: Review · Authority Class: EVIDENCE / IMPLEMENTATION BOUNDARY. Disposition: REVIEW_REQUIRED.
[Actual implementation Review](../reviews/CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md) and formal Issue CURIS-V1-WRITING-PRODUCT-ENTRY-001 retain the CEO-approved bounded definition, original local acceptance and history. Owner subsequently granted exact fresh isolated validation roots/ports; backend final40 /39PASS/1FAIL, frontend11PASS/scoped lint/build2 PASS; Browser first-instance authoring/CAS and controlled no-outbound UNKNOWN preservation evidenced. This does not accept the product entry, actual Provider/fee/Keychain, native/default App or AppRelease. Second independent Business fails existing workspace_package_instances company/package/version UNIQUE. Owner maintains multi-Business requirement and did not approve Schema implementation; minimum migration design was appended only to existing Task PACKAGE_INSTANCE_GATE.md for CEO decision. No Schema change/migration run or production DB write. Next Gate: CEO/Owner exact migration scope → populated migration evidence → independent QA → Owner final review. Full failures/NOT RUN, source seals and Task Output Manifest are in the Review. This append is evidence routing, not Frozen Product promotion.

## 2026-10-05 — Writing entry authorized schema / lifecycle / return revision

Authority Class: EVIDENCE / IMPLEMENTATION PROVENANCE · Status: Review · Disposition: REVIEW_REQUIRED. CEO “允许” minimum existing-table uniqueness migration; Delivery Owner delegated precise sibling disable/uninstall and WQA20 consumer return decisions, recorded in CURIS-V1-WRITING-PRODUCT-ENTRY-001 amendments01–03 (31→33 exact paths). Low-frequency same-type independent Businesses allowed; multiple Books normally same workspace. No Product/Frozen model promotion.

Actual developer evidence: backend94PASS; frontend13PASS/scopedlint/freshbuild PASS; populated parent-only migration preserves IDs/history/FK and strict rollback/repeat/concurrency, sibling assets retained through last live/disabled reference. Actual model/employee same-window buttons return verified chapter and preserve unsaved text/discussion/selection/UNKNOWN. Physical process boundaries prove precommitUNKNOWN/no replay and committed response-loss idempotency; cross-FS/DB and partial-copy recovery remain bounded risks. Three protected DB bytes equal/integrityok; no Provider/credentials/fees/native/defaultApp/Git.

Old independent QA REPORT SHA12ba4e7bd7a06e60701f19cbc0a990c105e1734a494df59042f690bc7eb89051 accepted by Owner as BOUNDED LOCAL evidence only, old WQA20FAIL/newSchemaNOTVERIFIED/Provider-nativeNOTRUN retained. New developer seal awaits independent QA and Owner acceptance, not Writing/fullAppAccepted. See issues/CURIS-V1-WRITING-PRODUCT-ENTRY-001.md and docs/reviews/CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md plus artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-001/source-seal-schema-01.json, manifest-schema-01.json and HANDOFF_SCHEMA_01.md. Next Gate: new-seal populated migration/sibling/return/boundary independent QA → Owner bounded verdict; remaining product/live/native/release gates unchanged.


## 2026-10-05 — Delivery Owner accepted bounded schema-01 independent QA

Status: Review · Authority Class: REVIEW / IMPLEMENTATION ACCEPTANCE EVIDENCE / OWNER DECISION PROVENANCE.
Verdict / Disposition: BOUNDED_LOCAL_SCHEMA_LIFECYCLE_BROWSER_RETURN_PASS accepted by Delivery Owner; retained bounded evidence, NOT full Writing/App Accepted.
Owner / Decision Source: Curis V1 Delivery Owner, chat 019ff1ba-f696-7002-8a6c-2b357ded819c; CEO delegated bounded decisions.
Next Action / Target Authority: preserve the sealed schema-01 source and independent QA; CG shared-code changes require new baseline/seal and Writing regressions. This append is implementation evidence, not Frozen product promotion.
Next Gate: cross-FS recovery remains PARTIAL; actual Provider/cloud fees/credentials/native NOT RUN and require exact separate grants; full Writing and App release remain open.

Owner independently checked schema-01 REPORT/source-seal/output-manifest, 119 outputs / 33 source hashes / 371 source-copy checks with zero mismatch, protected before/after equality, 11 migration variants, 4 physical process boundaries and actual same-window Model/Employee return evidence. This records the Owner's independent verification, not a new test rerun by this documentation task. The obsolete BLOCKED_SCHEMA_DECISION is historical, not the current blocker. Old WQA20 FAIL, old schema failures/seals/logs and residual assets are preserved unchanged. No QA119 output or physical sealed source was rewritten.

Evidence: artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-QA-001/schema-01/REPORT.md; source-seal.json; output-manifest.json. The three exact SHA256 fingerprints are in the receiving CG task SOURCE_SEAL baseline. Six authorized documentation paths were updated/append-only registered; before/after hashes are explicitly retained there. This does not wash old seal hashes or claim current shared-code hashes still match old sealed physical copies after subsequent CG edits.


## 2026-10-05 — CG first graphic vertical authorized, NOT ACCEPTED

Status: Review · Authority Class: IMPLEMENTATION BOUNDARY / OWNER DECISION PROVENANCE · Disposition: REVIEW_REQUIRED.
Delivery Owner accepted CG readiness as implementation input and R03 DESIGN_HANDOFF §8 as bounded Approved Design, then granted exact27 paths/owned functions after Writing schema-01 independent QA closure. Formal Issue: issues/CURIS-V1-CG-PRODUCT-ENTRY-001.md; actual review: docs/reviews/CURIS_V1_CG_PRODUCT_ENTRY_REVIEW.md; Task baseline: artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/SOURCE_SEAL.json.

Implementation IN PROGRESS / NOT ACCEPTED. Existing canonical CONTENT_ITEM/CONTENT_VERSION/Shared Task/Conversation/Identity/singleUsage are reused; bounded Package binding, atomicCAS and manualadopt without Review→SCHEDULED, purpose dispatch and readonly originalquery/UNKNOWNnoReplay are authorized. Candidate definition is no-publication; ordinary published activation, actualcloud/fees/credentials/native/defaultApp not authorized. Isolated focused/regression/build/Browser roots and ports only perIssue. FullCG fourformats/perAccount publication/receipts/analytics/review/nextcycle remain open in these existing backlogs, not removed by firstgraphic.

Owner/NextAction: Delivery Owner receives sealed matching evidence and independentQA; nextGate bounded actual implementation/test/Browser review, separate exact publication/live/native decisions. This append does not promote Product/Frozen or Accepted.


## 2026-10-05 — Exact28 bounded implementation handoff, review required

Status: Review. Authority Class: REVIEW / IMPLEMENTATION EVIDENCE. Disposition: REVIEW_REQUIRED.
Verdict: BOUNDED_IMPLEMENTATION_AND_CONTROLLED_REGRESSION_PASS / BROWSER_PARTIAL / NOT_ACCEPTED / DEFINITION_UNPUBLISHED.
Actual CG source28 is sealed in artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/SOURCE_SEAL.json; exact handoff/owned diff/output manifest share that area. Focused21 PASS; combined backend110 PASS; frontend17 PASS; lint/syntax/production build PASS; protected3 DB exact fingerprints unchanged and read-only integrity ok. Real Browser saved/manualcandidate/adoptedVersion, model return, old selection read-only, original UNKNOWN/list priority/cross-content lock verified. Query events8->8, Task0->0, Usage0->0, outbound0.
Employee detail Browser Failed to fetch remains FAIL/cause UNKNOWN (retry and independent tab); API/preflight success is not Browser return acceptance. Browser company used SQL fixture, canonical assistant + later ARRIVED/UNVERIFIED FoundingRun correction for existing-company bootstrap; not formal normal Company creation. Candidate package install is not published ordinary Business/atomic firstWorkspace activation proof. Original failures/logs retained. Physical crash at every Task/outbound gap, realProvider/fees/credentials/Keychain/native/defaultApp NOT RUN. FullCG3otherformats/accountpublication/receipt/review/learning goals remain. No Product/Frozen rewrite/Git mutation. Owner/independent QA is next Gate; publication/live/native require separate exact decisions.
