# CG product entry · first real graphic vertical

Task ID: CURIS-V1-CG-PRODUCT-ENTRY-001
Status: Review
Authority Class: CURRENT / IMPLEMENTATION SCOPE / OWNER DECISION PROVENANCE
Disposition: REVIEW_REQUIRED
Owner: Main Development / CG product entry
Decision Owner / Return Target: Curis V1 交付负责人 · 019ff1ba-f696-7002-8a6c-2b357ded819c
Verdict: FORMAL ISSUE PREPARED / CODE GRANT PENDING / NOT IMPLEMENTED / NOT FUNCTIONALLY ACCEPTED

## 1. Objective and current authorization

完整 CG 目标保持。第一真实纵向交付：合法精确定义与canonical Business/First Workspace→图文Content/Version→编辑/原子保存→当前Assignment/Employee下显式eligiblemodel员工建议→原请求核验→candidate回专业Main→人工明确采用写canonicalVersion/引用依据→同内容返回→真实保存/请求/采用重启连续。其余三个格式、账号经营/逐账号发布回执、复盘/学习/下一周期不因第一graphic被删除或宣布完成。

2026-10-05 CEO最新委派：目标内bounded技术、接线、兼容、测试由Delivery Owner结合使用场景与产品逻辑批准，不为普通实施方案反复向CEO请求；重要问题/方案/批准/依据/exact scope/影响风险/实际证据/后续必须记录。产品Authority冲突、第二canonicalTruth、保护DB变化、系统Keychain/凭据、真实云费用、发布仍有独立Stop Gate；NO COMMIT/PUSH/RESET/CLEAN/STASH。

本轮直接Owner授权只创建两文件：本Issue与 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/OWNER_IMPLEMENTATION_DECISION.md`。允许目录为既有 `/Users/yy/Documents/Curis AI Workspace/issues/` 和既有 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/`，不授权其它文件写入。下方27源码是将获批范围，**尚无正式代码写入grant**；不会因为正式Issue已存在而自动实施。Owner正等Writing schema-01独立QA最后封存，之后另给同轮27路径代码grant。没有创建未来task工区或外部root、没有服务/DB连接/测试/build/native/Provider调用。

## 2. Required inputs and accepted decisions

最小链：AGENTS→CURIS_CURRENT_ENTRYPOINT→PRODUCT_DOCUMENT_POINTER Current Required→唯一Product Blueprint、Master Map、UI Blueprint→Frozen CG Domain/Company OS Shared/Shell §3.1A。Implementation链为CURRENT_STATE→本Issue/Owner确切grant→实际source→独立Accepted evidence；没有把Research/prototype/API200当产品交付。

Readiness经Owner接受为**实施输入，非功能验收**；原四文件保留原hash/Status/Disposition，不因新决定重写：

|输入绝对路径|SHA256|
|---|---|
|`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/ENTRY_EXECUTION_PLAN.md`|27151efe21d7d0642788023df8346e92ca0b0ed3f8e63fb80e75ba154e4505de|
|`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/EXACT_SCOPE.md`|f5b86b0e9571cd03f77149dbebef28f617901eefc1241749296dce079a751645|
|`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/CAPABILITY_BOUNDARY.md`|cefb16a41482b626352643445a76f799ab2debd07d2c5da93be541714470bda4|
|`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/output-manifest.json`|eb30a0785bd47ebabfa93e4e65f15981683cac4a74a6c6a64d077a38dedf3743|

### R03 bounded Approved Design

Owner报告独立tab10实际复评三项PASS，批准BOUND​ED APPROVED DESIGN：列表原请求回程不执行、不解除锁；采用资格给具体合并原因并不回写basis；UTF-16选段有效回定位、过期只读原依据/重新选择。R02普通语言/密度等局部接受边界保持。此批准是专业局部设计输入，不是原型持久化或Runtime功能验收；本Agent未重跑Owner的Browser操作。

设计目录：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-RENDER-BASED-PROTOTYPE-002/evidence/cg-graphic-vertical-20261005/`。

|获批准源|实际采样SHA256（与Owner前缀一致）|
|---|---|
|entry-states.html|ed0e8f7e08a051f17f39fa1ec031d5821e3328489071afe37fa07c7c4e5ea47b|
|entry-states.css|a30d15b3c7a92747320dc32dc3231d024d993ad4cc83cddb3cf8f792727bde91|
|entry-states.js|16ee02152928bdd2aa974872981303417230bc8fe44f2cbe7ac33622947c3170|
|source-seal.json（批准时R03 seal）|60d94e0e25e62d076fa20d19baae217d08f4b7c13e12fc4c329cbbc7d58057d1|

最新 DESIGN_HANDOFF R03已读；本次采样hash c17b63b5d16197b07fbb6d993008e8ffa6c790d450e58095284e60f2ae5c4eb7。Owner已通知UI追加批准记录；若读取时追加尚未可见，接受来源为本Issue/Decision记录的直接Owner授权，最终追加复读结果在Decision末尾登记。它不是Frozen冲突，不自行修改UI记录；代码grant前必须消费最终Owner追加与精确接受hash，而非仅R02。

### Owner 已批准映射，尚未批准运行

1. G-CARRIER：现有Package v1 manifest新增optional canonicalEntityBindings；key必须合法且对应所声明domainSchemas，target为有限的已有canonical类型，首CG只消费CONTENT_ITEM及其CONTENT_VERSION关系。无字段旧包原语义保持，未知字段/映射fail-closed。generic create_object对绑定类型拒绝写workspace_package_objects；canonical Version只能经过严格域命令/合法parent，不是任意通用对象创建。无第二Content系统、不fakeXHS，不放松Blueprint/parent/tenant。
2. 同connection atomicCAS：Version/link/head/receipt在同一事务；失败零残留，expectedVersion冲突保输入，重复请求幂等。candidate不占head；采用明确人工action追加已有CONTENT_VERSION与不可变refs/selection/basis，不能连Review APPROVE→SCHEDULED、不能伪completedWork。
3. G-EXECUTION映射：已有Shared执行/Task/Employee identity/global model/唯一Usage按purpose分派；strict query只读原request，不执行；UNKNOWN noReplay。Writing原目的、原事件/key、返回和限制保留；只有代码grant后才改同共享source。
4. Readiness与上述普通映射决定已接受，无需再次向CEO请求同项批准。若实现实际需要新canonical primitive/大DDL或Frozen无法成立，精确STOP / REPORT，列最小不变量冲突/Owner/恢复入口，不偷造第三Truth。

## 3. Future exact code scope — pending next Owner grant

Fresh prehash采样时间：2026-10-05T06:15:28.673314+08:00。27路径=12existing＋15ABSENT；与readiness prehash比较0漂移。整个文件hash不证明我拥有整文件；只允许下列owned函数/片段在将来明确grant后修改，不覆盖其它dirty改动。新函数的有界私有helper不得借“等”无限扩展；表外path/函数需Owner精确补grant。

|绝对路径|将获批 owned functions/hunks|fresh prehash SHA256或ABSENT|理由与限制|
|---|---|---|---|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/runtime/workspace.py`|create_content_item、add_content_version；新增 _require_content_authoring_scope/_insert_content_version_in_connection/adopt_content_candidate（仅这三个有界新增接点）|b896cb1a4096e132e67aec48fe9d0feb1c531466067d493e1b39121cc8e07be9|获批PACKAGE→canonical Content；共享连接下atomicCAS；保旧XHS/TTK，_business_type/_blueprint不得全局放宽|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/runtime_foundation_router.py`|ContentItemIn/ContentVersionIn；create_content_item/add_content_version/workspace投影的CG字段白名单；execute_content_stage仅CG错误接线防护|b6ac7fcaa09818f3c2aa169077fc536a22c78c3243416eff0149771118af7a76|新增可空domain字段/expected_version/request_id；CG必填版本要求，legacy DTO兼容|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/frontend_v1_router.py`|business_definitions、create_business、save_business_draft及build_frontend_v1_router定义resolver注入|235ceb0d0aa977e14fdc4f6bb42fa8c7445b430d7721e19965444c6282fd77fb|已批准定义按exactpackage映射；保Writing/Generic响应与真实确认|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/conversation_service.py`|references、prepare、execute；新增严格只读read_request/read_attempt；selection_validator用途分派接点|dffee56e3eed6056693f1546cf7b3ed69582d898d087ccdf01710df546a03963|typed refs/Selection snapshot；原claim/Task/Usage复用，成本/模型/并发/UNKNOWNguard；不另executor|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/conversation_router.py`|ReferenceIn（仅可选version/purpose/locator及canonical内容type）；既有MessageIn兼容|409e1ee5b9748f125424d031624ba077c6aeba1e288ee0ce6dd936f33715f11d|共享typedref输入保extra=forbid；服务端资格校验，客户端不能提交grant|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/main.py`|execute_model_gateway内bound selection/预算/physicalclaim/noFallback段；create_app内Conversation/CG router注册与用途分派|2a27434ba39485b21a507474ef603ee540529290af977414cbd812bb381b03ab|同Gateway/Usage；Writing原事件/key/限制保持；execute_runtime_business legacy/RD不改|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/workspace_package_runtime.py`|validate_package：可选canonicalEntityBindings有限映射验证（G-CARRIER批准后）；create_object：声明canonical类型拒绝generic包对象写入|b20fd75e0e2d5dc7c8020112158ad7fe518017a21f884ec7eca8d1db42b192da|防第二Content holder；PACKAGE_DDL、uniqueness迁移、install、disable/uninstall不重做；无DDL|
|`/Users/yy/Documents/Curis AI Workspace/desktop/scripts/build-runtime.sh`|workspace PyInstaller --add-data资源声明两条精确CG bundle/release；其余命令不改|ca8ebeab2f99afa3156f93d16b6a0a3f3092f3a3d2d59cd08037058fb30e2424|fresh packagedApp必须含CG资源；原Writing打包声明保留|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/workspace/InstalledWorkspaceRuntime.js`|InstalledWorkspaceRuntime精确definition dispatch与入口校验|77b0d0f5452a089fd92b5b2c933f827879c65207d75aa8c46752342f80381f3d|接已有D0 WorkspacePaneShell，CG专业对象读canonical holder，不复制globalShell|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/CeoDeskOperating.js`|CreateBusiness：definitions集合/名称/限定能力notice/选择；其余CEO desk函数不改|e20859a6f2c43d688f9b9b8a8616e245dff45f7ba55567ec203a1cacfae68172|同一Main创建入口，不硬编码每专业实例Writing名称；旧Writing/Generic可用|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js`|既有返回处理/返回按钮的CG分支；Provider/credential/connection/preference逻辑不改|da11e6b5aa1a95dbddd4870973110ecc71d05c5076169d8de9c6706b23b7a0e7|实际修复模型返回同CG对象，原Writingreturn分支保留|
|`/Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/employees/[id]/page.js`|既有返回处理/返回按钮的CG分支；employee档案行为不改|06f1d87309eb2d6d7b8a68f82388220a1d9645867186bfbfcba766d34e5afeef|返回真实授权内容/version/anchor，外部或不合法scope拒绝|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/content_growth_entry_service.py`|NEW：publication/definitions/proposal/authoring_scope/execution_policy/validate_execution_selection|ABSENT|有界domain service；消费现有发行/Package/Assignment/identity/global models，非第二catalog或模型池|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/content_growth_service.py`|NEW：collection/content/command/resolve_references/selection/bind_discussion/prepare_message/query_request/materialize_candidate/adopt|ABSENT|组合现有runtime Content与Conversation/events；无新store/Task loop|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/api/content_growth_router.py`|NEW：build_content_growth_router、严格DTO；collection/content/command/discussion/send/query/candidate/adopt路由|ABSENT|scopedCompany/Workspace/Content入口；query不execute，server grant不能客户端改|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/content_growth/manifest.json`|NEW：精确definition身份/版本/兼容、专业surface与既有canonical binding批准契约|ABSENT|候选发行载体；G-CARRIER/PUBLISHED决定后才生成|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/content_growth/surfaces.json`|NEW：graphic专业surface/Main/按需Context/Utility描述|ABSENT|沿用Package合同合法声明；不生成第二Content collection|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/content_growth/schemas/graphic.json`|NEW：graphic字段形状/大小限制/所消费canonical类型的批准映射|ABSENT|这是定义schema描述，不是新的DB ContentGraphic；禁止generic持久化副本|
|`/Users/yy/Documents/Curis AI Workspace/backend/app/bundled_workspace_packages/content_growth_release.json`|NEW：source files/digest、精确scope/version/批准provenance、compat/support/retention/real capability边界|ABSENT|正式发行决定后才写批准，不使用候选自签hash充已发布|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthWorkspace.js`|NEW：scope collection/对象选择/return/责任EmployeeBar/按需Discussion/Utility宿主槽位|ABSENT|无新的一级导航/global assistant；D0/SharedComposer复用|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthMain.js`|NEW：主题受众/正文、版本/CAS冲突、候选compare/checks/明确adopt/原请求核验状态|ABSENT|消费ApprovedR03及已接受R02局部语义；正常主面普通中文、1280x720正文可见|
|`/Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowth.module.css`|NEW：只作用于本专业surface的ApprovedR02样式|ABSENT|消费既有tokens；不改全局Shell/主题/设计系统|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/contentGrowthApi.js`|NEW：scoped existing content helpers＋CG commands/query/candidate/adopt|ABSENT|不得legacy fallback；校验DTO身份与真实错误边界|
|`/Users/yy/Documents/Curis AI Workspace/frontend/lib/contentGrowthState.mjs`|NEW：typed selection/refs/pending request/basis状态、严格return parser/local未提交缓存键|ABSENT|tenant/actor/完整scope对象版本隔离，恢复不能自动send|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_cg_content_entry.py`|NEW：入口/定义/完整scope/create/atomicCAS/candidate/adopt/legacycompat/事务rollback/restart|ABSENT|fresh隔离DB；真实holder，拒绝fake平台/第二库|
|`/Users/yy/Documents/Curis AI Workspace/backend/tests/test_cg_selected_execution.py`|NEW：真实shared调用链的controlled executor、identity/model/refs/预算/singleUsage/原query/noReplay/physicalcrash|ABSENT|controlled与realProvider证据分开；不读取凭据/不收费|
|`/Users/yy/Documents/Curis AI Workspace/frontend/tests/contentGrowthEntryReadiness.test.mjs`|NEW：请求scope/不可变snapshot/原锁/return非法与版本stale/多对象缓存隔离|ABSENT|不以组件markup镜像代替Browser操作；使用既有测试runtime|

此27表按已封存EXACT_SCOPE §2转录，不表示其代码授权已生效。后续Ownergrant写明activation时间/批准事项/基线与Writing QA输出，SourceSeal捕捉真正改动后27paths；prehash漂移必须重新定位归属再改。未知字段仍extra=forbid；domain schema只用其真实能表达的string字段，不把structured typedrefs/account数组压字符串绕验证。

未来代码目录仅覆盖上述精确文件的parent：backend/app、backend/app/api、backend/app/runtime、backend/app/bundled_workspace_packages/content_growth及schemas、backend/tests、frontend/components/content-growth、frontend/components/workspace、frontend/components/v1、frontend/app/ceo-office/organization/employees/[id]、frontend/lib、frontend/tests、desktop/scripts。目录非整目录grant。不得写PACKAGE_DDL/uniqueness/disable/uninstall、Writing领域服务/bundle、全局Shell/SharedComposer/默认CEODesk其它函数、数据库schema或第二ledger。

## 4. Workspaces and execution authorization — pending

- 工作区 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/` 当前**未授权创建**、实际不存在。未来可承载source/output seal、owned diff、decisions、真实evidence，须Owner准确grant。
- 外部root `/private/tmp/curis-cg-entry-20261005-01/`、端口21411/21412 当前**未授权创建或运行**、root实际不存在。source/data/logs/build/native/evidence子目录亦未创建。
- Fresh tests之前CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB均指同外部freshSQLite，import前设置；不能自动初始化默认DB。liveCloud/credentials/费用/Keychain/defaultApp/native需单独grant，不因代码grant自动允许。
- protectedDB：`/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`、`/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite`、`/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite`。本轮未连接、不写、不声明本轮integrity已测。未来分层验证前/后/静默hash与只读integrity；任何变化STOP，不恢复覆盖。

## 5. Runtime acceptance contract

复用CONTENT_ITEM/CONTENT_VERSION/runtime_links/evolution_events、已有Conversation/Task/Assignment/CompanyEmployee/global model/ai_usage_records。platform/channel/account/format与canonical经营scope正交，不新增第五scope或第二Artifact库。具体Account holder/binding还须合法source与资格证据；refs=[] 是真实未连接，不是假Account。保存/人工编辑不需模型或账号；真正员工建议须单独授权实际model调用并有唯一Usage。

每个create/save/adopt用scope-bound request_id/payload hash；sameID不同snapshot拒绝；同事务Version/link/CAS head/receipt。候选保存不改变草稿，人工采用另加Version并保存basis/version/refs用途/选段来源/actor/实际execution provenance；Viewed≠Adopted≠Review Approved≠Scheduled≠Published。原Selection未保存basis不随保存自动改版，过期返回只读原依据，不对新正文自动定位。主题/受众/账号/refs改变也必须候选stale。

Shared请求同原attempt/Task与purpose snapshot；currentAssignment revision、explicit CompanyEmployee bridge、eligible model/binding、permission/budget/refs资格多次验证。strict query不open/prepare/execute/orchestrator，不换Provider、不新request绕锁。claim/Task/bound/outbound/Usage跨事务间隙需物理crash证明；不可许诺exactly-once外部效果。UNKNOWN保原依据待核验，取消等待不是取消远端。CG成功候选回Main需实际回调与Usage事实，不能凭测试将控制回复当真实模型建议。

## 6. Definition candidate and publication gate

候选 `com.curis.local.content-growth` 0.1.0 可在未来代码grant内设计实现现有bundledPackage/release载体。来源、维护/支持Owner、Core/App兼容、retention/migration、真实推荐范围与限度必须可验证。不得自签published批准、把Writing release授权扩给CG、fakeXHS或用Generic强接专业入口。

内部候选测试可明确no-publication，按Owner单独隔离测试grant验证规则；不能替代已发布精确定义→普通入口最终证明。推荐范围/来源维护/compat/retention真实测试完，Delivery Owner再作准确限定发行决定。真实员工建议/云调用另grant。第一graphic不代表外部发布analytics就绪；完整四格式及逐账号发布/效果未知回执/复盘/学习保留下一节点，仅更新既有backlog，不另造产品架构或backlog。

## 7. Minimum evidence and done standard (all execution NOT RUN)

|检查|必须证据|
|---|---|
|正式入口/范围|真实公司/合法Department/批准定义/原proposal确认→原子Business/First PACKAGE Workspace，重复响应丢失查询原ID；跨tenant/company/business/workspace/parent/blueprint拒绝；未发布无正式启用|
|事务/CAS/采用|多connection/多process同head一胜，zero partial Version/link/receipt；sameID回原/differentpayload拒绝；插入/link/head/receipt逐步故障rollback；candidate不占head，人工采用检查不绕stale/资格；重复不追加；旧snapshot保持|
|引用/Selection|purpose版本/locator/摘录资格；同ref不同用途、完全重复去重；来源/正文/受众/账号/权限变化stale；UTF-16范围，原未保存标签/只读旧依据；不latest、不静默截断|
|Shared执行/未知|真实Assignment/Employee/model/binding/revision/预算快照→既有Task/回调/唯一Usage；purpose分派兼容Writing；before/afterclaim/Task/bound/outbound/Usage/candidate/response物理终止；query零outbound、UNKNOWN不replay、不newrequest逃逸；late结果回原request|
|frontend/source/build|新readiness state test及scopedlint/freshproduction build对应sourcehash；实际Browser普通入口/保存/建议/候选Main/人工采用/真实modelEmployee返回/输入selection讨论原锁保持/多对象隔离；1280×720正文、隐藏讨论、按需Utility、普通文案、键盘focus|
|兼容回归|旧XHS/TTK及Package无binding/v2、canonical parent/scope、Shared Conversation/Identity/Usage、Writing selected execution/readiness/两个return消费者；不重做已Accepted产品设计，检查共享delta未破坏它们|
|live/native|另grant准确Provider/model/credential来源/成本次数界；实际员工回复/Usage。fresh打包CG资源hash、真正App/外部state正常退出同rootrestart无重复对象、版本/采用/UNKNOWN连续；默认App不触碰|
|independent QA/Owner|同source/build/seal，failed/NOTRUN全保留，三protectedDB指纹不变/只读integrity；独立QA/Owner给精确verdict，不把controlled/static/API200当完整CG/AppRelease|

未来fresh测试root/build/Browser/live/native未grant，所以此次全部NOT RUN。完成“本Issue准备”只意味着两文档可复核、hash/27prehash一致、决定和Gate清楚，不意味着本vertical功能完成。

## 8. Failure, rollback and next gates

Scope/Blueprint/parent/tenant不合法、Unknown外部效果、费用凭据或protectedDB风险、Frozen冲突、第二Truth、需要大DDL/newprimitive→STOP，回Delivery Owner/相应Authority Owner给准确恢复入口。普通授权内技术/接线/兼容/测试问题由Delivery Owner批准，不另等待CEO小批准。

回滚：不得reset/checkout/clean/stash或覆盖用户已有delta；保preimage/owned diff与exactgrant。隔离验证失败不promote；已发生外部效果/Usage不可回滚删除；definition下架/disabled保历史与原请求只读/核验，不假成功。无预期大Schema，任何DDL实际需要先新精确Gate。

Next Action: Owner确认Writing schema-01独立QA封存输出→同轮批准27准确代码grant及其活跃baseline；随后实施，测试/外部root/ports/live/native按准确后续授权。Target Authority: 本正式Issue的append-only授权记录＋对应既有implementationReview/Backlog；本轮不自写canonical Pointer/CurrentState/ChangeLog，因为直接grant仅两新文档，不推广Current Product/Frozen。原readiness四文件和Writing33 seal不改。

## 9. Task Output Manifest

|绝对路径|Authority Class / Status|Disposition / 作用|
|---|---|---|
|`/Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-CG-PRODUCT-ENTRY-001.md`|CURRENT / IMPLEMENTATION SCOPE / OWNER DECISION PROVENANCE · Review|REVIEW_REQUIRED；Owner授权创建的唯一正式Issue，codegrant pending；非功能接受|
|`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-READINESS-20261005/OWNER_IMPLEMENTATION_DECISION.md`|REVIEW / OWNER DECISION EVIDENCE · Review|REVIEW_REQUIRED；CEO委派Owner批准来源和边界，新增记录，不修改原四文件seal|

Issue记录与Decision交叉link只指同一批准链，不产生第二Product或并行backlog。后续对Issue/Decision追加授权/证据须Owner精确grant；源与scope不被未经批准的附注扩大。



## 2026-10-05 — Owner continuous implementation grant (ACTIVE, replaces preparation-only gate)

Status: Review · Authority Class: IMPLEMENTATION SCOPE / OWNER DECISION PROVENANCE · Disposition: REVIEW_REQUIRED.
Source: Curis V1 Delivery Owner chat 019ff1ba-f696-7002-8a6c-2b357ded819c; CEO delegated ordinary bounded decisions.
Verdict: CODE IMPLEMENTATION AUTHORIZED WITHIN EXACT27 / NOT IMPLEMENTED OR ACCEPTED BY THIS GRANT.

Owner accepted Writing schema-01 BOUNDED_LOCAL_SCHEMA_LIFECYCLE_BROWSER_RETURN_PASS, preserving old FAIL/seals/physical copies and remaining cross-FS PARTIAL, realProvider/fees/native NOT RUN. Six writing documentation closures were authorized and completed before this CG source baseline. Their exact pre/post hashes, QA REPORT/source-seal/output-manifest hashes and 27 fresh prehashes are in artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/SOURCE_SEAL.json. The obsolete historical Writing schema blocker does not block this active CG grant.

Exact code authorization now activates only the27 paths/owned functions in Issue §3, identical to readiness EXACT_SCOPE §2. Allowed artifact area: artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/ only SOURCE_SEAL.json, OUTPUT_MANIFEST.json, HANDOFF.md, OWNED_CHANGES.diff, DECISION_GATES.md and evidence/. Authorized externalroot /private/tmp/curis-cg-entry-20261005-01/ only source/data/logs/build/evidence; ports21411/21412 after free check; CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB same fresh externalSQLite before imports. Focused/regression/lint/compile/freshproductionbuild/actualBrowser are authorized. Native, realProvider/fees/credential/Keychain/defaultApp are not authorized; no desktop.checkout build outputs.

Authorized CG documentation: docs/reviews/CURIS_V1_CG_PRODUCT_ENTRY_REVIEW.md; owned CG append only to PRODUCT_DOCUMENT_POINTER/CURRENT_STATE/CHANGE_LOG/DOCUMENT_INVENTORY and the existing Execution/FinalUIAcceptance/RuntimeCapability backlogs. No Product/Frozen rewrite, no Accepted promotion. Original readiness fourfiles and R03 seal stay byte-identical.

Owner approved minimal canonicalEntityBindings, strict unknown mappings/legacy preservation/generic mappedcreate refusal; sameconnection atomicCAS Version/link/head/receipt and candidate-not-head/manualadopt without Review/P7/SCHEDULED; Shared purpose dispatch retains Writing event/key, unknown purpose rejects; original query readonly0outbound; UNKNOWN noreplay/nochangingemployee-model to escape. refs=[] means genuine unconnected; real account binding needs evidence. Candidate release evidence may be no-publication but no self-signed published scope. Internal tests do not accept formal ordinary activation. Full CG remaining formats/peraccountpublication/receipt/review goals remain.

Continuous execution: audit/prehash→boundedimplementation→tests/build→Browser→sealreturn. Ordinary fixes inside grant continue. Required out-of-table delta: send Owner exact path/function/reason, no repeated ordinary CEO approval. Newprimitive/largeDDL/Frozenconflict/secondtruth/protectedDBchange/realfees remain preciseStop. NoGit/no cleanup; old Writing physical sealedsource stays intact and CG gets a newseal plus Writing regressions.


## 2026-10-05 Owner exact implementation amendment: 27 → 28
Status: Review. Authority Class: IMPLEMENTATION SCOPE / OWNER DECISION. Disposition: REVIEW_REQUIRED.
Owner direct grant from Curis V1 Delivery Owner 019ff1ba-f696-7002-8a6c-2b357ded819c: add only backend/app/orchestrator.py::_writing_reply_selection common finite-purpose execution binding validation and run existing single model_gateway_tool purpose wording. No whole-file/workflow/context/skills redesign. Prehash: 7462c7bff314e963ec1873ddf2a86289431346b627d31f558e3fdc44074dc746. Existing 27 baseline retained. Detailed scope/model/content/version/reference eligibility stays in the registered server-owned validator; helper validates persisted common Task/attempt/company/employee/workspace/model/binding facts. Unknown purpose and RESUMED unknown effects fail before launch. Evidence: original controlled HTTP failures preserved, corrected CG Task/Usage and Writing selected execution regression, concurrent claim and independent scope checks. Definition remains unpublished, no native/realProvider/fees/Git.

## Owner approved cache revision 01 — 2026-10-05

Task unchanged; objective: preserve same-window unsent discussion and explicit employee/model preferences, hydrate before writes, revalidate current eligibility, and clear only the scoped new form after confirmed canonical creation. Owner: Curis V1 交付负责人. Required input: independent QA employee-return cache FAIL and new-form stale cache FAIL; existing frozen scope and old sealed handoff. Exact Allowed Files: frontend/components/content-growth/ContentGrowthMain.js, frontend/lib/contentGrowthState.mjs, frontend/tests/contentGrowthEntryReadiness.test.mjs; this Issue and docs/reviews/CURIS_V1_CG_PRODUCT_ENTRY_REVIEW.md append only. Allowed artifact directory: artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/revision-cache-01/. Baseline three hashes/preimages retained there. No Shared CORS/auth/Employee load/API base/Schema/Provider/native/Git/Authority changes. Existing sealed 68 outputs and copied build remain untouched.

Outputs: owned three-file diff, focused input lifecycle/eligibility/isolation/create outcome tests, source and output seals, REVIEW_REQUIRED handoff. Real pending/UNKNOWN and server grant outrank cache; no permission, Task, Usage, execution replay or current version restored from cache. Failed/unsent/response-loss create retains input; canonical success with matching company/workspace and actual new identity clears only exact :new input key. Acceptance: Owner independent Browser return/reload/new-create recheck on fresh exact three-file revision; previous Employee Failed to fetch root cause remains UNKNOWN, not part of this source fix.
