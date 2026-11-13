# Writing Chapter implementation Review

Task ID: CURIS-V1-DELIVERY-WRITING-001
Authority Class: REVIEW
Status: Review
Disposition: REVIEW_REQUIRED
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
Verdict: READY_FOR_INDEPENDENT_QA / NOT ACCEPTED
Source: explicit exact Issue/domain contract/Approved Design subset
Target Authority: this Issue / Review only; no Product or Frozen promotion
Next Action: Delivery Owner routes sealed implementation and evidence to independent QA
Next Gate: independent QA followed by explicit Delivery Owner decision

## Scope and authority

The CEO-approved bounded vertical implements the exact 16 paths in `/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DELIVERY-WRITING-001.md`. Inputs were the approved PREP/EXACT_SCOPE (SHA256 `77e26b8b27c835f4b25fef1101cd81f4bde66941236c603fc87768663ab3c5fe`), sealed next-delivery-20261004 Book/Chapter/Publishing content subset, applicable Frozen Shell §3.1A, and accepted D0/D1 seams. Those inputs constrain this delivery; this Review is REVIEW evidence and does not rewrite Current Product Authority. Historical prototype material supplies approved design references, not implementation truth. Product target and actual local behavior remain distinct.

Only three existing source seams changed: shared ConversationService construction/registration in main, optional service injection in the existing conversation-router builder, and exact Writing carrier dispatch/imports in InstalledWorkspaceRuntime. `owned-hunks-proof.json` verifies all bytes outside those owned changes match captured dirty-tree preimages. Existing handlers and executor body remain unchanged. 27 D0/D1 adjacent source paths and 101 sealed prototype files/assets match their recorded accepted/sealed hashes. All 16 outputs are listed individually in `source-seal.json` and the full Task Output Manifest. No Git operations or governance writes were made.

Evidence root for all relative links below: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/`.

## Implemented behavior

Book/Chapter are actual declared Package domain objects over existing PACKAGE_DOMAIN_OBJECT and append-only evolution_events. The approved local carrier is `com.curis.local.writing-authoring` v0.1.0, digest `2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e`, schema versions writing.book/v1 and writing.chapter/v1. Existing validation, isolated install and domain-object creation were exercised; no schema/DDL/core primitive or official Catalog change was needed. Every command validates tenant, company, CEO, workspace, exact package instance/version/digest and real Chapter→Book parent.

Transactional draft-head CAS and scoped payload-equal idempotency prevent overwrite and duplicate appends. The editor retains unsaved input and its original base when remote state changes; stale save is rejected until the author explicitly reviews and rebases. UTF16 selection checks exact offsets, excerpt, draft hash/version and anchor, including repeated paragraphs and surrogate boundaries. Selected Knowledge must be canonical, active, in legal scope and at the exact content hash. Limits reject excess input without truncating it.

Discussion uses the canonical shared ConversationService, legal WRITING_CHAPTER_AUTHOR assignment, verified execution identity and enabled model. Default execution is unavailable; the UI preserves input. Candidate provenance/adoption is exercised only by the controlled canonical executor fixture and is labelled CONTROLLED_EXECUTOR. A reply-derived candidate is communication, not Business Result, Viewed acceptance or Work completion. Existing Work links require a real scoped Work with matching writingBasis and responsibility route; otherwise unavailable. Business Result remains unavailable pending a legal basis.

AUTHOR_MANUAL inspection stores the current draft/knowledge/checks and author identity; it is explicitly not an independent review. Formal requires explicit confirmation and stores an immutable snapshot with FORMAL_NOT_PUBLISHED. Local Package requires explicit Formal, introduction, credits and author rights declaration; downloaded canonical JSON includes exact Package/Formal/draft identities, unchanged snapshot and SHA256. External publication is NOT_PUBLISHED and platform capability is UNVERIFIED. A mismatched explicit Formal/Package URL cannot expose the older package's download. No real platform upload or rights verification was performed.

The approved content occupies the accepted WorkspacePaneShell with one root Assistant; it does not import prototype Frame/AppShell/mock data. URL state uses explicit object/version/anchor refs, rejects incomplete or adjacent-object fallback, and marks historical drafts. Chapter/discussion input is scoped across refresh and hide. New responsibility or reply evidence cannot silently replace another chapter after a navigation race.

## Actual verification

| Evidence | Observed result / limit |
| --- | --- |
| `backend-check-final-05.log` | 26 passed across new vertical/API and existing employee-conversation/Package runtime suites. Meaningful scope/parent, concurrent CAS, replay conflicts, UTF16, stale Knowledge, limits, forged provenance, immutable versions, atomic rollback, disable/uninstall retention and shared-service in-flight checks. Controlled fixtures only. 127 existing/test warnings retained. |
| `frontend-check-final-03.log` | 38 passed across Writing and D0/D1 state/API/entry compatibility. Includes uncertain retry identity and mismatched Formal/Package refusal. Existing module-format warning retained. |
| `lint-final-03.log`, `build-final-03.log`, `build-source-match.json` | Scoped lint passed; fresh isolated final-03 production build passed; eight granted frontend paths match the built copy. No dependency installation, env/credential/DB copy or stale build reuse. |
| `closure-checks.json` | Four Python sources compile in memory without bytecode; source/adjacent/prototype/cache/protected DB closure assertions. |
| Browser screenshots, DOM records and `requests.jsonl` | Actual isolated UI, actual local routers and fresh production frontend; controlled foundation identities, no Provider. Collection create, manual author chain, inline missing-introduction feedback/focus, same-chapter/anchor return, refresh/hide input retention and D0/D1 adjacent navigation/Assistant/conversation reads. No full native Desktop/whole-product acceptance. |
| `browser-stale-input-dom.txt`, `browser-other-client.json` | Another client moved draft head. Browser reload retained dirty original input, stale save failed, explicit rebase then save succeeded. Repeated equal inspection clicks produced one current-draft event. |
| `browser-formal-package-mismatch-dom.txt` | New explicit Formal plus old Package shows mismatch and zero download controls. |
| `browser-download-sealed-evidence.json`, `browser-downloaded-package-sealed.json` | Real Chrome visible save gesture produced exact previously absent `/Users/yy/Downloads/writing-local-package (3).json`. 1380 bytes; SHA256 `1c5a3a1db8c88cbd198dd39727dfacc4f35776088272af53dde689f7f80b852d`; bytes match a fresh backend service read. Includes exact Package identity. |
| `runtime-before-cold-sealed.json`, `runtime-after-cold-sealed.json`, `browser-cold-sealed-complete-dom.txt` | Physical backend process restart followed by original URL reload retained exact draft/Formal/Package/download bytes. All 11 Writing events and recorded table counts unchanged by cold reads. Browser manual chain created zero tasks and zero AI usage. |
| `retention-evidence.json` and final backend retention checks | Actual separate isolated instance active→disabled→uninstalled→new-service read preserves Writing event/object and immutable Package fingerprints. Disabled writes reject. No destructive migration or core-reference redesign. |
| `protected-databases-closure.json` | Three protected DBs and nine possible sidecars match preflight size/mtime/SHA; immutable read-only integrity checks are ok. No default/native DB startup or writes. |

The final Browser chapter is `package-object-8ae4a98e-501f-4e02-9cf8-883f1df60e67` in Book `package-object-6ed381e4-bb60-459f-911e-924e37ac665e`, workspace `workspace-package-615933c2-dd07-446a-9132-b56a0c806131`. Final draft `writing-draft-saved-48b7036c-7b0e-4e31-b74e-e4936b7dcfb5`; Formal `writing-formal-confirmed-24fc5b03-59f2-4ed8-a22e-5ba252023bf5`; Package `writing-package-prepared-88329ffc-fc9d-4085-9447-e69c908be8b3`. Earlier immutable packages/files remain unchanged; earlier exports predate the added package_ref field and are historical verification artifacts, not the final sealed output.

## Failures, incident and retained boundaries

Three early download-capture mechanisms timed out (IAB event capture, IAB media capture, Chrome event capture). Their surrounding records remain in the task area; the earlier `(0)/(1)` physical file checks prove bytes, but uncertain browser attribution is not claimed as successful capture. Final `(2)` and `(3)` exact paths were checked absent before visible Chrome save and matched actual bytes afterward. No broad Downloads enumeration, deletion or browser-history cleanup was used. Initial cold reload loading-state screenshot is retained separately; completed-state evidence is `browser-cold-sealed-complete.png`.

First pytest's default cache created five Git-ignored files in workspace root `.pytest_cache/`, outside the exact grant. Exact paths, birth/mtime/hash and recovery copies are in `cache-scope-incident.json` and `cache-scope-incident-final.json`. Delivery Owner explicitly decided CLEANUP NOT AUTHORIZED: retain the five and recovery, no rm/rmdir, no backend cache touch; subsequent tests use an external cache. This is a recorded workflow followup and an actual scope incident. It does not affect protected DBs/business source, does not expand implementation authorization, and cannot be hidden by claiming zero out-of-scope writes. Preflight new-file proposal labels were inherited from PREP before approval; the explicit CEO-approved Issue grant is the implementation authorization.

Real Provider output, production employee execution, native/default App, platform account/capability, external publishing, independent review and full V1 release acceptance remain unverified. No credential, Keychain, platform or user-data access was introduced. Source tests, local API success and Browser evidence do not substitute for those gates. Task-local fixtures, copied builds, downloads and recovery remain REVIEW_REQUIRED; no PROMOTE/ARCHIVE/DELETE disposition is asserted.

## Decision and return

Main Development returns READY_FOR_INDEPENDENT_QA / NOT ACCEPTED. Delivery Owner owns independent QA routing and subsequent acceptance/rejection disposition. QA should consume the exact source seal/build match and replay the bounded local authoring/cold-read chain, provenance and retention checks, then report gaps without widening scope. Real Provider/native/platform followups need their own authorized gates. HANDOFF.md and TASK_OUTPUT_MANIFEST.json enumerate every retained output and evidence location; Owner workflow followup retains the cache incident. No CurrentState, Pointer, Blueprint, canonical backlog or ChangeLog promotion is authorized by this return.

## Appended Owner bounded acceptance · 2026-10-04

Authority Class: REVIEW. Status: Review. Retained output Disposition: REVIEW_REQUIRED; no Current/Frozen promotion. Decision Owner: Curis V1 Delivery Owner. Latest Owner Verdict: **Writing local authoring mechanics IMPLEMENTED / ACCEPTED within tested controlled Package / local Browser scope**. This authorized append records the Owner's subsequent decision; the original QA-ready header/return and sealed bytes remain preserved as the earlier checkpoint.

Independent QA final source: `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-QA-001/REPORT.md`, SHA256 `e861e3385379fba8dea679239b84a5ff4a19dbc54b5bd6db5345ff7f05714c79`, Authority Class REVIEW / Status Review / Disposition REVIEW_REQUIRED. Owner's direct delegation from chat `019ff1ba-f696-7002-8a6c-2b357ded819c` explicitly accepts only this tested local scope and authorizes appending these two original records plus task-local acceptance evidence. No QA report or old seal was replaced.

QA independent checks: 14 Writing backend, 11 adjacent identity/conversation, 7 Writing frontend passed; fresh build `Q_ZvyI8BSQV5hYI21RpdO` and lint passed. Real local Browser download was 1304 bytes, SHA256 `10452328f259968b988570aed5dbc05348e6092aba547bde36948351b06c4bb4`; nine Writing events with row SHA `89fd3818f33b26329a9c9d588ffe71fa5bc1617cec4d985ea2852fd8a696776f` survived physical restart/new client, disabled and uninstalled fresh-service reads. Protected DB closure passed. These are independent QA records, distinct from the author's earlier download/counts.

Accepted mechanics: version/CAS, exact Selection, unavailable execution retaining input, author manual check and explicit immutable Formal, local Package with actual downloaded file, cold reread, disable/uninstall retention. Controlled callback/candidate/adoption tests prove mechanism only and do not accept real AI generation, output quality or Business Result. AUTHOR_MANUAL is not independent review; AUTHOR_DECLARED is not validated rights; no platform publication occurred.

Expanded QA frontend evidence remains **19 total / 17 PASS / 2 FAIL**. The diagnosis `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/regression-diagnosis/REPORT.md` and findings.json reproduce both failures against current, pre-Writing D0 snapshot, and current with exact Writing preimage. Of 24 compared inputs only InstalledWorkspaceRuntime differs. Runtime test85 fails `/CEO 工作台/` in WorkspacePaneShell source, which delegates navigation to V1Sidebar containing the label; this is not the earlier RD/XHS/TTK entry assertions failing. Runtime test165 fails absent `/当前没有可证明的下一责任/` in identical legacy CeoDeskOperating bytes. Neither failing test reads Writing dispatch. All three original runtime runs remain 6 PASS / 2 FAIL; generic Package static contract is 1 PASS in each. This establishes failure provenance, not rendered product acceptance or a license to modify assertions.

The separate historical v2 Core gap test cannot reach parse/assertions because the selective QA copy lacks its referenced JSON (test71 / QA frontend-tests.log348). Original fixture exists, but was not imported or retested for this diagnosis. Verdict for that coverage is **UNEXECUTED / UNVERIFIED**, and no all-suite PASS is asserted.

Still unverified: production carrier installation/user starting flow, real responsibility configuration/employee executor/Provider, independent reviewer, full Book lifecycle/domain E2E, native/default App, platform/account/rights and full Writing business completion. Current unchanged source offers exact-carrier installed dispatch, but this delivery has only isolated installation evidence and no production catalog/onboarding acceptance. Production WritingChapterService defaults allow_execution=False. Responsibility resolution requires one same-workspace WRITING_CHAPTER_AUTHOR, legal execution context, verified explicit bridge and one enabled model; test foundations supply these under controlled labels and cannot prove production binding. No automatic new development follows this registration.

The root pytest-cache scope incident remains retained/read-only with recovery under Owner CLEANUP NOT AUTHORIZED. No cleanup, business source/test byte change, original seal/HANDOFF/manifest or QA report replacement, Git/native/Provider/DB write, or CurrentState/Pointer/Blueprint/Backlog/ChangeLog promotion was performed. New `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/owner-acceptance/` holds DECISION, before-append recovery, unchanged/prefix proof and a supplementary manifest. Next Gate: Owner routes separate authorized production/start/binding and test/fixture followups and any real-execution/native/platform review; bounded acceptance is not full Writing completion.


## 2026-10-05 — CEO bounded built-in Writing definition publication decision

Status: Review · Authority Class: REVIEW / CEO DECISION PROVENANCE.
Verdict: CEO APPROVED — EXACT BUILT-IN DEFINITION / BOUNDED LOCAL CAPABILITY CONTRACT.
Disposition: PROMOTE（仅明确接受的定义/范围/支持政策登记；不是全Review或产品能力升级）。
Owner / Maintainer coordination: Curis V1 Delivery Owner.
Source: Delivery Owner chat 019ff1ba-f696-7002-8a6c-2b357ded819c 转达CEO明确“同意，批准”，接受已解释的candidate限定合同、四文件登记及随后exact实施；不是Agent自行批准。
Target: existing Writing Review decision record；Blueprint / Shared19.1不变。

精确Package `com.curis.local.writing-authoring` version `0.1.0`，digest `2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e`。四源文件：manifest.json SHA `1c102888024e541de7f08f37d2c02ee10acc661da56f3779b43ced94049a96c2`；surfaces.json SHA `f18dbf61bf2b945f063f1479256fabcb6cf63052fff2b6cc937e1ce9005804e6`；schemas/book.json SHA `60397b885ffb4e8e7fd4f04b4293d4517999a82274b5bda5c38362e959ea32db`；schemas/chapter.json SHA `e9fe9cf8f06f3da7f53c04790410029409660d906fbdefb4b2ca99a9e410239e`。来源为原Task封存carrier，未来App承载须精确字节/digest一致；Task路径不是正式安装资产。

批准本地Book/Chapter记录与正文编辑保存、AUTHOR_MANUAL人工检查、作者明确确认不可变Formal及LOCAL_DOWNLOAD。原boundedAccepted/独立QA证据和失败保原级别；真实员工回复/独立审校/外部平台/版权核验/全Writing业务/native/全AppRelease未接受。不是publicRelease，不授权云调用费用。合法创建无模型可继续，AI授权单独核验。

支持精确版本与实测Core/App组合；manifest兼容声明不是全版本矩阵。Curis自有source，Delivery Owner维护协调、授权Writing实现席维护、独立QA验证；不承诺SLA/永久支持。定义不可变，同version不同digest拒绝；未来版本另验收/批准。已有用户对象/正文/Formal/包/Usage不自动改、不删；未测通用迁移，不授权自动迁移/回滚；改动须mapping、在途/UNKNOWN效果、恢复点、权限费用、Resume验证与另行范围。停用/卸载保原Business数据只读；下架不删除用户数据。

Publication definition contract获批不等产品入口已交付。正式启用须完成实际App资产、同一CEO确认原子Business/FirstWorkspace、幂等与同包多Business、真实对象创建、Approved UI和独立入口QA。R02 WRE-A/B/C/D已由Delivery Owner bounded APPROVED DESIGN，handoff SHA dabb32ee65ee4827b9546073a91d4c32c3503eb6eb35fbef236dd57137dfeb15；仅设计状态，持久化/授权/真实执行仍待实施验收。UNKNOWN确认/请求保原快照，不因换Holder或新提案洗状态。

Next Action:正式[CURIS-V1-WRITING-PRODUCT-ENTRY-001](../../issues/CURIS-V1-WRITING-PRODUCT-ENTRY-001.md)按精确27路径实施；四治理文件同步provenance。Next Gate:隔离tests/build roots显式授权、独立QA及Owner final review；真实Provider费用/系统/凭据使用、native exact roots与AppRelease分离。No second Catalog/primitive/schema/executor/Usage；本节不重定义Frozen产品。

Decision candidate来源：artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-READINESS-20261004/PACKAGE_PUBLICATION_DECISION_CANDIDATE.md SHA 9890cc7f086b78e6f3fdb795a25d6dbd267eed3391465cc634aa027c2e3878c7；限定内容已消费，本候选历史身份保留，不修改其Status或自授正式启用。


## 2026-10-05 — Writing entry isolated implementation return, NOT ACCEPTED

Status: Review · Authority Class: EVIDENCE / IMPLEMENTATION BOUNDARY. Disposition: REVIEW_REQUIRED.
[Actual implementation Review](./CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md) and formal Issue CURIS-V1-WRITING-PRODUCT-ENTRY-001 retain the CEO-approved bounded definition, original local acceptance and history. Owner subsequently granted exact fresh isolated validation roots/ports; backend final40 /39PASS/1FAIL, frontend11PASS/scoped lint/build2 PASS; Browser first-instance authoring/CAS and controlled no-outbound UNKNOWN preservation evidenced. This does not accept the product entry, actual Provider/fee/Keychain, native/default App or AppRelease. Second independent Business fails existing workspace_package_instances company/package/version UNIQUE. Owner maintains multi-Business requirement and did not approve Schema implementation; minimum migration design was appended only to existing Task PACKAGE_INSTANCE_GATE.md for CEO decision. No Schema change/migration run or production DB write. Next Gate: CEO/Owner exact migration scope → populated migration evidence → independent QA → Owner final review. Full failures/NOT RUN, source seals and Task Output Manifest are in the Review. This append is evidence routing, not Frozen Product promotion.

## 2026-10-05 — Writing entry authorized schema / lifecycle / return revision

Authority Class: EVIDENCE / IMPLEMENTATION PROVENANCE · Status: Review · Disposition: REVIEW_REQUIRED. CEO “允许” minimum existing-table uniqueness migration; Delivery Owner delegated precise sibling disable/uninstall and WQA20 consumer return decisions, recorded in CURIS-V1-WRITING-PRODUCT-ENTRY-001 amendments01–03 (31→33 exact paths). Low-frequency same-type independent Businesses allowed; multiple Books normally same workspace. No Product/Frozen model promotion.

Actual developer evidence: backend94PASS; frontend13PASS/scopedlint/freshbuild PASS; populated parent-only migration preserves IDs/history/FK and strict rollback/repeat/concurrency, sibling assets retained through last live/disabled reference. Actual model/employee same-window buttons return verified chapter and preserve unsaved text/discussion/selection/UNKNOWN. Physical process boundaries prove precommitUNKNOWN/no replay and committed response-loss idempotency; cross-FS/DB and partial-copy recovery remain bounded risks. Three protected DB bytes equal/integrityok; no Provider/credentials/fees/native/defaultApp/Git.

Old independent QA REPORT SHA12ba4e7bd7a06e60701f19cbc0a990c105e1734a494df59042f690bc7eb89051 accepted by Owner as BOUNDED LOCAL evidence only, old WQA20FAIL/newSchemaNOTVERIFIED/Provider-nativeNOTRUN retained. New developer seal awaits independent QA and Owner acceptance, not Writing/fullAppAccepted. See issues/CURIS-V1-WRITING-PRODUCT-ENTRY-001.md and docs/reviews/CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md plus artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-001/source-seal-schema-01.json, manifest-schema-01.json and HANDOFF_SCHEMA_01.md. Next Gate: new-seal populated migration/sibling/return/boundary independent QA → Owner bounded verdict; remaining product/live/native/release gates unchanged.


## 2026-10-05 — Delivery Owner accepted bounded schema-01 independent QA

Status: Review · Authority Class: REVIEW / IMPLEMENTATION ACCEPTANCE EVIDENCE / OWNER DECISION PROVENANCE.
Verdict / Disposition: BOUNDED_LOCAL_SCHEMA_LIFECYCLE_BROWSER_RETURN_PASS accepted by Delivery Owner; retained bounded evidence, NOT full Writing/App Accepted.
Owner / Decision Source: Curis V1 Delivery Owner, chat 019ff1ba-f696-7002-8a6c-2b357ded819c; CEO delegated bounded decisions.
Next Action / Target Authority: preserve the sealed schema-01 source and independent QA; CG shared-code changes require new baseline/seal and Writing regressions. This append is implementation evidence, not Frozen product promotion.
Next Gate: cross-FS recovery remains PARTIAL; actual Provider/cloud fees/credentials/native NOT RUN and require exact separate grants; full Writing and App release remain open.

Owner independently checked schema-01 REPORT/source-seal/output-manifest, 119 outputs / 33 source hashes / 371 source-copy checks with zero mismatch, protected before/after equality, 11 migration variants, 4 physical process boundaries and actual same-window Model/Employee return evidence. This records the Owner's independent verification, not a new test rerun by this documentation task. The obsolete BLOCKED_SCHEMA_DECISION is historical, not the current blocker. Old WQA20 FAIL, old schema failures/seals/logs and residual assets are preserved unchanged. No QA119 output or physical sealed source was rewritten.

Evidence: artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-QA-001/schema-01/REPORT.md; source-seal.json; output-manifest.json. The three exact SHA256 fingerprints are in the receiving CG task SOURCE_SEAL baseline. Six authorized documentation paths were updated/append-only registered; before/after hashes are explicitly retained there. This does not wash old seal hashes or claim current shared-code hashes still match old sealed physical copies after subsequent CG edits.
