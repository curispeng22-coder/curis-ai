# XHS Workspace — Calendar Pattern / Interaction Spec

> 关联：`Curis_XHS_Workspace_Design_Brief.md`、`Curis_XHS_Workspace_Design_Exploration_v1.md`（方案 A · Calendar-Dominant）、`Curis_XHS_Workspace_State_Semantics_Audit.md`（三层责任语义）。
>
> **状态**：REPOSITIONED / SUPERSEDED AS WORKSPACE DEFAULT（2026-08-21）· 继续作为内容运营内的 Calendar Object View 专项

---

## 1. 范围与原则

本 Spec 只解决 **内容运营内 Publishing Calendar「同一天多篇 Note」** 问题。不修改 Pane Shell、Search、Responsibility Semantics、Note Split、Utility。Calendar 不是 AI 科技 Workspace Default，也不是独立 Professional Surface；经营概览是当前 default candidate，具体菜单细节尚未冻结。

坚持的设计常量（来自 Blueprint / Frozen Design System）：

- **Content Object × Time**：Note 是业务对象，Calendar 是时间轴；日历格内放 Note，不放传统 Scheduler 事件条。
- **Employee Presence 持续可感知**：每篇 Note 轻量表达责任归属（作者 / Current Executor）。
- **Calendar → Note Split**：点击日历中的 Note → 进入现有 Note Selected / Split Working（状态 B），不另造详情页。
- **Low Surface Complexity, High Functional Density**：同一天多篇时，用「1 张 Primary + 紧凑 Row + +N」控制密度，不让日期格无限增高。

**不做什么**：不增加 Dashboard wall；不增加任务列表；不重新设计整个 XHS Workspace；不把 Note 退化成 Google-Calendar 式纯事件条；不把 Calendar 提升为 Workspace Default。

---

## 2. Month / Week / Day Focus 分工

| 视图 | 职责 | 单日 Note 展示 |
|------|------|----------------|
| **Month** | 看整月发布节奏、内容密度、状态、责任归属 | 单日**有限数量**（见 §3 规则），超出经 `+N` 收口 |
| **Week** | 空间更大，展示更多 Note、具体发布时间、更完整状态 | 比 Month 容纳更多 Row；仍不无限堆叠（Week 上限留待下一轮低保真） |
| **Day Focus / Day Detail** | 处理单日内容很多的情况，展示当天**完整 Note 列表** | 列出当天全部 Note；本轮只定义入口与基本职责（§7），不扩展成复杂页面 |

`周` 切换按钮在 v4 中为占位（Month 已实现，Week 详细布局 RESERVED）。

---

## 3. Month View 单日展示规则

| 当天 Note 数 | 展示规则 |
|--------------|----------|
| **0 篇** | 空日期格（仅日期数字） |
| **1 篇** | 保持当前**完整 Primary Note Card**（封面 + 标题 + Employee Presence + Status） |
| **2–3 篇** | 1 张 Primary Note Card + 其余用 **Compact Note Row** |
| **4 篇及以上** | 最多：`1 张 Primary Note Card` + `2 条 Compact Note Row` + `「+N 篇」入口`；**禁止继续纵向堆叠导致日期格无限增高** |

**Primary Note Card 在密集单元格内使用紧凑封面**（固定高度缩略，非 3/4 海报），以适配密度；单篇日（1 篇）的 Primary 仍用完整封面。两种都保留「封面 + 标题 + Presence + Status」四要素，不退化成事件条。

---

## 4. Compact Note Row 规范

低视觉重量，**不做成另一张完整卡片**。必备字段：

- **发布时间**（有排期时显示，如 `09:30`）
- **Note 标题**
- **轻量 Employee Presence**（作者首字头像，如 `[陈]`）
- **Status**（状态色点 + 文案，如 `● 已排期`）

示例：

```
09:30 [陈] 夏日通勤穿搭     ● 已排期
14:00 [王] 平价通勤包推荐   ● 制作中
```

视觉：一行紧凑行，hover 微高亮；字号 `fs-1`，无卡片边框/封面。

---

## 5. Primary Note 选择规则（推荐 · 最终修正）

**不要默认「第一篇就是 Primary」。** 采用简单、可解释的优先级，取第一个满足者。**Attention 状态必须高于「用户之前选中过」**——需要 CEO / 阻塞的 Note 即便不是用户当前选中的，也应自动成为 Primary。

| 优先级 | 条件 | 含义 |
|--------|------|------|
| **P0** | **Needs CEO / Blocking / Failed** | 需要 CEO 注意力或阻塞 / 失败，自动置顶（Attention > 一切） |
| **P1** | **用户当前选中的 Note** | 用户此刻正在查看 / 点开的 Note |
| **P2** | **Current Executor Working（制作中）** | 当天有员工正在制作的 Note |
| **P3** | **即将发布 / 排期最近** | 排期时间最早的待发布 Note |
| **P4** | **时间排序** | 兜底：按时间倒序 |

> - **P0 高于 P1**：Attention 状态（Needs CEO / Blocking / Failed）优先级最高，不可以被「用户之前选中过」覆盖——CEO 待决策的 Note 必须被看见。
> - 同优先级并列时，按排期 / 发布时间升序取首篇。
> - 不引入复杂算法；上述顺序即「注意力应落在哪篇」的可解释判据。

---

## 6. 交互

- **点击 Primary Note** → 进入现有 Note Selected / Split Working（状态 B）。
- **点击 Compact Note Row** → 进入对应 Note（同一状态 B，加载该 Note）。
- **点击「+N 篇」** → 打开 **Day Focus / Day Detail**，列出当天完整 Note 列表。
- **不在 Month Cell 内无限展开**；所有溢出经 `+N` 收口到 Day Focus。

---

## 7. Day Focus 入口与基本职责（冻结入口 · 不冻结呈现）

**冻结（Product / Pattern Contract）**：
- **入口**：Month Cell 内的 `「+N 篇」` → 打开 **Day Focus / Day Detail**，列出当天完整 Note 列表（按 §5 规则排序，Primary 置顶），每条可点击进入对应 Note。
- **关闭**：点击遮罩 / `Esc` / 关闭按钮。
- **基本职责**：处理单日内容很多的溢出情况，展示当天全部 Note。

**不冻结（Presentation 开放）**：
Day Focus 的具体呈现方式本轮**不冻结**，未来可以是以下任一形态：
- **A. Main 内 Day Focus** — 在 Main Pane 内展开当天列表（替换当前 Note 视图）。
- **B. Calendar Morph** — 日历格就地展开 / 变形为当日详情。
- **C. Overlay** — 覆盖层 / 浮层展示。

> ⚠️ **当前 v4 HTML 使用 Overlay 仅作 PRESENTATION EXAMPLE**，**标记 `PRESENTATION EXAMPLE ONLY / PENDING`**，**不得作为 Product / Pattern Contract**。具体呈现待后续轮次低保真选型后冻结。
> 本轮**不扩展**为带筛选、编辑、统计的复杂页面（RESERVED）。

---

## 8. 与 Responsibility Semantics 的衔接

日历格内展示的 Presence 是 **Current Responsibility / Current Executor** 的轻量表达，不是 Object Owner：

- Compact Row 的 `[陈]` / Primary 卡片头像 = 该 Note 当前责任员工（Current Executor 或 Current Responsibility）。
- 已完成发布、系统进入自动 Analytics 的 Note，其 Employee Presence 不伪装成员工（见 State Semantics Audit §E）；日历中以状态文案（如「已发布」「自动分析」）表达，不占用员工头像位。
- Object Owner（业务/Workspace 稳定归属）不进入日历格的每日 Presence。

---

## 9. 高保真验证点（v4）

`Curis_XHS_Workspace_Visual_v4.html` 状态 A 的 **day 12（周五）5 Note** 演示，专用于验证 **P0 > P2（Attention > Working）** 的 Primary 优先级：

- Primary（紧凑封面，P0 自动置顶）：`[王] 通勤穿搭合规审核 ● 待 CEO 决策`（Needs CEO / Blocking，命中 §5 P0）
- Compact Row 1（P2）：`09:00 [陈] 通勤穿搭灵感库 ● 制作中`
- Compact Row 2：`14:00 [陈] 早八妆容教程 ● 已排期`
- `「+2 篇」` → Day Focus 列出当天全部 5 篇（Primary 置顶 + 隐藏的 `平价通勤包测评 ● 已排期` + `油皮定妆实测 ● 待审核`）

> 验证要点：当天同时存在 Working Note（陈真 制作中）与已排期 Note，但 **Needs CEO Note 自动成为 Primary**（P0 > P2 > P3）；不再用 Working Note 单一验证优先级。日期格高度受控、+N 分流可用、Day Focus 仅作 PRESENTATION EXAMPLE（见 §7）。

---

## 10. RESERVED / 范围外

- Week View 详细布局与上限。
- Day Focus 内的筛选 / 排序控件 / 批量操作。
- 自然语言日期跳转、跨月拖拽改期、日历内联编辑。
- 搜索与日历的联合过滤（Search Surface 已独立，见 Pane Shell Spec §9.8）。

---

**状态**：REPOSITIONED / SUPERSEDED AS WORKSPACE DEFAULT —— Calendar 语义继续作为 AI 科技 Workspace「内容运营」内的 Object View Candidate；本文件不授权前端实现、XHS 迁移或最终菜单冻结。
