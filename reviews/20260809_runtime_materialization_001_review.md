# RUNTIME-MATERIALIZATION-001 Review

Status: Review  
Decision: `PASS_RUNTIME_MATERIALIZATION_WITH_BASELINE_BLOCKERS`
Date: 2026-08-09

## 1. 结论

已在授权封闭清单内闭合第一条 Company Runtime 物化链：

```text
CEO_CONFIRMED
→ 当前 Tenant / 可信 CEO 身份校验
→ 服务内部 SYSTEM 单事务物化 Company + Company-level CEO Assistant
→ FoundingRun = COMPANY_CREATED + transition audit
→ 前端确认 Runtime Company / Assistant 快照
→ /ceo-office
```

没有调用旧 `createCompany()`，没有创建 Workspace、Project、Task，没有修改 Desktop、
Prototype、活动数据库、真实平台 API 或清单外业务模块。本 Review 不宣称三业务 Workspace
或 Desktop 产品完成。

## 2. 实际改动文件

修改：

- `backend/app/runtime/foundation.py`
- `backend/app/api/runtime_foundation_router.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/onboarding/page.js`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

新增：

- `backend/tests/test_runtime_materialization_api.py`
- `frontend/tests/runtimeMaterialization.test.mjs`
- `reviews/20260809_runtime_materialization_001_review.md`

## 3. API 与事务契约

新增：

```text
POST /api/workspace/runtime/foundation/founding-runs/{founding_run_id}/materialize-company
```

请求只接受 `company_id`、`ceo_id`、`name`；Pydantic `extra=forbid` 拒绝 HTTP
`actor=SYSTEM`、prompt、密钥或任意 payload。ID 采用受限字符集与长度，名称去除首尾空白并
拒绝控制字符。

Foundation 使用 SQLite `BEGIN IMMEDIATE` 串行化物化边界；Company、唯一 CEO Assistant、
FoundingRun 的 `company_id / parent_id / COMPANY_CREATED`、SYSTEM transition audit 和
`CREATED_ASSISTANT` link 在同一事务提交。任一步失败由现有 `Database.connect()` 回滚。

已物化 FoundingRun 的相同请求直接读取并返回原 Company / Assistant，不生成新 ID、不重复
审计；请求参数与已物化事实不一致时返回安全 409。

## 4. 身份与隔离边界

- HTTP 入口先要求当前身份角色为 Owner / CEO；`test` 角色只存在于显式测试模式。
- 物化时要求请求 `ceo_id` 非空且等于 `TenantContext.current_identity().ceo_id`。
- Foundation 再要求同一个 `ceo_id` 等于 FoundingRun `owner_ref`。
- 缺失稳定 CEO 身份、伪造 CEO、跨 Tenant / FoundingRun 一律 fail-closed 404。
- 非 CEO 返回 403；非 `CEO_CONFIRMED` 返回 409；非法字段返回 422。
- HTTP 不接受 actor；只有 Foundation 内部状态机以 `SYSTEM / persist_company` 写入审计。
- 错误响应不包含 SQLite、路径、堆栈、内部行或敏感内容。

## 5. 数据库与幂等证据

聚焦测试在 fresh 临时 SQLite 覆盖：

- fresh 创建后 Company = 1、CEO Assistant = 1；
- FoundingRun、Company、Assistant 快照一致；
- 重复请求、服务重启后重复请求均返回相同 Assistant ID；
- 两个独立 App / Client 并发请求均为 200，最终 Company = 1、Assistant = 1、
  `COMPANY_CREATED` audit = 1；
- Workspace = 0、Project = 0、Task = 0；
- 跨租户、缺失 / 冒充 CEO、非 CEO、未确认状态、非法 ID、控制字符名称与额外
  `actor=SYSTEM` 均安全拒绝；
- `pragma integrity_check = ok`；
- 既有 fresh / upgrade schema convergence 测试通过。

浏览器正向链临时数据库：

```text
/tmp/curis-runtime-materialization-browser.G11ksG
```

真实记录：

- FoundingRun：`founding_run-ad24d07a-9768-47a1-9459-b9a234258971`
- Company：`company-ad24d07a-9768-47a1-9459-b9a234258971`
- CEO Assistant：`ceo_assistant-1f9011b1-d588-4a52-9f0b-f62a10192048`
- Tenant / CEO：`selfuse / selfuse-ceo`
- audit：`CEO_CONFIRMED → COMPANY_CREATED`、`SYSTEM`、`persist_company`、Company ID、UTC 时间
- HTTP 幂等重放：200；随后计数仍为 `1 | 1 | 1`
- 重启后 Company / Assistant 快照：200
- Workspace / Project / Task：`0 / 0 / 0`
- integrity：`ok`

## 6. 前端与浏览器证据

Founding Guide 在 `CEO_CONFIRMED` 展示“建立公司”，提交稳定的 FoundingRun 派生
`company_id`、可信 `CEO_ID` 与名称。成功后顺序为：materialize API →
`getRuntimeCompany()` 确认 Company / Assistant → `runtime.refresh()` → `/ceo-office`。

浏览器真实路径：

```text
/onboarding
→ 建立 FoundingRun
→ INTENT_CAPTURED
→ CLARIFYING
→ PROPOSED
→ CEO_CONFIRMED
→ 建立公司
→ /ceo-office
```

结果：CEO 工作台显示 `Curis Browser Company`、Company Runtime 快照、CEO 助理已建立、
0 个工作空间；浏览器 warning / error 日志均为 0。

验证入口使用临时同源代理在物化前仅把旧 `/api/workspace/companies` collection 投影为空；
FoundingRun、Transition、Materialization、Runtime snapshot 与物化后的 Company directory 请求均
原样转发真实 Backend。这样可独立证明本 Issue 的 `CEO_CONFIRMED → CEO Desk` 切片，但不能
证明现有旧 Company directory 在完全无辅助的新安装中不会抢先创建兼容 Company。

截图：

- `/tmp/curis-runtime-materialization-browser-evidence/01-ceo-confirmed.png`
- `/tmp/curis-runtime-materialization-browser-evidence/02-ceo-desk.png`

## 7. 测试与构建

Backend Runtime / Simulation / API / Materialization / schema 联合回归：

```text
38 passed
```

Frontend Runtime scoped Node tests：

```text
11 passed
```

Frontend scoped ESLint：通过。  
Next production build：通过，44 个 App Router 页面生成成功。

Backend 全量：

```text
1279 passed, 31 failed, 2 skipped
```

相对上一阶段 `1276 passed, 31 failed, 2 skipped`，新增 3 个 Materialization 测试通过，
既有失败数仍为 31。失败仍属于输入前的 Model Gateway / 默认 gateway seed、旧数字员工执行
绑定和旧前端源码断言等清单外基线；本 Issue 未修复或扩大这些范围。

全仓 Frontend lint 仍有输入前 5 个 error、1 个 warning；本 Issue 三个 scoped 文件 lint 通过。

## 8. Pre-existing Diff 分离

- `backend/app/main.py` 本 Issue 未写入；当前 SHA-256
  `7c9749a6ac6bfc7377cd9a448f1efc217ba3f5ad965e2bdafb7e3d8774fd7076`，与
  `RUNTIME-API-001` Review 完成值完全一致；当前 `93 insertions / 0 deletions` 均为既有
  Router 注册及更早 dirty diff。
- `foundation.py`：输入 SHA-256
  `55429a9bd911fd380f5ab78e8786cbb2a589c4b66286da5ac785b84b60adb0c0`；输出
  `334ec4cbc5b6d46f977dc41380daf7724f9d13fc031989feb0e682e9409e8355`。
- `runtime_foundation_router.py`：输入
  `54e33f042720bd0118a74c64f82175c9f60485d51e716852704761593bf02788`；输出
  `62209a7666cc5dae4724e75718c71840c589b65b490658dc36b7161cee9340e4`。
- `runtimeApi.js`：输入
  `083a28b6d7609b6e7b98e440901db6ebdec22999ea61931e2ef42d1a99900cc5`；输出
  `54c606313e4d6913d168bdd5ccc0e4d1c7f1797c5b4a58d598e39271d7edf5fb`。
- `onboarding/page.js`：输入
  `48158a2fd3f69918132ca61fba1a779bb93f8057249e3ffe4eebc14fdab2bbe1`；输出
  `48137e1327935d765f6f503eb77dbfb55ccfe9fbab2d9effe76fa5e7a56c819c`。
- 所有命令均使用显式 `/tmp/curis-runtime-materialization-*` SQLite；未指向
  `data/curis.sqlite` 或 `backend/data/curis.sqlite`。
- 未执行 reset、checkout、删除或 dirty tree 清理。

## 9. 已知限制与下一步

- 31 个 Backend 和全仓 lint 基线问题仍需各自独立 Issue；不属于本 Issue。
- fresh 临时 SQLite 直接调用旧 `GET /api/workspace/companies` 会由既有兼容服务自动 seed
  `Curis AI Company`。根级 RuntimeProvider 当前用该 collection 发现 Company，因此这一旧副作用
  可能遮蔽完全无辅助的新安装 Founding Guide。修复需要修改清单外旧 Company 服务，或另行批准
  Runtime Company collection 契约；本 Issue 已停止在边界内，未通过代理行为写入产品代码。
- 本实现只物化 Company 与第一位 CEO Assistant；业务 Workspace、Project、Task、真实平台、
  Tauri / Desktop 均未进入。
- 当前结论为 `IMPLEMENTED_PENDING_INDEPENDENT_REVIEW`：物化切片通过；完全无辅助的 fresh
  First Arrival 仍带上述既有 Company directory blocker。等待独立质量 Review 或新 Issue 授权。

## 10. Independent Review

主线程于 2026-08-09 完成独立复核：

- Backend Runtime 联合回归：`42 passed`；
- Frontend Runtime tests：`11 passed`；
- Next build：成功，44 个 App Router 页面；
- 临时 SQLite 的事务、幂等、并发、隔离、审计和完整性证据一致；
- 浏览器 CEO_CONFIRMED → Company → CEO Assistant → CEO Desk 路径通过，控制台无 warning / error。

独立决定：`PASS_RUNTIME_MATERIALIZATION_WITH_BASELINE_BLOCKERS`。

`GET /api/workspace/companies` 的旧惰性 seed 会遮蔽完全无辅助的新安装引导，已明确记录为
后续 `RUNTIME-FIRST-ARRIVAL-001`，不影响本 Issue 的物化边界，但阻止把完整 First Arrival
或 Desktop 目标态宣称为完成。
