# CEO Dashboard 运行时契约

状态：Phase-1B.5 设计冻结

日期：2026-07-10

归属：Workspace；不改变 Admin 商业治理边界。

## 对象关系

```text
DashboardTemplate（默认布局定义）
  -> DashboardInstance（tenant / Company 的 CEO 私有布局）
    -> DashboardWidget（一个可配置的 Widget 实例）
      -> Widget Catalog（固定的可用 Widget 类型）
```

## DashboardTemplate

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `dashboard_template_id` | string | 是 | 稳定模板 ID |
| `name` | string | 是 | 例如“AI 公司经营驾驶舱” |
| `version` | string | 是 | 模板展示版本 |
| `source` | enum | 是 | `official` / `tenant_private` / `marketplace`；本阶段仅 official 默认模板 |
| `layout_schema` | object | 是 | Widget 区域、默认顺序、尺寸约束；不含数据或敏感配置 |
| `default_widget_types` | string[] | 是 | 默认启用的 Widget Catalog 类型 |
| `enabled` | boolean | 是 | 是否可创建实例 |
| `created_at` | datetime | 是 | 创建时间 |

## DashboardInstance

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `dashboard_instance_id` | string | 是 | tenant 私有实例 ID |
| `tenant_id` | string | 是 | tenant 隔离 |
| `company_id` | string | 是 | 当前 Company 经营上下文 |
| `created_from_template_id` | string nullable | 否 | 来源模板；空白布局可为空 |
| `created_from_template_version` | string nullable | 否 | 来源版本；不可变追溯字段 |
| `name` | string | 是 | CEO 可改的显示名 |
| `layout_preferences` | object | 是 | Widget 排序、显示/隐藏、尺寸；不能存 API、凭据或商业规则 |
| `status` | enum | 是 | `active` / `disabled` |
| `created_at` / `updated_at` | datetime | 是 | 生命周期字段 |

## DashboardWidget

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `widget_id` | string | 是 | Widget 实例 ID |
| `dashboard_instance_id` | string | 是 | 所属 DashboardInstance |
| `widget_type` | enum | 是 | 必须来自 Widget Catalog |
| `title_override` | string nullable | 否 | CEO 可改展示标题 |
| `scope` | object | 是 | 仅 Company、Project、Department、时间范围等非敏感过滤条件 |
| `position` | object | 是 | 布局位置与尺寸 |
| `display_preferences` | object | 是 | 允许的展示偏好，不可存数据源 URL 或查询语句 |
| `enabled` | boolean | 是 | CEO 可显示/隐藏 |
| `created_at` / `updated_at` | datetime | 是 | 生命周期字段 |

## Widget Catalog

| 领域 | Widget Type | 经营含义 | 数据等级 |
| --- | --- | --- | --- |
| 公司 | `company_health` | Company 状态、活跃项目与阻塞事实 | 可聚合 |
| 公司 | `department_overview` | Department 状态与员工数量 | 可聚合 |
| 项目 | `project_progress` | Project / WorkflowRun 进度 | 可聚合 |
| 项目 | `project_risk` | blocked / failed 事实、缺失负责人或能力 | 派生事实，非预测 |
| 员工 | `employee_status` | 创建、启用、工作、等待、停用状态 | 可聚合 |
| 员工 | `employee_load` | 活跃 Step / Task 数量 | 可聚合 |
| 员工 | `employee_growth` | 新增实例、绑定变化、完成工作统计 | 需定义指标 |
| 成本 | `token_usage` | Token 消耗 | 可聚合 |
| 成本 | `model_usage` | 模型调用次数与 Token 分布 | 可聚合 |
| 成本 | `ai_cost` | `estimated_cost` 聚合 | 可聚合；非账单 |
| 价值 | `value_event` | 已记录价值事件 | 契约预留 |
| 价值 | `estimated_impact` | 价值事件估算值及来源 | 契约预留；非 ROI |
| 能力 | `skill_usage` | Skill 绑定/执行关联 | 部分就绪 |
| 能力 | `tool_usage` | Tool 能力调用归因 | 可聚合 |
| 知识 | `knowledge_growth` | Project Memory / Knowledge 记录数量与更新时间 | 部分就绪 |

## 自定义规则

1. CEO 可以从 Catalog 添加 Widget、删除 Widget、调整顺序、显示/隐藏 Widget 和修改允许的 scope。
2. CEO 不可以创建任意 Widget Type、写入原始查询、修改公式、添加外部数据源或更改官方模板定义。
3. Company 与 tenant 边界强制应用于每个 Widget；不得通过 scope 读取其他 tenant 或 Company 的数据。
4. Dashboard 实例不拥有业务数据，只保存布局和非敏感展示偏好。
5. 任何新 Widget、跨线数据源、实时推送、指标公式或商业字段必须先开独立 Contract / Gate。

## Admin / Workspace 边界

- Workspace 展示自身 tenant 的运行时事实、Usage Event、Value Event 记录和知识摘要。
- Admin 继续拥有 Plan、Quota、Pricing、Billing Event、Invoice 与官方供给治理。
- Dashboard 不调用 `/api/platform/*`，不计算账单、不执行收费，也不读取 tenant_private 明文凭据。
