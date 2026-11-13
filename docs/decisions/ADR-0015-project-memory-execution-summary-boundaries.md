# ADR-0015: Project Memory Execution Summary Boundaries

Date: 2026-07-07

Status: Proposed for quality verification

Related gate: `issues/041_project_memory_execution_summary_gate.md`

Related Project Memory artifact: `knowledge/PROJECT_MEMORY.md`

## Context

Project Memory currently provides a deterministic project-fact read model over source-of-truth files.

Since v0.1 local/demo release, the project has accumulated accepted release, reliability, operator, and verification evidence. Future Curis seats need a compact execution-summary memory surface that references those sources without rereading every review, issue, and release document.

This ADR defines boundaries only. It does not approve implementation.

## Decision

Define Project Memory Execution Summary as a deterministic, source-referenced memory layer over existing source-of-truth evidence.

The first phase must remain documentation-only unless a later read-model gap is separately approved.

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
- Project Memory source-of-truth ownership.
- Role Profiles, Role Context, release record/tag semantics, and source-of-truth ownership.

## Boundary Areas

### 1. Accepted Execution Evidence Summary

Allowed:

- Summarize accepted evidence for v0.1 release, post-v0.1 reliability, operator notes, and local/demo smoke verification.
- Reference owning source files for each summary claim.
- Keep summary statements deterministic and reviewable.

Not allowed:

- Creating hidden memory.
- Inferring facts without source references.
- Replacing issues, reviews, release docs, ADRs, `PROJECT_STATUS.md`, `TASKS.md`, or `knowledge/CURRENT_CONTEXT.md`.

### 2. Project Memory Integration

Allowed:

- Add a dedicated documentation artifact under `knowledge/`.
- Link it from `knowledge/PROJECT_MEMORY.md`.
- Keep corrections flowing from owning source files into the summary artifact.

Not allowed:

- Backend persistence changes.
- New API/read endpoint.
- Vector DB, embeddings, external memory service, or hidden store.
- Runtime prompt integration.

### 3. Future Read-Model Gap Classification

Allowed:

- Identify future gaps that may require a read-model helper or API.
- Classify gaps as documentation, verification, stabilization, or future product scope.

Not allowed:

- Implementing read APIs or helper code in this phase.
- Adding task evidence attachment, task-role association, agent memory, Employee memory, multi-agent coordination, or agent abstraction.

## First Implementation Slice Recommendation

Recommended first slice after quality verification and product acceptance:

`Project Memory Execution Summary`

Scope should be documentation-only:

- Add `knowledge/EXECUTION_SUMMARY_MEMORY.md`.
- Summarize v0.1 release, post-v0.1 reliability, operator notes, and local/demo verification automation evidence.
- Reference owning source files for every summary section.
- Link the artifact from `knowledge/PROJECT_MEMORY.md`.
- No backend/frontend behavior change, API semantic change, persistence/schema change, vector DB, embeddings, external memory service, hidden memory store, runtime prompt integration, task evidence attachment, agent memory, Employee memory, multi-agent coordination, or future-layer scope.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|automatic evolution behavior change|vector|embedding|external memory|hidden memory|agent memory|Employee memory|runtime prompt|task-role association|task evidence attachment|future-layer" docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md issues/041_project_memory_execution_summary_gate.md issues/042_project_memory_execution_summary_boundaries.md reviews/035_project_memory_execution_summary_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicit forbidden, preserved-scope, or anti-scope text.

## Consequences

- This ADR does not approve implementation.
- The next seat is 质量运行席 for architecture-boundary verification.
- If accepted, 产品规划席 may open a separate documentation-only first implementation issue.
- Any backend, frontend, API, persistence, execution, vector, embedding, external memory, hidden memory, runtime prompt, agent memory, Employee memory, multi-agent, ROI/economy, business-module, company-organization, agent-abstraction, or future-layer work remains blocked.
