# Pricing Contract

Status: Frozen v1 commercial package model

Owner: Admin Platform owns future pricing and billing implementation. Workspace supplies usage/value evidence only through approved contracts. This document is a commercial contract baseline, not an implementation plan.

## Product Progress

Curis has a stable local demo, AI Employee System, Workflow MVP, Credential Vault, usage_event, audit_event, and Value Event contract. Phase-7.6 freezes the first commercial model as Hybrid pricing without implementing Billing, payment, invoice generation, ROI, or new product behavior.

## Commercial Model

Curis commercial model is Hybrid:

- tiered subscription,
- token/model usage,
- capability packages,
- AI employee seats,
- future value-based pricing.

The first commercial package model is frozen in `docs/decisions/commercial-package-model-v1.md`.

Frozen package ladder:

- `free`: trial and onboarding package.
- `pro`: main self-serve paid package.
- `enterprise`: governed sales-led package.

Frozen monetization dimensions:

- subscription base,
- token usage,
- capability packages,
- AI employee seats,
- future value-based pricing reserve.

Prices remain `$XX` placeholders until 总控决策席 approves final price points. This contract freezes the package model, not payment, invoice, or charging implementation.

## Plan Definitions

| Plan | Purpose | Target User | Commercial Meaning |
| --- | --- | --- | --- |
| Free | Try the AI company workflow with constrained limits. | New solo founder / evaluator | Acquisition and onboarding tier. |
| Pro | Run a practical AI company workspace with higher usage and private capability support. | Solo entrepreneur / small operator | Primary self-serve paid tier. |
| Enterprise | Governed multi-tenant / team / compliance-ready deployment. | Company/team customer | Sales-led tier with custom limits and support. |

## Plan Structure

Plan contains:

- `plan_id`
- `name`
- `tier`: `free` / `pro` / `enterprise`
- `status`: `draft` / `active` / `deprecated`
- `billing_interval`: `monthly` / `annual` / `custom`
- `features`
- `quotas`
- `capability_packages`
- `employee_seat_limit`
- `created_at`
- `updated_at`

Phase-7.6 does not implement these fields in code.

## Feature

Feature defines what a plan unlocks.

Recommended feature keys:

- `task_execution`
- `workflow_sop`
- `tenant_private_capabilities`
- `credential_vault`
- `value_event_tracking`
- `admin_usage_observability`
- `team_management`
- `priority_support`

Feature fields:

- `feature_key`
- `name`
- `description`
- `enabled`
- `plan_tiers`

## Quota

Quota defines plan limits.

Recommended quota keys:

- `monthly_tokens`
- `monthly_model_calls`
- `monthly_workflow_runs`
- `monthly_tasks`
- `private_capability_count`
- `ai_employee_seats`
- `credential_count`
- `storage_mb`

Quota fields:

- `quota_key`
- `metric`
- `included_amount`
- `period`
- `overage_allowed`
- `overage_rule`

## Token Allowance

Token allowance is the first usage-based quota dimension.

Recommended fields:

- `token_quota_id`
- `plan_id`
- `monthly_included_tokens`
- `counted_token_types`: `prompt` / `completion` / `total`
- `model_scope`: `all` / `official` / `tenant_private` / specific model group
- `overage_allowed`
- `overage_unit_price`
- `currency`

Rules:

- Token allowance is based on usage_event token fields.
- Token allowance is not calculated in Workspace.
- Billing-rated token amount belongs to future Admin-owned BillingEvent.
- `estimated_cost` remains non-authoritative.

## Capability Package

Capability Package groups model/tool/connector/template access.

Package examples:

- `starter_rnd_pack`
- `pro_rnd_pack`
- `private_capability_pack`
- `premium_model_pack`
- `workflow_template_pack`
- `future_marketplace_pack`

Capability Package fields:

- `package_id`
- `name`
- `description`
- `source`: `official` / `tenant_private` / `marketplace`
- `included_capability_ids`
- `included_template_ids`
- `plan_tiers`
- `status`

Rules:

- `official` packages are supplied by Admin.
- `tenant_private` packages remain tenant-scoped.
- `marketplace` packages are future-gated.

## Employee Seat Reserve

Employee Seat is reserved as a pricing dimension.

Seat fields:

- `seat_type`: `ai_employee`
- `role_scope`: `all` / specific employee role
- `included_count`
- `additional_count_allowed`
- `overage_rule`

Phase-7.6 does not implement employee-seat billing.

## Suggested Tier Shape

| Dimension | Free | Pro | Enterprise |
| --- | --- | --- | --- |
| Tasks | Low monthly limit | Higher monthly limit | Custom |
| Workflow runs | Demo-level | Production-like self-serve | Custom |
| Token/model usage | Low included quota | Paid quota / overage-ready | Contracted |
| AI employee seats | Limited R&D seats | Full R&D seat set | Custom departments/seats |
| tenant_private capability | Limited or disabled | Enabled | Governed |
| Credential Vault | Local/demo or limited | Enabled within approved boundary | Production Vault/KMS required |
| Capability packs | Starter official pack | Pro official packs | Custom/approved packs |
| Marketplace | Not included | Future optional | Future governed |
| Value Event | Basic visibility | Commercial validation | Advanced analytics future-gated |

## Frozen V1 Package Model

| Dimension | Free | Pro | Enterprise |
| --- | --- | --- | --- |
| Package role | Trial / onboarding | Main self-serve paid tier | Governed sales-led tier |
| AI employee seats | Limited R&D seats, default ceiling 3 | Full R&D working set, default ceiling 15 | Custom / unlimited by contract |
| Token quota | Low included quota, default 1M monthly tokens | Production-like quota, default 50M monthly tokens | Custom / unlimited by contract |
| Workflow quota | Demo-level, default 5,000 monthly runs | Self-serve, default 50,000 monthly runs | Custom / unlimited by contract |
| Capability package | Official starter package | Official standard package | Full official package plus governed future options |
| tenant_private capability | Disabled or tightly limited | Enabled | Enabled with governance |
| Marketplace | Not included | Future optional after G3 | Future governed option after G3 |
| Value pricing | Not active | Not active | Future-gated only |

Rules:

- Free / Pro / Enterprise is the only v1 package ladder.
- Token usage is the first metered usage dimension.
- Capability Package is a package/content differentiation dimension, not a runtime permission bypass.
- AI Employee Seat is counted from active Workspace EmployeeInstance evidence until a future seat-specific gate adds explicit commercial seat fields.
- Value-based pricing is a reserved future L6 option and is not active in v1.

## Boundary

This contract does not approve:

- Billing implementation,
- payment,
- invoice generation,
- ROI system,
- Marketplace,
- Usage Event schema change,
- Workspace execution-chain change,
- Admin implementation change.
