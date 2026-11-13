# CURIS OPERATING INTELLIGENCE — DATA VISUALIZATION RESEARCH

### 经营洞察 · 数据可视化研究（仅研究，不设计页面）

**Authority Class**：RESEARCH  
**Disposition**：CONSUMED BY CURRENT PRODUCT TRUTH（Operating Intelligence contracts）

> 本轮属性：**纯研究**。只回答"Curis 经营洞察里，哪些经营问题应该用可视化、用什么图、成熟产品怎么做"。  
> 不设计 Curis 最终页面、不修改上一版 UX HTML、不修改 Blueprint / Master Map / UI Blueprint / Frozen Shell / Runtime / Schema、不写产品代码。
>
> 沿用结论（来自前两轮，保持有效）：
>
> - 经营洞察 / Operating Intelligence 统一心智；Company OS 是事实源，不建第二套 Truth。
> - Shared Metrics + Domain Metrics；跨业务比较需显式可比性声明。
> - 每个数字可拆：FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION；AI 解读不冒充事实。
> - Report 是可追溯的 Result / Asset，由真实 AI Employee 承担责任（Business Analyst / Company Analyst）。
> - Data Trust：Source / Freshness / Verified / Manual / Unknown / Stale / Missing 必须可感知。
> - Variant C（Hybrid Operating Intelligence）：Dashboard + Explore + Analyst + Report + Decision Support。
> - CEO Desk 与经营洞察分工：Desk 管"现在该打扰 CEO 什么"，Insights 管"完整分析"。
>
> 执行说明（透明）：当前会话无 `TeamCreate` 原语、`Agent` 工具被团队门禁拦截，无法拉起专家子团队。主理人以 AiDataCopilot 视角直接执行并汇编，保留"专长分离 + 主理人汇总"协作实质，纪律约束全盘照旧。

---

## 0. 研究边界与核心立场

### 0.1 本轮不回答什么

- 不决定经营洞察的最终页面布局、配色、组件清单。
- 不预设"必须做 N 个 Dashboard"。
- 不把"图表多"当作"分析强"。

### 0.2 本轮要回答什么

从 **CEO 要回答的经营问题**出发，倒推"该不该可视化、用什么图、为什么"。这是本文唯一的方法论红线——**不以图表类型出发，以问题出发**（与 AdSights、Kredily、Workforce Intelligence 等成熟产品的"ask bar / question-first"一致，见 §1）。

### 0.3 本研究的拼写原则

> Curis 不以 Dashboard 作为经营洞察的产品心智，但任何适合**视觉比较、趋势发现、分布判断、关系分析**的数据，都应该使用最有效的数据可视化。

最终体验应是：

```
Analyst 给出结论
→ Visualization 帮 CEO 看见模式
→ Table 查看精确数字
→ Evidence 验证事实
→ Conversation 质疑分析师
→ Employee 继续调查
```

---

## 1. External Product References（外部成熟产品参考）

> 下表记录真实产品及其可视化做法，作为 Curis 借鉴基线。**每条均标注来源 URL**。

| #  | 产品 / 类别                                                    | 分析对象             | 主要指标                                                                 | 典型图表做法                                                                                               | 关键启示                                              | 来源                                                                                                                                                                                                                                                                                                                                             |
| -- | ---------------------------------------------------------- | ---------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E1 | 小红书创作者中心 / 专业号                                             | 单篇笔记 / 账号        | 曝光、阅读、点赞、收藏、评论、分享、涨粉、完读率、CTR                                         | 数据面板 + **用户行为热力图**（滑动衰减节点）+ 互动分布饼图 + CSV 导出                                                          | 互动深度 > 播放量；**热力图用于定位内容钩子失效点**                     | [vivozhijia](https://www.vivozhijia.com/wz/908439.html) · [xiao-hong-shu](https://xiao-hong-shu.top/blogs/666279919) · [ufcn](https://www.ufcn.cn/article/2378370.html)                                                                                                                                                                        |
| E2 | 抖音 / 巨量引擎 / TikTok Business Suite                          | 短视频 / 账号         | 播放、平均观看时长、完播率、涨粉、关注、流量来源（FYP/搜索/主页）、粉丝活跃时段                           | Overview/Content/Followers 三段；**受众留存曲线**；**Followers Activity 时段热力**                                 | "平均观看时长"比"播放量"更重要；**时段热力指导发布时间**                  | [moonb.io](https://moonb.io/blog/best-tools-for-analyzing-video) · [influenceflow](https://influenceflow.io/resources/how-to-analyze-tiktok-analytics-in-2026-your-ultimate-guide-to-growth-monetization) · [mediaexposure](https://mediaexposurehub.com/creator-analytics-marketers-win-in-2026)                                              |
| E3 | YouTube Analytics / GA4                                    | 视频 / 网站          | 观看时长、 retention curve、Impressions、CTR、流量来源、订阅净增                      | **Performance Graph（时间序列，可切指标）+ 历史均值灰带**（高于/低于基线）+ 流量来源分解                                            | "视图数最不重要"，**retention 曲线揭示流失秒数**；**灰带对比自身基线**     | [ytgrowth](https://ytgrowth.io/blog/youtube-analytics) · [statiko](https://statiko.io/blog/best-free-social-media-analytics-tools)                                                                                                                                                                                                             |
| E4 | 营销 / 电商分析（AdSights、Triple Whale、Northbeam）                 | 投放 / ROAS        | ROAS、MER、CAC、CPA、渠道占比、留存队列                                           | **Line（趋势）/ 横向 Bar（渠道排名）/ Funnel（落地→加购→购买）/ Retention curve / Scatter（花费 vs 效率）/ Cohort heatmap**    | **"问对问题"优先于"选对图"**；避免饼图 >4 片、避免截断轴                | [adsights](https://www.adsights.ai/blog/topics/data-visualization/which-chart-for-which-metric-marketing-data-visualization-guide)                                                                                                                                                                                                             |
| E5 | Mixpanel / Amplitude（产品分析）                                 | 用户行为             | 事件、漏斗转化、留存、群组、路径                                                     | **Funnel Analysis（流失定位）/ Retention（队列热力）/ Event Segmentation / Journeys / Stickiness**；NLQ 自动选图      | 漏斗看"在哪流失"；**留存用队列热力**；问题分类→图族                     | [amplitude](https://amplitude.com/docs/analytics/charts/find-the-right-chart) · [mixpanel-insights](https://help.mixpanel.com/docs/reports/insights) · [mixpanel-retention](https://mixpanel.com/es/retention)                                                                                                                                 |
| E6 | BI（Power BI / Tableau / Looker）                            | 通用企业数据           | 任意指标                                                                 | 表格 + 折线 + 柱 + 堆叠 + 地图 + 参数过滤；**治理的数据访问**                                                             | 交互式钻取 + 行级安全；**图表选择靠语义层统一口径**                     | [tableau-hr](https://wifitalents.com/best/human-resources-reporting-software/)                                                                                                                                                                                                                                                                 |
| E7 | LLM Observability（LangSmith / Langfuse / Helicone / Arize） | Agent / Model 调用 | Token（in/out/cache）、Cost、Latency、Error rate、Eval score、Trace         | **可配置指标图（latency/cost/error/custom score）+ Trace waterfall + 按 model/feature/user 分组 + SQL 导出**；阈值告警 | **成本/延迟/质量分三类图并存**；按模型/功能分组是 benchmark 基础         | [unpromptedmind](https://www.unpromptedmind.com/llm-observability-helicone-langsmith-langfuse) · [aiagentrank](https://aiagentrank.io/blog/ai-agent-observability-2026) · [gauraw](https://www.gauraw.com/ai-app-monitoring-observability-production-llm-2026) · [pillai](https://pillaiinfotech.com/article/ai-observability-monitoring-llms) |
| E8 | Workforce Analytics（Runn / Kredily / MangoApps）            | 组织 / 员工          | Headcount、Capacity、Workload、Business Cost、离职/出勤/加班、Cost per employee | **KPI strip + sparkline + delta**、**容量/成本按雇佣类型堆叠**、**队列热力（留存）**、**负荷曲线**、**缺口/过载预警**；ask bar 而非图表菜单  | "领导驾驶舱不是图表库"；**Org→主题→个人 三级下钻**；**成本增长快于人数 = 预警** | [runn](https://help.runn.io/en/articles/11517235-workforce-dashboard) · [kredily](https://kredily.com/workforce-intelligence) · [hrduo](https://hrduo.com/operations/analytics-and-reporting) · [mangoapps](https://www.mangoapps.com/operations/insights-performance)                                                                         |

### 1.1 跨产品共性结论（Curis 可直接借鉴）

1. **问题分类 → 图族**：change over time / compare categories / part-to-whole / distribution / relationship / cohort，每个对应一个图族（AdSights、Sumboard、LobeHub 一致）。【[adsights](https://www.adsights.ai/blog/topics/data-visualization/which-chart-for-which-metric-marketing-data-visualization-guide) · [sumboard](https://www.sumboard.io/guides/chart-types)】
2. **视觉编码层级**：位置（共用刻度）> 长度 > 角度/斜率 > 面积 > 颜色饱和度 > 色相。最重要比较用"位置/长度"（柱/点对齐），别用面积/3D（Cleveland & McGill、Tufte data-ink、LobeHub）。【[lobehub](https://lobehub.com/en/skills/wentorai-research-plugins-data-visualization-principles) · [skillmd](https://skillmd.ai/skills/data-visualization-8)】
3. **受众决定图**：高管要"一屏一结论"静态概览；分析师要交互钻取；大众要熟悉图型（2026 Best Practice）。【[wp-guide](https://wp.me/pepC5j-1RU)】
4. **AI 解释但不算数**：Kredily / Workforce Intelligence 明确"AI 解释数字、从不计算"，每条预警带 evidence——与 Curis FACT/INTERPRETATION 分离原则一致。【[kredily](https://kredily.com/workforce-intelligence)】
5. **基线优于绝对值**：YouTube "历史均值灰带"、Mixpanel 队列热力相对着色——Curis 的 Before/After 与异常检测应复用"相对自身基线"而非裸数字。
6. **分组聚合是 benchmark 底座**：LangSmith/Langfuse 按 model/feature/user 分组统计；Curis Model/Agent Benchmark 复用同一思路（见 §11）。

---

## 2. Metric / Analysis Pattern Inventory（指标与分析模式清单）

> 覆盖 Curis 未来可能出现的主要数据类型。每类列出：数据项 / 典型分析问题 / 成熟产品对应模式 / 候选图族（**候选，非定案**）。

| 数据类型（Curis）                    | 典型分析问句                | 外部对应模式                   | 候选图族                 |
| ------------------------------ | --------------------- | ------------------------ | -------------------- |
| Company（整体运行）                  | 公司整体产出/成本/质量趋势？       | E8 KPI strip + sparkline | 概览卡 + 多线趋势           |
| Department                     | 哪个部门成本异常？             | E8 成本按部门分布               | 堆叠柱 / 分组柱            |
| Business                       | 某 Business 是否偏离 Goal？ | E3 灰带基线                  | 目标对比 + 趋势            |
| Goal                           | 目标完成度？                | E3 进度                    | 进度条 / 斜率图            |
| Result                         | 产出数量与质量？              | E5 事件                    | 计数 + 质量分布            |
| External Result                | 小红书涨粉/抖音播放？           | E1/E2 平台指标               | 领域折线 + 来源标注          |
| Cost                           | AI 成本增长？              | E7 成本图                   | 时间序列 + 分组            |
| Token                          | in/out/cache 占比？      | E7 token 图               | 堆叠面积 / 分组柱           |
| Duration                       | 执行耗时分布？               | E7 latency               | 直方图 / 箱线             |
| Quality                        | 一次通过率/返工？             | E5/E7 eval               | 分布 + 趋势              |
| Acceptance（CEO 验收）             | 验收通过率变化？              | E5 转化                    | 趋势 + 漏斗              |
| Failure                        | 失败率上升？                | E7 error rate            | 时间序列 + 告警            |
| Retry                          | 重试集中哪？                | E7                       | 分布 / 堆叠              |
| Rework                         | 返工增加？                 | E5                       | 趋势 + 漏斗              |
| Workflow / Stage               | 哪阶段耗时/失败最多？           | E5 Funnel                | 漏斗 / 桑基              |
| Role                           | 哪个 Role 过载？           | E8 负荷                    | 负荷曲线 / 堆叠            |
| Employee                       | 谁效率低/质量差？             | E8 个人下钻                  | 排名柱 + 下钻             |
| Capacity / Load                | 容量 vs 负载缺口？           | E8 capacity              | 容量-负载带               |
| Model                          | 哪个模型成本/质量好？           | E7 分组                    | 排序柱 + 散点（§11）        |
| Agent                          | Agent 间差异？            | E7                       | 同 Model              |
| Provider                       | Provider 维度成本？        | E7                       | 分组柱                  |
| Capability / Skill / Connector | 哪个能力真改善结果？            | E5 影响分析                  | 前后对比 / 关联            |
| Report                         | 有哪些待读报告？              | E8 预警列表                  | 列表 + 优先级             |
| Before / After                 | 换模型前后差异？              | E3 灰带 / 斜率               | 斜率图 / 分组（§10）        |
| Business Duplicate             | 复制后两 Business 表现？     | E4 A/B                   | 双线对比                 |
| Domain Metrics（内容/研发）          | 领域指标趋势与构成？            | E1/E2                    | 领域图 + 共享图同屏（§13/§14） |

---

## 3. CEO Question → Visualization Mapping（经营问题 → 可视化映射）

> 这是本文核心。每行从**CEO 问题**出发，给出数据与图表，并说明**为什么这样表达**（而非只给图名）。



| CEO 问句                   | 数据            | 选图                  | 为什么（表达逻辑）                              |
| ------------------------ | ------------- | ------------------- | -------------------------------------- |
| "最近涨粉是在上升还是下降？"          | 每日涨粉          | **时间序列折线**          | 趋势只能由"对齐的时间点位置"表达；折线让人一眼看到斜率方向，柱会丢失连续性 |
| "十几个模型哪个成本更高？"           | 各模型总成本        | **按值排序的横向柱**        | 长度比较最准（Cleveland 层级）；排序后差异自现，不按字母乱序    |
| "成本和质量之间什么关系？"           | (成本, 质量) 散点   | **散点图 + 趋势线**       | 关系是二维的，只有散点能暴露"高成本≠高质量"的离群点            |
| "内容增长部成本主要花在哪？"          | 成本按子项         | **堆叠柱 / 环形(≤5)**    | 构成是"部分-整体"，堆叠显示总量与占比；>5 片改堆叠柱          |
| "用户在哪一步流失？"              | 各阶段留存         | **漏斗 / 瀑布**         | 顺序阶段+流失率，漏斗直接显示"漏点"；桑基看跨阶段流向           |
| "什么发布时间效果最好？"            | 时段×表现         | **热力图 / 分桶对比**      | 二维（星期×小时）密度，热力色阶最快暴露峰值格子               |
| "换模型前后效果怎么样？"            | 前/后样本         | **斜率图 / 前后分组柱**     | 两时点对比，斜率图用一条线浓缩"变化方向与幅度"               |
| "哪个 Business 持续偏离 Goal？" | 目标 vs 实际      | **目标带 + 偏离标记**      | 基线/目标带让"偏多少"可量化，而非裸数                   |
| "哪个 Role 过载、哪个空闲？"       | 容量 vs 负载      | **容量-负载带 / 堆叠**     | 同时显示"上限"与"占用"，缺口=风险，溢出=过载              |
| "失败率是不是突然升高？"            | 失败率序列         | **时间序列 + 统计控制带**    | 突变 vs 基线波动，需统计阈值而非肉眼                   |
| "External Metric 是不是异常？" | 外部指标序列        | **时间序列 + 来源/新鲜度标注** | 外部数据必须标 Source/Freshness，避免误读陈旧回执      |
| "哪个 Employee 效率偏低？"      | 员工指标          | **排序柱 + 下钻个人**      | 排名暴露尾部；点开个人看分布与证据（E8 三级下钻）             |
| "两个 Business 表现差多少？"     | 两 Business 指标 | **双线 / 哑铃图**        | 两对象同指标对比，哑铃图一条线显示"起点-终点差距"             |
| "这个内容类型是不是更好？"           | 类型×表现         | **分组柱 / 小倍数**       | 类别对比用分组；多类型用 small multiples 避免图内拥挤    |

**映射红线**：

- 凡"比较大小"→ 位置/长度（柱/点），**禁用饼图做精确比较**。
- 凡"趋势"→ 折线/面积，**禁用把分类轴当时间连成线**。
- 凡"关系"→ 散点，**禁用量级差巨大的双 Y 轴**（用 small multiples 替代）。
- 凡"构成"且 >5 类 → 堆叠柱，**禁用 3D 饼**。
- 凡"分布"→ 直方图/箱线，**禁用用均值柱掩盖分布**（均值会藏掉离群与偏态）。

---

## 4. Trend Visualization（趋势）

**适用问题**：涨粉上升/下降？成本逐月变化？验收率趋势？失败率抬升？

**推荐图族**：

- **折线图（Line）**：最通用的时间序列；多系列时 ≤5–7 条，超出用 small multiples。
- **面积图（Area）**：强调累计量级（如累计成本）。
- **基线带（Baseline band）**：在折线外加一条"历史均值/目标"灰带（YouTube 做法，E3），高于带=超常，低于带=欠佳。**Curis 的 Goal 偏离与异常检测直接复用**。
- **迷你 sparkline**：概览卡里嵌入趋势微图（Kredily KPI strip，E8），让 CEO 首屏"看见方向"而不点开。
- **区间/置信带**：对波动大的指标（失败率）显示统计区间，区分"真突变"与"正常抖动"。

**Curis 注意**：趋势图必须带 **时间范围切换（7D/30D/Month/Quarter/Custom）** 与 **上期对比（Previous Period）** 开关——这是上一轮 §13 已确认的交互。External 数据趋势需标 Freshness，陈旧则灰显。

---

## 5. Comparison Visualization（比较）

**适用问题**：十几个模型哪个贵？哪个 Business 成本更高？哪个员工效率低？

**推荐图族**：

- **排序横向柱（Sorted horizontal bar）**：类别比较首选；按值排序，长标签友好。模型数 10–20 仍可读（见 §11）。
- **哑铃图（Dumbbell）**：两时点/两对象同指标对比（如换模型前后），一条线显示差距。
- **斜率图（Slope chart）**：仅两时点的变化方向（Before/After 见 §10）。
- **小倍数（Small multiples）**：同图型复制多份，每份一个切片（如每个 Business 一张迷你趋势），**替代双 Y 轴**避免误导。
- **分组/簇状柱（Grouped bar）**：少量类别并排比较。

**Curis 注意**：Shared Metrics 跨 Business 比较时，若口径一致直接比；Domain Metrics 跨 Business **默认不比**，显式提示"口径不同"（沿用 §7 Domain 原则）。比较结果必须可点开看 Evidence。

---

## 6. Composition Visualization（构成）

**适用问题**：内容增长部成本主要花在哪？某 Business 时间都耗在哪些 Workflow 阶段？Token 中 cache/in/out 占比？

**推荐图族**：

- **堆叠柱（Stacked bar）**：绝对构成的时序比较（如每月成本按子项堆叠）。
- **100% 堆叠（Percent stacked）**：看占比结构变化。
- **环形图（Donut，≤5 片）**：单期部分-整体；中心可放汇总指标（KPI 卡友好）。**>5 片改堆叠柱**。
- **瀑布图（Waterfall）**：累计变化分解（如"本月成本 = 上月 + 抖音增量 + 研发增量 − 优化"），适合解释"变化从哪里来"。
- **桑基图（Sankey）**：跨阶段/跨对象流量（如成本从 Department→Business→Capability 流向）。

**Curis 注意**：构成图必须标注**口径与来源**（尤其 External 占比，如"抖音 External Result 占 61% 成本增量"需带来源）。

---

## 7. Distribution / Correlation（分布与相关性）

**适用问题**：执行耗时分布？成本与质量是否相关？某模型是否"便宜但质量差"？

**推荐图族**：

- **直方图（Histogram）**：连续变量分布（Duration、Cost per execution）。
- **箱线图（Box plot）/ 小提琴图（Violin）**：多组分布比较（如各模型 Duration 分布），**暴露中位数、四分位、离群**——比均值柱诚实。
- **散点图（Scatter）**：两变量关系；加趋势线、按类别着色、标离群。
- **相关性热力（Correlation heatmap）**：多指标两两相关矩阵。

**Curis 关键原则**：**禁止用单均值柱掩盖分布**。例如"模型 A 平均成本低"可能因其多数任务极简、少数极贵——箱线+散点才能暴露。这正是避免"Token 少=模型更好"误导的图表手段（呼应前两轮 Model Benchmark 纪律）。

---

## 8. Funnel / Workflow（漏斗与流程）

**适用问题**：Workflow 哪阶段耗时/失败/返工最多？用户/任务在哪步流失？External 转化漏斗？

**推荐图族**：

- **漏斗图（Funnel）**：顺序阶段转化（如 选题→创作→发布→涨粉→转化；或 Execution: 创建→运行→验收→返工→完成）。直接显示每步流失。
- **桑基图（Sankey）**：跨阶段流向与分支（如任务在 Handoff 间的流转、Retry 回流）。
- **阶段时间堆叠（Swimlane / Gantt-like）**：各阶段耗时占比，定位瓶颈阶段。

**Curis 注意**：Workflow 是 Curis 核心对象（运行层：目标→规划→任务图→队列→调度→执行→验收→返工→完成）。漏斗/桑基应**从 Company OS 的 Workflow/Stage 事实直接生成**，不另建流程数据。返工回流用桑基的"回边"表达。

---

## 9. Time Pattern（时间规律）

**适用问题**：什么发布时间效果最好？哪天/哪小时员工负载最高？External 互动的时段规律？

**推荐图族**：

- **热力图（Heatmap）**：二维时间密度（星期×小时，或 日期×指标）。最快暴露峰值格子（小红书行为热力 E1、TikTok 粉丝活跃 E2、Mixpanel 队列热力 E5）。
- **分桶对比（Bucketed bar）**：一维时间分布（如各小时平均涨粉）。
- **周期性叠加（Seasonal small multiples）**：每周同天对比，看周规律。

**Curis 注意**：时间规律图必须尊重 **Timezone**（Curis 跨平台 External 数据可能 UTC/本地混用，需统一标注），否则"最佳发布时间"会误导。

---

## 10. Before / After（前后的变化对比）

**适用问题**：文案岗换 Model 前后？Role 增员前后？Workflow 调整前后？Business Duplicate 后两 Business 表现？

**推荐图族**：

- **斜率图（Slope chart）**：两时点单指标变化（前→后一条线），最紧凑表达"变好/变坏 + 幅度"。
- **前后分组柱（Before/After grouped bar）**：多指标并排（如 Cost/Duration/Review/Result 各画前/后两根柱）。
- **平行坐标（Parallel coordinates）**：多指标前后样本的分布位移（如换模型后整批执行的 Cost/Duration/Quality 分布整体左移/右移）。
- **差异标注（Delta badges）**：每指标显示 ±% 与统计显著性，避免"看起来变了其实噪声"。

**Curis 注意**：Before/After 是 Curis"自进化"的数据基础（前两轮 §14 历史比较）。必须保证**可比样本**：同 Role / Task Type / Workflow Stage / Business / Complexity / Context / Capability（Model Benchmark 可比性维度）。样本不足时显式"样本不足"，禁止无依据结论。

---

## 11. Model / Agent Benchmark（模型/智能体基准 · 重点）

**问题背景**：纯表格在模型数量增加到 10–20 个时可读性迅速崩塌；但只看一张汇总图又会丢失精确数字与证据。

### 11.1 数据维度（复用 E7 分组思路）

按 `model / agent / provider / capability` 分组，指标：Cost、Token(in/out/cache)、Duration、Acceptance、Quality、Rework、Failure、Human Intervention、External Result。

### 11.2 推荐图族组合（"图看差异，表看精确"）

1. **排序横向柱（核心）**：把 10–20 个模型按单一指标（如 Cost）排序，CEO 一眼看到最高/最低。**这是 CEO 第一眼用的图**。
2. **小倍数（Small multiples）**：每个关键指标一张迷你排序柱，拼成网格——避免把 10 模型×8 指标塞进一张图。
3. **散点图（关系）**：X=Cost，Y=Quality，点=模型，气泡大小=Execution 数。直接暴露"便宜但质量差"的离群模型（**破解"Token 少=更好"**）。
4. **箱线/小提琴（分布）**：每个模型的 Duration 分布，暴露稳定性差异（均值会藏掉长尾）。
5. **分组柱（可比切片）**：在固定 Role/Task Type 下对比少数模型——保证可比性。
6. **表格（必须保留）**：精确数字、样本量、置信区间、Evidence 链接。**图用于"发现差异"，表用于"核实精确值"**。

### 11.3 可读性纪律（避免表格式崩塌，也避免图表式误导）

- 模型 >8 个：默认**排序柱 + 小倍数**，不画多系列折线。
- 任何 Benchmark 视图**强制显示样本量（n）与可比性声明**（Role/Task/Stage 是否一致）。
- **禁止"最佳模型排行榜"式单一总分**；必须多维度并陈，且每维可下钻 Evidence。
- 不确定时：显示"样本不足 / 口径不一致"，不渲染伪精确排名。

---

## 12. Organization / Employee（组织与员工）

**借鉴 E8（Workforce Analytics）成熟做法**：

- **KPI strip + sparkline + delta**：组织概览卡（Headcount、Capacity、Load、Cost、Vacancy、Flight-risk 类比=过载风险），每卡带微趋势与环比。
- **容量-负载带（Capacity vs Load）**：显示每个 Role/Employee 的容量上限与当前负载；**缺口=空岗风险，溢出=过载**。这是"Role 过载""空岗影响 Business"的可视化答案。
- **负荷曲线 / 堆叠**：按时间看负载分布，定位持续阻塞的员工（呼应主动洞察 §12）。
- **成本-人数背离预警**：成本增长快于人数=预警（Kredily E8），Curis 中即"某 Department Cost ↑ 但 Headcount 平"。
- **三级下钻（Org→主题→个人）**：点 KPI 进主题钻取，点个人进档案——与 Curis 的 Scope Rail（Company→Department→Business→Role→Employee）天然一致。
- **Capability ≠ Capacity**：可视化上把"能力持有"与"容量/负载"分开两区，避免"执行次数多=表现好"的误读（前两轮 §六 明确）。

**Curis 注意**：员工分析不建第二套 Employee 真相，全部来自 Company OS 的 Employee/Role 事实 + ai_usage 账本聚合。

---

## 13. 小红书 Domain Visualization（内容业务案例）

**Shared Metrics（通用区，来自 Company OS / ai_usage）**：Duration、Cost、Result、Review、Employee、Model——用 §4–§12 的通用图。

**Domain Metrics（本业务区，来源=小红书平台回执，标 External/Manual）**：

- 曝光、阅读、点赞、收藏、评论、涨粉、转化、完读率、CTR。
- **趋势**：每日涨粉折线（§4）+ 历史基线带（§4 YouTube 灰带）。
- **构成**：互动分布（点赞/收藏/评论/分享占比）环形 ≤5 或堆叠（§6）；**小红书"收藏>点赞"权重高**，构成图能揭示内容"实用性强但情绪张力弱"（E1）。
- **关联**：CTR×涨粉散点，找"高曝光低转化"笔记（E1 关联思维：高曝光+低点击=封面问题）。
- **时间规律**：发布时段×涨粉热力图，指导最佳发布时间（§9，E2 Follower Activity）。
- **内容表现**：按选题/内容类型分组柱，识别"选题重复度上升→涨粉下降"（呼应前轮 CEO 质疑场景）。
- **External 状态**：Connector 未接入时显示"待连接 / 数据不可用"，**绝不显示 0 冒充无互动**（Data Trust 纪律）。

**共存原则**：Shared 区永远上方通用外壳，Domain 区下方本业务区带来源标注；切换 Business 只换 Domain 区——CEO 不会觉得每业务是一套不同 BI 软件（前轮 §7/§八）。

---

## 14. RD Domain Visualization（Curis 研发案例）

**Shared Metrics**：同上通用区。

**Domain Metrics（来源=RD 执行事实，部分 Runtime 已真实，见 Operating Intelligence Research §25）**：

- Build success、Test pass、Defect、Review cycle、Release frequency、返工、执行时间、模型使用。
- **趋势**：Build/Test 通过率折线 + 缺陷数折线（双线 small multiples，禁双 Y 轴）。
- **分布**：Defect 按模块/严重度箱线或直方图；Review cycle 时长分布（§7）。
- **漏斗**：RD 流程 编码→构建→测试→评审→发布，漏斗定位"测试阶段流失/返工回流"（§8）。
- **Before/After**：更换模型/流程调整后 Build/Defect/Review 前后对比（§10）。
- **构成**：时间花费按阶段堆叠（§6）；模型使用占比环形（§6）。

**注意**：RD 的 Usage/Cost 在 Curis Runtime 中**当前最真实**（real_rd_executor + usage_meter），是 Shared Metrics 可视化最早可落地的样本（Operating Intelligence Research §25 已确认）。

---

## 15. Chart vs Table vs Narrative 使用规则

> 不是"图越多越好"，也不是"为避 Dashboard 而全用文字"。三条媒介各司其职。

| 媒介               | 最适合                                                    | 不适合               | Curis 用法                  |
| ---------------- | ------------------------------------------------------ | ----------------- | ------------------------- |
| **图表 Chart**     | 模式发现、趋势、比较、分布、关系、构成                                    | 精确数值核对、长尾明细、可审计溯源 | Analyst 结论旁附图；CEO 看模式     |
| **表格 Table**     | 精确数字、多指标并陈、样本量/置信区间、Evidence 链接                        | 揭示趋势/关系（人眼读表慢）    | Benchmark、Report 元数据、下钻明细 |
| **叙述 Narrative** | FACT/INTERPRETATION/UNKNOWN/RECOMMENDATION、因果解释、不确定性声明 | 替代精确数字            | Analyst 报告正文；图/表之上        |

**组合范式（推荐进入 UX）**：

```
结论（Narrative 一句话）
+ 模式（Chart 一张，回答"为什么"）
+ 精确（Table 可展开，回答"具体多少"）
+ 证据（Evidence 链接，回答"从哪来"）
+ 追问（Conversation 入口，回答"再质疑"）
```

此范式直接对应前轮 Analyst Organization 的"Analyst 给结论 → Visualization 见模式 → Table 看数 → Evidence 验真 → Conversation 质疑"。

---

## 16. Curis Visualization Principles（Curis 可视化原则）

> 在沿用结论基础上，本轮修正并固化：

1. **问题优先，图表其次**：每个图必须能回答一个 CEO 经营问题；无法确定问题时不出图。
2. **不以 Dashboard 为心智，但不回避图表**：经营洞察的产品心智是"我的 AI 分析团队给我准备了什么"（前轮 §11），图是 Analyst 结论的视觉证据，不是入口。
3. **有效可视化优先于"像 BI"**：适合比较/趋势/分布/关系的数据必须用最有效图；不为避免 Dashboard 而退化成纯文字，也不为像 BI 而堆图。
4. **视觉编码守层级**：位置/长度 > 角度/斜率 > 面积 > 颜色；禁 3D、禁截断轴、禁 >5 片饼、禁量级悬殊双 Y 轴。
5. **分布比均值诚实**：凡涉及质量/耗时/成本，优先箱线/散点/直方图，均值柱需配分布。
6. **相对基线优于裸绝对值**：Goal 偏离、异常、Before/After 一律相对自身基线/目标带。
7. **图表必须可溯源**：每张图带来源、时间范围、Freshness、可比性声明；External 不可用显"待连接"而非 0。
8. **图看差异、表看精确、叙述给判断**：三媒介组合，AI 解读明确标 INTERPRETATION/UNKNOWN，不冒充 FACT。
9. **共享外壳、领域同屏**：Shared Metrics 上方通用区，Domain Metrics 下方本业务区；切换 Business 只换 Domain 区。
10. **不建第二套 Truth**：所有图的数据来自 Company OS 事实 + ai_usage 账本 + External Adapter，不复制 Employee/Business/Metric 真相。

---

## 17. 推荐进入下一轮 UX Exploration 的可视化模式

> 仅给出"哪些可视化模式值得在下一轮 UX 中落进交互原型"，不在此轮定稿。

| 优先级 | 可视化模式                              | 承载场景                         | 依赖                                        |
| --- | ---------------------------------- | ---------------------------- | ----------------------------------------- |
| P0  | 概览卡 + sparkline + delta（KPI strip） | 经营洞察首页 Company/Department 信号 | Shared Metrics 聚合（RD 真实，通用待补）             |
| P0  | 时间序列折线 + 基线带                       | 趋势/Goal 偏离/异常                | 同上                                        |
| P0  | 排序横向柱 + 小倍数                        | 模型/业务/员工比较                   | Benchmark 数据集                             |
| P0  | 漏斗 / 桑基                            | Workflow 瓶颈 / 返工回流           | Workflow/Stage 事实                         |
| P1  | 散点（Cost×Quality 等）                 | 关系/离群/破解"便宜=好"               | 多维 Shared Metrics                         |
| P1  | 热力图（时段/队列）                         | 时间规律 / 留存                    | 时间维度数据                                    |
| P1  | 堆叠/瀑布/环形                           | 构成与变化分解                      | 成本/Token 构成                               |
| P1  | 斜率图 / 前后分组柱                        | Before/After                 | 可比样本                                      |
| P1  | 箱线/小提琴                             | 分布与稳定性                       | 执行耗时/质量分布                                 |
| P1  | 容量-负载/负荷曲线                         | 组织过载/空岗                      | Capacity/Load 事实                          |
| P2  | Domain 同屏（内容/研发）                   | 小红书/研发领域图                    | Domain Metric Contract + External Adapter |
| P2  | External 状态标注（待连接/陈旧）              | Data Trust                   | Connector 状态                              |
| P2  | Report 卡 + 图嵌入                     | 报告体系                         | Report 对象                                 |

**下一轮 UX 建议**：在上一版 `CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html` 基础上，于"业务分析/模型基准/组织与员工"等视图中**嵌入上述 P0/P1 图族**，验证"Analyst 结论 → 图见模式 → 表看精确 → Evidence 验真 → Conversation 质疑"的组合范式是否流畅。本轮**不修改**该 HTML，留待下轮。

---

## 18. CEO 决议（Visualization 相关 — 已接受）

> 以下 6 项原"待 CEO 决策"已于 2026-08-18 CEO Review 全部接受（见 §19 状态与 Change Log 登记）：

1. ✅ 接受"图是 Analyst 结论的视觉证据"心智（原则 #2），不坚持首页零图、纯结论。
2. ✅ 接受 Model/Agent Benchmark 默认视图 = 排序横向柱 + 小倍数；散点（Cost×Quality）作为重要关系分析视图。
3. ✅ 接受分布图（箱线/散点）进入 CEO 默认视图与下钻。
4. ✅ 接受 External 数据"待连接"展示（灰显/占位/提示绑定），纳入 V1。
5. ✅ 接受 Before/After 强制"可比性声明"前置；系统不把不可比数据包装成可靠结论。
6. ✅ 接受图表可溯源到 Scope / Metric / Period / Source / Freshness / Responsible Analyst；不要求每张图成为独立 Asset。

---

## 19. 登记：三条 Product Delta（PENDING UX CONSOLIDATION）

CEO Review 同时登记以下三条 `CEO CONFIRMED PRODUCT DELTA — CONSUMED BY CURRENT PRODUCT TRUTH`，已由 **OPERATING INTELLIGENCE UX CONSOLIDATION** 与 Final Product Architecture Delta 消费；本轮不授权修改 Runtime / Schema / 代码。

- **A. Semantic-safe Visualization Switching**：同一 Dataset 在语义允许下可切换 Visualization（Trend: Line / Bar / Table；Model Comparison: Bar / Scatter / Table；Composition: Stacked / Donut / Table）。系统提供 Recommended Visualization，只允许切换到语义兼容图表，不允许任意错误转换。
- **B. Default Functional Analytics Organization**：Curis 默认 Company 应存在基础职能支撑组织，至少含**空间工程部 + 数据分析部**；数据分析部默认至少存在一名 Company Analyst / 公司经营分析师；Business Analyst 可属数据分析部并被分配到不同 Business，也可随业务组织成熟进入 Business 自身组织。此为 Product Delta，**暂不授权修改 Runtime / Schema**。
- **C. P0/P1/P2 仅研究/依赖参考**：研究中的 P0/P1/P2 优先级仅作研究与依赖参考，**不作为正式版本 Roadmap**；Curis 不为了版本迭代人为保留已确认且依赖满足的能力。

---

## 状态

**CURIS OPERATING INTELLIGENCE — DATA VISUALIZATION RESEARCH — ACCEPTED / REGISTERED**

> 2026-08-18 经 CEO Review 正式接受。状态：`APPROVED RESEARCH — CONSUMED BY CURRENT PRODUCT TRUTH`。
> 本轮仅产出研究文档，未修改任何 Current Product Truth（Blueprint / Master Map / UI Blueprint / Frozen Shell / Runtime / Schema / 代码 / 上一版 UX HTML 均未改动）。
> 已正式接受：7 项可视化原则、表达链（Analyst → Visualization → Table → Evidence → Conversation → Employee）、主要 Visualization Pattern、Model/Agent Benchmark 纪律（禁单一排行榜）、Data Trust 状态（External 未连接不显 0）、Before/After 可比性、图表溯源（Scope/Metric/Period/Source/Freshness/Responsible Analyst）。
> 并登记三条 Product Delta（A/B/C，见 §19），由后续统一 UX Consolidation 消费。
> 下一步不继续研究，等待 **OPERATING INTELLIGENCE UX CONSOLIDATION** 统一消费四轮研究（Operating Intelligence 产品研究 / Analytics UX Research / Analyst Organization / Analysis Work Loop / Data Visualization Research / Semantic-safe Visualization Switching / Default Analytics Department）。

**CURIS OPERATING INTELLIGENCE — DATA VISUALIZATION RESEARCH — WAITING FOR UX CONSOLIDATION**
