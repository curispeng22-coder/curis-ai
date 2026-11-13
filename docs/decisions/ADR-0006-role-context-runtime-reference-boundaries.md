# ADR-0006: Role Context Runtime Reference Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Sprint 3 role profiles are implemented in `knowledge/ROLE_PROFILES.md` as deterministic source-controlled guidance. The role-context runtime reference gate is approved for architecture boundary definition only. Runtime implementation remains blocked.

The protected loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Decision

A future role-context runtime reference may be considered only as a read-only context reference from an approved role profile into an existing prompt/context boundary. It must not become execution routing, role selection logic, persistence, UI, task evidence attachment, Employee expansion, agent abstraction, or company organization.

No runtime implementation is approved by this ADR.

## Allowed Future Reference Shape

If a separate implementation issue is approved later, the smallest allowed shape is:

- Input: a stable profile id that points to `knowledge/ROLE_PROFILES.md`.
- Lookup: deterministic read-only lookup of the matching source-controlled role profile.
- Output: a compact role-context excerpt containing only role intent, responsibility boundary, expected output shape, escalation triggers, and source references.
- Scope: prompt/context guidance only.
- Failure behavior: if the profile id is missing or invalid, stop or omit role context according to the approved issue; do not infer or create a role.

## First Runtime Slice Recommendation

The first runtime slice, if approved later, should use an explicit issue-declared profile id. It should not use an implicit default profile.

Reason:

- Explicit issue declaration is reviewable in source control.
- It avoids hidden role selection behavior.
- It avoids backend metadata, persistence, task-role association, and UI selector scope.
- It preserves source-of-truth ownership because profile choice is visible in the owning issue.

If no issue-declared profile id exists, the future runtime must proceed without role context unless a separate product decision approves a defaulting rule.

## Execution Boundary

Role context must not:

- select tools,
- route work,
- create or select agents,
- create employees,
- mutate workflow steps,
- change task state,
- trigger tasks,
- alter learning, meta-development, or evolution-governor behavior,
- change fallback behavior,
- change API semantics,
- change storage behavior.

Role context may only describe responsibility and output expectations. It cannot decide or enforce execution.

## Source Boundary

Allowed sources:

- `knowledge/ROLE_PROFILES.md`
- `knowledge/PROJECT_MEMORY.md` only by source reference when relevant
- the approved implementation issue that declares the profile id
- existing architecture and review records by source reference

Role context must not duplicate full project history. Corrections must happen in the owning source first.

## Persistence Boundary

No backend metadata, persistence, new tables, task-role association, or execution record attachment is approved.

Any future implementation must be read-only over source-controlled artifacts unless a separate approved metadata gap exists.

## UI Boundary

No role selector, role dashboard, role-management UI, or display surface is approved.

Any future UI work requires a separate product and architecture gate.

## Verification Evidence Required Before Future Runtime Implementation

Before runtime prompt integration may be implemented, a future issue must define evidence for:

- deterministic profile id lookup from `knowledge/ROLE_PROFILES.md`,
- exact compact context excerpt shape,
- context-size reduction compared with repeating full role prompts,
- no backend/frontend drift outside approved files,
- no persistence, task-role association, or task evidence attachment,
- no new tool selection, routing, workflow mutation, state mutation, or execution-loop behavior,
- fallback behavior for missing or invalid profile id,
- forbidden-scope scan over implementation and source-of-truth files.

## Forbidden Scope

This ADR does not approve:

- runtime implementation,
- runtime prompt integration,
- task evidence attachment,
- UI selector or dashboard,
- backend metadata, persistence, new tables, or task-role association,
- Employee CRUD or employee expansion,
- company organization, departments, reporting lines, staffing, or ownership model,
- multi-agent routing,
- agent abstraction layer,
- ROI, cost, compensation, scoring, or economy model,
- new execution behavior,
- automatic evolution behavior,
- vector database, embeddings, external role service, or external memory service.

## Consequences

Positive:

- Role profiles can later reduce repeated prompt context without creating hidden routing or persistence.
- Explicit issue-declared profile ids keep future runtime references reviewable.
- Current AI Task Executor MVP and Tool System v1.8 boundaries remain unchanged.

Trade-offs:

- No runtime behavior changes are available until a separate implementation issue is approved.
- No default profile behavior is available without a product decision.
- No task evidence or UI surface will show role context in this boundary.
