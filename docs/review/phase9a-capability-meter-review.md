# Phase 9A Capability Package Meter Review

Status: Completed

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace can now provide capability, employee, workflow, model, token, and redacted cost evidence for future Admin capability package quotas without implementing package pricing or billing.

## Scope

This review checks whether Workspace can provide the usage evidence needed for future Capability Package metering.

This phase does not modify:

- capability execution,
- workflow execution,
- employee runtime,
- Credential Vault,
- Admin package configuration,
- BillingEvent generation.

## Evidence Sources

| Evidence | Current Source |
| --- | --- |
| Official capability metadata | `/api/catalog/*` projections |
| Tenant-private capability metadata | `tenant_private_capabilities` table and Workspace private capability APIs |
| Capability selection | unified Workspace capability selector |
| Capability execution attribution | `usage_event.capability_source`, `usage_event.capability_type`, `usage_event.capability_id` |
| Employee attribution | `usage_event.employee_id`, `usage_event.employee_role` |
| Workflow attribution | `usage_event.workflow_run_id`, `usage_event.workflow_step_id` |
| Token / cost evidence | `prompt_tokens`, `completion_tokens`, `total_tokens`, `token_usage`, `estimated_cost`, `cost_metadata` |
| Read-only aggregation | `UsageMeterService` totals, by capability source, by capability type, by model, by employee, by workflow |

## Meter Capability Check

| Requirement | Result | Notes |
| --- | --- | --- |
| capability usage | Supported | Usage events carry capability source/type/id. |
| connector usage | Metadata supported; execution usage is future-limited | Connector capability records can be selected/bound; connector execution metering should rely on usage_event once connector execution is enabled. |
| workflow usage | Supported | Workflow run and step ids are present in workflow-originated usage events. |
| employee usage | Supported | Usage events carry employee id/role/name and meter aggregation groups by employee. |
| model usage | Supported | Model gateway id, model name, token usage, and cost metadata are present. |
| tenant_private attribution | Supported | Capability source stays `tenant_private`, with tenant-owned visibility in capability refs. |
| package quota evidence | Partially supported | Workspace emits capability-level evidence; Admin must map package membership. |

## Capability Package Quota Support

Workspace can support future package quota checks by producing evidence such as:

```text
tenant_id
capability_source
capability_type
capability_id
workflow_run_id
workflow_step_id
employee_id
model_name
token_usage
cost_metadata
created_at
status
```

Admin can then map those fields against Admin-owned package composition:

```text
package_id
  -> capability_ids
  -> connector_ids
  -> workflow_template_ids
  -> employee_template_ids
```

Workspace should not perform package membership checks, price decisions, or quota blocking in the execution path.

## Current Gaps

| Gap | Impact | Recommendation |
| --- | --- | --- |
| Usage events do not store `package_id` | Admin must derive package usage from its package membership table. | Keep as-is unless Admin requires immutable package-version attribution. |
| No `package_version` in Workspace events | Historical usage cannot prove which package definition was active at execution time. | Add only through shared contract if Admin needs auditable package snapshots. |
| Connector execution metering is not yet first-class | Future connector packages need usage-event writes when real connector execution is enabled. | Gate connector runtime separately; preserve existing usage_event shape. |
| Marketplace source remains mostly reserved | Marketplace package metering cannot be validated end to end yet. | Keep marketplace package metering future-gated. |

## Boundary Decision

Workspace should provide:

- raw execution evidence,
- usage_event and value_event,
- tenant_private capability metadata,
- redacted credential attribution,
- workflow / employee / capability usage joins.

Admin should provide:

- package definitions,
- package pricing,
- package quota rules,
- plan entitlement,
- package install / availability logic,
- BillingEvent generation.

## Shared Contract Need

Shared Contract is needed if Admin wants Workspace to stamp any of these on usage events:

- `package_id`,
- `package_version`,
- `commercial_config_version`,
- `entitlement_snapshot_id`.

No Shared Contract is required for current capability-level usage evidence.

## Conclusion

Workspace is ready to support Admin Capability Package quota development at the evidence layer. Package interpretation and enforcement must remain Admin-owned.
