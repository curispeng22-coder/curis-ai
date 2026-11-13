# ADR-0014: Local/Demo Verification Automation Boundaries

Date: 2026-07-07

Status: Proposed for quality verification

Related gate: `issues/038_local_demo_verification_automation_gate.md`

Related operator notes: `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`

## Context

AI Task Executor MVP v0.1 is local/demo ready. Operator notes now explain startup, smoke verification, shutdown, rollback, known warning, and evidence references.

Manual smoke verification is still repetitive. The next bounded reliability and operations step is a local-only verification helper that checks the existing local API without changing runtime behavior.

This ADR defines boundaries only. It does not approve implementation.

## Decision

Define Local/Demo Verification Automation as a bounded operational-support phase for the existing AI Task Executor MVP v0.1 local/demo release.

The phase may define and later implement a local-only verification helper that checks:

- Backend health endpoint.
- Task creation through the existing Task API payload `{ content }`.
- Task history through the existing History API.
- Optional human-readable output for local/demo verification evidence.

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

### 1. Local API Smoke Verification

Allowed:

- Check `GET /health`.
- Check `POST /api/task` with existing `{ content }` payload.
- Check `GET /api/tasks`.
- Exit non-zero when expected local API smoke checks fail.
- Print concise local verification evidence.

Not allowed:

- Changing API semantics.
- Adding API endpoints.
- Changing database schema.
- Seeding mock data or replacing real local API calls with simulation.

### 2. Local-Only Operator Helper

Allowed:

- Add a repo-local helper script outside backend/frontend runtime behavior paths.
- Use Python standard-library HTTP calls only unless a separately approved dependency is needed.
- Accept local base URL and task content as optional command-line arguments.
- Keep the helper deterministic and suitable for local/demo verification.

Not allowed:

- Adding backend or frontend runtime dependencies.
- Starting servers automatically.
- Managing secrets.
- Calling external services.
- Running model-provider execution smoke.

### 3. Release Documentation Linkage

Allowed:

- Update operator notes or release runbook to reference the helper.
- Keep manual smoke commands available as fallback.
- Record verification evidence in review files.

Not allowed:

- Claiming hosted production readiness.
- Expanding the release to external channels.
- Adding future AI Company System product layers.

## First Implementation Slice Recommendation

Recommended first slice after quality verification and product acceptance:

`Local/Demo API Smoke Helper`

Scope should be limited to:

- A local helper script under a non-runtime tooling path.
- Documentation reference in operator notes.
- Review evidence proving health, task creation, and task history checks use the real local API.
- No backend/frontend behavior change, API semantic change, persistence/schema change, execution behavior change, external service, mock/simulation substitution, complex UI/dashboard, or future-layer scope.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|automatic evolution behavior change|code self-modification|architecture mutation|unlocking locked modules|external service|task-role association|task evidence attachment|future-layer|mock|simulation" docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md issues/038_local_demo_verification_automation_gate.md issues/039_local_demo_verification_automation_boundaries.md reviews/033_local_demo_verification_automation_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicit forbidden, preserved-scope, or anti-scope text.
- Any mock or simulation match appears only to forbid mock/simulation substitution.

## Consequences

- This ADR does not approve implementation.
- The next seat is 质量运行席 for architecture-boundary verification.
- If accepted, 产品规划席 may open a separate first implementation issue.
- Any helper must remain local-only and must not change AI Task Executor runtime behavior.
- Any backend, frontend, API, persistence, execution, external-service, future-layer, ROI/economy, business-module, Employee, multi-agent, or agent-abstraction work remains blocked.
