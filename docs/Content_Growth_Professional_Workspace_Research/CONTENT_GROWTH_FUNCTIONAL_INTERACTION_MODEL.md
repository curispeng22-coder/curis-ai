# CONTENT GROWTH — FUNCTIONAL INTERACTION MODEL
### 核心对象逐项功能行为 · 产品细节研究

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md`（Source/Signal/Opportunity/Topic/Research）· `CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`（Channel/Account/Variant/Publishing/Calendar）· `CONTENT_GROWTH_CONTENT_EMPLOYEE_INTERACTION_MODEL.md`（Content/Asset/Employee/Feedback/Evaluation）
前置：本轮前 9 份交付（Domain Operating Model / Operating Matrix / Shared vs Channel / CEO Experience / Unit Economics / Product Mapping / Product Experience / User Journey / Current UI Reconciliation）。

---

## 0. 红线与对象基础

- **本研究性质**：把「内容增长业务模型」落到**每一个功能怎么用**，细到下一轮可直接画 IA / Wireframe。本轮**禁止画页面 / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority 修改**。
- **复用，不发明**：所有功能行为挂在已有 Curis 对象上（见 `CONTENT_GROWTH_PRODUCT_MAPPING_MODEL.md` §2）。Signal/Opportunity/Topic = **Artifact + Surface 投影**；Research/Brief/Evaluation/Publication = **Work/Result**；Variant/Publication 消费 Frozen 内容域契约；Channel = **Channel 对象 + Module + Connector**。
- **统一研究方法**（本轮 §1，应用于每一个核心对象）：
  1. 用户为什么需要它　2. 谁主要使用（CEO/Employee/两者）　3. 从哪里进入　4. 默认看到什么　5. 可执行动作　6. 新建　7. 编辑　8. 删除/暂停/归档　9. 搜索/筛选/排序　10. 多选/批量　11. 点击进入哪里　12. 如何继续下一步　13. 如何与负责 Employee 沟通　14. Result/Evidence 在哪　15. 异常/空/未连接　16. 什么操作需 CEO Gate　17. 如何保持小白简单　18. Employee Working View 多看到什么。
- 证据标记：`[CURIS-AUTH]`=消费 Frozen 语义（非修改）·`[CAND]`=候选建议。

---

## 1. 层级与入口基线（所有对象共用）

```
CEO Experience（投影层：只呈现 Result/Decision/Handoff）
  ↓
Workspace Main = 经营驾驶舱（默认 8 类结果类型，非 Surface）
  ↓
7 Professional Surfaces：信息与机会 / 选题 / 研究与洞察 / 内容 / 增长与评估 / 反馈 / 渠道
  ↓
Employee Work Area（按 Responsibility 执行）
  ↓
Work / Result / Evidence / Handoff / Decision / Cycle（Company OS 真源）
  ↓
Runtime（Autonomous Operating · Canonical/Child/Multi-Work · Responsibility Router · Capability · Connector）
```

- **三入口（Employee）**：直接对话（Conversation）/ 当前工作（Current Work）/ 员工资料（Employee Profile Quick Detail）。不得有第四入口 `[CURIS-AUTH]`。
- **Utility（右栏按需）**：Evidence / Source / Employee Quick Detail / Topic · Research Detail / Preview / Comparison / Channel Detail / Publish receipt。不承载全量池/库/裸 Dashboard。

---

## 2. 核心对象逐项功能行为

> 每个对象用上述 18 问模板。CEO=小白 CEO；Employee=负责员工。

### 2.1 Source（信息源）— 详见 OUTPUT 2 §2
- **为何需要**：研究/监控的原料；决定情报质量。「巧妇难为无米之炊」。
- **谁用**：Employee（Research&Intel）主用；CEO 仅在「指定来源」情境下偶尔添加（如补 3 个网站）。
- **进入**：设置区（低频）/ 任意 Research Work 内「添加来源」/ 对话中直接粘贴 URL 自动识别。
- **默认看到**：Source 列表 = 名称 + 类型图标 + 监控状态 + 最近采集时间 + 健康度。
- **动作**：添加 / 编辑 / 暂停 / 删除 / 查看最近采集 / 设监控范围·时间 / 设优先级。
- **新建**：粘 URL（自动识别 Website/Specific URL/RSS）；选账号类型加 XHS/Douyin 等账号；加关键词；选 Industry Media/Official/User File/Existing Knowledge。
- **编辑**：改范围、时间窗、优先级、是否「仅用这些来源」。
- **删除/暂停/归档**：删除（彻底）/ 暂停（保留配置停采）/ 归档（历史来源留痕）。
- **搜索/筛选/排序**：按类型/状态/健康度/最近采集；排序按最近采集或名称。
- **多选/批量**：支持批量暂停/删除/改优先级。
- **点击进入**：Source 详情（最近采集条目 + 健康度 + 失效原因）。
- **继续下一步**：作为 Research Work 的 Scope 输入。
- **与 Employee 沟通**：在 Research Work 内直接 @ 或「问王颖」携带当前对象。
- **Result/Evidence**：采集结果以 Signal(Artifact) 回流；Source 本身不存 Result。
- **异常/空/未连接**：无 Source→驾驶舱提示「先添加信息源」；失效→标「失效」并提示重新授权/替换；首次添加给引导。
- **CEO Gate**：否（配置类，Employee/Leader 默认处理）。
- **小白简单**：日常不碰；只在系统问「要指定来源吗」时粘链接；不要求理解监控机制。
- **Employee 多看到**：采集频率、去重规则、信号强度阈值、扩展搜索开关、失败重试日志。

### 2.2 Signal（信号）— 详见 OUTPUT 2 §3
- **为何需要**：把原始采集变成「值得注意的变化」，是机会的原料。
- **谁用**：Employee 主用（在「信息与机会」Surface）；CEO **不维护**，只看投影后的「需关注变化（3 条级）」。
- **进入**：信息与机会 Surface；驾驶舱③「需关注变化」是其压缩投影。
- **默认看到**：Signal 列表 = 摘要 + 来源 + 时间 + 相关 Topic + 强度 + 可信度 + 新旧标记。
- **动作**：查看 / 转 Opportunity / 收藏 / 忽略 / 聚类 / 去重 / 批量处理 / 追溯 Source / 过期。
- **新建**：通常由采集自动产生；Employee 也可手动建（如从对话洞察）。
- **编辑**：改强度/可信度/关联 Topic/标注（Employee）。
- **删除/暂停/归档**：忽略（软删，可恢复）/ 归档历史。
- **搜索/筛选/排序**：按来源/强度/可信度/时间/相关 Topic/已处理。
- **多选/批量**：批量转 Opportunity / 忽略 / 归档。
- **点击进入**：Signal 详情（完整原文 + Source 链接 + 自动判断说明）。
- **继续下一步**：转 Opportunity → 进入选题池评估。
- **与 Employee 沟通**：在 Signal 上「问王颖」→ 直接对话携带该 Signal。
- **Result/Evidence**：Signal 本身是 Evidence 的一种（轻量）；深度 Evidence 在 Research Work。
- **异常/空**：池空→提示「暂无新信号，已监控 N 个来源」；误报多→提示调阈值。
- **CEO Gate**：否。
- **小白简单**：CEO 永不进全量池；只看到顶 3 变化。
- **Employee 多看到**：聚类分组、去重队列、强度计算依据、自动判断理由、与历史 Signal 对比。

### 2.3 Opportunity（机会）— 详见 OUTPUT 2 §4
- **为何需要**：Signal 聚合后的「内容机会」，跨渠道复用，是选题的原料。
- **谁用**：Employee 生成与维护；CEO 在「选题」Surface 看到高价值 Opportunity（作为 Gate 输入）。
- **进入**：信息与机会 Surface（由 Signal 转来或 Employee/用户直接建）。
- **默认看到**：Opportunity 卡 = 是什么 + 为什么值得关注 + 支持 Signal + 预计价值 + 时效 + 跨渠道潜力 + 成本 + 风险 + 负责 Employee + 建议下一步。
- **动作**：继续观察 / 进入选题 / 立即 Research / 忽略 / 讨论 / 合并。
- **新建**：Signal 转 / Employee 建 / 用户对话中说「这个方向值得做」。
- **编辑**：改价值/时效/跨渠道/成本/风险/负责人。
- **删除/暂停/归档**：忽略 / 归档。
- **搜索/筛选/排序**：按价值/时效/跨渠道/状态/负责人。
- **多选/批量**：批量进入选题 / 忽略。
- **点击进入**：Opportunity 详情（所有 Signal + 判断依据）。
- **继续下一步**：「进入选题」→ 生成 Topic（curated Opportunity）。
- **与 Employee 沟通**：可「讨论」（开对话）。
- **Result/Evidence**：支持 Signal 即证据；深度论证在 Research。
- **异常/空**：无→提示从 Signal 转或新建。
- **CEO Gate**：高价值 Opportunity 跨渠道/超信封 → 进 Gate（确认取舍）。
- **小白简单**：CEO 只看「推荐机会 + 价值 + 建议」。
- **Employee 多看到**：信号置信度、竞争空白分析、历史类似机会成败。

### 2.4 Topic（选题）— 详见 OUTPUT 2 §5
- **为何需要**：经评分入选的 Opportunity，是「要做什么内容」的共识单元。
- **谁用**：Employee Working View（推荐子集+完整池）；CEO Review View（只看推荐 3 个）。
- **进入**：选题 Surface（独立工作面）。
- **默认看到**：Topic 卡 = 标题 + 一句价值判断 + 来源 Opportunity + 时效 + 预计价值 + 研究深度建议 + 跨渠道潜力 + 状态 + 负责 Employee。
- **动作**：就做这个 / 先调研 / 直接生成 / 调整方向 / 问员工 / 暂缓 / 放弃；搜索/筛选/排序/收藏/恢复/合并/去重。
- **新建**：从 Opportunity 转 / Research 结论来 / 用户手动输入 / AI 推荐。
- **编辑**：价值判断、状态、方向、跨渠道标注。
- **删除/暂停/归档**：放弃（软删可恢复）/ 暂缓 / 归档历史。
- **点击进入**：Topic 详情（推荐理由 + Evidence + 关联 Research + 当前负责 Employee + 下一步建议）。
- **继续下一步**：「就做这个」→ 创建 Content Intent/Brief Work → 自动进内容 Surface（详见 §2.7 与 OUTPUT 4 §8）。
- **与 Employee 沟通**：「问王颖」携带 Topic 上下文。
- **Result/Evidence**：来源 Opportunity + Research Result 即证据。
- **异常/空**：无推荐→提示「今天没有高价值选题，建议先 Research 或观察」；选题过多→按评分折叠。
- **CEO Gate**：进入制作（重大投入/超信封）→ 可能 Gate。
- **小白简单**：CEO 默认只看到「推荐 3 个选题 + 理由 + 价值」；不选、不维护。
- **Employee 多看到**：完整池、评分明细、去重候选、历史同类表现、跨渠道排期。

### 2.5 Research（调研）— 详见 OUTPUT 2 §6
- **为何需要**：把选题变成有 Evidence 的结论与建议，降低不确定性。
- **谁用**：Employee 执行（研究与洞察 Surface）；CEO 只看结论/意义/风险/未知/推荐。
- **进入**：选题「先调研」/ 机会「立即 Research」/ 直接对话「研究一下 X」。
- **默认看到（Employee）**：Research Question + Scope + Source 列表 + 进行中状态 + Evidence 草稿 + Unknown 区。
- **默认看到（CEO）**：结论 + 业务意义 + 价值 + 风险 + 未知 + 推荐 + Evidence 入口。
- **动作**：添加/删除来源、限定来源、补充问题、让员工继续查、停止、直接接受当前结论。
- **新建**：见上述进入方式；创建 Research Work（Canonical/Child）。
- **编辑**：改 Question/Scope/来源。
- **删除/暂停/归档**：停止（保留已得结论）/ 归档。
- **搜索/筛选/排序**：Evidence 按来源/可信度/时间。
- **多选/批量**：批量采纳 Evidence。
- **点击进入**：Research 详情（完整 Source/Scope/Evidence/Unknown/Conclusion/Recommendation）。
- **继续下一步**：结论「值得做」→ 回 Topic → 进内容（Brief Work）。
- **与 Employee 沟通**：在研究内「问王颖」自动携带该 Research 对象与 Scope。
- **Result/Evidence**：Research 闭合 = Result + Evidence 集合（回流 Workspace Truth）。
- **异常/空**：Research 失败→提示原因 + 建议（换来源/缩范围/人工）；无结论→显示 Unknown 并建议下一步。
- **CEO Gate**：高成本 Deep Research / 重大投入 → 可能 Gate（确认预算）。
- **小白简单**：CEO 只点「查看结论」；不碰 Scope/来源。
- **Employee 多看到**：完整工具、多源比对、置信度计算、竞品深挖、官方源核验。

### 2.6 Content Intent / Brief（内容意图/简报）— 详见 OUTPUT 4 §8
- **为何需要**：把「做什么内容」锁定为共享上游（WHY/WHAT/GOAL），下游多账号 Variant 复用。
- **谁用**：Employee（Producer）主用；CEO 只看推荐成品。
- **进入**：Topic「就做这个」→ 自动创建 Content Intent + Brief Work。
- **默认看到**：Intent（目标/受众/核心信息）+ Brief（结构/要点/调性/渠道初步）。
- **动作**：生成 Brief / 编辑 / 生成 Draft / 审核 / 标记可发布。
- **新建**：从 Topic 自动；或对话直接生成（Quick 路径也产生轻量 Intent）。
- **编辑**：改目标/受众/要点/调性。
- **删除/暂停/归档**：丢弃 Brief / 归档。
- **搜索/筛选/排序**：按 Topic/状态/渠道。
- **点击进入**：Brief 详情 + 关联 Draft/Variant。
- **继续下一步**：Brief 批准 → 生成 Draft / Channel Variant。
- **与 Employee 沟通**：「问 Producer」携带 Intent。
- **Result/Evidence**：Brief 本身 = Work 产物；Evidence = 支撑调研结论。
- **异常/空**：无 Brief→从 Topic 一键生成。
- **CEO Gate**：重大投入/多平台大制作 → 可能 Gate。
- **小白简单**：Quick 路径自动生成，CEO 只看到成品。
- **Employee 多看到**：比稿多版、渠道适配规则、合规预检明细。

### 2.7 Draft / Asset / Variant / Publication — 详见 OUTPUT 3 §13–14 与 OUTPUT 4 §8–9
- **Draft（草稿，Artifact）**：Work-in-progress 内容；默认看到推荐版（CEO）/ 全部版本（Employee）；动作=生成/修改/说话改/比稿/标记可发布；历史版本挂在 Work 下。
- **Asset（素材/资产，Artifact）**：图片/视频/封面/品牌资产；在「资产与知识」库复用；动作=上传/生成/替换/打标签/关联内容/复用历史。
- **Variant（账号变体，Content Variant）**：同一 Intent 发不同账号时的分叉产物；轻适配/重生成/完全不同三档；CEO 默认只见发布结果，Employee 见全部 Variant 对比。
- **Publication（发布真相，Result per-Account）**：由 Connector 回填 per-Account 状态（Ready/Needs Review/Needs Permission/Scheduled/Publishing/Published/Failed/Platform Reviewing/Rejected）；**绝不伪造单一「整体成功」**，保持 per-Account truth。

### 2.8 Feedback（反馈）— 详见 OUTPUT 4 §16
- **为何需要**：评论/私信/Mention/投诉/高意向线索跨 Channel 归集，转 Signal/Opportunity/Lead。
- **谁用**：Employee（Channel Operator）在反馈 Surface 处理；CEO 只看升级项（高风险/高价值线索）。
- **进入**：反馈 Surface（Channel Module 采集归一化）。
- **默认看到**：待处理队列 = 类型 + 渠道 + 情感/意图 + 优先级。
- **动作**：筛选 / 回复 / 转 Signal / 转 Opportunity / 转 Lead / 标记已处理。
- **新建**：采集自动；手动建（如从对话）。
- **编辑/删除**：标记状态 / 归档。
- **点击进入**：单条详情 + 上下文（原帖/用户/历史互动）。
- **继续下一步**：转 Signal→进信息与机会；转 Lead→进 CRM（外部）。
- **与 Employee 沟通**：「问 Channel Operator」携带该反馈。
- **异常/空**：无连接→提示连接渠道；无新反馈→「暂无」。
- **CEO Gate**：高风险投诉/重大舆情 → 可能 Gate（讨论/暂停）。
- **小白简单**：CEO 只看「X 条需关注反馈 + 建议」。
- **Employee 多看到**：合规红线校验、私信频次控制、防封策略、多渠道聚合。

### 2.9 Evaluation（评估）— 详见 OUTPUT 4 §17
- **为何需要**：把 Channel 原始数据变成「什么有效 + 为什么 + 下一步建议」。
- **谁用**：Employee（Strategist）在增长与评估 Surface；CEO 看结论与下一步。
- **进入**：增长与评估 Surface / 驾驶舱⑦增长变化。
- **默认看到（CEO）**：经营结论（如「收藏率↑12%，因选题 X」）+ 下一步建议。
- **默认看到（Employee）**：Metric → Interpretation → Recommendation 三层。
- **动作**：选范围（Channel/Account/Content/Topic/时间）、对比、下钻、生成下一轮建议。
- **新建/编辑**：评估由 Runtime 自动产 Result；可手动加注解。
- **删除/归档**：归档历史评估。
- **点击进入**：评估详情（原始数据 + 解读 + 建议）。
- **继续下一步**：建议 → 回选题/策略（下一 Cycle）。
- **与 Employee 沟通**：「问 Strategist」携带评估。
- **异常/空**：无数据→提示「先发布内容才有数据」；Connector 不可用→诚实标记。
- **CEO Gate**：策略重大调整 → 可能 Gate。
- **小白简单**：CEO 只问「最近效果怎样」得结论。
- **Employee 多看到**：原始指标、归因模型、跨账号对比、基准线。

### 2.10 Learning / Strategy Adjustment（学习/策略调整）
- **为何需要**：把评估与复盘沉淀为 Knowledge 与策略信封更新，驱动下一轮。
- **谁用**：Employee（Strategist）；CEO 裁决超信封变更。
- **进入**：增长与评估 Surface / 驾驶舱②经营重点。
- **默认看到**：当前策略信封 + 近期 Learning 摘要。
- **动作**：采纳 Learning（更新 Knowledge/信封）/ 提出信封变更。
- **新建/编辑**：Learning 由评估闭环自动建议；信封变更需 CEO Gate。
- **删除/归档**：归档旧 Learning。
- **点击进入**：Learning 详情 + 证据。
- **继续下一步**：信封内调整→下一 Cycle 自动；超信封→CEO Gate。
- **与 Employee 沟通**：「问 Strategist」。
- **异常/空**：无→维持信封。
- **CEO Gate**：**是**——Approved Strategy Envelope 越界（方向/定位/受众/变现/重大预算/不可逆外部承诺）强制 Gate `[CURIS-AUTH]`。
- **小白简单**：CEO 只在信封被建议变更时裁决。
- **Employee 多看到**：信封边界明细、历史调整记录、越界影响分析。

### 2.11 Channel（渠道）— 详见 OUTPUT 3 §10
- **为何需要**：XHS/Douyin/TikTok/YouTube/Bilibili/公众号/视频号是内容分发的终局层。
- **谁用**：Employee（Channel Operator）配置与运维；CEO 仅 awareness 时进入（选渠道/看真相/权限未就绪）。
- **进入**：渠道 Surface / 发布时选目标 / Context filter。
- **默认看到**：Channel 列表 = 名称 + 连接状态（Connected/Not Connected/Unavailable/Needs Permission/Failed）+ 账号数 + 最近发布。
- **动作**：添加 / 连接 / 断开 / 重新授权 / 查看状态 / 进 Channel-specific Module。
- **新建**：选平台 → OAuth/API 授权（官方）→ 成为 Channel 对象。
- **编辑**：改默认账号、发布默认、合规策略。
- **删除/断开**：断开（保留历史）/ 删除（彻底，谨慎）。
- **搜索/筛选/排序**：按状态/平台。
- **点击进入**：Channel 详情（账号列表 + 平台规则 + 分析 + 发布记录）。
- **继续下一步**：作为发布目标。
- **与 Employee 沟通**：「问 Channel Operator」。
- **异常/空**：未连接→诚实标记 + 引导连接；平台不支持 Connector→标记 Unavailable + 替代（RPA/手动）。
- **CEO Gate**：首次对外发布（重要外部动作）→ Gate。
- **小白简单**：系统后台自动处理格式适配/发布；用户多不感知 Channel。
- **Employee 多看到**：Connector 健康、平台规则更新、合规红线、API 限额。

### 2.12 Account（账号，多账号）— 详见 OUTPUT 3 §11
- **为何需要**：同 Channel 多个账号（如 XHS 主号/测评号/个人 IP），承载不同定位。
- **谁用**：Employee（Channel Operator）配置；CEO 仅选默认/切换时感知。
- **进入**：Channel 详情 → 账号列表；发布时选账号。
- **默认看到**：账号 = 名称 + 定位 + 授权状态 + 默认标 + 最近表现。
- **动作**：新增 / 命名 / 设定位(Audience/Tone) / 设默认 / 切换 / 分组 / 重授权 / 断开。
- **新建**：在 Channel 下「加账号」→ 平台授权 → 配定位/受众/调性。
- **编辑**：改定位/受众/调性/默认/分组。
- **删除/断开**：断开（保留历史内容）。
- **搜索/筛选/排序**：按定位/状态/表现。
- **多选/批量**：批量选发布目标 / 批量重授权检查。
- **点击进入**：账号详情（历史内容 + 表现 + 授权状态）。
- **继续下一步**：作为发布 Variant 目标。
- **与 Employee 沟通**：「问 Channel Operator」携带账号。
- **异常/空**：掉线/权限失效→标红 + 提示重授权 + 自动暂停该账号发布。
- **CEO Gate**：否（配置类）。
- **小白简单**：发布时系统推荐账号，用户勾选即可；不要求懂定位配置。
- **Employee 多看到**：授权令牌健康、内容定位匹配度、跨账号 Context 隔离保证。

### 2.13 Calendar（日历）— 详见 OUTPUT 3 §15
- **为何需要**：统一看多 Channel/多 Account 的 Draft/Scheduled/Published/Campaign，发现 Gap/Conflict。
- **谁用**：Employee（Producer/Channel Operator）更需要；CEO 通常不需要。
- **进入**：内容 Surface 内视图（OPEN QUESTION Z1/Z7，待 CEO 裁决层级）。
- **默认看到**：时间轴 = 各渠道各账号的排期 + 已发布 + Campaign 标记 + Gap/Conflict 提示。
- **动作**：拖拽排期 / 改时间 / 看某天详情 / 发现空白。
- **新建/编辑**：从发布排期自动落点；手动加。
- **删除/归档**：取消排期。
- **点击进入**：某天/某条目详情。
- **继续下一步**：排期→发布 Work。
- **与 Employee 沟通**：「问 Producer」。
- **异常/空**：无排期→提示「本周内容空白」。
- **CEO Gate**：否。
- **小白简单**：CEO 不强制用；驾驶舱已给发布结果。
- **Employee 多看到**：跨账号冲突、频率合规、养号节奏。

### 2.14 Employee（员工，三入口）— 详见 OUTPUT 4 §7
- **为何需要**：复杂过程由 AI 员工承担；用户通过三入口与之协作。
- **谁用**：CEO（三入口）/ Employee（彼此 Handoff）。
- **进入**：直接对话（任意处输入）/ 当前工作（Current Work 面板）/ 员工资料（点员工名→Quick Detail）。
- **默认看到（Quick Detail）**：姓名+责任+正在做什么+最近结果。
- **动作**：对话 / 查看当前工作 / 指派（Leader）/ 看资料。
- **新建/编辑**：Team 配置（Leader 职责，非用户日常）。
- **点击进入**：对话（携带当前对象上下文）/ Current Work / 资料。
- **继续下一步**：对话结果→创建 Work/Result。
- **与 Employee 沟通**：即三入口本身。
- **异常/空**：员工离线/失败→提示重试/转交。
- **CEO Gate**：否（组织内）。
- **小白简单**：点员工名或对话即可，无第四入口。
- **Employee 多看到**：彼此 Handoff、责任边界、专业工具。

### 2.15 Result / Evidence / Handoff / Decision（Company OS 真源）
- **为何需要**：所有阶段以这些对象承载，避免第二套 Runtime。
- **谁用**：Runtime 产出；CEO 看 Result/Decision 投影；Employee 看全量并 Handoff。
- **进入**：Result→驾驶舱/对象详情；Decision→驾驶舱④；Handoff→对象流转；Evidence→Utility。
- **默认看到**：Result=结论+价值+建议；Decision=待裁决+建议；Evidence=来源链。
- **动作（Decision）**：批准/调整/讨论/暂停（CEO 四选一）。
- **新建/编辑**：由 Work 闭合自动产；Leader 可手动建 Decision。
- **删除/归档**：归档历史。
- **点击进入**：对象详情 + 关联 Evidence/Handoff。
- **继续下一步**：Decision 裁决→next Cycle；Handoff→下一 Responsibility。
- **与 Employee 沟通**：Handoff 即传递。
- **异常/空**：无 Result→Work 进行中；无 Decision→无需裁决。
- **CEO Gate**：**是**——Decision 对象即 Gate 载体。
- **小白简单**：CEO 只点「批准/调整/讨论/暂停」。
- **Employee 多看到**：Handoff 明细、Work 子任务、Evidence 全量。

---

## 3. FINAL ACCEPTANCE — 21 问逐条回答（无需画页面，文字即明）

1. **我在哪里添加一个网址？** → 设置区「Source」加 URL；或任意 Research Work 内「添加来源」粘链接；或对话直接粘 URL 自动识别为 Source。
2. **我在哪里删除一个 Source？** → 设置区 Source 列表，点该 Source → 删除（或批量选中删除）；暂停=保留配置停采。
3. **我怎么添加一个小红书对标账号？** → 设置区「Source」选类型=XHS Account → 授权/输入账号 → 成为监控源；或在渠道 Surface 加 XHS Channel 后加对标账号为监控源。
4. **选题池里到底有什么？** → 经评分入选的 Opportunity（Artifact）：标题+价值判断+来源+时效+价值+研究建议+跨渠道+状态+负责 Employee。CEO 默认只见「推荐 3 个」。
5. **我点一个选题以后能干什么？** → 就做这个 / 先调研 / 直接生成 / 调整方向 / 问员工 / 暂缓 / 放弃（详见 §2.4 / OUTPUT 2 §5）。
6. **我怎么让王颖继续调研这个选题？** → 在 Topic 上「问王颖」（三入口·直接对话），自动携带该 Topic 上下文 → 她创建/续接 Research Work。
7. **我怎么给她补 3 个指定网站？** → 在 Research Work 内「添加来源」粘 3 个 URL，或对话中说「补充这 3 个网站」→ 自动加为 Scope 来源。
8. **Research 结束以后怎么进入 Content？** → Research 结论「值得做」→ 回 Topic → 「就做这个」自动创建 Content Intent + Brief Work → 进内容 Surface。
9. **Content 如何生成/修改/比稿？** → Topic→Brief→默认生成 1–3 版 Draft；用户说话改/直接改；Employee 在内容 Surface 比稿；CEO 默认见推荐版+备选（OUTPUT 4 §8）。
10. **图片视频在哪里处理？** → 资产库（Artifact）+ 内容 Surface 内 Preview/Comparison（Utility）；替换素材、局部重生成在此。
11. **内容库在哪里复用历史资产？** → 资产与知识 Surface / 库；按 Topic/Channel/Account/Campaign/Employee/时间搜索复用，避免重 Research/重生成。
12. **我怎么连接小红书/抖音/TikTok/YouTube/B站？** → 渠道 Surface / 设置区「Channel」→ 选平台 → 官方 OAuth/API 授权 → 成为 Channel 对象（OUTPUT 3 §10）。
13. **一个 Channel 多个账号怎么管理？** → Channel 详情→账号列表，加账号→授权→配定位/受众/调性/默认/分组；查看授权状态，掉线标红（OUTPUT 3 §11）。
14. **发布时如何选择具体账号？** → 发布目标选择 = Channel→Account→Variant 树；默认推荐/最近使用/多选/全选；不 Eligible/未连接/权限不足诚实标记（OUTPUT 3 §12）。
15. **一个内容如何生成多个账号 Variant？** → 同一 Content Intent 按账号自动轻适配/重生成/完全不同（三档）；Employee 见全部 Variant 对比，CEO 只见发布结果（OUTPUT 3 §13）。
16. **某个账号掉线怎么办？** → 标红「授权失效」→ 提示重授权 → 自动暂停该账号发布；历史内容与表现保留可查。
17. **多账号发布状态怎么看？** → 发布 Result 保持 per-Account truth：Ready/Needs Review/Needs Permission/Scheduled/Publishing/Published/Failed/Platform Reviewing/Rejected；不伪造整体成功（OUTPUT 3 §14）。
18. **Calendar 到底解决什么？** → 统一多 Channel/多 Account 的 Draft/Scheduled/Published/Campaign，发现 Gap/Conflict；Employee 主用，CEO 通常不需（OUTPUT 3 §15）。
19. **评论/私信如何回到 Signal？** → 反馈 Surface 采集归一化 → 「转 Signal」→ 进信息与机会 Surface，成为机会原料（OUTPUT 4 §16）。
20. **Analytics 如何变成下一步建议？** → 原始数据→共享增长真相→评估(Interpretation)→Recommendation→回选题/策略下一 Cycle（OUTPUT 4 §17）。
21. **Quick Path 为什么仍然简单？** → 用户一句话「帮我写篇 GPT-5.6 小红书笔记」停留 Conversation；系统按价值/复杂度自动选路径；1 句→结果→1 次发布确认，绝不逼用户学 Workflow/选员工/配流程（OUTPUT 4 §7 / Product Experience §7）。

---

*CONTENT GROWTH FUNCTIONAL INTERACTION MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
