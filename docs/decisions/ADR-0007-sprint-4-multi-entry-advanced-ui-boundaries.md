# ADR-0007: Sprint 4 Multi-Entry And Advanced UI Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Sprint 3 is closed. Sprint 4 - Multi-Entry And Advanced UI is approved for architecture boundary definition only. The current launch scope remains AI Task Executor MVP under Tool System v1.8.

Sprint 4 may improve how the CEO user starts, reviews, and navigates AI Task Executor work, but it must not add future company/economy layers, external channels, new execution behavior, API semantic changes, persistence, or complex UI.

## Decision

Sprint 4 multi-entry and advanced UI is a bounded operational UI composition layer inside the existing AI Task Executor product shell.

It may define multiple ways to compose or navigate an existing task-entry workflow, but all entries must use existing task creation, run, history, status, selected detail, trace/review evidence, Project Memory, Role Profiles, and Role Context boundaries.

No implementation is approved by this ADR.

## Allowed UI Boundary

Allowed future UI surfaces:

- Existing task composer refinements.
- Bounded task-entry modes that produce ordinary task content for the existing Task API.
- Compact entry affordances for common AI Task Executor intents.
- Navigation between existing task history, selected task detail, execution status, and review signals.
- Read-only references to approved Project Memory, Role Profiles, or Role Context helper outputs only when separately approved and source-referenced.

All UI surfaces must remain inside the existing web product shell.

## Multi-Entry Boundary

Multi-entry means multiple entry affordances for the same current task workflow.

Allowed examples:

- A primary task composer.
- A compact quick-entry composer.
- Bounded intent starters that prefill or structure task content without changing task semantics.
- Navigation affordances that help the user move from entry to existing selected-task detail.

Not allowed:

- External channels.
- Third-party platform entry.
- Role selector or role-management UI.
- Business-module entry.
- New task type with new execution semantics.
- Hidden task routing.
- Persisted entry preferences or backend metadata.

## Advanced UI Boundary

Advanced UI means clearer operational ergonomics, not dashboard expansion.

Allowed:

- Better grouping of task entry, task history, selected detail, and review signals.
- Clearer execution status visibility using existing state.
- Local presentation state when it does not require backend persistence or API changes.
- Frontend-only structure over existing data if the future implementation issue remains narrow.

Not allowed:

- Analytics dashboard.
- Company dashboard.
- Role dashboard.
- Workflow editor.
- Advanced dashboard customization.
- Complex filters requiring backend read-model changes.
- Product-domain or business-domain surfaces.

## API And Persistence Boundary

Sprint 4 first implementation should be frontend-only unless a separate approved gap documents otherwise.

Not approved:

- API semantic changes.
- New API routes.
- Backend metadata.
- New persistence tables.
- Task-role association.
- Task evidence attachment.
- Stored UI preferences.
- New read models.

If a future implementation finds an API or read-model gap, it must stop and route back for approval before changing backend behavior.

## Execution Boundary

Sprint 4 UI must not:

- change task creation semantics,
- trigger new execution paths,
- alter run behavior,
- select tools,
- route work,
- mutate workflow steps,
- change task state semantics,
- alter learning, meta-development, or evolution-governor behavior,
- add automatic evolution behavior.

Existing run actions may remain, but Sprint 4 UI must call only approved existing behavior.

## Source Boundary

Sprint 4 UI may reference:

- existing Task API behavior,
- accepted Sprint 2 task-console boundary,
- Project Memory boundary,
- Role Profiles boundary,
- Role Context boundary,
- current issue, ADR, and review evidence.

It must not replace source-of-truth files or duplicate project history.

## First Implementation Recommendation

The next implementation issue should be a narrow frontend-only first slice:

- Preserve the existing task composer.
- Add bounded entry affordances that only produce ordinary task content.
- Preserve existing run action, task history, selected detail, and review signals.
- Avoid backend/frontend scope beyond the existing product shell.
- Avoid role selectors, dashboards, persistence, and API changes.

Quality evidence should prove no backend changes, no API changes, no persistence, no external channels, no execution-loop drift, and no complex UI expansion.

## Forbidden Scope

This ADR does not approve:

- external entry channels,
- complex UI,
- ROI or economy behavior,
- business modules,
- Employee CRUD or employee expansion,
- company organization, departments, reporting lines, staffing, or ownership model,
- multi-agent routing,
- agent abstraction layer,
- new execution behavior,
- API semantic changes,
- backend metadata, persistence, new tables, or task-role association,
- task evidence attachment,
- runtime prompt integration beyond separately approved role-context helper behavior,
- automatic evolution behavior,
- vector database, embeddings, external role service, or external memory service.

## Consequences

Positive:

- Sprint 4 can improve user entry and operational clarity without expanding the execution kernel.
- First implementation can be verified as frontend-only composition over accepted behavior.
- Existing Sprint 2 and Sprint 3 boundaries remain intact.

Trade-offs:

- No external channels or dashboards are available in this boundary.
- No backend read-model, persistence, or API changes are available without a separate approval.
- Multi-entry is limited to UI affordances over the existing task workflow.
