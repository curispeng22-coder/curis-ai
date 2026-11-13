# Review 077: Workspace Company Department Catalog Summary

Date: 2026-07-08
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/080_workspace_company_department_catalog_summary_gate.md`
Status: READY_FOR_QUALITY_RECHECK

## Product Progress

Curis Workspace can now show a read-only official department catalog summary inside the company workspace frame, making the future company foundation visible without enabling department CRUD, employee management, organization routing, or runtime behavior changes.

## Scope

- Frontend-only implementation under `frontend/app`.
- Uses existing `GET /api/catalog/department-types` only.
- Adds a `部门目录` summary inside the existing `公司工作区` frame.
- Shows active official department type count, category summary, and non-secret department type labels.
- Adds loading, error, and empty states.
- Preserves Task API payload shape `{ content }`.
- Does not add backend/API/schema/persistence changes, new department APIs, department CRUD, department instances, department workflow routing, Employee CRUD, Admin Platform implementation, billing/ROI/packages/marketplace, business modules, secrets, or runtime behavior changes.

## Changed Files

- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `issues/080_workspace_company_department_catalog_summary_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/077_workspace_company_department_catalog_summary_review.md`

## Verification

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 18
pass 18
fail 0
```

```text
cd frontend && npm run lint
```

Result:

```text
eslint .
```

Exit code: 0.

```text
cd frontend && npm run build
```

Result:

```text
Compiled successfully
Route (app)
┌ ○ /
├ ○ /_not-found
└ ○ /platform
```

Exit code: 0.

```text
git diff --check -- issues/080_workspace_company_department_catalog_summary_gate.md reviews/077_workspace_company_department_catalog_summary_review.md TASKS.md PROJECT_STATUS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: passed.

API usage scan:

```text
rg -n "/api/(catalog/department-types|workspace/model-preference|task|tasks|task/)|fetch\\(|buildTaskPayload|buildDepartmentCatalogSummaryViewModel" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: the only new department-related API usage is existing `GET /api/catalog/department-types`.

Forbidden-scope scan:

```text
rg -n "billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex organization|business modules|secret|credential|provider SDK|direct provider|New API internal|department CRUD|workflow routing|Project Memory write|task_type|role_id|entry_kind" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: no production implementation drift. Expected matches are limited to existing negative tests for forbidden payload fields and secret-like metadata redaction.

## Quality Result

Quality Result: PASS.

Commands: frontend view-model tests, frontend lint, frontend build, whitespace check, API usage scan, Task API payload check, and forbidden-scope scan.

Evidence: department summary code filters active `source=official` department types, renders only type key, display label, and category label, and excludes tenant-private, disabled, and secret-like fields from the view model.

Risks: Browser runtime screenshot evidence was not captured for this implementation pass. Existing unrelated dirty backend files are present in the worktree and were not part of this issue.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close the frontend-only department catalog summary slice and continue to the next bounded Workspace Company Foundation step.

Scope: Accept the frontend-only read-only department catalog summary in the existing company frame.

Acceptance Criteria:

- Approved Option A scope is preserved.
- Existing `GET /api/catalog/department-types` is the only new department-related read used by the frontend.
- No backend/API/schema/persistence changes were made for this slice.
- No department CRUD, department instance creation, workflow routing, Employee CRUD, Admin Platform implementation, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, or runtime behavior changes were introduced.
- Verification passed with 18 frontend tests, lint, build, API scan, and forbidden-scope scan.

Source Of Truth Updates: `issues/080_workspace_company_department_catalog_summary_gate.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark the department catalog summary accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout

## Quality Scope Recheck

Quality Result: BLOCKED_BY_SCOPE_DRIFT.

Commands:

```text
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
git diff --check -- issues/079_workspace_company_foundation_local_demo_evidence_gate.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
git diff --name-only -- frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs issues/080_workspace_company_department_catalog_summary_gate.md reviews/077_workspace_company_department_catalog_summary_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md backend/app backend/tests
rg -n "/api/(catalog/department-types|workspace/departments/activation|workspace/model-preference|task|tasks|task/)|fetch\(|buildTaskPayload|buildDepartmentCatalogSummaryViewModel|buildDepartmentActivation" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
rg -n "billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex organization|business modules|secret|credential|provider SDK|direct provider|New API internal|department CRUD|workflow routing|Project Memory write|task_type|role_id|entry_kind" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
git diff --name-only -- backend/app backend/tests admin-platform shared deploy tools data workspace
```

Evidence:

- Fresh frontend verification passed in the current worktree: 21 frontend tests, lint, and build.
- Issue-080 allowed API is `GET /api/catalog/department-types`.
- Current dirty frontend files also contain later department activation scope: imports and calls for `buildDepartmentActivationPayload`, `buildDepartmentActivationViewModel`, `GET /api/workspace/departments/activation`, and `PUT /api/workspace/departments/activation`.
- Current dirty worktree also contains backend/runtime dirty files, including `backend/app/database.py`, `backend/app/main.py`, and `backend/tests/test_execution_engine.py`, plus untracked activation files.
- Therefore the current worktree cannot be used as clean issue-080 evidence without mixing later activation work into this issue.

Risks:

- Accepting issue-080 from the current dirty worktree would blur the approved frontend-only department catalog summary boundary with later activation API/backend work.
- The department catalog summary itself is still supported by tests/build, but the quality evidence must be re-cut from an issue-080 scoped diff or commit that excludes activation changes.

Blocked / Pass: Blocked for scope split; no product/runtime fix was made by 质量运行席.

Next Seat: 系统交付席.

Handoff: sent to 系统交付席

## Scope Split Resolution

Resolution Result: PASS.

Reason: the later department activation backend/UI work is now tracked and accepted under separate issues:

- `issues/083_workspace_department_activation_first_slice.md`
- `issues/084_workspace_department_activation_ui_gate.md`
- `reviews/080_workspace_department_activation_first_slice_review.md`
- `reviews/081_workspace_department_activation_ui_review.md`

Issue-080 remains scoped to the read-only `部门目录` summary using existing `GET /api/catalog/department-types` only. Current worktree-wide frontend files now include later accepted activation code, so current full-file scans must not be used as issue-080-only evidence. Issue-080 evidence is bounded to the original department catalog summary verification above plus browser-visible evidence in `reviews/078_workspace_department_catalog_local_demo_evidence_review.md`.

Scoped issue-080 evidence:

- `buildDepartmentCatalogSummaryViewModel` filters active `source=official` department types.
- The department catalog summary renders only label, category, and type key.
- Tenant-private, disabled, and secret-like metadata are excluded by tests.
- Browser evidence in `reviews/078_workspace_department_catalog_local_demo_evidence.png` confirms the `部门目录` summary renders in local/demo runtime.

Current-state correction:

- The scope drift blocker is resolved by assigning activation behavior to accepted issues 083/084 instead of issue 080.
- T-217 can be closed as evidence split completed.
- No product/runtime behavior change was made by this scope-resolution note.

Handoff: final closeout

## System Delivery Scoped Evidence

Delivery Result: READY_FOR_QUALITY_RECHECK.

Scope action:

- Removed later department activation frontend drift from the issue-080 scoped files.
- Issue-080 frontend code now uses only existing `GET /api/catalog/department-types` as the department-related API.
- Later activation backend/runtime files remain dirty or untracked in the broader worktree and are not part of the issue-080 scoped evidence.

Fresh scoped verification:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 18
pass 18
fail 0
```

```text
cd frontend && npm run lint
```

Result:

```text
eslint .
```

Exit code: 0.

```text
cd frontend && npm run build
```

Result:

```text
Compiled successfully
Route (app)
┌ ○ /
├ ○ /_not-found
└ ○ /platform
```

Exit code: 0.

API usage scan:

```text
rg -n "/api/(catalog/department-types|workspace/departments/activation|workspace/model-preference|task|tasks|task/)|fetch\\(|buildTaskPayload|buildDepartmentCatalogSummaryViewModel|buildDepartmentActivation" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: no `/api/workspace/departments/activation` or `buildDepartmentActivation*` matches; the only department-related API usage is `/api/catalog/department-types`.

Forbidden-scope scan:

```text
rg -n "billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex organization|business modules|secret|credential|provider SDK|direct provider|New API internal|department CRUD|workflow routing|Project Memory write|task_type|role_id|entry_kind|/api/workspace/departments/activation|activation" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: no production implementation drift; expected matches are limited to existing negative tests for forbidden payload fields and secret-like metadata redaction.

Next Seat: 质量运行席.

Handoff: sent to 质量运行席
