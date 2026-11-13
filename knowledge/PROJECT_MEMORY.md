# Project Memory

## Purpose

Project Memory is a compact, deterministic project-fact read model for Curis Workspace. It helps future Curis seats retrieve the smallest relevant context segment without rereading the whole repository.

It does not own project truth. If a fact is wrong, update the owning source first, then refresh this file.

Sources:

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`
- `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`
- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`
- `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`
- `knowledge/ROLE_PROFILES.md`
- `issues/011_sprint_2_project_memory_first_slice.md`
- `issues/012_sprint_3_lightweight_role_responsibility_gate.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`
- `issues/014_sprint_3_role_context_runtime_reference_gate.md`
- `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`
- `reviews/009_project_memory_foundation_architecture_boundaries_review.md`
- `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`
- `reviews/012_sprint_3_role_profiles_first_slice_review.md`
- `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`
- `reviews/014_role_context_runtime_reference_first_slice_review.md`
- `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`
- `docs/sprints/sprint-4-multi-entry-advanced-ui.md`
- `issues/016_sprint_3_closeout_sprint_4_entry_gate.md`
- `issues/017_sprint_4_multi_entry_ui_first_slice.md`
- `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`
- `docs/sprints/ai-task-executor-mvp-readiness.md`
- `issues/018_sprint_4_closeout_mvp_readiness_gate.md`
- `issues/019_ai_task_executor_mvp_readiness_review.md`
- `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md`
- `reviews/017_ai_task_executor_mvp_readiness_boundaries_review.md`
- `reviews/018_ai_task_executor_mvp_readiness_review.md`
- `issues/020_chinese_operation_console_localization.md`
- `reviews/019_chinese_operation_console_localization_review.md`
- `docs/sprints/ai-task-executor-mvp-release-candidate.md`
- `issues/021_ai_task_executor_mvp_release_candidate_gate.md`
- `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`
- `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`
- `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`
- `docs/release/ai-task-executor-mvp-v0.1.md`
- `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`
- `issues/023_ai_task_executor_mvp_local_demo_release_verification.md`
- `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`
- `issues/024_ai_task_executor_mvp_v0_1_release_closeout.md`
- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`
- `docs/sprints/post-v0.1-execution-reliability.md`
- `issues/025_post_v0_1_execution_reliability_gate.md`
- `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`
- `issues/026_post_v0_1_execution_reliability_boundaries.md`
- `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`
- `issues/027_run_evidence_reliability_first_slice.md`
- `reviews/025_run_evidence_reliability_first_slice_review.md`
- `issues/028_workflow_error_fallback_observability_gate.md`
- `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`
- `issues/071_workspace_tenant_model_preference_gate.md`
- `issues/029_workflow_error_fallback_observability_boundaries.md`
- `reviews/026_workflow_error_fallback_observability_boundaries_review.md`
- `issues/030_workflow_error_fallback_evidence_map.md`
- `reviews/027_workflow_error_fallback_evidence_map_review.md`
- `issues/031_evolution_decision_evidence_reliability_gate.md`
- `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`
- `issues/032_evolution_decision_evidence_reliability_boundaries.md`
- `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`
- `issues/033_evolution_decision_evidence_map.md`
- `reviews/029_evolution_decision_evidence_map_review.md`
- `issues/034_post_v0_1_execution_reliability_closeout_gate.md`
- `reviews/030_post_v0_1_execution_reliability_closeout_review.md`
- `issues/035_local_demo_operator_polish_gate.md`
- `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`
- `issues/036_local_demo_operator_polish_boundaries.md`
- `reviews/031_local_demo_operator_polish_boundaries_review.md`
- `issues/037_local_demo_operator_release_notes_package.md`
- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`
- `reviews/032_local_demo_operator_release_notes_package_review.md`
- `issues/038_local_demo_verification_automation_gate.md`
- `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`
- `issues/039_local_demo_verification_automation_boundaries.md`
- `reviews/033_local_demo_verification_automation_boundaries_review.md`
- `issues/040_local_demo_api_smoke_helper.md`
- `tools/local_demo_api_smoke.py`
- `reviews/034_local_demo_api_smoke_helper_review.md`
- `issues/041_project_memory_execution_summary_gate.md`
- `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md`
- `issues/042_project_memory_execution_summary_boundaries.md`
- `reviews/035_project_memory_execution_summary_boundaries_review.md`
- `issues/043_project_memory_execution_summary.md`
- `knowledge/EXECUTION_SUMMARY_MEMORY.md`
- `reviews/036_project_memory_execution_summary_review.md`
- `issues/065_workspace_model_gateway_adapter.md`
- `reviews/062_workspace_model_gateway_adapter_review.md`
- `issues/066_workspace_official_model_catalog.md`
- `reviews/063_workspace_official_model_catalog_review.md`
- `issues/067_workspace_official_tool_catalog.md`
- `reviews/064_workspace_official_tool_catalog_review.md`
- `docs/deployment/new-api-local.md`
- `issues/068_new_api_local_deployment.md`
- `reviews/065_new_api_local_deployment_review.md`
- `issues/073_workspace_model_preference_ui_gate.md`
- `reviews/070_workspace_model_preference_ui_review.md`
- `issues/074_workspace_model_preference_local_e2e_evidence.md`
- `reviews/071_workspace_model_preference_local_e2e_review.md`
- `issues/075_model_gateway_local_demo_release_candidate_gate.md`
- `docs/release/model-gateway-local-demo-rc.md`
- `reviews/072_model_gateway_local_demo_release_candidate_review.md`
- `issues/076_model_gateway_post_rc_next_phase_gate.md`
- `issues/077_post_first_version_workspace_company_foundation_gate.md`
- `docs/release/model-gateway-local-demo-first-version-release-record.md`
- `reviews/073_model_gateway_local_demo_release_closeout_review.md`
- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
- `reviews/074_workspace_company_foundation_boundaries_review.md`
- `issues/078_workspace_company_foundation_first_slice_gate.md`
- `reviews/075_workspace_company_foundation_first_slice_review.md`
- `issues/079_workspace_company_foundation_local_demo_evidence_gate.md`
- `issues/080_workspace_company_department_catalog_summary_gate.md`
- `issues/085_workspace_admin_contract_integration_completion.md`
- `reviews/082_workspace_admin_contract_integration_completion_review.md`
- `issues/086_workspace_self_extension_mvp.md`
- `reviews/083_workspace_self_extension_mvp_review.md`

## Current Product Frame

- Product direction: AI Company System for solo entrepreneurs.
- Current launch scope: AI Task Executor MVP.
- Current sprint: Workspace Self-Extension MVP completed.
- Current implementation gate: Tool System v1.8.
- Protected loop: Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage.
- Current task: Continue post-Phase-3 Workspace development from accepted tenant-private self-extension baseline.
- Latest completed task: T-223 Accept Workspace Self-Extension MVP.
- Current owner seat: 产品规划席.

Sources:

- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `knowledge/003_Architecture.md`

## Active Work Segment

- Current issue: `issues/080_workspace_company_department_catalog_summary_gate.md`.
- Latest completed task: T-216 Accept Workspace Department Activation UI.
- Latest Workspace integration: `issues/065_workspace_model_gateway_adapter.md` implemented a New API OpenAI-compatible `ModelGatewayAdapter`, default `model_gateway_tool` runtime routing, and gateway metric fields in UsageEvent payloads.
- Latest Workspace catalog: `issues/066_workspace_official_model_catalog.md` implemented `GET /api/catalog/models` for active `source=official` model metadata with no credential values.
- Latest Workspace catalog: `issues/067_workspace_official_tool_catalog.md` implemented `GET /api/catalog/tools` for active official tool metadata with no credential values.
- Latest deployment: `issues/068_new_api_local_deployment.md` prepared New API Docker Compose deployment docs and smoke script; Docker CLI, Docker Compose, and Colima are installed; New API container `curis-new-api` is running locally; DeepSeek is configured as the first upstream channel; Curis local New API token is stored only in ignored `deploy/new-api/.env`; `/v1/models` includes `deepseek-v4-flash`; `/v1/chat/completions` succeeds; Workspace task execution uses `model_gateway_tool` and writes required `usage.model_call` events.
- Latest security boundary: `issues/069_model_gateway_production_security_boundary.md` is done; ADR-0029 defines production-safe model gateway secret, Admin/Workspace responsibility, and UsageEvent logging boundaries. New API remains gateway-only, Curis DB stores no credential values, and Workspace calls stay behind `ModelGatewayAdapter`.
- Latest implementation: `issues/070_model_gateway_runtime_secret_guardrails.md` is implemented, quality-verified, and accepted with evidence in `reviews/067_model_gateway_runtime_secret_guardrails_review.md`. Partial gateway env config fails closed, model gateway errors are redacted, UsageEvent payloads remain allowlisted/redacted, and gateway/model metadata rejects secret-like values. Quality verification on commit `b01edfd4`: 16 focused guardrail tests and 203 backend regression tests passed; secret/scope/frontend guards passed; no blockers found.
- Latest gate approved: `issues/071_workspace_tenant_model_preference_gate.md` was approved by 总控决策席 on 2026-07-08 for architecture boundary definition only.
- Latest boundary: Workspace Tenant Model Preference Foundation architecture boundaries are defined, quality-verified, and accepted in `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md` with evidence in `reviews/068_workspace_tenant_model_preference_boundaries_review.md`. Commit `9dd75340` is boundary-only with no backend/frontend implementation files; ADR-0029, runtime secret guardrails, active `source=official` catalog source, metadata-only tenant preference state, and `ModelGatewayAdapter` execution path are preserved.
- Latest implementation: `issues/072_workspace_tenant_model_preference_first_slice.md` is implemented, quality-verified, and accepted with evidence in `reviews/069_workspace_tenant_model_preference_first_slice_review.md`. Workspace now has backend-only tenant model preference read/write/delete APIs, metadata-only persistence, active official catalog validation, and runtime preference resolution through `ModelGatewayAdapter`. Product acceptance completed by 产品规划席 on 2026-07-08. Quality verification on commit `a0d3a54b`: 4 focused tenant preference tests and 207 backend regression tests passed; secret/scope/frontend guards passed; no blockers found.
- Latest gate approved: `issues/073_workspace_model_preference_ui_gate.md` was approved by 总控决策席 on 2026-07-08 for a minimal frontend-only Workspace selector.
- Latest implementation: Workspace Model Preference UI first slice is implemented, quality-verified, and accepted with evidence in `reviews/070_workspace_model_preference_ui_review.md`. Workspace now has a frontend-only selector in the existing operation console to view, save, and reset tenant default model preference from active official model options. Product acceptance completed by 产品规划席 on 2026-07-08. Quality verification on commit `5727410f`: 14 frontend view-model tests passed, frontend lint passed, frontend build passed outside the sandbox after sandbox port binding was blocked, backend/Admin/shared/runtime guard passed, existing preference APIs only are used, and Task API payload shape `{ content }` is preserved.
- Latest verification: `issues/074_workspace_model_preference_local_e2e_evidence.md` passed with evidence in `reviews/071_workspace_model_preference_local_e2e_review.md`. Real local backend/frontend runtime verified preference read/save/reset, visible official model option, no secret-like rendered metadata, operation-console task creation, and Task API content-only boundary. Known local environment note: when frontend uses a non-default port such as `3010`, backend `CURIS_ALLOWED_ORIGINS` must include that origin.
- Latest gate approved: `issues/075_model_gateway_local_demo_release_candidate_gate.md` was approved by 总控决策席 on 2026-07-08 for a documentation/evidence-only local/demo release-candidate package.
- Latest package: Model Gateway Local Demo Release Candidate package is prepared, quality-verified, and accepted in `docs/release/model-gateway-local-demo-rc.md` with evidence in `reviews/072_model_gateway_local_demo_release_candidate_review.md`. Package coverage includes New API local gateway, official model/tool catalogs, UsageEvent model-call fields, ADR-0029 runtime secret guardrails, tenant model preference backend/UI, local E2E evidence, verification checklist, startup/runbook commands, and known-gap classification. Quality verification passed against commit `9bfc7d8b`: evidence map, runbook/checklist, known-gap classification, source-of-truth status, secret scan, and behavior-file scope guard passed; no backend/frontend behavior files changed for this issue. 产品规划席 accepted the local/demo RC package on 2026-07-08; hosted production remains blocked.
- Latest gate approved: `issues/076_model_gateway_post_rc_next_phase_gate.md` was approved by 总控决策席 on 2026-07-08 with Option A: documentation/evidence-only local/demo first-version release closeout.
- Latest closeout package: Model Gateway Local Demo first-version release closeout is prepared, quality-verified, and accepted in `docs/release/model-gateway-local-demo-first-version-release-record.md` with evidence in `reviews/073_model_gateway_local_demo_release_closeout_review.md`. The closeout package records release decision evidence, operator handoff summary, final local/demo checklist, known-gap confirmation, source-of-truth status updates, and next backlog boundary. Quality verification passed against commit `0801231d`: release decision record, operator handoff, checklist, known-gap classification, source-of-truth status, secret scan, and behavior-file scope guard passed; no backend/frontend behavior files changed for this issue. 产品规划席 accepted the local/demo first-version release closeout on 2026-07-08.
- Latest boundary: Workspace Company Foundation architecture/product boundaries are defined and quality-verified in `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md` with evidence in `reviews/074_workspace_company_foundation_boundaries_review.md`. The boundary defines a minimal local/demo CEO-facing company shell over existing tenant/workspace context, company identity concept, department catalog/instances, model preference, task console, Project Memory, and release status. Quality verification passed against commit `651bdb99`: ADR-0031 boundary-only scope, forbidden-scope locks, first-slice boundary, read-model gap rule, source-of-truth routing, secret scan, and behavior-file guard passed; no backend/frontend behavior files changed for this issue.
- Latest acceptance: 产品规划席 accepted Workspace Company Foundation boundaries in `reviews/074_workspace_company_foundation_boundaries_review.md`; ADR-0031 is accepted as the current boundary and implementation remains separately gated.
- Latest gate approved: `issues/078_workspace_company_foundation_first_slice_gate.md` was approved by 总控决策席 on 2026-07-08 with Option A. Next work is frontend-only implementation inside the existing operation console using only existing non-secret state and existing preference/catalog APIs. Backend/API/schema/persistence, Task API, execution-loop, tool routing, workflow, model-selection behavior, Project Memory writes, runtime behavior, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, New API source/internal DB dependency, and department CRUD/workflow routing remain blocked.
- Latest implementation: `issues/078_workspace_company_foundation_first_slice_gate.md` is implemented, quality-verified, and accepted with evidence in `reviews/075_workspace_company_foundation_first_slice_review.md`. Commit `dfd60689` adds a frontend-only local/demo company frame in the existing operation console over existing task list state and existing model preference state. Quality verification passed: 16 frontend tests, lint, build, API/payload scan, forbidden-scope scan, secret scan, and behavior-file guard passed; no backend/API/schema/persistence/Admin/shared/deploy/tools/data files entered the commit. 产品规划席 accepted the slice on 2026-07-08.
- Latest gate approved: `issues/079_workspace_company_foundation_local_demo_evidence_gate.md` was approved by 总控决策席 on 2026-07-08 with Option A. Next work is verification-only local/demo evidence for the accepted company frame, including browser-visible/screenshot evidence, visible company-frame content, no secret-like metadata, and Task API payload `{ content }`.
- Latest evidence accepted: `issues/079_workspace_company_foundation_local_demo_evidence_gate.md` is verified and accepted with evidence in `reviews/076_workspace_company_foundation_local_demo_evidence_review.md` and screenshot artifact `reviews/076_workspace_company_foundation_local_demo_evidence.png`. Browser-visible evidence confirms the company frame renders in local/demo runtime with company identity, local/demo status, model preference summary, task summary, and source links visible. Backend health, frontend runtime smoke, 16 frontend tests, lint, build, Task API payload boundary, and secret-like metadata scan passed. No implementation or behavior change was made for this evidence issue.
- Latest gate approved: `issues/080_workspace_company_department_catalog_summary_gate.md` was approved by 总控决策席 on 2026-07-08 with Option A. Next work is frontend-only department catalog summary inside the existing company frame using existing `GET /api/catalog/department-types` only.
- Latest implementation accepted: `issues/080_workspace_company_department_catalog_summary_gate.md` is implemented, quality-verified, and accepted with evidence in `reviews/077_workspace_company_department_catalog_summary_review.md`. Workspace now shows a frontend-only read-only `部门目录` summary inside the existing company frame using existing `GET /api/catalog/department-types` only. Verification passed with 18 frontend tests, lint, build, API usage scan, Task API payload guard, and forbidden-scope scan. No backend/API/schema/persistence, Admin Platform, department CRUD/instances/routing, Employee CRUD, billing/ROI/packages/marketplace, business-module, secret, Task API, or runtime behavior change was introduced.
- Latest gate approved: `issues/081_workspace_department_catalog_local_demo_evidence_gate.md` approved Option A for verification-only local/demo browser evidence for the accepted department catalog summary.
- Latest evidence accepted: `issues/081_workspace_department_catalog_local_demo_evidence_gate.md` is verified and accepted with evidence in `reviews/078_workspace_department_catalog_local_demo_evidence_review.md` and screenshot artifact `reviews/078_workspace_department_catalog_local_demo_evidence.png`. Browser-visible evidence confirms the accepted `部门目录` summary renders in local/demo runtime with active official count, category summary, and non-secret department labels visible. Backend health, frontend runtime smoke, department catalog API read, 18 frontend tests, lint, build, Task API payload boundary, and secret-like metadata scan passed. No implementation or behavior change was made for this evidence issue.
- Latest gate approved: `issues/082_workspace_department_activation_boundary_gate.md` approved Option A for architecture/product boundary definition only for future tenant-local department activation over existing active official department type metadata.
- Latest boundary accepted: `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md` is defined, quality-verified, and accepted with evidence in `reviews/079_workspace_department_activation_boundaries_review.md`. The boundary defines future tenant-local department activation as metadata-only selection over active official department type metadata. Official department type supply remains outside Workspace. Implementation, backend/API/schema/persistence, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, and runtime behavior changes remain blocked until a separate implementation issue is approved.
- Latest gate approved: `issues/083_workspace_department_activation_first_slice.md` approved backend-only tenant-local department activation metadata over active official department type metadata.
- Latest implementation accepted: `issues/083_workspace_department_activation_first_slice.md` is implemented, quality-verified, and accepted with evidence in `reviews/080_workspace_department_activation_first_slice_review.md`. Workspace now has backend-only tenant-local department activation metadata with `GET /api/workspace/departments/activation` and `PUT /api/workspace/departments/activation`. Writes validate active official department type metadata, reads/writes are tenant-scoped, persistence is metadata-only, and API responses expose only non-secret department metadata plus enabled state. Focused backend tests passed and full backend regression passed with 255 tests. Frontend selector, Admin Platform implementation, department instances, workflow routing, Employee CRUD, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, Project Memory runtime writes, and runtime behavior changes remain blocked.
- Latest gate approved: `issues/084_workspace_department_activation_ui_gate.md` approved frontend-only department activation display/selector inside the existing company frame using only existing activation APIs.
- Latest implementation accepted: `issues/084_workspace_department_activation_ui_gate.md` is implemented, quality-verified, accepted, and current-state corrected with evidence in `reviews/081_workspace_department_activation_ui_review.md`. Workspace now shows and saves tenant-local enabled department type selections inside the existing company frame using only existing activation APIs. A current audit found page-level selector wiring was missing; the correction added it, added regression coverage, and passed 22 frontend tests, lint, build, and focused backend activation tests. No backend/API/schema/persistence change, new department API, department instance, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business-module, secret, Task API, Project Memory runtime write, or runtime behavior change was introduced for this correction.
- Latest integration accepted: `issues/085_workspace_admin_contract_integration_completion.md` is implemented, quality-verified, and accepted with evidence in `reviews/082_workspace_admin_contract_integration_completion_review.md`. Workspace task execution now writes Admin-compatible `usage.model_call`, `usage.tool_call`, and `usage.task_execution` records; Admin usage projection can query by `tenant_id`; `tenant_private` capability metadata is isolated under `/api/workspace/capabilities/private`; official capability reads remain `/api/catalog/*`; Workspace runtime execution files do not call `/api/platform/*`. Verification passed with 7 focused ADR-0028 tests, 50 gateway/catalog/preference tests, 38 execution-engine tests, 279 full backend tests, whitespace check, endpoint scope scan, usage/namespace scan, and secret scan.
- Latest implementation accepted: `issues/086_workspace_self_extension_mvp.md` is implemented, quality-verified, and accepted with evidence in `reviews/083_workspace_self_extension_mvp_review.md`. Workspace now supports tenant-private model/tool/connector metadata, a unified official + tenant-private capability selector, and optional task capability selection. Tenant-private execution preserves the existing model gateway path and writes usage events with `capability_source=tenant_private`. Verification passed with TDD red evidence, 10 ADR-0028 focused tests, 42 Phase-3 focused tests, 38 execution-engine tests, 298 full backend tests, whitespace check, runtime `/api/platform/*` scope scan, tenant-private scan, and secret scan.
- Latest quality scope split: `reviews/077_workspace_company_department_catalog_summary_review.md` resolved the issue-080 evidence split. Department catalog summary evidence remains bounded to read-only `GET /api/catalog/department-types` plus `reviews/078` browser evidence; activation behavior belongs to accepted issues 083/084. T-217 is closed.
- Current task: Prepare next bounded Workspace Department Activation local/demo evidence gate.
- Owner seat: 产品规划席.
- Sprint 3 intent: add deterministic role profiles, responsibility boundaries, and escalation triggers inside AI Task Executor MVP.
- Gate decision: approved by 总控决策席 on 2026-07-06.
- Architecture boundary: defined by 系统交付席 in `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`.
- First implementation issue: `issues/013_sprint_3_role_profiles_first_slice.md`.
- First implementation artifact: `knowledge/ROLE_PROFILES.md`.
- Product acceptance: completed by 产品规划席 on 2026-07-06.
- Current gate issue: `issues/014_sprint_3_role_context_runtime_reference_gate.md`.
- Runtime reference gate decision: approved by 总控决策席 on 2026-07-06 for architecture boundary definition only.
- Runtime reference architecture boundary: defined by 系统交付席 in `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`.
- First runtime reference implementation issue: `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`.
- First runtime reference implementation artifact: `backend/app/role_context.py`.
- Sprint 4 PRD slice: `docs/sprints/sprint-4-multi-entry-advanced-ui.md`.
- Sprint 3 closeout / Sprint 4 entry gate issue: `issues/016_sprint_3_closeout_sprint_4_entry_gate.md`.
- Sprint 3 closeout decision: approved by 总控决策席 on 2026-07-06.
- Sprint 4 entry decision: approved by 总控决策席 on 2026-07-06 for architecture boundary definition only.
- Sprint 4 architecture boundary: defined by 系统交付席 in `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`.
- Sprint 4 first implementation issue: `issues/017_sprint_4_multi_entry_ui_first_slice.md`.
- Sprint 4 first implementation evidence: `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.
- MVP readiness gate PRD slice: `docs/sprints/ai-task-executor-mvp-readiness.md`.
- MVP readiness gate issue: `issues/018_sprint_4_closeout_mvp_readiness_gate.md`.
- Sprint 4 first-slice closeout decision: approved by 总控决策席 on 2026-07-06.
- MVP readiness review entry decision: approved by 总控决策席 on 2026-07-06 for gate-only planning and gap classification.
- MVP readiness architecture boundary: defined by 系统交付席 in `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md`.
- MVP readiness boundary evidence: `reviews/017_ai_task_executor_mvp_readiness_boundaries_review.md`.
- MVP readiness boundary verification plan was accepted by 产品规划席 on 2026-07-06.
- MVP readiness review issue: `issues/019_ai_task_executor_mvp_readiness_review.md`.
- MVP readiness review evidence: `reviews/018_ai_task_executor_mvp_readiness_review.md`.
- MVP release-candidate gate decision: approved by 总控决策席 on 2026-07-06 for boundary definition and stabilization/documentation planning only.
- MVP release-candidate architecture boundary: defined by 系统交付席 in `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`.
- MVP release-candidate boundary evidence: `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`.
- MVP release-candidate boundaries and exact stabilization/documentation plan were accepted by 产品规划席 on 2026-07-06.
- MVP release-candidate stabilization/documentation implementation issue is `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`.
- Release-candidate artifact: `docs/release/ai-task-executor-mvp-v0.1.md`.
- Release-candidate delivery evidence: `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`.
- Post-v0.1 Execution Reliability closeout review was accepted by 产品规划席 on 2026-07-06.
- Local/demo operator polish gate issue is `issues/035_local_demo_operator_polish_gate.md`.
- Next phase selected: Local/Demo Operator Polish and Release Notes.
- Local/demo operator polish gate was approved by 总控决策席 on 2026-07-06 for architecture boundary definition only.
- Local/demo operator polish boundaries are defined in `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`.
- Boundary issue is `issues/036_local_demo_operator_polish_boundaries.md`.
- Delivery evidence is `reviews/031_local_demo_operator_polish_boundaries_review.md`.
- Recommended first slice is documentation-only: `Local/Demo Operator Release Notes Package`.
- Local/demo operator polish architecture boundaries were verified by 质量运行席 on 2026-07-06.
- Local/demo operator polish architecture boundaries were accepted by 产品规划席 on 2026-07-06.
- First implementation issue is `issues/037_local_demo_operator_release_notes_package.md`.
- Implementation scope is documentation-only operator release notes.
- Local/demo operator notes artifact is `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`.
- Delivery evidence is `reviews/032_local_demo_operator_release_notes_package_review.md`.
- Local/demo operator release notes package was verified by 质量运行席 on 2026-07-06.
- Local/demo operator release notes package was accepted by 产品规划席 on 2026-07-06.
- Local/demo operator polish first slice is complete.
- Main thread closeout was prepared on 2026-07-06.
- 产品规划席 selected Local/Demo Verification Automation as the next bounded phase on 2026-07-07.
- Gate issue is `issues/038_local_demo_verification_automation_gate.md`.
- Local/demo verification automation gate was approved by 总控决策席 on 2026-07-07 for architecture boundary definition only.
- Local/demo verification automation boundaries are defined in `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`.
- Boundary issue is `issues/039_local_demo_verification_automation_boundaries.md`.
- Delivery evidence is `reviews/033_local_demo_verification_automation_boundaries_review.md`.
- Recommended first slice is `Local/Demo API Smoke Helper`.
- Local/demo verification automation boundaries were verified by 质量运行席 on 2026-07-07.
- Local/demo verification automation boundaries were accepted by 产品规划席 on 2026-07-07.
- First implementation issue is `issues/040_local_demo_api_smoke_helper.md`.
- Local/demo API smoke helper artifact is `tools/local_demo_api_smoke.py`.
- Delivery evidence is `reviews/034_local_demo_api_smoke_helper_review.md`.
- Local/demo API smoke helper was verified by 质量运行席 on 2026-07-07 against the real local FastAPI app.
- Local/demo API smoke helper was accepted by 产品规划席 on 2026-07-07.
- Local/demo verification automation first slice is complete.
- 产品规划席 selected Project Memory Execution Summary as the next bounded phase on 2026-07-07.
- Gate issue is `issues/041_project_memory_execution_summary_gate.md`.
- Project Memory execution summary gate was approved by 总控决策席 on 2026-07-07 for architecture boundary definition only.
- Project Memory execution summary boundaries are defined in `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md`.
- Boundary issue is `issues/042_project_memory_execution_summary_boundaries.md`.
- Delivery evidence is `reviews/035_project_memory_execution_summary_boundaries_review.md`.
- Recommended first slice is documentation-only `knowledge/EXECUTION_SUMMARY_MEMORY.md`.
- Project Memory execution summary boundaries were verified by 质量运行席 on 2026-07-07.
- Project Memory execution summary boundaries were accepted by 产品规划席 on 2026-07-07.
- First implementation issue is `issues/043_project_memory_execution_summary.md`.
- Execution summary memory artifact is `knowledge/EXECUTION_SUMMARY_MEMORY.md`.
- Delivery evidence is `reviews/036_project_memory_execution_summary_review.md`.
- Project Memory Execution Summary was verified by 质量运行席 on 2026-07-07.
- Project Memory Execution Summary was accepted by 产品规划席 on 2026-07-07.
- Project Memory execution summary first slice is complete.
- Next bounded phase selection is pending with 产品规划席.

Sources:

- `issues/012_sprint_3_lightweight_role_responsibility_gate.md`
- `issues/014_sprint_3_role_context_runtime_reference_gate.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`

## Architecture Segment

- Sprint 1 selected-task detail remains the accepted execution-evidence surface.
- Sprint 2 unified task console remains a frontend composition boundary over existing task composer, compact task history, existing run action, selected detail, and minimal review signals derived from existing state.
- Project Memory is a deterministic project-fact read model over existing source-of-truth files and existing execution summary memory.
- Project Memory does not replace `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, ADRs, issues, reviews, or Result Store execution evidence.
- Corrections must happen in the owning source file first.
- Sprint 3 may define lightweight role profiles and responsibility boundaries, but must not implement Employee CRUD, company organization, multi-agent routing, or agent abstraction.
- Sprint 3 lightweight roles are deterministic source-controlled execution guidance profiles, not employees, agents, departments, organization units, staffing records, or routing nodes.
- The first implementation should define role profiles only; runtime prompt integration, task evidence attachment, UI, backend metadata, and persistence are deferred unless separately approved.
- First implementation is approved only as deterministic source-controlled role profiles. Runtime prompt integration, task evidence attachment, UI, backend metadata, and persistence remain deferred unless separately approved.
- `knowledge/ROLE_PROFILES.md` defines fixed deterministic profiles for the five Curis operating seats with stable profile ids, responsibility boundaries, minimal context references, expected output shapes, escalation triggers, and source references.
- Role-context runtime reference has only a first-slice read-only helper implementation; runtime prompt integration remains deferred.
- Future runtime reference is limited to read-only prompt/context guidance from an explicit issue-declared profile id unless separately approved.
- Missing profile id must not imply a default role.
- Any future runtime caller must be constrained by a separately approved issue-declared profile id.
- Runtime implementation, task evidence attachment, UI selector, backend metadata, persistence, task-role association, routing, tool selection, workflow mutation, state mutation, and execution-loop behavior remain blocked.
- The first runtime reference slice is a read-only helper that builds a compact role-context excerpt from explicit profile id `curis.role.system-delivery.v1`.
- Missing or invalid profile ids return no role context and do not infer or create a default role.
- The first slice does not integrate with prompt execution, APIs, task evidence, UI, persistence, routing, workflow generation, task state, learning, meta-development, evolution governor, or storage behavior.
- Sprint 4 is approved for architecture boundary definition only for bounded multi-entry and operational UI inside the existing AI Task Executor product shell.
- Sprint 4 multi-entry means multiple UI affordances for the same existing task workflow, not new task semantics.
- Sprint 4 advanced UI means operational clarity over task entry, history, selected detail, status, and review signals, not dashboards.
- Sprint 4 first implementation should be frontend-only unless a separate approved API or read-model gap exists.
- Sprint 4 must not add external entry channels, complex UI, API semantic changes, persistence, new execution behavior, or future-layer leakage into L5 company organization or L6 economy.
- Sprint 4 first implementation is limited to frontend-only entry affordances that prefill or structure ordinary task content for the existing Task API.
- Sprint 4 first implementation adds three local starters inside `frontend/app`: Plan Next Slice, Review Execution, and Verify Boundary.
- Starter selection updates only existing composer content and local presentation state.
- Task submission still sends `{ content }` to the existing Task API.
- Sprint 4 first implementation quality verification passed for commit `c528ed72`.
- Sprint 4 first implementation was accepted by 产品规划席 on 2026-07-06.
- AI Task Executor MVP readiness review is approved as gate-only planning and gap classification; no implementation is approved.
- AI Task Executor MVP readiness review may classify gaps as blocker, stabilization, verification, documentation, or future product scope.
- Readiness review covers existing accepted MVP surfaces only: Task API `{ content }`, run action, task status/history, selected-task detail evidence, Project Memory, role profiles/helper, and Sprint 4 frontend-only entry starters.
- Any follow-up implementation requires separate approval after classification and routing.
- MVP readiness boundary verification planning passed for commit `031321bf`; no scope blockers were found by 质量运行席.
- MVP readiness boundary verification plan was accepted by 产品规划席 on 2026-07-06.
- MVP readiness review found no blocker gaps.
- Classified gaps are stabilization, verification, or future product scope.
- MVP readiness review quality verification passed for commit `e657b884`; no readiness blockers or scope blockers were found by 质量运行席.
- MVP readiness review was accepted by 产品规划席 on 2026-07-06.
- Operation-console Chinese localization was completed as a frontend-only presentation slice in `issues/020_chinese_operation_console_localization.md`.
- Localization evidence is recorded in `reviews/019_chinese_operation_console_localization_review.md`.
- MVP release-candidate PRD slice is `docs/sprints/ai-task-executor-mvp-release-candidate.md`.
- MVP release-candidate gate issue is `issues/021_ai_task_executor_mvp_release_candidate_gate.md`.
- Release-candidate gate allows stabilization, verification, startup/deployment documentation, release checklist, rollback notes, and local/demo deployment instructions only.
- Release-candidate gate does not approve implementation, new product features, API semantic changes, persistence, external services, or future-layer scope.
- MVP release-candidate exact plan is limited to verification command standardization, startup docs, local/demo deployment docs, release checklist, rollback notes, and stabilization triage.
- Release-candidate implementation remains blocked until a separate approved issue defines exact scope and verification.
- MVP release-candidate boundary verification passed for commit `d94fc084`; no scope blockers were found by 质量运行席.
- MVP release-candidate boundaries and exact plan were accepted by 产品规划席.
- Implementation is unblocked only for documentation/local configuration guidance scope in `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`.
- Release-candidate package covers RC-PLAN-001 through RC-PLAN-006 in source-controlled documentation.
- FastAPI Python 3.14 warning triage decision is `defer-known-gap`; no code fix was made.
- Release-candidate stabilization/documentation package quality verification passed for commit `33d89da7`; no blockers were found by 质量运行席.
- First-version local/demo release verification issue is `issues/023_ai_task_executor_mvp_local_demo_release_verification.md`.
- First-version local/demo release candidate verification passed at restore point `c5011acd`.
- Release verification evidence is recorded in `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`.
- API smoke passed for health, task creation, and task history using the real local FastAPI server and SQLite storage at `/private/tmp/curis_release_smoke.sqlite`.
- Product acceptance completed on 2026-07-06.
- First-version release-candidate closeout and v0.1 release record/tag decision are complete.
- AI Task Executor MVP v0.1 local/demo release was closed by 产品规划席 on 2026-07-06.
- Release record is `docs/release/ai-task-executor-mvp-v0.1-release-record.md`.
- Closeout evidence is `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`.
- Local tag decision is to create `v0.1` after the closeout commit; verified code restore point remains `c5011acd`.
- Post-v0.1 Execution Reliability gate was approved by 总控决策席 on 2026-07-06.
- Gate issue is `issues/025_post_v0_1_execution_reliability_gate.md`.
- Gate brief is `docs/sprints/post-v0.1-execution-reliability.md`.
- The gate approves architecture boundary definition only; implementation remains blocked until a later approved issue.
- Architecture boundaries are defined in `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`.
- Boundary issue is `issues/026_post_v0_1_execution_reliability_boundaries.md`.
- Delivery evidence is `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`.
- Recommended first slice is `Run Evidence Reliability`.
- Quality verification passed on 2026-07-06; no implementation drift or scope blockers were found.
- Product acceptance completed on 2026-07-06.
- First implementation issue is `issues/027_run_evidence_reliability_first_slice.md`.
- First slice is limited to backend tests and evidence quality around existing run behavior.
- Run Evidence Reliability first slice was implemented by 系统交付席 on 2026-07-06.
- Delivery evidence is `reviews/025_run_evidence_reliability_first_slice_review.md`.
- Backend coverage now verifies successful run evidence chain and failed run evidence chain.
- Duplicate failed-run tool trace persistence was fixed.
- Backend regression passed with 36 tests.
- Quality verification passed on 2026-07-06.
- Focused reliability tests passed with 2 tests.
- Backend regression passed with 36 tests.
- Frontend diff guard passed; no frontend files changed.
- Scope scan found no forbidden implementation drift.
- Product acceptance completed on 2026-07-06.
- Next proposed reliability slice is Workflow Error/Fallback Observability.
- Gate issue is `issues/028_workflow_error_fallback_observability_gate.md`.
- Gate decision was approved by 总控决策席 on 2026-07-06.
- Gate approval allows architecture boundary definition only and does not approve implementation.
- Architecture boundaries were defined by 系统交付席 on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`.
- Boundary issue is `issues/029_workflow_error_fallback_observability_boundaries.md`.
- Boundary evidence is `reviews/026_workflow_error_fallback_observability_boundaries_review.md`.
- Recommended first implementation slice is `Workflow Error/Fallback Evidence Map`.
- Quality verification passed on 2026-07-06.
- No backend/frontend implementation diff or scope blockers were found.
- Product acceptance completed on 2026-07-06.
- First implementation issue is `issues/030_workflow_error_fallback_evidence_map.md`.
- Implementation is limited to backend tests and evidence documentation for existing workflow error/fallback behavior.
- Implementation completed by 系统交付席 on 2026-07-06.
- Delivery evidence is `reviews/027_workflow_error_fallback_evidence_map_review.md`.
- Backend test coverage now includes successful fallback evidence map and full fallback-chain failure evidence map.
- No backend production files or frontend files were changed.
- Backend regression passed with 38 tests.
- Quality verification passed on 2026-07-06.
- No frontend diff, backend production diff, or scope blockers were found.
- Product acceptance completed on 2026-07-06.
- Next proposed reliability slice is Evolution Decision Evidence Reliability.
- Gate issue is `issues/031_evolution_decision_evidence_reliability_gate.md`.
- Gate decision was approved by 总控决策席 on 2026-07-06.
- Gate approval allows architecture boundary definition only and does not approve implementation.
- Architecture boundaries were defined by 系统交付席 on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`.
- Boundary issue is `issues/032_evolution_decision_evidence_reliability_boundaries.md`.
- Boundary evidence is `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`.
- Recommended first implementation slice is `Evolution Decision Evidence Map`.
- Quality verification passed on 2026-07-06.
- No backend/frontend implementation diff or scope blockers were found.
- Product acceptance completed on 2026-07-06.
- First implementation issue is `issues/033_evolution_decision_evidence_map.md`.
- Implementation is limited to backend tests and evidence documentation for existing Evolution Governor decision behavior.
- Implementation completed by 系统交付席 on 2026-07-06.
- Delivery evidence is `reviews/029_evolution_decision_evidence_map_review.md`.
- Backend test coverage now includes stable do-not-evolve, threshold-triggered controlled proposal/simulation/rollback, locked-module postpone risk, and evolution-decision API evidence.
- No backend production files or frontend files were changed.
- Backend regression passed with 41 tests.
- Quality verification passed on 2026-07-06.
- No frontend diff, backend production diff, or scope blockers were found.
- Product acceptance completed on 2026-07-06.
- Post-v0.1 reliability closeout gate issue is `issues/034_post_v0_1_execution_reliability_closeout_gate.md`.
- Gate decision was approved by 总控决策席 on 2026-07-06.
- Gate approval allows closeout review planning only and does not approve implementation.
- Closeout review was completed by 系统交付席 on 2026-07-06.
- Closeout evidence is `reviews/030_post_v0_1_execution_reliability_closeout_review.md`.
- No blocker gaps were identified for the post-v0.1 reliability phase.
- Recommended next move after quality verification and product acceptance is next-phase selection by 产品规划席.
- Quality verification passed on 2026-07-06.
- Backend regression passed with 41 tests.
- No backend/frontend implementation diff or scope blockers were found.

Sources:

- `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`
- `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`
- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`
- `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`
- `knowledge/ROLE_PROFILES.md`
- `reviews/009_project_memory_foundation_architecture_boundaries_review.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`

## Source Ownership Segment

- `knowledge/`: low-token context layer.
- `PROJECT_STATUS.md`: sprint and project snapshot.
- `TASKS.md`: task queue.
- `docs/decisions/`: architecture decisions.
- `issues/`: executable work queue.
- `reviews/`: verification and evidence record.
- Result Store execution summaries: execution evidence only, not product or architecture authority.

Sources:

- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `AGENTS.md`

## Verification Segment

Completed checks for this first slice:

- `git diff --check`
- Deterministic artifact check: `LC_ALL=C sed -n '1,220p' knowledge/PROJECT_MEMORY.md > /tmp/curis_project_memory_check.md && cmp -s knowledge/PROJECT_MEMORY.md /tmp/curis_project_memory_check.md`
- Source reference check: `rg -n "^- \`|^Sources:" knowledge/PROJECT_MEMORY.md`
- Forbidden-scope scan from `issues/011_sprint_2_project_memory_first_slice.md`.
- Quality verification passed for amended commit `3e44d9c`.
- Product acceptance completed on 2026-07-06.
- Sprint 3 lightweight role architecture-boundary evidence is ready for 质量运行席 verification planning in `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`.
- Sprint 3 role profiles first-slice quality verification passed for commit `53d8a30` in `reviews/012_sprint_3_role_profiles_first_slice_review.md`.
- Sprint 3 role-context runtime reference architecture-boundary verification planning passed for commit `c72e86dd` and was accepted by 产品规划席 in `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`.
- First role-context runtime reference implementation issue is `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`.
- Sprint 3 role-context runtime reference first-slice quality verification passed for commit `71e9577b` in `reviews/014_role_context_runtime_reference_first_slice_review.md`.
- Sprint 3 role-context runtime reference first slice was accepted by 产品规划席 on 2026-07-06.
- Sprint 4 multi-entry and advanced UI PRD slice is drafted for 总控决策席 gate review.
- Sprint 3 closeout and Sprint 4 entry were approved by 总控决策席 on 2026-07-06.
- Sprint 4 multi-entry UI architecture-boundary verification planning passed for commit `cf96d58b` in `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`.
- Sprint 4 multi-entry UI architecture-boundary verification planning was accepted by 产品规划席 on 2026-07-06.
- First Sprint 4 implementation issue is `issues/017_sprint_4_multi_entry_ui_first_slice.md`.
- Sprint 4 multi-entry UI first slice is implemented by 系统交付席 in `frontend/app`.
- Delivery evidence is recorded in `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.
- Implementation verification passed targeted frontend view-model tests, frontend lint, frontend build, backend diff guard, frontend diff review, diff check, and forbidden-scope scan.
- Quality verification passed for commit `c528ed72`; no blockers were found by 质量运行席.
- Product acceptance completed on 2026-07-06.
- Sprint 4 closeout and MVP readiness gate was approved by 总控决策席 on 2026-07-06.
- AI Task Executor MVP readiness boundaries are defined in `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md`.
- Boundary and verification-planning evidence is recorded in `reviews/017_ai_task_executor_mvp_readiness_boundaries_review.md`.
- MVP readiness boundary verification planning passed for commit `031321bf`.
- Backend regression passed with `backend/.venv/bin/python -m unittest discover tests`; system `python3` lacks the required FastAPI dependency unless prepared separately.
- Product acceptance completed on 2026-07-06.
- AI Task Executor MVP readiness review was conducted by 系统交付席.
- Evidence is recorded in `reviews/018_ai_task_executor_mvp_readiness_review.md`.
- Current verification passed backend regression, frontend view-model tests, frontend lint, frontend build, backend/frontend diff guard, diff hygiene, and evidence scans.
- No blocker readiness gaps were found.
- MVP readiness review quality verification passed for commit `e657b884`.
- Product acceptance completed on 2026-07-06.
- Next readiness work is release-candidate stabilization/documentation implementation.
- Operation-console Chinese localization verification passed frontend view-model tests, lint, build, and backend diff guard.
- Release-candidate stabilization/documentation package is implemented in `docs/release/ai-task-executor-mvp-v0.1.md`.
- Delivery evidence is recorded in `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`.
- Backend regression, frontend view-model tests, lint, build, backend/frontend diff guard, diff hygiene, Chinese UI guard, forbidden-scope scan, and RC plan coverage scan passed.
- Release-candidate stabilization/documentation package quality verification passed for commit `33d89da7`.
- Release-candidate stabilization/documentation package was accepted by 产品规划席 on 2026-07-06.
- AI Task Executor MVP release-candidate boundaries are defined in `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`.
- Boundary and stabilization/documentation planning evidence is recorded in `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`.
- MVP release-candidate boundary verification passed for commit `d94fc084`.
- Product acceptance completed on 2026-07-06.
- Release-candidate stabilization/documentation implementation issue opened on 2026-07-06.
- Release-candidate stabilization/documentation package accepted on 2026-07-06.
- First-version local/demo release verification issue opened on 2026-07-06.
- First-version local/demo release candidate verification passed at restore point `c5011acd`.
- First-version local/demo release candidate verification accepted by 产品规划席 on 2026-07-06.
- AI Task Executor MVP v0.1 local/demo release closed by 产品规划席 on 2026-07-06.
- Post-v0.1 Execution Reliability gate approved by 总控决策席 on 2026-07-06.
- Post-v0.1 Execution Reliability architecture boundaries defined by 系统交付席 on 2026-07-06.
- Post-v0.1 Execution Reliability architecture boundaries verified by 质量运行席 on 2026-07-06.
- Post-v0.1 Execution Reliability architecture boundaries accepted by 产品规划席 on 2026-07-06.
- Run Evidence Reliability first slice implemented by 系统交付席 on 2026-07-06.
- Next work is quality verification by 质量运行席.

Sources:

- `issues/011_sprint_2_project_memory_first_slice.md`
- `reviews/010_project_memory_first_slice_review.md`
- `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`
- `reviews/012_sprint_3_role_profiles_first_slice_review.md`
- `issues/014_sprint_3_role_context_runtime_reference_gate.md`
- `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`
- `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`
- `reviews/014_role_context_runtime_reference_first_slice_review.md`
- `docs/sprints/sprint-4-multi-entry-advanced-ui.md`
- `issues/016_sprint_3_closeout_sprint_4_entry_gate.md`
- `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`
- `issues/017_sprint_4_multi_entry_ui_first_slice.md`
- `reviews/018_ai_task_executor_mvp_readiness_review.md`
- `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`
- `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`

## Guardrail Segment

Project Memory first slice is documentation-only. It adds no backend implementation, frontend implementation, API, persistence table, vector index, embedding flow, external service, hidden store, task execution change, or evolution behavior.

Future implementation must stop and route back for approval before adding backend/frontend implementation files or any read API.

Sprint 3 lightweight role first implementation should remain source-controlled and profile-only. It must not add Employee CRUD, employee expansion, company organization, multi-agent routing, agent abstraction, ROI/economy, role dashboard, persistence, external role service, external memory service, new execution behavior, or automatic evolution behavior.

`knowledge/ROLE_PROFILES.md` is guidance-only. It does not create employees, agents, organization units, routing nodes, runtime behavior, backend metadata, persistence, task-role association, UI selection, or execution evidence attachment.

ADR-0006 does not approve runtime prompt integration. Future role-context runtime reference must not proceed beyond approved first-slice helper behavior without a separate approved implementation issue and quality plan.

The T-054 first slice is approved only as read-only role-context reference helper behavior. Runtime prompt integration, task evidence attachment, UI selector, backend metadata, persistence, task-role association, and API semantic changes remain deferred.

Sprint 4 implementation is unblocked only for `issues/017_sprint_4_multi_entry_ui_first_slice.md` and remains bounded to existing AI Task Executor product-shell behavior. Future Sprint 4 expansion still requires approved issue scope.

The Sprint 4 first slice must remain frontend-only under `frontend/app`: no backend/API changes, persistence, task type, role selector, external channel, execution-loop behavior change, or future-layer scope.

AI Task Executor MVP readiness review is approved only as a planning gate. It must not implement features or expand scope before a separate approved issue defines exact scope and verification.

ADR-0008 preserves gate-only readiness planning. Gap classification does not approve implementation; classified gaps must be routed by class and owner seat before any code, API, persistence, UI, runtime, external-channel, or future-layer change.

For readiness verification, use the repo virtualenv command `backend/.venv/bin/python -m unittest discover tests` for backend tests unless the system Python environment is explicitly prepared.

No readiness implementation is approved yet. The accepted next state is MVP release-candidate or stabilization follow-up decision only.

AI Task Executor MVP release-candidate entry is approved only for boundary definition, stabilization/documentation planning, and regression verification planning. Implementation remains blocked until a separate approved issue defines exact scope and verification.

ADR-0009 preserves release-candidate planning only. The approved plan may standardize verification commands, document startup/local-demo deployment, define release checklist and rollback notes, and triage stabilization, but it does not approve code, API, persistence, runtime, external service, or product-scope changes.

质量运行席 verified the release-candidate boundaries and exact stabilization/documentation plan for `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`; release-candidate implementation remains blocked until a separate approved issue defines exact scope and verification.

产品规划席 accepted the release-candidate boundaries and exact stabilization/documentation plan. Accepted RC items are RC-PLAN-001 through RC-PLAN-006 only; implementation still requires a separate scoped issue.

`issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md` is the separate scoped issue. It allows documentation-only release artifacts, verification command standardization, startup/local-demo docs, release checklist, rollback notes, FastAPI warning triage, `.env.example` or equivalent local configuration guidance if needed, and source-of-truth updates. It forbids backend/frontend behavior changes, API semantic changes, persistence, execution behavior changes, new product features, and fixing the FastAPI warning without a separate approved stabilization issue.

The release-candidate documentation package does not approve backend/frontend implementation changes. Any future stabilization code fix, including a FastAPI warning fix, requires a separate approved issue.

质量运行席 verified the release-candidate stabilization/documentation package in `docs/release/ai-task-executor-mvp-v0.1.md`; 产品规划席 accepted it on 2026-07-06.

`issues/023_ai_task_executor_mvp_local_demo_release_verification.md` verifies the accepted release runbook. It allows verification evidence, regressions, API smoke, Chinese UI guard, forbidden-scope scan, source-of-truth alignment, and restore point capture only. It forbids implementation changes, mock/simulation substitution, external services, FastAPI warning fix, and future-layer scope.

质量运行席 verified the first-version local/demo release candidate in `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`; 产品规划席 accepted the verification on 2026-07-06.

The accepted local/demo verification approves evidence only. It does not approve implementation changes, mock/simulation substitution, new features, API semantic changes, persistence/schema changes, execution behavior changes, external services, complex UI/dashboard, FastAPI warning fix, or future-layer scope.

产品规划席 closed AI Task Executor MVP v0.1 as a local/demo first version in `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`. This closeout approves release documentation and local tag semantics only; it does not approve hosted production deployment or future-layer implementation.

总控决策席 approved post-v0.1 Execution Reliability as the next gate. This phase strengthens the existing AI Task Executor execution loop before opening L5 company organization, L6 ROI/economy, business modules, external channels, or broader UI.

系统交付席 defined post-v0.1 Execution Reliability boundaries in ADR-0010. The approved boundary areas are run endpoint verification, execution trace/result evidence quality, workflow/error/fallback observability, existing Evolution Governor evidence, and current L1-L4 coverage planning. Implementation remains blocked until quality planning and product acceptance.

质量运行席 verified ADR-0010 and the boundary package in `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`. Verification found no backend/frontend implementation diff, no diff hygiene issues, and no scope blockers; product acceptance is now recorded.

产品规划席 accepted ADR-0010 and opened `issues/027_run_evidence_reliability_first_slice.md`. The first implementation slice may add backend tests and evidence quality for existing run behavior only; API semantics, persistence schema, UI, external services, new features, new execution behavior, and future-layer scope remain blocked.

系统交付席 implemented Run Evidence Reliability by adding backend coverage for successful and failed run evidence chains and by preventing duplicate failed-run tool trace persistence. API semantics, persistence schema, UI, external services, new product features, new execution behavior, automatic evolution behavior changes, and future-layer scope remain blocked.

The accepted readiness review mapped evidence and classified gaps only. It did not implement code or expand product scope.

The readiness review classified no blockers. Future follow-up must still be separately approved by gap class before implementation.

质量运行席 verified the readiness evidence map and gap classification for `reviews/018_ai_task_executor_mvp_readiness_review.md`; no implementation or scope expansion was approved.

Operation-console localization is presentation-only. It must not be treated as approval for backend/API, execution-loop, persistence, dashboard, external-channel, ROI, business-module, Employee CRUD, multi-agent routing, agent abstraction, or future-layer changes.

Sources:

- `issues/011_sprint_2_project_memory_first_slice.md`
- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`
- `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`
- `knowledge/ROLE_PROFILES.md`
