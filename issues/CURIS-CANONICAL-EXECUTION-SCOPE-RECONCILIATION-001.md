# Canonical Execution Scope Reconciliation

Status: Review
Authority Class: CURRENT / IMPLEMENTATION ISSUE
Disposition: IMPLEMENTED / ACCEPTED CANDIDATE — pending CEO / ChatGPT review
Owner: Main Development / Integration
Source: CEO Canonical Execution Scope Reconciliation correction, 2026-09-09.

## Contract and dependency

Final evidence: `docs/reviews/CURIS_CANONICAL_EXECUTION_SCOPE_RECONCILIATION_REVIEW.md` contains the complete 9×4 support matrix. Scope-focused 40 PASS, final expanded 120 PASS, migration rollback/idempotency, ACK recipient/scope validation and General Workspace same-Employee reuse verified. Phase B A–E integration, Browser, fresh packaged Desktop and restart completed; all three protected DB fingerprints unchanged. No higher-level autonomous product/cloud quality claim. No stage/commit/push. Historical checkpoints below remain provenance only.

One execution ownership vocabulary: COMPANY, DEPARTMENT, BUSINESS, WORKSPACE, with scope_type and scope_ref. Existing camel-case Runtime JSON equivalents remain compatible. Workspace is not a mandatory execution parent. Scope support does not certify autonomous operating at that level. This supersedes the Department-only stop in Phase B; Phase B changes are preserved, not rolled back.

Resolver owns existence, tenant/Company lineage and scope boundary validation. Employee identity remains Company identity; current Assignment authorizes execution, not identity alone. Parent ownership does not authorize bulk Context hydration. Selected references require explicit scope validation. Usage remains one ledger. No fake Workspace, overloaded workspace_id, parallel Work/Execution/Conversation or per-scope ledger.

## Preflight

HEAD bb72916daba3ae9555914d03bdb7fcea9953ab9c. Staged 0; 129 tracked changed/deleted paths; 615 untracked paths. All preserved. No add, commit, push, reset, clean, stash or default App launch.

|Protected SQLite|Bytes|mtime_ns|SHA-256|Integrity|
|---|---:|---:|---|---|
|data/curis.sqlite|1232896|1786873339955841838|2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6|ok|
|backend/data/curis.sqlite|1277952|1786783659967572836|a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4|ok|
|/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite|1536000|1788614881473263746|d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617|ok|

Read via immutable read-only SQLite; no Runtime import. Every test/import must set CURIS_DB, CURIS_DB_PATH, CURIS_WORKSPACE_DB to the same external isolated DB.

## Exact allowed implementation seams / pre-change hashes

Resume consumer audit additions (same authorized execution/provenance scope): backend/app/main.py only existing `team_employee:auto` dispatch branch, SHA 480cc160c74befb7dcad70a3529c35ff13018ef7c604dc6070b57016e9baf335; backend/app/result_attention.py only canonical Result detail scope propagation, SHA 9434e05f248b15618b6865ab7d3ca41f0819f2087d83623ad30479a76041868b; backend/app/shared_workspace_projection.py only Result reader scope validation, SHA d909df1f8518d80c2f81acb9818d82e71dd7cdb052888e707098228d969a80c9. No Meeting or unrelated main.py changes. backend/tests/test_conversation_usage.py only freeze its pre-scope migration fixture at the original schema phase, SHA 0c00feea85c19a9094dd6a56b299b9618b21e8681387956a4dbd2cf967959fa9. New migration/provenance tests stay in test_canonical_execution_scope.py.

Only named semantic seams, never whole-file promotion. Pre-existing code remains owned by its original initiative.

Focused regression wording update: backend/tests/test_canonical_usage_attribution.py only `test_invalid_parent_is_rejected_before_provider_launch` shared resolver error text assertion; pre-SHA 24e7ed485f53c2d2dea7f50c319c6676b9c6c6f2ebdbdaadc114e32a06c4160a. HTTP rejection and zero Provider calls remain required.

Existing test_phase_b_builtin_organization.py scope-gate function is now owned for positive Department context/Work proof and retained missing-explicit-scope rejection. Its bootstrap/idempotency tests are unchanged; original pre-hash below applies.

|File|Owned seam|Pre-change SHA-256|
|---|---|---|
|backend/app/resource_scope_policy.py|Shared canonical scope resolution/boundary methods; retain existing path ownership interface|97e516c57cbf6c2f513f931cfab069c785bea5cb43df5d01b3a1e5a00d7e0bc1|
|backend/app/runtime/responsibility_routing.py|Scope validation and propagation through existing routing/execution|a61776c6d8d2fe06b4fb53b10d2e40dcffd4d6f78f2c5f8b4f7ba48831b8c2fa|
|backend/app/runtime/child_work.py|Cycle/Work scope validation, release identity, reference/acceptance boundary|cc90b4e504cc9369d9ddcd4bdaa8b64fcad141923ca76819e018b7390753406a|
|backend/app/conversation_service.py|Current Assignment scope/context/execution provenance; durable owner unchanged|2ad2d52063f30cdee38a0499c0ffcb6b22ac39bedf7fac215773cde1ecf31781|
|backend/app/employee_execution_identity.py|Scope validation for existing binding/callback/ACK; identity unchanged|e0895590fd1628eb32c18c2f54c148543bf09d38e060bec044521e84c0af1660|
|backend/app/ai_usage.py|Existing sole resolver and ledger scope propagation|e40fa7fac5190dfae8a64d11221b1b42384a20f9601435dca94addaa4b30175f|
|backend/app/database.py|Bounded Task/usage scope reconciliation only after schema dependency audit|287f9f3270cdef1ba38d94b29e6f82970eea843a3fc95136209c84880d4f4217|
|backend/app/result_store.py|Existing Task scope persistence and validation|319ed07e84ece71b601467e5b708cef4f4661752e10033a347eb44ed64f4d7de|
|backend/app/context_service.py|Bounded Task context consumption of validated scope|06ba08a922f45cf0d2a3e4dc32aadb61237bbe9c25654736b0b81924ac9ed15a|
|backend/app/api/team_operating_router.py|Existing execution adapter scope input/propagation|34d4fe5c8f147623abea69714c4d9623750c90126cbadaa3b765d2613bdbfc9d|
|backend/app/orchestrator.py|Existing Task execution scope consumption, no scheduler changes|c2dcc9f1ef432414664c08eec380eff8a6862dd477a1b9113ebce8c3ce960194|
|backend/app/runtime/general_workspace_delivery.py|Company Employee identity compatibility only; General product stays Workspace-scoped|e33eb1c092f3f844628cb58359451daed22c50e85ff3daab036fb690450af6c1|
|backend/tests/test_canonical_execution_scope.py|New external-isolated scope regression|NEW|
|backend/tests/test_phase_b_builtin_organization.py|Existing no-implicit-scope assertion wording only, reflecting the authorized generalized resolver; preserve Conversation execution gate check|e1381ca06ff373e95edde31aafcaf0955c188135fb4cd2406ae630f7335df6cd|

This Issue and docs/reviews/CURIS_CANONICAL_EXECUTION_SCOPE_RECONCILIATION_REVIEW.md own scope progress/evidence. Additional consumers/tests require explicit path/hunk/hash registration before editing. Phase B files remain covered by their original issue, resumed only after unified execution support.

## Schema / migration boundary

Context dependency addition: backend/app/knowledge_service.py only `_work_scope` canonical resolver/parent lookup and selected-reference scope compatibility (pre-SHA c9af2e2e421ada94ff6cb842a4664933b881e3738942b391896b86abce0c4e8e). Existing Knowledge persistence/ingestion/UX unchanged; no new Knowledge scope model.

Continuation authorization: CEO `CONTINUE — CANONICAL EXECUTION SCOPE RECONCILIATION` explicitly authorizes ledger schema reconciliation and deterministic isolated infrastructure proof before Phase B B–E. No intermediate acceptance checkpoint is requested.

Resume hashes: database.py f0f28e76c19b720845376f0c3a5030a150f8bc2cff7da6fb494c919535ea36aa; ai_usage.py 77228ba0b48a88846a30705df4c2e1a325f888e636a88416b08f66648998bf44. Other not-yet-edited owned consumers retain the hashes above. Protected DB fingerprints remain identical at resume.

Ledger migration plan: preserve existing column values exactly and add nullable scope_type/scope_ref, without historical backfill. Rebuild the same ledger inside a savepoint, capture/recreate every explicit index/trigger, preserve primary/unique constraints via existing table DDL, compare old-column rows in both directions before replacing the table. Existing historical attribution CHECK remains a legacy branch with NULL scope; new explicit scopes use canonical lineage shape and source constraints, with optional Department for Company scope. Unknown schema shape refuses migration before mutation. Failure rolls back the complete ledger operation. No protected database initialization or migration.

First schema step: add nullable tasks.scope_type and tasks.scope_ref with the existing _ensure_column mechanism; no UPDATE/backfill, no table rewrite, no new table/index/trigger. Old rows remain NULL and keep their existing workspace_id/project_id. Explicit new Task scope is validated before insertion. This additive step alone does not unblock ledger recording; the usage CHECK/department nullability requires a separate verified migration before launch support can be claimed.

Reuse runtime_entities.data_json for existing scope vocabulary where sufficient. Never infer Company execution merely from a missing Workspace. Legacy explicit Workspace remains Workspace provenance. Task/ledger schema changes are authorized but require prior exact migration design and isolated historical-row/index/trigger/idempotency/atomic-abort proof; no protected DB migration. No blind historical backfill to broader scopes. No dropping historical evidence or changing immutable usage semantics.

## Acceptance

- Four-scope resolver existence, lineage, Company/tenant isolation; wrong parent/ref rejected.
- Assignment/Employee/Work/Task/callback/Result/Evidence/Usage agree on scope before provider launch.
- Company and Department with zero user Businesses execute without synthetic parents; Business without Workspace execution is legitimate.
- Selected Context remains bounded; sibling and cross-Company resources rejected, no implicit whole-Company history.
- All four scopes: real chain, durable provenance, failure, retry/idempotency, restart; scope support separately reported from autonomy acceptance.
- Legacy Workspace/RD/Conversation/canonical usage/ACK/Package/DB Safety regressions preserved.
- Migration proof if needed: rows, indexes, triggers, immutable semantics and idempotency preserved; ambiguous migration atomic abort.
- Final 9x4 Scope Support Matrix, values SUPPORTED / PARTIAL / NOT APPLICABLE / FAIL, each backed by evidence.
- Continue Phase B A–E and integrated Browser/fresh packaged Desktop/restart only after this dependency passes.

## Stop / recovery

Protected DB mutation, unknown mixed-source ownership collision, second truth requirement or unresolved authorization policy conflict: stop affected work and report exact gate. Ordinary tests/adapters are not CEO gates. Preserve all work; no rollback of accepted code or default databases.

## Historical checkpoint audit — superseded by the completed contract above

Historical checkpoint: 74 isolated checks PASS; resolver, Assignment and Cycle/Work/Task scope creation/persistence were implemented at that point. Execution identity, Conversation Context and ledger schema/resolver were then incomplete; non-Workspace Provider launch stayed fail-closed. The completed contract and final Review above supersede this checkpoint. This paragraph does not downgrade the current `IMPLEMENTED / ACCEPTED CANDIDATE` disposition.

Governance owned updates (progress/authorization only): CURRENT_STATE pre-SHA e645dbdaa37a651eb9a5be190c25db1c4bc1e639591d928985a8a3525796f51c; PRODUCT_DOCUMENT_POINTER 2e2a47e52abd831a60b5a084000397988653654dd6621da60beec1b1e9bdcdd0; CHANGE_LOG 11d477d21e48f7f6c06518c48f3290adf0d3e100d38b7524e5d0c57d1c51b8f7; Phase B Issue bf08feef610981dfb29c85c816f70b788d2ea8dc98e2b9da35b040a39043a8f1. Preserve old gate as historical evidence, supersede its pending-authorization status.

Pre-change audit: ResourceScopePolicy only provided tenant path checks, not execution scope resolution. ResponsibilityRouting supported three scopes but not COMPANY. ChildWork required Workspace Cycle/Assignment. Conversation context required explicit Workspace. Canonical Work usage required Workspace lineage. This paragraph records the starting point, not current completed support.
