# RD-PHASE-2B-ARTIFACT-REVIEW-001 Review

**Status:** IMPLEMENTED / ACCEPTED WITH RECORDED ACTIVE-DB INCIDENT
**Date:** 2026-08-16
**Issue:** `issues/RD-PHASE-2B-ARTIFACT-REVIEW-001.md`

## Review boundary

This Review accepts only a two-Employee Artifact Review Request on one existing RD Cycle.
Review is not Handoff and not P7. Handoff and Decision counts must both remain zero.

## Baseline protection

- Mixed-source hashes and owned hunks are recorded in the Issue before source edits.
- Active database baseline is recorded and must remain unchanged.
- No source file may be replaced wholesale or staged with unrelated mixed hunks.

## Evidence ledger

### Bounded implementation

- Cycle-scoped `artifactReview` request; no new Runtime entity/table/state machine.
- Developer Cycle Responsibility Holder is unchanged before, during and after review.
- Reviewer is a distinct persisted Workspace `AI_EMPLOYEE` with a real role capability.
- Reviewer execution uses the accepted Agent/Task/ResultStore/Codex path.
- Review output is stored as an `artifact_review` Artifact plus Runtime Evidence and Result
  References; Conversation only links/summarizes the result.
- Reviewer source-file mutation is fail-closed; no auto-fix is permitted.
- No `HANDOFF`, `DECISION_PACKET` or `ACCEPTANCE` is created by this branch.

### Real Codex vertical evidence

Fresh root and SQLite:

```text
/tmp/curis-rd-artifact-review-live.vBw8xG
/tmp/curis-rd-artifact-review-live.vBw8xG/runtime.sqlite
```

Observed through the real `create_app` Runtime/API path:

```text
Company: company-112e2f8d-928c-4700-9aab-1500aa7d37d6
Workspace: workspace-dfae08dd-936b-4321-9c12-7bd8fb1fd708
Cycle: cycle-77137d99-7467-433e-9e70-ce7a656ced03
Primary Task: 9003570a-6c05-4061-b04c-5d01ba883d2d = COMPLETED
Review Request: artifact-review-8fb7da51-cf3d-4874-ade5-1daa9355a5ee
Review Task: 115fa1b6-325a-4006-83f7-e3cefd775885 = COMPLETED
Review Session: 01a009fa-aadf-76a2-a539-c3ce5106296d
Review Result: APPROVED
Review Result refs: 3
Review Artifacts: execution_result, artifact_review
Review Current Executor after completion: none
Handoff count: 0
Decision Packet count: 0
```

The primary Codex Task changed the isolated `calc.py` from subtraction to addition and
`python3 -m unittest -q` passed. The second Codex Task reviewed that persisted Artifact and
did not change declared source files.

Computer Access remained truthful:

```text
requested_intent = AUTO_WITHIN_BOUNDARY
native sandbox = workspace-write
configured_state = CONFIGURED
effective_state = UNKNOWN
verification_state = UNVERIFIED
```

### Persistence, failure and idempotency

- A second `create_app` over the same isolated SQLite recovered both Employees, the same
  Cycle, Request, reviewer Task, Result refs and terminal `APPROVED` state.
- Both Cycle and Review Current Executor recovered as inactive (`none`).
- Deterministic focused tests cover `APPROVED`, `CHANGES_REQUESTED`, `FAILED`, duplicate
  active execution and interrupted-review restart fail-closed behavior.
- Duplicate active execution returns the existing `REVIEWING` record and starts no second
  executor call.

### Tests

Valid isolated backend invocation set all three DB variables before Python/pytest import:

```text
13 passed
  backend/tests/test_rd_artifact_review.py
  backend/tests/test_rd_workspace_real_execution.py
  backend/tests/test_xhs_calendar_note_runtime.py
  backend/tests/test_runtime_foundation_state_contracts.py
```

Frontend/source contracts:

```text
13 passed
  frontend/tests/rdArtifactReview.test.mjs
  frontend/tests/rdWorkspaceExecution.test.mjs
  frontend/tests/runtimeWorkspaceUi.test.mjs
```

Frontend production build:

```text
Next.js build: PASS, 45 pages generated
```

`python -m py_compile` and `git diff --check` also passed for the bounded files.

### No-regression

- Accepted primary RD execution and long-running accepted-submit projection tests pass.
- XHS calendar/note Runtime and shared Workspace UI tests pass.
- Computer Access remains requested/configured/effective separated; no Full Access path was
  added.
- Existing `frontend/tests/rdWorkspaceExecution.test.mjs` returned to its exact pre-change
  SHA-256; no no-regression test was rewritten to hide drift.

## Active database provenance audit

The first no-regression pytest command was launched without setting `CURIS_DB`,
`CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` at process start. Collection imported
`app.main`, whose module-level `create_app()` initialized `data/curis.sqlite`.

Observed baseline and incident:

```text
pre-change size/mtime: 1232896 / 1786871647 (2026-08-16 17:14:07 +0800)
post-incident size/mtime: 1232896 / 1786873339 (2026-08-16 17:42:19 +0800)
post-incident SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
SQLite quick_check: ok
companies: 0
runtime_entities: 0
```

The original pre-incident byte SHA was not captured. This Review therefore does not claim
byte-for-byte unchanged. The accepted post-incident read-only fact is:

```text
path: /Users/yy/Documents/Curis AI Workspace/data/curis.sqlite
size: 1232896
mtime_ns: 1786873339955841838
SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
application_id: 0
auto_vacuum: 0
encoding: UTF-8
foreign_keys (read-only audit connection): 0
freelist_count: 0
page_count: 301
page_size: 4096
schema_version: 246
secure_delete: 0
user_version: 1
user tables: 99
schema objects: 151
schema SHA-256: 9dc0259a0184183478e1975bae42896cf83cfc502ce8ecb23500e1e97110e1b7
quick_check: ok
integrity_check: ok
foreign_key_check: empty
```

### Complete user-table row inventory

```text
ai_usage_records=0, architecture_locks=0, artifacts=0, assistant_identities=0,
attributions=0, auto_workflows=0, billing_events=0, business_directions=0,
business_metrics=0, cadences=0, capability_lessons=0, capability_packages=1,
commitments=0, companies=0, company_department_state=0,
company_package_workflow_bridges=1, company_packages=1, company_templates=1,
content_publish_packages=0, content_workflow_runs=0, context_packages=0,
credential_metadata=0, d1_execution_log=0, dashboard_templates=9,
dashboard_widget_catalog=16, department_instances=0, department_observations=0,
department_templates=3, department_type_status=0, department_types=7,
departments=0, development_strategies=0, employee_affiliations=0,
employee_capabilities=0, employee_capability_bindings=0, employee_instances=0,
employee_skill_bindings=0, employee_templates=13, evolution_decisions=0,
evolution_events=0, evolution_simulations=0, execution_patterns=0,
execution_scores=0, executions=0, failure_logs=0, governance_proposals=0,
guide_sessions=0, installed_workspace_packages=0, knowledge_entries=0,
memory_entries=0, meta_development_reports=0, model_gateways=2,
official_models=1, outcomes=0, persona_templates=6, plans=3,
platform_policies=0, pricing_rules=2, projects=0, quota_rules=15, quotas=0,
rollback_records=0, runtime_entities=0, runtime_links=0,
runtime_simulation_runs=0, runtime_trace_event=0, runtime_transition_log=77,
runtime_workspace_versions=0, scheduled_runs=0, schema_migrations=2,
skill_templates=55, step_assignments=0, step_results=0, strategy_meetings=0,
system_evolution_log=0, system_settings=0, tasks=0,
template_version_snapshots=0, tenant_department_activations=0,
tenant_memberships=0, tenant_model_preferences=0,
tenant_private_capabilities=0, tenants=1, tool_performance=0,
tool_templates=115, tool_traces=0, tools=5, workflow_contents=36,
workflow_instances=0, workflow_metrics=0, workflow_runs=0, workflow_steps=0,
workflow_templates=18, workflow_traces=0, workflows=0,
workspace_package_activities=0, workspace_package_instances=0,
workspace_package_objects=0, workspaces=0
```

The nonzero catalog, seed and transition rows predate this incident. In particular,
`runtime_transition_log` contains 77 fixture/history transitions dated 2026-08-09 with no
Company or Workspace scope; no new business object was found.

### Initialization-path attribution

`app.main` owns a module-level `app = create_app()`. Importing it without explicit test DB
variables calls `Database.initialize()`, which applies `CREATE TABLE IF NOT EXISTS`,
additive schema initialization and canonical seed upserts before router construction. With
no `CURIS_PRODUCT` set, product-private pruning and R3 model-catalog seeding do not run;
default tool and quick-start seed registration can still refresh canonical metadata.

Direct logical comparison with
`data/backups/curis-before-workspace-p0-guard-repair-20260816.sqlite` proved:

- all 145 non-Package schema objects are exactly equal;
- the four Package P0 tables and their indexes have exactly the expected DDL and zero rows;
- all non-target row values are equal except `updated_at` on 2 plan rows and 18 workflow
  template rows, refreshed from `2026-08-16 09:07:57` to
  `2026-08-16 09:42:19`;
- Company, Workspace, Employee, Responsibility, Task, Execution, Artifact, Evidence,
  Result, XHS/RD Runtime and Package-instance tables all contain zero rows.

This proves the event was schema initialization plus canonical seed-metadata timestamp
refresh, not a business-data mutation. No backup was restored.

Formal classification:

`ACTIVE DB EMPTY-INITIALIZATION INCIDENT — OWNER ACCEPTED`

### Permanent regression guard

`backend/tests/conftest.py` now invokes the existing
`workspace_package_p0_db_guard.py` before test-module import. Collection requires
`CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB`, requires all three to resolve to the
same path, and rejects the repository active database.

Guard evidence:

```text
missing variables -> collection fails before app import
three variables = data/curis.sqlite -> collection fails before app import
fresh /tmp path -> collection and tests proceed
```

The active database SHA/size/mtime stayed at the accepted post-incident values throughout
these guard checks and the final isolated regression.

### Final isolated regression

Fresh SQLite:

`/tmp/curis-rd-artifact-review-acceptance.iEXxeY/runtime.sqlite`

```text
backend: 13 passed
frontend: 13 passed
git diff --check: pass
```

The backend set covers Artifact Review, accepted RD execution, XHS Calendar/Note and shared
Runtime state contracts. The frontend set covers Artifact Review, accepted RD Workspace
execution and shared Workspace UI.

## Commit boundary

The accepted implementation runs on the formally preserved mixed Shared Runtime baseline.
`backend/app/runtime/workspace.py`, `backend/app/api/runtime_foundation_router.py`,
`backend/app/main.py`, `frontend/components/rd/RdWorkspacePhaseTwo.js` and
`frontend/lib/runtimeApi.js` contain recorded Issue-owned hunks but are not safe whole-file
commit candidates: several are absent from historical `HEAD`, and each also carries prior
accepted RD/XHS/shared work. Staging them wholesale would absorb that baseline and violate
its preservation rule.

The bounded acceptance commit therefore contains only independently owned Artifact Review
files, the one tracked pytest guard hunk, and this Issue/Review. It is an ordered integration
commit against the preserved development baseline, not a standalone cherry-pick onto clean
historical `HEAD`. No unrelated mixed-source file is staged or normalized to manufacture a
false commit boundary.

## Acceptance decision

`IMPLEMENTED / ACCEPTED WITH RECORDED ACTIVE-DB INCIDENT`

The code/runtime acceptance conditions and the isolated no-regression checks are satisfied.
The incident is accepted as an empty initialization/metadata-touch event, with no claim of
byte-for-byte unchanged and no backup restoration. Review remains bounded to Artifact
Review: Handoff count is zero, Decision Packet count is zero, and no shared Runtime
primitive was added.
