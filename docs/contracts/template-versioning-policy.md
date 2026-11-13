# Template Versioning Policy（模板版本管理策略）

> **作者**：高见远（架构师，software-architect）
> **主理人**：齐活林（交付总监）
> **阶段**：Phase-1B Template Runtime Integration Gate（Admin 侧）—— 纯文档（design-only reservation），零代码
> **对齐**：ADR-0017；承接 `template-catalog-runtime-contract.md`（版本字段来源）、`admin-workspace-template-boundary.md`（实例化职责）、`company-package-runtime-contract.md`（组合包版本独立）
> **范围说明**：本策略定义"Admin 升级官方模板后，Workspace 已存在/新创建的实例如何受影响"。**仅为策略定义，不实现任何升级执行**——执行逻辑属后续 gate。

---

## 0. 文档定位与引用

- 本策略回答：**当 `EmployeeTemplate` 从 v1.0 升到 v1.1，已有的 Workspace `EmployeeInstance` 与新创建的实例分别如何表现？**
- 核心原则：**已存在实例快照隔离（默认不自动变化）；新实例使用最新版**。
- 本策略与 `template-catalog-runtime-contract.md` 的 `version` 字段、`admin-workspace-template-boundary.md` 的"Workspace 实例化职责"强相关。

---

## 1. 版本号约定（SemVer）

- 所有 9 类模板（含 `pt_` PersonaTemplate、`wl_` WorkflowContent、`dtpl_` DashboardTemplate）`TemplateCatalogEntry.version` 遵循 `MAJOR.MINOR.PATCH`（`^\d+\.\d+\.\d+$`）。
- 由 Admin 在官方目录侧控制演进（详见 `ai-company-template-system.md` §1）。
- `CompanyPackageRuntime.version` 独立于其组件模板版本演进（见 `company-package-runtime-contract.md` R5）。

---

## 2. 统一状态机（复用 TemplateBase.status）

```
draft ──activate──▶ active ──disable──▶ disabled
  ▲                    │                  │
  └──────── enable ───┴──────────────────┘
  active/archived ◀── archive（可选，仅官方保留历史）
```

- 实例侧有**独立**状态（如 `EmployeeInstance.status`），不因模板 `status` 变化而被动改变（见 §4 矩阵）。

---

## 3. 模板更新规则

### 3.1 已创建的 Workspace 实例：默认不自动变化（快照隔离）

- 实例化时，Workspace 把当时模板的 `version` 与 `metadata` 写入实例快照（见 §5 `template_version_snapshot`）。
- **后续模板升级（v1.0 → v1.1）不影响已存在实例**：实例继续持有 v1.0 快照，行为稳定、可复现。
- 这是默认行为，保证"已上线资产不漂移"。

### 3.2 新创建的实例：使用最新版模板

- Workspace 新建实例时，默认拉取 **`status=active` 中 `version` 最大** 的模板版本。
- 即新实例天然获得官方最新修复/能力，不回溯旧版。

### 3.3 `template_version_snapshot` 机制

- **定义**：实例化动作产生的"模板当时态"冻结副本，绑定到实例。
- **写入时机**：仅实例化那一刻；之后模板再升级不回写快照。
- **内容**：模板 `template_id` + 快照 `version` + 快照 `metadata` 摘要 + 快照时间戳 + `follow_latest` 开关。
- **作用**：实例可随时回溯"它基于哪个模板版本创建"，支持审计与差异对比。

---

## 4. 升级传播矩阵（已存在实例 vs 新实例）

| 升级动作（Admin 侧） | 已存在实例（快照隔离，默认） | 新实例（跟随最新） |
|---|---|---|
| 模板 `version` 升 v1.0 → v1.1（PATCH/MINOR） | **不变**（持有 v1.0 快照） | 使用 v1.1 |
| 模板 `metadata` 字段变更（如 `persona` 文案调整） | **不变**（快照 metadata 不变） | 使用新 metadata |
| 模板 `status` 变 `active`/`disabled`/`archived` | 实例独立状态不受影响 | 新实例按新 `status` 可选范围创建 |
| 模板 `source` 变 `marketplace`（预留） | 不变 | 按新 source 可选范围（须 G3 gate） |
| 组件模板升级，组合包 `CompanyPackageRuntime.version` 不变 | 包内已实例化组件不变 | 新包实例按新组件版本 |
| 组合包 `version` 升级（R5 独立演进） | 不影响已存在实例 | 新实例按新包版本选择组件 |

> **矩阵总结**：升级传播**单向向前**（只影响新实例），**绝不向后**（不影响已存在实例）。这是快照隔离的硬保证。

---

## 5. 快照数据结构（JSON Schema）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TemplateVersionSnapshot",
  "type": "object",
  "additionalProperties": false,
  "required": ["instance_id","template_type","template_id","snapshot_version","snapshot_metadata","snapshot_at","follow_latest"],
  "properties": {
    "instance_id":         { "type": "string", "description": "实例主键（如 EmployeeInstance.id）" },
    "template_type":       { "type": "string", "enum": ["company","department","employee","workflow","skill","tool","persona","dashboard","workflow_content"] },
    "template_id":         { "type": "string", "pattern": "^ct_|dt_|et_|wt_|st_|tt_|pt_|wl_|dtpl_[a-z0-9_-]+$", "description": "快照来源模板的 template_id（含 pt_/wl_/dtpl_ 新增 3 类）" },
    "snapshot_version":    { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "description": "实例化时模板的 version（冻结）" },
    "snapshot_metadata":   { "type": "object", "description": "实例化时模板 metadata 的冻结副本（与 template-catalog-runtime-contract.md 对应类型 metadata 同构）" },
    "snapshot_at":         { "type": "string", "format": "date-time", "description": "实例化时间戳（ISO 8601 UTC）" },
    "follow_latest":       { "type": "boolean", "default": false, "description": "是否跟随最新版开关；默认 false（快照隔离）" }
  },
  "examples": [{
    "instance_id": "ei_backend_001",
    "template_type": "employee",
    "template_id": "et_backend_engineer",
    "snapshot_version": "1.0.0",
    "snapshot_metadata": {
      "role": "Backend Engineer",
      "department_type": "software_rnd",
      "persona": "严谨、注重接口契约的后端工程师。",
      "default_skill": "st_backend_coding",
      "default_tool": "tt_code_executor"
    },
    "snapshot_at": "2026-07-15T08:30:00Z",
    "follow_latest": false
  },{
    "instance_id": "ei_pm_001",
    "template_type": "persona",
    "template_id": "pt_product_manager",
    "snapshot_version": "1.0.0",
    "snapshot_metadata": {
      "archetype": "balanced_facilitator",
      "role": "Product Manager",
      "decision_style": "consultative",
      "reporting_style": "结构化、结论先行"
    },
    "snapshot_at": "2026-07-15T09:10:00Z",
    "follow_latest": false
  },{
    "instance_id": "di_rnd_001",
    "template_type": "dashboard",
    "template_id": "dtpl_ai_rd_ceo_cockpit",
    "snapshot_version": "1.0.0",
    "snapshot_metadata": {
      "company_type": "ai_rd",
      "role_visibility": ["ceo"],
      "widget_ids": ["revenue_trend","active_projects","team_utilization"]
    },
    "snapshot_at": "2026-07-15T09:40:00Z",
    "follow_latest": false
  }]
}
```

---

## 6. "跟随最新"开关策略（默认 off）

| 开关 | 默认值 | 语义 | 影响 |
|---|---|---|---|
| `follow_latest` | **`false`**（默认） | 快照隔离：实例永远使用创建时的模板版本 | 已存在实例稳定、不漂移；模板升级不影响它 |
| `follow_latest = true` | （须显式开启，可能须 gate） | 实例在下次运行/刷新时拉取模板最新版 | 实例随官方升级而更新；带来"漂移"风险，需治理 |

- **默认 off 的理由**：保证已上线资产行为可复现、可审计；避免官方一次升级静默改变成百上千已存在实例。
- **开启 `follow_latest=true` 的治理**：属 Workspace 侧消费逻辑（不在本期）；若未来开放，须明确的"升级评审 + 回滚"机制（建议独立 gate）。

---

## 7. 版本演进示例（EmployeeTemplate v1.0 → v1.1）

```
时间线：
T0  Admin 发布 EmployeeTemplate et_backend_engineer v1.0 (status=active)
T1  Workspace 创建 EmployeeInstance ei_backend_001 → 快照 version=1.0.0, follow_latest=false
T2  Admin 升级 et_backend_engineer → v1.1（persona 文案优化，status 仍 active）
T3  Workspace 再创建 EmployeeInstance ei_backend_002 → 使用 v1.1.0

结果：
- ei_backend_001：持有 v1.0.0 快照，行为不变（快照隔离 ✅）
- ei_backend_002：使用 v1.1.0 最新版（跟随最新 ✅）
- 两者互不影响，Admin 升级未破坏任何已存在实例 ✅
```

---

## 8. 红线与禁止区（本策略遵守）

- **不实现** 任何自动升级执行、不写后端代码、不建表。
- **不修改** Workspace 执行链 / Credential Vault / EmployeeRuntime / Usage Event 写入。
- **不生成** 任何实例；本策略仅定义"若实例化发生，版本如何传播"的规则。

---

## 9. 验收映射

| # | 验收项 | 落点 |
|---|--------|------|
| 1 | SemVer 版本号约定 | §1 |
| 2 | 统一状态机（复用 TemplateBase） | §2 |
| 3 | 已存在实例默认不自动变化（快照隔离） | §3.1 |
| 4 | 新实例使用最新版 | §3.2 |
| 5 | `template_version_snapshot` 机制 | §3.3 / §5 |
| 6 | 升级传播矩阵 | §4 |
| 7 | 快照数据结构 JSON Schema | §5 |
| 8 | "跟随最新"开关策略（默认 off） | §6 |
| 9 | 版本演进示例 | §7 |

*—— Template Versioning Policy（纯设计/策略，零代码）。与 ADR-0017 一致。*
