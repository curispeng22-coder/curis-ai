# Workflow Error/Fallback Observability Boundaries Review

Date: 2026-07-06

Reviewer seat: 系统交付席

Source gate: `issues/028_workflow_error_fallback_observability_gate.md`

Boundary issue: `issues/029_workflow_error_fallback_observability_boundaries.md`

Boundary ADR: `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`

## Delivery Status

Status: accepted by 产品规划席.

Delivery type: architecture boundary definition only.

## Boundary Summary

Defined Workflow Error/Fallback Observability as a bounded post-v0.1 reliability slice over existing execution behavior and evidence surfaces.

Current implementation evidence surfaces identified:

- `ToolExecutor.execute_chain` records failed and successful tool attempts in a trace.
- `ToolRouter.fallback_chain` provides existing fallback candidates.
- `Orchestrator._record_adaptations` records `tool_fallback` adaptation events.
- `Orchestrator._run_workflow` records failed tool traces, failed workflow state, failure learning, and `step_failed` events.
- `Orchestrator.run` records `workflow_failed` events and FAILED task state.
- `ResultStore` owns tool traces, workflow traces, auto workflow adaptation logs, failure logs, and tool performance.
- `/api/task/{task_id}/trace` and `/api/task/{task_id}/workflow` expose existing trace and workflow evidence.

## Scope Guard

Preserved:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing tool registry, router, executor, and workflow behavior.
- Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.

Not approved:

- Backend/frontend implementation.
- New product features.
- New UI/dashboard.
- API semantic changes.
- Persistence/schema/new tables.
- New execution behavior.
- New tool-routing or registry behavior.
- External services.
- Automatic evolution behavior changes.
- Future-layer implementation.

## Recommended First Slice

`Workflow Error/Fallback Evidence Map`.

Allowed future implementation, only after product acceptance:

- Backend tests for primary tool failure followed by successful fallback.
- Backend tests for full fallback-chain failure.
- Evidence map across tool trace, workflow state, adaptation log, failure log, and tool performance.
- Documentation or review evidence proving current behavior.

## Verification Plan For 质量运行席

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|new tool-routing behavior|external service|automatic evolution|task-role association|task evidence attachment|future-layer" docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md issues/028_workflow_error_fallback_observability_gate.md issues/029_workflow_error_fallback_observability_boundaries.md reviews/026_workflow_error_fallback_observability_boundaries_review.md
```

Expected:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only in preserved/forbidden scope language.

## Quality Verification

Reviewer seat: 质量运行席

Status: PASS.

Verified on 2026-07-06 against boundary commit `8b96f693`.

Fresh verification commands:

```bash
git diff --name-only HEAD -- backend frontend
```

Result: PASS, no backend/frontend implementation diff.

```bash
git diff --check
```

Result: PASS.

```bash
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|new tool-routing behavior|external service|automatic evolution|task-role association|task evidence attachment|future-layer" docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md issues/028_workflow_error_fallback_observability_gate.md issues/029_workflow_error_fallback_observability_boundaries.md reviews/026_workflow_error_fallback_observability_boundaries_review.md
```

Result: PASS. Matches are limited to preserved/forbidden scope language and verification-command text; no allowed-scope drift was found.

Quality conclusion:

- Boundary remains architecture-only.
- No backend/frontend implementation changes were introduced.
- Recommended first slice remains bounded to backend tests and evidence documentation.
- API semantics, persistence schema, UI boundary, tool-routing semantics, external-service boundary, automatic-evolution boundary, and future-layer boundary remain preserved.
- No blockers found.

## Product Acceptance

Reviewer seat: 产品规划席

Decision: APPROVED on 2026-07-06.

Rationale:

- The boundaries stay inside the accepted post-v0.1 Execution Reliability phase.
- The recommended first slice improves confidence in existing workflow error and fallback evidence without changing product scope.
- Quality verification confirms no backend/frontend implementation drift and no forbidden allowed-scope drift.

Accepted next slice:

`Workflow Error/Fallback Evidence Map`.

Allowed implementation:

- Backend tests for primary tool failure followed by successful fallback.
- Backend tests for full fallback-chain failure.
- Evidence mapping across existing tool trace, workflow state, adaptation log, failure log, and tool performance surfaces.
- Review or documentation evidence proving current behavior.

Still blocked:

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- New execution behavior.
- New tool routing or registry behavior.
- External services or new model-provider integrations.
- Automatic evolution behavior changes.
- ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

## Handoff

Handoff: accepted by 产品规划席.

Target seat: 系统交付席.

Compact payload:

Issue: T-097 / Implement Workflow Error/Fallback Evidence Map

Objective: Implement the accepted first slice with backend tests and evidence documentation only.

Special Constraints: Boundaries accepted. Preserve AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing tool/workflow behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership. Allowed implementation is backend tests and evidence documentation only for existing workflow error/fallback observability. No API semantic changes, persistence/schema changes, UI changes, new execution behavior, new tool routing/registry semantics, external services, automatic evolution behavior changes, or future-layer scope.

Next Seat: 质量运行席 if implementation passes local verification; 产品规划席/system revision if blocked.
