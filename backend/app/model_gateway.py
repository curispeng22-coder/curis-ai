from __future__ import annotations

import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from urllib.parse import quote, unquote, urlsplit
from typing import Any, Callable


HttpPost = Callable[[str, dict[str, Any], dict[str, str], int], dict[str, Any]]

# Observed cloud reasoning calls reach81.7s; keep a finite network-operation bound.
MODEL_HTTP_TIMEOUT_SECONDS = 90

R3_PROFILE = "r3_openai"
R3_PROVIDER_ID = "openai"
R3_GATEWAY_ID = "newapi"
R3_BASE_URL = "https://api.openai.com"
R3_MODEL_ID = "gpt-5.4-mini-2026-03-17"
R3_CAPABILITY_ID = "official.openai.gpt-5.4-mini-2026-03-17"
R3_WORKFLOW_TEMPLATE_ID = "official.workflow.software_rnd_sop"
R3_MAX_INPUT_TOKENS = 8_192
R3_WORKFLOW_CONTEXT_MAX_BYTES = 7_168
R3_MAX_OUTPUT_TOKENS = 2_048
R3_MAX_TOTAL_TOKENS = 10_240
R3_MAX_COST_USD = 0.10
R3_INPUT_USD_PER_TOKEN = 0.75 / 1_000_000
R3_OUTPUT_USD_PER_TOKEN = 4.50 / 1_000_000
R3_PRICE_VERSION = "2026-07-17"
R3_COST_SOURCE = "openai_gpt_5_4_mini_2026_07_17"


class ModelGatewayExecutionError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status: str = "failed",
        http_status: int = 0,
        latency_ms: int = 0,
        outbound_attempted: bool = False,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.http_status = http_status
        self.latency_ms = latency_ms
        self.outbound_attempted = outbound_attempted


SECRET_PATTERNS = (
    re.compile(r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/\-=:-]+", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/\-=:-]+", re.IGNORECASE),
    re.compile(r"sk-(?:or-v1-)?[A-Za-z0-9_-]{10,}", re.IGNORECASE),
    re.compile(r"(api[_-]?key|token|password|secret)\s*[:=]\s*[^,\s;}]+", re.IGNORECASE),
)
ROUTE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/+~-]*$")


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def redact_model_gateway_text(value: Any, secrets: list[str] | None = None) -> str:
    text = str(value)
    for secret in secrets or []:
        if secret:
            text = text.replace(str(secret), "[REDACTED]")
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def resolve_gateway_api_key(credential_ref: str | None) -> str:
    """把网关 ``credential_ref`` 解析成真实 api_key（Step 5）。

    只支持 ``env:VAR`` 一种方案：密钥永远来自进程环境变量，绝不落库、绝不出现在
    任何 catalog 投影里。``kms:`` / ``vault:`` 尚未接入，此处**返回空串**而不是抛错——
    空 api_key 会在 ``validate_runtime_config`` 处以「配置不完整」拒绝执行，从而走
    既有降级/回退路径，而不是在装配期炸掉整个应用。
    """
    reference = (credential_ref or "").strip()
    if not reference:
        return ""
    scheme, _, name = reference.partition(":")
    if scheme.strip().lower() != "env" or not name.strip():
        return ""
    return os.getenv(name.strip(), "")


class ModelGatewayAdapter:
    """Execute an explicit model route; registered gateways use OpenAI chat.

    Only the same gateway may retain an existing single-gateway configuration.
    Private native protocols are supplied explicitly by their capability metadata.
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        gateway_id: str | None = None,
        model_name: str | None = None,
        timeout: int | None = None,
        http_post: HttpPost | None = None,
        gateway_resolver: Callable[[str], dict[str, Any] | None] | None = None,
        protocol: str = "openai_chat",
        chat_path: str = "/v1/chat/completions",
    ):
        self.base_url = (base_url or os.getenv("CURIS_MODEL_GATEWAY_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("CURIS_MODEL_GATEWAY_API_KEY", "")
        self.gateway_id = gateway_id or os.getenv("CURIS_MODEL_GATEWAY_ID", "newapi")
        self.model_name = model_name or os.getenv("CURIS_MODEL_GATEWAY_MODEL", "")
        self.profile = os.getenv("CURIS_MODEL_GATEWAY_PROFILE", "").strip()
        self.timeout = (60 if self.profile == R3_PROFILE else MODEL_HTTP_TIMEOUT_SECONDS) if timeout is None else timeout
        if type(self.timeout) is not int or not 1 <= self.timeout <= MODEL_HTTP_TIMEOUT_SECONDS:
            raise ValueError("model HTTP timeout must be an integer between1 and90 seconds")
        self.http_post = http_post or self._urllib_post
        self.gateway_resolver = gateway_resolver
        self.protocol = protocol
        self.chat_path = chat_path
        self.price_version = os.getenv("CURIS_MODEL_GATEWAY_PRICE_VERSION", "")
        self.estimated_rate = os.getenv("CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS", "0")
        # 目标网关已注册但被停用时记录原因，在 execute() 里显式拒绝（而不是静默
        # 打到别的供应商上）。装配期不抛错，保证既有回退路径仍能接管。
        self.disabled_reason = ""

    def _resolve_gateway_row(self, gateway_id: str) -> dict[str, Any] | None:
        if self.gateway_resolver is None:
            return None
        try:
            row = self.gateway_resolver(gateway_id)
        except Exception:
            raise ModelGatewayExecutionError(
                "Selected model gateway could not be resolved",
                status="configuration_rejected", http_status=422,
            ) from None
        if row is not None and (not isinstance(row, dict) or row.get("gateway_id") != gateway_id):
            raise ModelGatewayExecutionError(
                "Selected model gateway identity does not match",
                status="configuration_rejected", http_status=422,
            )
        return row

    def with_model_metadata(self, *, gateway_id: str, model_name: str) -> "ModelGatewayAdapter":
        if not gateway_id or not model_name:
            raise ModelGatewayExecutionError("Selected model route is incomplete",
                                             status="configuration_rejected", http_status=422)
        row = self._resolve_gateway_row(gateway_id)
        base_url, api_key = self.base_url, self.api_key
        protocol, chat_path = self.protocol, self.chat_path
        disabled_reason = ""
        if row is None:
            if gateway_id != self.gateway_id:
                raise ModelGatewayExecutionError("Selected model gateway is unavailable",
                                                 status="configuration_rejected", http_status=422)
        else:
            from .catalog_constants import GATEWAY_TYPE
            base_url = str(row.get("base_url") or "").rstrip("/")
            protocol, chat_path = "openai_chat", "/v1/chat/completions"
            api_key = ""
            if row.get("status") != "active" or row.get("type") not in GATEWAY_TYPE:
                disabled_reason = "Selected model gateway is inactive or unsupported"
            elif base_url:
                api_key = resolve_gateway_api_key(row.get("credential_ref"))
        adapter = ModelGatewayAdapter(
            gateway_id=gateway_id, model_name=model_name, timeout=self.timeout,
            http_post=self.http_post, gateway_resolver=self.gateway_resolver,
            protocol=protocol, chat_path=chat_path,
        )
        # Empty resolved values must not inherit constructor environment defaults.
        adapter.base_url, adapter.api_key = base_url, api_key
        adapter.profile = self.profile
        same_route = (gateway_id, model_name, base_url, protocol, chat_path) == (
            self.gateway_id, self.model_name, self.base_url, self.protocol, self.chat_path)
        adapter.price_version = self.price_version if same_route else ""
        adapter.estimated_rate = self.estimated_rate if same_route else "0"
        adapter.disabled_reason = disabled_reason
        return adapter

    def execute(self, prompt: str, *, max_output_tokens: int | None = None) -> dict[str, Any]:
        if max_output_tokens is not None and (
            type(max_output_tokens) is not int or not 1 <= max_output_tokens <= R3_MAX_OUTPUT_TOKENS
        ):
            raise ValueError("output ceiling must be a positive integer within the gateway bound")
        if self.disabled_reason:
            raise ModelGatewayExecutionError(
                self.disabled_reason,
                status="configuration_rejected",
                http_status=403,
            )
        self.validate_runtime_config()
        if self.profile == R3_PROFILE and len(prompt.encode("utf-8")) > R3_MAX_INPUT_TOKENS:
            raise ModelGatewayExecutionError(
                "Model gateway input exceeds the approved limit",
                status="limit_rejected",
                http_status=422,
            )
        endpoint, payload, headers = self._request(prompt)
        if max_output_tokens is not None:
            if self.protocol == "gemini_generate_content":
                payload["generationConfig"] = {"maxOutputTokens": max_output_tokens}
            elif self.profile == R3_PROFILE and self.protocol == "openai_chat":
                payload["max_completion_tokens"] = max_output_tokens
            else:
                payload["max_tokens"] = max_output_tokens
        started = time.monotonic()
        try:
            response = self.http_post(
                endpoint,
                payload,
                headers,
                self.timeout,
            )
        except urllib.error.HTTPError as error:
            latency_ms = round((time.monotonic() - started) * 1000)
            if error.code == 429:
                raise ModelGatewayExecutionError(
                    "Model gateway rate limited",
                    status="rate_limited",
                    http_status=429,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                ) from error
            raise ModelGatewayExecutionError(
                "Model gateway request failed",
                status="gateway_error",
                http_status=error.code,
                latency_ms=latency_ms,
                outbound_attempted=True,
            ) from error
        except Exception as error:
            message = redact_model_gateway_text(error, [self.api_key, prompt])
            if message != str(error):
                message = "[REDACTED]"
            raise ModelGatewayExecutionError(
                f"Model gateway request failed: {message}",
                status="network_error",
                latency_ms=round((time.monotonic() - started) * 1000),
                outbound_attempted=True,
            ) from error
        latency_ms = round((time.monotonic() - started) * 1000)
        if response.get("error"):
            raise ModelGatewayExecutionError(
                "Model gateway returned an error",
                status="gateway_error",
                http_status=502,
                latency_ms=latency_ms,
                outbound_attempted=True,
            )
        routed_via = str(response.pop("__curis_routed_via", "") or "")
        provider_id = self.gateway_id
        actual_model = self.model_name
        if self.gateway_id == "freellmapi.experimental":
            decoded_route = unquote(routed_via)
            route_is_sensitive = any(
                secret and secret in decoded_route
                for secret in (self.api_key, prompt)
            ) or redact_model_gateway_text(decoded_route) != decoded_route
            if "/" not in decoded_route:
                route_parts = ()
            else:
                route_parts = decoded_route.split("/", 1)
            if (
                len(route_parts) != 2
                or not route_parts[0]
                or not route_parts[1]
                or len(route_parts[0]) > 64
                or len(route_parts[1]) > 256
                or not ROUTE_IDENTIFIER_PATTERN.fullmatch(route_parts[0])
                or not ROUTE_IDENTIFIER_PATTERN.fullmatch(route_parts[1])
                or route_is_sensitive
            ):
                raise ModelGatewayExecutionError(
                    "Model gateway route metadata was not usable",
                    status="response_invalid",
                    http_status=502,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                )
            provider_id, actual_model = route_parts
        try:
            output, usage = self._response(response)
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ModelGatewayExecutionError(
                "Model gateway response was not usable",
                status="response_invalid",
                http_status=502,
                latency_ms=latency_ms,
                outbound_attempted=True,
            ) from error
        input_value = usage.get("prompt_tokens", usage.get("input_tokens"))
        output_value = usage.get("completion_tokens", usage.get("output_tokens"))
        total_value = usage.get("total_tokens")
        try:
            prompt_tokens = None if input_value is None else int(input_value)
            completion_tokens = None if output_value is None else int(output_value)
            total_tokens = None if total_value is None else int(total_value)
        except (TypeError, ValueError) as error:
            raise ModelGatewayExecutionError(
                "Model gateway usage metadata was not usable",
                status="metering_invalid",
                http_status=502,
                latency_ms=latency_ms,
                outbound_attempted=True,
            ) from error
        if total_tokens is None and prompt_tokens is not None and completion_tokens is not None:
            total_tokens = prompt_tokens + completion_tokens
        if any(value is not None and value < 0 for value in (prompt_tokens, completion_tokens, total_tokens)):
            raise ModelGatewayExecutionError(
                "Model gateway usage metadata was not usable",
                status="metering_invalid",
                http_status=502,
                latency_ms=latency_ms,
                outbound_attempted=True,
            )
        metering_status = (
            "confirmed"
            if total_tokens is not None
            else "unknown"
        )
        if self.profile == R3_PROFILE:
            if not prompt_tokens or not total_tokens:
                raise ModelGatewayExecutionError(
                    "Model gateway usage metadata is required",
                    status="audit_rejected",
                    http_status=502,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                )
            if (
                prompt_tokens > R3_MAX_INPUT_TOKENS
                or (completion_tokens or 0) > R3_MAX_OUTPUT_TOKENS
                or total_tokens > R3_MAX_TOTAL_TOKENS
            ):
                raise ModelGatewayExecutionError(
                    "Model gateway usage exceeds the approved limit",
                    status="limit_rejected",
                    http_status=422,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                )
            estimated_cost = round(
                prompt_tokens * R3_INPUT_USD_PER_TOKEN
                + (completion_tokens or 0) * R3_OUTPUT_USD_PER_TOKEN,
                8,
            )
            if estimated_cost <= 0 or estimated_cost > R3_MAX_COST_USD:
                raise ModelGatewayExecutionError(
                    "Model gateway cost exceeds the approved limit",
                    status="cost_rejected",
                    http_status=422,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                )
        else:
            try:
                estimated_cost = self._estimated_cost(usage, total_tokens or 0)
            except (TypeError, ValueError) as error:
                raise ModelGatewayExecutionError(
                    "Model gateway cost metadata was not usable",
                    status="metering_invalid",
                    http_status=502,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                ) from error
            if not math.isfinite(estimated_cost) or estimated_cost < 0:
                raise ModelGatewayExecutionError(
                    "Model gateway cost metadata was not usable",
                    status="metering_invalid",
                    http_status=502,
                    latency_ms=latency_ms,
                    outbound_attempted=True,
                )
        if self.profile == R3_PROFILE:
            ledger_cost_source = "estimated"
        elif any(key in usage and usage[key] is not None for key in ("cost", "total_cost")):
            ledger_cost_source = "provider_reported"
        elif estimated_cost > 0:
            ledger_cost_source = "estimated"
        else:
            ledger_cost_source = "unknown"
        prompt_details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
        completion_details = usage.get("completion_tokens_details") or usage.get("output_tokens_details") or {}
        return {
            "output": output,
            # Legacy workflow arithmetic; only estimated_cost + ledger_cost_source carry monetary certainty.
            "cost": estimated_cost,
            "model_gateway_id": self.gateway_id,
            "model_name": actual_model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "token": total_tokens,
            "metering_status": metering_status,
            "cache_read_tokens": prompt_details.get("cached_tokens"),
            "cache_write_tokens": prompt_details.get("cache_write_tokens"),
            "reasoning_tokens": completion_details.get("reasoning_tokens"),
            "estimated_cost": estimated_cost if ledger_cost_source != "unknown" else None,
            "ledger_cost_source": ledger_cost_source,
            "status": "success",
            "provider_id": R3_PROVIDER_ID if self.profile == R3_PROFILE else provider_id,
            "unit_price_input": R3_INPUT_USD_PER_TOKEN if self.profile == R3_PROFILE else None,
            "unit_price_output": R3_OUTPUT_USD_PER_TOKEN if self.profile == R3_PROFILE else None,
            "price_version": (
                R3_PRICE_VERSION
                if self.profile == R3_PROFILE
                else self.price_version
            ),
            "currency": "USD",
            "cost_source": R3_COST_SOURCE if self.profile == R3_PROFILE else ledger_cost_source,
            "http_status": 200,
            "latency_ms": latency_ms,
            "outbound_attempted": True,
        }

    def _request(self, prompt: str) -> tuple[str, dict[str, Any], dict[str, str]]:
        if self.protocol == "anthropic_messages":
            return (
                f"{self.base_url}{self.chat_path or '/v1/messages'}",
                {
                    "model": self.model_name,
                    "max_tokens": R3_MAX_OUTPUT_TOKENS,
                    "messages": [{"role": "user", "content": prompt}],
                },
                {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
            )
        if self.protocol == "gemini_generate_content":
            model = quote(self.model_name.removeprefix("models/"), safe="")
            return (
                f"{self.base_url}/v1beta/models/{model}:generateContent",
                {"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
                {"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
            )
        if self.protocol != "openai_chat":
            raise ModelGatewayExecutionError(
                "Model provider protocol is not supported",
                status="configuration_rejected",
                http_status=422,
            )
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }
        if self.profile == R3_PROFILE:
            payload["max_completion_tokens"] = R3_MAX_OUTPUT_TOKENS
        return (
            f"{self.base_url}{self.chat_path or '/v1/chat/completions'}",
            payload,
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )

    def _response(self, response: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if self.protocol == "anthropic_messages":
            text = "".join(
                str(item.get("text") or "")
                for item in response["content"]
                if item.get("type") == "text"
            )
            if not text:
                raise ValueError("missing Anthropic text response")
            usage = response.get("usage") or {}
            return text, {
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
            }
        if self.protocol == "gemini_generate_content":
            text = "".join(
                str(part.get("text") or "")
                for part in response["candidates"][0]["content"]["parts"]
            )
            if not text:
                raise ValueError("missing Gemini text response")
            usage = response.get("usageMetadata") or {}
            return text, {
                "prompt_tokens": usage.get("promptTokenCount"),
                "completion_tokens": usage.get("candidatesTokenCount"),
                "total_tokens": usage.get("totalTokenCount"),
            }
        return response["choices"][0]["message"]["content"], response.get("usage") or {}

    def runtime_config_is_declared(self) -> bool:
        return bool(self.base_url or self.api_key or self.model_name)

    def validate_runtime_config(self) -> None:
        try:
            target = urlsplit(self.base_url)
            valid_endpoint = (target.scheme in {"http", "https"} and bool(target.hostname)
                              and not target.username and not target.password
                              and not target.query and not target.fragment)
            target.port
        except ValueError:
            valid_endpoint = False
        if not valid_endpoint:
            raise ModelGatewayExecutionError("Model gateway endpoint is invalid",
                                             status="configuration_rejected", http_status=422)
        if not self.base_url or not self.api_key or not self.model_name:
            if self.profile == R3_PROFILE:
                raise ModelGatewayExecutionError(
                    "R3 model gateway configuration is incomplete",
                    status="configuration_rejected",
                    http_status=401,
                )
            raise RuntimeError(
                "Model Gateway Adapter requires CURIS_MODEL_GATEWAY_BASE_URL, "
                "CURIS_MODEL_GATEWAY_API_KEY, and CURIS_MODEL_GATEWAY_MODEL"
            )
        if self.profile and self.profile != R3_PROFILE:
            raise RuntimeError("Unsupported model gateway profile")
        if self.profile == R3_PROFILE and (
            self.base_url != R3_BASE_URL
            or self.gateway_id != R3_GATEWAY_ID
            or self.model_name != R3_MODEL_ID
            or self.timeout != 60
            or self.protocol != "openai_chat"
            or self.chat_path != "/v1/chat/completions"
        ):
            raise RuntimeError("R3 model gateway configuration does not match the approved contract")

    def _estimated_cost(self, usage: dict[str, Any], token: int) -> float:
        for key in ("estimated_cost", "cost", "total_cost"):
            value = usage.get(key)
            if value is not None:
                return round(float(value), 6)
        rate = float(self.estimated_rate or 0)
        return round((token / 1000) * rate, 6)

    @staticmethod
    def _urllib_post(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
        # Keep the existing transport seam. Socket inactivity timeouts alone do
        # not bound slow headers/body; cancellation must close the live client.
        import anyio
        import httpx
        from anyio.from_thread import start_blocking_portal

        async def request() -> dict[str, Any]:
            with anyio.fail_after(timeout):
                async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    if response.status_code >= 300:
                        raise urllib.error.HTTPError(url, response.status_code, "request failed", {}, None)
                    result = response.json()
                    result.pop("__curis_routed_via", None)
                    routed_via = response.headers.get("X-Routed-Via", "")
                    if routed_via:
                        result["__curis_routed_via"] = routed_via
                    return result

        # Callers include an Orchestrator asyncio loop and synchronous routes.
        # A portal owns only this cancellable HTTP call, never DB writes/retries.
        with start_blocking_portal() as portal:
            return portal.call(request)
