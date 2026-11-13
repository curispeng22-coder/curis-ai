# 用量计费 领域研究

> 范围：Curis Admin Platform 后续用量计费体系研究。基于 Phase-2 MVP（usage_event 多维查询）和 Phase-3.5 契约评审，研究 UsageEvent 字段设计、BillingEvent 字段设计、用量转账单方式、统计维度、第一版只做统计不做自动扣费的原因、plan_tier 标签与计费逻辑边界等。本文为纯研究文档，不写代码、不改现有文件。

---

## 现状分析

### Curis 当前用量计量架构

Curis Admin Platform 在 Phase-2（issue 065 / ADR-0028）已完成 usage_event 多维查询 MVP，核心架构如下：

**数据层**（`backend/app/evolution_event_log.py` + `backend/app/database.py`）：

UsageEvent 不独立建表，复用 `evolution_events` 表（append-only 事件日志），通过 `event_type like 'usage.%'` 过滤。`_usage_event_from_row` 方法将 payload 解包为扁平结构。

**当前 UsageEvent 字段**（从 payload 解包）：

| 字段 | 来源 | 说明 |
| --- | --- | --- |
| `id` | `payload.id` 或 `event_id` | 事件 ID |
| `task_id` | `payload.task_id` 或 `correlation_id` | 关联任务 |
| `tenant_id` | `evolution_events.tenant_id` | 租户 ID |
| `capability_type` | `payload.capability_type` 或 `payload.scope_type` | 能力类型（model/tool/connector） |
| `capability_id` | `payload.capability_id` 或 `payload.scope_ref` | 能力 ID |
| `capability_source` | `payload.capability_source` 或 `capability_ref.source` | 能力来源（official/tenant_private/marketplace） |
| `model_gateway_id` | `payload.model_gateway_id` | 网关 ID |
| `model_name` | `payload.model_name` | 模型名 |
| `prompt_tokens` | `payload.prompt_tokens` | 输入 token 数 |
| `completion_tokens` | `payload.completion_tokens` | 输出 token 数 |
| `total_tokens` | `payload.total_tokens` 或 `payload.token` | 总 token 数 |
| `estimated_cost` | `payload.estimated_cost` | 预估成本 |
| `status` | `payload.status` | 调用状态（success/failure/timeout 等） |
| `created_at` | `evolution_events.created_at` | 事件时间 |

**查询层**（`EvolutionEventLog.list_usage_events`）：

支持 7 维过滤（`tenant_id` / `capability_type` / `capability_source` / `model_gateway_id` / `model_name` / `status` / `since` / `until`），ORDER BY `created_at DESC`。

**API 层**（`backend/app/main.py`）：

- `GET /api/platform/usage`：Admin-only 只读计量，`tenant_id` 必填（fail-closed，禁止跨租户聚合），支持 7 维查询参数透传。

### 已有决策（ADR-0028）

1. **usage 投影纯计量**：`usage.*` 事件仅含计量数据（tokens/cost/status），无 `amount`/`currency`/`ROI`（G1 不触及）。
2. **G1 禁止区**：L5L6 经济/ROI 计算属禁止区，第一版只做统计，不做自动扣费、不做 ROI 计算、不做经济决策。
3. **fail-closed**：`tenant_id` 缺失 → 拒绝（422），不返回跨租户聚合。
4. **Admin 只读**：`/api/platform/usage` 仅 SELECT，绝不 INSERT/UPDATE/DELETE；Admin 不参与计费写入。
5. **capability_source 标记**：usage_event 通过 `capability_source` 字段标记能力来源（official/tenant_private/marketplace），支持按来源统计。
6. **`estimated_cost` 字段**：当前已有 `estimated_cost`（float），但仅为预估值，非账单金额。

### 当前痛点与未决项

1. **无 BillingEvent**：当前仅有 UsageEvent（计量），无 BillingEvent（账单）。用量如何转为账单未定义。
2. **`estimated_cost` 估值方式未定义**：当前 payload 可带 `estimated_cost`，但估值逻辑（按模型单价 × token 数）未在 Admin 侧实现，依赖 Workspace 执行层上报。
3. **plan_tier 标签未用于计费**：`tenants.plan_tier`（free/pro/enterprise）已有列，但仅作标签，不参与计费逻辑。
4. **无账期/结算周期**：无账单周期（日结/月结）概念，无法按周期聚合账单。
5. **无扣费/配额**：无自动扣费、无配额限制（用量超限阻断），仅做统计。
6. **跨租户 marketplace 计量未实现**：marketplace 能力的 usage 归属与收益分成须 G3 gate 解锁。

---

## 研究发现

### 行业最佳实践：用量计费体系

基于 AWS Bedrock / OpenAI API / Portkey / LiteLLM / New API 等平台的计费设计，主流用量计费体系分层：

#### 1. 事件层（UsageEvent）

记录单次调用的原始计量数据，append-only，不可变。

| 字段类别 | 字段示例 |
| --- | --- |
| 标识 | event_id, tenant_id, task_id, correlation_id |
| 能力 | capability_type, capability_id, capability_source, model_gateway_id, model_name |
| 计量 | prompt_tokens, completion_tokens, total_tokens, request_count, latency_ms |
| 成本 | estimated_cost, currency, unit_price |
| 状态 | status, error_code, error_message |
| 时间 | created_at, completed_at |

#### 2. 账单层（BillingEvent）

按账期聚合 UsageEvent，生成账单条目。

| 字段类别 | 字段示例 |
| --- | --- |
| 标识 | billing_id, tenant_id, billing_period_start, billing_period_end |
| 聚合 | total_requests, total_tokens, total_cost |
| 账单 | amount, currency, plan_tier, discount, final_amount |
| 状态 | status (draft/issued/paid/disputed) |
| 时间 | issued_at, paid_at |

#### 3. 配额层（Quota）

按租户/plan_tier 限制用量，超限阻断或告警。

| 字段类别 | 字段示例 |
| --- | --- |
| 标识 | tenant_id, plan_tier, quota_key |
| 限制 | daily_limit, monthly_limit, token_limit, request_limit |
| 当前 | current_usage, reset_at |
| 状态 | status (active/exceeded/paused) |

#### 4. 结算层（Settlement）

账单支付与结算。

| 字段类别 | 字段示例 |
| --- | --- |
| 标识 | settlement_id, billing_id, tenant_id |
| 支付 | payment_method, paid_amount, paid_at |
| 对账 | reconciliation_status, reconciled_at |

### Curis 当前层位

Curis 当前仅实现 **事件层（UsageEvent）**，且为只读统计（无配额、无账单、无结算）。这与 G1 禁止区约束一致：

| 层 | 当前状态 | G1 禁止区 | 未来扩展 |
| --- | --- | --- | --- |
| UsageEvent | ✅ 已实现（只读统计） | 不触及（纯计量） | 字段扩展 |
| BillingEvent | ❌ 未实现 | ⚠️ 触及（amount/currency） | G1 gate 解锁后 |
| Quota | ❌ 未实现 | ⚠️ 触及（经济决策） | G1 gate 解锁后 |
| Settlement | ❌ 未实现 | ⚠️ 触及（经济决策） | G1 gate 解锁后 |

### UsageEvent 字段建议

#### 当前字段评估

当前字段已覆盖核心计量维度，但存在以下改进点：

| 当前字段 | 评估 | 建议 |
| --- | --- | --- |
| `tenant_id` | ✅ 必填，租户隔离 | 保持 |
| `capability_type` | ✅ 三态能力类型 | 保持 |
| `capability_source` | ✅ 三态来源 | 保持 |
| `model_gateway_id` | ✅ 网关标识 | 保持 |
| `model_name` | ✅ 模型名 | 保持 |
| `prompt_tokens` | ✅ 输入 token | 保持 |
| `completion_tokens` | ✅ 输出 token | 保持 |
| `total_tokens` | ✅ 总 token | 保持 |
| `estimated_cost` | ⚠️ 估值方式未定义 | 建议增加 `currency` + `unit_price` 字段 |
| `status` | ✅ 调用状态 | 保持 |
| `created_at` | ✅ 事件时间 | 保持 |

#### 建议新增字段（additive，payload 内）

| 新增字段 | 类型 | 说明 | 前置 gate |
| --- | --- | --- | --- |
| `currency` | string | 货币代码（USD/CNY），默认 'USD' | 无（metadata） |
| `unit_price` | float | 单价（每千 token 价格），用于估算 | 无（metadata） |
| `latency_ms` | int | 调用延迟（毫秒） | 无（metadata） |
| `request_count` | int | 请求次数（单次调用=1，批量= N） | 无（metadata） |
| `error_code` | string | 错误码（status=failure 时） | 无（metadata） |
| `ceo_id` | string | CEO ID（关联 `governance_proposals.ceo_id`） | 无（metadata） |
| `department_type` | string | 部门类型（关联 `department_types.type_key`） | 无（metadata） |
| `employee_id` | string | 员工实例 ID（Phase-4 后，关联 `employee_instances.id`） | Phase-4 |

**说明**：
- `currency` + `unit_price` + `estimated_cost` 组合支持成本估算透明化，但非账单金额。
- `latency_ms` + `error_code` 支持质量统计（成功率/延迟分布）。
- `ceo_id` + `department_type` + `employee_id` 支持按组织维度统计用量。

#### 不建议新增的字段

| 字段 | 原因 |
| --- | --- |
| `amount` | 账单金额，属 BillingEvent 范畴，G1 禁止区 |
| `roi` | ROI 计算，L5L6 禁止区 |
| `profit` | 利润计算，L5L6 禁止区 |
| `payment_method` | 支付方式，属 Settlement 范畴 |

### BillingEvent 字段建议（G1 gate 相关）

BillingEvent 属账单层，须 G1 gate 解锁后方可实现。以下为设计建议：

#### 数据模型

BillingEvent 须独立建表（不复用 `evolution_events`），因其有状态机（draft → issued → paid → disputed），与 append-only 事件日志语义不同。

```sql
create table if not exists billing_events (
  billing_id           text primary key,
  tenant_id            text not null,
  billing_period_start text not null,
  billing_period_end   text not null,
  plan_tier            text not null default 'free',
  total_requests       integer not null default 0,
  total_tokens         integer not null default 0,
  total_cost           real not null default 0,
  currency             text not null default 'USD',
  discount             real not null default 0,
  final_amount         real not null default 0,
  status               text not null default 'draft'
                         check (status in ('draft','issued','paid','disputed','void')),
  issued_at            text,
  paid_at              text,
  created_at           text not null default current_timestamp,
  updated_at           text not null default current_timestamp
);
create index if not exists idx_billing_events_tenant_period
  on billing_events(tenant_id, billing_period_start);
```

#### 字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `billing_id` | text PK | 账单 ID |
| `tenant_id` | text | 租户 ID |
| `billing_period_start` | text | 账期开始（如 '2026-07-01'） |
| `billing_period_end` | text | 账期结束（如 '2026-07-31'） |
| `plan_tier` | text | 租户 plan_tier（free/pro/enterprise） |
| `total_requests` | int | 总请求数（聚合 UsageEvent） |
| `total_tokens` | int | 总 token 数（聚合） |
| `total_cost` | real | 总成本（聚合 estimated_cost） |
| `currency` | text | 货币 |
| `discount` | real | 折扣（按 plan_tier） |
| `final_amount` | real | 最终金额（total_cost - discount） |
| `status` | enum | 账单状态机 |
| `issued_at` | text | 开票时间 |
| `paid_at` | text | 支付时间 |

#### 状态机

```
draft → issued → paid
         ↓         ↓
      disputed   void
```

- `draft`：账期结束自动生成草稿。
- `issued`：Admin 审核后开票。
- `paid`：支付完成。
- `disputed`：租户异议。
- `void`：作废。

#### G1 gate 解锁条件

- **解锁条件**：总控决策席 gate。
- **须确认**：账单周期（日结/月结）；折扣规则（plan_tier 对应折扣）；货币策略；支付方式；是否自动扣费。
- **解锁后**：新增 `billing_events` 表 + `/api/platform/billing` 端点 + 账单生成作业。

### 用量如何从 usage_event 转为账单

#### 转换流程

```
UsageEvent（append-only 事件日志）
    ↓ 按账期聚合（tenant_id + billing_period）
BillingEvent（draft 草稿）
    ↓ Admin 审核 + 折扣计算
BillingEvent（issued 开票）
    ↓ 支付
BillingEvent（paid 已付）
```

#### 聚合逻辑

```python
def aggregate_usage_to_billing(tenant_id: str, period_start: str, period_end: str) -> dict:
    """按账期聚合 UsageEvent，生成 BillingEvent 草稿。"""
    usage_events = event_log.list_usage_events(
        tenant_id=tenant_id,
        since=period_start,
        until=period_end,
    )
    return {
        "tenant_id": tenant_id,
        "billing_period_start": period_start,
        "billing_period_end": period_end,
        "total_requests": len(usage_events),
        "total_tokens": sum(e["total_tokens"] for e in usage_events),
        "total_cost": sum(e["estimated_cost"] for e in usage_events),
        "status": "draft",
    }
```

#### 注意事项

1. **幂等性**：同一账期多次聚合应生成同一 BillingEvent（用 `idempotency_key = tenant_id + period`）。
2. **status 过滤**：聚合时是否排除 `status=failure` 的事件？建议默认计入（成本已发生），但标注 `failed_requests` 数量。
3. **currency 统一**：若 UsageEvent 有多种 currency，聚合时须按汇率统一（G1 gate 后定义）。
4. **marketplace 分成**：marketplace 能力的 usage 须按分成规则计算（G3 gate 后定义）。

### 按租户、模型、能力来源、时间统计的方式

#### 当前统计能力

`/api/platform/usage` 支持 7 维过滤，可组合查询：

| 统计维度 | 查询参数 | 示例 |
| --- | --- | --- |
| 按租户 | `tenant_id` | 某租户全部用量 |
| 按能力类型 | `capability_type` | 某租户的 model 用量 |
| 按能力来源 | `capability_source` | 某租户的 official vs tenant_private 用量 |
| 按网关 | `model_gateway_id` | 某租户经 newapi 网关的用量 |
| 按模型 | `model_name` | 某租户的 gpt-4o 用量 |
| 按状态 | `status` | 某租户的成功/失败用量 |
| 按时间 | `since` + `until` | 某租户某时段用量 |

#### 建议新增统计 API

当前 `/api/platform/usage` 返回原始事件列表，无聚合统计。建议新增聚合统计端点：

```
GET /api/platform/usage/summary?tenant_id=X&since=...&until=...&group_by=model_name
```

返回：
```json
{
  "tenant_id": "X",
  "period": {"since": "...", "until": "..."},
  "group_by": "model_name",
  "groups": [
    {"key": "gpt-4o", "total_requests": 100, "total_tokens": 50000, "total_cost": 1.5},
    {"key": "claude-3", "total_requests": 50, "total_tokens": 30000, "total_cost": 0.9}
  ],
  "grand_total": {"total_requests": 150, "total_tokens": 80000, "total_cost": 2.4}
}
```

支持 `group_by` 参数：`capability_type` / `capability_source` / `model_gateway_id` / `model_name` / `status` / `day` / `week` / `month`。

#### 统计实现方式

- **实时聚合**：直接对 `evolution_events` 表 SQL 聚合（`GROUP BY` + `SUM`）。数据量小时可行。
- **预聚合**：定期（日/小时）将 UsageEvent 聚合到 `usage_daily_summary` 表，查询时读预聚合表。数据量大时必要。

**建议**：第一版实时聚合（SQLite 单租户数据量可控），未来数据量增长后引入预聚合表。

### 第一版只做统计，不做自动扣费的原因（G1 禁止区）

#### G1 禁止区定义

ADR-0028 G1 禁止区明确：L5L6 经济/ROI 计算属禁止区。自动扣费涉及经济决策，属禁止区核心。

#### 自动扣费为何属 G1 禁止区

| 自动扣费环节 | 为何属禁止区 |
| --- | --- |
| 账单金额计算 | 涉及单价 × token 数，属经济计算 |
| 折扣规则 | 涉及 plan_tier 对应折扣，属经济决策 |
| 支付通道集成 | 涉及第三方支付，属经济操作 |
| 配额阻断 | 涉及"超限阻断"决策，属经济决策 |
| 退款/争议处理 | 涉及经济操作 |

#### 第一版只做统计的合理性

1. **契约先行**：UsageEvent 字段已定义并支持多维查询，为未来计费积累数据。
2. **低成本路径**：统计无经济风险，不触碰 G1 禁止区。
3. **价值验证**：先验证用量统计对 Admin/租户的价值，再决定是否进入计费。
4. **gate 解锁后可平滑扩展**：UsageEvent 数据已积累，G1 gate 解锁后只需新增 BillingEvent 表 + 聚合逻辑，不改动既有数据。

#### 解锁 G1 gate 后的能力扩展

| 能力 | 前置 gate | 实现方式 |
| --- | --- | --- |
| BillingEvent 账单 | G1 gate | 独立表 + 聚合作业 |
| 配额阻断 | G1 gate | Quota 表 + 中间件检查 |
| 自动扣费 | G1 gate + 支付集成 | Settlement 表 + 支付通道 |
| 折扣规则 | G1 gate | plan_tier → 折扣映射 |
| 退款/争议 | G1 gate | BillingEvent 状态机 |

### plan_tier 标签 vs 计费逻辑的边界

#### 当前 plan_tier 定位

`tenants.plan_tier`（free/pro/enterprise）已有列，但仅作**标签**，不参与任何计费逻辑：

- Admin 可查看/编辑租户的 plan_tier（`/api/platform/tenants`）。
- Admin 可按 plan_tier 筛选租户（客户端筛选）。
- plan_tier 不影响 usage 查询、不影响能力访问、不影响配额。

#### plan_tier 标签边界

| 用途 | 当前是否支持 | 前置 gate |
| --- | --- | --- |
| 租户分类标签 | ✅ | 无 |
| 按 plan_tier 筛选租户 | ✅（客户端） | 无 |
| 按 plan_tier 统计用量 | ⚠️（须 join tenants 表） | 无 |
| 按 plan_tier 限制能力访问 | ❌ | G1 gate |
| 按 plan_tier 计算折扣 | ❌ | G1 gate |
| 按 plan_tier 设置配额 | ❌ | G1 gate |

#### plan_tier 不参与计费逻辑的原因

1. **G1 禁止区**：plan_tier → 折扣/配额属经济决策，须 G1 gate 解锁。
2. **避免隐式行为**：若 plan_tier 影响能力访问，Admin 编辑 plan_tier 会产生隐式副作用，违反"元数据管理"边界。
3. **显式优于隐式**：能力访问控制应显式（`capability_source` + `status`），而非隐式（plan_tier 派生）。

#### G1 gate 解锁后的 plan_tier 计费逻辑

解锁后 plan_tier 可参与：

| plan_tier | 折扣 | 配额 | 能力访问 |
| --- | --- | --- | --- |
| free | 0% | 1000 tokens/day | official only |
| pro | 10% | 100000 tokens/day | official + marketplace |
| enterprise | 20% | unlimited | all（含 tenant_private） |

**注意**：此表仅为示例，实际规则须 G1 gate 解锁后由总控决策席定义。

---

## 设计建议

### 数据模型建议

#### 1. UsageEvent 字段扩展（additive，payload 内）

当前 UsageEvent 复用 `evolution_events` 表，字段在 payload 内。建议 additive 扩展 payload 字段：

| 新增字段 | 类型 | 说明 | 前置 gate |
| --- | --- | --- | --- |
| `currency` | string | 货币代码（USD/CNY） | 无 |
| `unit_price` | float | 单价（每千 token） | 无 |
| `latency_ms` | int | 调用延迟 | 无 |
| `error_code` | string | 错误码 | 无 |
| `ceo_id` | string | CEO ID | 无 |
| `department_type` | string | 部门类型 | 无 |
| `employee_id` | string | 员工实例 ID | Phase-4 |

**实现方式**：Workspace 执行层在上报 usage_event 时携带这些字段；`_usage_event_from_row` 解包时增加对应字段。DB schema 不变（payload 是 JSON text）。

#### 2. BillingEvent 表（G1 gate，待实现）

独立建表，不复用 `evolution_events`（有状态机，非 append-only）。见上方"BillingEvent 字段建议"小节。

#### 3. usage_daily_summary 预聚合表（未来，数据量大时）

```sql
create table if not exists usage_daily_summary (
  summary_id   text primary key,
  tenant_id    text not null,
  summary_date text not null,
  capability_source text,
  model_name   text,
  total_requests integer not null default 0,
  total_tokens   integer not null default 0,
  total_cost     real not null default 0,
  created_at     text not null default current_timestamp,
  unique(tenant_id, summary_date, capability_source, model_name)
);
```

**触发时机**：数据量增长导致实时聚合性能下降时引入；定期（日）聚合 UsageEvent 写入此表。

### API 设计建议

#### 1. 用量统计 API（已有，保持稳定）

- `GET /api/platform/usage`：7 维查询，返回原始事件列表。保持不变。

#### 2. 用量聚合统计 API（建议新增）

```
GET /api/platform/usage/summary?tenant_id=X&since=...&until=...&group_by=model_name
```

返回按 `group_by` 维度聚合的统计结果（见上方"按租户、模型、能力来源、时间统计的方式"小节）。

**鉴权**：`_require_platform_admin`。
**fail-closed**：`tenant_id` 必填，禁止跨租户聚合。

#### 3. 账单 API（G1 gate，待实现）

```
GET    /api/platform/billing                    # 账单列表（按 tenant_id + period）
POST   /api/platform/billing/generate           # 手动触发账单生成（Admin）
GET    /api/platform/billing/{billing_id}       # 账单详情
POST   /api/platform/billing/{billing_id}/issue # 开票（Admin）
POST   /api/platform/billing/{billing_id}/mark-paid  # 标记已付（Admin）
```

#### 4. 配额 API（G1 gate，待实现）

```
GET    /api/platform/tenants/{tenant_id}/quota  # 查询配额
PUT    /api/platform/tenants/{tenant_id}/quota  # 设置配额（Admin）
```

### 边界规则

#### 1. Admin 用量观测边界

| 规则 | 说明 |
| --- | --- |
| Admin 只读 usage | `/api/platform/usage` 仅 SELECT，不写 |
| fail-closed | `tenant_id` 必填，禁止跨租户聚合 |
| 纯计量 | 仅 tokens/cost/status，无 amount/currency/ROI |
| 不自动扣费 | G1 禁止区，第一版只做统计 |

#### 2. UsageEvent vs BillingEvent 边界

| 维度 | UsageEvent | BillingEvent |
| --- | --- | --- |
| 性质 | append-only 事件 | 有状态机账单 |
| 载体 | `evolution_events`（复用） | `billing_events`（独立表） |
| 写入方 | Workspace 执行层 | Admin（G1 gate 后） |
| 读取方 | Admin 只读 | Admin + 租户 |
| 字段 | 计量数据 | 账单数据（amount/currency/discount） |
| G1 禁止区 | 不触及 | 触及（G1 gate） |

#### 3. plan_tier 标签边界

| 规则 | 说明 |
| --- | --- |
| 当前仅标签 | 不参与计费逻辑 |
| G1 gate 解锁后 | 可参与折扣/配额/能力访问 |
| 显式优于隐式 | 能力访问用 `capability_source` 显式控制，非 plan_tier 派生 |

#### 4. 账期与结算边界

| 规则 | 说明 |
| --- | --- |
| 账期 | G1 gate 后定义（日结/月结） |
| 幂等 | 同一账期多次聚合生成同一账单 |
| 状态机 | draft → issued → paid → disputed → void |
| 货币 | G1 gate 后定义汇率策略 |

---

## 前置条件

### G1 gate（经济/ROI 计算）

- **解锁条件**：总控决策席 gate。
- **须确认**：账单周期；折扣规则（plan_tier 对应）；货币策略；支付方式；是否自动扣费；配额阻断规则；退款/争议流程。
- **解锁后**：新增 `billing_events` 表 + `/api/platform/billing` 端点 + 账单生成作业 + 配额中间件。

### G3 gate（Marketplace 跨租户计费）

- **解锁条件**：总控决策席 + 安全边界席双签。
- **须确认**：marketplace 能力的 usage 归属（提供方 vs 消费方）；收益分成规则；跨租户账单拆分。
- **解锁后**：BillingEvent 增加 `marketplace_revenue_share` 字段；账单生成时按分成规则计算。

### Phase-4 gate（员工维度统计）

- **解锁条件**：Phase-4 员工系统 gate（C1 解禁）。
- **须确认**：UsageEvent 携带 `employee_id`；按员工维度统计用量。
- **解锁后**：UsageEvent payload 增加 `employee_id` 字段；`/api/platform/usage` 支持 `employee_id` 查询维度。

### 数据量增长 gate（预聚合）

- **解锁条件**：实时聚合性能下降（SQLite 单租户事件数 > 10万）。
- **须确认**：预聚合周期（日/小时）；预聚合表设计；增量更新策略。
- **解锁后**：新增 `usage_daily_summary` 表 + 预聚合作业。

---

## 结论

1. **UsageEvent 当前字段已覆盖核心计量维度**：7 维查询（tenant_id/capability_type/capability_source/model_gateway_id/model_name/status/since/until）满足 MVP 统计需求。建议 additive 扩展 `currency`/`unit_price`/`latency_ms`/`error_code`/`ceo_id`/`department_type`/`employee_id` 字段，支持更细粒度统计。

2. **BillingEvent 须独立建表**：账单有状态机（draft→issued→paid→disputed→void），与 append-only 事件日志语义不同，不可复用 `evolution_events`。字段包括 `billing_id/tenant_id/billing_period/plan_tier/total_requests/total_tokens/total_cost/currency/discount/final_amount/status`。

3. **用量转账单流程**：UsageEvent → 按账期聚合 → BillingEvent(draft) → Admin 审核 → BillingEvent(issued) → 支付 → BillingEvent(paid)。聚合须幂等（`idempotency_key = tenant_id + period`），须处理失败请求计入、currency 统一、marketplace 分成（G3 gate）。

4. **第一版只做统计不做自动扣费是正确选择**：G1 禁止区明确 L5L6 经济/ROI 计算属禁止区，自动扣费涉及账单金额计算、折扣规则、支付通道、配额阻断，均属经济决策。统计无经济风险，且为未来计费积累数据，gate 解锁后可平滑扩展。

5. **plan_tier 当前仅作标签，不参与计费逻辑**：plan_tier → 折扣/配额/能力访问属经济决策，须 G1 gate 解锁。当前能力访问用 `capability_source` 显式控制，而非 plan_tier 派生，避免隐式副作用。

6. **建议新增用量聚合统计 API**：当前 `/api/platform/usage` 返回原始事件列表，无聚合。建议新增 `GET /api/platform/usage/summary?group_by=...`，支持按 `capability_type/capability_source/model_gateway_id/model_name/status/day/week/month` 聚合，返回 `grand_total`。

7. **预聚合表留待数据量增长后引入**：第一版实时聚合（SQLite 可控），未来事件数 > 10万时引入 `usage_daily_summary` 预聚合表 + 定期作业。

8. **marketplace 计费须 G3 gate**：跨租户能力共享的 usage 归属与收益分成须 G3 gate 解锁，BillingEvent 须增加 `marketplace_revenue_share` 字段，账单生成时按分成规则计算。
