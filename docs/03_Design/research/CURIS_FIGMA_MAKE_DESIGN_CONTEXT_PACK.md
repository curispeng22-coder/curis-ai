# CURIS FIGMA MAKE DESIGN CONTEXT PACK

Status: Review
Authority Class: RESEARCH
Disposition: DESIGN-AI CONTEXT PACK / NOT NEW AUTHORITY
Owner: Product / Design
Updated: 2026-08-23
Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

> This pack compresses current Curis product and visual context for Figma Make. It is not a Product Blueprint, visual authority, technical architecture document, or implementation authorization.

## 0. How to use this pack

### MUST PRESERVE

Preserve the product objects, navigation meaning, Workspace responsibilities, Employee identity, three Employee entries, benchmark information architecture, and the visual candidate rules below.

### MAY EXPLORE

Explore typography details, surface composition, spacing, content width, restrained Deep Green use, bounded professional accent, light-mode visual direction, responsive reflow, and motion direction—only within the preserved structure.

### MUST NOT INVENT

Do not invent product objects, navigation items, new panes, new Employee types, new Work/Result/Evidence/Decision semantics, new Assistant surfaces, new workflow/console views, new domain skins, or claims that an unverified capability is connected or complete.

### Reference status

Current Figma screens are **STRUCTURAL UX REFERENCE ONLY / VISUAL NOT ACCEPTED**. Consume only their information structure, content relationships, and interaction relationships. Do not imitate their typography, density, color ratio, card treatment, or whitespace ratio.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §01; `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` §1–2.

## A. What Curis is

Curis is a Desktop AI Company Operating Product. It brings mature AI work capabilities into one company so an ordinary user can express intent, know who is responsible, see work and results in a professional Workspace, and make decisions at important moments.

Curis is not only a chat product, task-flow agent, developer console, dashboard SaaS, low-code builder, or file manager. Its long-lived objects include Company, Business, Workspace, Team, Employee, Work, Result, Evidence, Decision, Conversation, Knowledge, Capability, Calendar and Meeting.

Source: `docs/01_Product/Curis_Product_Blueprint.html` §02; `docs/01_Product/Curis_Product_Master_Map.md` opening product statement and §Professional Workspace.

## B. Who the user is

The human user is the CEO / company operator. Typical company contexts include creators, independent developers, researchers, consultants, small businesses and one-person companies. The user should express intent, confirm boundaries, review proposals, authorize capabilities and make necessary decisions—not design professional information architecture or manage technical workflow machinery.

Source: `docs/01_Product/Curis_Product_Blueprint.html` §02; `docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_STRATEGY_AUTHORITY_RECONCILIATION_REVIEW.md` §F.

## C. Core product promise

“I say what I want to do, know who is responsible, see the work and result in a professional Workspace, and decide when it matters.”

The interface should make responsibility, current work, result, evidence and next decision understandable without exposing internal system machinery.

Source: `docs/01_Product/Curis_Product_Blueprint.html` §02; `docs/01_Product/Curis_Product_UI_Blueprint.html` §13.

## D. Primary Navigation

Use this fixed seven-area order:

1. CEO 工作台
2. 业务空间
3. 组织中心
4. 人才与能力
5. 经营洞察
6. 资料库
7. 会议

Navigation answers “我在哪里”. Recent Work may sit below the primary areas. CEO avatar / settings sit at the lower-left. Search, notifications / pending items and CEO Assistant are global capabilities; they do not become additional primary navigation items.

Do not add “首页”, “AI Team”, “Workspace Builder”, “Workflow”, “Automation Console” or a second chat entry to primary navigation.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §03, §04, §17; `docs/01_Product/Curis_Product_Master_Map.md` §Product IA.

## E. Workspace / Professional Workspace

Workspace is a complete professional operating environment, not a page. It has its own goal, positioning, rules, team operating, responsibilities, Employee Workstations, current work, results, analytics, risk and history. A Workspace can contain one or more Professional Surfaces.

Professional Workspace is a maintained, domain-aware working environment. Curis favors a small number of deep, researched and verified professional environments. A near or unknown business may begin honestly from a Generic Workspace; the visual design must not imply that every domain is already verified.

Workspace keeps a shared shell and shared Employee Work Area, while its Domain Navigation and Professional Surfaces may differ. Domain examples such as XHS, RD and Commerce are validation cases, not fixed Curis product categories.

Source: `docs/01_Product/Curis_Product_Master_Map.md` §Professional Workspace / Multi-Surface and §Professional Workspace Strategy; `docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_STRATEGY_AUTHORITY_RECONCILIATION_REVIEW.md` §A, §C, §R.

## F. Navigation / Context / Main / Utility

These are responsibilities, not necessarily four visible columns:

| Area | Responsibility | Preserve |
|---|---|---|
| Navigation | Company-level “where am I” | Fixed seven-area navigation |
| Context | Workspace identity, Domain Navigation, current Surface context and bounded supporting context | Adaptive; may be absent or collapsed |
| Main | Current Professional Surface and relevant Shared Work Area | Main must stand on its own |
| Utility | On-demand detail, editor, preview, evidence or tool for the current object | Default closed; never a permanent inspector |

Context is not an Employee directory. Utility is not a permanent result rail. Do not create a second global Assistant column.

Source: `docs/01_Product/Curis_Product_Master_Map.md` §Professional Workspace / Multi-Surface; `docs/01_Product/Curis_Product_UI_Blueprint.html` §04 and §17.

## G. Four-Pane is a responsibility model

“Four-Pane” means Navigation / Context / Main / Utility responsibilities. It does **not** require four physical columns, four permanent panes, or a fixed geometry. Context and Utility are adaptive surfaces. The layout must follow the current task and preserve Main priority.

Source: `docs/01_Product/Curis_Product_Master_Map.md` §Professional Workspace / Multi-Surface; `docs/01_Product/Curis_Product_UI_Blueprint.html` §17.

## H. Employee identity

Employee is a core product object and a responsibility-bearing person-like company member—not an online contact, monitoring tile or anonymous AI badge.

The shared identity group may show:

- Avatar
- Name
- Role / responsibility scope
- Current work summary
- User-facing work status: 空闲 / 工作中·简短描述 / 阻塞·原因, only when supported by real product truth
- Conversation affordance

Employment identity, work status, Work/Result status and Decision status must remain distinct. “已完成 / 待审核 / 已验收” belong to Work, Result or responsibility context, not Employee identity status.

Employee Row is a normal list row, not a large Card. Clicking avatar or name opens Employee detail in Utility; there is no separate “详情” button.

Source: `docs/01_Product/Curis_Product_Blueprint.html` §Employee Directory 与 Profile; `docs/03_Design/CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` §2.1–2.2.

## I. Employee three-entry model

The same Employee identity has three distinct user goals:

| Entry | Meaning | Visual priority |
|---|---|---|
| 直接对话 / Direct Conversation | Communication | Conversation and Composer |
| 当前工作 / Current Work | Work collaboration | Goal, current activity, judgment, result and handoff |
| 员工资料 / Employee Profile | Employee identity | Role, responsibility, capability, work history and identity context |

These are not three separate Employee products or three skins. Keep identity continuous while changing the active task and L1 focus. Assignment-scoped conversations retain their current Role / Scope context; they must not silently merge unrelated responsibility histories.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §08–§09 and §Employee Profile; `docs/01_Product/Curis_Product_Master_Map.md` §Employee / scoped Conversation; `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §8.

## J. CEO Assistant

CEO Assistant is a global company capability and a conversational entry point for the CEO’s intent. It is not a primary-navigation item, not a fifth pane, not a permanent right rail, and not a replacement for Employee Conversation or Workspace Thread.

It may help the CEO understand a situation, discover capability, form a proposal, return to the relevant company / business / Workspace context, and surface a decision. Keep it human-readable and context-aware; do not expose internal routing, workflow graphs or runtime consoles.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §03, §12, §17; `docs/01_Product/Curis_Product_Blueprint.html` §First open / Assistant.

## K. Research benchmark — exact structure to preserve

Research is a benchmark screen for visual-system comparison, not a new product truth. Use the current Operating Intelligence / Research pattern:

1. **Current scope and period** — what company, business, Workspace or Employee context is being examined.
2. **Analyst Brief / research question** — the primary reading and judgment focus in Main.
3. **Signals and findings** — relevant facts, interpretation, unknowns and recommendation; keep source / freshness / unknown visible when necessary.
4. **Report or research output** — readable primary content in Main; do not turn every finding into a separate colored Card.
5. **Follow-up Conversation** — “问分析师” continues in the existing Conversation Surface and stays connected to the current scope.
6. **Evidence / source / comparison** — on demand in Utility or Focus View, without displacing the primary reading surface.

The screen must feel like research and judgment, not a KPI dashboard, analytics wall, file manager or generic chat page. Keep the primary reading column bounded; secondary evidence may be disclosed progressively.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §09 Operating Intelligence, §16; `docs/01_Product/Curis_Product_Blueprint.html` §经营洞察; `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` §1–2.

## L. Employee Conversation benchmark — exact structure to preserve

1. Workspace / responsibility context stays available but does not dominate.
2. Employee identity is visible: avatar, name, role, current responsibility and user-facing status.
3. The Main surface contains the Employee Conversation-first Workstation, centered within a readable width.
4. Conversation is a natural message stream, not a bubble wall, monitoring dashboard or Card wall.
5. Work / Result / Handoff / Evidence appear as lightweight inline references; full detail opens in Utility or Focus View.
6. Composer sits with the conversation and uses the shared semantic slots below.
7. Employee Profile is reached by avatar/name; Current Work is a work-focused entry; Direct Conversation remains communication-focused.
8. Expand / collapse changes presentation only; it does not create a new product object or change responsibility.

Do not place an Employee list in Context Sidebar, add Employee tabs, or make Employee status the main page narrative.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §08, §17, §Employee Work Area; `docs/03_Design/CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` §2.1–2.3; `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` §2–4.

## M. Shared Composer structure

Preserve semantic slots, not one fixed geometry:

`Input` + `Add (+)` + `访问权限` + `工作模式` + `已选功能/资源` + `执行选择（Model / Agent）` + optional `Voice` + `Send`.

Desktop may use input above with grouped lower controls. Responsive layouts may reflow, but the semantic slots must remain understandable. Provider-native capabilities determine which permissions, modes, models, agents, voice and resources are actually available; Figma Make must not invent unsupported options or a second technical capability system.

Source: `docs/01_Product/Curis_Product_UI_Blueprint.html` §08, §10, §16–§17; `docs/03_Design/CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` §3.

## N. Shared Visual System Candidate

The candidate visual philosophy is:

**Calm Surface / Strong Focus / Rich Work**

- Calm Surface: quiet neutral surfaces and long-session readability.
- Strong Focus: one clear current priority per viewport.
- Rich Work: preserve real Work, Result, Evidence, Decision and responsibility content without turning the screen into a dashboard.

Candidate rules:

- Use typography, spacing, alignment and content width before borders, shadows or Cards.
- Use semantic color roles, not raw Hex scattered across screens.
- Keep raised surfaces and strong accents scarce.
- Use progressive disclosure for supporting work and advanced controls.
- Use Chinese-first typography and readable mixed Chinese/English/number treatment.
- Comfortable density is the default; Compact is a bounded alternative, not a compressed monitor wall.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §1–§5, §11–§12; `docs/07_Decisions/ADR-0042-calm-executive-visual-language.md`.

## O. Visual focus L1–L4

These are **visual attention levels**, not the Product UI Blueprint’s visibility levels:

| Visual level | Meaning |
|---|---|
| L1 | Current Decision, Work, Insight, Conversation, Critical Change or Business Object |
| L2 | Active Employee, Surface, Cycle or Work state that explains L1 |
| L3 | Supporting Result, Handoff, Evidence, Plan, related objects and metrics |
| L4 | Reference time, source, history, file and metadata |

Do not expose “L1/L2/L3/L4” labels in the UI. Use position, type, contrast, spacing, surface and disclosure to express them.

Product visibility remains governed by the UI Blueprint: L1 always-visible core, L2 contextual, L3 on demand, L4 advanced/internal. Do not make every visual level permanently visible.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §2; `docs/01_Product/Curis_Product_UI_Blueprint.html` §02 and §17.

## P. Attention Budget

Per desktop viewport, candidate default:

- 1 Primary Focus
- no more than 2 obvious accent areas
- no more than 1 Primary CTA
- raised surface is scarce
- all other content actively recedes

The design should still communicate hierarchy if all accent colors are removed.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §2; `docs/03_Design/research/CURIS_VISUAL_DESIGN_SYSTEM_RESEARCH.md` §5.

## Q. Card Policy

Use this order first:

`Typography → Spacing → Alignment → Divider / Subtle Surface → Card`

Card is allowed for an independent actionable object, a selected/focus object, a grouped action surface or an overlay. Card is not the default wrapper for each message, Employee, metric, metadata line, section or status. Do not build Card Wall or Dashboard Wall.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §7; `docs/03_Design/research/CURIS_VISUAL_DESIGN_SYSTEM_RESEARCH.md` §12; `docs/03_Design/Curis_Design_System.md` §4.

## R. Color, Deep Green and Domain Accent

Use semantic roles such as brand, focus, action, surface, text, border, attention, success, error and Employee state. Do not distribute raw Hex values as product meaning.

Deep Green is a candidate Curis brand/focus anchor, not a full-page skin. It may support brand identity, a primary action or a small focus treatment. It must not color every active state, link, navigation item or large background.

Professional Domain Accent may appear in charts, content types, domain objects, specialized visualizations and bounded domain status. It must not recolor the shell, primary navigation, Composer, common text, Employee identity or Curis focus semantics. XHS, RD and Commerce must not each become a full visual theme.

Status must never depend on color alone; pair it with text, icon, shape or position.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §5–§6; `docs/03_Design/research/CURIS_VISUAL_DESIGN_SYSTEM_RESEARCH.md` §9–§11; `docs/07_Decisions/ADR-0042-calm-executive-visual-language.md`.

## S. Chinese-first product language

The product is Chinese-first. Use plain Chinese as the primary user-facing language. English may remain where it is a necessary product term or provider-native label, but do not let English-only typography determine hierarchy or density.

Prefer human terms such as：CEO 工作台、业务空间、工作空间、员工、当前工作、结果、证据、需要我决定什么。 Do not surface internal engineering vocabulary as user-facing design content.

Source: `docs/03_Design/Curis_Design_System.md` §4.6; `docs/01_Product/Curis_Product_UI_Blueprint.html` §01, §13 and §17.

## T. Desktop sizes

Use these comparison sizes:

- 1440×900: full desktop composition; Main remains primary.
- 1280×800: Utility may narrow or close; Context may collapse; Main remains readable.
- 1024×800: adaptive surfaces may collapse or become overlays; preserve the current focus and task.

Do not use a fixed four-column layout as the acceptance target. Test responsive reflow, content width and priority, not merely shrinkage.

Source: `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` §2, §5; `docs/01_Product/Curis_Product_UI_Blueprint.html` §17.

## U. Visual anti-patterns

Reject or strongly challenge:

Card Wall · Dashboard Wall · Pill Everywhere · Gray-on-Gray Everywhere · Color Everywhere · No Visual Focus · Everything Bold · Everything Equal · Huge Empty Space · Over-compressed Density · Agent Monitoring Wall · File Manager Feel · Chat Bubble Wall · Engineering Console · Gradient AI SaaS · Excessive Radius · Excessive Shadow.

Source: `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` §13; `docs/03_Design/research/CURIS_VISUAL_DESIGN_SYSTEM_RESEARCH.md` §18.

## V. What Figma Make must not change

Do not change:

- Curis’s product identity or ordinary-user / CEO audience.
- The seven primary navigation areas or their order.
- Workspace as a complete professional operating environment.
- Professional Workspace as shared shell + domain navigation + one or more professional surfaces + shared Employee Work Area.
- Navigation / Context / Main / Utility responsibilities.
- Four-Pane as a responsibility model rather than fixed geometry.
- Employee identity and the three entries: Direct Conversation, Current Work, Employee Profile.
- CEO Assistant as a global capability, not a fifth pane or primary navigation item.
- Research and Employee Conversation benchmark information architecture.
- Shared Composer semantic slots.
- Result ≠ Evidence ≠ Decision.
- Calm Surface / Strong Focus / Rich Work, L1–L4, Attention Budget and Card Policy.
- Chinese-first language and honest capability/status expression.

Do not add implementation surfaces, technical control panels, new navigation, new domain skin or new product truth.

Source: `docs/01_Product/Curis_Product_Blueprint.html`; `docs/01_Product/Curis_Product_Master_Map.md`; `docs/01_Product/Curis_Product_UI_Blueprint.html`; `docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_STRATEGY_AUTHORITY_RECONCILIATION_REVIEW.md`; `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md`.

## W. Figma Make handoff boundary

Create three visual directions using the same information architecture and content:

- A — Quiet / Neutral baseline
- B — Curis Strong Focus
- C — Curis Focus + restrained Professional Accent

Benchmark screens: Research and Employee Conversation. Show 1440×900, 1280×800 and 1024×800 responsive states. Dark mode is directional only. Stop after visual comparison and return screenshots, scores, retained rules, rejected rules and unresolved questions for CEO Review.

Source: `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` §1–§7.

## Source Map

### Current Product Authority

1. `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` — Truth Router and current authority chain.
2. `docs/01_Product/Curis_Product_Blueprint.html` — sole Product Authority: product identity, audience, navigation, Employee, Assistant and Workspace semantics.
3. `docs/01_Product/Curis_Product_Master_Map.md` — canonical product structure and Professional Workspace strategy.
4. `docs/01_Product/Curis_Product_UI_Blueprint.html` — sole Current UI Blueprint: shell, navigation, spatial responsibilities, progressive disclosure, Employee Workstation and Composer boundary.
5. `docs/reviews/CURIS_PROFESSIONAL_WORKSPACE_STRATEGY_AUTHORITY_RECONCILIATION_REVIEW.md` — CEO Accepted Professional Workspace Strategy; Review/Frozen, not a second Blueprint.

### Shared and visual inputs

6. `docs/03_Design/CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` — Employee row, identity, Conversation-first workstation and shared Composer slots.
7. `docs/03_Design/Curis_Design_System.md` — Frozen Calm Executive Workspace and Chinese-first visual baseline.
8. `docs/07_Decisions/ADR-0042-calm-executive-visual-language.md` — Frozen Calm Executive visual language.
9. `docs/03_Design/research/CURIS_VISUAL_SYSTEM_CANDIDATE.md` — Review candidate visual system.
10. `docs/03_Design/research/CURIS_VISUAL_EXPLORATION_BRIEF.md` — Review brief for the next visual exploration.

### Explicitly not an input for visual imitation

Current Figma Structural Candidate screens and any existing prototype screenshots are structural references only. Their visual treatment is not accepted and must not be copied.
