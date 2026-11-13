# CURIS V1 — THREE-AREA SPECIALIZED DESIGN ASSET RECOVERY

**Authority Class**：REVIEW / DESIGN ASSET RECOVERY
**Status**：Review
**Date**：2026-08-31
**Scope**：Organization Center · Operating Intelligence · Meeting Room
**Disposition**：RECOVERED AS DESIGN INPUT; NOT A NEW UI AUTHORITY

> 本文件是历史设计资产恢复与 provenance 审计，不是 Product Blueprint、UI Blueprint、Figma 或 Frontend Authority。它不重新设计页面，不把 Demo、Prototype、截图或研究 Candidate 伪装成已接受视觉。Current 产品语义仍以 Pointer → Product Blueprint → Master Map → UI Blueprint → applicable Frozen Authority 为准。

## 0. Executive Summary

| Area | Product baseline | UX / composition evidence | Visual baseline | Recovery result |
|---|---|---|---|---|
| Organization Center | Company Map + Employee Directory；Company → Department → Business → Workspace → Role / Staffing → Employee | Variant A Department Container 与 Option C Hybrid Company Map 的关系已厘清；Business-first、Employee reverse lookup 已被研究消费 | `CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html` 是研究/Design Candidate，不是 Frozen visual；Figma 106:* 未能视觉核验 | Product / interaction direction recovered; final visual remains OPEN |
| Operating Intelligence | 跨 Company / Business / Workspace / Employee / Model / Capability / time 的经营分析消费面；不是 CEO Desk Dashboard | Accepted UX Baseline；Hybrid（C）方向，B skeleton → A Explore/Benchmark 的渐进表达 | `CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html` 是 `ACCEPTED UX BASELINE (DEMO)`，不是最终像素组成 | UX baseline recovered; final page composition remains OPEN |
| Meeting Room | Natural Conversation → Proposal → CEO Decision → Assignment → Work → Result / Review | Current Product/UI 语义已确认；coverage exploration 提供四个工作状态 | 没有发现已接受的专门会议视觉基线；旧 Strategy Room 与 coverage HTML 均为历史/探索 | Product semantics recovered; specialized visual acceptance NOT FOUND |

结论：三块资产没有丢失到“从零开始”。组织中心与经营洞察已有可消费的产品/交互依据；会议有产品语义和覆盖探索，但没有可称为最终视觉基线的已接受专门原型。下一步不是重新研究，而是将每块的 Final Inherit Package 交给后续 Visual Execution，并保留明确的开放项。

## 1. Retrieval Coverage and Evidence Rules

本轮搜索了 `docs/00_Context/`、`docs/01_Product/`、`docs/02_Architecture/`、`docs/03_Design/`、`docs/reviews/`、`deliverables/product-strategy/`、`curis-ui-prototype/`、`frontend/design-spec/`、`docs/99_Archive/` 及其截图、HTML、预览和 Figma 引用。

- 实际读取 HTML 的 `<title>`、页面结构、变体按钮/标签和交互文案；没有只凭文件名认定资产。
- 截图被映射到同目录 Prototype / Variant；单张截图不单独升级为 baseline。
- 没有可用的 Figma 读取连接或节点视觉证据时，只记录 `REFERENCE FOUND / VISUAL NOT VERIFIED` 或 `CANNOT DETERMINE`，不猜测画面。
- 研究、Review、Prototype、Demo 与 Current Product Truth 分层记录；历史文件不机械改写。

## 2. ORGANIZATION CENTER

### 2.1 Current Truth

当前 Product Blueprint / Master Map / UI Blueprint 的稳定语义是：

- 组织中心由 **公司版图** 与 **员工目录**组成，不是传统 HR Org Chart、平级 Agent 目录或第二套组织真相。
- 公司版图默认阅读 Company → Department → Business → Business Operating Model → Role Structure → Employee Binding；Business 进入 Business Detail / Operating Model，不直接跳入 Workspace；Role 展开后才看 Employee Binding。
- Employee Directory 从 Employee 反查 Role / Business / Department。
- Business 是唯一 canonical user/product identity；Workspace 是 Business 下独立工作空间。旧 Office 仅保留历史/实现/migration provenance，不作为当前用户身份。

**Current Product Authority**：`/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Blueprint.html`、`/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Master_Map.md`、`/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_UI_Blueprint.html`。
**Current interaction direction**：Company Map / Department Container 已被 CEO 接受为产品/交互方向；这不等于某个 HTML 或 Figma 已成为最终视觉。

### 2.2 Timeline and Recovered Assets

| Stage | Source / exact path | Status | What it establishes |
|---|---|---|---|
| Initial product/page contract | `/Users/yy/Documents/Curis AI Workspace/docs/reviews/ORGANIZATION_CENTER_PAGE_CONTRACT_FINAL_REVIEW.md` | REVIEW; CEO consolidated decision applied, final visual not accepted | 公司版图 + 员工目录；Variant A `Department Container`；Business first、Role/Employee progressive disclosure、空岗/风险/扩张表达、从组织处调整结构、从工作面添加业务对象 |
| Company Map research | `/Users/yy/Documents/Curis AI Workspace/docs/03_Design/CURIS_COMPANY_MAP_ORGANIZATION_GRAPH_RESEARCH.md` | RESEARCH; `CONSUMED BY CURRENT PRODUCT TRUTH` | Option A Enhanced Hierarchy Tree、Option B Business Portfolio、Option C Hybrid Company Map；推荐 Option C：Department containers + Business primary nodes + Role chip + separate Employee Directory |
| Actual visual exploration | `/Users/yy/Documents/Curis AI Workspace/docs/03_Design/CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html` | RESEARCH / informal high-fidelity / Design Candidate | 实际可读 HTML；Variant A（Department container，recommended）与 Variant B（horizontal hierarchy）可切换；搜索、状态筛选、缩放、部门聚焦、Business→Role→Employee 展开、Business detail drawer、进入 Workspace、复制 Business 演示 |
| Older organization prototype | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/ai-organization.html` | HISTORICAL PROTOTYPE | `AI 团队办公室`、组织异常、团队快照、安排团队、运行负载、能力添加；含旧 Global Topbar、旧绿色强调与能力控制台语言，不是 Current visual authority |
| Coverage exploration | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/coverage-exploration-2026-08-17/03-org-center.html` | COVERAGE EXPLORATION / NOT AUTHORITY | 组织总览、部门、员工列表、员工能力、招聘/组队四个 tabs；使用四 Pane shell，验证了状态和入口覆盖，不代表最终 IA/视觉 |
| Legacy HTML | `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/ceo-office/org-center.html`; `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/curis-ui-v2/pages/org-center.html` | HISTORICAL / SUPERSEDED FOR CURRENT COMPOSITION | 旧“组织空间总览/组织健康/部门空间”与旧 HR/轨道舞台假设；仅保留 provenance |
| Screenshot references | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/p1-preview/ai-organization-light.png`, `.../ai-organization-dark.png`; `/Users/yy/Documents/Curis AI Workspace/docs/99_Archive/design/curis-ui-v2/docs/ui/figma/org-center-default.png`; `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/curis-ui-v2/audit-evidence/org-center-1440.png` | REFERENCE / HISTORICAL | 可用于回看旧密度与布局，不足以证明当前视觉接受 |
| New Figma section | Figma `106:2`, frames `106:3`, `106:230`, `106:457`（用户提供的设计线索） | DESIGN CANDIDATE; `CANNOT DETERMINE` visually in this run | 未取得可核验的 file/frame/node 视觉内容；不得替代已恢复的 Product/interaction direction |

### 2.3 Variant Reconciliation

- **Page Contract Variant A — Department Container**：解决 Department 不应成为传统 HR 树根的问题，Department 是容器，Business 是第一视觉对象，Role/Employee 按需展开。
- **Research Option A — Enhanced Hierarchy Tree**：完整 Company→Department→Business→Role→Employee 树，信息完整但默认层级深、容易退回组织图。
- **Research Option B — Business Portfolio / Company Map**：Business first，看业务组合、扩张、风险和结果，Role/Staffing 下钻。
- **Research Option C — Hybrid Company Map（推荐）**：B 的 Business-first 默认阅读 + Department containers + Business 内 Role chip + 单独 Employee Directory。它不是与 Variant A 冲突的第四套模型；Variant A 是容器模式，Option C 是采用该容器后的整体组合。
- HTML exploration 的 Variant A / B 是视觉探索开关，不是新的 Product Authority，也不代表 Option C 已被像素冻结。

### 2.4 Current Baseline

- **Product Baseline**：公司版图 + 员工目录；Company Map 的使命是让 CEO 看见公司长成什么样、业务扩张到哪里、哪里空岗/有风险。
- **UX / Composition Baseline**：Department Container + Business-first Hybrid Company Map；Employee 默认隐藏，目录负责反查；Business Detail / Operating Model 是下钻，不把 Workspace 直接塞进版图。
- **Visual Baseline**：`VISUAL BASELINE: OPEN`。`CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html` 仅为参考候选；Figma `106:*` 视觉未验证。

### 2.5 Organization Final Inherit Package

**Product Authority**：当前 Company Map / Employee Directory 语义、Business canonical identity、Business→Workspace 关系。
**UX Contract**：Department Container、Business-first、Role/Staffing progressive disclosure、Employee reverse lookup、Business Detail → Workspace 明确入口。
**Accepted/consumed research**：`CURIS_COMPANY_MAP_ORGANIZATION_GRAPH_RESEARCH.md` 的 Option C / Hybrid 方向（研究已消费，不是并列 Authority）。
**Visual reference**：`CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html`；仅作交互与信息密度参考。
**Do Not Use**：旧 Office 作为当前身份；传统 HR Org Chart；旧 Global Topbar；把所有 Employee 默认铺开；把 HTML Demo 数据当真实组织；把 Figma 106:* 当已验收画面。

**Solved / do not redesign**：组织中心不是传统 HR 图；Business 是第一视觉对象；Employee Directory 与公司版图分离；Business 点击进入 Business Detail 而非直接 Workspace。
**Open for Visual Execution**：最终节点密度、空/增长/风险状态、深色/浅色、1024/窄屏、Map 与 Directory 的切换表达、Figma 106:* 是否与方向一致。

## 3. OPERATING INTELLIGENCE

### 3.1 Current Truth

经营洞察是第七个一级产品空间，但不是 CEO Desk Dashboard，也不建立第二套 Truth / Result / Analytics Runtime。它消费已有 Company Truth、Result、Usage、Cost、Execution、Feedback、Review，并支持 Company、Business、Workspace、Employee/Team、Model/Agent/Provider、Capability 与时间周期的 scoped 分析。

CEO Desk 负责注意力、异常、简报、结果、待处理和下一决定；经营洞察负责深度查看、趋势、比较、归因和经营评估。所有指标必须保留来源、新鲜度、verified/manual/unknown/stale/missing 等信任信息；无真实来源不得显示虚构成本或健康分数。

### 3.2 Timeline and Recovered Assets

| Stage | Source / exact path | Status | What it establishes |
|---|---|---|---|
| Initial analysis/product direction | `/Users/yy/Documents/Curis AI Workspace/deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_RESEARCH.md` | RESEARCH / consumed | 经营问题优先于图表；Company/Business/Workspace/Org/Model/Capability/Reports 等分析范围；Desk 与 Insights 边界 |
| UX research | `/Users/yy/Documents/Curis AI Workspace/deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_UX_RESEARCH.md` | RESEARCH; `CONSUMED BY CURRENT PRODUCT TRUTH` | Scope Rail + Context Bar；Company Overview、Business Analysis、Org/Employee、Model/Capability、Reports、Analyst；Variant A/B/C；建议 B skeleton first，再 A Explore/Benchmark |
| Consolidation / CEO acceptance | `/Users/yy/Documents/Curis AI Workspace/deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_UX_CONSOLIDATION.md` | `ACCEPTED — OPERATING INTELLIGENCE UX BASELINE`; consumed by Current Product Truth | Hybrid Operating Intelligence、Company Analyst / Business Analyst、Data Trust、five core visualization patterns、report/conversation/review/decision loop；明确 DEMO 不是真实 Runtime |
| Actual UX exploration | `/Users/yy/Documents/Curis AI Workspace/deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html` | `ACCEPTED UX BASELINE (DEMO)`; not final visual composition | 实际可读 HTML；Variant A Dashboard、B Analyst、C Hybrid 可切换（默认 C）；Overview、Explore、Analyst、Report、Scoped Analysis、Decision Support、Data Trust、Benchmark、趋势与报告状态均有交互占位 |
| Visualization research / later delta | `/Users/yy/Documents/Curis AI Workspace/deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_VISUALIZATION_RESEARCH.md` | RESEARCH; consumed | 问题→图族、基线优于绝对值、成本/延迟/质量分离、可比性声明、AI 解读不计算；不冻结最终图表/页面 |
| Supporting HTML/legacy pages | `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/curis-ui-v2/pages/analytics.html`, `analytics-workflow.html`, `analytics-org.html`, `reports.html`, `report-detail.html`; `/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/analytics/page.js` | HISTORICAL / IMPLEMENTATION REFERENCE | 旧 analytics/reports 结构和现有 route seam；不应反向决定当前 Operating Intelligence IA |

**Timeline gaps**：未发现一份独立、CEO 明确签收且像素级冻结的 Operating Intelligence final visual file；现有 HTML 是已接受 UX Baseline（Demo），不是 Final Visual Design。Figma 专用 frame/key 未在本轮研究材料中得到可核验记录。

### 3.3 Variant Reconciliation

- **Variant A — Dashboard / Explore First**：图表网格、Explore、筛选；熟悉但容易变成 BI 压力墙。
- **Variant B — Analyst / Report First**：先给结论、报告和分析师；更接近 CEO 阅读，但探索能力较弱。
- **Variant C — Hybrid Operating Intelligence**：Company Overview + Explore + Analyst + Report + Scoped Analysis + Decision Support；是研究整合后的最完整方向，但不意味着首屏必须同时铺满所有模块。
- 当前被消费的方向是“C 的能力范围，B skeleton first，再渐进暴露 A 的 Explore/Benchmark”，保持低表面复杂度；这是 UX 基线，不是新 Runtime。

### 3.4 Current Baseline

- **Product Baseline**：经营洞察 = 既有经营事实的跨层分析消费面；CEO Desk 与 Insights 的职责分离固定。
- **UX / Composition Baseline**：Scope + 时间 + 结论/报告 + Explore/Benchmark + Data Trust + Conversation/Decision 回路；图表是回答问题的工具，不是入口墙。
- **Visual Baseline**：`CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html` = `ACCEPTED UX BASELINE (DEMO)`；最终页面 composition、密度、主题和各 scope 的实际组件仍 `OPEN`。

### 3.5 Operating Intelligence Final Inherit Package

**Product Authority**：经营洞察第七区、分析维度、Desk/Insights 边界、来源/新鲜度/未知语义。
**UX Contract**：Hybrid capability envelope；Analyst-first skeleton、可探索/比较/下钻、报告可追溯、Data Trust 可见、返回原上下文。
**Accepted prototype**：`CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html`，仅以 DEMO/UX baseline 身份继承。
**Later correction consumed**：Visualization research、Analyst organization、semantic-safe comparison 与五类核心可视化；不扩大页面或 Runtime 对象。
**Do Not Use**：旧 BI Dashboard wall、没有来源的 health score、把 Demo 数字当 Runtime、把 AI Analyst 变成角落聊天、把 CEO Desk 与 Insights 合成第二个提醒中心。

**Solved / do not redesign**：不是 Dashboard-first 的产品心智；Fact / Interpretation / Unknown / Recommendation 分层；成本、速度、质量、验收和外部结果可关联比较；分析后可回 Conversation / Review / Decision。
**Open for Visual Execution**：首屏具体区块、图表和表格比例、scope切换密度、无数据/手动回填/冲突来源状态、深色/浅色、1024/窄屏、Analyst 与 Report 的具体视觉编排。

## 4. MEETING ROOM

### 4.1 Current Truth

会议是七个一级产品空间之一，用于事实、分歧、方案、决定和后续责任的连续工作面。会议不是普通聊天记录，也不是独立的 Handoff、Notification 或 Recovery Console。

Current semantics：自然 Conversation 中由 AI 识别 Question / Fact / Opinion / Evidence / Risk / Proposal；CEO 可批准、修改、拒绝或延后；形成 Decision / Assignment / Owner / Checkpoint，回到来源 Business / Workspace / Employee Workstation，继续 Work → Result / Evidence → Review。Company Meeting 与 Workspace Meeting 共享该语义，影响公司方向/跨业务资源/高影响承诺时才升级为 Company 会议。

### 4.2 Timeline and Recovered Assets

| Stage | Source / exact path | Status | What it establishes |
|---|---|---|---|
| Initial product definition | `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis 产品梳理 1.0_副本/Product Bible v1.0/09 会议室（Meeting Room）.md` | HISTORICAL PRODUCT DRAFT | 实时会议与后台研讨；目标澄清、方案讨论、风险评估、决策、任务生成；参与者、预算、准备/讨论/总结/决策阶段 |
| Early visual prototype | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/meeting.html` | HISTORICAL PROTOTYPE | 外部合作方周会、Operating Day、AI 准备背景/事实/未知、CEO 确认承诺与决议；不是当前视觉基线 |
| Legacy strategy room | `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/ceo-office/strategy-room.html`; `/Users/yy/Documents/Curis AI Workspace/frontend/design-spec/curis-ui-v2/pages/strategy-room.html` | HISTORICAL / SUPERSEDED FOR CURRENT COMPOSITION | 旧“战略会议室”、会议列表、战略级会议空间、固定卡片/上下文；不得冒充后来接受的 Meeting Room 设计 |
| Coverage exploration | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/coverage-exploration-2026-08-17/06-meeting.html` | COVERAGE EXPLORATION / NOT ACCEPTED VISUAL | 实际 HTML，标题 `会议 · Curis`；F1 会议首页、F2 创建会议、F3 Company/Workspace Meeting 工作面、F4 Proposal / Decision；中央 Conversation、议程/资料 Context、Proposal/Decision 按需展开、Composer 语义槽位 |
| Archived screenshots | `/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/p0-preview/meeting-light.png`, `meeting-dark.png`, `p1-preview/meeting-light.png`, `meeting-dark.png`; `/Users/yy/Documents/Curis AI Workspace/docs/99_Archive/design/curis-ui-v2/docs/ui/figma/strategy-room-default.png` | REFERENCE / HISTORICAL | 旧或覆盖探索的截图，未找到对应 CEO final acceptance provenance |
| Current product/UI contract | `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Blueprint.html`; `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Master_Map.md`; `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_UI_Blueprint.html` | CURRENT PRODUCT/UI TRUTH | 会议作为自然 Conversation → Decision → 责任/结果回流的产品空间；具体最终视觉仍未冻结 |

### 4.3 Missing Links and Status

- **INITIAL RESEARCH**：FOUND（Product Bible v1.0），但属于历史 draft。
- **UX EXPLORATION**：FOUND（coverage exploration `06-meeting.html`），是覆盖验证，不是 Final Design。
- **VARIANTS**：`NOT FOUND` 作为有明确 A/B/C 命名并被 CEO 选择的专门 Meeting 视觉变体；旧 Strategy Room 不算目标变体。
- **CEO REVIEW / CORRECTION / ACCEPTED DIRECTION**：Current Product/UI 语义有明确收敛，但本轮未找到独立“会议专门视觉 Accepted”记录，标记 `NOT FOUND`。
- **LATER DELTA**：未发现一份已接受的 Meeting-specific visual delta；通用 Composer、Pane-local Header、Conversation/Decision 规则属于 Shared Authority，不是会议专属视觉签收。
- **CURRENT BASELINE**：Product baseline = FOUND；UX contract = FOUND；specific visual baseline = `OPEN`。

因此，专门会议室的后续原型并非完全不存在：coverage exploration 原型确实存在；但“已经形成并被接受的最终会议室视觉基线”没有被找到，不能用旧 `/meeting`、旧 `strategy-room` 或单张截图补齐这一缺口。

### 4.4 Meeting Final Inherit Package

**Product Authority**：Meeting = bounded Conversation → Proposal → CEO Decision → Assignment / Checkpoint → Workspace Work → Result / Review。
**UX Contract**：Full Main Conversation；成员、议程、资料、Proposal 作为 Context/Utility/按需 Focus；决定必须带来源、责任、下一步和追踪。
**Recovered prototype**：`coverage-exploration-2026-08-17/06-meeting.html`，仅作为状态/交互参考，未接受。
**Visual reference**：旧 `meeting.html`、`strategy-room.html`、归档 PNG 只能作历史对照；没有 Accepted final visual。
**Do Not Use**：战略会议室作为默认产品身份；固定卡片墙；把会议当普通聊天归档；把 Proposal/Member/Resource 永久挤成右栏；把 coverage Demo 数据当真实会议。

**Solved / do not redesign**：会议不是第二任务系统；Conversation 是主工作面；AI 识别结构、CEO 决策、责任回流和结果追踪已经由 Current Product Truth 定义。
**Open for Visual Execution**：首页与具体会议工作面的构图、实时/后台研讨的差异表达、议程/资料/Proposal 的按需层级、Decision/Commitment/Checkpoint 的视觉权重、空/失败/等待/重启、Company 与 Workspace context、浅色/深色/窄屏。

## 5. Cross-area Supersession and “Do Not Draw” Rules

| Legacy / candidate pattern | Treatment |
|---|---|
| Organization traditional HR tree / Office identity | HISTORICAL / SUPERSEDED FOR CURRENT PRODUCT LANGUAGE |
| Organization HTML demo data / Figma 106:* without visual verification | REFERENCE ONLY / DO NOT ACCEPT |
| Operating Intelligence BI dashboard wall / ungrounded health score | SUPERSEDED by Operating Intelligence UX Baseline |
| Operating Intelligence DEMO figures | NOT RUNTIME TRUTH |
| Legacy strategy room / `/meeting` placeholder | HISTORICAL; not target specialized visual baseline |
| Coverage exploration tabs treated as final IA | NOT ACCEPTED; use only for state coverage |
| Any prototype’s old green palette or global topbar | SUPERSEDED by Frozen Visual Standard / Shell Authority |

三块都必须继续服从已冻结的结构性规则：七区导航、Shared Workspace Shell、Pane-local Header、Main = selected Professional Surface + Shared Work Area、Runtime State ≠ UI Expand/Collapse State、Employee Shared UI Status 三态、真实来源与空态纪律。结构 Frozen 与视觉语言 Frozen 分开消费；页面 composition 仍须专项设计。

## 6. Final Inherit Package Summary

| Area | Inherit directly | Inherit as reference only | Must not be carried forward |
|---|---|---|---|
| Organization Center | Company Map mission; Department Container; Business-first; Role/Staffing progressive disclosure; Employee Directory reverse lookup | Company Map Visual Exploration HTML; coverage org-center HTML; screenshots | Office as current identity; default employee wall; HR chart; unverified Figma 106:*; demo data |
| Operating Intelligence | Operating Intelligence product boundary; Hybrid capability envelope; Analyst/Report/Data Trust loop; Desk vs Insights boundary | Accepted UX Exploration HTML (DEMO); visualization research patterns | BI wall; unsupported metrics; second Truth/Analytics Runtime; DEMO numbers as facts |
| Meeting Room | Conversation → Proposal → Decision → Assignment → Work → Result/Review; full main conversation; source/owner/checkpoint | coverage `06-meeting.html`; early meeting and strategy-room screenshots/HTML | Strategy Room legacy composition; meeting as archive/chat; permanent right-column conversation; unaccepted prototype as baseline |

## 7. Required Answers for the Next Visual Execution Gate

1. **Organization Center**：Recovered direction is Department Container + Hybrid Company Map. The accepted product/interaction direction is sufficient to begin a bounded visual exploration; final visual is not yet accepted.
2. **Operating Intelligence**：Recovered direction is Accepted UX Baseline with Hybrid capability envelope and Analyst-first progressive disclosure. Visual composition remains open; do not restart research.
3. **Meeting Room**：A later specialized coverage prototype exists, but no accepted final specialized visual baseline was found. It requires a focused Visual Execution / Review pass, not a product-model rewrite.

## 8. Governance and Next Action

- This document is the only new artifact produced by this recovery task: `Status: Review`, `Authority Class: REVIEW`.
- No Product Blueprint, Master Map, UI Blueprint, Runtime, Schema, DB, Frontend, Prototype or Figma was modified.
- No Pointer / CURRENT_STATE / Change Log update is made: this is a read-only recovery artifact, not a Current Authority change. If CEO accepts it as an input, the acceptance should be registered through a separate bounded governance action rather than silently promoted here.
- Next action is area-specific Visual Execution: consume the three Final Inherit Packages; do not recreate Product Truth, do not treat historical prototypes as final, and do not design all three areas as one generic dashboard.

THREE-AREA SPECIALIZED DESIGN ASSETS RECOVERED
— ORGANIZATION DIRECTION RECOVERED
— OPERATING INTELLIGENCE UX BASELINE RECOVERED
— MEETING PRODUCT SEMANTICS RECOVERED; ACCEPTED SPECIALIZED VISUAL NOT FOUND
— NO AUTHORITY / IMPLEMENTATION CHANGE
— STOP FOR CEO REVIEW
