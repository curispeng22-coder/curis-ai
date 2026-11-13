# Phase 9A Commercial Boundary Check

Status: Completed

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace can now stay focused on execution and metering evidence while Admin Commercial Configuration owns pricing, quotas, packages, and billing rules.

## Scope

This check confirms the current Admin / Workspace commercial boundary for Phase-9A.

This phase does not implement:

- Billing,
- Pricing,
- Quota enforcement,
- Payment,
- Invoice,
- package purchase or entitlement enforcement.

## Workspace Responsibility

Workspace owns operational execution and evidence generation:

- Task Execution.
- AI Employee Runtime.
- Workflow Runtime.
- Credential Vault resolver usage.
- tenant_private model / tool / connector metadata.
- employee capability binding.
- usage_event generation.
- value_event generation.
- audit_event generation.
- Usage Meter read-only aggregation.

Workspace data should answer:

```text
What happened?
Who/which employee executed it?
Which workflow/step did it belong to?
Which capability was used?
How many tokens/resources were consumed?
What value was user-confirmed?
Was sensitive attribution redacted?
```

## Admin Responsibility

Admin owns commercial interpretation and governance:

- Pricing.
- Plan.
- Quota.
- Capability Package.
- Billing rules.
- BillingEvent generation.
- Invoice / payment in future phases.
- Official commercial configuration.
- Marketplace governance in future phases.

Admin data should answer:

```text
What is the tenant allowed to use?
Which package/plan applies?
How should usage be rated?
Which quota applies?
Which billing event should be generated?
Which invoice line may be created in a future phase?
```

## Boundary Rules

| Rule | Current Result |
| --- | --- |
| Workspace produces Usage Event and Value Event only | Pass |
| Admin produces Pricing / Quota / Package / Billing rules | Pass |
| Workspace does not call `/api/platform/*` from runtime UI / execution | Pass based on current runtime scan scope |
| Workspace does not generate BillingEvent | Pass |
| Workspace does not calculate invoice or payment | Pass |
| Workspace does not decide plan entitlement | Pass |
| Workspace does not expose tenant_private plaintext credentials to Admin | Pass |
| Admin observes redacted usage/audit attribution only | Pass |

## Commercial Data Flow

Current intended data flow:

```text
Workspace Execution
  -> Usage Event / Value Event / Audit Event
  -> Usage Meter read model
  -> Admin Commercial Configuration
  -> Admin Billing interpretation
```

Forbidden direction:

```text
Workspace Runtime
  -> /api/platform/*
  -> plan / quota / pricing decision
  -> execution blocking
```

The forbidden direction remains blocked unless a future shared contract and gate explicitly approve it.

## Current Boundary Risk

| Risk | Severity | Notes |
| --- | --- | --- |
| Shared database files contain Admin commercial tables and Workspace runtime tables together | Medium | This can make code-review scope noisy even when runtime boundaries are intact. |
| Future package enforcement may tempt Workspace to read Admin quota tables directly | Medium | Must require a shared contract before any execution-path enforcement. |
| `estimated_cost` may be mistaken for invoice authority | Medium | It must remain non-authoritative evidence only. |
| Employee seat semantics are not explicit yet | Low now, Medium before monetization | Count-only metering works; typed commercial seat billing needs contract. |

## Shared Contract Need

Shared Contract is not required for the current audit-only state.

Shared Contract is required before any of the following:

- Workspace stamps `package_id` or commercial config snapshots on events.
- Workspace blocks or alters execution based on quota.
- Workspace reads Admin plan/quota/price configuration at runtime.
- Admin calculates employee-seat usage by commercial seat type.
- Marketplace package usage enters billing.

## Conclusion

The Phase-9A boundary is intact: Workspace can supply execution evidence, while Admin remains responsible for pricing, quotas, packages, and billing rules.
