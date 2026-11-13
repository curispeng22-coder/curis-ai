# Local/Demo API Smoke Helper Review

Date: 2026-07-07

Reviewer seat: 系统交付席

Source issue: `issues/040_local_demo_api_smoke_helper.md`

Helper artifact: `tools/local_demo_api_smoke.py`

Operator notes: `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`

## Delivery Status

Status: accepted by 产品规划席.

Delivery type: local-only tooling implementation plus documentation reference.

No backend/frontend behavior files were changed.

## Delivery Summary

Implemented a local/demo API smoke helper that checks the existing local API:

- `GET /health`
- `POST /api/task` with existing `{ content }` payload
- `GET /api/tasks`

The helper:

- Uses Python standard-library HTTP calls.
- Accepts `--base-url`, `--task-content`, and `--timeout`.
- Exits non-zero if a smoke check fails.
- Prints concise pass evidence including the created `task_id`.

Operator notes now reference the helper while preserving manual smoke commands.

## Scope Guard

Preserved:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing execution behavior.
- Existing Evolution Governor behavior.
- Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.

Not changed:

- Backend behavior.
- Frontend behavior.
- API semantics.
- Persistence/schema.
- Execution behavior.
- External services.
- Future AI Company System layers.

## System Delivery Verification

Reviewer seat: 系统交付席

Status: PASS.

Fresh verification commands:

```bash
python3 -m py_compile tools/local_demo_api_smoke.py
```

Result: PASS.

```bash
python3 tools/local_demo_api_smoke.py --help
```

Result: PASS. CLI help shows `--base-url`, `--task-content`, and `--timeout`.

```bash
git diff --check
```

Result: PASS.

```bash
git diff --name-only HEAD -- backend frontend
```

Result: PASS, no backend/frontend implementation diff.

```bash
rg -n "tools/local_demo_api_smoke.py|local_demo_api_smoke|health|task creation|task history|base-url" docs/release/ai-task-executor-mvp-v0.1-operator-notes.md tools/local_demo_api_smoke.py reviews/034_local_demo_api_smoke_helper_review.md
```

Result: PASS. Helper and operator-note linkage are present.

Delivery conclusion:

- Helper compiles.
- CLI arguments are visible.
- Operator notes reference the helper.
- No backend/frontend behavior files were changed.

## Quality Verification

Reviewer seat: 质量运行席

Status: PASS.

Verified on 2026-07-07 against implementation commit `67460c0b`.

Local verification server:

```bash
cd backend && CURIS_DB=/private/tmp/curis_local_demo_smoke.sqlite ./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Fresh verification commands:

```bash
python3 tools/local_demo_api_smoke.py --base-url http://127.0.0.1:8765 --task-content "本地自动化验证任务"
```

Result: PASS. The helper called the real local FastAPI app and verified health, task creation, and task history. Created task id: `ee9d98b6-9a31-43b2-bd90-4ff26a7a4be8`.

```bash
python3 -m py_compile tools/local_demo_api_smoke.py
```

Result: PASS.

```bash
git diff --check
```

Result: PASS.

```bash
git diff --name-only HEAD -- backend frontend
```

Result: PASS, no backend/frontend implementation diff.

Quality conclusion:

- Helper verifies the accepted real local API surfaces.
- No mock data or simulation substitution was used.
- No backend/frontend behavior files were changed.
- API semantics, persistence schema, execution behavior, external-service boundary, mock/simulation boundary, and future-layer boundary remain preserved.
- No blockers found.

## Product Acceptance

Reviewer seat: 产品规划席

Decision: ACCEPTED on 2026-07-07.

Rationale:

- The helper reduces repeated local/demo verification effort without changing product behavior.
- Quality verification proves it checks the real local FastAPI app for health, task creation, and task history.
- Operator notes now reference the helper while preserving manual smoke commands.
- No backend/frontend behavior changes, API semantic changes, persistence/schema changes, new execution behavior, external services, mock/simulation substitution, or future-layer scope were introduced.

Accepted artifact:

- `tools/local_demo_api_smoke.py`

Product conclusion:

- Local/Demo Verification Automation first slice is complete.
- AI Task Executor MVP v0.1 can now be manually operated and locally smoke-verified with a repeatable helper.

## Handoff

Handoff: accepted by 产品规划席.

Target seat: main thread closeout.

Compact payload:

Issue: T-127 / Close out Local/Demo API Smoke Helper to user

Objective: Report local/demo verification automation completion and current product progress.

Special Constraints: Quality verification passed for implementation commit `67460c0b` against the real local FastAPI app; product acceptance complete. Local-only tooling implementation. Preserve AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership. No backend/frontend behavior changes, new features, complex UI/dashboard, API semantic changes, persistence/schema changes, new execution behavior, automatic evolution behavior changes, external services, mock/simulation substitution, or future-layer scope.

Next Seat: main thread closeout.
