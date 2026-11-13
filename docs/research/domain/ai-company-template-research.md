# AI 公司模板（Company Template）领域研究

> 研究范围：Curis Admin Platform 的 AI 公司模板（CompanyTemplate）应解决什么问题、字段设计、official / tenant_private / marketplace 三态边界、是否适合作为 marketplace 商品（Company Pack）、与部门模板 / 员工模板的层级关系、Phase-4 实现边界与预留策略。
>
> 研究性质：纯研究文档，不含实现方案、不含代码改动。所有结论须与 ADR-0028 共享契约、issue 087 Phase-3.5 决策、capability-catalog-research 决策对齐。
>
> 关键约束：issue 087 §6.2 (C5) 已决定 `CAPABILITY_TYPE` 保持 `["model","tool","connector"]` 不变，template 走独立 catalog 体系。CompanyTemplate 属于 template 体系的最上层，不应纳入 `official_models` 表，亦不应扩展 `CAPABILITY_TYPE`。

---

## 问题定义

### 1. AI 公司模板在 Curis 中解决什么问题

Curis 的最终产品目标是商业化多租户 AI 公司系统（ADR-0028 §1）：一个租户 = 一个 AI 公司，CEO 在其租户内构建部门、雇佣员工、绑定能力、执行任务。然而仅靠「部门模板 + 员工模板」两层不足以表达一个**可复用的完整业务蓝图**——CEO 在新租户冷启动时仍需手动挑选部门组合、配置员工、绑定能力、设定治理规则，启动成本高且一致性差。

AI 公司模板（CompanyTemplate）解决的核心问题是：

1. **冷启动成本**：新租户开箱即用，从「官方公司蓝图」一键派生出研发公司、内容公司、投资公司等完整结构。
2. **跨租户一致性**：同行业租户共享同一官方公司模板派生，保证 SOP、治理、能力组合的基线一致。
3. **市场化为商品**：将「一套部门 + 一套员工 + 一套能力绑定 + 一套治理」打包为 Company Pack，作为 marketplace 上的可订阅商品。
4. **治理层级清晰**：CompanyTemplate → DepartmentTemplate[] → EmployeeTemplate[] → CapabilityBinding[] → capability，自上而下引用。

简言之：**部门模板定义团队形状，员工模板定义角色行为，公司模板定义完整业务蓝图**。

### 2. 为什么 Phase-4 仅预留而不实现

issue 087 §8.2 明确 Phase-4 须先解锁 5 项 gate（C1-C5），切片顺序 S1→S5。CompanyTemplate 是最上层模板，依赖下层 DepartmentTemplate / EmployeeTemplate CRUD 已稳定：
- Phase-4 S1-S4 仅实现 employee / department template
- Phase-4 仅**预留** CompanyTemplate 表结构与契约（schema-only）
- Phase-5+ 视下层稳定后引入
- marketplace Company Pack 须待 G3 gate 解锁

---

## 现状分析

### 1. Curis 当前架构

- **Tenant / CEO / Company**（ADR-0028 §1）：Tenant 是隔离边界；CEO 是操作者（`ceo_id` 不透明令牌）；Company 是逻辑实体，与 Tenant 1:1，当前用 `tenants.company_name` + 派生 `company_id=tenant_id` 表达，不单独立表。
- **已有 template 表**：`database.py:442-496` 已新增 `employee_templates`/`department_templates`/`employee_instances`/`employee_capability_bindings` 四张表。**未创建** `company_templates` 表，符合 Phase-3.5 契约评审结论。
- **capability_source 三态**：ADR-0028 §2 定义 official/tenant_private/marketplace 三态，适用于所有能力/模板。

### 2. 已有决策锚点

- **issue 087 §6.2 (C5)**：`CAPABILITY_TYPE` 保持不变，CompanyTemplate 走独立 catalog。
- **capability-catalog-research §2.4**：`company_templates` 表 Phase-5+ 引入，走独立 catalog 模式。
- **ADR-0028 §0.2**：Phase-1 不做一 CEO 多公司。

---

## 竞品参考

### 1. Paperclip Companies

Paperclip Companies 是「ready-to-deploy agent companies」目录，将 AI 公司作为可导入的包（组织架构、技能、治理、代理、领域配置）。典型包包括工程公司、安全公司、游戏工作室、研究实验室。

可借鉴：公司作为可导入包（CompanyTemplate 作为可派生蓝图）；领域特定分类；组织架构 + 代理 + 技能 + 治理一体化。不可借鉴：庞大代理库、一键外部导入（须 Admin 审核）、可执行任意代码的 skill-loaded pack。

### 2. MetaGPT 软件公司模板

MetaGPT 核心哲学 `Code = SOP(Team)`，内置完整软件公司模板：5 核心角色 + 标准 SOP。可作为 official CompanyTemplate 首个实例。不可借鉴：一句话生成完整仓库、CLI-centric、角色直接持有 `api_key`、重型 SOPChain 引擎。

### 3. ChatDev 虚拟软件公司

ChatDev 1.0 是 Virtual Software Company，7 角色 + ChatChain 瀑布流程。可借鉴：完整公司配置可目录化。不可借鉴：CEO/CTO/CPO 高管头衔。

### 4. AWS Service Catalog Portfolio 模式

Portfolio + Product 双层结构对应 CompanyTemplate（Portfolio 层）。OpenAI GPT Store 的 `visibility: private / link / public` 对应 Curis 三态。

---

## 字段设计建议

### 1. CompanyTemplate 字段表

| 字段 | 类型 | 必填 | 来源 | 阶段 | 边界 |
| --- | --- | --- | --- | --- | --- |
| `id` | text PK | ✅ | 创建方 | Phase-5 预留 | 命名空间：`official.*` / `tenant:<tid>:*` / `marketplace:*` |
| `name` | text | ✅ | 创建方 | Phase-5 预留 | 公司模板展示名 |
| `description` | text | ✅ | 创建方 | Phase-5 预留 | 模板用途说明 |
| `company_type` | text | ✅ | 创建方 | Phase-5 预留 | 如 `software_rd` / `content_ops` |
| `industry` | text | ❌ | 创建方 | Phase-5 预留 | 行业标签 |
| `default_department_templates` | text (JSON) | ✅ | 创建方 | Phase-5 预留 | 引用 `department_templates.id` |
| `default_employee_templates` | text (JSON) | ❌ | 创建方 | Phase-5 预留 | 跨部门浮动员工引用 |
| `default_capability_pack_refs` | text (JSON) | ❌ | 创建方 | Phase-5+ 预留 | 引用 `capability_packs.id` |
| `default_governance_policy_ref` | text | ❌ | 创建方 | Phase-5+ 预留 | 引用 `platform_policies` |
| `default_model_policy_json` | text (JSON) | ❌ | 创建方 | Phase-5 预留 | 公司级默认模型策略 |
| `governance_rules_json` | text (JSON) | ❌ | 创建方 | Phase-5+ 预留 | 公司级治理规则 |
| `budget_limits_json` | text (JSON) | ❌ | 创建方 | Phase-5+ 预留 | **仅形状，金额计算待 G1 gate** |
| `source` | text (enum) | ✅ | 创建方 | Phase-5 预留 | CHECK 三态 |
| `tenant_id` | text | ✅ | 系统 | Phase-5 预留 | official='platform'，private=实际租户 |
| `version` | text | ✅ | 创建方 | Phase-5 预留 | 语义化版本 |
| `schema_version` | text | ✅ | 系统 | Phase-5 预留 | ADR-0028 §0.1 元约定 |
| `enabled` | integer | ✅ | 创建方 | Phase-5 预留 | 1/0 |
| `created_at` | datetime | ✅ | 系统 | Phase-5 预留 | ISO8601 UTC |
| `updated_at` | datetime | ❌ | 系统 | Phase-5 预留 | ISO8601 UTC |

### 2. 字段设计理由

- **`default_department_templates` vs `default_employee_templates`**：部门模板已含员工引用，公司模板仅需引用部门即可派生。保留公司级 `default_employee_templates` 作为冗余便利（跨部门浮动员工 + 简化全员清单查询）。
- **`governance_rules_json` vs `default_governance_policy_ref`**：前者自定义规则，后者引用官方策略。两者并存。
- **`budget_limits_json` 禁止区边界**：仅定义形状，不计算金额。金额计算落入 G1 禁止区。
- **命名空间**：遵循 ADR-0028 tenant_private 命名空间规则，禁止越权前缀。

### 3. 引用关系

```text
CompanyTemplate
  └── default_department_templates  → department_templates.id
        └── default_employee_templates_json  → employee_templates.id
              └── default_capability_types_json  → CAPABILITY_TYPE
                    └── employee_capability_bindings  → capability_id
  └── default_employee_templates  → employee_templates.id（跨部门浮动员工）
  └── default_capability_pack_refs  → capability_packs.id（Phase-5+）
  └── default_governance_policy_ref  → platform_policies
```

引用方向**严格自上而下**，禁止反向引用。

---

## 治理边界

### Admin 管理（official / marketplace）

#### 1. Official Company Template

- Admin 经 `/api/platform/company-templates` 写通道，`source='official'`，`tenant_id='platform'`
- 全局可见，所有租户经 `/api/catalog/company-templates` 只读
- 审计事件：`company_template.created` / `company_template.status_changed`

#### 2. Marketplace Company Template（Company Pack）

- CEO 提交 tenant_private → Admin 经 `/api/platform/marketplace-review` 审核 → approve 后提升为 `source='marketplace'` + `tenant_id='platform'`
- 跨租户共享触发 G3 gate，须总控决策席 + 安全边界席双签
- marketplace 公司模板即「Company Pack」或「Business Pack」

#### 3. Admin 可见性

- Admin 可见所有 official / marketplace 公司模板（完整字段）
- Admin 可见 tenant_private 公司模板的元数据（`id`/`name`/`source`/`tenant_id`/`enabled`/`created_at`）
- Admin **不可见** tenant_private 公司模板的业务配置

### Workspace 管理（tenant_private）

- CEO 经 `/api/tenant/company-templates` 内部写通道，`source='tenant_private'`
- CEO 可基于 official 模板派生 tenant_private 模板
- CEO 可从零创建 tenant_private 模板
- CEO 可提交至 marketplace 审核
- CEO **不可**修改 official 模板，**不可**跨租户共享

### 禁止区

- **ADR-0017**：CompanyTemplate 属模板定义层（metadata），可解禁。公司实例创建/执行仍锁定。
- **ADR-0028 §9 gate**：G1（`budget_limits_json` 金额计算）、G3（marketplace Company Pack 跨租户共享）、G5（LOCKED_ACTIONS）。
- **不变式**：不持久化凭证、不触发任务路由/prompt 注入、不被 `Orchestrator`/`ToolRouter`/`AIEmployee` 直接引用、不扩展 `CAPABILITY_TYPE`、不复用 `official_models`/`tenant_private_capabilities` 表。

---

## 前置条件

### 1. Phase-5 引入 CompanyTemplate 前置

- EmployeeTemplate / DepartmentTemplate CRUD 已稳定（Phase-4 S1-S4 完成）
- Template-Capability 绑定已实现（Phase-4 S4 完成）
- `company_templates` 表结构设计 + 独立 ADR
- `CompanyTemplateCatalog` 服务设计
- ADR-0017 禁止区部分解禁（CompanyTemplate 层）

### 2. Marketplace Company Pack 前置

- G3 gate 解锁（跨租户 marketplace，双签）
- marketplace 审核流程上线
- Company Pack 供应链检查
- 跨租户计量与收益分成

### 3. Company Pack 导入/导出前置

- 平台无关 JSON schema + 导入审核流程 + 版本兼容性策略

---

## Phase-4 建议

### 1. Phase-4 仅预留（不实现）

Phase-4 不实现 CompanyTemplate 的任何 API 或服务，仅预留表结构设计与契约文档。

### 2. Phase-4 实现的下层依赖

| 切片 | 内容 | 为 CompanyTemplate 铺路 |
| --- | --- | --- |
| S1 | 只读 official employee/department template | 验证 template catalog 读通道 |
| S2 | tenant_private template CRUD | 验证 tenant_private 治理 |
| S3 | Admin official template 管理 API | 验证 Admin 写通道 |
| S4 | Template-Capability 绑定 | 验证引用关系 |
| S5 | Marketplace template 审核（gate 后） | 为 Company Pack 审核铺路 |

### 3. Phase-5+ 建议

| 阶段 | 内容 | 优先级 |
| --- | --- | --- |
| Phase-5 S1 | `company_templates` 表 + `CompanyTemplateCatalog` 服务 | P1 |
| Phase-5 S2 | Admin official CompanyTemplate CRUD | P1 |
| Phase-5 S3 | Workspace tenant_private CompanyTemplate CRUD | P1 |
| Phase-5 S4 | 公司模板「应用」API | P2 |
| Phase-5 S5 | Marketplace Company Pack 审核（待 G3 gate） | P2 |
| Phase-6+ | Company Pack 导入/导出 | P3 |

### 4. 永不实现

公司模板直接执行任务、持久化凭证、触发 prompt 注入、一键外部导入到运行中 Workspace、可执行任意代码的 skill-loaded pack。

---

## 首个 Official CompanyTemplate 实例建议

基于 MetaGPT 软件公司模板，Phase-5 首个 official CompanyTemplate 应为：

```text
CompanyTemplate: official.company.software_rd
  name: "软件研发公司"
  company_type: software_rd
  industry: technology
  default_department_templates:
    - official.department.business_general
  default_employee_templates:
    - official.employee.tech_lead
    - official.employee.product_manager
    - official.employee.architect
    - official.employee.frontend_engineer
    - official.employee.backend_engineer
    - official.employee.qa_engineer
  default_governance_policy_ref: platform.standard_rd_governance
  default_model_policy_json: {"mode": "tenant_default"}
  source: official
  tenant_id: platform
  version: 0.1.0
```

---

## Company Pack 未来形态

参考 Paperclip Companies 包结构，Curis 未来 Company Pack 导出形态：

```text
company.json          # CompanyTemplate 元数据
departments.json      # DepartmentTemplate[] 数组
employees.json        # EmployeeTemplate[] 数组
capabilities.json     # capability_refs 引用清单
governance.json       # governance_rules + policy_ref
README.md             # 包说明
```

导出/导入须经脱敏 → Admin 审核（供应链检查、内容审核、schema 校验）→ 发布为 marketplace Company Pack。Phase-4/5 仅预留此形态。

### 1. Company Pack 与 Role Pack / Department Pack 的差异

| Pack 类型 | 对应模板 | 包含内容 | 跨租户共享 gate | Phase |
| --- | --- | --- | --- | --- |
| Role Pack | EmployeeTemplate | 单个角色定义 + 推荐能力类型 | G3 | Phase-4 S5+ |
| Department Pack | DepartmentTemplate | 部门配置 + 员工引用 + SOP | G3 | Phase-4 S5+ |
| **Company Pack** | **CompanyTemplate** | **公司蓝图 + 部门 + 员工 + 能力 + 治理** | **G3 + 总控决策席双签** | **Phase-5+ S5** |

Company Pack 是最高阶的商品形态，包内容最丰富，治理最严格。Phase-4 不实现任何 Pack 审核，仅预留契约。

### 2. 跨租户派生链路

```text
[Admin] official.company.software_rd
   ↓ CEO 派生（Phase-5 S3）
[Workspace:tenant_A] tenant:tenant_A:company.my_software_co
   ↓ CEO 提交至 marketplace（Phase-5 S5）
[Admin review queue] tenant:tenant_A:company.my_software_co（pending）
   ↓ Admin approve + G3 gate
[marketplace] marketplace:company.agile_rd_pack_v2
   ↓ 其他租户订阅（Phase-6+）
[Workspace:tenant_B] tenant:tenant_B:company.derived_agile_rd（基于 marketplace 派生）
```

每个箭头都对应明确的 API 端点与审计事件。Phase-4 仅实现链路最底层（official 只读 + tenant_private CRUD），上层链路待 Phase-5+。

---

## 审计事件目录

CompanyTemplate 治理涉及的全量审计事件：

| 事件 key | 触发方 | 触发时机 | Phase |
| --- | --- | --- | --- |
| `company_template.created` | Admin | 创建 official 模板 | Phase-5 S2 |
| `company_template.updated` | Admin | 修改 official 模板字段 | Phase-5 S2 |
| `company_template.status_changed` | Admin | 启停 official 模板 | Phase-5 S2 |
| `company_template.tenant_created` | CEO | 创建 tenant_private 模板 | Phase-5 S3 |
| `company_template.tenant_updated` | CEO | 修改 tenant_private 模板 | Phase-5 S3 |
| `company_template.tenant_derived` | CEO | 基于 official 派生 tenant_private | Phase-5 S3 |
| `company_template.marketplace_submitted` | CEO | 提交至 marketplace 审核 | Phase-5 S5 |
| `company_template.marketplace_approved` | Admin | 审核通过，提升为 marketplace | Phase-5 S5 |
| `company_template.marketplace_rejected` | Admin | 审核拒绝 | Phase-5 S5 |
| `company_template.applied` | CEO | 应用模板创建/更新公司实例 | Phase-6+（待 Instance gate） |

审计事件须写入 `audit_events` 表（ADR-0028 §4），包含 `actor_id`/`actor_role`/`action`/`resource_type`/`resource_id`/`tenant_id`/`metadata_json`/`created_at`。

---

## 风险分析

### 1. 设计风险

| 风险 | 描述 | 影响 | 缓解 |
| --- | --- | --- | --- |
| 字段膨胀 | CompanyTemplate 字段过多（17+） | Admin 维护负担 | Phase-5 仅实现核心 7 字段，其余 Phase-5+/6+ 渐进 |
| 引用断裂 | 部门/员工模板删除后公司模板引用失效 | 派生失败 | 软删除策略 + 引用完整性 CHECK + 删除前依赖检查 |
| 三态混淆 | tenant_private 误标记为 official | 跨租户泄露 | `source` CHECK 约束 + 创建方权限校验 + Admin 操作门控 |
| 治理规则泄露 | `governance_rules_json` 含敏感策略 | 跨租户暴露 | marketplace 提交前脱敏 + Admin 审核内容检查 |

### 2. 实现风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| Phase-4 过度设计 | 在 Phase-4 实现 CompanyTemplate API | 严格切片顺序，Phase-4 仅 schema 预留 |
| 依赖未就绪 | Phase-5 S1 时 DepartmentTemplate CRUD 未稳定 | Phase-4 S1-S4 完成后再启动 Phase-5 |
| marketplace 滥用 | 低质量 Company Pack 充斥市场 | 审核流程 + 评分机制 + 下架机制（Phase-6+） |

### 3. 商业风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| Pack 同质化 | 大量相似 Company Pack | 分类标签 + 推荐机制（Phase-6+） |
| 供应链攻击 | Pack 内嵌恶意 prompt 注入 | 供应链检查 + 内容审核 + sandbox 试用 |
| 收益分成争议 | Pack 作者与平台分成比例 | Phase-6+ 制定收益分成政策，需独立 ADR |

---

## 与 Capability Catalog 的对比

CompanyTemplate 与 Capability 走相同的「独立 catalog + 三态治理」模式，但有关键差异：

| 维度 | Capability | CompanyTemplate |
| --- | --- | --- |
| 表 | `official_models` / `tenant_private_capabilities` | `company_templates`（独立表） |
| 类型枚举 | `CAPABILITY_TYPE` = model/tool/connector | 无类型枚举（公司模板不分类） |
| 调用方式 | 直接被 `Orchestrator`/`ToolRouter` 引用执行 | 仅作为元数据被 CEO 派生，不直接执行 |
| 禁止区 | 部分能力属 LOCKED_ACTIONS | 全部属 metadata，可解禁 |
| marketplace 形态 | 单个能力商品 | Company Pack（包含多模板） |
| Phase-4 | S1-S4 已实现 | 仅 schema 预留 |

关键不变式：**CompanyTemplate 永不被运行时直接引用**，与 Capability 的本质差异。Capability 是执行单元，CompanyTemplate 是配置蓝图。

---

## 开放问题（待 ADR 决策）

### Q1: 一 CEO 多公司支持时机

ADR-0028 §0.2 明确 Phase-1 不做一 CEO 多公司。Phase-5+ 是否引入？

- 选项 A：保持 1:1（tenant ↔ company），CompanyTemplate 仅作为「公司配置模板」用于冷启动
- 选项 B：1:N（一个 tenant 可有多个 company），CompanyTemplate 用于创建多个子公司

建议：Phase-5/6 保持 1:1，Phase-7+ 视业务需求评估。本研究的字段设计兼容两种选项（`tenant_id` 字段不变）。

### Q2: Company Pack 与 Department Pack 是否可独立销售

- 选项 A：仅 Company Pack 可作为 marketplace 商品，Department Pack 不可独立销售（须打包进 Company Pack）
- 选项 B：Company Pack / Department Pack / Role Pack 均可独立销售

建议：选项 B，与 issue 087 三层模板独立 catalog 决策一致。但 Company Pack 享受更高分成（鼓励完整解决方案）。

### Q3: CompanyTemplate 是否承载 budget_limits_json

`budget_limits_json` 仅定义形状（如 `{"monthly_usd_limit": 1000}`），实际金额计算属 G1 禁止区。是否在 Phase-5 引入此字段？

- 选项 A：Phase-5 引入 `budget_limits_json`，仅形状不计算
- 选项 B：Phase-6+ 引入，待 G1 gate 解锁后一并设计

建议：选项 B，避免半成品字段。Phase-5 不引入 `budget_limits_json`，待 G1 gate 解锁后引入。

### Q4: 公司模板版本兼容性

公司模板 `version` 字段（语义化版本）如何与派生的 tenant_private 模板保持兼容？

- 选项 A：tenant_private 模板派生后不再跟随 official 更新
- 选项 B：tenant_private 模板可显式 rebase 到 official 新版本

建议：选项 A，简化治理。CEO 可手动基于新版本 official 重新派生。rebase 机制推迟到 Phase-7+ 评估。

### Q5: 行业标签（industry）的命名空间

`industry` 字段是自由文本还是受控词汇？

- 选项 A：自由文本（如 "technology" / "finance" / "healthcare"）
- 选项 B：受控词汇（Admin 维护的 `industry_catalog` 表）

建议：Phase-5 选项 A（自由文本），Phase-6+ 视分类需求评估选项 B。避免过早引入受控词汇表。

---

## Phase-4 S1-S4 详细验收标准（仅下层依赖）

虽然 Phase-4 不实现 CompanyTemplate，但下层 EmployeeTemplate / DepartmentTemplate 的 S1-S4 完成度直接影响 Phase-5 启动。CompanyTemplate 视角的验收标准：

### S1 验收

- [ ] `GET /api/catalog/employee-templates` 返回 official 列表
- [ ] `GET /api/catalog/department-templates` 返回 official 列表
- [ ] 6 个 official employee templates 预置
- [ ] 1 个 official department template 预置
- [ ] `updated_at` / `schema_version` 列已补齐

### S2 验收

- [ ] `POST /api/tenant/employee-templates` 创建 tenant_private 成功
- [ ] `POST /api/tenant/department-templates` 创建 tenant_private 成功
- [ ] 查询隔离生效（仅返回 official + 本租户 private）
- [ ] 命名空间校验生效（禁止 `official.*` 前缀）

### S3 验收

- [ ] `POST /api/platform/employee-templates` Admin 创建 official 成功
- [ ] `POST /api/platform/department-templates` Admin 创建 official 成功
- [ ] Admin 可见性边界生效（tenant_private 仅元数据可见）

### S4 验收

- [ ] `employee_capability_bindings` 表可填充（instance 仍锁定）
- [ ] 部门 → 员工 → 能力类型链路验证通过
- [ ] 引用完整性 CHECK 生效

S1-S4 全部通过后，Phase-5 S1 可启动 CompanyTemplate 表结构实现。

---

## 结论

### 1. 核心结论

1. **CompanyTemplate 是 template 体系的最上层**，解决「可复用完整业务蓝图」问题，是 Curis 商业化的天然商品载体（Company Pack）。
2. **Phase-4 仅预留**，Phase-5+ 视下层 template CRUD 稳定后引入。
3. **走独立 catalog**，不扩展 `CAPABILITY_TYPE`，不复用 `official_models`/`tenant_private_capabilities` 表。
4. **三态治理一致**：official / tenant_private / marketplace，与下层 template / capability 模式完全对齐。
5. **首个 official 实例**：软件研发公司（基于 MetaGPT 角色集 + Curis 改进）。

### 2. Phase-4 实现边界

- **实现**：无（仅 schema 预留 + 下层 dependency 实现）
- **预留**：`company_templates` 表 + `CompanyTemplateCatalog` 服务 + 全部 API
- **永不实现**：直接执行任务、持久化凭证、触发 prompt 注入、一键外部导入、可执行任意代码的 skill-loaded pack

### 3. 一句话总结

**CompanyTemplate 是 Curis template 体系的最上层蓝图，Phase-4 仅预留表结构与契约，Phase-5+ 引入独立 catalog 服务，marketplace Company Pack 待 G3 gate 解锁后落地；三态治理与下层 template / capability 完全一致，走独立 catalog 不扩展 CAPABILITY_TYPE，是 Curis 商业化的天然商品载体。**
