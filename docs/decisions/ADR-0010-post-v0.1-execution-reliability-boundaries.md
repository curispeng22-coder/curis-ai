# ADR-0010: Post-v0.1 Execution Reliability Boundaries

Date: 2026-07-06

Status: Accepted by 产品规划席 on 2026-07-06

Related gate: `issues/025_post_v0_1_execution_reliability_gate.md`

Related release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`

## Context

AI Task Executor MVP v0.1 has been closed as the first local/demo version. The current product should now strengthen reliability of the existing execution loop before expanding into future AI Company System layers.

The protected execution loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

Current implementation surfaces already include:

- Task creation, run, status, history, trace, workflow, meta-development, and evolution-decision APIs.
- `Orchestrator` workflow generation, state transitions, execution, trace persistence, failure handling, learning loop, meta-development loop, and Evolution Governor invocation.
- `ToolExecutor` chain execution and fallback trace.
- `ResultStore` persistence for tasks, executions, traces, workflows, auto workflows, workflow traces, failure logs, tool performance, workflow metrics, execution scores, development strategies, system evolution logs, evolution simulations, evolution decisions, and rollback records.
- Existing backend tests in `backend/tests/test_execution_engine.py`.

This phase must not change product scope. It defines boundaries and verification planning only.

## Decision

Define post-v0.1 Execution Reliability as a bounded stabilization architecture phase over the existing AI Task Executor surfaces.

The phase may define and later implement approved reliability work only when a separate implementation issue is accepted.

It must preserve:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop and Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing SQLite persistence schema unless a separate schema gap is approved.
- Project Memory, Role Profiles, and Role Context boundaries.
- v0.1 release record/tag semantics.
- Source-of-truth ownership.

## Reliability Boundary Areas

### 1. Run Endpoint Verification

Allowed:

- Define test coverage for successful `/api/task/{task_id}/run` execution using deterministic local test executors.
- Define test coverage for failed run behavior, HTTP error mapping, task status transition, workflow status transition, and trace/error evidence.
- Define smoke evidence requirements for local/demo run behavior when an approved executor environment exists.

Not allowed:

- Changing run API request or response semantics.
- Adding external model-provider dependencies.
- Adding new run modes, mock/simulation product modes, or background job systems.

### 2. Execution Trace And Result Evidence Quality

Allowed:

- Define evidence completeness expectations for task result, executions, tool traces, workflow traces, workflow state, auto workflow adaptation log, meta-development report, evolution decision, simulation, and rollback record.
- Define missing-evidence classification as stabilization gap, verification gap, documentation gap, or future product scope.
- Define read-only review criteria for existing evidence APIs.

Not allowed:

- Adding new persistence tables.
- Adding task evidence attachment.
- Changing stored evidence meaning.
- Introducing complex dashboard UI.

### 3. Workflow, Error, And Fallback Observability

Allowed:

- Define expected observability for tool fallback, step failure, workflow failure, failure log, tool performance, and adaptation events.
- Define verification cases for primary tool failure falling back to approved existing tools.
- Define operator-readable local/demo evidence checklist.

Not allowed:

- New tool-routing behavior without separate implementation approval.
- New tool registry semantics.
- Multi-agent routing.
- Agent abstraction layer.

### 4. Stability Gate For Evolution Behavior

Allowed:

- Define verification that Evolution Governor records decisions after execution and can decide not to evolve, postpone, or rollback within existing v1.8 rules.
- Define evidence expectations for thresholds, simulation, risk, approval, rollback, and stability-first policy.

Not allowed:

- Automatic evolution behavior changes.
- Code self-modification.
- Architecture mutation without approval.
- Unlocking locked modules.

### 5. Current L1-L4 Test Coverage Plan

Allowed:

- Define a coverage map for L1 task execution, L2 execution employee, L3 tool routing/execution, and L4 workflow generation/execution.
- Define regression commands and required evidence for backend, frontend view-model, lint/build, API smoke, and forbidden-scope scan.
- Define a gap list for future accepted implementation issues.

Not allowed:

- Opening L5 company organization or L6 economy/ROI work.
- New business modules.
- Employee CRUD/expansion.
- External channels.

## First Implementation Slice Recommendation

Recommended first slice after this boundary is verified and accepted:

`Run Evidence Reliability`.

Scope should be limited to backend tests and documentation/evidence around existing run behavior:

- Successful run preserves task status, execution row, workflow state, trace, workflow trace, learning metrics, meta-development report, and evolution decision evidence.
- Failed run preserves FAILED task status, failed workflow status, failure/adaptation evidence, and HTTP error mapping.
- No API semantic change, persistence/schema change, UI change, external service, or new execution behavior.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|new execution behavior|API semantic|persistence|new table|task-role association|task evidence attachment|automatic evolution|vector database|embedding|external service" docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md issues/026_post_v0_1_execution_reliability_boundaries.md reviews/024_post_v0_1_execution_reliability_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicitly forbidden scope, not as allowed work.

## Consequences

- Quality verification passed in `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`.
- 产品规划席 accepted the architecture boundaries on 2026-07-06.
- No implementation is approved by this ADR alone.
- The first implementation slice is opened separately as `issues/027_run_evidence_reliability_first_slice.md`.
- Any implementation must stay inside the accepted `Run Evidence Reliability` scope and preserve existing API semantics, persistence schema, UI, and execution behavior.
