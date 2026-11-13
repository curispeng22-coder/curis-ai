# Workspace Commercial Readiness

Status: Phase-8.5 Commercial Readiness Support

Owner: Workspace supplies commercial data evidence. Admin owns Plan, Quota, Usage, Billing Event, Invoice, payment, and future pricing logic.

## Product Progress

Curis Workspace can now support Admin commercial readiness with redacted usage metering, package composition evidence, and AI employee seat-count evidence without implementing charging.

## Scope

This document checks Workspace-side commercial data readiness only.

It does not approve or implement:

- Billing or charging.
- Payment.
- Invoice generation.
- Billing UI.
- Billing Event generation.
- Workflow changes.
- Credential Vault changes.
- Employee Runtime changes.
- Task Execution chain changes.
- Workspace runtime calls to `/api/platform/*`.

## 1. Usage Event Commercial Field Check

Workspace currently supports the required commercial usage fields through `usage_event` projection and the Phase-8 Usage Meter support.

| Field | Status | Source / Evidence | Notes |
| --- | --- | --- | --- |
| `tenant_id` | Supported | `EvolutionEventLog.list_usage_events()` and `_usage_event_from_row()` | Required for tenant-scoped Admin aggregation. |
| `employee_id` | Supported | `ResultStore._record_usage_events()` and Workflow Runtime step usage | Empty only when a task was executed before employee selection existed or no EmployeeInstance is selected. |
| `workflow_run_id` | Supported | Workflow Runtime step execution and usage_event projection | Empty for direct task execution outside Workflow. |
| `workflow_step_id` | Supported | Workflow Runtime step execution and usage_event projection | Empty for direct task execution outside Workflow. |
| `capability_id` | Supported | `capability_id` / `scope_ref` projection | Records model/tool/task capability id. |
| `capability_source` | Supported | `official` / `tenant_private` usage attribution | `marketplace` is contract-reserved but not enabled. |
| `model_name` | Supported | Model Gateway Adapter usage result | Required for model usage billing analysis. |
| `token_usage` | Supported | Phase-8 additive usage_event metadata | Contains prompt/completion/total token counts. |
| `cost_metadata` | Supported | Phase-8 additive usage_event metadata | Contains estimated cost metadata; not authoritative billing. |

Commercial meaning:

- Workspace can answer "who consumed what capability, in which tenant, task, workflow, step, employee, and model".
- Workspace can provide token and estimated cost evidence.
- Workspace cannot and should not decide invoiceable amount.

Known data limits:

- `estimated_cost` is an estimate, not settlement-grade billing cost.
- Direct task execution can have empty `workflow_run_id` and `workflow_step_id`.
- Historical usage events before Phase-4/6/8 may have empty employee/workflow/token metadata.
- `marketplace` source remains contract-reserved only.

Need new fields now:

- No required new Workspace fields for Phase-8.5.

Future candidate fields:

- `billing_period_hint` if Admin wants Workspace to pre-label periods. Recommendation: do not add now; Admin should derive periods.
- `usage_meter_version` if Billing aggregation semantics change. Recommendation: reserve only.

## 2. Capability Package Support Check

Future Capability Package contract requires packages to bind:

- tools,
- connectors,
- workflows,
- employee templates.

Workspace support status:

| Package Component | Workspace Data Exists | Source / Evidence | Readiness |
| --- | --- | --- | --- |
| tools | Yes | official tools registry, official capability catalog, tenant_private tools | Ready for package reference by id. |
| connectors | Yes | official connector catalog projection, tenant_private connectors | Ready for package reference by id; connector execution remains limited by approved capabilities. |
| workflows | Yes | `workflow_templates` table and official Software R&D SOP template | Ready for package reference by workflow template id. |
| employee templates | Yes | `employee_templates` table and six official R&D templates | Ready for package reference by employee template id. |

Boundary:

- Workspace can support package composition by stable ids.
- Workspace should not implement package purchase, package install, package enforcement, package pricing, or marketplace review.
- Admin may use Workspace ids as package references after a future package-governance gate.
- `tenant_private` package composition must remain tenant-scoped and must not pollute official catalog.

Need new fields now:

- No required new Workspace fields for package support.

Future candidate fields:

- `package_id` on template/capability install records if package installation is approved later.
- `package_source` only if Workspace needs to display package provenance.
- `package_version` if Admin supports package versioning.

## 3. Employee Seat Data Check

AI Employee seat counting requires:

- active employees,
- employee type,
- tenant ownership.

Workspace support status:

| Seat Requirement | Status | Source / Evidence | Notes |
| --- | --- | --- | --- |
| active employees | Supported | `employee_instances.enabled` and `employee_instances.status` | Count `enabled = 1` and non-disabled status. |
| employee type | Partially supported | `employee_instances.role` and `employee_templates.role` | Current type is role-based. Commercial `standard/professional/advanced` is not stored yet. |
| tenant ownership | Supported | `employee_instances.tenant_id` | Tenant isolation is already enforced in EmployeeTemplateContract reads. |
| template lineage | Supported | `employee_instances.template_id` | Lets Admin map employee instance to official or future private template. |
| department ownership | Supported | `employee_instances.department_id` | Supports future departmental commercial analysis. |

Commercial seat-count recommendation:

- Phase-8.5 can count seats as active EmployeeInstances per tenant.
- First billing-readiness metric should be `active_employee_count`.
- `employee_type` should map from role/template in the short term:
  - all current R&D employees = `standard` unless a future Employee Seat gate adds explicit type.
- Do not modify Employee Runtime for seat counting.

Need new fields now:

- No required new runtime fields.

Future candidate fields:

- `employee_type`: `standard` / `professional` / `advanced`.
- `seat_type`: `included` / `additional` / `trial` / `reserved`.
- `plan_binding`: future Admin plan/subscription reference.

These future fields belong in the Employee Seat commercial layer, not in current Employee Runtime unless a separate gate approves it.

## 4. Workspace Commercial Metering Support

Workspace currently supports these commercial measurement families:

| Measurement Family | Current Workspace Support | Billing Readiness |
| --- | --- | --- |
| Token usage | `prompt_tokens`, `completion_tokens`, `total_tokens`, `token_usage` | Ready as usage evidence. |
| Model usage | `model_gateway_id`, `model_name`, capability attribution | Ready as usage evidence. |
| Capability usage | `capability_source`, `capability_type`, `capability_id` | Ready for source/type/id aggregation. |
| Workflow usage | `workflow_run_id`, `workflow_step_id`, WorkflowRun records | Ready for sequential Workflow MVP. |
| Employee usage | `employee_id`, `employee_role`, EmployeeInstance records | Ready for active employee and execution attribution. |
| Credential attribution | `credential_id`, `credential_ref_digest` | Ready as redacted attribution only. |
| Value evidence | Value Event contract exists | Contract-ready; not Billing input yet. |

Workspace does not support:

- authoritative cost settlement,
- invoice amounts,
- plan enforcement,
- quota blocking,
- marketplace revenue share,
- value-based charging,
- package purchase/install/enforcement,
- payment status.

## 5. Missing Data And Field Decision

No immediate Workspace schema change is required for Phase-8.5.

Missing or partial data:

| Gap | Impact | Recommendation |
| --- | --- | --- |
| Explicit commercial `employee_type` | Admin cannot distinguish standard/pro/advanced seats directly from Workspace runtime state. | Keep role/template mapping now; add only under Employee Seat gate. |
| Package install/source/version records | Admin cannot know which package caused a capability/template to be available. | Reserve for future Capability Package gate; no runtime change now. |
| Billing period on usage_event | Admin must derive billing periods from timestamps. | Keep Admin-derived; do not add to usage_event now. |
| Authoritative cost | `estimated_cost` cannot produce invoices. | Admin BillingEvent must rate usage independently. |
| Marketplace source execution | Marketplace billing cannot be validated from live runtime yet. | Keep deferred until Marketplace gate. |

## 6. Admin / Workspace Boundary

Workspace produces:

- Usage Event.
- Value Event contract evidence after its own gate.
- EmployeeInstance and WorkflowRun operational state.
- Capability binding and usage attribution.

Admin handles:

- Plan.
- Quota.
- Usage aggregation ownership for billing views.
- Billing Event.
- Invoice.
- Payment.
- Marketplace governance and revenue share.

Boundary rule:

- Workspace must not call `/api/platform/*` at runtime.
- Admin must not read tenant_private plaintext credentials.
- Billing must not change Workflow Runtime, Credential Vault, Employee Runtime, or Task Execution chain.

## 7. Readiness Conclusion

Workspace is commercially ready for Admin-side Phase-8.5 support and future Billing MVP integration at the evidence layer.

Ready now:

- Usage Event commercial fields.
- Usage Meter aggregation.
- Capability Package reference basis.
- Employee Seat count basis.
- Tenant-scoped commercial attribution.

Not ready without future gates:

- explicit employee seat type enforcement,
- package purchase/install/enforcement,
- marketplace monetization,
- authoritative BillingEvent rating,
- invoice/payment,
- value-based pricing.

Recommendation:

- Do not add Workspace fields in Phase-8.5.
- Let Admin derive Billing and quota metrics from existing usage/event/employee/workflow evidence.
- Open a future gate only if Admin Billing MVP needs explicit `employee_type`, `package_id`, or package versioning fields.
