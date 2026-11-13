# Curis Documentation Governance Phase 3-A Report

Status: Review

Baseline:
main @ 8ac3b814

Updated:
2026-07-30

---

## 1. Conclusion

Phase 3-A completed status-only historical governance.

- Marked Markdown files: 62
- Files moved: 0
- Files renamed: 0
- Files deleted: 0
- Business-code changes: 0
- Product-logic changes: 0

All selected files now contain one standard `Status: Deprecated` line. Existing
historical lifecycle wording remains in the document where applicable.

## 2. Marked Files

### Old UI Proposals — 7

- `frontend/design-spec/curis-ui-v2/Curis_TRAE_UI_交互产品架构审计报告.md`
- `frontend/design-spec/curis-ui-v2/Curis_TRAE_UI_全站交互审计与IA重构方案_2026-07-27.md`
- `frontend/design-spec/curis-ui-v2/SPEC.md`
- `docs/99_Archive/design/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md`
- `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-completion-matrix.md`
- `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-handoff.md`
- `frontend/design-spec/curis-ui-v2/docs/ui/figma/README.md`

### Old Assistant Fixed-Secretary Architecture — 1

- `docs/architecture/curis-assistant-architecture-review.md`

This file describes the pre-runtime page-bound Assistant state. Current
Assistant architecture remains `docs/07_Decisions/ADR-0033-global-assistant-runtime.md`.

### Old Workspace/Admin Architecture — 25

- `PROJECT_HANDOFF.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/00-VISION.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/01-MISSION.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/02-PRODUCT-PHILOSOPHY.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/03-CORE-CONCEPTS.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/04-DESIGN-PRINCIPLES.md`
- `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/05-GLOSSARY.md`
- `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/00-SYSTEM-ARCHITECTURE.md`
- `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/01-DOMAIN-MODEL.md`
- `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/02-CAPABILITY-ARCHITECTURE.md`
- `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/00-PRODUCT-MODULES.md`
- `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/01-BUSINESS-PACKS.md`
- `docs/99_Archive/curis_workspace_blueprint/03-UX/00-INFORMATION-ARCHITECTURE.md`
- `docs/99_Archive/curis_workspace_blueprint/03-UX/01-USER-FLOWS.md`
- `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/00-MVP-SCOPE.md`
- `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/01-SPRINT-PLAN.md`
- `curis_workspace_blueprint/ADR/ADR-001-EMPLOYEE-BEFORE-MODEL.md`
- `curis_workspace_blueprint/ADR/ADR-002-CAPABILITY-PROVIDER-NOT-REBUILD.md`
- `docs/99_Archive/curis_workspace_blueprint/README.md`
- `docs/99_Archive/curis_workspace_blueprint/RESEARCH/00-REFERENCE-PRODUCTS.md`
- `docs/99_Archive/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md`
- `docs/99_Archive/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md`
- `docs/product/curis-product-vision-current-stage.md`
- `knowledge/003_Architecture.md`
- `knowledge/005_Key_Decisions.md`

### Superseded Development Processes — 24

- `PROJECT_STATUS.md`
- `TASKS.md`
- `docs/pmo/archive/PROJECT_STATUS_HISTORY_2026-07-12.md`
- `docs/pmo/archive/TASKS_HISTORY_2026-07-12.md`
- `docs/pmo/current-status.md`
- `docs/sprints/ai-task-executor-mvp-readiness.md`
- `docs/sprints/ai-task-executor-mvp-release-candidate.md`
- `docs/sprints/mvp-implementation.md`
- `docs/sprints/post-v0.1-execution-reliability.md`
- `docs/sprints/sprint-0-organization-review.md`
- `docs/sprints/sprint-1-company-visualization.md`
- `docs/sprints/sprint-2-project-memory-foundation.md`
- `docs/sprints/sprint-2-unified-task-console.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`
- `docs/sprints/sprint-3-role-context-runtime-reference.md`
- `docs/sprints/sprint-4-multi-entry-advanced-ui.md`
- `docs/sprints/sprint-workflow.md`
- `docs/sprints/tool-system-v1.6-meta-development.md`
- `docs/sprints/tool-system-v1.8-controlled-self-evolution.md`
- `knowledge/001_Project_History.md`
- `knowledge/004_Workflow.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/NOW.md`
- `knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md`

### Historical Prototype / Demo Documents — 5

- `docs/demo/phase3-demo-script.md`
- `docs/demo/phase4-ai-employee-demo-script.md`
- `docs/demo/phase5-g2-credential-vault-demo-script.md`
- `docs/demo/phase6-workflow-mvp-demo-script.md`
- `docs/demo/phase7-stable-demo-script.md`

## 3. Archive Governance

Created:

- `docs/99_Archive/README.md`

It defines Archive purpose, authority boundaries, reference checks and query
methods. It does not move any file.

## 4. Unprocessed Risks

- 16 WorkBuddy Memory Markdown files remain untouched because they may be tool
  state rather than ordinary project documentation.
- 29 Release Markdown files retain their historical lifecycle wording pending a
  separate evidence-retention policy.
- 354 Deprecated non-Markdown assets cannot safely receive a Markdown Status
  line. These include HTML prototypes, images, design sources and support
  assets.
- Review-classified legacy documents may still contain stale statements; they
  require content-specific confirmation before status changes.
- Repository references have not yet been audited for physical migration.
- Exact duplicate binary design exports remain in place.

## 5. Next-Stage Recommendation

If Phase 3-B is approved:

1. Start with one coherent domain only.
2. Audit all repository references before moving anything.
3. Use the 17 non-ADR Markdown files in `curis_workspace_blueprint/` as the
   first migration pilot. Keep the two ADR decision records at their original
   paths.
4. Record old and new paths.
5. Verify scripts, CI, tests and documentation links.
6. Stop before the next domain and request confirmation.

Phase 3-B had not started when this Phase 3-A report was produced. Phase 3-B1
later completed; see
`docs/Documentation_Governance_Phase3B1_Migration_Report.md`.
