# Curis Phase B Core Product Reconciliation Contract

Status: Review
Authority Class: REVIEW / IMPLEMENTATION CONTRACT CANDIDATE
Disposition: PHASE B P0 IMPLEMENTATION CONTRACT FINAL CANDIDATE — NOT IMPLEMENTATION AUTHORIZATION
Date: 2026-09-09
Owner: Main Development / Integration; Product decisions: CEO / Product Owner
Source: [accepted Phase A registration](CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md), existing Frozen authorities, Core Product Deviation Register.
Next Gate: CEO / ChatGPT Phase B final review, then approved bounded Issue with exact Allowed Files / owned hunks. Employee decomposition gate CLOSED by CEO decision. PHASE B IMPLEMENTATION NOT STARTED.

## Phase A.1 amendment — 2026-09-09

Source: CEO BUILT-IN OPERATING ORGANIZATION及ROLE DECOMPOSITION decisions；[Authority Repair A1](CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)。定义→Company实例→Assignment Holder分离。freshCompany空间工程必须6个不同Employee实例：空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家；各自对应官方Definition。数据分析部至少1 Company Analyst，默认显示名司衡可编辑，主要工作面经营洞察。不是只seed部门，也不能用1人兼任六岗代替初始六人；不把Prototype姓名当官方名单。
开工前审计现有employee/role templates、capability definitions、seed/catalog、official定义载体并复用。若需新canonical Official Employee Definition primitive/schema，STOP FOR ARCHITECTURE REVIEW；本合同不授权新表。Definition不是第二Employee运行真源；现有实例、关系、Execution Identity/绑定继续使用。

## 1. Goal and no-rewrite

纠正完整Company组织/经营入口/空间壳合同与已验收底座之间的接线缺口，不建设第二套Company、Employee、Conversation、Usage、Attention、Package、Workflow或Runtime。
KEEP：canonical Business spine/Parent Resolver/atomic validation、Employee identity、Conversation、Usage、Result、Attention、Knowledge、Meeting core、General lifecycle、Package runtime、P7、Work/Execution。已有Acceptance按原范围有效。

## 2. Minimal P0 implementation slices

|ID / deviation|Bounded change|Candidate ownership boundary (not an Allowed Files grant)|Acceptance|
|---|---|---|---|
|P0-A / D01|COMPANY BOOTSTRAP + BUILT-IN OPERATING ORGANIZATION：Company/CEO/same Assistant/两原装部门/official Employee实例/Role/Responsibility/Assignment同一可恢复bootstrap；用户Business可0|既有foundation.py、first_run_delivery.py、Employee物化/目录调用seams；先确认已有载体、六官方定义的技术映射和exact owned hunks；不新增系统|freshCompany空间工程6个不同真Employee/对应真关系；数据分析部至少1Company Analyst；无默认用户Business；不依赖Key；缺Provider仍创建但显示不可执行；retry/restart无重复，失败不冒充组织完整|
|P0-B / D02|BUILT-IN RESPONSIBILITY + WORK SURFACE INTEGRATION：空间工程团队、Company Analyst、Organization、Operating Intelligence、Business activation|既有组织/Analyst projection、责任/Assignment、Employee Detail/Edit与Work Surface消费者；不得按role文本选人|原装Team可见、分析师身份可见、缺业务数据诚实说明；空间工程已存在再接CEO意图；合法Work/Package/Result引用；Requirement与Holder分离，Reviewer/Handoff/P7保持|
|P0-C / D03|业务启用先读Company、复用/提案、合法Department→Business；修Studio/新增Workspace canonical seam|frontend/app/ceo-office/business/page.js、workspace/page.js、workspace/studio/page.js；最小runtimeApi seam（必要时）|新增Workspace只引用现存Business；无free-form/default Project；Business+firstWorkspace原子；空业务有入口；无效父关系拒绝、无孤儿；不把Package安装当经营完成|
|P0-D / D04|复用WorkspacePaneShell行为，收敛TerraShell/General的职责接线，不推翻专业域工作面|frontend/components/workspace/WorkspacePaneShell.js、frontend/components/terra/TerraShell.js、GeneralWorkspaceOperating.js真实位置及直接消费者|Nav+Main独立；Context/Utility按需、真实pointer resize、Pane-local headers、T1–T3、maximize/recover；无固定空白预留；关闭Pane不改Execution|
|P0-E / D05|现有GlobalAssistant host加入最低floating/drag/collapse/cross-area能力；同identity/持久Conversation|frontend/components/assistant/GlobalAssistant.js及既有shared host/Assistant holder consumer|跨七区不销毁、不占Pane、真实可拖动；同Conversation无重复消息/Usage；合法context；不会被Sidebar替代；restart保持既有对话|
|P0-F / D06|Current completion scope correction|本Phase A文档治理已完成；Phase B仅按真实验收更新|不得再次以局部PASS宣称全合同完成；不是新增代码任务|

A/B可作为同一有界支撑组织Issue；D/E可共享host集成验证，但不得整文件吸收未知hunks。P0-B不是一次建设完整自动空间工程系统：最低证明合法组织/责任承接、已有Work/Package结果和交付引用；完整行业研究质量、市场及任意生成能力不纳入。
P0-E不以未定snap/精确尺寸/位置记忆为前置；最低拖动规则已有授权，样式细节留Final UI Master。P0-D是行为合同接线，不要求提前重画七区。

## 3. P1 candidate queue

|Candidate|Minimal acceptance / boundary|
|---|---|
|Global navigation / search / identity（D07）|七区唯一来源；Company范围对象搜索与CEO/settings真实入口；advanced/semantic search非本轮承诺|
|Department/Business Leader operating entry（D08）|现有Assignment证明责任；Organization维护结构，Business Space进入工作；不造Router|
|Analyst Assignment ownership（D09）|最低原装Analyst及canonical归属已并入P0-B，不再延到P1；更广Business allocation保留P1，指标真源不改|
|Professional identity / return（D12）|Generic合法；Channel≠Workspace；旧XHS兼容保留；不重做域Runtime或自动新增CG产品|
|Legacy route escapes（D11）|逐消费者将用户返回canonical surface；历史deep link保留；不批量删route|
|Employee / Result spatial projection（D10）|Main Workstation、Utility detail/Result、P6/P7保留；Viewed≠Accepted；同Conversation回返|
|Knowledge reference UX（D13）|reading/reference/return语义，不建RAG或新引用系统|
|Capability ordinary language（D14）|仅投影用户语言，UNKNOWN/UNSUPPORTED保留，不改权限/Provider|
|Authority consistency（D15）|本Phase A裁决已记录；后续仅核对消费者，不重开产品研究|

D16及Assistant数值、Dark/1024、完整accessibility、position memory、未来connectors继续P2/UNRESOLVED，不升P0。空间工程六定义/六初始实例与数据分析最低1员工已确定；固定Workspace、部门删除政策未定。用户后续编辑/替换Holder/增减人员合法，不把初始人数当永久锁定。

## 4. Engineering gates before source changes

1. 独立Issue定义exact Allowed Files、owned functions/hunks、输入输出和验收；当前表是候选边界，不允许扩大。
2. 读HEAD/staged/unstaged/untracked、每个owned file pre-change hash，保留mixed-source。冲突文件停止，不覆盖。
3. 三个protected DB：repo data、repo backend data、default App DB。before/after size、mtime、SHA256、integrity一致。所有runtime tests先将CURIS_DB/CURIS_DB_PATH/CURIS_WORKSPACE_DB设同一repository-external isolated DB，使用既有fail-fast guard。
4. 不自动启动默认App，不迁移/补种活动库。历史Company若需补部门：只在隔离fixture证明策略；活动数据执行须另授权。ambiguous mapping停止，不能猜部门。
5. 需要新Schema/primitive、第二真源、权限绕过或未知ownership：STOP exact gate，不扩大。
6. 不做git add/commit/push/reset/clean/stash；后续如需提交另授权。

## 5. Acceptance matrix

- New Company：CEO identity、same Assistant、两原装部门、空间工程实际员工、至少1真实Company Analyst、Role/Responsibility/Assignment、合法Work Surface；经营Business=0。Organization有真组织而非空壳/fixture，Insights显示真Analyst及无业务/数据状态。
- Exact fresh staffing：空间工程6个不同canonical Employee ID，对应6个已裁决Official Definitions；数据分析至少1独立Company Analyst；不含CEO Assistant、不以Assistant/一人多岗代数。跨Company共享Definition来源但不共享Employee instance identity；不得默认Content Growth/RD Business。
- Provider boundary：无Key/无Model绑定仍能创建Company和Employees；Execution Identity与Capability缺口真实可读；不得假绑定、硬编码凭证或要求先配模型。
- Idempotency / failure：并发、retry、同root restart不重复department/assistant/employee/assignment；同一可恢复bootstrap保持原子或明确未完成恢复状态，不展示假完整；无半创建Business。
- Employee Edit：原装与用户Employee共用现有Detail/Edit；修改至少一个已支持字段→restart→same Employee ID及修改保持。bootstrap恢复不得重置用户name/avatar/已支持配置，不因改名丢失Analyst/Leader解析。
- User staffing changes：若用户合法增减人员/替换Holder，Requirement继续存在，缺口如实呈现；restart不得恢复固定初始人数、重复物化已处理定义或覆盖新Holder。bootstrap完成与用户后续变更须可区分，未完成恢复不得伪装完整。
- Responsibility continuity：V1若支持official Employee A→user Employee B，测试Requirement持续、Holder合法变化、历史Work/Result不改写；不支持则记录后续，不能借此扩Runtime。缺Holder显示组织能力缺口。
- Organization：真实Role/Responsibility/Assignment与Employee映射；vacancy/risk不由人数或WAITING推断；Analyst不靠名称。
- Business activation：Company读/reuse/propose/gate/canonical parent/atomic firstWorkspace；direct CEO和delegation均不强制DAG；invalid parent fail-closed。
- Spatial：真实Browser和fresh packaged pointer操作；七区/专业/Generic代表路径；Nav+Main、Context/Utility、headers/resize/maximize/recover；不强制四列。
- Assistant：same holder/conversation，跨区、拖动/收起、合法context、真实已支持回复路径；不虚构成功或重新造Usage。
- Reference/restart：Conversation/Result/Decision/Work identity与返回保持；Viewed不复活、Execution无假running。
- No-regression：canonical spine、Organization/Employee、RD/XHS、General、Package、Conversation/Usage/Attention、Knowledge、Meeting core existing tests；不重开Meeting cloud multi-cycle。
- Focused backend/frontend、compile、lint/build；Browser不能替代fresh packaged Desktop，screenshots不能替代Runtime/persistence evidence。
- Production capability proof不得用fixture冒充；fixture仅证明指定隔离关系。无外部connector时保留真实缺口。

## 6. Delivery / exit

每个bounded Issue提供changed files / owned hunks、tests、Browser/Desktop、restart、DB fingerprints、Remaining gaps与Review verdict。Phase B须真实完成built-in organization、official Employees、Business activation、Four-Pane、floating Assistant才建议恢复Final UI Master；设计恢复仍需CEO/Design确认，不等于发布授权。
Final UI增加初始原装组织/无用户Business、空间工程Team、数据分析Team及Insights入口、Official Employee Detail/Edit、User-created Employee对照。沿用同Employee模型及Main Conversation+Utility detail，不画第二套Built-in UI。
Final UI输入：Authority Repair→Blueprint→Shared→Shell→UI Blueprint→Visual Standard→Inventory→Gap Review。有限视觉frame不能覆盖整个产品合同。
RELEASE保持BLOCKED，直到后续整体验收/授权；本合同READY只表示可评审，不表示实现完成。
