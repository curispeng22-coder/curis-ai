# RUNTIME-FOUNDATION-001 Implementation Review

Status: Review
Decision: `READY_FOR_INDEPENDENT_REVIEW_WITH_BASELINE_BLOCKERS`
Date: 2026-08-09
Input: `docs/reviews/runtime-foundation-review-2026-08-09/INPUT_SNAPSHOT_2026-08-09.md`

## Scope

仅实施授权的 Backend Runtime Foundation。未修改 `backend/app/main.py`、前端、原型、Desktop、活动数据库、旧研发 / 内容模块或真实平台 API。

## Changed Files

- `backend/app/database.py`：只新增 Runtime Foundation additive migration hook；文件中的 capability ownership 等其他 diff 为输入快照前既有变更。
- `backend/app/runtime/__init__.py`
- `backend/app/runtime/models.py`
- `backend/app/runtime/states.py`
- `backend/app/runtime/registry.py`
- `backend/app/runtime/store.py`
- `backend/app/runtime/foundation.py`
- `backend/app/runtime/simulation.py`
- `backend/app/runtime/legacy_execution_adapter.py`
- `backend/tests/test_runtime_foundation_state_contracts.py`
- `backend/tests/test_runtime_foundation_persistence.py`
- `backend/tests/test_runtime_foundation_isolation.py`
- `backend/tests/test_runtime_foundation_simulation.py`
- `backend/tests/test_runtime_foundation_legacy_adapter.py`
- 本 Review 与授权的三份治理同步文件。

授权但无实际修改：`backend/app/runtime/state_machine.py`。

## Runtime Evidence

- First Arrival：CEO 确认前不建 Company；Company、唯一 CEOAssistant、FoundingRun 状态和反查 Link 同事务写入；失败回滚，不显示假成功。
- Organization：AIEmployee、RoleSlot、CapabilityBinding 拥有独立状态、`orgVersion` / presence / capability reference 与可反查 Link。
- Responsibility：Cycle → Handoff → Evidence → Acceptance → DecisionPacket，以及 Assistant → Brief / Handoff / DecisionPacket / Closeout 可双向查询。
- Content：ContentItem 审核必须绑定批准版本；发布 / 自动回复必须有具体版本和外部回执或 CEO 手动反馈引用。
- Evidence：生命周期、验证等级、证据条件和异常状态正交；fixture 永远 `UNVERIFIED`，不能支持 Simulation PASS。
- Legacy：只保存 `workflow_run / workflow_step / content_workflow_run` 的 `executionRef`，不接管旧状态。

## Tests

```text
backend/.venv/bin/python -m pytest -q backend/tests/test_runtime_foundation_*.py
11 passed

backend/.venv/bin/python -m pytest -q \
  backend/tests/test_runtime_foundation_*.py \
  backend/tests/test_state_machine.py \
  backend/tests/test_integration_baseline_fixes.py::SchemaGovernanceTests::test_fresh_and_upgraded_schema_match_and_record_version
27 passed

backend/.venv/bin/python -m pytest -q backend/tests --tb=short
1267 passed, 31 failed, 2 skipped
```

全量失败不可归为 Foundation PASS：它们集中于输入快照前既有的 `newapi` 与本地 `.env` 中 `newapi-local / deepseek-v4-pro` 默认漂移、Model Gateway 状态码漂移、数字员工旧能力绑定、旧研发 / 内容执行及前端知识库文案断言。相关文件均在封闭清单外，本 Issue 未修改。

## Temporary SQLite

Evidence directory: `/tmp/curis-runtime-foundation-acm2y3fg/`

- `fresh.sqlite`：重复 `Database.initialize()` 通过；`integrity_check=ok`。
- `upgrade.sqlite`：从旧 `workspaces` / `runtime_transition_log` 列形状和缺失 Foundation 表升级；重复初始化通过；与 fresh 的 Foundation 字段 / 类型 / 非空 / 默认值语义一致；`integrity_check=ok`。
- Restart：新 `Database` 实例可恢复 Cycle → Evidence 反查。
- Isolation：其他 tenant 读取相同 entity id 返回 `KeyError`；跨 Company / Workspace Link 被拒。
- Simulation：RD-001 `DRAFT → RUNNING → REVIEWED → PASSED`，`passStatus=PASS`，状态引用 3 条；历史不被失效动作覆盖。

## Pre-existing Diff Separation

- 最终输入快照已记录 `backend/app/main.py` 为既有 dirty 范围；本轮没有任何写入该文件的操作。当前 `main.py` 仍为 `90 insertions / 0 deletions` 的既有 diff，SHA-256 `91fa0969f29864e83dec680e13d66ae6cc41a118a8964d5cdf6434fa8e7067eb`。
- `backend/app/database.py` 在输入快照时已为 SHA-256 `93247b08...` 且包含既有 capability ownership / strategy meeting diff；本轮仅在初始化流程增加 3 行 Foundation migration hook。最终 SHA-256 `eda7f286...`。
- 未执行 reset、checkout、删除清理、活动数据库写入、前端或 Desktop 命令。

## Decision / Next Seat

实现席结论：`READY_FOR_INDEPENDENT_REVIEW_WITH_BASELINE_BLOCKERS`。

Next Seat：独立质量运行席。先复核本 Review 的授权 diff、聚焦测试和临时 SQLite；再判定 31 项既有全量失败是否阻止 Foundation PASS。未取得独立 PASS 前，不进入三业务 Simulation、UI 或 Desktop。
