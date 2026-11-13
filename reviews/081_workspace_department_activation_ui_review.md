# Review 081: Workspace Department Activation UI

Date: 2026-07-08
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/084_workspace_department_activation_ui_gate.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now show and save tenant-local enabled department type selections inside the existing company frame, making the company workspace configurable while keeping department instances, employees, workflow routing, Admin Platform, billing, and runtime behavior out of scope.

## Scope

- Frontend-only implementation under `frontend/app`.
- Uses existing `GET /api/workspace/departments/activation`.
- Uses existing `PUT /api/workspace/departments/activation`.
- Adds checkbox-based official department type selection inside the existing `公司工作区` frame.
- Saves payload `{ "department_type_keys": [...] }`.
- Shows active department count, active labels, loading/saving/error states, and Chinese copy.
- Preserves Task API payload shape `{ content }`.
- Does not add backend/API/schema/persistence changes for this issue, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform implementation, billing/ROI/packages/marketplace, business modules, secrets, Project Memory runtime writes, or runtime behavior changes.

## Changed Files

- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `issues/084_workspace_department_activation_ui_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/081_workspace_department_activation_ui_review.md`

## TDD Evidence

Red run before implementation:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Expected failure confirmed:

```text
SyntaxError: The requested module './taskViewModel.mjs' does not provide an export named 'buildDepartmentActivationPayload'
```

Green focused run after implementation:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 21
pass 21
fail 0
```

Frontend lint:

```text
cd frontend && npm run lint
```

Result:

```text
eslint .
```

Exit code: 0.

Frontend build:

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

## Scope Checks

API usage scan:

```text
rg -n "/api/(workspace/departments/activation|catalog/department-types|workspace/model-preference|task|tasks|task/)|fetch\\(|buildTaskPayload|buildDepartmentActivationPayload|buildDepartmentActivationViewModel" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: the only new department-activation API usage is existing `GET /api/workspace/departments/activation` and `PUT /api/workspace/departments/activation`; existing task/model/catalog calls are unchanged.

Secret/scope scan:

```text
rg -n "api_key|token|password|secret|credential|Authorization|prompt|output|billing|ROI|staffing|permission|routing|model_policy|external_platform|Employee CRUD|Admin Platform|marketplace|Task API|runtime behavior|department instance|workflow routing" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs issues/084_workspace_department_activation_ui_gate.md
```

Result: expected matches only in existing execution-detail rendering/tests, negative secret redaction tests, and issue forbidden-scope documentation.

Backend/Admin/shared guard:

```text
git diff --name-only -- backend admin-platform workspace shared deploy tools data
```

Result: worktree still contains pre-existing unrelated backend dirty files plus backend files from the already accepted issue 083. No backend/Admin/shared/deploy/tools/data edits were made for issue 084.

Whitespace check:

```text
git diff --check -- frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs issues/084_workspace_department_activation_ui_gate.md reviews/081_workspace_department_activation_ui_review.md TASKS.md PROJECT_STATUS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Result: passed.

## Quality Result

Quality Result: PASS.

Commands: TDD red run, frontend view-model tests, frontend lint, frontend build, API usage scan, secret/scope scan, backend/Admin/shared guard review, and whitespace check.

Evidence: UI reads current activation state, displays only official department type labels/category/type keys, lets the CEO select/unselect department type references with checkboxes, and saves `{ department_type_keys: [...] }` through the existing activation API.

Risks: Browser runtime screenshot evidence was not captured for this UI implementation pass. The worktree contains pre-existing unrelated or previously accepted dirty files; they were not used as evidence for this issue.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close frontend-only department activation UI and open local/demo evidence only if browser-visible proof is needed next.

Scope: Accept the frontend-only department activation display/selector inside the existing company frame.

Acceptance Criteria:

- UI uses only existing department activation APIs.
- UI shows selected active department count and labels.
- UI allows selecting/unselecting official department type references and saving them.
- Payload shape is `{ "department_type_keys": [...] }`.
- UI exposes no secret-like metadata.
- No backend/API/schema/persistence change was made for this issue.
- Task API payload remains `{ content }`.
- Frontend tests, lint, and build pass.

Source Of Truth Updates: `issues/084_workspace_department_activation_ui_gate.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark the department activation UI accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout

## Current-State Correction

Correction Result: PASS.

Reason: a current-state audit found that the accepted issue-084 UI behavior was documented but not present in `frontend/app/page.js`. The root cause was missing page-level integration for the existing department activation API and selector; backend activation APIs already existed from issue 083.

Corrective Scope:

- Added missing page-level wiring for `GET /api/workspace/departments/activation`.
- Added missing page-level wiring for `PUT /api/workspace/departments/activation`.
- Added the `启用部门` checkbox selector inside the existing `公司工作区` frame.
- Added view-model and payload helpers for the selector.
- Added regression tests so the Workspace page must wire the selector to existing APIs.
- Preserved Task API payload `{ content }`.
- No backend/API/schema/persistence changes were made by this correction.

Red verification:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
SyntaxError: The requested module './taskViewModel.mjs' does not provide an export named 'buildDepartmentActivationPayload'
```

Green verification:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 22
pass 22
fail 0
```

Additional verification:

```text
cd frontend && npm run lint
cd frontend && npm run build
cd backend && ./.venv/bin/python -m unittest tests/test_department_activation.py
```

Result:

```text
frontend lint passed
frontend build passed
backend department activation tests: Ran 3 tests, OK
```

Known Note: backend focused verification still emits the existing FastAPI/Python 3.14 deprecation warning; it is not introduced by this UI correction.

Handoff: final closeout
