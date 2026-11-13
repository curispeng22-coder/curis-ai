# 2026-07-18 Workspace R4 多项目 Session C3｜恢复可追溯性复核

- Issue：`issues/20260718_workspace_r4_multi_project_session_recovery_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`
- 执行方式：只读 SQL 复核（单次、无外网、无 mock）

## 复核结论

固定恢复目标 run：
- `run_target`：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- `tenant_id`：`tenant-a`
- `project_id`：`project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`
- `employee_id`：`emp-7417237e-2f30-4268-807f-88eaaf951bf8`
- `run.status`：`succeeded`

同一员工同项目（恢复范围内）：
- 项目内 run：`4`
- 组成：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`、`wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`、`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`、`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`

跨项目运行隔离核验：
- 其他项目 run：`1`
- 条目：`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`（`project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`）
- `scope_isolation_ok=True`

目标 run 的 step 全量：
- 共 `7` 步，均 `succeeded`，无新增 project 混入、无跨 project run 覆盖。

## 结论

- C3 的“项目级恢复可追溯性”边界成立：恢复对象与其他项目运行事实未互相污染。
- 本次未改代码、不调用外部模型、不触达外网。

Handoff: sent to 产品规划席
