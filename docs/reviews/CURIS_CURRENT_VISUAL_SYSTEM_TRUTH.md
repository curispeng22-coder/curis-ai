# CURIS CURRENT VISUAL SYSTEM TRUTH

Status: Review
Authority Class: REVIEW
Disposition: CEO REVIEW REQUIRED
Scope: Existing visual decisions and Trae qualification input only

> 本文是视觉真源审计，不是新的 Design System、Product Blueprint 或实现授权。未修改任何 Product Truth、Frozen Authority、Shell Contract、Frontend、Prototype、Figma、tokens、Runtime、Schema 或 DB。

## 1. Executive Summary

现有视觉系统足以支持 Trae 进行一次受约束的 Master Shell 资格测试，前提是 Trae 继承当前 Frozen token 与 Shell 结构，并把未决项限制在视觉表现层。当前最重要的纠正是：实际当前 token 真源使用 `#32f08c` 深绿；`#806BE5` 在当前 Product/UI/Frontend 真源中未发现，不得继续作为当前品牌色。

结论：`VISUAL SYSTEM SUFFICIENT FOR TRAE`。

这不是对昨日 Figma 构图的通过。页面构图失败 ≠ 视觉系统自动失败：昨日探索中可复用的结构关系与视觉语言必须拆开判断，不能用一张失败构图推翻已有 token、层级、表面和 Shell 规则。

本轮没有截图或 live visual QA；结论来自 Current Authority、Frozen Design/ Shell 文档、研究材料和前端 token/source reconciliation，不宣称可访问性、响应式或最终美学已经通过。

## 2. Product Composition vs Visual Language

### 2.1 Product Composition（不由本审计重新定义）

以下来自 Current/Frozen Shell，可作为结构约束：

- 七区一级导航；搜索、最近工作、通知/待处理、CEO Assistant 是 Global Capability，不是第八区，也不等于 Global Topbar。
- `Navigation | Context | Main | Utility` 是职责关系；Main 必须独立成立，Context/Utility 按需折叠。
- 每个 Pane 使用 Pane-local Header；取消横跨全 App 的 Global Topbar。
- `Main = selected Professional Surface + Shared Work Area`；Employee Workstation 属于 Main.WorkArea，不吞掉整个 Main。
- Employee 是责任主体与工作入口，不是 Employee Wall；Conversation 是阅读流，不是卡片墙；Composer 使用共享语义槽位。

这些是产品/空间结构，不是 Trae 可随意改动的视觉方向。

### 2.2 Visual Language（可独立保留或探索）

昨日 Figma/研究中仍有价值的视觉语言候选：

- Calm Surface / Strong Focus / Rich Work：安静表面、单一主焦点、保留真实工作内容。
- 中性表面、受控深绿、中文优先排版、清晰的 PRIMARY/SECONDARY/TERTIARY/QUIET 层级。
- 稀缺 Card、低对比 Divider、真实 elevation 才使用 Shadow、Conversation/Result/Evidence 以阅读和引用关系表达。

这些规则不能被一张构图不理想的探索稿自动废止；它们仍分别标注为 ACCEPTED 或 CANDIDATE，见矩阵。

## 3. Decision Timeline

| 时间/阶段 | 旧规则或研究 | 后续判断 | 当前归类 |
|---|---|---|---|
| 2026-08-04 | `Curis_UI_Frozen_Spec_2026-08-04.md` 固化 `--ui-*` token、桌面优先、主题与基础可访问性 | 后续 Shell 决策只替代其过时构图/导航，不否定 token 基础 | LOCKED（token） / SUPERSEDED（旧构图） |
| 2026-08-15 | Shell Delta-X7/X8：撤销横跨 Global Topbar，Pane-local Header；Conversation-first Workstation | Frozen Shell 继续约束结构与共享表达 | LOCKED |
| 2026-08-17 | Shared Main / Employee Work Area / Composer / Conversation Content Block | Main、员工、对话、Composer 的职责与语义固定，具体视觉布局仍可调 | ACCEPTED |
| 2026-08-23 | `CURIS_SHARED_VISUAL_DESIGN_SYSTEM_RESEARCH.md`、`CURIS_VISUAL_SYSTEM_CANDIDATE.md` | Calm Surface / Strong Focus / Rich Work、卡片稀缺、注意力预算进入候选 | CANDIDATE |
| 2026-08-23 | `CURIS_VISUAL_EXPLORATION_BRIEF.md` 的 A/B/C 方向 | 结构固定、视觉开放；A/B/C 是资格测试方向，不是产品新架构 | CANDIDATE |
| 2026-08-26 | `CURIS_MASTER_SHELL_VISUAL_EXECUTION_CONTRACT.md` | Trae 只做中性 Master Shell 资格测试，不做业务页面 | ACCEPTED（资格范围） |
| 当前审计 | Master Shell 中条件提及 `#806BE5`，但当前 sources/frontend 无该值 | 以当前 Frozen token 真源 `#32f08c` 为准；Shell 文本需另行做窄幅契约纠正 | SUPERSEDED（#806BE5） |

## 4. Visual Truth Matrix

| Element | Current Rule / Value | Status | Source | Trae Freedom |
|---|---|---|---|---|
| Primary Accent | 当前深色 `--ui-accent: #32f08c`；主行动 `--ui-action-primary-bg: #32f08c`，hover `#0fdc78` | LOCKED | `frontend/app/globals.css`; `docs/03_Design/Curis_Design_System.md`; `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` | 可调使用频率与位置；不可换成新品牌色 |
| `#806BE5` | 曾出现在历史 Figma/视觉探索候选与 Master Shell 条件句；当前 Product/UI/Frontend token 未找到 | SUPERSEDED | Historical Figma/visual exploration; current token scan; `docs/reviews/CURIS_MASTER_SHELL_VISUAL_EXECUTION_CONTRACT.md` | 不得使用；需由合同维护轮修正措辞 |
| Background | Dark `#1a1c1f`；Light/System `#f5f5f7` | LOCKED | `frontend/app/globals.css`; Frozen Spec | 可探索分区比例与留白，不得另造背景 palette |
| Surface | Dark `#222529` / `#2b2f34`；Light `#fff` / `#f7f8fa` | LOCKED | `frontend/app/globals.css`; `frontend/lib/theme.js` | 可探索表面层级和局部聚合，不得高饱和铺面 |
| Primary Text | Dark `#f3f4f6`；Light `#1a1c1f` | LOCKED | `frontend/app/globals.css` | 可探索字重、行长、对比层级 |
| Secondary / Tertiary Text | Dark `#a7adb6` / `#a3aab4`；Light `#4b5563` / `#626b76` | LOCKED | `frontend/app/globals.css` | 仅调层级与出现时机，不改语义 |
| Divider | `--ui-line`：Dark `#343940`、Light `#e5e7eb`；低噪音边界 | LOCKED | `frontend/app/globals.css`; Frozen Shell | 可探索线宽、分组与显隐，不用重边框墙 |
| Radius | `--ui-r-xs 4px`、`--ui-r-sm 8px`、`--ui-r-md 12px`、`--ui-r-lg 16px`；pill 仅语义需要 | LOCKED | `frontend/app/globals.css`; `frontend/lib/theme.js` | 可组合已有档位；不可引入任意半径体系 |
| Card | Card 不是默认信息容器；禁止 Card Wall/消息卡墙/KPI 卡墙 | ACCEPTED | Frozen Shell; Current UI Blueprint | 可在独立对象、Focus、Action Group、Overlay 中选择已有 surface/card 语义 |
| Shadow / Elevation | `--ui-shadow` / `-2` / `-3`；只表达真实 raised/overlay | ACCEPTED | `frontend/app/globals.css`; Frozen Spec; visual research | 可选择是否需要 elevation；不得泛滥阴影或发光 |
| Typography | 中文优先，系统/Inter fallback；7 档字号 token（12–28px）已存在 | LOCKED | `frontend/app/globals.css`; `frontend/lib/theme.js` | 可调字体组合、层级与排版节奏；不得写死新字号档 |
| Type Scale Detail | Research 提出的 28–36 focus、22–24 page 等仍待 benchmark | CANDIDATE | `CURIS_VISUAL_SYSTEM_CANDIDATE.md` §3 | 可在现有 token 约束内提出方向；不得当作已冻结数值 |
| Density | 信息丰富、渐进披露、不是 Landing Page/后台墙；默认 Comfortable | ACCEPTED | Frozen Shell; Current UI Blueprint; visual research | 可调 grid、间距、密度和 responsive reflow |
| Selected State | 选中态必须可由位置、层级、对比、焦点和必要 accent 联合识别，不只靠颜色 | ACCEPTED | Frozen Shell; visual research §4 | 可探索 marker、背景、underline、icon/label weight |
| Navigation Active | 七区顺序与稳定公司导航不变；Active 不得变成高饱和整栏皮肤 | LOCKED | Frozen Shell; Current UI Blueprint | 可探索 active marker、icon weight、padding、折叠呈现 |
| Result Focus | Result 是产出；在 Main/Conversation 中可作为当前 L1 或明确引用 | ACCEPTED | Current UI Blueprint; Frozen Shell; visual research §10 | 可探索 result 的视觉权重与 focus surface |
| Decision Focus | Decision 是选择/责任/行动；仅在真实需要时突出 | ACCEPTED | CEO Desk contract; Frozen Shell; visual research | 可探索 Decision 的 banner/inline/focus 表达；不造全局 Conflict 状态 |
| Employee Presence | Avatar/Name/Role/Scope/Status/Current Work/Conversation affordance；不做在线墙 | ACCEPTED | Frozen Shell §3.1/§3.8; Company OS Shared Authority | 可探索行、presence marker、展开反馈；不能让 Employee 成为整页主视觉 |
| Spatial Field | Canvas → Default → Focus/Raised → Overlay；“中性空间场”方向保留 | CANDIDATE | `CURIS_VISUAL_SYSTEM_CANDIDATE.md` §7; Figma context pack | 可探索分区、开放画布、局部聚合；不得以此重写 Pane 责任 |
| State Colors | Success `#3fcf86` / `#1f8157`、Warning `#d89a3a` / `#9c671d`、Danger `#e57373` / `#c43f3f`；颜色不能单独承载状态 | LOCKED | `frontend/app/globals.css`; Frozen Spec | 可调图标/文字/形状组合；不可用颜色替代文案 |
| State Language | UI 侧只消费空闲 / 工作中·desc / 阻塞·cause；Runtime 状态不自动决定折叠 | LOCKED | Frozen Shell §3.1; Company OS Shared Authority | 可探索排版与提示方式；不增加 completed/waiting UI 状态 |
| Theme | Dark / Light / System 均有 token mapping；`theme.js` 通过 `data-theme` 持久化切换 | LOCKED | `frontend/app/globals.css`; `frontend/lib/theme.js`; `frontend/components/terra/TerraShell.js` | 可探索三种主题下构图与对比；不得另造主题体系 |
| Theme Composition | 完整 Light/Dark 的最终页面构图与跨视口节奏尚未被最终 benchmark | OPEN | Visual research §2.1/§12; exploration brief | 可在 token 与可访问性约束内探索；不能把开放项解释为缺少系统 |
| Motion | 短、可打断、可减少；服务于 pane、focus、employee response、decision arrival | ACCEPTED | visual research §12; Frozen CSS reduced-motion rules | 可探索微交互与节奏；不可用持续动效制造注意力 |

## 5. Current Frontend Source Audit

| Source | Current assessment | Notes |
|---|---|---|
| `frontend/app/globals.css` | LOCKED | `--ui-*` 定义背景、表面、文字、accent、状态、半径、阴影、字号、间距、主题与 reduced-motion。 |
| `frontend/lib/theme.js` | LOCKED | JS 内联样式消费 `var(--ui-*)`，不应再写死 hex/px；`data-theme` 切换由 Shell 持久化。 |
| `frontend/components/terra/TerraShell.js` | ACCEPTED | 主题与 Shell 入口消费 current tokens；实现完成度不等于本轮视觉接受。 |
| Terra shared components | ACCEPTED | 可复用组件是实现输入；需继续以 Shell/Current UI Blueprint 的语义而非组件文件名判断。 |
| `TerraNavData` / 旧导航投影 | SUPERSEDED | 可能保留历史实现依赖；不能反向覆盖七区、Pane-local Header、无 Global Topbar 的 Current 结构。 |
| `docs/03_Design/Curis_Design_System.md` | LOCKED + SUPERSEDED | 文档头为 Frozen，但其旧 Top Bar/导航章节被后续 Shell Delta 替代；本审计只继承 token、桌面优先和语义规范。 |
| `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` | LOCKED + SUPERSEDED | 颜色、字号、主题、触达/焦点规则仍可作基础；旧页面/Global Topbar 不再是 Current 结构。 |
| old Prototype / Flow Pack / early Figma | SUPERSEDED | 不可作为 Current visual authority；仅用于理解历史决策和失败边界。 |

## 6. What Trae Must Inherit vs May Explore

### Must inherit（LOCKED / ACCEPTED）

- 七区导航、无 Global Topbar、Pane-local Header、四 Pane 职责和 Main 独立成立。
- Main = selected Professional Surface + Shared Work Area；Employee Workstation 不吞掉 Main。
- Conversation reading flow、Composer 语义槽位、Employee Presence 与三态 UI 投影。
- 当前 `--ui-*` token、Dark/Light/System 主题、状态颜色与 reduced-motion/焦点规则。
- Result / Evidence / Decision 的语义区分；Card Wall、Dashboard Wall、Employee Wall、发光 AI SaaS 禁止。
- 当前主 accent 是 `#32f08c`；不得使用 `#806BE5`。

### Direction to preserve（CANDIDATE）

- Calm Surface / Strong Focus / Rich Work。
- 一个默认 L1、稀缺 raised surface、低噪音 Divider、中文阅读节奏。
- Domain accent 仅用于领域对象/图表/状态，不改壳层、导航、Composer、通用文字。
- 卡片稀缺、内容宽度按场景变化、长内容可读、信息通过渐进披露组织。

### Trae may explore（OPEN / CANDIDATE范围内）

- 具体字体组合与字号映射、grid/spacing、pane 比例、collapse 处理。
- Selected marker、icon weight、divider/surface/depth、已有 radius/shadow 档位的组合。
- Light/Dark/System 下的具体构图、信息密度、motion/micro-interaction。
- A/B/C 三个视觉方向的空间节奏、层级、表面处理与导航呈现；结构和内容保持同一中性 fixture。

## 7. Current / Historical / Vision Boundary

| Layer | What it means here | Examples | Trae treatment |
|---|---|---|---|
| LOCKED | 当前可直接继承的视觉与结构事实 | `--ui-*` tokens、Dark/Light/System、七区 Shell、Pane-local Header、Main/Work Area 责任 | 必须继承 |
| ACCEPTED | 已被 Current/Frozen 语义接受，但具体像素仍可表达 | Result/Decision/Employee Presence 层级、Conversation reading flow、Card 非默认容器 | 继承语义，探索表现 |
| CANDIDATE | 研究或资格测试方向，尚未成为 Frozen 数值/页面 | Calm Surface / Strong Focus / Rich Work、Spatial Field、A/B/C 方向、候选 type scale | 可在边界内探索，不得当作最终事实 |
| SUPERSEDED | 旧构图、旧导航、旧视觉候选，仅保留 provenance | Global Topbar、旧五/六区、`#806BE5` 候选、旧 Prototype/Flow Pack | 不得作为当前身份或 token |
| OPEN | 尚未决定的具体视觉细节 | 最终字体 benchmark、完整主题构图、motion choreography | 可提案；不构成产品缺口 |

## 8. Open Questions and Blocker Test

仍开放：最终字体、候选 type scale、完整 Light/Dark 构图、精确 pane 比例、Spatial Field 的视觉实现、selected marker 细节、motion choreography。它们不构成阻塞，因为当前已有明确 token、语义层级、结构边界和 `#32f08c` accent；Trae 不需要重新发明 Curis 的视觉身份。

唯一需要单独维护的纠正是 Master Shell 合同中 `#806BE5` 的条件句。它不阻塞本轮 qualification，但属于 `CONTRACT CORRECTION REQUIRED`，应在后续窄范围文档维护中改为“以当前 Frozen token 真源为准”，而不是修改设计或前端。

## 9. Qualification Evidence Boundary

Trae 资格测试应只输出相同中性 fixture 的 A/B/C 方向与 Default / Context Expanded / Deep Work 三状态。Fixture 必须标注 `DESIGN FIXTURE ONLY — NOT PRODUCT CONTRACT`。评审只判断：是否继承结构、层级、token 与禁止项；不把构图方案选中误写为最终 Product/UI Authority。

本审计未进行 Figma 写入、页面设计、截图验证或实现变更。

— VISUAL SYSTEM SUFFICIENT FOR TRAE — STOP FOR CEO VISUAL TRUTH REVIEW
