# Curis · Content Growth 共享契约设计计划（Shared Contract Plan）

> **状态**：SHARED CONTRACT PLAN REVIEW REQUIRED（仅规划下一阶段需固化的契约，未 Frozen）
> **类型**：Reference Only · Contract Design Plan（设计期输入，非权威、非实现）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：
> - 上一轮 4 份 `Curis_Content_Production_Channel_Operations_Model.md` 等（已被本轮 DELTA 部分修正）
> - 本轮 4 份 `Curis_Content_Growth_Operating_Model.md` / `Channel_Account_Matrix_Model` / `Organization_Routing_Architecture` / `Company_Evolution_Model`（状态：DELTAS APPLIED）
> - 抖音官方能力研究（保留并重归类为 **Douyin Channel Capabilities**）
> - AiToEarn 参考实现（Reference Implementation 定位不变）

---

## 0. 本计划的目的与边界

本轮用户批准「总体方向 APPROVED WITH DELTAS」，仅修正 3 个架构 Delta（DELTA 1 Office/Org 正交、DELTA 2 Router/Team Lead 分离、DELTA 3 首版 Capacity 降复杂度），并明确要求：**进入 Contract 设计前，先产出「下一阶段需要固化的契约计划」**。

本计划**只规划**，不落地：

- ✅ 列出下一阶段需固化的 **9 个契约**及其**目的 / 关键元素 / 归属层 / 依赖 / 开放问题**。
- ✅ 明确每个契约属于 **Company OS Shared / Content Growth Domain / Workspace Instance / Capability·Connector** 哪一类。
- ❌ 不写入最终字段类型 / 数据库 schema / API 签名。
- ❌ 不 Frozen、不改任何权威文档、不开发 Runtime / Connector、不画 UI。
- ❌ 不解决平台政策强结论（仍 `POLICY VERIFICATION REQUIRED`）。

---

## 1. 四层归属框架（定义）

Curis 已有三层（组织层 / 运行层 / 能力层）。本计划在其上做**契约归属分类**，便于判断「该契约由谁拥有、谁消费」：

| 层 | 含义 | 在本计划中承担 |
|---|---|---|
| **Company OS Shared** | 跨 Workspace 共享的运行层 / 组织层原语（公司级中枢） | Responsibility Requirement（扩展 P1）、Organization Routing、Shared Employee + 服务关系、Lightweight Queue/Bottleneck |
| **Content Growth Domain** | Content Growth 业务专属对象（经营/内容/渠道） | Office、Channel、Channel Account、Account Pool、Content Opportunity/Intent、Target Account、Content Variant、Publication（记录） |
| **Workspace Instance** | 具体 Professional Workspace 的执行面（消费契约、持有实例态） | Content Production WS / 各 Channel Ops WS——它们是契约的**消费者 + 实例编排面**，不另立契约，但持有实例作用域配置（如某 WS 服务于哪些 Office、WS 本地队列视图） |
| **Capability·Connector** | 可替换的能力执行方（生产工具 / 渠道连接器） | Douyin/XHS/... Connector（OAuth/Scope/发布/互动/数据）、CapCut/即梦/Kling/HeyGen/Runway（生产）。本计划**只引用**，不重定义其内部 |

> 关键约束：Content Growth Domain 契约**调用** Capability·Connector 执行，但**不拥有**其实现；Company OS Shared 契约供所有 Workspace（含未来非 Content Growth 业务）复用。

---

## 2. 九个契约规划

### 契约 1 — Office / Operating Context Contract

**目的**：固化「经营单元」与其上层容器，落实 DELTA 1（Office 与 Organization 正交）。

**关键元素**：
- `Operating Context`：`id` / `company_id` / `name` / `type`（业务线容器）/ `shares_growth_context?`
- `Office`：`id` / `operating_context_id` / `name` / `business_goals` / `positioning` / `audience` / `content_strategy` / `knowledge_refs[]` / `growth_context` / `default_target_account_set[]` / `account_pool`（经 Binding 关联）
- 关系：`Operating Context 1—* Office`；`Office *—* Channel Account`（经 `OfficeAccountBinding`）

**归属层**：
- `Office` → **Content Growth Domain**
- `Operating Context` → **Company OS Shared**（通用业务容器；未来可承载非 Content Growth 业务线）

**依赖**：无（基础契约）。
**开放问题**：
1. Operating Context 是否每个 Office 必有一个，还是可多 Office 共享一个容器？
2. 「Office」命名是否与 Curis 既有组织层词汇冲突（避免与通用 workspace/office 概念混淆）？需对齐组织层术语。

---

### 契约 2 — Channel / Channel Account / Account Pool Contract

**目的**：固化平台事实层、账号经营层、绑定关系（落实 DELTA 1 的 `office_id` → `OfficeAccountBinding`）。

**关键元素**：
- `Channel`：`id`（DOUYIN/XHS/TIKTOK/BILIBILI/YOUTUBE）/ `capabilities_ref`（→ Connector 目录）/ `policy_context` / `constraints`（ratio/duration/resolution/copyright/scheduling 支持度）
- `Channel Account`：`id` / `channel`(FK) / `account_bindings[]`（office_id, role, binding_state）/ `identity` / `positioning` / `niche_pillars[]` / `audience` / `tone_style` / `language` / `format_preference` / `publishing_rhythm` / `growth_goals` / `historical_performance` / `authorization_ref`（→ Connector 凭据引用）/ `platform_policy_context` / `brand_knowledge_refs[]`
- `OfficeAccountBinding`：`office_id` / `channel_account_id` / `role` / `binding_state`
- `Account Pool`：由 Office 的 `account_bindings` 派生（或显式池实体）

**归属层**：
- Channel / Channel Account / Account Pool / Binding → **Content Growth Domain**
- `authorization_ref` / `capabilities_ref` 的执行机制 → **Capability·Connector**

**依赖**：契约 1（Office）。
**开放问题**：
1. 首版推荐 1 Account : 1 Office（结构支持 N:N），N:N 的触发场景（联名号/共享账号）何时启用？
2. `authorization_state` 失效（OAuth 过期 / Scope 撤销）时，运行层如何降级（暂停该 Account 发布）？
3. Channel `capabilities_ref` 与具体 Connector 的映射表（哪个 Connector 服务 DOUYIN 的 publish/engage/analytics）在何处定义？

---

### 契约 3 — Content Opportunity / Intent Contract

**目的**：固化「跨账号真正共享的上游对象」（本轮核心结论：共享的是 Intent/Opportunity，非母版）。

**关键元素**：
- `Content Opportunity`：`id` / `source`（Growth Intelligence 信号）/ `topic` / `score` / `rationale` / `suggested_offices[]`
- `Content Intent / Package`：`id` / `linked_opportunity_id` / `topic` / `core_message` / `business_goal` / `audience_hypothesis` / `verified_facts` / `source_material` / `brand_requirements` / `cta_intent` / `available_assets` / `knowledge_evidence_refs[]`

**归属层**：**Content Growth Domain**（属 Company 级 Growth Context，非 Office 私有；经 Target Account 再分流到各 Office 账号）。

**依赖**：契约 1（Office 上下文）、契约 2（平台/账号约束供后续生产要求推导）。
**开放问题**：
1. Intent 是 Company 级共享还是可跨 Company？本计划限定单 Company 内 Growth Context。
2. Intent 是否允许「先有 Intent 再选 Office」（跨 Office 复用同一母题）？设计期需明确 Intent 与 Office 的弱绑定关系。

---

### 契约 4 — Target Account Contract

**目的**：固化「Target 是 Account 而非 Platform」+「每 Intent 选子集」+「前置生成生产要求」。

**关键元素**：
- `Target Account Set / Distribution Targets`：`content_intent_id` / `selected_accounts[]`（相关 Office `account_pool` 的子集）/ `selection_basis`（`DEFAULT_SET` / `AI_RECOMMENDED` / `MANUAL`）/ `production_requirements`（由 selected_accounts 推导：ratio 并集、时长下限、copyright 占位、disclosure 字典、publishAt 占位等）

**归属层**：**Content Growth Domain**。
**依赖**：契约 1（Office 的 `default_target_account_set`）、契约 2（Account Pool）、契约 3（Intent）。
**开放问题**：
1. `default_target_account_set` 与 AI 推荐冲突时，用户否决权如何处理？
2. 跨 Office 的 Intent 选择账号时，`selected_accounts` 如何跨越多个 Office 的池？

---

### 契约 5 — Content Variant / Publication Contract

**目的**：固化「Variant 归属具体 Account（可每账号多份）」+「Publication 为 per-Account 真相源」。

**关键元素**：
- `Content Variant`：`id` / `content_intent_id` / `channel_account_id`（account-scoped）/ `ratio` / `duration` / `edit_variant` / `caption` / `title` / `cover` / `hashtag` / `music` / `disclosure` / `platform_policy_result` / `production_config` / `reuse_mode`（`HIGH_REUSE` / `FULL_DIVERGENCE`）
- `Publication`：`id` / `variant_id` / `channel_account_id` / `publish_status` / `publish_receipt`（→ Connector 回执引用）/ `scheduled_at?` / `published_at`

**归属层**：
- Content Variant / Publication（记录） → **Content Growth Domain**
- Publication 的实际执行（发布调用、回执产生） → **Capability·Connector**

**依赖**：契约 3（Intent）、契约 4（Target Account）、契约 2（Channel Account + Connector 引用）。
**开放问题**：
1. 定时发布（scheduling）各平台支持度不等（YouTube `publishAt`✅ / 抖音官方 API ❌），`scheduled_at` 字段如何按平台条件化（POLICY VERIFICATION REQUIRED，不在此计划固化强规则）？
2. 同一 Variant 是否允许对应多次 Publication（重发 / 多版本）？

---

### 契约 6 — Responsibility Requirement Contract

**目的**：固化「Process 只声明责任需求，不绑固定 Employee」，扩展 Frozen Shared Pattern P1（三层责任语义）。

**关键元素**（在 P1 的 Responsibility / Holder / Executor / Status 之上新增）：
- `Responsibility Requirement`：`id` / `process_node_id` / `required_capability` / `required_specialty` / `required_content_type` / `required_platform_experience` / `required_language` / `account_context` / 约束（**非执行人**）
- Content Growth 责任目录（候选）：`Topic Research` / `Script Writing` / `Video Production` / `Subtitle Production` / `Content Review` / `Channel Adaptation` / `Engagement Handling` / `Analytics Synthesis`

**归属层**：**Company OS Shared**（扩展 P1，供所有 Workspace 复用；责任**词汇**属 Content Growth Domain，机制属 OS Shared）。
**依赖**：契约 8（Employee 属性供匹配）、契约 2（Channel Account `tone_style` 可做风格匹配）。
**纪律**：本契约**扩展** P1，不修改 P1–P7。
**开放问题**：
1. 责任目录是否按 Content Type（VIDEO/NOTE/IMAGE_SET）细分 required 约束？
2. 责任 `account_context` 如何从 Channel Account 继承 `tone_style` 做自动风格匹配？

---

### 契约 7 — Organization Routing Contract

**目的**：固化「Router = 确定性低成本机械调度」，落实 DELTA 2（Router / Team Lead 分离）。

**关键元素**：
- `Router Spec`：输入（Responsibility Requirement + Account Context + Employee/Team 属性 + Capacity/Availability）/ 匹配维度（capability/specialty/platform_experience/content_type/language/style/capacity/availability）/ 确定性规则 / 输出（Holder→Executor）
- `Team Lead Exception Path`：**仅**异常/管理判断介入——`Priority Conflict` / `Blocker` / `Quality·Acceptance` / `Exception Handling` / `Standards·Coaching` / `Abnormal Workload Intervention`
- 明确：**常规 Queue/Assignment/Load balancing 属 Router，不调 Team Lead**；Team Lead 是 Employee/Role 实例，非新 primitive

**归属层**：**Company OS Shared**（通用路由引擎；Team Lead 实例属 OS Shared 的 Employee/Role）。
**依赖**：契约 6（Responsibility Requirement）、契约 8（Employee/Team + 服务关系）。
**开放问题**：
1. Router 实现为规则引擎还是轻量 LLM？设计期定（目标：确定性、低成本）。
2. Team Lead 作为 Employee/Role，是否也由 Router 在异常时路由（而非固定指派）？

---

### 契约 8 — Shared Employee service relation

**目的**：固化「Employee 属 Organization 轴，经 Responsibility Assignment 服务 N 个 Office」（DELTA 1）。

**关键元素**：
- `Employee`（OS Shared）：`id` / `capability` / `specialty` / `platform_experience` / `content_type` / `language` / `style` / `capacity` / `availability` / `organization_membership`（Department/Team）
- `Responsibility Assignment`（服务关系）：`employee_id` / `office_id`（或责任域）/ `responsibility_types[]` / `capacity_share`
- 关系：`Employee *—* Office`（经 Assignment，非组织隶属）

**归属层**：**Company OS Shared**（Employee 实体 + 服务绑定；Office 引用来自 Content Growth Domain）。
**依赖**：契约 1（Office）、契约 6（Responsibility Requirement 类型）。
**开放问题**：
1. Employee 的 `organization_membership`（Department/Team）与 `office_id` 服务关系如何并存展示？
2. `capacity_share` 跨多 Office 时如何计量（首版可简化为整段可用性）？

---

### 契约 9 — Lightweight Queue / Bottleneck Candidate

**目的**：固化「首版只采集 Runtime Facts → Bottleneck Candidate」，落实 DELTA 3（降复杂度）。

**关键元素**（仅观测，不做复杂推断）：
- `Runtime Facts`（per Responsibility）：`queue_depth` / `waiting_since` / `oldest_wait` / `active_count` / `employee_availability`
- `Bottleneck Candidate`：`responsibility_id` / `signal` / `threshold_breach` / `suggested_action`（`add_employee`）

**归属层**：**Company OS Shared**（运行层观测；跨域，不限于 Content Growth）。
**依赖**：契约 6（Responsibility）、契约 8（Employee availability）。
**明确不做（DELTA 3）**：完整 throughput 预测 / 复杂 capacity score / 智能负载算法 / 企业级 scheduler（留待规模增长后演化）。
**开放问题**：
1. 阈值（静态规则 / 自适应基线）如何设定？
2. 用户拒绝「增加员工」建议后，系统是否降级（暂停部分 Production / 排队）？

---

## 3. 契约依赖与建议固化顺序

```
① Office / Operating Context        （基础：经营单元 + 容器）
        ↓
② Channel / Channel Account / Account Pool   （账号矩阵 + 绑定）
        ↓                          ↘
⑥ Responsibility Requirement     ⑧ Shared Employee + 服务关系   （组织基础，并行）
        ↓ ⑦ Organization Routing （需 ⑥ + ⑧）
        ↓
③ Content Opportunity / Intent    （上游共享对象）
        ↓
④ Target Account                  （需 ① + ② + ③）
        ↓
⑤ Content Variant / Publication   （需 ③ + ④ + ②；执行经 Connector）
        ↓
⑨ Lightweight Queue / Bottleneck  （观测 ⑥/⑧，贯穿运行）
```

**建议顺序**：① → ② →（⑥ ∥ ⑧）→ ⑦ → ③ → ④ → ⑤ → ⑨。
Workspace Instance（Content Production WS / 各 Channel Ops WS）在契约 ⑤ 前后接入，作为执行面消费上述契约。

---

## 4. 各契约归属速查表

| # | 契约 | 主归属层 | 次接触层 |
|---|---|---|---|
| 1 | Office / Operating Context | Office=CG Domain；Operating Context=OS Shared | — |
| 2 | Channel / Channel Account / Account Pool | Content Growth Domain | Capability·Connector（auth/cap） |
| 3 | Content Opportunity / Intent | Content Growth Domain | （驱动 Runtime 任务图） |
| 4 | Target Account | Content Growth Domain | — |
| 5 | Content Variant / Publication | Content Growth Domain | Capability·Connector（发布执行） |
| 6 | Responsibility Requirement | Company OS Shared（扩展 P1） | Content Growth Domain（责任词汇） |
| 7 | Organization Routing | Company OS Shared | — |
| 8 | Shared Employee service relation | Company OS Shared | Content Growth Domain（Office 引用） |
| 9 | Lightweight Queue / Bottleneck | Company OS Shared | （per Responsibility 观测） |

**Workspace Instance**：非独立契约，是上述契约的**消费者 + 实例编排面**（持有 WS 本地队列视图、服务于哪些 Office 的实例配置）。

---

## 5. 冻结前必须通过的检查闸门（Verification Gates）

本计划不固化，但下一阶段设计这些契约时须先闭合：

1. **POLICY VERIFICATION REQUIRED**（继承前序结论）：抖音「AI 托管封禁 / 人工审核要求」须以**官方政策原文**核实（适用账号 / 场景 / 自动化定义 / 人工审核要求）后，方可写入任何 Frozen Product Rule。本计划**不**将「每次发布必须人工点击」写死。
2. **Channel 能力确认**：各平台发布 / 定时 / 评论 / 私信 / 数据能力须以**官方 open 文档**确认，不得因第三方 SaaS 能而推断官方 API 允许（继承前序纪律）。
3. **P1 兼容**：契约 6 必须扩展而非修改 Frozen P1–P7 的责任语义。
4. **XHS / RD Instance 不变**：本计划不触碰已 Approved 的 XHS Instance 与 RD Instance；XHS 未来纳入更高层模型仅作说明，不改当前实例。
5. **Connector 不开发**：契约 2/5 仅引用 Capability·Connector，其实现（OAuth/Scope/发布/互动/数据）在 Connector 设计期另行规划，不在本计划范围。

---

## 6. 明确不在本计划范围

- ❌ 任何字段级 schema / 数据库表 / API 签名
- ❌ Frozen 任何 Product Rule / Shared Pattern
- ❌ 修改 Product Blueprint / P1–P7 / XHS·RD Instance / Runtime / Authority Map
- ❌ 开发 Connector 或 Runtime 代码
- ❌ 绘制任何 UI / 高保真 / Prototype
- ❌ 解决平台政策强结论（仍 POLICY VERIFICATION REQUIRED）

---

## 7. 状态与下一步

**当前状态**：`SHARED CONTRACT PLAN REVIEW REQUIRED`
**上游状态**：本轮 4 份 Content Growth 文档 = `CONTENT GROWTH ARCHITECTURE DELTAS APPLIED`
**上一轮 4 份 Content Production × Channel Ops 文档**：被本轮 DELTA 修正（KEEP/MODIFY/REINTERPRET 见 Operating Model §末）。

**下一步（待 Review 批准）**：
1. 按 §3 顺序逐契约进入 **Contract Design**（落地字段/关系/规则草案）。
2. 先闭合 §5 的 Verification Gates（尤其政策核实）。
3. 将 9 个契约归并到 **Company OS Shared Contract Set** 与 **Content Growth Domain Contract Set** 两份权威契约文档，再视成熟度 Frozen。

*本文件为计划，未固化。所有契约以 Review 批准后的 Contract Design 阶段产出为准。*

---

*CONTENT GROWTH ARCHITECTURE DELTAS APPLIED — SHARED CONTRACT PLAN REVIEW REQUIRED*
