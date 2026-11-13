# Writing product entry implementation

Task ID: CURIS-V1-WRITING-PRODUCT-ENTRY-001
Status: Review
Authority Class: REVIEW / IMPLEMENTATION SCOPE
Disposition: REVIEW_REQUIRED
Owner: Main Development / Writing entry
Decision Owner / Return Target: Curis V1 Delivery Owner · 019ff1ba-f696-7002-8a6c-2b357ded819c
Verdict: BOUNDED_LOCAL_SCHEMA_LIFECYCLE_BROWSER_RETURN_PASS / OWNER ACCEPTED BOUNDED EVIDENCE / NOT FULL WRITING OR APP ACCEPTED

## Authorization and objective

2026-10-05：Delivery Owner转达CEO“同意，批准”，授权限定内置Writing定义及四canonical文件登记，并在建立本Issue后执行原EXACT_SCOPE的27逐路径/owned hunks。该授权不含Provider费用、native默认App、真实DB、Git、表外代码或外部test/build roots。
目标：同一Business Main合法专业提案/CEO确认→原子Business+FirstWorkspace→真实Book/Chapter→唯一责任配置与有效全局模型→服务端fail-closed共享执行准备；保留已Accepted本地authoring/CAS/精确Selection/人工Formal/LOCAL_DOWNLOAD。

## Required inputs / Approved Design

Readiness ENTRY_EXECUTION_PLAN.md SHA d6616fd2619dae88f755f4b2fb1affaa51c19af337d5800033b1b378c6c40060；EXACT_SCOPE.md SHA 80924064c989ec8a0de88e652225e5fd843ea6d9472bc547bab1f315b840768e；publication candidate SHA 9890cc7f086b78e6f3fdb795a25d6dbd267eed3391465cc634aa027c2e3878c7。
R02 WRE-A/B/C/D bounded Approved Design：artifacts/tasks/CURIS-V1-RENDER-BASED-PROTOTYPE-002/evidence/writing-product-entry-20261004/DESIGN_HANDOFF.md SHA dabb32ee65ee4827b9546073a91d4c32c3503eb6eb35fbef236dd57137dfeb15；STATE_CONTRACT.md消费R02优先规则，原prototype Shell不复制。
Current authority：Blueprint→Master Map→UI Blueprint→Shared19 / Shell3.1A；EngineeringLifecycle只1.0A Frozen。原WritingIssue/Review、Owner acceptance及QA保留局部结论。

## Exact Allowed Files / owned hunks

|绝对路径|授权操作/边界|
|---|---|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/main.py`|MODIFY_OWNED_HUNKS：仅 execute_attempt 的已验证章节对话输出上限、选定能力无 fallback；真实 conversation callback/router 注册注入策略。不得改其它默认路径。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/frontend_v1_router.py`|MODIFY_OWNED_HUNKS：ExistingCompanyBusinessIn 与现有 business draft / materialize 路由的同一提案、CEO确认分支；新增专业候选读取消费正式发布决定。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/runtime/first_run_delivery.py`|MODIFY_OWNED_HUNKS：现有 FoundingRun 的 package 专业创建分支；确认结果原子落库与幂等读取；Generic 分支保持原语义。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/workspace_package_runtime.py`|MODIFY_OWNED_HUNKS：抽取现有合法安装事务写入供同一确认事务调用；已发布精确 carrier 的按确认/Business实例化；共享不可变资产复用；原 install 兼容。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/writing_chapter_service.py`|MODIFY_OWNED_HUNKS：服务端逐 scope 执行策略、有效选定模型 binding、选文/知识依据快照、实际来源类别及排队 preflight；不改变人工正式稿合同。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/writing_router.py`|MODIFY_OWNED_HUNKS：严格配置/元数据/模型选择请求、CEO权限检查和共享 execute 调用；客户端不能传 allow_execution。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/conversation_service.py`|MODIFY_OWNED_HUNKS：可选服务端已验证 selection/purpose/preflight 快照；重验后使用同一 Task/executor/callback/Usage；旧调用默认保持。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/orchestrator.py`|MODIFY_OWNED_HUNKS：仅验证真实 conversation.execution_bound 的章节 EMPLOYEE_REPLY Task 后走现有单步 model_gateway_tool；其它 workflow 生成/恢复不改。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/CeoDeskOperating.js`|MODIFY_OWNED_HUNKS：仅 CreateBusiness 导出函数及必要 import：同一 Main 专业提案/确认/真实 Workspace landing；其余旧 CEO desk 正文保持。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/business/page.js`|MODIFY_OWNED_HUNKS：真实 PACKAGE Workspace 用已有 workspaceOfficeHref，现有目录/创建入口回程。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/SharedConversation.js`|MODIFY_OWNED_HUNKS：仅 useConversationModel 的可选 Writing 调用适配与选定元数据验证，使用同一全局 available_models；原调用兼容。ConversationComposer slots 复用。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingWorkspace.js`|MODIFY_OWNED_HUNKS：真实空 Book/Chapter 创建、责任缺口/原 EmployeeDetail 返回上下文；不加业务导航。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingChapterMain.js`|MODIFY_OWNED_HUNKS：统一模型池 composer control、当前选文发送及真实 provenance 展示；保留脏输入/CAS/人工正式稿/局部采用行为。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/writingApi.js`|MODIFY_OWNED_HUNKS：同 scope 配置/有效模型选择/元数据 strict DTO；不暴露路径/任意 executor/授权 boolean。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/v1FrontendApi.js`|MODIFY_OWNED_HUNKS：现有 Business proposal/create API 的专业候选与确认字段；不创建第二 Business create API。|
|`/Users/yy/Documents/Curis AI Workspace/desktop/scripts/build-runtime.sh`|MODIFY_OWNED_HUNKS：仅四个 carrier JSON 与已接受发布凭据的资源打包/校验；本任务不执行脚本。不得在用户 checkout 清理构建产物。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/writing_entry_service.py`|CREATE_AFTER_GRANT：只编排发布证据/资源解析、同一合法确认、现有 employee/role/assignment/identity/binding API；不新建 executor/Usage/primitive。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/writing_authoring/manifest.json`|CREATE_AFTER_GRANT：原 Accepted carrier 四文件之一，未来精确复制且 digest 一致。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/writing_authoring/surfaces.json`|CREATE_AFTER_GRANT：同上。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/writing_authoring/schemas/book.json`|CREATE_AFTER_GRANT：同上。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/writing_authoring/schemas/chapter.json`|CREATE_AFTER_GRANT：同上。|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/writing_authoring_release.json`|CREATE_AFTER_GRANT：正式发布决定的只读派生凭据；须先有 Owner/CEO批准的来源/范围/支持/版本决定及 canonical target，不能自封发布或 Catalog Authority。|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_writing_entry_readiness.py`|CREATE_AFTER_GRANT：合法/拒绝安装、同确认并发、多 Business、真实对象创建、责任配置、权限、打包资源合同。|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_writing_selected_execution.py`|CREATE_AFTER_GRANT：共享执行单调用、模型/身份/选文/知识/assignment变更、callback、Usage失败归属与并发负向。|
|`/Users/yy/Documents/Curis AI Workspace/frontend/tests/writingEntryReadiness.test.mjs`|CREATE_AFTER_GRANT：真实提案→PACKAGE landing→空 Book/Chapter→责任/模型修复回程、输入保留与来源展示。|
|`/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-WRITING-PRODUCT-ENTRY-001.md`|CREATE_AFTER_GRANT：未来正式实施 Issue：上述精确 scope、授权、验收及门槛，Status Review；现在不创建。|
|`/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md`|CREATE_AFTER_GRANT：未来实际验收证据/失败/Disposition；现在不创建，也不代替 Package 发布决定。|
|`/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DELIVERY_WRITING_CHAPTER_REVIEW.md`|CEO限定发布决定登记与最少provenance同步；不覆盖历史、不升格全产品验收。|
|`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`|CEO限定发布决定登记与最少provenance同步；不覆盖历史、不升格全产品验收。|
|`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md`|CEO限定发布决定登记与最少provenance同步；不覆盖历史、不升格全产品验收。|
|`/Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md`|CEO限定发布决定登记与最少provenance同步；不覆盖历史、不升格全产品验收。|

Allowed Directories：上述exact文件的父路径（仅表内文件），以及 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-001`（本Task source preimages、change manifest、静态检查证据、gate request；未经额外授权不建新测试输出目录）。

## Output / acceptance contract

1. 四canonical同步精确批准范围、来源及remaining gates，既有Review原前缀保持。
2. 27路径实施diff与逐文件source hash/owned-hunk证据；四carrier bytes/digest一致；无新primitive/schema/第二Catalog/executor/Usage。
3. R02确认快照不可变、RUNNING/UNKNOWN禁止换Holder/model/send及新建，换页/收起/修复保原请求；失败只能显式同请求重试或结束原确认重新授权，UNKNOWN不能洗掉。
4. 安装同确认幂等、同包多个独立Business不误返旧Workspace；不先Generic创建再install。真实对象parent/scope和actor授权。
5. 唯一实际作者责任与bridge/effective model；缺模型不挡创建；调用授权默认关闭，无费用grant不执行。
6. static-only当前可做内存AST/JS解析与diff；tests/build/browser/isolated roots需一次exact request及Ownergrant后执行；真实Provider/native另Gate。
7. 实际QA matrix准备非执行，所有NOT RUN保留；测试、API200或controlled模型不能替代产品/费用/native验收。

No reset/clean/stage/commit/push/stash/checkout；不删旧cache/历史artifact；不碰保护DB/Keychain。任何prehash未知重叠或表外必要修改先回Owner，routine bug在已授权范围内连续修复。

Next Gate: source implementation → authorized isolated tests/build/browser → independent QA → Owner final review；实际模型/费用/native和AppRelease仍独立。

## 2026-10-05 — Owner exact isolated validation grant

Delivery Owner approved VALIDATION_GATE_REQUEST.md within CEO continuous delivery: new `/private/tmp/curis-writing-entry-20261005-01/` and this Task's `validation-01/` are exact Allowed Directories for freshsource/DB/store/cache/tmp/frontendbuild and test/browser evidence. Before creation both verified absent. Approved:2newbackend+1newfrontend and acceptedWriting/adjacent regressions, lint/freshfrontendbuild, ownednoProvider20311/20312 and actualBrowser entry/concurrency/CAS/cold/UNKNOWN negatives. ThreeDBenv same fresh external beforeimports, dependency read-only reuse/no install/network, no checkoutbuild, no productionDB/defaultApp. Port conflictsSTOP, normalownPIDstop. Provider/Keychain fees/native/packaged not granted. Controlled replies only mechanism. No repeated grant needed for normal scope verification.

## 2026-10-05 — Actual evidence and Owner schema stop

Final combined isolated backend40 /39PASS/1FAIL (second distinct Business violates existing company/package/version UNIQUE); frontend11PASS, scoped lint and build2 PASS. Actual Browser first-instance/Book/Chapter/Holder/model metadata/no-fee fail-closed, CAS and author local Formal/package exercised. Package→Chapter transient mount input loss fixed and Browser retested; default source execution grant still absent. The controlled pending fixture proves lock/query/preservation only, no Provider callback or real Usage. No Schema source changed/migration run. Owner maintains multi-Business contract and requested minimum migration design only, appended to existing Task PACKAGE_INSTANCE_GATE.md. Next Gate: CEO/Owner exact schema decision → populated migration evidence → independent QA → Owner final review. [Actual Review](../docs/reviews/CURIS_V1_WRITING_PRODUCT_ENTRY_REVIEW.md), Status Review / REVIEW / REVIEW_REQUIRED, contains failures and precise NOT RUN coverage.

## 2026-10-05 — CEO / Delivery Owner schema amendment 01

Status: Review · Authority Class: REVIEW / IMPLEMENTATION SCOPE · Disposition: REVIEW_REQUIRED. Latest scope supersedes the earlier schema implementation STOP; implementation remains NOT ACCEPTED pending evidence and independent QA.

Decision maker: CEO explicitly “允许”; further ordinary bounded approvals delegated to Delivery Owner. CEO clarification retained: “业务可以允许同业务多个存在，这在产品上是允许的，但实际场景中使用不会太多”. Same-type independent Businesses are legitimate and low-frequency; multiple Books/tasks normally stay in one workspace. No new hierarchy or default multi-Business UX.

Problem / chosen solution: old company/package/version UNIQUE rejects a second independent confirmed Business. Owner approved existing PACKAGE_INSTANCE_GATE.md minimum migration: replace only the existing instance parent table transactionally to remove that UNIQUE; retain workspace uniqueness, all IDs, row values, digests, history and FK targets. No new ledger, primitive, fake Workspace, version alias or writable_schema.

Additional exact owned hunks only: backend/app/workspace_package_runtime.py PACKAGE_DDL obsolete UNIQUE removal, __init__ migration-before-reconcile, private _migrate_instance_uniqueness/preflight, and install legacy single/multiple ambiguity lookup; backend/tests/test_writing_entry_readiness.py append populated migration/rollback/repeated/concurrent/legacy/multiBusiness/tenant regressions. Existing 31 exact paths otherwise unchanged; append provenance only to this Issue, existing Review and four canonical documents. Allowed task/external directories remain this Task validation-01/ and /private/tmp/curis-writing-entry-20261005-01/ for fresh isolated populated migration DB/build/evidence.

Owned prehash and exact preimages: schema-amendment-preimages.json, captured before amendment; original source-seal.json and manifest.json retained for old QA. All source bytes matched old seal before changes. Protected three DB before-check schema-protected-before-01.json: no sidecars, immutable integrity ok, before/after exact fingerprints equal; never import Runtime against them.

Rollback / STOP: foreign_keys disabled before BEGIN IMMEDIATE only on owned migration connection, restored after explicit commit or rollback. Unknown schema/dependency/custom trigger/index/view or orphan stops before alteration; all populated parent/child values and FK/integrity checked before commit. Any protected DB sidecar or drift STOP. No destructive down-migration after multi-instance population. Legacy single-match behavior retained; multiple matches require actual Business identity, otherwise explicit ambiguity rejection.

Acceptance: populated success and injected transaction failure retain full old row values/IDs/history; repeat/concurrent migration; actual distinct Business creation; tenant/ambiguity/FK checks. Regress disable/uninstall/update/rollback/reconcile; defects outside granted hunks return exact impact and requested hunks to Owner, no implicit source expansion. Fresh source/build and separate new seal go to independent QA. Real Provider/Keychain/fees/native/public release and production DB mutation remain separate gates.

## 2026-10-05 — Delivery Owner delegated lifecycle amendment 02

Status: Review · Authority Class: REVIEW / IMPLEMENTATION SCOPE · Disposition: REVIEW_REQUIRED. Decision maker: Delivery Owner, under CEO explicit ordinary bounded approval delegation. Actual schema-backend-01.log retains 18PASS/3FAIL: two real sibling disable/uninstall failures, one tenant-test exception expectation mismatch (actual PackageScopeError correctly rejected foreign tenant; test expectation fixed without relaxing authorization).

Approved exact additional owned hunks: existing workspace_package_runtime.py disable and uninstall only, plus existing readiness test sibling/concurrency regressions. Source bytes immediately before these edits retained in lifecycle-amendment-preimage.json. Problem: global package/version state and shared asset removal incorrectly disable/archive independent siblings. disable changes target only; shared definition remains ACTIVE if any tenant/package/version ACTIVE sibling, otherwise DISABLED, preserving single-instance behavior. uninstall archives target only, duplicate rejects by target ARCHIVED; definition UNINSTALLED and assets removed only after last non-ARCHIVED tenant/package/version reference. Counts cover same-tenant other companies without granting callers sibling business access or writes.

BEGIN IMMEDIATE owns target revalidation/refcount/state changes and asset move; DB or move failure rolls back rows and restores moved assets with prior strategy. Exact owned store only. Cross-filesystem/DB process crash is an existing recovery/UNKNOWN boundary, not a full atomicity claim; retention or restoration failure STOP/report. No archived instance revival, sibling rewrite, new source path or unrelated lifecycle redesign. Verify active/disabled/archived/cross-company siblings, last reference, duplicate uninstall, create/uninstall race, move/commit restoration and retained single API regressions. Protected DB / Git / native / Provider gates unchanged; independent QA remains next acceptance gate.

## 2026-10-05 — Delivery Owner delegated WQA20 amendment 03

Status: Review · Authority Class: REVIEW / IMPLEMENTATION SCOPE · Disposition: REVIEW_REQUIRED. Owner approved actual repair-consumer closure after independent old-seal WQA20 P1: model link enters sample settings with no model controls, EmployeeDetail drops Writing return_to. Decision maker: Delivery Owner under CEO ordinary bounded delegation.

Exact added Allowed Files (31 → 33 records/source paths): /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js — only Writing return_to parsing, actual Company/collection/chapter scope validation and return button; /Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/employees/[id]/page.js — only Writing return_to parsing, employee Company consistency and chapter return. Exact parent directories only these files, no adjacent page/style redesign. Prehash/full old bytes repair-amendment-preimages.json. Preserve actual model Provider/connect/recover/secret/Keychain/default preference logic, ordinary Employee list and Conversation semantics.

Existing granted hunks: WritingChapterMain model repair link to actual /ceo-office/capabilities; writingApi shared strict Writing return validator and actual API scope verification; writingEntryReadiness test positive/negative return cases. Reject host/protocol-relative/javascript/encoded traversal/conflicting duplicate or unknown query scope; never trust client Company parameter. Actual authorized Writing DTO must prove Workspace/Book/Chapter ownership. Missing pair can only return verified workspace with truthful label; invalid/unauthorized leaves ordinary return available. Same chapter input/selection/request restored using existing storage; pending/UNKNOWN unchanged.

Existing external fresh source/build/scoped lint/tests/Browser allowed for these hunks. No real credentials/Provider calls/fees/native/default App/protected DB/Git. Old QA seal remains unchanged; migration and repair results get separate new combined seal and independent QA. Approval impact: two existing consumers gain bounded return entry, no product model or global Provider behavior change.

## 2026-10-05 — Amendment implementation return

Latest Verdict: IMPLEMENTED / BOUNDED LOCAL DEVELOPER PASS / NEW-SEAL INDEPENDENT QA REQUIRED / NOT ACCEPTED. Final backend94PASS; frontend13PASS, scoped9-file lint and freshwebpack build PASS; actual same-window model/employee→originalchapter/input/selection/UNKNOWN tested. Populated table migration and shared instance lifecycle preserve identity/history/FK; physical precommit crash remains UNKNOWN/no replay, committed lost response reads original identity. Protected3DB fingerprints equal/integrityok/no sidecars. Old QA bounded evidence accepted by Owner only, WQA20FAIL and schemaNOTVERIFIED kept in old report. This source revision awaits new QA. Exact failures and crash/Provider/native limits in actual Review appendix; no own acceptance. Output manifest-schema-01.json; source-seal-schema-01.json; HANDOFF_SCHEMA_01.md.

Historical top verdict before this authorized revision: Verdict: PARTIAL IMPLEMENTATION / BLOCKED_SCHEMA_DECISION / NOT ACCEPTED.


## 2026-10-05 — Delivery Owner accepted bounded schema-01 independent QA

Status: Review · Authority Class: REVIEW / IMPLEMENTATION ACCEPTANCE EVIDENCE / OWNER DECISION PROVENANCE.
Verdict / Disposition: BOUNDED_LOCAL_SCHEMA_LIFECYCLE_BROWSER_RETURN_PASS accepted by Delivery Owner; retained bounded evidence, NOT full Writing/App Accepted.
Owner / Decision Source: Curis V1 Delivery Owner, chat 019ff1ba-f696-7002-8a6c-2b357ded819c; CEO delegated bounded decisions.
Next Action / Target Authority: preserve the sealed schema-01 source and independent QA; CG shared-code changes require new baseline/seal and Writing regressions. This append is implementation evidence, not Frozen product promotion.
Next Gate: cross-FS recovery remains PARTIAL; actual Provider/cloud fees/credentials/native NOT RUN and require exact separate grants; full Writing and App release remain open.

Owner independently checked schema-01 REPORT/source-seal/output-manifest, 119 outputs / 33 source hashes / 371 source-copy checks with zero mismatch, protected before/after equality, 11 migration variants, 4 physical process boundaries and actual same-window Model/Employee return evidence. This records the Owner's independent verification, not a new test rerun by this documentation task. The obsolete BLOCKED_SCHEMA_DECISION is historical, not the current blocker. Old WQA20 FAIL, old schema failures/seals/logs and residual assets are preserved unchanged. No QA119 output or physical sealed source was rewritten.

Evidence: artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-QA-001/schema-01/REPORT.md; source-seal.json; output-manifest.json. The three exact SHA256 fingerprints are in the receiving CG task SOURCE_SEAL baseline. Six authorized documentation paths were updated/append-only registered; before/after hashes are explicitly retained there. This does not wash old seal hashes or claim current shared-code hashes still match old sealed physical copies after subsequent CG edits.


## 2026-10-05 Native build layout compatibility amendment

Task: CURIS-V1-WRITING-NATIVE-BUILD-COMPAT-20261005. Status: Review. Authority Class: IMPLEMENTATION SCOPE / OWNER DECISION. Disposition: REVIEW_REQUIRED.
Delivery Owner authorized only desktop/scripts/build-runtime.sh's @swc/helpers lookup and pnpm virtual-store materialization blocks. Support materialized npm standalone and pnpm standalone without dependency/version changes or absorbing CG. Exact output grant: TASK.md, OWNED_CHANGES.diff, TEST_EVIDENCE.md, source-seal.json, output-manifest.json and evidence/ under artifacts/tasks/CURIS-V1-WRITING-NATIVE-BUILD-COMPAT-20261005/. Optional external fixtures only /private/tmp/curis-writing-build-compat-20261005-01/. No Git, DB, App, install or native execution. Actual layout tests plus syntax validate this bounded candidate; next Gate is independent QA new native packaging.


## 2026-10-05 Explicit frontend bundler choice amendment
Task: CURIS-V1-WRITING-NATIVE-BUILD-COMPAT-20261005. Status: Review. Authority Class: IMPLEMENTATION SCOPE / OWNER DECISION. Disposition: REVIEW_REQUIRED.
Owner exact grant adds only desktop/scripts/build-runtime.sh frontend build command block. CURIS_FRONTEND_BUNDLER=webpack invokes pnpm build --webpack; absent/empty preserves pnpm build; unknown nonempty fails before invoking frontend build. No dependency, network policy, shim, native execution or CG add-data change. QA B1-RETRY-02 under network deny stalled default Turbopack; causality is UNKNOWN, not attributed as confirmed IPC/network failure. Next16.2.10 help confirms --webpack. Previous layout patch/source77f0 remain sealed; new command-only overlay separate. Prehash: 23a4c3727bd46086cf44c50029fde838b92c052a330c356c97bb93bbf7fbf8b9.
