# Workspace R4 第8项｜8a.2b 跨租户与错配封锁 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md`
- 分支：`feat/roadmap-r1r2`
- 复核基线：`8c20a4189042effd20cc63b6fdc592924f8dc532` + 当前 Issue 修正版
- 结论：`PASS`

## 结论

原 Review 指出的断链歧义已消除：必经对象或中间行未命中固定 `404`；对象均存在但 tenant/归属/关联值不一致固定 `403`。身份缺失、内容来源本源核验、固定响应、禁止推断/fallback 与零 partial 均保持成立。

唯一缺口：无。可推进 `8a.2c`。

## 独立核对

| 场景 | 唯一结果 |
| --- | --- |
| 身份域缺失或无效 | `401` |
| 必经对象、中间 Step/Run 或目标对象未命中/不可见 | `404` |
| 对象均存在，但 tenant/project/run/result/task 归属或关联值不一致 | `403` |
| package/content 被要求证明本源不存在的 project/run/task 关系 | `403` |

- StepResult 仅经 tenant + `workflow_steps` 真实路径关联 Run，不使用伪字段。
- package/content 只核验本源字段与 tenant，不把同名 ID、名称或字符串拼接当关联。
- 任一失败立即终止，不返回局部对象、其它 tenant 空列表或 fallback。
- `401/403/404` 继续复用 8a.1a.3a exact body，且仅允许 `error_code`、`message`。

## 新鲜证据

```text
.venv/bin/python -m pytest -q \
  backend/tests/test_ai_secretary_source_relation_contract.py \
  backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`8 passed in 0.07s`。覆盖真实 schema 关联、本源隔离、禁止推断、固定响应体、优先级和查询短路契约。

静态核对当前 Issue：缺失 `404` 与已存在错配 `403` 已拆成互斥条件，原“任一断链 `403`”表述不存在。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Gate 为契约复核，不声称 Secretary API 已实现。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
