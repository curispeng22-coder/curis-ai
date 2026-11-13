# Curis Content Growth — Product Model Closure

**Status**: PRODUCT MODEL RECOMMENDATION / REVIEW（设计建议 · 非 Frozen · 非高保真 · 非前端代码 · 非 Runtime/Connector）
**阶段**: PRODUCT / WORKSPACE DESIGN — UX / IA Exploration 收口（基于 5 份 Exploration 文档 + 本次 Review 的 2 个 Product DELTA）
**上位依据**（不修改）:
- `Curis_Company_OS_Shared_Authority.md`（Frozen · ⑥⑧⑦ + Context Isolation）
- `Curis_Content_Growth_Domain_Authority.md`（Frozen · ①②③④⑤ + Distribution Execution Policy + Capability Truth）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7）
- `Curis_Product_Blueprint.html`（v5.1 · Status: Review）
- 5 份 Exploration：`Curis_Content_Growth_{UX_Model,Information_Architecture,First_Run_Experience,User_Terminology_Map,Workspace_Composition_Options}_Exploration.md`（均 DESIGN RECOMMENDATION）

**本轮边界（硬约束）**：
- 不修改 Frozen Authority / Product Blueprint / XHS·RD Instance / Runtime / Connector / 代码 / UI。
- 不做高保真、不进 Figma、不开发、不新建业务 Primitive。
- 本文件是 **PRODUCT MODEL RECOMMENDATION**，待 Review 批准后，方可进入高保真 / 前端 / Instance Spec。

**Review 结论**：5 份 Exploration 整体方向 **APPROVED WITH 2 PRODUCT DELTAS**（UX-1：Content Growth ≠ 超级 Workspace；UX-2：Office 用户面主词 经营单元 → 经营方向）。OPTION D 方向通过，**暂不进入高保真**。本文件为 Product Model Closure。

---

## 1. Content Growth 在 IA 中的准确角色

- **层级**：Content Growth 是 **Business-level operating domain**，作为「业务空间」下的一个业务实例（与 XHS 小红书运营办公室、RD 研发办公室并列），**不是 Blueprint 的第七个一级区**。
- **不是什么**：不是把 Content Production / 各平台 Channel Operations / Engagement / Analytics 全装进去的「超级 Professional Workspace」。它自身**不承载专业深度工作**。
- **是什么**：经营层面的**聚合与轻操作**面。专业深度工作由各自的 Professional Workspace 承担，按需挂载（见 §2）。
- **承接的 Frozen 范围**：完整消费 Content Growth Domain Authority（①②③④⑤）+ Shared Authority（⑥⑧⑦ + Context Isolation），仅做用户面翻译与渐进披露，**未修改、未新增任何 Primitive**。

> 判据：若用户在界面上需要在「内容增长」和「制作 Workspace」「渠道 Workspace」之间反复横跳、且明显感知是两个独立大房间，IA 即失败（等于把 Content Growth 重新定义成了超级 Workspace）。

---

## 2. Business Home 与 Professional Workspace 的关系

| 维度 | Content Growth Business Home | Professional Workspace |
|---|---|---|
| 职责 | Attention / Light Ops / 经营方向切换 / 跨账号·跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback | 真正的深度工作：Content Production / XHS Channel Operations / Douyin Channel Operations / Future TikTok·Bilibili·YouTube Operations |
| 用户停留 | 常驻（每天进来都在这） | 按需进入（做某步时才展开） |
| 进入方式 | 默认落地 | Shell **Adaptive Surface / Deep Link**（点内容流里的某步 → 展开专业面） |
| IA 表现 | 业务空间 → 内容增长 → Home / [经营方向] | 不单列一级导航；作为内容流某步的深入工作面 |
| 用户体验 | 「我在内容增长里看该做的事、做内容」 | 「我只是把这条内容的某一步在专业面里做细了」，不觉得换了 Workspace |

**进入原则**：专业深度只在需要时点开，且点开仍处在**同一条内容流的语境**里。用户不感知「跳办公室」。

---

## 3. Office 内部词 / 用户词映射

| 层 | 词 |
|---|---|
| INTERNAL TERM（Frozen ①，不变） | `Office` |
| **USER-FACING PRIMARY TERM**（首版主 UI） | **经营方向** |
| USER-FACING ALIAS（品牌一致场景） | 内容品牌 |
| HELP / ADVANCED / MANAGEMENT CANDIDATE（不进首版主 UI） | 经营单元 |

- 内部 `Office` 语义（目标/定位/受众/策略/资料/账号池）完整保留于 Frozen Authority，用户面只做翻译，不改底层。
- 首版主 UI 一律用「经营方向」；「经营单元」仅出现在帮助文档 / 高级解释 / 管理语境。
- 单账号用户**连「经营方向」也隐去**，Curis 内部称为「你的内容经营」。
- 完整逐概念映射见 `Curis_Content_Growth_User_Terminology_Map.md`（含完全隐藏词清单：OfficeAccountBinding / Target Account Set / HIGH_REUSE / FULL_DIVERGENCE / 路由 / 队列指标等一律不出用户词典）。

---

## 4. OPTION D 最终产品骨架（推荐模型）

```
业务空间 → 内容增长（Business-level operating domain · 非一级区、非超级 Workspace）
├─ Content Growth Business Home（Attention + Light Operations）
│   今天值得做 / 正在生产 / 待发布 / 账号动态 / AI在做什么 / 需我决定
│   经营方向切换 / 跨账号·跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback
├─ [经营方向]（多账号时出现；单账号隐去该层）
│   └─ 连续内容流：制作 → 发到所选账号 → 发布 → 回流（一条线）
├─ 账号（Connected Accounts：平台 / 账号 / 状态 / 定位 / 所属经营方向）
└─ Professional Workspace（按需经 Shell Adaptive Surface / Deep Link 进入）
    ├─ Content Production
    └─ XHS / Douyin / Future TikTok·Bilibili·YouTube Channel Operations
```

**用户实际看到的路径（而非内部名词）**：

> 内容增长 → 今天值得做什么 → 某个经营方向 → 某条内容 → AI 制作 → 针对账号分别完成 → 发布 → 数据回流

**首版保留的 KEEP 项**（均不破坏）：
- 单账号隐藏 Office 层；多账号才出现经营方向；AI 建议账号分组、用户确认/调整。
- Home = Attention + Light Operations；Connected Accounts 独立管理入口。
- 发到哪里：默认 + AI 推荐 + 手动调整。
- Production + Distribution 在用户侧连续（一条内容流）。
- Employee 以责任状态浮现（谁在负责 / 正在做 / 卡在哪 / 需我决定）。
- Context 默认隐藏、按需追溯；Needs CEO 仅重大事项。
- XHS 当前实现不修改；Queue/Bottleneck 仍是 VISION / RESERVED（⑨ 未 Frozen）。

---

## 5. 首版明确不展示什么

- ❌ 不展示 `Office` / `OfficeAccountBinding` / `Account Pool` / `Target Account Set` / `Content Opportunity` / `Content Intent` / `Content Variant` / `reuse_mode` / `HIGH_REUSE` / `FULL_DIVERGENCE` 等内部原词。
- ❌ 不展示 Organization Routing / Responsibility Requirement / Shared Employee Service Relation 配置面。
- ❌ 不展示 Context Isolation 机制词（仅给「用了哪些资料」可追溯入口）。
- ❌ 不展示 Queue / Bottleneck 的**指标**（queue_depth / capacity / bottleneck score / 枚举名）——⑨ 未 Frozen，仅未来以 Frozen P7 白话呈现（VISION/RESERVED）。
- ❌ 不展示 Distribution Execution Policy 原词（只给「其他账号可继续发 / 等全部准备好」自然语言选项）。
- ❌ 不把 Content Growth 做成「制作 Workspace / 渠道 Workspace / 互动 Workspace / 数据 Workspace」四宫格导航（即不做 OPTION A 的切页暴露）。
- ❌ 不新建一级导航区、不新建业务 Primitive、不修改任何 Frozen 文档。
- ❌ 首版**不为 N:N 共享账号做复杂 UX**（遵循 1 Account : 1 Primary Office）；Operating Context 仍为 RESERVED/DEFERRED，不进首版。

---

## 6. 下一阶段应设计的关键界面（待 Closure Review 批准后）

按优先级（仅设计清单，本轮不实现）：

1. **Content Growth Business Home**（最高优先）：Attention + Light Operations 混合首屏——「今天值得做 / 正在生产 / 待发布 / 账号动态 / AI 在做什么 / 需我决定」的卡片与 Decision Banner（遵循 Frozen P7）。
2. **首次进入与账号连接流（First-Run）**：CASE A（单账号零配置）/ B（建议分开）/ C（建议一起经营）/ D（AI 读信息给建议分组），OAuth 失效不丢账号/历史。
3. **经营方向容器与切换器**：多账号时出现，单账号隐去；「添加账号 / 换经营方向 / 在经营方向间移动账号」轻操作。
4. **一条连续内容流（核心交互）**：AI 发现选题 → 接受 → 发到哪里（默认+AI推荐+手动）→ 针对账号分别制作（行为化复用/分制）→ 各账号发布状态 → 数据回流。
5. **Connected Accounts 管理面**：平台/账号/状态/定位/所属经营方向；新增/重连/移除/换定位。
6. **AI 员工责任状态浮现**：内容流/责任上的 Presence（谁在负责 / 正在做 / 卡在哪），及「主动增加 + Curis 建议增加」两条轻入口（指标全隐藏）。
7. **Professional Workspace（按需）**：Content Production / 各平台 Channel Operations 经 Shell Adaptive Surface / Deep Link 进入的深入工作面草图（不单列一级导航）。
8. **Context 可追溯入口**：内容/账号详情里的「资料来源」轻量入口（默认隐藏）。
9. **Needs CEO 决策呈现**：严格沿用 Frozen P7 的 8 要素 + 三层信息层级 + Provenance（领域内容填空，不重造机制）。
10. **XHS 当前实例的未来纳入 IA 草图**：「内容增长 → 小红书经营方向」复用现有 XHS 能力（不修改 XHS）。

---

*Curis Content Growth — Product Model Closure · PRODUCT MODEL RECOMMENDATION / REVIEW（非 Frozen）*
