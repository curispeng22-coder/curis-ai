"""D1 execute() orchestration + error classification + degraded status (scope A).

Wraps the pre-existing, already-real ``D1SingleModelToolchain`` behind a
controlled gate:

  - ``status()`` reports ``READY`` / ``DEGRADED`` / ``FROZEN``;
  - ``execute()`` only runs the supported task type, reuses the toolchain's
    single-owner lock (``_claim_once``), and never introduces new concurrency;
  - every failure path resolves to a desensitized ``D1ExecutionError`` carrying
    one of four categories and a fixed, path/stack/key-free detail constant.

No new third-party dependencies; the standard library plus existing project
modules only.

Desensitization red line: this module never logs, returns, or raises raw
exception text, file paths, stack traces, keys, or request parameters. All
outbound error detail is one of the fixed constants below.
"""

from __future__ import annotations

import time
from enum import Enum
from typing import Any

from .d1_config import D1_UNAVAILABLE_MESSAGE, D1ToolchainConfig
from .d1_single_model_toolchain import D1SingleModelToolchain, D1ToolchainError
from .model_gateway import ModelGatewayExecutionError
from .tenant_context import TenantContext


# 固定脱敏文案：受控 422 用例仅携带「任务类型不支持」的常量，绝不带参/路径/Key。
D1_TASK_INVALID_DETAIL = "D1 task type is not supported"


class D1ExecutionStatus(Enum):
    """Readiness of the controlled D1 execution gate."""

    READY = "ready"
    DEGRADED = "degraded"
    FROZEN = "frozen"


class D1ExecutionErrorCategory(Enum):
    """Four desensitized failure families for the D1 execution gate."""

    CREDENTIAL_MISSING = "credential_missing"
    GATEWAY_TIMEOUT = "gateway_timeout"
    TASK_INVALID = "task_invalid"
    FROZEN = "frozen"


class D1ExecutionError(Exception):
    """Desensitized execution error: category + suggested HTTP status + fixed detail.

    Carries no raw exception text, path, stack, key, or parameter. The
    ``status_code`` is the HTTP status the FastAPI route should emit, and
    ``detail`` is always one of the module-level fixed constants.
    """

    def __init__(
        self,
        category: D1ExecutionErrorCategory,
        status_code: int,
        detail: str,
    ) -> None:
        super().__init__(detail)
        self.category = category
        self.status_code = status_code
        self.detail = detail


# D1ToolchainError.failure_code values that map to the four categories.
#  - model_configuration_rejected: R3 runtime config incomplete -> credential missing.
#  - model_call_failed / model_input_limit_rejected / model_result_rejected: gateway
#    unreachable or rejected -> gateway timeout family.
_MODEL_CREDENTIAL_CODES = frozenset({"model_configuration_rejected"})
_MODEL_GATEWAY_CODES = frozenset(
    {"model_call_failed", "model_input_limit_rejected", "model_result_rejected"}
)


class D1ExecutionOrchestrator:
    """Controlled gate in front of the real D1 toolchain.

    The orchestrator is constructed once at application startup with the resolved
    ``D1ToolchainConfig``, a ``R3GatewayClient`` wrapping the injected model
    adapter, the (possibly ``None``) ``D1SingleModelToolchain`` instance, and
    optional sinks for structured logging (``D1ExecutionLogRepository``) and
    observability (``EvolutionEventLog``). Both sinks default to ``None`` so the
    orchestrator remains usable in isolation (unit tests, no database).
    """

    def __init__(
        self,
        config: D1ToolchainConfig,
        gateway_client: Any,
        toolchain: D1SingleModelToolchain | None,
        execution_log: Any = None,
        event_log: Any = None,
    ) -> None:
        self._config = config
        self._gateway = gateway_client
        self._toolchain = toolchain
        self._execution_log = execution_log
        self._event_log = event_log
        # 最近一次 execute() 的分类结果；用于 status() 的 DEGRADED 判定。
        self._last_category: D1ExecutionErrorCategory | None = None

    def status(self) -> D1ExecutionStatus:
        """Report execution readiness without exposing any sensitive detail."""
        if self._config.frozen or self._toolchain is None:
            return D1ExecutionStatus.FROZEN
        if not self._gateway.is_configured():
            return D1ExecutionStatus.DEGRADED
        if self._last_category == D1ExecutionErrorCategory.GATEWAY_TIMEOUT:
            return D1ExecutionStatus.DEGRADED
        return D1ExecutionStatus.READY

    def execute(self, task_type: str = "d1-tenant-reservation") -> dict[str, Any]:
        """Run the controlled D1 execution for ``task_type``.

        Returns a desensitized summary (same shape as
        ``D1SingleModelToolchain.execute()``) on success. Any failure is collapsed
        into a desensitized ``D1ExecutionError``; no raw exception / path / stack /
        key / parameter ever escapes.

        Every attempt (success or failure) is recorded for audit/observability via
        the ``execution_log`` repository and an ``EvolutionEventLog`` event — see
        ``_record_outcome``. Recording never surfaces sensitive detail.
        """
        started = time.monotonic()
        outcome_status: str | None = None
        outcome_category: str | None = None
        token_count = 0
        try:
            # 仅支持配置声明的任务类型；其余一律受控 422，不传播任何参数。
            if task_type != self._config.execute_task_type:
                raise D1ExecutionError(
                    D1ExecutionErrorCategory.TASK_INVALID,
                    422,
                    D1_TASK_INVALID_DETAIL,
                )
            status = self.status()
            if status == D1ExecutionStatus.FROZEN:
                raise D1ExecutionError(
                    D1ExecutionErrorCategory.FROZEN, 503, D1_UNAVAILABLE_MESSAGE
                )
            if status == D1ExecutionStatus.DEGRADED:
                # 非冻结但网关未就绪（凭证缺失）-> 受控降级。
                raise D1ExecutionError(
                    D1ExecutionErrorCategory.CREDENTIAL_MISSING, 503, D1_UNAVAILABLE_MESSAGE
                )
            if self._toolchain is None:
                raise D1ExecutionError(
                    D1ExecutionErrorCategory.FROZEN, 503, D1_UNAVAILABLE_MESSAGE
                )
            try:
                # 复用既有 D1SingleModelToolchain.execute()：其内部 _claim_once
                # 已是单主占锁，编排层不另造并发逻辑。
                summary = self._toolchain.execute()
            except D1ToolchainError as error:
                category = self._classify(error)
                if category is not None:
                    self._last_category = category
                    raise D1ExecutionError(
                        category, self._status_for(category), D1_UNAVAILABLE_MESSAGE
                    ) from error
                # 非模型类 D1ToolchainError（scope/工具/审计等）不归四类枚举，
                # 交由路由按既有 409 脱敏文案处理。
                raise
            except ModelGatewayExecutionError as error:
                category = self._gateway.classify_error(error)
                self._last_category = category
                raise D1ExecutionError(
                    category, self._status_for(category), D1_UNAVAILABLE_MESSAGE
                ) from error
            # 成功路径：清空最近异常分类，返回与既有工具链同构的脱敏 summary。
            self._last_category = None
            token_count = int(summary.get("total_tokens", 0) or 0)
            outcome_status = "succeeded"
            return summary
        except D1ExecutionError as error:
            # 受控错误分类已脱敏：outcome 仅记枚举 value，绝不记原始异常。
            outcome_status = error.category.value
            outcome_category = error.category.value
            raise
        except D1ToolchainError:
            # 非模型类 D1ToolchainError（scope/工具/审计）原样上抛；
            # 仍记一条 desensitized 的 toolchain_rejected 记录供可观测。
            outcome_status = "toolchain_rejected"
            outcome_category = "toolchain_rejected"
            raise
        finally:
            # 无论成功/失败均落库 + 记可观测事件（若已注入 sink）。
            if outcome_status is not None:
                duration_ms = int((time.monotonic() - started) * 1000)
                self._record_outcome(outcome_status, outcome_category, duration_ms, token_count)

    def _record_outcome(
        self,
        status: str,
        error_category: str | None,
        duration_ms: int,
        token_count: int,
    ) -> None:
        """Desensitized persistence + observability sink.

        Writes a single ``d1_execution_log`` row (task_type is always the
        configured constant — never a caller-supplied parameter) and emits one
        ``d1.execution.<status>`` observability event. Both are no-ops when the
        respective sink is ``None`` (e.g. isolated unit tests).
        """
        tenant_id = TenantContext.current_tenant_id()
        recorded_task_type = self._config.execute_task_type
        if self._execution_log is not None:
            self._execution_log.insert(
                tenant_id=tenant_id,
                task_type=recorded_task_type,
                status=status,
                error_category=error_category,
                duration_ms=duration_ms,
                token_count=token_count,
            )
        if self._event_log is not None:
            self._event_log.record(
                correlation_id=f"d1-execution:{recorded_task_type}",
                event_type=f"d1.execution.{status}",
                tenant_id=tenant_id,
                idempotency_key=None,
                payload={
                    "task_type": recorded_task_type,
                    "status": status,
                    "error_category": error_category,
                    "duration_ms": duration_ms,
                    "token_count": token_count,
                },
            )

    def _classify(self, error: D1ToolchainError) -> D1ExecutionErrorCategory | None:
        """Map a ``D1ToolchainError`` to an execution category, or ``None``.

        Returns ``None`` for failure codes that are not model-gateway related
        (scope / tool / audit mismatches); those propagate as ``D1ToolchainError``
        and are handled by the route's existing 409 path.
        """
        failure_code = getattr(error, "failure_code", "")
        if failure_code in _MODEL_CREDENTIAL_CODES:
            return D1ExecutionErrorCategory.CREDENTIAL_MISSING
        if failure_code in _MODEL_GATEWAY_CODES:
            return D1ExecutionErrorCategory.GATEWAY_TIMEOUT
        return None

    @staticmethod
    def _status_for(category: D1ExecutionErrorCategory) -> int:
        """HTTP status a route should emit for a given error category."""
        return {
            D1ExecutionErrorCategory.FROZEN: 503,
            D1ExecutionErrorCategory.CREDENTIAL_MISSING: 503,
            D1ExecutionErrorCategory.GATEWAY_TIMEOUT: 503,
            D1ExecutionErrorCategory.TASK_INVALID: 422,
        }[category]
