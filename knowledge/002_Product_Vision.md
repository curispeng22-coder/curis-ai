# Product Vision

## Vision

Curis Workspace's final product goal is an AI Company System.

It should let a solo entrepreneur operate like a small AI-powered company.

The product should eventually coordinate business scopes, departments, AI employees, workflows, knowledge, tools, models, costs, and external capability providers.

## Layered Product Architecture

```text
L6 经济层: ROI / 成本 / 优化
L5 公司层: 组织 / 部门 / 职责
L4 工作流层: 任务拆解 / 编排 / 状态流转
L3 工具层: 工具注册 / 路由 / 执行 / fallback
L2 员工层: AI执行角色 / 员工能力 / 角色偏好
L1 执行层: Task / Run / Status / History / Result
L0 产品层: 用户界面 / 操作台 / 可视化
```

## Current Strategy

Do not build the full company system first.

Current launch scope is AI Task Executor MVP. It proves the execution foundation and builds the framework needed for future company layers.

Current gated scope may cover:

- L0 产品层: task console and execution visualization.
- L1 执行层: task create, run, status, history, result.
- L2 员工层: minimal AI Employee coordinator required for execution.
- L3 工具层: tool registry, router, executor, fallback.
- L4 工作流层: workflow generation, trace, and stateful execution.

Future layers remain out of current scope until explicitly approved:

- L5 公司层: organization, department, role ownership, responsibility system.
- L6 经济层: ROI, cost, optimization, economic decisioning.

The current execution loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Sprint Roadmap

| Sprint | Name | Goal |
| --- | --- | --- |
| Sprint 0 | AI 公司执行内核 | Prove execution loop and persistence foundation |
| Sprint 1A | Meta Development System | Add self-managed development planning before visualization |
| Sprint 1B | Controlled Self-Evolution Kernel | Add strict evolution control, simulation, risk analysis, and rollback records |
| Sprint 1 | 公司运行可视化 | Visualize task execution, state, tools, traces, and learning |
| Sprint 2 | 统一任务操作台 | Provide daily task entry, history, run control, and execution review |
| Sprint 3 | 轻量角色与职责系统 | Add lightweight role ownership and responsibility labels |
| Sprint 4 | 多入口与高级 UI | Add multiple entry points and higher-interaction UI |

## Non-Goals For Current Gate

- Company CRUD
- Employee CRUD
- Multi-agent system
- Business modules
- ROI system
- Advanced UI
- Uncontrolled architecture changes
- Automatic code self-modification without approval
