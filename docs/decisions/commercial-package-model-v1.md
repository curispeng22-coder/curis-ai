# Commercial Package Model v1

Status: Frozen for first commercial package model

Date: 2026-07-09

Owner: 总控决策席 owns package freeze decisions. Admin Platform owns future Plan, Quota, BillingEvent, Invoice, payment, and package governance. Workspace supplies usage/value evidence and tenant-private capability execution data only through approved contracts.

## Product Progress

Curis now has a frozen first-version commercial package model: Free / Pro / Enterprise, built on subscription base, token usage, capability packages, AI employee seats, and future value pricing.

## Decision

Freeze Curis first commercial package model as a Hybrid three-tier package system:

1. Subscription Plan as the customer-facing base.
2. Token Usage as the primary metered usage dimension.
3. Capability Package as the differentiation dimension.
4. AI Employee Seat as the Curis-native seat dimension.
5. Future Value-based Pricing as a reserved L6 option only.

The first customer-facing packages are:

- Free
- Pro
- Enterprise

This freezes the model shape and package semantics. It does not freeze final real-world prices, payment rules, invoice rules, tax rules, marketplace revenue share, or value-based charging.

## Frozen Package Matrix

| Dimension | Free | Pro | Enterprise |
| --- | --- | --- | --- |
| Product role | Trial and onboarding package. | Main self-serve paid package. | Sales-led governed package. |
| Target user | Evaluator / solo founder validating AI company workflow. | Solo entrepreneur or small operator running practical AI company work. | Team / company customer needing governance, scale, support, or deployment control. |
| Subscription price | `$XX` placeholder. | `$XX` placeholder. | `$XX` / negotiated placeholder. |
| AI employee seats | Limited R&D seats, default ceiling 3. | Full R&D working set, default ceiling 15. | Custom / unlimited by contract. |
| Token quota | Low included quota, default 1M monthly tokens. | Production-like quota, default 50M monthly tokens. | Custom / unlimited by contract. |
| Workflow quota | Demo-level workflow runs, default 5,000 monthly runs. | Self-serve workflow runs, default 50,000 monthly runs. | Custom / unlimited by contract. |
| Capability package | Official starter package. | Official standard package. | Full official package plus governed future options. |
| tenant_private capability | Disabled or tightly limited. | Enabled. | Enabled with governance. |
| Credential Vault | Limited/local/demo or restricted. | Enabled within approved Credential Vault boundary. | Production Vault/KMS required before hosted customer secrets. |
| Marketplace | Not included. | Future optional only after G3. | Future governed option only after G3. |
| Value Event | Basic visibility / validation evidence. | Commercial validation evidence. | Advanced analytics / value-pricing experiments after future gate. |
| Overage | Not default; upgrade path preferred. | Token/seat/workflow overage-ready. | Contracted. |

## Frozen Billing Dimensions

### Subscription Plan

Meaning:

- The customer buys access to a Curis AI company workspace tier.
- Plan is the anchor for features, quotas, packages, and included seats.

Frozen tiers:

- `free`
- `pro`
- `enterprise`

Implementation owner:

- Admin Platform.

Workspace role:

- Read approved plan/package visibility only when future gates require it.
- Continue producing usage and value evidence.

### Token Usage

Meaning:

- Primary metered usage dimension.
- Based on Workspace `usage_event` token fields and Usage Meter aggregation.

Frozen rule:

- `total_tokens` is the first billing-readiness basis.
- `estimated_cost` is not authoritative billing amount.
- Admin-owned BillingEvent must rate usage independently.

### Capability Package

Meaning:

- Commercial grouping of tools, connectors, workflow templates, and employee templates.

Frozen package components:

- tools
- connectors
- workflows
- employee templates

Frozen source rules:

- `official`: Admin-governed.
- `tenant_private`: Workspace/CEO-owned, tenant-scoped, not official.
- `marketplace`: future-gated, not active in v1.

### AI Employee Seat

Meaning:

- Curis-native seat dimension based on AI EmployeeInstance.

Frozen first interpretation:

- Seat counting starts from active employee instances per tenant.
- Current R&D employees are treated as `standard` until a future Employee Seat gate adds explicit `standard/professional/advanced` fields.

Not frozen now:

- Real seat overage enforcement.
- New commercial employee types in Workspace runtime.

### Future Value-based Pricing

Meaning:

- Long-term value/ROI monetization option based on validated Value Event evidence.

Frozen rule:

- Not active in first commercial package model.
- Value Event remains validation evidence only.
- AI must not self-declare invoiceable value.

## Package To Contract Mapping

| Package Layer | Source Contract |
| --- | --- |
| Plan / tier shape | `docs/contracts/pricing-contract.md` |
| Billing domain objects | `docs/contracts/billing-domain-contract.md` |
| Capability Package | `docs/contracts/capability-package-contract.md` and `docs/contracts/pricing-package-contract.md` |
| Quota / overage semantics | `docs/contracts/quota-rule-contract.md` |
| Employee Seat | `docs/contracts/employee-seat-contract.md` |
| Commercial data flow | `docs/contracts/commercial-data-flow.md` |
| Usage / Value boundary | `docs/contracts/usage-value-event-boundary.md` |
| Workspace commercial evidence | `docs/research/domain/workspace-commercial-readiness.md` |

## Admin / Workspace Boundary

Admin owns:

- Plan.
- Quota.
- Billing Event.
- Invoice.
- Payment.
- Official capability packages.
- Marketplace governance in future gates.

Workspace owns:

- Task / Workflow / Employee execution.
- Usage Event evidence.
- Value Event contract evidence after approved implementation gate.
- tenant_private capability configuration and execution.
- Credential Vault boundary for tenant-private credentials.

Boundary rules:

- Workspace runtime must not call `/api/platform/*`.
- Workspace must not generate BillingEvent.
- Workspace must not generate Invoice.
- Admin must not read tenant_private plaintext credentials.
- Admin must not modify Workspace Employee Runtime, Workflow Runtime, Credential Vault, or Task Execution chain through package model decisions.

## Not Approved By This Freeze

- Billing implementation.
- Payment.
- Invoice generation or invoice UI.
- Automatic charging or automatic deduction.
- ROI system.
- Marketplace implementation or revenue share.
- Value-based charging.
- Usage Event structure change.
- Workflow Runtime change.
- Employee Runtime change.
- Credential Vault change.
- Workspace execution-chain change.
- Admin runtime change unless separately approved.

## Open Decisions

These remain future decisions:

- Final real-world prices for Free / Pro / Enterprise.
- Exact Pro overage unit prices.
- Whether Free allows any tenant_private capability.
- Whether Enterprise quotas use `0 = unlimited` or explicit contracted limits in implementation.
- When explicit `employee_type` and `seat_type` become first-class fields.
- When package versioning and package install records enter implementation.

## Freeze Conclusion

Curis first commercial package model is frozen as:

```text
Free -> Pro -> Enterprise
  + subscription base
  + token usage
  + capability packages
  + AI employee seats
  + future value pricing reserve
```

This model is ready to guide Admin Billing and commercial package implementation gates. It is not a Billing/payment implementation approval.
