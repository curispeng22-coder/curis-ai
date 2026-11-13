# THREE-DOCUMENT CONSISTENCY AUDIT

Authority Class: REVIEW
Status: Frozen
Disposition: FINAL AUTHORITY CLEANUP COMPLETE — CANONICAL BUSINESS SPINE ACCEPTED — OPERATING LIFECYCLE APPROVED CANDIDATE — IMPLEMENTATION AUTHORIZED FOR BUSINESS SPINE ONLY — VISUAL DELTA PENDING
日期：2026-08-20
Owner：Product Architecture Authority
范围：Current Product Blueprint、Current Product Master Map、Current UI Blueprint

### 2026-08-20 Autonomous Business Operation — CEO Accepted / Approved Candidate

三份 Current Product Truth 已同步同一 Operating Lifecycle 产品语义：Operating Responsibility 默认持续；每个 bounded Cycle 正常 Close；Cycle Close 不等于 Business、Workspace 或 Responsibility 停止；PAUSE 暂停 Operating Series，STOP 终止当前 Operating Responsibility / Goal Series；CONTINUE / ADJUST 才能产生 exactly one next Cycle。Leader 只能在 Approved Strategy Envelope 内调整，Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget 与高影响/不可逆外部承诺进入 CEO Gate。

V1 证明等级已统一为 Primary Autonomous E2E（至少一个真实 Domain 连续两轮，并验证 restart、duplicate trigger、late result、WAIT / ESCALATE、CEO Gate）与 Cross-domain Contract Proof（第二个 Domain 证明同一 Lifecycle 可承载不同策略/团队/结果/信号/评估/风险语义）。本次只同步产品合同；Lifecycle Controller、Review/Learning、atomic continuation 与 Domain proof 仍是 Product → Implementation Gap，不代表 Runtime 已实现或接受。

### 2026-08-20 Canonical Business Spine Acceptance

CEO 已接受 Business canonical persisted identity 与 `Company → Department → Business → Workspace` 不变量。Business Direction 仅为 Strategy / Direction supporting truth，Project 仅为 legacy compatibility object；Business + First Workspace 采用原子创建，无法解析的旧 Workspace 进入 `UNRESOLVED → QUARANTINED`，Parent Resolver 固定为 `Workspace → Business → Department → Company`。主开发担任 Frontend Baseline Promotion Integration Owner；该接受解除实现授权，但不改变三份 Product Truth 的职责边界，也不等于当前 Runtime / Schema / Frontend 已完成。正式实现入口：`issues/20260820_canonical_business_spine_implementation_001.md`。

### 2026-08-19 Leadership Delta 增量审计

三份 Current Truth 已同步 Leadership / Responsibility Assignment / Operating Loop 语义：Leader 为 system-defined Responsibility Role；`Employee × Role × Scope` Assignment 是责任承载；Conversation 以 Assignment 为上下文并隔离同一 Employee 的不同 Scope；Workflow Result 回到 Workspace Truth 与 Workspace Leader，进入 Continue / Adjust / Escalate / Next Operating Cycle。2026-08-19 即时清理进一步统一组织阅读链为 `Company → Department → Business → Workspace → Role → Responsibility Assignment → Employee`，明确 Workspace Leader Workstation 与 Workspace-local Inline Workflow Editor 边界，并移除“研发工作台”作为全局名称的歧义。该增量现已由 CEO 接受并冻结为 Current Product Truth；Runtime 事实仍按 Implementation Truth 分层。

## 1. 审计结论

三份 Current Truth 已按 bounded CEO correction 对齐：Curis 是普通用户可使用的 AI Company OS；Company OS 固定、Workspace 开放；七个一级产品空间共同承载经营闭环；产品组织链为 `Company → Department → Business → Workspace → Role → Responsibility Assignment → Employee`。Business 负责同类 Workspace 的分类/聚合并持有 Business-level Goal / Strategy；每个 Workspace 负责自己的 Workspace-level Goal / Positioning / Strategy，同时受所属 Business 整体方向约束，不创建 Default → Override 技术模型。2026-08-18 新增 Operating Work Directory 与 Leader Work Surface：业务空间提供 [部门] / [业务] / [工作空间] 直接入口，Organization Center 只负责结构与行政，Leader 是带 Responsibility Scope 的普通 Employee。长期 Workspace 必须有 Workspace Leader / Operating Team 承载；Workflow 仅在 Workspace 内以轻量 Inline Workflow Editor 存在，不形成独立 Workflow Console / 自由 DAG。Department / Business Work Surface 现定位为 Shared Management Surface Contract Candidate，后续由 Domain-specific Operating Surface 叠加；空间工程优先读取并复用当前 Company Truth，按需 Reuse / Create / Adjust。Product Blueprint 定义产品是什么，Master Map 展开页面/对象/动作，UI Blueprint 将其转译为空间与交互；三者不互相改写职责。本轮已完成窄范围 authority cleanup，不进入代码或 Runtime；下一步是 Workspace Leader visual delta。

本审计只检查 Current，不把 Research、Review 历史快照或 Archive 当作当前规则。历史审计快照见：
`docs/99_Archive/Product/THREE-DOCUMENT_CONSISTENCY_AUDIT_2026-08-18_Historical_Snapshot.md`。

## 2. Current Authority

| Authority | Current 文件 | 职责 |
| --- | --- | --- |
| Product | `docs/01_Product/Curis_Product_Blueprint.html` | Curis 身份、产品空间、核心关系、经营循环与产品原则 |
| Product Structure | `docs/01_Product/Curis_Product_Master_Map.md` | 页面使命、入口、字段、动作、创建/编辑、下钻、反向入口和来源 |
| UI | `docs/01_Product/Curis_Product_UI_Blueprint.html` | IA、空间模型、导航、交互、状态表达、渐进披露与 Workspace UI |
| Frozen Authority | `docs/07_Decisions/` 与适用 Frozen 设计/Company OS 文档 | 不能被 Current 文档静默覆盖的上位约束 |

## 3. Current 产品一致性

### 3.1 七个一级产品

三份文档统一为：

1. CEO 工作台
2. 业务空间
3. 组织中心
4. 人才与能力
5. 经营洞察 / Operating Intelligence
6. 资料库
7. 会议

Conversation 是独立工作 Surface，不是一级导航；Settings 从头像或上下文进入；CEO Assistant、搜索、最近工作、通知/待处理是 Global Capability，不是 Global Topbar 或一级导航。

### 3.2 Company Map / Organization

三份文档统一表达：

`Company → Department → Business → Workspace → Role Structure → Employee Binding`

公司版图回答公司长成什么样、业务扩张到哪里；员工目录从 Employee 反查 Role、Business、Department。Department 通常按重复责任、稳定协作和共享能力渐进形成，但新 Company 默认包含两个 Support Department：

- 空间工程部
- 数据分析部

它们不是 Business，也不是用户必须填写的组织表单。Company Analyst 属于数据分析部；Business Analyst 可由数据分析部 Assignment / Allocation 支持 Business，也可由成熟 Business 自建分析 Role / Employee。

### 3.3 Talent & Capability / Employee / Workspace

- Expert、Skill、Connector 属于“人才与能力”外部能力生态；专家只有完成招募、公司身份、岗位/责任和必要授权后才成为 Employee。
- Skill 以职业能力组合 / 岗位能力包进入员工配置，不要求普通用户从零拼插件。
- 招聘是外部专家 → Company Employee；组队是已有 Employee → Workspace 团队；员工身份不复制。
- Workspace = 专家团队 + 专业工作环境 + 自动协作方式；不同 Workspace 可以拥有不同专业 UI，不收敛为统一 Runtime / Workflow 页面。
- Business Space 是 Operating Work Directory，按 Business 聚合但提供 [部门] / [业务] / [工作空间] 三种直接入口；Business Work Surface 承担整体管理，Workspace 可直接进入；Duplicate Workspace 与 Duplicate Business 分开，External Account / Operating Object 不构成全局层级。

### 3.4 Operating Intelligence

经营洞察是独立第七一级产品空间，消费已有 Company Truth、Result、Usage、Cost、Execution、Feedback、Review；不创建第二套 Truth、Result 或 Analytics Runtime。

IA 统一为：公司经营、业务分析、组织与员工、模型与能力、分析报告、专项研究。Report 由真实 Analyst Employee 负责，正文区分 FACT、INTERPRETATION、UNKNOWN、RECOMMENDATION、EVIDENCE；解释不能升级为 Company Fact。

指标必须保留 scope、period、source、freshness、collection mode、unknown/stale/missing/external 语义。External 未连接不得显示 0；图表只能在同 Dataset 的语义兼容表达之间切换；没有 Calculation / Threshold / Evaluation Contract 不生成健康或综合评分。

### 3.5 Business Duplication / Exit / CEO Continuity

- Business Duplication 复用已验证 Business Definition / Rules 与经营方法，创建独立 Business Identity；不复制统一 Workflow / Role / Employee Binding 母模型，也不复制 Employee identity、Credential、Conversation、Execution、Result、Evidence、History 或 Runtime state。新业务回到同一 Company Map、Business Space 和对应 Workspace。
- Business Exit 是 Business Work Surface 的跨层动作：Pause、Reduce、Transfer、Close、Merge、Split；保护承诺、责任交接、释放/重分配 Employee/Capability/Capacity，并保留 History/Evidence/Result/Learning。不新增 Exit Center 或 Runtime Primitive。
- CEO Operating Day 通过 Brief、Matters、Handoff、Decision、Exception、Evidence、Learning、Closeout 跨日承接未完成责任、未决决定、风险与 Follow-up。不新增 OperatingDay 页面或 Runtime Primitive。

### 3.6 Shared Management Surface / Domain Surface

- Department Work Surface 与 Business Work Surface 共享 Identity、Leader Workstation、Responsibility、Goal、Current Focus、Children、Result / Risk、Team 摘要、Management Actions 与 Escalation 骨架；团队运转只属于 Workspace。
- 共享骨架不规定 Domain 最终页面；产品表达为 `Shared Management Shell + Domain-specific Operating Surface`。内容增长部、研发部、小红书运营与 Curis 产品研发需通过后续 UX Exploration 验证差异。
- 空间工程流程为 `Operating Intent → Read Current Company Truth → Structure Proposal → Reuse / Create / Adjust → Impact Preview → Decision Gate（必要时）→ Apply to same Company Truth`，不拥有第二套 Organization Truth。

### 3.7 Business Work Surface / Workspace Workflow

本轮 Final Structure Correction 已将上一轮复杂模型收敛：

- Business 页面是运行说明 / 经营定义，不是 Settings 后台或 BI Dashboard；固定连续结构为 Business Definition → Operating Status → Workspace Directory → Business Team。四个 Part 是信息架构责任，不是四个平级 Tab 或强制 Card。Workspace Directory 只展示 Workspace Name、Leader、轻量 status / focus / issue、成员摘要、直接进入和新建。
- Business 只共享 Business Introduction、Business-level Goal / Direction 与通用 Rules / Configuration；Rules / Configuration 以 `Title / Name + Content` 为最小语义，不预先发明行业字段 Schema。
- 每个 Business 至少拥有一个 Workspace；每个 Workspace 独立拥有 Goal、Rules、Team Operating、Role / Responsibility Assignment、Operating State 与 Result。Business 页面不嵌入 Workspace 详细工作面，点击目录直接进入 Professional Workspace；Business 不拥有统一 Team Operating，也不形成 Master Team Operating → Override / Inheritance / Migration。
- Team Operating 的产品语言是“团队运转 / 默认流程”。`A → B` 仅表示 A 产出 accepted Result 且没有更强的 Consult、Review、Return、Need、Leader、Decision、Wait 或 Domain rule 时，B 为默认下一 Responsibility；不是强制运行序列或任意 DAG 边。Workflow / Router / DAG / State Machine 仅属内部 Runtime / Audit 语言；编辑动作映射到真实 Responsibility Contract、scoped Assignment、Context Contract、Result Contract 与 immutable Operating Definition Version。
- Workspace 可关联团队可用的 Model / Agent、Skill、Tool、Connector、Knowledge 等资源，但 Employee 的实际能力绑定仍只在 Employee Workstation，Workspace 不维护第二套 Employee Capability Truth。
- Goal、Rules、Business Definition 与 Workspace Definition 默认通过 Conversation → Structured Proposal → 必要确认 → 写入 Truth → 更新摘要；Panel / Modal 只负责详情编辑和纠错。
- Department 不提供专业团队运转编辑器；Preset Domain 是可编辑 Professional Package，不是产品边界；未知业务可通过 Generic Business Definition、Generic Rules / Configuration、Workspace Team Operating、Role Structure 与 Workspace 使用。

本轮同步了 Product Blueprint、Master Map、UI Blueprint、Product Context、Business / Department / Organization contracts、CURRENT_STATE、Pointer 与 Change Log；未修改专业 Workspace、UX Exploration HTML、Frozen Employee Workstation、Runtime、Schema、数据库或代码。Generic Workspace 页面、Workflow Design Surface 最终视觉与 Workflow graph / routing / context injection / versioning / migration / rollback / 自动角色生成仍等待后续 Review。

### 3.8 Operating Hierarchy × Team Operating Engine reconciliation（2026-08-20）

- 固定 Current 阅读层级为 `Company → Department → Business → Workspace → Team / Responsibility Assignment / Employee Workstations`；Business 至少拥有一个实际 Workspace，不提供 Business-direct / Workspace 两套用户模式。
- Professional Workspace 由 Shared Workspace Shell、Domain-specific Primary Work Surface、Shared Team Operating、Shared Employee Work Area 组成；Domain Primary Work Surface 是页面最大区域，通用身份 / Goal / Rules / Current Operating Summary 保持轻量。
- 当前已接受的 Workspace-scoped Responsibility Routing / Team Operating Runtime Truth 已登记为 Implementation Truth，不由本轮产品文档重新定义；Business-scope Provider Execution 仍未实现且当前未被接受执行路径消费。

## 4. Source Authority 一致性

| 检查项 | 结论 |
| --- | --- |
| 产品身份与七区导航 | 一致，Product Blueprint 为权威 |
| 页面、对象、字段、动作 | 一致，Master Map 仅展开 Blueprint |
| 空间与交互表达 | 一致，UI Blueprint 仅消费 Product / Master Map |
| Default Support Organization | 一致，产品已确认；Runtime 是否已支持需看 Implementation Truth |
| Operating Intelligence | 产品与 UX Baseline 已消费；Runtime / 数据采集仍需实现证据 |
| Business Exit / CEO Cross-day Continuity | 产品语义已确认；未授权自行新增 Runtime Primitive |
| Business / Workspace Goal hierarchy | 一致：Business-level Goal / Strategy 约束整体方向；Workspace-level Goal / Positioning / Strategy 独立承载具体经营 |
| Shared Management Surface contracts | 一致：两份合同为 Shared Management Surface Candidate；Business 只提供 Workspace Directory，Domain-specific Surface 等待 UX Exploration |
| Business / Workspace / Team Operating | 一致：Business 管理 Workspace Directory；Workspace 承载 Domain Primary Work Surface、团队运转和 Employee Work Area；Default Flow 不等于强制序列 |
| On-demand Workspace Engineering | 一致：优先复用 Company Truth，按需 Reuse / Create / Adjust；未授权实现 planning / impact / atomic apply |
| Frozen Workspace Shell navigation | **RESOLVED**：Frozen Shell §1.1 / §1.3 已同步为七区 Navigation Authority，与 CEO Confirmed Current Product Truth 和三份 Current 文档一致 |

## 5. Product → Implementation Gaps

以下不是产品冲突，而是必须与 Implementation Truth 分开登记的 Gap：

- Default Support Departments / Company Analyst 的 Runtime 物化与默认绑定未由本审计证明。
- Operating Intelligence 的数据采集、Metric Registry、Report Runtime、外部业务指标与图表运行时未由本审计证明。
- Business Exit 的真实状态、责任交接、资源释放与历史保留仍需独立 Runtime/Simulation Issue。
- CEO 跨日连续性需要现有 Desk、Assistant、Meeting、Evidence/Result 的真实恢复证据；不因产品合同而声称已实现。
- Business Template 与 Business Duplication 的底层关系仍需独立 Authority/Schema 决策。
- Frozen Workspace Shell §1.1 / §1.3 已完成七区 Navigation Authority Sync；该项不再是 Product / Shell 冲突。
- Workspace-scoped Responsibility Routing / real Employee execution 已由接受的 Implementation Truth 覆盖；仍需独立证明的边界为 Business-scope Provider Execution、External live provider quality / cost、完整 RD/XHS migration 与 cross-layer automatic Leader escalation。

## 6. Follow-on Product / Implementation Gaps

本审计不重新设计产品。以下事项不阻塞本轮 Product Truth 冻结；若未来改变产品模型，必须另开明确的 CEO Review / Decision：

1. Workspace Workflow Design Surface 的最终 UI 承载位置；
2. Role 是否允许脱离 Business 独立创建；
3. Workspace Engineering 结果如何回写 Company Truth；
4. 外部 Expert/Skill/Connector 的正式接入、撤回与维护责任；
5. Business Template 与 Business Duplication 的 Runtime/Schema 关系。
6. Workflow Design Surface 的最终页面承载、版本与运行时回写方式。

## 7. Final Verdict

`OPERATING HIERARCHY × TEAM OPERATING ENGINE — FINAL AUTHORITY CLEANUP COMPLETE — THREE-DOCUMENT CURRENT TRUTH CONSISTENT — VISUAL DELTA PENDING`

本审计只修改产品治理文档与 Frozen Shell §1.1 / §1.3 的导航文字；没有修改 Runtime、Schema、数据库、代码、Prototype、Frozen Shared Patterns 或高保真设计。
