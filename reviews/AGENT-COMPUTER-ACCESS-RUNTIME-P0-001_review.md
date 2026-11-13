# AGENT-COMPUTER-ACCESS-RUNTIME-P0-001 Review

**Status:** Formal Acceptance Record
**Decision:** AGENT COMPUTER ACCESS RUNTIME P0 IMPLEMENTED / ACCEPTED
**Date:** 2026-08-15
**Scope:** Codex requested/configured/effective truth only
**Isolation:** `/tmp/curis-agent-computer-access-p0.Az782K/`; no active database,
credential, Agent configuration, Full Access, external task or platform call used.

## Implemented runtime model

`CodexCliAdapter` now emits one `computer_access` snapshot through the existing
ToolExecutor → Orchestrator → ResultStore usage-audit route:

```text
requested_intent
→ native_mapping
→ configured_state
→ effective_state
→ verification_state
→ evidence / verified_at
```

- New session: `ASK_WHEN_NEEDED` maps to Codex `--sandbox read-only` and
  `AUTO_WITHIN_BOUNDARY` maps to `--sandbox workspace-write`. A successfully accepted
  command records `configured_state=CONFIGURED`; it still records
  `verification_state=UNVERIFIED`, `effective_state=UNKNOWN` and `verified_at=null`
  because Codex JSONL does not return native effective-access evidence.
- Resume: Current `codex exec resume --help` exposes no sandbox declaration. Resume
  therefore creates a new snapshot with `native_mapping=NOT_CONFIGURABLE`,
  `configured_state=NOT_CONFIGURABLE`, `verification_state=UNVERIFIED`,
  `effective_state=UNKNOWN` and
  `drift=RESUME_ACCESS_UNVERIFIED`. It never copies a prior effective/granted claim.
- Full: `REQUEST_WIDEST_NATIVE_ACCESS` is rejected before an external process starts;
  its snapshot is `UNSUPPORTED`, never active/granted/effective.
- Compatibility `permissions` is now an explicitly non-effective audit projection. It
  carries requested/configured/effective facts rather than a bare sandbox value.

## Runtime evidence

`codex-cli 0.144.6` was inspected locally. `codex exec --help` lists
`--sandbox read-only|workspace-write|danger-full-access` for a new execution;
`codex exec resume --help` does not list a sandbox option. The P0 adapter consequently
does not pass a sandbox argument on resume and records the provider limitation instead.

Final focused isolated SQLite test database:

```text
/tmp/curis-agent-access-final.oRrJQr/test_access_snapshot_persists_0/computer-access.sqlite
PRAGMA integrity_check = ok

usage.tool_call | AUTO_WITHIN_BOUNDARY | CONFIGURED | UNVERIFIED | UNKNOWN | APPLIED
usage.tool_call | AUTO_WITHIN_BOUNDARY | NOT_CONFIGURABLE | UNVERIFIED | UNKNOWN | NOT_CONFIGURABLE
```

The first row is a new-session configuration record. The second is its resumed snapshot
after a fresh `Database` instance reopened the same SQLite file. Requested history
persists; effective state remains independently `UNKNOWN`.

## Focused checks

```text
backend/.venv/bin/python -m py_compile \
  backend/app/agent_adapter.py backend/app/main.py backend/app/tool_executor.py \
  backend/app/orchestrator.py backend/app/result_store.py
passed

backend/.venv/bin/python -m pytest -q \
  backend/tests/test_agent_adapter.py \
  backend/tests/test_agent_computer_access_runtime_p0.py \
  backend/tests/test_ai_capability_registry.py \
  backend/tests/test_codex_agent_backend.py \
  backend/tests/test_runtime_bridge_private_model.py
36 passed
```

The tests cover new-session mapping, resume re-verification truth, Full unsupported
without spawning a process, existing ToolExecutor propagation, isolated SQLite restart
readback and existing Agent discovery, binding, Codex backend and ResultStore/Audit
behavior. The test run produced only existing FastAPI deprecation warnings.

## Changed files

- `backend/app/agent_adapter.py`
- `backend/app/main.py`
- `backend/app/tool_executor.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_agent_computer_access_runtime_p0.py`
- `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`
- `reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md`

## No-regression and boundaries

- Existing Agent discovery registry focused test passes; existing Codex new/resume
  contract test is migrated and passes.
- XHS, RD, TTK, Product Blueprint, Frozen ADR/design contracts, schema, active database,
  other Agent mappings and permission UI were not changed.
- No external Codex task was run for P0. The implementation deliberately does not claim
  provider-effective access merely because the CLI accepted a command.
- No frontend currently consumes the `computer_access` snapshot. Therefore no existing
  UI-facing route can project `CONFIGURED`, `NOT_CONFIGURABLE`, `UNVERIFIED` or
  `UNKNOWN` as granted, active or effective access.

## Final acceptance closure

The final isolated run confirms all P0 truth boundaries:

1. New sessions retain requested intent and the applicable Codex sandbox mapping, but
   record `CONFIGURED / UNVERIFIED / UNKNOWN`; command acceptance is not an effective
   permission claim.
2. Resume sends no sandbox declaration, creates a fresh
   `NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN` snapshot and never inherits an old
   effective state.
3. Full access rejects before process launch with `UNSUPPORTED`; there is no fallback,
   automatic downgrade or configured/active claim.
4. A fresh `Database` instance reopened the isolated SQLite audit store. Requested
   history persisted; neither new nor resume snapshot became effective through
   persistence.
5. `UNKNOWN`, `UNVERIFIED`, `NOT_CONFIGURABLE` and `UNSUPPORTED` are accepted
   persisted runtime outcomes, not failure-to-display success.

P0 implements requested/configured/effective separation, truthful new-session mapping,
resume verification boundary, Full fail-closed behavior, access-snapshot persistence and
audit evidence. It does not implement Full Computer Access, provider-effective
verification beyond available evidence, Registry P1, P2 adapters or Computer Access UI.

## Remaining P1/P2

1. P1 Registry/Binding/Session capability facts, persistent session snapshots, expiry and
   drift beyond the existing usage-audit evidence path.
2. P2 per-Agent mapping for real installed and authorised adapters.
3. Full Computer Access remains prohibited until a specific adapter can both apply and
   verify it under a separate security review.

**AGENT COMPUTER ACCESS RUNTIME P0 IMPLEMENTATION CLOSED**

**AGENT COMPUTER ACCESS RUNTIME P0 FINAL ACCEPTANCE REVIEW REQUIRED**

**READY FOR RD IMPLEMENTATION PLANNING**
