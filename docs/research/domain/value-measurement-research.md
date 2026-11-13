# Value Measurement Research

Status: Phase-7.5 research

## Product Progress

Curis now has AI employees, workflow execution, credential-safe private capability use, usage_event, audit_event, and a stable demo package. The next commercial question is how to measure value without jumping into ROI or Billing too early.

## 1. SaaS Value Metrics

### Seat Value

Seat-based pricing charges per user or per role.

Pros:

- Easy to understand.
- Predictable recurring revenue.
- Familiar to SaaS buyers.

Cons:

- Curis AI employees do not map cleanly to human seats.
- Customers may resist paying per AI employee before value is proven.
- Does not capture high-value automation outcomes.

Curis fit:

- Useful as a packaging dimension, but weak as the only value metric.

### Usage Value

Usage-based pricing charges based on consumption such as tokens, model calls, workflow runs, or capability calls.

Pros:

- Easy to meter with usage_event.
- Aligns with infrastructure cost.
- Works well for AI-heavy products.

Cons:

- Customers may feel punished for using the product more.
- Usage does not always equal value.
- Requires clear quotas and cost predictability.

Curis fit:

- Strong for cost control and plan limits, but incomplete for business value.

### Outcome Value

Outcome-based pricing charges or positions value around results created.

Pros:

- Best aligned with customer value.
- Differentiates Curis from tool-only AI products.

Cons:

- Hard to measure objectively.
- Requires business context and user confirmation.
- Can create trust issues if AI overclaims value.

Curis fit:

- Important long-term direction, but first version should only collect Value Events as estimates.

### Productivity Value

Productivity pricing emphasizes time saved, tasks completed, throughput, and cycle-time reduction.

Pros:

- Easy for solo entrepreneurs to understand.
- Maps naturally to AI employee and workflow concepts.
- Can be estimated before full billing is ready.

Cons:

- Needs transparent assumptions.
- Time saved is still an estimate.

Curis fit:

- Best near-term value metric.

## 2. AI Agent Value Measurement

AI employee value can be measured through:

- tasks completed,
- workflow steps completed,
- human time saved,
- cost avoided,
- output generated,
- quality improvements,
- cycle time reduction,
- revenue assistance.

The key risk is hallucinated value. AI systems should not self-declare financial impact without user confirmation.

Recommended Curis rule:

```text
AI may draft value evidence.
User confirms estimated value.
Admin may later aggregate confirmed value.
```

## 3. Automation Value Measurement

Automation value is often estimated through:

```text
manual baseline time - automated execution time
```

For Curis local/demo:

- Manual baseline can be a user-entered estimate.
- Automated execution time can be measured later.
- First version can start with user-confirmed time_saved.

Recommended first metric:

```text
time_saved
```

Secondary metric:

```text
cost_avoided = time_saved * assumed hourly cost
```

## 4. Pricing Model Research

### Usage-Based Pricing

Curis can meter:

- model calls,
- tool calls,
- workflow runs,
- employee steps,
- tokens,
- estimated provider cost.

Fit:

- Good for plan limits and infrastructure cost recovery.
- Not enough for value narrative.

### Outcome-Based Pricing

Curis can eventually measure:

- value_event,
- completed workflows,
- revenue assisted,
- quality improvements.

Fit:

- Strong long-term, but not ready for automatic charging.

### Seat-Based Pricing

Curis could package:

- number of human CEO/users,
- number of AI employees,
- number of departments.

Fit:

- Good for simple tiers, but AI employee count alone is not enough.

### Capability-Based Pricing

Curis could package:

- official capability packs,
- private capability usage,
- premium model gateway access,
- workflow templates.

Fit:

- Strong for future Admin catalog and marketplace.
- Requires governance and Billing readiness.

## 5. Curis Commercial Model Recommendation

Recommended future direction: E. Hybrid model.

Curis should not sell only:

- A: AI employee quantity,
- B: AI company size,
- C: capability packs,
- D: execution value.

Recommended packaging:

```text
Base subscription
+ usage limits
+ capability/model access
+ workflow/department scale
+ optional value analytics
```

Near-term:

- Use usage_event for usage analytics and cost awareness.
- Use value_event for commercial validation and value narrative.
- Do not charge from value_event automatically.

Mid-term:

- Admin-owned Billing Event rates usage by plan/quota.
- Value Event supports customer-facing ROI-style reporting only after separate gate.

Long-term:

- Hybrid pricing can combine company scale, usage, capability packs, and validated outcome/value analytics.

## 6. Recommendation For Phase-7.5

Curis should establish:

- Value Event contract.
- Usage/Value boundary.
- Billing readiness assessment.

Curis should not implement:

- ROI dashboard,
- automatic value calculation,
- Billing,
- payment,
- outcome-based charging.
