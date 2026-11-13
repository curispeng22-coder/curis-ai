# Issue: Sprint 3 Role Profiles First Slice

## Owner

系统交付席

## Context

Sprint 3 lightweight role and responsibility gate is approved.

Architecture boundaries are defined in `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`.

Quality verification planning passed in `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`.

产品规划席 accepted the architecture-boundary verification plan on 2026-07-06.

## Objective

Implement the smallest Sprint 3 role-profile first slice as deterministic source-controlled execution guidance.

## Scope

Allowed:

- Create a deterministic source-controlled role profile artifact.
- Define compact fixed profiles for the current Curis execution seats only when they help reduce repeated prompt/context payload.
- Each profile must include:
  - stable profile id,
  - role name,
  - role intent,
  - responsibility boundary,
  - minimal context references,
  - expected output shape,
  - escalation triggers,
  - source references.
- Reference Project Memory or source-of-truth files by path rather than duplicating full history.
- Preserve existing source-of-truth ownership.
- Update PMO/status documents and review evidence.

## Non-Goals

- No ROI system.
- No business modules.
- No Employee CRUD or employee expansion.
- No multi-agent system or routing.
- No agent abstraction layer.
- No company organization, departments, reporting lines, staffing, or ownership model.
- No autonomous role creation.
- No role scoring, compensation, cost, ROI, or economy model.
- No role-management dashboard or UI selector.
- No runtime prompt integration.
- No task evidence attachment.
- No backend metadata, persistence, new tables, or task-role association.
- No new execution behavior.
- No automatic evolution behavior.
- No vector database, embeddings, external role service, or external memory service.

## Allowed Files

- `knowledge/ROLE_PROFILES.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`
- `reviews/012_sprint_3_role_profiles_first_slice_review.md`
- `TASKS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`

Backend and frontend implementation files are blocked unless 系统交付席 documents a separate approved gap before changing them.

## Acceptance Criteria

- [x] Role profiles are deterministic and source-controlled.
- [x] Profiles include responsibility boundaries, minimal context references, expected output shape, escalation triggers, and source references.
- [x] Profiles reduce repeated prompt/context payload rather than duplicating full project history.
- [x] Profiles do not replace `AGENTS.md`, `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, ADRs, issues, reviews, or Project Memory.
- [x] No backend/frontend implementation files are changed.
- [x] No Employee CRUD, employee expansion, company organization, multi-agent routing, agent abstraction, ROI/economy, role dashboard, new execution behavior, automatic evolution behavior, unapproved persistence, vector DB/embeddings, external role service, or external memory service is added.
- [x] Deterministic output check passes.
- [x] Source-reference check passes.
- [x] Forbidden-scope scan passes.
- [x] Review evidence is recorded.

## Verification

Required evidence:

```bash
git diff --check
```

Deterministic artifact check:

```bash
sed -n '1,240p' knowledge/ROLE_PROFILES.md > /tmp/curis_role_profiles_check.md
cmp -s knowledge/ROLE_PROFILES.md /tmp/curis_role_profiles_check.md
```

Backend/frontend guard:

```bash
git diff --name-only HEAD -- backend frontend
```

Forbidden-scope scan:

```bash
rg -n "Employee CRUD|employee expansion|company organization|departments|reporting lines|staffing|multi-agent|agent abstraction|ROI|economy|role dashboard|role-management dashboard|runtime prompt integration|task evidence attachment|backend metadata|backend persistence|new persistence|task-role association|new execution behavior|automatic evolution|vector database|embedding|external role service|external memory service|autonomous role" backend/app backend/tests frontend/app knowledge docs/decisions issues reviews
```

## Next Seat

质量运行席 after implementation evidence is ready.

## Completion Notes

Delivery: completed by 系统交付席 on 2026-07-06.

Implemented:

- Created deterministic source-controlled role profiles in `knowledge/ROLE_PROFILES.md`.
- Defined five fixed Curis operating-seat profiles with stable profile ids, role intent, responsibility boundaries, minimal context references, expected output shape, escalation triggers, and source references.
- Updated current context, Project Memory, task queue, project status, sprint status, and delivery review evidence.

Verification performed:

- TDD red check failed before implementation because `knowledge/ROLE_PROFILES.md` did not exist.
- `git diff --check`
- Deterministic artifact check for `knowledge/ROLE_PROFILES.md`
- Required field and source-reference scans
- Backend/frontend guard
- Forbidden-scope scan

Handoff: sent to 质量运行席.

Quality and product acceptance:

- 质量运行席 verified Sprint 3 role profiles first slice against commit `53d8a30`.
- Quality status: PASS; no blockers.
- 产品规划席 accepted Sprint 3 role profiles first slice on 2026-07-06.
