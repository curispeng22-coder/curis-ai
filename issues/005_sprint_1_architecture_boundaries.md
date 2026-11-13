# Issue: Sprint 1 Architecture Boundaries

## Owner

系统交付席

## Context

Sprint 1 - 公司运行可视化 is approved by 总控决策席 for architecture boundary definition only.

Current gate: Curis Workspace Tool System v1.8.

Protected loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Scope

Define architecture boundaries for Sprint 1 visualization before UI implementation.

Allowed boundary areas:

- Read-only visualization data sources.
- Frontend containment boundaries.
- Backend API/read-model boundaries.
- Persistence boundaries.
- Verification planning boundaries.
- Product decision routing boundaries.

## Non-Goals

- Do not implement UI.
- Do not add execution behavior.
- Do not add new business domain behavior.
- Do not add new employee-management behavior.
- Do not add a new agent layer.
- Do not add automatic evolution behavior.

## Allowed Files

- `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`
- `docs/sprints/sprint-1-company-visualization.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `reviews/004_sprint_1_architecture_boundaries_review.md`

## Acceptance Criteria

- [x] Sprint 1 visualization is constrained to existing v1.8 execution records.
- [x] Frontend boundary is minimal and read-only except existing task creation/run actions.
- [x] Backend boundary allows only read-only visualization endpoints or adapters over existing persisted records.
- [x] Persistence boundary forbids new tables unless a read-model gap is documented and approved.
- [x] No new execution behavior is introduced.
- [x] Product open questions are either routed or reduced to architecture recommendations.
- [x] Verification handoff is ready for 质量运行席.

## Verification

- Read back changed source-of-truth files.
- Scope drift scan over changed files for forbidden implementation terms.

## Completion Notes

Completed by 系统交付席 on 2026-07-06.

Evidence: `reviews/004_sprint_1_architecture_boundaries_review.md`.

Next Seat: 质量运行席.
