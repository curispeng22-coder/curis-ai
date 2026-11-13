# Phase-9A 发布文档：Commercial Design Freeze + G1 Pre-Metering

> **阶段**：Phase-9A（Design Freeze + G1 Pre-Metering）
> **协作团队**：`software-phase9a-design-freeze`（主理人齐活林 / 架构师高见远 / 产品经理许清楚）
> **文档性质**：**纯设计冻结 + 验证规则发布，零代码**——不创建表、不修改源文件、不实现支付/计费。
> **目标**：将 Phase-8 Billing MVP（已实现，G1 通过）+ Phase-8.5 Commercial Readiness（已冻结契约）收敛为可发布的「商业设计冻结」规范，确认 Curis 已具备进入 G1 Billing Gate 的商业与计量条件。
> **汇编**：本文件由主理人齐活林汇编自两份专家产出——架构师《技术冻结设计》（`_draft_phase9a_freeze_design.md`）+ 产品经理《商业就绪验收》（`_draft_phase9a_g1_readiness.md`），并合并为单一权威发布源。

---

## 0. 范围与边界

| 项 | 说明 |
| --- | --- |
| 收口对象 | Hybrid 商业模式（Subscription + Token Usage + Capability Package + AI Employee Seat + Future Value Pricing）的**设计冻结**状态 |
| 本阶段硬禁止（六条） | 不收费 / 不支付 / 不生成真实 Invoice / 不自动扣款 / 不实现 Marketplace 分成 / 不实现 Value Pricing；Billing Simulation 仅内存投影，**不持久化为真实 billing_event** |
| G1 前置说明 | G1 Billing Gate（Plans + Token Quota 计量与配置授权）已在 **Phase-8 由工程/架构侧通过并进入开发**。本阶段从**商业 + 计量验证**视角完成「设计冻结收口」，**不重新裁决 G1 工程通过与否**。 |
| 不在本范围 | 真实出账 / 支付 / 发票 / 自动扣款子系统——须作为**独立 gate 子项**（建议 Phase-9b）单独裁决 |
| 对齐来源（引用不重定义） | `docs/contracts/pricing-package-contract.md` · `quota-rule-contract.md` · `billing-rule-contract.md` · `admin-plan-management-contract.md` · `admin-quota-contract.md` · `admin-capability-package-contract.md` · `pricing-contract.md` · `usage-value-event-boundary.md` · `docs/design/phase8-billing-mvp-design.md` · `docs/research/domain/curis-packaging-research.md` · `issues/phase85_commercial_readiness_review.md` |

---

## 1. 套餐定义（Plan Configuration 冻结）

> 三档与 Phase-8 `plans.plan_code ∈ {free, pro, enterprise}` **1:1 对齐** `tenants.plan_tier`；价格一律 `$XX` 占位（不写死、不触发资金动作，待总控决策席在 G1 出账激活前填充）。下表以 **Phase-8 已 seed 的权威实现值**为冻结基线。

### 1.1 三档冻结快照

| 字段 | Free | Pro | Enterprise | 落到 `plans` 的位置 |
| --- | --- | --- | --- | --- |
| **订阅基底价（占位 `$XX`）** | `$XX` | `$XX`（锚定，待定） | `$XX` / 议价 | 未来 `plans.monthly_price`（G1 禁止区；本期仅占位） |
| **AI Employee 席位上限** | 3 | 15 | 0 = 不限 | `quota_rules.seat_limit` |
| **Token 额度（月度·总量）** | 1,000,000 | 50,000,000 | 0 = 不限 | `quota_rules.token_monthly_limit` |
| **Workflow 额度（月度运行）** | **0 = 不限¹** | 50,000 | 0 = 不限 | `quota_rules.workflow_monthly_limit` |
| **Capability 来源白名单** | `[official]` | `[official, tenant_private]` | `[official, tenant_private, marketplace(占位)]` | `quota_rules.capability_sources` |
| **Connector 来源白名单** | `[official]`² | `[official]`² | `[official]`² | `capability_sources` + 未来 `connector_limit`（待接入） |
| **私有能力 tenant_private** | 禁止 | 允许（Admin 不读明文） | 允许（治理） | `capability_sources` 含 `tenant_private` |
| **Overage 单价（占位估算）** | 全 `$0` | token `$0.002`/1k · seat `$9` · wf `$0.01` · cap `$0` | 全 `$0`（包干） | `quota_rules.overage{...}`（**非权威估算**） |
| **重置周期** | monthly | monthly | annual | `plans.billing_interval` |
| **Feature 列表** | `task_execution`, `tenant_private_capabilities` | 上述 + `workflow_sop`, `admin_usage_observability` | 全量 + `team_management`, `priority_support` | `plans.features_json` |

¹ **待确认项（冻结对齐项 #1）**：Phase-8.5 `pricing-package-contract.md` §2 标注 Free workflow = **5,000**，但 **Phase-8 seed 实际写入 `workflow_monthly_limit=0`（= 不限）**。本冻结以 **seed 现状（0/不限）为冻结基线**，提交 G1 前决策席二选一核定（5,000 或 不限）。
² Connector 属 `capability_type=connector`，其计量数据源 Phase-8 未接入，本期仅作白名单占位（见 §2.5）。

### 1.2 `quota_rules_json` 冻结快照（与 Phase-8 seed 完全一致）

```json
// Free
{"token_monthly_limit":1000000,"seat_limit":3,"capability_sources":["official"],
 "workflow_monthly_limit":0,
 "overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},
 "currency":"USD"}

// Pro
{"token_monthly_limit":50000000,"seat_limit":15,"capability_sources":["official","tenant_private"],
 "workflow_monthly_limit":50000,
 "overage":{"token_unit_price_per_1k":0.002,"seat_unit_price":9,"workflow_unit_price":0.01,"capability_unit_price":0},
 "currency":"USD"}

// Enterprise
{"token_monthly_limit":0,"seat_limit":0,"capability_sources":["official","tenant_private","marketplace"],
 "workflow_monthly_limit":0,
 "overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},
 "currency":"USD"}
```

### 1.3 Capability 配置（official 白名单 / tenant_private 铁律 / marketplace 占位）

- **official 白名单**：Free/Pro/Enterprise 差异体现在可绑定的 `official` 能力包集合（starter / pro pack / 全量）；具体包经 `admin-capability-package-contract.md` 由 Admin 绑定到 Plan，Workspace 经 catalog 只读感知。
- **tenant_private 铁律**：Free 禁止；Pro/Enterprise 允许。**Admin 不 CRUD、不读取其明文**（`default_instructions`/`metadata_json`/`credential_ref` 不可见），仅经 `usage_event.capability_source='tenant_private'` 观测存在性与计量。
- **marketplace**：仅 Enterprise 白名单占位；治理/分润须 **G3 双签**，本期不实现。

### 1.4 Admin 生产可配置性（引用 Phase-8 端点）

下列端点均受 `_require_platform_admin` 守卫，Admin 已可在生产中配置 §1.1/§1.2 的全部项（无需改代码）：

| 操作 | 端点 |
| --- | --- |
| 创建 Plan | `POST /api/platform/plans`（`PlanCreateIn{plan_code,name,tier,features,quota_rules,...}`） |
| 修改 Plan | `PUT /api/platform/plans/{plan_id}` |
| 启用·停用 | `POST /api/platform/plans/{plan_id}/toggle`（`enable→active` / `disable→deprecated`） |

三档默认 Plan 已由 `database.initialize()` 幂等 seed（`INSERT OR IGNORE`），与 `tenants.plan_tier` 1:1 对齐。

---

## 2. 配额规则（Quota Simulation 模拟）

### 2.1 模拟语义总原则

- **仅计算与展示** `current_usage` vs `limit_value`，**不阻断执行**（无配额中间件、无 block）。
- 采用 **读时聚合（query-time aggregation）**：Admin 查询时由 `evolution_events` / `employee_instances` / `workflow_runs` 做 `GROUP BY + SUM/COUNT` 实时派生；与「期末从原始事件重算」同源，天然一致，且**不在 Workspace 执行链注入任何写入钩子**。
- 超额仅触发 **notify（看板预警）**；block / degrade 的真实拦截属 G1 后配额中间件（未来工程），本期仅语义展示。

### 2.2 读时聚合来源（`derive_current_usage`）

| quota_type | 计数来源（读时聚合 SQL 落点） |
| --- | --- |
| `token` | `evolution_events` where `event_type like 'usage.%'` → `sum(json_extract(payload,'$.total_tokens'))` |
| `employee_seat` | `employee_instances` where `tenant_id=? and enabled=1` → `count(*)` |
| `workflow` | `workflow_runs` where `tenant_id=? [and created_at between ? and ?]` → `count(*)` |
| `capability` | `evolution_events` where `capability_source ∈ plan.capability_sources` 白名单命中 → `count(*)` |
| `connector` | ⚠️ 待接入：`capability_type='connector'` 的计量数据源 Phase-8 未建 `connector_limit` 列 |

> 防御：若源表不存在，回退 `current_usage=0` 并在前端标「待数据源解禁」（实际 schema 中 `employee_instances` / `workflow_runs` 均已存在，可真实派生）。

### 2.3 四类 + connector 模拟展示字段

> 展示字段统一为：**已用 / 限额 / 利用率 / 是否预警**。`limit_value=0` 时利用率显示「不限」、预警「否」。

| quota_type | 计数来源 | 已用字段 | 限额字段 | 利用率 | 预警（阈值 ≥80%） | 本阶段可模拟性 |
| --- | --- | --- | --- | --- | --- | --- |
| `token` | usage_event.total_tokens | `sum(total_tokens)` | `token_monthly_limit` | 已用/限额 | ≥ 0.8 → 预警 | ✅ 可模拟 |
| `employee_seat` | employee_instances(enabled=1) | `count(活跃实例)` | `seat_limit` | 已用/限额 | ≥ 0.8 → 预警 | ✅ 可模拟 |
| `workflow` | workflow_runs | `count(运行)` | `workflow_monthly_limit` | 已用/限额 | ≥ 0.8 → 预警 | ✅ 可模拟 |
| `capability` | capability_source 白名单命中 | `count(命中事件)` | 白名单集合（无数值） | 展示来源分布 | 命中白名单外 → 准入预警 | ✅ 可模拟 |
| `connector` | connector 调用 | — | — | — | — | ⚠️ **待 connector 计量接入**（G1 后 / 待 `connector_limit` 扩展） |

### 2.4 Connector 计量待接入标注

`connector` 配额在 `quota-rule-contract.md` 已定义为第五类（`connector_limit`），但 **Phase-8 `quotas.quota_type` 仅含 token/employee_seat/capability/workflow 四短名，未建 `connector_limit` 列**，计量数据源（connector 调用计数）未接入。本冻结将其标注为 **「待 connector 计量接入」**：当前不在模拟看板展示真实用量，仅保留白名单占位；接入须 additive 扩展 `quotas` 表与 `derive_current_usage`，对齐 `billing-domain-contract.md` 五类。

---

## 3. 计量规则（Usage Meter Validation）

### 3.1 `usage_event → usage meter` 逐维度映射

计量字段全部来自 `evolution_events` 表列的 `tenant_id` 与 `payload` JSON（经 `_usage_event_from_row` 解析）。

| 维度 | 计量字段来源（对应 usage_event payload 字段） | 是否已可真实派生（对照 `usage_summary` 分组） | 验证结论 |
| --- | --- | --- | --- |
| **tenant** | `evolution_events.tenant_id`（表列，非 payload） | ✅ 作为**查询边界**必填；`usage_summary(tenant_id,...)` 以 `where tenant_id=?` 防跨租户 | ✅ 可计量（边界层，fail-closed） |
| **employee** | `payload.employee_id` | ✅ `usage_summary` 已 `group by employee_id`（`by_employee`） | ✅ 可计量 |
| **workflow** | `payload.workflow_run_id` | ✅ `usage_summary` 已 `group by workflow_run_id`（`by_workflow`） | ✅ 可计量 |
| **capability** | `payload.capability_source` | ✅ `usage_summary` 已 `group by capability_source`（`by_capability_source`）；`tenant_private` 仅作存在性标记 | ✅ 可计量 |
| **model** | `payload.model_name` | ✅ `usage_summary` 已 `group by model_name`（`by_model`） | ✅ 可计量 |

> `usage_summary` 的 `tenant` 不是分组维度而是**作用域（scope）**——所有分组均在 `tenant_id=?` 约束内完成，故 tenant 维度的「验证」落在查询边界（fail-closed）而非聚合分组。五维度均可真实派生。

### 3.2 tenant_id 缺失 → fail-closed（422）与脱敏铁律

- **fail-closed**：`GET /api/platform/usage/summary` 要求 `tenant_id` 必填，缺失返回 **422**；`calculate_billing_events` 在 `get_tenant(tenant_id)` 为 `None` 时抛错（→ 422/404），**禁止跨租户聚合**。
- **脱敏铁律**：用量 / 计量响应只暴露 `credential_id` / `credential_ref_digest`，**绝不返回 `tenant_private` 明文、`credential_vault` 内容、provider 原始密钥**；`tenant_private` 仅在 `capability_source` 维度作为存在性标记出现。
- **Value 不混入**：`usage_event` 不含 `value_type` / `estimated_value` / ROI 字段（见 `usage-value-event-boundary.md`），计量不计算 ROI。

---

## 4. Billing Simulation 规则（Billing 预览）

### 4.1 预览规则定义

`billing preview` = **纯只读内存投影**，展示：

1. **当前套餐**：`tenant.plan_tier → plans.quota_rules`（含 limits / overage 单价占位）；
2. **当前使用量**：经 `derive_current_usage` 读时聚合的四类用量；
3. **超额情况**：`overage = max(0, 已用 − limit)`（`limit=0` 即不限，无超额）；
4. **预计费用**：`amount = 超额 × plan.quota_rules.overage 单价`（**非权威估算**，与 Phase-8 `calculate_billing_events` 同口径）。

> 预览**不生成真实 Billing Event**、不写 `billing_events` 表、不触发任何资金动作。

### 4.2 与 `calculate_billing_events`（生成 draft）的区别

| 维度 | Billing 预览（本阶段定义） | `calculate_billing_events`（Phase-8 已实现） |
| --- | --- | --- |
| 持久化 | ❌ **不写库**，纯内存投影 | ✅ 写入 `billing_events`（status=`draft`/`calculated`） |
| 副作用 | 无 | 生成持久化记录（仍非真实出账） |
| 是否真实账单 | 否（仅投影） | 否（`issued` 仅占位、零资金副作用） |
| 计算口径 | `amount = 超额 × overage 单价` | 同左（同源 overage 单价） |

> 二者**计算口径同源**（超额 = max(0, 用量 − limit)；amount = 超额 × overage 单价），差异仅在**是否持久化**：预览是「看一眼的估算」，draft 是「落库的估算记录」。本冻结明确：**预览永远不落库**。

### 4.3 预览端点建议

- **G1 前最小改动方案**：前端直接对 `GET /api/platform/usage/summary` + `GET /api/platform/plans` 返回做内存投影（无需新端点）。
- **可选新增只读端点**：`GET /api/platform/billing-preview?tenant_id=`（受 `_require_platform_admin` 守卫，纯 SELECT 聚合 + 内存估算，**不 INSERT**）。
- 端点归属 `/api/platform/*`，沿用既有 Admin 鉴权，**不触碰 Workspace、不引入支付/发票/扣款**。

### 4.4 六禁边界声明

Billing 预览**不在六条禁止范围内**：无支付 / 无发票 / 无自动扣款 / 不生成真实 `billing_event`（仅内存投影）/ 不涉及 Marketplace 分成 / 不引用 `value_event`、不计算 ROI。

---

## 5. 当前禁止范围（六条核对）

| # | 禁止项 | 断言满足 | 落地保障（本冻结） |
| --- | --- | --- | --- |
| 1 | **不收费** | ✅ 满足 | overage 单价仅为占位/非权威估算；`issued` 状态零资金副作用；无出账作业 |
| 2 | **不支付** | ✅ 满足 | 无支付通道、无订阅扣款；订阅基底价仅 `$XX` 占位 |
| 3 | **不生成真实 Invoice** | ✅ 满足 | 不创建 `invoice` 实体；`billing_event` 仅计量/估算记录，不触发出账 |
| 4 | **不自动扣款** | ✅ 满足 | 无扣款作业；`set_billing_event_status` 仅更新状态列、零副作用 |
| 5 | **不实现 Marketplace 分成** | ✅ 满足 | `capability_sources` 含 `"marketplace"` 仅作 Enterprise 白名单占位；分润须 G3 双签，本期不实现 |
| 6 | **不实现 Value Pricing** | ✅ 满足 | `billing_event` 仅 `usage_event × quota_rules.overage`；不引用 `value_event`、不计算 ROI、不含 `value_type`/`estimated_value` |
| + | **Billing Simulation 不持久化 billing_event** | ✅ 满足 | 预览 = 纯内存投影；与 `calculate_billing_events`（落库 draft）明确区分，预览永不 INSERT |

---

## 6. G1 前准备状态

### 6.1 准备状态矩阵

| 准备项 | 状态 | 说明 |
| --- | --- | --- |
| 商业配置冻结 | ✅ 就绪 | 三档套餐配置已钉死为发布基线 |
| 计量验证 | ✅ 通过 | 五维度全可计量，fail-closed + 脱敏成立 |
| 模拟规则 | ✅ 就绪 | 配额模拟 + Billing 预览规则已定义（纯只读/内存） |
| 六禁合规 | ✅ 满足 | 六条 + 不持久化，逐条断言通过 |
| ⚠️ Free workflow 口径 | **待决策席核定（冻结对齐项 #1）** | seed=0（不限）vs 契约=5,000，G1 前二选一 |
| ⚠️ 价格/overage 最终数字 | **待决策席核定** | `$XX` 占位 + seed 现状估算值，G1 解锁前填充 |
| 🔜 Connector 计量 | 待接入 | `connector_limit` 列与数据源 G1 后 additive 扩展 |
| 🔜 block/degrade 真实拦截 | 未来工程 | G1 后配额中间件承担，本期仅语义展示 |

### 6.2 概念区分：G1 Gate vs 支付/发票子系统授权

| 维度 | G1 Billing Gate（本阶段范围） | 支付 / 发票子系统授权（未来·独立 gate 子项） |
| --- | --- | --- |
| 授权内容 | Plans + Token Quota 的**计量与配置能力** | 真实出账 / 支付通道 / 发票生成 / 自动扣款 |
| 状态 | ✅ 已通过（Phase-8） | ❌ 未授权（须 Phase-9b+ 单独裁决） |
| 资金动作 | 无（仅计量 + 估算占位） | 有（真实资金归集） |
| 风险 | 零资金风险 | 须独立安全 / 合规 / 财务裁决 |

> **铁律重申**：G1 通过 **≠** 支付授权。真实收款能力（payment / invoice / 自动扣款）必须作为**独立 gate 子项**单独裁决后方可落地，否则 Pro 自助无法真实收费（仅能「先计量后开票 / 承诺制」运行）。

---

## 7. 验收结论：确认 Curis 已具备进入 G1 Billing Gate 的条件

### 结论：**PASS（有条件）** —— 商业 + 计量视角已具备进入（并已满足）G1 Billing Gate 条件

**论证（四支柱）**：
1. **设计层（契约 + 实现）就绪**：三份商业契约 + 包装研究 + Phase-8 实现，逐字段对齐、口径一致；Hybrid 五要素设计冻结收口完成。
2. **计量验证通过**：Usage 五维度可派生、Billing 四类规则已定义、`calculate` 可生成 `draft/calculated` 预览。
3. **六禁全部满足（零资金风险）**：不收费/不支付/不生成真实 Invoice/不自动扣款/不实现 Marketplace 分成/不实现 Value Pricing —— 全部满足；所有金额仅作计量/非权威估算，`billing_event.issued` 仅状态占位、零资金副作用。
4. **无收入风险**：当前不产生任何真实收入流：无价格生效、无出账、无扣款、无发票。

### 条件 / 范围声明（须随交付一并记录）

1. **PASS 范围限定**：本 PASS 仅针对「进入 G1 Billing Gate（计费计量与配置授权）的商业条件」；G1 已由工程侧在 Phase-8 通过，本文档完成商业设计冻结收口。
2. **支付 / 发票不在 G1 范围**：真实出账 / 支付 / 发票 / 自动扣款须作为**独立 gate 子项**（建议 Phase-9b）单独裁决，G1 通过不等于支付授权。
3. **升级售卖须 gate 解锁**：席位真实计费（G2）/ 市场包（G3 双签）/ 部门行业包（L5）/ 价值计费（G4-L6 禁止区）均须各自 gate 解锁后方可售卖。
4. **Pro 锚定价待拍板**：`$XX` 占位须总控决策席在 G1 出账激活前确定（参考 Devin $20 / Notion $10）。
5. **Free Workflow 额度待对齐（冻结对齐项 #1）**：契约 §2（5,000）与 Phase-8 seed（0）须在冻结收口前对齐，属可快速关闭的收口项，不阻塞 G1。
6. **Connector 计量与配额硬阻断属未来工程**：不在本冻结范围，须 G1 后 additive 扩展。

### 待决策 / 开放问题

| # | 开放问题 | 建议 / 处置 | 是否阻塞 G1 |
| --- | --- | --- | --- |
| 1 | Pro 具体锚定价 | `$XX` 占位；参考区间 Devin $20 / Notion $10，总控决策席在 G1 出账激活前拍板 | 否 |
| 2 | payment / invoice 子系统授权路线 | 建议作为 **Phase-9b 独立 gate 子项**单独裁决 | 否（不在 G1 范围） |
| 3 | 升级售卖 gate 解锁路线 | 席位(G2) / 市场包(G3 双签) / 部门行业包(L5) / 价值(G4-L6) | 否（已锁定） |
| 4 | **Free Workflow 额度对齐** | 契约 5,000 vs seed 0，二选一核定（建议决策席） | 否（收口项） |
| 5 | 席位对外文案口径 | Free/Pro 的 `seat_limit` 现在仅观测，避免暗示「已计费」 | 否（GTM 规范） |

---

## 8. 商业上线建议雏形（承接 Phase-8.5）

### Phase-9a（现在）：零资金风险上线
- **Free**：低门槛获客 + 教育市场（1M token / 3 席 / official 基础能力），不含真实收费。
- **Pro（自助）**：以 **Token 超额计量预览**为主卖点（超额金额仅估算展示，**不真实扣费**）；`$XX` 锚定价待定；在 payment 落地前以「先计量后开票 / 承诺制」运行。
- **Enterprise（销售介入）**：包干年费描述 + 不限 token / 席位 + 集中管控，**包干不计量出账**。

> 三档现在即可以「Pro 自助 + Enterprise 销售介入」形态上线，**零资金风险**——G1 范围内的全部能力仅做计量 / 配置 / 预览，不触达资金。

### 后续 9b / 9c / 9d / 9e 路线

```
Phase-9a（现在·G1 已通过）→ Phase-9b（G2 席位计费 + 支付/发票独立 gate）
→ Phase-9c（G3 双签 Marketplace 分润）→ Phase-9d（L5 部门/行业包实例化）
→ Phase-9e（G4/L6 远景·价值计费禁止区）
```

---

*—— Phase-9A Commercial Design Freeze + G1 Pre-Metering 发布文档。由主理人齐活林汇编自架构师《技术冻结设计》与产品经理《商业就绪验收》。零代码、六禁满足、无收入风险。*
