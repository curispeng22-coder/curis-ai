# Review 075: Workspace Company Foundation First Slice

Date: 2026-07-08
Owner: 系统交付席
Issue: `issues/078_workspace_company_foundation_first_slice_gate.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now show a local/demo company frame in the existing operation console while keeping task execution, model routing, APIs, and runtime behavior unchanged.

## Scope

- Frontend-only implementation under `frontend/app`.
- Adds a bounded `公司工作区` frame inside the existing operation console.
- Uses existing in-memory task list state and existing model preference state only.
- Shows local/demo company identity, default workspace label, local/demo first-version status, model preference summary, task console summary, and source-of-truth links.
- Preserves Task API payload shape `{ content }`.
- Does not add backend/API/schema/persistence changes, new runtime calls, new model-selection behavior, Project Memory writes, department CRUD, workflow routing, Admin Platform implementation, or future L5/L6 scope.

## Changed Files

- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `issues/078_workspace_company_foundation_first_slice_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/075_workspace_company_foundation_first_slice_review.md`

## Verification

TDD red:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Expected first failure confirmed before implementation:

```text
SyntaxError: The requested module './taskViewModel.mjs' does not provide an export named 'buildCompanyFoundationViewModel'
```

Expected follow-up failure confirmed before null-state fix:

```text
TypeError: Cannot read properties of null (reading 'available_models')
```

Post-implementation verification:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 16
pass 16
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

Sandbox result:

```text
Failed to write app endpoint /page
creating new process
binding to a port
Operation not permitted (os error 1)
```

Approved outside-sandbox build result already captured before the no-escalation follow-up:

```text
Compiled successfully
Route (app)
┌ ○ /
├ ○ /_not-found
└ ○ /platform
```

No additional escalated command was requested after the no-escalation follow-up instruction.

## Scope Drift Checks

Whitespace check:

```text
git diff --check -- frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: passed.

Frontend API and payload usage scan:

```text
rg -n "/api/(workspace/model-preference|task|tasks|task/)|fetch\(|buildTaskPayload|buildCompanyFoundationViewModel" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Observed calls remain the existing task/detail/model-preference calls:

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
```

Task payload guard:

```text
buildTaskPayload(content) -> { content }
```

Forbidden implementation scan:

```text
rg -n "billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex organization|business modules|secret|credential|provider SDK|direct provider|New API internal|department CRUD|workflow routing|Project Memory write|task_type|role_id|entry_kind" frontend/app/page.js frontend/app/taskViewModel.mjs
```

Result: no matches.

Backend/Admin/shared/runtime scope note: no files in those areas were changed by this implementation slice.

## Known Gaps

- No browser screenshot/runtime interaction evidence was captured in this delivery pass.
- Quality verification reran automated frontend tests, lint, build, API/payload scan, forbidden-scope scan, secret scan, and commit/file guards. Browser screenshot evidence remains optional and was not required for this pass.

## Quality Verification

Quality Result: PASS.

Commands: frontend view-model tests, frontend lint, frontend build, commit diff check, behavior-file scope guard, API/payload scan, forbidden-scope scan, secret scan, and Chinese company-frame UI scan.

Evidence: implementation commit `dfd60689` contains `frontend/app` files plus issue/review/status updates only; no backend/API/schema/persistence/Admin/shared/deploy/tools/data files entered the commit; 16 frontend tests passed; lint passed; build passed; Task API payload remains `{ content }`; API calls remain existing task/detail/run/model-preference calls; forbidden-scope and secret scans returned no matches.

Risks: browser screenshot/runtime interaction evidence was not captured in this quality pass; hosted production, Admin Platform, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, New API source/internal DB dependency, department CRUD/workflow routing, Task API, execution-loop, tool routing, workflow, model-selection, Project Memory writes, and runtime behavior remain blocked.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

Detailed evidence:

```text
git show --name-only --oneline dfd60689
git diff --check dfd60689^ dfd60689
git diff --name-only dfd60689^ dfd60689
git diff --name-only dfd60689^ dfd60689 -- backend/app backend/tests admin-platform workspace shared deploy tools data
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
rg -n "/api/(workspace/model-preference|task|tasks|task/)|fetch\(|buildTaskPayload|buildCompanyFoundationViewModel" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
rg -n "billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex organization|business modules|secret|credential|provider SDK|direct provider|New API internal|department CRUD|workflow routing|Project Memory write|task_type|role_id|entry_kind" frontend/app/page.js frontend/app/taskViewModel.mjs
```

## Handoff

Issue: `issues/078_workspace_company_foundation_first_slice_gate.md`
Objective: Accept frontend-only Workspace Company Foundation first-slice quality evidence for commit `dfd60689`.
Special Constraints: Quality verification passed with no blockers. Frontend-only scope, ADR-0031/Option A boundary, Task API payload, existing model preference/task APIs, forbidden-scope locks, secret scan, and behavior-file guard are verified; no backend/API/schema/persistence/runtime behavior files entered the commit.
Next Seat: 产品规划席

Handoff: sent to 产品规划席

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close the first Workspace Company Foundation implementation slice and report progress to the main thread.

Scope: Accept the frontend-only local/demo company frame in the existing operation console.

Acceptance Criteria:

- Quality verification passed with no blockers.
- Frontend-only scope is preserved under `frontend/app`.
- Task API payload remains `{ content }`.
- Existing task and model preference APIs are reused without new backend/API/schema/persistence/runtime behavior changes.
- Forbidden-scope locks remain active: hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, New API source/internal DB dependency, department CRUD/workflow routing, execution-loop/tool routing/workflow/model-selection behavior changes, and Project Memory writes remain blocked.

Source Of Truth Updates: `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark T-194 accepted and ready for main thread closeout.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout
