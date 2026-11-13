# CURIS V1 — CURRENT UI FOUNDATION

> Status: Review
> Authority Class: REVIEW
> Disposition: Candidate foundation for CEO UI reconciliation; not a second UI Blueprint
> Scope: Read-only foundation statement derived from Current Product Truth and Frozen Shell

## 1. Foundation position

本文件不是新的 UI Blueprint，也不替代 `Curis_Product_UI_Blueprint.html`。它把已经可以继承的 UI 责任压缩成一份审计候选，供后续 Page Contract / Visual Delta 使用。

### Visual language authority

`docs/03_Design/CURIS_VISUAL_STANDARD_V1.md` 是当前 Frozen Visual Language：Direction D、`#806BE5` Primary Brand Accent、Neutral Foundation、PRIMARY / SECONDARY / TERTIARY / QUIET、Calm Density、Open Canvas / Tonal Field、低频 accent 与稀缺 Card。它冻结视觉语言，不冻结任何具体页面构图。

CEO 与 Employee 的身份展示统一消费 `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`；头像可选，上传、Curis 预置卡通头像和 fallback 三者同一 Pattern，不影响责任或执行。该登记不等于头像持久化或资源实现已完成。

旧 `Curis_Design_System.md`、`Curis_UI_Frozen_Spec_2026-08-04.md` 与现有 Frontend 中的 `#32f08c` 只在未被新标准 supersede 的实现兼容、可访问性和结构部分继续参考；`#32f08c` 不再是 Current Brand Accent。迁移不在本文件执行，遵循 `docs/reviews/CURIS_VISUAL_TOKEN_MIGRATION_MAP.md`。

### App Entry accepted UI baseline

`docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md` 将 Figma `2Fh7DgPPfLgdbvNtnzPnk9`（13 个已登记 Core Frames）登记为当前 App Entry UI Design Baseline。Welcome → Create Company / Skip → Empty Curis、CEO Identity、CEO Assistant first presence、Conversation / Composer、Model Management / Selector 与 Empty State 共享模式为 `UI ACCEPTED`；`IMPLEMENTATION READY` 仍待 Engineering Reconciliation，不能写成 Frontend 已实现。旧 App Entry / First Run / Prototype / fixture / Trae 候选仅在冲突处 `SUPERSEDED FOR CURRENT UI`，保留历史 provenance。

`docs/reviews/CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md` 将同一 Figma 的 `CEO Desk — Operating / Matters Present`（`69:3`）登记为 Current Operating Design Baseline：CEO Desk 产品结构、Operating Composition 与 Operating UI 均 `ACCEPTED / UI ACCEPTED`，仅覆盖 1440 × 900 Light；Dark、1024、密度、展开态、真实数据投影和工程接入属于 Adaptation / Validation，下一步为 CEO Desk Implementation / Adaptation Readiness Review。

`docs/reviews/CURIS_V1_FRONTEND_BATCH_1_IMPLEMENTATION_ACCEPTANCE.md` 登记 Batch 1 的实现事实：App Shell、七区导航、App Entry、真实 Empty Curis / Empty Company、Company / canonical CEO Assistant、Model Management、Business Proposal、canonical General Business + First General Workspace、CEO Desk Operating / Attention Projection 与 packaged restart 主链已 `IMPLEMENTED / ACCEPTED WITH RECORDED BOUNDARIES`。Avatar、Conversation、Composer、Model Selector、1024 Assistant layout 与 General Workspace 完整运行仍是 Partial / P1；M3 Keychain、专业自动匹配和真实外部 AI 执行保持独立边界。旧 floating `GlobalAssistant` 为 Legacy，下一实施目标是 General Workspace P1 Operating Closure。

## 2. Shared foundation

### Shell

- 一级导航是七区：CEO 工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议。
- 搜索、最近工作、通知/待处理、CEO Assistant 是 Global Capability，不是 Global Topbar，也不占新增一级区。
- `Navigation Pane + Main Workspace Pane` 永远构成最小可用桌面；Context/Utility 是 Adaptive Surface，默认按需出现。
- 每个 Pane 有自己的 Pane-local Header；Main Header 不横跨 Context/Utility。
- Main 关闭 Context/Utility 后仍能理解当前业务并完成主要工作。

### Main composition

`Main = selected Professional Surface + Shared Work Area`。

- Domain Primary Surface 是 Workspace 最大视觉责任；它让业务像真实产品，而不是员工列表或运行控制台。
- Shared Work Area 承载 Employee Row、Conversation-first Workstation、当前 Work、Result/Artifact 轻量引用。
- Employee Workstation 属于 Work Area，不是整个 Workspace 的主视觉。
- Workspace 可以有不同 Domain UI；共享的是 Shell、责任、状态、上下文和恢复边界。

### Progressive disclosure

| 层级 | 默认内容 |
|---|---|
| L1 | 当前 Workspace/Business、核心业务面、当前责任、一个自然 Composer、重要结果/下一步 |
| L2 | Needs CEO、Handoff、Result/Evidence 引用、失败/恢复、当前对象上下文 |
| L3 | `+`、对象动作、Context/Utility、Focus View、专业对象与编辑 |
| L4 | Provider、Permission、Session、Trace、Runtime state、协议与审计细节 |

### User-facing state

普通 UI 消费真实但易懂的状态：空闲、工作中·描述、阻塞·原因；完成属于 Work/Task/Result，不属于 Employee。技术状态只在恢复、证据和高级诊断真正需要时出现，不能成为首页 IA。

## 3. Product entry foundation

### Organization Center accepted UI baseline

`docs/reviews/CURIS_V1_ORGANIZATION_CENTER_UI_ACCEPTANCE.md` registers the 1440 × 900 Light Figma baseline (`106:3`, `106:230`, `106:457`). Organization Center is fixed to two top tabs—`公司版图` and `员工目录`; Company Map uses Department Container + Business-first + progressive Role/Staffing disclosure, while Employee Directory reads Employee → Role → Business → Department. Implementation is separately registered as `IMPLEMENTED / ACCEPTED` in `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md`; Dark, 1024, accessibility and interaction wiring remain P2.

### Operating Intelligence accepted UI baseline

`docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_UI_ACCEPTANCE.md` registers the 1440 × 900 Light Figma baseline (`172:3`, `172:277`, `172:551`, `172:825`) for Overview, Scoped Business Analysis, Explore / Benchmark and Report / Decision Continuity. Operating Intelligence remains a scoped analyst workspace, not a CEO Desk Dashboard or a second Truth / Result / Analytics Runtime. Prototype wiring, Dark, 1024, accessibility / keyboard and real Runtime data-density verification remain P2; Frontend productization and Runtime / Data closure are not claimed.

### Knowledge Library accepted UI baseline

`docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_UI_ACCEPTANCE.md` registers the 1440 × 900 Light Figma baseline (`187:2`, `187:276`, `187:550`, `187:824`) for Overview, Browse / Search, Reading / Reference Detail and the compact Select Reference From Work picker. The user-facing product remains `资料库`, with internal mind Company Reference Space; the visual authority is Reading-first, uses Reference Rows and explicit Load More rather than a Card Wall or backend file tree, and treats Company / Business / Workspace as a lightweight current scope selector rather than fixed library tabs. Dark, 1024, accessibility / keyboard, dynamic batching, load failure and real Runtime data-density remain P2; Frontend productization and Runtime / Data closure are not claimed.

### Meeting Room accepted UI baseline

`docs/reviews/CURIS_V1_MEETING_ROOM_UI_ACCEPTANCE.md` registers Meeting Room Product / UX as `ACCEPTED` and UI as `UI ACCEPTED` for the 1440 × 900 Light Figma baseline (`214:3`, `247:2`, `214:279`, `214:555`, `214:831`). The accepted pattern is Overview → temporary Start Meeting Overlay → persistent Meeting, mature group Conversation with structured operating messages, canonical Decision/P7 and Responsibility → Work → Result continuity. Meeting remains independent of the CEO view/session lifecycle; Runtime/Data implementation is not claimed and proceeds through the `MEETING ROOM PRODUCTIZATION CLOSURE` gate.

### App entry and Create Business

```text
PRE-COMPANY Welcome
→ CEO Display Identity（若不存在）+ Company 创建
→ CEO Assistant identity
→ AI Readiness（需要模型推理时）
→ Company Ready / No Business
→ CEO Assistant Conversation / Create Business Flow
→ Business / Workspace 开始经营
```

Company = 0 时允许 Skip → Empty Curis Shell；不生成假数据。Company Ready 后的 Create Business Flow 才接受不完整经营意图。没有专业模板时进入 General Business Workspace；有模板时，专业工作环境只加速能力，不占有 Business/Workspace 身份。模型管理从左下 CEO 头像 → 设置进入，模型使用在 Conversation Model Selector 内完成，不要求逐 Employee 手工绑定。

### Company and Business entry

- Company / Business 负责身份、目标、整体方向、组织与结果聚合。
- Business 下面是一个或多个独立 Workspace；长期 Business 归属 Department。
- Business page 默认显示 Business Name、目标/定位、Workspace 入口、Responsible Leader、重要 Result 和 conditional Risk/Need；不要把所有 Workstation 或技术配置堆在卡片上。
- Workspace page 首先显示 Domain Primary Surface；通用 Work/Result/Conversation 和 Employee Work Area 按需出现。

## 4. Shared operating interactions

- “交给 Curis”是用户产品语言；内部仍走 Intent → Responsibility → Leader/Employee → Work → Result/Evidence → Review/Decision。
- 每一个真正动作都应返回对象、状态、下一步和 Activity/来源，而不是只显示 Toast。
- 失败、等待、未知、来源不一致和权限不足必须说明原因、责任、缺什么、如何恢复、回到哪个上下文。
- 用户控制展开/收起；Runtime 状态变化不得强制改变 UI 折叠状态。
- CEO Desk、Business、Workspace、Employee Profile、Organization/Company Map、Assistant 可以进入 scoped Insights，结束后回原上下文。

## 5. Foundation matrix

| 可继承结构 | 当前保留方式 | 后续动作 |
|---|---|---|
| Frozen Pane Shell | 作为唯一空间骨架 | 保持；只校正导航数据和 copy |
| Generic Workspace renderer | 作为任意业务的通用承载 | 接通 Business/Workspace first-run 与普通用户状态 |
| Employee Workstation | 统一工作区域模式 | 不扩成整个 Workspace 主视觉 |
| Runtime/API seam | 内部实现 seam | 不暴露成用户产品页面 |
| RD/XHS domain objects | 功能/对象来源 | 迁入各自 Domain Primary Surface；不把实例样本变成 Core domain |
| Terra components/tokens | 视觉基础 | 逐步消费 Frozen Visual Standard；不让旧导航数据支配 Current IA |

## 6. Not yet accepted by this audit

本候选不批准：最终像素、页面卡片数量、图表形式、Domain-specific visual、Meeting 高保真、Assistant 动画、Provider 目录视觉、任何 Frontend 删除或 Runtime 变更。上述内容需各自 Page Contract / Visual Delta / Implementation Review。

## 7. Foundation acceptance test for next phase

下一阶段只有在以下事实都具备后，才能把“foundation”升级为实现基线：

1. 七区导航与所有 route/deep-link 一致；
2. First Run 能从不完整意图落到 canonical Business + General Workspace；
3. CEO Desk、Business、Workspace、Employee、Result/Decision/Recovery 形成可回访路径；
4. 至少一个 Professional Workspace 在同一 Shell 中完成真实 packaged E2E；
5. 旧入口有 replacement、依赖审计与回归证据；
6. 1440/1024/窄屏、主题、console、重启/重载证据独立通过。

— CANDIDATE FOUNDATION · STOP FOR CEO REVIEW
