# AI Task Executor MVP Release-Candidate Boundaries Review

Date: 2026-07-06

Reviewer seat: 系统交付席

Source issue: `issues/021_ai_task_executor_mvp_release_candidate_gate.md`

Architecture record: `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`

## Verdict

Boundary status: ACCEPTED BY 产品规划席.

Blockers: None.

Implementation status: No implementation performed.

## Boundary Summary

- Release-candidate work is limited to stabilization planning, verification command standardization, startup/deployment documentation, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning.
- The current Chinese operation console, Task API `{ content }`, Tool System v1.8 loop, accepted readiness review, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and source-of-truth ownership are preserved.
- Release-candidate implementation remains blocked until this boundary plan is verified and accepted, then a separate scoped issue is opened.

## Exact Plan

| ID | Class | Scope | Output | Verification |
| --- | --- | --- | --- | --- |
| RC-PLAN-001 | verification standardization | Canonicalize backend regression as `cd backend && ./.venv/bin/python -m unittest discover tests`. | Startup/release docs or quality runbook update. | Backend regression PASS and command reference review. |
| RC-PLAN-002 | startup docs | Document local backend/frontend startup, working directories, dependencies, API base, and expected local URLs. | Local startup instructions. | Fresh walkthrough by 质量运行席. |
| RC-PLAN-003 | demo deployment docs | Document local/demo deployment using existing backend/frontend only. | Local/demo deployment instructions. | Build/lint/test evidence plus local smoke checklist. |
| RC-PLAN-004 | release checklist | Backend tests, frontend tests, lint, build, API smoke, Chinese UI, source-of-truth alignment, and scope drift. | Release checklist. | 质量运行席 checklist execution evidence. |
| RC-PLAN-005 | rollback notes | Document local rollback for release-candidate artifacts and source-of-truth state. | Rollback notes. | Review documented restore point process. |
| RC-PLAN-006 | stabilization triage | Decide whether the FastAPI Python 3.14 deprecation warning must be fixed before first-version release. | Stabilization decision or separate issue. | If fixed later, backend tests remain PASS; if deferred, known gap remains documented. |

Deferred by boundary:

- Sprint 2 status filters and local presentation preferences.
- Project Memory execution-summary memory.
- Runtime prompt integration, task evidence attachment, role selector, backend metadata, persistence, and task-role association.
- Broader task-entry expansion.
- Raw JSON backend field-name presentation in evidence inspection unless separately approved.

## Verification Plan For 质量运行席

| Area | Command / Evidence | Expected Result |
| --- | --- | --- |
| Boundary file review | `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md` | Confirms release-candidate planning only. |
| Review evidence | `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md` | Confirms no implementation approval. |
| No implementation diff | `git diff --name-only HEAD -- backend frontend` | No backend/frontend implementation files changed by T-075. |
| Diff hygiene | `git diff --check` | PASS. |
| Backend regression command | `cd backend && ./.venv/bin/python -m unittest discover tests` | PASS, with known Python 3.14 FastAPI warning if still present. |
| Frontend regression | `cd frontend && node --test app/taskViewModel.test.mjs` | PASS. |
| Frontend lint/build | `cd frontend && npm run lint` and `cd frontend && npm run build` | PASS or documented sandbox note for build. |
| Chinese UI guard | Search `frontend/app` for old English visible-console labels and Chinese operational labels. | Chinese labels remain present; old visible-console labels do not reappear. |
| Scope drift scan | Scan implementation paths for forbidden scope terms. | No implementation-path matches. |
| Source-of-truth consistency | Review `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md`. | Current sprint, next seat, and blocked implementation state align. |

## Quality Verification

Reviewer seat: 质量运行席

Quality status: PASS

Verified boundary commit: `d94fc084`

| Area | Command / Evidence | Result |
| --- | --- | --- |
| Commit boundary | `git show --name-only --oneline d94fc084` | PASS: changed files are ADR, sprint planning, issue, review, architecture/status/task/context/memory files only. |
| No backend/frontend implementation in commit | `git show --name-only --oneline d94fc084 -- backend frontend` | PASS: no backend/frontend implementation files changed by the boundary commit. |
| Current backend/frontend diff guard | `git diff --name-only HEAD -- backend frontend` | PASS: no current backend/frontend implementation diff. |
| Diff hygiene | `git diff --check` | PASS. |
| Backend regression | `cd backend && ./.venv/bin/python -m unittest discover tests` | PASS: 34 tests. FastAPI emits the known Python 3.14 deprecation warning. |
| Frontend view-model regression | `cd frontend && node --test app/taskViewModel.test.mjs` | PASS: 12 tests. |
| Frontend lint | `cd frontend && npm run lint` | PASS. |
| Frontend build | `cd frontend && npm run build` | PASS outside sandbox; Turbopack requires local worker port binding. |
| Chinese UI guard - old labels | `rg -n "Create Task\|Run Task\|Task Composer\|Task History\|Selected Task Detail\|No tasks yet\|No task selected\|Loading task evidence\|Task Entry\|Choose a starter\|Freeform" frontend/app` | PASS: no old visible-console English labels found. |
| Chinese UI guard - current labels | `rg -n "创建\|运行\|任务\|执行\|工作流\|工具\|学习\|演进" frontend/app` | PASS: Chinese operation-console labels and view-model strings are present. |
| Scope drift scan | `rg -n "ROI\|business module\|Employee CRUD\|employee expansion\|company organization\|department\|reporting line\|staffing\|multi-agent\|agent abstraction\|external channel\|dashboard\|new execution behavior\|API semantic\|persistence\|new table\|task-role association\|task evidence attachment\|automatic evolution\|vector database\|embedding\|external service" backend/app backend/tests frontend/app` | PASS: no matches in implementation paths. |
| Source-of-truth consistency | Review `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` | PASS: current sprint, active task, release-candidate planning scope, and blocked implementation state align. |

Quality observations:

- ADR-0009 and this review keep release-candidate work limited to stabilization planning, verification command standardization, startup/deployment docs, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning.
- No implementation, backend/frontend behavior change, API semantic change, persistence change, execution-loop change, complex UI/dashboard, external service, or future-layer scope was introduced.
- The exact RC plan is bounded to RC-PLAN-001 through RC-PLAN-006, with implementation still blocked until a separately approved issue defines exact scope and verification.
- Chinese operation console labels remain present, and old visible-console English labels did not reappear.

## Product Acceptance

Reviewer seat: 产品规划席

Acceptance status: ACCEPTED

Accepted on: 2026-07-06

Product decision:

- Accept the release-candidate boundaries and exact stabilization/documentation plan.
- Approve RC-PLAN-001 through RC-PLAN-006 as the only allowed release-candidate planning items.
- Keep implementation blocked until a separate scoped issue is opened for stabilization/documentation work.
- Keep all future product scope deferred until after first-version release-candidate completion.

## Scope Risk

Low. T-075 changes planning and source-of-truth files only. It does not change backend, frontend, API, persistence, execution behavior, UI behavior, external services, or future-layer scope.

## Handoff

Handoff: main thread closeout

Target seat: 产品规划席

Compact payload:

Issue: T-077 / Accept AI Task Executor MVP release-candidate boundaries

Objective: Review `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md` and accept or revise the release-candidate boundaries and exact stabilization/documentation plan.

Special Constraints: Quality verification passed for boundary commit `d94fc084`. No implementation approved. Preserve Chinese operation console, current Task API `{ content }`, accepted readiness review, Tool System v1.8, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and source-of-truth ownership. Release-candidate work remains planning-only until separately approved.

Next decision: open a separate release-candidate stabilization/documentation implementation issue.
