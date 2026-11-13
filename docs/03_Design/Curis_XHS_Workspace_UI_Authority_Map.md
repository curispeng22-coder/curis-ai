# WORKSPACE UI AUTHORITY MAP（Shell / Shared / XHS / RD Instance）

> 生成：2026-08-21（Professional Workspace Authority Reconciliation）· RD Instance 于 2026-08-15 最终收口批准（RD INSTANCE APPROVED）
> 用途：供未来 **Design Agent / Codex / 前端实现** 一行定位「哪份文件是权威真源、哪些只是参考」。
> 当任何 Exploration / Prototype / 旧文档与下方 Authority File 冲突时，以 Authority File 为准。

---

## Authority File（权威真源）

| # | Authority File | Status | Owns What | Supersedes / Reference Only |
|---|----------------|--------|-----------|-----------------------------|
| A1 | `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | **Frozen** | **Workspace Shell Contract**（所有 Workspace 共享）：Four-Pane responsibility model；Desktop 同时可见时可用 Top-aligned Independent Pane / Pane-local Header / T1–T3 Toggle / Resizable Adaptive Surface / Company-wide Object Search / Utility Maximize | Four-Pane 不等于固定四根物理栏；取代旧「Global Topbar 横跨」模型；**Prototype JS/CSS 不进入**（见 A3） |
| A2 | 同上文件 §3（P1–P7） | **Frozen** | **Shared Company Patterns**（跨 Workspace 复用）：三层责任语义 / Employee Presence / System Activity / Automation by default / Handoff Event / Result Reference / **CEO Decision Package（P7）** + 边界澄清（Employee Presence≠System Activity / CEO Decision≠Handoff / System Runtime≠Employee） | 旧 §7 Delta-X5/X6/X7 候选记录已回写为 Frozen；DP-CEO-1 FINAL REVIEW APPROVED 回写为 §3.13 P7 |
| A3 | `Curis_Desktop_Pane_Shell_Exploration_v1.md` | **Reference Only**（探索稿） | Shell Delta 探索过程、结构图 SVG、§9.7 参考 JS 模板 | §9.7 标 `PROTOTYPE REFERENCE ONLY`：`querySelectorAll` / `classList` / `.app` 作用域 / 纯 CSS 显隐 / 具体事件绑定方式 **不进入** A1 |
| A4 | `docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md` | **XHS INSTANCE AUTHORITY RECONCILED** | 内容增长部 / 小红书运营 / AI 科技 Workspace 的 Multi-Surface Candidate；经营概览为 default candidate；Calendar / Note / Analytics / Content Object×Time 属于内容运营专业切片 | 具体菜单未冻结；Calendar 不再是 Workspace Default，也不升格为 Shell / Shared |
| A5 | `_system/tokens.css`（经 `Curis_UI_Frozen_Spec_2026-08-04.md` 表述） | **Frozen** | 颜色 / 字号 / 间距 / 圆角唯一真源 | 页面私有令牌（如旧 `#387bff` / `--radius-*`）一律禁止 |
| A6 | `docs/03_Design/Curis_XHS_Workspace_Visual_v4.html` | **Reference Only**（高保真实物） | XHS A–E 五状态设计验证稿 | 非前端实现；前端须按 A1/A2/A4 + A5 重新实现，不得直接搬运 HTML |
| A7 | `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` | **RD INSTANCE APPROVED** | RD（研发）Instance 专业实现：四 Pane 适配 / Employee Workstation（多开·状态模型）/ Conversation / Diff·Source·Preview Utility / Handoff / Needs CEO（Frozen P7）/ Result Reference / **Artifact Review Request（Layer 4 Candidate，不升格）** / 四概念责任语义（Responsibility / Responsibility Holder / Current Executor / Status） | 不升格为 Shell / Shared；与 XHS（A4）并列，各自 Instance 专业能力 |
| A8 | `docs/03_Design/Curis_RD_Workspace_High_Fidelity_v1.html` | **Reference Only**（高保真实物 / Approved Visual Reference） | RD 5 状态设计验证稿（Default / Context Open / Utility Open / Needs CEO / Parallel） | 非前端实现；前端须按 A1/A2/A7 + A5 重新实现，不得直接搬运 HTML |
| A9 | `docs/03_Design/Curis_RD_Workspace_UI_Drift_Audit_v1.md` | **Review Record / Reference Only** | RD 设计重构审计过程稿（Drift Audit + Responsibility 收口） | 过程记录，最终权威以 A7 为准 |

---

## 真源责任划分（一眼看懂）

```text
Shell 真源        → A1（四 Pane / Toggle 行为 / Search / Utility Maximize / Resizable）
Shared Pattern 真源 → A1 §3（P1–P7：责任语义 / Presence / System Activity / Automation / Handoff / Result / **CEO Decision Package**）
XHS Instance 真源  → A4（AI 科技 Multi-Surface Candidate；Calendar 是内容运营 Object View，不升格）
RD Instance 真源   → A7（研发四 Pane 适配 / Employee Workstation / Diff·Source·Preview / Handoff / Needs CEO / Artifact Review Request Candidate / 四概念责任语义，不升格）
Design Tokens 真源 → A5（颜色/字号/间距/圆角）
```

---

## Reference Only（明确非权威）

| File | 角色 | 为什么只是 Reference |
|------|------|----------------------|
| `Curis_Desktop_Pane_Shell_Exploration_v1.md` | Shell 探索稿 | 探索过程 + Prototype 实现；§9.7 已标 PROTOTYPE REFERENCE ONLY |
| `Curis_XHS_Workspace_Visual_v4.html` | XHS 高保真实物 | 设计验证，非代码；前端按权威文件重写 |
| `Curis_XHS_Workspace_Reference_Research.md` | 研究稿 | 竞品/证据来源，已吸收进 A4 |
| `Curis_XHS_Workspace_Design_Brief.md` | 产品简报 | 需求源，已收敛进 A4 |
| `Curis_XHS_Workspace_Design_Exploration_v1.md` | 空间探索 | 方案比较过程，结论已进 A4 |
| `Curis_XHS_Workspace_Interaction_Exploration_v2.md` | 交互探索 | 低保真状态线框，已进 A4 |
| `Curis_XHS_Workspace_State_Semantics_Audit.md` | 状态语义审计 | 审计→Delta 候选，已回写 A1 §3 |
| `Curis_XHS_Workspace_Calendar_Pattern_Spec.md` | Calendar 专项 | Instance 专项，已进 A4（不升格） |
| `Curis_XHS_Shell_Shared_Delta_Summary.md` | Delta 候选汇总 | 收口清单，已回写 A1 / A2 |
| `Curis_CEO_Decision_Pattern_Review.md` | CEO Decision 研究记录 | 已回写为 A1 §3.13 P7（CEO Decision Package），**Reference Only** |
| `Curis_RD_Workspace_High_Fidelity_v1.html` | RD 高保真实物 | 设计验证，非代码；前端按权威文件重写（A8） |
| `Curis_RD_Workspace_UI_Drift_Audit_v1.md` | RD 重构审计稿 | 过程记录，最终权威以 A7 为准（A9） |

> RD Instance 已于 2026-08-15 批准（**RD INSTANCE APPROVED**，A7）；抖音 Instance 尚未批准，当前**不进入** UI 权威范围。各 Workspace Instance（XHS=A4 / RD=A7）须各自独立 Spec，不得复用对方作为全局基线。

---

## 铁律（违反即错）

1. **Shell / Shared 全局共享**；XHS 的 Calendar / Note / Analytics **不得**反向提升为 Shell / Shared 基线或 Workspace Default；Calendar 只属于内容运营 Object View。
2. **Prototype 实现不进 Contract**：`querySelectorAll` / `classList` / `.app` / 纯 CSS 显隐 / 具体事件绑定方式只作 Reference，正式 React / Tauri 自行决定技术方案，只需满足 A1 §1.5.3 四条行为契约。
3. **Employee Presence ≠ System Activity**；**CEO Decision ≠ Handoff**；**System Runtime ≠ Employee**。
4. 所有视觉令牌只来自 A5；禁止页面私有令牌。
5. 变更顺序固定：Product Blueprint → 本 Authority Map 对应权威文件 → 代码；不得平行另建版本。

---

**状态**：WORKSPACE UI AUTHORITY RECONCILED（Professional Workspace / Multi-Surface accepted · XHS Calendar repositioned · RD Instance unchanged · 2026-08-21）
