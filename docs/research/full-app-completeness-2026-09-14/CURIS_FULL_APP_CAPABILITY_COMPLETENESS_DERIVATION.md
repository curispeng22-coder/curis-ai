# CURIS FULL APP CAPABILITY COMPLETENESS DERIVATION

Authority Class: RESEARCH
Status: Review
Disposition: DERIVATION COMPLETE / CANDIDATE — CEO REVIEW REQUIRED
Date: 2026-09-15 Asia/Shanghai

本轮只推导研究候选。V1的READY FOR UI已按CEO指令暂停；未修改唯一Blueprint、Frozen Authority、Runtime、UI或数据库。以下“默认”与“应该”均为候选产品合同，不是当前实现事实。当前实际私有配置未读取，不能以候选默认冒充当前值。

## 证据与验收边界

E编号对应[evidence/source-manifest.json](evidence/source-manifest.json)中的精确路径与SHA256。源码读取仅证明相应实现片段，不代表真实端到端验收；接受报告只消费明确接受范围。未知与未验证不等于确定不存在。未读取Credential、真实数据库或用户数据。

[模型元数据安全探针](evidence/model-profile-probe.json)只从源码提取纯函数并输入合成数据。它证明本地解析的鲁棒性问题，不证明真实Provider返回了合成的嵌套vision字段。

官方协议对照： [OpenAI Models](https://developers.openai.com/api/reference/resources/models)、[Claude Models](https://platform.claude.com/docs/en/api/http/models)、[Gemini Models](https://ai.google.dev/api/models)、[Playwright隔离](https://playwright.dev/docs/browser-contexts)、[Playwright认证](https://playwright.dev/docs/auth)、[MCP Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)。目录可见性、模型能力声明、实测与工具执行授权是不同证据层；以下合同是基于这些边界和真实业务场景的研究推导。

## 推导方法与两轮反证

先从五类Business的工作链生成C01–C36；再经中途依赖失效攻击补入C37–C42；最后经长期使用、恢复、更新、退役与可访问性攻击补入C43–C48。详细过程见[FIRST_PASS_AND_ADVERSARIAL_REVIEW.md](FIRST_PASS_AND_ADVERSARIAL_REVIEW.md)。此阶段没有先读V1来限定能力。

## 完整18步推导

### C01 — 首次启动与就绪检查

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO第一次打开，想让公司研究一个业务，而不是先装全部工具。

**STEP 2 — BUSINESS / WORK NEED**

公司/CEO/真实原装员工可存在；明确何种工作可立即做、缺哪项能力。

**STEP 3 — REQUIRED CAPABILITY**

首次启动与就绪检查

**STEP 4 — CURRENT CHECK**

部分支持：E02记录无Key bootstrap/6+1员工及原子创建Accepted Candidate；不代表全部首次配置已接通。

**STEP 5 — FAILURE TEST**

若只画欢迎页或生成假员工，第一条真实委托无合法责任或模型。

**STEP 6 — CROSS-BUSINESS TEST**

研发：可准备需求；内容：可准备账号经营目标；均不应无模型假运行。全局。

**STEP 7 — PRODUCT OBJECT**

复用Company、CEO、Employee、Assignment与现有就绪状态投影。

**STEP 8 — USER-VISIBLE INFORMATION**

公司名/CEO名/原装组织/模型可用性/当前能做什么/缺口/继续入口；不显示假业务。

**STEP 9 — INPUT / EDITING**

首次公司名必填、CEO称呼可编辑、时区系统建议；可跳过模型但说明不能执行。

**STEP 10 — DEFAULT**

首次不选业务、不配任意Provider、不授电脑权限；按一项真实工作请求逐步补齐。

**STEP 11 — ADVANCED SETTINGS**

数据根目录/恢复旧公司在有需要时展开，不让新人配Runtime端口。

**STEP 12 — EFFECT**

改称呼不换identity；恢复公司不能另生成重复员工；完成模型检查只解锁相应动作。

**STEP 13 — VALIDATION**

隔离新数据根：无Key启动→真实组织→未配委托留待准备→配置后真实一项工作→重启不复制。

**STEP 14 — STATE**

创建中/已有公司/待配置/可开始某类工作/恢复失败。

**STEP 15 — FAILURE / UNKNOWN**

读失败不能显示0员工；初始化失败保留可诊断原因和恢复入口。

**STEP 16 — PERMISSION / SECURITY**

Company本地Owner，未有外部授权前不访问私人文件或账号。

**STEP 17 — PRODUCT PLACEMENT**

CEO工作台首屏+有返回目标的初始配置Main。

**STEP 18 — INTERACTION**

[开始第一项工作]收集意图；[配置模型]进入模型连接；[稍后设置]回可阅读公司，原意图保留。

### C02 — Provider连接实例与认证

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO有两个同品牌API账户，另有一个本地模型服务。

**STEP 2 — BUSINESS / WORK NEED**

区分供应品牌、具体连接、账号/项目/区域与认证方式。

**STEP 3 — REQUIRED CAPABILITY**

Provider连接实例与认证

**STEP 4 — CURRENT CHECK**

部分支持：E03 ProviderConnectIn有credential_ref/base_url/model_ids/save；E04有UI；多同品牌连接独立身份未验证。

**STEP 5 — FAILURE TEST**

按Provider品牌作唯一连接会覆盖账户、账单或隐私边界。

**STEP 6 — CROSS-BUSINESS TEST**

研发客户A密钥与写作个人服务；数据分析本地服务。全局共享。

**STEP 7 — PRODUCT OBJECT**

现有Provider/Connection的实例引用候选扩展，品牌不是连接ID。

**STEP 8 — USER-VISIBLE INFORMATION**

连接显示名、供应类型、位置、服务地址、外部账户提示、认证状态、检查时间、使用员工数。

**STEP 9 — INPUT / EDITING**

名称/类型必填；官方URL自动可读；自定义URL用户填；Key安全输入或受支持OAuth/Local；org/project/region仅适配器要求才出现。

**STEP 10 — DEFAULT**

未连接；官方URL来自适配器；不默认创建API账号/开启收费；HTTP仅明确本机服务。

**STEP 11 — ADVANCED SETTINGS**

代理/超时/TLS诊断/org/project/region等因服务要求出现；不默认要求每项填。

**STEP 12 — EFFECT**

变更URL/账户使旧检查失效，展示受影响员工；旧运行保留原连接版本。

**STEP 13 — VALIDATION**

元数据检查→认证→列表→用户选模型的实际最小调用；各步分别成功；撤销后不得继续用。

**STEP 14 — STATE**

草稿/授权中/已保存未测/可连接/需重授权/地址不可达。

**STEP 15 — FAILURE / UNKNOWN**

401/403/网络/协议错误分开；不把“已保存”写成能工作。

**STEP 16 — PERMISSION / SECURITY**

Secret只vault引用；OAuth敏感授权给人；外部项目权限不由Employee岗位授予。

**STEP 17 — PRODUCT PLACEMENT**

Settings模型与AI→Provider连接Main/Drawer；员工缺口就地返回。

**STEP 18 — INTERACTION**

[添加提供方]→选择类型→连接Drawer→[保存并检查]→显示逐步结果→[选择模型]；失败保输入但不回显秘密。

### C03 — 模型发现与手动登记

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO连上Provider却只想启用两个模型；服务不提供完整列表。

**STEP 2 — BUSINESS / WORK NEED**

动态分页发现+手动ID+可用性/去重/停用/刷新范围，不把模型列表当执行验证。

**STEP 3 — REQUIRED CAPABILITY**

模型发现与手动登记

**STEP 4 — CURRENT CHECK**

部分支持：E03 connect动态/curated及未发现项inactive；只读一页与手填验证闭环需进一步核查；E17 DeepSeek动态发现已Accepted。

**STEP 5 — FAILURE TEST**

不支持list但支持generate的服务永远不可用；分页缺失可能错误停用模型。

**STEP 6 — CROSS-BUSINESS TEST**

研究长上下文模型、内容图像模型在同目录；共享但用途不同。

**STEP 7 — PRODUCT OBJECT**

现有Model Catalog/Connection内模型条目、发现批次与来源。

**STEP 8 — USER-VISIBLE INFORMATION**

模型ID/显示名/连接/类型/已启用/发现来源/是否实际测试/最后发现时间/列表完整性。

**STEP 9 — INPUT / EDITING**

自动列表勾选启用；手动模型ID必填；可改展示名，不改远端ID身份。

**STEP 10 — DEFAULT**

发现不批量设默认；分页未完成不停用未返回项；手动模型先未测试。

**STEP 11 — ADVANCED SETTINGS**

API路径/兼容协议只自定义Provider；手动能力断言在高级并标用户声明。

**STEP 12 — EFFECT**

刷新新增/退役给差异预览；已绑定消失项保引用并阻塞后续，不删历史。

**STEP 13 — VALIDATION**

分页、多连接同ID、列表失败、手动合法ID、embedding-only、消失再出现的合成测试+真实选型调用。

**STEP 14 — STATE**

发现中/部分列表/已发现未测/手工登记/退役/已启用。

**STEP 15 — FAILURE / UNKNOWN**

发现失败不清空现有目录；无models接口给[手动添加]而非无路可走。

**STEP 16 — PERMISSION / SECURITY**

仅使用已授权连接；发现API不授员工模型使用权。

**STEP 17 — PRODUCT PLACEMENT**

Provider详情模型列表与[手动添加模型]Drawer。

**STEP 18 — INTERACTION**

[发现模型]→可选列表及来源→[启用所选]；手填→[测试此模型]→明确结果→返回员工原能力选择。

### C04 — Model Profile的能力事实与来源

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工收到图片/PDF/工具任务，需要先判断所选模型能否处理。

**STEP 2 — BUSINESS / WORK NEED**

按模态方向、工具/结构化/推理/上下文限制明确三值能力及证据新鲜度。

**STEP 3 — REQUIRED CAPABILITY**

Model Profile的能力事实与来源

**STEP 4 — CURRENT CHECK**

部分支持：E03 _profile有features和unknown；AST probe证实empty/embedding也chat=supported；新token字段未解析。

**STEP 5 — FAILURE TEST**

把模型名当能力会向文本模型发图片或把embedding模型选成聊天模型。

**STEP 6 — CROSS-BUSINESS TEST**

内容截图/研发UI截图；研究PDF/数据结构化输出。共享。

**STEP 7 — PRODUCT OBJECT**

Model Profile附于现有模型元数据，不新建Employee类型。

**STEP 8 — USER-VISIBLE INFORMATION**

名称/连接/ID/文本输入输出/视觉/音频/生成类型/Tool/结构化/推理/Computer Use/Context/Output/来源/测试状态。

**STEP 9 — INPUT / EDITING**

通常只读；缺资料可高级填写限制/能力声明，必须来源和更新时间；不允许覆盖验证失败为已通过。

**STEP 10 — DEFAULT**

未知就是unknown；不以family名称猜可用；用户覆盖只能收紧硬上限，扩大必须重新验证。

**STEP 11 — ADVANCED SETTINGS**

Model family、原始安全元数据、能力覆盖来源、最大输入输出/文件类型/streaming等详细页。

**STEP 12 — EFFECT**

能力变更影响候选路由/附件校验；原执行记录引用当时profile版本。

**STEP 13 — VALIDATION**

分别文本、图像、audio、Tool schema、structured output探针；不得以hello验证全部。

**STEP 14 — STATE**

官方声明/接口声明/用户声明/实测通过/实测失败/过期/未知同时分维度。

**STEP 15 — FAILURE / UNKNOWN**

“视觉未验证”，CTA[测试视觉]；不支持明确不可选，不能用灰掉空控件掩盖。

**STEP 16 — PERMISSION / SECURITY**

测试须可用连接及数据外发许可；合成样本不携用户内容。

**STEP 17 — PRODUCT PLACEMENT**

模型详情Main概览+能力表；Employee选择器只展示任务必需维度。

**STEP 18 — INTERACTION**

点模型→概览用途/限制→[查看能力依据]Utility→[测试所选能力]→更新该维度，不自动扩大权限。

### C05 — 多用途模型选择与有界Fallback

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

同员工写文案用快模型，看图用视觉模型，复杂审核用推理模型。

**STEP 2 — BUSINESS / WORK NEED**

员工可用集合/用途偏好/固定或自动/候选失败回退，以及隐私成本和效果约束。

**STEP 3 — REQUIRED CAPABILITY**

多用途模型选择与有界Fallback

**STEP 4 — CURRENT CHECK**

部分支持：E06可多能力+preferred；E05租户默认；E16有有限fallback执行；用途路由完整产品未验证。

**STEP 5 — FAILURE TEST**

一员工一模型导致任务不兼容；静默跨Provider回退可外发禁止资料。

**STEP 6 — CROSS-BUSINESS TEST**

研发coding+截图；研究抽取+推理；共享。

**STEP 7 — PRODUCT OBJECT**

复用Employee capability bindings与运行选择记录，用途不新建人。

**STEP 8 — USER-VISIBLE INFORMATION**

本用途选择模式/候选/实际模型/选择理由/不可用项/回退目标及原因/费用与位置。

**STEP 9 — INPUT / EDITING**

Company默认、Employee各用途继承或固定；自动只在明确许可集合选；fallback列表可排序。

**STEP 10 — DEFAULT**

不静默跨连接/区域回退；Company默认只是未指定用途起点；未配置fallback则等待恢复。

**STEP 11 — ADVANCED SETTINGS**

硬能力约束/位置/预算上限；高级禁用用途的自动选择；不是任意模型调度图。

**STEP 12 — EFFECT**

只影响后续调用；本轮能力切换要保运行与费用溯源；拒绝不能升级更广权限。

**STEP 13 — VALIDATION**

文本模型遇图片必须换合格候选或Blocked；回退禁域/超预算测试；记录实际模型不能只记录首选。

**STEP 14 — STATE**

继承/固定/受限自动/无合格候选/正在回退/等待选择。

**STEP 15 — FAILURE / UNKNOWN**

没有视觉能力明确需要补足，不能删掉图片再自称成功。

**STEP 16 — PERMISSION / SECURITY**

有效可用=资源许可∩Employee授权∩Work scope∩数据外发∩能力支持。

**STEP 17 — PRODUCT PLACEMENT**

Employee能力→按用途模型；Company Settings默认；Work Header按需实际执行详情。

**STEP 18 — INTERACTION**

[选择工作用途]→模式/候选→[保存选择规则]→影响说明；失败[选择替代能力]只显示合法选项。

### C06 — 分层模型测试与高级参数

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO想知道模型真的能工作，也想调输出长度而不填错参数。

**STEP 2 — BUSINESS / WORK NEED**

认证/可发现/推理响应/附件/工具/结构化/streaming分层测试；参数按适配器合法集合。

**STEP 3 — REQUIRED CAPABILITY**

分层模型测试与高级参数

**STEP 4 — CURRENT CHECK**

部分支持：E04仅测试连接并发现模型；E17有特定云调用接受；E16/E03不足以证明每模型多能力。

**STEP 5 — FAILURE TEST**

200列表接口被当全能力可用，员工实际工作才报参数/工具错误。

**STEP 6 — CROSS-BUSINESS TEST**

研发Tool调用；写作长输出；数据JSON。共享。

**STEP 7 — PRODUCT OBJECT**

Test Result关联Connection/Model Profile与参数快照，复用Evidence。

**STEP 8 — USER-VISIBLE INFORMATION**

测试项/样本/费用可能性/结果/时延/实际模型/错误阶段/时间；参数当前继承值。

**STEP 9 — INPUT / EDITING**

选测试项；温度/topP/effort/maxOutput/timeout等按支持显示；不要求普通人预填。

**STEP 10 — DEFAULT**

温度/topP省略交给提供方；effort为该模型官方默认；输出上限受任务预算和硬限；不通用硬写0.2。

**STEP 11 — ADVANCED SETTINGS**

temperature或topP优先只改一种；effort仅枚举；超时/重试/Context/Tool policy分清网络与执行。

**STEP 12 — EFFECT**

参数改变使对应测试过期；不改Employee身份；工具权限不是temperature旁随意开关。

**STEP 13 — VALIDATION**

无真实用户数据的探针；不支持参数先本地拒绝；测试中止回执/超时不判失败无调用。

**STEP 14 — STATE**

未测试/正在测/部分通过/失败/未支持/过期。

**STEP 15 — FAILURE / UNKNOWN**

测试某一项失败只影响该能力；输出敏感日志脱敏；高费用测试提前明示不偷偷花钱。

**STEP 16 — PERMISSION / SECURITY**

测试使用者有连接及预算授权；无Secret输出。

**STEP 17 — PRODUCT PLACEMENT**

Model详情测试Main；高级参数折叠区；普通概览只[测试能否工作]及必要限制。

**STEP 18 — INTERACTION**

[测试]→选择低成本测试项/预计约束→运行→逐项结果→[应用到后续工作]；保失败结果，不把按钮存在当验收。

### C07 — Context预算、压缩与附件兼容

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究十份长PDF或持续讨论一周，模型窗口不能无限装入。

**STEP 2 — BUSINESS / WORK NEED**

选择相关引用、计量或估算、保留来源、受控摘要、截断可见及恢复。

**STEP 3 — REQUIRED CAPABILITY**

Context预算、压缩与附件兼容

**STEP 4 — CURRENT CHECK**

部分支持：E19 bounded retrieval/reference Accepted；模型context元数据不全E03；完整窗口预算未验证。

**STEP 5 — FAILURE TEST**

超长输入失败或静默截掉关键证据，产生无依据回答。

**STEP 6 — CROSS-BUSINESS TEST**

研究长文、小说长稿、研发仓库；共享。

**STEP 7 — PRODUCT OBJECT**

既有Context Package/Reference/Message与摘要产物，不建永久全量知识注入。

**STEP 8 — USER-VISIBLE INFORMATION**

当前引用/估算输入量/限制是否已知/省略项/摘要来源/是否影响任务。

**STEP 9 — INPUT / EDITING**

添加/移除引用；选择保留关键材料；允许或禁止此次外发压缩。

**STEP 10 — DEFAULT**

只相关必要引用；窗口未知采用保守分段并明确，不能宣称模型实际上限。

**STEP 11 — ADVANCED SETTINGS**

压缩阈值/检索额度等管理员高级；不让CEO手工拼token包。

**STEP 12 — EFFECT**

改变下一消息Context，不重写历史；更换模型重新验证输入兼容。

**STEP 13 — VALIDATION**

超限、多模态、失效引用、摘要误差回原文；重要来源被排除时不执行无声截断。

**STEP 14 — STATE**

可发送/准备中/接近限制/无法确认容量/需减少输入/摘要待确认。

**STEP 15 — FAILURE / UNKNOWN**

[查看未纳入内容]/[拆成多步处理]；不能用“上下文已优化”隐去删了什么。

**STEP 16 — PERMISSION / SECURITY**

摘要服务同受数据位置/范围授权；不可跨Business借私有Context。

**STEP 17 — PRODUCT PLACEMENT**

Composer引用区+Context Utility；Employee高级Context policy。

**STEP 18 — INTERACTION**

[查看本次上下文]→字段/来源/未纳入项→[保留这些资料]或[分步处理]→回同草稿。

### C08 — 费用、Rate Limit与资源预算

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO多业务同时工作，担心费用/429/配额耗尽。

**STEP 2 — BUSINESS / WORK NEED**

区分价格声明/实际账单/估计Usage，有限队列和预算条件。

**STEP 3 — REQUIRED CAPABILITY**

费用、Rate Limit与资源预算

**STEP 4 — CURRENT CHECK**

部分支持：唯一Usage来源已存在E02；E03 cost unknown；完整Provider限额与产品预算配置未验证。

**STEP 5 — FAILURE TEST**

全业务拥堵或花费超预期；估算被当实际利润。

**STEP 6 — CROSS-BUSINESS TEST**

研发长Agent与内容批量生成；共享。

**STEP 7 — PRODUCT OBJECT**

既有Usage ledger/预算授权/执行队列；不第二账本。

**STEP 8 — USER-VISIBLE INFORMATION**

费率单位/币种/来源日期/输入输出缓存计费、实耗与估算、429原因/下一尝试时间。

**STEP 9 — INPUT / EDITING**

Company或Work预算、Provider软并发限额；手填价格标用户估计，未设不显示0。

**STEP 10 — DEFAULT**

未知价格明确；不自动购买额度；429按明确Retry-After且有限等待；成本门槛使用用户政策。

**STEP 11 — ADVANCED SETTINGS**

按连接并发/RPM/TPM软限制；不允许用户覆盖服务硬额度。

**STEP 12 — EFFECT**

调预算作用未来动作及当前未提交步骤；不能回滚已发生费用。

**STEP 13 — VALIDATION**

限额1队列/429/超预算/缺计量/双回调去重；实际费用缺失仍未知。

**STEP 14 — STATE**

额度可用/额度未知/等待额度/预算需确认/价格过期。

**STEP 15 — FAILURE / UNKNOWN**

[查看用量]/[调整工作安排]/[前往提供方]，不在Curis自动充值。

**STEP 16 — PERMISSION / SECURITY**

预算扩大/付费资源须CEO；连接账单权限不能推定已获。

**STEP 17 — PRODUCT PLACEMENT**

Settings模型费用/并发；Insights成本；Work等待状态。

**STEP 18 — INTERACTION**

点击费用标签→来源Utility；[限制本次投入]Drawer→明确预算和后果→保存授权规则。

### C09 — External Agent生命周期与执行能力声明

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研发员工用Codex；分析员工调用外部代码Agent。

**STEP 2 — BUSINESS / WORK NEED**

安装检测、版本、认证、工作目录、权限映射、会话/取消/恢复能力可核验。

**STEP 3 — REQUIRED CAPABILITY**

External Agent生命周期与执行能力声明

**STEP 4 — CURRENT CHECK**

部分支持：E07 CodexCliAdapter有exec/resume、timeout且拒Full Computer Access；E16接线；不等完整Computer Use。

**STEP 5 — FAILURE TEST**

CLI存在但不能授权/续接，或停止只杀本地等待不停止远端任务。

**STEP 6 — CROSS-BUSINESS TEST**

研发与数据分析共同；外部Agent是共享执行能力。

**STEP 7 — PRODUCT OBJECT**

既有Agent Capability/Connection/Execution session。

**STEP 8 — USER-VISIBLE INFORMATION**

名称/来源/版本/安装与授权/支持动作/工作目录/原生权限映射/取消恢复真实能力。

**STEP 9 — INPUT / EDITING**

选择已安装Agent、路径（必要时）、工作目录和授权意图；模型配置由该Agent真实支持决定。

**STEP 10 — DEFAULT**

无最广电脑授权；缺安装/权限就待配置；不伪共享ChatGPT订阅等于API额度。

**STEP 11 — ADVANCED SETTINGS**

启动参数/超时/环境变量名引用；秘密用vault不普通字符串。

**STEP 12 — EFFECT**

升级/改目录影响后续执行；老session能否继续显示版本兼容。

**STEP 13 — VALIDATION**

合成目录任务→真实返回文件→cancel/resume/restart→权限拒绝；CLI版本输出不够。

**STEP 14 — STATE**

未安装/待授权/可执行某动作/unsupported/运行中/中断/无法续接。

**STEP 15 — FAILURE / UNKNOWN**

[查看安装说明]/[检查授权]/[从已保存结果重新安排]，不假Resume。

**STEP 16 — PERMISSION / SECURITY**

Native permission仅映射证据，不能声称外部Agent强于已授权限。

**STEP 17 — PRODUCT PLACEMENT**

Settings外部Agent与Employee能力Drawer；Work中原会话状态。

**STEP 18 — INTERACTION**

[添加外部Agent]→检测→授权说明→沙盒任务验证→[绑定给员工]→保存后返回原工作。

### C10 — Skill / Plugin供应与安全更新

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工需要文档导出Skill或业务Connector插件。

**STEP 2 — BUSINESS / WORK NEED**

来源/版本/许可/依赖/安装/绑定/更新差异/停用/撤销。

**STEP 3 — REQUIRED CAPABILITY**

Skill / Plugin供应与安全更新

**STEP 4 — CURRENT CHECK**

部分支持：E18 install/enable/explicit binding已bounded Accepted，外部候选与类型限制保留。

**STEP 5 — FAILURE TEST**

目录项目被当已会执行；更新插件偷偷扩大权限或破坏老工作。

**STEP 6 — CROSS-BUSINESS TEST**

写作导出和研发测试工具；共享供给，具体Skill可Domain。

**STEP 7 — PRODUCT OBJECT**

复用Capability catalog/binding；Plugin为打包供给物，不新Employee。

**STEP 8 — USER-VISIBLE INFORMATION**

用途/作者来源/版本/依赖/许可证/需权限/实际启用与使用者。

**STEP 9 — INPUT / EDITING**

选包/目标员工/允许能力；可更新版本但显式看差异。

**STEP 10 — DEFAULT**

不自动安装未知代码；不自动升级权限；已装不自动绑定全部员工。

**STEP 11 — ADVANCED SETTINGS**

安装路径/依赖诊断/校验信息高级；不是普通CEO首屏。

**STEP 12 — EFFECT**

停用影响未来工作；在途版本固定或安全暂停；不删历史。

**STEP 13 — VALIDATION**

安装失败回滚、恶意指令不授新权、更新新增权限不默许、卸载影响清单。

**STEP 14 — STATE**

候选/待安装/已安装未绑定/可用/需更新/不兼容/已停用。

**STEP 15 — FAILURE / UNKNOWN**

[查看缺失依赖]/[回退已验证版本]仅真实支持；否则保持旧版。

**STEP 16 — PERMISSION / SECURITY**

第三方文档为不可信数据；包不自行获得File/Browser访问。

**STEP 17 — PRODUCT PLACEMENT**

人才与能力发现；Settings公司能力维护；Employee绑定。

**STEP 18 — INTERACTION**

[引入能力]→依赖/权限预览→安装状态→[绑定]；[更新]展示版本差异并保留原授权。

### C11 — MCP服务、工具发现与工具级授权

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究用Web MCP，分析用数据库MCP，员工要知道能调用什么参数。

**STEP 2 — BUSINESS / WORK NEED**

远程/stdio连接、协议协商、tools/list schema、工具效果/权限、调用与错误。

**STEP 3 — REQUIRED CAPABILITY**

MCP服务、工具发现与工具级授权

**STEP 4 — CURRENT CHECK**

部分支持：E09 McpAdapter是单次initialize+tools/call(prompt)，注释明示完整发现/编排后续；不可当所有MCP可用。

**STEP 5 — FAILURE TEST**

只支持固定run(prompt)不能执行标准多工具MCP或准确校验输入。

**STEP 6 — CROSS-BUSINESS TEST**

Research检索和Data Analysis数据库；共享。

**STEP 7 — PRODUCT OBJECT**

Connector/MCP capability及工具描述引用，仍由Shared Work执行。

**STEP 8 — USER-VISIBLE INFORMATION**

服务名/传输/来源/授权/连接状态/工具名称与输入概要/副作用/使用者。

**STEP 9 — INPUT / EDITING**

remote URL或本地命令（二选）；需要的授权；逐工具启用；JSON参数只维护者高级。

**STEP 10 — DEFAULT**

新工具先未授权；readOnly等annotation是提示不安全保证；schema变更重验。

**STEP 11 — ADVANCED SETTINGS**

环境变量引用、传输协议、诊断、版本；不常驻原始JSON。

**STEP 12 — EFFECT**

新增工具不自动扩Employee权限；工具失效阻止依赖Work并保输入。

**STEP 13 — VALIDATION**

discover→安全只读tool→schema错误→权限拒绝→重连；remote OAuth不是stdio环境注入。

**STEP 14 — STATE**

待连接/已发现未授权/部分可用/调用中/协议不兼容。

**STEP 15 — FAILURE / UNKNOWN**

[重新发现工具]/[检查授权]；empty tools不是健康全通过。

**STEP 16 — PERMISSION / SECURITY**

每次工具调用按scope/资源/effect检查；MCP服务器返回文本不能指挥越权。

**STEP 17 — PRODUCT PLACEMENT**

Settings连接器→MCP详情；Employee可用工具选择；Work进展。

**STEP 18 — INTERACTION**

[添加MCP]→连接并发现→工具清单及权限→[启用所选]→绑定→原Work继续；不新工具台一级区。

### C12 — Web Search

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究员搜竞品、作者查事实，必须找到可打开且可引用的来源。

**STEP 2 — BUSINESS / WORK NEED**

查询/搜索通道/结果、时效、来源域、语言与失败后路由。

**STEP 3 — REQUIRED CAPABILITY**

Web Search

**STEP 4 — CURRENT CHECK**

未验证：wave1_seed有web-search目录定义，但目录只证明概念；本轮未找到真实Employee Search→Evidence验收。

**STEP 5 — FAILURE TEST**

模型凭记忆冒充最新网页，研究无法核对。

**STEP 6 — CROSS-BUSINESS TEST**

Content Growth选题与Research事实核查；全局共享基础能力。

**STEP 7 — PRODUCT OBJECT**

工具Capability + Search结果Reference；不是Global Object Search。

**STEP 8 — USER-VISIBLE INFORMATION**

查询/实际搜索Provider/结果标题URL摘要日期/已打开与仅摘要区别。

**STEP 9 — INPUT / EDITING**

默认语言随任务，可选时间范围/可信域；用户无需填搜索API参数。

**STEP 10 — DEFAULT**

只公网页搜索，不用已有登录态；结果先是线索，不自动成为事实。

**STEP 11 — ADVANCED SETTINGS**

搜索Provider、结果预算、域限制；任务必要字段在Work，不全部进Settings。

**STEP 12 — EFFECT**

改通道影响数据外发和搜索结果，原引用保留来源。

**STEP 13 — VALIDATION**

真实查询→打开原页→存来源；无结果、配额、失效URL、多语言反例。

**STEP 14 — STATE**

搜索中/有结果/无结果/通道不可用/结果过期。

**STEP 15 — FAILURE / UNKNOWN**

[换个查询]/[连接搜索能力]/[手动提供来源]；没有结果不输出假引用。

**STEP 16 — PERMISSION / SECURITY**

网络和查询外发授权；搜索结果提示词不可改变用户目标。

**STEP 17 — PRODUCT PLACEMENT**

Employee Web能力、Settings网络/搜索通道；Work真实活动。

**STEP 18 — INTERACTION**

员工[搜索网页]进展可展开查询结果；CEO[查看来源]到Reader/Browser，后[加入依据]保存Reference。

### C13 — Page Reader与网页Evidence

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究员找到文章，需要阅读正文和固定引用版本。

**STEP 2 — BUSINESS / WORK NEED**

读取HTML/PDF/动态页面、提取、可追溯引用、时间/访问范围/失效说明。

**STEP 3 — REQUIRED CAPABILITY**

Page Reader与网页Evidence

**STEP 4 — CURRENT CHECK**

部分支持：Library手动md/txt与Reference E19已有接受；网页读取/动态提取全链未验证。

**STEP 5 — FAILURE TEST**

只引用搜索摘要或页面改版后证据不可复核。

**STEP 6 — CROSS-BUSINESS TEST**

研究/写作/内容竞品都需要；共享。

**STEP 7 — PRODUCT OBJECT**

Source→Reference快照→Evidence引用，复用资料库。

**STEP 8 — USER-VISIBLE INFORMATION**

URL/标题/作者日期如有/读取时间/正文/提取完整性/引用片段/访问状态。

**STEP 9 — INPUT / EDITING**

选择保存的正文片段/用途/范围；不要求手工维护浏览历史。

**STEP 10 — DEFAULT**

浏览历史不自动进Knowledge；明确[保存来源]才持久化可引用内容。

**STEP 11 — ADVANCED SETTINGS**

抓取模式/渲染等待/快照保留策略；不可无限全站爬取。

**STEP 12 — EFFECT**

刷新新增来源版本，旧证据不替换；私有页面保存遵守范围。

**STEP 13 — VALIDATION**

正文与原页对照、截断/付费边界/动态加载/失效/引用返回。

**STEP 14 — STATE**

读取中/可读/仅摘要/部分提取/需登录/不可读取/快照过期。

**STEP 15 — FAILURE / UNKNOWN**

[打开原网页]/[手动提供材料]；不能绕过付费/权限。

**STEP 16 — PERMISSION / SECURITY**

合法站点访问，敏感页面截图需范围控制，不保存Cookie。

**STEP 17 — PRODUCT PLACEMENT**

Work Reader Utility/maximize；Library来源阅读Main。

**STEP 18 — INTERACTION**

[打开来源]→标读取范围→[保存为依据]选择scope→回Work同位置，引用固定版本。

### C14 — 交互Browser与研发页面验证

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研发员工启动localhost，点表单，看失败，再修改代码。

**STEP 2 — BUSINESS / WORK NEED**

导航/点击/输入/DOM或可访问树/截图/Console与脱敏Network、受控session、证据回流。

**STEP 3 — REQUIRED CAPABILITY**

交互Browser与研发页面验证

**STEP 4 — CURRENT CHECK**

未验证：seed Playwright与Tauri生成WebView权限只是定义；本轮已检代码未证明真实Curis Browser工具链。

**STEP 5 — FAILURE TEST**

代码能build但页面不能打开/操作，研发验收是假成功。

**STEP 6 — CROSS-BUSINESS TEST**

研发localhost与外部业务后台操作；研究动态页面。共享基础能力，DevTools是专业扩展。

**STEP 7 — PRODUCT OBJECT**

Browser执行能力+Work-owned browsing session+Evidence；复用工具执行，不新Browser Runtime真源。

**STEP 8 — USER-VISIBLE INFORMATION**

当前URL/页面标题/工作scope/账号环境/员工当前动作/连接状态/最后截图/可接管状态。

**STEP 9 — INPUT / EDITING**

选择安全运行环境、允许域/localhost、必要人工接管；不要求每次手工输CDP端口。

**STEP 10 — DEFAULT**

隔离研究/测试会话；员工后台浏览有可见活动入口；默认不占Main抢焦点。

**STEP 11 — ADVANCED SETTINGS**

DevTools Console/Network只研发模式按需；隐藏Authorization/Cookie/敏感请求正文；连接桥诊断高级。

**STEP 12 — EFFECT**

切URL不换Work scope；换账号环境须重新权限检查；关闭观察窗口不停止执行。

**STEP 13 — VALIDATION**

隔离demo站导航→输入→断言→截图→故意console错误→脱敏Network→证据→修复再测；非仅截图。

**STEP 14 — STATE**

启动中/连接/浏览中/等待页面/等待你接管/桥断开/站点拒绝/结果未知。

**STEP 15 — FAILURE / UNKNOWN**

[查看浏览现场]/[接管操作]/[重新连接浏览器]；插件未连不能显示员工已完成点击。

**STEP 16 — PERMISSION / SECURITY**

Browser工具受site/action/Work约束；支付/发布/删除需既有授权或Decision；不读Cookie。

**STEP 17 — PRODUCT PLACEMENT**

Settings Web与电脑权限；Work[查看浏览现场]Utility/maximize；研发调试可专业Main。

**STEP 18 — INTERACTION**

[启用网页操作]→选择隔离Browser或授权插件桥→检查→测试页→保存；员工任务中点[查看浏览现场]观察，接管后显式[交还员工]。

### C15 — Browser账号环境隔离与人工登录

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

同一员工运营两个同平台账号，不能误用CEO个人账号。

**STEP 2 — BUSINESS / WORK NEED**

登录环境与外部Account明确绑定，多员工使用同环境需权限和互斥。

**STEP 3 — REQUIRED CAPABILITY**

Browser账号环境隔离与人工登录

**STEP 4 — CURRENT CHECK**

未验证：没有当前可追溯浏览器账号环境隔离/接管/恢复验收；不可用本机Codex的浏览器权限当Curis能力。

**STEP 5 — FAILURE TEST**

错误账号发内容、泄露跨Business会话、互相打断登录。

**STEP 6 — CROSS-BUSINESS TEST**

内容两个账号与研发测试/生产账号；共享。

**STEP 7 — PRODUCT OBJECT**

已有Connection/Account下的浏览环境引用候选；不按Employee复制Secret。

**STEP 8 — USER-VISIBLE INFORMATION**

环境显示名/站点/已验证账号身份/绑定用途/使用者/占用者/最后登录检查。

**STEP 9 — INPUT / EDITING**

创建隔离环境；正常网页登录；选择现有合法账号环境；不导入Cookie文件。

**STEP 10 — DEFAULT**

不共享CEO主浏览器全Session；按外部账号环境隔离；同环境同时仅一个变更执行者，其他只读/等待。

**STEP 11 — ADVANCED SETTINGS**

会话保留时限/站点白名单/失效恢复；不暴露storageState内容。

**STEP 12 — EFFECT**

移除环境不删除平台账号；退出登录影响依赖Work；已有history可引用但敏感快照按权限。

**STEP 13 — VALIDATION**

A/B账号标识核验→跨员工并发→token失效→手工登录→恢复且不重发副作用。

**STEP 14 — STATE**

未登录/身份待核验/已登录/被占用/需重登录/到期/撤销。

**STEP 15 — FAILURE / UNKNOWN**

身份不明必须Blocked；[登录此账号]/[等待当前操作]/[选择其他环境]，不能自动切个人账号。

**STEP 16 — PERMISSION / SECURITY**

MFA/CAPTCHA/敏感重新授权交CEO；账号访问不等任意发布许可。

**STEP 17 — PRODUCT PLACEMENT**

Settings连接与浏览环境；Account连接详情；Work接管动作包。

**STEP 18 — INTERACTION**

[创建浏览环境]→名称/用途→[打开登录页]→用户登录→[核对账号]→绑定→回原任务；不记录凭证。

### C16 — Computer Use与OS权限

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

网页外的桌面应用需要点击或读取屏幕，研发/内容员工不能凭有模型就会操作。

**STEP 2 — BUSINESS / WORK NEED**

区分模型规划、执行适配器、OS辅助功能/截图许可、授权动作与人接管。

**STEP 3 — REQUIRED CAPABILITY**

Computer Use与OS权限

**STEP 4 — CURRENT CHECK**

部分支持：E07电脑意图映射仅read-only/workspace-write，Full Computer Access明确unsupported；全桌面操作未验证。

**STEP 5 — FAILURE TEST**

把Computer Use模型能力误认为OS访问已开，工作停在“已授权”假状态。

**STEP 6 — CROSS-BUSINESS TEST**

内容素材桌面App与数据表格App；共享可选执行基础，不所有员工默认需要。

**STEP 7 — PRODUCT OBJECT**

Employee capability + host-specific Permission + Execution；不新增员工类别。

**STEP 8 — USER-VISIBLE INFORMATION**

本机/远端设备、读取屏幕/控制输入/文件权限分别状态、占用者、实际可用/未验证、接管。

**STEP 9 — INPUT / EDITING**

按任务申请具体OS权限；用户可选择只读屏幕或控制；无全部自动允许默认。

**STEP 10 — DEFAULT**

未授屏幕/控制；操作前告知范围，真人使用电脑时按冲突策略暂停。

**STEP 11 — ADVANCED SETTINGS**

动作速率/显示器选择/诊断；不能在普通页堆权限key。

**STEP 12 — EFFECT**

撤销立即阻止后续动作，已发生外部变化不回滚；跨设备权限独立。

**STEP 13 — VALIDATION**

屏幕测试→无敏感窗口操作→取消→人为移动焦点→OS撤销→恢复，逐层验证。

**STEP 14 — STATE**

OS未授权/适配器未安装/模型不支持/可用/占用/接管/撤销。

**STEP 15 — FAILURE / UNKNOWN**

[打开系统设置]不等[已授权]；回来[重新检查]，无法查状态写unknown。

**STEP 16 — PERMISSION / SECURITY**

OS系统prompt正常流程；不自动全盘、全屏、常驻记录；显式授权才操作。

**STEP 17 — PRODUCT PLACEMENT**

Settings权限与安全/浏览与电脑能力；Employee仅绑定；Work显示真实动作。

**STEP 18 — INTERACTION**

[允许此次桌面操作]→权限说明→系统授权→独立检查→测试→继续原Work；接管/交还清楚。

### C17 — 文件与目录的按需授权

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研发员工修改本地仓库，分析员工读取桌面CSV；CEO只希望授权这些资料。

**STEP 2 — BUSINESS / WORK NEED**

选择真实文件或目录，确认规范化路径、读写范围、存续时间和引用方式。

**STEP 3 — REQUIRED CAPABILITY**

文件与目录的按需授权

**STEP 4 — CURRENT CHECK**

部分支持：E08有路径边界和受控读写；E19有资料引用；完整用户目录授权、符号链接及跨设备路径恢复尚未验证。

**STEP 5 — FAILURE TEST**

员工找不到文件，或把选择一个文件误解成整个磁盘可读。

**STEP 6 — CROSS-BUSINESS TEST**

研发仓库和数据分析输入目录均需要；写作素材同用。共享能力。

**STEP 7 — PRODUCT OBJECT**

现有Workspace资源引用、文件授权和Reference；本地目录不是新的Business，也不自动等于Knowledge。

**STEP 8 — USER-VISIBLE INFORMATION**

名称/类型/大小/修改时间/设备/目录路径/权限/被哪些Work使用/外部位置是否在线。

**STEP 9 — INPUT / EDITING**

通过原生文件选择器选文件或文件夹；选择只读或指定写入子目录；更换位置需重新验证。

**STEP 10 — DEFAULT**

读取附件只读；写入独立输出目录；授权以明确任务或Workspace为界，不继承全盘访问。

**STEP 11 — ADVANCED SETTINGS**

排除规则、单文件大小限制、符号链接处理；普通用户无需编辑glob才能读一个文件。

**STEP 12 — EFFECT**

撤销阻止后续读取和写入，不声称能从已发送模型的上下文收回文件；历史引用留下不可访问状态。

**STEP 13 — VALIDATION**

选择目录外文件、符号链接指向外部、目录移动、磁盘卸载、权限撤销；检查拒绝而不是静默换目录。

**STEP 14 — STATE**

未选择/检查中/只读/可写/离线/位置失效/授权撤销/受系统限制。

**STEP 15 — FAILURE / UNKNOWN**

清楚区分路径不存在、无权限、设备不在线；提供重新定位或重新授权，不能创建空文件冒充恢复。

**STEP 16 — PERMISSION / SECURITY**

规范化路径后验证每次访问；排除凭证和系统目录；OS权限与产品范围分别检查。

**STEP 17 — PRODUCT PLACEMENT**

Workspace资源区、Composer附件、Settings文件与存储；Employee详情只显示有效范围。

**STEP 18 — INTERACTION**

[添加本地资料]→原生选择器→范围预览→[只读使用]或[允许输出]→引用卡；[更换位置]重新检查后保留原引用关系。

### C18 — 工作文件、版本与外部编辑冲突

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工生成报告后CEO在外部编辑器修改，员工继续执行不能覆盖CEO的新内容。

**STEP 2 — BUSINESS / WORK NEED**

读取版本指纹，提交修改前比较；预览差异、冲突保留、保存结果版本和位置。

**STEP 3 — REQUIRED CAPABILITY**

工作文件、版本与外部编辑冲突

**STEP 4 — CURRENT CHECK**

部分支持：E08原子写入及hash边界；E19资料生命周期；完整外部编辑冲突处理和用户版本恢复未验证。

**STEP 5 — FAILURE TEST**

后写覆盖先写；Conversation声称结果已更新而文件内容仍旧。

**STEP 6 — CROSS-BUSINESS TEST**

研发源文件与写作长稿都存在；数据工作簿也有。共享文件能力，代码合并规则是专业扩展。

**STEP 7 — PRODUCT OBJECT**

Work输出/Result版本/文件引用；Working File与发布或验收Result分开，不把每次自动保存变成新成果。

**STEP 8 — USER-VISIBLE INFORMATION**

当前版本/作者来源/保存时间/磁盘位置/未保存/外部已修改/差异摘要/关联Work。

**STEP 9 — INPUT / EDITING**

重命名、选择保存位置、编辑可支持格式、接受部分差异；不支持的格式用外部编辑器打开。

**STEP 10 — DEFAULT**

不覆盖外部变化；新输出保留原输入；保存与验收分开。

**STEP 11 — ADVANCED SETTINGS**

版本保留时长、较大二进制策略、比较工具；不承诺任意二进制自动合并。

**STEP 12 — EFFECT**

恢复旧版本产生新的可追溯版本；历史Evidence保持原版本，不能跟着当前文件静默变化。

**STEP 13 — VALIDATION**

读A→外部写B→员工提交C应冲突；取消后B不丢；重新载入再提交；磁盘满保存不显示成功。

**STEP 14 — STATE**

未修改/已修改未保存/保存中/已保存/外部变更/冲突/只读/保存失败。

**STEP 15 — FAILURE / UNKNOWN**

[查看差异]/[另存副本]/[重新载入]；对无法比较的二进制明确不支持合并。

**STEP 16 — PERMISSION / SECURITY**

文件写入授权，打开外部App只传所选路径；覆盖确认绑定当前版本，不能复用过期确认。

**STEP 17 — PRODUCT PLACEMENT**

Artifact文件预览Main、版本Utility、Workspace文件列表。

**STEP 18 — INTERACTION**

点击文件→预览→[编辑]→保存前校验；冲突面板显示两方时间/来源→选择另存或重新编辑→回同Work。

### C19 — Terminal与受控进程执行

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研发员工运行测试；分析员工运行Python脚本，需要看到进程是否结束以及真实错误。

**STEP 2 — BUSINESS / WORK NEED**

明确主机、工作目录、解释器、环境依赖、命令权限、输出、退出码和取消进程树。

**STEP 3 — REQUIRED CAPABILITY**

Terminal与受控进程执行

**STEP 4 — CURRENT CHECK**

部分支持：E08只有登记测试命令；E07 Codex可用workspace-write沙箱；通用Terminal、安装依赖与全过程验收未验证。

**STEP 5 — FAILURE TEST**

文件生成后无法测试；只凭输出片段判断成功；子进程继续占资源。

**STEP 6 — CROSS-BUSINESS TEST**

研发测试和数据分析脚本重复出现。共享执行能力，语言工具链按任务安装，不默认所有员工具备Shell。

**STEP 7 — PRODUCT OBJECT**

现有Execution及其Tool activity/日志；Terminal是执行观察或授权入口，不建立第二任务系统。

**STEP 8 — USER-VISIBLE INFORMATION**

命令摘要/主机/cwd/运行身份/开始时间/耗时/退出码/输出截断提示/实际授权范围。

**STEP 9 — INPUT / EDITING**

设置受控工作目录、选择登记命令或审查拟执行命令；依赖安装说明来源和变更范围。

**STEP 10 — DEFAULT**

不要求管理员；独立环境；禁止把模型文本直接作为无约束Shell；不自动继承用户全部环境变量。

**STEP 11 — ADVANCED SETTINGS**

环境变量仅显式非敏感键或Credential引用；超时、输出上限、网络和可执行程序策略由专业用户配置。

**STEP 12 — EFFECT**

目录或环境改变使原结果不可直接复用；停止需处理进程树；安装影响仅所选环境。

**STEP 13 — VALIDATION**

成功/非零退出/挂起/大量输出/超时/子进程/取消/重启后遗留进程；保留退出原因而非统一失败。

**STEP 14 — STATE**

待授权/准备环境/运行/等待输入/完成/非零退出/停止中/已停止/结果未知。

**STEP 15 — FAILURE / UNKNOWN**

缺解释器给检查或安装入口；交互输入回到用户；超时后先确认进程状态，不自动重复有副作用命令。

**STEP 16 — PERMISSION / SECURITY**

命令与文件、网络、设备权限同时受限；sudo、破坏性操作和外部部署有独立授权边界。

**STEP 17 — PRODUCT PLACEMENT**

Work工具活动展开日志；Workspace研发工具Main；Employee能力绑定只选择可用执行器。

**STEP 18 — INTERACTION**

[运行检查]→展示命令及影响→已有授权则执行→流式输出→退出码→[查看失败位置]/[再次运行]；再次运行建立新尝试。

### C20 — Git修改、审查与交付权限分离

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研发员工修复问题，CEO需要知道改了哪些文件并决定是否进入真实仓库。

**STEP 2 — BUSINESS / WORK NEED**

仓库识别、基线和dirty状态、隔离修改、差异审查、测试、提交与push/deploy分别授权。

**STEP 3 — REQUIRED CAPABILITY**

Git修改、审查与交付权限分离

**STEP 4 — CURRENT CHECK**

部分支持：E08 git_read只有status/diff/diff_check；当前Curis完整分支、接受拒绝、提交push交付闭环未验证。

**STEP 5 — FAILURE TEST**

员工覆盖现有修改；把测试通过当已部署；拒绝差异时误删用户文件。

**STEP 6 — CROSS-BUSINESS TEST**

研发应用与写作版本化内容仓库共同需要。Git本身为专业能力；变更审查与外发许可是共享。

**STEP 7 — PRODUCT OBJECT**

Workspace仓库资源、Work变更集、Result与验收Decision；不把分支当Business。

**STEP 8 — USER-VISIBLE INFORMATION**

仓库/工作目录/分支/基线commit/原有修改/员工修改/测试证据/已提交未推送/远端状态是否已核验。

**STEP 9 — INPUT / EDITING**

选择仓库和基线；勾选接受差异；提交信息；远端目标需实际可见且获授权。

**STEP 10 — DEFAULT**

保留原有dirty改动；有隔离环境时使用独立工作目录；不自动commit/push/deploy。

**STEP 11 — ADVANCED SETTINGS**

worktree、签名、rebase等专业动作仅能力支持时显示；不让普通CEO先学Git才能收报告。

**STEP 12 — EFFECT**

接受改动只影响当前工作文件；commit/push/deploy是不同外部效果，任何一步不能替下一步报告完成。

**STEP 13 — VALIDATION**

存在用户未提交更改、分支变化、冲突、测试失败、远端拒绝、push超时；恢复不得reset用户工作树。

**STEP 14 — STATE**

待变更/修改中/待审查/部分接受/冲突/测试失败/已接受/已提交/交付未知。

**STEP 15 — FAILURE / UNKNOWN**

[查看冲突]/[另存修改]/[重新核验远端]；不因网络超时自动再次发布。

**STEP 16 — PERMISSION / SECURITY**

文件允许范围和仓库写权限；远端发布授权绑定仓库分支及变更版本；凭证走已有连接。

**STEP 17 — PRODUCT PLACEMENT**

研发Workspace专业工具、Work变更预览、Result验收。

**STEP 18 — INTERACTION**

[查看修改]→按文件diff→接受或拒绝员工拥有的改动→测试→形成Result；有授权再进入[提交]/[交付]并显示各自回执。

### C21 — 本地预览服务与可验证页面

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工启动应用后，CEO要打开真实页面并知道其对应哪次修改。

**STEP 2 — BUSINESS / WORK NEED**

启动进程、端口分配、就绪探针、浏览器连接、源码版本及停止清理。

**STEP 3 — REQUIRED CAPABILITY**

本地预览服务与可验证页面

**STEP 4 — CURRENT CHECK**

部分支持：E14能启动Curis自身sidecar，不证明用户项目Preview；E08登记命令不能证明完整网页验证。

**STEP 5 — FAILURE TEST**

服务启动日志有URL，但端口被占或浏览器在不同主机；测试根本未打开目标版本。

**STEP 6 — CROSS-BUSINESS TEST**

研发应用与写作静态站预览共享；项目构建命令是Domain配置。

**STEP 7 — PRODUCT OBJECT**

现有Execution的预览端点与Result证据引用；不用新建发布系统。

**STEP 8 — USER-VISIBLE INFORMATION**

项目/版本/所在设备/本地地址/端口/就绪状态/进程/访问范围/截图时间。

**STEP 9 — INPUT / EDITING**

选择项目登记的启动命令；端口自动分配，可专业覆盖；网络暴露必须另选。

**STEP 10 — DEFAULT**

仅loopback；没有就绪验证不显示可用；不自动开公网隧道。

**STEP 11 — ADVANCED SETTINGS**

健康路径、启动超时、环境变量引用、端口；属于项目工具高级。

**STEP 12 — EFFECT**

重启后地址可能变；旧截图仍标旧版本，不能自动替换验收证据。

**STEP 13 — VALIDATION**

端口占用、进程早退、200空壳、跨主机localhost、重启、停止；验证实际DOM及操作。

**STEP 14 — STATE**

未启动/启动中/端口冲突/就绪/页面错误/停止/地址失效。

**STEP 15 — FAILURE / UNKNOWN**

[查看启动日志]/[换端口]/[重新打开]；区分服务可访问与功能测试通过。

**STEP 16 — PERMISSION / SECURITY**

执行与浏览授权同时满足；公开访问不由预览授权推导。

**STEP 17 — PRODUCT PLACEMENT**

Workspace工具Main和Work[打开预览]；浏览现场可展开。

**STEP 18 — INTERACTION**

启动→探针→打开页面→执行指定交互→截图和错误→关联版本结果；关闭面板不等于停止服务。

### C22 — 文档解析、OCR与导出格式

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究员工收到扫描PDF，写作员工需交付可编辑文档。

**STEP 2 — BUSINESS / WORK NEED**

识别格式、提取文本和版面、按页来源定位、OCR质量、生成目标格式并回读。

**STEP 3 — REQUIRED CAPABILITY**

文档解析、OCR与导出格式

**STEP 4 — CURRENT CHECK**

部分支持：E19接受范围为md/txt；PDF/OCR/Office等完整转换验收未验证。

**STEP 5 — FAILURE TEST**

把扫描页当空文档，或交付改扩展名的伪文档。

**STEP 6 — CROSS-BUSINESS TEST**

研究论文和写作出版共用；数据表格同需结构解析。共享，排版标准为Domain。

**STEP 7 — PRODUCT OBJECT**

文件Reference、解析产物、Evidence页码、Result导出版本。

**STEP 8 — USER-VISIBLE INFORMATION**

原始格式/页数/解析方式/失败页/置信局限/可编辑性/导出格式和版本。

**STEP 9 — INPUT / EDITING**

选择文件、OCR语言、输出格式；保留原件；人工更正引用定位。

**STEP 10 — DEFAULT**

优先本地文本解析；扫描才OCR；不静默向云端传全量文件。

**STEP 11 — ADVANCED SETTINGS**

OCR引擎、语言包、分辨率、版式保留；只专业用户按需要展开。

**STEP 12 — EFFECT**

重解析不改原件；更换引擎影响成本、隐私、引用定位，旧证据保持原快照。

**STEP 13 — VALIDATION**

加密、损坏、扫描、混排、超大表格；导出用实际读取器检查内容结构和缺失。

**STEP 14 — STATE**

待解析/解析中/部分成功/需密码/格式不支持/导出中/导出失败。

**STEP 15 — FAILURE / UNKNOWN**

逐页列未读取范围；密码由安全人工流程处理；不生成“完整阅读”假结论。

**STEP 16 — PERMISSION / SECURITY**

文件授权与云OCR授权独立；宏不执行，外部引用默认不拉取。

**STEP 17 — PRODUCT PLACEMENT**

附件预处理、文件预览、Result[导出]；Settings仅配置可用解析能力。

**STEP 18 — INTERACTION**

添加→格式检测→预览解析质量→选需要的页→引用；导出选格式→生成→回读检查→下载或打开。

### C23 — 数据连接与可信快照

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

分析员工查询数据库，CEO需要分辨没有数据、无权限和查询出错。

**STEP 2 — BUSINESS / WORK NEED**

连接、schema发现、只读查询、参数化、大小上限、快照与时间口径。

**STEP 3 — REQUIRED CAPABILITY**

数据连接与可信快照

**STEP 4 — CURRENT CHECK**

未验证：现有通用Connector/MCP适配不等于数据库只读与分析验收；本轮不连接真实数据库。

**STEP 5 — FAILURE TEST**

分析基于部分或旧数据得出完整经营结论；误执行写语句。

**STEP 6 — CROSS-BUSINESS TEST**

数据分析和内容效果分析共用；业务指标定义为Domain。

**STEP 7 — PRODUCT OBJECT**

Connection、数据源引用、查询执行、Evidence快照；不新增经营事实账本。

**STEP 8 — USER-VISIBLE INFORMATION**

数据源/账号角色/可读范围/schema/查询时间/数据时间/行数/截断/时区/采样及来源。

**STEP 9 — INPUT / EDITING**

选已授权表/参数/时间窗；专业SQL需读权限与限额验证。

**STEP 10 — DEFAULT**

只读；有限行数和超时；截断明确；不同源不自动拼身份信息。

**STEP 11 — ADVANCED SETTINGS**

分页、查询预算、schema缓存、脱敏规则；普通用户用目标和时间窗。

**STEP 12 — EFFECT**

时间窗改变指标口径；刷新产生新快照，旧结论保留当时依据。

**STEP 13 — VALIDATION**

权限拒绝、零行、超时、分页、重复记录、时区边界、缺字段和schema变化。

**STEP 14 — STATE**

未连接/检查中/可查询/权限不足/执行中/部分数据/过期/失败。

**STEP 15 — FAILURE / UNKNOWN**

展示“零条记录”而非“业务为零”；缺数据不能补成0；提供调整范围或重新授权。

**STEP 16 — PERMISSION / SECURITY**

凭证引用；读写角色分离；行列权限由真实服务落实，模型不能扩大范围。

**STEP 17 — PRODUCT PLACEMENT**

Workspace资料或数据源、Insights来源检查、连接Settings。

**STEP 18 — INTERACTION**

选择数据源→检查可读结构→确认查询范围→运行→显示完整性→生成图表/Result并附快照。

### C24 — 本地与云执行及数据外发边界

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO允许研究公开网页，但客户材料只能留在本机。

**STEP 2 — BUSINESS / WORK NEED**

识别实际执行位置、模型位置、工具网络和每次外发Context，不能只贴本地标签。

**STEP 3 — REQUIRED CAPABILITY**

本地与云执行及数据外发边界

**STEP 4 — CURRENT CHECK**

部分支持：E03有local/cloud标签，E08有网络隔离边界；完整跨模型工具数据流策略验收未验证。

**STEP 5 — FAILURE TEST**

本地Agent调用云模型泄露资料；fallback绕开原本地域约束。

**STEP 6 — CROSS-BUSINESS TEST**

研究客户文档与研发私有仓库共用；所有Business基础。

**STEP 7 — PRODUCT OBJECT**

既有执行授权和数据范围策略，绑定Connection/Work；不建立第二权限系统。

**STEP 8 — USER-VISIBLE INFORMATION**

执行主机/实际模型服务/材料分类/外发目标/受限原因/是否使用fallback。

**STEP 9 — INPUT / EDITING**

允许的服务或区域、可外发资料范围；选择本次仅本地能力。

**STEP 10 — DEFAULT**

未知目标不发送受限数据；缺本地能力则等待，不自动改云服务。

**STEP 11 — ADVANCED SETTINGS**

地域规则、代理出口和保留策略引用；不要求普通CEO配置网络实现细节。

**STEP 12 — EFFECT**

策略缩紧影响新请求和待发送内容；已外发数据不能声称自动收回。

**STEP 13 — VALIDATION**

本地执行器+云模型、云OCR、工具上传、fallback换地区；逐条校验实际目标。

**STEP 14 — STATE**

可执行/需授权/缺合规能力/待检查/已阻止/运行中。

**STEP 15 — FAILURE / UNKNOWN**

[选择允许的能力]/[减少资料]/[请求授权]；unknown不能显示符合政策。

**STEP 16 — PERMISSION / SECURITY**

Company策略上限、Work具体范围、外部服务协议；权限需可撤销。

**STEP 17 — PRODUCT PLACEMENT**

Settings隐私与执行位置、Work上下文检查、Employee有效能力状态。

**STEP 18 — INTERACTION**

选择工作资料→预检外发→说明目标与必要范围→符合已授权策略才运行→记录实际目标。

### C25 — 后台执行、退出与断点恢复

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工工作20分钟，CEO关闭窗口或电脑睡眠，次日回来要知道发生了什么。

**STEP 2 — BUSINESS / WORK NEED**

区分关闭面板/关闭窗口/退出App/睡眠/进程失败；持久化Work与执行位置，恢复核验外部效果。

**STEP 3 — REQUIRED CAPABILITY**

后台执行、退出与断点恢复

**STEP 4 — CURRENT CHECK**

部分支持：E02有真实General Work暂停重启恢复接受；E14关闭窗口或退出会kill sidecar，不能承诺关闭后常驻执行。

**STEP 5 — FAILURE TEST**

UI消失后任务停了却显示仍运行；恢复重复调用造成两次外部操作。

**STEP 6 — CROSS-BUSINESS TEST**

研发长测试与研究长任务共用。Company基础，外部云执行依Provider。

**STEP 7 — PRODUCT OBJECT**

现有Work/Execution尝试/检查点/Attention；不新建后台任务账本。

**STEP 8 — USER-VISIBLE INFORMATION**

运行地点/当前阶段/最后心跳/可否离线继续/暂停原因/待恢复项/未知外部结果。

**STEP 9 — INPUT / EDITING**

选择关闭时暂停或已有受支持后台策略；恢复前确认变化的上下文。

**STEP 10 — DEFAULT**

本机退出不承诺继续；关闭前提示受影响Work；恢复先查状态，不从头盲重跑。

**STEP 11 — ADVANCED SETTINGS**

保活、超时、检查点保留仅支持执行器开放；不能用一个开关假造后台能力。

**STEP 12 — EFFECT**

改变只作用于后续关闭行为；正在外部执行的任务需查询真实服务状态。

**STEP 13 — VALIDATION**

关面板、关窗、正常退出、强制结束、睡眠、断网、重新启动；核验重复副作用。

**STEP 14 — STATE**

运行/暂停中/已暂停/外部继续/心跳丢失/待核验/可恢复/不可恢复。

**STEP 15 — FAILURE / UNKNOWN**

显示最后确认状态与时间；提供核验、从安全步骤继续或保留部分结果。

**STEP 16 — PERMISSION / SECURITY**

恢复使用当前权限，过期授权不可沿用；后台不能绕过新的审批。

**STEP 17 — PRODUCT PLACEMENT**

全局工作状态、Attention、Work详情、Settings后台行为。

**STEP 18 — INTERACTION**

关闭时显示影响摘要→选择支持动作→重开进入恢复清单→核验→继续同Work的新执行尝试。

### C26 — 排程、触发和经营节奏

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO说晚上八点发布、明天取数，而不是现在执行。

**STEP 2 — BUSINESS / WORK NEED**

持久触发时间、时区、条件、执行主机可用性、授权有效性和错过处理。

**STEP 3 — REQUIRED CAPABILITY**

排程、触发和经营节奏

**STEP 4 — CURRENT CHECK**

部分支持：E13有后台调度；E11及E12一条节奏路径默认SimulatedExecutor；不能宣称真实定时业务交付完成。

**STEP 5 — FAILURE TEST**

定时卡片存在但不执行；电脑关机错过；补跑重复发布。

**STEP 6 — CROSS-BUSINESS TEST**

内容发布和数据日报重复；研发夜间测试也用。共享调度，发布API为Domain。

**STEP 7 — PRODUCT OBJECT**

既有Cycle/Work排程和触发记录；不另建一套Work。

**STEP 8 — USER-VISIBLE INFORMATION**

下一次执行绝对时间及时区/条件/依赖/运行位置/最近结果/错过原因/生效授权。

**STEP 9 — INPUT / EDITING**

时间、重复规则、结束条件、错过策略；条件触发仅从已验证事件源选择。

**STEP 10 — DEFAULT**

不默默补跑有副作用动作；本机不可常驻时明确需开机；无执行器不允许显示已就绪。

**STEP 11 — ADVANCED SETTINGS**

重叠策略、抖动、补跑窗口、事件去重；普通界面保留时间、对象和条件。

**STEP 12 — EFFECT**

修改产生新版本，已开始尝试不被时间编辑回滚；停用只阻止新触发。

**STEP 13 — VALIDATION**

跨时区、夏令时、关机错过、重复事件、运行超时与下一周期重叠、授权过期。

**STEP 14 — STATE**

草稿/待条件/已排程/需能力/已错过/运行/失败/暂停/结束。

**STEP 15 — FAILURE / UNKNOWN**

[现在核验]/[跳过此次]/[重新安排]；真实运行回执与模拟预演不同标签。

**STEP 16 — PERMISSION / SECURITY**

创建排程不等提前授权所有未来外部动作；执行时重新检查权限、预算及目标。

**STEP 17 — PRODUCT PLACEMENT**

Business Cycle及Work时间控件；Settings只存个人时区和默认行为。

**STEP 18 — INTERACTION**

[安排时间]→时间及可运行条件→预览未来触发→保存；点击错过记录查看原因后选择是否补跑。

### C27 — Attention与通知投递

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO离开三天后回来，希望先处理登录失效和需决策事项，而非逐条翻聊天。

**STEP 2 — BUSINESS / WORK NEED**

持久Attention、重要性、去重、站内入口、可选OS通知和投递状态。

**STEP 3 — REQUIRED CAPABILITY**

Attention与通知投递

**STEP 4 — CURRENT CHECK**

部分支持：E02有Attention与日常工作闭环；OS通知、quiet hours、digest及移动投递未验证。

**STEP 5 — FAILURE TEST**

阻塞无人知道；普通完成提示淹没必须人工决策。

**STEP 6 — CROSS-BUSINESS TEST**

内容登录失效与研发测试阻塞共享；所有长期Business需要。

**STEP 7 — PRODUCT OBJECT**

复用Attention关联Work/Decision；通知只是投递，不是另一套待办。

**STEP 8 — USER-VISIBLE INFORMATION**

标题/为什么需要你/责任对象/期限/影响/已读与已解决分别状态/来源/最后投递。

**STEP 9 — INPUT / EDITING**

个人通知渠道、免打扰时间、摘要频率；决定是否处理具体Attention。

**STEP 10 — DEFAULT**

站内保留；OS需正常授权；只对需行动和关键完成发通知；移动渠道没有验证能力就不显示已启用。

**STEP 11 — ADVANCED SETTINGS**

渠道路由和升级规则由真实多用户需求启用；不默认增加短信或第三方账号。

**STEP 12 — EFFECT**

静音不解决阻塞；已读不等于已处理；修改只影响新投递。

**STEP 13 — VALIDATION**

系统拒绝通知、重复事件、静音、跨设备点击、目标归档；站内仍可恢复处理。

**STEP 14 — STATE**

未读/已读/待处理/已解决/投递中/投递失败/渠道未授权。

**STEP 15 — FAILURE / UNKNOWN**

说明站内已记录但OS未送达；提供系统设置或回站内，不自动发外部消息。

**STEP 16 — PERMISSION / SECURITY**

锁屏默认隐藏敏感内容；渠道配置和外部收件人要明确授权。

**STEP 17 — PRODUCT PLACEMENT**

CEO工作台Attention、全局通知入口、个人Settings。

**STEP 18 — INTERACTION**

点击通知→定位原Work决策→完成动作→Attention解决；返回原筛选和位置。

### C28 — 凭证、连接与账号生命周期

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

连接有效一个月后失效，CEO换Key；员工应恢复工作而不暴露或复制Secret。

**STEP 2 — BUSINESS / WORK NEED**

安全保存、引用、轮换、检查、撤销、依赖影响和正常人工重新登录。

**STEP 3 — REQUIRED CAPABILITY**

凭证、连接与账号生命周期

**STEP 4 — CURRENT CHECK**

部分支持：E17原生Keychain存取轮换删除及重启接受；全OAuth/浏览会话/跨设备恢复不是该证据范围。

**STEP 5 — FAILURE TEST**

删除Key不知会阻塞谁；历史日志暴露Secret；重新登录后重发外部动作。

**STEP 6 — CROSS-BUSINESS TEST**

研发仓库服务与内容发布账号共同需要。共享。

**STEP 7 — PRODUCT OBJECT**

现有Credential reference、Connection、Account、执行使用记录。

**STEP 8 — USER-VISIBLE INFORMATION**

连接名/账号可核验标识/授权范围/到期/最后检查/使用员工和Work/撤销影响；绝不显示原始Cookie或Token。

**STEP 9 — INPUT / EDITING**

正常安全输入Key或OAuth登录；替换Secret；更改连接显示名。

**STEP 10 — DEFAULT**

输入后不回显可复制明文；不保存到普通配置、日志或文档；未知到期不编日期。

**STEP 11 — ADVANCED SETTINGS**

组织项目、服务权限和轮换策略按Provider实际支持；不提供Credential导出按钮。

**STEP 12 — EFFECT**

撤销立即阻止新请求；正在执行的外部效果可能继续，必须核验；轮换不改Account身份。

**STEP 13 — VALIDATION**

失效、Keychain不可用、拒绝授权、取消登录、轮换、重启、旧引用继续调用应受阻。

**STEP 14 — STATE**

未连接/连接中/可用/过期/待重新登录/撤销/密钥存储不可用/未知。

**STEP 15 — FAILURE / UNKNOWN**

给出影响列表和恢复入口；认证失败不向模型暴露完整响应头。

**STEP 16 — PERMISSION / SECURITY**

连接使用范围与执行动作权限不同；Secret仅运行时取用，员工只持引用。

**STEP 17 — PRODUCT PLACEMENT**

Settings连接与安全；Employee有效访问；Work阻塞卡。

**STEP 18 — INTERACTION**

[更新授权]→安全输入或官方登录→独立验证账号→检查依赖→恢复原Work前核验外部状态。

### C29 — 有效权限、撤销与动作审批

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO允许员工读取账号数据，却不允许发布；权限变更应立即可解释。

**STEP 2 — BUSINESS / WORK NEED**

计算Company/Business/Workspace/Employee/Work交集，显示允许原因与限制，审批绑定具体动作。

**STEP 3 — REQUIRED CAPABILITY**

有效权限、撤销与动作审批

**STEP 4 — CURRENT CHECK**

部分支持：E02 canonical scope和授权候选；完整每工具每外部副作用撤销链未验证。

**STEP 5 — FAILURE TEST**

有连接就被当全权；跨Business读取；撤销后排程仍执行。

**STEP 6 — CROSS-BUSINESS TEST**

内容发布与研发部署、数据读写均需要。全局基础。

**STEP 7 — PRODUCT OBJECT**

复用现有ResourceScopePolicy/Assignment授权/Decision；不复制第二权限树。

**STEP 8 — USER-VISIBLE INFORMATION**

目标/动作/数据范围/执行者/有效授权来源/到期/受限原因/待审批影响。

**STEP 9 — INPUT / EDITING**

授予具体范围和期限；批准一次或明确持续规则；撤销并查看依赖。

**STEP 10 — DEFAULT**

最小必要范围；没有授权等待；范围扩大不默认为已有授权延续。

**STEP 11 — ADVANCED SETTINGS**

组织策略继承及例外由有权者管理，普通员工只看有效结果。

**STEP 12 — EFFECT**

缩紧影响所有后续动作；已完成副作用不能自动撤回；既有结果可按访问权限隐藏。

**STEP 13 — VALIDATION**

不同scope同名对象、授权过期、撤销中执行、目标版本变化、员工调岗。

**STEP 14 — STATE**

允许/拒绝/需确认/过期/范围不明/正在撤销/已撤销。

**STEP 15 — FAILURE / UNKNOWN**

指出缺哪项权限和可申请对象；不能用万能“去设置”代替动作级解释。

**STEP 16 — PERMISSION / SECURITY**

审批发起者不得自行提升；执行端再次验证，UI隐藏不能代替安全边界。

**STEP 17 — PRODUCT PLACEMENT**

Work审批、Employee权限概览、Settings权限策略。

**STEP 18 — INTERACTION**

动作预检→影响摘要→有权者确认具体目标→执行前重检→回执；目标改变重新审批。

### C30 — Employee从设立到学习和停用

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO招一个研究员工，从职责开始配置能力并验证，再安排长期责任。

**STEP 2 — BUSINESS / WORK NEED**

身份职责、归属、能力与资源分配、就绪检查、Assignment、Conversation、Work、结果和学习。

**STEP 3 — REQUIRED CAPABILITY**

Employee从设立到学习和停用

**STEP 4 — CURRENT CHECK**

部分支持：E02组织/员工接受边界和执行候选；E18能力安装绑定接受；不能据此称所有Browser/MCP/Computer工作闭环已实现。

**STEP 5 — FAILURE TEST**

有头像职责却无法工作；模型坏了只显示员工在线；离职后未处理承诺。

**STEP 6 — CROSS-BUSINESS TEST**

研究员工与研发员工全链重复。共享Employee，专业技能不同。

**STEP 7 — PRODUCT OBJECT**

复用Employee/Responsibility/Assignment/Capability/Work/Result/Learning；不把Agent等于Employee。

**STEP 8 — USER-VISIBLE INFORMATION**

姓名/角色/职责/所属范围/领导关系/有效能力/阻塞/当前责任/工作/结果/学习依据。

**STEP 9 — INPUT / EDITING**

名称、职责和边界、选择能力组合及资料；授权责任与资源；不要求一人一个模型。

**STEP 10 — DEFAULT**

先草稿，满足当前Assignment所需能力才可开始；缺浏览不阻止纯文本工作但阻止需浏览任务。

**STEP 11 — ADVANCED SETTINGS**

用途模型路由、工具细权、Context策略属于能力详情；身份页不堆技术参数。

**STEP 12 — EFFECT**

换能力影响新执行；调岗须交接未完Work与责任；学习需依据，不自动改公司策略。

**STEP 13 — VALIDATION**

创建→绑定→低风险任务→失败→修复→重启→结果验收→交接停用完整验证。

**STEP 14 — STATE**

草稿/可执行某类工作/缺能力/工作中/等待/需人工/暂停/已停用。

**STEP 15 — FAILURE / UNKNOWN**

指出具体缺项及Work影响；不得以presence替代执行状态。

**STEP 16 — PERMISSION / SECURITY**

岗位不自动授予全部连接；任命责任不等外部副作用授权。

**STEP 17 — PRODUCT PLACEMENT**

组织中心Employee Detail在Utility；Conversation和Work在Main；人才能力供选择。

**STEP 18 — INTERACTION**

[创建员工]→职责/归属→按首个工作配置→检查→[安排工作]→Conversation与Work同步→验收结果→提出学习或调整。

### C31 — Business完整经营与资源就绪

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO开始业务，团队从目标和策略进入Cycle，执行后依据真实结果决定下一轮。

**STEP 2 — BUSINESS / WORK NEED**

Goal/Strategy/Workspace/Team/Responsibility/Resource/Cycle/Work/外部动作/分析/学习连贯。

**STEP 3 — REQUIRED CAPABILITY**

Business完整经营与资源就绪

**STEP 4 — CURRENT CHECK**

部分支持：E02 Business/Workspace/执行范围候选与接受层不同；不能从原子创建证明外部业务结果已打通。

**STEP 5 — FAILURE TEST**

业务页面填满但无人负责、无资源或无真实反馈；重复创建Workspace掩盖缺连接。

**STEP 6 — CROSS-BUSINESS TEST**

Content Growth与研发产品业务共用经营链；数据分析服务同用。

**STEP 7 — PRODUCT OBJECT**

现有Business、Workspace、Cycle、Assignment、Work、Result、Evidence；外部账号为资源，不是Workspace。

**STEP 8 — USER-VISIBLE INFORMATION**

目标与期限/策略假设/负责人/工作空间/团队/资源就绪/当前Cycle/运行阻塞/结果可信度。

**STEP 9 — INPUT / EDITING**

目标、成功标准、约束、策略、责任、所需账号和资料、周期；未知项允许明确待确认。

**STEP 10 — DEFAULT**

资源缺口显式保留；先建立业务意图，再按要执行的工作配置；不默认制造全部专业面板。

**STEP 11 — ADVANCED SETTINGS**

周期计算、领域指标和触发在对应策略详情；不将Provider参数塞进Business首页。

**STEP 12 — EFFECT**

目标变化版本化并说明影响；停止业务要处理未完Work、排程和外部承诺。

**STEP 13 — VALIDATION**

创建→资源缺失→补齐→分工→执行→失败→结果→分析→下轮；至少跨两类业务。

**STEP 14 — STATE**

草稿/待确认/缺资源/可启动/运行/等待/需决策/暂停/完成/归档。

**STEP 15 — FAILURE / UNKNOWN**

不能把“尚无指标”解释成0；给责任者和恢复入口；无回执的外部动作保持未知。

**STEP 16 — PERMISSION / SECURITY**

Business边界限定数据和账号；策略同意不等任意发布部署。

**STEP 17 — PRODUCT PLACEMENT**

业务空间Business概览及对应Workspace的Plan/Team/Work/Results等既有结构候选消费。

**STEP 18 — INTERACTION**

[开始业务]→目标与约束→策略确认→责任及资源检查→启动Cycle→跟踪Work→验收结果→复盘并决定下轮。

### C32 — Conversation与真实Work连续性

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO在聊天中补充要求，员工已开始执行；需要知道这句话有没有改变当前工作。

**STEP 2 — BUSINESS / WORK NEED**

Message与Work引用、草稿附件、提交意图、steering生效点、停止和历史可追溯。

**STEP 3 — REQUIRED CAPABILITY**

Conversation与真实Work连续性

**STEP 4 — CURRENT CHECK**

部分支持：E02多个topic/persistence/typed refs和General Work恢复接受；全部多工具steering时机未验证。

**STEP 5 — FAILURE TEST**

新消息丢失或被误当第二次执行；Stop只停止文字流，外部动作仍继续。

**STEP 6 — CROSS-BUSINESS TEST**

研究补来源与研发改验收标准共享。

**STEP 7 — PRODUCT OBJECT**

既有Conversation/Message/Work/Context/Execution；不另造聊天任务。

**STEP 8 — USER-VISIBLE INFORMATION**

发言者/时间/引用/对应Work/运行阶段/补充已收到或已应用/停止是否确认/结果引用。

**STEP 9 — INPUT / EDITING**

文本、附件、引用；选择补充当前Work或另起明确工作；编辑未发送草稿。

**STEP 10 — DEFAULT**

发送期间保留下一条草稿；意图不清先澄清；停止是请求不是即时保证。

**STEP 11 — ADVANCED SETTINGS**

Context检查和专业执行细节按需展开；普通Composer不永久堆模型工具日志。

**STEP 12 — EFFECT**

编辑历史消息不改既有执行事实；新指令形成有版本的补充，可能需重新审批。

**STEP 13 — VALIDATION**

多行IME、附件失败、并发发送、网络断开、重复提交、运行中补充、停止和重启。

**STEP 14 — STATE**

草稿/上传中/可发送/提交中/已收到/工作中/待应用/停止中/已停止/结果未知。

**STEP 15 — FAILURE / UNKNOWN**

保留草稿并明确重试是否会重复；提交未知先查询，不新增重复Work。

**STEP 16 — PERMISSION / SECURITY**

所有引用检查访问；网页文字不是用户指令；修改外部目标需新授权。

**STEP 17 — PRODUCT PLACEMENT**

Employee/Meeting/CEO Assistant共享Composer语义，宿主有不同对象和权限。

**STEP 18 — INTERACTION**

输入→附件检查→发送回执→Work状态；补充显示作用对象→应用确认；结果卡打开后可返回原滚动位置。

### C33 — Result验收、Evidence与学习

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

员工说发布成功或测试通过，CEO需要核验后才决定采用结果和复用经验。

**STEP 2 — BUSINESS / WORK NEED**

结果与执行回执、证据版本、验收标准、部分完成、修改请求及学习候选。

**STEP 3 — REQUIRED CAPABILITY**

Result验收、Evidence与学习

**STEP 4 — CURRENT CHECK**

部分支持：E19 typed Result/Evidence引用与UsedBy接受；E02真实工作链有证据但各Domain外部效果需分别验证。

**STEP 5 — FAILURE TEST**

推测成为经营事实；失败结果被包装成完成；经验污染长期策略。

**STEP 6 — CROSS-BUSINESS TEST**

内容发布回执和研发测试证据共用；研究引用同用。

**STEP 7 — PRODUCT OBJECT**

现有Result/Evidence/Acceptance/Knowledge或Learning候选，不复制事实源。

**STEP 8 — USER-VISIBLE INFORMATION**

结果摘要/交付物/对应目标/证据时间及来源/完整性/局限/验收状态/可复用范围。

**STEP 9 — INPUT / EDITING**

验收、退回修改、指定缺失证据；选择将已验证材料加入资料库。

**STEP 10 — DEFAULT**

结果生成不自动接受；未知外部状态不判失败或成功；学习先标候选。

**STEP 11 — ADVANCED SETTINGS**

证据保留和专业验收阈值按业务适用，不能一个通用分数替代判断。

**STEP 12 — EFFECT**

验收改变后续决策依据；退回产生关联Work，不抹掉旧结果。

**STEP 13 — VALIDATION**

证据过期、引用删除、版本变化、部分成功、重复回执、人工否决。

**STEP 14 — STATE**

待核验/部分证据/可审查/接受/需修改/不接受/过期/未知。

**STEP 15 — FAILURE / UNKNOWN**

提供证据缺口和补证据动作；不可访问原因和无证据不同。

**STEP 16 — PERMISSION / SECURITY**

结果访问继承真实范围；导出和公开发布分开；证据脱敏。

**STEP 17 — PRODUCT PLACEMENT**

Work结果、Business Results、资料预览及验收Utility。

**STEP 18 — INTERACTION**

点击结果→对照标准与证据→接受或说明修改→状态回写；[作为资料复用]保留来源版本和限制。

### C34 — Meeting形成责任而非仅聊天

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO召集多员工讨论策略，需要知道分歧、结论、负责人以及会后谁执行。

**STEP 2 — BUSINESS / WORK NEED**

参加者与范围、议题资料、发言、建议/决定区别、行动责任及会后Work链接。

**STEP 3 — REQUIRED CAPABILITY**

Meeting形成责任而非仅聊天

**STEP 4 — CURRENT CHECK**

部分支持：E02 MeetingAutonomy为候选，最终多周期边界未接受；不可宣称全自动主持落实。

**STEP 5 — FAILURE TEST**

会议结束没有责任；模型建议被自动当CEO批准外部行动。

**STEP 6 — CROSS-BUSINESS TEST**

内容策略与研发设计评审共同需要。共享协作，不替代全部Conversation。

**STEP 7 — PRODUCT OBJECT**

现有Meeting/Participant/Message/Decision/Assignment/Work。

**STEP 8 — USER-VISIBLE INFORMATION**

议题/参与者/角色/材料/当前议程/不同意见/待确认结论/行动负责人和状态。

**STEP 9 — INPUT / EDITING**

选择参与者、问题和材料；修改议程；确认决定和责任。

**STEP 10 — DEFAULT**

建议待确认；参与者只获得本次有权材料；会议不会自动扩大外部执行许可。

**STEP 11 — ADVANCED SETTINGS**

发言轮次和自动主持节奏仅能力支持才开；避免把模型参数放会议日程。

**STEP 12 — EFFECT**

更换参与者影响后续可见内容；修改决定保留历史并通知受影响责任。

**STEP 13 — VALIDATION**

缺席、模型失败、冲突意见、议题变更、重复生成行动、会后恢复。

**STEP 14 — STATE**

准备/进行/等待参与者/待决策/已结束/有未分配行动/部分失败。

**STEP 15 — FAILURE / UNKNOWN**

说明谁没有回应，不伪造共识；行动未创建显示待落实。

**STEP 16 — PERMISSION / SECURITY**

会议访问范围独立核验；主持权不等CEO审批权。

**STEP 17 — PRODUCT PLACEMENT**

会议Main、材料Utility、行动结果链接回Work。

**STEP 18 — INTERACTION**

创建→议题和参加者→讨论→确认结论→分配责任→查看对应Work；回会议保留决策上下文。

### C35 — 经营洞察的口径与未知

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO比较两业务进展，需要知道数据来自何时、是否完整，而不是看好看的数字。

**STEP 2 — BUSINESS / WORK NEED**

指标定义、时间口径、可追溯来源、缺失及估算标签、钻取与行动。

**STEP 3 — REQUIRED CAPABILITY**

经营洞察的口径与未知

**STEP 4 — CURRENT CHECK**

部分支持：E02 Insights有接受边界；外部平台数据和通用多源实时接入不能由此推定。

**STEP 5 — FAILURE TEST**

无数据显示0，估计收入显示实际，导致错误经营判断。

**STEP 6 — CROSS-BUSINESS TEST**

内容效果与研发交付周期共用可信度要求；各业务指标Domain-specific。

**STEP 7 — PRODUCT OBJECT**

现有Insights投影、Result/Evidence/Usage；无第二经营账本。

**STEP 8 — USER-VISIBLE INFORMATION**

指标名/定义/单位/时间窗/时区/来源/更新时间/覆盖率或缺失范围/估算标签。

**STEP 9 — INPUT / EDITING**

时间窗、业务筛选；选择已有定义；专业口径修改需可追溯。

**STEP 10 — DEFAULT**

无数据为未知；不默认跨不同币种或口径求和；显示最近确认时间。

**STEP 11 — ADVANCED SETTINGS**

归因窗口、排除规则、换算来源在指标详情；非普通全局开关。

**STEP 12 — EFFECT**

口径变化影响比较，保留版本；刷新不重写历史原始证据。

**STEP 13 — VALIDATION**

延迟、缺失、重复、零值、跨时区、来源冲突与单位不一致。

**STEP 14 — STATE**

加载/完整/部分/延迟/无数据/来源失败/口径不兼容。

**STEP 15 — FAILURE / UNKNOWN**

[查看来源]/[补齐数据]/[调整范围]；没有证据不能编趋势。

**STEP 16 — PERMISSION / SECURITY**

按Business访问范围过滤；聚合不泄露无权细项。

**STEP 17 — PRODUCT PLACEMENT**

经营洞察Main及来源Utility，跳转原Result。

**STEP 18 — INTERACTION**

选范围→看指标可信度→钻取依据→创建有上下文的分析或决策→返回原筛选。

### C36 — 资料库与全局对象查找

来源轮次：1（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO想找上周某结果，员工需要复用已验证资料，而非重复研究。

**STEP 2 — BUSINESS / WORK NEED**

稳定对象引用、范围过滤、搜索/快速打开、来源、版本、失效和安全复用。

**STEP 3 — REQUIRED CAPABILITY**

资料库与全局对象查找

**STEP 4 — CURRENT CHECK**

部分支持：E19资料检索与引用接受；E02全局对象搜索P1，不能当全部已有或全部没有。

**STEP 5 — FAILURE TEST**

找不到成果；复制旧内容失去来源；不同Business资料混入Context。

**STEP 6 — CROSS-BUSINESS TEST**

研究引用与研发历史决策、写作素材共同需要。共享。

**STEP 7 — PRODUCT OBJECT**

既有Knowledge/Reference及各对象搜索投影；Web Search另属外部搜索。

**STEP 8 — USER-VISIBLE INFORMATION**

名称/类型/所属范围/来源/更新时间/状态/匹配片段/访问限制/被使用位置。

**STEP 9 — INPUT / EDITING**

查询、类型范围筛选、固定常用对象；手动添加资料标来源；不要求建第二分类体系。

**STEP 10 — DEFAULT**

只搜有权对象；保留最近查询但不跨用户泄露；浏览历史不自动入库。

**STEP 11 — ADVANCED SETTINGS**

检索额度与语义增强按实际支持；普通用户不用选索引算法。

**STEP 12 — EFFECT**

归档使新检索可过滤，既有引用保留；删除受引用约束；权限缩紧立即影响结果。

**STEP 13 — VALIDATION**

无结果、重名、归档、权限变更、来源失效、大量结果与键盘返回。

**STEP 14 — STATE**

空查询/搜索中/有结果/无结果/部分索引/无权/来源失效。

**STEP 15 — FAILURE / UNKNOWN**

区分没有匹配和搜索服务失败；提供改范围；不展示无权对象标题。

**STEP 16 — PERMISSION / SECURITY**

搜索端和打开端均鉴权；引用发送再核验。

**STEP 17 — PRODUCT PLACEMENT**

资料库、全局Quick Open候选、Composer引用选择器。

**STEP 18 — INTERACTION**

快捷键打开→输入→键盘选中→打开原对象并保留返回路径；添加到Context显示来源与权限。

### C37 — 网络出口、代理与离线诊断

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

网页能打开，但员工模型请求或MCP失败；CEO需要知道故障在哪层。

**STEP 2 — BUSINESS / WORK NEED**

每类进程和连接的DNS/TLS/代理/可达性检查，受控超时及离线行为。

**STEP 3 — REQUIRED CAPABILITY**

网络出口、代理与离线诊断

**STEP 4 — CURRENT CHECK**

未验证：E03有受限URL和HTTP调用，未证明统一进程代理和用户诊断闭环；不能以浏览器连通替后台验收。

**STEP 5 — FAILURE TEST**

用户反复改Key，实际是代理或证书问题；绕过TLS后引入泄露。

**STEP 6 — CROSS-BUSINESS TEST**

研发依赖下载与研究模型/网页、数据连接都受影响。共享。

**STEP 7 — PRODUCT OBJECT**

Connection的网络配置与诊断Evidence，执行主机属性；不新增网络运营产品。

**STEP 8 — USER-VISIBLE INFORMATION**

失败阶段/目标主机/使用代理与否/检查时间/延迟/证书校验结果/运行进程类别；不显示认证头。

**STEP 9 — INPUT / EDITING**

选择系统网络或明确代理引用；超时；按连接覆盖需清楚其继承关系。

**STEP 10 — DEFAULT**

系统默认网络；TLS校验开启；不自动关闭证书校验；离线暂停需要网络的Work。

**STEP 11 — ADVANCED SETTINGS**

企业CA、分连接代理、绕过域和重试等待；仅受支持运行环境可配置，不开放任意隐藏环境变量。

**STEP 12 — EFFECT**

修改影响后续请求，可能改变数据出境；已发请求结果仍需核验。

**STEP 13 — VALIDATION**

浏览器成功后台失败、DNS失败、代理认证失败、TLS错误、断线、恢复及请求超时。

**STEP 14 — STATE**

未知/检查中/可达/离线/代理拒绝/TLS失败/超时/部分服务可用。

**STEP 15 — FAILURE / UNKNOWN**

按层给诊断与恢复入口；不将所有错误归为API Key错误；日志脱敏。

**STEP 16 — PERMISSION / SECURITY**

代理凭证走Vault；出口变化受数据策略；禁止从错误提示直接执行未知修复脚本。

**STEP 17 — PRODUCT PLACEMENT**

Settings网络与执行位置、Connection测试详情、Work阻塞原因。

**STEP 18 — INTERACTION**

[检查连接]→分层无敏感探针→展示具体失败层→调整授权配置→重新测→核验后恢复。

### C38 — 多员工资源占用与并发协调

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

两个员工同时改同一文件或操作同一账号，一个等待一个运行。

**STEP 2 — BUSINESS / WORK NEED**

共享资源所有权、允许并行与互斥区分、排队、释放、租约失效和公平恢复。

**STEP 3 — REQUIRED CAPABILITY**

多员工资源占用与并发协调

**STEP 4 — CURRENT CHECK**

未验证：当前证据不足以确认跨文件/浏览环境/电脑/Provider配额的统一占用体验；不能把执行队列当全部资源锁。

**STEP 5 — FAILURE TEST**

账号被切换、文件覆盖、等待无限、取消一个任务杀掉另一个进程。

**STEP 6 — CROSS-BUSINESS TEST**

研发共享目录与内容共享平台账号重复；数据GPU或数据库限额也有。共享。

**STEP 7 — PRODUCT OBJECT**

现有Execution资源占用记录候选，绑定Work和既有资源；不另建任务编排系统。

**STEP 8 — USER-VISIBLE INFORMATION**

资源/占用者Work/操作类别/等待原因/排队位置若可靠/最后心跳/可并行范围。

**STEP 9 — INPUT / EDITING**

选择等候、不同已授权资源或取消自己的等待；有权限才请求接管。

**STEP 10 — DEFAULT**

读可并行仅在安全范围；写/账号变更互斥；无心跳先核验外部状态再释放。

**STEP 11 — ADVANCED SETTINGS**

并发上限、租约和公平策略由运行管理员维护；普通用户不配置锁算法。

**STEP 12 — EFFECT**

降低并发影响新执行；强制接管可能打断动作，需显示风险和受影响Work。

**STEP 13 — VALIDATION**

两个员工争用、持有者崩溃、双资源交叉等待、取消队列、手工接管与恢复。

**STEP 14 — STATE**

可用/被占用/排队/核验持有者/释放中/需人工处理。

**STEP 15 — FAILURE / UNKNOWN**

明确等待哪个资源；提供替代或停止，不把资源等待显示模型思考。

**STEP 16 — PERMISSION / SECURITY**

占用信息不泄露无权Work内容；接管不继承原持有者权限。

**STEP 17 — PRODUCT PLACEMENT**

Work状态和资源Utility；Settings仅管理支持的并发限额。

**STEP 18 — INTERACTION**

点击等待原因→看占用与安全选项→等待或换资源→获得后重验Context/授权→继续同Work。

### C39 — 审批快照与变化后重检

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO批准发布A，员工随后把内容改成B，不能继续用A的批准。

**STEP 2 — BUSINESS / WORK NEED**

审批绑定目标、账号、内容版本、动作、费用范围及有效期；执行前重新比较。

**STEP 3 — REQUIRED CAPABILITY**

审批快照与变化后重检

**STEP 4 — CURRENT CHECK**

部分支持：E02有授权/Decision候选；当前逐类外部动作审批快照验收未验证。

**STEP 5 — FAILURE TEST**

一次同意被复用于其他账号或改后内容，形成越权发布或部署。

**STEP 6 — CROSS-BUSINESS TEST**

内容稿件发布和研发变更部署共用；数据导出亦然。共享安全基础。

**STEP 7 — PRODUCT OBJECT**

扩展既有Decision与Execution引用，不增加第二审批中心。

**STEP 8 — USER-VISIBLE INFORMATION**

批准的目标/版本/账号/动作/边界/批准人/时间/变化摘要/是否仍有效。

**STEP 9 — INPUT / EDITING**

批准一次、拒绝、请求修改；持续授权必须明确规则范围。

**STEP 10 — DEFAULT**

内容或目标关键变化使原批准失效；执行时重检；纯展示改动是否影响按明确规则。

**STEP 11 — ADVANCED SETTINGS**

版本指纹和差异证据可展开；普通用户看业务变化，不必看hash。

**STEP 12 — EFFECT**

新批准不删除旧审计；撤销阻止后续动作，已提交外部请求进入核验。

**STEP 13 — VALIDATION**

批准后换账号、改正文、换文件、增费用、过期、撤销与执行竞态。

**STEP 14 — STATE**

待审批/已批准/内容已变/已过期/已撤销/执行中/效果待核验。

**STEP 15 — FAILURE / UNKNOWN**

[查看变化]/[重新确认]；不能用普通toast隐去审批不再有效。

**STEP 16 — PERMISSION / SECURITY**

审批者权限与执行者权限同时成立；系统不得自批自己的范围扩大。

**STEP 17 — PRODUCT PLACEMENT**

Work审批摘要、Result变更对比、Attention。

**STEP 18 — INTERACTION**

打开请求→看精确影响→批准→执行前比对→变化则回Attention→新决定后再执行。

### C40 — 外部副作用未知与安全续做

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

发布或部署请求超时；平台可能已经成功，重复请求会造成重复内容或重复资源。

**STEP 2 — BUSINESS / WORK NEED**

区分未发出、已发出无回执、已确认效果；通过外部ID/查询核验及安全重试。

**STEP 3 — REQUIRED CAPABILITY**

外部副作用未知与安全续做

**STEP 4 — CURRENT CHECK**

部分支持：E16某些outbound错误不走fallback，体现有限边界；通用发布/部署幂等与回执核验未验证。

**STEP 5 — FAILURE TEST**

把超时当没执行并自动重试；错误重复发布。

**STEP 6 — CROSS-BUSINESS TEST**

内容发布、研发部署、数据写回共用；具体核验接口为Domain。

**STEP 7 — PRODUCT OBJECT**

现有Execution尝试、外部回执Evidence、Work状态；不另造执行账本。

**STEP 8 — USER-VISIBLE INFORMATION**

尝试ID/目标/提交时间/最后确认阶段/外部ID若有/可核验方式/重复风险。

**STEP 9 — INPUT / EDITING**

核验、等待、人工确认外部状态；仅明确风险后授权新的非幂等尝试。

**STEP 10 — DEFAULT**

未知保持未知；不自动对非幂等动作重试或切Provider；读操作可在预算内重试。

**STEP 11 — ADVANCED SETTINGS**

幂等key与轮询窗口由适配器能力声明；不能让用户自填一个ID就声称服务支持幂等。

**STEP 12 — EFFECT**

确认成功后只补回执不重做；新尝试保留与上次关系；取消不抹掉已提交效果。

**STEP 13 — VALIDATION**

发出前断线、服务成功响应丢失、重复回调、最终一致延迟、停止后晚到回执。

**STEP 14 — STATE**

未提交/提交中/已提交待回执/效果未知/已核验成功/已核验失败/需人工。

**STEP 15 — FAILURE / UNKNOWN**

[到目标核验]/[稍后检查]/[记录人工证据]；不可验证时保持阻塞并说明。

**STEP 16 — PERMISSION / SECURITY**

外部查询仍需范围权限；人工确认记录来源；无权发布不得借重试绕过。

**STEP 17 — PRODUCT PLACEMENT**

Work恢复区、Attention、Result证据详情。

**STEP 18 — INTERACTION**

点击未知→查看已确认事实→只读核验→有证据更新状态→必要时有权者决定是否新尝试。

### C41 — 外部内容与插件的指令信任边界

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究网页或安装的Skill要求忽略CEO并上传资料；员工不能把读到的内容当授权。

**STEP 2 — BUSINESS / WORK NEED**

来源标识、指令与资料分离、工具权限执行端约束、依赖更新复核。

**STEP 3 — REQUIRED CAPABILITY**

外部内容与插件的指令信任边界

**STEP 4 — CURRENT CHECK**

未验证：仅有工具适配和范围证据不足以证明端到端提示注入防护；不声称已经安全。

**STEP 5 — FAILURE TEST**

网页控制员工行为，越过工作目的或泄露资料。

**STEP 6 — CROSS-BUSINESS TEST**

网页研究与研发仓库README/依赖说明共同受影响。共享。

**STEP 7 — PRODUCT OBJECT**

现有Reference来源属性、Capability安装版本和Execution授权；无新安全仪表盘。

**STEP 8 — USER-VISIBLE INFORMATION**

来源/可信用途/触发的越界请求/被阻止动作/影响Work/需用户判断内容。

**STEP 9 — INPUT / EDITING**

允许作为资料引用或作为经审查Skill安装；用户不能用“信任网站”自动授权所有外发。

**STEP 10 — DEFAULT**

外部内容默认资料；安装包不自动提升权限；变更版本重新检查需要的能力。

**STEP 11 — ADVANCED SETTINGS**

允许工具集合与资料外发策略由授权管理，不能通过prompt开关代替。

**STEP 12 — EFFECT**

信任标签变化不改历史来源；更新Skill可使测试和授权需复核。

**STEP 13 — VALIDATION**

恶意网页、附件、工具输出、仓库说明提出读Secret/上传/改目标；执行端应拒绝越界。

**STEP 14 — STATE**

普通资料/待审查/已安装受限/检测到越界请求/已阻止/需处理。

**STEP 15 — FAILURE / UNKNOWN**

解释被阻止的动作和来源，不展示Secret；保留正常任务可继续的路径。

**STEP 16 — PERMISSION / SECURITY**

资料永远不提供用户权限；不能通过内容伪造系统或CEO身份。

**STEP 17 — PRODUCT PLACEMENT**

引用来源Utility、安装审查、Work工具阻止提示。

**STEP 18 — INTERACTION**

打开来源→按资料处理→遇越界请求阻止→记录来源→用户可排除材料或按正常授权重新定义任务。

### C42 — 素材生产、转写与可交付验证

来源轮次：2（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

写作员工要配图，内容员工要带字幕短片；视觉识别模型不一定能生成素材。

**STEP 2 — BUSINESS / WORK NEED**

分别识别图像生成/编辑、音频转写/合成、视频生成或处理、格式转换及产物校验。

**STEP 3 — REQUIRED CAPABILITY**

素材生产、转写与可交付验证

**STEP 4 — CURRENT CHECK**

未验证：E03 image/audio unknown；现有文本和资料接受不证明媒体生产；不得填造可用模型。

**STEP 5 — FAILURE TEST**

能描述图片却交不出图片；把文本链接当视频结果；成本时长未知仍批量执行。

**STEP 6 — CROSS-BUSINESS TEST**

内容运营与写作出版重复；研究访谈需要转写。能力编排共享，分镜剪辑是Domain。

**STEP 7 — PRODUCT OBJECT**

Capability/Model用途、输入素材Reference、Execution、Result版本与媒体元数据。

**STEP 8 — USER-VISIBLE INFORMATION**

支持操作/输入输出格式/尺寸或时长/大小上限/实际服务/预计预算/产物路径/生成状态。

**STEP 9 — INPUT / EDITING**

选择已验证能力、提示和素材、目标格式尺寸；转写语言可自动检测但显示未知。

**STEP 10 — DEFAULT**

没有能力则说明缺项；先小样；不自动购买Credits；素材权限和外发范围预检。

**STEP 11 — ADVANCED SETTINGS**

采样率、编码、帧率、种子等只对实际支持工具开放；专业领域才显示。

**STEP 12 — EFFECT**

换规格影响成本和质量；重生成新版本不覆盖已批准素材；输入变化重新检查授权。

**STEP 13 — VALIDATION**

真实文件存在、格式可读、时长尺寸正确、音画/字幕对应、超时/部分输出/取消回执。

**STEP 14 — STATE**

缺能力/准备素材/排队/生成/部分完成/格式校验失败/可预览/未知。

**STEP 15 — FAILURE / UNKNOWN**

展示已生成哪些和缺哪些；不能用占位图假装完成；保留部分有效产物。

**STEP 16 — PERMISSION / SECURITY**

输入素材使用权由业务确认；外发及发布权限独立；生成不自动公开。

**STEP 17 — PRODUCT PLACEMENT**

Work专业输入、Result媒体预览、Employee用途能力；Settings只管理连接和限制。

**STEP 18 — INTERACTION**

提出交付规格→检查所需能力→确认小样范围→生成→实际预览校验→选版本纳入最终Result。

### C43 — 备份、恢复、容量与设备迁移

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO电脑损坏或磁盘满，需恢复公司资料和未完工作；备份可能不包含Keychain。

**STEP 2 — BUSINESS / WORK NEED**

明确备份范围/一致性/加密/空间检查/恢复校验/凭证重连/外部效果核验。

**STEP 3 — REQUIRED CAPABILITY**

备份、恢复、容量与设备迁移

**STEP 4 — CURRENT CHECK**

部分支持：E20备份恢复实现存在但ACCEPTANCE PENDING；E17凭证原生保存接受不等于跨设备恢复接受。

**STEP 5 — FAILURE TEST**

备份看似成功却无法打开；恢复后模型缺授权，排程重复发布；磁盘满丢草稿。

**STEP 6 — CROSS-BUSINESS TEST**

研发成果与研究证据长期保存都需要。全局基础。

**STEP 7 — PRODUCT OBJECT**

既有备份包与恢复流程、Work/Reference状态，不创建第二数据库或默认复制秘密。

**STEP 8 — USER-VISIBLE INFORMATION**

包含/不含范围/版本/时间/大小/可用空间/校验结果/恢复位置/需重连列表/未完Work。

**STEP 9 — INPUT / EDITING**

选择备份目标、恢复包、保留策略；覆盖现有公司前显示精确影响。

**STEP 10 — DEFAULT**

不覆盖唯一现存副本；备份不明文含Secret；恢复后排程暂停待核验；旧来源文件可能需重新定位。

**STEP 11 — ADVANCED SETTINGS**

加密、保留上限、外部目录是否打包；真实支持才配置，不承诺跨版本任意兼容。

**STEP 12 — EFFECT**

恢复替换或导入范围明确；原设备权限与Credential可能无效；外部服务状态不随本地回滚。

**STEP 13 — VALIDATION**

磁盘满、中途断电、损坏包、版本不兼容、不同设备、缺外部文件、无Keychain、恢复后重复触发。

**STEP 14 — STATE**

可备份/空间不足/备份中/校验失败/可恢复/恢复中/需重连/需核验工作。

**STEP 15 — FAILURE / UNKNOWN**

显示哪些数据未恢复与下一步；不把包下载成功当恢复验收。

**STEP 16 — PERMISSION / SECURITY**

备份含私人材料需加密和本机授权；支持导出不授权发送第三方。

**STEP 17 — PRODUCT PLACEMENT**

Settings数据与恢复、启动恢复向导、Attention。

**STEP 18 — INTERACTION**

[备份]→范围和空间检查→生成→校验；[恢复]→预检包→选隔离目标→恢复→核对对象及引用→重新授权并核验Work。

### C44 — 版本更新、能力漂移与可复验性

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

一个月后模型下架、Plugin更新或App升级，原来能做的任务突然失效。

**STEP 2 — BUSINESS / WORK NEED**

版本来源、兼容性、能力重新发现、测试过期、依赖影响和有限回退。

**STEP 3 — REQUIRED CAPABILITY**

版本更新、能力漂移与可复验性

**STEP 4 — CURRENT CHECK**

部分支持：E03发现刷新和不可用标记存在；完整更新、分页完整性、插件迁移和回退验收未验证。

**STEP 5 — FAILURE TEST**

更新静默换模型行为；部分发现误下架；旧授权覆盖新插件权限。

**STEP 6 — CROSS-BUSINESS TEST**

研发Agent更新与内容模型/插件更新共用。共享维护能力。

**STEP 7 — PRODUCT OBJECT**

现有Connection/Model Profile/Capability版本及Test Result、Work执行快照。

**STEP 8 — USER-VISIBLE INFORMATION**

当前/可用版本/来源/变化/依赖/新增权限/测试是否过期/受影响员工及排程。

**STEP 9 — INPUT / EDITING**

检查更新、审查权限、选择适配器支持的更新或回退；不能回退远端已下架模型。

**STEP 10 — DEFAULT**

新增权限不自动接受；完整发现才确认移除；运行中的Work保持已确认快照或明确暂停。

**STEP 11 — ADVANCED SETTINGS**

更新通道、延迟策略和版本锁定仅实际可支持组件提供。

**STEP 12 — EFFECT**

更新影响下一执行兼容性；参数和Profile测试需刷新；不能把旧成功测试贴新版本。

**STEP 13 — VALIDATION**

部分发现、下架、breaking schema、更新失败、权限增加、运行中升级、数据迁移失败。

**STEP 14 — STATE**

当前可用/有更新/需复验/兼容性未知/更新中/失败/不再提供。

**STEP 15 — FAILURE / UNKNOWN**

列影响与替代方案；无安全回退则明确，不能显示万能恢复旧版。

**STEP 16 — PERMISSION / SECURITY**

官方来源与完整性检查；未知安装脚本不得自动获系统权限；不读取Secret检查。

**STEP 17 — PRODUCT PLACEMENT**

Settings应用与能力维护、Model详情、Employee就绪检查。

**STEP 18 — INTERACTION**

[检查更新]→变化和依赖→必要测试→授权新增权限→应用→复验→恢复受影响Work。

### C45 — 来源时效、矛盾与结果修订

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

研究报告昨天引用的页面今天改变，两来源互相冲突，CEO需要修正后续决策。

**STEP 2 — BUSINESS / WORK NEED**

来源快照和获取时间、冲突显式记录、刷新/比较、结论版本和依赖提示。

**STEP 3 — REQUIRED CAPABILITY**

来源时效、矛盾与结果修订

**STEP 4 — CURRENT CHECK**

部分支持：E19引用与UsedBy接受；完整外部来源更新检测、冲突处理未验证。

**STEP 5 — FAILURE TEST**

新网页覆盖旧证据；过期结论继续被员工当事实；合并冲突产生编造答案。

**STEP 6 — CROSS-BUSINESS TEST**

研究政策/产品资料与内容竞品/数据指标重复。共享证据能力，专业判定为Domain。

**STEP 7 — PRODUCT OBJECT**

Evidence版本、Reference、Result修订、依赖关系；不创造平行事实知识库。

**STEP 8 — USER-VISIBLE INFORMATION**

来源/获取时间/原始内容片段/变化/冲突点/可信局限/哪些结果引用。

**STEP 9 — INPUT / EDITING**

主动刷新、选择需保留的版本、标记矛盾、请求进一步核验。

**STEP 10 — DEFAULT**

原始证据不可静默覆写；冲突保持可见；没有证据不自动选赢家。

**STEP 11 — ADVANCED SETTINGS**

刷新频率和保留策略由明确需求启用；不是所有网页都持续监控。

**STEP 12 — EFFECT**

刷新不重写历史Result；新结论须显式修订，受影响任务可提醒重新核验。

**STEP 13 — VALIDATION**

页面删除、付费或登录限制、动态内容变化、两个可靠来源冲突、引用版本丢失。

**STEP 14 — STATE**

有效快照/可能过期/已变化/冲突/不可访问/待修订。

**STEP 15 — FAILURE / UNKNOWN**

显示最后可核验时间；原文无权访问不意味着旧快照可无限共享。

**STEP 16 — PERMISSION / SECURITY**

来源访问权和快照权限分开；不绕过付费获取更新。

**STEP 17 — PRODUCT PLACEMENT**

Evidence Utility、Result来源、资料详情。

**STEP 18 — INTERACTION**

[核对来源]→获取当前合法内容→差异→标记冲突或修订→查看受影响结果→决定重新分析。

### C46 — 可访问性、语言与长内容操作

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO用中文输入法、键盘或屏幕阅读器处理长对话；员工输出跨语言内容。

**STEP 2 — BUSINESS / WORK NEED**

IME安全发送、键盘焦点与返回、缩放、可读状态、语言/地区/时间一致。

**STEP 3 — REQUIRED CAPABILITY**

可访问性、语言与长内容操作

**STEP 4 — CURRENT CHECK**

部分支持：当前页面存在不等于跨宿主可访问性验收；本轮未做真实键盘/读屏测试，标未验证。

**STEP 5 — FAILURE TEST**

中文候选未确认就发送；缩放遮住按钮；色盲看不出失败；多时区误读排程。

**STEP 6 — CROSS-BUSINESS TEST**

写作多语言与数据时间格式、所有业务操作共用。全局基础。

**STEP 7 — PRODUCT OBJECT**

Personal偏好与Surface交互规则，非新增业务对象。

**STEP 8 — USER-VISIBLE INFORMATION**

界面语言/时间区/日期格式/快捷键作用域/焦点/文本状态/缩放支持。

**STEP 9 — INPUT / EDITING**

语言、时区、发送键行为、减少动画；继承OS可改但显示实际生效值。

**STEP 10 — DEFAULT**

跟随系统语言与时区；IME组合中不发送；状态不只靠颜色；遵循系统减少动画。

**STEP 11 — ADVANCED SETTINGS**

冲突快捷键映射仅有真实需求提供；不建复杂主题编辑器。

**STEP 12 — EFFECT**

语言改变不翻写历史内容；时区改显示但已排程绝对时间需明确确认是否重排。

**STEP 13 — VALIDATION**

中文IME、全键盘、读屏、200%缩放、长标题长文、窄窗口、减少动画、跨时区。

**STEP 14 — STATE**

聚焦/选中/禁用及原因/提交中/错误可读/焦点返回；辅助技术状态同步。

**STEP 15 — FAILURE / UNKNOWN**

无障碍错误作为可操作缺陷记录；不可把鼠标可用当键盘可用。

**STEP 16 — PERMISSION / SECURITY**

系统辅助设置不授权电脑控制；通知隐私仍遵循个人范围。

**STEP 17 — PRODUCT PLACEMENT**

全局Shell规则、共享Composer、个人Settings。

**STEP 18 — INTERACTION**

键盘进入→可见焦点→打开对象→Esc按层关闭→回触发点；发送尊重IME；错误聚焦说明。

### C47 — 诊断、支持导出与隐私保留

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

任务反复失败，CEO想把诊断发给支持，又不想泄露公司资料和Key。

**STEP 2 — BUSINESS / WORK NEED**

按执行关联收集错误、版本、环境摘要，用户预览脱敏包和保留期限。

**STEP 3 — REQUIRED CAPABILITY**

诊断、支持导出与隐私保留

**STEP 4 — CURRENT CHECK**

未验证：各局部日志不等于安全诊断导出验收；本轮未读取实际私有日志。

**STEP 5 — FAILURE TEST**

只能截聊天猜故障；打包包含Token、提示材料和Cookie。

**STEP 6 — CROSS-BUSINESS TEST**

研发执行失败与内容Provider失败共用。全局维护基础。

**STEP 7 — PRODUCT OBJECT**

既有Execution日志/Evidence的受控诊断导出；不新增全量监控数据系统。

**STEP 8 — USER-VISIBLE INFORMATION**

错误阶段/版本/时间/关联Work/将导出项目/已删除敏感项/仍可能含业务文本提示。

**STEP 9 — INPUT / EDITING**

选择某次执行和时间窗；预览、排除项目、保存本地；发送第三方另行明确动作。

**STEP 10 — DEFAULT**

最小必要数据；凭证、Cookie、认证头永不导出；内容正文默认不包含。

**STEP 11 — ADVANCED SETTINGS**

日志级别和保留期限有限期启用；详细调试不能永久常开。

**STEP 12 — EFFECT**

开启详细日志只影响后续执行；删诊断不删除业务证据；下载不代表已发给支持。

**STEP 13 — VALIDATION**

带Secret错误文本、URL参数、截图私人信息、超大日志、导出中断和脱敏漏项。

**STEP 14 — STATE**

可诊断/收集中/待预览/部分数据/生成失败/已保存。

**STEP 15 — FAILURE / UNKNOWN**

说明缺失日志及影响；不能用“已脱敏”保证未经检查内容完全安全。

**STEP 16 — PERMISSION / SECURITY**

仅有权用户访问日志；用户明确确认出站；不上传整库或系统凭证存储。

**STEP 17 — PRODUCT PLACEMENT**

Work错误详情、Settings帮助与诊断。

**STEP 18 — INTERACTION**

[查看诊断]→局部原因→需要时生成包→预览范围→本地保存→用户另行决定发送。

### C48 — 退出业务与资源退役

来源轮次：3（1=初推；2=反证一；3=反证二）。

**STEP 1 — REAL USER SCENARIO**

CEO停止某业务或员工离职，需要处理未完承诺，同时保留经营历史。

**STEP 2 — BUSINESS / WORK NEED**

停止新工作、梳理排程/占用/连接/责任、交接或取消、归档与引用保持。

**STEP 3 — REQUIRED CAPABILITY**

退出业务与资源退役

**STEP 4 — CURRENT CHECK**

部分支持：E02有Work归档恢复，E19资料归档引用边界接受；整业务退役及外部撤销闭环未验证。

**STEP 5 — FAILURE TEST**

归档业务后定时发布还执行；删除员工让未完工作失去责任人；删除证据无法审计。

**STEP 6 — CROSS-BUSINESS TEST**

内容停运与研发项目交付后维护、研究项目结束均有。共享生命周期。

**STEP 7 — PRODUCT OBJECT**

既有Business/Employee/Assignment/Work/Connection归档状态与交接Decision，不新造离职系统。

**STEP 8 — USER-VISIBLE INFORMATION**

未完Work/未来触发/外部待核验效果/资源占用/当前责任/资料引用/可恢复与不可逆范围。

**STEP 9 — INPUT / EDITING**

交接负责人、暂停或取消排程、撤销专用连接、保留历史；平台账号删除独立处理。

**STEP 10 — DEFAULT**

归档不等删除；先阻止新触发并核验在途动作；共享连接不因单业务归档直接删。

**STEP 11 — ADVANCED SETTINGS**

保留期限由已有公司策略及真实约束决定，不自动给固定法律期限。

**STEP 12 — EFFECT**

新工作停止，历史仍按权限可见；恢复需要重验能力和授权，不自动重启旧排程。

**STEP 13 — VALIDATION**

在途发布、共享连接、多业务员工、未认领责任、恢复后失效凭证、被引用对象。

**STEP 14 — STATE**

待交接/有在途动作/停止新工作/待核验/可归档/已归档/恢复待检查。

**STEP 15 — FAILURE / UNKNOWN**

明确尚未结束的外部承诺；不把归档成功当外部取消成功。

**STEP 16 — PERMISSION / SECURITY**

操作人需管理权限；删除真实外部账号不包含在内部归档授权中。

**STEP 17 — PRODUCT PLACEMENT**

Business/Employee更多菜单、影响预览Modal、Attention。

**STEP 18 — INTERACTION**

[暂停或归档]→影响清单→交接/停止/核验→确认归档→历史可访问；恢复先就绪检查。


## 设置、模型字段与V1对照

本轮设置从48条能力链导出，再映射回现有六类容器，共77条，每条14字段，见[设置字段台账](SETTINGS_FIELD_REGISTER.md)。实际私有配置未读取，Current Value为UNVERIFIED；默认是明确候选，不冒充当前值。Work/Employee/Workspace设置就地编辑，Settings不复制真源。

[Model / Provider字段合同](MODEL_PROVIDER_FIELD_CONTRACT.md)拆出24项Profile及11项Provider字段，区分普通、只读、自动发现、人工声明、高级覆盖和实测；它完整嵌入[V2](CURIS_FULL_PRODUCT_EXPRESSION_V2.md)。模型目录、认证、文本推理、各模态、工具调用、Computer执行分别验证。默认省略不支持或无需覆盖的采样参数，不硬设通用Temperature；适配器默认数字必须显示真实生效值，未确定则明确缺口。

[V1逐项对照](V1_COMPARISON.md)在两轮反证后进行，覆盖42章和局部遗漏/过度设计。V1已经有多用途绑定、Unknown、Stop、版本失效和副作用核验，不能谎称这些从未想到。本轮将这些表达扩展到完整能力条件，并补Browser真实执行、文件/进程、网络、恢复等基础链。

## 关键证据索引及适用等级

|证据|Class / 实际采用范围|精确位置与结论|
|---|---|---|
|E01 / E21–E26|Current/Frozen产品关系|Pointer Current Required Input；Blueprint/Map/UI/Baseline/Shell/Repair。七区、6+1初始员工、四层scope、四职责Pane与六类Settings；不从旧V1晋升Authority。|
|E02|CURRENT implementation ledger，逐条接受边界|CURRENT_STATE当前接受/候选分开；General Work恢复证据不能推出全部后台业务支持。|
|E03|Source-level implementation evidence|backend/app/ai_capability_registry.py `_profile` 217–250、`connect` 308–416：chat直接supported、其余多unknown；发现成功不是所有能力实测。单次获取及缺失标记需要完整分页规则。|
|E04|Source-level UI evidence|frontend/components/v1/ModelManagement.js `ModelManagement`：安全连接、发现、设默认入口存在；完整Profile/用途验证未由这个组件证明。|
|E05/E06|Source-level implementation evidence|backend/app/model_preferences.py `TenantModelPreferenceResolver`；employee_capability_model.py `set_employee_capabilities`：默认解析与多能力绑定已有，不声称一员工只能一模型。|
|E07|Source-level implementation evidence|backend/app/agent_adapter.py `CodexCliAdapter`：read-only/workspace-write及resume适配；widest native access显式不支持，不等完整OS操作。|
|E08|Source-level implementation evidence|backend/app/local_rd_toolset.py `LocalRDToolset`：read/search/apply_diff/run_test/git_read固定工具；不能将其声称通用Browser/Terminal/部署。|
|E09|Source-level implementation evidence|backend/app/capability_adapters.py `McpAdapter`：最小stdio initialize和单工具prompt调用；完整工具发现/schema/权限仍需合同。|
|E10/E17|实现源码+Frozen bounded acceptance|credential_vault.py `MacOSKeychainCredentialBackend`；Cloud AI Continuity接受原生Keychain与DeepSeek重启路径，未读取实际Secret，不能扩成所有OAuth/Provider接受。|
|E11/E12/E13|Source-level implementation evidence|runtime/scheduler.py `RuntimeScheduler`默认SimulatedExecutor；runtime/ceo_day_service.py默认模拟路径；另有backend/app/scheduler.py真实后台调度，不说“整个调度都模拟”，也不把某路径存在当业务按时交付。|
|E14/E15|Desktop source evidence|desktop/src/lib.rs `kill_sidecars`与window close/Exit分支；Cargo依赖。关闭会结束本机sidecar，不能承诺退出后常驻。|
|E16|Source-level bounded execution evidence|backend/app/main.py运行能力解析/部分fallback与启动关闭；已有特定outbound失败不fallback，但不等通用外部副作用核验实现。|
|E18|Frozen implementation acceptance|Talent/Skill install/Employee binding实际接受范围保留；外部连接和全部工具类型不能自动扩大接受。|
|E19|Frozen implementation acceptance|Knowledge Library typed reference/UsedBy/读写及范围接受；md/txt等既有边界不扩为PDF/OCR/所有文件版本系统。|
|E20|Review / execution backlog|备份恢复实现存在但ACCEPTANCE PENDING，不能写“没有备份”，也不能写“恢复已接受”。|
|纯函数探针|本轮合成输入证据|evidence/model-profile-probe.json：embedding-only也chat supported；合成嵌套vision对象被truthy判断；空metadata也chat supported。合成vision结构不冒充真实Claude API。|
|官方协议|L3 Documentation|OpenAI Models、Claude Models、Gemini Models、Playwright BrowserContext/auth、MCP Tools说明元数据与执行/隔离边界；研究候选判断为推导，不冒充内部实现。|

所有路径及SHA256见[evidence/source-manifest.json](evidence/source-manifest.json)。本轮对原20份输入重新比对未发生变化；新增Authority输入单独记录，不重写原hash。没有用线上成本/模型价格作无日期承诺。

## 新能力与优先级候选

|级别|候选|用户断点|Owner / 下一证据|
|---|---|---|---|
|P0 DESIGN FOUNDATION|用途级就绪与Model Profile可信状态 C01–08|连接成功仍无法工作|Product+Capability：连接/声明/实测/授权四层合同与受支持矩阵|
|P0 DESIGN FOUNDATION|真实Browser与隔离账号环境 C12–16|研究无法打开，研发无法点测，经营会用错账号|Product+Desktop：执行器、账号绑定、观察/接管/恢复合同|
|P0 DESIGN FOUNDATION|文件/进程/Preview连续性 C17–24|代码或资料产出后无法真实验证|Capability+Domain：五类工作链所需工具和结果证据|
|P0 DESIGN FOUNDATION|后台/排程/Attention与恢复 C25–29|CEO离开任务停止或重复执行|Product+Runtime：执行位置、退出保证、错过与权限检查|
|P0 DESIGN FOUNDATION|有效审批与效果未知 C38–40|批准失效、重复发布、资源冲突|Security+Runtime：复用既有Decision/Execution的动作级合同|
|P1 PRODUCT DEPTH|媒体/数据/OCR/来源修订 C22–23/C42/C45|只会输出文字，无法完成多种真实交付|Capability+Domain：格式/操作/来源测试与实际产物|
|P1 PRODUCT DEPTH|备份/升级/诊断/退役 C43–48|长期运行无法维护和安全结束|Desktop+Runtime：恢复/重连/版本漂移与交接证据|
|P2 POLISH / POWER USER|更细快捷键、摘要渠道、专业参数维护|高频用户操作耗时|Design+Product：真实可访问性和效率验证；不新增Reserved命令系统|
|FUTURE|移动独立客户端、任意IDE复制、全能媒体Studio|非当前五条共享链必需的独立产品范围|CEO明确战略授权后另立范围，不混进本轮完整性承诺|

Candidate不是Current能力，也不是强制所有员工安装全部工具。高级能力按任务需要出现；必要共享合同不能因实现困难降格成“只需链接”。

## 最终20问

### 1. V1为什么不能证明产品完整？

它对已知对象的页面/按钮/返回做了表达闭合，没有先用真实工作推导全部必要能力。其“没有留下产品逻辑给设计师”超出证据；Browser真实执行、完整模型能力、文件与后台等使工作链断裂，不能只归为后续实现小项。

### 2. 本轮新发现哪些遗漏？

除Browser和Model外，文件授权/外部编辑冲突、受控进程/Preview、OCR/格式校验、数据快照、实际外发路径、后台退出与错过排程、网络代理差异、共享资源争用、审批快照、跨域副作用未知、外部内容信任、媒体生产、备份恢复重连、更新漂移、来源矛盾、可访问性、安全诊断与退役交接。部分语义V1已有，本轮补完整条件而不冒称全新。

### 3. Browser是否基础能力？

是，受控网页操作是多业务共享执行基础：研究读动态网页、研发验证localhost、经营使用真实后台。Search/Reader/Browser/OS Computer Use必须分开，按需求启用。默认推荐按账号隔离环境，受控插件桥作为兼容途径；实际执行器合同仍需G1仲裁，不能把渲染WebView等同员工可操作浏览器。

### 4. Model Management需要什么？

连接实例、协议与安全认证、完整分页发现/手动未验证、24项Profile字段、声明来源/实测分离、用途分配与继承、固定或受限自动、兼容Fallback、按支持参数设置、分层测试、费用限流与版本复验。详见V2内完整模型表与设置条目，不是一张默认模型Dropdown。

### 5. Settings最终类别？

保留六类：个人与外观、公司设置、模型与AI、权限与安全、应用与数据、账户与帮助。内含77条字段合同；网络/后台/备份属于应用与数据，浏览环境/OS/文件/外发属于权限与安全，执行工具及模型用途在模型与AI。对象内参数不复制到全局真源。

### 6. 哪些放Advanced？

自定义endpoint、组织项目/区域、采样参数、推理effort、输出上限、超时/重试、Context/Tool policy、并发降低值、Agent启动参数、MCP工具细权、查询额度、会话保留、Proxy/企业CA、日志级别等。名称/连接状态/实际用途/缺权限/最后测试与账号身份是普通用户判断所必需，不能藏高级。

### 7. Employee真正工作还缺什么？

按目标的有效能力交集：模型用途、工具执行器、资料输入、账号连接、OS与动作权限、执行主机、预算、结果验证及恢复。已有Employee/多能力绑定必须保留；不能把没全量工具说成没有Employee系统。详细当前支持/未验证见48项Current Check。

### 8. Software Development暴露什么？

真实目录授权、dirty保护、版本冲突、解释器/依赖与命令执行、进程树停止、Preview主机端口、浏览交互验证、差异接受、push/deploy授权分层、未知效果核验。这些多数也出现在分析和出版，不能只放某张研发UI里。

### 9. Research暴露什么？

Search不是全局对象搜索；Reader不等Browser；来源快照/引用版本、解析/OCR、长Context预算、可信指令边界、长任务恢复及矛盾来源修订是共享需要。浏览历史不能自动变正式Knowledge。

### 10. Content Growth暴露什么？

账号环境隔离、素材真实生产、逐账号修订与审批有效性、定时可运行条件、发布未知不重发、真人登录恢复、真实数据口径和时效。Provider提供执行服务，Curis Employee仍承担责任；Account不是Workspace。

### 11. 哪些Core/shared？

身份/责任/范围、连接/权限、用途级能力验证、Context与引用、工作/执行/恢复、Search/Reader/受控Browser、文件与资源边界、排程/Attention、Result/Evidence、数据可信度、维护诊断。它们复用现有真源，不新增平行系统。

### 12. 哪些Domain-specific？

平台内容规格、Variant/Publication、账号策略；研发分支/测试/部署方案；研究评价方法；出版排版/格式标准；数据指标和归因。Terminal/Git/OCR/媒体工具为可复用专业能力，非全体员工默认安装，也不是全局导航。

### 13. 一级导航和Surface是否足够？

七一级导航足够容纳本轮需求，没有证据要求加第八区。原V1具体Surface不足：Model完整详情测试、浏览现场、文件/运行环境/Preview、恢复/备份等需真实工作面。V2定义29个主要工作面及48个能力配置/检查合同，不等新增77个设置页面。

### 14. 是否新增全局Surface？

需要全局可达的能力就绪/连接测试、恢复清单及网络/数据维护工作面，但嵌在既有Settings/CEO Attention/原Work中。Browser现场从Work打开，Employee不各建Browser App。全局对象Search沿既有合同；Command Palette仍Reserved，未借此扩权。

### 15. V1哪些删改？

撤销§41的完整性Ready推断、改§42对共享能力缺口的归类；扩充§20/28模型和连接、§24工具进展、§14资源工作、§26浏览接管、§27文件素材验收。无证据的固定条数/行数降为可验证设计参数；复杂模型配置不强塞单Drawer。保留范围、原身份、结果接受、Unknown不重发等正确语义。

### 16. 主要可见字段和交互覆盖了吗？

在本轮五类业务作为共享能力压力测试的范围内，已给29主工作面、48能力表达、核心对象字段、Model表、77设置及10张图。没有声称全部未来Domain编辑器已设计；尚未确认的能力接入边界明确列G1–G6，不藏在“按需”。此为候选表达覆盖，不是运行或视觉可用性接受。

### 17. Settings到字段级了吗？

是，77条均有14项必需信息。实际用户配置未读取标UNVERIFIED；动态默认按服务/适配器来源显示，不能伪填数值。只读能力事实不是可随意编辑的设置，Profile表单独说明来源/覆盖。

### 18. 还有UI设计师必须自行发明的逻辑吗？

不允许。已提出的普通/高级、Main/Utility、返回、编辑、验证和失败合同都明确；G1–G6由Product/Runtime/Capability/Security决定，UI必须等待相应正式合同，不能发明后台保证、登录保存、模型支持范围或恢复成功语义。视觉尺寸、字体等按后续正式Design Authority与真实可用性验证。

### 19. 真正达到FULL PRODUCT READY FOR UI了吗？

没有。结论为 **C. NOT READY — CAPABILITY GAPS REMAIN**。原因不仅是代码未实现：Browser接入/账号生命周期、模型能力与路由、后台位置/排程保证、外部效果恢复等产品承诺边界尚待正式仲裁；这些会影响可见字段与可执行动作。

### 20. 如果没有，还差什么？

G1 Browser执行合同；G2 Model Profile/多连接/用途与实测合同；G3真实后台与排程服务保证；G4审批/资源/副作用核验统一合同；G5五类业务所需首批工具、格式及结果验证矩阵；G6备份/更新/重连/在途恢复边界。CEO先Review本轮候选及范围，接受后才做PRODUCT BLUEPRINT DEEP RECONCILIATION。不是立即要求UI画不可验证按钮，也不是本研究擅自实施。

## Final disposition

Verdict: **C. NOT READY — CAPABILITY GAPS REMAIN**。
Disposition: 本轮完整性推导与候选表达交付；未获CEO接受；不改Current。
Owner: CEO / Product Review；G1–G6责任Owner见V2末节。
Next Action: CEO接受/修订本轮能力合同和边界候选。
Target Authority: 唯一Product Blueprint，在下一阶段显式仲裁。
Next Gate: CEO REVIEW → PRODUCT BLUEPRINT DEEP RECONCILIATION → 正式UI Gate。

**STOP FOR CEO REVIEW。NO BLUEPRINT WRITE / NO UI / NO RUNTIME CHANGE / NO COMMIT / NO PUSH。**
