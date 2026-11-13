# ADR-0004: Project Memory Foundation Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Project Memory Foundation is approved for architecture boundary definition before implementation. The final product goal is AI Company System, but the current launch scope remains AI Task Executor MVP. Project Memory must reduce future context reads by structuring existing project facts without creating agent memory, Employee memory, external vector memory, or new execution behavior.

The protected loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Decision

Project Memory is a deterministic project-fact read model over existing source-of-truth artifacts and execution summary memory. It is not a new persistence layer and does not own facts. It reads, indexes, and summarizes already-owned project evidence so future roles and implementation work can retrieve the smallest relevant context segment.

The first implementation slice should be documentation-backed and deterministic:

- Read existing source-of-truth files.
- Produce compact project-fact segments with source references.
- Keep all generated memory refreshes reviewable.
- Avoid backend persistence, embeddings, external services, autonomous memory writes, and execution-loop changes.

No backend API is required for the first slice unless 系统交付席 documents a read-model gap and receives separate approval.

## Source Boundary

Allowed inputs:

- `knowledge/`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `docs/decisions/`
- `issues/`
- `reviews/`
- Existing execution summary memory from Result Store.

Not allowed as Project Memory sources without separate approval:

- Browser history, private user files, chat transcripts, secrets, external services, or third-party knowledge bases.
- Inferred business facts that are not present in existing source-of-truth files.
- Agent or Employee private preferences.

## Read Model Boundary

Allowed project-fact segments:

- Product identity and current launch scope.
- Active implementation gate and protected execution loop.
- Current sprint, current task, next seat, and open blockers.
- Architecture boundaries and ADR decisions.
- Issue status, completion notes, and handoff state.
- Review evidence and verification commands.
- Forbidden scope and scope-risk reminders.
- Source references back to the owning files.

Not allowed:

- Agent memory or Employee memory.
- Multi-agent coordination state.
- Company organization, departments, ownership graph, or L5 operating model.
- ROI, economy, scoring, prioritization economics, or L6 optimization.
- Vector embeddings, semantic search service, external memory service, or hidden memory store.
- New persistence tables unless separately approved.

## Ownership Boundary

Project Memory must not replace source-of-truth ownership:

- `knowledge/` remains the low-token context layer.
- `PROJECT_STATUS.md` remains the sprint snapshot.
- `TASKS.md` remains the task queue.
- `docs/decisions/` remains the architecture decision record.
- `issues/` remains the executable work queue.
- `reviews/` remains evidence and verification record.
- Execution summary memory remains execution evidence, not product or architecture authority.

Project Memory may reference these files, but corrections must be made in the owning source first.

## Refresh Boundary

Allowed refresh points:

- After issue completion.
- After quality verification.
- After product acceptance.
- After sprint status changes.

Refresh rules:

- Refresh output must be deterministic from existing files or execution summaries.
- Refresh output must include source references.
- Refresh output must be reviewable before it becomes authoritative context for future work.
- Automated code or architecture changes are not allowed.

## Execution Boundary

Project Memory must not:

- Trigger tasks or tools.
- Change orchestration, workflow generation, tool routing, tool execution, learning, meta-development, evolution-governor behavior, or storage semantics.
- Write to Result Store unless a separate approved issue defines a read-model gap and persistence scope.
- Apply evolution proposals or modify code.

## First Implementation Recommendation

The next implementation issue should start with a local deterministic helper or generated documentation artifact, not a backend database:

- Input: selected project source-of-truth files.
- Output: compact Project Memory segments with source paths.
- Verification: deterministic output, source reference coverage, forbidden-scope scan, and no backend persistence changes.

If implementation proves a read API is necessary, the issue must stop and route back for approval before backend work.

## Verification Planning Boundary

质量运行席 should plan verification around:

- No backend persistence changes.
- No embeddings, vector database, external memory service, or hidden memory store.
- Source references point to existing source-of-truth files.
- Project Memory does not replace `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, ADRs, issues, or reviews.
- Scope drift scan covers forbidden memory and future-layer terms.
- Any future implementation remains inside AI Task Executor MVP and preserves the Tool System v1.8 loop.

## Consequences

Positive:

- Future work can retrieve smaller project context segments.
- Source-of-truth ownership remains intact.
- The AI Task Executor MVP gains memory structure without introducing L5/L6 behavior.

Trade-offs:

- No semantic search or embeddings in the foundation slice.
- Memory freshness depends on issue, review, and status files staying current.
- Any stronger read API must be justified later as a separate read-model gap.
