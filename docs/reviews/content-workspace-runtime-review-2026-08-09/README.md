# Content Workspace Runtime Review（2026-08-09）

Status: Review

Decision: `PASS_TO_RUNTIME_FOUNDATION_IMPLEMENTATION_ONLY`

本文件是小红书运营工作台、抖音 / TikTok 运营工作台及其 Content Workspace Studio 的运行评审记录。
它不是新的产品定义，也不替代唯一 Blueprint；目的是判断当前 Runtime 定义和 UI 证据是否已经足以进入实现 Issue。

## 1. 评审范围

| 范围 | 当前权威来源 |
| --- | --- |
| Product Definition | `docs/01_Product/Curis_Product_Blueprint.html`（4.12，Review） |
| Runtime Contract | `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`（v1.6，Draft） |
| Completion Standard | `docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`（Frozen） |
| UI Contract | `docs/03_Design/Curis_Workspace_Shell.md` §8.7 / §9.7 / §9.8 |
| Current UI Evidence | `docs/01_Product/Curis_UI_Evidence_Alignment_2026-08-09.md` §4.5 |
| Prototype | `curis-ui-prototype/workspace-studio.html`、`workspace-runtime-xhs.html`、`workspace-runtime-shortvideo.html` |
| Simulation Plan | `docs/reviews/three-business-runtime-simulation-plan-2026-08-09/README.md` |

## 2. ADR-0041 逐项评审

| 完成标准 | Runtime 定义 | 当前证据 | 结论 |
| --- | --- | --- | --- |
| Business Lifecycle | Workspace `DRAFT → BLUEPRINTING → SIMULATED → PENDING_APPROVAL → OPERATING → PAUSED → ARCHIVED`；ContentItem 独立生命周期 | 文档已定义；原型未持久化证明 | **定义通过，证据未通过** |
| State Machine | ContentItem、InteractionItem、ReplyPolicy、平台变体状态均有状态与动作边界 | 原型仍以静态节点和示例动作呈现 | **定义通过，证据未通过** |
| Runtime Stages | Outcome → 平台 → Role Slot → Agent / Capability → Connector → Evidence → Cadence → Simulation → Approval → Runtime；内容阶段补充 Stage Runtime Contract | Studio 画布存在，但抖音 / 小红书链路混合 | **定义通过，证据未通过** |
| Input / Output | 每个内容阶段有 Page / Surface、Entry State、Input、Output、Owner、Runtime Action、Exit、Exception、Audit | 文档已补齐 §5.8.1.1；原型缺少持久化对象和版本回溯 | **定义通过，证据未通过** |
| Owner / Organization | CEO → CEO Assistant → 内容策略 AI → 研究 / 创作 / 发布 / 互动 / 复盘 AI | 当前原型使用英文演示角色，未形成中文岗位状态带 | **未通过** |
| Feedback / Exception | 未授权、发布失败、数据延迟、CEO 拒绝、互动风险和模板越界均有路径 | 当前原型只显示静态配置缺口，未证明状态转换 | **定义通过，证据未通过** |
| Closure / Archive | ContentItem 复盘后进入下一轮 Decision；Workspace 可暂停、归档并保留学习 | 当前原型无运行版本与归档事实 | **未通过** |
| Runtime Simulation | XHS / TTK 正常、未授权、失败、延迟 / 冲突、CEO 拒绝、互动风险、平台变体不合规 | 没有真实 Simulation 运行记录 | **未通过** |

## 3. 当前原型事实

对 `workspace-studio.html` 做静态属性核对，以下契约属性均不存在：

```text
data-workspace-studio      0
data-studio-mode           0
data-platform-variant      0
data-role-slot             0
data-presence-state        0
data-reply-policy          0
data-evidence-rule         0
data-simulation-status     0
data-blueprint-version     0
data-studio-action         0
```

同时仍存在 `Research AI`、`Analysis AI`、`Script AI`、`Data AI`、`Review AI` 等英文演示角色。
“运行模拟”和“提交审批”是静态按钮，不能证明 `BLUEPRINTING → SIMULATED → PENDING_APPROVAL → OPERATING` 的持久化流转。

## 4. 评审结论

### 已确认

1. 外部内容工具的有效机制已经完成产品转译：平台适配、信号监听、排期节奏、版本审计、互动分流。
2. Curis 的运营办公室布局已明确：目标 → 信号 → 队列 → Assistant 上下文 → 外部结果 → 复盘。
3. Runtime 文档已覆盖正常、未授权、失败、延迟 / 冲突、CEO 拒绝和互动风险场景。
4. Runtime 文档已补充每个内容 Agent 的触发、输入、责任动作、输出、外部动作边界和升级条件。
5. 三业务 Simulation 的场景、证据字段和通过条件已形成独立计划，但尚未执行。

### 未确认

1. 当前 Studio 是否能持久化草稿、版本、模拟结果和审批状态。
2. 平台变体是否真正独立，而不是一条混合的短视频 / 图文演示链。
3. AI 岗位是否按组织关系显示责任、容量、交接和下一检查点。
4. 发布回执、互动回复回执和 `publishedVersionId` 是否能反查到 CEO 批准版本。
5. 运行失败、CEO 拒绝和外部数据异常是否能回到 CEO Desk 并形成下一次 Decision。
6. 三业务 Simulation 是否能在真实 Company 数据和外部证据路径上执行。

## 5. 进入实现 Issue 的必要条件

以下条件全部满足后，才能创建 Studio / Content Runtime 实现 Issue：

- Product Blueprint、Business Runtime 和 UI Shell 的交叉 Review 均为 PASS；
- 通过 §9.8 DOM 属性和交互断言，且深色 / 浅色 / 刷新后三次结果一致；
- 至少完成 XHS-CONTENT-001~005、TTK-CONTENT-001~005 和互动五类 Simulation；
- 至少一条真实发布或 CEO 手动发布记录具备 `contentId → runId → outcomeId` 证据链；
- 至少一条互动处理记录具备 `interactionId → responseVersion → externalReceipt` 证据链；
- 任何 Blueprint / Agent / Connector / Evidence Rule 修改都会使 `simulationPassed=false`；
- 未通过模拟、未授权、版本不一致或缺少回执时，提交审批和发布动作必须不可用；
- UI 中不再出现英文岗位作为独立用户标签，也不再使用通用“移动至下一阶段”。

## 6. 当前决策

当前保持 `BLOCKED_PENDING_RUNTIME_REVIEW`：

- 不修改业务前端；
- 不把现有 Studio 或内容运行页标记为完成；
- 允许继续完善产品定义、Runtime 契约、UI 线框和 Simulation 计划；
- 下一步应由产品席先完成 Runtime Review，再派发限定文件范围的实现 Issue。

## 7. 解锁后的 Studio 实现边界

这不是当前 Issue，也不授权直接修改代码。Runtime Review 通过后，Issue 至少应明确以下交付物：

| 交付面 | 必须实现 | 不得以什么替代 |
| --- | --- | --- |
| Studio 状态 | 草稿、装修中、模拟通过、待审批、运行版本的持久化和刷新恢复 | `localStorage` 演示状态或按钮点击后跳转 |
| 业务结构 | Outcome、平台变体、Role Slot、Agent / Capability、Connector、Evidence Rule 可回溯 | 一组没有语义的 Agent 卡片 |
| 模拟 | 正常、未授权、变体不合规、CEO 拒绝、工具失败、外部延迟等场景可执行并记录结果 | 静态“未通过 3 项”文案 |
| 审批 | 未通过模拟或存在缺口时禁用；批准版本与运行版本建立关联 | 直接进入决策室或直接写成运行中 |
| 运行交接 | 由批准的 Blueprint 版本创建 Runtime；修改草稿不会静默改写运行空间 | 页面内存对象或固定演示数据 |
| 证据 | `contentId / runId / outcomeId`、`versionId / publishedVersionId`、互动回执可追踪 | 截图、AI 自报完成或手动编辑数据库 |

Issue 的文件范围必须由实际运行架构重新确认；本 Review 不预先批准前端、后端、数据库或桌面壳的修改。

## 8. 后端运行事实交叉核对（2026-08-09）

为避免把“已有连接器 / 旧内容工作流”误认为当前 Content Workspace Runtime，已对后端代码与 `backend/data/curis.sqlite` 做只读核对：

| 现有基座 | 实际存在 | 不能替代的目标能力 |
| --- | --- | --- |
| `ContentWorkflowRuntime` + `content_publish_packages` | 内容生成、发布包快照和旧连接器发布链 | 不能替代 `ContentItem` 生命周期、平台独立变体、版本审核和 `publishedVersionId` |
| `content_workflow_runs` | 只有 `running / completed / failed` 的工作流运行摘要 | 不能替代 Stage Runtime Contract 的八阶段、失败恢复和 CEO 拒绝回退 |
| `Workspace` 状态机 + `blueprint_json` | 具备装修 / 模拟 / 审批 / 运行的基础字段 | 不能证明配置变更自动使模拟失效，也不能证明运行版本冻结 |
| `runtime_transition_log` | 通用状态转换留痕表 | 不能替代包含参与者、交接、外部回执、CEO 决策和失败事件的 `SimulationRun` 聚合 |
| `RdWorkflowRuntime` | 研发 workflow run / step 运行链 | 不能替代三业务共用 SimulationRun，也不能在无真实 commit/build/test/CEO acceptance 记录时宣称 RD 通过 |
| 旧状态写入路径 | `content_workflow_runtime.py` 直接更新 `content_workflow_runs.status`；`rd_workflow_runtime.py` 直接更新 `workflow_runs / workflow_steps.status` | 不能直接复用为 v1.6 的统一状态机；Runtime Foundation 必须建立对象状态流转入口与迁移边界，禁止把旧 `running/completed/failed` 当成 ContentItem / 研发 Stage 状态 |

核对结果：`backend/data/curis.sqlite` 中上述核心运行表当前均为 0 条记录；代码中未发现 `SimulationRun`、`ContentItem`、`InteractionItem`、`ReplyPolicy` 或 `publishedVersionId` 的持久化实现，同时发现内容 / 研发旧运行链存在直接写入 status 的路径。预期活动数据库 `data/curis.sqlite` 当前不在工作树中，不能用空数据库或静态原型补齐运行证据。

因此，本 Review 继续保持 `BLOCKED_PENDING_RUNTIME_REVIEW`。下一份实现 Issue 必须先限定 Runtime Foundation（SimulationRun、ContentItem / InteractionItem、平台版本 / ReplyPolicy、Studio 配置版本失效及三业务证据入口），并在其 Review 通过后执行三业务 Simulation；不能直接从现有发布包或页面跳入 UI 实现。

## 9. Runtime Definition 自审（2026-08-09）

Business Runtime v0.6 在进入实现前做了一次反向审查，发现会导致实现歧义的定义问题，已在 v0.7 / v0.8 修正：

| 发现 | 原风险 | v0.7 / v0.8 修正 |
| --- | --- | --- |
| 研发工作台只有 Simulation 场景，没有逐 Stage Runtime Contract | 开发团队仍可能直接把旧 `workflow_runs` 当成研发业务闭环，无法验证 CEO 意图、真实工程证据和 CEO 验收 | 增加 INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW → IMPROVE → ARCHIVE 的 Page / Input / Owner / Output / Exception / Audit 契约 |
| ContentItem 的正常生命周期与异常状态混在叙述中 | `FAILED / STALE / ABNORMAL / WAITING_CEO` 可能被实现成“成功生命周期”的额外状态，导致异常被覆盖或直接变成已发布 | 保持正常 `lifecycleStatus` 不变，新增 `exceptionStatus`；异常清除必须有恢复命令和审计 |
| SimulationRun 只列字段，没有数组元素结构 | 实现可能把交接、失败和 CEO 决策压缩成不可查询的文本 | 增加 `stateTransitions / handoffs / failureEvents / ceoDecisions` 的结构化字段契约 |
| 旧执行链直接写入 status | 新 Runtime 可能出现第二套可改变 CEO 所见状态的入口 | 增加旧 `workflow_runs / workflow_steps / content_workflow_runs` 的迁移边界，只允许作为 `executionRef` / 内部遥测 |
| Cycle / Handoff / Acceptance 只有流程词，没有独立契约 | 研发、内容和未来业务可能各自把“周期完成”“已交接”“CEO 已验收”实现成页面标签，无法跨模块反查 | v0.9 / v1.0 增加 Cycle 生命周期、Handoff / DecisionPacket / Acceptance 字段与状态机；SimulationRun 增加自身生命周期与 `passStatus` |

本次自审结论：**定义层问题已修正，但实现证据仍为零，Review 仍不通过。** v1.6 只能作为下一份 Runtime Foundation Issue 的产品输入，不能作为已经实现的 Runtime 证明。

## 10. Runtime Foundation Issue 候选（RUNTIME-FOUNDATION-001，非授权）

以下内容已经收敛为下一份正式 Issue 的候选定义，但本节本身不授权代码、数据库或桌面应用修改。

| 项目 | 候选值 |
| --- | --- |
| Issue ID | `RUNTIME-FOUNDATION-001` |
| 目标 | 让三类业务共享一套可持久化、可重启、可反查的 Business Runtime Foundation |
| 产品输入 | Product Blueprint 4.12、Business Runtime v1.6、ADR-0041 |
| 前置门禁 | 本 Review 通过，并由产品负责人明确授权实现 |
| 实现范围 | Runtime 对象、状态入口、迁移适配边界、最小 Simulation 证据；不含新 UI |
| 允许落点（候选） | `backend/app/` Runtime / migration 模块、`backend/tests/` Runtime 与 Simulation 测试、`docs/` 运行与迁移说明 |
| 禁止落点 | `frontend/` 页面改版、`curis-ui-prototype/` 继续扩展、真实平台 API、商业化 Admin、旧表物理删除 |

正式 Issue 创建前，必须再确认允许文件清单；任何未列入清单的文件不得因“顺手修复”而被修改。

### 10.1 必须交付

1. 持久化 `FoundingRun` 与 Company Formation 状态；保证从 `foundingRunId → companyId` 的确认、恢复、拒绝和失败路径可查询，未确认前不创建假 Company。
2. 持久化 `AIEmployee / RoleSlot / CapabilityBinding` 的身份、汇报关系、生命周期、授权、容量和在岗状态；支持缺能力、过载、撤权、退回和换责路径。
3. 持久化 `SimulationRun`，并能按 `companyId / workspaceId / scenarioId` 查询与重启恢复。
4. 持久化 `CEOAssistant` 的身份、契约、Context 版本、生命周期和质量快照；实现 v1.6 的状态入口、责任边界、升级 / 换责和 Assistant Simulation。
5. 持久化 `Cycle / Handoff / DecisionPacket / Acceptance`，实现 v1.6 的状态机、反查键、CEO 决策和回滚 / 拒绝 / 退回路径。
6. 持久化 `ContentItem / ContentVersion / ContentReview / PublicationReceipt / InteractionItem / InteractionResponse`，实现 v1.6 的状态、版本、ReplyPolicy、回执和审计不变量。
7. 建立研发 Cycle / Stage 的业务状态入口；旧 `workflow_runs / workflow_steps` 只能作为 `executionRef`，不得继续作为 CEO 所见状态真相。
8. 建立 Workspace Blueprint 版本与 `simulationPassed` 失效关联；修改 Stage、Agent、Connector、平台约束、ReplyPolicy 或 Evidence Rule 必须使运行版本与草稿版本分离。
9. 提供 First Arrival、组织配置与三业务最小可执行 fixture / 手动证据入口：FIRST-ARRIVAL-001、ORG-001、RD-001、XHS-001、TTK-001 及各自至少一条失败 / 拒绝路径。
10. 为每一条状态、交接、失败、CEO 决策、Assistant 输出、组织授权和外部回执提供可查询测试证据，不允许只在内存或页面状态中存在。

### 10.2 明确不在该 Issue

- 不实现 Workspace Studio 新 UI；
- 不改造现有 CEO Office / 运营办公室视觉；
- 不接入真实小红书、抖音或 TikTok API；
- 不删除旧表或物理迁移历史数据；
- 不创建新的一级导航、CRM 或第二套 Assistant；
- 不把 fixture 结果写入 `VERIFIED`。

### 10.3 Issue 关闭证据

Issue 关闭前必须同时提供：First Arrival `foundingRunId → companyId → assistantId` 恢复 / 拒绝 / 失败证据、AIEmployee / RoleSlot / CapabilityBinding 的创建 / 授权 / 过载 / 撤权 / 退回 / 换责证据、Runtime 状态与迁移测试、CEO Assistant 生命周期 / Context / 升级 / 换责证据、Cycle / Handoff / Acceptance / Decision 的拒绝与回滚证据、真实数据库重启恢复证据、三业务场景运行记录、至少一条失败 / CEO 拒绝记录、版本错配阻断记录、`assistantId → Brief / Handoff / DecisionPacket / Closeout`、`contentId → runId → outcomeId` 与 `interactionId → responseVersion → externalReceipt` 反查证据。仅有接口 200、单测通过或页面截图不得关闭。

### 10.4 下一步门禁（当前实际执行顺序）

当前最重要的动作不是继续改 Studio 页面，而是完成一次有明确决策结果的 Runtime Review。后续顺序固定如下：

| 阶段 | 允许动作 | 必须形成的证据 | 未满足时的处理 |
| --- | --- | --- | --- |
| A. 产品 / Runtime Review | 对 Blueprint 4.12、Runtime v1.6、ADR-0041、Workspace Shell 交叉审阅 | Review 记录明确 `PASS`、`CHANGES_REQUIRED` 或 `BLOCKED`；所有未决定义有责任人和回补项 | 保持 `BLOCKED_PENDING_RUNTIME_REVIEW`，不得创建实现 Issue |
| B. 正式 Issue 授权 | 由产品负责人批准 `RUNTIME-FOUNDATION-001` 的文件清单、验收条件和排除项 | 正式 Issue、授权人、允许修改路径、回滚方式 | 候选 Issue 仍是非授权输入，不得改代码或数据库 |
| C. Runtime Foundation | 只实现统一对象、状态入口、迁移适配边界和最小 Simulation 证据 | 持久化、重启恢复、身份隔离、状态转换、失败 / 拒绝 / 退回、版本失效和查询反查测试 | 任一关键证据缺失则不进入业务 Simulation |
| D. 三业务 Simulation | 运行研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台的正常与异常场景 | RD / XHS / TTK 的 `SimulationRun`、外部结果 / 手动反馈、CEO 决策、归档和回溯证据 | 只修 Runtime 契约或 Foundation；不以静态原型补齐 |
| E. UI 迁移 Issue | Foundation 与 Simulation 通过后，单独派发 UI 迁移 Issue | 导航、CEO Desk、Assistant、三工作台、空/错/未授权/延迟态的浏览器证据与视觉验收 | 保持当前 Project/Task-first 前端为交付事实，不宣称目标态已实现 |

Runtime Review 的最低决策清单：

1. 明确 `State` 是持久化业务事实，旧 `workflow_runs` / `content_workflow_runs` 只能作为 `executionRef`，不能继续作为 CEO 所见状态源。
2. 明确 `CEO Assistant` 只负责观察、准备、提醒、协调和升级；它不能创建第二套任务真相，也不能绕过 Runtime 状态入口。
3. 明确三条业务轨道同步验证，但研发工作台的首个工作项只是“Curis 的自研发”，不是新的业务类型或导航项。
4. 明确外部结果在有 API 授权时走回执，在无授权时必须走 CEO 手动反馈窗口；两种来源都必须带来源、时间、责任人和置信度。
5. 明确任何 Blueprint、Agent、Connector、Evidence Rule、平台约束或 ReplyPolicy 变更都会使此前的 Simulation 失效，不能沿用旧的 `simulationPassed`。
6. 明确结果的 `verificationStatus` 与 `evidenceCondition` 是两个正交维度；“待回流 / 来源冲突”不能被实现为新的成功生命周期，也不能覆盖验证结论。
7. 明确 Workspace 引擎固定 8 个语义槽位，`Produce` 可按业务拆成 1～N 个 Stage；不得把原型偶然呈现的 9 个节点实现成固定业务数量。
8. 明确 CEO Assistant 是 Company-level 唯一的 AI 员工对象；Global Assistant 只是基础设施，不能以聊天记录或 Snapshot 替代其生命周期、责任、Context 和质量证据；`UPGRADED` 与 `REASSIGNED` 必须是两个可审计的独立状态。
9. 明确 AIEmployee、RoleSlot、CapabilityBinding 三者分离；CEOAssistant 是 Company-level 特殊 AIEmployee，不重复创建；CEO 批准的是责任与授权，不是简单增加 Agent 卡片；`orgVersion`、RoleSlot 生命周期、`lifecycleStatus / presenceState` 与 `CapabilityBinding.status` 必须分别可追踪；缺能力、过载、撤权和退回都必须形成可追踪状态。

因此，当前可执行的下一步只有：先实现限定范围的 Runtime Foundation 对象与 API，再执行三业务 Simulation；前端视觉、导航和三工作台页面仍保持只读审计状态。

## 11. ADR-0041 逐项复核（v1.6 定义层）

| ADR-0041 要求 | v1.6 定义证据 | 当前实现 / 运行证据 | 结论 |
| --- | --- | --- | --- |
| Business Lifecycle | BusinessDirection、Commitment、Workspace、CEOAssistant、AIEmployee、Cycle、ContentItem、InteractionItem、SimulationRun 均有生命周期或正交异常维度 | 当前数据库无三业务运行记录 | 定义通过，运行未通过 |
| First Arrival | `FoundingRun` 与 Company Formation 从空公司到首个 Cycle 候选的状态、恢复、拒绝和失败路径已定义 | 当前 onboarding / guide 不能证明 `foundingRunId → companyId → assistantId` 持久化链 | 定义通过，运行未通过 |
| State Machine | 统一 5 个核心对象与 `CEOAssistant` 状态机；新增 Cycle、Content、Interaction、Handoff、DecisionPacket、Acceptance、SimulationRun 状态机 | 旧内容 / 研发链直接写旧 status，Global Assistant 尚未接入 CEOAssistant Runtime 入口 | 定义通过，迁移未通过 |
| Runtime Stages | 通用 Workspace Stage、研发八阶段、内容八阶段均有 Page / Input / Owner / Action / Output / Exception / Audit | 没有真实 Stage 运行记录和跨模块 Handoff | 定义通过，证据未通过 |
| CEO Assistant Runtime | `CEOAssistant` 的身份、生命周期、Context、责任输出、动作边界和质量评估已定义 | 当前 Global Assistant 仍是 Project/Task-first Snapshot，未有 CEOAssistant 对象或 Assistant Simulation 记录 | 定义通过，运行未通过 |
| AI Organization Runtime | `AIEmployee / RoleSlot / CapabilityBinding` 的身份、汇报、能力、容量、在岗和换责路径已定义；`orgVersion`、RoleSlot 生命周期与 `lifecycleStatus / presenceState` 维度已分离 | 当前 Employee / Capability 现有实现不能证明目标组织状态、岗位生命周期和授权版本链 | 定义通过，运行未通过 |
| Evidence axes | `verificationStatus` 与 `evidenceCondition` 分离；STALE / CONFLICT 不再伪装成生命周期 | 当前数据库和 UI 尚未持久化两维字段 | 定义通过，证据未通过 |
| Input / Output / Owner / Next Stage | Stage Contract 与 Cycle / Handoff / Acceptance 契约已给出 | 仍未持久化 | 定义通过，证据未通过 |
| Feedback / Exception | `exceptionStatus`、FailureEvent、STALE / ABNORMAL、CEO 拒绝 / 回滚路径已定义 | 原型与旧运行链不能证明异常不会被覆盖 | 定义通过，证据未通过 |
| Closure / Archive | Cycle、ContentItem、SimulationRun、Handoff、Acceptance 均有关闭 / 归档路径 | 没有归档运行记录与重启恢复证据 | 定义通过，证据未通过 |
| Business Runtime Simulation | 三业务 Plan 覆盖正常、失败、未授权、延迟、CEO 拒绝、互动和 Assistant | Simulation 尚未执行 | 未通过 |

复核结论：**Runtime v1.6 的定义层已完成本轮缺口修正并具备进入 Review 的完整度；当前整体仍不能 PASS，因为实现、迁移和真实 Simulation 证据缺失。**

## 12. Implementation Gate Addendum（2026-08-09）

主线程完成产品席复核，决定：`PASS_TO_RUNTIME_FOUNDATION_IMPLEMENTATION_ONLY`。

这不是对 Content Workspace、三业务 Simulation 或 UI 的完成验收，而是允许下一份封闭
Backend Issue 实现以下最小共享 Runtime 基础：

- Workspace Blueprint 草稿 / 运行版本与 Simulation 失效边界；
- Cycle / Stage 的持久化状态、责任、输入、输出、异常和审计；
- ContentItem / ContentVersion / ContentReview / PublicationReceipt / InteractionItem 的最小对象与版本引用；
- 研发工作台首个“完善 Curis” Cycle 与小红书 / 抖音各自独立 ContentItem 运行入口；
- API / 临时 SQLite / 重启 / Tenant 隔离 / 失败与 CEO 拒绝证据。

实现阶段仍禁止：真实平台 API、前端 Workspace UI、静态原型替代、旧执行链作为 CEO 事实、
商业化 Admin 和 Desktop。只有 Runtime Foundation 与三业务 Simulation 通过后，才能创建
三业务 Workspace UI Issue。
