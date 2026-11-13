# Workspace R4 第1项子Issue A1｜项目长期状态字段映射定义

- 日期：2026-07-18
- 状态：PASS — 已复核闭环并对齐 A3
- 父项：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席（A3联合）
- 分支：`feat/roadmap-r1r2`

## 目标

在当前实现读链基础上，给出“项目长期状态”一套唯一可复用映射规则（字段、主源、备援、缺失回退、更新触发），并明确只读边界。

## 约束事实（仅基于当前读链）

当前 `GET /api/workspace/workflows/{workflow_run_id}` 的返回中，`workflow_runs/steps/step_results/usage` 已形成一次性读投影。以下映射仅定义该读链内 `project_status` 与 `artifact` 的字段来源，不改 `projects.status`、不改 runtime 写入语义。

### 字段映射表（最小字段集）

| 字段 | 主源（优先级 1） | 备援（优先级 2） | 缺失回退 | 更新触发 |
| --- | --- | --- | --- | --- |
| `status` | `run["project_status"]["execution_status"]`（由 `_add_read_projection` 计算） | `run["status"] == "succeeded" ? "completed" : "incomplete"`（派生兜底） | `incomplete` | 任意 Run/Step/Result/Usage 读链刷新（读时即时计算） |
| `progress` | 成功步数比率：`len([s for s in steps if s["status"] == "succeeded"])/7`；当为合法闭环时可理解为 `100` | 非法闭环时以 Step 成功数百分比返回 | 无步骤时 `0%`；无合法执行时 `0%` | Run 发生状态变化（step/succeeded/failed）后重算 |
| `last_step` | `steps` 中最大 `step_order` 的 Step（按 order 排序） | `run["steps"][-1]`（存在时） | 无 Step 时 `None` | 每次读取运行时（尤其 step 追加/变更） |
| `last_event_time` | Step/usage/event 中最近更新时间：`max(step.updated_at, step.completed_at, run.updated_at)` | `run["updated_at"]` | 无任一时间戳时 `None` | Step/usage 事件落库/更新时 |
| `last_failure_code` | 第一条失败信息：优先 `step["error"]`（按 `step_order` 最早失败），再使用 usage 的 `status`；失败时 `usage["status"]` 可区分 `network_error / limit_rejected / ...` | 若无 usage 失败，退化为 `run["status"]` 与 `project_status.execution_status` 的失败语义 | 无失败事件时 `None` | 在 Step 失败或 usage 非 `success` 时更新 |
| `last_cost` | 完整且一致有效时：`sum(usage.valid.total_tokens)` | 仅成功 usage 的累计（按 `event_type='usage.model_call'`） | 无模型调用时 `0` | usage 追加后即时可重算 |
| `last_model` | 一致性通过且所有 usage 模型一致时的 `model_name`；同理 `model_gateway_id` | 仅单条 usage 时取该 step 的模型 | 多模型或缺失时 `None`（不猜测） | usage 入库后按模型一致性重算 |
| `updated_at` | `run["updated_at"]` | `project_row["updated_at"]`（只作兼容参考） | 均缺失时 `None` | run 状态或字段更新时 |
| `owner` | `project_row["owner_employee_id"]`（仅来自 `projects`） | `None` | 项目缺失时 `None` | `project update` 后的 `projects` 读取快照 |

### 只读导出边界（本 Issue 固定）

- 只读导出字段：`run.project_status` 与 `run.artifact`。
- `project_status.stored_status` 固定引用 `projects.status`（历史事实），不得把它当作执行驱动状态写入。
- `status = execution_status` 只读推导。
- 关闭态失败下不生成 `artifact`，并保留 `artifact=None`。
- 只写读取契约，不引入新字段回写 `projects`。

### 缺失/冲突时明确行为

- `workflow_run` 缺失：该 Issue 的读模型不满足“已结束 run”条件，`execution_status = incomplete`。
- `steps/results/usage` 缺一方：`execution_status = incomplete`，`progress` 降级，`artifact` 不可生成。
- `project_row` 缺失：`stored_status = None`，但仍允许 run 读取，属于可观测失败场景（`execution_status` 仍按 valid 规则得出）。
- usage 模型不一致或字段类型非法：`execution_status = incomplete`；`artifact` 禁止产出，`last_model/last_cost` 置空/失效。

### 更新规则（冻结）

1. 仅由已存在运行事实重算：`workflow_runs -> workflow_steps -> step_results -> executions -> usage`。
2. 任何人工覆盖 `artifact`/`project_status` 的写入均属于越权；必须拒绝。
3. 读链更新动作只在读取时发生，不改变持久化数据。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_project_state_fact_source_a1_mapping_gate.md`
Objective:
输出并冻结项目长期状态字段映射与失效回退。
Special Constraints:
仅定义读链与衍生，不改 `projects` 写入，不改模型，不改前端，不新增接口。
Next Seat:
系统交付席

## 复核结果（A3 同步）

- 已与 A3 对齐：`steps=7`/`step_results=7` 全部成功、`project_status.execution_status=completed`、`artifact.source=workflow_runs.final_report`、`usage.model_call=7`。
