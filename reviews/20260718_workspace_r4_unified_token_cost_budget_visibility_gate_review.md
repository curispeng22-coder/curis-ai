# 2026-07-18 Workspace R4 第7项 7b Review

- Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_visibility_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 复核 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- 结论：`PASS`

## 复核范围（只读）

1. `backend/app/main.py` 的 `/api/platform/usage` 与 `/api/platform/usage-meter`：`tenant_id` 必填、无凭证/越权 fail-closed；跨 tenant 查询拒绝返回全量。
2. `backend/app/main.py` 的 `workflow_runtime._add_read_projection`：项目状态与 artifact 仅通过 run/step/result/usage 同步回放。
3. SQL 可见域核验（quality.sqlite）：
   - 同租户同 run: usage 条目=7
   - tenant-b 同 run: 0
   - 其他 run: 0
   - 同租户错 project: 0

## 结果

- 在合法 `tenant-a + 指定 run` 下，仅能读取到该 run 的 7 条 usage 计量（无越权扩散）。
- 不同租户、错误 run、错误 project 组合计数为 0，可作为可见域 fail-closed 依据。
- 未发现该 run 的 `usage.model_call` 存在缺失 `estimated_cost`、`total_tokens <= 0` 或 `outbound_attempted=false`，当前预算读数无伪阴性风险。

## 结论

7b（预算可见域与阻断）在只读验收下通过：预算读取边界与越权闭环成立，不新增调用、无历史回改、无前端改造。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_visibility_gate.md`
Objective:
定义第7项项目预算可见域边界，防止跨租户/跨 run / 跨 project 误读。  
Special Constraints:
只做复核与可见域说明，不新增模型调用，不改历史。  
Next Seat:
产品规划席（7c 收口）→ 质量运行席（聚焦确认）
