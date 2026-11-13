# Curis Phase B P0 Core Product Reconciliation

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: IMPLEMENTED / ACCEPTED CANDIDATE — pending CEO / ChatGPT review
Owner: Main Development / Integration
Source: CEO Phase B P0 implementation authorization, 2026-09-09; `docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md` and `docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md`.

## Goal / slices

Final integration complete: see `docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md` current section for five Slice results, seven-Employee truth map, spatial/Assistant maps, fresh normal-entry Company and Business creation, native/Browser interactions, same-root restart and exact protected fingerprints. Unified Scope dependency passed; old Department-only gate and checkpoints below are historical. Backend 120 PASS, Scope 40 PASS, bootstrap 4 PASS, frontend 19 PASS, lint/compile/build/fresh package/diff checks PASS. FINAL UI MASTER READY TO RESUME, not implemented here; RELEASE BLOCKED. No stage/commit/push or next initiative.

2026-09-09 CEO correction: the historical Department gate below is superseded by authorized COMPANY / DEPARTMENT / BUSINESS / WORKSPACE reconciliation, not a Department-specific extension. Dependency: CURIS-CANONICAL-EXECUTION-SCOPE-RECONCILIATION-001.md. Existing Phase B work was preserved and remaining slices resumed after the unified execution/context/usage proof passed.

A: atomic fresh Company built-in organization; B: canonical responsibility and work-surface projection; C: canonical business activation; D: reuse shared four-pane behavior; E: same global floating CEO Assistant and durable conversation. The final Browser / fresh packaged Desktop / restart evidence now passes the bounded P0 gates; release remains blocked.

## Preflight

HEAD: `bb72916daba3ae9555914d03bdb7fcea9953ab9c`. Staged: 0. Working tree: 125 modified, 2 deleted, 611 untracked. All pre-existing content preserved; no staging, commit, push, reset, clean or stash.

|Protected DB|Size|mtime_ns|SHA-256|integrity_check|
|---|---:|---:|---|---|
|data/curis.sqlite|1232896|1786873339955841838|2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6|ok|
|backend/data/curis.sqlite|1277952|1786783659967572836|a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4|ok|
|/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite|1536000|1788614881473263746|d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617|ok|

Checks use read-only immutable SQLite connections, never production imports. Runtime tests must set CURIS_DB / CURIS_DB_PATH / CURIS_WORKSPACE_DB to the same repository-external database before collection/import. No default App launch.

## Slice A exact Allowed Files / semantic ownership

|Path|Owned functions/hunks|Pre-change SHA-256|
|---|---|---|
|backend/app/runtime/foundation.py|Only fresh Company `_materialize_company_in_connection` integration; preserve accepted FirstRun transaction/retry logic|465d2f6adc9f6979cf2ca6c51c0295e4359a0f829ad71489ceb17b7b4421c72d|
|backend/app/employee_templates.py|Bounded built-in catalog/instance materialization helper; preserve existing recruitment/avatar/edit methods|2a7fedae11f16cfe2ed1bbc145a497d6555fec7bb64067020935b5d604a9d89c|
|backend/tests/test_phase_b_builtin_organization.py|New isolated focused test only|NEW|
|issues/CURIS-PHASE-B-P0-CORE-PRODUCT-RECONCILIATION-001.md|This Issue|NEW|
|docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md|Local/final evidence, no unsupported acceptance|NEW|

Foundation's pre-existing connection-aware Company transaction is accepted First Run integration (CURIS_V1_UI_INDEPENDENT_DELIVERY_REPORT); it is retained, not replaced. EmployeeTemplateContract's pre-existing avatar/recruitment work is retained. This issue owns only added bootstrap integration and helper, not whole files. Later slices require exact paths, owned hunks and hashes before edits; candidate scope is not implicit authorization to overwrite.

## Reuse findings / remaining audit

### Slice A regression adjustment / Slice B owned read seams

Before edits, add these exact files; no whole-file replacement:

- `backend/tests/test_v1_first_run_delivery.py`: only expected Department count in successful fresh creation (two built-in plus one requested business department); SHA `78905631f8cce6a01a0e96466dcc84fe8e9a7a485c02306c09051cd07aa4f29e`.
- `backend/app/organization_projection.py`: department-scoped assignment read projection only; SHA `5a8328061406b57b88207a14e201543fb04f8b95041f1d42a438648d18e65665`.
- `backend/app/operating_intelligence.py`: replace analyst role-text selection with canonical responsibility resolution only; SHA `29d16c6ea34cff2d2138e642c97d005b053fccf6915a64275fb0eddd93c12dc2`.
- New focused assertions remain in `backend/tests/test_phase_b_builtin_organization.py`.

Existing Organization and Operating Intelligence accepted projections remain the owners; changes extend their real-data reads, not a new organization or analyst store. Frontend Slice B exact registration follows its consumer audit.

Slice B frontend additions: `frontend/lib/organizationProjection.js` (SHA `2ef05384503c6148ab46a13fad13d738d58754a35fdf35a08b2c0b71c6032741`) only departmentAssignment-to-employee/department projection; `frontend/app/ceo-office/organization/OrganizationCenter.js` (SHA `8fc8161519c577c90edd5215baecc4592503a40b17a147bb93cf5c82c03d592e`) only consume those relations and show shared Employee links under departments without businesses. Existing Business Focus/Directory/Avatar ownership preserved. New focused frontend check: `frontend/tests/phaseBBuiltinOrganization.test.mjs`.

Slice A/B backend checkpoint: 15 passed (bootstrap, foundation persistence, First Run, Organization and Operating Intelligence), external DB only. This is not Browser/Desktop acceptance.

### Slice C exact frontend seams

- `frontend/components/v1/CeoDeskOperating.js`, SHA `23176a033c38b36b4defc7c71038aba8c697b7d1dcf5b5fd4086f248737bcd5e`: export/reuse existing CreateBusiness, preserve origin path during proposal save. No second creator.
- `frontend/app/ceo-office/business/page.js`, SHA `9090b22aca71d9996831728213d67979db8544e376b502d3d5ee0796462b1987`: empty/new business entry and existing canonical department Leader link; Studio parent reference.
- `frontend/app/ceo-office/workspace/studio/page.js`, SHA `346316e63e017e42d9696fb2ca0e00fff2db9f2307934b048ef5e3462962e7e1`: load/select canonical Business and pass its ID, no synthetic ref. Legacy template content retained as compatibility, not new authority.

Existing direct creation uses FirstRunDelivery's accepted canonical atomic seam. Department Work execution remains separately audited; an Employee Conversation entry alone does not prove delegated Work execution.

### Slice D exact owned seams

|File|Pre-change SHA-256|Owned semantic block|
|---|---|---|
|frontend/components/terra/TerraShell.js|c8bf027c3a0f6205ddcee1feee14ea8a351efb2a19a3f4ea015beb74fab1b804|Reuse WorkspacePaneShell for layout; preserve theme, return routing and Assistant context; bounded UI-only content slot|
|frontend/components/workspace/WorkspacePaneShell.js|a6bf75a84d2af6fc578126774ccfd9a87ebdfca3afe52f76d09b717222bccd46|Shared Navigation consumer and header slot only; existing pane behavior retained|
|frontend/components/v1/V1Sidebar.js|0f94c100b3e14f980cc3997bdd8bad2887bd30798ef95e0121aad1daba1214d5|Embedded navigation layout only; seven-area list/Conversation truth retained|
|frontend/components/v1/GeneralWorkspaceOperating.js|a62e1b43edcdb892cf0ceaca8fbedc268beb111822d8c393fe37624ec17201ae|Fixed aside becomes Main readiness/team plus optional Result Utility and bounded Work Context; no execution handlers changed|

No new Shell or Runtime state. UI-only slots cannot write Work/Result/Decision. Professional domain Main stays unchanged.

Existing employee_templates, department_templates, department_types, employee_instances and runtime_entities support definitions/instances without new tables. Existing RESPONSIBILITY_ASSIGNMENT supports DEPARTMENT scope and holder replacement. Company transaction already serializes and atomically materializes Company/Assistant; original completion must remain distinct from later organizational edits. No Provider binding may be synthesized.

Canonical Child Work currently requires Workspace-scoped Cycle/Assignment. A Department Assignment alone is not proof of executable canonical Work. Verify the existing delegation/activation path before wiring Slice B/C; never use a generic runtime record or Conversation text as fake Work.

## Acceptance / stop conditions

### Slice E owned integration (after four-scope execution proof)

Slice B/C delegation input: backend/app/api/team_operating_router.py only an Assignment-scoped create Cycle/Work endpoint reusing CanonicalChildWorkRuntime (pre-SHA 525cd7cf2c7294147e35e658aabd23a5871f80c97a0d018cb2a3326ac83d4718); frontend/lib/v1FrontendApi.js only that endpoint client (pre-SHA 99df38524cb3976a0e816d2a201e7d930cd30d85b8a6f05be7352194c571ae4f). Existing CreateBusiness and Business page owned seams add explicit delegation of the same captured intent, not another Business creator or automatic provider launch. Focused proof remains test_phase_b_builtin_organization.py.

`frontend/components/assistant/GlobalAssistant.js`, pre-SHA 48bf15a76906604d8ff2b1eefb14ae44123da71318536a7068ccef6c63132eba: only persistent overlay host drag/collapse and existing CEO Assistant conversation/API/SharedConversation integration. Existing root Provider remains mounted across navigation; no second message persistence or Assistant identity. Existing attention projection remains canonical. New focused frontend checks in frontend/tests/phaseBSpatialAssistant.test.mjs. Position state is UI-only and need not survive restart; messages must come from the existing durable holder.

Governance-only allowed append/prepend at stop (no Accepted registration): CURRENT_STATE SHA `0d572736f088fde89724194374be894e58e28d2ac6882a17dcebd86c54c41a4b`; PRODUCT_DOCUMENT_POINTER SHA `b87b2a6b32fe642b29309d64329be07faa9bacfa6c8d86d2d1e41db35a4a538f`; Product Completion Reconciliation SHA `392e3a6e42d06c04e233afa16b625c6522374e4fd789914ab836889fa8d08ca5`; Execution Backlog SHA `9dd4ce4108275e37aeacd991ac04e40adbddd59d637eda9944aab1a5ac9a6def`; CHANGE_LOG SHA `602b4a2d4e38ed3586d6336e82eafaed4e89e9963954ea68f0843deca41755c2`. Only a bounded progress/gate entry; historical and other initiative sections preserved.

Current stop evidence: `test_department_execution_scope_gate_is_not_model_configuration` proves the real Department Leader Assignment is rejected by Conversation context and canonical Work creation without a Workspace. General Workspace assignment also has a Company-scoped Employee identity compatibility gap (source audit). Do not weaken these checks or create a synthetic Business. See `docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md` for exact sources and next architecture decision.

Checkpoint: 16 backend tests + 1 new frontend projection test PASS; focused ESLint, Python compile and diff check PASS. Browser/package/full integration NOT RUN. Slice E not begun. No acceptance registration authorized by these partial checks.

A: Company 1, CEO 1, Assistant 1, departments 2, engineering Employees exactly 6, analyst >=1, user Business 0; no-key, failure atomicity, concurrent/retry/restart identity, user-edit preservation, no headcount repair on completed bootstrap.
B: genuine Department/Role/Responsibility/Assignment, canonical analyst resolution without role-text inference, shared Employee surfaces/edit, legitimate intent/Work seam.
C: generic canonical Business+first Workspace atomic activation, invalid parent rejected, no synthetic parent, direct/delegated same seam.
D: Nav+Main default, Context/Utility optional, actual pointer resize/toggle/maximize/recover without Runtime changes; preserve professional Main.
E: same Assistant/Conversation across seven areas, actual drag/collapse/expand, overlay not Pane, bounded authorized context, existing Usage ledger.
Final: focused and bounded regressions, Python compile, frontend lint/build, continuous Browser journey, fresh packaged normal-entry journey, full restart identity/count comparison, three protected DB fingerprints unchanged.

Stop for new primitive/schema, second truth, unsafe transaction, unresolved owned-hunk collision, Authority conflict or protected DB mutation. No rollback of preserved files or active database. Ordinary bugs do not constitute a gate. No Meeting re-opening, final UI redesign, default business, new provider capability, commit or push.
