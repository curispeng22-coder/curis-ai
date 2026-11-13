# Workspace R4 第8项｜8a.1c 来源真实关联契约修复 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_relation_contract_fix_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`8c20a4189042effd20cc63b6fdc592924f8dc532`
- 结论：`PASS`

## 结论

四类来源关系已改为现有 schema 可证明的真实路径，原 Review 指出的伪字段和伪跨状态机关联已删除；关系不可证明时明确 fail-closed。

唯一缺口：无。本修复 Gate 通过；需回到父项重新复核 8a.1c，完成前 `8a.2a` 继续冻结。

## 独立核对

- `workflow_runs` 唯一使用 `(tenant_id, workflow_run_id)` 定位。
- `step_results` 到 Run 仅允许：`(tenant_id, workflow_step_id) → workflow_steps → (tenant_id, workflow_run_id) → workflow_runs`。
- 已明确不存在 `workflow_runs.id` 和 `step_results.workflow_run_id`，不得作为关联依据。
- `content_publish_packages` 只核验 `(tenant_id, package_id)` 与本源 `source_workflow`；该字段不是 RD Run 外键。
- `content_workflow_runs` 只核验 `(tenant_id, run_id)` 与本源字段；该 `run_id` 不关联 RD `workflow_run_id`。
- project/company/RD workflow 关系无现有字段可证明时固定 `403`，不允许同名 ID、名称、字符串拼接、默认值或最近一次推断。
- 任一错配立即停止；中间对象不存在为 `404`，已解析作用域不一致为 `403`，均复用既有固定响应体。

## 新鲜证据

提交范围：3 个文件，仅契约 Issue 与 focused 测试；未修改 schema、API 或运行时。

```text
.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_source_relation_contract.py
```

结果：`4 passed in 0.07s`。测试使用 fresh database schema 核对真实列、StepResult→Run 路径、内容来源本源隔离和禁止推断规则。

`git diff --check 8c20a418^ 8c20a418`：通过。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Review 不替代父项 8a.1c 的重新复核。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
