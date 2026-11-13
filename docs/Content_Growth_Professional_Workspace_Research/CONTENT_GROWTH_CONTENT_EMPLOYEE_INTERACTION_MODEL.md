# CONTENT GROWTH — CONTENT / EMPLOYEE INTERACTION MODEL
### Employee 三入口 · 内容生产 · 内容/素材库 · 反馈收件箱 · 分析与评估

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_FUNCTIONAL_INTERACTION_MODEL.md`（主模型 §2.6–2.8, 2.14）· `CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` · `CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`
前置：Domain Operating Model（阶段⑦⑧⑨⑩⑪⑭⑬⑮⑯）；Product Mapping（Draft/Asset=Artifact，Brief=Content Intent+Brief Work，Variant/Publication=Frozen 契约）；Product Experience（三入口 / 内容·反馈·增长与评估 Surface）。

---

## 0. 红线
- **Content Intent/Brief/Draft/Asset/Variant/Publication** 全部复用现有对象（Intent=Frozen 契约；Draft/Asset=Artifact；Brief=Work Result；Variant/Publication=Frozen 契约）。不新造。
- **比稿/版本有节制**：默认生成 1–3 版，不做无限版本生成器；历史版本挂在 Work 下可追溯。
- **Feedback 采集属 Channel，归一后 Signal 属 SHARED**：评论/私信跨 Channel 归集 → 转 Signal/Opportunity/Lead。
- **Analytics → 结论 → 建议**：不裸 Dashboard。

---

## 1. EMPLOYEE INTERACTION（§7，三入口模型）

### 1.1 三入口（无第四入口 `[CURIS-AUTH]`）
1. **直接对话（Direct Conversation）**：任意处输入即对话；可携带当前对象上下文。
2. **当前工作（Current Work）**：面板看员工正在做什么、进度、在途 Work。
3. **员工资料（Employee Profile）**：点员工名 → Quick Detail（右栏 Utility）。

### 1.2 场景细化（Content Growth）
- **在 Signal 里点 Employee** → Quick Detail（Utility）：姓名+责任+正在做+最近结果；点「对话」→ 直接对话携带该 Signal。
- **在 Topic 里「问王颖」** → 直接对话，自动携带 Topic 上下文（她说「补 3 个网站」即加进该 Topic 的 Research Scope）。
- **在 Research 里问 Employee** → 自动携带当前 Research 对象 + Scope（她继续查即续接该 Work，不新建）。
- **在 Current Work 看 Domain 信息**：显示该员工负责的 Content Growth 在途 Work（选题/研究/内容/发布）及状态，不含其他业务。
- **员工接收用户新增 URL/文件/关键词**：在对应 Work 内「添加来源/附件」→ 即时进入该 Work Scope。
- **员工完成 Result 后返回原对象**：Result 挂回原 Topic/Research/Content；点 Result → 看结论 + Evidence + 下一步。

> 所有「问员工」均经三入口之一，绝不新增第四、第五入口。

---

## 2. CONTENT PRODUCTION（§8）

### 2.1 从 Topic/Research 进入 Content
- Topic「就做这个」/ Research 结论「值得做」→ 自动创建 **Content Intent + Brief Work** → 进内容 Surface。

### 2.2 Brief / Draft / Version / Asset / Review / Channel Adaptation
- **Brief**：Intent（目标/受众/核心信息）+ Brief（结构/要点/调性/渠道初步）。CEO 默认只见推荐成品。
- **Draft 生成**：默认 1–3 版；用户可「再生成一版」。不做无限版。
- **用户修改**：直接在编辑器改 / **说话改**（「把开头改得更口语」→ 局部更新该 Draft）。
- **比稿**：Employee 在内容 Surface 并排多版（Comparison），标注差异；CEO 见推荐版 + 备选。
- **CEO 默认看到**：推荐成品 + 必要备选（不强制看全部版本）。
- **历史版本**：挂在 Work 下，可回滚/复用。
- **图片/视频/封面**：在资产库 + 内容 Surface Preview/Comparison（Utility）处理；可替换素材、局部重生成。
- **审核 / 标记可发布**：Draft → 审核（合规/品牌）→ 标「可发布」→ 进发布选择。
- **Channel Adaptation**：从 Intent 自动派生各账号 Variant（见 Channel 文件 §4），员工可逐账号微调。

### 2.3 不无限生成
- 版本上限由 Unit-Economics Auto-Selector 约束（单内容 Token/成本上限）；超出提示「已生成 N 版，建议选定或进入比稿」。

---

## 3. CONTENT LIBRARY / ASSET LIBRARY（§9）

### 3.1 是否分开
- **内容库**（Topic/Research Result/Brief/Draft/Published）与 **素材库**（Image/Video/Brand/Reusable Asset）建议**逻辑分开但同「资产与知识」Surface 下两个视图**：内容库管「做了什么」，素材库管「用什么做的」。
- 共享：Topic、Research Result、Brief、Draft、Published Content、Image、Video、Brand Asset、Reusable Asset。

### 3.2 操作
- **搜索/筛选/复用/关联/历史版本/Channel/Account/Campaign/Employee/时间**：全字段可搜可筛。
- **重点价值**：用户找「过去做过的东西」避免重 Research/重生成——如复用某爆款 Brief 结构、某视频素材、某 Brand Asset。
- **复用路径**：在内容 Surface「复用历史」→ 选历史资产 → 新 Intent 引用 → 省去重做。

---

## 4. FEEDBACK / INBOX（§16）

### 4.1 归集
评论 / 私信 / Mention / 投诉 / 高意向线索 跨 Channel 经 Channel Module 归集到反馈 Surface，归一化为统一格式（情感/意图/优先级）。

### 4.2 用户默认看什么 / Employee 处理什么
- **CEO 默认**：仅升级项（高风险投诉 / 高价值线索）→ 驾驶舱④/反馈 Surface 顶区。
- **Employee（Channel Operator）**：全量待处理队列，按情感/意图/优先级处理。

### 4.3 操作
- **筛选**：按渠道/类型/情感/意图/优先级/已处理。
- **回复**：在合规骨架内（官方接口 + 留资组件 + 防封）；高意向线索走官方留资卡，不直发微信号。
- **转 Signal / 转 Opportunity / 转 Lead / 标记已处理**：反馈 → Signal 回信息与机会 Surface（成为机会原料）；高意向 → Lead 进外部 CRM（经官方 API）。

### 4.4 升级 CEO
- 高风险投诉 / 重大舆情 / 合规临近 → 可能 Gate（讨论/暂停）。

---

## 5. ANALYTICS / EVALUATION（§17）

### 5.1 原始数据 vs 共享增长真相
- **Channel 原始数据**：各平台原生指标（阅读/播放/收藏/完播/互动），由 Channel Module 回收。
- **Shared Growth Truth**：跨渠道归一后的共享真相（如「收藏率↑12%」），是 Evaluation 的输入。

### 5.2 用户问「最近效果怎么样」
- **默认返回经营结论**（非裸指标）：例「收藏率提升 12%，主因是 GPT-5.6 选题切中搜索红利；建议下周续做同类并扩到抖音」。
- **深入才看**：Channel / Account / Content / Topic / 时间 / Metric 下钻。

### 5.3 Metric → Interpretation → Recommendation
- 每一指标自动配「为什么（Interpretation）+ 下一步建议（Recommendation）」。
- **多账号比较**：同 Content 跨账号表现对比，识别哪账号/哪渠道更有效。

### 5.4 进入下一轮
- 评估建议 → 回选题/策略（下一 Cycle）；重大策略调整超信封 → CEO Gate。

---

## 6. QUICK PATH CROSS-CHECK（§20）
- 用户：「帮我写一篇 GPT-5.6 小红书笔记」→ 停留 Conversation → 系统判 Quick（单条/低 stakes）→ 直接生成 + 单 Channel 适配 → 风险检查 → **1 次发布确认** → Result。
- **不因专业系统完善而变复杂**：Quick 路径不强制走选题池/Research/比稿；结构化能力在后台，用户无感。

---

## 7. 与 FINAL ACCEPTANCE 对应（本轮 §22 子集）
- Q5 点选题能干什么 → 见 Source/Topic 文件 §4.5
- Q6 让王颖调研 → §1.2
- Q7 补 3 网站 → §1.2
- Q8 Research 进 Content → Source/Topic 文件 §5.5
- Q9 Content 生成/修改/比稿 → §2
- Q10 图片视频在哪 → §2.2 / §3
- Q11 内容库复用 → §3
- Q19 评论私信回 Signal → §4.3
- Q20 Analytics 变建议 → §5
- Q21 Quick Path 简单 → §6

---

*CONTENT GROWTH CONTENT / EMPLOYEE INTERACTION MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
