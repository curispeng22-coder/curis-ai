# Admin Commercial Configuration Contract（商业配置契约）

> **作者**：高见远（架构师，software-architect）
> **阶段**：Phase-8.6 Admin Commercial Configuration Audit + Design（设计审计阶段，零代码）
> **契约定位**：定义 **Admin Commercial Configuration Domain** 的 8 个核心配置对象，逐节标注
>   - **当前实现状态**：`exists`（已落地可生产配置）/ `partial`（部分落地或仅以 JSON blob 承载）/ `design-only`（仅设计，无 Admin API/表）
>   - **管理 API / 表**：由哪个 Admin API 或数据库表管理
> - 本文档**引用不重定义**既有契约（`admin-plan-management-contract.md`、`admin-quota-contract.md`、`admin-capability-package-contract.md`、`pricing-package-contract.md`、`quota-rule-contract.md`、`billing-rule-contract.md`、`phase9a-plan-config-adjust-design.md`、`phase9a-commercial-design-freeze.md`）。
> - **红线**：本阶段不开发 payment / 自动扣款 / Invoice / Marketplace 交易 / Promotion 执行 / ROI；不修改 Workspace 执行链；不修改 Credential Vault；不把商业规则写死代码。

---

## 0. 引用基线（来自真实代码扫描）

| 真实落点 | 证据 | 说明 |
| --- | --- | --- |
| `plans` 表（三档 seed 可配） | `backend/app/database.py:746-838` | 列：`plan_id, plan_code, name, tier, status, version, billing_interval, features_json, quota_rules_json`；**无 price / billing_cycle 列** |
| `quotas` 表（租户实例） | `backend/app/database.py:763-781` | 列含 `is_unlimited`（Phase-9A 新增）；`quota_type ∈ {token, employee_seat, capability, workflow}` |
| `quota_rules_json`（plan 模板内 JSON blob） | `database.py:829-836` | 含 `quota_mode / is_unlimited / token_monthly_limit / seat_limit / workflow_monthly_limit / capability_sources / overage{...} / currency` |
| Plan/Quota/Capability/Billing API | `main.py:1428-1583` | `GET/POST/PUT /api/platform/plans`、`/api/platform/quotas`、`/api/platform/capabilities`、`/api/platform/billing-events` |
| Tier 枚举 | `database.py:750` CHECK + `frontend/.../PlanManagementPanel.js:9` | `free / pro / enterprise`（受控词汇，非商业数值） |

---

## 1. Plan Configuration（对象 Plan）

**字段**：`plan_id, name, tier, description, price, billing_cycle, status, features, quota_rules`

### 1.1 当前实现状态：`partial`

- `plan_id / plan_code / name / tier / status / version / billing_interval / features_json / quota_rules_json` **已落地**（`plans` 表 + `POST/PUT /api/platform/plans` + `POST /api/platform/plans/{id}/toggle`）。
- ⚠️ **`price` / `billing_cycle` 字段缺失**：`plans` 表**无 `price` 列**，也无 `billing_cycle` 列。当前价格仅以 `quota_rules_json.overage{...}` 内的**超量单价占位**（Pro 为 `null` 占位，Free 为 `0`，Enterprise 为 `null`）存在，**订阅基底价（subscription price）完全无落点**。
- Free / Pro / Enterprise **不是硬编码**：三档由 `database.py` 幂等 seed（`INSERT OR IGNORE`）初始生成，Admin 经 `PUT /api/platform/plans/{id}` 可整体覆盖 `name / features / quota_rules`，经 `toggle` 改 `status`。**运行时完全可配置**；仅"默认初始值"写在 seed 中（属 bootstrap 数据，非逻辑硬编码）。

### 1.2 Phase-9 Schema Gap（订阅价无落点）

| 方案 | 推荐度 | 说明 |
| --- | --- | --- |
| **A. 统一由 PricingRule 管理**（新增 `pricing_rules` 表，`subject_type='subscription'`，`subject_id=plan_id`） | ⭐ 推荐（主） | 与超量价、能力包价、席位价统一在同一张定价规则表，避免 `plans` 表膨胀；`price / billing_cycle` 由 PricingRule 表达 |
| **B. `plans` 表新增 `price` + `billing_cycle` 列** | 次选（便利镜像） | 在 `plans` 直接加列，由 PricingRule(subscription) 激活后同步；前端展示更直接 |
| **C. 维持现状（仅 overage 占位）** | ❌ 不推荐 | 订阅价无法配置，违反"商业规则必须配置化"红线 |

> **结论**：采用 **方案 A 为主、B 可选镜像**。Phase-9 必须新增订阅价配置能力，否则 Pro/Enterprise 无法进入真实收费。本阶段（8.6）仅设计，不建列。

### 1.3 管理 API / 表

- **表**：`plans`（`backend/app/database.py:746`）
- **API**：`GET/POST /api/platform/plans`、`GET/PUT /api/platform/plans/{plan_id}`、`POST /api/platform/plans/{plan_id}/toggle`（`main.py:1428-1483`）

---

## 2. Pricing Rule（对象 PricingRule）

**支持维度**：`subscription_price, token_usage_price, capability_package_price, employee_seat_price, connector_price`
**字段**：`rule_id, subject_type, pricing_type, amount, currency, effective_time, status`

### 2.1 当前实现状态：`partial`（仅超量价，且嵌在 plan JSON 内）

- **超量价（token_usage / employee_seat / workflow / capability）**：已存在，但**非结构化**——嵌在 `plans.quota_rules_json.overage{ token_unit_price_per_1k, seat_unit_price, workflow_unit_price, capability_unit_price }`（`database.py:829-836`）。Admin 经 `PUT /api/platform/plans` 整体覆盖可改。
- **订阅价（subscription_price）**：❌ 无落点（见 §1.2）。
- **能力包价（capability_package_price）/ 席位价（employee_seat_price）/ connector 价**：❌ 无独立结构化规则（仅 seat 超量价存在）。
- **结构化 `pricing_rules` 表**：❌ 未建。当前价格散落在 plan JSON，无 `effective_time`、无 `status` 生命周期、无多维统一建模。

### 2.2 设计（Phase-9 落地）

新增 `pricing_rules` 表，`subject_type ∈ {subscription, token_usage, capability_package, employee_seat, connector}`，`subject_id` 指向 plan_id / capability_package_id / connector_id 等。历史 `quota_rules.overage` 迁移为 `pricing_rules` 中 `subject_type ∈ {token_usage, employee_seat, workflow, capability}` 的行。

### 2.3 管理 API / 表

- **表（设计）**：`pricing_rules`（Phase-9 新增）
- **API（设计）**：`GET/POST/PUT /api/platform/pricing-rules`（Phase-9 新增）
- **当前过渡**：超量价经 `PUT /api/platform/plans/{id}` 的 `quota_rules.overage` 字段配置（`main.py:1463`）

---

## 3. Quota Rule（对象 QuotaRule）

**支持维度**：`token_limit, employee_seat_limit, workflow_limit, capability_limit, connector_limit`
**字段**：`quota_id, plan_id, quota_type, limit_value, period, enforcement_mode`
**`enforcement_mode` ∈ `notify / throttle / block / billing_only`**

### 3.1 当前实现状态：`partial`（plan 内 JSON blob，非结构化；enforcement_mode 缺失）

- 配额规则**已存在但非结构化**：作为 `plans.quota_rules_json` 内的 JSON blob（`token_monthly_limit / seat_limit / workflow_monthly_limit / capability_sources`），**不是独立结构化表**。
- `enforcement_mode`：**❌ 不存在**。当前配额仅用于"读时聚合 + 看板 notify 预警"（`phase9a-commercial-design-freeze.md` §2.1），语义上等价于 `notify`；`throttle / block / billing_only` 均未实现。
- `connector_limit`：**❌ 未实现**。`quotas.quota_type` CHECK 仅含 `token/employee_seat/capability/workflow`（`database.py:769`）；`capability_type=connector` 虽在 `catalog_constants.CAPABILITY_TYPE`（`catalog_constants.py:32`），但 connector 计量数据源未接入（freeze §2.4）。
- 区分提示：`quotas` 表是**租户实例表**（per-tenant per-quota_type），`QuotaRule` 应是**套餐模板规则表**（per-plan）。二者必须区分。

### 3.2 设计建议：Phase-9 将 QuotaRule 提升为独立表

> **推荐**：新增 `plan_quota_rules` 表（套餐模板规则），与 `quotas`（租户实例）明确区分：

| 表 | 语义 | 主键 | 关键列 |
| --- | --- | --- | --- |
| `plan_quota_rules`（Phase-9 新增） | 套餐模板规则 | `quota_rule_id` | `plan_id, quota_type, limit_value, period, enforcement_mode, is_unlimited, overage_price_ref` |
| `quotas`（已存在） | 租户配额实例 | `quota_id` | `tenant_id, plan_id, quota_type, limit_value, is_unlimited, current_usage, period` |

### 3.3 迁移建议（从 `quota_rules_json` 到 `plan_quota_rules`）

1. 新建 `plan_quota_rules` 表（additive，不删 `quota_rules_json` 兼容期）。
2. 一次性脚本：遍历 `plans`，解析 `quota_rules_json`，为 `token/employee_seat/workflow/capability` 各生成一行 `plan_quota_rules`（`enforcement_mode` 默认 `notify`，`limit_value` 取自 `token_monthly_limit` 等，`period` 取自 `billing_interval`）。
3. 新增 `POST/PUT /api/platform/plans/{id}/quota-rules` 管理端点；保留 `quota_rules_json` 作为冗余缓存或弃用。
4. `calculate_billing_events` 改为读 `plan_quota_rules`（custom 模式仍派生 `quotas` 实例）。

### 3.4 管理 API / 表

- **表（当前）**：`plans.quota_rules_json`（`database.py:757`）；`quotas`（租户实例，`database.py:763`）
- **API（当前）**：`GET/POST /api/platform/quotas`、`PUT /api/platform/quotas/{quota_id}`（租户实例，`main.py:1500-1555`）；plan 模板经 `PUT /api/platform/plans/{id}`（整体覆盖）
- **API（设计）**：`GET/POST/PUT /api/platform/plans/{id}/quota-rules`（模板规则）

---

## 4. Capability Package Configuration（对象 CapabilityPackage）

**字段**：`package_id, name, description, capability_ids, connector_ids, workflow_ids, employee_templates, pricing_reference, status`

### 4.1 当前实现状态：`partial`（单能力目录 exists；组合包 design-only）

- **单能力目录（official capability）**：`capability_catalog`（表）+ `GET/POST/PUT /api/platform/capabilities`（`main.py:1371-1417`）已落地，Admin 可 CRUD 单个 model/tool/connector 能力并上/下架。
- **组合能力包（CapabilityPackage）**：❌ **design-only**。文档定义的"内容运营包 = 小红书 Connector + TikTok Connector + 内容生产 Workflow + 内容运营 AI Employee Template"这类**组合包**尚无结构化对象与 Admin API。当前能力以扁平 `capability_key` 列表存在，无 `workflow_ids / employee_templates` 组合字段，无 `pricing_reference`。
- 既有契约 `admin-capability-package-contract.md` 已定义 `package_id / included_capability_ids / included_template_ids / plan_tiers / version / pricing_reference`，但实现侧仅落地了"单能力条目"，未落地"组合包"。

### 4.2 示例（设计态）

**内容运营包**（`package_id = pkg_content_ops`）：
- `capability_ids`：[`connector_xiaohongshu`, `connector_tiktok`]
- `workflow_ids`：[`wf_content_production`]
- `employee_templates`：[`tpl_content_ops_employee`]
- `pricing_reference`：`pricing_rule:capability_package:pkg_content_ops`（指向 PricingRule）
- `status`：`draft`（待 Admin 上架）

### 4.3 管理 API / 表

- **表（当前）**：`capability_catalog`（单能力）
- **API（当前）**：`GET/POST/PUT /api/platform/capabilities`（`main.py:1371-1417`）
- **API（设计）**：`GET/POST/PUT /api/platform/capability-packages`、`/bind-plan`（组合包，参考 `admin-capability-package-contract.md` §3）

---

## 5. Employee Template Commercial Catalog（对象 EmployeeTemplateCatalog）

**字段**：`template_id, name, role, department_type, default_capabilities, pricing_reference, seat_type, status`
**边界**：Admin 管官方员工模板（目录/商业语义）；Workspace 管 EmployeeInstance（运行实例）。

### 5.1 当前实现状态：`design-only`（种子数据 exists；Admin 作者 API 缺失）

- 官方员工模板由 `database.py:_seed_employee_template_contract`（`database.py:941`）幂等 seed，但**仅是数据**。
- **Admin 官方模板作者 API**：❌ 不存在。路由仅 `GET /api/workspace/employee-templates`（`main.py:912`，Workspace 只读官方模板），**无 `/api/platform/employee-templates` 写端点**。Admin 无法在后台创建/编辑/上下架官方员工模板。
- `default_capabilities / seat_type / pricing_reference`：尚未作为结构化商业字段建模。

### 5.2 管理 API / 表

- **表（种子）**：员工模板表（`database.py:_seed_employee_template_contract`）
- **API（设计）**：`GET/POST/PUT /api/platform/employee-templates`、`/publish`、`/deprecate`（Admin 官方模板治理）
- **运行时读取**：`GET /api/workspace/employee-templates`（`main.py:912`，Workspace 侧）

---

## 6. Workflow Template Commercial Catalog（对象 WorkflowTemplateCatalog）

**字段**：`workflow_template_id, name, type, steps, employee_roles, pricing_reference, status`
**边界**：Admin 管官方 Workflow（SOP）模板；Workspace 管 WorkflowRun（运行实例）。

### 6.1 当前实现状态：`design-only`（种子数据 exists；Admin 作者 API 缺失）

- 官方 Workflow 模板由 `database.py:_seed_workflow_runtime_contract`（`database.py:1076`）seed。
- **Admin 官方 SOP 模板作者 API**：❌ 不存在。路由仅 `GET /api/workspace/workflow-templates`（`main.py:920`），**无 `/api/platform/workflow-templates` 写端点**。
- `employee_roles / pricing_reference`：尚未结构化。

### 6.2 管理 API / 表

- **表（种子）**：workflow 模板表（`database.py:1076`）
- **API（设计）**：`GET/POST/PUT /api/platform/workflow-templates`（Admin 官方 SOP 治理）
- **运行时读取**：`GET /api/workspace/workflow-templates`（`main.py:920`）

---

## 7. Promotion Rule（对象 PromotionRule，本阶段只设计不实现）

**支持**：新用户优惠 / 限时优惠 / 节日活动 / 企业客户优惠
**字段**：`promotion_id, name, type, discount_rule, start_time, end_time, target_scope, status`

### 7.1 当前实现状态：`design-only`

- 无任何 Promotion 表 / API（本阶段红线禁止 Promotion 执行系统）。
- 仅作为**设计态对象**存在，供 Phase-9C/运营场景预览（见 §9 场景4）。

### 7.2 管理 API / 表（设计）

- **表（设计）**：`promotion_rules`（Phase-9 设计）
- **API（设计）**：`GET/POST/PUT /api/platform/promotions`

---

## 8. Tenant Pricing Policy（对象 TenantPricingPolicy）

**支持**：企业客户特殊价格
**字段**：`tenant_id, plan_override, quota_override, discount_override, effective_time, status`
**示例**：战略客户 Pro Enterprise + 特殊额度 + 特殊价格。

### 8.1 当前实现状态：`design-only`（部分能力可由 quotas 近似，但无统一策略对象）

- **特殊额度（quota_override）**：✅ 部分可配——Admin 经 `POST /api/platform/quotas` 为企业租户建 `quotas` 实例（`custom` 模式，`database.py` + `main.py:1508`），已支持"特殊额度"。
- **特殊价格（plan_override / discount_override）**：❌ 无落点。订阅价/折扣无结构化对象（依赖 §1.2 / §2 的 PricingRule + PromotionRule）。
- 统一的 `TenantPricingPolicy` 策略对象：**design-only**。

### 8.2 管理 API / 表（设计）

- **表（设计）**：`tenant_pricing_policies`（Phase-9）
- **API（设计）**：`GET/POST/PUT /api/platform/tenants/{tenant_id}/pricing-policy`
- **当前近似**：`POST /api/platform/quotas`（仅额度，`main.py:1508`）

---

## 9. 商业配置对象清单（8 对象总览）

| # | 对象 | 核心字段 | 当前状态 | 管理 API / 表 | 是否需 Phase-9 新增 |
| --- | --- | --- | --- | --- | --- |
| 1 | **Plan** | plan_id, name, tier, price, billing_cycle, status, features, quota_rules | `partial` | `plans` 表 + `/api/platform/plans` | ✅ 需补 `price/billing_cycle`（或 PricingRule 承载） |
| 2 | **PricingRule** | rule_id, subject_type, pricing_type, amount, currency, effective_time, status | `partial` | 当前嵌 `plans.quota_rules.overage`；设计 `pricing_rules` 表 | ✅ 需新增 `pricing_rules` 结构化表 |
| 3 | **QuotaRule** | quota_id, plan_id, quota_type, limit_value, period, enforcement_mode | `partial` | 当前 `plans.quota_rules_json`（blob）；设计 `plan_quota_rules` | ✅ 需提升为结构化表 + enforcement_mode |
| 4 | **CapabilityPackage** | package_id, capability_ids, connector_ids, workflow_ids, employee_templates, pricing_reference, status | `partial` | 单能力 `capability_catalog` + `/api/platform/capabilities`；组合包 design-only | ✅ 需新增组合包对象/API |
| 5 | **EmployeeTemplateCatalog** | template_id, role, default_capabilities, seat_type, pricing_reference, status | `design-only` | 种子数据；无 Admin 写 API | ✅ 需新增 `/api/platform/employee-templates` |
| 6 | **WorkflowTemplateCatalog** | workflow_template_id, type, steps, employee_roles, pricing_reference, status | `design-only` | 种子数据；无 Admin 写 API | ✅ 需新增 `/api/platform/workflow-templates` |
| 7 | **PromotionRule** | promotion_id, type, discount_rule, start_time, end_time, target_scope, status | `design-only` | 无（本阶段禁止实现） | ⏸ Phase-9C（禁止本阶段） |
| 8 | **TenantPricingPolicy** | tenant_id, plan_override, quota_override, discount_override, effective_time, status | `design-only` | 额度近似 `quotas`；策略对象无 | ✅ 需新增策略对象（价格/折扣部分） |

---

## 10. 未来运营场景验证（无需修改代码即可达成）

> 核心证明：以下场景依赖的"配置面"已在设计/现状中具备，运营经 Admin API/后台即可操作，**无需改码、无需重新发布**。

| 场景 | 依赖对象 / API | 当前是否具备 | gap 与处置 |
| --- | --- | --- | --- |
| **场景1：运营创建新套餐** | Plan（`POST /api/platform/plans`） | ✅ `exists` | 无 gap；新套餐经 API 创建即生效，`tenants.plan_tier` 1:1 对齐 |
| **场景2：运营创建能力包**（如内容运营包：Connector+Workflow+Employee Template） | CapabilityPackage（`/api/platform/capability-packages`） | ⚠️ `design-only`（组合包） | gap：组合包 API 未建；**Phase-9A 需落地组合包对象**（单能力已可配）。落地后无需改 Workspace |
| **场景3：企业客户特殊价格** | TenantPricingPolicy + PricingRule | ⚠️ `design-only` | gap：订阅价/折扣无落点（§1.2/§2/§8）；Phase-9 引入 `pricing_rules` + `tenant_pricing_policies` 后无需改码 |
| **场景4：促销活动 30 天优惠** | PromotionRule（设计态） | ⚠️ `design-only` | gap：PromotionRule 本阶段禁止实现；Phase-9C 设计态落地后，运营配置即生效，无需重新发布 |

> **结论**：场景 1 现已具备（零代码即可运营新套餐）；场景 2/3/4 的依赖对象需在 Phase-9 对应 gate 落地后具备，落地后均"无需改码"。本契约即为这些场景的配置面契约基础。

---

*—— Phase-8.6 Admin Commercial Configuration Contract（纯设计/契约，无代码）。引用既有契约，标注 8 对象现状与 Phase-9 缺口。*
