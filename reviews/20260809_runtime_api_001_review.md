# RUNTIME-API-001 Final Review

Status: Review
Decision: `PASS_RUNTIME_API_WITH_BASELINE_BLOCKERS`
Date: 2026-08-09
Issue: `issues/20260809_runtime_api_001.md`
Input: Runtime Simulation `PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`

## Scope

本轮只增加 Backend Runtime Foundation 的 tenant-scoped 薄 API Adapter。运行对象与状态仍由 `RuntimeFoundation` / `SimulationRuntime` 提供；API 不拥有第二份状态，不直接更新 `status`，不把旧 Project / Task / Workflow 聚合伪装成目标 Runtime。

未进入 frontend、`curis-ui-prototype/`、Desktop、活动数据库、真实平台 API、旧链迁移或历史回填。

## Actual Changed Files

- `backend/app/api/runtime_foundation_router.py`：新增 Runtime Foundation Router；
- `backend/tests/test_runtime_foundation_api.py`：新增 API fresh / restart / isolation / state / error 测试；
- `backend/app/main.py`：仅新增 Router import 与 `include_router` 注册，共 3 行；
- `docs/00_Context/CURRENT_STATE.md`：同步当前交付事实；
- `docs/08_Change_Log/CHANGE_LOG.md`：追加本 Issue 记录；
- `reviews/20260809_runtime_api_001_review.md`：本 Review。

## API Contract

```text
GET  /api/workspace/runtime/foundation/companies/{company_id}
GET  /api/workspace/runtime/foundation/companies/{company_id}/workspaces/{workspace_id}/simulations
POST /api/workspace/runtime/foundation/founding-runs
GET  /api/workspace/runtime/foundation/founding-runs/{founding_run_id}
POST /api/workspace/runtime/foundation/entities/{entity_id}/transition
```

- Company 快照只读取当前 Tenant 的 Company、唯一 CEO Assistant、AI Employee、Role Slot、Capability Binding 和 Workspace 投影；
- SimulationRun 只返回状态、PASS、最终态、失效状态和结构化失败摘要，不返回 participants、receipt 原文、事件 payload 或内部上下文；
- FoundingRun 从 Foundation 初始态创建，重启后按原 ID 恢复；
- 状态转换只调用 `RuntimeFoundation.transition()`，不直接写状态；
- actor、trigger、reason、`evidenceRefs`、`nextCheckAt` 全部进入既有 transition audit；
- `context` 只接受已批准的 guard 引用字段，不接受任意 prompt、credential 或 raw payload；
- Simulation receipt、manual feedback、failure resolution 继续保留在可信 Backend `SimulationRuntime`；本 Issue 不新增前端直写端点。

## Security Boundary

- 所有读取依赖当前 `TenantContext`；Company / Workspace 不匹配统一返回 404，不暴露对象是否存在；
- Transition API 只接受 `actor=CEO`，并要求当前身份角色为 `owner / ceo`；`test` 仅供现有测试身份模式；
- Evidence 引用必须属于当前 Tenant，并与目标对象 Company / Workspace 一致；
- SYSTEM / AI / EXTERNAL 不可通过用户入口伪装 CEO；`WAITING_CEO` 自动批准被拒；
- 错误只返回可操作中文信息，不返回 SQLite 路径、异常文本、内部堆栈、Prompt、密钥或原始数据字段；
- 只读投影使用字段白名单，实体 `data_json` 与 Simulation 原始集合不进入响应。

## Focused Tests

```text
backend/.venv/bin/python -m pytest -q backend/tests/test_runtime_foundation_api.py

4 passed, 1939 warnings in 1.09s
```

覆盖：

1. Company / Assistant / AI Organization / Workspace 快照与 SimulationRun 脱敏投影；
2. FoundingRun fresh 创建、状态转换、完整审计及新 App / Database 实例重启恢复；
3. Tenant、Company、Workspace 跨作用域 fail-closed；
4. 非法 actor、非法状态、`WAITING_CEO` SYSTEM 自动批准、缺失对象与安全错误响应。

## Existing Foundation / Simulation Regression

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_three_business_runtime_simulations.py \
  backend/tests/test_runtime_foundation_state_contracts.py \
  backend/tests/test_runtime_foundation_persistence.py \
  backend/tests/test_runtime_foundation_isolation.py \
  backend/tests/test_runtime_foundation_simulation.py \
  backend/tests/test_runtime_foundation_legacy_adapter.py \
  backend/tests/test_state_machine.py \
  backend/tests/test_integration_baseline_fixes.py::SchemaGovernanceTests::test_fresh_and_upgraded_schema_match_and_record_version

31 passed, 339 warnings in 2.37s
```

原 Foundation / 三业务 Simulation 聚焦基线保持 31 项全部通过。

## Full Backend Baseline

```text
backend/.venv/bin/python -m pytest -q backend/tests --tb=short

1276 passed, 31 failed, 2 skipped, 167589 warnings in 157.84s
```

失败数量与上一阶段基线完全一致，没有新增失败。31 项仍归属于授权范围外的既有漂移：

- `newapi` 与本地 `.env` 默认 Gateway / Model 配置不一致；
- Model Gateway / R3 状态码及 Catalog 断言漂移；
- 旧数字员工执行控制链与 Capability 绑定；
- 旧研发 / 内容执行测试；
- Tenant 模型偏好与前端知识库文案断言。

本 Issue 未修改或掩盖这些失败。

## Temporary SQLite / Restart Evidence

聚焦测试只使用 pytest `tmp_path`，未触碰活动数据库。最新证据目录：

```text
/private/var/folders/80/w7l2qyt12zx9_n8tg2vgy_pw0000gn/T/pytest-of-yy/pytest-10/
```

- `test_snapshot_and_simulation_p0/runtime-api.sqlite`：`integrity_check=ok`，`runtime_simulation_runs=1`；
- `test_founding_run_survives_res0/runtime-api-restart.sqlite`：`integrity_check=ok`；新 App / Database 实例恢复 `FOUNDING_RUN / INTENT_CAPTURED / nextCheckAt=2026-08-10T00:00:00+00:00`；
- transition audit 反查：`actor=CEO`、`trigger=capture_intent`、`evidence_refs_json=[]`、`next_check_at=2026-08-10T00:00:00+00:00`；
- `runtime-api-isolation.sqlite`：Tenant / Company / Workspace 跨作用域读取返回安全 404；
- `runtime-api-errors.sqlite`：非法 actor 403、非法状态 409、缺失对象 404，响应无 SQLite / path / Traceback。

这些数据库是临时核验证据，不是交付数据库或活动数据源。

## Pre-existing Diff Separation

- 本 Issue 开始前 `backend/app/main.py` 为既有 `90 insertions / 0 deletions`，SHA-256 `91fa0969f29864e83dec680e13d66ae6cc41a118a8964d5cdf6434fa8e7067eb`；
- 本 Issue 只在 Home Router 注册后增加：

```python
from .api.runtime_foundation_router import build_runtime_foundation_router

app.include_router(build_runtime_foundation_router(database))
```

- 当前 `main.py` 为 `93 insertions / 0 deletions`，SHA-256 `7c9749a6ac6bfc7377cd9a448f1efc217ba3f5ad965e2bdafb7e3d8774fd7076`；其余 90 行 diff 均为输入前既有变更；
- API 测试 SHA-256 `76b9081595c89cde55f339a82081b19b291f4c7bb676300a77f0d7969e4cc8f3`；
- 未执行 reset、checkout 或删除清理；未写 frontend、prototype、Desktop、活动数据库或真实平台。

## Known Limitations

- 本 Issue 只提供 Runtime API，不提供 UI、浏览器流程、真实平台发布、平台回执验签或 Desktop 打包证据；
- Simulation 写入仍是可信 Backend 内部能力；未开放前端直写 receipt、manual feedback 或 failure recovery；
- 既有 31 项全量失败继续保留，需各自独立 Issue，不能在本范围顺带修复。

## Final Decision

`RUNTIME-API-001` 验收通过，Decision=`PASS_RUNTIME_API_WITH_BASELINE_BLOCKERS`。下一阶段必须等待 UI Runtime Migration 的正式 Issue；本阶段完成后暂停。
