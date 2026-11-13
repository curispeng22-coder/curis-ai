# Writing Chapter local authoring vertical

Task ID: CURIS-V1-DELIVERY-WRITING-001
Authority Class: REVIEW
Status: Review
Disposition: REVIEW_REQUIRED
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
Verdict: READY_FOR_INDEPENDENT_QA / NOT ACCEPTED
Updated: 2026-10-04

## Objective / explicit decision

CEO approved continue via Delivery Owner: implement the approved bounded Book/Chapter local authoring contract and sealed UI subset in one vertical batch. Required input: PREP.md and EXACT_SCOPE.md SHA77e26b8b27c835f4b25fef1101cd81f4bde66941236c603fc87768663ab3c5fe, exactscope prehash SHAd1da906aa573f1782b509b466f34b270e7afd73c48883dbc9cd55beee090262a, next-delivery-20261004 UI HANDOFF/COVERAGE/101seal, Frozen Shell§3.1A, accepted D0/D1 bounded seams. Design subset: BookCollection/ChapterWorkspace and Publishing professional content; no Frame or prototype mock/C-02 import. One accepted D0 host/root Assistant. Missing introduction gets inline field feedback/focus.

## Exact Allowed Files / owned hunks

- `/Users/yy/Documents/Curis AI Workspace/backend/app/main.py` — owned hunk baseline c30a4cfbd2a1a2106ec91bf88c800a192bca2c939274ac4b965a10b65ca6aedf
- `/Users/yy/Documents/Curis AI Workspace/backend/app/api/conversation_router.py` — owned hunk baseline 16530d4810315ef95067d4b91d0c7f2abc0087cd7c29774f9052b7a158a4b39a
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/workspace/InstalledWorkspaceRuntime.js` — owned hunk baseline a3fd7aced062b4aff0443345c0e25d02c5f593a2712cb7390934642e1a31598b
- `/Users/yy/Documents/Curis AI Workspace/backend/app/writing_chapter_service.py` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/backend/app/api/writing_router.py` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingWorkspace.js` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingChapterMain.js` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingPublishingMain.js` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/Writing.module.css` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/lib/writingApi.js` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/lib/writingState.mjs` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/backend/tests/test_writing_chapter_vertical.py` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/backend/tests/test_writing_chapter_api.py` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/frontend/tests/writingChapter.test.mjs` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DELIVERY-WRITING-001.md` — NEW / absent verified
- `/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DELIVERY_WRITING_CHAPTER_REVIEW.md` — NEW / absent verified

Only existing hunks: main.py5650–5660 shared ConversationService construction/router registration; conversation_router.py41–45 optional keyword-only service injection with old handlers unchanged; InstalledWorkspaceRuntime import + approvedWriting ready-state dispatch before generic branches. No whole-file replacement. All other old functions/source/DB/schema/coreprimitive/Catalog/governance/Git stay protected. Scope roots: frontend/components/writing only the granted4files, existing parents only exactfilelist. Artifact root `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/`; fresh external `/private/tmp/curis-writing-impl-20261004-01/`. Drift unknown or new necessary file/hunk STOP/report exact amendment; do not reset/delete unowned changes.

## Approved local Package / object contract

Local carrier `com.curis.local.writing-authoring` v0.1.0 digest **2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e**. Complete manifest/surfaces/Book/Chapter schemas and hashes are `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/package-contract.json` SHAf132d444a3c2e341c33bcd406b5f7022b98cef4d3ff32fa16179e9a8c3b80197; exact4 source JSON files `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/package-source/`. Existing validator/install/create must verify this declared carrier. No official Catalog publication, no default/production install or guessed identity. Source is this explicit task contract, not user samples/prototype. Book/Chapter are existing PACKAGE_DOMAIN_OBJECT domain types, writing.book/v1 and writing.chapter/v1; strict parent Book relationship. Responsible Assignment must actually have WRITING_CHAPTER_AUTHOR in same scope; Holder/Executor/author distinct. Empty/missing legal production instance/Book remains unavailable/empty; UI may create records only via existing declared domainobject.create API.

## Approved domain events / boundaries

Only append writing.chapter.* scoped draft.saved/discussion.bound/candidate.recorded/candidate.adopted/inspection.recorded/formal.confirmed/package.prepared/work.linked to existing evolution_events. Fulltenant/company/workspace/packageinstance/version/digest/book/chapter/action/request namespace, transactionCAS/payload-equal replay, immutableformal/package; no DDL/newCoreEntity. Selection UTF16/excerpt/version/hash/selectedknowledge/anchor checked, stale rejects. Draft≤200000Unicode chars, event≤1MiB, message≤8000; explicit error no truncation/cost-safety claim. AUTHOR_MANUAL versioned inspection is author judgment, not independent review. Reply-derived proposal is communication, neverbusinessResult/Viewed/Workcomplete. Existing Work/Result requires scope+basis legal; otherwise unavailable. Formal≠Published; localpackage/download no external success. Current Package migration fingerprint does not include these domain events: fingerprint them separately across disabled/uninstall/cold reread.

## Safety / acceptance / rollback-stop

Before any backend import all CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB same fresh externalSQLite, PYTHONDONTWRITEBYTECODE=1. Preflight three protected DB+sidecars size/mtime/SHA/immutable integrity recorded in preflight.json; repeat quiet read-only atclosure, never write them. Fresh selective source copy excludesDB/.env/credentials/oldbuild. Isolated legalPackage install/domaincreate/author domaincommands/canonical discussion controlled executor only; foundation test fixtures labelcontrolled. No realProvider/keychain/native/defaultApp/platform/uploads/publication/Git. Provider absent retainsinput/unavailable, test output labeledtestsource nofakeemployee/Candidate/Result/review.

Acceptance: exactscope matrix scope/parent/CAS/two-client/replay/UTF16/staleknowledge/sourceprovenance/immutable/atomicrollback; canonicalsharedservice in-flight compatibility; disabled/uninstall/new event retention; Pythoncompile/backendfrontendfocused/lint/freshbuild; actualBrowser manualoriginaltext→save→AUTHOR_MANUAL→explicitformal→localpackage/download→sameChapter/anchor/refresh/servicecoldreread; candidate branch clearlycontrolledtestsource or unavailable. D0/D1 bounded adjacency including navigation/Assistant/discussion/Viewed remains. Tests/API200 do not wholeproductaccept. No destructive migration or rollback of user work; source repair stays exacthunks, snapshot preimages retained. ProtectedDB drift/Authority conflict/illegalcarrier/scope boundary stops with evidence.

Outputs: source/seal/preimage/ownedhunks/actualchecks/Browser/network/DB/retention/version records, substantive originalReview, task HANDOFF/fullmanifest. StatusReview/REVIEW_REQUIRED until independentQA thenOwner decision. NextAction: implement continuously and return sealednode to Owner019ff1ba-f696-7002-8a6c-2b357ded819c. TargetAuthority: thisIssue/Review only; no CurrentState/Pointer/Blueprint/Backlog/ChangeLog writes. NextGate: independentQA, not selfAccepted.

## Implementation return · 2026-10-04

The exact 16 granted paths are implemented; final evidence and full output manifest remain in the granted task root. Backend focused suites: 26 passed (`backend-check-final-05.log`); frontend Writing/D0/D1 suites: 38 passed (`frontend-check-final-03.log`); scoped lint and fresh final-03 build passed. Actual isolated Browser author flow created Book/Chapter, saved original Unicode text, preserved selected-text discussion input across hide/refresh, rejected stale save while keeping dirty input, explicitly rebased and saved, recorded AUTHOR_MANUAL inspection, explicitly confirmed immutable Formal, and saved/downloaded a local Package. Latest physical file: 1380 bytes, SHA256 `1c5a3a1db8c88cbd198dd39727dfacc4f35776088272af53dde689f7f80b852d`; exact Package identity in bytes. Physical backend restart and Browser reload retained the same draft/Formal/Package with unchanged 11 Writing events; manual chain created zero tasks/AI usage. This is local evidence, not full product acceptance or real Provider/platform/native acceptance.

Scope incident: first pytest default cache wrote five new Git-ignored files under root `.pytest_cache/`, outside grant. Exact paths/hashes and recovery copies are in `cache-scope-incident-final.json`; Delivery Owner decision is CLEANUP NOT AUTHORIZED. Retain all five and recovery, do not delete; subsequent tests used external cache. This incident is a recorded workflow followup, not source scope promotion. Preflight's new-file row modes were copied from pre-approval PREP; they describe historical proposal state, while this Issue's explicit CEO-approved exact grant authorized implementation.

Next Action: Delivery Owner routes this sealed return to independent QA, then records an explicit Owner decision. Review: `/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DELIVERY_WRITING_CHAPTER_REVIEW.md`. HANDOFF and Task Output Manifest: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/HANDOFF.md` and `TASK_OUTPUT_MANIFEST.json`. No authority promotion, Git mutation or cleanup was performed.

## Appended Owner bounded decision · 2026-10-04

Authority Class: REVIEW. Status: Review. Disposition: REVIEW_REQUIRED for retained evidence; no Current/Frozen promotion. Owner: Curis V1 Delivery Owner. Latest Owner Verdict: **Writing local authoring mechanics IMPLEMENTED / ACCEPTED within tested controlled Package / local Browser scope**. The earlier READY_FOR_INDEPENDENT_QA header and original sealed return remain historical at their sealing point; this append records the subsequent bounded decision without replacing them.

Decision source: Owner chat `019ff1ba-f696-7002-8a6c-2b357ded819c`, explicit instruction after final independent QA report `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-QA-001/REPORT.md`, SHA256 `e861e3385379fba8dea679239b84a5ff4a19dbc54b5bd6db5345ff7f05714c79`. QA independently passed 14 Writing backend + 11 adjacent identity/conversation + 7 Writing frontend; fresh QA build `Q_ZvyI8BSQV5hYI21RpdO`; actual download, cold reread, disable/uninstall retention and protected database closure passed.

Accepted scope ONLY: local version/CAS, exact Selection, unavailable execution preserving input, AUTHOR_MANUAL→explicit immutable Formal→local Package and actual download, physical cold reread and disable/uninstall retention. Controlled candidate tests do not accept real generation. Not accepted/verified: production Package installation and user starting flow, real Provider execution, independent manuscript reviewer, full Book lifecycle/business E2E, native/default App, platform publishing/account/rights verification, or full Writing business completion.

Expanded QA suite remains 17 PASS / 2 FAIL. Read-only diagnosis in `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/regression-diagnosis/REPORT.md` reproduced both exact failures in three fresh copies, including the actual Writing-before D0 snapshot and InstalledWorkspaceRuntime task preimage control. Only dispatch bytes differ among 24 compared inputs. Actual failures: test85 checks Shell source for CEO 工作台; test165 checks legacy CeoDeskOperating for 当前没有可证明的下一责任. Neither reads Writing dispatch. A separate v2 gap test is UNEXECUTED because selective QA copy lacks its historical JSON before assertions; it stays UNVERIFIED. No assertion/source repair or all-suite PASS claim.

Current production facts from unchanged source/evidence: Writing content dispatch exists only for the exact declared carrier/version/digest/schemas under installed workspace route; this task installed it only in isolated test/QA companies and supplied an artifact-local carrier, not a production catalog/onboarding delivery. No production installation/user-entry evidence is available. Legal author responsibility requires exactly one WRITING_CHAPTER_AUTHOR assignment in the same workspace with valid execution context, verified explicit identity bridge and one enabled model. The production router creates WritingChapterService with default allow_execution=False, so real execution remains unavailable even after valid binding; controlled fixture assignments/models do not prove production configuration. No new path is automatically developed.

Next Action / Next Gate: Owner records separately authorized followups for production installation/start/binding, real execution and independent/native/platform gates, plus extended test expectation/fixture coverage disposition. Evidence remains REVIEW_REQUIRED. The original five pytest-cache incident files and recovery remain retained under CLEANUP NOT AUTHORIZED. Registration records and exact append-prefix/source unchanged proofs: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/owner-acceptance/`. No CurrentState/Pointer/Blueprint/Backlog/ChangeLog, original seals, QA report, business source/tests, Git, native, Provider or database write changed.
