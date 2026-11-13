# CURIS-V1-PLATFORM-ACCOUNT-S1-20261007 — 平台链 S1：Platform 目录 + ChannelAccount 本地 CRUD + 诚实未连接投影

- **Status**: Accepted（CEO/Owner 2026-10-08 接受，见 §7）
- **Authority Class**: ACCEPTED / IMPLEMENTATION TRUTH
- **Owner**: Main Development（实施）/ CEO（接受）
- **Date**: 2026-10-07（实施与 QA）/ 2026-10-08（Owner 接受）
- **Backlog**: 平台链 P3 切片 S1；依据 [平台/账号本地链合同](../docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md)（Frozen）§6 与 [存储架构评审](../docs/02_Architecture/CURIS_CHANNEL_ACCOUNT_STORAGE_ARCHITECTURE_REVIEW.md)
- **Next Gate**: 已闭合；S2 已于 2026-10-08 接受，下一 backlog 为 S3

## 1. Background

平台链合同已 Frozen（D1–D5 裁定）。S1 交付：平台只读目录（6 平台常量）、ChannelAccount 本地 CRUD（business 级可见）、CG 工作台「账号」新视图与诚实 NOT_CONNECTED 投影。零外发、零连接器。存储按架构评审：复用 runtime_entities（PACKAGE_DOMAIN_OBJECT + objectType='ChannelAccount'），零新表零迁移。

## 2. Allowed Files

后端：
- `backend/app/content_growth_service.py`（新增 accounts 方法：目录/列表/创建/读取/编辑/状态；常量 PLATFORM_CATALOG、ACCOUNT_GROWTH_STAGES、ACCOUNT_STATUS）
- `backend/app/content_growth_entry_service.py`（如需 business_ref 解析 helper）
- `backend/app/api/content_growth_router.py`（新增 `/accounts` GET/POST、`/accounts/{account}` GET/PUT 端点，同错误映射）
- `backend/app/main.py`（仅当构造签名需新参数时最小 hunk；目标零改动）
- `backend/tests/test_cg_channel_accounts.py`（NEW）

前端：
- `frontend/lib/contentGrowthApi.js`（account API 封装）
- `frontend/lib/contentGrowthState.mjs`（accounts 视图注册，如需）
- `frontend/components/content-growth/ContentGrowthWorkspace.js`（视图路由 + 入口）
- `frontend/components/content-growth/ContentGrowthAccounts.js`（NEW：列表+详情+编辑，仅 --ui-* token）
- `frontend/components/content-growth/ContentGrowthWorkspace.module.css`（仅新增结构类，--ui-* token）
- `frontend/tests/`（新增 cg accounts 测试文件）

文档/证据：本 Issue §6、`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S1-20261007/qa/`、CURRENT_STATE head、CHANGE_LOG tail。

**Forbidden**：workspace_package_objects 链、connectors/、content_workflow_runtime.py、legacy 页面、Writing/Music/PACKAGE 既有对象、schema/建表、product docs、hex 色值、任何外发网络调用。

## 3. Acceptance Evidence

1. **新测试**：pytest 全绿——目录 6 平台恒定；创建/读取/编辑（name/positioning/audience/content_mix/cadence/voice/growth_stage/responsibility/status）；`platform_ref` 非法值 422；`connection_status` 客户端传入被忽略且恒 NOT_CONNECTED；跨公司 404；business 级可见：同公司同业务另一 CG workspace 可见同一账号；`status` 枚举校验（active/dormant/banned）。
2. **全量回归**：失败集与当前基线（43 failed / 1886 passed / 8 skipped，qa/FAILSET_CURRENT.txt of LEGACY-RD-XHS-TTK-FREEZE-20261007）IDENTICAL。
3. **前端**：eslint 0 error；新测试全过；全量 9 既有失败不变零新增；生产 build 成功。
4. **独立 QA**（隔离 sqlite + 真实浏览器）：账号视图创建→列表→详情→编辑；NOT_CONNECTED 恒显示「未连接」；跨工作区互见；伪造/越权 4xx；零 5xx；forbidden 网关零外发；PREHASH=POSTHASH（仅 Allowed Files）；冷重启数据存活；进程/端口//tmp 清理。
5. **登记五处**：QA_REPORT / DEVELOPMENT_RETURN / Issue §6 / CURRENT_STATE head / CHANGE_LOG tail。

## 4. Stop Conditions

- 需要建表/迁移或触碰 workspace_package_objects 才能实现 → STOP 回报（架构评审前提失效）。
- 发现 CG 内容链 `target_account_refs` 校验与账号对象冲突 → STOP 定位根因。
- 现行三业务链出现回归 → STOP 优先恢复。
- 出现任何外发请求路径 → 立即移除并回报。

## 5. Conventions

- 中文汇报；无 Git 写；后端测试 `CURIS_DB=CURIS_DB_PATH=CURIS_WORKSPACE_DB` 同隔离路径 + `PYTHONPATH=backend` + cwd=仓库根；前端 QA 后端起 8000（QA_PORT）。
- 合同红线 §1 全量适用于本切片。

## 6. Execution Record

Status: Review（实施 + 独立 QA 完成，待 Owner 接受）· Date: 2026-10-07 · Owner: Main Development。

**实现面**（全部在 §2 Allowed Files 内；PREHASH=POSTHASH 8 文件仅 5 个变更）：

- 后端 [content_growth_service.py](../../backend/app/content_growth_service.py)：模块常量
  PLATFORM_CATALOG（6 平台：xhs/douyin/wechat_oa/tiktok/youtube/bilibili）、
  ACCOUNT_GROWTH_STAGES、ACCOUNT_STATUS、ACCOUNT_CONNECTION_STATUS="NOT_CONNECTED"、
  ACCOUNT_CREATE_FIELDS（10）/ ACCOUNT_EDIT_FIELDS（9，无 platform_ref 即平台不可编辑）；
  CG_ACCOUNT_KIND="ChannelAccount"；`_account_payload`（先剥离客户端 connection_status 再
  exact，故客户端值被静默忽略而非 422；platform_ref 目录校验；learning_text 256/2000；
  枚举校验；注入 NOT_CONNECTED）、`_account_row`（business 闸门 404「账号不在当前业务范围」）、
  `_account_business_ref`（authoring_scope WORKSPACE→BUSINESS 解析）、account_collection /
  account / account_create（begin-immediate + write=True）/ account_edit。
- 存储按架构评审：runtime_entities 行 entity_type='PACKAGE_DOMAIN_OBJECT' +
  data_json.objectType='ChannelAccount' + verification_status='UNVERIFIED' +
  evidence_condition='MISSING'；行写 company_id，workspace_id 记创建工作区，业务归属
  data_json.business_ref；business 级可见 = `company_id + json_extract('$.business_ref')`
  查询（D2：同业务跨工作区互见可编辑）。**零新表零迁移**。
- 后端 [content_growth_router.py](../../backend/app/api/content_growth_router.py)：
  AccountIn(extra="forbid") + GET/POST `/accounts`、GET/PUT `/accounts/{account}`，同 invoke
  错误映射（RuntimeScopeError/KeyError→404、Conflict→409、ValueError→422）。
  [main.py](../../backend/app/main.py) **零改动**（哈希验证）。
- 前端 [contentGrowthState.mjs](../../frontend/lib/contentGrowthState.mjs) 视图白名单 +accounts；
  [contentGrowthApi.js](../../frontend/lib/contentGrowthApi.js) 4 封装；
  [ContentGrowthAccounts.js](../../frontend/components/content-growth/ContentGrowthAccounts.js)
  （NEW：list/create/edit/detail，平台/阶段/状态中文标签，`formPayload()` 不含
  platform_ref 与 connection_status，所有外部状态位恒显「未连接」，仅复用既有
  ContentGrowth.module.css 类——该 CSS 零改动）；
  [ContentGrowthWorkspace.js](../../frontend/components/content-growth/ContentGrowthWorkspace.js)
  「经营账号」入口 + 视图分支。
- 测试：[test_cg_channel_accounts.py](../../backend/tests/test_cg_channel_accounts.py) 7/7
  （目录恒定+诚实空态、全字段 CRUD+NOT_CONNECTED、客户端 connection_status 被忽略、非法
  platform_ref/枚举 422、跨公司 404、同业务跨工作区可见+编辑、owner 写权限）；
  [contentGrowthAccounts.test.mjs](../../frontend/tests/contentGrowthAccounts.test.mjs) 3/3。

**回归与独立 QA**：

- 后端全量 43 failed / 1893 passed / 8 skipped，失败集与基线（43/1886/8，
  LEGACY-RD-XHS-TTK-FREEZE FAILSET_CURRENT.txt）IDENTICAL（+7 新通过；
  `artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S1-20261007/qa/FAILSET_S1_IDS.txt`）。
- 前端全量 226/217/9（9 既有失败不变，+3 新通过）；eslint 0 error；`next build` 成功。
- 独立 QA（隔离 sqlite/store、8000/3000、forbidden 网关零外发、真实浏览器）：
  API 探针 27/27（含客户端 connection_status 静默忽略、platform_ref 不可编辑、同业务第二
  工作区互见/可编辑、冷重启存活、无新表）；浏览器 6/6（列表 2 seed 账号均「未连接」→注册
  抖音账号→详情/编辑改名+休眠→无 error banner→console 干净→冷重启存活）；105 请求零 5xx
  （97×200/3×404/5×422）；forbidden-outbound.log 全程不存在。
- 清理：QA server 与 next dev 已 kill，端口 8000/3000 释放；本任务 /tmp 隔离文件已删。

**证据**：`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S1-20261007/qa/` 下 QA_REPORT.md、
DEVELOPMENT_RETURN.md、PREHASH.txt / POSTHASH.txt、BACKEND_REGRESSION_TAIL.txt、
requests.jsonl、server-ownership.json。

**边界与不做项**（合同切片，非遗漏）：S2 核验清单 + D4 最小导出、S3 人工回执（UNVERIFIED/
CEO_MANUAL/时点不可变）+ 人工表现观察、S4 平台角色+Learning scope（v1.1）；legacy connectors/
与 content_workflow_runtime.py 保持冻结未触碰；零外发零连接器。

**下一 Gate**：~~Owner Review~~ 已闭合（2026-10-08 接受，见 §7）；S2 已接受，backlog 下一项 S3。

## 7. Owner Acceptance Record（2026-10-08）

- **Verdict**: ACCEPTED — 实施与独立 QA 均通过（API 探针 27/27、浏览器 6/6、回归失败集与基线 IDENTICAL、PREHASH=POSTHASH、零 5xx/零外发、冷重启存活），合同红线全部遵守。
- **Disposition**: SLICE ACCEPTED / CLOSED；产物 PROMOTE 为正式 Implementation Truth（已在 canonical 路径）；qa/ 证据保留为 EVIDENCE。
- **Owner**: CEO（2026-10-08 指令「执行吧」：接受 S1 并推进 S3）。
- **接受依据**：§6 证据包（QA_REPORT.md / DEVELOPMENT_RETURN.md / PREHASH=POSTHASH / requests.jsonl）；本接受为补登记——S1 的 QA PASS 于 2026-10-07 完成，S2/S3 均以 S1 为前置。
- **未完成项（合同切片，不在本接受范围）**：S2（已于 2026-10-08 同日接受）、S3 人工回执+人工表现观察、S4 挂 v1.1（D5）。
- **Next Action**: S3 Issue（人工回执 + 人工表现观察）。
- **Target Authority**: 合同 §6；CURRENT_STATE / CHANGE_LOG 同步本接受。
- **Next Gate**: S3 Owner 接受后，平台链 S1–S3 本地内容经营闭环全部闭合。
