# Curis Core Product Authority Repair

## Phase A.1 — CEO Role Decomposition Decision（2026-09-09，当前有效）

Status: Frozen
Authority Class: CURRENT / ACCEPTED CEO DECISION
Disposition: ROLE DECOMPOSITION ACCEPTED — previous employee-count gate CLOSED
Source: CEO “PHASE A.1 — CEO ROLE DECOMPOSITION DECISION”
Next Gate: PHASE B P0 IMPLEMENTATION CONTRACT FINAL CANDIDATE review；NO IMPLEMENTATION。

### Official Employee definitions / fresh Company instances

空间工程部在fresh Company bootstrap中物化 **6个不同canonical Employee instances**，分别来自以下 **6个Curis Official Employee Definitions**。不允许用一个Employee绑定六项责任替代初始六人；不是Frontend seed或Prototype名单。

|Official role / definition|Responsibilities|
|---|---|
|空间工程负责人|Team leadership；CEO沟通/Decision Gate；结果整合与最终交付责任|
|行业研究专家|行业/用户/竞品/经营实践研究；Evidence|
|经营方法专家|Operating Model、经营策略/工作方法、设计翻译输入|
|空间设计专家|Business/Workspace/Surface/Context；责任交互设计|
|搭建实施专家|Package、配置、能力集成、安装/实施|
|质量验证专家|Test、证据验证、缺陷/反馈、交付验收支持|

数据分析部初始至少 **1个canonical Company Analyst / 公司经营分析师**，历史默认display_name为 **司衡**，可编辑且不作为canonical identity key；主要工作面为 **Operating Intelligence / 经营洞察**。它与六名空间工程员工及same canonical CEO Assistant分别表达，不以Assistant代替原装专业员工。

以上是产品Definition，不在本轮指定数据库键或新增schema。official_employee_definition_id由后续已有template/catalog载体映射确定；这属于技术映射，不再是人数/岗位的CEO Gate。若需新canonical primitive/schema，仍须Architecture Review。
空间工程六岗位为正式名称，不虚构额外人格姓名。工作面/能力期待/上下游责任沿用A1.3已恢复语义；Current Runtime仍按真实Assignment/Execution/Capability校验，不把职责链变固定DAG。

### Instance / responsibility lifecycle

Official Definition → Company Employee Instance → current Responsibility Holder保持分离。用户之后可依合法机制编辑、替换Holder、增减人员；六人是fresh bootstrap承诺，不是永久人数锁定。
Responsibility requirement持续，Holder可改变；空缺诚实显示，不强制自动重招、不重写历史Work/Result。恢复bootstrap不得覆盖用户编辑或把后续主动减少误判成需要重新seed。
无Provider/Model授权也创建员工，显示需配置/暂不可执行；不伪造绑定。用户Business允许0，不自动创建Content Growth/RD/示例Business。

### Supersession and scope

下文历史恢复中的“六职责不等于六人/员工拆分UNRESOLVED/CEO DECISION REQUIRED”仅记录此前证据不足，**已由本次CEO新裁决关闭**；不把原型姓名追认成历史官方名单。Shared旧可兼任规则继续适用于后续合法Assignment，不能削减fresh六Employee承诺。
Phase B P0-A/B必须消费本表与更新验收；正式Issue的exact Allowed Files/owned hunks及现有定义载体复用检查仍需完成。人数Gate关闭不等于实现已授权。

PHASE B P0 IMPLEMENTATION CONTRACT: FINAL CANDIDATE
PHASE B IMPLEMENTATION: NOT STARTED / AWAITING FINAL REVIEW
FINAL UI MASTER: PAUSED
RELEASE: BLOCKED

本次裁决登记核验：三protected DB size/mtime_ns/SHA256前后一致、integrity均ok；git diff --check通过、staged=0。仅文档修订，无实现/应用启动/测试/commit/push。

## Phase A.1 — Historical recovery record（2026-09-09；人数Gate已由上方CEO裁决关闭）

Status: Frozen
Authority Class: CURRENT / ACCEPTED DECISION REGISTRATION
Disposition: Historical responsibility recovery preserved; prior employee decomposition gate SUPERSEDED / CLOSED by CEO Role Decomposition Decision above.
Owner: CEO / Product Authority; registration: Main Development
Source: CEO “PHASE A.1 BUILT-IN OPERATING ORGANIZATION AUTHORITY AMENDMENT”; historical sources below.
Next Gate: Phase B P0 final contract review / bounded Issue; no remaining employee-count decision gate. No implementation.
本节仅在明确范围替代Phase A下文§2/§11的“仅默认部门/全部人数未定”边界，不撤销其他Phase A裁决或已验收实现。

### A1.1 Built-in organization / initial Company

CURRENT TERM: **CURIS BUILT-IN COMPANY OPERATING ORGANIZATION / Curis 原装公司经营组织**。
空间工程部、数据分析部是 **CURIS BUILT-IN COMPANY OPERATING DEPARTMENT / Curis 原装经营部门**。旧System-default Company Support Department仅保留技术/历史别称，不能再把产品定义缩成seed。
它们是每个Company获得的Curis基础经营能力，不是用户Business、Business Template、Workspace/Marketplace Package或Demo data。

Company materialization把原装定义落实为该Company自己的canonical实例：
Company + CEO + same canonical CEO Assistant + 2 built-in Departments + 对应real AI Employees + Role/Responsibility/Assignment + 合法Work Surface关系。
USER OPERATING BUSINESSES可以为0；禁止自动创建内容增长/研发/示例Business。Company不是空组织；用户不需要先招聘空间工程员工才能发起建设。

Provider/Model未配置不阻止Company和员工创建；员工真实显示需配置/暂不可执行，不能伪造GRANTED、绑定、回复或credentials。Bootstrap不得依赖先输Key。

### A1.2 Historical evidence / classification

|Source / exact section|Authority / disposition|Recovered fact|Not proved|
|---|---|---|---|
|Company OS Shared Authority §9.4–9.5|FROZEN|六类固定Responsibility；Employee可变化/复用，一人可多责任；Leader组织Research/Operating/Design/Build/Quality，向业务Team交付|六个固定Employee定义、固定姓名、目录ID|
|Workspace Engineering Methodology §9.1–9.3|APPROVED CANDIDATE；职责链被Shared引用|六类岗位职责，Leader不代领域研究/开发；Operating收敛Handoff；Quality以真实证据验收|整篇Candidate自动Frozen；一岗位=一员工|
|Expert Handoff Protocol §0–1|APPROVED CANDIDATE / RESEARCH|研究收敛为下游可消费单份Handoff，不把全历史抛给设计|永久固定DAG或每次必触发P5|
|WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE §1.2|Domain IA evidence；Shared UI部分已SUPERSEDED|Result flow≠P5；仅真实Holder转移为Handoff；最终交付按真实责任判断|所有箭头都是Handoff；旧六区/像素继续有效|
|High_Fidelity_Remake.html: BUILD/chain及前置“全部为占位内容”|PROTOTYPE FIXTURE / VISUAL REFERENCE|高建、研真、方法、小录、实施、QA演示六类责任|任何一个为官方员工姓名/实例|
|VISUAL_DESIGN_REMAKE_CLOSURE|HISTORICAL approval evidence，原型非Authority|原型展示团队/工位行为|Fixture名单升为官方编制|
|Product Blueprint default organization；Operating Intelligence UX Consolidation §2/§3|Blueprint FROZEN；UX ACCEPTED / CONSUMED|Company Analyst岗位、数据分析部归属、产品称谓“司衡”|数据库已有该Employee，名称不可编辑或唯一查找键|
|Operating Intelligence UI Acceptance: Data truth boundary|FROZEN UI acceptance|设计“司衡/苏禾”是fixture；Frontend必须读真Employee identity|允许从截图/姓名创建或选择负责人|
|Default Functional Talent Verification 2026-08-18 §1–2|Research / candidate verification|空间工程核心员工/Company Analyst属Curis内置gap，不冒充外部市场Expert|外部Skill候选已经安装、验证或成为员工|
|Workspace Engineering P0.5 Issue / Package v2 Accepted Review|IMPLEMENTATION EVIDENCE|真实Employee/Role/Capability接线与有限Package substrate可复用|原装员工名单、完整默认组织已验收|

检索覆盖当前docs（含99_Archive）、issues、deliverables、历史设计HTML/Markdown，以及可用Git历史中相关路径。关键词覆盖空间工程/Workspace Engineering/Leader/研究/经营/设计/搭建/Quality/Test/Feedback/第一支团队/牧人。当前仓库文本与相关可用Git历史未检出“牧人”的可定位定义；这是本次搜索未恢复，不证明任何仓外聊天从未确认。未读取秘密/聊天私有日志，未把代码seed升为Authority。

**Recovery conclusion：六类Responsibility已恢复；official Employee definition数量/合并拆分仍未被Frozen来源唯一确定。六项职责 ≠ 六名员工。ROLE DECOMPOSITION: CEO DECISION REQUIRED。**

### A1.3 SPACE ENGINEERING OFFICIAL TEAM — responsibility definitions

以下每行是已恢复岗位责任，不是未经批准的新Employee名单。所有行department=空间工程部（CEO CURRENT DECISION）；official_employee_definition_id=UNRESOLVED（未恢复已接受稳定ID，Phase B须映射现有定义载体，不得现在建表/编造ID）；display_name=UNRESOLVED。不得将下列行号或岗位文本当Runtime identity。
Primary Work Surface为既有空间工程建设任务/Employee Main Workstation，详情沿用Utility；具体路由/固定Workspace ID未定，不得为组织工作面伪造用户Business。

|Employee / Role slot|Role / responsibilities|Primary Work Surface|Capability expectations（需求，不是已Granted）|Handoff / leader relationship|Status|
|---|---|---|---|---|---|
|Leadership|空间工程Leader；收CEO目标、澄清需求、组织团队/讨论、分工、异常、整合结果、CEO Gate沟通、最终交付负责|空间工程部门责任/建设任务工作面；same Employee Workstation|需求理解、团队协作、结果综合、Gate/证据判断；不得偷偷代研究/开发|向CEO负责，组织其他责任；CEO可直接找员工，Assistant可协调但不代专业部门|Role/责任FROZEN + CEO CURRENT DECISION；员工拆分UNRESOLVED|
|Industry / Business Research|行业研究/Domain Expert；行业、模式、竞品、用户、经营方法、专业工作方式|建设任务研究Workstation + bounded资料/证据|研究、来源验证、业务分析；外部research/tool须合法绑定|向Operating Model交付研究/证据，受Leader统筹；交付文档不自动转责任|FROZEN责任；员工定义UNRESOLVED|
|Operating Model / Design Translation|经营/运营方法；把研究转Operating Model、工作方式、信息结构、Workspace需求与Design Language输入|建设任务经营方法Workstation|经营建模、研究综合、单份Product Handoff、用户语言翻译|承接Research，交给产品/空间设计；Leader整合；同员工兼任须CEO拆分裁决|FROZEN责任 + CEO CURRENT DECISION；人数UNRESOLVED|
|Workspace / Product Design|产品/空间设计；Business Home、Workspace、Professional Surface、Context/Tools/Responsibilities/Handoff的产品映射|建设任务设计Workstation；Result/设计证据Utility|产品设计、专业到用户语言翻译、消费Frozen design，不重定义上位Authority|承接经营模型，向Build交付合法设计；向Leader反馈范围/冲突|FROZEN责任；员工定义UNRESOLVED|
|Build / Implementation|搭建实施；Package/配置/能力接入/必要实现/安装/Company integration|建设任务Build Workstation + 既有Package/Execution引用|现有Package/实施能力；只有真实Core gap才bounded代码Issue；权限由既有执行链判断|消费Design，交付Artifact/Result给Quality；失败反馈不伪装完成，向Leader负责|FROZEN责任；员工定义UNRESOLVED|
|Quality / Test / Feedback|质量/验收；检查Installed、Operational、Company Integrated、Operating，发现/反馈/修正/交付|建设任务验收Workstation + Evidence/Result|真实测试/证据审阅、反馈；不能用Mock/截图替代运行|反馈Build/Design，向Leader提交验收事实；最终业务Team接手按真实责任关系，不机械P5|FROZEN责任 + CEO CURRENT DECISION；独立验收方法见Candidate，不据此擅增人数|

六类责任都必须有合法覆盖，但允许依已裁决编制由同Employee承担多个Assignment。职责清单不是Scheduler/DAG，不强制固定执行顺序。最终handoff始终保持Review≠Handoff≠P7；CEO参与Decision而非手点每个技术步骤。
**SPACE ENGINEERING OFFICIAL EMPLOYEE DEFINITION COUNT: UNRESOLVED — CEO DECISION REQUIRED**。不得用Prototype的6人表替代裁决。

### A1.4 DATA ANALYTICS OFFICIAL TEAM

- official_employee_definition_id：**UNRESOLVED**，未恢复目录稳定键；岗位定义已明确，技术承载由Phase B复用审计确定。
- display_name：**司衡 — ACCEPTED产品称谓恢复**（Blueprint及已消费UX来源）；不是锁死姓名、查询键或已有实例证明。UI中的同名fixture仍是fixture，实际显示Company Employee可编辑name。
- Role：**Company Analyst / 公司经营分析师 — FROZEN岗位 + CEO CURRENT DECISION**。
- Department：**数据分析部 — FROZEN / CEO CURRENT DECISION**。
- Staffing minimum：**至少1 canonical Employee instance — CEO CURRENT DECISION**；不是整部门上限1，不扩增储备Analytics Engineer等岗位。
- Responsibilities：Company-level、cross-Business、Business-scoped分析；Data Trust；FACT/INTERPRETATION/UNKNOWN/RECOMMENDATION；Report/Evidence/Decision support/CEO经营问题。**FROZEN既有分析责任 + CEO CURRENT DECISION**。
- Primary Work Surface：**经营洞察 / Operating Intelligence — CEO CURRENT DECISION**；Employee Conversation/Detail使用同共享模型。
- Capability expectations：合法范围数据/证据读取、分析/可视化/报告、真实Model/Skill/Tool绑定；UNAVAILABLE/UNKNOWN按实际呈现，不把研究候选工具写成默认可用。
- Handoff：分析Result/Report/Evidence→CEO/适用Leader→必要Decision support；报告≠Decision≠自动Handoff；实际责任转移才有交接，具体每次接收者按真实scope。
- Leader relationship：承担Company分析责任，可按Business Assignment服务；CEO是经营问题/决策受众，**数据分析部单独固定Leader员工/名字UNRESOLVED**，不把Analyst自动声明为部门Leader。
- Business=0时真实Analyst仍存在；显示“当前暂无经营业务 / 暂无足够经营数据”，不是无负责人或假数据Dashboard。

“司衡”的产品称谓与UI fixture纪律不矛盾：恢复定义的可编辑称谓，不将画面中人物当真实实例，不由姓名解析Assignment。
**DATA ANALYTICS BUILT-IN STAFFING MINIMUM: 1 CANONICAL EMPLOYEE INSTANCE。**该下限不再UNRESOLVED。

### A1.5 Official definition / instance / holder

**CURIS OFFICIAL EMPLOYEE DEFINITION → materialize → COMPANY EMPLOYEE INSTANCE → assignment → CURRENT RESPONSIBILITY HOLDER**。

Definition只提供岗位/职责/推荐能力的创建、恢复及推荐配置来源，不是第二套Employee truth。真实运行使用现有canonical Employee及其关系；本登记中的“employee instance”是产品概念，不授权名为employee_instances的新表。
Company实例必须真实挂Department、Role、Responsibility、Assignment、Execution Identity，以及按合法机制存在/缺失的Capability/Skill/Model binding；provider未配不等于员工不存在。
Responsibility requirement持续；Holder可变化，Executor可none。不能把组织责任永久绑定official definition ID或name。

原装/招聘/用户创建/编辑共用同Employee system和Detail/Edit，不建built-in专用Profile。只按现有支持字段编辑name/avatar/role presentation/skills/capabilities/model-provider/preferences/允许的allocation，不在本轮增字段。
用户可替换合法Holder时，Requirement保持、历史Work/Result不改写；V1若未支持替换，记录后续，不扩Runtime。缺Leader/Holder时展示组织能力缺口，不假装正常。

### A1.6 Product projection / teaching reference

原装Employee已是Company Employee，不是Talent待招聘Expert。Talent用于新增/招聘/扩展；编辑走Current Employee Edit。
Organization初始显示两原装部门及真实员工，用户Business暂无并有启用入口。空间工程团队在用户新Business intent前已存在，缺模型可配置但不要求用户先建员工。
数据分析部→Company Analyst→Operating Intelligence Work Surface→Analysis/Report/Evidence→Decision Support；页面与Employee/Department分离。

原装Employee是同一Employee系统的官方示范：Profile使用户理解identity、Department、Role、Responsibilities、当前服务范围、Work Surface、Skills/Capabilities、Model/Provider真实状态、当前Work、最近Result、Conversation及可编辑配置。**这不把Conversation塞进Utility**：仍Main Workstation+Utility Detail，共用同canonical identity。
默认不显示tenant_private、catalog JSON或runtime refs；不新建字段或后台系统。

### A1.7 Phase B / Final UI gates

P0-A=COMPANY BOOTSTRAP + BUILT-IN OPERATING ORGANIZATION：Company/CEO/Assistant/两原装部门/official Employee instances/Role/Responsibility/Assignment同一可恢复bootstrap，用户Business=0合法，Key不是前置。
P0-B=BUILT-IN RESPONSIBILITY + WORK SURFACE INTEGRATION：空间工程Team、Company Analyst、Organization、Operating Intelligence、Business activation。
开工前复用审计现有employee/role templates、capability definitions、seed/catalog及official定义载体；若必须新增canonical Official Employee Definition primitive/schema，STOP FOR ARCHITECTURE REVIEW。不得以文档新增概念为建表许可。
具体空间工程Employee拆分/数量未裁决前，该物化部分不得由开发猜；Phase B implementation保持暂停。

新增验收：freshCompany真员工/真Assignment/Business0/sameAssistant/Analyst可见；无Key也存在但不可执行；通过已有Edit修改一支持字段→restart→sameEmployee保留修改；bootstrap重复/失败恢复不重置用户编辑；如V1支持Holder替换则测试Requirement/历史连续，否则明确后续。
Final UI未来必须覆盖Company初始组织、空间工程Team、分析Team/Insights入口、官方Employee Detail/Edit、用户Employee对照；同UI模型，不画两套员工产品。
Resume Gate：Phase B built-in organization、official Employees、Business activation、Four-Pane、floating Assistant真实验收；Final UI持续PAUSED / Release BLOCKED。固定部门Workspace、改名/删除政策、精确布局细节仍未裁决。

### A1.8 Supersession / status

- Phase A“具体员工/人数全部UNRESOLVED”仅部分SUPERSEDED：Company Analyst最低1、真原装Employees/Role/Assignment必须存在已由本轮裁决；空间工程六责任恢复，官方Employee拆分仍待CEO。
- Phase A仅“默认部门”表述被原装经营组织产品身份替代；自动materialization只是实现方式。
- 已验收Runtime能力原样保留。本轮无代码/Frontend/Schema/DB/Figma/Provider/App启动、无stage/commit/push。
- 三个protected DB沿用本登记§12相同fingerprints，开始/结束immutable读取均ok，size、mtime_ns、SHA256完全不变。git diff --check与本登记/Phase B合同本地链接检查通过；staged=0，status开始/结束均738项。未运行业务测试或App，文档校验不等于实现验收。
- 本轮仅修订既有11份文档：Authority Repair、Phase B Contract、Blueprint/Master/Shared/UI、Current State/Pointer/Completion/Backlog/Change Log；未创建新员工定义表、名单文件或平行Authority。历史方法论/原型/审计保持原证据状态。

BUILT-IN OPERATING ORGANIZATION: AUTHORITY REGISTERED
SPACE ENGINEERING OFFICIAL TEAM: RESPONSIBILITIES RECOVERED / EMPLOYEE DECOMPOSITION CEO DECISION REQUIRED
DATA ANALYTICS OFFICIAL TEAM: REGISTERED
OFFICIAL EMPLOYEE MODEL / EDITABLE COMPANY INSTANCE: REGISTERED
PHASE B CONTRACT: UPDATED / READY FOR REVIEW — IMPLEMENTATION PAUSED
FINAL UI MASTER: PAUSED
RELEASE: BLOCKED

---

Status: Frozen
Authority Class: CURRENT / ACCEPTED DECISION REGISTRATION
Disposition: ACCEPTED — CEO Phase A decisions registered, 2026-09-09
Owner: CEO / Product Authority; registration: Main Development
Source: CEO “PHASE A: CORE AUTHORITY REPAIR”, 2026-09-09; the three Core Product audit reports.
Target Authority: existing Product Blueprint, Master Map, Company OS Shared Authority, Workspace Shell Contract and UI Blueprint.
Next Gate: CEO / ChatGPT Phase A review; Phase B implementation Issue approval. No implementation authorized by this registration.

## 1. Authority and applicability

本登记是既有 Authority 的有界修订记录，不是第二份 Blueprint。Product Blueprint 仍为唯一 Product Authority；Shared/Shell在其职责范围展开，Master Map/UI Blueprint消费这些规则。本轮CEO明确裁决回写原文件，因此不是Review覆盖Frozen。优先级为 FROZEN → ACCEPTED → CURRENT AUTHORITY → APPROVED CANDIDATE → REVIEW → IMPLEMENTATION → HISTORY；在同一适用范围内，本次明确supersession替代下列旧解释。未列冲突处保持原规则。Source代码和截图只证明实现，不定义产品。

审计输入（REVIEW/EVIDENCE，不升级为产品定义）：
- [Truth Ledger](CURIS_CORE_PRODUCT_TRUTH_LEDGER.md)
- [Authority Reconciliation](CURIS_CORE_PRODUCT_AUTHORITY_RECONCILIATION.md)
- [Deviation Register](CURIS_CORE_PRODUCT_DEVIATION_REGISTER.md)

## 2. Company bootstrap and support organization

新Company必须具有 Company、CEO identity、same canonical CEO Assistant、空间工程部、数据分析部。用户经营Business可以为空；不得默认创建内容增长、研发或示例Business，除非用户真实启用。

Phase A旧称SYSTEM-DEFAULT COMPANY SUPPORT DEPARTMENT已由A.1收敛为CURIS BUILT-IN COMPANY OPERATING DEPARTMENT，不是Business、Workspace、Template或fixture。人数边界以A.1为准：数据分析至少1真实Employee已确定；空间工程official Employee数量/拆分仍需CEO决定。固定Workspace ID、删除/改名/隐藏策略仍UNRESOLVED；不得据此编造员工或业务。

空间工程部负责：CEO经营目标 → 需求理解 → 行业/业务研究 → Operating Model → Business/Workspace空间设计 → implementation/build → quality/test → Team/Workspace交付 → 持续演化。Leader是业务领导者；task routing only-on-exception只约束WHO路由，不削弱持续业务领导力，不创建特殊Leader身份。

数据分析部承担Company-level/cross-Business analysis、Operating Intelligence、Report和Decision support。Company Analyst归属必须由canonical Responsibility/Assignment证明；role文本含“分析/经营”不能选定负责人。Business Analyst可以跨业务Allocation服务，不因此改变functional department identity。经营洞察是产品区，数据分析部是组织主体：组织责任 → 分析能力 → 产品Surface。

## 3. Ownership and activation

Company → Department → Business → Workspace。
Department是组织责任边界；Business是持续经营身份、方向、目标、规则和团队经营上下文；Workspace是Business内真实工作环境。Business≠Workspace，Project≠Business，Workspace≠Department。

标准启用：CEO intent → read Company → reuse/propose Business → 必要CEO Decision Gate → canonical Department relation → canonical Business + atomic first Workspace → legitimate Team/Leader/Employee Responsibility → Operating。保持既有原子创建与fail-closed校验；初始DRAFT不等于已有完整经营能力。没有支持能力可诚实表达缺口，不伪造团队。

Organization / Business Space提供合法业务启用或选择入口，业务为空时能回答“公司准备经营什么业务？”。不是模板商店、Studio技术表单，不要求CEO配置DAG/Router/Workflow graph。CEO可直接创建，也可委托空间工程部；建设可包含研究、经营模型、Workspace/Team提案、能力缺口、build/package/install/test/handoff，必须bounded、可解释、可被合法CEO Gate打断。Business创建≠安装成功≠实际经营成功。

## 4. Generic / Professional / Domain

Generic Workspace是合法、真实、可经营的通用环境。Professional Workspace是业务形成稳定专业方法、工具和语义时的目标专业形态，不是所有Workspace的强制前置。Generic不得吞并Professional；长期经营的真实责任/Operating Team要求不被取消。旧“所有长期Workspace终态必须Professional”的普遍强制解释被替代。

内容增长和研发不是默认支撑Department，而是用户启用的经营Business / Professional Workspace portfolio。Content Growth Business与具体Workspace、Channel/Account不同；RD Business下的专业Workspace可含RD Project作为域对象，但Project不是Company或通用执行父节点。

XHS / Douyin / TikTok / YouTube / Bilibili默认是Channel/capability context；Channel≠Workspace，Channel Account≠Channel。旧XHS/Shortvideo Workspace作为兼容/历史专业实现保留，不代表Current Content Growth完整identity或全渠道能力已交付。不得由平台名自动生成Business或Workspace关系。

## 5. Conversation, identity and attention

持续Conversation identity可跨Assignment保持；same Employee允许multiple topics。Assignment/Workspace/Work是消息发生时的合法context/provenance，不是必须重新创建Conversation的永久identity。
每条message保留当时合法scope；每次新消息/读取引用重新验证授权，不因历史参与而获得全部历史Workspace数据。旧scope隔离不等于强制拆分Conversation。历史消息保持当时事实，不迁移或复制新聊天库。

Sidebar = GLOBAL CONVERSATION QUICK ACCESS：persisted canonical recent Employee-backed及Task/Work-backed conversations，按message activity排序、bounded subset、现有范围搜索；dismiss≠delete；reopen same identity。不是Assistant、Employee/Work清单或第八区。

CEO Assistant保持同canonical identity和durable conversation。Employee、Assistant、Meeting共享词汇/引用/Composer基础不等于强制相同业务生命周期。Result Returned≠Viewed≠Accepted；显式成功查看才写现有Viewed Receipt；Decision使用自身生命周期。既有Usage ledger不改。

## 6. Current spatial authority

Four-Pane = Navigation / Context / Main / Utility，是职责，不是四列常驻。默认Nav+Main成立，Context/Utility按需，Main在辅助Pane关闭后仍独立成立。沿用Pane-local Header、T1–T3、Resizable及Utility Maximize，不冻结旧Research像素。

|Pane|Current responsibility|Boundary|
|---|---|---|
|Navigation|七一级区、Conversation quick access、Company object search、CEO identity/settings|不是Employee/Work list或Assistant Pane|
|Context|当前domain/work的navigation、object collection、bounded context；可收起|不长期放完整Employee profile、Conversation、Result正文|
|Main|当前Reading / Working / Operating主工作面|辅助Pane关闭不破坏主工作|
|Utility|Detail、Editor、Evidence、Professional Tool、Result inspection；默认收起，可maximize|不是固定结果/员工/Assistant栏|

READING=理解内容/资料/结果/证据；WORKING=与Employee/Work/Meeting持续工作；OPERATING=方向/责任/状态/结果/问题/下一判断。冻结职责与心智，不新增Runtime状态。

|Object|Spatial mapping|
|---|---|
|Business|OPERATING Main|
|Workspace|selected Domain Main，保留适用Shared Work Area|
|Employee Conversation / Conversation|WORKING Main|
|Employee Detail|Main Workstation + Utility detail；Utility不承载Conversation|
|Work|WORKING Main|
|Result|READING Utility / maximized Reading|
|Evidence|Utility|
|Knowledge|READING Main|
|Operating Intelligence|OPERATING analysis / Report Reading|
|Meeting|WORKING Main|
|Decision|既有P7 + Utility Evidence，不新建审批语义|

CEO Desk是Operating Surface，承载Attention、Decision、Result、Operating matters，不是Assistant本体或聊天首页。

## 7. Floating / overlay / navigation

CEO ASSISTANT = GLOBAL FLOATING ASSISTANT：可拖动、可收起/展开、跨七区持续，切页不销毁；same canonical identity / same durable conversation；只消费当前合法Context；不占Four-Pane、不预留布局空间、不等于Sidebar或Desk inline-only。旧“draggable=Vision only”适用结论明确SUPERSEDED。

INTERACTION DETAIL: TO BE DEFINED IN FINAL UI MASTER。Exact width、initial X/Y、snap、position memory、shortcut、drag physics本轮不定义，不将当前CSS数值升为合同。最低floating/drag/collapse能力不被这些细节阻断。

Temporary overlay/modal可用于start/create/config/select/confirmation，包括Start Meeting；不是所有Modal都为审批。高风险动作仍需明确确认，P7不变。Floating是持续全局layer；Drawer是bounded edit/detail。旧“Modal只用于高风险”及把详情编辑用途当成所有Overlay禁令的解释SUPERSEDED。

七一级区固定：CEO工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议。Conversation、Assistant、Model/Settings是global utility，不是第八区。

## 8. Workspace Engineering substrate

Curis Core + Declarative Workspace Package继续成立。Package持有bounded professional composition；Core持有truth、identity、execution、安全和references。不把专业Workspace重新全部硬编码成Frontend monolith；也不承诺任意JS扩展或无限生成能力。

Workspace Package v1/v2有限renderer/install/migration已验收；Methodology APPROVED CANDIDATE不因引用变成全部Frozen或已实现。默认工程组织和完整建设承接仍是实现缺口。

## 9. Supersession and route intended use

|Old claim / location|Disposition|Current meaning|
|---|---|---|
|Assistant Historical Product Truth Recovery: draggable=Vision|SUPERSEDED for current applicability|§7；历史文档保留原日期证据，不得拒绝当前floating合同|
|Project-as-Business / Project-as-Company|SUPERSEDED；旧对象COMPATIBILITY ONLY|canonical Company→Department→Business→Workspace；Project可为RD域对象|
|Master Map旧账号通常一Workspace、UI旧平台空间例|HISTORICAL / COMPATIBILITY ONLY|Channel≠Workspace；不得推导新业务结构|
|Shared/Master旧Assignment Conversation Continuity隔离|SUPERSEDED interpretation|§5；消息/引用scope隔离，不强制切换Conversation identity|
|旧长期Workspace必须Professional|SUPERSEDED universal prerequisite|§4；保留真实团队责任|
|Studio free-form business ref|LEGACY / COMPATIBILITY UNTIL RECONCILED|不具Current Business activation Authority；保留后端拒绝无效父关系|
|旧Knowledge/Meeting/App Entry implementation pending说明|HISTORICAL scoped checkpoint|按已接受Implementation registrations；不撤销具体未来连接器缺口|
|2026-09-08 PRODUCT COMPLETE/no blocking P1|SUPERSEDED whole-product inference|局部accepted chains保留；完整合同待reconciliation|

路由分类是intended use，不代表本轮改路由或已封闭遗留入口。以下前缀均为 /ceo-office/：

|Route|Classification / intended use|
|---|---|
|root、business、organization、talent-market、analytics、knowledge、meeting|CURRENT primary areas|
|conversation、organization/employees/[id]、workspace、workspace/installed/[workspaceId]、workspace/software、capabilities、settings|CURRENT canonical deep surface / utility，不能新增一级区|
|workspace/xhs、workspace/shortvideo|COMPATIBILITY accepted historical professional instances|
|execution/tasks/[id]|CURRENT bounded Result/Execution evidence deep link，不是主经营区|
|projects/**、execution/runs/**|COMPATIBILITY legacy/domain references，不能作为canonical Business入口|
|reports/**、decisions、strategy-room、brainstorm/**、workspace/department/**、knowledge/memory|LEGACY intended use；当前经营洞察/P7/Meeting/Knowledge等canonical入口优先|
|workspace/studio|LEGACY / COMPATIBILITY UNTIL RECONCILED，禁作Current activation authority|
|execution（列表）、company-runtime、runtime-trace、execution/pipeline/**|DEV / INTERNAL；非CEO默认经营路径|

不删除任何route；Phase B须检查真实消费者/return，避免盲删兼容数据和历史链接。

## 10. Traceability

|Final Rule|Authority Source|Current Registration|Phase B Impact|Final UI Impact|
|---|---|---|---|---|
|Company bootstrap|Blueprint default support; CEO §3|§2 + Blueprint修订|P0-A|freshCompany可空业务|
|Support departments|Shared §9.4–5; CEO §4–6|§2|P0-B|真实组织主体，非fixture|
|Business activation|canonical spine; CEO §7–9/24–25|§3|P0-C|经营意图入口|
|Generic/Professional/Channel|Shared §0.1/9.1A; CEO §10–11|§4|identity/return|不把渠道变空间|
|Four-Pane|Shell §0–3; CEO §13–17|§6 + Shell修订|P0-D|adaptive职责，不四列|
|Reading/Working/Operating|Blueprint/UI; CEO §18–19|§6|P0-D/P1 projection|逐对象Main/Utility|
|CEO Assistant|CEO §20–21，替代历史Vision解释|§7|P0-E|全局floating，细节未定|
|Conversation Sidebar|accepted Conversation review; CEO §22|§5|KEEP + nav integration|最近/活跃，非第八区|
|Workspace Engineering|Shared §9.4–5; accepted Package review|§2/8|P0-B|组织交付≠安装|
|Operating Intelligence ownership|default organization; CEO §6/26|§2|P1 Analyst|assignment证明作者|
|Seven areas|UI/Shell; CEO §29|§7|P1导航|唯一七区|
|Current completion scope|CEO §32–35|§11 + Current载体|P0-F已治理收口|Final UI暂停|

## 11. Current status and preserved acceptance

CORE PRODUCT MODEL: AUTHORITY REPAIRED / IMPLEMENTATION RECONCILIATION PENDING
CORE ORGANIZATION MODEL: RECONCILIATION PENDING
CORE SPATIAL MODEL: RECONCILIATION PENDING
ACCEPTED CAPABILITY CHAINS: PRESERVED
SCOPED CAPABILITY IMPLEMENTATIONS: ACCEPTED within their recorded verdicts
WHOLE PRODUCT CONTRACT: NOT YET RECONCILED
FINAL UI MASTER: PAUSED / NOT READY
RELEASE: BLOCKED / PUBLICATION NOT AUTHORIZED

保持：canonical spine/ParentResolver/atomic/fail-closed、Employee identity、Holder/Executor分离、Conversation/references/Usage、ResultViewed/Attention、Knowledge、Meeting core + autonomy accepted candidate、General lifecycle、Package v1/v2、P7、Work/Execution。不可将candidate升为final；Meeting自然multi-cycle evidence仍单列，不因本轮重新消耗云模型。

Final UI Resume Gate = PHASE B CORE PRODUCT P0 RECONCILIATION ACCEPTED，至少Company bootstrap、组织骨架、共享Four-Pane、Assistant最低合同真实落地。未来Final UI读取：本登记 → Blueprint → Shared → Shell → UI Blueprint → Visual Standard → Surface Inventory → Gap Review；不是从截图反推模型。

Phase B见 [Core Product Reconciliation Contract](CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_CONTRACT.md)，本轮不实施。

## 12. Preservation / governance verification

只允许文档治理修订，NO CODE / FIGMA / DB WRITE / APP LAUNCH / TEST RUN / COMMIT / PUSH / STAGE / RESET / CLEAN / STASH。
本轮开始HEAD bb72916daba3ae9555914d03bdb7fcea9953ab9c，status736项，staged0，保留全部已有成果。
三个DB只用immutable readonly连接核验。开始fingerprints：
- repo data/curis.sqlite：1232896；mtime_ns1786873339955841838；SHA256 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6。
- repo backend/data/curis.sqlite：1277952；mtime_ns1786783659967572836；SHA256 a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4。
- /Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite：1536000；mtime_ns1788614881473263746；SHA256 d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617。
开始与交付前size、mtime_ns、SHA256完全一致，三个integrity_check均ok。文档中的源路径相对主仓库，不是worktree Authority。
交付校验：两新文档本地Markdown链接通过；git diff --check通过；staged=0；status由736到738（新增本轮两文档）。未运行应用或业务测试，不将文档检查称Runtime验收。

### Exact documentation scope

- 新增本登记与Phase B Contract（均位于docs/reviews）。
- 原位修订docs/01_Product/Curis_Product_Blueprint.html、Curis_Product_Master_Map.md、Curis_Product_UI_Blueprint.html；docs/03_Design/Curis_Company_OS_Shared_Authority.md、Curis_Workspace_Shell_Contract_And_Shared_Patterns.md。
- 同步docs/00_Context/CURRENT_STATE.md、PRODUCT_DOCUMENT_POINTER.md；docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md、CURIS_V1_EXECUTION_BACKLOG.md；docs/08_Change_Log/CHANGE_LOG.md。
- 在docs/reviews/CURIS_CEO_ASSISTANT_HISTORICAL_PRODUCT_TRUTH_RECOVERY.md追加Current适用性更正，不删除原历史结论。
- Visual Standard仅消费，未改token/视觉规则；Methodology仍Approved Candidate，Package accepted implementation保持；三份审计报告保持原证据状态。

### Final Phase A verdict

PHASE A AUTHORITY REPAIR: COMPLETE
CORE PRODUCT / ORGANIZATION / SPATIAL AUTHORITY: RECONCILED
CURRENT STATE: CORRECTED
PRODUCT COMPLETE CLAIM: NARROWED
PHASE B CONTRACT: READY FOR REVIEW / NO IMPLEMENTATION
FINAL UI MASTER: PAUSED
RELEASE: BLOCKED

尚未决定的是明确保留的交互/人员/管理细节，不是本次核心合同冲突；不将UNRESOLVED升级。STOP FOR CEO / CHATGPT PHASE A REVIEW。
