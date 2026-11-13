# 模板实例定制策略

状态：Phase-1B Template Runtime Integration Gate

日期：2026-07-10

归属：Workspace 产品与运行时边界

## 原则

实例可以为一家 AI 公司服务而定制，但定制不能改写模板来源、绕过能力治理或引入敏感数据。

## 可定制字段

| 对象 | CEO 可定制 | 约束 |
| --- | --- | --- |
| CompanyInstance | 名称、描述、状态 | 不改变 tenant、来源追溯或商业配置 |
| DepartmentInstance | 名称、使命、经理、状态 | 仅已批准的 `software_rnd`；不创建新部门类型 |
| EmployeeInstance | 名称、受限 instructions override、启用状态、允许的 persona 预留 | 角色、Company、Department、模板来源不可直接篡改 |
| EmployeeSkillBinding | 启用、优先级、tenant 私有 Skill 绑定 | Skill 文本受敏感信息与路由指令限制 |
| EmployeeToolBinding | 启用、优先级、official / tenant_private 能力选择 | 复用 EmployeeCapabilityBinding；不得绕过 Credential Vault |
| WorkflowInstance | 显示名称、启用状态、Project 关联 | 不改变官方 SOP 步骤、顺序或执行引擎 |

## 不可定制字段

- `tenant_id`、`company_id`、`department_id` 等归属字段不得通过普通编辑动作跨范围修改。
- `created_from_template_id`、`created_from_template_version`、`template_source` 和 template snapshot 不可修改。
- 官方 Template 定义、官方能力目录、能力来源、模型网关、Credential Vault、计费和套餐不可由 Workspace 实例编辑。
- 禁止在任何名称、描述、persona、Skill 或 Workflow 配置中保存明文密钥、token、Provider SDK 配置或凭据 URI。

## 定制后的执行规则

1. 定制仅改变 tenant 私有 Instance 或 Binding，不能污染官方目录。
2. 被停用的 Employee / Binding 不可接受新的 Task 或 WorkflowStep。
3. Project 驱动 Workflow；实例定制不能把 Workflow 变成独立 CEO 入口。
4. 所有执行仍使用既有 Tool Router、Model Gateway Adapter、Credential Vault，并写入脱敏 UsageEvent / AuditEvent。

## 审计与回退

- 本 Gate 只定义来源与编辑边界，不实现版本对比、自动回退或模板同步。
- 后续如果实现实例版本迁移，必须创建新的 Instance 或显式变更记录，不能覆盖 origin 字段。
