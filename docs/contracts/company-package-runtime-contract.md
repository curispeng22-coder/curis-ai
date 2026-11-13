# Company Package Runtime Contract（公司包运行时契约 · 资产组合 Bundle）

> **作者**：高见远（架构师，software-architect）
> **主理人**：齐活林（交付总监）
> **阶段**：Phase-1B Template Runtime Integration Gate（Admin 侧）—— 纯文档（design-only reservation），零代码
> **继承**：在 `docs/contracts/company-package-contract.md`（Company Package 升级契约）基础上，定义 **Admin 对外输出的运行时契约形状**（指向 6 类模板运行时对象的 id 组合）
> **对齐**：ADR-0017；复用 `capability-package-commercial-contract.md` 商业信封；与 `template-catalog-runtime-contract.md`（本文引用的 6 类 `template_id` 即其输出键）一致
> **范围说明**：Company Package 是 **资产组合（asset bundle）**，不是运行实例（not a runtime instance）。本契约描述 Admin 如何把"一组官方模板 id"打包成一个可选择的单元对外输出。

---

## 0. 文档定位与引用

- 本契约是 Company Package 在 **运行时集成层（Admin 对外输出）** 的形状定义。
- 它**继承并升级** `company-package-contract.md`：复用其商业信封（`pricing_reference` / `quota_reference` / `availability` / `status`），并把"模板引用"表达为 6 类模板运行时对象的 id 组合。
- Company Package 仅为目录定义；**不触发** EmployeeInstance / DepartmentInstance / 公司激活 / 计费事件。

---

## 1. 与 company-package-contract.md 的继承 / 差异

| 维度 | `company-package-contract.md`（商业产品单元视角） | 本运行时契约（资产组合输出视角） |
|---|---|---|
| 定位 | Admin 可配置的商业产品单元（含 SkillPackage/ToolPackage 子包） | Admin 对外输出的"模板组合包"（指向 6 类 TemplateCatalogEntry） |
| 公司模板引用 | `company_template_ref`（`ct_`） | `company_template_id`（同 `ct_`，键名统一为 `_id`） |
| 部门/员工引用 | `department_template_refs` / `employee_template_refs`（`dt_`/`et_` 数组） | `department_template_ids` / `employee_template_ids`（键名统一为 `_ids`） |
| 工作流引用 | 经 `capability_ids`/`workflow_template_ids`（CapabilityPackage 继承） | **新增** `workflow_template_ids`（`wt_` 数组，显式平铺） |
| 技能引用 | 经 `skill_package_refs`（`sp_` 子包） | **新增** `skill_template_ids`（`st_` 数组，直接指向 SkillTemplateEntry） |
| 工具引用 | 经 `tool_package_refs`（`tp_` 子包） | **新增** `tool_template_ids`（`tt_` 数组，直接指向 ToolTemplateEntry） |
| 商业信封 | `pricing_reference`/`quota_reference`/`availability`/`status` | **原样复用**（不重定义） |
| 能力真相源 | `SkillPackage.capability_ids`/`ToolPackage.capability_ids` 指向 `official_models` | 一致：Skill/Tool 仍经 `capability_ref` 指向官方能力目录 |

> **差异本质**：`company-package-contract.md` 站在"商业产品单元 + 能力子包"视角（技能/工具经 `SkillPackage`/`ToolPackage` 聚合）；本运行时契约站在"Admin 对外输出模板组合"视角，把 6 类模板**平铺为直接 id 引用**，便于 Workspace 一次性选择整包。两者**不冲突**：运行时契约是产品单元契约的"模板组合视图"。落库时二选一或并存由后续 gate 决定（本契约 design-only）。

---

## 2. CompanyPackageRuntime JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CompanyPackageRuntime",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "company_package_id","name","version","status","availability",
    "company_template_id","department_template_ids","employee_template_ids",
    "workflow_template_ids","skill_template_ids","tool_template_ids"
  ],
  "properties": {
    "company_package_id":       { "type": "string", "pattern": "^ccp_[a-z0-9_-]+$" },
    "name":                     { "type": "string" },
    "description":              { "type": "string", "default": "" },
    "version":                  { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "default": "1.0.0" },
    "status":                   { "type": "string", "enum": ["draft","active","disabled"], "default": "draft" },
    "availability":             { "type": "string", "enum": ["public","tenant_invite_only","enterprise_only"], "default": "public" },
    "pricing_reference":        { "type": ["string","null"], "description": "复用 CapabilityPackage：指向 plan_id" },
    "quota_reference":          { "type": ["string","null"], "description": "复用 CapabilityPackage：指向 plan_id" },
    "company_template_id":      { "type": ["string","null"], "pattern": "^ct_[a-z0-9_-]+$", "description": "引用 CompanyTemplateEntry.template_id" },
    "department_template_ids":  { "type": "array", "items": { "type": "string", "pattern": "^dt_[a-z0-9_-]+$" }, "default": [] },
    "employee_template_ids":    { "type": "array", "items": { "type": "string", "pattern": "^et_[a-z0-9_-]+$" }, "default": [] },
    "workflow_template_ids":    { "type": "array", "items": { "type": "string", "pattern": "^wt_[a-z0-9_-]+$" }, "default": [] },
    "skill_template_ids":       { "type": "array", "items": { "type": "string", "pattern": "^st_[a-z0-9_-]+$" }, "default": [] },
    "tool_template_ids":        { "type": "array", "items": { "type": "string", "pattern": "^tt_[a-z0-9_-]+$" }, "default": [] },
    "created_at":               { "type": "string", "format": "date-time" },
    "updated_at":               { "type": "string", "format": "date-time" }
  },
  "examples": [{
    "company_package_id": "ccp_ai_software_company",
    "name": "AI Software Company 套装",
    "description": "标准 AI 软件公司官方资产套装：研发部 + 6 类研发员工 + 研发 SOP + 后端编码技能 + 代码执行工具。",
    "version": "1.0.0",
    "status": "active",
    "availability": "public",
    "pricing_reference": "plan_pro",
    "quota_reference": "plan_pro",
    "company_template_id": "ct_ai_software_company",
    "department_template_ids": ["dt_engineering"],
    "employee_template_ids": ["et_backend_engineer","et_frontend_engineer","et_architect","et_tech_lead","et_product_manager","et_qa_engineer"],
    "workflow_template_ids": ["wt_software_rnd_sop"],
    "skill_template_ids": ["st_backend_coding"],
    "tool_template_ids": ["tt_code_executor"]
  }]
}
```

> 字段对齐：商业信封 **原样复用** `capability-package-commercial-contract.md` §2（`pricing_reference`/`quota_reference`/`availability`/`status`）；6 类 `template_id(s)` 引用 `template-catalog-runtime-contract.md` 的输出键。

---

## 3. 组装规则（Assembly Rules）

| # | 规则 | 说明 |
|---|------|------|
| **R1** | **商业信封复用** | `pricing_reference`/`quota_reference`/`availability`/`status` 与 CapabilityPackage **完全一致**，指向 `plan_id` 派生价格/配额；不新增计费逻辑。 |
| **R2** | **引用 6 类模板运行时对象** | 所有 `*_template_id(s)` 必须指向 `template-catalog-runtime-contract.md` 定义的 `TemplateCatalogEntry.template_id`（即 `ct_/dt_/et_/wt_/st_/tt_*`）。 |
| **R3** | **引用完整性（配置时校验，运行时不强制 FK）** | Admin 配置时由应用层校验 ID 格式与存在性；允许"先发布包、后补模板"。 |
| **R4** | **单一能力真相源** | `skill_template_ids`/`tool_template_ids` 经 `ToolTemplateEntry.metadata.capability_ref` / `SkillTemplateEntry.metadata.capability_ref` 最终指向 `official_models`；不内联能力定义、不重复注册。 |
| **R5** | **版本独立演进** | `CompanyPackageRuntime.version`（SemVer）独立于各组件模板的 `TemplateCatalogEntry.version`；组件升级不强制本包升级（快照隔离见 `template-versioning-policy.md`）。 |
| **R6** | **来源权威** | `official` Company Package 仅平台 Admin 可写；`marketplace` 须 G3 双签 + 安全 gate。 |
| **R7** | **资产组合而非实例** | Company Package 是**资产组合（bundle）**，仅为目录定义；**不持有**任何运行态（无 EmployeeInstance / DepartmentInstance / 公司激活）。 |
| **R8** | **无实例化动作** | 本包仅描述"包含哪些模板 id"；实例化须经后续 gate，由 Workspace 按 `template_id` 拉取+快照产生实例（见 `admin-workspace-template-boundary.md`）。 |

---

## 4. 与商业信封关系

```
CompanyPackageRuntime
  ├── pricing_reference ──▶ plan_id ──▶ pricing_rules(plan_id)   [价格权威，复用 CapabilityPackage]
  ├── quota_reference   ──▶ plan_id ──▶ quota_rules(plan_id)     [配额权威，复用 CapabilityPackage]
  ├── company_template_id      ──▶ CompanyTemplateEntry.template_id
  ├── department_template_ids  ──▶ DepartmentTemplateEntry.template_id[]
  ├── employee_template_ids   ──▶ EmployeeTemplateEntry.template_id[]
  ├── workflow_template_ids   ──▶ WorkflowTemplateEntry.template_id[]
  ├── skill_template_ids      ──▶ SkillTemplateEntry.template_id[]
  └── tool_template_ids       ──▶ ToolTemplateEntry.template_id[]
```

> Company Package **不持有价格/配额数值**，仅持有"指向哪个 plan"的引用；**也不持有模板全量数据**，仅持有 `template_id` 引用。完整模板形状由 Workspace 经 catalog 按 id 拉取（见 `template-catalog-runtime-contract.md`）。

---

## 5. 与 company-package-contract.md 字段对照

| 本运行时契约字段 | company-package-contract.md 字段 | 差异 |
|---|---|---|
| `company_package_id` | `company_package_id`（`ccp_`） | ✅ 一致 |
| `company_template_id` | `company_template_ref` | 键名 `_id` 化 |
| `department_template_ids` | `department_template_refs` | 键名 `_ids` 化 |
| `employee_template_ids` | `employee_template_refs` | 键名 `_ids` 化 |
| `workflow_template_ids` | （经 CapabilityPackage 继承字段） | **新增显式平铺** |
| `skill_template_ids` | `skill_package_refs`（`sp_`） | **改为直接 `st_` 引用** |
| `tool_template_ids` | `tool_package_refs`（`tp_`） | **改为直接 `tt_` 引用** |
| `pricing_reference`/`quota_reference`/`availability`/`status` | 同 | ✅ 原样复用 |

---

## 6. 红线与禁止区（本契约遵守）

- **不开发** Payment / Invoice / BillingEvent / 自动扣款 / Marketplace 交易 / Promotion。
- **不写** 任何后端代码、不建表、不加 API 路由、不碰 Workspace 执行链 / Credential Vault / EmployeeRuntime / Usage Event 写入。
- **不实例化**：Company Package 仅为官方资产组合目录；不触发任何租户安装、员工创建、公司激活或计费动作。
- **能力不重复**：Skill/Tool 仅经 `capability_ref` 指向官方能力目录，不新建能力实体。

---

## 7. 验收映射

| # | 验收项 | 落点 |
|---|--------|------|
| 1 | Company Package 运行时契约（6 类模板 id 组合） | 本文 |
| 2 | 继承并复用商业信封 | §1 / §2 / §4 |
| 3 | 与 company-package-contract.md 继承/差异说明 | §1 / §5 |
| 4 | 组装规则（引用完整性/单一真相源/无实例化） | §3 |
| 5 | 红线遵守 | §6 |

*—— Company Package Runtime Contract（纯设计/契约，零代码）。继承并升级 Company Package 契约；与 ADR-0017 一致。*
