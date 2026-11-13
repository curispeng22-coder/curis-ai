# Workspace R4 第8项｜8a.3a 建议来源追溯字段 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`dc764e4cd0b637c7467c99bc646f210685afddf6`
- 结论：`PASS`

## 结论

四类来源均使用真实 ID、tenant 与时间字段形成最小追溯引用；只有 StepResult 能沿 tenant + `workflow_steps` 真实路径关联 RD Run。不可证关系、缺失必选引用、伪 ID 或裸文本补足均 fail-closed。

唯一缺口：无。可推进 `8a.3b`。

## 独立核对

| 来源 | 必选字段 | 关系边界 |
| --- | --- | --- |
| `workflow_runs` | `tenant_id`、`workflow_run_id`、`created_at` | 仅同一 Run 行的本源作用域字段 |
| `step_results` | `tenant_id`、`step_result_id`、`workflow_step_id`、`created_at` | 仅经 tenant + `workflow_steps` 关联 `workflow_runs` |
| `content_publish_packages` | `tenant_id`、`package_id`、`created_at` | 仅同一 package 行；不关联 RD Run/Step/Result |
| `content_workflow_runs` | `tenant_id`、`run_id`、`created_at` | 仅同一内容 Run 行；不等同 RD Run ID |

- `source_result_hash` 在当前 schema 中不存在，不是必选或默认字段，也未新增持久化。
- 禁止现场哈希 `result`、`final_report`、`summary`、`artifacts` 补足引用。
- 禁止同名 ID、名称匹配、字符串拼接、前后缀、默认值和最近一次推断。
- 必选引用缺失或关系不可证时立即拒绝，不返回部分追溯字段。

## 新鲜证据

固定修订：`feat/roadmap-r1r2 @ dc764e4c`。

```text
.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_traceability_field_contract.py
```

结果：`4 passed in 0.07s`。覆盖 fresh schema 真实字段、分源必选项、StepResult 唯一关联路径、内容来源隔离和禁止推断/裸文本哈希。

提交仅包含父/修复契约与 focused 测试；未修改 schema、API 或运行时。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Gate 为契约复核，不声称 Secretary API 已实现。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
