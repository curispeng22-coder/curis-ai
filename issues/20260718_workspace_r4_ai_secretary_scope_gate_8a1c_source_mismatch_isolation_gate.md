# Workspace R4 第8项｜8a.1c｜来源错配隔离 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（真实关联契约已修正；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义来源对象错配时的 fail-closed 规则：任一错配即整体拒绝，不返回部分结果。

## 约束

- 不改历史记录。
- 不改数据库。
- 不新增模型调用。

## 任务

1. 固定 `tenant_id / project_id / company_id / department_id / workflow_id / task_id / employee_id / run_id` 一致性规则。
2. 定义 `workflow_runs + step_results + publish_packages + content_workflow_runs` 之间的来源关联完整性。
3. 失败时统一终止与统一错误码。

## 真实 schema 关联矩阵（修正版）

| 来源 | 允许用于定位/关联的真实列 | 唯一允许路径 | 无法证明时 |
| --- | --- | --- | --- |
| `workflow_runs` | `tenant_id`、`workflow_run_id`、`company_id`、`project_id`、`workflow_instance_id`、`workflow_template_id`、`department_id`、`task_id` | 仅以 `(tenant_id, workflow_run_id)` 定位；其余作用域只与该行同名本源列逐值核验 | 必要本源列为空/类型错误为 `400`；作用域不一致为 `403` |
| `step_results` | `tenant_id`、`step_result_id`、`workflow_step_id`、`employee_id` | 仅允许 `step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)` | 任一中间行缺失为 `404`；tenant 或已解析关联不一致为 `403` |
| `content_publish_packages`（API 投影名 `publish_packages`） | `tenant_id`、`package_id`、`source_workflow` | 仅以 `(tenant_id, package_id)` 定位并核验该行本源字段；`source_workflow` 是本源文本，不是到 RD `workflow_runs` 的外键 | 请求要求证明本表没有的 project/company/RD workflow 关系时即 `403` |
| `content_workflow_runs` | `tenant_id`、`run_id`、`workflow_content_id`、`department_id` | 仅以 `(tenant_id, run_id)` 定位并核验该行本源字段；该 `run_id` 不关联 RD `workflow_runs.workflow_run_id` | 请求要求证明本表没有的 project/company/RD workflow 关系时即 `403` |

### 固定关联规则

- 所有跨表等值关联必须同时包含 `tenant_id`；不得只凭裸 ID 关联。
- `step_results` 不存在 `workflow_run_id`；Run 归属只能经过上表所列 `workflow_steps` 两段路径证明。
- `content_publish_packages.source_workflow` 与 `content_workflow_runs.workflow_content_id` 只代表各自状态机的本源字段；没有现有 schema 关系时不得联到 RD Run。
- 禁止把两个状态机中的同名 `run_id` 视为同一实体，禁止名称匹配、字符串拼接、前后缀替换、默认值或“最近一次”推断。
- `tenant_id` 是最高优先域；已解析跨租户或关联错配为 `403`，对象或必经中间行不存在、状态不可读为 `404`（详见 8a.1a.3a）。

## 统一失败行为

- 任一错配即立即停止，不执行任何后续对象读取。
- 错配错误码统一：`403`（跨域/关联错配）；`404` 仅用于对象不存在或状态不可读。
- 不返回局部匹配结果或空列表；复用 8a.1a.3a 对应状态的固定响应体，避免侧信道。

## 复用规则

- 上述规则在 8a.1a 全链中复用：参数检查通过后再进入 8a.2/8a.3。

## 结果（本批次）

- 状态：IMPLEMENTED（来源错配 fail-closed 关系已按真实 schema 修正；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`。
- `8a.2a` 在本修复 Gate 获得质量 PASS 前继续冻结。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md`
Objective:
定义来源错配 fail-closed 隔离规则。
Special Constraints:
只读边界定义；不改运行引擎。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
