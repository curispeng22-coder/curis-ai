# Sprint 2 Follow-up - Project Memory Foundation

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`; verification planning accepted by 产品规划席 on 2026-07-06.

Implementation status: first slice accepted by 产品规划席 on 2026-07-06.

## Product Goal

Add a Project Memory foundation for the AI Task Executor MVP so Curis can remember project facts, decisions, sprint history, architecture boundaries, issue outcomes, and review evidence without rereading the whole repository.

This is a framework step toward the final AI Company System, but it remains inside the current AI Task Executor MVP gate.

## Product Definition

Project Memory is a structured project-fact memory layer.

It is not:

- Agent memory.
- Employee memory.
- Multi-agent coordination.
- Vector database or embedding system.
- Business knowledge base.
- Company organization layer.
- ROI or economic optimization layer.

## Layer Fit

Project Memory supports current L0-L4 execution work:

- L0: show concise project facts in the operating console later.
- L1: remember task and execution facts.
- L2: give the minimal AI Employee coordinator relevant project facts only when needed.
- L3: preserve tool and execution evidence.
- L4: preserve workflow and decision history.

It must not implement L5 company organization or L6 economy/ROI.

## Scope

Allowed product scope:

- Define Project Memory sources from existing facts:
  - `knowledge/`
  - `PROJECT_STATUS.md`
  - `TASKS.md`
  - `docs/decisions/`
  - `issues/`
  - `reviews/`
  - existing execution summary memory from Result Store.
- Define a minimal Project Memory read model.
- Define how Project Memory is refreshed after issue completion or sprint completion.
- Define how roles read only the relevant memory segment to reduce token usage.
- Define the boundary between Project Memory and Execution Memory.

## First Slice Recommendation

Start with architecture boundary definition only.

Recommended implementation later, if approved:

- No new backend persistence.
- No embeddings.
- No external services.
- No autonomous memory writes from agents.
- A deterministic project-memory summary assembled from existing source-of-truth files.
- A compact read API or local helper only if 系统交付席 proves it is necessary.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Complex UI.
- Company CRUD.
- New execution behavior.
- Automatic evolution behavior.
- New persistence tables without a separate approved read-model gap.
- External vector database, embeddings, or third-party memory service.

## Acceptance Criteria

- Project Memory has a clear product definition and source boundary.
- It preserves the AI Task Executor MVP scope.
- It reduces future context reads rather than expanding prompt payloads.
- It uses existing source-of-truth files and execution records as inputs.
- It does not replace `knowledge/`, `issues/`, `reviews/`, ADRs, or `PROJECT_STATUS.md`.
- It does not add L5 company organization or L6 economy/ROI behavior.
- 总控决策席 approves whether this follow-up can enter architecture boundary definition.

## Next Seat

产品规划席 to decide the next Sprint 2 follow-up or Sprint 3 entry.
