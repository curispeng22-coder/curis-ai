# CURIS OPERATING INTELLIGENCE — ANALYTICS UX & PAGE EXPLORATION

**Authority Class**：RESEARCH  
**Disposition**：CONSUMED BY CURRENT PRODUCT TRUTH（Operating Intelligence UX Baseline → Product Blueprint 5.3 / Master Map 3.0 / UI Blueprint）  
本文保留研究过程；旧的导航占位建议不再是 Current 规则。

**日期**：2026-08-18
**类型**：Analytics UX / 页面信息架构研究（Operating Intelligence）
**参与**：智数分析专家团（主理人诺亚 Nova）
**状态**：研究完成 · ANALYTICS UX RESEARCH COMPLETE · STOP FOR CEO VISUAL REVIEW

> ⚠️ 团队协作说明：当前会话无 `TeamCreate` 原语，`Agent` 工具被团队门禁整体拦截，无法拉起专家子团队。主理人诺亚按五位成员视角（sql/data-science/knowledge/dashboard/report）直接执行并汇编，保留"专业分析 + 主理人编排"的协作实质。本研究过程未修改 Current Product Truth；其已确认结论现已由 Final Product Architecture Delta 消费，不把 Research 升格为独立 Authority。

---

## 0. 输入与边界（已确认，不重新讨论）

- 前置研究 `CURIS_OPERATING_INTELLIGENCE_RESEARCH.md` = **研究方向**，不是 Current Authority。
- Research-time Current Truth = Blueprint v5.3 + Master Map v3.0 + UI Blueprint（已消费为经营洞察合同）。
- Recovery Audit = **ACCEPTED Recovery Baseline**（已读；V1 / Later / LATER 分类、经营内核保留清单）。
- Derivation / Reasoning = 经营逻辑来源，非 Authority。
- 已确认方向：统一命名"经营洞察 / Operating Intelligence"；Company OS 是事实源；Shared + Domain Metrics；Fact 与 Interpretation 分离；新 Business 自动进入；CEO Desk 与经营洞察边界分明；经营洞察不是第二套 Business Editor。

---

## 1. CEO Analytics Mental Model（CEO 分析心智模型）

CEO 不会想"我要配一个 Dashboard 看 retention funnel"。他会想：

> 1. 我的公司现在经营得**怎么样**？
> 2. **为什么**会这样（变好 / 变坏）？
> 3. 哪个 **Business / Department / Role / Employee / Model** 表现不同？
> 4. 哪些事**值得我深入分析**？
> 5. 我接下来该**看什么、问什么、决定什么**？

因此系统语言必须是**经营语言**，不是 BI 语言：
- 不说"维度 / 度量 / 切片"，说"看哪个业务 / 比哪个模型 / 这段时间"。
- 不说"报表"，说"小红书这周的经营情况"。
- 首屏给**结论与信号**，不是图表网格。
- 任何数字都能一句话回答"它从哪来、是不是最新的、我能不能信"。

---

## 2. Information Architecture（信息架构）

### 2.1 Scope 不堆成一级 Tab
分析对象（Company / Department / Business / Workspace / Role / Employee / Workflow / Model / Agent / Provider / Capability / External Channel / Time）**不做成一级导航**。采用：

- **Scope Rail（范围栏）**：左侧或上下文栏选择"看什么对象"，默认 Company。
- **Context Bar（上下文条）**：显示当前 Scope + 时间范围 + 对比基准，随下钻变化。
- **动作**：Filter（筛选）/ Segment（分段）/ Compare（对比）/ Drill-down（下钻）/ Cross-filter（联动过滤）/ Time range / Period comparison / Search（搜 Business/Employee/Metric）。
- **下钻链**：Company → Department → Business → Workspace / Execution / Result。

### 2.2 第一屏信息层级（§二/A 答案）
首屏只给 CEO 三类信息：

| 层级 | 内容 | 呈现 |
|---|---|---|
| **必须首屏** | 公司一句话经营概况 + 关键信号（成本/产出/质量/外部结果概要） | 顶部状态行 + 2-3 张结论卡 |
| **必须首屏** | Business 表现列表（带状态，不是图海） | 卡片/列表，点开下钻 |
| **必须首屏** | 时间范围切换（默认 30D）+ 最近分析报告入口 | 上下文条 + 入口 |
| **下钻才显示** | 单 Business 的 Domain Metrics、Workflow 表现、Employee 贡献 | 进入 Business 后 |
| **仅异常时出现** | 重要变化 / 风险（正常时折叠，不占首屏） | 异常徽标 + 展开 |

**原则**：首屏 ≤ 6 个信息块；图表是下钻的结果，不是入口。

---

## 3. Company Analysis（公司分析）

CEO 看到：公司整体运行、Business 数量与表现、产出、成本、质量、外部结果、Failure/Retry/Rework、组织负载、风险变化、时间趋势。

**禁止**无依据 Company Health Score。改为：
- 用**多张结论卡**分别呈现"成本 / 产出 / 质量 / 外部结果"，每张卡带趋势箭头 + 可信度。
- "风险变化"只在出现偏差时显示，并链到对应 Business / Employee。
- 时间趋势用单图（如成本 vs 产出双轴），不堆多图。

---

## 4. Business Analysis（业务分析）

点击 Business 后理解：Goal、当前经营结果、Shared Metrics、Domain Metrics、External Result、Cost/Usage、Workflow 表现、Employee/Role 贡献、Result Quality、Review/Rework、时间趋势、Report、最近变化。

**下钻自然性**：Company 列表 → 点 Business → Business 主页（Goal+结果+Shared+Domain）→ 下钻到 Workspace / Execution / Result（跳回原产品入口，不在 Insights 内编辑）。

---

## 5. Organization / Employee Analysis（组织与员工分析）

表达：Department / Role / Employee / Staffing / Capacity / Load / Vacancy / Workload / Cost / Quality / Rework / Result。

**红线**：
- **Capability ≠ Capacity**：有能力不代表有可用容量；展示 Load / 供给缺口，不做企业级资源计划软件。
- **执行次数多 ≠ 表现好**：必须结合 Quality / Acceptance / External Result / Rework 判断；次数仅作工作量信号，不自动给"优秀员工"结论。
- Vacancy（空岗）与 Overload（过载）是组织信号，链回招聘/组队入口。

---

## 6. Model / Agent Benchmark UX（模型/智能体基准 — 重点）

为 CEO 设计**可读的比较页**：同一 Role / 同类 Task 下比较 GPT / Claude / Gemini / Codex / 其他 Provider 的 Duration / Token / Cost / Failure / Retry / Human Intervention / Review Pass / Rework / CEO Acceptance / Result Quality / External Business Result。

**Comparability 面板（必须显示样本为何可比）**：
- 锁定维度：Role / Task Type / Workflow Stage / Business / Complexity / Context / Capability / **Sample Size**。
- **样本不足**：当可比样本 < 阈值，明确显示"样本不足，暂不比较"，而非给出可疑结论。
- **禁止**无依据"最佳模型排行榜"：只做联合指标呈现（如"Claude 成本低 18%、一次通过率高 12%、耗时高 8%"），不排单一名次。

---

## 7. Domain Metric UX（域指标共存 — §八）

**小红书**：Shared（Duration/Cost/Result/Review/Employee/Model）+ Domain（曝光/阅读/点赞/收藏/评论/涨粉/转化）。
**Curis 研发**：Shared + Domain（Build/Test/Defect/Review Cycle/Release）。

**统一产品感的做法**：
- 同一个产品外壳（Scope Rail / Context Bar / 时间 / 报告 / Analyst）不变。
- Shared Metrics 永远在上方"通用区"；Domain Metrics 在下方"本业务区"，标注来源（如"小红书平台回执"）。
- CEO 切换 Business 时，只换 Domain 区内容，外壳与操作完全一致 → **不会觉得每个 Business 是一套不同 BI 软件**。
- Domain Metric 默认 `comparable=false`，跨业务比较时显式提示"口径不同，不强行对比"。

---

## 8. AI Analyst UX（AI 分析师 — §九）

**不是右下角聊天机器人**。它继承当前 Scope，作为分析主面的一个常驻能力：

- 当前 Scope 自动继承（在 Business 内问，就基于该 Business）。
- 预设动作：「解释这个变化」「为什么下降？」「比较这两个 Business」「比较两个 Model」「生成专项分析」「有哪些数据不足？」「给我看证据」「形成报告」。
- 回答**结构化**为四段：**FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION**，每段可下钻到原始来源。
- 禁止把 INTERPRETATION 伪装成 FACT；UNKNOWN 必须明示。

---

## 9. Report UX（报告体验 — §十）

报告类型：Daily / Weekly / Monthly / Business / Department / Model Benchmark / Cost Efficiency / Anomaly / Industry Research / Competitor Research / Custom。

**不是普通文档列表**。每张报告卡显示：Scope / Period / Author Employee / Facts / Findings / Unknown / Evidence / Recommendation / Created At / Model-Agent provenance。

可动作：查看来源 / 与 Analyst 继续讨论 / 召开 Meeting / 进入 Decision / 回到 Business。报告是**可追溯的 Result / Asset**。

---

## 10. Proactive Insight UX（主动洞察 — §十一）

系统发现 Cost 突升 / Result 下降 / Rework 增加 / Employee 阻塞 / Role 过载 / External 异常 / Model 切换后变化。

**分工（关键）**：
- **CEO Desk** 负责"值得现在打扰 CEO" → 轻量提醒（注意力层）。
- **经营洞察**负责"完整分析" → 在 Insights 内有一节"重要变化"，点开是完整归因与证据。

**禁止**复制两个 Alert Center。推荐：信号在 CEO Desk 以注意力形式出现；同一信号在 Insights 内有完整分析页，二者共享同一事件源，不重复生成。

---

## 11. Data Trust UX（数据真实性 — 重点 §十二）

CEO 需轻松理解 Source / Freshness / Verified / Manual Entry / Unknown / Stale / Missing / Late / Conflicting。

**做法**：
- 不铺满技术标签。每个指标旁一个**轻量可信度标识**（如小圆点 + hover/展开显示来源与时间）。
- 提供"数据可信度"展开面板：来源系统 / 最后更新 / 是否人工补录 / 是否缺失/过期/冲突。
- External Source unavailable → 显示"待连接 / 无数据"而非 0 或空。
- Manual Entry → 明确"人工补录 · 录入人 · 时间 · 可信度"。
- 核心原则：CEO 不必懂技术，但必须能回答"这数字从哪来、最新吗、能信吗"。

---

## 12. Time / Before-After（时间与前后对比 — §十三）

范围：Today / 7D / 30D / Month / Quarter / Custom；对比：Previous Period；Before/After：Model 切换前/后、Role 增员前/后、Workflow 调整前/后、Business Duplicate 后不同 Business。

Before/After 依赖变更事件标记（如 `model_switch_event`）+ 可比样本集；无标记时只给 Period 对比，不给因果结论。

---

## 13. Variant A / B / C（三方案 — §十五）

### Variant A — Dashboard / Explore First
偏传统现代 BI（为 CEO 简化）：首屏图表网格 + Explore 拖拽。
- 优点：信息密度高、熟悉。缺点：CEO 第一眼压力大、需理解图表；普通用户复杂；易变成数据监控工具。

### Variant B — Analyst / Report First
AI Analyst + Report + 结论为核心：首屏结论型简报 + 异常 + 报告，深入分析靠对话。
- 优点：CEO 友好、主动。缺点：可信度依赖 Fact/Interpretation 分离；易被误读为"AI 替我决策"；探索深度弱于 A。

### Variant C — Hybrid Operating Intelligence
Company Overview + Explore + Analyst + Report + Scoped Analysis + Decision Support。
- 优点：兼顾主动与探索、CEO 与普通用户。缺点：实现最重、需分阶段。

**不预设 C 一定赢**。评价：A 适合"爱看数"的 CEO 但门槛高；B 适合"不想配"的 CEO 但探索弱；C 最平衡但最重。推荐**以 B 的骨架起步（结论+报告+Analyst），逐步补 A 的 Explore 与 Benchmark 能力**——即 C 的分阶段实现，而非一次性全做。

---

## 14. 经营内核不能被 Dashboard 吞掉（§十四）

Recovery Audit 已确认经营内核：Result / Evidence / Acceptance / Decision / Capacity / Commitment / External Result / Failure-Recovery / CEO Attention。

**页面检查清单**：
- 数据是否仍服务"CEO 经营"（看→为什么→决定），而非把 Curis 变成数据监控工具？
- 每个分析页是否都能回到 Business / Workspace / Employee / Meeting / Decision 原入口？
- 是否保留 Evidence / Acceptance / External Result / Failure 的真实表达（不绿色卡片代替事实）？
- 是否不生成无源 Health Score、不排模型排行榜？

---

## 15. Navigation Recommendation（导航研究 — §十八，仅 Recommendation）

比较：A 第七一级导航 / B 全局空间不固定导航 / C CEO Desk 下钻 / D Business Space 内部 / E 其他。

| 角度 | 评估 |
|---|---|
| CEO 使用频率 | 经营洞察是高频深度分析，非每日首屏 |
| 独立任务心智 | 有（"我想分析公司经营"） |
| 跨 Business 需求 | 强（需跨 Business 比较） |
| 信息复杂度 | 高，宜独立空间 |
| Discoverability | scoped 入口已覆盖 |
| 导航负担 | 第七导航增加负担 |
| 与 CEO Desk 重叠 | 高（若都做首屏） |
| 与 Business Space 重叠 | 中（Business 内分析可 scoped） |
| 规模扩大价值 | 全局空间价值随 Business 增多上升 |

**Recommendation（仅建议，不修改 Frozen 六区）**：
研究阶段曾延续 `NAVIGATION PLACEMENT — REVIEW REQUIRED`，提出 **"scoped 入口 + 全局 Insights 空间"**；该问题已由 Final Product Architecture Delta 收口为第七个一级产品空间：
- 在 CEO Desk / Business / Employee Profile / 公司版图 / Assistant 保留带 Scope 的进入入口（Current 已定义）。
- 同时提供一个**全局 Insights 空间**（从现有六区上下文可达，如 CEO Desk 的"深入分析"、Business 详情的"经营分析"），不作为第七个一级导航项。
- 明确**不选 A（第七导航）**（增负担、与 Desk 重叠）；**不选纯 C（只 CEO Desk 下钻）**（跨 Business 比较需要独立空间）；**不选纯 D（只 Business 内）**（缺跨业务视角）。
- 最终由 CEO Review 决定。

---

## 16. Current / Dependency-Gated / Vision（§十九）

### CURRENT / CONFIRMED（可合理实现）
- Company / Business / Employee / Model 概览 UX（基于现有只读投影）。
- Scope Rail + Context Bar + 下钻 + 时间范围 + Period 对比。
- Data Trust 轻量标识（source/freshness/unknown/manual 展示）。
- 现有 Usage/Cost 真实数据的 Shared Metrics 呈现（RD 真实，通用 capability 待补）。
- Scoped 入口进入 Insights（Master Map / UI Blueprint 已定义）。

### DEPENDENCY-GATED（方向确认，依赖真实基础）
- **Domain Metrics 同屏**：依赖 Domain Metric Contract + External Adapter（Research §25 Gap）。
- **Model/Agent Benchmark 深比**：依赖 Benchmark 数据集 + 真实可比样本（Recovery Audit LATER）。
- **Report 对象与自动报告**：依赖 Report Runtime（未交付）。
- **主动洞察引擎**：依赖检测引擎 + 事件标记（未交付）。
- **Before/After 因果对比**：依赖变更事件标记（model_switch 等）。
- **External Result 真实展示**：依赖首个 Business 外部数据源接通（XHS 仍 NOT_CONNECTED）。
- 重新进入条件：对应 Runtime Gap 补齐或出现真实经营瓶颈。

### VISION（价值成立，当前不足固定）
- 完整外部 Metric Adapter 生态、Observation、跨平台 Report。
- 自主行业/竞品研究 Agent（需 Research Employee + 外部知识）。
- 跨业务投资组合优化、容量自动调度。
- 不提前猜实现；保留方向。

**不用**"为了 v1 简单所以放 v2"作理由——以上分类基于"依赖是否满足 / 真实经营经验是否足够"，不是功能砍切。

---

## 17. Risks（风险）

1. **Dashboard 吞掉经营内核**：变成数据监控工具，偏离 Result/Evidence/Acceptance/Decision 闭环（§14）。
2. **无源 Health Score**：用单一分数误导 CEO。
3. **AI 解释冒充事实**：INTERPRETATION 未与 FACT 分离、UNKNOWN 不标。
4. **每 Business 不同 BI 软件感**：Domain 指标未统一外壳。
5. **双 Alert Center**：CEO Desk 与 Insights 各做一套提醒。
6. **Vision 当 Current**：把未依赖满足的能力提前固定。
7. **与 CEO Desk 重叠成第二首页**：经营洞察首屏复制 Desk 的注意力职责。

---

## 18. CEO Decisions Required（需 CEO 决策）

1. **命名**：是否正式统一"经营洞察 / Operating Intelligence"？（Recovery Audit Q3）
2. **导航**：是否接受"scoped 入口 + 全局 Insights 空间（不占第七一级导航）"？（延续 REVIEW REQUIRED）
3. **首屏形态**：Variant B 骨架起步（结论+报告+Analyst）是否被接受，再分阶段补 Explore/Benchmark（即 C 的分阶段）？
4. **外部数据源**：哪个真实 Business 的外部数据先接通，触发 Metric/Report/Adapter 专项？（Recovery Audit Q5）
5. **BI 组织成长**：是否同意 BI 能力按 Stage 1→5 由真实责任长出，不预设 BI Department？
6. **Demo→真数据**：本 UX 探索用 DEMO DATA，何时以真实 Runtime 投影替换（依赖 §16 DEPENDENCY-GATED 补齐）？

---

## 19. 配套可视化

- `CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html`：单文件、可切换 A/B/C、含 12 个指定状态、使用 DEMO DATA（显著标注 NOT RUNTIME TRUTH）。

---

**最终状态：CURIS OPERATING INTELLIGENCE — ANALYTICS UX RESEARCH COMPLETE — STOP FOR CEO VISUAL REVIEW**

> 本报告为 Analytics UX 研究，未修改任何 Current Product Truth（Blueprint / Master Map / UI Blueprint / Frozen Shell / Runtime / Schema / 代码 / 高保真均未改动）。所有结论待 CEO 视觉评审。

---

# ANALYST ORGANIZATION / ANALYSIS WORK LOOP DELTA

**日期**：2026-08-18（Delta）　**范围**：在上一轮 UX 研究之上，补"分析必须由真实 AI Employee 承担责任"这一重大产品缺口。
**状态**：Analyst Organization UX Delta 完成 · STOP FOR CEO VISUAL REVIEW

> 本轮**不重做**经营洞察研究。前一版结论全部有效：经营洞察 / Operating Intelligence、Shared + Domain Metrics、FACT/INTERPRETATION/UNKNOWN/RECOMMENDATION、Report、Data Trust、Scope/Context、Benchmark、CEO Desk 与 Insights 分工、Variant C Hybrid。本轮只把产品从 **Analytics Tool + AI Analyst** 升级为 **Operating Intelligence Workspace + Analyst Organization**。
> 纪律全守：未修改 Blueprint / Master Map / UI Blueprint / Frozen Shell / Runtime / Schema / 代码 / 高保真；未创建第二套 Employee；未创建匿名"AI Analyst"；未直接创建 BI Department；未把 demo 数据当 Runtime Truth。

---

## A.1 两层分析责任（核心模型）

### A.1.1 Business Analyst（业务分析师）
- 每个 Business 可有自己的数据/经营分析 Role 与 Employee（如内容增长部 → 小红书运营 → 数据分析岗 → 小红书分析师）。
- 只对**自己 Business** 的经营对象负责；阅读 Shared Metrics + 本 Business Domain Metrics；按 Workflow / Schedule 执行分析；产出 Daily / Weekly / Monthly / 专项 Report；对自己的结论负责。
- CEO 可直接与其对话、质疑、要求继续调查。
- 研发业务同样可设研发分析/质量分析责任，不做成统一 BI 岗。

### A.1.2 Company Analyst（公司级经营分析责任）
- 名称建议：**Company Operating Intelligence Analyst / Company Analyst / Chief Analyst**（仅建议，未写入 Product Truth）。
- 职责**不是替代** Business Analyst，而是从公司全局看 Department / Business / Role·Staffing / Employee / Cost·Usage / Result·Quality / Capacity·Load / Model·Agent / Capability / External Result / Risk·Trend。
- 典型主动发现：某 Department Token/Cost 异常 / 某 Business 连续偏离 Goal / 某 Role 过载 / 某 Business 成本增长快于 Result / 某 Model 在多个 Business 返工偏高 / 哪些 Business 值得深入调查。
- 它是未来 Analyst Team / BI Team 的 **Leader 型责任**，不是独立孤岛。

---

## A.2 数据流：事实与下级分析分离

```
Company OS / Metric Truth ──────────────→ Company Analyst（读原始/治理后事实）
                                              ↑
Company OS / Domain Data → Business Analyst → Business Report ──┘（作为额外分析输入）
```

- Company Analyst **同时**可读：① 原始/治理后的经营事实；② Business Analyst 的报告与解释。
- **关键红线**：Business Report 的 INTERPRETATION **不能被自动升级成 Company Fact**。Company Analyst 将其作为"额外分析输入"，独立给出带 Evidence 的汇总。
- 这避免了"下级判断自动变成公司真相"的错误，也避免 Company Analyst 必须重做所有 Business 分析。

---

## A.3 Report 成为 AI Employee 的正式工作成果（Header 重设计）

上一版只显示 Author 不够。新版 Report Header / Metadata 至少体现：

| 字段 | 说明 |
|---|---|
| Report Name | 报告名 |
| Scope | 分析对象 |
| Period | 时间范围 |
| Analysis Responsibility / Role | 分析责任归属（岗） |
| Author Employee | 产出报告的真实 Employee |
| Business / Department | 所属业务/部门 |
| Trigger | Scheduled / Requested by CEO / Proactive / Follow-up |
| Data Sources | 来源（ai_usage / Manual / External 回执等） |
| Model / Agent provenance | 使用的模型/智能体 |
| Created At | 生成时间 |
| Review / Verification 状态 | 待 CEO 确认 / 已复核等 |

正文保持：**FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION / EVIDENCE** 五段。
→ 报告是**可追溯的 Result / Asset**，作者永远是真实 Employee，不是匿名文档。

---

## A.4 CEO「找人讨论」交互（本轮核心）

- CEO 看到任意分析或 Report 后，可：问分析师 / 质疑结论 / 为什么这么判断 / 给我看证据 / 继续调查 / 验证我的另一个假设 / 让第二位分析师复核 / 让所属 Business Analyst 补充 / 召开 Meeting / 形成 Decision / 回到 Business。
- 点击「问分析师」→ 进入 Curis **已确认的 Conversation Surface**（Main 区完整员工对话），**不是右下角小聊天框**，与员工 Workspace 中 Conversation 是**同一记录**，只是完整展示。
- 借此把"看数据"自然转成"和责任人对谈"。

---

## A.5 CEO 质疑场景（完整闭环示例）

报告：《小红书经营日报》· Author：小红书分析师 小陈
结论：涨粉较上周下降 12%，可能与选题重复度上升有关。

1. CEO 点「问小陈」→ 进入完整 Conversation。
2. CEO：为什么你认为是选题导致的？
   小陈（FACT/INTERPRETATION/UNKNOWN/EVIDENCE/RECOMMENDATION）：涨粉 -12%、发布频次未降、近 20 篇选题相似度提高；指向触达疲劳；但 External Connector 未提供完整曝光结构，**无法证明因果**；建议做"选题多样性专项分析"。
3. CEO：我觉得可能是平台流量变化，你去验证一下。
   → **创建一个真实 Analysis Task**；Responsibility 仍归小陈；小陈开始执行。
   → 完成后产生**新的 Report / Evidence**；回到**同一 Conversation**；CEO 继续判断。
4. 不只是一个"收到"——全程责任链清晰、可追溯。

---

## A.6 第二位分析师复核（Second Analyst Review）

CEO 点「请求复核」→ 由 Company Analyst 或另一名 Research Analyst **独立复核**。
结果结构必须表达：**Original Analysis / Reviewer / Agreement / Disagreement / Evidence / Unknown / Final Recommendation**。
- 复核不是简单点赞/通过：本例中复核认同 FACT 与主假设，但指出"平台流量变化不能仅以大盘持平排除"，建议补充分时段流量结构。
- 独立复核人**不能修改其他 Business 的分析责任**。

---

## A.7 Company Analyst 委派 Business Analyst（公司级闭环）

经营洞察首页出现：内容增长部 Cost ↑27%。
Company Analyst（司衡）主动形成《内容增长部成本异常专项分析》，结论：61% 增量来自抖音运营，但 External Result 未完整接入，建议请抖音 Business Analyst 补充。

CEO："让抖音分析师查一下。"
真实责任流：
```
司衡(Company Analyst) → Handoff/Assigned Analysis Request → 小陆(抖音 Business Analyst)
→ 专项分析 → 《抖音 30D 业务效果》Report → 司衡 汇总 → CEO
```
- 抖音分析师返回的 INTERPRETATION 作为**额外输入**进入司衡的汇总，不被自动升级为 Company Fact。
- 体现 Company Analyst 居中协调、Business Analyst 负责本职的协作分工。

---

## A.8 CEO Assistant 与 Company Analyst 边界

| | CEO Assistant | Company Analyst |
|---|---|---|
| 负责 | Attention / 汇报 / 哪件事现在值得看 / Routing / Decision 提醒 / 跟进 | 专业经营分析 / 跨 Business 比较 / 原因解释 / 证据 / 专项调查 / Recommendation |
| 示例 | "老板，Company Analyst 刚完成内容增长部成本专项，建议你查看。" | 给出成本异常的原因、证据、建议与复核结论 |

- **不让 CEO Assistant 变成专业分析师**：Assistant 负责"attention & routing"，Analyst 负责"analysis & evidence"。

---

## A.9 没有 Analyst Employee 时（No Analyst 状态）

新 Business（如公众号运营）尚无数据分析岗：
- CEO 问"为什么最近 Result 下降？" → 系统**不假装存在匿名 Analyst**。
- 显示：当前没有负责「公众号运营经营分析」的 Employee。
- 提供四选一：① **创建临时分析任务**（≠ 自动创建永久岗位）；② 指派现有 Employee；③ 创建数据分析岗位；④ 从人才与能力招募分析师。
- 红线：**临时任务 ≠ 永久 Role**；长期重复后才可能形成稳定责任。

---

## A.10 组织成长模型（由真实责任长出）

1. CEO 临时请求分析
2. Business 出现稳定数据分析责任
3. Business 建立数据分析 Role + Employee
4. 多个 Business 都有分析师
5. 出现稳定 Company-level 综合分析责任
6. 形成 Analyst Team / BI Team
7. 责任规模足够后形成正式 Department

- 页面只做轻量 Growth State 说明，**不创建新 Primitive**、不预设 BI Department。
- 与 Curis 已确认组织成长模型一致：**组织由真实工作量和责任长出来**。

---

## A.11 首页重做（更像"我的 AI 分析团队给我准备了什么"）

去除"KPI 卡片集合"心智，改为：
- **Company Analyst Brief**：头像 / Employee Name / Role + 一句经营结论 + [和他讨论] / [查看完整分析]。
- **Company Operating Signals**：少量真实指标（Cost / Result / Acceptance / External Result / Capacity·Load / 重要变化）。
- **Business Reports**：各 Business 分析师产出的报告卡（Author 真实 Employee + [查看] / [问分析师]）。
- **Cross-company Analysis**：Model Benchmark / Cost Efficiency / Organization Capacity / Industry Research / 专项分析。

---

## A.12 左侧导航重做（Curis 式，§12）

上一版 HTML 左侧是 "Company Overview / Business / Employee / Benchmark / Report / AI Analyst" —— 太像 BI 功能菜单。
改为（方案 1，推荐）：

```
经营洞察
├ 公司经营
├ 业务分析
├ 组织与员工
├ 模型与能力
├ 分析报告
└ 专项研究（Company Analyst）
```

- **AI Analyst / Company Analyst 不是"功能菜单"**：它们是当前经营洞察里的真实 Employee / Work Surface，出现在主区内容（Brief、报告作者、对话入口），而非侧栏按钮。
- 备选方案 2：将"我的分析团队"作为首页一个常驻区块（而非导航项），导航仍保持 6 个 scope 项。两种都遵循"Analyst 是真实责任，不是功能开关"。

---

## A.13 UI 变化小结

- 经营洞察从"数据后台 + AI 聊天"→"Operating Intelligence Workspace + Analyst Organization"。
- 每个 Business 有值守分析师；公司有一个全局分析负责人；二者通过 Handoff/复核/Meeting/Decision 协作。
- 所有分析责任归属真实 Employee，报告有完整 Header + 五段正文 + 可追溯证据。
- CEO 的"看→质疑→调查→复核→决策"全程在已确认 Conversation / Meeting / Decision 原入口闭环，经营洞察不做第二套 Editor。

---

## A.14 当前仍待 CEO 决定的问题

1. **命名**：Company Analyst 是否定名"司衡 / Company Analyst / Chief Analyst"？Business Analyst 岗位命名规范？（未写入 Product Truth）
2. **责任归属权**：Company Analyst 能否主动 Handoff 给 Business Analyst，还是必须经 CEO 授权？（影响 Handoff 合同）
3. **复核机制**：Second Analyst Review 是强制（关键决策前）还是按需？复核人来自哪个 Role 池？
4. **No Analyst 路径**："创建临时任务"是否计入该 Business 的"责任重复次数"以触发 Stage 升级？阈值如何定？
5. **与 CEO Desk 的分工再确认**：Company Analyst 的 Proactive 分析"建议查看"由 Assistant 路由，还是直接进 Insights？二者事件源是否共享（避免双 Alert）？
6. **组织成长触发**：Analyst Team / BI Team / Department 的形成阈值与审批流由谁定义（沿用 Curis 组织成长模型，不预设 BI Department Primitive）？
7. **Demo→真数据**：本 Delta 全部用模拟 Employee/报告；何时以真实 Runtime 投影 + 真实 AI Employee 替换（依赖上一轮 §16 DEPENDENCY-GATED：Report Runtime、External Adapter、Benchmark 数据集）？

---

**Delta 最终状态：CURIS OPERATING INTELLIGENCE — ANALYST ORGANIZATION UX DELTA COMPLETE — CONSUMED BY CURRENT PRODUCT TRUTH**
