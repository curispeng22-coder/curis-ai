# CURIS PAGE CONTRACT CANDIDATE — BUSINESS WORK SURFACE

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CEO FINAL STRUCTURE CORRECTION APPLIED — READY FOR BUSINESS UX VISUAL DELTA  
**性质：** Business Space 内的 Business 管理工作面；属于所有 Domain 都需要的 Shared Management Surface Contract Candidate，不是新一级导航、非 Runtime / Schema / Database / Code 设计。

## 1. Contract Position

本合同定义所有 Domain 都需要的共享管理职责：Identity、Leader Workstation、Responsibility、Goal、Current Focus、Children、Result / Risk、Team 摘要、Management Actions 与 Escalation 关系。Workflow 不属于共享管理骨架；它只属于具体 Workspace。合同不规定所有 Domain 的最终视觉或具体专业工作方式。

产品表达固定为：

```text
Shared Management Shell
+ Domain-specific Operating Surface
```

内容增长、研发及其具体业务（例如小红书运营、Curis 产品研发）必须通过后续 UX Exploration 验证差异，不在本合同内预先做成同一页面。

## 2. Mission

Business Work Surface 是 Business Leader 的真实管理与经营工作面。它回答：

> 这项 Business 现在要达成什么、由哪些工作空间承担、哪些责任正在推进、哪里需要 Business Leader 或 CEO 判断？

### Leader / Assignment / Operating Loop Contract

Business Leader 是普通 Employee 的 Leadership Role，负责 Business Definition、Business-level Goal / Strategy、Rules、Workspace 集合与整体 Result / Risk，不是静态负责人字符串或 Admin。页面 Leader 必须投影真实 `Employee × Role × Scope` Assignment；同一 Employee 可同时担任 Business Leader、Workspace Leader 与普通 Workflow Role。

Business Work Surface 不复制 Employee Identity Conversation。进入 Business Leader 时上下文为该 Business Scope；进入 Workspace / Workflow Role 时切换到对应 Assignment Scope，并保持 Conversation Context 隔离。Workspace Workflow 完成后，Result 回到 Workspace Truth → Workspace Leader，再由最低有效责任范围决定继续、调整、升级或等待，不要求 CEO 重新派每一轮工作；跨 Workspace 或 Business 级问题才回到 Business Leader。

它承载整体业务管理职责，不再创建重复的业务整体页面。低频编辑使用 Focus / Edit / Settings-like configuration surface，不创建第二个 Business 页面。

## 3. Entry / Return

入口：

- Business Space → [业务] → Business；
- Business Card / Business Name；
- Company Map 的 Business Node；
- CEO Desk、Employee Profile、Workspace、Meeting、Assistant、经营洞察的 Business scope；
- Search / Recent。

返回必须恢复 Company、Business、Department、Office、Leader、Matter / Result、Filter、Focus 和未完成输入。Business Work Surface 可直接进入任一 Workspace，不强制逐层经过 Organization Center。

## 4. Business Work Surface Structure

Business 页面是该业务的运行说明 / 经营定义，也是 Business Leader 管理下属 Workspace 的连续工作面；它不是传统 Settings 后台，也不是 BI Dashboard。四个 Part 是信息架构责任，不要求绘制为四张大 Card 或四个平级 Tab。

### Part 1 — Business Definition

标题 / 简介之后靠前放置由真实 Business Leader Assignment 投影的 Business Leader Employee Workstation，再以摘要表达：

- 业务介绍；
- Business-level Goal / Direction；
- Rules / Configuration 摘要。

完整规则通过右侧 Panel / Modal 按需查看和编辑。Business Leader 是真实 Employee，负责维护业务介绍、整体方向、Rules / Configuration，并持续与 CEO 对话；不是静态负责人字段，也不创建新的 Employee 类型。

### Part 2 — Operating Status

只表达结论优先的 Business 整体经营状态：Current Focus、Overall Progress、Important Result、Problem / Risk，以及需要 Business Leader 处理的事项。详细趋势、比较、归因和指标进入经营洞察，不在 Business 页面复制 Dashboard。

### Part 3 — Workspace Directory / Portfolio List

Business 页面提供 Workspace Directory：`[Workspace A] [Workspace B] [Workspace C] [+]`。`+` 是新建 Workspace 入口，位于目录区域，不放页面顶部或底部大 CTA。每条 Workspace 记录只表达 Workspace Name、Workspace Leader、轻量 status / focus / issue、可选成员数、直接进入 Workspace；Business 不在此展开 Workspace Goal、详细 Rules、Progress、Problem、Team Operating、Employee Workstations 或 Workflow 编辑器。点击 Workspace 直接进入真正的 Professional Workspace。

Workspace 详细 Goal / Rules / Team Operating / Workflow 只在 Workspace 内承载。Business 只保留目录与聚合投影，不嵌入一个缩小版 Workspace，也不提供 Business-direct / Workspace 两套用户模式。

### Part 4 — Business Team

只显示当前 Business 相关人员的轻量列表：姓名、Role、所属 Workspace / Responsibility 摘要。它不重复完整 Employee Workstation，详细组织关系回到 Organization Center；Business Leader 的完整 Workstation只在 Part 1 出现。

## 5. Business Definition / Workspace Operating Configuration

Business Work Surface 用经营语言表达：

- Business-level Goal、Business-level Strategy、Positioning、Audience；
Business 定义所有下属 Workspace 共同理解的业务语义：

- Business Introduction / Domain Definition；
- Business-level Goal / Direction；
- 通用 Rules / Configuration；
- Business-level Quality、Compliance 与 Output 要求；
- 参与该 Business 的 Workspace 集合与人员摘要。

Rules / Configuration 是通用容器，每项至少有 `Title / Name` 与 `Content`。不同 Domain 通过内容表达差异，不预先发明行业字段 Schema；完整内容默认不铺满 Business 页面。

每个 Workspace 独立拥有自己的 Goal、Rules / Configuration、Team Operating、Role / Responsibility Assignment、Operating Object / Account、Current Operating State、Result 与 Domain-specific Professional Work Surface。Business 只共享 Business-level 语义，不规定所有 Workspace 使用同一个 Team Operating，也不建立 Master Workflow → Override / Inheritance / Migration 模型。

Workspace 可以关联并提供团队可用的 Model / Agent、Skill、Tool、MCP / Connector、Knowledge、Permission 等资源，作为专业工作环境的能力投影；Employee 的实际能力绑定与工作模式仍只在 Employee / Employee Workstation 配置，Workspace 不维护第二套 Employee Capability Truth。

Team Operating 的产品语言是“团队运转”，主区可显示“默认流程”。`A → B` 只表示 A 产出 accepted Result 且没有更强的 Consult、Review、Return、Need、Leader、Decision、Wait 或 Domain rule 时，B 是默认下一 Responsibility，不是强制运行序列或任意 DAG 边。编辑动作映射为 Reorder→Default Flow、Responsibility→Responsibility Contract、Employee Binding→scoped Assignment、Input→Context Contract、Output→Result Contract、Save→immutable Operating Definition Version；运行中的工作 pinned 旧版本。Workflow / Router / DAG / State Machine 仅属内部 Runtime / Audit 语言。

Employee 绑定 Role 后自然承担该 Workspace Workflow 节点的 Responsibility；Employee 的 Model、Skill、Tool、MCP / Connector、Knowledge、Permission、Work Mode 仍在 Employee Workstation 配置。实际执行上下文由 Business Context + Workspace Context + Role / Responsibility Context + Employee Capability Context 共同形成。

规则、目标、Business Definition 与 Workspace Definition 的主要创建路径是 CEO / User ↔ Assistant / Business Leader → Structured Proposal → 必要确认 → 写入 Business / Workspace Truth → 页面更新摘要。Panel / Modal 只用于查看、精确编辑和纠错，不是主要创建方式。

## 6. Responsibility / Workflow Routing

工作默认在最低有效责任 Scope 自动完成：

```text
Role / Employee
→ Workspace Responsibility
→ Business Responsibility
→ Department Responsibility
→ Company / CEO
```

Workspace 内部的文案→Review→发布→分析等正常流转不经过 Business Leader。只有 Workspace 无法解决、跨 Workspace 协调、Business 整体策略/资源问题或 Business-level Decision 才进入 Business Leader。跨 Business、Department 资源/优先级问题才向上进入 Department；跨 Department、高风险、不可逆或 CEO Decision Gate 才到 CEO。

Business Leader Workstation 必须真实接收本 Scope 的 Responsibility、Handoff、Exception、Decision Request、Follow-up，而不是只显示名字。

Department Work Surface 不提供专业 Workflow Builder；Department 负责 Department Goal、Department Leader、Business Portfolio、跨 Business 协调、Resource、Result / Risk。具体业务规则、Workspace Workflow 与 Role Structure 进入 Business Work Surface / Workspace Management。

## 7. Workspace Relation

```text
Business（分类 / 聚合）
├─ Workspace A（独立经营单元）
├─ Workspace B（独立经营单元）
└─ Workspace C（独立经营单元）
```

每个 Business 至少拥有一个实际 Workspace；一个 Business 只有一个 Workspace 是正常状态。Business 是 Management / Aggregate View，Workspace 是 Execution / Professional Operating View；Business 页面不复制 Workspace 的详细工作面。

Business 持有 Business-level Goal / Strategy；不同 Workspace 各自持有 Workspace-level Goal / Positioning / Strategy。Workspace 默认独立配置，不默认共享彼此的 Workspace-level Goal / Strategy、员工、能力、知识、凭证、排期、Result 或当前运行状态；它们仍共同服务所属 Business-level Goal / Strategy。Business Work Surface 提供 Workspace 入口、整体聚合与 Business 级判断，不替代专业 Workspace。

## 8. Actions

- 编辑 Business Identity、Goal、Positioning、Audience、Strategy；
- 查看 / 调整 Business Definition / Workspace Operating Configuration 摘要；
- 进入 / 复制 Workspace；
- 查看 Business Result、Risk、Blocker、Staffing、Resource；
- 处理 Business Responsibility、Handoff、Exception、Decision Request、Follow-up；
- 进入 Organization Center 调整 Role / Staffing / Leader Assignment；
- 进入人才与能力、资料库、经营洞察、会议；
- Duplicate Business；
- Pause、Reduce、Transfer、Close、Merge、Split（动作前展示责任保护与影响预览）。

外部 Connector、Credential、权限和高风险授权回到设置/能力缺口入口，不在此复制能力中心。

## 9. Empty / Loading / Unknown / Error

- Business 无 Workspace：视为需要修复的结构空缺，显示“尚未建立工作空间”与创建/复制入口；创建 Business 的正常结果必须能物化至少一个 Generic Workspace；
- Business 无 Leader：显示 Responsibility Gap，不自动创建 Employee；
- Workspace 读取部分失败：保留其他 Workspace 与 Business 事实；
- Business 无 Result：显示“尚无真实结果”，不显示 0；
- Unknown / Stale / Source 不一致：明确来源、新鲜度和核实入口；
- Closed / Merged Business：从 Current Operating Directory 移出，但保留 History / Result / Evidence / Responsibility Provenance。

## 10. Drill-down / Reverse Entry

Business → Workspace / Employee / Result / Insights / Meeting / Organization / Talent。  
Workspace、Employee Profile、Company Map、CEO Desk、Assistant、Meeting、经营洞察 → Business Work Surface 时，带回原 Business、Office、Leader、Matter / Result 与 Context。

## 11. Cross-page Boundary

| Surface | 负责 | 不负责 |
|---|---|---|
| Business Work Surface | Business Leader 经营、目标、策略、Workspace 聚合、Business 责任与升级 | 公司组织关系真源、Workspace 专业工作细节 |
| Business Space Operating Work Directory | Department / Business / Workspace 三种直接入口 | 组织关系管理或第二套 Business Truth |
| Organization Center | Business 所属关系、Role / Staffing / Leader Assignment、Duplicate / Exit 投影 | Business Leader 持续工作 |
| Professional Workspace | 专业工作、员工 Workstations、Domain Result | Business 整体策略与跨 Workspace 资源判断 |
| CEO Desk | Business 级需要 CEO 的 Matter / Decision / Exception | Business 全部日常工作 |

## 12. Source Authority

Business、Workspace、Leader、Role / Responsibility、Result、Risk、Work Status 均消费既有 Company / Organization / Result / Runtime Truth。Business Work Surface 是 Projection / Management Surface，不创建第二套 Business Truth；Employee Workstation 消费 Frozen Shared Pattern。

## 13. Product → Implementation Gaps

仅登记：Business Leader Scope 与 Workstation 投影、Business→Workspace 直接入口、Business Result / Risk 聚合、最低有效责任路由、Business-level Handoff / Exception、Lifecycle 投影、返回原 Context、Partial Failure、Workspace Workflow graph storage、Drag/drop、Runtime routing、Context injection、Workflow versioning、Migration、Rollback、Auto role assignment engine、Generic role generation runtime。未授权开发或 Runtime Primitive。

## 14. Recommendation

接受为 Business Space 的 Business 入口 Shared Management Surface Contract Candidate；其最终结构为 Business Definition → Operating Status → Workspace Directory → Business Team。Preset Domain（研发、内容增长、小红书、短视频）是可编辑的 Professional Package，不是 Curis 产品边界；未知 Domain 也必须先落到 Generic Business + 至少一个 Generic Workspace，再由专业空间工程替换 / 增强 Domain Work Surface。已有专业 Workspace 页面不因本合同重做；Generic Workspace 页面另行 Review。本合同不授权 UI 高保真、Runtime、Schema、Database 或 Code。
