# Admin AI Company Asset Foundation · 发布与完成度评估

> **作者**：高见远（架构师，software-architect）
> **主理人**：齐活林（交付总监）
> **阶段**：AI Company Asset Factory Foundation —— 纯文档（design-only reservation）发布评估
> **对齐**：ADR-0017（仅做 design-only reservation：契约 + 占位，无行为变化、无后端改动）；承接 `docs/research/domain/admin-support-aicos-roadmap.md`（Admin 支撑 AI Company OS 评估，issue 087 C3 缺口）
> **日期**：2026-07-10

---

## 1. 发布概述

本期交付 **AI Company 官方资产基础（Template Catalog Contract）** 的**契约层（design-only）**，包含 3 份文档：

| 文档 | 性质 | 内容 |
|---|---|---|
| `docs/contracts/ai-company-template-system.md` | 契约（design-only） | 6 类官方模板目录总契约：公共基类型 `TemplateBase` + 各自 JSON Schema + 组合类图 + 命名对齐 |
| `docs/contracts/company-package-contract.md` | 契约（design-only） | Company Package 升级契约：继承并扩展 CapabilityPackage，组合 Company/Department/Employee 模板 + SkillPackage/ToolPackage |
| `docs/release/admin-ai-company-asset-foundation.md` | 发布评估 | 本文：完成度、红线核验、下一步 gate 建议 |

**核心结论**：本期把此前缺失的「官方业务模板作者能力」以**契约（design-only）**形式落地，作为未来实例化的基础。**零行为变化、零后端改动、零代码**——所有定义为 catalog 契约，非实例化数据。

---

## 2. 已实现（契约层）

| # | 交付物 | 状态 | 说明 |
|---|---|---|---|
| 1 | `TemplateBase` 公共基类型（version/status/source/description + 枚举） | ✅ 已定义 | 6 类模板统一继承 |
| 2 | CompanyTemplate 契约 | ✅ 已定义（Reserved） | 字段对齐 `company-template-contract.md`；无物理表（Phase-5+） |
| 3 | DepartmentTemplate 契约 | ✅ 已定义 | 字段对齐 `department_templates` 种子 + `department-template-contract.md` |
| 4 | EmployeeTemplate 契约 | ✅ 已定义 | 含任务要求字段 `role`/`department_type`/`default_skill`/`default_tool`/`persona`；对齐 `employee_templates` 种子 |
| 5 | SkillTemplate 契约 | ✅ 已定义（catalog-reference） | 对齐 `skill-runtime-contract.md`；引用官方能力目录 |
| 6 | ToolTemplate 契约 | ✅ 已定义（catalog-reference） | 对齐 `tool-runtime-contract.md`；引用 `capability_type=tool` |
| 7 | WorkflowTemplate 契约 | ✅ 已定义 | 对齐 `workflow_templates` 种子 + `workflow-template-contract.md` |
| 8 | Company Package 契约（CapabilityPackage 升级） | ✅ 已定义 | 继承 CapabilityPackage 商业信封 + 组合模板/Skill/Tool 子包 |
| 9 | 组合关系类图（Company→Department→Employee，Skill/Tool/Workflow 引用） | ✅ 已绘制 | Mermaid classDiagram |
| 10 | 命名对齐表（契约 vs 种子/专属契约 + 差异标注） | ✅ 已标注 | 见 `ai-company-template-system.md` §4 |

**既有可复用资产（本期未改，仅引用）**：
- 官方能力目录（`official_models` + `/api/platform/capabilities`，issue 071 已实现）——Skill/Tool 真相源。
- `CapabilityPackage`（已实现，`capability_packages` 表 + `/api/platform/capability-packages`）——Company Package 升级基线。
- `department_types` 类型注册表（Admin 经 `manage_department_types` 已可管理）。
- Employee/Department/Workflow 模板种子（`employee_templates` / `department_templates` / `workflow_templates` 表已落种子，Workspace 只读）。

---

## 3. 待实现（实例化 / 作者端点，issue 087 C3）

> 以下**均不在本期范围**，列为后续 gate 动作。

| # | 缺口 | 严重度 | 依赖 gate |
|---|---|---|---|
| 1 | `/api/platform/company-templates` 作者端点 | 阻塞（对完整 OS 蓝图） | `company_templates` 表设计（Phase-5+） |
| 2 | `/api/platform/department-templates` 作者端点 | 部分 | issue 087 C3（沿用 CapabilityCatalog 范式） |
| 3 | `/api/platform/employee-templates` 作者端点 | 部分 | **须 ADR-0017 员工 CRUD 禁止区部分解禁 gate**（总控决策席 + 安全边界席） |
| 4 | `/api/platform/workflow-templates` 作者端点 | 部分 | issue 087 C3（无引擎，仅目录） |
| 5 | `employee_templates` 表补 `updated_at` / `schema_version` | 轻微 | issue 087 §1.2 / §10 |
| 6 | `company_packages` 表 + `/api/platform/company-packages` | 阻塞（对 Company Package 实例化） | 依赖 #2/#3 + CapabilityPackage 已具备 |
| 7 | Skill/Tool 模板物理表 | **不需要** | 经 `/api/platform/capabilities` 统一目录供给 |

> **与 Phase-1 关系**（依据 `admin-support-aicos-roadmap.md` §D）：Company/Workflow 模板本就不在 Phase-1 范围；Department 类型注册表与 Employee 种子已足以支撑 Phase-1 最小实例化。本期契约为未来丰富官方供给奠定 catalog 基础，**不阻塞 Phase-1**。

---

## 4. 禁止区已遵守（红线核验）

| # | 红线 | 本期状态 |
|---|---|---|
| 1 | 不开发 Payment / Invoice / Billing / 自动扣款 | ✅ 遵守（无任何计费逻辑；pricing/quota 仅引用 plan_id） |
| 2 | 不开发 Marketplace 交易 / 分润 | ✅ 遵守（`marketplace` 源仅命名占位，无交易/上架执行） |
| 3 | 不执行 Promotion | ✅ 遵守（无 PromotionRule 实现） |
| 4 | 不写任何后端代码 / 不建表 / 不加 API 路由 | ✅ 遵守（纯 markdown 契约，零代码） |
| 5 | 不碰 Workspace 执行链 / Credential Vault / EmployeeRuntime / Usage Event 写入 | ✅ 遵守（仅为 catalog 定义，无实例化动作） |
| 6 | 模板为 design-only catalog 定义，非实例化数据 | ✅ 遵守（所有 `*-template` 仅为官方蓝图） |
| 7 | Skill/Tool 不重复定义能力（指向官方目录） | ✅ 遵守（catalog-reference 包装） |

**结论**：本期**严格位于 ADR-0017 design-only reservation 红区内**，未越界。

---

## 5. 下一步 gate 建议

| Gate | 目标 | 触发条件 / 决策席 | 依赖 |
|---|---|---|---|
| **Gate A：ADR-0017 员工 CRUD 禁止区部分解禁** | 允许 `employee_templates` 官方写（含 `updated_at`/`schema_version`） | 总控决策席 + 安全边界席 gate 解锁（issue 087 C1） | 无（先决） |
| **Gate B：`/api/platform/*-templates` 作者端点建设** | Department/Employee/Workflow 模板 Admin 作者能力 | 沿用 `CapabilityCatalog` 范式（`create`/`set_status`/`template.*` 审计 / `_reject_secret_like_metadata`）；issue 087 C3 | Gate A（Employee 写） |
| **Gate C：Company Package 落表 + Admin API** | `company_packages` 表 + `/api/platform/company-packages` | 依赖 Gate B + CapabilityPackage 已具备 | Gate B |
| **Gate D：Company Template 表设计（Phase-5+）** | `company_templates` 表 + 作者端点 | 研究 `ai-company-template-research.md`；独立 ADR | Gate B |
| **Gate E：Phase-9c Marketplace 官方模板上架销售** | 官方模板经 G3 双签上架 | G3 双签 + 安全 gate | Gate B/C（须先有可管理的模板） |

> **优先级建议**：先 Gate A → Gate B（解锁 Admin 可运营官方业务模板的最小动作），再 Gate C/D；Marketplace（Gate E）须最后，且依赖 B/C 完成后模板方可被引用销售。

---

## 6. 完成度评估

| 维度 | 完成度 | 说明 |
|---|---|---|
| 6 类模板契约定义 | 100% | 全部 JSON Schema + 公共基类型 + 类图 |
| Company Package 升级契约 | 100% | 继承 CapabilityPackage + 子包定义 + 组装规则 |
| 与现状命名对齐 | 100% | 差异/待打平项已逐条标注 |
| 后端实现 | 0% | 故意为 0（design-only）；缺口已列 §3 |
| 红线遵守 | 100% | 见 §4 核验 |
| 与 ADR-0017 一致 | 100% | 仅 reservation，无行为变化 |

**总体**：本期为 **design-only 资产基础（100% 契约层）**，实例化/作者端点列为后续 gate（0% 实现，符合预期）。

---

## 7. 验收清单

| # | 验收项 | 状态 |
|---|---|---|
| 1 | 6 类模板 Catalog 总契约（`ai-company-template-system.md`） | ✅ |
| 2 | Company Package 升级契约（`company-package-contract.md`） | ✅ |
| 3 | 公共字段 version/status/source/description 统一 | ✅ |
| 4 | Employee 字段 role/department_type/default_skill/default_tool/persona 覆盖 | ✅ |
| 5 | Department 字段 roles/employee templates/workflows 覆盖 | ✅ |
| 6 | Company 字段 departments/employees/workflows/capability packages 覆盖 | ✅ |
| 7 | SkillPackage / ToolPackage 组合规则 | ✅ |
| 8 | 与 CapabilityPackage 继承/扩展关系 | ✅ |
| 9 | 禁止区核验通过 | ✅ |
| 10 | 下一步 gate 建议明确 | ✅ |

*—— Admin AI Company Asset Foundation 发布评估（纯设计/契约，零代码）。与 ADR-0017 一致；缺口对应 issue 087 C3。*
