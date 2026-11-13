# Curis Product Master Map v3.2

## Shared Employee Interaction — 2026-09-23

Status: Frozen · Authority Class: CURRENT / PRODUCT EXPANSION · Disposition: CEO ACCEPTED / RECONCILED。仅展开[Blueprint](Curis_Product_Blueprint.html#shared-employee-interaction-20260923)与[Shell §3.1A](../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)，不是独立对象或Schema。

|Surface / source|字段与动作|保留 / 返回边界|
|---|---|---|
|Professional Object / canonical Work与Domain对象|对象、版本、轻量Employee Bar：头像/姓名/Responsibility/必要状态/一起讨论|Holder ≠ Executor；无重要状态不常驻Idle；Reviewer仅在贡献处出现|
|Optional Conversation / 既有Conversation|默认隐藏；一起讨论、讨论这段、要求修改展开；Shared Composer真实能力|收起保history/input/selection/object/target，不改变执行；在Bar下、专业Main上|
|Selection / 既有引用＋专业Locator|Object、Version、Locator、短摘录/描述、Return Anchor；定位/移除/更换|stale不自动指向latest，重选/重比较；scope逐次校验|
|Result / Domain专业Main|Preview/Compare/Review/Audition；Accept/Reject/Revise明确对象/版本/效果|引用Utility检查后回同Main；Viewed ≠ Accepted；业务转换各自定义|
|Global CEO Assistant / 同Company identity|轻量全局浮层，专业讨论时视觉降权|不替Employee回复，不占Pane，不复制Conversation|

普通创作选择不是P7，Review不是Handoff；CG脚本采纳≠视频/发布，Writing草稿→审校→作者确认，Music选版→明确Master确认。仅冻结交互职责，不冻结统一布局或Provider能力。

## BUSINESS ACTIVATION PRODUCT TRUTH PATCH — 2026-09-15

Status: Frozen · Authority Class: CURRENT / PRODUCT EXPANSION。来源：[Blueprint](Curis_Product_Blueprint.html#business-activation-20260915) → [Company OS §19](../03_Design/Curis_Company_OS_Shared_Authority.md) → [Workspace Engineering §1.0A](../05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md)。以下字段是信息责任，不是DB Schema或要求CEO逐项填写；本轮不宣称Catalog/Migration实现，不发布Content Growth。

标记：P=批准产品关系，T=目标能力/状态，C=真实来源值（可以Unknown）。系统提供默认建议，用户只确认必要事实/边界。所有入口仅消费同一Company Truth/Proposal/Creation；没有第八导航或第二能力库。

### A1. Business Creation

- Mission / Sections：从可开展业务或其他经营意图形成合法Business；发现、详情、提案、确认、创建结果。Main工作面，不是Settings/Utility/小Modal。
- Entry / Context：Business Space“新建业务”（0/N同一逻辑）；Organization“新建→新建Business”（与新建Department区分）；Assistant自然语言。P字段逐项：Company ref、origin view、Department suggestion、Conversation ref、Intent、return anchor。
- Fields：P: selected Package ref、Generic path、proposal ref；C: 当前合法Company context、已有相关Business refs、来源查询、筛选、滚动位置、已输入内容；T: 创建中、失败原因、恢复/确认结果引用。没有Model配置/重复Binding字段。
- Actions / Create / Edit：浏览、描述其他业务、查看详情、起草/修改必要事实、确认、取消、恢复；Create只落实确认的同一提案，重复确认先查结果。无AI允许可确定事实/手工确认，不伪造研究。
- Drill-down / Return：包详情→Proposal→真实结果；取消回来源；Organization成功回原图选中新Business，Assistant回同Conversation，Business Space保First Workspace landing与目录回程。
- Shared / Source：Shared + Package投影；Blueprint Activation / Shared§19。

### A2. Catalog Item

- Mission / Entry / Sections：帮助发现已发布可启用专业业务；Creation发现区，不是用户Business目录。空Catalog仍可描述其他业务。
- Fields逐项：P: Package identity、display name、经营价值摘要、适用对象摘要、source/maintainer ref；C: released version ref、allowed activation scope、重要限制、publication decision ref、当前用户合法可见范围、已有相关Business refs/数量（有可靠来源才显示）；T: 详情入口、Generic入口。分类/搜索关键词按规模可选；版本/证据按需高级，不每版本复制业务卡。
- Actions / Create / Edit：查看/返回、选择经营方向；不在此创建Business，不编辑Package真源；未发布无启用按钮，不把Research/Candidate当可开展事实。
- Drill-down / Reverse：同一Capability Detail/已有Business；返回保搜索/位置。Shared projection；Source=Package发布记录，不是Company配置状态或新Catalog DB。

### A3. Business Capability Detail

- Mission：判断适不适合、启用后能做到什么；Entry=Catalog或Assistant，Main阅读/决策面。
- Fields逐项：P: 经营对象、结果类型、适用情况、不适用情况、经营方法摘要、Curis responsibility、User responsibility、所需准备、Human Handoff边界；C: 当前真实支持、限制、来源、维护者、允许启用范围/原因；高级C: Package version、validation scope、evidence refs、migration policy、support window。未知不填假承诺，Company缺模型/账号不降Package资格。
- Sections / Actions：价值/适用、怎么经营、边界/准备、来源；已发布“启用具体业务”→提案，未发布只明确尚未开放及Generic路径。不直接运行/绑定Provider。无独立Create/Edit真源。
- Drill-down / Return：验证/版本/来源（按需）→回同详情；回Catalog/Conversation。Mixed；Source=Package＋Shared§19，Content Growth状态依Domain。

### A4. Business Proposal / Activation

- Mission / Entry：把Intent＋Package/Generic＋Company Context转换为真实经营提案；复用Conversation/Structured Proposal，在Guided Main，不做长表单Wizard。
- Fields逐项：P: CEO Intent、Business name、Package/Generic path、Goal、当前假设、Department ref或新建建议、First Workspace建议、Leader ref/缺口、Responsibility requirements、Employee Assignment建议、Company organization effects、必要缺口、initial Work、permission boundary、budget boundary、automation boundary、必要确认事项、proposal/confirmation refs、return anchor；C: current context/version、合法创建权限、选定发布版本/范围、校验时间、创建结果。无证据写Unknown，建议≠已落实。
- Sections：你的目标、建议怎么开始、准备先做什么、需要确认什么；组织/责任/环境作为影响说明，非每项同权卡片。只有真正影响确认的组织变化/风险默认显露。
- Actions / Create Fields / Edit Fields：确认创建、修改必要名称/目标/归属/边界、选择扩现有或独立、取消/恢复；系统推导字段不要求全填写。最终Create=同一canonical Business＋First Workspace＋合法Department关系；真实责任/Assignment如实落实或缺口，不能假Holder。快照变化重查，不重复创建或静默换包。
- Drill-down / Return：已有Business、合法Employee、Package范围→回同提案；失败保输入和原确认结果查询。Shared；Source=Bootstrap / canonical hierarchy / Shared§19。无Model不是创建门禁，依赖AI生成时能力不足诚实等待。

### A5. Created Business Summary

- Mission / Entry：确认真正创建了什么，而非“包安装成功”；来自同次确认的持久结果。
- Fields逐项：C: Business identity/name、Department identity/name、First Workspace identity/name、真实Responsibility、Assignment/Holder或缺口、组织关系、实际Package版本关系、当前可做Work、Work capability limitation、next action、source/return refs。
- Actions / Sections：查看真实结构/责任/下一步，进首Workspace/原Business、回Organization/Conversation/目录；无独立Create/Edit。Business+First Workspace或含新Department结果不一致不能报告成功；后续Work不Ready不删除已建Business。
- Drill-down / Reverse：同一Business/Workspace/Employee；两区域同一数据。Shared；Source=canonical creation result，非Catalog fixture。

### A6. Package Update / Migration

- Mission / Entry：同Business/Workspace发现新版本→看影响→兼容/提案→必要Decision→升级/恢复；Main复杂提案，Utility仅辅助证据，无Migration Center。
- Fields逐项：C: Business/Workspace refs、current Package/version/config refs、target immutable version、publication/support refs、compatibility result/unknown、check time、affected scope、method changes、object/field mapping、Company customizations、responsibility changes、capability changes、provider/destination changes、permission changes、cost changes、in-flight Work refs、Approval snapshots、EFFECT_UNKNOWN、pause/write impact、effective time、preflight result、recovery point scope/integrity/exclusions、rollback condition、post-upgrade new-data protection、other-Business protection、owner、next action、confirmation snapshot、application result、resume result、history/return refs。
- Actions / Create / Edit：查看、合规延后、准备、必要确认、开始政策允许更新、查看失败及安全恢复；Create/编辑仅既有工程Proposal/Work中的影响计划/确认，不新建Migration对象、Business或Package系统。源/目标/重大影响变化重计划，不手工改Evidence。
- Contract：UI version≠Data Truth；纯布局通常不迁移。新字段Unknown、旧字段/旧语义保留；在途不热切、未知外部效果先核验。回退不能覆盖其它Business/升级后新事实；不安全原地则同Business sibling Workspace受控交接。新权限/Provider不自动获批。
- Drill-down / Return：版本/工程Evidence/现有Decision→回原计划→原Business/Workspace继续；失败不无条件重试。Mixed；Source=Shared§15/17/19＋Engineering§1.0A。Target Contract，实施验证另Gate。

## 2026-09-15 CURRENT CONSOLIDATED CONTRACT — Product / Target / Current 分层

Status: Frozen · Authority Class: CURRENT / PRODUCT EXPANSION · Disposition: CEO ACCEPTED DECISIONS APPLIED; CONSOLIDATION REVIEW REQUIRED.

本节展开[唯一Blueprint](Curis_Product_Blueprint.html#consolidation-20260915)、[Company OS Shared §10–18](../03_Design/Curis_Company_OS_Shared_Authority.md)与[Content Growth §5.4](../03_Design/Curis_Content_Growth_Domain_Authority.md)。旧日期段的实现/视觉记录不是新能力验收；七区与Company → Department → Business → Workspace不变。无新增Browser/Model/Background/Recovery一级区。

字段标记：**P = Product Truth**（已批准语义，非预设DB字段）；**T = Target Capability**（交付义务/所需状态）；**C = Current Capability**（实际来源提供的值/证据，可Unknown，不代表本轮已实现）。不得以字段存在推定Runtime支持。所有目标完整合同G1-V～G6-V **NOT RUN**，Interactive Browser **NOT VALIDATED**；既有接受链只按CURRENT_STATE原证据消费。

共同Return Contract：Entry保留来源Company/Department/Business/Workspace、Employee/Assignment、Work/Conversation与对象引用；只使用授权上下文。完成、取消、修复/重连后返回原工作、输入与查看位置，重新核验再继续；关闭页面不制造成功或停止责任。复杂工作Main，辅助详情Utility，局部对象Context；具体组件DESIGN OPEN。

### 1. Browser / Web 工作能力

- **Page Mission / Sections:** 完成合法Web研究/交互浏览；问题与来源、当前站点/账号、动作/观察、权限/接管、结果/恢复。
- **Entry:** 原Work / Employee Workstation / Workspace能力入口；Talent发现/绑定，Settings修复连接。不是独立Browser产品导航。
- **Fields（逐字段）:** P: Work ref、Assignment ref、scope ref、研究问题、站点/URL、目标对象、账号ref、动作目的、来源ref、返回锚点；T: Search/Reader/Interactive模式、读取范围、上传/下载资源范围、允许动作、接管原因、完成判据；C: 连接/登录状态、实际账号、权限有效状态、当前动作、观察状态、提取范围/截断、来源时间、Evidence refs、错误原因、外部效果判断、下一动作。
- **Actions / Create / Edit:** 提出研究、选择授权来源/账号、阅读/引用、开始已授权动作、观察、停止/接管、报告完成、核验、修复后续接。Create只形成原Work中的请求/引用；Edit问题/范围/目标必须重新检查授权，不能编辑已发生Evidence。
- **Drill-down / Reverse Entry:** 来源→Reader，复杂浏览→Main，证据→Utility；从Result/Conversation回同Work。不新增Browser profile truth。
- **Shared / Source:** Shared；Company OS §11–12/15，Shell空间合同。当前完整交互浏览G1-V未验。

### 2. Human Handoff / User Required

- **Page Mission / Sections:** 清楚完成不能代理的必要动作并接回原责任；发生了什么、为何需要人、去哪里/做什么、核验/继续。
- **Entry:** 原Work/Conversation/Workspace；CEO Desk Matter/通知/Assistant仅给真实需要的入口。
- **Fields:** P: Work ref、Responsibility/Assignment ref、scope、目标/账号ref、合法操作者、来源与返回锚点；T: AI已完成内容、需要人原因、用户动作、目的地、完成判据、完成后继续内容、失效条件；C: 等待原因、报告者/报告时间、manual标记、Evidence refs、核验状态/限制、权限是否仍有效、下一动作。
- **Actions / Create / Edit:** 在原Work请求接续、打开目标、接管/交还、补材料、报告已完成、核验、暂缓/升级；不新建HumanWork。Edit允许补充事实/说明，不改原证据。涉及经营取舍再关联P7，责任转移另按P5。
- **Drill-down / Reverse Entry:** 原动作/来源/Evidence→原Work；用户离开或沉默保持真实等待。Shared；Company OS §11、Shell §3.11。

### 3. Model / Provider Connection / Capability

- **Page Mission / Sections:** 选择可用用途能力、连接和修复；连接、发现、模型事实/证据、用途默认、能力测试、受控fallback/限制。
- **Entry:** CEO头像→模型配置/AI能力设置；Work/Employee遇缺口定向进入并返回；人才与能力只发现/绑定，不复制模型管理。
- **Fields:** P: connection ref/name、Provider identity、Model identity/version、tenant、purpose、选择来源层级、Employee/Work refs；T: 认证方式、用途要求、合法数据目的地/region、预算/权限范围、fallback允许边界；C: Credential availability、Health、Discovery complete/partial、模型可用性、输入/输出modalities、Vision、Reasoning、Tool Calling、Computer Use、Context硬限、Output硬限、Cost estimated/actual、Rate limit、source、checkedAt/freshness、per-capability SUPPORTED/UNSUPPORTED/UNKNOWN、测试Evidence、错误/下一动作。
- **Create Fields:** connection name、实际支持的认证与必要tenant/org/project/region、凭据安全输入；自定义endpoint高级且校验。自动发现优先，受限手动ID仍需核验。
- **Edit Fields:** 别名、用途选择/继承、合法预算软限、授权；Context/能力/Provider limit只读。支持时才显示高级采样/Reasoning/output/timeout；不允许编造硬能力。
- **Actions:** 连接/断开、发现/刷新、测试当前用途（提示费用/外发）、选择Work explicit→Employee purpose→Company default、修复、查看fallback理由/Usage；不因测试chat成功提升其他能力。
- **Drill-down / Reverse Entry:** 当前连接/能力证据/限制/Usage→原Work/Conversation；Shared；Company OS §13/18、ADR-0046。已有Cloud接受不等完整G2-V通过。

### 4. Background / Exit / Continuation

- **Page Mission / Sections:** 用户知道UI关闭后是否工作，能明确停止并恢复；opt-in偏好、实际本机状态、受影响Work、停止/恢复说明。
- **Entry:** Settings运行/退出偏好；退出动作；原Work状态/必要CEO Desk异常；重开接回原历史。
- **Fields:** P: Company/原Work refs、返回位置；T: opt-in选择、关闭UI继续说明、Stop All & Quit意图、设备不可运行边界；C: 后台Enabled/Disabled配置、实际Work continues/Paused/Unavailable、最近活动/原因、待核验外部动作、恢复条件/下一步。
- **Create / Edit / Actions:** 不创建新runtime；显式开启/关闭偏好、关闭UI、停止全部并退出、重开、核验恢复。Disabled不承诺继续；Enabled不证明Running。
- **Drill-down / Reverse Entry:** 受影响Work/Evidence/权限修复→同Runtime/Work；Shared；Company OS §14/15。TARGET Option A accepted，CURRENT G3-V NOT RUN。sleep/off/shutdown/logout不伪在线。

### 5. External Effect / Approval / Recovery

- **Page Mission / Sections:** 查清外界发生什么再安全继续；原动作快照、Evidence、效果判断、合法恢复。
- **Entry:** Work失败/迟到回执/重启恢复、Publication、Result、CEO Desk真实待核验Matter。
- **Fields:** P: 同Work/Execution refs、动作、目标、账号、资源、输入版本、审批/授权ref、预算/权限范围；T: 有效期/条件、完成/重试判据；C: effect confirmed、effect unknown、verification required、safe retry、cannot replay、reason、Owner、receipt/source/time、Evidence refs、核验结果、当前权限、next action。
- **Create / Edit / Actions:** 追加核验记录、合法远端查询、人工证明、授权有效性复查、安全重试/停止/升级；只有明确经营Decision才P7。不得编辑原事实、用新Work或换Provider重发、因超时默认Retry。
- **Drill-down / Reverse Entry:** 快照→Evidence/远端来源→原Work/账号；Shared含Domain回执投影；Company OS §15、Content Growth §5.4。G4-V未验，不预设enum/表。

### 6. Backup / Restore

- **Page Mission / Sections:** 恢复公司资料与经营引用并安全接续；备份范围、完整性、影响预检、恢复、重连、Resume Check。
- **Entry:** Settings数据/存储/备份；故障恢复的合法入口。不是新Company初始化或Recovery Center。
- **Fields:** P: Company ref、备份来源/目标、Database/Managed Files范围、Manifest、版本、时间、排除项；T: 完整性/兼容要求、恢复影响、保全/回退条件；C: 实际文件/引用完整性、可用空间、preflight结果/失败原因、restore结果、Reconnect List、凭据/权限/能力状态、待核验Work/外部效果、Resume Check结果、next action。
- **Create Fields:** 合法目标位置与范围；不包括Credential/Cookie/Keychain Secret/Browser Profile。**Edit Fields:** 偏好/位置/范围，不修改备份来源事实；不提供未实现加密假开关。
- **Actions / Drill-down / Reverse:** 备份、查看范围/排除、预检、确认影响、恢复/失败保全、重连、核验原Work再继续→原公司现场。Shared；Company OS §17。完整G6-V未验，不以DB-only包证明恢复。

### 7. Professional Capability / External Result verification

- **Page Mission / Sections:** 员工用真正工作工具产出可验结果；合法输入/环境、动作、产物、验证/返回。
- **Entry:** Employee Workstation / Workspace专业Main；只读预览/Evidence可Utility；无需独立工具导航。
- **Fields:** P: Work/Assignment/scope、Capability/Provider ref、文件/仓库/数据源/素材ref、输入版本、结果合同；T: 输出目标/格式、只读或写授权、允许外发/预算；C: 有效能力/权限、cwd/仓库/分支事实（专业需要时）、dirty状态、实际进程/Preview地址、提取页范围/Partial/OCR置信限制、数据口径/窗口、产物ref、验证结果/Evidence、真实业务反馈source/time/manual/freshness/Unknown。
- **Create / Edit:** 选择合法资源/提出Work/输出需求；编辑工作输入需版本和权限核验，不改原Result。Actions: 读取/运行/取消/预览/测试/验证/引用/回Work；Git commit/push/破坏动作另授权。
- **Drill-down / Reverse:** 工具产物→Result/Evidence→原责任/Business Result；反馈无来源不推断，已读不等Accepted。Shared工具+Domain评估；Company OS §15–17、既有Result/P7。G5-V未验。

### 8. Content Growth Account Operating

- **Page Mission / Sections:** 经营已有Channel Account，持续目标/计划/产出/反馈/学习；不只是生产列表。
- **Entry:** Content Growth Workspace的当前账号对象/经营结果Surface；Business仅聚合方向与Workspace目录。
- **Fields:** P: Company/Business/Workspace refs、Channel、Account ref、合法binding、Goal、Strategy、Positioning/Audience、Cadence、Plan、负责Assignment、Intent ref、Platform Form约束、Account Context refs、Variant/version、Target/Eligibility、Publication ref；T: 批准边界、输出/评价合同、观察窗口、下一轮条件；C: 授权/能力状态、内容历史、逐账号提交/发布时间/receipt、效果判断、Analytics metric/unit/definition/value、source、collectedAt、freshness、真实0/Unknown/Not Collected/Unsupported/Connection Failed/Stale、Result/Evidence/Review/accepted Learning、Next Work或既有Cycle ref。
- **Create Fields:** 合法账号资产/绑定、目标/初始策略提案、责任范围；CEO不必填写完整行业配置。**Edit Fields:** Envelope内战术/计划；Goal/受保护策略/高影响承诺另Gate；历史回执不改写。
- **Actions:** 理解/研究、计划、生产Variant、核验/批准必要动作、发布/人工接续、读取数据、比较/Review、继续/调整/等待；不一键假群发成功。
- **Drill-down / Reverse:** Account→Intent/Variant→per-account Publication/Evidence→原Work/Account；可合法进入scoped Insights并返回。Domain；Content Growth §1–5.4＋Shared §10–15。
- **Scope / Implementation:** Account是长期经营对象，不是Workspace或execution scope；Provider不是Employee；具体发布/Analytics与AiToEarn接入不因文档通过而Verified。

### 9. Settings与原对象合同的增量

Company字段只补真实预算/经营时区/用途默认/政策与恢复入口；Employee字段只补用途继承、能力证据/有效权限/多Assignment投影；Workspace字段只补相关专业能力、资源、计划/恢复引用。所有对象仍是原canonical identity，不能复制Company/Employee/Usage。

按Personal / Company / Employee / Workspace / Provider-Connection / Capability Advanced / System-Runtime分Owner，不改既有Settings IA。普通选择与自动只读事实分开；Advanced仅支持的参数，进程owner/lease/锁与协议schema不进普通产品字段。研究77项已按责任归并到Company OS §18，不要求用户配置77项。信息职责不等固定Card/Tab/Drawer；无正式交互确认处为DESIGN OPEN。



## 2026-09-10 — Pre-Design-Research Product Structure Baseline

Authority Class: CURRENT / PRODUCT STRUCTURE AUTHORITY. Status: Frozen. Disposition: RECORDED / CURRENT — INCLUDED IN CONTROLLED BASELINE PROMOTION.

本文件与 [CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md) 共同作为设计研究前结构输入；基线只收敛已接受的产品结构，不新增 Product Truth、Runtime primitive 或视觉方案。七个一级产品区、Company → Department → Business → Workspace、原装组织、Employee/责任关系、Four-Pane 与 global CEO Assistant 等结构保持当前语义；FINAL UI MASTER: **PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**，Figma 仅为结构/IA参考，非最终视觉权威。

## 2026-09-09 Phase A.1 — Curis 原装公司经营组织

Authority Class: CURRENT / FROZEN. Disposition: CEO CURRENT DECISION REGISTERED.
依据 [Authority Repair · Phase A.1](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)；仅替代本文件“仅默认部门/员工人数全部未定”的旧边界，其他Phase A与Frozen规则保留。

空间工程部、数据分析部是 **CURIS BUILT-IN COMPANY OPERATING DEPARTMENT / Curis 原装经营部门**，共同属于 **CURIS BUILT-IN COMPANY OPERATING ORGANIZATION**，不是用户Business/Template/Package/Demo。自动物化是实现方式，不是产品身份。
新Company必须有Company/CEO/same Assistant、两原装部门、对应canonical Employee实例、Role/Responsibility/Assignment和合法工作面关系；用户Business可0。没有Provider/Key也创建组织和员工，真实显示需配置/暂不可执行，不伪造绑定。

空间工程六类职责（Leader、行业研究、经营方法/设计翻译、产品/空间设计、搭建、Quality/反馈）从Shared §9.4/Methodology §9恢复；后续可合法兼任/调整Holder，但不能用一人兼任代替fresh六实例。**CEO ROLE DECOMPOSITION已裁决：freshCompany为6个Official Definitions / 6个不同canonical Employee实例，岗位为空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家**，不得将原型高建/研真/方法/小录/实施/QA当官方员工定义；未恢复“牧人”可定位Authority。
数据分析部**至少1 canonical Company Analyst / 公司经营分析师**，主要工作面为Operating Intelligence。产品称谓“司衡”有历史Blueprint/Accepted来源，可编辑，不是匹配员工的键；UI同名fixture不是实例证据。分析师归属必须由canonical Role/Responsibility/Assignment证明。Business0仍有分析师，诚实说明暂无业务/足够数据。

Official Definition（岗位/责任/推荐能力来源）→ Company Employee Instance（唯一运行真源）→ Assignment/Current Holder（三者不同）。不新增员工系统/表，不将Definition ID永久绑定责任。原装与用户员工共用Detail/Edit、身份/头像/Conversation/能力模型，按现有字段编辑；责任Requirement持续，Holder可合法替换，历史Work/Result不改写。缺Holder展示组织能力缺口。
Organization显示原装团队而非空部门；Talent是扩充，不把已有原装员工当待招聘。空间工程在新业务意图前已存在；模型未配是执行缺口，不要求用户先建团队。
Employee Profile作为官方示范应覆盖身份/Department/Role/职责/服务范围/Work Surface/能力/模型状态/工作/结果/Conversation/可编辑配置；仍Main Workstation+Utility detail，不把Conversation塞入Utility。不得默认暴露runtime refs/JSON。

技术definition ID映射由Phase B先审计复用templates/catalog；若需新canonical Definition primitive/schema则Architecture Review，不能直接建表。人数/岗位拆分已由CEO正式裁决，不再作为Gate；实例姓名可编辑，不能成为identity key。

## 2026-09-09 Phase A — Current expansion repair

Authority Class: CURRENT / FROZEN. Disposition: ACCEPTED.
依据Blueprint本日修订与[Authority Repair](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)，本节限定下文旧段适用范围，不创建新母版。

新Company具有Company/CEO/same Assistant/空间工程部/数据分析部；业务可空。Organization/Business Space必须提供经营意图启用/选择，读Company→reuse/propose→必要Gate→canonical Department/Business+atomic firstWorkspace→合法Team/Leader责任；不是模板/Studio技术配置。两支持部门不是Business；研发/内容增长仅用户真实启用。
Business是持续经营身份，Workspace是其工作环境。Generic合法经营；Professional非所有长期Workspace强制前置。旧“一个账号通常一个Workspace”只保留历史平台实例参考，不适用于Current Content Growth：Channel/Account≠Workspace。
旧Assignment Conversation Continuity隔离解释仅指消息/引用scope：可保持同Conversation跨Assignment与多topic，历史不能被新scope重写或越权读取。
对象空间映射遵循Shell本日修订；七区不变、Conversation quick access与floating Assistant不是第八区。Company Analyst须canonical责任/Assignment证明，业务服务不改变数据分析部职能身份。
下文旧Knowledge及Meeting/App Entry待实现说明为历史checkpoint，具体已验收功能见Current State/accepted reviews，不得整体恢复为“未实现”；外部连接器与其他未验收边界保留。
Legacy intended routes和Studio降级以Authority Repair §9为准；不授权删除路由。

Authority Class: CURRENT
Status: Frozen
Disposition: CURIS PRODUCT TRUTH — FINAL ACCEPTED / FROZEN
日期：2026-08-20
复审修订：2026-08-22 · Professional Workspace Strategy / Verified-first resolution authority reconciliation；在原文件原位升级，不创建并列 Product Structure Map
定位：Curis 的产品母版，不是页面清单、Runtime 设计或技术实现方案。
历史推导（非默认必读）：[Curis_Product_Rethink_Reasoning.md](/Users/yy/Documents/Curis%20AI%20Workspace/Curis_Product_Rethink_Reasoning.md)

本文件在前述产品重新推导基础上继续收敛，不推翻其核心判断。v3.2 是同一 canonical 文件的结构化展开升级；本轮补入 Professional Workspace multi-Surface、Team × Surface、Domain Navigation、Package 声明责任与 Verified-first resolution，Product Blueprint 仍是唯一产品权威：

> Curis 是一款把成熟 AI 工作能力组装成一家公司，并让普通用户能够统一使用、管理、扩张和进化这家公司的 Desktop App。

**Canonical Business Spine（CEO Accepted 2026-08-20）：** Business 是唯一可持续引用的业务身份；必须归属 Department，并至少拥有一个 Workspace。`business_directions` 只承载 Business 下 Strategy / Direction supporting truth，Project 只作为 legacy compatibility object；Workspace 不得使用 free-form Business relation。Business + First Workspace 采用原子创建，无法解析的 legacy Workspace 进入 `UNRESOLVED → QUARANTINED`。本段定义 Product Truth；实现状态、迁移证据与 Frontend promotion 只见 CURRENT_STATE、Issue 与 Review。

本轮正式补充页面、字段、动作、Create/Add、Drill-down、Reverse Entry、Shared/Domain 和 Source Authority 契约；不修改 Runtime、数据库或业务代码。

本次自审进一步检查了“结构简洁是否误删用户需要的能力”，并补齐 Desktop 壳层、首次打开状态、CEO 注意力排序、对象入口归属和最小完整闭环。结论是：核心能力覆盖没有被删掉，但设置、运行关注、通知审批、资源健康、帮助与数据管理不应继续占据主工作区；它们应通过上下文入口和左下角用户头像菜单可达。

本轮不新增无必要的系统对象或生命周期；正式一级产品名称为“人才与能力”，内部以 Market / Discover 等 Surface 承担外部能力发现。“专家团队”和“岗位能力包”仍是 Workspace / Employee 配置的产品表达与组合视图。经营洞察 / Operating Intelligence 已确认成为第七个一级产品空间；底层继续使用既有 RoleSlot、Handoff、Cycle、Capability 和结果契约。2026-08-19 新增的 Leadership / Responsibility Assignment / Operating Loop 只收敛产品语义，未授权 Runtime、Schema 或代码实现。

### Autonomous Business Operation（CEO Accepted / Approved Candidate · 未实现）

经营责任默认持续，但每个 Operating Cycle 都是 bounded 并必须 Close。Cycle Close 不表示 Business、Workspace 或 Operating Responsibility 停止；`PAUSE` 暂停 Operating Series 并要求显式 Resume，`STOP` 才终止当前 Operating Responsibility / Goal Series，且只能由 CEO 或事先明确授权的 terminal policy 触发。没有 Work、一次失败、一次 Review 或一次 Cycle terminal 均不得自动 STOP 整个责任。

Leader 只能在 **Approved Strategy Envelope** 内自主调整 hypothesis、tactic、cadence、experiment、resource allocation、Work priority、content / execution mix 与 bounded Plan，且必须满足 Evaluation Contract 与 Evidence / Review。Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget 及 high-impact / irreversible external commitment 的改变必须经过 CEO Gate；`ADJUST` 不代表 Leader 可修改任意 Strategy。

`CONTINUE / ADJUST` 才能创建或安排 exactly one next Cycle；`WAIT / ESCALATE` 只保持可恢复等待，不创建未授权运行。V1 跨域证明分为：至少一个真实 Domain 连续 ≥2 个 Cycle 的 **Primary Autonomous E2E**，以及第二个 Domain 的 **Cross-domain Contract Proof**；不得以 fake Result、fake Analytics 或 static UI 冒充 Autonomous E2E。该候选合同不代表 Runtime 已实现或接受，且必须使用 canonical `Company → Department → Business → Workspace` identity。

**Bootstrap 产品规则（CEO Accepted Surface Mapping）：** Bootstrap 默认接受模糊或不完整的 CEO 经营意图；不得要求 CEO 先填写 Positioning、Strategy、Team、Workflow、Workspace Structure 或 Operating Plan。缺失信息先经过 `Curis Research → Situation Understanding → Strategy Proposal`，CEO Gate 只处理系统不能合理代理的 Goal、Strategy Boundary、Risk、Constraint 与 High-impact Decision。Bootstrap 不得实现为复杂的“新建业务配置表单”。

**Workspace Current Operating 产品规则（CEO Accepted Surface Mapping）：** Current Operating 默认只呈现 `经营状态 → 本轮重点 → 最新判断 → 下一步`。进展优先由当前相关 Professional Surface 表达，只有当前面无法表达时才补充；需要关注仅在存在真实 Need / Risk / CEO Gate 时显示。该摘要保持轻量，不成为经营 Dashboard。

### Professional Workspace / Multi-Surface（CEO Accepted 2026-08-21；Content Growth Decision Reconciliation 2026-08-24）

Workspace 是由真实 Operating Team 持续承担业务责任的完整专业经营环境，不是 Page。一个 Workspace 可包含多个 Professional Surface；Surface 围绕一类稳定专业问题组织对象、动作、工具与相关经营 Truth，但不拥有 Team、Employee、Workspace Leader、Work lifecycle、Result/Evidence truth、Cycle 或 Runtime。切换 Surface / Object View / Detail / Utility / Filter 不改变 Workspace identity，不创建 Sub-Workspace 或其他 canonical identity。

一个长期 Workspace 只有一套 canonical accountable Operating Team responsibility boundary，但 Team 不是固定人数或排他成员集合。Employee、Assignment、Team membership 和临时协作者可以变化；同一 Employee 可通过不同 Assignment 承担多个 Responsibility 并跨多个 Surface 工作，identity 不复制。Surface 只声明 Responsibility Requirement（WHAT）；Organization Routing 解析 WHO；Workspace-scoped Assignment 承载 Holder / verified Executor；Capability 决定 HOW。Surface / Package 不得绑定 `employee_id`。

Workspace-local Domain Navigation 由真实 Domain semantics 形成并由 Workspace Package 声明；Core 只负责 validate / resolve / render，不写死 XHS、RD、电商菜单。Context 承载 Workspace identity、Domain Navigation 和 current Surface context；Main 承载 selected Professional Surface 与 relevant Shared Work Area；Utility 承载按需 Detail / Editor / Preview / Evidence / Tool。Four-Pane 是职责模型，不是固定四列；Operating Overview 只是可能的 default Surface，Main 不固定等于 Overview。Content Growth 当前是 Professional Workspace Candidate（不是 Verified）；其默认 selected Surface / projection 为 CEO Operating Result / 经营结果面。XHS / Douyin / TikTok / YouTube / Bilibili 等是 Channel，具体账号是 Channel Account；Channel ≠ Workspace，Channel ≠ Channel Account。

Team、Knowledge、Artifact、Result、Evidence 与 Employee Workstation 继续使用 Company OS / shared truth 的 Workspace-scoped projection。一个 Cycle 可跨多个 Surface，产品模型允许多个 sequential / parallel Work；Surface 切换不控制执行，Handoff 只在 acknowledged accountability transfer 时成立。Multi-Surface Workspace Package v2 foundation 与 sequential cross-professional multi-Work runtime proof 已 `IMPLEMENTED / ACCEPTED / COMMITTED`；parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping 与最终 Professional integration 仍是 Product → Implementation Gap。

### Professional Workspace Strategy（CEO Accepted 2026-08-22）

Curis 优先提供少而深、经过专业研究与真实验证的 Professional Workspace；相近业务优先通过 Instance Configuration、Maintained Derived 或 Safe Composition 适配。没有成熟专业环境时，Generic Workspace 仍是可真实经营、可恢复、缺口透明且尽量可升级的起点。Curis 不承诺任何业务一句话自动生成专业级软件。

#### Resolution order

```text
Business Intent
→ Read Current Company Truth
→ Recognize Domain / Scope / Risk
→ Search Verified Match
→ Instance Configuration
→ Maintained Derived
→ Safe Composition
→ 判断 Domain Truth 是否足够支持 Generic
→ 必要时插入 bounded Domain / Risk Research
→ Generic / Derived / Composed / Professional Candidate 判断
→ Generation only when necessary
```

Research 按 Truth / Domain / Risk Gap 按需插入，Generation 是 last resort；成熟 Package / Template 可以复用适用版本的研究、设计、能力和验证证据，但 Professional、Official、Verified 与 Generated 不得互相替代。

#### Product form / provenance / assurance

| 轴 | 允许值 | 语义 |
|---|---|---|
| Product Form | `Professional` / `Generic` | Professional 是稳定 Domain / Operating Problem 的专业业务应用；Generic 是 Company OS 通用经营底座上的真实工作环境，适合未知、长尾、临时或专业包缺失场景 |
| Provenance | `Curis Official` / `Partner` / `Community` / `User or AI Generated` | 说明来源与维护关系，不说明质量已验证 |
| Assurance | `Verified` / `Candidate` / `Unverified` / `Deprecated` | 说明版本、范围、证据、连接、已知缺口与支持状态 |

Professional ≠ Verified；Official ≠ Verified；Generated 默认只能是 Candidate；组合后的 Workspace 必须重新验证。Verified 记录至少绑定 version、scope、evidence、maintainer、required connections、provider boundaries、known gaps 与 migration/support policy。本轮不授予 XHS 或 RD Verified Professional Workspace 状态。

#### Business Configuration 与 Workspace 边界

Business 页面继续是通用的 Business Configuration：身份 / 定位、Goal、Rules / Preferences、Team / Responsibility coverage、Capability / Connector 选择与授权、automation boundary、optional module、通知与 operating cadence 等。它回答“这个业务怎么经营”，不要求普通用户设计 Professional IA、Navigation、Handoff、DAG、Router、行业 Evaluation 或 Value semantics，也不是 Workspace Builder / Low-code App Builder / Workflow Builder。Professional Workspace 回答“这个专业业务具体怎么工作”。

#### Workspace Engineering / Package direction

Workspace Engineering 负责理解意图、读取 Company Truth、识别 Domain / Scope / Risk、发现 Verified Match、配置 / 派生 / 组合、解析 Team / Responsibility / Capability / Connection、安装验证、监测缺口与版本兼容、持续演进；它不再被定义为默认从零生成器。Workspace Package 的产品语义是 Domain Operating Capability Package；Professional UX / Interaction（Surface、View、Detail、Editor、Tool、对象/动作投影与可用性声明）属于 Package 一等资产，但继续使用受限、可验证的声明式 registry，不授权 arbitrary HTML / React / JS。Generic / Generated 应尽量 identity-preserving upgrade 到 Professional / Verified；不能安全原地升级时使用 sibling Workspace + controlled Handoff，不静默重建。Official Professional Workspace Library、Professional Module、Verified Registry 与第三方 Package ecosystem 均为后续架构方向，不是本轮实现。

### Three-Layer Operating Model（CEO Accepted 2026-08-20）

Current Product Truth 采用三层边界：`User Surface → Employee Operating Layer → System Runtime`。用户表面承载“把这件事交给 Curis”、公司/业务/Workspace、Leader Conversation、Decision、Result/Evidence 与下一步；员工经营层消费 Goal、Strategy Envelope、Situation、Capability、Method / Package、Knowledge、Plan、Result、Review、Learning；System Runtime 仅负责责任、Scope、权限、版本、证据、持久化与恢复。固定的是经营责任 / Truth / Evidence / Gate / Recovery Contract，不是所有业务共用的固定箭头。

未知业务在同一模型内按 `USE EXISTING → COMPOSE EXISTING → RESEARCH / ADAPT → BUILD / ACQUIRE → ESCALATE → REFUSE / CANNOT OPERATE YET` 选择路径；目录可见不等于已验证可运行。XHS、小红书、抖音、RD、宠物寄养仅为 Validation / Pressure-test Examples，不进入 Core 或默认模板。

不新增 Playbook canonical object。Methodology Handoff、Package method metadata、Skill composition、Operating Definition、Result / Evaluation / Review 共同承载专业经营方法。Package 的产品语义正式为 **Domain Operating Capability Package**，其方法元数据持久化与版本化仍登记为 Future Capability Architecture / Product → Implementation Gap，不改变 Autonomous V1 或现有 Runtime。

### Brand Neutrality（CEO Accepted 2026-08-20）

`Curis` 只属于 Brand Identity。Company OS、Company、Department、Business、Workspace、Leader、Employee、Responsibility、Capability、Package、Skill、Operating Definition、Operating Lifecycle 属于品牌中立的 Product Semantic Identity；`company_id`、`business_id`、`workspace_id`、`employee_id`、`assignment_id`、`work_id`、`result_id`、`evidence_id`、`decision_id`、`cycle_id` 与 Package identity/version refs 属于稳定 Runtime / Persistent Identity。用户语言仍可使用“交给 Curis”；品牌重塑不得重建业务归属、Workspace、历史结果或证据引用。技术 namespace 不因本原则批量改名，未来统一 Brand Configuration 另走实现方向。

> **Current Truth 边界：** 本文件从第一行到最后一行只表达当前 v3.2 产品合同；Runtime / Internal 关系仅作为实现支撑，并必须与 Product Organization Map 分层阅读。唯一 Product Blueprint v5.6 与 UI Blueprint 共同消费本文件，但不由本文件反向创造产品规则。本轮 Professional Workspace Strategy、multi-Surface 与 Team × Surface 语义已由 CEO 接受；Multi-Surface Workspace Package v2 foundation 与 sequential cross-professional multi-Work proof 已由既有 commits 接受；parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping、Verified Registry 与 RD/XHS migration 仍需独立验收。

---

## CURRENT v3.2 CONTRACT — 先读

本节是当前产品阅读入口，也是本文件后续字段、页面和动作合同的共同语义基线；它不新增 Runtime Primitive，也不把内部对象当作普通用户导航。

### 当前产品组织图

```text
Company
├── Department（可渐进形成；长期 Business 必须归属）
│   └── Business
│       ├── Business Definition / Rules
│       └── Workspace（至少一个；一个 Business 只有一个 Workspace 也正常）
│           ├── Shared Workspace Shell
│           ├── Domain Navigation → selected Professional Surface
│           ├── Team Operating / Default Flow
│           └── Responsibility Assignment / Employee Workstations
└── 员工目录（从员工反查 Responsibility Assignment / Role / Workspace / Business / Department）
```

公司版图默认展示 Company → Department → Business → Workspace → Role → Responsibility Assignment → Employee，优先让 CEO 看见业务数量、扩张、空岗、风险和最近结果；Business 点击进入 Business Work Surface / Business Definition，Workspace 按需展开，Role 展开后才看责任分配和员工。Business Space 是 Operating Work Directory，默认提供 [部门] / [业务] / [工作空间] 三种直接入口，并允许直接进入具体 Workspace；对象层级不等于导航层级。

### Business × Workspace 产品关系（CEO Correction）

```text
Company
└── Department
    └── Business（持续经营身份 / 方向 / Workspace组合）
        ├── Workspace（独立经营）
        ├── Workspace（独立经营）
        └── Workspace（独立经营）
```

Business 负责表达业务类别、Department、整体方向/目标、Business Introduction、Business-level Rules / Configuration、Workspace Directory、整体结果、整体人员/资源和整体风险；每个 Business 至少拥有一个 Workspace。Workspace 是独立运行的经营单元与专业工作环境，拥有自己的 External Account / Operating Object、Goal、Positioning、Audience、Rules / Configuration、Strategy、Team Operating、Role/Staffing、Employee Assignment、Model/Agent、Skill/Capability、Connector、Knowledge、Schedule、Current Work、Result、Analytics、Risk 与 History。每个长期 Workspace 都由 Operating Team（Leader、成员、明确职责）承载；同一 Business 可以聚合多个独立 Workspace，不要求共享同一 Team。Account 是 Workspace 服务或经营的外部对象，不是全局层级，也不自动等同 Workspace。一个 Workspace 服务一个或多个 Account、或同一 Business 以多个 Workspace 分别经营 Account，均由 Domain Operating Model 决定，不建立全局一对一规则。Business 只共享 Business-level 语义，不规定所有 Workspace 使用同一个 Team Operating。

同一 Business 下的 Workspace 默认互相独立；可复用已验证方法和配置，但不默认共享 Workspace-level Goal、Positioning、Strategy、员工、模型、Skill、Knowledge、Credential、Schedule、Result 或 Analytics。它们仍共同服务所属 Business-level Goal / Strategy。不采用 Business Default → Account Override；是否由一个 Workspace 服务多个 Account，按对应 Domain Operating Model 明确判断。

默认 Company Support Organization（Department 例外）：Department 通常按需、随重复责任和共享能力渐进形成；每个新 Company 默认拥有「空间工程部」与「数据分析部」两个 System-default Company Support Department。它们不是 Business，也不要求用户先配置完整组织。空间工程部负责业务空间建设与维护；数据分析部承载 Company Analyst。Business Analyst 默认可由数据分析部 Employee 通过 Assignment / Allocation 支持具体 Business，成熟 Business 也可创建自己的分析 Role / Employee。Employee 的 Functional Affiliation 与 Business Assignment / Allocation 必须分开表达。

一级产品：**CEO 工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议**。设置进入左下角头像；CEO Assistant、搜索、最近工作、通知/待处理是全局能力，不占一级导航。对话保持独立工作 Surface，不重复建立聊天或任务系统。

### Operating Work Directory 与领导工作面

业务空间 = **Operating Work Directory**，不是 Business 列表或统一 Runtime 控制台。它在同一 Company Truth 上提供三个直接入口：

```text
[部门]       → Department Work Surface
[业务]       → Business Work Surface
[工作空间]   → Professional Workspace
```

Department Work Surface 是 Department Leader 的责任与协调工作面；Business Work Surface 是 Business Leader 的 Business-level Goal / Strategy、Workspace Directory / Portfolio 与业务级决定工作面，不嵌入 Workspace 细节；Professional Workspace 是独立的专业工作环境与员工工位，采用 Shared Workspace Shell + Workspace-local Domain Navigation + one or more Professional Surfaces + Shared Team Operating + Shared Employee Work Area。Workspace 不默认共享彼此的 Workspace-level Goal / Positioning / Strategy，但都属于并服务于所属 Business，受 Business-level Goal / Strategy 的整体方向约束；不创建 Default → Override 技术模型。Leader 不是新的 Employee 类型：Department / Business / Workspace Leader 都是带有相应 Responsibility Scope 的普通 Employee，使用同一 Employee Workstation。正常专业工作在最低有效责任范围完成，只有跨范围、资源/策略冲突、无法解决或高风险/不可逆问题才逐级上移：`Role / Employee → Workspace → Business → Department → Company / CEO`。

### Leadership / Responsibility Assignment（当前产品语义）

Leader 是 Curis system-defined 的责任角色，不是 Employee Type，也不等同于 Admin 或技术权限。三层 Leader 均由普通 Employee 承担：

- **Department Leader**：对 Department Goal、所辖 Business 的整体状态、跨 Business 资源/问题协调和必要的 CEO 升级负责。
- **Business Leader**：对 Business Definition、Business-level Goal / Strategy、Rules、Workspace 集合、业务级结果和 Workspace 协调负责。
- **Workspace Leader / Operating Owner**：对 Workspace Goal、Rules、团队运转、团队协作、Current Progress / Problem / Result 负责；一轮工作结束后必须判断下一步，而不是让 Workspace 因一轮工作完成而停工。

运行中的责任必须落到 `Role Definition → Responsibility → Employee Binding → Responsibility Assignment`。Assignment 的最小产品语义是 `Employee × Role × Scope`；同一 Employee 可以拥有多个普通 Role、多个 Leadership Role、跨 Business / Workspace 的多个 Assignment，Employee Identity 不复制。页面上的“负责人”必须投影真实 Leadership Assignment，团队运转步骤中的 Employee 必须投影真实 Role Assignment。

### Assignment-scoped Conversation 与 Context Isolation

工作和角色对话默认路由到 Responsibility Assignment，而非裸 Employee。Employee Profile 可保留 Employee Identity Conversation，用于整体能力、负荷、Model / Skill / Tool / Knowledge、权限、表现与成长；从 Business Leader、Workspace Leader 或 Workflow Role 进入的 Conversation 必须携带 `Employee Identity + Role + Scope`，按消息/引用隔离同Employee的其他Assignment Context，校验当前授权；同一Conversation可跨Assignment持续，不强制复制或切断。允许读取完成当前责任所需的 Company Truth，但不得因为身份相同而混入其他 Scope 的完整历史。

### Team Operating / Default Flow → Result → Leader → Next Operating Cycle

Team Operating 的产品语言是“团队运转”，其中“默认流程”表达责任协作。`A → B` 表示 A 产出 accepted Result 且没有更强的 Consult、Review、Return、Need、Leader、Decision、Wait 或 Domain rule 时，B 是默认下一 Responsibility；箭头不是强制运行序列，也不是任意可执行 DAG 边。团队编辑动作映射为 Reorder→Default Flow、Responsibility→Responsibility Contract、Employee Binding→scoped Assignment、Input→Context Contract、Output→Result Contract、Save→immutable Operating Definition Version；运行中的工作保持 pinned 旧版本。它不是完整 Operating Loop，也不包含 Model、Skill、Tool、Knowledge、Permission 或 Execution 状态。Result 必须回写 Workspace Current Truth，并回到 Workspace Leader 的责任范围；Workspace Leader / Operating System 根据 Goal、Rules、Current Truth、Result / Problem 与外部新输入选择 `Continue Next Work`、调整团队运转/规则/Staffing、升级或等待新目标；正常经营可自动进入下一轮，CEO 只在结果偏离、判断、异常、规则/人员调整、跨 Scope 或高风险事项介入。

Operating Escalation 采用 `Employee → Workspace Leader → Business Leader → Department Leader → CEO`，但责任停留在能够解决问题的最低有效范围；Organizational Authority 不自动授予 System Permission。

Organization Center 只负责公司结构与行政真相（Company Map + Employee Directory、Department / Business / Role / Staffing / Leader assignment）；Leader 的持续 Conversation、Handoff、Exception、Decision Request 与 Follow-up 在 Business Space 的对应 Work Surface 中承载。两者共享同一 Truth，不复制组织数据或工作记录。

人才与能力内部包含 `[专家] [技能] [连接器]`。专家不是员工；专家经招募、公司身份、岗位/职责、必要关系与授权后才成为 Employee。Department 不是招聘前置。Skill 以职业能力组合 / 岗位能力包进入招聘与员工配置；Connector 的授权与维护进入设置。

### Business Duplication

Duplicate Workspace 与 Duplicate Business 是两个不同动作。Duplicate Workspace 在同一 Business 下创建新的独立 Workspace，复用 Workspace IA、专业界面、团队运转、Role / Responsibility Structure、Model / Agent、Skill / Capability、Automation 和业务方法；必须重新确认 Workspace Name、External Account、Goal、Positioning、Audience、Strategy、Employee Binding、Knowledge、Credential / Permission、Schedule；禁止复制 Workspace Identity、Employee Identity、Secret、Conversation / Execution / Result / Evidence / External Receipt / Audit History / Current Runtime State。Duplicate Business 创建新的 Business Identity，复用已验证 Business Definition / Rules 与经营方法，但不复制统一团队运转 / Role / Employee Binding 母模型；必须重新确认 Business Name、Goal、定位、外部对象、Staffing 和排期；同样不复制身份、秘密、历史、结果、审计或当前运行状态。两种动作都必须先显示 Copy Preview（复用 / 重新配置 / 不复制），并回到同一 Company Truth，不复制第二套组织数据。

### Business Exit Lifecycle（跨层产品合同）

Business Work Surface / Business Management Actions 必须支持 `Pause`、`Reduce`、`Transfer`、`Close`、`Merge`、`Split`。退出或调整前先展示未完成责任、Commitment 保护、责任接收人和 Employee / Capability / Capacity 的释放或重新分配；完成后保留 Workspace 状态、History、Evidence、Result、Learning 与外部承诺记录。它不是独立导航，也不新增 Runtime Primitive；具体动作继续消费既有状态、责任、结果与审计契约。

### CEO Operating Day Cross-day Continuity（跨层产品合同）

CEO 工作台以连续经营日承接 `Brief → Matters → Handoff → Decision → Exception → Evidence → Learning → Closeout`。Day N 未完成责任、未决 Decision、Exception、Risk、Follow-up 和需要 CEO 继续关注的事项必须自然进入 Day N+1；重新打开 App 不应清空经营上下文。该合同不创建 OperatingDay 页面或 Runtime Primitive，落在 CEO Desk、Assistant、Business、Meeting 与结果回流的既有入口中。

### Workspace 产品语义

> **Workspace = 专家团队 + 专业工作环境 + 自动协作方式。**

Workspace 是业务内可自由装配、可采用不同成熟产品工作方式的独立专业空间，不是统一 Runtime / Workflow 页面，也是当前唯一 canonical user/product identity。历史 Office / “办公室”仅保留为 domain、implementation、migration provenance，不与 Workspace 建立产品等式。员工可加入多个合理 Workspace，但不复制身份；招聘（外部专家 → 公司员工）与组队（已有员工 → Workspace 团队）严格分开。研发可参考 Codex / Claude Code，内容等领域采用各自专业界面；页面责任由 Workspace 自己定义。

### 经营洞察 / Operating Intelligence 产品空间

**Page Mission：**消费 Company 已有的 Truth、Result、Usage、Cost、Execution、Feedback、Review 等事实，帮助 CEO 深度查看趋势、比较差异、解释归因并评估经营；不创建第二套 Truth、Result 或 Analytics Runtime，也不取代 CEO 工作台。

**边界：**CEO 工作台负责注意力、异常、简报、结果、待处理和下一决定；经营洞察负责深度查看、趋势、比较、归因和经营评估。经营洞察不是首页 Dashboard，也不生成没有真实来源的健康分数。

**Entry / Return：**CEO Desk、Business、Workspace、Employee Profile、Organization / Company Map、CEO Assistant 均可带当前对象与范围进入 scoped Insights；完成查看、比较、注释或手动回填后返回原业务、Workspace、员工或公司版图上下文，不建立孤立分析入口。

**Sections：**公司经营、业务分析、组织与员工、模型与能力、分析报告、专项研究；每个范围内提供周期筛选、经营指标摘要、趋势、比较、归因、运行与使用、成本、人与质量、外部业务结果、来源 / 新鲜度 / 未知 / 手动回填、下钻与返回。

**Fields（逐字段）：**`scopeType`（Company / Business / Workspace / Employee / Team / Model / Agent / Provider / Capability）、`scopeId`、`period`、`metricId`、`metricName`、`value`、`unit`、`source`、`freshness`、`collectionMode`（automatic / manually_entered / unknown）、`unknownReason`、`employeeId`、`teamId`、`modelId`、`agentId`、`providerId`、`capabilityId`、`executionRef`、`resultRef`、`reviewRef`、`acceptanceRef`、`externalResultRef`、`comparisonSet`、`annotation`。

**指标合同：**execution duration；token / usage；estimated / actual cost（只有真实来源时）；task / result volume；failure / retry；human intervention；review / rework；CEO acceptance；result quality / business feedback；external business metrics；trend / comparison。每个指标必须显示来源、新鲜度与采集方式；不可采集时显示未知或 CEO 手动录入，并保留回填来源。

**Actions：**切换范围、调整时间与筛选、查看趋势、创建比较、选择语义兼容的图表表达、打开来源、下钻到原始运行 / 结果 / Review / 外部回执、添加带来源的人工记录、保存视图（若权限允许）、返回来源上下文。比较同一员工或同类工作使用不同 Model / Agent 时，必须同时关联运行时长、使用量、Failure / Retry、Human Intervention、Review / Rework、Result Quality、CEO Acceptance 与 External Business Result，显示 Sample Size / Comparability / Evidence，禁止无依据的单一最佳模型排行榜。

**Drill-down / Reverse Entry：**Company → Department → Business → Workspace → Employee / Team → Execution / Result / Review / External Result；任何来源对象均可反向打开对应 scoped Insights。**Shared / Domain / Mixed：**分析壳层、筛选、来源和比较为 Shared；业务指标、结果质量和外部结果由 Business / Workspace Domain 提供；不新增运行时事实源。**Source Authority：**Product Blueprint、既有 Company Truth / Result / Usage / Feedback / Review 契约与本 Master Map 当前合同。

**Analyst / Report 工作回路：**Business Runtime / External Data → Business Analyst → Business Report；Company OS / Metric Truth → Company Analyst → Company Analysis → CEO。Report 是 AI Employee 的正式工作成果，字段至少包括 `scope`、`period`、`responsibility`、`authorEmployee`、`department`、`business`、`trigger`、`dataSources`、`modelAgentProvenance`、`createdAt`、`review`；正文分为 `FACT`、`INTERPRETATION`、`UNKNOWN`、`RECOMMENDATION`、`EVIDENCE`。CEO 追问进入现有 Conversation Surface，形成 Analysis Task 与新报告；Second Analyst Review 必须同时满足独立性与相关分析能力。Business Analyst 的解释不得自动升级为 Company Fact。

**Visualization / Data Trust：**Trend 使用 Line（可切换兼容 Bar / Table）；Comparison 使用 Sorted Bar / Small Multiples（可切换 Scatter / Table）；Composition 使用 Stacked / Donut / Table；Workflow 使用 Funnel；Organization 使用 Capacity / Load；内容趋势可使用 Heatmap 或业务定义的关系图。图表只改变 Presentation，不改变 Dataset / Metric Truth。每个视图保留 `source`、`freshness`、`verified`、`manual`、`unknown`、`stale`、`missing`、`external` 语义；External 未连接显示“待连接 / 无数据”，不显示 0。没有 Calculation / Threshold / Evaluation Contract，不生成健康、优秀、饱和、过载或综合评分。

### 资料库 / Company Reference Space 产品登记（2026-09-01）

资料库是用户可见的 Company Reference Space：Overview、Browse/Search、Reading / Reference Detail、Select Reference From Work、Used By Work / Result。正式范围语言为“适用范围 / 使用范围”（Company → Business → Workspace），并保持 Source、Knowledge/Reference、Context、Evidence、Result 的边界；复用既有资料真源，不建立第二套 Knowledge、Citation 或 Context 存储。资料库与 Work、Library、Result 之间保持可追溯使用关系；具体视觉仍待 `KNOWLEDGE LIBRARY DIRECTION D VISUAL CLOSURE`，当前实现仍为 bounded manual / `.md`、`.txt` 导入与有限搜索，Business/Workspace 作用域、引用、新鲜度/版本、反向 Work/Result、外部连接、细粒度权限和 packaged restart 仍是 Product → Implementation Gaps。历史 Project / Department 作用域仅保留 implementation / migration provenance，不作为当前产品范围语言。

### 当前对象字段合同

| 对象 | Page Mission | Entry | Sections | Fields（逐字段） | Actions | Create Fields | Edit Fields | Drill-down | Reverse Entry | Shared / Domain / Mixed | Source Authority |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Company | 看清公司身份与经营边界 | CEO 工作台 / 公司版图 | 身份、意图、状态、关键结果 | `id`、名称、使命、经营意图、CEO、状态、时区、成立时间 | 查看、编辑、进入版图 | 名称、使命、意图、时区 | 名称、使命、意图、时区 | 部门、业务、员工、资料、会议 | 头像菜单、Assistant、业务详情 | Shared | Product Blueprint / Company OS |
| Department | 表达已形成的责任分组 | 公司版图 | 责任、业务、岗位、风险、Department Leader Workstation 摘要 | `id`、名称、职责、状态、业务数、岗位数、Leader Assignment（可空）、Leader Scope | 创建、编辑、查看业务、归档、查看 Leader Work Surface | 名称、职责、Leader Assignment（可空） | 名称、职责、Leader Assignment | 业务与 Role Structure、跨 Business 风险 | 业务详情、员工目录、Business Space | Mixed | Master Map v3.0 + Leadership Assignment |
| Business | 表达持续Business身份、整体方向、Workspace组合与成长；Business Work Surface 是 Business 管理与 Workspace Directory / Portfolio List | 公司版图 / Business Space → [业务] | Business Definition、Operating Status、Workspace Directory、Business Team；业务介绍、Business-level Goal / Direction、Rules / Configuration、整体结果与风险 | `id`、名称、Department（必填；长期 Business 必须归属 Department）、Business-level Goal / Direction、Introduction、Rules / Configuration（Title / Content 项集合）、Business Leader Assignment、至少一个 Workspace、Workspace 数量/轻量摘要、整体状态、重要结果、问题/风险、Team 摘要 | 创建、编辑、复制 Business、查看/编辑 Rules、创建 Workspace、进入 Workspace、进入 Leader Work Surface、进入 Insights；不在 Business 内编辑 Workspace Team Operating | Name、Department（必填）、Business Leader Assignment（可空）；Introduction / Goal / Rules 通过 Conversation Proposal 逐步形成；正式创建Business成功必须原子形成First Workspace；无专业匹配使用Generic | Introduction、Goal、Rules / Configuration、Leader Assignment、生命周期动作；不把 Workspace Execution 状态写回 Definition | Workspace Directory → Professional Workspace、Role、Employee、结果、Insights | Workspace、结果、会议、Insights、Assistant | Domain / Mixed | Business Work Surface + Leadership Assignment |
| Workspace | 承载一个独立经营单元和完整专业经营环境；不是 Page | Business Space → [工作空间] / Workspace Directory / 直接工作入口 | Shared Workspace Shell、Workspace-local Domain Navigation、一个或多个 Professional Surface、Shared Team Operating、Shared Employee Work Area；Identity、Workspace Leader、Goal、Rules / Configuration 与轻量 Current Operating Summary | `id`、所属 Business、名称、Workspace Leader Assignment、External Account / Operating Object、Workspace-level Goal、定位、受众、Workspace-level Strategy、Rules / Configuration（Title / Content）、Package/version、Domain Navigation、Professional Surfaces、Team Operating / Default Flow、Role / Responsibility Assignment、Employee Workstations、Capability requirements、Knowledge、Schedule、Current Work、Result、Analytics、Risk、History | 创建、编辑、进入/切换专业工作面、配置、复制 Workspace、组队、暂停/恢复、进入 Leader Workstation；Surface 切换不改变 identity / ownership / execution | Business、名称、外部对象、Goal、定位、受众、Strategy、Rules / Configuration、Package、Team Operating、Workspace Leader Assignment、团队/岗位、能力、资料、排期 | 上述独立 Workspace 配置；高风险授权单独确认；不采用 Default → Override 技术模型；Package/Surface 不绑定 Employee ID | selected Professional Surface、Leader / Employee Workstation、Result、Evidence、Insights、Meeting | Business Work Surface、Company Map、Assistant | Domain / Mixed | Business Work Surface + Leadership Assignment + Workspace Package |
| Team Operating / Default Flow | 定义当前 Workspace 如何按责任协作 | Professional Workspace → 团队运转；按需打开编辑器 | Role、Responsibility、Employee Binding、Input、Output、Default Flow、Review / Return、Work Handoff；Workflow / Router / DAG / State Machine 仅为内部语言 | `id`、Workspace、Role、Responsibility、Assigned Employee、Input 摘要、Output 摘要、Default Flow / Review / Return 关系、Operating Definition Version | Add Role、Delete Role、Drag/Reorder、编辑 Responsibility / Binding / Input / Output、查看影响、保存不可变版本；A→B 仅为默认下一 Responsibility，不是强制序列或任意 DAG 边 | Role、Responsibility、Input/Output 摘要、合法 Employee Binding、关系 | Responsibility、Binding、关系与版本；不含 Model/Skill/Tool/MCP/Knowledge/Permission；不含 Execution 状态 | Role、Responsibility Assignment、运行/结果（仅反查） | Workspace、Employee Workstation、Assistant | Mixed | Team Operating contract + Responsibility Routing Runtime |
| Role | 定义公司岗位责任 | 公司版图 → Business Work Surface / Department Work Surface | 职责、Workflow Position、责任 Scope、Leadership Role（如适用）、员工绑定、空岗 | `id`、名称、职责、Workflow Position、责任 Scope、业务/部门/工作空间归属、是否 Leadership Role、能力包摘要、状态、Assignment 数、空缺原因 | 创建、编辑、绑定、解除绑定、设为/移除对应 Scope 的 Leader Assignment | 名称、职责、Workflow Position、责任 Scope、Leadership Role（可选）、能力包、所属范围 | 职责、Workflow Position、责任 Scope、Leadership Role、能力包、状态 | Responsibility Assignment、Employee Binding、Workflow Step、能力包 | 人才与能力、员工目录、对应 Work Surface | Mixed | Organization Map + Responsibility Assignment + Workflow Definition |
| Employee Profile | 让 CEO 看见一个正在工作的公司员工 | 员工目录 / Role | 身份、岗位与 Assignment、能力、工作状态、近期结果、成长 | `id`、姓名、身份、来源专家、Role、Assignment（Employee × Role × Scope）列表、Business / Department 关系、状态（空闲/工作中·desc/阻塞·cause）、能力摘要、Workspace、最近结果 | 查看、配置、添加/撤销 Assignment、换岗、组队、暂停、进入 Identity Conversation、进入指定 Assignment Conversation | 专家来源、公司身份、Role、Assignment Scope、能力包、权限 | Role、Assignment Scope、能力、权限、Workspace | 工作记录、结果、资料引用、各 Scope Conversation | Role、Workspace、Business、Department、Leader Work Surface | Shared / Mixed | UI Frozen Shell + Leadership Assignment + Employee contract |

> **Assignment 投影补充：** Business / Workspace 的 Leader 字段必须落到真实 Leader Assignment（而非自由文本）；Workspace 继续拥有自己的 Leader Workstation。Workflow 节点的 Assigned Employee 必须带 Role / Scope Assignment；同一 Employee 的不同 Assignment 不合并 Conversation Context。
| Expert | 发现可招募的外部专业能力 | 人才与能力 → 专家 | 简介、擅长、来源、可用能力、关系要求 | `id`、名称、领域、简介、来源、Agent/Model、Skill、Tool、Knowledge、Connector、授权要求 | 搜索、查看、招募、保存候选 | 来源、简介、能力、关系要求 | 能力映射、关系与授权 | 招募预览、岗位匹配 | Role、员工创建、Workspace 组队 | Domain | Talent Market documents |
| Skill | 提供职业能力组合而非零散插件 | 人才与能力 → 技能 | 能力包、适用岗位、依赖、版本 | `id`、名称、说明、版本、来源、适用岗位、依赖、权限、健康 | 查看、安装/引入、组合、更新、停用 | 名称、来源、依赖、适用岗位 | 版本、组合、权限 | 绑定员工、运行记录 | Expert、Employee、Workspace | Shared / Domain | Talent Market + capability contract |
| Connector | 把外部系统带入公司 | 人才与能力 → 连接器 / 设置 | 系统、授权、健康、范围、维护 | `id`、名称、系统、授权方式、scope、状态、最近检查、负责人、影响业务 | 连接、验证、重授权、撤销、维护 | 系统、scope、授权方式 | scope、负责人、授权 | 使用它的 Business / Workspace | Business、资料库、员工能力 | Shared | Capability / Settings authority |
| Meeting | 形成讨论、决定与后续责任 | 会议 / Business / Workspace | 议题、讨论、提案、决定、承诺、回顾 | `id`、上下文、标题、参与者、议题、事实/观点、提案、决定、承诺、截止、状态、证据 | 创建、讨论、提案、决定、跟进、回顾 | 上下文、议题、参与者、时间 | 议题、提案、承诺、状态 | Decision、Commitment、Result | Assistant、Business、Workspace | Shared / Domain | Meeting contract |
| Settings | 维护连接、权限、偏好与本地运行 | 左下角头像 | Personal & Appearance、Company Defaults、Models & AI Providers、Permissions & Security、Application & Data、Account & Help | `profile`、语言/locale、时区、主题、通知偏好、公司资料与默认值、Model Provider 连接/安全凭证引用/endpoint/模型发现/默认模型、Agent Provider 状态/授权/安装健康、审批与访问状态、Connector 权限、凭证状态、审计/验证记录、本地数据位置/缓存/导入导出、版本/帮助 | 修改、测试连接、发现模型、选择默认、连接/撤销/轮换、导入/导出、清理缓存、重置偏好 | 首次身份、语言、时区、主题、公司资料、Provider/Agent Provider 连接引用、权限默认值、通知默认值 | 除不可变身份外的上述字段；高风险授权单独确认 | Provider / Agent Provider 详情、权限审计、数据管理、帮助 | 能力中心、头像菜单、CEO Desk/Business/Workspace 缺口恢复 | Shared | Settings Research / Product Blueprint / Security authority |
| Business Duplicate | 从验证模型快速建立独立业务 | Business `…` / Business Work Surface / Company Map | Copy Preview、复用项、重配项、不复制项、新业务 | 源 Business、Business Definition / Rules 与经营方法版本、新名称、目标、定位、外部对象、Staffing 方式、排期 | 预览、确认复制、取消、进入新业务 | 名称、目标、定位、外部对象、Staffing、排期 | 复制后按 Business 编辑字段修改 | 新 Business Work Surface、Company Map、Business Space、Workspace | 公司版图、业务空间、会议 | Domain | Business Duplication decision |
| Workspace Duplicate | 在同一 Business 内从成熟工作空间创建新的独立 Workspace | Business Space / Business Work Surface / Workspace `…` | Copy Preview、复用项、重配项、不复制项、新 Workspace | 源 Workspace、Workspace IA / Operating Configuration 版本、新名称、外部对象、目标、定位、受众、Staffing、知识、授权、排期 | 预览、确认复制、取消、进入新 Workspace | 名称、外部对象、目标、定位、受众、Staffing、知识、授权、排期 | 复制后按 Workspace 字段修改 | 新 Workspace、Business Work Surface、Business | Business Space、Workspace、Assistant | Domain | Business × Workspace Product Model |
| Business Report | 让分析师交付可追溯的经营分析成果 | 经营洞察、Business、Workspace、Employee Workstation | 范围、周期、责任、事实、解释、未知、建议、证据、复核 | `id`、`scope`、`period`、`responsibility`、`authorEmployee`、`department`、`business`、`trigger`、`dataSources`、`modelAgentProvenance`、`createdAt`、`review`、`facts`、`interpretation`、`unknowns`、`recommendations`、`evidence` | 查看、追问、要求调查、请求独立复核、进入会议 / 决策、回到来源 | scope、period、trigger、sources、责任员工 | 仅允许追加复核、注释和新版本，不改写原始事实 | Report → Conversation → Analysis Task → Evidence / 新 Report → Decision | CEO Desk、Business、Workspace、经营洞察 | Shared / Domain | Operating Intelligence UX Baseline |
| Insights | 深入理解经营变化并比较效果 | 经营洞察一级导航 / CEO Desk / Business / Workspace / Employee / Company Map / Assistant | 公司经营、业务分析、组织与员工、模型与能力、分析报告、专项研究；范围与周期、指标、趋势、比较、归因、质量、来源与未知 | `scopeType`、`scopeId`、`period`、`metricId/name/value/unit`、source、freshness、collectionMode、unknownReason、employee/team/model/agent/provider/capability refs、execution/result/review/acceptance/externalResult refs、comparisonSet、sampleSize、comparability、evidence、annotation | 筛选、趋势、比较、语义兼容图表切换、归因、打开来源、下钻、带来源手动录入、返回原上下文 | scope、period、metric、comparisonSet | 筛选、注释、手动回填记录（不可改原始事实） | Company → Department → Business → Workspace → Employee/Team → Execution/Result/Review/External Result | CEO Desk、Business、Workspace、Employee Profile、Company Map、Assistant | Shared / Domain / Mixed | Product Blueprint / Operating Intelligence UX Baseline / existing Truth & Result authority |

### Work Surface Page Contracts

| Page Contract | Page Mission | Entry / Return | Information Responsibilities | Actions / Drill-down | Cross-page Boundary | Source Authority |
|---|---|---|---|---|---|---|
| Department Work Surface | Shared Management Surface Contract Candidate：让 Department Leader 处理本 Department 的责任、Business 协调、资源与升级事项 | Business Space → [部门]；Company Map / CEO Desk / Assistant / Meeting / Insights 可反向进入；完成后回原范围 | Shared Identity、Leader Workstation、Responsibility、Goal、Current Focus、Children、Result/Risk、Team 摘要、Management Actions、Escalation | 查看/编辑使命与负责人、处理 Handoff / Exception / Decision Request、进入 Business Work Surface、Organization Center、Insights、Meeting | 不复制 Organization Center 结构真相，不承载 Domain-specific 专业工作 | `docs/reviews/DEPARTMENT_WORK_SURFACE_PAGE_CONTRACT.md` |
| Business Work Surface | Shared Management Surface Contract Candidate：让 Business Leader 通过连续结构管理 Business Definition、Operating Status、Workspace Directory / Portfolio 与 Business Team | Business Space → [业务]；Company Map / CEO Desk / Workspace / Employee / Meeting / Assistant / Insights 可反向进入；完成后回原范围 | Business Definition（Leader Workstation、简介、Business-level Goal / Direction、Rules / Configuration 摘要）、Operating Status、Workspace Directory（Name / Leader / 轻量 status / focus / issue / member count / direct enter / create）、Business Team | 查看/编辑 Business Definition、查看整体状态、创建 Workspace、进入专业 Workspace、处理业务级 Handoff / Exception / Decision、复制/暂停/缩减/转移/关闭/合并/拆分；不在 Business 内编辑 Workspace Team Operating | 不创建第二个业务整体页面；不提供 Business 统一团队运转，不嵌入 Workspace 详细工作面，不复制 Organization Truth 或 Insights | `docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md` |

### 当前共享产品规则

- **Business / Workspace Goal 语义：** Business 持有 Business-level Goal / Strategy，负责该类业务的整体方向；每个 Workspace 持有自己的 Workspace-level Goal / Positioning / Strategy，负责独立工作空间的具体经营。同一 Business 下 Workspace 不默认共享彼此的 Workspace-level Goal / Strategy，但都受所属 Business-level Goal / Strategy 的整体方向约束；不创建 Default → Override 技术模型。
- **Shared Management Surface 定位：** Department Work Surface 与 Business Work Surface 都是 Shared Management Surface Contract Candidate，提供跨 Domain 的管理骨架；具体 Domain 必须在 Shared Management Shell 上叠加 Domain-specific Operating Surface，先经内容增长部、研发部、小红书运营、Curis 产品研发 UX Exploration 验证，不预设统一页面。
- **Business Definition / Workspace Boundary 语义：** Business 是运行说明 / 经营定义，提供 Business Introduction、Business-level Goal / Direction、通用 Rules / Configuration 与 Workspace Directory / Portfolio 投影；Business 不拥有统一团队运转，也不嵌入 Workspace 详细设置。每个 Workspace 独立拥有自己的 Goal、Rules、Team Operating、Role / Responsibility Assignment、Operating State 与 Result，点击目录直接进入 Professional Workspace。
- **Team Operating / Role / Employee 语义：** 用户产品语言为“团队运转 / 默认流程”。`A → B` 仅在 A 产出 accepted Result 且没有更强的 Consult、Review、Return、Need、Leader、Decision、Wait 或 Domain rule 时表示 B 为默认下一 Responsibility；不是强制运行序列或任意 DAG 边。Role、Responsibility、Employee Binding、Input、Output、Review / Return 仍由 Workspace 承载，运行中的工作 pinned immutable Operating Definition Version；Workflow / Router / DAG / State Machine 仅属内部 Runtime / Audit 语言。
- **Workspace Capability / Employee Capability 语义：** Workspace 可以关联并提供团队可用的 Model / Agent、Skill、Tool、MCP / Connector、Knowledge、Permission 等资源，作为专业工作环境的能力投影；Employee 的Skill/Tool等按合法能力机制配置，Work Mode消费Shared；Model/Agent在Conversation选择全局可用项，不重复Business或Employee固定绑定，Workspace 不维护第二套 Employee Capability Truth。
- **Rules / Configuration 与 Conversation Truth：** Rules / Configuration 是通用 `Title / Name + Content` 项集合，不为行业预先发明字段 Schema。Goal、Rules、Business Definition、Workspace Definition 的主要创建路径是 Conversation → Structured Proposal → 必要确认 → 写入 Truth → 更新摘要；Panel / Modal 只负责详情编辑与纠错。
- **Generic / Professional Domain：** 研发、内容增长、小红书、短视频只是 Professional Workspace 形态示例，不是 Curis 边界或固定业务类型；相近业务优先匹配、配置、派生或安全组合，未知业务可以从 Generic Business + Generic Workspace 真实开始，再按 Domain / Risk Gap 研究与演进。Department 不提供专业 Workflow Builder；Business Configuration 不等价于 Professional Workspace Builder；已有专业 Workspace 页面不因 Business Contract 重做，Generic Workspace 页面另行 Review。
- **本轮 Product → Implementation Gaps：** Structure-aware planning、multi-level creation 与 impact calculation、atomic apply / rollback 仍只登记为实现缺口；Workspace-scoped Responsibility Routing / real Employee execution 已由接受的 Implementation Truth 覆盖。本轮不设计 Runtime / Schema / Database / Code。
- 普通用户语言优先使用公司、业务、部门、员工、专家、团队、工作空间、目标、工作、技能、资料、结果、问题、确认、决定、下一步；Office 仅作为历史 / implementation / migration provenance。RoleSlot、Executor、Cycle、Gate、Simulation、Evidence 等只在高级/审计/内部层出现。
- 资料库是统一的本地资料、外部资料、网页/GitHub/云盘、成果与经验入口，支持读取、索引、搜索、引用、权限、来源追踪和自动沉淀。
- 经营洞察 / Operating Intelligence 只消费既有 Truth、Result、Usage、Cost、Execution、Feedback、Review；所有指标带 source / freshness / verified / manual / unknown / stale / missing / external，不新增第二套 Truth / Result / Analytics Runtime。图表只在同一 Dataset 的语义兼容视图间切换；不展示无 Calculation / Threshold / Evaluation Contract 支撑的综合健康或最佳排行。
- 默认 Company Support Organization 包含空间工程部与数据分析部；Company Analyst 属于数据分析部，Business Analyst 可由数据分析部 Assignment / Allocation 支持 Business 或由成熟 Business 自建 Role / Employee。Functional Affiliation 与 Business Assignment 分离。
- Business Exit（Pause / Reduce / Transfer / Close / Merge / Split）和 CEO Operating Day Cross-day Continuity 是跨层产品合同，不创建独立导航、页面或 OperatingDay Runtime Primitive。
- 产品规划从真实经营/员工工作/失败证据出发，明确能力与AI/User/Provider边界，再在既有一级区/对象结构内展开字段、动作、状态和回程；禁止由Runtime对象反推导航，不机械page-first。
- 保留结果真实性、权限、外部副作用、状态恢复、责任连续性、用户确认、失败回退和审计；成熟通用能力优先复用 Workbuddy、Coze、Codex/Claude Code、ChatGPT、OpenOPC、EvoFlow、Linear 的已验证产品模式。
- Desktop 壳层采用一级侧栏 + 可折叠上下文侧栏 + 自由主工作区 + 按需右侧检查器：左边是我在哪里，中间是我正在做什么，右边是我正在查看/修改什么。Workspace 内部使用 Pane-local Header，不设永久 Global Topbar。

---

## 0. 这份母版要确定什么

当前产品合同继续回答六个结构问题，并在下方逐层展开：

1. 普通用户打开 Curis 后从哪里开始。
2. Curis 的一级产品框架应该保持多大、每一层解决什么问题。
3. Company、组织、业务、员工、能力、Workspace 和资料库如何形成易懂关系。
4. Workspace 怎样成为可以内嵌成熟 AI 产品的独立数字工作空间。
5. 用户如何通过对话、UI 和自动运行完成工作。
6. 目标、数据、分析、复盘、调整和持续进化如何回到公司级循环。

它不在本轮确定：

- 像素布局和未经交互Review的具体组件组合（字段责任由Current Contract展开，不再留给UI猜测）。
- Provider 的具体 API、协议和数据库表。
- Runtime 状态机、Simulation、Evidence 结构的实现细节。
- 任何外部 Agent 已经接入或已经能够真实执行的事实。
- 未来商业化的租户、计费、市场和平台拆分。

### 0.1 三层产品优先级

```text
第一层：普通用户体验
  我想做什么？谁在做？发生了什么？我需要决定什么？

第二层：公司化组织
  公司、部门、业务、员工、Workspace、资料和会议怎样形成关系？

第三层：底层运行支撑
  外部 Agent 怎样接入？工作怎样持续、失败、恢复、记录和受控？
```

第一层决定产品入口，第二层形成 Curis 的差异化，第三层保证前两层不造假。

---
