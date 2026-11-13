# Run Evidence Reliability First Slice Review

Date: 2026-07-06

Reviewer seat: 系统交付席

Source issue: `issues/027_run_evidence_reliability_first_slice.md`

Boundary ADR: `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`

## Delivery Status

Status: accepted by 产品规划席.

Implementation status: backend reliability test coverage plus evidence-quality fix.

## Implementation Summary

Implemented `Run Evidence Reliability` first slice inside the accepted post-v0.1 boundary.

Changes:

- Added success-path backend reliability coverage proving a completed run exposes task status, execution row, tool trace, workflow state, workflow trace, meta-development report, and evolution decision evidence.
- Added failure-path backend reliability coverage proving a failed run exposes one non-duplicated tool error trace, FAILED task status, FAILED workflow state, failed step evidence, and adaptation events.
- Fixed duplicate failed-run tool trace persistence by keeping trace storage in the workflow step failure handler and avoiding a second save in the outer run failure handler.

## Scope Guard

Preserved:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.

Not changed:

- Frontend files.
- API route shapes.
- Persistence schema.
- UI.
- External services.
- Product features.
- Execution behavior beyond duplicate evidence persistence.
- Automatic evolution behavior.
- Future-layer scope.

## Verification Evidence

Targeted RED evidence:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_failed_run_records_single_error_trace_and_workflow_evidence
```

Result before fix: FAIL. The trace API returned duplicated failed tool evidence: `codex_tool`, `codex_tool`, `gpt_tool`, `gpt_tool`, `default_tool`, `default_tool`.

Targeted GREEN evidence:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_failed_run_records_single_error_trace_and_workflow_evidence
```

Result after fix: PASS.

Focused reliability evidence:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_successful_run_exposes_complete_existing_evidence_chain tests.test_execution_engine.ExecutionEngineTest.test_failed_run_records_single_error_trace_and_workflow_evidence
```

Result: PASS, 2 tests.

Backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: PASS, 36 tests.

Known warning:

- FastAPI emits the existing Python 3.14 deprecation warning. It remains `defer-known-gap`.

## Quality Verification

Reviewer seat: 质量运行席

Status: PASS.

Verified on 2026-07-06 against the current workspace state after implementation commit `8b08b22d`.

Fresh verification commands:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_successful_run_exposes_complete_existing_evidence_chain tests.test_execution_engine.ExecutionEngineTest.test_failed_run_records_single_error_trace_and_workflow_evidence
```

Result: PASS, 2 tests.

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: PASS, 36 tests.

```bash
git diff --check
```

Result: PASS.

```bash
git diff --name-only HEAD -- frontend
```

Result: PASS, no frontend diff.

```bash
git diff --name-only HEAD -- backend/app backend/tests
```

Result: PASS, no uncommitted backend implementation diff during quality verification.

```bash
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic|persistence/schema|new table|task-role association|task evidence attachment|automatic evolution|vector database|embedding|external service" backend/app backend/tests issues/027_run_evidence_reliability_first_slice.md reviews/025_run_evidence_reliability_first_slice_review.md
```

Result: PASS. Matches are limited to issue and review preservation/forbidden-scope text; no backend implementation or test drift was found.

Known warning:

- FastAPI emits the existing Python 3.14 deprecation warning. It remains `defer-known-gap`.

Quality conclusion:

- Successful run evidence chain is covered.
- Failed run evidence chain is covered.
- Duplicate failed-run tool trace persistence is resolved.
- API semantics, persistence schema, UI boundary, external-service boundary, new-feature boundary, and future-layer boundary remain preserved.
- No blockers found.

## Product Acceptance

Reviewer seat: 产品规划席

Decision: APPROVED on 2026-07-06.

Rationale:

- The slice strengthens confidence in the existing AI Task Executor run path without expanding product scope.
- The quality evidence proves both successful-run and failed-run evidence chains.
- The duplicate failed-run trace fix improves evidence correctness while preserving API semantics, persistence schema, UI scope, and execution-loop boundaries.
- The slice supports the post-v0.1 Execution Reliability phase and keeps future AI Company System layers grounded on a more reliable L1-L4 execution base.

Accepted scope:

- Backend reliability coverage for existing run behavior.
- Evidence-quality correction for duplicate failed-run trace persistence.
- Source-of-truth updates for the accepted verification result.

Still blocked:

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- External services or new model-provider integrations.
- New product features.
- New execution behavior.
- Automatic evolution behavior changes.
- ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

Next product move:

- Open a bounded gate for Workflow Error/Fallback Observability as the next post-v0.1 reliability slice.

## Handoff

Handoff: accepted by 产品规划席; main thread closeout complete.

Target seat: 总控决策席 for the next reliability gate.

Compact payload:

Issue: T-093 / Review Workflow Error/Fallback Observability gate

Objective: Decide whether to approve architecture boundary definition for the next post-v0.1 reliability slice.

Special Constraints: Run Evidence Reliability first slice is accepted. Preserve AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership. New gate is boundary-definition only for existing workflow error and tool fallback observability. No implementation, API semantic change, persistence/schema change, UI change, external service, new product feature, new execution behavior, automatic evolution behavior change, or future-layer scope.

Next Seat: 系统交付席 if approved; main thread/product revision if rejected.
