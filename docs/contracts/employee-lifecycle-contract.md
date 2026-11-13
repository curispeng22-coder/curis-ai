# AI 员工生命周期契约

状态：Phase-1A.5 设计冻结

日期：2026-07-10

归属：Workspace 产品规划席

## 生命周期

```text
创建 -> 启用 -> 工作 -> 等待 -> 停用
                 ^      |
                 |______|
```

## 状态定义

| 产品状态 | 含义 | 可进入状态 | 可执行工作 | Phase-1A 运行时映射 |
| --- | --- | --- | --- | --- |
| 创建 | CEO 基于 EmployeeTemplate 创建 EmployeeInstance，尚未进入可分配状态 | 启用、停用 | 否 | 创建事件；现有实例创建后可直接进入启用 |
| 启用 | 员工在所属 Company / Department 内可被 Project 或 Workflow 分配 | 工作、等待、停用 | 可被分配 | `enabled=true`、现有 `idle` |
| 工作 | 员工正在执行 WorkflowStep 或内部 Task | 等待、停用 | 仅执行已分配工作 | 现有 `assigned` |
| 等待 | 员工已无进行中工作，等待下一次分配 | 工作、停用 | 否 | `enabled=true`、现有 `idle` |
| 停用 | 员工不可被新任务或 WorkflowStep 分配 | 启用 | 否 | `enabled=false` 或现有 `disabled` |

## 冻结规则

1. EmployeeInstance 必须属于一个 tenant、Company 和 Department，并保留 `created_from_template_id`。
2. 只有“启用”或“等待”员工可作为新任务、Project 负责人或 WorkflowStep 的候选人。
3. “工作”状态由现有任务或 WorkflowStep 事实驱动，不允许 UI 伪造执行完成。
4. “停用”员工不可接受新分配；进行中的执行遵循现有 Task / Workflow 失败或完成语义，本阶段不新增中断机制。
5. EmployeeCapabilityBinding 是能力权限唯一事实源。EmployeeSkillBinding 只提供受限、非权威的工作提示；EmployeeToolBinding 只是 Tool 类型能力绑定的投影。
6. Employee 不直接持有密钥、选择 Provider 或绕过 Tool Router、Model Gateway、Credential Vault。

## Phase-1B UI 要求

- 员工列表必须展示姓名、角色、Company、Department、生命周期状态、启用状态和已绑定能力摘要。
- 员工创建页以模板为起点；不允许把模板本身当成员工实例编辑。
- UI 可以触发创建、启用、停用和查看能力绑定；“工作/等待”仅展示运行时事实。
- 不做员工人格、绩效、晋升、招聘、复杂汇报线或员工市场。

## 后续实现说明

本契约冻结产品状态词汇。现有 `idle / assigned / disabled` 后端枚举在 Phase-1B 前保持兼容；若后续统一枚举，必须通过独立迁移 Issue，不能由 UI 或本契约隐式改变运行时行为。
