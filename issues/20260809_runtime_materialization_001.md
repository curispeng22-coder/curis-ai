# RUNTIME-MATERIALIZATION-001：CEO 确认后的 Company Runtime 物化

Status: Completed  
Decision: `PASS_RUNTIME_MATERIALIZATION_WITH_BASELINE_BLOCKERS`  
Input: `PASS_UI_RUNTIME_WITH_BASELINE_BLOCKERS`  
Owner: Curis 产品 / Runtime 评审  
Date: 2026-08-09

## 1. 背景与目标

首批 Company OS UI 已经能够让 CEO 创建并恢复 FoundingRun，但在
`CEO_CONFIRMED` 后只能显示“等待 Runtime 系统动作”。Runtime Foundation 已有
`materialize_company()` 内核能力，本 Issue 只把这一条受控系统动作开放给前端，闭合
“创办公司”的第一条真实链路：

```text
CEO_CONFIRMED
→ SYSTEM 物化 Company
→ 创建 Company-level CEO Assistant
→ FoundingRun = COMPANY_CREATED
→ UI 进入 CEO 工作台
```

本 Issue 不创建业务 Workspace、不创建 Project / Task、不生成示例数据，也不提前进入
三业务工作台或 Desktop。

## 2. 允许文件

### 2.1 允许修改

- `backend/app/runtime/foundation.py`：只补物化的幂等、作用域与事务行为；不改变既有状态机定义；
- `backend/app/api/runtime_foundation_router.py`：增加 Company 物化 Router；
- `frontend/lib/runtimeApi.js`：增加物化 API 客户端；
- `frontend/app/onboarding/page.js`：CEO_CONFIRMED 后调用受控物化 API，并在成功后进入 CEO 工作台；
- `docs/00_Context/CURRENT_STATE.md`；
- `docs/08_Change_Log/CHANGE_LOG.md`。

### 2.2 允许新增

- `backend/tests/test_runtime_materialization_api.py`；
- `frontend/tests/runtimeMaterialization.test.mjs`；
- `reviews/20260809_runtime_materialization_001_review.md`。

除上述清单外不得修改任何文件；保留输入时所有 dirty diff。

## 3. API 契约

```text
POST /api/workspace/runtime/foundation/founding-runs/{founding_run_id}/materialize-company
```

请求体只允许：

```json
{
  "company_id": "company-...",
  "ceo_id": "ceo-...",
  "name": "..."
}
```

约束：

- 只接受当前 Tenant 的明确 CEO 请求；SYSTEM 只在服务内部调用 Foundation，不可由 HTTP
  `actor` 字段伪装；
- FoundingRun 必须处于 `CEO_CONFIRMED`；其它状态返回安全的 409；
- Company、CEO Assistant、FoundingRun 状态更新必须在同一事务中完成，并写入已有 transition audit；
- 同一 FoundingRun 的重试必须幂等返回同一 Company / Assistant，不得重复插入或生成第二位 Assistant；
- `company_id`、`ceo_id`、`name` 必须经过长度与安全校验；不得接收 prompt、密钥、原始意图或任意 payload；
- Tenant / FoundingRun 不匹配统一 fail-closed；错误不得泄漏 SQLite、堆栈或内部字段。

## 4. 前端行为

- `CEO_CONFIRMED` 页面显示明确的“建立公司”系统动作；
- 成功后刷新 Runtime，确认 Company / Assistant 快照，再跳转 `/ceo-office`；
- 网络失败、冲突、越权保持中文安全错误，并允许重试；
- 不调用旧 `createCompany()`，不写 LocalStorage 作为 Company 事实，不用 mock 或 Project 代替。

## 5. 必须证明

1. fresh 数据库创建、重启恢复、物化后 Company / Assistant / FoundingRun 快照一致；
2. 同一请求重试幂等，Company 与 CEO Assistant 只有一份；
3. Tenant / FoundingRun 隔离，跨租户返回 404；
4. 非 CEO、未确认状态、非法参数和并发冲突安全失败；
5. transition audit 包含 SYSTEM、`persist_company`、Company ID 和时间；
6. 前端 scoped tests、build 和浏览器真实 CEO_CONFIRMED → CEO Desk 路径通过；
7. 既有 Runtime Foundation / Simulation / API 回归不下降，全量基线失败数不新增。

## 6. 禁止范围

- 三业务 Workspace 详细 UI、真实小红书 / 抖音 / TikTok API、外部消息；
- Desktop / Tauri、活动数据库、旧 Company API 迁移、Project / Task 回填；
- 新 Assistant、第二套状态机或第二套 Company 创建流程；
- 删除、reset、checkout 或清理既有 dirty / untracked 文件。

## 7. 关闭条件

生成 `reviews/20260809_runtime_materialization_001_review.md`，记录实际文件、API
状态、事务 / 幂等 / 隔离证据、前端路径、测试和构建结果。完成后暂停，不进入三业务
Workspace UI。

## 8. 独立验收

主线程复核通过：Backend Runtime 联合回归 `42 passed`，Frontend Runtime tests `11 passed`，
scoped ESLint 通过，Next build 成功生成 44 个页面。临时 SQLite 的 fresh / restart / 幂等 /
并发 / 隔离 / audit / integrity 证据与浏览器 CEO_CONFIRMED → CEO Desk 证据均可复核。

保留基线阻塞：旧 `GET /api/workspace/companies` 会在 fresh 数据库惰性创建兼容 Company，
而 RuntimeProvider 仍通过该旧集合发现 Company；因此本 Issue 通过的是物化切片，不是完整
“全新安装 → 空公司 First Arrival”验收。该问题不在本 Issue 清单内，已转入后续
`RUNTIME-FIRST-ARRIVAL-001`，不得在本 Issue 内扩大修改。
