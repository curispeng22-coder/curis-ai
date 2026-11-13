# CONTENT GROWTH — PRODUCT EXPERIENCE MODEL
### 默认 Main · Context · Surface · Utility · Result Projection · Quick/Structured/Deep 体验

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen）
Companion: `CONTENT_GROWTH_PRODUCT_MAPPING_MODEL.md` · `CONTENT_GROWTH_USER_JOURNEY_MODEL.md` · `CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md`
前置：Domain Operating Model（CEO Experience Model 已定义投影规则与默认 Main 五要素，本模型将其落地为可解释产品体验）。

---

## 0. 设计宪法（两个最高要求之一：用户是小白 CEO）

> AI 员工处理复杂过程；CEO 看 **结果 / 价值 / 建议 / 风险 / 需决定的事**。
> 后台复杂，前台简单；**想不清楚→说不清楚→不允许做 UI**。

本模型只定义「产品信息合同」与「体验行为」，不定义颜色/字号/卡片/间距（那是 UI 阶段）。

---

## 1. 默认 Main：经营驾驶舱（回答本轮 §1/§3/§26-Q1/Q2）

### 1.1 它是什么（不是什么）
- **是**：Workspace Main 的默认呈现 = 「经营驾驶舱」= Operating Result Surface / Attention Feed / Current Business Focus 的合称（名字待 CEO 定，本文暂称**经营驾驶舱**）。
- **不是**：信息池、选题池、Research 数据库、内容库、Analytics Dashboard 的任一全量视图。

### 1.2 应展示的 8 类「经营结果类型」
| 类型 | 内容 | 来源对象 |
|---|---|---|
| ① 员工最新结果 | 各 Responsible Employee 最近交付摘要 | Result（投影） |
| ② 当前经营重点 | 本季方向 + 在途关键选题 | Strategy Envelope + 在途 Work |
| ③ 需关注的变化 | 信号/数据异常 → 3 条级投影 | Signal→Result 投影 |
| ④ 需决定的事 | 待 CEO Gate 卡，附建议 | Decision（CEO Gate） |
| ⑤ 重要在途工作 | 发布中/审核中/研究中状态 | Work（in-flight） |
| ⑥ 发布结果 | per-Account 真相（XHS 阅读中/抖音审核中） | Publication（Result） |
| ⑦ 增长变化 | 本周收藏率↑12% / 完播↓5% | 共享增长真相（Result） |
| ⑧ 下一步推荐 | 系统建议的下一步动作 | Handoff / Next-cycle 假设 |

### 1.3 排序 / 出现 / 消失 / 生成者（回答本轮 §3）
- **排序**：④需决定 > ③需关注变化 > ⑤在途 > ①结果 > ⑧推荐 > ⑦增长 > ②重点 > ⑥发布。（风险/决策优先。）
- **出现**：当对应 Result/Decision/Handoff/Work 状态变化且未关闭时出现；CEO Gate 卡出现即置顶。
- **消失**：Decision 被裁决（批准/调整/讨论/暂停）→ 卡消失，转 next Cycle；在途 Work 闭合→从⑤移除进①；变化已读/无新 Signal→③收敛。
- **谁生成**：全部由 Employee 在 Runtime 产出的 Result/Decision/Handoff/Work 经 CEO Projection 规则压缩生成（OUTPUT 1 §1 / Domain CEO Model §1），**Main 不自己算任何东西，只是投影层**。

### 1.4 它是现有对象的 Projection，不是新 primitive
- 驾驶舱 = 对 `Result / Decision / Handoff / Work / Publication` 等**现有对象**的聚合投影视图。
- **禁止**为此新造「聚合对象 / AttentionFeed 类型」；以现有对象 + 投影规则解决（Domain Mapping G4）。

---

## 2. Relevant Gates（CEO 不是每步审批人，回答本轮 §9/§26-Q5 部分）

仅 **真正 Relevant Gate** 进 CEO 决策（依据 Shared Authority §0.2 `[CURIS-AUTH]`）：

| Gate 类型 | 触发 | CEO 操作 |
|---|---|---|
| 方向变化 | 选题偏离本季重点/策略信封 | 批准/调整 |
| 重大投入 | Deep Research 高成本 / 多平台大投放 | 确认预算 |
| 明显风险 | 合规红线临近 / 平台限流预警 | 讨论/暂停 |
| 重要外部动作 | 首次对外发布/商单/投放 | 批准 |
| 超策略边界 | 选题超出 Approved Strategy Envelope | Gate |
| 高价值机会 | 竞争空白/趋势红利 | 确认取舍 |
| 重大取舍 | 渠道优先级/资源分配 | 决策 |

CEO 默认操作四选一：**批准 / 调整 / 讨论 / 暂停**。日常 Team 自主推进（CONTINUE/ADJUST）。

---

## 3. Result Projection 信息合同（回答本轮 §4）

每个员工复杂工作完成后，进入驾驶舱的投影必须包含以下字段（先定义合同，非高保真）：

| 字段 | 含义 | 例 |
|---|---|---|
| **Result Title** | 一句话结果名 | 「GPT-5.6 办公实测 选题已定」 |
| **Conclusion** | 结论 | 推荐做，价值高 |
| **Business Meaning** | 对经营意味着什么 | 抢占 AI 办公搜索红利 |
| **Recommendation** | 建议怎么办 | 先做 XHS+抖音双发 |
| **Value** | 预期业务价值 | 高（搜索流量红利窗口） |
| **Risk** | 风险 | 合规需 AI 标识 |
| **Confidence / Unknown** | 置信度与未知项 | 高；3 处待证实 |
| **Next Step** | 下一步 | 进入 Brief |
| **Employee** | 负责员工 | 王颖（Research&Intel） |
| **Relevant Gate** | 是否需 CEO | 否 / 是（类型） |
| **Evidence access** | 证据入口 | 「查看来源/证据」→ Utility |

> 员工内部「300 Signals / 20 Sources / 10 Competitors / Deep Research」**永不**进入驾驶舱；只投影为上述合同。证据需 deep-dive 时经 Utility 展开（§5）。

---

## 4. Professional Surfaces（16 阶段 → 7 工作面，回答本轮 §6/§26-Q6）

> 16 阶段 ≠ 16 Surface。组合原则：①同 Responsibility ②同对象族 ③同进入情境 ④CEO 通常只按需深入。

| # | Surface（建议名） | 覆盖阶段 | 谁主用 | CEO 何时进 |
|---|---|---|---|---|
| 1 | **信息与机会** | ①②③ Signal/Opportunity | Research&Intel | 想看「为什么值得做」依据 |
| 2 | **选题** | ④⑤ Topic Pool + Judgment | Research&Intel + Strategist | 看推荐/做决策（Gate） |
| 3 | **研究与洞察** | ⑥ Research | Research&Intel | 看结论/证据/未知 |
| 4 | **内容** | ⑦⑧⑨⑩⑪ Brief/Draft/Asset/Review/Adapt | Producer | 看推荐成品/比稿/审核 |
| 5 | **增长与评估** | ⑬⑮⑯ 真相/Evaluation/Learning | Strategist | 看「什么有效+下一步」 |
| 6 | **反馈** | ⑭ Feedback（归一化后） | Channel Operator | 看线索/投诉处理 |
| 7 | **渠道** | ⑫ + 渠道原始数据/采集 | Channel Operator | 选渠道/看 per-Account 真相/发布 |

**组合理由**：
- ①③合并：Signal→Opportunity 是同一「情报」对象的上下游，员工同是 Research&Intel，CEO 深究时才分。
- ④⑤合并为「选题」：判断（⑤）本身就是选题池的高价值卡，且含 CEO Gate，不应拆成两个 Surface。
- ⑦⑧⑨⑩⑪合并为「内容」：Brief→草稿→素材→审核→适配是同一 Producer 的连续创作链路，用户在此比稿/审核；Calendar 作为此 Surface 内的视图（OPEN QUESTION Z1/Z7）。
- ⑬⑮⑯合并为「增长与评估」：数据真相→评估→学习是同一归因闭环。
- ⑭独立「反馈」：它是收件箱型工作面，进入情境特殊（处理评论/私信/线索）。
- ⑫+渠道原始独立「渠道」：CHANNEL 专属，用户仅 awareness 时进入。

> 全部 Surface 遵守 Frozen 不变量：只声明 Responsibility Requirement，不绑 Employee、不新 Runtime `[CURIS-AUTH]`。

---

## 5. Utility（回答本轮 §17）

Utility = 右栏按需详情，承载「drill-down」而非「常驻」。

**应承载**：
- Evidence（证据链 / 来源 / 强度）
- Source（监控源健康度）
- Employee Quick Detail（点员工名→速览；点对话→Direct Conversation；看正在做什么→Current Work）`[CURIS-AUTH §18 三入口]`
- Topic Detail / Research Detail
- Preview（草稿/素材预览）
- Comparison（变体对比 / A/B）
- Channel Detail（平台规则 / 账号状态）
- Publish receipt（发布回执，来自 Connector）

**不应进入 Utility**（更不应进 Main）：
- 全量 Signal 池、全量选题库、裸 Analytics Dashboard、编辑画布。

---

## 6. Channel 在产品里的出现方式（回答本轮 §7/§11/§26-Q7）

XHS / Douyin 降为 **Channel** 后，在产品中以下列形式出现，**不默认做成 XHS Tab / Douyin Tab**：

| 形式 | 何时出现 | 用户感知 |
|---|---|---|
| **Channel switch** | 用户主动切渠道 / 多渠道操作时 | 轻量切换，非主导航 |
| **Publishing target** | 发布阶段选账号 | 「发布到 XHS + 抖音」 |
| **Channel-specific Module** | 格式适配/平台分析/渠道反馈 | 后台自动，用户多不感知 |
| **Context filter** | 当当前任务与某渠道强相关 | Context 栏显示当前 Channel/Account |

**系统自动处理 vs 用户感知**：
- 格式适配/发布执行/数据回收/合规防封 → **系统后台自动**（Channel Operator + Connector）。
- 用户仅在 **选渠道、看 per-Account 发布真相、处理渠道反馈、渠道权限未就绪** 时意识到 Channel。
- 诚实表达渠道能力状态（§12）：Connected / Not Connected / Unavailable / Needs Permission / Failed。

---

## 7. Quick / Structured / Deep 体验（回答本轮 §14/§15/§26-Q8/Q9）

### 7.1 Quick Path（保留最简单）
- 用户说：「帮我写一篇 GPT-5.6 小红书笔记。」
- 系统：自动判为单条/低 stakes → **Quick**（对话→直接生成→单 Channel 适配→Human-in-the-loop 发布）。
- 用户**停留 Conversation**，不离开、不选模式、不学 Workflow。

### 7.2 升级判定（AI 决定复杂度，用户只见状态）
系统按 价值×复杂度×合规×跨渠道 自动选路径（Unit Economics L0/L1/L2）：
- 检测到多平台/品牌一致/合规敏感/需测量迭代 → 升级 **Structured**（后台创建 Brief/审核/回收 Work）。
- 检测到经营资产/复利/跨渠道规模 → 升级 **Deep**（持续监控+Research+跨渠道+Learning）。

### 7.3 升级时如何不增加负担（非阻塞提示）
- 系统以一条轻提示呈现升级理由与价值，例如：
  > 「这个主题值得先做调研，预计会复用到 3 个渠道。需要我深入吗？」
- 用户只需：**继续 / 直接生成 / 讨论**——三选一，不展示 16 阶段内部流程。
- 若用户选「直接生成」→ 降级 Quick，不强制闭环。

### 7.4 原则
> 不让用户选择 Workflow；AI 决定复杂度，用户只见必要状态与结果。

---

## 8. Context 行为（回答本轮 §16）

Context 不是「把所有 Surface 永久列满」，而是**按当前任务呈现**：
- **默认收起**：进入驾驶舱时，仅显示 Workspace identity + 必要专业导航（7 Surface 入口）。
- **展开**：用户点击某 Surface / 进入专业工作时展开该 Surface 导航 + 业务空间树。
- **切 Channel**：当前任务与某渠道强相关时，Context 显示当前 Channel/Account 过滤。
- **显示 Topic / Research scope**：当处于研究/选题工作流中，Context 显示当前范围（选题/研究问题/Scope）。
- 收起/展开由用户动作或当前 Work 上下文驱动，不常驻全量。

---

## 9. 给后续 UI 研究的输入（非本研究交付）
本模型定义的「驾驶舱 8 类型 + 排序/生命周期」「Projection 信息合同 11 字段」「7 Surface 组合」「Utility 边界」「Channel 4 形式」「Quick/Structured/Deep 升级提示」可作为后续 **IA / 低保真结构稿** 的消费真源。本研究**不画页面、不改 Figma、不写前端**。

---

*CONTENT GROWTH PRODUCT EXPERIENCE MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
