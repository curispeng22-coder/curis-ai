# Phase 9A Employee Seat Meter Review

Status: Completed

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace can now provide tenant-scoped AI employee seat evidence for future Admin commercial metering without implementing plan, quota, pricing, billing, or invoice logic.

## Scope

This review checks whether Workspace data can support future `employee_seat_usage`.

This phase does not modify:

- Employee Runtime.
- Workflow Runtime.
- Credential Vault.
- Task Execution.
- Admin Platform pricing, quota, package, or billing logic.

## Evidence Sources

| Evidence | Current Source |
| --- | --- |
| Tenant employee records | `employee_instances` table |
| Active employee count | `employee_instances.enabled` plus `employee_instances.status` |
| Employee role / current type proxy | `employee_instances.role` |
| Employee template lineage | `employee_instances.template_id` |
| Employee template source | `employee_templates.source` |
| Employee usage attribution | `usage_event.employee_id`, `usage_event.employee_role`, `usage_event.employee_name` |
| Employee capability binding | `employee_capability_bindings` table |

## Meter Capability Check

| Requirement | Result | Notes |
| --- | --- | --- |
| tenant employee count | Supported | Count `employee_instances` by `tenant_id`. |
| active employee count | Supported | Count employees where `enabled = 1` and `status != disabled`. |
| employee type | Partially supported | Current runtime stores `role`; commercial `employee_type` / `seat_type` is not explicit yet. |
| employee template source | Supported | Join `employee_instances.template_id` to `employee_templates.id` and read `employee_templates.source`. |
| employee usage | Supported | `UsageMeterService` groups usage by `employee_id`, falling back to `employee_role`. |
| tenant isolation | Supported | Employee instance reads are tenant-scoped through `TenantContext.current_tenant_id()`. |

## Recommended Admin Meter Interpretation

Admin can calculate first-version `employee_seat_usage` from Workspace evidence:

```text
employee_seat_usage =
  count(employee_instances)
  where tenant_id = target tenant
  and enabled = 1
  and status != 'disabled'
```

Recommended breakdowns:

- by `role`,
- by `template_id`,
- by joined template `source`,
- by `department_id`,
- by `status`,
- by usage attribution from `usage_event.employee_id`.

## Current Gaps

| Gap | Impact | Recommendation |
| --- | --- | --- |
| No explicit commercial `employee_type` | Admin cannot distinguish standard / professional / advanced seats from Workspace data alone. | Add via shared contract before G2 employee-seat pricing enforcement. |
| No `seat_type` or `plan_binding` in Workspace employee records | Workspace intentionally does not know package or plan entitlement. | Keep Admin-owned; pass only evidence from Workspace. |
| No Workspace quota enforcement | Correct boundary for this phase. | Admin should compute limits; Workspace should not block execution by plan/quota without a future gate. |
| Official template availability is still Workspace-seeded | Acceptable MVP scaffold, but not final commercial control. | Migrate official template supply / package availability to Admin Commercial Configuration later. |

## Boundary Decision

Workspace should continue to own:

- tenant EmployeeInstance records,
- employee runtime status,
- employee capability binding,
- employee usage attribution.

Admin should own:

- plan seat limits,
- employee seat pricing,
- employee type commercial semantics,
- package-level employee template availability,
- BillingEvent generation.

## Shared Contract Need

Shared Contract is needed before Admin enforces AI employee seats by type.

Minimum future fields to define:

- `employee_type`,
- `seat_type`,
- `billable_status`,
- `template_source`,
- `commercial_config_version` if Admin needs versioned package attribution.

No Shared Contract is required for current count-only evidence.

## Conclusion

Workspace can support Admin Billing continuation for count-based AI employee seat metering now. Explicit employee-seat type semantics should remain future shared-contract work.
