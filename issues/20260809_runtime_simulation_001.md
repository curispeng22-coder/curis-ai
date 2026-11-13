# RUNTIME-SIMULATION-001：三业务 Runtime Simulation

Status: Completed  
Decision: `PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`  
Input: `PASS_WITH_BASELINE_BLOCKERS`  
Owner: Curis 产品 / Runtime 评审  
Date: 2026-08-09

Runtime Foundation 已通过独立聚焦复核。现在只验证同一 Company OS 是否能承载研发、小红书、抖音 / TikTok 三条业务的可回放运行链；不进入 UI、真实平台 API 或 Desktop。

## 1. 目标

用临时 SQLite 运行并持久化以下场景：

- `RD-001`：研发工作台首个任务“完善 Curis”，CEO 验收后进入下一周期；
- `XHS-001`：小红书内容发布，使用明确来源的外部回执或 CEO 手动反馈；
- `TTK-001`：抖音 / TikTok 内容发布，使用明确来源的外部回执或 CEO 手动反馈；
- 每条业务至少覆盖一个 CEO 等待 / 拒绝 / 失败路径；
- 运行可按 `companyId / workspaceId / scenarioId` 查询，重启后仍可反查。

## 2. 允许文件

### 2.1 现有文件

- `backend/app/runtime/foundation.py`
- `backend/app/runtime/simulation.py`
- `backend/app/runtime/legacy_execution_adapter.py`

仅在发现 Simulation 契约缺陷时修改；不得借机重写 Foundation。

### 2.2 新增文件

- `backend/tests/test_three_business_runtime_simulations.py`
- `docs/reviews/three-business-runtime-simulation-plan-2026-08-09/README.md`
- `docs/reviews/runtime-foundation-review-2026-08-09/README.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
- `reviews/20260809_runtime_simulation_001_review.md`

## 3. 禁止范围

- `frontend/`、`curis-ui-prototype/`、`desktop/`；
- `data/curis.sqlite`、`backend/data/curis.sqlite` 和其他活动数据库；
- 真实小红书、抖音 / TikTok API、账号授权和外部消息；
- 旧研发 / 内容执行链的状态迁移、历史数据回填或物理删除；
- 清单外任何文件；不得使用 reset、checkout 或删除清理既有 dirty diff。

## 4. 必须证明

1. RD / XHS / TTK 各自生成独立 `SimulationRun`，但共用同一 Company / Assistant / 组织内核；
2. PASS 需要非 fixture 的 `VERIFIED` 证据、handoff、CEO decision 和 final state；
3. XHS / TTK 缺少外部回执时不能 PASS；手动反馈必须显式标明来源与未验证状态；
4. `WAITING_CEO` 不可由 SYSTEM 自动恢复；CEO 拒绝 / 失败不能被成功态覆盖；
5. Blueprint / Capability / Platform / ReplyPolicy 变化会使运行失效，历史状态不被覆盖；
6. 临时 SQLite fresh / restart / tenant、Company、Workspace 隔离通过；
7. Foundation 聚焦回归与既有状态 / schema 联合回归继续通过；全量既有 31 项失败不得在本 Issue 扩大修复。

## 5. 关闭条件

- 聚焦 Simulation 测试通过；
- 独立 Review 记录实际命令、结果、临时数据库路径、失败与回滚证据；
- 明确说明这些是 Backend Runtime Simulation 证据，不是 UI Browser Evidence、真实平台发布或 Desktop 完成。

完成后暂停，等待下一 Issue 授权。
