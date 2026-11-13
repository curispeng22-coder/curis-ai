# CONTENT GROWTH — AI EMPLOYEE AUTONOMOUS OPERATING DECISION MODEL
### 配置经营权移交后，AI 员工凭什么判断、如何避免「AI AUTO = AI 瞎干」（不新增功能 · 不画 UI · 不实现）

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）

Companion: `CONTENT_GROWTH_AUTONOMOUS_OPERATING_CASE.md`（用真实 CEO 三句话证明本模型每一步可落到 Evidence / Decision Rule / Cost-Value / Confidence / Boundary）
前置：Round 3 `CONTENT_GROWTH_CONFIGURATION_OWNERSHIP_AUDIT.md`（39 项归属 A/B/C/D/E）+ `CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md`（三句话责任原则）；Round 2 全部 5 份；Frozen `Curis_Content_Growth_Domain_Authority.md`。

---

## 0. 本轮纪律与范围

- **只研究决策责任制**，不新增任何功能、不画 IA / Wireframe / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority。
- 消费 Frozen 不变量（不重定义）：`OAUTH_FAILURE_KEEPS_ACCOUNT` / `TARGET_NE_ELIGIBILITY` / `PUBLICATION_PER_ACCOUNT_TRUTH` / `FACT_NOT_ROLLED_BACK` / `NO_CROSS_ACCOUNT_CONTEXT_LEAK` / `INTENT_EXCLUDES_INFERENCE` / `RECEIPT_FROM_CONNECTOR` / `UNKNOWN_IS_LEGAL`。
- 团队与对象沿用 Round 2：`王颖(Research&Intel)`、`李想(Producer)`、`陈帆(Channel Operator)`、`周明(Strategist)`；Office / Intent / Source / Signal / Opportunity / Topic / Research / Brief / Draft / Asset / Variant / Publication / Channel / Channel Account。
- **核心命题**：Round 3 已把配置/经营责任从 CEO 移交给 AI 员工（大量 A / B / E）。本轮回答：**当 AI 员工自主决策时，凭什么判断，如何避免「有答案就干」**。

---

## 1. 问题框架：AI AUTO ≠ AI 瞎干

错误认知：「既然归属 AI（A），AI 就直接执行。」
正确认知：归属 AI 只意味着**责任在 AI**，不等于**无判断地执行**。每一项 AI AUTO / AI RECOMMEND 行为都必须可审计地回答一套统一问题，否则就是瞎干。

统一机制三件套：
1. **决策契约（18 问）**——每项决策都必须能逐条回答（见 §2）。
2. **Confidence 闸门**——不是「有答案」就能执行，答案必须达到对应动作允许的置信门槛（见 §3）。
3. **Envelope + Progressive Investment + Learning**——约束自主的边界、成本与演化（见 §4–§6）。

---

## 2. 决策契约（18 问统一模板）

> 适用于**所有** AI AUTO / AI RECOMMEND 行为。任何一项说不清下列任一条，即判定为「瞎干」，须降级为建议或 WAIT。

| # | 问题 | 含义（落地要求） |
|---|---|---|
| 1 | **谁负责** | 哪个 Responsibility / 哪个 Employee 对该决策有 ownership（链接 Frozen ⑥ WHAT / ⑦ WHO） |
| 2 | **目标是什么** | 这个决策服务的业务目标（涨粉/接广告/内容质量/合规…），不是「完成任务」 |
| 3 | **输入是什么** | 决策依赖的输入（Intent / Reference / Existing Assets / Evidence / CEO Constraint） |
| 4 | **Evidence 是什么** | 支撑判断的**事实**来源与强度（多源/单源/推断/UNKNOWN），不得用「常识」冒充 Evidence |
| 5 | **判断标准是什么** | 可复核的判定规则（评分维度、阈值、比对基准） |
| 6 | **有哪些候选方案** | 至少列出 2 个可行候选，含「不做/WAIT」选项 |
| 7 | **为什么选择这个** | 候选间的取舍依据，可追溯到 Evidence + 标准 |
| 8 | **Confidence 如何判断** | 该结论的置信度（HIGH/MEDIUM/LOW/UNKNOWN）及其判定依据（见 §3） |
| 9 | **Cost / Expected Value 如何考虑** | 该决策的边际成本（Token/员工/时间/外部风险）vs 期望价值，是否过价值门（见 §4） |
| 10 | **什么情况下可以自己执行** | 自执行（AUTO）的触发条件（高置信+可逆+Envelope 内+过价值门） |
| 11 | **什么情况下只能建议** | 建议（B）的触发条件（中置信/不可逆外部动作/Envelope 边缘） |
| 12 | **什么情况下必须 WAIT** | WAIT 条件（低置信/证据冲突/需补 Evidence/未过价值门） |
| 13 | **什么情况下 STOP** | STOP 条件（明显无价值/事实不足且不可补/合规红线/Envelope 外未授权） |
| 14 | **什么情况下升级 Leader** | 升级周明（Strategist）的条件（跨决策协同/信封边缘/资源冲突） |
| 15 | **什么情况下必须找 CEO** | 找 CEO Gate 的条件（Strategy Envelope 越界/不可逆重大外部动作/用户独有事实） |
| 16 | **做完以后如何 Evaluation** | 如何衡量该决策结果（指标/复盘时点） |
| 17 | **判断错了如何纠正** | 纠正路径（自动回滚/降级/用户一句纠偏/重做） |
| 18 | **什么可以进入 Learning** | 哪些经验可沉淀为可复用判断（见 §6，单次好/坏不直接改 Strategy） |

---

## 3. Confidence 模型（区分「有答案」与「可执行」）

**核心规则：AI 不能因为「有答案」就执行。** 有答案 ≠ 答案可信 ≠ 可自主执行。

### 3.1 四档定义与允许动作

| 档位 | 判定依据 | 允许动作 | 禁止动作 |
|---|---|---|---|
| **HIGH** | ≥2 独立 Evidence 一致 + 在 Envelope 内 + 事实可复核 + 可逆 | **AUTO 自执行**（低影响）；或 B 建议（高影响/不可逆仍走确认） | 不得仅凭 HIGH 跳过 Envelope 边界 |
| **MEDIUM** | 单源或强推断 + 在 Envelope 内 + 可逆 | 低影响可 AUTO；**不可逆/中影响一律 B 建议** | 不得 AUTO 发布/授权等不可逆动作 |
| **LOW** | 信号弱 / 来源少 / 推断链长 | **WAIT**：继续观察或补 Evidence，不决定不执行 | 不得落定任何方向性结论 |
| **UNKNOWN** | 事实不足且不可即时补 | 标 UNKNOWN，触发补 Research 或问 USER FACT（C）；否则 STOP | **禁止用推测填充**（Frozen `UNKNOWN_IS_LEGAL`） |

### 3.2 Confidence 不是静态标签

每次决策前重新评估；Evidence 新增可升档（LOW→MEDIUM→HIGH），新冲突可降档。HIGH 被反证即回 LOW，不固执。

### 3.3 与动作边界的硬连接

- 任何 **不可逆外部动作**（发布到平台 / OAuth / 重大预算）→ 即便 HIGH，仍须 **B + CEO 一次确认**（Human-in-the-loop），Confidence 只影响「是否轻提示」而非「是否惊动 CEO」。
- 任何 **Envelope 外** → 不论置信，统一 **找 CEO Gate**（§5）。
- 任何 **LOW/UNKNOWN** → 不进 B/AUTO，先 WAIT/补证据/问。

---

## 4. Progressive Investment（渐进投资 · 成本阶梯 + 价值门）

**避免：为一个低价值内容启动大量 Employee 与 Token。** 成本随价值阶梯上升，每一级都设价值门（Value Gate）。

### 4.1 成本阶梯（自下而上）

```
L0 Conversation/Quick   零/极低  一句话成稿，无研究无资产
L1 Structured            低      定向抓取+单源比对+轻结论
L2 Deep                 中       多源比对+冲突标注+置信度
L3 Production           中高     生成 Draft+素材+审核（资产成本）
L4 Cross-channel        高       多账号 Variant+分发+回执归集（缩放成本）
```

### 4.2 价值门（每级进入前必过）

| 上一级结论 | 价值门条件 | 否则 |
|---|---|---|
| 收到 Signal | Topic Score ≥ 阈值(暂定 MED) 且 与 Office 目标相关 | 入观察池，不升 L1 |
| L1 Structured 完 | 信息增量 ≥ 阈值 或 用户/CEO 显式要深 | 停在 L1，出轻结论 |
| L2 Deep 完 | 结论支撑「值得生产」(Content Value ≥ 阈值) | 仅存档，不进 L3 |
| L3 Production 完 | 过审核五项 且 Eligibility 满足 | 不进 L4，留草稿 |
| L4 分发前 | Target 非空 且 Distribution Policy 满足 | WAIT/缩范围 |

### 4.3 反例（本轮要杜绝）

「用户说一句『写一篇 GPT-5.6 笔记』」→ 直接 L0 成稿（Quick Path），**不**自动拉起 L2 研究 + L3 生产 + L4 多账号。只有当 AI 判断「值得先调研」(MEDIUM+) 才轻提示升级，且用户三选一（继续调研/直接生成/讨论）。

---

## 5. Strategy Envelope（自主经营边界信封）

AI 可自主经营，**不能自主改变 CEO 已确认的重大方向**。三区模型：

### 5.1 信封维度（由 CEO / Policy 设定，AI 只读）

- **Goal direction**（涨粉/接广告/带货…）：CEO 定，AI 不可改。
- **Audience 大方向**（如「科技从业者」）：CEO 定边界，AI 可在内细化微观受众。
- **Channel family**（主发平台集）：CEO 定边界，AI 可在内调整。
- **Brand safety**：始终在信封内，不可妥协。
- **Budget / Token ceiling**：CEO/Policy 定，AI 不可超。
- **Risk tolerance**：CEO 定。

### 5.2 三区与对应动作

| 区 | 范围举例 | AI 动作 | 是否惊动 CEO |
|---|---|---|---|
| **Envelope 内** | Keyword、Source、微观受众、Topic、内容、发布时间/频率、下一周期微调、账号默认 | AI 自调（A）或低影响 AUTO | 否 |
| **Envelope 边缘** | 首次跨渠道扩展、主内容格式大转向、Channel family 内新增平台、重大资源重排 | AI 建议（B），**Leader 判断**：周明评估后报 CEO 或自批 | 是（看建议） |
| **Envelope 外** | 变现方式改变、换赛道、超预算、重大不可逆外部风险、修改信封本身 | **CEO Gate**（批准/调整/讨论/暂停） | 是（Gate） |

### 5.3 信封与 Confidence 的叠加

边缘/外区的决策，**不论 Confidence 多高**，一律走建议或 Gate；信封只拦「方向」，Confidence 只拦「是否执行」。两者正交。

---

## 6. Learning 模型（一次好/坏不能直接改 Strategy）

**Observation → Candidate Learning → 多次 Evidence → Accepted Learning → Strategy Adjustment**

| 阶段 | 定义 | 动作权限 |
|---|---|---|
| **Observation** | 单次事件（某内容收藏率高/某 Source 失准） | 仅记录，更新短期权重，**不得**固化 |
| **Candidate Learning** | 形成假设（「第一手实测类内容更涨粉」） | 进候选池，标「待验证」 |
| **多次 Evidence** | ≥ N 次（暂定 3）一致 Observation 支撑该假设 | 升级为证据链 |
| **Accepted Learning** | 证据链稳固 → 更新 playbook / 评分权重 / Source 优先级 | 在 Envelope 内自动采纳 |
| **Strategy Adjustment** | 若学习跨信封（如「应新增视频号渠道」） | **须 CEO 批准**；信封内微调 AI 自调 |

**Guardrail**：单次好/坏结果只更新 Observation 与候选，**禁止直接改写 Strategy / Envelope / 重大默认**。防止过拟合单次噪声。

---

## 7. 22 个真实决策的逐项契约回答

> 每个决策块按 §2 的 18 问压缩为 14 个标准字段（Q10–Q15 合并为「决策边界」；Q1–Q9、Q16–Q18 各一字段）。引用 Round 3 归属审计编号（如「项 8-A」）。

### 7.A 定位与策略类（6）

#### D01 赛道 / 账号定位
- **负责人**：王颖(Research&Intel) 协同 周明(Strategist) 核准方向。
- **目标**：确定 Office 在 AI 科技内容中的差异化定位，指导后续全部选题/内容/渠道。
- **输入**：Office 主题(用户给) + Reference(贴链接) 或 行业常识(无对标) + CEO Goal(涨粉/接广告)。
- **Evidence**：参考账号历史内容类型/互动/增长模式；公开搜索到的赛道拥挤度；用户目标方向。
- **判断标准**：定位 = 用户目标 ∩ 参考账号可学模式 ∩ 赛道空白点；评分维度=相关性/差异化/可达性。
- **候选**：① 从业者视角实用测评 ② 前沿资讯快报 ③ 工具横评。
- **为何选此**：Reference 显示该账号靠「第一手实测」起量且与用户「接广告」目标兼容 → 选①，用实测拉开同质化。
- **Confidence**：有 Reference 时 MEDIUM→HIGH（多源一致）；无对标时 MEDIUM（行业常识推断）。
- **Cost/Value**：定位错误代价高但修正成本低（早期）；一次性分析成本中，避免后续选题全偏。
- **决策边界**：定位属**重大方向** → **B 建议 + CEO 确认**（项 1-B）；Envelope 边缘；若用户改赛道(换 Goal) → **找 CEO Gate**(项 39-C)。
- **Envelope 位**：边缘（影响 Goal 表达）。
- **评估**：6–8 周起量信号、接广告路径是否清晰。
- **纠正**：用户「调整」→ 改定位重生成 growth_context；不污染其他 Office。
- **Learning**：多次验证「实测类定位更涨粉」→ Accepted，更新定位权重（信封内）。

#### D02 Audience（受众）
- **负责人**：王颖。
- **目标**：明确内容服务谁，支撑选题与表达。
- **输入**：参考账号互动画像 + 内容主题 + CEO Goal。
- **Evidence**：参考账号粉丝画像（平台可得部分）、高互动内容特征、搜索词。
- **判断标准**：受众 = 高互动内容吸引的人群 ∩ 用户目标客群。
- **候选**：① 科技从业者 ② 泛科技爱好者 ③ AI 产品消费者。
- **为何选此**：参考账号互动以从业者讨论为主 → ①，兼顾 ③ 做个人 IP。
- **Confidence**：MEDIUM（推断自互动）；有 Reference 时 HIGH。
- **Cost/Value**：低成本推断；错误仅影响微观表达，易纠。
- **决策边界**：**A 自调**（微观受众，项 2-B 内「AI 推断」）；大方向受众越信封 → 边缘/外。
- **Envelope 位**：内（微观）/ 边缘（大方向）。
- **评估**：内容互动是否命中预期受众。
- **纠正**：用户一句纠偏或数据反证 → 调整。
- **Learning**：互动数据持续印证 → 固化受众权重。

#### D03 Channel Strategy（渠道组合）
- **负责人**：陈帆(Channel Operator) 提，周明 核准。
- **目标**：选择主发平台集，匹配内容类型与用户目标。
- **输入**：内容类型(实测类/视频向) + Reference 主平台 + CEO Goal + 各 Channel 能力事实(VERIFIED/CONDITIONAL/UNKNOWN)。
- **Evidence**：参考账号主平台、内容形态适配度、Channel 能力真相（Frozen `UNKNOWN_IS_LEGAL`，不支持定时不写死）。
- **判断标准**：Channel = 内容形态最适配 ∩ 用户目标可达 ∩ 能力 VERIFIED/CONDITIONAL。
- **候选**：① 小红书+抖音 ② 仅小红书 ③ 加 Bilibili/YouTube。
- **为何选此**：实测类图文+短视频双适配，Reference 在 XHS/Douyin 起量 → ①。
- **Confidence**：MEDIUM（内容形态推断）；有 Reference 时 HIGH。
- **Cost/Value**：连多平台有 OAuth 与维护成本；首轮选高适配两平台控成本（Progressive Investment L4 前的收敛）。
- **决策边界**：**B 建议 + CEO 确认**（项 15-B）；信封内常规加平台可 A，首跨新平台族 → 边缘。
- **Envelope 位**：内（已知族内）/ 边缘（新增族）。
- **评估**：各平台起量速度、涨粉效率。
- **纠正**：用户调整渠道 → 改策略重算 Target。
- **Learning**：某平台持续低效 → Accepted 降权（信封内）。

#### D04 Source 选择与监控
- **负责人**：王颖(Research&Intel)。
- **目标**：建立并维护初始 Source 池，保证情报质量与覆盖。
- **输入**：Office 主题 + Reference(互链源) + 公开搜索 + CEO 自然语言「重点看这个」。
- **Evidence**：主题关键词命中、参考账号引用源、行业媒体权威性、历史信号质量。
- **判断标准**：Source = 相关性高 ∩ 权威性足 ∩ 更新频繁；分优先级 P0/P1/P2。
- **候选**：① 官方博客(OpenAI/Anthropic) ② 科技媒体 ③ 参考账号互链 ④ 社区(Reddit/HN)。
- **为何选此**：用户做 AI 科技 → ①+② 为核心；Reference 互链 → ③；④ 作 P1 补信号。
- **Confidence**：HIGH（官方源 VERIFIED）；社区源 MEDIUM（噪声多）。
- **Cost/Value**：发现成本一次；监控成本随源数线性；按信号量自调频率（项 13-A）。
- **决策边界**：**A 自维护**（项 8/9-A）；用户「重点看/别看」自然语言快捷（C 轻量）；专业管理界面 **E 隐藏**。
- **Envelope 位**：内。
- **评估**：Source 产出的 Signal 质量 / 命中率。
- **纠正**：用户「别看这个」→ 降/移除；信号稀疏 → 自动扩搜索。
- **Learning**：某源持续高命中 → 升优先级（Accepted）。

#### D05 对标账号选择
- **负责人**：王颖。
- **目标**：发现可学习对标，支撑定位/选题/表达。
- **输入**：Office 主题 + Reference + 公开搜索。
- **Evidence**：同赛道高增长账号、内容模式可迁移性、与用户目标兼容。
- **判断标准**：对标 = 赛道相关 ∩ 增长可解释 ∩ 模式可学 ∩ 非直接竞品抄袭。
- **候选**：3–5 个候选，按可学性排序。
- **为何选此**：选增长靠「实测」而非「搬运」的账号，避免教 AI 学搬运。
- **Confidence**：MEDIUM（公开数据推断）；有 Reference 时 HIGH。
- **Cost/Value**：发现成本低；监控中成本。
- **决策边界**：**A 自动发现监控**（项 11-A）；出现在 Expert 区。
- **Envelope 位**：内。
- **评估**：对标模式是否真可迁移（学后效果）。
- **纠正**：用户指出某对标不合适 → 移除。
- **Learning**：可迁移模式沉淀为选题模板。

#### D06 Keyword（关键词）
- **负责人**：王颖。
- **目标**：派生检索/监控关键词，捕捉 Signal。
- **输入**：定位 + 受众 + 对标内容词 + 行业词。
- **Evidence**：参考账号高频词、搜索词、行业术语。
- **判断标准：关键词 = 高搜索量 ∩ 高相关 ∩ 低至中竞争。
- **候选**：8–12 个主词 + 长尾。
- **为何选此**：围绕「AI 实测/模型评测/工具对比」派生，避开泛词。
- **Confidence**：HIGH（术语派生确定性高）。
- **Cost/Value**：几乎零成本；直接提升 Signal 召回。
- **决策边界**：**A 自动派生维护**（项 5-A）；Expert 区可见。
- **Envelope 位**：内。
- **评估**：关键词命中 Signal 率。
- **纠正**：用户补词自然语言 → 并入。
- **Learning**：高命中词升权。

### 7.B 选题与调研类（6）

#### D07 Signal → Opportunity
- **负责人**：王颖。
- **目标**：从 Signal 池识别「什么值得做」的候选。
- **输入**：多 Source 采集的 Signal + Keyword 命中 + 参考动态。
- **Evidence**：≥2 Source 提及（去重聚类后）、与 Office 目标相关、时效性。
- **判断标准**：Opportunity = 多源一致 ∩ 目标相关 ∩ 时效窗口内；评分=相关×热度×差异。
- **候选**：聚类的若干 Opportunity，按分排序。
- **为何选此**：3 源提及 OpenAI 新模型 → 高 Opportunity。
- **Confidence**：多源一致 HIGH；单源 MEDIUM；孤源 LOW→WAIT 观察。
- **Cost/Value**：聚类成本低；过早升 Opportunity 浪费后续成本 → 设阈值。
- **决策边界**：**A 自动聚类**（信封内）；LOW 信号留观察池不升。
- **Envelope 位**：内。
- **评估**：升 Opportunity 后是否真被做、效果。
- **纠正**：误聚 → 拆/并。
- **Learning**：某类 Signal 持续高转化 → 升权聚类阈值。

#### D08 Opportunity → Topic
- **负责人**：王颖。
- **目标**：把 Opportunity 落成具体可产内容主题（Topic）。
- **输入**：Opportunity + Reference 表达模式 + 受众兴趣。
- **Evidence**：Opportunity 评分 + 参考账号同类内容互动。
- **判断标准**：Topic = Opportunity ∩ 可表达 ∩ 受众想看；初评分。
- **候选**：同一 Opportunity 可拆 1–3 个角度 Topic。
- **为何选此**：OpenAI 新模型 → 拆「实测」「对比」「科普」三角度。
- **Confidence**：MEDIUM（需后续 Research 验证）。
- **Cost/Value**：低成本；过早定稿浪费 → 进推荐卡待 CEO 看。
- **决策边界**：**A 生成推荐**（信封内）；CEO 看卡 B。
- **Envelope 位**：内。
- **评估**：被 CEO 采纳率、后续效果。
- **纠正**：CEO 否 → 弃/改角度。
- **Learning**：高采纳角度模式沉淀。

#### D09 Topic 排序
- **负责人**：王颖 协同 周明。
- **目标**：从候选 Topic 池排出本周期优先序。
- **输入**：各 Topic 初评分 + 时效 + 资源占用。
- **Evidence**：评分维度一致可比。
- **判断标准**：排序 = 分高 ∩ 时效紧 ∩ 资源可承载 优先。
- **候选**：全池重排。
- **为何选此**：紧时效高分 Topic 置顶。
- **Confidence**：HIGH（规则确定）。
- **Cost/Value**：零成本。
- **决策边界**：**A 自动排序**（信封内）。
- **Envelope 位**：内。
- **评估**：置顶 Topic 实际效果。
- **纠正**：CEO 调整顺序 → 采纳。
- **Learning**：排序权重微调。

#### D10 是否值得 Research（价值门）
- **负责人**：王颖。
- **目标**：决定是否从 L1 升 L2 Deep Research（过 §4 价值门）。
- **输入**：Topic 评分 + 已有 Knowledge + 用户是否显式要深。
- **Evidence**：Topic 分 ≥ 阈值；信息增量预期。
- **判断标准**：值得 Research = 分够 ∩ 现有 Knowledge 不足 ∩ 过价值门。
- **候选**：① 升 L2 ② 停 L1 出轻结论 ③ WAIT。
- **为何选此**：高分紧时效 → 升 L2；低分 → 停 L1。
- **Confidence**：MEDIUM（预期值推断）。
- **Cost/Value**：L2 成本中；低分硬升 = 浪费 → 严卡门。
- **决策边界**：**A 自判**（信封内）；LOW 分 WAIT。
- **Envelope 位**：内。
- **评估**：升 L2 后结论是否被采纳。
- **纠正**：升后无增量 → 后续降门。
- **Learning**：阈值校准。

#### D11 Research 深度（L1/L2 选档）
- **负责人**：王颖。
- **目标**：选 Structured(L1) 还是 Deep(L2)。
- **输入**：Topic 复杂度 + 争议性 + 事实密度需求。
- **Evidence**：主题是否多争议/多事实。
- **判断标准**：深度 = 争议高/事实密 → L2；否则 L1。
- **候选**：L1 / L2。
- **为何选此**：GPT-5.6 有官方事实+社区争议 → 选 L2 多源比对。
- **Confidence**：MEDIUM（复杂度推断）。
- **Cost/Value**：L2 成本中；过度深 = 浪费。
- **决策边界**：**A 自选档**（项 14-A，Expert 可改）；信封内。
- **Envelope 位**：内。
- **评估**：深度是否匹配结论需求。
- **纠正**：结论冲突多 → 升档补查。
- **Learning**：主题类型→深度映射沉淀。

#### D12 是否值得生产（Content Value 门）
- **负责人**：李想(Producer) 协同 周明。
- **目标**：Research 完后判断是否进 L3 Production。
- **输入**：Research 结论 + Content Value 评分 + 审核预判。
- **Evidence**：结论支撑「用户会看/会互动」。
- **判断标准**：值得生产 = Research 结论明确 ∩ Content Value ≥ 阈值 ∩ 无合规硬伤。
- **候选**：① 生产 ② 仅存档 ③ WAIT 补 Research。
- **为何选此**：结论清晰且切搜索红利 → 生产。
- **Confidence**：MEDIUM（价值推断）；结论 UNKNOWN → STOP/补。
- **Cost/Value**：L3 成本中高；硬产低价值 = 浪费。
- **决策边界**：**A 自判**（信封内）；UNKNOWN → WAIT/STOP。
- **Envelope 位**：内。
- **评估**：生产后互动。
- **纠正**：生产后差 → 回看价值门。
- **Learning**：价值门阈值校准。

### 7.C 内容生产类（3）

#### D13 Draft 数量（1–3 版）
- **负责人**：李想。
- **目标**：生成恰当数量的 Draft 版本。
- **输入**：Brief + 渠道形态 + 历史表现。
- **Evidence**：同类内容历史互动差异。
- **判断标准**：默认 1–3 版；高不确定/多账号差异大 → 上限 3；达 5 提示选定（防无限，Round 2 Doc3）。
- **候选**：1 / 2 / 3 版。
- **为何选此**：单主渠道 1 版够；跨形态差异大 → 3 版。
- **Confidence**：HIGH（规则确定）。
- **Cost/Value**：多版边际成本；严控上限防烧 Token。
- **决策边界**：**A 自动出推荐版**（项 24-A）；信封内。
- **Envelope 位**：内。
- **评估**：推荐版是否被采纳。
- **纠正**：用户要更多 → 生成但计上限。
- **Learning**：最佳版式沉淀模板。

#### D14 推荐版本（选哪版为推荐）
- **负责人**：李想。
- **目标**：从多版中选一为推荐版，余标备选。
- **输入**：各版质量评分 + 渠道适配 + 参考风格。
- **Evidence**：质量评分维度（结构/表达/合规/互动预期）。
- **判断标准**：推荐 = 综合分最高 ∩ 合规过 ∩ 风格近参考。
- **候选**：各版互比。
- **为何选此**：v2 结构更口语且过合规 → 推荐。
- **Confidence**：MEDIUM（互动预期推断）；有历史则 HIGH。
- **Cost/Value**：零成本。
- **决策边界**：**A 推荐**（项 25-A）；深度比稿 E 隐藏。
- **Envelope 位**：内。
- **评估**：推荐版实际互动。
- **纠正**：用户选备选 → 换推荐。
- **Learning**：高分特征沉淀。

#### D15 素材策略（封面/图/视频）
- **负责人**：李想 协同 陈帆(渠道规则)。
- **目标**：决定是否需要素材、生成几版、选哪版。
- **输入**：内容形态 + 渠道规范 + 历史素材表现。
- **Evidence**：渠道对封面/图的要求、历史点击。
- **判断标准**：需素材 = 渠道强依赖视觉 ∩ 无现成库素材；生成 1–2 版选 1。
- **候选**：生成 / 库选 / 上传；生成 1–2 版。
- **为何选此**：小红书强依赖封面 → 生成 2 选 1；复用历史高CTR封面。
- **Confidence**：MEDIUM（渠道推断）。
- **Cost/Value**：生成有成本；复用库零成本优先。
- **决策边界**：**A 生成并选**（项 27-A）；深管 E 隐藏。
- **Envelope 位**：内。
- **评估**：带素材 vs 不带 CTR。
- **纠正**：用户换 → 替换/重做局部。
- **Learning**：高 CTR 素材特征沉淀。

### 7.D 发布与分发类（5）

#### D16 Channel / Account 选择（Target）
- **负责人**：陈帆。
- **目标**：推荐本次发布的目标账号集。
- **输入**：内容定位 + Channel Strategy + 各 Account Positioning + 历史表现 + **Eligibility**(失效/未授权 BLOCKED) + Distribution Policy。
- **Evidence**：账号历史表现、定位匹配度、Eligibility 状态（Frozen `TARGET_NE_ELIGIBILITY`）、平台限频。
- **判断标准**：Target = 定位匹配 ∩ Eligibility 满足 ∩ 策略覆盖；不匹配账号灰显不强行（项 22-E）。
- **候选**：推荐集 / 用户增减 / 全选。
- **为何选此**：GPT-5.6 实测 → 主号最匹配 → 推 XHS主号+抖音主号。
- **Confidence**：HIGH（匹配规则确定）；未授权账号 MEDIUM 但 BLOCKED。
- **Cost/Value**：多发边际成本低但风险升；按策略控。
- **决策边界**：**B 建议 + CEO 确认**（项 30-B）；HIGH 匹配仍走确认（不可逆外部动作，Human-in-loop）。
- **Envelope 位**：内（已知账号）/ 边缘（首跨新账号族）。
- **评估**：各账号发布后表现（per-Account，Frozen `PUBLICATION_PER_ACCOUNT_TRUTH`）。
- **纠正**：CEO 调整 → 增减账号；不匹配不强行。
- **Learning**：高表现账号升默认优先（信封内）。

#### D17 Variant 适配深度（轻/重/完全不同）
- **负责人**：陈帆（遵循 Frozen `NO_CROSS_ACCOUNT_CONTEXT_LEAK`）。
- **目标**：为每选中账号定适配档。
- **输入**：Intent + 各账号 positioning/tone_style（隔离不串）。
- **Evidence**：账号定位差异度。
- **判断标准**：差异小 → HIGH_REUSE(轻)；差异大 → FULL_DIVERGENCE(完全不同)；中 → 重生成。
- **候选**：轻 / 重 / 完全不同。
- **为何选此**：XHS主号与抖音主号定位近 → XHS 轻适配、抖音重生成(视频向)。
- **Confidence**：HIGH（差异规则确定）。
- **Cost/Value**：重/完全不同成本高；按差异精准选档省成本。
- **决策边界**：**A 自动选档**（项 31-A，Expert 可改）。
- **Envelope 位**：内。
- **评估**：各 Variant 表现。
- **纠正**：某账号表现差 → 升档重做。
- **Learning**：差异→档位映射沉淀。

#### D18 发布时间
- **负责人**：陈帆。
- **目标**：建议各账号发布时间。
- **输入**：历史表现时段 + 平台活跃峰 + 内容时效 + 平台 scheduling 能力(Frozen `SCHEDULING_IS_CONDITIONAL`)。
- **Evidence**：账号历史高互动时段、平台峰。
- **判断标准**：时间 = 高互动时段 ∩ 平台支持(VERIFIED/CONDITIONAL)；不支持定时 → 标不支持不写死。
- **候选**：立即 / 建议时段 / 用户精调。
- **为何选此**：XHS 晚 8 峰、抖音晚 9 峰 → 分别建议。
- **Confidence**：MEDIUM（时段推断）；不支持定时平台 UNKNOWN→标不支持。
- **Cost/Value**：零成本建议；错峰提升互动。
- **决策边界**：**A 建议时间 / 默认立即**（项 32-A）；逐账号精调 E 隐藏。
- **Envelope 位**：内。
- **评估**：时段实际互动。
- **纠正**：表现差 → 调时段。
- **Learning**：最优时段沉淀。

#### D19 发布频率
- **负责人**：陈帆（守平台限频）。
- **目标**：设定各账号发布节奏。
- **输入**：平台限频规则 + 内容供给 + 账号承载。
- **Evidence**：平台官方限频（VERIFIED）。
- **判断标准**：频率 = 不超平台限频 ∩ 内容供给可持续。
- **候选**：日更 / 周 N 更 / 按需。
- **为何选此**：参考账号周更起量 → 初定周 2–3 更。
- **Confidence**：HIGH（规则确定）。
- **Cost/Value**：过高触限频/掉权；过低掉活跃。
- **决策边界**：**A 自设节奏**（项 36-A，Expert 可改）。
- **Envelope 位**：内。
- **评估**：频率对涨粉/权重的实际影响。
- **纠正**：掉权 → 降频。
- **Learning**：最优频率沉淀。

#### D20 是否跨渠道扩展
- **负责人**：陈帆 提，周明 核准。
- **目标**：决定是否把内容扩到更多渠道/账号。
- **输入**：当前渠道表现 + 内容可迁移性 + 资源余量。
- **Evidence**：现有渠道 ROI、内容形态跨平台适配度。
- **判断标准**：扩展 = 现有渠道达预期 ∩ 内容可迁移 ∩ 资源余 ≥ 阈值。
- **候选**：① 扩 ② 维持 ③ WAIT。
- **为何选此**：XHS/抖音起量且视频可迁 Bilibili → 建议扩 Bilibili（边缘）。
- **Confidence**：MEDIUM（迁移推断）。
- **Cost/Value**：扩展有 OAuth/维护成本；过早扩稀释精力。
- **决策边界**：**B 建议 + CEO 确认**（信封边缘，项 15 边界）；首跨新平台族 → 边缘/外。
- **Envelope 位**：边缘。
- **评估**：新渠道起量速度。
- **纠正**：新渠道低效 → 收。
- **Learning**：跨渠道协同模式沉淀（超信封需 CEO 批）。

### 7.E 周期治理类（2）

#### D21 是否继续下一周期
- **负责人**：周明(Strategist)。
- **目标**：基于 Evaluation 决定是否起下一轮。
- **输入**：Evaluation 结论 + 当前策略表现 + 资源。
- **Evidence**：指标趋势（收藏率↑/涨粉）、建议置信。
- **判断标准**：继续 = 策略有效(指标正向) ∩ 资源可续 ∩ 信封内。
- **候选**：① 继续 ② 暂缓 ③ 调整方向(越信封→Gate)。
- **为何选此**：收藏率↑12% 且建议清晰 → 继续。
- **Confidence**：MEDIUM（趋势推断，需多次 Observation）。
- **Cost/Value**：继续有供给成本；停错失势。
- **决策边界**：**B 建议 + CEO 确认**（项 38-B）；调整方向越信封 → **找 CEO Gate**。
- **Envelope 位**：内（微调）/ 边缘（方向调整）。
- **评估**：下一周期指标。
- **纠正**：下周期差 → 回看策略。
- **Learning**：周期节奏校准（信封内）。

#### D22 是否改变 Strategy（信封越界判定）
- **负责人**：周明 提，**CEO Gate**。
- **目标**：判断是否需修改整体 Strategy / Envelope。
- **输入**：Envelope 内表现 + 外部变化 + Accepted Learning（若跨信封）。
- **Evidence**：持续 Evidence 链（≥3 次）指向需变。
- **判断标准**：改 Strategy = 信封内微调 AI 自调；跨信封(换赛道/变现/超预算) → **CEO Gate**。
- **候选**：① 信封内自调 ② 报 Leader ③ Gate CEO。
- **为何选此**：仅「扩抖音」= 信封内/边缘 → 建议；「转带货」= 越信封 → Gate。
- **Confidence**：依赖 Evidence 强度；单次 Observation 不得触发。
- **Cost/Value**：改错代价高；须稳妥。
- **决策边界**：**信封内 A 自调**；**边缘 B 报 Leader**；**外 找 CEO Gate**（项 39-C）。
- **Envelope 位**：定义本身。
- **评估**：改后长期指标。
- **纠正**：Gate 被否 → 维持。
- **Learning**：仅 Accepted Learning（多次 Evidence）可提议改 Strategy；单次禁改（§6）。

---

## 8. 决策边界总表（速查）

| 动作 | 自执行(AUTO) 条件 | 仅建议(B) 条件 | WAIT | STOP | 升级 Leader | 找 CEO |
|---|---|---|---|---|---|---|
| 定位/受众大方向 | — | 重大方向 | — | 事实不足 | 边缘协同 | 改 Goal |
| 微观受众/关键词/Source | 信封内 HIGH/MED 可逆 | — | LOW | UNKNOWN 不可补 | — | 用户事实 |
| 渠道(已知族) | 信封内 | 常规加平台 | — | — | — | — |
| 渠道(新族)/跨渠道扩展 | — | 边缘 B | — | — | 首跨报 Leader | 超预算 |
| Topic/Research/内容 | 信封内价值门过 | 高风险轻提示 | 低分 | UNKNOWN | 资源冲突 | — |
| Target/发布时间/频率 | 信封内 | 不可逆仍确认 | — | 合规硬伤 | 排期冲突 | 发布确认(Human-in-loop) |
| 下一周期/改 Strategy | 信封内微调 | 边缘 B | — | — | 边缘报 Leader | 越信封 Gate |

**不可自动化红线（与 Round 3 §6 一致）**：OAuth 授权(D)、发布确认(B/D Human-in-loop)、Strategy Envelope 越界(C Gate)、用户独有事实(C)。

---

## 9. STOP FOR CEO REVIEW

本轮只建立 **AI 员工自主决策责任制**（18 问契约 + Confidence 闸门 + Progressive Investment + Strategy Envelope + Learning），**未新增功能、未改 UI/Runtime/Schema/DB/Authority/Frozen**。所有结论消费 Frozen 不变量。

待 CEO 裁决的开放点（非阻塞，标注待定）：
- 价值门阈值（Topic Score / Content Value / 观察次数 N）的初值，需后续用真实数据校准（属 Runtime Config / Extension Points，不在本 Authority 冻结范围）。
- Envelope 维度的初始边界值（Goal/Channel family/Budget）由 CEO 首次表达时确立。

若裁决通过，五轮研究（领域 → 产品映射 → 功能交互 → 端到端 → AI 公司体验 → 本决策模型）已自洽，可进入 **IA / 低保真结构稿**消费本模型。

*CONTENT GROWTH AI EMPLOYEE DECISION MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
