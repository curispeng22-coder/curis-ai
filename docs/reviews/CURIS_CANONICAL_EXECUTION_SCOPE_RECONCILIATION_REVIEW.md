# Canonical Execution Scope Reconciliation

Status: Review
Authority Class: REVIEW / IMPLEMENTATION EVIDENCE
Disposition: IMPLEMENTED / ACCEPTED CANDIDATE — four-scope infrastructure and Phase B integration verified
Owner: Main Development / Integration
Source: CEO 2026-09-09 scope correction; issues/CURIS-CANONICAL-EXECUTION-SCOPE-RECONCILIATION-001.md.
Next Action: CEO / ChatGPT final review; no further implementation or commit.

## Current continuation evidence — supersedes the checkpoint below

The existing resolver, Assignment authorization, Task identity/callback, Conversation context, Work adapter, ContextService, Result/Evidence references and sole Usage ledger now consume the same four-scope contract. Company identity does not grant unbounded context. Scoped calls validate the current persisted Assignment/Employee/revision; Work calls also validate the persisted execution claim (including a consultant distinct from the Holder). Broader scope has NULL workspace_id, not an overloaded or synthetic ID.

|System|COMPANY|DEPARTMENT|BUSINESS|WORKSPACE|
|---|---|---|---|---|
|Assignment|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Conversation|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Work|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Execution|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Context|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Result|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Evidence|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Usage|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|
|Authorization|SUPPORTED|SUPPORTED|SUPPORTED|SUPPORTED|

Meaning: canonical data/execution infrastructure, NOT complete autonomous products at all levels or live-cloud quality acceptance. Controlled HTTP executes through the actual ModelGatewayAdapter, Orchestrator, persisted Task/identity/callback and one ledger. No deterministic response is labeled external cloud evidence.

Evidence: test_canonical_execution_scope.py **40 passed** (12.29s), including all four scopes' successful and failed Conversation/Work calls; persistent Result/artifact hashes, scoped Evidence references; no fake Project; Company/Department Work with no Business/Workspace; Business Work without Workspace; restart/replay without new calls; Assignment tenant/Company/Employee/revision/sibling rejection. Result/Evidence source provenance is retained; provider cost remains NULL/unknown. Selected context is bounded, unrelated Memory history is not automatically loaded. Existing Knowledge scopes remain unchanged.

Handoff ACK verification covers all four scopes, restart, wrong recipient and scope mismatch. It checks the actual Handoff toEmployeeRef as well as Task/Cycle/projection identity. This does not create a new Handoff system. General Workspace assignment now accepts the same canonical Company Employee (NULL workspace) without moving or cloning it; replay/restart preserve identity. Historical Employees explicitly restricted to another Workspace still fail closed.

Migration: nullable Task scope fields and transactional rebuild of the same ai_usage_records ledger. Historical legacy Project, Workspace Work and Conversation rows retain every old column value and NULL new scope; indexes, triggers, unique constraints and immutable semantics survive. Injected DROP denial rolls back table swap and temporary table; repeat migration is idempotent. No guessed historical lineage. Existing migrations' historical fixtures are pinned to their original schema step rather than weakened.

Final expanded regression **120 passed** (45.43s): scope, child Work/multi-Work, routing, Team real employee adapter, identity, Usage/migration/Conversation, DB safety, General lifecycle, RD P7, XHS, Package P0/P1/P1.5/v2, Meeting core and built-in organization. Prior Knowledge/Attention coverage remains recorded in the earlier 97-test run; these counts are separate runs, not additive unique coverage. Historical Workspace/RD semantics retained. Native fresh Company no-key Department delegation and normal canonical Business activation passed after this infrastructure closure; native no-key Work correctly remains PLANNED. Complete evidence and all three unchanged protected fingerprints are in `CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md`.

No protected DB migration; final size/mtime/SHA-256 identical, integrity ok. No fake Workspace/Business/Project, second ledger, per-scope Runtime or stage/commit/push. Four-scope infrastructure support is not acceptance of Company/Department/Business autonomous operating quality. Next gate is CEO / ChatGPT review of the completed candidate, not the old Department architecture decision.

## Historical checkpoint provenance — no longer Current gaps

## Historical checkpoint changes

- Reused ResourceScopePolicy rather than a second Runtime. One table-driven COMPANY → DEPARTMENT → BUSINESS → WORKSPACE lineage vocabulary resolves real rows within tenant/Company. Missing, archived Business, deleted Department, unresolved Workspace, wrong parents and conflicting persisted representations fail closed.
- Existing path_is_owned/owns interfaces preserved. Resolving ownership is explicitly NOT an actor grant. Exact scope comparison is available; full Assignment/actor authorization consumption remains incomplete.
- ResponsibilityRouting scope validator consumes the resolver and accepts COMPANY as well as the existing three scopes. Workspace-restricted Employee/Role/Capability cannot silently escape into broader scope through a NULL workspace argument.
- Existing CanonicalChildWorkRuntime creates scoped Cycle/Work in one transaction, retains the historical Workspace release-ID algorithm, and stores explicit scope in existing Runtime JSON. Four-scope create/retry/restart tests pass. No new Work table or system. These are creation/persistence proofs, not Provider execution proofs.
- Existing tasks gains nullable scope_type/scope_ref atomically in a savepoint. No historical backfill, no table rewrite or additional truth store. ResultStore validates explicit Task scope and canonical Work identity before insertion. Historical Project/Workspace fields remain unchanged.
- Non-Workspace Work completion cannot accept a same-Company-only Task as proof. ResultStore artifacts still belong to their Task; broader Result/Evidence acceptance requires further integration.
- AIUsageService rejects explicit non-Workspace Task scope before it could fall into legacy Project attribution. This is a safety boundary during incomplete implementation, NOT completion of the requested scope reconciliation.

## Historical checkpoint remaining implementation

1. ai_usage_records still has Department NOT NULL and a canonical CHECK requiring Business + Workspace. Reconcile that existing ledger schema atomically, preserve all rows/indexes/triggers/idempotency, and extend its sole resolver. No per-scope ledger.
2. EmployeeExecutionIdentity still requires workspace_id in identity/callback/ACK queries. Separate Company Employee identity from execution scope; current Assignment, Task and callback must agree, including replay/restart and legacy compatibility.
3. ConversationService.context still rejects Department/Business/Company Assignment without Workspace. Reuse the persistent owner; validate per-message current scope and selected references, never widen Conversation identity into unlimited context access.
4. Team execution adapter, ContextService, orchestration and result/evidence propagation must consume the same resolved scope. Mere nullable fields are not execution authorization.
5. Complete each four-scope end-to-end path and negative cross-scope tests before claiming SUPPORTED throughout. No real Provider was launched here.
6. Phase B B–E/integrated Browser/Desktop remain unfinished. Existing bootstrap/UI changes are preserved; no further UI changes made in this scope checkpoint.

These are unfinished engineering work under the current authorization, not new architecture decisions and not a claim that only Department requires a special runtime.

## Historical checkpoint Scope Support Matrix — not final acceptance

SUPPORTED below refers to the existing Workspace baseline retained by regression, not a new full-stack certification. PARTIAL identifies concrete implemented pieces with incomplete end-to-end scope propagation. FAIL identifies a current explicit gate for this execution scope. No row implies autonomous operating product acceptance at Company/Department/Business level.

|System|COMPANY|DEPARTMENT|BUSINESS|WORKSPACE|
|---|---|---|---|---|
|Assignment|PARTIAL|PARTIAL|PARTIAL|SUPPORTED|
|Conversation|FAIL|FAIL|FAIL|SUPPORTED|
|Work|PARTIAL|PARTIAL|PARTIAL|SUPPORTED|
|Execution|FAIL|FAIL|FAIL|SUPPORTED|
|Context|FAIL|FAIL|FAIL|SUPPORTED|
|Result|PARTIAL|PARTIAL|PARTIAL|SUPPORTED|
|Evidence|PARTIAL|PARTIAL|PARTIAL|SUPPORTED|
|Usage|FAIL|FAIL|FAIL|SUPPORTED|
|Authorization|PARTIAL|PARTIAL|PARTIAL|SUPPORTED|

Conversation row is Employee execution-context support, not denial of the existing Company CEO Assistant holder. Result/Evidence partial means the existing holders and Task/Work provenance are reusable; no new non-Workspace completed Result or verified Evidence has been claimed. Assignment partial reflects resolver/creation support without full downstream authorization proof.

## Historical checkpoint evidence

Repository-external isolated three-variable DB guard, no protected DB imports/initialization. Latest combined command: **74 passed**, 21615 existing warnings, 22.16 s.

Files run:

- backend/tests/test_canonical_execution_scope.py (18 checks)
- backend/tests/test_canonical_child_work_foundation.py
- backend/tests/test_autonomous_cross_surface_multi_work_runtime_proof.py
- backend/tests/test_responsibility_routing_runtime.py
- backend/tests/test_team_operating_adapter.py
- backend/tests/test_team_operating_real_employee_e2e.py
- backend/tests/test_employee_execution_identity.py
- backend/tests/test_canonical_usage_attribution.py
- backend/tests/test_conversation_usage.py
- backend/tests/test_database_canonical_usage_attribution_migration.py
- backend/tests/test_backend_test_db_safety.py
- backend/tests/test_phase_b_builtin_organization.py
- backend/tests/test_v1_general_workspace_lifecycle_closure.py

Python compile of six changed app modules plus new test: PASS. git diff --check: PASS. No Browser/build/package/Provider claim for this checkpoint.

Task migration tests prove exact preservation of old Task columns, Task indexes/triggers, repeated migration, and rollback when second-column creation fails. Initial broad Database.initialize comparison exposed its pre-existing execution_state_changed_at initialization for NULL historical metadata. The test now isolates the new migration itself; it does NOT claim all pre-existing initializer behavior is byte-neutral. The pending ledger migration requires its own full evidence.

## Historical checkpoint protected DB evidence

Before/after size, mtime_ns and SHA-256 all identical; integrity_check=ok for each:

|Path|Bytes|mtime_ns|SHA-256|
|---|---:|---:|---|
|data/curis.sqlite|1232896|1786873339955841838|2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6|
|backend/data/curis.sqlite|1277952|1786783659967572836|a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4|
|/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite|1536000|1788614881473263746|d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617|

No protected DB migration, App launch, credential operation, stage, commit, push, reset, clean or stash. Prior Phase B and unrelated worktree changes preserved.

## Historical checkpoint verdict

CANONICAL EXECUTION SCOPE RECONCILIATION: IN PROGRESS / NOT ACCEPTED.
Unified data/resolver foundation has progressed; unified execution trust/ledger/context closure is still incomplete. FINAL UI MASTER remains PAUSED. RELEASE remains BLOCKED.
