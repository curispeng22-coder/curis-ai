# Curis XHS Workspace — Instance Spec v1

> **定位**：XHS（小红书）是 Curis Company OS 的**一个具体 Workspace 实例**的专业实现（Instance），不是 Shell，也不是全局 Pattern。本 Spec 只定义「小红书自己怎么做」，不向上提升为 Shell / Shared 基线。
>
> **三层边界（硬约束）**：
> - **Shell Contract** = 所有 Workspace 共享（Pane Shell / Toggle / Search / Resizable 等）。来源：`Curis_Desktop_Pane_Shell_Exploration_v1.md`。
> - **Shared Pattern** = 跨 Workspace 可复用能力（Employee Presence / System Activity / 三层责任 / Handoff / Result Reference 等）。来源：本 Spec §8–§11 标记 `SHARED` 者。
> - **XHS Instance** = 小红书自己的专业实现（Calendar / Note / Analytics / 业务对象语义）。**不升格**为全局 Pattern。
>
> **状态**：XHS INSTANCE AUTHORITY RECONCILED（2026-08-21）· Multi-Surface 产品模型已接受；具体菜单与最终迁移仍待独立 Design / Implementation Gate
>
> **关联文档**：
> - `Curis_Desktop_Pane_Shell_Exploration_v1.md`（Shell Contract，共享）
> - `Curis_XHS_Workspace_Design_Brief.md`（产品简报，需求源）
> - `Curis_XHS_Workspace_Calendar_Pattern_Spec.md`（Calendar 专项，Instance）
> - `Curis_XHS_Workspace_State_Semantics_Audit.md`（状态语义审计，Instance + Shared Delta）
> - `Curis_XHS_Workspace_Visual_v4.html`（高保真实物）

---

## 1. XHS Workspace 定位

Curis Company OS 中的一个 **Publishing / Content Professional Workspace 实例**：Department =「内容增长部」，Business / Parent =「小红书运营」，Workspace =「AI 科技」。

- 它是 **Company OS 的租户侧专业实现**，不是一个独立产品。
- 它在 Curis 的 **Organization 层（Company → Department → Business → Workspace）** 中挂靠于「内容增长部 / 小红书运营 / AI 科技」。
- 它是一套完整专业环境，可拥有多个 Professional Surface；不是一个页面，也不是每个 Surface 各自拥有一支 Team。
- 它的业务对象、状态机、Analytics 闭环都属于**本实例的专业域**，不反向约束其他 Workspace（如 RD）。

---

## 2. Content Object × Time

XHS 的核心设计常量之一：

- **Note 是业务对象**（Content Object），承载小红书图文内容（封面 / 标题 / 正文 / 标签）。
- **Calendar 是时间轴**（Time），用于组织 Note 的排期与发布节奏。
- 日历格内放 **Note 对象**（封面 + 标题 + 轻量 Presence + Status），**不退化**成传统 Scheduler 事件条（无纯事件标题、无 calendar-only 条目）。
- 这一常量由 **XHS Instance** 定义，属于 Instance 专业域（其他 Workspace 的时间轴语义可能不同，如 RD 用 Sprint / Milestone）。

---

## 3. Professional Surface Candidate 与 Calendar 归位

- 当前 Surface Candidate：经营概览、研究洞察、内容运营、数据增长、用户反馈；商业化为 Optional，团队与资料为 Company OS scoped projection。
- **经营概览是 Workspace default candidate**，用于理解当前业务的整体经营状态；具体菜单名称、排序、显隐与默认细节尚未冻结。
- **Publishing Calendar 归属于内容运营内的 Object View**，继续负责表达「什么内容、什么时间、什么状态、谁负责」，但不再是 Workspace Default，也不构成独立 Surface。
- 本节不授权 UI 重设计、Frontend 迁移或最终 Package Schema。

---

## 4. Multi-Note Calendar Pattern（Instance）

> 详细规则见 `Curis_XHS_Workspace_Calendar_Pattern_Spec.md`。摘要：

- **Month / Week / Day Focus 分工**：Month 看整月节奏 + 密度；Week 空间更大（详细布局 RESERVED）；Day Focus 处理单日很多 Note 的溢出。
- **单日展示规则**：
  - 0 篇：空日期格
  - 1 篇：完整 Primary Note Card
  - 2–3 篇：1 Primary + Compact Rows
  - 4+ 篇：1 Primary + 最多 2 Compact + `「+N 篇」` 收口；**禁止日期格无限增高**
- **Compact Note Row**：时间 + 轻量 Presence `[陈]` + 标题 + 状态色点，低视觉重量，非完整卡片。
- **Primary 选择优先级（最终）**：P0 Needs CEO/Blocking/Failed > P1 用户选中 > P2 Current Executor Working > P3 排期最近 > P4 时间排序。**Attention 高于「用户之前选中」**。
- **Day Focus**：冻结「`+N` → Day Focus」入口；**不冻结呈现**（A. Main 内 / B. Calendar Morph / C. Overlay 三选一待定，当前 v4 Overlay 仅 PRESENTATION EXAMPLE）。

---

## 5. Calendar → Note Split Working

- 点击日历中的 Note（Primary 或 Compact Row）→ 进入 **Note Selected / Split Working**（状态 B）。
- Main Pane 内 Split 为：左「时间上下文 / 选题库信号」，右「Note 工作区（封面 + 标题 + 正文 + 标签 + 状态）」。
- 不另造 Note 详情页；Calendar 与 Note 是同一对象的两种视图。
- Split 是 XHS 实例的**工作流呈现方式**（Instance 专业），不升格为 Shell 通用布局。

---

## 6. Employee Presence（SHARED · 见 §8 三层责任）

- Presence **只**表达 **Current Responsibility / Current Executor**（有真实员工在场）。
- 在 XHS 中用于：Calendar Note 卡片头像、状态 B/D 的「陈真 · 内容创作 · 制作中」、状态 C 的「王芳 · 内容审核 · needs_ceo」。
- 不表达 Object Owner，不表达历史 Handoff，不伪装成系统活动。
- **SHARED Pattern**：跨 Workspace 复用，来源 State Semantics Audit §2/§7。

---

## 7. System Activity（SHARED · 见 §8 三层责任）

- 当 **Current Executor = none**、系统接管运行时（Analytics / Monitoring / Automation / Content Reuse Loop），改用**独立 System Activity 组件**。
- 特征：**无员工头像、无「工作过程」入口、不伪装成 Employee Presence**。
- XHS 中用于状态 E 的「自动数据观察中 / 发布员工已完成发布（历史 Handoff）/ Object Owner AI 科技 Workspace / 当前无执行员工」。
- **SHARED Pattern**：跨 Workspace 复用；与 Employee Presence 不得混用。

---

## 8. Object Owner / Current Responsibility / Current Executor（SHARED）

> **Shared Pattern Delta Candidate #1**：`Object Owner ≠ Current Responsibility ≠ Current Executor`

- **Object Owner**：业务对象稳定归属（Business / Workspace / 长期岗位，如「AI 科技 Workspace」）。**不因单次 Handoff 改变**，**不进入 Employee Presence**。
- **Current Responsibility**：当前工作阶段责任方；Handoff 转移它。
- **Current Executor**：此刻真正执行者；员工完成 / 系统接管时允许为 **none**。
- **Presence 硬边界**：只表达 Current Responsibility / Current Executor；不是 Object Owner；不是「最后处理过的人」。

---

## 9. Handoff（SHARED）

- Handoff = **责任转移事件**（Current Responsibility 的变更），由已完成员工自动触发下一员工。
- XHS Handoff 链（单一事实源）：`策划·李翔 → 内容创作·陈真 → 内容审核·王芳 → 发布员工 →（已发布）→ 数据复盘（系统自动，非 Handoff）`。
- 历史 Handoff 以 **Event / Result** 呈现（如状态 E 的 `✅ Handoff：陈真 → 王芳 → 发布员工 已完成发布`），不占 Presence。
- **升级 CEO 不是 Handoff**（见 §11）。

---

## 10. Automation by default（SHARED 原则）

- **Automation by default；Human action only at Decision Gates。**
- 员工完成 → 自动 Handoff 下一员工；发布完成 → 自动进入 Analytics / Content Reuse Loop。
- CEO **不充当工作流「下一步」按钮**：只在 Decision Gate 出现。
- 这一原则跨 Workspace 通用（SHARED）。

---

## 11. Needs CEO / Decision Gate（SHARED · 采用 Frozen §3.13 CEO Decision Package · P7）

- **Needs CEO** = 当前员工（仍持 Current Responsibility / Executor）已完成判断 → 自动升级 **Decision Gate**。
- **CEO = Decision Authority**，不接管 Current Responsibility，不产生 Handoff。
- Presence 仍显当前员工（如状态 C 的王芳），不显 CEO 为责任方。
- CEO 决策后 → 工作流自动恢复（自动发布或退回修改）。
- **内容结构（Frozen §3.13 P7）**：决策须语义覆盖 8 要素、主界面只讲 CEO 语言、专业证据走 Layer 2；**8 要素是语义非固定 UI**；Impact/Risk/Cost/Recommendation 须带 Provenance（FACT/POLICY/EVIDENCE/EST/UNK），禁止编造。
- **Layer 0 复杂度感知动作**：XHS 合规审核属简单·低歧义·低风险类，Layer 0 可直接 `[按建议处理] [其他方案] [暂缓]`；展开后显示紧凑 Plain Package。不可逆 / 高风险类才降级为 `[查看方案] [暂缓]`（RD 数据迁移示例）。
- **员工 Conversation 只做白话汇报 + Decision Reference**，指向与顶部 Banner 相同的唯一 Decision Packet；不复制完整 8 要素、不把技术/审核细节原文扔给 CEO、不产生新 Handoff。
- 这一原则跨 Workspace 通用（SHARED）。

---

## 12. Context Surface（Instance）

- XHS 的 Context 承担 Workspace 的 **Domain Navigation + 当前 Professional Surface / 对象上下文**；在内容运营的 Note 工作里可投影「选题库 · 信号」作为创作上下文。
- 具体菜单名称、排序和层级尚未冻结；Context 不拥有 Team、Employee 或 Runtime。
- 由 Shell 的 **T2（Context Toggle）** 控制开合（Shell 能力，SHARED/Shell）。

---

## 13. Utility Surface（Instance）

- XHS 的 Utility Pane = **图文预览 / 文件预览**（状态 D），由 Shell 的 **T3（Utility Toggle）** 控制开合（Shell 能力）。
- XHS 内置浏览器（多 Tab + 最大化 + 全屏 Overlay）用于预览发布态 / 外链。
- **Utility 打开只是视图变化，不改变业务状态**（状态 D 业务时间线必须 = 状态 B）。
- Utility 的**内容**是 XHS 实例专业的（图文预览）；**开合/最大化机制**是 Shell（SHARED/Shell）。

---

## 14. Result Reference（SHARED）

- 已发布 / 已完成的对象产出称为 **Result**（如状态 E 的发布 Result、Analytics 数据）。
- Result 作为历史 Handoff 的落点，可引用、可复盘（Content Reuse Loop 反哺选题库）。
- Result 概念跨 Workspace 通用（SHARED）；XHS 的 Result 具体形态（小红书图文发布数据）是 Instance 专业。

---

## 15. Publishing / Analytics 闭环（Instance）

XHS 实例特有的业务闭环：

1. 选题信号（Context）→ 内容创作（陈真）→ 内容审核（王芳）→ 发布（发布员工）→ **已发布 Result**。
2. 发布后 → **系统自动 Analytics / Content Reuse Loop**（System Activity，Current Executor = none）。
3. Analytics 反哺选题库（Automation by default），形成闭环。
4. **数据复盘不是员工岗位**，是系统自动阶段（见 §7 / §9 链末）。

> 闭环中的「发布 / Analytics / 反哺」是 XHS Instance 专业业务；「自动阶段用 System Activity 表达」「闭环自动化」是 SHARED 原则。

---

## 16. A–E 核心状态矩阵（Instance）

| 状态 | 主导面 | 当前责任员工 | Employee / System | Handoff 状态 | 需 CEO | 下一步触发 |
|------|--------|--------------|-------------------|--------------|:------:|-----------|
| **A Content Calendar View** | 内容运营内 Calendar Object View | 无（日历观察态） | — | 未发生 | 否 | 用户事件 → B；AI 自动浮现 in-progress Presence |
| **B Split Working** | Note Split | 陈真（创作 / 制作中） | Employee Presence | 李翔→陈真（已发生）；陈真→王芳（未发生） | 否 | AI 自动：陈真完成 → Handoff 王芳 |
| **C Needs CEO** | Review Gate | 王芳（审核 / needs_ceo） | Employee Presence（仍王芳） | 陈真→王芳（已发生）；CEO 升级=Decision Gate，**非 Handoff** | **是** | CEO Decision → 自动恢复 |
| **D Utility Preview** | Note + Utility | 陈真（继承 B） | Employee Presence | 完全继承 B（仅视图变化） | 否 | 同 B |
| **E Published / Analytics** | Result + Analytics | 发布员工 completed（历史） | **System Activity**（Current Executor = none） | 陈真→王芳→发布员工（全链历史 Result） | 否 | 系统事件（自动 Analytics / Content Reuse Loop） |

> A–E 是内容运营 / Calendar 这一专业切片的状态矩阵，不代表 Workspace 默认入口。Object Owner 在所有状态均 = AI 科技 Workspace（稳定，不随 Handoff 变）。

---

## 17. DESIGN NOW / RESERVED / LATER / DO NOT COPY

### ✅ DESIGN NOW（XHS Content Operating slice）
- Calendar 作为内容运营内的 Object View + Multi-Note Month/Week/Day Focus 分工；不作为 Workspace Default。
- 单日 0/1/2-3/4+ 展示规则 + Compact Note Row + `「+N 篇」` 收口。
- Primary 优先级 P0–P4（Attention > 用户选中）。
- Calendar → Note Split Working。
- Employee Presence / System Activity 分离；三层责任语义。
- Handoff Event / Result Reference；Automation by default；Needs CEO Decision Gate。
- Context（选题库）/ Utility（图文预览）内容面。
- Publishing → 自动 Analytics → 反哺闭环。
- A–E 五状态矩阵一致。

### 🔒 RESERVED（已识别，未冻结）
- Week View 详细布局与单日上限。
- Day Focus 具体呈现（A. Main 内 / B. Calendar Morph / C. Overlay 三选一；当前 v4 Overlay 仅 PRESENTATION EXAMPLE / PENDING）。
- Day Focus 内筛选 / 排序 / 批量操作。
- 自然语言日期跳转、跨月拖拽改期、日历内联编辑。
- Search Surface 的 Recent / AI 问答 / Command Palette / 高级过滤器（见 Pane Shell Spec §9.8 RESERVED）。
- 多真实员工协作、深度 CRM/ERP 集成、Marketplace（Blueprint §16 暂不建设）。

### ⏳ LATER（未来轮次）
- RD Workspace 实例（独立专业域，不复用 XHS Calendar/Note 作为全局）。
- 抖音等更多 XHS 同类实例（各自 Instance，共享 Shell / Shared Pattern）。
- 真实前端实现（待 Shell / Shared Delta Review 后起 Issue）。

### 🚫 DO NOT COPY（明确禁止）
- 不把 XHS Calendar / Note / Analytics **升格为全局 Shell Pattern**（它们是 Instance 专业域）。
- 不创造「数据分析员工」「运营复盘员工」等伪岗位（数据复盘是系统自动阶段）。
- 不把 System Activity 伪装成 Employee Presence（不显员工头像、不显「工作过程」）。
- 不让 CEO 充当工作流「下一步」按钮（CEO 只在 Decision Gate）。
- 不把 Search 做成文件搜索器 / 任务历史列表（Company-wide Object Search，Task-capable 非 Task-first）。
- 不把经营概览退化为传统 Dashboard wall 或任务列表；保持 Low Surface Complexity。

---

**最终状态**：XHS INSTANCE AUTHORITY RECONCILED（2026-08-21）· AI 科技 Workspace 的 Multi-Surface 产品模型已接受；经营概览为 default candidate，Calendar 只属于内容运营 Object View；具体菜单、UI、最终 Package Schema 与 RD / XHS 产品迁移仍未冻结或实现。
