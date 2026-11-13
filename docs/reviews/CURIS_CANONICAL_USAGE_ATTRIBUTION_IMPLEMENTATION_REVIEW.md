# CURIS CANONICAL USAGE ATTRIBUTION IMPLEMENTATION REVIEW

Status: Review

Authority Class: REVIEW / EVIDENCE

Disposition: IMPLEMENTED / CEO REVIEW REQUIRED

Date: 2026-08-27

Issue: `issues/CURIS-CANONICAL-USAGE-ATTRIBUTION-001.md`

## Verdict

The bounded implementation is complete. One existing usage ledger now accepts either verified canonical `Company → Department → Business → Workspace → Work / Execution` ownership or verified legacy `Task → Project → Department` ownership. Project remains optional domain attribution for canonical Workspace execution; no default, synthetic or free-form Project was introduced.

## Runtime result

- `tasks` persists nullable `workspace_id`, `work_ref` and `execution_ref` beside the existing optional Project reference.
- `ai_usage_records` persists required Company ownership plus optional Business/Workspace/Work/Execution and Project dimensions under one immutable ledger.
- `AIUsageService` owns both attribution branches. `main.py` consumes its resolved snapshot and does not reconstruct a second ownership chain.
- Canonical execution rejects unresolved/quarantined parents, cross-tenant/company scope, wrong Business/Work, invalid Employee or capability binding, conflicting optional Project and non-unique execution provenance before Provider launch.
- Legacy RD remains `Task → Project → Department → Company`; Business metrics aggregate direct Company ownership and count canonical and legacy rows once.

## Migration evidence

- Fresh schema accepts complete canonical or legacy attribution and rejects incomplete ownership.
- Upgrade derives historical Company only through the recorded Project whose Department exists and belongs to the same Company.
- Unresolved history aborts atomically.
- Historical row values, idempotency keys, indexes and immutable triggers are preserved; migration is idempotent.
- No active database was migrated.

## Real Provider evidence

Repository-external evidence root: `/tmp/curis-canonical-usage-attribution.YtLWJY/live-codex/`.

- Provider: installed `/Users/yy/.local/bin/codex`, `codex-cli 0.144.6`.
- General Workspace Task used a canonical `WORK` and execution reference with `project_id = null`.
- HTTP result: `200`; ResultStore Task reached its real final state; exactly one Artifact and one canonical usage attempt were persisted.
- Usage ownership: Company, Department, Business, Workspace, Work, Execution, Employee, capability and Provider/model were all recorded; metering was confirmed with `22611` total tokens.
- Runtime restart reread the same canonical snapshot and usage count remained `1`.
- The real provider rejected the requested business outcome because available context lacked sufficient facts. Curis preserved that result as `WAITING`; it did not invent completion or business evidence.

## Failure and isolation evidence

- A failed Provider attempt records the same canonical ownership and failure truth without a fake Completed Result or Artifact.
- Cross-tenant, cross-Company, wrong Work, wrong Employee, wrong capability, conflicting Project and unresolved/quarantined Workspace scenarios reject before the Provider adapter is called.
- Duplicate/replay handling does not duplicate the usage attempt.

## Tests

- Canonical attribution, migration and legacy usage core: `21 passed`.
- Billing and business metrics compatibility: `33 passed`.
- RD persisted evidence, Phase 2B and real execution: `16 passed`.
- General Workspace, Team Operating and Responsibility Routing: `15 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.

Preserved unrelated fixture failures observed outside the bounded acceptance set were not changed: a missing `newapi` gateway fixture, an Employee capability-binding fixture that fails before usage attribution, and one Real RD executor fixture failure in its own file/test cycle.

## Changed files

Source:

- `backend/app/database.py`
- `backend/app/ai_usage.py`
- `backend/app/result_store.py`
- `backend/app/orchestrator.py`
- `backend/app/main.py` — bounded attribution and Team Task hunks only
- `backend/app/task_execution_control.py`
- `backend/app/business_metrics.py`

Tests:

- `backend/tests/test_canonical_usage_attribution.py`
- `backend/tests/test_database_canonical_usage_attribution_migration.py`
- `backend/tests/test_database_agent_type_migration.py` — fixture lineage only
- `backend/tests/test_phase8_billing_mvp.py` — fixture lineage only

## Active database safety

Both active databases remained byte-identical to preflight and returned `integrity_check = ok`:

| Path | Size | mtime | SHA-256 |
|---|---:|---:|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` |

## Remaining boundaries

- M2 usage-attribution architecture and execution blocker: CLOSED.
- General Workspace context assembly still needs to supply enough relevant business facts for useful provider outcomes; this is not an attribution failure.
- M3 native durable Keychain remains independently `SECURITY BLOCKED`.
- M4 RD canonical integration and M5 Content Growth headless were not started in this bounded Issue.
- No UI, Product Authority, active database, commit or push change was made.

## Next gate

CEO Implementation Review. Do not start M4/M5 from this Review alone.
