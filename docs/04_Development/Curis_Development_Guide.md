# Curis Development Guide

Status: Frozen
Authority Class: CURRENT / DEVELOPMENT STANDARD
Owner: Delivery Owner
Updated: 2026-10-25
Decision: [开发基线与文档维护决定](<../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)
Baseline observation: main @ 78cacbd0857cc36c9f3fe0e4b11346489993b728；工作区不是 clean committed release

## 1. 从哪里开始

先读 [AGENTS](<../../AGENTS.md>) → [当前入口](<../00_Context/CURIS_CURRENT_ENTRYPOINT.md>)。
产品定义走 Pointer → Blueprint → Master Map → UI Blueprint → 适用 Frozen Authority；实现走 CURRENT_STATE → 正式 Issue / Allowed Files → 代码/运行证据 → 已接受回证。
进度只看 [现有执行看板](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)，后续任务沿用 [Execution Backlog](<../reviews/CURIS_V1_EXECUTION_BACKLOG.md>)，根目录 TASKS 仅为当前导航兼容指针，旧正文已获批准归档，不另设任务队列。

## 2. 当前开发目录与已交付版本

这四类事实不能混用：

| 对象 | 2026-10-25 核对结果 | 含义 |
|---|---|---|
| Git | main @ 78cacbd0857cc36c9f3fe0e4b11346489993b728 | 当前 HEAD 观察，不能代称 RC9 源码版本 |
| 既有工作区 | 1050 个 porcelain 条目：162 modified / 888 untracked | 正常 untracked 模式会折叠目录，不是文件总数；排除本轮新 Issue / 任务产物 |
| RC9 Source67 | 67/67 与当前文件逐项匹配；manifest SHA f0d308e549788aff9c791f565182e2e62b60cad1f2e5e71ed9a5e36a57add916 | 精确已集成源码快照；不代表其余工作区都在验收范围 |
| RC9/App10 安装交付 | Package SHA 4204c1396bd1dcf762b90b6ecdce5ca88689003d2f74a3742074461c1f87160a | 同版批准本地手工 L1/L2 已接受；Git clean promotion 未做 |

版本对应输入：[Source67](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/developer/remaining-app-delivery/local-use-closure-01/build-l1-rc1-10/SOURCE_MANIFEST.json>) / [Package12705](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/developer/remaining-app-delivery/local-use-closure-01/build-l1-rc1-10/MATCHED_PACKAGE_MANIFEST.json>) / [最终交付回证](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/owner-incident-20261018-01/rootf-writing-ui-owner-01/RC9_DELIVERY_RECEIPT.md>)。
前端 BUILD_ID：LaRyju9Y4Otw3tUGMlAEs。
Native SHA：1fa7866c017fce73eeb7c4d272781c27b6d6585415463e7bc564bb2709447477；源 App10 与 /Applications/Curis.app 的 Native 一致。
已交付 [RC9 DMG](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/developer/remaining-app-delivery/local-use-closure-01/install-01/Curis_0.1.0_local_20261024_rc9_arm64.dmg>) SHA：1fd5284bae218220aa2046813b5c9bc341426dc5ca3f21bdd11486ce2eb432bb；[原安装说明](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/developer/remaining-app-delivery/local-use-closure-01/install-01/CANDIDATE_INSTALL_GUIDE.md>)保持原件。

本轮 [基线快照](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/BASELINE_SNAPSHOT.json>)记录完整路径、大小、SHA 和文档前像。
旧 main @ c0e1855f 的说法只属于早期基线；不再作为当前唯一产品/源码版本。
用户确认 App 可以打开，但实际使用差距仍需具体化；有限本地交付不等于完整日用或模型能力通过。

## 3. 运行与环境分开

| 方式 | 现有入口/配置 | 数据与使用边界 |
|---|---|---|
| 已安装桌面版 | /Applications/Curis.app；desktop/tauri.conf.json 声明 0.1.0 / com.curis.desktop | 用户正常资料；开发测试不借用此资料库 |
| Frontend 单独开发 | pnpm --dir frontend dev --port 3010 | 仅前端开发命令；不是后端/Gateway/桌面全栈启动证明 |
| Tauri 开发配置 | beforeDevCommand 同上；devUrl 127.0.0.1:3010 | 仍须独立 Issue、精确隔离根及保护门；不能直接拿 tauri dev 验收 |
| Docker/Gateway 历史开发链 | deploy/curis/start-local.sh / stop-local.sh；前端默认 3001，Gateway 8080 | start-local 非 sentinel 分支强制工作区 data/curis.sqlite，并读取生成质量配置；不得当无副作用的默认启动方式 |

源码目录 frontend / backend / desktop，支撑 deploy / shared / tools / plugins；目录分类见 [文档与目录索引](<../00_Context/DOCUMENT_INVENTORY.md>)。
本轮不安装依赖、不读凭据、不启动服务或 App。Next/pnpm、Python、Rust/Tauri 的精确依赖以对应 package/lock/config 和批准构建证据为准，不凭安装机状态推定干净机器可复现。
macOS minimumSystemVersion=12.0 是配置声明；已验主机为 macOS 26.5 / arm64，未扩展到 Intel、跨机器、全 macOS 版本或公证发行。

## 4. 测试与构建命令的适用条件

以下是对现有脚本的静态核对，**本任务未执行**。未来必须在独立 Issue 明确源码范围、隔离资料和输出后才运行；不能把下面的命令清单当成已经通过的回归。

| 检查/输出 | 现有命令或文件 | 运行条件 |
|---|---|---|
| 前端 lint | pnpm --dir frontend lint | package.json 现有脚本；只验证相关改动，不等于全链验收 |
| 前端生产构建 | pnpm --dir frontend build | 会写 frontend/.next；先授权构建输出和复用范围 |
| 前端定向单测示例 | node --test frontend/tests/writingBookFlow.test.mjs | 无 package.json test 脚本；按实际影响选既有测试，不机械全重跑 |
| 后端定向单测示例 | backend/.venv/bin/python -m pytest -q backend/tests/test_writing_book_context.py | 复用批准隔离 fixture/DB 环境，禁止默认资料库；不用根目录 .venv 路径冒充已验环境 |
| 恢复定向单测示例 | backend/.venv/bin/python -m pytest -q desktop/tests/test_release_recovery.py | 仅在明确隔离/保护条件后运行，不是真实恢复许可 |
| 通用 runtime 构建 | pnpm --dir desktop build:runtime | scripts/build-runtime.sh 会重建 desktop/.runtime 和 frontend/.next；可能缺本地 PyInstaller 工具，不允许隐式联网安装 |
| 通用 App 构建 | pnpm --dir desktop build | runtime 构建后 tauri build --bundles app；frontendDist=desktop/static，runtime 作为资源捆绑 |
| 通用 DMG 脚本 | desktop/scripts/build-manual-dmg.sh [明确的 App 路径] [新的 DMG 路径] | hdiutil 使用 -ov；只可指定新输出并核对不覆盖；脚本存在不等于 RC9 被重新验证 |

对应配置：[frontend scripts](<../../frontend/package.json>) / [desktop scripts](<../../desktop/package.json>) / [Tauri config](<../../desktop/tauri.conf.json>) / [runtime builder](<../../desktop/scripts/build-runtime.sh>) / [DMG builder](<../../desktop/scripts/build-manual-dmg.sh>)。

### RC9 复现边界

RC9 按 [原精确构建计划](<../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/developer/remaining-app-delivery/local-use-closure-01/build-l1-rc1-10/BUILD_PLAN.json>) 重新编译 Recovery，复用已核验 donor 的 frontend/workspace/gateway/guardian/node/Native，重新签名并形成整包 manifest。
这是有来源绑定的增量构建，**没有证明“只从当前 HEAD 干净 checkout 即可完整重建同一 RC9”**。通用构建脚本也不是这一结论的替代证据。
原 OWNER_BUILD_RELEASE / one-use marker 和实际执行记录已消费、应原样保留；不得复制标记重跑旧 helper。
后续要做干净源码版本整合或重建时，先建立独立 Issue、明确 Allowed Files/输出与保护门，再核对输入闭包、实际构建和同版验收；本次不擅自 commit/tag/build。

## 5. Issue、Git 与三角色职责

任何多文件/实现任务先有 Task ID、Scope、Allowed Files/Directories、输入、输出、验收、Risk Level、Owner 与 Next Task。
普通文档维护沿本轮授权处理；业务功能顺序仍为 Product Definition → Business Runtime Blueprint → UI Design → Code，不凭代码反向改产品。

- Owner 定义完整用户旅程、跨角色 Gate、固定候选和真实 App 最终接受，维护唯一看板。
- Developer 在授权范围内连续完成流程、错误/取消/持久化和普通修复，并自测。
- 独立 QA 同步准备、集中核验固定候选，普通失败直接回开发、只复验受影响部分，不以开发自测代替判断。

禁止覆盖、重置或清除既有用户改动。记录分支与 SHA；Git 变更、整合、stage/commit/push、stash/checkout/reset/clean/worktree 操作均需精确授权。
新分支仅限正式任务，使用当前 Agent 约定的 codex/ 前缀；旧阶段 feat/fix 命名不是本轮开分支许可。

P0 数据风险/未知变化、不可逆操作、新增系统权限、密钥费用、产品 Authority 冲突、重大 Scope 变化交 CEO；P1 走自测+独立 QA+同版真实 App；P2 批量修复并按影响复验。
这不解除身份/资料保护门，也不要求继续无限完善与用户功能无关的文件框自动化工具。

## 6. 完成与证据

SOURCE COMPLETE、QA PASSED、PACKAGE READY、NATIVE ACCEPTED、DELIVERED 分别记录。
验收须有对象/版本一致性、业务终点、保存/重启和必要异常证据，不能以页面、按钮、API 200、Mock 或多个历史版本的局部成功相加代替整条旅程。
真实模型、外部发布、外部数据及音频生成 Provider 继续 DEFERRED；C01/真实 Employee Result 正向 PENDING。已接受且未受影响的证据保留，不机械重验。

文档任务做引用、状态/分类、范围和 git diff --check；不触发产品回归。
Runtime/Schema/数据库变化另按既有保护与迁移合同执行。遇到缺合法证据、Scope、授权或同类 Authority 冲突，STOP / REPORT 并指出 Owner 和恢复 Gate。

## 7. 文档与历史

文档状态仅 Draft / Review / Frozen / Deprecated。Frozen 维护须有 lawful Decision、Change Log 及相应 Pointer/CURRENT_STATE 同步。
移动、重命名、归档或删除必须先扫引用、评估源码/构建依赖、保全独有来源，再取得精确授权；前阶段只列候选；CEO 后续已精确批准 A01–A03 并完成归档，见 [核对结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>)。其余目录不动。
旧迁移/ADR 在其适用任务中继续消费，不再将 Product Reset 历史 Gate 当成所有新任务默认状态。历史来源与 supersession 见既有索引及各原文件。

本轮 [正式 Issue](<../../issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>) / [核对结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/RESULT.md>)；未完成的源码整合和实际使用迭代仍从唯一看板进入，不另立第二套开发基线。

## 8. 业务实现 Review 的既有约束

业务实现仍需写明 Company OS 或 Workspace 所属、Blueprint 对应段落，以及适用的 ADR-0040 / ADR-0041；说明 Business Runtime 的阶段/状态、Owner、Input/Output、转换、反馈、终点和模拟证据。
不得重新引入 Project/Task-first 导航、用一个通用 Dashboard 代替全部专业 Workspace、把 Business Engineering 改成 Agent/Capability/Tool 开发，或把 Capability 冒充工程交付物。

完整业务模拟至少覆盖相关的拒绝、失败、延迟、重试或取消路径之一；涉及数据库变更时另核 fresh/upgrade convergence、integrity 和 foreign-key 约束。
这些是既有业务 Review 标准的保留，不要求本轮文档任务运行产品模拟。
历史 Product Reset 的精确迁移门只在该范围且未被合法替代时适用，不把旧 BLOCKED_PENDING_BUSINESS_RUNTIME_BLUEPRINT 自动恢复成全部工作的当前 Gate。
