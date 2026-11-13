---
issue: "066"
title: "Workspace Official Model Catalog"
status: "implemented-and-verified"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/063_adr0028_phase2_admin_platform_mvp_prd.md; issues/064_adr0028_phase2_newapi_gateway_prd.md"
---

# Workspace Official Model Catalog

## Objective

Expose a Workspace read-only official model catalog so Workspace can consume Admin-supplied model capability metadata without implementing Admin pages, billing, governance, marketplace, or credentials.

## Minimal Context

- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/062_adr0028_phase1_shared_contract.md`
- `issues/063_adr0028_phase2_admin_platform_mvp_prd.md`
- `issues/064_adr0028_phase2_newapi_gateway_prd.md`

## Scope

- Add additive `official_models` catalog metadata table.
- Seed one official New API model catalog row from gateway environment defaults.
- Add `GET /api/catalog/models` Workspace read-only endpoint.
- Return only active `source=official` model rows.
- Include `gateway_ref`, `auth_type`, and `supported_models` shape metadata only.

## Non-Goals

- No Admin Platform page.
- No Admin write API for models.
- No credential, secret, API key, or password persistence.
- No billing, ROI, tenant package, or platform governance.
- No marketplace or tenant-private model implementation.
- No execution behavior changes beyond the already accepted Model Gateway Adapter.

## Allowed Files

- `backend/app/database.py`
- `backend/app/main.py`
- `backend/tests/test_model_gateway_adapter.py`
- status/context/review files.

## Acceptance Criteria

- `GET /api/catalog/models` returns HTTP 200.
- Response contains `models`.
- Returned models are `source=official` and `status=active`.
- Returned models include `gateway_ref` and `supported_models`.
- Returned models do not expose credential-like fields.
- Existing Model Gateway Adapter and ADR-0028 UsageEvent tests remain green.

## Verification

- Add failing test before implementation.
- Run targeted official model catalog test.
- Run model gateway adapter tests.
- Run backend regression with `python -m unittest discover tests`.

## Completion Notes

- Implemented additive `official_models` catalog table.
- Implemented idempotent official New API model seed.
- Implemented `GET /api/catalog/models`.
- Verification recorded in `reviews/063_workspace_official_model_catalog_review.md`.
