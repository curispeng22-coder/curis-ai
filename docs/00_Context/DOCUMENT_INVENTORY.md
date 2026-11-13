# Curis Document Inventory

Status: Frozen
Authority Class: CURRENT / INDEX ONLY
Owner: Delivery Owner
Updated: 2026-10-25
Decision: [开发基线与文档维护决定](<../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)

索引用于定位，不产生 Product / Implementation Authority。本轮在既有索引中补齐当前入口及目录分类，不新建平行产品文档；2026-09-24 Workspace Audit/Cleanup 仍 CLOSED。

## 当前最小读取与任务

| 要找什么 | 唯一定位 |
|---|---|
| Agent 工作规则 / 当前导航 | [AGENTS](<../../AGENTS.md>) → [Entrypoint](<CURIS_CURRENT_ENTRYPOINT.md>) |
| 产品定义 | [Pointer 的 Product / Design Required Input](<PRODUCT_DOCUMENT_POINTER.md>) |
| 实现状态 / 开发事实 | [CURRENT_STATE](<CURRENT_STATE.md>) / [Development Guide](<../04_Development/Curis_Development_Guide.md>) |
| 当前任务 / 唯一进度 | [文档收口 Issue](<../../issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>) / [原唯一执行看板](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>) |
| 后续执行 / 既有专题清单 | [Execution Backlog](<../reviews/CURIS_V1_EXECUTION_BACKLOG.md>)；Final UI / Runtime Backlog 仍按原职责消费 |
| 已接受本地交付 | [RC9 Final Receipt](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/owner-incident-20261018-01/rootf-writing-ui-owner-01/RC9_DELIVERY_RECEIPT.md>)；安装指南和原回证原样保留 |
| 文档状态 / 维护来源 | [Status Rules](<DOCUMENT_STATUS_RULES.md>) / 本轮维护 Decision |

## 目录分类与本轮覆盖

| 目录/文件组 | 当前用途和处置 |
|---|---|
| docs/00_Context、01_Product、02_Architecture、03_Design、04_Development、07_Decisions、08_Change_Log | 既有正式目录；按入口和适用合同读取，名称/日期不自动赋予 Authority |
| docs/reviews、docs/research、issues、reviews | 按明确任务消费 Review / Research / Issue；历史成功不自动升级当前能力 |
| docs/99_Archive | 既有历史位置，非默认输入；CEO 精确批准的 A01–A03 已归档，其他历史材料不动 |
| frontend、backend、desktop、deploy、shared、tools、plugins | 当前代码/配置，保留原位；本轮只静态核对开发命令和文件保全 |
| artifacts/tasks | Task 专属回证、候选和生成物；既有 accepted release / QA / Owner 证据不动 |
| 根目录 PROJECT_STATUS / PROJECT_HANDOFF / TASKS | 现为 Frozen / CURRENT NAVIGATION ONLY 兼容指针；Deprecated / HISTORY 原文已归档 |
| 根目录业务/视觉探索、prototype、research 与备份目录 | 本轮仅分类和扫描引用，不因探索 CLOSED 就移动唯一可编辑来源 |
| data、默认 App 资料、未知数据库形态文件、工作树和本地环境 | 保留原位；不读取/哈希数据库内容，不清理、不重建、不恢复 |

前阶段记录 146 个顶层条目及有限子目录元数据；[目录清单](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/DIRECTORY_INVENTORY.json>)明确重型目录/资料/凭据排除项。
[文档头部索引](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/DOCUMENT_METADATA.csv>)是归档前头部快照，仅汇总当时 docs 内和本轮根入口的标题、Status、Authority Class 与所在位置，共 1234 行；不覆盖本次新增归档和根兼容指针状态；这是定位用 metadata survey，未重新做全产品 Audit，也不代表所有历史文档均已规范化或获接受。

## 已批准归档与继续保留

CEO 已确认原清单 A01–A03，本次迁移完成：

| ID | 保留的根兼容入口 | 已归档原文 | 归档分类 |
|---|---|---|---|
| A01 | [PROJECT_STATUS.md](<../../PROJECT_STATUS.md>) | [历史原文](<../99_Archive/development-baseline-2026-10-25/root-legacy-docs/PROJECT_STATUS.md>) | Deprecated / HISTORY |
| A02 | [PROJECT_HANDOFF.md](<../../PROJECT_HANDOFF.md>) | [历史原文](<../99_Archive/development-baseline-2026-10-25/root-legacy-docs/PROJECT_HANDOFF.md>) | Deprecated / HISTORY |
| A03 | [TASKS.md](<../../TASKS.md>) | [历史原文](<../99_Archive/development-baseline-2026-10-25/root-legacy-docs/TASKS.md>) | Deprecated / HISTORY |

[本次归档结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>) / [精确旧→新路径、SHA 与链接换算](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/MIGRATION_RECEIPT.json>) / [本次 Output Manifest](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/OUTPUT_MANIFEST.json>)。
[原候选说明](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.md>)与原 CSV 保留为批准来源，仍描述当时待确认/未操作的状态；本集合的授权与实际结果以上述最新记录为准。
只归档这三份正文并保留根指针，无删除。其他目录、已验材料、独有/未跟踪来源、缓存和未知资料继续原位 KEEP；不把本次批准扩大为任何其他路径许可。

## 历史索引原文（按原扫描日期解释）

以下旧基线/旧 Current 标签属于各次扫描当时，不能作为今天 HEAD 或默认产品入口。

Historical inventory status: Frozen

Historical scan baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Historical full-scan date: 2026-07-30

## 2026-08-09 复位审计增补

本清单的完整扫描日期仍为 2026-07-30，不能覆盖 2026-08-09 的现场事实。此次新增的
复位文档先登记如下，待旧系统迁移完成后重新生成完整清单：

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| `docs/00_Context/CURIS_FACT_BASELINE_2026-08-09.md` | Review | 记录当前代码、运行、数据、原型和文档事实 |
| `docs/00_Context/CURIS_LEGACY_MIGRATION_MAP_2026-08-09.md` | Review | 记录旧产品/旧 UI/旧数据的迁移与清理动作 |
| `docs/01_Product/Curis_UI_Evidence_Alignment_2026-08-09.md` | Review | 记录前端 UI 链路如何补充 Blueprint |

当前工作树存在大量未跟踪 WorkBuddy、桌面、原型、数据库和前端产物；在复位清理完成前，
不得把它们自动提升为当前有效文档或代码基线。

## 2026-08-14 产品文档收敛增补

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | Frozen | 新会话产品文档、主线程和 worktree 纪律唯一指针 |
| `docs/01_Product/Curis_Product_Assembly_Pack.md` | Review | CEO 主线、产品组成、三类业务空间和产品取舍 |
| `docs/01_Product/Curis_Product_UI_Flow_Pack.html` | Review | 逐页布局、动作、空态、失败、恢复和返回路径 |
| `docs/01_Product/Curis_Product_Development_Queue_Pack.md` | Review | 按用户结果排序的开发队列和验收合同 |

以上文件已从 7157 受控复制到主目录；来源 worktree 不是权威位置。

## 2026-08-14 产品重定基线增补

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| `docs/07_Decisions/ADR-0045-ordinary-user-desktop-product-rebaseline.md` | Frozen | 冻结普通用户优先、六区域、人才市场与独立 Workspace 方向 |
| `docs/01_Product/Curis_Product_Master_Map.md` | Review | 产品母版：顶层模型、对象边界、Workspace 与经营闭环 |
| `docs/01_Product/Curis_Product_Page_Map_v1.0.md` | Review | 页面地图、壳层、检查器、状态、返回和用户路径 |
| `docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md` | Review | 产品重新推导和竞品能力下沉结论 |
| `docs/01_Product/Curis_Talent_Market_Product_Map.md` | Review | 人才市场用户路径和首版范围 |
| `docs/01_Product/Curis_Talent_Market_Integration_Contract.md` | Review | 市场、设置、组织和 Workspace 的集成边界 |
| `docs/01_Product/Curis_Talent_Market_Resource_Audit.md` | Review | 外部专家、Skill、Connector 和 Agent 资源审计 |

## 2026-10-07 平台/账号本地链合同增补

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| `docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md` | Frozen | 2026-10-07 CEO 确认：CG Platform/ChannelAccount 本地模型、诚实未连接与人工回填三强制、不发出的发布核验清单；V1-P3 平台链 S1–S3 产品输入 |

## Scope

本清单覆盖 Git 已跟踪文件和本阶段新增但尚未提交的治理文件：

- 所有 Markdown
- 所有 README
- 所有 AGENTS / agent 文档
- `docs/`
- `reviews/`
- `issues/`
- `prototypes/`
- 所有 `design-spec/`
- 所有 HTML 文档
- 上述目录中的设计图片、图表和原型支持资产

扫描总数：**1404**

分类是基于当前路径、用途、当前基线和明确替代关系形成的第一阶段治理判断。
`待复核` 不能作为当前事实；`是（证据）` 和 `是（参考）` 表示文件仍有追溯价值，
但不拥有当前产品定义权。

## Summary

| Metric | Count |
| --- | ---: |
| Total | 1404 |
| Frozen | 344 |
| Review | 606 |
| Draft | 0 |
| Deprecated | 454 |
| Current authority | 18 |
| Historical evidence | 563 |
| Reference | 50 |
| Pending review | 319 |
| Not current | 454 |
| Exact or semantic duplicate candidates | 394 |

## Inventory

| 文件路径 | 文件用途 | 所属模块 | 当前状态 | 是否有效 | 是否重复 | 是否废弃 |
| --- | --- | --- | --- | --- | --- | --- |
| `.agents/skills/brandkit/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/design-taste-frontend-v1/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/design-taste-frontend/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/full-output-enforcement/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/gpt-taste/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/high-end-visual-design/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/image-to-code/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/imagegen-frontend-mobile/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/imagegen-frontend-web/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/industrial-brutalist-ui/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/minimalist-ui/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/redesign-existing-projects/SKILL.md` | 项目文档或参考资产 | Project | Review | 待复核 | 否 | 否 |
| `.agents/skills/stitch-design-taste/DESIGN.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.agents/skills/stitch-design-taste/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `.githooks/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |
| `.workbuddy/automations/automation-1783450520356/memory.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/automations/automation-1784564820520/memory.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-07.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-08.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-09.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-10.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-11.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-12.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-13.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-17.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-18.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-19.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-20.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-21.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/2026-07-22.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `.workbuddy/memory/MEMORY.md` | 项目文档或参考资产 | Memory | Deprecated | 否（当前） | Semantic:WORKBUDDY | 是 |
| `admin-platform/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |
| `AGENTS.md` | Agent 工作规则 | Task / Execution | Frozen | 是（当前） | 否 | 否 |
| `backend/app/agent_conversion/README.md` | 目录或项目入口 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/finance/finance-financial-analyst.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/finance/finance-tax-strategist.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/marketing/marketing-content-creator.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/marketing/marketing-growth-hacker.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/marketing/marketing-social-media-strategist.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/product/product-behavioral-nudge-engine.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/product/product-feedback-synth.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/product/product-trend-researcher.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/sales/sales-discovery-coach.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/sales/sales-pipeline-analyst.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/skill/code_review/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/skill/customer_support/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/skill/data_analysis/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/skill/doc_writing/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/skill/web_research/SKILL.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/support/support-legal-compliance-checker.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/app/agent_conversion/sources/support/support-support-responder.md` | 项目文档或参考资产 | Task / Execution | Review | 待复核 | 否 | 否 |
| `backend/docs/real_rd_local_run.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/00-VISION.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/01-MISSION.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/02-PRODUCT-PHILOSOPHY.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/03-CORE-CONCEPTS.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/04-DESIGN-PRINCIPLES.md` | 项目文档或参考资产 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/05-GLOSSARY.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/00-SYSTEM-ARCHITECTURE.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/01-DOMAIN-MODEL.md` | 项目文档或参考资产 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/02-CAPABILITY-ARCHITECTURE.md` | 项目文档或参考资产 | Capability | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/00-PRODUCT-MODULES.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/01-BUSINESS-PACKS.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/03-UX/00-INFORMATION-ARCHITECTURE.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/03-UX/01-USER-FLOWS.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/00-MVP-SCOPE.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/01-SPRINT-PLAN.md` | 项目文档或参考资产 | General | Deprecated | 否（当前） | 否 | 是 |
| `curis_workspace_blueprint/ADR/ADR-001-EMPLOYEE-BEFORE-MODEL.md` | 架构或产品决策 | Employee | Deprecated | 否（当前） | 否 | 是 |
| `curis_workspace_blueprint/ADR/ADR-002-CAPABILITY-PROVIDER-NOT-REBUILD.md` | 架构或产品决策 | Capability | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/README.md` | 目录或项目入口 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/curis_workspace_blueprint/RESEARCH/00-REFERENCE-PRODUCTS.md` | 项目文档或参考资产 | Research | Deprecated | 否（当前） | 否 | 是 |
| `data/sample_publish_package.md` | 项目文档或参考资产 | Artifact | Review | 待复核 | 否 | 否 |
| `deploy/aitoearn/debrand/README.md` | 目录或项目入口 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `deploy/aitoearn/README.md` | 目录或项目入口 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `deploy/curis/README.md` | 目录或项目入口 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `deploy/curis/release-checklist.md` | 项目文档或参考资产 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `deploy/freellmapi/README.md` | 目录或项目入口 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `deploy/social-auto-upload/README.md` | 目录或项目入口 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `diagrams/curis-architecture-diagrams.html` | 历史原型 | General | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/overview.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `docs/99_Archive/prototypes/diagrams/ui-aicost.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-capability.html` | 历史原型 | Capability | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-databi.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-department.html` | 历史原型 | Business Department | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-employee.html` | 历史原型 | Employee | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-finance.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-homepage-teal-v2.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-homepage-variants.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-knowledge.html` | 历史原型 | Knowledge | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-login.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-report.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-scope.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-settings.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `diagrams/ui-task-console.html` | 历史原型 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/prototypes/diagrams/ui-workflow.html` | 历史原型 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/00_Context/CURRENT_STATE.md` | 当前上下文与治理 | General | Frozen | 是（当前） | Semantic:CURRENT_STATE | 否 |
| `docs/00_Context/DOCUMENT_INVENTORY.md` | 当前上下文与治理 | General | Frozen | 是（当前） | 否 | 否 |
| `docs/00_Context/DOCUMENT_MIGRATION_PLAN.md` | 当前上下文与治理 | General | Review | 待复核 | 否 | 否 |
| `docs/00_Context/DOCUMENT_STATUS_RULES.md` | 当前上下文与治理 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/01_Product/Curis_Product_Context.md` | 产品领域唯一入口 | General | Frozen | 是（当前） | 否 | 否 |
| `docs/02_Architecture/Curis_System_Architecture.md` | 架构领域唯一入口 | General | Frozen | 是（当前） | 否 | 否 |
| `docs/03_Design/Curis_Design_System.md` | 设计领域唯一入口 | UI / Design System | Frozen | 是（当前） | 否 | 否 |
| `docs/04_Development/Curis_Development_Guide.md` | 开发领域唯一入口 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0033-global-assistant-runtime.md` | 架构或产品决策 | Assistant | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0034-main-baseline-restoration.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0035-desktop-first.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0036-workspace-admin-boundary.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0037-domain-frozen-entry-documents.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0038-status-only-historical-governance.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/07_Decisions/ADR-0039-phase3b1-workspace-blueprint-migration.md` | 架构或产品决策 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/08_Change_Log/CHANGE_LOG.md` | 变更记录 | General | Frozen | 是（当前） | 否 | 否 |
| `docs/99_Archive/README.md` | Archive 治理与查询入口 | Governance | Frozen | 是（当前） | 否 | 否 |
| `docs/adr-0024-class-diagram.mermaid` | 架构或产品决策 | Governance | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/adr-0024-sequence-diagram.mermaid` | 架构或产品决策 | Governance | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/ai-development-organization/agent-execution-loop.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/bootstrap-sequence.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/ceo-reporting-standard.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/collaboration-protocol.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/context-boundary-system.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/decision-authority-matrix.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/mvp-execution-loop.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/README.md` | 目录或项目入口 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/responsibility-matrix.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/roles.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/runtime-state-observer.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/sprint-gate-system.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/standard-task-template.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/system-feedback-loop.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/system-state-machine.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/task-execution-system.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/task-runtime-engine.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/team-structure.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/token-governance-layer.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/ai-development-organization/token-optimization-strategy.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/architecture/agent-execution-kernel-impl-plan.md` | 架构说明 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-decisionsink-class.mermaid` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-decisionsink-sequence.mermaid` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-decisionsink.md` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-impl-class.mermaid` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-impl-plan.md` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance-impl-sequence.mermaid` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/b-layer-runtime-governance.md` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/curis-assistant-architecture-review.md` | 架构说明 | Assistant | Deprecated | 否（当前） | 否 | 是 |
| `docs/architecture/curis-assistant-runtime-architecture-report.md` | 架构说明 | Assistant | Review | 待复核 | 否 | 否 |
| `docs/architecture/curis-backend-core-arch.md` | 架构说明 | General | Review | 待复核 | 否 | 否 |
| `docs/architecture/curis-class-diagram.mermaid` | 架构说明 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/architecture/curis-p1-adapters-arch.md` | 架构说明 | Capability | Review | 待复核 | 否 | 否 |
| `docs/architecture/curis-sequence-diagram.mermaid` | 架构说明 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/architecture/issue-b-ceo-runtime-evidence-impl-plan.md` | 架构说明 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/architecture/issue-c-budget-guard-impl-plan.md` | 架构说明 | Governance | Review | 待复核 | 否 | 否 |
| `docs/architecture/paperclip-conclusion-gap-analysis.md` | 架构说明 | Research | Review | 待复核 | 否 | 否 |
| `docs/architecture/paperclip-curis-mapping-report.md` | 架构说明 | Research | Review | 待复核 | 否 | 否 |
| `docs/architecture/redesign-v2-architecture-and-roadmap.md` | 架构说明 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/archive-commit-2026-07-17.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `docs/class-diagram.mermaid` | 架构或流程图 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/contracts/admin-capability-package-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/admin-plan-management-contract.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/admin-quota-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/admin-workspace-commercial-boundary.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/admin-workspace-template-boundary.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/ai-company-template-system.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/billing-domain-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/billing-rule-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/capability-package-commercial-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/capability-package-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/capability-type-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/ceo-dashboard-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/commercial-configuration-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/commercial-configuration-v1.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/commercial-data-flow.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-bootstrap-flow.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-operation-flow-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-package-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-package-runtime-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-runtime-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/company-template-contract.md` | API、数据或产品契约 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/contracts/customization-policy.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/dashboard-template-admin-contract.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/dashboard-template-catalog-v2.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/department-runtime-contract.md` | API、数据或产品契约 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/contracts/department-template-contract.md` | API、数据或产品契约 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/contracts/employee-lifecycle-contract.md` | API、数据或产品契约 | Employee | Review | 待复核 | 否 | 否 |
| `docs/contracts/employee-seat-commercial-contract.md` | API、数据或产品契约 | Employee | Review | 待复核 | 否 | 否 |
| `docs/contracts/employee-seat-contract.md` | API、数据或产品契约 | Employee | Review | 待复核 | 否 | 否 |
| `docs/contracts/employee-template-contract.md` | API、数据或产品契约 | Employee | Review | 待复核 | 否 | 否 |
| `docs/contracts/employee-template-instance-contract.md` | API、数据或产品契约 | Employee | Review | 待复核 | 否 | 否 |
| `docs/contracts/official-skill-catalog-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/pricing-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/pricing-package-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/pricing-rule-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/project-lifecycle-contract.md` | API、数据或产品契约 | Project | Review | 待复核 | 否 | 否 |
| `docs/contracts/project-runtime-contract.md` | API、数据或产品契约 | Project | Review | 待复核 | 否 | 否 |
| `docs/contracts/quota-rule-contract.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/skill-runtime-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/template-catalog-runtime-contract.md` | API、数据或产品契约 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `docs/contracts/template-instance-runtime-contract.md` | API、数据或产品契约 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `docs/contracts/template-versioning-policy.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/tool-runtime-contract.md` | API、数据或产品契约 | Capability | Review | 待复核 | 否 | 否 |
| `docs/contracts/usage-value-event-boundary.md` | API、数据或产品契约 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/contracts/value-event-contract.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/value-event-generation-flow.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/value-event-type-contract.md` | API、数据或产品契约 | General | Review | 待复核 | 否 | 否 |
| `docs/contracts/workflow-runtime-contract.md` | API、数据或产品契约 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/contracts/workflow-template-contract.md` | API、数据或产品契约 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/contracts/workflow-trigger-contract.md` | API、数据或产品契约 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0001-ai-development-organization.md` | 架构或产品决策 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md` | 架构或产品决策 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md` | 架构或产品决策 | Project | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md` | 架构或产品决策 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md` | 架构或产品决策 | Project | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0016-execution-substance-initiative.md` | 架构或产品决策 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0017-multitenant-department-catalog.md` | 架构或产品决策 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0018-sprint3-role-context-runtime-unblock.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0019-d1-runtime-role-wiring-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0020-d3-append-only-evolution-event-log-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0021-d2-evolution-governor-sandbox-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0022-d1-tenant-id-reservation-boundaries.md` | 架构或产品决策 | Identity / Security | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0023-d2-department-catalog-boundaries.md` | 架构或产品决策 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0024-d3-self-observability-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0025-d4-two-tier-governance-boundaries.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0026-d2-impl-department-instantiation.md` | 架构或产品决策 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0027-d-series-real-impl-roadmap.md` | 架构或产品决策 | Governance | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md` | 架构或产品决策 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md` | 架构或产品决策 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md` | 架构或产品决策 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md` | 架构或产品决策 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/decisions/commercial-operation-roadmap.md` | 架构或产品决策 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/decisions/commercial-package-model-v1.md` | 架构或产品决策 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/decisions/commercial-roadmap.md` | 架构或产品决策 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/demo/phase3-demo-script.md` | 历史 Demo 说明 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/demo/phase4-ai-employee-demo-script.md` | 历史 Demo 说明 | Employee | Deprecated | 否（当前） | 否 | 是 |
| `docs/demo/phase5-g2-credential-vault-demo-script.md` | 历史 Demo 说明 | Identity / Security | Deprecated | 否（当前） | 否 | 是 |
| `docs/demo/phase6-workflow-mvp-demo-script.md` | 历史 Demo 说明 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/demo/phase7-demo-seed.json` | 历史 Demo 说明 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/demo/phase7-stable-demo-script.md` | 历史 Demo 说明 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/deployment/new-api-local.md` | 项目文档或参考资产 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `docs/design/ceo-dashboard-product-definition.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/design/p1-adapters/class-diagram.mermaid` | UI 或 Design System 规范 | Capability | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/p1-adapters/sequence-diagram.mermaid` | UI 或 Design System 规范 | Capability | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/p1-adapters/system_design.md` | 架构说明 | Capability | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/phase1c-ceo-office-ui-design.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/design/phase1c-ceo-office-ui-redesign.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/design/phase1c-ceo-office-ui-v3.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/design/phase8-billing-mvp-design.md` | UI 或 Design System 规范 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/design/phase9a-p0-pricing-implementation-design.md` | UI 或 Design System 规范 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/design/phase9a-p1-quota-implementation-design.md` | UI 或 Design System 规范 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/design/phase9a-p2-cappkg-implementation-design.md` | UI 或 Design System 规范 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/design/phase9a-plan-config-adjust-design.md` | UI 或 Design System 规范 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/design/real-rd-executor/class-diagram.mermaid` | UI 或 Design System 规范 | UI / Design System | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/real-rd-executor/sequence-diagram.mermaid` | UI 或 Design System 规范 | UI / Design System | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/real-rd-executor/system_design.md` | 架构说明 | UI / Design System | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/design/workspace-employee-directory.md` | UI 或 Design System 规范 | Employee | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase2_Report.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3A_Report.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3B1_Migration_Report.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3B2_Asset_Report.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3B2_Migration_Plan.md` | 文档治理迁移计划 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3C1_Archive_Migration_Report.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3C2_Asset_Review.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Phase3C3_Delete_Review.md` | 文档治理阶段报告 | Governance | Review | 待复核 | 否 | 否 |
| `docs/Documentation_Governance_Final_Report.md` | 文档治理最终报告 | Governance | Frozen | 是（证据） | 否 | 否 |
| `docs/Documentation_Governance_Report.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/99_Archive/handoff/2026_07_23CURIS_PRODUCT_DELIVERY_HANDOFF.md` | 历史交接 | Governance | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/handoff/curis-roadmap-r1r2-handoff-2026-07-22.md` | 历史交接 | Governance | Deprecated | 否（当前） | 否 | 是 |
| `docs/merge_checklist.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-asset-completion-standard.md` | 历史或待审计划 | Governance | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-asset-factory-product-review.md` | 历史或待审计划 | Governance | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-asset-remediation-design.md` | 历史或待审计划 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-workspace-collaboration-discipline.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-workspace-deployment-isolation-2026-07-17.md` | 历史或待审计划 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `docs/plan/admin-workspace-isolation-preflight-2026-07-17.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/agent-conversion-multisource-class-diagram.mermaid` | 历史或待审计划 | Task / Execution | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/agent-conversion-multisource-design.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/agent-conversion-multisource-prd.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/agent-conversion-multisource-sequence-diagram.mermaid` | 历史或待审计划 | Task / Execution | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/agent-conversion-pilot-b-design.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/agent-conversion-pilot-b-prd.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/agent-conversion-pilot-b-review.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/ai-company-asset-factory-v2-roadmap-review.md` | 历史或待审计划 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/plan/commercial-config-cmcf-proposal.md` | 历史或待审计划 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/plan/company-package-official-content-plan.md` | 历史或待审计划 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/plan/content-department-phase1-dev-spec.md` | 历史或待审计划 | Business Department | Review | 待复核 | 否 | 否 |
| `docs/plan/curis-roadmap-execution.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/dashboard-official-content-plan.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/employee-persona-system-plan.md` | 历史或待审计划 | Employee | Review | 待复核 | 否 | 否 |
| `docs/plan/gate-b-directory-folding-unification.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/p1-1-security-col-design.md` | 历史或待审计划 | Identity / Security | Review | 待复核 | 否 | 否 |
| `docs/plan/phase1-impl-class-diagram.mermaid` | 历史或待审计划 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/phase1-impl-design-gate-cdef.md` | 历史或待审计划 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/plan/phase1-impl-sequence-diagram.mermaid` | 历史或待审计划 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/pilot-b-class-diagram.mermaid` | 历史或待审计划 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/pilot-b-sequence-diagram.mermaid` | 历史或待审计划 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/plan/real-rd-toolset-spec.md` | 历史或待审计划 | Capability | Review | 待复核 | 否 | 否 |
| `docs/plan/tool-catalog-official-plan.md` | 历史或待审计划 | Capability | Review | 待复核 | 否 | 否 |
| `docs/plan/v1-selfuse-architecture.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/v1-selfuse-content-dataflow.mermaid` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/v1-selfuse-content-execution.mermaid` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/plan/v2-p0p1-architect-brief.md` | 历史或待审计划 | General | Review | 待复核 | 否 | 否 |
| `docs/plan/v2-p0p1-architect-review.md` | 历史或待审计划 | Governance | Review | 待复核 | 否 | 否 |
| `docs/plan/v2-p0p1-impl-design.md` | 历史或待审计划 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/plan/workflow-official-content-plan.md` | 历史或待审计划 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/pmo/20260719_quota_handoff_plan.md` | 历史交接 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/pmo/archive/PROJECT_STATUS_HISTORY_2026-07-12.md` | 协作与交付治理 | Project | Deprecated | 否（当前） | 否 | 是 |
| `docs/pmo/archive/TASKS_HISTORY_2026-07-12.md` | 协作与交付治理 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/pmo/current-status.md` | 协作与交付治理 | Governance | Deprecated | 否（当前） | Semantic:CURRENT_STATE | 是 |
| `docs/pmo/low-token-workflow-v2.md` | 协作与交付治理 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/pmo/source-control-baseline-freeze.md` | 协作与交付治理 | Governance | Review | 待复核 | 否 | 否 |
| `docs/pmo/workflow.md` | 协作与交付治理 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/prd/workspace-employee-directory.md` | 产品定义或 PRD | Employee | Review | 待复核 | 否 | 否 |
| `docs/product-development-spec.md` | 项目文档或参考资产 | General | Review | 待复核 | Semantic:PRODUCT_BASELINE | 否 |
| `docs/product-governance-principle.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/product/2026-07-23_Curis_产品架构图更新说明.md` | 产品定义或 PRD | General | Review | 待复核 | 否 | 否 |
| `docs/product/adr0028_phase1_shared_contract_handoff.md` | 历史交接 | Governance | Review | 待复核 | 否 | 否 |
| `docs/product/ai-content-publish-package.md` | 产品定义或 PRD | Artifact | Review | 待复核 | 否 | 否 |
| `docs/product/CURIS_PRODUCT_BASELINE.md` | 产品定义或 PRD | General | Review | 待复核 | Semantic:PRODUCT_BASELINE | 否 |
| `docs/product/curis-product-vision-current-stage.md` | 产品定义或 PRD | General | Deprecated | 否（当前） | Semantic:PRODUCT_BASELINE | 是 |
| `docs/product/federated-agent-os.md` | 产品定义或 PRD | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/product/org-center-real-frontend-prd.md` | 产品定义或 PRD | Business Department | Review | 待复核 | 否 | 否 |
| `docs/product/prd.md` | 产品定义或 PRD | General | Review | 待复核 | Semantic:PRODUCT_BASELINE | 否 |
| `docs/product/ui-r4-stitch/00_scope_and_non_goals.md` | 产品定义或 PRD | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/project-space-confirmation-2026-07-17.md` | 项目文档或参考资产 | Project | Review | 待复核 | 否 | 否 |
| `docs/prototypes/curis-full-system-high-fidelity-prototype.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/r1r2_release_notes.md` | 项目文档或参考资产 | Runtime / Deployment | Review | 待复核 | 否 | 否 |
| `docs/release/admin-ai-company-asset-foundation.md` | 历史发布记录 | Company / CEO Office | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/ai-task-executor-mvp-v0.1-release-record.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/ai-task-executor-mvp-v0.1.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/model-gateway-local-demo-first-version-release-record.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/model-gateway-local-demo-rc.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase1-company-runtime-foundation-report.md` | 历史发布记录 | Company / CEO Office | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase1a-company-project-runtime-backend.md` | 历史发布记录 | Project | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase1b-gate-assessment.md` | 历史发布记录 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase1b-template-runtime-integration-gate.md` | 历史发布记录 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase3-demo-freeze-report.md` | 历史发布记录 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase3-workspace-self-extension-rc.md` | 历史发布记录 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase4-ai-employee-demo-freeze-report.md` | 历史发布记录 | Employee | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase4-ai-employee-system-rc.md` | 历史发布记录 | Employee | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase45-workspace-demo-review-roadmap.md` | 历史发布记录 | Governance | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase5-g2-credential-vault-demo-freeze-report.md` | 历史发布记录 | Identity / Security | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase5-g2-credential-vault-implementation-report.md` | 历史发布记录 | Identity / Security | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase5-g2-credential-vault-rc.md` | 历史发布记录 | Identity / Security | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase55-post-g2-roadmap-review.md` | 历史发布记录 | Governance | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase6-workflow-mvp-demo-freeze-report.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase6-workflow-mvp-implementation-report.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase6-workflow-mvp-rc.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase65-post-workflow-roadmap-review.md` | 历史发布记录 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase7-demo-polish-commercial-readiness.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase75-commercial-validation-value-event-design.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase75-value-event-validation-report.md` | 历史发布记录 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase8-workspace-billing-support-implementation-report.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase9a-commercial-configuration-status.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/release/phase9a-commercial-design-freeze.md` | 历史发布记录 | Model / Usage | Deprecated | 否（当前） | 否 | 是 |
| `docs/research/agent-conversion-engine-v1-design.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/agent-conversion-engine-v1-plan.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/agent-conversion-engine-v1-report.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/agent-conversion-multisource-qa.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/agent-conversion-multisource-research.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/aiearn-asset-mapping.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/aiearn-content-marketing-final-decision.md` | 研究与参考 | Governance | Frozen | 是（参考） | 否 | 否 |
| `docs/research/aiearn-content-marketing-reuse-plan.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/aitoearn-reuse-research.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/autoagents.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/chatdev.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/coze.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/crewai-examples.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/crewai.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/dify.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/gpts.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/litellm.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/make.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/metagpt.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/new-api.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/one-api.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/openclaw-agents.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/paperclip-companies.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/paperclip.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/taskade.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/competitors/zapier.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/decisions/adopted-patterns.md` | 研究与参考 | Governance | Frozen | 是（参考） | 否 | 否 |
| `docs/research/decisions/phase4-issue-suggestions.md` | 研究与参考 | Governance | Frozen | 是（参考） | 否 | 否 |
| `docs/research/decisions/rejected-patterns.md` | 研究与参考 | Governance | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/admin-governance-research.md` | 研究与参考 | Governance | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/admin-support-aicos-roadmap.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/ai-company-template-research.md` | 研究与参考 | Company / CEO Office | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/billing-readiness-assessment.md` | 研究与参考 | Model / Usage | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/capability-catalog-research.md` | 研究与参考 | Capability | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/capability-marketplace-research.md` | 研究与参考 | Capability | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/curis-packaging-research.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/department-template-research.md` | 研究与参考 | Business Department | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/employee-template-research.md` | 研究与参考 | Employee | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/model-gateway-research.md` | 研究与参考 | Model / Usage | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/official-skill-catalog-v1.md` | 研究与参考 | Capability | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/official-tool-catalog-v1.md` | 研究与参考 | Capability | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/pricing-model-research.md` | 研究与参考 | Model / Usage | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/software-dev-sop-research.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/usage-billing-research.md` | 研究与参考 | Model / Usage | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/value-measurement-research.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/workflow-engine-research.md` | 研究与参考 | Task / Execution | Frozen | 是（参考） | 否 | 否 |
| `docs/research/domain/workspace-commercial-readiness.md` | 研究与参考 | Model / Usage | Frozen | 是（参考） | 否 | 否 |
| `docs/research/employee-template-research.md` | 研究与参考 | Employee | Frozen | 是（参考） | 否 | 否 |
| `docs/research/platform-api-qualification-tracker.md` | 研究与参考 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/research/README.md` | 目录或项目入口 | Research | Frozen | 是（参考） | 否 | 否 |
| `docs/review/2026-07-17_admin-asset-real-status-review.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/review/2026-07-17_WorkBuddy_Admin跨团队协作与当前开发规则.md` | 项目文档或参考资产 | Governance | Review | 待复核 | Semantic:WORKBUDDY | 否 |
| `docs/review/2026-07-17_workspace-real-status-review.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/review/2026-07-18_curis-joint-progress-review.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/review/dashboard-data-readiness.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/review/employee-default-skill-mapping.md` | 项目文档或参考资产 | Employee | Review | 待复核 | 否 | 否 |
| `docs/review/phase1-ai-rnd-company-mvp-gap-list.md` | 项目文档或参考资产 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `docs/review/phase86-admin-commercial-hardcode-audit.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/review/phase86-workspace-commercial-audit.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/review/phase9a-capability-meter-review.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `docs/review/phase9a-commercial-boundary-check.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/review/phase9a-employee-seat-meter-review.md` | 项目文档或参考资产 | Employee | Review | 待复核 | 否 | 否 |
| `docs/review/phase9a-workspace-commercial-hardcode-check.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `docs/sequence-diagram.mermaid` | 架构或流程图 | General | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/sprints/ai-task-executor-mvp-readiness.md` | 历史 Sprint 计划 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/ai-task-executor-mvp-release-candidate.md` | 历史 Sprint 计划 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/mvp-implementation.md` | 历史 Sprint 计划 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/post-v0.1-execution-reliability.md` | 历史 Sprint 计划 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-0-organization-review.md` | 历史 Sprint 计划 | Business Department | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-1-company-visualization.md` | 历史 Sprint 计划 | Company / CEO Office | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-2-project-memory-foundation.md` | 历史 Sprint 计划 | Project | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-2-unified-task-console.md` | 历史 Sprint 计划 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-3-lightweight-role-responsibility.md` | 历史 Sprint 计划 | General | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-3-role-context-runtime-reference.md` | 历史 Sprint 计划 | Runtime / Deployment | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-4-multi-entry-advanced-ui.md` | 历史 Sprint 计划 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/sprint-workflow.md` | 历史 Sprint 计划 | Task / Execution | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/tool-system-v1.6-meta-development.md` | 历史 Sprint 计划 | Capability | Deprecated | 否（当前） | 否 | 是 |
| `docs/sprints/tool-system-v1.8-controlled-self-evolution.md` | 历史 Sprint 计划 | Capability | Deprecated | 否（当前） | 否 | 是 |
| `docs/standards/coding-standard.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/standards/directory-structure.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/standards/documentation-standard.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `docs/status/USER_CAPABILITY_LEDGER.md` | 项目文档或参考资产 | Capability | Review | 待复核 | 否 | 否 |
| `docs/superpowers/plans/2026-07-10-curis-obsidian-knowledge-base.md` | 项目文档或参考资产 | Knowledge | Review | 待复核 | 否 | 否 |
| `docs/superpowers/plans/2026-07-10-curis-obsidian-visual-system.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `docs/superpowers/specs/2026-07-10-curis-obsidian-knowledge-base-design.md` | 项目文档或参考资产 | Knowledge | Review | 待复核 | 否 | 否 |
| `docs/superpowers/specs/2026-07-10-curis-obsidian-visual-system-design.md` | 项目文档或参考资产 | UI / Design System | Review | 待复核 | 否 | 否 |
| `docs/system_design.md` | 架构说明 | UI / Design System | Review | 待复核 | Semantic:ARCHITECTURE | 否 |
| `docs/99_Archive/handoff/team-v2/BOOTSTRAP_HANDOFFS.md` | 历史交接 | Governance | Review | 待复核 | 否 | 否 |
| `docs/team-v2/CONTEXT_RULES.md` | 协作与交付治理 | Governance | Review | 待复核 | 否 | 否 |
| `docs/99_Archive/handoff/team-v2/HANDOFF_TEMPLATE.md` | 历史交接 | Governance | Review | 待复核 | 否 | 否 |
| `docs/team-v2/LEGACY_RULES_AUDIT.md` | 协作与交付治理 | Governance | Review | 待复核 | 否 | 否 |
| `docs/team-v2/TEAM_ROLES.md` | 协作与交付治理 | Governance | Review | 待复核 | 否 | 否 |
| `docs/team-v2/WORKFLOW.md` | 协作与交付治理 | Task / Execution | Review | 待复核 | 否 | 否 |
| `docs/team/conversations/CONV-SEAT-GATE-001.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/conversations/CONV-SEAT-PRODUCT-001.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/conversations/CONV-SEAT-QUALITY-001.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/conversations/CONV-SEAT-SECURITY-001.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/conversations/CONV-SEAT-SYSTEM-001.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/gate-decision-seat-role.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/product-planning-seat-role.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/quality-runtime-seat-role.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/SEAT_OVERVIEW.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/security-boundary-seat-role.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `docs/team/system-delivery-seat-role.md` | 协作与交付治理 | Employee | Review | 待复核 | 否 | 否 |
| `experimental/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |
| `frontend/ceo-evidence/index.html` | 历史原型 | Company / CEO Office | Deprecated | 否（当前） | 否 | 是 |
| `docs/99_Archive/design/ceo-office/_archive/capability-center-compact-v6.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v2.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v3.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v4.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v5.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v6.devmode.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact-v6.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home-compact.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.devmode.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/ceo-office-home.terra.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/org-center-compact-v6.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/org-center.terra.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/org-spatial-3d.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/outcome-center-compact-v6.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/_archive/project-center-compact-v6.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/analytics-sample.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/brainstorm-sample.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/capability-center-sample.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/ceo-home-sample.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/department-detail-sample.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/execution-sample.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/knowledge-sample.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/org-center-sample.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/project-center-sample.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/project-detail-sample.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/report-detail-sample.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/skill-detail-sample.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/_samples/task-detail-sample.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/项目中心与组织中心职能划分.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/analytics-org.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/analytics-project.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/analytics-workflow.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/analytics.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/brainstorm-active.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/brainstorm-result-detail.html` | 交互或视觉原型 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/brainstorm-results.html` | 交互或视觉原型 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/brainstorm-session-detail.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/brainstorm.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-agent-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-center.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-model-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-skill-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-tool-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/capability-workflow-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/ceo-home.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/company-runtime.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/decision-center.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/department-detail.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/DESIGN.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/employee-detail.html` | 交互或视觉原型 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/execution-runs.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/execution-tasks.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/execution.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/ceo-office/handoff/capability-center/capability-center.devmode.md` | UI 或 Design System 规范 | Capability | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/handoff/capability-center/capability-center.hifi.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/knowledge-company.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/knowledge-dept.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/knowledge-entry-detail.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/knowledge-project.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/knowledge.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/org-center.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/org-dept.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/org-employees.html` | 交互或视觉原型 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/project-center.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/project-dept.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/project-detail.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/report-detail.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/reports.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/run-detail.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/settings-brand.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/settings-notify.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/settings-profile.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/settings.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/skill-detail.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/strategy-room.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/task-detail.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/ceo-office/TRAE_vs_UI_Designer_对比.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/Trae对齐指令_整合版.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/Trae交互设计问题检查.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/Trae缺失页面清单_由Trae补齐.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/design-spec/ceo-office/UI_设计与布局规范.md` | UI 或 Design System 规范 | Company / CEO Office | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `docs/99_Archive/design/curis-ui-v2/.preflight/preflight.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.css` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.js` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.css` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.js` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/project-dept-ia.js` | 设计原型支持资产 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.css` | 设计原型支持资产 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.js` | 设计原型支持资产 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/01-ceo-home-1440-viewport.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-capability-center-1440.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-org-center-1440.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-project-center-1440.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-1440.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-390.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-1440.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-390.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/ceo-home-390.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/audit-evidence/company-runtime-1440.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/audit-evidence/employee-detail-1440.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/audit-evidence/execution-1440.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-1440.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-390.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-1440.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-390.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/audit-evidence/settings-1440.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/colors_and_type.css` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/Curis_TRAE_UI_交互产品架构审计报告.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/Curis_TRAE_UI_全站交互审计与IA重构方案_2026-07-27.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/curis-ceo-office.design` | UI 或 Design System 规范 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-state-catalog.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-completion-matrix.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-data-map.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-handoff.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-secondary-page-contracts.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-org.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics-workflow.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/analytics.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-active.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-results.png` | 设计导出图片 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm-session-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/brainstorm.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-agent-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-center.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-model-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-skill-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-tool-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/capability-workflow-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/ceo-home.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/company-runtime.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/decision-center.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/department-create.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/department-detail.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/employee-create.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/employee-detail.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution-runs.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution-tasks.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/execution.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-company.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-dept.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-entry-detail.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/knowledge.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-center.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-dept.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/org-employees.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-center.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-dept.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-detail.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G001 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G002 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/report-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/reports.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/run-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-brand.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-notify.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings-profile.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/settings.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/skill-detail.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/strategy-room.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/task-detail.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-org.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics-workflow.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/analytics.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-active.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-results.png` | 设计导出图片 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm-session-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/brainstorm.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-agent-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-center.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-model-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-skill-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-tool-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/capability-workflow-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/ceo-home.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/company-runtime.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/decision-center.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/department-create.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/department-detail.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/employee-create.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/employee-detail.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution-runs.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution-tasks.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/execution.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-company.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-dept.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-entry-detail.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/knowledge.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-center.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-dept.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/org-employees.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-center.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-dept.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-detail.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G003 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G004 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/report-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/reports.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/run-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-brand.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-notify.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings-profile.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/settings.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/skill-detail.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/strategy-room.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/task-detail.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-org.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics-workflow.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/analytics.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-active.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-results.png` | 设计导出图片 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm-session-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/brainstorm.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-agent-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-center.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-model-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-skill-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-tool-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/capability-workflow-list.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/ceo-home.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/company-runtime.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/decision-center.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/department-create.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/department-detail.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/employee-create.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/employee-detail.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution-runs.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution-tasks.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/execution.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-company.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-dept.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-entry-detail.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge-project.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/knowledge.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-center.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-dept.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/org-employees.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-center.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-dept.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-detail.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G005 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-xhs.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Exact:G006 | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/report-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/reports.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/run-detail.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-brand.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-notify.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings-profile.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/settings.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/skill-detail.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/strategy-room.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/task-detail.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/manifest.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/analytics-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/brainstorm-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/capability-center-default.png` | 设计导出图片 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/ceo-home-default.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/company-runtime-default.png` | 设计导出图片 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.all-pages.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.frames.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.interactions.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.tokens.json` | 设计原型支持资产 | Model / Usage | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/decision-center-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/department-create-default.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/employee-create-default.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/execution-default.png` | 设计导出图片 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/knowledge-default.png` | 设计导出图片 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/org-center-default.png` | 设计导出图片 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/org-employees-default.png` | 设计导出图片 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-center-default.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-dept-default.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-miniapp-default.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/project-xhs-default.png` | 设计导出图片 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/README.md` | 目录或项目入口 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/reports-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/settings-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/figma/strategy-room-default.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/docs/ui/index.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/LOCAL_HANDOFF.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-1024.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-1440.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/catalog-390.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-1024.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-1440.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/docs/ui/states/index-390.png` | 设计导出图片 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/fix-cap-links.mjs` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/fix-placeholders-v3.js` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-org.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-project.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/analytics-workflow.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/analytics.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-active.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-results.html` | 交互或视觉原型 | Artifact | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-session-detail.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-agent-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-center.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-model-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-skill-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-tool-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/capability-workflow-list.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/ceo-home.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/company-runtime.html` | 交互或视觉原型 | Company / CEO Office | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/decision-center.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/department-create.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/department-detail.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/employee-create.html` | 交互或视觉原型 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/employee-detail.html` | 交互或视觉原型 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/execution-runs.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/execution-tasks.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/execution.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-company.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-dept.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-entry-detail.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-project.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/knowledge.html` | 交互或视觉原型 | Knowledge | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/org-center.html` | 交互或视觉原型 | Business Department | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/org-dept.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/org-employees.html` | 交互或视觉原型 | Employee | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/project-center.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/project-dept.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/project-detail.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/project-miniapp-detail.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/project-xhs-workflow-detail.html` | 交互或视觉原型 | Project | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/report-detail.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/reports.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/run-detail.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/settings-brand.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/settings-notify.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/settings-profile.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/settings.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/skill-detail.html` | 交互或视觉原型 | Capability | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/strategy-room.html` | 交互或视觉原型 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/pages/task-detail.html` | 交互或视觉原型 | Task / Execution | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/runtime-orchestration-summary.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/curis-ui-v2/SPEC.md` | UI 或 Design System 规范 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `docs/99_Archive/design/curis-ui-v2/validation-report.json` | 设计原型支持资产 | UI / Design System | Deprecated | 否（当前） | Semantic:UI_VARIANTS | 是 |
| `frontend/design-spec/UI规范交付模板.md` | UI 或 Design System 规范 | UI / Design System | Review | 待复核 | Semantic:UI_VARIANTS | 否 |
| `frontend/docs/ceo-ui-v2-class.mermaid` | 架构或流程图 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `frontend/docs/ceo-ui-v2-sequence.mermaid` | 架构或流程图 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `frontend/docs/ceo-ui-v2-system-design.md` | 项目文档或参考资产 | Company / CEO Office | Review | 待复核 | 否 | 否 |
| `issues/001_sprint_0_acceptance.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/002_tool_system_v1_6_meta_development.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/003_tool_system_v1_8_controlled_self_evolution.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/004_sprint_1_company_visualization_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/005_sprint_1_architecture_boundaries.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/006_sprint_1_visualization_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/007_sprint_1_ceo_readable_visualization_polish.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/008_sprint_2_unified_task_console_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/009_sprint_2_unified_task_console_first_slice.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/010_sprint_2_project_memory_foundation_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/011_sprint_2_project_memory_first_slice.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/012_sprint_3_lightweight_role_responsibility_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/013_sprint_3_role_profiles_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/014_sprint_3_role_context_runtime_reference_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/015_sprint_3_role_context_runtime_reference_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/016_sprint_3_closeout_sprint_4_entry_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/017_sprint_4_multi_entry_ui_first_slice.md` | Issue 范围与验收 | UI / Design System | Review | 是（证据） | 否 | 否 |
| `issues/018_sprint_4_closeout_mvp_readiness_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/019_ai_task_executor_mvp_readiness_review.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/020_chinese_operation_console_localization.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/021_ai_task_executor_mvp_release_candidate_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/023_ai_task_executor_mvp_local_demo_release_verification.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/024_ai_task_executor_mvp_v0_1_release_closeout.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/025_post_v0_1_execution_reliability_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/026_post_v0_1_execution_reliability_boundaries.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/027_run_evidence_reliability_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/028_workflow_error_fallback_observability_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/029_workflow_error_fallback_observability_boundaries.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/030_workflow_error_fallback_evidence_map.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/031_evolution_decision_evidence_reliability_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/032_evolution_decision_evidence_reliability_boundaries.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/033_evolution_decision_evidence_map.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/034_post_v0_1_execution_reliability_closeout_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/035_local_demo_operator_polish_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/036_local_demo_operator_polish_boundaries.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/037_local_demo_operator_release_notes_package.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/038_local_demo_verification_automation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/039_local_demo_verification_automation_boundaries.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/040_local_demo_api_smoke_helper.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/041_project_memory_execution_summary_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/042_project_memory_execution_summary_boundaries.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/043_project_memory_execution_summary.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/044_execution_substance_phase_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/045_runtime_role_wiring_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/046_evolution_governor_sandbox_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/047_append_only_evolution_log_first_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/048_adr0016_gate_submission_package.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/049_adr0017_future_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/050_adr0017_future_gate_submission_package.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/051_adr0017_d1_tenant_id_reservation.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/052_adr0017_d2_department_catalog.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/054_adr0017_d3_self_observability.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/055_adr0017_d4_two_tier_governance.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/056_adr0017_d2_impl_department_instantiation.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/057_adr0017_d1_impl_multitenant_isolation.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/058_adr0017_d3_impl_self_observability.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/059_adr0017_d4_impl_two_tier_governance.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/060_adr0017_d4_platform_management_console.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/062_adr0028_phase1_shared_contract.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/063_adr0028_phase2_admin_platform_mvp_prd.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/064_adr0028_phase2_newapi_gateway_prd.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/064_workspace_capability_integration_phase_1.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/065_adr0028_phase2_newapi_gateway_class.mermaid` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/065_adr0028_phase2_newapi_gateway_design.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/065_adr0028_phase2_newapi_gateway_sequence.mermaid` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/065_workspace_model_gateway_adapter.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/066_workspace_official_model_catalog.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/067_workspace_official_tool_catalog.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/068_new_api_local_deployment.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/069_model_gateway_production_security_boundary.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/070_adr0028_phase2_official_capability_catalog_prd.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/070_model_gateway_runtime_secret_guardrails.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/071_adr0028_phase2_official_capability_catalog_class.mermaid` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/071_adr0028_phase2_official_capability_catalog_design.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/071_adr0028_phase2_official_capability_catalog_sequence.mermaid` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/071_workspace_tenant_model_preference_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/072_workspace_tenant_model_preference_first_slice.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/073_workspace_model_preference_ui_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/074_workspace_model_preference_local_e2e_evidence.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/075_model_gateway_local_demo_release_candidate_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/076_model_gateway_post_rc_next_phase_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/077_post_first_version_workspace_company_foundation_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/078_workspace_company_foundation_first_slice_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/079_workspace_company_foundation_local_demo_evidence_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/080_workspace_company_department_catalog_summary_gate.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/081_workspace_department_catalog_local_demo_evidence_gate.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/082_workspace_department_activation_boundary_gate.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/083_workspace_department_activation_first_slice.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/084_workspace_department_activation_ui_gate.md` | Issue 范围与验收 | Business Department | Review | 是（证据） | 否 | 否 |
| `issues/085_workspace_admin_contract_integration_completion.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/086_workspace_self_extension_mvp.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/087_phase35_admin_contract_review_employee_department_templates.md` | Issue 范围与验收 | Employee | Review | 是（证据） | 否 | 否 |
| `issues/088_admin_workspace_frontend_split.md` | Issue 范围与验收 | UI / Design System | Review | 是（证据） | 否 | 否 |
| `issues/089_backend_process_db_isolation.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/090_independent_build_release_rollback.md` | Issue 范围与验收 | UI / Design System | Review | 是（证据） | 否 | 否 |
| `issues/091_admin_asset_dangling_fix.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/092_admin_orphan_instances_cleanup.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/093_admin_readonly_catalog_routes.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/094_admin_asset_completion_standard.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/095_admin_l2_gate_tracking.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_pr2_post_merge_scope_governance_closeout.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r1_unified_runtime_baseline.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r2_asset_instantiation_closure.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_artifact_project_status_closure.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_ceo_mapping_migration_input_l2_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_real_model_execution_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_remaining_role_employee_binding_set_l2_gate.md` | Issue 范围与验收 | Employee | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_remaining_workflow_completion_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r3_workflow_context_budget_l2_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260717_workspace_tenant_identity_membership_implementation.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_company_package_provenance_isolated_setup.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_company_package_provenance_real_execution_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_company_package_r3_provenance_closure_gate.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_container_exit1_static_diagnostic.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_d1_e2e_gateway_startup_diagnostic.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_d1_entry_owner_role_claim_fix.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_d1_selfuse_trusted_identity_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_d1_selfuse_trusted_provisioning.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_d1_single_model_toolchain_entry_gate.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_gateway_startup_evidence_preservation_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_minimal_rd_toolset_implementation.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_package_workflow_bridge_revocation_failclosed_fix.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_agent_mode_failclosed_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_agent_mode_profile_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_backend_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_closeout_gate_8c_rollout_queue.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_closeout_gate_8c1_8a_8b_review_rollup_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_closeout_gate_8c2_release_precondition_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_closeout_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b_rollout_queue.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_failure_blocking_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_response_contract_alignment_decision.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b3_minimal_logging_visibility_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_risk_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a_rollout_queue.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_refusal_status_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_relation_contract_fix_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_field_contract_fix_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3c_no_execute_side_effect_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_ai_secretary_scope_gate.md` | Issue 范围与验收 | Assistant | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_auto_progress_advance_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_auto_progress_recovery_takeover_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_auto_progress_timeout_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_validation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_codex_workbuddy_team_migration_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | Semantic:WORKBUDDY | 否 |
| `issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_hybrid_mode_profile_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_items_1_7_code_construction_audit_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_manual_risk_escalation_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_manual_stop_boundary_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_mode_contract_validation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_multi_project_session_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_multi_project_session_recovery_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_multi_project_session_scope_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_memory_recovery_path_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_state_fact_source_a1_mapping_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_state_fact_source_a2_tenant_scope_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_project_state_fact_source_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_closeout_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_rollout_queue.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate_9a_rollup_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md` | Issue 范围与验收 | Artifact | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_scope_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b_rollup_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_snapshot_fix_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_failure_check_matrix_fix_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate.md` | Issue 范围与验收 | Artifact | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_team_migration_transfer_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md` | Issue 范围与验收 | Artifact | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_artifact_output_closeout_gate.md` | Issue 范围与验收 | Artifact | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_artifact_output_contract_gate.md` | Issue 范围与验收 | Artifact | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_token_cost_budget_closeout_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_token_cost_budget_projection_failclosed_fix_gate.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_unified_token_cost_budget_visibility_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_workflow_mode_entry_guard_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_workflow_mode_profile_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_r4_workflow_mode_sequence_contract_gate.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_real_rd_tool_closure_prerequisite_gate.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_real_rd_tool_e2e_candidate_selection.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260718_workspace_selfuse_official_workflow_bridge_compatibility_fix.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/20260719_d1_execute_full_loop_proposal.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_d1_toolchain_unfreeze_implement.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260719_d1_toolchain_unfreeze_proposal.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_admin_warning_suppression_minimal_fix.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_create_app_failed_d1_toolchain_minimal_fix.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_pinned_online_build_postbuild_sentinel.md` | Issue 范围与验收 | UI / Design System | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_entry_wrapper_minimal_implementation.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_failure_deterministic_evidence_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_failure_signal_contract_fix.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_failure_signal_controlled_revert.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_failure_single_sentinel_diagnostic.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_signal_coverage_gap_decision.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_signal_exception_type_enrichment.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260719_workspace_startup_stage_signal_minimal_implementation.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260720_b_layer_test_local_rd_toolset_isolation_debt.md` | Issue 范围与验收 | Capability | Review | 是（证据） | 否 | 否 |
| `issues/20260720_d1_execute_a_implement.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260720_d1_execute_b_implement.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260722_google_oidc_owner_pre_authorization.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/20260722_google_oidc_project_runtime_vertical_slice.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260722_local_project_runtime_target_provisioning.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260722_macos_keychain_google_oidc_project_runtime.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260722_project_runtime_page.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260722_real_rd_container_runtime_prerequisite.md` | Issue 范围与验收 | UI / Design System | Review | 是（证据） | 否 | 否 |
| `issues/20260722_real_rd_persistent_run_usage_audit_evidence.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/20260722_real_rd_single_call_evidence_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260722_trusted_development_identity_source.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260722_workspace_product_flow_first_vertical_slice.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/20260723_project_owner_workbench_product_flow.md` | Issue 范围与验收 | Project | Review | 是（证据） | 否 | 否 |
| `issues/20260729_ai_call_usage_ledger_foundation.md` | Issue 范围与验收 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_business_department_org_model.md` | Issue 范围与验收 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_freellmapi_owner_only_experimental_gateway.md` | Issue 范围与验收 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_p0_authentication_onboarding.md` | Issue 范围与验收 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_p0_local_desktop_owner.md` | Issue 范围与验收 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase1_s1_app_shell_design_system.md` | Issue 范围与验收 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase1_s2_workspace_model.md` | Issue 范围与验收 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase2_s3_ai_employee.md` | Issue 范围与验收 | Employee | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase3_s4_project.md` | Issue 范围与验收 | Project | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase3_s5_task_execution.md` | Issue 范围与验收 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase4_s6_capability_registry.md` | Issue 范围与验收 | Capability | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase4_s7_model_gateway.md` | Issue 范围与验收 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase5_s10_knowledge_management.md` | Issue 范围与验收 | Knowledge | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase5_s8_rd_template.md` | Issue 范围与验收 | Governance | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase5_s9_content_template.md` | Issue 范围与验收 | Governance | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase6_s11_basic_memory_context.md` | Issue 范围与验收 | Memory | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_mvp_phase6_s12_experience_convergence.md` | Issue 范围与验收 | Governance | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_regression_stabilization.md` | Issue 范围与验收 | Governance | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_sprint0_architecture_convergence.md` | Issue 范围与验收 | Governance | Frozen | 是（证据） | 否 | 否 |
| `issues/20260729_workspace_regression_employee_templates.md` | Issue 范围与验收 | Employee | Frozen | 是（证据） | 否 | 否 |
| `issues/20260730_digital_employee_execution_control_loop_v1.md` | Issue 范围与验收 | Employee | Frozen | 是（证据） | 否 | 否 |
| `issues/20260730_global_assistant_live_model_validation.md` | Issue 范围与验收 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `issues/20260730_global_assistant_runtime_v1.md` | Issue 范围与验收 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `issues/phase1_asset_factory_consolidation_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/phase1a_ai_company_runtime_foundation.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/phase1c_ceo_office_ui_first_slice.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/phase4_ai_employee_system_mvp.md` | Issue 范围与验收 | Employee | Review | 是（证据） | 否 | 否 |
| `issues/phase45_admin_demo_polish_execution.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/phase45_admin_demo_polish.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/phase45_demo_polish.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/phase5_billing_mvp.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase5_g2_credential_vault_gate.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/phase5_g2_security_review_kickoff.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/phase5_workflow_mvp.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/phase55_admin_readiness_review.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/phase6_workflow_mvp.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/phase7_billing_readiness.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase7_billing_usage_contract_gate.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase7_local_demo_release_hardening_gate.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/phase7_production_credential_vault_gate.md` | Issue 范围与验收 | Identity / Security | Review | 是（证据） | 否 | 否 |
| `issues/phase77_billing_readiness_review.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase8_billing_mvp.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase8_workspace_billing_support.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/phase85_commercial_readiness_review.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `issues/README.md` | 目录或项目入口 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260717_admin_company_package_verify.md` | Issue 范围与验收 | Company / CEO Office | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260717_admin_orphan_instances.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260717_admin_r3_e2e_handoff.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260717_admin_workspace_stash_handoff.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260717_workspace_shared_main_manual_merge_preparation.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260718_admin_next_round_joint_plan.md` | Issue 范围与验收 | Governance | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260718_workspace_admin_company_package_workflow_provenance_l2.md` | Issue 范围与验收 | Task / Execution | Review | 是（证据） | 否 | 否 |
| `issues/shared/20260718_workspace_workbuddy_real_rd_tool_closure_status_sync.md` | Issue 范围与验收 | Capability | Review | 是（证据） | Semantic:WORKBUDDY | 否 |
| `issues/shared/20260722_admin_backend_supply_model_credential.md` | Issue 范围与验收 | Model / Usage | Review | 是（证据） | 否 | 否 |
| `knowledge/000_Project_Brief.md` | 历史上下文或状态 | Project | Review | 待复核 | Semantic:PRODUCT_BASELINE | 否 |
| `knowledge/001_Project_History.md` | 历史上下文或状态 | Project | Deprecated | 否（当前） | 否 | 是 |
| `knowledge/002_Product_Vision.md` | 历史上下文或状态 | Knowledge | Review | 待复核 | Semantic:PRODUCT_BASELINE | 否 |
| `knowledge/003_Architecture.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | Semantic:ARCHITECTURE | 是 |
| `knowledge/004_Workflow.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | 否 | 是 |
| `knowledge/005_Key_Decisions.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | 否 | 是 |
| `knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | 否 | 是 |
| `knowledge/CURRENT_CONTEXT.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | Semantic:CURRENT_STATE | 是 |
| `knowledge/EXECUTION_SUMMARY_MEMORY.md` | 历史上下文或状态 | Knowledge | Review | 待复核 | 否 | 否 |
| `knowledge/NOW.md` | 历史上下文或状态 | Knowledge | Deprecated | 否（当前） | Semantic:CURRENT_STATE | 是 |
| `knowledge/PROJECT_MEMORY.md` | 历史上下文或状态 | Project | Review | 待复核 | 否 | 否 |
| `knowledge/README.md` | 目录或项目入口 | Knowledge | Review | 待复核 | 否 | 否 |
| `knowledge/ROLE_PROFILES.md` | 历史上下文或状态 | Knowledge | Review | 待复核 | 否 | 否 |
| `plugins/curis-ai-development-organization/skills/curis-development-organization/SKILL.md` | 项目文档或参考资产 | Business Department | Review | 待复核 | 否 | 否 |
| `PROJECT_HANDOFF.md` | 历史交接 | Project | Deprecated | 否（当前） | 否 | 是 |
| `PROJECT_STATUS.md` | 历史上下文或状态 | Project | Deprecated | 否（当前） | Semantic:CURRENT_STATE | 是 |
| `README.md` | 目录或项目入口 | General | Frozen | 是（当前） | 否 | 否 |
| `reviews/001_sprint_0_acceptance_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/002_tool_system_v1_6_meta_development_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/003_tool_system_v1_8_controlled_self_evolution_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/004_sprint_1_architecture_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/005_sprint_1_visualization_first_slice_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/006_sprint_1_ceo_readable_visualization_polish_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/007_sprint_2_architecture_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/008_sprint_2_unified_task_console_first_slice_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/009_project_memory_foundation_architecture_boundaries_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/010_project_memory_first_slice_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/012_sprint_3_role_profiles_first_slice_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/014_role_context_runtime_reference_first_slice_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md` | Review 验证证据 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `reviews/017_ai_task_executor_mvp_readiness_boundaries_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/018_ai_task_executor_mvp_readiness_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/019_chinese_operation_console_localization_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/024_post_v0_1_execution_reliability_boundaries_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/025_run_evidence_reliability_first_slice_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/026_workflow_error_fallback_observability_boundaries_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/027_workflow_error_fallback_evidence_map_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/029_evolution_decision_evidence_map_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/030_post_v0_1_execution_reliability_closeout_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/031_local_demo_operator_polish_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/032_local_demo_operator_release_notes_package_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/033_local_demo_verification_automation_boundaries_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/034_local_demo_api_smoke_helper_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/035_project_memory_execution_summary_boundaries_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/036_project_memory_execution_summary_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/037_redesign_v2_architecture_review_decision.md` | Review 验证证据 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `reviews/038_d1_runtime_role_wiring_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/039_d1_boundary_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/040_d1_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/041_d1_implementation_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/042_d3_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/043_d3_boundary_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/044_d3_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/045_d3_implementation_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/046_d2_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/047_d2_boundary_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/048_d2_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/049_d2_implementation_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/050_d1_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/051_d1_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/052_d2_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/053_d2_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/054_d3_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/055_d3_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/056_d4_boundary_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/057_d4_boundary_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/058_d4_implementation_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/059_d2_impl_verification.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/060_d2_impl_acceptance.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/061_workspace_capability_integration_phase_1_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/062_workspace_model_gateway_adapter_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/063_workspace_official_model_catalog_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/064_workspace_official_tool_catalog_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/065_new_api_local_deployment_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/066_model_gateway_production_security_boundary_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/067_model_gateway_runtime_secret_guardrails_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/068_workspace_tenant_model_preference_boundaries_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/069_workspace_tenant_model_preference_first_slice_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/070_workspace_model_preference_ui_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/071_workspace_model_preference_local_e2e_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/072_model_gateway_local_demo_release_candidate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/073_model_gateway_local_demo_release_closeout_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/074_workspace_company_foundation_boundaries_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/075_workspace_company_foundation_first_slice_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/076_workspace_company_foundation_local_demo_evidence_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/076_workspace_company_foundation_local_demo_evidence.png` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/077_workspace_company_department_catalog_summary_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/078_workspace_department_catalog_local_demo_evidence_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/078_workspace_department_catalog_local_demo_evidence.png` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/079_workspace_department_activation_boundaries_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/080_workspace_department_activation_first_slice_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/081_workspace_department_activation_ui_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/082_workspace_admin_contract_integration_completion_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/083_workspace_self_extension_mvp_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/084_phase4_ai_employee_system_mvp_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/085_phase4_ai_employee_system_rc_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_pr2_post_merge_scope_governance_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r1_unified_runtime_baseline_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_artifact_project_status_architecture_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_ceo_mapping_migration_input_architecture_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_exact_binding_scope_set_architecture_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_exact_binding_scope_set_l2_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_real_model_execution_architecture_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_real_model_execution_dns_https_egress_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_real_model_execution_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_real_model_execution_security_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_remaining_role_employee_binding_set_architecture_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_remaining_role_employee_binding_set_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_remaining_six_model_calls_l2_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_remaining_six_model_calls_security_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_remaining_workflow_completion_architecture_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_trusted_ceo_usage_context_architecture_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_trusted_ceo_usage_context_security_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_workflow_context_budget_architecture_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_r3_workflow_context_budget_l2_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_shared_main_manual_merge_preparation_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_tenant_identity_membership_implementation_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260717_workspace_tenant_identity_membership_implementation_security_boundary_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_admin_company_package_workflow_provenance_l2_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_company_package_provenance_isolated_setup_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_company_package_provenance_membership_provisioning_architecture_review.md` | Review 验证证据 | Company / CEO Office | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_company_package_provenance_real_execution_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_container_exit1_static_diagnostic_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_container_exit1_static_diagnostic_security_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_entry_owner_role_claim_fix_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_entry_owner_role_claim_fix_security_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_selfuse_trusted_identity_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_selfuse_trusted_provisioning_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_single_model_toolchain_entry_gate_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_d1_single_model_toolchain_entry_security_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_gateway_startup_evidence_preservation_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_gateway_startup_evidence_preservation_security_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_minimal_rd_toolset_implementation_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_minimal_rd_toolset_security_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_package_workflow_bridge_revocation_failclosed_fix_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_package_workflow_versioned_bridge_implementation_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_agent_mode_entry_criteria_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_agent_mode_failclosed_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b1_failure_blocking_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b1_response_contract_alignment_security_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_security_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b3_minimal_logging_visibility_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b3_minimal_logging_visibility_security_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_risk_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_refusal_status_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_relation_contract_fix_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_security_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_field_contract_fix_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_security_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3c_no_execute_side_effect_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_ai_secretary_scope_gate_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_hybrid_mode_entry_switch_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_hybrid_mode_handoff_contract_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_hybrid_mode_profile_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_items_1_7_code_construction_audit_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_manual_risk_escalation_contract_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_manual_stop_boundary_contract_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_manual_takeover_request_contract_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_mode_contract_validation_compatibility_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_mode_contract_validation_failclosed_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_mode_contract_validation_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_multi_project_session_context_switch_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_multi_project_session_recovery_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_multi_project_session_scope_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_multi_project_session_seed_gap_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_closeout_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_security_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_security_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_scope_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_snapshot_fix_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b2_failure_check_matrix_fix_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_security_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_team_migration_transfer_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_artifact_output_backend_gate_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_artifact_output_closeout_gate_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_artifact_output_contract_gate_review.md` | Review 验证证据 | Artifact | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_token_cost_budget_closeout_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_token_cost_budget_contract_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_token_cost_budget_projection_failclosed_fix_gate_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_unified_token_cost_budget_visibility_gate_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_workflow_mode_entry_guard_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_r4_workflow_mode_sequence_contract_gate_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_real_rd_tool_closure_prerequisite_gate_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation_security_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260718_workspace_selfuse_official_workflow_bridge_compatibility_fix_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_d1_unfreeze_qa.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_admin_warning_suppression_minimal_fix_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_create_app_d1_minimal_fix_qa.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_pinned_online_build_postbuild_sentinel_review.md` | Review 验证证据 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_entry_wrapper_minimal_implementation_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_failure_deterministic_evidence_gate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_failure_signal_controlled_revert_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_failure_single_sentinel_diagnostic_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_signal_exception_type_enrichment_qa.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260719_workspace_startup_stage_signal_minimal_implementation_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260720_d1_execute_a_qa.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260720_d1_execute_b_qa.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260722_local_project_runtime_target_provisioning_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260722_macos_keychain_google_oidc_project_runtime_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260722_project_runtime_page_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260722_real_rd_container_runtime_prerequisite_review.md` | Review 验证证据 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260723_project_owner_workbench_product_flow_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_ai_call_usage_ledger_foundation_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_business_department_org_model_review.md` | Review 验证证据 | Business Department | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_freellmapi_owner_only_experimental_gateway_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_p0_authentication_onboarding_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_p0_local_desktop_owner_review.md` | Review 验证证据 | Identity / Security | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md` | Review 验证证据 | UI / Design System | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase1_s2_workspace_model_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase2_s3_ai_employee_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase3_s4_project_review.md` | Review 验证证据 | Project | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase3_s5_task_execution_review.md` | Review 验证证据 | Task / Execution | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase4_s6_capability_registry_review.md` | Review 验证证据 | Capability | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase4_s7_model_gateway_review.md` | Review 验证证据 | Model / Usage | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase5_s10_knowledge_management_review.md` | Review 验证证据 | Knowledge | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase5_s8_rd_template_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase5_s9_content_template_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase6_s11_basic_memory_context_review.md` | Review 验证证据 | Memory | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_mvp_phase6_s12_experience_convergence_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_regression_stabilization_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_sprint0_architecture_convergence_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260729_workspace_regression_employee_templates_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260730_digital_employee_execution_control_loop_v1_review.md` | Review 验证证据 | Employee | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260730_global_assistant_live_model_validation_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260730_global_assistant_runtime_v1_review.md` | Review 验证证据 | Assistant | Frozen | 是（证据） | 否 | 否 |
| `reviews/20260730_integration_candidate_review.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/paperclip-competitive-analysis-2026-07-08.md` | Review 验证证据 | Governance | Frozen | 是（证据） | 否 | 否 |
| `reviews/README.md` | 目录或项目入口 | Governance | Frozen | 是（证据） | 否 | 否 |
| `shared/architecture/curis-admin-workspace-product-architecture.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md` | 项目文档或参考资产 | Governance | Review | 待复核 | 否 | 否 |
| `shared/pmo/PROJECT_SPACE_MAP.md` | 项目文档或参考资产 | Project | Review | 待复核 | 否 | 否 |
| `shared/product/curis-admin-workspace-flows.md` | 项目文档或参考资产 | General | Review | 待复核 | 否 | 否 |
| `shared/product/curis-commercial-multitenant-change-brief.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `shared/product/curis-commercial-system-product-doc.md` | 项目文档或参考资产 | Model / Usage | Review | 待复核 | 否 | 否 |
| `shared/prototypes/curis-full-system-high-fidelity-prototype.html` | 历史原型 | UI / Design System | Deprecated | 否（当前） | 否 | 是 |
| `shared/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |
| `TASKS.md` | 历史上下文或状态 | Task / Execution | Deprecated | 否（当前） | Semantic:CURRENT_STATE | 是 |
| `workspace/README.md` | 目录或项目入口 | General | Review | 待复核 | 否 | 否 |


## 2026-10-05 — CG first graphic vertical authorized, NOT ACCEPTED

Status: Review · Authority Class: IMPLEMENTATION BOUNDARY / OWNER DECISION PROVENANCE · Disposition: REVIEW_REQUIRED.
Delivery Owner accepted CG readiness as implementation input and R03 DESIGN_HANDOFF §8 as bounded Approved Design, then granted exact27 paths/owned functions after Writing schema-01 independent QA closure. Formal Issue: issues/CURIS-V1-CG-PRODUCT-ENTRY-001.md; actual review: docs/reviews/CURIS_V1_CG_PRODUCT_ENTRY_REVIEW.md; Task baseline: artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/SOURCE_SEAL.json.

Implementation IN PROGRESS / NOT ACCEPTED. Existing canonical CONTENT_ITEM/CONTENT_VERSION/Shared Task/Conversation/Identity/singleUsage are reused; bounded Package binding, atomicCAS and manualadopt without Review→SCHEDULED, purpose dispatch and readonly originalquery/UNKNOWNnoReplay are authorized. Candidate definition is no-publication; ordinary published activation, actualcloud/fees/credentials/native/defaultApp not authorized. Isolated focused/regression/build/Browser roots and ports only perIssue. FullCG fourformats/perAccount publication/receipts/analytics/review/nextcycle remain open in these existing backlogs, not removed by firstgraphic.

Owner/NextAction: Delivery Owner receives sealed matching evidence and independentQA; nextGate bounded actual implementation/test/Browser review, separate exact publication/live/native decisions. This append does not promote Product/Frozen or Accepted.


## 2026-10-05 — Exact28 bounded implementation handoff, review required

Status: Review. Authority Class: REVIEW / IMPLEMENTATION EVIDENCE. Disposition: REVIEW_REQUIRED.
Verdict: BOUNDED_IMPLEMENTATION_AND_CONTROLLED_REGRESSION_PASS / BROWSER_PARTIAL / NOT_ACCEPTED / DEFINITION_UNPUBLISHED.
Actual CG source28 is sealed in artifacts/tasks/CURIS-V1-CG-PRODUCT-ENTRY-001/SOURCE_SEAL.json; exact handoff/owned diff/output manifest share that area. Focused21 PASS; combined backend110 PASS; frontend17 PASS; lint/syntax/production build PASS; protected3 DB exact fingerprints unchanged and read-only integrity ok. Real Browser saved/manualcandidate/adoptedVersion, model return, old selection read-only, original UNKNOWN/list priority/cross-content lock verified. Query events8->8, Task0->0, Usage0->0, outbound0.
Employee detail Browser Failed to fetch remains FAIL/cause UNKNOWN (retry and independent tab); API/preflight success is not Browser return acceptance. Browser company used SQL fixture, canonical assistant + later ARRIVED/UNVERIFIED FoundingRun correction for existing-company bootstrap; not formal normal Company creation. Candidate package install is not published ordinary Business/atomic firstWorkspace activation proof. Original failures/logs retained. Physical crash at every Task/outbound gap, realProvider/fees/credentials/Keychain/native/defaultApp NOT RUN. FullCG3otherformats/accountpublication/receipt/review/learning goals remain. No Product/Frozen rewrite/Git mutation. Owner/independent QA is next Gate; publication/live/native require separate exact decisions.


## 2026-10-06 — Stage A Beta 分发文档索引增补

| 文件 | 状态 | 用途 |
| --- | --- | --- |
| `docs/04_Development/CURIS_BETA_STAGE_A_DISTRIBUTION.md` | Review | Curis V1 Beta Stage A（未签名/不公证/零 Apple 费用）唯一发布文档：版本化 DMG 与 SHA-256 校验、Sequoia 15+ Gatekeeper Open Anyway 安装、首启与默认数据位置、已知限制、curis-recovery 备份/恢复、手动升级与发布 checklist |
