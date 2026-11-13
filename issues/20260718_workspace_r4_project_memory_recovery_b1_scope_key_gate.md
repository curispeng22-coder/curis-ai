# Workspace R4 第1项子Issue B1｜Memory Scope 与 Key 规范

- 日期：2026-07-18
- 状态：PASS — 质量复核完成
- 前置：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- 父项：`issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

定义 `tenant_id + project_id + scope` 规范下的 Memory 键值模型（含 `run / step / execution / usage / project / owner`），并明确可复用/不可复用、冲突判定与只读边界。

## Must Do

1. 定义 `scope` 字典与版本化 key 格式。
2. 明确同一条目可复用、不可复用与冲突判定。
3. 明确 `Memory` 与历史运行记录的读写边界（只读优先；必要时可登记追加）。

## Scope 与 Key 规范（v1）

固定版本：`workspace.project_memory.scope.v1`

### 1）Scope 字典（最小六类）

| Scope | Key 必填字段（最小） | 主读来源 | 唯一性（主键） |
| --- | --- | --- | --- |
| `project` | `tenant_id` `project_id` `scope_version` `scope_name` | `projects` + `workflow_runs` | `tenant_id + project_id + scope_version` |
| `run` | `tenant_id` `project_id` `run_id` `scope_version` `scope_name` | `workflow_runs` + `workflow_steps` + `step_results` + `executions` + `usage` | `workflow_run_id + scope_version` |
| `step` | `tenant_id` `project_id` `run_id` `step_id` `scope_version` `scope_name` | `workflow_steps` | `workflow_step_id + scope_version` |
| `execution` | `tenant_id` `project_id` `task_id` `execution_id` `scope_version` `scope_name` | `executions` | `execution_id + scope_version` |
| `usage` | `tenant_id` `project_id` `task_id` `usage_event_id` `step_id` `scope_version` `scope_name` | `evolution_events`（`event_type='usage.model_call'`） | `event_id + scope_version` |
| `owner` | `tenant_id` `project_id` `owner_employee_id` `scope_version` `scope_name` | `projects.owner_employee_id` | `tenant_id + project_id + scope_version` |

### 2）Memory Key 生成规则（最小固定拼接）

- 统一 key 前缀：`mem.v1.{scope}`。
- 运行期 key：
  - `project`: `mem.v1.project|tenant={tenant_id}|project={project_id}|version=workspace.project_memory.scope.v1`
  - `run`: `mem.v1.run|tenant={tenant_id}|project={project_id}|run={workflow_run_id}|version=workspace.project_memory.scope.v1`
  - `step`: `mem.v1.step|tenant={tenant_id}|project={project_id}|run={workflow_run_id}|step={workflow_step_id}|version=workspace.project_memory.scope.v1`
  - `execution`: `mem.v1.execution|tenant={tenant_id}|project={project_id}|task={task_id}|execution={execution_id}|version=workspace.project_memory.scope.v1`
  - `usage`: `mem.v1.usage|tenant={tenant_id}|project={project_id}|task={task_id}|step={workflow_step_id}|usage={event_id}|version=workspace.project_memory.scope.v1`
  - `owner`: `mem.v1.owner|tenant={tenant_id}|project={project_id}|owner={owner_employee_id}|version=workspace.project_memory.scope.v1`

### 3）可复用与不可复用

- 可复用：同一 `tenant_id + scope + 主键` 下的 key 重放读取应稳定命中、可重复展示。
- 不可复用：`final_report` 文本不作为 owner/project 的写入输入。
- 历史失败 run 的 `artifact`/`project_status` 在本项不得回填任何历史实体，仅保留读视角。

### 4）冲突判定

- 同 scope 同主键重复且 payload 不一致时：判定为“冲突恢复样本”，优先 `project_scope` 只读映射，不做自动修复。
- 同一 run 下 step_order 重复时：判定为结构异常，`project_status` 不得进入 completed。
- scope 读链缺失任一主元（如 `run_id`）时：判定 `recoverable=false` 并停止续推。

### 5）读写边界

- 读边界：`project/owner` 只读 `projects`；`run/step/usage` 只读现有 workspace 读链（本 issue 不改 API、DB 结构、不改前端）。
- 写边界：不新增持久化项；不变更 `project_status`、`workflow_runs`、`workflow_steps`、`executions`、`step_results`、`evolution_events`。

### 6）最小核对命令（只读，供实现后复核）

```bash
sqlite3 '/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite' \
  "select workflow_run_id,status,tenant_id,project_id,task_id from workflow_runs where tenant_id='tenant-a' and project_id='project-e84e06d4-f014-4326-abcd-e6d9aea6ff95' order by created_at;"
```

- 该查询用于回收每个 run 的最小 project 作用域，后续 step/execution/usage 需使用该 run/task 继续映射。

## 更新

- 与 A1/A2 映射一致：`tenant_id + project_id + scope` 作为 Memory 外层主约束。
- 前置链路已完成，B1 已复核 PASS；继续执行 `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`，B3 待 B2 收口后执行。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
Objective:
定义 Memory key 与 scope 规范，形成可复用、可复核的唯一标识规则。
Special Constraints:
不得新增服务/数据库；不得启动新 Run；不得并行打开第2~9项。
Next Seat:
产品规划席
