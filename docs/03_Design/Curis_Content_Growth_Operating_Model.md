# Curis · Content Growth 上层运营模型（最终收敛轮）

> **状态**：CONTENT GROWTH ARCHITECTURE DELTAS APPLIED（DELTA 1/2/3 已应用 · 原 REVIEW REQUIRED 已收敛）
> **类型**：Reference Only · 上层业务模型收敛（非权威文档）
> **纪律**：不画 UI / 不改 Frozen Shell / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Connector / 不改 Runtime / 不改 Authority Map / 不改 Product Blueprint
> **关联文档**：`Curis_Channel_Account_Matrix_Model.md`（Channel/Account 矩阵）、`Curis_Organization_Routing_Architecture.md`（组织/路由）、`Curis_Content_Growth_Company_Evolution_Model.md`（公司演化）
> **前置**：上一轮 `Curis_Content_Production_Channel_Operations_Model.md` 等 4 份（本轮 DELTA 见 §末）

---

## 0. 本轮要解决的六大张力

Content Growth 同时存在的现实：

1. **同平台多账号、定位不同**（Douyin A=AI科普 / Douyin B=个人IP）
2. **多平台多账号、定位相同**（Douyin·Curis AI / XHS·Curis AI / Bilibili·Curis AI / TikTok·Curis AI）
3. **同一 Office 内并非每条内容都发所有账号**（Content #101 发 3 个、Content #102 发 2 个）
4. **上游能力 / Employee 可跨账号、跨平台共享**（字幕员工服务所有视频）
5. **公司规模增长后，Employee / Team / Queue 自然演化**（单人→多人→团队）
6. **普通用户不能被迫理解复杂组织设计**（只认 Office + Employee + Connected Accounts + Current Work + Needs CEO）

本轮结论：**上一轮「Production × Channel 拆两层」方向正确，但缺了第三层 —— Office（经营单元）与 Content Intent（跨平台/跨账号真正共享对象）**。补齐后形成「Office × Content Intent × Channel Account × Professional Workspace」的稳定上层模型。

---

## A. Office 的重新定义

> **Office ≠ Platform，Office ≠ Account，Office ≠ Content Type。**

**Office = 一套共同的经营目标 / 定位 / 受众 / 内容策略 / Knowledge / Growth Context（增长上下文）。**

它是 Company 下的**业务经营单元**（属 `Business / Operating Context` 轴，与 `Organization` 轴正交；详见 §G DELTA 1），拥有：

- 共享经营目标与定位（这条业务线为谁、解决什么、讲什么故事）
- 受众定义（人群 / 场景 / 转化路径）
- 内容策略与 pillars
- 专属 Knowledge / Brand / Evidence 引用
- **Account Pool**（绑定的 Channel Account 集合，1..N）
  - Growth Context（历史表现、复盘知识、反馈沉淀）

**正交性（DELTA 1）**：Office 是**经营单元**，**不是组织节点**——它**不拥有 / 不隶属 Employee**。Employee 属于独立的 **Organization** 轴（Company → Organization → Department / Team / Role / Employee），通过 **Responsibility Assignment（责任指派）** 服务 Office，而非组织归属。Office ≠ Department，Office ≠ Team。详见 §G 与 Doc 3。

**现实佐证**（本轮检索）：抖音 / 小红书「矩阵号」实践明确反对「一个平台一个 Office」或「一个账号一个 Office」。真实做法是「围绕不同人群、不同场景、不同转化路径建立的内容体系」，每个账号有清晰**角色分工**（品牌号 / 产品号 / IP号 / 区域号 / 员工号），前端分散、后端承接统一。这说明**经营定位**才是分单元的正确边界，平台与账号只是它的载体。

**候选实例（本轮采用）**：

```
Office A：个人 IP
└ Douyin · 个人IP号                       （1 账号）

Office B：AI工具内容
├ Douyin · AI工具号
├ XHS · AI工具号
├ Bilibili · AI教程号
└ TikTok · AI Tools                        （4 账号，跨平台同定位）

Office C：生活方式
├ Douyin · 生活号
└ XHS · 生活号                            （2 账号，跨平台同定位）
```

**判定**：此模型**优于**「一个平台一个 Office」（无法表达同定位跨平台）与「一个账号一个 Office」（无法表达同平台不同定位），应作为长期产品模型。

---

## B. 同时解决首版两种场景

**场景 1：同平台多账号、定位不同 → 允许两个 Office**

```
Douyin Account A = AI科普   → Office: AI科普内容
Douyin Account B = 个人IP   → Office: 个人IP
```
两 Office 各自拥有独立目标 / 受众 / 策略 / Knowledge，甚至不同 Brand 调性。

**场景 2：多平台多账号、定位相同 → 允许同一 Office 绑多个账号**

```
Office: Curis AI
├ Douyin · Curis AI
├ XHS · Curis AI
├ Bilibili · Curis AI
└ TikTok · Curis AI
```

**上游共享、下游分流**：Research / Knowledge / Topic Analysis / Content Opportunity / Content Strategy 在 Office 层共享；产生**平台 / 账号差异**（定位微调、语言、ratio、policy）后再分流到各 Channel Account。

**铁律**：两种模式**必须同时支持，不能二选一**。

---

## C. Channel 与 Channel Account 分离

**Channel = 平台本身**（Douyin / XHS / TikTok / Bilibili / YouTube …）。

- 决定「平台**允许什么 / 要求什么**」：能力边界、政策、约束（如 Bilibili 强制 copyright、YouTube 支持 publishAt、各平台 AI disclosure 字典）。
- 属**平台事实层**，与任何用户账号无关。

**Channel Account = 用户在该平台实际经营的账号**。

- 一个 Channel 可绑 N 个 Channel Accounts（如 Douyin 上有 AI工具号 + 个人IP号）。
- 决定「**这个账号应该做什么 / 用什么风格经营**」。

**Channel Account 候选 Context**（详见 Doc 2）：

`identity` / `positioning` / `niche_pillars` / `audience` / `tone_style` / `language` / `format_preference` / `publishing_rhythm` / `growth_goals` / `historical_performance` / `authorization_state` / `connected_capabilities` / `platform_policy_context` / `brand_knowledge_refs`

**判定**：
- Channel 决定 **平台允许/要求**（能力 + 政策）
- Channel Account 决定 **账号经营方式**（定位 + 风格 + 策略）

---

## D. Target Channel 升级为 Target Account

上一轮「Target Channels 前置」升级为：

> **Target Accounts / Distribution Targets 前置。**

- Office 拥有 **Account Pool**。
- 每个 Content Intent **只从 Account Pool 中选择本次实际目标账号子集**。
- 绑定 N 个账号 **≠** 每条内容群发所有账号。

```
AI工具 Office（4 账号）
  Content #101：Douyin ✓  XHS ✓  Bilibili ✓  TikTok ✕
  Content #102：Douyin ✓  XHS ✕  Bilibili ✕  TikTok ✓
```

- Business / Office 可保存**默认 Target Account Set**（如「常规发 Douyin+XHS+Bilibili」）。
- AI 可根据**内容特征 + 历史表现**推荐本次目标账号，用户**不必每条机械勾选**。
- 这是 Office 与 Production / Channel Ops 的**契约点**：Target Account Set → 生成 Account-aware Production Requirements。

---

## E. Canonical 层上移（真正共享对象不是母版）

上一轮模型：`Canonical Content → Production Result → Channel Variant`
**问题**：过早假设「先做一个母版成品，再适配所有平台」。

**补齐上游层**：

```
Growth Intelligence
  → Content Opportunity      （什么值得做）
    → Content Intent / Package（准备表达什么）
      → Target Accounts
        → Account-aware Production
          → Content Variant
            → Publication → Engagement → Analytics
```

**关键判定：真正跨平台 / 跨账号共享的对象，是 `Content Opportunity` / `Content Intent` / `Content Package`，而不是最终 `Canonical Video`。**

`Content Intent` 候选包含：

- `topic`（主题）
- `core_message`（核心信息）
- `business_goal`（业务目标）
- `audience_hypothesis`（受众假设）
- `verified_facts`（已核实事实）
- `source_material`（素材来源）
- `brand_requirements`（品牌要求）
- `cta_intent`（行动召唤意图）
- `available_assets`（可用素材）
- `knowledge_evidence_refs`（知识 / 证据引用）

它回答：**「我们准备讲什么」**，不是「最终视频已经长什么样」。

> 这不 REJECT `Canonical Content / Production Result` —— 二者仍作为 **HIGH REUSE 场景的母版**（见 F）。而是明确：**Intent 是跨账号复用的「一次推理」，Production Result 是跨账号复用的「一次生产」**，两者在不同颗粒度上共享，互不替代。

---

## F. Production 必须允许动态分流

**禁止规定**：一个 Canonical Video 必须适配所有账号。

**必须同时支持两种生产形态**：

**HIGH REUSE（高复用）**
同一 Production Result → 多账号只改 `Caption / Cover / Metadata / Minor Edit`。

**FULL DIVERGENCE（完全分流）**
同一 Content Intent → 不同账号产出**完全不同形态**：

```
Douyin AI号      → 30秒 快节奏口播
Douyin 个人IP号   → 60秒 个人观点
XHS 效率号       → 图文笔记
Bilibili 教程号   → 8分钟 教程
TikTok 海外号    → 英文短视频
```

**系统决策依据**：
`Content Intent` + `Platform Requirements` + `Channel Account Strategy` + `Audience` + `Historical Performance` + `Employee Capability`

**原则**：
> **Shared reasoning once, divergent production when necessary.**
> （一次推理共享；必要时才生产分流。）

现实佐证：抖音矩阵「一次拍摄多次拆解」「优质素材经二次创作适配不同账号风格」、小红书「图文转视频 / 视频转图文」、各账号「和而不同」—— 均为同一母题下按账号差异化表达。

---

## G. Content Growth 上层业务模型

恢复并重新审查「Content Growth / 内容增长办公室」。未来业务**不应**被理解为彼此孤立的 XHS Office / Douyin Office / Video Office。

**推荐 CONTENT GROWTH 八阶段闭环**：

```
1. Growth Intelligence   趋势 / 搜索 / 评论 / Analytics / Knowledge
2. Content Opportunity   什么值得做
3. Content Strategy/Intent 准备表达什么（Content Intent/Package）
4. Target Account Routing 针对哪些账号（从 Account Pool 选子集）
5. Account-aware Production 按账号/平台要求生产（HIGH REUSE 或 DIVERGENCE）
6. Channel Operations    Review / Publish / Engage / Analytics（每 Account）
7. Unified Growth Feedback 跨账号、跨平台回流
8. Next Growth Cycle     驱动下一轮 Opportunity
```

**Content Growth 应归属哪个 Curis 概念？**

- ❌ 不新建顶层产品概念（用户硬约束）。
- ✅ 推荐：**Business 级跨 Workspace 运营域（运行层编排）**，在已有 Curis 三层架构内实现。关键修正（**DELTA 1 — Office 与 Organization 正交**）：二者都是 Company 下的并列轴，**不存在**「Company → Office → Employee/Team」的隶属链：

  ```
  Company
  ├ Business / Operating Context      （经营上下文容器）
  │   └ Office ×M                     （经营单元：目标/定位/受众/策略/Knowledge/Account Pool/Growth Context）
  └ Organization                      （组织结构，与 Office 正交）
      ├ Department
      ├ Team
      ├ Role
      └ Employee
  ```

  - **Office ≠ Department，Office ≠ Team**。Office 表达「为谁经营」；Department/Team 表达「谁在组织结构里」。
  - **Employee 不要求隶属于 Office**：Employee 属于 Organization（Department/Team），通过 **Responsibility Assignment（责任指派）** 服务 N 个 Office。Employee ↔ Office 是「服务 / 责任承担」关系，不是「组织归属」关系。
  - **运行层**：Content Growth 八阶段闭环 = 跨 Office + 跨 Professional Workspace 的业务流程编排（目标→规划→执行→验收→返工→完成）。
  - **能力层**：Capability Provider（生产工具 / 渠道 Connector）可替换
- 若 Curis 已有「Workspace Family」概念，则 Content Growth 最自然的承载是 **Workspace Family**（协调多个 Professional Workspace 的共享增长上下文）；否则它就是 **Business 级 operating domain**，由运行层 workflow 具体实现，并非新 primitive。

**关键**：Content Growth 不是又一个新的孤立 Workspace，而是**跨 Office + 跨 Professional Workspace 的编排与增长上下文**。

---

## H. Organization 与 Process 分离（本轮核心二）

**Business Process 不得绑定固定 Employee。**

Process 只声明 **Responsibility Requirement**（需要什么责任能力）：

```
Topic Research / Script Writing / Video Production /
Subtitle Production / Content Review / Channel Adaptation …
```

然后 **Organization Routing** 决定谁承担：

```
Business Process
  → Responsibility Requirement      （WHAT：需要什么责任）
    → Organization Routing          （WHO：谁承担）
      → Responsibility Holder       （当前责任持有人）
        → Current Executor          （当前执行人，可为 none/等待）
          → Employee / Team         （具体岗位）
            → Execution Binding     （绑定到具体任务实例）
              → Agent / Skill / Tool / Connector （HOW：能力）
```

**三句判诀**：
- **Process asks WHAT**
- **Organization decides WHO**
- **Capability determines HOW**

**禁止建立固定 DAG**（如「字幕永远由员工 X 做」）。路由是动态的、按责任需求 + 上下文求解。

---

## I. Employee 跨 Office / Account 共享

**示例**：Subtitle Employee 职责 =「为公司所有视频生产字幕」，可同时服务 Douyin Office / XHS Office / Bilibili Office，**不必复制**为「Douyin字幕员工 / XHS字幕员工 / B站字幕员工」。

**Employee 可拥有**：

`capability` / `specialty` / `platform_experience` / `content_type` / `language` / `style` / `capacity` / `availability`

**Org Router 分配依据**：
`Responsibility Requirement` + `Account Context` + `Employee Specialty` + `Capacity` + `Availability`

**硬约束**：**不要求普通用户配置 Routing Rules**。路由由系统后台求解。

---

## J. 组织自然演化

**必须支持渐进演化，Curis 不规定分组维度**：

```
早期：  Subtitle Employee A → 服务所有视频
增长：  Subtitle Employee A / B / C
再增长：Subtitle Team
        ├ Team Lead
        ├ Employee A
        ├ Employee B
        └ Employee C
```

**Team Lead 真实责任（DELTA 2：仅管理判断 / 异常，非机械调度）**：

Team Lead 是 **Employee / Role**（运行层管理角色），**不是新的系统 primitive**。正常机械调度由 **Organization Router** 确定性完成（见 Doc 3 §3），Team Lead **不介入**每个任务的常规路由。

Team Lead 只在**异常 / 管理判断**时介入：
- `Priority Conflict`（优先级冲突裁决）
- `Blocker`（阻塞处理 / 升级）
- `Quality / Acceptance`（验收与质量把关）
- `Exception Handling`（异常处置）
- `Standards / Coaching`（标准制定与辅导）
- `Abnormal Workload Intervention`（异常负载干预，如突发积压）

> **不属于 Team Lead**：`Queue`（队列）/ `Assignment`（常规分派）/ `Load balancing`（常规负载均衡）属 Router 的确定性职责（DELTA 2），Team Lead 不逐任务决策。避免每个任务都经过额外 LLM Team Lead，降低 Token / latency / complexity。

**允许另一家公司按平台分组**：
`Douyin Team` / `Bilibili Team` / `Overseas Team`。

**Curis 不规定**：必须按平台分组 **或** 必须按职能分组。

---

## K. 普通用户认知必须保持简单（硬约束）

**首版用户只需理解**：

`Office` · `AI Employee` · `Connected Accounts` · `Current Work` · `Needs CEO`

**不向普通用户暴露**：Organization Router / Capacity / Queue / Load balancing / Team topology 作为必配项。

**复杂组织由 Curis 自管**。示例：

> 系统检测到：字幕责任平均等待时间持续升高，上游产出超过字幕处理能力。

**CEO Assistant 白话汇报**：
> 「最近视频经常卡在字幕环节。建议增加一名字幕员工。」

**用户只做**：`[按建议增加]` / `[先不增加]`

**后台完成**：Employee 创建 → 加入 Routing Pool → Capacity 更新 → Responsibility 指派。

---

## L. Capacity / Queue / Bottleneck 候选（DELTA 3：首版降复杂度，暂不 Frozen）

研究但不 Frozen：`Capacity` / `Work Queue` / `Load` / `Bottleneck` / `Team Formation`。

**是否应成为 Company OS Shared Runtime Candidate？**

- ✅ 方向：是。Capacity / Queue / Bottleneck 信号应作为 **Company OS 共享运行层** 的轻量候选能力，服务于 K 节的「系统自管组织」与 J 节的「自然演化」。
- ⚠️ **DELTA 3 — 首版降复杂度**：方向保留为 Company OS Shared Candidate，但首版**不建设**完整 throughput 预测 / 复杂 capacity score / 智能负载算法 / 企业级 scheduler。
- ✅ 首版最小 **Runtime Facts**（仅观测，不做复杂推断）：
  1. `queue_depth`（某 Responsibility 当前排队深度）
  2. `waiting_since` / `oldest_wait`（最旧任务等待时长）
  3. `active_count`（在制数量）
  4. `employee_availability`（相关 Employee 可用性）
  → 由上述事实直接产生 **Bottleneck Candidate**（如某 Responsibility `oldest_wait` 持续超阈值）。
- ✅ **一键「增加员工」建议**：Bottleneck Candidate 触发 → CEO Assistant 白话汇报 → 用户 `[按建议增加]` / `[先不增加]` → 后台完成 Employee 创建 + 加入 Routing Pool + Capacity 更新 + Responsibility 指派。
- 🔄 **后续演化**（规模增长后，非首版）：`throughput` 度量 / 自适应 capacity / Team scheduling / load balancing。
- ❌ **不为未来一次性建设大型调度系统**。

---

## M. Unified Growth Feedback

`Publication / Engagement / Analytics` **继续保持 per-Account、per-Platform 事实真相源**（上一轮结论不变）。

但必须**回流 Growth Intelligence**：

```
同一主题：
  Douyin AI号    → 完播表现好
  Bilibili 教程号 → 用户更关注成本
  XHS 效率号     → 收藏表现高
        ↓
  Cross-account Growth Knowledge（跨账号增长知识）
        ↓
  驱动下一轮：Content Opportunity → Target Accounts → Account-aware Production
```

这正是 G 节第 7 步，使 Content Growth 形成**闭环**而非单向管道。

---

## N. AiToEarn 定位继续保持

上一轮结论基本保留：

- **主：Reference Implementation（参考实现，MIT）**
- 借：多平台 Account Binding、Distribution UX、Connector/MCP 抽象、渠道配置化
- **不继承**：Relay 凭据代理、Content/Channel 混淆、浏览器自动互动、缺失的 Publication/Analytics 数据契约

本轮新增印证：AiToEarn 的「多账号矩阵」也未见 Office / 跨账号定位分流 / 共享 Employee 概念 —— 再次确认其**产品模型不足**，Curis 应自有 Office × Intent × Account 上层模型。

---

## P. 16 个必答问题（最终结论）

**P1. Office 的准确业务定义？**
Office = 一套共同的经营目标/定位/受众/内容策略/Knowledge/Growth Context 的业务经营单元（Company 下部门/业务线级），拥有 Account Pool。≠ Platform / Account / Content Type。

**P2. 一个 Office 是否允许绑定 N 个 Channel Accounts？**
✅ YES。跨平台同定位（Office B/C）即典型形态。

**P3. 同平台不同定位账号如何处理？**
→ 拆成**不同 Office**（各自独立目标/受众/策略/Knowledge），每 Office 绑各自账号。

**P4. 多平台同定位账号如何处理？**
→ **同一 Office 绑 N 个账号**（场景 2），上游共享、下游按平台差异分流。

**P5. Target 应该是 Platform 还是 Account？**
→ **Account**（Target Accounts / Distribution Targets）。Channel 只决定平台允许/要求，决定「发哪个号」的是 Account（含其定位/策略）。

**P6. 真正跨平台/跨账号共享的 Canonical 对象是什么？**
→ **Content Opportunity / Content Intent / Content Package**（一次推理共享）。Production Result 是次一级的「一次生产共享」（HIGH REUSE 母版）。两者并存、颗粒度不同。

**P7. Production 在什么时候开始分流？**
→ 在 **Content Intent 确定 + Target Accounts 选定 + Account-aware Production Requirements 生成** 之后。系统据 Intent/Platform/Account Strategy/Audience/History/Capability 决定 HIGH REUSE 或 FULL DIVERGENCE。

**P8. Content Variant 应归属于 Platform、Account 还是 Content Intent？**
→ 归属 **Channel Account**（每 Account 一份，可多份以支持 DIVERGENCE）。Content Intent 是 Variant 的来源与约束，Platform 是 Account 的所在；Variant 实体挂在 Account 上。

**P9. Process / Responsibility / Organization / Employee / Capability 的准确关系？**
→ Process→Responsibility Requirement(WHAT) → Organization Routing(WHO) → Responsibility Holder → Current Executor → Employee/Team → Execution Binding → Agent/Skill/Tool/Connector(HOW)。Process 不绑固定 Employee；组织动态求解；能力决定如何执行。**DELTA 1**：Employee/Team 属 **Organization** 轴（与 Office 正交），经 Responsibility Assignment 服务 Office，非组织隶属。**DELTA 2**：正常路由由 Router 确定性完成，Team Lead 仅介入异常/管理判断。

**P10. Shared Employee 如何跨多个 Office 服务？**
→ Employee 拥有 specialty/platform/content_type/language/capacity 等属性；Org Router 按 Responsibility Requirement + Account Context + Employee 属性 + Capacity/Availability 动态分配，不复制、不要求用户配规则。

**P11. 什么情况下 Employee 应演化成 Team？**
→ 当单 Employee 容量不足（Capacity 信号：等待升高 / 在制堆积），且同类责任持续超载 → 演化出同 specialty 的多 Employee + Team Lead（Queue/Assignment/Load balancing/Blocker/Acceptance）。Curis 按职能或按平台分组均可，不强制。

**P12. Team Lead 的真实责任是什么？**
→ Team Lead 是 **Employee/Role**（运行层管理角色，非新 primitive）。**仅管理判断/异常**介入：Priority Conflict / Blocker / Quality·Acceptance / Exception Handling / Standards·Coaching / Abnormal Workload Intervention。**不**负责逐任务机械调度（Queue/Assignment/Load balancing 属 Organization Router 的确定性职责，DELTA 2）。避免每个任务经额外 LLM Team Lead。

**P13. Capacity / Queue / Bottleneck 首版需要做到什么程度？**
→ **DELTA 3 降复杂度**：首版只采集轻量 **Runtime Facts**（`queue_depth` / `waiting_since`·`oldest_wait` / `active_count` / `employee_availability`），直接产生 **Bottleneck Candidate**；不做 throughput 预测 / capacity score / 智能负载 / 企业级 scheduler。Bottleneck Candidate → CEO Assistant 白话建议 + 一键「增加员工」。后续再演化 throughput / 自适应 capacity / Team scheduling / load balancing。

**P14. 如何保持普通用户只理解 Office + Employee，而底层仍支持复杂组织？**
→ 首版界面仅暴露 Office / AI Employee / Connected Accounts / Current Work / Needs CEO；Org Router / Capacity / Queue / Team topology 全在后台。瓶颈由 CEO Assistant 白话汇报 + 一键建议，用户只做二选一。

**P15. Content Growth 最终推荐架构？**
→ **Business 级跨 Workspace 运营域（运行层八阶段闭环）**，组合 Office 单元 + Content Production WS + N 个 Channel Ops WS + Growth Intelligence。不新建顶层 primitive；若已有 Workspace Family 概念则为其自然承载。详见 G 节。

**P16. 当前 Content × Channel Contract 应如何修改？**
→ 在上一轮「Canonical Content → Channel Variant → Publication」契约之上**加两层**：
1. **Office 层契约**：Office 拥有 Account Pool + Growth Context；Target Accounts 前置生成 Account-aware Production Requirements。
2. **Intent 层契约**：Content Intent / Opportunity 为跨账号共享对象，Production 据 Account 动态 HIGH REUSE / DIVERGENCE。
3. **Variant 修正**：Channel Variant 增加 `channel_account_ref`（归属具体账号，可每账号多份以支持 DIVERGENCE）。
4. **Org 契约（新）**：Process→Responsibility Requirement→Org Routing→Holder→Executor→Employee/Team→Capability，作为运行层共享契约。

---

## CONTENT × CHANNEL MODEL DELTA（对上一轮 4 份文档的处置）

| 上一轮概念 / 文档 | 处置 | 说明 |
|---|---|---|
| **Content Production × Channel Operations 拆分本身** | **KEEP** | 两层拆分仍正确，现为 Content Growth 的下层支撑 |
| `Canonical Content` | **KEEP** | 仍为 Production 母版对象；明确其**不是**顶层共享对象（Intent 才是） |
| `Production Result` | **KEEP** | 仍为平台无关母版，服务 HIGH REUSE 场景 |
| `Channel Variant` | **MODIFY** | 增加 `channel_account_ref`（归属具体账号）；支持每账号多份（DIVERGENCE）；不再仅按 platform 枚举 |
| `Publication` | **KEEP** | 不变 |
| `Engagement` | **KEEP** | 明确归属 per-Account Publication（矩阵研究佐证 per-account 指标分离） |
| `Analytics` | **KEEP** | 不变，per-Account/per-Platform 真相源 |
| `Target Channels` | **MODIFY → Target Accounts** | 升级为 Distribution Targets，前置到 Intent 之后、Production 之前 |
| `Video Production Workspace` | **MODIFY → Content Production Workspace** | 泛化（不止 Video，含 Note/Image）；且它**不拥有 Office**，Office 在其上层 |
| `Channel Operations Workspace` | **MODIFY** | 明确其在 **Office 上下文 + 具体 Channel Account** 内运行（如「Office B 的 Douyin AI号 Ops」是一个实例），非纯 per-platform |
| `XHS Approved Instance` | **KEEP** | 当前不改；未来纳入更高层 = XHS Channel Ops 接受 Note+Video（见上一轮结论） |
| `Douyin Research（官方能力）` | **KEEP + REINTERPRET** | 事实保留；现定位为 **Douyin Channel Capabilities**，作用域收窄到具体 Channel Account；政策强结论仍 `POLICY VERIFICATION REQUIRED` |
| `AiToEarn Reference` | **KEEP** | 定位不变（Reference Implementation 为主） |
| 上一轮 Doc 1（Content Production × Channel Ops Model） | **KEEP + EXTEND** | 核心拆分保留；需补 Office / Channel Account / Content Intent / Org 路由层 |
| 上一轮 Doc 2（Canonical × Channel Variant 数据模型） | **KEEP + MODIFY** | 补 Content Intent/Opportunity 上游对象、Variant 加 `channel_account_ref`、每账号多 Variant |
| 上一轮 Doc 3（Multi-Channel Architecture Review） | **KEEP（G 平台差异）+ SUPERSEDE（7 问→16 问）** | 平台差异矩阵保留；7 问被本轮 16 问取代；处置节更新 |
| 上一轮 Doc 4（AiToEarn Review） | **KEEP** | 不变 |

**被新模型替代/升级的概念**：`Target Channels` → `Target Accounts`；`Video Production WS` → `Content Production WS`；`platform-only Variant` → `account-scoped multi-variant`；新增 `Office` / `Content Intent` / `Org Routing` 三层（上一轮缺）。

---

## DELTA 1/2/3 应用记录（本轮批准，APPLIED）

用户批准「总体方向 APPROVED WITH DELTAS」，仅修正 3 个架构 Delta，不再做外部研究：

- **DELTA 1 — Office 与 Organization 正交**：取消 `Company → Office → Employee/Team` 隶属表达；改为 Company 下 `Business/Operating Context → Office` 与 `Organization → (Department/Team/Role/Employee)` 两轴正交；Employee 经 Responsibility Assignment 服务 N Office（非隶属）；Channel Account 的 `office_id` 改为 OfficeAccountBinding / Account Pool 关系（见 Doc 2）。
- **DELTA 2 — Router 与 Team Lead 职责分离**：Router = 确定性低成本机械调度（eligibility/capability/availability/queue/capacity/auto-assignment）；Team Lead = 管理判断/异常（priority conflict/blocker/quality/acceptance/exception/standards/coaching/abnormal workload），仍是 Employee/Role，非新 primitive；避免每任务经额外 LLM Team Lead。
- **DELTA 3 — 首版 Capacity 降复杂度**：方向保留为 Company OS Shared Candidate；首版只采集 Runtime Facts（queue_depth/waiting_since/oldest_wait/active_count/employee_availability）→ Bottleneck Candidate；不建 throughput 预测/capacity score/智能负载/企业级 scheduler。

> 其余结论（Office=经营单元、Office 绑 N 账号、Channel≠Channel Account、Target Accounts 前置、Intent/Opportunity 跨账号共享、HIGH REUSE+DIVERGENCE、Variant account-scoped、Publication/Engagement/Analytics per-Account、Unified Feedback、Process/Org/Capability 分离、Shared Employee、用户简单性、AiToEarn=Reference、XHS 不改、Douyin 官方研究保留并重归类）均 **APPROVED 不变**。

---

## 纪律核对

- ❌ 未画 UI
- ❌ 未改 Product Blueprint / Frozen Shell / P1–P7
- ❌ 未改 XHS / RD Instance
- ❌ 未开发 Connector
- ❌ 未改 Runtime / Authority Map
- ✅ 仅产出 4 份 Reference Only 文档 + 同步 CURRENT_STATE（状态登记，非权威改写）

---

*CONTENT GROWTH × ORGANIZATION ARCHITECTURE REVIEW REQUIRED —— 待 Review 批准后，方可进入 Office / Intent / Org Routing Contract 设计与 Workspace 实例化。*
