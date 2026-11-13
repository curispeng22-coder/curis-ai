# CEO Dashboard 数据就绪度评审

状态：Phase-1B.5 设计评审

日期：2026-07-10

## 评审结论

CEO Dashboard 可以进入产品与 UI 设计，但第一版必须按数据就绪度分层展示。已存在的事实数据可以聚合；未持久化的 Value Event、知识增长指标和增长评分只能显示为空状态、预留状态或在后续 Gate 后启用。

## 数据来源矩阵

| Dashboard 领域 | 主要来源 | 当前可用性 | 可展示内容 | 限制 |
| --- | --- | --- | --- | --- |
| Company Health | CompanyRuntime、ProjectRuntime、DepartmentRuntime | 可聚合 | Company 状态、活跃/阻塞项目数、部门可用状态 | 无统一健康评分 |
| Department Overview | DepartmentInstance、EmployeeInstance | 可聚合 | 研发部门状态、员工数量、负责人 | 仅 `software_rnd` |
| Project Progress | Project、WorkflowRun、WorkflowStep、StepResult | 可聚合 | Project 状态、Workflow 状态、步骤完成度、最终报告状态 | 不做预测进度 |
| Project Risk | Project `blocked`、Workflow failed、缺失负责人/能力事实 | 部分就绪 | 明确阻塞与失败事实 | 不做 AI 风险评分 |
| Employee Status | EmployeeInstance、WorkflowStep / Assignment | 可聚合 | 启用、停用、工作/等待映射 | 产品生命周期词与后端枚举暂为映射关系 |
| Employee Load | 活跃 WorkflowStep、Task 归因 | 可聚合 | 每位员工的进行中工作数 | 不作产能或绩效结论 |
| Employee Growth | EmployeeInstance、Skill/Tool Binding、完成记录 | 需定义指标 | 新增员工、绑定变化、完成工作数 | 无正式成长评分 |
| Token Usage | UsageEvent | 可聚合 | prompt/completion/total token | 仅已写入事件 |
| Model Usage | UsageEvent、Model Gateway metadata | 可聚合 | 模型名称、调用次数、Token 分布 | 不显示 Provider 密钥或原始响应 |
| AI Cost | UsageEvent `estimated_cost` | 可聚合 | 估算成本趋势与分类 | 非账单、非价格、非 Invoice |
| Value Event | Value Event Contract | 契约预留 | 后续记录列表 | 当前不得假定持久化存在 |
| Estimated Impact | Value Event `estimated_value` | 契约预留 | 未来经用户确认的估算影响 | 非 ROI、非收费依据 |
| Skill Usage | EmployeeSkillBinding、Task/Workflow attribution | 部分就绪 | 绑定覆盖与后续使用关联 | 现有 UsageEvent 无独立 Skill id 字段 |
| Tool Usage | UsageEvent capability fields、EmployeeCapabilityBinding | 可聚合 | Tool 调用次数、状态、来源 | 不显示私有 config / credential |
| Knowledge Growth | Project Memory、Execution Summary Memory、Knowledge 文档 | 部分就绪 | 记录数量、更新时间、来源摘要 | 无统一知识库持久化计数模型 |

## 数据边界

### Workspace 事实源

- Company、Department、Project、Employee、Skill Binding、Tool Binding。
- WorkflowRun、WorkflowStep、Task、StepResult。
- tenant-scoped Usage Event 与脱敏 Audit Event。
- Project Memory 和已批准的知识文档摘要。

### 不属于 Dashboard 的数据

- Plan、Quota、Pricing、Billing Event、Invoice、支付状态。
- tenant_private 明文凭据、可解析 credential_ref、config_ref、Provider 原始响应。
- 自动 ROI、预测收入、自动价值结论或跨 tenant 对比。

## 第一版数据策略

1. Widget 必须显式声明 `data_level`：`ready`、`derived`、`reserved`。
2. `ready` Widget 可在后续 UI Issue 中读取已有 Workspace 只读数据。
3. `derived` Widget 只能采用可解释事实聚合，必须展示来源或计算说明。
4. `reserved` Widget 展示受控空状态或“等待数据接入”，不得伪造示例、模拟数据或商业结论。
5. Value Event、Employee Growth 与 Knowledge Growth 的持久化/聚合要先通过独立数据契约和实现 Gate。

## 风险与前置 Gate

| 风险 | 处理方式 |
| --- | --- |
| `estimated_cost` 被误解为账单 | 固定文案为“估算消耗”，不展示价格、账单或额度 |
| Value Event 被误解为 ROI | 标记为记录/估算，需用户确认后才可展示数值 |
| Knowledge 指标缺少统一数据模型 | 第一版只显示来源摘要或空状态 |
| Widget 自定义造成越权查询 | Widget 只允许 Catalog 类型和受限 scope，禁止任意查询 |
| Admin / Workspace 数据混淆 | Dashboard 不读取或调用 `/api/platform/*`；跨线数据必须 Shared Contract |
