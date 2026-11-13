# Issue — CURIS V1 Writing WR-OP 经营投影只读面（P1-c）

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-07「继续，完成一阶段就继续下一项，持续」授权，承接 D3 顺序 P1-a✅→P1-b✅→P1-c；P1-a/P1-b 均已 QA PASS）
Task ID: CURIS-V1-WRITING-OPERATING-OVERVIEW-20261007
Recorded: 2026-10-07
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：[Curis_Writing_Domain_Authority.md](../docs/03_Design/Curis_Writing_Domain_Authority.md)（Draft，§1.5/§3.5/§4/§6 D3「S（诚实壳）」）；同构参照 Music 已接受经营只读链、本仓 P1-a/P1-b WritingOperatingService 已接受范式

## 1. Objective

**WR-OP-01 WritingOperatingView（经营投影，只读）**：一个只读聚合投影面，**不是数据源、无写动作、不新建聚合表**。聚合本工作区现有对象的当前状态，回答四问：

1. **方向是什么**：当前方向（每个 direction identity 的最新 revision 一行；如实带确认状态）。
2. **正在写什么**：作品及其章节、章节是否已有草稿（来自既有 workspace_package_objects + evolution_events，不新增统计）。
3. **积累了什么经验**：当前经验（每个 learning identity 的最新 revision 一行；带接受状态）。
4. **最新信号**：最新市场快照与最新表现观察（时点不可变记录，按时间倒序取最近 3 条；观察如实带「未连接」语义位，不新增任何平台数据）。

数据不齐时**逐块显示诚实空态**，不造 Mock、不隐藏 UNVERIFIED；投影只读，不提供任何保存/修订/应用按钮。

**语义约束**：
- 只读：仅 GET；不写 runtime_entities/runtime_links/evolution_events，不产生新对象。
- 复用：方向/经验「当前行」= 同 identity_ref 下 revision 最大的记录（沿用既有版本链读取）；快照/观察全部 revision=1 独立 identity，倒序取最近。
- 隔离：tenant/company/workspace 三层 scope，跨公司 404；read_only 入口状态如实透传。
- 投影中的 UNVERIFIED/接受/确认状态必须来自服务端记录真值，前端不可推断。

**不在本切片**：任何写动作/命令端点；新 schema 表或列；新 Surface/Dashboard；平台链（P3）；对既有五面对象模型的任何改动；分页/检索/统计图表（合同 S 诚实壳之外）；main.py 挂载（复用 P1-a 已挂 operating 实例，零改动）。

## 2. Allowed Files / Directories（开工前登记 SHA256，见任务区 PREHASH.txt）

- backend/app/writing_operating_service.py（新增 operating_overview 只读聚合方法 + 必要私有投影辅助）
- backend/app/api/writing_router.py（仅加 GET /operating/overview）
- backend/tests/test_writing_overview.py（新增）
- frontend/lib/writingApi.js（overview 只读方法）
- frontend/lib/writingState.mjs（WRITING_VIEWS 白名单加 overview）
- frontend/components/writing/WritingOverview.js（新增，纯只读）
- frontend/components/writing/WritingWorkspace.js（opNav 加 1 链接 + books+view 挂载）
- frontend/components/writing/Writing.module.css（仅现有类不够用时最小追加；预期零改动）
- frontend/tests/writingOperatingState.test.mjs（白名单断言扩 overview）
- artifacts/tasks/CURIS-V1-WRITING-OPERATING-OVERVIEW-20261007/**

**不授权**：schema migration；backend/app/main.py（零改动，若必须改即 STOP）；其他业务域；任何写路径；真实云调用；8+1 DB；Git。

## 3. Acceptance Evidence

- pytest（新文件，隔离 DB）：空工作区投影五块全空态且 200；种子书/章 + 方向多版本（仅最新 revision 进当前行，且 confirmed 真值）+ 经验多版本（accepted 真值）+ 快照 4 条（只回最近 3 条、总数 4）+ 观察 2 条；章节草稿状态来自 draft.saved 事件真值（无草稿章节 has_draft=false，保存草稿后 true）；投影调用前后 runtime_entities/runtime_links/evolution_events 计数零变化（只读）；跨公司 404；employee 可读（投影无写授权要求）；冷重启；HTTP smoke（GET 200、无 POST 路由→405、非法 wr 身份 404）。
- 真实 UI QA（隔离环境）：作品库上下文栏出现「经营投影」入口；空库五块逐块空态文案；播种后四块显示当前真值（方向显示已/待确认、经验显示已接受、快照/观察最近 3）；投影面无任何写控件；观察块带「外部平台未连接」；非法 wr_view fail-closed；跨公司不可见；冷重启。
- 视觉：沿用 op* 类与 --ui-* token（无 hex/`dark:`）；writing 单测全绿；build；切片文件 lint。
- 受保护 DB 指纹；frontend QA 冻结串行；结束清理；CHANGE_LOG/CURRENT_STATE 接受后登记。

## 4. Stop Conditions

聚合必须新表/新列才能完成；合同 §1.5/§3.5 出现未覆盖的关键语义空白；main.py 出现绕不开的改动；投影需要执行授权（allow_execution）→ STOP 并引用 Curis_Writing_Domain_Authority.md 具体行。

## 5. Workload / 依赖

S ≈ 1 人日（含独立 QA，诚实壳）。无外部凭证依赖。依赖 P1-a/P1-b 已 QA PASS 的 operating service/router/前端范式与全部五类记录。

## 6. Execution Record（2026-10-07）

### 6.1 Changed Files（POSTHASH：artifacts/tasks/CURIS-V1-WRITING-OPERATING-OVERVIEW-20261007/POSTHASH.txt）

| 文件 | 处置 | 摘要 |
| --- | --- | --- |
| backend/app/writing_operating_service.py | 修改 | 新增 `operating_overview` 只读聚合方法 + OVERVIEW_LATEST_LIMIT=3：单连接读 workspace_package_objects（书/章）、evolution_events（draft.saved 存在性，单条分组查询）、四类经营记录（`_get` 全量 hash 校验）；方向/经验按 identity_ref 取最高 revision 当前行；快照/观察按 created_at desc, entity_id desc 取最近 3；返回七块结构 entry/books/chapters/directions/learnings/snapshots/observations；零写入 |
| backend/app/api/writing_router.py | 修改 | 仅加 GET `/operating/overview`（FastAPI 无同径 POST，写请求 405） |
| backend/app/main.py | **零改动** | 复用 P1-a 已挂 operating 实例（POSTHASH 未列即未触碰） |
| backend/tests/test_writing_overview.py | 新增 | 9 测试（空态五块/书章草稿真值/方向当前版本+确认真值/经验当前+接受真值/快照 4 取最近 3/观察/严格只读三表计数不变/跨公司 404+employee 可读/冷重启/HTTP smoke 405+404） |
| frontend/lib/writingState.mjs | 修改 | WRITING_VIEWS 白名单加 overview |
| frontend/lib/writingApi.js | 修改 | overview 只读方法 |
| frontend/components/writing/WritingOverview.js | 新增 | 纯只读五块投影（作品章节/当前方向/最新经验/最新快照/最新观察），逐块空态、已/待确认与已/待接受真值徽标、UNVERIFIED 不隐藏、观察块外部平台「未连接」、4 个面跳转链接；无任何写控件 |
| frontend/components/writing/WritingWorkspace.js | 修改 | opNav 加「经营投影」链接；books+view 挂载 |
| frontend/components/writing/Writing.module.css | 修改 | 最小追加 .opSection/.opBlockHead 两结构类（全 --ui-* token，无 hex/dark:） |
| frontend/tests/writingOperatingState.test.mjs | 修改 | 白名单/href/repair/章节模式互斥断言扩 overview |

### 6.2 证据

- 后端：`test_writing_overview.py` **9/9**；与 P1-b/P1-a operating 测试合跑 **30/30**。
- 前端：writingOperatingState 4/4；全量 213 → 204 pass / 9 失败（P1-a 起登记的同集基线，不涉 writing）；`npm run build` 成功；切片 5 文件 eslint 0 问题。
- 独立真实浏览器 QA：[qa/QA_REPORT.md](qa/QA_REPORT.md)——浏览器 **S 段 19/19** + API 探针 **A1–A4 20 项** + 冷重启 **C1–C7**；3 截图；75 请求零 5xx（POST 200×11 全为探针播种、405×1 投影写拒绝、404×1 跨公司）；console/page/http 错误均 0。
- 受保护 DB 指纹前后 diff 为空；DB 探针证实无 overview 事件/无聚合表；无 Provider 外发；进程与 /tmp 已清理。

### 6.3 越界文件追认

无。全部变更落在 §2 Allowed Files；main.py 零改动；qa/ 工件在已授权 artifacts/tasks/<TASK-ID>/** 内。

### 6.4 既有失败登记（不修）

- 后端：test_writing_selected_execution.py 跨文件合跑 2 失败（单跑 7/7，顺序基线，WQA-20/P1-a/P1-b 先例）。
- 前端：全量 9 失败基线同 P1-a §6.4 登记，与本切片无关。

### 6.5 Disposition

- 代码/测试：在本 Issue 授权范围内交付，QA 证据 Accepted（EVIDENCE）。
- 合同 docs/03_Design/Curis_Writing_Domain_Authority.md 保持 Draft（本切片未改产品语义；五面已全部落地，Frozen 时机由 Owner 决定）。
- 任务工件（PREHASH/POSTHASH/qa/DEVELOPMENT_RETURN）：REVIEW_REQUIRED，留待 Owner 随 P1 序列统一 PROMOTE/ARCHIVE。
- Next Gate：Writing 五面收官（P1-a/b/c 全部 QA PASS）；继续 backlog：Music 经营链完整 QA → Composer 三控件 → GAP1 provider 泛化 → 全局搜索 → legacy 清理；平台链 P3。
