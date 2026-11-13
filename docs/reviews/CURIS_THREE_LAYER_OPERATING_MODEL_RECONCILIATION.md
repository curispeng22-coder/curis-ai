# CURIS THREE-LAYER OPERATING MODEL RECONCILIATION

**Authority Class:** REVIEW  
**Status:** Frozen  
**Disposition:** CEO ACCEPTED / APPROVED ARCHITECTURE REVIEW INPUT  
**Date:** 2026-08-20  
**Scope:** Product/architecture reconciliation only; no Runtime, Schema, DB, Frontend, Prototype, high-fidelity UI, Autonomous V1 Issue, or Canonical Business Spine Issue changes.

## 0. Executive verdict

Curis 已经有足够的共享经营骨架，能够承载任意业务；缺的不是第四套 Workflow，也不是一个新的通用 Agent Runtime。

本轮结论：

1. **三层模型成立。** User Surface 负责 CEO 经营；Employee Operating Layer 负责专业方法与工作上下文；System Runtime 负责确定性、责任、证据、权限和恢复。
2. **固定的是经营责任合同，不是行业步骤。** 现有 Operating Lifecycle Contract、Team Operating Engine 和 Workspace Engineering 的 Gate/Package First 规则可以承载不同业务，不应再建立第二套十步生命周期或固定行业箭头。
3. **Business Responsibility Handoff 可以复用现有对象。** Intent、Goal、Business、Workspace、Capability Gap、Research/Handoff、Assignment、Work、Result、Evidence、Review、Decision 与 Next-cycle Contract 已分别有产品或实现承载。
4. **未知业务路径成立为产品合同，但尚未是完整自动实现。** Curis 可以先理解、研究、检查能力、提出方案、请求 CEO 边界，再决定复用、组合、获取、建设或拒绝；“方法候选自动沉淀并验证”的编译/晋升能力仍是 Product → Implementation Gap。
5. **本轮不新增 Playbook 对象。** `Methodology + Package + Skill composition + Operating Definition + Evaluation/Result Contract` 已能分担所需语义。真正缺口是 Package 对专业方法元数据的表达与版本化实现，而不是必须新增一个叫 Playbook 的实体。
6. **XHS、RD、宠物寄养只是压力测试样本。** 它们不是 Curis 固定业务、预置业务或 Core Domain。

本文件是已接受的架构 Review 输入，不成为第四份 Product Authority，也不覆盖三份 Current Product Truth；后续若要落实 Package 方法元数据，必须另走单独的 Product Delta / Package Contract 工作。

## 1. Source and truth boundary

### 1.1 Current Product Truth consumed

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/01_Product/Curis_Product_UI_Blueprint.html`
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`

### 1.2 Product/architecture contracts and evidence consumed

- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md` — `Review / APPROVED CANDIDATE`，定义 Package First、Operating Model、Semantic Model 与空间工程方法；不是 Runtime。
- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md` — `Review / APPROVED CANDIDATE`，定义从意图到 Package/Acceptance 的可复用 Gate；不要求每条路径机械重跑。
- `docs/02_Architecture/WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md` — `Review / TECHNICAL DIRECTION APPROVED CANDIDATE`，定义声明式 Package 边界、Package Domain Schema、能力需求和 Core Action；当前 P0 形状不是任意代码容器。
- `docs/02_Architecture/WORKSPACE_ENGINEERING_RUNTIME_AND_EXTENSIBILITY_AUDIT.md` — `Review`，区分 Workspace Package 与 Company/Capability/Context/Content Publish Package 等同名对象，并记录当前安装/演进能力边界。
- `docs/01_Product/AI_Capability_Current_State_Audit.md`、`AI_Capability_UI_Contract.md`、`Curis_Capability_Intelligence_SOP.md`、`Skill_Expert_Registry.md`、`Curis_Talent_Candidate_Package_2026-08-18.md` — 能力目录、Provider、Skill、专家与招募/绑定语义。
- `docs/reviews/CURIS_TEAM_OPERATING_ENGINE_CONTRACT_CANDIDATE.md` — `Review`，Work-centered Responsibility Routing Control Plane；复用既有 Assignment、Employee Execution、Result、Evidence、Decision、Handoff。
- `docs/02_Architecture/WORKSPACE_ENGINEERING_END_TO_END_ACCEPTANCE_CONTRACT.md`、P0/P0.5/P1/P1.5 验收记录 — 实现事实与边界，仅用于 Implementation Truth，不反向改产品定义。

### 1.3 Reading rule

Research、Review 和实现证据解释“为什么/目前能做到什么”，不自动改变 Current Product Truth。本文发现的差距都标为 Product → Implementation Gap 或 Future Capability Architecture，不在本轮实现。

## 2. Three-layer operating model

### 2.1 Layer A — User Surface

CEO 看到的是公司正在经营什么、发生了什么、需要什么决定：

- CEO Desk
- Department / Company Map
- Business
- Workspace
- Leader Conversation
- Decision、Result / Evidence Detail
- 人才与能力、资料库、会议、经营洞察

用户主动作是表达意图、与负责人讨论、确认 Goal/Boundary/高影响决定、查看真实结果、回填外部反馈、决定继续/调整/等待/暂停/停止。Skill、Package、Cycle、Router、Provider Session 等默认隐藏在按需详情、员工能力、设置和审计中。

**产品检验：** CEO 可以把“经营这件事”交给 Curis，而不必先成为 Skill、DAG 或 Provider 配置工程师；当系统需要 CEO 做边界决定时，必须说明原因、证据、风险、缺口和返回位置。

### 2.2 Layer B — Employee Operating Layer

AI Leader/Employee 消费专业经营方法，但仍受同一责任骨架约束：

```text
Operating Responsibility
→ Situation Understanding
→ Research / Discovery（如适用）
→ Strategy / Plan
→ Execute
→ Result / Evidence
→ Review / Learning
→ Next-cycle Decision
```

这不是固定步骤表。不同业务可以合并、重复、跳过或插入专业活动，只要仍满足责任、真相、证据、边界、结果、复盘和继续/停止合同。

Leader 默认消费：Goal、Approved Strategy Envelope、当前 Situation、可用 Capability、适用 Method/Package、相关 Knowledge、Plan、Result/Evidence、Learning。Employee 只获得自己 Assignment 所需的最小 Context、Input Contract、Output Contract、Skill/Capability 和权限，不复制整个 Leader 经营上下文。

### 2.3 Layer C — System Runtime

Runtime 负责确定性和可靠性：Scope、Identity、Role/Assignment、Work、Responsibility Router、Team Operating、Employee Execution、Provider Task/Session、Result、Evidence、Decision、Handoff、Context、Persistence、Recovery、immutable version、CEO Gate、permission、idempotency、restart、WAIT/PAUSE/STOP、exactly-one successor。

Runtime 不负责判断“宠物寄养该如何经营”或把某个行业写入 Core。专业判断来自 Package、Skill、Methodology、Knowledge、Domain Adapter 与真实研究，最终仍受 CEO Boundary/Decision 约束。

## 3. Fixed contract, not dead workflow

当前已接受的 Operating Lifecycle/Team Operating 语义应被理解为“每项长期经营都必须有的责任与证据契约”，而不是所有业务的同一条箭头。

### 3.1 不变的责任

- 有明确 Operating Responsibility 与唯一合法 Current Holder；
- Intent/Goal/Boundary/Scope 可追溯；
- 重要策略或高影响动作有 CEO Gate；
- Work/Assignment/Execution 有合法范围、权限和版本；
- Result 不等于外部业务成功，必须有 Evidence/Source/Acceptance；
- Review/learning 有来源，策略调整不能只由 AI summary 触发；
- 继续、调整、等待、升级、暂停和停止是显式决定；
- 失败、迟到结果、权限失效、重启和重复触发可恢复且不伪造成功。

### 3.2 可变化的专业活动

Research、Strategy、Plan、Execute、Observe 的具体活动由 Domain Operating Method/Package 决定。内容增长可能需要受众/内容/发布/反馈；软件研发可能需要产品判断/架构/代码/测试/发布/反馈；宠物寄养可能需要服务设计/照护规则/排班/客户沟通/安全记录。三者不能共享一条内容生产 Workflow，但可以共享责任、结果、证据和恢复边界。

### 3.3 Cycle/Stop 语义

Cycle Close 是 bounded Cycle 的正常结束，不是 Business/Workspace STOP。PAUSE 保留 Goal、Strategy、Responsibility、History 并等待 Resume；STOP 终止当前 Operating Responsibility/Goal Series，只能由 CEO 或明确授权的 terminal policy 触发。

## 4. Universal Business Responsibility Handoff

### 4.1 用户心智

“把这个业务交给 Curis”不是“给我生成一个 Agent”或“让我填写一张行业配置表”，而是：

> 由 Curis 承接这项经营责任，先理解真实情况和边界，再提出能够被 CEO 确认的经营方案；条件满足后由 Leader/团队持续负责，并以真实结果、反馈和下一周期决定回到公司。

### 4.2 通用合同

```text
CEO Intent
  → Curis Understands
  → Capability Discovery
  → Research / Situation Understanding（必要时）
  → Operating Proposal
  → CEO Gate（仅系统无法合理代理的边界）
  → Bootstrap / Reuse / Compose
  → Leader Accepts Responsibility
  → Workspace Operating
  → Result / Evidence / Review
  → Continue / Adjust / Wait / Escalate / Pause / Stop
```

箭头是责任转译关系，不是固定 Workflow。Proposal 可以回到 Research，Capability Gap 可以回到 Discovery，低风险已验证模板可以跳过重复研究；任何跳跃都必须保留来源和理由。

### 4.3 阶段性质

| 阶段 | 性质 | 必须保留什么 | 何时可跳过/重复 |
|---|---|---|---|
| 接收 Intent | MANDATORY RESPONSIBILITY | 原始意图、来源、范围、当前 Company Truth | 不能跳过；可持续补充 |
| 理解 Situation / Goal | MANDATORY RESPONSIBILITY | 当前事实、未知、Goal/Success Contract 草案 | 已有可信版本可复用；事实过期需重查 |
| Capability Discovery | MANDATORY RESPONSIBILITY | Required/Available/Gap/Provider/Permission/Quality/Cost/Risk | 已验证 Package 可复用检查结果；不能凭目录存在当可用 |
| Research / Discovery | CONDITIONAL | 研究来源、适用性、未知和边界 | 已有可复用方法可跳过重复研究；陌生业务必须进入 |
| Strategy / Operating Proposal | MANDATORY RESPONSIBILITY | 方案、假设、活动、输出、评价、风险、请求的边界 | 可多轮修订；不是自动永久方法 |
| CEO Gate | CONDITIONAL GATE | Goal、Boundary、Risk、Constraint、Budget、高影响外部动作 | 低风险且已授权的 Envelope 内不要求每步确认 |
| Bootstrap / Reuse / Compose | MANDATORY RESPONSIBILITY | 复用/组合/获取/建设的选择与影响预览 | 现有结构可复用时不从零搭建 |
| Leader Accepts Responsibility | MANDATORY RESPONSIBILITY | Leader Assignment、Scope、责任连续性、下一步 | 无合法责任人则等待/升级/拒绝运行 |
| Operate | MANDATORY RESPONSIBILITY（仅在 Gate 通过后） | Work、Plan、权限、Execution、Result Contract | 专业活动由 Domain 方法决定，不固定箭头 |
| Result / Evidence / Review | MANDATORY RESPONSIBILITY | 来源、Freshness、Unknown、Acceptance、反馈 | 无结果可进入 WAIT/ESCALATE，不能伪造 |
| Next-cycle Decision | MANDATORY RESPONSIBILITY | CONTINUE/ADJUST/WAIT/ESCALATE/PAUSE/STOP 及理由 | 只有确定的终止合同才 STOP |

### 4.4 用户不应被迫承担的配置

CEO 不应被默认要求填写 Positioning、Strategy、Team、Workflow、Workspace Structure、Operating Plan。缺信息时优先由 Curis Research → Situation Understanding → Strategy Proposal；只有 Goal、Strategy Boundary、Risk、Constraint 和高影响决定无法合理代理时，才请求 CEO Gate。

## 5. Unknown Business：Curis 如何处理“不知道”

陌生业务是通用性测试。Curis 必须能诚实地把“不知道”变成可处理的 Capability Gap，而不是把一个通用 Agent 假装成行业专家。

### 5.1 处理路径

1. 识别 Intent、Business/Workspace Scope、目标和外部影响。
2. 拆出 Required Capability：专业判断、资料、连接、工具、权限、执行、评价与安全边界。
3. 与 Company 已有 Capability/Provider/Skill/Knowledge/Package 比对。
4. 对每项选择：
   - `USE EXISTING`：已有验证能力直接满足；
   - `COMPOSE EXISTING`：多个已验证 Skill/Tool/Knowledge/Connector 组合，仍需明确责任与评价；
   - `RESEARCH / ADAPT`：业务方法未知，研究真实行业并形成临时方法候选；
   - `BUILD / ACQUIRE CAPABILITY`：现有能力无法满足，获取 Connector/Tool/专家或建立受控能力；
   - `ESCALATE CEO`：目标、边界、预算、风险、外部关系或不可逆决定需要 CEO；
   - `REFUSE / CANNOT OPERATE YET`：关键能力/权限/质量/安全条件不成立，返回缺口与恢复入口。
5. 形成 Operating Proposal：Objective、适用情境、推荐能力、活动、必要输出、评价方式、风险/约束、Gate、来源和未知。
6. CEO 确认不能代理的边界后，建立/复用最小 Workspace、Leader Assignment 和 Capability Binding。
7. 以 bounded Cycle 运行；Result/Evidence/Review 验证方法，不因一次成功自动永久化。

### 5.2 诚实状态

“目录可见”不等于“可运行”；“方法候选”不等于“已验证”；“内部完成”不等于“外部结果”；“未知”不等于 0。每个缺口必须显示 Owner、原因、缺什么、下一步、返回原 Stage、是否产生外部副作用。

### 5.3 能力晋升的未来边界

未来可将 Research → Method Candidate → controlled test → Evidence → Review → versioned reusable Package/Capability。一次临时 AI 建议不得自动成为公司永久 Skill/Method。Promotion 需要版本、来源、证据和 CEO/授权 Review。本轮不进入 Autonomous V1 实现，也不创建 Self-Evolution Runtime。

## 6. Existing Object Audit

### 6.1 审计判定规则

- **Canonical?** 指当前 Product Truth/冻结合同是否承认该语义；不等于已有代码表。
- **Persisted/versioned?** 分别记录产品语义与当前实现事实；文档中没有证据的部分标 `UNVERIFIED / GAP`。
- **Core/Provider?** Core 是公司、责任、结果、权限、生命周期；Provider 是外部模型、工具、资料、连接或专业能力来源。
- **Method expressive?** 只问能否表达专业方法，不把“能执行”误当“知道行业怎么经营”。

### 6.2 Three-layer concept matrix

| Concept | User Surface | Employee Operating Layer | System Runtime | Owner / source authority | Canonical / persisted / versioned | Core or Provider | 能否承载专业经营方法 | V1 / Future |
|---|---|---|---|---|---|---|---|---|
| Intent | 表达“想经营什么” | 转为 Situation/Goal 候选 | Scope、来源、提案引用 | Product Blueprint / Workspace Methodology | Canonical；Company/Business/Workspace 相关事实按现有实现保存；版本/补充需可追溯 | Core | 只能表达方向，不表达完整方法 | V1 基础 |
| Goal | CEO 可确认目标与成功标准 | 约束 Strategy/Plan/Evaluation | pinned Goal/Success Contract | Product Blueprint / Operating Lifecycle Contract | Canonical；已进入 Business/Workspace 合同；运行时需 pin | Core | 不是方法本身，是方法目标 | V1 基础 |
| Strategy | CEO/Leader 看方案与边界 | Approved Strategy Envelope 内调整假设、战术、节奏、资源 | Decision/Review/Next Cycle 引用 | Operating Lifecycle Contract | Canonical；版本化/运行 pin 合同存在；外部质量仍按 evidence | Core + Domain | 表达策略方向，可由 Domain 方法建议 | V1 基础 |
| Leader | 公司/Business/Workspace 负责人 | 持续承担 Goal、Strategy、Review、升级 | `Employee × Role × Scope` Assignment | Leadership Authority / Team Operating | Canonical；Assignment 为真实身份关系；不另建 Leader 类型 | Core | 负责采用方法，不是方法对象 | V1 基础 |
| Business | CEO 经营单元与结果聚合 | 提供目标、方向、Workspace portfolio | Canonical Business Spine resolver | Product Blueprint / Canonical Business Spine | Canonical；Business identity 持久化；长期必须归 Department、至少一个 Workspace | Core | 聚合业务，不写行业流程 | V1 基础 |
| Workspace | 专业业务工作空间 | Domain Surface + Team Operating + Employee Work Area | Workspace/Package/Instance scope、persistence、recovery | Product Blueprint / Workspace Shell / Package proposal | Canonical；Workspace/Package version provenance 部分有实现证据，动态能力边界需分层 | Core host + Domain package | 承载方法的专业环境，不等于方法 | V1 基础 |
| Capability | CEO 可见能力准备/缺口 | 判断员工是否能完成某职责 | Catalog → Connection → Health → Binding → permission | Capability UI/Current State Audit | Canonical；连接/健康/绑定有状态合同；不可用时 fail closed | Core orchestration; provider-backed | 给出能力要求/可用性，不给行业方法 | V1 基础 |
| Skill | 按岗位理解的专业能力/能力组合 | 员工实际工作的可复用专业能力 | Binding/health/version 引用；不拥有责任路由 | Skill/Expert Registry / Talent Market contracts | Canonical product concept；目录/版本/绑定事实分层，具体来源需验证 | Provider/domain resource | 适合表达原子能力或组合输入，不足以单独表达完整经营方法 | V1 + 增强 |
| Methodology | 领域研究/空间工程建立方法的收敛文档 | 提供方法设计原则、Gate、翻译规则 | 当前主要是文档/人工 Handoff，不是运行对象 | Workspace Engineering Methodology | Canonical methodology candidate；未证明为 persisted runtime object | Product/Provider process | 能表达完整 Operating Model 的研究与设计语义 | V1 依赖；自动化未来 |
| Package | 声明式 Workspace/Domain composition 与版本来源 | 给员工/Workspace 提供方法、能力、对象、界面与要求的组合容器 | install/validate/provenance/instance substrate；不装任意代码 | Workspace Package Technical Proposal / P0/P0.5 evidence | Canonical target contract；P0 组合/安装能力有实现证据，但专业方法元数据持久化边界仍 GAP | Core host + domain/provider contents | 能成为方法载体的组合边界；当前技术形状需扩展方法描述字段 | V1 foundation + targeted extension |
| Operating Definition | 用户语言“团队运转/默认流程” | Role/Responsibility/Input/Output/Review/Return 的责任合同 | immutable version、Work pins version、Router consumes | Team Operating Engine Contract | Canonical；immutable version/route evidence accepted；不含 Model/Skill/Tool/Knowledge | Core | 表达“谁对什么结果负责”，不表达行业经营知识 | V1 基础 |
| Work | CEO/Leader 看当前工作与下一步 | Assignment 下的工作输入/输出 | durable Work、Holder/Executor、idempotency/recovery | Team Operating Engine Contract | Canonical/persisted/version-linked | Core | 经营责任执行载体，不是专业方法 | V1 基础 |
| Assignment | 员工在某 Role/Scope 的职责关系 | 员工工作边界、输入、输出、权限 | unique Holder/Executor resolution | Leadership / Team Operating authority | Canonical/persisted；Scope 与版本必须可追溯 | Core | 将方法映射到人，不定义方法 | V1 基础 |
| Result | CEO 看得到的工作结果 | 员工输出与下一判断的输入 | Result Contract、status、provenance、refs | Team Operating / Product Truth | Canonical/persisted；可接受/拒绝/回退 | Core | 必须由 Domain 定义结果内容与质量 | V1 基础 |
| Evidence | 证明来源、执行和外部反馈 | 判断能否接受/学习 | Evidence refs、freshness、unknown/stale | Product Blueprint / Result & Evidence authority | Canonical/persisted as refs/bodies by source; retention varies | Core truth boundary | 为方法评价提供依据，不等于方法 | V1 基础 |
| Review | CEO/Leader 对结果、风险和方法的判断 | 解释、批评、复核、接受/拒绝 | Review/Decision refs and gates | Operating Lifecycle / Meeting / Result contracts | Canonical；审计/版本事实需保留 | Core decision | 将结果转为 learning/next action | V1 基础 |
| Learning | 被证据支持的经验/方法变化 | 员工/Leader 下一轮消费 | accepted Learning ref，不能由 summary 直接改策略 | Operating Lifecycle / Product Blueprint | Canonical product semantics；Promotion/Memory persistence varies | Core + Domain | 可更新方法/Skill/Knowledge/Strategy，但必须 Review | V1 基础；自动晋升未来 |
| Cycle | bounded 经营周期，不是行业步骤 | Leader 通过周期观察、复盘、继续/调整 | one active Cycle、pin、successor、WAIT/PAUSE/STOP | Operating Lifecycle Contract | Canonical contract; implementation readiness gated by Business Spine | Core control plane | 为方法提供时间/边界，不定义内容 | V1 基础 |
| Decision | CEO/授权人批准、修改、等待、暂停或停止 | 边界、风险、资源、下一周期 | Decision Gate/Packet、resume action | Product Blueprint / Team Operating | Canonical/persisted and auditable | Core | 选择是否采用方法，不提供方法本身 | V1 基础 |
| Provider | 模型/Agent/Skill/Tool/Connector 等外部能力来源 | Employee/Workspace 可用能力的供给者 | Connection/Health/Binding/permission | Capability/Settings/Security authority | Canonical provider relation; credentials secret and external | Provider | 提供能力，不拥有公司责任或行业真相 | V1 foundation |
| Tool | 可调用的具体外部或本地操作能力 | 执行某个 bounded activity | Provider Task/Session/permission/side effect | Capability Registry / Connector authority | Provider-backed; health/permission evidence required | Provider | 只能执行活动，不决定方法 | V1 foundation |
| Knowledge | 本地/外部资料、来源和公司沉淀 | Situation/Research/Plan/Execution 相关引用 | Context refs, indexing, permission, source/freshness | Library / Knowledge contract | Canonical; source/index/permission facts; retention policy separate | Provider/content | 为方法提供事实，不是方法本身 | V1 foundation |

### 6.3 Audit answers for each object

| Audit question | Finding |
|---|---|
| 当前谁消费？ | CEO/Leader 消费 Goal、Strategy、Result、Evidence、Decision；Leader/Employee 消费 Assignment、Capability、Skill、Knowledge、Method/Package；Runtime 消费 Work、Assignment、Result、Evidence、Decision、Cycle、Provider facts。 |
| 是否已经有第二套 Playbook 语义？ | 没有发现独立 Playbook 对象。Workspace Engineering 的 Operating Model/Handoff 是方法论产物；Operating Definition 是责任路由版本；Package 是声明式组合边界。三者职责不同，不能合并成 Runtime。 |
| 是否可以组合多个 Skill？ | 产品合同与人才/能力语义允许岗位能力包、Skill/Tool/Knowledge/Connector 组合；具体绑定/健康/权限由 Capability/Provider 事实决定。 |
| 是否能表达 recommended actions / outputs / evaluation / risk？ | Product Handoff/Operating Model 可以表达；Package 当前目标形状可以声明能力、对象、表面、允许 Action、Result/Evidence 结构和权限要求；对“建议活动、适用情境、评价指导、风险”没有一份已确认的统一 persisted method schema，属于 Package contract gap，不自动新增 Playbook。 |
| 是否 versioned？ | Operating Definition、Workspace/Package provenance、Capability connection/health、Result/Evidence/Decision 各自有版本或来源语义；“方法候选→可复用版本”的推广链尚未实现。 |
| 是否属于 Core 还是 Provider？ | Responsibility/Decision/Result/Evidence/Context/Recovery/Workspace host 属 Core；Skill/Tool/Connector/Knowledge/模型/外部 Agent 属 Provider 或 Domain resource；Package 是 Core host 承载的 Domain composition，不把 Provider 写入 Core。 |

## 7. Package reconciliation

### 7.1 Package 不是“只装 UI”

当前 Package First 与 technical proposal 已把 Workspace Package 定义为声明式 Domain composition：身份/版本/来源、Navigation/Surface 声明、Package Domain Schema、允许的 Core Action、Capability/Knowledge/Permission requirements、Result/Evidence presentation references 和实例 provenance。它不是任意 JS/Python 容器，也不是第二个 Workflow/Agent/Task Runtime。

因此，产品语义上应把它理解为：

> **Domain Operating Capability Package：把一个业务的专业工作面、语义、职责起点、能力需求、方法引用、评价/结果契约和安全边界组合成可验证、可版本化的业务能力包。**

这是对现有 Package First 的语义澄清，不是本轮授权改 Schema 或扩大 P0。

### 7.2 已覆盖与真实缺口

**已覆盖：** Domain surface/objects/actions、局部语义、能力与权限需求、Workspace/Instance provenance、复用 Core Runtime、版本和安装/禁用/撤销等生命周期边界的产品/技术合同。

**真实缺口：** 当前 Package 还没有一个被实现/验收的统一方法元数据层，能够结构化表达 `Applicability / Objective / Recommended capabilities / Recommended activities / Required outputs / Evaluation guidance / Risk / Required gates / transition conditions / references`。Workspace Engineering 文档可以人工产出这些内容，但不是自动运行的 persisted Method object。

**最小处理：** 未来优先扩展 Package manifest/contract 与 Methodology Handoff 的引用，而不是新增 Playbook；在证据证明 Package 无法承载前，不创建第二个对象。

### 7.3 Package 生命周期与未知业务

未知业务的最小 Package Candidate 可以先是 Research/Handoff 文档 + 可验证的 Capability Review + Domain Surface/Result Contract 草案；只有 CEO Gate 和 Core Expressibility Check 通过，才进入 Package/Instance。缺能力时 Package 保持未激活/缺口，不得安装一个看起来完整但不能工作的办公室。

## 8. Playbook adjudication

### Decision: NO NEW PLAYBOOK OBJECT IN THIS REVIEW

原因：

1. `Methodology` 已承载研究、方法建立、适用 Gate、Handoff、翻译和进化原则，但它是产品/工程方法论，不是 Runtime。
2. `Skill composition` 已承载可复用专业能力；Skill 不应承担 Goal、责任、路由和公司边界。
3. `Package` 已是最合适的跨 Skill/Capability/Domain Surface 组合边界；可在不造新实体的情况下扩展方法元数据引用。
4. `Operating Definition` 已承载 Role/Responsibility/Input/Output/Default Flow/Review/Return 的责任执行定义；它不应膨胀成行业知识库。
5. `Result Contract + Evaluation/Review + Evidence` 已承载输出、评价、风险和是否继续的可靠边界。
6. 新增 Playbook 会产生第五种“方法真相”，容易与 Workflow、Operating Definition、Package 和 Skill 重叠。

因此不创建 `CURIS_DOMAIN_OPERATING_CAPABILITY_MODEL_CANDIDATE.md`。若后续实现验证 Package 仍无法表达上述方法元数据，再建立一个受限 Package Contract Delta；只有该 Delta 证明无法复用 Package/Methodology/Skill composition，才重新评估独立 Method Bundle 候选。

## 9. Three-domain pressure test

### 9.1 Case A — AI technology content account

**Intent：** 经营一个 AI 科技内容账号，目标是增长与业务反馈。

**可复用：** Company/Business/Workspace、Leader Assignment、内容/研究/分析所需 Skill/Tool/Knowledge/Connector、Team Operating、Result/Evidence/Review、外部反馈手动回填与下一周期。

**Domain method：** 受众/赛道研究 → 内容假设 → 选题/文案/素材 → CEO/品牌边界 → 发布 → 反馈/数据 → 复盘。活动顺序由当前情况和能力决定，不写入 Core。

**缺口行为：** 没有平台数据连接时显示 `CAPABILITY_GAP`，说明需要的连接/负责人/恢复入口；不把草稿或内部执行当增长结果。

**结论：** 成立，证明内容类方法可以作为 Package/Skill/Knowledge/Result Contract 组合，不证明 Curis 是内容产品。

### 9.2 Case B — Software / Product Development

**Intent：** 持续研发 Curis 或另一个 SaaS。

**可复用：** Company/Business/Workspace、研发 Leader、代码/测试/资料 Capability、Assignment/Handoff、Work/Result/Evidence、Review/Decision、发布/用户反馈回流。

**Domain method：** 产品问题 → 研究/取舍 → 架构 → 实现 → 测试 → Review/发布 → 使用反馈 → 优先级/策略调整。它不需要内容发布或账号增长步骤，且可在一次 Cycle 内并行/往返。

**结论：** 成立，证明“固定经营责任 + 可变专业方法”不是内容 Workflow 的改名。

### 9.3 Case C — Unknown business: pet boarding

**Intent：** 经营宠物寄养，目标、规模、服务对象、地区规则可能不完整。

**Curis 不应假装知道：** 先识别照护安全、容量、排班、客户沟通、场地、保险/法规、价格和外部承诺等 Required Capability；未知事实进入 Research/Capability Gap，不直接生成可运营员工。

**最小路径：**

1. Situation Understanding：询问/研究最低必要事实；不要求 CEO 先填写完整行业表单。
2. Research：研究当地合规、照护标准、常见服务模型和风险；来源与未知可回看。
3. Capability Discovery：复用日历/资料/沟通/排班/支付等已有能力，识别缺失连接、专业知识与权限。
4. Proposal：提出最小服务模型、责任、能力、评价与 Gate；CEO 只确认高影响安全/预算/边界。
5. Establish：形成 Generic/Domain Workspace Candidate + Leader/Team/Capability Gap；缺少安全能力时保持不可运行。
6. Operate：先在受控范围运行；Result/Evidence/Review 验证服务质量与外部反馈。

**拒绝条件：** 关键安全/法律/权限/责任人缺失，或无法给出可验证评价时，Curis 必须 `CANNOT OPERATE YET`，而不是让 CEO 自己搭完整流程或让通用 Agent 自由发挥。

**结论：** 模型成立，但“自动研究→方法候选→验证→晋升”仍不是当前已交付能力；这是明确的 Product → Implementation Gap，不是新行业 Core。

### 9.4 Pressure-test summary

| Dimension | Content growth | Software/RD | Pet boarding / unknown |
|---|---|---|---|
| Shared | Intent、Goal、Leader、Assignment、Work、Result/Evidence、Review、Decision、Recovery | 同左 | 同左 |
| Domain | 内容/受众/发布/反馈 | 产品/代码/测试/发布/反馈 | 照护/容量/安全/合规/服务反馈 |
| Method form | Package + Skill/Knowledge + Result Contract | Package + Skill/Knowledge + Result Contract | Research/Handoff → Candidate Package，不能假装成熟 |
| Fixed arrow? | 否 | 否 | 否；Gate/责任/证据仍固定 |
| Core hard-code? | 禁止 | 禁止 | 禁止 |
| Truth boundary | 外部平台反馈 | 测试/发布/用户反馈 | 合规/安全/客户/容量真实来源 |

## 10. User Surface mapping

### 10.1 CEO 默认看到

CEO Desk、Business/Workspace、Company Map、Leader Conversation、Result/Evidence、Decision、人才与能力、资料库、经营洞察和会议。用户感知是：Curis 在理解、研究、提出方案、组团队、工作、复盘、继续；不是看到 Runtime Console。

### 10.2 按需出现

Employee Detail / Workstation、Capability Detail、Package/Workspace Engineering 进阶信息、Skill/Tool/Connector/Knowledge 来源、权限/健康、Audit/Execution 诊断。高级用户可查看 Method/Package 适用性、版本、评价和风险，但普通 CEO 不必先学习这些词。

### 10.3 不新增一级产品

本轮不新增 Skill Center、Playbook Center、Lifecycle Center、Runtime Center。若 Package 方法元数据未来需要可视化，优先放入 Workspace/Employee/Capability/Package Detail 或高级管理，不预设新的一级导航。

## 11. Employee Operating View

### Leader consumes

`Goal → Approved Strategy Envelope → Current Situation → Available/Required Capability → Relevant Method/Package → Relevant Knowledge → Current Plan → Result/Evidence → Review/Learning → Next-cycle Decision`。

Leader 负责连续经营与 CEO 沟通；Leader 不是特殊 Employee Type，也不替代专业员工执行所有工作。

### Employee consumes

`Assignment → Responsibility → Work → relevant Skill/Capability → bounded Context → Input Contract → Output/Result Contract → Permission → Evidence requirements`。

员工只消费与其 Scope/Work 相关的上下文。Method/Package 只能提供适用活动、输入/输出、评价和风险提示；不能把员工变成隐式无限 Agent。

## 12. Capability discovery contract

Curis 判断“会不会做这件事”至少检查：

| Check | 询问 | 结果 |
|---|---|---|
| Required Capability | 这项责任需要什么专业判断、资料、工具、连接和执行权限？ | 需求条目与适用范围 |
| Available Capability | 公司目录中什么已连接、已验证、可绑定？ | 可用集合 |
| Provider availability | 来源、版本、健康、许可、地区/账号范围是什么？ | Provider 事实 |
| Permission | 员工/Workspace/Company 是否有合法权限与外部副作用授权？ | 可执行/需授权 |
| Quality / evidence | 能力结果如何验证、来源是否新鲜？ | 可接受/未知 |
| Cost / risk | 使用成本、失败代价、不可逆风险是什么？ | Envelope/Gate |
| Decision | 复用、组合、获取、建设、升级还是拒绝？ | `USE_EXISTING / COMPOSE / ACQUIRE / BUILD / ESCALATE / REFUSE` |

Capability Catalog 可发现不等于 Health verified，不等于 Employee Binding，不等于外部业务结果。缺口必须返回原工作位置。

## 13. Self-evolution boundary

允许的未来方向是“方法候选的受控晋升”，不是 AI 自行修改 Core：

```text
Research
→ Method Candidate
→ controlled/replay test
→ Result / Evidence
→ Review / CEO or delegated promotion
→ versioned Package / Skill / Knowledge / Operating Definition reference
```

任何晋升都要保留来源、版本、适用范围、评价、风险、失败和撤回关系。当前不把一次对话、一次 AI Summary 或一次成功外部动作自动转为永久能力，不修改 Autonomous V1。

## 14. Concept minimization

### KEEP

Company、Department、Business、Workspace、Leader/Employee Assignment、Capability/Provider/Connection/Health/Binding、Skill、Tool、Connector、Knowledge、Package、Operating Definition、Work、Result、Evidence、Review、Learning、Decision、Handoff、Cycle、Context、Recovery。

### EXTEND (minimal, no implementation in this review)

1. **Package contract**：允许引用/承载版本化的专业方法元数据（适用情境、目标、推荐能力/活动、必要输出、评价指导、风险/Gate、转换条件），不把它变成 Workflow/DAG。
2. **Workspace Engineering Handoff**：将上述方法元数据作为收敛输入，区分 `TEMP AI REASONING`、`CANDIDATE`、`VALIDATED`、`PROMOTED`；不自动写入永久 Skill。
3. **Capability Review**：对 unknown business 明确 Required/Available/Gap/Owner/Return Stage/Decision。

### MERGE / REINTERPRET

- “Playbook”语义由 `Methodology Handoff + Package method metadata + Skill composition + Operating Definition + Result/Evaluation Contract` 共同承载；不把任何一个对象改成全能方法对象。
- “Workflow”在用户层表达为团队运转/默认流程；内部路由和 Runtime 继续由 Team Operating/Responsibility Router 负责。
- “Provider”是能力来源，不是公司员工、Leader、业务真相或 Runtime owner。
- “Domain Package”是 Core host 上的专业组合，不是新的行业 Core。

### DO NOT ADD

- 不新增 Playbook、Playbook Center、Method Runtime、Industry Workflow Engine、Domain Agent Runtime、第二 Task/Result/Decision/Knowledge 系统。
- 不把 XHS/RD/Pet Boarding 写成 Core enum、默认模板或固定产品导航。
- 不把 Package、Skill、Methodology、Operating Definition 复制成多个同名对象。

### NEW CANDIDATE

本轮无新候选对象。只有在 Package contract 扩展经过真实用例证明仍无法承载方法元数据时，才重新提出受限 `Method Bundle` 候选；该条件目前未满足。

## 15. Product / implementation boundary

### Product contract now

- 三层模型与职责边界；
- 通用 Business Responsibility Handoff；
- unknown business 的能力发现、研究、提案、Gate、拒绝/恢复语义；
- Package First、复用优先、Core 不硬编码领域方法；
- 固定责任/证据/恢复契约，非固定行业箭头；
- Method 不自动晋升为永久能力。

### Implementation gaps (not blockers for this review)

- 方法元数据在 Package 中的最小持久化/版本/验证表达；
- Research/Handoff → Candidate Package 的结构化转译；
- unknown business 的自动 Capability Planner/Provider availability 组合；
- 外部行业事实、质量、成本、合规的真实连接与评价；
- method promotion/revoke 的完整流程；
- 当前 Dynamic Workspace Package Runtime、通用升级/迁移/回退和第三方信任边界仍按各自 Review 记录，不在本文夸大。

### Autonomous V1 boundary

Autonomous V1 Issue 仍以 Canonical Business Spine `IMPLEMENTED / ACCEPTED` 为硬 Start Gate；本报告不修改该 Gate、Scope、Schema 或 Runtime。若方法元数据未来成为 V1 的硬依赖，须另走 Product/Implementation Review，不能从本报告静默升级。

## 16. Final answers to the 20 questions

1. **Curis App 用户真正看到什么？** 公司经营表面：Desk、Business、Workspace、组织/人才与能力、资料、会议、洞察、Leader Conversation、Decision、Result/Evidence。
2. **AI Employee 内部消费什么？** Assignment/Responsibility、Goal/Boundary、最小 Context、相关 Capability/Skill/Knowledge/Method、Input/Output Contract、Result/Evidence 与权限。
3. **Runtime 必须保证什么？** Scope、责任唯一性、版本、权限、幂等、证据、结果真实性、CEO Gate、恢复、WAIT/PAUSE/STOP 和有限 successor。
4. **“把业务交给 Curis”意味着什么？** Curis 承接经营责任，先理解与研究，再提出可确认方案，组建责任与能力，运行并把结果/反馈带回下一周期。
5. **任意未知业务如何进入同一模型？** 通过 Intent → Situation → Capability Discovery → Research/Proposal → Gate → Reuse/Compose/Acquire/Build → Leader/Workspace → bounded Operation。
6. **Curis 不知道怎么经营时怎么办？** 明确不知道，研究真实行业与风险，形成临时方法候选；缺关键能力则显示 Gap/Owner/Return Stage，必要时拒绝运行。
7. **Skill 当前承担什么？** 原子或岗位能力组合；提供“能做什么/依赖什么”，不承担 Goal、责任路由或公司真相。
8. **Package 当前承担什么？** 声明式 Workspace/Domain 组合边界：专业表面、对象/动作、能力/权限需求、结果/证据表示、版本/来源和实例关系。
9. **Methodology 当前承担什么？** 研究、方法建立、Handoff、翻译、Gate、Package First 与进化的工程/产品方法，不是 Runtime。
10. **Operating Definition 承担什么？** Workspace 内 Role/Responsibility/Input/Output/Default Flow/Review/Return 的不可变责任执行定义。
11. **是否真的需要 Playbook？** 当前不需要新增对象。
12. **如果不需要，谁承担 Playbook 语义？** 方法论 Handoff、Package 方法元数据、Skill composition、Operating Definition、Result/Evaluation/Review 共同承担。
13. **如果需要，为什么现有对象无法承载？** 本轮尚未证明无法承载；目前只发现 Package 方法元数据实现缺口，优先扩展 Package。
14. **Domain Package 是否应该扩展为 Operating Capability Package？** 产品语义上应这样理解，技术上先以 Package Contract 最小扩展实现，不新建同义对象。
15. **如何避免 Domain 能力进入 Curis Core？** Core 只保留责任、结果、证据、权限、生命周期、Package host 与能力编排；专业方法进入 Package/Skill/Knowledge/Provider/Adapter。
16. **如何避免专业 Method 变成死 Workflow？** 只记录推荐活动、输出、评价、风险和 Gate；执行顺序由 Situation、Assignment、Result、Review 和 Domain 规则动态决定，不把 Method 编译成 DAG。
17. **小红书/RD/宠物寄养是否都成立？** 成立为压力测试：共享责任/证据/运行契约，专业方法分别不同；宠物寄养缺能力时必须诚实拒绝/等待，不伪装成熟。
18. **Autonomous V1 是否需要修改？** 不需要；本报告不改变其 Scope/Start Gate。只有证明方法元数据是硬依赖时，另走 Review。
19. **Future self-evolution 如何接入？** Research → Candidate → controlled test → Evidence → Review/Promotion → versioned Package/Skill/Knowledge reference；禁止一次 AI 输出自动晋升。
20. **最少新增几个概念？** **零个新持久化概念。** 先扩展 Package 方法元数据与 Handoff/Capability Review 的表达；若未来证据证明仍不足，再单独评估一个受限 Method Bundle。

## 17. CEO review questions / unresolved authority

以下不是本轮产品模型冲突，而是后续若要进入 Product Delta 必须单独确认的边界：

1. Package 方法元数据的最小字段、来源、版本、Promotion/Revocation 责任是否由 Package Contract 单独冻结？
2. `TEMP AI REASONING / CANDIDATE / VALIDATED / PROMOTED` 是否只做 Handoff/Review 标记，还是将来进入 persisted Package provenance？
3. Unknown business 的 Research/Provider/Quality/Cost 真实依赖何时达到可安全自动运行的条件？
4. Domain UX Exploration 如何验证“同一责任模型、不同 Primary Surface”，且不把 XHS/RD 样本升级为固定模板？

## 18. Brand Neutrality Architecture Principle Delta（CEO Accepted 2026-08-20）

### 18.1 Three identities

本轮冻结：**Curis 是当前产品品牌，不是 canonical business/runtime semantic。**

- **Brand Identity：** Curis、产品显示名、Logo、App 名称、营销文案和“交给 Curis”等用户语言；未来允许 Rebrand。
- **Product Semantic Identity：** Company OS、CEO Assistant、Company、Department、Business、Workspace、Leader、Employee、Responsibility、Capability、Package、Skill、Operating Definition、Operating Lifecycle；这些保持品牌中立。
- **Runtime / Persistent Identity：** `company_id`、`department_id`、`business_id`、`workspace_id`、`employee_id`、`assignment_id`、`work_id`、`result_id`、`evidence_id`、`decision_id`、`cycle_id` 及 Package identity/version refs；Rebrand 不重新生成、不迁移归属、不破坏历史引用。

### 18.2 Boundary

User Surface 可以使用“交给 Curis”“Curis 正在研究”“Curis 助理”；Employee Operating Layer 与 System Runtime 使用品牌中立的 Business Responsibility Handoff、Operating Responsibility、Package、Capability Provider 等语义。品牌显示名不得成为 Business、Workspace、Operating Lifecycle 或 Runtime 类型判断；现有 `curis.*`、`curis_app`、repository/package namespace 仅属技术命名空间，不因本原则机械重命名。

### 18.3 Future direction and audit

未来用户可见品牌文案优先消费统一 Brand Configuration（候选：`productName`、`displayName`、`assistantDisplayName`、logo/icon refs、brand assets），但本轮不设计 Schema、Brand Runtime、Frontend 或 Rebrand Initiative。对 Current Product Authority 的轻量审计结论：未发现必须立即修复的品牌耦合；潜在注意点仅是少量内部标题/文案可能把 Curis 当作语义前缀，后续新 Authority 应优先采用品牌中立命名。历史文档、技术 namespace、bundle/repository/database/API/Package identity 本轮均不批量改名。

## 19. STOP STATE

**CURIS THREE-LAYER OPERATING MODEL**  
— USER SURFACE DEFINED  
— EMPLOYEE OPERATING LAYER DEFINED  
— SYSTEM RUNTIME BOUNDARY DEFINED  
— UNIVERSAL BUSINESS HANDOFF DEFINED  
— UNKNOWN BUSINESS PATH DEFINED  
— CAPABILITY / PACKAGE / SKILL / METHOD RECONCILED  
— NO NEW PLAYBOOK OBJECT JUSTIFIED  
— DOMAIN EXAMPLES REMAIN EXAMPLES ONLY  
— BRAND IDENTITY ≠ PRODUCT SEMANTIC ≠ RUNTIME IDENTITY  
— NO REBRAND IMPLEMENTATION / NO BULK RENAME  
— AUTONOMOUS V1 UNCHANGED  
— NO IMPLEMENTATION  
— STOP FOR CEO REVIEW
