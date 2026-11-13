# Phase-7.7 Billing Readiness Admin 评估 — 验收输出

> **评估阶段**：Phase-7.7 Billing Readiness Admin 评估（非 Billing 开发）
> **性质**：契约设计 / 治理边界界定 —— 零代码、不实现任何系统
> **团队**：`software-phase77-billing-readiness`（主理人齐活林编排；架构师高见远 + 产品经理许清楚）
> **已冻结背景**：Phase-7.6 冻结 Hybrid 商业模型（Subscription Plan + Token Usage + Capability Package + AI Employee Seat + Future Value Pricing）；G1 经济/ROI 禁止区当前生效

---

## 0. 验收结论速览

| # | 验收项 | 结论 |
| --- | --- | --- |
| 1 | Admin 商业治理契约 | ✅ 三份契约已交付（Plan / Quota / Capability Package），对齐既有 `pricing-contract.md` 等，**不重定义商业模型** |
| 2 | Billing MVP 边界 | ✅ `issues/phase8_billing_mvp.md` 已界定 In-Scope / Out-of-Scope，与 `billing-domain-contract.md`「Not Approved」一致 |
| 3 | Plan / Quota 模型建议 | ✅ 「模板(Admin 定义) → per-tenant 实例(派生)」两层结构；Plan `status` 四态机 + 版本化；配额实时计数 + 期末重算双轨 |
| 4 | Capability Package 治理建议 | ✅ 三态所有权矩阵（official→Admin / tenant_private→Workspace / marketplace→G3 后）；Admin 不介入 tenant_private |
| 5 | Phase-8 能否进入开发 | ⚠️ **设计层已就绪可进入设计冻结**；真实计费实现须 **G1 gate 硬前置**（总控决策席裁决 + 安全边界席确认），建议先启动 G1 前「计量与规则配置」子阶段 |

**一句话**：Curis 商业化架构与 Admin / Workspace 边界一致——Admin 负责"规则配置 + 只读计量 + 计费策略设计"，Workspace 负责"产生 usage_event / value_event + 自我约束执行"，双方通过 catalog 只读接口与 `*.changed` 事件解耦；真实计费落地须 G1 解锁。

---

## 一、Admin 商业治理契约

三份契约均位于 `docs/contracts/`，`Status: Phase-7.7 design only`，Owner 为 Admin Platform，结尾含「结论与 gate 边界」，且每份均含横切章节：**Usage/Billing 边界**、**严格禁止清单（六）**、**Phase-8 进入判定**。

### 1.1 `admin-plan-management-contract.md`（套餐治理）
- Admin 拥有 Plan 目录写权（CRUD + 生命周期）。
- **`plan_code` 与既有 `plan_tier` 标签 1:1 对齐**（`free`/`pro`/`enterprise`），保证现有 Admin 只读契约零改动；G1 后 additive 增加 `tenants.plan_id` 外键。
- `status` 流转 `draft → active → deprecated → archived`（不可跳变；重大修订先 deprecated 旧版再 active 新版，原子切换）。
- 新增 `billing_interval`、`version` 版本化（语义化）。
- Plan 变更经 **catalog 只读投影 + `plan.changed` 事件**通知 Workspace，**Admin 不回写、不接管执行**。
- 核心原则：**Plan 是"规则配置"不是"执行指令"**。

### 1.2 `admin-quota-contract.md`（配额治理）
- 四类配额统一「模板（Admin 定义于 Plan 内）→ per-tenant 实例（派生）」两层结构（erDiagram）。
- 逐类来源明确：`token ← usage_event`（现已可）/`employee_seat ← employee_instances`（Phase-4）/`capability ← capability_source 白名单`（marketplace 须 G3）/`workflow ← workflow_run`（Phase-6）。
- **双轨计数**：实时轻量计数（展示/预警）+ 期末从原始事件重算（与 `billing_event` 同源，保证对账权威）。
- **超限策略分级**：G1 前**仅计量与预警，不阻断、不计费**；阻断/超额计费属 G1 后实现，由独立配额中间件承担，Admin 不接管执行。

### 1.3 `admin-capability-package-contract.md`（能力包治理）
- **三态所有权矩阵（关键）**：`official → Admin`（CRUD + 绑定 Plan）；`tenant_private → Workspace/CEO`（Admin 不介入、不管理、不读取内容，仅经 `usage_event` 观测存在性与计量）；`marketplace → 未来 Admin 审核`（须 **G3 双签**，当前仅占位与边界声明）。
- official 包状态机 `draft → active(上架) → deprecated(下架) → archived`；绑定 Plan 为目录配置关系，不回写。
- marketplace 明确须经审核流程（tenant_private → 提交 → Admin 审核 → 双签 → 发布），**三态不可跨态直接修改**；`tenant_private` 不得未经审核直接成为 official。

---

## 二、Billing MVP 边界（`issues/phase8_billing_mvp.md`）

### 2.1 Admin 侧 In-Scope
| 范围 | 说明 | 阶段 |
| --- | --- | --- |
| Plan CRUD | free/pro/enterprise 创建/读取/更新/停用 | G1 前可启动 |
| Quota 配置 + 实时计数 | token/seat/capability/workflow 配额配置 + 用量实时计数（计数≠阻断） | G1 前可启动 |
| Usage 只读聚合查询 | 基于既有 `usage_event` 的租户用量统计面板（脱敏、租户隔离） | G1 前可启动 |
| Billing Event 状态机 | `draft → calculated → issued → paid` 生命周期（G1 前仅 draft/calculated） | draft/calculated G1 前；issued/paid 须 G1 |

### 2.2 明确不做（Out-of-Scope）
支付系统 / 发票系统 / Marketplace 分成(G3) / Workspace 执行改动 / Credential Vault 改动 / Workflow 改动 / tenant_private 管理 / 折扣引擎(G1 禁止区) / ROI 价值计费(G1 禁止区) / 配额阻断强制(G1 前禁止)。

> 边界与 `docs/contracts/billing-domain-contract.md`「Not Approved In Phase-7.7」完全一致，本期继续有效。

---

## 三、Plan / Quota 模型建议

- **两层结构**：Admin 在 Plan 内定义配额**模板**（规则配置）→ 租户绑定 Plan 时派生 **per-tenant 配额实例**（运行时计数载体）；`unique(tenant_id, period_start)` 每账期一行，保留历史可审计。
- **Plan 生命周期**：四态机 + 版本化，重大变更原子切换避免 Workspace 在线配置突变。
- **计数双轨**：实时计数供看板/预警（允许中途重置）；期末从原始事件重算为权威对账源（`billing_event` 不读 `current_usage`）。
- **G1 前 vs G1 后**：
  - G1 前：仅配置 + 只读统计 + 预警，**不阻断、不计费**（零收入风险）。
  - G1 后：配额阻断 + `billing_event` 超额聚合 + 自动扣费，由独立计费作业/端点承担，不并入现有 Admin 只读契约。

---

## 四、Capability Package 治理建议

- **治理分工铁律**：`official` 全局共享（tenant_id='platform'），Workspace 经 `/api/catalog/*` 只读；`tenant_private` 租户隔离，Admin 无 CRUD 端点、不可见配置内容（`default_instructions`/`metadata_json`/`credential_ref` 不可见）；`marketplace` 须经审核流程。
- **Admin 治理 official 包**：创建/编辑/上架/下架/绑定 Plan/版本；所有写操作触发 `capability.*` / `package.*` 审计事件（append-only）。
- **marketplace 占位**：本期不设计实现细节，明确须 G3 双签后进入 Admin 治理（审核队列 + 收益分成），`tenant_private` 不可未经审核直接成为 official。

---

## 五、Phase-8 是否可以进入开发

**结论：可以进入设计冻结，但实现分两阶段。**

| 阶段 | 前置 Gate | 内容 | 风险 |
| --- | --- | --- | --- |
| **阶段 A：计量与规则配置** | 无（G1 前可先行） | Plan CRUD + Quota 配置 + 实时计数 + Usage 只读聚合 + Billing Event `draft`/`calculated` + catalog 只读投影 | 零收入风险、不越 G1 禁止区 |
| **阶段 B：真实计费** | **G1 解锁**（席位须 Phase-4、工作流须 Phase-6、marketplace 须 G3） | `billing_event` issued/paid + 配额阻断 + 超额计费；独立计费作业/端点 | 须总控决策席裁决 + 安全边界席确认 |

**设计层就绪度**：Plan/Quota/Capability Package 三份契约 + Billing MVP issue 均已交付，与既有商业基线（`pricing-contract.md`）和事件边界（`usage-value-event-boundary.md`）一致，**可进入 Phase-8 设计冻结**。

**真实计费实现硬前置**：
1. **G1 gate 批准**（总控决策席）—— 解锁 `billing_event` issued/paid、配额阻断、自动扣费、折扣。
2. **安全边界席确认** —— 脱敏、租户隔离、`tenant_private` 不暴露。
3. G3 仅当涉及 Marketplace 分成时需要（本期不涉及）。

**建议下一步**：
- ✅ 现在即启动 Stage A（G1 前只读/草稿子阶段），在零收入风险下验证 Admin 侧计量与配置能力。
- ⏳ 将本 issue 提交**总控决策席**做 G1 gate 裁决，并请**安全边界席**确认数据/安全边界。
- ⏳ 待 G1 解锁后开放 Stage B。

---

## 六、严格禁止遵守确认

本阶段全部产出均遵守 Phase-7.7 严格禁止清单（六）：
1. ✅ 不开发 Billing 实现（未创建 `billing_event`/`invoice` 实体、未写计费逻辑）
2. ✅ 不开发支付（未实现扣费/支付通道/发票）
3. ✅ 不修改 Workspace（未改 `main.py`/`database.py`/`result_store.py`/`evolution_event_log.py`）
4. ✅ 不修改 Credential Vault
5. ✅ 不修改 Workflow
6. ✅ 不管理 `tenant_private` 私有能力（Admin 仅经 `usage_event` 观测）

**零代码改动**：本阶段仅新建 3 份契约 + 1 份 issue，未修改任何 `.py` 源文件、未创建任何数据库表、未触碰 Workspace/Credential Vault/Workflow。

---

## 七、交付文件清单

| 文件 | 作者 | 类型 |
| --- | --- | --- |
| `docs/contracts/admin-plan-management-contract.md` | 高见远（架构师） | Admin 套餐治理契约 |
| `docs/contracts/admin-quota-contract.md` | 高见远（架构师） | Admin 配额治理契约 |
| `docs/contracts/admin-capability-package-contract.md` | 高见远（架构师） | Admin 能力包治理契约 |
| `issues/phase8_billing_mvp.md` | 许清楚（产品经理） | Billing MVP issue 草案 |
| `issues/phase77_billing_readiness_review.md`（本文件） | 齐活林（主理人汇编） | 验收输出 |

---

## 结论

Phase-7.7 评估完成：**Curis 商业化架构与 Admin / Workspace 边界一致**。三份 Admin 治理契约 + Billing MVP issue 已交付，设计层就绪，可进入 Phase-8 设计冻结；真实计费实现须 G1 gate 解锁（总控决策席裁决 + 安全边界席确认），建议先启动 G1 前「计量与规则配置」子阶段以零风险验证 Admin 侧能力。

*—— Phase-7.7 Billing Readiness Admin 评估验收输出（纯评估，无代码）。*
