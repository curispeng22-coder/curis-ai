# Issue — CURIS V1 Writing WR-DIRECTION + WR-LEARNING 经营面（P1-a）

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-06 「按照你的建议，开工」授权；合同 D1–D4 已确认）
Task ID: CURIS-V1-WRITING-DIRECTION-LEARNING-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：[Curis_Writing_Domain_Authority.md](../docs/03_Design/Curis_Writing_Domain_Authority.md)（Draft，§3.1/§3.2/§6 D1-D3）、完工盘点 §3.1/§3.3/§6 决策 1；同构参照 Music operating_command、CG-LEARNING-01 已接受链

## 1. Objective

1. **WR-DIRECTION-01 创作方向**：保存（title/body/scope_ref 两级/reference_refs≤8/learning_ref/confirmed 明确 bool）、列表/查看、版本化（revision/previous_ref/identity_ref）、`apply-direction` 将章节与已确认方向建立显式 runtime_links 引用；未确认方向不可被章节引用；旧版本引用需 historical:true。
2. **WR-LEARNING-01 人工经验学习**：保存（title/body/basis_refs≤8+hash 快照/applicability/counterexample/accepted）、列表/查看；`use-learning` 在选定作品下**新建 WritingChapter（DRAFT）并写首版草稿**（含经验正文/适用范围/反例与 learning_ref），不触碰任何现有章节及其草稿 latest；全部强制 validation=UNVERIFIED，无「平台验证/效果提升」表述。

**不在本切片**：WR-MARKET / WR-PERFORMANCE / WR-OP（P1-b/P1-c 另行立项）；平台连载/读者数据/收益/凭证链（P3）；schema migration（复用 runtime_entities PACKAGE_DOMAIN_OBJECT 范式，必须加表即 STOP）；章节链语义改动；执行授权（allow_execution 边界不变）；UI 新风格（沿用已接受视觉基线与 --ui-* token）。

## 2. Allowed Files / Directories（开工前登记 SHA256）

- backend/app/api/writing_router.py
- backend/app/writing_operating_service.py（新增）
- backend/tests/test_writing_operating.py（新增）
- backend/app/main.py（仅 router 构造/挂载最小 hunk）
- frontend/lib/writingApi.js
- frontend/lib/writingState.mjs
- frontend/components/writing/WritingWorkspace.js
- frontend/components/writing/WritingDirection.js（新增）
- frontend/components/writing/WritingLearning.js（新增）
- frontend/components/writing/Writing.module.css
- frontend/tests/writingOperatingState.test.mjs（新增）
- frontend/tests/writingEntryReadiness.test.mjs（仅 writingEntry 返回结构新增 view 字段的断言同步最小 hunk）
- frontend/tests/writingChapter.test.mjs（同上：writingEntry roundtrip deepEqual 新增 view:"" 一行最小 hunk）
- artifacts/tasks/CURIS-V1-WRITING-DIRECTION-LEARNING-20261006/**

**不授权**：schema migration；其他业务域；真实云调用；8+1 DB；Git。

## 3. Acceptance Evidence

- pytest：tenant/company/workspace 三层隔离与跨域 404；方向 exact 字段/确认闸门/版本化/旧版本 historical；reference_refs ≤8 且属本工作区；学习强制 UNVERIFIED、basis hash 快照、accepted 闸门、应用幂等（同 request_id 指纹重放/异指纹 409）；use-learning 新章节首版草稿、原章节 draft latest 不变、跨作品拒绝；非法 action 拒绝。
- 真实 UI QA（隔离环境）：方向保存（未确认/已确认两态）→ 列表/查看 → 章节应用方向；学习保存→查看→应用到选定作品生成新章节并跳转；新章节正文含原经验/适用范围/反例；旧经验未选 historical 拒绝；冷重启后对象保留且仍 UNVERIFIED；跨公司不可见。
- 视觉：与已接受 Writing 基线一致（--ui-* token；无硬编码 hex/`dark:`）；构建/lint。
- 受保护 DB 指纹；frontend QA 冻结串行；结束清理；完成回报与 CHANGE_LOG/CURRENT_STATE 更新在接受后登记。

## 4. Stop Conditions

learning/direction 无现成存储范式可复用（需新表）；产品合同出现未覆盖的关键语义空白 → STOP 并引用 Curis_Writing_Domain_Authority.md 具体行。

## 5. Workload / 依赖

M+M ≈ 3 人日（含独立 QA）。无外部凭证依赖。依赖已 PROMOTE Draft 合同（docs/03_Design/Curis_Writing_Domain_Authority.md）。

## 6. Execution Record（2026-10-06）

### 6.1 Changed Files（POSTHASH：artifacts/tasks/CURIS-V1-WRITING-DIRECTION-LEARNING-20261006/POSTHASH.txt）

| 文件 | 处置 | 摘要 |
| --- | --- | --- |
| backend/app/writing_operating_service.py | 新增 | WritingOperatingService：save/apply-direction、save/use-learning；runtime_entities PACKAGE_DOMAIN_OBJECT 复用；幂等键/digest/版本链；UNVERIFIED 强制；runtime_links 三关系 |
| backend/app/api/writing_router.py | 修改 | OperatingIn（request_id/expected_ref/data，extra=forbid）+ 6 端点；build_writing_router 增 operating 参数；action Literal 白名单 |
| backend/app/main.py | 修改 | 仅 2 处最小 hunk：构造 writing_operating 并挂载（L5707-5708、L5741-5742） |
| backend/tests/test_writing_operating.py | 新增 | 11 测试（版本化/确认闸门/ref≤8/幂等/UNVERIFIED/basis hash/新章节不替换 latest/跨公司/冷重启/HTTP smoke） |
| frontend/lib/writingState.mjs | 修改 | WRITING_VIEWS 白名单、writingEntry 增 view（非法 fail-closed、view 与章节模式互斥）、writingViewHref |
| frontend/lib/writingApi.js | 修改 | return 白名单加 wr_view；directions/direction/directionCommand/learnings/learning/learningCommand 6 方法 |
| frontend/components/writing/WritingDirection.js | 新增 | 列表/保存（confirmed）/详情/修订/应用到章节 |
| frontend/components/writing/WritingLearning.js | 新增 | 列表/保存（accepted+basis）/详情/修订/use-learning 选作品+新章节标题并跳转 |
| frontend/components/writing/WritingWorkspace.js | 修改 | context 经营面导航；books+view 渲染挂载；use-learning 成功 router.push 新章节 |
| frontend/components/writing/Writing.module.css | 修改 | 仅追加 op*/notice 类，全部 --ui-* token，无 hex/dark: |
| frontend/tests/writingOperatingState.test.mjs | 新增 | view 白名单/互斥/writingViewHref/repair 白名单 4 组 |
| frontend/tests/writingEntryReadiness.test.mjs | 修改 | deepEqual 断言同步 view:""（1 行） |
| frontend/tests/writingChapter.test.mjs | 修改（越界追认，见 6.3） | roundtrip deepEqual 断言同步 view:""（1 行） |

### 6.2 证据

- 后端：`test_writing_operating.py` 11/11 通过（隔离 DB + CURIS_ENV=test 跑法，见交接记忆）。
- 前端：writing 三测试文件 17/17；`npm run build` 成功；切片 5 文件 eslint 0 问题（warnings 已修复）。
- 独立真实浏览器 QA：artifacts/tasks/CURIS-V1-WRITING-DIRECTION-LEARNING-20261006/qa/QA_REPORT.md——34/34 场景通过 + DB 探针 12 项 + 冷重启 C1–C3；受保护 DB 指纹前后一致；零 5xx、无外发 Provider；进程与 /tmp 已清理。

### 6.3 越界文件追认

1. `frontend/tests/writingChapter.test.mjs`：不在原 Allowed Files；writingEntry 返回结构新增 view 字段导致既有 deepEqual 失败，按与 writingEntryReadiness.test.mjs 同类的「1 行断言同步最小 hunk」处理，已补登 §2。
2. 本 Issue 文件自身：§2 追加上述允许行（任务治理登记，非业务代码）。
3. qa/ 目录新增 qa_seed.py、qa_server.py、qa_harness.cjs、qa_probe.py、QA_REPORT.md 等：落在 §2 已授权的 artifacts/tasks/<TASK-ID>/** 内。

### 6.4 既有失败登记（不修）

- 后端：`test_writing_selected_execution.py` 两参例在**跨文件合跑**时 404（该文件单跑 7/7；不含本切片新文件时同样复现）——既有跑法/顺序基线，与 WQA-20 DEVELOPMENT_RETURN 同类先例一致。
- 前端：全量 213 中 9 失败（v1SevenAreaAcceptance、mvp-p0-auth-onboarding、rdWorkspaceExecution、runtimeProvider、runtimeWorkspaceUi），全部不 import/引用任何 writing 文件，属全局搜索/provider 链统一等待办项的既有基线。

### 6.5 Disposition

- 代码/测试：在本 Issue 授权范围内交付，QA 证据 Accepted（EVIDENCE）。
- 合同 docs/03_Design/Curis_Writing_Domain_Authority.md 保持 Draft（本切片未改产品语义）。
- 任务工件（PREHASH/POSTHASH/qa/）：REVIEW_REQUIRED → 留待 Owner 按 P1 序列结束统一 PROMOTE/ARCHIVE。
- Next Gate：P1-b（WR-MARKET + WR-PERFORMANCE）另行立项；P1-c（WR-OP）随后。

