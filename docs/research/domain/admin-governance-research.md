# Admin 治理 领域研究

> 范围：Curis Admin Platform 后续 Admin 治理边界研究。基于 Phase-2 MVP（New API 网关管理 + 审计轨迹 + usage_event 多维查询）和 Phase-3.5 契约评审（EmployeeTemplate / DepartmentTemplate 三态治理），研究 Admin 应该管什么、不应该管什么、`/api/platform/*` 与 `/api/catalog/*` 边界、AuditEvent 白名单策略、tenant_private 可见但不可编辑原则、capability_source 三态治理边界等。本文为纯研究文档，不写代码、不改现有文件。

---

## 现状分析

### Curis 当前 Admin 治理架构

Curis Admin Platform 在 Phase-2 / Phase-3.5 已建立以下治理边界：

**Admin 管理范围**（`/api/platform/*`，admin-only 写通道）：

| 端点 | 功能 | 数据载体 | 审计事件 |
| --- | --- | --- | --- |
| `GET/POST /api/platform/department-types` | 部门类型 CRUD | `department_types` + `department_type_status` | `governance.type_created` / `governance.type_removed` |
| `PUT/DELETE /api/platform/department-types/{type_key}` | 编辑/停用/删除 | 同上 | 同上 |
| `GET/POST /api/platform/policies` | 跨公司策略/全局护栏 | `platform_policies` | `governance.policy_set` |
| `GET/POST /api/platform/tenants` | 租户 CRUD | `tenants` | 无（metadata only） |
| `GET/PUT /api/platform/tenants/{tenant_id}` | 租户编辑 | 同上 | 无 |
| `GET /api/platform/usage` | usage_event 只读计量 | `evolution_events`（filter `usage.%`） | 无（只读） |
| `GET /api/platform/audit` | 审计轨迹只读 | `evolution_events`（filter `capability.%`/`governance.%`） | 无（只读） |
| `GET/POST /api/platform/gateways` | 网关 CRUD | `model_gateways` | `capability.gateway_created` / `capability.gateway_status_changed` |
| `PUT /api/platform/gateways/{gateway_id}` | 网关启停 | 同上 | 同上 |
| `GET/POST /api/platform/models` | 官方模型 CRUD | `official_models`（type='model'） | `capability.model_created` / `capability.model_status_changed` |
| `PUT /api/platform/models/{model_key}` | 模型启停 | 同上 | 同上 |
| `GET/POST /api/platform/capabilities` | 统一能力 CRUD（model/tool/connector） | `official_models`（type 区分） | `capability.created` / `capability.status_changed` |
| `PUT /api/platform/capabilities/{capability_key}` | 能力启停 | 同上 | 同上 |

**Workspace 只读通道**（`/api/catalog/*`，无 admin 鉴权，按 `X-Tenant-Id` 隔离）：

| 端点 | 功能 | 数据来源 |
| --- | --- | --- |
| `GET /api/catalog/department-types` | 部门类型只读 | `department_types` |
| `GET /api/catalog/models` | 官方模型只读 | `official_models`（source='official', status='active', type='model'） |
| `GET /api/catalog/capabilities` | 统一能力只读 | `official_models`（source='official', status='active'） |
| `GET /api/catalog/tools` | 工具只读 | `tool_registry` |
| `GET /api/catalog/connectors` | 连接器只读 | `official_models`（type='connector'） |
| `GET /api/catalog/gateways` | 网关只读（不含 credential_ref） | `model_gateways`（白名单列） |

**Workspace 自管通道**（`/api/workspace/*`，按 `X-Tenant-Id` 隔离）：

| 端点 | 功能 | 数据载体 |
| --- | --- | --- |
| `GET/POST /api/workspace/capabilities/private` | 租户私有能力 CRUD | `tenant_private_capabilities` |
| `GET/POST /api/workspace/private-models` | 租户私有模型 | 同上（type='model'） |
| `GET/POST /api/workspace/private-tools` | 租户私有工具 | 同上（type='tool'） |
| `GET/POST /api/workspace/private-connectors` | 租户私有连接器 | 同上（type='connector'） |
| `GET/PUT/DELETE /api/workspace/model-preference` | 租户模型偏好 | `tenant_model_preferences` |
| `GET/PUT /api/workspace/departments/activation` | 租户部门激活 | `tenant_department_activations` |
| `GET /api/workspace/employee-templates` | 员工模板只读 | `employee_templates` |
| `GET /api/workspace/department-templates` | 部门模板只读 | `department_templates` |

### 已有决策（ADR-0028 / Phase-3.5）

1. **Admin 边界铁律**（约束 6/7）：Admin 仅定义网关/模型元数据 + 只读计量；绝不 import Workspace 执行层、绝不实现模型调用/网关代理/请求转发。
2. **`/api/platform/*` vs `/api/catalog/*` 分工**：platform 为 Admin 写通道，catalog 为 Workspace 只读通道，二者非替代。
3. **AuditEvent 白名单**：`/api/platform/audit` 仅暴露 `capability.*` 与 `governance.*` 命名空间，绝不泄漏 `usage.*` 或其他未授权事件类型。
4. **usage fail-closed**：`/api/platform/usage` 须 `tenant_id` 必填，禁止跨租户聚合返回。
5. **capability_source 三态**（ADR-0028 §2）：`official` / `tenant_private` / `marketplace`，所有能力/模板统一来源标签。
6. **Phase-3.5 契约评审结论**：
   - C1：EmployeeTemplate 定义解禁，Instance 仍锁定（ADR-0017 禁止区部分解禁）。
   - C3：Admin 端 official template 管理须独立于 `CapabilityCatalog`，走 `EmployeeTemplateCatalog` / `DepartmentTemplateCatalog`。
   - C5：`CAPABILITY_TYPE` 保持 3 类型（model/tool/connector）不变，template 走独立 catalog 体系。
   - tenant_private template 隔离：`list_employee_templates` 用 `source = 'official' or (source = 'tenant_private' and tenant_id = ?)` 过滤。

### 当前痛点与未决项

1. **Admin template 管理 API 未实现**：Phase-3.5 评审建议新增 `EmployeeTemplateCatalog` / `DepartmentTemplateCatalog` 服务 + `/api/platform/employee-templates` / `/api/platform/department-templates` 端点，但尚未实现。
2. **Marketplace 审核 API 未实现**：Phase-3.5 评审建议新增 `/api/platform/marketplace-review` 端点 + 审核队列表，须 G3 gate 解锁。
3. **tenant_private 投影字段白名单未显式定义**：Phase-3.5 §5.2 建议 Admin 查看 tenant_private template 时仅返回 `(id, name, source, tenant_id, enabled, created_at)`，不含业务配置字段，但未落地。
4. **Admin 是否应管理 employee_instances 仍锁定**：ADR-0017 禁止区核心，Instance 创建/激活/执行须 governance gate 解锁。
5. **AuditEvent 白名单是否扩展 `template.*` 命名空间**：Phase-3.5 §3.2 建议 template 审计事件用 `template.created` / `template.status_changed`，与 `capability.*` 区分，但未纳入白名单。

---

## 研究发现

### 行业最佳实践：Admin 平台治理边界

基于 Dify / Coze / LangChain / Portkey 等平台的 Admin 治理设计，主流边界原则：

#### 1. Admin 应该管什么（元数据 + 治理 + 只读观测）

| 管理对象 | 示例 | Curis 对应 |
| --- | --- | --- |
| 官方能力元数据 | 模型/工具/连接器目录 | `official_models`（Admin CRUD） |
| 网关配置 | 网关地址/类型/状态 | `model_gateways`（Admin CRUD） |
| 部门类型注册表 | 组织架构模板 | `department_types`（Admin CRUD） |
| 租户注册表 | 租户身份/plan_tier | `tenants`（Admin CRUD） |
| 跨公司策略/护栏 | 全局策略 | `platform_policies`（Admin CRUD） |
| 审计轨迹 | 只读日志 | `evolution_events`（Admin 只读） |
| 用量计量 | 只读统计 | `evolution_events`（Admin 只读，按 tenant_id） |
| Marketplace 审核 | 跨租户能力审核 | 待实现（G3 gate） |

#### 2. Admin 不应该管什么（执行 + 私有配置 + 真实凭证）

| 禁止对象 | 原因 | Curis 落地 |
| --- | --- | --- |
| Workspace 任务执行 | 执行属 Workspace 职责 | Admin 无 `/api/task/*` 写端点 |
| tenant_private 配置 | 租户私有，Admin 不可见配置内容 | Admin 无 tenant_private CRUD 端点 |
| 员工实例（employee_instances） | ADR-0017 禁止区核心 | Admin 无 instance 端点 |
| 真实凭证 | 安全铁律 | DB 零密钥列，Admin 不解析 credential_ref |
| 模型调用/网关代理 | 执行属 Workspace | Admin 不 import `model_gateway` |
| 租户业务配置 | 租户私有 | Admin 不见 `default_instructions` / `default_model_policy_json` |

#### 3. 分层治理原则

主流平台采用"元数据/实例/运行时"三层分离：

| 层 | 管理方 | Curis 对应 |
| --- | --- | --- |
| 元数据层（Template/Catalog） | Admin（official）+ CEO（tenant_private） | `official_models` / `employee_templates` / `department_templates` |
| 实例层（Instance） | CEO（Workspace） | `employee_instances` / `departments` |
| 运行时层（Execution） | Workspace | `AIEmployee` / `Orchestrator` / `ModelGatewayAdapter` |

Curis 当前已遵循此分层：Admin 管元数据，CEO 管实例（部分锁定），Workspace 管运行时。

### `/api/platform/*` 与 `/api/catalog/*` 边界分析

#### 职责分工

| 维度 | `/api/platform/*` | `/api/catalog/*` |
| --- | --- | --- |
| 鉴权 | `_require_platform_admin`（Bearer token） | 无 admin 鉴权，按 `X-Tenant-Id` |
| 操作 | 读 + 写（CRUD） | 仅读 |
| 调用方 | Admin 后台 UI | Workspace 服务 |
| 数据范围 | 全量（含 inactive） | 仅 `source='official' AND status='active'` |
| 凭证可见性 | 含 `credential_ref` 占位串 | **显式排除** `credential_ref` / `default_model` |
| 审计 | 写操作触发 `capability.*` / `governance.*` | 无写，无审计 |
| 用途 | 管理后台配置 | Workspace 能力发现 |

#### 边界铁律

1. **catalog 读 ≠ platform 写**：`/api/catalog/*` 仅只读投影，绝不接受写操作；`/api/platform/*` 仅 Admin 写，绝不向 Workspace 开放。
2. **catalog 投影白名单**：`/api/catalog/gateways` 显式排除 `credential_ref`；`/api/catalog/capabilities` 白名单列（`capability_key/type/name/provider_id/display_name/source/gateway_ref/auth_type/status/created_at/updated_at`）。
3. **platform 写须审计**：所有 `/api/platform/*` 写操作须写 `capability.*` / `governance.*` 审计事件（append-only）。
4. **catalog 不可回调 platform**：Workspace 经 catalog 读到能力元数据后，不可反向触发 Admin 写操作。

#### 当前实现的边界一致性

已验证：
- `/api/catalog/gateways` → `list_catalog_gateways()` 显式 SELECT 非密钥列。✅
- `/api/catalog/capabilities` → `list_catalog_capabilities()` 白名单列 + `source='official' AND status='active'`。✅
- `/api/catalog/models` → `list_official_models()` 过滤 `type='model'`。✅
- `/api/platform/*` 全部复用 `_require_platform_admin`。✅
- platform 写操作全部写审计事件。✅

### AuditEvent 白名单策略

#### 当前白名单

`/api/platform/audit`（`database.list_audit_events`）仅暴露：

```sql
where (event_type like 'capability.%' or event_type like 'governance.%')
```

#### 命名空间规划

| 命名空间 | 用途 | 示例事件 | Admin 可见 |
| --- | --- | --- | --- |
| `capability.*` | 能力/网关/模型元数据变更 | `capability.gateway_created` / `capability.model_status_changed` / `capability.created` | ✅ |
| `governance.*` | 治理/策略变更 | `governance.type_created` / `governance.policy_set` | ✅ |
| `usage.*` | 用量计量 | `usage.model_invoked` | ❌（经 `/api/platform/usage` 单独查询） |
| `template.*` | 模板变更（建议） | `template.created` / `template.status_changed` | ✅（建议纳入） |
| `marketplace.*` | 市场审核（建议） | `marketplace.submitted` / `marketplace.approved` | ✅（建议纳入，G3 gate） |

#### 白名单扩展建议

1. **`template.*` 纳入白名单**：Phase-3.5 建议模板审计事件用 `template.created` / `template.status_changed`，须扩展 `list_audit_events` 的 WHERE 子句为：
   ```sql
   where (event_type like 'capability.%' or event_type like 'governance.%' or event_type like 'template.%')
   ```

2. **`marketplace.*` 纳入白名单**（G3 gate 解锁后）：市场审核事件须独立命名空间，与 `capability.*` 区分（审核流程有状态机，非单纯元数据变更）。

3. **`usage.*` 绝不纳入 audit**：usage 事件经 `/api/platform/usage` 单独查询（7 维过滤），与审计轨迹分离，避免 audit 接口被 usage 事件淹没。

#### 审计事件不变式

- **append-only**：`EvolutionEventLog.record` 是唯一写方法（INSERT），无 update/delete。
- **idempotency_key**：支持幂等写入（重复请求不产生重复事件）。
- **tenant_id 标记**：每个事件带 tenant_id（official 事件 tenant_id='platform'/'default'）。
- **payload JSON**：payload 保持 JSON 字符串，调用方按需解析。

### tenant_private 可见但不可编辑原则

#### 核心原则

Admin 对 tenant_private 的可见性遵循"用量可见，配置不可见"：

| 维度 | Admin 可见 | Admin 不可见 |
| --- | --- | --- |
| usage_event | ✅（按 tenant_id 过滤，含 capability_source='tenant_private'） | — |
| 存在性 | ✅（可统计租户有多少 private capability） | — |
| 配置内容 | — | ❌（`default_instructions` / `default_model_policy_json` / `metadata_json` 业务配置） |
| credential_ref | — | ❌（即使占位串也不可见，防止泄露密钥托管位置） |
| 执行日志 | — | ❌（Workspace 任务执行属租户私有） |

#### 落地方式

1. **usage 投影按 tenant_id 过滤**：`/api/platform/usage?tenant_id=X` 返回该租户所有 usage 事件（含 tenant_private 来源），但 payload 中不含 tenant_private 配置内容，仅含计量数据（tokens/cost/status）。

2. **tenant_private 投影字段白名单**（Phase-3.5 §5.2 建议，待落地）：
   Admin 查看 tenant_private template/capability 时，投影仅返回：
   ```
   (id/capability_id, name, source, tenant_id, enabled/status, created_at)
   ```
   不返回：`default_instructions` / `default_model_policy_json` / `metadata_json` / `credential_ref`。

3. **Admin 无 tenant_private CRUD 端点**：Admin 不可创建/编辑/删除 tenant_private capability/template，仅 CEO 经 `/api/workspace/*` 管理。

#### 边界一致性

| capability_source | Admin 管理方 | Admin 可见字段 | Workspace 可见字段 |
| --- | --- | --- | --- |
| `official` | Admin CRUD | 全量（含 credential_ref 占位串） | catalog 投影（不含 credential_ref） |
| `tenant_private` | CEO CRUD | 仅 usage_event + 存在性 | 租户内全量（含 metadata_json） |
| `marketplace` | Admin 审核 | 全量（审核通过后） | catalog 投影（审核通过后） |

### capability_source 三态治理边界

#### 三态定义（ADR-0028 §2）

| source | 管理方 | tenant_id | 载体表 | Workspace 可见性 | Admin 可见性 |
| --- | --- | --- | --- | --- | --- |
| `official` | Admin | 'platform' | `official_models` / `employee_templates` / `department_templates` | `/api/catalog/*` 全局只读 | 全量 CRUD |
| `tenant_private` | CEO | 实际租户 ID | `tenant_private_capabilities` / `employee_templates`(source=tenant_private) / `department_templates`(source=tenant_private) | `/api/workspace/*` 租户内 | 仅 usage_event |
| `marketplace` | Admin 审核 | 'platform'（审核通过后） | 同 official 载体 | `/api/catalog/*` 全局只读（审核通过后） | 全量 CRUD + 审核队列 |

#### 三态治理一致性矩阵（Phase-3.5 §7.1 已验证）

| 维度 | model/tool/connector | employee_template | department_template | 一致性 |
| --- | --- | --- | --- | --- |
| source 枚举 | official/tenant_private/marketplace | 同 | 同 | ✅ |
| official 管理方 | Admin | Admin（待实现） | Admin（待实现） | ✅ |
| tenant_private 管理方 | CEO | CEO | CEO | ✅ |
| marketplace 审核 | Admin（G3 gate） | Admin（G3 gate） | Admin（G3 gate） | ✅ |
| tenant_private 隔离 | `tenant_private_capabilities` + tenant_id | `employee_templates` + tenant_id | `department_templates` + tenant_id | ✅ |
| official 全局可见 | `/api/catalog/*` | 待实现 `/api/catalog/employee-templates` | 待实现 `/api/catalog/department-templates` | ✅ |
| usage_event 投影 | `capability_source` 标记 | `capability_source` 标记（经 bindings） | `capability_source` 标记（经 bindings） | ✅ |
| 审计事件 | `capability.created` | `template.created`（建议） | `template.created`（建议） | ✅ |
| 凭证 | ❌ 不持久化 | ❌ 不涉及 | ❌ 不涉及 | ✅ |

#### 边界规则

1. **official 全局共享**：`source='official'` 的能力/模板对所有租户可见（经 `/api/catalog/*`），tenant_id='platform'。
2. **tenant_private 租户隔离**：`source='tenant_private'` 的能力/模板仅本租户可见（`tenant_id = ?` 过滤），不进入 `/api/catalog/*`。
3. **marketplace 审核准入**：`source='tenant_private'` → 提交申请 → Admin 审核 → `source='marketplace'` + `tenant_id='platform'`（全局可见）。须 G3 gate。
4. **三态不可混用**：同一能力/模板的 `source` 不可跨态修改（official 不可降级为 tenant_private，tenant_private 须经审核流程升为 marketplace）。

---

## 设计建议

### 数据模型建议

#### 1. Admin template 管理（Phase-3.5 C3 条件，待实现）

建议新增独立 template catalog 服务，不扩展 `CAPABILITY_TYPE`：

```
CapabilityCatalog（现有）          → official_models 表 → model/tool/connector
EmployeeTemplateCatalog（新增）     → employee_templates 表 → employee_template
DepartmentTemplateCatalog（新增）   → department_templates 表 → department_template
```

三个服务遵循相同设计模式：
- `create()` → 校验 + 落库 + `template.created` 审计事件
- `set_status()` → 启停 + `template.status_changed` 审计事件
- `get()` / `list()` → 只读投影
- `_reject_secret_like_metadata()` → 复用密钥拒绝逻辑

#### 2. tenant_private 投影白名单（Phase-3.5 §5.2，待落地）

Admin 查看 tenant_private template/capability 时，建议投影方法：

```python
def list_tenant_private_summary(self, tenant_id: str) -> list[dict]:
    """Admin 投影 tenant_private 概要（不含业务配置）。"""
    # 仅返回 (id, name, source, tenant_id, enabled, created_at)
    # 不返回 default_instructions / default_model_policy_json / metadata_json / credential_ref
```

#### 3. Marketplace 审核队列表（G3 gate，待实现）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `review_id` | text PK | |
| `template_type` | enum | `employee_template` / `department_template` / `capability` |
| `source_id` | text | → employee_templates / department_templates / official_models |
| `source_tenant_id` | text | 提交方租户 |
| `status` | enum | `pending_review` / `approved` / `rejected` / `published` |
| `reviewer_id` | text | Admin 审核人 |
| `reviewed_at` | datetime | |
| `review_notes` | text | |
| `published_id` | text | 批准后生成的 marketplace ID |

#### 4. AuditEvent 白名单扩展

`list_audit_events` WHERE 子句扩展（additive）：

```sql
-- 当前
where (event_type like 'capability.%' or event_type like 'governance.%')
-- 扩展后
where (event_type like 'capability.%' or event_type like 'governance.%'
       or event_type like 'template.%' or event_type like 'marketplace.%')
```

### API 设计建议

#### 1. Admin template 管理 API（Phase-3.5 C3，待实现）

```
POST   /api/platform/employee-templates          # 创建 official employee template
GET    /api/platform/employee-templates          # 列表（含 inactive）
PATCH  /api/platform/employee-templates/:id      # 编辑
POST   /api/platform/employee-templates/:id/status  # 启停

POST   /api/platform/department-templates         # 创建 official department template
GET    /api/platform/department-templates         # 列表（含 inactive）
PATCH  /api/platform/department-templates/:id     # 编辑
POST   /api/platform/department-templates/:id/status  # 启停
```

Workspace 只读通道：
```
GET    /api/catalog/employee-templates            # 只读 official employee templates
GET    /api/catalog/department-templates           # 只读 official department templates
```

#### 2. Marketplace 审核 API（G3 gate，待实现）

```
GET    /api/platform/marketplace-review           # 待审核列表
POST   /api/platform/marketplace-review/:review_id/approve  # 批准
POST   /api/platform/marketplace-review/:review_id/reject   # 驳回
```

#### 3. tenant_private 概要投影 API（建议新增）

```
GET    /api/platform/tenants/:tenant_id/private-summary    # 租户私有能力/模板概要（不含配置）
```

返回：`(id, name, source, tenant_id, enabled, created_at)` 列表，按 capability_type/template_type 分组。

### 边界规则

#### 1. Admin 管理边界（铁律）

| 应该管 | 不应该管 |
| --- | --- |
| official 能力元数据（model/tool/connector） | Workspace 任务执行 |
| official 网关配置 | tenant_private 配置内容 |
| official 模板元数据（employee/department） | employee_instances 创建/激活 |
| 租户注册表（身份/plan_tier） | 真实凭证 |
| 跨公司策略/护栏 | 模型调用/网关代理 |
| 审计轨迹（只读） | 租户业务配置 |
| 用量计量（只读，按 tenant_id） | |
| Marketplace 审核（G3 gate 后） | |

#### 2. `/api/platform/*` vs `/api/catalog/*` 边界

| 规则 | platform | catalog |
| --- | --- | --- |
| 鉴权 | `_require_platform_admin` | `X-Tenant-Id` |
| 操作 | 读 + 写 | 仅读 |
| 数据范围 | 全量（含 inactive） | 仅 official + active |
| credential_ref | 含占位串 | 显式排除 |
| 审计 | 写操作触发 | 无写 |

#### 3. AuditEvent 白名单规则

- 仅 `capability.*` / `governance.*`（当前）+ `template.*` / `marketplace.*`（建议扩展）。
- `usage.*` 经 `/api/platform/usage` 单独查询，绝不纳入 audit。
- append-only，无 update/delete。
- payload 不含密钥值。

#### 4. tenant_private 可见性规则

- usage_event 可见（按 tenant_id 过滤）。
- 存在性可见（可统计数量）。
- 配置内容不可见（`default_instructions` / `metadata_json` / `credential_ref`）。
- Admin 无 tenant_private CRUD 端点。

#### 5. capability_source 三态规则

- official：Admin CRUD，全局共享，`/api/catalog/*` 只读。
- tenant_private：CEO CRUD，租户隔离，不进 catalog。
- marketplace：Admin 审核，审核通过后全局共享。
- 三态不可跨态修改，须走审核流程。

---

## 前置条件

### G3 gate（Marketplace 跨租户共享）

- **解锁条件**：总控决策席 + 安全边界席双签。
- **须确认**：跨租户能力共享的安全模型；审核流程状态机；跨租户 usage 归属与收益分成；marketplace 审核队列表设计。
- **解锁后**：新增 `/api/platform/marketplace-review` 端点 + 审核队列表 + `marketplace.*` 审计命名空间。

### C1 gate（EmployeeTemplate 解禁）

- **解锁条件**：独立 ADR（ADR-00xx Employee Template 解禁），总控决策席 + 安全边界席 gate。
- **须确认**：解禁范围仅限模板元数据 CRUD；`employee_instances` 创建/激活仍锁定；`AIEmployee` 执行仍锁定。
- **解锁后**：Admin 可管理 official employee template，CEO 可配置 tenant_private template。

### C3 gate（Admin template catalog 服务）

- **解锁条件**：`EmployeeTemplateCatalog` / `DepartmentTemplateCatalog` 服务设计文档。
- **须确认**：独立于 `CapabilityCatalog`；`template.*` 审计命名空间；`/api/platform/employee-templates` / `/api/platform/department-templates` 端点设计。
- **解锁后**：实现 Admin template CRUD + catalog 只读投影。

### tenant_private 投影白名单 gate

- **解锁条件**：Admin 投影字段白名单文档化（Phase-3.5 §5.2 建议）。
- **须确认**：哪些字段可见（建议仅 `id/name/source/tenant_id/enabled/created_at`）；哪些字段不可见（`default_instructions`/`metadata_json`/`credential_ref`）。
- **解锁后**：新增 `/api/platform/tenants/:tenant_id/private-summary` 端点。

---

## 结论

1. **Admin 管理边界已清晰**：管元数据（official 能力/网关/模板）+ 治理（租户/策略）+ 只读观测（usage/audit）；不管执行（任务/调用）+ 私有配置（tenant_private）+ 真实凭证。此边界与行业最佳实践一致。

2. **`/api/platform/*` 与 `/api/catalog/*` 边界须持续守护**：platform 为 Admin 写通道（含 credential_ref 占位串），catalog 为 Workspace 只读通道（显式排除敏感字段）。catalog 投影白名单须用显式列名 SELECT + 测试断言双重保障。

3. **AuditEvent 白名单策略建议扩展**：当前 `capability.*` / `governance.*` 须扩展 `template.*`（Phase-3.5 后）和 `marketplace.*`（G3 gate 后）。`usage.*` 绝不纳入 audit，经 `/api/platform/usage` 单独查询。

4. **tenant_private 可见但不可编辑原则须落地**：Admin 可见 usage_event（按 tenant_id）+ 存在性，不可见配置内容（`default_instructions`/`metadata_json`/`credential_ref`）。建议新增 `/api/platform/tenants/:tenant_id/private-summary` 端点，投影字段白名单。

5. **capability_source 三态治理边界已一致**：model/tool/connector 与 employee_template/department_template 的三态治理（official/tenant_private/marketplace）在 source 枚举、管理方、隔离方式、审计模式上完全对齐。差异仅在实现载体（独立表 vs 共享表）。

6. **Admin template 管理须独立 catalog 服务**：Phase-3.5 C3 条件建议 `EmployeeTemplateCatalog` / `DepartmentTemplateCatalog` 独立于 `CapabilityCatalog`，不扩展 `CAPABILITY_TYPE`。此决策正确，须 C3 gate 解锁后实现。

7. **Marketplace 审核须 G3 gate**：跨租户能力共享触发 G3 gate，须总控决策席 + 安全边界席双签。审核流程须独立队列表 + `marketplace.*` 审计命名空间 + 状态机（submit → review → approve/reject → publish）。

8. **Admin 绝不出站、绝不解析凭证铁律须扩展至 template 领域**：Admin template CRUD 同样不 import `model_gateway`、不发起 HTTP 调用、不解析 credential_ref、不持久化密钥值。禁止区扫描须覆盖新增的 template catalog 服务文件。
