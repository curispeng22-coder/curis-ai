---
issue: "067"
title: "Workspace Official Tool Catalog"
status: "implemented-and-verified"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/062_adr0028_phase1_shared_contract.md; issues/063_adr0028_phase2_admin_platform_mvp_prd.md"
---

# Workspace Official Tool Catalog

## Objective

Expose a Workspace read-only official tool catalog using the existing tool registry so Workspace can consume official tool metadata without implementing Admin pages, marketplace, tenant-private tools, or credentials.

## Minimal Context

- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/062_adr0028_phase1_shared_contract.md`
- `issues/063_adr0028_phase2_admin_platform_mvp_prd.md`

## Scope

- Add `GET /api/catalog/tools`.
- Project existing tool registry rows as `source=official` and `status=active`.
- Keep the endpoint read-only.
- Do not alter tool execution behavior.

## Non-Goals

- No Admin Platform page.
- No Admin write API for tools.
- No credential, secret, API key, or password persistence.
- No marketplace or tenant-private tool implementation.
- No billing, ROI, tenant package, or platform governance.
- No execution routing behavior change.

## Allowed Files

- `backend/app/main.py`
- `backend/tests/test_adr0028_workspace_integration.py`
- status/context/review files.

## Acceptance Criteria

- `GET /api/catalog/tools` returns HTTP 200.
- Response contains `tools`.
- Returned tools are `source=official` and `status=active`.
- Returned tools do not expose credential-like fields.
- Existing ADR-0028 UsageEvent and Model Gateway Adapter tests remain green.

## Verification

- Add failing test before implementation.
- Run targeted official tool catalog test.
- Run ADR-0028 Workspace integration tests.
- Run backend regression with `python -m unittest discover tests`.

## Completion Notes

- Implemented `GET /api/catalog/tools`.
- Reused existing `ToolRegistry.list()` as the source.
- Verification recorded in `reviews/064_workspace_official_tool_catalog_review.md`.
