# Issue — CURIS V1 Writing WR-MARKET + WR-PERFORMANCE 经营面（P1-b）

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-06 「开工」授权，承接 D3 顺序 P1-a→P1-b→P1-c；P1-a 已 QA PASS）
Task ID: CURIS-V1-WRITING-MARKET-PERFORMANCE-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：[Curis_Writing_Domain_Authority.md](../docs/03_Design/Curis_Writing_Domain_Authority.md)（Draft，§1.3/§1.4/§3.3/§3.4/§4/§6 D3）；同构参照 Music MarketSnapshot/Observation 已接受链、本仓 P1-a WritingOperatingService 已接受范式

## 1. Objective

1. **WR-MARKET-01 人工市场快照（WritingMarketSnapshot）**：动作 `save-snapshot`（人工录入）；exact 字段 `{title, body, period, source_note}`；`source_note` 必填非空（写明人工观察/编辑沟通/公开榜单阅读等来源说明）；服务端强制 `verification="UNVERIFIED"`，客户端传入 verification 拒绝；工作区级独立人工记录（无 scope_ref、无外发、无自动采集）。
2. **WR-PERFORMANCE-01 人工表现观察（WritingObservation）**：动作 `save-observation`（人工录入）；exact 字段 `{title, body, scope_ref, period}`；scope_ref 必须是本工作区内 WritingBook 或 WritingChapter（否则 404）；写 runtime_links `WRITING_OBSERVATION_SCOPE` 显式绑定；服务端强制 `verification="UNVERIFIED"`；视图固定展示外部平台数据位「未连接」（P3 前置，不做假接通）。
3. 两类记录均为**时点不可变记录**：每次保存产生新实体（revision=1、独立 identity），不提供编辑/版本链（expected_ref 必须为空串）；快照不修正历史，只追加新快照。

**不在本切片**：WR-OP 只读投影（P1-c）；平台连载/读者数据/收益/凭证链（P3）；schema migration（继续复用 runtime_entities PACKAGE_DOMAIN_OBJECT，必须加表即 STOP）；章节链语义改动；执行授权（allow_execution 边界不变）；UI 新风格（沿用 P1-a 已接受 op* 视觉类与 --ui-* token）；main.py 挂载（复用 P1-a 已挂的 operating 实例，本切片应零改动）。

## 2. Allowed Files / Directories（开工前登记 SHA256）

- backend/app/writing_operating_service.py
- backend/app/api/writing_router.py
- backend/tests/test_writing_market_performance.py（新增）
- frontend/lib/writingApi.js
- frontend/lib/writingState.mjs
- frontend/components/writing/WritingWorkspace.js
- frontend/components/writing/WritingMarket.js（新增）
- frontend/components/writing/WritingPerformance.js（新增）
- frontend/components/writing/Writing.module.css（仅在现有 op* 类不够用时最小追加）
- frontend/tests/writingOperatingState.test.mjs（扩 market/performance 白名单断言）
- artifacts/tasks/CURIS-V1-WRITING-MARKET-PERFORMANCE-20261006/**

**不授权**：schema migration；backend/app/main.py（P1-a 已挂 operating，无需改动；若发现必须改动即 STOP 上报）；其他业务域；真实云调用；8+1 DB；Git。

## 3. Acceptance Evidence

- pytest（新文件，隔离 DB）：快照 exact 字段/source_note 必填/period 边界/verification 服务端强制且客户端传入即 422/幂等（同 request_id 指纹重放、异指纹 409）；观察 scope_ref 作品与章节两类合法、跨工作区对象 404、WRITING_OBSERVATION_SCOPE 链接写入；两类记录 expected_ref 非空拒绝（不可变，无版本链）；tenant/company/workspace 三层隔离与跨公司 404；列表/详情读取与 payload hash 校验；冷重启重读；未知 action 422。
- 真实 UI QA（隔离环境）：快照保存→列表「人工录入 · 未验证」标识→详情；观察保存（分别绑定作品/章节）→列表/详情；外部平台位始终「未连接」；冷重启后记录保留且仍 UNVERIFIED；跨公司不可见；非法 wr_view fail-closed。
- 视觉：沿用 P1-a 已接受 op* 类与 --ui-* token（无硬编码 hex/`dark:`）；前端 writing 单测全绿；build；切片文件 lint。
- 受保护 DB 指纹；frontend QA 冻结串行；结束清理；完成回报与 CHANGE_LOG/CURRENT_STATE 更新在接受后登记。

## 4. Stop Conditions

两类记录无现成存储范式可复用（需新表/新列）；合同 §1.3/§1.4/§3.3/§3.4 出现未覆盖的关键语义空白；main.py 挂载出现绕不开的改动 → STOP 并引用 Curis_Writing_Domain_Authority.md 具体行。

## 5. Workload / 依赖

M+M ≈ 2.5 人日（含独立 QA）。无外部凭证依赖。依赖 P1-a 已 QA PASS 的 WritingOperatingService/router operating 块/前端 op* 视图范式。

## 6. Execution Record（2026-10-07）

### 6.1 Changed Files（POSTHASH：artifacts/tasks/CURIS-V1-WRITING-MARKET-PERFORMANCE-20261006/POSTHASH.txt）

| 文件 | 处置 | 摘要 |
| --- | --- | --- |
| backend/app/writing_operating_service.py | 修改 | 新增 SNAPSHOT_KIND/OBSERVATION_KIND、`_require_scope_target`（本工作区 WritingBook/WritingChapter 校验）、snapshot/observation 六个读+命令方法、`_save_snapshot`（exact 4 字段、source_note 必填非空、expected_ref 非空拒绝、revision=1/identity=自身/previous_ref=""、wr-snapshot- 前缀）、`_save_observation`（同构 + scope_ref 校验 + WRITING_OBSERVATION_SCOPE 链接、wr-observation- 前缀）；两类强制 UNVERIFIED；幂等键前缀 writing:snapshot:/writing:observation: |
| backend/app/api/writing_router.py | 修改 | 6 端点 GET/POST operating/snapshots[/…/commands/{action}] 与 operating/observations 同构；action Literal 白名单 save-snapshot/save-observation |
| backend/app/main.py | **零改动** | 复用 P1-a 已挂载 operating 实例（本切片关键约束达成，POSTHASH 未列即未触碰） |
| backend/tests/test_writing_market_performance.py | 新增 | 10 测试（exact 字段/source_note 必填/不可变追加/幂等 409/tamper/作品+章节 scope/外部对象 404/scope 链接/跨公司/employee 拒写/冷重启/HTTP smoke 含命令组白名单） |
| frontend/lib/writingState.mjs | 修改 | WRITING_VIEWS 白名单加 market/performance（枚举式 fail-closed 不变） |
| frontend/lib/writingApi.js | 修改 | snapshots/snapshot/snapshotCommand、observations/observation/observationCommand 6 方法 |
| frontend/components/writing/WritingMarket.js | 新增 | 列表/录入（title/body/period/source_note，前端 source_note 必填闸门）/只读详情；「人工录入 · 未验证」徽标；无修订控件 |
| frontend/components/writing/WritingPerformance.js | 新增 | 列表/录入（scope_ref 下拉 2 书+N 章，前端必选闸门）/只读详情；外部平台数据固定「未连接」提示（列表与详情）；无修订控件 |
| frontend/components/writing/WritingWorkspace.js | 修改 | context opNav 加市场快照/表现观察 2 链接；books+view 挂载 2 组件 |
| frontend/components/writing/Writing.module.css | **零改动** | 现有 op*/notice 类与 .workspace input 规则足够（POSTHASH 与 PREHASH 哈希一致 ed3aed6b…） |
| frontend/tests/writingOperatingState.test.mjs | 修改 | 白名单断言扩 market/performance；原「market 非法」断言改为合法并新增 observations 非法用例；repair return 同步 |

### 6.2 证据

- 后端：`test_writing_market_performance.py` **10/10**，与 P1-a `test_writing_operating.py` 合跑 **21/21**（隔离 DB，跑法见交接记忆）。
- 前端：writingOperatingState 4/4；全量 213 → 204 pass / 9 失败，9 失败与 P1-a 登记基线完全同集（v1SevenAreaAcceptance/mvp-p0-auth-onboarding/rdWorkspaceExecution/runtimeProvider/runtimeWorkspaceUi，均不引用 writing 文件）；`npm run build` 成功；切片 6 文件 eslint 0 问题。
- 独立真实浏览器 QA：artifacts/tasks/CURIS-V1-WRITING-MARKET-PERFORMANCE-20261006/qa/QA_REPORT.md——浏览器 **28/28** + API 探针 **16/16**；DB 探针 **15 项**；冷重启 **C1–C4**；截图 7；requests.jsonl 98 请求零 5xx（POST 200×6，422×5/409×1/404×3 均为设计内负向）；console/page/http 错误均 0。
- 受保护 DB 指纹前后 diff 为空（7 sqlite + com.curis.desktop 全部文件）；无 Provider 外发（forbidden 网关心证 P5）；进程与 /tmp 已清理。

### 6.3 越界文件追认

无。全部变更落在 §2 Allowed Files；main.py 与 Writing.module.css 经验证零改动；qa/ 工件落在已授权 artifacts/tasks/<TASK-ID>/** 内。

### 6.4 既有失败登记（不修）

- 后端：test_writing_selected_execution.py 跨文件合跑 2 失败（单跑 7/7，顺序基线，WQA-20/P1-a 同类先例）。
- 前端：全量 9 失败基线同 P1-a §6.4 登记，与本切片无关。

### 6.5 Disposition

- 代码/测试：在本 Issue 授权范围内交付，QA 证据 Accepted（EVIDENCE）。
- 合同 docs/03_Design/Curis_Writing_Domain_Authority.md 保持 Draft（本切片未改产品语义）。
- 任务工件（PREHASH/POSTHASH/qa/DEVELOPMENT_RETURN）：REVIEW_REQUIRED → 留待 Owner 按 P1 序列结束统一 PROMOTE/ARCHIVE。
- Next Gate：P1-c（WR-OP 只读投影）立项，完成后五面齐备，由 Owner 决定合同 Frozen。
