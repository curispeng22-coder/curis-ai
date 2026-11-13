# Phase-9A Commercial Configuration 完成度评估

> **阶段**：Phase-9A（Commercial Configuration Foundation）
> **作者**：高见远（架构师，software-architect）
> **协作团队**：`software-phase9a-lrt-commcfg`（主理人齐活林 / 架构师高见远）
> **文档性质**：**完成度评估（纯文档·零代码）**——不创建表、不修改源码、不实现支付/计费。
> **目标**：评估 Phase-9A 商业配置对象的落地程度，判定是否具备进入 **Commercial Operation Console（商业运营控制台）** 开发的条件。

---

## 0. 范围与边界

| 项 | 说明 |
| --- | --- |
| 评估对象 | Commercial Configuration Domain 的 9 个配置对象（见 `commercial-configuration-v1.md` §2） |
| 本会话产出 | 仅 3 份契约/状态文档（EmployeeSeatPolicy 契约 + 域总览 v1 + 本评估）；**零代码变更** |
| 红线一致性 | 与 `phase9a-commercial-design-freeze.md` 六禁一致：不收费/不支付/不生成真实 Invoice/不自动扣款/不实现 Marketplace 分成/不实现 Value Pricing |
| 不在本范围 | 真实出账 / 支付 / 发票 / 自动扣款子系统——须作为**独立 gate 子项**（建议 Phase-9b）单独裁决 |

---

## 1. 已完成对象

| 对象 | 落地证据 | 状态 |
| --- | --- | --- |
| **PricingRule** | `pricing_rules` 表 + `_require_platform_admin` 路由（GET/POST/PUT `/api/platform/pricing-rules`）+ P0b 采纳「激活新规则时置旧 active 同 plan 规则 expired」 | ✅ 已实现结构化实体 + Admin API + 测试 |
| **QuotaRule** | `quota_rules` 表（部分唯一索引：每 plan+type 仅一条 active）+ 路由（GET/POST/PUT `/api/platform/quota-rules` + GET `/api/platform/plans/{plan_id}/quotas`）；`quota_type ∈ {token_limit, employee_seat_limit, workflow_limit, capability_limit, connector_limit}`；`enforcement_mode ∈ {notify, throttle, block, billing_only}` | ✅ 已实现结构化实体 + Admin API + 测试 |
| **CapabilityPackage** | `capability_packages` 表 + 路由（GET/POST/GET/{id}/PUT `/api/platform/capability-packages`）；字段含 `package_id/name/description/capability_ids/connector_ids/workflow_template_ids/employee_template_ids/pricing_reference/quota_reference/availability/status` | ✅ 已实现结构化实体 + Admin API + 测试 |
| **EmployeeSeatPolicy** | 本批次新增 `employee-seat-commercial-contract.md`（套餐级商业席位政策契约） | 📄 本次**设计契约**（design-only，未落地表/API） |

---

## 2. 未完成对象（均 design-only）

| 对象 | 缺口 | 阻塞项 |
| --- | --- | --- |
| **EmployeeTemplateCatalog** | 种子数据 exists；无 Admin 写 API（`/api/platform/employee-templates` 缺失） | 需 Phase-9 新增作者 API |
| **WorkflowTemplateCatalog** | 种子数据 exists；无 Admin 写 API（`/api/platform/workflow-templates` 缺失） | 需 Phase-9 新增作者 API |
| **PromotionRule** | 无表/无 API；本阶段红线**禁止实现** | 须 Phase-9C gate 解锁 |
| **TenantPricingPolicy** | 额度近似 `quotas` 可配；特殊价/折扣无结构化对象 | 需 Phase-9 引入策略对象 |
| **Plan.price 列** | `plans` 表**仍无 `price` 列**；订阅基底价依赖 `pricing_rules(subscription)` 占位派生 | 采用 PricingRule 方案 A（已落地），`price` 仅镜像可选 |
| **Connector 计量** | `connector_limit` 已在 QuotaRule 设计为第五类，但计量数据源未接入看板 | 须 G1 后 additive 扩展 |

---

## 3. 当前商业模型覆盖范围

**已覆盖（配置面 + 观测面）**：
- **Subscription 基底**：经 `PricingRule(subscription)` 配置化（价格权威）。
- **Token 超额**：经 `quota_rules(token_limit)` + `enforcement_mode` 语义（notify 默认）。
- **AI Employee Seat**：`EmployeeSeatPolicy` 设计 + `quota_rules(employee_seat_limit)` 观测基线。
- **Capability Package**：组合包配置（`capability_packages` + `pricing_reference`/`quota_reference`）。
- **Quota 五类**：`token_limit` / `employee_seat_limit` / `workflow_limit` / `capability_limit` / `connector_limit`（设计）。

**NOT 覆盖（须独立 gate）**：
- 真实出账 / **Payment** / **Invoice** / Billing 结算。
- **Marketplace** 上架与分润（G3 双签）。
- **Value Pricing** / ROI 度量。
- **Promotion 执行**（Phase-9C）。

---

## 4. 进入 Commercial Operation Console 开发条件评估

### 结论：**PASS（有条件）**

**论证（四支柱）**：
1. **配置面已具备**：Plan / PricingRule / QuotaRule / CapabilityPackage 均已结构化落地 + Admin API，运营可零代码配置；EmployeeSeatPolicy 设计契约已就位（落地待 Phase-9b）。
2. **运行实例面由 Workspace 提供**：`EmployeeInstance` / per-tenant `quotas` / `workflow_runs` / `usage_event` 由 Workspace 持有，Admin 以**读时聚合**只读观测（见 `phase9a-commercial-design-freeze.md` §2），控制台可基于二者**只读聚合展示**。
3. **红线满足、零资金风险**：本阶段全部为配置/观测，不触资金；六禁逐条满足。
4. **无收入风险**：当前不产生真实收入流（无出账/扣款/发票）。

**条件 / 范围声明**：
- PASS 范围限定于「**Commercial Operation Console 的只读聚合展示 + 配置面托管**」开发条件；不含真实出账/支付。
- **计费/支付须独立 gate**（建议 Phase-9b）解锁后，控制台方可接入资金动作；此前控制台对资金相关功能**保持只读/禁用**。
- `EmployeeSeatPolicy` / `EmployeeTemplateCatalog` / `WorkflowTemplateCatalog` / `PromotionRule` / `TenantPricingPolicy` 仍为 design-only——控制台对应"配置子模块"需在其各自 gate 落地后逐步开放。

---

## 5. 明天汇报（六点）

### 5.1 完成内容
- 撰写 `employee-seat-commercial-contract.md`：定义 `EmployeeSeatPolicy`（套餐级 AI 员工商业席位政策），含字段表、与 Phase-7.7 `EmployeeSeat` 实例视图的区分、商业规则、状态机、Admin/Workspace 边界、关联图、API 摘要、红线、待确认项。
- 撰写 `commercial-configuration-v1.md`：更新 Phase-8.6 八对象现状（PricingRule/QuotaRule/CapabilityPackage 由 `partial` 升为**已实现**），新增 `EmployeeSeatPolicy` 为第 9 对象，给出域边界与运营场景验证。
- 撰写本评估文档：Phase-9A 完成度评估 + 控制台开发条件 PASS（有条件）。

### 5.2 修改文件列表
- **新增** `docs/contracts/employee-seat-commercial-contract.md`
- **新增** `docs/contracts/commercial-configuration-v1.md`
- **新增** `docs/release/phase9a-commercial-configuration-status.md`
- 本次**无任何源码/表/测试变更**（纯文档会话）。

### 5.3 Commit 列表
- （见主理人交付总结）

### 5.4 测试结果
- 本会话**仅文档、零代码变更**，全仓既有测试 **439 passed 不受影响**（PricingRule / CapabilityPackage / QuotaRule 等 Phase-9A 既有实现测试已通过）。

### 5.5 风险
1. **EmployeeSeatPolicy 仍 design-only**：未落地表/API，控制台席位政策配置模块需等 Phase-9b 实现。
2. **`employee_type` 命名未打平**：Phase-7.7 实例用 `advanced`，本政策用 `enterprise`；跨层映射待确认（见 `employee-seat-commercial-contract.md` §10）。
3. **Plan.price 列缺失**：订阅基底价仍依赖 `pricing_rules` 占位派生，控制台订阅价展示需经 `pricing_reference` 聚合。
4. **Connector 计量待接入**：`connector_limit` 看板用量仍为占位，非真实计数。
5. **红线依赖人工 gate**：真实计费/支付须独立 gate（Phase-9b）解锁，否则控制台不得触达资金。

### 5.6 下一步建议
- **Phase-9b**：实现 `EmployeeSeatPolicy` 表 + Admin API；解锁**支付/发票独立 gate**（G2 席位计费 + 支付通道）。
- **打平枚举**：将 Phase-7.7 `employee_type` 的 `advanced` 更名为 `enterprise`，统一两层词汇。
- **Plan.price 镜像列评估**（可选 B 方案）：在 `pricing_rules(subscription)` 激活后同步镜像列，便于前端直显。
- **Connector 计量接入**：additive 扩展 `quotas` 表与 `derive_current_usage`，对齐五类。
- **控制台只读聚合先行**：基于现有配置面（Plan/PricingRule/QuotaRule/CapabilityPackage）+ Workspace 观测面，优先交付"配置托管 + 用量只读看板"，资金动作模块保留 gate 后开放。

---

*—— Phase-9A Commercial Configuration 完成度评估（纯文档·零代码）。配置面已具备、运行实例面由 Workspace 提供，结论 PASS（有条件）：具备进入 Commercial Operation Console 只读聚合 + 配置面托管开发条件；真实出账/支付须独立 gate。*
