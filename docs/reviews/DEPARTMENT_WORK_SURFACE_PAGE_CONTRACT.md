# CURIS PAGE CONTRACT CANDIDATE — DEPARTMENT WORK SURFACE

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CEO CONSOLIDATED PRODUCT DECISION APPLIED — SHARED MANAGEMENT SURFACE CANDIDATE  
**性质：** Business Space 内的 Department 管理工作面；属于所有 Domain 都需要的 Shared Management Surface Contract Candidate，不是新一级导航、非 Runtime / Schema / Database / Code 设计。

## 1. Contract Position

本合同定义所有 Domain 都需要的共享管理职责：Identity、Leader Workstation、Responsibility、Goal、Current Focus、Children、Result / Risk、Team 摘要、Management Actions 与 Escalation 关系。Workflow 不属于 Department 共享管理骨架；具体 Workflow 只在 Workspace 内定义。它不规定所有 Domain 的最终视觉或具体专业工作方式。

产品表达固定为：

```text
Shared Management Shell
+ Domain-specific Operating Surface
```

内容增长、研发及其具体业务（例如小红书运营、Curis 产品研发）必须通过后续 UX Exploration 验证差异，不在本合同内预先做成同一页面。

## 2. Mission

Department Work Surface 是 Department Leader 的真实管理与经营工作面。它回答：

> 这个 Department 当前承担什么责任、服务哪些 Business、哪些责任需要处理、下一步要向谁协调？

### Leader / Assignment Contract

Department Leader 是普通 Employee 的 Leadership Role，不是 Employee Type 或 Admin。页面负责人必须投影真实 `Employee × Role × Scope` Assignment；同一 Employee 可兼任多个 Department / Business / Workspace Scope。Leader Workstation 以 Department Scope 读取 Goal、Children、Result / Risk、Team 摘要与升级事项；日常 Conversation 不在组织中心复制，而在本 Work Surface 承载。

Department 只接收跨 Business、资源/策略冲突、共同风险或下级无法解决的问题。责任在最低有效范围解决，重大或不可逆事项才向 CEO 升级；Workflow 的具体步骤仍属于 Workspace，不在 Department Work Surface 建立统一 Workflow。

它不是 Organization Center 的组织详情复制品，也不是 Dashboard。组织关系和调整留在 Organization Center；Department Leader 的持续 Workstation、责任、Handoff、Exception、Decision Request 与 Follow-up 在这里发生。

## 3. Entry / Return

入口：

- Business Space → [部门] → Department；
- Company Map 点击 Department Header / Focus；
- CEO Desk 的 Department Matter / Result / Risk；
- Search、Recent、Assistant、Meeting、经营洞察的 Department scope。

返回必须保留 Company、Department、Business / Office、Matter / Result、Filter、Focus 和未完成输入；从 Organization Center 进入时返回组织版图，不把组织详情变成经营 Surface。

## 4. Information Responsibilities

信息责任集合不等于固定 Dashboard 区块。默认第一视觉优先：

- Department Identity；
- Mission / Responsibility；
- Department Leader；
- Leader Employee Workstation 的当前状态与当前工作；
- Department Goal / Current Focus；
- 所辖 Business 摘要与进入入口；
- Department-level Result；
- Risk / Blocker / Needs Higher Authority（仅存在时）；
- Staffing / Resource 摘要与 Responsibility Gap；
- Department-level Decision / Follow-up。

Department Leader 仍是普通 Employee，不创建 DepartmentLeaderAgent 或第二套管理 Workstation。Workstation 统一消费 Frozen Employee Workstation Pattern：Avatar、Name、Role、Responsibility、Shared Work Status、Current Work、Conversation、Composer。

## 5. Responsibility / Workflow Routing

Department 是责任 Scope，不是机械审批层。工作默认在最低有效责任 Scope 完成；仅在跨 Business、Department 级资源/目标/优先级、当前 Scope 无法解决或需要更高 Decision Authority 时进入 Department Leader。

```text
Workspace Responsibility
→ Business Responsibility
→ Department Responsibility
→ Company / CEO
```

Workspace 内部正常专业工作不经过 Department Leader；Department Leader 接收属于本 Department Scope 的 Responsibility、Handoff、Exception、Decision Request、Follow-up，并可向 CEO 升级。

Department Work Surface 不提供专业 Workflow Builder。Department 负责 Department Goal、Department Leader、Business Portfolio、跨 Business 协调、Resource、Result / Risk；具体业务规则、标准、Workflow 与 Role Structure 进入 Business Work Surface。

## 6. Actions

- 查看 / 编辑 Department Mission、负责人和组织关系摘要；
- 进入 Business Work Surface；
- 查看 Department Result、Risk、Responsibility Gap；
- 接收 / 处理 Handoff、Exception、Decision Request、Follow-up；
- 进入 Organization Center 调整 Department / Role / Employee Binding；
- 进入经营洞察、会议、资料库；
- 在合法生命周期范围内提出 Department 调整、暂停或归档。

组织关系调整不在本 Surface 内复制实现；应回到 Organization Center 的组织操作。

## 7. Empty / Loading / Unknown / Error

- Department 无 Business：合法空态，解释责任与可创建/接入的下一步；
- Department 无 Leader：显示责任空缺，不自动创建 Employee；
- Department 无 Result：显示“尚无真实结果”，不显示伪造 0；
- Unknown：显示未知及来源/更新时间，不推断为空；
- Partial Failure：保留可读的其他 Business 与责任，提供重试和来源；
- Department 归档/关闭：不混入 Current Operating Surface，历史仍可反查。

## 8. Drill-down / Reverse Entry

Department → Business Work Surface → Workspace / Employee / Result / Insights / Meeting。  
Employee Profile / Workspace / CEO Desk / Assistant / Meeting → Department Work Surface 时，带回 Department 与原 Scope，并支持返回原上下文。

## 9. Cross-page Boundary

| Surface | 负责 | 不负责 |
|---|---|---|
| Department Work Surface | Department 经营、Leader Workstation、责任协调和升级 | 组织关系真源、Business 日常专业工作 |
| Organization Center | Department / Business / Role / Employee 关系与调整 | Leader 持续 Conversation / 经营工作 |
| Business Work Surface | Business 目标、策略、Office 与结果 | Department 全局资源治理 |
| CEO Desk | 公司级注意力与需要 CEO 的 Department Matters | Department 全部工作台账 |

## 10. Source Authority

Department、Leader、Business 归属、Role / Employee Binding、Result、Risk、Work Status 均消费既有 Company / Organization / Result / Runtime Truth。Department Work Surface 只是投影，不创建第二份 Department Truth；Leader 的 Workstation 状态消费 Shared Employee UI Status 投影。

## 11. Product → Implementation Gaps

仅登记：Department Work Surface 投影、Department Leader 责任绑定、Department Result/Risk 聚合、跨 Business Handoff、返回原上下文、Partial Failure。未授权开发或 Runtime Primitive。

## 12. Recommendation

接受为 Department Work Surface Shared Management Surface Contract Candidate；后续 Domain UX Exploration 至少覆盖内容增长部、研发部、小红书运营与 Curis 产品研发，再决定各自 Domain-specific Operating Surface。当前不新增 Department-specific Runtime 或管理 UI。
