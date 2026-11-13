# Phase-5.5 Post-G2 Roadmap Review

Date: 2026-07-09

Status: roadmap review and contract preparation only.

Scope: Workspace line. No Workflow implementation, no Billing implementation, no Marketplace implementation, no business module implementation, no Credential Vault security-boundary change.

## Product Progress

Curis Workspace can now demonstrate an R&D AI employee using tenant_private private capability credentials through the server-side resolver, with usage_event and audit_event retaining only redacted attribution that Admin can observe without seeing plaintext secrets.

## 1. Current Capability Review

### 1.1 Admin Platform Completed Capability

- Tenant and CEO management baseline for commercial multi-tenant operation.
- Official capability supply boundary through read-only catalog APIs.
- Admin usage_event read projection by `tenant_id`.
- Admin audit_event read projection by `tenant_id`.
- Redacted observability for Workspace usage and credential activity.
- Admin / Workspace shared-contract baseline from ADR-0028.

### 1.2 Workspace Completed Capability

- AI Task Executor task create, run, status, history, and result path.
- Model Gateway Adapter path through New API compatible interface.
- Official capability read through `/api/catalog/*`.
- tenant_private private model / tool / connector metadata.
- Official + tenant_private capability selector.
- Tenant-scoped private capability isolation.
- Workspace runtime guard: no `/api/platform/*` calls.

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
- If no employee is selected, Tech Lead/default R&D employee fallback is available.
- usage_event can attribute task execution to employee identity or role.

Current limitation: the employee system is still single-employee execution per task. It is not yet multi-employee SOP collaboration.

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

Confirmation: tenant_private private capability moved from "configurable only" to "local/demo truly executable" when backed by resolver and demo credential backend. Production usability still requires a real Vault/KMS backend.

### 1.5 usage_event / audit_event Completed Capability

- usage_event records tenant, task, employee, capability, model, token/cost estimate, status, and credential digest attribution where applicable.
- audit_event records credential lifecycle and resolver events with allowlisted redacted fields.
- usage_event / audit_event do not store plaintext API key, token, secret, credential value, Authorization header, or raw sensitive provider response.
- Admin can observe redacted attribution.
- Admin cannot see tenant_private plaintext credential.

### 1.6 Current Still Missing Capability

- Multi-employee SOP Workflow.
- WorkflowRun / WorkflowStep level execution trace.
- Step-level usage_event attribution.
- Step-level audit_event status transitions.
- Production Vault/KMS implementation.
- Credential management UI.
- Billing aggregation and invoices.
- Marketplace governance.
- External production deployment hardening.

### 1.7 Current Explicitly Deferred Capability

- ROI system.
- Billing MVP implementation.
- Capability Marketplace.
- Complex DAG workflow builder.
- Cross-department workflows.
- Content operations / investment / ecommerce departments.
- Automatic employee recruiting.
- Complex human approval flow.
- Full production queue scheduler.
- Admin reading tenant_private plaintext secrets.

## 2. Phase-6 Workflow MVP Feasibility

### 2.1 Why Workflow Is Now The Right Next Step

Phase-4 made R&D employees visible and executable. Phase-5 made tenant_private capabilities safer and more real by resolving credentials through the server-side vault boundary. The biggest remaining gap in the AI company experience is that employees still execute as isolated single actors. Workflow is now the most direct way to turn "AI employees" into an "AI company" by showing coordinated SOP work.

### 2.2 G2 Dependency Status

G2 Credential Vault removes the main blocker for real tenant_private capability use inside workflows:

- Employees can bind private capabilities.
- Private capabilities can bind credential_ref.
- Runtime can resolve credential_ref through resolver.
- usage_event and audit_event can attribute credential use without exposing secrets.

Production Vault/KMS remains future work, but local/demo Workflow MVP no longer needs fake `scheme:reference` placeholders for private model execution.

### 2.3 Employee System Reuse

Phase-6 can reuse:

- EmployeeTemplate role definitions.
- EmployeeInstance tenant/company/department scope.
- EmployeeCapabilityBinding.
- Tech Lead default fallback.
- Employee role metadata for step ownership.
- Existing Workspace employee management UI as the source for available employees.

### 2.4 Task Execution Reuse

Phase-6 can reuse:

- Existing task record as the CEO requirement anchor.
- Existing task run/result path for per-step execution.
- Model Gateway Adapter-only model calls.
- Existing Result Store and usage_event writer.
- Existing tenant and ceo header conventions.

Important rule: existing single-task execution must remain backward-compatible. Workflow should be an added orchestration layer, not a rewrite of Task Execution.

### 2.5 Capability Binding Reuse

Each workflow step should resolve the assigned employee's enabled bindings:

- `official` capability source from Admin catalog metadata.
- `tenant_private` capability source from Workspace private capabilities.
- `marketplace` remains reserved only.
- Step runtime may select the highest-priority enabled binding matching the step's required capability type.
- Private model execution must still pass through Credential Resolver and Model Gateway Adapter.

### 2.6 usage_event / audit_event Tracking

usage_event should add or populate:

- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `credential_id`
- `credential_ref_digest`
- `status`

audit_event should record workflow state changes:

- `workflow.created`
- `workflow.started`
- `workflow.step_assigned`
- `workflow.step_started`
- `workflow.step_completed`
- `workflow.step_failed`
- `workflow.completed`
- `workflow.cancelled`

Audit payload must be allowlisted and must not include prompts containing secrets, plaintext credentials, provider raw sensitive responses, or hidden resolver output.

### 2.7 Minimum Workflow MVP

Do:

- WorkflowTemplate.
- WorkflowInstance.
- WorkflowRun.
- WorkflowStep.
- StepAssignment.
- StepResult.
- One official Software R&D SOP template.
- Sequential execution only.
- Tech Lead starts/breaks down.
- Product Manager clarifies requirements.
- Architect drafts technical plan.
- Frontend Engineer / Backend Engineer execute bounded implementation steps.
- QA Engineer verifies.
- Tech Lead summarizes final report.
- Each step has one assigned employee.
- Each employee uses own capability binding.
- usage_event gets workflow and step attribution.
- audit_event gets workflow status changes.

### 2.8 Workflow Capabilities To Defer

- Complex DAG.
- Visual workflow editor.
- Cross-department workflow.
- Dynamic employee recruiting.
- Autonomous arbitrary task decomposition.
- Parallel branches.
- Complex approval workflow.
- Production queue scheduler.
- Marketplace workflow templates.
- ROI optimization loop.

## 3. Phase-6 MVP Scope Recommendation

Recommended MVP shape:

```text
CEO creates R&D requirement
-> WorkflowRun is created from official Software R&D WorkflowTemplate
-> Tech Lead receives and creates bounded step plan
-> Product Manager produces requirement clarification
-> Architect produces implementation plan
-> Frontend Engineer runs frontend step when assigned
-> Backend Engineer runs backend step when assigned
-> QA Engineer runs verification step
-> Tech Lead produces final report
-> CEO views step outputs and final report
```

State model:

```text
draft -> ready -> running -> completed
                  |-> failed
                  |-> cancelled
```

First version should expose a `run-next-step` action rather than uncontrolled automatic background execution.

## 4. Billing MVP Evaluation

Current usage_event is sufficient for early usage statistics:

- `tenant_id`
- `employee_id` / `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `model_gateway_id`
- `model_name`
- token fields
- `estimated_cost`
- `status`
- `created_at`

Billing is not yet ready for production charging because:

- `estimated_cost` is still estimate-level, not settlement-grade.
- No plan/quota/invoice lifecycle exists.
- No billing_event ledger exists.
- No payment or invoice workflow is approved.
- Cost authority likely belongs on Admin side.

Recommendation:

- Billing should come after Workflow MVP as a product mainline.
- Admin Platform can research Billing in parallel.
- Billing should not block Phase-6 Workflow because Workflow increases usage_event richness and will make billing attribution more valuable.
- A future Billing MVP probably needs `billing_event`, `plan`, `quota`, `invoice`, and admin read-only aggregation.

## 5. Demo Polish Evaluation

Demo Polish remains useful and parallel-safe.

Recommended scope:

- Demo seed for Phase-4 + Phase-5 + Phase-6 once workflow exists.
- One-command local startup wrapper.
- Browser E2E for the core demo chain.
- Screenshot package.
- Demo copy explaining local/demo limits.
- Combined Phase-4 employee + Phase-5 credential + Phase-6 workflow script.

Priority:

- Keep as P2 parallel track.
- It should not block Phase-6 architecture and implementation.

## 6. Capability Marketplace Evaluation

Marketplace should remain deferred.

Reasons:

- Marketplace review/governance model is not complete.
- Billing and revenue-share rules are not ready.
- Capability template quality standards are not mature enough.
- Workflow templates are not yet runtime-proven.
- Introducing cross-tenant distribution before Workflow MVP would expand governance and security risk too early.

Recommendation:

- Revisit after Phase-6 Workflow MVP and at least a Billing/Governance planning gate.
- Earliest reasonable target: Phase-7 or later.

## 7. Roadmap Recommendation

### P0: Phase-6 Workflow MVP

Why:

- It is the clearest next step from "single employee executes task" to "R&D team collaborates by SOP".
- G2 removed the private credential blocker for tenant_private capability execution.
- It makes Curis feel like an AI company system, not just a task runner with employee labels.

Problem solved:

- Converts AI Employee System from role attribution into step-by-step team collaboration.

Risk if not done:

- Product will still require explanation that employees are not really working together.
- Long-term AI company vision remains under-demonstrated.

Dependencies:

- Requires Phase-6 gate acceptance.
- Must preserve Phase-4 Employee and Phase-5 Credential Vault boundaries.

Recommendation:

- Enter development after this roadmap review is accepted.

### P1: Demo Polish

Why:

- Workflow will add more moving parts; a stable demo script and screenshots will reduce demo risk.

Problem solved:

- Makes local/demo repeatable for team handoff and investor/customer walkthroughs.

Risk if not done:

- Demo will remain command-heavy and fragile.

Dependencies:

- Can run in parallel but should not change core product behavior.

Recommendation:

- Prepare after Phase-6 issue is accepted; implement either before or immediately after Phase-6 first slice.

### P2: Billing MVP Planning

Why:

- Commercialization needs billing, but Workflow should come first so usage is attributable to workflow/step/employee.

Problem solved:

- Turns usage_event into commercial accounting foundation.

Risk if not done:

- Commercial readiness remains incomplete.

Dependencies:

- Admin Platform ownership.
- May require billing_event, plan/quota/invoice contract.

Recommendation:

- Admin can research in parallel; Workspace should not implement Billing now.

### P3: Capability Marketplace

Why:

- Marketplace is useful after official and tenant_private capability models prove stable.

Problem solved:

- Enables cross-tenant reusable capabilities and templates.

Risk if done too early:

- Governance, billing, security, and quality boundaries may become chaotic.

Dependencies:

- Billing.
- Capability governance.
- Mature capability templates.
- Workflow template maturity.

Recommendation:

- Keep deferred to Phase-7 or later.

## 8. Phase-6 Issue And Contract Outputs

- Phase-6 issue: `issues/phase6_workflow_mvp.md`
- Workflow runtime contract: `docs/contracts/workflow-runtime-contract.md`

## 9. Development Recommendation

Recommendation: enter Phase-6 Workflow MVP after 产品规划席 / 总控决策席 acceptance of `issues/phase6_workflow_mvp.md` and `docs/contracts/workflow-runtime-contract.md`.

Phase-6 should start with a bounded first slice:

1. Workflow runtime schema and read/write APIs.
2. Official Software R&D sequential workflow template.
3. `run-next-step` backend execution using assigned employee capability binding.
4. Minimal Workspace workflow status UI.
5. usage_event and audit_event attribution.

No Workflow code should be implemented until the Phase-6 issue is accepted.

## 10. Verification

This phase is documentation / contract / issue preparation only.

Executed checks:

- `cd backend && .venv/bin/python -m unittest discover tests`
  - Result: `Ran 310 tests ... OK`
- `cd frontend && node --test app/taskViewModel.test.mjs`
  - Result: `tests 30`, `pass 30`, `fail 0`
- `cd frontend && npm run lint`
  - Result: pass
- `cd frontend && npm run build`
  - Result: compiled successfully
- `git diff --check -- docs/release/phase55-post-g2-roadmap-review.md docs/contracts/workflow-runtime-contract.md issues/phase6_workflow_mvp.md knowledge/CURRENT_CONTEXT.md`
  - Result: pass
- Workspace runtime `/api/platform/*` scan over frontend and backend runtime files
  - Result: pass
- scoped secret scan over the new roadmap / contract / issue / context files
  - Result: pass
