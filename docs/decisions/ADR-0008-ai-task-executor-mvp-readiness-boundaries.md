# ADR-0008: AI Task Executor MVP Readiness Review Boundaries

Date: 2026-07-06

Status: Accepted for MVP readiness review planning

Related issue: `issues/018_sprint_4_closeout_mvp_readiness_gate.md`

## Context

Sprint 4 multi-entry UI first slice is implemented, verified, and accepted. 总控决策席 approved Sprint 4 first-slice closeout and opened AI Task Executor MVP readiness review as gate-only planning.

The readiness review is a checkpoint over the accepted AI Task Executor MVP foundation. It is not a feature implementation issue and does not approve broader AI Company System layers.

Preserved boundaries:

- AI Task Executor MVP remains the current launch scope.
- Tool System v1.8 remains the active implementation gate.
- Sprint 2 unified task console boundary remains accepted.
- Project Memory boundary remains accepted.
- Role Profiles boundary remains accepted.
- Role Context runtime reference boundary remains accepted.
- Sprint 4 frontend-only multi-entry boundary remains accepted.
- Existing source-of-truth ownership remains unchanged.

## Decision

Define MVP readiness review as a gate-only architecture and verification planning activity.

The review may:

- Map existing MVP capabilities from Task API, run action, history, selected detail, execution evidence, Project Memory, role guidance, and Sprint 4 entry affordances.
- Plan verification across backend tests, frontend tests, build/lint, API evidence, source-of-truth consistency, and scope guardrails.
- Classify gaps without implementing them.
- Route classified gaps to the responsible Curis seat for separate approval.

The review must not:

- Implement features or change runtime behavior.
- Change APIs, persistence, task schema, task types, task-role associations, or execution semantics.
- Expand into ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, external channels, complex UI/dashboard, automatic evolution behavior, or future-layer scope.
- Attach new task evidence or expand runtime prompt integration beyond the already approved role-context helper behavior.

## Readiness Scope

The readiness review covers existing AI Task Executor MVP surfaces only:

- Task creation through `POST /api/task` with `{ content }`.
- Existing run action through `POST /api/task/{task_id}/run`.
- Existing task status and history APIs.
- Existing selected-task detail evidence: result, workflow, tool trace/fallback, learning, meta-development, and evolution-decision records.
- Existing Project Memory source-of-truth read model.
- Existing deterministic role profiles and approved explicit role-context helper.
- Existing Sprint 4 frontend-only task-entry starters that prefill ordinary composer content.

## Verification Plan

质量运行席 should verify the readiness boundary with evidence from current source files and accepted reviews.

Required checks:

- Confirm no backend or frontend implementation files changed during boundary planning.
- Confirm ADR-0008 and review evidence define planning only.
- Confirm current Task API payload shape remains `{ content }`.
- Confirm current tests/build/lint commands are known and runnable for a future readiness pass.
- Confirm source-of-truth files agree on current sprint, active gate, next task, and known gaps.
- Confirm forbidden-scope scan shows any matches are guardrail text only, not implementation.

Recommended command set:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
cd backend && ./.venv/bin/python -m unittest discover tests
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
rg -n "Task API|\\{ content \\}|MVP readiness|gap classification" docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md reviews
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|new execution behavior|API semantic|persistence|new table|task-role association|task evidence attachment|automatic evolution" backend/app backend/tests frontend/app
```

## Gap Classification Plan

Each readiness gap must be classified before any implementation issue is opened.

Allowed classes:

- `blocker`: prevents a credible AI Task Executor MVP readiness decision; requires product or gate decision before implementation.
- `stabilization`: improves reliability of existing approved behavior without changing product or execution semantics.
- `verification`: adds or repairs tests, lint/build evidence, API evidence, scope scans, or runtime verification scripts.
- `documentation`: aligns source-of-truth files, known gaps, handoffs, or operating instructions.
- `future_product_scope`: valuable but outside current MVP readiness; must remain deferred until a separate gate.

Classification requirements:

- Every gap must include source evidence, affected existing surface, proposed owner seat, and whether a separate issue is required.
- Any gap touching external services, secrets, privacy, or data handling routes to 安全边界席 before implementation.
- Any gap requiring API semantics, persistence, runtime behavior, UI expansion, or future layers routes to 总控决策席 or 产品规划席 before implementation.
- 系统交付席 may implement only a separately approved issue after classification and routing.

## Consequences

- The next step is quality verification planning for ADR-0008 and its review evidence.
- No code or runtime behavior is changed by this ADR.
- MVP readiness implementation follow-up remains blocked until a gap is classified and separately approved.
