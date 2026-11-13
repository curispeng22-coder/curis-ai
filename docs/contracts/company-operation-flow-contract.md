# AI 公司运营流程契约

状态：Phase-1A.5 设计冻结

日期：2026-07-10

归属：Workspace 产品规划席

## 产品原则

Curis 管理的是一家由 CEO 经营的 AI 公司，Task 只是内部执行记录，不是产品主入口。

## 冻结后的主链路

```text
CEO
  -> Company
    -> Project
      -> Department（项目所属研发部门）
        -> Employee
          -> Skill / Tool / Model / Connector
            -> Workflow
              -> Task
                -> Result / UsageEvent / AuditEvent
```

`Department` 是 Company 的组织单元，也是 Project 分派员工的范围；它不替代 Project 的 CEO 产品入口。

## 运行规则

1. CEO 在 Company 中创建或选择 Project，Project 是研发目标、上下文和最终结果的承载对象。
2. Project 选择其所属的 Software R&D Department，并从该部门的 Employee 中选择负责人或由 Tech Lead 接收。
3. Employee 只能使用自身有效的 Skill 和 EmployeeCapabilityBinding；Skill 只提供受限提示，Tool Router、Model Gateway 与 Credential Vault 仍是唯一执行边界。
4. Workflow 由 Project 驱动。Workflow 的每个步骤关联 Employee，并把内部 Task 作为执行单元。
5. Result、UsageEvent 和 AuditEvent 必须保持 Project、Workflow、Employee 和 Capability 的可追踪归因；不得包含明文凭据。

## 产品入口与内部底座

| 层级 | 产品定位 | Phase-1B UI 规则 |
| --- | --- | --- |
| Company | CEO 的 AI 公司根对象 | 一级入口 |
| Project | CEO 发起和跟踪研发目标的主对象 | 一级工作入口 |
| Department | 项目资源与员工所属范围 | Project 内的组织上下文 |
| Employee | 具体负责工作的 AI 员工 | Project / Workflow 中可见、可选择 |
| Workflow | Project 的研发 SOP 执行过程 | Project 详情内启动和追踪 |
| Task | Workflow 或员工动作的内部执行记录 | 不作为主导航或新建入口 |

## Phase-1B UI 前置条件

- Phase-1B 必须从 Company 和 Project 开始设计信息架构，不得以 Task Console 作为产品首页。
- UI 的产品方向、导航、页面结构、关键交互和文案由 产品规划席 定义并经总控确认；开发团队只实现批准方案。
- 现有直接 Task Console 可作为兼容或调试能力保留，但不应成为 CEO 默认路径。

## 不做范围

- CEO Office、会议、秘书、复杂组织图。
- 跨部门或跨公司流程。
- Billing、ROI、Marketplace、Payment。
- 自动创建公司、自动招聘员工、复杂自治规划。
