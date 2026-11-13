# Phase-4.5 Demo Polish

Status: Draft

Owner Seat: 系统交付席 for doc/seed/E2E delivery after 产品规划席 acceptance.

## Background

Phase-4 Demo Freeze is functionally ready, but the demo still requires manual startup, manual seed creation, manual screenshot capture, and explanation around placeholder credential references.

## Goal

Improve local/demo repeatability without adding core product functionality.

Allowed polish:

- Demo seed script.
- Startup script.
- Stable browser E2E.
- Screenshot capture checklist or generated screenshots.
- Demo copy.
- Operator notes.

## Non-Goals

- Do not add product features.
- Do not implement Workflow.
- Do not implement credential vault.
- Do not implement Billing.
- Do not implement ROI.
- Do not add marketplace.
- Do not add content operations, investment, ecommerce, HR, or other departments.
- Do not modify Admin Platform governance.
- Do not change Task Execution semantics.
- Do not add real secrets.

## Data Model Impact

No data model changes.

Allowed:

- Optional local demo seed data inserted through existing APIs or a local-only script.

Blocked:

- No schema changes.
- No migrations.
- No new persistent product tables.

## API Impact

No API changes.

Allowed:

- Use existing Workspace and Admin read APIs in demo scripts.

Blocked:

- No new endpoints.
- No API semantic changes.
- No `/api/platform/*` calls from Workspace runtime.

## UI Impact

Allowed:

- No-code or documentation-only screenshot guidance.
- If separately approved, small copy-only demo hints may be proposed.

Blocked:

- No new UI feature.
- No complex dashboard.
- No org chart.
- No workflow UI.

## Security Boundary

- Demo seed must not include real secrets.
- `credential_ref` and `config_ref` must remain placeholders such as `env:DEMO_REF`.
- Screenshots must not show real credentials.
- Admin usage query remains read-only.

## Test Requirements

- Run demo seed from a clean `/tmp` database.
- Run browser E2E or documented manual click path.
- Capture screenshot set:
  - R&D employee templates.
  - Employee instance list.
  - Employee capability binding.
  - Task creation with employee selector.
  - Task execution result.
  - Admin usage_event employee attribution.
- `git diff --check`.
- Workspace `/api/platform/*` runtime scan.
- Secret scan.

## Acceptance Criteria

- A non-core engineer can start the local demo from documented commands.
- Demo data is repeatable.
- Screenshots can be captured from a clean local database.
- No core feature behavior changed.
- No secret or Admin governance boundary changed.

## Recommended Priority

P2, parallel-safe.

Reason: improves demo quality but does not unlock production capability or core AI company behavior.
