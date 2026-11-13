# ADR-0013: Local/Demo Operator Polish Boundaries

Date: 2026-07-06

Status: Proposed for quality verification

Related gate: `issues/035_local_demo_operator_polish_gate.md`

Related release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`

Related reliability closeout: `reviews/030_post_v0_1_execution_reliability_closeout_review.md`

## Context

AI Task Executor MVP v0.1 is closed as the first local/demo version.

Post-v0.1 Execution Reliability is also closed. The current system has accepted evidence for run evidence, workflow fallback/error evidence, and evolution decision evidence.

The next phase should reduce local/demo operation risk without adding product capability. The work should help an operator understand how to start, verify, explain, and recover the existing v0.1 system.

This ADR defines boundaries only. It does not approve implementation.

## Decision

Define Local/Demo Operator Polish as a bounded post-v0.1 phase over release clarity, operator wording, and demo readiness for the existing AI Task Executor MVP.

The phase must preserve:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing execution behavior.
- Existing Evolution Governor behavior.
- Project Memory, Role Profiles, Role Context, release record/tag semantics, and source-of-truth ownership.

## Boundary Areas

### 1. Operator Runbook Clarity

Allowed:

- Clarify local startup, health check, smoke verification, and shutdown wording.
- Clarify known warning handling, especially the FastAPI Python 3.14 warning as `defer-known-gap`.
- Clarify rollback and restore-point wording using existing release records.

Not allowed:

- Changing startup behavior.
- Changing deployment topology.
- Adding external hosting, external channels, or external services.

### 2. Release Notes Clarity

Allowed:

- Summarize what v0.1 can do today.
- Summarize post-v0.1 reliability improvements: run evidence, fallback/error evidence, and evolution decision evidence.
- Distinguish implemented capability from blocked future AI Company System layers.

Not allowed:

- Claiming unsupported features.
- Opening L5 company organization, L6 ROI/economy, business modules, Employee CRUD/expansion, multi-agent routing, or agent abstraction.

### 3. Chinese Console Presentation Polish

Allowed only after separate product acceptance:

- Small wording refinements inside the existing operation console.
- Label clarity that helps local/demo operation.
- No new workflow, new panel, complex dashboard, task type, API field, persistence field, or execution behavior.

Not allowed:

- Complex UI/dashboard.
- New entry channels.
- New task semantics.
- API, backend, persistence, or execution-loop changes.

### 4. Demo Readiness Evidence

Allowed:

- Define a deterministic checklist for local/demo verification.
- Reference existing commands, review files, release records, and evidence maps.
- Classify any gap as stabilization, documentation, verification, or future product scope.

Not allowed:

- Mock/simulation substitution for release evidence.
- Adding telemetry, external monitoring, or model-provider integrations.
- Changing Evolution Governor decisions or automatic evolution behavior.

## First Implementation Slice Recommendation

Recommended first slice after quality verification and product acceptance:

`Local/Demo Operator Release Notes Package`.

Scope should be documentation-only:

- Update or add a concise operator-facing release notes document.
- Include startup, smoke verification, shutdown, rollback, known warning, and evidence-reference sections.
- Summarize the implemented v0.1 capability and post-v0.1 reliability improvements.
- Keep all backend, frontend, API, persistence, execution, external-service, UI/dashboard, and future-layer behavior unchanged.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|automatic evolution behavior change|code self-modification|architecture mutation|unlocking locked modules|external service|task-role association|task evidence attachment|future-layer|mock|simulation" docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md issues/035_local_demo_operator_polish_gate.md issues/036_local_demo_operator_polish_boundaries.md reviews/031_local_demo_operator_polish_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicit forbidden, preserved-scope, or anti-scope text.
- Any mention of simulation appears only to forbid mock/simulation substitution or preserve existing Evolution Governor behavior.

## Consequences

- This ADR does not approve implementation.
- The next seat is 质量运行席 for architecture-boundary verification.
- If accepted, 产品规划席 may open a separate documentation-only first implementation issue.
- Any later UI wording polish must be separately scoped and accepted before implementation.
- Any backend, API, persistence, execution, external-service, future-layer, ROI/economy, business-module, Employee, multi-agent, or agent-abstraction work remains blocked.
