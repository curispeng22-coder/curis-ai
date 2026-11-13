# Workspace R4 第8项｜8a.1c 来源错配隔离 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`8c20a4189042effd20cc63b6fdc592924f8dc532`
- 结论：`PASS`

## 结论

四类来源的错配隔离已改为真实 schema 可证明的关联；跨 tenant/已解析关联错配固定 `403`，对象或必经中间行不存在、状态不可读固定 `404`。伪字段、同名 ID 和字符串推断已禁止，拒绝后不继续关联查询、不返回局部结果或空列表。

唯一缺口：无。可推进 `8a.2a`。

## 独立核对

- `workflow_runs` 仅以 `(tenant_id, workflow_run_id)` 定位并核验本行作用域。
- `step_results` 只经 `(tenant_id, workflow_step_id) → workflow_steps → (tenant_id, workflow_run_id) → workflow_runs` 归属 Run。
- 不存在的 `workflow_runs.id`、`step_results.workflow_run_id` 已从契约删除。
- `content_publish_packages` 仅按 tenant、package 与 `source_workflow` 本源字段核验；不得把 `source_workflow` 当 RD Run 外键。
- `content_workflow_runs` 仅按 tenant、run 与本源字段核验；不得把同名 `run_id` 当 RD `workflow_run_id`。
- 本源无法证明 project/company/RD workflow 关系时固定 `403`；禁止名称匹配、字符串拼接、前后缀、默认值和最近一次推断。

## 拒绝行为

| 条件 | 唯一结果 |
| --- | --- |
| 已解析跨 tenant 或关联错配 | `403` + `secretary_source_forbidden` 固定体 |
| 对象不存在、必经中间行缺失或状态不可读 | `404` + `secretary_source_unavailable` 固定体 |

- 任一错配立即终止，不执行后续对象读取。
- 不返回局部对象、部分集合、空列表或 fallback。
- `403/404` 响应仅含 `error_code`、`message`，不泄露实体差异。

## 新鲜证据

固定修订：`feat/roadmap-r1r2 @ 8c20a418`。

```text
.venv/bin/python -m pytest -q \
  backend/tests/test_ai_secretary_source_relation_contract.py \
  backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`8 passed in 0.07s`。覆盖 fresh schema 真实列、StepResult→Run 唯一路径、内容来源本源隔离、禁止推断、403/404 exact 固定体、优先级和查询短路契约。

`git diff --check 8c20a418^ 8c20a418`：通过。该提交仅包含两个契约 Issue 与一个 focused 测试，未修改 schema、API 或运行时。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Gate 为只读契约复核，不声称 Secretary API 已实现。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
