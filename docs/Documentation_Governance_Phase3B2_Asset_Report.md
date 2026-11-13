# Curis Documentation Governance Phase 3-B2 Asset Report

Status: Review

Baseline:
main @ 75a9ce13e2653c8d94f8c9f8243c223d891577d7

Updated:
2026-07-30

---

## 1. Conclusion

Phase 3-B2 completed the historical asset analysis only.

- Files moved: 0
- Files deleted: 0
- Business-code changes: 0
- Product-logic changes: 0
- Git-tracked asset records: 425
- Ignored/generated location records: 44
- Total inventory records: 469

The tracked inventory includes all 144 HTML files, all 191 PNG files, all
Deprecated non-Markdown support assets, WorkBuddy Memory, Release Evidence,
Demo assets, Handoff records and tracked generated outputs in the approved
scope. No tracked JPG, JPEG or SVG asset exists in this scope.

## 2. Scan Method

The scan used the repository at the declared baseline and combined:

1. all non-Markdown rows marked `Deprecated` in
   `docs/00_Context/DOCUMENT_INVENTORY.md`;
2. all Git-tracked HTML, PNG, JPG, JPEG and SVG files;
3. all Git-tracked files under `.workbuddy/`, `docs/release/` and
   `docs/demo/`;
4. all Git-tracked paths containing `handoff`;
5. tracked paths identifiable as export, generated output, build output or
   build metadata;
6. top-level ignored locations returned by `git status --ignored --short`.

Tracked-file size is the logical filesystem size. Ignored-directory size is
the current `du -sk` disk usage. Reference analysis checks:

- exact repository-relative path mentions;
- relative Markdown/HTML/CSS/script path references that resolve to a tracked
  asset;
- Markdown referrers;
- script/config referrers;
- AGENTS referrers;
- references from another asset inside the same historical cohort.

Governance inventories and previous Documentation Governance reports are not
counted as operational references. Their purpose is to list assets, not consume
them.

## 3. Classification Summary

### 3.1 Git-Tracked Assets

| Classification | Count | Size | Meaning |
| --- | ---: | ---: | --- |
| Keep | 40 | 460.7 KiB | Evidence, Issue/Review record or decision provenance |
| Archive | 377 | 24.2 MiB | Historical material retained outside current authority |
| Delete Candidate | 8 | 881.9 KiB | Reproducible or byte-identical redundant tracked output |
| Total | 425 | 25.5 MiB | Complete tracked Phase 3-B2 scope |

### 3.2 Ignored/Generated Locations

| Classification | Records | Size | Meaning |
| --- | ---: | ---: | --- |
| Keep | 10 | 3,607.5 MiB | Protected runtime, data, worktree or sensitive local state |
| Archive | 1 | 15.7 MiB | Historical local release bundle |
| Delete Candidate | 33 | 2,687.4 MiB | Regenerable cache, dependency, log or temporary residue |
| Total | 44 | 6,310.6 MiB | Location-level inventory; directories are not counted as files |

### 3.3 Combined Governance Result

| Classification | Records |
| --- | ---: |
| Keep | 50 |
| Archive | 378 |
| Delete Candidate | 41 |
| Total | 469 |

### 3.4 Asset Types

| Type | Count |
| --- | ---: |
| HTML Prototype | 144 |
| PNG Design Export | 189 |
| PNG Evidence | 2 |
| JPG/JPEG Design Export | 0 |
| SVG Design Export | 0 |
| WorkBuddy Memory | 16 |
| Release Evidence | 29 |
| Handoff Document | 18 |
| Demo Document | 5 |
| JSON Demo/Support | 9 |
| Export Manifest/Support | 1 |
| Prototype CSS | 4 |
| Prototype Script | 6 |
| Design Source | 1 |
| Generated Build Metadata | 1 |
| Total | 425 |

## 4. Reference Audit

Reference notation used below:

- `M`: Markdown referrer count
- `S`: script/config referrer count
- `A`: AGENTS referrer count
- `I`: internal referrer count from another asset in this historical scope

Results:

- Assets with at least one direct or resolved reference: 199
- Markdown reference edges: 302
- Script/config reference edges: 3
- AGENTS reference edges: 0
- Internal historical-package reference edges: 1,550
- Safe-move records: 200
- Human-confirmation records: 184 tracked plus 34 ignored locations
- Forbidden-move records: 41 tracked plus 10 ignored locations

Two tracked assets have external script/config consumers:

- `docs/release/model-gateway-local-demo-first-version-release-record.md`
  is referenced by `frontend/app/taskViewModel.mjs` and its test.
- `frontend/ceo-evidence/index.html` is referenced by
  `frontend/ceo-evidence/tailwind.config.ts`.

No AGENTS file references a Phase 3-B2 tracked asset directly.

### Directory-Level References

| Directory | Referrer Count | Referrers |
| --- | ---: | --- |
| `frontend/design-spec/curis-ui-v2/` | 2 | `docs/03_Design/Curis_Design_System.md`<br>`frontend/docs/ceo-ui-v2-system-design.md` |
| `frontend/design-spec/ceo-office/` | 3 | `docs/03_Design/Curis_Design_System.md`<br>`frontend/design-spec/UI规范交付模板.md`<br>`frontend/design-spec/ceo-office/TRAE_vs_UI_Designer_对比.md` |
| `diagrams/` | 6 | `.workbuddy/memory/2026-07-07.md`<br>`.workbuddy/memory/2026-07-08.md`<br>`docs/03_Design/Curis_Design_System.md`<br>`docs/pmo/source-control-baseline-freeze.md`<br>`frontend/design-spec/ceo-office/UI_设计与布局规范.md`<br>`shared/pmo/PROJECT_SPACE_MAP.md` |
| `docs/release/` | 64 | `.workbuddy/memory/2026-07-09.md`<br>`docs/00_Context/DOCUMENT_MIGRATION_PLAN.md`<br>`docs/contracts/ai-company-template-system.md`<br>`docs/contracts/workflow-runtime-contract.md`<br>`docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`<br>`docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`<br>`docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`<br>`docs/demo/phase7-stable-demo-script.md`<br>`docs/deployment/new-api-local.md`<br>`docs/pmo/archive/PROJECT_STATUS_HISTORY_2026-07-12.md`<br>`docs/pmo/archive/TASKS_HISTORY_2026-07-12.md`<br>`docs/pmo/source-control-baseline-freeze.md`<br>`docs/release/admin-ai-company-asset-foundation.md`<br>`docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`<br>`docs/release/ai-task-executor-mvp-v0.1-release-record.md`<br>`docs/release/ai-task-executor-mvp-v0.1.md`<br>`docs/release/model-gateway-local-demo-first-version-release-record.md`<br>`docs/release/phase1b-gate-assessment.md`<br>`docs/release/phase3-demo-freeze-report.md`<br>`docs/release/phase4-ai-employee-demo-freeze-report.md`<br>`docs/release/phase45-workspace-demo-review-roadmap.md`<br>`docs/release/phase5-g2-credential-vault-demo-freeze-report.md`<br>`docs/release/phase5-g2-credential-vault-rc.md`<br>`docs/release/phase55-post-g2-roadmap-review.md`<br>`docs/release/phase6-workflow-mvp-demo-freeze-report.md`<br>`docs/release/phase6-workflow-mvp-implementation-report.md`<br>`docs/release/phase6-workflow-mvp-rc.md`<br>`docs/release/phase65-post-workflow-roadmap-review.md`<br>`docs/release/phase7-demo-polish-commercial-readiness.md`<br>`docs/release/phase8-workspace-billing-support-implementation-report.md`<br>`docs/release/phase9a-commercial-configuration-status.md`<br>`docs/sprints/ai-task-executor-mvp-release-candidate.md`<br>`docs/sprints/post-v0.1-execution-reliability.md`<br>`frontend/app/taskViewModel.mjs`<br>`frontend/app/taskViewModel.test.mjs`<br>`issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`<br>`issues/023_ai_task_executor_mvp_local_demo_release_verification.md`<br>`issues/024_ai_task_executor_mvp_v0_1_release_closeout.md`<br>`issues/025_post_v0_1_execution_reliability_gate.md`<br>`issues/026_post_v0_1_execution_reliability_boundaries.md`<br>`issues/037_local_demo_operator_release_notes_package.md`<br>`issues/040_local_demo_api_smoke_helper.md`<br>`issues/075_model_gateway_local_demo_release_candidate_gate.md`<br>`issues/076_model_gateway_post_rc_next_phase_gate.md`<br>`issues/077_post_first_version_workspace_company_foundation_gate.md`<br>`issues/phase1a_ai_company_runtime_foundation.md`<br>`issues/phase5_g2_credential_vault_gate.md`<br>`issues/phase6_workflow_mvp.md`<br>`issues/phase7_billing_readiness.md`<br>`issues/phase7_billing_usage_contract_gate.md`<br>`issues/phase7_local_demo_release_hardening_gate.md`<br>`issues/phase7_production_credential_vault_gate.md`<br>`knowledge/EXECUTION_SUMMARY_MEMORY.md`<br>`knowledge/PROJECT_MEMORY.md`<br>`knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md`<br>`reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`<br>`reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`<br>`reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`<br>`reviews/032_local_demo_operator_release_notes_package_review.md`<br>`reviews/034_local_demo_api_smoke_helper_review.md`<br>`reviews/072_model_gateway_local_demo_release_candidate_review.md`<br>`reviews/073_model_gateway_local_demo_release_closeout_review.md`<br>`reviews/076_workspace_company_foundation_local_demo_evidence_review.md`<br>`reviews/085_phase4_ai_employee_system_rc_review.md` |
| `docs/demo/` | 10 | `docs/00_Context/DOCUMENT_MIGRATION_PLAN.md`<br>`docs/demo/phase7-stable-demo-script.md`<br>`docs/pmo/source-control-baseline-freeze.md`<br>`docs/release/phase3-demo-freeze-report.md`<br>`docs/release/phase4-ai-employee-demo-freeze-report.md`<br>`docs/release/phase5-g2-credential-vault-demo-freeze-report.md`<br>`docs/release/phase6-workflow-mvp-demo-freeze-report.md`<br>`docs/release/phase7-demo-polish-commercial-readiness.md`<br>`issues/phase45_admin_demo_polish_execution.md`<br>`knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md` |
| `docs/handoff/` | 1 | `docs/00_Context/DOCUMENT_MIGRATION_PLAN.md` |
| `.workbuddy/` | 21 | `.workbuddy/automations/automation-1783450520356/memory.md`<br>`.workbuddy/automations/automation-1784564820520/memory.md`<br>`.workbuddy/memory/2026-07-07.md`<br>`.workbuddy/memory/2026-07-10.md`<br>`.workbuddy/memory/2026-07-12.md`<br>`.workbuddy/memory/2026-07-13.md`<br>`.workbuddy/memory/2026-07-21.md`<br>`docs/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md`<br>`docs/pmo/source-control-baseline-freeze.md`<br>`docs/project-space-confirmation-2026-07-17.md`<br>`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate.md`<br>`issues/shared/20260717_admin_workspace_stash_handoff.md`<br>`knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md`<br>`reviews/055_d3_implementation_verification.md`<br>`reviews/059_d2_impl_verification.md`<br>`reviews/20260717_workspace_shared_main_manual_merge_preparation_review.md`<br>`reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate_review.md`<br>`reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate_review.md`<br>`reviews/20260719_d1_unfreeze_qa.md`<br>`reviews/20260720_d1_execute_a_qa.md`<br>`shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md` |
| `frontend/ceo-evidence/` | 5 | `.workbuddy/memory/2026-07-21.md`<br>`docs/architecture/issue-b-ceo-runtime-evidence-impl-plan.md`<br>`docs/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md`<br>`docs/status/USER_CAPABILITY_LEDGER.md`<br>`reviews/20260729_sprint0_architecture_convergence_review.md` |

Directory references make a whole-directory move unsafe even when an
individual child has no direct file reference. The row-level gate remains the
authoritative movement decision.

## 5. Keep

Keep assets are evidence, Issue/Review records or decision provenance. They are
not migration candidates in Phase 3-B2.

The 10 protected ignored-location Keep records are listed in Section 8.

| Path | Type | Size | Source | Git | References | Current Use | Gate |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `docs/product/adr0028_phase1_shared_contract_handoff.md` | Handoff Document | 1.7 KiB (1723 B) | Product decision basis | Tracked | M0 / S0 / A0 / I1 | Decision provenance | 禁止移动 |
| `docs/release/admin-ai-company-asset-foundation.md` | Release Evidence | 8.6 KiB (8854 B) | Release evidence | Tracked | M1 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md` | Release Evidence | 6.1 KiB (6276 B) | Release evidence | Tracked | M9 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/ai-task-executor-mvp-v0.1-release-record.md` | Release Evidence | 4.8 KiB (4931 B) | Release evidence | Tracked | M15 / S0 / A0 / I3 | Release/acceptance provenance | 禁止移动 |
| `docs/release/ai-task-executor-mvp-v0.1.md` | Release Evidence | 8.2 KiB (8351 B) | Release evidence | Tracked | M11 / S0 / A0 / I2 | Release/acceptance provenance | 禁止移动 |
| `docs/release/model-gateway-local-demo-first-version-release-record.md` | Release Evidence | 7.0 KiB (7134 B) | Release evidence | Tracked | M8 / S2 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/model-gateway-local-demo-rc.md` | Release Evidence | 9.0 KiB (9246 B) | Release evidence | Tracked | M9 / S0 / A0 / I2 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase1-company-runtime-foundation-report.md` | Release Evidence | 4.6 KiB (4703 B) | Release evidence | Tracked | M3 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase1a-company-project-runtime-backend.md` | Release Evidence | 3.8 KiB (3855 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase1b-gate-assessment.md` | Release Evidence | 10.3 KiB (10564 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase1b-template-runtime-integration-gate.md` | Release Evidence | 2.6 KiB (2678 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase3-demo-freeze-report.md` | Release Evidence | 6.3 KiB (6454 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase3-workspace-self-extension-rc.md` | Release Evidence | 8.2 KiB (8425 B) | Release evidence | Tracked | M0 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase4-ai-employee-demo-freeze-report.md` | Release Evidence | 6.4 KiB (6512 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase4-ai-employee-system-rc.md` | Release Evidence | 8.1 KiB (8266 B) | Release evidence | Tracked | M2 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase45-workspace-demo-review-roadmap.md` | Release Evidence | 14.2 KiB (14499 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase5-g2-credential-vault-demo-freeze-report.md` | Release Evidence | 8.1 KiB (8302 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase5-g2-credential-vault-implementation-report.md` | Release Evidence | 6.3 KiB (6487 B) | Release evidence | Tracked | M2 / S0 / A0 / I2 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase5-g2-credential-vault-rc.md` | Release Evidence | 8.4 KiB (8649 B) | Release evidence | Tracked | M2 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase55-post-g2-roadmap-review.md` | Release Evidence | 14.9 KiB (15210 B) | Release evidence | Tracked | M3 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase6-workflow-mvp-demo-freeze-report.md` | Release Evidence | 9.8 KiB (10062 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase6-workflow-mvp-implementation-report.md` | Release Evidence | 6.8 KiB (6987 B) | Release evidence | Tracked | M1 / S0 / A0 / I2 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase6-workflow-mvp-rc.md` | Release Evidence | 8.6 KiB (8853 B) | Release evidence | Tracked | M1 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase65-post-workflow-roadmap-review.md` | Release Evidence | 13.0 KiB (13267 B) | Release evidence | Tracked | M4 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase7-demo-polish-commercial-readiness.md` | Release Evidence | 8.3 KiB (8452 B) | Release evidence | Tracked | M3 / S0 / A0 / I1 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase75-commercial-validation-value-event-design.md` | Release Evidence | 5.3 KiB (5387 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase75-value-event-validation-report.md` | Release Evidence | 4.3 KiB (4364 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase8-workspace-billing-support-implementation-report.md` | Release Evidence | 3.8 KiB (3842 B) | Release evidence | Tracked | M1 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase9a-commercial-configuration-status.md` | Release Evidence | 8.5 KiB (8735 B) | Release evidence | Tracked | M0 / S0 / A0 / I0 | Release/acceptance provenance | 禁止移动 |
| `docs/release/phase9a-commercial-design-freeze.md` | Release Evidence | 21.0 KiB (21461 B) | Release evidence | Tracked | M0 / S0 / A0 / I2 | Release/acceptance provenance | 禁止移动 |
| `issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md` | Handoff Document | 2.0 KiB (2022 B) | Issue record | Tracked | M3 / S0 / A0 / I1 | Issue scope history | 禁止移动 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate.md` | Handoff Document | 5.9 KiB (6049 B) | Issue record | Tracked | M3 / S0 / A0 / I3 | Issue scope history | 禁止移动 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_snapshot_fix_gate.md` | Handoff Document | 1.9 KiB (1978 B) | Issue record | Tracked | M0 / S0 / A0 / I1 | Issue scope history | 禁止移动 |
| `issues/shared/20260717_admin_r3_e2e_handoff.md` | Handoff Document | 5.1 KiB (5245 B) | Issue record | Tracked | M4 / S0 / A0 / I2 | Issue scope history | 禁止移动 |
| `issues/shared/20260717_admin_workspace_stash_handoff.md` | Handoff Document | 4.8 KiB (4874 B) | Issue record | Tracked | M1 / S0 / A0 / I2 | Issue scope history | 禁止移动 |
| `reviews/076_workspace_company_foundation_local_demo_evidence.png` | PNG Evidence | 90.3 KiB (92480 B) | Review evidence | Tracked | M4 / S0 / A0 / I0 | Acceptance evidence | 禁止移动 |
| `reviews/078_workspace_department_catalog_local_demo_evidence.png` | PNG Evidence | 109.3 KiB (111919 B) | Review evidence | Tracked | M6 / S0 / A0 / I0 | Acceptance evidence | 禁止移动 |
| `reviews/20260718_workspace_r4_hybrid_mode_handoff_contract_gate_review.md` | Handoff Document | 1.2 KiB (1262 B) | Review evidence | Tracked | M1 / S0 / A0 / I1 | Acceptance evidence | 禁止移动 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate_review.md` | Handoff Document | 1.7 KiB (1732 B) | Review evidence | Tracked | M0 / S0 / A0 / I0 | Acceptance evidence | 禁止移动 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_snapshot_fix_gate_review.md` | Handoff Document | 1.7 KiB (1701 B) | Review evidence | Tracked | M0 / S0 / A0 / I1 | Acceptance evidence | 禁止移动 |

## 6. Archive

Archive assets have historical value but no current authority. `安全移动`
means the individual file has no detected direct, resolved or internal
reference. A directory-level move still requires a batch reference check.

The ignored `deploy/curis/releases/` Archive record is listed in Section 8.

| Path | Type | Size | Source | Git | References | Current Use | Gate |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `.workbuddy/automations/automation-1783450520356/memory.md` | WorkBuddy Memory | 787 B (787 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/automations/automation-1784564820520/memory.md` | WorkBuddy Memory | 13.3 KiB (13651 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-07.md` | WorkBuddy Memory | 39.0 KiB (39915 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-08.md` | WorkBuddy Memory | 26.7 KiB (27372 B) | WorkBuddy tool memory | Tracked | M1 / S0 / A0 / I1 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-09.md` | WorkBuddy Memory | 38.0 KiB (38870 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-10.md` | WorkBuddy Memory | 20.5 KiB (20970 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-11.md` | WorkBuddy Memory | 34.0 KiB (34796 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-12.md` | WorkBuddy Memory | 49.1 KiB (50310 B) | WorkBuddy tool memory | Tracked | M1 / S0 / A0 / I1 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-13.md` | WorkBuddy Memory | 19.5 KiB (19943 B) | WorkBuddy tool memory | Tracked | M1 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-17.md` | WorkBuddy Memory | 11.7 KiB (11995 B) | WorkBuddy tool memory | Tracked | M1 / S0 / A0 / I1 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-18.md` | WorkBuddy Memory | 6.5 KiB (6626 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-19.md` | WorkBuddy Memory | 1.8 KiB (1835 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-20.md` | WorkBuddy Memory | 29.8 KiB (30496 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-21.md` | WorkBuddy Memory | 23.5 KiB (24037 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/2026-07-22.md` | WorkBuddy Memory | 5.1 KiB (5205 B) | WorkBuddy tool memory | Tracked | M0 / S0 / A0 / I0 | Historical Agent/tool context | 需要人工确认 |
| `.workbuddy/memory/MEMORY.md` | WorkBuddy Memory | 16.5 KiB (16902 B) | WorkBuddy tool memory | Tracked | M5 / S0 / A0 / I4 | Historical Agent/tool context | 需要人工确认 |
| `PROJECT_HANDOFF.md` | Handoff Document | 16.8 KiB (17221 B) | Historical handoff/governance | Tracked | M9 / S0 / A0 / I1 | Completed or superseded handoff | 需要人工确认 |
| `diagrams/curis-architecture-diagrams.html` | HTML Prototype | 49.0 KiB (50140 B) | Historical diagram/prototype | Tracked | M1 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-aicost.html` | HTML Prototype | 15.9 KiB (16269 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-capability.html` | HTML Prototype | 18.1 KiB (18557 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-databi.html` | HTML Prototype | 16.7 KiB (17117 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-department.html` | HTML Prototype | 18.1 KiB (18534 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-employee.html` | HTML Prototype | 16.2 KiB (16592 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-finance.html` | HTML Prototype | 17.2 KiB (17646 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-homepage-teal-v2.html` | HTML Prototype | 32.9 KiB (33640 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-homepage-variants.html` | HTML Prototype | 22.0 KiB (22573 B) | Historical diagram/prototype | Tracked | M1 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-knowledge.html` | HTML Prototype | 18.0 KiB (18407 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-login.html` | HTML Prototype | 12.9 KiB (13185 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-report.html` | HTML Prototype | 16.2 KiB (16610 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-scope.html` | HTML Prototype | 16.9 KiB (17260 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `diagrams/ui-settings.html` | HTML Prototype | 19.8 KiB (20297 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-task-console.html` | HTML Prototype | 23.0 KiB (23512 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `diagrams/ui-workflow.html` | HTML Prototype | 19.0 KiB (19411 B) | Historical diagram/prototype | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `docs/demo/phase3-demo-script.md` | Demo Document | 5.4 KiB (5575 B) | Historical demo | Tracked | M0 / S0 / A0 / I1 | Completed demo material | 需要人工确认 |
| `docs/demo/phase4-ai-employee-demo-script.md` | Demo Document | 6.8 KiB (6965 B) | Historical demo | Tracked | M1 / S0 / A0 / I1 | Completed demo material | 需要人工确认 |
| `docs/demo/phase5-g2-credential-vault-demo-script.md` | Demo Document | 11.5 KiB (11766 B) | Historical demo | Tracked | M1 / S0 / A0 / I1 | Completed demo material | 需要人工确认 |
| `docs/demo/phase6-workflow-mvp-demo-script.md` | Demo Document | 11.8 KiB (12073 B) | Historical demo | Tracked | M1 / S0 / A0 / I2 | Completed demo material | 需要人工确认 |
| `docs/demo/phase7-demo-seed.json` | JSON Demo/Support | 1011 B (1011 B) | Historical demo | Tracked | M1 / S0 / A0 / I2 | Completed demo material | 需要人工确认 |
| `docs/demo/phase7-stable-demo-script.md` | Demo Document | 6.7 KiB (6907 B) | Historical demo | Tracked | M1 / S0 / A0 / I1 | Completed demo material | 需要人工确认 |
| `docs/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md` | Handoff Document | 11.1 KiB (11411 B) | Historical handoff/governance | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `docs/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md` | Handoff Document | 14.4 KiB (14730 B) | Historical handoff/governance | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `docs/pmo/20260719_quota_handoff_plan.md` | Handoff Document | 3.0 KiB (3025 B) | Historical handoff/governance | Tracked | M4 / S0 / A0 / I0 | Completed or superseded handoff | 需要人工确认 |
| `docs/prototypes/curis-full-system-high-fidelity-prototype.html` | HTML Prototype | 478 B (478 B) | Static prototype | Tracked | M2 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `docs/team-v2/BOOTSTRAP_HANDOFFS.md` | Handoff Document | 1.1 KiB (1076 B) | Historical handoff/governance | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `docs/team-v2/HANDOFF_TEMPLATE.md` | Handoff Document | 194 B (194 B) | Historical handoff/governance | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `frontend/ceo-evidence/index.html` | HTML Prototype | 335 B (335 B) | Legacy CEO evidence app | Tracked | M0 / S1 / A0 / I0 | Historical interactive prototype | 禁止移动 |
| `frontend/design-spec/ceo-office/_archive/capability-center-compact-v6.html` | HTML Prototype | 36.4 KiB (37260 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v2.html` | HTML Prototype | 22.4 KiB (22962 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v3.html` | HTML Prototype | 23.8 KiB (24340 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v4.html` | HTML Prototype | 24.3 KiB (24863 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v5.html` | HTML Prototype | 25.4 KiB (26015 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v6.devmode.html` | HTML Prototype | 35.9 KiB (36797 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact-v6.html` | HTML Prototype | 33.6 KiB (34377 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home-compact.html` | HTML Prototype | 18.9 KiB (19317 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.devmode.html` | HTML Prototype | 49.1 KiB (50243 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.html` | HTML Prototype | 38.5 KiB (39450 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/ceo-office-home.terra.html` | HTML Prototype | 22.3 KiB (22862 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/org-center-compact-v6.html` | HTML Prototype | 33.2 KiB (34009 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/org-center.terra.html` | HTML Prototype | 18.6 KiB (19065 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/org-spatial-3d.html` | HTML Prototype | 11.6 KiB (11870 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/outcome-center-compact-v6.html` | HTML Prototype | 29.0 KiB (29719 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_archive/project-center-compact-v6.html` | HTML Prototype | 29.2 KiB (29929 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/ceo-office/_samples/analytics-sample.html` | HTML Prototype | 35.8 KiB (36618 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/brainstorm-sample.html` | HTML Prototype | 34.0 KiB (34855 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/capability-center-sample.html` | HTML Prototype | 37.3 KiB (38223 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/ceo-home-sample.html` | HTML Prototype | 36.2 KiB (37045 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/department-detail-sample.html` | HTML Prototype | 34.8 KiB (35682 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/execution-sample.html` | HTML Prototype | 35.0 KiB (35857 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/knowledge-sample.html` | HTML Prototype | 35.6 KiB (36417 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/org-center-sample.html` | HTML Prototype | 35.2 KiB (36076 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/project-center-sample.html` | HTML Prototype | 34.5 KiB (35279 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/project-detail-sample.html` | HTML Prototype | 34.7 KiB (35489 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/report-detail-sample.html` | HTML Prototype | 33.7 KiB (34532 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/skill-detail-sample.html` | HTML Prototype | 34.9 KiB (35758 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/_samples/task-detail-sample.html` | HTML Prototype | 34.1 KiB (34938 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/analytics-org.html` | HTML Prototype | 31.1 KiB (31885 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/analytics-project.html` | HTML Prototype | 31.2 KiB (31961 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/analytics-workflow.html` | HTML Prototype | 31.2 KiB (31908 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/analytics.html` | HTML Prototype | 31.2 KiB (31927 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/brainstorm-active.html` | HTML Prototype | 30.6 KiB (31366 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/brainstorm-result-detail.html` | HTML Prototype | 31.4 KiB (32126 B) | CEO Office historical design | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/brainstorm-results.html` | HTML Prototype | 30.5 KiB (31254 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/brainstorm-session-detail.html` | HTML Prototype | 31.8 KiB (32575 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/brainstorm.html` | HTML Prototype | 31.2 KiB (31903 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-agent-list.html` | HTML Prototype | 36.2 KiB (37032 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I6 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-center.html` | HTML Prototype | 35.5 KiB (36325 B) | CEO Office historical design | Tracked | M4 / S0 / A0 / I5 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-model-list.html` | HTML Prototype | 36.1 KiB (36975 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I6 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-skill-list.html` | HTML Prototype | 36.6 KiB (37513 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I6 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-tool-list.html` | HTML Prototype | 36.3 KiB (37179 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I6 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/capability-workflow-list.html` | HTML Prototype | 36.4 KiB (37251 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I6 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/ceo-home.html` | HTML Prototype | 31.9 KiB (32716 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/company-runtime.html` | HTML Prototype | 31.1 KiB (31810 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/decision-center.html` | HTML Prototype | 32.0 KiB (32799 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I5 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/department-detail.html` | HTML Prototype | 32.1 KiB (32830 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/employee-detail.html` | HTML Prototype | 32.3 KiB (33091 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/execution-runs.html` | HTML Prototype | 31.0 KiB (31708 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/execution-tasks.html` | HTML Prototype | 30.9 KiB (31650 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/execution.html` | HTML Prototype | 31.0 KiB (31729 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/handoff/capability-center/capability-center.devmode.md` | Handoff Document | 6.6 KiB (6757 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `frontend/design-spec/ceo-office/handoff/capability-center/capability-center.hifi.html` | HTML Prototype | 14.8 KiB (15158 B) | CEO Office historical design | Tracked | M0 / S0 / A0 / I1 | Completed or superseded handoff | 需要人工确认 |
| `frontend/design-spec/ceo-office/knowledge-company.html` | HTML Prototype | 30.8 KiB (31577 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/knowledge-dept.html` | HTML Prototype | 30.8 KiB (31568 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/knowledge-entry-detail.html` | HTML Prototype | 31.5 KiB (32232 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/knowledge-project.html` | HTML Prototype | 30.8 KiB (31572 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/knowledge.html` | HTML Prototype | 32.0 KiB (32775 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/org-center.html` | HTML Prototype | 31.4 KiB (32173 B) | CEO Office historical design | Tracked | M4 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/org-dept.html` | HTML Prototype | 31.0 KiB (31740 B) | CEO Office historical design | Tracked | M5 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/org-employees.html` | HTML Prototype | 30.7 KiB (31430 B) | CEO Office historical design | Tracked | M4 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/project-center.html` | HTML Prototype | 31.3 KiB (32077 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/project-dept.html` | HTML Prototype | 30.9 KiB (31667 B) | CEO Office historical design | Tracked | M4 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/project-detail.html` | HTML Prototype | 31.9 KiB (32708 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/report-detail.html` | HTML Prototype | 31.4 KiB (32132 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/reports.html` | HTML Prototype | 32.0 KiB (32785 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I5 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/run-detail.html` | HTML Prototype | 31.9 KiB (32628 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/settings-brand.html` | HTML Prototype | 31.2 KiB (31938 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/settings-notify.html` | HTML Prototype | 31.1 KiB (31847 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/settings-profile.html` | HTML Prototype | 31.5 KiB (32207 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/settings.html` | HTML Prototype | 33.9 KiB (34663 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/skill-detail.html` | HTML Prototype | 32.7 KiB (33524 B) | CEO Office historical design | Tracked | M3 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/strategy-room.html` | HTML Prototype | 32.1 KiB (32821 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I5 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/ceo-office/task-detail.html` | HTML Prototype | 31.8 KiB (32605 B) | CEO Office historical design | Tracked | M2 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/.preflight/preflight.html` | HTML Prototype | 14.0 KiB (14362 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical interactive prototype | 安全移动 |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.css` | Prototype CSS | 1.8 KiB (1850 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.js` | Prototype Script | 3.1 KiB (3138 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.css` | Prototype CSS | 3.4 KiB (3471 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I48 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.js` | Prototype Script | 5.5 KiB (5666 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I47 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/project-dept-ia.js` | Prototype Script | 5.7 KiB (5839 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.css` | Prototype CSS | 18.2 KiB (18673 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.js` | Prototype Script | 4.8 KiB (4931 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/01-ceo-home-1440-viewport.png` | PNG Design Export | 79.2 KiB (81145 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-capability-center-1440.png` | PNG Design Export | 68.5 KiB (70147 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-org-center-1440.png` | PNG Design Export | 48.3 KiB (49483 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-project-center-1440.png` | PNG Design Export | 51.8 KiB (53060 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-1440.png` | PNG Design Export | 75.0 KiB (76792 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-390.png` | PNG Design Export | 27.6 KiB (28284 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-1440.png` | PNG Design Export | 82.2 KiB (84150 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-390.png` | PNG Design Export | 18.9 KiB (19339 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/ceo-home-390.png` | PNG Design Export | 24.4 KiB (24978 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/company-runtime-1440.png` | PNG Design Export | 54.1 KiB (55425 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/employee-detail-1440.png` | PNG Design Export | 61.3 KiB (62806 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/execution-1440.png` | PNG Design Export | 76.8 KiB (78607 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-1440.png` | PNG Design Export | 65.6 KiB (67151 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-390.png` | PNG Design Export | 25.8 KiB (26384 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-1440.png` | PNG Design Export | 70.8 KiB (72494 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-390.png` | PNG Design Export | 29.7 KiB (30397 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/settings-1440.png` | PNG Design Export | 69.6 KiB (71278 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/colors_and_type.css` | Prototype CSS | 8.8 KiB (8973 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I6 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/curis-ceo-office.design` | Design Source | 14.9 KiB (15228 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I1 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md` | Handoff Document | 1.7 KiB (1789 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Completed or superseded handoff | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-state-catalog.html` | HTML Prototype | 8.9 KiB (9073 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-data-map.json` | JSON Demo/Support | 5.4 KiB (5485 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I4 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-handoff.md` | Handoff Document | 9.8 KiB (10010 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I2 | Completed or superseded handoff | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-secondary-page-contracts.json` | JSON Demo/Support | 5.0 KiB (5082 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I3 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-org.png` | PNG Design Export | 116.6 KiB (119396 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-project.png` | PNG Design Export | 105.7 KiB (108262 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics-workflow.png` | PNG Design Export | 119.6 KiB (122428 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/analytics.png` | PNG Design Export | 123.2 KiB (126126 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-active.png` | PNG Design Export | 80.6 KiB (82522 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-results.png` | PNG Design Export | 94.4 KiB (96660 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm-session-detail.png` | PNG Design Export | 98.8 KiB (101219 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/brainstorm.png` | PNG Design Export | 112.1 KiB (114805 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-agent-list.png` | PNG Design Export | 108.7 KiB (111345 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-center.png` | PNG Design Export | 151.8 KiB (155432 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-model-list.png` | PNG Design Export | 92.0 KiB (94226 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-skill-list.png` | PNG Design Export | 99.8 KiB (102190 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-tool-list.png` | PNG Design Export | 116.4 KiB (119235 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/capability-workflow-list.png` | PNG Design Export | 76.2 KiB (78021 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/ceo-home.png` | PNG Design Export | 139.9 KiB (143256 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/company-runtime.png` | PNG Design Export | 101.0 KiB (103413 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/decision-center.png` | PNG Design Export | 129.1 KiB (132246 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/department-create.png` | PNG Design Export | 67.6 KiB (69178 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/department-detail.png` | PNG Design Export | 78.1 KiB (79969 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/employee-create.png` | PNG Design Export | 70.2 KiB (71935 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/employee-detail.png` | PNG Design Export | 73.6 KiB (75344 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution-runs.png` | PNG Design Export | 98.9 KiB (101284 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution-tasks.png` | PNG Design Export | 114.9 KiB (117699 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/execution.png` | PNG Design Export | 124.7 KiB (127737 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-company.png` | PNG Design Export | 99.2 KiB (101537 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-dept.png` | PNG Design Export | 97.6 KiB (99978 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-entry-detail.png` | PNG Design Export | 97.0 KiB (99290 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge-project.png` | PNG Design Export | 98.5 KiB (100834 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/knowledge.png` | PNG Design Export | 105.0 KiB (107555 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-center.png` | PNG Design Export | 117.8 KiB (120675 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-dept.png` | PNG Design Export | 80.5 KiB (82432 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/org-employees.png` | PNG Design Export | 98.7 KiB (101078 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-center.png` | PNG Design Export | 105.1 KiB (107604 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-dept.png` | PNG Design Export | 81.5 KiB (83417 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-detail.png` | PNG Design Export | 89.1 KiB (91229 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` | PNG Design Export | 164.7 KiB (168636 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` | PNG Design Export | 155.8 KiB (159550 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/report-detail.png` | PNG Design Export | 113.4 KiB (116088 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/reports.png` | PNG Design Export | 138.3 KiB (141648 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/run-detail.png` | PNG Design Export | 81.8 KiB (83734 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-brand.png` | PNG Design Export | 119.3 KiB (122209 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-notify.png` | PNG Design Export | 120.0 KiB (122831 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings-profile.png` | PNG Design Export | 119.9 KiB (122801 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/settings.png` | PNG Design Export | 130.1 KiB (133226 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/skill-detail.png` | PNG Design Export | 99.2 KiB (101554 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/strategy-room.png` | PNG Design Export | 101.3 KiB (103781 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/task-detail.png` | PNG Design Export | 143.5 KiB (146958 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-org.png` | PNG Design Export | 120.9 KiB (123836 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-project.png` | PNG Design Export | 109.1 KiB (111697 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics-workflow.png` | PNG Design Export | 122.8 KiB (125723 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/analytics.png` | PNG Design Export | 163.8 KiB (167741 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-active.png` | PNG Design Export | 83.7 KiB (85705 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-results.png` | PNG Design Export | 97.7 KiB (100019 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm-session-detail.png` | PNG Design Export | 119.2 KiB (122026 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/brainstorm.png` | PNG Design Export | 141.4 KiB (144784 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-agent-list.png` | PNG Design Export | 113.3 KiB (116042 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-center.png` | PNG Design Export | 184.4 KiB (188780 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-model-list.png` | PNG Design Export | 96.1 KiB (98376 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-skill-list.png` | PNG Design Export | 104.3 KiB (106841 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-tool-list.png` | PNG Design Export | 122.3 KiB (125281 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/capability-workflow-list.png` | PNG Design Export | 82.0 KiB (83960 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/ceo-home.png` | PNG Design Export | 179.6 KiB (183876 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/company-runtime.png` | PNG Design Export | 114.5 KiB (117216 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/decision-center.png` | PNG Design Export | 138.2 KiB (141521 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/department-create.png` | PNG Design Export | 71.2 KiB (72880 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/department-detail.png` | PNG Design Export | 89.9 KiB (92050 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/employee-create.png` | PNG Design Export | 77.8 KiB (79714 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/employee-detail.png` | PNG Design Export | 88.9 KiB (91040 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution-runs.png` | PNG Design Export | 109.3 KiB (111919 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution-tasks.png` | PNG Design Export | 123.8 KiB (126769 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/execution.png` | PNG Design Export | 144.6 KiB (148053 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-company.png` | PNG Design Export | 101.1 KiB (103486 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-dept.png` | PNG Design Export | 99.9 KiB (102248 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-entry-detail.png` | PNG Design Export | 113.5 KiB (116267 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge-project.png` | PNG Design Export | 102.0 KiB (104411 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/knowledge.png` | PNG Design Export | 128.2 KiB (131297 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-center.png` | PNG Design Export | 152.7 KiB (156354 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-dept.png` | PNG Design Export | 84.0 KiB (86003 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/org-employees.png` | PNG Design Export | 102.4 KiB (104896 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-center.png` | PNG Design Export | 122.3 KiB (125269 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-dept.png` | PNG Design Export | 85.3 KiB (87371 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-detail.png` | PNG Design Export | 101.9 KiB (104355 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` | PNG Design Export | 193.2 KiB (197819 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` | PNG Design Export | 195.2 KiB (199899 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/report-detail.png` | PNG Design Export | 161.0 KiB (164833 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/reports.png` | PNG Design Export | 144.0 KiB (147463 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/run-detail.png` | PNG Design Export | 135.8 KiB (139084 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-brand.png` | PNG Design Export | 125.8 KiB (128780 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-notify.png` | PNG Design Export | 123.6 KiB (126560 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings-profile.png` | PNG Design Export | 123.3 KiB (126209 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/settings.png` | PNG Design Export | 133.4 KiB (136580 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/skill-detail.png` | PNG Design Export | 117.7 KiB (120511 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/strategy-room.png` | PNG Design Export | 115.6 KiB (118367 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/task-detail.png` | PNG Design Export | 157.3 KiB (161115 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-org.png` | PNG Design Export | 42.7 KiB (43695 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-project.png` | PNG Design Export | 42.2 KiB (43180 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics-workflow.png` | PNG Design Export | 45.6 KiB (46679 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/analytics.png` | PNG Design Export | 39.3 KiB (40273 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-active.png` | PNG Design Export | 45.8 KiB (46888 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-results.png` | PNG Design Export | 67.3 KiB (68877 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm-session-detail.png` | PNG Design Export | 78.6 KiB (80468 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/brainstorm.png` | PNG Design Export | 37.6 KiB (38517 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-agent-list.png` | PNG Design Export | 59.1 KiB (60559 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-center.png` | PNG Design Export | 83.0 KiB (85022 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-model-list.png` | PNG Design Export | 51.5 KiB (52761 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-skill-list.png` | PNG Design Export | 52.7 KiB (54004 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-tool-list.png` | PNG Design Export | 67.4 KiB (69015 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/capability-workflow-list.png` | PNG Design Export | 41.1 KiB (42091 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/ceo-home.png` | PNG Design Export | 53.4 KiB (54694 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical visual reference | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/company-runtime.png` | PNG Design Export | 49.7 KiB (50908 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/decision-center.png` | PNG Design Export | 71.5 KiB (73208 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/department-create.png` | PNG Design Export | 42.7 KiB (43724 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/department-detail.png` | PNG Design Export | 55.9 KiB (57269 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/employee-create.png` | PNG Design Export | 48.2 KiB (49320 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/employee-detail.png` | PNG Design Export | 55.4 KiB (56681 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution-runs.png` | PNG Design Export | 49.0 KiB (50215 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution-tasks.png` | PNG Design Export | 60.2 KiB (61659 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/execution.png` | PNG Design Export | 55.4 KiB (56708 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-company.png` | PNG Design Export | 50.7 KiB (51928 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-dept.png` | PNG Design Export | 62.8 KiB (64297 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-entry-detail.png` | PNG Design Export | 70.4 KiB (72091 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge-project.png` | PNG Design Export | 62.6 KiB (64117 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/knowledge.png` | PNG Design Export | 58.4 KiB (59794 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-center.png` | PNG Design Export | 45.5 KiB (46547 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-dept.png` | PNG Design Export | 48.8 KiB (50020 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/org-employees.png` | PNG Design Export | 63.8 KiB (65329 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-center.png` | PNG Design Export | 61.1 KiB (62579 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-dept.png` | PNG Design Export | 52.9 KiB (54174 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-detail.png` | PNG Design Export | 63.4 KiB (64884 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` | PNG Design Export | 85.0 KiB (87071 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs.png` | PNG Design Export | 87.1 KiB (89236 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/report-detail.png` | PNG Design Export | 94.1 KiB (96315 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/reports.png` | PNG Design Export | 78.0 KiB (79841 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/run-detail.png` | PNG Design Export | 58.7 KiB (60144 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-brand.png` | PNG Design Export | 52.5 KiB (53805 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-notify.png` | PNG Design Export | 44.1 KiB (45155 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings-profile.png` | PNG Design Export | 44.4 KiB (45441 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/settings.png` | PNG Design Export | 45.0 KiB (46122 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/skill-detail.png` | PNG Design Export | 75.4 KiB (77220 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/strategy-room.png` | PNG Design Export | 58.2 KiB (59607 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/task-detail.png` | PNG Design Export | 69.7 KiB (71333 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/manifest.json` | Export Manifest/Support | 1.4 KiB (1422 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/analytics-default.png` | PNG Design Export | 237.7 KiB (243382 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/brainstorm-default.png` | PNG Design Export | 248.5 KiB (254421 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/capability-center-default.png` | PNG Design Export | 331.2 KiB (339189 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/ceo-home-default.png` | PNG Design Export | 303.8 KiB (311074 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/company-runtime-default.png` | PNG Design Export | 214.5 KiB (219684 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.all-pages.json` | JSON Demo/Support | 4.4 KiB (4462 B) | Deprecated UI V2 | Tracked | M2 / S0 / A0 / I4 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.frames.json` | JSON Demo/Support | 3.6 KiB (3719 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.interactions.json` | JSON Demo/Support | 2.2 KiB (2258 B) | Deprecated UI V2 | Tracked | M2 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.tokens.json` | JSON Demo/Support | 2.0 KiB (2055 B) | Deprecated UI V2 | Tracked | M2 / S0 / A0 / I2 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/decision-center-default.png` | PNG Design Export | 249.3 KiB (255297 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/department-create-default.png` | PNG Design Export | 145.1 KiB (148566 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/employee-create-default.png` | PNG Design Export | 140.2 KiB (143519 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/execution-default.png` | PNG Design Export | 266.2 KiB (272575 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/knowledge-default.png` | PNG Design Export | 215.5 KiB (220692 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/org-center-default.png` | PNG Design Export | 257.4 KiB (263620 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/org-employees-default.png` | PNG Design Export | 226.2 KiB (231626 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-center-default.png` | PNG Design Export | 224.3 KiB (229671 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-dept-default.png` | PNG Design Export | 176.0 KiB (180173 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-miniapp-default.png` | PNG Design Export | 334.5 KiB (342562 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/project-xhs-default.png` | PNG Design Export | 311.6 KiB (319112 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/reports-default.png` | PNG Design Export | 267.6 KiB (274003 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/settings-default.png` | PNG Design Export | 233.3 KiB (238849 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/strategy-room-default.png` | PNG Design Export | 203.0 KiB (207896 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/index.html` | HTML Prototype | 2.9 KiB (2965 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I0 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-1024.png` | PNG Design Export | 77.1 KiB (78912 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-1440.png` | PNG Design Export | 85.3 KiB (87393 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-390.png` | PNG Design Export | 46.1 KiB (47186 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-1024.png` | PNG Design Export | 73.6 KiB (75346 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-1440.png` | PNG Design Export | 74.9 KiB (76712 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/docs/ui/states/index-390.png` | PNG Design Export | 64.4 KiB (65990 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical visual reference | 安全移动 |
| `frontend/design-spec/curis-ui-v2/fix-cap-links.mjs` | Prototype Script | 2.0 KiB (2077 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical package support | 安全移动 |
| `frontend/design-spec/curis-ui-v2/fix-placeholders-v3.js` | Prototype Script | 21.7 KiB (22223 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical package support | 安全移动 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-org.html` | HTML Prototype | 43.8 KiB (44855 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-project.html` | HTML Prototype | 43.2 KiB (44227 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-workflow.html` | HTML Prototype | 44.0 KiB (45061 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/analytics.html` | HTML Prototype | 48.9 KiB (50040 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-active.html` | HTML Prototype | 41.9 KiB (42918 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-results.html` | HTML Prototype | 42.5 KiB (43537 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-session-detail.html` | HTML Prototype | 43.5 KiB (44567 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm.html` | HTML Prototype | 49.1 KiB (50257 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-agent-list.html` | HTML Prototype | 44.8 KiB (45923 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-center.html` | HTML Prototype | 59.3 KiB (60766 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I45 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-model-list.html` | HTML Prototype | 42.4 KiB (43451 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-skill-list.html` | HTML Prototype | 43.0 KiB (43986 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-tool-list.html` | HTML Prototype | 46.2 KiB (47284 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/capability-workflow-list.html` | HTML Prototype | 39.8 KiB (40753 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/ceo-home.html` | HTML Prototype | 56.0 KiB (57300 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I46 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/company-runtime.html` | HTML Prototype | 41.2 KiB (42199 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/decision-center.html` | HTML Prototype | 53.0 KiB (54318 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/department-create.html` | HTML Prototype | 1.1 KiB (1131 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/department-detail.html` | HTML Prototype | 42.8 KiB (43821 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/employee-create.html` | HTML Prototype | 1.1 KiB (1144 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/employee-detail.html` | HTML Prototype | 39.0 KiB (39938 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/execution-runs.html` | HTML Prototype | 41.4 KiB (42429 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/execution-tasks.html` | HTML Prototype | 42.6 KiB (43631 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/execution.html` | HTML Prototype | 51.0 KiB (52231 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I44 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-company.html` | HTML Prototype | 42.4 KiB (43406 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-dept.html` | HTML Prototype | 42.0 KiB (43038 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-entry-detail.html` | HTML Prototype | 43.9 KiB (44964 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-project.html` | HTML Prototype | 42.0 KiB (43052 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge.html` | HTML Prototype | 45.0 KiB (46128 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I44 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/org-center.html` | HTML Prototype | 55.7 KiB (57012 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I46 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/org-dept.html` | HTML Prototype | 40.4 KiB (41339 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/org-employees.html` | HTML Prototype | 45.4 KiB (46532 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I4 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/project-center.html` | HTML Prototype | 58.2 KiB (59605 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I44 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/project-dept.html` | HTML Prototype | 44.2 KiB (45275 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/project-detail.html` | HTML Prototype | 43.3 KiB (44307 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I3 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/project-miniapp-detail.html` | HTML Prototype | 13.5 KiB (13855 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/project-xhs-workflow-detail.html` | HTML Prototype | 14.3 KiB (14692 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I2 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/report-detail.html` | HTML Prototype | 41.8 KiB (42755 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/reports.html` | HTML Prototype | 50.9 KiB (52136 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/run-detail.html` | HTML Prototype | 44.4 KiB (45506 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/settings-brand.html` | HTML Prototype | 43.9 KiB (44997 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/settings-notify.html` | HTML Prototype | 46.5 KiB (47618 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/settings-profile.html` | HTML Prototype | 41.2 KiB (42195 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/settings.html` | HTML Prototype | 44.0 KiB (45020 B) | Deprecated UI V2 | Tracked | M1 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/skill-detail.html` | HTML Prototype | 42.1 KiB (43124 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/strategy-room.html` | HTML Prototype | 50.0 KiB (51196 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I42 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/pages/task-detail.html` | HTML Prototype | 45.9 KiB (46991 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/runtime-orchestration-summary.json` | JSON Demo/Support | 1.5 KiB (1572 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I1 | Historical package support | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/validation-report.json` | JSON Demo/Support | 57.1 KiB (58421 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Historical package support | 安全移动 |
| `shared/prototypes/curis-full-system-high-fidelity-prototype.html` | HTML Prototype | 48.2 KiB (49384 B) | Static prototype | Tracked | M1 / S0 / A0 / I1 | Historical interactive prototype | 需要人工确认 |

## 7. Delete Candidate

Delete Candidate does not authorize deletion. Every row requires separate
human confirmation, a fresh reference check and an explicit deletion action.

The 33 ignored-location Delete Candidate records are listed in Section 8.

| Path | Type | Size | Source | Git | References | Current Use | Gate |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `frontend/ceo-evidence/dist/index.html` | HTML Prototype | 433 B (433 B) | Legacy CEO evidence app | Tracked | M0 / S0 / A0 / I0 | Reproducible Vite build output | 需要人工确认 |
| `frontend/ceo-evidence/tsconfig.tsbuildinfo` | Generated Build Metadata | 401 B (401 B) | Legacy CEO evidence app | Tracked | M0 / S0 / A0 / I0 | Reproducible TypeScript cache | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp-detail.png` | PNG Design Export | 164.7 KiB (168636 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs-workflow-detail.png` | PNG Design Export | 155.8 KiB (159550 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp-detail.png` | PNG Design Export | 193.2 KiB (197819 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs-workflow-detail.png` | PNG Design Export | 195.2 KiB (199899 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp-detail.png` | PNG Design Export | 85.0 KiB (87071 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs-workflow-detail.png` | PNG Design Export | 87.1 KiB (89236 B) | Deprecated UI V2 | Tracked | M0 / S0 / A0 / I0 | Byte-identical duplicate export | 需要人工确认 |

The six PNG rows are one redundant side of six SHA-256-confirmed,
byte-identical pairs. The retained side remains classified Archive.

| Delete Candidate | Retained Archive Asset | SHA-256 |
| --- | --- | --- |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` | `ee516e9be227c2200db5dbaf4d76271036058167820281f2a86df9df792c780f` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs-workflow-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` | `0afd0b2d2f473c409d5ef20b193d9681327e85054bea3c5c2a5fa418a573c57b` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` | `162dd8ddbe012230ef9d44a5a4d94543835e6430df8727dbc77bce058044f80a` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs-workflow-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` | `0475158ce59d431b090936be83abb798eb027bcb4d7a1f4559be9b76757dc27b` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` | `67cc00942629d00d33d25d85cc5cbe27fa32f13fa76c0106bf70c7a50d0afbfd` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs-workflow-detail.png` | `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs.png` | `d44acb7e378aa4434d878c91673375f396dfb5ae10a314b3c45f5ef8595df3a1` |

`frontend/ceo-evidence/package.json` defines the reproducible
`tsc -b && vite build` chain, and `frontend/ceo-evidence/.gitignore` excludes
`dist/`. This is the basis for classifying the tracked dist index and
TypeScript build metadata as Delete Candidates.

## 8. Ignored, Generated And Temporary Locations

Ignored locations are recorded at directory/file level. Their child files are
not added to the 425 tracked-file count. Sensitive generated gateway state and
local environment content were not opened for content inspection.

| Path | Type | Size | Source | Git | References | Current Use | Classification | Gate |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `.DS_Store` | Ignored File | 36.0 KiB (36864 B) | Ignored workspace state | Ignored | M7/S1/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `.pytest_cache/` | Ignored Directory | 152.0 KiB (155648 B) | Ignored workspace state | Ignored | M3/S2/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `.tmp-ui-handoff/` | Ignored Directory | 16.0 KiB (16384 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `.venv/` | Ignored Directory | 40.4 MiB (42315776 B) | Ignored workspace state | Ignored | M181/S28/A0 | Regenerable Python environment | Delete Candidate | 需要人工确认 |
| `.worktrees/` | Ignored Directory | 3598.9 MiB (3773673472 B) | Ignored workspace state | Ignored | M1/S2/A0 | Active Git worktrees | Keep | 禁止移动 |
| `backend/.pytest_cache/` | Ignored Directory | 124.0 KiB (126976 B) | Ignored workspace state | Ignored | M0/S1/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/.venv/` | Ignored Directory | 40.3 MiB (42307584 B) | Ignored workspace state | Ignored | M67/S17/A0 | Regenerable Python environment | Delete Candidate | 需要人工确认 |
| `backend/__pycache__/` | Ignored Directory | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/app/__pycache__/` | Ignored Directory | 4.0 MiB (4161536 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/app/agent_conversion/__pycache__/` | Ignored Directory | 176.0 KiB (180224 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/app/connectors/__pycache__/` | Ignored Directory | 68.0 KiB (69632 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/app/models/__pycache__/` | Ignored Directory | 24.0 KiB (24576 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/app/routers/__pycache__/` | Ignored Directory | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/data/` | Ignored Directory | 1.0 MiB (1064960 B) | Ignored workspace state | Ignored | M11/S1/A0 | Runtime or test data | Keep | 禁止移动 |
| `backend/scripts/__pycache__/` | Ignored Directory | 24.0 KiB (24576 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/selfuse.log` | Ignored File | 324.0 KiB (331776 B) | Ignored workspace state | Ignored | M0/S0/A0 | Runtime log | Delete Candidate | 需要人工确认 |
| `backend/tests/__pycache__/` | Ignored Directory | 5.0 MiB (5287936 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `backend/tests/data/` | Ignored Directory | 188.0 KiB (192512 B) | Ignored workspace state | Ignored | M1/S1/A0 | Runtime or test data | Keep | 禁止移动 |
| `backend/tests/real_run/__pycache__/` | Ignored Directory | 20.0 KiB (20480 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `data/b_layer_pending_decisions.sqlite` | Ignored File | 32.0 KiB (32768 B) | Ignored workspace state | Ignored | M3/S2/A0 | Runtime or test data | Keep | 禁止移动 |
| `data/curis.sqlite` | Ignored File | 2.0 MiB (2121728 B) | Ignored workspace state | Ignored | M42/S8/A1 | Runtime or test data | Keep | 禁止移动 |
| `data/issue_pipeline.sqlite` | Ignored File | 128.0 KiB (131072 B) | Ignored workspace state | Ignored | M1/S0/A0 | Runtime or test data | Keep | 禁止移动 |
| `data/quality.sqlite` | Ignored File | 0 B (0 B) | Ignored workspace state | Ignored | M43/S1/A0 | Runtime or test data | Keep | 禁止移动 |
| `deploy/.DS_Store` | Ignored File | 8.0 KiB (8192 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `deploy/curis/.DS_Store` | Ignored File | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `deploy/curis/gateway/.generated/` | Ignored Directory | 2.4 MiB (2486272 B) | Ignored workspace state | Ignored | M44/S3/A0 | Sensitive generated gateway/runtime state | Keep | 禁止移动 |
| `deploy/curis/releases/` | Ignored Directory | 15.7 MiB (16486400 B) | Ignored workspace state | Ignored | M0/S2/A0 | Historical local release bundle | Archive | 需要人工确认 |
| `deploy/new-api/.env` | Ignored File | 4.0 KiB (4096 B) | Ignored workspace state | Ignored | M19/S5/A0 | Sensitive local configuration | Keep | 禁止移动 |
| `deploy/new-api/data/` | Ignored Directory | 2.9 MiB (3059712 B) | Ignored workspace state | Ignored | M4/S1/A0 | Runtime or test data | Keep | 禁止移动 |
| `docs/.DS_Store` | Ignored File | 32.0 KiB (32768 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `docs/product/.DS_Store` | Ignored File | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/.DS_Store` | Ignored File | 8.0 KiB (8192 B) | Ignored workspace state | Ignored | M1/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/.next/` | Ignored Directory | 1865.3 MiB (1955946496 B) | Ignored workspace state | Ignored | M1/S2/A0 | Regenerable frontend build cache | Delete Candidate | 需要人工确认 |
| `frontend/ceo-evidence/dist/assets/` | Ignored Directory | 512.0 KiB (524288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable Vite build assets | Delete Candidate | 需要人工确认 |
| `frontend/ceo-evidence/node_modules/` | Ignored Directory | 295.1 MiB (309387264 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable dependencies | Delete Candidate | 需要人工确认 |
| `frontend/design-spec/.DS_Store` | Ignored File | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/design-spec/ceo-office/.DS_Store` | Ignored File | 16.0 KiB (16384 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/.DS_Store` | Ignored File | 8.0 KiB (8192 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/design-spec/curis-ui-v2/docs/ui/.DS_Store` | Ignored File | 8.0 KiB (8192 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/design-spec/prototypes/` | Ignored Directory | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `frontend/node_modules/` | Ignored Directory | 435.6 MiB (456806400 B) | Ignored workspace state | Ignored | M4/S1/A0 | Regenerable dependencies | Delete Candidate | 需要人工确认 |
| `issues/.DS_Store` | Ignored File | 48.0 KiB (49152 B) | Ignored workspace state | Ignored | M0/S0/A0 | Temporary Finder/delivery residue | Delete Candidate | 需要人工确认 |
| `tools/migrations/__pycache__/` | Ignored Directory | 12.0 KiB (12288 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |
| `tools/real_rd_fixture/__pycache__/` | Ignored Directory | 8.0 KiB (8192 B) | Ignored workspace state | Ignored | M0/S0/A0 | Regenerable test/runtime cache | Delete Candidate | 需要人工确认 |

## 9. Risks

- A directory reference can cover children that have no direct file link.
- HTML, CSS, JavaScript and image assets form internal packages; partial moves
  can break relative paths even when external references are absent.
- WorkBuddy Memory may be consumed by WorkBuddy outside repository text
  references; it requires tool-owner confirmation.
- Release Evidence is part of historical acceptance provenance and is
  forbidden to move without an evidence-retention decision.
- Issue, Review and product-decision Handoff records remain in place.
- `frontend/ceo-evidence/index.html` has a live configuration reference and is
  forbidden to move.
- Ignored runtime databases, worktrees, environment files and generated
  gateway state are protected, not cleanup targets.
- Generated gateway state may contain credentials or private runtime material;
  it requires Security review before any cleanup.
- Dynamic references assembled at runtime cannot be proven by static text
  scanning alone.
- Delete Candidate status is analytical only and does not authorize deletion.

## 10. Recommended Next Step

1. Review and commit these two Phase 3-B2 analysis documents.
2. If migration is approved, open a separate Phase 3-B3 archive batch using
   only rows marked `Archive` and `安全移动`.
3. Move one coherent directory cohort at a time and repeat reference checks
   immediately before each move.
4. Keep all `Keep` and `禁止移动` records at their current paths.
5. Handle WorkBuddy Memory, Release Evidence and ignored generated state in
   separate owner-specific reviews.
6. Treat tracked and ignored Delete Candidates as a later deletion review;
   do not combine deletion with archive migration.

Phase 3-B2 performs no move and no deletion.
