# Curis Content Growth — Workspace Composition Options

**Status**: Exploration（设计探索 · 非 Frozen · 非高保真 · 非代码）
**阶段**: PRODUCT / WORKSPACE DESIGN — UX & IA Exploration（第 5 份 / 共 5 份）
**上位依据**: 同 UX Model 文档顶部；Frozen Domain（Production×Channel Ops 底层已分离，但用户侧是否分离待定）；Frozen Shared ⑧（Shared Employee ≠ Shared Context）；Shell Contract P1–P7；XHS Instance 先例（内容对象 × 时间 / Low Surface Complexity）。

**边界**：不修改 Frozen Authority / Blueprint / XHS·RD；不新建 Primitive；不画高保真。本文为 DESIGN RECOMMENDATION。

> **Review 更新（2026-08-16 · APPROVED WITH 2 PRODUCT DELTAS）**：整体 OPTION D 方向通过。本轮落实 **DELTA UX-1**（Content Growth = Business-level operating domain，≠ 超级 Workspace；Business Home 与 Professional Workspace 经 Shell Adaptive Surface / Deep Link 自然分工）与 **DELTA UX-2**（Office 用户面主词 经营单元 → 经营方向）。OPTION D 收敛为「Content Growth Business Home + 经营方向 + 连续内容流 + 按需 Professional Workspace」。收口见 `Curis_Content_Growth_Product_Model_Closure.md`。不修改 Frozen。

---

## 0. 要回答的核心问题

底层已经分开 **Content Production（平台无关制作）** 与 **Channel Operations（每平台账号运营）**。但用户侧是否需要看到两个**完全独立**的 Workspace？

本章比较四种方案，给出推荐。

> 评估维度（每方案必答）：用户如何理解 / 第一次怎么创建 / 日常怎么使用 / 多账号怎么处理 / Employee 怎么出现 / 优点 / 缺点 / 认知成本 / 扩展成本 / 实现复杂度。

---

## OPTION A — 功能拆分（Production / Channels / Engagement / Analytics）

```
内容增长
├─ 制作（Production）
├─ 渠道（Channels / 账号运营）
├─ 互动（Engagement）
└─ 数据（Analytics）
```

**用户如何理解**：「按功能分房间，做制作去制作页，发账号去渠道页。」
**第一次怎么创建**：连接账号 → 进制作页建内容 → 切渠道页分发。
**日常怎么使用**：在四个 tab 间切换完成一件事。
**多账号怎么处理**：渠道页管理所有账号，制作页产出后手动分配到渠道。
**Employee 怎么出现**：各功能页内以责任状态浮现（制作页见制作员工，渠道页见发布员工）。
**优点**：功能边界清晰，工程映射直接（Production WS / Channel Ops WS 各一）。
**缺点**：违背用户心智「做一条内容并发多平台是一件事」；切页打断连续流；单人对四页认知负担重。
**认知成本**：高（需理解四个功能分区及其关系）。
**扩展成本**：中（加新功能 = 加 tab，但 tab 越多越碎）。
**实现复杂度**：低（与底层 Production/Channel 拆分一一对应，最省力）。

> 评价：实现最省力，但**用户体验最差**——把内部能力分层直接暴露成导航。不推荐为主方案。

---

## OPTION B — Home → 进入不同 Professional Workspace

```
内容增长 Home
→ 制作工作台（Professional Workspace）
→ 渠道运营台（Professional Workspace）
→ 互动台
→ 数据台
```

**用户如何理解**：「先回 Home，再进一个专业间做深度工作。」
**第一次怎么创建**：Home 引导 → 选「去制作」进制作工作台。
**日常怎么使用**：每次操作先回 Home 再进子 Workspace；专业面沉浸。
**多账号怎么处理**：在渠道运营台内集中处理。
**Employee 怎么出现**：各 Professional Workspace 内以 Workstation / Presence 呈现。
**优点**：专业深度好，每个 Workspace 可独立优化（类似 XHS 的 Instance 专业取向）。
**缺点**：单人创作者每次都要 Home↔子 Workspace 跳转；「内容增长」被拆成多个入口，聚合感弱；轻操作（接受选题/确认发布）也要进专门间。
**认知成本**：中高（多入口、需记住去哪做啥）。
**扩展成本**：中（新增专业间 = 新增子 Workspace，但首页导航变长）。
**实现复杂度**：中（每个 Professional Workspace 需独立布局，复用 Shell 但内容各异）。

> 评价：适合「团队 / 重运营」场景，对单人 / 轻量创作者过重。可作未来「重度模式」备选，不作首版主方案。

---

## OPTION C — 经营单元为入口，内嵌 Production + Channel Ops

```
内容增长
└─ [经营方向]（如「Curis AI 内容矩阵」）
    ├─ 内容流（制作 + 分发 合并呈现）
    ├─ 账号
    └─ 数据
```

**用户如何理解**：「我先进我的经营方向，里面一条线把内容做了发了。」
**第一次怎么创建**：连接账号 → Curis 建议经营单元 → 进入该经营单元 → 内容流。
**日常怎么使用**：在经营单元内走「选题→制作→发所选账号→发布→回流」一条线。
**多账号怎么处理**：经营单元聚合其下所有账号，内容流内选「发到哪里」。
**Employee 怎么出现**：内容流上以责任状态浮现（谁在做哪一步）。
**优点**：最贴合「经营方向」心智；一条内容流不切页；多账号自然归到经营单元。
**缺点**：单账号用户被强迫先理解「经营单元」这一层（层级略重）；若用户只有一个经营单元，外层容器略显多余。
**认知成本**：低–中（单账号时容器冗余；多账号时正合适）。
**扩展成本**：低（加经营单元 = 加一层列表项，不重构）。
**实现复杂度**：中（需做经营单元容器 + 内容流编排）。

> 评价：方向对，但**单账号时的容器冗余**需缓解（见 OPTION D 的隐去策略）。

---

## OPTION D（提议 · 推荐）— Content Growth Business Home + 经营方向 + 连续内容流 + 按需 Professional Workspace

```
业务空间 → 内容增长（Business-level operating domain · 非一级区、非超级 Workspace）
├─ Content Growth Business Home（Attention + Light Operations：今天值得做 / 正在生产 / 待发布 / 账号动态 / AI在做什么 / 需我决定 / 经营方向切换 / 跨账号·跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback）
├─ [经营方向]（多账号时出现；单账号隐去该层）
│   └─ 连续内容流（制作 → 发到所选账号 → 发布 → 回流，一条线）
├─ 账号（Connected Accounts：平台/账号/状态/定位/所属经营方向）
└─ Professional Workspace（按需经 Shell Adaptive Surface / Deep Link 进入）
    ├─ Content Production
    ├─ XHS / Douyin / Future TikTok·Bilibili·YouTube Channel Operations
    └─ 用户不感知「跳办公室」，专业面只是内容流某步的深入
```

**用户如何理解**：「进来就看到该做的事；做内容是一条线；账号单独管；专业事点开看（但感觉还是同一个内容增长）。」
**第一次怎么创建**：
- 单账号：连账号 → 直接进 Business Home → 隐去经营方向层，Curis 内部当「你的内容经营」。
- 多账号：连完 → Curis 建议经营方向（CASE B/C/D）→ 确认 → Business Home + 经营方向层出现。
**日常怎么使用**：Business Home 聚合待办与动态；点进某条内容 → 连续内容流一条线做完；需要深度制作/某平台渠道运营时，经 Adaptive Surface / Deep Link 展开 Professional Workspace，但仍在同一内容流语境。
**多账号怎么处理**：经营方向聚合同方向账号；不同方向多经营方向切换；内容流内「发到哪里」三源合并（默认/AI推荐/手动）。
**Employee 怎么出现**：内容流 / 责任上以 Presence / Workstation 浮现（「内容策划·王芳 正在整理选题」），绝不暴露 Router / Capacity / Queue。
**优点**：
- 合并 Production 与 Channel Ops 为「一条内容流」，契合用户心智；
- Content Growth 明确为 Business Home（聚合/轻操作），专业深度只按需进 Professional Workspace，**不构成超级 Workspace**；
- 单账号零层级、多账号才显经营方向（渐进披露）；
- 完美复用 Shell（Main=Home/内容流；Context=选题库；Utility=数据/预览/审核；Professional 深度=Adaptive Surface/Deep Link 按需挂载）；
- 专业深度仍在（Professional Workspace 按需），但不强制常驻、不单列一级导航。
**缺点**：
- 内容流编排比 A 的切页复杂（实现侧）；
- 需要在「Business Home 聚合」与「内容流专注 / 专业面深入」间做好视图切换与语境延续。
**认知成本**：**低**（单账号几乎无层级；多账号只多一个列表切换）。
**扩展成本**：**低**（经营方向=列表项；专业面=声明式 Surface；不重构）。
**实现复杂度**：**中**（新的是 Home 聚合 + 内容流编排，但全面复用 Shell + XHS 先例）。

> 评价：吸收 C 的「经营方向容器」+ A 的「能力但不切页」+ B 的「专业面但按需」，并明确 Business Home 与 Professional Workspace 分工（DELTA UX-1），规避三者缺点。**推荐为主方案**。

---

## 方案比较总表

| 维度 | A 功能拆分 | B 专业 Workspace | C 经营单元入口 | **D 推荐（混合）** |
|---|---|---|---|---|
| 用户心智契合 | 低 | 中 | 高 | **高** |
| 单账号负担 | 高（四 tab） | 高（多入口） | 中（容器冗余） | **低（隐去层级）** |
| 一条内容流连续性 | 低（切页） | 中（进专门间） | 高 | **高** |
| 多账号处理 | 中 | 中 | 高 | **高** |
| Employee 出现 | 各页浮现 | 各 WS 浮现 | 内容流浮现 | **内容流浮现** |
| 认知成本 | 高 | 中高 | 低–中 | **低** |
| 扩展成本 | 中 | 中 | 低 | **低** |
| 实现复杂度 | 低 | 中 | 中 | **中** |

---

## RECOMMENDED PRODUCT MODEL（DESIGN RECOMMENDATION · 非 Frozen）

> 推荐 **OPTION D**（融合 DELTA UX-1 / UX-2 收敛），并明确其为**设计建议**，待 Product Model Closure Review 批准后方可进入高保真 / 前端 / Instance Spec。收口见 `Curis_Content_Growth_Product_Model_Closure.md`。

### 推荐模型要点

1. **IA 角色**：「内容增长」是 **Business-level operating domain**，挂在「业务空间」下（Blueprint 六区之子项），**不新增一级区、不新建 Primitive、不成超级 Workspace**。
2. **Content Growth Business Home**：负责 Attention / Light Operations / 经营方向切换 / 跨账号·跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback；首屏 = Attention + Light Operations 混合。
3. **经营方向（Office 用户面主词）按需显隐**：多账号时出现容器；单账号隐去，Curis 内部称「你的内容经营」；「经营单元」留作帮助/管理语境候选。
4. **一条连续内容流合并制作与分发**：Production 与 Channel Ops 在用户侧合并为「做内容 → 发到所选账号 → 发布 → 回流」一个连续动作；底层能力分层不暴露为两个 Workspace。
5. **Professional Workspace 按需进入**：真正的深度工作在 Content Production / XHS·Douyin·Future 平台 Channel Operations，经 Shell Adaptive Surface / Deep Link 自然展开，用户不感知跳办公室。
6. **发到哪里三源合并**：默认自动选择 + Curis 推荐（自然语言解释）+ 手动调整。
7. **HIGH_REUSE / FULL_DIVERGENCE 行为化**：用户只见「Curis 针对不同账号分别制作，能复用的自动复用」，不出现词。
8. **AI 员工以责任状态浮现**：谁在负责 / 正在做 / 卡在哪 / 需我决定；不暴露路由 / 容量 / 队列。
9. **增员两路**：主动增加 + Curis 白话建议（⑨ 未 Frozen，仅未来以 Frozen P7 呈现，指标全隐藏）。
10. **Context 默认隐藏、按需可追溯**；**Needs CEO 仅重大事由**（Frozen P7）。
11. **XHS 未来自然纳入**：内容增长为超集，XHS 成为「内容增长 → 小红书经营方向」的落地能力（不修改 XHS）。

### 用户看到的产品骨架（OPTION D 收敛）

> 内容增长 → 今天值得做什么 → 某个经营方向 → 某条内容 → AI 制作 → 针对账号分别完成 → 发布 → 数据回流

（而不是 Production Workspace / Channel Workspace / Routing / Variant / Target Set）

### 为什么不是 A / B / C 纯方案

- **A** 把内部能力分层直接暴露成导航，违背用户「做一条内容并发多平台是一件事」的心智，认知成本最高。
- **B** 对单人 / 轻量创作者过重，轻操作也要进专门间，聚合感弱。
- **C** 方向最对，但单账号时的经营方向容器冗余；D 通过「单账号隐去该层」化解，并进一步用 Business Home / Professional Workspace 分工（DELTA UX-1）避免把内容增长做成超级 Workspace。

### 与 Frozen Authority 的对应（证明推荐未破坏语义）

| 用户面（D） | Frozen 语义（不暴露原词） |
|---|---|
| 经营方向（Office 用户面主词；经营单元仅帮助/管理语境） | Office（①） |
| 账号 / 平台 | Channel Account / Channel（②） |
| 选题 / 要讲的内容 | Content Opportunity / Intent（③） |
| 发到哪里 | Target Account Set（④，三源合并） |
| 各账号分别制作 / 发布 | Variant / Publication（⑤，reuse_mode 行为化） |
| 其他账号可继续发 / 等全部准备好 | Distribution Execution Policy（④） |
| 谁在负责 / 正在做 | Responsibility Requirement（⑥）+ Routing（⑦）+ Employee（⑧） |
| 用了哪些资料（按需） | Context Isolation Truth Boundary |
| 需我决定（仅重大事由） | Needs CEO（Frozen P7） |

> 推荐模型**完全消费** Frozen Authority 语义，仅做用户面翻译与渐进披露，**未修改、未新增任何 Primitive**。

---

*Curis Content Growth — Workspace Composition Options · DESIGN RECOMMENDATION（非 Frozen）*
