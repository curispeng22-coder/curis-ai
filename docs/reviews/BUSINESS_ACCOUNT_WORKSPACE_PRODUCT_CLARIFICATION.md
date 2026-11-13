# CURIS BUSINESS × ACCOUNT × WORKSPACE
## SUPERSEDED PRODUCT CLARIFICATION — HISTORICAL REASONING

**Authority Class:** REVIEW  
**Status:** Deprecated  
**Disposition:** CEO REJECTED / SUPERSEDED BY BUSINESS × OFFICE MODEL  
**日期：** 2026-08-18  
**范围：** 只澄清 Business、External Account / Operating Object、Workspace / Office 的产品语义、导航和复制关系；不修改 Product Blueprint、Master Map、UI Blueprint、Business Space Page Contract、Frozen Authority、Runtime、Schema、数据库或代码。

> **重要：** 本文件以下原推荐只保留为研究过程与推导证据，不再是 Review Candidate、Product Authority 或开发依据。上一轮“Business-level Workspace + Account Scope Switching”已被 CEO 明确拒绝；当前请以文末「CEO Correction — Current Product Input」为准。

## 当前 CEO 产品模型（先读）

```text
Company
└─ 内容增长部
   ├─ 小红书运营
   │  ├─ AI科技办公室
   │  ├─ 旅游办公室
   │  └─ 汽车办公室
   ├─ 抖音运营
   │  ├─ 官方账号办公室
   │  └─ AI科技办公室
   └─ 公众号运营
      └─ 公众号办公室
```

**Business = 分类 / 聚合；Office = 独立经营；Account = Office 经营的外部对象。** 以下历史章节不再改变这条当前模型。

## 0. 一句话结论（已被取代）

普通用户不应因为经营多个账号而看到一长串重复 Business。推荐的产品心智是：

```text
Company
└─ Business（小红书运营）
   ├─ Account（AI 科技账号）
   ├─ Account（旅游账号）
   └─ Account（汽车账号）
      ↳ 进入同一专业办公室时，带着当前 Account Scope 工作
```

Business 是“我经营什么业务”；Account 是“这项业务正在经营哪个具体对象”；Workspace / Office 是“员工在哪里完成专业工作”。Account 不自动升级为 Business，Workspace 也不自动成为 Business。

这是推荐的**用户产品模型**，不是对当前 Frozen Domain Authority 的静默覆盖。现行 Content Growth Authority 将 Office 定义为直接挂 Company 的经营单元，并以 `OfficeAccountBinding` 服务 Channel Account；因此本文件最后登记了需要 CEO 决定的 Authority / Product Delta。

## 1. Superseded Recommendation (Historical Reasoning Only)

### 1.1 产品关系

| 对象 | 普通用户理解 | 负责的 Truth |
|---|---|---|
| Business | 一类稳定的经营活动，例如“小红书运营” | Business identity、共同目标/策略、共享方法、角色结构、整体结果 |
| Account / Operating Object | 这项业务具体经营的账号、频道或对象 | 账号身份、定位、受众、外部绑定、账号目标、账号资料、账号结果 |
| Workspace / Office | 员工真正工作的专业办公室 | 专业界面、当前工作、协作方式、结果产出；带一个或多个 Account Scope |
| Employee | 有公司身份、岗位和责任的专家 / Agent | 公司身份、岗位能力、服务关系和执行责任；不因 Account 或 Workspace 复制 |

### 1.2 推荐的 Scope 规则

- Business 允许拥有多个 Account；多账号是同一业务的经营对象集合，不是 Business 列表扩张。
- Account 可以拥有独立 Goal / Positioning / Audience，但默认继承 Business 的共同策略和方法。
- Workspace 默认服务一个 Business，并以当前 Account Scope 工作；共享型 Workspace 可以切换多个 Account，账号差异大的场景可建立账号专用办公室。
- Account-specific 的工作、资料、配置、结果和分析必须隔离；Business shared 的策略、角色和能力默认可复用。
- 用户进入办公室时保留当前 Account Scope；切换账号只切换允许切换的事实，不把整套 Business 复制一遍。

## 2. Business Truth

### KEEP（Business Shared Truth）

- Business Identity / Name / Category；
- Department 归属（可空、按需形成）；
- Business Leader / 经营责任；
- Shared Goal / Strategy；
- Shared Operating Model：共同工作方法、Role Structure、Responsibility、Required Capability；
- 共享的 Skill / Tool / Knowledge 方法；
- Business 默认 Workflow / Automation / Cadence；
- Business 级总体 Result / Analysis（由 Account / Workspace 结果汇总而来，不覆盖账号事实）。

### 不直接放在 Business 的内容

具体平台凭证、账号定位、账号受众、账号发布时间表、账号级知识和账号级发布回执不能被 Business shared 配置覆盖。它们属于 Account 或 Domain Workspace Scope。

## 3. Account Truth

### ACCOUNT-ONLY

- Account Identity / Name / External ID；
- Channel / Platform；
- Positioning / Tone / Audience；
- Account Goal（若与 Business 共同目标不同）；
- External Account Binding、授权状态和最近验证；
- Account-specific Knowledge / Brand / Content Context；
- Account Strategy、Workflow Configuration、Schedule / Publishing Cadence；
- Account Employee Assignment / 当前工作；
- Account Result、Publication / Receipt、External Business Metrics、Account Analytics。

### Business Default → Account Override

允许账号继承 Business 默认值，再保存可解释的局部 Override：

```text
Business 默认工作方式
  → AI 科技账号：直接继承
  → 汽车账号：只覆盖定位、受众、标签和发布时间
```

页面必须让 CEO 看见“继承自 Business”与“账号已覆盖的部分”。Override 不复制完整 Operating Model，也不让 Account A 读取 Account B 的定位、知识、凭证或对话。

## 4. Workspace Relationship

### 推荐语义：Business-level Office + Account Scope

产品层优先把 Workspace 作为 Business 的专业工作环境，同时支持一个当前 Account Scope：

```text
Business: 小红书运营
└─ Content Operations Workspace
   ├─ active scope: AI 科技账号
   ├─ active scope: 旅游账号
   └─ active scope: 汽车账号
```

这解决日常工作中的“进入同一个小红书办公室，切换不同账号”的自然心智，也避免为每个账号默认复制办公室。

### 何时需要账号专用 Workspace

当两个 Account 的专业工作方式、员工团队、知识边界、外部副作用或结果契约已经明显不同，才在同一 Business 下建立不同 Workspace。产品动作应表达为“为账号建立办公室 / 复制账号的工作方式”，不创建面向普通用户的通用 `Duplicate Workspace` Primitive。

### 现行 Authority 注意

Content Growth Domain Authority 当前定义：Office 直接挂 Company，`OfficeAccountBinding` 连接 Office 与 Channel Account，首版 UX 推荐 1 Account : 1 Office，结构支持 N:N；Company OS 又冻结了 Business = Operating Team + Business Workspace。两者与本推荐的 Business-level Office + Account Scope 存在边界差异，必须由 CEO 另行确认，不能在本文件自行改写。

## 5. Navigation

### 5.1 高频路径

```text
Business Space
  → 选择 Business
  → 选择 Account（若有多个）
  → 进入对应 Office / Workspace
```

Business Detail 不是 Workspace 的强制导航父页面。高频经营从 Business Space 直接进入当前账号办公室；低频管理仍走：

```text
Business Space → Business Detail
  → Goal / Strategy / Operating Model / Account / Staffing / Lifecycle
```

这遵守：**Object hierarchy ≠ Navigation hierarchy**。

### 5.2 Account Scope Switcher

进入 Business 或 Office 后，提供轻量当前账号选择：

```text
[AI 科技账号 ▼]  [旅游账号]  [汽车账号]  [+ 添加账号]
```

切换只更新允许 Account-specific 的内容：Goal、Positioning、Configuration、Workflow Override、Employee Assignment、Current Work、Result、Analytics、Knowledge；Business shared 的名称、共同策略、共享角色和方法保持不变。

如果某项信息在当前 Scope 不可用，显示“继承 Business 默认 / 尚未配置 / 未连接”，不显示 0 或复制一份空对象。

## 6. Business Space Contract Delta

现有 `BUSINESS_SPACE_PAGE_CONTRACT_FINAL_REVIEW.md` 需要在 CEO 接受本澄清后作以下窄范围 Delta；本轮不直接修改它：

1. Business Portfolio 仍按 Business 展示，不按 Account 拆成重复卡片；多账号以 Business 卡内的当前 Account 摘要或轻量切换表达。
2. Business Card 增加当前 Account / Account 数量 / External Object 摘要，但不把 Account 变成 Business。
3. Business Space 增加“进入当前账号办公室”的高频动作；Business Detail 保留为低频管理入口，不再作为 Workspace 的必经页面。
4. Business Detail 增加 Account 集合、Business Default / Account Override、账号级 Result / External Data 摘要。
5. Workspace 摘要明确“办公室服务的 Business 与当前 Account Scope”；多个 Account 不默认创建多个 Workspace。
6. Duplicate Business 与 Add / Duplicate Account Configuration 在动作名称和 Copy Preview 中明确区分。

## 7. Duplication Semantics

### 7.1 Add / Duplicate Account Configuration

适用判断：仍然是同一种 Business，只是新增一个定位不同的账号。

```text
Business
  → 添加账号 / 复制账号工作方式
  → 选择新 Account
  → 复用 Business Default 或源 Account Configuration
  → 重新填写 Goal / Positioning / Audience / Knowledge / Credential / Staffing / Schedule
  → 进入同一 Business 的 Account Scope / Office
```

它复用的是工作方法、Role / Responsibility 结构、Required Capability、Workspace 配置和可复用运营经验；它不复制身份、凭证、对话、Execution、Result、Evidence、历史或当前运行状态。

### 7.2 Duplicate Business

适用判断：CEO 明确要独立经营、独立目标、独立投入/退出判断和独立历史。

```text
Business A → Duplicate Business → Business B
```

新 Business 拥有独立 Identity、Goal、Operating Model、Lifecycle、Result、History 和经营决策；External Account、Credential、Employee Binding 和 Workspace 必须重新确认。

### 7.3 “复制办公室”的真实产品动作

普通用户可以说“复制办公室”，但产品内部优先解释为：

```text
Create Account
  + Reuse Account Operating Configuration
  + 可选 Reuse Workspace Configuration
  → 新 Account Scope / 必要时新 Office
```

除非 Domain 明确需要不同专业环境，不新增通用 `Duplicate Workspace` 产品 Primitive。

### 7.4 简单判断规则

> 仍属于同一种业务，只是多经营一个账号 → **添加 / 复制账号工作方式**。  
> 需要独立经营、独立目标、独立投入或独立退出判断 → **复制业务**。

## 8. Staffing

Employee identity 始终是 Company Organization 中的一个身份，不因 Account 或 Workspace 复制。

产品语义分开表达：

```text
Organization Affiliation  = 员工属于哪个 Department / Role
Business Assignment       = 员工为哪个 Business 承担责任
Account / Workspace Scope = 员工当前为哪个账号、办公室执行工作
```

同一 Employee 可以合理服务多个 Account；每次执行读取当前 Account Scope 的定位、知识、权限和目标。服务关系不等于组织成员复制；完整组织关系仍进入 Organization Center，招募仍进入 Talent & Capability。

## 9. Company Map Impact

Company Map 默认保持：

```text
Company
└─ Department
   └─ Business
      └─ Role / Staffing
         └─ Employee Reference
```

Account 不是默认 Organization Node。CEO 展开某个 Business 时，才按需显示账号集合和每个账号的简短经营状态：

```text
内容增长部
└─ 小红书运营
   ├─ AI 科技账号
   ├─ 旅游账号
   └─ 汽车账号
```

这样公司版图表达组织成长，Business Space 表达账号经营，二者共享同一 Business / Account Truth，不复制组织树。

## 10. Operating Intelligence Impact

经营洞察增加 **Account Scope** 作为既有 scoped Insights 的一个维度，不创建第二套 Analytics Truth：

```text
Company → Department → Business → Account → Workspace → Employee → Model / Agent
```

必须支持：

- 看 Business 整体；
- 切换 AI 科技 / 旅游 / 汽车账号；
- 比较不同 Account 的 Result、Acceptance、External Business Result；
- 从 Account 结果下钻到 Workspace、Employee、Evidence、Publication / Receipt；
- 从 Insights 返回原 Business / Account / Workspace 上下文。

所有指标继续带 source、freshness、automatic / manual / unknown / external 语义；没有来源不显示 0，不新增 Account Analytics Runtime。

## 11. External Account ≠ Business

Channel Account / External Account / Operating Object 是 Business 经营的外部对象，不因为连接一个新账号而自动创建 Business。只有 CEO 选择独立经营、独立目标、独立生命周期时，才走 Duplicate Business。

External Account 失效时保留账号身份和历史结果，当前执行降级并显示未连接/需授权；不能静默删除或篡改历史。账号绑定不授予 Organization 成员资格。

## 12. Product → Implementation Gaps

本澄清没有授权实现。需要后续正式 Issue 的 Gap：

1. **Authority Reconciliation Gap**：Product Blueprint / Company OS 的 Business = Team + Office，与 Content Growth Authority 的 Office 直挂 Company、OfficeAccountBinding 之间需要明确上位关系；当前不得自行选择。
2. **Account Scope Gap**：需要同源的 Business / Account / Workspace scope 投影与上下文隔离，不能由页面拼接账号卡片。
3. **Default / Override Lineage Gap**：需要记录 Business Default 与 Account Override 的来源、版本、回退和生效范围，不复制整套 Operating Model。
4. **Workspace Binding Gap**：需要明确一个 Workspace 服务多个 Account 与账号专用 Workspace 的合法边界；现有 Domain 支持 N:N 结构但 UX 推荐 1:1，需统一产品表达。
5. **Account Result / Receipt Gap**：Account 级 Result、Publication / Receipt、External Metric 必须可追溯并与 Business 汇总区分。
6. **Scoped Staffing Gap**：需要在不复制 Employee identity 的前提下表达 Business Assignment 与 Account / Workspace execution scope。
7. **Duplication Gap**：Add / Duplicate Account Configuration、Duplicate Business 和“复制办公室”的真实持久化边界与恢复证据尚未形成正式 Runtime Issue。
8. **Insights Scope Gap**：经营洞察需要按 Account 过滤、比较和反查，但不新增第二套 Analytics Truth。
9. **Navigation Projection Gap**：Business Space 需要从 Business 直接进入当前 Account Office，同时保留 Business Detail 的低频管理入口。

## 13. CEO Decisions Required

以下必须由 CEO / Product Authority 决定后，才能回写 Business Space Page Contract 或三份 Current Truth：

1. 是否接受“一个 Business 可包含多个 Account，Account 不是 Business”的产品语义；
2. 是否接受“Business-level Workspace + 当前 Account Scope”作为默认用户体验；
3. Content Growth 中 Frozen 的 Office 直挂 Company / OfficeAccountBinding，如何与 Business = Team + Office 的 Company OS 规则统一；
4. 多 Account 是否默认共用同一 Office，何时必须建立账号专用 Workspace；
5. 是否将“复制办公室”正式表达为“添加账号并复用账号工作方式”，而不是新增 Duplicate Workspace；
6. Business Space 是否按本文件 Delta 支持 Business 直达当前 Account Office；
7. Business Template 与 Account Configuration Reuse 的关系是否另行定义；本轮不默认建立 Template Primitive。

## 14. Recommendation

推荐接受以下普通用户规则：

> 同一类业务、多账号经营：添加或复制账号工作方式。  
> 独立目标、独立经营、独立退出：复制业务。  
> 进入办公室时携带当前账号 Scope；员工身份不复制；公司版图不展开成账号森林。

但在 CEO 解决第 3 项 Authority Reconciliation 前，Business Space Page Contract 应保持：

```text
REVIEW PAUSED — WAITING FOR BUSINESS × ACCOUNT × WORKSPACE AUTHORITY DECISION
```

本文件不修改任何 Frozen Product Truth，也不授权 Runtime / Schema / Code。

---

CURIS BUSINESS × ACCOUNT × WORKSPACE  
— PRODUCT CLARIFICATION COMPLETE  
— STOP FOR CEO REVIEW

## CEO Correction — Current Product Input

本节取代本文件前述推荐，作为后续 Current Product Truth 消费的唯一输入：

```text
Company
└─ Department
   └─ Business（同类办公室的分类 / 聚合）
      └─ Office / Workspace（独立经营与专业工作环境）
```

Business 负责业务类别、整体目标/方向、Office 集合、整体结果、整体资源与风险；Office / Workspace 负责独立 Goal、定位、受众、策略、Workflow、Role/Staffing、Employee Assignment、Model/Agent、Skill/Capability、Connector、Knowledge、Schedule、Current Work、Result、Analytics、Risk 与 History。Account 不是全局层级，而是 Office 服务或经营的 External Account / Operating Object。小红书、抖音等账号经营场景通常一账号对应一 Office，但不冻结为所有 Domain 的全局 Primitive。

- Business Space 默认按 Business 聚合，Business 卡片显示 Office 数量/摘要，并允许直接进入 Office；Business Detail 是低频整体管理，不是 Office 的强制父页面。
- 同一 Business 的多个 Office 默认独立；可以复用方法和配置，但不默认共享具体目标、员工、模型、资料、凭证、排期、结果或分析事实。
- `Duplicate Office` 在同一 Business 下创建新的独立 Office；`Duplicate Business` 创建新的 Business Identity。两者均使用 Copy Preview，明确复用、重新确认和禁止复制边界。
- 不采用 Business Default → Account Override、Account Scope Switching、Account Matrix Runtime 或新的 Account 层级。

本节是 CEO 当前产品输入；正式消费由 Product Blueprint → Master Map → UI Blueprint 完成，Runtime / Schema / Code 仍需独立 Issue 与 Review。
