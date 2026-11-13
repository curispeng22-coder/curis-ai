# CURIS CANONICAL CHILD WORK FOUNDATION 001

Authority Class: CURRENT
Status: Frozen
Disposition: IMPLEMENTED / ACCEPTED
Date: 2026-08-21
Owner: Main Developer / Shared Runtime

## Exact Objective

Establish the smallest shared canonical child Work foundation so one existing Cycle
can own multiple distinct Work identities with Work-scoped Responsibility, Assignment,
holder, Result, Artifact, Evidence and Acceptance truth; atomically release exactly
one next Work through the existing Handoff lifecycle; aggregate complete child Work
truth into the existing Cycle close/evaluation path; and preserve legacy
`cycle_id as work_ref` behavior when no child Work exists.

## Current Blocker Evidence

- `AutonomousOperatingControl.materialize_cycle_work()` currently calls
  `ResponsibilityRoutingRuntime.start_work(cycle_id, ...)`.
- `ResponsibilityRoutingRuntime.start_work()` writes one routing record onto the
  supplied entity and replay returns that same entity.
- Existing Handoff changes responsibility on that same `workRef`; it does not create
  a successor Work.
- Existing Cycle close/evaluation reads one flat routing/Cycle Result and Evidence
  projection and cannot validate per-Work completeness.

## Exact Allowed Files

1. `backend/app/runtime/child_work.py` — new shared child Work identity, lifecycle,
   Work-scoped outcome, atomic Handoff/release and aggregation.
2. `backend/app/runtime/autonomous_operating.py` — bounded child-Work-aware Cycle
   close/evaluation branch with unchanged legacy fallback.
3. `backend/tests/test_canonical_child_work_foundation.py` — isolated persistence,
   concurrency, restart, failure, aggregation and compatibility proof.
4. `issues/20260821_canonical_child_work_foundation_001.md` — this Issue.
5. `docs/reviews/CURIS_CANONICAL_CHILD_WORK_FOUNDATION_REVIEW.md` — evidence record.

No other source, schema, API, frontend, Package, domain or database file is allowed.

## Pre-change Ownership

- `backend/app/runtime/autonomous_operating.py`
  - SHA-256: `6b79c731b43b691c4b21383d2167e515c83774ff405f9425b1f0f3359a51d3cd`
  - clean at Issue entry;
  - owned future hunk: child Work aggregation only.
- `backend/app/runtime/responsibility_routing.py` is pre-existing mixed/dirty and is
  explicitly excluded.
- `backend/app/database.py` is pre-existing mixed/dirty and is explicitly excluded.

## Work Identity Strategy

- one shared `entity_type='WORK'` row in existing `runtime_entities`;
- stable deterministic `work_id` from tenant + parent Cycle + release identity;
- `parent_id` is exactly one canonical Cycle;
- no Surface, Domain, Autonomous V2 or Package identity participates;
- replay with the same identity returns the same Work; conflicting replay fails.

## Persistence Feasibility

Existing generic persistence is sufficient:

- `runtime_entities.entity_id` is a primary key;
- tenant/company/workspace/parent scope is stored on each Work;
- `runtime_links` has unique `(tenant_id, source_id, relation, target_id)`;
- deterministic IDs plus `BEGIN IMMEDIATE` serialize concurrent release;
- no table, index or migration is required.

## Cycle → Work Relation

- Work row: `parent_id=<cycle_id>`;
- Cycle link: `Cycle -HAS_WORK→ Work`;
- successor lineage: `Work A -HAS_SUCCESSOR_WORK→ Work B` and reverse predecessor
  link;
- a Work has at most one sequential successor in this bounded foundation.

## Work Lifecycle

Minimal existing vocabulary:

`PLANNED → READY → ACTIVE → COMPLETED | FAILED | CANCELLED`

`ACTIVE ↔ WAITING | BLOCKED`, with terminal states immutable. Lifecycle changes use
guarded compare-and-update plus existing transition-log persistence; no new engine.

## Responsibility / Assignment Binding

Creation validates one existing Workspace-scoped `RESPONSIBILITY_ASSIGNMENT`, its
canonical Employee holder, Company/Workspace scope and Employee availability. Work
stores an immutable Assignment snapshot/ref and holder ref. The same Employee may
hold multiple Work through distinct valid Assignments without identity duplication.

## Result / Evidence / Acceptance Ownership

Completion requires Work-scoped, independently validated refs:

- completed ResultStore Task refs;
- Artifacts owned by those Tasks;
- verified/current `EVIDENCE` rows parented to the Work;
- closed `ACCEPTANCE` rows parented to the Work and covering the same refs.

The Work stores these refs before becoming `COMPLETED`. Terminal output/context is
not rewritten by successor release.

## Deterministic Release Identity

`release_key` is scoped to parent Work. Deterministic Handoff and successor Work IDs
derive from tenant + parent Work + release key. Same replay returns the same pair;
same release key with another target or context fails closed.

## Handoff → Next Work Transaction

One `BEGIN IMMEDIATE` transaction validates completed Work A and target Assignment,
persists one existing-type `HANDOFF` through CREATED/SENT/ACKNOWLEDGED/COMPLETED,
creates Work B, creates all Cycle/lineage/release links, and commits together.
Provider callback, UI, Surface and scheduler cannot independently release Work.

## Restart / Replay

Rows and links are canonical SQLite truth. Restart reconstructs Work and lineage from
the same database. Replays and concurrent requests use deterministic IDs and compare
canonical payloads; partial Handoff/Work pairs fail closed.

## Evaluation Aggregation

When a Cycle has child Work, close/evaluation aggregates each required Work's own
Result/Artifact/Evidence/Acceptance refs and persists Work summaries/provenance on
Cycle evidence/evaluation. Missing, failed or incomplete required Work fails closed.
When no child Work exists, the accepted legacy flat Cycle path is unchanged.

## Migration Strategy

No migration and no historical rewrite. Existing Cycles with no `WORK` child continue
through the legacy cycle-as-work path. Only explicitly created new child Work uses the
new branch.

## Active DB Guard

All tests set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one
repository-external isolated SQLite before import. Repository active databases are
fingerprinted before/after and must not initialize, migrate or change.

## Explicit Exclusions

- no Surface identity/runtime, Package v2, UI or API;
- no domain-specific Work type;
- no Workflow/DAG/scheduler, parallel/fan-out/join;
- no provider execution expansion;
- no successor Cycle or Learning;
- no schema/table/index/migration;
- no change to mixed `responsibility_routing.py` or `database.py`;
- no stage, commit or push.

## Stop Gates

Stop if generic rows/links cannot guarantee identity/lineage, if release cannot be one
transaction, if legacy Autonomous V1 regresses, if Evaluation loses Work provenance,
or if any schema, Surface, Package, DAG, active DB or mixed-source modification becomes
necessary.

## Implementation Result

Implemented within the exact Allowed Files without schema, API, UI, Surface,
Package, scheduler or provider-execution changes. Focused proof: 5 passed. Existing
Autonomous/Responsibility/Team Operating regression: 73 passed. Active database
fingerprints remained byte-identical. No file was staged, committed or pushed.
