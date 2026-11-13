"""内部预算硬停护栏（Issue C）。

本模块是独立、自主的硬上限熔断机制，与 B 层闸引擎解耦：它仅基于
``total_tokens`` 做 ok / warn / hard_stop 三态判定，绝不引入价格 / 计费 /
套餐 / Quota。

设计铁律（全部满足，详见 issue-c-budget-guard-impl-plan.md §0.2）：
- 零新依赖：仅用 Python 标准库 + 项目既有 ``RealRDExecutorError``。
- 不解除人工批准闸：本模块不 import / 不调用任何解除批准闸的路径；仅吸收
  「硬上限熔断」这一安全子集，不采用预算内自主改码模型。
- 不碰 L2 冻结域：不引入 Marketplace / 真实计费 / 多租户 / 外部 Agent；
  BudgetGuard 仅基于 ``total_tokens``。
- 与 B 层治理共存：模块不 import 治理层；事件 ``a.budget.*`` 与既有审计事件
  并列独立追加写、不混。
- 脱敏贯穿：落库 payload 仅含 scope / status / ratio / limit 等聚合值 +
  脱敏范围键；无路径 / Key / 参数 / 原始 Secret。
- fail-closed 确定性：``enabled=true`` 且配置加载失败时，按 §3.1 穷尽组合
  给出唯一行为（硬停或自禁用），绝不视情况二选一。

导入约定：模块置于 ``backend/app/budget_guard.py``，调用方仅以
``from .budget_guard`` 或 ``from app.budget_guard`` 引用；绝不顶层
``import budget_guard``（保持 B 层守卫测试绿）。
"""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from dataclasses import dataclass
from typing import Any, NoReturn


# ---------------------------------------------------------------------------
# 常量（命名一致，见 impl-plan §7.3）
# ---------------------------------------------------------------------------
DEFAULT_MAX_TOKENS_PER_RUN = 100000
DEFAULT_WARN_RATIO = 0.8
DEFAULT_HARD_STOP_RATIO = 1.0
DEFAULT_FAIL_CLOSED = True
DEFAULT_SCOPE = "per_run"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "budget_guard_config.json")

# 累加表（仅在 database 传入且 scope=per_agent_session 时自管理建表）。
ACCUMULATOR_TABLE = "budget_guard_accumulators"

# 脱敏事件类型（与既有审计事件并列独立）。
EVENT_OK = "a.budget.ok"
EVENT_WARN = "a.budget.warn"
EVENT_EXCEEDED = "a.budget.exceeded"
EVENT_CONFIG_ERROR = "a.budget.config_error"


@dataclass
class BudgetGuardConfig:
    """护栏配置（stdlib dataclass，不引 pydantic）。"""

    max_tokens_per_run: int = DEFAULT_MAX_TOKENS_PER_RUN  # ≥ 1（非法回退默认）
    warn_ratio: float = DEFAULT_WARN_RATIO  # 软提醒阈值（0~1）
    hard_stop_ratio: float = DEFAULT_HARD_STOP_RATIO  # 硬暂停阈值（0~1）
    fail_closed: bool = DEFAULT_FAIL_CLOSED  # 配置不可用时是否硬停
    scope: str = DEFAULT_SCOPE  # per_run | per_agent_session
    enabled: bool = False  # 总开关，默认关闭 → 零回归


@dataclass
class BudgetCheckResult:
    """三态判定结果（脱敏聚合值）。"""

    status: str  # ok | warn | hard_stop
    ratio: float  # total_tokens / max_tokens_per_run（per_agent_session 为累加后比值）
    limit: int  # 生效上限（max_tokens_per_run）
    scope: str  # per_run | per_agent_session
    agent_session_id: str = ""  # 仅范围键（脱敏后的会话标识前缀），不落原始业务 id


class BudgetGuard:
    """基于 ``total_tokens`` 的自主硬停护栏。

    不调用用户询问路径；``check()`` 直接基于累计 token 做 ok / warn /
    hard_stop 三态判定。配置不可用时按 fail-closed 确定性语义硬停或自禁用。
    """

    def __init__(
        self,
        *,
        config: "BudgetGuardConfig | None" = None,
        config_path: "str | None" = None,
        database: "Any | None" = None,
        event_log: "Any | None" = None,
    ) -> None:
        self._explicit_config = config
        self._config_path = config_path
        self._database = database
        self._event_log = event_log
        # 进程内累加器（per_agent_session 跨轮/跨调用累加）。
        self._acc: dict[str, int] = {}
        # 最近一次 check 的 ratio（供调用方在硬停时落审计）。
        self._last_ratio: float = 0.0
        # 配置加载是否失败（触发 fail-closed 确定性语义）。
        self._load_failed: bool = False
        # 解析配置（含 fail-closed 确定性处理）。
        self._config, self._load_failed = self._resolve_config()
        # 仅 per_agent_session 且提供 database 时，载入既有累加（跨进程耐久）。
        if self._config.scope == "per_agent_session" and self._database is not None:
            self._load_accumulators()

    # ------------------------------------------------------------------ #
    # 配置解析（含 fail-closed 确定性语义）
    # ------------------------------------------------------------------ #
    def _resolve_config(self) -> "tuple[BudgetGuardConfig, bool]":
        """解析配置；返回 (config, load_failed)。

        load_failed=True 表示配置缺失 / JSON 损坏 / max_tokens_per_run 非法，
        此时按 §3.1 确定性语义决定行为（硬停或自禁用）。
        """
        if self._explicit_config is not None:
            cfg = self._explicit_config
            return cfg, (cfg.max_tokens_per_run < 1)
        if self._config_path is not None:
            return self._read_config_file(self._config_path)
        # 无配置源：使用默认（enabled=False → 惰性 no-op）。
        return BudgetGuardConfig(), False

    def _read_config_file(self, path: str) -> "tuple[BudgetGuardConfig, bool]":
        try:
            with open(path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except Exception:
            # 文件缺失 / JSON 损坏 → 加载失败，采用最严格回退（enabled=True,
            # fail_closed=True），由 fail-closed 语义决定硬停。
            return (
                BudgetGuardConfig(enabled=True, fail_closed=True),
                True,
            )
        # 解析字段（带默认值）；字段转换失败 → 加载失败（保守回退）。
        try:
            cfg = BudgetGuardConfig(
                max_tokens_per_run=int(
                    raw.get("max_tokens_per_run", DEFAULT_MAX_TOKENS_PER_RUN)
                ),
                warn_ratio=float(raw.get("warn_ratio", DEFAULT_WARN_RATIO)),
                hard_stop_ratio=float(
                    raw.get("hard_stop_ratio", DEFAULT_HARD_STOP_RATIO)
                ),
                fail_closed=bool(raw.get("fail_closed", DEFAULT_FAIL_CLOSED)),
                scope=str(raw.get("scope", DEFAULT_SCOPE)),
                enabled=bool(raw.get("enabled", False)),
            )
        except (TypeError, ValueError):
            return BudgetGuardConfig(enabled=True, fail_closed=True), True
        if cfg.max_tokens_per_run < 1:
            # max_tokens_per_run 非法 → 加载失败，但保留文件中已声明的
            # enabled / fail_closed / scope（供确定性语义判定）。
            return (
                BudgetGuardConfig(
                    max_tokens_per_run=DEFAULT_MAX_TOKENS_PER_RUN,
                    warn_ratio=cfg.warn_ratio,
                    hard_stop_ratio=cfg.hard_stop_ratio,
                    fail_closed=cfg.fail_closed,
                    scope=cfg.scope,
                    enabled=cfg.enabled,
                ),
                True,
            )
        return cfg, False

    # ------------------------------------------------------------------ #
    # 三态判定（纯函数 + 可选累加）
    # ------------------------------------------------------------------ #
    def check(
        self, total_tokens: int, *, agent_session_id: str = ""
    ) -> BudgetCheckResult:
        """基于 total_tokens 返回 ok / warn / hard_stop；超硬限抛脱敏异常。

        前置：``enabled=False`` → 直接返回 ok（惰性 no-op，不累加、不写事件）。
        超 ``hard_stop_ratio`` → 抛 ``RealRDExecutorError("budget_exceeded")``
        （fail-closed，脱敏；不携带路径 / Key / 参数）。
        """
        cfg = self._config
        # 惰性 no-op：开关关闭时全程不介入。
        if not cfg.enabled:
            return BudgetCheckResult(
                status="ok",
                ratio=0.0,
                limit=cfg.max_tokens_per_run,
                scope=cfg.scope,
                agent_session_id="",
            )
        # fail-closed 确定性语义：配置加载失败。
        if self._load_failed:
            if cfg.fail_closed:
                # 硬停模式：状态未知 → 拒绝执行，防止无上限消耗。
                self._last_ratio = 1.0
                self._raise_budget_exceeded()
            # 自禁用（fail-open）：跳过检查，仅落 config_error 审计。
            self.record_budget_event(
                self._event_log,
                EVENT_CONFIG_ERROR,
                {
                    "scope": cfg.scope,
                    "status": "config_error",
                    "reason": "config_load_failed",
                },
                "",
            )
            return BudgetCheckResult(
                status="ok",
                ratio=0.0,
                limit=cfg.max_tokens_per_run,
                scope=cfg.scope,
                agent_session_id="",
            )

        limit = cfg.max_tokens_per_run
        if cfg.scope == "per_agent_session":
            key = f"{cfg.scope}:{agent_session_id}"
            self._acc[key] = self._acc.get(key, 0) + int(total_tokens)
            effective = self._acc[key]
            self._persist_accumulator(key, effective)
        else:
            effective = int(total_tokens)

        ratio = (effective / limit) if limit > 0 else 0.0
        self._last_ratio = ratio

        if ratio >= cfg.hard_stop_ratio:
            self._raise_budget_exceeded()
        if ratio >= cfg.warn_ratio:
            return BudgetCheckResult(
                status="warn",
                ratio=ratio,
                limit=limit,
                scope=cfg.scope,
                agent_session_id=agent_session_id,
            )
        return BudgetCheckResult(
            status="ok",
            ratio=ratio,
            limit=limit,
            scope=cfg.scope,
            agent_session_id=agent_session_id,
        )

    @staticmethod
    def _raise_budget_exceeded() -> NoReturn:
        # 延迟导入以规避与 real_rd_executor 的循环依赖（real_rd_executor 在
        # 其 __init__ 中 import 本模块；运行期调用 check() 时两者均已加载）。
        from .real_rd_executor import RealRDExecutorError

        raise RealRDExecutorError("budget_exceeded")

    # ------------------------------------------------------------------ #
    # per_agent_session 累加持久化（自管理表，不并入 database.initialize()）
    # ------------------------------------------------------------------ #
    def _load_accumulators(self) -> None:
        try:
            rows = self._query_all(
                f"select acc_key, accumulated_tokens from {ACCUMULATOR_TABLE}"
            )
            for acc_key, accumulated in rows:
                self._acc[acc_key] = int(accumulated)
        except Exception:  # noqa: BLE001 - 累加载入失败不影响主流程
            pass

    def _persist_accumulator(self, key: str, value: int) -> None:
        if self._database is None:
            return
        try:
            stmt = (
                f"INSERT OR REPLACE INTO {ACCUMULATOR_TABLE} "
                f"(acc_key, scope, accumulated_tokens, updated_at) VALUES (?, ?, ?, ?)"
            )
            params = (key, self._config.scope, int(value), self._now_iso())
            if isinstance(self._database, str):
                conn = sqlite3.connect(self._database)
                try:
                    self._ensure_table(conn)
                    conn.execute(stmt, params)
                    conn.commit()
                finally:
                    conn.close()
            else:
                with self._database.connect() as conn:
                    self._ensure_table(conn)
                    conn.execute(stmt, params)
        except Exception:  # noqa: BLE001 - 累加持久化失败不影响主流程（进程内仍生效）
            pass

    def _query_all(self, sql: str) -> "list[tuple[Any, ...]]":
        if isinstance(self._database, str):
            conn = sqlite3.connect(self._database)
            try:
                self._ensure_table(conn)
                return list(conn.execute(sql).fetchall())
            finally:
                conn.close()
        with self._database.connect() as conn:
            self._ensure_table(conn)
            return list(conn.execute(sql).fetchall())

    @staticmethod
    def _ensure_table(conn: Any) -> None:
        conn.execute(
            f"CREATE TABLE IF NOT EXISTS {ACCUMULATOR_TABLE} ("
            "acc_key TEXT PRIMARY KEY, "
            "scope TEXT, "
            "accumulated_tokens INTEGER, "
            "updated_at TEXT)"
        )

    @staticmethod
    def _now_iso() -> str:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()

    # ------------------------------------------------------------------ #
    # 脱敏事件写（best-effort，绝不阻断主流程）
    # ------------------------------------------------------------------ #
    def record_budget_event(
        self,
        event_log: Any,
        event_type: str,
        payload: dict[str, Any],
        correlation_id: str,
    ) -> None:
        """落 ``a.budget.*`` 事件（脱敏：仅 scope / status / ratio / limit / 范围键）。

        与既有审计事件并列独立追加写、不混。``event_log`` 为注入的
        ``EvolutionEventLog``（Any，避免 BudgetGuard 依赖具体类型）；``payload``
        仅含聚合值，无路径 / Key / 参数 / 原始 Secret。
        """
        if event_log is None:
            return
        try:
            event_log.record(
                correlation_id=correlation_id or "",
                event_type=event_type,
                payload=payload,
                tenant_id=None,  # 由 EvolutionEventLog 自行解析 selfuse
                idempotency_key=f"{correlation_id}:{event_type}:{uuid.uuid4().hex[:8]}",
            )
        except Exception:  # noqa: BLE001 - 预算事件为尽力而为，绝不影响主流程
            pass
