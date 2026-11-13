# Curis XHS Workspace Design Brief

**Status**: Review — **XHS READY FOR DESIGN**  
**Document type**: Design-AI input derived from Reference Research  
**Research date**: 2026-08-15  
**上位依据**:
1. `docs/01_Product/Curis_Product_Blueprint.html`（v5.1 · Single Current）
2. `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` + `_system/tokens.css`（Frozen）
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（A 阶段 Shell Contract + Shared Patterns）
4. `docs/03_Design/Curis_XHS_Workspace_Reference_Research.md`（本轮研究，8 问已答）

> 本 Brief **不是 Blueprint**，不授权 UI 实现。它定义未来设计探索必须从参考研究中保留什么。当前阶段不画页面、不改代码、不修改 Shell Contract。

---

## FINAL SCOPE SUMMARY

### DESIGN NOW

- Workspace foundation（Shell Contract 直接引用）;
- Content Calendar（周 / 月视图，拖拽规划，发布节奏）;
- Content Object / Note（单篇笔记：封面 3:4 / 标题 / 正文 / 标签 / 状态 / 数据快照）;
- 最小 Context Surface（选题库 / 信号监测，默认收起）;
- 按需 Utility Surface（图文预览 / 数据看板 / 素材 / 审核详情）;
- Result Reference 轻量引用（`📊 数据看板 ▸` / `✅ 笔记已发布 ▸`）;
- Needs CEO / Decision（品牌 / 敏感表达确认，橙色 Decision Banner）;
- Review Gate（违禁词 / 人设一致性 / 品牌确认，可升级 Needs CEO）;
- Handoff Event（策划 → 审核责任交接，轻量）;
- Employee Workstation（仅创作执行 / 审核阻塞 / Handoff 时浮现，非常驻）;
- Publishing Queue（定时列表 + 冷启动观察状态；5/30/60 为可配置观察阶段示例）;
- Analytics（默认 Template，可配置指标/阈值；CES 为示例，非不可变体系）;
- Content Reuse Loop（复盘结论反哺选题库）.

> **双主轴语义冻结 / 几何不冻结（本轮修正 1）**：DESIGN NOW 的 Content Calendar + Content Object 是"时间轴 × 内容对象"双主轴语义的冻结项；其**具体几何布局（左日历+右笔记等）不冻结**，由 Design Exploration Round 1 探索。
> **数字降级（本轮修正 2 / 3）**：7:2:1 / 5/30/60 / 收藏率>5% / CES 均为 Strategy Template / Expert Knowledge 示例；UI 以可配置策略、观察阶段、指标阈值、Analytics Template 承载，不写死。

### RESERVED

- 多账号矩阵管理深度视图（蒲公英式，先单账号）;
- 商业合作 / 蒲公英任务流;
- 财务管理 / 结算;
- AI 文案自动生成引擎（先人工 + AI 辅助润色）;
- 社媒监听 / 竞品实时追踪;
- 团队审批流（多角色会签）;
- 外部 API 集成面板.

### LATER

- 短视频 / 抖音跨平台内容复用;
- 自动化发布（Auto Publish）与智能时段建议;
- 爆文预测模型;
- 多 Workspace 内容资产打通;
- 语音 / 口播脚本生产;
- 高级 CES 归因与达人深度画像;
- 多 Utility 同时展开.

### DO NOT COPY

- 以 Conversation 为默认 Main 核心（研发换皮）;
- 文件树 / Diff 布局平移为素材树 / 数据 Diff;
- 常驻员工列表侧栏 / 员工顶部 tab;
- 把 7 个 XHS 自有 Pattern 同时铺满主区;
- 对话内嵌入完整数据表 / 长图文（应走 Result Reference → Utility）;
- 永久工具墙 / 每个能力同时展开;
- 完整小红书 App / 千瓜 / Later 视觉克隆;
- 把 Shell Contract 当四栏固定（Context/Utility 是 Adaptive，默认收起）.

---

## 1. Page goal

帮助 CEO 督导由 AI 员工执行的小红书内容运营，同时让每一条内容（笔记）的责任、制作、审核、发布、数据与复盘都可追溯、可复用。

页面必须立刻说清三件事：
1. 当前运营节奏里**哪一天 / 哪一篇内容**是重点；
2. 当前笔记处于哪个责任节点（制作 / 审核 / 发布 / 复盘）；
3. CEO 是否需要决策、检查，还是让内容自然流转。

页面是专业的内容运营 Workspace，以**内容对象 × 时间**为主轴，不是聊天首页、通用任务板或社媒仪表盘克隆。

## 2. Information hierarchy

1. Workspace 身份与当前运营目标（如"本月涨粉 3000"）；
2. Content Calendar（规划与节奏）；
3. 选中笔记的 Content Object 详情（制作状态）；
4. 审核闸状态与 CEO 注意力；
5. 最小 Context Surface：选题库 / 信号、账号基准、相关素材；
6. 按需 Utility Surface：图文预览、数据看板、素材、审核详情；
7. 持久结果：发布记录、数据快照、复盘学习。

技术 / 业务对象在有用时可见，但永不挤占"内容对象 + 时间节奏 + 下一责任节点"。

## 3. Spatial structure

使用三个独立可理解的面（符合 Shell Contract §1–2）：

- **Main Workspace（双主轴语义，几何未冻结）**：语义上必须同时承载"时间轴（发布节奏）"与"内容对象（笔记）"两轴；**具体几何布局（左日历+右笔记 / Calendar 主视图 / Object-First 等）不冻结**，由 Design Exploration Round 1 探索。默认第一眼简单。
- **Context Surface（左 · Adaptive）**：选题库 / 信号监测、账号基准、相关素材。可收起，不预设全产品统一内容。
- **Utility Surface（右 · Adaptive）**：图文预览 / 数据看板 / 素材 / 审核详情。专注模式用更深背景。可单开、双开、全关。

不要将 Utility Surface 做成永久右栏；不要将 Employee Workstation 做成导航侧栏或顶部 tab。

## 4. Content Object / Note behavior

每篇笔记（Content Object）显示：

- 封面（3:4 还原缩略）;
- 标题 + 正文摘要;
- 标签（大词 / 长尾）;
- 状态（草稿 / 制作中 / 待审核 / 已发布 / 复盘）;
- 责任员工（仅在有归属时显示）;
- 数据快照（发布后：CES 维度）;
- 折叠 / 展开控制。

状态行为：

| State | Default behavior |
|---|---|
| 制作中 | 展开显示当前制作进度；员工卡可浮现"内容生产中" |
| 待审核 | 进入 Review Gate，可升级为 Needs CEO |
| 已发布 | 折叠显示数据快照摘要，点开 Utility 看完整数据 |
| 复盘 | 展开显示 CES 维度与复用建议 |
| 失败 | 展开显示失败阶段 / 责任人 / 重试边界 |

展开笔记显示其制作详情，不应新建线程，除非用户显式开启新内容。

## 5. Content Calendar

日历负责"规划与节奏"：

- 周 / 月视图切换；
- 每格显示当日计划发布笔记卡片（状态色点）；
- 拖拽改期；
- 选中某日 / 某笔记 → 右轴显示 Content Object；
- 冷启动赛马状态可在卡片角标显示（5/30/60 观察）。

日历不是装饰，须绑定真实笔记对象；空日不显示假卡片。

## 6. Context Surface（选题库 / 信号）

侧栏应回答"创作 / 选题时哪些上下文必须持续可见"：

- 选题库（7:2:1 配比的已验证 / 延伸 / 测试方向）;
- 信号监测（搜索下拉词 / 评论区提问 / 热门话题 / 竞品爆款）;
- 账号基准（定位 / 人设 / 视觉规范 / 违禁词表）;
- 相关素材目录。

不得变成第二个员工目录、权限中心或常驻工具墙。

## 7. Utility Surface（图文预览 / 数据 / 素材 / 审核）

未来 Utility Surface 可支持：

- 图文预览（Note Preview）：3:4 封面 + 标题 + 正文 + 标签完整还原；
- 数据看板（Analytics）：单篇 CES 维度、账号趋势、粉丝画像；
- 素材 / 资料（Asset）：图片库、参考笔记、品牌视觉规范；
- 审核详情（Review Detail）：违禁词报告、人设一致性、Handoff 上下文包。

每个 Utility 须显示其归属笔记与返回锚点。打开 Utility 不得清除日历 / 笔记选择或静默改变责任。多账号矩阵、商业合作、财务为 Reserved/Later。

## 8. Review Gate 与 Handoff

审核是独立、不可省略的节点：

- 触发：笔记进入"待审核"；
- 检查：违禁词 / 人设一致性 / 品牌表达；
- 通过 → Handoff 到发布员工；
- 阻塞（品牌 / 敏感）→ 升级 Needs CEO（橙色 Decision Banner）。

Handoff 是可见业务事件：发送员工 → 接收员工 → 责任转移 → 上下文包 → 验收态 → 待决问题 → 期望结果 → 返回 / 升级路径。

## 9. Employee Workstation 出现时机

Employee Workstation 仅在节点浮现（⚪ 可选采用，非 Required）：

- 创作执行中（"内容生产中"责任状态）;
- 审核阻塞（needs_ceo）;
- Handoff 交接时;
- 失败 / 恢复。

日常浏览日历、看数据、看预览时**不**强制展开员工卡。绝不把员工列表常驻为侧栏或顶部 tab。needs_ceo 员工**不固定「默认折叠」**，保留当前展开/折叠状态（与 Shared Pattern §3.1 一致）；Workspace 级注意力由顶部 Decision Banner 承载，不由员工卡强制。

## 10. Needs CEO

Needs CEO 是一等公民状态，非 toast。须显示：

- 需决策 / 输入的内容（如敏感表达确认）;
- 员工为何不能安全继续;
- 受影响责任与外部影响;
- 支撑证据;
- 批准 / 驳回 / 暂缓 / 替代选项;
- 决策后恢复的动作。

决策后同一笔记与责任继续，仅在责任真实变更时新建。

## 11. Analytics / Content Reuse Loop

- 数据复盘采用可配置的 Analytics Template；**默认模板可含 CES 类维度**（点击率 → 完读率 → 收藏率 → 评论 → 转粉）作为示例，但指标与阈值**均可配置**，CES 非不可变体系（本轮修正 3）；
- 单篇与账号双视角；
- 7:2:1 选题配比、5/30/60 观察、收藏率 >5% 等均为 Strategy Template / Expert Knowledge 示例，UI 只提供可配置策略、观察阶段与阈值（本轮修正 2）；
- 复盘结论（爆款结构拆解）反哺 Topic & Signal Library，形成数据驱动的复用环；
- 复用环是 XHS 自有 Pattern，研发无对应物，Design 须显式支持"笔记 → 选题库"的数据回流。

## 12. Publishing Queue

- 定时列表：计划发布时间、目标账号、状态（待发 / 赛马中 / 已发）;
- 冷启动赛马：5/30/60 分钟观察状态在卡片角标；
- 多账号发布管理（先单账号，矩阵为 Reserved）;
- 队列项须绑定真实笔记对象，禁止无对象的"发布按钮"。

## 13. Reference product mapping

| Design concern | Primary reference | Secondary reference | Boundary |
|---|---|---|---|
| 内容日历 / 规划 | Later Visual Calendar | 小红书定时发布 | 采用日历 + 拖拽，不抄品牌视觉 |
| 内容对象 / 笔记 | 小红书创作服务平台 | Later Draft Posts | Note 为业务对象，非聊天 |
| 图文预览 | 小红书 App 笔记详情 | Later Preview | 3:4 还原，不抄平台 UI |
| 数据分析 / Analytics | 千瓜 / 灰豚 / 新红 | Later Analytics | 采用可配置 Analytics Template（CES 为示例），不抄仪表盘 |
| 选题 / 信号 | 新红选题灵感 | 千瓜爆款拆解 | Topic Library 为 Curis 自有 |
| 审核闸 | 小红书违禁词 | 蒲公英规范 | 复用 Handoff + Needs CEO |
| 多账号 / 队列 | Later Multi-Profile | 蒲公英矩阵 | Publishing Queue 为 XHS 自有 |
| 员工 / 责任 | Curis Shared Pattern | — | 组织层专属 |

## 14. Prohibited design errors

- 以 Conversation 为默认主轴的"聊天式"小红书（研发换皮）;
- 文件树 / Diff 平移成素材树 / 数据 Diff;
- 常驻员工列表侧栏 / 员工顶部 tab;
- 7 个 XHS 自有 Pattern 同时铺满主区;
- 完整数据表 / 长图文嵌入对话（应走 Result Reference → Utility）;
- 永久 Utility 右栏使所有工具同时可见;
- 无真实笔记对象的"发布按钮";
- 无审核 / 无责任的"已完成"徽标;
- 完整小红书 App / 千瓜 / Later 视觉克隆;
- 为显得专业而添加 Goal / Plan / Skill / Voice 等控件。

## 15. Design gate

设计 / 实现前确认：

1. "内容对象 × 时间"双主轴语义已冻结（非 Conversation），几何布局交由 Design 探索;
2. 当前笔记责任节点与 CEO 注意力可见;
3. 每个 Utility Surface 有入口、返回、持久化契约;
4. Review Gate、Handoff、Needs CEO、失败、恢复均被表达;
5. 数据 / 发布声明绑定真实笔记对象;
6. 设计未把 Curis 变成通用聊天壳或社媒仪表盘克隆;
7. 4 个 Shell Contract Delta Candidate 已记录待 Review，未擅自修改 Contract。

## 16. Shell Contract 适配性单独回答（Delta Candidate，不修改）

> 本 Brief 不修改 Shell Contract。以下内容为对 A 阶段 Contract 的适配性评估，作为 Delta Candidate 提出，待 Review 批准后再决定是否升格为 Contract 正式修订（遵循 Blueprint → Design → Code 顺序）。

### 16.1 现有 Shell Contract 是否适合 XHS？

**基本适合，无需推翻。** Main 必有 + Context/Utility Adaptive + 六区导航 + Shared Pattern 矩阵对 XHS 完全成立。XHS 把 Main 声明为"日历 + 内容对象"、Context 声明为"选题库"、Utility 声明为"预览/数据/审核"，完全落在 Shell Contract §0.1 / §2 的"内容由 Instance 声明"框架内。

### 16.2 可直接复用的 Shared Patterns

✅ 直接复用（不改）：Context Surface、Utility Surface、Result Reference、Needs CEO / Decision、Handoff Event。
⚪ 按需复用（不强制）：Employee Workstation、Composer（仅在节点浮现）。

### 16.3 暴露出的 Shell Contract 不足（**已裁决 · 2026-08-15 XHS Review**）

| # | 裁决 | 理由 / 动作 |
|---|---|---|
| **Delta-X1** | **不采纳** | Main 布局本就由各 Instance 决定（Shell Contract §0.1），无需显式区分单核/双核。 |
| **Delta-X2** | **采纳 · 已回写 Shell Contract §3.1 / §4** | XHS 正式补为第二个 Context/Utility 实例示例（Context=选题库（信号/素材）；Utility=图文预览/数据看板/审核）。 |
| **Delta-X3** | **暂不采纳** | 不创建 "Business Object Surface" 抽象；业务对象由 Instance 在 Main 内表达。 |
| **Delta-X4** | **不升 Shared Pattern** | 创作进度用现有 `Current Work / Progress` 字段表达，不新增子状态。 |

> 仅 X2 落地（已回写 Shell Contract），X1 / X3 / X4 驳回。本 Brief 不修改 Shell Contract 其他内容。

---

**Final status**: `XHS READY FOR DESIGN`.

**UI Designer**: UI Designer  
**文档日期**: 2026-08-15  
**阶段**: XHS 专项 · Reference Research + Design Brief（不画页面、不改代码、不修改 Contract）
