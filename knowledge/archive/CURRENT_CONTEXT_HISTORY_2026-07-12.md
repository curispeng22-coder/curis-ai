# Current Context

Status: Deprecated

## Current Sprint

Phase-1C CEO Office UI First Slice.

## Current Objective

Implement the product-approved CEO Office first slice using existing Workspace APIs only, while preserving the current execution workspace as a secondary entry.

## Current Gate

`issues/phase1c_ceo_office_ui_first_slice.md` is approved for 系统交付席 frontend-only implementation.

Runtime baseline: Curis Workspace Tool System v1.8 plus the verified Phase-1 AI Company Runtime Foundation.

Final product goal: AI Company System.

Current launch scope: AI Company OS CEO Office first frontend slice over the existing Workspace runtime.

Current-stage rule: implement only the approved CEO Office first slice. Company and Project are product entry points; Task remains an internal execution substrate and the existing execution console remains a secondary entry.

Allowed loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Active Constraints

- Frontend-only implementation inside the approved Issue and Allowed Files.
- Do not modify backend, API, data model, Admin, Billing, Marketplace, Credential Vault, or Workflow Runtime.
- Do not create Decision Center, Strategic Meeting Room, Brainstorm Room, or Report Inbox runtime behavior without separate Contracts and executable Issues.
- Do not use mock data to simulate unapproved runtime behavior.
- UI direction, information architecture, user flows, interaction principles, and visual acceptance remain product-owned.
- Keep context reads minimal by role.

## Active Curis Role Model

- 总控决策席：direction, gate decisions, scope conflict, sprint advancement.
- 产品规划席：product scope, PRD, backlog, acceptance criteria, source-of-truth hygiene.
- 系统交付席：architecture boundaries, implementation, technical review, commits.
- 质量运行席：verification, commands, environment reliability, completion evidence.
- 安全边界席：secrets, external services, data handling, privacy, security blockers.

Standalone legacy roles are no longer active dispatch targets.

## Current Status

- 2026-07-10: Phase 1A Company / Project Runtime Backend is implemented as a Workspace-only backend foundation. Added tenant-scoped `companies` and `projects` persistence, lazy per-tenant default `Curis AI Company`, Company CRUD APIs, Project CRUD APIs, Company/Department/Employee ownership validation, and tenant isolation. The product entry is now represented by Company -> Project -> Department -> Employee/Skill/Tool -> Workflow/Task execution substrate; direct Task remains preserved only as an internal/compatibility substrate. No CEO Office, Meeting, Secretary, Employee Persona, Billing, Payment, Invoice, Marketplace, ROI, Admin Commercial Configuration, Credential Vault boundary, Workflow Runtime, Employee Runtime, Tool Router, Model Gateway, or Workspace `/api/platform/*` runtime change was introduced.
- 2026-07-10: Phase 1A AI Company OS Backend Foundation contracts are prepared as documentation-only source-of-truth updates. Added `docs/contracts/company-runtime-contract.md`, `docs/contracts/department-runtime-contract.md`, `docs/contracts/project-runtime-contract.md`, `docs/contracts/skill-runtime-contract.md`, `docs/contracts/tool-runtime-contract.md`, and `docs/review/phase1-ai-rnd-company-mvp-gap-list.md`. The product entry is corrected from Task-first to Company -> Project -> Department -> Employee/Skill/Tool -> Workflow/Task execution substrate. Existing Task, Orchestrator, Tool Router, Model Gateway, Credential Vault, Workflow Runtime, Employee Runtime, usage_event, audit_event, and value_event remain preserved. No backend runtime code, execution chain, Workflow Runtime, Employee Runtime, Credential Vault, Pricing, Quota, Billing, Payment, Invoice, ROI, Marketplace, or `/api/platform/*` Workspace call was introduced.
- 2026-07-10: Phase-9A Workspace Commercial Support Audit is completed as documentation-only evidence in `docs/review/phase9a-employee-seat-meter-review.md`, `docs/review/phase9a-capability-meter-review.md`, `docs/review/phase9a-commercial-boundary-check.md`, and `docs/review/phase9a-workspace-commercial-hardcode-check.md`. Workspace can support future Admin commercial metering for employee seats, capability/package usage evidence, workflow/employee/capability/model/token attribution, and redacted cost metadata while Admin remains responsible for Pricing, Quota, Package, Billing rules, BillingEvent, Invoice, and payment. No Billing, Pricing, Quota, Payment, Invoice, Workflow Runtime, Employee Runtime, Credential Vault, Task Execution, Admin Platform, or `/api/platform/*` Workspace runtime change was introduced.
- 2026-07-09: Source Control Stabilization / Git Baseline Freeze is completed as a PMO checkpoint process in `docs/pmo/source-control-baseline-freeze.md`. The freeze records why Phase-5 through Phase-9A accumulated in one dirty worktree, classifies current files by Admin / Workspace / shared ownership, captures verification results, and sets post-checkpoint rules: clean `git status` before every issue, one issue per commit, docs-only phases cannot include source changes, code phases cannot include unrelated docs, and cross-line edits require shared contract/gate. Verification before checkpoint passed: `git diff --check`, backend 356-test regression, frontend 32-test unit run, frontend lint, frontend build, scoped secret scan, and Workspace `/api/platform/*` runtime call-pattern scan. The checkpoint is a source-control baseline, not a feature approval or release acceptance decision.
- 2026-07-09: Phase-8.6 Workspace Commercial Configuration Audit is completed in `docs/review/phase86-workspace-commercial-audit.md` as audit-only documentation. Workspace commercial-related data was reviewed across Employee, Workflow, Capability, and Usage. Conclusion: Workspace already supplies commercial evidence for tenant/employee/workflow/step/capability/model/token/redacted-cost attribution, while official employee templates, official R&D SOP workflow templates, capability package composition, plan/quota limits, employee seat semantics, package versioning, marketplace enablement, BillingEvent, and Invoice logic should migrate to future Admin Commercial Configuration gates. Workspace should keep tenant_private capability metadata, credential_ref binding/resolver boundary, EmployeeInstance/WorkflowRun runtime records, usage_event/audit_event generation, and task/workflow execution. No Task Execution, Workflow Runtime, Employee Runtime, Credential Vault, Billing, Admin governance, Marketplace, ROI, or code behavior change was introduced.
- 2026-07-09: Curis first commercial package model is frozen in `docs/decisions/commercial-package-model-v1.md`; `docs/contracts/pricing-contract.md` and `docs/decisions/commercial-roadmap.md` are aligned to Frozen v1. The frozen ladder is Free -> Pro -> Enterprise, with subscription base, token usage, capability packages, AI employee seats, and future value-based pricing reserve. This freezes package model semantics, not real-world price points, Billing implementation, payment, invoice generation, Marketplace revenue share, Value Pricing, ROI, Usage Event changes, Workflow changes, Employee Runtime changes, Credential Vault changes, Workspace execution-chain changes, or Admin runtime changes.
- 2026-07-09: Phase-8.5 Commercial Readiness support is completed as documentation/research only in `docs/research/domain/workspace-commercial-readiness.md`. Workspace commercial support was checked across Usage Event fields, Capability Package references, and Employee Seat count basis. Conclusion: Workspace already supports required commercial evidence for tenant/employee/workflow/capability/model/token/cost attribution and Usage Meter aggregation; package composition can reference tools/connectors/workflows/employee templates by existing ids; active employee seat counting is possible from EmployeeInstance tenant/status/enabled/template/role data. No new Workspace fields are required now. Explicit commercial `employee_type`, `package_id`, package versioning, BillingEvent rating, invoice/payment, marketplace monetization, and value-based pricing remain future-gated. No Workflow, Credential Vault, Employee Runtime, Task Execution chain, Billing, or `/api/platform/*` Workspace runtime changes were introduced.
- 2026-07-09: Phase-8 Workspace Billing Support is implemented and locally verified after G1 Billing Gate approval. Added `UsageMeterService`, Admin-read-only `/api/platform/usage-meter`, additive usage_event `token_usage` and `cost_metadata` projection/write metadata, `issues/phase8_workspace_billing_support.md`, and `docs/release/phase8-workspace-billing-support-implementation-report.md`. Verification passed: Phase-8 focused tests, targeted Workspace/Admin integration tests, backend regression, frontend view-model tests, frontend lint/build, scoped `git diff --check`, scoped secret scan, and Workspace frontend runtime `/api/platform/*` scan. Scope remains Workspace usage evidence support only: no Billing UI, Payment, Invoice, BillingEvent generation, charge logic, Credential Vault change, Workflow Runtime change, Employee Runtime change, Task Execution chain change, or Workspace runtime `/api/platform/*` call.
- 2026-07-09: Phase-7.7 Billing Readiness is prepared as contract/domain/issue only. Updated `docs/contracts/billing-domain-contract.md`; added `docs/contracts/capability-package-contract.md`, `docs/contracts/employee-seat-contract.md`, `docs/contracts/commercial-data-flow.md`, and `issues/phase8_billing_mvp.md`. The Hybrid commercial model now has a technical Billing domain basis: BillingSubject, Plan, Quota, Usage Meter, BillingEvent, Capability Package, Employee Seat, and Commercial Data Flow. Curis is ready for Phase-8 Billing MVP gate review, but Billing, payment, invoice generation/UI, Marketplace revenue share, Value Pricing, Usage Event changes, Workflow changes, Employee Runtime changes, Credential Vault changes, Workspace execution-chain changes, and Admin runtime changes remain unapproved.
- 2026-07-09: Phase-7.6 Commercial Contract Freeze is prepared as contract/decision only. Added `docs/contracts/pricing-contract.md`, `docs/contracts/billing-domain-contract.md`, and `docs/decisions/commercial-roadmap.md`. The frozen commercial direction is Hybrid: tiered subscription, token/model usage, capability packages, AI employee seats, and future value-based pricing. Commercial roadmap gates are G0 Usage Observation, G1 Plans + Model Quota Billing, G2 AI Employee Seats, G3 Marketplace Revenue Share, and G4 Value-Based Pricing. These files define future Billing MVP basis but do not approve Billing, payment, invoice generation, Usage Event structure changes, Workspace execution-chain changes, Admin implementation changes, ROI, Marketplace, or new commercial features.
- 2026-07-09: Phase-7.5 Value Event Validation is prepared as documentation/contract/research only. Added/updated `docs/contracts/value-event-contract.md`, `docs/contracts/value-event-generation-flow.md`, `docs/contracts/value-event-type-contract.md`, `docs/contracts/usage-value-event-boundary.md`, `docs/research/domain/value-measurement-research.md`, `docs/research/domain/billing-readiness-assessment.md`, and `docs/release/phase75-commercial-validation-value-event-design.md`; updated `issues/phase7_billing_readiness.md`. Recommendation: Value Event is reasonable as user-confirmed commercial validation evidence; first version should generate drafts after Execution Result and require user confirmation of `estimated_value`; usage_event records AI consumption, value_event records AI-created value estimates, and future Admin-owned billing_event records rated billable interpretation. Curis is ready for Billing Readiness planning, not Billing implementation. No ROI, Billing, payment, Task Execution change, Workflow Runtime change, Employee Runtime change, Credential Vault change, new AI employee, new workflow, or new business department is approved.
- 2026-07-09: Phase-7 Demo Polish + Commercial Readiness preparation is completed in `docs/release/phase7-demo-polish-commercial-readiness.md`. Demo package artifacts: `docs/demo/phase7-demo-seed.json`, `tools/phase7_check_local_demo_env.py`, `tools/phase7_start_local_demo.sh`, `tools/phase7_stable_demo_e2e.py`, and `docs/demo/phase7-stable-demo-script.md`. Billing readiness is drafted in `issues/phase7_billing_readiness.md`; conclusion: usage_event is strong enough for usage analytics and billing input mapping, but `estimated_cost` is not authoritative billing cost, so Billing MVP should introduce Admin-owned billing_event/plan/quota/invoice models after gate approval. Verification passed: environment check, stable demo E2E, backend regression, frontend unit tests/lint/build, Workspace `/api/platform/*` runtime scan, scoped secret scan, and `git diff --check`. No Marketplace, Workflow Plus, formal Billing, ROI, new business module, Credential Vault boundary change, Admin plaintext access, or Workspace platform runtime call was introduced.
- 2026-07-09: Phase-6.5 Post-Workflow Roadmap Review is prepared in `docs/release/phase65-post-workflow-roadmap-review.md`. Recommendation: P0 `issues/phase7_local_demo_release_hardening_gate.md` to make the Phase-4/5/6 demo repeatable; P1 `issues/phase7_production_credential_vault_gate.md` for production Vault/KMS custody before hosted customer private credentials; P1/P2 `issues/phase7_billing_usage_contract_gate.md` as an Admin-led billing contract gate with Workspace compatibility review; P2 Workflow v2 boundary later; P3 Marketplace deferred. This phase is documentation/issue drafting only and does not implement new runtime behavior, Billing, Marketplace, ROI, Workflow v2, business modules, or Credential Vault boundary changes.
- 2026-07-09: Phase-6 Workflow MVP Demo Freeze is completed in `docs/demo/phase6-workflow-mvp-demo-script.md` and `docs/release/phase6-workflow-mvp-demo-freeze-report.md`. The frozen local/demo chain confirms CEO requirement creation, Software R&D SOP WorkflowRun startup, Tech Lead task decomposition, Product Manager requirement supplementation, Architect technical plan, Frontend Engineer step, Backend Engineer step, QA verification, Tech Lead final report, CEO-readable final result, usage_event workflow/step/employee/capability redacted attribution, audit_event workflow-state audit, tenant_private credential_ref/resolver reuse, Admin plaintext non-visibility, and Workspace `/api/platform/*` runtime guard. Stability verification passed: focused workflow tests, focused credential resolver tests, backend regression, frontend tests/lint/build, test-output leakage checks, Workspace `/api/platform/*` runtime scan, scoped secret scan, and `git diff --check`. Phase-6 can be formally marked as Workflow MVP Demo Freeze complete.
- 2026-07-09: Phase-6 Workflow MVP RC verification is complete and documented in `docs/release/phase6-workflow-mvp-rc.md`. RC confirmed official sequential R&D SOP WorkflowTemplate, WorkflowRun creation, ordered step execution, expected employee-role assignment, StepResult persistence, Tech Lead final report, EmployeeCapabilityBinding reuse, tenant_private credential resolver reuse, workflow/step/employee/capability usage_event attribution, workflow.* audit_event attribution, tenant isolation, Workspace `/api/platform/*` runtime guard, no plaintext credential leakage, backend regression, frontend tests/lint/build, focused workflow and credential boundary tests, scoped secret scan, and `git diff --check`. Phase-6 is ready to enter Demo Freeze after product acceptance.
- 2026-07-09: Phase-6 Workflow MVP implementation is complete and documented in `docs/release/phase6-workflow-mvp-implementation-report.md`. Workspace now has official Software R&D WorkflowTemplate, tenant-scoped WorkflowInstance/WorkflowRun/WorkflowStep/StepAssignment/StepResult records, bounded `run-next-step` sequential execution, employee-role assignment, EmployeeCapabilityBinding reuse, tenant_private model execution through existing Credential Resolver and Model Gateway Adapter, workflow/step/employee usage_event attribution, workflow.* audit_event attribution, and minimal Workflow UI in the Workspace operation console. Verification passed: focused Phase-6 backend tests, backend full regression, frontend tests/lint/build, test-output leakage check, Workspace runtime `/api/platform/*` scan, scoped secret scan, and `git diff --check`. Phase-6 is ready for RC verification.
- 2026-07-09: Phase-5.5 Post-G2 Roadmap Review is prepared in `docs/release/phase55-post-g2-roadmap-review.md`, with Phase-6 development basis in `issues/phase6_workflow_mvp.md` and `docs/contracts/workflow-runtime-contract.md`. Recommendation: enter Phase-6 Workflow MVP as P0 after gate acceptance; keep Demo Polish P1/P2 parallel-safe, Billing as Admin-side planning, and Marketplace deferred to Phase-7 or later. This stage is documentation/contract/issue only and does not implement Workflow, Billing, Marketplace, ROI, business modules, or Credential Vault boundary changes.
- 2026-07-09: Phase-5 G2 Credential Vault Demo Freeze is prepared in `docs/demo/phase5-g2-credential-vault-demo-script.md` and `docs/release/phase5-g2-credential-vault-demo-freeze-report.md`. The demo script covers backend/frontend startup, tenant_private credential creation, response plaintext check, credential_ref binding to private model/tool/connector, R&D employee setup, employee private capability execution, task result review, Admin usage_event redacted attribution, Admin audit_event redacted audit, and Admin plaintext non-visibility checks. Stability verification remains green: focused resolver/leakage tests, backend regression, frontend tests/lint/build, `git diff --check`, Workspace `/api/platform/*` runtime scan, and changed production/docs secret scan passed. Phase-5 G2 is ready to freeze as a local/demo version after product acceptance.
- 2026-07-09: Phase-5 G2 Credential Vault RC verification is complete and documented in `docs/release/phase5-g2-credential-vault-rc.md`. RC verification confirmed credential creation/storage without plaintext persistence, safe API responses, local-dev credential_ref format, same-tenant resolver success, cross-tenant and disabled credential rejection, production `local-dev://` rejection, private model/tool/connector credential binding, tenant_private private model execution through resolver, redacted usage_event credential attribution, redacted credential audit_event allowlist, Admin read-only redacted observability, Workspace `/api/platform/*` runtime guard, backend regression, frontend tests/lint/build, focused test-output leakage check, `git diff --check`, and changed production/docs secret scan. No Workflow, Billing, Marketplace, ROI, business module, complex employee expansion, Admin governance change, or plaintext secret exposure was introduced.
- 2026-07-09: Phase-5 G2 Credential Vault minimum safety loop is implemented and pending RC acceptance. Workspace now has tenant-scoped credential metadata APIs, local/demo server-side credential backend, resolver-enforced credential_ref parsing, tenant isolation, production `local-dev://` rejection, private capability credential binding/unbinding, private model execution through resolver-backed Model Gateway Adapter config, redacted credential audit events, and usage_event credential attribution (`credential_id`, `credential_ref_digest`). Plaintext secrets are not persisted, returned to frontend, written to usage_event, or written to audit_event. Implementation report: `docs/release/phase5-g2-credential-vault-implementation-report.md`.
- 2026-07-09: Phase-4.5 Workspace Demo Review and Roadmap evaluation is documented in `docs/release/phase45-workspace-demo-review-roadmap.md`. Recommendation: P0 `issues/phase5_g2_credential_vault_gate.md` for real credential_ref/config_ref custody gate; P1 `issues/phase5_workflow_mvp.md` for bounded Software R&D SOP collaboration; P2 `issues/phase45_demo_polish.md` for repeatable local demo polish. No core code, Workflow, Billing, credential vault, Admin Platform governance, ROI, or new business module implementation was introduced.
- 2026-07-09: Phase-4 AI Employee System MVP Demo Freeze is prepared in `docs/demo/phase4-ai-employee-demo-script.md` and `docs/release/phase4-ai-employee-demo-freeze-report.md`. The local/demo script covers backend/frontend startup, Workspace employee templates, employee instance creation, official and tenant_private employee capability binding, selected-employee task creation/run, task result inspection, and Admin usage_event employee-attribution review. Stability verification remains green: backend regression, frontend tests, lint, build, `git diff --check`, Workspace `/api/platform/*` runtime scan, and scoped secret scan passed. Phase-4 is ready to freeze as a local/demo version after product acceptance.
- 2026-07-09: Phase-4 AI Employee System MVP RC verification is complete and documented in `docs/release/phase4-ai-employee-system-rc.md`, with review evidence in `reviews/085_phase4_ai_employee_system_rc_review.md`. RC smoke verified the six official R&D employee templates, tenant_private template isolation, Software R&D DepartmentInstance creation, EmployeeInstance creation with tenant/company/department/status/instructions fields, official and tenant_private EmployeeCapabilityBinding, selected-employee task execution, Tech Lead default routing, usage_event employee attribution, tenant isolation, catalog isolation, Workspace `/api/platform/*` runtime guard, scoped secret scan, backend regression, frontend tests, lint, build, and `git diff --check`. Phase-4 is suitable to enter Demo Freeze after product acceptance. Marketplace source remains schema/contract-reserved only because capability marketplace is outside the Phase-4 gate.
- 2026-07-09: Phase-4 AI Employee System MVP is implemented in the Workspace line and pending final acceptance. Workspace now has official Software R&D DepartmentTemplate and six official R&D EmployeeTemplates, tenant-scoped DepartmentInstance and EmployeeInstance metadata, EmployeeCapabilityBinding over official/tenant_private capabilities, task creation `employee_id` selection with Tech Lead default fallback, selected employee capability resolution, employee attribution in usage_event (`employee_id`, `employee_role`, `employee_name`), and a minimal `研发部员工` UI inside the existing operation console. No ROI, non-R&D departments, marketplace, real credential custody, Admin Platform governance change, or `/api/platform/*` Workspace UI call was introduced.
- 2026-07-09: Phase-3.5 Workspace Research -> Decision -> Contract -> Issue convergence is in progress for Phase-4 AI Employee System MVP. The active convergence scope is documentation/contract only: research completeness check, adopted/rejected decision hardening, five contract files, and `issues/phase4_ai_employee_system_mvp.md`. Direct employee system implementation, Task Execution main-flow changes, ROI, marketplace, real credential custody, and Admin Platform governance changes remain blocked.
- 2026-07-08: Model Gateway runtime secret guardrails are implemented, quality-verified, and accepted in `issues/070_model_gateway_runtime_secret_guardrails.md` with evidence in `reviews/067_model_gateway_runtime_secret_guardrails_review.md`. Partial gateway env config fails closed without echoing values; model gateway request/response errors are redacted; UsageEvent payloads stay allowlisted/redacted; gateway/model metadata rejects secret-like values before persistence or API exposure; Workspace model execution remains constrained to `ModelGatewayAdapter`. 质量运行席 verification passed on commit `b01edfd4`: 16 focused guardrail tests and 203 backend regression tests passed; secret/scope/frontend guards passed; no blockers found.
- 2026-07-08: Workspace Tenant Model Preference Foundation gate is opened in `issues/071_workspace_tenant_model_preference_gate.md` and routed to 总控决策席. Proposed scope: tenant-scoped default model preference from approved official model catalog metadata; runtime resolves model preference when available; no secret storage, no provider SDK, no New API source/internal DB dependency, no billing/ROI/tenant package, and model execution remains constrained to `ModelGatewayAdapter`.
- 2026-07-08: 总控决策席 approved Workspace Tenant Model Preference Foundation gate in `issues/071_workspace_tenant_model_preference_gate.md`. Architecture boundary definition may proceed only for metadata-only tenant default model preference over approved active `source=official` model catalog metadata, with runtime model resolution when available and all execution constrained to `ModelGatewayAdapter`.
- 2026-07-08: Workspace Tenant Model Preference Foundation boundaries are quality-verified and accepted in `reviews/068_workspace_tenant_model_preference_boundaries_review.md`; ADR-0030 is the accepted boundary. First implementation slice is opened in `issues/072_workspace_tenant_model_preference_first_slice.md` for backend-only tenant preference persistence/resolution over active `source=official` official model catalog entries. UI, billing, ROI, tenant packages, marketplace, provider SDKs, direct provider calls, credential persistence/exposure, automatic model optimization, per-department/per-employee policy, New API source/internal DB dependency, and execution path drift remain blocked.
- 2026-07-08: Workspace Tenant Model Preference first slice is implemented, quality-verified, and accepted in `issues/072_workspace_tenant_model_preference_first_slice.md` with evidence in `reviews/069_workspace_tenant_model_preference_first_slice_review.md`. Workspace now has backend-only tenant-scoped model preference read/write/delete APIs, metadata-only persistence, active `source=official` catalog validation, and runtime preference resolution through `ModelGatewayAdapter`; invalid/stale preference falls back to existing default adapter metadata. 产品规划席 accepted commit `a0d3a54b` after 质量运行席 verification passed: 4 focused tenant preference tests and 207 backend regression tests passed; secret/scope/frontend guards passed; no blockers found.
- 2026-07-08: Workspace Model Preference UI gate is opened in `issues/073_workspace_model_preference_ui_gate.md` and routed to 总控决策席. Proposed scope is a minimal frontend-only selector inside the existing Workspace operation console to read/save/reset tenant default model preference from approved official catalog metadata. Admin UI, complex dashboard, billing/ROI/packages, secret handling, provider integration, model optimization, backend semantic changes, and execution behavior changes remain blocked.
- 2026-07-08: 总控决策席 approved Workspace Model Preference UI gate in `issues/073_workspace_model_preference_ui_gate.md`. First implementation is frontend-only inside the existing Workspace operation console and may use only existing preference APIs. ADR-0030, ADR-0029, runtime secret guardrails, official model catalog metadata boundary, current Task API payloads, and `ModelGatewayAdapter`-only execution remain binding.
- 2026-07-08: Workspace Model Preference UI first slice is implemented, quality-verified, and accepted with evidence in `reviews/070_workspace_model_preference_ui_review.md`. Workspace now has a frontend-only selector in the existing operation console to view, save, and reset tenant default model preference from active official model options. 产品规划席 accepted commit `5727410f` after 质量运行席 verification passed: 14 frontend view-model tests passed, frontend lint passed, frontend build passed outside the sandbox after sandbox port binding was blocked, backend/Admin/shared/runtime guard passed, existing preference APIs only are used, and Task API payload shape `{ content }` is preserved.
- 2026-07-08: Workspace Model Preference local E2E evidence is verified and accepted in `issues/074_workspace_model_preference_local_e2e_evidence.md` with evidence in `reviews/071_workspace_model_preference_local_e2e_review.md`. Real local backend/frontend runtime passed preference read/save/reset and operation-console task creation; Task API remains content-only. Known local environment note: when frontend uses a non-default port such as `3010`, backend `CURIS_ALLOWED_ORIGINS` must include that origin.
- 2026-07-08: Model Gateway Local Demo Release Candidate gate is opened in `issues/075_model_gateway_local_demo_release_candidate_gate.md` and routed to 总控决策席. Proposed next step is documentation/evidence only: prepare a local/demo release-candidate package for the model-gateway-enabled AI Task Executor MVP after New API, official catalogs, usage events, runtime guardrails, tenant model preference, model preference UI, and local E2E evidence. No new implementation is approved at this gate.
- 2026-07-08: 总控决策席 approved Model Gateway Local Demo Release Candidate gate in `issues/075_model_gateway_local_demo_release_candidate_gate.md`. Next work is documentation/evidence-only release-candidate preparation covering New API model gateway, official model/tool catalogs, UsageEvent model-call fields, runtime secret guardrails, tenant model preference backend/UI, and local E2E evidence. No implementation or behavior change is approved.
- 2026-07-08: Model Gateway Local Demo Release Candidate package is prepared, quality-verified, and accepted in `docs/release/model-gateway-local-demo-rc.md` with evidence in `reviews/072_model_gateway_local_demo_release_candidate_review.md`. Package coverage includes New API local gateway, official model/tool catalogs, UsageEvent model-call fields, ADR-0029 runtime secret guardrails, tenant model preference backend/UI, local E2E evidence, verification checklist, startup/runbook commands, and known-gap classification. 质量运行席 verification passed against commit `9bfc7d8b`: evidence map, runbook/checklist, known-gap classification, source-of-truth status, secret scan, and behavior-file scope guard passed; no backend/frontend behavior files changed for this issue. 产品规划席 accepted the local/demo RC package on 2026-07-08; hosted production remains blocked.
- 2026-07-08: Model Gateway Post-RC Next Phase gate is opened in `issues/076_model_gateway_post_rc_next_phase_gate.md` and routed to 总控决策席. Product recommendation is Option A: documentation/evidence-only local/demo first-version release closeout, with no implementation or behavior change.
- 2026-07-08: 总控决策席 approved Model Gateway Post-RC Next Phase gate in `issues/076_model_gateway_post_rc_next_phase_gate.md` with Option A. Next work is documentation/evidence-only local/demo first-version release closeout; no implementation or behavior change is approved.
- 2026-07-08: Model Gateway Local Demo first-version release closeout package is prepared, quality-verified, and accepted in `docs/release/model-gateway-local-demo-first-version-release-record.md` with evidence in `reviews/073_model_gateway_local_demo_release_closeout_review.md`. The closeout package records release decision evidence, operator handoff summary, final local/demo checklist, known-gap confirmation, source-of-truth status updates, and next backlog boundary. 质量运行席 verification passed against commit `0801231d`: release decision record, operator handoff, checklist, known-gap classification, source-of-truth status, secret scan, and behavior-file scope guard passed; no backend/frontend behavior files changed for this issue. 产品规划席 accepted the local/demo first-version release closeout on 2026-07-08.
- 2026-07-08: Post-first-version Workspace Company Foundation gate is opened in `issues/077_post_first_version_workspace_company_foundation_gate.md` and routed to 总控决策席. Product recommendation is Option A: architecture/product boundary definition only for the first minimal CEO-facing Workspace company foundation. No implementation or behavior change is approved; local/demo, model-gateway security boundary, Admin/Workspace separation, hosted-production lock, billing/ROI/packages/marketplace lock, Employee CRUD/expansion lock, complex organization lock, business-module lock, and execution-loop/runtime behavior lock remain binding.
- 2026-07-08: 总控决策席 approved Post-first-version Workspace Company Foundation gate in `issues/077_post_first_version_workspace_company_foundation_gate.md` with Option A. Next work is architecture/product boundary definition only for the first minimal CEO-facing Workspace company foundation: existing tenant id, company identity, department catalog/instances, model preference, task console, and Project Memory as one bounded Workspace frame. No implementation or behavior change is approved; local/demo, model-gateway security boundary, Admin/Workspace separation, hosted-production lock, billing/ROI/packages/marketplace lock, Employee CRUD/expansion lock, complex organization lock, business-module lock, secret persistence/display lock, and execution-loop/runtime behavior lock remain binding. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Company Foundation architecture/product boundaries are defined and quality-verified in `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md` with evidence in `reviews/074_workspace_company_foundation_boundaries_review.md`. The boundary defines a minimal local/demo CEO-facing company shell over existing tenant/workspace context, company identity concept, department catalog/instances, model preference, task console, Project Memory, and release status. 质量运行席 verification passed against commit `651bdb99`: ADR-0031 boundary-only scope, forbidden-scope locks, first-slice boundary, read-model gap rule, source-of-truth routing, secret scan, and behavior-file guard passed; no backend/frontend behavior files changed for this issue. Handoff sent to 产品规划席 for acceptance.
- 2026-07-08: 产品规划席 accepted Workspace Company Foundation boundaries in `reviews/074_workspace_company_foundation_boundaries_review.md`; ADR-0031 is accepted as the current boundary and implementation remains separately gated.
- 2026-07-08: Workspace Company Foundation first-slice gate is opened in `issues/078_workspace_company_foundation_first_slice_gate.md` and routed to 总控决策席. Product recommendation is Option A: frontend-only local/demo company frame inside the existing operation console using existing non-secret state and existing preference/catalog APIs only. No backend/API/schema/persistence, execution-loop, Task API, runtime, Admin Platform, billing/ROI, Employee CRUD, complex organization, business module, or secret behavior is approved at this gate.
- 2026-07-08: 总控决策席 approved Workspace Company Foundation first-slice gate in `issues/078_workspace_company_foundation_first_slice_gate.md` with Option A. Next work is frontend-only implementation inside the existing operation console using only existing non-secret state and existing preference/catalog APIs. Backend/API/schema/persistence, Task API, execution-loop, tool routing, workflow, model-selection behavior, Project Memory writes, runtime behavior, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, New API source/internal DB dependency, and department CRUD/workflow routing remain blocked. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Company Foundation first slice is implemented and quality-verified with evidence in `reviews/075_workspace_company_foundation_first_slice_review.md`. The slice adds a frontend-only local/demo company frame to the existing operation console using existing task list state and existing model preference state only. 质量运行席 verification passed against commit `dfd60689`: 16 frontend tests passed, lint passed, build passed, API/payload scan passed, forbidden-scope scan passed, secret scan passed, and commit behavior-file guard showed no backend/API/schema/persistence/Admin/shared/deploy/tools/data files changed for this issue. Handoff sent to 产品规划席 for acceptance.
- 2026-07-08: Workspace Company Foundation local/demo evidence gate was approved by 总控决策席 in `issues/079_workspace_company_foundation_local_demo_evidence_gate.md` with Option A. Next work is verification-only local/demo evidence for the accepted company frame: browser-visible/screenshot evidence, visible company-frame content, no secret-like metadata, and Task API payload `{ content }`. No new feature, backend/API/schema/persistence change, runtime behavior change, Admin Platform, hosted production, billing/ROI/packages/marketplace, Employee CRUD, complex organization, business module, secret handling, or department workflow routing is approved. Handoff sent to 质量运行席.
- 2026-07-08: Workspace Company Department Catalog Summary gate was approved by 总控决策席 in `issues/080_workspace_company_department_catalog_summary_gate.md` with Option A. Next work is frontend-only implementation inside the existing company frame using existing `GET /api/catalog/department-types` only. Backend/API/schema/persistence changes, new department APIs, department CRUD/instances/routing, Employee CRUD, Admin Platform implementation, billing/ROI/packages/marketplace, complex organization, business modules, secrets, Task API changes, and runtime behavior changes remain blocked. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Company Department Catalog Summary is implemented, quality-verified, and accepted in `reviews/077_workspace_company_department_catalog_summary_review.md`. The slice adds a frontend-only read-only `部门目录` summary inside the existing company frame using existing `GET /api/catalog/department-types` only. Verification passed with 18 frontend tests, lint, build, API usage scan, Task API payload guard, and forbidden-scope scan. No backend/API/schema/persistence, Admin Platform, department CRUD/instances/routing, Employee CRUD, billing/ROI/packages/marketplace, business-module, secret, Task API, or runtime behavior change was introduced. Handoff: final closeout.
- 2026-07-08: Workspace Department Catalog local/demo evidence gate is opened and approved in `issues/081_workspace_department_catalog_local_demo_evidence_gate.md` with Option A. Next work is verification-only browser-visible evidence for the accepted `部门目录` summary in the existing company frame. No implementation, backend/API/schema/persistence, new department API, department CRUD/instances/routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business-module, secret, Task API, or runtime behavior change is approved.
- 2026-07-08: Workspace Department Catalog local/demo evidence is verified and accepted in `reviews/078_workspace_department_catalog_local_demo_evidence_review.md`. Browser-visible evidence and screenshot artifact `reviews/078_workspace_department_catalog_local_demo_evidence.png` confirm the accepted `部门目录` summary renders in local/demo runtime with active official count, category summary, and non-secret department labels visible. Backend health, frontend runtime smoke, department catalog API read, 18 frontend tests, lint, build, Task API payload boundary, and secret-like metadata scan passed. No implementation or behavior change was made for this evidence issue. Handoff: final closeout.
- 2026-07-08: Workspace Department Activation boundary gate is opened and approved in `issues/082_workspace_department_activation_boundary_gate.md` with Option A. Next work is architecture/product boundary definition only for future tenant-local department activation over existing active official department type metadata. No implementation, backend/API/schema/persistence change, new department API, department instance, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business-module, secret, Task API, or runtime behavior change is approved. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Department Activation boundaries are defined, quality-verified, and accepted in `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md` with evidence in `reviews/079_workspace_department_activation_boundaries_review.md`. The boundary defines future tenant-local department activation as metadata-only selection over active official department type metadata. Official department type supply remains outside Workspace. Implementation, backend/API/schema/persistence, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, and runtime behavior changes remain blocked until a separate implementation issue is approved. Handoff: final closeout.
- 2026-07-08: Workspace Department Activation first-slice gate is opened and approved in `issues/083_workspace_department_activation_first_slice.md`. Next work is backend-only tenant-local department activation metadata over active official department type metadata. Frontend UI selector, Admin Platform implementation, new official department type supply, department instances, workflow routing, Employee CRUD, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, Project Memory runtime writes, and runtime behavior changes remain blocked. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Department Activation first slice is implemented, quality-verified, and accepted in `reviews/080_workspace_department_activation_first_slice_review.md`. Workspace now has backend-only tenant-local department activation metadata with `GET /api/workspace/departments/activation` and `PUT /api/workspace/departments/activation`. Writes validate active official department type metadata, reads/writes are tenant-scoped, persistence is metadata-only, and API responses expose only non-secret department metadata plus enabled state. Focused backend tests passed and full backend regression passed with 255 tests. Frontend selector, Admin Platform implementation, department instances, workflow routing, Employee CRUD, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, Project Memory runtime writes, and runtime behavior changes remain blocked. Handoff: final closeout.
- 2026-07-08: Workspace Department Activation UI gate is opened and approved in `issues/084_workspace_department_activation_ui_gate.md`. Next work is frontend-only display/selector inside the existing company frame using only existing `GET /api/workspace/departments/activation` and `PUT /api/workspace/departments/activation`. Backend/API/schema/persistence changes, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, Project Memory runtime writes, and runtime behavior changes remain blocked. Handoff sent to 系统交付席.
- 2026-07-08: Workspace Department Activation UI is implemented, quality-verified, and accepted in `reviews/081_workspace_department_activation_ui_review.md`. Workspace now shows and saves tenant-local enabled department type selections inside the existing company frame using only existing activation APIs. Frontend verification passed with 21 tests, lint, build, API usage scan, and scope scan. No backend/API/schema/persistence change, new department API, department instance, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business-module, secret, Task API, Project Memory runtime write, or runtime behavior change was introduced for this issue. Handoff: final closeout.
- 2026-07-08: 质量运行席 rechecked issue-080 department catalog summary scope in `reviews/077_workspace_company_department_catalog_summary_review.md` after activation work appeared in the same dirty worktree. 系统交付席 resolved the evidence split by assigning activation behavior to accepted issues 083/084 and keeping issue-080 evidence bounded to read-only `GET /api/catalog/department-types` plus `reviews/078` browser evidence. T-217 is closed.
- 2026-07-08: Workspace Department Activation UI current-state correction is recorded in `reviews/081_workspace_department_activation_ui_review.md`. A current audit found page-level activation selector wiring was missing from `frontend/app/page.js`; the correction added the selector inside the existing `公司工作区` frame using only existing `GET /api/workspace/departments/activation` and `PUT /api/workspace/departments/activation`, added regression coverage, and passed 22 frontend tests, lint, build, and focused backend activation tests. Handoff: final closeout.
- 2026-07-09: Workspace Admin shared-contract integration补齐 is implemented, quality-verified, and accepted in `issues/085_workspace_admin_contract_integration_completion.md` with evidence in `reviews/082_workspace_admin_contract_integration_completion_review.md`. Workspace task execution now writes Admin-compatible `usage.model_call`, `usage.tool_call`, and `usage.task_execution` records with `tenant_id`, `task_id`, `capability_type`, `capability_id`, `capability_source`, `model_gateway_id`, `model_name`, `prompt_tokens`, `completion_tokens`, `total_tokens`, `estimated_cost`, `status`, and `created_at`; Admin usage projection supports tenant query; tenant-private capability metadata is isolated under `/api/workspace/capabilities/private`; official capability reads remain `/api/catalog/*`; Workspace runtime execution files do not call `/api/platform/*`. Verification passed with focused and full backend regression: 279 tests green. Handoff: final closeout.
- 2026-07-09: Workspace Self-Extension MVP is implemented, quality-verified, and accepted in `issues/086_workspace_self_extension_mvp.md` with evidence in `reviews/083_workspace_self_extension_mvp_review.md`. Workspace now supports tenant-private model/tool/connector metadata through typed backend endpoints, a unified official + tenant-private capability selector, and optional task capability selection. Tenant-private execution uses the existing model gateway tool path and records usage events with `capability_source=tenant_private`. Verification passed with TDD red evidence, 10 ADR-0028 focused tests, 42 Phase-3 focused tests, 38 execution-engine tests, 298 full backend tests, whitespace check, runtime `/api/platform/*` scope scan, tenant-private scan, and secret scan. Handoff: final closeout.
- 2026-07-08: New API local deployment is verified in `docs/deployment/new-api-local.md`, `deploy/new-api/docker-compose.yml`, `deploy/new-api/.env.example`, and `tools/smoke_new_api_gateway.py`. Docker CLI, Docker Compose, and Colima are installed; New API container `curis-new-api` is running locally at `http://127.0.0.1:3000`; New API root setup succeeded; a Curis local New API token is stored only in ignored `deploy/new-api/.env`; DeepSeek is configured as the first upstream channel; `/v1/models` includes `deepseek-v4-flash`; `/v1/chat/completions` returns a successful response; Workspace task execution uses `model_gateway_tool` and writes required `usage.model_call` events.
- 2026-07-08: Model Gateway production security boundary is accepted in `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md` with evidence in `reviews/066_model_gateway_production_security_boundary_review.md`. New API remains a gateway only; Curis DB stores no credential values; Workspace model calls stay constrained to `ModelGatewayAdapter`; UsageEvent model-meter fields are constrained to tenant/task/gateway/model/token/cost/status; production external-model operation requires follow-up `issues/070_model_gateway_runtime_secret_guardrails.md`.
- 2026-07-08: Workspace Official Tool Catalog is implemented and verified in `issues/067_workspace_official_tool_catalog.md` with evidence in `reviews/064_workspace_official_tool_catalog_review.md`. Workspace now exposes `GET /api/catalog/tools` for existing official tool metadata with `source=official` and `status=active`; no Admin UI, write API, credential persistence, marketplace, tenant-private tool, billing, ROI, governance, or routing behavior change was added. Backend regression: 163 tests passed.
- 2026-07-08: Workspace Official Model Catalog is implemented and verified in `issues/066_workspace_official_model_catalog.md` with evidence in `reviews/063_workspace_official_model_catalog_review.md`. Workspace now exposes `GET /api/catalog/models` for active `source=official` model metadata with `gateway_ref`, `auth_type`, and `supported_models`; no credential values, Admin UI, billing, ROI, governance, marketplace, or tenant-private model implementation was added. Backend regression: 163 tests passed.
- 2026-07-08: Workspace Model Gateway Adapter is implemented and verified in `issues/065_workspace_model_gateway_adapter.md` with evidence in `reviews/062_workspace_model_gateway_adapter_review.md`. Default AI Task Executor model calls now route through a New API OpenAI-compatible `ModelGatewayAdapter` and the runtime selected tool is `model_gateway_tool`; UsageEvent payloads include tenant/task/gateway/model/token/cost/status metrics. Backend regression: 161 tests passed.
- 2026-07-08: Workspace Capability Integration Phase-1 is implemented and verified in `issues/064_workspace_capability_integration_phase_1.md` with evidence in `reviews/061_workspace_capability_integration_phase_1_review.md`. Workspace now exposes a read-only official department catalog, writes `usage.model_call` events from execution persistence with tenant/CEO attribution, and exposes admin-only usage projection. Backend regression: 159 tests passed.
- Product direction is defined: final product is an AI Company System for solo entrepreneurs.
- Current launch scope is AI Task Executor MVP.
- Global layered architecture is L0 product UI, L1 task execution, L2 execution employee, L3 tools, L4 workflow, L5 company organization, and L6 economy/ROI.
- Sprint 0 scope is defined.
- Root low-token workflow files are initialized.
- Sprint 0 acceptance issue is created.
- Backend tests and frontend lint/build were previously repaired.
- Sprint 0 acceptance verification is complete in `reviews/001_sprint_0_acceptance_review.md`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 总控决策席 approved Sprint 0 closure on 2026-07-06.
- User selected option A: pause Sprint 1 visualization and enter Tool System v1.6 first.
- Tool System v1.6 implementation is complete in `issues/002_tool_system_v1_6_meta_development.md`.
- Quality evidence is recorded in `reviews/002_tool_system_v1_6_meta_development_review.md`.
- User approved Tool System v1.8: Controlled Self-Evolving AI Operating System Kernel.
- 产品规划席 must not implement v1.8 code directly; implementation belongs to 系统交付席.
- Tool System v1.8 implementation is complete in `issues/003_tool_system_v1_8_controlled_self_evolution.md`.
- System delivery evidence is recorded in `reviews/003_tool_system_v1_8_controlled_self_evolution_review.md`.
- 质量运行席 independently verified Tool System v1.8 backend regression, API evidence, scope drift, and acceptance evidence.
- Quality status: PASS; no blockers were found by 质量运行席.
- 产品规划席 accepted Tool System v1.8 on 2026-07-06.
- AI Employee runtime workflow must also use compact step packages, minimal context, event-style next-step routing, and Orchestrator final closeout.
- Sprint 1 company visualization PRD slice is drafted in `docs/sprints/sprint-1-company-visualization.md`.
- Sprint 1 gate decision issue is `issues/004_sprint_1_company_visualization_gate.md`.
- 总控决策席 approved the Sprint 1 company visualization gate on 2026-07-06.
- Sprint 1 architecture-boundary handoff was sent to 系统交付席 on 2026-07-06.
- 系统交付席 completed T-006 and reported `HANDOFF_REQUIRED`; main thread routed the handoff to 质量运行席 on 2026-07-06.
- Sprint 1 architecture boundaries are defined in `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`.
- Boundary evidence is recorded in `reviews/004_sprint_1_architecture_boundaries_review.md`.
- 质量运行席 prepared Sprint 1 boundary verification planning in `reviews/004_sprint_1_architecture_boundaries_review.md`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-015 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the Sprint 1 architecture-boundary verification plan on 2026-07-06.
- First implementation slice: compact task list plus selected task detail.
- Implementation issue: `issues/006_sprint_1_visualization_first_slice.md`.
- Sprint 1 visualization first slice is implemented by 系统交付席.
- Delivery evidence is recorded in `reviews/005_sprint_1_visualization_first_slice_review.md`.
- 质量运行席 verified Sprint 1 visualization first slice against commit `c0dd48a`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-018 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Sprint 1 visualization first slice on 2026-07-06.
- Current main contains implementation commit `8ab1cb4`; quality review references equivalent implementation commit `c0dd48a`.
- User chose to continue Sprint 1 visualization polish before Sprint 2.
- Polish issue: `issues/007_sprint_1_ceo_readable_visualization_polish.md`.
- Sprint 1 CEO-readable visualization polish is implemented by 系统交付席.
- Delivery evidence is recorded in `reviews/006_sprint_1_ceo_readable_visualization_polish_review.md`.
- Implementation preserved the accepted first-slice boundary: compact task list plus selected task detail.
- Backend files were not changed.
- 质量运行席 verified Sprint 1 CEO-readable visualization polish.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-023 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Sprint 1 CEO-readable visualization polish on 2026-07-06.
- User chose to enter Sprint 2 on 2026-07-06.
- Sprint 2 unified task console PRD slice is drafted in `docs/sprints/sprint-2-unified-task-console.md`.
- Sprint 2 gate decision issue is `issues/008_sprint_2_unified_task_console_gate.md`.
- 总控决策席 approved the Sprint 2 unified task console gate on 2026-07-06.
- Sprint 2 architecture boundaries are defined in `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`.
- Boundary evidence is recorded in `reviews/007_sprint_2_architecture_boundaries_review.md`.
- First Sprint 2 implementation slice is bounded to existing task composer, compact task history, existing run action, accepted Sprint 1 selected detail, and minimal review signals derived from existing state.
- Backend changes are blocked unless an approved read-model gap is documented first.
- 质量运行席 verified Sprint 2 architecture boundaries against amended commit `e801da4`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-029 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the Sprint 2 architecture-boundary verification plan on 2026-07-06.
- Sprint 2 first implementation issue is `issues/009_sprint_2_unified_task_console_first_slice.md`.
- Sprint 2 unified task console first slice is implemented by 系统交付席.
- Delivery evidence is recorded in `reviews/008_sprint_2_unified_task_console_first_slice_review.md`.
- Implementation remains frontend-only and preserves the accepted Sprint 1 selected-task detail boundary.
- Backend files were not changed.
- 质量运行席 verified Sprint 2 unified task console first slice against commit `b799041`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-032 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Sprint 2 unified task console first slice on 2026-07-06.
- 产品规划席 selected Sprint 2 Project Memory Foundation as the next follow-up before Sprint 3.
- Sprint 2 Project Memory Foundation PRD slice is drafted in `docs/sprints/sprint-2-project-memory-foundation.md`.
- Sprint 2 Project Memory Foundation gate issue is `issues/010_sprint_2_project_memory_foundation_gate.md`.
- 总控决策席 approved the Sprint 2 Project Memory Foundation gate on 2026-07-06.
- Project Memory Foundation architecture boundaries are defined in `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`.
- Boundary evidence is recorded in `reviews/009_project_memory_foundation_architecture_boundaries_review.md`.
- Project Memory is bounded as a deterministic project-fact read model over existing source-of-truth files and execution summary memory.
- Backend persistence, embeddings, external memory service, agent memory, Employee memory, multi-agent coordination, L5 company organization, and L6 ROI/economy remain blocked unless separately approved.
- 质量运行席 verified Project Memory Foundation architecture boundaries against amended commit `c8e047b`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-037 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the Project Memory Foundation architecture-boundary verification plan on 2026-07-06.
- First Project Memory implementation issue is `issues/011_sprint_2_project_memory_first_slice.md`.
- First Project Memory implementation slice is bounded to a deterministic project-fact read model over approved source files and existing execution summary memory only.
- Project Memory first slice is implemented by 系统交付席 in `knowledge/PROJECT_MEMORY.md`.
- Delivery evidence is recorded in `reviews/010_project_memory_first_slice_review.md`.
- Implementation is documentation-only; backend and frontend implementation files were not changed.
- 质量运行席 verified Project Memory first slice against amended commit `3e44d9c`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-040 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Project Memory first slice on 2026-07-06.
- `knowledge/PROJECT_MEMORY.md` is now the first Project Memory artifact and should be refreshed after completed issues or sprint closeout when project facts change.
- 产品规划席 selected Sprint 3 lightweight role and responsibility system as the next step on 2026-07-06.
- Sprint 3 PRD slice is drafted in `docs/sprints/sprint-3-lightweight-role-responsibility.md`.
- Sprint 3 gate issue is `issues/012_sprint_3_lightweight_role_responsibility_gate.md`.
- Sprint 3 is bounded to deterministic role profiles, responsibility boundaries, and escalation triggers inside the AI Task Executor MVP.
- Sprint 3 must not add Employee CRUD, employee expansion, company organization, multi-agent routing, agent abstraction, complex UI, ROI, business modules, new execution behavior, automatic evolution behavior, or unapproved persistence.
- 总控决策席 approved the Sprint 3 lightweight role and responsibility gate on 2026-07-06.
- Sprint 3 lightweight role architecture boundaries are defined in `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`.
- Boundary evidence is recorded in `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`.
- First implementation is bounded to deterministic source-controlled role profiles only.
- Runtime prompt integration, task evidence attachment, UI, backend metadata, and persistence are deferred unless separately approved.
- 质量运行席 verified Sprint 3 lightweight role architecture boundaries against commit `cef5265`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-045 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the Sprint 3 lightweight role architecture-boundary verification plan on 2026-07-06.
- First Sprint 3 implementation issue is `issues/013_sprint_3_role_profiles_first_slice.md`.
- First Sprint 3 implementation is bounded to deterministic source-controlled role profiles in `knowledge/ROLE_PROFILES.md`.
- Sprint 3 role profiles first slice is implemented in `knowledge/ROLE_PROFILES.md`.
- Delivery evidence is recorded in `reviews/012_sprint_3_role_profiles_first_slice_review.md`.
- Implementation is documentation-only; backend and frontend implementation files were not changed.
- 质量运行席 verified Sprint 3 role profiles first slice against commit `53d8a30`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-048 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Sprint 3 role profiles first slice on 2026-07-06.
- 产品规划席 closed out Sprint 3 role profiles first slice to user on 2026-07-06.
- 产品规划席 opened Sprint 3 role-context runtime reference gate in `issues/014_sprint_3_role_context_runtime_reference_gate.md`.
- Runtime implementation remains blocked; the gate only asks whether 系统交付席 may define architecture boundaries.
- 总控决策席 approved the Sprint 3 role-context runtime reference gate on 2026-07-06.
- Role-context runtime reference architecture boundaries are defined in `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`.
- Boundary evidence is recorded in `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`.
- Runtime implementation, task evidence attachment, UI selector, backend metadata, persistence, and task-role association remain blocked.
- Future runtime reference is limited to read-only prompt/context guidance from an explicit issue-declared profile id unless separately approved.
- 质量运行席 verified role-context runtime reference architecture boundaries against commit `c72e86dd`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-053 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the role-context runtime reference architecture-boundary verification plan on 2026-07-06.
- First implementation issue is `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`.
- First slice is limited to minimal read-only role-context reference from an explicit issue-declared profile id; no implicit default role is approved.
- Role-context runtime reference first slice is implemented in `backend/app/role_context.py`.
- Delivery evidence is recorded in `reviews/014_role_context_runtime_reference_first_slice_review.md`.
- The first slice is read-only and uses explicit profile id `curis.role.system-delivery.v1`; missing or invalid profile ids omit role context.
- No API routes, UI, persistence, task evidence attachment, tool routing, workflow mutation, task-state mutation, or execution-loop behavior were changed.
- 质量运行席 verified role-context runtime reference first slice against commit `71e9577b`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-056 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted role-context runtime reference first slice on 2026-07-06.
- Future runtime callers must be constrained by a separately approved issue-declared profile id; no implicit default role is approved.
- Sprint 4 product PRD slice is drafted in `docs/sprints/sprint-4-multi-entry-advanced-ui.md`.
- Sprint 3 closeout and Sprint 4 entry gate issue is `issues/016_sprint_3_closeout_sprint_4_entry_gate.md`.
- 总控决策席 approved Sprint 3 closeout and Sprint 4 architecture-boundary entry on 2026-07-06.
- Sprint 4 multi-entry and advanced UI architecture boundaries are defined in `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`.
- Boundary evidence is recorded in `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`.
- First implementation should stay bounded to operational UI inside the existing AI Task Executor product shell.
- Backend/API changes, persistence, external entry channels, complex UI, new execution behavior, and future-layer scope remain blocked unless separately approved.
- 质量运行席 verified Sprint 4 multi-entry and advanced UI architecture boundaries against commit `cf96d58b`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-061 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the Sprint 4 multi-entry UI architecture-boundary verification plan on 2026-07-06.
- First Sprint 4 implementation issue is `issues/017_sprint_4_multi_entry_ui_first_slice.md`.
- First slice is frontend-only task-entry affordances inside the existing AI Task Executor shell.
- Sprint 4 multi-entry UI first slice is implemented by 系统交付席.
- Delivery evidence is recorded in `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.
- Implementation added bounded local task-entry starters that only prefill ordinary composer content.
- Existing task composer, Task API payload `{ content }`, run action, task history, selected detail, and review signals remain preserved.
- Backend files, API semantics, persistence, task type, role selector, dashboard, external channel, and execution-loop behavior were not changed.
- 质量运行席 verified Sprint 4 multi-entry UI first slice against commit `c528ed72`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-064 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted Sprint 4 multi-entry UI first slice on 2026-07-06.
- 产品规划席 drafted AI Task Executor MVP readiness gate in `docs/sprints/ai-task-executor-mvp-readiness.md`.
- Sprint 4 closeout and MVP readiness gate issue is `issues/018_sprint_4_closeout_mvp_readiness_gate.md`.
- 总控决策席 approved Sprint 4 first-slice closeout and opened AI Task Executor MVP readiness review as gate-only planning on 2026-07-06.
- MVP readiness review may classify readiness gaps, stabilization needs, verification gaps, documentation gaps, and future product scope only.
- No implementation is approved by the MVP readiness gate.
- AI Task Executor MVP readiness review boundaries are defined in `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md`.
- Boundary evidence and verification plan are recorded in `reviews/017_ai_task_executor_mvp_readiness_boundaries_review.md`.
- Gap classification is limited to blocker, stabilization, verification, documentation, and future product scope.
- Any follow-up implementation remains blocked until a separate approved issue defines exact scope and verification.
- 质量运行席 verified the MVP readiness boundary, verification plan, and gap-classification plan against commit `031321bf`.
- Quality status: PASS; no scope blockers were found by 质量运行席.
- Verification note: backend regression passes with `backend/.venv/bin/python -m unittest discover tests`; the system `python3` command does not have the required FastAPI dependency.
- 质量运行席 sent the T-068 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the AI Task Executor MVP readiness boundary verification plan on 2026-07-06.
- 产品规划席 opened the AI Task Executor MVP readiness review issue in `issues/019_ai_task_executor_mvp_readiness_review.md`.
- AI Task Executor MVP readiness review was conducted by 系统交付席 on 2026-07-06.
- Evidence is recorded in `reviews/018_ai_task_executor_mvp_readiness_review.md`.
- Existing accepted MVP surfaces were mapped to source evidence.
- Current backend/frontend verification commands passed.
- No blocker readiness gaps were found; gaps were classified as stabilization, verification, or future product scope.
- No implementation follow-up is approved by `issues/019_ai_task_executor_mvp_readiness_review.md`.
- 质量运行席 verified the AI Task Executor MVP readiness evidence map and gap classification against commit `e657b884`.
- Quality status: PASS; no readiness blockers or scope blockers were found by 质量运行席.
- 质量运行席 sent the T-071 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the AI Task Executor MVP readiness review on 2026-07-06.
- Current AI Task Executor MVP readiness state: no blocker gaps; follow-up work must be routed as separate stabilization, verification, or future product scope issues.
- User requested operation-console Chinese localization.
- Operation-console Chinese localization was completed by 系统交付席 on 2026-07-06.
- Localization evidence is recorded in `reviews/019_chinese_operation_console_localization_review.md`.
- The localization is frontend-only and preserves Task API payload `{ content }`, backend behavior, persistence, and execution-loop behavior.
- 产品规划席 opened AI Task Executor MVP release-candidate gate on 2026-07-06.
- Release-candidate PRD slice is `docs/sprints/ai-task-executor-mvp-release-candidate.md`.
- Release-candidate gate issue is `issues/021_ai_task_executor_mvp_release_candidate_gate.md`.
- The gate may approve stabilization, verification, startup/deployment documentation, release checklist, rollback notes, and local/demo deployment instructions only.
- 总控决策席 approved AI Task Executor MVP release-candidate entry on 2026-07-06 for boundary definition and stabilization/documentation planning only.
- No release-candidate implementation is approved by the gate decision.
- AI Task Executor MVP release-candidate boundaries are defined in `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`.
- Boundary and exact stabilization/documentation planning evidence is recorded in `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`.
- Planned release-candidate items are limited to verification command standardization, startup docs, local/demo deployment docs, release checklist, rollback notes, and stabilization triage.
- Release-candidate implementation remains blocked until a separate approved issue defines exact scope and verification.
- 质量运行席 verified the AI Task Executor MVP release-candidate boundaries and exact stabilization/documentation plan against commit `d94fc084`.
- Quality status: PASS; no scope blockers were found by 质量运行席.
- 质量运行席 sent the T-077 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the AI Task Executor MVP release-candidate boundaries and exact stabilization/documentation plan on 2026-07-06.
- Accepted RC items are RC-PLAN-001 through RC-PLAN-006 only; implementation still requires a separate scoped issue.
- 产品规划席 opened `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md` on 2026-07-06.
- The implementation issue is documentation-only except `.env.example` or equivalent local configuration guidance if needed.
- FastAPI Python 3.14 deprecation warning may be triaged only; fixing it requires a separate approved stabilization issue.
- Release-candidate stabilization/documentation package is implemented in `docs/release/ai-task-executor-mvp-v0.1.md`.
- Delivery evidence is recorded in `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`.
- RC-PLAN-001 through RC-PLAN-006 are covered.
- FastAPI Python 3.14 warning triage decision is `defer-known-gap`; no code fix was made.
- Backend/frontend implementation files were not changed.
- 质量运行席 verified the release-candidate stabilization/documentation package against commit `33d89da7`.
- Quality status: PASS; no blockers were found by 质量运行席.
- 质量运行席 sent the T-081 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the release-candidate stabilization/documentation package on 2026-07-06.
- `docs/release/ai-task-executor-mvp-v0.1.md` is now the accepted local/demo release-candidate runbook.
- 产品规划席 opened `issues/023_ai_task_executor_mvp_local_demo_release_verification.md` on 2026-07-06.
- This issue is verification-only; it does not approve implementation changes, mock/simulation substitution, external services, FastAPI warning fix, or future-layer scope.
- 质量运行席 verified the first-version local/demo release candidate at restore point `c5011acd`.
- Release verification evidence is recorded in `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`.
- Quality status: PASS; no blockers were found by 质量运行席.
- API smoke passed for health, task creation, and task history using the real local FastAPI server with SQLite storage at `/private/tmp/curis_release_smoke.sqlite`.
- FastAPI Python 3.14 warning remains `defer-known-gap`.
- 质量运行席 sent the T-084 handoff to 产品规划席 thread `019f33b8-bc87-71e0-a03b-e937a1b35c48`.
- 产品规划席 accepted the first-version local/demo release candidate verification on 2026-07-06.
- The acceptance approves verification evidence only; it does not approve implementation changes, mock/simulation substitution, new features, API semantic changes, persistence/schema changes, execution behavior changes, external services, complex UI/dashboard, FastAPI warning fix, or future-layer scope.
- 产品规划席 closed AI Task Executor MVP v0.1 as the first local/demo version on 2026-07-06.
- Release record is `docs/release/ai-task-executor-mvp-v0.1-release-record.md`.
- Release closeout evidence is `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`.
- Local tag decision: create `v0.1` after the closeout commit; verified code restore point remains `c5011acd`.
- 总控决策席 approved the post-v0.1 Execution Reliability gate on 2026-07-06.
- Gate issue is `issues/025_post_v0_1_execution_reliability_gate.md`.
- Gate brief is `docs/sprints/post-v0.1-execution-reliability.md`.
- This gate approves architecture boundary definition only; no implementation, new feature, UI/dashboard, future-layer scope, API semantic change, persistence/schema change, external service, or automatic evolution behavior change is approved.
- 系统交付席 defined post-v0.1 Execution Reliability architecture boundaries on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`.
- Boundary issue is `issues/026_post_v0_1_execution_reliability_boundaries.md`.
- Delivery evidence is `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`.
- Recommended first implementation slice is `Run Evidence Reliability`; implementation remains blocked until quality planning and product acceptance.
- 质量运行席 verified the post-v0.1 Execution Reliability architecture boundaries on 2026-07-06.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the post-v0.1 Execution Reliability architecture boundaries on 2026-07-06.
- First implementation slice is `Run Evidence Reliability`.
- Implementation issue is `issues/027_run_evidence_reliability_first_slice.md`.
- Implementation is limited to backend tests and evidence quality around existing run behavior; API semantics, persistence schema, UI, external services, new features, new execution behavior, and future-layer scope remain blocked.
- 系统交付席 implemented the Run Evidence Reliability first slice on 2026-07-06.
- Delivery evidence is `reviews/025_run_evidence_reliability_first_slice_review.md`.
- Backend reliability coverage now verifies successful run evidence chain and failed run evidence chain.
- Duplicate failed-run tool trace persistence was fixed without changing API semantics or persistence schema.
- Backend regression passed with 36 tests.
- 质量运行席 verified the Run Evidence Reliability first slice on 2026-07-06.
- Quality evidence is recorded in `reviews/025_run_evidence_reliability_first_slice_review.md`.
- Focused reliability tests passed with 2 tests.
- Backend regression passed with 36 tests.
- Frontend diff guard passed; no frontend files changed.
- Scope scan found no forbidden implementation drift.
- 产品规划席 accepted the Run Evidence Reliability first slice on 2026-07-06.
- Next proposed post-v0.1 reliability slice is Workflow Error/Fallback Observability.
- Gate issue is `issues/028_workflow_error_fallback_observability_gate.md`.
- 总控决策席 approved the Workflow Error/Fallback Observability gate on 2026-07-06.
- This gate approves architecture boundary definition only and does not approve implementation.
- 系统交付席 defined Workflow Error/Fallback Observability architecture boundaries on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`.
- Boundary issue is `issues/029_workflow_error_fallback_observability_boundaries.md`.
- Delivery evidence is `reviews/026_workflow_error_fallback_observability_boundaries_review.md`.
- Recommended first implementation slice is `Workflow Error/Fallback Evidence Map`; limited implementation is unblocked only through `issues/030_workflow_error_fallback_evidence_map.md`.
- 质量运行席 verified the Workflow Error/Fallback Observability architecture boundaries on 2026-07-06.
- Quality status: PASS; no backend/frontend implementation diff or scope blockers were found.
- 产品规划席 accepted the Workflow Error/Fallback Observability architecture boundaries on 2026-07-06.
- First implementation issue is `issues/030_workflow_error_fallback_evidence_map.md`.
- First implementation is limited to backend tests and evidence documentation for existing workflow error/fallback behavior.
- 系统交付席 implemented Workflow Error/Fallback Evidence Map on 2026-07-06.
- Delivery evidence is `reviews/027_workflow_error_fallback_evidence_map_review.md`.
- Backend tests now cover successful fallback evidence map and full fallback-chain failure evidence map.
- No backend production files or frontend files were changed.
- Backend regression passed with 38 tests.
- 质量运行席 verified Workflow Error/Fallback Evidence Map on 2026-07-06.
- Quality status: PASS; focused tests passed with 2 tests and backend regression passed with 38 tests.
- No frontend diff, backend production diff, or scope blockers were found.
- 产品规划席 accepted Workflow Error/Fallback Evidence Map on 2026-07-06.
- Next proposed post-v0.1 reliability slice is Evolution Decision Evidence Reliability.
- Gate issue is `issues/031_evolution_decision_evidence_reliability_gate.md`.
- 总控决策席 approved the Evolution Decision Evidence Reliability gate on 2026-07-06.
- This gate approves architecture boundary definition only and does not approve implementation.
- 系统交付席 defined Evolution Decision Evidence Reliability architecture boundaries on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`.
- Boundary issue is `issues/032_evolution_decision_evidence_reliability_boundaries.md`.
- Delivery evidence is `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`.
- Recommended first implementation slice is `Evolution Decision Evidence Map`; limited implementation is unblocked only through `issues/033_evolution_decision_evidence_map.md`.
- 质量运行席 verified the Evolution Decision Evidence Reliability architecture boundaries on 2026-07-06.
- Quality status: PASS; no backend/frontend implementation diff or scope blockers were found.
- 产品规划席 accepted the Evolution Decision Evidence Reliability architecture boundaries on 2026-07-06.
- First implementation issue is `issues/033_evolution_decision_evidence_map.md`.
- First implementation is limited to backend tests and evidence documentation for existing Evolution Governor decision behavior.
- 系统交付席 implemented Evolution Decision Evidence Map on 2026-07-06.
- Delivery evidence is `reviews/029_evolution_decision_evidence_map_review.md`.
- Backend tests now cover stable do-not-evolve, threshold-triggered controlled proposal/simulation/rollback, locked-module postpone risk, and evolution-decision API evidence.
- No backend production files or frontend files were changed.
- Backend regression passed with 41 tests.
- 质量运行席 verified Evolution Decision Evidence Map on 2026-07-06.
- Quality status: PASS; focused tests passed with 4 tests and backend regression passed with 41 tests.
- No frontend diff, backend production diff, or scope blockers were found.
- 产品规划席 accepted Evolution Decision Evidence Map on 2026-07-06.
- Post-v0.1 Execution Reliability closeout gate issue is `issues/034_post_v0_1_execution_reliability_closeout_gate.md`.
- 总控决策席 approved the post-v0.1 Execution Reliability closeout gate on 2026-07-06.
- This gate approves closeout review planning only and does not approve implementation.
- 系统交付席 completed the post-v0.1 Execution Reliability closeout review on 2026-07-06.
- Closeout evidence is `reviews/030_post_v0_1_execution_reliability_closeout_review.md`.
- No blocker gaps were identified for the post-v0.1 reliability phase.
- Recommended next move after quality verification and product acceptance is next-phase selection by 产品规划席.
- 质量运行席 verified the post-v0.1 Execution Reliability closeout review on 2026-07-06.
- Backend regression passed with 41 tests.
- No backend/frontend implementation diff or scope blockers were found.
- 产品规划席 accepted the post-v0.1 Execution Reliability closeout review on 2026-07-06.
- Product selected Local/Demo Operator Polish and Release Notes as the next bounded phase.
- Local/demo operator polish gate issue is `issues/035_local_demo_operator_polish_gate.md`.
- 总控决策席 approved the local/demo operator polish gate on 2026-07-06.
- This gate approves architecture boundary definition only; implementation remains blocked.
- 系统交付席 defined local/demo operator polish architecture boundaries on 2026-07-06.
- Boundary ADR is `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`.
- Boundary issue is `issues/036_local_demo_operator_polish_boundaries.md`.
- Delivery evidence is `reviews/031_local_demo_operator_polish_boundaries_review.md`.
- Recommended first slice is `Local/Demo Operator Release Notes Package`.
- 质量运行席 verified the local/demo operator polish architecture boundaries on 2026-07-06.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the local/demo operator polish architecture boundaries on 2026-07-06.
- First implementation issue is `issues/037_local_demo_operator_release_notes_package.md`.
- The accepted implementation is documentation-only operator release notes.
- 系统交付席 implemented the Local/Demo Operator Release Notes Package on 2026-07-06.
- Release notes artifact is `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`.
- Delivery evidence is `reviews/032_local_demo_operator_release_notes_package_review.md`.
- 质量运行席 verified the Local/Demo Operator Release Notes Package on 2026-07-06.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the Local/Demo Operator Release Notes Package on 2026-07-06.
- Local/demo operator polish first slice is complete.
- Main thread closeout prepared on 2026-07-06.
- 产品规划席 selected Local/Demo Verification Automation as the next bounded phase on 2026-07-07.
- Local/demo verification automation gate issue is `issues/038_local_demo_verification_automation_gate.md`.
- 总控决策席 approved the local/demo verification automation gate on 2026-07-07.
- This gate approves architecture boundary definition only; implementation remains blocked.
- 系统交付席 defined local/demo verification automation architecture boundaries on 2026-07-07.
- Boundary ADR is `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`.
- Boundary issue is `issues/039_local_demo_verification_automation_boundaries.md`.
- Delivery evidence is `reviews/033_local_demo_verification_automation_boundaries_review.md`.
- Recommended first slice is `Local/Demo API Smoke Helper`.
- 质量运行席 verified the local/demo verification automation architecture boundaries on 2026-07-07.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the local/demo verification automation architecture boundaries on 2026-07-07.
- First implementation issue is `issues/040_local_demo_api_smoke_helper.md`.
- 系统交付席 implemented the Local/Demo API Smoke Helper on 2026-07-07.
- Helper artifact is `tools/local_demo_api_smoke.py`.
- Operator notes reference is in `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`.
- Delivery evidence is `reviews/034_local_demo_api_smoke_helper_review.md`.
- 质量运行席 verified the Local/Demo API Smoke Helper on 2026-07-07.
- Real local FastAPI smoke passed for health, task creation, and task history.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the Local/Demo API Smoke Helper on 2026-07-07.
- Local/demo verification automation first slice is complete.
- Main thread closeout prepared on 2026-07-07.
- 产品规划席 selected Project Memory Execution Summary as the next bounded phase on 2026-07-07.
- Project Memory execution summary gate issue is `issues/041_project_memory_execution_summary_gate.md`.
- 总控决策席 approved the Project Memory execution summary gate on 2026-07-07.
- This gate approves architecture boundary definition only; implementation remains blocked.
- 系统交付席 defined Project Memory execution summary architecture boundaries on 2026-07-07.
- Boundary ADR is `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md`.
- Boundary issue is `issues/042_project_memory_execution_summary_boundaries.md`.
- Delivery evidence is `reviews/035_project_memory_execution_summary_boundaries_review.md`.
- Recommended first slice is documentation-only `knowledge/EXECUTION_SUMMARY_MEMORY.md`.
- 质量运行席 verified the Project Memory execution summary architecture boundaries on 2026-07-07.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the Project Memory execution summary architecture boundaries on 2026-07-07.
- First implementation issue is `issues/043_project_memory_execution_summary.md`.
- 系统交付席 implemented the Project Memory Execution Summary on 2026-07-07.
- Summary artifact is `knowledge/EXECUTION_SUMMARY_MEMORY.md`.
- Delivery evidence is `reviews/036_project_memory_execution_summary_review.md`.
- 质量运行席 verified the Project Memory Execution Summary on 2026-07-07.
- Quality status: PASS; no implementation drift or scope blockers were found.
- 产品规划席 accepted the Project Memory Execution Summary on 2026-07-07.
- Project Memory execution summary first slice is complete.
- Main thread closeout prepared on 2026-07-07.
- 2026-07-07: ADR-0016 gate approved (issues/048 option a). D1 Runtime Role Wiring boundary (ADR-0019) verified PASS-WITH-NOTES by 质量运行席 and accepted by 产品规划席; ready for 系统交付席 implementation per issues/045. Slice order D1→D3→D2.
- 2026-07-07: D1 Runtime Role Wiring implemented (prompt_builder.py + employee.py wired to role_context, additive guidance only), verified PASS by 质量运行席 (48 tests), accepted by 产品规划席. D1 slice closed. Next: D3 Append-Only Event Log (separate gate/boundary, order D1→D3→D2).
- 2026-07-07: D3 Append-Only Evolution Event Log boundary (ADR-0020) verified PASS-WITH-NOTES by 质量运行席 and accepted by 产品规划席; ready for 系统交付席 implementation per ADR-0020. Slice order D1→D3→D2.
- 2026-07-07: D3 Append-Only Evolution Event Log implemented (new evolution_events table + EvolutionEventLog append-only module + correlated event emission from ResultStore/EvolutionGovernor + additive /api/evolution-events endpoint), verified PASS by 质量运行席 (57 tests), accepted by 产品规划席. D3 slice closed. Next: D2 Evolution Governor Sandbox (issues/046, Sub-decision B).
- 2026-07-07: D2 Evolution Governor Sandbox boundary (ADR-0021) verified PASS-WITH-NOTES by 质量运行席 and accepted by 产品规划席; ready for 系统交付席 implementation per ADR-0021. Last slice of ADR-0016 (order D1→D3→D2).

## Next Curis Role

系统交付席.

## 2026-07-10 Phase 1 AI Company Runtime Foundation

- In-progress foundation issue: `issues/phase1a_ai_company_runtime_foundation.md`.
- Company, Department, Project, Employee, Skill, Tool, Task, and Workflow runtime associations are implemented as additive Workspace backend state.
- Product hierarchy is now explicit: Company -> Department / Project -> Employee -> Skill / Tool -> Workflow / Task substrate.
- Task and Workflow execution behavior, Credential Vault resolver boundary, usage_event, audit_event, and Model Gateway path remain preserved.
- Skill prompt guidance is bounded and non-authoritative; EmployeeToolBinding is a projection of canonical EmployeeCapabilityBinding records.
- Verification complete: focused Phase 1A / Phase 4 / Phase 5 / Phase 6 regression passes 23 tests; full backend regression passes 452 tests; `git diff --check`, scoped secret scan, and no-new-Workspace-runtime-`/api/platform/*` scan pass.
- Independent review found and this slice fixed company-scoped default employee selection, cross-company Task/Workflow association rejection, and Skill credential-URI rejection.
- Pending: isolated implementation commit and product closeout.

## 2026-07-10 UI Product Decision Rule

- UI is a core product experience. 产品规划席 owns UI direction, information architecture, user flows, interaction principles, and acceptance criteria.
- 系统交付席 and 质量运行席 may only implement and verify an approved UI specification. They must route UI ambiguity to 产品规划席 and escalate material UI decisions for user confirmation.

## 2026-07-10 Phase-1A.5 AI Company Runtime Design Freeze

- Product chain is frozen as CEO -> Company -> Project -> Department -> Employee -> Skill / Tool -> Workflow -> Task execution substrate.
- Project is the CEO work entry; Workflow is Project-driven; Task remains internal execution substrate.
- Employee lifecycle product states: 创建 -> 启用 -> 工作 -> 等待 -> 停用. Existing runtime enums remain compatible until a separately approved migration.
- Project lifecycle product states: 创建 -> 规划 -> 执行 -> 完成 -> 归档, with 阻塞 as an exception state. Existing runtime enums remain compatible until a separately approved migration.
- Phase-1B UI must use Company / Project as product entry points. UI decisions remain Product-owned under AGENTS.md.

## 2026-07-10 Phase-1B Template Runtime Integration Gate

- Template -> Instance contracts are frozen for Company, Department, Employee, Workflow, Skill binding, and Tool binding.
- Template-created instances must retain immutable `created_from_template_id` and future `created_from_template_version`; source tracking is not dynamic inheritance.
- CEO customization is limited to tenant-private instance fields and bindings. Official templates, origin metadata, credentials, routing, commercial settings, and Admin governance remain immutable from Workspace.
- Company bootstrap product design supports blank company or future CompanyPackage; CompanyPackage auto-instantiation and official template version APIs remain separate gated implementation work.
- Phase-1B may begin UI product design only after 产品规划席 approves Company / Project-first information architecture. No UI may assume unresolved shared template APIs exist.

## 2026-07-10 Phase-1B.5 CEO Dashboard Design Gate

- CEO Dashboard is frozen as an AI company operating cockpit, not a task list or Admin backend.
- Default domains: Company, Department, Project/Workflow, Employee/Capability, Usage/estimated cost, Value Event, and Knowledge.
- Dashboard customisation is constrained to Catalog Widgets, layout, display and non-sensitive scope. It cannot introduce arbitrary queries, external data, commercial rules, credentials, or official-template edits.
- Data readiness: Company/Department/Project/Employee/Workflow/Usage/Tool facts are aggregatable; Value Event persistence, Employee Growth metrics, Skill usage attribution and Knowledge Growth aggregation remain partially ready or reserved.
- Phase-1B UI requires a separate product-approved information architecture and must present `estimated_cost` as non-billing estimated consumption and Value Event as non-ROI value records.

## 2026-07-10 Phase-1C CEO Office UI Product + Figma Design System

- Historical design gate, superseded for implementation by the V3.1 product decision below.
- Product design is frozen in `docs/design/phase1c-ceo-office-ui-design.md`; CEO Office is an AI company headquarters, not a task list or Admin console.
- Figma file: `https://www.figma.com/design/aE7KcRhwGVXYUbwdpyLfzO`.
- Completed Figma artifacts: Design Tokens, typography/elevation styles, Status Chip variants, Employee/Project/Department Card components, and CEO Office homepage high-fidelity frame.
- Figma Starter MCP call limit blocked remaining screen frames and final screenshot QA. Company, Department, Project, Employee, onboarding, Widget details, and interaction specifications are documented but still need Figma rendering when the limit resets or plan is upgraded.
- No implementation was approved by this historical Figma gate.

## 2026-07-10 Phase-1C CEO Office UI Redesign

- Historical redesign stage, superseded for implementation by `docs/design/phase1c-ceo-office-ui-v3.md`.
- Redesign source of truth: `docs/design/phase1c-ceo-office-ui-redesign.md`.
- Adopted direction: future enterprise headquarters space with selected control-center signals; rejected BI dashboard and game-like virtual office directions.
- First-screen hierarchy is frozen as Company identity / strategic goal -> Department operations overview -> Project War Room -> CEO decisions -> executive signals.
- Headquarters does not render the full employee tree. It shows at most four core/exception departments, a five-to-seven-person active project team, and exception signals; all remaining employees collapse into counts.
- The complete CEO -> department lead -> employee organization tree belongs to the dedicated Organization page with search, filtering, folding, and large-scale rendering support.
- Project War Room is the operating unit; Workflow is Project-driven and Task stays an internal execution record.
- Dashboard Widgets remain configurable operating signals, but do not define the default headquarters layout and cannot introduce arbitrary queries or commercial rules.
- This stage approved no implementation; the bounded implementation decision is recorded in the V3.1 section below.

## 2026-07-10 Phase-1C CEO Office UI V3.1

- V3 design source of truth: `docs/design/phase1c-ceo-office-ui-v3.md`; the previous redesign document is superseded for homepage product structure.
- Headquarters is now an event-driven CEO operating space: Company/Strategy -> Needs CEO Decision -> Important Reports -> Core Project Command -> Organization Health -> AI Resource Operations / Value / Knowledge.
- The homepage never renders the full organization tree. Organization Health only shows department health signals; Organization Center owns full Department / AI Employee navigation at scale.
- Project remains the operating core; Task stays internal to Project / Workflow / Employee execution contexts.
- AI Employee presentation is identity-first: role, Persona, Skill, current Project, state, reports, deliverables, and AI employee identity markers rather than a generic employee or Agent list.
- AI Employee visual identity must stay consistent with the confirmed homepage style: lightly cartooned, semi-real, professional virtual-person portraits with a bit of digital-employee distance. Use AI badges, role labels, persona hints, skill chips, or subtle light treatment to mark AI identity; do not use robot/mechanical avatars or photo-real human staff portraits as employee portraits.
- Project War Room defaults to CEO View: project goal, AI employee owner, workflow summary, CEO intervention points, and Project Knowledge Chain. Technical details are expandable and must not dominate the default view.
- Decision Center, Strategic Meeting Room, and Brainstorm Room are product-defined but runtime-gated. They require separate Contracts and executable Issues before implementation; frontend mock behavior is forbidden.
- Visual direction is softened from military-control-center density toward glass-like, spatial, high-end AI company headquarters with more whitespace and fewer dense data cards.
- UI remains product-owned. Delivery roles may not independently change information architecture, page hierarchy, interaction flow, or visual direction.
- Product direction is approved on 2026-07-11. Frontend implementation is limited to `issues/phase1c_ceo_office_ui_first_slice.md`; backend, API, data model, Admin, Billing, Marketplace, Credential Vault, Workflow Runtime, and runtime-gated CEO modules remain blocked.

## Next Step

系统交付席 implements `issues/phase1c_ceo_office_ui_first_slice.md` within its Allowed Files, then routes verification to 质量运行席.

Current executable Phase-1C Issue: `issues/phase1c_ceo_office_ui_first_slice.md`.

Handoff: HANDOFF_REQUIRED to 系统交付席.

## Open Questions

- Decision Center、Important Reports Inbox、Strategic Meeting Room、Brainstorm Room 仍缺 Runtime Contract，不进入首个实现切片。
- 当前工作树包含既有删除项和未跟踪目录；系统交付席必须使用精确文件范围，禁止混入。

## 2026-07-07

2026-07-07: D2 Evolution Governor Sandbox implemented (GovernorSandbox throwaway-copy substrate + additive EvolutionGovernor.demonstrate(); writes only to OS temp, zero authoritative writes, rollback restores exactly), verified PASS by 质量运行席 (63 tests), accepted by 产品规划席. D2 slice closed — ADR-0016 (D1→D3→D2) fully complete.

- 2026-07-07 (21:33 GMT+8): User (COO) chose **Option A** — open ADR-0017 future gate (multi-tenant CEO + department catalog) and keep pushing. Feishu notify preference recorded (stage-report / confirmation stop points → Feishu push; connector now connected). Prepared ADR-0017 gate submission package: `issues/049_adr0017_future_gate.md` (gate issue) + `issues/050_adr0017_future_gate_submission_package.md` (decision request to 总控决策席, options a/b/c). Awaiting 总控决策席 gate decision — natural stop, Feishu notification sent.

- 2026-07-07 (22:08 GMT+8): Feishu scope approved by user → bot added user to group `oc_1b559ad633e40345229275d15f7e8d42`「Curis 开发通知」, stage report pushed (message_id om_x100b6be4c64c4ca8b3df4b7db00fe6e). 总控决策席 accepted ADR-0017 option a (gate OPEN). 系统交付席 drafted + implemented **D1 `tenant_id` reservation**: ADR-0022 boundary, `issues/051` slice, new `backend/app/tenant_context.py`, additive `_ensure_column` on `tasks`+`evolution_events`, `backend/tests/test_d1_tenant.py` (6 tests). 质量运行席 verified PASS (reviews/050 boundary, reviews/051 implementation; 69 tests green). Awaiting 产品规划席 acceptance of issue 051.

- 2026-07-07 (23:27 GMT+8): Operating-mode change per user directive. **Slice acceptance (产品规划席) delegated to 主理人齐活林**; **user retains 总控决策席 (gate only)**; routine stage reports / slice acceptance NO LONGER reported to user — team pushes autonomously, escalate only on major planning conflict or required user input. 主理人 accepted D1 (issue 051) + D2 boundary+gate (issue 052) under pre-authorized ADR-0017 option-a roadmap; dispatched 系统交付席 (Kou) to implement D2 reservation T01–T05. D3/D4 follow same autonomous pipeline.

- 2026-07-08 (00:24 GMT+8): D2 部门目录 reservation **slice CLOSED**. 系统交付席 (Kou) implemented (c8a30781, 4 files +459: department_manifest.py / department_catalog.py / database.py additive department_types + seed / test_d2_department.py). 质量运行席 (Yan) implementation verification reviews/053 PASS-WITH-NOTES (81 tests green; AC1–8 read-code verified; forbidden-zone independent scan clean; routing NoOne). 主理人 (齐活林, 产品规划席 delegation) ACCEPTED D2 (issue 052 closed). ADR-0017 D1✅ D2✅ → next 系统交付席 (Gao) defines D3 (self-observability / meta-loop) reservation boundary.

- 2026-07-08: D3 自可观测 reservation **boundary ACCEPTED + gate** by 主理人齐活林 (产品规划席 delegation) under ADR-0017 option-a pre-authorized roadmap. 系统交付席 (Gao) delivered ADR-0024 + issues/054 (design-only, zero schema delta, database.py unchanged); 质量运行席 (Yan) boundary verification reviews/054 PASS-WITH-NOTES (10-class forbidden-zone clean; reused base EvolutionEventLog/DepartmentCatalog/TenantContext signatures matched; notes N1–N5 non-blocking). Next: 系统交付席 (Kou) implements D3 reservation T01–T04 (zero schema delta), then 质量运行席 (Yan) verifies.

- 2026-07-08: D3 自可观测 reservation **slice CLOSED**. 系统交付席 (Kou) implemented (22c5cd55, 2 files +287: department_observability.py / test_d3_observability.py). 质量运行席 (Yan) implementation verification reviews/055 PASS-WITH-NOTES (90 tests green; AC1–8 read-code verified; forbidden-zone independent scan clean; database.py zero delta; routing NoOne). 主理人 (齐活林, 产品规划席 delegation) ACCEPTED D3 (issue 054 closed). ADR-0017 D1✅ D2✅ D3✅ → next 系统交付席 (Gao) defines D4 (two-tier governance) reservation boundary.

- 2026-07-08: D4 两级治理 reservation **boundary ACCEPTED + gate** by 主理人齐活林 (产品规划席 delegation) under ADR-0017 option-a pre-authorized roadmap. 系统交付席 (Gao) delivered ADR-0025 + issues/055 (design-only, zero schema delta, database.py unchanged); 质量运行席 (Yan) boundary verification reviews/056 PASS-WITH-NOTES (A–F all pass; reused base DepartmentCatalog/CompanyTopology/EvolutionEventLog signatures matched; LOCKED_ACTIONS four actions clean; notes N1–N4 non-blocking). 主理人 accept+gate reviews/057. Next: 系统交付席 (Kou) implements D4 reservation T01–T04 (governance.py read-only facade + test_d4_governance.py, zero schema delta).

- 2026-07-08: D4 两级治理 reservation **implemented** by 系统交付席 (Kou) — commit b97728d4 (2 files +393: governance.py / test_d4_governance.py), 100 tests green (baseline 90 + 10 D4), zero schema delta (database.py unchanged), forbidden-scope scan clean. Deviation note (non-blocking): `selectable_type_keys` holds `list[DepartmentType]` (per AC2 literal equality with `DepartmentCatalog.list_types()`) while ADR-0025 class-diagram annotates `list[str]` — doc wording inconsistency only, tests green. Next: 质量运行席 (Yan) implementation verification (reviews/058).

- 2026-07-08: D4 两级治理 reservation **slice CLOSED**. 系统交付席 (Kou) implemented (b97728d4, 2 files +393: governance.py / test_d4_governance.py). 质量运行席 (Yan) implementation verification reviews/058 PASS-WITH-NOTES (100 tests green; AC1–10 read-code verified; forbidden-zone independent scan clean; database.py zero delta; routing NoOne). 主理人 (齐活林, 产品规划席 delegation) ACCEPTED D4 (issue 055 CLOSED). **ADR-0017 四个子决策（D1✅ D2✅ D3✅ D4✅）reservation 边界与实现全部收口** — 当前预授权 roadmap 已完成。后续真实实现（D1.impl–D4.impl / D4.platform：实例化 / 平台级管理后台 / 真实公司持久化 / 解除 gate / 跨公司策略 / 外部平台）须各自独立小 gate + 总控决策席 + 安全边界席 review，超出当前预授权范围。

- 2026-07-08 (02:33 GMT+8): 用户选定 **D2.impl 部门真实实例化** 作为首个真实实现切片（超出 ADR-0017 option-a 预授权）。主理人建团队 `software-curis-d2impl`，派 系统交付席(高见远) 起草 D2.impl gate 提交包 = `docs/decisions/ADR-0026-d2-impl-department-instantiation.md` + `issues/056_adr0017_d2_impl_department_instantiation.md`（commit be49328e，2 文件 +531）。设计=additive `departments` 表(沿用 D1 tenant_id 哨兵列 'default') + `DepartmentCatalog.create_department/list_departments/get_department`（落实 instantiate_department hook）；connect_platform/manage_employees 仍 NotImplementedError；manage_department_types(ADR-0025 LOCKED) 不触碰；D3/D4 facade 接口不动；不写 evolution_events；单租户纪律保持。禁止区(Employee CRUD/外部平台/真实多租户/L6 ROI/自动改码/复杂UI/向量库)零触碰。Gate 要求：总控决策席批准 + 安全边界席 review；放行后 Kou 实现 T01–T03 + Yan 验证。当前状态：**gate 已批准 (2026-07-08 02:33 GMT+8, 总控决策席 + 安全边界席 review 随选确认)，系统交付席(Kou) 实现 T01–T03 中**。

- 2026-07-08: D2.impl 部门真实实例化 **实现完成**（系统交付席 Kou, commit `7617ed2c`：additive `departments` 表 7 列无 FK 复用 D1 tenant_id 哨兵列 `'default'` + `DepartmentCatalog.create_department/list_departments/get_department` 三真实落库方法，落实 `instantiate_department` hook；`connect_platform`/`manage_employees` 仍 NotImplementedError；跨连接 round-trip 实证真持久化；114 tests 全绿）。主理人一致性修复 `4ec02a59`（删除过时 reservation 契约断言 `assertNotIn("departments")`，保 clean checkout 全绿）。

- 2026-07-08: D2.impl 部门真实实例化 **实现验证 PASS-WITH-NOTES**（质量运行席 Yan, reviews/059, commit `67ab1616`）：独立实跑 114 全绿，AC1–AC10 逐条读码核实通过，禁止区独立 grep 全绿（`manage_employees`/`connect_platform` 仅 2 处 def 占位 NotImplementedError；无 employee 表写 / 外部凭证 / L6 ROI / auto_modify_code / 新 endpoint / evolution_events 写 / 向量 embedding），`database.py` 纯 additive 建表、基座+facade 零改动，路由 NoOne。非阻断注记 N1（测试实际 14 例 vs 文档称 10，真实 114 全绿已实证）= 纯文档口径差异，无需改码。

- 2026-07-08: D2.impl 部门真实实例化 **slice CLOSED**（主理人齐活林, 产品规划席 delegation）：issue 056 置 CLOSED；reviews/060 主理人验收评审落盘；T-155/T-156/T-157 标记 DONE；ADR-0017 四个子决策中**首个真实实现切片收口**。收口后即按用户指令创建飞书条件提醒自动化（D2.impl 收口后 15 分钟内无下一步指令则向「Curis 开发通知」群推送软性提醒）。

- 2026-07-08: 用户补充指令——D-series 收口里程碑（如本 D2.impl CLOSED）后若 15 分钟内无下一步指令，经飞书（群 `oc_1b559ad633e40345229275d15f7e8d42`）推送软性提醒（局部覆盖「非冲突不飞书」默认偏好，仅里程碑 nudge）。已记入 `.workbuddy/memory/2026-07-08.md`。

- 2026-07-08 (03:05 GMT+8): 用户新指令（大白话）——**自主推进窗口**：从现在到上午 10:00，团队自行拆解分配开发任务、推进进度，不需要用户确认；若某动作实在需用户确认才能继续，先记下来跳过、转做其他任务，10:00 整汇总汇报。据此执行：①撤销原「D2.impl 收口后 15 分钟飞书提醒」自动化（实测仍 ACTIVE，已 `automation_update(mode=delete)` 软删）；②新建「10:00 汇总汇报」一次性自动化（id `automation-1783451439781`，scheduleType=once，scheduledAt=2026-07-08T10:00:00）经飞书「Curis 开发通知」+会话呈现；③建团队 `software-curis-autopush`（主理人齐活林 + 高见远草拟 gate 包 + 寇豆码/严过关按需）。D-series 真实实现（D1.impl/D3.impl/D4.impl/D4.platform）执行前仍须 **总控决策席 + 安全边界席 gate**（升级边界不变）→ 属「需用户确认」动作，按指令**记录跳过**；草拟 gate 包（设计-only）不需确认，可自主进行。已完成：高见远(software-architect) 草拟 `ADR-0027` D-series real-impl roadmap + `issue 057–060` 四个真实实现切片 gate 提交包（design-only，不写码），主理人复核通过、本地提交 `77c8b2fb`（5 文件 +949 行，无 remote）。Roadmap 定序 **S1 D1.impl → S2 D3.impl → S3 D4.impl → S4 D4.platform**，含 gate 矩阵 + LOCKED_ACTIONS 解锁映射 + 依赖图 + 全局 Forbidden Scope；架构师建议最优先确认 S1 D1.impl（首次翻转 `is_multi_tenant()→True`，安全边界席强制 review，且为 S2/S3/S4 的 tenant 作用域前置）。**D1.impl/D3.impl/D4.impl/D4.platform 真实执行仍须 总控决策席 + 安全边界席 gate → 按窗口指令记录跳过**，本窗口无更多可自主执行的开发任务，团队收尾。

- 2026-07-08 (03:36 GMT+8): 用户(总控决策席) 确认 **D1.impl / D3.impl / D4.impl / D4.platform 依序全部批准**（roadmap gate ADR-0027 + issue 057–060 获准），原「记录跳过」解除，进入真实实现执行阶段。安全边界席 review 随 gate 包内嵌安全清单（隔离模型 / 按租户凭证隔离架构 / 4 个 LOCKED_ACTIONS 锁定 / 无实际外部凭证落地）在 S1/S4 落实，由主理人于 accept 阶段复核。本窗口转为「真实实现执行」模式：重建团队 `software-curis-realimpl`，按 **S1→S2→S3→S4** 跑「工程师实现 → QA 验证 → 主理人 accept」流水线，自主推进、本地提交、10:00 汇总。S1 D1.impl 先行（基础翻转 `is_multi_tenant()→True`，是 S2/S3/S4 的 tenant 作用域前置）；工程师(寇豆码) 实现中。

- 2026-07-08 (S1 D1.impl CLOSED, 主理人 accept ~03:50 GMT+8): 总控决策席 03:36 确认全部四个真实实现 gate 后，S1 D1.impl 工程师实现完成并经 QA + 主理人 accept，commit `70e05652`（13 files, +356/−77, 121 tests green）。实现=真实多租户隔离（is_multi_tenant()→True + tenants 注册表零凭证列 + ResultStore WHERE tenant_id 读过滤 + X-Tenant-Id scoping 中间件）；4 LOCKED_ACTIONS 全程锁定、禁止区零触碰、跨租户隔离实证。主理人记录 2 处 non-blocking 偏差（tenants 列名命名、department_catalog 跨切片守卫修正）。**S2 D3.impl CLOSED**（issue 058, 主理人 accept, commit `dfa2315e`, 128 tests green）：真实 `DepartmentObservability`（部门→事件关联+call_count/success_rate/quality_line_hits 真实聚合+自反馈闭环持久化 `department_observations`，默认不写 evolution_events）；删除矛盾的 D3 reservation 测试(可逆)。4 LOCKED_ACTIONS 锁定、禁止区零触碰。**S3 D4.impl CLOSED**（issue 059, 主理人 accept, commit `20cb4776`, 138 tests green）：真实 `CompanyGovernance`（propose 持久化+人工批准流(不解除 gate)+apply_proposal 落地 company_department_state+真实 departments enabled/disabled+受控 governance.propose/apply 事件写，gate 批准）；4 LOCKED_ACTIONS 锁定、禁止区零触碰、human-approval gate 实证。**S4 D4.platform CLOSED**（issue 060, 主理人 accept + 安全边界席复核, commit `e2271e60`, 155 tests green）：解锁 `manage_department_types`+`cross_company_policy`（真实 CRUD + 全局护栏 + `/api/platform/*` 鉴权路由 + 前端管理控制台 UI（UI 解禁由 03:36 总控确认覆盖））；`lift_human_approval_gate`/`auto_modify_code` 仍全程锁定；受控 `evolution_events` 写仅 5 批准类型；安全边界席清单全过。**ADR-0027 D-series real-impl roadmap S1→S2→S3→S4 全四切片 CLOSED，roadmap COMPLETE（155 tests green）。**
