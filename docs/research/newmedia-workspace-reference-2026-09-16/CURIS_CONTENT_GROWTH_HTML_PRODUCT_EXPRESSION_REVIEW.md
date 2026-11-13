# CURIS CONTENT GROWTH HTML PRODUCT EXPRESSION REVIEW

Status: Review
Authority Class: REVIEW
Disposition: CEO REVIEW REQUIRED — NO CHANGES AUTHORIZED
Date: 2026-09-16
Owner: CEO / Product Review
Next Gate: STOP FOR CEO REVIEW

## Evidence / 审查范围与限制

本轮为**源码与产品合同静态审查，浏览器交互验证未完成**。尝试用Computer Use打开用户指定本地HTML时，浏览器安全策略拒绝file URL，并明确禁止其它浏览器/间接方式绕过。没有切换工具绕过，没有可用当前页面截图，不把源码输出当实际点击观察。下列行为依据处理函数推导，标HTML STATIC；真实可见性、焦点、滚动、点击后渲染与运行时异常仍需实操补验。

审查输入：

- [HTML](../../../CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION/Content%20Growth%20Workspace.html)，3213行，SHA256：`e599de860b5f7be8fd0e018e3af7fd3df17b8d3c30d8b945b167582f29efe101`。源码读取未执行其中脚本。
- [原研究](CURIS_CONTENT_GROWTH_PROFESSIONAL_WORKSPACE_REFERENCE_STUDY.md)，§3、§12、§30及结论：用户指定既有OBSERVED/研究证据，本轮未重新观察竞品。
- [Operational Expression](CURIS_CONTENT_GROWTH_OPERATIONAL_PRODUCT_EXPRESSION_CANDIDATE.md)，尤其选题池、制作工作面及字段合同。
- [最新Product Structure Candidate](CURIS_CONTENT_GROWTH_TEAM_WORKSPACE_PRODUCT_STRUCTURE_CANDIDATE.md)，§4.1、5.2.1、5.3、6–12及Account Scope合同。它是候选，不冒充Current Authority。

原Workbuddy记录只观察到四条方法链说明及产线卡；未实际执行“开工”，产线卡未进入独立编辑器。不能把CEO所述“开工先确认形式”倒写成已由本轮/原轮完整实测。原研究已将跨方法稳定性列为针对性缺口；其它开源样本主要证明Composer/适配等，不证明完整员工节点协作。

## A. Root Cause

**结论：MIXED，以PRODUCT TRANSLATION GAP为主，叠加明确HTML EXECUTION GAP及未关闭的研究问题。上一轮Ready结论对Production与Employee协作细节过于乐观；七区/Portfolio/持续经营骨架仍可保留。**

| 编号 | 发现与影响 | 根因 | 证据 |
|---|---|---|---|
| A1 | Format/方法曾是明确方向，却退化成队列＋通用Tabs | PRODUCT TRANSLATION GAP + HTML EXECUTION GAP | 原研究20、257–267行定义Hybrid/Production Line；Candidate §5.3列制作区域但未规定方法选择与差异化节点；HTML2555–2617统一BENCH_TABS且只按状态/账号过滤 |
| A2 | “向团队委派”与“指定人解释”“当前Work讨论”被合并成入口复用，没有充分保留不同路由语义 | MIXED，产品转译为主 | Candidate §6要求实际Owner、§7同系统入口、§4.1团队交流；未完整规定指定Employee不得隐式改派及Node上下文。HTML1838默认区域m.emp；2605讨论Work不传实际w.owner |
| A3 | Employee入口并非完全不存在，但关键链路断裂 | HTML EXECUTION GAP | openTeam1797起、openEmp1782起均有员工与Work；1792生成conv-open按钮，全文只有此动作声明，无CORE/CG.H处理；1880起dispatcher只识别已注册动作 |
| A4 | 找具体Employee后丢失对象/账号，通用Work讨论丢workId | HTML EXECUTION GAP | modal-act1871只传area；openWork2505只传conv-owner，不携Work。collab-send2467只在经营account scope传accountId，研究提案页虽显示Account但发送未带该上下文 |
| A5 | 声称已路由给新员工，却继续用旧员工身份渲染回复 | HTML EXECUTION GAP | convSend1708起用脚本who生成转交文字，但renderDrawer1652起所有AI消息使用当前t.e；没有逐消息sender身份；不等于真实路由 |
| A6 | 开工不形成已确认的目标/方法/规格组合，还可能进入无关旧Work | MIXED | propPage2436合并“形式/方法”字符串，无规格确认；p-start2484无work时固定W-204，不创建对应提案工作，也不确认方法/目标集 |
| A7 | 输出规格并非完全没有，而是分散、过晚、口径混乱 | PRODUCT TRANSLATION GAP + HTML EXECUTION GAP | W-202数据1054含60秒，editing含9:16；benchAside2620把subtitle.style当“形态”；adapt按账号推比例，不能表示同账号不同格式 |
| A8 | Workflow节点与责任/Owner/输入/版本/结果未成合同 | RESEARCH GAP + PRODUCT TRANSLATION GAP | 原研究只证明方法链；Candidate有多Work/责任但无逐节点接续标准；HTML主要stage字符串、固定Tabs及片段状态，无对应责任节点模型 |
| A9 | 新输入的结果固定落到抖音品牌号，破坏Account-aware研究 | HTML EXECUTION GAP | applyResult1737起topic/combine/data硬编码dy-brand；idea无论当前明确账号都存unassigned |
| A10 | 模拟异步回复可能进入切换后的会话 | HTML EXECUTION GAP（静态风险） | convSend setTimeout读取可变S.conv.msgs并pop，没有绑定发起会话/Work；需实际快速切换复验 |

“一个页面一个员工”不是既有合同结论。HTML已有collabs、团队详情、多Work、无Owner状态，不能笼统指控全部重做。当前问题是**有人员名单但缺乏可追溯协作关系**，而非缺更多头像。

## B. Employee Interaction Review

三种协作Scope成立；Specific Work与Workflow Node应分成两个精度层次，但不是四个新的Conversation系统。

| 层级 | 用户意图/入口 | 必须携带 | 路由及反馈 | 返回 |
|---|---|---|---|---|
| Work Area / Team Intent | 区域输入：“帮品牌号找选题” | Workspace、Area、可选Account/对象、意图 | 按Responsibility与有效Assignment找接收人，显示谁接、为何、需澄清什么；不预设某固定员工永远处理 | 同专业区，显示提案/Work/Result变化 |
| Specific Employee | 员工身份/负责关系：“解释你的判断” | Employee、有效Assignment、当前合法对象/Account，可选Work | 保持指定交流对象；咨询他人或转交执行显式说明，不用关键词偷偷换人 | 原对象/员工入口 |
| Specific Work | Work行/详情：“这条怎么改” | workId、实际Owner、输入/当前Artifact版本、Account、Area | 由实际Work Owner接住；区域Owner可协调但不是默认冒充执行Owner | 原Work及产物 |
| Workflow Node | 当前步骤/产物：“前三秒给三个Hook” | 上述＋明确节点/步骤引用、节点责任/当前承担人、Artifact版本 | 修改限该步骤；若影响下游，说明受影响版本与Review，不重写已发布事实 | 同节点/产物与流程概览 |

节点无独立canonical ID时引用已有执行计划步骤，不能为了对话新建Node Runtime。一个节点可有明确负责人及协作者；多责任拆分按实际依赖，不默认一个节点一个员工或一个工具调用一个Work。已完成节点的原作者和当前处理者可能不同，必须区分。

Team输入不是“只允许一个入口”；统一Work/Result系统也不是抹掉Specific Employee/Work/Node入口。对话头应回答“和谁、讨论什么、为何由此人负责”，路由变化后每条消息保真实sender与当时scope。跨Assignment继续交流仍需权限校验。

**当前HTML已有优点：** collabBar自然语言输入、对象discuss、员工详情、Work Owner/协作者、并行说明、结构化结果卡及返回提示。不应退回能力选择菜单或把所有按钮删除。

**研究区判断：** 现源码research页面主要通过collabBar输入，已无必要要求先选“分析能力”。不能沿用旧截图认定当前仍有全部重复快速输入。Proposal/Reference上的查看、开工、引用、筛选属于明确动作，保留合理；当前关键问题是上下文和结果一致性，不是传统表单数量。统一输入应接受链接/文字等，截图目前只是模拟文件名，不可当真实上传能力。

## C. Production Model Review

| 概念 | 稳定定义 | 例子 | 不应混同 |
|---|---|---|---|
| Content Format | 交付物表现形态 | 文章、图文/图集、视频、音频 | 不是平台、Provider或流程 |
| Production Method | 怎样制作，决定必要输入/责任/步骤/检查 | 图文排版、数字人口播、真人素材剪辑、屏幕演示、分镜生成 | 不是9:16或某模型品牌 |
| Output Specification | 每个目标交付的可验证规格 | 比例、分辨率、时长、页数/字数、字幕/文件要求 | 不是成品之后才临时推导 |
| Production Line | 已可用方法及输出/质量合同的专业分组/视图 | 图文制作、口播制作；方法变体按需展开 | 非canonical对象、独立团队或Runtime |
| Production Workflow | 本次Work根据方法/规格/能力与审阅边界形成的执行步骤及依赖 | Script→合成→剪辑→字幕→QA，其中可并行 | 不是所有Work共用Tabs，也不是用户手画DAG |

**Format/Method优先于Platform作为制作组织维度，成立；“先忽略Account/Platform再制作”不成立。** 账号目标决定内容需要，平台限制在开工前参与规格裁决。原研究本来就是Hybrid，而不是纯Format-first。

“长图文/短图文”可用作用户熟悉的制作分组，但长短通常是规格/编辑策略，不能假定独立Runtime。“口播”描述表达/方法，数字人/真人/旁白是实现方法差异；“短视频/长视频”主要是时长类别且可能覆盖口播，若并列需说明互斥规则或允许筛选，不能让同Work重复算两条线。微短剧可能需要独特分镜/角色连续流程，但没有真实能力验证不宣称已支持。

### 开工合同建议

Account Goal/Strategy → Content Need（既有目标/Brief专业表达） → Research/Proposal → 确定目标交付集合 → Method/Output Spec → Work/Workflow → Artifact → 每账号Variant/Publication → Result → Account Judgment。

每项交付至少明确Target Account、业务目的/成功标准、Format、Method、必要规格、来源及需人工审阅条件。系统根据已有事实预填，用户只确认必要分歧，不强迫填四套表单。已批准Envelope可以允许系统自主形成并推进；“开工确认”不是每轮必须CEO点按钮。

| 规格来源 | 举例 | 裁决 |
|---|---|---|
| 平台/接口硬约束 | 接受格式、上限、账号可用能力 | 不满足不能执行该目标，保留Target和Blocker |
| Account Content Strategy | 风格、节奏、常用时长/图集安排 | 是可解释默认，不把同平台全账号设成一致 |
| 本次内容目标 | 信息量、叙事、篇幅、CTA | 在硬约束内确定必要规格 |
| Method/Capability | 所需素材、输入长度、合成能力 | 不匹配时换合法方法或请求补充，不能静默降质量 |

比例/Resolution/Duration/Pages/字数只显示适用字段：文章不必填分辨率，视频不必填页数。3:4八页、9:16六十秒、2000–2500字是本次交付示例，不是永久平台规则。改变规格若影响在途工作须保版本和下游影响。

### 反证与唯一层级建议

同选题生成三种交付是合理的，但**不强制一个Account一个Work，也不强制所有交付放一个Work**。共享Research/Brief/素材可复用；不同方法、负责人、截止/审批/重试边界需要独立推进时拆关联Work，轻量同方法适配可在同Work保留账号Variant。避免笛卡尔积生产所有账号×所有形式。

推荐**两个必达层级＋一个可选分组视图**：内容制作总览同时提供方法/产线分组与跨线Work列表 → 具体Production Work。产线详情是筛选后的工作列表，可保深链/返回，不强制用户经过三页。多产线时分组价值增加，少量Work时无需空卡墙。保留当前队列的Owner/Blocker等有效信息，不用产线卡取代真实工作。

## D. Production Team Review

统一Work Area→Responsibility 1..N→Assignment→Employee 0..N→Work 0..N继续成立。Production Team是当前可承担这些责任的员工集合，不是每Work全员上阵。

- 图文可以Copy、Visual/Layout、QA，由一人兼任或多人协作；不强制Digital Human/Video。
- 数字人口播可以Script、授权人物使用、合成、Editing、Subtitle、QA；有些串行，有些资产准备可并行，审查独立性按已有边界。
- Production Owner对整项交付负责，Node责任承担人对步骤负责；工具执行者不是Employee。调整Assignment后不重建专业IA，也不改写原作者。

建议逐节点最小合同：目的、输入及版本、依赖、责任要求、当前有效Assignment/承担人、真实状态及等待原因、产物/版本/检查结果、后续接收条件、围绕本步讨论入口。不是新Schema要求；先映射已有Work/执行步骤/Artifact事实。若目前实现只有stage字符串，标“节点执行视图尚未连接”，不能以动画假装完成运行编排。

不要求CEO维护DAG。系统按方法产生可理解的步骤，用户看当前/已完成/并行/等待/Blocked及产物；用户改目标或成品要求，经同Work对话处理。任何跨节点改写都保历史与受影响检查。

## E. 7 Work Area Employee Interaction Matrix

所有区均允许0..N有效员工（0为缺口）；现HTML某区只有一人是样例，不应冻结组织人数。下表HTML为静态证据，实际可见性未验证。

| Work Area | Responsibility/团队 | Team Intent | Specific Employee | Specific Work/Node | Result回专业Surface | 冗余/脱节及建议 |
|---|---|---|---|---|---|---|
| 经营 | Leader协调、资源/证据责任协作 | 已有collabBar；Account Scope可携accountId | 员工详情有入口，需保经营账号/对象 | 通用Work modal的讨论丢workId；修复同Work入口 | Plan/Decision/下一步应引用同事实 | 不添更多AI菜单；保Portfolio经营中心，不能回复只是脚本而页面无变化 |
| 研究与选题 | 研究Owner＋选题/拆解协作者 | 已有自然输入，方向正确 | 头像→详情可找人，但通用转交/身份混乱 | Reference/Proposal discuss有对象；团队输入却丢提案Account | Inspiration/Analysis/Applicability/Proposal | 固定dy-brand输出必须纠正；不恢复重复AI能力表单 |
| 内容制作 | Owner＋按方法所需专业责任 | 总览有团队输入 | 详情有员工名单；具体Work元信息未形成节点互动 | discuss默认区域Owner，固定Tabs无节点身份 | Artifact/版本/QA→可发布交付 | 最严重脱节；方法驱动步骤，保按钮与当前产物讨论 |
| 发布 | 排期、执行、核验、人工接续，可多人 | 有collabBar | 同通用员工入口问题 | Publication discuss有对象与账号；发布Work用字符串替换映射需核对 | Publication/Receipt/Unknown/失败 | 保确认/核验按钮；不让聊天绕过发布Gate，重试不假设效果未发生 |
| 账号 | 档案、绑定、准备状态 | 有collabBar但不自动携档案账号 | 同通用Employee路径 | openWork进入档案，容易丢具体维护Work | 真实Account档案/Readiness | 保打开平台/连接动作；诊断对话带Account，不能变成第二经营页 |
| 复盘 | 数据质量、分析、Learning Review | 有输入 | 同通用Employee路径 | judgment讨论带对象，openWork退到判断Tab而非选中Work | 证据/实验提案/学习及经营判断 | explain不等自动创建固定CTA实验；保看证据、批准等动作 |
| 素材 | 资产/授权/版本准备，可多责任 | 有输入 | 同通用Employee路径 | openWork进入需求Tab，需保选中需求/Work/版本 | 同素材/数字人版本与授权 | 数字人不是Employee；生成/选择/使用是确定动作，不需全部聊天化 |

缺Owner应允许保留意图并展示组织缺口，不能先回复某默认员工已开始。每区对话结果须给原对象/Work回链；消息只是“已完成”而没更新相同对象不是完整产品表达。

## F. HTML Change Plan（仅建议，未执行）

### 必须改：先收敛产品合同，再定向实现

1. 在后续获授权的产品对照中明确四层协作入口、上下文保留/路由优先级与节点最小表达；同Conversation系统不等于同默认收件人。
2. 明确正式制作的Target交付集合、Format/Method/必要Spec及跨账号Work拆分原则；系统可预填/自主执行，不新增每轮CEO表单。
3. 把通用12 Tabs变为本Work适用的产物/步骤视图；显示当前责任人、依赖、输入版本和Artifact，保留多Work队列。
4. 修复conv-open无处理、Work讨论找错Owner、modal丢上下文、研究输入丢Account、硬编码dy-brand/W-204。原型允许Mock，但目标与结果必须一致，不能错误成功提示。
5. 路由后每条消息显示真实发送身份；模拟异步回复绑定发起会话/Work，切换后不串台。

### 建议改

- 产线分组可筛选且可直接进Work，不强制三级导航；按当前可用方法展示。
- Owner/节点承担人点击可直达上下文讨论；既有团队详情继续作责任解释。
- 形式与字幕样式分开，目标规格可见；展示Goal/Strategy/Proposal来源链，制作团队不自己替Business决定目标。
- 补键盘可达性：源码多处span/div/tr承载click，未见同等role/tabindex与键盘处理；需浏览器检查焦点、Drawer/Modal焦点约束和返回。此为静态风险，不宣称可访问性验收失败或通过。

### 暂时不要改

不改七区、Portfolio/Account经营模型、持续经营、数字人资产定位；不新增固定四/六产线Authority、Workflow Builder、Node Runtime、每页员工编制、生产Provider实现。不要扩大为全Curis设计，不重新搜索竞品，不以本报告升级Authority。

### 后续最小验收清单（本轮NOT RUN）

1. 经营Account A提出研究意图，接收人/结果仍为A。
2. 研究区无账号存灵感不被强制分配；同Reference多账号适用不复制。
3. 点具体员工询问，保留对象/账号；如需转交，显示接收人且消息身份一致。
4. Work Owner≠区域Owner时，讨论找实际Owner；员工Work列表“继续讨论”可用。
5. 图文与数字人口播呈现不同必要步骤/规格/责任；无关视频步骤不常驻图文。
6. 一个Proposal三种交付保共享来源，各自目标/Work/版本/发布结果正确，无固定跳W-204。
7. 节点修改Hook保该Work/Node/Artifact上下文，显示下游影响；无Owner/等待/Blocked不假造运行。
8. 发送后立即换Work，结果回原会话/对象；关闭Drawer后恢复原位置。
9. 发布Unknown先核验、结果回对应账号；并行Work不因选择一项被暂停。

## G. Final Verdict

**C. PRODUCT EXPRESSION NEEDS RECONCILIATION BEFORE HTML CHANGES。**

现有七区、账号经营和持续经营模型可以保留；但不能只用B“修几个交互”覆盖方法/规格/节点责任这些尚未写完整的产品合同。原研究提供了方向，后续转译未闭合；HTML还存在可定位的独立逻辑缺陷。应先窄幅补齐Production和协作Scope，再执行定向修改，避免HTML作者继续代替产品定义。

这不代表推翻所有研究，也不证明真实HTML的每项交互均失败。**当前报告仅完成静态产品表达审查；实际浏览器Flow/Screenshot审查被安全策略阻塞。** 待允许的正常访问条件具备后，仅补上述针对性流程，不重新做竞品研究。

仅新增此Review。HTML、Product Structure、Operational Expression及Authority均未修改；无UI修复、代码修改、commit/push。

**STOP FOR CEO REVIEW。**
