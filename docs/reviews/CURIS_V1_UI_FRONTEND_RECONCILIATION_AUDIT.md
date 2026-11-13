# CURIS V1 — UI / FRONTEND RECONCILIATION AUDIT

> Status: Review
> Authority Class: REVIEW
> Date: 2026-08-26
> Disposition: STOP FOR CEO UI RECONCILIATION REVIEW
> Scope: Current Product Truth → UI Authority → Frontend implementation mapping
> Mode: READ-ONLY · NO UI / CODE / RUNTIME / PROTOTYPE CHANGE

## 0. Audit boundary

本审计先消费当前产品真源，再检查 Frontend；不是用代码反推产品，也不是重新设计视觉。

| 层 | 本轮依据 | 权威等级 |
|---|---|---|
| 产品 | `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` → `docs/01_Product/Curis_Product_Blueprint.html` → `docs/01_Product/Curis_Product_Master_Map.md` | Current / Frozen Product Truth |
| UI | `docs/01_Product/Curis_Product_UI_Blueprint.html` → `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | Current / Frozen UI authority |
| 共享语义 | `docs/03_Design/Curis_Company_OS_Shared_Authority.md`、`docs/03_Design/Curis_Content_Growth_Domain_Authority.md` | Frozen authority |
| V1 reality | `docs/reviews/CURIS_V1_APP_READINESS_AUDIT.md`、`CURIS_V1_DEVELOPMENT_MASTER_PLAN.md`、`CURIS_V1_EXECUTION_BACKLOG.md` | Review / implementation planning |
| 额外输入 | 根目录 `CURIS_PRODUCT_REALITY_ALIGNMENT.md`、`CURIS_FIRST_RUN_AND_BUSINESS_ENTRY_MODEL.md` | 未归档的 Review 输入；不覆盖 Current |

根目录两份 alignment 文件虽被本轮消费，但不符合仓库“产品文档只写入 `docs/`”规则；它们在本审计中仅作为 Review 输入，不能成为新入口或第二套真相。

本轮没有启动浏览器、没有抓取新截图，也没有做运行时验收。因此下文的 Frontend 判断是源码/路由静态证据；不能据此宣称视觉细节、可访问性、响应式或真实运行链已经通过。

## 1. Executive summary

### 1.1 Current Product Truth（不看旧 Frontend 也成立）

Curis 是面向普通 CEO 的 Company Operating Product：用户表达经营意图，Curis 组织公司、业务、员工、责任、资料与专业工作，在重要结果、风险和决定处让 CEO 介入。产品结构已冻结为七个一级空间：

1. CEO 工作台
2. 业务空间
3. 组织中心
4. 人才与能力
5. 经营洞察
6. 资料库
7. 会议

搜索、最近工作、通知 / 待处理和 CEO Assistant 是全局能力，不是第八个导航区，也不构成 Global Topbar。`Main = selected Professional Surface + Shared Work Area`；Workspace 是产品身份，Office 只保留历史/实现 provenance。任意业务均可开始：有专业能力时进入 Professional Workspace，没有时进入 General Business Workspace；模板不是门槛。

### 1.2 Reconciliation judgment

- **可直接继承**：Frozen Pane-local Shell、Navigation/Context/Main/Utility 职责、Adaptive Surface、Employee Workstation 与 Conversation-first 共享模式、Main 自成立、真实状态不伪装、Result/Evidence/Decision 引用。
- **需要重新装配**：七区导航、首次运行到 canonical Business + General Workspace、CEO Desk 的经营日投影、Business/Organization/Talent/Insights 的当前语义、通用 Workspace 入口、Assistant 连续性。
- **只保留功能、重做产品面**：现有工作台运行与数据 seam、RD 的专业工作对象、Content/XHS 的业务对象与 Result/Evidence；它们不能把旧技术页面继续当成 Current IA。
- **必须在替换后退役**：旧项目/执行/流水线/Runtime Console、旧 prototype/Flow Pack、旧技术管理页面。当前不安全直接删除，因为仍可能承担兼容路由、测试或迁移 provenance。
- **本轮不建议立即删除任何文件**：删除必须等待替代路径、测试、deep-link、Runtime 依赖与回归证据。

### 1.3 V1 readiness reality

`CURIS_V1_APP_READINESS_AUDIT.md` 把 Frontend assembly 评为约 62%，并把 V1 P0 阻断集中在：First Run 没有落到 Business/Workspace、General Business Workspace 未装配、CEO Desk/Assistant 仅部分产品化、会议占位、没有 fresh packaged whole-app E2E。Shared Runtime、Canonical Business Spine、Employee/Responsibility、Team Operating、RD 真实执行和通用 Package substrate 已有较强基础，但“已有基础”不等于普通用户产品已组装完成。

## 2. Current Blueprint truth

| 产品责任 | Current UI 语义 | Frontend 静态对应 | 当前判断 |
|---|---|---|---|
| CEO 工作台 | 注意力、简报、变化、重要结果、风险、待处理、下一决定；不是 Dashboard/Task Console | `/ceo-office` | **PARTIAL / REFACTOR**：页面仍含 Runtime snapshot、Resource Check、Simulation/Approval 等技术投影 |
| 业务空间 | Company Truth 的 Department / Business / Workspace 入口；Business 是聚合，Workspace 是独立工作单元 | `/ceo-office/business`、`/ceo-office/workspace`、`/ceo-office/workspace/installed/[workspaceId]` | **PARTIAL**：目录和 parent/deep route 有基础，创建与通用经营闭环缺失 |
| 组织中心 | [公司版图] [员工目录]；Company → Department → Business → Workspace → Role/Staffing；不是传统 HR/Agent 图 | `/ceo-office/organization`、`/ceo-office/organization/*` | **PARTIAL / REFACTOR**：源码仍以 `AI Workforce Map`、旧组织节点和项目数据组合 |
| 人才与能力 | 专家、技能、连接器三个内部 Surface；专家经招募、公司身份、岗位/责任和授权后成为 Employee | `/ceo-office/talent-market`、`/ceo-office/capabilities` | **PARTIAL / RE-SKIN**：核心交互较接近，正式名称、路由和能力/员工边界仍需统一 |
| 经营洞察 | Company/Business/Workspace/Employee/Team/Model/Agent/Provider/Capability/时间的分析消费面；不是 CEO 首页 Dashboard | `/ceo-office/analytics` | **PARTIAL / REFACTOR**：当前“经营”页仍混合脉搏、队列和 Dashboard 式区块 |
| 资料库 | 本地资料、文件夹、外部来源、索引、搜索、引用、权限、来源追踪、自动沉淀 | `/ceo-office/knowledge` | **PARTIAL**：本地/范围与导入 seam 存在，完整外部连接、引用与回写未证明 |
| 会议 | 讨论、事实、分歧、Decision、责任与跟进回写 | `/ceo-office/meeting` | **MISSING**：当前明确是占位页 |
| 全局 CEO Assistant | 公司级第一位 AI Employee；跨页面可达，继承合法 context；协调、汇总、跟进、升级，不替代 Domain Leader/Expert/Executor | `frontend/components/assistant/GlobalAssistant.js`、`TerraShell` 相关接线 | **PARTIAL**：组件/状态存在，持续伙伴、上下文隔离和主动注意力未完成 |
| Main / Workspace | Main 为选定专业面 + Shared Work Area；四 Pane 自适应；Context/Utility 关闭时 Main 自成立 | `WorkspacePaneShell.js`、各 Workspace 路由 | **FOUNDATION PRESENT**：共享壳层存在，但部分路由仍按旧导航或模板表单组织 |

## 3. Supersession map

Frozen 不意味着永远不能被后续明确 Decision 取代；下表记录继承关系，不把旧材料直接当 Current。

| 历史材料 | 原有内容 | 当前处理 | 状态 |
|---|---|---|---|
| `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | Pane、Adaptive Surface、Pane-local Header、Employee Workstation、Composer、Main composition | 直接继承；它是当前 Frozen UI foundation | **KEEP / CURRENT** |
| `Curis_Company_OS_Shared_Authority.md` | Shared Company / Employee / Responsibility / Result / Evidence 语义 | 直接继承；只作为产品与实现边界 | **KEEP / CURRENT** |
| `Curis_UI_Frozen_Spec_2026-08-04.md` | 旧 prototype 的 tokens、desktop-first、18 页/Global Topbar 结构 | tokens、desktop-first 可继承；Global Topbar、固定 18 页和旧 IA 已被后续 Shell/Product Truth 取代 | **PARTIAL / SUPERSEDED** |
| `Curis_XHS_Workspace_UI_Authority_Map.md` | Shell Frozen；XHS/RD instance 与高保真参考分层 | Shell 与 boundary 继承；XHS visual v4、RD high fidelity 只作 reference | **PARTIAL / CURRENT + REFERENCE** |
| `Curis_XHS_Workspace_Visual_v4.html` | XHS 专业视觉探索 | 保留研究价值，不作为 Frontend implementation 或 Current visual authority | **KEEP AS REFERENCE** |
| `Curis_RD_Workspace_High_Fidelity_v1.html` | RD 专业视觉参考 | 保留业务对象/关系参考；不得当作已完成 UI | **KEEP AS REFERENCE** |
| `Curis_UI_Blueprint_Prototype.html` | 旧导航、Office/办公室、模板优先首次路径 | 只保留迁移/对照价值；由 Current Product/UI Blueprint 取代 | **REMOVE AFTER REPLACEMENT** |
| `Curis_Product_UI_Flow_Pack.html` | 旧业务流、模板/办公室导向 | 不作为 Current IA；替代路径和 deep-link 完成后退役 | **REMOVE AFTER REPLACEMENT** |
| `curis-ui-prototype/`、`curis-ui-prototype.bak/` | HTML/CSS/JS 原型 | 仅原型/历史，不应被实现 Agent 当作 authority | **REMOVE AFTER REPLACEMENT** |
| `docs/reviews/20260810_product_ui_audit/`、`20260813_current_state_product_drift_audit/` | 旧截图与审计结论 | 只作历史 evidence；不证明今天的视觉/运行状态 | **HISTORY / REFERENCE** |
| 旧六区/“经营、业务版图、AI 团队、人才市场、工作空间”导航 | 旧产品阅读模型 | 后续七区 Current Product Truth 已明确 supersede | **SUPERSEDED** |

## 4. Frontend implementation map

状态只描述源码与已登记 readiness，不等于完整产品验收。

| Frontend 位置 | 实际承担 | 映射 | 建议 | 依赖/安全门 |
|---|---|---|---|---|
| `frontend/components/workspace/WorkspacePaneShell.js` | Nav/Main/Context/Utility、resizable、search、maximize、pane preference | 共享 Shell foundation；当前 `NAV_ITEMS` 仍是六项且写有“人才市场” | **REFACTOR** 导航数据，**KEEP** 壳层关系 | 七区 Current Truth、route/deep-link、responsive regression |
| `frontend/components/terra/TerraNavData.js`、`TerraSidebar.js` | 全站导航与兼容入口 | 仍显式保留旧 IA、旧分组、旧“AI 团队/经营/业务版图” | **REPLACE/REFACTOR** 为唯一七区数据源；兼容入口下沉 | 全仓 route 引用、旧链接迁移、回归 |
| `frontend/components/runtime/RuntimeProvider.js`、`frontend/lib/runtimeApi.js`、`frontend/lib/api.js` | Runtime/API seam 与状态读取 | 内部实现层，不应成为用户 IA | **KEEP**，只调整投影调用 | 不改变 Runtime/Schema；需保留 fail-closed |
| `frontend/app/layout.js`、`globals.css`、Terra primitives | app layout、tokens、主题、通用可视组件 | 可承载 Frozen Shell | **KEEP / RE-SKIN** | 只消费 Frozen tokens；视觉 QA 后续进行 |
| `frontend/app/onboarding/page.js`、`FirstRunGate.js` | FoundingRun intent / proposal / Company materialization | 旧技术状态与 Company-first partial path；未进入 canonical Business + General Workspace | **REPLACE** 首次产品路径 | Business Spine accepted seam、fresh packaged E2E、restart |
| `frontend/app/ceo-office/page.js` | CEO Desk、workforce/capability/simulation projection | 将内部运行面直接暴露给 CEO | **REFACTOR** 为 operating-day projection；保留必要 result/decision links |真实 Company facts、attention、cross-day continuity、无第二 Truth |
| `frontend/app/ceo-office/business/page.js` | Business + Workspace directory | 部分符合 Business / Workspace canonical model | **REFACTOR** 补 Business creation、General entry、duplicate/deep-link | canonical Business Spine、atomic creation、route proof |
| `frontend/app/ceo-office/workspace/page.js`、`installed/[workspaceId]` | Workspace directory 与 generic package renderer | 可复用通用 Workspace 入口与 renderer | **KEEP / REFACTOR**，补 ordinary user path 与 state projection | Generic Workspace product contract、restart/revisit |
| `frontend/app/ceo-office/workspace/studio/page.js` | 模板/Blueprint/Bind/Staff/Simulate/Approve/Operate 技术化表单 | 把 Studio 当成用户必须完成的配置后台 | **REFACTOR** 为意图→Truth→proposal→reuse/compose→candidate；内部细节按需 | 不扩大 Package/Runtime；未知业务不被模板阻挡 |
| `frontend/app/ceo-office/organization/*` | Company/Department/Employee CRUD 与旧 map | 有数据 seam，产品表达不完全符合公司版图/员工目录 | **REFACTOR** 两个视图与 parent path；保留安全 CRUD | Company Spine、Role/Staffing semantics、no orphan |
| `frontend/app/ceo-office/talent-market/page.js` | 专家/技能/连接器 search、recruit、assign | 交互结构接近三 Surface；正式入口仍叫 talent-market | **RE-SKIN / REFACTOR** 为人才与能力；保留专家→员工边界 | 真实 provider/connector evidence、授权、撤回 |
| `frontend/app/ceo-office/analytics/page.js` | operating pulse、metric cards、queues | 经营洞察与 CEO Desk 边界混合 | **REFACTOR** scoped insights、source/freshness/unknown、compare | 真实指标来源；不造第二 Analytics Runtime |
| `frontend/app/ceo-office/knowledge/page.js` | Knowledge entries、local roots/files、import | 资料库基础存在 | **KEEP / REFACTOR** 为资料库 source/index/search/citation model | 外部连接、权限、source trace、no fake data |
| `frontend/app/ceo-office/meeting/page.js` | 空态/规划中占位 | 不承载会议 Current Product Truth | **REPLACE** | 会议 Page Contract、Decision/Responsibility 回写、后续 evidence |
| `frontend/app/ceo-office/settings/page.js` | profile/brand/notify tabs | 设置属于左下角头像；基础路由可保留 | **KEEP / RE-SKIN**，删除示例快照假象 | real data / brand configuration future direction |
| `/ceo-office/workspace/xhs`、`/shortvideo`、`/software` 及 RD/XHS components | Domain prototypes/instances | 是 Professional Surface / validation examples，不是固定业务导航 | **KEEP FUNCTION / REFACTOR ENTRY** | Professional Workspace candidate/verified boundary |
| `/ceo-office/projects`、`/execution`、`/runtime-trace`、`/company-runtime`、`/dev-console`、`/control/secret-vault`、`/platform/*` 等 | legacy/admin/runtime diagnostics | 非普通用户 Current product surface | **REMOVE AFTER REPLACEMENT** | replacement + tests + deep-link + Runtime dependency + regression |

## 5. Classification decisions

### KEEP

- Frozen Shell 的职责、Pane-local Header、Adaptive Context/Utility、Main 自成立与用户控制展开/收起。
- `WorkspacePaneShell` 的 pane state、resizable、utility maximize、company object search seam；导航数据本身需重构。
- Runtime/API adapters、Package renderer、Employee Workstation/Conversation-first 基础组件。
- Company / Business / Workspace canonical read-model 接线和 RD 的真实业务对象/Result/Evidence 功能。
- Frozen tokens、theme foundation 与已有真实状态投影能力。

### RE-SKIN

- Terra primitives、shell copy、status labels、Talent Market 路由/标题、Business/Workspace page headings。
- RD/XHS 页面中仍有价值的业务对象与动作，但去除“示例/技术控制台”作为普通用户主语义。

### REFACTOR

- 唯一七区导航与所有 deep-link。
- First Run、CEO Desk、Business directory、Organization map/directory、Talent & Ability、Insights、Studio。
- `Office/办公室` 仅在历史/实现字段出现时保留，不作为当前 UI 名称。
- Runtime/Simulation/Capability/Provider 只在需要时作为解释、阻塞和恢复信息出现。

### REPLACE

- 首次运行技术表单 → “你想开始做什么？”的意图入口，落到 Business + General/Professional Workspace。
- 会议占位页 → 真实会议产品空间（必须先有 Page Contract/实现授权）。
- 旧五/六项导航 → 七区 Current navigation。
- CEO Desk 的运行控制台式首屏 → 经营日/注意力/结果/决定投影。

### REMOVE AFTER REPLACEMENT

- Legacy project/execution/pipeline/runtime-trace/admin routes。
- `Curis_UI_Blueprint_Prototype.html`、`Curis_Product_UI_Flow_Pack.html`、旧 prototype 目录。

### REMOVE NOW

无。当前没有满足安全删除条件的对象；直接删除会破坏兼容路由、测试、迁移或历史 provenance。

## 6. Product → Frontend gaps

| Gap | Product Truth | Frontend evidence | Priority | Next gate |
|---|---|---|---|---|
| UI-001 | 七个一级区，人才与能力/经营洞察为正式名称 | `WorkspacePaneShell.js` 仍六项；`TerraNavData.js` 仍旧分组/旧名称 | P0 | route inventory + replacement nav + regression |
| UI-002 | 任意业务先从意图开始，模板不是门槛 | `onboarding/page.js` 是 FoundingRun technical form；未创建 canonical Business/Workspace | P0 | V1-P0-001 packaged first-run E2E |
| UI-003 | General Workspace 是真实可经营起点 | Business page 仅目录/新建 Workspace；Studio 偏 template configuration | P0 | atomic Business + First Workspace + generic operation |
| UI-004 | CEO Desk 是经营日投影 | 当前显示 Runtime snapshot、Resource Check、Simulation、staffing gate | P0 | CEO Desk page contract + ordinary-user evidence |
| UI-005 | 会议是事实/分歧/决定/跟进空间 | meeting page 明确规划中占位 | P0 | Meeting Page Contract + implementation issue |
| UI-006 | Organization 是公司版图 + 员工目录 | organization page 仍写 AI Workforce Map，混入 projects/capacity | P1 | Company Map page contract + data/read model proof |
| UI-007 | Workspace = real business product；Employee 不替代业务面 | generic installed route 可开，但普通业务入口/primary surface 未完整装配 | P1 | generic/professional product E2E |
| UI-008 | Talent & Ability 内部专家/技能/连接器，专家经招募才成为 Employee | route/label 仍 talent-market；能力与员工表达需统一 | P1 | recruit → employee evidence |
| UI-009 | Insights 是 scoped analysis，不是 Dashboard | analytics page 的脉搏/队列/机会卡仍偏 Dashboard | P1 | Operating Intelligence page contract + real source/freshness |
| UI-010 | Assistant 跨页面可达且上下文连续 | component seam 存在，continuous partner/attention 未完整 | P1 | context continuity + packaged revisit |
| UI-011 | Result/Evidence/Decision/Recovery 可回原上下文 | Runtime primitives 有，通用页面投影不完整 | P1 | ordinary-user recovery route evidence |
| UI-012 | 视觉必须遵守 Shared Shell 与 Domain Primary Surface | Domain high-fidelity 多为 reference only，当前 Frontend 整合未接受 | P1 | visual delta + browser QA |
| UI-013 | V1 必须 fresh packaged whole-app 可回访 | readiness audit 标记 whole-app E2E MISSING | P0 | isolated packaged run + restart/reload + regression |

## 7. Cleanup safety rules

本审计仅提出动作，不执行删除。任何后续开发 Issue 若要 `REMOVE`，必须先证明：

1. replacement 已完成并被接受；
2. existing route 与 deep-link 已迁移或有兼容策略；
3. Runtime / API / package / tests 不再依赖旧入口；
4. fresh Browser/Desktop 与 reload/restart regression 通过；
5. 删除范围、Owner、Review 和回退路径明确。

## 8. FINAL UI REBUILD STARTING POINT

如果下一轮重新开始最终 Curis UI，起点不是空白画布：

| 类别 | 起点判断 |
|---|---|
| 直接继承 | Frozen seven-area shell responsibility；Pane-local Header；Adaptive Context/Utility；Main = selected Professional Surface + Shared Work Area；Conversation-first Employee Workstation；真实状态、Result/Evidence/Decision、用户控制 pane 展开/收起。 |
| 只保留功能 | Runtime/API adapters、Canonical Business/Workspace read model、Package renderer、RD 的 code/build/test/review/result 功能、XHS 的对象/反馈语义；这些功能要迁入正确产品面，不继承旧页面 IA。 |
| 必须重新设计 | First Run 与 Business entry；CEO Desk operating-day；Business/Organization/Talent & Ability/Insights/Meeting 页面；General Workspace；Workspace Studio 的意图与复用路径；全局 Assistant/context continuity；Domain Primary Surface 的最终视觉。 |
| 最终应删除 | 旧六区/旧分组导航；技术化 onboarding；Meeting 占位；旧项目/执行/流水线/Runtime Console 入口；旧 prototype/Flow Pack；但都要在 replacement、测试、deep-link、Runtime 依赖与回归通过后删除。 |

**结论：Current UI Foundation 已有可复用骨架，但尚未成为完整普通用户产品。最终 UI 应从 Frozen Shell + canonical Company/Workspace seams + 已验证业务功能继续组装，而不是重新研究 Curis 或直接沿用旧页面。**

— STOP FOR CEO UI RECONCILIATION REVIEW
