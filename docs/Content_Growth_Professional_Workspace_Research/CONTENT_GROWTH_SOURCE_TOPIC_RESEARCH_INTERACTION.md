# CONTENT GROWTH — SOURCE / TOPIC / RESEARCH INTERACTION
### Source 信息管理 · Signal 信息池 · Opportunity · 选题池 · Research 完整模型

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_FUNCTIONAL_INTERACTION_MODEL.md`（主模型）· `CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md` · `CONTENT_GROWTH_CONTENT_EMPLOYEE_INTERACTION_MODEL.md`
前置：Domain Operating Model（阶段①②③④⑤⑥）、Product Mapping（Signal/Opportunity/Topic = Artifact + Surface 投影）、Product Experience（信息与机会/选题/研究与洞察 3 个 Surface）。

---

## 0. 本文件范围与红线
- 覆盖本轮 §2 Source / §3 Signal / §4 Opportunity / §5 Topic / §6 Research。
- **不发明对象**：Source = 配置型 Artifact（或 Channel/Connector 监控配置）；Signal/Opportunity/Topic = Artifact + 信息与机会·选题 Surface 投影；Research = Work+Result+Evidence。全部复用 Company OS。
- **CEO 不维护 Signal/选题全量池**：只通过驾驶舱投影看顶 3 变化与推荐 3 选题。

---

## 1. SOURCE / INFORMATION MANAGEMENT（§2）

### 1.1 Source 到底是什么
Source = **情报采集的原材料入口**。一类是「监控型」（平台账号/关键词/RSS/媒体，持续采），一类是「指定型」（用户粘的 URL/文件/指定官网，单次或限定使用）。它决定 Research 与 Signal 的质量下限。

### 1.2 支持的类型
| 类型 | 说明 | 采集方式 |
|---|---|---|
| Website | 单个站点 | 周期抓取 |
| Specific URL | 指定网页 | 单次/按需抓 |
| RSS | 订阅源 | 周期拉取 |
| Keyword | 关键词（全网/平台内） | 周期检索 |
| XHS Account | 小红书对标/参考账号 | 平台 API/RPA 监控 |
| Douyin Account | 抖音对标账号 | 同上 |
| TikTok Account | TikTok 对标 | 同上 |
| YouTube Channel | YouTube 频道 | API |
| Bilibili Account | B站账号 | API |
| Industry Media | 行业媒体源 | RSS/抓取 |
| Official Source | 官方/品牌源 | 抓取/API |
| User File | 用户上传文件 | 解析入库 |
| Existing Knowledge | 已沉淀 Knowledge | 直接引用 |

### 1.3 添加 Source（逐项）
- **直接粘 URL**：对话或 Research Work 内粘链接 → 系统自动识别是 Website/Specific URL/RSS → 弹确认「加到监控 / 仅本次使用」。
- **一次多个 URL**：粘多行/批量粘贴 → 逐个识别 → 列表预览 → 确认加入。
- **加一个账号（如 XHS 对标）**：设置区 Source → 选类型=XHS Account → 输入/授权账号 → 成为监控源（注意：这是「监控源」，与「Channel 发布账号」不同，后者在渠道 Surface）。
- **加关键词**：Source → 关键词 → 输入词 + 选范围（全网/指定平台）→ 保存。
- **设监控范围**：平台范围（XHS only / XHS+Douyin / 全网）、语言、地理。
- **设时间范围**：持续 / 近 7 天 / 近 30 天 / 自定义。
- **「仅使用这些来源」**：开关=ON → Research 只用指定源，不扩展。
- **「来源优先，允许扩展」**：开关=ON → 以指定源为主，遇空白自动扩展公开搜索（标记「扩展」）。
- **暂停**：保留配置停采（不删）。**删除**：彻底移除。**编辑**：改范围/时间/优先级/开关。
- **查看最近采集**：Source 详情看最近 N 条采集 + 时间。
- **失效**：标「失效」+ 原因（404/授权过期/反爬）→ 提示替换或重授权。
- **重新授权**：Channel 型源走平台重授权；网页型源改抓取策略。
- **来源可信度**：显示可信度标（官方高 / 媒体中 / UGC 低 / 未知），影响 Signal 强度加权。
- **避免变成复杂后台**：Source 管理集中在设置区低频区；日常由 Employee 维护；CEO 仅在「指定来源」情境偶发添加（如对话粘 3 个网站），不进全量后台。

### 1.4 Employee 在具体 Research Work 中消费 Source
- Research Work 的 Scope 直接引用 Source 集合；Employee 可临时加/限/换来源。
- 系统记录「本次用了哪些源、是否扩展、可信度」→ 进 Evidence。

---

## 2. SIGNAL / INFORMATION POOL（§3）

### 2.1 Signal 列表字段
| 字段 | 说明 |
|---|---|
| 来源 | 哪个 Source / 平台 |
| 摘要 | 自动生成的一句话 |
| 时间 | 采集时间 |
| 相关 Topic | 已关联选题（若有） |
| 强度 | 高/中/低（基于频次/情感/匹配度） |
| 可信度 | 来源可信度 × 内容置信 |
| 新旧状态 | 新 / 已读 / 已处理 |
| Employee 判断 | 自动标签 + 人工修正 |

### 2.2 操作
- **搜索/筛选/排序**：按来源/强度/可信度/时间/相关 Topic/已处理；排序默认时间倒序或强度。
- **聚类**：同主题 Signal 自动聚成簇（如「GPT-5.6 多源提及」）。
- **去重**：同源重复/跨源同事件去重，保留代表。
- **忽略**：软删，可恢复；**收藏**：置顶/标星；**转 Opportunity**：一键聚合进机会。
- **批量处理**：批量转 Opportunity / 忽略 / 归档。
- **过期**：超过时效窗自动降权/归档。
- **追溯 Source**：点 Signal → 看原文 + Source 链接。

### 2.3 Employee Working View vs CEO Projection
- **Employee Working View**：全量池、聚类、去重队列、强度计算依据、与历史对比、可调阈值。**主用「信息与机会」Surface**。
- **CEO Projection**：驾驶舱③「需关注变化」= 全量池压缩为 **3 条级**变化卡（摘要+来源+建议），不暴露池。CEO 不进全量池。

---

## 3. OPPORTUNITY（§4）

### 3.1 产生与共存
- **产生**：Signal 聚合（自动）/ Employee 建 / 用户对话输入（「这个方向值得做」）。
- **用户自建 vs 员工推荐共存**：都进同一 Opportunity 集合，标注「来源=用户/员工/系统」；用户建的也会被 Employee 评估价值。

### 3.2 最小表达（必填）
是什么 / 为什么值得关注 / 支持 Signal / 预计价值 / 时效 / 跨渠道潜力 / 成本 / 风险 / 负责 Employee / 建议下一步。

### 3.3 动作
- **继续观察**：留池，等更多 Signal。
- **进入选题**：转成 Topic（curated Opportunity）→ 进选题池。
- **立即 Research**：直接建 Research Work 论证。
- **忽略 / 讨论 / 合并**：忽略（软删）；讨论（开对话）；合并（与相似 Opportunity 合）。

---

## 4. TOPIC POOL（§5，本轮重点）

### 4.1 选题从哪里来
1. Opportunity「进入选题」→ 自动建 Topic。
2. Research 结论「值得做」→ 建 Topic。
3. AI 推荐（基于 Signal/Opportunity 评分）。
4. 用户手动输入（对话/选题 Surface 新建）。
- **AI 推荐 vs 手动 vs Opportunity**：都进同一 Topic 集合，标注来源；去重合并为同一候选。

### 4.2 去重 / 合并 / 评分 / 排序
- **去重**：相似标题/意图自动并为一个 Topic（保留多来源）。
- **合并**：手动把两个 Topic 合（如「GPT-5.6 办公」+「AI 办公实测」）。
- **评分**：维度=趋势强度 × 受众匹配 × 账号定位契合 × 竞争空缺 × 历史表现 × 时效 × 跨渠道潜力 × 成本/价值比。总分驱动排序与「推荐」标记。
- **排序**：默认按评分；可切时效/价值/跨渠道。
- **搜索/筛选**：按状态（推荐/研究中/已采用/已放弃/历史重复）/跨渠道/负责 Employee/标签。
- **收藏以后做**：标「暂缓」入收藏，不占推荐位。
- **放弃/恢复**：放弃=软删（可恢复）；恢复从回收区取回。

### 4.3 一个 Topic 应显示什么
标题 / 一句价值判断 / 来源 Opportunity / 时效 / 预计价值 / 研究深度建议 / 跨渠道潜力 / 状态 / 负责 Employee。（即 §2.4 卡面）

### 4.4 点击 Topic 以后默认看到什么
- Topic 详情 = 推荐理由 + 支撑 Evidence（来源 Opportunity/Research 结论）+ 关联 Research + 当前负责 Employee + 下一步建议 + 状态操作区。
- 不默认展开全量 Research/Signal，按需经 Utility 下钻。

### 4.5 动作（逐项）
- **就做这个**：→ 创建 Content Intent + Brief Work → 自动进内容 Surface（见 §6 与 OUTPUT 4 §8）。系统后台起 Brief，用户只见「已为你准备内容草稿」。
- **先调研**：→ 建 Research Work（Scope 带 Topic 上下文）。
- **直接生成**：→ Quick/Structured 直接出 Draft（跳过深度 Research）。
- **调整方向**：→ 改 Topic 价值判断/跨渠道/定位 → 回评分。
- **问员工**：→ 三入口·直接对话，携带 Topic 上下文。
- **暂缓**：→ 标暂缓，移出推荐。
- **放弃**：→ 软删。

### 4.6 Employee Working View vs CEO Review View
- **Employee Working View**：完整池 + 评分明细 + 去重候选 + 历史同类表现 + 跨渠道排期；用于筛选/维护/评分。
- **CEO Review View**：同一 Topic 对象的不同投影深度——只显示「推荐 3 个 + 理由 + 价值 + 建议」，不复制数据。**CEO 默认不强制维护池**。

---

## 5. RESEARCH（§6）

### 5.1 Research Work 产品行为
- **进入**：选题「先调研」/ 机会「立即 Research」/ 对话「研究一下 X」。
- **承载**：Research = Work（Canonical/Child）+ 闭合后 Result + Evidence。深度由 Scope 决定，不新造「Research 对象」。
- **必含字段**：Research Question / Scope / Source / Specified URL / Keyword / Competitor / Official Source / Evidence / Unknown / Conclusion / Recommendation。

### 5.2 用户可做的（CEO 视角最小化）
- 添加来源 / 删除来源 / 限定来源 / 补充问题 / 让员工继续查 / 停止 / 直接接受当前结论。
- CEO 默认只点「查看结论」，**不碰 Scope/来源**。

### 5.3 Employee 可做的（专业 Working View）
- 使用更完整专业工具：多源比对、竞品深挖、官方源核验、置信度计算、Unknown 显式标注。
- 可把 Research 拆 Child Work（如分平台调研）。

### 5.4 CEO 默认只看
结论 / 业务意义 / 价值 / 风险 / 未知 / 推荐 / Evidence 入口（见 Product Experience §3 投影合同）。

### 5.5 结束 → 进入 Content 的路径
- Research 结论「值得做」→ 回原 Topic（更新状态）→ 用户/Employee 点「就做这个」→ 自动创建 Content Intent + Brief Work → 进内容 Surface。
- 若结论「不值得」→ Topic 标放弃/暂缓，不进 Content。

---

## 6. 与 FINAL ACCEPTANCE 对应（本轮 §22 子集）
- Q1 加网址 → §1.3
- Q2 删 Source → §1.3
- Q3 加 XHS 对标账号 → §1.3
- Q4 选题池有什么 → §4.3
- Q5 点选题能干什么 → §4.5
- Q6 让王颖继续调研 → §4.5「问员工」+ §5.2
- Q7 补 3 个网站 → §1.3「直接粘 URL」+ §5.2「添加来源」
- Q8 Research 结束进 Content → §5.5

---

*CONTENT GROWTH SOURCE / TOPIC / RESEARCH INTERACTION — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
