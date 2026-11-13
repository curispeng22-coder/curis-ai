# Curis · Workspace Engineering Methodology（空间工程方法论）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论定义（非 Frozen · 非高保真 · 非 Runtime · 非代码）
**日期**: 2026-08-22
**Owner**: Workspace Engineering Methodology Expert（空间工程方法论专家）
**上位约束**（不修改）:
- `docs/01_Product/Curis_Product_Blueprint.html`（v5.6 · Status: Frozen）
- `docs/00_Context/CURRENT_STATE.md`（Frozen）
- `docs/07_Decisions/ADR-0040-company-os-workspace-product-reset.md`（产品重置原则 Frozen）
- `docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`（业务运行完成标准 Frozen）

**铁律（本文件范围）**:
- ❌ 不 Frozen（保持 CANDIDATE / REVIEW）
- ❌ 不开发 Workspace Runtime
- ❌ 不修改 Product Blueprint / Frozen Shell / P1–P7 / XHS·RD Instance / 代码 / UI
- ✅ 仅定义「空间工程团队应如何把一个 CEO 经营目标转化为可运营、可进化的 Business Space / Professional Workspace 体系」的方法论

---

## 0. 阅读指引

本文是 Curis 空间工程（Workspace Engineering）的**总纲**。它回答三个问题：

1. **Workspace Engineering 是什么、为什么是 Curis 的默认核心能力？**
2. **它和「让用户自己画 Workflow / 配 Agent / 搭 Task DAG」的根本区别是什么？**
3. **它遵循哪一套可重复、可治理、可进化的方法？**

本文与另外 5 份文档构成完整方法论集：

| 文档 | 角色 |
|---|---|
| `Curis_Workspace_Engineering_Methodology.md`（本文） | 总纲：定义、哲学、角色、原则 |
| `Curis_Workspace_Engineering_Lifecycle.md` | 15 步生命周期（闭环，含步骤 6 Curis Workspace IA Composition） |
| `Curis_Workspace_Engineering_Gates_and_Acceptance.md` | 6 道 Gate + 7 项验收 |
| `Curis_Workspace_Engineering_Expert_Handoff_Protocol.md` | 领域专家 → 产品专家的 Handoff 协议 |
| `Curis_Workspace_Engineering_Content_Growth_Case_Study.md` | Content Growth 正确链复盘（Case Study） |
| `Curis_RD_Methodology_Gap_Review.md` | RD Workspace 方法论缺口审查（Gap，不重设计） |

---

## 1. Workspace Engineering 是什么

**Workspace Engineering = Curis 把「一个 CEO 的经营目标」转化为「一套可真实投入运营、并随时间持续进化的 Business Space / Professional Workspace 体系」的工程能力。**

它不是一次性的「画一个界面」，也不是「配置一组 Agent」。它是一条从**经营意图**到**运行现实**再到**经营进化**的端到端链路，并且这条链路在 Workspace 上线后**持续自转**。

Workspace Engineering 的目标产出是：

- 一个可复用的 **Business Space / Workspace Package**，以及由它物化的 Workspace Instance；
- 其背后支撑的 **Operating Model（经营方法）**、**Semantic Model（业务对象 / 关系 / 状态 / 责任 / 关键业务真相）**、**Shared / Domain Capability 映射**、**Workspace Design**、**Package Domain Schema**、**Acceptance 证据**与**进化回环**；
- 只有当局部语义跨多个 Instance 复用、成为官方 Domain 标准、影响 Company OS 或需要长期兼容保证时，才形成全局 Frozen Domain Authority。

### 1.1 它服务的对象

Curis 的定义是「自进化的 AI 公司」操作系统。研发、内容增长、销售、客服、电商等**不是 Curis 的固定业务本体**，它们是 Professional Workspace 形态示例或验证案例——CEO 根据自己的经营目标选择、配置或复用：

> 启用 · 不启用 · 新增 · 调整 · 进化

但无论用户怎么选，**Workspace Engineering 本身属于 Curis 的默认核心能力，必须存在。**

### 1.2 为什么必须存在（而不是交给用户自己搭）

Curis 的差异化**不是**：

> 让用户自己画 Workflow、配置 Agent、搭建 Task DAG。

Curis 的差异化**是**：

> CEO 表达经营目标 → Curis 空间工程理解业务 → 调专业专家研究真实业务 → 建立经营方法 → 转译为产品体验 → 搭建需要的业务空间 → 验收 → 投入运营 → 根据真实经营继续进化。

把「研究真实业务、建立经营方法、转译产品语言、搭建空间、验收、进化」下沉为 Curis 的系统能力，CEO 才不必成为「 workflow 架构师 / Agent 配置工程师 / 业务分析师」。这正是普通用户优先（ADR-0045）与 Company OS 固定经营语义（ADR-0040）的必然要求。

---

## 2. 核心哲学：从意图到进化的闭环

Workspace Engineering 的根本信条是——**业务不是被「配置」出来的，而是被「理解」出来的。**

```
CEO 经营意图
   ↓  （理解业务，不是让用户画流程图）
领域专家研究真实世界这门业务怎么经营
   ↓  （提炼方法，不是堆功能列表）
建立 Operating Model（目标/策略/规则/职责/方法/反馈/学习/进化）
   ↓  （收敛，不是把几十份 Research 扔给设计）
Product Handoff（一份可消费的专业输入）
   ↓  （翻译，不是把架构图搬上屏幕）
Product Translation → 普通用户能理解的产品语言
   ↓  （先组合长期信息架构，不是直接进能力审查）
Curis Workspace IA Composition / Curis Host Adaptation
   ↓  （复用优先，不是每 Workspace 重造一套）
Shared / Domain Capability Review
   ↓  （由业务反推空间，不是由页面清单反推业务）
Workspace Composition + Semantic Model + Workspace Design
   ↓  （Package First）
Package Composition → Core Expressibility Check
   ├─ Core 可表达 → Validate → Install → Run
   └─ Core 不可表达 → Core / Capability Gap → bounded Issue
                         → 扩展 Core → 回到 Package Composition
   ↓  （真实证据，不是 Mock/设计稿）
Acceptance → Go Live
   ↓  （运营中学习，不是只看 Analytics）
Operating Learning → Workspace Evolution ↺
```

**Relevant Gate 不可跳，但 Resolution 不机械生成。** 任何经营意图先读取 Current Company Truth，识别 Domain / Scope / Risk，搜索 Verified Match，再依次尝试 Instance Configuration、Maintained Derived 与 Safe Composition；只有 Domain Truth 不足时才插入 bounded Research，Generation 是 last resort。已验证 Template / Package 实例化可复用其版本化研究、Handoff、Translation、Design 与 Validation 证据，只做目标适配、能力检查、实例生成与验收；已有 Workspace 进化从受影响的最早阶段重新进入并重过相关 Gate。任何缺少适用 Gate 证据的路径，都会在下游以返工、伪完成或范围蔓延偿还（详见 Doc 6）。

### 2.1 CURRENT DELIVERY PATH 与 TARGET WORKSPACE ENGINEERING PATH

```text
CURRENT DELIVERY PATH（当前事实）
Workspace / Instance Design
→ Gap Audit
→ bounded Implementation Issue
→ Development Agent 修改 Curis 源码
→ 重新 Build / 验收

TARGET WORKSPACE STUDIO PRODUCT PATH（目标，未完成）
Workspace Design
→ Package Composition
→ Core Expressibility Check
→ Core 可表达：Validate → Install → Run（不改源码、不重新 Build）
→ Core 不可表达：Core / Capability Gap → bounded Issue → 扩展 Core → 回到 Package
```

当前已安装 Curis 已具备受控 Multi-Surface Workspace Package v2 的动态安装、验证、持久化与打包 Desktop 渲染基础；这不等于已具备用户可见的 Workspace Studio 动态创建、任意专业 Package 生成或完整迁移能力。Codex 能修改 Curis 源码，也不等于 Studio 产品已完成。

---

## 3. 角色定义

Workspace Engineering 不是「产品设计师一个人完成」，也不是「设计专家直接承担开发」。它是一组**职责分离、经 Handoff 中转**的角色协作：

| 角色 | 身份 | 核心职责 | 禁止 |
|---|---|---|---|
| **Workspace Engineering Methodology Expert** | 方法论主理人 | 维护本方法论、判定 Gate、审计链路完整性、在 Review 时收口 | 代替领域专家做业务研究；代替开发写代码 |
| **Domain Expert（行业/运营专家）** | 真实业务权威（如 Social Media Growth Expert、R&D Org Expert） | 研究「现实世界里这门业务到底怎么经营」，产出 Operating Model 与收敛 Handoff | 凭想象定义业务流程；把研究直接甩给设计专家 |
| **Product Expert / Designer（产品专家）** | 产品/设计专家 | 把专业经营方法翻译为普通用户可理解的产品语言与体验 | 把内部架构机械画给用户；重新解释领域研究 |
| **Capability / Connector Engineer** | 能力/连接器工程师 | 评估 Company OS 已有能力复用，定义缺失 Capability/Connector 需求 | 每 Workspace 重造 Runtime 原语 |
| **Development Agent（研发能力）** | Curis 研发能力 / Development Agent | 仅在 Core / Capability Gap 成立时执行 bounded Issue，扩展 Core 后回到 Package；当前过渡期执行明确标注的源码交付路径 | 自行定义业务；把修改源码当成目标默认路径；自行决定产品形态 |
| **CEO（经营决策权）** | 最终决策权威 | 在 Gate 与 Needs CEO 处拍板经营目标、策略边界、上线与进化 | 被迫配置路由/队列/组织等内部机制 |

**关键纪律**：领域专家与产品专家之间**必须经 Product Handoff 中转**（见 Doc 4）；目标路径中产品专家先交付 Semantic Model + Workspace Design + Package Composition，只有 Core Expressibility Check 失败才建立 bounded Issue。当前源码交付必须明确标注为 `CURRENT DELIVERY PATH`。任何「研究文档直接进设计」「设计稿直接进代码」都是违规。

---

## 4. Workspace Engineering 与 Company OS / Business Space 的关系

Curis 的层次（来自 CURRENT_STATE 与 Product Blueprint v5.4）：

```
Company OS（固定经营语义：Truth / Decision / Assistant / Change / 责任 / 交接 / 验收 / 进化）
   └─ Business Space / Professional Workspace（用户按经营目标启用/调整/进化的业务空间）
        └─ Operating Model（该业务的经营方法）
             └─ Semantic Model（对象 / 关系 / 状态 / 责任 / 关键业务真相）
                  └─ Workspace Design + Package Domain Schema（默认局部语义）
                       └─ Workspace Package → Instance
```

- **Company OS = 固定层**：责任、交接、验收、失败恢复、CEO 验收、资料来源、审计严谨性——这些是跨所有 Workspace 共享的「经营语义底盘」，不因业务而变。
- **Business Space / Professional Workspace = 开放层**：研发、内容增长、销售、客服、电商……都是这一层的实例。它们**不是 Curis 本体**，是模板与实例。
- **Workspace Engineering = 连接两层的工程能力**：它把开放层的业务「理解并落位」到固定层的语义底盘上，使每个业务空间既独立演进、又共享 Company OS 的真相/责任/验收基础设施。
- **Package Domain Schema = 默认局部层**：普通用户自定义 Workspace 只需在 Package 内明确局部业务语义，不要求先建立全局 Frozen Authority。
- **Domain Authority = 条件升级层**：仅在语义跨多个 Instance 复用、成为官方标准、影响 Company OS 或需要长期兼容保证时进入 Frozen 流程。

> 判据：如果一个新业务空间「重新发明了一套责任/交接/验收/失败恢复」，说明它没有走 Shared / Domain Capability Review（Lifecycle 第 7 步），违反了本方法论。

---

## 4.1 长期 Workspace = Operating Team + Professional Workspace（上位产品规则）

Curis 是公司组织经营系统。任何长期 Workspace 都不能只是一个页面或专业界面，必须同时由一支真实 Operating Team 承载——团队有 Leader、有成员、有明确职责。这是 Company OS 全局经营规则，高于任何 Domain / Instance（正式定义见 Company OS Shared Authority §9 · Frozen）。Business 是同类 Workspace 的分类 / 聚合层，不等于 Team + Workspace 的单一副本。

对 Workspace Engineering 的直接含义：

- **任何长期业务必须有真实 Operating Team**（Leader + 成员 + 明确职责）。
- **Team Leader 是 CEO 对该业务的主要入口（双重语义必须区分）**：
  - **(a) 业务领导**：Leader 持续负责目标落地、策略执行、团队协作、结果汇总、异常判断与 CEO 沟通——始终在业务中，**绝不等于「平时不参与」**。
  - **(b) 任务路由**：普通任务由 Organization Routing 自动解析，Leader 只在异常 / 管理判断时手动介入。`TEAM_LEAD_ONLY_ON_EXCEPTION` 仅约束 (b)，不得上推到 (a)。
- **CEO 默认通过 Leader 经营，但可随时进入具体员工的工作**，与员工直接讨论和调整。
- **CEO Assistant / Leader / Employee 三层，不是二选一入口**：CEO 可先与 Assistant 讨论新业务、再交空间工程部，也可直接找空间工程 Leader；两入口进入同一真实 Department Responsibility / Work Context，不形成两套工作。Assistant 可协调 / 监督 / 汇报 / 升级，但**不能替代**专业部门完成行业研究、经营策略、设计、实施、Quality 等职责（正式定义见 Shared Authority §9.3 · Frozen）。
- **Conversation 必须围绕真实职责、工作、经营方法和结果运转**，不形成独立聊天世界。
- **员工之间通过真实工作结果和必要的 Handoff 协作**。
- **不同业务的经营方法、岗位分工、专业 UI 可以不同，但团队协作方式属于 Curis 全局 Company OS 规则**（Shell Contract / P1–P7 Shared Patterns 提供统一协作骨架）。
- **空间工程创建长期 Workspace 时，必须同时创建 / 组队 Operating Team + Professional Workspace**（详见 Lifecycle 步骤 8 与 Gates Doc 3 验收第 8 项）。
- **没有真实团队承载的长期 Workspace，不得算空间工程完整成功。**
- **本规则仅约束长期经营业务的终态，不扩大到「所有 Curis 工作必须建立 Business / Workspace」**：临时 Conversation / Task、单 Employee 工作、多 Employee 临时 Task Team 均合法；任一阶段可合法停止，不强制升级（渐进工作形态见 Company OS Shared Authority §9.7 · Frozen）。空间工程是 CEO 可委托的专业建设路径，**不是**创建 Business / Department / Workspace 的唯一入口——CEO 也可自建、把临时团队升级为长期业务，或从轻量工作开始。

> 纪律：上述团队承载规则是上位产品规则。空间工程团队自身另有一套专属岗位结构（见 §9），但该结构**不是**所有业务的统一团队模板。

---

## 5. Workspace Engineering 不是什么（边界铁律）

| ❌ 不是 | 为什么 |
|---|---|
| 让用户自己画 Workflow / 配 Agent / 搭 Task DAG | 这把「业务分析师 + workflow 架构师」的负担转嫁给 CEO，违背普通用户优先 |
| 产品设计师凭想象定义业务流程 | 真实经营方法必须来自领域专家对真实世界的研究，不是产品直觉 |
| 设计专家直接承担开发职责 | 设计与实现分离；开发由 Curis 研发能力 / Development Agent 执行 bounded Issue |
| 每 Workspace 重新造一套 Runtime 原语 | Shared / Domain Capability Review 强制复用 Employee / Responsibility Routing / Context Isolation / Handoff / Decision / Result Reference / Computer Access |
| 把「几十份 Research 直接扔给设计专家」 | 领域专家必须先收敛为单份 Product Handoff（见 Doc 4） |
| 用 Mock / 设计稿 / 接口数量冒充完成 | Acceptance 要求 Business Truth / Runtime Truth / Persistence / Failure Truth 等真实证据（见 Doc 3） |
| 上线后只看 Analytics 即判定成功 | Operating Learning Gate 要求判断「经营方法本身是否需要进化」（见 Lifecycle 第 14 步） |

---

## 6. 十五条核心原则（Doctrines）

1. **意图优先（Intent First）**：一切从 CEO 经营目标出发；不先谈页面、Agent、DAG。
2. **真实业务优先（Reality Over Imagination）**：经营方法必须来自领域专家对真实世界的研究，禁止产品凭想象定义业务。
3. **理解而非配置（Understand, Not Configure）**：Curis 理解业务，CEO 不必成为配置工程师。
4. **收敛 Handoff（Convergent Handoff）**：领域研究必须先收敛为一份可消费的 Handoff，再交产品专家。
5. **翻译而非搬运（Translate, Not Port）**：产品专家把专业语言翻译成用户语言；内部架构不进用户视野。
6. **复用优先（Reuse First）**：搭新 Workspace 前先查 Company OS 已有能力：REUSE / EXTEND / DOMAIN SPECIFIC / MISSING。
7. **由业务反推空间（Business-Drives-Surface）**：真正需要哪些 Business Home / Professional Workspace / Context / Utility / Employee / Presence / Conversation / Evidence，由经营方法决定，不由「页面清单」反推。
8. **真实证据（Real Evidence）**：验收以真实运行、真实持久化、真实失败恢复为准，Mock 不算完成。
9. **闭环自转（Closed-Loop Self-Rotation）**：上线不是终点；运营数据 / 用户反馈 / Employee 经验 / 异常必须回流到领域研究与产品 Review，驱动进化。
10. **Relevant Gate 不可跳（No Relevant Gate Skipping）**：每个适用 Gate 必须有当前或可复用的有效证据；不要求每次机械重跑完整生命周期（见 Doc 3）。
11. **Professional Workspace Before Package**：先从经营模型推导 Domain Navigation、多个 Professional Surface、Surface 所需 Responsibility、对象 / Detail 映射与共享 Truth 投影，再形成 Package Candidate；不得从菜单、页面或 Employee ID 反推业务模型。
12. **Package First**：目标默认交付物是声明式 Package；只有 Core 无法表达时才建立 Core / Capability Gap，并在 Core 扩展后回到 Package。
13. **Semantic Model Before Instance**：任何 Workspace 搭建前必须明确业务对象、关系、状态、责任与关键业务真相；局部语义先落 Package Domain Schema，不默认升格全局 Authority。
14. **长期 Workspace = Operating Team + Professional Workspace**：任何长期 Workspace 必须由真实 Operating Team（Leader + 成员 + 明确职责）承载；Business 可以聚合一个或多个独立 Workspace，不要求共享同一 Team；无真实团队承载的长期 Workspace 不算完整成功（见 §4.1 / Shared Authority §9 · Frozen）。
15. **渐进工作形态（Progressive Work Forms）**：Curis 同时支持 临时 Conversation / Task → 单 Employee 工作 → 多 Employee 临时 Task Team →（必要时）长期 Operating Team + Business Workspace；任一阶段可合法停止，不强制升级。空间工程是可委托的专业建设路径，不是创建 Business / Department / Workspace 的唯一入口（见 Shared Authority §9.6–§9.7 · Frozen）。

---

## 7. 与既有 Curis 治理的关系

| 既有治理 | 本方法论如何对齐 |
|---|---|
| ADR-0040（Company OS / Workspace 产品重置） | Workspace Engineering 是 ADR-0040「开放 Workspace」落地的工程方法；固定 Company OS，开放 Workspace |
| ADR-0041（业务运行完成标准） | Acceptance（Doc 3）的 7 项检查是 ADR-0041 在「空间工程交付」上的具体化 |
| Blueprint 变更顺序（Definition → Runtime Blueprint → UI → Code） | 新业务首次创建仍先完成 Definition / Operating Model / Product Translation；其后经 Curis Workspace IA Composition（长期信息架构组合）；目标后半段改为 Workspace Design → Package Composition → Core Expressibility Check。只有 Gap 成立才进入 bounded Core 实现；顺序一致，不倒置 |
| 文档状态纪律（Draft/Review/Frozen） | 本方法论集保持 `Status: Review / APPROVED CANDIDATE`，不 Frozen；只有满足跨 Instance / 官方标准 / Company OS 影响 / 长期兼容条件的领域语义才另走 Domain Authority 流程 |
| 文档指针 / Change Log | 本轮 Approved Candidate 已登记 `PRODUCT_DOCUMENT_POINTER.md`、CURRENT_STATE 与 Change Log；该登记不等于 Frozen 或 Runtime 授权 |

---

## 8. 本方法论集的使用方式

- **新业务空间首次创建**：默认走完整 Lifecycle，并逐项提供 Gate 证据。
- **已验证 Template 实例化**：只走 Business Intent → Template Match → Goal 适配 → Capability Check → Instance 生成 → Acceptance / Activation；研究、Handoff 与 Translation 证据从匹配的 Template 版本复用。
- **已有 Workspace 进化**：从受影响的最早阶段重新进入，重过所有相关 Gate；不受影响的上游证据可复用。
- **审计一个已有 Workspace 是否「方法正确」**：用 Doc 6 的 Gap 审查法，对照 Lifecycle 逐环判定 present / weak / missing。
- **判断领域专家是否达标**：对照 Doc 4 的 Handoff 协议与质量清单。
- **判断产品翻译是否达标**：对照 Lifecycle 第 5 步与 Content Growth Case Study（Doc 5）的反面教材边界。

---

## 9. 空间工程团队自身组织结构（非所有业务的统一模板）

本节定义**空间工程团队自己的岗位责任链**。这是「负责把一个 CEO 经营目标转化为可运营、可进化 Workspace 体系」的团队结构——它只描述空间工程这一 Curis 默认核心能力的内部组织方式。

> ⚠️ **重要边界**：以下岗位是**空间工程团队自身**的岗位，不是 Company OS 所有业务的统一团队模板。各业务团队（Operating Team）的具体角色分工由各自 Domain Expert 的经营方法决定（见 §4.1），不得强制所有业务采用与空间工程相同的岗位结构。

### 9.1 空间工程岗位责任链

```text
CEO（经营决策权）
  → 空间工程 Leader（方法论主理 + 链路统筹 + Gate 判定）
      → 行业研究（Domain Expert：研究真实世界这门业务怎么经营）
      → 经营 / 运营专家（Operating Model + Product Handoff 收敛）
      → 产品 / 空间设计（Product Expert：专业→用户语言翻译 + Workspace 设计）
      → 搭建实施（Development Agent / Workspace Engineer：Package / 源码交付）
      → Quality / 验收（独立验收：真实证据验收）
      → 最终交付给新业务团队（Business Operating Team：Leader + 成员）
```

### 9.2 各岗位责任（空间工程团队内部）

| 岗位 | 责任 | 禁止 |
|---|---|---|
| 空间工程 Leader | 统筹端到端链路、维护方法论、判定 Gate、在 Review 收口、确保业务团队 + 办公室一并交付 | 代替领域专家做业务研究；代替开发写代码 |
| 行业研究（Domain Expert） | 研究真实世界经营实践，产出 Operating Model 与收敛 Handoff | 凭想象定义业务流程；把研究直接甩给设计 |
| 经营 / 运营专家 | 提炼经营模型、收敛为单份 Product Handoff | 把几十份 Research 直接扔给设计 |
| 产品 / 空间设计 | 专业经营方法 → 用户语言；Workspace Design；引用 Frozen 不重定义 | 把内部架构机械画给用户；自行重定义领域语义 |
| 搭建实施（Development Agent） | 仅在 Core / Capability Gap 成立时执行 bounded Issue；当前过渡期执行明确标注的源码交付 | 自行定义业务；把修改源码当默认路径 |
| Quality / 验收 | 独立以真实证据验收 7+1 项（含 Operating Team Presence）+ §2.1 长期办公室 6 项检查 | 用 Mock / 设计稿 / 接口数量冒充完成 |
| 交付对象：新业务团队 | 接收已启用 Workspace 与其 Operating Team（Leader + 成员）；由该业务 Leader 对 CEO 负责 | — |

### 9.3 与其他结构的关系

- 空间工程团队是 Curis 的**默认核心能力团队**，不属于某个 Business Space。
- 它交付的「新业务团队」是 Business Operating Team（见 §4.1 / Shared Authority §9 · Frozen），由该业务自身 Domain Expert 决定的角色分工承载，不是空间工程岗位结构的复制。

---

## 10. 状态与下一步

### 10.1 Three-Layer Operating Model sync（CEO Accepted 2026-08-20）

本方法论继续作为 Employee Operating Layer 的研究、Handoff、翻译与 Package 组合方法，不成为 Runtime 或第四套产品真相。User Surface 只消费 CEO 可理解的经营责任、结果、缺口与下一步；System Runtime 继续复用 Company OS 的责任、证据、权限、版本和恢复合同。Workspace Package 的产品语义收敛为 **Domain Operating Capability Package**；Professional UX / Interaction 是 Package 一等资产，但仍采用受限、可验证的声明式 registry；Package method metadata 的持久化/版本化仍是 Future Capability Architecture / Product → Implementation Gap。
本方法论同时消费 Professional / Generic、Curis Official / Partner / Community / User or AI Generated、Verified / Candidate / Unverified / Deprecated 三轴质量模型。Official 不等于 Verified，Generated 默认是 Candidate；XHS / RD / 电商仅为验证案例，不是 Core Domain 或默认模板。

不新增 Playbook 对象。专业方法由本方法论的 Handoff、Package 方法元数据、Skill composition、Operating Definition 与 Result / Evaluation / Review 分工承载。XHS / RD / 其他行业只作为可替换的 Domain 例证，不成为空间工程的固定业务模板。

```text
WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE
```

- 本文件与另外 5 份同处 `Status: Review / APPROVED CANDIDATE`，**未 Frozen**。
- 引用的 **Company OS Shared Authority §9（长期 Workspace = Operating Team + Professional Workspace）已由 Current Authority Frozen**（Business 聚合 Workspace；渐进工作形态保留；空间工程可委托、非唯一入口）。本方法论集不重定义该 Authority，仅引用。
- 2026-08-16 Methodology Delta：Lifecycle 新增步骤 6 Curis Workspace IA Composition / Curis Host Adaptation（基于 `docs/03_Design/WORKBUDDY_PROJECT_TO_CURIS_WORKSPACE_LONG_TERM_IA_REVIEW.md` 的 IA 结论，不重做研究）；Acceptance 新增 §2.1 长期办公室 6 项检查。仍保持 APPROVED CANDIDATE / Review，不 Frozen。
- 不修改 Product Blueprint / Frozen Shell / P1–P7 / XHS·RD Instance / Runtime / 代码 / UI。
- 受控声明式 Package P0 / P0.5 与 Multi-Surface Workspace Package v2 foundation 已完成既有验收；Canonical Child Work foundation 与 sequential cross-professional multi-Work proof 已由既有 commits 接受。Parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping、Professional UX registry 与完整 Studio productization 仍为 Gap。本次只对齐方法论，不授权继续实现。

---

*Curis Workspace Engineering Methodology · APPROVED CANDIDATE / Review（非 Frozen · 非 Runtime · 非代码）*
