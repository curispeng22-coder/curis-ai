# Phase-9A P1 QuotaRule Configuration — 实现设计文档

> 本文件是 `docs/contracts/quota-rule-contract.md`（QuotaRule 实体契约）的**实现设计**。仅做架构设计 + 落盘契约/设计文档；**不写实现代码、不写测试**（测试矩阵为给工程师的规格，非已执行）。
> 作者：架构师 高见远（software-architect）

---

## 0. 概述

| 项 | 内容 |
| --- | --- |
| Issue | Phase-9A P1：**QuotaRule Configuration**（计划级配额规则 Admin 可配置） |
| 目标 | 新增 `quota_rules` 表作为计划级配额**权威来源**；提供 Admin CRUD API；seed 三档套餐各 5 类 active 规则 |
| 设计哲学 | 配额不写死进 Plan 表列（对齐 P0「价格不写死 Plan」）；`quota_rules(plan_id)` 权威，per-tenant `quotas` 实例层不变 |
| 参考风格 | P0 `pricing_rules`（建表 / 7 方法 Store / 4 路由 main.py / `_require_platform_admin` 守卫） |

### 红线 / 禁止清单（本 Issue 必须严守）
- ❌ 不实现 BillingEvent 生成 / 超额收费 / Payment / Invoice / Marketplace / Value Pricing
- ❌ 不修改 Workspace 执行链 / Credential Vault / Shared Contract / Employee Runtime / Usage Event 写入
- ❌ 不硬编码套餐限制值为不可改（默认 seed 仅为**可覆盖占位**）
- ❌ 不修改 `quotas` 实例表结构（仅确认边界）

---

## 1. `quota_rules` 表 DDL

与 `pricing_rules` 同区（Phase-8 Billing 表簇），`create table if not exists` 保证幂等；部分唯一索引强制「每 `plan_id+quota_type` 仅一条 active」。

```sql
create table if not exists quota_rules (
  quota_rule_id    text primary key,
  plan_id          text not null,
  quota_type       text not null
                    check (quota_type in
                      ('token_limit','employee_seat_limit','workflow_limit',
                       'capability_limit','connector_limit')),
  limit_value      integer,                       -- NULL = 不限（配合 is_unlimited）
  is_unlimited     integer not null default 0,    -- 0/1
  period           text not null default 'monthly'
                    check (period in ('daily','monthly','annual','none')),
  enforcement_mode text not null default 'notify'
                    check (enforcement_mode in ('notify','throttle','block','billing_only')),
  status           text not null default 'draft'
                    check (status in ('draft','active','disabled')),
  source_scope_json text not null default '[]',   -- 准入型专用，数值型恒 '[]'
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

-- 每 (plan_id, quota_type) 仅一条 active（部分唯一索引，DB 层强制）
create unique index if not exists idx_quota_rules_plan_type_active
  on quota_rules(plan_id, quota_type) where status = 'active';

-- 列表/按 plan 查询加速
create index if not exists idx_quota_rules_plan on quota_rules(plan_id);
create index if not exists idx_quota_rules_status on quota_rules(status);
```

**列 / 约束说明**：
- `quota_type` CHECK 预置 5 类（含 `connector_limit`），未来无需再 ALTER。
- `limit_value` 允许 `NULL`（不限量）；`is_unlimited=1` 时其值无效。二者并存（满足契约「NULL 或 is_unlimited 标记」）。
- `source_scope_json` 准入型（capability/connector）存白名单 `['official'|'tenant_private'|'marketplace']`；数值型恒 `[]`。
- 状态机 / 覆盖语义见契约 §5。

---

## 2. `database.py` 迁移（幂等）

插入位置：紧随 P0 `pricing_rules` 建表与 seed 之后（同 `initialize()` 事务块内）。沿用 P0 的 `pragma table_info` 探测 + `create table if not exists` 幂等模式；seed 用 `insert or ignore`（可重复执行）。

```python
# ── Phase-9A P1：quota_rules 表（计划级配额权威来源）──
# 与 plans / quotas / pricing_rules 同区；create table if not exists 保证幂等。
connection.executescript(
    """
    create table if not exists quota_rules (
      quota_rule_id     text primary key,
      plan_id           text not null,
      quota_type        text not null
                         check (quota_type in
                           ('token_limit','employee_seat_limit','workflow_limit',
                            'capability_limit','connector_limit')),
      limit_value       integer,
      is_unlimited      integer not null default 0,
      period            text not null default 'monthly'
                         check (period in ('daily','monthly','annual','none')),
      enforcement_mode  text not null default 'notify'
                         check (enforcement_mode in ('notify','throttle','block','billing_only')),
      status            text not null default 'draft'
                         check (status in ('draft','active','disabled')),
      source_scope_json text not null default '[]',
      created_at        text not null default current_timestamp,
      updated_at        text not null default current_timestamp
    );
    create unique index if not exists idx_quota_rules_plan_type_active
      on quota_rules(plan_id, quota_type) where status = 'active';
    create index if not exists idx_quota_rules_plan on quota_rules(plan_id);
    create index if not exists idx_quota_rules_status on quota_rules(status);
    """
)

# ── Phase-9A P1：默认配额规则 seed（三档各 5 类，active，占位可被 Admin 改写）──
# insert or ignore：已存在则跳过，可重复执行；部分唯一索引保证每 plan+type 仅一条 active。
_SEED_QUOTA_RULES = [
    # (quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, period, enforcement_mode, status, source_scope_json)
    # ── Free ──
    ('qr_free_token',       'plan_free', 'token_limit',        1000000, 0, 'monthly', 'notify',   'active', '[]'),
    ('qr_free_seat',        'plan_free', 'employee_seat_limit',     3, 0, 'monthly', 'notify',   'active', '[]'),
    ('qr_free_workflow',    'plan_free', 'workflow_limit',        None, 1, 'monthly', 'notify',   'active', '[]'),
    ('qr_free_capability',  'plan_free', 'capability_limit',     None, 1, 'monthly', 'block',    'active', '["official"]'),
    ('qr_free_connector',   'plan_free', 'connector_limit',         0, 0, 'monthly', 'block',    'active', '[]'),
    # ── Pro ──
    ('qr_pro_token',        'plan_pro', 'token_limit',        50000000, 0, 'monthly', 'notify',   'active', '[]'),
    ('qr_pro_seat',         'plan_pro', 'employee_seat_limit',    15, 0, 'monthly', 'notify',   'active', '[]'),
    ('qr_pro_workflow',     'plan_pro', 'workflow_limit',       50000, 0, 'monthly', 'notify',   'active', '[]'),
    ('qr_pro_capability',   'plan_pro', 'capability_limit',      None, 1, 'monthly', 'block',    'active', '["official","tenant_private"]'),
    ('qr_pro_connector',    'plan_pro', 'connector_limit',       None, 1, 'monthly', 'block',    'active', '["official","tenant_private"]'),
    # ── Enterprise（custom：占位 NULL，is_unlimited=1，Admin 按企业改写）──
    ('qr_ent_token',        'plan_enterprise', 'token_limit',      None, 1, 'annual', 'notify',   'active', '[]'),
    ('qr_ent_seat',         'plan_enterprise', 'employee_seat_limit', None, 1, 'annual', 'notify', 'active', '[]'),
    ('qr_ent_workflow',     'plan_enterprise', 'workflow_limit',   None, 1, 'annual', 'notify',   'active', '[]'),
    ('qr_ent_capability',   'plan_enterprise', 'capability_limit', None, 1, 'annual', 'block',    'active', '["official","tenant_private","marketplace"]'),
    ('qr_ent_connector',    'plan_enterprise', 'connector_limit',  None, 1, 'annual', 'block',    'active', '["official","tenant_private","marketplace"]'),
]
for r in _SEED_QUOTA_RULES:
    connection.execute(
        "insert or ignore into quota_rules "
        "(quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, "
        " period, enforcement_mode, status, source_scope_json) "
        "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        r,
    )
```

> 幂等说明：建表用 `if not exists`；seed 用 `insert or ignore`（主键冲突跳过）。部分唯一索引保证 active 唯一性；重复运行安全。

---

## 3. `billing_store.py` 方法签名（参考 pricing_rules 7 方法，按需精简）

新增校验常量（模块级，与 `_VALID_QUOTA_TYPES` 等并列）：

```python
_VALID_QUOTA_RULE_TYPES = frozenset(
    {"token_limit", "employee_seat_limit", "workflow_limit", "capability_limit", "connector_limit"}
)
_VALID_ENFORCEMENT_MODES = frozenset({"notify", "throttle", "block", "billing_only"})
_VALID_QUOTA_RULE_PERIODS = frozenset({"daily", "monthly", "annual", "none"})
_VALID_QUOTA_RULE_STATUSES = frozenset({"draft", "active", "disabled"})
```

方法（7 个，对应 `pricing_rules` 风格）：

```python
# ── QuotaRule management (Phase-9A P1): quota_rules 为计划级配额权威 ──

def _quota_rule_dto(self, row) -> dict:
    """quota_rules 行 → API/契约 dict。"""

def _get_quota_rule_row(self, rule_id: str) -> "Any | None":
    """按 quota_rule_id 取原始行。"""

def _expire_old_active_quota_rules(self, plan_id: str, quota_type: str, exclude_rule_id: str | None = None) -> None:
    """同 plan_id+quota_type 的其它 active 规则置 disabled（历史保留，不删）。"""

def create_quota_rule(
    self, plan_id: str, quota_type: str,
    limit_value: "int | None" = None, is_unlimited: bool = False,
    period: str = "monthly", enforcement_mode: str = "notify",
    source_scope: "list[str] | None" = None, status: str = "draft",
) -> dict:
    """创建配额规则。若 status='active' 且同 plan+type 已有 active，先将其置 disabled（新覆盖旧）。"""

def update_quota_rule(self, rule_id: str, **fields: Any) -> dict:
    """部分更新。已 active 的历史记录禁止改 limit_value（须 disable 后重建）；
       激活触发覆盖：变 active 时先把同 plan+type 其它 active 置 disabled。"""

def list_quota_rules(
    self, plan_id: str | None = None, quota_type: str | None = None,
    status: str | None = None, enforcement_mode: str | None = None,
) -> list[dict]:
    """列表，支持按 plan / type / status / enforcement 过滤。"""

def get_active_quota_rule(self, plan_id: str, quota_type: str) -> "dict | None":
    """返回某 plan+type 当前 active 规则（部分唯一索引保证唯一），无则 None。"""
```

**与 pricing_rules 方法对照**：

| pricing_rules | quota_rules（本 Issue） | 差异 |
| --- | --- | --- |
| `_pricing_rule_dto` | `_quota_rule_dto` | 字段不同 |
| `_get_pricing_rule_row` | `_get_quota_rule_row` | — |
| `_expire_old_active_fixed_rules` | `_expire_old_active_quota_rules` | 按 `plan_id+quota_type`，不限 pricing_type |
| `create_pricing_rule` | `create_quota_rule` | 无 `amount`/`billing_cycle`/`effective_*`，改为 `limit_value`/`is_unlimited`/`period`/`enforcement_mode`/`source_scope` |
| `update_pricing_rule` | `update_quota_rule` | 同风格覆盖触发 |
| `list_pricing_rules` | `list_quota_rules` | + `enforcement_mode` 过滤 |
| `get_active_pricing_rule` | `get_active_quota_rule` | 按 `plan_id+quota_type` |

> 全部纯 SQL、`?` 占位、`row→dict`，不触 Workspace / Credential Vault（与 P0 一致）。

---

## 4. `main.py` 路由 + pydantic 模型

### 4.1 pydantic 模型（置于现有 `PricingRule*` 模型附近）

```python
class QuotaRuleCreateIn(BaseModel):
    """创建计划级配额规则。"""
    plan_id: str
    quota_type: str                       # 五类之一
    limit_value: int | None = None
    is_unlimited: bool = False
    period: str = "monthly"
    enforcement_mode: str = "notify"
    source_scope: list[str] = []         # 准入型专用
    status: str = "draft"


class QuotaRuleUpdateIn(BaseModel):
    """更新配额规则（全部可选，部分更新）。"""
    limit_value: int | None = None
    is_unlimited: bool | None = None
    period: str | None = None
    enforcement_mode: str | None = None
    source_scope: list[str] | None = None
    status: str | None = None
```

### 4.2 路由（全部 `_require_platform_admin`，4+1 个）

```python
# ── Phase-9A P1 计划级配额规则（quota_rules 为权威；全部平台管理员守卫）──
@app.get("/api/platform/quota-rules")
def list_platform_quota_rules(
    request: Request,
    plan_id: str | None = None,
    quota_type: str | None = None,
    status: str | None = None,
    enforcement_mode: str | None = None,
):
    _require_platform_admin(request)
    return {"quota_rules": billing.list_quota_rules(plan_id, quota_type, status, enforcement_mode)}

@app.post("/api/platform/quota-rules", status_code=201)
def create_platform_quota_rule(payload: QuotaRuleCreateIn, request: Request):
    _require_platform_admin(request)
    try:
        rule = billing.create_quota_rule(
            plan_id=payload.plan_id, quota_type=payload.quota_type,
            limit_value=payload.limit_value, is_unlimited=payload.is_unlimited,
            period=payload.period, enforcement_mode=payload.enforcement_mode,
            source_scope=payload.source_scope, status=payload.status,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return rule

@app.put("/api/platform/quota-rules/{rule_id}")
def update_platform_quota_rule(rule_id: str, payload: QuotaRuleUpdateIn, request: Request):
    _require_platform_admin(request)
    try:
        rule = billing.update_quota_rule(
            rule_id, limit_value=payload.limit_value, is_unlimited=payload.is_unlimited,
            period=payload.period, enforcement_mode=payload.enforcement_mode,
            source_scope=payload.source_scope, status=payload.status,
        )
    except KeyError as error:
        raise HTTPException(status_code=404, detail=f"QuotaRule {rule_id!r} 不存在") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return rule

@app.get("/api/platform/plans/{plan_id}/quotas")
def get_platform_plan_quotas(plan_id: str, request: Request):
    """读取某套餐的计划级配额规则（权威来源预览）。"""
    _require_platform_admin(request)
    return {"plan_id": plan_id, "quota_rules": billing.list_quota_rules(plan_id=plan_id)}
```

> 路由对照 P0：GET/POST/PUT `/api/platform/quota-rules`（对应 pricing-rules 三路由）+ GET `/api/platform/plans/{id}/quotas`（套餐配额预览）。错误映射沿用 P0：`ValueError → 422`、`KeyError → 404`。

---

## 5. API 设计说明

| 方法 & 路径 | 守卫 | 请求体 / 参数 | 成功响应 | 错误码 |
| --- | --- | --- | --- | --- |
| `GET /api/platform/quota-rules` | `_require_platform_admin` | query: `plan_id?`, `quota_type?`, `status?`, `enforcement_mode?` | `200 {quota_rules: [...]}` | 401（无/错令牌） |
| `POST /api/platform/quota-rules` | 同上 | `QuotaRuleCreateIn` | `201` 规则对象 | 401 / 422（非法枚举或参数） |
| `PUT /api/platform/quota-rules/{rule_id}` | 同上 | `QuotaRuleUpdateIn` | `200` 规则对象 | 401 / 404（rule 不存在）/ 422 |
| `GET /api/platform/plans/{plan_id}/quotas` | 同上 | path: `plan_id` | `200 {plan_id, quota_rules: [...]}` | 401 |

**统一状态码约定**：
- 鉴权失败 → **401**（沿用 `_require_platform_admin`，**不用 403**）。
- 业务校验失败（非法 `quota_type` / `enforcement_mode` / `period` / `status`）→ **422**。
- 资源不存在（`rule_id` 未命中）→ **404**。
- 创建成功 → **201**；读/更新成功 → **200**。

**响应字段**（单条 `quota_rule` 对象，来自 `_quota_rule_dto`）：
`quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, period, enforcement_mode, status, source_scope, created_at, updated_at`。

---

## 6. Plan–Quota 关系边界说明

- **权威来源**：`quota_rules(plan_id)` 是计划级配额配置的权威。任何套餐的限制值**须经 Admin API 可配置**；默认 seed 仅为占位。
- **不写死 Plan**：配额规则不进入 `plans` 表列，按 `plan_id` 关联（对齐 P0 价格不写死 Plan）。
- **per-tenant 实例层**：`quotas` 实例表结构**本 Issue 不变**；未来由 Usage Meter / 实例化作业读取 `quota_rules` 派生实例（不在本 Issue 实现）。
- **遗留 `plans.quota_rules_json`**：保留作展示/历史回退；新写入以 `quota_rules` 为准。

---

## 7. Usage Meter 关联链路（可达性，不实现）

```
Plan → quota_rules(plan_id) → [未来] 实例化 quotas → Usage Event → Usage Meter 读时聚合
```
本 Issue 仅新增 `quota_rules` 定义层，**确认链路可达**；不新增/修改 Usage Event 写入、Employee Runtime、Workspace 执行链、Credential Vault。

---

## 8. seed 详情（占位，可被 Admin 改写）

| 套餐 | quota_type | limit_value | is_unlimited | period | enforcement_mode | source_scope | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Free | `token_limit` | 1,000,000 | 0 | monthly | notify | [] | active |
| Free | `employee_seat_limit` | 3 | 0 | monthly | notify | [] | active |
| Free | `workflow_limit` | NULL | 1 | monthly | notify | [] | active |
| Free | `capability_limit` | NULL | 1 | monthly | block | ["official"] | active |
| Free | `connector_limit` | 0 | 0 | monthly | block | [] | active |
| Pro | `token_limit` | 50,000,000 | 0 | monthly | notify | [] | active |
| Pro | `employee_seat_limit` | 15 | 0 | monthly | notify | [] | active |
| Pro | `workflow_limit` | 50,000 | 0 | monthly | notify | [] | active |
| Pro | `capability_limit` | NULL | 1 | monthly | block | ["official","tenant_private"] | active |
| Pro | `connector_limit` | NULL | 1 | monthly | block | ["official","tenant_private"] | active |
| Enterprise | `token_limit` | NULL | 1 | annual | notify | [] | active |
| Enterprise | `employee_seat_limit` | NULL | 1 | annual | notify | [] | active |
| Enterprise | `workflow_limit` | NULL | 1 | annual | notify | [] | active |
| Enterprise | `capability_limit` | NULL | 1 | annual | block | ["official","tenant_private","marketplace"] | active |
| Enterprise | `connector_limit` | NULL | 1 | annual | block | ["official","tenant_private","marketplace"] | active |

> **占位声明**：上表数值为合理占位（非真实业务数值）。Free/Pro 数值型为示例上限；Enterprise 为 `custom`（NULL + is_unlimited，Admin 按企业改写）。全部须经 Admin API 可改；无一处写死为不可改。

---

## 9. 测试矩阵（给工程师的规格，未执行）

| ID | 用例 | 验证点 | 期望 |
| --- | --- | --- | --- |
| T1 | 建表幂等 | 重复 `initialize()` | `quota_rules` 表存在；部分唯一索引生效；无重复 |
| T2 | seed 幂等 | 重复运行迁移 | 15 条 active 规则存在且唯一（每 plan+type 一条 active） |
| T3 | 创建数值型规则 | POST `/quota-rules`（token_limit, limit=xxx） | 201；返回对象含 `quota_rule_id`；`is_unlimited=0` |
| T4 | 创建准入型规则 | POST（capability_limit, source_scope） | 201；`source_scope_json` 正确持久化；`limit_value=NULL` |
| T5 | 非法枚举校验 | POST `quota_type='xxx'` / `enforcement_mode='xxx'` | 422 |
| T6 | 覆盖语义 | 同 plan+type 再 POST `status=active` | 旧 active → disabled；新 active 唯一（部分唯一索引 + `_expire_old_active_quota_rules`） |
| T7 | 列表过滤 | GET `?plan_id=plan_pro&status=active` | 仅返回 Pro 的 active 规则 |
| T8 | 更新部分字段 | PUT `limit_value` / `status` | 200；未传字段不变；`updated_at` 刷新 |
| T9 | 更新已 active 禁止改 limit | PUT 已 active 规则的 `limit_value` | 422（须 disable 后重建） |
| T10 | 不存在资源 | PUT 错误 `rule_id` | 404 |
| T11 | 套餐配额预览 | GET `/plans/{plan_id}/quotas` | 200；返回该 plan 全部 `quota_rules` |
| T12 | **不硬编码** | 修改某 plan 规则 limit 后读取 | 返回改写后值（证明可配置，非写死） |
| T13 | 守卫 | 无/错 `Authorization` 调用任意路由 | 401（非 403） |
| T14 | 状态机 | draft→active→disabled 流转 | 各态 `get_active_quota_rule` 仅返回 active 那条 |
| T15 | 边界：禁止清单 | 代码审查确认无 BillingEvent/Payment/Invoice/Marketplace/ValuePricing 逻辑；未改 Workspace/CredentialVault/UsageEvent | 通过 |

---

## 10. 受影响文件清单

| 文件 | 改动类型 | 说明 |
| --- | --- | --- |
| `backend/app/database.py` | 修改 | 新增 `quota_rules` 建表 + 部分唯一索引；新增 15 条 seed（`insert or ignore`） |
| `backend/app/billing_store.py` | 修改 | 新增 4 个校验常量 + 7 个 QuotaRule 方法（`_quota_rule_dto` / `_get_quota_rule_row` / `_expire_old_active_quota_rules` / `create_quota_rule` / `update_quota_rule` / `list_quota_rules` / `get_active_quota_rule`） |
| `backend/app/main.py` | 修改 | 新增 `QuotaRuleCreateIn` / `QuotaRuleUpdateIn` 模型；新增 4 个路由（GET/POST/PUT `/quota-rules` + GET `/plans/{id}/quotas`） |
| `docs/contracts/quota-rule-contract.md` | **重写** | 由 Phase-8.5 策略层占位 → QuotaRule 实体契约（吸收策略矩阵入 §4） |
| `docs/design/phase9a-p1-quota-implementation-design.md` | **新增** | 本设计文档 |
| `tests/test_quota_rules.py`（或既有 billing 测试文件） | 新增 | 测试矩阵 T1–T15 |

> **不改**：`quotas` 实例表结构、`usage_event` / `employee_instances` / `workflow_runs` 写入、`Workspace` / `CredentialVault` / `EmployeeRuntime` / `SharedContract`、`pricing_rules` 相关代码。

---

## 11. 有序任务列表（给工程师，含依赖）

| 任务 | 内容 | 依赖 | 优先级 |
| --- | --- | --- | --- |
| **Task 1** | `database.py`：新增 `quota_rules` 建表（含部分唯一索引）+ 15 条 seed；幂等 `if not exists` / `insert or ignore` | 无 | P0 |
| **Task 2** | `billing_store.py`：新增 4 校验常量 + 7 个 QuotaRule 方法（dto/get_row/expire/create/update/list/get_active） | Task 1 | P0 |
| **Task 3** | `main.py`：新增 `QuotaRuleCreateIn` / `QuotaRuleUpdateIn` 模型 + 4 路由（全 `_require_platform_admin`，错误映射 401/404/422） | Task 2 | P0 |
| **Task 4** | 集成验证 + 测试矩阵 T1–T15（建表/seed 幂等、CRUD、覆盖语义、不硬编码、状态机、守卫、边界） | Task 1,2,3 | P1 |
| **Task 5** | 文档复核：确认 `quota-rule-contract.md` 已取代旧版、本设计文档与设计哲学/禁止清单一致；更新 `docs/contracts/README.md` 索引（如适用） | Task 3 | P2 |

> 实现顺序严格 1→2→3→4→5（每层依赖前层）。Task 5 为文档收尾，可与 Task 4 并行。

---

## 12. 待明确事项

1. **`source_scope_json` 列**：本设计已采用（使 `quota_rules` 对 5 类完全权威）。若 PO 要求严格 7 字段不加列，则 capability/connector 白名单暂留 `plans.quota_rules_json`，`quota_rules` 对这两类仅作治理标记。两种方案均兼容，推荐采用列方案（已在契约 §10 标注）。
2. **seed 占位数值**：上表为合理占位，非真实业务值；最终值以 Admin 运营决策为准（全部可改）。
3. **`period` 含 `annual`**：向前兼容 Enterprise 年付；如需严格限于 `daily/monthly/none` 可移除（需同步改 DDL 与常量）。
4. **`quotas` 实例表短名（token 等）与 `quota_rules` 规范名（token_limit 等）映射**：本 Issue 不统一，留待未来 Issue。
5. **命名冲突已处理**：`docs/contracts/quota-rule-contract.md` 已重写为实体契约并取代 Phase-8.5 策略占位版（旧策略矩阵并入 §4）。无遗留歧义。

*—— Phase-9A P1 QuotaRule Configuration 实现设计（架构师 高见远）。*
