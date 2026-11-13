"""Phase-8 Billing MVP (issue P8): 计费数据访问层。

`BillingStore` 持有 `Database` 引用，封装 plans / quotas / usage 聚合 /
billing_events 的纯 SQL 读写。所有方法：

* 仅 SELECT / INSERT / UPDATE，零出站调用；
* 用量字段（current_usage）采用**读时聚合**（query-time aggregation），
  对 `evolution_events`（token / capability / employee / workflow 派生源）
  做 GROUP BY + SUM，天然与「期末从原始事件重算」同源；
* 绝不 import `credential_vault`、绝不读取 `tenant_private` 明文，
  仅聚合脱敏字段（credential_id / credential_ref_digest）；
* 不引用 value_event、不计算 ROI；billing_event 的 amount 为非权威估算；
* 所有 SQL 用 `?` 占位符参数化，杜绝拼接注入。
"""

from __future__ import annotations

from collections import defaultdict
import json
import sqlite3
import uuid
from typing import Any

from .usage_meter import UsageMeterService

_VALID_PLAN_STATUSES = frozenset({"draft", "active", "deprecated", "archived"})
_VALID_PLAN_TIERS = frozenset({"free", "pro", "enterprise"})
_VALID_BILLING_INTERVALS = frozenset({"monthly", "annual", "custom"})
_VALID_QUOTA_TYPES = frozenset({"token", "employee_seat", "capability", "workflow"})
_VALID_BILLING_EVENT_STATUSES = frozenset({"draft", "calculated", "issued"})

# ── Phase-9A P0：PricingRule 枚举（与既有 _VALID_* frozenset 风格一致）──
_VALID_PRICING_SUBJECT_TYPES = frozenset({"subscription", "capability", "employee", "connector", "template"})
_VALID_PRICING_TYPES = frozenset({"fixed", "discount", "override"})
_VALID_PRICING_RULE_STATUSES = frozenset({"draft", "active", "expired", "disabled"})

# ── Phase-9A P1：QuotaRule 枚举（与既有 _VALID_* frozenset 风格一致）──
_VALID_QUOTA_RULE_TYPES = frozenset(
    {"token_limit", "employee_seat_limit", "workflow_limit", "capability_limit", "connector_limit"}
)
_VALID_ENFORCEMENT_MODES = frozenset({"notify", "throttle", "block", "billing_only"})
_VALID_QUOTA_RULE_PERIODS = frozenset({"daily", "monthly", "annual", "none"})
_VALID_QUOTA_RULE_STATUSES = frozenset({"draft", "active", "disabled"})
_VALID_PACKAGE_STATUSES = frozenset({"draft", "active", "disabled"})
_VALID_PACKAGE_AVAILABILITY = frozenset({"public", "tenant_invite_only", "enterprise_only"})


def _parse_json(raw: Any, default: Any) -> Any:
    """Parse a JSON column, falling back to ``default`` on empty / malformed input."""
    if raw is None or raw == "":
        return default
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return default


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class BillingStore:
    """Data-access layer for the Phase-8 Billing MVP entities.

    Holds a reference to the shared :class:`Database` instance (created once in
    ``main.create_app``). No credentials, no outbound calls, no Workspace writes.
    """

    def __init__(self, database: "Any") -> None:
        self.db = database

    # ──────────────────────────────────────────────────────────────
    # Plan management
    # ──────────────────────────────────────────────────────────────

    def _plan_dto(self, row: "Any") -> dict[str, Any]:
        return {
            "plan_id": row["plan_id"],
            "plan_code": row["plan_code"],
            "name": row["name"],
            "tier": row["tier"],
            "status": row["status"],
            "version": row["version"],
            "billing_interval": row["billing_interval"],
            "features": _parse_json(row["features_json"], []),
            "quota_rules": _parse_json(row["quota_rules_json"], {}),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def list_plans(self) -> list[dict[str, Any]]:
        """Return all plans ordered by plan_code (free, pro, enterprise)."""
        with self.db.connect() as connection:
            rows = connection.execute(
                "select * from plans order by plan_code"
            ).fetchall()
        return [self._plan_dto(row) for row in rows]

    def get_plan(self, plan_id: str) -> dict[str, Any] | None:
        with self.db.connect() as connection:
            row = connection.execute(
                "select * from plans where plan_id = ?", (plan_id,)
            ).fetchone()
        return self._plan_dto(row) if row is not None else None

    def get_plan_by_code(self, code: str) -> dict[str, Any] | None:
        with self.db.connect() as connection:
            row = connection.execute(
                "select * from plans where plan_code = ?", (code,)
            ).fetchone()
        return self._plan_dto(row) if row is not None else None

    def create_plan(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new plan. ``plan_code`` is unique (IntegrityError on dup)."""
        plan_code = kwargs.get("plan_code")
        if not plan_code:
            raise ValueError("plan_code 为必填")
        name = kwargs.get("name", "")
        tier = kwargs.get("tier", "free")
        status = kwargs.get("status", "draft")
        version = kwargs.get("version", "1.0.0")
        billing_interval = kwargs.get("billing_interval", "monthly")
        features = kwargs.get("features", [])
        quota_rules = kwargs.get("quota_rules", {})
        if tier not in _VALID_PLAN_TIERS:
            raise ValueError(f"非法的 tier: {tier!r}")
        if status not in _VALID_PLAN_STATUSES:
            raise ValueError(f"非法的 status: {status!r}")
        if billing_interval not in _VALID_BILLING_INTERVALS:
            raise ValueError(f"非法的 billing_interval: {billing_interval!r}")

        plan_id = f"plan_{uuid.uuid4().hex}"
        features_json = json.dumps(features, ensure_ascii=False)
        quota_rules_json = json.dumps(quota_rules, ensure_ascii=False)
        with self.db.connect() as connection:
            connection.execute(
                "insert into plans "
                "(plan_id, plan_code, name, tier, status, version, billing_interval, features_json, quota_rules_json) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    plan_id,
                    plan_code,
                    name,
                    tier,
                    status,
                    version,
                    billing_interval,
                    features_json,
                    quota_rules_json,
                ),
            )
            row = connection.execute(
                "select * from plans where plan_id = ?", (plan_id,)
            ).fetchone()
        return self._plan_dto(row)

    def update_plan(self, plan_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update mutable plan fields. Only provided (non-None) fields are written."""
        allowed_scalars = {
            "name": "name",
            "tier": "tier",
            "status": "status",
            "version": "version",
            "billing_interval": "billing_interval",
        }
        sets: list[str] = []
        params: list[Any] = []
        for key, column in allowed_scalars.items():
            if key in kwargs and kwargs[key] is not None:
                value = kwargs[key]
                if key == "tier" and value not in _VALID_PLAN_TIERS:
                    raise ValueError(f"非法的 tier: {value!r}")
                if key == "status" and value not in _VALID_PLAN_STATUSES:
                    raise ValueError(f"非法的 status: {value!r}")
                if key == "billing_interval" and value not in _VALID_BILLING_INTERVALS:
                    raise ValueError(f"非法的 billing_interval: {value!r}")
                sets.append(f"{column} = ?")
                params.append(value)
        if kwargs.get("features") is not None:
            sets.append("features_json = ?")
            params.append(json.dumps(kwargs["features"], ensure_ascii=False))
        if kwargs.get("quota_rules") is not None:
            sets.append("quota_rules_json = ?")
            params.append(json.dumps(kwargs["quota_rules"], ensure_ascii=False))

        if not sets:
            existing = self.get_plan(plan_id)
            if existing is None:
                raise KeyError(plan_id)
            return existing

        sets.append("updated_at = current_timestamp")
        params.append(plan_id)
        with self.db.connect() as connection:
            connection.execute(
                f"update plans set {', '.join(sets)} where plan_id = ?",
                params,
            )
            row = connection.execute(
                "select * from plans where plan_id = ?", (plan_id,)
            ).fetchone()
        if row is None:
            raise KeyError(plan_id)
        return self._plan_dto(row)

    def set_plan_status(self, plan_id: str, status: str) -> dict[str, Any]:
        if status not in _VALID_PLAN_STATUSES:
            raise ValueError(f"非法的 status: {status!r}")
        with self.db.connect() as connection:
            connection.execute(
                "update plans set status = ?, updated_at = current_timestamp where plan_id = ?",
                (status, plan_id),
            )
            row = connection.execute(
                "select * from plans where plan_id = ?", (plan_id,)
            ).fetchone()
        if row is None:
            raise KeyError(plan_id)
        return self._plan_dto(row)

    # ──────────────────────────────────────────────────────────────
    # Pricing rule management (Phase-9A P0): pricing_rules 为价格权威，
    # plans.price/price_currency/billing_cycle 仅镜像（由 active rule 派生写入）。
    # 全部纯 SQL、? 占位、row→dict，不触 Workspace / Credential Vault。
    # ──────────────────────────────────────────────────────────────

    def _pricing_rule_dto(self, row: "Any") -> dict[str, Any]:
        """Map a ``pricing_rules`` row to its API/contract dict representation."""
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

    def _get_pricing_rule_row(self, rule_id: str) -> "Any | None":
        """Fetch a raw ``pricing_rules`` row by id (or ``None``)."""
        with self.db.connect() as connection:
            return connection.execute(
                "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
            ).fetchone()

    def _expire_old_active_fixed_rules(
        self, plan_id: str, subject_type: str, exclude_rule_id: "str | None" = None
    ) -> None:
        """将同 ``plan_id`` + ``subject_type`` 下，其它 active 的固定价规则置 ``expired``。

        回填 ``effective_end=now`` 与 ``updated_at=now``，实现「新覆盖旧」而**不删除**任何
        历史价格记录。``exclude_rule_id`` 用于排除正在激活的当前规则自身（避免把它也过期掉）。
        """
        sql = (
            "update pricing_rules set status='expired', effective_end=current_timestamp, "
            "updated_at=current_timestamp "
            "where plan_id=? and subject_type=? and pricing_type='fixed' and status='active'"
        )
        params: list[Any] = [plan_id, subject_type]
        if exclude_rule_id is not None:
            sql += " and pricing_rule_id != ?"
            params.append(exclude_rule_id)
        with self.db.connect() as connection:
            connection.execute(sql, params)

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
        """Create a pricing rule.

        If ``pricing_type='fixed'`` and ``status='active'``, any existing active
        fixed rule for the same plan + subject_type is first retired
        (``status='expired'`` + ``effective_end=now``) — new overrides old, history
        is preserved (never physically deleted).
        """
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
                self._expire_old_active_fixed_rules(plan_id, subject_type)
            connection.execute(
                "insert into pricing_rules "
                "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
                "billing_cycle, effective_start, effective_end, status) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    rule_id,
                    subject_type,
                    pricing_type,
                    plan_id,
                    float(amount),
                    currency,
                    billing_cycle,
                    effective_start,
                    effective_end,
                    status,
                ),
            )
            row = connection.execute(
                "select * from pricing_rules where pricing_rule_id = ?", (rule_id,)
            ).fetchone()
        return self._pricing_rule_dto(row)

    def update_pricing_rule(self, rule_id: str, **fields: "Any") -> dict[str, Any]:
        """Update mutable fields of a pricing rule.

        Only draft / not-yet-active records may change their mutable fields.
        An already-``active`` historical record is forbidden from changing its
        ``amount`` (must be expired and recreated instead).

        Activation-cover: when the update turns a rule into ``active`` + ``fixed``
        while it was NOT already ``active`` + ``fixed`` (e.g. a draft fixed rule
        activated via ``status='active'``), any other ``active`` fixed rule for the
        same ``plan_id`` + ``subject_type`` is retired to ``expired`` (history
        preserved, never deleted) before this rule is written as ``active``. The
        rule itself is always excluded from that retirement.
        """
        existing = self._get_pricing_rule_row(rule_id)
        if existing is None:
            raise KeyError(rule_id)
        is_active_history = existing["status"] == "active"

        # 解析更新后的目标状态/类型（未提供的字段沿用既有值）。
        post_status = fields["status"] if fields.get("status") is not None else existing["status"]
        post_pricing_type = (
            fields["pricing_type"]
            if fields.get("pricing_type") is not None
            else existing["pricing_type"]
        )
        # 覆盖触发条件：更新后将变为 active+fixed，且原本并非 active+fixed。
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
        # 覆盖触发：先把同 plan+subject 其它 active 固定价置 expired（排除自身），
        # 随后当前规则被 UPDATE 为 active（状态来自请求的 post_status）。
        if trigger_cover:
            self._expire_old_active_fixed_rules(plan_id=existing["plan_id"], subject_type=existing["subject_type"], exclude_rule_id=rule_id)
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

    def list_pricing_rules(
        self,
        plan_id: "str | None" = None,
        subject_type: "str | None" = None,
        status: "str | None" = None,
    ) -> list[dict[str, Any]]:
        """List pricing rules, optionally filtered by plan / subject_type / status."""
        sql = "select * from pricing_rules"
        clauses: list[str] = []
        params: list[Any] = []
        if plan_id:
            clauses.append("plan_id = ?")
            params.append(plan_id)
        if subject_type:
            clauses.append("subject_type = ?")
            params.append(subject_type)
        if status:
            clauses.append("status = ?")
            params.append(status)
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by plan_id, effective_start desc, created_at desc"
        with self.db.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._pricing_rule_dto(row) for row in rows]

    def get_active_pricing_rule(
        self,
        plan_id: str,
        subject_type: str = "subscription",
        pricing_type: str = "fixed",
        as_of: "str | None" = None,
    ) -> "dict[str, Any] | None":
        """Return the currently-active rule for a plan.

        The active rule satisfies: subject_type + pricing_type + status='active' +
        effective window covering ``as_of`` (or now), newest first. ``None`` if none.
        """
        if as_of is None:
            time_clause = (
                "effective_start <= current_timestamp "
                "and (effective_end is null or effective_end >= current_timestamp)"
            )
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

    def get_plan_pricing(self, plan_id: str, sync_mirror: bool = False) -> dict[str, Any]:
        """Return a plan's pricing view: active_rule + plans mirror columns.

        When ``sync_mirror=True`` and an active rule exists, derived values are
        written back to the ``plans`` mirror columns (display only, never authoritative).
        """
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
            "active_rule": active_rule,  # None = 无生效订阅价（如 Enterprise）
            "mirror_price": mirror["mirror_price"],
            "mirror_currency": mirror["mirror_currency"],
            "mirror_billing_cycle": mirror["mirror_billing_cycle"],
        }

    # ──────────────────────────────────────────────────────────────
    # QuotaRule management (Phase-9A P1): quota_rules 为计划级配额权威，
    # quotas 实例层结构不变。全部纯 SQL、? 占位、row→dict，不触 Workspace /
    # Credential Vault / Employee Runtime。枚举校验集中于此，违例 → ValueError。
    # ──────────────────────────────────────────────────────────────

    def _quota_rule_dto(self, row: "Any") -> dict[str, Any]:
        """quota_rules 行 → API/契约 dict。"""
        return {
            "quota_rule_id": row["quota_rule_id"],
            "plan_id": row["plan_id"],
            "quota_type": row["quota_type"],
            "limit_value": row["limit_value"],  # 可能为 None（NULL = 不限）
            "is_unlimited": bool(row["is_unlimited"]),
            "period": row["period"],
            "enforcement_mode": row["enforcement_mode"],
            "status": row["status"],
            "source_scope": _parse_json(row["source_scope_json"], []),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _get_quota_rule_row(self, rule_id: str) -> "Any | None":
        """按 quota_rule_id 取原始行（或 ``None``）。"""
        with self.db.connect() as connection:
            return connection.execute(
                "select * from quota_rules where quota_rule_id = ?", (rule_id,)
            ).fetchone()

    def _expire_old_active_quota_rules(
        self, plan_id: str, quota_type: str, exclude_rule_id: "str | None" = None
    ) -> None:
        """将同 ``plan_id`` + ``quota_type`` 下，其它 active 的规则置 ``disabled``。

        历史记录保留（不物理删除），实现「新覆盖旧」的语义。``exclude_rule_id``
        用于排除正在激活的当前规则自身（避免把它也过期掉）。
        """
        sql = (
            "update quota_rules set status='disabled', updated_at=current_timestamp "
            "where plan_id=? and quota_type=? and status='active'"
        )
        params: list[Any] = [plan_id, quota_type]
        if exclude_rule_id is not None:
            sql += " and quota_rule_id != ?"
            params.append(exclude_rule_id)
        with self.db.connect() as connection:
            connection.execute(sql, params)

    def create_quota_rule(
        self,
        plan_id: str,
        quota_type: str,
        limit_value: "int | None" = None,
        is_unlimited: bool = False,
        period: str = "monthly",
        enforcement_mode: str = "notify",
        source_scope: "list[str] | None" = None,
        status: str = "draft",
    ) -> dict[str, Any]:
        """Create a plan-level quota rule.

        If ``status='active'`` and another active rule already exists for the same
        ``plan_id`` + ``quota_type`` (enforced by the partial unique index
        ``idx_quota_rules_plan_type_active``), that old active rule is retired to
        ``disabled`` first — new overrides old, history preserved (never deleted).
        """
        if quota_type not in _VALID_QUOTA_RULE_TYPES:
            raise ValueError(f"非法的 quota_type: {quota_type!r}")
        if period not in _VALID_QUOTA_RULE_PERIODS:
            raise ValueError(f"非法的 period: {period!r}")
        if enforcement_mode not in _VALID_ENFORCEMENT_MODES:
            raise ValueError(f"非法的 enforcement_mode: {enforcement_mode!r}")
        if status not in _VALID_QUOTA_RULE_STATUSES:
            raise ValueError(f"非法的 status: {status!r}")

        rule_id = f"qr_{uuid.uuid4().hex}"
        source_scope_json = json.dumps(source_scope or [], ensure_ascii=False)
        with self.db.connect() as connection:
            # 新 active 覆盖旧：同 plan+type 旧 active → disabled（排除自身）
            if status == "active":
                self._expire_old_active_quota_rules(plan_id, quota_type)
            connection.execute(
                "insert into quota_rules "
                "(quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, "
                " period, enforcement_mode, status, source_scope_json) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    rule_id,
                    plan_id,
                    quota_type,
                    limit_value,
                    int(is_unlimited),
                    period,
                    enforcement_mode,
                    status,
                    source_scope_json,
                ),
            )
            row = connection.execute(
                "select * from quota_rules where quota_rule_id = ?", (rule_id,)
            ).fetchone()
        return self._quota_rule_dto(row)

    def update_quota_rule(self, rule_id: str, **fields: "Any") -> dict[str, Any]:
        """Update mutable fields of a quota rule (partial update).

        Only draft / not-yet-active records may change ``limit_value``. An
        already-``active`` historical record is forbidden from changing its
        ``limit_value`` (must be disabled and recreated instead).

        Activation-cover: when the update turns a rule into ``active`` (while it was
        NOT already ``active``), any other ``active`` rule for the same ``plan_id`` +
        ``quota_type`` is retired to ``disabled`` (history preserved, never deleted)
        before this rule is written as ``active``. The rule itself is always excluded.
        """
        existing = self._get_quota_rule_row(rule_id)
        if existing is None:
            raise KeyError(rule_id)
        is_active_history = existing["status"] == "active"

        # 解析更新后的目标状态（未提供的字段沿用既有值）。
        post_status = fields["status"] if fields.get("status") is not None else existing["status"]
        # 覆盖触发条件：更新后将变为 active，且原本并非 active。
        trigger_cover = post_status == "active" and existing["status"] != "active"

        allowed_enums = {
            "period": _VALID_QUOTA_RULE_PERIODS,
            "enforcement_mode": _VALID_ENFORCEMENT_MODES,
            "status": _VALID_QUOTA_RULE_STATUSES,
        }
        sets: list[str] = []
        params: list[Any] = []
        # 标量枚举字段
        for key in ("period", "enforcement_mode", "status"):
            if key in fields and fields[key] is not None:
                value = fields[key]
                if value not in allowed_enums[key]:
                    raise ValueError(f"非法的 {key}: {value!r}")
                sets.append(f"{key} = ?")
                params.append(value)
        # is_unlimited
        if fields.get("is_unlimited") is not None:
            sets.append("is_unlimited = ?")
            params.append(1 if fields["is_unlimited"] else 0)
        # source_scope（准入型专用白名单）
        if fields.get("source_scope") is not None:
            sets.append("source_scope_json = ?")
            params.append(json.dumps(fields["source_scope"], ensure_ascii=False))
        # limit_value：已 active 历史禁止改
        if fields.get("limit_value") is not None:
            if is_active_history:
                raise ValueError("已生效(active)配额规则不允许修改 limit_value，请 disable 后新建")
            sets.append("limit_value = ?")
            params.append(fields["limit_value"])

        if not sets:
            return self._quota_rule_dto(existing)
        # 覆盖触发：先把同 plan+type 其它 active 置 disabled（排除自身），
        # 随后当前规则被 UPDATE 为 active（状态来自请求的 post_status）。
        if trigger_cover:
            self._expire_old_active_quota_rules(
                plan_id=existing["plan_id"],
                quota_type=existing["quota_type"],
                exclude_rule_id=rule_id,
            )
        sets.append("updated_at = current_timestamp")
        params.append(rule_id)
        with self.db.connect() as connection:
            connection.execute(
                f"update quota_rules set {', '.join(sets)} where quota_rule_id = ?",
                params,
            )
            row = connection.execute(
                "select * from quota_rules where quota_rule_id = ?", (rule_id,)
            ).fetchone()
        if row is None:
            raise KeyError(rule_id)
        return self._quota_rule_dto(row)

    def list_quota_rules(
        self,
        plan_id: "str | None" = None,
        quota_type: "str | None" = None,
        status: "str | None" = None,
        enforcement_mode: "str | None" = None,
    ) -> list[dict[str, Any]]:
        """List quota rules, optionally filtered by plan / type / status / enforcement."""
        sql = "select * from quota_rules"
        clauses: list[str] = []
        params: list[Any] = []
        if plan_id:
            clauses.append("plan_id = ?")
            params.append(plan_id)
        if quota_type:
            clauses.append("quota_type = ?")
            params.append(quota_type)
        if status:
            clauses.append("status = ?")
            params.append(status)
        if enforcement_mode:
            clauses.append("enforcement_mode = ?")
            params.append(enforcement_mode)
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by plan_id, quota_type, created_at desc"
        with self.db.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._quota_rule_dto(row) for row in rows]

    def get_active_quota_rule(
        self, plan_id: str, quota_type: str
    ) -> "dict[str, Any] | None":
        """Return the currently-active rule for a plan + quota_type (or ``None``).

        Uniqueness is guaranteed by the partial unique index
        ``idx_quota_rules_plan_type_active`` (only one ``active`` per plan+type).
        """
        with self.db.connect() as connection:
            row = connection.execute(
                "select * from quota_rules "
                "where plan_id = ? and quota_type = ? and status = 'active'",
                (plan_id, quota_type),
            ).fetchone()
        return self._quota_rule_dto(row) if row is not None else None

    # ──────────────────────────────────────────────────────────────
    # Capability Package Commercial Configuration (Phase-9A P2)
    # ──────────────────────────────────────────────────────────────
    def _capability_package_dto(self, row: "Any") -> dict[str, Any]:
        """capability_packages 行 → API/契约 dict（JSON 数组字段还原为 list）。"""
        return {
            "package_id": row["package_id"],
            "name": row["name"],
            "description": row["description"],
            "capability_ids": _parse_json(row["capability_ids"], []),
            "connector_ids": _parse_json(row["connector_ids"], []),
            "workflow_template_ids": _parse_json(row["workflow_template_ids"], []),
            "employee_template_ids": _parse_json(row["employee_template_ids"], []),
            "pricing_reference": row["pricing_reference"],
            "quota_reference": row["quota_reference"],
            "availability": row["availability"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _get_capability_package_row(self, package_id: str) -> "Any | None":
        """按 package_id 取原始行（或 ``None``）。"""
        with self.db.connect() as connection:
            return connection.execute(
                "select * from capability_packages where package_id = ?", (package_id,)
            ).fetchone()

    @staticmethod
    def _validate_json_id_list(value: "Any", field: str) -> list[str]:
        """capability_ids/connector_ids/... 必须是字符串数组（或 None→空）。"""
        if value is None:
            return []
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise ValueError(f"{field} 必须是字符串数组")
        return value

    def create_capability_package(
        self,
        name: str,
        description: str = "",
        capability_ids: "list[str] | None" = None,
        connector_ids: "list[str] | None" = None,
        workflow_template_ids: "list[str] | None" = None,
        employee_template_ids: "list[str] | None" = None,
        pricing_reference: "str | None" = None,
        quota_reference: "str | None" = None,
        availability: str = "public",
        status: str = "draft",
    ) -> dict[str, Any]:
        """Create an official capability package (commercial configuration).

        ``pricing_reference`` / ``quota_reference`` point to a ``plan_id`` whose
        ``pricing_rules`` / ``quota_rules`` define the package's price and quotas.
        Composition references (capability/connector/workflow_template/employee
        template ids) are stored as JSON arrays; referential integrity is validated
        at Admin config time, not enforced at runtime (no FK).
        """
        if not name:
            raise ValueError("package name 不能为空")
        if availability not in _VALID_PACKAGE_AVAILABILITY:
            raise ValueError(f"非法的 availability: {availability!r}")
        if status not in _VALID_PACKAGE_STATUSES:
            raise ValueError(f"非法的 status: {status!r}")
        capability_ids = self._validate_json_id_list(capability_ids, "capability_ids")
        connector_ids = self._validate_json_id_list(connector_ids, "connector_ids")
        workflow_template_ids = self._validate_json_id_list(workflow_template_ids, "workflow_template_ids")
        employee_template_ids = self._validate_json_id_list(employee_template_ids, "employee_template_ids")

        package_id = f"cp_{uuid.uuid4().hex}"
        with self.db.connect() as connection:
            connection.execute(
                "insert into capability_packages "
                "(package_id, name, description, capability_ids, connector_ids, "
                " workflow_template_ids, employee_template_ids, pricing_reference, "
                " quota_reference, availability, status) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    package_id,
                    name,
                    description,
                    json.dumps(capability_ids, ensure_ascii=False),
                    json.dumps(connector_ids, ensure_ascii=False),
                    json.dumps(workflow_template_ids, ensure_ascii=False),
                    json.dumps(employee_template_ids, ensure_ascii=False),
                    pricing_reference,
                    quota_reference,
                    availability,
                    status,
                ),
            )
            row = connection.execute(
                "select * from capability_packages where package_id = ?", (package_id,)
            ).fetchone()
        return self._capability_package_dto(row)

    def update_capability_package(self, package_id: str, **fields: "Any") -> dict[str, Any]:
        """Update mutable fields of a capability package (partial update)."""
        existing = self._get_capability_package_row(package_id)
        if existing is None:
            raise KeyError(package_id)

        allowed_enums = {
            "availability": _VALID_PACKAGE_AVAILABILITY,
            "status": _VALID_PACKAGE_STATUSES,
        }
        sets: list[str] = []
        params: list[Any] = []

        # 标量枚举字段
        for key in ("availability", "status"):
            if key in fields and fields[key] is not None:
                value = fields[key]
                if value not in allowed_enums[key]:
                    raise ValueError(f"非法的 {key}: {value!r}")
                sets.append(f"{key} = ?")
                params.append(value)

        # 标量文本字段
        for key in ("name", "description", "pricing_reference", "quota_reference"):
            if key in fields and fields[key] is not None:
                sets.append(f"{key} = ?")
                params.append(fields[key])

        # JSON 数组字段
        for key in ("capability_ids", "connector_ids", "workflow_template_ids", "employee_template_ids"):
            if key in fields and fields[key] is not None:
                ids = self._validate_json_id_list(fields[key], key)
                sets.append(f"{key} = ?")
                params.append(json.dumps(ids, ensure_ascii=False))

        if not sets:
            return self._capability_package_dto(existing)
        sets.append("updated_at = current_timestamp")
        params.append(package_id)
        with self.db.connect() as connection:
            connection.execute(
                f"update capability_packages set {', '.join(sets)} where package_id = ?",
                params,
            )
            row = connection.execute(
                "select * from capability_packages where package_id = ?", (package_id,)
            ).fetchone()
        if row is None:
            raise KeyError(package_id)
        return self._capability_package_dto(row)

    def list_capability_packages(
        self,
        status: "str | None" = None,
        availability: "str | None" = None,
        name: "str | None" = None,
    ) -> list[dict[str, Any]]:
        """List capability packages, optionally filtered by status/availability/name."""
        sql = "select * from capability_packages"
        clauses: list[str] = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if availability:
            clauses.append("availability = ?")
            params.append(availability)
        if name:
            clauses.append("name like ?")
            params.append(f"%{name}%")
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by created_at desc"
        with self.db.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._capability_package_dto(row) for row in rows]

    def get_capability_package(self, package_id: str) -> dict[str, Any]:
        """Return a single package by id, or raise ``KeyError`` (→ 404) if missing."""
        row = self._get_capability_package_row(package_id)
        if row is None:
            raise KeyError(package_id)
        return self._capability_package_dto(row)

    # ──────────────────────────────────────────────────────────────
    # Quota management (config + read-time current_usage derivation)
    # ──────────────────────────────────────────────────────────────

    def _quota_dto(self, row: "Any") -> dict[str, Any]:
        return {
            "quota_id": row["quota_id"],
            "tenant_id": row["tenant_id"],
            "plan_id": row["plan_id"],
            "plan_code": row["plan_code"],
            "quota_type": row["quota_type"],
        "limit_value": _coerce_int(row["limit_value"], 0),
        "is_unlimited": bool(row["is_unlimited"]) if "is_unlimited" in (row.keys() if hasattr(row, "keys") else []) else False,
        "current_usage": _coerce_int(row["current_usage"], 0),
            "period": row["period"],
            "period_start": row["period_start"],
            "period_end": row["period_end"],
            "source_scope": _parse_json(row["source_scope_json"], []),
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def list_quotas(self, tenant_id: str) -> list[dict[str, Any]]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "select * from quotas where tenant_id = ? order by quota_type, period_start",
                (tenant_id,),
            ).fetchall()
        return [self._quota_dto(row) for row in rows]

    def get_quotas_for_tenant(self, tenant_id: str) -> list[dict[str, Any]]:
        """List quotas for a tenant, with ``current_usage`` re-derived at read time.

        The derived value is query-time aggregation (same source as a period-end
        recompute), so the panel always shows live usage without any Workspace
        write hook.
        """
        quotas = self.list_quotas(tenant_id)
        result: list[dict[str, Any]] = []
        for quota in quotas:
            usage = self.derive_current_usage(
                tenant_id,
                quota["quota_type"],
                quota["period_start"],
                quota["period_end"],
            )
            result.append({**quota, "current_usage": usage})
        return result

    def upsert_quota_limit(
        self,
        tenant_id: str,
        plan_id: str,
        quota_type: str,
        limit_value: int = 0,
        period: str = "monthly",
        period_start: str = "",
        period_end: str = "",
        source_scope: "list[str] | None" = None,
        is_unlimited: bool = False,          # ── Phase-9A NEW ──
    ) -> dict[str, Any]:
        """Create a quota instance from a plan (if absent) or update its limit.

        Matched on (tenant_id, quota_type, plan_id). The instance is never
        auto-created from thin air: it is always plan-derived (admin-config).
        """
        if quota_type not in _VALID_QUOTA_TYPES:
            raise ValueError(f"非法的 quota_type: {quota_type!r}")
        source_scope = source_scope or []
        u_flag = 1 if is_unlimited else 0
        with self.db.connect() as connection:
            plan_row = connection.execute(
                "select plan_code from plans where plan_id = ?", (plan_id,)
            ).fetchone()
            plan_code = plan_row["plan_code"] if plan_row is not None else "free"
            existing = connection.execute(
                "select * from quotas where tenant_id = ? and quota_type = ? and plan_id = ?",
                (tenant_id, quota_type, plan_id),
            ).fetchone()
            source_scope_json = json.dumps(source_scope, ensure_ascii=False)
            if existing is None:
                quota_id = f"quota_{uuid.uuid4().hex}"
                connection.execute(
                    "insert into quotas "
                    "(quota_id, tenant_id, plan_id, plan_code, quota_type, limit_value, "
                    "is_unlimited, period, period_start, period_end, source_scope_json) "
                    "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        quota_id,
                        tenant_id,
                        plan_id,
                        plan_code,
                        quota_type,
                        _coerce_int(limit_value, 0),
                        u_flag,
                        period,
                        period_start,
                        period_end,
                        source_scope_json,
                    ),
                )
                row = connection.execute(
                    "select * from quotas where quota_id = ?", (quota_id,)
                ).fetchone()
            else:
                connection.execute(
                    "update quotas set limit_value = ?, is_unlimited = ?, period = ?, "
                    "period_start = ?, period_end = ?, source_scope_json = ?, "
                    "updated_at = current_timestamp where quota_id = ?",
                    (
                        _coerce_int(limit_value, 0),
                        u_flag,
                        period,
                        period_start,
                        period_end,
                        source_scope_json,
                        existing["quota_id"],
                    ),
                )
                row = connection.execute(
                    "select * from quotas where quota_id = ?", (existing["quota_id"],)
                ).fetchone()
        return self._quota_dto(row)

    def update_quota(
        self,
        quota_id: str,
        limit_value: int,
        period: "str | None" = None,
        period_start: "str | None" = None,
        period_end: "str | None" = None,
        source_scope: "list[str] | None" = None,
        is_unlimited: "bool | None" = None,   # ── Phase-9A NEW ──
    ) -> dict[str, Any]:
        """Update an existing quota instance (by quota_id)."""
        sets: list[str] = ["limit_value = ?"]
        params: list[Any] = [_coerce_int(limit_value, 0)]
        if period is not None:
            sets.append("period = ?")
            params.append(period)
        if period_start is not None:
            sets.append("period_start = ?")
            params.append(period_start)
        if period_end is not None:
            sets.append("period_end = ?")
            params.append(period_end)
        if source_scope is not None:
            sets.append("source_scope_json = ?")
            params.append(json.dumps(source_scope, ensure_ascii=False))
        if is_unlimited is not None:
            sets.append("is_unlimited = ?")
            params.append(1 if is_unlimited else 0)
        sets.append("updated_at = current_timestamp")
        params.append(quota_id)
        with self.db.connect() as connection:
            connection.execute(
                f"update quotas set {', '.join(sets)} where quota_id = ?",
                params,
            )
            row = connection.execute(
                "select * from quotas where quota_id = ?", (quota_id,)
            ).fetchone()
        if row is None:
            raise KeyError(quota_id)
        return self._quota_dto(row)

    def _table_exists(self, table_name: str) -> bool:
        with self.db.connect() as connection:
            row = connection.execute(
                "select name from sqlite_master where type = 'table' and name = ?",
                (table_name,),
            ).fetchone()
        return row is not None

    def derive_current_usage(
        self, tenant_id: str, quota_type: str, period_start: str = "", period_end: str = ""
    ) -> int:
        """Read-time aggregate of current usage for a quota type.

        Defensive: if a source table does not exist (it does in this schema),
        the value falls back to 0 without raising.
        """
        if quota_type == "token":
            return self._derive_token_usage(tenant_id, period_start, period_end)
        if quota_type == "employee_seat":
            return self._derive_employee_seat_usage(tenant_id)
        if quota_type == "capability":
            return self._derive_capability_usage(tenant_id, period_start, period_end)
        if quota_type == "workflow":
            return self._derive_workflow_usage(tenant_id, period_start, period_end)
        return 0

    def _derive_token_usage(self, tenant_id: str, period_start: str, period_end: str) -> int:
        sql = (
            "select coalesce(sum(total_tokens), 0) as total "
            "from ai_usage_records where tenant_id = ?"
        )
        params: list[Any] = [tenant_id]
        if period_start and period_end:
            sql += " and occurred_at between ? and ?"
            params += [period_start, period_end]
        with self.db.connect() as connection:
            row = connection.execute(sql, params).fetchone()
        return int(row["total"]) if row is not None else 0

    def _derive_employee_seat_usage(self, tenant_id: str) -> int:
        if not self._table_exists("employee_instances"):
            return 0
        with self.db.connect() as connection:
            row = connection.execute(
                "select count(*) as cnt from employee_instances where tenant_id = ? and enabled = 1",
                (tenant_id,),
            ).fetchone()
        return int(row["cnt"]) if row is not None else 0

    def _derive_capability_usage(self, tenant_id: str, period_start: str, period_end: str) -> int:
        sources = self._tenant_capability_sources(tenant_id)
        sql = (
            "select count(*) as cnt from ai_usage_records r where r.tenant_id = ?"
        )
        params: list[Any] = [tenant_id]
        if period_start and period_end:
            sql += " and r.occurred_at between ? and ?"
            params += [period_start, period_end]
        if sources:
            placeholders = ",".join("?" for _ in sources)
            sql += (
                " and exists (select 1 from evolution_events e "
                "where e.tenant_id=r.tenant_id and e.event_type='usage.model_call' "
                "and json_extract(e.payload, '$.usage_record_id')=r.usage_record_id "
                f"and json_extract(e.payload, '$.capability_source') in ({placeholders}))"
            )
            params += list(sources)
        with self.db.connect() as connection:
            row = connection.execute(sql, params).fetchone()
        return int(row["cnt"]) if row is not None else 0

    def _derive_workflow_usage(self, tenant_id: str, period_start: str, period_end: str) -> int:
        if not self._table_exists("workflow_runs"):
            return 0
        sql = "select count(*) as cnt from workflow_runs where tenant_id = ?"
        params: list[Any] = [tenant_id]
        if period_start and period_end:
            sql += " and created_at between ? and ?"
            params += [period_start, period_end]
        with self.db.connect() as connection:
            row = connection.execute(sql, params).fetchone()
        return int(row["cnt"]) if row is not None else 0

    def _tenant_capability_sources(self, tenant_id: str) -> list[str]:
        """Resolve the active plan's capability whitelist for a tenant."""
        tenant = self.db.get_tenant(tenant_id)
        if tenant is None:
            return []
        plan_code = tenant.get("plan_tier") or "free"
        plan = self.get_plan_by_code(plan_code)
        if plan is None:
            return []
        rules = plan.get("quota_rules") or {}
        return list(rules.get("capability_sources") or [])

    def sync_quota_current_usage(self, quota_id: str) -> dict[str, Any]:
        """Re-derive and persist ``current_usage`` for a single quota instance."""
        with self.db.connect() as connection:
            row = connection.execute(
                "select * from quotas where quota_id = ?", (quota_id,)
            ).fetchone()
            if row is None:
                raise KeyError(quota_id)
            usage = self.derive_current_usage(
                row["tenant_id"],
                row["quota_type"],
                row["period_start"],
                row["period_end"],
            )
            connection.execute(
                "update quotas set current_usage = ?, updated_at = current_timestamp where quota_id = ?",
                (usage, quota_id),
            )
            row = connection.execute(
                "select * from quotas where quota_id = ?", (quota_id,)
            ).fetchone()
        return self._quota_dto(row)

    def recompute_quota_period(self, tenant_id: str, period: str = "monthly") -> list[dict[str, Any]]:
        """Refresh current_usage for every quota of a tenant in the given period.

        Reserved interface: the MVP does not schedule a period-end job, but this
        method lets an operator (or future scheduler) trigger the same
        query-time aggregation used by the read path.
        """
        quotas = self.list_quotas(tenant_id)
        result: list[dict[str, Any]] = []
        for quota in quotas:
            if period and quota["period"] != period:
                continue
            try:
                result.append(self.sync_quota_current_usage(quota["quota_id"]))
            except KeyError:
                continue
        return result

    # ──────────────────────────────────────────────────────────────
    # Usage aggregation (read-only, desensitized)
    # ──────────────────────────────────────────────────────────────

    def usage_summary(
        self, tenant_id: str, period_start: str = "", period_end: str = ""
    ) -> dict[str, Any]:
        """Aggregate usage for a tenant across model / capability / employee / workflow.

        Only desensitized fields are returned (never plaintext credentials or
        tenant_private content). ``credential_id`` / ``credential_ref_digest``
        may appear if present in the payload, but are never expanded.
        """
        where = "from ai_usage_records r where r.tenant_id = ?"
        params: list[Any] = [tenant_id]
        if period_start and period_end:
            where += " and r.occurred_at between ? and ?"
            params += [period_start, period_end]

        with self.db.connect() as connection:
            totals_row = connection.execute(
                "select "
                "coalesce(sum(r.total_tokens), 0) as total_tokens, "
                "count(*) as event_count "
                + where,
                params,
            ).fetchone()
            cost_rows = [dict(row) for row in connection.execute(
                "select r.model_name,r.cost_amount,r.cost_source,r.currency " + where, params).fetchall()]
            model_costs = defaultdict(list)
            for row in cost_rows:
                model_costs[row["model_name"]].append(row)
            by_model = connection.execute(
                "select "
                "r.model_name, "
                "coalesce(sum(r.total_tokens), 0) as total_tokens, "
                "count(*) as cnt "
                + where
                + " group by r.model_name"
                " order by total_tokens desc",
                params,
            ).fetchall()
            by_capability_source = connection.execute(
                "select coalesce(a.capability_source, '(unknown)') as capability_source, "
                "count(*) as cnt, coalesce(sum(r.total_tokens), 0) as total_tokens "
                "from ai_usage_records r left join ("
                "select tenant_id, json_extract(payload, '$.usage_record_id') as usage_record_id, "
                "max(json_extract(payload, '$.capability_source')) as capability_source "
                "from evolution_events where event_type='usage.model_call' "
                "group by tenant_id, json_extract(payload, '$.usage_record_id')"
                ") a on a.tenant_id=r.tenant_id and a.usage_record_id=r.usage_record_id "
                "where r.tenant_id = ?"
                + (" and r.occurred_at between ? and ?" if period_start and period_end else "")
                + " group by coalesce(a.capability_source, '(unknown)')"
                " order by cnt desc",
                params,
            ).fetchall()
            by_employee = connection.execute(
                "select r.employee_id, "
                "count(*) as cnt, "
                "coalesce(sum(r.total_tokens), 0) as total_tokens "
                + where
                + " group by r.employee_id"
                " order by cnt desc",
                params,
            ).fetchall()
            by_workflow = connection.execute(
                "select coalesce(r.workflow_run_id, '(unknown)') as workflow_run_id, "
                "count(*) as cnt, "
                "coalesce(sum(r.total_tokens), 0) as total_tokens "
                + where
                + " group by coalesce(r.workflow_run_id, '(unknown)')"
                " order by cnt desc",
                params,
            ).fetchall()

        def money(rows):
            facts = UsageMeterService._cost_totals(rows)
            return {"total_cost": facts.pop("estimated_cost"), **facts}

        return {
            "tenant_id": tenant_id,
            "period": {"period_start": period_start, "period_end": period_end},
            "totals": {
                "total_tokens": int(totals_row["total_tokens"]) if totals_row else 0,
                **money(cost_rows),
                "event_count": int(totals_row["event_count"]) if totals_row else 0,
            },
            "by_model": [
                {
                    "model_name": row["model_name"],
                    "total_tokens": int(row["total_tokens"]),
                    **money(model_costs[row["model_name"]]),
                    "count": int(row["cnt"]),
                }
                for row in by_model
            ],
            "by_capability_source": [
                {
                    "capability_source": row["capability_source"],
                    "count": int(row["cnt"]),
                    "total_tokens": int(row["total_tokens"]),
                }
                for row in by_capability_source
            ],
            "by_employee": [
                {
                    "employee_id": row["employee_id"],
                    "count": int(row["cnt"]),
                    "total_tokens": int(row["total_tokens"]),
                }
                for row in by_employee
            ],
            "by_workflow": [
                {
                    "workflow_run_id": row["workflow_run_id"],
                    "count": int(row["cnt"]),
                    "total_tokens": int(row["total_tokens"]),
                }
                for row in by_workflow
            ],
        }

    # ──────────────────────────────────────────────────────────────
    # Billing events (non-authoritative estimate; no payment side effects)
    # ──────────────────────────────────────────────────────────────

    def _billing_event_dto(self, row: "Any") -> dict[str, Any]:
        return {
            "billing_event_id": row["billing_event_id"],
            "tenant_id": row["tenant_id"],
            "plan_id": row["plan_id"],
            "plan_code": row["plan_code"],
            "subject_type": row["subject_type"],
            "subject_id": row["subject_id"],
            "amount": float(row["amount"]),
            "currency": row["currency"],
            "status": row["status"],
            "period_start": row["period_start"],
            "period_end": row["period_end"],
            "breakdown": _parse_json(row["breakdown_json"], {}),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def list_billing_events(
        self, tenant_id: "str | None" = None, status: "str | None" = None
    ) -> list[dict[str, Any]]:
        sql = "select * from billing_events"
        clauses: list[str] = []
        params: list[Any] = []
        if tenant_id:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if status:
            clauses.append("status = ?")
            params.append(status)
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by created_at desc, billing_event_id"
        with self.db.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._billing_event_dto(row) for row in rows]

    def calculate_billing_events(
        self,
        tenant_id: str,
        period_start: str = "",
        period_end: str = "",
        as_calculated: bool = True,
    ) -> list[dict[str, Any]]:
        """Generate draft/calculated billing events from usage × plan overage pricing.

        This is a NON-AUTHORITATIVE estimate for observability only. It never
        references value_event, never computes ROI, and never triggers any
        payment / invoice / deduction. ``issued`` status is set elsewhere (and
        has zero financial side effects).
        """
        tenant = self.db.get_tenant(tenant_id)
        if tenant is None:
            raise KeyError(tenant_id)
        plan_code = tenant.get("plan_tier") or "free"
        plan = self.get_plan_by_code(plan_code)
        if plan is None:
            raise ValueError(f"未找到 plan_code={plan_code!r} 对应的计划")
        rules = plan.get("quota_rules") or {}
        overage = rules.get("overage") or {}
        currency = rules.get("currency", "USD")
        status = "calculated" if as_calculated else "draft"

        usage_by_dim = {
            "token": self.derive_current_usage(tenant_id, "token", period_start, period_end),
            "employee_seat": self.derive_current_usage(tenant_id, "employee_seat", period_start, period_end),
            "workflow": self.derive_current_usage(tenant_id, "workflow", period_start, period_end),
            "capability": self.derive_current_usage(tenant_id, "capability", period_start, period_end),
        }

        dimensions = [
            ("token", _coerce_int(rules.get("token_monthly_limit"), 0), float(overage.get("token_unit_price_per_1k", 0) or 0), "per_1k"),
            ("employee_seat", _coerce_int(rules.get("seat_limit"), 0), float(overage.get("seat_unit_price", 0) or 0), "each"),
            ("workflow", _coerce_int(rules.get("workflow_monthly_limit"), 0), float(overage.get("workflow_unit_price", 0) or 0), "each"),
        ]

        # ── Phase-9A 修正：基于显式 quota_mode / is_unlimited 语义（不再用 limit==0 代表无限）──
        quota_mode = rules.get("quota_mode", "plan_default")  # plan_default | custom | unlimited
        is_plan_unlimited = bool(rules.get("is_unlimited", False))
        quota_instances: dict[str, Any] = {}
        if quota_mode == "custom":
            for q in self.get_quotas_for_tenant(tenant_id):  # 派生自 quotas 表，Admin 按企业配置
                quota_instances[q["quota_type"]] = q

        created_ids: list[str] = []
        plan_dimensions: dict[str, Any] = {}
        total_amount = 0.0
        with self.db.connect() as connection:
            for dim_name, plan_limit, price, unit in dimensions:
                # 解析该维度 limit 与 is_unlimited（custom 模式取租户实例）
                if quota_mode == "custom":
                    inst = quota_instances.get(dim_name)
                    if inst is None:
                        limit, is_unlimited, configured = 0, False, False  # 未配置：不产生超量，待 Admin 设置
                    else:
                        limit = inst["limit_value"]
                        is_unlimited = bool(inst.get("is_unlimited", False))
                        configured = True
                else:
                    limit, is_unlimited, configured = plan_limit, is_plan_unlimited, True

                usage = usage_by_dim[dim_name]
                # ── 核心修正：显式 is_unlimited 才为 0；limit<=0 一律 0 但非"无限"──
                if is_unlimited:
                    overage_qty = 0
                elif limit and limit > 0:
                    overage_qty = max(0, usage - limit)
                else:
                    overage_qty = 0
                amount = 0.0
                if overage_qty > 0:
                    amount = (overage_qty / 1000.0) * price if unit == "per_1k" else overage_qty * price
                amount = round(amount, 6)
                plan_dimensions[dim_name] = {
                    "limit": limit,
                    "usage": usage,
                    "overage": overage_qty,
                    "unit_price": price,
                    "amount": amount,
                    "currency": currency,
                    "configured": configured,          # ── NEW：标记是否已由 Admin 配置
                    "is_unlimited": is_unlimited,      # ── NEW
                }
                if amount > 0 and overage_qty > 0:
                    billing_event_id = f"be_{uuid.uuid4().hex}"
                    connection.execute(
                        "insert into billing_events "
                        "(billing_event_id, tenant_id, plan_id, plan_code, subject_type, subject_id, "
                        "amount, currency, status, period_start, period_end, breakdown_json) "
                        "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            billing_event_id,
                            tenant_id,
                            plan["plan_id"],
                            plan_code,
                            "quota_overage",
                            dim_name,
                            amount,
                            currency,
                            status,
                            period_start,
                            period_end,
                            json.dumps(
                                {
                                    "quota_type": dim_name,
                                    "limit": limit,
                                    "usage": usage,
                                    "overage": overage_qty,
                                    "unit_price": price,
                                    "currency": currency,
                                    "estimated": True,
                                    "configured": configured,
                                    "is_unlimited": is_unlimited,
                                },
                                ensure_ascii=False,
                            ),
                        ),
                    )
                    created_ids.append(billing_event_id)
                    total_amount += amount

            # Plan-level summary event (subject_type='plan') aggregating all overages.
            plan_breakdown = {
                "currency": currency,
                "period_start": period_start,
                "period_end": period_end,
                "estimated": True,
                "note": "非权威估算：仅基于 usage_event × quota_rules.overage，不触发任何资金动作",
                "capability_usage": usage_by_dim["capability"],
                "dimensions": plan_dimensions,
                "total_amount": round(total_amount, 6),
            }
            plan_event_id = f"be_{uuid.uuid4().hex}"
            connection.execute(
                "insert into billing_events "
                "(billing_event_id, tenant_id, plan_id, plan_code, subject_type, subject_id, "
                "amount, currency, status, period_start, period_end, breakdown_json) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    plan_event_id,
                    tenant_id,
                    plan["plan_id"],
                    plan_code,
                    "plan",
                    plan_code,
                    round(total_amount, 6),
                    currency,
                    status,
                    period_start,
                    period_end,
                    json.dumps(plan_breakdown, ensure_ascii=False),
                ),
            )
            created_ids.append(plan_event_id)

            placeholders = ",".join("?" for _ in created_ids)
            rows = connection.execute(
                f"select * from billing_events where billing_event_id in ({placeholders}) "
                f"order by created_at desc, billing_event_id",
                created_ids,
            ).fetchall()
        return [self._billing_event_dto(row) for row in rows]

    def set_billing_event_status(self, billing_event_id: str, status: str) -> dict[str, Any]:
        """Update a billing event's status. ``issued`` is a placeholder with no financial effect."""
        if status not in _VALID_BILLING_EVENT_STATUSES:
            raise ValueError(f"非法的 billing_event status: {status!r}")
        with self.db.connect() as connection:
            connection.execute(
                "update billing_events set status = ?, updated_at = current_timestamp where billing_event_id = ?",
                (status, billing_event_id),
            )
            row = connection.execute(
                "select * from billing_events where billing_event_id = ?", (billing_event_id,)
            ).fetchone()
        if row is None:
            raise KeyError(billing_event_id)
        return self._billing_event_dto(row)
