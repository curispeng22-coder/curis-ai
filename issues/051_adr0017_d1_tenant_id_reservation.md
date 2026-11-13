# Issue 051 — ADR-0017 D1: `tenant_id` Reservation (Design-Only)

- **Owner seat**: 系统交付席
- **Status**: Boundary proposed (ADR-0022) → 质量运行席 verification PASS (reviews/050, reviews/051) → **ACCEPTED by 主理人齐活林 (产品规划席 delegation, 2026-07-07 23:27)** → implementation done (committed 73001046) → D1 CLOSED
- **Source gate**: `issues/050_adr0017_future_gate_submission_package.md` option a (accepted by 总控决策席, 2026-07-07)
- **Boundary**: `docs/decisions/ADR-0022-d1-tenant-id-reservation-boundaries.md`

## Minimal Context

ADR-0017 future phase gate is OPEN (option a). D1 is the first slice: reserve a tenant scope on the two concrete aggregate roots (`tasks`, `evolution_events`) plus a `TenantContext` resolver stub, so future multi-tenancy is an "add column + inject middleware" evolution rather than a rewrite. Today the system stays single-tenant (`'default'` sentinel).

## Scope

- Additive schema: `tenant_id TEXT NOT NULL DEFAULT 'default'` on `tasks` and `evolution_events`, via the existing `_ensure_column()` helper (zero rewrite; backfills existing rows).
- New module `backend/app/tenant_context.py`: `TenantContext` with `current_tenant_id()`, `scope()` (contextvar hook), `is_multi_tenant()` (always `False` today).
- Tests in `backend/tests/test_d1_tenant.py`.

## Non-goals

- No real multi-tenant isolation, no `WHERE tenant_id = ?` filtering, no per-tenant creds, no worker propagation.
- No API endpoint, no read-path scoping, no insert-site changes.
- No Department / Employee / Asset tables (future slices).
- No Employee CRUD, multi-agent, external services, L5/L6 (forbidden zone).

## Allowed files

- `backend/app/database.py` (additive `_ensure_column` calls only)
- `backend/app/tenant_context.py` (new)
- `backend/tests/test_d1_tenant.py` (new)
- `docs/decisions/ADR-0022-d1-tenant-id-reservation-boundaries.md` (this slice's boundary)
- `issues/051_adr0017_d1_tenant_id_reservation.md` (this issue)

## Acceptance criteria

1. After `Database().initialize()`, `tasks` and `evolution_events` both expose `tenant_id`.
2. All rows (pre-existing + new) carry `tenant_id = 'default'`.
3. `TenantContext.current_tenant_id()` == `'default'`; `is_multi_tenant()` == `False`.
4. `TenantContext.scope()` sets within block, restores after (hook wired, still single-tenant at data layer).
5. Backend regression green; no existing test modified; forbidden-scope scan clean.

## Verification

质量运行席:
- `git diff --name-only HEAD -- backend frontend` (scope check)
- `git diff --check` (whitespace)
- forbidden-scope keyword scan on changed `backend/app` files
- `python -m unittest discover tests` (regression)
- `backend/tests/test_d1_tenant.py` all pass

## Completion notes

D1 `tenant_id` reservation CLOSED 2026-07-07 23:27. Implementation: `backend/app/tenant_context.py` (TenantContext stub) + additive `tenant_id` on `tasks`/`evolution_events` via `_ensure_column`; 6 new tests; 69 backend tests green (committed 73001046). Boundary verification reviews/050 PASS, implementation verification reviews/051 PASS. **Slice accepted by 主理人齐活林** (产品规划席 role delegated per 2026-07-07 23:27 operating-mode change; user retains 总控决策席 gate only).
