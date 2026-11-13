# Sprint 2 Unified Task Console Architecture Boundaries Review

Date: 2026-07-06

Reviewer seat: 系统交付席

Source issue: `issues/008_sprint_2_unified_task_console_gate.md`

Architecture record: `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`

## Verdict

Boundary status: READY FOR 质量运行席 verification planning.

Blockers: None.

## Boundary Summary

- Sprint 2 is a frontend composition boundary over existing task composer, task history, run action, selected task state, and accepted Sprint 1 selected-task detail.
- The first implementation slice should include composer, compact history, existing run action, selected detail, and minimal review signals derived from existing state.
- Backend changes are not allowed for the first implementation slice because current APIs already expose task, workflow, trace, meta-development, and evolution-decision evidence.
- Any future read-model gap must be documented and approved before backend work.
- Status filters and local presentation preferences are deferred unless they remain purely local UI state and do not create complex UI.

## Preserved Boundaries

- Tool System v1.8 loop remains unchanged.
- Accepted Sprint 1 selected-task detail remains the evidence anchor.
- Existing Task API, Run API, Status API, History API, workflow, trace, meta-development, and evolution-decision APIs remain the source of truth.
- Rerun, if implemented, must call the existing Run API only.
- Review signals must be derived from existing task, workflow, trace, meta-development, and evolution-decision records.

## Forbidden Scope Check

- No ROI.
- No business modules.
- No Employee CRUD or employee expansion.
- No multi-agent behavior.
- No agent abstraction layer.
- No complex UI.
- No new execution behavior.
- No automatic evolution behavior.
- No new persistence tables without an approved read-model gap.

## Verification Evidence

| Area | Command / Evidence | Result |
| --- | --- | --- |
| Source issue reviewed | `issues/008_sprint_2_unified_task_console_gate.md` | PASS: Sprint 2 gate approved for architecture boundary definition. |
| Architecture context reviewed | `knowledge/003_Architecture.md` and Sprint 1 ADR | PASS: v1.8 loop and Sprint 1 selected-task detail boundary preserved. |
| Sprint 2 PRD reviewed | `docs/sprints/sprint-2-unified-task-console.md` | PASS: boundary follows recommended first slice and non-goals. |
| API surface checked | Route scan in `backend/app/main.py` and frontend API usage | PASS: existing APIs cover first-slice read/control needs. |
| Documentation evidence | `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md` | PASS: boundary record created. |

## Verification Planning Recommendation

质量运行席 should verify:

- ADR-0003 preserves Tool System v1.8 and accepted Sprint 1 selected-task detail.
- No backend implementation is required before the first Sprint 2 slice.
- Future implementation verification should require frontend tests, frontend lint/build, scope drift scan, and manual UI evidence.
- Any backend file change in Sprint 2 implementation should be blocked unless a read-model gap is approved first.

## Quality Verification Planning

Reviewer seat: 质量运行席

Planning status: PASS.

Blockers: None.

Architecture commit verified: `e801da4`.

Quality evidence performed:

| Area | Command / Evidence | Result |
| --- | --- | --- |
| Architecture commit boundary | `git show --name-only --oneline e801da4` | PASS: commit changed docs, issue/review, project status, task queue, and knowledge files only; no backend or frontend implementation files changed. |
| Architecture source review | `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md` | PASS: preserves Tool System v1.8 loop and accepted Sprint 1 selected-task detail boundary. |
| Issue/review source review | `issues/008_sprint_2_unified_task_console_gate.md` and this review | PASS: first slice is limited to composer, compact history, existing run action, selected detail, and minimal review signals derived from existing state. |
| Implementation scope drift scan | `rg -n "ROI|business module|agent abstraction|multi-agent|Employee CRUD|employee-management|mock data|simulation mode|uncontrolled architecture|automatic evolution" backend/app backend/tests frontend/app` | PASS: no matches. |
| Source-of-truth guardrail scan | `rg -n "ROI|business module|agent abstraction|multi-agent|Employee CRUD|employee-management|mock data|simulation mode|uncontrolled architecture|automatic evolution|new execution behavior|new persistence" docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md reviews/007_sprint_2_architecture_boundaries_review.md issues/008_sprint_2_unified_task_console_gate.md` | PASS: matches are boundary/guardrail statements only. |

Required verification for Sprint 2 first implementation slice:

- Confirm no backend files changed. If backend files changed, block unless an approved read-model gap exists.
- Run frontend tests for review-signal derivation and console state helpers.
- Run `cd frontend && pnpm lint`.
- Run `cd frontend && pnpm build`.
- Run the scope drift scan over `backend/app`, `backend/tests`, and `frontend/app`.
- Capture manual UI evidence showing task composer, compact history, existing run action, selected task detail, and review signals derived from existing persisted state.
- If any backend read adapter is separately approved, run `cd backend && .venv/bin/python -m unittest discover -s tests` and API evidence for task status/history/workflow/trace/meta-development/evolution decisions.

Quality conclusion:

- Sprint 2 architecture-boundary verification planning is ready for 产品规划席 acceptance.
- No backend change, new execution behavior, business module, employee-management behavior, agent abstraction, complex UI, automatic evolution behavior, or unapproved persistence is authorized by the boundary plan.

## Product Acceptance

Reviewer seat: 产品规划席

Decision: ACCEPTED on 2026-07-06.

Rationale:

- The verification plan preserves Tool System v1.8 and the accepted Sprint 1 selected-task detail boundary.
- The first implementation slice is correctly limited to composer, compact history, existing run action, selected detail, and minimal review signals derived from existing state.
- Backend changes are blocked unless an approved read-model gap is documented first.
- Status filters and local presentation preferences remain deferred.

Next implementation issue:

- `issues/009_sprint_2_unified_task_console_first_slice.md`

## Known Gaps

- No implementation has started.
- Status filters and local presentation preferences are intentionally deferred from the first slice unless 产品规划席 explicitly promotes them.

## Handoff

Handoff: sent to 产品规划席

Payload:

Issue: `issues/008_sprint_2_unified_task_console_gate.md`

Objective: Accept or revise Sprint 2 unified task console architecture-boundary verification plan before implementation.

Special Constraints: Quality verification planning passed. Preserve Tool System v1.8 loop and accepted Sprint 1 selected-task detail boundary. First slice is composer, compact history, existing run action, selected detail, and minimal review signals derived from existing state. Backend changes are blocked unless an approved read-model gap is documented first.

Next Seat: 产品规划席.

Handoff status: sent to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.

## Product Handoff

Handoff: sent to 系统交付席

Payload:

Issue: `issues/009_sprint_2_unified_task_console_first_slice.md`

Objective: Implement Sprint 2 unified task console first slice.

Special Constraints: Preserve Tool System v1.8 loop and accepted Sprint 1 selected-task detail boundary. First slice is existing task composer, compact task history, existing run action, selected detail, and minimal review signals derived from existing state. Backend changes are blocked unless an approved read-model gap is documented first. Status filters and local presentation preferences remain deferred.

Next Seat: 质量运行席 after implementation evidence is ready.
