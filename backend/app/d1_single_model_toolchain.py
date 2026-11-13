from __future__ import annotations

import hashlib
import json
import threading
from typing import Any

from .evolution_event_log import EvolutionEventLog
from .local_rd_toolset import LocalRDToolScope, LocalRDToolset
from .model_gateway import (
    ModelGatewayAdapter,
    ModelGatewayExecutionError,
    R3_BASE_URL,
    R3_GATEWAY_ID,
    R3_MAX_INPUT_TOKENS,
    R3_MAX_OUTPUT_TOKENS,
    R3_MAX_TOTAL_TOKENS,
    R3_MODEL_ID,
    R3_PROFILE,
    R3_PROVIDER_ID,
)
from . import local_rd_toolset as local_rd_toolset_module
from .d1_config import D1ToolchainConfig
from .tenant_context import TenantContext


D1_TENANT_ID = "selfuse"
D1_PROJECT_ID = "curis-ai-workspace"
D1_TASK_ID = "d1-tenant-reservation"
D1_RUN_ID = "20260718-workspace-d1-tenant-reservation-single-model-e2e"
D1_TARGET_PATH = "tools/verify_d1_tenant_reservation.py"
D1_TEST_PATH = "backend/tests/test_d1_verify_script.py"
D1_ALLOWED_PATHS = (D1_TARGET_PATH, D1_TEST_PATH)
D1_COMMAND_ID = "rd_e2e_verify_d1_tenant_reservation"
D1_COMMAND_ARGV = (
    "backend/.venv/bin/python",
    "-m",
    "pytest",
    "-q",
    D1_TEST_PATH,
)
D1_MAX_DIFF_BYTES = 4 * 1024
D1_MAX_COST_USD = 0.02
D1_SEARCH_QUERY = "DEFAULT_TENANT"
D1_ROUTE = "/api/workspace/internal/d1-tenant-reservation/run"


class D1ToolchainError(RuntimeError):
    def __init__(self, failure_code: str, message: str = "D1 toolchain rejected") -> None:
        super().__init__(message)
        self.failure_code = failure_code


class D1SingleModelToolchain:
    """One fixed D1 model call followed by one fixed local tool chain."""

    def __init__(
        self,
        model: ModelGatewayAdapter,
        read_tools: LocalRDToolset,
        write_tools: LocalRDToolset,
        git_tools: LocalRDToolset,
        event_log: EvolutionEventLog,
    ) -> None:
        self.model = model
        self.read_tools = read_tools
        self.write_tools = write_tools
        self.git_tools = git_tools
        self.event_log = event_log
        self._lock = threading.Lock()

    def execute(self) -> dict[str, Any]:
        with self._lock:
            self._preflight()
            self._claim_once()
            rollback = None
            model_called = False
            try:
                target = self.read_tools.read_file(json.dumps({"path": D1_TARGET_PATH}))
                test = self.read_tools.read_file(json.dumps({"path": D1_TEST_PATH}))
                self.read_tools.search(json.dumps({"query": D1_SEARCH_QUERY}))
                prompt = self._prompt(target, test)
                model_called = True
                model_result = self._call_model(prompt)
                diff = self._approved_diff(model_result.get("output"))
                writer, rollback = self.write_tools._apply_diff_transactional(
                    json.dumps(
                        {
                            "diff": diff,
                            "preimage_hashes": {
                                D1_TARGET_PATH: target["output"]["sha256"]
                            },
                        }
                    )
                )
                test_result = self.write_tools.run_test(
                    json.dumps({"command_id": D1_COMMAND_ID})
                )
                git_diff = self.git_tools.git_read(json.dumps({"operation": "diff"}))
                git_check = self.git_tools.git_read(
                    json.dumps({"operation": "diff_check"})
                )
                summary = {
                    "run_id": D1_RUN_ID,
                    "status": "succeeded",
                    "target_path": D1_TARGET_PATH,
                    "preimage_hash": writer["output"]["files"][0]["preimage_hash"],
                    "postimage_hash": writer["output"]["files"][0]["postimage_hash"],
                    "command_id": D1_COMMAND_ID,
                    "test_exit_code": test_result["output"]["exit_code"],
                    "git_diff_hash": git_diff["output"]["output_hash"],
                    "git_diff_check_exit_code": git_check["output"]["exit_code"],
                    "model_gateway_id": model_result["model_gateway_id"],
                    "model_name": model_result["model_name"],
                    "total_tokens": model_result["total_tokens"],
                    "estimated_cost": model_result["estimated_cost"],
                }
                self._record("d1.toolchain.succeeded", "succeeded", "", summary)
                return summary
            except Exception as error:
                if rollback is not None:
                    rollback()
                failure_code = getattr(error, "failure_code", "toolchain_failed")
                try:
                    self._record(
                        "d1.toolchain.failed",
                        "failed",
                        str(failure_code),
                        {"model_call": int(model_called)},
                    )
                except Exception:
                    pass
                if isinstance(error, D1ToolchainError):
                    raise
                raise D1ToolchainError(str(failure_code)) from error

    def _preflight(self) -> None:
        identity = TenantContext.current_identity()
        if (
            TenantContext.current_tenant_id() != D1_TENANT_ID
            or identity.get("tenant_id") != D1_TENANT_ID
            or identity.get("membership_status") != "active"
            or identity.get("role") not in {"owner", "ceo"}
            or not identity.get("ceo_id")
            or not identity.get("request_id")
        ):
            raise D1ToolchainError("scope_rejected")
        if (
            self.model.profile != R3_PROFILE
            or self.model.base_url != R3_BASE_URL
            or self.model.gateway_id != R3_GATEWAY_ID
            or self.model.model_name != R3_MODEL_ID
            or self.model.timeout != 60
            or not self.model.api_key
        ):
            raise D1ToolchainError("model_configuration_rejected")
        expected_scope = (D1_TENANT_ID, D1_PROJECT_ID, D1_TASK_ID, D1_RUN_ID)
        for tools, paths in (
            (self.read_tools, frozenset(D1_ALLOWED_PATHS)),
            (self.write_tools, frozenset(D1_ALLOWED_PATHS)),
            (self.git_tools, frozenset({D1_TARGET_PATH})),
        ):
            scope = tools.scope
            if (
                (scope.tenant_id, scope.project_id, scope.task_id, scope.run_id)
                != expected_scope
                or tools.allowed_paths != paths
            ):
                raise D1ToolchainError("tool_scope_rejected")
        if self.read_tools.command_registry or self.git_tools.command_registry:
            raise D1ToolchainError("command_scope_rejected")
        if self.write_tools.command_registry != {D1_COMMAND_ID: D1_COMMAND_ARGV}:
            raise D1ToolchainError("command_scope_rejected")
        if not callable(getattr(self.event_log, "record", None)) or not getattr(
            self.event_log, "database", None
        ):
            raise D1ToolchainError("audit_unavailable")

    def _claim_once(self) -> None:
        with self.event_log.database.connect() as connection:
            connection.execute("begin immediate")
            existing = connection.execute(
                "select 1 from evolution_events where tenant_id=? and correlation_id=? "
                "and (event_type like 'd1.toolchain.%' or event_type='usage.model_call') limit 1",
                (D1_TENANT_ID, D1_RUN_ID),
            ).fetchone()
            if existing is not None:
                raise D1ToolchainError("run_already_consumed")
            connection.execute(
                "insert into evolution_events "
                "(correlation_id,event_type,payload,tenant_id,idempotency_key) values (?,?,?,?,?)",
                (
                    D1_RUN_ID,
                    "d1.toolchain.started",
                    json.dumps(
                        {
                            "run_id": D1_RUN_ID,
                            "tenant_id": D1_TENANT_ID,
                            "project_id": D1_PROJECT_ID,
                            "task_id": D1_TASK_ID,
                            "outcome": "started",
                        }
                    ),
                    D1_TENANT_ID,
                    f"{D1_RUN_ID}:started",
                ),
            )

    def _prompt(self, target: dict[str, Any], test: dict[str, Any]) -> str:
        sections = []
        for expected_path, result in ((D1_TARGET_PATH, target), (D1_TEST_PATH, test)):
            output = result.get("output", {})
            if output.get("path") != expected_path or any(
                line.get("truncated") for line in output.get("lines", [])
            ):
                raise D1ToolchainError("reader_output_rejected")
            content = "\n".join(line["text"] for line in output.get("lines", []))
            if output.get("ends_with_newline"):
                content += "\n"
            sections.append(f"[FILE {expected_path}]\n{content}")
        prompt = (
            "Fix only the D1 tenant reservation verifier. The SQLite column sentinel remains "
            "'default'; runtime DEFAULT_TENANT is 'selfuse'. Return exactly one raw unified diff "
            f"for {D1_TARGET_PATH}, with no Markdown or explanation.\n\n"
            + "\n".join(sections)
        )
        if len(prompt.encode("utf-8")) > R3_MAX_INPUT_TOKENS:
            raise D1ToolchainError("model_input_limit_rejected")
        return prompt

    def _call_model(self, prompt: str) -> dict[str, Any]:
        try:
            result = self.model.execute(prompt)
        except ModelGatewayExecutionError as error:
            if error.outbound_attempted:
                self._record_model_usage(
                    {
                        "usage_record_id": getattr(error, "usage_record_id", ""),
                        "status": error.status,
                        "outbound_attempted": True,
                    }
                )
            raise D1ToolchainError("model_call_failed") from error
        if (
            result.get("model_gateway_id") != R3_GATEWAY_ID
            or result.get("model_name") != R3_MODEL_ID
            or result.get("provider_id") != R3_PROVIDER_ID
            or not result.get("outbound_attempted")
            or not 0 < int(result.get("total_tokens", 0)) <= R3_MAX_TOTAL_TOKENS
            or not 0 <= int(result.get("completion_tokens", 0)) <= R3_MAX_OUTPUT_TOKENS
            or not 0 < float(result.get("estimated_cost", 0)) <= D1_MAX_COST_USD
        ):
            self._record_model_usage({**result, "status": "model_result_rejected"})
            raise D1ToolchainError("model_result_rejected")
        self._record_model_usage(result)
        return result

    @staticmethod
    def _approved_diff(value: Any) -> str:
        if not isinstance(value, str) or not value or len(value.encode("utf-8")) > D1_MAX_DIFF_BYTES:
            raise D1ToolchainError("diff_limit_rejected")
        if "```" in value or value.count("\n--- ") or not value.startswith(
            f"--- a/{D1_TARGET_PATH}\n+++ b/{D1_TARGET_PATH}\n"
        ):
            raise D1ToolchainError("diff_shape_rejected")
        return value

    def _record_model_usage(self, result: dict[str, Any]) -> None:
        usage_record_id = str(result.get("usage_record_id") or "")
        if not usage_record_id:
            raise D1ToolchainError("usage_audit_failed")
        self.event_log.record(
            correlation_id=D1_RUN_ID,
            event_type="d1.model_call_linked",
            tenant_id=D1_TENANT_ID,
            idempotency_key=f"{D1_RUN_ID}:model-call",
            payload={
                "usage_record_id": usage_record_id,
                "run_id": D1_RUN_ID,
                "workflow_run_id": D1_RUN_ID,
                "tenant_id": D1_TENANT_ID,
                "project_id": D1_PROJECT_ID,
                "task_id": D1_TASK_ID,
                "capability_type": "model",
                "capability_id": R3_MODEL_ID,
                "capability_source": "official",
                "status": str(result.get("status", "failed")),
                "outbound_attempted": bool(result.get("outbound_attempted", False)),
            },
        )

    def _record(
        self,
        event_type: str,
        outcome: str,
        failure_code: str,
        fields: dict[str, Any],
    ) -> None:
        payload = {
            "run_id": D1_RUN_ID,
            "tenant_id": D1_TENANT_ID,
            "project_id": D1_PROJECT_ID,
            "task_id": D1_TASK_ID,
            "outcome": outcome,
            "failure_code": failure_code,
            **fields,
        }
        self.event_log.record(
            correlation_id=D1_RUN_ID,
            event_type=event_type,
            tenant_id=D1_TENANT_ID,
            idempotency_key=f"{D1_RUN_ID}:{event_type}",
            payload=payload,
        )


def build_d1_toolchain(
    model: ModelGatewayAdapter,
    event_log: EvolutionEventLog,
    config: "D1ToolchainConfig | None" = None,
) -> D1SingleModelToolchain | None:
    # kill-switch：frozen 配置即整体回退到降级态（→ None → 503 守卫）。
    if config is not None and config.frozen:
        return None
    # 将配置中的可选覆盖位注入 local_rd_toolset（仅当非 None）。
    if config is not None and config.workspace_root_override is not None:
        local_rd_toolset_module._WORKSPACE_ROOT_OVERRIDE = config.workspace_root_override
    scope = LocalRDToolScope(
        tenant_id=D1_TENANT_ID,
        project_id=D1_PROJECT_ID,
        task_id=D1_TASK_ID,
        run_id=D1_RUN_ID,
        allowed_paths=D1_ALLOWED_PATHS,
    )
    git_scope = LocalRDToolScope(
        tenant_id=D1_TENANT_ID,
        project_id=D1_PROJECT_ID,
        task_id=D1_TASK_ID,
        run_id=D1_RUN_ID,
        allowed_paths=(D1_TARGET_PATH,),
    )
    return D1SingleModelToolchain(
        model,
        LocalRDToolset(scope, event_log),
        LocalRDToolset(scope, event_log, {D1_COMMAND_ID: D1_COMMAND_ARGV}),
        LocalRDToolset(git_scope, event_log),
        event_log,
    )
