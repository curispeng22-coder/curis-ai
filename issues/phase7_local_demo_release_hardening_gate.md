# Phase-7 Local/Demo Release Hardening Gate

Status: Draft for gate review

Owner Seat: 产品规划席 for product scope; 总控决策席 for gate approval; 系统交付席 only after approval.

Source review: `docs/release/phase65-post-workflow-roadmap-review.md`

## Background

Phase-6 Workflow MVP Demo Freeze is complete. Curis Workspace can demonstrate a Software R&D AI team running an ordered SOP workflow with redacted usage_event and audit_event attribution.

The demo is still operator-heavy: backend, frontend, local model gateway, seed data, workflow execution, Admin usage/audit checks, and screenshots require manual steps.

## Goal

Create a repeatable local/demo release hardening package without adding product features.

Allowed scope:

- Local/demo seed script or documented seed package.
- Startup/runbook consolidation.
- Browser E2E or scripted smoke for the end-to-end demo chain.
- Screenshot checklist or generated screenshot package.
- Demo narrative copy.
- Known-gap confirmation.
- Release checklist.

## Non-Goals

- Do not add product features.
- Do not change Workflow runtime behavior.
- Do not implement complex DAG.
- Do not implement visual workflow editor.
- Do not implement Billing.
- Do not implement Marketplace.
- Do not implement ROI.
- Do not add content operations / investment / ecommerce modules.
- Do not change Credential Vault security boundaries.
- Do not store real secrets in demo seed.
- Do not let Workspace runtime call `/api/platform/*`.

## Data Model Impact

No schema changes.

Allowed:

- Local/demo seed data inserted through existing APIs.
- Temporary `/tmp` database usage in scripts.

Blocked:

- New persistent product tables.
- Migration files.
- Product runtime state changes.

## API Impact

No API changes.

Allowed:

- Use existing Workspace APIs for setup.
- Use existing Admin read APIs for redacted usage/audit evidence.

Blocked:

- New endpoints.
- API semantic changes.
- Workspace runtime calls to `/api/platform/*`.

## UI Impact

No UI feature changes.

Allowed:

- Documentation-only screenshot guidance.
- Browser E2E using existing pages.

Blocked:

- New dashboard.
- New workflow editor.
- New business UI.

## Security Boundary

- Demo seed must use fake local/demo credentials only.
- Demo scripts must not contain real API keys.
- Evidence must confirm no plaintext credential in API responses, usage_event, audit_event, logs, or screenshots.
- Admin remains read-only observer of redacted usage/audit data.

## Test Requirements

- Run seed from a clean local database.
- Run backend full regression.
- Run frontend unit tests.
- Run frontend lint.
- Run frontend build.
- Run workflow-focused tests.
- Run credential resolver boundary tests.
- Run browser E2E or documented local smoke.
- Run Workspace `/api/platform/*` runtime scan.
- Run scoped secret scan.
- Run `git diff --check`.

## Acceptance Criteria

- A new operator can start the Phase-6 demo from documented commands.
- Demo data can be recreated from a clean local database.
- The Software R&D SOP workflow can be executed end to end.
- usage_event and audit_event evidence can be collected.
- Screenshot checklist is complete.
- No new product behavior was added.
- No secret, Admin governance, Billing, Marketplace, ROI, or Workflow v2 scope was introduced.

## Recommended Priority

P0.

Reason: it converts the working AI company demo into a reliable handoff and presentation package before expanding scope.
