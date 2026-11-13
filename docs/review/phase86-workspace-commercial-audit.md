# Phase 8.6 Workspace Commercial Configuration Audit

Status: Completed

Date: 2026-07-09

Owner: Workspace line. Admin Platform owns future commercial configuration, plan, quota, package, billing, and marketplace governance.

## Product Progress

Curis Workspace can now provide commercial metering evidence for employees, workflows, capabilities, models, tokens, and redacted cost metadata, while commercial rules remain outside the Workspace runtime.

## Scope

This is an audit-only review. It scans whether Workspace contains commercial-facing rules that should eventually be controlled by Admin Commercial Configuration instead of remaining hardcoded in Workspace code.

This phase does not modify:

- Task Execution.
- Workflow Runtime.
- Employee Runtime.
- Credential Vault.
- Billing.
- Admin Platform governance.
- Marketplace.
- ROI.

## Summary Decision

Workspace currently has enough commercial data for Admin-side metering readiness, but several official defaults are still embedded in Workspace code because they were introduced as Phase-4 / Phase-6 MVP scaffolding.

The hardcoded items are acceptable for the local demo and MVP, but should be migrated to Admin-controlled commercial configuration before production package enforcement:

- official R&D employee template availability,
- official R&D SOP workflow template availability,
- capability package composition,
- plan-level feature flags and quotas,
- AI employee seat type / seat limit semantics,
- marketplace source enablement.

Workspace should keep tenant-owned operational state and runtime execution boundaries:

- tenant_private capability definitions,
- credential_ref binding and resolver usage,
- EmployeeInstance / WorkflowRun runtime records,
- usage_event / audit_event generation,
- task and workflow execution.

## 1. Current Workspace Commercial-Related Data

Workspace already produces or stores the following commercial evidence.

| Area | Current Data | Commercial Use |
| --- | --- | --- |
| Tenant | `tenant_id` on tasks, usage events, employees, departments, workflows, credentials, and tenant_private capabilities | Tenant-scoped billing and isolation. |
| Employee | EmployeeTemplate, EmployeeInstance, role, status, enabled, department/template lineage | AI employee seat count and employee-attributed usage. |
| Workflow | WorkflowTemplate, WorkflowInstance, WorkflowRun, WorkflowStep, StepAssignment, StepResult | Workflow run count, step count, and SOP usage analysis. |
| Capability | official catalog projection plus tenant_private model/tool/connector records | Capability package reference, source attribution, tenant-private self-extension. |
| Model | model gateway id, model name, model preference, model-call token metadata | Token/model usage metering. |
| Usage | usage.model_call, usage.tool_call, usage.task_execution events | Admin Billing input evidence, not invoice authority. |
| Audit | workflow and credential audit events | Operational traceability and security review. |
| Credential | credential metadata, credential_ref digest, credential_id | Redacted credential attribution without exposing secrets. |

Commercial boundary:

- Workspace supplies evidence.
- Admin interprets evidence into plan/quota/package/billing decisions.
- `estimated_cost` remains non-authoritative and must not become an invoice amount inside Workspace.

## 2. Employee Audit

### Already Configurable In Workspace

- CEO can create tenant-scoped EmployeeInstance records from available templates.
- CEO can enable/disable employees and set status.
- CEO can add `instructions_override`.
- CEO can bind official or tenant_private capabilities to an employee.
- Usage events can attribute execution to `employee_id`, `employee_role`, and `employee_name`.
- Active employee count can be inferred from tenant-owned EmployeeInstance records.

### Currently Hardcoded Or MVP-Scoped

| Rule | Current Location / Evidence | Audit Finding |
| --- | --- | --- |
| Six official R&D employee templates: Tech Lead, Product Manager, Architect, Frontend Engineer, Backend Engineer, QA Engineer | Seeded in `Database._seed_employee_template_contract()` | Should become Admin official template supply / package configuration later. |
| Default employee fallback is Tech Lead | `EmployeeTemplateContract.default_employee_for_task()` | Should become configurable default-role policy later. |
| Phase-4 department restriction to `software_rnd` | `create_department_instance()` rejects other department types | Acceptable MVP scope; future department package availability belongs to Admin configuration. |
| Employee status enum `idle`, `assigned`, `disabled` | `create_employee_instance()` validation | Runtime status can stay Workspace-owned; commercial seat status may need separate Admin contract. |
| Employee binding sources limited to `official` and `tenant_private` | `_normalize_binding()` | Marketplace remains future-gated and should be enabled by Admin governance only. |
| Employee binding capability types limited to `model`, `tool`, `connector` | `_normalize_binding()` | Reasonable runtime allowlist; package-level capability families should be Admin-configured. |

### Should Migrate To Admin Commercial Configuration

- Which official employee templates are available per plan.
- Which employee templates are included in Free / Pro / Enterprise.
- AI employee seat limits per plan.
- Future employee seat type: `standard`, `professional`, `advanced`.
- Future official employee template packages.
- Future marketplace employee templates.

### Should Stay Workspace Internal

- EmployeeInstance creation and tenant ownership.
- Employee instructions override.
- Employee capability binding to tenant-owned or official capabilities.
- Employee runtime status used by execution.
- Employee usage attribution in usage_event.

## 3. Workflow Audit

### Already Configurable In Workspace

- Workspace can list workflow templates available to the tenant.
- CEO can create WorkflowRun records from the official Software R&D SOP template.
- WorkflowRun, WorkflowStep, StepAssignment, and StepResult are tenant-scoped runtime records.
- Workflow usage can be attributed by `workflow_run_id` and `workflow_step_id`.

### Currently Hardcoded Or MVP-Scoped

| Rule | Current Location / Evidence | Audit Finding |
| --- | --- | --- |
| Official Software R&D SOP step list | `Database._seed_workflow_runtime_contract()` | Should become Admin official workflow template supply later. |
| Seven ordered roles/steps | Workflow seed JSON | Acceptable demo/MVP scaffold; plan/package availability should not remain hardcoded. |
| Only `source = official` is accepted when creating a WorkflowRun | `WorkflowRuntime.create_run()` | Tenant-private templates are listed but not executable; future enablement needs gate and Admin/package boundary review. |
| Only `process_type = sequential` is supported | `WorkflowRuntime.create_run()` | Correct MVP boundary; complex DAG should remain future-gated. |
| Only `department_type = software_rnd` is supported | `WorkflowRuntime.create_run()` | Correct MVP boundary; future departments should be Admin-configured official templates plus Workspace tenant instances. |
| Employee assignment chooses first enabled employee matching role | `_find_employee_for_step()` | Runtime policy is simple and hardcoded; future routing policy could be configurable but should not be commercial gating logic in Workspace. |

### Should Migrate To Admin Commercial Configuration

- Official workflow template catalog and package membership.
- Which plans can access which workflow templates.
- Workflow run quotas per plan.
- Future workflow package composition.
- Future marketplace workflow template governance.

### Should Stay Workspace Internal

- WorkflowRun runtime state.
- Step execution order for a selected template version.
- StepAssignment and StepResult records.
- usage_event / audit_event attribution for workflow runtime.
- Tenant isolation for WorkflowRun and tenant_private workflow data.

## 4. Capability Audit

### Already Configurable In Workspace

- official capabilities are read through `/api/catalog/*`.
- tenant_private model/tool/connector metadata is managed through Workspace APIs.
- tenant_private capability visibility is tenant-scoped.
- Capability selector merges official and tenant_private options while preserving `source`.
- Private capabilities can bind credential_ref through Credential Vault.
- Usage events record capability source/type/id.

### Currently Hardcoded Or MVP-Scoped

| Rule | Current Location / Evidence | Audit Finding |
| --- | --- | --- |
| official tool catalog is based on the Workspace registry | `/api/catalog/tools` returns registered runtime tools as `source=official` | Future official tool/package availability should come from Admin catalog/config; runtime tool registry can stay Workspace execution infrastructure. |
| official model/connector catalog projections are read-only metadata | `/api/catalog/models`, `/api/catalog/capabilities`, `/api/catalog/connectors` | Correct boundary; Admin owns official definitions. |
| tenant_private capability types are model/tool/connector only | private capability endpoints and binding validation | Correct MVP boundary; future capability package types need contract gate. |
| capability package dependencies are not enforced | Package support is reference-ready only | Correct: package purchase/install/enforcement belongs to Admin Commercial Configuration. |
| marketplace source is contract-reserved but not executable | binding validation excludes marketplace | Correct until marketplace governance gate. |

### Should Migrate To Admin Commercial Configuration

- official capability package composition.
- plan-based access to official models/tools/connectors.
- capability package install/enforcement.
- marketplace enablement and review status.
- future connector/package quotas.
- official capability versioning.

### Should Stay Workspace Internal

- tenant_private capability definitions.
- credential_ref binding to tenant_private capabilities.
- runtime capability selection for task/workflow execution.
- capability usage attribution.
- Credential Vault resolver boundary.

## 5. Usage Audit

### Workspace Provides

Workspace already supports commercial usage evidence for:

- employee usage: `employee_id`, `employee_role`, `employee_name`,
- workflow usage: `workflow_run_id`, `workflow_step_id`,
- capability usage: `capability_source`, `capability_type`, `capability_id`,
- model usage: `model_gateway_id`, `model_name`,
- token usage: `prompt_tokens`, `completion_tokens`, `total_tokens`, `token_usage`,
- cost metadata: `estimated_cost`, `currency`, `cost_source`, `raw_meter_value`,
- credential attribution: `credential_id`, `credential_ref_digest`.

`UsageMeterService` provides read-only aggregation by:

- totals,
- capability source,
- capability type,
- model,
- employee,
- workflow.

### Usage Limits

- Usage Event is evidence, not billing.
- Usage Meter is aggregation, not charging.
- `estimated_cost` is non-authoritative.
- Billing periods should be derived by Admin from timestamps, not written by Workspace.
- Historical events may lack newer fields if created before employee/workflow/commercial support.

### Should Migrate To Admin Commercial Configuration

- Plan quota limits.
- Billing period logic.
- Overage pricing.
- BillingEvent generation.
- Invoice line-item logic.
- package quota enforcement.

### Should Stay Workspace Internal

- UsageEvent creation after execution.
- Redaction and no-secret guards.
- Usage attribution to tenant/task/workflow/step/employee/capability.
- Read-only usage evidence projection.

## 6. Already Configured Versus Not Configured

### Already Configured Or Tenant-Configurable

- tenant_private model/tool/connector metadata.
- tenant_private credential_ref binding.
- EmployeeInstance creation and capability binding.
- DepartmentInstance creation for current R&D scope.
- WorkflowRun runtime records.
- Tenant model preference.
- Usage Meter query filters.

### Not Configured Yet

- plan-based feature availability.
- plan-based quotas.
- Free / Pro / Enterprise package enforcement.
- employee seat type and seat limit enforcement.
- official workflow template availability by package.
- official employee template availability by package.
- capability package install/enforcement.
- marketplace source enablement.
- package versioning / install records.

## 7. Should Move To Admin

Move later, under separate gate:

1. Commercial package and plan rules.
2. Quota limits for tokens, workflow runs, employee seats, private capabilities, connectors, and credentials.
3. official EmployeeTemplate catalog supply and plan availability.
4. official WorkflowTemplate catalog supply and plan availability.
5. official Capability Package composition.
6. Marketplace source enablement and review workflow.
7. BillingEvent / Invoice generation.
8. Plan-specific `tenant_private` availability and limits.

Migration note:

- Migration should be additive. Do not remove Workspace runtime records.
- Admin should publish commercial configuration through approved read-only contracts.
- Workspace should consume only approved configuration snapshots if a future gate requires runtime enforcement.

## 8. Should Stay Workspace Internal

Keep in Workspace:

1. Tenant private capability metadata and credential_ref binding.
2. Credential Vault resolver and secret boundary.
3. Task, WorkflowRun, WorkflowStep, StepAssignment, StepResult runtime state.
4. EmployeeInstance tenant-local configuration.
5. EmployeeCapabilityBinding runtime selection.
6. usage_event and audit_event creation/redaction.
7. Runtime execution through Model Gateway Adapter and Tool Executor.
8. Tenant isolation enforcement for operational data.

Reason:

- These are execution and tenant-owned operational concerns.
- Moving them to Admin would blur the Admin / Workspace boundary and increase secret/data-handling risk.

## 9. Field Gap Assessment

No Workspace field change is required in Phase-8.6.

Future fields to consider only after Admin Commercial Configuration gate:

| Candidate Field | Possible Owner | Reason |
| --- | --- | --- |
| `employee_type` | Commercial / Admin contract, optionally mirrored in Workspace | Distinguish standard/professional/advanced AI employee seats. |
| `seat_type` | Commercial / Admin contract | Included/additional/trial seat semantics. |
| `plan_binding` | Admin billing domain | Link tenant or seat to subscription plan. |
| `package_id` | Admin package domain, optional Workspace display snapshot | Trace which package made a template/capability available. |
| `package_version` | Admin package domain | Support package upgrades and auditability. |
| `commercial_config_version` | Admin config snapshot | Audit which plan/package config governed a run. |
| `marketplace_status` | Admin marketplace governance | Enable marketplace without polluting official catalog. |

Recommendation:

- Do not add these fields now.
- Define them first in Admin/Workspace shared commercial configuration contract.
- Only mirror into Workspace when runtime enforcement or display requires it.

## 10. Risk Assessment

| Risk | Severity | Current Mitigation | Future Action |
| --- | --- | --- | --- |
| MVP official templates remain hardcoded in Workspace | Medium | Bounded to demo/MVP and documented here | Move official template availability to Admin configuration. |
| Commercial package enforcement not present | Medium | No Billing or enforcement is approved yet | Implement after Admin Commercial Configuration and Billing gates. |
| Marketplace source is contract-reserved but not runtime-enabled | Low | Binding validation excludes marketplace | Keep deferred until governance gate. |
| Employee seat type is inferred from role/template | Medium | Active employee count is available | Add seat contract fields only under future gate. |
| Estimated cost could be mistaken for invoice amount | Medium | Docs state non-authoritative status | Admin BillingEvent must rate usage independently. |

## 11. Conclusion

Phase-8.6 audit conclusion:

- Workspace commercial data support is sufficient for Admin-side commercial configuration planning.
- Workspace has several MVP hardcoded defaults that should become Admin-supplied official configuration before production commercialization.
- No immediate Workspace runtime or schema change is required.
- Do not modify Workflow Runtime, Employee Runtime, Credential Vault, or Task Execution for this audit.
- Next recommended step is an Admin-owned Commercial Configuration Contract gate, with Workspace compatibility review before any runtime enforcement.

Handoff: final closeout.
