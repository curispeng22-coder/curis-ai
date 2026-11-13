"""D1 execute() controlled-gate tests (scope A).

No real network, no real credentials. Exercises:

  A2  R3GatewayClient contract (is_configured / call / classify_error) with a
      mocked ``http_post`` so the adapter's real transport is never touched.
  A3  D1ExecutionOrchestrator: status() matrix (READY/DEGRADED/FROZEN), task-type
      validation, error classification, and the desensitized error surface.
  A4  D1 route integration (TestClient): frozen -> 503, execute_enabled=false ->
      503, both with a fixed, path/stack/key-free detail.
  A5  Mocked real-call success path: a fake toolchain whose model returns a
      controlled success dict yields a ``status=succeeded`` non-empty summary.

The genuine R3 end-to-end test is skipped until the security boundary seat
ratifies the credential-injection approach (no key is ever hardcoded here).

Desensitization red line is asserted throughout: no path / stack / key / parameter
leaks into any raised error, HTTP detail, or status.
"""

from __future__ import annotations

import os
import unittest
from unittest.mock import MagicMock

import pytest

from app.d1_config import D1ToolchainConfig, D1_UNAVAILABLE_MESSAGE
from app.d1_execute import (
    D1ExecutionError,
    D1ExecutionErrorCategory,
    D1ExecutionOrchestrator,
    D1ExecutionStatus,
    D1_TASK_INVALID_DETAIL,
)
from app.d1_gateway_client import R3GatewayClient
from app.d1_single_model_toolchain import D1ToolchainError
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.models.d1_execution_log import D1ExecutionLogRepository, D1ExecutionLogRow
from app.model_gateway import (
    ModelGatewayAdapter,
    ModelGatewayExecutionError,
    R3_GATEWAY_ID,
    R3_MODEL_ID,
    R3_PROFILE,
    R3_PROVIDER_ID,
)
from app.tenant_context import TenantContext


def _controlled_success_dict() -> dict:
    """A desensitized success payload shaped like ModelGatewayAdapter.execute()."""
    return {
        "output": "controlled-model-output",
        "provider_id": R3_PROVIDER_ID,
        "model_gateway_id": R3_GATEWAY_ID,
        "model_name": R3_MODEL_ID,
        "prompt_tokens": 100,
        "completion_tokens": 40,
        "total_tokens": 140,
        "estimated_cost": 0.001,
        "status": "success",
        "http_status": 200,
        "latency_ms": 1,
        "outbound_attempted": True,
    }


def _openai_chat_response() -> dict:
    """OpenAI-compatible chat-completions shape returned by a mocked ``http_post``."""
    return {
        "choices": [{"message": {"content": "controlled-model-output"}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 40, "total_tokens": 140},
    }


class FakeGatewayClient:
    """Isolation double for D1ExecutionOrchestrator: no real adapter needed."""

    def __init__(self, configured: bool = True) -> None:
        self._configured = configured
        self.classified: list[BaseException] = []

    def is_configured(self) -> bool:
        return self._configured

    def classify_error(self, error: BaseException) -> D1ExecutionErrorCategory:
        self.classified.append(error)
        return D1ExecutionErrorCategory.GATEWAY_TIMEOUT


class FakeToolchain:
    """Isolation double for D1SingleModelToolchain.execute()."""

    def __init__(self, result: dict | None = None, raise_error: BaseException | None = None) -> None:
        self._result = result or {
            "status": "succeeded",
            "total_tokens": 140,
            "estimated_cost": 0.001,
            "model_gateway_id": R3_GATEWAY_ID,
            "model_name": R3_MODEL_ID,
        }
        self._raise = raise_error
        self.calls = 0

    def execute(self) -> dict:
        self.calls += 1
        if self._raise is not None:
            raise self._raise
        return self._result


# ───────────────────────────── A2: R3GatewayClient ──────────────────────────
class R3GatewayClientTest(unittest.TestCase):
    def test_is_configured_true_when_runtime_declared(self) -> None:
        adapter = ModelGatewayAdapter(
            base_url="https://example.invalid", api_key="present", model_name="m"
        )
        self.assertTrue(R3GatewayClient(adapter).is_configured())

    def test_is_configured_false_when_runtime_empty(self) -> None:
        # 空适配器（未注入凭证）：脱敏判定为未就绪，且不暴露任何 Key。
        adapter = ModelGatewayAdapter(api_key="", model_name="")
        self.assertFalse(R3GatewayClient(adapter).is_configured())

    def test_call_delegates_and_returns_desensitized_result(self) -> None:
        captured = {}

        def fake_http_post(url, payload, headers, timeout):
            captured["url"] = url
            return _openai_chat_response()

        adapter = ModelGatewayAdapter(
            base_url="https://example.invalid", api_key="present", model_name="m",
            http_post=fake_http_post,
        )
        result = R3GatewayClient(adapter).call("hello")
        self.assertEqual(result["output"], "controlled-model-output")
        self.assertEqual(captured["url"], "https://example.invalid/v1/chat/completions")

    def test_classify_configuration_rejected_is_credential_missing(self) -> None:
        error = ModelGatewayExecutionError("incomplete", status="configuration_rejected")
        self.assertEqual(
            R3GatewayClient(MagicMock()).classify_error(error),
            D1ExecutionErrorCategory.CREDENTIAL_MISSING,
        )

    def test_classify_network_or_gateway_error_is_gateway_timeout(self) -> None:
        for status in ("network_error", "gateway_error", "rate_limited", "limit_rejected"):
            error = ModelGatewayExecutionError("boom", status=status)
            self.assertEqual(
                R3GatewayClient(MagicMock()).classify_error(error),
                D1ExecutionErrorCategory.GATEWAY_TIMEOUT,
            )

    def test_classify_transport_exception_is_gateway_timeout(self) -> None:
        error = ConnectionError("refused at /secret/path with key sk-xyz")
        self.assertEqual(
            R3GatewayClient(MagicMock()).classify_error(error),
            D1ExecutionErrorCategory.GATEWAY_TIMEOUT,
        )


# ──────────────────────── A3: D1ExecutionOrchestrator ───────────────────────
class D1ExecutionOrchestratorStatusTest(unittest.TestCase):
    def _make(self, *, frozen=False, configured=True, toolchain=None):
        config = D1ToolchainConfig(frozen=frozen, execute_enabled=True)
        client = FakeGatewayClient(configured=configured)
        return D1ExecutionOrchestrator(config, client, toolchain), config, client

    def test_status_frozen_when_config_frozen(self) -> None:
        orch, _, _ = self._make(frozen=True, toolchain=FakeToolchain())
        self.assertEqual(orch.status(), D1ExecutionStatus.FROZEN)

    def test_status_frozen_when_toolchain_none(self) -> None:
        orch, _, _ = self._make(toolchain=None)
        self.assertEqual(orch.status(), D1ExecutionStatus.FROZEN)

    def test_status_degraded_when_gateway_not_configured(self) -> None:
        orch, _, _ = self._make(configured=False, toolchain=FakeToolchain())
        self.assertEqual(orch.status(), D1ExecutionStatus.DEGRADED)

    def test_status_ready_when_configured_and_present(self) -> None:
        orch, _, _ = self._make(toolchain=FakeToolchain())
        self.assertEqual(orch.status(), D1ExecutionStatus.READY)

    def test_status_degraded_after_gateway_timeout(self) -> None:
        toolchain = FakeToolchain(raise_error=D1ToolchainError("model_call_failed"))
        orch, _, _ = self._make(toolchain=toolchain)
        self.assertEqual(orch.status(), D1ExecutionStatus.READY)
        with self.assertRaises(D1ExecutionError):
            orch.execute()
        # 最近一次分类为 GATEWAY_TIMEOUT -> 状态回落为 DEGRADED。
        self.assertEqual(orch.status(), D1ExecutionStatus.DEGRADED)


class D1ExecutionOrchestratorExecuteTest(unittest.TestCase):
    def _make(self, *, frozen=False, configured=True, toolchain=None, execute_enabled=True):
        config = D1ToolchainConfig(frozen=frozen, execute_enabled=execute_enabled)
        client = FakeGatewayClient(configured=configured)
        return D1ExecutionOrchestrator(config, client, toolchain), config, client

    def test_execute_unsupported_task_type_is_task_invalid_422(self) -> None:
        orch, _, _ = self._make(toolchain=FakeToolchain())
        with self.assertRaises(D1ExecutionError) as ctx:
            orch.execute(task_type="unsupported-task")
        self.assertEqual(ctx.exception.category, D1ExecutionErrorCategory.TASK_INVALID)
        self.assertEqual(ctx.exception.status_code, 422)
        self.assertEqual(ctx.exception.detail, D1_TASK_INVALID_DETAIL)

    def test_execute_degraded_is_credential_missing_503(self) -> None:
        orch, _, _ = self._make(configured=False, toolchain=FakeToolchain())
        with self.assertRaises(D1ExecutionError) as ctx:
            orch.execute()
        self.assertEqual(ctx.exception.category, D1ExecutionErrorCategory.CREDENTIAL_MISSING)
        self.assertEqual(ctx.exception.status_code, 503)
        self.assertEqual(ctx.exception.detail, D1_UNAVAILABLE_MESSAGE)

    def test_execute_frozen_is_503(self) -> None:
        orch, _, _ = self._make(frozen=True, toolchain=FakeToolchain())
        with self.assertRaises(D1ExecutionError) as ctx:
            orch.execute()
        self.assertEqual(ctx.exception.category, D1ExecutionErrorCategory.FROZEN)
        self.assertEqual(ctx.exception.status_code, 503)

    def test_execute_gateway_timeout_classified_503(self) -> None:
        toolchain = FakeToolchain(raise_error=D1ToolchainError("model_call_failed"))
        orch, _, _ = self._make(toolchain=toolchain)
        with self.assertRaises(D1ExecutionError) as ctx:
            orch.execute()
        self.assertEqual(ctx.exception.category, D1ExecutionErrorCategory.GATEWAY_TIMEOUT)
        self.assertEqual(ctx.exception.status_code, 503)
        self.assertEqual(ctx.exception.detail, D1_UNAVAILABLE_MESSAGE)

    def test_execute_credential_missing_from_model_config_503(self) -> None:
        toolchain = FakeToolchain(raise_error=D1ToolchainError("model_configuration_rejected"))
        orch, _, _ = self._make(toolchain=toolchain)
        with self.assertRaises(D1ExecutionError) as ctx:
            orch.execute()
        self.assertEqual(ctx.exception.category, D1ExecutionErrorCategory.CREDENTIAL_MISSING)
        self.assertEqual(ctx.exception.status_code, 503)

    def test_execute_non_model_d1_error_propagates(self) -> None:
        # scope/工具/审计类失败不归四类枚举，原样向上抛 D1ToolchainError（路由按 409 处理）。
        toolchain = FakeToolchain(raise_error=D1ToolchainError("scope_rejected"))
        orch, _, _ = self._make(toolchain=toolchain)
        with self.assertRaises(D1ToolchainError):
            orch.execute()

    def test_execute_success_returns_succeeded_summary(self) -> None:
        # mock 真实调用成功路径：模型返回受控成功 dict，工具链汇总为 succeeded 摘要。
        toolchain = FakeToolchain(
            result={
                "status": "succeeded",
                "total_tokens": 140,
                "estimated_cost": 0.001,
                "model_gateway_id": R3_GATEWAY_ID,
                "model_name": R3_MODEL_ID,
            }
        )
        orch, _, _ = self._make(toolchain=toolchain)
        summary = orch.execute()
        self.assertEqual(summary["status"], "succeeded")
        self.assertGreater(len(summary), 0)
        self.assertEqual(toolchain.calls, 1)

    def test_classify_maps_failure_codes(self) -> None:
        orch, _, _ = self._make(toolchain=FakeToolchain())
        self.assertEqual(
            orch._classify(D1ToolchainError("model_call_failed")),
            D1ExecutionErrorCategory.GATEWAY_TIMEOUT,
        )
        self.assertEqual(
            orch._classify(D1ToolchainError("model_configuration_rejected")),
            D1ExecutionErrorCategory.CREDENTIAL_MISSING,
        )
        self.assertIsNone(orch._classify(D1ToolchainError("scope_rejected")))


# ─────────────────────────── A4: D1 route integration ───────────────────────
class D1RouteIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self._env = {}
        for key in ("CURIS_D1_FROZEN", "CURIS_D1_EXECUTE_ENABLED", "CURIS_DB"):
            self._env[key] = os.environ.pop(key, None)
        import tempfile

        self._tmp = tempfile.mkdtemp()
        os.environ["CURIS_DB"] = os.path.join(self._tmp, "curis.sqlite")

    def tearDown(self) -> None:
        for key, value in self._env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def _client(self, frozen: str = "false", execute_enabled: str = "false"):
        os.environ["CURIS_D1_FROZEN"] = frozen
        os.environ["CURIS_D1_EXECUTE_ENABLED"] = execute_enabled
        from app.main import create_app

        app = create_app()
        from fastapi.testclient import TestClient

        return TestClient(app)

    def _assert_degraded_503(self, client) -> None:
        resp = client.post("/api/workspace/internal/d1-tenant-reservation/run")
        self.assertEqual(resp.status_code, 503)
        detail = resp.json()["detail"]
        # 脱敏红线：固定常量，且不得含路径/堆栈/Key/参数。
        self.assertEqual(detail, D1_UNAVAILABLE_MESSAGE)
        self.assertNotIn("/", detail)
        self.assertNotIn("sk-", detail)
        self.assertNotIn("key", detail.lower())

    def test_route_frozen_returns_503(self) -> None:
        self._assert_degraded_503(self._client(frozen="true"))

    def test_route_execute_disabled_returns_503(self) -> None:
        # execute_enabled 默认 false（未拍板）-> 整体降级 503，不真实调用。
        self._assert_degraded_503(self._client(frozen="false", execute_enabled="false"))


# ───────────── A5: 真实网关端到端（待安全边界席裁定后补，硬编 Key 禁止） ─────────────
@pytest.mark.skip(
    reason="待安全边界席裁定 R3 凭证接入方式后补；本测试不硬编 Key、不读真实凭证"
)
def test_real_gateway_end_to_end_is_blocked_until_ratified():
    """真实 R3 网关端到端验证：仅在安全边界席裁定凭证接入方式后启用。

    期间不得硬编码 CURIS_MODEL_GATEWAY_API_KEY 或读取真实凭证；测试须从受控
    凭证注入边界获取适配器实例。
    """
    raise AssertionError("R3 credential injection not yet ratified by security boundary seat")


# ───────────────────────── B1/B2: 落库仓储与编排层写入 ─────────────────────────
class FakeExecutionLog:
    """Isolation double for D1ExecutionLogRepository; records insert calls."""

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def insert(self, *, tenant_id, task_type, status, error_category, duration_ms, token_count) -> int:
        self.rows.append(
            {
                "tenant_id": tenant_id,
                "task_type": task_type,
                "status": status,
                "error_category": error_category,
                "duration_ms": duration_ms,
                "token_count": token_count,
            }
        )
        return len(self.rows)


class D1ExecutionLogRepositoryTest(unittest.TestCase):
    def _repo(self):
        import tempfile

        path = tempfile.mkdtemp()
        db = Database(os.path.join(path, "curis.sqlite"))
        db.initialize()
        return D1ExecutionLogRepository(db), db

    def test_table_registered_and_insert_queryable(self) -> None:
        repo, _ = self._repo()
        row_id = repo.insert(
            tenant_id="selfuse",
            task_type="d1-tenant-reservation",
            status="succeeded",
            error_category=None,
            duration_ms=12,
            token_count=140,
        )
        self.assertGreater(row_id, 0)
        recent = repo.recent()
        self.assertEqual(len(recent), 1)
        self.assertIsInstance(recent[0], D1ExecutionLogRow)
        self.assertEqual(recent[0].status, "succeeded")
        self.assertEqual(recent[0].token_count, 140)
        self.assertIsNone(recent[0].error_category)
        # 脱敏红线：落库字段不含路径/Key/参数。
        self.assertNotIn("/", recent[0].tenant_id + recent[0].task_type)

    def test_count_by_status_aggregates(self) -> None:
        repo, _ = self._repo()
        repo.insert(tenant_id="t", task_type="d1-tenant-reservation", status="succeeded",
                    error_category=None, duration_ms=1, token_count=1)
        repo.insert(tenant_id="t", task_type="d1-tenant-reservation", status="gateway_timeout",
                    error_category="gateway_timeout", duration_ms=2, token_count=0)
        self.assertEqual(repo.count_by_status(), {"succeeded": 1, "gateway_timeout": 1})


class D1ExecutionOrchestratorPersistenceTest(unittest.TestCase):
    def _make(self, toolchain=None, execution_log=None, event_log=None, configured=True):
        config = D1ToolchainConfig(frozen=False, execute_enabled=True)
        client = FakeGatewayClient(configured=configured)
        return D1ExecutionOrchestrator(config, client, toolchain, execution_log, event_log)

    def test_success_writes_succeeded_row_with_tokens(self) -> None:
        log = FakeExecutionLog()
        toolchain = FakeToolchain(
            result={"status": "succeeded", "total_tokens": 140, "estimated_cost": 0.001}
        )
        orch = self._make(toolchain=toolchain, execution_log=log)
        summary = orch.execute()
        self.assertEqual(summary["status"], "succeeded")
        self.assertEqual(len(log.rows), 1)
        row = log.rows[0]
        self.assertEqual(row["status"], "succeeded")
        self.assertEqual(row["token_count"], 140)
        # task_type 列仅记配置常量，绝不记调用方传入的参数。
        self.assertEqual(row["task_type"], "d1-tenant-reservation")
        self.assertIsNone(row["error_category"])

    def test_gateway_timeout_writes_classified_row(self) -> None:
        log = FakeExecutionLog()
        toolchain = FakeToolchain(raise_error=D1ToolchainError("model_call_failed"))
        orch = self._make(toolchain=toolchain, execution_log=log)
        with self.assertRaises(D1ExecutionError):
            orch.execute()
        self.assertEqual(len(log.rows), 1)
        row = log.rows[0]
        self.assertEqual(row["status"], "gateway_timeout")
        self.assertEqual(row["error_category"], "gateway_timeout")
        self.assertEqual(row["token_count"], 0)

    def test_task_invalid_writes_task_invalid_row(self) -> None:
        log = FakeExecutionLog()
        orch = self._make(toolchain=FakeToolchain(), execution_log=log)
        with self.assertRaises(D1ExecutionError):
            orch.execute(task_type="unsupported-task")
        self.assertEqual(log.rows[0]["status"], "task_invalid")

    def test_no_sink_does_not_record(self) -> None:
        # execution_log / event_log 为 None 时（隔离单测）不应报错。
        orch = self._make(toolchain=FakeToolchain())
        summary = orch.execute()
        self.assertEqual(summary["status"], "succeeded")


# ───────────────────────── B4: 可观测（EvolutionEventLog） ─────────────────────────
class D1ExecutionObservabilityTest(unittest.TestCase):
    def _make(self, toolchain, configured=True):
        import tempfile

        path = tempfile.mkdtemp()
        db = Database(os.path.join(path, "curis.sqlite"))
        db.initialize()
        event_log = EvolutionEventLog(db)
        config = D1ToolchainConfig(frozen=False, execute_enabled=True)
        client = FakeGatewayClient(configured=configured)
        return D1ExecutionOrchestrator(config, client, toolchain, event_log=event_log), event_log

    def test_success_emits_observability_event(self) -> None:
        orch, event_log = self._make(FakeToolchain(result={"status": "succeeded", "total_tokens": 99}))
        orch.execute()
        events = [e for e in event_log.get_all() if e["event_type"] == "d1.execution.succeeded"]
        self.assertEqual(len(events), 1)
        payload = events[0]["payload"]
        self.assertEqual(payload["status"], "succeeded")
        self.assertEqual(payload["token_count"], 99)
        self.assertEqual(payload["error_category"], None)
        self.assertNotIn("key", str(payload).lower())

    def test_failure_emits_classified_observability_event(self) -> None:
        orch, event_log = self._make(FakeToolchain(raise_error=D1ToolchainError("model_call_failed")))
        with self.assertRaises(D1ExecutionError):
            orch.execute()
        events = [e for e in event_log.get_all() if e["event_type"] == "d1.execution.gateway_timeout"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["payload"]["error_category"], "gateway_timeout")


# ───────────────────────── B3: 只读状态端点 ─────────────────────────
class D1StatusEndpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self._env = {}
        for key in ("CURIS_D1_FROZEN", "CURIS_D1_EXECUTE_ENABLED", "CURIS_DB"):
            self._env[key] = os.environ.pop(key, None)
        import tempfile

        self._tmp = tempfile.mkdtemp()
        os.environ["CURIS_DB"] = os.path.join(self._tmp, "curis.sqlite")

    def tearDown(self) -> None:
        for key, value in self._env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def _client(self, frozen="false"):
        os.environ["CURIS_D1_FROZEN"] = frozen
        from app.main import create_app
        from fastapi.testclient import TestClient

        return TestClient(create_app())

    def test_status_ready(self) -> None:
        client = self._client(frozen="false")
        resp = client.get("/api/workspace/internal/d1-tenant-reservation/status")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(resp.json()["status"], ("ready", "degraded", "frozen"))

    def test_status_frozen_when_config_frozen(self) -> None:
        client = self._client(frozen="true")
        resp = client.get("/api/workspace/internal/d1-tenant-reservation/status")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "frozen")
        # 不泄露凭证/路径。
        self.assertNotIn("key", str(resp.json()).lower())


if __name__ == "__main__":
    unittest.main()
