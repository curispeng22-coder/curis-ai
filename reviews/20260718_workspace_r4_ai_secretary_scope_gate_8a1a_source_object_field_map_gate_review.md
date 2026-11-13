# Workspace R4 第8项｜8a.1a.1 来源对象字段映射白名单 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`2da0367be0e8185421523d608f8fb4e1f7c7d737`
- 结论：`PASS`

## 结论

四类来源对象、required/optional 字段、空值策略和 tenant 边界定义完整，且与现有 schema 或只读 API 投影一致。本 Issue 是只读边界定义，不代表 Secretary 运行时接口已经实现。

唯一缺口：无。

## 独立核对

| 来源对象 | Required | Optional | 真实来源核对 |
| --- | --- | --- | --- |
| `workflow_runs` | `tenant_id`、`workflow_run_id`、`company_id`、`project_id`、`workflow_template_id`、`workflow_instance_id`、`department_id`、`status`、`task_id` | `created_at`、`updated_at`、`started_at`、`completed_at`、`failed_at`、`final_report` | 字段均存在于 `workflow_runs`；schema 可空字段被本契约收紧为 required，空值必须拒绝 |
| `step_results` | `tenant_id`、`step_result_id`、`workflow_step_id`、`employee_id`、`status`、`result` | `created_at` | 字段均存在于 `step_results`；通过 `workflow_step_id` 联到 `workflow_steps`，再联到 `workflow_runs` |
| `publish_packages` | `tenant_id`、`package_id`、`source_workflow`、`status`、`platforms_targeted`、`published_platforms`、`artifacts` | `version`、`language`、`brand_voice_ref`、`created_at`、`updated_at` | 现有只读 API 投影来自 `content_publish_packages`；存储字段 `artifacts_json` 被规范化为 `artifacts` 并从响应移除，白名单未暴露存储细节 |
| `content_workflow_runs` | `tenant_id`、`run_id`、`workflow_content_id`、`department_id`、`status`、`steps_total`、`steps_done` | `summary`、`created_at`、`updated_at` | 字段均存在于 `content_workflow_runs` |

## Fail-closed 与隔离

- required 字段为 `null` 或空字符串：立即拒绝。
- optional 字段可空，但不得据此做类型推断。
- 白名单外字段不属于允许输入；当前 Issue 未授权其它注入路径。
- `workflow_runs`、`step_results` 均携带 `tenant_id`；结果通过既定 step/run 链路核验。
- `content_publish_packages` 与 `content_workflow_runs` 的现有读取均使用 `where tenant_id = ?`，只在当前 tenant 内返回；本契约没有扩大到外租户。
- 成果包与内容运行只按 tenant 级独立索引，不在本 Issue 中伪造跨状态机关系。

## 验证证据

执行聚焦验证：

```text
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_v1_wave2_results.py \
  backend/tests/test_workspace_identity_membership.py::test_http_200_401_403_404
```

结果：`4 passed`。覆盖成果包/内容运行只读接口和 200/401/403/404 tenant 身份边界。

另以 `data/curis.sqlite` 只读 schema 复核四类字段，并核对 `Database._content_publish_package_from_row` 的 `artifacts_json` → `artifacts` 投影及两个成果读取方法的 tenant 条件。

## 范围声明

- 未修改实现、数据库或历史记录。
- 未运行全量回归。
- 未推进 8a.1a.2；仅在本 Review 回流后由产品规划席继续调度。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
