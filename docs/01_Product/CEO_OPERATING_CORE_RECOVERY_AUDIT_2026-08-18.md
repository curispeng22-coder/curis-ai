# CEO OPERATING CORE RECOVERY AUDIT

**Status:** ACCEPTED — CEO OPERATING CORE RECOVERY BASELINE  
**Authority Class:** REVIEW  
**Disposition:** CONSUMED BY CURRENT PRODUCT TRUTH（Business Exit / CEO Operating Day Cross-day Continuity）  
**日期：** 2026-08-18  
**范围：** 历史 CEO 经营推导与当前 Product Truth 的只读对照  
**结论状态：** CEO OPERATING CORE RECOVERY AUDIT — ACCEPTED / REGISTERED — CONSUMED BY CURRENT PRODUCT TRUTH

**CEO 接受说明：** 本审计作为后续 Product Architecture 最终收口的正式输入，不是 Product Authority，不覆盖 Current Blueprint；除非出现新的历史材料或 CEO 明确要求，不重复进行同范围历史经营内核考古。

## 0. 审计结论先行

本轮没有修改 Product Blueprint、Master Map、UI Blueprint、Runtime、Schema、数据库或代码；只生成本审计文件。

历史经营内核没有整体丢失。当前产品已经安全保留了最重要的经营闭环：

```text
CEO 意图 → Company / Business → 责任与能力 → Workspace 工作
→ 外部结果 / 反馈 → Evidence / Acceptance → CEO Decision
→ Change / Learning → 下一轮经营
```

丢失风险集中在两个“连续性契约”上，而不是少了两个页面：

1. **Business Exit 的完整经营动作语义**（Reduce / Transfer / Close / Merge / Split，以及退出前保护承诺、交接、释放资源、保留历史的统一规则）在 Current 中没有完整承载位置；当前只有暂停、调整、替换、关闭等零散动作。
2. **CEO Operating Day 的持久化连续性语义**（一天的 Brief、Matters、Handoff、Decision、Exception、Evidence、Learning、Closeout 以及未完成责任承接到下一天）在 Current 中被 CEO Desk / Assistant 的日常体验承载，但没有完整的跨日经营合同。

这两项先标为 **ACCIDENTALLY LOST**，只提交 CEO Review，不在本轮恢复页面或 Runtime Primitive。其余核心判断主要是 PRESERVED 或 EVOLVED；高级组合经营、完整经济模型、跨业务资源优化和外部指标适配属于 LATER。

### 研究边界

- `docs/01_Product/Curis_Product_Derivation_Journal.md` 与 `docs/01_Product/Curis_Product_Reasoning_Record.md` 是本轮历史推导依据，不是 Current Authority。
- 当前对照文件是唯一 Product Blueprint、唯一 Master Map、唯一 UI Blueprint、`PRODUCT_DOCUMENT_POINTER.md` 与 `CURRENT_STATE.md`。
- `deliverables/product-strategy/CURIS_OPERATING_INTELLIGENCE_RESEARCH.md` 已读取，但它位于 `deliverables/`，不在 canonical `docs/` 产品文档链中，且状态为 Research / STOP FOR CEO REVIEW；其“Operating Intelligence”统一命名和 Runtime Gap 不能直接覆盖 Current。
- `docs/03_Design/CURIS_COMPANY_MAP_ORGANIZATION_GRAPH_RESEARCH.md` 与 `CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html` 作为公司版图研究输入；研究阶段未写回 Current Authority，现已由 Final Product Architecture Delta 消费为产品/交互方向。

## 1. 审计方法与分类纪律

每条历史判断都按“历史来源 → 当前合法承载 → 分类”核对：

- **PRESERVED：** 经营原则已经进入 Current，未丢失。
- **EVOLVED：** 原则保留，但被更成熟的产品模型、语言或层级替代；不恢复旧模型。
- **LATER：** 仍成立，但基础经营闭环之外，等触发条件成立后再 Review。
- **SUPERSEDED：** 有明确的后续 Current / Frozen 来源正式推翻；不以“当前没看到”代替证据。
- **ACCIDENTALLY LOST：** 历史判断成熟、没有正式 Supersede，Current 又没有合法承载位置；本轮只报给 CEO。
- **ORPHANED PRODUCT REASONING：** 历史上形成过有价值的推导，但从未成为正式 Current 规则；不自动恢复。

页面缺失不等于经营逻辑丢失。Evidence、Capacity、Commitment、Failure 等可作为跨产品真相、责任约束或状态语义存在；只有 Current 无法回答“这条经营判断由什么承载”时，才进入 ACCIDENTALLY LOST。

## 2. 总表

| Historical Operating Principle | Historical Source | Current Mapping | Classification | Current/Lost Location | V1/Later | Recommendation |
|---|---|---|---|---|---|---|
| Curis 是帮助 CEO 建设、经营、扩展一人 AI 公司的 Company OS | Derivation Journal §4、§19；Reasoning Record §2 | Blueprint 5.2 产品身份、Company OS 固定 / Workspace 开放 | PRESERVED | Blueprint §01；Pointer；CURRENT_STATE | V1 Foundation | 保留，不恢复旧模块目录 |
| CEO 的五个经营问题：公司现状、业务价值、能力供给、工作分配、共识与知识 | Derivation Journal §2；Reasoning Record §1 | 六个产品空间 + 跨层 Truth / Decision / Result / Insights | EVOLVED | Blueprint §03、§05、§10–§12；Master Current Contract | V1 Foundation | 继续用经营问题检查产品，不创建“五个问题”页面 |
| 从零创建到持续经营的生命周期 | Derivation Journal §5；Reasoning Record §3–§4 | 意图 → 最小 Company / Business → 员工与能力 → Workspace → 结果 → 验收 → 决策 → 下一轮 | PRESERVED | Blueprint §02、§05、§12；Master 生命周期合同 | V1 Foundation | 作为所有一级区域的共同闭环 |
| 公司循环与价值循环在 Outcome / Decision 处相交 | Derivation Journal §17；Reasoning Record §4 | Business Goal、Result、External Feedback、CEO Decision、Change / Learning | PRESERVED | Blueprint §05、§11–§12；Master Business / Result / Decision | V1 Foundation | 不创建第二套价值或战略系统 |
| 公司不是任务集合，而是承诺网络 | Derivation Journal §8；Reasoning Record §5 | Commitment 是高级经营对象；Task / Cycle 是执行载体；Acceptance 独立于完成 | EVOLVED | Master §14 用户可见生命周期、Meeting / Commitment / Cycle；Blueprint §12 | V1 Foundation（最小承诺）/ Later（网络化） | 保留责任、范围、检查点和验收；完整承诺网络后置 |
| 外部结果必须来自外部系统或 CEO 可信手动回填 | Derivation Journal §9；Reasoning Record §6 | External Result / Feedback 与来源、可信度、Unknown、Manual Entry；外部系统保有原始事实 | PRESERVED | Blueprint §11；UI Result / Insights；Master Result / Insights | V1 Foundation | 所有首批 Workspace 都必须走真实来源或人工回填 |
| 任务完成不等于价值成立，必须 Evidence → Acceptance | Derivation Journal §8–§9；Reasoning Record §5–§6 | Evidence、Result、CEO Acceptance、Decision 分离 | PRESERVED | Blueprint §12；Master §14 生命周期；UI Meeting / Result | V1 Foundation | 禁止用完成状态代替价值判断 |
| Decision 必须改变后续行动并回到下一 Cycle | Derivation Journal §5、§17；Reasoning Record §4、§15 | CEO 可继续、调整、暂停、替换、拒绝；变化回写 Business / Employee / Capability / Workspace | PRESERVED | Blueprint §12；Master Decision / Change；UI CEO Desk / Meeting | V1 Foundation | 保留来源、影响、Owner、下一检查点 |
| Capability 与 Capacity 不同；有能力不代表有可用容量 | Derivation Journal §10；Reasoning Record §7 | Capability 是公司资源；Role / Employee / Workspace 有 Capacity / Load；健康、成本、权限和供给可阻塞运行 | EVOLVED | Blueprint §05–§08、§10；Master Role / Capability / Settings | V1 Foundation（最小供给检查）/ Later（组合优化） | 继续显示负载与供给缺口，不做企业级资源计划软件 |
| 资源冲突本质是承诺冲突，应说明影响和取舍 | Reasoning Record §5.3、§7；Derivation Journal §10 | Company / Business / Workspace 的成本、权限、容量、风险与 CEO 确认 | PRESERVED | Master §16、§18、§20；Blueprint §05、§12 | V1 Foundation | 进入决策影响预览，不新增资源调度中心 |
| AI 员工是有身份、岗位、责任和边界的责任主体 | Derivation Journal §11–§12；Reasoning Record §8、§18 | Expert → Employee；Role / Responsibility；Model / Agent / Skill / Tool / Knowledge / Connector / Permission 是供给 | PRESERVED | Blueprint §06–§08、§10；Master Employee / Role / Capability | V1 Foundation | 继续把 AI 员工而非聊天机器人作为工作主体 |
| 组织从真实责任和能力缺口中成长，Department 不是第一天前置 | Derivation Journal §12、§14；Reasoning Record §3.2、§11 | Company → Department → Business → Operating Model → Role → Employee Binding；可直接 Company 级员工 / Role / 临时团队 | PRESERVED | Blueprint §05；Master Company Map；Company Map Research | V1 Foundation | 不恢复强制建部门或传统 HR 图 |
| AI 团队有汇报关系：CEO → Assistant → 专业 AI → Workspace AI | Derivation Journal §20–§24；Reasoning Record §16、§18 | CEO Assistant 是 Company-level 第一位 AI 员工；专业员工与 Workspace Workstation 分层 | EVOLVED | Blueprint §10；Master Employee / Workspace；UI Workstation | V1 Foundation | 保留责任升级链，不把内部层级做成平级 Agent 目录 |
| CEO Assistant 是 Chief of Staff，不是聊天按钮 | Derivation Journal §20–§24；Reasoning Record §16、§18 | Assistant 负责简报、提醒、准备、委派、跟进、恢复和连接历史；不替 CEO 做高影响决定 | PRESERVED | Blueprint §10；Master Assistant / CEO Desk；UI Global Capability | V1 Foundation | 继续以 CEO Desk + scoped Assistant 承载 |
| CEO Operating Day 是验证 Curis 的最小体验单位 | Derivation Journal §21–§26；Reasoning Record §16 | CEO Desk 每日简报、变化、风险、待处理、下一决定；Assistant 在关键处介入 | EVOLVED | Blueprint §02、§10–§12；UI CEO Desk / Global Capability | V1 Foundation（体验）/ Later（完整持久化） | 不新增 Operating Day 页面；见 ACCIDENTALLY LOST 的连续性缺口 |
| CEO 需求分为 Assistive、Operating、Decision、Coordination、External Commitment | Derivation Journal §22；Reasoning Record §16 | Assistant 对低风险请求轻量处理；改变公司状态、外部副作用或高影响资源时进入确认链 | PRESERVED | Blueprint §10、§12；Master Decision / Attention | V1 Foundation | 继续用影响分级，不把所有请求变成 Goal / Task |
| CEO 注意力是有限资源，低影响进度应聚合或静默 | Derivation Journal §20–§23；Reasoning Record §16 | CEO Desk 只突出变化、异常、待处理、需要决定；Assistant 不制造二次任务系统 | PRESERVED | Blueprint §02、§10；Master §18.1；UI CEO Desk | V1 Foundation | 保留为什么现在、影响、最小 CEO 动作 |
| Workspace 只有在重复交付、多员工、独立能力/数据/权限/异常/验收出现时成立 | Reasoning Record §9；Derivation Journal §38–§41 | Workspace = 专业业务办公室 + Employee Workstations + 自动协作 + 结果反馈；轻量 Conversation / Task 不强制升级 | PRESERVED | Blueprint §08；Master Workspace Contract；UI Workspace | V1 Foundation | 保持“Company OS 固定、Workspace 开放” |
| Workspace Studio 先理解业务，再装配团队、能力、工具、资料、外部系统和结果 | Derivation Journal §39–§41；Reasoning Record §18 | Studio 是创建、复制、修改、影响预览、测试、确认、恢复的装配空间，不是自由 DAG | PRESERVED | Blueprint §08、§13；Master Workspace / Studio；UI Studio | V1 Foundation | 不让 Runtime 页面反过来定义 Workspace |
| Business Template / Duplication 复用 Operating Model，不复制身份、凭证、执行、历史 | Derivation Journal §15、§39；本轮 Duplication Delta | Copy Preview → 独立 Business Identity → 同一 Company Map / 新 Workspace | PRESERVED | Blueprint §05；Master Business Duplicate；UI Business Detail | V1 Domain Validation | 三业务样板使用同一复制边界 |
| 失败必须分类、隔离影响、恢复、验证、关闭并学习 | Derivation Journal §13；Reasoning Record §10 | Result / Failure / Unknown / Stale / Conflict；原工作现场提供继续、重试、回退、转派、暂停 | PRESERVED | Blueprint §04、§08、§12；Master §14；UI 状态与恢复 | V1 Foundation | 不能以绿色卡片或 200 响应代替事实 |
| 业务退出有不同含义：Pause / Reduce / Transfer / Close / Merge / Split | Derivation Journal §13；Reasoning Record §10.4 | Current 只分散出现暂停、关闭、替换、组织合并/拆分；没有完整 Business Exit 语义 | ACCIDENTALLY LOST | 没有一个完整 Current Contract；Master 的组织合并/拆分不能替代业务退出 | V1 Foundation 的最小暂停/关闭；完整动作 Later | CEO 决定是否在下一次 Blueprint Delta 恢复为跨层生命周期规则；不要先建 Exit 页面或 Primitive |
| 公司成熟度逐步激活：创始、首次价值、可重复运行、委托经营、业务组合、重构扩展 | Derivation Journal §14；Reasoning Record §11 | Founding / First Value / Repeatable Run / Progressive Department / Workspace / Growth | EVOLVED | Blueprint §02、§05、§12；Master 生命周期 | V1 Foundation（前两阶段）/ Later（组合与重构） | 以真实结果触发复杂度，不要求第一天填满公司 |
| Business Economics 应把 AI 成本与验证结果、外部价值联系起来 | Reasoning Record §7.3；Derivation Journal §10 | Insights 已要求 Usage / Cost / Acceptance / Result Quality / External Business Metrics，并带 source / freshness / unknown / manual | PRESERVED | Blueprint §04；Master Insights；Operating Intelligence Research 作为研究补充 | V1 Foundation（事实链）/ Later（完整经济模型） | 不把成本数字直接当价值；完整单位经济学另行 Review |
| 模型 / Agent 选择要比较质量、验收和外部价值，不能只比 Token | Reasoning Record §7.3、§18；Operating Intelligence Research §10 | Insights 合同可按 Model / Agent / Provider、Result、Acceptance、External Result 比较 | EVOLVED | Blueprint Insights；Master Insights | Later（真实 Benchmark 数据集和跨样本可比性） | 先保留比较语义，未有数据不得显示排行榜 |
| 日历 / 节奏 / Schedule 是业务节奏投影，不是公司主导航 | Derivation Journal §7、§21、§40；Reasoning Record §20 | Workspace 自己决定 Trigger / Schedule；内容 Workspace 有日历，CEO Desk 只显示下一检查点 | EVOLVED | Blueprint §08、§10；UI XHS/TTK 与 Automation | V1 Domain Validation / Later（统一排程） | 不恢复 Scheduler / Calendar Center |
| 资料、知识、学习和历史应成为下一次决策可引用的公司记忆 | Derivation Journal §2、§9、§12；Reasoning Record §1、§12 | 资料库负责来源、索引、引用、权限和沉淀；Employee Growth / Lessons 与 Review 回写 | PRESERVED | Blueprint §09、§11–§12；Master Library / Employee / Result | V1 Foundation | 与 Truth / Decision 关联，不建立孤立 Knowledge Center |
| Meeting 不是聊天存档，而是事实、分歧、提案、Decision、责任和跟进 | Derivation Journal §21、§25；Reasoning Record §12、§17 | Company / Workspace Meeting；Conversation → Proposal → CEO Decision → Owner / Checkpoint → Result | PRESERVED | Blueprint §11；Master Meeting；UI Meeting | V1 Foundation | 会议结果必须回到原 Business / Workspace |
| 经营分析、数据洞察、报告、成本、质量和外部结果应共同支持 CEO 决策 | Derivation Journal §2、§17、§21；历史 Product Bible 仅作背景 | Current 已恢复数据洞察空间；它消费已有 Truth / Result / Usage / Cost / Feedback，不创建第二套事实 | EVOLVED | Blueprint §04；Master Insights；UI Insights | V1 Foundation（产品合同）/ Later（采集和 Report Runtime） | “Operating Intelligence”统一命名仍只属 Research，待 CEO 决定 |
| Company Map 以业务 WHAT 为骨架，WHO 通过 Role / Employee 下钻 | Derivation Journal §12；Company Map Research §5–§8、Visual Exploration | Company → Department → Business → Operating Model → Role → Employee Binding；Employee Directory 反查 | EVOLVED | Blueprint §05；Master Company Map；研究文件只补表达 | V1 Foundation | 不恢复旧自由关系图或 HR Org Chart |
| 外部系统负责原始执行，Curis 负责经营事实、责任、解释和决策 | Derivation Journal §9；Reasoning Record §6 | Connector / Provider / Workspace 负责接入；Curis 保存来源、权限、结果、反馈与 CEO 决定 | PRESERVED | Blueprint §01、§06–§12；Master Connector / Result | V1 Foundation | 外部平台数据未接通时显示待连接 / 手动回填 / 未知 |
| 公司经营需要规划周期、检查点和资源取舍 | Derivation Journal §2、§5、§14；Reasoning Record §3、§11 | Goal、Business、周期、下一 Review、Commitment、CEO Attention 具备最小承载；公司级长期规划未独立成契约 | LATER | 当前可由 Business / Commitment / Review 承载，组合规划尚不完整 | Later | 进入多 Business、投资或资源竞争时重新 Review |
| 跨业务的完整容量规划、预算、投资组合和资源最优分配 | Derivation Journal §10、§14；Reasoning Record §7、§11 | 当前有 Capacity / Load、成本和影响预览，但没有组合级优化模型 | LATER | Role / Employee / Business / Insights 的局部字段 | Later | 出现多个业务争夺共享员工、模型或预算时建立专项 |
| 完整 Promise / Obligation 网络、重新协商和违约处理 | Derivation Journal §8；Reasoning Record §5 | 当前有 Commitment、负责人、Evidence、Acceptance、Decision；完整网络和谈判模型未成为普通用户主路径 | LATER | Master Commitment / Meeting / Decision；没有独立承诺网络空间 | Later | 外部客户、伙伴或多方承诺真实出现时 Review |
| 完整外部指标适配、Observation、Report 和主动洞察 | Operating Intelligence Research §2、§4、§7、§13（Research） | Product Defined 的 Insights 合同已存在；Runtime 仅有部分 Usage / Cost，外部数据、Report、主动洞察未交付 | LATER | Blueprint / Master / UI Insights；研究文件记录 Runtime Gaps | Later | 先有一个 Business 的真实外部数据源，再建立 Metric / Report 专项 |
| 完整 CEO Operating Day 持久化对象与跨日 Closeout | Derivation Journal §21；Reasoning Record §16 | 当前有 CEO Desk / Brief / Matters / Timeline / Closeout 体验语义，但没有完整跨日承接合同 | ACCIDENTALLY LOST | Current 没有单一“跨日责任承接”规则；不是缺少一个页面 | V1 Foundation 的连续性应先确认；完整对象 Later | CEO 决定是否恢复为跨层连续性契约；不要直接新增 Operating Day Runtime |
| 第一项研发任务固定为“完善 Curis” | Reasoning Record §13；Derivation Journal §16 | Current 明确研发 Workspace 只定义通用能力，任务由 CEO 创建；旧名称仅可作历史 dogfood 证据 | SUPERSEDED | PRODUCT-002、CURRENT_STATE、Blueprint §08 / §13 | 不再恢复 | 保留历史证据，但禁止默认任务和硬编码 |
| 旧五层 / 四入口 / 技术 Console 作为普通用户主导航 | Derivation Journal §2、§6、§17 的中间方案 | ADR-0045、Blueprint 5.2、Master v3.0 已收敛六区 + scoped spaces；Runtime / Workflow / Gate 下沉 | SUPERSEDED | ADR-0045；Pointer；Blueprint / Master Current Contract | 不再恢复 | 继续以当前组织阅读模型为准 |

## A. PRESERVED：已经安全进入 Current

以下是本轮确认无需恢复的经营内核：

1. Company OS 固定、Workspace 开放；普通用户从 CEO 意图进入业务与工作，而不是从 Runtime 对象开始。
2. 外部结果真实来源、人工回填、Evidence、Acceptance、CEO Decision 和下一轮 Change 的闭环。
3. CEO Assistant 作为第一位 AI 员工 / Chief of Staff，负责观察、准备、提醒、协调、跟进和升级，不替 CEO 做高影响决定。
4. 责任优先的 AI 员工、渐进式组织、Department / Shared Service 由真实责任与共享能力形成。
5. Workspace 的成立条件、专业工作面、Employee Workstation、Studio、能力缺口与恢复路径。
6. Failure、Unknown、Stale、Conflict、权限、成本、副作用和审计必须如实表达。
7. Business Duplication、资料库、会议、外部系统关系和结果学习。
8. 数据洞察作为跨层消费面已恢复；这次审计不把研究中的 Operating Intelligence 名称直接升格为 Current。

这些判断已经有合法产品承载位置，不需要因为没有同名页面而“补回旧模块”。

## B. EVOLVED：旧模型没有丢，只是被更成熟模型替代

| Old | Current | 为什么是演进，不是丢失 |
|---|---|---|
| 五个 CEO 经营问题 / 四个入口 | 六个一级产品空间 + CEO Desk / scoped Insights / Assistant | 经营问题被分布到产品空间，Truth / Decision / Result 横跨所有空间；原问题仍能回答。 |
| 三个经营引擎 + 一个控制面 | Company OS 固定、Workspace 开放、结果与决定回流 | 原来的分层变成产品责任边界，不再要求用户理解“引擎”。 |
| Promise / Obligation / Commitment / Task 三层 | 普通用户语言为目标、这轮承诺、工作、结果；高级面保留 Commitment | 责任与验收仍在，只是避免内部对象统治导航。 |
| 责任→能力→组织图 | Company→Department→Business→Operating Model→Role→Employee Binding | Company Map 研究进一步确认“WHAT 为骨架、WHO 按需下钻”。 |
| CEO Operating Day | CEO Desk + Assistant Brief + Matters + Timeline + Closeout 体验 | 日常入口保留；缺口是跨日持久化合同，不是旧页面应恢复。 |
| Capability / Capacity / Allocation | 能力中心与员工/Role/Workspace 的供给、负载、成本和影响预览 | 最小经营判断可用；跨企业组合优化属于 Later。 |
| 公司成熟度 | Founding → First Value → Repeatable Run → 渐进组织 / 业务成长 | 阶段仍存在，但不以成熟度中心或额外导航呈现。 |
| 日历 / cadence / schedule | Workspace 自有节奏、Trigger、Schedule 和内容日历 | 保留专业节奏，不把日历提升为公司经营主面。 |
| 数据洞察 + 经营分析 | 当前数据洞察空间；Research 提议 Operating Intelligence | 历史能力已回收，统一命名和分析 Runtime 仍待 CEO Review。 |

## C. LATER：仍成立，但不是当前最小经营闭环

以下不是遗忘，而是明确后置：

- 完整 Business Economics / 单位经济学 / 投资组合和跨业务预算优化。
- 完整 Promise / Obligation 网络、谈判、违约和多方承诺协同。
- 多业务共享员工、模型、工具、预算时的组合容量规划与自动优化。
- 完整 Calendar / Scheduler / Autopilot 体系；当前只保留 Workspace 级节奏和检查点。
- 全部外部平台的 Metric Adapter、Webhook / Pull、Observation、Report 对象和主动洞察规则。
- 模型 / Agent Benchmark 的可比数据集与质量—验收—外部价值联合评估；没有真实样本时不能做排行榜。
- 复杂 Business Exit 的高级补偿、合并迁移、历史归档与外部副作用回收；其最小暂停 / 恢复 / 关闭边界需先解决 E 类缺口。
- 完整跨日 CEO Operating Day 对象、自动 Closeout、未完成责任的跨日承接与长期运营档案。

触发条件不是“开发时间到了”，而是：至少一个 Business 产生真实重复结果、多个业务争夺共享供给、或外部承诺/平台数据使上述能力成为经营瓶颈。

## D. SUPERSEDED：有明确 Current 来源推翻的内容

### 1. “完善 Curis”作为研发 Workspace 默认首个任务

- **Old：** Reasoning Record §13 把 Curis 自研发作为第一个真实研发任务。
- **Current：** PRODUCT-002、CURRENT_STATE 与 Blueprint 当前规则明确：研发 Workspace 只定义通用能力，具体任务由 CEO 创建；历史名称只能作为 dogfood 证据。
- **结论：** 这是任务内容被正式修正，不是经营闭环丢失。不得恢复硬编码或默认任务。

### 2. 技术模块 / 五层视图直接成为普通用户导航

- **Old：** 历史中间方案曾把经营层、能力、员工、工作和结果拆成页面 / Console。
- **Current：** ADR-0045、Master Map v3.0、Blueprint 5.2 和 UI Blueprint 明确六个一级区域，Runtime / Workflow / Gate / Simulation 下沉为高级、审计或实现语言。
- **结论：** 页面结构被正式替换；其背后的经营问题已在当前产品空间中保留。

## E. ACCIDENTALLY LOST：需要 CEO 决定是否恢复的真正缺口

### E1. Business Exit 的完整经营动作语义

历史推导不是简单的“删掉业务”，而是区分：

```text
Pause / Reduce / Transfer / Close / Merge / Split
→ 保护未完成承诺
→ 交接责任
→ 释放或重新分配能力与容量
→ 保存历史、Evidence、Result 与 Learning
→ 明确新的 Business / Workspace 状态
```

Current 已有“暂停、调整、替换、关闭”等零散动作，也有组织合并 / 拆分的规则；但没有一份跨 Company、Business、Role、Workspace、Commitment、Employee、Capability、Result 的 Business Exit 合同。组织合并/拆分不能替代业务退出，Delete 也不能替代退出。

**CEO Review：** 是否把上述最小退出语义恢复为 Blueprint 的跨层生命周期规则？本轮不增加 Exit 页面、不新增 Runtime Primitive。

### E2. CEO Operating Day 的跨日责任连续性

历史推导把 Operating Day 定义为可持续的经营单位：Brief、Matters、Handoff、Decision、Exception、Evidence、Learning、Closeout 都应可回看，未完成责任承接到下一天。Current 已有 CEO Desk、Assistant Brief、今日变化、待处理、下一决定和收束体验，但没有明确“上一天未完成事项如何成为下一天责任、哪些已关闭、哪些仍需 CEO 注意”的统一 Current 合同。

**CEO Review：** 是否先恢复“跨日连续性语义”作为产品规则，再决定是否需要 Runtime 持久化？本轮不创建 Operating Day 对象。

## F. ORPHANED PRODUCT REASONING：有价值但从未成为 Current 规则

这些内容不应误报为“丢失”，也没有资格直接回写 Blueprint：

| Orphaned reasoning | 为什么没有进入 Current | 处理建议 |
|---|---|---|
| “Company Core / Value Engine / Operating Engine + Truth / Decision / Change control plane”作为完整架构图 | 它是推导用的解释框架，当前产品已用 Company OS、Business、Workspace、Result、Decision 表达同一关系 | 作为产品推理参考保留；不新增三引擎导航或对象 |
| 旧导航候选（五层、四入口、能力中心 / 运行中心等） | 后续 ADR-0045 与 Master v3.0 已完成正式收敛 | 保留历史记录，不重新投票 |
| Workspace Studio 的详细“Stage / Role Slot / Agent / Capability / Tool / Knowledge / External System / Evidence / Acceptance”装配图 | Current 保留 Studio 的产品责任，但底层装配字段属于高级实现 / Domain Contract，未全部成为普通用户模型 | 继续作为 Studio 设计和 Runtime Review 输入，不升格为新页面 |
| 首批研发业务的具体 dogfood 脚本 | 具体任务不属于 Blueprint；Current 已明确由 CEO 创建 | 只保留为历史验证证据 |
| 早期 UI 中的固定 Topbar、统一 Console、员工完成/等待状态 | 已由 Frozen Shell / UI Blueprint 正式清理 | 不恢复；只在历史审计中可检索 |

**孤儿判断：** 本轮没有发现另一套未被 Supersede、且必须立即恢复为一级产品的经营内核。E 类两项是 Current 合同缺口，不应通过恢复旧页面解决。

## 3. V1 Foundation、V1 Domain Validation 与 Later

### V1 Foundation：一个 Business 也必须闭环

- CEO 身份、Company、CEO Assistant、最小目标和 Business。
- 至少一个有责任、有能力、有权限边界的 Employee / Team。
- 一个有专业工作现场的 Workspace（或合法的轻量工作形态）。
- 真实工作、外部结果或可信手动反馈。
- Evidence、Acceptance、Decision、Failure / Recovery、Unknown / Stale / Conflict。
- 资料来源、知识沉淀、下一检查点和 CEO 注意力回流。
- 最小 Usage / Cost / Quality / Acceptance 关联；未知不能伪造为零。
- E 类两项连续性规则应在进入完整 V1 前由 CEO 定义是否纳入。

### V1 Domain Validation：研发 / 小红书 / 抖音样板

三类 Workspace 用各自成熟的专业工作面验证同一经营内核：

- 研发：开发、测试、Review、交付 / 验收结果。
- 小红书：定位、选题、创作、审核、发布、平台回执、互动和增长反馈。
- 抖音 / TikTok：选题、脚本、素材、制作、剪辑、审核、发布、互动和交易 / 增长反馈。

它们不是三套 Company OS，也不是三套分析或组织真相；各 Domain 只提供自己的工作对象和外部指标来源。

### Later / Evolution

多业务投资组合、完整经济模型、跨业务容量优化、完整外部 Metric Adapter、Report / 主动洞察、Benchmark、复杂退出迁移和跨日长期运营档案，均需以真实经营瓶颈触发重新 Review。

## 4. 经营洞察专项判断

历史上“数据洞察、经营分析、External Result、Cost、Evidence、Business Analysis、Insight、Report、CEO Decision”是一条关系链，不是互相竞争的页面：

```text
Company Truth / Usage / Cost / Execution / External Result / Evidence
→ Insight / Analysis / Report（解释，不能冒充事实）
→ CEO Decision
→ Business / Employee / Capability / Workspace Change
```

当前已经恢复的是 **数据洞察产品空间合同**，包括范围、趋势、比较、归因、来源、新鲜度、Unknown、人工回填、质量、验收和外部结果关联；这属于历史能力的安全回收。Operating Intelligence Research 提议将数据洞察与经营分析统一命名，并补 Metric Registry、Domain Metric、External Adapter、Report 和主动洞察，但这些是 Research 结论，不是本轮 Current。

**判断：** 当前不存在经营洞察级别的产品空间遗漏；真正未完成的是数据采集和分析运行时，而不是缺少一个导航。Final Product Architecture Delta 已将“经营洞察 / Operating Intelligence”正式消费为第七个一级产品空间；页面与运行时实现仍按 Current / Implementation Truth 分开。

## 5. 公司版图专项判断

历史责任 → 能力 → 多主体协作 → 组织单元 → Department / Shared Service 的逻辑已演进为：

```text
Company
→ Department（稳定责任 / 共享能力的容器）
→ Business（经营价值方向）
→ Business Operating Model
→ Role / Staffing
→ Employee Binding
```

Company Map Research 与 Visual Exploration 只补充了表达方式：Department 容器、Business 节点、Role 折叠、Employee 隐藏、搜索 / Focus / Filter / Minimap / 成长标记；没有创造新的组织语义。故此处是 **EVOLVED，不是 ACCIDENTALLY LOST**。

研究中没有发现历史“协作关系图”必须成为默认主视图的正式判断；Current 已明确协作关系按需展开，员工目录负责反查。不要恢复自由 Network Graph 或传统 HR Org Chart。

## 6. 五个 CEO Review 问题

### 1. 过去几个月的核心经营内核，有多少已经安全保留？

按本表 38 条历史判断粗分：约 **20 条 PRESERVED，10 条 EVOLVED，4 条 LATER，2 条 SUPERSEDED，2 条 ACCIDENTALLY LOST**；另有 5 条 ORPHANED reasoning 作为历史参考。数字用于审计定位，不是产品健康分数。核心闭环相关条目绝大多数已安全进入 Current，丢失集中在 Business Exit 与跨日 Operating Day 连续性。

### 2. 哪些只是演进，不需要恢复旧模型？

五问 / 四入口、三引擎、承诺网络的普通用户表达、责任组织图、AI 团队层级、CEO Operating Day 的日常体验、Capacity 的最小表达、日历节奏和数据洞察命名关系，均已由当前 Company OS、六区产品空间、Workspace、Assistant、Insights 和 Company Map 更成熟地承载。恢复旧页面、旧导航或旧 Console 会制造第二套产品。

### 3. 哪些是真正意外丢失？

只有两项达到本审计的 ACCIDENTALLY LOST 门槛：

- Business Exit 的完整动作与历史保护规则；
- CEO Operating Day 的跨日责任连续性规则。

它们是经营内核合同缺口，不是要求立刻新增两个页面或两个 Runtime 对象。

### 4. 哪些应该进入 V1 基础能力，哪些明确属于 Later？

- **V1：** 一个 Business 的目标、责任、能力、Workspace、真实结果 / 手动反馈、Evidence、Acceptance、Decision、Failure / Recovery、资料沉淀、最小成本与质量关联，以及 CEO 的注意力回流。E 类两项先由 CEO 决定是否加入 V1 合同。
- **V1 Domain Validation：** 研发、小红书、抖音分别用真实专业工作面验证同一经营闭环。
- **Later：** 完整退出迁移、高级 Promise 网络、投资组合经济学、跨业务容量优化、外部指标适配、Report / 主动洞察、模型 Benchmark、统一调度和长期跨日运营档案。

### 5. 当前 Product Architecture 是否还有类似“经营洞察”级别的重大遗漏？

未发现另一个已经被历史推导充分证明、又完全没有 Current 承载的一级产品空间。需要 CEO 关注的不是再加导航，而是两项跨层连续性缺口（E 类），以及 Research 提出的 Operating Intelligence Runtime 尚未交付。它们必须分别走产品决策与实现队列，不能用研究文档直接覆盖 Current。

## 7. CEO Review 待决定事项（本轮不执行）

1. 是否接受 E1：把 Business Exit 最小语义（Pause / Reduce / Transfer / Close / Merge / Split、承诺保护、责任交接、资源释放、历史保留）写入下一次 Product Blueprint Delta？
2. 是否接受 E2：先定义 CEO Operating Day 的跨日连续性，再决定是否需要 Runtime 持久化？
3. “数据洞察 + 经营分析”是否正式统一命名为“经营洞察 / Operating Intelligence”？
4. Operating Intelligence 是否继续 scoped 入口，还是另做第七一级导航决策？
5. 哪一个真实 Business 的外部数据源先触发 Metric / Report / Adapter 专项？

---

**CEO OPERATING CORE RECOVERY AUDIT**  
**— ACCEPTED / REGISTERED**  
**— CONSUMED BY FINAL PRODUCT ARCHITECTURE DELTA**
