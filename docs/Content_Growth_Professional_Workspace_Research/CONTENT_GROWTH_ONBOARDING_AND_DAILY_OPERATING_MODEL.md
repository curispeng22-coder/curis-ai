# CONTENT GROWTH — ONBOARDING & DAILY OPERATING MODEL
### 首次建立 · Daily CEO · Deep-dive 三种使用深度

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_END_TO_END_JOURNEY_MODEL.md`（Journey A 全步骤）· `CONTENT_GROWTH_CONTENT_CREATION_MECHANICS.md` · `CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` · `CONTENT_GROWTH_ERROR_RECOVERY_AND_STATE_MODEL.md`
前置：Product Experience Model（驾驶舱 8 类 / 投影合同 / 7 Surface / Quick·Structured·Deep 升级）；Domain Operating Model；Frozen Domain Authority。

---

## 0. 红线

- 首次建立**不是 12 步向导**：1 次表达意图 + 少量必要确认 → 开始经营（见 Doc 1 Journey A）。
- **三种使用深度必须隔离复杂度**：Daily CEO 长期不暴露 Expert 复杂度；Deep-dive 才进专业 Surface。
- 团队在后台组建，用户**不**被迫看「建立了 4 个员工」；仅主动点「看看团队」才展示。
- 不新造 Onboarding primitive；全部复用 Office / Intent / Source / Employee Service / Work / Result。

---

## 1. FIRST-TIME SETUP（深化 Journey A）

### 1.1 启动入口与首屏
首次进入 Workspace，主区是**经营驾驶舱空态**，不是设置向导：
- 一句话输入框 + 三个轻建议卡（做内容增长 / 做产品研发 / 其他）。
- 用户说「我想开始做 AI 科技内容」即触发建立（Doc 1 A01）。

### 1.2 必须问 vs 可推断
系统只在**影响后续情报质量与定位**时追问，且每项给「跳过，你帮我定」：

| 问题 | 必须问？ | 若跳过，Employee 推断依据 |
|---|---|---|
| 主要面向谁 | 建议问 | 从内容主题+公开对标推断 Audience |
| 主要在哪发 | 建议问 | 主题常见平台（AI 科技→XHS+Douyin+B站） |
| 已有账号吗 | 建议问 | 无则先不连，之后随时加 |
| 做什么内容 | **已由首句给出** | — |
| 账号定位/调性 | 可推断 | 王颖基于对标+主题生成建议，用户采用/改/跳 |
| 初始关键词 | 可推断 | 王颖从主题派生 8 个 |
| 对标账号 | 可推断 | 公开搜索发现 5 个候选，加入监控 |
| 历史内容 | 可选 | 无则不分析，靠对标推断 |

### 1.3 来源接入（可无 / 可补）
- 用户可在建立时粘网站/账号（A03）；也可**完全不连**，系统先跑「无源分析」，之后随时补（B 路线）。
- 「连接已有账号」走 Channel OAuth（E01/E02），建立时可连可暂不连。
- 历史内容导入：用户上传文件/授权平台抓取 → 王颖做「账号定位分析」；无则跳过。

### 1.4 最小团队组建（后台，非前台仪式）
- `setup` Work 闭合后，Responsibility Router 建 4 个 Service 关系（王颖/李想/陈帆/周明）。
- 用户**不**需要看到「建立了 4 个员工」；驾驶舱①只显示「团队已就位」结果卡。
- 主动查看入口：点结果卡「看看团队」→ Utility 速览（姓名+责任+正在做），不强制。

### 1.5 用户离开后系统如何继续
- `intel-scan`（监控 Source）+ `positioning-analysis`（定位/对标）在 Runtime 后台跑，不依赖用户在线（A05）。
- 产出 Signal→Opportunity→Topic 与「定位建议」，以 Result/Artifact 落库；用户回来见通知（A06/A08）。

### 1.6 首次 Opportunity → 选题推荐 的完整链条
A06（Signal 通知）→ A07（定位/关键词/对标建议，用户采用）→ A08（3 张 Topic 卡「推荐 3 个选题」）。到此首次建立闭环完成。

---

## 2. DAILY CEO（每天看结果 + 少量判断）

### 2.1 每天打开看到什么
进入即**经营驾驶舱**（默认 Main），按优先级排序（Product Experience §1.3）：
④需决定 > ③需关注变化 > ⑤在途 > ①结果 > ⑧推荐 > ⑦增长 > ②重点 > ⑥发布。

典型日：
- ③「OpenAI 新动态，3 源提及」（点开看依据）
- ①「上周内容评估：收藏率↑12%，建议扩抖音」
- ⑤「GPT-5.6 选题 研究中 / 抖音主号 平台审核中」
- ⑧「下一周期已启动：3 个新选题 👇」

### 2.2 Daily CEO 的「动作词汇」（最小集）
每天只需会这几种：
- **查看依据**（展开 Evidence / 为什么值得做）
- **就做这个 / 先调研 / 直接生成**（对选题）
- **批准 / 调整 / 讨论 / 暂停**（对 Decision Gate）
- **按建议继续**（对 Evaluation 建议）
- **发布**（对可发布内容，1 次确认）
- **问员工**（不懂就问，携带上下文）

### 2.3 Daily CEO 不应看到 / 不做的
- 不进全量 Signal 池、全量选题库、裸 Analytics Dashboard（只经投影/Utility 按需下钻）。
- 不配 Workflow、不选 Employee、不写 Scope、不调阈值。
- 不手动维护 Source/账号（除非主动进低频区）。

### 2.4 判断节奏
- 无 Gate 时：看结果卡，点「按建议继续」即可，系统自主推进。
- 有 Gate（④置顶）时：四选一，平均每日决策 < 3 次。
- 离开再回：状态连续（见 Doc 5），不丢在途、不重复通知。

---

## 3. DEEP-DIVE USER（偶尔深入）

### 3.1 何时进入 Deep-dive
用户主动点 7 个 Professional Surface 之一（信息与机会 / 选题 / 研究与洞察 / 内容 / 增长与评估 / 反馈 / 渠道）即进入专家深度。Daily CEO 不被强制进入。

### 3.2 Deep-dive 才暴露的复杂度（按 Surface）
| Surface | Deep-dive 才可见 |
|---|---|
| 信息与机会 | 全量 Signal 池、聚类/去重队列、强度计算、阈值 |
| 选题 | 完整池、评分明细、去重候选、跨渠道排期 |
| 研究与洞察 | Scope/来源/多源比对/置信度/Unknown 区 |
| 内容 | 多版对比、比稿、素材库、合规预检明细 |
| 增长与评估 | 原始指标、归因模型、跨账号对比、基准线 |
| 反馈 | 全量待处理队列、合规红线校验、防封策略 |
| 渠道 | Connector 健康、平台规则、API 限额、授权令牌 |

### 3.3 返回机制
每个 Surface 有「返回经营」/ 关闭 Utility；回到驾驶舱，Context 不丢（Doc 1 B07、E03）。

### 3.4 三深度不互相污染的原则
- **FIRST-TIME**：引导极简，1 句话起步，不展示团队/池/阈值。
- **DAILY**：投影层，只结果/价值/建议/风险/决策。
- **EXPERT**：按需下钻，复杂度只在主动进入时出现，且可随时退回投影层。
- 同一对象（如 Topic）在三层是**不同投影深度**，不复制数据（Product Experience §4.6）。

---

## 4. QUICK PATH 在三种深度里的位置
- FIRST-TIME / DAILY 都可直接用 Quick（一句话→结果→1 次发布确认，Doc 1 Journey H）。
- Deep-dive 用户也可回落 Quick；Quick 不因系统变复杂而变复杂。
- 升级提示非阻塞（Product Experience §7.3）：值得调研时只轻提示，用户三选一。

---

## 5. 与 FINAL ACCEPTANCE 对应
- 「第一次使用、说经营意图」→ §1.1–1.2（A01–A02）
- 「连接 3 XHS + 2 Douyin」→ Doc 1 E01–E02
- 「监控 5 网站 + 3 对标」→ §1.3（A03 / B01）
- 「第二天推荐 3 选题」→ §1.6（A08）
- 「Daily 只看结果做少量判断」→ §2
- 「不暴露 Expert 复杂度」→ §3.4

---

*CONTENT GROWTH ONBOARDING & DAILY OPERATING MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
