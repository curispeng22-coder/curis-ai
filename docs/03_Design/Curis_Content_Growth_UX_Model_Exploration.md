# Curis Content Growth — UX Model Exploration

**Status**: Exploration（设计探索 · 非 Frozen · 非最终高保真 · 非前端代码）
**阶段**: PRODUCT / WORKSPACE DESIGN — UX & IA Exploration（第 1 份 / 共 5 份）
**上位依据**（按权威顺序）:
1. `Curis_Company_OS_Shared_Authority.md`（Frozen · ⑥ Responsibility Requirement / ⑧ Shared Employee Service Relation / ⑦ Organization Routing / Context Isolation Truth Boundary）
2. `Curis_Content_Growth_Domain_Authority.md`（Frozen · ① Office / ② Channel·Account·Pool / ③ Opportunity·Intent / ④ Target Account / ⑤ Variant·Publication / Distribution Execution Policy / Capability Truth）
3. `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7 · Shell Contract · Adaptive Surface）
4. `Curis_XHS_Workspace_Instance_Spec_v1.md` + `Curis_XHS_Workspace_Reference_Research.md`（当前已实现 XHS 实例与产品研究，作先例与未来迁移参考）
5. `Curis_Product_Blueprint.html`（v5.1 · Status: Review · 单一产品形态真源）

**本文件边界（最高优先级）**：
- 只解决「普通用户到底怎么理解和使用已经设计好的 Content Growth 系统」，不解决「系统怎么实现」。
- **不修改** Frozen Authority / Product Blueprint / XHS·RD Instance / Runtime / Connector / 代码 / UI。
- **不新建**业务 Primitive；**不为了 UI 修改**任何 Contract。
- 本文是 **DESIGN RECOMMENDATION**，不是 Authority，不得作为冻结引用。

> **Review 更新（2026-08-16 · APPROVED WITH 2 PRODUCT DELTAS）**：整体方向通过，OPTION D 通过但不进高保真。本轮按 **DELTA UX-1**（Content Growth = Business-level operating domain，≠ 超级 Professional Workspace；明确 Business Home 与 Professional Workspace 分工）与 **DELTA UX-2**（Office 用户面主词由「经营单元」改为「经营方向」，「经营单元」降级为帮助/高级/管理语境候选）修订全文，并产出 `Curis_Content_Growth_Product_Model_Closure.md` 作收口。不修改 Frozen Authority / Blueprint / XHS。

---

## 0. 为什么需要这一份（探索的出发点）

架构阶段已把 Content Growth 的底层模型冻结为一组精确但**内部**的语义：

> Office · Channel · Channel Account · OfficeAccountBinding · Account Pool · Content Opportunity · Content Intent · Target Account Set · Content Variant · Publication · Distribution Execution Policy · Responsibility Requirement · Organization Routing · Shared Employee Service Relation · Context Isolation · HIGH_REUSE · FULL_DIVERGENCE

这些词对设计系统的人是资产，对普通用户是噪音。本阶段唯一任务：把它们**翻译成用户本来就会说的语言与本来就想做的动作**，同时不破坏底层语义的正确性。

> 铁律：**Frozen Authority 决定「产品语义」；Contract Candidate / Review 决定「为什么这样设计」；两者都不能被机械地翻译成 UI。**

---

## 1. 第一原则：用户不学习架构

普通用户不应被要求理解以下任何词：

| 用户绝不应看到的词 | 用户应该看到的表达 |
|---|---|
| 创建 OfficeAccountBinding | 「添加你要经营的账号」 |
| 设置 Target Account Set | 「这条内容准备发到哪里？」 |
| BEST_EFFORT / ALL_REQUIRED | 「其他账号可以继续发」 / 「需要所有账号都准备好再一起发」 |
| Responsibility Requirement | （完全隐藏 — AI 自己知道该做什么） |
| Organization Routing | （完全隐藏 — 用户不配置路由） |
| Context Isolation | （默认隐藏 — 需要时「用了哪些资料」可查） |
| HIGH_REUSE / FULL_DIVERGENCE | 「Curis 会针对不同账号分别制作；能复用的自动复用」 |

设计判据：**如果用户需要打开一个叫「路由配置」或「绑定管理」的面板才能正常用 Content Growth，设计就失败了。**

---

## 2. 翻译层：内部语义 → 用户心智模型

> 术语的逐词映射见 `Curis_Content_Growth_User_Terminology_Map.md`。此处只给「体验层」的归并。

### 2.1 把「对象图」压成「用户想做的事」

底层对象链（Frozen）：
```
Company → Office → (Channel Account × N) → Content Intent → Target Account → Variant → Publication
```
用户心智里它应该是：
```
我想做内容、经营账号 → Curis 帮我发现值得做的选题 → 我接受 → Curis 针对不同账号分别制作 → 发到对应平台 → 数据回来
```

关键归并：
- **Office + Account Pool + Binding** → 用户只表达「我有哪些账号、它们属于哪个经营方向」。技术绑定关系不暴露。
- **Content Opportunity → Content Intent** → 用户只看到「一个值得做的选题」+「为什么值得做」+「建议哪些账号做」。O→I 的转化在背后发生。
- **Target Account Set（三源合并）** → 用户看到「默认勾选 + Curis 建议 + 你可改」。三源（Office 默认 / AI 推荐 / 手动）在背后裁决，用户只面对一个「发到哪里」的选择。
- **Variant + Publication** → 用户看到「每个账号分别做好了」+「已发布 / 待发布」。reuse_mode 不暴露。

### 2.2 什么完全隐藏、什么按需可见

| 层 | 用户可见性 | 理由（来自 Frozen） |
|---|---|---|
| Responsibility Requirement（⑥） | 完全隐藏 | Process asks WHAT，用户只说「帮我做内容」 |
| Organization Routing（⑦） | 完全隐藏 | ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE，用户不配置路由；Team Lead 仅异常也隐藏 |
| Shared Employee Service Relation（⑧） | 完全隐藏（结构上） | 员工跨 Office 服务是系统事实，用户只见「谁在负责」 |
| Context Isolation Truth Boundary | 默认隐藏，按需可追溯 | 用户可在需要时看「这条内容用了哪些资料 / 这个账号用哪套品牌资料」 |
| Queue / Bottleneck（⑨） | **不暴露为指标** | ⑨ 未 Frozen；仅在未来以 Frozen P7 白话建议呈现（VISION / RESERVED） |
| Distribution Execution Policy | 翻译为自然语言选项 | BEST_EFFORT / ALL_REQUIRED → 「其他账号可继续发 / 等全部准备好」 |

---

## 3. 内容增长对用户的核心价值命题

用户雇 Curis 做 Content Growth，不是为了「管理一个账号矩阵」，而是：

> **「我想让 Curis 帮我做内容、运营账号，最好我少操心、但该我定的时候能定。」**

据此，Content Growth 的体验主轴应是：

1. **发现**：Curis 主动告诉我「有什么值得做」。
2. **制作**：Curis 针对不同账号把内容做好，能复用的复用。
3. **发布**：按我选的账号发，状态清晰。
4. **回流**：数据回来，反哺下一轮选题。
5. **兜底**：只有真正需要我判断时才打断我。

这五件事里，**「制作」和「发布」在用户视角是同一件事的两个瞬间**，不该被切成两个独立 Workspace（详见 `Curis_Content_Growth_Workspace_Composition_Options.md` §9）。

---

## 4. 日常使用模型：Home 不是 Calendar / Pipeline / Dashboard

> XHS 当前首页是 Calendar，但**那是 XHS 单 Office·单账号实例的专业取向，不代表 Content Growth Home 也必须 Calendar**（Frozen Authority 不规定 Home 形状，这是设计选择）。

研究用户每天进入 Content Growth 最想知道什么（按需求强度排序，非固定 UI）：

1. **今天有什么值得做**（AI 发现的选题 / 待我接受的建议）
2. **正在生产什么**（哪些内容在制作中、谁在做）
3. **哪些内容待发布 / 刚发布**（发布节奏的轻量感知）
4. **哪些账号有新互动 / 异常**（评论、数据异常、OAuth 失效）
5. **AI 员工正在做什么**（谁在负责、卡在哪）
6. **哪些事需要我决定**（Needs CEO 汇总）
7. **最近哪些选题值得做**（选题库沉淀，进 Context Surface）

**结论**：Content Growth Home 应是一个 **Attention Surface + Light Operations Surface 的混合体**，而不是一个默认填满的 Calendar 或 Dashboard。

- **Attention Surface**：把「需要你注意 / 需要你决定」的事前置（遵循 Frozen P7 与 Shell 的 Decision Banner 机制）。
- **Light Operations Surface**：直接在主区完成「接受选题 / 看制作进度 / 确认发布 / 看数据」等轻操作，无需跳多个页面。
- Calendar / 排期 / 数据看板作为**按需专业面**（Utility / Context Adaptive Surface），不强制默认。

> 这与 XHS「内容对象 × 时间双主轴」并不冲突：双主轴约束的是「主工作区必须同时承载一篇内容和它在时间线上的位置」，Home 仍可在选中某条内容后展开为「内容 + 时间」视图。Home 是入口聚合，不是对双主轴的否定。

---

## 5. 一条内容的生命旅程（用户视角，非工程视角）

```
[AI 发现]  "很多用户在讨论 AI 浏览器"
     ↓  Curis 解释：为什么值得做（信号来源 / 受众匹配）
[你接受]  "这个选题值得做"  ← 用户只点接受，不创建对象
     ↓  Curis 建议：适合哪些账号（基于经营方向 / 历史表现 / 平台特性）
[你确认发到哪里]
     · 默认自动选择
     · Curis 推荐（"这个选题主要针对国内用户，暂不建议发 TikTok"）
     · 你可加减账号
     ↓  Curis 分别制作
     · 抖音：30 秒口播
     · 小红书：图文笔记
     · B站：8 分钟教程
     · TikTok：英文短视频（若你加了）
     ↓  发布（按你选的账号）
     · 每个账号独立显示 已发布 / 待发布 / 失败
     ↓  数据回流
     · 哪些表现好 → 反哺选题库
```

**用户全程只做四件事**：接受选题 / 确认发哪里 / 必要时调整 / 需要时拍板。其余都是 Curis 在背后按 Frozen Authority 运行。

---

## 6. AI 员工如何出现（绝不暴露路由）

用户主要看到的是**责任状态**，不是**调度机制**：

| 用户看到的 | 背后对应的（用户不需知） |
|---|---|
| 「内容策划 · 王芳 正在整理选题」 | Responsibility Requirement（⑥）+ Routing（⑦）解析出的 Holder |
| 「视频制作 · 陈真 正在做抖音版本」 | Employee（⑧）经 Assignment 服务该 Office |
| 「字幕 · 李翔 等待视频完成」 | 责任链 Handoff（P5）+ 当前 Responsibility（P1） |
| 「需要你决定：这条内容的品牌表述」 | Needs CEO（P7 / Frozen §3.13） |

**禁止出现的 UI**：Router 配置、Capacity 仪表、Assignment Policy 编辑器、Queue 规则设置。这些在 Frozen Authority 里由系统治理，用户只消费结果（「谁在负责 / 正在做 / 卡在哪 / 需我决定」）。

> 复用 XHS 先例（Reference Research Q4）：Employee Workstation 只在「需要看到某个 AI 员工正在做 / 卡在某件事」的节点浮现，**非常驻主区、不做常驻员工列表**。

---

## 7. 用户怎么增加员工（两条路径，都不暴露内部指标）

### 路径一：主动增加
用户想到「我需要一个人专门做字幕」→ 在员工入口说「加一名字幕员工」→ 看到的是「这个员工会做什么 / 大概增加什么成本」，不是 queue_depth / capacity score。

### 路径二：Curis 建议增加
```
Curis：「最近视频经常卡在字幕环节，建议增加一名字幕员工。」
你看到：为什么需要 / 增加后有什么变化 / 大概增加什么成本
你只需：[按建议增加] [暂时不用] [其他方案]
```
> 这是 **VISION / RESERVED 探索**：⑨ Queue/Bottleneck 未 Frozen，不得把未来 Candidate 画成当前确定功能。上述「卡在字幕」的归因只能以 Frozen P7 白话叙述（现象 + 可能原因 + 不确定性 + 一个建议），**不得显示 bottleneck score / 枚举名 / queue 指标**。

---

## 8. Context Isolation 对 UX 的影响（默认隐藏，按需可追溯）

Frozen：`Shared Employee ≠ Shared Context`。正常情况下用户**不应管理 Context Package**。

但用户可能需要**可解释入口**：
- 「这条内容用了哪些资料？」
- 「依据了哪些 Knowledge？」
- 「这个账号使用哪套品牌资料？」

设计原则：
- **默认隐藏**复杂上下文；
- **需要时可追溯**（在内容详情 / 账号详情里给一个轻量「资料来源」入口）；
- **不设计 Prompt 编辑器作为主要交互**（Frozen：Intent 禁存 Prompt / CoT；用户不写推理）。

---

## 9. Needs CEO 的边界（严格沿用 Frozen P7）

内容增长里**只有这些**升级 CEO Decision：

- 品牌方向调整
- 预算 / 投放确认
- 版权风险
- 合规风险
- 重要渠道变化
- 重大账号定位变化

**普通事项不打断 CEO**：
- 选题接受 / 制作 / 字幕 / 发布成功 / 普通评论 → 全自动（P4 Automation by default）

Decision 呈现严格遵循 Frozen §3.13（8 要素语义 + 三层信息层级 + Provenance + 复杂度感知动作 + 禁止编造）。内容增长只需填入领域内容，不重新发明 Decision 机制。

---

## 10. 设计纪律红线（本轮不可越）

- ❌ 修改 Frozen Authority / Product Blueprint / XHS·RD Instance。
- ❌ 写 Runtime / Connector / 正式前端代码。
- ❌ 画最终高保真 / 直接进入 Figma。
- ❌ 新建业务 Primitive（Office 等已是 Frozen 定义，只做用户面翻译）。
- ❌ 为了 UI 修改任何 Contract。
- ❌ 把 ⑨ Queue/Bottleneck 的未 Frozen 指标画成当前功能。
- ❌ 任何暴露 `OfficeAccountBinding` / `Target Account Set` / `BEST_EFFORT` / `HIGH_REUSE` / `FULL_DIVERGENCE` 原词的界面。
- ✅ 把内部语义翻成自然语言与轻操作。
- ✅ 复用 Shell Contract（Adaptive Surface / P1–P7）与 XHS 先例（内容对象 × 时间 / Low Surface Complexity）。

---

## 11. RECOMMENDED PRODUCT MODEL（DESIGN RECOMMENDATION · 非 Frozen）

> 完整方案比较见 `Curis_Content_Growth_Workspace_Composition_Options.md`；收口结论见 `Curis_Content_Growth_Product_Model_Closure.md`。此处给结论性推荐，供后续 Review。

**推荐模型（概要 · 融合 DELTA UX-1 / UX-2）**：

1. **IA 层级**：「内容增长」是 **Business-level operating domain**，挂在「业务空间」下（Blueprint 六区之子项），**不新增一级区、不新建 Primitive、不成超级 Workspace**。
2. **Content Growth Business Home / Operating Home**（用户常驻面）：负责 Attention / Light Operations / 经营方向切换 / 跨账号状态 / 跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback。首屏 = Attention + Light Operations 混合。
3. **Professional Workspace（专业深度工作面，按需进入）**：真正的深度工作在 Content Production / XHS Channel Operations / Douyin Channel Operations / Future TikTok·Bilibili·YouTube Operations 等。用户通过 **Shell Adaptive Surface / Deep Link** 自然进入，不感知「跳办公室」。体验上这些能力是一条**连续内容流**，但底层/IA 不把它们重新装进一个 Content Growth 超级 Workspace。
4. **经营方向（Office 用户面主词）**：组织容器但不是首屏负担；单账号隐去，多账号出现；「经营单元」降级为帮助文档/高级解释/管理语境候选，不进首版主 UI。
5. **一条内容流贯穿制作与分发**：Production 与 Channel Operations 在用户侧**合并为「做内容 → 发到所选账号 → 发布 → 回流」一个连续动作**，底层能力分层不暴露为两个 Workspace。
6. **AI 员工以责任状态浮现**，不暴露路由 / 容量 / 队列。
7. **增员**走「主动 + Curis 建议」两条路，指标全隐藏。
8. **Context 默认隐藏、按需可追溯**；**Needs CEO 仅重大事由**。

**为什么推荐这个（OPTION D 收敛）**：在 C 的「经营方向」容器上，叠加 A 的能力但不切页、吸收 B 的专业面但按需展开，形成 **「Content Growth Business Home + 经营方向 + 连续内容流 + 按需 Professional Workspace」** 的混合体。用户看到的是：

> 内容增长 → 今天值得做什么 → 某个经营方向 → 某条内容 → AI 制作 → 针对账号分别完成 → 发布 → 数据回流

而不是 Production Workspace / Channel Workspace / Routing / Variant / Target Set。

> 此推荐仅为 **DESIGN RECOMMENDATION**，待 Product Model Closure Review 批准（不进高保真 / 前端 / Instance Spec）。

---

*Curis Content Growth — UX Model Exploration · DESIGN RECOMMENDATION（非 Frozen）*
