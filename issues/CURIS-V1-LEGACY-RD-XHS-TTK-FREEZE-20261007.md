# CURIS V1 — Legacy RD/XHS/TTK 旧 business_type 链冻结隐藏

- **Task ID**: CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007
- **Backlog**: Execution Backlog「legacy 清理（RD/XHS/TTK）」；紧接 Global Object Search（CURIS-V1-GLOBAL-OBJECT-SEARCH-20261007）之后
- **Date**: 2026-10-07
- **Authority Class**: REVIEW / IMPLEMENTATION（执行前为 Issue；验收证据见 §6）
- **Owner**: Main Development
- **Next Gate**: 独立 QA → Owner 接受

## 1. Background / Product Authority

**产品模型（真相）**：[CURIS_V1_PRODUCT_FREEZE.md](../docs/reviews/CURIS_V1_PRODUCT_FREEZE.md)（Frozen / CEO FINAL）规定 V1 Business 范围仅 **Content Growth（内容增长）、Writing（写作）、Music（音乐）**；**RD 与 E-commerce 范围外**；并明确「此范围决定**不删除历史工作**」「未批准的业务/导航区不进 V1」。

[CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md](../01_Product/CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md)（CEO ACCEPT WITH CORRECTIONS）确立 `Business → Platform → Account` 层级：小红书 / 抖音 / 公众号是「内容增长」业务内的**平台层**，不是独立业务。

**实现现状（差距）**：代码中残留**旧模型**——把 `RD / XHS / TTK` 当作三种 `business_type`，各配专用办公室页：

- `frontend/app/ceo-office/workspace/software/page.js`（RD，渲染 `components/rd/RdWorkspacePhaseTwo.js`）
- `frontend/app/ceo-office/workspace/xhs/page.js`（XHS，渲染 `components/xhs/XhsWorkspacePhaseOne.js`）
- `frontend/app/ceo-office/workspace/shortvideo/page.js`（TTK，渲染通用 `WorkspaceRuntimeView businessType="TTK"`）
- 路由中枢 [runtimeApi.js `workspaceOfficeHref()`](../frontend/lib/runtimeApi.js#L358-L369) 仍把 RD/XHS/TTK 映射到上述旧页。

现行 V1 新建业务只返回 content_growth / writing / music 三个 package（[frontend_v1_router.py business_definitions](../backend/app/api/frontend_v1_router.py#L328-L337)），落为 `business_type=PACKAGE` → `/ceo-office/workspace/installed/[id]`；**新建业务不会再产生 RD/XHS/TTK**，旧页只服务历史旧数据，属 backlog 登记的「legacy route escapes」。后端 RD codex-cli 执行硬门（`RealRDExecutor`、main.py rd 段、rd_workflow_runtime、dev_agent、issue_pipeline 等）为历史执行链。

### CEO 产品裁定（2026-10-07，本轮）

1. **RD（研发）与 TTK（抖音电商）链**：冻结并隐藏 V1 入口；**代码全部保留**（遵守 Freeze 不删历史），不接线新分派器；旧数据直接 URL 仍可读但须标注 V1 范围外。
2. **旧 XHS 专用页**：与 software/shortvideo **一并冻结隐藏**（旧 business_type 专用页性质相同）。小红书作为「内容增长」内**平台层**的现行能力（PACKAGE installed 工作面、content_growth 链）**不受影响**。
3. **5 个 legacy 失败测试**：随旧链冻结标注 skip + 原因，不再挂红；回归失败基线由 48 调整为 **43**（本次唯一经批准的基线变更，须集合 diff 证明仅减这 5 项）。

## 2. Allowed Files / Directories

**前端（仅以下文件）**：

- `frontend/lib/runtimeApi.js`（**仅 hunk**：`workspaceOfficeHref()` 移除 RD/XHS/TTK→旧页映射，旧类型回落通用工作空间入口；新增并导出纯函数 `isLegacyOfficeType(type)` 与常量 `LEGACY_OFFICE_TYPES`；PACKAGE→installed 行为字节级不变）
- `frontend/app/ceo-office/workspace/page.js`（**仅 hunk**：对 legacy business_type 不渲染会自环的「进入专业工作面」按钮，改为诚实冻结提示；PACKAGE/GENERIC 路径不变）
- `frontend/components/workspace/LegacyOfficeScopeNotice.js`（**新增**：单一无依赖提示组件，仅用 `--ui-*` token，文案「该业务类型不在 CURIS V1 范围内，专业工作面已冻结；历史数据保留只读」，三处旧页复用）
- `frontend/app/ceo-office/workspace/software/page.js`、`frontend/app/ceo-office/workspace/xhs/page.js`、`frontend/app/ceo-office/workspace/shortvideo/page.js`（**仅 hunk**：在 Suspense 内容顶部挂载 `LegacyOfficeScopeNotice`；原组件保留仍渲染）
- `frontend/tests/runtimeWorkspaceUi.test.mjs`（更新 L33-37 映射断言为新行为 + 新增 `isLegacyOfficeType` / PACKAGE 不变断言；L53-56 旧页文件存在性断言保留）

**后端（仅测试标记，零业务代码改动）**：

- `backend/tests/test_rd_workflow_real_rd.py`（仅对 `TestScenarioA_PositivePath::test_a4_real_executor_modifies_target_a` 加 `@unittest.skip(reason)`）
- `backend/tests/test_mvp_phase5_s8_rd_template.py`（仅对 `test_real_development_task_writes_tests_and_records_git_diff`、`test_failed_model_output_marks_workflow_and_task_failed` 加 skip）
- `backend/tests/test_mvp_phase5_s9_content_template.py`（仅对 `test_real_content_task_persists_copy_svg_and_retrospective`、`test_invalid_model_output_marks_run_and_task_failed` 加 skip）
- skip reason 统一引用：`"Legacy RD/XHS/TTK business_type chain frozen out of V1 (CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007, CEO decision 2026-10-07)"`

**任务与登记**：

- `artifacts/tasks/CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007/**`
- 本 Issue、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`（仅追加）

**禁止**：删除/重写任何后端 app 业务代码（RealRDExecutor / rd_workflow_runtime / main.py rd 段 / runtime/workspace.py 旧校验 / dev_agent / issue_pipeline / content_workflow_runtime 一律冻结不动）；删除三个旧页或其组件；改动 content_growth / writing / music PACKAGE 链、installed 工作面、studio、TaskLauncher、CeoDeskOperating、TerraNavData；数据库 schema/写路径；产品/Frozen 文件；Git 写；前端硬编码 hex。

## 3. 验收证据 / Acceptance Evidence

1. **路由中枢纯函数**（单测）：
   - `workspaceOfficeHref({business_type:"PACKAGE",workspace_id:"w"})` 仍为 `/ceo-office/workspace/installed/w`（不变）。
   - `business_type` 为 RD/XHS/TTK 时返回通用 `workspaceEntryHref`（`/ceo-office/workspace?workspace_id=…`），**绝不**返回 software/xhs/shortvideo。
   - 其它/空类型行为不变；`isLegacyOfficeType("RD"|"XHS"|"TTK")` 为 true、PACKAGE/GENERIC 为 false（大小写不敏感）。
2. **V1 入口零旧链**（浏览器真实证据）：从 ceo-office 主导航、业务空间业务列表（business/page）、工作空间入口页（workspace/page）、新建业务流程，**无任何**链接/按钮指向 `/workspace/software|xhs|shortvideo`；新建业务仍只有内容增长/写作/音乐（含通用），无 RD/XHS/TTK 选项。
3. **工作空间入口页对旧类型诚实**：legacy business_type 工作空间不再出现自环的「进入专业工作面」按钮，改为冻结提示文案；PACKAGE「进入专业工作面」仍正确进入 installed。
4. **直接 URL 仍可读 + 范围外标注**：浏览器直接访问 `/ceo-office/workspace/software`、`/xhs`、`/shortvideo` 均仍渲染原组件（组件未删除），且顶部可见统一「V1 范围外 / 已冻结」提示条（--ui-* token，无硬编码色值）。
5. **现行能力零回归**：内容增长/写作/音乐 PACKAGE 业务从业务提案 → installed 工作面打开路径不受影响；相关前端测试零新增失败。
6. **后端测试标记**：上述 5 个测试以 skip（非 xfail、非删除）落地，reason 含 Task ID 与裁定日期；其余同文件测试不动。
7. **回归（IDENTICAL-FAIL-SET，批准的 5 项基线变更除外）**：
   - 后端全量：**43 failed / 1886 passed / 8 skipped**（原 48 failed / 1886 passed / 3 skipped）；集合 diff 证明新失败集 = 原失败集 **减去除这 5 个被 skip 的测试**，无任何其它增减。
   - 前端：9 个既有失败不变（零新增）；更新/新增的映射断言通过；eslint 0 error；生产 build 成功。
8. **独立 QA**：隔离 sqlite + 隔离端口 + forbidden 网关 + 真实浏览器：枚举现行 V1 入口零旧链；三旧页直链提示条；PACKAGE installed 正常打开；PREHASH=POSTHASH（仅 Allowed Files，后端 app 代码指纹 identical）；零 5xx；清理进程/端口//tmp。
9. **登记**：QA_REPORT + DEVELOPMENT_RETURN（含冻结清单与未删代码说明）+ Issue §6 + CURRENT_STATE + CHANGE_LOG。

## 4. Stop Conditions

- 发现需要删除/改写后端 app 代码或 PACKAGE 链才能隐藏入口 → STOP，回报，不扩大范围。
- 现行内容增长/写作/音乐链出现回归 → STOP，优先恢复，不带回归登记完成。
- 5 个测试 skip 后仍有其它失败集变化（非精确减 5）→ STOP，定位到根因再继续。
- 需要真实外部 Provider 才能验收 → 不做，如实标注 NOT RUN。

## 5. 工程约束

- 不 Git 写；中文汇报；后端测试 `CURIS_DB=CURIS_DB_PATH=CURIS_WORKSPACE_DB` 同隔离路径 + `PYTHONPATH=backend` + cwd=仓库根。
- QA 通过则在五处登记（QA_REPORT / DEVELOPMENT_RETURN / Issue §6 / CURRENT_STATE head / CHANGE_LOG tail）。

## 6. Execution Record

- **Date**: 2026-10-07 · **Status**: COMPLETE（独立 QA 通过，待 Owner 接受）
- **实现**:
  - `frontend/lib/runtimeApi.js`：`workspaceOfficeHref()` 删除 RD/XHS/TTK→software/xhs/shortvideo 映射；PACKAGE→installed 不变；新增导出 `LEGACY_OFFICE_TYPES` / `isLegacyOfficeType()`。
  - `frontend/components/workspace/LegacyOfficeScopeNotice.js`（新增，仅 --ui-* token，`data-legacy-office-notice`）。
  - `workspace/{software,xhs,shortvideo}/page.js`：在保留的 legacy 组件上方挂冻结提示。
  - `workspace/page.js`：legacy 类型详情卡显示冻结说明，不再给「进入专业工作面」自循环按钮。
  - `runtimeWorkspaceUi.test.mjs`：更新映射断言 + 2 个新测试。
  - 后端仅 3 个测试文件 +20 行 `@unittest.skip`（原因含 Task ID + CEO decision 2026-10-07），**app 代码零改动**。
- **证据**（[QA_REPORT.md](../../artifacts/tasks/CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007/qa/QA_REPORT.md) / [DEVELOPMENT_RETURN.md](../../artifacts/tasks/CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007/qa/DEVELOPMENT_RETURN.md)）：
  - 后端全量 **43 failed / 1886 passed / 8 skipped**（基线 48/1886/3）；失败集差集 = 恰好 5 个被 skip 的 legacy 节点，零新增。
  - 3 个目标测试文件 13 passed / 5 skipped。
  - 前端全量 223 tests / 214 passed / 9 failed（9 个为既有基线，净 +2 通过，零新增失败）；eslint 0 error；`next build` 成功，三个旧页与 installed 路由均保留。
  - 浏览器 QA：三条直链均显示范围外提示；/ceo-office、/business、/workspace 零旧链；business-definitions 仅返回 PACKAGE（无 rd/xhs/ttk）。
- **边界**: 后端 app 字节级未改，无需服务冷启重验；legacy 历史代码/页面/后端门全部保留；进程/端口//tmp 已清；无 Git 写。
