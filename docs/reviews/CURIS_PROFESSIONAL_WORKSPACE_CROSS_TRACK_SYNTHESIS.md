# CURIS PROFESSIONAL WORKSPACE — CROSS-TRACK SYNTHESIS

**Authority Class:** REVIEW

**Status:** Review

**Disposition:** PRODUCT / WORKSPACE AUTHORITY CANDIDATE · CEO REVIEW REQUIRED

**Date:** 2026-08-21

**Target Authority:** Product Blueprint / Master Map / UI Blueprint / applicable Workspace and Package Authority, only after a separate accepted reconciliation

**Authority Effect:** NONE

**Implementation:** NOT AUTHORIZED

> 本文只综合已经完成的三条研究，不新增研究问题，不修改任何 Current / Frozen Authority，不定义最终 Package Schema，不进入 UI 重设计或实现。

---

## 1. Executive Verdict

三条研究可收敛为一套一致的 Professional Workspace Product Model：

> **Workspace 不是一张页面，而是一个由真实团队持续经营业务的完整专业环境。**

一个长期 Workspace：

- 位于 `Company → Department → Business → Workspace` 的 canonical 层级中；
- 有一个 canonical Operating Team responsibility boundary；
- 有一个 Workspace Leader / Operating Owner；
- 有多个 Responsibility；
- Employee 通过 Workspace-scoped Assignment 承担 Responsibility，身份不复制；
- 可以包含多个围绕稳定专业问题组织的 Professional Surface；
- 复用同一套 Work、Result、Evidence、Handoff、Cycle、Evaluation、Decision 与 Learning truth。

Professional Surface 是这个专业环境中的工作面。它不是 Team、Employee、Responsibility、Cycle、Runtime 或第二个 Workspace。

### 1.1 Unified model

```text
Company
└─ Department
   └─ Business
      └─ Workspace = one Professional Operating Environment
         ├─ one Workspace Leader
         ├─ one canonical Operating Team responsibility boundary
         │  ├─ Responsibilities
         │  ├─ Assignments
         │  └─ Employees
         ├─ multiple Professional Surfaces
         │  ├─ domain objects and actions
         │  ├─ responsibility requirements
         │  └─ Work / Result / Evidence projections
         ├─ scoped Team / Knowledge / Artifact views
         └─ one shared operating truth and existing Runtime
```

### 1.2 Synthesis result

| Question | Result |
|---|---|
| Product model coherent? | **YES — PRODUCT MODEL ACCEPTABLE AS CANDIDATE** |
| Authority conflict? | **No Frozen conflict found.** One XHS candidate-default tension requires later reconciliation if accepted. |
| Generic multi-Surface implementation delivered? | **NO** |
| New Runtime required? | **NO** |
| Authority updated by this document? | **NO** |
| Next gate | **CEO Review of the separate 10-item Decision Packet** |

---

## 2. Inputs and Truth Classification

### 2.1 Three research tracks consumed

| Track | Current class | Contribution to this synthesis |
|---|---|---|
| XHS Professional Workspace External Domain Research | RESEARCH / EXPERT RECOMMENDATION | Real XHS operating lifecycle, candidate Surfaces, objects, cadence, responsibilities, Calendar placement, optional Commercialization. |
| Professional Workspace Internal Architecture Research | REVIEW / CANDIDATE | Workspace ≠ Page, multiple Professional Surfaces, Domain Navigation, Four-Pane responsibility mapping, Core/Package/Instance/View ownership. |
| Team × Surface Operating Model Research | RESEARCH / CEO REVIEW REQUIRED | One Workspace team boundary, Responsibility bridge, multi-Surface Employee/Work/Cycle model, Handoff and Runtime boundary. |

### 2.2 Current/Frozen facts preserved

- Current hierarchy remains `Company → Department → Business → Workspace`.
- A long-term Workspace must be carried by a real Operating Team with Leader, members, and explicit responsibilities.
- Leader is a scoped Responsibility Assignment held by an ordinary Employee, not a special Employee type.
- Responsibility Requirement declares WHAT and never directly names an Employee.
- Organization Routing resolves WHO; Capability determines HOW.
- Assignment carries responsibility; Employee identity is not copied for each Workspace or Surface.
- Team Operating and Autonomous Operating reuse the shared Work, Handoff, Result, Evidence, Cycle, Evaluation and Decision foundations.
- CEO Assistant coordinates but does not replace professional Leader or Employee responsibility.
- Four-Pane defines responsibility areas, not a fixed number of visible columns.

### 2.3 New Candidate conclusions

The following require CEO acceptance before any Authority reconciliation:

1. `Workspace = Professional Operating Environment` as the unified product expression.
2. One long-term Workspace has one canonical Operating Team responsibility boundary.
3. One Workspace may contain multiple Package-declared Professional Surfaces.
4. Workspace-local Domain Navigation belongs to Context responsibility; Main shows the selected Professional Surface; Utility shows selected detail/tool/evidence.
5. Professional Surfaces declare Responsibility Requirements and projections but never Employee IDs.
6. Work, Result, Evidence and Employee presence may project across several Surfaces without duplication.
7. XHS uses Operating Overview as the candidate default; Calendar belongs inside Content Operating.

These are Candidate conclusions, not current implementation facts.

---

## 3. Professional Workspace Product Definition

### 3.1 Workspace

A Workspace is a canonical, persistent, Business-owned operating scope and professional environment. It carries:

- Workspace Goal, positioning and strategy scope;
- Workspace Leader responsibility;
- Operating Team responsibility coverage;
- permissions and data boundary;
- Workspace Package/version reference;
- Operating Series and bounded Cycles;
- domain objects, Work, Results, Evidence, Decisions and Learning references;
- one durable operating history.

Changing Surface, object, detail view, filter or pane state does not create another Workspace.

### 3.2 Professional Surface

A Professional Surface organizes one stable class of professional problem inside the Workspace. It may contain domain objects, object views, actions, tools and relevant work projections.

A Surface:

- does not own a Team or Employee roster;
- does not own the Workspace Leader;
- does not own Work, Result, Evidence or Cycle truth;
- does not start or stop execution because a user opens or closes it;
- does not become a Sub-Workspace, Mini Workspace or Workspace-inside-Workspace;
- may be required, optional or conditionally available according to the Workspace Package and current capability/permission/stage truth.

### 3.3 Surface versus other concepts

```text
Surface ≠ Team ≠ Employee ≠ Responsibility ≠ Work ≠ Cycle ≠ Runtime
```

If an area requires its own Goal, Leader, team accountability, Operating Series, permission/data boundary and lifecycle, it is a candidate sibling Workspace—not another Surface Team.

---

## 4. Navigation and Four-Pane Responsibility Model

```text
Curis Global Navigation
→ company-level location and entry to Departments, Businesses and Workspaces

Workspace Context
→ current Workspace identity, Domain Navigation and selected Surface context

Main
→ current Professional Surface and relevant shared Work Area

Utility
→ selected object Detail, editor, preview, Evidence or professional tool

CEO Assistant
→ one Global Company Employee with current scoped context
```

### 4.1 Hard boundary

Four-Pane is a responsibility contract, not four permanent physical columns. Context and Utility may collapse, overlay, focus, or appear only when needed. Main remains the professional subject. CEO Assistant is not a fifth pane and not a Workspace-local replacement Assistant.

### 4.2 Domain Navigation

Domain Navigation belongs to the current Workspace. It selects Professional Surfaces without changing Workspace identity. It is formed from real domain semantics and declared by the Workspace Package, while Core validates and renders it.

This synthesis does not decide pixels, breakpoints, component layout, final route syntax, exact menu order, or responsive behavior.

---

## 5. Operating Team, Responsibility and Employee

### 5.1 One Workspace team boundary

One long-term Workspace has one canonical Operating Team responsibility boundary. This means one accountable business team reality, not:

- one fixed headcount;
- one Employee per Responsibility;
- one exclusive Organization team that cannot share Employees;
- one Team for each Surface;
- a prohibition on temporary collaborators or cross-Workspace service.

The Workspace Leader is responsible across the entire Workspace for goal/strategy execution, team coverage, cross-Surface coherence, material Result review, exceptions, CEO communication and next-cycle judgment.

### 5.2 Responsibility is the bridge

```text
Surface action or object state
→ Responsibility Requirement: what responsibility is needed
→ Organization Routing: who is eligible and selected
→ Workspace-scoped Assignment
→ Employee as Holder / verified Executor
→ Result / Evidence
→ projection back to all relevant Surfaces
```

Surface authors may declare responsibility semantics or categories. They must not bind a named Employee or `employee_id`. Replacing an Employee changes the Assignment/routing result, not the Package.

### 5.3 Multi-Surface Employee model

One Employee can carry multiple Responsibilities and therefore work across multiple Surfaces while retaining one identity. One Responsibility may also be relevant to several Surfaces. Conversation and Workstation context change by Assignment, Work, Workspace, object and relevant evidence—not by creating a Surface-specific Employee profile.

Leader does not manually assign every ordinary Work item. Normal WHO resolution remains Router-owned; Leader enters individual Work only when holding that responsibility, acting as an explicit reviewer/consultant, or accepting an exception through the same accountability rules.

---

## 6. Cross-Surface Operating Flow

Employees do not “move between pages” as a business event. The canonical flow is:

```text
Work
→ Result
→ Evidence
→ Evaluation or responsibility change
→ Consult / Review / Handoff when genuinely required
→ next Responsibility Requirement
→ next Work
```

The same canonical Work, Result or Evidence may be visible on several Surfaces through references and derived projections. Surface navigation itself has no effect on ownership or execution.

### 6.1 Handoff boundary

Handoff is acknowledged accountability transfer between Assignments. It is not a Surface transition.

- Changing Surface: no Handoff.
- Same Holder opens another object or Surface: no Handoff.
- Consult/review while Holder remains accountable: no Handoff.
- Another Assignment accepts accountability for the next required Result: Handoff.

### 6.2 Cycle boundary

One Operating Cycle may span Research, Content, Publishing, Growth, Feedback and Leader Review. `single-active Cycle` means one active Cycle per Operating Series; it does not mean one Surface, one Employee, one Task or necessarily one Work item.

The product model permits sequential or parallel Work inside a Cycle. Generic cross-Surface multi-Work Autonomous E2E remains unaccepted implementation evidence and must not be claimed as delivered.

### 6.3 Execution independence

Opening, closing or switching a Surface does not start, pause, transfer or stop Employee, Provider, Work, Session or Cycle execution. User presence is not Employee execution. Only verified execution identity may become Current Executor.

---

## 7. Team, Knowledge, Artifact and Evidence Reuse

### 7.1 Team

The Team view is a Workspace-scoped projection of Company OS Employee, Role, Assignment, Responsibility, Work, Handoff and Result truth. It may show Leader, members, responsibility coverage, unresolved/blocked responsibility, real cross-Surface Handoffs and recent material Results.

It must not become an XHS Team System, RD Team System, Employee Monitoring Center or agent log wall.

### 7.2 Knowledge and materials

Knowledge and materials are Workspace/Surface-scoped projections over Curis Global Knowledge, Artifact and Evidence truth. Domain Packages may specify which references are relevant; they do not create a second domain Knowledge Base or copy shared truth.

Prohibited duplicates include:

- XHS Knowledge Base;
- RD Knowledge System;
- Surface-specific Artifact or Evidence stores;
- Domain-specific shared Team/Runtime systems.

---

## 8. XHS Candidate — AI 科技

**Authority status:** Candidate example only

```text
Department: 内容增长部
└─ Business: 小红书运营
   └─ Workspace: AI 科技
```

### 8.1 Candidate Professional Surfaces

| Surface | Product role | Status in this synthesis |
|---|---|---|
| 经营概览 | Restore current stage, goal, strategy, attention, latest judgment and next step | Candidate default |
| 研究洞察 | Research audience, competitors, trends, keywords and hypotheses | Core candidate |
| 内容运营 | Topic/content strategy, production, review, Calendar, publishing queue and publishing | Core candidate |
| 数据增长 | Performance, audience evidence, experiment evaluation and growth signals | Core candidate |
| 用户反馈 | Comments/DM/questions, risk, insight and lead feedback | Lightweight Surface or subordinate view; exact menu level unresolved |
| 商业化 | Brand opportunity, proposal, delivery and settlement linkage | Optional/conditional candidate |
| 团队 | Workspace-scoped Company OS Team projection | Scoped shared view |
| 资料 | Workspace-scoped Knowledge/Artifact/Evidence projection | Scoped shared view |

### 8.2 Calendar decision

Calendar is an Object View inside Content Operating, representing Note/content objects against time and publishing state. It is not the Workspace default and does not represent the whole business.

This conclusion creates a deliberate Candidate delta against the older XHS `Calendar-Dominant` default candidate. The `Content Object × Time` semantic remains reusable; only default-entry status is proposed for change. No existing XHS Authority or UI is changed by this synthesis.

### 8.3 Candidate operating chain

```text
Research Result / Evidence
→ Content strategy and production Work
→ Review and publishing Result
→ Growth / Feedback Evidence
→ Evaluation
→ Workspace Leader Review
→ Next-cycle Decision
```

All stages may belong to the same Operating Cycle. Exact XHS responsibility names, Employee bindings, headcount, menu hierarchy and provider availability remain unfrozen.

---

## 9. Workspace Package Authority Candidate

The Workspace Package should eventually be the declarative owner of domain composition. At product level it needs to express:

- Domain Navigation;
- Professional Surface Registry;
- Surface responsibility requirements;
- domain object and Object View mappings;
- object Detail/editor/tool mappings;
- Work, Result and Evidence projection relevance;
- required, optional and conditional Surface availability;
- Capability requirements;
- scoped reuse requests for Team, Knowledge, Artifact and Evidence views.

### 9.1 Ownership boundary

| Layer | Owns | Does not own |
|---|---|---|
| Core | canonical identity, Shell responsibilities, validation, permissions, shared Runtime truth, failure/recovery | XHS/RD menu semantics or domain staffing |
| Package | domain navigation, Surfaces, semantic mappings and requirements | Employee IDs, credentials, instance truth, Runtime lifecycle |
| Workspace Instance | pinned Package/version, enabled optional capabilities/Surfaces, domain instance data | arbitrary new Surface definitions |
| View/User preference | current selection, last active, filters and layout | Goal, Assignment, Result, Evidence or Cycle truth |

### 9.2 Not decided here

This Candidate does not define the final manifest, JSON keys, database fields, route format, migration, API, validation algorithm, renderer, component registry or deployment process.

---

## 10. Runtime Boundary

Existing shared Runtime remains the only owner of:

```text
Work
Responsibility
Assignment
Employee
Handoff
Result
Evidence
Cycle
Evaluation
Decision
Learning
```

Professional Surfaces consume and project this truth. They do not own lifecycle or durability.

The following are prohibited by this Candidate:

- Surface Runtime;
- Surface Agent;
- Surface Cycle;
- Surface Result;
- Surface Evidence;
- Surface Session;
- Domain-specific shared Runtime equivalents.

No evidence reviewed requires one of these additions.

---

## 11. Product Model versus Current Implementation

### 11.1 Product model status

**PRODUCT MODEL ACCEPTABLE AS A COHERENT AUTHORITY CANDIDATE.**

The model is compatible with the current hierarchy, Shared Workspace responsibilities, Team Operating, Responsibility Routing and Operating Lifecycle. It reuses existing primitives and provides one domain-neutral explanation for XHS, RD, e-commerce and unknown domains.

This does not mean the model is Current Authority or implemented.

### 11.2 Current implementation truth

| Capability | Current classification |
|---|---|
| Workspace-scoped Responsibility Routing, Assignment, Holder/Executor, Handoff, real Employee execution and Result return | **IMPLEMENTED / ACCEPTED in bounded evidence** |
| Durable Cycle, execution closure, Evaluation, Leader Review, successor control, cross-domain contract proof and evidence-bound Learning | **IMPLEMENTED / ACCEPTED in their bounded Reviews** |
| Existing RD/XHS domain-specific Workspace implementations | **IMPLEMENTED / ACCEPTED only within their recorded bounded scope; not this generic model** |
| Controlled declarative Workspace Package with one navigation entry and fixed Main/Context/Utility composition | **PARTIAL substrate** |
| Generic multi-Surface Workspace Package | **NOT IMPLEMENTED / NOT ACCEPTED** |
| Domain Navigation and Professional Surface Registry implementation | **NOT IMPLEMENTED / NOT ACCEPTED** |
| Surface Responsibility Requirement declaration | **NOT IMPLEMENTED / NOT ACCEPTED** |
| Generic object/detail and Work/Result/Evidence projection across Surfaces | **NOT IMPLEMENTED / NOT ACCEPTED** |
| Multi-Surface UI projection and navigation experience | **NOT IMPLEMENTED / NOT ACCEPTED** |
| Cross-Surface multi-Work Autonomous E2E | **NOT ACCEPTED / UNVERIFIED** |
| RD and XHS migration to the final generic Professional Workspace product model | **NOT IMPLEMENTED / NOT ACCEPTED** |

The implementation gaps are future bounded work. They do not authorize code, Schema, DB, Frontend, Prototype or Package changes in this round.

---

## 12. CEO Acceptance Scope and Next Gate

The CEO is asked only to decide the product principles in `CURIS_PROFESSIONAL_WORKSPACE_CEO_DECISION_PACKET.md`.

If accepted, a separate Authority Reconciliation must identify exact target paragraphs, superseded XHS candidate language, owners, allowed documents and next gates. Only after that may a Package proposal or design/implementation Issue be considered.

```text
CANDIDATE ONLY
NO AUTHORITY CHANGE
NO IMPLEMENTATION
NO UI REDESIGN
STOP FOR CEO REVIEW
```

