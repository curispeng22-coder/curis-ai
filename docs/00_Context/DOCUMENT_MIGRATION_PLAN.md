# Curis Documentation Migration Plan

Status: Review

Baseline: `main @ c0e1855f`

Updated: 2026-07-30

## 2026-08-09 Product Reset Addendum

本轮复位不直接删除历史内容。先以 `CURIS_FACT_BASELINE_2026-08-09.md` 固化现场，
以 `CURIS_LEGACY_MIGRATION_MAP_2026-08-09.md` 登记旧前端、旧 UI、旧文档、旧数据和
WorkBuddy 产物的处理动作。产品范围为三业务同步验证：研发工作台承接“完善 Curis”这一首个
dogfood 任务，小红书运营工作台与抖音 / TikTok 运营工作台同步进行 Workspace 设计和运行验证。

UI 原型和前端不再作为第二份产品真相；必要 UI 链路先登记到
`docs/01_Product/Curis_UI_Evidence_Alignment_2026-08-09.md`，经产品评审补入
唯一 Blueprint 后才进入代码。实际迁移仍需单独 Issue、引用扫描、备份和 Review。

## 1. Target Structure

```text
docs/
├── 00_Context/
├── 01_Product/
├── 02_Architecture/
├── 03_Design/
├── 04_Development/
├── 05_Features/
├── 06_Research/
├── 07_Decisions/
├── 08_Change_Log/
└── 99_Archive/
```

## 2. Directory Ownership

| Directory | Purpose | Current Source Candidates |
| --- | --- | --- |
| `00_Context` | 当前状态、文档规则、清单、迁移计划 | `knowledge/NOW.md`、`PROJECT_STATUS.md`、`TASKS.md`、`knowledge/CURRENT_CONTEXT.md` |
| `01_Product` | 产品定位、层级、用户流程、能力边界 | `docs/product/`、`docs/prd/`、`docs/status/USER_CAPABILITY_LEDGER.md` |
| `02_Architecture` | 系统、数据、API、Runtime、Security Contract | `docs/architecture/`、`docs/contracts/`、`knowledge/003_Architecture.md` |
| `03_Design` | Design System、当前 UI 规范和验收设计 | `docs/design/`、`frontend/design-spec/` 的有效部分 |
| `04_Development` | 开发、测试、部署、PMO 和协作规则 | `docs/standards/`、`docs/deployment/`、`docs/pmo/`、`docs/team-v2/` |
| `05_Features` | 当前功能定义和纵向切片证据索引 | 当前 MVP Issue/Review 的功能级索引 |
| `06_Research` | 竞品、技术和领域研究 | `docs/research/`、Paperclip/WorkBuddy 研究 |
| `07_Decisions` | 当前有效 ADR 和产品决策 | `docs/decisions/`、零散架构决策 |
| `08_Change_Log` | 事实变化、旧方案、新方案和影响 | Release Notes、状态变化和治理变更 |
| `99_Archive` | 历史方案、旧 UI、旧 Sprint、旧 Release 和 Prototype | `docs/sprints/`、`docs/release/`、`docs/demo/`、`docs/handoff/`、旧设计 |

## 3. Phase 1 — Current Stage

- 建立 Current State
- 建立 Document Inventory
- 建立 Status Rules
- 建立当前 Decisions
- 建立 Change Log
- 更新根 README 与 AGENTS 指向新事实源
- 不移动、删除或重命名既有文档

## 4. Phase 2 — Core Document Freeze

按顺序处理：

1. Product
2. Architecture
3. Design
4. Development
5. Features

每个域只保留一个 Frozen 入口文档；其他内容标记为 Review、Deprecated 或历史证据。

## 5. Phase 3 — Reference-Safe Migration

每批迁移必须：

1. 列出源路径和目标路径
2. 使用 `rg -n '<source-path>'` 检查引用
3. 更新 Markdown、脚本、测试、CI 和运行配置引用
4. 执行相关测试和构建
5. 在 Change Log 记录迁移
6. 保留可追溯提交

优先迁移没有代码引用的纯文档。任何可能被代码、测试、构建或部署脚本引用的文件保持原位，
直到独立迁移 Issue 获得确认。

## 6. Phase 4 — Archive

建议归档：

- 旧 UI V1/V2/V3 和导出图片
- 静态 HTML Prototype
- 已完成 Sprint、Release、Demo 和 Handoff
- 已被当前实现替代的架构方案
- WorkBuddy 作为产品基线的探索稿
- 旧 Workspace/Admin 分拆方案
- 旧 Current Context、Status 和 Task 历史

历史设计决策不删除；进入 Archive 后保持可搜索和可追溯。

## 7. Deletion Boundary

第一阶段不删除任何仓库内容。

后续仅允许删除可再生成且无治理价值的内容：

- Runtime log
- Cache
- Build output
- Generated output

删除前必须确认它们未被 Git 跟踪、未作为 Review Evidence 引用，并且存在明确再生成方式。

## 8. Known Migration Risks

- 根 README 和 `knowledge/NOW.md` 引用不存在的 `docs/curis-takeover/`
- 根 AGENTS 仍声明过期 Phase-1C Gate
- `docs/product/CURIS_PRODUCT_BASELINE.md` 声称存在尚未创建的
  `docs/delivery/CURRENT_DELIVERY_TARGET.md`
- Current State 同时分散在 `knowledge/NOW.md`、`PROJECT_STATUS.md`、`TASKS.md`、
  `knowledge/CURRENT_CONTEXT.md` 和 PMO 状态文件
- 大量 Issue、Review、Release 和 UI Export 造成搜索结果噪声
- 移动旧路径可能破坏 Markdown 链接、脚本、测试或自动化

## 9. Confirmation Gate

Phase 1、Phase 2 和 Phase 3-A 已完成。

Phase 3-B1 已获得独立确认，只授权迁移
`curis_workspace_blueprint/` 中 17 个非 ADR、无代码引用的 Deprecated Markdown。
两份历史 ADR 决策记录保持原路径。后续域迁移仍需要独立确认。
