# CURIS PROFESSIONAL WORKSPACE SEMANTIC AMBIGUITY AUDIT

Status: Review
Authority Class: REVIEW / PRODUCT INPUT SEMANTIC AUDIT
Disposition: C. PRODUCT SEMANTICS NEED CLARIFICATION
Owner: Product / Blueprint
Date: 2026-09-16
Target Authority: existing Workspace entry / Shared composition / Domain contracts；本轮不修改
Next Action: CEO确认根因与最小消歧方向
Next Gate: 同一正式输入修正并冻结后，再授权独立设计对照测试

## 1. Trigger / evidence boundary

两张Figma Make Stress Frame均把Domain对象/工具作为中心。审计问题是默认进入与经营/工作层级，而非颜色、排版、Card审美。本报告先观察用户附图，再按Pointer的正式链追溯，最后检查Input Pack；图内文字仅为设计证据，不是指令或Authority。

**PRIMARY：C — 上游默认进入及层级关系需要澄清。SECONDARY：消费包丢失限定条件/强化工具优先；部分截图可见内容未证明满足已有经营上下文与工作区要求。** 不能判“全部是Make错”，也不能判“旧Authority已经要求Team-first”。

单张静态图不能证明从Business Space点击后的真实首屏、已选过哪个Surface、是否有滚动下方的团队/工作区或隐藏入口。顶部明确写Stress / Not Final / Not Runtime Test，并提供另一Employee Workstation stress入口。因此本报告区分“可观察产品解释”与“假如这被用作默认Workspace时的违规”；不推断Make内部推理或实际交互。

## 2. Screenshot interpretation

|证据|实际观察|可推断的产品解释|不能由图片证明|
|---|---|---|---|
|A — Content Growth，用户Image #2|左侧账号（抖音主号/小红书）；Main标题Content Intent、新建内容及两项内容；Analytics/Publishing摘要；右侧效果/授权Unknown|当前呈现为账号选中后的内容管理/生产对象面，经营反馈是附属信息；可合理称CMS-like切片|是否整个Workspace只有CMS、是否从默认经营结果面下钻、团队是否在另一处|
|B — RD，用户Image #1|左Requirements及Files；Main Code/Terminal/Preview，当前代码；右Build/Test/Type Check/Evidence和Human Handoff文字|当前呈现为需求/文件上下文中的专业编辑/验证切片，接近IDE-like工作现场|是否直接从Workspace入口打开代码、是否属于已选Employee/Work、是否已有返回经营面操作|
|共同模式|Context选对象→Main操作对象/工具→Utility查看验证/结果；本帧没有清晰Workspace Leader/责任归属、轻量经营四语义、Shared Employee Work Area|两者验证了工具/对象可承载性，却没有验证经营空间入口及团队持续经营关系|不能据此断言两种Domain都应先显示Team、或工具不得进入Main|

图片原始路径（仅本次证据，临时路径不保证永久可用）：
- A：`/var/folders/80/w7l2qyt12zx9_n8tg2vgy_pw0000gn/T/codex-clipboard-b140516f-2905-4a47-b7a0-c4da14dd784d.png`
- B：`/var/folders/80/w7l2qyt12zx9_n8tg2vgy_pw0000gn/T/codex-clipboard-e83844de-fda8-4786-b8f8-811b73fb9904.png`

没有重画/编辑图片，没有检查未提供的Figma节点或运行路径。截图中的Fixture成绩、人物/公司与代码不作为实施事实。

## 3. Authority baseline / evidence ledger

按以下顺序读取相关Current段；行号为本次文件位置，章节为稳定定位。

|ID|Source / section / line|Status与本题证据|
|---|---|---|
|P0|[Pointer](../00_Context/PRODUCT_DOCUMENT_POINTER.md)，Current Required Input，13–27|Frozen router；RD仅当前域对象/责任，Shared/旧composition受上位约束|
|P1|[Blueprint](../01_Product/Curis_Product_Blueprint.html)，Workspace/Professional Workspace表，232–241|Frozen Current；Workspace拥有完整经营事实与Shared Team/Employee Area；Main selected Surface，不固定Overview|
|M1|[Master Map](../01_Product/Curis_Product_Master_Map.md)，207/215|Current派生；轻量Current Operating四语义；CG默认CEO Operating Result；其他Domain默认由声明决定|
|M2|同Map，294/307/325/339/343|目录可直接进Workspace；长期Workspace由Team承载；责任对话带Scope；Team Operating是默认责任协作，不是完整Operating Loop|
|M3|同Map，对象表401–403、A5及能力Entry 119|Workspace Entry/Drill-down到selected Surface/Leader/Employee/Result；团队运转按需编辑；工具从Workstation或Workspace专业Main进入；A5只保证首Workspace落点|
|U1|[UI Blueprint](../01_Product/Curis_Product_UI_Blueprint.html)，42/48/52|Current Consolidation：专业Surface为最大工作主体，工作按需进Main；CG默认经营结果；Work/对象/能力缺口为工具入口|
|U2|同UI，228–232/244/255/285–286|Workspace是完整结构；团队运转与Workstations按需展开；Current Operating默认轻量；RD旧首版范围仅历史；CG日历不是Workspace Default|
|S1|[Company OS Shared](../03_Design/Curis_Company_OS_Shared_Authority.md)，59/95/326及§12/16|适用Frozen；Domain定default，Lifecycle≠Team Operating编辑器；Browser/Tools按真实工作能力，不新增产品区|
|H1|[Frozen Shell](../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)，§0.1，49–63|Main可独立理解业务整体；Domain Business Surface+Shared Work Area；员工进入Conversation-first，但工作区局部不抹掉业务展示责任|
|H2|同Shell，§3.1，294–301|长期Business Workspace+真实AI Team的Shared Work Area非可选；真实员工轻量Row；单working外部进入初始一次展开；多员工默认策略未额外定义|
|CG|[Content Growth Domain](../03_Design/Curis_Content_Growth_Domain_Authority.md)，§0.1 / §5.4，34/169–194|Frozen Domain合同；Professional Workspace仍Candidate。经营结果default；Account长期经营≠生产，责任在Curis员工|
|RD|[RD Instance](../03_Design/Curis_RD_Workspace_Instance_Spec_v1.md)，头部/§1，5/34，§1a/§2/3|RD INSTANCE APPROVED的scoped当前依据；旧工位栈/首版工具上限已收窄；真实研发对象/Version/Build/Test/Review/Blocker为核心，复杂工作Main/辅助阅读Utility|
|IP|[Input Pack](CURIS_FIGMA_DESIGN_INPUT_PACK.md)，§05/08A/10/12/21/22|Review / consumption only；最后读取，不作为自证Authority|

未读最近研究合集、未以Runtime状态决定Target，也不把旧RD Figma/Reserved行恢复为Current。结构Baseline没有提供本题独立的通用首屏选择算法；不另造Authority。

## 4. Business / Workspace Entry

**已确定：** Business Space的Business入口→Business Work Surface（Definition/Operating Status/Workspace Directory/Team摘要）；Workspace入口/目录→真实Workspace；也允许直接Workspace入口，不强制所有访问先过Business页（M2/M3）。Activation成功只确定First Workspace和来源回程，不确定哪一个内部Surface默认选中（M A5）。

**Workspace不是Domain Primary Surface的等号。** P1/M3明确其还包含身份、Leader、Goal/Rules、Domain Navigation、多Surface、Shared Team Operating、Shared Employee Work Area。专业面是其组成部分。问题不是没有对象定义，而是组成清单未完整转化成进入状态及优先级。

“?”目前可回答为：**当前selected Professional Surface +相关Shared Work Area，轻量经营摘要；具体默认由Domain决定。** 不能进一步普遍回答Team、Code、Account或Conversation。通用文件未完整区分新建落地、普通目录进入、回访恢复、Employee入口、Work深链的选择优先级。

|路径|已有唯一规定|未闭合部分|
|---|---|---|
|CG普通进入|Domain默认CEO Operating Result /经营结果面，非Publishing Calendar|该面必须呈现哪些跨账号/Team/Work事实、如何与账号详情/生产面分层，字段/状态未形成足够唯一首屏|
|RD普通进入|真实研发对象/Version/Build/Test/Review/Blocker为专业核心；不默认工位栈覆盖Main|没有指明普通进入选Version/Requirement概览还是已选文件，Code/Terminal是否只能在工作深链中成为当前Primary|
|具体Employee进入|Main工作区Conversation-first，合法责任上下文；单working初始展开规则存在|和当前selected Domain Surface保持/切换的组合规则、来源焦点恢复不是完整状态表|
|具体Work/工具进入|原Work/对象/能力入口→Main完整工作或Utility辅助→原处|不要求全部经Employee点击；目录入口与此深链的优先关系未统一|

因此不能强行补出唯一串行链“Workspace→Employee→Work→Tool”。已有合同允许Work/Object直接入口；CEO先见团队并不是Current已定答案。

## 5. Team Operating

不是只有口号：P1/M2/H2明确Team承载责任，Leader有经营职责，长期Workspace的Shared Work Area是组成部分；M3定义“专业Workspace→团队运转→按需编辑器”，字段Role/Responsibility/Binding/Input/Output/Default Flow及版本已明确。

但“团队持续经营”与专有名词**Team Operating（团队运转/默认流程）**不能混同：后者是责任协作定义，不包含完整Loop、模型能力配置或Execution状态（M343/S326）。把它直接设成默认入口，可能把CEO送进责任编排编辑器，而非经营现场。

缺少的是：普通进入时如何可消费地知道谁负责、正在推进什么、为什么、下一步，以及如何到Workstation/专业对象，并与轻量Current Operating/Domain Primary组合。不是缺少Team对象或要求新增Team Dashboard。H2已有真实员工Row要求，输入提取不应稀释为仅“员工能力可达”。

## 6. Domain Primary Surface — 三句逐条核验

|表述|单独合理性/来源|组合后层级与入口|Team / Tool / Employee条件|截图风险|
|---|---|---|---|---|
|“Domain Primary Surface是唯一可最大占视觉面积区域”|IP§10；U42支持“专业Surface最大工作主体”，P241 selected Surface。严格“唯一可最大”是提炼措辞，不是默认选择算法|规定视觉主次，不规定哪个Surface默认；不能从最大面积推出工具首屏|不取消H2 Shared Work Area或Current Operating；无员工进入时机细化|容易将最多屏幕给编辑器、把经营全部推右|
|“完整专业操作可在Main”|IP08A；RD34、U48/M119支持|能力/承载许可，不等“首次进入必须专业操作”|已有Work/对象/能力入口；无规定只能Employee进入后才可用|从“可以”偷换“default”，合理诱因明显|
|Professional=Shell+Domain Surface+Shared Team Operating+Shared Employee Work Area|P237/M325/U229；IP10省略多Surface/局部导航等细节|不是等号简化成Domain Surface；缺进入选择和各组成初始披露合同|U按需展开；H长期团队工作区必有；对多员工初始焦点未定|组成名词有了，设计Agent仍可能只画明确对象/工具|

组合后有**职责分工**，但没有完整**进入层级/选择规则**。单独正确并不能保证组合充分。尤其“轻量”“按需”“不Dashboard/不Employee Wall”等限制远比“保留经营可理解性及真实责任入口”的正向示例具体，形成不对称优先级。

## 7. Employee Workstation / Conversation / Work

H §0.1与§3.1已有清楚约束：具体员工进入统一Conversation-first；长期真实Team工作区是Main组成；Row可展开，收起不停止，Runtime不驱动布局。它不是一整页员工监视器，也不是Provider身份。

两图均无可见Employee/Holder/当前Work入口，顶端“Employee Workstation”是Stress frame切换标签，不能替代Workspace内真实员工可达合同。若图仅工具局部截图，不能断言完整产品不支持；若作为完整经营Workspace验收，现有责任与工作区证据不足。

Conversation是持续工作关系；Work是有Scope/责任的真实工作；工具是工作能力现场。当前Authority允许从对象/Work直接进入工具，故“所有Code必须在Employee之后”不是已证实规则。需要澄清的是即使深链进工具，原责任/经营上下文怎么保留与返回，而不是强制多一次点击。

## 8. Content Growth findings

四层语义在数据/责任层**部分明确**：Business/Workspace方向与合法经营边界（M307、CG171）；Account Goal/Strategy/Cadence/Plan/History/Result/Learning（CG§5.4）；Intent→Platform Form→Account Context→Variant及逐账号Publication（CG175–186）；Curis员工负责发布/分析、Provider只能力（CG177）。因此不能把Domain说成只有内容生产。

**首屏方向明确，具体进入合同不充分。** CG34/194、M215、U52/286反复指定“CEO Operating Result /经营结果面”；这比IP§08A罗列账号/内容/发布/反馈更强。截图A中心是Content Intent，新建内容是主动作，没有清晰Workspace经营结果层。如果声称默认入口，它不符合该明确方向；不能将“无外部数据”当作允许用生产列表替代整体经营表达的依据。

另一方面，“经营结果面”没有把Workspace整体/Account经营/内容生产/Employee Work之间的默认展开、选中Account及返回关系定义成完整状态合同。不能凭该名称断定第一屏必须Team/Current Cycle/Leader占多大面积。8状态/4桶仍候选，不能拿来补现行缺口。

## 9. RD findings

RD34确立专业核心：真实研发对象、Version、Build、Test、Review、Blocker；明确废止旧工位栈/首版工具上限作为当前约束。§2/3允许责任/文件Context与Diff/Code/Preview辅助、回Conversation。S§16允许File/Terminal/Git/Preview作为共享专业能力。

这支持截图B作为**研发工作切片**，但没有明确授权“普通Workspace进入→Code编辑器默认选中”。Goal/当前产品或Version/优先级/Leader责任/Current Work/Next与Requirement/Delivery管理、工具执行之间，仍主要是清单和承载规则，非完整入口分层。

也没有现行证据禁止Code/Terminal成为某一selected Professional Surface，或规定只能先Employee再工具。旧Reserved表不能作为反证；也不能把“工具目标已批准”作为“默认进入已批准”。Build/Test放Utility可作为当前代码验证辅助，但若那是理解整体研发阶段/阻断的唯一来源，违反Main自成立的责任，而非工具本身错误。

## 10. Four-Pane findings

Left对象 / Main工作 / Right辅助是一种**合法映射**；不是天然误用。错误是把它当唯一Workspace解剖，或认为经营/团队必然放不进去。

H51/63要求Context/Utility关掉后Main仍理解整体业务，并保独立业务展示责任；H294–300要求长期团队工作区。RD截图关右侧后只剩代码，CG关右侧后只剩内容条目与授权提示：可见帧未证明这些要求满足。辅助侧栏打开本身不能判违规（可能已由用户打开）；“结果必须固定右侧”则无依据。

不需要先改变Four-Pane。需要区分经营空间的默认进入与已聚焦专业对象；“Primary最大”解决面积权重，不能替代默认选择、上下文持续与团队可达合同。

## 11. Input Pack findings / self-correction of prior audit

**PARTIAL / 有合理诱导。** IP08A的RD工具枚举及“完整专业操作可Main”、比较表“文件/代码、Terminal…”、IP10最大面积句一起强化了最具体的对象工具；没有同等强度定义默认Entry。CG比较表虽写“Domain默认经营结果”，没有充分展开该限定。不是新增“工具默认”明文，但可合理引向当前两图。

更具体的提取损失：IP12说明Row/员工进入，却没有同H§3.1一样明确“长期Business Workspace＋真实AI Team，Shared Work Area非Domain可选项”；IP05也没有完整保留H63“即使钻员工，Main仍保独立业务展示责任”的条件。这些已有上游依据，可在获授权后纯消费修正，不必新增对象。

IP的Work入口/Return矩阵证明“能进入与返回”，不等证明“Workspace普通进入选什么”。上一轮17问/8问YES是文档覆盖检查，遗漏本轮默认进入的条件压力测试；**不能继续将其解释为Workspace Entry语义已充分验证**。本轮只在本报告记录该局限，不修改Pack或旧Audit。

## 12. Semantic matrix

|Concept|Current Authority Definition|Default Entry?|Main Responsibility|Relation to Team|Relation to Employee Work|Ambiguity|Screenshot Misread Risk|
|---|---|---|---|---|---|---|---|
|Business|持续身份/方向/Workspace组合（P232/M401）|有Business Work Surface，也可直Workspace|管理与目录，非内嵌工作详情|Leader与Team摘要|通过Workspace/Leader进入|低；不等Workspace|把账号当Business|
|Workspace|完整独立经营与专业环境（P237/M402）|到Workspace确定，内部selected未普遍确定|多Surface+Shared区+轻量经营|长期Team承载|员工/Work入口并存|默认选择条件不足|Workspace=CMS/IDE|
|Workspace Home / Entry|Entry路径存在，未检出独立Home对象合同|CG有default命名；RD未指定具体首屏|不得自创Home|初次团队披露未全定|普通进入与深链未分类|高|一个工具面冒充完整入口|
|Current Operating|状态/本轮重点/最新判断/下一步（M207/U232）|默认轻量|经营摘要，不Dashboard|责任经营上下文|不等运行日志|和Domain/Team组合不足|因“轻量”被省略|
|Team Operating / Shared Team Operating|责任协作/默认流程（M343/403）|按需编辑，不规定first|共享团队运转，不完整Loop|Role/Binding/Input/Output|不等Execution状态|“Team-first”可能误成编辑器first|文字存在但不知到哪看|
|Domain Primary / selected Surface|Domain具体工作面（P241/U42）|Domain声明，CG经营结果|主要工作主体|与Shared区共存|可对象工作也可工具用途|Primary与default混读|最具体工具占满|
|Shared Employee Work Area|长期真实Team的Main组成（H294）|必有但初始披露不全定|员工Row/展开工作区|真实团队投影|承载Workstations|“按需”被读成可省略|完全没有团队关系|
|Employee Workstation|具体Employee Conversation-first（H61/286）|具体员工进入确定|工作区内完整对话/过程/引用|同身份责任|直接处理工作|与selected Surface切换/保留需明确|只能另一个独立示例页见员工|
|Conversation|持久关系/合法Scope（M339/H）|Employee/Topic入口明确|完整工作Main|责任上下文|不是Execution log|不是所有Workspace唯一首屏|Conversation-only或完全消失|
|Work|真实责任工作/输入输出/状态（P237）|对象/员工/深链可达|执行与结果可追溯|Assignment归属|唯一系统|默认Workspace到Work选择不足|代码与员工无归属|
|Professional Working / Tool Surface|工作能力承载，不新Workspace（M119/S12/16）|按需原Work/专业Main|复杂操作Main/辅助Utility|通过权限责任使用|File/Code/Terminal等|许可≠default，非必须经员工点击|工具就是经营整体|
|Domain Object|CG Account/Variant；RD研发对象（CG/RD）|各Domain不一|当前操作对象|合法负责Assignment|可产生/关联Work|集合/详情/经营层未全映射|对象列表代替经营|
|Context|局部导航/集合/bounded context（H）|按需，非永久列|不是整体理解唯一来源|不能第二员工目录|文件/责任引用|不负责决定Main初始状态|左侧对象选择定义全产品|
|Utility|当前对象辅助Detail/Preview/Evidence（H）|按需|不承载不可缺整体事实|非固定员工/结果栏|辅助阅读与返回|把“可辅助”变“必须右侧”|经营结果/Blocker被移走|

## 13. Root cause classification

- **C. AUTHORITY AMBIGUITY — PRIMARY。** P/M/U/S定义组合和Domain default，但RD普通进入、回访/深链选中及持续经营上下文不唯一；多员工默认焦点H301明确未额外定义。
- **E. PRODUCT CONTRACT GAP — bounded。** 缺的是入口条件×初始selected Surface×经营/团队保留责任×到工作及回程的组合合同；不是所有经营对象都没定义，也不是需要新Home对象。
- **B. INPUT PACK AMBIGUITY — SECONDARY。** 对已有Main自成立/长期Shared Work Area限定提取不足，对工具可用性过度具体；应修正优先级，但仅修包无法凭空补RD默认选择。
- **A. DESIGN AGENT MISREAD — 条件性局部。** 若截图是普通CG默认入口，Content Intent-first不满足明确经营结果default；若两图作为完整长期团队Workspace，必须证明现有工作区和经营上下文。当前截图未展示进入序列，不支持“全部Make错”。
- **D. AUTHORITY CONFLICT — 本轮未确证不可调和冲突。** H旧“Pattern可选”和后续长期Team工作区必备有明确适用限定；RD旧栈/Reserved被§1收窄；CG特定default不与全局可选Surface相矛盾。不能为获得CEO裁决把未充分定义冒充两个明确相反答案。

## 14. Minimum semantic correction options — proposals only

|Option|对象/Four-Pane|Primary变化|CG / RD /未来Domain|一人AI公司与复杂度|
|---|---|---|---|---|
|A 默认Team Operating|不必新对象，不改Shell；但须防既有术语变义|若把责任编辑器提升默认，改变当前Domain-default政策|CG须解释经营结果default；RD可能遮蔽研发工作；其他行业同样被团队编辑主导|责任明显但未必经营清楚；不推荐直接采用|
|B 普通进入Domain经营投影，专业对象按需聚焦|复用Workspace/selected Surface/Current Operating/Shared区；不新Home对象|明确default而非取消专业Main最大；字段由Domain承担|CG已有方向可细化；RD需确认default契约；未来Domain同样声明|保持专业性与经营可理解，增加的是合同精度，不必加Tab|
|C 按入口/当前Work动态选择|复用现有refs/Surface，不改Four-Pane|普通/深链/回访有不同selected规则|支持两域真实工作与回程；必须有确定fallback和可理解上下文|效率好，但若只说“智能决定”会再歧义；规则复杂度稍高|
|D 仅修消费包限定，不补Authority|零对象/结构变化|恢复Main自成立/Shared区/CGdefault|可纠正部分图，仍不能回答RD普通进入唯一选择|最小但不能完全关闭本轮问题|

推荐CEO评估**B作为普通进入规则 + C仅对显式Employee/Work深链及回访规定例外**，同时做D的忠实提取修正。不是本轮正式新Truth，也不预设一个Dashboard/Home页面。无需新增Workspace Home canonical object；若CEO不选该方向，先明确其他default规则再画。

## 15. Cross-domain impact / counterarguments

统一的是经营上下文、真实责任、default选择与回程可解释，不是两个Domain同布局/Workflow。CG能保Account/Variant生产工具，RD能保代码/Terminal；两者都不能因此消失Team/Work关系。

反证：全部Team-first会把公司系统变责任编辑器；全部工具-first会让经营语义退化；强制每次经员工再工具增加无必要步骤；新Home对象增加平行真源；“按需”无入口会把关键能力实质隐藏。现有对象足够，优先CLARIFY。

## 16. Recommended next step / scope and validation

请CEO确认两件事：普通Workspace进入的默认选择原则；显式Employee/Work/对象深链时必须保持哪些经营/责任上下文与返回条件。CG不必重审账号模型；RD不必重研流程；只需明确已批准对象之间的进入合同。

之后才授权窄幅Authority消歧及Pack同步。相同测试输入应明确“普通目录进入”与“已进入专业Work”两个条件，分别让Make与另一独立Agent设计CG/RD；对照是否保经营语义与真实责任、是否误把深链当default。不能用当前两张无入口前史的Stress切片独自证明因果。

本轮仅新增本报告。未改Authority、Input Pack、Manifest、Visual、Domain/RD、代码；未开始Figma，无commit/push。检查：报告本地相对链接及git diff --check；不宣称用户测试/Runtime/全仓Authority审计完成。

## 17. Final verdict

**C. PRODUCT SEMANTICS NEED CLARIFICATION。**

PRIMARY：上游默认进入与经营/专业工作组合合同不充分（C + bounded E）。SECONDARY：Input Pack限定提取不足/工具优先诱导（B），截图作为默认入口时存在局部不符（conditional A）。未证实需用D裁决的当前Authority硬冲突。

当前Input Pack会**部分合理诱导CMS + IDE式结果**；已有Shared要求和CG默认又限制这种解释，故不能以包自证设计无误。不是现在确定“Team-first正确”，也不是禁止专业工具Main。先消歧，再重测。

STOP FOR CEO REVIEW。
