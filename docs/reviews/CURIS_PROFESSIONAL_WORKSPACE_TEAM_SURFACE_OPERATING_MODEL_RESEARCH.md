# CURIS PROFESSIONAL WORKSPACE — TEAM × SURFACE OPERATING MODEL RESEARCH

**Authority Class:** RESEARCH

**Status:** Review

**Disposition:** CEO REVIEW REQUIRED

**Date:** 2026-08-21

**Scope:** Team × Professional Surface operating semantics only

**Authority Effect:** NONE — this document does not update Product Blueprint, Master Map, UI Blueprint, Shared Authority, Workspace Engineering Methodology, Package Proposal, Runtime, Schema, Database, Frontend, or Prototype.

> Research conclusion: for a long-term Workspace, there is one canonical Workspace-scoped Operating Team responsibility boundary. Professional Surfaces are domain work projections inside that Workspace. They do not own Employees, Teams, Responsibilities, Work, Results, Evidence, or Cycles. Existing Assignment, Organization Routing, Work, Handoff, Result/Evidence, Leader Review, and Cycle primitives remain the execution truth.

---

## A. Executive Summary

### A.1 Recommended operating model

```text
Company
└─ Department
   └─ Business
      └─ Workspace
         ├─ one canonical Operating Team responsibility boundary
         │  ├─ Workspace Leader / Operating Owner
         │  ├─ Responsibility Assignments
         │  └─ Employees resolved through Organization Routing
         └─ multiple Professional Surfaces
            ├─ declare responsibility requirements: WHAT
            └─ project relevant Work / Result / Evidence / presence
```

The shortest valid model is:

1. **One long-term Workspace = one accountable Operating Team boundary.** This does not mean one fixed headcount, one exclusive Organization team, or one Employee per responsibility.
2. **Surface does not own Team.** Surface declares domain responsibility requirements and shows scoped projections.
3. **Responsibility is the bridge.** A Surface says what responsibility is required; Organization Routing resolves the current Assignment, Holder, and verified Executor.
4. **Employees may cross Surfaces without identity duplication.** The same Employee can hold several Workspace-scoped Assignments and appear wherever those responsibilities are relevant.
5. **Work, Result, Evidence, and Cycle remain Workspace Runtime truth.** Surface affinity is derived presentation metadata or Package mapping, not a new lifecycle.
6. **Handoff transfers accountability, not navigation.** A Surface change alone never creates a Handoff; a Handoff may cause the same Work or its Result to become relevant on another Surface.
7. **One active Cycle may contain multiple Work items.** Current accepted Autonomous evidence proves one materialized Team Operating Work per Cycle, not general cross-Surface multi-Work execution; that broader proof remains partial.
8. **Closing or switching a Surface cannot stop execution.** There is no Surface Runtime.
9. **One shared Employee Workstation serves all Surfaces.** It opens with Assignment/Work/object context; it is not cloned per Surface.
10. **CEO Assistant stays global.** It may coordinate and surface exceptions, but it is not automatically a member, Leader, Holder, or professional executor of the Workspace team.

### A.2 Answers to the 25 CEO questions

| # | CEO question | Research answer |
|---:|---|---|
| 1 | 一个 Workspace 是否只对应一支 Operating Team？ | **是，限长期 Workspace。**它只有一个 canonical、可问责的 Workspace Operating Team 边界；这不冻结人数，也不排斥共享 Employee 或临时协作者。 |
| 2 | Surface 是否拥有 Team？ | **否。** Team 属于 Workspace 经营责任边界；Surface 只投影相关责任和工作。 |
| 3 | Surface 是否绑定 Employee？ | **否。** Surface 声明 WHAT；Employee 由 Workspace-scoped Assignment 与 Organization Routing 解析。 |
| 4 | Surface 与 Team 的桥梁是什么？ | **Responsibility。**具体链为 Surface requirement → Organization Routing → Assignment → Holder/Executor。 |
| 5 | 一个 Employee 能否跨多个 Surface？ | **可以。**保持一个 identity，通过多个 Assignment/Work context 出现在相关 Surface。 |
| 6 | 一个 Responsibility 能否跨多个 Surface？ | **可以。**Responsibility 独立于呈现，可被多个 Surface 消费。 |
| 7 | Leader 是否贯穿整个 Workspace？ | **是。**Leader 持续承担目标、策略、团队、结果、异常和 CEO 沟通责任，不按 Surface 分裂。 |
| 8 | Leader 是否需要逐 Work 分派？ | **不需要。**正常 WHO 由 Router 解析；Leader 只在异常、冲突、管理或策略判断时介入。 |
| 9 | Work 如何跨 Surface？ | 通过共享对象、Responsibility、Work/Result/Evidence refs 与 Package 投影规则；不是通过用户点击页面。 |
| 10 | Handoff 是否等于 Surface transition？ | **不等于。**Handoff 是经 ACK 的 Assignment accountability transfer；Surface 变化只是可能的呈现结果。 |
| 11 | 一个 Cycle 是否可以跨多个 Surface？ | **可以。**Cycle 是经营边界，不是屏幕边界。 |
| 12 | 一个 Cycle 是否允许多个 Work？ | **产品模型允许。**single-active Cycle 不等于 single Work；但通用跨 Surface 多 Work Autonomous E2E 仍缺 accepted evidence。 |
| 13 | 切换 Surface 是否影响执行？ | **不影响。**切换/关闭 Surface 不改变 Holder、Executor、Work、Provider 或 Cycle truth。 |
| 14 | 用户不在页面时 Employee 是否继续工作？ | **可以。**执行由 durable Work 和已验证执行身份控制，不由用户 presence 控制。 |
| 15 | Employee 在 Default Surface 应显示到什么程度？ | 仅在相关时轻量显示负责人、当前责任、协作/Handoff 与简要处理状态；不显示“Agent 在线墙”。 |
| 16 | Team Surface 应显示什么？ | Leader、成员、责任覆盖、当前/阻塞责任、真实 Handoff、重要 Work 与近期 Result；不是 Employee Monitoring Center。 |
| 17 | Employee Detail 是否保持同一 identity？ | **是。**展示当前 Workspace responsibility、Work、Result、Handoff、capability 和授权历史，不建 Surface profile。 |
| 18 | Workstation 是否共享？ | **是。**一个共享 Workstation，以 Surface-scoped current context 打开，不按 Surface 复制。 |
| 19 | Conversation 如何携带 Surface context？ | identity 由 Employee + Assignment/Work/Scope 决定；Surface 仅作为可选 source/return context，并携带相关 object/result refs。 |
| 20 | CEO Assistant 与 Workspace Team 什么关系？ | Assistant 是 Company-level Global Employee，默认不属于 Workspace Team；可协调、跟进、升级，但不替代 Leader 或专业责任。 |
| 21 | Package 是否需要 responsibility requirement？ | **需要最小声明，限可发起/接收专业工作的 Surface。**声明责任语义/类别，不声明 Employee ID。 |
| 22 | 是否需要 Surface Runtime？ | **不需要。**禁止新增 Surface Task/Agent/Cycle/Result/Session。 |
| 23 | 当前 Runtime 真正缺什么？ | 核心执行 primitive 已有；缺口是 Package 声明、UI 投影、XHS domain bridge，以及跨 Surface/多 Work accepted E2E evidence。 |
| 24 | Unknown Domain 如何一起生成 Surface + Responsibility + Team？ | Domain Research → Semantic Model → Professional Surface Model → Responsibility Model → Capability Map → Team Design → Package → Validation，并先读当前 Company Truth。 |
| 25 | CEO 需要决定什么？ | 决定是否接受五项 Candidate：一 Workspace/一 Team 边界、Responsibility bridge、Surface 只投影、Package 最小声明方向、后续验证 Gate；本轮不决定 Schema、UI 或实现。 |

---

## B. Current Authority Audit

### B.1 Authority and evidence classes

| Source | Class / disposition | What it can establish here |
|---|---|---|
| `Curis_Company_OS_Shared_Authority.md` | FROZEN | Long-term Workspace requires real Operating Team; Leader/Assignment/Router/context/Assistant invariants. |
| `CURRENT_STATE.md` | CURRENT implementation summary | Current Product → Implementation relationship and accepted gaps. |
| Workspace Engineering Methodology / Lifecycle | REVIEW · APPROVED CANDIDATE; Three-Layer Unknown Business contract CEO Accepted | Domain research, semantic/operating model, capability review, Package and validation order; methodology is not Runtime. Its older blanket “Package Runtime not implemented” wording is stale against later bounded P0/P0.5 evidence. |
| Workspace Engineering P0/P0.5 Reviews | REVIEW · ACCEPTED BOUNDED implementation evidence | Declarative Package install/navigation, fixed shell panes, generic object projection, real Company/Workspace integration; not generic multi-Professional-Surface delivery. |
| Professional Workspace Internal Research | RESEARCH · Review | Candidate Domain Navigation + multiple Professional Surfaces + Context/Main/Utility ownership; no Authority effect. |
| Team Operating Engine Research / Contract Candidate | RESEARCH / REVIEW | Selected Work-centered Responsibility Routing model; not independently Product Authority. |
| Responsibility Routing Runtime Review | REVIEW · implemented, CEO review required | Current implementation evidence for Work projection, Holder/Executor, Handoff, consult/review, restart. |
| Real Employee E2E Review | REVIEW · ACCEPTED | Real Workspace-scoped Employee execution and Result return through the existing bridge. |
| Autonomous Phase 1 / 2 / 3A / 3B Reviews | REVIEW · IMPLEMENTED / ACCEPTED | Durable Cycle, Work release, execution, evaluation, Leader Review, bounded successor authorization. |
| Primary Two-Cycle E2E Review | REVIEW · CEO REVIEW REQUIRED | Two-cycle RD evidence; it must not be described as accepted. |
| XHS Professional Workspace research and map | RESEARCH / EXPERT RECOMMENDATION | Candidate XHS Surfaces, objects, responsibility areas, and human-visible projections. |

### B.2 Accepted and current facts

- A long-term Workspace must be carried by a real Operating Team with Leader, members, and explicit responsibilities.
- Leader is a scoped responsibility role, not an Employee type; one Employee identity may hold multiple roles and scopes.
- Responsibility Requirement names WHAT and never directly names an Employee.
- Organization Routing resolves WHO; Capability determines HOW.
- Assignment is the responsibility carrier. Work, Conversation, and Result default to Assignment scope rather than a naked Employee identity.
- Holder and Current Executor are distinct. Executor never gains accountability by implication.
- Handoff changes Holder only after valid acceptance; consult/review can execute without transferring Holder.
- Existing Team Operating and Autonomous Operating reuse the same Work, Assignment, Employee, Result, Evidence, Decision, and Handoff foundations.
- CEO Assistant coordinates but does not replace professional responsibility.

### B.3 Not established as current truth

- No current Authority says a Professional Surface owns Employees, a Team, a Responsibility, or a Cycle.
- No accepted evidence proves a generic multi-Surface Package declaration or a cross-Surface multi-Work Autonomous E2E.
- XHS exact Surface taxonomy, responsibility vocabulary, headcount, Employee names, and operating flow remain candidate research.
- Primary Two-Cycle E2E remains CEO Review Required, not Accepted.

### B.4 Authority conflict check

No current Authority conflict was found. The candidate “One Workspace = One Operating Team” is compatible with the Frozen rule when interpreted as **one Workspace-scoped accountable team boundary**, not as Employee exclusivity or a prohibition on cross-Workspace service.

### B.5 New research inferences requiring CEO review

- “One Workspace = exactly one canonical Operating Team responsibility boundary” is a **new narrowing inference**; Frozen Authority requires a real team but does not literally define an `exactly-one` cardinality field.
- Professional Surface → Responsibility Requirement and projection metadata are **new Package candidates**, not current Package contract.
- Responsibility/Employee many-to-many relevance across Surfaces is a **derived candidate** from existing Assignment and identity rules.
- One Cycle spanning several Surfaces and several Work items is **product-consistent**, but the generic cross-Surface multi-Work execution proof is not Accepted.
- Employee presence levels, Team Scoped View contents, and optional Conversation source/return Surface context are **product-semantic candidates**, not Approved UI.

---

## C. Workspace Team Definition

A Workspace Operating Team is the Workspace-scoped responsibility system that carries its goal and operating lifecycle:

```text
Workspace Goal / Strategy
→ Workspace Leader Assignment
→ Responsibility Definitions and Requirements
→ Workspace-scoped Assignments
→ Organization Routing
→ Work / Holder / Executor
→ Result / Evidence
→ Evaluation / Leader Review / next decision
```

The team boundary is stable while membership and assignment bindings may change. Shared Employees, temporary collaborators, consultants, or replacement bindings do not create another Workspace Team.

If two bodies of work require materially independent goals, strategies, Leaders, operating lifecycles, permissions, and truth boundaries, they are candidates for sibling Workspaces—not “Surface Teams” inside one Workspace.

---

## D. Surface / Team Boundary

| Concern | Workspace Operating Team | Professional Surface |
|---|---|---|
| Owns goal/strategy responsibility | Yes | No; displays relevant context |
| Owns Leader responsibility | Yes | No |
| Owns Employee identity | No; Organization owns identity | No |
| Holds Assignments | Workspace scope references them | No; projects them |
| Declares domain WHAT | Through operating definition/process | May declare or consume requirements |
| Resolves WHO | Organization Router | Never |
| Runs Work/Cycle | Existing Runtime | Never |
| Shows domain objects and actions | Indirectly | Yes |
| Shows Work/Result/Evidence | Through truth refs | Scoped projections only |

Surface is a professional lens over shared Workspace truth. It can originate a user action that requests Work, but the action must enter the existing requirement/routing/work path.

---

## E. Responsibility as Bridge

Responsibility is the only necessary bridge between domain presentation and team execution:

```text
Surface action or object state
→ Responsibility Requirement (WHAT)
→ Organization Routing (WHO)
→ Workspace-scoped Assignment
→ Holder
→ optional verified Executor
→ Result / Evidence refs
→ projections back to relevant Surfaces
```

This keeps Surface vocabulary domain-specific while preserving one shared operating skeleton. It also prevents Package authors from hard-binding work to named Employees.

---

## F. Surface Responsibility Requirements

A professional Surface should declare responsibility requirements only for actions or states that need professional accountability. Minimum candidate declaration:

- stable domain responsibility type or responsibility-category reference;
- triggering object/action/state;
- required result contract and evidence expectations;
- scope constraints and permission boundary;
- optional default projection destinations;
- exception/escalation semantics through existing Leader/CEO gates.

It must not declare:

- `employee_id` or a fixed Employee name;
- a Surface-owned team roster;
- a second routing algorithm;
- a Surface lifecycle that duplicates Work/Cycle;
- Provider/model/tool binding as responsibility ownership.

Overview, Team, Knowledge, and read-only detail views may require no unique responsibility declarations; they can consume existing projections.

---

## G. Employee Multi-Surface Model

One Employee identity can be relevant on several Surfaces through one or more scoped Assignments:

```text
Employee identity
├─ Assignment: research responsibility @ AI 科技 Workspace
├─ Assignment: content strategy responsibility @ AI 科技 Workspace
└─ Assignment: Workspace Leader @ AI 科技 Workspace
```

Research, Content, and Growth Surfaces may all display that Employee when the active Work or object state calls for one of those Assignments. The Employee is not copied, re-created, or permanently loaded with all Surface context.

---

## H. Responsibility Multi-Surface Model

A Responsibility may span Surfaces because responsibility describes accountability, not a screen. Examples:

- content strategy consumes Research evidence, governs Content planning, and reviews Growth evaluation;
- risk/compliance may appear in Content, Feedback, and Commercialization;
- Workspace leadership spans all Surfaces without becoming the ordinary task router.

Package mappings should therefore be many-to-many: `responsibility type ↔ relevant Surface projections`. The canonical Responsibility remains independent.

---

## I. Workspace Leader Model

One Workspace Leader / Operating Owner provides the primary professional responsibility entry for the Workspace. The Leader:

- owns goal/strategy execution and operating coherence;
- maintains responsibility coverage and team division;
- reviews material Results, Evidence, evaluations, exceptions, and next-cycle proposals;
- communicates material changes and decisions to the CEO;
- may hold additional ordinary responsibilities;
- may appear across every Surface where leadership attention is relevant.

The Leader does **not** manually dispatch every routine Work item. Organization Routing resolves normal WHO. Leader intervention is for unresolved requirements, conflicts, capacity/quality exceptions, material strategy judgment, or explicit review gates.

The Leader personally enters a Work only when the Leader holds its current responsibility, is an explicit consultant/reviewer, or accepts a valid exception takeover through the same Assignment/Handoff rules. Otherwise the Leader leads through goals, coverage, review, decisions, and escalation without becoming Current Executor.

---

## J. Cross-Surface Work Flow

Recommended flow:

```text
Research object/action
→ research requirement
→ routed Work / Result / Evidence
→ same Result projected into Content planning
→ content strategy or production requirement
→ routed Work / reviewed Result
→ publishing Result projected into Growth and Feedback
→ evaluation / insight Result
→ Leader Review
→ current Cycle decision
```

Continuity rules:

- keep one canonical Work while objective, Result contract, and accountability thread remain continuous;
- create/reuse a distinct Work when a new independently executable responsibility/result contract begins;
- link Work by Cycle, predecessor/result refs, shared objects, and Handoff/consult records;
- never copy full Conversation or Result bodies just to make another Surface show them.

---

## K. Handoff

Handoff is an acknowledged transfer of accountability from one Assignment to another.

| Event | Handoff? |
|---|---|
| User changes Surface | No |
| Same Holder opens another Surface | No |
| Another Employee consults/reviews while Holder remains | No |
| Current responsibility completes and a different Assignment must own the next Result | Yes, if accountability transfers |
| Same Assignment revises its own output | No |
| Target has not acknowledged/validated acceptance | Holder has not changed |

After transfer, the Work and its refs may be projected on another Surface because responsibility relevance changed. That visual movement is a consequence, not the Handoff itself.

---

## L. Work / Result / Evidence Projection

Surface affinity should be derived in this order:

1. canonical domain object relation;
2. active Responsibility / Assignment;
3. Work type and Result contract;
4. Result/Evidence semantic type;
5. Package-declared projection rule;
6. optional explicit source/return Surface ref for UI continuity.

One Work/Result/Evidence identity may appear on several Surfaces. Surfaces store references and presentation state, not copies of truth. A Surface filter must never become the permission or ownership boundary.

No new universal `SurfaceWork`, `SurfaceResult`, or `SurfaceEvidence` entity is justified.

---

## M. Cycle × Surface

Cycle is a bounded operating period under one Operating Series. It may span Research, Content, Growth, Feedback, Commercialization, Team, and Overview projections.

- Surface does not start, close, pause, continue, or succeed a Cycle.
- Cycle close is based on result/evidence/evaluation/decision truth.
- `CONTINUE / ADJUST` may authorize exactly one successor Cycle; `WAIT / ESCALATE / PAUSE / STOP` retain their existing meaning.
- Surface navigation and render state are irrelevant to Cycle durability.

---

## N. Parallel Work

“One active Cycle” means one active Cycle per Operating Series. It does not mean one Employee, one Surface, or one Work item.

Within a Cycle, multiple Work items may be sequential or parallel when their dependencies and responsibility contracts permit it. Each Work still has exactly one accountable Current Holder at a time; execution may occur independently through existing Task/Provider substrates.

Evidence boundary: Team Operating supports multiple Work generally, but accepted Autonomous Phase 2 and the Primary Two-Cycle proof materialize one Team Operating Work per Cycle. Generic parallel cross-Surface Work inside one autonomous Cycle is therefore **PARTIAL / UNVERIFIED**, not delivered fact.

---

## O. Surface / Execution Independence

Hard invariant candidate:

> A Professional Surface is a human-visible projection and action origin. It is never the owner, scheduler, executor, or durability boundary of Work.

Consequences:

- switching or closing a Surface cannot cancel or pause Work;
- a background Work may continue with no Surface open;
- a Work may finish while the CEO is on another Surface;
- returning to a Surface reads canonical Runtime truth;
- Surface change does not replace or mutate Employee/Provider Task or Session truth;
- user interaction is not Employee execution;
- only verified execution identity may populate Current Executor.

---

## P. Employee Presence Rules

Presence must answer “who is responsibly involved here?” rather than “which agents are online?”

| Condition | Presence level |
|---|---|
| No responsibility relevance | None |
| Surface/object has an assigned responsibility but no active Work | Lightweight responsibility presence |
| Active Work has Current Holder | Owner presence with responsibility and concise state |
| Verified Task execution is active | Current Executor state, distinct from Holder |
| Consult/review is active | Collaboration presence without ownership transfer |
| Handoff is awaiting/accepted | Source/target responsibility transition |
| User explicitly opens Team or Employee | Full scoped detail / Workstation entry |

Default visible fields should remain bounded: Employee identity, scoped responsibility, Holder/Executor distinction, Work state, exception/Handoff/decision attention. Do not show fabricated “online” status, chain-of-thought, raw provider logs, token walls, or continuous monitoring telemetry.

---

## Q. Team Scoped View

Team is a Workspace-scoped view over Organization identity and Workspace Assignments. It should show:

- Workspace Leader and current responsibility scope;
- members/shared Employees relevant to this Workspace;
- responsibility coverage, unresolved requirements, and assignment availability;
- active Work ownership and material exceptions;
- real Handoffs, consults, review requests, and recent Results;
- direct entry to Employee Detail and Workstation.

It should not become:

- a Surface-specific team;
- a second Organization Center;
- a provider/session/process monitor;
- a generic agent dashboard;
- a place to redefine Runtime state.

---

## R. Employee Detail

Employee Detail is one identity view with explicit scope. Within a Workspace it may show:

- Organization identity, role, specialty, stable capabilities;
- Workspace-scoped Assignments and leadership responsibilities;
- current/recent Work, Results, Evidence, Handoffs, and exceptions allowed by permission;
- service to other Workspaces only when authorized, without importing their context;
- entry to the shared Workstation.

There is no Research Employee profile, Content Employee profile, or Growth Employee copy.

---

## S. Employee Workstation

Use one shared Employee Workstation capability. A Surface opens it with a bounded context package:

```text
Employee identity
+ Assignment / Responsibility scope
+ Workspace / Business / Company refs
+ current Work / Cycle refs
+ current domain object
+ required Knowledge / Result / Evidence refs
+ optional source Surface / return target
```

The Workstation may render domain-appropriate tools, context, and outputs, but it does not become a separate Surface-specific employee application or own another Conversation history.

---

## T. Employee Conversation Context

Conversation continuity is anchored to real work:

- canonical identity: Employee;
- accountability scope: Assignment / Responsibility;
- operating scope: Workspace and, when relevant, Business/Company;
- work scope: Work / Cycle / object / Result / Evidence refs;
- presentation context: optional source Surface and return target.

Surface is not Conversation identity. Opening the same Work from another Surface should continue the same scoped work context. Unrelated Workspace, account, or Assignment histories are not preloaded.

---

## U. CEO Assistant Boundary

CEO Assistant is a company-level coordination role outside the Workspace professional team by default. It may:

- translate CEO intent into a real Workspace request;
- retrieve progress and evidence across scoped Work;
- coordinate follow-up, remind, summarize, and escalate exceptions;
- open the same Leader/Employee Work context for the CEO.

It may not silently become:

- Workspace Leader;
- default Holder or Executor;
- domain research/content/growth/commercial professional;
- a second routing or Work system;
- a second Conversation reality disconnected from the Workspace.

If the Assistant legitimately holds a professional Workspace responsibility, that must be an explicit scoped Assignment like any other Employee.

---

## V. XHS Case

**Candidate Example only**

**Department:** 内容增长部

**Business:** 小红书运营

**Workspace:** AI 科技

Candidate operating chain:

```text
Research & Insight
→ Content Operating
→ Performance & Growth
→ Feedback
↘ optional Commercialization
→ Workspace Leader review / next-cycle decision
```

One Operating Team carries all Surfaces. Research findings, Notes, publishing receipts, Performance Records, Comment Insights, Growth Signals, and Brand Deals remain canonical domain/Result/Evidence objects. Team and Knowledge are scoped projections. Calendar is a Content Operating view, not a team or runtime boundary.

Exact responsibility names, employee bindings, headcount, and Surface taxonomy remain candidate. See `CURIS_XHS_TEAM_SURFACE_OPERATING_MAP.md` for the case map.

---

## W. RD Cross-check

The model holds for RD:

| RD Surface area | Responsibility relevance | Shared truth |
|---|---|---|
| Definition / planning | product/architecture responsibility | Goal, requirement, plan refs |
| Build / implementation | development responsibility | Work, code Artifact, provider Task |
| Review / quality | review/test responsibility | Review, Evidence, Acceptance |
| Release / operating review | Leader responsibility | Result, Evaluation, Decision |

One RD Employee may contribute across planning, implementation, or review through different Assignments; consult does not transfer Holder; revision transfers only when accountability changes. Existing RD two-cycle evidence supports Surface-independent execution and lineage, but the reviewed two-cycle document remains CEO Review Required.

---

## X. E-commerce Stress Test

Candidate Surfaces might include Market/Assortment, Merchandising, Content, Campaign, Order/Service, Performance, and Finance/Commercial. The same model survives:

- merchandising and campaign responsibilities may span several Surfaces;
- one customer-service or compliance Employee may serve multiple Workspaces;
- order exceptions can create Work without changing the current Surface;
- commercial commitments and refunds may require explicit Leader/CEO gates;
- Results/Evidence from orders, campaigns, and feedback project into Performance;
- separate stores with independent goals, Leaders, permissions, and cycles should be separate Workspaces, not Surface Teams.

This stress test exposes no need for Surface-owned Employees or a Surface Runtime.

---

## Y. Unknown Domain Bootstrap

For an unknown domain:

1. recover current Company → Department → Business → Workspace truth;
2. perform Domain Research;
3. define the Semantic Model: goal, strategy, canonical objects, operating loops, success/evidence boundary;
4. derive the minimum Professional Surface Model;
5. define the Responsibility Model by WHAT, never named Employees;
6. map Capability requirements to those responsibilities;
7. design Team coverage and bind/route existing Employees through scoped Assignments;
8. declare Package navigation, Surface requirements, and Result/Evidence projections;
9. validate Handoff, exceptions, decisions, permissions, restart, context isolation, and operating continuity;
10. keep unknown vocabulary/provider facts `UNKNOWN`, and create a sibling Workspace only when goal/Leader/lifecycle/truth boundaries are genuinely independent.

No domain bootstrap step creates a new Team, Employee, Work, Result, Cycle, or Runtime primitive.

---

## Z. Package / Runtime Gaps

### Z.1 Classification

| Capability | Classification | Evidence / implication |
|---|---|---|
| Long-term Workspace Operating Team + Leader semantics | **ALREADY EXISTS** | Frozen Shared Authority. |
| Responsibility Requirement → Organization Routing → Assignment | **ALREADY EXISTS** | Frozen semantic model; routing implementation and E2E evidence exist. |
| Holder / Executor separation | **ALREADY EXISTS** | Runtime review and Accepted real Employee E2E. |
| Handoff / consult / review / return | **ALREADY EXISTS** | Existing Work-centered routing; no Surface dependency. |
| Result / Evidence / Evaluation / Leader Review / Decision | **ALREADY EXISTS** | Existing shared and autonomous operating chain. |
| Durable single-active-Cycle and successor authorization | **ALREADY EXISTS** | Phase 1–3B Accepted. |
| Primary two-cycle RD E2E | **PARTIAL** | Implemented, CEO Review Required; not Accepted. |
| Multiple Work items inside one autonomous Cycle | **PARTIAL / UNVERIFIED** | Product model permits it; current autonomous reviews do not accept this broader proof. |
| Cross-Surface Team Operating E2E | **MISSING ACCEPTANCE EVIDENCE** | No accepted generic cross-Surface proof found. |
| Generic Domain Navigation / multi-Surface registry | **PACKAGE DECLARATION GAP** | Current Package contract exposes fixed shell panes rather than domain Surface declarations. |
| Surface responsibility requirement mapping | **PACKAGE DECLARATION GAP** | Must declare WHAT/projection semantics without Employee bindings. |
| Work/Result/Evidence Surface affinity | **PACKAGE DECLARATION GAP** | Prefer derived mapping/ref rules, not new canonical objects. |
| Responsibility-aware Employee presence | **UI PROJECTION GAP** | Existing Holder/Executor state exists; multi-Surface consumption is not proven. |
| Team Scoped View / shared Workstation entry across Surfaces | **UI PROJECTION GAP** | Shared semantics exist; final multi-Surface experience is not accepted. |
| XHS operating responsibilities and bindings | **PARTIAL / RESEARCH** | External research is Expert Recommendation; exact operating definition remains candidate. |

### Z.2 Minimum future Package implications

If this research is accepted, a later Package proposal may need only declarative additions such as:

- Domain Navigation and Surface registry;
- Surface → responsibility requirement references;
- object/Work/Result/Evidence projection rules;
- bounded Employee presence policy;
- optional source/return Surface refs.

It should not contain Employee IDs, team rosters, runtime transitions, provider session logic, Cycle state, or another Handoff model.

### Z.3 Stop point

This research stops at **CEO REVIEW REQUIRED**. It does not authorize cross-track synthesis, Authority reconciliation, Package contract changes, Runtime work, schema changes, UI redesign, prototype edits, implementation, commit, or push.
