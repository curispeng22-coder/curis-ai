# Curis 开发基线与文档目录收口

Status: Review
Authority Class: EVIDENCE / EXECUTION ISSUE
Owner: Delivery Owner
Updated: 2026-10-25
Task ID: CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025

CEO 已授权本轮普通文档维护。用户确认 App 可正常打开，但实际使用仍有差距。本任务保留 RC9 有限本地手工验收，只整理基线、文档及目录索引。

## 授权来源与范围

CEO 2026-10-25: 就按这个方案开始，先收口开发基线、文档和目录，沿用现有入口和看板。保留已验收成果，不改业务代码，模型继续搁置；需要移动、归档或删除的先列清单给我确认，普通文档问题自行处理，跟完核对再汇报。

[治理维护 Decision](<../docs/07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)仅落实既有 AGENTS 的真相分层和本轮文档授权，不改变 Product/Frozen 产品合同。源码、配置只作静态只读核对；不执行构建、测试或 App 操作，不读取数据库和凭据。

## Allowed Files

- /Users/yy/Documents/Curis AI Workspace/README.md
- /Users/yy/Documents/Curis AI Workspace/AGENT.md
- /Users/yy/Documents/Curis AI Workspace/PROJECT_STATUS.md
- /Users/yy/Documents/Curis AI Workspace/PROJECT_HANDOFF.md
- /Users/yy/Documents/Curis AI Workspace/TASKS.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/DOCUMENT_INVENTORY.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/DOCUMENT_STATUS_RULES.md
- /Users/yy/Documents/Curis AI Workspace/docs/04_Development/Curis_Development_Guide.md
- /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md
- /Users/yy/Documents/Curis AI Workspace/docs/07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md
- /Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/TASK_START.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/BASELINE_SNAPSHOT.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/WORKTREE_STATUS_BEFORE.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/CODE_FINGERPRINTS_BEFORE.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/DIRECTORY_INVENTORY.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/DOCUMENT_METADATA.csv
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.csv
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/REFERENCE_CHECK.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/CHECK_RESULTS.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/OUTPUT_MANIFEST.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/RESULT.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/CODE_PRESERVATION_AFTER.json

## Allowed Directories

- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/preimages

## 输入、输出与验收

输入：AGENTS → 现有入口 → CURRENT_STATE → 本 Issue / 现有执行看板；已接受 RC9 的 Source / Package / Owner 回证；相关开发配置。
输出：现有文档中的明确开发基线、修正入口和索引；任务区事实快照、前像、目录清单、引用及保全核对和 Output Manifest。

- 唯一入口与看板指向本Task；不新建平行产品Authority或Backlog
- Git HEAD/工作区状态/RC9 Source67/安装包身份与复现边界分别登记
- 开发指南启动/测试/打包命令对照现有配置，文档检查不运行产品或写数据
- 当前文档引用和状态/Authority分类一致，新链接无新增断链
- 移动/归档/删除只提出精确路径清单，实际动作0
- 业务代码、既有交付包与验收证据前后保持不变；未stage/commit/push/reset/clean/stash
- 用户实际使用差距登记为待具体化输入，不撤销有限已验成果，不升级模型或全产品验收

## 禁止项

- 业务代码/Runtime/Schema修改；任何数据库、凭据或模型连接读写及测试（源码与构建配置仅可静态只读核对）
- 启动/退出/控制App或开发服务、执行构建及产品回归
- 任何物理移动/归档/删除/重命名
- 任何Git mutation
- 修改Product Blueprint/Master Map/UI Blueprint/领域产品合同、旧已验回证、RC9安装指南/镜像/源码快照
- 把dirty worktree或当前HEAD自动提升为已提交release

## 执行与回证

本轮进度只登记在 [既有唯一执行看板](<../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)；最终文档核对、未做事项与下一 Gate 见 [本轮结果](<../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/RESULT.md>)。物理移动、归档、删除、重命名均为 0；候选清单仅供 CEO 确认。

Next Gate: 文档核对完成后，CEO 决定精确归档候选；后续实际使用迭代在现有 Backlog 建立正式 Issue 后执行。本任务不授权业务开发或 Git 源码整合。

## CEO 已确认 A01–A03 归档：本任务的精确续执行范围

Task ID: CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/ARCHIVE-A01-A03
Owner: Delivery Owner
Risk Level: P2 文档迁移 / P1 引用与保全
Source: CEO 本次明确同意原清单三项，保留历史正文和原根路径兼容指针，其他目录不动，模型 DEFERRED。

本节对前阶段“只列清单/不物理归档”的限制仅在 A01–A03 精确集合内作后续授权登记；此前事实和回证原样保留，不将本授权扩大到其他目录或删除。继续使用本 Issue / 原唯一看板。

### 续执行 Allowed Files

- /Users/yy/Documents/Curis AI Workspace/README.md
- /Users/yy/Documents/Curis AI Workspace/PROJECT_STATUS.md
- /Users/yy/Documents/Curis AI Workspace/PROJECT_HANDOFF.md
- /Users/yy/Documents/Curis AI Workspace/TASKS.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md
- /Users/yy/Documents/Curis AI Workspace/docs/00_Context/DOCUMENT_INVENTORY.md
- /Users/yy/Documents/Curis AI Workspace/docs/04_Development/Curis_Development_Guide.md
- /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md
- /Users/yy/Documents/Curis AI Workspace/docs/07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/README.md
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/CURIS_CLEANUP_LEDGER.md
- /Users/yy/Documents/Curis AI Workspace/issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/development-baseline-2026-10-25/root-legacy-docs/PROJECT_STATUS.md
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/development-baseline-2026-10-25/root-legacy-docs/PROJECT_HANDOFF.md
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/development-baseline-2026-10-25/root-legacy-docs/TASKS.md
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/TASK_START.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/PRECHECK.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/REFERENCE_CHECK.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/MIGRATION_RECEIPT.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/CHECK_RESULTS.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/OUTPUT_MANIFEST.json
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md

### 续执行 Allowed Directories

- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03
- /Users/yy/Documents/Curis AI Workspace/artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/preimages
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/development-baseline-2026-10-25
- /Users/yy/Documents/Curis AI Workspace/docs/99_Archive/development-baseline-2026-10-25/root-legacy-docs

### 验收、交付与下一步

- Three exact archive destinations; retain original root paths as current navigation stubs
- Preserve complete historical prose/date and exact original preimages; rebase only Markdown relative link targets at archive destinations, with reversible change map
- New/current refs resolve; root path dependencies remain compatible; record before/after scoped reference scan
- Current entrypoint/board/backlog/inventory/Archive index/ledger/Current State/ChangeLog synchronized; no parallel authority or backlog
- Business code/config/accepted RC9 seal files/Product authority and prior phase evidence hashes unchanged
- No DB/credential/model read or write, no App operation/build/test, no Git mutation, no other directory placement changes

输入为原精确清单/前像、当前三文件、现有归档索引/清理账本、开发事实及已接受 RC9 回证。输出为三个历史归档、三份兼容指针和 archive-a01-a03 内的迁移回证/引用及保全核对/Output Manifest。归档正文只换算相对 Markdown 链接目标以适应新位置；文字、日期与前像可逆保全。

Next Gate: 完成后由 Owner 接受本次文档归档；后续实际使用迭代和干净源码集成另走现有队列与正式 Scope。

### A01–A03 执行结果

三份历史正文已归档，原根路径保留当前导航兼容指针；本集合归档批准门已满足，无需再次向 CEO 确认。
[归档结果](<../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>) / [引用与保全核对](<../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/CHECK_RESULTS.json>) / [Output Manifest](<../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/OUTPUT_MANIFEST.json>)；其他目录与旧阶段 Evidence 保持原位。
