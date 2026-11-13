# Curis Core Product Authority Reconciliation

Status: Review
Authority Class: REVIEW / EVIDENCE
Date: 2026-09-09
Owner: Main Development
Disposition: CORE AUTHORITY DRIFT IDENTIFIED / STOP FOR CEO REVIEW
Source: CEO Core Product Truth / Current App Deviation Audit; current repository and immutable SQLite inspection; earlier same-day native inventory.
Next Gate: Authority reconciliation, then bounded core product correction. Final UI Master Batch 1 remains PAUSED.

## 1 Executive Verdict

**不能把当前状态继续概括为“功能全完成，只差 UI polish”。** 已验收的执行、Conversation、Usage、Result Viewed、Meeting、Knowledge、General lifecycle 是真实且应保留的局部能力；它们没有证明默认公司支撑组织、专业业务启用、完整领导工作面、统一 Four-Pane 和可拖动全局 Assistant 已交付。

本次定位到可复查的结构缺口：默认两个支撑部门没有进入 Company materialization；旧 Studio 从 Current Business 入口可达，但提交非 canonical Business ref；WorkspacePaneShell 与 TerraShell 的导航/空间职责分叉；全局助理退成固定角落的简报面板，不能拖动，聊天必须回 CEO Desk。经营洞察还以 Role 文本匹配选分析师，而非分析岗位 Assignment。

这不是重建 Company OS 的依据。**Canonical Business、Parent Resolver、Workspace Package v2、Shared Runtime 都存在。** 正确修复是补组织形成与空间/入口集成，不能再造第二套数据系统。

证据边界：本轮没有运行 App、测试、Provider 或写业务对象。使用当前源代码、正式 scoped reviews、既有 34 张 native 截图和当前隔离 DB 只读核验；不宣称所有历史材料已穷尽，也不宣称 76 个状态全部实机覆盖。未恢复的细节明确列 UNRESOLVED。

## 2 Authority Hierarchy

按本轮 CEO 指定：FROZEN → ACCEPTED → CURRENT AUTHORITY → APPROVED CANDIDATE → REVIEW → IMPLEMENTATION → HISTORY。每条仍需看 **Authority Class、适用范围及 supersession**；文件中某个实现段落写 ACCEPTED，不使它有权废弃 Frozen 产品语义。

核心源与定位见 [Truth Ledger](CURIS_CORE_PRODUCT_TRUTH_LEDGER.md) 的 B/M/U/S/C/V/F/W/P/Q/H 键。AGENTS 已读取；根目录 `CLAUDE.md` 不存在，不编造其指令。CURRENT_STATE / Pointer / Completion / Backlog / Change Log 的最新 2026-09-08 注册一致写 `PRODUCT COMPLETE / ACCEPTED WITH RECORDED P2`，同时要求 final CEO review；本报告不替它们改字。

Pointer 并非完全遗漏 Shared Authority：#32 指向 Company OS Shared，#45 指向 Frozen Shell，文尾还单列 Design Agent 路线。因此“Pointer 没有指向关键 Frozen”不是可成立的统一根因。更具体问题是顶端完成声明未说明支撑组织/空间职责未覆盖；部分旧 CURRENT 段仍说 Knowledge/Meeting 待实现。

CURRENT UI Foundation 明确是 Review / Candidate；Visual Standard V1 明确只冻结视觉语言且不替代 Shell。不得让二者中的局部实现说明覆盖产品。

## 3 Company Model

Company 是 CEO 经营的整体：方向、规则、员工、资源、业务、结果与历史。身份链不是 Project。用户业务可为空，但默认职能支持不是用户 Business。

|阶段|产品应有|当前实现|
|---|---|---|
|未创建 Company / 先浏览|合法 Empty Curis；无伪造公司业务|App Entry accepted evidence 已覆盖|
|Company 创建后|CEO 身份、Company、同一 CEO Assistant；默认空间工程部/数据分析部；用户 Business 可为空|Foundation 只物化 Company + CEO_ASSISTANT + FoundingRun/link/transition；未建立两个部门|
|确认首个业务|真实 Department 归属 + canonical Business + first Workspace；DRAFT 不冒充已经营|FirstRunDelivery 原子创建，支持已有 Company；真实员工/能力另行取得|
|进入长期经营|Operating Team、Leader责任、能力与具体工作；缺项诚实等待|已有 explicit Team truth → workflow/work；默认支撑部门承接未闭环|

不能把“公司创建后业务为空”解释为“公司组织可以永远缺两个系统支撑部门”。也不能自动塞进研发/内容增长示例业务。

## 4 Fixed Support Departments

**Authority 已明确，不是 Research Candidate。** B 默认 Company Support Organization、M 同名段：每个新 Company 默认空间工程部、数据分析部；C §9.4 冻结空间工程部身份及专属责任。

|项|空间工程部|数据分析部|
|---|---|---|
|组织身份|System-default Company Support Department|System-default Company Support Department|
|用途|把经营目标转成可工作的业务空间，并维护/演进|Company Analyst、跨业务分析及决策支持|
|是否用户 Business|否|否|
|责任|Leader、行业研究、经营方法、设计、搭建、Quality；一人可兼任，不固定员工名单|Company Analyst；Business Analyst 可经 Assignment/Allocation 服务业务|
|固定 Team 人数/具体员工|未冻结；不得按流程文字自动复制员工|未找到固定人数合同；司衡是产品中 Company Analyst 名称，不等于 DB 已有员工|
|固定 Workspace identity/创建时机|UNRESOLVED|UNRESOLVED|
|删除/隐藏/重命名规则|UNRESOLVED；默认存在不自动等于不可改名|UNRESOLVED|
|组织中心|应显现真实部门及责任/员工，不应伪造 Business 来容纳|同左|
|业务空间入口|Department Leader Work Surface，非技术安装页|分析工作面与真实组织身份连续|

当前 isolated DB 有 2 个 `department_instances`，均 `name=业务部 / department_type=business.general`；没有这两个默认支撑部门。它是验收公司，不代表所有用户库。本轮不新建 fresh Company；结合 Foundation 唯一 materialization 和 FirstRunDelivery 调用路径，证明被审创建路径缺省组织未实现，而非仅从某一张空截图下结论。

## 5 Business Activation

恢复链：Intent → read Company → reuse/create/adjust proposal → 必要 CEO Gate → canonical Department/Business/Workspace → 合法团队/Leader/能力 → 工作。空间工程可委托，CEO 自建也合法；不要求每次行业研究，不要求每次从模板开始。

**已成立**：General proposal/first-run + canonical atomic create + Parent Resolver + explicit staffing + Work execution。**未证明完整**：默认工程 Leader 从需求澄清到专业方法、Package、team handoff、业务接管的产品链；Verified Professional Match 自动交付。

具体坏接线：`frontend/app/ceo-office/business/page.js:60`、`workspace/page.js:44` 都链接 Studio；`workspace/studio/page.js:200–207` 使用 `business-${type.toLowerCase()}`。`backend/app/runtime/workspace.py:102–109` 验证真实 `canonical_businesses.business_id`，不存在即拒绝。**后端 fail-closed 正确，不能为旧 UI 加默认 Business。** 未提交表单、不制造新 Workspace；这是可静态证明的接口契约冲突，不冒称现场观测到一个新 422。

Department 中启用业务不是选一个 Department template 等于开业；创建 canonical Business 才加入经营关系。模板/Package 提供结构与能力，不提供用户 identity/credentials/results。选入后能否自动组队必须以真实 Assignment/能力为准，缺人不能生成假的 Operational。

## 6 Organization Model

```text
Company
├─ System-default Support Departments
│  ├─ 空间工程部 → 专属责任 / 实际员工分配
│  └─ 数据分析部 → Company Analyst / Business allocations
├─ 用户 Department → Business → Workspace(s)
│                             └─ Operating Team responsibility boundary
│                                └─ Role / Responsibility Assignment → Employee
└─ Company-level Employees（可以无 Department）
```

这不是强制创建顺序，也不是 Employee 只能服务一个 Workspace。Functional affiliation 与 service Assignment 正交。Team 不插成第二个 ownership 父节点替代 Business→Workspace。

`organization_projection.py` 读取 companies / departments / canonical businesses / employee_instances / assignments，利用 EmployeeExecutionIdentity 映射。该读层是真实的，不能因为部门缺省没做而叫它 fake。Current OrganizationCenter 两 Tab、Business-first、反查已实现；但没有完整 Company+→Department、Department+→Business、领导责任形成工作链。**读已有关系的 acceptance 不覆盖组织形成机制。**

## 7 Team Operating Model

C §3.3 `TEAM_LEAD_ONLY_ON_EXCEPTION` 仅约束 WHO 任务路由；§9.1/9.3 明确持续业务领导力。Leader 不是特殊 Employee 类型或权限。Work/Child Work、Assignment、verified callback、Handoff、P7、Result/Evidence、Cycle evaluation 在现有 Runtime 有实现及 scoped acceptance。

直接复用 `responsibility_routing.py`、`autonomous_operating.py`、`employee_execution_identity.py` 及相关 tests。不得说缺 Department UI 就缺 Router，也不得把 Workspace-scoped 已验收扩写成 Department/Business 跨层自动领导已全部完成。

CEO 表达目标/边界/策略和重大选择；可深入员工，但不必须画 DAG。默认流程只是可解释的下一责任，不是任意图引擎。Draft/unconfigured 空间允许继续搭建；无真实团队不算长期经营完整成功。

## 8 Business / Workspace Contract

Business 承载整体持续方向、Goal/Strategy、Rules 与 Workspace 组合；Workspace 是其中具体独立经营工作环境。B/M 中“聚合同类 Workspace”不能把 Business 降成无身份目录；`canonical_businesses` 实际独立持久化。

Primary Business 四块（Definition / Operating Status / Workspace Directory / Business Team）合法。其卡片/重复标题主要属视觉；不能据截图宣布 Business=Workspace。相反 `/projects` 明确沿用 Project-as-Business 旧注释/页面，必须隔离；RD 内 Project 仍是合法 domain object。

同 Business 的 Workspace 不默认共享目标、凭证、知识、历史或所有成员。复制 Business ≠ 复制 Workspace，禁止复制 identity/secret/conversation/result/audit。当前完整复制/退出/merge/split 产品链不能由既有 create/lifecycle tests 推定已实现。

## 9 Workspace Engineering

产品规定复用优先、Generation last resort；方法论本身 W 为 Approved Candidate，不把其全部 15 步升格已实现。C §9 固定的组织/责任/交付边界则必须遵守。

**不是纯 monolithic frontend**：`workspace_package_runtime.py`、`workspace_package_api.py`、`InstalledWorkspaceRuntime.js`、installed route 真实存在。P 已接受 v2 Navigation/Surface Registry/Views/Requirements/Projections、canonical responsibility resolution、同 Workspace deep link、restart；P1.5 finite JSON migration/rollback 亦有正式回归。六种有限 renderer 不是任意 React/JS 执行许可。

**也不是完整自主空间工程产品**：普通专业入口仍 RD/XHS/Shortvideo 专属 React；默认工程组织不存在；Studio旧建造表单与新 canonical relation不一致。正确结论：Package substrate SUPPORTED，organizational operating chain PARTIAL。Installed/Operational/Company Integrated/Operating/Evolvable 必须分别证明；Package install 不等于经营交付。

## 10 Four-Pane Framework

|Pane|职责/内容|显示/交互|边界|
|---|---|---|---|
|Navigation|公司级七区、对象搜索、身份设置、快捷访问|可完全收起；T1 在 Main 恢复；Pane-local header|不是业务员工列表；Conversation quick access不是第八区|
|Context|Domain Navigation、当前工作所需对象集合/上下文|默认收起；T2；按需 resizable；空间不足 overlay/focus|不放完整 Conversation/Employee profile；不得把 Main 必需业务信息只放这里|
|Main|selected Professional Surface + shared work area；阅读/讨论/工作现场|始终存在，关闭辅助 Pane 后独立可用|布局由域决定，不强制 Calendar 或统一员工 Dashboard|
|Utility|对象 Detail/Editor/Evidence/Tool、Result专业阅读|默认收起；T3；resizable；maximize overlay|不是固定“成果列”；不是 CEO Assistant 栏|

四 Pane 独立顶部对齐；260/360 是建议默认不是固定合同；像素不要取代角色。普通两列 Nav+Main 完全合法。

当前两种壳：TerraShell 有 Nav+Main，但 desktop T1、统一Context/Utility机制未接；WorkspacePaneShell 有T1–T3、resize/maximize，但 Nav仍六区、没有当前Recent Conversation。因此不是“Four-Pane全部消失”，而是**共享基本空间契约没有贯穿当前 App**。

General 的 XL `grid-cols-[minmax(0,1.6fr)_minmax(280px,.8fr)]` + 永久 aside 装 readiness/team/selected result，非独立按需 Utility。先恢复职责与按需消费，不能直接删右栏。CEO/Business/Conversation/Insights 用 Nav+Main 本身不违规；各自引用详情/上下文、Header、导航仍需按 shared contract接通。Meeting不常驻右栏是合法。Knowledge正文在Main正确，其辅助来源区不是仅凭视觉就可判非法。

## 11 Reading / Working / Operating

本轮 CEO 明确重申该空间范式。现有 B §04、U §09–17、S 支持以下职责；精确全产品枚举/宽度表没有在已读 Frozen 文档中恢复到唯一完整版本。旧 Research 的 Reading 640–760 / Work 720–1040 / Operating 920–1200 为 Candidate，不能写 SAFE/Frozen。

|模式|心智/主职责|典型对象|Context / Utility|密度边界|
|---|---|---|---|---|
|READING|理解资料、结果和依据|Knowledge、Report、Result/Evidence正文|集合/来源按需；属性/证据可开Utility|正文可读优先；精确数字 UNRESOLVED|
|WORKING|与员工或业务对象持续工作|Employee Conversation、Workstation、Work、Meeting讨论|本次责任上下文；专业工具/Result引用|自然消息+有限嵌入，不让terminal主导|
|OPERATING|看方向、责任、结果、问题与下一判断|CEO Desk、Business/Department管理面、Workspace经营面、Insights|专业Domain选择；具体判断/证据按需|摘要优先，不等于统计Dashboard|

七区：CEO→Operating；业务空间→Operating目录与域内Working/Reading；组织→结构Reading/管理，不冒充员工工作；人才→发现Reading/招募操作；洞察→Operating analysis/Report Reading；资料→Reading；会议→Working讨论/Decision。这是一张职责恢复表，不是新视觉状态机。

Object→Surface：Business→Operating Main；Workspace→Domain selected Main；Employee→Main Workstation，资料详情Utility；Work→相关Workspace Work Area；Result/Artifact→轻量reference后Utility（需要长读可maximize）；Evidence→Utility；Knowledge→Reading Main；Decision→P7 attention→plain package→evidence Utility；Conversation→Main或同一Workstation；Meeting→Main多人讨论；Report→Reading/analysis面。Floating是Assistant承载方式；Modal/Drawer是交互容器，不是所有对象的永久identity。未规定的细分对象容器/精确尺寸均UNRESOLVED，不能仅凭本表开工设计。

## 12 App Shell

```text
Curis root / stable Company + CEO context
├─ Primary Navigation（七区）
│  ├─ Conversation Quick Access（recent subset）
│  └─ Object Search / CEO avatar → settings/help
├─ Current surface
│  ├─ Context（按需）
│  ├─ Main（独立自成立；selected domain + related work）
│  └─ Utility（按需 detail/editor/evidence/tool）
├─ Global Floating CEO Assistant（同身份/同对话，非 Pane）
└─ Temporary overlay / modal / drawer（合法确认/启动/配置，保留返回来源）
```

当前 TerraShell 的静态“齐”头像不来自CEO；实际左栏头像来自presentation，两个身份展示不一致。Global Search按钮disabled虽诚实，但与Frozen公司级对象搜索交付有缺口；Conversation局部search不能冒充它。

## 13 CEO Assistant

当前 CEO §22直接确认 floating/draggable/collapsible/cross-seven persistent/not reserved Pane。历史 H 将自由拖动判Vision只能作为当时审计，不能否决本轮。历史 memory 所指旧设计规格路径当前不存在；尺寸360等不能依记忆再冻结。

代码 `GlobalAssistant.js:192–299`：固定右下FAB、固定right/bottom面板、minimize/close；没有pointer/drag位置状态；内容为简报/待处理/关注；footer链接回CEO Desk聊天。当前入口至少三种：FAB、TerraShell按钮（同host）、CEO Desk inline真实Conversation。前两者不是两个AI身份，但浮层不是可持续聊天的完整承载。根Provider保留canonical身份是KEEP，不新造assistant。

精确初始位置/尺寸、吸附、记忆位置、快捷键、拖动边界：UNRESOLVED，需要找到当前有效原始决定或做窄范围补录；不能把当前390px CSS写成Authority。**不建议退役floating能力，只替换不满足合同的宿主投影。**

## 14 Conversation Sidebar

`ConversationQuickAccess.js`读取 canonical recent summaries，5秒poll，最多30条由服务约束；search仅当前recent subset的title/employee。服务按persisted message event activity排序；empty holder不出现；dismiss-through-activity持久化，非delete；同employee不同topic可区分。打开conversation_id恢复samehistory，Work/ref不是conversationidentity。

Q已有真实云回复、Usage、reference、Viewed、native/restart证据，本轮KEEP。CEO Assistant保留其现有 durable holder，不要求为统一一次迁移Meeting/Assistant历史。Sidebar≠Assistant，不能用sidebar完成浮层合同。旧Assignment-scoped history与后续跨assignment持续conversation的关系需明确“per-message context isolation ≠ 必须新conversation”措辞，不擅自拆已验收记录。

## 15 Capability / Talent

复用成熟Provider/Agent/Skill/Connector，招募后才有Employee；安装≠授权≠可运行。当前 recruitment/avatar/binding是实能力；未连接目录无假成功，KEEP。但连接器技术项目名、Capability Profile等默认暴露是产品投影偏差。不能因此重建插件或身份系统。

## 16 Knowledge

Company Reference Space合同、真实scope/typedrefs/UsedBy/archive/restart已有accepted实现。现有导入的资料根/相对路径与Memory措辞、整页Work picker偏离普通阅读/引用心智。主阅读、来源可追踪要保留；不把未知格式/connector补成假支持。旧U/M仍写Runtime PARTIAL/implementation PENDING，与Pointer实现登记不一致，是文档状态旧段，不是推翻Knowledge验收。

## 17 Operating Intelligence

真实分析projection可按Company/Business/time读已有usage/runtime/artifact，UNKNOWN保留，Report/P7链存在。**组织归属没有完整接通**：`operating_intelligence.py:144–147` 用 role like 分析/经营取第一人，没有验证其数据分析部/Analyst Assignment或Business allocation。即使找到一个真实Employee，也不等于该人是当前合法负责分析师。不得标fake指标，因为指标来源查询仍真实；这是analyst ownership projection gap。

自动analyst/report authoring在原review本就列未完成。数据分析部缺省修复后，还需正确scope的责任入口和“无负责分析师”恢复，而不是创建另一个Analytics Truth。

## 18 Meeting

保持Leader orchestration、Employee SPEAK/STAY_SILENT、Proposal/P7→Work/Result→Evidence→Leader、budget/no replay的已登记真实性。最终多cycle真实新事件证据仍pending且非本轮代码blocker。当前页面的讨论/P7密度不能撤销runtime验收，也不能据两张漂亮截图宣布整个SharedShell aligned。不重新调用云模型。

## 19 Current Runtime Truth

|对象/能力|状态|依据与不足|
|---|---|---|
|Company / CEO Assistant|SUPPORTED|foundation materialization；缺supportbootstrap不是缺Company表|
|Department|PARTIAL|department_instances、员工/Business关系真实；默认支撑职责未建立|
|Business / Workspace canonical parent|SUPPORTED|business_spine、canonical_businesses、Workspace校验、quarantine|
|Team / Employee / Responsibility|SUPPORTED（Workspace scoped）|runtime_entities、identity bridge、routing；不外推跨层自动领导|
|Business/Department leadership operation|PARTIAL|产品责任已定，主入口/组织装配证据不完整|
|Business activation|PARTIAL|General atomic path有；professional/旧Studio与engineering承接缺口|
|Package|SUPPORTED（bounded declarations）|v2 renderer/validation + lifecycle/migration tests/review|
|空间工程部默认承接链|MISSING（被审bootstrap）|Foundation/FirstRun不物化；不是Package底层缺失|
|Company Analyst authoritative assignment|PARTIAL|查询真Employee但角色文本heuristic不能代替assignment|
|Legacy Project path|LEGACY ONLY as universal ownership|RD domain Project仍合法；不能影响General usage|

定位的既有tests包括 `test_canonical_business_spine_schema.py`、`test_canonical_business_spine_runtime.py`、`test_v1_first_run_delivery.py`、`test_organization_center_projection.py`、`test_employee_execution_identity.py`、`test_team_operating_real_employee_e2e.py`、`test_autonomous_cross_surface_multi_work_runtime_proof.py`、`test_workspace_package_multi_surface_v2.py`、`test_workspace_package_transactional_migration_p15.py`、`test_conversation_productization.py`。本轮未运行；证据等级是当前代码+历史review，不编造新PASS数量。

## 20 Current Frontend Truth

同日I实际记录34张native、53 observed / 22 source-only / 1 domain-family unverified。维持该边界。新发现的source级问题独立标明，不冒称新Desktop click。

Current primary Organization实际export `OrganizationCenter`；analytics实际return `OperatingIntelligence`。它们文件内legacy函数的href不能直接说是当前页面可点。RD当前确实链接execution/tasks，后者返回legacy执行工作台，构成可追踪的漏出口。

## 21 Current Route Drift

以下42个路径省略共同前缀 `/ceo-office`；分类是本次审计，不是删除授权。Primary=七区；current deep link不是primary。无current incoming link只说明静态检索未找到，不声称地址不可直开。

|Path|分类|入口/证据与风险|
|---|---|---|
|/|CURRENT PRIMARY|V1Sidebar CEO|
|/business|CURRENT PRIMARY|V1Sidebar；canonical四块，漏接旧Studio|
|/organization|CURRENT PRIMARY|V1Sidebar；export OrganizationCenter，旧函数非current|
|/talent-market|CURRENT PRIMARY|V1Sidebar；市场/招聘|
|/analytics|CURRENT PRIMARY|V1Sidebar；export OperatingIntelligence|
|/knowledge|CURRENT PRIMARY|V1Sidebar；reference picker也用此路由|
|/meeting|CURRENT PRIMARY|V1Sidebar；独立多人语义|
|/conversation|CURRENT UTILITY|QuickAccess/Employee/work return，sameidentity|
|/capabilities|CURRENT UTILITY|V1Sidebar模型设置；位置与完整Settings需收敛|
|/capabilities/[type]/[id]|CURRENT DEEP LINK|能力详情，非组织主体|
|/knowledge/entries/[id]|CURRENT DEEP LINK|资料阅读/return|
|/organization/employees/[id]|CURRENT DEEP LINK|Organization/General员工入口；admin投影需修|
|/workspace|CURRENT DEEP LINK|Business目录/General identity入口|
|/workspace/installed/[workspaceId]|CURRENT DEEP LINK|Package renderer，保留动态能力|
|/workspace/software|CURRENT DEEP LINK|RD adapter；shared nav drift不删RD|
|/workspace/xhs|COMPATIBILITY|已验收XHS instance入口；不得冒充当前ContentGrowth产品identity|
|/workspace/shortvideo|COMPATIBILITY|旧TTK适配入口；未证明Current完整专业产品|
|/workspace/studio|LEGACY|Current Business/Workspace链接可达；拼接business-ref与canonical校验冲突|
|/organization/employees|LEGACY|旧独立员工目录，Current入口已在Organization Tab；不新增一级区|
|/organization/departments/[id]|LEGACY|旧Department详情链接Project；旧org函数引用，不证明当前Tab会进入|
|/projects|LEGACY|Project-as-Business；旧导航组/Project详情返回|
|/projects/[id]|COMPATIBILITY|合法RD历史Project读层同时有旧产品包装；execution run返回可能到此|
|/reports|LEGACY|SAMPLE_REPORTS；不是Current analytics artifact-report|
|/reports/[id]|LEGACY|旧报告详情/返回reports；不作为新分析报告权威|
|/decisions|LEGACY|旧Project links；本地placeholder选择，不是Current P7|
|/execution/tasks/[id]|CURRENT DEEP LINK|RD“完整执行记录”真实引用；返回旧execution是风险|
|/execution/runs/[id]|COMPATIBILITY|旧Project DevelopmentRunDrawer入口；保留历史证据访问|
|/execution|LEGACY|RD task返回/trace入口可达，旧派发中心不应CEO主流程|
|/execution/pipeline|DEV / INTERNAL|execution直链，pipeline控制面非团队运转产品|
|/execution/pipeline/[taskId]|DEV / INTERNAL|pipeline详情，非独立产品|
|/runtime-trace|DEV / INTERNAL|trace诊断，链接旧执行；不应primary|
|/company-runtime|DEV / INTERNAL|TerraNavData旧技术组；Current V1Sidebar未消费|
|/brainstorm|LEGACY|独立旧session列表；不能替Meeting|
|/brainstorm/sessions/[id]|LEGACY|旧brainstorm child；不要迁移为Meeting truth|
|/strategy-room|LEGACY|旧专题页，Current七区无入口；新策略工作归业务|
|/knowledge/memory|LEGACY|旧Memory管理；Current Knowledge非此入口|
|/finance|DEV / INTERNAL|明确planning placeholder，Current V1Sidebar无入口|
|/calendar|DEV / INTERNAL|planning placeholder；旧analytics函数有引用但未render|
|/workspace/department|LEGACY|planning placeholder，无法作为Department Leader真实工作面|
|/workspace/department/[id]|LEGACY|部门旧下钻，不代表Current领导经营闭环|
|/settings|CURRENT UTILITY|合法Settings空间，现入口主要导模型；未认证完整类别覆盖|
|/help|CURRENT UTILITY|合法帮助utility；不把文件存在当头像入口已接|

已证明的legacy escape：Business→Studio；RD→execution/tasks→execution→pipeline。仅旧代码中出现的href：analytics→calendar/execution、old organization→department detail；这些不计Current click proof。无批量退役/redirect本轮授权。

## 22 Bootstrap Drift

`RuntimeFoundation._materialize_company_in_connection`创建Company、CEO_ASSISTANT、FoundingRun状态/link；不创建supportDepartments。FirstRunDelivery在明确提案后插`business.general` Department，用旧 `official.department.software_rnd` template_ref，但名称来自提案；该引用残留不能说实际给每家公司自动建了研发业务。

另有 `CompanyProjectRuntime._ensure_default_company` 的legacy隐式default，以及`CompanyInstantiationService`的ccp软件公司包实例化。它们不是当前Welcome最终语义，不能拿其出厂研发员工做supportDepartment证据。

隔离当前库：1 Company、2 Department（都是业务部）、2 canonical Business、2 Workspace、2 company Employee；runtime有CEO_ASSISTANT 1、AI_EMPLOYEE 2、ROLE_SLOT 2、ASSIGNMENT 2、WORK 5等。这些来自先前验收安排，不是产品出厂seed证明。未显示任何credential或消息正文。

## 23 Final UI Audit Reinterpretation

I原76条评分不删除。追加独立维度：**21条已有产品/空间/投影authority drift证据，36条本项仅确认visual gap/保留态，19条authority符合性未完整验证**。这不是21个独立底层bug，多个surface共享同一root cause；36也不表示全局Shell在这些页面通过。S33领域内容仍未实机核验，只新增shared六区导航的source证据。

原判断修正：S07不可解释为退役floating；S23不能据右边稀疏删Pane；S19四块Business卡片不自动等于Business identity缺失；S68/S70 bounded native好看不等于整个Meeting/globalShell符合。详表附原Inventory；原Gap Review追加读取规则。

原58-frame范围**不是当前可直接投产的完整Master**。须先增加/整合Four-Pane default/expanded/return、Company empty-business与supportDepartments、Department/Business activation及Leader、floatingAssistant展开/收起/drag/continuity等覆盖。这里不拍新总数、不设计frame：先解决authority缺口，再由设计Owner裁定合并复用。

## 24 Critical Deviations

详见 [Deviation Register](CURIS_CORE_PRODUCT_DEVIATION_REGISTER.md)。P0为真实结构违反，不按“不好看”评级：support bootstrap/engineering responsibility入口、Studio canonical mismatch、fragmented Shell/General fixedaside、floatingAssistant、全产品完成过度注册。

### FORGOTTEN / LOST ACCEPTED RULES

除了本轮提醒：Company-level Employee无需Department前置；Functional affiliation≠Workspace assignment；Leader exception-only仅指routing；Business与Workspace复制不复制secret/history；DefaultFlow非DAG；Workstation折叠不停止员工/Handoff不强改展开；Company-wide Search≠recent-conversation search；settings归头像；模糊Intent可开始；配置/授权后返回原context；Generated/Official/Professional都不等于Verified；Context不加载全历史；Shared Employee Detail/Result按需Utility。这些应进入未来traceable验收，不强迫重写已正确Runtime。

### CONFLICTING AUTHORITY / REQUIRED RECONCILIATION

1. **长期Workspace=Professional**（C §9结果规则）与**Generic是真实可经营环境**（同文件§9.1A/B §02）。不是本轮宣布Generic非法；需产品Owner明确前者是完整专业工作能力要求还是排斥Generic形态。
2. **旧按账号Workspace示例**（M部分账号段、U三旧域路径）与**Channel≠Workspace**（C §0.1/U新channel rows）。后者有明确reconciliation，旧段应显式标例外/历史，不能继续混读。
3. **Assignment Conversation history隔离**（C §0.1/M/U）与**persistent Employee/topic跨Assignment owner**（后续CEO/Q）。可同时保留每消息scope隔离，但旧“历史不混合”对UI可见历史的定义须补明确映射；不得自行拆已验收消息。
4. **Floating拖动是Vision**（H Review）与**本轮CEO必须实现**。此项本轮明确覆盖旧Review裁决；待登记，不是继续拒绝floating的Gate。
5. **Modal只用于高风险**（B §04）与已接受StartMeeting/Recruit overlay。需限定temporary overlay≠所有modal都审批，不能根据广义禁令删除已接受启动交互。
6. **PRODUCT COMPLETE / no blocking P1**最新implementation注册与本次T03/T11/T23/T28事实不相容。这是coverage错误，不是产品允许删支撑部门的授权。

### SHOULD NO LONGER GUIDE IMPLEMENTATION

H的“拖动不是Current”旧结论；F旧GlobalAssistant Legacy标签作为删除产品能力依据；旧六区TerraNavData/WorkspacePaneShell作为导航authority；Studio固定三类blueprint/free-formbusiness-ref；旧Project-as-Business和reports sample；旧XHS Visual v4默认日历作为整个ContentGrowth的默认；视觉标准更新前绿色brand条款；把Curis_Workspace_Shell.md五槽位变体当唯一Shell；Blueprint/UI中旧Knowledge/Meeting“待实现”句当最新runtime状态。保留原文件与历史，不删除。

### Root cause — evidence, not author speculation

|证据|能够支持的根因|不能声称|
|---|---|---|
|Organization review明确只测两部门/两Business fixture与read projection|局部关系展示验收遗漏freshCompany组织形成|不是证明某开发者故意删department|
|September8同段PRODUCT COMPLETE复制到多个current载体|路径级验收被放大为整个product合规|不是撤销所有测试PASS|
|TerraShell与WorkspacePaneShell独立导航数组|shared seam没有统一消费currentnav|不是所有专业域Runtime消失|
|Studio current入口仍提交旧ref|legacy保留但未验证新旧边界incominglink|不是数据库已写入orphan|
|F候选foundation叫floating legacy；I沿用退役措辞|实现宿主退役与产品能力退役混淆|不能说所有历史拖动细节已Frozen|
|Pointer存在#32/#45但旧/新状态叠加|入口有，逐规则验收与supersession不够|不能一律归因Pointer缺失|
|有限Figma注册/截图覆盖，source-only行仍多|Design/state coverage不完整|不能推测会话交接中谁丢失了哪一行|

会话交接丢失原始操作因果：UNVERIFIED；没有作者/hunk证据，不对WorkBuddy/Codex个体归责。bounded任务本身有保护价值，问题是缺总合同交集复验。

## 25 Recovery Plan

|Phase|边界/产出|Gate|
|---|---|---|
|A Authority Repair|产品Owner裁决上列明确语义；只修既有Authority/Pointer适用范围；将全产品完成收窄为accepted chains + coredrift|CEO/ChatGPT接受；此轮只提议未改Current|
|B Core Product / Runtime Reconciliation|默认支撑Department/责任的同canonical bootstrap；补专业建设/analyst ownership接线；修Studio canonical父关系与OperatingDirectory入口；不造新模型|isolated freshCompany空业务+支持组织、真实assignment、reuse、restart/failure；无假员工|
|C Final UI Master|以已恢复FourPane/三空间/七区/浮层为基础；重新覆盖58frame遗漏，保留accepted域结构|设计Owner逐规则traceability；不是再探索产品理论|
|D Frontend Reconciliation|最小统一Shell/导航、浮层宿主、专业detail/return、legacyescape封口；复用真实Runtime|Browser+freshDesktop+restart；不能只有静态卡/截图|
|E Release Acceptance|freshCompany无fixture全链、支持组织、业务启用、专业/Generic、跨区、能力边界、DB安全；再看分发|产品验收与发布授权分别通过；目前未授权|

KEEP AS-IS：canonical Business/ParentResolver/atomic/quarantine；EmployeeIdentity/callback/Usage；Work/Result/Evidence/Decision；Conversation owner/message/idempotency/ViewReceipt；Knowledge引用；Meeting已验收核心；General lifecycle；Package v1/v2有限renderer及migration。禁止借审计重写。

### Read-only / preservation record

HEAD `bb72916daba3ae9555914d03bdb7fcea9953ab9c`。接管733项：125 modified、2 deleted、606 untracked；staged=0。未stage/commit/push/reset/clean/stash；不处理其它initiative。只新增本次3份review并append既有2份audit；没有Current/Pointer修改。检查方法仅代码/文档读取和stdlib SQLite immutable只读，没有Runtime import/测试/新截图/Provider调用。

|Protected SQLite|size|mtime_ns|SHA256|integrity|
|---|---:|---:|---|---|
|`data/curis.sqlite`|1232896|1786873339955841838|`2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`|ok|
|`backend/data/curis.sqlite`|1277952|1786783659967572836|`a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`|ok|
|`/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite`|1536000|1788614881473263746|`d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617`|ok|

本轮开始、中间及交付前复核完全相同：三个受保护DB的size、mtime_ns、SHA256未变化，integrity_check均为ok。交付前staged=0，工作树736项（原733项加本次3份报告），git diff --check通过。主报告不展示用户credential/消息正文。旧native evidence来自I明确列出的isolatedroot，不当freshCompany默认事实。

### Verdict

CORE PRODUCT MODEL: DRIFTED

CORE ORGANIZATION MODEL: DRIFTED

CORE SPATIAL MODEL: DRIFTED

FUNCTIONAL CAPABILITIES / FUNCTIONAL PRODUCT: PARTIAL against the complete current product contract; accepted scoped implementation remains accepted.

FINAL UI: NOT READY

RELEASE: BLOCKED; distribution technical preparation is not product acceptance.

NEXT: PHASE A — AUTHORITY REPAIR, then bounded core product reconciliation; no implementation started.

STOP FOR CEO / CHATGPT CORE PRODUCT REVIEW.
