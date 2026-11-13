# CURIS V1 视觉基线生产落地 — 总控实现 Issue

Status: Review
Authority Class: CURRENT / IMPLEMENTATION ISSUE（总控编排）
Disposition: ALL SLICES ACCEPTED（S1–S6 + X1/X2 治理闭合，2026-10-06）
Task ID: CURIS-V1-VISUAL-BASELINE-IMPLEMENTATION-20261005
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
Created: 2026-10-05
Source: artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/development-return/FORMAL_IMPLEMENTATION_ISSUE_DRAFT.md（Owner 已口头批准 PROMOTE）

## 1. Objective

把 CEO 已接受的 V1 视觉基线（FINAL_UI_HANDOFF 2026-10-05；52 路由 = 19 确认 + 33 衍生）实现进生产前端（Next.js 16 / Tauri 2）。控件只绑既有 canonical API/Runtime；复用已接受 runtime 基础；不复制 P002 原型 mock/session.js；不以旧前端视觉为默认。视觉接受 ≠ 功能验收 ≠ Desktop 验收 ≠ 发布授权。

本 Issue 只做**编排、顺序、切片授权**；不重复 D0/D1/Writing/Settings/CG/Music 已有 Issue 的实现细节与 QA 轨迹。

## 2. Authority 输入（只读）

- AGENTS.md → CURIS_CURRENT_ENTRYPOINT → PRODUCT_DOCUMENT_POINTER Current Required → Product Blueprint / Master Map / UI Blueprint / 适用 Frozen Authority
- 视觉基线：artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/design-delivery/ 六文件 + P002 sealed src（仅视觉参考）
- 实现真相：CURRENT_STATE、development-return/READINESS_INVENTORY.md、FRONTEND_AND_PACKAGING_INVENTORY.md、D0/D1/Writing/CG/Music/Settings Issue 与 Review

## 3. Owner 已裁定（2026-10-05，锁定）

1. **双主题**：`light`（默认；浅中性底 + 紫 `#806BE5` 主色 / `#5B469E` 文字行动）+ `dark`（暗底 + 绿 `#32f08c`，保留现有暗色 token 值）；`system` 随 OS。语义色跨主题一致。Frozen Spec 文档同步与否由 Owner 另行裁定，本 Issue 不改 Frozen 文档。
2. **Nav 宽度 = 190/158px**（D0 实现值；220 属被 Frozen Shell 新模型取代的旧两区模型）。孤儿 token `--ui-sidebar-w: 220px` 在 S1 内改 190 或删除。
3. **编排方式**：本 Issue 为总控；D0/D1/Writing/Settings/CG/Music Issue 独立保留，由本 Issue 引用排队。

## 4. 汇合关系

| 现有 Issue | 关系 |
|---|---|
| CURIS-V1-DELIVERY-D0-FRONTEND-001 | S1 前置：独立 QA retest 通过后才进入 S2 |
| CURIS-V1-DELIVERY-D1-FRONTEND-001 | S1/S4 汇合语义，QA 先行 |
| CURIS-V1-DELIVERY-WRITING-001 | S3 前置：QA 封存后作为 WR 扩散基线 |
| CURIS-V1-CG-PRODUCT-ENTRY-001 | S3 内执行，沿用其 27 路径 grant |
| CURIS-V1-MUSIC-PRODUCT-ENTRY-001 | S3 内执行，沿用其 28 路径 grant |
| CURIS-V1-SETTINGS-FORMAL-INTEGRATION-001 | S2 汇合，QA 收口 |

## 5. 切片顺序（Handoff §5）

S1 共享壳 → S2 全局八区 → S3 三业务 → S4 跨区域公共项/全状态 → S5 构建打包（另授权运行）。每切片开工前在本 Issue 追加该切片 exact-file allowlist + prehash 表；未列入文件零修改。

## 6. S1 — 共享桌面壳收口（本切片已授权）

### Allowed Files（S1 exact-file allowlist，prehash 见 development-return/S1_PREHASH.json）

| 文件 | 拥有的改动范围 |
|---|---|
| `frontend/app/globals.css` | `:root`/`[data-theme]` token 值重组为双主题；语义色跨主题统一；`--ui-sidebar-w` 220→190（或删除并清理引用）；不改布局规则/桥接块/admin 块 |
| `frontend/tailwind.config.js` | 仅当 token 名增减时的映射同步 |
| `frontend/components/workspace/WorkspacePaneShell.js` | 不改（Nav 190/158 已正确）；仅如需引用修正 |
| `frontend/components/workspace/WorkspacePaneShell.module.css` | 硬编码色/尺寸改 token 引用 |
| `frontend/components/v1/V1Sidebar.js` | 不改结构；`w-[190px]` 保持；如有硬编码色改 token 类 |
| `frontend/components/assistant/GlobalAssistant.js` | 不改行为；如有硬编码色改 token |

### S1 验收证据

- 双主题在 1440×900 与 1280×800 下：light=浅底紫主色、dark=暗底绿主色、system 随 OS；切换无残影
- 四栏开合/Resizer/窄幅 overlay/Utility dialog 焦点回归
- 全 owned 文件无新增硬编码 hex；`--ui-sidebar-w` 引用一致
- posthash 与 prehash diff 仅限本 allowlist

### S1 明确不做

不改业务数据/API/Runtime；不新增 Dark 专属设计（P2）；不做 1024 以下；不动 backend/desktop/DB；不动他人 dirty hunks。

## 7. 受保护数据与运行规则

任何 dev/build/打包运行前指纹：`backend/curis.sqlite`、`backend/data/curis.sqlite`、`backend/tests/data/curis.sqlite`、`data/{curis,quality,issue_pipeline,b_layer_pending_decisions}.sqlite` 及默认 App DB；全部测试用仓库外隔离数据根；禁止 migrate/init/seed 受保护库；异常即 STOP。根目录 `<app.database...>` 18 条目与 `"backend` 目录不触碰。

## 8. Exclusions（本 Issue 永不授权）

真实云模型/Provider 调用与费用；外部平台授权/发布/回执；Obsidian/飞书接入；Keychain/凭据；schema 新 primitive/DDL（除 CG/Music 已批）；发布/分发；Git stage/commit/push/reset/clean/stash。

## 9. Stop 条件

Authority 冲突；scope 越界；受保护数据变化；真实费用/发布风险；身份/租户隔离疑点；D0 QA 未过即进 S2。回滚仅用 prehash preimage 精确还原 owned hunks。

## 10. 验收级别（始终分列）

视觉基线已接受 / 实现须生产前端+runtime 证据 / 功能验收由独立 QA 用隔离真实数据 / Desktop 须 fresh 包+隔离 root+restart / 发布另治理。开发者自测不算独立 QA。

## Task Output Manifest

| 输出 | Disposition |
|---|---|
| issues/CURIS-V1-VISUAL-BASELINE-IMPLEMENTATION-20261005.md（本文件） | ACTIVE / 总控 |
| development-return/S1_PREHASH.json | EVIDENCE |
| development-return/S1_POSTHASH.json | EVIDENCE（2026-10-05 追加） |
| development-return/S1_RETURN.md | REVIEW_REQUIRED（S1 完成回报；待独立 QA 视觉回证 + D0 R2 retest + filled primary 对比度裁定） |

### S1 完成登记（2026-10-05）

S1 代码变更完成，仅 3 文件（globals.css / tailwind.config.js / WorkspacePaneShell.module.css），其余 3 个 allowlist 文件零改动。双主题与 Nav 190 已落地；详见 S1_RETURN.md。S1 状态：READY_FOR_INDEPENDENT_QA / NOT ACCEPTED。

### S1 Owner 接受登记（2026-10-05）

Owner Verdict：**ACCEPTED（S1 切片）**。依据：独立 QA 报告 development-return/S1_QA_REPORT.md（CONDITIONAL PASS：双主题 token、system 随 OS、Nav 190/158 三处对齐、硬编码 hex 零残留、四栏静态+单测闭环；24+3 张截图）+ Owner 浏览器视觉回证（S1_RETURN.md §2.1）。

接受边界与附带裁定：
1. filled primary `#806BE5` + 白字实测 4.08:1（QA 实测值），低于 Frozen §6 4.5:1——Owner 接受该组合作为已接受视觉基线的字面实现；正文级阅读行动使用 `--ui-action-primary-text`（`#5B469E`）。完整对比度回归列入 S4 a11y。
2. QA 范围外发现 Q1（`D1.module.css` L101 dark 适配 AND 条件）——Owner 裁定**并入 S2 修复**（exact hunk，仅条件拆分，色值不动）。
3. 接受仅限 S1 token/双主题/Nav 切片；不是 whole-product / Desktop / Runtime 接受。

前置更新：D0 R2 与 R3 final-01 均已有 Owner 接受记录（2026-10-04，见 CURIS-V1-DELIVERY-D0-FRONTEND-001.md），总控 §4 的 D0 retest 前置**已闭合**。

## 11. S2 — 全局八区视觉组合（本切片已授权，2026-10-05）

Owner 授权：接受 S2_PREHASH_DRAFT.md 12 文件 allowlist，并追加 #13 `organizationCenter.module.css` 与 #14 `D1.module.css`（仅 Q1 owned hunk）。正式 prehash：development-return/S2_PREHASH.json（14 文件，实施前复核一致）。

### S2 Allowed Files（exact-file allowlist）

| # | 文件 | 拥有的改动范围 |
|---|---|---|
| 1 | `frontend/app/ceo-office/page.js` | hash 哨兵，预期零改动（D1Surface 包装归 D1 Issue） |
| 2 | `frontend/components/v1/CeoDeskOperating.js` | CEO 工作台卡片布局/间距/语义类/token 替换；不动 v1FrontendApi/runtimeApi/writingApi/musicApi 调用与状态机 |
| 3 | `frontend/app/ceo-office/business/page.js` | 业务空间视觉组合；不动 runtimeApi 调用 |
| 4 | `frontend/app/ceo-office/organization/page.js` | 仅默认导出视觉 token/类名；`LegacyOrganizationPage` 命名导出冻结不动 |
| 5 | `frontend/app/ceo-office/organization/OrganizationCenter.js` | 组织三视图卡片/状态点视觉；不动 organizationProjection/runtimeApi/useRuntime/href 构造 |
| 6 | `frontend/app/ceo-office/talent-market/page.js` | 人才与能力入口视觉组合；不动 roleLabel/API |
| 7 | `frontend/app/ceo-office/analytics/page.js` | 仅默认导出视觉；`LegacyOperatingPage` 命名导出冻结不动 |
| 8 | `frontend/app/ceo-office/analytics/OperatingIntelligence.js` | 概览/探索/报告三 tab 视觉；不动 getOperatingIntelligence/submitOperatingReportDecision/STATE_COPY/TABS |
| 9 | `frontend/app/ceo-office/knowledge/page.js` | 资料库入口视觉组合；不动 API/搜索参数 |
| 10 | `frontend/app/ceo-office/meeting/page.js` | 会议入口视觉组合；不动 API/回调 |
| 11 | `frontend/app/ceo-office/settings/page.js` | 仅视觉 token/类；六分类 GET/PUT 接线冻结（SETTINGS Issue 治理） |
| 12 | `frontend/components/terra/TerraShell.js` | 面包屑/顶栏/链接色/返回链接类；不透传协议/return_to/context 机制 |
| 13 | `frontend/app/ceo-office/organization/organizationCenter.module.css` | 配合 #5 的 token/双主题视觉；不新增第二套主题 |
| 14 | `frontend/components/delivery/d1/D1.module.css` | **仅 L101 Q1 hunk**：把 `@media(prefers-color-scheme:dark)` 与 `:global(html[data-theme=dark])` 的 AND 条件拆分为独立 `[data-theme=dark]` 规则 + system-dark 媒体分支；色值与其余所有选择器不动 |

### S2 明确不做

不动 API/业务逻辑/Runtime 调用；不动 Legacy 命名导出；不动 Settings 接线；不动 D1Surface/SharedConversation/ResultReferenceView；不接 mock/session.js；不新增一级路由；不重开 S1 文件；子路由页（员工详情/资料详情/记忆等）留 S4；不改 Frozen 文档；Git 写操作仍禁止。

### S2 验收证据

- 八区在 1440×900 与 1280×800 下 light/dark/system 三态视觉与基线一致，无 OS=light 时 dark 不生效类缺陷（Q1 回归）
- 全 owned 文件新增硬编码 hex 检查；#4/#7 Legacy 导出 byte 冻结
- posthash 与 prehash diff 仅限 14 文件 allowlist；#1 若改动即 STOP
- 独立 QA 报告（不由开发自测替代）

## Task Output Manifest（续）

| 输出 | Disposition |
|---|---|
| development-return/S1_QA_REPORT.md + shots/（27 张） | EVIDENCE（S1 独立 QA，CONDITIONAL PASS） |
| development-return/S2_PREHASH_DRAFT.md | SUPERSEDED_BY_S2_PREHASH_JSON（草案保留 provenance） |
| development-return/S2_PREHASH.json | EVIDENCE（S2 授权 14 文件 prehash） |

### S2 实施完成登记（2026-10-05）

开发回报：development-return/S2_RETURN.md + S2_POSTHASH.json + s2-preimages/。14 文件中 7 文件改动（#2/#3/#8/#9/#10/#13/#14），7 文件冻结（#1/#4/#5/#6/#7/#11/#12，hash pre=post）。Q1 修复精确为 #14 L101→L101-102，8 个色值逐字保留。ESLint exit 0；未跑 dev/build/DB；无 Git 写操作。开发自评 READY_FOR_INDEPENDENT_QA / NOT ACCEPTED。

### S2 独立 QA 登记（2026-10-05）

Verdict：**PASS**（0 P0/P1；3 项 P2 观察）。报告：development-return/S2_QA_REPORT.md（74 张截图 shots-s2/、diff 校验脚本、computed style 采样、Q1 双路取证）。

- 静态：14 文件 hash 独立复算一致；改动行仅 className/CSS；API/href/onClick/中文文案零改动；#4/#7 Legacy 冻结；裸 hex/dark: 变体零新增。
- 运行时：8 路由 × 2 视口 × 4 态 = 64 矩阵截图，无白屏/编译错误，11 个 token ×64 样本零偏差，32 组横向溢出巡检通过；Q1 回归 8/8（OS=light+强制 dark 实测 D1 root bg=#202129；system 两方向正确）；控制台仅 :8000 离线类错误，切片回归类 0。
- P2-1：#13 间距吸附实际 22 处（开发回报低估），均在授权内且落 4px 网格。
- P2-2（登记 S4）：后端离线，四个数据态（组织三视图/会议真实徽章/DT 报告列表/CeoDesk 主视图）像素目验待联调环境补双主题回归。
- P2-3（登记 S4）：`text-ui-cyan` 实值 light=紫/dark=绿（S1 映射既有事实），会议"等待结果"徽章 light 呈紫非青，真青色诉求归 S4 token/a11y。

S2 状态：QA PASS，**待 Owner 接受裁定**；P2-2/P2-3 登记 S4 不阻塞。

## 12. S3 盘点登记（2026-10-05，待 Owner 四项裁定）

盘点报告：development-return/S3_INVENTORY_DRAFT.md（只读，零代码改动）。对总控既有认知的更正：

1. **CG / Music 已实施**（非"未实施/grant pending"）：两 Issue 内有 2026-10-05 激活 grant 与 HANDOFF；磁盘另有两个后续 Issue——CG-FOUR-FORM-INTERACTION-001（21 路径 P1 候选，CEO 已暂停，视觉迁移留给 S3 决策）与 MUSIC-OPERATING-CHAIN-001（独立 QA PASS_WITH_LIMITS，未见 Owner 接受）。三线功能实施**均无 Owner 最终封存**。
2. 专业区 28 路由实算：PRESENT 4 / PRESENT*（未封存）4 / PARTIAL 7 / NOT PRESENT 13；derived 实算 **18 而非 19**（口径差异待 Owner 裁定）。13 个无生产面路由严禁造占位页，应登记功能 backlog。
3. 挂载机制核实：唯一挂载页 installed/[workspaceId]/page.js → InstalledWorkspaceRuntime L280-282 按 package 分发；衍生页只能是 query 视图状态/surfaces.json 声明，不新增一级路由。
4. 视觉债：JS 零 hex；CSS Writing 0、CG 2、Music 22 处/11 色（含偏离基线 `#6653c4/#5745b0/#53607e`，dark 不翻转）。S3 为 S2 同口径纯视觉组合，不需新建 token；lib/state/runtime/测试/后端不入 allowlist。
5. 建议子切片：S3a=Writing 4 文件（唯一有 Owner bounded 接受+完整 QA）；S3b=CG 3 文件；S3c=Music 3 文件；prehash 候选见草案 §4（授权时复算）。

待 Owner 四项裁定（见盘点报告末尾）：
- ① Writing QA 封存口径（WQA-20 留存登记）后是否授权 S3a
- ② S3b/S3c 是否"视觉不等待功能补测、视觉后 bytes 为功能侧新基线"
- ③ 13 个 NOT PRESENT 面登记功能 backlog + 18/19 口径
- ④ runtime/state/api 确认不入 S3 allowlist

## 13. Owner 裁定登记（2026-10-06，"全部按建议执行"）

1. **S2 接受**：Owner Verdict **ACCEPTED（S2 切片）**。依据 S2_QA_REPORT.md PASS（0 P0/P1）+ S2_RETURN.md/S2_POSTHASH.json。边界：仅限八区视觉组合；P2-1（#13 间距 22 处）、P2-2（四个数据态待联调补验）、P2-3（text-ui-cyan 实值问题）登记 S4；不是 whole-product / Desktop / Runtime 接受。
2. **S3 四项裁定**（对应盘点报告决策项）：
   - ① Writing「QA 封存」口径确认：WRITING-001 bounded 接受 + WQA-20 登记为 S3 不关闭的留存项 → **S3a 授权**。
   - ② S3b/S3c「视觉组合不等待功能补测、视觉后 bytes 为功能侧新基线」**确认**，但每子切片独立独立 QA；CG P1 候选/Music 功能状态不被视觉 hunk 关闭或继承。
   - ③ 13 个 NOT PRESENT 面登记**功能 backlog**（S3 不造占位页）；derived 口径按实算 **18**（CG5/WR6/MU7）。
   - ④ InstalledWorkspaceRuntime.js 与各 *State.mjs/*Api.js/测试/后端**不入** S3 任何 allowlist。

## 14. S3a — Writing 视觉组合（本切片已授权，2026-10-06）

正式 prehash：development-return/S3A_PREHASH.json（2026-10-06 复算一致；preimage 封存 s3a-preimages/writing/）。

| # | 文件 | 拥有的改动范围 |
|---|---|---|
| 1 | `frontend/components/writing/WritingWorkspace.js` | 作品库/责任区/书架视觉类名与版式；不动 create/assign/command/load 与 entry 构造 |
| 2 | `frontend/components/writing/WritingChapterMain.js` | tab/编辑器/检查区/候选卡片视觉组合；不动 run()/事件名/WRITING_CHECKS/ConversationComposer 接线 |
| 3 | `frontend/components/writing/WritingPublishingMain.js` | 发布包表单/历史列表视觉；不动 command 调用与 LOCAL_DOWNLOAD 语义 |
| 4 | `frontend/components/writing/Writing.module.css` | 视觉规则 token 化/基线对齐；19 处 hex 均为 var() 回退值，保留回退并核对 S1 token |

覆盖：WR-BOOKS-01、WR-CHAPTER-01（全）；WR-NEWBOOK-01、WR-SERIAL-01 仅现有 PARTIAL 载体视觉组合，不补功能。冻结：writingApi.js、writingState.mjs、InstalledWorkspaceRuntime.js、writing*.test.mjs。

### S3a 明确不做

不动 API/状态机/href/query 键/中文文案关键语义/package 身份/测试；不新增一级路由或页面文件；不暗示"已连载/有收益"（WR-SERIAL 为章节级本地包语义）；不改 globals.css/tailwind.config.js；无 Git 写操作；diff 超出 4 文件即 STOP。

### S3a 验收证据

- 三态（light/dark/system）× 1440×900/1280×800 视觉与基线一致；独立 QA 报告；posthash diff 仅限 4 文件。

### S3a 独立 QA 登记（2026-10-06）

Verdict：**PASS**（0 P0/P1；4 项 P2 观察）。报告：development-return/S3A_QA_REPORT.md（35 选择器 × 31 token × 7 态 computed style 采样；7 张截图 shots-s3a/）。

- 静态：4 文件 hash 独立复算一致；3 个 JS pre=post=preimage 零改动；CSS diff 16 行逐行审查通过；20 处 hex 均在 var() fallback；token 逐一核对存在。
- 运行时：dev 编译零错误；harness 三态采样 light=紫系/dark=绿系/system 双向正确。
- P2-1：行高吸附（1.8→1.7 等）未在回报中披露，QA diff 发现。
- P2-2：outline-offset 3px→2px 未逐项披露。
- P2-3：hex 计数口径差异（19 vs 20）。
- P2-4：真实 workspace 像素目验受后端离线限制，登记 S4 联调补验。

S3a 状态：**待 Owner 接受裁定**。

## 15. S3b — CG 视觉组合（已授权，2026-10-06）

依据 §13-② 裁定"视觉组合不等待功能补测"授权。正式 prehash：development-return/S3B_PREHASH.json；preimage：s3b-preimages/content-growth/。

| # | 文件 | 拥有的改动范围 |
|---|---|---|
| 1 | `frontend/components/content-growth/ContentGrowthWorkspace.js` | 列表/新建/通知条/原请求链接视觉；不动 perform/load/cgEntry/href |
| 2 | `frontend/components/content-growth/ContentGrowthMain.js` | 编辑器/引用区/候选采用区/四形态 utility 视觉组合；**不实施 FOUR-FORM P1 label 候选**；不动 operate/send/adopt/选择校验 |
| 3 | `frontend/components/content-growth/ContentGrowth.module.css` | 视觉规则；2 处独立 hex（`#fff1ed/#973f35`）换语义 token；var 回退值核对 |

明确不做：8 个 NOT PRESENT 面不得造占位页；不实施 FOUR-FORM P1；不改 state/api/测试/InstalledWorkspaceRuntime。

### S3b 独立 QA 登记（2026-10-06）

Verdict：**PASS**（0 P0/P1；3 项 P2 观察）。报告：development-return/S3B_QA_REPORT.md（54 选择器 × 41 token × 7 态采样；7 张截图 shots-s3b/）。

- 静态：3 文件 hash 一致；JS diff 仅 className/span 包装；FOUR-FORM P1 label 候选逐字保留未实施；4 处裸 hex 全在 var() fallback；token 逐一核对存在。
- 运行时：dev 编译零错误；harness 三态 light=紫系/dark=绿系/system 双向正确。
- P2-1：间距/字号/圆角吸附差分未逐项披露（合规）。
- P2-2：新增样式项（editor header align-items 等）视觉差分影响未列。
- P2-3：真实数据态像素目验受后端离线限制，登记 S4 联调补验。

S3b 状态：**待 Owner 接受裁定**。

## 16. S3c — Music 视觉组合（已授权，2026-10-06）

依据 §13-② 裁定授权。正式 prehash：development-return/S3C_PREHASH.json；preimage：s3c-preimages/music/。

| # | 文件 | 拥有的改动范围 |
|---|---|---|
| 1 | `frontend/components/music/MusicWorkspace.js` | 目录/经营 8 视图框架/context/utility 视觉；不动 musicEntry/operatingEntry/perform/MusicOperatingMain 表单提交逻辑 |
| 2 | `frontend/components/music/MusicMain.js` | 四 tab/歌词双栏/候选卡/播放器/确认 dialog 视觉；不动播放器时钟状态机、selection、save/operate、master 确认契约 |
| 3 | `frontend/components/music/Music.module.css` | 视觉规则；**22 处独立硬编码（11 色，含 `#6653c4/#5745b0/#53607e`）须全部 token 化并通过 dark 三态**；forced-colors/reduced-motion 块保留 |

明确不做：不关闭 Music 功能 QA 状态；不改 state/api/测试/bundle；MU-RELEASE/PERFORMANCE 仅现有 PARTIAL 载体视觉组合。

### S3c 独立 QA 登记（2026-10-06）

Verdict：**PASS**（0 P0/P1；4 项 P2 观察）。报告：development-return/S3C_QA_REPORT.md（7 态 × 33 采样点 × 16 token；7 张截图 shots-s3c/）。

- 静态：3 文件 hash 一致；2 个 JS byte 级零改动；CSS 选择器集合零增删；22 处独立硬编码（11 色）全部 token 化（25 行对照表逐条核对属实）；forced-colors/reduced-motion 块逐字保留；裸 hex 剥离 var() 后零残留。
- 运行时：dev 编译零错误；三态采样全绿（light=紫系/dark=绿系/system 双向正确）；hover 实触发与 ::backdrop 双态正确；9 个旧色 RGB 在 7 态采样中 legacyHits 全空；dark 关键对比度 11.37/7.56/5.96/13.01:1 均 ≥4.5。
- P2-1：3 处值中性微改动未逐条披露（tabs 底边别名等价；notice/confirm fallback 移除）。
- P2-2：.error 新增 1px danger border（已披露，盒模型 +2px）。
- P2-3：dark .error danger on surface-2 = 3.08:1 < 4.5:1，沿用 S1 全局 token，登记 S4 a11y。
- P2-4：真实 workspace 像素目验受后端离线限制，登记 S4 联调补验。

S3c 状态：**待 Owner 接受裁定**。

### S3 汇总（2026-10-06）

S3a（Writing，1 CSS）/ S3b（CG，3 文件）/ S3c（Music，1 CSS）全部独立 QA PASS，0 P0/P1。P2 共 11 项全部不阻塞（披露不充分类 + 后端离线数据态补验 + 2 项对比度登记 S4 a11y）。三切片待 Owner 统一接受。

### S3 Owner 接受登记（2026-10-06）

Owner Verdict：**ACCEPTED（S3a/S3b/S3c 三切片）**。依据三份独立 QA 报告（S3A/S3B/S3C_QA_REPORT.md，均 PASS、0 P0/P1）。Owner 授权规则更新（2026-10-06）：纯工程判断由交付线自行推进，仅三类事项上报 Owner——①产品方向多选一、②视觉/排版方案确认、③外部资源需求（API key 等）。S3 接受属工程确认，按此规则直接登记。

边界：仅限视觉组合层；功能接受状态不变（CG P1 候选暂停、Music 经营链 QA 未接受、WQA-20 留存均不被本接受关闭）；11 项 P2 登记 S4；非 whole-product/Desktop/Runtime 接受。

**S4 启动授权**：依据同一规则，S4（跨区域公共项 + 全状态 + a11y/52 路由回归）直接推进。S4 中涉及**改色/改字/对比度方案选择**的项（如 dark .error 3.08:1、text-ui-cyan 实值）属视觉确认类，将在 S4 盘点后单独报 Owner 选择；纯工程回归项直接执行。

### S4 视觉裁定登记（2026-10-06，Owner 已裁定）

1. **dark .error 对比度（S3c P2-3）→ 调亮**：dark 主题 error 文字 token 值上调至与 `--ui-surface-2` 底对比 ≥4.5:1；仅改 `[data-theme=dark]` 一个 token 值，light 主题与选择器不动。实施归 S4 allowlist（globals.css dark error token hunk），由独立 QA 实测对比度回归验收。
2. **text-ui-cyan 实值（S2 P2-3）→ 保持主题紫/绿**：不新增真青 token；会议"等待结果"徽章维持 light=紫 / dark=绿的主题行动色映射（S1 已接受）。该项关闭，无后续改动。
3. filled primary 4.08:1 维持 S1 已接受裁定（§10），不重开。
4. **V5 D1 dark 适配（2026-10-06）→ S4 内完成**：授权 D1.module.css 二次入册，内部组件浅主题硬编码色全部 token 化并随 dark 主题翻转；S2 Q1 hunk（L101-102）与其 8 个保留色值逐字冻结。
5. **V4 ComposerShell 七件（2026-10-06）→ Owner 授权占位控件**：前端控件为三段选择器/徽章/开关等标准 UI 模式，无需额外开源依赖；后端语义（授权模型 API、工作模式状态机、Auto 调度器）不在 S4 范围。S4 内实现占位态（disabled/置灰 + "即将推出"标注），接受对当前不可点状态的视觉如实表达；功能实现由后续独立 Issue 闭环。
6. **V6 dark warning 对比度（2026-10-06，S4 E8 新发现）→ 调亮**：dark 主题 `--ui-warning`（#b57708，实测 on dark 底 ≈4.11:1）与 V1 同口径上调至 ≥4.5:1；仅改 `[data-theme=dark]` 与 system-dark 媒体分支两处作用域的 token 值，light 冻结。globals.css S4 owned 范围相应扩展为 V1+V6 两个 hunk。
7. **V7 存量语义色对比度（2026-10-06，S4 E8 全量采样）→ 调深至达标**：四组 S1 存量 token 上调至 ≥4.5:1——light success（3.37/3.11）、light warning（3.75/3.45）、light danger（4.38/4.04）、dark success on surface-2（3.99）；每组须对 surface 与 surface-2 双底实测。globals.css S4 owned 范围扩展为 V1+V6+V7 三个 hunk；filled primary 4.08:1 维持 V3 闭合不重开。light 主题已验收截图基线相应更新（QA delta 重拍受影响组件）。

## 17. S4 — 跨区域公共项 + 全状态 + a11y + 52 路由回归（本切片已授权，2026-10-06）

依据：Owner 2026-10-06 授权规则（纯工程直接推进）+ S4 视觉裁定（§16 后登记，V1 调亮 / V2 保持 / V3 闭合 / V4 占位控件已授权 / V5 批准）。盘点：development-return/S4_INVENTORY_DRAFT.md。正式 prehash：development-return/S4_PREHASH.json（2026-10-06 复算 25 文件全一致）；preimage 封存：s4-preimages/（25 文件）。

### S4 Allowed Files（25 文件 = 组A 6 + 组B 6 + 组C 9 + 组D 2 + 条件项 2）

共同 owned 范围：className/语义类/CSS 视觉规则（间距/字号/圆角/色值→token）。共同不拥有：API 调用与 DTO、href/query 键、状态机/reducer、中文文案关键语义、package 身份、测试、后端、InstalledWorkspaceRuntime、`*State.mjs/*Api.js`、admin/control 面、legacy 并行入口、13 个 NOT PRESENT 面（严禁占位页）。

各文件 owned 范围与 role（owned/sentinel/conditional）逐条见 S4_PREHASH.json。要点：
- 组A：SharedConversation（含 E5：发送按钮 `text-white`→`text-ui-primary-fg`；含 V4：Composer 占位控件——访问权限/工作模式/Auto 三件 disabled/置灰 + "即将推出"标注，不动 onSubmit/controls slot 契约/showVoice/模型选择逻辑）、ResultReferenceView（三屏对齐共享状态形态）、RuntimeStates（哨兵）、SharedEmployeeWorkArea、EmployeeConversation、GlobalAssistant。
- 组B：D1 五 JS 视觉类 + D1.module.css（V5：内部组件 dark token 化；L101-102 Q1 hunk 与 8 色值逐字冻结）。
- 组C：employees(+[id])、knowledge entries/[id]、memory、reports(+[id])、capabilities 哨兵、capabilities/[type]/[id]、ModelManagement；英文 key 直出仅登记不改文案。
- 组D：TerraPrimitives、TerraConfirm（哨兵）；TerraState 仅 E7 证据不入册。
- 条件项：globals.css 仅 V1 hunk（dark error/danger 文字 token 值上调至 ≥4.5:1，light 与其余 token 逐字冻结）；tailwind.config.js 哨兵（V1 无 token 名增减，预期零改动，改动即 STOP）。

### S4 工程项登记

- E1–E4（披露口径类）：闭合，无改动。
- E5：Composer 发送按钮对比度修复（组A #1 owned hunk）。
- E6：52 路由扩展回归截图矩阵（已组合面复核 + 子路由 + D1 四 view + ResultReferenceView；light/dark/system × 1440×900/1280×800）。
- E7：状态组件并存核对（仅取证，不合并）。
- E8：语义色全量对比度采样自动化；新发现 <4.5:1 组合一律转视觉确认类上报，不自行改色。
- X1/X2：数据态联调目验需 backend :8000 + dev 运行授权；运行前按 §7 指纹受保护 DB，测试用隔离数据根；纯本地无外部费用。X3：无外部资源需求。

### S4 验收证据

- posthash 与 S4_PREHASH.json diff 仅限 25 文件；哨兵/conditional-sentinel 零改动。
- D1.module.css diff 中 L101-102 与 8 个保留色值逐字一致。
- E6 截图矩阵 + E8 对比度采样报告 + V1 dark error 实测 ≥4.5:1。
- 独立 QA 报告（不由开发自测替代）；X1/X2 数据态目验截图（联调窗口内）。
- ESLint 对改动 JS exit 0；无 Git 写操作。

### S4 明确不做

不动 admin/control 面与 legacy 入口；不合并状态组件；不集中化 Employee Status 投影（登记功能 backlog）；Composer 三控件按 V4 裁定实施占位（已落地）；不造 NOT PRESENT 占位页；不关闭 CG P1/Music 经营链/WQA-20 功能状态；不改 Frozen 文档。

### S4 STOP 条件（在 §9 之上补充）

开工复算 hash ≠ S4_PREHASH.json → STOP；diff 触及共同不拥有清单 → STOP；V4 未确认而动 Composer 控件位 → STOP；发现候选文件被其他 ACTIVE Issue grant 覆盖且口径冲突 → STOP 报 Owner；X1/X2 运行前未指纹受保护 DB → STOP。

### S4 独立 QA 登记（2026-10-06）

Verdict：**PASS**（0 P0 / 0 P1 / 1 P2 保留；V7 delta 后 E8 全量闭合）。报告：development-return/S4_QA_REPORT.md（129 张截图 shots-s4/、E8 采样 s4-qa-e8-results.json + s4-qa-e8-sample.cjs、V7 delta 小节）。

- 静态：25 文件 posthash 独立复算一致；preimage 全对；globals.css 仅 V1+V6+V7 三个授权 hunk（dark/system-dark + light 语义色值），filled primary #806BE5 逐字冻结；D1.module.css L101-102 Q1 hunk 与 8 色值逐字一致；哨兵（tailwind.config.js/RuntimeStates/TerraConfirm/capabilities page）零改动；裸 hex 剥离 var() fallback 后零残留。
- V1 验收：dark danger on surface-2 = 4.82:1 ✓。V6 验收：dark warning #c98f1f on surface 5.45:1 / surface-2 4.77:1 ✓；D1 .attempt dark 5.45:1 闭合 ✓。V7 delta 验收：light success 5.08/4.68、light warning 5.09/4.69、light danger 5.12/4.72、dark success 5.30/4.64（surface/surface-2，全 ≥4.5）✓；E8 全量闭合。
- V4 占位控件：三件 disabled/aria-disabled + 「即将推出」标注、无真实 onClick，取证通过。
- E6：52 路由有生产面全量 × 三主题 × 双视口截图矩阵零白屏/编译错误/横向溢出；Q1 回归通过。
- 唯一保留 P2（X1/X2）：受保护库无业务数据 + 隔离副本启动触发迁移冲突 → 数据态像素目验登记保留，待联调窗口（需隔离数据根灌入真实业务数据 + 迁移冲突由后端治理）。

### S4 Owner 接受登记（2026-10-06）

Owner Verdict：**ACCEPTED（S4 切片，含 V7 delta）**。依据 S4_QA_REPORT.md PASS（0 P0/P1，V7 delta 后 E8 全量闭合）+ 2026-10-06 授权规则（QA 通过后的接受属工程确认，直接登记）。边界：仅限视觉组合层与跨区域公共项；唯一保留项 X1/X2 数据态目验不随本接受关闭；功能状态不变（CG P1 暂停、Music 经营链 QA 未接受、WQA-20 留存、Composer 三控件功能 backlog）；非 whole-product/Desktop/Runtime 接受。

S1–S4 全部切片至此 ACCEPTED。S5 构建打包另授权。

### S4-QA-1（X1/X2 唯一保留 P2）联调窗口进展登记（2026-10-06）

治理 Issue：issues/CURIS-V1-X1X2-STARTUP-MIGRATION-FIX-20261006.md（Disposition: **ACCEPTED / CLOSED**，2026-10-06）。R1 独立 QA Verdict：**CONDITIONAL PASS**（报告 development-return/X1X2_QA_REPORT.md）——迁移冲突修复与启动/灌数/指纹维度全过（同库 5 次 cold start 零 PackageConflictError、37 张截图质量项全绿、四 GET 200 含真实条目、8+1 受保护 DB 指纹零变化）；**四数据态页数据维度未目验**（GAP2：quickstart 灌数不含 FOUNDING_RUN/CEO_ASSISTANT，前端 runtime bootstrap 公司列表为空，/ceo-office→/welcome、org/meeting 永久 loading、reports=mock）。处置（工程判断直接推进）：R2 补灌 founding-run 基底（canonical API：founding-runs → transitions → materialize-company，零代码改动，/tmp 隔离根）后由独立 QA 复验四数据态像素维度；GAP1（DT reports=0，无 canonical 生产路径）维持 backlog 登记不阻塞。

**S4-QA-1 闭合登记（2026-10-06）**：R2 补灌成功（materialized company-x1x2r2-bf494d25「X1X2 联调目验公司」，bootstrap 唯一可见，2部门/10员工/3业务/3 knowledge/真实会议含 decision）+ R2 独立 QA **PASS（GAP2 闭合）**（报告 development-return/X1X2_QA_REPORT_R2.md，27/27 截图全过：/ceo-office 不再 302→/welcome、org/meeting 脱离 loading 呈现真实数据、reports 维持诚实 mock；8+1 受保护 DB 指纹零变化；零仓库改动/Git 写/真实云调用）。**S4-QA-1 闭合**，S4 切片（含 X1/X2 数据态目验）至此全部 ACCEPTED。GAP1（DT reports=0）维持 backlog 不阻塞。

## 18. S5 — 构建打包（Desktop / Tauri 2）（本切片已授权，2026-10-06）

授权依据：Owner 2026-10-06「按这个方案执行」（覆盖 S5 构建打包 + X1/X2 联调窗口治理）。性质：**构建运行授权，预期零源代码改动**；构建因代码缺陷失败即 STOP 回报，修复另行授权。

### S5 Allowed Operations

1. 运行前指纹 §7 受保护 DB 全清单；并从 `desktop/runtime/*.py` / 启动配置确认默认 App DB 落盘位置，一并指纹登记（§7 遗留项收口）。
2. `desktop/` 下 `pnpm build`（= `scripts/build-runtime.sh` + `CURIS_SKIP_RUNTIME_BUILD=1 tauri build --bundles app`）；其后 `pnpm build:dmg`（`scripts/build-manual-dmg.sh`）。
3. 构建环境变量按脚本既有契约使用（`NEXT_PUBLIC_API_BASE=http://127.0.0.1:8080` 由脚本内嵌）；`CURIS_ALLOW_BUILD_NETWORK` 默认不设——若 PyInstaller 缓存或 Rust 工具链缺失须 STOP 上报（外部资源类）。
4. 覆写性产物目录（构建输出，非源码改动）：`desktop/.runtime/`、`desktop/target/`、`frontend/.next/`、`frontend/node_modules/`、`desktop/node_modules/`。

### S5 Allowed Files（改动类）

无。任何源代码/构建脚本/tauri.conf.json 改动即 STOP。证据输出至 `artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/development-return/`：`S5_BUILD_EVIDENCE.md`、`S5_POSTHASH.json`（受保护 DB 指纹复算）。

### S5 验收证据（打包证据 ≠ Desktop 验收）

- 构建 exit 0；产物清单（`.app` / `.dmg` 绝对路径、大小、SHA256）；`BUILD-MANIFEST.json` 内容存档。
- 受保护 DB 指纹运行前后一致；无 Git 写操作；无真实云模型调用/费用。
- 独立 QA Desktop 验收随后执行：fresh 包 + 隔离 app-data root 启动 + restart + 窗口/主题/路由冒烟；Browser 证据不替代 Desktop 证据。

### S5 明确不做

不签名/公证/发布/分发；不动受保护 DB 与根目录 18 个异常条目；不修构建中发现的代码缺陷；不改 Frozen 文档；不触碰 X1/X2 治理（由独立 Issue 闭环）。

### S5 构建完成登记（2026-10-06）

构建成功：`pnpm build` 与 `pnpm build:dmg` 均 exit 0。产物：`desktop/target/release/bundle/macos/Curis.app`（458,201,479 B，主二进制 SHA256 `c7d85eff…2754d`）与 `desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg`（216,737,419 B，SHA256 `0f31ff03…9aa026`）；未签名/未公证（identity: None）。包内 runtime 五件套 + frontend/server.js 齐全。指纹：8 个受保护 DB + 默认 App DB（`~/Library/Application Support/com.curis.desktop/data/curis.sqlite`，lib.rs 落盘规则确认）共 9 项 pre/post SHA256 零变化。证据：development-return/S5_BUILD_EVIDENCE.md、S5_POSTHASH.json、s5-build.log（437 行）。零源码改动、零 Git 写操作。打包证据 ≠ Desktop 验收——独立 QA（fresh 包 + 隔离 app-data root + restart）随后执行。

### S5 独立 QA 登记（2026-10-06）

Verdict：**PASS**（1 项证据采集 BLOCKED + 1 项观察 F1）。报告：development-return/S5_QA_REPORT.md + shots-s5/（3 张）+ s5-qa-prehash/posthash.txt。

- 隔离 root 可用：`desktop/src/lib.rs` L35-48 存在 `CURIS_DESKTOP_DATA_ROOT` 覆盖，全程以 /tmp/curis_s5_qa 启动，默认 App DB 零触碰。
- 静态验收全过：包结构/runtime 五件套/frontend server.js/BUILD-MANIFEST 齐全；Info.plist = com.curis.desktop / 0.1.0；arm64；DMG verify VALID 可挂载、主二进制 hash 与构建证据一致。
- 运行时全过：冷启动 15s 就绪；窗口在屏 1440×901（配置 1440×900，标题 "Curis — CEO Office"）；:8080/:8002/:3010 全 200；welcome 渲染与 system→dark→light 主题冒烟通过（CDP/浏览器级像素证据）；restart 5s 就绪、锁正常释放、隔离 DB 持久。
- 指纹：9 项 SHA256 复算零变化。零 Git 写、零源码改动；/tmp/curis_s5_qa 已清理，进程全 kill。
- BLOCKED 子项：screencapture OS 级窗口截图与窗口标题运行时文本——宿主无 macOS 屏幕录制/辅助功能 TCC 权限（系统级，全应用标题均被 redact）。运行时证据已由 CDP 级覆盖，OS 级截图待宿主授权后补，不影响验收结论。
- F1 观察：dark 主题下 no-company 空态主内容区未翻转（sidebar 已暗底绿 accent）——登记为主题覆盖缺陷，另起小切片治理（S6）。

### S5 Owner 接受登记（2026-10-06）

Owner Verdict：**ACCEPTED（S5 切片）**。依据 S5_QA_REPORT.md PASS + 2026-10-06 授权规则（QA 通过后的接受属工程确认，直接登记）。边界：Desktop 验收通过（fresh 包 + 隔离 root + restart）；不等于发布授权（未签名/未公证/未分发）；BLOCKED 子项为宿主权限类证据缺口；F1 缺陷另行治理不随本接受关闭。

## 19. S6 — F1 缺陷治理：入口流（AppEntry）dark 主题翻转（本切片已授权，2026-10-06）

授权依据：S5 QA F1 登记「另起小切片治理（S6）」+ Owner 2026-10-06「按这个方案执行」视觉确认收尾（V1 dark error 调亮与 V2 cyan 维持已于 §16 裁定并在 S4 闭合，本条无新增改色）。F1 属 dark 主题合规缺陷（应翻转而未翻转），非视觉方案多选一，按授权规则工程判断直接推进，完成后告知影响。

### 根因（只读核实，2026-10-06）

`frontend/components/v1/AppEntry.js`（Welcome / EmptyCuris / Setup / error / loading 五分支）全量使用硬编码 hex + Tailwind `dark:` 变体；而 `tailwind.config.js` 未配置 `darkMode`（默认 media 策略，随 OS prefers-color-scheme），与本项目 `data-theme="light|dark|system"` 属性 + `--ui-*` token 机制脱钩。用户手动选 dark 而 OS 为 light 时：token 组件（V1Sidebar）正确翻转，`dark:` 类区域不翻转 → S5 实证「sidebar 已暗、主内容区浅底白卡」。该文件为 S1–S5 allowlist 未覆盖的治理盲区。

### S6 Allowed Files（改动类）

| # | 文件 | owned 范围 |
|---|---|---|
| 1 | `frontend/components/v1/AppEntry.js` | 五分支视觉类全量 token 化：硬编码 hex / `dark:` 变体 → `bg-ui-bg` / `bg-ui-surface` / `bg-ui-surface-2` / `text-ui-txt(-2/-3)` / `border-ui-line` / `bg-ui-primary` / `hover:bg-ui-primary-dark` / `text-ui-primary-fg` / `text-ui-primary-text` / `bg-ui-primary-soft` / `text-ui-red` / `shadow-ui-2/3` 及 S3b 已接受 `color-mix(--ui-danger …)` error 组合先例；头像 PRESETS 色板（`style={{background,color}}` 内容数据，非 UI 表面色，不随主题翻转）保留并登记为例外。**零行为改动**：不动 founding-run 创建链 / presentation 存取 / runtime 分支逻辑 / 路由跳转 / 表单校验与 240KB 上限 |

其余文件零改动。globals.css / tailwind.config.js 本切片**不动**（无新 token 需求）；backend / desktop / Frozen 文档 / 受保护 DB 不在范围。

### S6 验收证据

- AppEntry 各可达态（welcome / empty 空态含 sidebar / setup 表单 / setup error 提示）× light / dark / system（CDP emulate 双向）× 1440×900 / 1280×800 截图矩阵：无白屏/编译错误/横向溢出；dark 下主内容区与 sidebar 同步翻转（F1 闭合直接证据）；`--ui-*` computed 值逐张命中主题实值。
- 改动文件剥离 var() fallback 后裸 hex 扫描 = 0（PRESETS 四组头像色板为例外登记项）；无新增 `dark:` 写死色类；pre/post SHA256 登记。
- 独立 QA 执行并出报告；受保护 DB 指纹不变；零 Git 写、零真实云模型调用。

### S6 明确不做

不改主题机制本身（不加 `darkMode` class 策略、不改 layout.js data-theme 流）；不动 V1Sidebar 等已 token 化组件；不改 Frozen 文档；不处理 S5 BLOCKED 子项（宿主 TCC 权限，待 Owner 授权后补证）；不扩大为入口流功能改动。

### S6 独立 QA 登记（2026-10-06）

Verdict：**PASS（F1 闭合）**。报告：development-return/S6_QA_REPORT.md + shots-s6/（16 张 + probe-results-s6.json）；开发回报：development-return/S6_RETURN.md。

- 静态：AppEntry.js POST SHA256 `9823120f…9e0b` 与开发声明一致；剥离 PRESETS 例外行后裸 hex=0、`dark:` 变体=0；行为逻辑零改动。
- 像素矩阵 **16/16 全过**（welcome/empty/setup × light/dark × 双视口 + system 抽样 4 张）：dark 下 empty 态 main=rgb(26,28,31)、卡片=rgb(34,37,41)，sidebar 与主区同主题（F1 闭合直接证据）；setup 主按钮 dark 绿 #32f08c + 深前景；无白屏/编译错误/横向溢出/状态串台；system 双 emulate 正确。
- 环境事实（非产品缺陷）：backend CORS 默认白名单仅 :3000/:3001（本次以 `CURIS_ALLOWED_ORIGINS` env 扩展）；presentation 按 tenant+ceo 键存取。
- 清理：8018/3018 已 kill，/tmp 隔离根已删；零仓库外改动、零 Git 写、未触受保护 DB。

### S6 Owner 接受登记（2026-10-06）

Owner Verdict：**ACCEPTED（S6 切片，F1 闭合）**。依据 S6_QA_REPORT.md PASS + 2026-10-06 授权规则（QA 通过后的接受属工程确认，直接登记）。边界：仅入口流视觉层；S5 BLOCKED 子项（宿主 TCC 屏幕录制权限补证）不随本接受关闭。
