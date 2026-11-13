# Value Event Type Contract

Status: Phase-7.5 design only

No runtime implementation is approved by this document.

## Supported First-Version Types

| value_type | Meaning | Unit Recommendation | First-Version Source | Notes |
| --- | --- | --- | --- | --- |
| `time_saved` | Estimated human time saved by task/workflow/employee output. | hours | user confirmed or default assumption | Best first value metric because it is easy to understand. |
| `cost_avoided` | Estimated labor/vendor cost avoided. | currency | user confirmed | Usually derived from time_saved and an assumed hourly cost. |
| `output_generated` | Valuable deliverable was generated. | count or value score | workflow_result or user confirmed | Examples: document, code, QA report, analysis. |
| `quality_improved` | Output improved quality or reduced defects. | score or currency estimate | user confirmed | Should be conservative because quality is subjective. |
| `revenue_assisted` | AI work helped create or accelerate revenue. | currency | user confirmed or external import | First version records estimate only; no revenue prediction. |

## Type Rules

### `time_saved`

Use when the user can estimate hours saved.

Example:

```text
QA Engineer generated a test plan that would take 0.5 hours manually.
```

### `cost_avoided`

Use when the user can estimate avoided human/vendor cost.

Example:

```text
2.0 hours saved * 50 USD/hour = 100 USD cost_avoided.
```

### `output_generated`

Use when a useful artifact is generated.

Examples:

- PRD
- technical plan
- frontend implementation
- backend implementation
- QA report
- final workflow report

### `quality_improved`

Use when AI output catches issues, improves completeness, or reduces rework.

Example:

```text
QA step identifies missing API validation before handoff.
```

### `revenue_assisted`

Use when AI work supports revenue activity.

Examples:

- prepares sales material,
- accelerates delivery,
- improves response to a customer opportunity.

First version rule:

- Record estimate only.
- Do not predict revenue automatically.
- Do not use for financial settlement.

## Explicitly Not Implemented

- Automatic ROI.
- Revenue forecasting.
- Financial settlement.
- Pricing calculation.
- Payment.
- Business metric import.

## Future Reserved Types

Future gates may add:

- `risk_reduced`
- `cycle_time_reduced`
- `customer_response_improved`
- `conversion_assisted`
- `compliance_evidence_created`
