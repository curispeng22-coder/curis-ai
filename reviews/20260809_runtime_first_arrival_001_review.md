# RUNTIME-FIRST-ARRIVAL-001 Review

Status: Review  
Decision: `PASS_RUNTIME_FIRST_ARRIVAL_WITH_BASELINE_BLOCKERS`
Date: 2026-08-09

## 1. 结论

已在授权封闭清单内增加无副作用 Runtime Company collection，并让 Runtime bootstrap
停止调用会在 fresh 数据库惰性 seed 的旧 Company collection。真实 fresh 浏览器现在无需
拦截即可进入 Founding Guide，完成物化后由同一 Runtime collection 发现 Company 并进入
CEO 工作台。

未修改旧 Company 服务、`backend/app/main.py`、onboarding、Desktop、Prototype、活动数据库
或清单外文件。

## 2. 实际改动文件

修改：

- `backend/app/api/runtime_foundation_router.py`
- `frontend/lib/runtimeApi.js`
- `frontend/tests/runtimeApi.test.mjs`（仅 3 处 collection 路径预期）
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

新增：

- `backend/tests/test_runtime_first_arrival_api.py`
- `frontend/tests/runtimeFirstArrival.test.mjs`
- `reviews/20260809_runtime_first_arrival_001_review.md`

## 3. API 契约

```text
GET /api/workspace/runtime/foundation/companies
```

返回当前 Tenant 的 Runtime Company collection。查询只执行 `SELECT`，不调用旧
Company service，不创建、不补种、不更新 Company。

一条 Company 只有同时满足以下事实才被投影：

1. 当前 Tenant 的 `companies` 记录；
2. 同 Tenant / Company 的 `FOUNDING_RUN` 已关联 Company；
3. FoundingRun `parent_id` 指向同 Tenant / Company 的 `CEO_ASSISTANT`。

因此普通旧 Company、Project/Task-first Company、只有孤立 CEO Assistant 的兼容 Company
均不会被自动升级或返回。响应只包含安全 Company 投影，不返回 Runtime `data_json`、prompt、
密钥、旧执行数据、内部表名或跨租户事实。

## 4. Fresh / 兼容排除 / 隔离证据

Backend 聚焦测试证明：

- fresh collection：HTTP 200，`{"tenant_id": ..., "companies": []}`；
- collection 前后 `companies / runtime_entities / runtime_transition_log = 0 / 0 / 0`；
- 旧兼容 Company 被排除且整行内容未改写；
- 旧兼容 Company 即使存在孤立 Company-level CEO Assistant，仍不会被视为已物化 Company；
- Tenant A / Tenant B 各自只能发现自身物化 Company；
- 跨租户 snapshot 返回安全 404，不泄露另一 Tenant ID；
- 物化 Company 在服务重启后 collection 投影完全一致；
- `pragma integrity_check = ok`。

## 5. Frontend 行为

`getRuntimeBootstrap()` 现在先调用：

```text
/api/workspace/runtime/foundation/companies
```

- 0 rows：返回 `{companyId: "", snapshot: null, simulations: []}`，进入 Founding Guide；
- 1+ rows：沿用既有 Runtime Company snapshot 与 Workspace Simulation 查询；
- `runtimeApi.js` 不再调用旧 `/api/workspace/companies` 发现 Company；
- 未改变 onboarding、RuntimeProvider、Company snapshot 或 Simulation 契约。

## 6. 真实浏览器证据

验证数据库：

```text
/tmp/curis-runtime-first-arrival.h0FfT2
```

同源代理只直通 `/gateway/* → Backend` 和页面请求，没有拦截、伪造或改写 collection。

实际链路：

```text
fresh SQLite（Company = 0）
→ GET Runtime Company collection = []
→ /onboarding 显示 Founding Guide
→ FoundingRun
→ INTENT_CAPTURED → CLARIFYING → PROPOSED → CEO_CONFIRMED
→ 物化 Curis First Arrival Company
→ Runtime Company collection 返回该 Company
→ /ceo-office
```

物化事实：

- Company：`company-5bfebbfe-8197-4170-9628-0b7d202e6390`
- FoundingRun：`founding_run-5bfebbfe-8197-4170-9628-0b7d202e6390`
- CEO Assistant：`ceo_assistant-bb6ed86a-da85-4b3b-94aa-2ce40e858892`
- Workspace / Project / Task：`0 / 0 / 0`
- 重启后 collection：HTTP 200，同一 Company
- integrity：`ok`
- 浏览器 warning / error：0
- Backend 请求日志未出现旧 `GET /api/workspace/companies`

截图：

- `/tmp/curis-runtime-first-arrival-browser-evidence/01-fresh-first-arrival.png`
- `/tmp/curis-runtime-first-arrival-browser-evidence/02-materialized-ceo-desk.png`

## 7. 测试与构建

Backend First Arrival focused：

```text
2 passed
```

Backend Foundation / Simulation / API / Materialization / First Arrival / schema 联合回归：

```text
40 passed
```

Frontend Runtime scoped tests：

```text
13 passed
```

Frontend scoped ESLint：通过。  
Next production build：通过，44 个 App Router 页面生成成功。

Backend 全量：

```text
1281 passed, 31 failed, 2 skipped
```

相对上一阶段 `1279 passed, 31 failed, 2 skipped`，新增 2 个 First Arrival 测试通过，
既有失败数保持 31。失败仍属于输入前 Model Gateway / gateway seed、旧数字员工执行绑定和
旧前端源码断言等清单外基线，本 Issue 未扩大修复。

## 8. Pre-existing Diff 分离

- `backend/app/main.py` 未写入，SHA-256 保持
  `7c9749a6ac6bfc7377cd9a448f1efc217ba3f5ad965e2bdafb7e3d8774fd7076`。
- `frontend/app/onboarding/page.js` 未写入，SHA-256 保持
  `48137e1327935d765f6f503eb77dbfb55ccfe9fbab2d9effe76fa5e7a56c819c`。
- Router 输入 SHA-256
  `62209a7666cc5dae4724e75718c71840c589b65b490658dc36b7161cee9340e4`；输出
  `f9c6d0cc4d2651a389e732f981083e0dad0cb7327464cdda3a3d3d89e85c4a8f`。
- `runtimeApi.js` 输入
  `54c606313e4d6913d168bdd5ccc0e4d1c7f1797c5b4a58d598e39271d7edf5fb`；输出
  `4e2de711a6d6664d79a450793680ebf40da2a71fa9ac9bd6f21404c8539225c1`。
- `runtimeApi.test.mjs` 输入
  `f14029193ae88d9a6bbbe1474b394276ec62fca582ca53b43c83ed74c4ef41fa`；输出
  `5721ede616ff16e82cd716da046f98833223209c621eec498046605667edb980`。
- 所有运行验证使用显式 `/tmp/curis-runtime-first-arrival*` SQLite；未指向活动数据库。
- 未执行 reset、checkout、删除或 dirty tree 清理。

## 9. 边界与下一步

- 本 Issue 只解决 Runtime Company 发现与真实空公司入口；没有修改旧 Company API 的兼容行为。
- 三业务 Workspace UI、真实平台、Tauri / Desktop 均未进入。
- 当前结论已通过独立 Review：`PASS_RUNTIME_FIRST_ARRIVAL_WITH_BASELINE_BLOCKERS`。

## 10. Independent Review

主线程于 2026-08-09 完成独立复核：

- Backend First Arrival / Foundation / Simulation / API / Materialization 联合回归：`44 passed`；
- Frontend Runtime tests：`13 passed`；
- Next build：成功，44 个 App Router 页面；
- fresh collection 读取前后数据库 Company 计数保持 `0`，无兼容 Company 惰性 seed；
- 物化后 collection 发现、重启一致、Tenant 隔离和旧 Company 排除均通过；
- 浏览器完整路径为 fresh First Arrival → FoundingRun → Company 物化 → CEO Desk，控制台无错误。

独立决定：`PASS_RUNTIME_FIRST_ARRIVAL_WITH_BASELINE_BLOCKERS`。

保留输入前全仓 Backend / ESLint 基线问题；本 Issue 不进入三业务 Workspace UI、真实平台或
Desktop。Runtime Company collection 现已成为 Company OS 首批 UI 的唯一发现入口。
