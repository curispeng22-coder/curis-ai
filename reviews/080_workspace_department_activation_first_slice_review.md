# Review 080: Workspace Department Activation First Slice

Date: 2026-07-08
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/083_workspace_department_activation_first_slice.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now store tenant-local active department type selections as backend metadata, moving the company frame from read-only department visibility toward CEO-configurable structure without enabling department CRUD, employees, workflow routing, Admin Platform, billing, or runtime behavior changes.

## Scope

- Backend-only first slice.
- Adds tenant-local department activation metadata over active official department type metadata.
- Adds `GET /api/workspace/departments/activation`.
- Adds `PUT /api/workspace/departments/activation` with payload `{ "department_type_keys": [...] }`.
- Validates requested department type keys against active official department type metadata.
- Returns a non-secret read model with active keys and department type options.
- Preserves Task API payload shape `{ content }`.
- Does not add frontend UI selector, Admin Platform implementation, new official department type supply, department instances, workflow routing, Employee CRUD, billing/ROI/packages/marketplace, business modules, secrets, Project Memory runtime writes, or runtime behavior changes.

## Changed Files

- `backend/app/database.py`
- `backend/app/department_activation.py`
- `backend/app/main.py`
- `backend/tests/test_department_activation.py`
- `issues/083_workspace_department_activation_first_slice.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/080_workspace_department_activation_first_slice_review.md`

## TDD Evidence

Red run before implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_department_activation.py
```

Expected failure confirmed:

```text
FAILED (failures=3)
AssertionError: 404 != 200
AssertionError: 404 != 422
```

Green focused run after implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_department_activation.py
```

Result:

```text
Ran 3 tests in 0.097s
OK
```

Backend regression:

```text
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 255 tests in 6.496s
OK
```

Known warning:

```text
fastapi/routing.py:234: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated
```

This is the existing Python 3.14 FastAPI warning and remains a known non-blocking gap.

## Scope Checks

Secret/scope scan:

```text
rg -n "api_key|token|password|secret|credential|Authorization|prompt|output|billing|ROI|staffing|permission|routing|model_policy|external_platform|Employee CRUD|Admin Platform|marketplace|Task API|runtime behavior" backend/app/department_activation.py backend/tests/test_department_activation.py issues/083_workspace_department_activation_first_slice.md
```

Result: expected matches only in negative test strings, redaction error text, and issue forbidden-scope documentation.

Frontend/Admin/shared guard:

```text
git diff --name-only -- frontend admin-platform workspace shared deploy tools data
```

Result: pre-existing dirty frontend files from the accepted department summary slice are still present in the worktree. No new frontend, Admin Platform, shared, deploy, tools, or data edits were made for issue 083.

Whitespace check:

```text
git diff --check -- backend/app/database.py backend/app/department_activation.py backend/app/main.py backend/tests/test_department_activation.py issues/083_workspace_department_activation_first_slice.md reviews/080_workspace_department_activation_first_slice_review.md TASKS.md PROJECT_STATUS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Result: passed.

## Quality Result

Quality Result: PASS.

Commands: TDD red run, focused backend test, full backend regression, secret/scope scan, frontend/Admin/shared guard review, and whitespace check.

Evidence: `TenantDepartmentActivation` stores only tenant id, official department type key, source, enabled state, display order, and timestamp. API reads/writes are tenant-scoped, validate against active official department type metadata, and return only non-secret catalog labels plus tenant-local enabled state.

Risks: The worktree contains pre-existing unrelated or previously accepted dirty files, including frontend files from the department summary slice and unrelated backend files. They were not used as evidence for this issue. Future UI selector still needs a separate gate.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close backend-only department activation metadata and decide whether to open a frontend selector/display gate next.

Scope: Accept the backend-only tenant-local department activation first slice.

Acceptance Criteria:

- `GET /api/workspace/departments/activation` returns tenant-local activation state and active official department options.
- `PUT /api/workspace/departments/activation` accepts `{ "department_type_keys": [...] }`.
- Unknown, inactive, and non-official department type keys are rejected.
- Reads/writes are tenant-scoped.
- Persistence is metadata-only and has no secret, prompt, output, credential, billing, ROI, staffing, permission, routing, model-policy, or external-platform fields.
- API response exposes only non-secret official department metadata and tenant-local enabled state.
- Focused backend tests and full backend regression pass.
- No frontend selector, Admin Platform implementation, department instance, workflow routing, Employee CRUD, billing, business-module, secret, Task API, Project Memory runtime write, or runtime behavior change is approved.

Source Of Truth Updates: `issues/083_workspace_department_activation_first_slice.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark the department activation first slice accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout
