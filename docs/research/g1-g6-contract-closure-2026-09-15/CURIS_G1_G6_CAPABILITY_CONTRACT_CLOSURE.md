# CURIS — G1–G6 CAPABILITY CONTRACT CLOSURE

Authority Class: RESEARCH
Status: Review
Disposition: PROPOSED CONTRACT CLOSURE — CEO REVIEW REQUIRED
Date: 2026-09-15 Asia/Shanghai
Owner: Product Research / Codex
Target Authority: CEO 接受后才进入 Blueprint Deep Reconciliation
Next Gate: CEO REVIEW

**Verdict: B. CLOSED WITH EXPLICIT IMPLEMENTATION VALIDATION。** 这里的 CLOSED 指六项缺口均已有明确、可验收的合同建议，不表示 CEO 已接受，不表示当前产品已实现或可发布。Current Blueprint、Authority、V2、Runtime 均未修改。

## 1. Search Method

按 Required Capability → Existing Curis Evidence → Targeted OSS Search → Candidate Comparison → Architecture Options → Product Decision → Contract Closure 执行。先写本目录 `REQUIRED_CAPABILITIES_AND_SEARCH_LOG.md`，再外查。上一轮三份研究文档是需求输入，不是 Current Authority。

证据：L2=源码静态核查；L3=官方 API/文档；项目自己的 README 描述标 DOCUMENTED；Issue 仅为报告者的证据，不自动等于维护者确认。架构选择均为本轮 RESEARCH DECISION。本轮无安装、无运行外部项目、无现场性能/兼容性验收。

|Gap|第一轮候选 / 深查上限|查询或直接定位及原因|停止依据|
|---|---|---|---|
|G1|Playwright / 官方 MCP / browser-use，3|session isolation / manual takeover / DOM screenshot；核对当前 README、BrowserContext、extension API|三种边界足够区分底层、桥接与自主 Agent；B/C|
|G2|LiteLLM / models.dev；OpenRouter 仅服务边界筛选|model capabilities fallback / schema；核对 Router、metadata、许可证与相关安全 Issue|协议与元数据不等于 Curis 用途系统；C|
|G3+G4|APScheduler / DBOS / Temporal，共用3|`site:docs.dbos.dev python sqlite durable workflow recover sleep resume`：本地持久性；`site:apscheduler.readthedocs.io userguide persistent job store misfire coalesce`：漏触发；`site:docs.temporal.io python activity idempotent retry human approval`：外部副作用|定时计算、嵌入式持久步骤、服务型工作流三类已足够；B/C|
|G3 平台|Apple 原生能力，不另算 OSS 引擎|`site:developer.apple.com launchd LaunchAgent background process sleep KeepAlive`：退出 UI、系统禁用和进程所有权|原生生命周期职责明确；A|
|G5|Docling / Tesseract / FFmpeg，3|直接已知项目的 converter / baseapi / license；只查解析、OCR、媒体；Shell/Git/Preview/Data 复用已有底层|不需要第四套 AI Workspace；A/C|
|G6|现有恢复工具 + SQLite/Python 标准库|直接 `Connection.backup` 官方文档及本地 recovery.py；恢复预检、凭证排除|库足够，缺口在产品清单和恢复规程；A/C|

首批四条 GitHub 查询误用了 `site.github.com/...`，结果混入无关材料；无关结果未采纳，随后转为官方仓库直接定位。没有用第三方排行榜、Star 数或广撒网补搜。MCP 元数据请求连接重置，README/LICENSE 重试成功；其 release/commit 仍 UNKNOWN，不冒充固定发布版。APScheduler 使用稳定 tag 3.11.3 源码，不能拿默认分支的新版本能力混算。FFmpeg 的 GitHub latest release 404 不等于停更，本文只固定源码快照，不声称 GitHub release 是官方发布渠道。

## 2. Existing Curis Evidence

|证据|Authority / 状态用途|本轮可复用结论与边界|
|---|---|---|
|`docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` Current Required Input|Frozen truth router|只承接现有 Company / Employee / Work / Result 模型；研究无权改其状态|
|上一轮 `full-app-completeness-2026-09-14/` 三份主报告|RESEARCH；缺口推导|C01–C48、77 项 Settings 是需求来源；“有产品表达”不等于能力存在|
|`backend/app/ai_capability_registry.py` `_profile` / `connect`|L2 implementation|已有连接与模型档案；能力真实性、发现完整性仍要验证；不另造 Model System|
|`backend/app/model_preferences.py` `TenantModelPreferenceResolver`；`employee_capability_model.py`|L2|复用 Employee 多用途/能力关系；无需一人一模型或第二套员工模型表|
|`backend/app/model_gateway.py`；`capability_adapters.py` `McpAdapter`|L2|已有调用与失败表达；MCP 当前窄工具调用不能冒充完整 discovery/schema/session/cancellation client|
|`backend/app/agent_adapter.py` `CodexCliAdapter`；`local_rd_toolset.py`|L2|已有 read-only/workspace-write 和会话恢复、有限研发工具；不等于完整电脑控制或 Shell|
|`backend/app/scheduler.py` 与 `runtime/scheduler.py`|L2|真实调度路径和默认模拟路径并存；不能概括成“全部模拟”，也不能用真实路径替模拟经营回路背书|
|`backend/app/runtime/workspace.py` `WorkspaceRuntime`；`task_execution_control.py` `TaskExecutionControlService`|L2|已有执行载体和控制、幂等入口；可扩展，不替换为外部项目的 Work|
|`desktop/src/lib.rs` 退出处理|L2|close/exit 会杀 sidecars，当前不满足 G3 的后台服务建议合同|
|`desktop/runtime/recovery.py` `backup` / `_read_archive` / `restore`|L2|SQLite backup、hash、integrity、格式校验、进程锁和恢复前副本已有；仅 DB 包，不是完整附件与账号重连体验|
|`CURIS_V1_CLOUD_AI_CONTINUITY_ACCEPTANCE.md`|Accepted implementation evidence|Keychain/真实调用/重启已有接受证据；不采用旧研究“凭证占位”结论|
|`CURIS_V1_EXECUTION_BACKLOG.md`|Implementation backlog|备份接受未闭合；源码存在不能提升为已验收|
|`docs/research/competitors/litellm.md`、`domain/model-gateway-research.md`|历史 RESEARCH|只沿用已知候选；旧 Admin-only、计价、架构和凭证说法不升级为 Current|
|`CURIS_TEAM_OPERATING_ENGINE_RESEARCH.md`、`CURIS_AUTONOMOUS_OPERATION_CODEX_RESEARCH.md`|RESEARCH|复用单一 Work Runtime/Decision/Result 的边界；“不引入工作流引擎”是比较输入，不是免比较指令|
|`domain/official-tool-catalog-v1.md` Playwright 条目|RESEARCH catalog|目录里有名字不等于安装、可调用、通过审批或登录隔离验收|

源码引用路径相对仓库根；完整绝对路径与 hash 见上轮 `evidence/source-manifest.json`，本轮复核见 `evidence/local-source-verification.json`。新增针对性代码文件见本轮证据索引。`backend/requirements.txt` 未登记本轮候选依赖；未以此推断整个电脑上没有这些软件。

## 3. G1 Browser

### PRODUCT CONTRACT

首版提供三种可区分能力：Search 返回链接、摘要、来源与时间；Reader 返回指定网页可读内容及引用；Interactive Browser 提供 DOM 定位/操作、截图、页面及 Console/Network 观察、上传下载、localhost 验证。Search 通过现有 Provider 路径接搜索服务；不将打开搜索页或 Reader 伪装成独立搜索索引。未配置搜索来源时明确 UNAVAILABLE。

登录上下文以 Company/授权账号为隔离边界，并归属于被授权 Work；员工可使用分配给其职责的会话，但不能因为同属 Company 就获得所有账号。默认 Curis 管理的专用可见浏览器 profile，用户在其中正常登录。同账号写操作串行占有；非持久 BrowserContext 可用于无账号临时任务。profile 不是 OS 沙箱，登录信息不能进入模型上下文、日志、Evidence 或备份包。

需要 MFA/CAPTCHA/敏感确认时进入 WAITING_FOR_USER：呈现目标页面、原因、任务与已完成步骤，停止自动点击；用户完成后重新核对账号/域名/目标，才继续。不能由“登录成功”推导出发布/购买授权。接管期间 Agent 不与用户竞争控制。浏览器关闭或掉线进入可重连/效果待核验，不盲目重放最后点击。

localhost 仅在已授权 Preview/Work 的地址和端口范围开放；普通远程网页不能任意探测本地服务。下载落在 Work 目录，登记文件、hash、来源；上传只用明确授权文件。Console/Network 默认元数据与脱敏错误，不收集 Cookie/Authorization。Employee 通过现有执行上下文调用，输出进入唯一 Result/Evidence。

### OSS DECISION

**WRAP Playwright core 为首选。** 官方 MCP/extension 是按需 WRAP 的互操作桥，首版不强制接管用户日常浏览器。browser-use 为 REFERENCE ONLY：自动规划层会与 Curis Employee/Work 执行循环重叠。Playwright 不提供 Company 权限、审批或搜索产品语义。[BrowserContext 源码](https://github.com/microsoft/playwright/blob/52a0e72005b4e8cef47b3174b6fb502636380023/packages/playwright-core/src/client/browserContext.ts)、[官方 MCP 模式](https://github.com/microsoft/playwright-mcp#browser-profiles)。

### CURIS OWNERSHIP

会话身份/租约、网络和文件范围、用户接管、外部动作审批、证据脱敏、引用持久性、恢复裁决。

### IMPLEMENTATION BOUNDARY

Curis Core → 现有 Capability Adapter 扩展 → Playwright → 专用 profile/context。先使用可见专用会话满足登录与接管；仅在站点确需已有浏览器且用户授权时加入 extension 路径。浏览器运行时负责 DOM/协议，Adapter 负责生命周期和标准输出，Core 负责谁能做什么。无需 fork 浏览器。验收 G1-V 必须证明两个账号隔离、接管互斥、掉线与最后动作未知、localhost 限制、上传下载与脱敏；当前均 NOT RUN。

## 4. G2 Model Capability

### PRODUCT CONTRACT

连接实例 ≠ Provider 名称 ≠ Model 名称。发现结果是该连接实际可访问集合；分页未完成或同步失败时，不据缺失结果批量禁用旧模型。档案区分 provider 声明 / 外部目录 / 本地测试，带来源、日期、连接和模型版本。每项能力取 supported / unsupported / unknown，不以 chat 成功证明 vision、tool、audio、embedding 或图像生成成功。

用途路由在现有 Employee 能力关系上解析：显式 Work 选择 → Employee 用途配置 → 合法 Company 默认；每步仍受权限、能力、数据外发与预算约束。无合格模型应等待配置，不能偷偷降级。fallback 只在预先允许、能力足够、数据目的地合法的集合发生；记录原模型、实际模型和原因。输出已开始、工具已外发或副作用未知时不得将 fallback 当透明重试。

提供按用途的轻量真实测试及失败原因。成本估计与 Provider 实际 usage 分开；无 usage 为 UNKNOWN，不能记零。所有 attempts 归入既有 `ai_usage_records`，外部 gateway 计量仅作来源，不创建第二 ledger。连接与凭证仍走已有 Keychain。

### OSS DECISION

REUSE 当前 ModelGateway 与 resolver；**ADAPT models.dev 的元数据映射**；**WRAP LiteLLM SDK 为有条件技术候选**，仅新增协议确实需要时采用，不默认部署代理服务、不替换现有正常路径。OpenRouter 是可接服务，不是本地开源 Model System。

LiteLLM 根 LICENSE 明确普通代码 MIT、enterprise 目录另有条款。其仓库 [Issue 24512](https://github.com/BerriAI/litellm/issues/24512) 报告历史 1.82.8 发布包安全问题；本轮未审计 wheel、未验证当前版本修复状态，不能认定当前 1.100.1 安全或受影响。进入集成前需发布来源、制品和依赖验证；这不阻塞现有 Gateway 承接首版合同。

### CURIS OWNERSHIP

Employee 用途关系、连接特定能力测试、数据外发授权、路由解释、受控 fallback、唯一计费归属。元数据目录中的 bool 只是声明，不是当前连接的产品可用状态。[models.dev schema](https://github.com/anomalyco/models.dev/blob/c142a1f8d11298643ebf9313fa889415775b3a4a/packages/core/src/schema.ts)。

### IMPLEMENTATION BOUNDARY

Core 决定允许集与用途；Adapter 规范化协议、错误、usage；Provider 实际执行。保留现有可用协议，不为抽象统一而接入所有 SDK。G2-V：分页故障不丢档案、同名不同连接、真假 tool/vision、未知能力、禁止 fallback、stream 中断、多 attempt 唯一记账，NOT RUN。

## 5. G3 Background Runtime

### PRODUCT CONTRACT

**选 B：用户级 Local background service。** 不选 A 作为默认经营承诺；不将首版依赖 C 云服务；D 混合是后续明确需求。后台服务需用户启用，权限被系统禁用时如实显示不可后台运行。

|生命周期|首版承诺|
|---|---|
|关闭窗口 / 退出 UI，后台已开启|Work 与合法排程继续；有可找到的状态与停止入口|
|选择“停止全部并退出” / 系统禁用后台|停止领取新动作，保存已知状态；正在外发动作可能进入效果未知；不能自动对抗用户重新拉起|
|睡眠 / 断网|本地不保证执行；恢复后检查漏触发与进行中动作，不宣称睡眠时持续经营|
|重启 / 登出|用户服务不承诺无登录执行；下次合法启动恢复；不会需要 root daemon 来绕开登录|
|UI 重开|接回同一 Runtime 与历史，不能启动第二个并行 owner|
|后台崩溃|监督重启后按持久状态和 lease/claim 核验；不把进程重启等同动作安全重试|

排程保存时区、规则、下一触发和漏触发策略。首版默认合并为一次待检查触发，不补发所有错过的外部写动作；用户显式设置跳过亦可。夏令时、系统时间变化与重复触发必须有验收。每次实际触发进入同一 Work 系统并具唯一标识，触发器不直接发布或付款。

### OSS DECISION

REUSE launchd/SMAppService + 现有 Runtime/SQLite；需要 cron/日历表达时 **WRAP APScheduler 3.11.3 的 trigger 计算**，不引入独立业务 job store。DBOS 为优先备用 REFERENCE ONLY；Temporal 为服务化未来 REFERENCE ONLY。[Apple 后台管理](https://developer.apple.com/documentation/appkit/managing-ongoing-background-processes-in-your-mac)、[APScheduler 3.x](https://apscheduler.readthedocs.io/en/3.x/userguide.html)。

### CURIS OWNERSHIP

后台开关含义、Work 领取和停止、漏触发策略、租约、资源上限、系统禁用表达、恢复列表。

### IMPLEMENTATION BOUNDARY

原生监督器管进程，触发库管时间计算，已有 Runtime 管唯一 Work 状态。当前 sidecar 退出即停止是明确 PRODUCT → IMPLEMENTATION GAP。DBOS 当前 `_sys_db.py` 明确选择 SQLiteSystemDatabase，故不是“必须 Postgres 所以淘汰”；暂不采用的理由是已有持久执行模型，再接引擎会增加操作记录/重放生命周期映射，而本轮需求还不要求通用代码工作流重放。若 G3/G4 验证证明现有 Runtime 无法可靠满足有限动作合同，应在同一 Work 下重新评估 DBOS，不能临时搭建通用工作流引擎。

G3-V：签名打包、用户服务注册/禁用、UI 退出不停、停止全部不自启、睡眠/断网/重启、重复 owner、时区/漏触发，NOT RUN。

## 6. G4 Execution / Recovery

### PRODUCT CONTRACT

一次 Work 可有多个 attempt；每次外部动作先有不可变请求摘要、目标、账号、资源范围、输入版本和幂等标识。审批绑定该快照；参数、对象、账号或权限发生实质变化即失效并重批。审批等待应持久化，不依赖 UI 存活；批准后执行前再次校验授权有效性。

|事件|必须发生的产品处理|
|---|---|
|只读/已确认未外发失败|在策略次数与预算内可重试；显示 attempt|
|写操作外发，超时/进程死亡|EFFECT_UNKNOWN；先查远端状态/幂等回执，再裁决；不能自动再发|
|Provider 支持可靠幂等键|同一逻辑动作重用键；不同目标或变更参数必须新动作|
|外部成功，落盘前崩溃|通过远端证据协调为成功或未知；不承诺任意 HTTP/浏览器 exactly-once|
|用户停止|停止新动作，尝试取消当前动作；“请求停止”与“已停止”分开；不能承诺撤销已经完成的外部效果|
|恢复|展示最后确认步骤、未确认动作、继续/核验/放弃选项；已完成步骤不重做|
|旧审批恢复/过期/已撤权|重新检查快照与授权；不自动消费旧 approval|

### OSS DECISION

REUSE 现有 Execution / Decision / Result / SQLite；**ADAPT DBOS/Temporal 的 durable step、历史、重试边界思想**；不复制其引擎或另建 Work。APScheduler 的 pause 是排程控制，不是正在执行动作的 checkpoint。DBOS 的 `invoke_step` 先运行函数再记录结果，直接证明第三方副作用与本地记录间仍有窗口；需要 Curis action-specific reconciliation。[DBOS invoke_step](https://github.com/dbos-inc/dbos-transact-py/blob/83805fd84494c85ea09105443884a2786152d921/dbos/_core.py)、[Temporal Activity Execution](https://docs.temporal.io/activity-execution)。

### CURIS OWNERSHIP

EFFECT_UNKNOWN、审批快照、幂等范围、补偿是否允许、停止反馈、证据与业务责任链；这些不是库配置项能替代的产品决定。

### IMPLEMENTATION BOUNDARY

首版只支持已登记 Adapter 动作的恢复分类：safe read / idempotent write / externally verifiable write / non-replayable。Core 原有执行状态扩展这些语义，不构建任意 Python 工作流重放服务。数据库事务/唯一约束承担本地原子性，原生进程工具承担取消，Adapter 给出 outbound/receipt/remote verification 事实。不能把“未知”映射成普通 failed。

G4-V：外发前、外发后、成功落盘前注入中断；重复触发/重复审批；变参旧审批；同动作幂等；停止后真实远端核验。先做可控假 Provider 故障验证，再做合法真实副作用验收；本轮 NOT RUN。

## 7. G5 Professional Tools

### PRODUCT CONTRACT

六类工具是共享能力，输出回到已有 Work/Result；没有独立 AI Workspace、Agent 商店或第二产物中心。

|类别|首版能力 / 成功证据|底层与边界|
|---|---|---|
|Terminal|限定 cwd/env 的命令；stdout/stderr、exit、超时、取消；交互仅在明确 PTY 会话|REUSE OS Shell + subprocess/asyncio；显式 Shell 时走授权，普通参数数组不拼接命令；cwd 不是安全沙箱，文件/网络权限需真实执行约束|
|Git|status/diff/log、明确授权的本地变更；操作前后 revision 与 dirty 状态|WRAP 已安装 Git CLI；不重写 Git、不清理用户改动、不隐式 push；凭证不取回模型|
|Preview|启动现有项目预览、显示地址/就绪/失败、停止；可由 G1 检查|WRAP 项目既有 dev server；不自造 Web Server；独占登记进程/端口，默认 loopback|
|OCR / Parser|文件转结构化文本、页/区域引用、错误与部分结果；保留原件|WRAP Docling 按需隔离 worker；轻量图像 OCR 可用 Tesseract，避免同一输入两套默认链|
|Data|授权文件/数据库读取、查询、导出和行数/来源；写入另需授权|REUSE sqlite3/CSV 与必要 Provider driver；只读连接/查询策略，不把模型生成 SQL 当安全边界|
|Media|probe、格式转换、裁剪/合并/提帧等已登记变换；文件与参数证据|WRAP FFmpeg/ffprobe；生成图片/视频走 G2 对应 Provider，不以转码冒充生成|

### OSS DECISION

首选原生与已安装能力；Docling/Tesseract/FFmpeg 只是后三类需要的底层候选。Docling `DocumentConverter.convert` 有 max_num_pages/max_file_size、ConversionResult、错误选项；默认上限不适合直接暴露不可信输入，Adapter 必须设限。Docling MIT 代码不覆盖所有模型权重许可。FFmpeg 具体构建决定 LGPL/GPL 义务，不因为用 CLI 就无需检查分发条件。[Docling converter](https://github.com/docling-project/docling/blob/014e8e357b24aa9d5113317fa454df8a70de9aeb/docling/document_converter.py)、[FFmpeg licensing](https://ffmpeg.org/legal.html)。

### CURIS OWNERSHIP

Work 目录和能力许可、危险动作审批、输入限额、长任务停止、工具版本、输出真实性、可恢复/不可恢复边界、Result/Evidence 归属。

### IMPLEMENTATION BOUNDARY

不复制 Shell/Git/OCR/编码器算法。长任务隔离进程，明确资源上限与取消；命令成功仅证明工具完成，结果需类型/存在性/内容校验。MCP 是可选传输，使用成熟协议实现；当前窄 McpAdapter 后续补 discovery/schema/errors/cancellation/version negotiation，不能自创协议。本轮不为协议查一整套新生态。

G5-V：Shell 子进程树终止、Git dirty 保留、Preview readiness、OCR 中英混排/坏页/超大文件、Data 只读拒写、Media 部分输出/取消及构建许可，NOT RUN。

## 8. G6 Backup / Recovery

### PRODUCT CONTRACT

备份是明确范围的结构包：数据库一致快照、格式/schema版本、受管附件与引用清单、文件 hash、排除项和不可搬迁资源。外部链接保留引用，不宣称远端内容已归档。凭证、Cookie、浏览器 profile、Keychain 材料不入包；使用正常登录/连接流程恢复。

恢复先预检：格式、大小/解压上限、路径、hash、DB integrity、schema兼容、可用空间、目标 Company、缺失附件与外部连接。先给恢复摘要，再停写并保留原数据回滚点；不能边经营边覆盖数据库。恢复后默认暂停自动触发与外部写动作，展示重连列表、断链引用和 G4 待核验 Work；用户核验后才重新启用。备份完整性校验不是防篡改签名，也不代表文件被加密。

### OSS DECISION

**REUSE 现有 recovery.py + sqlite3 / zipfile / hashlib / 文件系统原子替换 / macOS Keychain；ADAPT 现有包合同。** 不引入大型备份/同步集群。现有 `curis.release-backup/v1` 恰有 manifest+DB 两项校验，应通过后续批准的版本迁移扩展，不能直接往旧包塞附件破坏验证。

### CURIS OWNERSHIP

备份覆盖清单、稳定对象引用、重连待办、迁移可逆边界、恢复模式与外部副作用再核验。SHA256 验完整性，仍需明确备份含业务内容、存放位置和访问边界。

### IMPLEMENTATION BOUNDARY

SQLite `Connection.backup` 做一致数据库副本，现有工具已有 readonly source → backup → integrity/hash → ZIP → replace；restore 有锁和 safety copy。新增工作是附件一致性/包版本/预检/恢复后控制，不能称现有工具已覆盖所有这些。[Python SQLite backup](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup)。

G6-V：坏包/hash不符/未来schema/空间不足拒绝且原数据不变；DB+受管文件一致；Keychain排除；新机器重连；历史外部写不重发；恢复失败回滚。当前未执行备份或读写真实 DB，NOT RUN。

## 9. Open-source Reuse Matrix

Coverage 为能力边界判断，不是未经测试的百分比。

|Capability|Curis Need|Existing OSS|Coverage|Integration Cost|License|Decision|Curis Must Own|
|---|---|---|---|---|---|---|---|
|Browser|DOM/页面/账号上下文|Playwright|浏览器执行层强；经营/审批缺失|MEDIUM|Apache-2.0|WRAP|账号范围/接管/证据|
|Existing browser|已登录页面桥接|Playwright MCP/extension|桥接强；默认不强制|MEDIUM|Apache-2.0|WRAP optional|会话授权与互斥|
|Autonomous browsing|Agent浏览循环|browser-use|上层规划重叠|HIGH|MIT|REFERENCE ONLY|Employee/Work|
|Model protocol|多 Provider 调用|LiteLLM|协议/路由强；不含用途合同|MEDIUM|MIT core / enterprise separate|WRAP conditional|权限/用途/唯一Usage|
|Model catalog|元数据来源|models.dev|声明/价格/模态；不证明连接可用|LOW|MIT|ADAPT|测试/来源/unknown|
|Schedule|日历/cron|APScheduler 3.11.3|时间计算；不保证执行正确性|LOW trigger / MEDIUM scheduler|MIT|WRAP trigger|触发归属/漏触发|
|Durable steps|checkpoint/重放|DBOS|本地SQLite/持久步骤；需映射|HIGH migration|MIT|REFERENCE ONLY now|动作效果/批准/Work|
|Distributed workflows|服务型durability|Temporal Python SDK|完整引擎依赖服务；首版过重|HIGH|SDK MIT；服务独立审查|REFERENCE ONLY|经营模型与副作用|
|OCR/parser|页/结构解析|Docling|结构化解析强；质量需实测|MEDIUM|MIT code；weights separate|WRAP|原件/引用/限额|
|Image OCR|图像文字|Tesseract|OCR底层，不是完整文档理解|LOW–MEDIUM|Apache-2.0|WRAP optional|页与置信结果|
|Media|probe/变换|FFmpeg|媒体执行强；非生成Agent|MEDIUM|LGPL/GPL by build|WRAP|授权/结果/许可制品|
|Terminal/Git/Data|共享底层执行|OS Shell/Git/sqlite3|原生执行与驱动|LOW–MEDIUM|各自许可；不作统一MIT声明|REUSE + thin WRAP|资源边界/结果|
|Backup|一致包/恢复|SQLite/Python + current recovery|DB基础已在；产品清单待补|LOW–MEDIUM|标准库/SQLite各自许可|REUSE / ADAPT current|引用/重连/恢复模式|
|Background process|UI退出继续|launchd/SMAppService|macOS原生，非OSS新依赖|MEDIUM|Apple platform API|REUSE|用户选择/可见停止|

### 候选逐项16问

下表组统一用编号：1解决什么；2匹配；3缺口；4接口；5嵌入；6服务；7macOS；8权限；9状态；10暂停恢复重试；11真实结果；12观察；13许可；14维护；15成本；16分类。维护与版本见后附快照表。DOCUMENTED/L2 不等于本机验证。

#### Playwright

|问题|判断|
|---|---|
|1|浏览器自动化|
|2|DOM/截图/网络/文件|
|3|搜索源、经营授权、人工接管协调|
|4|Node/Python等API|
|5|可作为本地浏览器worker|
|6|本地浏览器进程；无需SaaS|
|7|官方支持；打包未验|
|8|context权限不是安全隔离；Core限制|
|9|context/profile；持久profile受保护|
|10|API超时/关闭；Work恢复自管|
|11|页面/截图/下载等真实返回|
|12|events/trace/console；敏感内容需过滤|
|13|Apache-2.0|
|14|固定快照和发布见下表|
|15|MEDIUM|
|16|WRAP|

#### Playwright MCP

|问题|判断|
|---|---|
|1|Agent可调用浏览工具|
|2|snapshot/交互/extension桥|
|3|Company权限及Work恢复|
|4|MCP stdio/HTTP|
|5|可本地子进程|
|6|MCP server+浏览器；不需云|
|7|Chrome/Edge extension；本机未验|
|8|工具开关/域限制不等于授权；不开放任意代码给未信任调用方|
|9|persistent/isolated/extension；profile独占|
|10|关闭/重连不等于业务resume|
|11|工具结果/截图|
|12|工具调用与页面活动|
|13|Apache-2.0|
|14|main内容已保存hash；release/commit UNKNOWN|
|15|MEDIUM|
|16|WRAP optional|

#### browser-use

|问题|判断|
|---|---|
|1|自主浏览Agent循环|
|2|浏览器session/DOM/截图/远端连接|
|3|会重叠Curis Agent决策层|
|4|Python Agent/BrowserSession|
|5|可但高耦合|
|6|本地浏览器；云能力需另审|
|7|Python/Chromium路径；未实测|
|8|域限制配置不是Curis权责|
|9|BrowserSession/profile可配|
|10|Agent控制不证明副作用安全恢复|
|11|浏览动作/任务结果；需接Curis证据|
|12|history/logs；使用前脱敏|
|13|MIT|
|14|见快照|
|15|HIGH|
|16|REFERENCE ONLY|

#### LiteLLM

|问题|判断|
|---|---|
|1|多模型协议与Router|
|2|调用/策略/fallback/usage|
|3|Employee用途测试与权限|
|4|Python SDK/HTTP proxy|
|5|SDK可嵌入|
|6|SDK不要求代理；代理可独立|
|7|Python可用性为文档层；未验|
|8|gateway权限不能替Curis权限|
|9|请求/Router配置；非Work历史|
|10|有retry/fallback；必须由Core约束|
|11|Provider响应与usage；非业务验收|
|12|回调/错误/日志需脱敏|
|13|MIT core；enterprise另约|
|14|见快照；历史包安全Issue待制品核验|
|15|MEDIUM|
|16|WRAP conditional|

#### models.dev

|问题|判断|
|---|---|
|1|模型目录|
|2|价格/模态/上下文/tool声明|
|3|实际连接可用与测试|
|4|JSON/TOML/schema|
|5|数据适配即可|
|6|无必要常驻服务|
|7|数据平台无关|
|8|不授予任何Provider访问|
|9|本地缓存+来源时间由Curis|
|10|刷新失败保留旧快照；没有Execution恢复|
|11|元数据不是Execution Result|
|12|字段来源/差异由Curis记录|
|13|MIT|
|14|按commit；无latest release|
|15|LOW|
|16|ADAPT|

#### APScheduler

|问题|判断|
|---|---|
|1|定时计算与调度|
|2|cron/interval/date/misfire|
|3|durable动作/批准/效果未知|
|4|Python trigger/scheduler|
|5|可嵌入|
|6|无需远程服务|
|7|Python；Desktop打包未验|
|8|执行进程权限；不管业务授权|
|9|trigger参数；完整scheduler可jobstore但不采用第二业务库|
|10|pause schedule；不停止已运行函数|
|11|job返回/异常非业务证据|
|12|events/logs|
|13|MIT|
|14|3.11.3稳定tag；见快照|
|15|LOW trigger|
|16|WRAP trigger|

#### DBOS

|问题|判断|
|---|---|
|1|持久workflow/step|
|2|SQLite路径/checkpoint/retry/队列|
|3|审批意义/外部原子性/现有Work映射|
|4|Python decorators/client|
|5|可以，非必须SaaS|
|6|SQLite可无DB服务；Postgres模式需服务|
|7|Python本地路径；当前打包未验|
|8|worker OS/DB权限；不是业务授权|
|9|workflow/operation结果库|
|10|durable恢复/取消/重试；同步步骤不可假设立即抢占|
|11|保存函数返回；外部效果需核验|
|12|步骤历史/日志/trace|
|13|MIT|
|14|见快照；README强调Postgres但源码仍有SQLite|
|15|HIGH迁移|
|16|REFERENCE ONLY；ADAPT原则|

#### Temporal Python SDK

|问题|判断|
|---|---|
|1|服务型持久编排|
|2|历史/活动/超时/重试/信号|
|3|服务运维与Curis业务映射|
|4|Python SDK/worker|
|5|客户端可嵌入；完整系统非单库|
|6|需要Temporal服务；dev server非产品部署保证|
|7|SDK文档路径；完整Desktop未验|
|8|namespace/TLS等不是Employee权限；workflow sandbox非安全沙箱|
|9|服务保存history|
|10|恢复/重试/协作取消；外部effect仍可能未知|
|11|activity真实返回；验证自管|
|12|history/metrics/tracing|
|13|SDK MIT；server/部署条款单独核验|
|14|见快照|
|15|HIGH|
|16|REFERENCE ONLY|

#### Docling

|问题|判断|
|---|---|
|1|结构化文档转换|
|2|PDF/多格式/OCR/页结构|
|3|Curis引用体系/质量保证|
|4|Python converter/CLI|
|5|可隔离worker|
|6|本地可；模型资产需准备|
|7|README声明macOS arm64/x86_64；未验|
|8|进程/输入路径权限；默认大小上限需收紧|
|9|转换结果；非持久Work|
|10|失败/部分结果可表达；持久resume不保证|
|11|ConversionResult/DoclingDocument|
|12|错误/处理元数据|
|13|MIT code；模型另许可|
|14|见快照|
|15|MEDIUM|
|16|WRAP|

#### Tesseract

|问题|判断|
|---|---|
|1|图像OCR|
|2|文字/布局输出|
|3|复杂文档结构及经营语义|
|4|CLI/C++ TessBaseAPI|
|5|可独立进程或库|
|6|无需网络服务；语言数据需准备|
|7|项目说明支持；打包未验|
|8|进程/文件范围；无Curis授权|
|9|图像/模型/结果；无Work库|
|10|重跑/终止由Adapter；无durable恢复|
|11|GetUTF8Text等真实识别结果；质量不保证|
|12|错误/置信相关输出|
|13|Apache-2.0|
|14|见快照|
|15|LOW–MEDIUM|
|16|WRAP optional|

#### FFmpeg

|问题|判断|
|---|---|
|1|媒体probe和转换|
|2|音视频变换/文件结果|
|3|生成式模型/Work语义|
|4|ffmpeg/ffprobe CLI/library|
|5|可子进程|
|6|无需SaaS|
|7|平台可编译；具体制品未验|
|8|本地/网络协议需限制；文件进程权限|
|9|输入输出文件，无Work持久化|
|10|信号取消/重跑；不保证任意转码checkpoint|
|11|输出文件与probe需二次校验|
|12|stderr/progress/exit|
|13|LGPL基础、可选GPL；具体build核验|
|14|源码活跃；GitHub release不适用|
|15|MEDIUM|
|16|WRAP|

### 固定源码、发布与维护快照

检索日期为2026-09-15；最近提交只证明活动，不证明质量或稳定。默认分支源码可能领先发布版；实施必须重新固定实际采用tag/制品并复验，不直接安装本表HEAD。

|Repo|源码commit|最近发布|最近push|
|---|---|---|---|
|microsoft/playwright|52a0e72005b4e8cef47b3174b6fb502636380023|v1.63.0|2026-09-14T15:45:05Z|
|microsoft/playwright-mcp|UNKNOWN|UNKNOWN / release API unavailable|UNKNOWN|
|browser-use/browser-use|843819cb8131e1370948d381ede9be7f8366ddc4|0.13.10|2026-09-13T20:04:16Z|
|BerriAI/litellm|9e1ed40db3376dc8e7b9392aa104653ca22d3fdb|v1.100.1|2026-09-14T16:49:56Z|
|anomalyco/models.dev|c142a1f8d11298643ebf9313fa889415775b3a4a|UNKNOWN / release API unavailable|2026-09-14T16:46:51Z|
|agronholm/apscheduler|6a2a8851bafeb01dfe48e3b54be6dd3b3d4eae96|3.11.3|2026-09-10T21:21:50Z|
|dbos-inc/dbos-transact-py|83805fd84494c85ea09105443884a2786152d921|2.31.1|2026-09-14T16:44:49Z|
|temporalio/sdk-python|ab25ed693f7ec77589346e66c98db299a8c9c9fe|1.32.0|2026-09-14T16:31:06Z|
|docling-project/docling|014e8e357b24aa9d5113317fa454df8a70de9aeb|v2.127.0|2026-09-14T10:06:55Z|
|tesseract-ocr/tesseract|8ae68101439b3f7df123499a784e8896c805179d|5.5.3|2026-09-11T05:17:27Z|
|FFmpeg/FFmpeg|639ee849526cfe61ceb312776335c245b98bd9d4|UNKNOWN / release API unavailable|2026-09-14T12:44:39Z|

### 针对性源码索引

|Repo / path|symbol与用途|固定证据|
|---|---|---|
|microsoft/playwright / `packages/playwright-core/src/client/browserContext.ts`|BrowserContext：page/context/storage state边界|[保存源码](https://raw.githubusercontent.com/microsoft/playwright/52a0e72005b4e8cef47b3174b6fb502636380023/packages/playwright-core/src/client/browserContext.ts)；ref `52a0e72005b4e8cef47b3174b6fb502636380023`|
|microsoft/playwright-mcp / `README.md`|README/License边界筛选|[保存源码](https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md)；ref `main`|
|microsoft/playwright-mcp / `LICENSE`|README/License边界筛选|[保存源码](https://raw.githubusercontent.com/microsoft/playwright-mcp/main/LICENSE)；ref `main`|
|anomalyco/models.dev / `packages/core/src/schema.ts`|Model/Provider字段：tool_call/modalities/limit，声明不是测试|[保存源码](https://raw.githubusercontent.com/anomalyco/models.dev/c142a1f8d11298643ebf9313fa889415775b3a4a/packages/core/src/schema.ts)；ref `c142a1f8d11298643ebf9313fa889415775b3a4a`|
|BerriAI/litellm / `litellm/router.py`|Router及fallback helpers：路由、错误与回退|[保存源码](https://raw.githubusercontent.com/BerriAI/litellm/9e1ed40db3376dc8e7b9392aa104653ca22d3fdb/litellm/router.py)；ref `9e1ed40db3376dc8e7b9392aa104653ca22d3fdb`|
|dbos-inc/dbos-transact-py / `dbos/_sys_db.py`|SystemDatabase工厂：SQLite/Postgres选择；operation结果|[保存源码](https://raw.githubusercontent.com/dbos-inc/dbos-transact-py/83805fd84494c85ea09105443884a2786152d921/dbos/_sys_db.py)；ref `83805fd84494c85ea09105443884a2786152d921`|
|dbos-inc/dbos-transact-py / `dbos/_core.py`|invoke_step/record_step_result：函数执行后记录，外部副作用窗口|[保存源码](https://raw.githubusercontent.com/dbos-inc/dbos-transact-py/83805fd84494c85ea09105443884a2786152d921/dbos/_core.py)；ref `83805fd84494c85ea09105443884a2786152d921`|
|agronholm/apscheduler / `README.rst`|README/License边界筛选|[保存源码](https://raw.githubusercontent.com/agronholm/apscheduler/3.11.3/README.rst)；ref `3.11.3`|
|agronholm/apscheduler / `LICENSE.txt`|README/License边界筛选|[保存源码](https://raw.githubusercontent.com/agronholm/apscheduler/3.11.3/LICENSE.txt)；ref `3.11.3`|
|agronholm/apscheduler / `src/apscheduler/triggers/cron/__init__.py`|CronTrigger：日历匹配/get_next_fire_time|[保存源码](https://raw.githubusercontent.com/agronholm/apscheduler/3.11.3/src/apscheduler/triggers/cron/__init__.py)；ref `3.11.3`|
|docling-project/docling / `docling/document_converter.py`|DocumentConverter.convert：输入限额/ConversionResult|[保存源码](https://raw.githubusercontent.com/docling-project/docling/014e8e357b24aa9d5113317fa454df8a70de9aeb/docling/document_converter.py)；ref `014e8e357b24aa9d5113317fa454df8a70de9aeb`|
|tesseract-ocr/tesseract / `include/tesseract/baseapi.h`|TessBaseAPI::Init/GetUTF8Text：OCR可调用API|[保存源码](https://raw.githubusercontent.com/tesseract-ocr/tesseract/8ae68101439b3f7df123499a784e8896c805179d/include/tesseract/baseapi.h)；ref `8ae68101439b3f7df123499a784e8896c805179d`|
|FFmpeg/FFmpeg / `LICENSE.md`|FFmpeg许可构建边界|[保存源码](https://raw.githubusercontent.com/FFmpeg/FFmpeg/639ee849526cfe61ceb312776335c245b98bd9d4/LICENSE.md)；ref `639ee849526cfe61ceb312776335c245b98bd9d4`|

## 10. REUSE / WRAP / ADAPT / BUILD Decisions

REUSE：现有 Work/Execution/Decision/Result、ModelGateway、Keychain、恢复工具；标准 SQLite/文件操作；系统 Shell/Git；原生后台管理。这里“复用现有”不是宣称已有实现覆盖全部合同。

WRAP：Playwright 主路径；APScheduler 时间计算；Docling/FFmpeg；按需 Tesseract 和官方浏览桥。LiteLLM 仅在协议需求和安全制品门槛通过后选入。

ADAPT：models.dev 字段映射、出处与unknown规则；现有备份包的范围与版本；durable步骤/重试原则映射进现有执行控制。ADAPT 不表示复制另一套数据库或fork整个项目。

REFERENCE ONLY：browser-use 的浏览交互经验、DBOS 的恢复边界、Temporal 的成熟历史/活动契约。DBOS 是现有 Runtime 无法通过验证时第一备用技术比较对象，Temporal 只在服务化规模需求成立后重开。

BUILD：Curis 权限与责任语义、审批快照、EFFECT_UNKNOWN 协调、账号接管、连接特定测试、漏触发策略、恢复清单、工具结果归属。这些是产品合同闭合所需，不是自造浏览器/模型路由/持久引擎的理由。

## 11. Curis Core Ownership

Company / Business / Department / Workspace 是现有归属与Context；Employee / Responsibility 决定谁负责；Work / Execution 是唯一执行关系；Permission / Decision 决定动作是否允许；Result / Evidence / Learning 记录结果与追溯；CEO 体验负责理解、介入和裁决。外部 workflow_id/session_id/request_id 只能是技术关联，不能变成第二个用户 Work 或第二个 Employee。

外部库不能自行选择业务目标、扩大权限、改变审批快照、默认发布、替换账号、把未知效果降级为失败、吞掉 usage、宣布 Result 已被业务接受。Provider 返回成功是证据输入，业务成功仍要按目标标准核验。

## 12. Provider / Adapter Architecture

```text
现有 Company/Employee/Work + Context/Permission/Decision
          ↓ 合法动作与已批准快照
现有 Execution 控制（claim / attempt / checkpoint / unknown-effect）
          ↓ 现有 Capability Adapter 按能力扩展
Browser → Playwright       Model → 当前Gateway（必要时LiteLLM）
Tools → Shell/Git/Parser/Media/Data   Schedule → 时间计算
          ↓ 标准结果、错误、外发状态、回执、usage
现有 Result / Evidence / 唯一 Usage → Work 历史与 CEO 介入
```

后台用户服务承载同一 Runtime，不在 UI 和 daemon 各跑一套调度器。现有数据库持久化状态；生产接入需既有正式 Issue 指定唯一写入/领取机制与 allowed files。模型与工具不共享无限权限；能力选择只返回允许执行的动作集合。

Adapter 最少必须带原有 scope/work/execution关联、动作输入版本、授权引用、外发是否发生、远端回执、可恢复类别和真实输出引用。字段名称是合同表达，不在本轮创建 schema。一个 Provider 不要求一个新微服务；仅浏览器/重解析/媒体等资源隔离有实际意义的工作用进程边界。

## 13. Product Contract Changes

|Gap|从上轮未闭合点到明确建议|不承诺|
|---|---|---|
|G1|专用可见会话优先；三种Web能力；登录隔离+人工接管|任意网站保证成功、绕验证码、自动共享日常账号|
|G2|连接特定三态能力+用途路由+受限fallback+真实测试|模型列表即能力验证、静默跨Provider、未知费用记零|
|G3|B 用户级后台服务；明确用户开关与睡眠/退出规则|睡眠/关机仍本地执行、隐藏root常驻、停用后自启|
|G4|有限动作类型恢复；审批快照；EFFECT_UNKNOWN单独处理|任意外部动作exactly-once、停止等于撤回、旧审批永久有效|
|G5|六类共享工具，真实结果回唯一Work|第二AI Workspace、Shell安全靠cwd、转码冒充生成|
|G6|DB+受管文件范围、重连列表、恢复暂停与核验|备份导出登录凭证、远端对象自动搬家、恢复自动重发|

这些是 Research Product Decisions，需 CEO 一次审查；不是 Current Authority 的新增事实。若 CEO 不接受 B 后台选项或其他关键边界，本裁决改为 C 并重开对应合同，不能以“实现更方便”为由默默改成 A。

## 14. Product Expression V2 Changes Required

**仅列后续修改，不改 V2 文件。** 原有页面结构、七区和六组 Settings 不因选库而增加项目导航。

|V2对应能力段|CEO接受后需要的表达变化|验证链接|
|---|---|---|
|C12–16/C21 Browser与Web|Search/Reader/Interactive可用性分开；专用账号会话、接管/归还控制、掉线核验、授权localhost；来源和下载返回Work|G1-V|
|C02–08 Model|连接/模型区分；来源/测试三态；真实用途测试；fallback说明和实际usage；发现不完整提示|G2-V|
|C25–27 Background|后台服务开启/系统禁用、关闭UI继续、停止全部；休眠漏触发与重启核验；同一任务历史|G3-V|
|C29/C38–40 Execution|审批对象快照、变更失效、attempt、等待停止、效果未知与核验/继续入口|G4-V|
|C17–24/C42 Tools|共享工具可用性、安装/授权/限额状态；Terminal进程、Preview就绪、Parser部分失败、媒体实际产物|G5-V|
|C43–48 Recovery|备份范围摘要、缺失文件、凭证排除、restore preflight、重连待办、恢复后暂停与原数据回退|G6-V|
|跨全部状态合同|unsupported / unknown / unconfigured / permission denied / offline / effect unknown不可合并成generic error|各Gap|

参数范围、默认值与触发入口应回填原77项Settings及相关surface/action字段，不生成第二份V2或平行Master Map。LiteLLM、Playwright、APScheduler等名字是实现/高级诊断信息，不成为普通用户必须理解的核心产品名词。

## 15. Remaining Product Gaps

本轮需求层不保留“以后再决定是否有后台、能否恢复、如何登录”的空白。保留的是 CEO 接受门槛及明确实施验证，不将未运行的技术判断升级为可用产品。

|Gate|Owner|需返回证据|失败后的处理|
|---|---|---|---|
|CEO合同Review|CEO / Product|接受/拒绝本文各合同；尤其B后台与恢复停止规则|拒绝项回C，不能先集成|
|G1-V|Browser/Runtime owner|账号隔离、接管、写后掉线、脱敏与localhost测试|修Adapter或窄化支持站点，不绕授权|
|G2-V|Model/Runtime owner|分页、能力真实测试、fallback/usage；如采用LiteLLM附制品验证|保留当前Gateway；不将目录当测试|
|G3-V|Desktop/Runtime owner|真实打包后台、系统禁用、退出/睡眠/重启和重复claim|复核生命周期；必要时重评DBOS，不偷改合同|
|G4-V|Execution/Review owner|中断注入与真实远端核验、审批失效、幂等与停止证据|未证明前相关外部写能力不可接受|
|G5-V|Tool/Release owner|六类代表性输入输出、取消/资源权限、实际构建license|缺哪类就显示该类不可用，不影响其他独立能力|
|G6-V|Desktop/Recovery owner|损坏包拒绝、原数据不变、新机重连、恢复不重发|恢复发布保持blocked|

Unknown：本机新候选打包/性能、MCP当前精确release、LiteLLM当前wheel安全状态、FFmpeg最终构建配置、Parser选用权重许可/识别质量。都不能由本报告假定通过。它们没有迫使首版引入新的产品对象，也没有改变本轮明确的用户合同。

## 16. Final Closure Verdict

**B. CLOSED WITH EXPLICIT IMPLEMENTATION VALIDATION**

六项均有用户能力、首版边界、首选路径、Curis ownership 与可失败的验证标准。A 不适用：未做实现验证与 CEO 接受；C 不作为本轮建议：架构选择已明确，不再把核心产品决定留给开发猜。本文 Verdict 不修改上轮原始 C，也不修改发布/Final UI/Authority 的状态。

Disposition: SUBMITTED FOR CEO REVIEW — NOT ACCEPTED.
Owner: CEO / Product Review.
Next Action: 接受或拒绝合同；接受后只进入 Blueprint Deep Reconciliation，再开正式实现 Issue。
Target Authority: 唯一现有 Product Blueprint 及其派生文档；本研究不是第二份 Authority。
Next Gate: CEO REVIEW.

STOP FOR CEO REVIEW.
