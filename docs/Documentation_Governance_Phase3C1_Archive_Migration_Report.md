# Curis Documentation Governance Phase 3-C1 Archive Migration Report

Status: Review

Baseline:
main @ e313322dd234f64ca2463a9b796bc73b471a6e57

Updated:
2026-07-30

---

## 1. Conclusion

Phase 3-C1 completed the approved Safe Move archive migration.

- Assets moved: 200
- Assets deleted: 0
- Delete Candidates processed: 0
- Human-confirmation assets processed: 0
- Business-code changes: 0
- Product-logic changes: 0
- Frontend/backend application-code changes: 0

Moved cohorts:

| Cohort | Count | Destination |
| --- | ---: | --- |
| Deprecated UI V2 | 172 | `docs/99_Archive/design/curis-ui-v2/` |
| CEO Office historical design | 17 | `docs/99_Archive/design/ceo-office/` |
| Standalone diagram prototypes | 7 | `docs/99_Archive/prototypes/diagrams/` |
| Historical Handoff/governance | 4 | `docs/99_Archive/handoff/` |
| Total | 200 | `docs/99_Archive/` |

## 2. Pre-Migration Checks

The Safe Move list was extracted from the complete Archive table in
`docs/Documentation_Governance_Phase3B2_Asset_Report.md`.

Immediately before migration:

- Safe Move rows: 200
- Git-tracked sources: 200
- Existing destinations: 0
- Destination collisions: 0
- External Markdown incoming references: 0
- Script/config incoming references: 0
- AGENTS incoming references: 0
- Internal incoming references from another Phase 3-B2 asset: 0

The outgoing-path audit found 60 unique resolved targets in five source files:

- 46 historical validation-path records in
  `frontend/design-spec/curis-ui-v2/validation-report.json`;
- 2 repository-root path mentions in
  `docs/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md`;
- 12 unique relative targets in three Markdown files.

The validation records and repository-root path mentions retain their original
meaning after migration. Fourteen relative-path occurrences in three moved
Markdown files and nine historical governance references required updates.

## 3. Migration Map

| Original Path | Archive Path |
| --- | --- |
| `diagrams/ui-aicost.html` | `docs/99_Archive/prototypes/diagrams/ui-aicost.html` |
| `diagrams/ui-capability.html` | `docs/99_Archive/prototypes/diagrams/ui-capability.html` |
| `diagrams/ui-finance.html` | `docs/99_Archive/prototypes/diagrams/ui-finance.html` |
| `diagrams/ui-knowledge.html` | `docs/99_Archive/prototypes/diagrams/ui-knowledge.html` |
| `diagrams/ui-report.html` | `docs/99_Archive/prototypes/diagrams/ui-report.html` |
| `diagrams/ui-scope.html` | `docs/99_Archive/prototypes/diagrams/ui-scope.html` |
| `diagrams/ui-workflow.html` | `docs/99_Archive/prototypes/diagrams/ui-workflow.html` |
| `docs/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md` | `docs/99_Archive/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md` |
| `docs/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md` | `docs/99_Archive/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md` |
| `docs/team-v2/BOOTSTRAP_HANDOFFS.md` | `docs/99_Archive/handoff/team-v2/BOOTSTRAP_HANDOFFS.md` |
| `docs/team-v2/HANDOFF_TEMPLATE.md` | `docs/99_Archive/handoff/team-v2/HANDOFF_TEMPLATE.md` |
| `frontend/design-spec/ceo-office/_archive/capability-center-compact-v6.html` | `docs/99_Archive/design/ceo-office/_archive/capability-center-compact-v6.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v2.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v2.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v3.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v3.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v4.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v4.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v5.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v5.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v6.devmode.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v6.devmode.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v6.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v6.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.devmode.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.devmode.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.html` |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.terra.html` | `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.terra.html` |
| `frontend/design-spec/ceo-office/_archive/org-center-compact-v6.html` | `docs/99_Archive/design/ceo-office/_archive/org-center-compact-v6.html` |
| `frontend/design-spec/ceo-office/_archive/org-center.terra.html` | `docs/99_Archive/design/ceo-office/_archive/org-center.terra.html` |
| `frontend/design-spec/ceo-office/_archive/org-spatial-3d.html` | `docs/99_Archive/design/ceo-office/_archive/org-spatial-3d.html` |
| `frontend/design-spec/ceo-office/_archive/outcome-center-compact-v6.html` | `docs/99_Archive/design/ceo-office/_archive/outcome-center-compact-v6.html` |
| `frontend/design-spec/ceo-office/_archive/project-center-compact-v6.html` | `docs/99_Archive/design/ceo-office/_archive/project-center-compact-v6.html` |
| `frontend/design-spec/ceo-office/handoff/capability-center/capability-center.devmode.md` | `docs/99_Archive/design/ceo-office/handoff/capability-center/capability-center.devmode.md` |
| `frontend/design-spec/curis-ui-v2/.preflight/preflight.html` | `docs/99_Archive/design/curis-ui-v2/.preflight/preflight.html` |
| `frontend/design-spec/curis-ui-v2/audit-evidence/company-runtime-1440.png` | `docs/99_Archive/design/curis-ui-v2/audit-evidence/company-runtime-1440.png` |
| `frontend/design-spec/curis-ui-v2/audit-evidence/employee-detail-1440.png` | `docs/99_Archive/design/curis-ui-v2/audit-evidence/employee-detail-1440.png` |
| `frontend/design-spec/curis-ui-v2/audit-evidence/execution-1440.png` | `docs/99_Archive/design/curis-ui-v2/audit-evidence/execution-1440.png` |
| `frontend/design-spec/curis-ui-v2/audit-evidence/settings-1440.png` | `docs/99_Archive/design/curis-ui-v2/audit-evidence/settings-1440.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md` | `docs/99_Archive/design/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-org.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-org.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-workflow.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-workflow.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-active.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-active.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-results.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-results.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-session-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-session-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-agent-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-agent-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-model-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-model-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-skill-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-skill-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-tool-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-tool-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-workflow-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-workflow-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/company-runtime.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/company-runtime.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/decision-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/decision-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/department-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/department-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/department-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/department-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/employee-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/employee-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/employee-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/employee-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution-runs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution-runs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution-tasks.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution-tasks.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-company.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-company.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-entry-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-entry-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-employees.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-employees.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/report-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/report-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/reports.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/reports.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/run-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/run-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-brand.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-brand.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-notify.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-notify.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-profile.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-profile.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/skill-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/skill-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/strategy-room.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/strategy-room.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/task-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/task-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-org.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-org.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-workflow.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-workflow.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-active.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-active.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-results.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-results.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-session-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-session-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-agent-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-agent-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-model-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-model-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-skill-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-skill-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-tool-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-tool-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-workflow-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-workflow-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/company-runtime.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/company-runtime.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/decision-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/decision-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/department-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/department-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/department-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/department-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/employee-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/employee-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/employee-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/employee-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution-runs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution-runs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution-tasks.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution-tasks.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-company.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-company.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-entry-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-entry-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-employees.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-employees.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/report-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/report-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/reports.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/reports.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/run-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/run-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-brand.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-brand.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-notify.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-notify.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-profile.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-profile.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/skill-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/skill-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/strategy-room.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/strategy-room.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/task-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/task-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-org.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-org.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-workflow.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-workflow.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-active.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-active.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-results.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-results.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-session-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-session-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-agent-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-agent-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-model-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-model-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-skill-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-skill-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-tool-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-tool-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-workflow-list.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-workflow-list.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/company-runtime.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/company-runtime.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/decision-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/decision-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/department-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/department-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/department-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/department-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/employee-create.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/employee-create.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/employee-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/employee-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution-runs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution-runs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution-tasks.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution-tasks.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-company.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-company.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-entry-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-entry-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-project.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-project.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-employees.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-employees.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-center.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-center.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-dept.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-dept.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-xhs.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/report-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/report-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/reports.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/reports.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/run-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/run-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-brand.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-brand.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-notify.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-notify.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-profile.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-profile.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/skill-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/skill-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/strategy-room.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/strategy-room.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/task-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/task-detail.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/analytics-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/analytics-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/brainstorm-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/brainstorm-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/capability-center-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/capability-center-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/ceo-home-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/ceo-home-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/company-runtime-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/company-runtime-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/decision-center-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/decision-center-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/department-create-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/department-create-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/employee-create-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/employee-create-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/execution-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/execution-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/knowledge-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/knowledge-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/org-center-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/org-center-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/org-employees-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/org-employees-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-center-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-center-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-dept-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-dept-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-miniapp-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-miniapp-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-xhs-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-xhs-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/reports-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/reports-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/settings-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/settings-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/strategy-room-default.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/strategy-room-default.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-1024.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-1024.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-1440.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-1440.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-390.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-390.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-1024.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-1024.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-1440.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-1440.png` |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-390.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-390.png` |
| `frontend/design-spec/curis-ui-v2/fix-cap-links.mjs` | `docs/99_Archive/design/curis-ui-v2/fix-cap-links.mjs` |
| `frontend/design-spec/curis-ui-v2/fix-placeholders-v3.js` | `docs/99_Archive/design/curis-ui-v2/fix-placeholders-v3.js` |
| `frontend/design-spec/curis-ui-v2/validation-report.json` | `docs/99_Archive/design/curis-ui-v2/validation-report.json` |

All operations used exact source and destination paths through `git mv`.
Relative directory structure is preserved inside each destination cohort.

## 4. Reference Updates

Reference updates: 23 path occurrences across 5 Markdown files.

| Archived File | Updates | Result |
| --- | ---: | --- |
| `docs/99_Archive/handoff/team-v2/BOOTSTRAP_HANDOFFS.md` | 1 | `LEGACY_RULES_AUDIT.md` now points to `docs/team-v2/LEGACY_RULES_AUDIT.md` |
| `docs/99_Archive/design/ceo-office/handoff/capability-center/capability-center.devmode.md` | 1 | The high-fidelity prototype path now points to its retained source path |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md` | 12 | All retained manifest, state, Figma and handoff references now use repository paths |
| `docs/Documentation_Governance_Phase3A_Report.md` | 3 | Historical marked-file entries now use their archive paths |
| `docs/Documentation_Governance_Report.md` | 6 | Exact-duplicate pair records now point to the archived retained copies |

The 46 filename records in the archived validation report are historical
validation evidence, not executable relative links, and remain unchanged.

The Phase 3-B2 Asset Report remains unchanged as the pre-migration analytical
snapshot. Its old paths are intentional historical records, not active links.

## 5. Governance Updates

Updated:

- `docs/00_Context/CURRENT_STATE.md`
- `docs/00_Context/DOCUMENT_INVENTORY.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
- `docs/99_Archive/README.md`

Inventory changes:

- 200 source paths replaced by their archive destinations
- Phase 3-B2 Asset Report added to Inventory
- Phase 3-B2 Migration Plan added to Inventory
- Phase 3-C1 Archive Migration Report added to Inventory
- Inventory total: 1408

## 6. Preserved Boundaries

The following remain at their original paths:

- all Human Confirmation Required assets
- all Delete Candidates
- Release Evidence
- Issue and Review evidence
- WorkBuddy Memory
- current runtime data
- ignored generated state
- frontend/backend application code

No asset was deleted.

## 7. Risks

- Source directories still contain Human Confirmation Required and Delete
  Candidate assets. Directory-level references therefore remain valid but do
  not identify every archived child.
- Old direct paths do not have compatibility copies. Historical lookup must
  use Inventory or this migration map.
- UI V2 and CEO Office are now intentionally split between archived Safe Move
  assets and retained manual-review assets.
- Nine basename-only historical mentions remain unchanged in WorkBuddy Memory
  and a manual-review CEO Office comparison document; Phase 3-C1 does not edit
  those protected assets.
- Static scanning cannot prove dynamically assembled paths, but the fresh
  incoming-reference audit found no executable or Agent consumer.
- Phase 3-C1 does not authorize processing the remaining asset cohorts.

## 8. Validation

- Moved count: PASS — 200 exact rename records
- Cohort counts: PASS — UI V2 172, CEO Office 17, diagrams 7, Handoff 4
- Source absence and destination presence: PASS — 200/200
- Git history/content preservation: PASS — 197 byte-identical moves; 3 moved
  Markdown files changed only for 14 required reference corrections
- Inventory coverage: PASS — 1408 rows and no missing listed path
- Human-confirmation/Delete Candidate preservation: PASS — all 269 protected
  tracked and ignored records remain present
- Active exact old-path references: PASS — none outside the Phase 3-B2
  analytical snapshot and this migration map
- Direct deletions: PASS — 0
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- untracked Migration Report whitespace check: PASS
- Commit required: Yes, after review and explicit commit instruction
