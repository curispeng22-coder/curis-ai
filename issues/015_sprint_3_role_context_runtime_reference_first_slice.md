# Issue: Sprint 3 Role Context Runtime Reference First Slice

## Owner

系统交付席

## Context

Sprint 3 role-context runtime reference architecture-boundary verification planning was accepted by 产品规划席 on 2026-07-06.

Role profiles are deterministic source-controlled guidance in `knowledge/ROLE_PROFILES.md`.

The current launch scope remains AI Task Executor MVP under Tool System v1.8.

This issue approves only the smallest first implementation slice for read-only role-context reference. It does not approve role selection, routing, persistence, UI, task evidence attachment, Employee expansion, company organization, or execution behavior changes.

## Explicit Profile ID For First Slice

`curis.role.system-delivery.v1`

This profile id is declared only for this first slice's deterministic implementation and verification evidence. It must not become an implicit runtime default. If an execution path has no explicitly approved profile id, it must omit role context.

## Objective

Implement a minimal deterministic role-context reference that can produce a compact prompt/context excerpt from the explicitly declared profile id.

## Scope To Implement

- Deterministic read-only lookup from `knowledge/ROLE_PROFILES.md`.
- Compact role-context excerpt containing only:
  - role intent,
  - responsibility boundary,
  - expected output shape,
  - escalation triggers,
  - source references.
- Missing or invalid profile id fallback that omits role context or stops according to the narrowest safe implementation choice.
- Verification evidence for deterministic lookup, compact context excerpt shape, context-size reduction versus repeating the full profile, and forbidden-scope scans.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Company organization, departments, reporting lines, staffing, or ownership model.
- Multi-agent routing.
- Agent abstraction layer.
- Autonomous role creation or role selection.
- UI selector, role dashboard, or role-management UI.
- Backend metadata, persistence, new tables, or task-role association.
- Task evidence attachment.
- Tool selection, routing, workflow mutation, task-state mutation, or execution-loop behavior change.
- API semantic changes unless 系统交付席 documents a blocking gap and routes it back for approval first.
- Automatic evolution behavior.
- Vector database, embeddings, external role service, or external memory service.

## Acceptance Criteria

- [x] Implementation uses the explicit profile id declared in this issue; no implicit default role is introduced.
- [x] Role context is read-only prompt/context guidance only.
- [x] No backend persistence, new tables, task-role association, task evidence attachment, UI selector, role dashboard, or Employee expansion is added.
- [x] No tool routing, workflow generation, task state, learning, meta-development, evolution governor, or storage behavior changes.
- [x] Compact context evidence is shorter than repeating the full role profile.
- [x] Missing or invalid profile id behavior is deterministic and does not infer or create a role.
- [x] Delivery evidence is recorded in `reviews/014_role_context_runtime_reference_first_slice_review.md`.
- [x] `knowledge/CURRENT_CONTEXT.md`, `PROJECT_STATUS.md`, `TASKS.md`, and `knowledge/PROJECT_MEMORY.md` are updated after delivery.

## Evidence To Review

- `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`
- `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`
- `knowledge/ROLE_PROFILES.md`
- `knowledge/CURRENT_CONTEXT.md`

## Handoff

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload sent on 2026-07-06:

- Objective: implement minimal read-only role-context reference first slice.
- Explicit profile id: `curis.role.system-delivery.v1`.
- Evidence: `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`.
- Product acceptance commit: `166538e`.
- Next seat after delivery: 质量运行席.

## Completion Notes

Delivery: completed by 系统交付席 on 2026-07-06.

Implemented:

- Added `backend/app/role_context.py` with deterministic read-only profile lookup and compact role-context excerpt generation.
- Added `backend/tests/test_role_context.py` covering explicit profile lookup, missing profile id behavior, and invalid profile id behavior.
- The first slice uses explicit profile id `curis.role.system-delivery.v1` and does not introduce an implicit default role.

Verification performed:

- TDD red check: `python3 -m unittest tests.test_role_context` failed before implementation with missing `app.role_context`.
- Focused role-context tests.
- Backend regression tests.
- Deterministic lookup and context-size evidence.
- `git diff --check`.
- Forbidden-scope scan.

Handoff: sent to 质量运行席.

Quality and product acceptance:

- 质量运行席 verified the first slice against commit `71e9577b`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 产品规划席 accepted the first slice on 2026-07-06.
- Product constraint: any future runtime caller must be constrained by a separately approved issue-declared profile id; no implicit default role is approved.
