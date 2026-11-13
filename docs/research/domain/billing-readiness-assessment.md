# Billing Readiness Assessment

Status: Phase-7.5 assessment

## Product Progress

Curis now has a stable local demo, usage_event attribution, audit_event attribution, and Value Event contract design. This assessment decides whether the system is ready to enter Billing Readiness planning, not Billing implementation.

## 1. Is usage_event Enough?

For usage analytics: yes.

usage_event currently supports:

- tenant attribution,
- task attribution,
- workflow_run attribution,
- workflow_step attribution,
- employee attribution,
- capability source/type/id attribution,
- model gateway/model name,
- token usage,
- estimated cost,
- status,
- timestamp,
- redacted credential attribution.

For authoritative billing: no.

Reasons:

- `estimated_cost` is not settlement-grade.
- usage_event is execution evidence, not billing interpretation.
- usage_event does not apply plan, quota, discounts, credits, tax, invoice period, or payment status.

## 2. Is Value Event Needed?

For Billing MVP: not strictly required.

For commercial validation: yes.

Value Event helps Curis answer:

```text
What value did AI create?
```

It supports:

- customer value narrative,
- pricing research,
- productivity reporting,
- future ROI analysis.

Value Event should not be required to issue basic usage-based invoices, but it is useful for pricing strategy and future value analytics.

## 3. Is billing_event Needed?

Yes, before Billing MVP implementation.

billing_event should separate:

- raw usage evidence,
- value estimates,
- billing interpretation.

Billing Event should apply:

- plan,
- quota,
- rating rules,
- billing period,
- currency,
- invoice line mapping.

## 4. Are Plan / Quota Needed?

Yes, for any commercial product beyond manual invoicing.

Minimum plan/quota concepts:

- plan tier,
- billing interval,
- included usage,
- overage rule,
- tenant subscription,
- quota period,
- used quantity.

Without plan/quota:

- customers cannot predict cost,
- Admin cannot enforce limits,
- invoices lack commercial context.

## 5. Is Admin / Workspace Boundary Clear?

Yes, with one caveat.

Workspace owns:

- execution,
- employee/workflow/capability attribution,
- usage_event,
- audit_event,
- future Value Event drafts/confirmation only if separately approved.

Admin owns:

- plan,
- quota,
- billing_event,
- invoice,
- subscription/payment integration,
- billing UI,
- billing analytics.

Caveat:

- If Value Event confirmation happens in Workspace, Admin must still treat it as commercial analytics input, not invoice authority.

## 6. Readiness Decision

Curis is ready to enter Billing Readiness planning.

Curis is not ready to enter Billing implementation.

Reason:

- Usage Event data foundation exists.
- Value Event contract now defines value-side evidence.
- Admin/Workspace boundary is clear.
- But billing_event, plan/quota, invoice, rating, and payment contracts are not implemented or approved.

## 7. Recommended Next Step

Open a Billing Readiness gate that produces:

- Admin-owned billing_event contract.
- Plan/quota contract.
- Invoice draft contract.
- usage_event-to-billing_event mapping.
- value_event optional analytics mapping.
- redaction and tenant isolation requirements.

Do not implement:

- payment,
- invoice issuance,
- ROI dashboard,
- automatic value-based pricing,
- Marketplace monetization.
