# Curis Content Growth — User Terminology Map

**Status**: Exploration（设计探索 · 非 Frozen · 非高保真 · 非代码）
**阶段**: PRODUCT / WORKSPACE DESIGN — UX & IA Exploration（第 4 份 / 共 5 份）
**上位依据**: 同 UX Model 文档顶部；Frozen Domain ①②③④⑤；Frozen Shared ⑥⑧⑦；UX 模型第 1 节。

**边界**：不修改 Frozen Authority；本文为 DESIGN RECOMMENDATION。术语映射**不改变底层语义**，只决定「用户看到什么词」。

> **Review 更新（2026-08-16 · APPROVED WITH 2 PRODUCT DELTAS）**：整体术语方向通过。本轮落实 **DELTA UX-2**：Office 用户面主词由「经营单元」改为「经营方向」；「经营单元」降级为帮助文档/高级解释/管理语境候选，不进首版主 UI；「内容品牌」保留为品牌一致场景别名。不修改 Frozen Authority。

---

## 0. 映射原则

1. **不强迫用户看内部术语**：Frozen 里的正式词（Office / Channel Account / Target Account Set…）是系统语义，用户面用自然语言替代。
2. **一词一义、避免与 Blueprint 现有词冲突**：Blueprint 已有「业务 / 业务空间 / 员工 / 资料库 / 会议」等，「经营单元」等命名需避开歧义。
3. **复杂度按需披露**：单账号时连替代词都可隐藏；多账号时才引出「经营单元」概念。
4. **完全隐藏的概念**：底层机制词（Routing / Requirement / Context Isolation / Queue / Bottleneck 指标 / reuse_mode）不进入用户词典。

---

## 1. Office 候选名评估（本轮重点）

**内部语义（Frozen ①）**：Office = 「经营什么」的载体 = 一套共同的 business_goals / positioning / audience / content_strategy / knowledge_refs / growth_context / account_pool。直接挂 Company，≠ Platform / Account / Content Type / Department / Team。

**用户心智目标**：「这几个账号属于同一个经营方向。」

### 候选评估

| 候选 | 直觉匹配 | 风险 | 结论 |
|---|---|---|---|
| **内容办公室** | 中 | 「办公室」像物理/公司房间，单人创作者觉沉重 | ✗ 不推荐 |
| **经营方向** | 高 | 最贴合用户心智「这几个账号在做同一个方向」，自然、零企业感 | ✅ **主推荐（用户面主词）** |
| **经营单元** | 高（最忠实内部语义） | 略抽象/企业感；可作帮助文档/高级解释/管理语境候选，但不进首版主 UI | ◐ 降级为帮助/管理语境候选 |
| **内容品牌** | 高（品牌一致场景） | 若 Office 是「话题垂直」而非品牌则不准 | ◐ 别名（品牌一致场景） |
| **账号组** | 低 | 只表达「账号集合」，丢失目标/策略/受众 | ✗ 不推荐（过于机械） |
| **业务线** | 中 | 与 Blueprint「业务 / 业务空间」重叠混淆 | ✗ 不推荐（歧义） |
| **内容项目** | 低 | 「项目」暗示临时，Office 是持续经营 | ✗ 不推荐 |
| **品牌空间** | 中 | 同「内容品牌」，偏品牌、偏空间隐喻 | ◐ 次选 |

### 推荐结论（DELTA UX-2 更新）

> **INTERNAL TERM**：`Office`（Frozen ①，内部语义不变）
> **USER-FACING PRIMARY TERM**：**「经营方向」**（首版主 UI 主词）
> **USER-FACING ALIAS（品牌一致场景）**：「内容品牌」
> **HELP / ADVANCED / MANAGEMENT CANDIDATE**：「经营单元」（帮助文档 / 高级解释 / 管理语境使用，不进首版主 UI）
> **单账号隐去**：单账号用户不出现该词，Curis 内部称为「你的内容经营」。

**理由**：
- 「经营方向」最贴合用户心智（「这几个账号在做同一个方向」），零企业感，首版主 UI 最自然；
- 内部 `Office` 语义（目标/定位/受众/策略/资料/账号池）完整保留于 Frozen Authority，用户面只做翻译，不改底层；
- 「经营单元」仍最忠实内部语义，留作帮助文档/高级解释/管理语境候选，避免首版给用户强加内部术语；
- 「内容品牌」作为品牌一致场景的别名（如四个平台同品牌）；
- 实际文案例句：「这几个账号看起来在做同一个方向 / 要把它们放在同一个经营方向吗？ / AI工具 · 个人IP · 数码测评 · 生活方式」。

---

## 2. 逐概念映射表

| INTERNAL TERM | USER-FACING TERM | 备注 |
|---|---|---|
| Office | **经营方向**（USER-FACING PRIMARY；单账号隐去；品牌场景别名「内容品牌」；「经营单元」仅帮助/管理语境） | 见 §1 |
| Channel | **平台**（小红书 / 抖音 / B站 / TikTok） | 用户本来就叫平台 |
| Channel Account | **账号** | 用户本来就叫账号 |
| OfficeAccountBinding | （**完全隐藏**） | 技术绑定关系不暴露；用户只做「账号属于哪个经营单元」 |
| Account Pool | （**完全隐藏 / 弱化为「这个经营方向下的账号」**） | 派生集合，不单独成概念 |
| Content Opportunity | **「发现一个值得做的选题」** | 用户只见「这个选题值得做」 |
| Content Intent | **「要讲的内容 / 这条内容的想法」** | 用户不创建 Intent 对象，只接受/调整 |
| Target Account Set | **「这条内容发到哪里」** | 三源合并（默认/AI推荐/手动）在背后裁决 |
| Effective Target Set | （同「发到哪里」，无需区分） | 用户只见最终选择 |
| Content Variant | （**完全隐藏**） | 用户只见「每个账号分别做好了」 |
| `reuse_mode` HIGH_REUSE | 「能复用的自动复用」 | 不出现词，体现为行为 |
| `reuse_mode` FULL_DIVERGENCE | 「针对不同账号分别制作」 | 不出现词，体现为行为 |
| Publication | **「已发布 / 待发布 / 发布失败」**（每账号独立） | per-Account 真相，用户按账号看状态 |
| Distribution Execution Policy · BEST_EFFORT | **「其他账号可以继续发」** | 自然语言选项 |
| Distribution Execution Policy · ALL_REQUIRED | **「需要所有账号都准备好再一起发」** | 自然语言选项 |
| Responsibility Requirement（⑥） | （**完全隐藏**） | 用户只说「帮我做内容」 |
| Organization Routing（⑦） | （**完全隐藏**） | 用户不配置路由 |
| Shared Employee Service Relation（⑧） | （**完全隐藏**） | 用户只见「谁在负责」 |
| Context Isolation Truth Boundary | （**默认隐藏，按需可追溯**） | 「用了哪些资料」入口 |
| Lightweight Queue / Bottleneck（⑨） | （**不暴露为指标**） | 仅未来以 Frozen P7 白话建议呈现（VISION/RESERVED） |
| Employee | **「AI 员工 / 员工」**（带角色名，如「内容策划·王芳」） | 用户见角色与责任状态，不见路由 |

---

## 3. 完全隐藏的概念清单（用户词典中不存在）

以下词**绝不**出现在任何用户可见文案（含按钮 / 标签 / 提示）：

- `OfficeAccountBinding` · `Account Pool` · `Target Account Set` · `Effective Target Account Set`
- `Content Opportunity` · `Content Intent`（对象名；只呈现「选题 / 要讲的内容」）
- `Content Variant` · `reuse_mode` · `HIGH_REUSE` · `FULL_DIVERGENCE`
- `Responsibility Requirement` · `Organization Routing` · `Shared Employee Service Relation`
- `Context Isolation`（机制词；只给「资料来源」可追溯入口）
- `Distribution Execution Policy`（只给自然语言选项）
- `BEST_EFFORT` · `ALL_REQUIRED` · `VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE`（Capability Truth 内部枚举）
- Queue / Bottleneck 的 **指标名**（queue_depth / capacity / bottleneck score / 枚举值）

---

## 4. 命名一致性要求（跨文档）

- 所有 Content Growth 用户面文档 / 未来 Instance Spec / 前端文案**必须**使用本映射的用户面词，不得混用内部原词。
- 内部原词仅允许出现在：Frozen Authority / Contract Candidate / 后端 Schema / API（作为语义真源），与用户面严格分层。
- 当内部语义演化为 Extension（如 Routing 算法 / 具体平台 API）时，用户面词**不变**，扩展只发生在底层。

---

*Curis Content Growth — User Terminology Map · DESIGN RECOMMENDATION（非 Frozen）*
