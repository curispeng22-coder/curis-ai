# Phase-8 Billing MVP（Issue 草案）

> 纯规划文档，零代码、不实现任何系统。本 issue 界定 Billing MVP 的边界与就绪度，真实计费实现须 G1 gate 解锁。

## 1. Meta

| 字段 | 内容 |
| --- | --- |
| **Issue ID** | `ISSUE-PHASE8-BILLING-MVP` |
| **文件** | `issues/phase8_billing_mvp.md` |
| **Title** | Phase-8 Billing MVP |
| **Status** | `design-ready`（设计就绪；真实计费实现待 **G1 gate** 解锁） |
| **Owner Seat** | 系统交付席（实现交付）＋ 质量运行席（质量验证）；gate 批准：总控决策席；安全边界：安全边界席 |
| **类型** | 规划 / 边界界定（非实现） |

**依赖（Dependencies）**：
- **Phase-7.5 研究**：`usage_event` 能力评估与 Billing Readiness 评估 —— `docs/research/domain/billing-readiness-assessment.md`、`docs/research/domain/value-measurement-research.md`。
- **Phase-7.6 定价冻结**：Hybrid 商业模型冻结基线 —— `docs/contracts/pricing-contract.md`。
- **Phase-7.7 Admin 治理契约**：计费域技术契约 —— `docs/contracts/billing-domain-contract.md`；**Admin 治理契约见 `docs/contracts/admin-*-contract.md`**（由架构师并行产出，作为本 issue 的硬依赖引用；写 issue 时若尚未落盘，基于 `pricing-contract.md` + 研究自行推导 Admin 侧范围）。
- **关联研究**：`docs/research/domain/pricing-model-research.md`（Part B：Billing MVP 四构造 `plan` / `quota` / `billing_event` / `invoice` 蓝图）、`docs/research/domain/usage-billing-research.md`（技术计费机制）。

**前置 Gate（Prerequisite Gates）**：
- **G1（经济 / ROI 解锁 gate）**：真实计费**硬前置**。G1 解锁前，禁止自动扣费、配额阻断、折扣、ROI；真实计费（`billing_event` 进入 `issued` / `paid`、配额阻断生效、折扣引擎）须 G1 批准后开放。
- **G3（Marketplace gate）**：Marketplace 分成**硬前置**，须 G3 批准（本期不涉及）。
- **设计阶段已就绪**：契约 + 研究已完成，G1 前可先行启动「计量与规则配置（只读 / 草稿）」子阶段。

---

## 2. 目标

Billing MVP = **Admin 拥有的计费域最小可运行底座**，在严格保持 Workspace 运行时边界、不引入支付 / 发票 / 扣费的前提下，把 Hybrid 商业模型从「合同冻结」推进到「可观测、可配置、可计量」的 Admin 侧底座。

Gate 解锁后，Phase-8 须交付：
1. **Plan CRUD / 配置** —— 套餐（free / pro / enterprise）的创建、读取、更新、停用。
2. **Quota 配置 + 实时计数** —— token / seat / capability / workflow 配额的配置与用量实时计数（计数 ≠ 阻断）。
3. **Usage 只读聚合查询面板** —— 基于既有 `usage_event` 的租户用量统计（只读）。
4. **Billing Event 聚合 + 状态机** —— `billing_event` 的 `draft → calculated → issued → paid` 生命周期管理（G1 后完整开放）。

**关键约束**：这是计量与规则配置底座，**不是收入系统**。`usage_event.estimated_cost` 仅作估算信号，**非结算依据**；发票、支付、扣费、折扣、ROI 均不在本期。

---

## 3. Admin 侧范围（In-Scope）

### 3.1 Plan CRUD（套餐管理）
- Admin 拥有的 Plan 生命周期：`create` / `read` / `update` / `deprecate`。
- 字段对齐 `billing-domain-contract.md` Plan 契约：`plan_id`、`name`、`tier`（free / pro / enterprise）、`features`、`quota_rules`、`enabled`、`created_at`。
- 不破坏既有 `plan_tier` 契约（free / pro / enterprise 三档语义）。
- 参考 `pricing-contract.md` 套餐定义（Free / Pro / Enterprise 目标与商业含义）。

### 3.2 Quota 管理（配额配置 + 实时计数）
- 配额维度：`token_limit`、`employee_seat_limit`、`workflow_limit`、`capability_limit`（对应 `billing-domain-contract.md` Quota 契约）。
- 配置：为租户 / 套餐设定 `limit_value`、`period`（monthly / annual / custom / lifetime）。
- **实时计数**：`current_usage` 由 `usage_event` 聚合派生，须与期末重算一致；计数过程**不得 mutation 原始 `usage_event` 记录**。
- G1 前仅配置 + 计数（观测），**不执行配额阻断**（阻断属 G1 禁止区）。

### 3.3 Usage 查询（只读聚合）
- 只读聚合既有 `usage_event` 的用量统计面板：租户级 token / 模型调用 / workflow 运行 / task / employee / capability 归因聚合。
- 映射信号见 `billing-domain-contract.md` Usage Meter 契约（model / tool / connector / workflow / employee → `BillingSubject`）。
- 仅暴露脱敏字段（`credential_id` / `credential_ref_digest`），**不得暴露 `tenant_private` 明文凭证**。
- 不改动 `usage_event` schema，不新增运行时写路径。

### 3.4 Billing Event 管理（聚合 + 状态机）
- Admin 拥有的 `billing_event` 生成与生命周期管理。
- 字段对齐 `billing-domain-contract.md` Billing Event 契约：`billing_event_id`、`tenant_id`、`subject_type`、`subject_id`、`usage_source`、`amount`、`currency`、`status`、`created_at`。
- 状态机：`draft → calculated → issued → paid → cancelled`。
  - **G1 前**：允许生成 `draft` / `calculated`（只读 / 草稿阶段，供内部核对）。
  - **G1 后**：开放 `issued` / `paid`（`paid` 状态在计费域契约中保留，须 G1 解锁）。
- `billing_event` 可引用 `usage_event`；引用 `value_event` 仅限未来价值计费 gate。
- **禁止**在 `billing_event` 中写入明文凭证、原始 provider 敏感响应或 `tenant_private` 私密材料。

---

## 4. 明确不做（Out-of-Scope）

| 类别 | 说明 | Gate 状态 |
| --- | --- | --- |
| 支付系统 | 含自动扣费 / 支付网关集成 / 订阅扣款 | G1 前禁止（自动扣费属 G1 禁止区） |
| 发票系统 | `invoice` 单据生成、发票 UI、税计算（`Invoice` / `InvoiceLineItem` 保留为未来对象） | 本期不批准 |
| Marketplace 分成 | capability marketplace 收入分成 | 须 **G3** |
| Workspace 执行改动 | 任何 Workflow / Employee / Task Execution 运行时链路变更 | 禁止 |
| Credential Vault 改动 | 凭证库 schema / 安全边界变更 | 禁止 |
| Workflow 改动 | Workflow Runtime / 模板运行时变更 | 禁止 |
| tenant_private 管理 | `tenant_private` 明文凭证或私有套餐被提升为官方对象 | 禁止（须 marketplace / 治理 gate） |
| 折扣引擎 | discount / credit / overage 优惠计算 | G1 禁止区 |
| ROI / 价值计费系统 | 基于 `value_event` 的 ROI 分析与价值计费 | G1 禁止区 |
| 配额阻断 / 强制 | 用量超限时阻断 Workspace 执行 | G1 前禁止（G1 后可使能） |

> 上述边界与 `docs/contracts/billing-domain-contract.md`「Not Approved In Phase-7.7」保持一致，并在本期继续有效。

---

## 5. 任务切片建议

| 子任务 | 范围 | 前置 Gate | 依赖顺序 | 主要交付 |
| --- | --- | --- | --- | --- |
| **P8-1 Plan CRUD API** | Plan 创建 / 读取 / 更新 / 停用（free / pro / enterprise），不引入支付 | G1 前可启动（草稿 / 只读配置） | 无硬依赖，可与 P8-3 并行 | Plan 管理 API + 契约对齐（不破坏 `plan_tier`） |
| **P8-2 Quota 配置与实时计数** | token / seat / capability / workflow 配额配置 + 实时计数（计数不阻断） | G1 前可启动；配额阻断禁 | 依赖 P8-1（引用 `plan_id` 授予配额） | Quota 管理 API + 实时计数器（与期末重算一致） |
| **P8-3 Usage 只读聚合查询** | 聚合 `usage_event` 的租户用量统计面板（只读） | G1 前可启动（只读） | 无硬依赖（直接读 `usage_event`） | Usage 聚合查询 API + 面板（脱敏、租户隔离） |
| **P8-4 Billing Event 聚合与状态机** | `billing_event` 聚合 + `draft → calculated → issued → paid` 状态机 | `draft` / `calculated` 可 G1 前；`issued` / `paid` 须 **G1** | 依赖 P8-3（用量聚合）+ P8-1 / P8-2（plan / quota 规则） | Billing Event 聚合器 + 状态机 |

**推荐执行顺序**：
- **Stage A（G1 前 · 只读 / 草稿阶段）**：P8-3（Usage 聚合）→ P8-1（Plan）→ P8-2（Quota）→ P8-4 的 `draft` / `calculated` 部分。此阶段全部可交付且不构成真实计费。
- **Stage B（G1 后 · 真实计费阶段）**：开放 P8-4 的 `issued` / `paid`，并使能配额阻断（若 G1 授权）。折扣 / 支付 / 发票仍不在本期。

---

## 6. 与 Workspace 的职责边界

| 维度 | Workspace 拥有 | Admin（Billing MVP）拥有 |
| --- | --- | --- |
| 运行时执行 | 执行、workflow、employee / capability 归因 | — |
| 事件生产 | 写入 `usage_event`、`audit_event`；未来 `value_event`（须单独 gate） | — |
| 计费解释 | — | 生成 `billing_event`、Plan、Quota、未来 Invoice |
| 统计 / 配置 | — | 只读聚合 Usage 面板 + 规则配置 |
| 凭证 | `tenant_private` 归属租户，仅脱敏归因 | **不得读取 `tenant_private` 明文凭证** |

**硬性边界（任何子任务不得违反）**：
- Workspace 继续写入既有 `usage_event`；**Workspace 不写 `billing_event`、不生成发票**。
- Workspace 运行时**不得调用 `/api/platform/*`**（须通过扫描验证）。
- Admin **只读**脱敏用量证据，**不修改** WorkflowRun / EmployeeInstance / Credential Vault / Task Execution。
- 计费契约不得改变 Workflow、Employee Runtime、Credential Vault、Task Execution。
- `usage_event` / `audit_event` 保持不可变执行证据；计费聚合不得 mutation 原始记录。

---

## 7. 验收标准

**P8-1 Plan CRUD**
- [ ] Admin 可定义 Free / Pro / Enterprise 三档套餐，不破坏既有 `plan_tier` 契约语义。
- [ ] Plan 写操作仅限 Admin；Workspace 不写 Plan 记录（运行时 `/api/platform/*` 扫描通过）。
- [ ] 不引入任何支付 / 扣费 / 折扣字段。

**P8-2 Quota 配置与实时计数**
- [ ] 可为租户 / 套餐配置 token / seat / capability / workflow 配额（`limit_value` + `period`）。
- [ ] 实时计数 `current_usage` 与期末重算结果**一致**（误差 < 容差）。
- [ ] 计数过程不 mutation 原始 `usage_event` 记录。
- [ ] G1 前**不触发配额阻断**（仅观测 / 告警）。

**P8-3 Usage 只读聚合查询**
- [ ] 可基于既有 `usage_event` 聚合租户级用量（token / 模型调用 / workflow / task / employee / capability）。
- [ ] 响应**不暴露敏感字段**，仅含 `credential_id` / `credential_ref_digest` 脱敏归因。
- [ ] 租户隔离通过：跨租户查询返回空 / 拒绝。
- [ ] 不改动 `usage_event` schema，不新增运行时写路径。

**P8-4 Billing Event 聚合与状态机**
- [ ] 状态机 `draft → calculated → issued → paid → cancelled` 转移合法、可审计。
- [ ] `draft` / `calculated` 可在 G1 前生成；`issued` / `paid` **须 G1 解锁**后开放。
- [ ] `billing_event` 不含明文凭证、原始 provider 敏感响应或 `tenant_private` 私密材料（日志 / API 响应 / 测试输出均不含）。
- [ ] `estimated_cost` 显式标记为非权威计费金额，仅作估算信号。
- [ ] 计费聚合可引用 `usage_event`，但不反向改写它。

**通用（质量运行席验收）**
- [ ] Workspace 运行时 `/api/platform/*` 调用扫描通过。
- [ ] 租户隔离在全部计费查询中成立。
- [ ] 无明文凭证泄漏（代码 / 日志 / API / 测试）。
- [ ] 无 Workflow / Employee Runtime / Credential Vault / Task Execution 运行时行为变更。
- [ ] Admin / Workspace 边界与 `billing-domain-contract.md` 一致。

---

## 8. Phase-8 进入条件

**设计就绪（当前已满足）**：
- Phase-7.5 研究完成（`usage_event` 能力 + Billing Readiness 评估）。
- Phase-7.6 定价冻结完成（`pricing-contract.md`）。
- Phase-7.7 计费域契约完成（`billing-domain-contract.md`）；Admin 治理契约（`admin-*-contract.md`）由架构师并行产出并作为依赖引用。
- 商业模型（Hybrid：Plan + Token Usage + Capability Package + AI Employee Seat + Future Value Pricing）已冻结。

**真实计费实现进入条件（硬前置）**：
- **G1 gate 批准**（总控决策席）：解锁 `billing_event` `issued` / `paid`、配额阻断、自动扣费、折扣。
- **安全边界席**确认数据 / 安全边界（脱敏、租户隔离、`tenant_private` 不暴露）。
- **G3 gate** 仅当涉及 Marketplace 分成时才需要（本期不涉及）。

**建议的分阶段进入策略**：
- ✅ **现在可启动「计量与规则配置（G1 前只读 / 草稿）」阶段**：P8-1 + P8-2 + P8-3 全量，以及 P8-4 的 `draft` / `calculated` 部分。此阶段零收入风险、不越 gate。
- ⏳ **G1 解锁后再开放**：P8-4 `issued` / `paid`、配额阻断使能；折扣 / 支付 / 发票仍不在本期范围。

---

## 结论与下一步建议

1. **立项结论**：Phase-8 Billing MVP 设计就绪（`design-ready`），边界清晰，建议以本 issue 作为 Billing MVP 的规划基线。真实计费实现须 G1 gate 解锁，符合当前「经济 / ROI 禁止区」冻结。
2. **建议立即启动 G1 前子阶段**：优先交付 P8-3（Usage 只读聚合）+ P8-1（Plan）+ P8-2（Quota）+ P8-4 的 `draft` / `calculated`，在零收入风险下验证 Admin 侧计量与配置能力。
3. **路由与协作**：
   - 本 issue 提交**总控决策席**做 G1 gate 裁决（是否开放真实计费与配额阻断）。
   - 请求**安全边界席**确认数据 / 安全边界（脱敏、租户隔离）。
   - Admin 治理契约（`docs/contracts/admin-*-contract.md`）由架构师并行落盘，本 issue 已作为依赖引用；待其落盘后回填精确字段锚点。
   - Workspace 兼容性由**产品规划席**复核（确保 `/api/platform/*` 不被运行时调用、`usage_event` 不被 mutation）。
4. **不在本期**：支付、发票、Marketplace 分成（G3）、折扣（G1 禁止区）、ROI / 价值计费（G1 禁止区）、Workspace / Credential Vault / Workflow 运行时改动。

> 本文件为纯规划文档，零代码实现。所有实现动作须待对应 gate 批准后由系统交付席执行、质量运行席验证。
