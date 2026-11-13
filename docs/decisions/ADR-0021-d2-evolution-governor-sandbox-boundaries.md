# ADR-0021: D2 Evolution Governor Sandbox — Boundary

Date: 2026-07-07

Status: Proposed — boundary for D2 (ADR-0016 Sub-decision B); pending 质量运行席 verification + 产品规划席 acceptance.

Source gate: `issues/044_execution_substance_phase_gate.md` (approved via `issues/048` option a, 2026-07-07)
Carried-forward decision: `docs/decisions/ADR-0016-execution-substance-initiative.md` (Accepted)
Slice issue: `issues/046_evolution_governor_sandbox_first_slice.md`

## Context

ADR-0016 Sub-decision B is approved. The Evolution Governor currently produces proposals, simulations, and rollback *records*, but there is no safe substrate to demonstrate a controlled change. D2 adds a sandbox that applies a Stability-first proposal to a **throwaway copy** of state and rolls it back, capturing reviewable evidence — converting "governor produces records" into "governor can safely demonstrate a change" without ever touching the authoritative repo or SQLite.

## Decision (Boundary Contract)

### New module `backend/app/governor_sandbox.py`

```python
class GovernorSandbox:
    def __init__(self, state_snapshot: dict | None = None): ...
    def run(self, proposal: dict, *, dry_run: bool = True) -> dict: ...
    @staticmethod
    def _apply_proposal(snapshot: dict, proposal: dict) -> dict: ...
```

- `run(proposal, *, dry_run=True)`:
  1. Creates a throwaway directory via `tempfile.mkdtemp(prefix="curis-sandbox-")` (OS temp, never under the project/repo).
  2. Writes a copy of `state_snapshot` into the throwaway dir (`state_snapshot.json`).
  3. `_apply_proposal` produces a *new* dict with a sandbox-proposal marker — it does **not** mutate the input snapshot and does **not** touch authoritative state.
  4. Writes the applied copy (`state_applied.json`) and an `evidence.json` (proposal, dry_run flag, applied_state, rollback_snapshot, throwaway_path).
  5. Rolls back the throwaway copy exactly: writes `state_rolledback.json` equal to the original `state_snapshot`.
  6. Returns an evidence dict (throwaway_path, applied_state, rollback_snapshot, evidence_path, rolled_back=True).
  - **All writes stay under the throwaway temp dir. Zero writes to the authoritative repo or SQLite.**
- `_apply_proposal` is a pure function (no side effects, returns a new dict).

### Additive method on `EvolutionGovernor` (does NOT change `evaluate()`)

`EvolutionGovernor.demonstrate(self, proposal, *, dry_run=True) -> dict`:
- Builds a state snapshot from `self.store.list_architecture_locks()` (current locks).
- Runs `GovernorSandbox(snapshot).run(proposal, dry_run=dry_run)`.
- Returns the sandbox evidence dict.
- This is a demonstration substrate only. Any real production mutation still requires the **explicit human-approval path outside the sandbox** (unchanged gate — D2 does not lift it).

### No API endpoint

D2's allowed scope does **not** include an endpoint, and "API semantic changes" are forbidden. Therefore **no new route is added** in `main.py`. D2 is delivered as the sandbox module + the additive `demonstrate` method + tests.

### Invariant (enforced in code)

The sandbox writes exclusively under the OS temp directory. It never imports or calls `Database`/`ResultStore` write paths. A test asserts the authoritative SQLite file (size/mtime) is unchanged after a run, and that no evolution events are emitted.

## Forbidden Scope (carried forward from ADR-0016 + issues/046)

Same as ADR-0016 Forbidden Scope, plus D2-specific:
- Writing to the authoritative repo or SQLite during a sandbox run.
- Automatic production mutation without explicit human approval.
- Lifting the human-approval gate for code self-modification.
- Changing existing Evolution Governor decision policy beyond the sandbox substrate (do not modify `evaluate()`'s logic).
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- Complex UI / dashboard beyond minimal evidence display.
- API semantic changes (therefore no new endpoint in D2).
- Persistence / schema / new table changes (the append-only log in slice 047 is the only allowed schema addition overall).
- ROI / economy, business modules, company organization (L5/L6).
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Vector database, embeddings, external memory service, hidden memory store.
- Future-layer implementation.

## Verification Plan

质量运行席 verifies with the standard diff and forbidden-scope guards plus:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
# forbidden-scope keyword scan on changed backend/app files
```

Plus slice-specific assertions (covered by `backend/tests/test_d2_sandbox.py`):
- A `run()` produces evidence with `applied_state`, `rollback_snapshot`, `throwaway_path`, `rolled_back=True`.
- `throwaway_path` is inside the OS temp dir (not under the project/repo).
- `applied_state` differs from `rollback_snapshot` (apply changed the copy); `rollback_snapshot` equals the original input snapshot **exactly** (rollback restores precisely).
- `_apply_proposal` does not mutate its input dict.
- After `EvolutionGovernor.demonstrate()`, the authoritative SQLite file size/mtime is **unchanged** (zero authoritative writes); no evolution events are emitted.
- Backend regression passes; `evaluate()` behavior is unchanged (its own tests still pass).

## Consequences

- Easier: the governor can now safely *demonstrate* a controlled change on a throwaway copy with reviewable apply/rollback evidence — the safe execution substrate Sub-decision B promised.
- Easier: this is the proving ground for future genuine self-improvement; today it demonstrates without any production effect.
- Harder: one new module + one additive governor method; another small, reviewable production-diff surface (code only, no schema).
- No behavior change to `evaluate()` or any existing decision policy; no new endpoint; zero writes to authoritative state.
