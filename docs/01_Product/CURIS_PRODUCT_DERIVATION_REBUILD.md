# CURIS PRODUCT DERIVATION REBUILD

> Status: Draft（产品推导工作稿 · 供 CEO 逐条核对）
> Authority Class: REVIEW — 本文件是可审查推导记录，不修改任何 Authority；所有缺口只登记进 GAP REGISTER，不直接进入产品权威。
> Updated: 2026-09-14 · 第一轮 PART A–F + ROUND 1 CORRECTION（C-01~C-18 已回写，详见 CURIS_PRODUCT_DERIVATION_ROUND1_CORRECTION.md）· STOP FOR CEO REVIEW
> 上游：CURIS_PRODUCT_DEFINITION_REBUILD.md（已确认方向：帮助一个普通人通过 AI 员工同时建立、管理并持续经营多项不同真实业务）。
> 事实依据：Company OS Shared Authority / Workspace Shell Contract / Content Growth Domain Authority / Product Blueprint 5.6 / ADR-0046 / CURRENT_STATE / 前端实现证据。
> 标注：【事实】项目资料记载；【分析】由事实推导；【判断】本轮结论，待核对；【推导不足】= 证据不够，暂不下结论。

---

# PART A — 推导方法与统一判断规则

**A.1 唯一推导链**（每一项产品结论都必须沿这条链走，不许倒置）：
经营目标 → 业务行为 → 业务对象 → 组织关系 → 员工责任 → 所需能力 → 能力来源 → 权限与上下文 → Work → Result/Evidence → 用户需要看到什么 → 应该放在哪里 → 形成产品模块。

**A.2 单项推导统一格式（A–N）**：
A 真实经营目标（用户想完成什么）｜B 真实业务行为（现实里必须发生什么）｜C 必要对象/关系（系统必须知道什么）｜D 必要能力（员工/业务/公司需要什么能力）｜E 外部依赖（Model/Skill/MCP/Connector/External Agent/Account/API/Computer Access/Knowledge/File/External Service）｜F 权限与上下文（谁能用、在哪个业务、什么 Context、什么必须隔离）｜G 产品必须因此增加什么｜H 放在哪里｜I 为什么放这里｜J 为什么不放别处（至少检查一个易混淆位置）｜K 用户最终看到什么｜L 用户能做什么｜M 反例/压力测试（换一门生意是否仍成立）｜N 一句话结论。

**A.3 三层分类规则**（每个推导产物必须归类其一）：
① **COMPANY OS CORE**：所有生意共用的运行语法（身份、任职、对话隔离、工作/结果/证据、权限、用量、外部对象与连接的通用抽象）。
② **BUSINESS PROFESSIONAL MODEL**：只有特定生意才需要的专业对象与专业现场（发布记录、订单、章节、代码差异、选题信号）。
③ **INFRASTRUCTURE / PROVIDER**：支撑执行的能力供给（模型、外部 Agent、Skill、工具、MCP、连接器、接口授权）。

**A.4 放置判断规则（"用户此刻在管理什么"）**【判断】：
- 在管理"怎么经营它" → Business / Workspace
- 在管理"谁负责它" → Team / Employee / Responsibility
- 在管理"员工会什么" → Employee 能力
- 在管理"公司能获得什么新能力" → Talent & Capability
- 在管理"这个能力技术上怎么连" → Settings / Connection / Provider
- 在管理"谁被允许用它" → Permission / Assignment
- 在管理"现在结果怎么样" → Result / Operating Intelligence
- 在管理"我要继续跟谁工作" → Conversation
每次放置决定必须能用这条规则解释。

**A.5 共性抽象验证规则**：任何想进 COMPANY OS CORE 的抽象，必须至少在两个完全不同的业务上推导通过；通不过的写【推导不足，暂不下结论】。

**A.6 本轮纪律**：不进入 Authority；不设计导航/页面/UI；发现缺口只登记（见 GAP REGISTER）；与现行 Authority 有张力处如实标注，不自行改写。

---

# PART B — Employee 跨 Business 完整推导（林墨案例）

**B.0 案例**：公司有一名设计员工林墨，同时服务三门生意——内容增长（封面/配图/视频视觉/品牌一致性）、小说（封面/人物视觉/宣传物料）、电商（商品主图/详情页/广告素材）。

**观察**：现实中，老板只雇"一个设计师"，但他在三门生意里是三种工作状态：做电商主图时不应被小说的世界观设定干扰；他给小说画的封面经验，会让电商主图也做得更好；老板月底想问"我的设计师这个月都在干嘛"。
**问题**：如果员工"属于"某一门生意，他服务第二门生意时就等于重新入职（另一份身份、另一份履历）——这正是 1.16 号问题（业务越多管理越崩）在人员维度的形态。
**推导**：必须把"这个人"与"他的每一条任职线"分开建模。人是稳定的；任职线（在哪个生意、什么岗位、负责什么、能用什么、聊过什么、干过什么、结果如何）是按业务隔离的。

**逐问推导（对应 CEO 问题 3.1–3.12）：**

**B·3.1 什么稳定不变？**【判断】
跟随"这个人"的三样：①**Employee Identity**（姓名/头像/履历——他的"人籍"）；②**能力清单**（会什么：视觉设计、会用哪些工具——注意是"会不会"，不是"被允许在哪用"）；③**个人经验/通用记忆**（跨业务有效的技法与风格，如"他擅长的排版手法"）。
反例：若身份随业务变，他换生意就是另一个人，履历断裂，CEO 无法回答"我有几个设计师、他们分别怎么样"。【事实】现行模型（Official Definition → Company Instance → Holder、`EMPLOYEE_IDENTITY_CROSSES_SURFACES`、`NO_EMPLOYEE_DUPLICATION`）与此一致——本轮为验证，非新增。

**B·3.2 什么随 Business 改变？**【判断】
岗位名（Role——内容业务叫"视觉设计"、电商业务可以叫"商品视觉"）、当前责任（Responsibility）、任职关系（Assignment）、工作上下文（当前现场/对象/相关资料）、Work、该范围的对话线、该范围的使用授权（Permission to use：能用哪个账号/工具/资料）。
分界线一句话：**"他是谁"稳定；"他在为谁干什么"变化。**

**B·3.3 Employee 属于 Company、Department、Business 还是 Team？**【判断】
- **Company**：身份归属——他的人籍在公司（全员层）。
- **Department**：编制归属，可属可不属（原装员工属；用户员工可不属）；是组织表达，不是干活前提。
- **Business / Team**：不"属于"——通过任职线（Assignment）**服务**；同时服务多门，不复制身份。
【事实】现行 `SERVICE ≠ MEMBERSHIP`、`ORG_AND_SERVICE_ORTHOGONAL` 与此一致。
反例：若员工硬性隶属单一 Business，跨业务复用必须复制员工——公司里出现"三个林墨"，履历、花销、管理全部×3。

> **ROUND 1 CORRECTION — 2026-09-14（C-01）**：上句"Department=编制归属，可属可不属"收口过早。已证明的最小结论：Department 现阶段仅被证明三件事——①承载部门级职责与 Assignment（原装两部门的职责链挂在部门范围：空间工程/数据分析对公司负责）；②员工的行政分组与组织呈现；③公司级支撑职能的组织容器。Department **不**限制跨业务服务、**不**授权能力、**不**是招聘前提。"Department=能力之家/职能矩阵归属"仅为 CANDIDATE。→ **DEPARTMENT–EMPLOYEE RELATIONSHIP — NOT YET FINAL**。原结论 superseded by Round 1 Correction C-01。
>
> **ROUND 2 CORRECTION — 2026-09-14（C-01 更新，CEO 已确认，员工侧关闭）**：Employee Identity 在 Company 层唯一；AI Employee **不要求**唯一 Department / Business 归属，可同时出现在多个 Department / Business / Team 组织节点中，每次出现代表独立 Assignment / Responsibility，不复制 Employee。**Employee Directory 表达"人"；Business / Organization Map 表达"组织关系"。** 员工侧关系就此关闭。**继续推导的只剩：Department 本身承担什么公司级职责**（原装两部门的公司级责任链已有事实；用户侧/新建部门的公司级职责待真实场景推导）——此项保持 OPEN。

**B·3.4 如何进入多个 Business？** 通过任职线（Assignment = 员工 × 岗位 × 范围）。每条线独立成立、独立暂停/终止。

**B·3.5 每条任职线记录什么？**【判断】
范围（哪个 Business/现场）、岗位名（在那里他叫什么）、当前责任（负责什么——P1 的 Current Responsibility）、该范围的使用授权（能用哪些账号/工具/资料——区别于 3.1 的"能力清单"）、状态、开始时间。
【事实】现行 Assignment 最小语义 = Employee × Role × Scope，一致；【分析】本轮补充的一点：**"能力清单"是人级的，"在范围内被允许用什么"是线级的**——两个概念必须分开（详见 PART C·4.1）。

> **ROUND 1 CORRECTION — 2026-09-14（C-02）**：上句把"该范围的使用授权"写进任职线字段，混淆了组织任职与资源授权（授权变更频率高于任职：新增账号→新授权，不改任职）。修正：**Assignment（任职：范围×岗位×当前责任）与 Grant（授权：主体×范围×对象×动作）是两条独立记录**；链路为 Employee → Assignment → Responsibility（声明所需能力与权限 = 授权需求）→ Grant（独立存在，可先于任职，如公司级工具授权）；责任缺授权 = 诚实的"执行准备缺口"，不是字段缺失。原结论 superseded by Round 1 Correction C-02。

**B·3.6 不同 Business 的 Conversation 怎么隔离？**【判断】
三条独立对话线（内容线谈封面、小说线谈立绘、电商线谈主图），每条携带 员工身份 + 岗位 + 范围；互不混历史。另有一条**个人线**（Identity Conversation：谈他的能力、负荷、成长），全局、不属于任何生意。
【事实】现行 Assignment-scoped Conversation 与 Identity Conversation 分离、每条消息按真实 scope 校验授权，一致。
反例：不隔离则做电商主图时 AI 自动引用小说世界观——上下文污染（1.5 号问题复现）。

> **ROUND 1 CORRECTION — 2026-09-14（C-03）**：上句把"个人线 Identity Conversation"写成正式对话类型，证据不足。修正：该**需求**（与员工谈能力/负荷/成长/跨业务表现）成立，但其形态——A 独立 Employee 级持续对话 / B Employee Detail 问答 + scoped 对话 / C 两者——**NOT FINAL，标记 CANDIDATE**；已证主体仍是 scoped conversations。现行产品资料提及 Identity Conversation 的事实保留，但本推导不再把它当作已证结论。原结论 superseded by Round 1 Correction C-03。

**B·3.7 Conversation Quick Access 应显示什么字段？**【判断】
从业务关系推导：一条快捷项必须让 CEO 三眼答出"**谁？为哪门生意？谈什么/到哪了？**"——所以字段至少为：①员工（头像+名）②**所属业务**（跨业务员工场景下不可省）③责任/话题（当前责任或话题名）④诚实状态（有新消息 / 等你决定 / 结果就绪）⑤时间。
【事实】当前实现只有"标题+员工名+日期"——缺②③④，跨业务员工一多就不可用。已登记 GAP G-01。

> **ROUND 1 CORRECTION — 2026-09-14（C-04）**：六字段平铺有信息过载风险。修正为**三层信息模型**（只定优先级，不画 UI）：**Primary 直接显示** = 员工（头像+名）+ 所属业务 + 注意状态（需要我/结果就绪/新消息/进行中）；**Secondary 弱化显示** = 最新 Topic/Work（这条关系最近在谈的事）；**Hover/展开按需** = 当前责任线、状态原因、时间、dismiss 动作。主要第二层判定：**Topic/Work 优先于 Responsibility**（快捷区首要任务是"恢复刚才在谈的事"；责任线是稳定背景，放 Hover 层）。原字段清单 superseded by Round 1 Correction C-04；G-01 → REFINED。

**B·3.8 Employee Detail 如何表达跨业务任职？**【判断】
结构：身份区（稳定：是谁/履历）→ **任职列表**（每条：业务 / 岗位 / 当前责任 / 状态 / 进入该线对话或现场）→ 能力区（会什么、被授权用什么）→ 最近结果（按业务分组）。
【事实】现行 Detail 六字段中"当前 Responsibility"是单数；跨业务场景必须是**列表**。已登记 GAP G-02。【事实】"Utility 只放 Detail、不放对话"铁律不变——任职列表里"进入对话"是跳转到 Main 的工位，不是把对话塞进 Utility。

> **ROUND 1 CORRECTION — 2026-09-14（C-05）**：四段平铺有把 Detail 变成"员工后台大页"的风险。修正首层范围：**首层 = 身份 + 任职列表（各线：业务/岗位/当前责任/状态）+ 能力摘要**；**折叠/次层 = 履历与历史、完整能力清单、完整结果历史、配置**；**从任职线进入 = 该线的对话、工作、结果**（不复制进 Detail）。Detail 只回答"这个员工是谁、现在在哪些地方负责什么、能力如何"，保持 Conversation-first（Detail 永不承载对话）。原结构 superseded by Round 1 Correction C-05；G-02 → REFINED。

**B·3.9 Search 搜到这个 Employee 显示什么？**【判断】"一人多线"摘要：身份 + 各任职行（业务名+岗位+状态）；点击进 Detail 或直达某条线。不能只显示一个全局头像加名字。

**B·3.10 Notification 如何避免"不知道是哪门业务"？**【判断】通知必须携带三段身份：**业务 + 责任 + 员工**。文案模式："【电商 · 商品视觉】林墨：3 张主图已完成，待你验收"。【事实】当前实现通知并入 Assistant、条目不可点、无业务字段——GAP G-03。

**B·3.11 Result 如何继承 Business + Responsibility + Work Context？**【判断】结果天生携带五元组：所属业务/现场 + 来源 Work + 责任线 + 产出者 + 状态（查看≠验收）。【事实】Result 挂 Work、Viewed≠Accepted 已是现行规则；跨业务场景只要求"业务"字段在所有结果列表/详情中**显性投影**——GAP G-11（表达层）。

**B·3.12 Knowledge / Memory / File Context 怎么隔离？**【判断】
- **业务资料**（品牌规范、世界观、商品素材）：按范围隔离——干电商的活默认只见 电商资料 + 公司共享资料，不见小说资料。
- **员工个人经验**：跟随人，跨业务可用；但注入任何一次工作时只取相关部分，绝不把 A 生意的商业数据带进 B。
【事实】现行 Context Isolation 两层（Employee Persistent Context vs Responsibility Execution Context）+ task-scoped Context Package 正是这个结构——验证成立。

> **ROUND 1 CORRECTION — 2026-09-14（C-18）**：G-12 不能停在表达层，补 **MEMORY PORTABILITY MODEL — DRAFT**。四类记忆：①**Employee Personal Experience**（排版习惯/工具熟练度）——跟人走，**默认可跨业务**，但显式注入且**禁带任何业务数据**；②**Business Knowledge**（品牌规范等）——业务私有，禁止跨业务自动注入（公司共享库除外）；③**Client/Account Sensitive Context**（某账号数据/私信）——最严：仅在该对象当前 Operating Binding 上下文内，禁止跨业务/跨账号，不得进入个人经验；④**Responsibility-specific Memory**（这条任职线上学到的策略）——默认不跨；当被判断有共性价值时，经脱敏提炼**升级**为公司知识/方法——需 Leader 提出 + CEO 确认（这就是公司级学习的入口，第二轮展开）。Open Questions：①"不含业务数据"的自动判定标准；②升级提炼由谁执行（空间工程/分析师）。原表达层结论 superseded by Round 1 Correction C-18；G-12 → REFINED。

**反例压力测试（M）**：把林墨换成"运营员工"（内容：排期；电商：上架；小说：连载发布）——3.1–3.12 全部成立，仅专业对象不同。**跨业务验证通过。**

**N. EMPLOYEE CROSS-BUSINESS MODEL（一句话收口）**【判断】
> **员工是公司的稳定身份（人 + 能力清单 + 个人经验）；他在每门生意里有一条独立任职线（岗位 + 当前责任 + 上下文 + 对话 + 工作 + 结果）；他对资源的可用性由独立的 Grant 决定（Round 1 Correction C-02）；任何显示员工的地方都必须同时显示"哪条线"（显示层级按 C-04 三层信息模型）。**
与现行 Authority 的关系：模型本体与 Company OS §1.2/§5.1/P1 一致（验证）；**新增的是三处表达层要求**：快捷区字段（3.7）、Detail 任职列表（3.8）、通知三段身份（3.10）——全部登记 GAP，不改 Authority。

---

# PART C — Employee 如何真正获得能力 / External Agent 完整推导

**C.0 案例**：RD 业务的开发员工，当前责任 = 完成 Curis 登录模块开发。
**观察**：现实中他要：读懂需求（推理）→ 写代码 → 管仓库（分支/提交/PR）→ 跑命令 → 查文档/网页 → 跑测试 → GitHub 协作 → 对设计稿（Figma）→ 部署验证。
**问题**：这些"需要的东西"不是同一种东西——把"会写代码"和"能连 GitHub"和"是 Codex"混为一谈，就会做出"给员工装插件"式的错误模型。
**推导**：把能力世界切成五类，再回答"每类从哪来、归谁管"。

**C·4.1 这五类是什么（对应 CEO 问题 4.1–4.6）**【判断】
① **Model**：提供"头脑"（推理/写作/编码的智能）——是**能力提供者**，不是能力本身。员工的能力是"能写代码"；OpenAI/DeepSeek 是这个能力的不同供应商。模型可换，员工不变。【事实】现行"身份与执行分离"一致。
② **Skill**：方法包——把"会"变成"做得好、做得一致"（如"这个项目的测试怎么跑""平台文案规范"）。装在人身上或岗位包里。
③ **Tool**：直接的动作工具——员工的手脚（终端、文件、浏览器操作、图像生成调用）。
④ **Connector / Connection**：到外部系统的授权通道+数据通道（GitHub、Figma、店铺平台）。持有授权、状态、权限范围。
⑤ **External Agent**（Codex / Zcode / Claude Code / Browser Agent）：**一个完整的外部执行者**——内部自带模型+工具+方法，能独立完成一段被委托的工作。它不是"一件工具"，是"可被委托的执行者"。

> **ROUND 1 CORRECTION — 2026-09-14（C-06）**："External Agent = Capability Provider"只是第一步，与 Model Provider 压成同层会丢失关键差异。修正为五层：**Capability**（员工能做什么）/ **Provider**（谁提供能力：**Model Provider** 或 **Agent Runtime Provider**）/ **Agent Runtime**（是否有自主执行生命周期——Agent Runtime Provider 的属性）/ **Execution Environment**（在哪里执行——属性）/ **Tool Access**（能调用什么——属性）。由此：**Codex / Zcode / Claude Code = Agent Runtime Provider**（自带大脑+工具+环境+生命周期）；**GPT API 类 = Model Provider**（只供大脑，工具与环境由 Curis 编排）。Curis 不重建两者，经 Adapter 消费真实项。原单层结论 superseded by Round 1 Correction C-06；G-04 按此细化。
**MCP 的角色**【判断】：MCP 是 Tool/Connector 的**接入协议**——回答"怎么把外部工具接到员工手上"，不回答"这是什么能力"。属于内部实现语言，用户不需要懂。【事实】与现行"Provider 细节不进用户语言"一致。
**Computer Access 的角色**【判断】：一种高权限 Tool 通道（直接操作这台电脑）。必须有显式授权档位。【事实】ADR-0046 三档（请求批准/自动处理/完全访问）。
**外部 Agent 与 Model 的关系**【判断】：同为 **Capability Provider（执行提供者）**的两个类型——Model-backed 与 Agent-backed。【事实】Shell Contract §3.5 已固定"执行选择必须显性区分 Model/Agent、Agent ≠ Model"——本轮从真实需求反推验证。

**C·5 多 Agent 协作推导（对应 CEO 问题 5.1–5.10）**
**5.1 Employee Identity 是否保持不变？** 是。员工身份稳定；执行提供者可换。【事实】P1 三层责任（Object Owner / Current Responsibility / Current Executor）+ 身份与执行分离。
**5.2 Executor / Provider 是否可以变化？** 是。同一个员工这一步用模型 A、下一步委托 Codex；换 Provider 不换责任主体。
**5.3 一个 Work 允许多 Provider 协作吗？**【判断】允许，但协作发生在 Work 的**不同步骤/不同责任**之间（开发用 Codex → 审核用 Claude Code → 视觉验证用 Browser Agent），每一步的执行者都被记录；不是模糊的"一群 Agent 混跑"。反例：若允许多 Provider 无记录地共写一个步骤，出了问题无法回答"这句代码是谁写的"。

> **ROUND 1 CORRECTION — 2026-09-14（C-07）**："只在不同步骤间协作"过窄，排除了真实形态。修正：支持 **Sequential / Parallel / Review / Compare / Candidate generation / Verification**；结构改为 **Work → Execution（可多个）→ Executor（员工或系统自动化）+ Provider + Contribution（对结果的具体贡献部分）+ Status**；Result 由可归因的贡献组成（含"对比后选用哪个候选"的选用记录）。核心原则不是"必须串行"，而是**每一份执行贡献都可追踪、可追责**。原串行限定 superseded by Round 1 Correction C-07。
**5.4 Provider 使用记录属于什么？** 两个账：**用量账**（Usage Ledger：按 员工×工作×Provider 记）+ **执行记录**（Work 的执行详情：谁/用什么/何时执行了这一步）。【事实】现行唯一 Usage Ledger 已有；Work 执行详情已有 Evidence 承载。
**5.5 Result 属于 Employee 还是 Provider？**【判断】**Result 属于员工**（责任主体对结果负责）；Provider 是工具。→ 责任永远可追问到"人"，不会漂移到"某个模型"。

> **ROUND 1 CORRECTION — 2026-09-14（C-08）**：原结论"Result 属于员工"有问题——自动化 Work（无员工，如系统定时取数）无法表达，除非伪造员工；多员工协作时归属含糊。修正：**Result ∈ Work ∈ Business（业务真相层）；Employee 是 Responsible Producer（责任产出者，可为"系统自动化"——用 System Activity 表达，不造假员工）；Executor/Provider 是实际执行者（经执行记录归因）**。四场景压测：单员工单 Provider ✓；单员工多 Provider（一人责任、多段贡献归因）✓；多员工协作 ✓；自动化 Work（生产者=系统）✓。原结论 superseded by Round 1 Correction C-08。
**5.6 Evidence 如何记录实际哪个 Agent 执行？** 执行详情含：Provider/模型、调用时间、关键参数摘要、成本、产物哈希。【事实】Evidence 承载执行详情已是现行规则，此处只是明确"Provider 身份"是必录字段——GAP G-04（外部 Agent 类 Provider 的登记与健康尚不完整）。

> **ROUND 1 CORRECTION — 2026-09-14（C-09）**：原句把 Provider/参数/成本/哈希都放进 Evidence，会让 Evidence 变成 Runtime Debug Panel。修正为**两层但关联**：**Evidence（用户层）** = 证明业务结果真实可信——发布回执、测试通过、外部链接、平台数据、审核记录；**Execution Audit / Technical Trace（技术审计层）** = Provider/Model/Tool、成本、哈希、时间、执行环境——默认折叠（对应 Blueprint L4），供排错/审计/成本核算。两层经 Result↔Execution 关联互通；Audit 数据同时喂养用量账。原混层结论 superseded by Round 1 Correction C-09。
**5.7 在哪里添加 Codex / Zcode？**【判断】发现 → Talent & Capability（"公司能获得什么新能力"）；接入/授权/健康 → Settings / Connections（"技术上怎么连"）。四段归属见 C·3。
**5.8 在哪里授权某 Employee 使用它？**【判断】员工能力区（Employee Detail / 工位能力行）：该员工被允许使用哪些 Provider/连接。规则 A.4："谁被允许用它" → Permission/Assignment。
**5.9 在哪里看它当前是否可用？**【判断】三处一致性显示：Settings 的 Provider 健康（源）；员工能力行（这个人现在能不能干活）；Work 运行前检查（这项工作所需的资源是否就绪——现行"运行准备卡"雏形）。
**5.10 Usage / Cost 如何记录？** 按 员工 × Work × Provider 记账 → 汇总到业务成本 → 公司总账。【事实】现行 Usage Ledger + 经营洞察的"有真实来源才显示成本"一致。

**C·2 用户现实约束推导**【判断】
用户的状态可能是：有 OpenAI Key / 没 Key 但订阅了 Codex / 有 Zcode / 有 Claude Code。→ 用户心智不是"配置模型"，而是"**我有哪些可用的执行资源，谁在用，能不能用，花了多少**"。由此产品需要（每个都由真实行为逼出）：
- **Provider Registry**（登记公司可用的执行资源：模型供应商、外部 Agent、连接服务）——否则无法回答"我有什么"。
- **Capability Binding**（员工 ↔ 资源的允许关系）——否则无法回答"谁能用"。
- **Availability / Health**（现在能不能用、为什么不能）——否则"已配置但用不了"的黑箱。
- **Usage**（按人按活记账）——否则多业务时算不清谁烧的钱（1.15）。
- **Multi-agent execution history**（一个 Work 内多段执行记录）——否则无法审计与复盘（5.3 反例）。
【事实】模型 Provider 的 Registry/Binding/Health/Usage 已实现；**外部 Agent 作为 Provider 类型的完整登记/健康/授权是缺口**——GAP G-04；公司级"能力供给总览"视图缺失——GAP G-05。

**C·3 放置（用 A.4 规则）**【判断】
"我有哪些执行资源、连没连上、健康如何" → Settings / Connections（技术上怎么连）。
"这类能力怎么获得新的" → Talent & Capability（发现/招募/安装）。
"这名员工被允许用哪些" → Employee 能力授权。
"干活时用哪一个" → 工位 Composer 的执行选择槽（现行语义槽位已预留）。
"这次到底谁干的、花了多少" → Work 执行记录 + Usage。
**J 为什么不放别处**：若把"Codex 接入"放进 Talent 当"技能安装"，用户会以为装完即用，但它是需要订阅/授权/健康的连接关系——"已安装却用不了"的困惑由此而来。获得 ≠ 连接 ≠ 授权 ≠ 使用，四段各有归属。

> **ROUND 1 CORRECTION — 2026-09-14（C-10）**：上述原则升级为正式模型 **CAPABILITY LIFECYCLE**：`Discover → Acquire/Install → Connect → Authorize → Bind → Use → Observe/Cost → Disable/Remove`。四类能力验证：Model（发现→取得 Key→连接测试→授权→绑定员工/默认→使用→用量→吊销）✓；Skill（发现→安装→[连接 N/A]→授权→绑岗位包→使用→效果观察→停用）✓；External Agent（发现→订阅→连接→授权→绑定执行选择→使用→用量→解绑）✓；Connector（发现→[取得 N/A]→OAuth 连接→授权范围→绑定业务/对象→使用→同步/用量→撤销）✓。每步有自己的入口与诚实状态；放置按 A.4 规则。原一句话原则 superseded by Round 1 Correction C-10。

**M 跨业务验证**：电商运营员工 = 文案模型（Provider）+ 店铺连接（Connection）+ 上架动作授权（Grant）——同一套 Registry/Binding/Health/Usage 结构成立。小说：写作模型 + 连载平台连接。成立。

**N 收口**【判断】
> **员工的能力 = 会什么（稳定清单）；能力的供给 = 模型或外部 Agent（可插拔 Provider）；Provider 的获得在 Talent、接入在 Settings、授权在员工、使用在 Work、消耗在总账。**

---

# PART D — Content Growth 完整经营链（重点 Publishing）

> 链条：信息收集 → 竞品账号研究 → 选题与内容生产 → 审核 → **发布（P0）** → 数据回流 → 分析复盘 → 下一轮。每步用 A–N 格式；对象属业务专业模型，行为骨架属公司语法（见 A.3）。

**D.1 信息收集**

- **A 目标**：知道"现在什么值得做"。
- **B 行为**：持续看行业资讯、平台热点、竞品更新、自己账号的评论与反馈。
- **C 对象**：信息源（Source）、采集到的信号、值得做的机会（Opportunity 候选）。
- **D 能力**：研究员工的"监测与摘要"能力（可自动巡检、可人工投喂）。
- **E 依赖**：Search / Browser（公开信息）、平台数据 Connector（有 API 时）、Knowledge（沉淀）、无 API 时 Browser Agent 或人工导入。
- **F 权限/上下文**：源配置与信号属于**该业务**；不同业务的雷达互不混。连接能力在 Settings。
- **G 增加**：信号对象（来源+内容+时间+可信度）与机会对象（为什么值得+时效+建议动作）。
- **H 放哪**：业务专业对象，放在该业务现场；"持续收集"作为一种 Work 模式（公司语法层）。
- **I 为什么**：换电商=选品情报、换投资研究=行业动态——"源→信号→机会"结构相同，对象不同；故行为共性、对象分业。
- **J 不放别处**：不当 Knowledge 资料存——知识库是沉淀物，雷达是活水；值得留的信号才沉淀为资料。
- **K/L 用户看到/能做**：今天的信号与机会列表（带来源与时效）；一键把某条转为选题。
- **M 反例**：小说业务 → 收同类作品榜单/读者评论趋势，结构同构。成立。
- **N 结论**【判断】：信号/机会是业务专业对象；"持续收集"是共性 Work 模式。【分析】Content Growth Authority 已有 Content Opportunity/Intent；共性化（其他业务是否需要同构对象）→ 推导不足（电商/小说案例里信号更弱），暂不下结论，登记观察 G-10。

**D.2 竞品账号研究**

- **A 目标**：知道"别人怎么做、做到什么水平"。
- **B 行为**：选定竞品账号 → 看定位/内容历史/更新节奏/表现数据 → 形成对标分析。
- **C 对象**：**竞品账号**（平台+账号+定位+内容历史+指标）与**对标分析**（结论+依据）。
- **D 能力**：研究能力 + 公开数据读取（Browser/Connector）。
- **E 依赖**：浏览器或平台公开数据；无 API 时人工导入并标注来源/新鲜度。
- **F 权限/上下文**：竞品档案属于本业务；读公开数据不需要账号授权（区分于自己的账号）。
- **G 增加**：竞品账号作为**持续观察对象**（有身份、会更新、有指标）。
- **H 放哪**：业务现场（经营对象）；分析结论可沉淀为 Knowledge。
- **I 为什么**：它被选题和策略反复引用，是活对象不是一次性笔记。
- **J 不放别处**：不混入普通 Knowledge——知识条目是静态资料，竞品账号是持续跟踪的经营参照。【判断】这是"Account 概念的两种用法"的边界：自己的账号=经营对象（可发布），竞品账号=观察对象（只读）。
- **K/L**：竞品列表+各家近况+"和我们对比"的分析；可引用进选题依据。
- **M 反例**：电商→竞品店铺（价格带/上新节奏/爆款）；小说→同品类作品（更新节奏/榜单）。同构成立。
- **N 结论**【判断】：竞品账号是业务专业对象；其分析结论按普通资料沉淀。

> **ROUND 1 CORRECTION — 2026-09-14（C-11）**：本步把"竞品账号"与"自己的账号"都用了 Account 语言，污染后续模型。修正为两类对象：**Owned / Operated External Object**（我们实际经营、可执行动作——自己的内容账号/Store/Repo；可有 Connection、Action Grant、对外动作记录、一方数据）与 **Observed External Entity**（只观察、不拥有、不执行——竞品账号/竞品店铺/竞品产品；只有平台画像+公开快照数据，必须带来源与新鲜度；**绝不能有** Connection、Permission/Grant、对外动作记录）。两者共享的只有：平台、公开画像、公开指标（出处不同）。原混用 superseded by Round 1 Correction C-11。

**D.3 选题与内容生产**

- **A 目标**：把机会变成可发布的内容成品。
- **B 行为**：定选题 → 写 Brief（要求）→ 产出文案/脚本 → 出视觉素材 → 按账号适配 → 审核。
- **C 对象链**：**Topic → Brief → Copy / Script → Asset → Variant（按账号适配版）→ Review 结论**。
- **D 能力**：策划、写作、视觉（林墨跨业务案例在此汇合）、审核。
- **E 依赖**：写作/图像模型（Provider）、设计 Skill、图像工具、品牌规范资料（业务 Knowledge）。
- **F 权限/上下文**：Variant 与目标账号绑定（为哪个账号适配什么）；审核是强制前置（发布的前一道门）。
- **G 增加**：上述专业对象；交接沿 Work/Handoff（完成→默认下一棒；审核为强制 Review 点）。
- **H 放哪**：全部业务专业模型（现场内）；Work/Handoff/审核骨架是公司语法。
- **I 为什么**：对象是内容行业特有的；骨架（分工→交接→审核→结果）与研发、电商同构。
- **J 不放别处**：Variant 不是"另一个文件"而是"与账号绑定的适配产物"——不放进通用文件管理。
- **K/L**：一条内容的进度视图（选题→成品→审核）；每步的产出可点开看；审核可批/驳/改。
- **M 反例**：小说=大纲→章节→编辑→定稿；电商=选品→商品页→上架审核。同构成立。
- **N 结论**【判断】：内容对象链是业务专业模型；"分工→交接→审核→结果"是 Company OS CORE。

**D.4 发布（P0，完整展开 10.1–10.16）**

- **A 目标**：把成品内容真正发到指定平台账号，拿到回执，收回数据。
- **B 行为**：选平台 → 选账号 → 按平台规则适配 → 审核/必要时老板拍板 → 立即或定时发 → 拿"发成功了"的凭证 → 回收数据。
- **C 对象**：**Platform、Account、Connection、Publication（发布记录）、Receipt（回执）、Metrics（回流数据）**——六件套。
- **D 能力**：发布执行能力（谁被授权发布）。
- **E 依赖**：平台 Connector（OAuth/API Key/MCP）、浏览器自动化（无 API 时，需授权档位）、人工代发（最终兜底）。
- **F 权限/上下文**：发布是对外承诺动作（高风险类）；发布权必须显式授予。
- **G 增加**：六件套对象 + 发布权授权 + 降级通道。
- **H 放哪**：Publication/数据 = 业务专业对象；Connection = Settings；发布权 = 员工授权；高风险确认 = CEO Gate。
- **I/J 为什么**：发布记录离开现场就无法回答"谁发的、发的什么、结果如何"，所以必须在业务内；连接细节放现场会让经营页塞满凭证管理——所以 Connection 在 Settings。
- **K/L 用户看到/能做**：发布队列/日历（什么将何时发到哪）；每条状态（待发/已发/失败+原因）；回执（链接/编号/时间）；后续数据。能做：排期/立即发/改期/撤回未发的/失败重发。
- **M 反例**：小说"发布"=章节上连载平台——同样六件套。电商"上架"=商品发布到店铺——同构。成立。
- **N 结论**【判断】：**发布链 = Platform + Account + Connection + Publication + Receipt + Metrics；发布是对外承诺动作，必须有审核前置、显式授权、诚实回执、真实数据回流。**

**逐问 10.1–10.16**【判断，逐条】：
- **10.1 发布到什么 Platform？** 平台=频道（Channel），发布目标第一层。【事实：Channel 概念已在 Content Growth Authority】
- **10.2 发布到哪个 Account？** 账号（Channel Account），第二层——真正接收回执与数据的对象。
- **10.3 一个 Platform 几个 Account？** 任意多个（矩阵经营正是多账号）。
- **10.4 Account 属于哪个 Business？** 账号挂在业务下（经营对象）。【张力标注】现行 Authority 说"Channel/Account 是 Company 资产经 Binding 服务 Workspace"；【判断】用户心智默认"账号属于我这门生意"，少数官方号公司共享。登记 GAP G-07，待你裁决，不改 Authority。
- **10.5 一个 Account 能否服务多个 Business？**【判断】默认不（定位/受众/策略会被污染）。若确需共用（公司官方号）→ 挂 Company 层、各业务经授权使用——即"账号归属 = Business 私有（默认）或 Company 共享"两档。

> **ROUND 1 CORRECTION — 2026-09-14（C-13，P0）**：原"默认 Business 私有、少数 Company 共享"不够稳。重新比较两模型：**Model A**（Business owns External Object）vs **Model B**（Company owns 对象身份 + Business 获得 Operating Binding），按七维比较：简单性（A 略优，B 可用表述弥补）/ 多业务共享（B 胜：官方账号、Repo 天然多业务经营）/ 权限（B 胜：授权挂在对象，不随业务搬家）/ 历史（B 胜：对象历史连续）/ 转移与业务关闭（B 胜：撤 binding 即可，对象不失家）/ 审计（B 胜）。判定：**采用 Model B——External Object 的身份/所有权登记在公司层；Business 通过 Operating Binding 获得经营权；通常一个对象只有一条活跃 binding；用户看到的"这门生意的账号"= 当前 binding 的表述投影。**此结论与现行 Authority（"Channel/Account 是 Company 资产经 Binding 服务 Workspace"）**一致——推导收敛到权威，无需改 Authority**。G-07 → RESOLVED（Round 1 Correction C-13）。原"默认私有"结论 superseded。
- **10.6 Platform 规则存哪里？** 平台规则（尺寸/字数/标签/时间/审核规则）属于 **Platform 层**——同平台所有账号共享；来源=Curis 频道能力档案 + 用户经验补充。【事实：现行"具体平台规则下放 Capability Registry/Channel Facts"一致】

  > **ROUND 1 CORRECTION — 2026-09-14（C-14）**：补齐事实质量要求：**Platform Rule 必须携带 Source（官方文档/用户经验/连接探测）、Updated At、Verification state（已验证/声称/已过期）、适用范围（地区/账号类型，若适用）**——否则专业现场会按过期规则工作。判定：**"事实必须带来源与新鲜度"是 COMPANY OS 通用 Truth 原则**；**规则库本身属 Platform Capability Facts / Channel Registry（INFRA 层）**，不是 Core 对象。
- **10.7 发布需要什么 Connection？** 每个账号一条连接；无连接=诚实显示"待连接"，不伪造发布。
- **10.8 授权类型？** OAuth / API Key / MCP / Connector / 浏览器自动化 / 人工——全部合法，但必须如实标注"当前是哪种、是否有效"。【事实：与"不伪造已连接"原则一致】

  > **ROUND 1 CORRECTION — 2026-09-14（C-15）**：原列表把 MCP（集成协议）与 OAuth（授权方式）混在一层。修正为两层：**认证/授权方式** = OAuth、API Key、本地会话、人工确认；**集成/工具协议** = MCP、REST API、本地工具桥、连接器。一条连接 = 一种授权方式 + 一种或多种协议；无论哪种组合都必须如实标注"当前是哪种、是否有效"。原混层列表 superseded by Round 1 Correction C-15。【事实：与"不伪造已连接"一致】
- **10.9 谁有权发布？**【判断】发布权 = 员工 × 账号 × 动作 的显式授权记录；默认仅负责人/指定发布者。GAP G-09（现行权限模型无"对外部对象的动作授权"粒度）。

  > **ROUND 1 CORRECTION — 2026-09-14（C-16）**：三元组深化为 **ACTION GRANT MINIMUM SEMANTICS**（只定义语义，不设计 UI）：`Grant = { Subject(员工/角色), Object(外部对象/工具/Provider), Action, Scope(生效范围), Effect(allow), Constraints(风险级/政策检查), Expiry(期限/自动授权到期), Approval requirement(生效前是否需审批), Source(谁授的：CEO/负责人/策略默认/继承), Status(active/revoked/expired) }`。示例：林墨×小红书官方账号×publish×内容业务范围×日常自动（政策）×到期随任职×CEO 授予；开发员工×Repo×merge×研发范围×高风险需审批。G-09 → REFINED。原三元组 superseded by Round 1 Correction C-16。
- **10.10 发布前是否需要 Review？** 是——内容审核通过是发布前置（强制 Review 点）。

  > **ROUND 1 CORRECTION — 2026-09-14（C-12）**：原"发布前强制 Review + 发布一律高风险"过重，会把 CEO 变回审批机器人（违背 P4 自动化与"日均动作<3"）。修正为 **ACTION RISK & REVIEW MODEL**：是否需要 Review/审批由 **业务政策 × 动作类型 × 账号状态 × 员工授权级 × 规模（批量升级）× CEO 偏好** 共同决定；三档：**自动执行（事后留痕）/ 执行前 Review（由内容审核责任者把关，不是 CEO）/ CEO Decision（不可逆、大额、首次新渠道、敏感、批量超阈值）**；新账号/新平台的首次动作默认升一档。业务政策示例："本账号日常内容自动发布；商业化内容需我确认。"原一刀切结论 superseded by Round 1 Correction C-12（10.11 的 CEO 高风险清单保持不变，只是不再"一律"）。
- **10.11 哪些情况需要 CEO Decision？** 首次在新账号发布、敏感话题、商业化内容、平台规则风险、批量群发——即"高影响/不可逆对外承诺"。【事实：与 P7 边界一致】
- **10.12 定时发布怎么表达？** 发布计划是业务现场的对象（内容日历）；到点由系统执行；CEO 看"什么将何时发到哪"。
- **10.13 成功后怎么得到 Receipt？** Connector 返回（链接/平台编号/时间/状态）或人工贴入并标注来源；Receipt 是 Publication 的证据（进 Evidence 层）。
- **10.14 失败怎么办？** 如实显示原因（审核驳回/接口失败/规则不符）→ 修复重发；已发生的动作不回滚（已发就是已发），可撤回的只是"未执行的计划"。【事实：现行 Distribution Policy"已发生不回滚 / 未执行看策略"分离一致】
- **10.15 平台无 API 怎么处理？** 诚实降级两档：浏览器自动化（需授权档位，ADR-0046 三档）或人工代发（员工备齐一切，人贴发）；回执人工录入并标注来源。GAP G-08（降级通道与动作流的统一表达未定义）。
- **10.16 数据如何回流？** 定时拉取或人工回填：曝光/互动/涨粉/转化挂在 Publication → 汇成账号/内容维度分析（进经营洞察）。【事实：Publication 逐账号真相、"平台通用建议 vs 本账号数据学到的建议"边界已有】

**D.5 数据回流与复盘（链尾）**
- **A–N（紧凑）**：目标=知道这轮做得怎么样、下轮怎么改；行为=按周期拉数据→对比→归因（什么标题/时间/账号有效）→复盘结论；对象=周期复盘记录+结论（Learning 候选）；依赖=平台数据 Connector/人工回填；权限=数据属业务，公司层只见汇总；G 增加=复盘作为 Work 的固定收尾；H=业务内复盘，结论沉淀见第 22 条（第二轮）；K/L=复盘页（事实/分析/未知/建议）+"下一轮怎么调"；M=电商（销售复盘）/小说（读者复盘）同构；N=**每轮以复盘收尾，结论可指向下轮策略调整——经营才会连续（1.8/1.9）。**

---

# PART E — Platform / Account / Connection / Permission 模型

**E·11 三者关系推导（问题 11）**【判断】
- **Platform（平台/频道）**：发布与数据的"舞台"及其规则。持有：平台规则、支持的内容形态、能力状态（有无 API、支持什么）。是行业事实层，不是用户经营的对象。
- **Account（账号）**：用户在平台上的**经营身份**。持有：定位、受众、策略、负责人、发布历史、数据。是经营对象。
- **Connection（连接）**：Curis 与该账号之间的**技术通道**。持有：授权方式、凭证状态、权限范围、同步状态。是基础设施。
> 一句话：**平台是舞台，账号是演员身份，连接是后台的电线。** 一个 Platform 多个 Account；一个 Account 一条（或备份）Connection；**连接失效不删账号**——历史与身份保留、执行降级。【事实：OAUTH_FAILURE_KEEPS_ACCOUNT 一致】

**E·12 ONE TRUTH — MULTIPLE CONTEXTUAL PROJECTIONS（问题 12）**【判断】
同一个账号真相，三个上下文三种投影（不是三份数据）：
- 业务现场（决定**怎么经营**它）→ 定位/受众/策略/发布历史/数据；
- Settings（决定**怎么连接**它）→ 授权方式/凭证状态/权限范围/最近同步；
- 员工授权（决定**谁能用**它）→ 账号名 + 谁有什么动作权（发布/读数）。
【事实】"Surface 只投影共享 Truth"（SURFACE_PROJECTS_SHARED_TRUTH）是该原则的现行表达，一致。

**E·13 复用到 RD（问题 13）**【判断】GitHub：Repository=业务现场的工作/经营对象（代码/PR/版本）；GitHub Connection=Settings 基础设施；动作授权=开发员工读写、审核员工只读、发布员工可 merge/deploy。→ 与账号模型同构（Repo≈Account，GitHub≈Platform，Connection≈Connection，动作授权≈发布权）。
**E·14 复用到电商（问题 14）**【判断】Shopify：Store/Product/Order=经营对象；Shopify Connection=Settings；运营员工可改商品、财务员工只读订单。→ 同构成立。
**跨三个业务验证通过** → 抽象正确，可进 COMPANY OS CORE。

**E·15 通用模型收口**【判断】
> **External Object（业务经营的外部对象：账号/仓库/店铺）+ Connection（技术通道，Settings）+ Action Grant（谁可对它做什么）** 三件套是 COMPANY OS CORE；Platform（GitHub/Shopify/小红书）是 External Object 的"类型/舞台"层事实；账号的经营属性（定位/受众/策略/数据）是 BUSINESS PROFESSIONAL MODEL。
放置：External Object 归业务（或公司共享档）；Connection 归 Settings；Grant 归员工/责任授权；使用记录进用量账。

> **ROUND 1 CORRECTION — 2026-09-14（C-13/C-17）**：两处修正。①放置改为：**External Object 身份登记在公司层（Model B），Business 经 Operating Binding 获得经营权**；Connection 仍归 Settings；Grant 归员工/责任授权。②三件套之外补第四段：**对外动作共性骨架** `Intent → Action → External Target → Execution → Receipt → State → Metrics`（四案例——内容发布/电商上架/软件 Deploy/小说章节发布——全部成立；专业对象 Publication/Listing/Deployment/Chapter Release 保留为各业务实例；通用命名 External Action vs External Operation 待 CEO 选定，G-06 → REFINED）。原"归业务"表述 superseded。
>
> **ROUND 2 CORRECTION — 2026-09-14（对 C-17/C-13 的窄幅修正，CEO 复核意见）**：
> ①**Metrics/Feedback 移出动作骨架**。重新检查结论：`Intent → Action → External Target → Execution → Receipt → State` 六段才是所有对外动作的通用核心（"动作发生了没有、成功没有、凭证是什么"）；**Metrics / Feedback 不属于动作本身**——它是动作之后的**业务反馈**：专业层对象，**引用**该动作（"这条数据属于哪次发布/哪个 Deploy"），有独立生命周期（可迟到、可人工回填、可能永远不来）。不为统一强绑。例：Deploy 的"表现"（崩溃率/采用率）是产品反馈，不进部署动作记录；Listing 的销量是生意反馈，不进上架记录。
> ②**Operating Binding 四层拆分**（压力测试"通常一条 active binding"后修正）：**Ownership（公司层身份）→ Business Usage Binding（可多条：公司官方账号、共享 Repo 可被多业务同时合法使用）→ Primary Operating Responsibility（通常一条：谁对该对象整体经营与策略负责；可暂时空缺=责任缺口）→ Employee Action Grant（正交：谁可对它做什么）**。"通常只有一条 binding"修正为"通常一条主要经营责任；使用绑定可多条"。共享对象的各业务视图 = 按动作发起方归因过滤的投影（对象自身历史仍是一条时间线）。

---

# PART F — 第一批 Product Gaps（已登记 GAP REGISTER）

本轮推导产生的缺口（详见 CURIS_PRODUCT_DERIVATION_GAP_REGISTER.md）：
> **ROUND 1 CORRECTION 同步说明（2026-09-14）**：以下缺口状态已在 GAP REGISTER 更新——**G-01 REFINED**（三层信息模型）、**G-02 REFINED**（Detail 首层收敛）、**G-04 REFINED**（Agent Runtime Provider 分层）、**G-06 REFINED**（对外动作七段骨架，命名待定）、**G-07 RESOLVED**（C-13 采 Model B，与现行 Authority 一致）、**G-09 REFINED**（Grant 最小语义）、**G-12 REFINED**（Memory Portability Model DRAFT）；G-03/G-05/G-08/G-10/G-11 维持原状（OPEN/DEFERRED）。下表为第一轮原始登记，保留作推导痕迹。
- **G-01** 快捷对话缺"业务+责任+状态"字段（B·3.7）；
- **G-02** Employee Detail 单责任字段 vs 多条任职列表（B·3.8）；
- **G-03** 通知缺"业务+责任+员工"三段身份、条目不可点（B·3.10）；
- **G-04** 外部 Agent 作为 Provider 类型的登记/健康/授权/执行记录不完整（C·5）；
- **G-05** 公司级"能力供给总览"（我有什么、谁在用、能否用、花多少）缺失（C·2）；
- **G-06** "对外动作+回执+数据回流"作为跨业务共性结构未抽象（发布/上架/部署/连载同构）（D·4）；
- **G-07** 账号归属层级（Business 私有 vs Company 共享）与现行 Authority 表述有张力，待 CEO 裁决（10.4/10.5）；
- **G-08** 无 API 平台的诚实降级通道（浏览器自动化/人工代发）与回执人工录入的统一表达未定义（10.15）；
- **G-09** Action Grant（员工×外部对象×动作）授权粒度未定义（10.9/E·15）；
- **G-10** "源→信号→机会"信息雷达的跨业务共性化——推导不足，暂不下结论（D.1）；
- **G-11** Result 的"业务"字段在结果列表/详情中未显性投影（B·3.11）；
- **G-12** 员工个人经验跨业务复用的用户表达——推导不足，暂不下结论（B·3.12）。

**三层分类小结（A.3 规则）**【判断】：
- **COMPANY OS CORE**（本轮验证/新增的共性）：员工身份与任职线；对话按线隔离+个人线；Work/Handoff/强制审核点；Result 五元组；Evidence 含执行者身份；用量账；通知三段身份；检索"一人多线"；**External Object + Connection + Action Grant** 三件套；Provider Registry / Binding / Health / Usage。
- **BUSINESS PROFESSIONAL MODEL**：Channel/Account 经营属性、Publication/Receipt/Metrics、Topic/Brief/Variant、信号与竞品账号、Repository、Store/Product/Order、（未来的）Chapter。
- **INFRASTRUCTURE / PROVIDER**：Model、External Agent（Codex/Zcode/Claude Code/Browser Agent）、Skill、Tool、MCP（接入协议）、Connector、Computer Access、Key/订阅、Availability/Health。

---

## 核对与下一步
1. 本文件为 Draft 推导记录；B/C/D/E 各步可逐条核对（例如"B·3.7 字段不对""10.5 应该只能私有"）。
2. 核对通过后第二轮再做：Business Operating Loop / Lifecycle / Success Definition / Resource Allocation / Context Isolation 汇总 / Business Activation / Evolution / 公司级学习（CEO 指令 35 条）。
3. 未使用 Authority 修改权：G-07 等与现行表述有张力处只登记，等你裁决。

（第一轮完 · STOP FOR CEO REVIEW）
