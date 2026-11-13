# Issue: Sprint 2 Project Memory First Slice

## Owner

系统交付席

## Context

Sprint 2 Project Memory Foundation gate is approved.

Architecture boundaries are defined in `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`.

Quality verification planning passed in `reviews/009_project_memory_foundation_architecture_boundaries_review.md`.

产品规划席 accepted the architecture-boundary verification plan on 2026-07-06.

## Objective

Implement the smallest Project Memory first slice as a deterministic project-fact read model.

## Scope

Allowed:

- Read from approved source-of-truth files only:
  - `knowledge/`
  - `PROJECT_STATUS.md`
  - `TASKS.md`
  - `docs/decisions/`
  - `issues/`
  - `reviews/`
  - existing execution summary memory if already available in the current Result Store.
- Produce a compact Project Memory summary or local helper output that references source files.
- Keep the output deterministic and repeatable.
- Preserve existing source-of-truth ownership; corrections must happen in owning files first.
- Update PMO/status documents and review evidence.

## Non-Goals

- No ROI system.
- No business modules.
- No Employee CRUD or employee expansion.
- No multi-agent behavior.
- No agent abstraction layer.
- No complex UI.
- No Company CRUD.
- No L5 company organization.
- No L6 ROI/economy behavior.
- No new execution behavior.
- No automatic evolution behavior.
- No backend persistence.
- No new persistence tables.
- No vector database or embeddings.
- No external memory service.
- No hidden memory store.
- No autonomous memory writes.
- No backend API unless a separately approved read-model gap is documented first.

## Allowed Files

- `knowledge/**`
- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `issues/011_sprint_2_project_memory_first_slice.md`
- `reviews/010_project_memory_first_slice_review.md`
- `TASKS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`

If 系统交付席 needs a local deterministic helper, it may add a narrowly scoped repository script after documenting why a generated documentation artifact alone is insufficient.

Backend and frontend implementation files are blocked unless 系统交付席 documents a read-model gap and routes back for approval before changing them.

## Acceptance Criteria

- [x] Project Memory first slice is deterministic from approved source files.
- [x] Output is compact enough to reduce future context reads.
- [x] Output includes source references back to owning files.
- [x] Project Memory does not replace `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, ADRs, issues, reviews, or Result Store execution evidence.
- [x] No backend persistence, vector database, embeddings, external memory service, hidden memory store, agent memory, Employee memory, multi-agent coordination, L5 company organization, L6 ROI/economy behavior, new execution behavior, or automatic evolution behavior is added.
- [x] Deterministic output check passes.
- [x] Forbidden-scope scan passes.
- [x] Review evidence is recorded.

## Verification

Required evidence:

```bash
git diff --check
```

Forbidden-scope scan:

```bash
rg -n "agent memory|Employee memory|multi-agent|vector database|embedding|external memory|memory service|hidden memory|L5|company organization|L6|ROI|economy|new execution behavior|automatic evolution|backend persistence|new persistence|business module|Employee CRUD|agent abstraction" backend/app backend/tests frontend/app knowledge docs/decisions issues reviews
```

If a helper script is added, 系统交付席 must also provide a deterministic output check command.

## Next Seat

质量运行席 after implementation evidence is ready.

## Completion Notes

Implemented by 系统交付席 on 2026-07-06.

Output:

- `knowledge/PROJECT_MEMORY.md`

Review evidence:

- `reviews/010_project_memory_first_slice_review.md`

Verification:

- `git diff --check`
- Deterministic artifact check with `sed` plus `cmp`
- Source reference check with `rg`
- Forbidden-scope scan over implementation and source-of-truth surfaces
- Backend/frontend guard confirming no backend or frontend implementation files changed

Handoff: sent to 质量运行席 thread `019f33c4-9517-7dd0-814b-d2e323b018f5`.

Quality and product acceptance:

- 质量运行席 verified Project Memory first slice against amended commit `3e44d9c`.
- Quality status: PASS; no blockers.
- 产品规划席 accepted Project Memory first slice on 2026-07-06.
