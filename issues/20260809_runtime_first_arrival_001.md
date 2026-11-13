# RUNTIME-FIRST-ARRIVAL-001：Runtime Company Collection 与真实空公司入口

Status: Completed  
Decision: `PASS_RUNTIME_FIRST_ARRIVAL_WITH_BASELINE_BLOCKERS`  
Input: `PASS_RUNTIME_MATERIALIZATION_WITH_BASELINE_BLOCKERS`  
Owner: Curis 产品 / Runtime 评审  
Date: 2026-08-09

## 1. 背景

RuntimeProvider 为发现当前 Company 仍调用旧 `GET /api/workspace/companies`。该旧服务在
fresh 数据库中惰性创建 `Curis AI Company`，使完全新安装无法可靠进入空公司 Founding Guide。
这会把兼容层的历史默认值重新伪装成 Company OS 事实，必须在进入三业务 UI 和 Desktop 前消除。

## 2. 目标

增加不产生副作用的 Runtime Company collection，并让首批 UI 只通过它发现 Runtime Company：

```text
GET Runtime Company collection
→ 0 rows：显示 First Arrival / Founding Guide
→ 1+ rows：读取 Runtime snapshot / CEO Desk
```

已物化的 Runtime Company 可被发现；旧 Project/Task-first Company 不自动升级，也不从兼容表
推断为 Runtime Company。

## 3. 允许文件

允许修改：

- `backend/app/api/runtime_foundation_router.py`；
- `frontend/lib/runtimeApi.js`；
- `frontend/tests/runtimeApi.test.mjs`：仅更新 Runtime Company collection 的路径断言；
- `docs/00_Context/CURRENT_STATE.md`；
- `docs/08_Change_Log/CHANGE_LOG.md`。

允许新增：

- `backend/tests/test_runtime_first_arrival_api.py`；
- `frontend/tests/runtimeFirstArrival.test.mjs`；
- `reviews/20260809_runtime_first_arrival_001_review.md`。

禁止修改 `backend/app/main.py`、旧 `company_project_runtime.py`、`frontend/app/onboarding/page.js`、
Desktop、原型、活动数据库及清单外文件。保留所有输入 dirty diff。

## 4. API 契约

```text
GET /api/workspace/runtime/foundation/companies
```

- 当前 Tenant-scoped；不创建、不补种、不修改任何 Company；
- 只返回通过 Runtime Foundation 物化并具有 Company-level Runtime entity 的 Company；
- 失败与跨 Tenant 返回安全错误；不返回 prompt、密钥或旧执行数据；
- RuntimeProvider 将 `getRuntimeBootstrap()` 的发现请求改为该 collection；其它快照与 Simulation
  请求不变；
- 不新增第二套 Company 状态或兼容路由。

## 5. 必须证明

1. fresh SQLite collection 返回空，不新增 Company；
2. 物化 Company 可被 collection 发现，重启后仍一致；
3. 旧兼容 Company 不会被 collection 返回，也不会被改写；
4. Tenant 隔离 / 失败安全 / 完整性通过；
5. 首批 UI tests、build 和浏览器 fresh First Arrival 证据通过；
6. Foundation / Simulation / API / Materialization 联合回归不下降，全量既有失败数不新增。

## 6. 关闭条件

生成 `reviews/20260809_runtime_first_arrival_001_review.md`，记录 fresh 空入口、物化后发现、
旧兼容 Company 排除、隔离、浏览器和测试证据。完成后暂停，不进入三业务 Workspace UI 或 Desktop。

## 7. 独立验收

主线程复核通过：Backend First Arrival 及联合 Runtime 回归 `44 passed`，Frontend Runtime
tests `13 passed`，scoped ESLint 通过，Next build 成功生成 44 个路由。Fresh SQLite 读取
Runtime collection 前后 Company 计数保持 0；物化后发现、重启、Tenant 隔离、旧兼容 Company
排除和浏览器空 First Arrival 均有证据。Issue 已关闭；三业务 Workspace UI 与 Desktop 仍未进入。
