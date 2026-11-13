# CURIS PAGE CONTRACT FINAL REVIEW — 03 ORGANIZATION CENTER
## Company Map + Employee Directory

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CEO CONSOLIDATED PRODUCT DECISION APPLIED — ACCEPTANCE PAUSED FOR FINAL REVIEW  
**日期：** 2026-08-18  
**性质：** Page Contract；非 Product Authority、非 Runtime / Schema / Database / Code 设计。  
**前置：** CEO Desk 与 Business Space 均为 Accepted Candidate；Company Map Variant A / Department Container 已被接受为产品与交互方向。本轮 Operating Hierarchy 决策要求先完成 Department / Business Work Surface 与责任 Scope 同步，再接受本合同。

## 1. Page Mission

组织中心回答两类 CEO 问题：

1. **公司版图：**我的公司现在长成什么样、业务扩张到哪里、哪里缺责任、哪里有风险？
2. **员工目录：**公司有哪些员工，每个人属于哪里、承担什么责任、正在服务哪些 Business / Office？

它不是传统 HR Org Chart、Agent Market、经营 Dashboard，也不是第二套 Organization Truth。它是 **Organization Structure & Administration**：负责公司如何组成、谁属于哪里、谁承担什么责任以及如何调整组织；Department Leader / Business Leader 的持续 Workstation 和经营 Conversation 属于 Business Space 的对应 Work Surface。

## 2. Current Product Model

```text
Company
├─ Department（稳定责任聚合，通常按需渐进形成）
│  └─ Business（同类 Office 的分类 / 聚合）
│     ├─ Office / Workspace（独立经营单元）
│     │  └─ Workspace Leader / Operating Team → Role → Responsibility Assignment → Employee
│     └─ Office / Workspace ...
└─ Employee Directory（从 Employee 反查 Role / Business / Office / Department）
```

固定语义：

- **Department** = 稳定责任聚合；空间工程部、数据分析部是新 Company 默认存在的 Company Support Department，不向普通用户暴露“System Exception”术语。
- **Business** = Office 分类 / 聚合层，表达整体方向、Office 集合、整体结果、资源与风险。
- **Office / Workspace** = 独立经营单元与专业工作环境；长期 Office / Workspace 必须由 Operating Team（Workspace Leader、成员、职责）承载。负责人未设置时可以暂存，但不构成完整经营责任承载。
- **Employee** = 稳定的 Company Identity；多 Role、多 Business、多 Office 不复制身份。

## 3. IA：两个核心 Surface

### 3.1 公司版图（默认）

采用 Variant A · Department Container：Department 是容器，Business 是默认主要经营节点，Office / Role / Employee 渐进展开。

```text
公司版图
├─ 空间工程部
├─ 数据分析部
└─ 内容增长部
   ├─ 小红书运营
   │  ├─ AI科技办公室
   │  ├─ 旅游办公室
   │  └─ 汽车办公室
   ├─ 抖音运营
   └─ 公众号运营
```

第一眼看 Department 分布、Business 数量与扩张，不把全部 Office 铺成“Office 森林”。

### 3.2 员工目录

员工目录只显示已经属于 Company 的 Employee；人才与能力展示外部 Expert / Skill / Connector。员工目录支持全部、在岗、未在岗、离职等 Employment Status 过滤，但不把完成或等待当作 Employee Work Status。

## 4. Department Container Contract

Department 是信息容器，不要求 Header 一次显示所有信息。其 Information Responsibilities 包括：

- Department Name
- Responsibility / Mission
- Leader（若有）
- Business 数量与分布
- Employee / Staffing 摘要
- Vacancy / Responsibility Gap
- Risk / Blocker（仅存在时）
- Recent Important Result（仅存在时）

默认优先 Department Name、Responsibility、Business 分布与必要 Attention。保持 **Low Surface Complexity / High Operating Information Density**。

默认 Support Departments：

- **空间工程部：**将经营目标转化为可工作的 Business Office / Workspace。
- **数据分析部：**承载 Company Analyst 与跨公司分析，并可通过 Assignment / Allocation 支持 Business。

其他 Department 由重复责任、稳定协作和共享能力逐渐形成；不要求先建立 Department 才能招聘员工或创建业务。

## 5. Business Node Contract

Company Map 中的 Business Node 不是 Business Space Card 的复制品，而是回答“这项 Business 在公司版图中处于什么位置”。

默认第一视觉优先：

- Business Name
- Office 数量
- Business Leader / Responsibility
- Staffing / Vacancy 摘要
- Risk / Blocker（仅存在时）
- Recent Important Result
- NEW / Expansion 等有真实来源和时间依据的变化

完整 Goal、Strategy、Workflow、Analytics、External Account 不在 Node 全量展开，进入 Business Work Surface / Workspace / 经营洞察。

Business Name 进入 Business Work Surface；Business Node 展开的 Workspace 可直接进入对应 Workspace，不强制经过 Business Work Surface。

## 6. Office Expansion

Business 拥有多个 Office 时默认显示数量与摘要，例如“小红书运营 · 3 个办公室”。按需展开：

```text
小红书运营 · 3 个办公室
├─ AI科技办公室
├─ 旅游办公室
└─ 汽车办公室
```

Office 展开可表达：Office Name、External Object 摘要、Leader / Team、Current Work、Result、Risk / Blocker、Staffing Gap。点击进入 Office / Workspace；不默认展开全部 Role / Employee。

## 7. Role / Responsibility Scope / Staffing Contract

组织中心必须表达：

```text
Business / Workspace
→ Role
→ Responsibility Assignment
→ Employee
```

Role 展开至少包括 Role Name、Responsibility、Required Capability、Staffing Count、Vacancy、Responsibility Assignment 与 Employee。普通用户不直接看到 RoleSlot 等内部术语。

Role / Responsibility 必须有明确经营 Scope，不冻结为“Role 只属于 Business”或“Role 只属于 Workspace”。当前合法 Scope 至少包括 Department、Business、Workspace；Company 级最高责任由 CEO 承载。Business Definition / Rules 可以提供可复用的经营方法与 Role / Responsibility 参考，但不得形成统一 Workflow 母模型或第二套 Staffing Truth。Employee Binding 绑定到对应 Scope，并形成 Responsibility Assignment；Employee Binding 是形成 Assignment 的动作/关系，不是最终运行责任语义。同一 Employee 可在多个合法 Scope 承担不同责任，身份不复制。

### Leadership Assignment 与目录边界

Department Leader、Business Leader、Workspace Leader / Operating Owner 是 system-defined Leadership Role 的产品语义，不是 Employee Type 或 Admin。组织中心只维护真实 `Employee × Role × Scope` Assignment 与 Leader assignment 投影；持续 Leader Conversation、Result 回收、Handoff、Exception 与 Follow-up 回到对应 Work Surface，不在组织中心复制第二套工作记录。Employee Profile 可从 Identity Conversation 进入整体能力，也可按指定 Assignment 进入隔离的 Role / Scope Conversation。

## 8. Employee Binding

Employee 是稳定 Company Identity。一个 Employee 可以有多个 Role、服务多个 Business / Office，但不能因组队或多重分配而复制身份。

示例：

```text
白露
├─ 内容增长部 → 小红书运营 → AI科技办公室 · 文案
└─ 内容增长部 → 小红书运营 → 汽车办公室 · 内容 Review
```

Employee Directory 必须能够反查这些关系；Workspace 内的 Add Employee 只完成组队，不创建第二个 Employee。

## 9. Employee Directory Contract

员工目录的第一视觉优先：

- Avatar / Name
- Role
- Department（若有）
- 当前主要 Business / Office 责任
- Shared Work Status：空闲 / 工作中·描述 / 阻塞·原因
- Current Work 摘要
- 最近 Result（有价值时）

Model、Skill、Tool、Cost、完整 Capability、History 进入 Employee Profile，不默认塞进列表。Employment Status 与 Shared Work Status 严格分开；“已完成”“等待”属于 Goal / Task / Result，不属于 Employee。

## 10. Employee Profile / Workstation

从员工目录进入 Employee Profile 后可反查：

```text
Employee
→ Role
→ Business
→ Office / Workspace
→ Department
```

Profile 还可查看 Capability、Current Responsibility、Result、Conversation、Growth / Lessons。实际协作进入 Employee Workstation / Conversation；组织中心不放永久员工聊天栏。

## 11. Create / Add Contract

遵循 **Create Where You Organize；Add Where You Work**：

```text
Company + → Department
Department + → Business
Business / Office 组织结构 → Role
Role / Employee Directory → Employee
Business Work Surface / Business Space → 创建或复制 Workspace
Workspace → Add Employee（只组队，不复制身份）
```

Business Duplicate 创建新的 Business 节点；Office Duplicate 保持在原 Business 下，均回到同一 Company Truth。

## 12. Vacancy / Staffing Gap

空岗是组织中心的经营事实。例如：`小红书运营 → AI科技办公室 → 数据分析岗 → 0/1` 显示为“数据分析 · 空岗”。允许：绑定已有 Employee、从人才与能力招募、按 Current Authority 允许的路径创建岗位员工、暂时保持空岗。空岗不自动创建 Employee。

## 13. Capacity / Load

只有存在合法来源时才显示 Staffing Count、Vacancy、Load %、Capacity。没有 Threshold Contract 时，只显示原始事实，例如“Load 88%”，不得自行判断“接近饱和”“过载”“优秀”或“健康”。

## 14. Risk / Blocker / Result

Company Map 只显示轻量经营信号：例如“发布授权阻塞”“最近产生重要 Result”。完整对象回到其职责页面：

```text
Risk / Blocker → CEO Desk / Business
Analysis → 经营洞察
Result → Result / Evidence
```

Company Map 不变成经营 Dashboard。

## 15. Duplicate / Exit Projection

### Duplicate

- **Duplicate Business：**产生新的 Business 节点，自动进入同一 Company Map 与 Business Space。
- **Duplicate Office：**仍属于原 Business；Company Map 默认只显示 Office 数量变化，例如“3 → 4 个办公室”，展开后才看到新 Office。
- NEW / Expansion 只能来自真实创建来源和时间依据。

### Exit

Pause、Reduce、Transfer、Close、Merge、Split 后，Company Map 反映真实组织变化。Closed Business 不留在默认 Current Operating Map，但 History、Result、Evidence、Responsibility Provenance 仍可反查。Merge / Split 必须保持组织变化可解释。本页不定义 Runtime 状态机。

## 16. Focus / Search / Filter / Zoom

- 点击 Department Header → Focus Department；其他 Department 降低视觉权重；退出后恢复原 Zoom、Position、Selection、Focus。
- Search 支持 Department / Business / Office / Role / Employee。
- Filter 至少支持 Vacancy、Risk / Blocker、New / Recently Changed；不无限扩展过滤器系统。
- Zoom / Minimap 是 Company Map 导航辅助，不是经营功能；是否成为最终 Design Requirement 取决于真实组织规模。

Focus 是 Company Map 的查看方式，不新增页面对象或 Runtime Truth。

## 17. Empty / Loading / Unknown / Error

- **New Company：**默认显示空间工程部、数据分析部；没有经营 Business 时，说明“公司已有基础职能团队，现在可以开始第一项业务”。
- **Department 无 Business：**合法空态，不显示错误。
- **Business 无 Office：**显示“尚未建立办公室”及合法创建入口。
- **Office 无 Team：**显示“Staffing Gap / 无责任承载”，不伪装 Operating。
- **Employee 无 Department：**合法；Employee 可以直接属于 Company。
- **Unknown：**不显示 0，不以 Unknown 推断为空。
- **Partial Failure：**单个 Department / Business 读取失败时，其余组织仍可查看，并保留重试 / 来源入口。
- **Archived / Closed：**不与 Current Operating Map 混在默认视图。

## 18. Actions / Drill-down / Reverse Entry

| 对象 | 主动作 | Drill-down | Reverse Entry / 返回 |
|---|---|---|---|
| Department | 聚焦、编辑、查看 Business | Department Focus / context | 返回原 Company Map focus |
| Business | 查看、复制、创建/复制 Workspace | Business Work Surface | 返回 Company Map / Business Space |
| Workspace | 查看、复制、组队、暂停/恢复 | Professional Workspace | 返回 Business / 原 Workspace |
| Role | 查看、绑定、解除绑定、查看空岗 | Role Detail | 返回 Business / Office |
| Employee | 查看、组队、配置 | Employee Profile / Workstation | 返回原 Role / Business / Workspace |
| Vacancy | 绑定、招募、保持空岗 | Employee / Talent & Capability | 返回原 Vacancy focus |
| Risk / Blocker | 查看来源 | CEO Desk / Business Matter | 返回原节点 |
| Result | 查看证据 | Result / Evidence | 返回原 Business / Office |
| Analysis | 查看分析 | Scoped Operating Intelligence | 返回原上下文 |

从 Business Space、Employee Profile、Workspace、人才与能力、经营洞察、CEO Desk、Meeting、Assistant 进入组织中心时，必须携带 Company、Department、Business、Workspace、Role、Responsibility Assignment、Employee 与对应 Focus，并可返回原来源和原 Context。

## 19. Cross-page Boundary

| 页面 | 负责回答 | 不负责替代 |
|---|---|---|
| 组织中心 | 公司怎么组成、业务如何扩张、谁承担责任、如何调整组织 | Department / Business / Leader 的持续经营 Workstation |
| 业务空间 | 从 Department / Business / Workspace 直接进入对应 Work Surface，继续经营 | 组织关系总览 |
| 人才与能力 | 外部 Expert / Skill / Connector | 已入职 Employee 目录 |
| 经营洞察 | 趋势、比较、归因、报告 | 组织事实源 |
| CEO 工作台 | 今天值得关注的组织变化 | 完整公司版图 |

## 20. Source Authority / Truth Boundary

Company Map 是 Projection / Navigation Surface，不是新的事实源。信息来源必须可追溯：

| 信息 | Source Authority |
|---|---|
| Company / Department / Business / Office / Role / Employee | Company OS / Organization Truth；Product Blueprint 与 Master Map 只定义产品语义 |
| Staffing / Vacancy / Employee Assignment | Organization / Employee Binding Truth |
| Result / Evidence | Result / Evidence Truth |
| Risk / Blocker | 来源 Business Matter / CEO Desk / Workspace |
| Work Status | Runtime Truth 的 Shared Employee UI Status 投影 |
| 趋势 / 比较 / 分析 | Scoped Operating Intelligence，不能回写组织事实 |

Company Map 不创建第二套组织关系、状态或结果记录。

## 21. Product → Implementation Gaps

本页只登记 Gap，不授权开发：

1. Business → multiple Office projection；
2. Office → Team / Role / Employee projection；
3. Employee multi-Office assignment；
4. Vacancy / Responsibility Gap；
5. Business / Office Duplicate projection；
6. Business Exit lifecycle projection；
7. Default Support Departments initialization；
8. Risk / Result aggregation；
9. Search / Filter / Focus state；
10. Company Map partial failure / recovery。

## 22. Open Questions

1. **Zoom / Minimap Design Requirement：**在真实组织规模达到何种范围后必须启用，交由 Design Review 根据真实密度确认。
2. **Employee 直接属于 Company 的默认阅读：**当前语义允许，但其在 Company Map 中的可见位置与员工目录入口由 UI Design 确认。

## 23. Final Recommendation

当前模型、IA、边界和状态语义足以形成 Organization Center Page Contract。推荐在同步 Department / Business Work Surface 后接受为跨页面设计输入：公司版图采用 Department Container；Business 默认经营节点；Office / Role / Employee 渐进展开；员工目录独立反查；Company Map 只消费组织、结果与运行投影，不成为新事实源。Leader 的持续经营必须留在 Business Space 对应 Work Surface。

未发现需要新增 Product Delta 的问题。Role / Responsibility Scope 已按 Department、Business、Workspace 的经营 Scope 原则收敛；仍需 Design Review 确认 Company Map 的 Focus、Zoom、Minimap 与 Company-level Employee 阅读细节。

CURIS PAGE CONTRACT FINAL REVIEW  
— 03 ORGANIZATION CENTER COMPLETE  
— STOP FOR CEO REVIEW
