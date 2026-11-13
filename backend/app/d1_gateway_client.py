"""R3 gateway client contract (scope A).

Thin, read-only wrapper around the pre-existing ``ModelGatewayAdapter``.

This module deliberately:
  - NEVER reads credentials. It performs no ``CURIS_MODEL_GATEWAY_API_KEY``
    access and never constructs or mutates an adapter; it only *consumes* an
    already-injected instance. Credential injection is the security boundary
    seat's decision and is out of scope here.
  - exposes ``is_configured()`` which answers "is the gateway usable?" without
    ever returning or logging the key / base URL / token;
  - delegates the real model call to ``ModelGatewayAdapter.execute`` and returns
    its (already desensitized) result.

Standard library only; no new third-party dependencies.
"""

from __future__ import annotations

from typing import Any

from .d1_execute import D1ExecutionErrorCategory
from .model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError


class R3GatewayClient:
    """Consumes an injected ``ModelGatewayAdapter`` instance; no credential access.

    The adapter is supplied fully configured by the caller (the application
    startup path / security boundary seat). This client only inspects the
    adapter's declared runtime configuration and forwards prompt executions.
    """

    def __init__(self, adapter: ModelGatewayAdapter) -> None:
        self._adapter = adapter

    def is_configured(self) -> bool:
        """True when the underlying gateway reports a declared runtime config.

        Delegates to ``ModelGatewayAdapter.runtime_config_is_declared()``.
        Returns/records nothing about keys, URLs, or tokens.
        """
        return self._adapter.runtime_config_is_declared()

    def call(self, prompt: str) -> dict[str, Any]:
        """Delegate a single prompt to the adapter; returns its desensitized result.

        The adapter is responsible for transport, usage accounting, and
        desensitization; this method only forwards the prompt and the result.
        """
        return self._adapter.execute(prompt)

    def classify_error(self, error: BaseException) -> D1ExecutionErrorCategory:
        """Map a gateway-originated error to a desensitized execution error category.

        Rationale for the mapping:
          - ``ModelGatewayExecutionError`` with status ``configuration_rejected``
            means the R3 gateway runtime config is incomplete (missing base URL /
            key / model) -> ``CREDENTIAL_MISSING``.
          - Any other ``ModelGatewayExecutionError`` (network, gateway, rate-limit,
            limit/cost rejection) -> ``GATEWAY_TIMEOUT`` (gateway unreachable or
            rejected). The raw status is never surfaced to the caller.
          - Transport-level exceptions (urllib errors, connection/timeout) are
            also collapsed to ``GATEWAY_TIMEOUT``; no path/stack/key is exposed.
        """
        if isinstance(error, ModelGatewayExecutionError):
            if error.status == "configuration_rejected":
                return D1ExecutionErrorCategory.CREDENTIAL_MISSING
            return D1ExecutionErrorCategory.GATEWAY_TIMEOUT
        # 网络/传输层异常一律归为网关异常，绝不向上暴露原始异常/路径/堆栈/Key。
        return D1ExecutionErrorCategory.GATEWAY_TIMEOUT
