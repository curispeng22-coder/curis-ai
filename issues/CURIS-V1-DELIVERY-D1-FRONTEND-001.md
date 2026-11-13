# D1-A Supported Frontend Paths

Status: Review
Authority Class: REVIEW
Document Role: Implementation Task
Disposition: REVIEW_REQUIRED
Task ID: CURIS-V1-DELIVERY-D1-FRONTEND-001
Owner: Main Development
Receiving Owner: Curis V1 Delivery Owner
Date: 2026-10-04

## Objective and authorization

Implement the approved D1-A subset in new frontend views: CompanyAttention source projection, on-demand Employee discussion/full same-topic conversation, existing canonical Work reading, explicit Result opening with independent Viewed receipt, original-object return, waiting/error/unknown states. Delivery Owner explicitly authorized this task in chat. Author implementation does not confer acceptance.

Approved Design input: confirmed Render and `artifacts/tasks/CURIS-V1-RENDER-BASED-PROTOTYPE-002/evidence/delivery-d1-20261004/revision-02/source-seal.json`. Seal SHA256 `fb933e39e997979deb8008627ae442f6ba4805668a0e2eca3b5fd23a39a0e71c`; all 100 source hashes verified before writing. Only the delegated D1-A subset is approved; prototype mock state, full D1/P7/HumanGate/extra reference permissions are not implementation truth.

## Exact Allowed Files

All paths below are relative to `/Users/yy/Documents/Curis AI Workspace/`:

- `issues/CURIS-V1-DELIVERY-D1-FRONTEND-001.md`
- `docs/reviews/CURIS_V1_DELIVERY_D1_FRONTEND_REVIEW.md`
- `frontend/components/delivery/d1/D1Surface.js`
- `frontend/components/delivery/d1/CeoMatterView.js`
- `frontend/components/delivery/d1/EmployeeConversationView.js`
- `frontend/components/delivery/d1/WorkView.js`
- `frontend/components/delivery/d1/ResultView.js`
- `frontend/components/delivery/d1/D1.module.css`
- `frontend/lib/d1Api.js`
- `frontend/lib/d1State.mjs`
- `frontend/tests/d1Api.test.mjs`
- `frontend/tests/d1State.test.mjs`
- `frontend/tests/d1EntryCompatibility.test.mjs`
- `frontend/app/ceo-office/page.js`: imports and D1 route render only; preserve onboarding/zero-business branch through the existing compatibility entry.
- `frontend/app/ceo-office/conversation/page.js`: import and new view entry render only; preserve existing controller and legacy query semantics.

Allowed Directories: parents of these exact files only for listed files; `artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/` for scoped pre/post hashes, snapshots, test/build/browser evidence and handoff. Isolated copied build/browser workspace and test utilities stay within this task directory. No empty component scaffolds.

Existing prehashes:

| File | SHA256 |
|---|---|
| frontend/app/ceo-office/page.js | 22086b12860fccfe5318a8aec323d4b78a38521ea3b65353a28e877629ad211f |
| frontend/app/ceo-office/conversation/page.js | 36f5a7ab7bd301ef400fb8e212d919d17214d46009bb92e5d40f0a2a6089e993 |

All newly allowed paths were absent before task writes. Original dirty content must be retained; compare task snapshots rather than treating HEAD as a rollback baseline.

## Implementation boundaries

Use existing workspaceFetch auth/identity/error boundaries and existing accepted API contracts. Matter remains a source projection. Draft/return anchor are bounded frontend state, not canonical history. Company, topic, Employee and assignment identities remain separate. Late reads cannot replace a newly selected object. A network retry retains the original request_id. Explicit successful Result opening alone may record Viewed; URL restoration/prefetch never records it. Viewed is not Accepted.

New layout consumes approved D1 content/Employee interaction; old dedicated visual modules do not become the new visual body. D0 host/slots are provisional, with global shell validation separate. Existing onboarding and zero-business behavior remains a compatibility branch.

Unsupported commands must retain visible precise explanations and lawful repair/return links: atomic referenced Work creation/version CAS, general Result acceptance, full HumanGate verification, additional COMPANY reference grants, P7/Meeting design. No local success mutation. Only existing supported lifecycle commands for their applicable scope; unresolvable scope fails closed.

## Safety and evidence

Protected databases (read-only size/mtime/SHA256/integrity baseline and postcheck): `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`, `/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite`, `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite`. Fingerprints are recorded in task evidence. Never import Runtime against defaults. If isolated runtime evidence is attempted, set CURIS_DB, CURIS_DB_PATH and CURIS_WORKSPACE_DB to the same fresh repository-external database before imports, record exact owner/root/ports. No default App, packaging, Keychain, real Provider, upload/publish or external write.

Required checks: meaningful API transport/state/query tests; related existing frontend Conversation/Viewed regression; targeted lint and production build in isolated task copy; Browser operation for reading/return/error/topic separation/Viewed. Transport mocks prove mechanics only. Real API evidence, missing runtime capability and visual deviations must be distinguished. Delivery Owner and independent QA determine acceptance.

## Stop and rollback

Stop on unknown prehash or overlapping owned hunk, new target already existing, protected DB risk, unauthorized path, Authority conflict or new canonical truth requirement. Routine in-scope bugs may be fixed. No backend/schema/global CSS/legacy-module changes, no Git stage/commit/push/reset/clean/stash/checkout/worktree operations. Rollback only task-added files and task-owned hunks against captured preimages, under exact recovery authorization; do not overwrite the user's original dirty changes. Frontend rollback does not undo persisted API commands.

## Output and next gate

Outputs: substantive allowed frontend files, scoped evidence manifest, `docs/reviews/CURIS_V1_DELIVERY_D1_FRONTEND_REVIEW.md`. Status/Disposition remains Review/REVIEW_REQUIRED until Delivery Owner review and independent QA. No Pointer/CURRENT_STATE/CHANGE_LOG or Frozen Authority promotion is authorized.

## Submitted evidence

Implementation submitted for review on 2026-10-04. The 15-file grant was used, with only import/render hunks changed in the two existing entries; their original dirty preimages are preserved. 24 frontend tests pass; targeted lint and isolated production build pass. Browser evidence has 10 primary cases and 2 separate race/waiting cases. Real isolated routers/SQLite confirm independent Viewed receipts and pause/resume of the same Work. Retry timeout/conflict, delayed reads, RUNNING and duplicate-purpose rendering are mechanics evidence, with no Provider launch.

The three protected database fingerprints and immutable integrity checks remain identical. Both task-owned services stopped. The external fixture databases, copied build and scoped evidence are retained for Owner/QA review, not promoted as product truth. Review and exact output inventory are in `docs/reviews/CURIS_V1_DELIVERY_D1_FRONTEND_REVIEW.md` and `artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/output-manifest.json`.

## R1 bounded repair authorization and independent FAIL

Status remains Review; Disposition REVIEW_REQUIRED. Delivery Owner adjudicated independent QA D1-A FAIL and authorized one bounded repair within this Task, not a new product/architecture gate. Independent QA report: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-A-QA-001/REPORT.md`; SHA256 `364f31775e22df5299a5f60e40d87f5e8535e61d6112eb84722480778e8ab0c8`. QA-01 through QA-06 remain historical failures until independently retested. Do not alter QA output or previous author evidence.

R1 output directory only: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/revision-01/`. Scope and safety from the original Issue persist. Two page entries are read-only. Exactly one scope extension: SharedConversation.js ConversationComposer-only optional compatible props/slots, prehash below; use the shared export without its model hook or legacy visual body.

| Exact file | R1 owned hunks / QA mapping | Before SHA256 |
|---|---|---|
| `/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DELIVERY-D1-FRONTEND-001.md` | Append R1 grant, prehash and QA mapping; preserve original scope and FAIL history | `5638ec5aeb0db328f66286a344303b06edb20a65d3d5e5f7b126b12e5970c767` |
| `/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DELIVERY_D1_FRONTEND_REVIEW.md` | Append R1 evidence; preserve earlier submission and QA FAIL, no Accepted promotion | `e8227404a977bd9882c48bc96a2245e025ad40e9e91994772bfc15d7ee086cc5` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/D1Surface.js` | QA-03 same-context toggle and Bar-adjacent slot; on-demand Employee Detail utility only; QA-05 labels | `d8cc5dbea2615acd24f0f4ad4f7754d6b5c3a4dc30f86b7305aea99f1465758f` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/CeoMatterView.js` | QA-06 CANCELLED mapping; QA-05 current-field labels/source details | `764e521f03eeef7e586dff4b5326c0d343caf53a93747df7394be588ef777c41` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/EmployeeConversationView.js` | QA-01 current-draft comparison and request capture; QA-03 detail trigger; QA-04 consume shared Composer via semantic slots; QA-05 primary labels/source details | `2a265853f77c3c762a8b841b4c6551f2c6426e56de1e804f087494697e8be936` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/WorkView.js` | QA-03 name/avatar/detail and discussion toggle/slot directly under Bar; QA-05 ordinary labels/source details | `6915874c96204f8ba6ba0f70af7233a091e6ad24644c55f8d5474c854f8a31b4` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/ResultView.js` | QA-02 actually rendered readable material gate and receipt; QA-05 primary labels/source details | `43f271edfd1505fe06f1cc99beaa37e9089587b8b61360c6b23569f8b7e33e21` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/D1.module.css` | Only necessary local styles for the preceding new D1 views, Composer adapter and utility | `916b4675aa3e8649222c3204d836d78177821ae89f76df1ed8d839ca8eb867eb` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/lib/d1Api.js` | Only existing lawful read-only Employee mapping/detail/binding reads if needed; send and attribution unchanged | `52845b670038d878a9ebee79e141a92ebbcf7323abc86fcc48cea8376de7990a` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/lib/d1State.mjs` | Only current-draft comparison/readability/display helpers for preceding corrections | `03feaeb40690e39a0a3c54bb6c407ea7bc2e481b24a8b527dcc5763b63f3eb40` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1Api.test.mjs` | R1 API/mapping regression | `092f131f8b9878780a7c0d5e451dd7529715f99e7a5393fa165a75ec3e0a191a` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1State.test.mjs` | R1 draft/readability regression | `02e2b60ca86a89a1579ac7c48d99d4eb121f2da04aed0cb53d7aacbd8cfaade8` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1EntryCompatibility.test.mjs` | R1 entry/Composer compatibility regression | `7d1c82688d9c05d0089a9f9591436ab11d7406e997b6009023ada9a0ed13ef48` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/page.js` | Both existing page entry paths read-only during R1; retain their sealed hashes | `bfb36a97206cfa477d1c3007f70cabed19cffafce1be148c3778f327546314bd` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/conversation/page.js` | Both existing page entry paths read-only during R1; retain their sealed hashes | `1cb65049fda4e3b3cb8e05c26d4f0470f32712e48193856031f182300a53c2eb` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/SharedConversation.js` | ConversationComposer export only: backward-compatible optional style/input label/maxLength/showVoice slots; preserve defaults and all other code | `bf645c6ce3cf2c3254a019165eae60dd1ba1b8d8fef7071019179efc4f08adae` |

Acceptance evidence: focused tests plus existing shared consumer regressions, isolated build/lint, new external Runtime root with three identical DB env variables before imports and no Provider, real empty-result router/SQLite receipt boundary, browser new-draft completion race, collapse/Bar placement/full return/detail utility/semantic Composer/ordinary language screenshots. Protected DB fingerprints/integrity must be identical before/after R1. Preserve original seal/evidence; submit new exact 16-file seal including unchanged paths. No backend/API contract/old consumer/global CSS/Git operations. One completion/hard-gate return to Owner, followed by independent QA; no self-Accepted.

### R1 repair return (2026-10-04)

R1 is submitted for independent retest, not Accepted. QA-01 current-input race, QA-02 rendered-readability receipt gate, QA-03 Bar slot/toggle/demand-only Employee detail, QA-04 shared Composer adapter and QA-05/06 primary labels/stopped state were repaired within the exact owned hunks. The earlier independent FAIL remains recorded and awaits QA/Owner disposition.

Evidence is only in `artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/revision-01/`: 44/44 focused and existing shared consumer regressions, empty targeted lint, successful final isolated production build, 15 primary Browser cases, 3 separate late-response/RUNNING cases and a final-build source-detail check. Real Result router/SQLite shows empty/blank specimens not viewed, blank Attention retained, supported text/structured material viewed, and the same Work CANCELLED displaying 已停止. Provider reply/completion/retry timing remains explicitly mocked, with 0 execution/usage records.

Both page entries remain unchanged; SharedConversation edits are limited to the ConversationComposer export, with the default consumer behavior and remaining file suffix identical. All three protected databases are byte/fingerprint/integrity unchanged. The R1-owned listeners stopped. New 16-file seal, owned-hunk diff, manifest, sample Runtime checks and screenshots remain REVIEW_REQUIRED in revision-01. No original seal, author evidence or independent QA report/fixture was modified. No canonical promotion or additional gate opened.

### R1 final draft snapshot verification

The local complete input snapshot additionally preserves whitespace-only edits and survives bounded pending-request remounts. Existing send/attribution DTOs are unchanged. Final rebuilt source passes 44 regressions, targeted lint/build, and 5/5 supplemental Browser cases in `revision-01/browser-snapshot-final-report.json`, including matching completion after topic return. Earlier 15+3 Browser reports and independent FAIL remain untouched; source-stage limits are recorded in Review. Final exact 16-file seal and manifest follow this supplement. Review / REVIEW_REQUIRED; next gate remains independent QA and Owner disposition.

## R2 exact bounded authorization — current responsibility (2026-10-04)

Task ID: CURIS-V1-DELIVERY-D1-FRONTEND-001, R2. Owner: Main Development; Receiving/Decision Owner: Curis V1 Delivery Owner. Status Review; Authority Class REVIEW; Disposition REVIEW_REQUIRED. Objective: repair only R1-QA-03-01 current responsibility omission using the already lawful current_responsibilities response. No product/architecture exploration or new read API.

Input: independent QA revision-01 REPORT.md SHA256 `f506cdc825ce206f43eacf98dcf2d9a9b75d9ee094aae3261746b4d1cef636f1`, real-team.json and employee-detail.png/DOM; R1 exact seal `00d0ebed290913a5591d71fcb42b0310254202e497de8a07e77d4c1974026f77`. All 16 hashes matched before R2. QA is REVIEW / Review / REVIEW_REQUIRED: five findings and QA03 interaction passed within their limits, but final independent Verdict remains FAIL for this one omission. Historic FAIL/author evidence remain unchanged.

Allowed evidence directory: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/revision-02/`. Original scope safety persists; other sealed sources are read-only. No new production source file.

| Exact allowed file | Owned hunks | R2 before SHA256 |
|---|---|---|
| `/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DELIVERY-D1-FRONTEND-001.md` | append exact R2 grant and final return; preserve R0/R1 | `1773afb42a8a309d51af7d673a947367975df178cca642d1eb191944740adf6b` |
| `/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DELIVERY_D1_FRONTEND_REVIEW.md` | append R2 repair evidence only; preserve FAIL history | `4d7936cb0359bea7f713f0b33c6cf9df3b50987d37e41cd71d490d3cabdbe786` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/D1Surface.js` | R1-QA-03-01 Employee Utility current-responsibility display and current-entry context only | `1c811f1f8fd344fdbb3fabc9c3457526319659bd6313f51fb5b34c7c9ab1e0fc` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/lib/d1State.mjs` | pure current-responsibility projection helper only | `746fc4e29a19e69c8387c8f7199376c9f74cad3d35ba3d928d016920c97f5b03` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1State.test.mjs` | exact current-responsibility helper regressions only | `7541afea4ac65ea7908441dd99b1c531a312f6075eebd564025942e66ee8f4f7` |
| `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1EntryCompatibility.test.mjs` | Utility/context display regressions if needed | `3e40663b232b8c4b0a347de805e9c1e9292ff7d66e112416bb0ba3c34f6ffd68` |

Behavior: separate current responsibilities from long-term static role responsibility; prioritize exact current Work object_ref without guessing a primary or dropping other lawful entries. Render supplied assigned activity without changing it to running. Empty list, missing fields and foreign holder/owner entries remain truthful/isolated. Only the already authorized Company+Workspace response may be consumed; no broader Company/history lookup. Utility close retains focus and draft; viewing emits no Runtime/Conversation/Work command.

Required output/evidence: focused helper and necessary adjacent regression, targeted lint/build, final-source Browser + real router + isolated SQLite for current detail; three protected DB read-only pre/post fingerprints/integrity; owned service exit; new exact 16-file seal/diff/manifest with unchanged hashes rechecked. Reuse signed R1 PASS evidence; do not repeat 44+29 whole suites or broad E2E. All R2 outputs REVIEW_REQUIRED. No Git/default App/backend/schema/Provider/Keychain/Desktop/global UI changes, canonical promotion or Accepted claim. Next Gate: one completion return to Delivery Owner -> independent targeted QA -> explicit Owner disposition.

### R2 repair return — author evidence, pending independent retest

R1-QA-03-01 display repair is submitted, not Accepted. Only four source/test files changed: D1Surface current detail/context hunks, pure currentResponsibilities helper, its exact regressions and Utility SSR/context regression. This Issue and original Review append only. Other ten source/test/entry paths of the 16-file seal remain byte-identical to R1.

18/18 focused helper/entry/Composer compatibility regressions pass; targeted lint and final isolated production build pass. Browser 7/7 checks: three real-read cases establish assigned-but-not-executing activity on the exact current Work, keyboard/close focus/draft retention and full-discussion same-Work return; four response-mechanics cases establish multiple-entry retention/current priority, foreign-holder/owner exclusion and empty/missing-list/missing-activity language. Isolated SQLite Work and event counts match the pre-Browser baseline, with zero execution/usage/Viewed; all three protected DB fingerprints/integrity identical; owned services stopped. Prior QA/author evidence and historical FAIL retained.

R2 evidence only in revision-02, with final new 16-file seal, exact diff and output manifest. Reused R1 independent PASS evidence remains explicitly bounded; no 44+29/full E2E rerun, live AI or Desktop claim. Next gate: Delivery Owner return -> independent targeted QA against R2 seal -> explicit Owner disposition. Review / REVIEW_REQUIRED; no canonical promotion.

## Latest Delivery Owner Decision — D1-A supported paths accepted (2026-10-04)

Status: Review. Authority Class: REVIEW.
Verdict: **CURIS-V1-DELIVERY-D1-FRONTEND-001 / D1-A SUPPORTED PATHS IMPLEMENTED / ACCEPTED**.
Decision Owner: Curis V1 Delivery Owner.
Scope: **bounded integration baseline only**, as defined below.
Disposition: Owner ACCEPTED within this bounded scope; canonical delivery registration pending separate exact authorization. This document remains Review; no document Status of Accepted or Frozen promotion.
Next Action: retain the accepted implementation snapshot and provenance; await a separately authorized canonical delivery registration. No next development batch is opened.
Target: existing canonical delivery registration/backlog, only through a later exact grant.
Next Gate: Delivery Owner's separately authorized canonical registration or next scoped task; D0, whole-product and Release gates remain separate.

Decision evidence:

- [R2 independent QA REPORT](</Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-A-QA-001/revision-02/REPORT.md>), SHA256 `cdbfa00fe0bb80c1eb522985d870ede7f97a3a8bffa96bd403f189f8649c0ee2`: R1-QA-03-01 closed, bounded D1-A QA PASS inheriting Owner-signed R1 local PASS and their limits.
- [R2 independent QA manifest](</Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-A-QA-001/revision-02/output-manifest.json>), SHA256 `d9355b97b42cb6f246bbc6899bbf3525d640d8b0669759fc38f5bc33aece59de`.
- [Final R2 16-file seal](</Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/revision-02/source-seal.json>), SHA256 `92445b51bef69c166e851a4e1d22017ebbf9f018aada16520ee2fa9e5831bcaa`: all 16 matched before this governance append; the current 14 implementation/test files remain identical afterward.
- [Independent safety postcheck](</Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-A-QA-001/revision-02/postcheck.json>): source/prior evidence unchanged during QA; three protected DB fingerprints/integrity identical; owned processes exited and listeners closed. This record cites existing verified evidence and runs no new Runtime/DB/test operation.

Accepted scope only: authorized real-source reading; existing lawful Work lifecycle; on-demand Employee discussion/full/return; shared Composer semantic adaptation; actually readable explicitly opened Result Viewed and Attention semantics; request/session-draft isolation; lawful Employee Utility identity and current responsibilities. The real source specimens are isolated seeded routers/SQLite. Send/completion faults and races are mock mechanics. Zero Usage does not establish cost safety.

Excluded: D0/final visual/global four-pane/sidebar; whole D1; Company-scope Work reading; new references/CAS/general accept/HumanGate/P7/MeetingReturn; real cloud Provider/usage bills/production authorization; fresh packaged Desktop/full restart; three-business end-to-end journeys; Release. Session-only draft/return-stack limits remain; persistent draft acceptance is not granted. R03 prototype P7 conflicts/duplicate keys remain independent and unopened.

Historical FAIL and R1/R2 author NOT ACCEPTED submissions remain unchanged as provenance. This latest explicit Owner verdict supersedes their pending acceptance only for the above bounded supported paths; it does not rewrite historical evidence or infer whole-product acceptance.

Only this Issue and the original Review receive append-only governance updates. Their current hashes therefore differ from their pre-acceptance values in the permanent R2 seal; this is the authorized metadata append, not an implementation mismatch. The original seal and QA artifacts remain untouched. [Owner decision and output manifest](</Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-D1-FRONTEND-001/owner-acceptance/output-manifest.json>) record before/after document hashes and the 14 unchanged source hashes. Durable outputs remain REVIEW_REQUIRED for subsequent canonical registration; no PROMOTE/ARCHIVE/DELETE is performed here.

CurrentState, Pointer, Backlog, ChangeLog, Frozen Authority and all implementation files are outside this acceptance-record grant and remain unmodified. No Git, DB, Runtime, App, development, QA expansion or next-batch action.
