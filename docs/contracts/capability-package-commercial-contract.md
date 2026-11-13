# Capability Package Commercial Contract（能力包商业配置契约）

> Phase-9A P2 —— 取代此前任何零散讨论，本文为 **Capability Package 商业配置的实体契约权威版**。
> 配套实现设计见 `docs/design/phase9a-p2-cappkg-implementation-design.md`。
> 与 `pricing-rule-contract.md` / `quota-rule-contract.md` 互补：本契约定义「能力包」这一**商业产品单元**，
> 其价格/配额经由 `pricing_reference` / `quota_reference` 指向 `plan_id` 派生。

---

## 1. 概述

Capability Package（能力包）是 Admin 可配置的**官方商业能力产品单元**。一个包把一组能力
（Capability / Connector / Workflow Template / Employee Template）打包，并关联其价格引用与配额引用，
供未来运营人员创建、调整、启用/停用。

**本契约范围**：仅商业配置（composition + 价格/配额引用 + 可用状态）。**不定义** Marketplace 上架、
支付、自动销售、租户安装逻辑——那些属于后续 gate 解锁的能力（见 §9）。

---

## 2. 实体字段

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `package_id` | TEXT | PK | 主键，`cp_` + uuid |
| `name` | TEXT | NOT NULL | 包名称（如「内容运营包」） |
| `description` | TEXT | DEFAULT '' | 包描述 |
| `capability_ids` | TEXT(JSON[]) | NOT NULL DEFAULT '[]' | 能力 key 数组（模型/工具/连接器能力） |
| `connector_ids` | TEXT(JSON[]) | NOT NULL DEFAULT '[]' | 连接器 key 数组（如 `xiaohongshu`/`douyin`/`shopify`） |
| `workflow_template_ids` | TEXT(JSON[]) | NOT NULL DEFAULT '[]' | 工作流模板 id 数组 |
| `employee_template_ids` | TEXT(JSON[]) | NOT NULL DEFAULT '[]' | 员工模板 id 数组 |
| `pricing_reference` | TEXT | NULLABLE | **价格引用**，指向 `plan_id`（价格来自该 plan 的 `pricing_rules`） |
| `quota_reference` | TEXT | NULLABLE | **配额引用**，指向 `plan_id`（配额来自该 plan 的 `quota_rules`） |
| `availability` | TEXT | CHECK IN (`public`,`tenant_invite_only`,`enterprise_only`) DEFAULT `public` | 商业可用范围 |
| `status` | TEXT | CHECK IN (`draft`,`active`,`disabled`) DEFAULT `draft` | 生命周期状态 |
| `created_at` / `updated_at` | TEXT | DEFAULT current_timestamp | 时间戳 |

> 与用户原始字段列表（`pricing_reference`/`quota_reference`/`status`）及商业规则段落的
> `package_price_reference`/`package_quota_reference`/`availability` 的对应关系：
> - 落库字段 `pricing_reference` ≡ 商业规则中的 `package_price_reference`
> - 落库字段 `quota_reference` ≡ 商业规则中的 `package_quota_reference`
> - 落库字段 `availability` 即商业规则中的 `availability`

---

## 3. Package 组成关系

一个 Capability Package 可包含四类引用（均以 **JSON 数组** 存于对应 TEXT 列，存 ID 列表）：

| 组成 | 引用实体 | 真实存法 | 示例 |
|------|----------|----------|------|
| **Capability** | 能力 key（无独立官方表，以字符串 key 存在，如 `plans.capabilities`） | `capability_ids` | `task_execution`、`workflow_sop`、`tenant_private_capabilities` |
| **Connector** | 连接器 key（统一 official capability catalog） | `connector_ids` | `xiaohongshu`、`douyin`、`shopify` |
| **Workflow Template** | `workflow_templates.id` | `workflow_template_ids` | `wt_content_prod` |
| **Employee Template** | `employee_templates.id` | `employee_template_ids` | `et_content_ops` |

**引用完整性策略**：Admin 配置时由应用层校验（数组必须为字符串列表）；**运行时不强制外键**——
包可引用尚未存在的模板 id（例如先发布包、后补模板），避免耦合。这与 `pricing_rules`/
`quota_rules` 的「配置即权威、运行读时聚合」哲学一致。

---

## 4. Package 商业规则

- **价格引用** `pricing_reference` → 指向某 `plan_id`，该 plan 的 `pricing_rules(subscription)` 即包的生效价。
- **配额引用** `quota_reference` → 指向某 `plan_id`，该 plan 的 `quota_rules` 即包的各类型额度。
- **可用状态** `availability`：
  - `public`：任何租户均可被指派/安装（未来 Marketplace 前的通用可用）。
  - `tenant_invite_only`：仅受邀租户可用。
  - `enterprise_only`：仅特定企业直供（如 Enterprise 定制包）。

> 本契约**不实现** BillingEvent 生成 / 超额收费 / Payment / Invoice / Marketplace / Value Pricing /
> 自动销售。上述引用仅为「配置」，不构成任何计费动作。

---

## 5. 状态机

```
draft ──activate──▶ active ──disable──▶ disabled
  ▲                      │                  │
  └──────── enable ──────┴──────────────────┘
```
- `draft`：编辑中，未对外可用。
- `active`：已发布为可用官方包。
- `disabled`：停用（保留历史，不物理删除）。
- `availability` 独立于 `status` 演进：一个 `active` 包可同时是 `enterprise_only`（仅企业可见）。

无「每 plan 仅一条 active」的覆盖语义（能力包允许多个并行 active），故无 `_expire` 类方法。

---

## 6. Admin 配置边界

| 角色 | 职责 | 本 Issue 是否实现 |
|------|------|------------------|
| **Admin（平台）** | 管理 **official capability package**：创建/修改/调价引用/启用停用 | ✅ 实现（`/api/platform/capability-packages`） |
| **Workspace（租户）** | 使用「已安装能力包」 | ❌ 本 Issue 仅明确边界，不实现安装/使用逻辑 |
| **tenant_private** | 租户私有能力（连接器/模型/工具） | ❌ 保持私有，不触碰 workspace private 路由/数据 |

> 边界红线：本 Issue 的所有读写都收敛到 `billing_store` 的 `capability_packages` 表与
> `/api/platform/*` 路由；**不修改** Workspace 执行链 / Credential Vault / Shared Contract /
> Employee Runtime / Usage Event 写入；**不触碰** `/api/workspace/*` private 路由。

---

## 7. 与 pricing_rules / quota_rules 的关联

```
CapabilityPackage
   ├── pricing_reference ──▶ plan_id ──▶ pricing_rules(plan_id)  [价格权威]
   └── quota_reference   ──▶ plan_id ──▶ quota_rules(plan_id)    [配额权威]
```
包本身**不持有价格数值/配额数值**，只持有「指向哪个 plan」的引用，从而复用 P0/P1 已建立的
价格与配额权威来源，避免重复定义、保证单一事实来源。

---

## 8. API 设计（摘要，详见实现设计稿）

全部端点受 `_require_platform_admin` 守卫（缺/错令牌 → **401**，非 403）：

| 方法 | 路径 | 说明 | 成功码 |
|------|------|------|--------|
| GET | `/api/platform/capability-packages` | 列表（query: `status`/`availability`/`name`） | 200 |
| POST | `/api/platform/capability-packages` | 创建 | 201 |
| GET | `/api/platform/capability-packages/{package_id}` | 获取单条 | 200 / 404 |
| PUT | `/api/platform/capability-packages/{package_id}` | 部分更新 | 200 / 404 / 422 |

错误映射：`ValueError`→422（非法枚举/空名）、`KeyError`→404（包不存在）。

---

## 9. 禁止清单（红线）

本 Issue **不实现**：
- Marketplace 上架 / 交易
- Payment / Invoice / BillingEvent 生成 / 超额收费
- 自动销售 / 销售系统
- Workspace 安装/使用能力包逻辑
- 任何对 Workspace 执行链 / Credential Vault / Shared Contract / Employee Runtime /
  Usage Event 写入的修改
- 对 `/api/workspace/*` private 路由的触碰

---

## 10. 验收映射

| 验收项 | 落点 |
|--------|------|
| 1. `capability-package-commercial-contract.md` | 本文 |
| 2. Package 数据模型说明 | §2 / §3 |
| 3. Capability/Connector/Workflow/Employee 关系说明 | §3 |
| 4. Admin 配置设计 | §6 / §8 |
| 5. 测试结果 | 全仓 439 passed（`test_capability_packages.py` 14 例） |
| 6. `git diff --check` | 提交 `feat(admin): add capability package commercial configuration` 通过 |
