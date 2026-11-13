# Curis 旧系统迁移与清理清单（2026-08-09）

Status: Review

本清单把旧内容从“当前产品空间”中隔离出去，但不直接抹除历史证据。所有实际移动、删除、
路由下线和数据清理都必须在对应 Issue 中执行，并在 Change Log 留下来源与结果。

## 1. 清理原则

| 原则 | 说明 |
| --- | --- |
| 当前空间只有一套产品 | 只允许 CEO Company OS / Workspace 方向进入当前设计和开发入口 |
| 历史不等于当前 | 被替代的内容进入 `docs/99_Archive/`，标记 `Deprecated` 和 `Do Not Use` |
| 先引用扫描，再移动 | 使用 `rg -n` 检查 Markdown、代码、测试、构建和部署引用 |
| 先备份，再处理数据 | 不物理删除数据库记录，不在未确认依赖前删除 Project/Task 数据 |
| UI 不是独立真相源 | UI 链路作为证据；确认后补入 Blueprint，再进入实现 |

## 2. 文件与目录处理矩阵

| 范围 | 当前问题 | 建议动作 | 当前阶段 |
| --- | --- | --- | --- |
| `docs/01_Product/Curis 产品梳理 1.0_副本/` | 大量旧 Project/Task、旧模块和开发规范混在产品目录 | 整体 `Archive`，建立替代索引；代码引用另行迁移 | 待确认 |
| `docs/01_Product/Curis_Product_UI_Blueprint_v1.0.html` | 已完成 canonical rename；旧路径不再是 Current 入口 | 旧路径保持缺失并作为历史迁移记录；Current UI 依据为 `docs/01_Product/Curis_Product_UI_Blueprint.html` | 已完成 · 2026-08-18 |
| `.workbuddy/output/` | WorkBuddy 生成的阶段产物使用了不适用的 Approved/Gate 状态 | 移出当前产品阅读路径，保留为审计证据 | 待确认 |
| `curis-ui-prototype/` | 仍有固定业务、演示数据和旧办公室页面 | 保留可复用视觉资产；旧业务结构和演示数据隔离 | 待确认 |
| `frontend/app/ceo-office/execution*` | Task-first 入口暴露在 CEO 产品中 | 迁入 Workspace 内部或隔离到开发入口 | 待确认 |
| `frontend/app/ceo-office/brainstorm*`、`reports*`、`runtime-trace*` | 非 Blueprint 一级经营入口 | 隔离或删除，保留迁移依据 | 待确认 |
| `frontend/components/terra/TerraNavData.js` 与原型 `canonical-nav.js` | 两套导航来源 | 评审后只保留一个运行时来源 | 待确认 |
| `backend/data/curis.sqlite`、`data/*.sqlite`、`backend/*.db` | 运行数据库与历史/测试数据库混杂 | 备份、标记、确认唯一运行库后再清理 | 待确认 |
| `graph-*` 项目和 `local-demo-company` | 测试/演示记录进入 CEO 事实 | 隔离 fixture；生产 Company 不预置任务，由 CEO 在对应 Business Workspace 创建工作 | 待确认 |

## 3. 不允许重新进入当前空间的内容

- Project / Task / Workflow 作为 CEO 一级产品心智
- 固定的小红书、抖音、软件开发办公室作为无法由 CEO 创建/配置的硬编码业务
- `graph-*`、`local-demo-company` 等演示数据
- 独立 Assistant 侧栏或第二套 Assistant 任务系统
- 未经过 Blueprint 评审的工作台、模板市场、商业化方案
- 页面存在但没有 Runtime、证据、验收和关闭条件的功能

## 4. 三业务并行边界

三条业务可以同步进入产品设计和验证，但必须共享同一个 Company OS、CEO Assistant、AI
组织、Evidence、Decision 和 Change Runtime。三条业务只能在 CEO 创建或确认后生成对应
Workspace；不能通过预置卡片、fixture 或固定办公室绕过业务创建。

| 业务 | 当前作用 | 独立必须验证的内容 |
| --- | --- | --- |
| 研发工作台 | 首个业务轨道；第一个 dogfood 任务是“Curis 的自研发”（工作项名：完善 Curis） | 意图、研发责任、真实代码/测试、CEO 验收、下一周期 |
| 小红书运营工作台 | 并行重点业务轨道 | 内容生产、发布授权、播放/互动/粉丝等外部结果、复盘 |
| 抖音 / TikTok 运营工作台 | 并行重点业务轨道 | 内容生产、发布授权、播放/互动/成交等外部结果、复盘 |

## 5. 清理完成判定

清理只有同时满足以下条件才算完成：

1. 当前文档入口不再出现两套产品定义。
2. 当前导航只有一个来源，且不暴露旧 Task-first 入口。
3. 当前 Company 数据不再读取跨 Company fixture。
4. 当前原型只保留已评审的三类工作台链路、研发工作台的“Curis 的自研发（完善 Curis）”任务和通用 Company OS 组件。
5. 旧内容都有 Archive / Deprecated / 替代文件记录。
6. 新开发者仅阅读 `CURRENT_STATE → Blueprint → Runtime Blueprint → Design System` 就能开始工作。
7. 三条业务都能从同一 Company OS 进入，但业务差异只存在于各自 Workspace，不复制三套产品。
