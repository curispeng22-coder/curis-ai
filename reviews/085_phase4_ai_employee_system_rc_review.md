# Phase-4 AI Employee System MVP RC Review

Status: PASS

Date: 2026-07-09

Release Report: `docs/release/phase4-ai-employee-system-rc.md`

Issue: `issues/phase4_ai_employee_system_mvp.md`

## Product Progress

Curis Workspace can now run a local/demo R&D employee flow: configure the Software R&D department, create a tenant-local Tech Lead employee, bind official and tenant_private capabilities, execute a selected-employee task, and write employee-attributed usage events.

## Acceptance Evidence

- Official employee templates verified:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- Template source handling verified:
  - `official` source appears for seeded official templates.
  - `tenant_private` source is visible only to the owning tenant when seeded as tenant metadata.
  - `marketplace` is schema/contract-reserved and remains inactive because marketplace is outside the Phase-4 gate.
- Tenant-local department instance creation verified.
- Tenant-local employee instance creation verified with `tenant_id`, `company_id`, `department_id`, `instructions_override`, `enabled`, and `status`.
- Employee binding verified for:
  - official tool capability.
  - tenant_private model capability.
- Selected-employee task execution verified.
- Unselected task default routing to Tech Lead verified.
- Unbound explicit capability selection rejected.
- usage_event employee attribution verified.
- tenant_private isolation verified across tenants and catalog endpoints.

## Verification

- Phase-4 RC smoke: PASS.
- `backend/.venv/bin/python -m unittest discover tests`: PASS, 306 tests.
- `frontend/node --test app/taskViewModel.test.mjs`: PASS, 30 tests.
- `frontend/npm run lint`: PASS.
- `frontend/npm run build`: PASS.
- `git diff --check`: PASS on Phase-4 scoped files.
- Workspace `/api/platform/*` runtime scan: PASS.
- Scoped secret scan: PASS.
- Live API template smoke: PASS.

## Known Limits

- No full workflow engine.
- No complex organization chart or multi-department UI.
- No content operations, investment, ecommerce, HR, ROI, marketplace, billing, employee memory, autonomous hiring, or real credential custody.
- Marketplace source stays reserved only until a separate marketplace gate exists.

## Decision

Phase-4 AI Employee System MVP may enter Demo Freeze after product acceptance.

Next Seat: 产品规划席 for final RC acceptance.

Handoff: final closeout
