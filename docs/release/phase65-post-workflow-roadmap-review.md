# Phase-6.5 Post-Workflow Roadmap Review

Date: 2026-07-09

Status: roadmap review and next-gate preparation only.

Scope: Workspace line. No new runtime feature, no Workflow expansion, no Billing implementation, no Marketplace implementation, no ROI, no business module implementation, and no Credential Vault security-boundary change.

## Product Progress

Curis Workspace can now demonstrate a Software R&D AI team executing an ordered SOP workflow, with employee/capability/credential usage attributed through redacted usage_event and audit_event records.

## 1. Current Capability Review

### 1.1 Admin Platform Completed Capability

- Tenant and CEO management baseline for commercial multi-tenant operation.
- Official capability supply through read-only catalog APIs.
- Admin usage_event read projection by `tenant_id`.
- Admin audit_event read projection by `tenant_id`.
- Redacted observability for Workspace usage, credential activity, employee attribution, and workflow attribution.
- Admin / Workspace shared-contract baseline from ADR-0028.

### 1.2 Workspace Completed Capability

- AI Task Executor task create, run, status, history, and result path.
- Model Gateway Adapter path through New API compatible interface.
- Official capability read through `/api/catalog/*`.
- tenant_private private model / tool / connector metadata.
- Official + tenant_private capability selector.
- Tenant-scoped private capability isolation.
- Workspace runtime guard: no `/api/platform/*` calls.
- Local/demo company frame with department catalog and department activation.

### 1.3 AI Employee System Completed Capability

- Software R&D DepartmentTemplate and DepartmentInstance.
- Six R&D EmployeeTemplates:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- EmployeeInstance creation under `tenant_id`, `company_id`, and `department_id`.
- EmployeeCapabilityBinding over official and tenant_private capability sources.
- Task creation can select an employee.
- usage_event can attribute execution to employee identity and role.

### 1.4 Credential Vault Completed Capability

- tenant_private Credential Metadata Model without plaintext persistence.
- `local-dev://tenant/{tenant_id}/credential/{credential_id}` reference generation for local/demo.
- Production-reserved `vault://tenant/{tenant_id}/credential/{credential_id}` and `kms://tenant/{tenant_id}/credential/{credential_id}` formats.
- Local/demo credential backend with server-side short-lived secret resolution.
- Resolver tenant validation, disabled credential rejection, and production `local-dev://` rejection.
- Vault/KMS adapter interface stubs.
- Workspace credential API for create, test, bind, unbind, disable/delete.
- private model / tool / connector credential_ref binding.
- Redaction for API response, errors, logs, usage_event, and audit_event.

Current limitation: local/demo private credentials are truly executable through resolver, but production customer credentials still require a real Vault/KMS backend and security gate.

### 1.5 Workflow MVP Completed Capability

- Official Software R&D sequential WorkflowTemplate.
- Tenant-scoped WorkflowInstance and WorkflowRun.
- Ordered WorkflowStep records.
- StepAssignment per step.
- StepResult per completed step.
- `run-next-step` bounded sequential execution.
- Role-based step assignment for Tech Lead, Product Manager, Architect, Frontend Engineer, Backend Engineer, QA Engineer, and Tech Lead final report.
- EmployeeCapabilityBinding reuse for step execution.
- tenant_private private model execution through Credential Resolver and Model Gateway Adapter.
- usage_event workflow / step / employee / capability attribution.
- audit_event workflow state attribution.
- Minimal Workflow UI inside the existing Workspace operation console.

### 1.6 Current Still Missing Capability

- One-click local demo seed and browser E2E package.
- Production Vault/KMS implementation for real customer private credentials.
- Billing ledger / invoice / plan / quota lifecycle.
- Billing-grade cost authority rather than estimate-only `estimated_cost`.
- Workflow v2 capabilities such as DAG, pause/resume, retry, manual approval, and workflow template versioning.
- Multi-department workflows.
- Capability Marketplace governance and review model.
- Hosted production deployment hardening.
- Workspace/Admin operational monitoring beyond local/demo evidence.

### 1.7 Current Explicitly Deferred Capability

- ROI system.
- Billing MVP implementation in Workspace.
- Capability Marketplace.
- Complex DAG workflow builder.
- Visual workflow editor.
- Cross-department business workflows.
- Content operations / investment / ecommerce departments.
- Automatic employee recruiting.
- Complex human approval flow.
- Full production queue scheduler.
- Admin reading tenant_private plaintext secrets.
- Workspace calling `/api/platform/*` at runtime.

## 2. Demo Readiness Review

Phase-6 is demonstrable but still manual:

- Demo startup uses separate backend, frontend, and local model gateway terminals.
- Demo seed requires multiple API calls.
- Workflow execution uses repeated `run-next-step`.
- Screenshot collection is manual.
- Admin usage/audit proof requires manual query.

This is acceptable for internal local/demo validation. It is not yet ideal for investor, customer, or external team demos because the operator has to explain too many setup steps and boundaries.

Recommended conclusion: the next Workspace P0 should be a demo/release hardening gate before adding another large product layer.

## 3. Risk Review

### 3.1 Product Experience Risk

The product now has the right story: CEO -> R&D team -> SOP workflow -> final report. The weak point is repeatability. If a demo fails due to manual setup rather than product behavior, the system will look less mature than it is.

Mitigation: Phase-7 local/demo release hardening with seed, scripted startup, E2E, and screenshot package.

### 3.2 Security Risk

Credential Vault is safe for local/demo, but production real-secret custody is not complete. Real customer credentials should not be accepted before Vault/KMS implementation and security review.

Mitigation: separate production credential vault gate before hosted customer use.

### 3.3 Commercialization Risk

usage_event is now rich enough for usage analytics, but not billing-grade. `estimated_cost` is useful for product feedback, not invoice settlement.

Mitigation: Admin-led Billing Usage Contract gate, with Workspace only preserving event fields and attribution.

### 3.4 Workflow Scope Risk

Phase-6 uses a sequential SOP. Adding DAG, retries, pause/resume, or multi-department flows too soon would make the workflow engine productively interesting but operationally risky.

Mitigation: defer Workflow v2 until demo hardening and billing/credential gates are clearer.

### 3.5 Marketplace Risk

Marketplace requires review policy, billing/revenue rules, capability quality standards, and template trust boundaries. It remains too early.

Mitigation: keep Marketplace deferred.

## 4. Next-Phase Candidate Evaluation

### A. Phase-7 Local/Demo Release Hardening

Goal:

- Make the Phase-4 + Phase-5 + Phase-6 demo repeatable from a clean local database.
- Reduce manual setup and evidence collection.

Candidate scope:

- Demo seed script.
- Startup/runbook consolidation.
- Browser E2E for the complete demo chain.
- Screenshot package/checklist.
- Demo copy for CEO-facing explanation.
- Release checklist and known-gap confirmation.

Why now:

- It turns the working system into a reliable story.
- It lowers future team handoff cost.
- It does not expand product scope.

Recommendation: P0.

### B. Production Credential Vault/KMS Gate

Goal:

- Move from local/demo credential backend to production-ready secret custody.

Candidate scope:

- Real Vault/KMS adapter selection.
- Production `vault://` or `kms://` resolver behavior.
- Secret rotation/disable/delete policy.
- Operator recovery process.
- Security review.

Why not first:

- It is essential before hosted customer use, but it does not improve local demo repeatability.
- It likely requires security and deployment decisions outside Workspace alone.

Recommendation: P1, security-gated.

### C. Billing Usage Contract Gate

Goal:

- Convert usage_event richness into billing-ready contract planning.

Candidate scope:

- Billing event contract.
- Plan/quota/invoice model draft.
- Mapping from workflow/employee/capability usage to billing aggregation.
- Admin ownership boundary.
- Workspace compatibility requirements.

Why not Workspace implementation:

- Billing authority belongs primarily to Admin Platform.
- Workspace should preserve redacted usage and attribution, not own invoice logic.

Recommendation: P1/P2, Admin-led with Workspace contract review.

### D. Workflow v2 Boundary Gate

Goal:

- Explore advanced workflow capabilities after the sequential SOP proves stable.

Candidate scope:

- Retry policy.
- Pause/resume.
- Manual approval checkpoint.
- Step rerun.
- Template versioning.
- Multi-department future boundary.

Why not now:

- Sequential SOP is enough to demonstrate AI company collaboration.
- v2 features would expand state-machine complexity.

Recommendation: P2.

### E. Capability Marketplace

Goal:

- Allow capability/template sharing across tenants.

Why defer:

- Governance, billing, review, security, and template quality standards are not ready.

Recommendation: P3 or later.

## 5. Roadmap Recommendation

### P0: Phase-7 Local/Demo Release Hardening

Why:

- The current product is valuable enough to demonstrate, but the demo path is manual.
- Hardening improves reliability without adding product scope.

Problem solved:

- Makes the AI company story repeatable for the user, new teams, and demos.

Risk if not done:

- Future demos remain fragile and operator-heavy.

Dependency:

- No new product gate needed beyond a bounded documentation/automation gate.

Development recommendation:

- Enter after 总控决策席 approves the gate.

### P1: Production Credential Vault/KMS Gate

Why:

- Real customer tenant_private capability use requires production-grade secret custody.

Problem solved:

- Moves private capability execution toward commercial readiness.

Risk if not done:

- Curis remains local/demo only for customer private credentials.

Dependency:

- Requires 安全边界席 and likely deployment/environment decisions.

Development recommendation:

- Prepare gate after demo hardening starts or completes.

### P1/P2: Billing Usage Contract Gate

Why:

- Commercial multi-tenant AI company system needs metering and billing.
- usage_event now contains tenant/workflow/step/employee/capability attribution.

Problem solved:

- Defines how Admin turns usage into billing evidence without Workspace owning invoices.

Risk if not done:

- Product can demonstrate execution but cannot validate monetization.

Dependency:

- Admin Platform ownership; Workspace participates only in contract compatibility.

Development recommendation:

- Admin-led planning can run in parallel, but Workspace should not implement billing logic.

### P2: Workflow v2 Boundary Gate

Why:

- Current sequential SOP is intentionally minimal.

Problem solved:

- Defines future retry, pause/resume, approval, rerun, and template-version scope.

Risk if not done:

- Workflow remains usable but limited to straight-line SOP.

Dependency:

- Phase-7 demo evidence should come first.

Development recommendation:

- Boundary-only review after demo hardening.

### P3: Capability Marketplace

Why:

- Marketplace matters for the long-term ecosystem, not immediate local/demo quality.

Problem solved:

- Future cross-tenant capability/template distribution.

Risk if done too early:

- Governance and billing risks expand before the system is ready.

Dependency:

- Billing, review governance, template quality standards, and security model.

Development recommendation:

- Defer.

## 6. Issue Drafts Prepared

- `issues/phase7_local_demo_release_hardening_gate.md`
- `issues/phase7_production_credential_vault_gate.md`
- `issues/phase7_billing_usage_contract_gate.md`

## 7. Recommendation

Proceed to Phase-7 Local/Demo Release Hardening first.

Do not start Workflow v2, Billing implementation, Marketplace, ROI, or new business modules yet.

## 8. Verification

This phase is documentation and issue drafting only.

Verification performed:

- `git diff --check -- docs/release/phase65-post-workflow-roadmap-review.md issues/phase7_local_demo_release_hardening_gate.md issues/phase7_production_credential_vault_gate.md issues/phase7_billing_usage_contract_gate.md knowledge/CURRENT_CONTEXT.md`
  - Result: pass.
- `! rg -n "/api/platform/" frontend/app/page.js backend/app/workflow_runtime.py backend/app/result_store.py backend/app/evolution_event_log.py`
  - Result: pass.
- `! rg -n "sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|ghp_[A-Za-z0-9]{36}" docs/release/phase65-post-workflow-roadmap-review.md issues/phase7_local_demo_release_hardening_gate.md issues/phase7_production_credential_vault_gate.md issues/phase7_billing_usage_contract_gate.md knowledge/CURRENT_CONTEXT.md`
  - Result: pass.
