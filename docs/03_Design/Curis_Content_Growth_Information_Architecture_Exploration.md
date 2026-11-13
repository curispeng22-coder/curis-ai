# Curis Content Growth — Information Architecture Exploration

**Status**: Exploration（设计探索 · 非 Frozen · 非最终高保真 · 非前端代码）
**阶段**: PRODUCT / WORKSPACE DESIGN — UX & IA Exploration（第 2 份 / 共 5 份）
**上位依据**: 同 `Curis_Content_Growth_UX_Model_Exploration.md` §顶部；重点参考 Shell Contract §1.3 六区导航、Blueprint「业务空间」模型、XHS Instance 单 Office 实例。

**边界**：不修改 Frozen Authority / Blueprint / XHS·RD；不新建 Primitive；不画高保真。本文为 DESIGN RECOMMENDATION。

> **Review 更新（2026-08-16 · APPROVED WITH 2 PRODUCT DELTAS）**：整体 IA 方向通过。本轮落实 **DELTA UX-1**：明确 Content Growth = Business-level operating domain（业务空间子项，非一级区、非超级 Workspace）；区分 Business Home 与 Professional Workspace，专业工作经 Shell Adaptive Surface / Deep Link 自然进入、用户不感知跳办公室；经营单元 → 经营方向（DELTA UX-2）。收口见 `Curis_Content_Growth_Product_Model_Closure.md`。不修改 Frozen / Blueprint / XHS。

---

## 1. 全局导航锚点（不可动）

依据 Blueprint 与 Shell Contract §1.3，全局六区固定不变：

1. 首页 / CEO 工作台
2. **业务空间**（Workspace 实例作为其子项出现，非第七个一级区）
3. 组织中心
4. 人才市场
5. 资料库
6. 会议

**结论**：Content Growth **不是新的一级区**，而是「业务空间」下的一个业务实例（与 XHS 小红书运营办公室、RD 研发办公室并列）。这避免了把内容增长升格为顶层概念（符合 Frozen：Content Growth = Business 级跨 Workspace 运营域，不新建顶层 primitive）。

---

## 2. 内容增长在「业务空间」下的位置

```
业务空间
├─ 小红书运营办公室        （XHS Instance · 已实现 · 单 Office 单账号退化形态）
├─ 内容增长              （本轮探索目标 · Business-level operating domain · 多经营方向多账号超集）
│   ├─ [经营方向 A] 小红书 + 抖音 + B站 + TikTok（同定位）
│   ├─ [经营方向 B] 抖音·AI科普
│   └─ [经营方向 C] 抖音·个人IP
└─ 研发办公室            （RD Instance）
```

> **关键**：当前 XHS 是「内容增长」的**退化形态子集**（单 Office·单账号）。未来 XHS 自然成为「内容增长 → 某经营单元（小红书）」下的能力，而非对立关系（详见第 6 节迁移建议，且不修改 XHS）。

---

## 3. 内容增长内部 IA 的三条可能路线（IA 视角）

> 与 `Curis_Content_Growth_Workspace_Composition_Options.md` 的 OPTION A/B/C 一一对应，但本节只谈**信息结构与导航**，不谈工作区内部布局。

### OPTION A — 功能拆分 IA
```
内容增长
├─ 制作（Production）
├─ 渠道（Channels / 账号）
├─ 互动（Engagement）
└─ 数据（Analytics）
```
- 用户心智：「按功能找地方」。
- 风险：把「做一条内容并发多平台」拆成「制作页做完了 → 切到渠道页分发」，割裂用户心智（违背 §UX 第 3 节结论）。

### OPTION B — 专业 Workspace IA
```
内容增长 Home
→ 进入不同 Professional Workspace（制作工作台 / 渠道运营台 / 互动台 / 数据台）
```
- 用户心智：「先回 Home，再进一个专业间」。
- 风险：对单人创作者，每次操作都要在 Home 与子 Workspace 间跳转，认知与点击成本高。

### OPTION C — 经营单元为入口 IA
```
内容增长
└─ [经营单元]（如「Curis AI 内容矩阵」）
    ├─ 内容流（制作 + 分发 合并）
    ├─ 账号
    └─ 数据
```
- 用户心智：「我先进我的经营方向，里面啥都有」。
- 风险：单账号用户被强迫先理解「经营单元」这一层（可缓解：单账号时自动隐去该层）。

### OPTION D（推荐，IA 视角）— Business Home + 经营方向 + 连续内容流 + 按需 Professional Workspace
```
业务空间 → 内容增长（Business-level operating domain · 非一级区、非超级 Workspace）
├─ Content Growth Business Home（Attention + Light Operations：今天值得做 / 正在生产 / 待发布 / 账号动态 / AI在做什么 / 需我决定 / 经营方向切换 / 跨账号·跨平台状态 / 内容进度聚合 / Needs CEO / Growth Feedback）
├─ [经营方向]（多账号时出现；单账号隐去该层）
│   └─ 连续内容流（一条内容贯穿 制作→发到所选账号→发布→回流）
├─ 账号（Connected Accounts：平台 / 账号 / 连接状态 / 定位 / 所属经营方向）
└─ Professional Workspace（按需经 Shell Adaptive Surface / Deep Link 进入：Content Production / XHS Channel Operations / Douyin Channel Operations / Future TikTok·Bilibili·YouTube Operations）
    └─ 用户不感知「跳办公室」，体验上只是内容流里的某一步展开成专业面
```
- 用户心智：「进来就看到该做的事；做内容是一条线；账号单独管；专业事点开看（但感觉还是同一个内容增长）」。
- 与 Shell Contract 完美契合：Main = Home / 内容流；Context Surface = 选题库；Utility Surface = 数据 / 预览 / 审核；Professional 深度工作面 = Adaptive Surface / Deep Link 按需挂载，不新建一级导航。

---

## 4. 与 XHS 当前实例的 IA 关系

| 维度 | XHS 当前（已实现） | 内容增长（探索） |
|---|---|---|
| 入口层级 | 业务空间 → 小红书运营办公室 | 业务空间 → 内容增长 → [经营单元] |
| 默认面 | Calendar-Dominant | Attention + Light Operations Home |
| 账号 | 单账号 | 多账号 / 跨平台 |
| 主对象 | Note × 时间（双主轴） | 内容流（制作+分发合并）× 时间（按需） |
| 专业面 | Context=选题库 / Utility=预览·数据·审核 | 同左，且可跨经营单元复用 |

> XHS 的「内容对象 × 时间双主轴」是其实例级专业约束（不升格 Shell）。内容增长 Home 不否定它——当用户在某经营单元内选中一条内容时，仍可展开为「内容 + 时间」视图。Home 是聚合入口，双主轴在内容详情层仍成立。

---

## 5. 未来多 Office / 多员工扩展的 IA 预留

- **多经营单元**：在 Home 下以列表 / 切换器呈现，不强制树形层级。
- **多 Employee 协作**：员工不进入导航（Frozen P2/P3），只在内容/责任上以 Presence 浮现。
- **N:N 共享账号**：首版遵循 1 Account : 1 Primary Office（Frozen Domain §1.2），N:N 共享关系以后扩展，IA 上预留「账号可加入多个经营单元」的入口但不首版强推。

---

## 6. XHS 当前实例的未来 IA 迁移建议（不修改 XHS）

仅输出建议，**本轮不改动 XHS**：

```
未来（非当前）：
业务空间 → 内容增长 → [小红书经营单元]
                      └─ 复用当前 XHS Note Workspace 能力
                         （Calendar / Note / 图文预览 / 数据 / 审核 / 内容复用环）
```
- 当前 XHS 实例保持不变，作为「内容增长 → 小红书经营单元」的落地能力之一。
- 不把 XHS Calendar/Note 升格为全局 Shell Pattern（Frozen 边界：Instance 专业域不升格）。
- 迁移是「纳入超集」而非「推翻重做」。

---

## 7. Content Growth 的准确 IA 层级与角色（DELTA UX-1 收口）

**Content Growth 在 IA 中的准确位置**：

- **层级**：它是「业务空间」下的一个业务实例（与 XHS 小红书运营办公室、RD 研发办公室并列），**不是 Blueprint 的第七个一级区**，也**不是把 Production/Channel/Engagement/Analytics 全装进去的超级 Professional Workspace**。
- **角色 = Business-level operating domain**：负责「经营层面的聚合与轻操作」，本身不承载专业深度工作。专业深度工作（制作、各平台渠道运营）由各自的 Professional Workspace 承担，按需挂载。

**Business Home ↔ Professional Workspace 的进入关系**（用户不感知跳办公室）：

| 维度 | Content Growth Business Home | Professional Workspace |
|---|---|---|
| 职责 | Attention / Light Ops / 方向切换 / 跨账号·跨平台状态 / 进度聚合 / Needs CEO / Growth Feedback | 真正的深度工作：Content Production / XHS·Douyin·Future 平台 Channel Operations |
| 用户停留 | 常驻（每天进来都在这） | 按需进入（做某步时才展开） |
| 进入方式 | 默认落地 | Shell **Adaptive Surface / Deep Link**（点内容流里的某步 → 展开专业面） |
| IA 表现 | 业务空间 → 内容增长 → Home / [经营方向] | 不单列一级导航；作为内容流某步的深入工作面 |
| 用户体验 | 「我在内容增长里看该做的事、做内容」 | 「我只是把这条内容的某一步在专业面里做细了」，不觉得换了 Workspace |

**关键判据**：如果用户在界面上需要先在「内容增长」和「制作 Workspace」「渠道 Workspace」之间反复横跳、且明显感知是两个独立大房间，IA 就失败了（那等于把 Content Growth 重新定义成了超级 Workspace）。正确做法：Home + 经营方向 + 连续内容流是一体，专业深度只在需要时点开，且点开仍处在同一条内容流的语境里。

---

## 8. RECOMMENDED IA（DESIGN RECOMMENDATION · 非 Frozen）

**推荐 OPTION D 的 IA（DELTA UX-1 / UX-2 收口）**：
- 内容增长作为 **Business-level operating domain** 挂在「业务空间」下，不新增一级区、不成超级 Workspace。
- **Content Growth Business Home** = Attention + Light Operations（含经营方向切换 / 跨账号·跨平台状态 / 进度聚合 / Needs CEO / Growth Feedback）。
- 多账号时出现「经营方向」容器；单账号隐去该层。
- 一条**连续内容流**合并制作与分发（用户侧不切页）。
- 账号独立管理面（Connected Accounts）。
- **Professional Workspace**（Content Production / 各平台 Channel Operations）经 Shell Adaptive Surface / Deep Link 按需进入，用户不感知跳办公室。

**认知成本**：低（单账号几乎无层级）；**扩展成本**：低（加经营方向 = 加一层列表项，不重构；专业面 = 声明式 Surface）；**实现复杂度**：中（复用 Shell + XHS 先例，新的是 Home 聚合与内容流编排）。

待 Product Model Closure Review 批准后，进入高保真 / Instance Spec。

---

*Curis Content Growth — Information Architecture Exploration · DESIGN RECOMMENDATION（非 Frozen）*
