# CONTENT GROWTH — CEO OPERATING STATE MODEL
### 从复杂经营状态 → 小白 CEO 可理解的工作状态（不新增功能 · 不画 IA / Wireframe / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority）

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）

Companion: `CONTENT_GROWTH_CEO_DAILY_SIMULATION.md`（用连续 5 天证明本模型真实可运营）
前置：Round 4 `CONTENT_GROWTH_AI_EMPLOYEE_DECISION_MODEL.md`（Confidence / Progressive Investment / Strategy Envelope / Learning）+ `CONTENT_GROWTH_AUTONOMOUS_OPERATING_CASE.md`；Round 3 `CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md`（三句话责任 / A·B·C·D·E）+ `CONTENT_GROWTH_CONFIGURATION_OWNERSHIP_AUDIT.md`；Round 2 `CONTENT_GROWTH_ONBOARDING_AND_DAILY_OPERATING_MODEL.md`（驾驶舱 8 类 / 7 Surface / 三深度）；Frozen `Curis_Content_Growth_Domain_Authority.md`。

---

## 0. 本轮纪律与范围

- 本轮**只研究 CEO 看到的「经营状态」如何收敛与行为**，不新增任何功能、不画 IA / Wireframe / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority。
- 后台对象全部沿用既有：`Office / Intent / Source / Signal / Opportunity / Topic / Research / Brief / Draft / Asset / Variant / Publication / Channel / Channel Account / Work / Result / Evidence / Decision / Evaluation`，团队 王颖(Research&Intel)·李想(Producer)·陈帆(Channel Operator)·周明(Strategist)。
- **消费 Frozen 不变量**（不重定义）：`OAUTH_FAILURE_KEEPS_ACCOUNT` / `TARGET_NE_ELIGIBILITY` / `PUBLICATION_PER_ACCOUNT_TRUTH` / `FACT_NOT_ROLLED_BACK` / `NO_CROSS_ACCOUNT_CONTEXT_LEAK` / `INTENT_EXCLUDES_INFERENCE` / `RECEIPT_FROM_CONNECTOR` / `UNKNOWN_IS_LEGAL` / `SCHEDULING_IS_CONDITIONAL`。
- 核心命题：后台越复杂，前台越简单。**本模型定义的是「CEO 视角的状态与信息合同」，不是页面布局**——任何「UI 阶段再决定」的缺口都视为本轮不合格。

---

## 1. 最高原则

CEO 默认界面**不展示业务系统结构**（不看 Work 队列 / Signal 池 / 状态机 / Binding）。

CEO 主要看到：

```
发生了什么
员工得出了什么结果
现在正在做什么
有什么值得关注
是否需要我决定
是否需要我执行不可替代的动作
下一步建议是什么
```

后台的所有 `Work / Result / Evidence / Decision / Employee / Research / Content / Publication / Evaluation / Error`，经两层压缩后投影为少量 CEO 状态：

1. **Result Projection**（§4）：复杂 Employee 结果 → 一句业务语言。
2. **Operating State**（§2）：投影后的对象按「是否需要 CEO 注意/行动」归入 8 个状态之一。

---

## 2. 最终 Operating State 分类（8 态收敛）

### 2.1 候选 A–H 的研究结论

用户给出的候选 A–H 经研究**全部保留，不合并、不拆分**，恰好 8 态，且每态行为边界清晰、无重叠：

| 态 | 名称 | 一句话定义 | 谁需要 CEO |
|---|---|---|---|
| **S1** | QUIET 正常运行 | 没有需要 CEO 关注的事 | 否（系统自己跑） |
| **S2** | RESULT 新结果 | 员工完成了一项有价值的工作 | 否（看即可） |
| **S3** | WATCH 值得关注 | 发现机会/变化/风险，暂不需决策 | 否（知情即可） |
| **S4** | DECISION 需要决定 | 重大方向 / 相关 Gate 需 CEO | **是（判断）** |
| **S5** | IN_PROGRESS 正在进行 | 重要工作在跑，CEO 只需知状态 | 否（等即可） |
| **S6** | READY 成品就绪 | 内容/方案已准备好，可查看 | 否（看即可） |
| **S7** | ACTION_REQUIRED 等待用户动作 | OAuth / 发布确认等 AI 无法代替 | **是（点击）** |
| **S8** | ALERT 异常 | 失败 / 掉线 / 驳回 / UNKNOWN 阻塞 | 视情况（多需关注） |

**为什么不合并 G 进 D**：D 要的是「判断」（战略方向，给 批准/调整/讨论/暂停 四选一）；G 要的是「点击一次」（重授权、确认发布，无判断空间）。行为不同，必须分态，否则会把「确认发布」误渲染成「需要你决策」而惊动 CEO。

**为什么不合并 A 进其他**：QUIET 是**正常产品状态**，不是「空」。没有它，系统会为了「不空」而制造假 KPI / 假推荐（用户 §8 明令禁止）。

### 2.2 与 Round 2 驾驶舱 8 类的 Reconciliation（消除矛盾）

Round 2 `ONBOARDING_AND_DAILY_OPERATING_MODEL.md` 的驾驶舱 8 类（①结果 ②重点 ③需关注变化 ④需决定 ⑤在途 ⑥发布 ⑦增长 ⑧推荐）是**投影内容类型**；本轮 8 态是**行为状态（带生命周期/优先级/注意力）**。二者不冲突，后者为权威行为层，前者被吸收映射：

| Round 2 驾驶舱类 | 归入本轮 Operating State | 说明 |
|---|---|---|
| ①结果 / ⑦增长 | **S2 RESULT** | 研究完成、增长评估都属「员工产出值得看的结果」 |
| ②重点 / ③需关注变化 | **S3 WATCH** | 机会、变化、风险，暂不需决策 |
| ④需决定 | **S4 DECISION** | 战略 Gate |
| ⑤在途 | **S5 IN_PROGRESS** | 研究进行中、平台审核中 |
| ⑥发布（待确认） | **S7 ACTION_REQUIRED** | 发布确认是 AI 无法代做的点击 |
| ⑥发布（已就绪未发） | **S6 READY** | 内容可发布，待 CEO 看 |
| ⑧推荐（选题/下一周期） | **S2 或 S3** | 推荐选题=新结果(S2)；推荐方向=值得关注(S3) |

> 结论：Round 2 的 8 类 ≠ 本轮 8 态是「不同分类维度」，旧 8 类在投影层仍可作卡片视觉分组，但**状态机行为以本轮 8 态为准**。无矛盾。

---

## 3. 每种状态的信息合同（统一 15 问）

> 下列 8 态逐条回答用户 §3 的统一问题。同一对象（如一个 Topic）跨 8 态是**不同投影深度**，数据不复制（消费 Round 2 Product Experience §4.6）。

### 3.1 S1 QUIET 正常运行

- **为什么出现**：当前无 S2–S8 任何需要 CEO 注意的投影；员工在后台正常经营。
- **谁产生**：系统状态机（无新事件越过注意力阈值）。
- **对应 Curis 对象**：无突出对象；Office 运行态健康。
- **CEO 第一眼看到**：一句「团队正在正常运行，目前没有需要你处理的事情。」（可附极轻的「监控中：X 源 / Y 账号」一行，非 KPI 墙）。
- **最重要的一句话**：「一切正常，你可以离开。」
- **主动作**：无（或「查看团队」可选）。
- **次动作**：「问员工」（想了解随便问）。
- **允许问员工**：是，携带 Office 上下文。
- **默认隐藏**：所有 Work 进度、Signal 池、指标原始值。
- **查看详情进入**：无（或点「查看团队」→ 团队速览，仍非专业 Surface）。
- **什么时候消失**：出现任一 S2–S8 时自然让位。
- **什么时候降权**：不适用（本就是最低态）。
- **离开再回**：持续存在（本身就是常态投影）。
- **多条同时**：不可能（独占态）。
- **绝不打扰**：本态**绝不发通知、不弹窗**，页面静默。

### 3.2 S2 RESULT 新结果

- **为什么出现**：员工完成一项越过「价值门 + 注意力阈值」的工作（研究出结论 / 增长评估 / 内容产出 / 新选题建议）。
- **谁产生**：对应 Responsibility（王颖/李想/周明）的 Result Work 闭合。
- **对应对象**：`Result`（Research / Evaluation / Content / Topic Recommendation）。
- **CEO 第一眼看到**：压缩投影卡（见 §4），如「王颖发现一个值得做的内容机会：GPT-5.6 实测」。
- **最重要的一句话**：「员工做好了 X，结论/价值是 Y。」
- **主动作**：「查看依据」（展开为什么值得做 / 价值）。
- **次动作**：「就做这个 / 先调研 / 按建议继续 / 问员工」。
- **允许问员工**：是，自动携带该 Result + 来源 refs。
- **默认隐藏**：Evidence 明细、置信度数值、评分维度、原始指标。
- **查看详情进入**：对应 Professional Surface（研究→研究与洞察；增长→增长与评估；选题→选题）。
- **什么时候消失**：CEO 看过(SEEN)后降权；若该 Result 已派生后续动作（如已「就做这个」）→ RESOLVED→HISTORY。
- **什么时候降权**：被读后从顶部降为「已读」，仍可在历史查。
- **离开再回**：继续存在（同一 object_id 不重复建卡）。
- **多条同时**：按 §6 优先级排在 S4/S7/S8 之下、S6 之上；同类合并（如多个选题建议聚成「3 个新选题 👇」）。
- **绝不打扰**：纯内部进度（未完成 Work）**不**升 S2；仅越过价值门的结果才投影。

### 3.3 S3 WATCH 值得关注

- **为什么出现**：发现机会 / 市场变化 / 风险信号，但当前**不需 CEO 决策**，只需知情（如某对标涨粉、平台规则变动、竞品动作）。
- **谁产生**：王颖(Growth Intel) 监测 Signal/Opportunity。
- **对应对象**：`Signal`（高权重）/ `Opportunity`（未到决策）/ 外部变化 `Evidence`。
- **CEO 第一眼看到**：「OpenAI 发布新动态，3 源提及，可能影响你的选题。」
- **最重要的一句话**：「有件事你可能想知道，目前不用你做决定。」
- **主动作**：「查看依据」。
- **次动作**：「问员工」/「先调研」（若想升级为动作）。
- **允许问员工**：是。
- **默认隐藏**：Signal 原始池、聚类过程、全部 Source 命中明细。
- **查看详情进入**：信息与机会 Surface（仅当用户主动深潜）。
- **什么时候消失**：超过时效窗口（如热点已过）自动 HIDE；若升级为选题→转 S2/S6。
- **什么时候降权**：被读后降权，保留于 WATCH 历史。
- **离开再回**：继续存在。
- **多条同时**：按新颖度+业务价值排序，普通日常 Signal 多被 HIDE（§5）。
- **绝不打扰**：非紧急变化（如常规行业新闻）**不**发推送通知，仅在驾驶舱以低调条目出现。

### 3.4 S4 DECISION 需要决定

- **为什么出现**：出现 Strategy Envelope 越界 / 重大不可逆方向，需 CEO 批准（如「建议转型带货」「超预算扩渠道」）。
- **谁产生**：周明(Strategist) 判断 Envelope 外，发起 Gate（消费 Round 4 §5）。
- **对应对象**：`Decision`（Gate 类型）/ `Strategy Adjustment` 提案。
- **CEO 第一眼看到**：顶部置顶卡「需要你决定：是否把 AI 科技内容扩展到视频号？」（附 为什么 / 预计价值 / 风险 / 建议）。
- **最重要的一句话**：「有件事只有你能定，其他我都能做。」
- **主动作**：「批准 / 调整 / 讨论 / 暂停」（四选一）。
- **次动作**：「问员工」（了解决策背景）。
- **允许问员工**：是，携带 Decision Context。
- **默认隐藏**：内部评估过程；只给决策所需的最小事实。
- **查看详情进入**：策略 Surface（若 Expert 想看底层参数，须主动进）。
- **什么时候消失**：CEO 四选一后 RESOLVED→HISTORY；Gate 持续保留直到被处理（**不自动消失**）。
- **什么时候降权**：不降权——Decision 未完成始终置顶（除非被更高优先级 S7/S8 暂时插队）。
- **离开再回**：持续存在，回来仍置顶，不重复通知。
- **多条同时**：同类 Decision 合并或排队；置顶于一切 S2/S3/S5/S6。
- **绝不打扰**：仅在**真越信封**时出现；信封内微调（Round 4 D22）AI 自调，**不**升 S4。

### 3.5 S5 IN_PROGRESS 正在进行

- **为什么出现**：重要 Work 正在执行（Research 多源比对中 / 内容生成中 / 平台审核中）。
- **谁产生**：对应 Responsibility 的 Work 进行中。
- **对应对象**：`Work`（status=RUNNING）/ `Publication`（Platform Reviewing）。
- **CEO 第一眼看到**：低优先级状态条「GPT-5.6 选题研究中…」/「抖音主号平台审核中…」。
- **最重要的一句话**：「员工正在做 X，你不用管，好了会告诉你。」
- **主动作**：无（或「查看依据」看进度）。
- **次动作**：「问员工」。
- **允许问员工**：是。
- **默认隐藏**：执行细节、中间步骤、token 消耗。
- **查看详情进入**：对应 Surface（研究→研究与洞察；发布→渠道）。
- **什么时候消失**：Work 完成→转 S2（结果）/ S6（成品）；Publication 审完→转 S7/S2。
- **什么时候降权**：天生低优先级，排在 S2/S3 之后，不打扰。
- **离开再回**：继续存在（完成后再回来见对应 S2/S6 结果卡）。
- **多条同时**：合并为「N 项工作进行中」，不逐条刷屏。
- **绝不打扰**：进行中**不发通知**；仅在完成且越过阈值时以 S2 通知（一次）。

### 3.6 S6 READY 成品就绪

- **为什么出现**：内容/方案已通过员工自检、达到「可发布/可采纳」标准，等 CEO 查看或确认。
- **谁产生**：李想(Producer) 审核五项通过 / 周明 方案成形。
- **对应对象**：`Draft`（审核通过）/ `Content Intent`（Brief 完成）/ `Variant`（生成完）。
- **CEO 第一眼看到**：「内容已准备好：GPT-5.6 小红书笔记（已通过品牌/事实/合规检查）。」
- **最重要的一句话**：「员工做好了，你可以看看，满意就发。」
- **主动作**：「查看 / 发布」。
- **次动作**：「调整 / 讨论 / 问员工」。
- **允许问员工**：是。
- **默认隐藏**：版本管理细节、素材库、比稿过程（Round 3 已降 EXPERT ONLY）。
- **查看详情进入**：内容 Surface（深度比稿仍 EXPERT）。
- **什么时候消失**：CEO 点「发布」→ 转 S7（确认）/ 发布后转 S2（结果）。
- **什么时候降权**：被读后降权，保留历史。
- **离开再回**：继续存在（同一 Draft id）。
- **多条同时**：多个就绪内容聚成「N 篇内容已就绪 👇」。
- **绝不打扰**：就绪本身**不**弹通知；若同时需发布确认则借 S7 一次提示。

### 3.7 S7 ACTION_REQUIRED 等待用户动作

- **为什么出现**：出现 AI **无法代为执行**的机械动作——OAuth 重授权 / 发布确认（Human-in-the-loop）/ 必要外部授权。
- **谁产生**：陈帆(Channel Operator) 检测到授权态 / 发布流程到确认点；触发 Round 4 §8 红线（D 类 / Human-in-loop）。
- **对应对象**：`Channel Account`(authorization_state=Expired/Needs Permission) / `Publication`(Needs Permission) / `OfficeAccountBinding`。
- **CEO 第一眼看到**：明确的「需要你点一下」卡 + 单一按钮：
  - 授权失效：「抖音主号授权已过期，点此重新授权（约 10 秒）。」
  - 发布确认：「内容已就绪，确认发到 小红书主号+抖音主号？（预计今晚 20:00/21:00）」
- **最重要的一句话**：「这一步只能你来，点一下就好，其他我做完。」
- **主动作**：唯一按钮——「重新授权」/「确认发布」。
- **次动作**：「调整」（改发布目标，进 EXPERT 或回 S6）。
- **允许问员工**：是。
- **默认隐藏**：授权令牌细节、Connector 内部、逐账号精调（EXPERT）。
- **查看详情进入**：渠道 Surface（仅 Expert）。
- **什么时候消失**：CEO 点击后（OAuth 成功 / 发布确认）→ 转对应态（S5 发布中 / S2 结果）。
- **什么时候降权**：不降权直到动作完成；若 CEO 暂不选，保持待办（但可折叠）。
- **离开再回**：持续存在，回来仍在；不重复通知已存在的待办。
- **多条同时**：按影响排序（阻断发布的授权失效 > 普通确认）；可批处理。
- **绝不打扰**：**仅此态与 S4 可主动提示**（因需 CEO 物理动作）；但提示克制——一次，不重复弹。

### 3.8 S8 ALERT 异常

- **为什么出现**：出现失败 / 掉线 / 平台驳回 / UNKNOWN 阻塞等异常（如发布部分失败、账号掉线、Research 无结论、Analytics 拉取失败）。
- **谁产生**：对应 Responsibility 检测到异常（消费 Doc 5 ERROR RECOVERY 14 类）。
- **对应对象**：`Publication`(Failed/Rejected) / `Channel Account`(Offline) / `Research`(Unknown/Conflict) / `Work`(Failed)。
- **CEO 第一眼看到**：诚实状态，绝不伪造整体成功（Frozen `PUBLICATION_PER_ACCOUNT_TRUTH`）：
  - 「部分完成：小红书已发布 ✅，抖音发布失败（网络超时）。」
  - 「抖音主号被平台驳回：疑似含未标识的 AI 生成内容，已标出需修改处。」
- **最重要的一句话**：「有件事没按预期走，我已处理/或需要你知。」
- **主动作**：「查看 / 重试 / 改后重提」（依异常类型）。
- **次动作**：「问员工」。
- **允许问员工**：是。
- **默认隐藏**：堆栈、内部错误码（除非 Expert）。
- **查看详情进入**：渠道 Surface（发布失败）/ 研究与洞察（Research 异常）/ 反馈 Surface（驳回原因）。
- **什么时候消失**：修复后转 RESOLVED→HISTORY（如失败重试成功→S2 结果；驳回改后重提→S5）。
- **什么时候降权**：恢复中降权；未恢复保持可见。
- **离开再回**：持续存在，回来仍可见真实状态。
- **多条同时**：按严重度（阻断 > 部分失败 > 可自愈）；同一对象异常不重复建卡。
- **绝不打扰**：异常**诚实呈现不刷屏**；可自愈的轻微异常（如某 Source 临时失效 AI 已自动换源）**不**升 S8，仅记日志。

---

## 4. RESULT PROJECTION（压缩规则）

### 4.1 统一候选结构

任何复杂 Employee Result，投影到 CEO 时默认只给 7 字段（按需展开其余）：

```
谁完成的         → 王颖 / 李想 / 陈帆 / 周明
结论             → 一句话业务结论
这意味着什么     → 对经营目标的相关性
价值             → 预计价值（涨粉/接广告路径/互动）
风险 / Unknown   → 仅当值得 CEO 知（如合规、平台变量）
建议下一步       → 员工建议 CEO 做什么（或「无需你做」）
是否需要 CEO    → 是(转S4/S7) / 否(转S2/S3/S5/S6)
```

### 4.2 压缩示例（后台 → 前台）

| 后台（大量） | CEO 看到（S2 投影） |
|---|---|
| 300 Signals / 20 Sources / Research Work / 12 Evidence / Confidence=HIGH / Topic Score=0.82 | 「王颖发现一个值得做的内容机会：GPT-5.6 办公实测。为什么值得：3 源提及+切搜索红利。预计价值：高互动。建议：先调研或就做这个。」 |
| 周明 Evaluation：收藏率↑12%、涨粉 +340、归因=第一手实测 | 「上周评估：收藏率↑12%，建议继续并扩抖音。」 |
| 李想生成 3 版 Draft + 2 封面，过审核五项 | 「内容已准备好：GPT-5.6 小红书笔记（已过品牌/事实/合规）。」 |

### 4.3 压缩纪律

- **不丢真相**：压缩是「隐藏细节」不是「编造」。CEO 点「查看依据」可下钻到完整 Evidence（Frozen `UNKNOWN_IS_LEGAL` 允许标 Unknown 不填充）。
- **不刷屏**：一个 Result 一个卡；同类聚并（3 选题=1 卡带展开）；内部中间 Work **不**投影（§5 HIDE）。
- **价值门前置**：只有越过 Round 4 §4 价值门的 Result 才进投影；低价值结论留库，不惊动 CEO。

---

## 5. ATTENTION MODEL（SHOW / DOWNRANK / HIDE / NOTIFY）

不是每个 Work 完成都变 CEO 消息。四维判定后归类：

| 规则 | 触发条件 | 行为 |
|---|---|---|
| **SHOW** | Importance 高 ∩ (BusinessValue 高 ∪ NeedCEO ∪ Risk 高 ∪ Novelty 高) | 投影为 S2/S3/S4/S7/S8，可进通知 |
| **DOWNRANK** | 已被读(SEEN) ∪ 低 Novelty(重复类) ∪ 例行 | 保留但降序、折叠，不通知 |
| **HIDE** | 纯内部进度(未完成 Work) ∪ 低价值 Signal ∪ 例行监控 tick | 不投影，仅留专业层/日志 |
| **NOTIFY** | 仅当新事件从 HIDE/DOWNRANK **跨越**到 SHOW（新 Decision / 新 Alert / 新高价值 Result） | 一次轻提示；不重复 |

**八维权重（判定 SHOW 与否）**：Importance / Urgency / BusinessValue / Risk / NeedCEO / Novelty / Confidence / AlreadyRead。
- `AlreadyRead=true` → 强制 DOWNRANK（不重复提醒）。
- `Confidence=LOW/UNKNOWN` 且非风险 → 多 HIDE（不拿不确定结论打扰）。
- 例行「监控中」「账号正常」→ HIDE（永不 NOTIFY）。

**核心禁令**：员工每次完成 Work **不**自动成 CEO 消息。只有「越过价值门 + 注意力阈值」的结果才 SHOW+（可能）NOTIFY 一次。

---

## 6. PRIORITY（多条共存排序）

排序服务「**现在最值得 CEO 关注什么**」，**不**按数据库时间倒序。

```
Tier 1 — 需要 CEO 现在介入（置顶）
  S4 DECISION      （战略 Gate，不可推）
  S7 ACTION_REQUIRED（机械动作，需点一次）
  S8 ALERT         （失败/驳回/掉线，需关注）
Tier 2 — 需知情（中优先级）
  S3 WATCH         （机会/变化/风险）
  S2 RESULT        （有价值结果）
  S6 READY         （成品就绪待看）
Tier 3 — 被动（最低）
  S5 IN_PROGRESS   （进行中，仅状态）
  S1 QUIET         （无事项，独占底态）
```

**用户示例 6 条共存时的真实顺序**：
1. S4「是否扩视频号」（Strategy Decision，置顶）
2. S7「抖音主号授权过期，点此重授权」（阻断发布，需点）
3. S8「小红书发布失败（网络）」（需关注）
4. S3「OpenAI 新动态，3 源提及」（值得关注）
5. S2「研究完成：GPT-5.6 值得做」（新结果）
6. S2「增长建议：收藏率↑12%」（新结果）
7. S5「抖音主号平台审核中」（进行中，最底）

CEO 第一眼 = S4；最底 = S5。非时间序。

---

## 7. LIFECYCLE（每条 CEO 投影的生命周期）

```
NEW      刚出现，未读（可能触发一次 NOTIFY）
  ↓ CEO 打开/看到
SEEN     已读 → DOWNRANK（降序保留，不消失）
  ↓ CEO 做主/次动作
ACTED    CEO 已响应（确认/调整/发布/重授权）
  ↓ 工作闭环
RESOLVED 事项完成（决策落定/发布成功/异常修复）
  ↓ 自动归档
HISTORY  进入历史（按需查，不在驾驶舱常驻）
```

**关键纪律**：
- 已读 → **降权不消失**（避免「看了就丢」导致遗忘）。
- Decision(S4) → **持续保留直到 ACTED**，不自动消失（防漏决）。
- Alert(S8) 修复后 → RESOLVED→HISTORY，不残留红色。
- 同一对象更新 → **替换原卡**（按 object_id 幂等），不新建重复卡（如 Research 从 S5→S2 只变状态不增卡）。
- 用户离开再回 → 不重复 NOTIFY 已存在的 NEW 项；已 SEEN 项保持降权。

---

## 8. QUIET STATE（正常产品状态）

- 当无 S2–S8 时，默认投影 = **S1 QUIET**：「团队正在正常运行，目前没有需要你处理的事情。」
- 可附一行极轻上下文（非 KPI 墙）：「监控中：5 个网站 · 3 对标 · 8 账号」。
- **严禁**为「不空」而制造 Dashboard / KPI 墙 / 假推荐 / 重复状态 / 无意义通知。
- Quiet 本身是一种**健康状态**，不是「系统坏了」或「没事做」。

---

## 9. ASK EMPLOYEE（与员工交流的关系）

每态都允许「问员工」，且**自动携带当前上下文**（不要求用户重述背景）：

- 携带内容：当前 Result / Topic / Research / Evidence refs / 当前 Decision Context / 所属 Office。
- 入口维持三入口模型（Round 3 / Round 2）：**直接对话 / 当前工作 / 员工资料**。
- 示例：S2「王颖发现机会」→ CEO 点「问王颖」→ 对话自动带该研究结论+Evidence 引用，CEO 只需说「这个结论我不太信，再查查社区」。

---

## 10. DEEP-DIVE（为什么 / 依据按需下钻）

每种 Operating State 默认**不展示专业复杂度**；CEO 点「查看依据」才进对应 Professional Surface（Round 2 七 Surface）：

| 态 | 默认隐藏 | 下钻到 Surface |
|---|---|---|
| S2 RESULT（研究） | Evidence 明细/置信 | 研究与洞察 |
| S2 RESULT（增长） | 原始指标/归因 | 增长与评估 |
| S2/S3 选题 | 评分维度/去重 | 选题 |
| S3 WATCH | Signal 池/聚类 | 信息与机会 |
| S4 DECISION | 内部评估过程 | 策略（Expert 才见底层参数） |
| S5 IN_PROGRESS（研究） | 执行步骤 | 研究与洞察 |
| S5 IN_PROGRESS（发布） | 逐账号态 | 渠道 |
| S6 READY | 版本/比稿/素材库 | 内容（比稿 EXPERT） |
| S7 ACTION_REQUIRED | 令牌/Connector | 渠道（EXPERT） |
| S8 ALERT | 错误码/堆栈 | 渠道 / 研究与洞察 / 反馈 |

下钻后可随时「返回经营」回驾驶舱，Context 不丢。

---

## 11. STRATEGY ENVELOPE 产品规则（不变成配置页）

Strategy Envelope **不是小白配置页**，它由以下自然形成（消费 Round 4 §5）：

```
CEO 自然语言（「先涨粉，以后接广告」）
+ CEO 确认过的建议（「小红书+抖音先做」→ 批准）
+ Decision（Gate 结果）
+ 用户真实 Constraint（预算/时间/是否露脸）
        ↓ 累积
当前经营边界（Envelope）
```

- 普通 CEO **只看到「已确认的方向」一句话**（如「当前：涨粉为主，暂接广告；主发小红书+抖音」），不看到可调参数。
- 仅 **Expert** 主动进策略 Surface 才可见/调整底层维度（Goal / Channel family / Budget / Risk tolerance）。
- Envelope 内微调 AI 自调（Round 4 D22），**不**升 S4；仅越信封才 S4 Gate。
- 反例禁止：不让小白在「策略页」自己拖滑块设「涨粉权重 0.7」。

---

## 12. QUICK PATH 交叉校验

用户突然说「帮我写篇 GPT-5.6 小红书。」：
- **不进入 Operating State 流程**：不走 S2/S3/S6 选题池（消费 Round 3 §7 / Round 2 Journey H）。
- 走 `Conversation → Result（成稿）→ 一句修改 → 发布建议(S7 一次确认)`。
- 完成后该成稿**可自然进经营历史**（HISTORY），但**不污染** Quick 体验（不弹 S2/S3 卡、不要求进驾驶舱）。
- 证明：Quick Path 与 Operating State 模型正交——State 模型服务「持续经营投影」，Quick Path 服务「一次性对话成稿」，二者互不打扰。

---

## 13. ACCEPTANCE 15 问逐条回答

| # | 验收问题 | 本模型回答位置 |
|---|---|---|
| 1 | CEO 每天打开第一眼看什么？ | §6 优先级：S4/S7/S8 置顶（若有），否则 S3/S2/S6，否则 S5，否则 S1「一切正常」。 |
| 2 | 没事的时候看什么？ | §8 S1 QUIET：「团队正常，无事项」。 |
| 3 | 员工完成普通 Work 为何不刷屏？ | §5 HIDE + §4.3：内部进度不投影，仅越价值门的结果 SHOW，且一次 NOTIFY。 |
| 4 | 什么 Result 值得出现？ | §4.3 + §5 SHOW：越 Round 4 价值门 ∩ 注意力阈值。 |
| 5 | 什么情况必须置顶？ | §6 Tier1：S4/S7/S8 置顶。 |
| 6 | 多条信息怎么排序？ | §6 优先级（非时间序）。 |
| 7 | 已处理信息怎么消失？ | §7：ACTED→RESOLVED→HISTORY，驾驶舱不再常驻。 |
| 8 | 在途工作如何存在但不抢注意力？ | §3.5 S5：低优先级状态条，完成才转 S2 一次通知。 |
| 9 | 异常怎么出现？ | §3.8 S8：诚实 per-account 真相（Frozen `PUBLICATION_PER_ACCOUNT_TRUTH`），不伪造整体成功。 |
| 10 | Decision 怎么持续等 CEO？ | §3.4 + §7：S4 不自动消失，置顶至 ACTED。 |
| 11 | 为什么/依据如何按需下钻？ | §10 DEEP-DIVE：每态映射到 Surface，默认隐藏专业层。 |
| 12 | 如何直接问负责员工？ | §9：每态「问员工」自动携带上下文，三入口模型。 |
| 13 | Strategy Envelope 为何不是配置页？ | §11：由自然语言+确认+Decision+Constraint 自然形成，仅 Expert 见底层。 |
| 14 | Quick Path 为何仍简单？ | §12：正交，不进 State 流程，成稿自然入历史不污染。 |
| 15 | 用户能否一眼知道「公司在干啥+我现在要干啥」？ | **能**：驾驶舱顶部 = 需我做的（S4/S7/S8）+ 需我知的（S3/S2/S6）+ 在做的（S5）；S1 时明确「无需你做」。一句话状态总览可加：「今天：1 件需你确认，2 件已就绪，3 项进行中。」 |

---

*CONTENT GROWTH CEO OPERATING STATE MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
