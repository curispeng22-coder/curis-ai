# Workspace R4 第8项｜8a.3a｜建议来源追溯字段 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（真实追溯字段契约已修正；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

明确 Secretary 输出建议的可追溯字段清单，确保每条建议都能回到已归档来源对象。

## 约束

- 不触发新模型调用。
- 不起新 run。
- 不改前端。

## 任务

1. 按四类来源分别固定真实 ID、tenant、时间与已有关系字段，不补统一伪字段。
2. 只有 schema 中已有且可核验的路径才允许携带 run/step/result 关联。
3. 定义必需引用缺失或关系不可证时的 fail-closed 行为。

## 按来源可追溯字段白名单（exact）

### `workflow_runs`

- 必选直出：`tenant_id`、`workflow_run_id`、`created_at`。
- 可选直出：`company_id`、`project_id`、`workflow_instance_id`、`workflow_template_id`、`department_id`、`task_id`、`status`、`updated_at`、`started_at`、`completed_at`、`failed_at`。
- 可证关系：上述作用域字段均来自同一 `(tenant_id, workflow_run_id)` 行；本来源没有可直接证明的 `source_step_id` 或 `source_result_id`。
- 拒绝：必选直出缺失/空白，或请求携带无法从该行证明的 step/result 关系。

### `step_results`

- 必选直出：`tenant_id`、`step_result_id`、`workflow_step_id`、`created_at`。
- 可选直出：`employee_id`、`status`。
- 可证关系：仅允许 `step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)`；由此可引用已核验的 `workflow_run_id` 及该 Run 的本源作用域字段。
- 拒绝：任一必经行缺失、tenant 不一致、关系重复/错配，或请求使用不存在的 `step_results.workflow_run_id`。

### `content_publish_packages`（API 投影名 `publish_packages`）

- 必选直出：`tenant_id`、`package_id`、`created_at`。
- 可选直出：`source_workflow`、`status`、`updated_at`。
- 可证关系：仅限同一 `(tenant_id, package_id)` 行；`source_workflow` 是本源文本，不是 RD Run/Step/Result 外键。
- 拒绝：必选直出缺失/空白，或请求证明 project/company/RD workflow/run/step/result 关系。

### `content_workflow_runs`

- 必选直出：`tenant_id`、`run_id`、`created_at`。
- 可选直出：`workflow_content_id`、`department_id`、`status`、`updated_at`。
- 可证关系：仅限同一 `(tenant_id, run_id)` 行；该 `run_id` 是内容状态机本源 ID，不等于 RD `workflow_runs.workflow_run_id`。
- 拒绝：必选直出缺失/空白，或请求证明 project/company/RD workflow/run/step/result 关系。

## 哈希与文本约束

- 当前四类来源表均不存在稳定持久化的 `source_result_hash`，因此它不是必选或默认返回字段，也不得为本 Gate 新增持久化列。
- 其它只读投影中的临时摘要值不自动成为 Secretary 来源哈希；只有未来单独批准且能从同一来源规范字节稳定复验时才可选用。
- 禁止现场哈希裸 `result`、`final_report`、`summary` 或 `artifacts` 来补足引用；这些正文不得替代来源 ID、tenant、时间或可证关系。
- 禁止同名 ID、名称匹配、字符串拼接、前后缀替换、默认值或“最近一次”推断。

## 统一失败行为

- 任一来源的必选直出缺失，或请求关系无法由上述路径证明，立即拒绝且不返回部分追溯字段。
- 对象/必经行不存在或状态不可读复用 `404` 固定体；参数无效复用 `400`；tenant/作用域/关系错配或关系不可证复用 `403`。
- `summary`、`next_step_hint` 仅能在来源记录与关系全部核验后映射，禁止空引用和裸文本入口。

## 结果（本批次）

- 状态：IMPLEMENTED（追溯字段已按真实 schema 分来源收敛；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md`。
- `8a.3b`、`8a.3c` 在本修复 Gate 获得质量 PASS 前继续冻结。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
Objective:
定义 Secretary 建议来源字段白名单。
Special Constraints:
只读定义；不新增模型执行。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
