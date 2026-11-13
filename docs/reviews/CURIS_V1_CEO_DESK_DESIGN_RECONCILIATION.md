# CURIS V1 — CEO DESK CURRENT DESIGN RECONCILIATION

**Status:** Review
**Authority Class:** REVIEW / HISTORICAL DESIGN RECONCILIATION
**Disposition:** STOP FOR CEO / CHATGPT REVIEW
**Date:** 2026-08-28
**Scope:** 只对账 CEO Desk 的既有产品结构、设计资产与当前共享规则；不新建 IA、视觉方向、Figma 设计或实现

## 1. Executive conclusion

CEO Desk 已经被多轮真实设计过，不需要从空白重新研究。最成熟的可复用组合是：

1. 产品结构：`docs/reviews/CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md`（Review / ACCEPTED CANDIDATE）。
2. 当前 Operating / Matters Present 构图：Figma `CEO Desk — Operating / Matters Present`（`69:3`），已登记为 CEO Desk Current Operating Design Baseline；范围是 1440 × 900、Light，不代表所有状态或实现均已完成。
3. 历史运营场景参考：Figma `Operating Result — Final Spatial Polish`（`81:113`）及 Shell `81:3`，保留结构与层级 provenance，但不再是 Current UI Baseline。
4. 空态与共享壳层参考：Figma `Empty Curis — CEO Desk 1440w light`（`1:424`）及 `Empty Company — CEO Desk 1440w light`（`1:1515`），来自当前 App Entry baseline，仍需遵守 6 px shell overrun 记录。
4. 可运行 HTML 参考：`curis-ui-prototype/coverage-exploration-2026-08-17/01-ceo-desk.html`，结构覆盖完整但旧六区导航与旧视觉已被 Current Authority 替代，因此只能 `UPDATE`。

结论不是重新设计：下一步应是 **REUSE 69:3 → ADAPT → IMPLEMENT**；只处理 Dark、1024、密度、展开态和真实数据投影等适配/验证，不启动新的 CEO Desk 构图或 Trae 重画整页。

## 2. Current CEO Desk product purpose

Current CEO Desk 的唯一使命是：

> 让 CEO 用最少注意力知道公司发生了什么、什么值得现在打扰、什么需要自己决定、哪些责任要继续跟进，以及决定之后公司如何继续。

Current Page Contract 已确定的信息职责为：

`Desk Header → Today Brief → Matters → Decision / Exception / Handoff → Important Results → Follow-up / Closeout → Assistant（按需）`

这些是 Information Responsibilities，不要求分别绘制成独立 Card 或 Dashboard Block。Decision、Exception、Handoff 优先作为 Matter 类型或下钻内容。CEO Desk 不承担完整指标仪表盘、结果归档、完整组织图、业务后台、任务台、通知中心或独立聊天首页；深度分析由经营洞察承担。

**Authority source:** `docs/reviews/CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md` §1–§5，`Status: Review / ACCEPTED CANDIDATE`。

## 3. Historical authority inventory

| Source | Status | What it established | Current treatment |
| --- | --- | --- | --- |
| `docs/01_Product/Curis_Product_Blueprint.html` | Current Product Authority | CEO 工作台、公司经营循环、Result / Evidence / Decision、Assistant、七区与 Main 责任 | KEEP；只消费后续 Page Contract / Visual Standard，不在 Blueprint 重新构图 |
| `docs/01_Product/Curis_Product_UI_Blueprint.html` | Current UI Authority | CEO Desk 是七区中的 CEO 工作台；Shared Shell、Main、Assistant、Employee Work Area、Result / Evidence 入口 | KEEP；继续作为结构真源 |
| `docs/reviews/CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md` | ACCEPTED CANDIDATE | Mission、Entry/Return、Brief、Matters、Decision、Results、Follow-up、跨日连续性与 Assistant 边界 | KEEP；下一设计的产品输入，不是已批准像素稿 |
| `curis-ui-prototype/coverage-exploration-2026-08-17/02-QUALITY-REVIEW.md` | Historical Review | `01-ceo-desk.html` 覆盖 Brief、Decision、Current Run、Result Review、首次创建、空态；当时认定结构稳定 | 结构可复用；六区导航、旧文案和旧视觉 SUPERSEDED |
| `docs/reviews/2026-08-03-curis-ui-prototype-review.md` | Deprecated | 早期完整页面覆盖和 CEO Desk 六段骨架 | 仅历史 provenance；不作 Current UI Authority |

## 4. Historical design asset inventory

### 4.1 Figma — Theme Exploration

File: [Curis Theme Exploration Review](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82)

| Frame | Node | Status / value |
| --- | --- | --- |
| Shell Default — Company Operating Presence | `68:3` | `PARTIAL / USEFUL`；公司存在感与安静状态参考，空间仍偏 SaaS |
| Operating Result — Company Rhythm | `68:203` | `PARTIAL / USEFUL`；Result → Owner → Work → Next 语义参考 |
| Shell Default — Company Space | `75:3` | `PARTIAL / STRONG`；去 Hero-card、开放公司空间方向，但过空 |
| Operating Result — Company Space | `75:160` | `PARTIAL / STRONG`；空间身份增强，经营场景过分散 |
| Shell Default — Final Spatial Polish | `81:3` | `PARTIAL / STRONG`；最成熟 Shell / company-first 参考，仍未接受 |
| Operating Result — Final Spatial Polish | `81:113` | `HISTORICAL / REFERENCE`；曾是最成熟 Operating Result / Operating Scene 参考，Current Operating Baseline 已升级为 `69:3` |

Earlier `3:*`, `23:*`, `42:*` frames remain historical research. Green/terminal, warm/terracotta and Mineral Blue visual branches are superseded by Direction D;它们的层级/密度观察可保留，颜色和页面构图不可继承。

### 4.2 Figma — App Entry & CEO Assistant Experience

File: [Curis V1 — App Entry & CEO Assistant Experience](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=0-1&p=f)

| Frame | Node | Current reuse |
| --- | --- | --- |
| Empty Curis — CEO Desk 1440w light | `1:424` | KEEP shared shell / truthful empty state；6 px shell overrun待增量修正 |
| Empty Company — CEO Desk 1440w light | `1:1515` | KEEP Company Ready / No Business 空态语义；不伪造经营数据 |
| CEO Assistant — No Model 1440w light | `1:821` | KEEP Assistant identity、模型缺口、Conversation surface |
| CEO Assistant — 模型已启用 1440w light | `1:1292` | KEEP Assistant Conversation + Model Selector pattern |
| CEO Assistant — 切换模型 1440w light | `1:2428` | KEEP scoped Model Selector；菜单间距缺陷需后续修正 |

App Entry audit（`docs/reviews/CURIS_V1_APP_ENTRY_FIGMA_BASELINE_AUDIT.md`）明确这些 Frame 可编辑但无共享 Component Instance；它们是当前共享模式基线，不是 CEO Desk 最终构图。未在本轮修改 Figma。

### 4.3 HTML / prototype assets

| Asset | Status | Assessment |
| --- | --- | --- |
| `curis-ui-prototype/coverage-exploration-2026-08-17/01-ceo-desk.html` | Historical implementation reference | 覆盖度最高的可运行 Desk 参考之一；结构可复用，旧六区、旧绿色、Dashboard/card-heavy 视觉需替代 |
| `curis-ui-prototype/ceo-desk.html` | Legacy prototype | Brief Header、Assistant Brief、Company Pulse、Matters、Timeline、Handoffs 六段骨架；含旧硬编码业务样本，不能作为 Current identity |
| `.design/curis-hifi-v1/pages/ceo-desk.html` | High-fidelity historical | 同一旧产品结构，蓝色/绿色旧视觉；仅保留功能和信息分层参考 |
| `curis-ui-prototype.bak/ceo-desk.html` | Backup / history | 不作为实现或设计入口 |

## 5. Product structure truth

| Responsibility | Current status | Source |
| --- | --- | --- |
| Company-scoped brief and change summary | FROZEN / ACCEPTED | CEO Desk Page Contract §2, §5.2 |
| CEO attention matters | FROZEN / ACCEPTED | Page Contract §5.3；Matter 不是 Task List / Notification Center |
| CEO Decision Package entry | FROZEN / ACCEPTED | Shared Decision Package / P7；高风险事项必须完整包与证据 |
| Result / Evidence / Acceptance | FROZEN / ACCEPTED | Result 仍回到 Business / Workspace 来源，Desk 只显示重要结果 |
| Responsibility / Handoff / Exception follow-up | FROZEN / ACCEPTED | Page Contract §5.6；保留 Owner、原因、检查点与关闭条件 |
| Operating-day cross-day continuity | ACCEPTED CANDIDATE | Day N 未完成责任、Decision、Risk、Exception、Result 等承接 Day N+1 |
| CEO Assistant | ACCEPTED / current product semantics | Company-level coordinator + Conversation Surface；按需进入，不占固定秘书栏 |
| Seven-area navigation / Four-Pane shell | FROZEN / ACCEPTED | Current Product/UI Blueprint + Frozen Shell |
| CEO identity / Avatar | REVIEW READY / shared pattern | `CURIS_AVATAR_IDENTITY_PATTERN.md`；可选头像，不改变 Desk truth |
| Operating Intelligence | CEO ACCEPTED PRODUCT DIRECTION | 经营洞察负责深度分析；Desk 不变成 Dashboard |

## 6. Historical composition truth

### KEEP

- Brief → Matters → Decision / Exception / Handoff → Important Results → Follow-up 的信息叙事。
- Company / Business / Employee / Result 的来源回溯和返回原上下文。
- Empty Curis / Empty Company 的真实空态，不生成假 Company、Business、Result 或指标。
- Assistant 作为 Company-level coordinator 与按需 Conversation Surface，而不是独立秘书栏。
- Employee presence、责任、当前 Work 与结果的轻量表达；Employee Workstation 不是整个 Desk 主视觉。

### UPDATE

- 历史六区导航 → 当前七区导航；不要重做 IA。
- 旧 `#32f08c`、蓝色第二 accent、渐变、暖色和重卡片 → Direction D：`#806BE5`、Neutral Foundation、Calm Density、Open Canvas / Tonal Field。
- 旧 Assistant Brief / 固定 Chat drawer → 当前 Global Assistant + scoped Conversation / Model Selector / Avatar pattern。
- “软件开发 / 短视频”等硬编码示例 → Company / Business / Workspace current truth；验证样本不能变成默认业务。
- CEO Desk 直接展示大量指标 → 仅保留注意力与重要结果；深度趋势、比较、归因进入经营洞察。

### ADAPTATION / VALIDATION ONLY

- Dark、1024 与更高 Matters 密度的派生适配。
- Assistant Expanded、Decision Expanded、Evidence Expanded 的按需状态。
- 多 Business / 多 Workspace 同时变化时的排序与密度验证。
- Day N → Day N+1 的 Closeout / Carry-forward 最小表达。
- 真实 Attention Ranking、Runtime 数据投影与可访问性验证。

以上不重新打开 `69:3` 的 Main Composition。

## 7. Current App Entry shared patterns to inherit

直接继承当前 App Entry Figma 的：

- 七区 Navigation 与 Sparse Iris cue；
- CEO Display Name + optional Avatar；
- CEO Assistant first presence、No Model / Model Enabled 状态；
- Conversation stream、Composer、Model Selector；
- Empty Curis / Empty Company 的真实空态与 Create Company / Create Business 入口；
- 共享 Pane-local Header、Context/Utility 按需出现、完成后回原上下文。

不要直接继承：6 px shell overrun、未复用的独立 Frame 组件副本、具体 placeholder avatar、旧色彩或任何未接受的 Desk 构图。

## 8. Superseded visual elements

以下只在历史中保留，不是 Current Visual Authority：

- `#32f08c` 作为品牌主色；
- Mineral Blue、暖棕/terracotta、黑绿 terminal 风格；
- Card Wall、Dashboard Wall、固定多栏指标墙；
- 把 Assistant 做成 CEO Desk 固定右侧秘书栏；
- 把 Employee Workstation 做成 Desk 最大主视觉；
- 旧六区导航、全局 Topbar 或页面私有侧栏；
- 旧 HTML 中把 XHS / RD 作为默认产品业务的硬编码文案。

视觉替代依据：`docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`（Direction D，Status Frozen）。产品结构替代依据：Current Product/UI Blueprint、Frozen Shell、CEO Desk Page Contract。

## 9. Exact recommended next action

1. 不启动新 CEO Desk 研究，不消耗 Trae 重新画完整页面。
2. 以 `CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md` + `69:3` + App Entry Figma shared patterns 为结构基线。
3. 对 `69:3` 做受限适配矩阵：Dark、1024、密度、空态/有事项态、Assistant/Decision/Evidence 按需展开与真实数据投影。
4. 进入 `CEO DESK IMPLEMENTATION / ADAPTATION READINESS REVIEW`；Frontend 实施另需 Approved Design、依赖审计与回归证据。

### Operating UI acceptance registration

`CEO Desk — Operating / Matters Present`（Figma `69:3`）现登记为 **CEO DESK PRODUCT STRUCTURE: ACCEPTED**、**CEO DESK OPERATING COMPOSITION: ACCEPTED**、**CEO DESK OPERATING UI: UI ACCEPTED**、**CURRENT OPERATING DESIGN BASELINE: 69:3**。这只覆盖 1440 × 900、Light 的 Operating / Matters Present；其余状态是 Adaptation / Validation，不应被误写为全部设计完成。**IMPLEMENTATION READY: PENDING ENGINEERING RECONCILIATION；IMPLEMENTED: NO。**

## 10. Direct answers

**A. CEO Desk 以前到底有没有真正设计过？**
有。至少有多版可运行 HTML、早期高保真 HTML、Figma Operating Result / Shell Default，以及当前 App Entry 的 Empty Curis / Empty Company Desk。它不是未设计页面。

**B. 最成熟的一版具体是哪一个文件 / Frame？**
产品上最成熟的是 `CEO_DESK_PAGE_CONTRACT_FINAL_REVIEW.md`；当前视觉基线是 Figma `CEO Desk — Operating / Matters Present`（`69:3`）。`81:113` 与 `1:424` 继续作为历史运营/空态参考。可运行 HTML 则以 `coverage-exploration-2026-08-17/01-ceo-desk.html` 为结构参考，但不是 Current UI。

**C. 哪些产品结构已经确定，绝不能重做？**
CEO Desk Mission、Brief/Matters/Decision/Result/Follow-up 信息职责、七区导航、Four-Pane、返回原上下文、Result/Evidence 来源、Assistant Company-level coordinator 边界、真实空态与不虚构数据。

**D. 哪些只是旧视觉，需要换成 Direction D？**
旧绿色 `#32f08c`、蓝/暖色分支、渐变、Card/Dashboard Wall、Terminal 风格、固定 Assistant 侧栏，以及旧 HTML 的重卡片密度。

**E. CEO Assistant 加入以后具体影响哪里？**
Desk 只增加按需 scoped 入口、解释 Brief/Matter、准备 Decision、路由和跟进；不新增秘书栏、聊天首页、Task/Decision 系统，也不替代 Team Leader / Domain Expert。

**F. 当前 App Entry Figma 哪些组件直接继承？**
Navigation、Pane-local Shell、CEO identity/avatar、Assistant identity、Conversation、Composer、Model Selector、Empty Curis / Empty Company 空态，以及返回原上下文规则。

**G. 现在真正还缺什么？**
产品结构与 Operating Main Composition 已接受；剩余是 Dark、1024、密度、展开态、真实数据投影与工程适配验证，不缺一套新的 Desk IA 或 Main 重设计。

**H. 下一步应该直接 Figma 增量修改、补有限 Composition，还是重新设计？**
复用 `69:3` 做适配与工程准备；不重新设计 Main。

**I. 是否还需要 Trae？**
不需要重新画 CEO Desk。只有 CEO 明确 Reopen Product/UI Decision 时，才允许重新进入 Design Candidate。

## 11. Evidence limits and boundary

本报告是历史与当前权威对账，不是当前运行页面的截图审计；未把旧截图、Prototype 或 Figma Frame 当作新一轮视觉验收证据。Figma、HTML、Frontend、Runtime、Schema、DB、Prototype 均未修改；Pointer / CURRENT_STATE 不更新，因为本轮没有改变 Product/UI Authority，只新增本 Review 文档。

**CEO DESK CURRENT DESIGN RECONCILED — STOP FOR CEO / CHATGPT REVIEW**
