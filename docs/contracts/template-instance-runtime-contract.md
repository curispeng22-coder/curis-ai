# 模板到运行时实例契约

状态：Phase-1B Template Runtime Integration Gate

日期：2026-07-10

归属：Workspace；官方模板供给由 Admin 侧后续契约提供。

## 目标

定义只读 Template 如何在 Workspace 内转换为 tenant 私有的 Runtime Instance。该契约只冻结数据与运行规则，不实现 UI、Admin 接口、Credential Vault 或 Workflow Engine 改动。

## 总原则

```text
Admin 官方 Template（只读）
  -> Workspace 读取并选择
    -> Workspace 创建 tenant_private Instance / Binding
      -> CEO 在允许范围内定制实例
        -> 保留不可变 origin_template
```

## 通用来源追踪字段

每个由模板实例化的对象必须保留下列字段：

| 字段 | 类型 | 必填 | 写入时机 | 规则 |
| --- | --- | --- | --- | --- |
| `created_from_template_id` | string nullable | 是，空白创建除外 | 实例创建 | 原始模板稳定 ID；创建后不可修改 |
| `created_from_template_version` | string nullable | 是，空白创建除外 | 实例创建 | 模板发布版本，例如 `1.2.0`；创建后不可修改 |
| `template_source` | enum | 是，空白创建为 `tenant_private` | 实例创建 | `official` / `tenant_private` / `marketplace`；本阶段 marketplace 仅保留语义 |
| `template_snapshot` | object nullable | 否 | 后续实例化实现 | 仅保存非敏感模板展示/默认配置快照；不保存 credential、config_ref 或明文密钥 |

`created_from_template_id` 和 `created_from_template_version` 是来源追溯字段，不是动态继承关系。模板后续升级不会静默覆盖已创建实例。

## Template -> Instance 映射

| Template | Workspace Runtime 产物 | 当前状态 | 实例化后的所有权 |
| --- | --- | --- | --- |
| CompanyTemplate | CompanyInstance / CompanyRuntime | CompanyRuntime 已有；Template 预留 | 当前 tenant 的 Workspace |
| DepartmentTemplate | DepartmentInstance | 已有基础 | 当前 tenant 的 Workspace |
| EmployeeTemplate | EmployeeInstance | 已有基础 | 当前 tenant 的 Workspace |
| WorkflowTemplate | WorkflowInstance | 已有基础 | 当前 tenant 的 Workspace |
| SkillTemplate | EmployeeSkillBinding | 已有基础 | 当前 tenant 的 Workspace |
| ToolTemplate | EmployeeToolBinding | 已有基础 | 当前 tenant 的 Workspace |

## 来源与边界

| 来源 | Workspace 权限 | Admin 权限 | 本阶段规则 |
| --- | --- | --- | --- |
| `official` | 读取、选择、实例化；不得修改定义 | 未来提供与版本治理 | 可作为实例来源 |
| `tenant_private` | 创建、修改、启用/停用本租户实例或模板 | 不读取私有明文，不接管实例 | 可作为本租户来源 |
| `marketplace` | 仅保留来源语义 | 未来审核与供给治理 | 不启用安装、交易或分成 |

Workspace 不调用 `/api/platform/*` 写接口。任何跨线模板目录读取、版本协商或安装接口都必须先经过 Shared Contract / Gate。

## 实例化不变量

1. 官方 Template 永远只读；Workspace 不能修改其定义。
2. 所有 Instance 和 Binding 必须 tenant 隔离，且属于一个 Company / Department 上下文（Skill / Tool Binding 通过 Employee 间接归属）。
3. 空白创建的 Company、Department、Employee 或 Project 可没有模板来源，但必须明确 `template_source=tenant_private`。
4. 模板实例化不得复制、返回、记录或解析明文凭据；能力执行继续经过 Tool Router、Model Gateway 与 Credential Vault。
5. Instance 的可定制字段与 origin 字段必须分离。删除或停用模板不自动删除既有实例。

## Phase-1B 准备结论

现有 Foundation 已支持多个对象的 `created_from_template_id`。`created_from_template_version`、非敏感快照和跨线官方目录读取仍是后续独立实现切片，不能由 UI 自行补写。
