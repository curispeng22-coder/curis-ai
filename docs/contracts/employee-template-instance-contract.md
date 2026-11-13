# 员工模板与员工实例契约

状态：Phase-1B Template Runtime Integration Gate

日期：2026-07-10

归属：Workspace

## 对象边界

`EmployeeTemplate` 定义可复用的岗位默认值；`EmployeeInstance` 是某个 tenant、Company、Department 中可被分配工作的具体 AI 员工。

```text
EmployeeTemplate（只读默认值）
  -> EmployeeInstance（tenant 私有运行时对象）
    -> EmployeeSkillBinding
    -> EmployeeToolBinding / EmployeeCapabilityBinding
```

## EmployeeInstance 最小契约

| 字段 | 类型 | 实例化规则 | 可由 CEO 定制 |
| --- | --- | --- | --- |
| `id` | string | 生成 | 否 |
| `tenant_id` | string | 当前 tenant | 否 |
| `company_id` | string | 来自所选 Department | 否；迁移需独立流程 |
| `department_id` | string | CEO 所选 Department | 否；迁移需独立流程 |
| `template_id` | string | 所选模板 ID | 否 |
| `created_from_template_id` | string nullable | 复制模板稳定 ID | 否 |
| `created_from_template_version` | string nullable | 复制模板版本 | 否 |
| `name` | string | 模板默认名称 | 是 |
| `role` | string | 模板默认岗位 | 否；避免实例脱离岗位语义 |
| `instructions_override` | text | 空 | 是，但仅按已批准的受限提示规则生效 |
| `persona` | object nullable | 空 | 仅预留；不得存放密钥、路由、Provider、价格或绕过指令 |
| `status` | lifecycle enum | 启用前为创建，随后按员工生命周期 | 仅启用/停用动作可改变 |
| `enabled` | boolean | true | 是 |

## 能力绑定规则

1. CEO 可以为 EmployeeInstance 添加、移除或排序 Skill / Tool / Model / Connector 能力绑定。
2. 所有实际权限由 `EmployeeCapabilityBinding` 决定；ToolBinding 是其中 `capability_type=tool` 的投影，不能形成第二套权限面。
3. 绑定可引用 `official` 或本 tenant 的 `tenant_private` 能力。marketplace 仅预留，不可执行。
4. Skill 只提供受限、非权威的工作提示；不得选择工具、模型、凭据或执行路径。
5. 凭据只通过 Capability 对应的 Credential Vault resolver 使用；绑定与实例 API 不返回或保存明文密钥。

## 模板升级规则

- 模板升级不会自动改变 EmployeeInstance。
- CEO 可在未来“比较模板版本”流程中选择创建新实例、手动同步允许字段或保持当前实例；该流程不属于本 Gate。
- origin_template 必须始终保留，使后续升级、审计和迁移可追溯。
