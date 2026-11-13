# 2026-07-18 Workspace R4 多项目 Session C1｜Scope/Key 规范复核

- Issue：`issues/20260718_workspace_r4_multi_project_session_scope_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`
- 执行方式：只读 SQL 采样

## 复核结论

- `tenant-a` 下已存在至少 2 个多项目候选员工，满足前置样本要求。
- 选用样本 `emp-7417237e-2f30-4268-807f-88eaaf951bf8`，关联两个项目：
  - `project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`
  - `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`
- 按拟定 key：
  - `session_scope:{tenant_id}:{employee_id}:{project_id}:{scope}`
  - 示例 scope：`owner / execution / context`
  - 产出 key 数：`6`
  - 去重后唯一数：`6`
  - 说明：`project` + `scope` 纳入维度后无冲突
- 数据级 fail-closed 先验：`tenant-a` 下 `workflow_runs.project_id IS NULL` 记录为 `0`
- `multi-project candidates=2`，最小冲突面已具备

## 结论

- C1 scope/key 规范在当前 DB 事实下可闭环通过。
- 本次未改模型、未调用外网、未改运行契约。

Handoff: sent to 质量运行席（C2 联动）
