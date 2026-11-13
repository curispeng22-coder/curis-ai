# Workspace R4 第8项｜8a.3a 来源追溯真实字段契约修复 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_field_contract_fix_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`dc764e4cd0b637c7467c99bc646f210685afddf6`
- 结论：`PASS`

## 结论

四类来源的追溯字段已按真实 schema 分源锁定；只有 StepResult 可经 tenant + `workflow_steps` 真实路径关联 RD Run。内容来源不再伪造跨状态机关系，`source_result_hash` 不作为必填或持久化字段。

唯一缺口：无。本修复 Gate 通过；需重派父项 8a.3a 复核，完成前 `8a.3b/8a.3c` 继续冻结。

## 独立核对

| 来源 | 必选追溯字段 | 允许关系 |
| --- | --- | --- |
| `workflow_runs` | `tenant_id`、`workflow_run_id`、`created_at` | 仅同一 Run 行的本源作用域字段 |
| `step_results` | `tenant_id`、`step_result_id`、`workflow_step_id`、`created_at` | 仅经 tenant + `workflow_steps` 关联 `workflow_runs` |
| `content_publish_packages` | `tenant_id`、`package_id`、`created_at` | 仅同一 package 行；`source_workflow` 不是 RD 外键 |
| `content_workflow_runs` | `tenant_id`、`run_id`、`created_at` | 仅同一内容 Run 行；该 ID 不等于 RD Run ID |

- 关系不可证或必选引用缺失时立即拒绝，不返回部分追溯字段。
- `source_result_hash` 在四类来源 schema 中不存在，不是必选或默认返回字段，也未新增持久化列。
- 禁止现场哈希 `result/final_report/summary/artifacts`，禁止裸文本替代来源引用。
- 禁止同名 ID、名称匹配、字符串拼接、前后缀、默认值和最近一次推断。

## 新鲜证据

提交范围：3 个文件，仅父/修复契约与 focused 测试；未修改 schema、API 或运行时。

```text
.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_traceability_field_contract.py
```

结果：`4 passed in 0.07s`。使用 fresh database 核对真实列、分源必选字段、StepResult 唯一关联路径、内容来源隔离和禁止推断/裸文本哈希。

`git diff --check dc764e4c^ dc764e4c`：通过。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Review 不替代父项 8a.3a 的重新复核。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
