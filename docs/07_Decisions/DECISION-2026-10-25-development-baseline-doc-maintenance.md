# 开发基线与文档维护决定 — 2026-10-25

Status: Frozen
Authority Class: FROZEN / GOVERNANCE DECISION
Owner: Delivery Owner（CEO 本轮委托的普通文档维护）
Updated: 2026-10-25
Task ID: CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025
Disposition: OWNER ACCEPTED / DOCUMENT MAINTENANCE ONLY
Baseline: main @ 78cacbd0857cc36c9f3fe0e4b11346489993b728（本轮观察；非提交态 RC9）
Supersedes: 现有入口/开发指南中的过期默认导航与旧提交“唯一产品基线”表述；不替代产品合同或历史验收。

## 来源与决定

CEO 原文：“就按这个方案开始，先收口开发基线、文档和目录，沿用现有入口和看板。保留已验收成果，不改业务代码，模型继续搁置；需要移动、归档或删除的先列清单给我确认，普通文档问题自行处理，跟完核对再汇报。”

依据 [AGENTS](<../../AGENTS.md>) §1/2/5/9/10、本轮 [正式 Issue](<../../issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>) 的精确 Allowed Files，以及已封存的 [RC9 本地交付回证](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/owner-incident-20261018-01/rootf-writing-ui-owner-01/RC9_DELIVERY_RECEIPT.md>)，决定：

1. 继续使用现有 Entrypoint、Pointer、CURRENT_STATE、Development Guide、Document Inventory、Execution Backlog 和唯一执行看板。修正文档导航、开发事实及元数据；不建立第二套 Current 产品文档或进度表。
2. 产品真相与实现真相按 AGENTS 的现行路线分开。状态规则旧 §3 的通用排序不再用于跨类裁决；这是对现行用户指令的文档同步。相同类别的 Current/Frozen Authority 若仍冲突，必须 STOP / REPORT，不能凭本决定自行选边。
3. RC9 的 Source67、Package、Native、DMG、L1/L2 Owner 接受保持原证据和有限本地手工范围。当前 Git HEAD 与既有混合工作区单独登记；不将其视为干净已提交的 RC9，不授权 Git 整合或重建。
4. 用户“可以打开但距离实际使用有差距”的反馈登记为待具体化迭代输入；不抹去已接受成果，也不把局部/本地接受升级为完整产品可用。模型继续 DEFERRED，C01/真实 Employee Result 正向继续 PENDING。
5. 历史内容保留原文并退出默认入口；物理移动/归档/删除一律先列精确路径，待 CEO 确认后另行执行。

## 精确维护集与保留边界

仅 [Issue 的 Allowed Files](<../../issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>) 中列出的 14 份既有导航、开发、治理、状态、索引及看板文件，以及本决定、Issue 和该任务区证据可写。
Product Blueprint / Master Map / UI Blueprint / 领域 Frozen 合同、业务代码、Runtime/Schema、既有安装包和验收证据均不改。
不启动/退出/操作 App，不读写数据库/凭据，不连接模型，不运行产品构建或回归，不执行 Git mutation。

## 验收与处置

文档引用、状态/分类、当前版本对应、代码及交付物保全核对由 Owner 完成，结果见 [本轮结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/RESULT.md>) 和 [机器核对结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/CHECK_RESULTS.json>)。
已授权的 canonical 文档维护接受后为 PROMOTE；任务快照与候选保留 REVIEW_REQUIRED。候选不是归档或删除许可。
同步登记 [CURRENT_STATE](<../00_Context/CURRENT_STATE.md>) 与 [Change Log](<../08_Change_Log/CHANGE_LOG.md>)。
Next Gate: CEO 确认精确目录处置；后续业务/源码版本整合仍需正式 Scope 和 Allowed Files。

## CEO 后续确认：A01–A03 归档与根路径兼容指针

Source: “同意按清单归档 PROJECT_STATUS、PROJECT_HANDOFF、TASKS 这三份旧文档，保留历史正文和原路径兼容指针，其他目录先不动。沿用现有入口和看板，模型继续搁置，完成引用和保全核对后再汇报。”
Task ID: CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/ARCHIVE-A01-A03
Disposition: CEO APPROVED EXACT ARCHIVE SET / OWNER EXECUTION AND VERIFICATION

本次只执行原清单 A01 PROJECT_STATUS.md、A02 PROJECT_HANDOFF.md、A03 TASKS.md，目的地逐项固定在 docs/99_Archive/development-baseline-2026-10-25/root-legacy-docs/ 同名文件。
历史正文、原日期和 Status: Deprecated / HISTORY 保留；仅将归档文件中 5 处原导航相对链接按新位置换算，逐项记录可逆映射和原始完整字节前像。根三路径改为 Frozen / CURRENT NAVIGATION ONLY 的简短指针；旧代码字符串引用可继续访问这些路径。
精确 Allowed Files/Directories 见同一 Issue 的“CEO 已确认 A01–A03”续执行节及 [本次范围记录](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/TASK_START.json>)；新增归档索引和账本维护在该集合中，产品 Authority 不变。
前阶段“候选待确认/未归档”保留为当时事实；本集合已获明确授权，不再等重复确认。其他目录不动、无删除，业务代码/Runtime/Schema/资料/模型、已验 RC9 和历史证据继续保护。

[实际迁移回证](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/MIGRATION_RECEIPT.json>) / [最终核对](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/CHECK_RESULTS.json>) / [结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>)。
Next Gate: Owner 接受本次精确归档后，返回现有 Backlog 的实际使用差距与源码版本整理；该后续工作仍须其独立 Scope，不由本归档授权扩大。
