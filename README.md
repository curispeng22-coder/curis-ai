# Curis AI Company Operating System

Status: Frozen
Authority Class: CURRENT / WORKSPACE NAVIGATION
Owner: Delivery Owner
Updated: 2026-10-25
Decision: [开发基线与文档维护](<docs/07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)

先读 [AGENTS](<AGENTS.md>) → [当前入口](<docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md>)。产品定义经 Pointer 查询；实现现状、任务和验收经 CURRENT_STATE 查询。

## 当前基线与任务

RC9 已完成批准范围内的本地手工 L1/L2 验收和安装交付，见 [交付回证](<artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/owner-incident-20261018-01/rootf-writing-ui-owner-01/RC9_DELIVERY_RECEIPT.md>)。用户确认可以打开，实际使用差距仍需补充迭代。模型继续 DEFERRED；C01/真实员工 Result 正向仍待验。

当前观察的 Git 为 main @ 78cacbd0857cc36c9f3fe0e4b11346489993b728，含大量既有未提交改动；该 SHA 不代表 RC9 的干净源码提交。RC9 的 Source67 / Package / Native / DMG 对应关系、运行和构建边界统一见 [开发指南](<docs/04_Development/Curis_Development_Guide.md>)。

本轮 [文档目录收口 Issue](<issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>)只修改文档。进度沿用 [既有执行看板](<artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)，根 TASKS / PROJECT_STATUS / PROJECT_HANDOFF 仅保留兼容导航，三份历史正文已按 CEO 批准归档，不构成另一套任务入口。

## 开发目录

| 路径 | 作用 |
|---|---|
| frontend / backend | 当前前端与本地业务服务源码 |
| desktop / deploy | 桌面壳、打包及本地 Gateway 脚本 |
| shared / tools / plugins | 共享实现与开发工具；具体用途按 Issue 核对 |
| docs / issues | 正式文档与精确任务 Scope |
| artifacts/tasks | 已登记任务证据和生成物；保留既有成果 |

完整目录分类与待确认的历史放置候选见 [文档与目录索引](<docs/00_Context/DOCUMENT_INVENTORY.md>)。数据、环境、工作树及未知文件保留原位。

## 启动、检查和打包

已交付 App 位于 /Applications/Curis.app；安装镜像和已验版本身份见开发指南。开发启动必须先有隔离资料根与正式 Issue，不能把用户正常资料当作测试库。

deploy/curis/start-local.sh 属于历史 Docker/Gateway 开发链，会绑定工作区 data/curis.sqlite，并非最新桌面版的唯一运行入口。
本轮只静态核对现有命令；未启动服务、运行测试或重建安装包。测试、构建和已提交源码整合须在后续正式任务中分别验证。
