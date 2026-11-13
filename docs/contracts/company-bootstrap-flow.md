# AI 公司创建与模板引导流程

状态：Phase-1B Template Runtime Integration Gate

日期：2026-07-10

归属：Workspace 产品流程设计

## CEO 创建公司的两种入口

```text
CEO 选择“创建 AI 公司”
  -> 空白公司
     -> CompanyInstance
     -> 默认 Engineering Department（可选）
     -> CEO 继续配置 Project / Employee / Capability

  -> CompanyPackage
     -> 校验官方 Package 与版本
     -> CompanyInstance
     -> DepartmentInstance
     -> EmployeeInstance
     -> EmployeeSkillBinding
     -> EmployeeToolBinding
     -> WorkflowInstance
     -> CEO 查看并确认公司配置
```

## 空白公司流程

1. CEO 输入公司名称与描述。
2. Workspace 创建 tenant 私有 CompanyInstance；`created_from_template_id` 和 `created_from_template_version` 为空。
3. Workspace 可创建或延迟创建默认 Engineering Department。
4. CEO 在 Company 内创建 Project，再创建或选择 Employee，并绑定 tenant_private / official 能力。
5. Workflow 仅从 Project 详情按已批准 SOP 启动。

## CompanyPackage 流程

1. CEO 从官方只读 CompanyPackage 中选择一个版本。
2. Workspace 验证 Package 中的 Department、Employee、Skill、Tool、Workflow 模板均可读取且版本一致。
3. Workspace 在一个事务性 bootstrap 操作中创建所有 tenant 私有 Runtime Instance / Binding。
4. 每个创建对象写入对应 `created_from_template_id`、`created_from_template_version` 与 `template_source`。
5. CEO 进入 Company 配置确认页，可定制允许字段；系统不得修改官方原始模板。
6. 若任一模板不可用、跨 tenant、版本不一致或能力引用不合法，bootstrap 必须失败并且不留下半完成的公司实例。

## CompanyPackage 最小内容模型

| 区域 | 最小内容 | 本阶段状态 |
| --- | --- | --- |
| Company | 名称、描述、公司类型、版本 | 契约预留 |
| Department | Software R&D 模板、默认 SOP | 契约预留 |
| Employee | 默认研发员工模板和角色顺序 | 契约预留 |
| Skill | 非敏感 SkillTemplate 与默认绑定 | 契约预留 |
| Tool | 非敏感 ToolTemplate / capability reference | 契约预留 |
| Workflow | 官方 Software R&D 顺序 SOP | 契约预留 |

CompanyPackage 不能包含 credential value、credential_ref 的可解析内容、真实连接器配置、价格、套餐或商业规则。

## UI 前置规则

- Phase-1B 可设计“空白创建 / 使用模板”选择页面，但不可自行假设官方目录、版本 API 或自动安装实现已经存在。
- 模板选择、预览、字段确认、失败提示和后续配置流程必须由 产品规划席 单独批准。
- 不做 CEO Office、会议、秘书、市场、支付、商业套餐或复杂组织图。
