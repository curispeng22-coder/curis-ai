# Project 驱动 Workflow 触发契约

状态：Phase-1A.5 设计冻结

日期：2026-07-10

归属：Workspace 产品规划席

## 冻结决策

Workflow 由 Project 驱动。CEO 不能以独立 Workflow 或独立 Task 作为默认产品入口启动研发协作。

## 触发流程

```text
CEO 创建或选择 Project
  -> Project 处于“规划”状态
  -> CEO 选择官方 Software R&D SOP
  -> 系统校验 Company / Department / Employee / Capability 归属
  -> 创建 WorkflowInstance 与 WorkflowRun
  -> Project 进入“执行”状态
  -> 顺序执行 WorkflowStep
  -> Tech Lead 汇总最终报告
  -> WorkflowRun 完成后，Project 进入“完成”或“阻塞”
```

## 触发前置条件

1. Project、Department 和所有显式选择的 Employee 必须属于当前 tenant 和同一 Company。
2. Phase-1B 仅允许官方 `software_rnd` 顺序 SOP；不开放私有或 marketplace Workflow 模板。
3. WorkflowStep 按既有 `step_order` 顺序分配给角色匹配、可用的 Employee。
4. 每位 Employee 仅可使用自身有效的 EmployeeCapabilityBinding；tenant_private 能力继续经过 Credential Vault resolver。
5. Task、UsageEvent 与 AuditEvent 必须保留 WorkflowRun、WorkflowStep、Employee 和 Capability 的脱敏归因。

## 触发与状态规则

| 事件 | Project | WorkflowRun | 结果 |
| --- | --- | --- | --- |
| CEO 启动 SOP | 规划 -> 执行 | 创建 -> pending / running | 建立执行关联 |
| 任一步骤执行 | 执行 | running | 更新步骤和归因 |
| SOP 成功完成 | 执行 -> 完成 | succeeded | 保存 Tech Lead 最终报告 |
| SOP 步骤失败 | 执行 -> 阻塞 | failed | 保留脱敏错误和审计事件 |
| CEO 归档项目 | 完成/阻塞 -> 归档 | 不新增运行 | Project 只读 |

## Phase-1B UI 要求

- Workflow 启动入口必须位于 Project 详情，不单独作为 CEO 首页入口。
- UI 必须在启动前展示 SOP、Department、关键员工和能力可用性摘要。
- Workflow 详情必须展示顺序步骤、负责人、步骤结果、最终报告和脱敏事件归因。
- 不做拖拽编排、复杂 DAG、自动重试策略、审批流、跨部门流程或 Workflow 市场。

## 不变边界

- 不修改现有 Workflow Runtime 状态机或执行顺序。
- 不绕过 Tool Router、Model Gateway Adapter 或 Credential Vault。
- Workspace 不调用 `/api/platform/*`。
- 不实现 Billing、ROI、Marketplace 或商业规则。
