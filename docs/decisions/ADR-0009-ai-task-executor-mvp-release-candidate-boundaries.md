# ADR-0009: AI Task Executor MVP Release-Candidate Boundaries

Date: 2026-07-06

Status: Accepted by 产品规划席 on 2026-07-06

Related issue: `issues/021_ai_task_executor_mvp_release_candidate_gate.md`

## Context

The AI Task Executor MVP readiness review was accepted with no blocker gaps. The operation console was localized to Chinese as frontend-only presentation work. 总控决策席 approved AI Task Executor MVP release-candidate entry for boundary definition and stabilization/documentation planning only.

The release-candidate pass is a first-version readiness checkpoint. It is not a product expansion and does not approve runtime, API, persistence, or UI feature changes.

Preserved boundaries:

- AI Task Executor MVP remains the launch scope.
- Tool System v1.8 remains the active gate.
- Chinese operation console remains the accepted UI presentation baseline.
- Task API payload remains `{ content }`.
- Accepted MVP readiness review remains the release evidence baseline.
- Project Memory, Role Profiles, Role Context, and Sprint 4 frontend-only boundaries remain unchanged.
- Source-of-truth ownership remains unchanged.

## Decision

Define release-candidate work as stabilization, verification standardization, startup/deployment documentation, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning only.

The release-candidate pass may:

- Standardize verification commands and interpreter/runtime assumptions.
- Plan stabilization for accepted readiness gaps without implementing them in this boundary issue.
- Define startup and local/demo deployment documentation.
- Define release checklist and rollback notes.
- Define regression coverage for backend tests, frontend tests, lint, build, API smoke, Chinese UI, and scope drift.

The release-candidate pass must not:

- Add new product features.
- Change backend/frontend behavior, Task API semantics, persistence, execution behavior, or schema.
- Add ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, external channels, complex dashboard UI, task-role association, task evidence attachment, automatic evolution behavior, vector DB/embeddings, external services, or future-layer scope.

## Exact Stabilization And Documentation Plan

Release-candidate follow-up should be opened as a separate implementation issue only after this boundary plan is accepted.

Approved planning items:

| ID | Class | Scope | Output | Verification |
| --- | --- | --- | --- | --- |
| RC-PLAN-001 | verification standardization | Document canonical backend regression command: `cd backend && ./.venv/bin/python -m unittest discover tests`; document system Python as unsupported unless dependencies are prepared. | Startup/release docs or quality runbook update. | Command reference review plus backend test PASS. |
| RC-PLAN-002 | startup docs | Document local backend and frontend startup steps, required working directories, dependency assumptions, API base configuration, and expected local URLs. | Local startup section in release docs. | Fresh command walkthrough by 质量运行席. |
| RC-PLAN-003 | demo deployment docs | Document local/demo deployment path using existing backend and frontend only; no external service or production integration. | Local/demo deployment instructions. | Build/lint/test evidence plus local smoke checklist. |
| RC-PLAN-004 | release checklist | Define first-version checklist covering backend regression, frontend view-model tests, lint, build, API smoke, Chinese UI review, source-of-truth alignment, and forbidden-scope scan. | Release checklist. | 质量运行席 checklist execution evidence. |
| RC-PLAN-005 | rollback notes | Document local rollback steps for release-candidate artifacts and accepted source-of-truth state. | Rollback notes. | Review of git commit/tag or documented restore point process. |
| RC-PLAN-006 | stabilization triage | Decide whether the FastAPI Python 3.14 deprecation warning requires a fix before first-version release. | Stabilization decision or separate issue. | If fixed later, backend regression remains PASS; if deferred, known gap is documented. |

Blocked or deferred items:

- Sprint 2 status filters and local presentation preferences remain future product scope.
- Project Memory execution-summary memory remains future read-model scope.
- Runtime prompt integration, task evidence attachment, role selector, backend metadata, persistence, and task-role association remain future gated scope.
- Broader task-entry expansion remains future product scope.
- Raw JSON backend field names in evidence inspection remain acceptable for stored evidence inspection unless 产品规划席 opens a separate presentation issue.

## Regression Verification Plan

质量运行席 should verify release-candidate boundary planning with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
cd backend && ./.venv/bin/python -m unittest discover tests
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
rg -n "Create Task|Run Task|Task Composer|Task History|Selected Task Detail" frontend/app
rg -n "创建|运行|任务|执行|工作流|工具|学习|演进" frontend/app
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|new execution behavior|API semantic|persistence|new table|task-role association|task evidence attachment|automatic evolution|vector database|embedding|external service" backend/app backend/tests frontend/app
```

Expected results:

- No backend/frontend implementation diff in the boundary-planning commit.
- Backend regression passes with repo virtualenv.
- Frontend tests, lint, and build pass.
- Chinese UI strings remain present and old English visible-console labels do not reappear.
- Forbidden-scope scan has no implementation-path matches.

## Consequences

- The boundary plan was verified by 质量运行席 and accepted by 产品规划席.
- No implementation is approved by this ADR alone.
- Release-candidate implementation is unblocked only for the separate scoped issue `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`.
