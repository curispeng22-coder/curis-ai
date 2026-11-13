# RUNTIME-SIMULATION-001 Final Review

Status: Review
Decision: `PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`
Date: 2026-08-09
Issue: `issues/20260809_runtime_simulation_001.md`
Input: Runtime Foundation `PASS_WITH_BASELINE_BLOCKERS`

## Scope

本轮只完成 Backend Runtime Simulation。RD-001、XHS-001、TTK-001 使用同一 Company、CEO Assistant 与组织参与者，在三个独立 Workspace 中生成独立 `SimulationRun`。未进入 UI、浏览器、Desktop、真实小红书 / 抖音 / TikTok API、活动数据库或旧链迁移。

## Actual Changed Files

- `backend/app/runtime/simulation.py`
  - PASS 前校验当前 Workspace Blueprint 与运行快照一致；失效运行不能 PASS，历史终态不被覆盖；
  - XHS / TTK 必须存在 `PLATFORM_API + VERIFIED + SUCCESS` 的结构化外部回执；
  - `CEO_MANUAL` 回执必须显式为 `UNVERIFIED` 且记录 `recordedBy`；
  - 新增结构化失败解除，失败事件原记录继续保留；
  - PASS 后只更新对应 Workspace 的 Simulation 投影。
- `backend/tests/test_three_business_runtime_simulations.py`
  - 覆盖 RD-001、XHS-001、TTK-001、重启、查询及 Tenant / Company / Workspace fail-closed。
- `reviews/20260809_runtime_simulation_001_review.md`

授权但本 Issue 未修改：

- `backend/app/runtime/foundation.py`
- `backend/app/runtime/legacy_execution_adapter.py`

## Simulation Evidence

### RD-001

- 独立 `SimulationRun`；
- `RUNNING → WAITING_CEO` 后，SYSTEM 自动恢复被 `ActorNotAllowedError` 拒绝；
- CEO 补充决策后恢复原运行；
- Commit / Build / Test 三类非 fixture、`VERIFIED` Evidence 完成验收；
- Cycle 关闭并通过 `NEXT_CYCLE` 反查下一周期；
- handoff、CEO decision、final state 齐全后 PASS。

### XHS-001

- 独立 `SimulationRun`；
- CEO 拒绝形成 `IN_REVIEW → DRAFT` 历史，后续成功态不覆盖该记录；
- 内容按 `DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED → AWAITING_FEEDBACK → REVIEWED` 运行；
- 只有 `PLATFORM_API / VERIFIED / SUCCESS` 外部回执与非 fixture Evidence 齐全后 PASS；
- ReplyPolicy 变化使运行失效，但既有 `PASSED` 历史状态不被改写。

### TTK-001

- 独立 `SimulationRun`；
- `CEO_MANUAL / UNVERIFIED` 反馈单独存在，不能替代平台外部回执；伪造为 `VERIFIED` 被拒；
- 未解决的平台处理失败阻断 PASS；解除后失败事件仍保留，并携带 `resolvedAt` 与 Evidence 引用；
- 补充 `PLATFORM_API / VERIFIED / SUCCESS` 回执后 PASS；
- 独立失败运行保持 `FAILED / FAIL`，不能再次改判 PASS。

## Focused Tests

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_three_business_runtime_simulations.py \
  backend/tests/test_runtime_foundation_*.py \
  backend/tests/test_state_machine.py \
  backend/tests/test_integration_baseline_fixes.py::SchemaGovernanceTests::test_fresh_and_upgraded_schema_match_and_record_version

31 passed, 329 warnings in 2.32s
```

其中三业务 Simulation 新增测试为 4 项；Foundation、既有状态机和 fresh / upgrade schema 联合基线 27 项继续全部通过。

## Full Backend Baseline

```text
backend/.venv/bin/python -m pytest -q backend/tests --tb=short

1272 passed, 31 failed, 2 skipped, 160819 warnings in 154.55s
```

失败数量与授权输入基线完全一致，没有新增失败。本 Issue 不将全量结果伪装为全绿。

31 项既有失败仍归属于封闭范围外的已知漂移：

- `newapi` 与本地 `.env` 中 `newapi-local / deepseek` 默认配置不一致；
- Model Gateway / R3 预期状态码和 Catalog 断言漂移；
- 旧数字员工执行控制链与 Capability 绑定测试；
- 旧研发 / 内容执行测试；
- Tenant 模型偏好与前端知识库文案断言。

本 Issue 未修改上述模块，未扩大修复范围。

## Temporary SQLite / Restart / Isolation

- 三业务测试的数据库由 `tempfile.NamedTemporaryFile(suffix=".sqlite")` 创建；每个测试使用独立的 OS 私有临时 SQLite，测试结束自动删除，不触碰 `data/curis.sqlite`、`backend/data/curis.sqlite` 或其他活动数据库。
- Fresh：每个测试从空临时文件执行 `Database.initialize()`，三业务表、Foundation 投影和约束正常建立。
- Restart：在同一临时 SQLite 上创建新的 `Database` 与 `SimulationRuntime` 实例，仍能按 Company 查询 RD / XHS / TTK 三个运行并恢复 participants。
- Query：运行可按 `company_id / workspace_id / scenario_id` 精确反查。
- Tenant：切换到其他 Tenant 后列表为空，按已知 run id 读取返回 `KeyError`。
- Company / Workspace：以 Company A 创建指向 Company B Workspace 的运行返回 `RuntimeScopeError`。
- Blueprint / Capability 失效：重启后对 RD Workspace 触发 Capability 版本失效，运行保持原历史状态且 PASS 被拒。

临时路径由标准库在测试进程中分配并在 teardown 后删除，因此本 Review 不提供一个可误认为交付数据库的持久路径；可核验入口是上述聚焦命令和测试源码。

## Pre-existing Diff Separation

- `backend/app/main.py` 是输入快照前既有 dirty diff，本 Issue 未写入；当前仍为 `90 insertions / 0 deletions`，SHA-256 `91fa0969f29864e83dec680e13d66ae6cc41a118a8964d5cdf6434fa8e7067eb`。
- `backend/app/runtime/foundation.py` 为前一 Foundation Issue 的既有未跟踪文件，本 Issue 未写入；SHA-256 `55429a9bd911fd380f5ab78e8786cbb2a589c4b66286da5ac785b84b60adb0c0`。
- `backend/app/runtime/legacy_execution_adapter.py` 为前一 Foundation Issue 的既有未跟踪文件，本 Issue 未写入；SHA-256 `ae7e92712f140d2eb548fc448c341b4845b7185eefbffd42edfe3ef05a81ea8b`。
- 本 Issue 的 Runtime 实现集中在 `simulation.py`，SHA-256 `1aa79b8a4a8d68842de4aef35dd5467df7c712f2145b75ec9f0b2494854c9265`；新增三业务测试 SHA-256 `7fd5346c2a07e415a6cd641cde4737cad862e0d441d4f3ea020882938a379bc2`。
- 未执行 reset、checkout、删除清理；未写活动数据库；未运行前端或 Desktop 命令。

## Boundary / Known Limitations

- 平台回执是临时 SQLite 内的结构化、非 fixture 验证数据，用于证明 Runtime 合同，不是真实平台发布证明。
- 本 Review 不代表 UI Browser Evidence、导航迁移、Assistant UI、Tauri 壳或 `.app` 完成。
- 真实平台 API、账号授权、回执验签与手动反馈 UI 仍需后续独立 Issue；本阶段不提前实现。

## Final Decision

`RUNTIME-SIMULATION-001` 的 Backend Runtime Simulation 验收项通过，结论为 `PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`。既有 31 项全量失败未增加，归属清单外旧基线。阶段完成后暂停，等待下一阶段正式授权。
