# Phase-9A P0 Subscription Pricing Rule — 实现设计（工程师执行蓝图）

> **作者**：高见远（架构师，software-architect）
> **阶段**：Phase-9A P0（设计 + 契约阶段，**本文件为给工程师的精确执行蓝图，不写任何 .py/.js 源码**）
> **归属**：Admin Platform 线；**不触及 Workspace / Shared Contract**
> **目标**：把订阅价格从硬编码升级为 Admin 可配置的 `PricingRule`；`pricing_rules(subscription)` 为价格权威，`plans.price` 仅作展示/镜像。

> ⚠️ **本文件仅描述"做什么 / 怎么落地"，不含可运行源码。** 以下代码片段为设计蓝图（方法签名、SQL、路由骨架），由工程师照此编写 `backend/app/*.py` 与测试。请勿将本文件误认为已落地的代码。

---

## 0. 设计原则（贴合真实代码风格）

| 既有模式（来自真实代码） | 本 Issue 沿用方式 |
| --- | --- |
| `create table if not exists` + `create index if not exists` | `pricing_rules` DDL 见 §1 |
| `pragma table_info` + `alter table ... add column`（Phase-9A `is_unlimited` 迁移，`database.py:805-809`） | `plans` 镜像列 ALTER 见 §2 |
| `insert or ignore` 幂等 seed（`database.py:823-838` 三档 plan） | 默认订阅价 seed 见 §5 |
| `BillingStore` 纯 SQL、`?` 占位、row→dict（`_quota_dto` 等） | 新增方法见 §3 |
| `main.py` pydantic `QuotaCreateIn/QuotaUpdateIn` + 路由透传 `billing.*` + `_require_platform_admin` | pydantic + 路由见 §4 |
| `_ensure_column` 辅助（`database.py:856`） | 复用或内联 pragma 探测见 §2 |

---

## 1. `pricing_rules` DDL（完整建表）

> 落地位置：`backend/app/database.py` 的 Phase-8 Billing 建表 `executescript` 区块之后（与 `plans` / `quotas` / `billing_events` 同区），用 `create table if not exists` 保证幂等。

```sql
create table if not exists pricing_rules (
  pricing_rule_id  text primary key,
  subject_type     text not null
                    check (subject_type in
                      ('subscription','capability','employee','connector','template')),
  pricing_type     text not null
                    check (pricing_type in ('fixed','discount','override')),
  plan_id          text not null,
  amount           real not null default 0,
  currency         text not null default 'USD',
  billing_cycle    text not null default 'month'
                    check (billing_cycle in ('month','year','one_time')),
  effective_start  text not null,
  effective_end    text,
  status           text not null default 'draft'
                    check (status in ('draft','active','expired','disabled')),
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create index if not exists idx_pricing_rules_plan_status
  on pricing_rules(plan_id, status);
create index if not exists idx_pricing_rules_subject
  on pricing_rules(subject_type);
```

**要点**
- 列与契约 §1 一一对应：`pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, billing_cycle, effective_start, effective_end, status, created_at, updated_at`。
- 索引 `idx_pricing_rules_plan_status(plan_id, status)` 支撑"按 plan 解析当前 active 价"；`idx_pricing_rules_subject(subject_type)` 支撑未来多维扩展。
- `subject_type` CHECK 预置 5 类（含未来类型），**本 Issue 仅写入 `subscription`**，未来 Issue 无需再 ALTER。

---

## 2. `plans` 镜像列（Additive ALTER，仅展示/镜像，**非价格权威**）

> **现状确认**：`plans` 表（`database.py:746-760`）**无 `price` / `price_currency` / `billing_cycle` 列**（Phase-8.6 审计唯一 P0 缺口）。
> **设计**：新增 3 个 **nullable** 镜像列，由 active pricing rule **派生写入**，前端展示用。

### 2.1 迁移 SQL（additive，兼容既有库）

> 落地位置：`database.py` 中 Phase-9A `is_unlimited` 迁移块（`database.py:805-817`）**之后**，沿用 `pragma table_info` 探测 + `alter table ... add column` 模式（与 `is_unlimited` 完全一致）。

```python
# ── Phase-9A P0：plans 新增订阅价镜像列（additive，兼容既有库）──
# 仅展示/镜像，由 active pricing rule 派生写入；绝不作为价格权威。
with connection:
    plan_cols = {r["name"] for r in connection.execute("pragma table_info(plans)")}
    if "price" not in plan_cols:
        connection.execute("alter table plans add column price real")
    if "price_currency" not in plan_cols:
        connection.execute("alter table plans add column price_currency text")
    if "billing_cycle" not in plan_cols:
        connection.execute("alter table plans add column billing_cycle text")
```

### 2.2 镜像列判定（消除"是否改 Shared Contract"疑虑）

| 判项 | 结论 |
| --- | --- |
| 是否修改 `plans` 的契约语义？ | **否**。`plan_id/plan_code/name/tier/status/...` 等原列与约束**完全不变**；仅 additive 加 3 个可空列。 |
| 是否修改 Shared Contract？ | **否**。`plans` 本就是 **Admin 商业表**（Admin Platform 线负责，见 `source-control-baseline-freeze.md` §4.1/§4.3）。镜像列属 Admin 管理范围，仅 `platform admin` 路由可写。 |
| 是否影响 Workspace？ | **否**。Workspace 运行时只读 `tenants.plan_tier` / `quota_rules_json` 派生配额，**不读 `plans.price`**；镜像列对 Workspace 执行链零影响（无读时耦合、无写时耦合）。 |
| 是否作为价格权威？ | **绝对否**。`pricing_rules(subscription)` 才是权威；镜像列仅用于前端展示/看板，值由 `get_plan_pricing(sync_mirror=True)` 从 active rule 派生。 |

> ✅ **判定结论**：3 个镜像列属 Admin Platform 范围内的 additive 扩展，**不触碰 Shared Contract、不影响 Workspace**，符合基线冻结文档 §5 新规则与红线。

---

## 3. `BillingStore` 新增方法（沿用 `?` 占位 + row dict 风格）

> 落地位置：`backend/app/billing_store.py`（`BillingStore` 类内，与 `create_plan` / `update_plan` / `upsert_quota_limit` 同区）。
> 需新增模块级枚举常量（与既有 `_VALID_*` frozenset 风格一致）：
> ```python
> _VALID_PRICING_SUBJECT_TYPES = frozenset({"subscription", "capability", "employee", "connector", "template"})
> _VALID_PRICING_TYPES = frozenset({"fixed", "discount", "override"})
> _VALID_PRICING_RULE_STATUSES = frozenset({"draft", "active", "expired", "disabled"})
> ```

### 3.1 `_pricing_rule_dto(row)`

```python
def _pricing_rule_dto(self, row: "Any") -> dict[str, Any]:
    return {
        "pricing_rule_id": row["pricing_rule_id"],
        "subject_type": row["subject_type"],
        "pricing_type": row["pricing_type"],
        "plan_id": row["plan_id"],
        "amount": float(row["amount"]),
        "currency": row["currency"],
        "billing_cycle": row["billing_cycle"],
        "effective_start": row["effective_start"],
        "effective_end": row["effective_end"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
```

### 3.2 `create_pricing_rule(...)`

```python
def create_pricing_rule(
    self,
    plan_id: str,
    subject_type: str,
    pricing_type: str,
    amount: float,
    currency: str = "USD",
    billing_cycle: str = "month",
    effective_start: str = "",
    effective_end: "str | None" = None,
    status: str = "draft",
) -> dict[str, Any]:
    """创建定价规则。若 pricing_type='fixed' 且 status='active'，先把同 plan 旧 active
    固定价置为 expired 并回填 effective_end=now（新覆盖旧，历史不删）。"""
    if subject_type not in _VALID_PRICING_SUBJECT_TYPES:
        raise ValueError(f"非法的 subject_type: {subject_type!r}")
    if pricing_type not in _VALID_PRICING_TYPES:
        raise ValueError(f"非法的 pricing_type: {pricing_type!r}")
    if status not in _VALID_PRICING_RULE_STATUSES:
        raise ValueError(f"非法的 status: {status!r}")
    rule_id = f"pr_{uuid.uuid4().hex}"
    with self.db.connect() as connection:
        # 新 active 固定价覆盖旧：旧 active 固定价 -> expired + effective_end=now
        if pricing_type == "fixed" and status == "active":
            connection.execute(
                "update pricing_rules set status='expired', effective_end=current_timestamp, "
                "updated_at=current_timestamp "
                "where plan_id=? and subject_type=? and pricing_type='fixed' and status='active'",
                (plan_id, subject_type),
            )
        connection.execute(
            "insert into pricing_rules "
            "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
            "billing_cycle, effective_start, effective_end, status) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                rule_id, subject_type, pricing_type, plan_id,
                float(amount), currency, billing_cycle,
                effective_start, effective_end, status,
            ),
        )
        row = connection.execute(
            "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
        ).fetchone()
    return self._pricing_rule_dto(row)
```

### 3.3 `update_pricing_rule(rule_id, **fields)`

```python
def update_pricing_rule(self, rule_id: str, **fields: "Any") -> dict[str, Any]:
    """仅改 draft/未生效记录的可变字段；已 active 历史记录不允许改金额
    （只能 expire 后新建）。"""
    existing = self._get_pricing_rule_row(rule_id)
    if existing is None:
        raise KeyError(rule_id)
    is_active_history = existing["status"] == "active"

    allowed = {
        "subject_type": _VALID_PRICING_SUBJECT_TYPES,
        "pricing_type": _VALID_PRICING_TYPES,
        "status": _VALID_PRICING_RULE_STATUSES,
    }
    sets: list[str] = []
    params: list[Any] = []
    # 标量枚举字段
    for key in ("subject_type", "pricing_type", "status"):
        if key in fields and fields[key] is not None:
            value = fields[key]
            if value not in allowed[key]:
                raise ValueError(f"非法的 {key}: {value!r}")
            sets.append(f"{key} = ?")
            params.append(value)
    # 金额：已 active 历史禁止改
    if fields.get("amount") is not None:
        if is_active_history:
            raise ValueError("已生效(active)定价规则不允许修改金额，请 expire 后新建")
        sets.append("amount = ?")
        params.append(float(fields["amount"]))
    # 其余标量
    for key in ("currency", "billing_cycle", "effective_start", "effective_end"):
        if key in fields and fields[key] is not None:
            sets.append(f"{key} = ?")
            params.append(fields[key])

    if not sets:
        return self._pricing_rule_dto(existing)
    sets.append("updated_at = current_timestamp")
    params.append(rule_id)
    with self.db.connect() as connection:
        connection.execute(
            f"update pricing_rules set {', '.join(sets)} where pricing_rule_id = ?",
            params,
        )
        row = connection.execute(
            "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
        ).fetchone()
    if row is None:
        raise KeyError(rule_id)
    return self._pricing_rule_dto(row)

#### 3.3.1 私有辅助 `_expire_old_active_fixed_rules(plan_id, subject_type, exclude_rule_id=None)`

将同 `plan_id`+`subject_type` 下，其它 `active` 的固定价规则置 `expired`（回填 `effective_end=now` 与 `updated_at=now`）。`exclude_rule_id` 用于排除正在激活的当前规则自身（避免把它也过期）。**不删除任何历史价格记录**。`create_pricing_rule` 与 `update_pricing_rule` 的覆盖逻辑统一复用此辅助，避免内联 SQL 散落。

### 3.3 `update_pricing_rule(rule_id, **fields)`（激活覆盖语义）

```python
def update_pricing_rule(self, rule_id: str, **fields: "Any") -> dict[str, Any]:
    """更新可改字段；已 active 历史禁止改金额（只能 expire 后新建）。
    激活覆盖：当更新使规则变为 active+fixed 且原本不是 active+fixed 时，
    先把同 plan+subject 其它 active 固定价置 expired（排除自身），再把它置 active；
    历史价格不删。"""
    existing = self._get_pricing_rule_row(rule_id)
    if existing is None:
        raise KeyError(rule_id)
    is_active_history = existing["status"] == "active"

    # 解析更新后目标值（未提供字段沿用既有值）
    post_status = fields["status"] if fields.get("status") is not None else existing["status"]
    post_pricing_type = (
        fields["pricing_type"]
        if fields.get("pricing_type") is not None
        else existing["pricing_type"]
    )
    # 覆盖触发：将变为 active+fixed 且原本并非 active+fixed
    trigger_cover = (
        post_status == "active"
        and post_pricing_type == "fixed"
        and not (existing["status"] == "active" and existing["pricing_type"] == "fixed")
    )

    allowed = {
        "subject_type": _VALID_PRICING_SUBJECT_TYPES,
        "pricing_type": _VALID_PRICING_TYPES,
        "status": _VALID_PRICING_RULE_STATUSES,
    }
    sets: list[str] = []
    params: list[Any] = []
    # 标量枚举字段
    for key in ("subject_type", "pricing_type", "status"):
        if key in fields and fields[key] is not None:
            value = fields[key]
            if value not in allowed[key]:
                raise ValueError(f"非法的 {key}: {value!r}")
            sets.append(f"{key} = ?")
            params.append(value)
    # 金额：已 active 历史禁止改
    if fields.get("amount") is not None:
        if is_active_history:
            raise ValueError("已生效(active)定价规则不允许修改金额，请 expire 后新建")
        sets.append("amount = ?")
        params.append(float(fields["amount"]))
    # 其余标量
    for key in ("currency", "billing_cycle", "effective_start", "effective_end"):
        if key in fields and fields[key] is not None:
            sets.append(f"{key} = ?")
            params.append(fields[key])

    if not sets:
        return self._pricing_rule_dto(existing)
    # 覆盖触发：先置其它 active 固定价为 expired（排除自身），随后本规则 UPDATE 为 active
    if trigger_cover:
        self._expire_old_active_fixed_rules(
            plan_id=existing["plan_id"],
            subject_type=existing["subject_type"],
            exclude_rule_id=rule_id,
        )
    sets.append("updated_at = current_timestamp")
    params.append(rule_id)
    with self.db.connect() as connection:
        connection.execute(
            f"update pricing_rules set {', '.join(sets)} where pricing_rule_id = ?",
            params,
        )
        row = connection.execute(
            "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
        ).fetchone()
    if row is None:
        raise KeyError(rule_id)
    return self._pricing_rule_dto(row)
```

**边界**：① 更新后 `status≠active` 或 `pricing_type≠fixed` → 不触发覆盖；② 已 `active` 记录禁改 `amount` 的既有 `ValueError`→422 规则不变；③ 不删除任何历史价格（仅置 expired + 回填 effective_end）；④ 覆盖时排除自身（exclude=rule_id），随后才把它置 active；⑤ subject_type 沿用 existing。

> 注：`create_pricing_rule` 中原内联的覆盖 SQL 已抽取至 `_expire_old_active_fixed_rules`，插入前在 `pricing_type=='fixed' and status=='active'` 守卫下调用（exclude=None），行为不变。

def _get_pricing_rule_row(self, rule_id: str):
    with self.db.connect() as connection:
        return connection.execute(
            "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
        ).fetchone()
```

### 3.4 `list_pricing_rules(plan_id=None, subject_type=None, status=None)`

```python
def list_pricing_rules(
    self,
    plan_id: "str | None" = None,
    subject_type: "str | None" = None,
    status: "str | None" = None,
) -> list[dict[str, Any]]:
    sql = "select * from pricing_rules"
    clauses: list[str] = []
    params: list[Any] = []
    if plan_id:
        clauses.append("plan_id = ?"); params.append(plan_id)
    if subject_type:
        clauses.append("subject_type = ?"); params.append(subject_type)
    if status:
        clauses.append("status = ?"); params.append(status)
    if clauses:
        sql += " where " + " and ".join(clauses)
    sql += " order by plan_id, effective_start desc, created_at desc"
    with self.db.connect() as connection:
        rows = connection.execute(sql, params).fetchall()
    return [self._pricing_rule_dto(row) for row in rows]
```

### 3.5 `get_active_pricing_rule(plan_id, subject_type="subscription", pricing_type="fixed", as_of=None)`

```python
def get_active_pricing_rule(
    self,
    plan_id: str,
    subject_type: str = "subscription",
    pricing_type: str = "fixed",
    as_of: "str | None" = None,
) -> "dict[str, Any] | None":
    """返回当前生效规则：subject_type + pricing_type + status='active' + effective 区间覆盖 as_of 的最新一条。无则 None。"""
    if as_of is None:
        time_clause = "effective_start <= current_timestamp and (effective_end is null or effective_end >= current_timestamp)"
        params: list[Any] = [plan_id, subject_type, pricing_type]
    else:
        time_clause = "effective_start <= ? and (effective_end is null or effective_end >= ?)"
        params = [plan_id, subject_type, pricing_type, as_of, as_of]
    sql = (
        "select * from pricing_rules "
        "where plan_id = ? and subject_type = ? and pricing_type = ? "
        f"and status = 'active' and {time_clause} "
        "order by effective_start desc, created_at desc limit 1"
    )
    with self.db.connect() as connection:
        row = connection.execute(sql, params).fetchone()
    return self._pricing_rule_dto(row) if row is not None else None
```

### 3.6 `get_plan_pricing(plan_id, sync_mirror=False)`

```python
def get_plan_pricing(self, plan_id: str, sync_mirror: bool = False) -> dict[str, Any]:
    """返回 plan 定价视图：active_rule + plans 镜像列。
    sync_mirror=True 时仅在有 active rule 的情况下，将派生值写回 plans 镜像列。"""
    active_rule = self.get_active_pricing_rule(
        plan_id, subject_type="subscription", pricing_type="fixed"
    )
    with self.db.connect() as connection:
        plan_row = connection.execute(
            "select plan_id, price, price_currency, billing_cycle from plans where plan_id = ?",
            (plan_id,),
        ).fetchone()
    mirror = {
        "mirror_price": plan_row["price"] if plan_row is not None else None,
        "mirror_currency": plan_row["price_currency"] if plan_row is not None else None,
        "mirror_billing_cycle": plan_row["billing_cycle"] if plan_row is not None else None,
    }
    if sync_mirror and active_rule is not None:
        with self.db.connect() as connection:
            connection.execute(
                "update plans set price=?, price_currency=?, billing_cycle=?, updated_at=current_timestamp "
                "where plan_id=?",
                (
                    float(active_rule["amount"]),
                    active_rule["currency"],
                    active_rule["billing_cycle"],
                    plan_id,
                ),
            )
        mirror = {
            "mirror_price": float(active_rule["amount"]),
            "mirror_currency": active_rule["currency"],
            "mirror_billing_cycle": active_rule["billing_cycle"],
        }
    return {
        "plan_id": plan_id,
        "active_rule": active_rule,          # None = 无生效订阅价（如 Enterprise）
        "mirror_price": mirror["mirror_price"],
        "mirror_currency": mirror["mirror_currency"],
        "mirror_billing_cycle": mirror["mirror_billing_cycle"],
    }
```

---

## 4. `main.py` 路由 + pydantic（沿用 `QuotaCreateIn` 风格）

> 落地位置：`backend/app/main.py`
> 1. 在 `QuotaCreateIn` / `QuotaUpdateIn`（`main.py:292-312`）附近新增两个 pydantic 模型。
> 2. 在 platform 路由区（`main.py:1500` 之后、`return app` 之前）新增 4 个端点，全部 `_require_platform_admin` 守卫，透传 `billing.*`（与 `create_platform_quota` / `update_platform_quota` 写法一致）。

### 4.1 pydantic 模型

```python
class PricingRuleCreateIn(BaseModel):
    """创建定价规则（subscription 固定价为主）。"""
    plan_id: str
    subject_type: str = "subscription"
    pricing_type: str = "fixed"
    amount: float
    currency: str = "USD"
    billing_cycle: str = "month"
    effective_start: str
    effective_end: str | None = None
    status: str = "draft"


class PricingRuleUpdateIn(BaseModel):
    """更新定价规则（全部可选，部分更新）。"""
    pricing_type: str | None = None
    amount: float | None = None
    currency: str | None = None
    billing_cycle: str | None = None
    effective_start: str | None = None
    effective_end: str | None = None
    status: str | None = None
```

### 4.2 路由

```python
@app.get("/api/platform/pricing-rules")
def list_platform_pricing_rules(
    request: Request,
    plan_id: str | None = None,
    subject_type: str | None = None,
    status: str | None = None,
):
    _require_platform_admin(request)
    return {"pricing_rules": billing.list_pricing_rules(plan_id, subject_type, status)}

@app.post("/api/platform/pricing-rules", status_code=201)
def create_platform_pricing_rule(payload: PricingRuleCreateIn, request: Request):
    _require_platform_admin(request)
    try:
        rule = billing.create_pricing_rule(
            plan_id=payload.plan_id,
            subject_type=payload.subject_type,
            pricing_type=payload.pricing_type,
            amount=payload.amount,
            currency=payload.currency,
            billing_cycle=payload.billing_cycle,
            effective_start=payload.effective_start,
            effective_end=payload.effective_end,
            status=payload.status,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return rule

@app.put("/api/platform/pricing-rules/{rule_id}")
def update_platform_pricing_rule(rule_id: str, payload: PricingRuleUpdateIn, request: Request):
    _require_platform_admin(request)
    try:
        rule = billing.update_pricing_rule(
            rule_id,
            pricing_type=payload.pricing_type,
            amount=payload.amount,
            currency=payload.currency,
            billing_cycle=payload.billing_cycle,
            effective_start=payload.effective_start,
            effective_end=payload.effective_end,
            status=payload.status,
        )
    except KeyError as error:
        raise HTTPException(status_code=404, detail=f"PricingRule {rule_id!r} 不存在") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return rule

@app.get("/api/platform/plans/{plan_id}/pricing")
def get_platform_plan_pricing(plan_id: str, request: Request, sync: bool = False):
    _require_platform_admin(request)
    return billing.get_plan_pricing(plan_id, sync_mirror=sync)
```

> **端点总览**：`GET/POST/PUT /api/platform/pricing-rules` + `GET /api/platform/plans/{plan_id}/pricing`，全部 `_require_platform_admin`（非 admin → 403）。**不提供任何 Workspace / 前台价格端点**。

---

## 5. seed 默认订阅价规则（幂等 `insert or ignore`）

> 落地位置：`database.py` 三档 plan seed（`database.py:823-838`）**之后**。使用确定性 `pricing_rule_id` + `insert or ignore` 保证幂等可重复执行。
> `plan_id` 用 `plan_free` / `plan_pro` / `plan_enterprise`（与 plan seed 的 `plan_id` 对齐）。

```python
# ── Phase-9A P0：默认订阅价规则（idempotent insert or ignore）──
# Free：固定价 0 USD/月，已生效，无结束（过去日期起生效）
connection.execute(
    "insert or ignore into pricing_rules "
    "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
    " billing_cycle, effective_start, effective_end, status) "
    "values ('pr_default_free', 'subscription', 'fixed', 'plan_free', 0, 'USD', "
    " 'month', '2024-01-01T00:00:00Z', NULL, 'active')"
)
# Pro：固定价 99 USD/月，已生效（用户示例 $99/month）
connection.execute(
    "insert or ignore into pricing_rules "
    "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
    " billing_cycle, effective_start, effective_end, status) "
    "values ('pr_default_pro', 'subscription', 'fixed', 'plan_pro', 99, 'USD', "
    " 'month', '2024-01-01T00:00:00Z', NULL, 'active')"
)
# Enterprise：本 Issue 不设默认订阅价规则（Enterprise 为 custom 定价，
#   未来由 TenantPricingPolicy 处理）。文档注明，不插入 subscription 规则。

# 同步将 Free/Pro 的镜像写入 plans.price/price_currency/billing_cycle（仅展示用）
connection.execute(
    "update plans set price=0, price_currency='USD', billing_cycle='month', "
    "updated_at=current_timestamp where plan_id='plan_free'"
)
connection.execute(
    "update plans set price=99, price_currency='USD', billing_cycle='month', "
    "updated_at=current_timestamp where plan_id='plan_pro'"
)
```

**seed 约定**
- `effective_start = '2024-01-01T00:00:00Z'`（过去日期，确保 seed 后即 active）。
- `effective_end = NULL`（永久生效，直到被新规则覆盖置 `expired`）。
- Enterprise **不插入** subscription 规则；其 `get_plan_pricing` 返回 `active_rule=None`（符合 §3.1 语义）。
- 镜像列仅 Free/Pro 同步；Enterprise 镜像列保持 `NULL`（无默认订阅价）。

---

## 6. 测试计划（给工程师，`backend/tests/test_phase9a_p0_pricing_rule.py`）

> 沿用 `backend/.venv/bin/python -m pytest` 回归体系（基线 356 passed）。新增文件独立覆盖本 Issue。

| # | 测试场景 | 断言要点 |
| --- | --- | --- |
| T1 | **Create + List** | `create_pricing_rule` 返回 dict；`list_pricing_rules(plan_id='plan_pro')` 含该条 |
| T2 | **Get active（单条）** | seed 后 `get_active_pricing_rule('plan_pro')` 返回 amount=99 / USD / month |
| T3 | **Active 解析（多规则按 effective 区间）** | 为 `plan_pro` 建两条 `fixed` `active` 规则（不同 `effective_start`）；断言返回 `effective_start` 最新者，旧者被置 `expired` |
| T4 | **历史保留（旧规则不删）** | T3 后 `list_pricing_rules(plan_id='plan_pro', status='expired')` 仍存在旧记录；断言**未被物理删除** |
| T5 | **Status 流转** | `create` 为 `draft` → `update(status='active')` → `update(status='expired'/'disabled')` 均成功 |
| T6 | **已 active 禁止改金额** | 对 `active` 规则 `update_pricing_rule(amount=...)` 抛 `ValueError`（422） |
| T7 | **`get_plan_pricing` 形状** | 返回含 `plan_id / active_rule / mirror_price / mirror_currency / mirror_billing_cycle` |
| T8 | **镜像同步** | `get_plan_pricing('plan_pro', sync_mirror=True)` 后，`plans.price=99`；`sync=False` 时不写回 |
| T9 | **admin-only 守卫** | 非 platform admin 调用 4 个端点均返回 **403** |
| T10 | **Enterprise 无默认规则** | `get_active_pricing_rule('plan_enterprise')` = `None`；`get_plan_pricing('plan_enterprise').active_rule` = `None`；镜像列 `NULL` |
| T11 | **非法枚举** | `subject_type/pricing_type/status` 非法值 → `create` 抛 `ValueError`（422） |

---

## 7. 受影响文件清单

| 文件 | 改动类型 | 改动内容 |
| --- | --- | --- |
| `backend/app/database.py` | 改 | 新增 `pricing_rules` DDL + 索引；`plans` 镜像列 ALTER（pragma 探测）；默认订阅价 seed（Free/Pro） |
| `backend/app/billing_store.py` | 改 | 新增 3 个枚举常量 + `_pricing_rule_dto` / `create_pricing_rule` / `update_pricing_rule` / `list_pricing_rules` / `get_active_pricing_rule` / `get_plan_pricing` / `_get_pricing_rule_row` |
| `backend/app/main.py` | 改 | 新增 `PricingRuleCreateIn` / `PricingRuleUpdateIn` + 4 个 platform 路由（全 `_require_platform_admin`） |
| `backend/tests/test_phase9a_p0_pricing_rule.py` | **新** | 覆盖 §6 测试矩阵（T1–T11） |

### 7.1 明确**不涉及**（红线隔离）

- ❌ **Workspace 执行链**：`workflow_runtime.py` / `orchestrator.py` / `employee_instances` 写入 / `tool_executor` — 不读不写。
- ❌ **Credential Vault**：`credential_vault.py` 明文语义不动。
- ❌ **Workflow / Employee Runtime / Usage Event**：`workflow_runs` / `evolution_events` 不新增写路径。
- ❌ **Shared Contract**：`plans` 镜像列属 Admin 商业表 additive 扩展（§2.2 判定），不改变 `plans` 契约语义、不影响 Workspace。
- ❌ **Payment / Invoice / Marketplace / Promotion / Value Pricing / ROI**：本 Issue 禁止区，零实现。

---

## 8. 验收对照（实现 ↔ 契约）

| 契约条款 | 实现落点 |
| --- | --- |
| 契约 §1 字段 | §1 DDL 列 + §3.1 `_pricing_rule_dto` |
| 契约 §2 Plan↔PricingRule 1:N | §1 DDL `plan_id` FK 关联；§3.5 解析 |
| 契约 §3 当前生效价算法 | §3.5 `get_active_pricing_rule` |
| 契约 §3 新覆盖旧（不删历史） | §3.2 `create_pricing_rule` 的 expire+回填 |
| 契约 §3 禁止改 active 金额 | §3.3 `update_pricing_rule` 校验 |
| 契约 §4 四端点 | §4.2 路由 |
| 契约 §5 `pricing_rules` 表 | §1 DDL |
| 契约 §6 仅 subscription | seed / 路由仅处理 `subscription` |
| 契约 §7 红线 | §7.1 不涉及清单 |
| 契约 §2 镜像列判定 | §2.2 判定表 |

---

*—— Phase-9A P0 Subscription Pricing Rule 实现设计（纯设计蓝图，无 .py/.js 源码）。工程师依此落地；不提交 git、不写业务代码于本文件。*
