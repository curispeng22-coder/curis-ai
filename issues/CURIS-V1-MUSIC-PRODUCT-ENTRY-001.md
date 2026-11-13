# CURIS-V1-MUSIC-PRODUCT-ENTRY-001

Status: Review
Authority Class: REVIEW / IMPLEMENTATION SCOPE
Disposition: REVIEW_REQUIRED
Owner: Curis V1 交付负责人
Executor: Main Development
Return target: Owner chat 019ff1ba-f696-7002-8a6c-2b357ded819c

## Objective and approved decision

Deliver a bounded first Song vertical on existing Package/Core, Shared Conversation, Task/Gateway and sole Usage ledger. Preserve market → direction → Song → audition → Master → release → analysis → next Song as remaining full-product coverage.
Owner approved G-HOLDER and G-ASSET on 2026-10-05: runtime_entities PACKAGE_DOMAIN_OBJECT sole Music primary; finite Song/LyricsVersion/ProductionVersion/Candidate/AudioAssetVersion/Choice/MasterRevision/ReleasePackage schemas; mapped generic create refuses, no workspace_package_objects duplicate. No DDL/new core primitive/ledger/executor. Version heads independent; Choice differs from Master and publication. Explicit owner confirmation, append-only Master revision, CAS and immutable original rights/credits/version/audio basis.
Problem: generic package dual projection lacks typed immutable version/asset/master semantics. Reuse existing generic core carrier with finite domain validation; validate parent/scope, rollback, concurrency and file/DB non-atomic failure boundaries.

G-DESIGN: Owner independent R2 verdict BOUNDED_SONG_LOCAL_MEDIA_INTERACTION_DESIGN_APPROVED_FOR_IMPLEMENTATION. Design manifest SHA 1dbcfb929296363e27b9e0cbf6f209c208f54755f1eaa0ef24155ae6056297a6, 196 outputs verified by Owner. Use Frozen Shared/D0 and current R2 bounded interaction. Preserve per-asset player clock/paused state across reference/fold/version operations; one player; return-to-range restores valid start. Not full Music/audio generation/commercial Master/runtime/native acceptance.

## Required inputs

AGENTS → CURIS_CURRENT_ENTRYPOINT → CURRENT_STATE and Pointer Current Required; scoped Frozen Music/Shared/D0 inputs recorded by readiness; CANONICAL_MAP and EXACT_IMPLEMENTATION_SCOPE of CURIS-V1-MUSIC-CANONICAL-READINESS-20261005; current R2 DESIGN_HANDOFF and Owner independent review. Prior CG/Writing source baseline only implementation provenance; preserve unrelated dirty hunks.

## Allowed files and directories

Exactly 28 source paths and owned functions/hunks from approved readiness table below. Fresh baseline and preimages: artifacts/tasks/CURIS-V1-MUSIC-PRODUCT-ENTRY-001/SOURCE_BASELINE.json and evidence/preimage. Issue and Review exact paths additionally granted. Parents grant only listed files, not whole directories.
|Absolute path|Fresh prehash|Proposed owned scope|
|---|---|---|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/workspace_package_runtime.py`|`9825cdb661aa435e4193f00d8563998943fa3f6082c112b0c8a9f164eebad7aa`|validate_package finite canonicalEntityBindings只增加现有PACKAGE_DOMAIN_OBJECT target；create_object mapped refusal文案/精确guard；不改DDL/install/migrate/validated_data|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/conversation_service.py`|`b14bbeb13c8a1ae10efe84b641450c487ca9517678c0a0af7596181d4f93a36c`|references Music-qualified PACKAGE_DOMAIN_OBJECT version只读；prepare/execute有限Music purpose保原Writer/CG限制；不改append_ceo或另executor|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/conversation_router.py`|`b17c9110aae5d8b0d69665472dc5aa1bbee6a676d1a2296d6e9cb768bcb56829`|ReferenceIn只增加Music授权的PACKAGE_DOMAIN_OBJECT kind；保MessageIn/extra=forbid；typed audioselection在MusicDTO|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/main.py`|`dd1b2edd80481e8e4cd4ca23bf9529a1e1e890612f6ba136c7b28e9d78d7150e`|create_app Musicservice/router/purposevalidator注入；execute_model_gateway既有boundpurpose/预算/singleclaim标签；保原Writing/CG event/key|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/orchestrator.py`|`850daaf5897a08603cc6c0aebbb6750666a3edc6bfdff2669f82cc5a1e8c481a`|_writing_reply_selection commonfinitepurpose+run现有single-step目的描述；无新workflow/Toolexecutor|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/frontend_v1_router.py`|`f4a7a2e36da033b59cf2ccb8c19eaaf855de5e4be05888b024abb48fb44d893c`|business_definitions/create_business/save_business_draft＋resolver参数只添exactpublishedMusic；保Generic/Writing/CG|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/workspace/InstalledWorkspaceRuntime.js`|`b979652e885152e8eb53431e1d3dea4b73c70a7f81ee8d16e9a2f2db7718b041`|exactMusicid/version/digest/schema dispatch；沿用D0pane，不复制Shell|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/CeoDeskOperating.js`|`0db03be8219028149f40e38195f3094233f5cd49b323f9c7724d07ae17502360`|CreateBusiness definitions/name/notices Music条目，仅正式发布可显示|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js`|`6b82fa775cd3c4a4c1a218818df8c671529a9b436a6eb1e3f391d36e8bab2d14`|Music return finite parser/scoped验证/按钮；Provider/credentials配置逻辑不改|
|`/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/employees/[id]/page.js`|`88d21798d9b0174608932372a1b480713ff8268f9bfca75e670f910f081555f4`|Music return branch有限同Song/版本/候选/asset/time anchor；既有employee加载/编辑不改|
|`/Users/yy/Documents/Curis AI Workspace/desktop/scripts/build-runtime.sh`|`1b5536c19b684b54c3a29a5efe6d5af87970b0016daa3c8cb1751977ba901df6`|workspace PyInstaller仅Musicbundle/release两add-data行；保Writingcompat与CG资源，noNative本grant|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/runtime/music.py`|`ABSENT`|唯一typed Music holder commands；受控PACKAGE_DOMAIN_OBJECT根与有限子kind；sameconnectionCAS/parent/immutable/receipt|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/music_entry_service.py`|`ABSENT`|exactdefinition/release/actor/scope/currentAssignment/identity/model/servergrant与原请求锁validator|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/music_service.py`|`ABSENT`|combine现有holder/Conversation；collection/content/qualifiedrefs/typedselection/bind/send/read/materialize/Choice/Master/ReleasePackage，非第二执行器|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/music_media_service.py`|`ABSENT`|唯一ownedbyte store/register/scopedopaqueID读取/Range/hash/size/metadata/rights/MIME/symlink保护；不任意URL/Cloud|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/music_router.py`|`ABSENT`|严格typed DTO与scopedcommand/query/media route；query不得execute，extra=forbid|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/music/manifest.json`|`ABSENT`|候选exactidentity/version/compat/map/retention/support；MusicSong mappedroot|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/music/surfaces.json`|`ABSENT`|合法Song专业surface；用D0/Shared，不第二导航|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/music/schemas/song.json`|`ABSENT`|Package v1 scalar surface descriptor，typedpayload真验证在Music holder；不压nested为string|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/music_release.json`|`ABSENT`|published:false/decision:null默认，真实scope/knownlimits/hash；另publicationGate|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/music/MusicWorkspace.js`|`ABSENT`|actualscope/collection/同Song回程、原请求优先、D0Context/Utility|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/music/MusicMain.js`|`ABSENT`|已批准Song设计消费：明确保存歌词/制作、候选实际audio试听/Choice/Master独立；默认隐藏讨论/旧依据只读|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/music/Music.module.css`|`ABSENT`|仅专业域approveddesign样式/tokens/可读focus；无全局Shell修改|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/musicApi.js`|`ABSENT`|typedscopedcommands/readonlyquery/opaqueassetURL/同对象修复回程；无legacyfallback|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/musicState.mjs`|`ABSENT`|UTF16/seconds locator+immutablebasis+原requestlock+perSong输入缓存/exactreturnparser|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_music_canonical_entry.py`|`ABSENT`|隔离actualholder/CAS/rollback/parent/company/versions/immutableMaster/ReleasePackage/legacypackage|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_music_selected_execution.py`|`ABSENT`|existingShared controlled actualTask/Usage/claim锁/0outboundquery/UNKNOWN/noFallback/WriterCG回归|
|`/Users/yy/Documents/Curis AI Workspace/frontend/tests/musicEntryReadiness.test.mjs`|`ABSENT`|finite locator/expiry/return/hash/lock/requestidentity与跨Song输入隔离；Browser实操另evidence|


Task products only artifacts/tasks/CURIS-V1-MUSIC-PRODUCT-ENTRY-001/; external /private/tmp/curis-music-entry-20261005-01/{data,media,staging,logs,evidence,build}, and exact inputs/demo-a.wav,inputs/demo-b.wav. Three DB environment variables must equal external data/curis.sqlite before imports. Protected DBs fingerprint/read-only integrity before/after. No listening ports authorized. No native/default App/real Provider/fees/Keychain/publication/Git changes/cleanup. No canonical Pointer/Current State/Change Log grant: do not promote this Review into Authority.

## Outputs and evidence acceptance

Source-only bounded implementation, candidate bundle published:false/decision:null, focused isolated tests and Shared Writing/CG regressions; actual immutable holder/media read Range/hash/duration/symlink/rights/parent/CAS/idempotency/concurrency/restart/rollback; existing controlled selected Task/Usage/UNKNOWN/noFallback and zero-write query. Frontend tests/build and later scoped browser evidence; tests/fixture/audio samples do not prove formal Company activation or full Music/provider audio/rights/native.
Task source seal/owned diff/test logs/protected after/input provenance/handoff/output manifest all REVIEW_REQUIRED. Keep failure records. Orphan bytes retained unreadable, never automatically delete. Media inputs exact source/hash from evidence/input-media.json for noncommercial local test only, no lyric-vocal matching or commercial rights assertion.

## Risks and next gates

File publication and DB are not atomic: content-address verify/fsync/rename precedes scoped registration; orphan never becomes readable without canonical asset row. Current assignment/actor/capability/model/server grant must revalidate at actual claim. Pending/UNKNOWN blocks changing Song/employee/model in same workspace; read-only query does not execute.
Next Gate: Owner independent implementation acceptance; exact definition publication, ordinary Company/business/first workspace, browser ports, real media Provider and licensing, native package and full Music flow separately pending. No self-acceptance.

## Owner bounded Browser grant (2026-10-05)

Owner approved self-owned backend 127.0.0.1:21421 and frontend 127.0.0.1:21422 only, free check before start; external build/ source/config/scripts/cache with source closure SHA, no .env/user DB/secrets/old generated packages/dependency download. Existing approved dependencies read/copy only, no install/Corepack. Server-owned controlled grant only, guard outside owned loopback; no real Provider/fees. Test Company/Dept/candidate install/responsibility fixtures explicit, not formal ordinary Company/business activation. Record effective API base, argv/PGID/build ID, DOM/screenshots/actual media clock, cold restart/no duplication/protected before-after, normal owned process exits and free ports. No native/Cloud/Keychain/publication/Git/Authority promotion. Problem: source/test evidence lacks real Browser player/version/return proof; effect limited to external state and own processes. Next Gate: Owner independent QA, ordinary entry/publication and full Music G2/G4.
