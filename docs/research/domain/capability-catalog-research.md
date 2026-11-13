# 能力目录（Capability Catalog）领域研究

> 研究范围：Curis Admin Platform 的 Official Capability Catalog 应包含哪些类型、`capability_type` 枚举演进方向、official / tenant_private / marketplace 三态目录边界、Admin 写 vs Workspace 读规则、是否预留 template 与 pack 类型。
>
> 研究性质：纯研究文档，不含实现方案、不含代码改动。所有结论须与 ADR-0028 共享契约与 issue 087 Phase-3.5 决策对齐。

---

## 现状分析

### 1. Curis 当前能力目录架构

Curis Admin Platform 已完成 Phase-2 MVP 与 Phase-3 治理边界验证，Phase-3.5 契约评审（issue 087）已决定 `CAPABILITY_TYPE` 保持 3 类型不变，template 走独立 catalog 体系。当前架构关键事实如下：

#### 1.1 `CAPABILITY_TYPE` 常量定义

`backend/app/catalog_constants.py:32` 定义：

```python
CAPABILITY_TYPE: List[str] = ["model", "tool", "connector"]
```

- 仅承载「可执行能力」（executable capability）三类
- template 不在其中（issue 087 §6.2 决策）
- 常量被 `capability_catalog.py:85` 用于 `is_valid_capability_type()` 校验

#### 1.2 `official_models` 表结构

`backend/app/database.py:366-377` 定义 `official_models` 表，作为 Admin 官方能力目录的唯一载体表：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `model_key` | text PK | 全局唯一 capability key（共享于 model/tool/connector） |
| `provider_id` | text | 供应方 ID |
| `display_name` | text | 展示名 |
| `supported_models` | text(JSON) | 支持的模型名清单 |
| `auth_type` | text | none/oauth/apikey（仅形状） |
| `source` | text | 默认 `official` |
| `gateway_ref` | text | 默认 `newapi`（仅 model 类型校验存在性） |
| `status` | text | active/inactive |
| `default_model` | text | additive 扩展 |
| `type` | text | additive 扩展，默认 `model` |
| `name` | text | additive 扩展，默认空 |

字段集是为 model/tool/connector 设计的，无法自然承载 template 专属字段（如 `role`、`default_instructions`、`department_type`）。

#### 1.3 `tenant_private_capabilities` 表结构

`backend/app/database.py:425-437` 定义租户私有能力表，`capability_type` CHECK 约束为 `('model', 'tool', 'connector')`，**不含** template 类型。此为 issue 087 §5.3 (C4 条件) 明确确认的设计意图。

#### 1.4 Template 独立表已落地

Phase-3.5 已新增 4 张表（`database.py:442-496`）：

- `employee_templates`：含 `role`、`default_instructions`、`default_capability_types_json`、`default_model_policy_json` 等专属字段，`source` CHECK 三态
- `department_templates`：含 `department_type`、`default_employee_templates_json` 等专属字段，`source` CHECK 三态
- `employee_instances`：实例层（仍锁定，ADR-0017 禁止区）
- `employee_capability_bindings`：实例级能力绑定（`capability_source` 三态、`capability_type` 仅 3 类型）

#### 1.5 `CapabilityCatalog` 服务

`backend/app/capability_catalog.py:40-177` 实现 `CapabilityCatalog` 服务，提供：

- `create()`：校验 `capability_type`、`auth_type`、`gateway_ref` 存在性（仅 model 类型）+ 落库 + `capability.created` 审计事件
- `set_status()`：启停 + `capability.status_changed` 审计事件
- `get()` / `list()`：只读投影

服务设计明确：
- 仅 model 类型校验 `gateway_ref`，tool/connector 不校验
- 复用 `model_catalog._reject_secret_like_metadata()` 拒绝密钥
- 审计事件命名空间为 `capability.*`（区别于 `ModelCatalog` 的 `capability.model_*`）

#### 1.6 已有决策锚点

issue 087 §6.2 (C5 条件) 与 §11 总结明确：
- `CAPABILITY_TYPE` 保持 `["model","tool","connector"]` 不变
- template 走独立 catalog 体系（`EmployeeTemplateCatalog` / `DepartmentTemplateCatalog`，尚未实现）
- `capability_source` 三态枚举（official/tenant_private/marketplace）是所有能力/模板的统一来源标签，与 `capability_type` 正交

issue 062 (ADR-0028 §2) 定义 `capability_source` 三态：
- `official`：Admin 管理，全局可见
- `tenant_private`：Workspace 管理，仅本租户可见
- `marketplace`：Admin 审核，订阅租户可见（待 G3 gate）

### 2. Admin 写 vs Workspace 读现状

issue 063 (Phase-2 PRD) R-02 与 issue 062 §8.1 明确接口分工：

| 通道 | 路径前缀 | 鉴权 | 操作方 | 用途 |
| --- | --- | --- | --- | --- |
| Admin 写 | `/api/platform/*` | admin token | Admin Platform | 写 official 定义、管理租户、读审计 |
| Workspace 读 | `/api/catalog/*` | X-Tenant-Id | Workspace（CEO） | 只读 official 能力目录 |
| 租户私有写 | Workspace 内部 | X-Tenant-Id + CEO | Workspace（CEO） | 写 tenant_private 能力/模板 |
| 平台用量投影 | `/api/platform/usage` | admin token | Admin | 只读租户 UsageEvent |

**非替代分工**（issue 062 §8.1 条件 #3）：catalog 读通道不替代 platform 写通道，任何一端不得混用对方接口语义。

### 3. Template 与 Capability 关系现状

issue 087 §3.2 明确：
- Template **引用** capability（经 `default_capability_types_json` / `employee_capability_bindings`）
- Template 不是 capability 本身（语义不同：capability 是可执行资源，template 是定义配置）
- 两者通过 `capability_source` 共享三态治理语义，但 `capability_type` 分类正交

### 4. 待研究问题

- Official Capability Catalog 是否应扩展类型（如 `pack`、`workflow_template`、`company_template`）
- `capability_type` 枚举的演进路径（保持 3 类型 vs 分阶段扩展）
- official / tenant_private / marketplace 三态在不同类型上的边界一致性
- Pack（能力包）是否应成为新类型，以及归 Admin 还是 Workspace 管
- `company_template` / `department_template` / `employee_template` / `workflow_template` / `capability_pack` 的预留策略

---

## 研究发现

### 1. 行业能力目录模式

#### 1.1 AWS Service Catalog 模式

AWS Service Catalog 采用「Portfolio + Product」双层结构：
- **Portfolio**：能力的逻辑分组（如「数据团队能力包」），可分享给特定账户
- **Product**：具体能力条目（CloudFormation 模板），版本化管理
- **Constraint**：按 Portfolio 级别注入 launch constraint（IAM 角色、通知）

参考价值：Portfolio 概念对应 Curis 未来 `capability_pack`（能力组合），Product 对应 `capability` 单条目。Curis 的 `capability_pack` 若引入，应作为 Portfolio 层（包含多个 capability 引用），而非扩展 `CAPABILITY_TYPE`。

#### 1.2 Hugging Face Hub 模式

Hugging Face Hub 的 model repository 采用：
- **单表多类型**：models、datasets、spaces 共用 Hub 抽象，但各类型独立 listing 与字段
- **版本化**：Git-based，每个 revision 是一个 commit hash
- **Tags**：用 `model-index` metadata 标记任务类型（text-classification 等）
- **Lifecycle**：`gated`、`disabled`、`deprecated` 状态标志

参考价值：Hugging Face 证明了「独立 catalog + 共享 source/lifecycle 语义」的可行性，与 issue 087 决策（template 独立 catalog，共享 `capability_source` 三态）方向一致。HF 的 `deprecated` 状态值得 Curis 在 marketplace 阶段引入。

#### 1.3 OpenAI GPT Store 模式

GPT Store 中的 Custom GPT 字段：
- `name`、`description`、`instructions`、`conversation_starters`
- `actions`（API 工具绑定）、`knowledge`（文件）、`capabilities`（Code Interpreter / DALL-E / Web Browsing）
- `version`（Builder 控制版本）
- `visibility`：private / anyone with link / public

参考价值：GPT 的 `actions` + `capabilities` 模式与 Curis `employee_templates.default_capability_types_json` + `employee_capability_bindings` 模式类似。GPT Store 的 `private / link / public` 三档可见性比 Curis 三态更细，但 Curis 三态（official/tenant_private/marketplace）已足够覆盖 Phase-4 需求。

#### 1.4 Microsoft Azure Marketplace / Microsoft AppSource 模式

Azure Marketplace 商品类型：
- Virtual Machines、Containers、SaaS Apps、AI Apps、Agents
- 每类有独立的 listing 字段、审核要求、定价模型
- 统一的发布流程：Create → Publish → Review → Live → Deprecate

参考价值：Azure Marketplace 证明了「多商品类型 + 统一审核状态机」的可行性。Curis 未来 marketplace 若引入 `pack` 类型，应参照 Azure 的多类型 listing 模式。

### 2. 能力类型分类的两种范式

#### 2.1 单一巨型 catalog（Cap Gemini Capability Matrix）

部分企业内部平台采用单一 catalog 承载所有能力（model、tool、agent、template、workflow），通过 `type` 字段区分。优点是统一治理；缺点是字段冗余、类型膨胀时表结构脆弱。

#### 2.2 分治 catalog（Curis 当前方向）

Curis 选择了分治模式：
- `CapabilityCatalog`（model/tool/connector）
- `EmployeeTemplateCatalog`（待建）
- `DepartmentTemplateCatalog`（待建）
- 各 catalog 共享 `capability_source` 三态治理语义

优点是关注点分离、字段强类型、additive 扩展不破坏既有契约。缺点是跨 catalog 查询、统一 listing 需要在 API 层聚合。

### 3. Pack（能力包）的两种实现模式

#### 3.1 Pack 作为新 capability_type

将 `capability_pack` 加入 `CAPABILITY_TYPE`，承载于 `official_models` 表，`metadata_json` 存放 capability 引用列表。问题：`official_models` 字段集（`provider_id`、`auth_type`、`gateway_ref`、`supported_models`）对 pack 无意义，需大量特判。

#### 3.2 Pack 作为独立 catalog（推荐）

新建 `capability_packs` 表，承载 pack 元数据 + capability 引用列表。与 template catalog 走相同模式。优点是字段独立、不污染 `official_models`，符合 issue 087 §3.2 推荐方案。

### 4. Marketplace 与 Catalog 的边界

行业实践（AWS Marketplace、Azure Marketplace、Hugging Face Hub）普遍采用：
- **Catalog**：定义「有什么」（listing 元数据）
- **Marketplace**：定义「如何获取与订阅」（审核、安装、版本、计量）
- 两者共享 catalog 条目，但 marketplace 增加审核状态、订阅关系、版本管理

Curis 当前 `capability_source=marketplace` 是来源标签，但「如何上架/订阅/版本」尚未定义。这与行业实践一致：marketplace 是独立子系统，复用 catalog 元数据。

### 5. Template 类型预留的必要性

#### 5.1 当前 template 类型

- `employee_template`（已落地）
- `department_template`（已落地）

#### 5.2 未来可能的 template 类型

- `workflow_template`：工作流模板（Dify Workflow、Coze Workflow 类似）
- `company_template`：公司结构模板（包含部门组合、员工配置的完整公司蓝图）
- `capability_pack`：能力组合包（多个 capability + template 的打包）

#### 5.3 预留策略建议

不建议在 `CAPABILITY_TYPE` 中预留这些类型（违反 issue 087 §6.2 决策）。建议：
- 各 template 类型走独立表 + 独立 catalog 服务
- 共享 `capability_source` 三态枚举
- 引入 `template_type` 枚举（仅用于 template 体系内部区分），与 `capability_type` 正交

### 6. Admin 与 Workspace 的目录管理边界

行业实践（SaaS 多租户平台）普遍遵循：
- **Official 目录**：平台方独占写，所有租户只读
- **Tenant Private 目录**：租户独占写，仅本租户可见
- **Marketplace 目录**：平台方审核，租户提交后经审核提升为 marketplace

Curis 当前架构与行业实践一致。需明确的是：Pack 类型是否由 Admin 管 official、Workspace 管 tenant_private，还是 Pack 只允许 official（避免租户私有能力组合引发治理复杂度）。

---

## 设计建议

### 1. `CAPABILITY_TYPE` 演进建议

#### 1.1 当前阶段（Phase-3.5 至 Phase-4 S3）

保持 `CAPABILITY_TYPE = ["model", "tool", "connector"]` 不变（issue 087 C5 条件）。

#### 1.2 Phase-4 后期（marketplace gate 解锁后）

仍保持 3 类型不变。理由：
- `official_models` 表字段集是为可执行能力设计的，强行扩展会破坏类型安全
- template / pack 走独立 catalog，已验证可行
- 行业最佳实践（Hugging Face Hub、OpenAI GPT Store）证明分治 catalog 优于单一巨型 catalog

#### 1.3 长期演进（Phase-5+，如需引入新可执行能力类型）

仅当出现新的「可执行能力」类型时才扩展 `CAPABILITY_TYPE`，候选：
- `agent_runtime`：独立 agent 运行时（若未来引入不同于 employee 的 agent 类型）
- `eval_suite`：评估套件（若引入模型评估能力）
- `dataset`：数据集（若引入数据集管理能力）

扩展条件：
- 必须是「可执行资源」（调用产生 usage_event）
- 字段集与 `official_models` 兼容（或接受 additive 扩展）
- 经总控决策席 + 安全边界席 gate 评审

### 2. Official Capability Catalog 应包含的类型

#### 2.1 现阶段（Phase-3.5/Phase-4）

Official Capability Catalog（即 `official_models` 表）仅承载 `model` / `tool` / `connector` 三类。

#### 2.2 Template 体系独立但并列

- `EmployeeTemplateCatalog` → `employee_templates` 表 → `employee_template`
- `DepartmentTemplateCatalog` → `department_templates` 表 → `department_template`

两者与 `CapabilityCatalog` 并列，**不**纳入 Official Capability Catalog，但共享：
- `capability_source` 三态枚举
- 审计事件模式（`template.created` / `template.status_changed`）
- 密钥拒绝逻辑（`_reject_secret_like_metadata`）

#### 2.3 未来 Pack 体系

建议引入 `capability_packs` 表与 `CapabilityPackCatalog` 服务：
- 字段：`pack_id`、`name`、`description`、`capability_refs_json`、`template_refs_json`、`source`、`tenant_id`、`enabled`、`version`、`created_at`、`updated_at`
- `capability_refs_json` 引用 `official_models.model_key`
- `template_refs_json` 引用 `employee_templates.id` / `department_templates.id`
- 三态治理：official（Admin 管）/ tenant_private（CEO 管）/ marketplace（待 G3 gate）

#### 2.4 未来 Workflow / Company Template

- `workflow_templates` 表：Phase-5+ 引入，承载工作流模板（节点图、变量、触发器）
- `company_templates` 表：Phase-5+ 引入，承载公司结构模板（部门组合、员工配置、能力绑定）

两者均走独立 catalog 模式，不纳入 `CAPABILITY_TYPE`。

### 3. `capability_type` 建议枚举

#### 3.1 当前

```python
CAPABILITY_TYPE = ["model", "tool", "connector"]
```

#### 3.2 未来扩展（仅可执行能力）

```python
# Phase-5+ 候选（须经 gate 评审）
CAPABILITY_TYPE = [
    "model",
    "tool",
    "connector",
    "agent_runtime",  # 若引入独立 agent 运行时
    "eval_suite",     # 若引入评估套件
    "dataset",        # 若引入数据集
]
```

#### 3.3 Template 分类枚举（独立体系）

```python
# 建议新增常量（Phase-4 S3 引入）
TEMPLATE_TYPE = [
    "employee_template",
    "department_template",
    # Phase-5+ 候选
    "workflow_template",
    "company_template",
    "capability_pack",
]
```

#### 3.4 Pack 分类枚举

```python
# Phase-5+ 引入
PACK_TYPE = [
    "company_pack",      # 公司蓝图包（部门 + 员工 + 能力）
    "department_pack",   # 部门能力包（多 capability 组合）
    "employee_pack",     # 员工能力包（角色 + 能力组合）
]
```

### 4. official / tenant_private / marketplace 三态目录边界

#### 4.1 边界矩阵

| 类型 | official (Admin 管) | tenant_private (Workspace 管) | marketplace (Admin 审核) |
| --- | --- | --- | --- |
| model | ✅ `official_models` 表 | ✅ `tenant_private_capabilities` 表 | ⚠️ 待 G3 gate |
| tool | ✅ `official_models` 表 | ✅ `tenant_private_capabilities` 表 | ⚠️ 待 G3 gate |
| connector | ✅ `official_models` 表 | ✅ `tenant_private_capabilities` 表 | ⚠️ 待 G3 gate |
| employee_template | ✅ `employee_templates` 表 | ✅ `employee_templates` 表（自有 source 列） | ⚠️ 待 G3 gate |
| department_template | ✅ `department_templates` 表 | ✅ `department_templates` 表（自有 source 列） | ⚠️ 待 G3 gate |
| workflow_template | ✅（Phase-5+） | ✅（Phase-5+） | ⚠️ 待 G3 gate |
| company_template | ✅（Phase-5+） | ✅（Phase-5+） | ⚠️ 待 G3 gate |
| capability_pack | ✅（Phase-5+） | ✅（Phase-5+） | ⚠️ 待 G3 gate |

#### 4.2 三态治理一致性规则

所有类型必须遵循：
- `source` 列 CHECK 三态枚举
- `tenant_id`：official='platform'，tenant_private=实际租户，marketplace='platform'（全局）
- 查询隔离：`source = 'official' or (source = 'tenant_private' and tenant_id = ?)`
- Admin 投影 tenant_private 时仅返回 `(id, name, source, tenant_id, enabled, created_at)`，不返回业务配置字段（issue 087 §5.2）
- 审计事件：`{type}.created` / `{type}.status_changed` 模式
- 密钥拒绝：复用 `_reject_secret_like_metadata`

### 5. Admin 写（/api/platform/*）与 Workspace 读（/api/catalog/*）规则

#### 5.1 Admin 写通道（/api/platform/*）

| 端点 | 方法 | 用途 | 鉴权 |
| --- | --- | --- | --- |
| `/api/platform/capabilities` | POST | 创建 official model/tool/connector | admin token |
| `/api/platform/capabilities/:key/status` | POST | 启停 capability | admin token |
| `/api/platform/employee-templates` | POST | 创建 official employee template | admin token |
| `/api/platform/employee-templates/:id/status` | POST | 启停 template | admin token |
| `/api/platform/department-templates` | POST | 创建 official department template | admin token |
| `/api/platform/department-templates/:id/status` | POST | 启停 template | admin token |
| `/api/platform/capability-packs`（Phase-5+） | POST | 创建 official pack | admin token |
| `/api/platform/marketplace-review`（待 G3） | POST | 审核 marketplace 提交 | admin token |

Admin 写通道**只**写 official 定义，不写 tenant_private，不读 catalog 之外的 Workspace 私有数据。

#### 5.2 Workspace 读通道（/api/catalog/*）

| 端点 | 方法 | 用途 | 鉴权 |
| --- | --- | --- | --- |
| `/api/catalog/capabilities` | GET | 只读 official model/tool/connector | X-Tenant-Id |
| `/api/catalog/employee-templates` | GET | 只读 official employee template | X-Tenant-Id |
| `/api/catalog/department-templates` | GET | 只读 official department template | X-Tenant-Id |
| `/api/catalog/capability-packs`（Phase-5+） | GET | 只读 official pack | X-Tenant-Id |

Workspace 读通道**只**读 official 定义，不读 tenant_private（tenant_private 走 Workspace 内部端点）。

#### 5.3 Workspace 内部写通道（tenant_private）

| 端点 | 方法 | 用途 | 鉴权 |
| --- | --- | --- | --- |
| `/api/tenant/capabilities` | POST | CEO 创建 tenant_private capability | X-Tenant-Id + X-Ceo-Id |
| `/api/tenant/employee-templates` | POST | CEO 创建 tenant_private template | X-Tenant-Id + X-Ceo-Id |
| `/api/tenant/department-templates` | POST | CEO 创建 tenant_private template | X-Tenant-Id + X-Ceo-Id |

Workspace 内部写通道**不**经 `/api/catalog/*`（catalog 是只读通道），不复用 `/api/platform/*`（platform 是 Admin 写通道）。

#### 5.4 接口分工不变式

- Workspace 不写 `/api/platform/*`
- Admin 不读 `/api/catalog/*` 之外的 Workspace 私有数据
- catalog 读 ≠ platform 写（非替代分工，issue 062 §8.1 条件 #3）
- tenant_private 不进入 `/api/catalog/*`（catalog 仅 official + marketplace）

### 6. 是否预留 template / pack 类型

#### 6.1 立即预留（Phase-4 S1-S3）

- `employee_template`：✅ 已落地（`employee_templates` 表）
- `department_template`：✅ 已落地（`department_templates` 表）

#### 6.2 Phase-4 后期预留（待 gate）

- `workflow_template`：Phase-4 S5+ 预留表结构，不实现执行逻辑
  - 字段：`id`、`name`、`description`、`nodes_json`、`edges_json`、`variables_json`、`source`、`tenant_id`、`enabled`、`version`、`created_at`
  - 不含触发器、执行引擎（属 L4 禁止区）
- `company_template`：Phase-5 预留
  - 字段：`id`、`name`、`description`、`department_templates_json`、`employee_templates_json`、`capability_bindings_json`、`source`、`tenant_id`、`enabled`、`version`、`created_at`

#### 6.3 Phase-5+ 预留

- `capability_pack`：Phase-5+ 预留
  - 字段：`id`、`name`、`description`、`capability_refs_json`、`template_refs_json`、`pack_type`、`source`、`tenant_id`、`enabled`、`version`、`created_at`
  - `pack_type` 枚举：`company_pack` / `department_pack` / `employee_pack`

#### 6.4 预留策略原则

- 表结构可提前预留（additive，不破坏既有契约）
- API 端点不提前实现（避免误用）
- `CAPABILITY_TYPE` 不扩展（保持 3 类型）
- 各类型走独立 catalog 服务，共享 `capability_source` 三态治理

### 7. 类型归属规则

#### 7.1 Admin 管 official / marketplace 的类型

- `model` / `tool` / `connector`：✅ 已由 Admin 管 official
- `employee_template` / `department_template`：✅ Phase-4 S3 由 Admin 管 official
- `workflow_template` / `company_template`：✅ Phase-5+ 由 Admin 管 official
- `capability_pack`：✅ Phase-5+ 由 Admin 管 official

marketplace 提交审核后，所有类型均经 Admin 审核提升为 `source='marketplace'`。

#### 7.2 Workspace 管 tenant_private 的类型

- `model` / `tool` / `connector`：✅ CEO 可创建 tenant_private（经 `tenant_private_capabilities` 表）
- `employee_template` / `department_template`：✅ CEO 可创建 tenant_private（经 `employee_templates` / `department_templates` 表 source 列）
- `workflow_template` / `company_template`：✅ Phase-5+ CEO 可创建 tenant_private
- `capability_pack`：建议 Phase-5+ 允许 CEO 创建 tenant_private pack，但须额外评审（pack 跨多 capability 引用，治理复杂度更高）

#### 7.3 Pack 治理建议

- `company_pack`：建议只允许 official + marketplace，不允许 tenant_private（公司蓝图应由平台审核）
- `department_pack` / `employee_pack`：允许 tenant_private（CEO 可组合私有能力包）

### 8. 数据模型建议

#### 8.1 现有表保持不变

- `official_models`：保持 3 类型，additive 扩展已完成（`type` / `name` 列）
- `tenant_private_capabilities`：保持 CHECK 约束 `('model', 'tool', 'connector')`，**不**扩展（issue 087 C4 条件）
- `employee_templates` / `department_templates`：保持现有结构，建议 additive 补 `updated_at` / `schema_version` 列（issue 087 §1.2 缺失字段建议）

#### 8.2 新增表（Phase-4 S3+）

- `capability_packs`（Phase-5+）：
  ```sql
  create table if not exists capability_packs (
    id                    text primary key,
    name                  text not null,
    description           text not null default '',
    pack_type             text not null
                          check (pack_type in ('company_pack', 'department_pack', 'employee_pack')),
    capability_refs_json  text not null default '[]',
    template_refs_json    text not null default '[]',
    source                text not null default 'official'
                          check (source in ('official', 'tenant_private', 'marketplace')),
    tenant_id             text not null default 'platform',
    enabled               integer not null default 1,
    version               text not null default '0.0.1',
    schema_version        text not null default '0.0',
    created_at            text not null default current_timestamp,
    updated_at            text not null default current_timestamp
  );
  ```

#### 8.3 新增 catalog 服务（Phase-4 S3+）

- `EmployeeTemplateCatalog`：CRUD + 启停 + `template.created` / `template.status_changed` 审计事件
- `DepartmentTemplateCatalog`：同上
- `CapabilityPackCatalog`（Phase-5+）：CRUD + 启停 + `pack.created` / `pack.status_changed` 审计事件

所有服务遵循 `CapabilityCatalog` 相同设计模式：复用 `_reject_secret_like_metadata`、append-only 审计、active/inactive 状态机（无物理删除）。

### 9. API 设计建议

#### 9.1 Admin 写端点（Phase-4 S3）

```
POST   /api/platform/employee-templates
GET    /api/platform/employee-templates          # 列表（含 inactive）
PATCH  /api/platform/employee-templates/:id      # 编辑
POST   /api/platform/employee-templates/:id/status  # 启停

POST   /api/platform/department-templates
GET    /api/platform/department-templates
PATCH  /api/platform/department-templates/:id
POST   /api/platform/department-templates/:id/status
```

#### 9.2 Workspace 读端点（Phase-4 S1）

```
GET    /api/catalog/employee-templates            # 只读 official
GET    /api/catalog/department-templates           # 只读 official
```

#### 9.3 Workspace 内部写端点（Phase-4 S2）

```
POST   /api/tenant/employee-templates             # CEO 创建 tenant_private
GET    /api/tenant/employee-templates              # 列表（official + 本租户 private）
PATCH  /api/tenant/employee-templates/:id          # 编辑本租户 private
POST   /api/tenant/employee-templates/:id/status   # 启停本租户 private

POST   /api/tenant/department-templates
GET    /api/tenant/department-templates
PATCH  /api/tenant/department-templates/:id
POST   /api/tenant/department-templates/:id/status
```

### 10. 边界规则

#### 10.1 不变式（Phase-4 全程）

- `CAPABILITY_TYPE` 保持 `["model","tool","connector"]` 不变
- `tenant_private_capabilities` 表 `capability_type` CHECK 不扩展
- template / pack 走独立 catalog，不复用 `official_models` 表
- template / pack 不被 `Orchestrator` / `ToolRouter` / `AIEmployee` 引用（执行层仍锁定）
- template / pack 不持久化任何凭证/密钥
- template / pack 不触发任务路由或 prompt 注入

#### 10.2 治理一致性

- 所有类型共享 `capability_source` 三态枚举
- 所有类型共享 `_reject_secret_like_metadata` 密钥拒绝
- 所有类型共享 append-only 审计事件模式（`{type}.created` / `{type}.status_changed`）
- 所有类型共享 active/inactive 状态机（无物理删除）

#### 10.3 Admin 可见性

- Admin 可见所有 official / marketplace 定义（完整字段）
- Admin 可见所有 tenant_private 的元数据（`id`、`name`、`source`、`tenant_id`、`enabled`、`created_at`）
- Admin **不可见** tenant_private 的业务配置（`default_instructions`、`default_model_policy_json`、`metadata_json`）

#### 10.4 Workspace 可见性

- Workspace 可读所有 official 定义（经 `/api/catalog/*`）
- Workspace 可读所有 marketplace 定义（待 G3 gate 解锁后）
- Workspace 仅可读本租户 tenant_private 定义（经 Workspace 内部端点）

---

## 前置条件

### 1. Phase-4 解锁条件（5 项 gate）

| Gate | 条件 | 解锁方式 |
| --- | --- | --- |
| G-C1 | ADR-0017「员工 CRUD」禁止区部分解禁（Template 定义层） | 提交独立 ADR，总控决策席 + 安全边界席 gate |
| G-C2 | `department_templates` vs `department_types` 双层关系文档化 | 更新 ADR-0028 §6 或新 ADR |
| G-C3 | Admin template catalog 服务设计 | 设计文档（含本研究的 API 建议） |
| G-C4 | `tenant_private_capabilities` 不承载 template 的设计意图文档化 | 更新 ADR-0028 或代码注释 |
| G-C5 | `CAPABILITY_TYPE` 保持 3 类型的决策文档化 | 本研究与 issue 087 作为 ADR 输入 |

### 2. Phase-4 S3 解锁条件

- Phase-4 S1（Workspace 只读 official template）已完成
- Phase-4 S2（Workspace tenant_private template CRUD）已完成
- G-C1 / G-C3 gate 已通过

### 3. Marketplace 解锁条件

- G3 gate（跨租户 marketplace）经总控决策席 + 安全边界席双签解锁
- 独立 ADR（如 ADR-00xx Marketplace 审核流程）已落
- 审核队列表（`marketplace_reviews`）已设计

### 4. Pack 解锁条件

- Phase-5+ 才考虑引入 `capability_pack`
- 前置：employee/department template CRUD 已稳定运行
- 前置：marketplace 审核流程已上线（pack 是天然的 marketplace 商品）

### 5. Workflow / Company Template 解锁条件

- `workflow_template`：L4 工作流编排禁止区部分解禁（须独立 ADR）
- `company_template`：Phase-5 公司蓝图治理评审通过

---

## 结论

### 1. 核心结论

1. **`CAPABILITY_TYPE` 保持 `["model","tool","connector"]` 不变**（issue 087 C5 决策确认）。template / pack 走独立 catalog 体系，符合行业最佳实践（Hugging Face Hub、OpenAI GPT Store 均采用分治 catalog）。

2. **Official Capability Catalog 仅承载可执行能力**（model/tool/connector）。template / pack 是定义配置，不是可执行资源，不应纳入 `official_models` 表。

3. **Template 体系独立但并列**：
   - `EmployeeTemplateCatalog` → `employee_templates` 表
   - `DepartmentTemplateCatalog` → `department_templates` 表
   - 共享 `capability_source` 三态治理语义，与 `CapabilityCatalog` 模式一致

4. **未来 Pack 体系走独立 catalog**：`CapabilityPackCatalog` → `capability_packs` 表（Phase-5+）。Pack 作为能力组合包，是天然的 marketplace 商品类型。

5. **未来 Workflow / Company Template 走独立 catalog**（Phase-5+），不纳入 `CAPABILITY_TYPE`。

### 2. `capability_type` 演进路径

- **当前**：`["model","tool","connector"]`
- **Phase-4**：保持不变
- **Phase-5+**：仅当出现新的「可执行能力」类型时才扩展（如 `agent_runtime` / `eval_suite` / `dataset`），须经 gate 评审
- **Template 分类**：独立 `TEMPLATE_TYPE` 枚举（`employee_template` / `department_template` / `workflow_template` / `company_template`）
- **Pack 分类**：独立 `PACK_TYPE` 枚举（`company_pack` / `department_pack` / `employee_pack`）

### 3. 三态目录边界

所有类型（capability / template / pack）共享 `capability_source` 三态治理：
- **official**：Admin 管，全局可见，经 `/api/platform/*` 写、`/api/catalog/*` 读
- **tenant_private**：Workspace 管，仅本租户可见，经 Workspace 内部端点写读
- **marketplace**：Admin 审核，订阅租户可见，待 G3 gate 解锁

### 4. Admin 写 vs Workspace 读规则

- **Admin 写通道**（`/api/platform/*`）：仅写 official 定义，不碰 tenant_private
- **Workspace 读通道**（`/api/catalog/*`）：仅读 official + marketplace 定义
- **Workspace 内部写通道**：写 tenant_private，不经 `/api/catalog/*` 或 `/api/platform/*`
- **非替代分工**（issue 062 §8.1 条件 #3）：catalog 读 ≠ platform 写

### 5. 类型归属规则

- **Admin 管 official / marketplace**：所有类型（model/tool/connector/template/pack）
- **Workspace 管 tenant_private**：所有类型（建议 pack 中 `company_pack` 仅允许 official，不允许 tenant_private）
- **Marketplace 审核**：所有类型经 Admin 审核后提升为 `source='marketplace'`

### 6. 一句话总结

**Curis 能力目录应保持「分治 catalog + 共享三态治理」的架构**：`CAPABILITY_TYPE` 永远只承载可执行能力（model/tool/connector），template / pack / workflow_template / company_template 走独立 catalog 体系，所有类型共享 `capability_source` 三态治理与 `_reject_secret_like_metadata` 密钥拒绝。Phase-4 优先解锁 5 项 gate，按 S1→S5 切片推进 employee/department template；Phase-5+ 视需求引入 pack / workflow_template / company_template，marketplace 待 G3 gate 解锁后落地。
