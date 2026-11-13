# ADR-0011: Workflow Error/Fallback Observability Boundaries

Date: 2026-07-06

Status: Proposed for quality verification

Related gate: `issues/028_workflow_error_fallback_observability_gate.md`

Related reliability phase: `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`

## Context

AI Task Executor MVP v0.1 is released as the first local/demo version. The accepted post-v0.1 reliability phase is strengthening the existing L1-L4 execution base before opening future AI Company System layers.

Run Evidence Reliability has been implemented, verified, and accepted in `reviews/025_run_evidence_reliability_first_slice_review.md`.

The next reliability area is observability for existing workflow error and tool fallback behavior.

Current implementation surfaces already include:

- `ToolExecutor.execute_chain`, which records per-attempt tool trace entries and tries fallback candidates from the existing router fallback chain.
- `Orchestrator._record_adaptations`, which records `tool_fallback` adaptation events when a step succeeds after a failed attempt.
- `Orchestrator._run_workflow`, which records failed tool traces, failed workflow step state, and `step_failed` adaptation events when all fallback candidates fail.
- `Orchestrator.run`, which records `workflow_failed` adaptation events and FAILED task state after workflow failure.
- `ResultStore` surfaces for `tool_traces`, `workflow_traces`, `auto_workflows.adaptation_log`, `failure_logs`, and `tool_performance`.
- API evidence through `/api/task/{task_id}/trace` and `/api/task/{task_id}/workflow`.
- Existing backend tests for primary tool fallback, auto-workflow fallback adaptation, workflow API trace, failure analysis, and failed-run evidence.

This boundary does not approve implementation. It defines what a later implementation slice may verify or clarify.

## Decision

Define Workflow Error/Fallback Observability as a bounded architecture slice over existing execution behavior and evidence.

The slice must preserve:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing tool registry, tool router, tool executor, and workflow behavior.
- Project Memory, Role Profiles, Role Context, release record/tag semantics, and source-of-truth ownership.

## Boundary Areas

### 1. Tool Fallback Evidence

Allowed:

- Verify that a failed primary tool attempt is visible in tool trace evidence.
- Verify that the successful fallback tool attempt is visible in tool trace evidence.
- Verify that fallback adaptation events identify the failed tool and selected fallback tool.
- Verify that tool performance records failed and successful attempts using existing semantics.

Not allowed:

- Changing fallback candidate order.
- Adding new tool routing behavior.
- Adding new tool registry semantics.
- Adding new external tools or model providers.

### 2. Workflow Error Evidence

Allowed:

- Verify that failed workflow execution records FAILED task status.
- Verify that workflow state records failed step evidence.
- Verify that auto workflow adaptation log records `step_failed` and `workflow_failed` events.
- Verify that failure logs record root cause and correction strategy with existing fields.

Not allowed:

- Changing HTTP semantics.
- Changing task status semantics.
- Adding new workflow states.
- Adding new persistence tables or evidence attachment models.

### 3. Operator-Readable Evidence Map

Allowed:

- Define a deterministic evidence map from one execution to the existing evidence surfaces: task status, tool trace, workflow status, workflow trace, adaptation log, failure log, tool performance, and evolution decision.
- Classify missing or weak evidence as stabilization, verification, documentation, or future product scope.
- Document which existing API or store method owns each evidence surface.

Not allowed:

- Adding a dashboard.
- Adding UI complexity.
- Adding external monitoring services.
- Adding future L5/L6 product-layer concepts.

## First Implementation Slice Recommendation

Recommended first slice after quality verification and product acceptance:

`Workflow Error/Fallback Evidence Map`.

Scope should be limited to backend tests and documentation/evidence around existing behavior:

- Primary tool failure followed by successful fallback.
- Full fallback-chain failure.
- Evidence mapping across tool trace, workflow state, adaptation log, failure log, and tool performance.
- No API semantic change, persistence/schema change, UI change, external service, new execution behavior, or future-layer scope.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|new tool-routing behavior|external service|automatic evolution|task-role association|task evidence attachment|future-layer" docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md issues/028_workflow_error_fallback_observability_gate.md issues/029_workflow_error_fallback_observability_boundaries.md reviews/026_workflow_error_fallback_observability_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicit forbidden or preserved-scope text, not as allowed implementation work.

## Consequences

- This ADR does not approve implementation.
- The next seat is 质量运行席 for architecture-boundary verification.
- If accepted, 产品规划席 may open a separate first implementation issue.
- Any later implementation must preserve existing API semantics, persistence schema, UI scope, tool routing semantics, and execution behavior.
