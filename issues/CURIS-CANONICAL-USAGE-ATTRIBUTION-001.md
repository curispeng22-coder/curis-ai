# CURIS-CANONICAL-USAGE-ATTRIBUTION-001

Status: Review

Authority Class: CURRENT

Implementation State: IMPLEMENTED / CEO REVIEW REQUIRED

Baseline: `main @ c797db840bad285d7e9f1962d06eac61aa28508b`

Updated: 2026-08-27

Owner: Main Development / Runtime Integration

## Goal

Remove the shared M2 execution blocker by extending the one existing Usage ledger to accept a verified canonical `Company → Department → Business → Workspace → Work / Execution` lineage while preserving verified legacy `Task → Project → Department` attribution. No synthetic/default Project is permitted.

## Authority

- `docs/reviews/CURIS_CANONICAL_USAGE_ATTRIBUTION_ARCHITECTURE_REVIEW.md` — accepted by CEO/Architecture for bounded implementation.
- `docs/00_Context/CURRENT_STATE.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md` — M2 architecture stop gate.
- Current canonical Business Spine and Team Operating Runtime truth.

## Exact Allowed Files

### Source

- `backend/app/database.py`
- `backend/app/ai_usage.py`
- `backend/app/result_store.py`
- `backend/app/orchestrator.py`
- `backend/app/main.py` — only `execute_model_gateway()/execute_attempt()` attribution and `team_employee:auto` Task creation hunks
- `backend/app/task_execution_control.py`
- `backend/app/business_metrics.py`

### Tests

- `backend/tests/test_canonical_usage_attribution.py` — new focused Runtime/lineage tests
- `backend/tests/test_database_canonical_usage_attribution_migration.py` — new fresh/upgrade/atomic migration tests
- `backend/tests/test_database_agent_type_migration.py` — compatibility fixture only: add the Project lineage now required for its historical usage row
- `backend/tests/test_phase8_billing_mvp.py` — compatibility fixture only: make direct ledger fixtures carry a real legacy Company/Project lineage

Existing regression tests are execution-only unless a failing assertion proves a required compatibility update. The agent-type migration fixture is amended because its historical usage row previously named a nonexistent Project; production behavior must now reject that impossible lineage.

### Issue / Review / accepted state

- `issues/CURIS-CANONICAL-USAGE-ATTRIBUTION-001.md`
- `docs/reviews/CURIS_CANONICAL_USAGE_ATTRIBUTION_IMPLEMENTATION_REVIEW.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md` — M2 status only after acceptance
- `docs/reviews/CURIS_V1_UI_INDEPENDENT_DELIVERY_REPORT.md` — M2 status only after acceptance
- `docs/00_Context/CURRENT_STATE.md` — implementation truth only after acceptance

## Exact migration scope

1. Add nullable `workspace_id`, `work_ref`, `execution_ref` to `tasks`.
2. Rebuild `ai_usage_records` transactionally so:
   - `company_id` is present and required for new rows;
   - `project_id` is nullable;
   - canonical `business_id`, `workspace_id`, `work_ref`, `execution_ref` snapshots are available;
   - each row has either complete canonical attribution or a Project compatibility attribution;
   - historical Company is backfilled only through the recorded Project relation;
   - historical Business/Workspace/Work/Execution remain null;
   - all historical rows, values, idempotency keys, indexes and immutability triggers are preserved.
3. Abort atomically if any historical row cannot resolve Company from its recorded Project lineage.
4. No active database migration is authorized; all migration evidence uses repository-external isolated SQLite.

## Pre-change hashes and ownership

Captured before source edits:

| Path | Working-copy SHA-256 | Pre-existing state | Owned implementation boundary |
|---|---|---|---|
| `backend/app/database.py` | `90327bbe41aba54460ce8c8599f0960ffaed49302ec2d714c1430a6e15271b93` | modified, unrelated capability/strategy/talent deltas | Task schema, usage schema/migration only; preserve all unrelated hunks |
| `backend/app/ai_usage.py` | `14f0a86379a5575b41540a8ddcbcc06518f85207dd24f666bc4b898e3bd72873` | clean | canonical/legacy resolver, ledger write/read only |
| `backend/app/result_store.py` | `ebdd98f6dd2cb1ba5e5075f718ba7ecfc9f2ff4250684ac36e7c366802c401e8` | clean | Task canonical refs and existing usage-event payloads only |
| `backend/app/orchestrator.py` | `44ec12d9112550248cb9c802c7d7bb619c86203d525367e54637cf29f2b22921` | clean | RuntimeCapabilityContext canonical refs only |
| `backend/app/main.py` | `7186d132695296ccd0a1c527d20d2151b268f2750bd3d5236b3b7d3a6ee1947f` | modified, multiple unrelated initiatives; model-gateway trace delta intersects the same function | exact attribution resolution/record payload and Team Operating Task creation only; preserve current trace/provider/talent/meeting hunks |
| `backend/app/task_execution_control.py` | `b0883f5273321383be1789bd13b7fa10d548e3d187c9e7a3aa0a6acc12f9ebd2` | clean | canonical timeline refs only |
| `backend/app/business_metrics.py` | `ea8187486a4b29157bcf8aa20b458d49de15537153e2e169806edf47639527d9` | clean | Company usage aggregation only |

`database.py` and `main.py` are preserved mixed-source files. Changes must be exact-context patches. Any inability to separate the named semantic block is an ownership Stop Gate.

## Isolated database

All implementation tests set all three variables to one repository-external path under:

`/tmp/curis-canonical-usage-attribution.YtLWJY/`

- `CURIS_DB`
- `CURIS_DB_PATH`
- `CURIS_WORKSPACE_DB`

The Backend Test DB Safety guard must fail before initialization if this contract is not met.

## Active database baseline

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

## Acceptance tests

1. Fresh schema supports canonical and legacy attribution without a second ledger.
2. Upgrade preserves every historical row/value/idempotency key/index/immutability trigger.
3. Unresolvable historical Project ownership aborts atomically.
4. General Workspace Task persists Workspace/Work/Execution and has no Project.
5. Canonical resolver verifies Workspace → Business → Department → Company, Work, Employee assignment provenance and Capability Binding.
6. Success and failed Provider attempts record canonical attribution; failure does not create fake completed Result.
7. Restart reconstructs and revalidates the same Task attribution.
8. Replay/idempotency does not duplicate attempts or usage.
9. Cross-tenant, cross-Company, wrong Business/Work, invalid Employee/Capability and conflicting Project reject before Provider launch.
10. Existing RD real Codex, Workflow, Project task-job, AI usage, billing, business metrics and task timeline regressions pass.
11. Company metrics include legacy and canonical usage exactly once.
12. Existing usage filters remain compatible; canonical filters expose the new dimensions.
13. Active SQLite fingerprints and integrity remain unchanged.
14. One real General Workspace Provider proof runs without Project and reaches real Result/Artifact/Evidence/usage attribution.

## Rollback and Stop Conditions

Stop before continuing if any of the following occurs:

- any active SQLite write or fingerprint drift;
- any historical usage row cannot resolve Company from its recorded Project;
- migration loses or changes a historical value, index, trigger or idempotency key;
- canonical Parent Resolver is ambiguous, unresolved or quarantined;
- Provider could launch before full canonical validation;
- required implementation touches a file outside this manifest;
- `database.py` or `main.py` ownership cannot be separated from unrelated hunks;
- accepted RD Project attribution regresses;
- a second Usage/Cost/Audit system or synthetic Project appears necessary.

Rollback for isolated migration/test failure is deletion of the disposable repository-external test database only. No active database repair, rewrite, restore or cleanup is authorized.

## Explicit exclusions

No M3 Keychain, UI, Content Growth, RD redesign, Workflow/DAG, tool-cost expansion, Product Authority change, active DB work, unrelated cleanup, commit, or push.

## Next Gate

Implementation Review must present migration evidence, canonical/legacy Runtime evidence, real Provider proof, restart/failure/isolation evidence, RD no-regression, active DB safety, changed files and remaining non-architecture gaps.

## Implementation Result

- The existing Task and `ai_usage_records` contracts now carry verified canonical Workspace/Work/Execution attribution without creating a second ledger or synthetic Project.
- `AIUsageService` is the single canonical/legacy resolver. Canonical validation covers Workspace → Business → Department → Company, Work scope, Employee assignment provenance, capability binding and execution identity before Provider launch.
- Legacy RD Project attribution remains supported; Project is optional only for canonical Workspace execution.
- Historical migration is transactional, preserves rows/indexes/triggers/idempotency, and aborts when the recorded Project → Department → Company lineage is not provable.
- A real installed Codex provider ran from a General Workspace with `project_id = null`; canonical usage, Result, Artifact and Evidence were persisted and reread after restart.
- The provider truthfully returned a rejected business result because the supplied Work context lacked sufficient business facts. The Work remained `WAITING`; no fake Completed result was created. This is a separate General Workspace context-assembly gap, not an attribution blocker.
- Formal evidence: `docs/reviews/CURIS_CANONICAL_USAGE_ATTRIBUTION_IMPLEMENTATION_REVIEW.md`.
