# Issue — CURIS V1 Content Growth 素材库独立面 + 人工经验学习面

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-06 盘点 §6 决策 5 授权）
Task ID: CURIS-V1-CG-REFERENCE-LEARNING-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：盘点 §3.1 CG-REFERENCE/LEARNING 行、§7-P0；产品依据 docs/03_Design/Curis_Content_Growth_Domain_Authority.md（L52、L56-74、L169-194）、Master Map L138-146

## 1. Objective

1. **CG-REFERENCE-01 素材灵感库独立面**：现状 reference_options 仅在采集编辑内勾选（content_growth_service.py 约 L144-151，≤8 引用）。新增独立素材库视图：浏览本工作区合法素材（collection contents/versions 现有数据）、按形态/标题/版本筛选、查看素材当前/固定/历史版本语义、勾选引用进草稿（沿用现有 reference spread/purpose/version_ref 语义，不新增 DTO 字段）。同名素材按 FOUR-FORM label helper 同口径区分（来源1/来源2 仅视图消歧）。若现有 collection 载荷不足以支撑列表，仅允许新增**只读**列表端点。
2. **CG-LEARNING-01 学习面（人工经验，强制 UNVERIFIED）**：仿 Music save-learning/use-learning 已接受模式新增 CG 经验：保存（标题/经验正文/basis 引用/适用范围/反例）、列表/查看、应用到新内容草稿（应用时固定原 basis 与范围、不默认替换 latest）；全部记录 verification_status=UNVERIFIED，无「平台验证/效果提升」表述。

**不在本切片**：channel_account/publish_receipt/analytics/MARKET/Opportunity schema 与任何平台凭证链（P3）；CG-OP/ANALYSIS；full CG 视觉迁移（另决策）；FOUR-FORM label hunks（已在 CURIS-V1-CG-FOUR-FORM-INTERACTION-001 授权内，本切片可消费其 helper 但不重复实现）；UI 新风格（沿用已接受视觉基线与 token）。

## 2. Allowed Files / Directories（开工前登记 SHA256）

- backend/app/api/content_growth_router.py
- backend/app/content_growth_service.py
- backend/app/content_growth_entry_service.py（仅 scope/复用最小 hunk）
- frontend/components/content-growth/**（新面组件允许新增于此目录）
- frontend/lib/contentGrowthState.mjs
- frontend/components/workspace/InstalledWorkspaceRuntime.js（仅挂载/入口最小 hunk，约 L280-282 区域）
- backend/tests/、frontend/tests/ content growth 相关测试（exact 文件开工登记）
- artifacts/tasks/CURIS-V1-CG-REFERENCE-LEARNING-20261006/**

**不授权**：schema migration（learning 持久化优先复用现有 knowledge/learning 存储范式；发现必须加表/加列→STOP 报产品/架构决策）；其他业务域；真实云调用；8+1 DB；Git。

## 3. Acceptance Evidence

- pytest：tenant/company/workspace 三层隔离与跨域拒绝；素材只读列表载荷与现有 collection 授权一致；引用 ≤8、kind/purpose 白名单、版本语义（当前/固定/历史/候选）；learning 强制 UNVERIFIED、basis 不可变、应用幂等、旧经验应用不替换 latest、缺失/歧义素材→来源需核对。
- 真实 UI QA（隔离环境）：素材库浏览/筛选/同名区分/引用进草稿/取消；学习保存→查看→应用到新内容；冷重启后对象保留且仍为 UNVERIFIED；跨公司不可见不可引用。
- 视觉：与已接受 CG 基线一致（`--ui-*` token；无硬编码 hex/`dark:`）；构建/lint。
- 受保护 DB 指纹；frontend QA 冻结串行；结束清理；完成回报与 CHANGE_LOG/CURRENT_STATE 更新在接受后登记。

## 4. Stop Conditions

learning 无现成存储范式可复用（需新表）；只读列表端点需要触碰 channel/account 模型；产品合同对素材库交互出现空白（Domain Authority 未覆盖的关键语义）→STOP 并引用具体合同行。

## 5. Workload / 依赖

M+M ≈ 3–4 人日（含独立 QA），P0 内最大切片，建议排其他三个之后。无外部凭证依赖。

## 6. Execution Record

Recorded: 2026-10-06

### 6.1 Changed Files（POSTHASH）

| 文件 | 状态 | SHA256 |
|---|---|---|
| backend/app/api/content_growth_router.py | DIFF | ddf1af29f5dd15054ff1d4deeef087e184898f83b2a7a5eff10bdf5b3954c05f |
| backend/app/content_growth_service.py | DIFF | e83b8c2112a414ca585ba97ed9610d5c3465c3f553e68b227576e0e18cc03c3d |
| frontend/lib/contentGrowthState.mjs | DIFF | e97e188b966c73ad4d48054b40e04c81ff05736f286e31c17bc527b8829c7b6c |
| frontend/lib/contentGrowthApi.js | DIFF（越界追认，不在 §2 Allowed Files；新增 materials/learnings/learningCommand 三方法 6 行） | 91eb4bcb7d468bdd19b582c4cb7365901918744ec1ec0fb7f6cc040340f33042 |
| frontend/components/content-growth/ContentGrowthWorkspace.js | DIFF | 547943bf25f2cd60a0dcf71d8fb896f20ece1935fcc725c7024d172d26285af8 |
| frontend/components/content-growth/ContentGrowthMaterials.js | NEW | 394344f4c25aad597e67556d3417e4b994d3f2fb14ddd273e38ae79e7e5f8e26 |
| frontend/components/content-growth/ContentGrowthLearning.js | NEW | f4baa401b0b74c5e28f81fb8dc5edd2b108a26ffebaebf27cb0a8bca75bf0c22 |
| frontend/components/content-growth/ContentGrowth.module.css | DIFF | 588322b5a53e875cc2f3ab34bb8930251072fb3d439cc442012390dd33076f13 |
| backend/tests/test_cg_reference_learning.py | NEW | 4dfc31bf45785d390a68d329b559cc7d435c20fc10f02dc31c3bfc89962b602b |
| backend/app/content_growth_entry_service.py | SAME | 7119fca5c4da6bb1e0aea56d0a671c2c38fdcb418763d35df18d768cf9fd76b9 |
| frontend/components/content-growth/ContentGrowthMain.js | SAME | c0a7dfe439e8ae0d249d4ce8600f98dac2ec553e44dade5ab90e6b369c54e9d9 |
| frontend/components/workspace/InstalledWorkspaceRuntime.js | SAME | 8309f98669f6f55895c9e108004bca079089b57823d4fb163ac3b4a11ff6432a |
| frontend/tests/contentGrowthEntryReadiness.test.mjs | SAME | 603b394bba9c318ca62494207f47ae991bf0a3fe776937e10a777c62a55c27ae |
| frontend/tests/contentGrowthFourFormInteraction.test.mjs | SAME | 8b0aa962c9d9f7b97d2d4d3cfd710d69037629a3278660c137c821f35a532d95 |
| backend/tests/test_cg_content_entry.py | SAME | d508e47c3dbe9399ebe97149c0950a899bc0913e1fb5caa1a4ee02987749f4d3 |
| backend/tests/test_cg_four_form_interaction.py | SAME | c169ab35e6e1ab007debf45b85735de5dcaf0042885309d606120c9ba0b164e7 |
| backend/tests/test_cg_selected_execution.py | SAME | 90804d3743be80fecdb73c9c86e4480a7ddadc38fb436799af1a0c05d01b0b5e |

### 6.2 越界追认

- `frontend/lib/contentGrowthApi.js`（§2 Allowed Files 未列）：新增 `materials()`、`learnings()`、`learningCommand(action, body)` 三方法，共 6 行，为 CG-REFERENCE-01 / CG-LEARNING-01 前端数据接口必需最小 hunk。请 Owner 追认。

### 6.3 QA 结果

- 独立真实浏览器 QA（Playwright + 隔离后端 8024 + 隔离前端 3023 + mock 网关）：12 场景（S1–S12）、35/35 布尔断言全 PASS、50 marks 全收集、0 console error / 0 page error / 0 HTTP error。
- DB 指纹：8 受保护表中 7/8 与 WQA-20 pre 逐字节一致；`data/issue_pipeline.sqlite` 不同但 mtime 20:26 < QA 开始 20:39，非本 QA 引入。
- 回归：后端 pytest（新增 23 断言 + 既有回归全绿）、前端单测（26/26 通过，含 cg_sources 新用例）、build 成功；lint 4 errors 既有基线登记不修。
- QA 修复的 3 缺陷：
  1. `contentGrowthState.mjs` cg_sources 解析与 >8 fail-closed。
  2. `ContentGrowthWorkspace.js` useEffect `ready` 引用顺序 bug（内联 `verifiedKey === entryKey`）。
  3. `ContentGrowthMaterials.js` 同名消歧缺少 contents 数组（改为并行 fetch collection）、引用进草稿 URL 序列化（`cg_sources`）。
- 报告：[QA_REPORT.md](../../artifacts/tasks/CURIS-V1-CG-REFERENCE-LEARNING-20261006/qa/QA_REPORT.md)、[DEVELOPMENT_RETURN.md](../../artifacts/tasks/CURIS-V1-CG-REFERENCE-LEARNING-20261006/DEVELOPMENT_RETURN.md)。

### 6.4 Disposition

**SLICE ACCEPTED（工程确认登记）**。P0 全部清零。
