# XHS Implementation Plan v1

**Status:** Review  
**Date:** 2026-08-15  
**Precondition:** `XHS_IMPLEMENTATION_GAP_AUDIT.md` **and** `XHS_RUNTIME_ARCHITECTURE_REVIEW.md` are reviewed together with the Frozen Shell/Shared contract and Approved XHS Instance Spec.  
**Source:** Read-only audit of the current `frontend/` and Runtime Foundation against the authority files named above.  
**Non-goal:** This document authorizes no code by itself.  A bounded implementation Issue with Allowed Files and a Runtime Simulation plan is required before Phase 1.

## 1. First vertical slice

### User-visible path

```text
进入 XHS Workspace
→ Month Calendar（真实 ContentItem）
→ 选择 Note
→ Calendar → Note Split Working
→ Note 上的 Employee Presence
→ 打开选题库 / 信号 Context 与图文预览 Utility
→ 有真实完成事实后自动 Handoff 到审核
→ Needs CEO Decision Gate
→ CEO 批准 / 退回 / 暂缓
→ 批准后 Publish Execution（working / completed / failed / waiting）
→ 有合法回执后进入发布结果
→ Published Result + System Activity（Analytics）
```

### Truth boundary for this slice

The slice is complete only when every object is persisted in an isolated SQLite
database, reload/restart returns the same selected Workspace/Note state, and the
decision/result chain is visible through the same Runtime projection.

- A trusted XHS Connector receipt may say **已发布 / 已验证**.
- A CEO manual receipt may say **已由 CEO 手动回填 / 未验证**.
- Without either receipt, the Note remains **等待发布结果**; no visual state may call
  it published.
- Analytics is a System Activity only after publication.  With no provider metrics it
  says **等待外部数据** and exposes the manual/connector return path; it never shows
  invented zero or growth values.
- “自动 Handoff” means Runtime reacts to a persisted execution-completion event.  It
  is not a hidden client click or a hard-coded demo transition.

## 2. Target state and module ownership

| Layer | Owns | First-slice module direction |
| --- | --- | --- |
| Root | theme, Runtime Company context, Global Assistant | Reuse existing providers. |
| Workspace shell | four independent panes, pane headers, T1/T2/T3, resizable surface, search, Utility maximize | New `WorkspacePaneShell`, mounted only by XHS. |
| XHS instance | calendar, note, split editing, signal context, preview utility, published/analytics views | New XHS components; no generic Workspace card layout. |
| Shared semantic view | Presence, System Activity, Handoff Event, Decision Banner, Result Reference | New reusable, data-driven components with no XHS layout assumptions. |
| Company OS Runtime composition | Work Context, Handoff, Decision Packet, Result Reference | Extend existing `WorkspaceRuntime` / Foundation entities and links; extract only the present RD-Cycle-specific writer path. |
| XHS domain Runtime | Note/version/review/publish/analytics facts | Extend `CONTENT_ITEM` / `CONTENT_VERSION` and existing receipt/interaction facts; do not add a second content system. |

## 3. Phase plan

### Phase 0 — Migration safety

| Item | Plan |
| --- | --- |
| Modify directories | `docs/04_Development/` only until implementation Issue is approved; then scoped `frontend/`, `backend/app/runtime/`, `backend/app/api/`, tests. |
| Modules | Create the formal `XHS-WORKSPACE-INSTANCE-001` Issue/Review and Runtime Simulation plan. Baseline a focused XHS fixture using a fresh isolated SQLite path. |
| Dependencies | Frozen Shell/Shared contract, Approved XHS spec, Authority Map, current Runtime Foundation tests. |
| Risk | Existing tree is dirty; generic XHS, RD and TTK share `WorkspaceRuntimeView`. |
| Acceptance | Allowed Files exclude RD/TTK routes and `TerraShell`; test DB is not `data/curis.sqlite`; no reference-only HTML/CSS/JS copied. |

### Phase 1 — Workspace shell

| Item | Plan |
| --- | --- |
| Modify directories | `frontend/app/ceo-office/workspace/xhs/`, `frontend/components/workspace/`, `frontend/components/terra/` only for icon/nav-data reuse; `frontend/lib/` for pane preference/search client. |
| New/modified modules | `WorkspacePaneShell`, PaneHeader, `useWorkspacePaneState`, ResizeHandle, CompanyObjectSearchSurface, UtilityMaximizeOverlay, XHS route boundary. |
| Dependencies | Root `RuntimeProvider`, existing token classes and `TerraIcon`; a small scoped search API is required before Search is marked functional. |
| Risk | Copying `TerraShell` behavior would retain the forbidden global topbar; a global navigation rewrite would break RD/TTK. |
| Acceptance | XHS alone has independent top-aligned Pane Headers; T1/T2/T3 meet the transfer/reachability contract; panes are isolated by Workspace ID; Context/Utility default closed; widths persist per Workspace and become overlay/focus before Main is unusable; `Esc` exits search/maximize; no fake traffic lights. |

### Phase 2 — XHS Calendar and Note

| Item | Plan |
| --- | --- |
| Modify directories | `frontend/components/xhs/`, XHS route, `frontend/lib/runtimeApi.js`; `backend/app/runtime/workspace.py`, `backend/app/api/runtime_foundation_router.py`; focused XHS Runtime/frontend tests. |
| New/modified modules | `XhsCalendar`, `XhsCalendarDay`, `XhsNoteSplit`, `XhsNoteEditor`, `XhsSignalContext`, `XhsPreviewUtility`; create/update Note and version commands/projection. |
| Dependencies | Content-item scoped persistence, title/body/tags/cover/scheduled date data, URL `note_id` selection. |
| Risk | The current initial ContentItem is `IDEA` but version creation accepts only `DRAFT`; do not hide this with frontend state. |
| Acceptance | Month view obeys 0/1/2–3/4+ and P0–P4 primary choice; selecting a persisted Note opens Split Working and survives reload; editing creates a legal new version without overwriting a submitted/published version; empty Context/preview reports missing source rather than inventing content. |

### Phase 3 — Shared Runtime semantics

| Item | Plan |
| --- | --- |
| Modify directories | `frontend/components/workspace/`, `frontend/components/xhs/`, `backend/app/runtime/workspace.py`, Foundation router/projection, focused tests. |
| New/modified modules | `EmployeePresence`, `SystemActivity`, `HandoffEvent`, `ResultReference`; one validated subject Work Context projection. |
| Dependencies | Real Workspace `AI_EMPLOYEE` entities and content-stage fields; current executor mapping; completion evidence. |
| Risk | Treating `owner_ref`, the last actor, or an Analytics process as employee presence violates the Frozen distinction. |
| Acceptance | A Note shows stable Object Owner separately from Current Responsibility/Executor; employee presence has a real employee reference; post-publication analytics has no avatar; handoff is a persisted event and not a CEO button. |

### Phase 4 — Decision and Handoff

| Item | Plan |
| --- | --- |
| Modify directories | Same XHS Runtime boundary plus `frontend/lib/runtimeApi.js`, XHS view/components and tests. |
| New/modified modules | Content review submission; a subject-scoped completion callback/Handoff helper; `XhsDecisionBanner`; approve/return/defer commands and recovery projection. |
| Dependencies | Legal content lifecycle state machine, Evidence linking, existing `HANDOFF` and `DECISION_PACKET` persistence, and the reviewed Shared Runtime helper. |
| Risk | Reusing RD `OperatingCycleControl` would force wrong terminology/states; letting the client decide state would bypass audit/retry rules. |
| Acceptance | A completed creator execution automatically creates its Handoff; the Note remains legally `IN_REVIEW` while the linked Decision Packet produces `Needs CEO`; CEO approval/return/defer writes a packet and changes only permitted Note context/state; failure retains owner, reason, return stage and retry boundary. |

### Phase 5 — Published and Analytics

| Item | Plan |
| --- | --- |
| Modify directories | XHS Runtime projection/API and XHS result components; focused tests. |
| New/modified modules | `XhsPublishedResult`, `XhsAnalyticsActivity`, manual receipt/metrics entry and connector-result adapter boundary. |
| Dependencies | Approved content version, receipt source, Result reference, capability/connector status. |
| Risk | Content publication without a trusted receipt must not be rendered as external success; Analytics cannot create an invented analyst employee. |
| Acceptance | Trusted receipt → verified Published Result; CEO manual receipt → visible unverified manual fact; absent receipt → waiting state; Analytics uses System Activity and only shows received values/sources/timestamps. |

### Phase 6 — Acceptance

| Item | Plan |
| --- | --- |
| Modify directories | Focused frontend/backend tests, Issue Review, evidence location only. |
| Modules | Isolated SQLite scenario, browser/packaged Desktop validation, restart/recovery check. |
| Dependencies | Phases 1–5; current Desktop launch procedure; current Company/CEO identity. |
| Risk | Static UI, mock Calendar cards, old browser screenshots, or SQL seeds could falsely appear to prove the chain. |
| Acceptance | Fresh isolated Company/XHS Workspace; persisted Note; Calendar→Split→Context/Utility; real employee/handoff/decision records; manual or trusted result truthful; System Activity/Analytics state; failure/recovery; reload/restart; scoped no-regression RD/TTK route check; Review conclusion backed by a full Runtime Simulation. |

## 4. Required Runtime contract before Phase 2/4

The implementation Issue must name the exact transitions, actors, inputs, outputs and
recovery rules.  The intended minimum contract is:

| State | Actor | Input / output | Next state | Truth rule |
| --- | --- | --- | --- | --- |
| `DRAFT` | Creator employee | editable Note / immutable candidate version | `IN_REVIEW` | Submission must identify the version and evidence. |
| `IN_REVIEW` | System | persisted creator-completion event | reviewer responsibility + linked `HANDOFF` | No CEO click advances it. |
| `IN_REVIEW` + `DECISION_PACKET=WAITING_CEO` | Reviewer employee | review evidence + risk summary | **Needs CEO** surface | CEO is never current executor; Needs CEO is derived, not a new global state. |
| `APPROVED` | CEO decision | approve/return/defer `DECISION_PACKET` | `SCHEDULED` or returned Draft | Decision is separate from Handoff. |
| `SCHEDULED` | Publish Execution | `working` / `waiting` / `failed` / `completed`, plus trusted connector result or explicit CEO manual receipt | `PUBLISHED` only with a legal receipt; otherwise remains scheduled with a recoverable execution fact | Execution state is not a ContentItem lifecycle state. Connector health gap remains visible. |
| `PUBLISHED` | System | receipt | `AWAITING_FEEDBACK` | CEO manual source stays unverified. |
| `AWAITING_FEEDBACK` | Analytics System Activity | `waiting` / `running` / `ready` / `failed`; external metrics or manual observation | `REVIEWED` only through the legal domain review action | Activity is not an employee and does not create a ContentItem analytics state. |

`HANDOFF`, `EVIDENCE`, `DECISION_PACKET`, receipt and interaction links must share the
same Company/Workspace/ContentItem. A Task/Agent execution remains a child reference,
not a Note state. A failed execution must preserve its return stage, responsible
employee/system, reason, retry count/boundary and recovery action.

The implementation must preserve this separation throughout the UI and API:

```text
Business Object State ≠ Current Responsibility ≠ Current Executor ≠ System Activity State
```

## 5. Proposed implementation Issue boundaries

The formal issue should use these **candidate** Allowed Files, then shrink them if an
existing component covers a listed behavior:

```text
frontend/app/ceo-office/workspace/xhs/page.js
frontend/components/workspace/**
frontend/components/xhs/**
frontend/lib/runtimeApi.js
frontend/tests/xhs_*.test.mjs
backend/app/runtime/workspace.py
backend/app/api/runtime_foundation_router.py
backend/tests/test_xhs_*.py
docs/04_Development/XHS_IMPLEMENTATION_*.md
issues/<new-xhs-issue>.md
docs/reviews/<new-xhs-review>.md
```

Explicit exclusions:

```text
frontend/components/terra/TerraShell.js
frontend/components/runtime/WorkspaceRuntimeView.js (RD/TTK behavior)
frontend/app/ceo-office/workspace/software/**
frontend/app/ceo-office/workspace/shortvideo/**
docs/01_Product/Curis_Product_Blueprint.html
docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md
docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md
curis-ui-prototype/**
data/curis.sqlite
```

An exception to alter a shared component, schema, or another Workspace must be handled
as a separate shared-Runtime or product decision, not folded into the XHS UI Issue.

## 6. Focused acceptance scenarios

1. **Empty truthful office:** XHS Workspace has no Notes; Calendar is empty, Context
   explains no signal source is bound, no sample card/result/employee appears.
2. **Calendar density:** persisted Notes on one day obey the primary selection priority
   and `+N` collapse; a Needs CEO Note outranks the previously selected Note.
3. **Responsibility:** selected Note has real creator Presence, then a persisted Handoff
   to reviewer; Owner remains the Workspace.
4. **Decision:** reviewer creates `Needs CEO`; CEO approves, returns, and defers on
   separate isolated runs; no CEO “next step” appears.
5. **Result truth:** CEO manual receipt appears as unverified; connector-unavailable
   state remains blocked/waiting; Analytics shows only provenance-backed values.
6. **Recovery:** failed creator/publish execution retains the same Note, owner, reason,
   return stage and retry boundary; recovery does not spawn a fake replacement Note.
7. **Persistence/isolation:** restart retains Company/Workspace/Note/Decision/Handoff;
   cross-Workspace or cross-Company URL access is rejected.

## 7. Review gate

No Phase is product acceptance by itself.  The XHS instance is ready for Review only
after Phase 6 demonstrates the complete first-slice Runtime Simulation and the desktop
surface is backed by that same isolated database.

**XHS IMPLEMENTATION PLAN REVIEW REQUIRED**
