# 部门模板（Department Template）领域研究

> 研究范围：Curis Admin Platform 的部门模板（DepartmentTemplate）应解决什么问题、字段设计、与 `department_types` 表的双层关系（issue 087 C2）、official / tenant_private / marketplace 三态边界、SOP 流程与员工配置、Phase-4 实现边界与预留策略。
>
> 研究性质：纯研究文档，不含实现方案、不含代码改动。所有结论须与 ADR-0028 共享契约、issue 087 Phase-3.5 决策、capability-catalog-research 决策对齐。
>
> 关键约束：issue 087 §2 (C2) 明确 `department_templates` 与 `department_types` 的双层关系须显式文档化——`department_types` 是类型注册表（已解禁），`department_templates` 是模板治理层（source 三态），两者通过 `department_templates.department_type` → `department_types.type_key` 关联。

---

## 问题定义

### 1. 部门模板在 Curis 中解决什么问题

Curis 的 AI 公司由部门组成，部门由员工组成。但「部门」这一概念在 Curis 中有三个层次：

- **部门类型（Department Type）**：部门的**类别注册表**，如 `business.general` / `function.research`。由 `department_types` 表承载，`is_system=1` 表示系统内置类型。已解禁。
- **部门模板（Department Template）**：定义部门类型下的**具体配置蓝图**——SOP 流程、默认员工模板组合、治理规则、能力包引用。由 `department_templates` 表承载，`source` 三态治理。Phase-3.5 已落地。
- **部门实例（Department Instance）**：租户内真实存在的部门，有生命周期（draft → active → disabled）。由 `departments` + `company_department_state` 表承载。经 governance gate 解锁。

部门模板解决的核心问题是：

1. **配置复用**：同一部门类型可有多个模板（official 标准模板 + tenant_private 定制模板），CEO 无需每次从零配置 SOP 与员工组合。
2. **SOP 标准化**：official 部门模板提供跨租户的 SOP 基线（如 MetaGPT 研发部 SOP），保证流程一致性。
3. **员工组合预设**：部门模板预置 `default_employee_templates_json`，CEO 应用模板即获得推荐的角色组合。
4. **治理与能力绑定**：部门模板可引用治理策略与能力包，统一部门级治理与能力配置。
5. **类型与模板分离**：`department_types` 是稳定的类型注册表（ADR-0023 D2 锁定 7 列 DDL），`department_templates` 是可演进的配置层，两者分离避免破坏锁定契约。

简言之：**部门类型定义类别，部门模板定义配置蓝图，部门实例是蓝图的具体化**。

### 2. 为什么 Phase-3.5 偏离 ADR-0028 §6 原方案

ADR-0028 §6 原方案：DepartmentTemplate = `department_types` 表 + additive `source` 列。**实际实现**（Phase-3.5）：Workspace 团队创建了独立的 `department_templates` 表。

issue 087 §2.1 评审意见认为**实际实现更优**：
1. **不破坏锁定 DDL**：`department_types` 有 ADR-0023 D2 reservation test 要求固定 7 列，加 `source` 列需解锁该约束。
2. **关注点分离**：`department_types` 是类型注册表，`department_templates` 是模板治理层，职责不同。
3. **一对多关系**：同一 `department_type` 可有多个 template（official + tenant_private），单表无法表达。

此偏离须在 ADR-0028 §6 或新 ADR 中显式文档化（C2 条件）。

---

## 现状分析

### 1. `department_types` 表（类型注册表，已解禁）

`database.py` 定义 `department_types` 表（ADR-0023 D2 锁定 7 列 DDL）：`type_key`（PK）/ `category` / `display_name` / `description` / `manifest_json`（7 键 MANIFEST_FIELDS 契约）/ `manifest_schema_version` / `is_system`。已解禁，由 `manage_department_types` CRUD（human-approval 门控）。

### 2. `department_templates` 表（模板治理层，Phase-3.5 已落地）

`database.py:472-483` 定义 `department_templates` 表：`id`（PK）/ `name` / `department_type`（→ `department_types.type_key`）/ `description` / `default_employee_templates_json` / `source`（CHECK 三态）/ `tenant_id` / `enabled` / `created_at`。

### 3. `departments` 表（部门实例）

`database.py` 定义 `departments` 表（ADR-0026 D2.impl）：`department_id`（PK）/ `tenant_id` / `type_key` / `display_name` / `status`（active/disabled）/ `created_at` / `updated_at`。另有 `company_department_state` 表承载 CEO 级启用态（human-approval gate 不解除）。

### 4. 查询隔离已实现

`list_department_templates` 已实现三态查询隔离：`source = 'official' or (source = 'tenant_private' and tenant_id = ?)`。

### 5. 已有决策锚点

- **issue 087 §2 (C2)**：双层关系须文档化。
- **issue 087 §2.2**：`is_system` 向后兼容，无迁移问题。
- **issue 087 §6.2 (C5)**：部门模板走独立 catalog，不扩展 `CAPABILITY_TYPE`。
- **issue 087 §5.3 (C4)**：`tenant_private_capabilities` 不承载 template。
- **ADR-0028 §6.2**：`manifest_json` 归属问题（issue 087 §10 #2 待明确）。

---

## 竞品参考

### 1. MetaGPT 研发部 SOP

MetaGPT 核心哲学 `Code = SOP(Team)`，将团队 SOP 显式化。标准 SOP：接收需求 → 产品经理输出 PRD → 架构师设计 → 项目经理任务分解 → 工程师编码 → QA 测试 → 汇总产出物。

可借鉴点：标准 SOP 作为 official DepartmentTemplate 的 `sop_flow`；`Code = SOP(Team)` 哲学转化为部门模板 = SOP(Employees + Capabilities)；每步明确输入/输出（Phase-5+ WorkflowStep 的 `expected_output`）。

不可借鉴点：完整仓库生成、SOPChain 引擎、角色直接持有 LLM 配置。

### 2. ChatDev 软件公司流程

ChatDev 1.0 的 ChatChain 瀑布流程：`DemandAnalysis → Coding → Testing → Manual`，每个阶段有固定参与者、阶段门禁、顺序依赖、无并行。核心创新是功能研讨会（角色不自由交流，通过结构化会议协作）。

可借鉴点：瀑布 SOP 作为研发部 SOP 参考基线；双角色步骤（owner + reviewer）影响 WorkflowStep 设计（Phase-5+）；`max_revision_count` 限制返工，编码为 `governance_rules_json`。

不可借鉴点：CEO/CTO/CPO 高管角色名；无界研讨会对话；完整瀑布用于简单任务；编译时固定工作流。

### 3. CrewAI Sequential Process

CrewAI 的 Sequential Process 是顺序执行，前任务输出作为后任务输入。Phase-4 默认流程模式：`DepartmentTemplate.default_process = "sequential"`。Hierarchical Process 推迟到 Phase-5+。

### 4. AWS Service Catalog Portfolio 模式

Portfolio + Product 双层结构对应 Curis 的 `department_types`（Portfolio 层）+ `department_templates`（Product 层），与 issue 087 §2.1 双层设计一致。

---

## 字段设计建议

### 1. DepartmentTemplate 字段表（扩展现有）

| 字段 | 类型 | 必填 | 来源 | 阶段 | 边界 |
| --- | --- | --- | --- | --- | --- |
| `id` | text PK | ✅ | 创建方 | Phase-4 S1 | 命名空间：`official.*` / `tenant:<tid>:*` / `marketplace:*` |
| `name` | text | ✅ | 创建方 | Phase-4 S1 | 模板展示名 |
| `department_type` | text | ✅ | 创建方 | Phase-4 S1 | → `department_types.type_key` |
| `description` | text | ✅ | 创建方 | Phase-4 S1 | 模板说明 |
| `default_employee_templates_json` | text (JSON) | ✅ | 创建方 | Phase-4 S1 | 引用 `employee_templates.id` |
| `source` | text (enum) | ✅ | 创建方 | Phase-4 S1 | CHECK `('official','tenant_private','marketplace')` |
| `tenant_id` | text | ✅ | 系统 | Phase-4 S1 | official='platform'，private=实际租户 |
| `enabled` | integer | ✅ | 创建方 | Phase-4 S1 | 1/0 |
| `created_at` | datetime | ✅ | 系统 | Phase-4 S1 | ISO8601 UTC |
| `updated_at` | datetime | ❌ | 系统 | Phase-4 S1 additive | **缺失字段补齐**（issue 087 §2.3） |
| `schema_version` | text | ❌ | 系统 | Phase-4 S1 additive | ADR-0028 §0.1 元约定 |
| `sop_flow_json` | text (JSON) | ❌ | 创建方 | Phase-4+ 预留 | SOP 流程 JSON（节点列表 + 顺序） |
| `default_workflow_template_id` | text | ❌ | 创建方 | Phase-5+ 预留 | → `workflow_templates.id` |
| `default_process` | text | ❌ | 创建方 | Phase-4+ 预留 | 流程模式（默认 `sequential`） |
| `default_capability_pack_refs` | text (JSON) | ❌ | 创建方 | Phase-5+ 预留 | 引用 `capability_packs.id` |
| `governance_rules_json` | text (JSON) | ❌ | 创建方 | Phase-4+ 预留 | 部门级治理规则 |
| `default_governance_policy_ref` | text | ❌ | 创建方 | Phase-5+ 预留 | 引用 `platform_policies` |
| `version` | text | ❌ | 创建方 | Phase-5+ 预留 | 语义化版本 |

### 2. 字段设计理由

#### 2.1 `sop_flow_json` vs `default_workflow_template_id`

| 字段 | 阶段 | 内容 |
| --- | --- | --- |
| `sop_flow_json` | Phase-4+ 预留 | 轻量级 SOP 流程 JSON（节点列表 + 顺序），自包含 |
| `default_workflow_template_id` | Phase-5+ 预留 | 引用独立的 `workflow_templates` 表（复杂工作流） |

`sop_flow_json` 建议形状：
```json
{
  "steps": [
    {"name": "需求理解", "owner_role": "product_manager", "expected_output": "需求文档"},
    {"name": "任务拆分", "owner_role": "tech_lead", "expected_output": "任务清单"},
    {"name": "架构设计", "owner_role": "architect", "expected_output": "架构文档"},
    {"name": "编码", "owner_role": "frontend_engineer|backend_engineer", "expected_output": "代码"},
    {"name": "测试", "owner_role": "qa_engineer", "expected_output": "测试报告"},
    {"name": "汇报", "owner_role": "tech_lead", "expected_output": "汇总报告"}
  ],
  "process": "sequential",
  "max_revision_count": 3
}
```

#### 2.2 `default_employee_templates_json` 引用方式

- official 部门模板应仅引用 official 员工模板
- tenant_private 部门模板可引用 official + 本租户 private 员工模板
- marketplace 部门模板应仅引用 official + marketplace 员工模板（避免跨租户依赖）

#### 2.3 `governance_rules_json` 边界

编码部门级治理规则：`max_revision_count`（返工上限）、`approval_gates`（审批门）、`cost_guardrails`（成本护栏，**仅形状，金额计算待 G1 gate**）。

#### 2.4 manifest_json 归属确认

**确认**：`manifest_json`（7 键 MANIFEST_FIELDS）由 `department_types` 层承载，`department_templates` **不重复**此字段。理由：manifest 描述类型级能力上限，template 描述模板级具体配置，职责不同。查询时 JOIN `department_types` 即可获取 manifest。此分工须在 ADR-0028 §6.2 或新 ADR 中显式文档化（issue 087 §10 #2）。

### 3. 命名空间

| source | 唯一键 | 示例 |
| --- | --- | --- |
| `official` | 全局 key | `official.department.business_general` |
| `tenant_private` | 复合 key | `tenant:<tid>:department.my_custom_research_dept` |
| `marketplace` | 全局 key | `marketplace:department.finance_research_pack_v2` |

### 4. 首个 Official DepartmentTemplate 建议

```text
DepartmentTemplate: official.department.business_general
  name: "通用研发部"
  department_type: business.general
  description: "标准软件研发部门，含 Tech Lead / PM / Architect / FE / BE / QA 六个角色"
  default_employee_templates_json:
    - official.employee.tech_lead
    - official.employee.product_manager
    - official.employee.architect
    - official.employee.frontend_engineer
    - official.employee.backend_engineer
    - official.employee.qa_engineer
  default_process: sequential
  source: official
  tenant_id: platform
```

### 5. 未来部门模板扩展

Phase-4 仅实现研发部，未来扩展须分阶段经 gate：内容运营部（content_ops）、投资研究部（investment_research）、电商运营部（ecommerce）、BI/数据部（bi_data）。研发部证明模板/运行时模型可行后再扩展。

#### 5.1 内容运营部（content_ops）预留

| 角色 | responsibility | capability_types |
| --- | --- | --- |
| content_strategist | 制定内容策略与选题方向 | `["model"]` |
| researcher | 收集素材、研究背景 | `["model", "tool", "connector"]` |
| copywriter | 撰写初稿 | `["model"]` |
| editor | 审校、润色、合规检查 | `["model", "tool"]` |
| distribution_operator | 多渠道发布、SEO 优化 | `["model", "tool", "connector"]` |

#### 5.2 投资研究部（investment_research）预留

| 角色 | responsibility | capability_types |
| --- | --- | --- |
| market_researcher | 行业、市场、政策研究 | `["model", "tool", "connector"]` |
| financial_analyst | 财报分析、估值建模 | `["model", "tool"]` |
| risk_analyst | 风险识别与压力测试 | `["model", "tool"]` |
| memo_writer | 撰写投资备忘录 | `["model"]` |
| portfolio_monitor | 持仓监控、预警 | `["model", "tool", "connector"]` |

#### 5.3 电商运营部（ecommerce）预留

| 角色 | responsibility | capability_types |
| --- | --- | --- |
| product_researcher | 选品研究、竞品分析 | `["model", "tool", "connector"]` |
| listing_operator | 商品上架、详情优化 | `["model", "tool"]` |
| customer_support | 客户咨询、售后处理 | `["model", "connector"]` |
| campaign_operator | 营销活动、广告投放 | `["model", "tool"]` |
| analytics_operator | 数据分析、报表 | `["model", "tool", "connector"]` |

#### 5.4 BI/数据部（bi_data）预留

| 角色 | responsibility | capability_types |
| --- | --- | --- |
| data_engineer | 数据管道、ETL | `["model", "tool", "connector"]` |
| data_analyst | 数据分析、可视化 | `["model", "tool"]` |
| bi_developer | 仪表盘、报表开发 | `["model", "tool"]` |
| data_scientist | 建模、预测 | `["model", "tool"]` |

以上扩展均推迟至 Phase-5+ 视研发部模板验证结果后再启动，每个新部门模板须独立 ADR + 5 项 gate 评估。

---

## 与 department_types 的双层关系（C2 条件）

### 1. 双层关系文档化

```text
Department Type Registry = department_types（不变，is_system 语义保留）
  ├── 类型注册表：type_key / category / display_name / description
  ├── manifest 契约：manifest_json（7 键 MANIFEST_FIELDS）
  └── 系统标记：is_system

Department Template Catalog = department_templates（新增，source 三态治理）
  ├── 模板配置：name / description / department_type（→ type_key）
  ├── 员工组合：default_employee_templates_json
  ├── SOP 流程：sop_flow_json / default_workflow_template_id
  ├── 治理规则：governance_rules_json / default_governance_policy_ref
  ├── 能力包引用：default_capability_pack_refs
  └── 三态治理：source / tenant_id / enabled

Department Instance = departments + company_department_state（不变）
```

### 2. 关系图

```text
department_types（1）─── type_key ───→（N）department_templates
                                         │ default_employee_templates_json
                                         ↓
                                    employee_templates（N）
                                         │ default_capability_types_json
                                         ↓
                                    CAPABILITY_TYPE（model/tool/connector）
```

### 3. 职责分工

| 层 | 表 | 职责 | 管理方 | ADR-0017 |
| --- | --- | --- | --- | --- |
| Type Registry | `department_types` | 类型注册 + manifest 契约 | Admin（is_system=1）/ CEO（is_system=0） | 已解禁 |
| Template Catalog | `department_templates` | 模板配置 + 三态治理 | Admin（official）/ CEO（tenant_private） | 可解禁 |
| Instance | `departments` + `company_department_state` | 真实部门实例 | CEO（经 governance gate） | 部分解禁 |

### 4. is_system vs source 兼容性

`department_types.is_system` 保持不变；`department_templates.source` 在创建时显式设置；两表通过 `department_type` → `type_key` 关联；无迁移问题；向后兼容。

### 5. 一对多关系表达

同一 `department_type` 可有多个 template：如 `business.general` 类型下可有 official 标准研发部、tenant:acme 定制敏捷研发部、marketplace 研究密集型研发部。这种一对多关系是独立表优于加列的核心优势。

### 6. manifest_json 7 键契约（参考）

`department_types.manifest_json` 锁定 7 键 MANIFEST_FIELDS 契约（ADR-0023 D2 reservation test）：

| 键 | 含义 | 示例 |
| --- | --- | --- |
| `allowed_employee_roles` | 允许的角色枚举 | `["tech_lead", "product_manager", ...]` |
| `allowed_capability_types` | 允许的能力类型 | `["model", "tool", "connector"]` |
| `governance_required` | 治理必填项 | `["sop_flow", "cost_guardrails"]` |
| `max_employee_count` | 员工数上限 | `20` |
| `min_employee_count` | 员工数下限 | `1` |
| `allowed_workflow_patterns` | 允许的工作流模式 | `["sequential", "parallel"]` |
| `cost_center_required` | 是否需要成本中心 | `true` |

（具体 7 键以 ADR-0023 D2 文档为准，本表为示意。）

---

## 治理边界

### Admin 管理（official / marketplace）

#### 1. Official Department Template

- Admin 经 `/api/platform/department-templates` 写通道，`source='official'`，`tenant_id='platform'`
- 全局可见，所有租户经 `/api/catalog/department-templates` 只读
- 审计事件：`template.created` / `template.status_changed`

#### 2. Marketplace Department Template（Department Pack）

- CEO 提交 tenant_private 部门模板 → Admin 经 `/api/platform/marketplace-review` 审核 → approve 后提升为 `source='marketplace'` + `tenant_id='platform'`
- 跨租户共享触发 G3 gate
- marketplace 部门模板即「Department Pack」

#### 3. Admin API 端点建议

```
POST   /api/platform/department-templates          # 创建 official
GET    /api/platform/department-templates          # 列表（含 inactive）
PATCH  /api/platform/department-templates/:id      # 编辑
POST   /api/platform/department-templates/:id/status  # 启停
```

#### 4. Admin 可见性

- Admin 可见所有 official / marketplace 部门模板（完整字段）
- Admin 可见 tenant_private 部门模板的元数据
- Admin **不可见** tenant_private 部门模板的业务配置（`sop_flow_json`/`governance_rules_json`/`default_employee_templates_json`）

### Workspace 管理（tenant_private）

- CEO 经 `/api/tenant/department-templates` 内部写通道，`source='tenant_private'`
- CEO 可基于 official 模板派生 tenant_private 模板
- CEO 可从零创建 tenant_private 模板
- CEO 可提交至 marketplace 审核
- CEO **不可**修改 official 模板，**不可**跨租户共享

只读通道（Phase-4 S1）：`GET /api/catalog/department-templates`

内部写通道（Phase-4 S2）：
```
POST   /api/tenant/department-templates            # CEO 创建 tenant_private
GET    /api/tenant/department-templates             # 列表
PATCH  /api/tenant/department-templates/:id         # 编辑本租户 private
POST   /api/tenant/department-templates/:id/status  # 启停本租户 private
```

### 禁止区

#### 1. ADR-0017 禁止区

| 层次 | 表 | ADR-0017 | Phase-4 |
| --- | --- | --- | --- |
| Type Registry | `department_types` | 已解禁 | 不变 |
| Template 定义 | `department_templates` | **可解禁** | S1-S3 解禁 |
| Instance | `departments` + `company_department_state` | 部分解禁 | 不新增 |

#### 2. ADR-0028 §9 gate

G1（`governance_rules_json.cost_guardrails` 金额计算）、G3（marketplace Department Pack 跨租户共享）、G5（LOCKED_ACTIONS）。

#### 3. 不变式（Phase-4 全程）

- `department_templates` 不得被 `Orchestrator`/`ToolRouter`/`AIEmployee` 直接引用
- 不持久化凭证、不触发任务路由/prompt 注入
- 不扩展 `CAPABILITY_TYPE`，不复用 `official_models`/`tenant_private_capabilities` 表
- `department_types` 的 7 列 DDL 契约（ADR-0023 D2）不被破坏

---

## 前置条件

### 1. Phase-4 解锁条件

- **G-C2**：`department_templates` vs `department_types` 双层关系文档化（更新 ADR-0028 §6 或新 ADR）
- **G-C3**：Admin template catalog 服务设计（`DepartmentTemplateCatalog`）
- **G-C4**：`tenant_private_capabilities` 不承载 template 的设计意图文档化
- **G-C5**：`CAPABILITY_TYPE` 保持 3 类型的决策文档化

### 2. 切片解锁依赖

- S2 依赖 S1 完成 + G-C2 gate 通过
- S3 依赖 S2 完成 + G-C3 gate 通过
- Marketplace 依赖 G3 gate 解锁 + 独立 ADR + 审核队列表设计

### 3. manifest_json 归属文档化

issue 087 §10 #2 须在 ADR-0028 §6.2 或新 ADR 中显式文档化：确认 manifest 由 `department_types` 层承载，`department_templates` 不重复。

---

## Phase-4 建议

### 1. Phase-4 实现

| 切片 | 内容 | 优先级 |
| --- | --- | --- |
| S1 | Workspace 只读 official department template | P0 |
| S1 | additive 补齐 `updated_at` / `schema_version` 列 | P0 |
| S1 | 预置 1 个 official department template（通用研发部） | P0 |
| S2 | Workspace tenant_private department template CRUD | P0 |
| S3 | Admin official department template 管理 API（`DepartmentTemplateCatalog`） | P1 |
| S4 | Template-Capability 绑定（部门 → 员工 → 能力类型链路验证） | P1 |

### 2. Phase-4 预留（不实现）

`sop_flow_json`（依赖 WorkflowStep，Phase-5+）、`default_workflow_template_id`（依赖 `workflow_templates`，Phase-5+）、`default_process`（Phase-5+）、`default_capability_pack_refs`（依赖 `capability_packs`，Phase-5+）、`governance_rules_json`（Phase-5+）、`default_governance_policy_ref`（Phase-5+）、`version`（Phase-5+ marketplace）、部门实例创建/激活（governance gate）、Marketplace Department Pack 审核（G3 gate 后）、内容/投资/电商/BI 部门模板。

### 3. 永不实现

部门模板直接执行任务、持久化凭证、触发 prompt 注入、扩展 `CAPABILITY_TYPE`、破坏 `department_types` 7 列 DDL 契约、复用 `official_models`/`tenant_private_capabilities` 表、完整 ChatChain/SOPChain 运行时、无界研讨会对话。

---

## Phase-4 S1-S4 详细验收标准

### S1 验收（只读 official）

- [ ] `GET /api/catalog/department-templates` 返回 1 个 official 模板（通用研发部）
- [ ] 返回字段含 `id`/`name`/`department_type`/`description`/`default_employee_templates_json`/`source`/`enabled`
- [ ] `default_employee_templates_json` 引用 6 个 official employee templates
- [ ] `updated_at` / `schema_version` 列已 additive 补齐
- [ ] 命名空间校验：official 模板 `id` 以 `official.department.` 开头
- [ ] 查询隔离：tenant A 无法看到 tenant B 的 tenant_private 模板
- [ ] JOIN `department_types` 可获取 `manifest_json`、`display_name`、`is_system`

### S2 验收（tenant_private CRUD）

- [ ] `POST /api/tenant/department-templates` 创建 tenant_private 成功
- [ ] 创建时 `source` 强制为 `tenant_private`，`tenant_id` 强制为当前租户
- [ ] 命名空间校验：tenant_private 模板 `id` 须以 `tenant:<tid>:department.` 开头
- [ ] `PATCH` 仅允许修改本租户 private 模板，official 模板只读
- [ ] `POST /:id/status` 启停仅作用于本租户 private 模板
- [ ] 派生 API：`POST /api/tenant/department-templates/:id/derive` 基于 official 创建 tenant_private 副本
- [ ] `default_employee_templates_json` 引用校验：仅允许引用 official + 本租户 private 员工模板
- [ ] 软删除策略：`enabled=0` 而非物理删除

### S3 验收（Admin 管理）

- [ ] `POST /api/platform/department-templates` Admin 创建 official 成功
- [ ] Admin 可见所有 official / marketplace 模板完整字段
- [ ] Admin 可见 tenant_private 模板元数据
- [ ] Admin **不可见** tenant_private 模板的 `sop_flow_json` / `governance_rules_json` / `default_employee_templates_json`
- [ ] 审计事件 `template.created` / `template.status_changed` 写入 `audit_events` 表

### S4 验收（Template-Capability 绑定）

- [ ] 部门 → 员工 → 能力类型链路验证通过
- [ ] 从 `department_templates.default_employee_templates_json` → `employee_templates.id` → `default_capability_types_json` → `CAPABILITY_TYPE` 全链路可追溯
- [ ] 引用完整性 CHECK：删除 department template 前须检查是否被 company template 引用（Phase-5+）；删除 employee template 前须检查是否被 department template 引用
- [ ] `department_types.manifest_json.allowed_employee_roles` 与 `default_employee_templates_json` 中 employee role 一致性校验

---

## 风险分析

### 1. 设计风险

| 风险 | 描述 | 影响 | 缓解 |
| --- | --- | --- | --- |
| 类型与模板混淆 | `department_types` vs `department_templates` 职责不清 | 字段重复或缺失 | C2 双层关系文档化 + 字段归属明确（manifest 归 type，sop 归 template） |
| manifest 与 sop 割裂 | `manifest_json` 限制与 `sop_flow_json` 配置不一致 | 模板应用失败 | 应用模板时校验 `sop_flow` 是否符合 `manifest.allowed_workflow_patterns` |
| 引用循环 | 部门模板引用员工模板，员工模板 `department_type` 又引用部门类型 | 死循环 | 引用方向严格自上而下，`employee_templates.department_type` 仅作语义标签，不参与运行时解析 |
| 一对多治理复杂 | 同一 `department_type` 下多个 template 选择困难 | CEO 困惑 | UI 默认展示 official 模板 + 推荐标签 |

### 2. 实现风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| C2 gate 延迟 | 双层关系 ADR 未通过 | Phase-4 S1 不依赖 gate（仅只读），S2 须 gate 通过 |
| `updated_at` 补齐失败 | additive 列添加失败 | migration 脚本 + 默认值 `created_at` |
| manifest JOIN 性能 | 频繁 JOIN `department_types` 查询 manifest | 缓存层（Phase-5+ 评估） |

### 3. 安全风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| 跨租户引用 | tenant_private 部门模板引用其他租户的 private 员工模板 | 引用校验：仅允许 official + 本租户 private |
| 治理规则注入 | `governance_rules_json` 含恶意规则 | 字段形状校验 + Admin 审查（marketplace 提交前） |
| manifest 篡改 | `department_types.manifest_json` 被越权修改 | `is_system=1` 类型仅 Admin 可改 + 审计事件 |

---

## 开放问题（待 ADR 决策）

### Q1: `sop_flow_json` 引入时机

- 选项 A：Phase-4 S2 引入（与 tenant_private CRUD 同步）
- 选项 B：Phase-5+ 引入（与 WorkflowStep 同步）

建议：选项 B，Phase-4 不引入 `sop_flow_json`，避免与 WorkflowStep 设计耦合。Phase-4 部门模板仅承载员工组合 + 类型 + 描述，SOP 推迟到 Phase-5+。

### Q2: `default_process` 默认值

- 选项 A：硬编码 `sequential` 为默认值
- 选项 B：从 `department_types.manifest_json.allowed_workflow_patterns` 取第一个

建议：选项 A，Phase-4 硬编码 `sequential`。Phase-5+ 评估选项 B 的动态读取。

### Q3: 部门模板是否承载 `default_capability_types_json`

员工模板已有 `default_capability_types_json`，部门模板是否需要部门级聚合？

- 选项 A：部门模板不承载，仅员工模板有
- 选项 B：部门模板承载 `default_capability_types_json` 作为部门级聚合

建议：选项 A，避免冗余。部门级能力类型可通过聚合 `default_employee_templates_json` 中所有员工的 `default_capability_types_json` 派生。

### Q4: 部门模板与公司模板的引用时机

Phase-5+ CompanyTemplate 引入时，`default_department_templates` 字段如何引用？

- 选项 A：直接引用 `department_templates.id`（强引用）
- 选项 B：引用 `department_templates.id` + `version`（弱引用，允许版本漂移）

建议：选项 A，强引用。Phase-5 简化治理，版本兼容性问题推迟到 Phase-7+。

### Q5: 是否允许「无部门类型」的部门模板

`department_type` 字段是否可空？

- 选项 A：必填，所有部门模板须归属某个 `department_type`
- 选项 B：可空，允许「自由模板」无类型归属

建议：选项 A，必填。保证双层关系完整性，避免「孤儿模板」。

---

## 结论

### 1. 核心结论

1. **部门模板定义配置蓝图，部门类型定义类别，部门实例是蓝图的具体化**。
2. **双层关系须文档化**（C2）：`department_types`（类型注册表，已解禁）vs `department_templates`（模板治理层，source 三态），独立表优于加列。
3. **manifest_json 归 type 层**：`manifest_json` 由 `department_types` 承载，`department_templates` 不重复。
4. **字段设计采纳 MetaGPT + ChatDev**：`default_employee_templates_json` + `sop_flow_json`（Phase-4 预留）+ `governance_rules_json`（Phase-4 预留）。
5. **首个 official 实例**：通用研发部（含 6 员工引用）。
6. **走独立 catalog**，不扩展 `CAPABILITY_TYPE`，不复用 `official_models`/`tenant_private_capabilities` 表。
7. **三态治理一致**：official / tenant_private / marketplace，与 capability / employee_template / company_template 模式完全对齐。

### 2. Phase-4 实现边界

- **实现**：S1 只读 official + S2 tenant_private CRUD + S3 Admin 管理 + S4 capability 绑定（metadata only）
- **预留**：`sop_flow_json` / `default_workflow_template_id` / `default_process` / `governance_rules_json` / `default_capability_pack_refs` / `version`
- **永不实现**：直接执行任务、持久化凭证、触发 prompt 注入、扩展 CAPABILITY_TYPE、破坏 department_types DDL 契约

### 3. 一句话总结

**部门模板是 Curis AI 公司的配置蓝图层，与 `department_types`（类型注册表）形成双层关系（C2 条件须文档化），Phase-4 优先实现 S1-S4（metadata CRUD + capability 绑定）；字段设计采纳 MetaGPT SOP + ChatDev ChatChain 转化为 `sop_flow_json` / `governance_rules_json`（Phase-4 预留），首个 official 实例为通用研发部（含 6 员工引用）；走独立 catalog 不扩展 CAPABILITY_TYPE，manifest_json 归 type 层不重复，三态治理与下层 capability / employee_template 完全一致。**
