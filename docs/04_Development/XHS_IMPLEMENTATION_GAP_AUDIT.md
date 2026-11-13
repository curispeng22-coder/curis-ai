# XHS Implementation Gap Audit

**Status:** Review  
**Date:** 2026-08-15  
**Mode:** Read-only implementation audit — no production code, schema, Blueprint, Frozen design contract, or activity database was changed.  
**Source:** `docs/00_Context/CURRENT_STATE.md`; `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` (Frozen); `docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md` (Approved); `docs/03_Design/Curis_XHS_Workspace_UI_Authority_Map.md` (Approved); `curis-ui-prototype/_system/tokens.css` (Frozen token source as referenced by the Authority Map); newest relevant `docs/08_Change_Log/CHANGE_LOG.md` entries.

## 1. Audit boundary and finding

The current XHS route is a **generic Runtime inspection page**, not the approved XHS
office.  It persists real Workspace and content objects, but presents them as cards,
forms, Simulation controls, and raw Runtime facts.  The approved Calendar → Note
working surface, adaptive panes, responsibility semantics, decision gate, and
automatic post-publish analytics are not yet implemented.

This is a migration, not a rewrite of Company Runtime.  Reuse the existing Runtime
Company/Workspace isolation and `runtime_entities` graph.  Replace the XHS route's
generic presentation with a workspace-scoped shell and add only the content commands
needed to make the approved XHS state chain truthful.

### Evidence read

| Area | Current evidence | Audit result |
| --- | --- | --- |
| App root | `frontend/app/layout.js` mounts `RuntimeProvider`, `GlobalAssistantProvider`, token-backed globals, and shared theme state. | Reuse as-is. |
| Current desktop shell | `frontend/components/terra/TerraShell.js` renders a global 52px topbar over a fixed/drawer `TerraSidebar`. | Conflicts with Top-aligned Independent Pane / Pane-local Header. |
| Current navigation | `TerraSidebar.js` + `TerraNavData.js` are global, responsive, and token based. | Data/icons reusable; layout and workspace-child semantics need migration. |
| XHS route | `frontend/app/ceo-office/workspace/xhs/page.js` delegates entirely to `WorkspaceRuntimeView({ businessType: "XHS" })`. | Conflicting legacy UI; no XHS-specific container. |
| XHS UI | `WorkspaceRuntimeView.js` renders generic `ContentRuntime`: create form, cards, versions, receipts, interactions, simulations. | Real read projection, but not Calendar / Note / Split / Presence / Decision UX. |
| Runtime projection | `runtime_foundation_router.py` returns workspace-scoped employees, content, receipts, interactions, handoffs, acceptance, decisions, evidence and simulations. | Reusable read foundation. |
| Runtime persistence | `runtime_entities` / `runtime_links` carry scope, lifecycle, owner, versions, evidence, execution refs and JSON data. | Reusable; Phase 1 does not require a new table. |
| Content commands | Create ContentItem/initial immutable version; manual receipt and interaction APIs exist and preserve `CEO_MANUAL` as `UNVERIFIED`. | Reusable partial path; content handoff/review/publish lifecycle has no public XHS command path. |
| Existing test proof | `test_runtime_workspace_foundation.py` proves isolated XHS/TTK content objects, version/receipt/manual boundary and restart reads. | Foundation proof only; no approved XHS office lifecycle proof. |

## 2. Existing architecture, separated by reuse boundary

### 2.1 Desktop shell and page composition

`RootLayout` owns the shared runtime snapshot, Assistant and theme.  `TerraShell`
then adds the legacy global topbar and navigation to each page.  A Workspace currently
renders *inside* this shell.  Therefore Context/Utility cannot become top-aligned
independent panes without either changing the global shell for every page or replacing
the shell at the XHS route boundary.

There is no existing Company-wide Object Search surface, pane state controller,
pointer-driven resizer, or Utility maximize overlay.  The only reusable search control
is the presentational `TerraSearch`; it has no company-object query behind it.

### 2.2 XHS route and state today

The XHS route selects an existing workspace by `workspace_id`, reads only its Runtime
detail, and refuses unknown/out-of-company IDs.  That scope behavior is correct and
must remain.  The generic content component can create `CONTENT_ITEM` plus one
immutable `CONTENT_VERSION`; it displays versions, manual receipts and interaction
records honestly.

However it has no scheduled-at data, title/body/tags data, selected Note route state,
month aggregation, Context/Utility surfaces, employee presence, or XHS-specific
decision controls.  Its Simulation actions are development verification controls,
not the approved content-office automation model.

### 2.3 Runtime and API today

The current projection already returns the object families needed by a read model:

```text
Workspace
  ├─ AI_EMPLOYEE / ROLE_SLOT / CAPABILITY_BINDING
  ├─ CONTENT_ITEM → CONTENT_VERSION
  ├─ PUBLICATION_RECEIPT / INTERACTION_ITEM
  └─ HANDOFF / EVIDENCE / ACCEPTANCE / DECISION_PACKET
```

The object graph is Company and Workspace scoped.  This is the correct persistence
base for XHS.  It does **not** yet express the approved content state chain through
public APIs:

```text
创作中 → 自动交接审核 → Needs CEO → CEO 决策 → 自动发布 → Result → System Analytics
```

The existing `add_content_version()` is not exposed by the Runtime Foundation router
and requires a `DRAFT` item even though the create command produces `IDEA`.  This is a
real lifecycle/API mismatch, not a UI gap.  The existing manual receipt route is
correctly constrained to a CEO-recorded, `UNVERIFIED` fact and must not be relabelled
as verified platform publication.

## 3. Gap matrix

### 3.1 Shell

| Required capability | Existing evidence | Status | Required migration |
| --- | --- | --- | --- |
| Top-aligned Independent Pane | `TerraShell` has a global topbar above nav + main. | **CONFLICTING LEGACY** | Mount a new Workspace-only pane container at the XHS route; do not change RD/TTK `TerraShell` in this slice. |
| Pane-local Header | Only global topbar; no Context/Utility headers. | **MISSING** | New Nav/Main/Context/Utility header slots. |
| T1 Navigation toggle | Mobile drawer only; desktop sidebar cannot fully collapse/reopen from Main header. | **PARTIAL** | Workspace container owns T1 and transfers its reopen affordance to Main header. |
| T2 Context toggle | No Workspace context pane. | **MISSING** | New stable Main-header toggle; XHS Context = 选题库 / 信号. |
| T3 Utility toggle | No Workspace utility pane. | **MISSING** | New Main/Utility-header transfer behavior; XHS Utility = 图文预览. |
| Resizable adaptive surface | No pointer resizer, min/max, per-workspace width memory, or narrow overlay behavior. | **MISSING** | Client-scoped pane hook plus CSS grid; persist widths in local storage keyed by Workspace ID. |
| Company-wide Object Search | `TerraSearch` is UI-only; no object query API/surface. | **PARTIAL** | Add a scoped Runtime search endpoint and Search Surface; search only persisted objects, never mock results. |
| Utility maximize | No overlay/maximize behavior. | **MISSING** | Local UI overlay over Workspace shell; no business-state mutation. |
| Token discipline / three themes | `globals.css` mirrors the Frozen `--ui-*` values; root theme handling exists. | **EXISTS + REUSABLE** | Consume existing tokens only; resolve source duplication separately, outside this XHS issue. |

### 3.2 Shared Company patterns

| Required capability | Existing evidence | Status | Required migration |
| --- | --- | --- | --- |
| Object Owner | `owner_ref` exists, but generic UI calls it “负责人”. | **EXISTS + NEEDS MIGRATION** | Project stable owner separately from stage responsibility. |
| Current Responsibility / Current Executor | No separate read/write fields or XHS projection. | **MISSING** | Add explicit content runtime fields in `data_json`; populate only with real employee/system facts. |
| Employee Presence | Workspace employee entities exist; generic cards do not bind them to a Note. | **PARTIAL** | New Note-level presence projection/renderer. Never use object owner or historic actor as presence. |
| System Activity | Simulation status exists but is not a System Activity model. | **PARTIAL** | Project Analytics/polling as executor=`none`; no avatar/no workstation affordance. |
| Handoff Event | `HANDOFF` entity and links exist for Operating Cycle; XHS detail returns handoffs. | **EXISTS + NEEDS MIGRATION** | Content-specific automatic handoff command must create linked, readable events. |
| Automation by default | RD Cycle has automatic Runtime transitions; XHS UI exposes manual Simulation buttons. | **CONFLICTING LEGACY** | XHS transition happens from completed execution/decision callback, not from a CEO “next step” UI control. |
| Needs CEO / Decision Gate | `ACCEPTANCE` / `DECISION_PACKET` exist for RD; generic XHS does not render or command one. | **PARTIAL** | Add a content review decision command and XHS Decision Banner. |
| Result Reference | Receipt/interaction entities are read and displayed as cards. | **EXISTS + NEEDS MIGRATION** | Convert to lightweight references that open Utility; retain detail accessibility. |

### 3.3 XHS instance

| Required capability | Existing evidence | Status | Required migration |
| --- | --- | --- | --- |
| Publishing Calendar | No calendar query/model/UI; global calendar route is unrelated. | **MISSING** | Persist scheduled date on Note and aggregate XHS Notes by month. |
| Multi-Note Month View | No day-density/primary priority implementation. | **MISSING** | Implement P0–P4 selection and `+N` collapse; Day Focus stays reserved. |
| Calendar → Note Split | Generic ContentItem card list only. | **MISSING** | Route/query selected note; one Main pane with Calendar and Split views. |
| Note editing surface | Initial version is created from three generic fields; subsequent version API absent. | **PARTIAL** | XHS note draft/version commands and editor with immutable submitted/published versions. |
| Context = 选题库 / 信号 | No XHS Context source/entity projection. | **MISSING** | First slice may read actual Knowledge entries and Note signal refs; empty state must say no source is bound. |
| Utility = 图文预览 | No preview renderer. | **MISSING** | Render persisted Note title/body/cover reference; unknown local files stay a reference, not a fabricated preview. |
| Review / Needs CEO | No content review state/API/UI. | **MISSING** | Content review gate linked to reviewer, evidence and decision. |
| Published / Analytics | Manual receipt/interactions are persisted; no actual XHS connector, no analytics automation/projector. | **PARTIAL** | Show manual receipt as `UNVERIFIED`; trusted connector remains a capability gap. Build system activity only after a real receipt/metric read exists. |

## 4. Migration strategy and direct answers

### 4.0 P0 Runtime architecture review update

`XHS_RUNTIME_ARCHITECTURE_REVIEW.md` is now a required companion to this audit.  Its
decision narrows the Runtime work: `CONTENT_ITEM` remains an XHS Note; existing Task /
Agent execution remains its child substrate; `HANDOFF`, `DECISION_PACKET`, `EVIDENCE`,
receipt, interaction and Artifact references remain Company OS facts.  The missing
work is not an XHS workflow.  It is a small subject-scoped composition layer because
current Handoff and Decision creators are embedded in the RD `CYCLE` path.

The first implementation Issue must therefore split its authority boundary:

1. an XHS domain command/projection for Note/version/review/publish data; and
2. a separately reviewed minimal Shared Runtime command helper for Work Context,
   Handoff, Decision Packet and Result Reference.

No XHS UI issue may duplicate those shared entities, or create client-side substitutes.

### 4.1 Shell choice

**Use a new, route-scoped `WorkspacePaneShell` to replace `TerraShell` for XHS only.**
This is a gradual migration, not a global refactor and not a second app shell.  It
uses the existing root providers, theme, icon set, runtime fetch client and navigation
data, but owns the four-pane contract inside the XHS route.  RD, TTK and non-Workspace
pages continue using `TerraShell` unchanged.

This is the smallest safe way to satisfy the Frozen “no Global Topbar” requirement
without breaking other Workspaces.  After independent RD/TTK instance specifications
exist, they can opt into the same container instead of copying the XHS layout.

### 4.2 Reuse and retirement

| Reuse now | Do not reuse directly | Why |
| --- | --- | --- |
| `RuntimeProvider`, `GlobalAssistantProvider`, `workspaceFetch`, `runtimeApi` read calls, `TerraIcon`, token classes, `TerraButton` / `TerraTag` primitives, `TerraNavData` labels/links | `TerraShell` outer layout, `TerraSidebar` DOM, `WorkspaceRuntimeView` / `ContentRuntime` as the XHS office, Studio's fixed XHS stage template, Simulation action UI | The first group is shared infrastructure. The second encodes the replaced global topbar, generic Runtime card view, or a pre-approval content lifecycle. |
| `runtime_entities`, `runtime_links`, `CONTENT_ITEM`, `CONTENT_VERSION`, `PUBLICATION_RECEIPT`, `INTERACTION_ITEM`, `HANDOFF`, `DECISION_PACKET`, scoped workspace projection | Visual v4 / Shell Exploration HTML/CSS/JS, old Prototype interactions | Runtime entities are current persisted facts; prototype mechanics are Reference Only by Authority Map. |

No existing component is physically deleted in the first slice.  The XHS generic
presentation becomes unmounted only at the XHS route after its replacement has passed
acceptance.

### 4.3 RD and other Workspace safety

1. Keep the new shell under `frontend/components/workspace/` and select it only in
   `frontend/app/ceo-office/workspace/xhs/page.js`.
2. Do not edit `TerraShell`, shared nav behavior, generic RD Cycle controls, or TTK
   content rendering in the XHS issue.
3. Filter every new API command by current Company + Workspace + `business_type=XHS`.
4. Run existing RD/TTK route and focused Runtime tests as no-regression checks; do not
   claim their new-shell implementation.

### 4.4 What can genuinely connect now

- Company/Workspace-scoped reads, identity checks, persistence, restart reads, version
  references, manual receipt and manual interaction facts.
- Actual Company AI employee entities, role slots and capability bindings where the
  Workspace has reached that Runtime state.
- Existing Evidence/Handoff/Decision entities, provided XHS gets an explicit,
  authorized content transition command rather than reusing RD Cycle controls.

### 4.5 What remains an honest non-success state

- No configured XHS Connector: no API publication or verified external ID.
- No provider/executor completion: no automatic “创作完成” or fabricated Handoff.
- No external metric read: Analytics is “等待外部结果” or “未读取”，not zero metrics
  and not a fake analyst employee.
- Missing knowledge/signal sources: Context opens an explicit empty/gap state, not
  generated trend material.

### 4.6 Is the current Employee / Agent Runtime sufficient?

**No, not for the full approved chain.**  It is sufficient for employee identity,
Workspace scope, capability binding and generic evidence/decision objects.  It is not
sufficiently exposed for `创作 → 审核 → Needs CEO → 发布 → Analytics`: ContentItem
has no public transition/assignment/handoff/decision commands, and its initial `IDEA`
state conflicts with the version writer's `DRAFT` requirement.  This is P0 Runtime
work, not a frontend-only styling task.

### 4.7 Data/API/store decision

No new SQLite table is needed for the first vertical slice.  Use the existing
`runtime_entities` / `runtime_links` model and add a narrow XHS content projection:

```text
CONTENT_ITEM.data
  scheduledAt, title, body, tags, coverRef,
  objectOwnerRef, currentResponsibilityRef, currentExecutorRef,
  activityKind(employee|system|none), currentStage
```

Create linked `HANDOFF`, `EVIDENCE`, `DECISION_PACKET`, `PUBLICATION_RECEIPT`, and
`INTERACTION_ITEM` facts through explicit Runtime commands.  `Needs CEO` is a derived
surface state from a linked `DECISION_PACKET=WAITING_CEO`, not a new global ContentItem
state. Pane open/closed state
and widths are view preference only: store them client-side, keyed by Workspace ID;
do not create a server store for a local layout preference.  Note selection belongs in
the URL (`workspace_id`, `note_id`) so refresh/restart remains revisit-able.

A scoped object-search API is required for the Frozen Shell contract.  It should query
only already-persisted Company objects and return type/title/context/route metadata;
no AI search, command palette or hidden broad search is part of this slice.

### 4.8 P0 implementation blockers

1. **Content lifecycle bridge:** public, Company/Workspace-scoped commands that make
   versioning and XHS review transitions legal and auditable; resolve the current
   `IDEA`-creation / `DRAFT`-version-writer mismatch at the Runtime root.
2. **Shared subject composition:** a narrow generalization of the existing RD-only
   Handoff/Decision creation path for any scoped Workspace business object. It must
   reuse `HANDOFF`, `DECISION_PACKET`, `EVIDENCE` and links; it is not a workflow engine.
3. **Content projection:** fields required for Calendar, Note selection and the
   three responsibility semantics must be persisted/read in the same source.
4. **WorkspacePaneShell:** only after the component has a clear route boundary and
   per-Workspace pane-state isolation.
5. **Company object search:** minimal scoped query endpoint, not a client-side fake
   search corpus.
6. **Desktop window boundary:** verify Tauri's native titlebar/traffic-light
   integration.  Until it exists, do not render fake macOS window controls.

## 5. Review conclusion

The implementation should begin with a bounded XHS Issue covering a new route-scoped
shell, Calendar/Note projection, and the first legal content handoff/decision/result
chain.  It must not begin with Visual v4 copy/paste, a global TerraShell rewrite, or a
generic dashboard.

**XHS IMPLEMENTATION PLAN REVIEW REQUIRED**
