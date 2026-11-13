# ADR-0020: D3 Append-Only Evolution Event Log — Boundary

Date: 2026-07-07

Status: Proposed — boundary for D3 (ADR-0016 Sub-decision C); pending 质量运行席 verification + 产品规划席 acceptance.

Source gate: `issues/044_execution_substance_phase_gate.md` (approved via `issues/048` option a, 2026-07-07)
Carried-forward decision: `docs/decisions/ADR-0016-execution-substance-initiative.md` (Accepted)
Slice issue: `issues/047_append_only_evolution_log_first_slice.md`

## Context

ADR-0016 Sub-decision C is approved. The Evolution Governor and architecture-lock paths currently write to *mutable* SQLite tables (`evolution_simulations`, `evolution_decisions`, `rollback_records`, `architecture_locks`, plus the legacy `system_evolution_log`). For a system whose core claim is controlled self-modification, the audit trail must be append-only and tamper-evident. D3 introduces the append-only `evolution_events` log as the system of record for audit, without dropping or mutating any existing table.

## Decision (Boundary Contract)

### Schema (additive, in `backend/app/database.py` `initialize()`)

```sql
create table if not exists evolution_events (
  event_id integer primary key autoincrement,
  correlation_id text not null,
  event_type text not null,   -- 'proposal' | 'simulation' | 'decision' | 'lock' | 'rollback'
  payload text not null,       -- JSON
  created_at text not null default current_timestamp
);
```

No existing table is dropped, altered, or given an UPDATE/DELETE path.

### New module `backend/app/evolution_event_log.py`

```python
class EvolutionEventLog:
    def __init__(self, database: Database): ...
    def record(self, *, correlation_id, event_type, payload) -> dict   # INSERT ONLY
    def get_by_correlation_id(self, correlation_id) -> list[dict]      # SELECT ONLY
    def get_all(self) -> list[dict]                                    # SELECT ONLY
```

**Invariant (enforced in code, not just policy):** this class exposes **no** `update` / `delete` / mutating method. The only write path is `record` (INSERT). Verification asserts the class has no update/delete attribute and that no UPDATE/DELETE SQL string exists in the module.

### Injection (optional, backward-compatible)

- `ResultStore.__init__(self, database, event_log=None)` — when `event_log` is provided, the following save methods accept an optional `correlation_id` and emit an event after the insert:
  - `save_evolution_simulation(..., correlation_id=None)` → event_type `simulation`
  - `save_rollback_record(..., correlation_id=None)` → event_type `rollback`
  - `save_evolution_decision(..., correlation_id=None)` → event_type `decision`
  - `save_architecture_lock(..., correlation_id=None)` → event_type `lock`
  - A private `_emit(correlation_id, event_type, payload)` guards on `self.event_log is not None and correlation_id is not None`.
- `EvolutionGovernor.__init__(self, store, event_log=None)` — when provided, `evaluate()` generates one `correlation_id = str(uuid.uuid4())` per call, passes it to the three store saves, and emits a `proposal` event (if a proposal was built). `evaluate()` also returns the `correlation_id` in its result dict (additive field).
- `orchestrator.py` constructs `EvolutionGovernor(store, store.event_log)` — no change to `Orchestrator` constructor signature.
- `main.create_app` builds `event_log = EvolutionEventLog(database)` and passes it to `ResultStore(database, event_log)`.

Old tests that construct `ResultStore(database)` / `EvolutionGovernor(store)` without `event_log` keep working unchanged (no events emitted).

### Read-only endpoint (additive, in `main.create_app`)

```python
@app.get("/api/evolution-events")
def get_evolution_events(correlation_id: str | None = None):
    return event_log.get_by_correlation_id(correlation_id) if correlation_id else event_log.get_all()
```

This is an additive read endpoint (allowed by issues/047). No existing endpoint semantics change.

### Correlation id

One `correlation_id` is generated per `EvolutionGovernor.evaluate()` run and threads proposal → simulation → decision → rollback. Lock events carry the `correlation_id` passed to `save_architecture_lock` (caller-supplied). Every event is thus linkable.

## Forbidden Scope (carried forward from ADR-0016 + issues/047)

Same as ADR-0016 Forbidden Scope, plus:
- Dropping / mutating existing persistence tables in this phase.
- UPDATE / DELETE paths on `evolution_events` (the log is immutable).
- Replacing `CURRENT_CONTEXT.md`, `PROJECT_STATUS.md`, or other source-of-truth files with the log.
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- Complex UI / dashboard beyond minimal evidence display.
- API semantic changes beyond the additive `/api/evolution-events` read endpoint.
- ROI / economy, business modules, company organization (L5/L6).
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Vector database, embeddings, external memory service, hidden memory store.
- Automatic evolution behavior changes / automatic code self-modification.
- Future-layer implementation.

## Verification Plan

质量运行席 verifies with the standard diff and forbidden-scope guards plus:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
# forbidden-scope keyword scan on changed backend/app files
```

Plus slice-specific assertions (covered by `backend/tests/test_d3_event_log.py`):
- `evolution_events` table exists after `database.initialize()`.
- `EvolutionEventLog` exposes no `update` / `delete` method (insert-only invariant).
- `record` inserts; `get_by_correlation_id` returns the event; payload round-trips.
- Multiple events under one `correlation_id` are returned together; different `correlation_id`s do not mix.
- `ResultStore` with `event_log` emits `lock` / `simulation` / `decision` / `rollback` events carrying the supplied `correlation_id`.
- `EvolutionGovernor.evaluate()` emits `proposal` / `simulation` / `decision` / `rollback` events sharing one `correlation_id` (read from the returned `correlation_id`).
- Backend regression passes (no behavior change when `event_log` is None).

## Consequences

- Easier: evolution history (proposal/simulation/decision/lock/rollback) is now auditable and tamper-evident via an append-only log; a queryable correlation chain exists.
- Easier: this is the audit substrate that D2 (Governor Sandbox) and future L5/L6 ROI/BI can read from.
- Harder: one new table + one new module + optional injection params; another small, reviewable production-diff surface.
- No behavior change when `event_log` is absent (backward compatible; zero regression risk for existing paths).
