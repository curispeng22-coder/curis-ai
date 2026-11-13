# CURIS V1 — ORGANIZATION CENTER UI ACCEPTANCE

**Authority Class**：REVIEW / UI ACCEPTANCE REGISTRATION
**Status**：Frozen
**Date**：2026-08-31
**Disposition**：UI ACCEPTED / IMPLEMENTED / ACCEPTED（implementation registration: `CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md`）

## Accepted scope

- **Organization Center Product**：ACCEPTED
- **Organization Center Interaction Structure**：ACCEPTED
- **Company Map**：ACCEPTED
- **Employee Directory**：ACCEPTED
- **Organization Center UI**：UI ACCEPTED（1440 × 900 Light）
- **Current Figma Design Baseline**：file key `2Fh7DgPPfLgdbvNtnzPnk9`, frames `106:3`, `106:230`, `106:457`

组织中心固定为两个顶部横向 Tab：**公司版图**、**员工目录**。左侧仍是七区一级导航，不恢复组织中心二级 Context Navigation。

公司版图继承 `Department Container → Business-first → Role / Staffing progressive disclosure → Vacancy / Risk / Business Focus`；Employee 按需展开，不默认铺满 Map；Workspace 是 Business 下的执行空间，不是公司版图默认主节点。`106:230` 是 Company Map 内部 Business Focus，不是第三个 Tab、独立 Business Detail 或 Workspace 页面。

员工目录采用 `Employee → Role → Business → Department` 反查；Workspace 只作必要弱上下文，不退回 HR Admin、Employee Management Backend 或 Capability Catalog。

## Boundaries

`CURIS_COMPANY_MAP_VISUAL_EXPLORATION.html` 继续是 `RESEARCH / HISTORICAL DESIGN INPUT`，不覆盖当前 Figma baseline。旧 AI Team Office、legacy Project organization、Capability-admin organization、traditional HR hierarchy 不得反向定义当前页面。

Current visual language：Direction D、Neutral Foundation、Iris `#806BE5`、Calm Density、Typography-first、Low-card、Current seven-area Navigation 与 Frozen Shell。

本次只接受 1440 × 900 Light。Prototype wiring、Search / Filter 细节、Dark、1024、accessibility / keyboard verification 保持 P2，不阻塞本次 UI Acceptance。

## Implementation status

`CURIS_V1_ORGANIZATION_CENTER_PRODUCTIZATION_REVIEW.md` 与对应 Issue 的 Browser、fresh packaged Desktop、restart/persistence、canonical projection、测试及 DB safety 证据已由 `CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md` 登记为 `IMPLEMENTED / ACCEPTED`。Dark、1024、accessibility / keyboard、Search / Filter wiring 与 legacy cleanup 仍为 P2。
