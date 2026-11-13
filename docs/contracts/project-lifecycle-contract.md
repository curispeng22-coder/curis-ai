# 项目生命周期契约

状态：Phase-1A.5 设计冻结

日期：2026-07-10

归属：Workspace 产品规划席

## 生命周期

```text
创建 -> 规划 -> 执行 -> 完成 -> 归档
           |       |
           +----阻塞-+
```

## 状态定义

| 产品状态 | 含义 | 允许动作 | 当前后端兼容映射 |
| --- | --- | --- | --- |
| 创建 | CEO 提交项目名称、目标和 Company 归属后的生成事件 | 进入规划、归档 | 创建事件；持久化后默认进入规划 |
| 规划 | 定义目标、Department、负责人和研发 SOP | 修改项目、指定员工、启动 Workflow、归档 | `planned` |
| 执行 | 已有正在运行或已启动的 Project 驱动 Workflow | 查看进度、查看步骤和结果、标记阻塞 | `active` |
| 阻塞 | 需要 CEO 或后续机制处理的项目状态 | 恢复执行、归档 | `blocked` |
| 完成 | 最终报告已经可供 CEO 查看 | 归档、创建后续项目 | `completed` |
| 归档 | 不再接受新的 Workflow 或 Task 关联 | 只读查看 | `archived` |

## 冻结规则

1. Project 必须属于一个 Company；Department 和 owner_employee_id 必须属于同一 tenant 和 Company。
2. Project 是 CEO 发起研发目标的主对象，包含目标、说明、状态、负责人、Workflow 关联和最终报告引用。
3. 新研发工作从 Project 发起，再由 Project 启动指定的官方 Software R&D SOP Workflow。
4. Project 的 Task 仅是内部关联：Task 必须携带同一 Company / Project 归属，不能被挂到另一公司的 Workflow。
5. Project 状态不替代 WorkflowRun 状态：Project 汇总其工作流事实，WorkflowRun 仍独立维护顺序步骤状态。
6. Project 不含商业套餐、配额、价格、账单、密钥或 Provider 配置。

## Phase-1B UI 要求

- Project 是 Company 工作区的主列表和默认新建入口。
- 创建 Project 的最小字段：Company、名称、目标、可选 Department、可选负责人、说明。
- Project 详情必须显示当前生命周期、负责人、关联研发 SOP、执行进度、最终报告和内部任务摘要。
- 不做 Kanban、Sprint 管理、客户协作门户、跨公司项目或复杂项目组合管理。

## 后续实现说明

现有 `planned / active / blocked / completed / archived` 后端值继续有效。本契约把产品展示词统一为“规划 / 执行 / 阻塞 / 完成 / 归档”；任何数据枚举迁移必须通过独立后端 Issue。
