# Curis — Shell / Shared Pattern Delta Summary

> **用途**：汇总本轮 XHS Workspace 最终收口中，**确认可回写**的 Shell 与 Shared Pattern Delta 候选。供后续统一回写 Shell Contract / Design System 并起前端实现 Issue。
>
> **纪律**：
> - 只整理**已确认**内容；不自行新增 Pattern；不扩大范围。
> - **暂不修改 Product Blueprint**（Blueprint §16 暂不建设项维持）。
> - **暂不修改正式前端代码**（等 Delta Review 批准后起 Issue）。
> - 暂不开始 RD / 抖音（各自独立 Instance，未来轮次）。
>
> **状态**：SHELL / SHARED DELTA FINAL REVIEW REQUIRED（随 XHS INSTANCE APPROVED CANDIDATE 一同待 Final Review）

---

## A. Shell Delta（所有 Workspace 共享）

来源：`Curis_Desktop_Pane_Shell_Exploration_v1.md`（§3 / §4 / §8 / §9）。

| # | Delta 项 | 内容摘要 | 来源章节 |
|---|----------|----------|----------|
| S1 | **Top-aligned Independent Pane** | 四独立 Pane 列（Navigation / Context / Main / Utility），各自 Pane Header + Pane Content，顶部齐平 | §3 Pane Shell |
| S2 | **Pane-local Header** | 每个 Pane 自带 Header（不横跨）；macOS traffic lights 仅在 Navigation 顶栏左侧 | §3.1 Nav Header |
| S3 | **T1 / T2 / T3 Toggle** | 三折叠按钮：T1 Nav（展开在 Nav 右 / 折叠在 Main 左）、T2 Context（常驻 Main 左）、T3 Utility（折叠在 Main 右 / 展开在 Utility 右，与 T1 对称） | §3 / §4 |
| S4 | **Resizable Adaptive Surface** | Pane 可拖拽 resizable；Utility 最大化 Overlay 全屏 | §5 |
| S5 | **Navigation Search → Company-wide Object Search** | Nav Header 轻量 Search icon（非常驻大框）→ 独立 Search Surface；Object-first, Task-capable（非 Task 历史搜索） | §9.1 / §9.8 |
| S6 | **Utility Maximize** | Utility 内置浏览器 + ↗ 最大化全屏 Overlay（Esc / ✕ / 点遮罩退出） | §9.6 |
| S7 | **Toggle 行为约束（跨 Workspace 强制）** | **冻结行为**：① T1/T2/T3 双向 Toggle（禁止独立 ✕ 关闭按钮）；② 展开/收起后控制入口持续可达；③ Pane 状态变化后 Toggle 仍可操作；④ Workspace / Pane 实例状态隔离。**技术实现不冻结**（以下仅 `PROTOTYPE REFERENCE ONLY`：`querySelectorAll` / `classList` / `.app` / 纯 CSS 显隐 / 当前 HTML 具体事件绑定方式；正式 React/Tauri 实现自行决定技术方案） | §9.7 |

> Shell Delta S1–S7 Recommended for Freeze，待本轮 Review 批准后回写权威 Shell Contract。

---

## B. Shared Pattern Delta（跨 Workspace 可复用能力）

来源：`Curis_XHS_Workspace_State_Semantics_Audit.md` §7（Delta Candidate #1 / #2）、Instance Spec §6–§14。

| # | Delta 项 | 内容摘要 | 约束 / 边界 |
|---|----------|----------|-------------|
| P1 | **Object Owner ≠ Current Responsibility ≠ Current Executor** | 三层责任语义：Object Owner 稳定归属（不随 Handoff 变，不进 Presence）；Current Responsibility 随 Handoff 转移；Current Executor 允许为 none | Presence 硬边界：只显 Current Responsibility / Executor |
| P2 | **Employee Presence** | 仅表达 Employee 的 Current Responsibility / Current Executor（有真实员工在场） | 不是 Object Owner；不是「最后处理过的人」；无员工时不用 |
| P3 | **System Activity** | 表达非员工 Runtime / Automation 状态（Analytics / Monitoring / 自动流水线），Current Executor = none 时启用 | **与 Employee Presence 不得混用**；无员工头像、无「工作过程」入口、不伪装成员工、不造伪岗位 |
| P4 | **Automation by default / Human action only at Decision Gates** | 员工完成自动 Handoff；发布自动进 Analytics；CEO 只在 Decision Gate，不充当工作流「下一步」按钮 | 跨 Workspace 通用原则 |
| P5 | **Handoff Event** | **Handoff Event** = 责任转移事件（Current Responsibility 变更），由已完成员工自动触发 | 历史 Handoff 以 Event / Result 呈现，不占 Presence；升级 CEO **不是** Handoff |
| P6 | **Result Reference** | 已发布 / 已完成产出称 Result，可引用、可复盘（Content Reuse Loop 反哺） | Result 概念跨 Workspace 通用；具体形态属 Instance 专业 |

> Shared Pattern Delta P1–P6 Recommended for Freeze pending Review，待本轮 Review 批准后回写 Design System / Shell Contract。

---

## C. 明确不升格为 Shell / Shared 的 Instance 项

以下属于 **XHS Instance 专业域**，**不得**反向提升为全局基线（见 Instance Spec §17 DO NOT COPY）：

- XHS Calendar（Month/Week/Day Focus 分工、单日 0/1/2-3/4+ 规则、Compact Row）。
- XHS Note（Content Object 图文结构、Split Working 布局）。
- XHS Analytics / Content Reuse Loop 业务闭环。
- XHS Context（选题库 · 信号）、XHS Utility（图文预览）的**内容**。
- Primary 优先级 P0–P4 的**业务取值**（Attention/Working 等状态语义属 Instance；通用「Attention 高于普通选中」原则可 SHARED）。

---

## D. 待办（Review 批准后）

1. 回写 Shell Contract（S1–S7）至 `Curis_Desktop_Pane_Shell_Exploration_v1.md` Status: Frozen。
2. 回写 Shared Pattern（P1–P6）+ 三层责任 / System Activity 至 Design System / Shell Contract。
3. 起 XHS 前端实现 Issue（Pane Shell + Toggle + Search + Calendar + State 语义）。
4. Blueprint §16 暂不建设项维持不变（不修改 Blueprint）。
5. RD / 抖音 Instance 留待未来轮次（各自独立，不复用 XHS Instance 作为全局）。

---

**状态**：SHELL / SHARED DELTA FINAL REVIEW REQUIRED
