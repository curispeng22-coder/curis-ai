# Workspace Model Preference UI First Slice Review

Date: 2026-07-08
Owner: 系统交付席
Issue: `issues/073_workspace_model_preference_ui_gate.md`
Status: READY_FOR_QUALITY_VERIFICATION

## Product Progress

Curis Workspace can now let the CEO view, save, and reset the Workspace default model from active official model options inside the existing operation console.

## Scope

- Frontend-only implementation under `frontend/app`.
- UI stays inside the existing Workspace operation console shell.
- Uses only existing Workspace preference APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference` with `{ "model_key": "..." }`
  - `DELETE /api/workspace/model-preference`
- Displays current preference, active official model options, loading/saving/reset/error states, and Chinese copy.
- Preserves current Task API payload shape `{ content }`.

## Changed Files

- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `issues/073_workspace_model_preference_ui_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/070_workspace_model_preference_ui_review.md`

## Verification

TDD red:

```text
node --test app/taskViewModel.test.mjs
```

Expected failure confirmed before implementation:

```text
SyntaxError: The requested module './taskViewModel.mjs' does not provide an export named 'buildModelPreferencePayload'
```

Post-implementation verification:

```text
node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 14
pass 14
fail 0
```

```text
npm run lint
```

Result:

```text
eslint .
```

Exit code: 0.

```text
npm run build
```

Sandbox result:

```text
Failed to write app endpoint /page
creating new process
binding to a port
Operation not permitted (os error 1)
```

Rerun outside sandbox with approval:

```text
npm run build
```

Result:

```text
Compiled successfully
Route (app)
┌ ○ /
├ ○ /_not-found
└ ○ /platform
```

## Scope Drift Checks

UI credential/scope text scan:

```text
rg -n "api_key|credential_ref|Authorization|Bearer|secret|password|billing|ROI|tenant package|marketplace|optimization|provider SDK|New API|department|employee" frontend/app/page.js frontend/app/taskViewModel.mjs
```

Result: no matches.

Frontend API usage scan:

```text
rg -n "/api/(workspace/model-preference|task|tasks|task/)" frontend/app/page.js
```

Observed calls:

```text
/api/tasks
/api/task/{task_id}
/api/task/{task_id}/workflow
/api/task/{task_id}/trace
/api/task/{task_id}/meta-development
/api/task/{task_id}/evolution-decisions
/api/workspace/model-preference
/api/task
/api/task/{task_id}/run
/api/workspace/model-preference
/api/workspace/model-preference
```

Task payload guard:

```text
buildTaskPayload(content) -> { content }
```

Preference payload guard:

```text
buildModelPreferencePayload(modelKey) -> { model_key: modelKey }
```

Backend/Admin/shared/runtime files: no implementation changes were made for this issue.

## Known Gaps

- No automated browser interaction evidence was captured in this delivery pass.
- Quality seat should verify the UI against a running backend if runtime environment evidence is required.

## Quality Verification

PASS.

Fresh verification was run by 质量运行席 on commit `5727410f`.

Commands:

```bash
cd frontend
node --test app/taskViewModel.test.mjs
npm run lint
npm run build
cd ..
git diff --check 5727410f^ 5727410f
git diff --name-only 5727410f^ 5727410f -- backend admin-platform shared workspace deploy plugins tools data
rg -n "api_key|credential_ref|Authorization|Bearer|secret|password|billing|ROI|tenant package|marketplace|optimization|provider SDK|New API|department|employee|prompt|output|raw|credential|token" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
rg -n "/api/[A-Za-z0-9_{}$./?-]+|fetch\\(|buildTaskPayload|buildModelPreferencePayload" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
git diff 5727410f^ 5727410f -- frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs | rg -n "^\\+.*(api_key|credential_ref|Authorization|Bearer|secret|password|billing|ROI|tenant package|marketplace|optimization|provider SDK|New API|department|employee|raw gateway|provider account|token)"
git diff 5727410f^ 5727410f -- frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs | rg -n "^\\+.*(/api/|fetch\\(|buildTaskPayload|buildModelPreferencePayload|body:)"
```

Evidence:

- Frontend view-model tests: 14 tests ran and passed.
- Frontend lint passed.
- Frontend build first failed inside the sandbox with the known Next/Turbopack port-binding restriction, then passed outside the sandbox with approval.
- Commit diff hygiene passed.
- Backend/Admin/shared/workspace/deploy/plugins/tools/data implementation guard returned no files.
- API usage scan showed the new selector calls only `GET /api/workspace/model-preference`, `PUT /api/workspace/model-preference`, and `DELETE /api/workspace/model-preference`; existing task/history/detail calls are unchanged.
- Task API payload remains `buildTaskPayload(content) -> { content }`; preference payload is `buildModelPreferencePayload(modelKey) -> { model_key: modelKey }`.
- UI secret/scope scan found no rendered secret-like fields in implementation. The only added `credential_ref` match is a test fixture proving it is not rendered.

Acceptance Check:

- Frontend-only scope is preserved under `frontend/app`.
- UI uses existing Workspace preference APIs only.
- Task API payload shape `{ content }` is preserved.
- No backend/Admin/shared/runtime execution-path files changed for this issue.
- No secret-like metadata is exposed by the model preference view model.

Quality Result: PASS; no blockers found.

## Product Acceptance

ACCEPTED by 产品规划席 on 2026-07-08.

Reason:

- Quality verification passed for commit `5727410f`.
- Frontend-only selector stayed inside the existing Workspace operation console.
- UI uses only existing Workspace preference APIs and preserves Task API `{ content }`.
- No backend/Admin/shared/runtime execution-path files changed for this issue.
- No secret-like metadata is exposed by the model preference view model.

## Handoff

Issue: `issues/073_workspace_model_preference_ui_gate.md`
Objective: Accept frontend-only Workspace model preference selector verification for commit `5727410f`.
Special Constraints: Quality verification passed with no blockers. UI uses only existing preference APIs, preserves Task API `{ content }`, exposes no secret-like metadata, and does not alter backend/Admin/shared/runtime execution paths.
Next Seat: main thread closeout

Handoff: final closeout
