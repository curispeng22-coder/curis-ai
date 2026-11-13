---
issue: "064"
title: "Workspace Capability Integration Phase-1"
status: "implemented-and-verified"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/062_adr0028_phase1_shared_contract.md"
---

# Workspace Capability Integration Phase-1

## Objective

Implement the smallest Workspace-side slice of ADR-0028:

- expose a read-only official capability catalog for Workspace;
- preserve tenant-scoped execution behavior;
- write UsageEvent records from the Workspace execution path;
- keep tenant-private namespace rules documented for future implementation.

## Scope

- Add Workspace read-only catalog API for official department types.
- Add request-scoped CEO placeholder context from `X-Ceo-Id`.
- Add UsageEvent write from execution persistence.
- Add admin-only UsageEvent projection.

## Non-Goals

- No billing calculation.
- No connector credential persistence.
- No marketplace implementation.
- No private model/tool credential persistence.
- No CEO login or token issuance implementation.
- No complex UI.

## Allowed Files

- `backend/app/`
- `backend/tests/`
- `issues/064_workspace_capability_integration_phase_1.md`
- status/context files if needed for closeout.

## Acceptance Criteria

- `GET /api/catalog/department-types` returns official department types with `source=official`.
- Workspace task execution writes a `usage.model_call` event with `tenant_id`, `ceo_id`, capability reference, and idempotency key.
- Usage projection is available only through an admin-token endpoint.
- Missing `X-Ceo-Id` fails closed for execution paths that would emit UsageEvent.
- Existing tenant task isolation remains intact.

## Verification

- Add failing tests before implementation.
- Run the targeted new tests.
- Run backend regression with `python -m unittest discover tests`.

## Completion Notes

- Implemented `GET /api/catalog/department-types` as a Workspace read-only official catalog.
- Added request-scoped `X-Ceo-Id` placeholder context.
- Added `usage.model_call` event writing from `ResultStore.save_execution`.
- Added admin-only `GET /api/platform/usage` projection.
- Verification recorded in `reviews/061_workspace_capability_integration_phase_1_review.md`.
