# Curis Content Growth Domain Authority

Status: **Frozen**

Updated: 2026-09-15

Authority Class: CURRENT / FROZEN DOMAIN PRODUCT AUTHORITY
Disposition: CEO ACCEPTED RECONCILIATION CONSUMED — CONSOLIDATION REVIEW REQUIRED；不是实现验收。§5.4为账号经营与Provider正式合同。

Scope: Content Growth 业务域语义（适用 Content Growth Professional Workspace Candidate / Channel 与多账号扩展；Office 仅保留历史与迁移 provenance）

Authority level: **Domain Authority** —— 高于 Instance Spec，低于 Company OS Shared Authority；只可消费 Company OS Shared（⑥⑧⑦），不可重定义。

---

## 0. 本文件的性质与边界

- 本文件只保留 **Definitions / Relationships / Invariants / Ownership / Truth Boundaries / Cross-domain Rules / Extension Points**。
- **Examples / CASE 验证 / Delta 推理史 / 字段候选 / 平台调查**不在此处，保留于对应 Contract Candidate 与 Consolidation Review（Reference / Design Record）。
- 本文件**不修改** Product Blueprint、Frozen P1–P7 原文、XHS Instance、RD Instance、Runtime、Connector、代码、UI。
- 与 Company OS Shared Authority（⑥⑧⑦ + Context Isolation）的关系：**CONSUMES（消费，不修改）**；与 Frozen P1–P7：**EXTENDS（扩展，不修改）**。
- 与两份 Authority Consolidation Review 的关系：本文件为 Review 批准后的 **Frozen 落定**；Review 留作 Review Record / Reference（见 §8）。

### Activation / Publication boundary（CEO Accepted 2026-09-15）

消费[Company OS Shared §19](Curis_Company_OS_Shared_Authority.md)。Content Growth是首个完整推导的专业Business Capability实例，仍Professional Workspace Candidate；本Patch不授予Publishing Gate通过、Verified或可启用资格。正式发布版本/范围才可进入Catalog“启用内容增长”；未启用定义不是用户Business。Channel/Channel Account≠Workspace，账号经营合同不变。

### 0.1 CEO Content Growth identity reconciliation（2026-08-24）

CEO 已确认当前产品层级为：`Company → Department → Business → Workspace`。`Workspace` 是唯一 canonical user/product identity；Content Growth 是 Professional Workspace Candidate，不是 Verified Professional Workspace。

`Office` 退出当前用户产品语义，仅保留历史 / implementation / migration provenance。本轮不迁移 `company_id`、`office_id`、`OfficeAccountBinding` 或 Schema；这些名称继续作为旧 Domain / Runtime 证据读取，不得被解释为 `Office = Workspace`。

XHS / Douyin / TikTok / YouTube / Bilibili 等是 **Channel**，具体账号是 **Channel Account**；`Channel ≠ Workspace` 且 `Channel ≠ Channel Account`。保持 Shared Main Contract 不变；Content Growth 的 CEO Operating Result / 经营结果面是 Domain-scoped default selected Professional Surface / projection，不是新的全局 Main 或第二套 Truth。

---

## 1. Definitions（Frozen）

### 1.1 Workspace（Content Growth 独立经营环境；旧 Office 仅为 provenance）

「**经营什么**」的载体 = 一套共同的 business_goals / positioning / audience / content_strategy / knowledge_refs / growth_context / account_pool。

- **产品身份遵循 `Company → Department → Business → Workspace`**；Workspace 承载独立目标、策略、工作现场、员工服务关系、能力、账号对象、发布与回执事实。
- 旧 Domain identity 的 `company_id` / `office_id` 直连与 `OfficeAccountBinding` 仅是 implementation / migration provenance，不是当前用户产品层级。
- **≠ Platform / Channel / Channel Account / Content Type / Department / Team**。Workspace 与 Organization 树的关系由 Shared Authority 解释。
- Operating Context 为 **RESERVED / DEFERRED CANDIDATE**，本轮不固化；未来若需上层容器，优先对齐 Blueprint 的 Business / 业务空间概念。

### 1.2 Channel / Channel Account / legacy OfficeAccountBinding / Account Pool

- **Channel**（平台事实层）：平台本身。只引用 **VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE** 能力；不将第三方 SaaS 能力写成 Channel 原生能力。
- **Channel Account**（账号经营层）：用户在该平台实际经营的账号（`positioning` / `tone_style` 等每账号属性）。OAuth 失效 → 账号与历史保留、当前执行降级、不删除账号。
- **OfficeAccountBinding**：历史 Runtime / migration relation 名称；其持久化语义暂不迁移。本产品层只表达 Workspace 与 Channel Account 的绑定关系（允许同一Workspace经营多个合法绑定账号；结构支持N:N，不因账号数量自动创建Workspace）。
- **Account Pool**（派生集合，非必存实体）：某 Workspace 下所有 `binding_state=ACTIVE` 的绑定所指向 Channel Account 全集；是 Target Account Set 的候选来源。

### 1.3 Content Opportunity / Content Intent

- **Content Opportunity**（信号）：来自 Growth Intelligence 的「什么值得做」候选（`source` / `topic` / `score`），不绑定具体账号/平台。
- **Content Intent**（共享上游对象）：「准备讲什么 / 为什么做 / 服务什么目标」（topic / core_message / business_goal）。表达 WHY / WHAT / GOAL，**不表达**最终资产形态。
  - **禁存**：AI 推理过程 / Prompt / Chain-of-Thought / 中间草稿 / 工具调用日志（属运行期执行，不进 Intent）。
  - **弱服务关系**：Intent 可服务多个 Workspace，不被单一 Workspace 拥有。

### 1.4 Target Account Set / Distribution Targets

某一次**内容实例**所针对的**具体账号子集**（账号粒度，非 Platform）。

- **Effective Target Account Set** = Workspace Default Set + AI Recommendation + Manual Override 三者合并裁决。
- **Target ≠ Eligibility**：Target 表达「业务/用户想发哪里」；Eligibility（能不能发）运行期派生，账号失效时仍是 Target 仅 BLOCKED，禁静默删除。
- **Distribution Execution Policy**（BEST_EFFORT / ALL_REQUIRED）：定义于本契约 ④，**唯一定义方**；⑤ 只读取服从（DELTA C1）。

### 1.5 Content Variant / Publication

- **Content Variant**（账号级变体）：一个 Intent 在**某具体 Channel Account** 上的适配产物，绑定且仅绑定一个账号。`reuse_mode` = HIGH_REUSE（轻量 metadata 适配）/ FULL_DIVERGENCE（完全重产）。
- **Publication**（per-Account 真相源）：某 Variant 在某 Channel Account 上的一次发布事件/记录，是该账号状态/回执/时间**唯一真相源**。真实发布执行与回执由 Capability·Connector 承担，本契约只引用 `publish_receipt`。

---

## 2. Relationships（Frozen）

```
Company → Department → Business → Workspace（canonical产品层级）
Company → Channel Account（公司资产；经合法绑定服务Workspace）

Workspace
  ├─ *—* Channel Account（经 legacy OfficeAccountBinding / binding provenance → Account Pool 派生）
  ├─ 1—1 default_target_account_set（引用 Account Pool 子集）
  └─ *—* Content Intent（弱服务链接）

Channel 1—* Channel Account（平台事实层 ⊥ 账号经营层）

Content Opportunity → Content Intent（转化）
  └─ *—1 Target Account Set（账号粒度选择，三源合并裁决）
        └─ *—1 Content Variant（每选中账号一份，绑单一账号）
              └─ 1—* Publication（per-Account 真相源）

Domain 消费 Company OS Shared：
  Process → Responsibility Requirement（⑥ · WHAT）
         → Organization Routing（⑦ · WHO）
         → Employee（⑧ · 执行，∈ Organization，经 Service 服务 Workspace）
```

- **经营闭环**：Account Goal/Strategy → Plan → Intent/Variant → Publication/External Reality → Analytics/Review → accepted Learning → Next；生产发布是其中一段，不替代长期经营。
- Domain 不自行分派 WHO；WHO 由 ⑦ 解析（见 Company OS Shared Authority §5.2）。

---

## 3. Invariants（Frozen · 硬约束）

| ID | 约束 |
|---|---|
| `OFFICE_UNDER_COMPANY_AND_NOT_ORG` | **Implementation / migration provenance only:** 旧 Office `company_id` / `office_id` 仍可直挂 Company，Office ≠ Department / Team；这不定义当前用户产品层级。产品阅读只遵循 Business 内 Workspace，未来迁移须另立 Runtime / Schema Delta。 |
| `CHANNEL_NE_ACCOUNT` | Channel（平台事实层）与 Channel Account（账号经营层）严格分离；一 Channel 可含 N 个定位不同的 Account。 |
| `BINDING_DERIVES_POOL` | Account Pool 由 Active OfficeAccountBinding 派生；Binding 不授予 Organization 成员资格。 |
| `OAUTH_FAILURE_KEEPS_ACCOUNT` | Channel Account OAuth 失效 → 账号保留、`authorization_state` 降级、历史 Publication 保留、当前执行降级；不删除账号、不删除历史。 |
| `INTENT_EXCLUDES_INFERENCE` | Intent 禁存推理 / Prompt / CoT / 中间草稿；只承载 WHY / WHAT / GOAL 结论性业务语义。 |
| `INTENT_SHARED_UPSTREAM` | Intent 为跨账号共享上游对象；单 Intent 可产 N 账号级变体（HIGH REUSE + FULL_DIVERGENCE 并存）。 |
| `TARGET_IS_ACCOUNT_NOT_PLATFORM` | Target 粒度是账号；绑 N 账号 ≠ 每条内容群发所有账号（每次仅选子集）。 |
| `TARGET_NE_ELIGIBILITY` | Target（想发哪里）与 Eligibility（能不能发）分离；账号失效仍是 Target 仅 BLOCKED，禁静默从 Target 删除。 |
| `DISTRIBUTION_POLICY_IS_UNIQUE_SOURCE` | `distribution_execution_policy`（BEST_EFFORT / ALL_REQUIRED）**唯一定义于 ④**；Workspace 有默认、任务可覆盖。 |
| `PUBLICATION_PER_ACCOUNT_TRUTH` | Publication 状态 / 回执 / 时间逐账号独立记录；无跨账号「整体发布状态」概念。 |
| `FACT_NOT_ROLLED_BACK` | 已发生的 Publication 事实（某账号 PUBLISHED / FAILED）**不得篡改、不得回滚**其他账号。 |
| `FUTURE_EXECUTION_GOVERNED_BY_POLICY` | 某账号不可执行后，**尚未执行**部分是否继续，读 ④ `distribution_execution_policy`（BEST_EFFORT / ALL_REQUIRED），禁把「不回滚」误读为「无条件继续」。 |
| `PUBLICATION_OBEYS_POLICY_NOT_REDEFINE` | ⑤ **不重定义**第二套分发/中止策略；只读取并服从 ④ Policy。 |
| `RECEIPT_FROM_CONNECTOR` | `publish_receipt` 由 Capability·Connector 回填；本契约不生成、不伪造发布证据。 |
| `SCHEDULING_IS_CONDITIONAL` | `scheduled_at` 仅在该平台官方支持时有效；不支持平台置空 / 标记不支持，POLICY VERIFICATION REQUIRED，不写死强规则。 |
| `NO_CROSS_ACCOUNT_CONTEXT_LEAK` | 为 Account A 生产的 Variant **不得**携带 Account B 的 tone_style / 策略 / Knowledge（上下文隔离，链接 ⑧ §5.1）。 |

---

## 4. Ownership（Frozen）

| 对象 | 归属 |
|---|---|
| Workspace | Business 内的独立经营层；唯一产品身份，非 Channel / Channel Account |
| Channel / Channel Account | Company 资产（经 Binding 服务 Workspace，不属于 Channel） |
| Content Opportunity / Intent | Company 级 Growth Context（共享，不被 Workspace 独占） |
| Target Account Set | 一次内容实例（由 Intent + Workspace 派生） |
| Content Variant | Content Growth 业务层（per-Account） |
| Publication（记录） | Content Growth 记录层（per-Account 真相） |
| Publication（执行 + 回执） | Capability·Connector（仅引用，不定义） |
| Distribution Execution Policy 语义与默认 | 本契约 ④（唯一源） |

---

## 5. Truth Boundaries（Frozen）

### 5.1 Capability Truth（跨域候选，本轮在 Domain 引用）

Channel 只引用 `VERIFIED` / `CONDITIONAL` / `UNKNOWN` / `UNAVAILABLE` 能力状态。

- `UNKNOWN` = 尚未以官方源验证，**不得**假定可用（如抖音官方 API 定时发布参数）。
- 不将第三方 SaaS 能力写成 Channel 原生能力。
- 2026-09-15：跨业务能力真实性原则已由Company OS Shared §10/12–13正式承载；此处保留Channel专属状态与映射，不新增全局enum。

### 5.2 Distribution Execution Policy 唯一真相源

`distribution_execution_policy`（BEST_EFFORT / ALL_REQUIRED）**唯一定义于 ④**。

- ⑤ Publication **只读服从**，不承担策略定义权（DELTA C1）。
- 事实一致性（已发生不回滚）与后续执行策略（未执行是否继续）**严格分离**。

### 5.3 UNKNOWN 是合法事实状态

在本 Domain 覆盖范围内，事实不足时使用 UNKNOWN 是**合法且必须**的表达，**禁止**以推测填充（能力核实 / scheduling 支持度 / 账号 eligibility 均适用）。

---


## 5.4 Account Operating / Provider Boundary（CEO Accepted 2026-09-15 · Frozen）

Account正式作为已有Channel Account的**长期经营对象**，产品关系覆盖Goal、Strategy、Cadence、Plan、Content history、Result、Analytics、Learning与Next cycle；不是新Account系统、Workspace或第五execution scope。账号目标/定位与策略在Business方向及Workspace合法经营边界内形成。

Business → Platform Strategy → Account Strategy → Account Operating Cycle 是Domain经营视角，不取代Company → Department → Business → Workspace。Account Operating Cycle表达账号计划/执行/观察/Review/学习/下一步，映射已有Work/Operating Cycle/Assignment；不得为多账号创建第二控制Runtime或违反one-active Workspace Cycle。

Content Intent → Platform Form → Account Context → Variant：Platform Form是规格/生产约束，不要求新canonical实体。Intent保留共同目标与核心信息；Variant引用账号定位/语气/受众、平台形态与输入版本，绑定具体账号；只共享合法上游资产，禁止无授权复制另一账号私有Context。

发布与分析责任均由Curis canonical Employee承担；Provider只提供已验证的提交、发布、回执、数据读取等能力。Publishing/Analytics不是固定人数/新员工类型，人员由原责任分配解析。数据自动采集是系统活动，不替代Analyst的口径判断、Review和Decision support。

|经营环节|必备产品事实 / 行为|失败与恢复|
|---|---|---|
|Account目标与策略|合法Company/Workspace binding、Goal/Strategy/受众/节奏、负责Assignment、能力/授权、范围与时间|缺事实先研究/提案；CEO只处理不能代理的边界，普通战术按Approved Envelope|
|Plan / Production|当前计划、Intent、平台形态、Account Context、Variant版本与结果合同|能力不够可人工辅助或Cannot operate yet，不假成品|
|Publish|逐账号Target/Eligibility、动作/输入版本、Approval范围、计划时间与真实提交/发布时间、Provider ref/receipt|部分成功保各账号事实；BEST_EFFORT/ALL_REQUIRED只治理尚未执行部分，不假跨账号事务/回滚|
|External Effect|effect confirmed / effect unknown / verification required / safe retry / cannot replay|消费Shared §15；超时先核验，不换Provider或人工重发制造重复|
|Analytics / Review|metric/unit/definition、source、observation window、collectedAt、freshness、验证/人工标记、Evidence与Recommendation|真实0、Unknown、Not Collected、Unsupported、Connection Failed、Stale分开；缺值不可补0；同口径才比较|
|Learning / Next|经授权Review接受的学习、适用范围、下一Work/计划或既有Cycle决定|AI摘要不直接改永久方法；收入/转化/增长无外部证据不宣称成立|

平台原生scheduled_at仍仅在真实支持时可用；本地计划时间/nextCheckAt是独立语义，不能伪装平台定时。错过排程先重查权限/目标/时效/效果，不自动补发。授权失效保留账号与历史，不自动删除Target。

人工登录/MFA/手机确认/现实动作消费[Company OS Shared §11](Curis_Company_OS_Shared_Authority.md)：解释下一步与回程，仍属原Work；人工报告不伪装平台receipt。发布责任仍在Curis，不转给Provider。

**AiToEarn = Social Platform Execution Provider Candidate**，仅在实施选型/来源审计时引用；不是Blueprint依赖、唯一底座或当前已集成能力。任何平台支持、Analytics、Engagement与变现能力必须逐连接/账号核验；不承诺统一收入、钱包或保证收益。8 Operating States / 4 Cognitive Buckets仍Research / Accepted Candidate，不成为Runtime Schema或固定UI合同。

**TARGET PRODUCT:** 本节账号经营及Shared能力合同已接受。**CURRENT IMPLEMENTATION:** 以CURRENT_STATE与对应验收为准；G1-V～G6-V NOT RUN、外部发布/数据接通不因本节冻结而变Verified。Domain默认CEO Operating Result / 经营结果面仍是selected Professional Surface projection，不是新的全局Main。

## 6. Cross-domain Rules（Frozen）

1. Domain（Content Growth）**消费** Company OS Shared Authority（⑥⑧⑦ + Context Isolation），**不得重定义** Responsibility / Routing / Employee 服务关系 / Context Isolation 语义。
2. Domain 可提供领域约束（如 Channel 事实层、Publication per-Account 真相），**不得**改变 Company OS Shared 任何 Invariant。
3. Content Growth专业实例（含XHS Channel场景）消费本Domain，不得重定义；RD消费其自身Domain/Instance与Shared，不能被内容经营规则覆盖。历史单Workspace·单账号只是合法退化形态；旧Office仅implementation/migration provenance，平台名不作为Workspace identity。
4. 任何与本 Authority 冲突的 Domain / Instance / Review 文档，以本 Authority 为准，并须建立修正记录。

---

## 7. Extension Points（**不 Frozen**）

以下属 Capability Registry / Channel Facts / Runtime Config / Shared Extension，**明确不在本 Domain Authority 冻结范围**：

| 扩展点 | 归属 |
|---|---|
| 具体平台 API（Douyin / XHS / Bilibili / YouTube 接口形态） | Capability Registry / Connector |
| 具体 OAuth Scope（各平台授权范围） | Capability Registry / Connector |
| 具体 scheduling 能力（哪些平台支持定时发布） | Capability Truth 枚举（UNKNOWN 合法） |
| 具体 ratio（复用/发散比例常量） | Channel Facts / Runtime Config |
| 具体 duration（scheduling 时长） | Channel Facts / Runtime Config |
| Routing 算法 / 权重 / 评分 / LLM 实现 | Company OS Shared Extension（未来 Runtime Policy） |
| `responsibility_type` 领域词汇表 | Company OS Shared Extension |
| Channel-specific能力事实/实施映射 | Domain事实；跨业务能力原则消费Company OS Shared §10/12–13 |

> Extension Points 的演化**不得**违反 §3 Invariants 与 §5 Truth Boundaries。

---

## 8. Reference / Design Record（非 Authority）

以下文档保留为 Reference，**不得**作为 Authority 引用，也**不得**删除或覆盖：

- `Curis_Operating_Context_Office_Contract_Candidate.md`（①）
- `Curis_Channel_Account_Contract_Candidate.md`（②）
- `Curis_Content_Intent_Contract_Candidate.md`（③）
- `Curis_Target_Account_Contract_Candidate.md`（④）
- `Curis_Content_Variant_Publication_Contract_Candidate.md`（⑤，已应用 DELTA C1）
- `BATCH_A_CONTRACT_REVIEW.md` / `Curis_BATCH_B_CONTRACT_REVIEW.md` / `Curis_BATCH_C_CONTRACT_REVIEW.md`
- `Curis_Content_Growth_Domain_Authority_Consolidation_Review.md`（Review Record）

用途：CASE 场景（B1–B6 / C1–C7）· Delta 历史（A1/A2/A3、B1、C1/C2）· 设计理由 · 字段候选 · 平台调查笔记 · 后续演化依据。

---

*CONTENT GROWTH DOMAIN AUTHORITY — FROZEN*
