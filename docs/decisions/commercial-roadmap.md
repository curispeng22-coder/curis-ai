# Commercial Roadmap

Status: Frozen v1 commercial package roadmap

Decision: Curis commercial model will follow a Hybrid path:

- tiered subscription,
- token/model usage,
- capability packages,
- AI employee seats,
- future value-based pricing.

Package model decision: `docs/decisions/commercial-package-model-v1.md` freezes the first customer-facing package ladder as `Free -> Pro -> Enterprise`. The package model is frozen; final real-world price points, payment, invoice generation, Marketplace revenue share, and value-based charging remain future-gated.

This roadmap is a decision baseline only. It does not approve Billing, payment, invoice generation, ROI, Marketplace, Admin changes, Workspace changes, or execution-chain changes.

## G0: Usage Observation

Goal:

- Observe how tenants use tasks, workflows, employees, capabilities, models, and credentials.

Inputs:

- usage_event
- audit_event
- workflow/employee/capability attribution

Output:

- usage visibility,
- commercial hypotheses,
- quota planning input.

Status:

- Current foundation exists.

Not included:

- charging,
- invoice,
- payment,
- ROI.

## G1: Plans + Model Quota Billing

Goal:

- Introduce plan/quota/rated usage model for model and token usage.

Required contracts:

- `docs/contracts/pricing-contract.md`
- `docs/contracts/billing-domain-contract.md`

Expected objects:

- Plan
- Quota
- BillingEvent

Scope:

- plan tiers,
- token/model usage quota,
- billing-ready aggregation.

Not included:

- payment,
- automatic invoice issuance unless separately approved,
- value-based pricing.

## G2: AI Employee Seats

Goal:

- Add AI employee seat as a pricing dimension.

Inputs:

- EmployeeTemplate
- EmployeeInstance
- EmployeeCapabilityBinding
- usage_event employee attribution

Scope:

- included AI employee count by plan,
- additional AI employee seat reserve,
- role-based seat policy.

Not included:

- employee runtime changes,
- new employees,
- complex HR system.

## G3: Marketplace Revenue Share

Goal:

- Enable future marketplace monetization for official/third-party capability packs or workflow templates.

Prerequisites:

- marketplace governance,
- review and approval workflow,
- billing/revenue-share model,
- capability/template quality standard,
- security review.

Scope:

- marketplace package listing,
- revenue share rules,
- tenant install/use attribution.

Not included now:

- Marketplace implementation,
- payment,
- third-party settlement.

## G4: Value-Based Pricing

Goal:

- Explore pricing based on validated value created by AI employees/workflows.

Inputs:

- Value Event
- usage_event
- billing_event
- user-confirmed value assumptions
- external business metrics in future gates

Scope:

- value analytics,
- value-based plan options,
- outcome/value commercial experiments.

Required guardrail:

- Value Event must remain user-confirmed or externally validated.
- AI must not self-declare invoiceable value.

Not included now:

- ROI system,
- automatic value charging,
- revenue prediction,
- financial settlement.

## Roadmap Order

```text
G0 Usage Observation
  -> G1 Plans + Model Quota Billing
  -> G2 AI Employee Seats
  -> G3 Marketplace Revenue Share
  -> G4 Value-Based Pricing
```

## Current Recommendation

Next commercial development basis:

1. Use G0 to keep observing usage.
2. Prepare G1 Billing MVP only after gate approval.
3. Keep G2/G3/G4 as future-gated commercial layers.

## Forbidden In Phase-7.6

- Billing implementation.
- Payment implementation.
- Invoice generation.
- Usage Event structure change.
- Workspace execution-chain change.
- Admin implementation change.
- New commercial feature implementation.
