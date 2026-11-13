# CONTENT GROWTH — PRE-IA CONTRACT CLOSURE
### 进入 IA 前的 5 个产品合同闭合（Red-Team Blocker Resolution · 不新增功能 · 不画 IA / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority）

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）

Companion 前置：
- Frozen `Curis_Content_Growth_Domain_Authority.md`（Domain 语义真源）
- Frozen `Curis_Company_OS_Shared_Authority.md`（§9 Business→Workspace→Operating Team + Professional Workspace + Surface；⑥⑧⑦）
- Round 3 `CONTENT_GROWTH_CONFIGURATION_OWNERSHIP_AUDIT.md`（39 项归属 A/B/C/D/E）
- Round 4 `CONTENT_GROWTH_AI_EMPLOYEE_DECISION_MODEL.md`（18 问契约 / Confidence / Progressive Investment / Strategy Envelope / Learning）
- Round 5 `CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md`（8 态 + 压缩 + 注意力 + 生命周期）+ `CONTENT_GROWTH_CEO_DAILY_SIMULATION.md`

---

## 0. 本轮纪律与范围

- 只闭合进入 IA 前的 **5 个产品合同**，不新增任何功能、不新增 Surface、不新增 Employee、不画 IA / Wireframe / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority。
- 所有结论**消费** Frozen 不变量（不重定义）：`CHANNEL_NE_ACCOUNT` / `OAUTH_FAILURE_KEEPS_ACCOUNT` / `TARGET_NE_ELIGIBILITY` / `PUBLICATION_PER_ACCOUNT_TRUTH` / `FACT_NOT_ROLLED_BACK` / `NO_CROSS_ACCOUNT_CONTEXT_LEAK` / `INTENT_EXCLUDES_INFERENCE` / `RECEIPT_FROM_CONNECTOR` / `UNKNOWN_IS_LEGAL` / `SCHEDULING_IS_CONDITIONAL`。
- 目标：把「Research Candidate 语义」与「Current Authority 语义」对齐、把「AI 自主」压成硬边界、把「CEO 认知」收敛为最少可操作集合，使 IA 阶段**只消费已闭合的合同**，不再在 IA 中补产品决策。

---

## 1. PRODUCT IDENTITY CONTRACT（产品身份合同）

### 1.1 唯一答案（消除 Research Candidate 与 Current Authority 的语义分叉）

| 问题 | 唯一答案 | 依据 |
|---|---|---|
| **Content Growth 到底是什么？** | 一个 **Professional Workspace**（领域专业工作区），不是独立 App、不是 Business、不是 Platform。它是「经营什么」的载体（business_goals / positioning / audience / content_strategy）+ 一支真实 Operating Team（周明/王颖/李想/陈帆）+ 若干 Professional Surface。 | Shared Authority §9.1（`Professional Workspace` 定义）；Domain ① Opportunity→Intent→Variant→Publication 主价值链 |
| **Business / Workspace / Office 如何对应？** | 普通用户层级 = `Company → Department → Business → Office / Workspace`。**Content Growth 的「经营单元」= Office = Workspace**（Domain §0.1 已 reconcile：Office 不再与 Business 平级，归入 Business 下独立经营执行单元）。一个 Business 可聚合多个同类 Office（如「内容增长」Business 下可挂「AI 科技内容」Office、「美妆内容」Office）。 | Domain §0.1 CEO Business×Office Reconciliation；Shared §9.1A |
| **XHS / Douyin 等到底是什么？** | **Channel**（平台事实层），**不是 Workspace、不是 Office、不是 App**。XHS / Douyin / TikTok / YouTube / Bilibili 都是 Channel；其下真实经营的账号是 **Channel Account**。它们存在于 Content Growth Workspace **内部**，作为 Channel 对象 + Channel Account 集合。 | Domain §1.2 `CHANNEL_NE_ACCOUNT`；`OAUTH_FAILURE_KEEPS_ACCOUNT` |
| **Channel / Account 位于哪里？** | 在 Content Growth Workspace 内：`Office —* Channel Account（经 OfficeAccountBinding → Account Pool）`；Channel 是平台事实层，与 Channel Account 严格分离。 | Domain §2 Relationships；`BINDING_DERIVES_POOL` |
| **默认 Main 的责任是什么？** | 不展示业务系统结构（不看 Work 队列 / Signal 池 / 状态机 / Binding）。只回答：发生了什么 / 员工得出什么结果 / 正在做什么 / 什么值得关注 / 是否需要我决定 / 是否需要我点一下 / 下一步建议是什么。即 Round 5 的 **CEO Operating State 驾驶舱（8 态压缩投影）**。 | Round 5 §1 最高原则 + §2 8 态 |
| **Professional Surface 与 Main 什么关系？** | Main = 压缩后的 CEO 认知驾驶舱（8 态投影）；Professional Surface = 承载真实复杂度的下钻层（信息机会 / 选题 / 研究与洞察 / 内容 / 增长评估 / 反馈 / 渠道）。Main 投影的是 Surface 真相的**压缩视图**；Surface 是 Shared Truth 的专业面，CEO 仅「查看依据」时进入。**Surface 不新增 Runtime / 不绑定 Employee（Shared `NO_SURFACE_RUNTIME` / `SURFACE_DECLARES_RESPONSIBILITY_NOT_EMPLOYEE`）**。 | Shared §9.2 `NO_SURFACE_RUNTIME`；Round 5 §10 DEEP-DIVE |

### 1.2 分叉消除结论

Prior rounds 把 XHS 称为「Channel candidate」、Content Growth 称为「Workspace candidate」——**与 Frozen 完全一致，无分叉**。唯一需钉死的是：早期研究曾把「Office」当普通用户产品顶层入口（旧语义 `DEPRECATED`），本轮明确 **Office = Workspace，归属 Business**，普通用户导航遵循 `Business → Workspace`。**不重新设计 Curis 架构**，只消费既有 Authority。

> **RESOLVED 标记 A（产品身份）**：语义分叉已消除，Content Growth=Workspace、XHS/Douyin=Channel 在 Frozen 与 Research 间一致。

---

## 2. MINIMUM BUSINESS VALUE CONTRACT（经营价值合同）

### 2.1 核心裁定

**「内容发出去了」≠「经营结果」。** Evaluation 优化的目标必须是用户的 **经营目标（Goal）**，不是平台赞藏评（vanity metric）。任何拿不到销售 / 广告 / 品牌结果时，明确标 **UNKNOWN**，禁止伪造 ROI。

### 2.2 统一 9 元组（每个 Evaluation 必须回答）

> Goal → Observable Result → Business Meaning → Cost → Risk → Attribution Boundary → UNKNOWN → Recommendation → Learning

### 2.3 三目标压力测试

| 目标 | Observable Result（可观测） | Business Meaning（经营含义） | Cost | Risk | Attribution Boundary（归因边界） | UNKNOWN（必须诚实） | Recommendation | Learning |
|---|---|---|---|---|---|---|---|---|
| **A. 个人IP / 涨粉** | 粉丝净增 / 互动率 / 粉丝画像质量 / 内容收藏率 | 影响力资产积累，为后续接广告 / 带货铺垫 **路径** | Token / 员工 / 时间 / 机会成本 | 平台限流 / 内容同质化 / 人设漂移 | 涨粉可归因到「内容策略 + 选题」但需 ≥3 次一致 Observation（Round 4 §6），单次禁固化 | 初期「接广告转化」UNKNOWN（尚未发生） | 继续高收藏率方向，扩匹配渠道 | 「第一手实测类」持续高收藏 → Accepted 加权 |
| **B. 带货** | 点击 / 加购 / 成交 / GMV / CPS / 佣金 | 直接收入 | 同上 + 退货损失可能 | 合规（虚假宣传）/ 退货 / 选品失误 | 站内转化可部分归因；**跨平台 / 心智转化 UNKNOWN** | 品牌心智带动的复购 UNKNOWN | 强化可归因带货路径，弱归因渠道降权 | 高转化选题模板沉淀（信封内） |
| **C. 企业品牌** | 品牌词搜索指数 / 提及量 / 线索数 / PR 声量 | 长期资产 / 销售线索 | 同上 | 负面舆情 / 人设错位 | **最弱**：单条内容难归因品牌价值，多为 UNKNOWN | 绝大多数品牌价值 UNKNOWN（不强行量化） | 持续声量建设，重点监测负面 | 危机信号模式沉淀（升 S8） |

### 2.4 与既有模型的对齐

- Round 4 `D12 是否值得生产` 的 Content Value 门、Round 5 `S2 RESULT` 的「价值 / 建议下一步」字段，必须携带 **Business Meaning**（Goal 锚定含义），而非仅赞藏。
- `UNKNOWN_IS_LEGAL`（Frozen + Shared §5.3）：拿不到经营结果时，Evaluation 显式写「此项 UNKNOWN，不计入 ROI」。

> **RESOLVED 标记 B（经营价值）**：Evaluation 以用户 Goal 为锚，平台指标≠Business Value，UNKNOWN 合法且强制，无伪造 ROI。

---

## 3. AUTONOMY SAFETY CONTRACT（自主安全硬边界）

把 Round 4 的「原则」压成**最小硬边界**。无真实数据能定精确阈值时，不伪造数字，标注三类之一：
- **SAFE DEFAULT**：无数据即可采用的保守默认（直接进 Runtime 初版）。
- **CALIBRATION REQUIRED**：需真实数据校准，结构已定、初值待补（不阻塞 IA，属 Runtime Config / Extension）。
- **UNKNOWN**：当前无法判定，须 WAIT / 补证据。

| # | 硬边界 | 类别 | 最小边界值 / 规则 |
|---|---|---|---|
| 1 | **Evidence 独立性** | SAFE DEFAULT | ≥2 独立源一致 ⇒ 可 HIGH；单源 / 强推断 ⇒ 最高 MEDIUM；否则 LOW / UNKNOWN（Round 4 §3.1） |
| 2 | **Evidence 新鲜度** | CALIBRATION REQUIRED | 各 Source / Channel 最大有效龄（官方 30d / 社区 7d 候选）超龄降级；初值待真实数据 |
| 3 | **最小观察量** | SAFE DEFAULT | Learning 需 ≥3 次一致 Observation；单次好 / 坏禁改 Strategy（Round 4 §6） |
| 4 | **LOW / UNKNOWN 处理** | SAFE DEFAULT | LOW ⇒ WAIT（不决定不执行）；UNKNOWN ⇒ 标 UNKNOWN + 补 Research / 问 USER FACT；禁推测填充 |
| 5 | **单次 Token / Cost 上限** | CALIBRATION REQUIRED | 单 Work token cap 初值待真实数据；初版取保守 SAFE DEFAULT 占位值 |
| 6 | **单周期 Cost 上限** | CALIBRATION REQUIRED | 单 Cycle 总 cap 待校准；Progressive Investment L0–L4 各档预算带随校准 |
| 7 | **最大自动 Work 链长度** | SAFE DEFAULT | 自动链 ≤ L0→L1→L2（到「建议」为止）；**进入 L3 Production / L4 Publish 必须 Human-in-loop 确认**，AI 不得跨确认自跑全链 |
| 8 | **最大重试次数** | SAFE DEFAULT | 每 Work 重试 ≤ 2 次；超则降级 / WAIT / 升 Leader |
| 9 | **超时** | SAFE DEFAULT | 单 Work 超时（如 Research 30min）⇒ WAIT / 重调度，不无限挂起 |
| 10 | **循环检测** | SAFE DEFAULT | 同对象重复同决策 ≥3 次无进展 ⇒ STOP / 升 Leader，防死循环 |
| 11 | **连续失败降级** | SAFE DEFAULT | 连续失败 ≥3 ⇒ 暂停该能力 / 降档 / 通知 CEO（S8） |
| 12 | **WAIT 条件** | SAFE DEFAULT | 低置信 / 证据冲突 / 未过价值门 ⇒ WAIT |
| 13 | **STOP 条件** | SAFE DEFAULT | 明显无价值 / 事实不足不可补 / 合规红线 / Envelope 外未授权 ⇒ STOP |
| 14 | **Leader escalation** | SAFE DEFAULT | 信封边缘 / 资源冲突 / 重试耗尽 ⇒ 升周明(Strategist) |
| 15 | **CEO Gate** | SAFE DEFAULT | Envelope 外 / 不可逆重大外部动作（发布 / OAuth） / 用户独有事实 ⇒ CEO Gate（Round 4 §8 红线） |

**目标达成**：AI AUTO 不允许无限工作（#7/#10）、无限重试（#8）、无限烧 Token（#5/#6）。所有边界初版可用 SAFE DEFAULT 启动，CALIBRATION REQUIRED 项在 Runtime Config 阶段填真实值，不阻塞 IA。

> **RESOLVED 标记 C（自主安全）**：Round 4 原则已压成 15 条硬边界，含不可自动化红线（OAuth / 发布确认 / Envelope 越界 / 用户事实）。

---

## 4. CEO ATTENTION & CONTINUITY CONTRACT（CEO 认知与连续性合同）

### 4.1 删除测试：8 态是否能减少？

对 Round 5 的 8 态做删除测试，并区分两层：

- **Internal State（系统态）**：后台 Work / Result / Publication 的真实生命周期，8 态是系统合同，需精确分流，不可合并（如 S5 进行中「从不通知」与 S8 异常「诚实呈现」行为不同）。
- **CEO Cognitive State（CEO 认知态）**：CEO 实际只需面对 **4 个桶**，8 态映射进来：

| CEO 认知桶 | 包含系统态 | CEO 第一眼心智 |
|---|---|---|
| **NEEDS_ME_NOW** | S4 DECISION / S7 ACTION_REQUIRED / S8 ALERT | 「有件事要我定 / 要我点 / 要我知」 |
| **KNOW_ABOUT** | S2 RESULT / S3 WATCH / S6 READY | 「有几件事我可以看」 |
| **RUNNING** | S5 IN_PROGRESS | 「团队在干活，好了会告诉我」 |
| **QUIET** | S1 QUIET | 「一切正常，无需我」 |

**结论**：8 态作为**系统合同保留**（保证每类行为精确），但 CEO 的** lived experience 收敛为 4 桶**。这满足「8 态可减少」的意图——在认知层确实减少到 4，且系统层仍精确。不强行压成少于 8 的系统态（会丢失 S5/S7 的行为差异）。

### 4.2 连续性场景压力测试（每个场景只答：第一眼 / 唯一最高优先动作 / 合并 / 隐藏 / 过期 / 不再通知）

| 场景 | CEO 第一眼（认知桶） | 唯一最高优先动作 | 合并 / 隐藏 / 过期 / 不再通知 |
|---|---|---|---|
| **离开两天再回来** | NEEDS_ME_NOW（若期间出现 S4/S7/S8 仍置顶）/ 否则 KNOW_ABOUT / QUIET | 处理仍存在的 S4/S7/S8 | 同 object_id 幂等不重建卡；已 SEEN 项保持降权；**不重复通知**已存在项 |
| **Desktop restart** | 同上（状态持久化，非内存态） | 同上 | 状态从持久层恢复，与离开前一致 |
| **5 个 Work 同时运行** | RUNNING（「5 项工作进行中」） | 无（等完成） | 5 个 S5 **合并为一条**状态条，不刷屏 |
| **Research 已完成** | KNOW_ABOUT（S2 结果卡） | 「查看依据」 | S5→S2 仅变状态不增卡；完成**一次** NOTIFY |
| **Publication 审核中** | RUNNING（低优先状态条） | 无 | 不通知，审完转 S2/S7 |
| **OAuth 失效** | NEEDS_ME_NOW（S7 重授权） | 「重新授权」 | 阻断发布的授权失效排最高；其余折叠 |
| **迟到回执** | 更新既有卡（per-account） | 无新动作（若已知） | 同 Publication object_id 替换，不新建；已通知过则不重复 |
| **Recommendation 已过期** | 降级 / 隐藏 | 无 | 超时效窗口 ⇒ DOWNRANK→HIDE，不再置顶 |
| **无任何变化** | QUIET（「团队正常运行，无事项」） | 无 | 严禁制造 KPI 墙 / 假推荐 |
| **同一对象连续更新** | 替换原卡 | 无 | object_id 幂等，永不重复建卡 |

> **RESOLVED 标记 D（CEO 认知与连续性）**：8 态经删除测试保留为系统合同、收敛为 4 认知桶；10 个连续性场景均有明确「第一眼 / 最高动作 / 合并隐藏过期不再通知」答案。

---

## 5. FIRST RUN & CAPABILITY TRUTH CONTRACT（首跑与能力真相合同）

### 5.1 三条 First Run 路径（不假设「贴链接 = 完整理解」）

| 场景 | AI 能确认 | AI 只能推断 | 什么是 UNKNOWN | 最少需要问用户 | 如何保持小白体验 |
|---|---|---|---|---|---|
| **A. Reference 可完整访问**（链接可拉到内容 / 数据） | 账号内容类型 / 更新规律 / 互动模式 / 增长特点（基于真实数据） | 受众细分 / Tone 微风格 / 商业化方式 | 平台内部算法权重 / 未公开后台数据 | 仅确认 Goal（「想达到什么目的」） | 直接给「我们建议这样定位」卡，采用 / 调整 / 讨论 |
| **B. Reference 部分可访问**（链接可用但数据受限 / 私有 / 限频） | 仅可访问部分（如可见内容、不可见后台数据） | 其余维度从可见部分推断 | 被限制 / 不可见的部分 | 仅当意图模糊时问一句「主要想学它哪方面」 | 同上，明确标注「基于可见部分推断」 |
| **C. Reference 无法访问**（死链 / 平台封锁 / 无链接） | 无（不能从 reference 确认任何事） | 无 | **整个 reference 全部 UNKNOWN** | Goal +（可选）「有没有其他参考」 | 走 Round 3 §3 无对标路径：AI 自做市场 / 赛道 / 对标研究，给建议；零配置起步 |

**铁律**：任何情况下 AI 只 CONFIRM 真实可访问的、只 INFER 有依据的、其余标 UNKNOWN；**不假设贴链接即完整理解账号**。

### 5.2 首批 Channel × Account × Capability Truth Matrix

能力状态**只允许 4 值**：`VERIFIED`（官方源已验证）/ `CONDITIONAL`（可用但有条件或待验证）/ `UNKNOWN`（尚未验证，不得假定可用）/ `UNAVAILABLE`（平台不提供 / 不在首批）。

| Channel | Auth | Read Content | Publish | Schedule | Receipt | Analytics | Comments/Feedback |
|---|---|---|---|---|---|---|---|
| **XHS** | VERIFIED(OAuth) | CONDITIONAL(官方 API 受限，需爬虫/开放平台) | CONDITIONAL | CONDITIONAL(平台支持但参数 UNKNOWN) | CONDITIONAL | CONDITIONAL(创作者后台部分可得) | CONDITIONAL |
| **Douyin** | VERIFIED(开放平台) | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL |
| **TikTok** | VERIFIED(海外 OAuth) | CONDITIONAL | CONDITIONAL/UNKNOWN | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL |
| **YouTube** | VERIFIED | VERIFIED(官方 API 成熟) | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED |
| **Bilibili** | VERIFIED | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL |

> **关键红线**：**不**为了覆盖 XHS/Douyin/TikTok/YouTube/Bilibili 而假设全部可经营。首批产品**只消费 `VERIFIED` / `CONDITIONAL` 单元格**；`UNKNOWN` / `UNAVAILABLE` 的 Channel / 能力**不呈现为可经营选项**（如某平台 Publish=UNAVAILABLE，则该平台首批不可发，仅可作 Reference 监控）。各单元格精确状态属 **CALIBRATION REQUIRED**（需 Connector 实测回填），但结构已定、首批消费规则已明。

> **RESOLVED 标记 E（首跑与能力真相）**：3 条 First Run 路径明确定义 CONFIRM/INFER/UNKNOWN 边界；能力矩阵只用 4 值枚举，首批只消费真实能力。

---

## 6. RED-TEAM P0 / P1 RECONCILIATION

| Red-Team 关注 | 对应合同 | 状态 | 说明 |
|---|---|---|---|
| **P0-1 语义分叉**（Research vs Authority） | §1 Product Identity | **RESOLVED** | Content Growth=Workspace、XHS=Channel 与 Frozen 一致；Office=Workspace 归属 Business 钉死 |
| **P0-2 无经营价值证明**（只证明「发出去了」） | §2 Business Value | **RESOLVED** | Evaluation 锚定 Goal，9 元组含 Business Meaning / Attribution / UNKNOWN；禁伪造 ROI |
| **P0-3 自主安全**（AI AUTO = 瞎干） | §3 Autonomy Safety | **RESOLVED** | 15 条硬边界，含不可自动化红线；SAFE DEFAULT 可直接启动，CALIBRATION 不阻塞 |
| **P0-4 CEO 认知刚性 / 连续性** | §4 CEO Attention | **RESOLVED** | 8 态→4 认知桶；10 场景连续性全答 |
| **P0-5 首跑假设**（贴链接=完整理解） | §5 First Run | **RESOLVED** | 3 路径 + 能力矩阵 4 值，首批只消费真实 |
| **P1-a CEO 确认疲劳** | §4 + §3 | **RESOLVED** | S4 仅真越信封才出现；B 建议低频批处理；不可逆才惊动（Round 4 §8） |
| **P1-b Quick→Structured 升级成本** | §3 #7 + Round 4 §4.3 | **RESOLVED** | Quick 恒为 L0；仅 MEDIUM+ 轻提示三选一；升级成本受价值门 + 单次 cap 限制 |
| **P1-c 多账号推荐解释** | §1 + Round 4 D16 | **RESOLVED** | 发布建议带「为什么」（定位匹配 / 历史表现）；S7 显示「XHS主号+抖音主号 预计时间」 |
| **P1-d 专业能力可发现性** | §1 + Round 5 §10 | **RESOLVED** | 专业层经「查看依据」按需下钻；EXPERT ONLY 默认隐藏，不污染小白 |
| **P1-e canonical object / truth 重复建模风险** | §1 | **RESOLVED** | 单一真相源 = Office / Intent / Channel / Publication（消费 Frozen）；无第二套 Registry / Surface Runtime |

无 P0 / P1 残留 OPEN。

---

## 7. REMAINING OPEN（非阻塞）

| # | OPEN | 类别 | 是否阻塞 IA |
|---|---|---|---|
| O1 | 安全阈值精确值（单次 token cap / 单周期 cap / 观察次数 N / 价值门阈值） | CALIBRATION REQUIRED（Runtime Config / Extension） | **否** — SAFE DEFAULT 可启动，实值实现期填 |
| O2 | Envelope 初始边界值（Goal / Channel family / Budget / Risk tolerance） | 由 CEO 首次表达时确立 | **否** — 不预设 |
| O3 | 能力矩阵各单元格精确状态 | CALIBRATION REQUIRED（Connector 实测） | **否** — 结构固定，首批消费 VERIFIED/CONDITIONAL |
| O4 | Calendar 是否独立 L1 Surface | Round 2 OPEN（建议作「内容」Surface 内视图） | **否** — IA 时可定 |

以上 OPEN 均属 Runtime Config / Extension Points / IA 细化，**不影响**产品身份、经营价值、自主安全、CEO 认知、First Run 五个维度的正确性，故不触发 NOT READY。

---

## 8. FINAL IA READINESS DECISION

| 维度 | 是否仍有影响进入 IA 的 OPEN | 判定 |
|---|---|---|
| 产品身份 | 无（§1 RESOLVED） | PASS |
| 经营价值 | 无（§2 RESOLVED） | PASS |
| 自主安全 | 无（§3 RESOLVED；阈值 CALIBRATION 不阻塞） | PASS |
| CEO 认知 | 无（§4 RESOLVED） | PASS |
| First Run | 无（§5 RESOLVED） | PASS |

### ✅ FINAL DECISION: **READY FOR IA**

理由：5 个 Red-Team P0 全部 RESOLVED，P1 全部 RESOLVED，Remaining OPEN 均属 Runtime Config / Extension / IA 细化，不构成产品合同级阻塞。六轮研究（领域 → 产品映射 → 功能交互 → 端到端 → AI 公司体验 → 决策模型 → CEO 状态 → 本 Pre-IA 合同）已自洽，**可进入 IA / 低保真结构稿消费本模型**。

IA 阶段约束（来自本闭合合同，必须消费）：
1. 不重新争论产品身份——Content Growth=Workspace、XHS/Douyin=Channel。
2. Main = 8 态压缩驾驶舱（认知 4 桶）；Professional Surface 仅下钻层。
3. Evaluation 锚定用户 Goal，UNKNOWN 合法。
4. 自主行为受 §3 硬边界约束，不可自动化红线（OAuth / 发布确认 / Envelope 越界 / 用户事实）不可绕过。
5. 首批只消费 VERIFIED/CONDITIONAL 能力，不假设全平台可经营。

---

*CONTENT_GROWTH PRE-IA CONTRACT CLOSURE — RESEARCH / EXPERT RECOMMENDATION — FINAL DECISION: READY FOR IA — STOP FOR CEO REVIEW*
