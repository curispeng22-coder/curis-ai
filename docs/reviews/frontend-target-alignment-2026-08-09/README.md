# Curis 前端目标对齐复核（2026-08-09）

Status: Review

Decision: `BLOCKED_PENDING_RUNTIME_REVIEW`

本复核只判断当前 `frontend/` 是否已经与 Blueprint 4.12、Business Runtime v1.6 和 Frozen Design System 对齐；它不授权前端改造，也不把当前页面渲染结果当成目标产品已交付。

## 1. 复核基准

| 维度 | 当前权威 | 结论要求 |
| --- | --- | --- |
| Product | `docs/01_Product/Curis_Product_Blueprint.html` 4.12 | Company OS 固定、Workspace 开放、CEO Operating Day、三业务共享内核 |
| Runtime | `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md` v1.6 | 状态、责任、证据、交接、验收和失败路径必须可持久化 |
| Design | `docs/03_Design/Curis_Design_System.md` Frozen | 220px 侧栏、52px 顶栏、唯一令牌、三主题、中文界面、全局 Assistant |
| Fact | `docs/00_Context/CURRENT_STATE.md` Frozen | 当前代码仍是 Project/Task-first 交付基线，不得描述为目标态 |

## 2. 当前代码事实

只读检索结果：

| 证据 | 当前事实 | 产品含义 |
| --- | --- | --- |
| `frontend/components/terra/TerraSidebar.js` | 仍由 TerraSidebar + TerraNavData 提供导航，代码注释称 Terra 为 Frozen 视觉 | 代码壳层可以复用，但必须按 Frozen Design System 和目标导航逐项验收；Terra 名称不能继续代表产品身份 |
| `frontend/app/globals.css` | 已有 `220px` 侧栏、`52px` 顶栏和品牌绿 token；同时保留旧 TerraShell / 旧壳层注释 | 尺寸基础部分对齐，代码注释与产品身份仍混杂，需要在正式 UI Issue 中清理 |
| `frontend/app/ceo-office/page.js` | CEO 页面仍通过 KPI 小卡和项目 / 任务 / Artifact 聚合形成经营视图 | 这是已交付事实，不等于 CEO Operating Day 的 Business Runtime；不能用页面聚合替代 Pulse / Evidence / Decision Runtime |
| `frontend/components/assistant/GlobalAssistant.js` | Assistant 已有全局 Provider / Host，但 Snapshot 仍读取 projects / tasks / artifacts，并能链接到 execution task | Global Assistant 基础设施可复用；业务语义仍是旧执行链，不能宣称 CEO Assistant v1.6 已成立 |
| `frontend/app/ceo-office/execution/`、`projects/`、`reports/`、`analytics/`、`runtime-trace/` | 旧 Project / Task / Execution 入口仍存在 | 目标产品不能以这些页面作为 CEO 一级经营入口；后续应迁入 Workspace 内部或按迁移决策隔离 |
| `frontend/app/onboarding/`、`frontend/app/guide/` | 首次引导和工作台引导已有实现 | 可作为 First Arrival 交互证据，但还不能证明 Company / Business / Workspace / AI Team 的 Runtime 已持久化 |

### 2.1 现场事实刷新（2026-08-09）

本次继续核对工作树与实际 SQLite 后，确认“页面已经出现”与“目标 Runtime 已成立”之间仍有明确边界：

| 现场证据 | 当前事实 | 不能据此推出 |
| --- | --- | --- |
| `frontend/app/ceo-office/workspace/page.js` | 工作空间门户通过 `getProjects()` 读取 Project，再按 Project 状态派生“运行中 / 装修中 / 已归档” | 不能证明 `Workspace / Blueprint / Cycle` 是独立业务事实源 |
| `frontend/app/ceo-office/workspace/page.js` 的 `resolveRuntimeHref()` | 仍按 `project_type` 把入口映射到固定的研发、小红书、抖音页面 | 不能把固定路由映射当成 CEO 创建业务后生成的 Workspace |
| `frontend/app/ceo-office/page.js` | CEO Desk 读取 `getHomeSummary()` 与 `getOperatingDay()`，当前数据投影仍以 Project / Task / Artifact 聚合为主 | 不能证明 v1.6 的 `MorningBrief / Matter / Handoff / DecisionPacket / Closeout` 已由 Runtime 持久化 |
| `backend/tests/test_mvp_phase2_s3_ai_employee.py` | 验证的是旧 `employee_instances`、能力绑定和租户隔离 CRUD | 不能替代 `AIEmployee / RoleSlot / CapabilityBinding` 的生命周期、授权、容量和换责 Simulation |
| `backend/data/curis.sqlite` | `business_directions`、`commitments`、`workspaces`、`outcomes`、`assistant_identities`、`guide_sessions`、`runtime_transition_log` 当前均为 0 条；`employee_instances` 与 `department_instances` 有记录 | 不能把已有 Employee / Department 记录误报为 First Arrival、CEOAssistant 或目标 AI 组织运行记录 |

这次刷新不改变当前结论，反而强化迁移边界：当前代码有可复用的组织 CRUD、CEO Desk 和 Workspace 视觉入口，但仍是旧执行链上的交付基线；必须先通过 Runtime Foundation，再把这些入口接到 v1.6 对象和状态入口。

## 3. 与 Visual Acceptance Gate 的对照

| 门禁 | 当前证据 | 结论 |
| --- | --- | --- |
| 壳层 220px / 52px / 390px | CSS 有 220px / 52px；Assistant 抽屉运行行为仍需浏览器实测 | 部分通过，待真实 UI Review |
| 唯一令牌 | `globals.css` 有 `--ui-*`，但组件和历史 Terra 代码仍需逐页面扫描 | 未通过证明 |
| 三主题 | theme.js / globals.css 存在主题通道 | 未证明所有页面结构、按钮与错误态一致 |
| 中文界面 | 主要页面已有中文；旧对象、指标和开发入口仍混合 | 未通过证明 |
| Assistant 边界 | GlobalAssistant Provider / Host 存在 | 业务快照仍 Project/Task-first；未证明 v1.6 责任与升级链 |
| Runtime 动作 | 页面有执行、项目、任务按钮 | 未连接 v1.6 Cycle / Handoff / Acceptance 状态入口 |
| 真实证据 | 当前数据库和目标 Runtime 对象尚无记录 | 未通过 |

## 4. 迁移边界

在 Runtime Foundation Review 通过前，前端不得做以下事情：

- 不把 CEO Office 页面改名或重排成目标导航并宣称迁移完成；
- 不删除 Project / Task / Workflow 路由或数据；
- 不把静态 Assistant Snapshot 改写成 v1.6 运行事实；
- 不为研发、小红书、抖音复制三套页面；
- 不用视觉截图、接口 200 或组件状态代替 Runtime 证据。

Runtime Foundation 通过后，前端迁移 Issue 必须单独列出：

1. Company OS 导航和 Workspace 入口的唯一映射；
2. CEO Desk / Assistant 的 v1.6 数据投影；
3. 研发 Cycle Office、内容运营办公室和 Studio 的状态动作；
4. 旧 Project / Task 入口在 Workspace 内部的归位或隔离；
5. 三主题、中文术语、空 / 加载 / 失败 / 未授权状态和浏览器证据。

## 5. 结论

当前前端是“具有可复用壳层、Assistant 基础设施和旧执行能力的 Project/Task-first 应用”，不是 Blueprint 4.12 / Runtime v1.6 的已交付 Company OS。

因此本复核保持 `BLOCKED_PENDING_RUNTIME_REVIEW`。下一份前端 UI Issue 必须等待 `RUNTIME-FOUNDATION-001` 通过，并以真实 Runtime 记录作为 UI 数据来源。
