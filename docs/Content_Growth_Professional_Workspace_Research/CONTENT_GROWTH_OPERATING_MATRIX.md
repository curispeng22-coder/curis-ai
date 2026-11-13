# CONTENT GROWTH — OPERATING MATRIX
### 每个 Stage：Input / Employee / Method / Tool / Result / Evidence / Handoff / Cost / Reuse / CEO Projection / UI Need

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen）
Companion: `CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` · `CONTENT_GROWTH_SHARED_VS_CHANNEL_MATRIX.md` · `CONTENT_GROWTH_CEO_EXPERIENCE_MODEL.md` · `CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md`

---

## 阅读说明
- **Employee** 用责任角色（见 Domain Model §6），不按步骤拆人；同一员工可跨多 Stage。
- **层**：`[S]`=SHARED（Content Growth 层，建一次）· `[C]`=CHANNEL（XHS/Douyin 等，封装在 Module+Connector）· `[H]`=HYBRID。
- **CEO Projection** 列即 OUTPUT 4 的「内部复杂度 → CEO 投影」投影结果。
- 证据标记：`[REAL][COMP][CURIS-AUTH][INF][CAND]`（定义见 OUTPUT 1 §0.3）。

---

## ① 信息搜集 Information Gathering  `[S]`
- **Input**：经营目标、受众定义、对标账号集、关键词集、关注 URL/媒体源、历史内容/数据。
- **Employee**：Research & Intelligence。
- **Method**：指定来源 → 持续监控（定时/触发）→ 去重 → 过滤 → 原始条目入 Signal 候选。
- **Tool/Capability**：平台搜索 API/爬虫、监控（BuzzSumo/Ahrefs/千瓜/飞瓜/新抖/蝉妈妈/今日热榜）、RSS、用户文件读取、去重/过滤规则 `[COMP]`。
- **Result**：结构化原始信号候选（来源/类型/时间/摘要）。
- **Evidence**：监控覆盖度、去重命中率、来源可信度标记。
- **Handoff**：→ ② Signal Pool。
- **Cost**：低（监控自动化）；人工仅定来源与边界 `[COMP]`。
- **Reuse**：信号源配置可复用；信号本身跨选题复用。
- **CEO Projection**：「已监控 N 个来源，本周新增 M 条相关信号」（不呈现原始流）。
- **UI Need**：源配置面板（低频）+ 信号源健康度；**非**默认 Main。

## ② 信息池 / Signal Pool  `[S]`
- **Input**：① 的原始信号候选。
- **Employee**：Research & Intelligence。
- **Method**：归一化、打标（类型/情感/强度）、关联经营目标、形成 Signal 对象。
- **Tool/Capability**：Signal Schema（类型/来源/强度/关联目标）、去重与聚类 `[CAND]`。
- **Result**：Signal 对象池（可查询、可聚合）。
- **Evidence**：Signal 数量/分布/Top 信号。
- **Handoff**：→ ③ Opportunity Discovery。
- **Cost**：低。
- **Reuse**：Signal 跨周期复用，沉淀为趋势记忆。
- **CEO Projection**：「今天有 3 个变化值得关注：…」（内部 300 条 → 3 条）。
- **UI Need**：信号归集视图（专业 Surface，追溯用）；默认不呈现全量。

## ③ 机会发现 Opportunity Discovery  `[S]`
- **Input**：Signal 池。
- **Employee**：Research & Intelligence。
- **Method**：Signal 聚合 → 模式识别 → Opportunity（什么值得做/为什么/服务什么目标）。
- **Tool/Capability**：趋势聚类、受众痛点映射、竞争空白识别 `[INF]`。
- **Result**：Opportunity 候选（source/topic/score，不绑账号/平台）`[CURIS-AUTH: Content Opportunity]`。
- **Evidence**：机会评分依据（信号支撑度）。
- **Handoff**：→ ④ Topic Pool。
- **Cost**：中（需判断）。
- **Reuse**：Opportunity 可服务多 Office/多 Intent `[CURIS-AUTH: INTENT_SHARED_UPSTREAM]`。
- **CEO Projection**：「发现 2 个高潜机会：A（趋势上升）、B（竞争空白）」。
- **UI Need**：机会卡片（价值+依据）；非原始池。

## ④ 选题池 Topic Pool  `[S]`
- **Input**：Opportunity + 历史表现 + 账号定位。
- **Employee**：Research & Intelligence（+ Strategist 终审）。
- **Method**：按 趋势/受众/定位/竞争/历史/缺口/时效/成本/跨渠道潜力 评分 → 入选题池并排优先级。
- **Tool/Capability**：选题评分模型、常青树池、热点日历 `[COMP]`。
- **Result**：优先级选题池（curated）。
- **Evidence**：评分维度与历史对标。
- **Handoff**：→ ⑤ Topic Judgment（高价值进 CEO Gate）。
- **Cost**：中。
- **Reuse**：选题库是资产（分类存储模板实现日更）`[COMP]`。
- **CEO Projection**：「推荐 3 个选题：①…价值…②…③…；建议先做 ①」。
- **UI Need**：推荐视图（CEO 默认可见子集）+ 完整池（专业 Surface）。

## ⑤ 选题判断 Topic Judgment  `[S] + CEO Gate`
- **Input**：选题池候选项。
- **Employee**：Growth Strategist（终审）。
- **Method**：战略对齐、资源评估、风险识别；高价值/高投入/超策略边界 → CEO Gate。
- **Tool/Capability**：策略信封（Approved Strategy Envelope）比对 `[CURIS-AUTH §0.2]`。
- **Result**：入选选题（或 WAIT/SKIP/STOP）。
- **Evidence**：判断依据、与定位/目标的吻合度。
- **Handoff**：→ ⑥ Research 或 → ⑦ Brief。
- **Cost**：低-中（决策为主）。
- **Reuse**：判断逻辑沉淀为策略知识。
- **CEO Projection**：「3 选 1 已定，方向符合本季重点；1 个高价值机会需您确认预算」。
- **UI Need**：决策卡（批准/调整/讨论/暂停）；**CEO Gate 仅此处触发**。

## ⑥ 调研 Research / Deep Research  `[S]`
- **Input**：入选选题；研究问题 + Scope。
- **Employee**：Research & Intelligence。
- **Method**：研究问题 → 范围 → 指定 URL/平台搜索/竞品/官方源 → 证据 → 未知项 → 结论。**按内容「保质期」」决定深度**；短保质期热点常刻意 SKIP `[COMP][INF]`。
- **Tool/Capability**：Deep Research（多源）、官方源检索、竞品分析 `[REAL]`。
- **Result**：研究结论 + 证据包 + Unknowns。
- **Evidence**：引用来源、证据强度。
- **Handoff**：→ ⑦ Brief。
- **Cost**：高（Deep Research 最贵，白皮书 $3k–10k 当量）`[REAL]`；故按需。
- **Reuse**：研究结论入 Knowledge，跨选题复用。
- **CEO Projection**：「结论：X 成立，意味着…；建议…；3 处未知待证实」。
- **UI Need**：研究简报（结论优先）；原始数据库专业 Surface 追溯。

## ⑦ 内容策略 / Brief  `[S]`
- **Input**：选题 + 研究结论 + 定位/调性。
- **Employee**：Growth Strategist（+ Producer）。
- **Method**：写 Brief（受众/目标/核心信息/调性/CTA/合规禁词/渠道策略）。
- **Tool/Capability**：Brief 模板、品牌语气库、合规禁词表 `[COMP]`。
- **Result**：Content Intent（WHY/WHAT/GOAL，结论性，**禁存推理/CoT**）`[CURIS-AUTH: INTENT_EXCLUDES_INFERENCE]`。
- **Evidence**：Brief 与策略信封一致。
- **Handoff**：→ ⑧ Content Creation。
- **Cost**：中。
- **Reuse**：Intent 为共享上游，可产 N 账号变体 `[CURIS-AUTH: INTENT_SHARED_UPSTREAM]`。
- **CEO Projection**：「已定方向：讲 X，目标 Y，调性 Z；将分 N 渠道适配」。
- **UI Need**：Intent/Brief 视图（共享 Surface）。

## ⑧ 内容创作 Content Creation  `[S]（核心观点）`
- **Input**：Brief / Intent。
- **Employee**：Content Producer。
- **Method**：生成核心观点内容（标题/正文/脚本骨架），**不做无限版本**；刻意 A/B 但限量 `[COMP]`。
- **Tool/Capability**：生成式写作/多模态、版本管理 `[REAL]`。
- **Result**：渠道无关的核心草稿（shared asset 雏形）。
- **Evidence**：与 Brief 吻合、可读性。
- **Handoff**：→ ⑨ Asset Production / → ⑪ Channel Adaptation。
- **Cost**：中（AI 初稿快 10–50×，但品牌/合规仍须人核）`[COMP]`。
- **Reuse**：核心观点跨渠道复用（1 长文→多形态）`[COMP]`。
- **CEO Projection**：「推荐成品 + 1 备选；已对齐 Brief」。
- **UI Need**：草稿/版本对比视图（专业 Surface）。

## ⑨ 素材生产 Asset Production  `[S 核心 + C 格式]`
- **Input**：核心草稿。
- **Employee**：Content Producer。
- **Method**：图文/视频/封面生产；共享资产（核心创意）与渠道格式资产分离。
- **Tool/Capability**：图像/视频生成、剪映/Canva 批量、资产库 `[COMP]`。
- **Result**：可复用资产（核心创意 + 渠道格式包）。
- **Evidence**：资产可用性、格式合规。
- **Handoff**：→ ⑩ Review / → ⑪ Adaptation。
- **Cost**：中-高（视频高）。
- **Reuse**：**核心资产跨渠道高复用**；格式包按渠道。
- **CEO Projection**：「素材就绪：主视觉 + 3 渠道格式包」。
- **UI Need**：资产库（共享 Surface，跨渠道复用）。

## ⑩ 审核 Review / Approval  `[S 合规闸 + C 平台规则]`
- **Input**：草稿 + 素材。
- **Employee**：Growth Strategist（终审）/ Channel Operator（平台规则）。
- **Method**：SHARED 合规闸（禁词/AI 标识/AIGC 标注/广告法）+ CHANNEL 平台规则校验。
- **Tool/Capability**：违禁词检测、AI 标识校验、平台规则引擎 `[REAL][COMP]`。
- **Result**：审核通过 / 驳回（附原因）。
- **Evidence**：审核记录、违规拦截。
- **Handoff**：→ ⑪ Adaptation（通过）。
- **Cost**：低-中。
- **Reuse**：审核规则沉淀。
- **CEO Projection**：「N 条待发，已通过合规；1 条 AI 标识需补」。
- **UI Need**：审核卡（通过/驳回+原因）；**Human-in-the-loop 默认**。

## ⑪ 渠道适配 Channel Adaptation  `[分叉点 H]`
- **Input**：审核通过的 Intent + 资产。
- **Employee**：Content Producer（+ Channel Operator）。
- **Method**：**在此分叉**——共享观点 → 按账号生成 `Content Variant`（HIGH_REUSE 轻适配 / FULL_DIVERGENCE 重产）`[CURIS-AUTH]`。
- **Tool/Capability**：CHANNEL Module（格式适配：XHS 3:4 首图/收藏钩子；抖音 9:16/前3秒）`[COMP]`。
- **Result**：每选中账号一份 Variant（绑单一账号）`[CURIS-AUTH]`。
- **Evidence**：变体合规、上下文隔离（不携其他账号 tone）`[CURIS-AUTH: NO_CROSS_ACCOUNT_CONTEXT_LEAK]`。
- **Handoff**：→ ⑫ Publishing。
- **Cost**：中（按复用模式）。
- **Reuse**：HIGH_REUSE 摊薄成本。
- **CEO Projection**：「将发 XHS+抖音，已按各平台格式适配」。
- **UI Need**：变体对比（专业 Surface）；默认不呈现分叉细节。

## ⑫ 发布 Publishing  `[C]`
- **Input**：Variant + Target Account Set（账号粒度，三源合并裁决）`[CURIS-AUTH]`。
- **Employee**：Channel Operator。
- **Method**：经 Channel Connector 发布；**默认 Human-in-the-loop**；仅三条件齐备（开放平台权限+合规预审+养号达标）才受控自动发布 `[CAND]`。
- **Tool/Capability**：XHS 开放平台/聚光/私信通、抖音巨量/蓝V；定时发布（XHS ≤7天原生，CONDITIONAL）`[COMP][CURIS-AUTH: SCHEDULING_IS_CONDITIONAL]`。
- **Result**：`Publication`（per-Account 真相，receipt 由 Connector 回填）`[CURIS-AUTH]`。
- **Evidence**：publish_receipt（不得伪造）`[CURIS-AUTH: RECEIPT_FROM_CONNECTOR]`。
- **Handoff**：→ ⑬ Data Recovery。
- **Cost**：低（执行）；合规风险高。
- **Reuse**：发布模板/节奏可复用。
- **CEO Projection**：「已发布 XHS（阅读中）/抖音（审核中）；异常将提示」。
- **UI Need**：发布状态（per-Account 真相）；**非跨账号整体状态** `[CURIS-AUTH]`。

## ⑬ 数据回收 Data Recovery  `[C 原始 → S 真相]`
- **Input**：平台原始数据（完播/收藏/3秒/打开率）。
- **Employee**：Channel Operator → Research & Intelligence。
- **Method**：CHANNEL 原始拉取 → 归一化为 SHARED 增长真相（跨渠道可比口径）。
- **Tool/Capability**：平台分析 API/三方（千瓜/蝉妈妈/GA4/Metricool）`[COMP]`。
- **Result**：共享增长真相（归因就绪）。
- **Evidence**：数据覆盖、口径一致性。
- **Handoff**：→ ⑭ Feedback / → ⑮ Evaluation。
- **Cost**：低-中。
- **Reuse**：真相跨周期对比。
- **CEO Projection**：「本周 XHS 收藏率↑12%，抖音完播↓5%」。
- **UI Need**：共享增长真相视图（专业 Surface）；非孤立 Dashboard。

## ⑭ 用户反馈 User Feedback  `[C 收件箱 → S 信号]`
- **Input**：评论/私信/@提及/评价。
- **Employee**：Channel Operator（+ Strategist 高价值）。
- **Method**：CHANNEL 统一收件箱（私信通/授权三方IM/蒲公英）→ 分类（情感×意图）→ 线索 → 回流 SHARED Signal `[COMP]`。
- **Tool/Capability**：CHANNEL 反馈 Module + 私信合规（留资卡/防封）`[COMP]`；**遵守 2026-05 私信三大红线** `[COMP]`。
- **Result**：结构化反馈 + 线索 + 新 Signal。
- **Evidence**：回复时效、合规无违规。
- **Handoff**：→ ②/③ Signal 回流。
- **Cost**：中（合规敏感）。
- **Reuse**：反馈→信号闭环。
- **CEO Projection**：「2 条高意向评论已转线索；1 起投诉已处理」。
- **UI Need**：反馈收件箱（CHANNEL Module）；合规骨架内置防封。

## ⑮ 效果评估 Evaluation  `[S]`
- **Input**：增长真相 + 反馈。
- **Employee**：Growth Strategist（+ Research）。
- **Method**：归因（标题/钩子/互动引导特征）→ 经营判断 → 下一轮选题/策略建议。
- **Tool/Capability**：归因模型、决策树（播放低→改封面；完播低→精简）`[COMP]`。
- **Result**：评估结论 + 下一轮假设。
- **Evidence**：指标变化与动作关联。
- **Handoff**：→ ⑯ Learning。
- **Cost**：中。
- **Reuse**：评估方法沉淀。
- **CEO Projection**：「什么有效、为什么、下一步建议」。
- **UI Need**：评估摘要（CEO 可见）+ 明细（专业 Surface）。

## ⑯ Learning / Strategy Adjustment  `[S]`
- **Input**：评估结论。
- **Employee**：Growth Strategist。
- **Method**：更新 Knowledge/策略信封；在 Approved Strategy Envelope 内调 tactic/cadence/experiment `[CURIS-AUTH §0.2]`；超边界 → CEO Gate。
- **Tool/Capability**：Knowledge 库、策略信封。
- **Result**：策略更新 + 下一 Cycle 假设。
- **Evidence**：策略版本、假设可验证。
- **Handoff**：→ 下一周期 ①/④/⑤。
- **Cost**：低。
- **Reuse**：Learning 复利（核心杠杆）。
- **CEO Projection**：「策略微调：增加 X 类选题；已记录」。
- **UI Need**：策略演进视图（专业 Surface）。

---

## 矩阵读法小结
- **SHARED 阶段（建一次）**：①②③④⑤⑥⑦⑧⑨(核心) ⑩(闸) ⑬(→真相) ⑭(→信号) ⑮⑯。
- **CHANNEL 阶段（每渠道封装）**：⑪(格式) ⑫(发布) ⑬(原始) ⑭(收件箱) ⑩(平台规则)。
- **CEO Gate 仅 ⑤ 高价值 / ⑯ 超边界**触发；日常由 Team 自主推进。
- **成本拐点**：⑥ Deep Research 最贵→按需；⑧⑨ 复用摊薄；⑫ 合规风险最高→Human-in-the-loop。

---

*CONTENT GROWTH OPERATING MATRIX — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
