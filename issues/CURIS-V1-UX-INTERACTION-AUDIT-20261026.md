# Curis V1 全 App 视觉与用户操作审核及修复

Status: Review
Authority Class: EVIDENCE / EXECUTION ISSUE
Owner: Delivery Owner
Task ID: CURIS-V1-UX-INTERACTION-AUDIT-20261026

CEO明确授权：当前模型任务完成后使用指定ux-interaction-audit，操作电脑审核整个App视觉与用户操作、给修改意见并执行。模型有界接受c66fc57/独立95f2e51已满足前置，不改写为全产品模型接受。

唯一执行看板继续沿用 L1/L2 原入口，不建并行Backlog或Authority。三角色不新增；当前第一范围为真实截图与操作审核、最小capture路径适配和已观察P2准备，业务源码此刻只读。精确Allowed Files/Directories、PID/kernel/Root、保护对象、后续Gate与完整输入/输出定义见同Task TASK_START.json。

## 初始明确文件范围

- /Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-UX-INTERACTION-AUDIT-20261026.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/TASK_START.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/AUDIT_REPORT.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/FINDINGS.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/CHECK_RESULTS.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OUTPUT_MANIFEST.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/native-events.jsonl
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md
- /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_FINAL_UI_ACCEPTANCE_BACKLOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md

## 目录范围

- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/qa-01
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/screenshots
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/tmp
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/tool-cache

## 验收

先按Skill硬顺序记录页面目标和实际动线，再Top5/九层评分/修改规则/文案。每个修复必须对应真实证据和既有产品目标，独立QA及Owner实际App定向复验；业务代码写入必须先在本Issue补精确Allowed Files及hunk批准，不改Frozen产品模型。源/包/QA/Native分别声明。普通问题在现有团队直接修复收口，只有真实CEO Gate请求人工。

## Owner 批准的同一源码修复批次：CURIS-UX-RC1

Status: Review；Authority Class: EVIDENCE / DELEGATED OWNER EXECUTION DECISION。

当前模型前置已接受；首轮同版本实机与 Skill 顺序报告已完成，来源为本 Task AUDIT_REPORT.md、FINDINGS、native-events 及独立 QA。当前旧 App 已正常退出，Native/parent/control/focus 均0，旧PGID及三监听端口清。以下为正式精确源码写入授权，取代“当前源码一律只读”的阶段限制；没有改动 Frozen Product Authority。

主开发在下列文件与已定义 hunk 内连续开发，普通失败自行修复，与独立QA直接反馈复验。Owner不再逐按钮/文案审批。既有两组私有候选有不同前像，必须按 SOURCE_MANIFEST 正确组合、检查当前 preimage，不能覆盖无关改动。代码/测试/包/实机分别回证，不用离线通过冒充交付。

### Allowed Source Files

- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/GeneralWorkspaceOperating.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/BusinessCatalogSurface.js
- /Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/business/page.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/CeoDeskOperating.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingWorkspace.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/writing/WritingPublishingMain.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/terra/TerraPrimitives.js
- /Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/talent-market/page.js
- /Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/meeting/page.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthMain.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthWorkspace.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthVerify.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/content-growth/ContentGrowthAccounts.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js
- /Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/settings/page.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ResultReferenceView.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/workspace/SharedEmployeeWorkArea.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/delivery/d1/ResultView.js

### Allowed Test Files

- /Users/yy/Documents/Curis AI Workspace/frontend/tests/d1WorkStatus.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/contentGrowthWorkbench.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/modelCredentialRecovery.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/settingsFormalIntegration.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/uxBusinessCreation.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/uxWritingDisplay.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/uxSearchLabels.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/resultDisplayTitle.test.mjs
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/uxComponentHarness.mjs

### Hunk / Scope

- GeneralWorkspaceOperating：明确请求当前结果页签，并为General成果提供同范围公开Work线索；不改Work执行/责任生命周期或自动采用。
- BusinessCatalogSurface、business/page、CeoDeskOperating：独立source_definition合法已发行包承接；旧完成结果与新CG/Music冲突同位旧结果/显式新草稿，保留new=1+来源；本地提案表单，完成锁和实际忙态分离。保留UNKNOWN、幂等、旧确认、迟到响应、公司/版本/digest/团队合同全部守卫。
- WritingWorkspace：仅新书标题局部验证、编辑/取消清局部错误及就近可访问提示；远端UNKNOWN和原创建锁保持。WritingPublishingMain：三处确定UTC时间显示，存储/ref/排序不变。
- TerraPrimitives、talent-market/page、meeting/page：搜索目的名称，不顺带全局重构导航/checkbox或触发真实会议。
- 四份ContentGrowth：已保存正文核验入口携有界cg_object提示，严格同company/workspace当前contents唯一匹配并显式选用；无效/重复/歧义不猜首项。成功读取0账号时给既有本地账号登记入口、来源和同对象回程；可在这些同文件内承接安全提示到accounts并提供既有路由返回，保持草稿/版本/明确选择，不声称未实测的回程已通过。账号措辞明确本地登记；无自动核验、勾选、保存、发送或假回执。
- ModelManagement、settings/page：中性管理标题/准确未验证状态；资格过滤后显式人工选择优先，再精确匹配已存default capability id，失效/歧义留空。首次connect的程序性首项必须与人工选择分开；保留真实FAILED/STALE/UNKNOWN/锁、留空复用、秘密清除/作用域与显式设默认。外部Agent集成措辞与模型提供方分开。不得自动连接/重测/写偏好或重做SOURCE01。
- ResultReferenceView、SharedEmployeeWorkArea、D1 ResultView：仅展示层安全标题/详情副本，按company/workspace/tenant/kind/ref/task-ref及唯一公开Work来源严格匹配，缺失/歧义各类型中性名称；General页头、展开JSON详情、D1页头/关联材料/来源展示均闭合原内部标题出口。保留原result、正文、status、verification、版本、receipt/Decision/human gate，不读或回写原Prompt/Task数据。62受限图不打开/复制/对外嵌入，不为定位重新读取Task API/DB。
- 对应真实组件/纯函数与作用域反例测试，测试夹具仅隔离内存；正式代码批准不授权Provider/DB/默认资料写入或付费调用。

### 输出与版本 Gate

沿用本 Task developer-01、qa-01 与唯一看板。允许 fixed-package-01、其build/evidence 精确目录保存不可变候选及匹配清单；无需预先建目录。独立源码QA通过后可以按既有已接受配方构建；安装到/Applications/Curis.app与隔离Root启动仍由Owner在包QA/身份/保护核验通过后执行。任何构建配方需要源文件范围之外更改先向Owner说明精确路径，由Owner处理普通scope，不新增Agent/平行计划。

Target：CURIS-UX-RC1，同一包定向实机修复回证、媒体真实导入/试听和冷启动保留所有已接受模型/作品对象；不能以各历史版本局部通过相加。未知费用不作0，Provider/外部发布/音频生成等边界保持。

### 同批普通测试适配补充（无新业务范围）

Owner批准精确追加 `/Users/yy/Documents/Curis AI Workspace/frontend/tests/writingEntryReadiness.test.mjs`：旧BusinessCatalogSurface fixture补实际Creator消费的BUSINESS_DIRECTIONS，改由真实本地form事件驱动；保留当前员工/原Run/来源失效守卫及原断言。业务源码仍18份，测试写入总10份。businessCatalogSurface.test.mjs撤回写入请求，不在本追加范围；精确公开发行JSON读取例外产生的EPERM不能作产品失败。原失败日志保留，复跑只声明实际结果。

### Owner 实机复验同批补充（RC1保持冻结）

Owner实际截图71及正常result-detail形状证据确认：D1把完整 general-business-result JSON封装直接作为阅读正文；没有证据证明源正文截断。允许Main在developer-01先做私有候选：仅完整已知封装的阅读展示副本，保留原始结果/版本/身份/验证/receipt；General长标题下完成badge仅局部防换行。经QA后再由Owner批准下一源码封存，当前包不热改。

额外精确Allowed Source File：`frontend/components/content-growth/ContentGrowthOperating.js`（前像SHA f21bccd4f271e81ec4af016784d3192b4761555a4411356707b297dca13ade73）。只允许唯一文案“当前平台还没有经营账号，注册账号后可在本业务内持续维护。”改为“当前平台还没有本地账号。登记后可在本业务内维护账号资料，尚未连接外部平台。”，不得改条件、路由、结构。其余已批路径/保护条件不变，不是新计划或Authority。前一TASK_START e2735f11完整保留在同Task evidence/TASK_START_BEFORE_RC2_SCOPE.json。

Owner已接受六文件合并私有候选QA5c9768ab及精确patch1ace8df3。RC1正常退出receipt767b4fa后批准六路径canonical集成，封存下一Source29路径，旧包/manifest/QA保留；Source集成QA后仅现有fixed-package-01/attempt-02及build/evidence构建新匹配包，Owner安装/Native/媒体/cold仍为后续Gate，不建立新计划。

RC2实际截图83确认D1结果已可读，但人类选择radio文字被全宽input规则挤成竖排。Owner精确新增Allowed Source File `frontend/components/delivery/d1/D1.module.css`，只允许.responseForm radio/checkbox尺寸、flex、对齐与必要标签局部换行规则，不改全局表单/布局/状态/receipt。先同Task私有候选与定向QA，RC2运行包/canonical当前冻结，后续合入/签名仍经Owner固定版本Gate。

Owner接受局部CSS静态QA ae58a90d，批准精确patch7405db16于RC2正常退出f6297564后集成唯一D1.module.css；30路径中其余29逐字节资格复用。唯一posthash由QA确认后允许现有fixed-package-01/attempt-03及build/evidence匹配构建，不覆盖前包。普通CSS无需重跑未受影响JS矩阵，真实几何/媒体/最终同包cold由Owner完成。

### RC3 原进程 transport 丢失后的有限正常退出观察合同

2026-10-27续行：Native76464/kernel1792973422.413563/c2f600仍存活，旧parent31978/control98142/focus87131 tool handles已失效，旧OS退出信息UNOBSERVABLE，原READY收据保留。Owner精确批准仅本身份的NORMAL_TERMINATE_REQUEST_ACCEPTED_AND_TARGET_GONE分支：新重绑control87245正常terminate实际返回true、记录新helper退出、随后独立核原PID/已知子PID/PGID/端口及helper精确路径无残留，cold前重查。原strict模式保留；不补EXITED/0，不改包/profile/Root/保护Works/费用/one-use。静态独立QA96ce1df2通过；真实退出、helper EOF、receipt、cold release尚不存在，不可提前执行。当前系统图文选择框FOREIGN_AX_ELEMENT（服务28492）等待一次集中三文件人工操作协助，不扩建工具或越过原生归属门。

## 2026-10-27 — Owner 本轮最终有界接受

Status: Review；Authority Class: EVIDENCE / DELEGATED OWNER ACCEPTANCE；Disposition: PROMOTE。

全App审核/获批20源码+10测试修复/独立QA/匹配RC3实机及同包冷启已完成；17项观察保留原始记录，15项修复、2项原语义保留。最终 `artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_FINAL_UX_ACCEPTANCE.json` SHA dd99e326b203896780dcf246c99a037b76cf518b0574b2d43e14cf5e7bd33c04，详细原始/最终证据和排除边界见同Task报告及QA最终23项清单。Source/QA/包/Native分列；旧OS退出码仍UNOBSERVABLE，不补0。C01/专业员工正向/外部能力与历史RC9边界不扩大，不声称新DMG或全产品接受。沿既有Current State、Pointer、两Backlog和唯一执行看板同步；本Issue内无未关闭普通修复或CEO Gate。

## 2026-10-27 — CEO拒收整体体验：重开业务进入与员工交流两条完整旅程

Status: Review；Authority Class: REVIEW / PRODUCT TO IMPLEMENTATION GAP；Disposition: REVIEW_REQUIRED。

来源为CEO当前截图与明确不满意反馈，Owner已承认先前技术性验收未充分证明普通用户的可发现性和完整交流。细项见同Task `CEO_FEEDBACK_CORE_JOURNEY_GAPS_20261027.md` 与用户图116；原15项修复/2语义原始证据不删除，旧dd99e326收据不改字节，但不得据其宣称整体UX或日常可用已接受。当前Task ID/目录/三角色/唯一看板沿用，Main和QA先在既有各自目录只读核对Current Blueprint/Master/UI/Shell3.1A与上述两路径，给准确源文件/前后端接线候选与独立验收标准；此阶段未扩大20份业务源码hunk授权，不改RC3、DB、凭据或调Provider。Owner收到具体范围后再在本Issue补精确Allowed Files/hunk，普通合同内问题自行协调。

## 2026-10-27 — Owner批准双旅程合同内修复（同批，UX-RC4目标，非接受）

Status: Review；Authority Class: EXECUTION AUTHORIZATION WITHIN EXISTING FROZEN DESIGN；Disposition: PROMOTE（仅精确实施范围）；Owner: Delivery Owner。

输入：Main `developer-01/UX_ENTRY_AND_EMPLOYEE_JOURNEYS_READONLY_01.md` §3.3/4.4/4.6，独立QA `qa-01/UX_CEO_REJECTED_TWO_JOURNEYS_READONLY_QA_01.md`，Owner实机117与CEO116。无新产品Decision/新Authority，不以本范围批准费用、默认资料写入或App重启。Main报告是hunk说明输入而非可自行扩大的文件集。

Task ID沿用；Developer一次完成两条旅程，普通同范围问题自行修复，与独立QA直接对账。Allowed Files（workspace相对路径，绝对前缀`/Users/yy/Documents/Curis AI Workspace/`）如下：

- `frontend/components/v1/BusinessCatalogSurface.js`
- `frontend/components/v1/BusinessCatalogSurface.module.css`
- `frontend/components/v1/CeoDeskOperating.js`
- `frontend/app/ceo-office/workspace/page.js`
- `backend/app/runtime/business_spine.py`
- `frontend/components/v1/SharedConversation.js`
- `frontend/components/v1/EmployeeConversation.js`
- `frontend/components/writing/WritingChapterMain.js`
- `frontend/components/content-growth/ContentGrowthMain.js`
- `frontend/components/music/MusicMain.js`
- `frontend/components/writing/WritingWorkspace.js`
- `frontend/components/content-growth/ContentGrowthWorkspace.js`
- `frontend/components/music/MusicWorkspace.js`
- `backend/app/model_preferences.py`
- `backend/app/conversation_service.py`
- `backend/app/api/conversation_router.py`
- `backend/app/writing_entry_service.py`
- `backend/app/content_growth_entry_service.py`
- `backend/app/music_entry_service.py`
- `backend/app/content_growth_service.py`
- `backend/app/music_service.py`
- `backend/app/writing_chapter_service.py`
- `backend/app/main.py`
- `backend/tests/test_canonical_business_spine_runtime.py`
- `frontend/tests/businessCatalogSurface.test.mjs`
- `frontend/tests/uxBusinessCreation.test.mjs`
- `frontend/tests/workspaceEntryJourney.test.mjs`
- `frontend/tests/employeeConversation.test.mjs`
- `frontend/tests/conversationProductization.test.mjs`
- `frontend/tests/writingChapter.test.mjs`
- `frontend/tests/writingEntryReadiness.test.mjs`
- `frontend/tests/contentGrowthWorkbench.test.mjs`
- `frontend/tests/contentGrowthEntryReadiness.test.mjs`
- `frontend/tests/musicWorkbench.test.mjs`
- `frontend/tests/musicEntryReadiness.test.mjs`
- `backend/tests/test_tenant_model_preference.py`
- `backend/tests/test_employee_conversation.py`
- `backend/tests/test_conversation_productization.py`
- `backend/tests/test_writing_entry_readiness.py`
- `backend/tests/test_writing_chapter_vertical.py`
- `backend/tests/test_music_selected_execution.py`
- `backend/tests/test_music_canonical_entry.py`
- `backend/tests/test_professional_conversation_journeys.py`

精确hunk边界：A仅业务目录主次/合法Workspace直达/准确First Workspace落点/GET投影business_type与对应测试；保留Business管理、原子创建、历史回执、UNKNOWN原请求、多实例显式选择与隔离。B仅现有EmployeeConversation内嵌复用Shared Composer、三域Workspace/Object真实责任与双向消息/可选引用/原选择修改adapter/准确返回/草稿与历史保持；禁止新造平行Conversation组件或API系统。C仅复用现有模型resolver、身份桥接与canonical会话生产接线；原专业修改purpose、版本/选择/候选/幂等/安全/UNKNOWN门保留。不得仅删disabled/Selection/policy来冒充可用。

执行与费用：此批准允许实现和隔离自动化自测，不允许新Provider真实请求。生产执行必须消费已有可验证的租户/公司/责任/模型/系统/成本授权真源；没有真源仍fail closed并回报精确缺口，不发明永久allow、客户端grant、新权限模式、测试环境变量冒充正式授权或绕direct purpose。内部binding只能由既有合法资格推导，用户不需逐业务重复固定绑定；不自动扩权。新真实请求待候选与QA后再走费用/外发Gate。

Allowed Directories：上述精确文件的现存父目录（仅授权这些文件/hunk）；既有Task developer-01用于私有前像/patch/source manifest/自测回证；qa-01用于独立回证；evidence/tmp用于全新且不复用的fixture DB与测试缓存。Main先保全准确前像/hash；测试前把CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB一致指到该目录全新fixture路径，禁止import回落默认库、读取/复制现存App DB。隔离测试创建/更新只限测试自建fixture；不得清理他人文件。

固定RC3 App/包/Root继续保持，当前运行实例禁止新业务写入/请求；Source通过后由Owner另定匹配包/安装/启动/实际对象场景精确Gate。无Schema/DB迁移、Provider新能力、密钥读取、外部服务发布、音频生成、Git操作、新Agent或全产品Audit。需要额外文件时先回准确hunk，不默扩。

验收：三专业方向0/1/N入口与合法目标/回程；普通意图不强迫选段；真责任与合法全局模型；双向消息/明确状态/准确Result与原Main；原选择修改保持版本与人工采用；收起/重开/跨对象/冷启不串不丢。开发有意义自测→独立QA固定版本→Owner同版真实App；不得以离线/组件通过当正向生成或完整交付。Next Task为同一UX-RC4双旅程候选资格/独立QA，再匹配包与真实App（非另起交付批次）。

### UX-RC4测试安全门兼容：Owner精确批准外部临时fixture（2026-10-27）

原23源码/20测试业务hunk保持。既有 `backend/tests/db_safety.py` 拒绝仓库内DB，原Task/evidence/tmp安排无法执行；本次不改安全门、不触任何现存DB。Owner已只读确认下列根目录尚不存在，批准仅本批从无到有创建 `/private/tmp/curis-ux-rc4-20261027-01/`。

Allowed Directories（仅全新自动化fixture/缓存/pytest输出）：Main独占 `/private/tmp/curis-ux-rc4-20261027-01/developer-01/`；独立QA独占 `/private/tmp/curis-ux-rc4-20261027-01/qa-01/`。各自三个CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB在任何backend import前一致指向各自全新 `bootstrap.sqlite`，测试各自创建的其他DB也仅在所属子目录；不得共享、读取或修改对方fixture。创建根/所属目录使用不存在才创建，不复用既存根或库；如发现抢先存在/身份不明先报Owner。

sandbox继续禁止网络/Keychain、任何默认或保护DB和范围外DB及写入。此处仅为可再生成的自动化测试临时fixture，不是App验收Root/保护业务资料/历史升级样本；结果与命令、文件身份保留Task各自developer-01/qa-01。未授权清理、删除、重新创建已有路径或复制现存业务DB。原Task/evidence/tmp继续可作非DB缓存；不授权App启动/安装/真实调用。Main/QA普通测试问题同批直接对账，不因该可解目录冲突请求CEO。

### 2026-10-28 — Owner批准既有Company预算/外发政策的最小正式接线（合并同UX-RC4候选）

Status: Review；Authority Class: EXECUTION AUTHORIZATION WITHIN FROZEN SHARED CONTRACT；Disposition: PROMOTE（仅精确实施范围）；Owner: Delivery Owner。

依据：已实际核当前Shared Authority §13、§15、§18、§19.3：Company已定义预算、数据外发/审批政策，模型资格不是费用授权；已批准产品范围内的Company设置实施，不新增产品权限模式/Runtime Primitive/Schema/Approval表。Main与独立QA确认当前Company预算和数据外发项仅Unsupported，三专业Entry默认grant None，现存事件日志可承载正式政策及幂等预算记录。Owner接受Main的最小技术路线；不再要求CEO选择内部grant架构。

准确追加Allowed Files（workspace相对路径，绝对前缀同上）：
- `frontend/app/ceo-office/settings/page.js`
- `frontend/lib/v1FrontendApi.js`
- `backend/app/api/frontend_v1_router.py`
- `backend/app/company_execution_policy.py`
- `frontend/tests/settingsFormalIntegration.test.mjs`
- `backend/tests/test_company_execution_policy.py`

允许hunk：Settings仅原Company“预算与审批”“数据外发与备份”中的文字执行许可、预算/有效期/撤销/准确返回，不改备份功能、不新建Settings页/分类；v1FrontendApi及frontend_v1_router仅该Company政策读取/显式保存/撤销接口。新company_execution_policy小服务仅在既有tenant隔离evolution_events消费版本化Company同意/撤销/预算占额/结算，沿唯一既有事件日志，不改schema/database/evolution_event_log，不另造会话/模型目录或权限体系。源码先保全新增文件缺席及原文件前像。原已准main.py/conversation_service.py/model_preferences.py/三Entry的hunk追加为正式policy读取/重核/单次占额与结果结算，不只接受fixture注入。

产品行为：用户在现有Company设置明确同意当前公司所选Workspace内负责员工的文字交流/选段修改，把本次输入和主动选定的引用发给界面列明的现有Provider/Model；未保存内容不得静默发送。模型全局可选不等同许可，新增Provider/目的地/范围/价格实质变化重新核准。用户不填内部grant字段、不逐员工重复模型绑定。显示有来源估算、累计预算与有效期；显式保存才授权，默认未授权；可撤销，不删除旧记录/Usage。

安全/预算：服务端按已有CEO/tenant/company/scope资格验保存与每次发送，校当前Assignment/对象版本/模型健康资格/目的地/政策版本/有效期/价格来源。预算为执行准入上限，事务内幂等占额后才发出，跨并发/重启不归零；无授权/未知或过期价格/额度不足拒绝并保输入。UNKNOWN保留占额只查询，无自动重放；撤销阻止未开始的新执行，不伪造已取消远端调用。已知用量仅按来源价格估算，不伪称实付；旧USD字段不塞CNY，单位明确并分别校验。原强Selection/候选/人工采用门保持。

价格事实的本轮公开依据：DeepSeek官方中/英文 pricing，中文 https://api-docs.deepseek.com/zh-cn/quick_start/pricing/，模型deepseek-flash，版本V4.1-Flash-1017，峰值输入未命中CNY2/百万、输出CNY8/百万；英文同模型USD0.3/百万输入、USD1.2/百万输出。只能作为有来源/检查日期/单位/freshness的元数据，不能外推其他模型或未知价格；不新增自动联网解析器/Provider调用或凭据读取。来源过期/不匹配fail closed，Owner/QA核事实后才可消费，不把用户声明升级Verified。

测试追加只涵盖Company身份/范围/显式同意/撤销/有效期/价格/预算并发/重复请求/UNKNOWN/冷重建读取与原专业效果；沿已批准外部各角色新fixture，禁现存DB/Key/网络。新增Allowed Directories仅上述精确文件现存父目录，输出沿developer-01/qa-01；无新Review目录。

这仍是同一候选：原23源/20测试+4源/2测试=最多27源/22测试（未改文件不为凑数修改），完成后一次封存Manifest与对应前像/patch；独立QA只对同一完整固定候选集中验证，禁止先把无授权外壳封存成完整交流交付。真实调用/当前App写入/安装启动仍未放行。

原CEO明确的5元总验证上限保留，旧Model Task两次/原收据不改。Owner已核原保守费用准入CNY4.227072，当前可评估原总额内至多CNY0.50的后续有界验证；这不是本节的真实调用release。必须先独立核完整输入计量/实际物理调用数/价格与单位/历史保留/幂等预算，Owner另发精确场景和执行许可；超原人类金额/数据外发范围、新OS权限或Product Authority冲突才报CEO。

### UX-RC4目录真实方向投影：Owner同文件精确hunk补充（2026-10-28）

原已批 `backend/app/runtime/business_spine.py:get_business` 的同一Workspace SELECT 除business_type外，准确追加从同一受tenant/company/business/RESOLVED约束的Workspace blueprint_json中投影 `$.packageId AS package_id`、`$.packageVersion AS package_version`。两键已是各Entry消费的既有事实；只读DTO投影，不变Schema/蓝图/Package binding/版本，不返回整个blueprint_json。缺失、非法JSON/字段类型或未知Package如实未识别，不猜名字、首项或latest，不让一个非法字段拖垮整个合法目录。

`BusinessCatalogSurface`在原已批hunk内复用既有BUSINESS_DIRECTIONS的真实package_id映射方向，首屏三方向清楚可发现，其已有实例/Workspace按实际名称与业务关系显式选择，开始新业务与能力介绍主次明确；保留全部自定义业务和Business管理，未知类别保留合法目录入口/诚实状态，不按UX前缀隐藏。package_version保持来源实际版本，不借分类暗中升级或把未验证版本当已发布可执行。对应已批business spine与目录测试补缺字段/同名/未知/跨scope负例；不新增文件或另批。

### 2026-10-28 — CEO再次确认本批持续收口与费用总上限

人类原文：“继续按这一批收口，按我确认过的 UI 把三业务入口、员工连续对话、结果回原工作和冷启动真正跑通。跟完开发、独立 QA 和你的实际 App 验收再给我看，费用总额仍不超过5元，普通问题自行修复，别再拿局部通过当完整交付。”

Disposition: PROMOTE（本批执行与费用目的授权）；Status: Review；Authority Class: CURRENT / HUMAN EXECUTION GRANT；Owner: Delivery Owner。沿同Task/唯一看板/三角色，27源/22测试与精确hunk保持；不得停在源码或QA准备，普通问题同批修复。新专业验证的费用目的明确获授权，但金额为前后累计总额CNY5，不是另加5；旧Model Task两次/封存收据不改。当前尚未固定Source、没有Owner实际调用release；具体Company/Workspace/员工/对象/次数/完整prompt/输出/价格/预算占额/恢复/冷启按固定候选独立QA后Owner发精确准入。新OS权限、保护资料异常、不可逆动作与真实Product Authority冲突仍有原CEO Gate；默认资料不改，凭据不读不回显。

### 2026-10-28 — Owner批准业务素材准备的并发原子发布修复（同UX-RC4）

只读已核 `UX_RC4_LIFECYCLE_FIXTURE_DIAGNOSTIC_01.txt` 与当前 `prepare_confirmed_assets`、调用者 `runtime/first_run_delivery.py:372` 和既有Writing/CG测试。原实现copytree直接写最终目标，FileExistsError竞争分支立即验证，确有读半成品窗口；不能预热夹具隐藏。

准确追加Allowed Source File：`/Users/yy/Documents/Curis AI Workspace/backend/app/workspace_package_runtime.py`，Owner读取指纹 `1ae882be6ee4dab2c85fa222a317379d0d8d8d8778d52519b4e59d8333c1eaba`（Main编辑前重新核并保前像，不混淆旧版本）。仅 `prepare_confirmed_assets` 与该函数必要stdlib import hunk：同文件既有staging实践优先复用；同目录本次唯一staging完整复制并验证digest后原子发布，目标不可覆盖/删除，竞争者只复用已完成且digest一致的不可变终目录。对既存损坏/不明目录保现场并明确失败，不自动修复或移除；不改store路径/权限/Schema/安装或业务身份语义，不改其他install函数。自建staging的收尾仅限本次函数独占创建且身份确认的目录，不能触碰其他producer/已有资产；不得引新依赖/锁框架或扩大普通资源访问。

在已准 `backend/tests/test_writing_entry_readiness.py` 加确定性并发回归（用可控屏障展示旧实现读半份、修复仅见完整资产），不依赖反复碰运气/预热。增加 `backend/tests/test_cg_reference_learning.py` 仅只读及隔离运行资格，不授权修改它；与本helper的CG调用者一起核受影响范围。所有测试DB仍专属外部fixture，禁网/Keychain/现存DB守卫不变。修复后定向回归及一次必要完整后端回归，前端SHA未变无需重跑整套前端；最终同一Source manifest注明基于相同前端hash复用结果。

候选上限更新为28源/22可写测试；Caller CG测试只读/可运行。仍为同一批同一候选，未授权打包/App/真实调用，普通测试失败直接Main/QA同批闭环。

### UX-RC4-SOURCE-01固定与并行包配方准备（2026-10-28）

Main已固定Seal SHA7d181030e534db9565a4efcf47ad77fde8abb3b3b7d753ace2f15d4784dd5a21、Source Manifest SHA47767265b58a897ef3efad7a335aa5a408e6113aead3cf75f786d91d95c4d63e（28源/22测试，43改动）、Owned Patch SHA3a51b4b6e3e197f44e9939c63722655f1deca0d8b90b473a96561dab17a90707。Owner已复核全部50文件当前SHA与固定manifest一致；开发backend150通过、frontend206通过/6条件skip为开发回证，独立QA正在测此一版本，尚无Source QA/包/Native接受。

开发在QA并行期间可准备精确包配方，禁止改冻结源：Allowed Write Files仅本Task既有developer-01下 `BUILD_UX_RC4_PACKAGE_01.py`、`UX_RC4_PACKAGE_SPEC_01.json`、`UX_RC4_PACKAGE_PREPARATION_CHECK_01.json`。可只读参考原已接受attempt-03 App/匹配manifest15edf770与其build输入，旧DeepSeek任务BUILD_TEAM_PROJECTION_PACKAGE_01.py/FRONTEND_ONLY_BUILD_05.py及对应spec（历史算法证据，不作新授权）；新SourceManifest/三份前像/新QA结果为真正输入。

目标为在原同Task `fixed-package-01/attempt-04` 制作匹配双端App的未来配方；现在不创建该目录、不执行构建、安装或启动。复用已核旧包/已安装本地runtime，前端旧输入闭包只替本轮批准源；后端基于既有carrier精确验证旧module code与前像后替换本轮模块，并正确加入新company_execution_policy模块、核导入依赖，不把旧c1 carrier误当已含新后端。其余成员保持，无新下载/依赖/私有凭据/DB读取，不把混合W整树作为未审基线。

执行前必须等待Source独立QA通过，再由Owner给绑定Source/QA/脚本/spec/旧包/输出目录的精确build release；准备代码缺release须拒绝执行。旧配方仅复用纯编译/归档/trace方法，不绕门；Source/QA改变后更新配方pins，保旧记录。冻结源不得为准备包修改。保持HOME/CODEX_HOME，不重定向系统家目录；只用Task已准临时/cache路径。Owner负责最终同包实际App/冷启和费用准入。

### 2026-10-28 — Source-01独立QA不通过；Owner批准预算防回滚最小修复

证据：`qa-01/UX_RC4_SOURCE_01_INDEPENDENT_QA_01.json` SHA fe175969e99dd7c13d8012d088672c1818ae807dc0b2fbff75d74d77ac4992c4；QA仅自建fixture恢复授权后/占额前快照，同一预算由49664 micro-CNY回到0且再次允许预留，Provider0，非保护资料变动。Source-01 Seal/报告不改字节，Gate为FAIL/OPEN，禁止构建该失败版。其余Source散列/独立150后端/206前端6条件skip仅为具体证据，不替完整Gate。

Owner已只读核当前Frozen Shared §17：恢复后Resume Check必须重验权限/外部效果；当前`desktop/runtime/recovery.py` EXCLUDED_ROOTS明确排除runtime（以及cache/tmp/logs/recovery），`_managed_files`拒绝未知root/data项，正常恢复以受管清单替换DB/文件。不改恢复模块/Schema/数据库框架，不能随便往data或Root增加未知JSON破坏备份。

批准在原已批 `backend/app/company_execution_policy.py` 做最小当前资料世代/防回滚校验。优先既有可证恢复代际；为覆盖同inode旧快照回滚，精确允许仅当前应用profile运行命名空间中的不随正常备份恢复的最小状态锚：`<当前合法Data Root>/runtime/company-execution-policy/<sha256(规范化DB路径+tenant_id+company_id)>.json`。该目录0700/文件0600、来源由服务器当前DB/profile推导或既有main依赖注入，不从客户端收路径；不得回落默认profile，不枚举/读他tenant或Company。测试锚只在各自已批外部fixture子目录内；当前App/保护Root仍不操作。

锚只存防回滚的opaque世代/一致性标识，不成为另一本预算账或授权真源；正式policy/占额/用量仍沿唯一evolution_events。政策保存、预留、撤销、结算的DB状态与当前外锚须有可证明的一致性；任何部分失败/缺失/不匹配先拒新物理执行，不根据回滚DB自动重建旧锚或默默补额度。所有grant返回/物理发送前需核当前完整状态可信及该精确预留仍有效，不能把其他合法并发事件导致的nonce推进误判为所有旧在途请求失效。正常冷启保policy/计数，不以每次启动清零/重授权代替。只读metadata不得自动授权/重置。首次无policy的明确保存才创建锚；旧policy存在却无锚应失效需明确重新确认。锚丢失/损坏/链接/权限不明保现场拒绝，禁止自动清理修复。

只授权本次独占新建的原子写临时文件收尾，不删除他人/既有状态；Path祖先/文件uid/类型/链接边界与原子fsync/失败姿态需明确。真实App后续release会把此新增状态路径列入预期变更；此刻只代码与全新fixture。不得读Keychain、复制真实DB、改备份流程或新Schema。若已有更小实现能覆盖同inode探针且正常冷启兼容，Main先短报替代来源，再Owner登记。

允许原已批Settings Company组/对应frontend测试、frontend_v1_router政策接口hunk在必要时就近显示“资料状态变化，旧费用授权失效，历史费用不可完整核实”，明确后续额度/同意；不显示已恢复全额，不把UNKNOWN历史写0。重新授权必须真实CEO明确核对新的后续预算/范围，不自动重发旧消息、不取消已发外部效果。必要的显式状态确认字段只沿已有政策DTO，不新审批类型/页面。

在原test_company_execution_policy.py补确定性同inode旧快照（QA探针）、正常新service冷读、缺失/不匹配/坏锚、持久失败/并发与原预算撤销边界；settings现有测试仅验受影响提示/明确确认。受影响项复验后同批Source-02新Seal；Source-01 QA及失效证据保留。28源/22测试文件集不扩大；仍无包构建/App/新真实调用release，普通修复直接Main/QA。

#### 防回滚最小方案定稿：采用Main连续性指纹与recovery排除域（取代前条runtime路径）

Owner接受Main已核的更小实现：仅对该公司changed（含保存/撤销）、reserved、settled事件序列形成连续性指纹，存最小控制锚，不新增收费账/授权来源。精确生产路径模板为 `<服务器CURIS_DESKTOP_DATA_ROOT>/recovery/company-text-policy/<SHA256(tenant_id,company_id)>.json`，且db.path必须严格匹配该Root/data/curis.sqlite；无Desktop Root的隔离headless/fixture为 `<当前DB-parent>/recovery/company-text-policy/<SHA256(规范化abs DB path)>/<SHA256(tenant_id,company_id)>.json`。只允许当前scope，不读他profile，不从客户端收路径、不回落真实默认库。此项替代上一条runtime模板，不授权同时写两处或迁移/删除旧不明状态。

依据当前recovery.py EXCLUDED_ROOTS与受管恢复：recovery/整体不入普通备份，restore_v2只替managed rows，现有recovery/last.json代际仅覆盖正常恢复，不能覆盖QA同inode SQLite覆盖；故不单绑inode/last.json。新增精确子目录不改任何恢复模块、journal/generations、Schema或原恢复行为；正常生命周期不得清理该连续性锚。

每次相关变更在已有BEGIN IMMEDIATE内先以包含本次待提交事件的预期指纹，在独占同目录新临时文件中持久写入/fsync/原子替换控制锚，再提交DB；DB回滚、外部旧快照、缺锚/坏锚/写失败不匹配即拒发，不能从旧DB自动续用。外锚仅scope摘要/版本/序列指纹，无Prompt/凭据/金额；指纹不是已付款证明。读取只校验不重建。并发scope安全按现行DB+外锚与具体持有预留验，不要求所有pending grant都等于最新事件序号。

只有在当前UI明确显示历史费用可能不完整、旧许可失效后，CEO以新的明确后续范围/金额请求确认才可重新建立连续性；旧save原request重放不能复活。必要已有政策DTO/Settings确认提示与原批准测试hunk可改，非新权限模式。需覆同inode/替换DB、正常冷启、丢/坏锚、持久失败/DB回滚、并发和原save重放。28源/22测试内，Source01失败收据不改；Source02重封后QA定向复验，仍不得构建/真实App或Provider调用。

### 2026-10-28 — Source02独立QA通过，Owner放行同版匹配包一次构建

Source02 ab559deb/Seal cd71157b/patch e78f05db经独立QA 767e72ca判 `PASS_BOUNDED_SOURCE_AND_ISOLATED_AUTOMATION_FOR_OWNER_PACKAGE_GATE`；后端163、受影响前端16及原206/6skip资格、同inode恢复探针与授权/锚负例均分别核验。Owner复核Source50当前hash及QA归属后仅接受Source资格，旧Source01 FAIL回证不改、非产品接受。

精确执行release：本Task `OWNER_UX_RC4_PACKAGE_RELEASE_01.json`（脚本e787/spec1704/donor15edf770/Sourceab559/QA767e绑定）。新增Allowed File该release；Allowed Directory仅全新 `fixed-package-01/attempt-04/` 及其构建/证据/临时子树。允许经已准脚本一次执行匹配双端App构建、仅阶段包ad-hoc签名，不访问凭据/DB、禁网、不安装/启动/真实调用，不写旧包/源/Default资料。输出与失败现场保留，失败不可原目录自动重试或清理。

Next Gate：Main构建回证→独立包QA（Source/PYZ新增模块/前端/签名/未变资源）→Owner精确安装/新进程身份/实际同版三业务连续对话与结果返回/冷启/总费用准入。未通过后两项不能完整交付。

### UX-RC4构建启动路径修正：attempt04保全，准备attempt05（2026-10-28）

attempt04已按release01执行一次，但仅worker启动因未白名单的venv中间符号链接被sandbox拒绝；未编译/无App产物，无现存App/DB/Keychain/网络/Provider动作。现场BUILD_START/bootstrap-tmp/worker.sb/worker.log保留，禁止原目录重试或清理；Source02及独立QA不变。

Owner批准在已准三份配方文件中做精确路径修正：Python pin及worker执行仅改为同一SHA2477b47f…的已核Homebrew解释器规范化真实路径，保留HOME/CODEX_HOME与全部数据/网络/写入限制，不扩大用户目录读取。旧script/spec/check精确字节沿现有priorPreparations保全。未来唯一输出改为全新 `fixed-package-01/attempt-05`，未来release改为本Task `OWNER_UX_RC4_PACKAGE_RELEASE_02.json`。本节只准配方准备/无执行校验，尚不创建05、不构建；待新hash与Owner核对后另写release02才可执行。

### attempt05精确构建执行放行（2026-10-28）

Owner复核新script ad3e46e3/spec04a457bb/check74f2e8aa、Source02ab559/独立QA767e72ca、当前50源文件不变、05目录不存在；修正仅同一已核解释器规范路径和原中文literal的UTF-8编码，无扩大读范围，原04现场/旧字节保留。release02现已写入，精确绑定仅全新 `fixed-package-01/attempt-05/` 及其子树一次匹配包构建；该Root递归为Allowed Directory，release02为Allowed File。保持禁网/DB/Keychain、阶段签名only、不安装启动或真实调用。失败现场保留，不原目录重试/清理。独立包QA后才Owner实际App。

### 普通构建修正：单层继承沙箱，准备attempt06（2026-10-28）

attempt05已通过全部输入/复制校验，但Next子进程试图在生效worker sandbox中再次sandbox_apply被系统拒绝exit71，未执行Next/签名/形成包。现场全保留，不重用/清理05，Source02/QA不变。

Owner准在既有三配方文件内做精确最小修正：Next build与阶段runtime-resolution probe直接启动同一固定Node，继承当前worker单层sandbox；移除其无效第二层sandbox-exec调用。worker禁网、仅全新OUT可写、限定既有已授权输入闭包可读、DB/.env/Keychain/security禁止均保持。Node可读取同一已授权worker输入（donor/批准源/依赖），不新增读根/写根；不降低到无sandbox运行，不改产品源/依赖。可在既有Task自有临时区域做无产品执行/无保护资料的只读Node继承探针，禁止借探针读真实保护数据或发实际Provider请求。

未来唯一OUT为本Task全新fixed-package-01/attempt-06，未来release为OWNER_UX_RC4_PACKAGE_RELEASE_03.json；此节仅准备，尚不创建06/不执行build，等修正版准确pins后Owner即重绑。旧recipe/spec/check字节继续priorPreparations保留，无需重跑未变业务Source QA，Main/QA普通问题同批处理。

### attempt06一次匹配包执行放行（2026-10-28）

Owner复核script18ca95b0/spec739237eb/check22f9f180、固定Source02ab559/QA767e与当前50源不变、06不存在后写release03。准备确认仅移除Next/probe嵌套sandbox并沿用原worker完整限制；只读继承启动/禁网检查有效，未新增读写根。允许仅全新fixed-package-01/attempt-06及其子树一次构建、阶段签名，不安装/启动/访问DB或Keychain/真实Provider。Owner release03为Allowed File、06子树为Allowed Directory。04/05与旧准备字节保留，失败不原目录重试清理；包QA后才真实App Gate。

### 新包既有原生工具固定摘要适配：只准备、不操作App（2026-10-28）

Main已产attempt06匹配包manifest31eb2166、BUILD_ID M6xm08QC9_CFhz3Cv5-dA、Native115d7ccd35888287bc7f8bccf9a098eca03c4ee09c338c848ca0d9408f1a0186、workspace carrier3aed91a6；独立包QA正在核验，尚未安装/启动/产品接受。

Owner已读旧control/focus Swift头部，准仅复制既有RC3安全工具并在新文件替换productSHA这一精确字面量：c2f6006e…→上述115d7ccd完整摘要。其余代码/目标路径/PID+kernel身份/拒foreign/密码与新权限边界/60s引用/截图目的地保持字节一致，不加新功能或新UI技术。Allowed Write Files仅本Task既有developer-01/下 `pid_native_control_ux_rc4.swift`、`pid_native_focus_ux_rc4.swift`、`pid_native_control_ux_rc4`、`pid_native_focus_ux_rc4`、`UX_RC4_NATIVE_PIN_PREPARATION_01.json`；编译cache只原Task evidence/tool-cache。旧工具/回证不动。

只允许本机已有Swift编译器编译及原纯self-check，不运行AX binding/snapshot/screenshot/动作，不启动Curis/fixture、不新建控制目标、不请求系统权限，不访问DB/Keychain。回报新旧Source SHA、精确字面量diff、binary SHA和selfcheck；独立工具核验与包QA后Owner另发实际安装/新进程绑定/Native门。此为既有受限工具识别新版本，不开发新自动化能力。

### 匹配包/工具静态QA通过，准备精确安装与既有Root启动（2026-10-28）

Owner接受独立包/工具QA 0befd4629f620dabd9cdaf7ff267220c569b1a35102e37701afc551ea2159672为安装资格（不是Native/产品接受），同版manifest31eb2166、Native115d7ccd、carrier3aed91a6、BUILD_ID M6xm08QC9_CFhz3Cv5-dA、Sourceab559/QA767e。历史PID52778的退出推论由QA增量badc1b0f撤回；Owner独核旧36376及36561/36567/36584当前缺席、三端口空闲，不能补称正常退出码。当前/Applications/Curis.app Native仍c2f600、目录UID501/非symlink；既有隔离Root dev16777229/inode88268446/uid501/mode0700保持。

仅准备，当前不执行安装/启动：Main可在既有developer-01写INSTALL_UX_RC4_APP_01.py、LAUNCH_UX_RC4_APP_01.py、UX_RC4_NATIVE_RUN_SPEC_01.json、UX_RC4_NATIVE_RUN_PREPARATION_01.json。复用旧已核安装/launcher的身份/最小环境解析/PGID/端口/父句柄方法，不新造工具框架或改产品源；除Inputs/输出/既有Root检查外不扩功能。

未来唯一安装目标 `/Applications/Curis.app`；源仅同版attempt06/Curis.app；当前旧App精确保全到本Task未来新建native-install-01/previous/Curis.app（所有原字节/额外运行缓存一起保留），staged复制/检查在该安装工作区；同设备安全rename，失败不丢旧包、不清不明文件。不得触用户其他App/源码/资料、不得清理/覆盖已存在目标备份，原包/04/05/06不变。安装前必须无活Curis相关目标/端口、核旧c2身份并拒symlink/不明归属。新源完整member hash/mode/签名须复核；不得重签改变已验新包。无执行release时拒绝写入。

未来启动只用当前既有隔离Root `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-root-01`（上述identity），不新建/重建/恢复/复制DB；正常App自身初始化/运行元数据为已有授权，本段不准实际启动。保持旧app-stage-01/app-profile.sb（SHA93345efc…）全部保护/网络限制及已验合法loopback proxy/官方TLS边界，不改系统网络设置或新增目的地，不改HOME/CODEX_HOME。新Native按PID+kernel start+UID+绝对路径+115d哈希绑定，三服务必须同PGID；仅读取六字段Root/三DB别名/macOS-keychain/packaged标记的环境投影，不输出其他env/凭据。保留原Popen父句柄、仅正常退出请求，绝不forcekill未知进程。

未来运行输出目录为本Task全新native-rc4-01（receipt/binding/最小状态日志，不读App私有stdout），安装输出为native-install-01；此次不创建这些目录。程序须要求Owner另发绑定包QA/Source/全部脚本/spec/hash/Rootidentity/输出/工具的精确release才执行。纯准备校验不AX/App/DB/Keychain/Provider；启动后生成仍另有费用/业务场景门。收到prepare后QA只增量核这些身份和输入适配，Owner亲自执行安装/启动/实际UI。

### Owner实际安装/同Root启动放行（0真实生成；2026-10-28）

recipe独立QA78e74fb3已接受，最终installer1fdd/launcherb78e/spec8a642/preparec1984。精确允许Owner新写本Task OWNER_UX_RC4_INSTALL_RELEASE_01.json、OWNER_UX_RC4_LAUNCH_RELEASE_01.json；并由已验脚本创建本Task native-install-01、native-rc4-01及其精确spec输出。准Owner执行一次安装：Source06原字节至/Applications/Curis.app，旧App整目录同设备no-replace保全至native-install-01/previous/Curis.app，默认数据不读写。成功安装receipt后同一既有Root启动一次，原sandbox93345/loopback边界不放宽，retain父句柄，验真实PID/kernel+Root/六字段/同PGID服务。准使用同版已核AX工具9d12/3705对新唯一绑定App做本地入口/界面/政策设置检查及普通自制文本操作；不读私prompt/reasoning/密钥，不自动答系统权限，不Provider真实发送。本次真实生成仍未放行，等现场Company政策/模型/对象及独立费用批门。旧退出未知保持。

### Owner实机返修：同批三业务入口普通视觉（Source03，2026-10-28）

实际App06/PID23477/同Root在正常业务首页取得截图118-ux-rc4-three-business-entry.png，长业务与工作空间名称在多实例卡片中越界产生横滚，主标题混英文、入口暴露安装包版本。不是Source/包资格撤销，不是产品Authority冲突；整体尚未Native接受。

同原Task仅解冻准确3文件：frontend/components/v1/BusinessCatalogSurface.js、frontend/components/v1/BusinessCatalogSurface.module.css、frontend/tests/businessCatalogSurface.test.mjs；Main自主修正常文案/局部排布与长名称/多实例约束，不改真实分类/身份路由、数据、权限、其他Source02或Frozen Authority。Owner已直接反馈Main，QA并行定向复验；必要测试只证明新边界，不重复无关163后端/全产品Audit。旧Source02/QA/06与失败证据保留，精确前像与补丁后固定Source03，最终新匹配包重跑受影响入口和完整真实旅程同版，不拼接06诊断当最终。06当前可继续不受影响本地UI诊断/政策准备，真实新Provider仍0、未放行；不新造Backlog/计划/Review目录。

Source03定向测试追加准确已准文件 `frontend/tests/workspaceEntryJourney.test.mjs`，仅同步入口版本文案移除/长名列表约束断言，不改变身份路由合同；共4个文件可动，其余冻结。

### Source03同批增量QA通过：匹配包07准备（2026-10-28）

Owner接受Source03 manifest5adee9b6/Sealcb35/QA57920970仅4文件delta及28定向通过、其他46不变，几何/Native未通过。Main仅准在既有developer-01新写BUILD_UX_RC4_PACKAGE_02.py、UX_RC4_PACKAGE_SPEC_02.json、UX_RC4_PACKAGE_PREPARATION_CHECK_02.json，最大复用已执行/已核18ca脚本的单层sandbox/解释器/Node固定方法，适配Source03/QA03/07输出，保留18ca及所有旧配方/包/回证。

优先沿既有合法donor/14模块delta规则，不扩大读取、写入、网络或源码范围；若改用06 donor，必须精确证明所有Backend/Native/依赖字节及CodeField不变且不宽旧前像门，先回差异供独立QA。未来唯一构建输出本Task fixed-package-01/attempt-07，纯准备不得创建或执行构建，Owner精确release后才建。独立Source03已接受；不重复无关后端/权限测试，但同版包/实际视觉及三业务/cold仍必验。0新Provider。

Owner准对当前已绑定PID23477/隔离Root作旧READ_UX_RC3_ACCEPTANCE_STATE.py完全相同12个normal GET白名单投影，仅读原已接受General结果/用量/偏好与W/M/CG自制测试对象，不读原Task/private prompt/DB/凭据，不写接口；仅内存替换新输出前缀UX_RC4_DIAGNOSTIC_BASELINE，旧脚本/旧回证不改。本次精确新输出evidence/UX_RC4_DIAGNOSTIC_BASELINE_BEFORE.json，标诊断非最终07回证。

### 同批首次许可提示普通返修（固定候选Source04，Package07尚不执行）

Owner实机在首次未保存公司文字许可时，章节Composer把continuity FRESH/no policy也提示“资料状态变化…旧费用授权失效”，而设置页明确当前从未授权（0占额）；这不是资料变化，属于普通首次使用提示错误。已保存的当前0.60/三W许可现VALID，不能为测试撤销或篡改。

Main仅追加解冻原已准 backend/app/company_execution_policy.py 和 backend/tests/test_company_execution_policy.py：仅在当前current_grant原拒绝分支区分FRESH/no policy的引导文案，仍同RuntimeScopeError拒执行，未知/MISSING/MISMATCH/旧policy分支保持原强阻断与提示；不变权限、价格、占额、anchor、事务、Schema、恢复。精确2文件修复，保Source03/QA/原Package07准备pins，Source04仅这两个文件增量并冻结；Source03已准前端4文件原样保留。独立只复首次提示/未知强阻断及受影响测试，不重复无关全产品。

Package07纯准备暂不执行Source03旧pins；Main在既有PACKAGE_02三准备文件中适配待接受Source04/QA04，保先前精确字节/哈希修订记录，由QA增量核后Owner一次release07实际构建。当前06诊断0真实Provider，最终三业务/cold继续同一最终包，非增加交付批次。

Owner接受Source04 manifestb90d1ad0/Seald2234c20/独立QA950af4d0：仅首次FRESH提示2文件增量、独立25policy检查与未知状态强阻断保持；Source03前端及其余48不变。资格为匹配包输入，不是Native接受。原Package02三准备文件可按前述scope适配04/QA950，保旧03配方资格历史；待精确新pins增量QA后Owner实际release07。

Owner接受07当前Source04配方增量QA ee21798a（script1b226/specbc1f/checka145），已精确签发OWNER_UX_RC4_PACKAGE_RELEASE_04.json，准现Main执行一次BUILD_UX_RC4_PACKAGE_02.py --execute，在fixed-package-01/attempt-07构建并只签staged App；不安装启动/资料凭据/Provider。Source04/QA950+Source03/QA579+Source02/QA767资格链保留，07后独立包核再Owner同版Native。诊断06已由Owner绑定工具正常Quit，父句柄实获23477 exit0（三服务端口空），正常退出证据native-rc4-01/result.json，三个未发送对话草稿和实际0.60三W许可保留；不同于更早旧36376未知退出，不混淆。

### 07已实际产出：只读包核与单哈希工具适配并行

包07 manifestf50fac36 / BUILD_ID bd98JmJYMwvLvBZaZ4T10 / Native663773b1 / carrierbdd9ae06，Main自核完整6803与50源码及签名通过，独立包QA尚待，非Native接受。Main仅准既有developer-01新写pid_native_control_ux_rc4_07.swift、pid_native_focus_ux_rc4_07.swift及同名无扩展binary、UX_RC4_NATIVE_PIN_PREPARATION_02.json。仅把原rc4工具产品SHA115d7ccd全字面量改为07 Native663773b1412c537947f935f17e192d767fe34bf263568b75c142cea0319be162，其余全部字节不变；只已有SDK编译和pure self-check，0AX调用/绑定/启动/资料/Provider。旧工具/回证完整保留，QA仅精确单literal/source/binary/diff/purechecks增量，实际绑定仍Owner后续release。

### 07安装/正常warm与同版cold的最小参数准备（仅prepare）

Main准在D新写INSTALL_UX_RC4_APP_02.py、LAUNCH_UX_RC4_APP_02.py、LAUNCH_UX_RC4_COLD_01.py、UX_RC4_NATIVE_RUN_SPEC_02.json、UX_RC4_NATIVE_RUN_PREPARATION_02.json，共5文件。复用已执行1fdd/b78安装与launch函数；仅当前07实际包/Source04/独立包QA/新工具hash、旧installed115d、新6637、运行输出和正确已观察到的前一退出证据适配，保留全部01/旧release/执行回证；不新增UI权限/技术/网络。输入只有已接受实际包/实际QA，不伪造待定PASS或hash。

未来唯一安装位置仍/Applications/Curis.app，源attempt07；当前06整App保native-install-02/previous/Curis.app，stage与安装receipt只在native-install-02，不重签。当前06已观察23477正常quit/Popen exit0回执native-rc4-01/result.json，验证该回执hash与Parent证据后才使用这一已观察状态，36376历史未知另外保持，不混。

未来warm输出native-rc4-02、warm release OWNER_UX_RC4_LAUNCH_RELEASE_02.json；未来cold输出native-rc4-03、cold release OWNER_UX_RC4_COLD_RELEASE_01.json；安装release OWNER_UX_RC4_INSTALL_RELEASE_02.json。各自全新且单用，不提前建目录或release。共同现存同Root dev16777229/inode88268446/UID501/mode0700、同sandbox93345、六字段/PGID/kernel/原最小HOME guard、Popen父句柄不变。cold与warm源码只有限固定Inputs/输出/operation及必要前序回执门差异；cold必须绑定真实warm normal exit0回执SHA/身份，并同包/同Root/三端口空，Owner另签release才执行，不自动退出或重启。

纯准备仅允许输出上述脚本/spec/check及纯校验结果，无安装/启动/AX/数据库/Keychain/Provider；数据与当前许可不撤销/恢复/复制。独立QA可一次增量核整套已有方法参数适配和精确前序门，Owner之后分别精确执行安装、warm、cold，真实生成另有批次费用门。所有真实进程值均在实际回执/Owner现场后填写，不预造未来PID/退出。

Owner接受独立07/新工具静态QA89e07239：6803成员/签名/BUILD_ID、14新模块+1387未改模块、Source04及19依赖链、新AX仅productSHA6637单literal资格已过。准将真QA/hash用于已准07安装/warm/cold纯准备；不等于Native几何/真实生成/冷启接受。

Owner接受Native07配方QAa2a616c6（installer132e/warma8cd/coldc59b/specbc45/prep54ce），准Owner精确新写INSTALL_RELEASE02、LAUNCH_RELEASE02、COLD_RELEASE01三JSON（实际名称按spec）；准Owner执行07安装至/Applications并保整个06于native-install02/previous，然后另签warm启动同Root至native-rc4-02并用已核07工具按新实际PID/kernel绑定。本次准新建native-install-02、native-rc4-02、native-rc4-03，仅各自已签执行门后创建，冷启需未来真warm四回证/normal0后另签，不提前运行。Owner亲自操作App本地UI/自写文本/正常政策/只读DTO/截图状态日志准许，真实Provider仍0/未释放，等新包live批费用准入。前序23477正常Quit/Popen0四SHA真绑定；历史52778不采用，36376未知另保留。

07安装02第一次在全部effect前预条件拒绝：89e报告仅链接工具prepare a35，原guard需要两binary完整SHA在QA JSON直见。native-install-02未建，0App/库/Provider操作，拒绝前release精确文本/SHA保OWNER_UX_RC4_INSTALL_RELEASE_02_PRECONDITION_REFUSED_01.json。独立QA仅补真实已核工具pin链薄报告，Main仅原SPEC02/PREP02适配真实QA path/hash并保先前字节，三脚本不变不宽guard；QA仅新Spec参数增量后Owner纠正release02元数据。全部同批普通元数据修复，不新计划/Scope/权限。

Owner接受薄QA df6046工具直pin与1d0b78配方元数据delta；三脚本仍132e/a8cd/c59b，新spec89c571/prep039a866仅QA三leaf引用纠正。拒绝前release原字节/SHA已保全，Owner重签同INSTALL_RELEASE02绑定新Spec/QA，Scope/guard/产品/资料权限不改，按原guard续执行一次安装。

Owner准对当前07 PID33289作相同12个normal GET安全投影（原General两结果/usage/pref及W/M/CG自制对象），原READ_UX_RC3脚本不变，仅内存新输出前缀UX_RC4_PACKAGE07_BASELINE_BEFORE；精确新证据evidence/UX_RC4_PACKAGE07_BASELINE_BEFORE.json，正常只读无Task/private prompt/DB/凭据/Provider。

### 同版统一安装交付并行静态准备（不制作/不执行）

Main准在既有D新写BUILD_UX_RC4_INSTALLER_01.py、UX_RC4_INSTALLER_SPEC_01.json、UX_RC4_INSTALLER_PREPARATION_01.json、UX_RC4_INSTALLATION_GUIDE_01.md，复用既有正常macOS DMG/签名/完整成员核方法，仅静态准备。当前候选07不可声称已Native接受；未来实际DMG只能绑定最终同版Owner Native接受收据+独立旅程QA，后续普通修复则重pin再核，不据旧版本局部相加。

未来候选交付输出仅本Task delivery-01（尚不创建），App字节取immutable已核候选07，stage仅Curis.app与/Applications兼容symlink及必要纯安装说明；禁止拷资料库/凭据/用户文件/Runtime缓存，保持原签名不重签不notarize/不引入账号或付费。创建DMG/只读挂载检查全成员/签名均须Owner精确release后，mountpoint也限定delivery-01下碰撞拒绝，绝不卸载他人卷。准备不写/拷/改Applications、不启动App、不hdiutil attach/no Provider；不可绕过Gatekeeper或安全授权。安装指南白话交代本地文字模型/手动媒体/外部服务边界、保护原资料与首次模型配置，不暴露技术id给普通用户。

安装产物Built/Verified与实际安装接受保持分别，拟定未来同字节包正常安装并启动回证所需精确对象/输出，但不预造实际PID/接受状态。Owner跟完当前07三业务真实对话/回原/cold后，再签同一版本实际制作/安装交付。此为已有L2范围内并行准备，不新计划/Authority/Backlog。

Owner接受07实际安装/identity/120几何及live批费用条件QA2f151a7b，精确签OWNER_UX_RC4_REAL_BATCH_RELEASE_01.json：本C714三W/真实assignment/唯一Flash及现有0.60政策，最多12物理文字请求（warm9+cold3），新外保守0.72+旧4.227072=4.947072<人类5，实付Unknown不当0。准Owner经真实GUI逐条发送固定SCENARIOS02消息，前次fresh身份/政策/模型/预算/对象/选段检查与证据必保；第三消息现场真实选段再核版本，不拿计划替选中；无私prompt/凭据读取/媒体音频Provider/外发平台/自动重试，UNKNOWN只查原。暖/冷同版整个旅程独立QA与Owner最终接受仍待。Owner运行证据/安全投影/真实请求ledger在已准native-rc4-02/03，三原保护General works不得重放。

### Native07真实CG选段P1失败，同批Source05精确修复授权

实际07 policyVALID、普通CG两轮真回复/计量confirmed、准确版本2e5及选区0..64/模型/文本均具备，collection.execution_authorized仍false使按钮禁用（122），第6请求未admit/未调用。根因只认显式server injected execution_grant，生产构造默认None，遗漏既有professional_grant(None)→CompanyPolicy.current_grant。此为普通P1接线，非缺人类授权，不准删guard/伪true/注旧env。Music无同类阻塞，静态检查不等于实机接受。

仅解冻原已准4文件：backend/app/content_growth_service.py、frontend/components/content-growth/ContentGrowthMain.js、backend/tests/test_professional_conversation_journeys.py、frontend/tests/contentGrowthWorkbench.test.mjs，当前前像与Source04一致（TaskStart精确哈希）。Main准collection逐当前模型用既有professional_grant+require_professional_grant只读形成per-model execution_authorized/notice，总bool仅兼容汇总；不输出grant/不占额/不prepare binding。前端仅消费当前选中模型的精确资格，缺失/false拒；send/selection/hash/源版本/pending锁和真正reserve/最终重验完全保留。测试必须覆盖真实policy无injected grant的collection→选中模型→selected发送接线、错模型/撤销/到期/未授权与GET零attempt/Task/Usage/占额，前端不能仅用伪总true。CompanyPolicy/预算/Schema/环境/音乐/其他46源测试不改。

Main同批保存Source04原证与4前像、固定Source05后direct独立QA仅受影响范围；Source/包/Native阶段仍分开。若另需文件先列精确scope，不自扩。原真实5调用/写作人工采用保持，来源不能假作最终新包全程。Owner暂停release01剩余发送，后续source/新包真实门另签；原5 usage confirmed/no retry/fallback，峰值CNY0.016520（非账单），新12最大CNY0.595968，合0.612488可UI预算0.62；独立USD峰值工程8合0.7349856，新保守外预留0.74+原4.227072=4.967072<人类5。当前不改许可不调用。

为续行提速，Main在Source05正式QA PASS后准直接纯准备D新BUILD_UX_RC4_PACKAGE_03.py、UX_RC4_PACKAGE_SPEC_03.json、UX_RC4_PACKAGE_PREPARATION_CHECK_03.json，复用已核07算法只适配真实05/QA/Source与future fixed-package-01/attempt-08、future OWNER_UX_RC4_PACKAGE_RELEASE_05.json，旧包/配方全部保留；不提前创建08/不执行，需Owner exact release后才一次构建。QA可并行准备受影响资格+08参数delta，不重开全产品Audit/历史回证。

### Source05之后同版08最小交付准备范围（Owner，2026-10-28）

为避免普通哈希参数适配反复转交，Main可在Source05正式独立PASS及08实际构建产出后，连续纯准备既有D内精确文件：pid_native_control_ux_rc4_08.swift、pid_native_focus_ux_rc4_08.swift、对应同名binary、UX_RC4_NATIVE_PIN_PREPARATION_03.json；只能把07工具的产品Native SHA字面量替换为实际08 SHA，其余源字节不变，已有SDK编译及纯自检，不进行AX调用。QA一次集中核08实际包和两工具，报告直接列manifest和两binary完整SHA。

包/工具独立PASS后准纯准备D内INSTALL_UX_RC4_APP_03.py、LAUNCH_UX_RC4_APP_03.py、LAUNCH_UX_RC4_COLD_02.py、UX_RC4_NATIVE_RUN_SPEC_03.json、UX_RC4_NATIVE_RUN_PREPARATION_03.json；沿用已执行07三脚本原有算法/身份/最小环境/sandbox/Root/前序退出/逐项hash强门，仅适配实际08/Source05/QA/工具及新路径。未来安装输出native-install-03（整份07保previous），warm native-rc4-04、cold native-rc4-05；Owner release为OWNER_UX_RC4_INSTALL_RELEASE_03.json、OWNER_UX_RC4_LAUNCH_RELEASE_03.json、OWNER_UX_RC4_COLD_RELEASE_02.json。现在不建输出目录、不安装启动；待Owner实际精确release才执行。前序只用native-rc4-02实际33289正常Quit/Popen0，不假造未来PID。旧全部字节及回证保留。

Owner准新写OWNER_UX_RC4_NATIVE_SCENARIOS_03.json及未来OWNER_UX_RC4_REAL_BATCH_RELEASE_02.json，前者准备而非执行放行：保留5已结算历史和旧批停止记录，以新代号区分旧消息；最终同一08完整12真实请求资格须独立核当前现场。经正常UI仅将同公司许可预算0.60提升0.62、保留累计已用0.016520，不能重置/抹除历史；外层本UX累计保守0.74加旧4.227072仍小于人类5，不是新加额度。所有调用/数据变更仍Owner实际GUI与原已准profile，凭据不读、默认库不改。

### 08统一安装交付最小参数适配（纯准备，2026-10-28）

Owner据Main只读差异接受原已批D内三文件参数范围：BUILD_UX_RC4_INSTALLER_01.py仅SOURCE/MANIFEST常量attempt07→实际08，所有函数/安全/打包/挂载算法不变；UX_RC4_INSTALLER_SPEC_01.json仅实际08 Source05/独立包QA/脚本SHA/sourceApp与各重复manifest/native/BUILD_ID身份绑定及method来源文案，原verifiedInventoryMethod方法固定不变；UX_RC4_INSTALLER_PREPARATION_01.json在改前完整保存原07四文件精确bytes/hash及QA4573c3eb历史，再记录新08纯检查/manifest。GUIDE_01.md字节01cb478d不改。不得修改源、签名方式、门条件或安装数据策略。

仅在08真实包工具独立PASS后做此纯准备，实际Native全旅程未Accepted不运行DMG/hdiutil或建delivery-01。未来Owner Native receipt与独立同版全旅程QA均必须真实，固定版本manifest/native/BUILD_ID与四journeyChecks守卫保留；不预填虚假接受，不以旧07局部或静态QA代替。制作/实际安装执行仍须Owner后续精确release，旧字节不丢失。

### 现有窗口不可枚举时的最小激活候选：仅纯准备，实际范围须CEO决定（2026-10-28）

Owner实际两次观察same PID46596/kernel1793175055.879040/window16317可恢复且随后AX只根节点、CG onscreen为空。CEO已协助点Dock和同桌面同时可见，仍复现；不能据此称窗口销毁或产品失焦hide。3个本轮Writing请求现已完成，无待处理生成；当前只记录新候选，尚未采用。旧control08/focus08没有可在无AXWindow状态下使用的activation入口。禁止open -a/-b、AppleScript、CUA、复用失效引用或扩大到系统授权界面。

Main获准纯准备D精确3文件：pid_native_control_ux_rc4_08_activate.swift、同名无扩展binary、UX_RC4_ACTIVATION_PREPARATION_01.json。复制当前已独立核验control08源，新增逻辑仅一个明确op activate-existing-app分支及必要少量纯自检；复用原verify完整PID/绝对路径/NativeSHA/内核启动时间/当前登录与私密边界，新增操作只对verify后NSRunningApplication(processIdentifier:binding.pid)已存在、未终止且对应原executableURL的当前App调用unhide/activate。调用前后再次verify，清空旧引用/token，只回报同绑定App状态。不启动、重建、open、reopen、枚举其他App或系统UI，不操作文件框/Keychain/安全权限/私密字段，不接受客户端任意App或路径，不改变所有既有Window role/AXRaise/键盘/引用/截图/退出守卫。原control08/focus08全部字节不动，不改50业务源/包08/Schema/数据。

只用已准本地SDK/compiler及Task缓存编译，既有72纯自检必须继续通过；新handler负例/失效identity门用内存注入或纯函数验证，无真实NSRunningApplication选择/激活/AX/系统权限请求。QA增量核精确diff/原core函数未变/新分支边界/所有pins/纯自检，只提出准备资格。Main和QA不得绑定实际PID调用新操作。

这份候选不授予新增Native实际操作权限。Owner必须在完整准备+独立QA后，向CEO给出具体范围与实现证据，获得明确同意才签单独执行release，绑定当前实际PID/kernel/路径/SHA/Root。若CEO不允许，继续保持窗口可见性阻塞；不能借持续自主授权绕过既有Native范围门。全程无新Provider、预算/当前App请求不重试不重启。

### CEO新增顺序要求：本轮完成后暂停迭代，先处理磁盘空间（2026-10-28）

人类原文：“从磁盘监视器看，现在项目任务占据大量本地电脑磁盘空间，这轮任务完成后先暂停，清理下空间”。本轮UX-RC4真实完整旅程/同版安装交付继续，不能以清理为由跳过剩余验收；本轮结束后不自动续开其他业务迭代，先转磁盘空间收口。当前不是立即暂停正在执行的本轮。

Owner准只读核算当前Task目录、相关已有包构建/缓存/临时副本的磁盘占用（不读取凭据或数据库正文），输出仅本Task evidence/DISK_SPACE_INVENTORY_01.json 和DISK_SPACE_CLEANUP_PROPOSAL_01.md。路径范围仅当前T、现有BusinessCatalog Task中的developer/remaining-app-delivery和旧DeepSeek Task；可读df与这些目录的du/stat来核容量，不全盘扫描或枚举其他个人文件。调查不创建清理目标、不移动/压缩/删除任何文件。

沿此前人类明确“移动、归档或删除先列清单确认”的约束：后续实际清理必须给出精确路径、占用、归属、保留/恢复与引用/Git/证据检查、必要保留项后一次确认。保留当前源码/所有用户已有改动/真实或保护库/凭据/当前App和最终安装包/唯一必要验收证据；旧构建/缓存可作为候选，不因文件名或历史版本自行删除。当前无删除/归档/移动授权。

### CEO明确允许本轮同版隔离Curis激活（2026-10-28）

人类对已完成17生产行/80纯检查/独立QA16e95899候选明确回复：“授权本轮同版隔离 Curis 激活”。Disposition: PROMOTE（只该Native操作范围）；Status: Review；Authority Class: CURRENT / HUMAN EXECUTION GRANT；Owner: Delivery Owner。

准Owner在本轮同版隔离验收warm/cold中，仅使用固定新工具50f84088，对每次实际已核验PID/绝对路径/内核启动时间/NativeSHA与同一Root的既有Curis执行activate-existing-app。绑定前和调用前后所有原身份/私密/登录守卫保持；没有launch/reopen/进程重建/SystemUI/Keychain/其他App权限。每次返回只是请求状态，须原工具fresh snapshot证明Window确实可读后才继续原已授权业务UI动作。首份Owner精确执行release仅本Task OWNER_UX_RC4_ACTIVATION_RELEASE_01.json；当前PID46596，未来同版cold新PID须实际启动回证和单独OWNER_UX_RC4_ACTIVATION_COLD_RELEASE_01.json，不套用旧binding。

Owner运行日志限当前native-rc4-04或已准cold05内activation-序号JSON；旧工具/Source50/App08全部不改。真实文字仍原12条release02/累计CNY5，无新增Provider次数或费用额度。功能本轮结束后按CEO新要求暂停并先精确清理清单确认，资料库/默认资料不动。

### 同已获准激活范围内普通修正02：请求接受但窗口未恢复（2026-10-28）

Owner实际首份activation release01/同46596绑定已执行一次，系统返回activationRequestAccepted=true、unhideRequestAccepted=false、windowRecoveryVerified=false；原工具两次fresh snapshot仍只有AXApplication/windows[]，故没有宣称恢复、没有点击采用或新Provider。该失败回证/01源与binary全保留。CEO已经明确允许的效果仍仅当前既有同版隔离App取消隐藏并置前，本条不新增操作类型、目标或系统权限。

准Main纯准备D新3文件：pid_native_control_ux_rc4_08_activate02.swift、同名binary、UX_RC4_ACTIVATION_PREPARATION_02.json。复制固定01候选，唯一activate-existing-app分支内复用原control.raise已经使用的AXUIElementSetAttributeValue(当前已verify的ax, kAXFrontmostAttribute, true)，并将既有NSRunningApplication.activate选项改为activateAllWindows，仍仅此已存在同PID/App的窗口、无新window创建或reopen。调用前后原verify/target验证/清refs均保留，失败明确返回，不接受新参数或读取/操作其他App。可返回当前App的AXFrontmost、NSRunningApplication.isActive/isHidden等无内容状态用于判断，但不能用bool代替原工具fresh Window实际回证。除该新增分支的最小修正/必要纯测试，不动原72 core/所有原操作/隐私/Window守卫与01已执行文件。不得新增minimize/窗口设置、全局UI、SystemUI、open、reopen或其他操作。

现有已准SDK/cache纯编译+80纯检查与必要分支静态/负例；Main/QA不实际绑定或调用。独立QA通过后Owner准在原人类“本轮同版隔离Curis激活”范围内签OWNER_UX_RC4_ACTIVATION_RELEASE_02.json精确绑定新toolSHA/QA/实际Root/PID/kernel并实际验证。02仍失败则保留现场，不继续盲目叠加工具操作。50业务源/App08/费用目的不变、0新Provider、不重启或重发。

### 同轮L2从最终DMG实际安装/启动的并行纯准备（2026-10-28）

Owner当前08实机继续，activate02实际恢复Window已观察并完成W三轮/人工采用；全三业务/冷启尚未接受。本条只为最终同版DMG实际安装交付的既有L2范围，不能创建新业务批次或重建App。

准Main仅在D新4文件：INSTALL_UX_RC4_DELIVERY_APP_01.py、LAUNCH_UX_RC4_DELIVERY_APP_01.py、UX_RC4_DELIVERY_INSTALL_SPEC_01.json、UX_RC4_DELIVERY_INSTALL_PREPARATION_01.json。复用已实际接受INSTALL_UX_RC4_APP_03/LAUNCH_UX_RC4_APP_03全部身份/完整成员/原目录保全/最小env/sandbox/HOME不变/6字段/PGID/实际前序退出/父句柄方法。安装来源必须为未来真实最终delivery-01安装包的本任务独占只读挂载内Curis.app，挂载前核真实DMG SHA/独立QA/同版Owner Native接受与独立全旅程QA，实际挂载卷归属和目标新鲜目录明确，退出只卸载本次自己的卷。来源manifest/native/BUILD_ID严格等同已接受08，不重签。

未来只准新输出native-final-install-01（含staged/previous保整份当前08）和native-final-start-01；只读挂载点delivery-01/installation-mount-01，碰撞/软链/归属不明拒绝。安装目标/Applications/Curis.app、Root仍现有旧DeepSeek app-root-01，不读写默认DB、不改OS权限、不复制资料。前序须最终cold05真实normalQuit/Popen0四回证，不能预造PID、退出、DMG hash/Native接受。未来Owner分别OWNER_UX_RC4_DELIVERY_INSTALL_RELEASE_01.json和OWNER_UX_RC4_DELIVERY_LAUNCH_RELEASE_01.json；实际DMG未产出时只能明确待填prepare状态，不能假PASS或实际execute；需要的真实pin只能在实际产出后最小参数更新并保前版字节，不改已核方法。

Main/QA此刻只静态准备/内存fixture、无hdiutil/mount/安装/启动/AX/Provider/现存DB操作，无全App拷贝或额外大空间目录创建。Owner先跟完08全旅程接受，再制作同版DMG和实际安装/0新生成启动复核。现有installer08纯准备与QA8f3f不重复改算法。安装/启动各自精确release之后由Owner执行，最后才可INSTALLATION ACCEPTED；Built/Verified不等于实际安装接受。完成本轮后按CEO要求暂停功能迭代并先清理精确清单确认。

### Native08实跑CG保存执行依据遗漏：同批Source06精确修复（2026-10-28）

实际新W三轮/采用与CG普通两轮均已成功；CG选段点击后页面明确“先保存本次责任员工与模型依据，再发送”。normal当前v2e5的work.assignment_ref/recipient_ref/model_key全空，虽然合法当前负责人和Flash已在UI继承显示。该错误是backend prepare_message唯一保存依据比较守卫，位于消息/attempt/Provider前；实际会话无新CEO消息/attempt，normalUsage无新条目，Company占额0和峰估35388micro与点击前完全相同。第6GUI意图已保留为REJECTED_BEFORE_MESSAGE_ATTEMPT_OR_PROVIDER，实际本新版5次成功物理调用，前07历史5次另保留。Owner暂停旧release02其余发送，不重试UNKNOWN，也不改真实库绕过UI。

只解冻原已准Source05的3文件：frontend/components/content-growth/ContentGrowthMain.js、frontend/tests/contentGrowthWorkbench.test.mjs、backend/tests/test_professional_conversation_journeys.py。前像精确SHA见TaskStart.source06Repair。其余47源测试与Backend生产/公司政策/预算/credential/runtime/schema/原Source05/包08全部冻结。

修复目标：UI当前合法显示的员工/模型选择，应在用户明确点击已有“保存正文或脚本”时成为这一新内容版本的work执行依据，包含当前assignment_ref、对应company_employee_ref、model_key；不能仅显示已选却继续保存空依据。优先最小save payload接线，必要既有notice与selected-send guard同步反映“当前选择尚未保存，先保存再重新选择”，不新增业务页面/产品设计。无可用模型或尚未授权时本地正文编辑/保存保持可用；不伪造资格/自动占额/执行，不默默替换既有合法或未知旧依据。不自动保存或静默把旧Selection换到新版本；保存后必须实际重选新保存版本，旧source/version/selection guard继续拒绝。

真正send、context/tenant/company/assignment/model/price/budget/selection/pending/final guard均不放宽。Source05当前模型执行资格投影保留。用可执行生产逻辑验证空旧basis→合法UI选择→明确save payload正确→保存新版本→旧选段拒绝/新选段发送；至少覆盖missing/foreign/stale employee/model、本地无模型保存与已有依据不被静默覆盖。Backend test保留正确拒绝空basis/零Task/Usage/占额，再用合法正常业务save（仅新测试fixture）验证保存依据后的真实prepare/send路径与旧版拒绝，不修改Backend生产守卫。

Main先只读确认Music是否存在同类执行依据保存契约遗漏，现有已批准Music源/测试只读，不先扩大write；若有真实缺口列精确文件/前像/依据再Owner登记，不凭猜测改。尽量一次固定完整Scope Source06，保Source05全部前像和收据，direct QA受影响3文件，其他资格保留，不再全产品Audit/新UI探索。

费用仍人类总CNY5：当前UX已确认10个实际调用（原07历史5+本08新5），CNY官方峰估累计0.035388（非实付），USD工程8界0.0424656。若固定06新最终版再完整12，CNY上界合0.631356可通过正常UI累计预算0.64；独立USD上界合0.7576272可保守外留0.77，原4.227072+0.77=4.997072<5。旧版真实与拒绝分别保全，后续新12要新的固定版本/独立准入/Owner精确release，不能聚合历史完成；当前不发新调用、不改许可。费用新限不是另加5，不减少maxOutput或放松产品边界来凑通过。

当前只准Source06普通修复，不准构建/安装/启动。匹配包09若必要预计沿已核单产物约1.2GiB，后续Owner独立精确gate才放行，不为此提前复制整包/创建目录。本轮完成后先停功能迭代再清理磁盘，原精确删除清单Gate保持。

Source06同批必要小回证精确输出（沿原D，不新建目录）：
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_SOURCE06_PREIMAGES.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_SOURCE_MANIFEST_06.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_SOURCE_SEAL_06.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_PATCH_06.diff`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_SOURCE_REVIEW_06.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_OUTPUT_MANIFEST_06.json`
只写小preimage/50-filemanifest/seal/受影响diff/review/output index，不复制完整源码/整包。旧05/08回证不改。Music只读已确认无CG同类saved-work三元组契约，不扩大Music写。QA按受影响源与既有资格复核，不全产品Audit。

### Source06后匹配09：原算法精确参数准备（非执行放行）

Main可在Source06固定后沿Source05匹配08已有算法准备以下D精确文件；不要提前建输出目录/复制App。新attempt-09 build仅后续Owner exact PACKAGE_RELEASE_06.json可执行；package/source QA必须真实齐备，禁止填假未来PASS。Backend生产与14模块都应保持Source05/08完全相同，可验证carrier相同但不得承诺或替代实证；不为了优化重新开发工具。

- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/BUILD_UX_RC4_MATCHED_APP_04.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_PACKAGE_SPEC_04.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_PACKAGE_PREPARATION_04.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_09.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_09`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_focus_ux_rc4_09.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_focus_ux_rc4_09`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_09_activate.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_09_activate`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE09_TOOL_PREPARATION_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/INSTALL_UX_RC4_APP_04.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/LAUNCH_UX_RC4_APP_04.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/LAUNCH_UX_RC4_COLD_03.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE_RUN_SPEC_04.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE_RUN_PREPARATION_04.json`

包配方03→04仅Source06/实际sourceQA/attempt09/release06参数；原单层sandbox/50file/485+输入/依赖闭包/签名/预算/Root隔离算法保持。09新Native实际出包后才可从08 control/focus与已授权activation02仅换productSHA编译，全部原纯守卫测试与激活支路一致；不得新增Native操作/权限。

安装/暖启/冷启配方只参数：原08 PID46596 kernel1793175055.879040、children46766/46767/46776，经Owner normalQuit/Popen0/ports空真实退出，parent native-rc4-04/result.json SHA013d9cdb0f5e52bbca9c5fc9237f6819ba6ecfac932261a2b0b99e6e2efcbfbe；另三receipt按实际binding/started/authorization读取，不能凭空命名或预填futurePID。安装native-install-04整份保08到previous，暖启native-rc4-06，冷启native-rc4-07（冷启四前任收据未发生前明确pending）。新的Owner INSTALL/LAUNCH_RELEASE_04与COLD_RELEASE_03分开真正放行；same approved Root/profile不变，不读DB/credentials，不forcequit、不mkdir/launch。

旧pending installer01与final delivery install/launch01四脚本/规格/准备尚未执行，可在原精确允许范围按真实09/最终cold07回证更新参数并保旧版本bytes/preimage。真正DMG产出/来自DMG安装与启动仍须同版完整实际旅程接受+独立QA后Owner分别放行；静态准备不当已经交付。现不授权构建/安装/启动/挂载/新的Provider调用。

Owner下一固定Source06/匹配09完整实跑准备精确输出：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_NATIVE_SCENARIOS_04.json` 与实际准入齐备后 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_REAL_BATCH_RELEASE_03.json`。当前scenario仅准备不发调用；新nonce W雾灯六三/CG晴岸五四/M潮星一七，三业务每项3warm+1cold，共12新物理；原全部10实际调用和1已知拒绝独立保留，不替代最终同版。场景4需明确CG先通过正常UI保存合法默认work新版本，随后实际重选保存的新source/version再发送；不能填假预见版本。实际Source06 hash已知，Package09/Native实际出包前null/pending，不伪造。当前预算/真实发送未放行。

Owner接受Source06仅本次修复源码资格：manifest5e3af397/seale62b9e91，fresh50哈希及3准确delta已核；独立QA c8440602（63前端/15隔离后端）通过，backend生产原样。Disposition PROMOTE仅进入下个匹配候选构建门，不是Native或产品接受。Main可在已准04配方绑定此真实sourceQA后交配方参数QA；没有执行构建release之前不建attempt09/复制包。

Owner实核Source06/50源和配方04输入真实SHA、独立Source c844及配方0da167b4后，一次构建放行：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_PACKAGE_RELEASE_06.json` SHA9015667d984e607ea863902c94c67f0bfcceea83a018eb4211a0e844af797fff，只新鲜`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/fixed-package-01/attempt-09`匹配09 staged App/正常签名/evidence；现有算法与保护不改，不安装/启动/Provider/读DB凭据。Main正常执行后直交QA全成员/签名/源/模块、Owner核后续安装门。

Owner原操作的09后续精确release输出如下，当前仅登记路径、不是执行：
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_INSTALL_RELEASE_04.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_LAUNCH_RELEASE_04.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_COLD_RELEASE_03.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_ACTIVATION_RELEASE_03.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_ACTIVATION_COLD_RELEASE_02.json`
09激活沿CEO已准本轮受限现有App取消隐藏/置前和已审02原算法，仅实际新PID/路径/内核启动时刻/09 productSHA绑定；须安装暖启真实发生+三工具纯/静态QA后再独立Owner release，不预写未来PID、不新权限/系统UI/他App。冷启的实际binding与激活release只在原暖启真正常Quit/Popen0后才准填。仍同原Root/profile保护，旧日志保全。

Owner已核真实09包/三工具/Source06/13pin与独立安装参数QA85373a91、08真实退出0及空ports，精确release `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_INSTALL_RELEASE_04.json` SHA44b2b10ecaca9de616ef1816a2b9ea2b7c7b2c4e183d99a0d5324083ec0bc8ad。允许一次正常stage09→整份08原inode保留到native-install04/previous→激活同字节09目录；不启动/Provider/DB/凭据访问。失败按已审原算法保全/恢复目录，不强杀。暖启另真实安装收据后放行。

Owner actual install04脚本exit0，receipt954b961d verdict INSTALLED_BYTES_VERIFIED_NOT_LAUNCHED，新Nativec996；整份08备份同inode90193028。真实安装收据核过后单独暖启release `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_LAUNCH_RELEASE_04.json` SHA41f0b20f38ef3510ed62d83c6e92de0bbebd7d1f03003b17768425e45bf35258：一次同Root/profile09 startup到native-rc4-06，保父Popen句柄、不发新Provider/不replay保护work。待真实PID/内核时刻/根6env检查后才允许绑定新工具；cold07仍未释放。

### Source07 同批共享发送CTA对比度普通视觉修正（09零调用实机前置发现）

09实机CG明确“保存正文”确实新建a89c2729版本并保存合法assignment/recipient/Flash，正文64字未变，fresh重新全选、填写建议后真实发送按钮enabled；没有任何新模型调用。但Owner已实际view截图126：普通与选段composer发送CTA均白底白字、不可辨读。Source确认CG .main button的background surface specificity覆盖SharedConversation.js发送button的Tailwind bg-ui-primary，而text-ui-primary-fg仍白。不能拿AX enabled当视觉通过。

精确解冻只2文件：`frontend/components/v1/SharedConversation.js`、`frontend/tests/conversationProductization.test.mjs`；前像SHA在TaskStart.source07SendVisual。最小共享composer修复，使用已确认ui-action-primary-bg/fg主题token，使真实主发送按钮跨CG/Writing/Music父级button reset仍清楚可见、禁用/忙态仍诚实，不设计新界面，不修改任何发送/费用/权限/Selection/Provider/状态逻辑。必要生产渲染测试验证三业务submitLabel、light/dark token、disabled/busy及父选择器覆盖下inline/高优先样式；不引入新库，不镜像虚假浏览器。

Source06其余48文件不改，后台14/carrier/模型系统守卫全冻结；09包/实际zero-call保存/新版本、全部失败图证保留。Main可沿既有D Source07六个小文件标准命名 PREIMAGES/MANIFEST/SEAL/PATCH/REVIEW/OUTPUT，准确50项同schema，只2delta；不要复制整源码/包，不新目录。Main普通修正先行，Owner并行完成09三业务零调用本地前置检查，再一起固定最终候选；暂不构建下一包或放任何模型。若Owner发现更多同类视觉问题直接同批合并，不逐按钮完整验收轮次。最终完整12须同一最终匹配版本，已有10真实调用费用保留，5元不变。

Source07 Owner已核50hash及独立f80f5f09接受仅source qualification（实际视觉仍待）。09本地三业务选段/模型/绑定可发送前置均实际通过，CG a89保存依据生效，source9共0新Provider/总估35388micro；唯共享CTA视觉FAIL，图126/127/128保留，未另扩大产品审查。09 PID64097现normalQuit/父54793实测Popen0，服务PID64236/64242/64248已空；native-rc4-06/result SHA36e43a988324eb9379bdd5f243faeaf4718760391f9f26d5393a5e8ccab25366。
匹配10原算法纯准备精确D输出：
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/BUILD_UX_RC4_MATCHED_APP_05.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_PACKAGE_SPEC_05.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_PACKAGE_PREPARATION_05.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_10.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_10`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_focus_ux_rc4_10.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_focus_ux_rc4_10`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_10_activate.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/pid_native_control_ux_rc4_10_activate`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE10_TOOL_PREPARATION_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/INSTALL_UX_RC4_APP_05.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/LAUNCH_UX_RC4_APP_05.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/LAUNCH_UX_RC4_COLD_04.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE_RUN_SPEC_05.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/UX_RC4_NATIVE_RUN_PREPARATION_05.json`
不新建目录/整包，不执行。配方05仅source07+真实QA+attempt10+Owner PACKAGE_RELEASE_07参数；实际Native10出包后工具只从09替换productSHA，activation沿已准现有App02操作，不新增UI权限。install05整份保09、warm08/cold09继续原Root/profile，前任仅真实native06四pin，cold07/05没有发生不当作回证。未来实际安装/暖启另Owner INSTALL/LAUNCH_RELEASE05；cold09需真warm08退出后另COLD_RELEASE04。旧D所有03/04与09App全部保留；pending L2三+四文件沿原精确Scope之后可按真实10/未来cold09 repin且lossless保09bytes，不额外文档目录。Source7其余48和全部后端/费用/权限冻结。Owner PACKAGE_RELEASE07文件尚未写，当前0新调用。

Owner Source07 all50 fresh＋实际QA f80f/配方1fa7及05输入核过，一次匹配10构建release：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_PACKAGE_RELEASE_07.json` SHAf64999fa6f1b5bef22977979aa3daa2ad5fca5bc01b859899d7efc8efdfee6f1；只新鲜attempt10原算法staged build/签名/小evidence，不安装/启动/Provider/DB/Keychain。09全部真实0调用前置与视觉失败保留；后续三业务真实CTA可见仍须实机，不拿静态色值PASS替代。

Owner匹配10后续精确scenarios05/REAL_BATCH_RELEASE03/install05/launch05/cold04/activation04/activationCold03路径已在TaskStart登记。Scenario05仅准备 Source07实hash/实际10 pins尚null，消息新nonce星港六四/晴帆四七/潮笺九二，仍9warm3cold共12/old10保留；warm按Music→CG→Writing先覆盖未真回原链，但每域顺序1→2→选段3不变。未放新Provider，Root已存累计.64/epoch/35388保留，实际新PID/CTA/价格/liveQA齐备再单独release03。

Owner已fresh核13pins/三配方及Native05独立QA73a19e0a、实际09前序正常exit0/空进程和ports，放行单次正常10安装 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_INSTALL_RELEASE_05.json` SHAbb6a2854cc77d0334b9963d96a17d70505e20b148497e0213512af7cf57f6d1c。整份09原目录保native-install05/previous，不启动/Provider；暖启08等真实安装收据另LAUNCH_RELEASE05，cold09未准。原Scope/Root/权限/数据保护不变。

Owner实际安装10脚本exit0，receipt333e4561、Native97d2、整份旧09同inode90433101保全。基于真实安装单独暖启 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_LAUNCH_RELEASE_05.json` SHAb89f8c2df492f7b8849ebfdc7eb60e652cc1c82b827c525ea4cacaad52211b16：同Root/profile到native-rc4-08，保实际Popen父句柄，0新Provider/不replay；真实PID/6env/CTA可见/liveQA后另ModelBatch03，未来cold09仍未准。

### 2026-10-29 — 同版10实际完整旅程、安装收尾与只读清理准备

Owner基于现有CEO持续交付和本轮后暂停清理指令，登记精确收尾输出：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_NATIVE_ACCEPTANCE_01.json`、`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_DELIVERY_ACCEPTANCE_01.json`、`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/developer-01/DISK_SPACE_CLEANUP_CHECKS_01.json`、`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/qa-01/DISK_SPACE_CLEANUP_QA_01.json`。只消费当前同版Source07/Package10实际Native+独立全旅程回证，不改原封存OWNER_FINAL_UX_ACCEPTANCE，不把源码或暖机有限PASS当完整交付。全12Provider已完成并关闭发送门，新调用0授权。Main可在既有D只读核现有清理提案9精确路径的归属、Git、引用/唯一输入证据、可再生、运行占用和恢复；QA在现有Q独立核，普通发现直接协调，输出小JSON，不新Plan/Backlog/Review目录。零业务代码变更，零删除/移动/归档；完成安装实际接受后暂停功能迭代，CEO精确清理清单确认仍为必要下一Gate。

### 2026-10-29 — 本轮限定交付已最终签收，功能迭代暂停

Owner签收 `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/OWNER_UX_RC4_DELIVERY_ACCEPTANCE_01.json` SHA f4477378d0dc6981e17c8f9ad3a76b54458975a1be0164768c6f4821cf373647。固定Source07/Package10全12真实旅程经独立a705接受；匹配DMG c22c经独立9629接受；实际从DMG安装、正常启动、三业务保存结果/对话读回、预算94608/0保持、0额外调用、最终正常Quit/原父31804 exit0，经独立4c118接受。旧App inode90494090保全，原封存dd99不改。当前目标整批闭合，不声明全V1/C01/通用员工Result及外部能力接受。按CEO指令停止功能自动续派，转既有清理提案8个精确编译缓存约1.970GiB待CEO确认；8个完整构建/前端目录保留，472 donor03输入保留，尚未删除/归档/移动。后续仅确认集合的新鲜身份/运行/保留项核验与清理，不另启产品设计/开发。

### 2026-10-29 — CEO已确认精确8缓存清理

CEO原话“确认仅清理这8处缓存”。仅删除原DISK_SPACE_CLEANUP_PROPOSAL_01.md表内8个绝对路径，其他完整构建/源码/App/DMG/资料/备份保留；TaskStart.approvedCacheCleanupExecution记录精确Scope。Owner先作新鲜身份/占用/最新输入/保留指纹核验，再精确执行和df/du/保留项复核；独立QA只读检查实际结果。精确输出：`/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/DISK_SPACE_CLEANUP_PREFLIGHT_01.json`, `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/DISK_SPACE_CLEANUP_EXECUTION_01.json`, `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/evidence/tmp/execute-approved-cache-cleanup-01.py`, `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-UX-INTERACTION-AUDIT-20261026/qa-01/DISK_SPACE_CLEANUP_EXECUTION_QA_01.json`。这是既有Task后续清理，不恢复功能迭代，不调用模型，不改业务代码或受保护数据库。

### 2026-10-29 — 获批8缓存清理已独立收口

清理已按CEO确认仅删除8处精确编译缓存（目录计量约1.970GiB），独立执行QA012c562c通过，550保留文件及3份App完整指纹未变；执行前后df可用空间4.45→6.42GiB（同期净变化约1.972GiB，不作精确物理归因）。功能迭代继续暂停，等待CEO下一明确任务。 执行报告SHA 3df2eda9bd8a4ebfae140f01afb30c586400f7caa81821e201db569c95ab1c79；独立QA SHA 012c562cd3011e563eb07442b3f1d0fb469dadeda490ff47782f16d8bfabccc2。Scope精确8路径全部不存在，8完整构建根、550保留文件/472 donor、3份App各6803成员hash/mode、隔离Root/DB仅元数据前后一致。没有扩大删除、恢复功能迭代或发模型调用。下一Gate仅CEO下一明确任务。
