# Trae 交互原型 · 缺失页面清单（由 Trae 继续补齐）

> 比对基准：`UI_设计与布局规范.md` §11 交付清单（44 页正本）
> Trae 现状：`curis-ceo-office/pages/` 共 **23 个扁平 HTML 页**
> 比对日期：2026-07-26
> 目的：标出 Trae 漏做/缺的页面，交 Trae 按其既有排版风格补齐；补齐后由 UI Designer 团队基于完整交互原型产出「Figma 高保真 + Dev Mode 标注 + 规格 markdown」三件套。

---

## 1. Trae 已覆盖页面（对齐命名后 = 23 页，全部保留）

| # | Trae 文件 | 对应规范页 | 层级 | 备注 |
|---|---|---|---|---|
| 1 | ceo-office.html | ceo-home.html | 一级 | 命名差异，建议统一为 ceo-home |
| 2 | org-center.html | org-center.html | 一级 | |
| 3 | project-center.html | project-center.html | 一级 | |
| 4 | capability-center.html | capability-center.html | 一级 | |
| 5 | analysis.html | analytics.html | 一级 | 命名差异，建议统一为 analytics |
| 6 | brainstorm.html | brainstorm.html | 一级 | |
| 7 | knowledge.html | knowledge.html | 一级 | |
| 8 | workbench.html | execution.html | 一级 | 命名差异，建议统一为 execution |
| 9 | settings.html | settings.html | 一级 | |
| 10 | capability-agent-list.html | capability-agent-list.html | 二级 | |
| 11 | capability-model-list.html | capability-model-list.html | 二级 | |
| 12 | capability-skill-list.html | capability-skill-list.html | 二级 | |
| 13 | capability-tool-list.html | capability-tool-list.html | 二级 | |
| 14 | capability-workflow-list.html | capability-workflow-list.html | 二级 | |
| 15 | decision-center.html | decision-center.html | 二级 | |
| 16 | reports.html | reports.html | 二级 | |
| 17 | company-runtime.html | company-runtime.html | 二级 | |
| 18 | strategy-room.html | strategy-room.html | 二级 | |
| 19 | department-detail.html | department-detail.html | 三级 | |
| 20 | project-detail.html | project-detail.html | 三级 | |
| 21 | capability-skill-detail.html | skill-detail.html | 三级 | 命名差异，建议统一为 skill-detail |
| 22 | report-detail.html | report-detail.html | 三级 | |
| 23 | task-detail.html | task-detail.html | 三级 | |

> Trae 的排版布局已被用户确认优于 mockup 版，故上述 23 页**原样保留、不重做**。

---

## 2. Trae 缺失页面清单（共 20 页，由 Trae 补齐）

### 2.1 二级页面（缺 16 页）

| # | 缺失文件 | 所属一级区块 | 页面定位 | 优先级 |
|---|---|---|---|---|
| 1 | org-dept.html | 组织中心 | 部门空间列表（各部门的空间/职责概览） | 高 |
| 2 | org-employees.html | 组织中心 | 员工（动态岗位）列表 | 高 |
| 3 | project-dept.html | 项目中心 | 项目内的部门/团队视图 | 中 |
| 4 | analytics-org.html | 经营分析 | 组织维度经营分析 | 中 |
| 5 | analytics-project.html | 经营分析 | 项目维度经营分析 | 中 |
| 6 | analytics-workflow.html | 经营分析 | 工作流维度经营分析 | 中 |
| 7 | brainstorm-active.html | 头脑风暴室 | 进行中的会话列表 | 中 |
| 8 | brainstorm-results.html | 头脑风暴室 | 产出结果列表 | 中 |
| 9 | knowledge-company.html | 知识中心 | 公司级知识条目列表 | 中 |
| 10 | knowledge-project.html | 知识中心 | 项目级知识条目列表 | 中 |
| 11 | knowledge-dept.html | 知识中心 | 部门级知识条目列表 | 中 |
| 12 | execution-tasks.html | 执行工作台 | 任务队列列表 | 高 |
| 13 | execution-runs.html | 执行工作台 | Workflow Run 运行记录列表 | 高 |
| 14 | settings-profile.html | 公司设置 | 公司档案设置 | 低 |
| 15 | settings-brand.html | 公司设置 | 品牌/视觉设置 | 低 |
| 16 | settings-notify.html | 公司设置 | 通知设置 | 低 |

### 2.2 三级详情页面（缺 4 页）

| # | 缺失文件 | 关联二级入口 | 页面定位 | 优先级 |
|---|---|---|---|---|
| 17 | employee-detail.html | org-employees.html | 员工/岗位详情（职责+目标+权限+可用能力） | 高 |
| 18 | knowledge-entry-detail.html | knowledge-*.html | 单条知识条目详情 | 中 |
| 19 | brainstorm-session-detail.html | brainstorm-active.html | 单个头脑风暴会话详情 | 中 |
| 20 | run-detail.html | execution-runs.html | 单次 Workflow Run 执行详情（含日志/错误边界） | 高 |

---

## 3. 命名对齐要求（重要，避免三件套对不上）

Trae 当前命名与规范（DESIGN.md / UI 规范）不一致，补齐 20 页时请**统一采用规范命名**：

| Trae 现用 | 应统一为 | 原因 |
|---|---|---|
| ceo-office.html | ceo-home.html | 规范一级页命名 |
| analysis.html | analytics.html | 规范一级页命名 |
| workbench.html | execution.html | 规范一级页命名 |
| capability-skill-detail.html | skill-detail.html | 与规范三级命名一致 |

若 Trae 侧不便改名，请在 Trae 的 `SPEC.md` 内维护一份「Trae 文件名 ↔ 规范文件名」映射表，供三件套阶段对照。

---

## 4. 补齐后的交付目标

Trae 补齐后，交互原型应达到 **44 页全覆盖**（9 一级 + 30 二级 + 5 三级……含本清单 16 二级 + 4 三级），且：

- 全站内部链接无 404（含 sidebar / 面包屑 / 卡片跳转）
- Terra token 一致（`colors_and_type.css` 已与 DESIGN.md 对齐，无需改色）
- 空状态占位保留（不预填假数据，符合既有纪律）

---

## 5. 后续：UI Designer 团队补齐「三件套」的边界说明

Trae 交付完整交互原型后，UI Designer 团队据此产出三件套。当前环境**无 Figma 账号写权限 / 无 Figma MCP 连接**，故落地形式确认如下（待用户拍板）：

| 三件套项 | 标准 Figma 交付 | 本环境等价落地（推荐） |
|---|---|---|
| ① 高保真稿 | Figma .fig（hover/点击/抽屉/空态/错误态） | **高保真 HTML/CSS 原型**（可运行，含全部交互态） |
| ② Dev Mode 标注 | Figma Dev Mode inspect | **Dev Mode 规格 markdown**（尺寸/色值/间距/字号/组件 token 表，前端直读） |
| ③ 规格 markdown | 设计规格文档 | **规格 markdown 进仓库可 diff**（同左，即为交付物本身） |

> 若用户后续接入 Figma MCP / 提供 API Token，可直接产出真 .fig 与 Dev Mode；否则以「高保真 HTML 原型 + Dev Mode 规格 markdown」作为等效交付。
