# 2026-07-18 Workspace R4 多项目 Session C2｜跨项目切换隔离复核

- Issue：`issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`
- 执行方式：只读 SQL 采样（单员工两项目集合）

## 复核结论

- 在 `tenant-a` 选取样本员工 `emp-7417237e-2f30-4268-807f-88eaaf951bf8`，其项目/Run 分布：
  - `project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`：`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`
  - `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50` / `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff` / `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` / `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`
- 项目 run 集无交集：`wfr` 集合两项目互斥（交集为空）。
- `workflow_runs` 级反查 `run_id` 与非当前 `project_id` 匹配计数为 `0`（反向读无串项目命中）。
- 该验证仅覆盖数据库聚焦读边界，符合 C2 隔离核验目标。

## 结论

- C2 跨项目上下文隔离可闭环通过。
- 未新增 API，不改 Gateway/Runtime，不出网，不改历史 run。

Handoff: sent to 质量运行席（C3）
