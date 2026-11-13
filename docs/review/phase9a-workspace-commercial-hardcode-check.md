# Phase 9A Workspace Commercial Hardcode Check

Status: Completed

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace currently has no Workspace-owned runtime pricing, plan, quota, payment, invoice, or BillingEvent logic; commercial interpretation remains Admin-owned.

## Scope

This scan checks Workspace-facing code and docs for hardcoded commercial rules.

This phase records findings only. It does not modify:

- Task Execution.
- Workflow Runtime.
- Employee Runtime.
- Credential Vault.
- Admin Platform logic.
- Billing / Pricing / Quota / Payment / Invoice code.

## Scan Terms

The audit scanned for:

- `plan`
- `price`
- `pricing`
- `quota`
- `billing`
- `billing_event`
- `invoice`
- `payment`
- `commercial`
- `/api/platform/*`

The scan intentionally distinguishes:

- Workspace runtime code,
- Admin Platform code,
- shared database setup,
- documentation / contract references.

## Findings

| Area | Workspace Runtime Finding | Decision |
| --- | --- | --- |
| plan judgment | Not found in Workspace execution path | Pass |
| price / pricing judgment | Not found in Workspace execution path | Pass |
| quota judgment / enforcement | Not found in Workspace execution path | Pass |
| BillingEvent generation | Not found in Workspace execution path | Pass |
| invoice / payment logic | Not found in Workspace execution path | Pass |
| commercial rule enforcement | Not found in Workspace execution path | Pass |
| `/api/platform/*` runtime calls from Workspace frontend | Not found in Workspace frontend runtime scope | Pass |

## Commercial Code That Exists Outside Workspace Runtime

The repository now contains Admin commercial code and shared database structures. These are expected because Admin Phase-9A is in progress.

| Location | Type | Boundary Notes |
| --- | --- | --- |
| `backend/app/billing_store.py` | Admin commercial data service | Admin-owned. Not Workspace execution runtime. |
| `backend/app/main.py` `/api/platform/*` routes | Admin Platform APIs | Platform-admin guarded routes; not Workspace UI/runtime calls. |
| `frontend/app/platform/*` | Admin Platform UI | Admin-owned UI. |
| `backend/app/database.py` plan / quota / pricing / package tables | Shared database setup | Creates Admin commercial tables; Workspace execution should not use these to rate or block execution. |

## Workspace MVP Defaults That Are Not Commercial Rules

Some Workspace defaults remain hardcoded because they are product/runtime scaffolding, not commercial enforcement:

| Default | Why It Is Not A Commercial Rule | Future Owner If Commercialized |
| --- | --- | --- |
| Six software R&D employee templates | Phase-4 AI Employee MVP default team | Admin official template / package configuration |
| Software R&D SOP workflow | Phase-6 Workflow MVP default SOP | Admin official workflow template / package configuration |
| Sequential workflow process only | MVP runtime boundary | Future Workflow v2 gate |
| `official` / `tenant_private` capability source allowlist | Runtime security and source boundary | Marketplace gate for `marketplace` |
| `model` / `tool` / `connector` capability type allowlist | Runtime capability boundary | Shared capability-type contract |

These defaults should not be used as pricing, package, quota, or entitlement rules inside Workspace.

## No-Modify Findings

The following should be recorded only and not changed in this phase:

- Admin commercial tables are present in shared `Database` initialization.
- Admin commercial routes are present under `/api/platform/*`.
- Admin package/pricing/quota contracts are present under `docs/contracts/`.
- Workspace runtime continues to produce usage/value evidence without commercial interpretation.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Reviewers may see Admin commercial code in shared backend files and mistake it for Workspace logic | Medium | Keep PMO ownership notes and issue-level file scopes explicit. |
| Future developers may reuse `plans` / `quotas` directly in Workspace runtime | Medium | Require shared contract and gate before any Workspace quota enforcement. |
| MVP templates may become de facto commercial availability rules | Medium | Migrate official template/package availability to Admin Commercial Configuration before production commercialization. |
| `estimated_cost` may be treated as invoice cost | Medium | Continue labeling it non-authoritative cost evidence only. |

## Shared Contract Need

No new Shared Contract is needed for this audit-only checkpoint.

Shared Contract is needed before:

- Workspace reads Admin commercial config at runtime,
- Workspace enforces package/plan/quota limits,
- Admin requires event-level package/version stamps,
- commercial employee seat type becomes billable.

## Conclusion

Workspace has no commercial hardcode that currently violates the Phase-9A boundary. Existing commercial implementation belongs to Admin Platform or shared database setup, while Workspace remains an execution and evidence producer.
