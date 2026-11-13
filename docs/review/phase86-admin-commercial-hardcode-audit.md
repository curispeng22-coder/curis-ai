# Phase-8.6 Admin Commercial Hardcode Audit（商业规则硬编码审计）

> **作者**：高见远（架构师，software-architect）
> **阶段**：Phase-8.6 Admin Commercial Configuration Audit + Design（设计审计阶段，零代码）
> **方法**：真实扫描 `backend/app/*.py` 与 `frontend/app/platform/*.js`，对每条发现给出 `文件:行号`、字面量、控制语义、P0/P1/P2。
> **P 分级**：
> - **P0**：必须配置化（套餐名称/价格、Token 额度、员工数量、Workflow 额度、Capability 额度、Connector 额度等）
> - **P1**：未来 Marketplace / 企业版需要（能力收费规则、能力包组成、模型价格范围、员工等级等）
> - **P2**：可保持代码固定（纯内部常量、非商业语义的枚举/默认值）

---

## 0. 审计范围与基线

| 扫描对象 | 行数/范围 | 目的 |
| --- | --- | --- |
| `backend/app/database.py` | seed / DDL `746-838`、`941` 员工模板、`1076` workflow 模板 | 找 plan/quota/模板的硬编码数值与枚举 |
| `backend/app/billing_store.py` | `659-800` calculate_billing_events | 确认超量价来源（是否硬编码） |
| `backend/app/catalog_constants.py` | `18-73` 枚举常量 | 确认能力/网关枚举 |
| `backend/app/model_gateway.py` | `100-126` 成本估算 | 确认模型价格是否硬编码/可配 |
| `backend/app/main.py` | `1428-1583` platform 路由 | 确认 Admin 可配面覆盖 |
| `frontend/app/platform/PlanManagementPanel.js` | `9` TIERS | 找前端硬编码枚举 |
| `frontend/app/platform/QuotaManagementPanel.js` | `207` 注释 | 找残留语义 |

**关键结论前情**：结合 Phase-9A 调整成果（Free/Pro/Enterprise 已 seed 可配、Pro 价格已 `null` 占位、is_unlimited 已引入），**逻辑层硬编码商业规则已大量消除**；残留项主要为"订阅价无落点""组合包/模板作者 API 缺失""模型价不可配"等**配置面缺口**，以及少量可保留的枚举常量。

---

## 1. 已消除的硬编码项（结合 Phase-9A + 当前代码）

| 原硬编码项 | 证据（当前代码） | 消除方式 |
| --- | --- | --- |
| **Enterprise "0=无限"**（limit=0 被静默当无限） | `database.py:814` Enterprise seed `quota_mode:"custom", is_unlimited:false, token_monthly_limit:null`；`billing_store.py:699-727` 基于显式 `is_unlimited` 判定 | ✅ 引入 `quota_mode` + `is_unlimited`，0 不再等于无限 |
| **Pro 真实超量价写死**（0.002/9/0.01） | `database.py:833` Pro overage 全部 `null` 占位 | ✅ 改为 `null` 占位，待 Admin 配置，不写死真实价格 |
| **Plan 三档名称/额度写死在逻辑** | `plans` 经 `POST/PUT /api/platform/plans`（`main.py:1428-1483`）运行时可整体覆盖 | ✅ 三档为 seed 初始值，Admin 可配；非逻辑硬编码 |
| **配额上限判定依赖 limit>0** | `billing_store.py:727` `elif limit and limit > 0` + `configured` 标记 | ✅ 修正语义，未配置场景标记待 Admin 设 |

---

## 2. 仍残留的硬编码 / 配置面缺口（5 类）

### 2.1 商业规则（套餐 / 价格 / 额度）

| 文件:行号 | 字面量 | 控制什么 | 分级 |
| --- | --- | --- | --- |
| `database.py:829-836` | `token_monthly_limit:1000000/50000000`、`seat_limit:3/15`、`workflow_monthly_limit:0/50000`、`overage:{...0 / null}` | Free/Pro 默认额度与超量价（seed 初始值） | **P2**（bootstrap 数据；运行时经 `/api/platform/plans` 可覆盖，非逻辑硬编码） |
| `database.py:829-836` | `name:'Free'/'Pro'/'Enterprise'`、`tier` | 三档默认名称/档位（seed） | **P2**（同上，可配） |
| `database.py`（全表） | **无 `price` / `billing_cycle` 列** | 订阅基底价**完全无落点**，无法配置 | **P0**（必须配置化；见契约 §1.2，Phase-9 补 `pricing_rules` 或 `plans.price`） |
| `database.py:750` | `tier in ('free','pro','enterprise')` | 套餐档位受控枚举 | **P2**（商业分类枚举，可接受） |
| `database.py:754-755` | `billing_interval in ('monthly','annual','custom')` | 计费周期枚举 | **P2** |
| `database.py:769` | `quota_type in ('token','employee_seat','capability','workflow')` | 配额类型枚举（**缺 `connector`**） | **P1**（Connector 计量未接入；需 additive 扩展） |
| `frontend/app/platform/PlanManagementPanel.js:9` | `const TIERS = ["free","pro","enterprise"]` | 前端档位下拉枚举 | **P2**（UI 常量；未来新增档位建议从 API 派生） |

### 2.2 AI 员工商业规则（官方模板 / 默认能力绑定 / 席位 / 等级）

| 文件:行号 | 字面量 | 控制什么 | 分级 |
| --- | --- | --- | --- |
| `database.py:941` (`_seed_employee_template_contract`) | 官方员工模板 seed（含默认能力绑定） | 官方 AI 员工模板及其默认能力 | **P1**（Admin 官方模板作者 API 缺失，仅种子数据；需 `/api/platform/employee-templates`） |
| `database.py:829-836` | `seat_limit:3/15` | 各档 AI 员工席位数（seed 默认） | **P2**（运行时可配） |
| （无字段） | 无 `seat_type` / 员工等级商业字段 | 员工席位类型/等级未结构化 | **P1**（未来企业版席位分级需配置化） |

### 2.3 Workflow 商业规则（官方 SOP 模板 / 限制 / 执行额度）

| 文件:行号 | 字面量 | 控制什么 | 分级 |
| --- | --- | --- | --- |
| `database.py:1076` (`_seed_workflow_runtime_contract`) | 官方 Workflow 模板 seed | 官方 SOP 模板 | **P1**（Admin 官方 SOP 作者 API 缺失，仅种子；需 `/api/platform/workflow-templates`） |
| `database.py:829-836` | `workflow_monthly_limit:0/50000` | 各档 Workflow 月度运行额度（seed） | **P2**（运行时可配） |
| （无字段） | 无 `enforcement_mode` | 配额仅 notify，无 throttle/block | **P1**（真实拦截属 G1 后工程，本期语义展示） |

### 2.4 Capability 商业规则（能力收费 / 包组成 / 套餐关联）

| 文件:行号 | 字面量 | 控制什么 | 分级 |
| --- | --- | --- | --- |
| `database.py:829-836` | `overage.capability_unit_price:0/null` | Capability 超量单价（嵌 plan JSON） | **P2**（运行时经 plan 可配；但非结构化，建议 Phase-9 提 `pricing_rules`） |
| `database.py:829-836` | `capability_sources:["official"]/["official","tenant_private"]/["official","tenant_private","marketplace"]` | 各档能力来源白名单 | **P2**（运行时可配） |
| （无组合包对象） | 无 `CapabilityPackage`（组合包） | 内容运营包等组合包未建模 | **P1**（组合包 design-only，需 Phase-9A 落地组合包对象/API） |
| `catalog_constants.py:32` | `CAPABILITY_TYPE = ["model","tool","connector"]` | 能力类型枚举 | **P2** |

### 2.5 Model 商业规则（模型价格 / 可用范围 / 成本参数）

| 文件:行号 | 字面量 | 控制什么 | 分级 |
| --- | --- | --- | --- |
| `model_gateway.py:125` (`_estimated_cost`) | `estimated_cost = f(usage, total_tokens)`（来自网关运行时响应） | 模型成本估算（**来自上游网关响应，非 Admin 配置**） | **P1**（模型价格**不可 Admin 配置**，仅运行时派生；需 Phase-9 引入模型价配置面） |
| `catalog_constants.py:21` | `MODEL_AUTH_TYPE = ["none","oauth","apikey"]` | 模型鉴权类型枚举 | **P2** |
| `main.py:1326-1351` | `/api/platform/models` | 模型可用范围（active/inactive）管理 | **P2**（已可配；价格仍不可配，见上） |
| （无列） | `official_models` 无 price 列 | 模型单价不可配 | **P1**（缺口，需 `pricing_rules` subject_type=model 或模型价列） |

---

## 3. 硬编码商业规则清单（汇总表）

| # | 规则 | 位置 | 当前值 | 分级 | 迁移动作 |
| --- | --- | --- | --- | --- | --- |
| 1 | 订阅基底价 | `plans` 表（无列） | 无落点（`$XX` 占位） | **P0** | Phase-9 新增 `pricing_rules`(subscription) 或 `plans.price` |
| 2 | Free Token 额度 | `database.py:830` | 1,000,000 | P2 | 保留 seed；运行时可配 |
| 3 | Pro Token 额度 | `database.py:833` | 50,000,000 | P2 | 保留 seed；运行时可配 |
| 4 | Free/Pro 席位 | `database.py:830/833` | 3 / 15 | P2 | 保留 seed；运行时可配 |
| 5 | Free/Pro Workflow 额度 | `database.py:830/833` | 0 / 50,000 | P2 | 保留 seed；运行时可配 |
| 6 | Pro 超量价 | `database.py:833` | `null` 占位 | P2 | Admin 经 plan 配置（已可配，非写死） |
| 7 | Enterprise 自定义额度 | `database.py:836` | `null`（custom） | P2 | Admin 经 `quotas` 实例配置 |
| 8 | tier 枚举 | `database.py:750` | free/pro/enterprise | P2 | 保留受控枚举 |
| 9 | billing_interval 枚举 | `database.py:754` | monthly/annual/custom | P2 | 保留 |
| 10 | quota_type 枚举（缺 connector） | `database.py:769` | 4 类 | **P1** | additive 扩展 `connector` |
| 11 | 官方员工模板 | `database.py:941` | seed 数据 | **P1** | 新增 `/api/platform/employee-templates` |
| 12 | 员工等级/seat_type | 无字段 | — | **P1** | Phase-9 结构化 |
| 13 | 官方 Workflow 模板 | `database.py:1076` | seed 数据 | **P1** | 新增 `/api/platform/workflow-templates` |
| 14 | enforcement_mode | 无字段 | 仅 notify 语义 | **P1** | Phase-9 新增字段（throttle/block/billing_only） |
| 15 | Capability 超量价 | `database.py:830/833` | 0 / null | P2 | 运行时可配；建议提 `pricing_rules` |
| 16 | capability_sources 白名单 | `database.py:830/833/836` | official/tenant_private/marketplace | P2 | 运行时可配 |
| 17 | 组合能力包 | 无对象 | — | **P1** | Phase-9A 落地组合包 |
| 18 | 模型价格 | `model_gateway.py:125`（运行时派生） | 网关响应 | **P1** | Phase-9 引入模型价配置面 |
| 19 | 模型可用范围 | `main.py:1326` | active/inactive | P2 | 已可配 |
| 20 | 前端 tier 下拉 | `PlanManagementPanel.js:9` | 三档数组 | P2 | 未来从 API 派生 |
| 21 | Quota 面板语义注释 | `QuotaManagementPanel.js:207` | "0=不限" 旧语义 | P2 | 修正注释为 is_unlimited |

---

## 4. P0 / P1 / P2 迁移计划

| 阶段 | 对象 | 动作 | 负责 Phase | 分级 |
| --- | --- | --- | --- | --- |
| **Phase-9A** | Plan / PricingRule / QuotaRule / CapabilityPackage | 补订阅价（`pricing_rules` 或 `plans.price`）；将 `quota_rules_json` 提升为结构化 `plan_quota_rules`（含 `enforcement_mode`）；落地组合能力包对象 | Phase-9A | **P0 + P1** |
| **Phase-9A** | CapabilityPackage | 组合包（Connector+Workflow+Employee Template）可配，无需改 Workspace | Phase-9A | **P1** |
| **Phase-9B** | PricingRule / TenantPricingPolicy | 订阅价生效、企业客户特殊价格/折扣策略（接支付/发票 gate） | Phase-9B（gate） | **P0** |
| **Phase-9B** | Model | 模型价配置面（subject_type=model 的 PricingRule 或模型价列） | Phase-9B | **P1** |
| **Phase-9B** | QuotaRule | `enforcement_mode` 真实 throttle/block（G1 后配额中间件） | Phase-9B+ | **P1** |
| **Phase-9C** | PromotionRule / CapabilityPackage | 促销活动 30 天优惠；Marketplace 能力包销售/分成（G3 双签） | Phase-9C（gate） | **P1** |
| **Phase-9D** | ValueEvent / Model | 价值计费商业化（禁止区，独立 gate） | Phase-9D（gate） | **P1** |
| **始终保留** | tier / billing_interval / quota_type / CAPABILITY_TYPE / MODEL_AUTH_TYPE / 前端 TIERS | 受控枚举常量，不配置化 | — | **P2** |
| **收尾** | QuotaManagementPanel.js:207 注释 | 修正 "0=不限" → is_unlimited 语义 | Phase-9A 前端 | **P2** |

---

## 5. 审计结论

1. **逻辑层硬编码商业规则已基本消除**：套餐名称/档位/额度/超量价均可在运行时经 Admin API 配置；Enterprise "0=无限" 与 Pro 真实价写死两项已在 Phase-9A 修正。
2. **P0 残留 = 订阅价无落点**：`plans` 表无 `price`/`billing_cycle`，订阅基底价完全无法配置。Phase-9 必须补 `pricing_rules`（subscription）或 `plans.price`，否则 Pro/Enterprise 无法进入真实收费。**这是本阶段唯一 P0 缺口**。
3. **P1 残留 = 配置面未覆盖项**：组合能力包、官方员工/Workflow 模板作者 API、模型价配置面、enforcement_mode、connector 配额、员工等级——均为"未来 Marketplace/企业版需要"的对象，设计态已定义，待对应 Phase gate 落地。
4. **P2 保留 = 受控枚举/seed 默认值**：tier/billing_interval/quota_type/CAPABILITY_TYPE 等枚举与 seed 初始值保持代码固定，不违反"商业规则不写死"红线（它们是非数值的商业分类常量，且运行时可覆盖）。

> **红线校验**：全程未发现"将真实商业数值写死在函数逻辑中"的残留（如 `if plan=='pro': price=0.002` 这类）；所有数值均来自 `plans.quota_rules_json` / `quotas` 配置或网关运行时响应。符合"不把商业规则写死代码"约束。

---

*—— Phase-8.6 Admin Commercial Hardcode Audit（真实代码扫描，零代码）。P0=订阅价缺口；P1=配置面未覆盖；P2=受控枚举/seed。*
