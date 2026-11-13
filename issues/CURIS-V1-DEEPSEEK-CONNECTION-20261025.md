# DeepSeek 连接恢复与真实工作闭环

Status: Review
Authority Class: EVIDENCE / EXECUTION ISSUE
Owner: Delivery Owner
Updated: 2026-10-26
Task ID: CURIS-V1-DEEPSEEK-CONNECTION-20261025
Risk Level: P0 凭据/系统边界；P1 模型执行、保存和重启

## CEO 来源与当前目标

CEO 将模型接通调整为当前优先项，并明确“继续 DeepSeek，验证费用上限 5 元”。
此前模型 DEFERRED 只保留为历史决定；本次恢复的是本 Issue 的精确诊断/验证范围，不扩大外部发布、真实经营数据或其他 Provider。
目标为凭据保存→Health/模型发现→默认/员工选择→真实 Work/Result/Usage→退出重开后继续，不以连接按钮或 API200 代替闭环。

## 当前事实与待证假设

10-13 package06 真人一次 DeepSeek 尝试报 native_store/unknown，未记录实际 OSStatus，保存结果仍 UNKNOWN；不能推定旧原生条目存在/不存在。
当前源码已从后端到 frontend/lib/api.js 传递可选整数 OSStatus，但 ModelManagement 只显示固定文案。06 原启动使用额外 Seatbelt profile，是否影响凭据 API 尚待验证，不据此改写历史根因。
RC9 本地手工 L1/L2、此前已接受的有限 Cloud 证据保持各自版本/范围；不能当作本次真实连接通过。

## 本阶段 Allowed Files

- /Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DEEPSEEK-CONNECTION-20261025.md
- /Users/yy/Documents/Curis AI Workspace/docs/07_Decisions/DECISION-2026-10-25-deepseek-connection-resume.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md
- /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/TASK_START.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/SOURCE_INPUT_SEAL.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_FINDINGS.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/PLAN.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/CHECK_RESULTS.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OUTPUT_MANIFEST.json

## 本阶段 Allowed Directories

- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/preimages
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/qa-01

## Read-only source inputs

- /Users/yy/Documents/Curis AI Workspace/backend/app/credential_vault.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/main.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/ai_capability_registry.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/model_gateway.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/model_preferences.py
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js
- /Users/yy/Documents/Curis AI Workspace/frontend/lib/api.js
- /Users/yy/Documents/Curis AI Workspace/frontend/lib/v1FrontendApi.js
- /Users/yy/Documents/Curis AI Workspace/backend/tests/test_v1_p0_003_keychain.py
- /Users/yy/Documents/Curis AI Workspace/backend/tests/test_phase5_credential_vault.py
- /Users/yy/Documents/Curis AI Workspace/frontend/tests/modelCredentialRecovery.test.mjs

## 三角色分工与本阶段接受

- Owner：当前事实/历史失败分层，精确隔离与费用边界，选择最低成本真实诊断方式，同版 App 最终验收及原唯一看板。
- Developer：仅写 developer-01，静态审查当前凭据链与06启动限制，必要私有 fake-only 复现/工具准备；提交最小可执行方案和精确候选源码 hunk，不直接改 canonical 业务源码。
- Independent QA：仅写 qa-01，与开发并行独立审查失败边界、可逆测试身份、无秘密泄露/无默认资料访问、预算/一次尝试/冷启动真实工作验收矩阵；普通准备问题可在本次范围内直接反馈 Main。
- 假凭据/Mock 仅用于离线故障注入，不能接受真实模型能力；此阶段不访问真实 Keychain、默认 DB、App 或 Provider。
- 如准备离线测试，三个 CURIS DB 别名须在任何导入之前绑定同一私有测试路径；框架/网络/子进程/真实 DB 由哨兵拒绝。未经审查的普通导入或测试不能触发默认 bootstrap。

## 真实执行 Gate 与完成标准

费用总上限人民币 5 元，连接 Health 与业务请求均计入。价格/最大输入输出/物理调用数必须先核实；不能验证上限则不发请求。
真实凭据只由人通过 Curis 密码框输入。Owner 先确定当前包、唯一测试进程、全新隔离根、测试条目身份/恢复策略，并经独立 QA 后放行；不读取或清理既有未知 Keychain 条目。
最终需要真实保存/可用性、发现/选模、真实员工 Work/Result/Usage、正常退出和冷启动续用实证。失败保留具体 stage/整数 OSStatus/时点和 uncertainty，不记录原始异常/secret，不自动重放结果未知的写入。
本阶段只做可独立推进的离线审查；真实执行或最小源码修复由后续精确 release/hunk grant 承接，不靠不断扩建工具或连续打包补结论。

## 保留与禁止

- No default/protected DB reads/writes or credential enumeration/resolution/deletion
- No existing App control/relaunch or live security/Provider operations before exact live gate
- No broad keychain directory/system-permission expansion or old-item cleanup
- No business source/Runtime/Schema edits before exact follow-up hunk grant
- No broad source rebuild or installation replacement before evidence shows need
- No Product/Frozen product contract changes; no Git mutation; no new Agent

进度只看 [原唯一执行看板](<../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)；Source/Review/QA/Package/Native 接受分别记录。
Next Task: Owner reviews Main + independent QA offline return; release smallest legitimate native diagnosis then one real DeepSeek journey within total 5CNY, or report genuine credential/system gate

### Phase A 最小只读输入补充：员工调用与物理尝试

- /Users/yy/Documents/Curis AI Workspace/backend/app/conversation_service.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/orchestrator.py
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/EmployeeConversation.js
- /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/SharedConversation.js

仅用于证明实际员工caller的输入/输出token边界与物理调用数，不新增源码写权限或执行权限。实际测试需另有Owner精确release。QA所提旧PID52778仅保留为来源待核的历史定位，不作为本Task当前App绑定；本Task尚未启动App。

### 最小原生诊断技术 Release 准备（尚未执行）

Owner待Main独立代码审查和QA范围核对后，可在本CEO恢复模型指令内发布一个无真实Secret/无Provider/无DB的精确synthetic probe。唯一helper为qa-01/native_probe.py；不再开发平行工具。

新增Allowed Files：
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_NATIVE_RELEASE_01.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_NATIVE_RESULT_01.json

新增Allowed Directory：/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-01

只操作新随机service/tenant/credential；一次store，只有明确成功才读回并删除同条目；store失败/超时/未知时停止，无读回/删除/重试。stdout只取phase/整数OSStatus；stderr原文不落盘/回显，只记字节数与hash。若需要新增系统授权或发现旧条目/真实资料风险，停止该动作交CEO。该探针不接受签名App/真实模型成功。

### 现有有界 General Work 路径只读核查

- /Users/yy/Documents/Curis AI Workspace/backend/app/employee.py
- /Users/yy/Documents/Curis AI Workspace/backend/app/runtime/general_execution_limits.py

优先核查已有general_limits是否能合法完成真实员工Work/Result，以复用既有硬上限而避免为本轮测试改全局对话合同；仍无源码写权限。

### Owner exact synthetic-native release 01

Allowed File: /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-01/owner-native-profile.sb

Main对唯一bd34 helper的7项假接口/静态检查通过，QA已封存范围/矩阵，Owner逐行复核后放行一次独立Python新namespace合成探针。此技术release仅为本CEO模型恢复范围内的自制占位项，非旧条目或真实Key、非App/Provider接受。Kernel限制helper直接网络与Curis资料路径，未限制正常Security框架系统内部传输；不改变系统设置/权限。精确nonce/service/account/源码/程序/profile/hash和允许动作写OWNER_NATIVE_RELEASE_01.json，未知停止不重放，输出只保留白名单阶段/整数OSStatus及字节/hash元数据。

### Owner精确App阶段01：同包新业务根与正常Key输入准备

Allowed Files：
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_APP_RELEASE_01.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_APP_RESULT_01.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_APP_BINDING_01.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-stage-01/app-profile.sb
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-stage-01/launch_owner.py
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-stage-01/safe-ax-transcript.jsonl

Allowed Directories：
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-stage-01
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-root-01
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-root-01/cache
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-root-01/cache/tmp

Owner以已接受installed RC9/Source/完整12705成员核对启动一次当前不存在的app-root-01；现有install-01 AX二进制只绑定该新PID/路径/SHA/启动时间，跳过secure节点、禁止截图及密码value读写。保留父进程直到正常App退出。启动后先核kernel身份、端口与私有root/子环境白名单、全新Company归属/无旧credential metadata，满足后才请人输入Key并一次点连接。系统常规WebKit缓存可能共享，此为已明示限制，不读/清理它；不宣称全新浏览器profile。Kernel允许固定loopback和解析的官方DeepSeek:443/DNS，拒绝默认Curis数据子目录和旧业务roots、.env和CLI既有凭据目录，不限制正常Keychain内部必要通道，不扩大系统设置权限。所有模型请求仍按预算Gate；首次/冷启发现最多2 GET，两个新General Work各4096bytes/2048output/一次outbound，canonical Flash、已核高峰token预算4.227072元<5，未知/额外请求停，无默认回退。Native Key/真实Key不进脚本/环境/捕获；App自身仅按现有脱敏日志机制写新root日志，Owner不读取日志正文。

### 真实网络路线更正与最终启动 Gate

当前DNS的198.18.22.10处于benchmarking网段，不能称官方公网IP；只读route显示utun4，系统HTTP/HTTPS代理是既有StashTunnel的127.0.0.1:7890。无秘密CONNECT+TLS校验api.deepseek.com已成功；未发模型HTTP请求。应用改为显式使用既有loopback代理和NO_PROXY loopback，不改系统设置，不宣称物理直连。profile删去198.18地址/DNS开放，loopback监听/连接拆分单独规则，并只允许现有7890代理通道。首次执行前须验证profile实际bind/connect/TLS可用。

新增Allowed File: /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/qa-01/APP_START_GATE_01.json

QA最终Gate JSON只绑定profile、launcher、mainPlan、已核package/AX等输入hash，不反向绑定包含该QA hash的release，以免循环依赖。Owner release绑定此Gate JSON；launcher执行前重新验Gate verdict与所有候选hash/源文件。旧QA HOLD回证和网络误标记录作为历史保留，不宣称旧方案通过。

App final gate补充Allowed File: /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/app-stage-01/package-preflight.json；此固定包前检副本供Gate绑定，避免之后聚合CHECK_RESULTS状态更新造成原证明覆盖。仅复用既有12705逐项核对，未重测或改包。

App01普通只读校准回证 Allowed File: /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_APP_POSTCHECK_01.json。原launcher首次2MiB sysctl缓冲超过本机kern.argmax=1MiB，系统以EINVAL(22)拒绝，未通过归属核对；原App/父端保持。只在原精确PID上改用本机只读ARGMAX大小获取白名单环境，复用同一NUL parser/typed PID/来源hash，不改原已执行launcher、不中止/重启App、不重写原拒绝事件；新回证与binding单独保存，独立QA复核后才能操作UI。

### 首次App前端就绪诊断：无真人Key阶段

当前新root credential metadata=0、无人输入Key、无模型请求；只允许对app-root-01/logs/frontend.log和frontend.err.log做固定错误类别/计数统计，不输出或保存日志正文，不读取workspace日志、旧日志/默认资料。必要时仅报告当前bundle/task生成物的缺失文件名，绝不扫真实凭据。原父端/进程和失败回证保持，普通启动异常由Owner协调，不自动重启。

### 同一无Key进程的启动栈分类

允许只读sample既有77098一秒，仅保留固定栈分类布尔值到app-stage-01/startup-stack-classification.json；不保存/输出原始栈、不读内存内容、无调试注入/新权限，失败不提权。无真人Key、无付费调用。

### 一次普通AX前台激活

Owner允许在Main/QA独立审查后，使用app-stage-01/activate-frontmost-once.py对当前既有77098做一次AXApplication AXFrontmost=true；写入前后核内核PID/UID/start/path/hash，先核属性可写。仅同一既有App，不launch、不open、不换浏览器/CUA、不触碰输入内容或模型请求。结果activate-frontmost-result-01.json存在即拒绝再执行。失败停留，不为此扩建通用工具。

### 真人连接后非秘密核验与单窗观察

CEO确认已填Key并点击一次，要求Owner自行查看。恢复既有过滤密码子树的非秘密AX与本地metadata GET，不重发save/discover。只允许既有固定controller对同77098/15139截取一次窗口，输出 /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/QA_LOCAL_USE_CLOSURE_20261018/install-02/rc9/owner-install/screenshots/deepseek-post-connect-20261025-01.png；该既有700目录兼容现有工具白名单，作为本Task新证据，不覆盖历史。输入阶段已结束；HTML密码框固定type=password无显示控件，截图不读取密码值；禁止全屏/其他App/权限升级。截图仅用来判定AX是否遗漏选模组件，不扩大测试工具。Main/QA仅静态查当前组件及实际包chunk，不改业务canonical或打包，真实生成仍未放行。

### 精确前端修复正式授权（覆盖此前只读限制，仅两文件）

独立QA PASS_FOR_EXACT_CANONICAL_GRANT_ONLY 后，Owner按OWNER_UI_FIX_RELEASE_01.json授权主开发修改 /Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ModelManagement.js（8cbe前像→7f7f后像，ce632私有patch）及 /Users/yy/Documents/Curis AI Workspace/frontend/tests/modelCredentialRecovery.test.mjs（98dcea前像；只扩现有回归框架）。精确前像已保留于本Task/preimages，新增SOURCE_DELTA_01.json记录。Allowed Directories仍本Task/既有preimages/developer-01/qa-01；业务源码只允许这两个exact files，不扩大目录写。Developer直接与QA在本批普通测试问题收口；包/签名/安装/运行版本切换、真实生成均未放行。原Source67/RC9接受不改写。

### 一次精确私有前端包执行授权

QA静审通过后，Owner按OWNER_FRONTEND_PACKAGE_RELEASE_01.json放行唯一已审FRONTEND_ONLY_BUILD_01.py（6e685d）+SPEC（4d30bf）在 /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/frontend-package-01 内私有构建/封装/adhoc签名/回证；目录由脚本按one-use门创建。允许该目录内frontend/home/tmp/build.sb/BUILD_INPUTS.json/build.log/Curis.app/sign.log/MATCHED_PACKAGE_MANIFEST.json及编译产生的内部文件。旧已安装App、PID77098/所有liveRoot、旧donor、任何凭据/Provider/Git/依赖安装均禁止修改或执行；不launch/quit/install。失败保留现场，原输出不可覆写；Owner同批处置普通构建失败，不需CEO小问题介入。下一Gate为实际包独立QA及另行安装/原生身份放行。

### 私有包同批链接修正02正式放行

01在kind=link安全拒绝、Next未启动；原输出/脚本/Spec/Release保留，01静审PASS已撤回。旧02 hash4272/cbeadb从未放行，因预检拒绝未生成release。QA复审末版d76a44脚本/3580e4 Spec（相对link文本pin/词法界限/全树resolve containment及unknown-kind拒绝；fixture通过）后，Owner实际写入并查验OWNER_FRONTEND_PACKAGE_RELEASE_02.json，唯一OUT /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/frontend-package-02；同边界一次私有构建，不动安装/live77098/Root/Provider，失败保留不自动重试。

### 私有包同批构建环境修正03

02源/依赖已复制核对，Node入口因精确OUT祖先的metadata lstat被沙箱拒绝，Next compiler尚未开始，输出保留。QA对a18d8d脚本/e4fc6e Spec及独立合成沙箱实测通过：仅精确祖先metadata可读、祖先data/xattr仍拒绝、其他用户目录内容/网络/OUT外写仍拒绝。Owner按OWNER_FRONTEND_PACKAGE_RELEASE_03.json一次放行OUT /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/frontend-package-03，不扩大任何实际App/资料/凭据权限；01/02原样保留。

### 私有包同批冻结素材修正04

03进入Next webpack后报三个BusinessCatalogSurface外部PNG引用缺失，未封装/签包；原输出保留。QA核closure.externalAssets精确三素材的路径/字节/SHA及原import到staged映射通过。Owner按OWNER_FRONTEND_PACKAGE_RELEASE_04.json一次放行0615a9脚本/5d36a8 Spec、OUT /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/frontend-package-04；只增加精确三冻结素材复制及路径/哈希护栏，不改任何业务源或live权限，01–03保留。

### 私有包05及普通构建问题同批直收口

04在执行前因rewrite参数遗漏/:path*被HOLD，未创建OUT04；Release04保留为unused，现撤销执行并由OWNER_FRONTEND_PACKAGE_RELEASE_05.json替代。QA通过86bdba脚本/8dd560 Spec，Owner放行OUT /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/frontend-package-05。为执行CEO提速职责，Developer可在同一05脚本/Spec内修普通构建问题；独立QA可在保留旧字节和独立定向复审后，只重pin此Release05的脚本/Spec SHA及该精确OUT根内新attempt子目录，记入现有QA结果，不再逐次经Owner普通脚本中转。不新建平行Authority/Backlog，固定代码delta/输入闭包/无网络/无敏感读取/OUT外写禁止/复用旧后台/无install-live-Provider等边界不得改变。失败输出保留不覆写，最终固定包仍须独立QA+Owner实际App Gate；权限、真实数据、费用或边界变化仍由Owner处理。

### 新签包既有AX工具最小校准（仅静态/编译）

实际私有包05已产生Native签名后SHA97fc66071f1a44ec918287229597a99b36dd649922c66f66e208d0819c1b1b8b。Owner授权Developer在 /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01 复制既有pid_native_control.swift（前像af15fa179579918e95165c391b852a3af419530775bb6aca8b7d0781306a2e6b）与pid_native_focus.swift（ccf1ffddca71fd26b926ecfb182d5c4d743bd0bb8b55a76a0d886979a4745ba8），仅将productSHA的1fa旧literal替换为97fc新literal，禁止其他变化。可在此精确目录创建编译cache/tmp、编译两二进制与pure --self-check/回证CALIBRATION_CHECKS.json；不修改旧工具或源、不得实际绑定/AX/截图/App操作。独立QA核diff/原护栏/pure结果后另行实际AppGate。App安装/启动/退出与coldstart的未执行脚本仅允许准备在既有developer-01，不赋予执行。

### 固定可运行依赖闭包候选与最终工具校准目标

首05包97fc因runtime依赖不完整已撤回package PASS、禁止安装。现唯一固定候选为frontend-package-05/attempt-02/Curis.app，manifest573817ee、QA回证872fe34f，BUILD_ID eoeyeTGJ7VptrzXy8ReME、Native962efb033d77362543a3ae6e6a44b11b6b9240fac1de828042c4190c86b22533，实际包6803members及隔离require测试通过，尚未安装/启动。此前native-ui-fix-01 hash-only校准授权目标由97fc替换为此最终962ef，仍只原1fa productSHA literal→962ef、其余source/guard/路径不改、纯编译与self-check，禁止实际bind/GUI。Main仅准备安装/同根cold脚本，实际Owner退出/安装/启动还需精确Gate。

### Owner当前测试App正常退出授权

固定依赖闭包包已过独立QA，Owner放行仅对原binding ccdc2bae/PID77098/start1792920322.243647/path /Applications/Curis.app/Native1fa 的正常quit请求；旧parent56562必须保留等待，不能强杀。遇未保存/系统提示保留现场，不丢弃。执行后由Owner查旧Native/PGID77098侧car/三端口/父端正常结果，记录OWNER_OLD_APP_POSTQUIT_01.json；当前仅退出，不赋予安装或新启动权限。业务root app-root-01保留、默认资料禁止读取和写入。

### Owner精确安装固定候选（仅应用代码）

旧77098已正常exit0，父端56562正常结束，进程组和三端口无遗留；原退出回证SHA233cead3。Owner经QA准备回证7ed99a97后按OWNER_MODEL_UI_INSTALL_RELEASE_01.json放行唯一7417076安装脚本，候选573817包复制到native-ui-fix-01/Curis-model-ui-stage.app核6803清单/签名，原/Applications/Curis.app完整重命名保留于native-ui-fix-01/Curis-RC9-before-model-ui.app，同文件系统再将stage置为唯一/Applications/Curis.app。这三个exact app directories列入Allowed Directories；候选/旧donor保留，无删除；失败按原脚本保全/恢复。仅Owner执行，禁止启动或任何默认/测试DB及Key/Provider操作，新启动仍另Gate。

### Owner同根新签版一次启动

安装已实际完成，Owner退出/安装回证与独立QA2286382a确认新6803/旧12705精确清单及签名、新旧App/候选均保留、无运行。Owner按OWNER_MODEL_UI_COLD_RELEASE_01.json放行31809c冷启动脚本，Popen前完整installed manifest573817重核、private app-root-01原device/inode、profile93345/Native962ef/校准tools137cc5及2119bf pin、安全env/实际kern.argmax及新PID/PGID/三port后验。原本机Stash代理/官方TLS界限沿用，保留parent直至正常退出。仅启动同根App并核metadata；不重输Key、不调用Provider、不放UI动作至新binding独立核验，默认资料继续禁止读取/写入。

### Owner新绑定实际UI与无生成的完整前置旅程

独立新PID/root gate806e80通过，binding03f3f3/PID1895/Native962ef。Owner按OWNER_MODEL_UI_NATIVE_RELEASE_01.json放行同固定包的非秘密观察/普通前台/模型页合法已保存Flash选择和实际UI设默认；公司必须唯一C7140航灯模型验证室且同Root。可连续完成通用业务/工作空间正常表单、现有真实员工招募、单一主责任团队接线和创建短Work A，不可点执行。默认模型必须deepseek-flash实际key7d963且server readback，不能重发connect/recover/Key操作。真实模型另发Work绑定限额release，总预算5不变。默认资料库/无关进程/系统新权限仍禁。

### 当前固定版已保存凭据显式复验（第二/最后模型列表GET）

Owner已实际UI选Flash并设默认，UI及metadata读回正确。QA83d6ca确认空密码saved-ref connect不新建/改写Key、仅App服务端按provider resolve后一次官方/models GET，save:true会更新本隔离root模型metadata或将消失项inactive。Owner按OWNER_SAVED_REF_REVALIDATION_RELEASE_01.json放行1895/03f3f3的一次显式按钮，计入本Task第二且最后/models GET；原真人一次属第一。不是不明保存重试，无新Key输入/值读取/新凭据写，失败超时无自动重试；仍无generation授权。此后冷启模型页无自动recover，不再点测试。

### 固定版模型设置实际成功回证截图

同1895/962ef已实际用已保存凭据显式复验一次成功，显示连接成功且selector/default保留Flash，元数据凭据仍1。允许既有controller对当前自有window15237截取一次 /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/QA_LOCAL_USE_CLOSURE_20261018/install-02/rc9/owner-install/screenshots/deepseek-fixed-success-20261025-01.png（复用已审白名单、不覆盖历史）；新会话未输入Key且密码框为空/固定password类型，禁止其他窗口或完整屏幕。之后进入已授权无生成业务前置。

## Owner bounded Work A → cold reopen preparation — 2026-10-25

Authority Class: EVIDENCE / OWNER IMPLEMENTATION SCOPE
Status: Review
Disposition: REVIEW_REQUIRED

Preparation only. Main may adapt the already accepted one-use cold launcher to reopen the same installed 962efb033d77362543a3ae6e6a44b11b6b9240fac1de828042c4190c86b22533 package, same app-root-01, after actual Work A acceptance and normal exit of PID 1895. No execution until Owner release plus independent QA. Preserve every original launcher/receipt; same environment/profile/privacy/identity/package guards; fail closed on unknown exit, occupied ports, reused receipt, changed package, changed root or invalid fingerprints. No source/business/permission/network expansion, no live calls, no App operation by Main/QA. Exact new files:

- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/LAUNCH_MODEL_UI_WORK_REOPEN_02.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/WORK_REOPEN_SPEC_02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/work-a-normal-exit.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/work-reopen-started-02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/work-reopen-result-02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/work-reopen-binding-02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_WORK_REOPEN_RELEASE_02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_NAVIGATION_METADATA_RECONCILIATION_01.json`

Metadata navigation scope reconciliation is pending independent QA; current page writes and generation paused. The earlier explicit two /models checks are known; SharedConversation mount recovery can add another metadata GET. Do not keep claiming total exactly two, do not replay tests or hide this discrepancy. CEO total generation validation ceiling remains CNY 5.

### Navigation metadata reconciliation accepted by Owner + independent QA

Current model-setting/default/saved-reference actual App branch passed independent QA; employee generation remains pending. See `OWNER_NAVIGATION_METADATA_RECONCILIATION_01.json`: known explicit discovery GETs 2; current Shared mount 0/1 physical unobserved; future four necessary page entries allow up to eight logical metadata recoveries, no new credentials or generations. This corrects an Owner planning omission rather than relabelling extra requests as absent. User CNY5 total ceiling and two strict single-use Work executions unchanged. Ordinary UI preconditions may continue under exact current binding/root; errors/unknown outcomes stop without retry.

## Ordinary P1 actual team projection repair — Owner exact grant

Status: Review
Authority Class: EVIDENCE / OWNER IMPLEMENTATION SCOPE
Disposition: REVIEW_REQUIRED

Owner actual one-time team assignment is retained. Independent source and real readback locate valid company-scope employee/role responsibility omitted by the Shared projection; one enabled tenant-private Flash Employee binding is present. Main may change only the following canonical source/test files, within their existing parent directories and this Task Workspace; all other canonical files remain read-only. Exact gates and original hashes: `OWNER_TEAM_PROJECTION_FIX_RELEASE_01.json`. No App/live Root/Provider/Git operation; no identity movement, reassign/recruit or DB mutation workaround; package build/installation separate Gate.

- `/Users/yy/Documents/Curis AI Workspace/backend/app/shared_workspace_projection.py`
- `/Users/yy/Documents/Curis AI Workspace/backend/tests/test_v1_general_workspace_p1_operating_closure.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/preimages/shared-workspace-projection-before-fix-02.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/preimages/general-operating-tests-before-fix-02.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_TEAM_PROJECTION_FIX_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/SOURCE_DELTA_02.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/GENERAL_TEAM_PROJECTION_CANDIDATE_01.patch`

Targeted offline fixture outputs only under `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/general-team-projection-test-01`; Main/QA may refine ordinary private harness/profile and rerun affected tests there under network/Keychain/env/protected/live-root denial.

### Same-batch fixed package recipe preparation (not build execution)

Main may prepare the following exact private script/spec only, while source tests/QA proceed. Base is immutable frontend-package-05/attempt-02/Curis.app, full manifest 573817eebbffa4b4d4ed45e202dfc0b8458e8ad9a5fe9132fba83abbfcca7d1a. Plan one mapped backend.app.shared_workspace_projection PYZ replacement from authorized source delta, preserve every other module/resource and accepted fixed frontend, no dependency download or broad dirty-tree rebuild. Recipe must prove old/new code mapping, all non-target module bytes, archive structure and code signatures; offline profile denies network/Keychain/.env/default/protected/live roots. No candidate output creation/build until separate Owner release + independent source/recipe QA.

- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/BUILD_TEAM_PROJECTION_PACKAGE_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/TEAM_PROJECTION_PACKAGE_SPEC_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_TEAM_PROJECTION_PACKAGE_RELEASE_01.json`


### Owner source candidate freeze — P1 projection

SOURCE COMPLETE / QA PASSED only: `SOURCE_DELTA_02.json` SHA `0812a602062587806f2a3a0cbedc849654ea13c059d1994220e570cd3a562e72`, source `7958f6d4a01e7633574f50e750ae21d0d98d4b90c870e0579640cc8776a2102f`, test `606624ee7dffc2ab2bb6dd68ff9cbacfd7a3a1154579f887de215652ec6b76cb`; exact preimages preserved, independent 30/30 regression and diff check passed (QA `1c0872d24f3988989fc3b3d49da71cc87b816077b6e147cc1ef0717ff3a47a5d`). Fixed source is now frozen for package preparation. No more source edits while packaging without explicit recorded withdrawal/affected re-QA. PACKAGE READY / NATIVE ACCEPTED / Work-Result acceptance remain false. Main proceeds to existing exact private package script/spec; build remains separate Gate. Current live PID1895 is old projection and retained.

## Current metadata lifecycle scope — supersedes page-count plan prospectively

Status: Review
Authority Class: EVIDENCE / OWNER EXISTING JOURNEY SCOPE CLARIFICATION
Disposition: REVIEW_REQUIRED

Independent QA confirmed General refresh switches loading/ready and can remount SharedConversation after assignment, Work creation or execution, in addition to page entry. Therefore the old page-only 0/1 and 8-logical plans are historical and cannot be used as physical /models counts. Known explicit discovery requests=2; all automatic physical metadata counts=UNKNOWN. No generated-content request has occurred. This records the additional planning omission without retroactively claiming it was absent or exactly authorized by the original count plan.

Owner now explicitly includes metadata recoveries inherently caused by this exact normal UI journey: retained assigned team → fixed projection package normal reopening → Work A create/strict single execute/result/usage → normal exit/cold reopen → new Work B create/strict single execute/result/usage. Existing same-selfuse DeepSeek saved-ref internal resolve → official https://api.deepseek.com/models only → isolated app-root-01 model metadata/audit refresh is allowed; no new Key store/update or Owner secret access. No manual test/connect/recover/reload/retry, additional pages or abnormal remount loops. Unexpected loop, endpoint/identity drift, metadata failure/unknown outcome, or generation outside the two exact Work gates stops the affected action. Free-of-generated-tokens metadata is not converted into extra generation permission or a new CEO gate per request. Exact physical count remains UNKNOWN unless non-secret evidence proves it.

Human hard ceiling stays CNY5. Work A/B generation remain separately released, each physical once, full prompt4096 bytes/max_tokens2048, no tools/search/fetch; official Chinese peak-price conservative total CNY4.227072. Metadata has no generated tokens; no separately listed /models fee on checked official pricing is an inference, not a verified account bill. All prior releases/QA/evidence are retained, not rewritten as preauthorized.

## Private module-only package build released — same batch

Status: Review
Authority Class: EVIDENCE / OWNER IMPLEMENTATION SCOPE
Disposition: REVIEW_REQUIRED

`OWNER_TEAM_PROJECTION_PACKAGE_RELEASE_01.json` authorizes Main to build into exact `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/backend-projection-package-01` and unique attempt descendants. Source/delta/QA/base/target hashes fixed; only workspace carrier plus Native signature and CodeResources may change; all non-target module/resource bytes and Native/bootloader program semantics remain equal. No App launch/install/live Root/Provider/Git/dependency download. Ordinary bounded recipe/script/sign/profile issues are delegated to Main+QA: retain prior bytes/hashes and all failed outputs, QA alone independently repins matching script/spec/release before a unique new attempt; do not weaken guards, mutate source, broaden inputs or reuse consumed attempt. Final candidate and independent package QA return to Owner; install/start separate Gate. Old ea026/81eb preparation pins were rejected before writes when final TOCTOU guard revisions appeared; final QA-reviewed9c6f0a/ee66fb pins used, no old attempt was executed.

## Projection candidate install/reopen minimal preparation — not live release

Main may adapt only the existing accepted INSTALL_MODEL_UI_01 / LAUNCH_MODEL_UI_COLD_01 guard logic to the forthcoming independently accepted module-only package: same /Applications/Curis.app, same app-root-01/dev/inode/company/workspace/employee, old current PID1895/start1792934494.927628/native962ef/parent32515 must normally exit before install/reopen. Preserve old bundle to exact N/Curis-model-ui-before-team-projection.app; exact stage N/Curis-projection-stage.app; no deletion/overwrite. Source scripts may read final Owner package release pins instead of unfilled hashes and must refuse missing/invalid release. No build/install/quit/start during preparation. Calibration script may prepare copying existing N Swift helpers with exactly one productSHA literal replaced from Owner-final-package Native, compile to listed distinct paths, unchanged identity/privacy/AX guards and existing pure checks; calibration actual run separate Owner release. No new Native functionality, permissions, or tools. Same private profile/environment/package/identity/root/ports/one-use/parent-wait safeguards; script must explicitly distinguish App page lifecycle metadata recoveries from script explicit Provider calls. Existing Work-reopen-02 remains unexecuted and will need final package pins before Work A cold-B phase, not this pre-Work P1 reopen.

Exact preparation and future output paths:

- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/INSTALL_TEAM_PROJECTION_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/LAUNCH_TEAM_PROJECTION_COLD_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/TEAM_PROJECTION_NATIVE_SPEC_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/CALIBRATE_TEAM_PROJECTION_TOOLS_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_TEAM_PROJECTION_NATIVE_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_TEAM_PROJECTION_INSTALL_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_TEAM_PROJECTION_COLD_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-prior-normal-exit-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-install-started-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-install-result-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-started-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-start-result-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-binding-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_control_projection.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_focus_projection.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_control_projection`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_focus_projection`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/PROJECTION_TOOL_CALIBRATION_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/Curis-projection-stage.app`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/Curis-model-ui-before-team-projection.app`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/projection-tool-cache-01`

Main/QA handle ordinary private script/spec issues together, output to existing Task Workspace; no live operations until Owner final package/identity Gate.

### Owner fixed candidate — projection-01 PACKAGE READY

Source7958f6/test606624 and base573817 retained. `backend-projection-package-01/Curis.app` manifest `489bea7f8aa55e1e0de6be9b3a9c312c1c37971215f6ea60fdec1f8f27f8b30d`, Native `480888104845d763d4a1e97ad02788850d2fec299f5c4c3bd1ea79934b08980a`, workspace `797dd0bbe5802bb44a27747124ed2ce68d04200ebb6283aad35a50c9ba6f9ed2`, module delta d6003fcd5648… fixed. Independent actual package QA6e71eec6… passes6803 inventory, deep strict signatures, 1399 unchanged modules/one target, unchanged bootloader/Native program semantics. Owner freezes candidate for next Native stage. NATIVE ACCEPTED / real Work-Result acceptance still false; current installed/live1895 remains962ef old projection. Main may finish already-authorized minimal installation/calibration/cold preparation against this exact candidate; no source/package edits or live operations before Owner stage release.

### Owner exact current test App normal exit before fixed-package install

Owner permits exactly one normal quit through already-bound N control for PID1895, /Applications/Curis.app/Contents/MacOS/curis-desktop, kernel start1792934494.927628, Native962efb033d77362543a3ae6e6a44b11b6b9240fac1de828042c4190c86b22533, parent retained exec session32515, private app-root-01 and company航灯模型验证室/current workspace-first-6330d90a7a1b374e0dfbe3ef. Preserve assigned team and zero Work state; no force signal, other App, user-data movement or install until exit/ports/parent evidence. Write exact N/projection-prior-normal-exit-01.json after observation, not beforehand. Candidate489bea/Native480888 is separately fixed/QA; actual replacement/start remains future precise installer/launcher Gate.

## Prepare existing Work A-to-B reopen for final fixed version

Owner permits Main/QA to update only existing developer-01/LAUNCH_MODEL_UI_WORK_REOPEN_02.py and WORK_REOPEN_SPEC_02.json pins/paths/old-parent binding to fixed projection package489bea/Native480888, currently running Native PID13298/kernel1792939846.791690, parent exec88658, binding N/projection-binding-01.json SHA9fe51b511e5bda4d40ce474a8ec6dbbb03cf84e8613c4f73fb99ed697f45aeb2 and parent result N/projection-start-result-01.json. Preserve Work A actual Owner acceptance/ref + normal exit/new parent final0 + package/root/environment/ports/one-use safety and same outputs work-reopen-*-02. Owner preimages stored exact preimages/work-reopen-launcher-before-projection-02.py and work-reopen-spec-before-projection-02.json. No execution until actual A acceptance and separate Owner release; no App/live Root/Provider/Git action by Main/QA; only AST/pure-fixture guards. New pure helpers c7ce/747c target480888 already compiled/QA, do not recompile them. Future UI/Work A/B release exact paths added TASK_START; no generation granted by preparation.


## P2 — General team employee display-name fallback

Status: Review  
Authority Class: REVIEW / EVIDENCE — bounded issue registration, not Product Authority  
Disposition: REVIEW_REQUIRED  
Owner: Delivery Owner; Main proposes the smallest render correction, independent QA verifies the affected display after a separate exact implementation grant.

Owner actual readback reports final Native480888/PID13298 team READY_FOR_WORK, employee0b4a454d-1bf2-461c-b1f2-54fd4a46cd20 identity VERIFIED_EXPLICIT_BRIDGE, correct role holder and retained enabled binding; no reassignment. General API `employee.name` and the team UI show `未命名员工`, while the attached `organization_record.name` is `经营方法专家`. This is an ordinary P2 display issue; these observations are Owner-reported, not a Main live read or Work/Result acceptance.

Read-only source finding: `backend/app/shared_workspace_projection.py` `_employee()` uses `data.get("name") or "未命名员工"` (line543); `workspace()` attaches the company/tenant-scoped organization record by the employee's `company_employee_ref` afterward (lines109–116), without changing the display name. `frontend/components/v1/GeneralWorkspaceOperating.js` business-team row renders `item.name` in both linked/plain labels (line400). A truthy placeholder therefore bypasses a simple `item.name || organization_record.name` fallback.

Minimal proposed render correction, not authorized implementation: confine the change to the General business-team name label. Preserve a nonempty real projected name; when it is empty/whitespace or exactly the known placeholder `未命名员工`, use a nonempty attached organization name only for the existing verified employee bridge/organization identity; otherwise retain the existing unnamed display. Apply the same derived label to the linked and plain text. Keep employee refs, conversation URL, role/responsibility, readiness, assignment, API payload, persisted identity, model selection and execution unchanged. No organization fetch, API call, DB rename, reassignment or role-name substitution is needed.

Decision / Next Action: keep current source7958/test606624/package489bea/Native480888 frozen and finish the same-version real Work A/B core validation first. Do not start a separate source/package cycle or create a new report for this P2 now. If a genuine generation-chain P1 appears, Owner may explicitly include this display fix in that bounded repair; otherwise close P2 afterward under an exact frontend-file grant. This note does not grant source edits or package replacement.

Target / Next Gate: existing General team rendering only, after the core model-validation gate. Acceptance should cover real-name preservation, verified organization-name fallback, missing/unverified-name fallback, and the displayed label/conversation link in the affected UI. Recheck affected rendering and ordinary package integrity if packaging becomes necessary; do not repeat unaffected model-core generation validation solely for this display field. Work-reopen02 preparation remains independently passed (QA ca59a5d5…); no further edits or live polling are required by this P2.

### P2 bounded merge preparation — no implementation

Future proposed exact source/test targets, pending Owner grant: `frontend/components/v1/GeneralWorkspaceOperating.js` and existing `frontend/tests/d1WorkStatus.test.mjs` (its mocked General render harness already exists). Keep the name decision local to the team label; do not add a shared name system, a backend projection change, another fetch or a new test/report file. Reuse the existing bridge checks already expressed in `frontend/lib/d1Api.js`: verified employee identity, bridge status VERIFIED, bridge companyEmployeeRef equal to the nonempty company_employee_ref, and verified organization_record identity. Only then may an empty/known-placeholder projected name fall back to a nonempty attached organization name. A real projected name remains unchanged. This records a proposal only; none of these source/test files is edited by this preparation.

Affected-scope verification after authorization: render the General team with a real projected name, with the verified organization fallback, with missing/blank organization data, and with mismatched/unverified bridge data. Check the displayed name and unchanged conversation href/employee refs; ensure the display calculation makes no API or execution calls. Use the existing mocked render harness; do not invoke model recovery or Provider generation as a display test. If a root-cause-confirmed blocking fix requires a package, Owner may merge this P2 into that exact source/package batch and repin/review only its affected inputs; the present UNKNOWN does not itself authorize a source fix or rebuild. If the blocker clears without code change, keep the fixed package for A/B and schedule this P2 after core validation.

## Cold automatic model recovery unavailable — minimal readonly diagnosis

Actual fixed13298 General team/bridge is READY with existing E, but Shared model selector settled unavailable. No Work created/generated; original failed action is stopped, no manual recover/test retry. Saved preference/active models remain, so failure stage is UNKNOWN; ad-hoc workspace carrier DR changed (1052→797d) is a Keychain hypothesis only, not proof.

Owner permits one normal authenticated GET /api/platform/audit read under existing selfuse/selfuse-ceo headers only, tenant selfuse and narrow since2026-10-25T14:40:00Z, exact event_type credential.resolve_failed/resolved, limit5 per type. If current identity is denied403, stop; never add platform-admin identity/header/token or widen tenant. Filter only event timestamp/type/result and known failure category/OSStatus numeric; no raw payload/ref/key/user data/log/DB output. No credential resolution, Provider request, credential write, system permission or generation by this readonly query. If audit cannot provide evidence, separate Owner exact App-internal nonsecret credential-test diagnostic may be considered after source/QA (not currently granted by this section).

### One exact App-internal credential test released

See OWNER_COLD_RECOVERY_DIAGNOSTIC_01.json: current Root tenant has one active DeepSeek macOS Keychain credential. One credential-test POST through existing normal workspace API only; App reads its saved item, Owner receives boolean/known error/OSStatus only, no secret/ref/payload. No Provider HTTP, credential mutation, retries or system authorization changes. AX/screenshots paused during potential secure UI. Source admin audit is unavailable without separate token; no token lookup or elevation. Keychain ACL/CDhash remains hypothesis until evidence.


### Exact credential diagnostic outcome — UNKNOWN, no retry

Owner's existing `native-ui-fix-01/cold-credential-test-result-01.json` SHA `803a96ba52b517643ac1c8d2b7eb20ba9e4a5148a914283cb8ad067996cfe662` records PID13298, attempts1, errorType TimeoutError, outcome UNKNOWN_TIMEOUT_OR_LOCAL_TRANSPORT, providerHttpRequests0, generationRequests0, ownerReceivedSecret false and retryAllowed false. Owner reports a 20-second wait with no HTTP response and zero Work. Main read only the named receipt's nonsecret fields; no App/native/credential/API probe was performed. A client timeout does not prove the server-side operation has ended or establish ACL, Keychain, network, transport or UI root cause. Do not append another native read, credential test or recover request. Source/candidate remain frozen; parent88658/13298 are not operated by Main. AX/screenshots remain paused per Owner; any possible system Keychain prompt is for Owner to ask the human about in text, not to inspect foreign secure UI. Owner's separate ordinary health/preference observations may narrow service reachability, but neither success nor failure alone identifies the pending credential-read cause. Platform audit was unavailable through the ordinary route and requires a separate admin token in source; no token lookup or escalation is authorized.

## Resume bounded manual Work creation after human confirmation

Status: Review
Authority Class: EVIDENCE / OWNER EXISTING JOURNEY RESUME
Disposition: REVIEW_REQUIRED

CEO replied “已确认” to the secure-system-prompt observation question. No broad permission or exact ACL operation is inferred. Independently observed saved DeepSeek models refreshed from13:54:22 to15:40:44, same13298/kernel/path/hash/Root/default Flash. Own-App bound AX read resumed; team still READY, Shared selected-model state remains unavailable/cached, blank manual form. Original credential test20s UNKNOWN retained, no test/recover replay or foreign secure UI/permission operation. Existing General UI explicitly allowWithoutModel creates Work from manual fields and ignores conversation model; this creation does not generate. Owner resumes only ordinary focus/fill/one Work A creation under c3f5 UI release, then actual refs/bindings/strict-cap QA before generation. Normal UI lifecycle metadata rule remains; sensitive input/focus guard refusal stops, no forced activation of secure UI.

### Work A actual generation released

Exact OWNER_WORK_A_RELEASE_01.json pins current13298/480888/C/W/E/WorkA/defaultFlash and independent QA admission of38419faa preflight. Strict UI checkbox observed1, actual execution/Usage/Result all0 before release. Owner may press this Work Start once, backend4096bytes/2048tokens/max_executions1 and immutable physical claim; no second API or retry. Total2 generations/<=5CNY unchanged. Actual result/body/usage still nextGate, not acceptance from click.

## 2026-10-26 Work A single-attempt integrated failure

Actual WorkA efbc0f/Task ab55d19f failed after exactly one normal UI Start; no retry. Safe Task error is exactly static “Complete prompt exceeds the approved byte limit” (47 chars); final prompt metric5297 UTF8 bytes vs approved4096, content2077, private prompt not shown/saved. Task executions/artifacts0, Usage rows0; failed Result contentnull/UNVERIFIED retained. Source guard is before outbound claim/executor, independent confirmation pending; emptyUsage alone never proves0calls. No caps increase, reset/clear held, new Work, credentials/recover, or source/package mutation. Main/QA may only inspect source and existing Task private fixtures to propose exact compact model prompt/source/test scope; originalA and its once-only marker remain. See existing native-ui-fix-01/work-a-attempt-result-01.json. Human confirmation and current Shared Flash-ready are separate from earlier credential-test timeout UNKNOWN.

## 2026-10-26 Combined minimal prompt duplication P1 + name display P2 source grant

Status: Review
Authority Class: EVIDENCE / OWNER IMPLEMENTATION SCOPE
Disposition: REVIEW_REQUIRED

OWNER_PROMPT_AND_DISPLAY_FIX_RELEASE_03.json grants exactly five canonical files below; Owner preserved every preimage. Remove only repeated Task Goal from context excerpt for limited General normal PromptBuilder, default compatibility true and persisted goal/first full task/role/skill/all constraints retained. No caps/identity/outbound/transport weakening or task replay. General verified-name fallback in team/current Work holder label only; references/URLs/meaning unchanged. Ordinary test fixes directly Main/QA in task-scoped offline fresh fixtures, no live Root/API/Key/Provider/App/Git. Five-file source + independent QA first; one combined candidate build separately gated.

- `/Users/yy/Documents/Curis AI Workspace/backend/app/context_service.py` — preSHA `94c03d63901f7deeccd4c6c523601ff5d171961d60088a4a971eac48a2490e31`
- `/Users/yy/Documents/Curis AI Workspace/backend/app/orchestrator.py` — preSHA `930898e79cc3abfa2eb79c120f63cbc7ba65c843f050b7b4deb1c7fa1263db9f`
- `/Users/yy/Documents/Curis AI Workspace/backend/tests/test_general_single_attempt_limits.py` — preSHA `5b9d2f3eb087b9d118b5da19b9414ccb2845082eb55ac52f8478287b24597264`
- `/Users/yy/Documents/Curis AI Workspace/frontend/components/v1/GeneralWorkspaceOperating.js` — preSHA `f633c6a27608f3aec5f3cfeb231352f63fa443bdca2a2417aa869ab64b1deae2`
- `/Users/yy/Documents/Curis AI Workspace/frontend/tests/d1WorkStatus.test.mjs` — preSHA `cfefdf964bf773aaffcf5905bcc23a8135ac4b47262bcf6acf6c744ba41a6813`

Exact test directory `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/limited-prompt-test-01`; SOURCE_DELTA_03.json and existing Task output manifests preserve results. Original A held forever/no retry; no new actual Work before corrected candidate and fresh budget Gate.

### Combined final package recipe preparation only

Main may prepare exactly developer-01/BUILD_PROMPT_DISPLAY_PACKAGE_01.py and PROMPT_DISPLAY_PACKAGE_SPEC_01.json, future OWNER_PROMPT_DISPLAY_PACKAGE_RELEASE_01.json. No build/output directory creation before fixed SOURCE_DELTA_03 and independent source/recipe QA. Proposed output prompt-display-package-01 under existing Task, immutable base backend-projection-package-01/Curis.app manifest489bea. Reuse accepted frontend-package-05/attempt-02 frozen481-source/closed dependency recipe, preserving ModelManagement7f fix and applying only final GeneralWorkspace/d1-test authorized deltas; no dirty-tree source/dependency scan/download. Only two accepted Python module replacements context_service+orchestrator; all other1398 original PYZ compressed payloads unchanged,12CArchive onlyPYZ changes, original shared projection7958 preserved. Frontend changes limited frozen rebuild subtree, target backend carrier, Native signature/CodeResources; program fingerprint and code signatures/full inventory checked. All profile no-network/no-Keychain/no-env/no-default/protected/liveR conditions retained. Ordinary private recipe bugs Main/QA coordinate without Owner per-error; execution still separate stage Gate.

### Combined final candidate Native minimal adaptation preparation only

After five-file source freeze and combined private package, Main may prepare below exact scripts/spec by reusing accepted projection-stage guards; pins/paths/old binding change only. Former current App13298/start1792939846.791690/Native480888/parent88658/children13494,13497,13514/sameR+C+W+E, failed original A/Task/hold retained. No WorkA acceptance prerequisite for this ordinary pre-acceptance repair reopen; new successful Work and later same-package cold reuse remain separate. Tool calibration exactly one productSHA literal per existing projection helper, unchanged66/62 pure guard tests and no new UI functionality/permission. New receipts/backup/stage must be unique; old outputs immutable. No actual compile/quit/install/start/live/Key/Provider during prep; Owner phase release and independentQA required. Existing Work-reopen02 later repins to final actually started tuple before acceptance-work cold reuse, preserving full acceptance+normal exit guard.

- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/CALIBRATE_FINAL_TOOLS_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/INSTALL_FINAL_PACKAGE_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/LAUNCH_FINAL_COLD_01.py`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/developer-01/FINAL_NATIVE_SPEC_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_FINAL_TOOL_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_FINAL_INSTALL_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/OWNER_FINAL_COLD_RELEASE_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-prior-normal-exit-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-install-started-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-install-result-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-started-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-start-result-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-binding-01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/FINAL_TOOL_CALIBRATION_01.json`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_control_final.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_focus_final.swift`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_control_final`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/pid_native_focus_final`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/final-tool-cache-01`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/Curis-final-stage.app`
- `/Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEEPSEEK-CONNECTION-20261025/native-ui-fix-01/Curis-before-prompt-display.app`


### 10-26 Owner five-source freeze: SOURCE COMPLETE / QA PASSED only

Exact SOURCE_DELTA_03 f2d779ed3d16e2b168dedbdbe583d06c55fea8417e1981917a7a11c6752de984 and independentQA29f4f774600998b608bd9587bc0a08735826124794a739f3284d039523661b58 lock all5 pre/post images. Backend61/61 and frontend24/24 independent offline regression passed; full public fixture3214<=4096/fake1 outbound/output2048 and oversized5234 pretransport/0outbound prove checks retained. No real model result acceptance. Canonical source now frozen for the already-authorized single combined recipe; Main automatically continues BUILD_PROMPT_DISPLAY_PACKAGE_01.py/spec preparation, no further Owner/CEO confirmation required to prepare. No execution/output until exact package build stage. OriginalA failed/held immutable; Root13298/parent88658 retained.

### Single combined private package build released

Owner OWNER_PROMPT_DISPLAY_PACKAGE_RELEASE_01.json pins sourceDeltaf2d779/sourceQA29f4f7/recipeb47d63/specc7f90e/prepQA0d8d66/base489bea. Exact output prompt-display-package-01 and unique attempt descendants now approved; only frozen frontend subtree and ctx/orch two-module carrier, Native signatures/CodeResources can change. No live App/Root/Provider/Keychain/network/Git/dependency download. Main/QA jointly handle bounded ordinary recipe issues, preserve all prior bytes/hashes and failures, QA independently repins; no source/closure/identity/outbound/privacy/program-equality guard weakening. Do not wait for per-error Owner/CEO. Final independently verified complete candidate comes to Owner; Native stage remains separate.

### Combined candidate fixed; actual private package QA accepted only

Attempt03 manifest7e5545a64699ff67c8f63a70f4cac8d7ab9366cebec645047a139747af4610a8, Native81d17374661ec40b081022a14fd177f89985ff3b7d6d7ad8e59f96286fe18a9b, carrierc1e40122b40739b0167f73d3b1c3bbeffbd2108e4de96f81d5be03bccc735272, buildID-VC0J2HgxZ47vGzURscwA fixed. Independent actual QAe5418f verifies6803 members/724 bounded deltas/2target PYZ+1398 raw identical/closed frontend19 runtime+481sources/codesign/program fingerprints. Owner accepts PACKAGE_READY only. Ordinary Unicode literal and nested sandbox failures retained, repaired under the unchanged per-stage permissions with QA repin; no live/Provider generation. FINAL minimal preparation then separate actual gates; original failed A is not accepted.

### Final actual installation/cold identity accepted; normal UI model check pending

Installed actualQA59dbb2 and cold actualQA281915 passed: Native29655/kernel1792948071.404675/parent41178; original13298/88658/helpers normal0 preserved by exitcebd5db + QA6d917. Final helpers3163/60207 bound60983e, normal CEO→same business/workspace navigation observed company/workspace and corrected team/holder names. Shared mount automatic model check remains pending; ordinary model-preference GET200/17ms returns saved Flash. Cause UNKNOWN; no new credential test/recover or generation. Human asked only for system/Keychain prompt presence/text under existing CEO system authorization Gate; all AX/screenshot/generation/retry/restart paused, sessions retained. Main/QA final Work-reopen02 minimal offline preparation continues. See native-ui-fix-01/final-cold-model-state-01.json; original A remains failed/held, future actual prompt/Work/Result/Usage/cold second Work unaccepted.

### Human confirms Always Allow; resume normal saved-ref connection and real journey

CEO confirmed clicking Always Allow in the already-visible curis-workspace/com.curis.desktop.credentials.v1 system prompt and explicitly requested actual generation/Result/Usage then same-final-package cold continuity. Owner did not read OS password or control secure UI; original accidental Deny and all timeout history retained. Exact29655/81d173 kernel binding reverified. Shared UI currently stale unavailable; one normal model-page saved-ref connection refresh now authorized by current human continuation/retrigger request, no secret create/update/delete or new Provider/generation, no loop. Final Work1/2 generation still separately pinned and limited4096/2048, task<=2 and<=5CNY; original failedA never replayed.

### Delivery Owner bounded model task ACCEPTED

Independent final QA95f2e514 and Owner actual two normal native Result views accept saved-key DeepSeek Flash → two distinct General employee Works/Task/Result/Usage with exact same Native81/backendc1 and normal cold between. 3364/3214 prompt bytes; each one app-layer request/no fallback,1971 input+3601 output=5572 total (3135 reasoning included). Actual ledger fee unknown, official peak estimate0.03275CNY not a bill;<=5CNY admission retained. No key reentry/manual reconnect after cold. Original failedA and credential timeout UNKNOWN retained; default profile not touched/configured and other business/providers/full product not accepted. Final OWNER_FINAL_MODEL_ACCEPTANCE.json records precise decision/evidence. Installed P2 result tab bug OPEN, offline candidate only. No further model generation authorized under this completed task; automatically enter CEO specified full-App ux-interaction-audit and bounded implemented fixes after formal next-scope setup, preserving one existing board/three seats.
