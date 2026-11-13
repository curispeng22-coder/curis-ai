# ADR-0022: D1 Multi-Tenant `tenant_id` Reservation — Boundary

Date: 2026-07-07

Status: Proposed — boundary for D1 (ADR-0017 Sub-decision D1); pending 质量运行席 verification + 产品规划席 acceptance.

Source gate: `issues/050_adr0017_future_gate_submission_package.md` (option a accepted by 总控决策席, 2026-07-07)
Carried-forward decisions: `docs/decisions/ADR-0017-multitenant-department-catalog.md` (Proposed, D1 section), `docs/decisions/ADR-0016-execution-substance-initiative.md` (Accepted)
Slice issue: `issues/051_adr0017_d1_tenant_id_reservation.md`

## Context

ADR-0017 option a is accepted: the "multi-tenant CEO + department catalog" future phase gate is OPEN, and D1 (tenant_id reservation, design-only) is the first slice. The product is a commercial multi-tenant system where every login is an independent CEO. Today it runs single-user / single-process, but ADR-0017 requires that turning on multi-tenancy later be a "add column + inject middleware" change, **not a rewrite**.

The current SQLite schema has no tenant scope on any table. This boundary reserves that scope on the two concrete aggregate roots that exist today — `tasks` (the L1 execution root) and `evolution_events` (the ADR-0016 D3 observability root) — plus a `TenantContext` resolver hook that today always returns the single-tenant sentinel `'default'`.

## Decision (Boundary Contract)

### 1. Additive schema reservation (zero rewrite)

Leverage the existing `_ensure_column()` migration helper in `backend/app/database.py` (it already uses `ALTER TABLE ... ADD COLUMN`, which is additive and backfills existing rows):

```python
# in Database.initialize(), alongside the existing _ensure_column calls:
self._ensure_column(connection, "tasks", "tenant_id", "text not null default 'default'")
self._ensure_column(connection, "evolution_events", "tenant_id", "text not null default 'default'")
```

- `tenant_id TEXT NOT NULL DEFAULT 'default'`.
- Existing rows backfill to `'default'`; new rows without an explicit `tenant_id` get `'default'` from the DB default — **no insert-site code changes required**.
- Scoped to `tasks` + `evolution_events` only. These are the two concrete roots ADR-0017 D1 names (Task, EvolutionLog). Department / Employee / Asset tables do not exist yet and will reserve `tenant_id` when they are introduced in later slices. `tools` is a cross-tenant shared registry and is intentionally **not** scoped.

### 2. New module `backend/app/tenant_context.py` (resolver stub)

```python
from contextvars import ContextVar
from typing import Iterator

DEFAULT_TENANT = "default"
_current_tenant: ContextVar[str] = ContextVar("curis_tenant", default=DEFAULT_TENANT)

class TenantContext:
    @staticmethod
    def current_tenant_id() -> str:
        """Return the active tenant id. Today always 'default' (single-tenant)."""
        return _current_tenant.get()

    @staticmethod
    def scope(tenant_id: str) -> Iterator[None]:
        """Context-manager hook reserved for future per-request tenant injection.
        No-op for isolation today — only sets the contextvar within the block."""
        token = _current_tenant.set(tenant_id)
        try:
            yield
        finally:
            _current_tenant.reset(token)

    @staticmethod
    def is_multi_tenant() -> bool:
        """Always False today. Flips to True when real resolution is wired in."""
        return False
```

- `current_tenant_id()` returns `'default'` unconditionally today.
- `scope()` is a reserved injection point (contextvar only; no filtering, no isolation logic).
- `is_multi_tenant()` is a single feature-flag the rest of the system can branch on later.

### 3. No behavior change, no new endpoint, no query filtering

- D1 does **not** add `WHERE tenant_id = ?` to any read path.
- D1 does **not** change any existing insert statement (the DB default covers it).
- D1 does **not** add an API endpoint or change API semantics.
- D1 does **not** implement real isolation, per-tenant credential scoping, or worker `tenant_id` propagation — those are deferred future slices and trigger 安全边界席 review when they land.

### Invariant (enforced in code + tests)

- After `Database().initialize()`, both `tasks` and `evolution_events` have a `tenant_id` column.
- All rows (pre-existing and new) carry `tenant_id = 'default'`.
- `TenantContext.current_tenant_id()` == `'default'`; `TenantContext.is_multi_tenant()` == `False`.
- No existing test breaks; backend regression stays green.

## Forbidden Scope (carried forward from ADR-0017 + ADR-0016)

- Real multi-tenant isolation, per-tenant credential scoping, worker `tenant_id` propagation.
- `WHERE tenant_id = ?` query filtering or any read-path scoping.
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- External services, external platform credentials, compliance surfaces (these are 安全边界席 territory).
- Complex UI / dashboard beyond minimal evidence display.
- API semantic changes (therefore no new endpoint).
- Lifting the human-approval gate for code self-modification.
- ROI / economy, business modules, company organization (L5/L6) beyond the `tenant_id` column reservation itself.
- Vector database, embeddings, external memory service, hidden memory store.
- Other future-layer implementation.

## Verification Plan

质量运行席 verifies with the standard diff and forbidden-scope guards plus:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
# forbidden-scope keyword scan on changed backend/app files
```

Plus slice-specific assertions (covered by `backend/tests/test_d1_tenant.py`):
- `tasks` and `evolution_events` each expose a `tenant_id` column after `initialize()`.
- A pre-existing row (seeded before migration) backfills to `'default'`.
- A newly inserted row without explicit `tenant_id` gets `'default'` from the DB default.
- `TenantContext.current_tenant_id()` returns `'default'`; `is_multi_tenant()` returns `False`.
- `TenantContext.scope('ceo-2')` sets the value within the `with` block and restores `'default'` after — proving the hook is wired (still single-tenant at the data layer).
- Backend regression passes; no existing test modified.

## Consequences

- Easier: the system now *has* a tenant scope on its two core roots and a resolver hook — proving multi-tenancy is an "add column + inject" evolution, not a rewrite, exactly as ADR-0017 promised.
- Easier: future D1.x slices (real resolution, query filtering, per-tenant creds) have a clean, tested seam to build on.
- Harder / cost: one new tiny module + two additive columns; a small, reviewable production-diff surface (code + schema migration, no behavior change).
- No isolation is actually enforced today — this is a reservation, deliberately. The isolation *model* decision (shared-DB + column vs per-tenant schema) is recorded here and should be re-confirmed with 安全边界席 when the isolation slice is opened.
