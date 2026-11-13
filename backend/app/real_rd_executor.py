"""真实研发工具闭环（Issue 驱动）执行器。

本模块是 D1 ``execute()`` 范围 A/B 闭环之后的增量单模块，仅新增、
不重写任何受保护文件（``local_rd_toolset.py`` / ``model_gateway.py`` /
``evolution_event_log.py`` / ``d1_single_model_toolchain.py``）。

职责：给定一个结构化 ``issue_spec``，编排三个 ``LocalRDToolset`` 实例
（read / write / git）与真实模型网关，按「读代码 → 改代码 → 跑测试 →
交付 Diff」的每轮闭环迭代，直到测试通过或耗尽轮次。

设计铁律（全部复用既有受控能力，不重新实现）：
- 路径白名单 / 敏感路径拒绝：交给 ``LocalRDToolset._reject_forbidden_path``。
- 事务化写 + 乐观锁：复用 ``LocalRDToolset._apply_diff_transactional`` 返回的
  ``rollback``；preimage 取自 ``read_file`` 的 ``sha256``。
- 单主占锁：借鉴 D1 ``_claim_once`` 的 ``event_log.database.connect()`` +
  ``begin immediate`` 模式，无 ``.database`` 时降级跳过（测试态）。
- 脱敏：异常只携带固定 ``failure_code``，绝不带路径 / 堆栈 / Key / 参数；
  ``diff_text`` 作为受控产物允许返回。

无新依赖、无 HTTP 端点、无 UI。
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any, Callable

from .dev_agent import DevAgent
from .evolution_event_log import EvolutionEventLog
from .local_rd_toolset import (
    LocalRDToolError,
    LocalRDToolScope,
    LocalRDToolset,
    SandboxMode,
)
# B 层运行时治理边界（T05 接线点）：G3 删/覆盖受保护数据 + G4 token 预算。
from .runtime_governance import (
    ActionContext,
    evaluate,
    load_config,
    outcome_for_letter,
)
# 真实 DecisionSink 后端机制（T-DS1 接线信号；仅类型依赖，零新依赖）。
from .decision_sink import PendingDecisionRaised
# Issue C · 内部预算硬停护栏（default-off）。独立自主硬停机制，不解除人工批准闸；
# 复用 RealRDExecutorError("budget_exceeded") 作为脱敏硬停信号。
from .budget_guard import BudgetGuard
# Issue A · 通用 Agent Execution Kernel 接线（T-A4，default-off）。
# 仅当 agent_kernel_enabled=True 时建立 wake→claim→session（单执行者保证 +
# 可恢复记录）；接线点位于 runtime_governance.evaluate() 之后，不重评
# gate、不绕过 b.governance.gate 决策链；事件独立追加写 a.kernel.*。
from .agent_execution_kernel import ExecutionClaimStore
from .agent_wakeup_session import AgentTaskSessionStore, WakeRequestStore
from .run_config_fingerprint import (
    RunConfig,
    build_idempotency_key,
    compute_fingerprint,
)

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
REAL_RD_RUN_ID_PREFIX = "real-rd:"
REAL_RD_STARTED_EVENT = "real_rd.run.started"
REAL_RD_SUMMARY_OK = "real_rd.run.succeeded"
REAL_RD_SUMMARY_FAIL = "real_rd.run.failed"

# 当 issue_spec 未显式提供租户/项目/任务时使用的默认值（本模块不读取
# TenantContext 身份，仅受 LocalRDToolset 既有作用域约束）。
DEFAULT_TENANT_ID = "real-rd-tenant"
DEFAULT_PROJECT_ID = "real-rd-project"

# pytest 受验命令模板前缀（与 LocalRDToolset._validate_command_registry 对齐）。
_PYTEST_COMMAND_PREFIX = ("backend/.venv/bin/python", "-m", "pytest", "-q")

# 20260722 RealRD 单次真实取证 Gate 的服务端固定 fixture。Task.content 只保存
# 本次实例的动态 ID 与该固定契约快照；它不是可扩展 registry，也不接受客户端
# 选择 target / command / argv。
_EVIDENCE_FIXTURE_SCHEMA = "real_rd_single_call_fixture/v1"
_EVIDENCE_ISSUE_ID = "20260722_real_rd_single_call_evidence_gate"
_EVIDENCE_RUN_SOURCE = "real_rd_single_call_evidence_gate/v1"
_EVIDENCE_TARGET_FILES = ("tools/real_rd_fixture/target_b.py",)
_EVIDENCE_TEST_FILE = "backend/tests/test_real_rd_fixture_b.py"
_EVIDENCE_COMMAND_ID = "rd_evidence_fixture_b_v1"
_EVIDENCE_TEST_COMMAND_ARGV = (_EVIDENCE_TEST_FILE,)
_EVIDENCE_REGISTERED_ARGV = (*_PYTEST_COMMAND_PREFIX, _EVIDENCE_TEST_FILE)
_EVIDENCE_TOOL_ID = "real_rd_executor_tool"
_EVIDENCE_AUDIT_FIELDS = {
    "correlation": [
        "tenant_id",
        "project_id",
        "task_id",
        "workflow_run_id",
        "workflow_step_id",
    ],
    "tool_usage": [
        "tool_id",
        "request_id",
        "outcome",
        "failure_code",
        "exit_code",
        "duration_ms",
        "timestamp",
        "capability_type",
        "capability_id",
        "capability_source",
        "model_call",
        "total_tokens",
        "estimated_cost",
        "cost_source",
        "outbound_attempted",
        "path_hash",
        "content_hash",
        "preimage_hash",
        "postimage_hash",
        "command_id",
        "sandbox_degraded",
    ],
    "model_usage": [
        "provider_id",
        "model_gateway_id",
        "model_name",
        "model_call",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "unit_price_input",
        "unit_price_output",
        "price_version",
        "estimated_cost",
        "currency",
        "cost_source",
        "status",
        "http_status",
        "latency_ms",
        "outbound_attempted",
    ],
}
_EVIDENCE_MAPPING_KEYS = frozenset(
    {
        "schema",
        "issue_id",
        "run_source",
        "operation_id",
        "fixture_id",
        "fixture_sha256",
        "target_files",
        "test_command_id",
        "test_command_argv",
        "registered_argv",
        "allow_paths",
        "tenant_id",
        "company_id",
        "department_id",
        "project_id",
        "workflow_run_id",
        "workflow_step_id",
        "employee_id",
        "employee_role",
        "tool_binding_id",
        "tool_capability_id",
        "audit_fields",
    }
)


def _evidence_fixture_sha256() -> str:
    """Return the fixed fixture manifest hash without exposing file contents."""

    repository_root = Path(__file__).resolve().parents[2]
    entries = []
    for relative_path in (*_EVIDENCE_TARGET_FILES, _EVIDENCE_TEST_FILE):
        content = (repository_root / relative_path).read_bytes()
        entries.append(
            {
                "path": relative_path,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    manifest = json.dumps(
        entries, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(manifest).hexdigest()

# 工具层在「应用 diff」阶段可能抛出的、可通过重生成 diff 自愈的错误。
# 这些错误发生在尚未落盘（或已回滚）时，应作为可恢复轮次重试，而非致命。
_RETRYABLE_TOOL_ERRORS = frozenset(
    {
        "diff_invalid",
        "diff_context_mismatch",
        "preimage_hash_invalid",
        "preimage_hash_mismatch",
        "duplicate_diff_path",
    }
)

# Issue C · 内部预算硬停配置落点（default-off，enabled=false → 零回归）。
_BUDGET_GUARD_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "budget_guard_config.json"
)


class _RoundFailed(Exception):
    """内部信号：当前轮被认为是可恢复的失败，应回滚并进入下一轮重试。

    与 ``RealRDExecutorError`` 严格区分——后者一律视为致命并向上抛出。
    """


class RealRDExecutorError(RuntimeError):
    """脱敏异常。

    只携带固定的 ``failure_code``；``message`` 为通用脱敏文案，绝不带
    文件系统路径、堆栈、密钥或输入参数。所有对外异常均应为本类型。
    """

    def __init__(self, failure_code: str, *, message: str | None = None) -> None:
        self.failure_code = failure_code
        super().__init__(message or "real rd executor operation failed")


class RealRDExecutor:
    """Issue 驱动的读→改→测→交付 Diff 编排器。

    通过 ``run(issue_spec)`` 驱动闭环；构造时仅注入模型网关与事件日志，
    三个 ``LocalRDToolset`` 实例在每次 ``run`` 内按需构造。
    """

    # 与 ``local_rd_toolset._HUNK`` 对齐的 unified-diff hunk 头正则。
    # 用于归一模型产出 diff 的 old/new 行数计数（详见 ``_normalize_diff_counts``）。
    _HUNK_RE = re.compile(
        r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?\n?$"
    )

    def __init__(
        self,
        model: DevAgent,
        event_log: EvolutionEventLog,
        toolset_cls: type | None = None,
        *,
        sandbox_mode: SandboxMode | str | None = None,
        agent_kernel_enabled: bool = False,
        budget_guard_enabled: bool = False,
    ) -> None:
        self.model = model
        self.event_log = event_log
        # 允许注入 LocalRDToolset 的子类（例如在无 macOS sandbox-exec 的
        # 执行环境 / CI 中用绕过沙箱包装的变体），默认沿用标准实现。
        self.toolset_cls = toolset_cls or LocalRDToolset
        # sandbox 网络隔离模式：透传给三个 LocalRDToolset 实例（仅关键字、默认 None）。
        self.sandbox_mode = sandbox_mode
        # Issue A · 通用 Agent Execution Kernel 接线总开关（default-off）。
        # 仅当为 True 时，run() 入口才建立 wake→claim→session 并落
        # a.kernel.* 事件；默认 False 保证既有 8 passed 零回归。
        self.agent_kernel_enabled = agent_kernel_enabled
        # Issue C · 内部预算硬停接线总开关（default-off，镜像 agent_kernel_enabled）。
        # 仅当为 True 时，run() 主循环在 evaluate() 之后调用 budget_guard.check()；
        # 默认 False 保证既有 test_real_rd_executor.py 8 passed 零回归。
        self.budget_guard_enabled = budget_guard_enabled
        # 按配置（默认 off）构造护栏实例；配置加载失败按 fail-closed 语义处理。
        self._budget_guard = BudgetGuard(
            config_path=_BUDGET_GUARD_CONFIG_PATH,
            database=getattr(event_log, "database", None),
            event_log=event_log,
        )

    # ------------------------------------------------------------------ #
    # 公共入口
    # ------------------------------------------------------------------ #
    def run(
        self,
        issue_spec: dict[str, Any],
        *,
        decision_sink: Any = None,
        pending_sink: Any = None,
    ) -> dict[str, Any]:
        """按 issue_spec 执行真实研发闭环，返回脱敏结果字典。

        返回 schema（详见设计文档 3.2）：
        ``{issue_id, status, rounds, diff_text, test_exit_code, files,
        total_tokens, estimated_cost, audit_event_count,
        model_gateway_id, model_name}``。
        """
        self._validate_spec(issue_spec)

        issue_id = str(issue_spec["issue_id"])
        target_files = [str(f) for f in issue_spec["target_files"]]
        test_command_id = str(issue_spec["test_command_id"])
        test_command_argv = [str(a) for a in issue_spec["test_command_argv"]]
        instructions = str(issue_spec["instructions"])
        max_rounds = int(issue_spec.get("max_rounds", 3) or 3)
        allow_paths = [str(p) for p in issue_spec["allow_paths"]]
        tenant_id = str(issue_spec.get("tenant_id") or DEFAULT_TENANT_ID)
        project_id = str(issue_spec.get("project_id") or DEFAULT_PROJECT_ID)
        task_id = str(issue_spec.get("task_id") or issue_id)
        workflow_run_id = str(issue_spec.get("workflow_run_id") or "")
        workflow_step_id = str(issue_spec.get("workflow_step_id") or "")
        if bool(workflow_run_id) != bool(workflow_step_id):
            raise RealRDExecutorError("usage_scope_invalid")
        run_id = workflow_run_id or f"{REAL_RD_RUN_ID_PREFIX}{issue_id}"
        if workflow_run_id:
            self._validate_persistent_scope(
                tenant_id,
                project_id,
                task_id,
                workflow_run_id,
                workflow_step_id,
                target_files=target_files,
                test_command_id=test_command_id,
                test_command_argv=test_command_argv,
                allow_paths=allow_paths,
            )

        # B 层运行时治理 · 运行前评估（G3 删/覆盖受保护数据）。
        # 沙箱内代码改动不命中受保护集合 → 自治边界满足 → 通常放行（needs_gate=False）。
        self._gov_config = load_config()
        pre_letter = self._governance_evaluate(
            ActionContext(
                action_type="data_delete",
                protected_collections=(),
                in_sandbox=True,
                in_path_whitelist=True,
                external=False,
                irreversible=False,
                estimated_tokens=0,
            ),
            decision_sink, issue_id, "G3-prerun", pending_sink=pending_sink,
        )
        # 本期顶层无 resume 编排：pending_sink 信号在 run() 内无法 resume →
        # fail-closed 取消（绝不静默误用、不继续执行动作）。
        if isinstance(pre_letter, PendingDecisionRaised):
            self._record_run_summary(issue_id, run_id, tenant_id, "cancelled", 0, 0.0, 0)
            return {
                "issue_id": issue_id,
                "status": "cancelled",
                "rounds": 0,
                "diff_text": "",
                "test_exit_code": None,
                "files": [],
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "audit_event_count": 0,
                "model_gateway_id": None,
                "model_name": None,
            }
        if pre_letter in ("C", "D"):
            # fail-closed 取消 → 中止运行（不进入后续写链路）。
            self._record_run_summary(issue_id, run_id, tenant_id, "cancelled", 0, 0.0, 0)
            return {
                "issue_id": issue_id,
                "status": "cancelled",
                "rounds": 0,
                "diff_text": "",
                "test_exit_code": None,
                "files": [],
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "audit_event_count": 0,
                "model_gateway_id": None,
                "model_name": None,
            }

        # 单主占锁（同 Issue 防重入）；无 database 时降级跳过。
        self._claim_once(
            tenant_id,
            run_id,
            claim_id=(f"{run_id}:{workflow_step_id}" if workflow_step_id else run_id),
            workflow_step_id=workflow_step_id,
        )

        # Issue A · 通用 Agent Execution Kernel 接线（default-off）。
        # 仅当 agent_kernel_enabled 为真时建立 wake→claim→session（单执行者
        # 保证 + 可恢复记录）。接线点位于 runtime_governance.evaluate()
        # 之后，不重评 gate、不绕过 b.governance.gate 决策链。
        kernel_ctx: dict[str, Any] | None = None
        if self.agent_kernel_enabled:
            kernel_ctx = self._kernel_begin(
                issue_id, run_id, tenant_id, task_id, target_files,
                instructions, test_command_argv, allow_paths, max_rounds,
            )

        try:
            read_tools, write_tools, git_tools = self._build_toolsets(
                tenant_id, project_id, task_id, run_id,
                target_files, test_command_id, test_command_argv, allow_paths,
                workflow_step_id=workflow_step_id,
            )
        except (ValueError, LocalRDToolError) as error:
            if kernel_ctx is not None:
                self._kernel_abort(kernel_ctx, "configuration_rejected")
            raise RealRDExecutorError(
                "configuration_rejected"
            ) from error

        # 累计统计（本地计数，与真实落库审计行解耦）。
        total_tokens = 0
        estimated_cost = 0.0
        audit_event_count = 0
        model_gateway_id: Any = None
        model_name: Any = None

        status = "failed"
        diff_text = ""
        test_exit_code: Any = None
        files: list[dict[str, str]] = []
        rounds = 0
        last_failure = ""

        for round_index in range(1, max_rounds + 1):
            rounds = round_index
            # Issue A · 每轮续接 + 心跳（default-off 时 kernel_ctx 为 None 跳过）。
            if kernel_ctx is not None:
                kernel_ctx = self._kernel_round_tick(kernel_ctx, rounds)
            rollback = None
            try:
                # 1) 读取每个目标文件并取 preimage 乐观锁哈希。
                preimages: dict[str, str] = {}
                contents: dict[str, str] = {}
                for target in target_files:
                    audit_event_count += 1
                    read_result = read_tools.read_file(json.dumps({"path": target}))
                    output = read_result["output"]
                    preimages[target] = output["sha256"]
                    contents[target] = self._lines_to_text(
                        output.get("lines", []), output.get("ends_with_newline", False)
                    )

                # 2) 构造 prompt。
                #    判断后端是否为 filesystem-mutating（agent 直接改磁盘）：
                #    - 是：用 agent prompt（不要求返回 diff，直接改目标文件）。
                #    - 否：保持原 unified-diff prompt 不变。
                is_agent = getattr(self.model, "mutates_filesystem", False)
                if is_agent:
                    prompt = self._build_agent_prompt(
                        instructions, target_files, last_failure
                    )
                else:
                    prompt = self._build_prompt(instructions, contents, last_failure)

                # 3) 真实调用模型网关（超时/限流/网络等瞬时错误视为可恢复，
                #    记录后进入下一轮重试；此时尚未 apply，无需回滚）。
                try:
                    response = self.model.execute(prompt)
                except Exception as model_error:
                    if workflow_run_id:
                        raise RealRDExecutorError(
                            "usage_evidence_invalid"
                        ) from model_error
                    last_failure = (
                        "model gateway error "
                        f"(status={getattr(model_error, 'status', 'unknown')})"
                    )
                    continue
                if workflow_run_id:
                    usage = self._validated_model_usage(response)
                    self._record_model_usage(
                        usage,
                        tenant_id=tenant_id,
                        project_id=project_id,
                        task_id=task_id,
                        workflow_run_id=workflow_run_id,
                        workflow_step_id=workflow_step_id,
                        round_index=round_index,
                    )
                total_tokens += int(response.get("total_tokens", 0) or 0)

                # B 层运行时治理 · G4 token 预算评估（累计 token 超硬限 → 弹闸）。
                token_letter = self._governance_evaluate(
                    ActionContext(action_type="token_spend", estimated_tokens=total_tokens),
                    decision_sink, issue_id, "G4-token", pending_sink=pending_sink,
                )
                # 顶层无 resume 编排：pending 信号 → fail-closed 取消（不静默误用）。
                if isinstance(token_letter, PendingDecisionRaised):
                    status = "cancelled"
                    self._record_run_summary(
                        issue_id, run_id, tenant_id, status, total_tokens, estimated_cost, rounds
                    )
                    if kernel_ctx is not None:
                        self._kernel_finish(kernel_ctx, "cancelled")
                    return {
                        "issue_id": issue_id,
                        "status": status,
                        "rounds": rounds,
                        "diff_text": "",
                        "test_exit_code": test_exit_code,
                        "files": files,
                        "total_tokens": total_tokens,
                        "estimated_cost": estimated_cost,
                        "audit_event_count": audit_event_count,
                        "model_gateway_id": model_gateway_id,
                        "model_name": model_name,
                    }
                if token_letter in ("C", "D"):
                    # fail-closed 取消 → 跳出循环，标记 cancelled 并脱敏返回。
                    status = "cancelled"
                    self._record_run_summary(
                        issue_id, run_id, tenant_id, status, total_tokens, estimated_cost, rounds
                    )
                    if kernel_ctx is not None:
                        self._kernel_finish(kernel_ctx, "cancelled")
                    return {
                        "issue_id": issue_id,
                        "status": status,
                        "rounds": rounds,
                        "diff_text": "",
                        "test_exit_code": test_exit_code,
                        "files": files,
                        "total_tokens": total_tokens,
                        "estimated_cost": estimated_cost,
                        "audit_event_count": audit_event_count,
                        "model_gateway_id": model_gateway_id,
                        "model_name": model_name,
                    }

                # Issue C · 内部预算硬停（default-off）。接线点置于
                # runtime_governance.evaluate()（G4-token）之后，与 B 层 G4
                # 用户询问闸并存不冲突：G4 问用户、本 Issue 自主停。超
                # hard_stop_ratio → BudgetGuard 抛脱敏
                # RealRDExecutorError("budget_exceeded")（由下方 except 分支处理）。
                if self.budget_guard_enabled:
                    budget_result = self._budget_guard.check(
                        total_tokens, agent_session_id=run_id
                    )
                    if budget_result.status == "warn":
                        # 软提醒：仅落脱敏 a.budget.warn，不阻断主流程。
                        self._record_budget_event(
                            "a.budget.warn",
                            {
                                "scope": budget_result.scope,
                                "status": "warn",
                                "ratio": budget_result.ratio,
                                "limit": budget_result.limit,
                            },
                            issue_id,
                        )

                estimated_cost += float(response.get("estimated_cost", 0) or 0)
                model_gateway_id = response.get("model_gateway_id", model_gateway_id)
                model_name = response.get("model_name", model_name)

                # 4) 解析 / 应用分支。
                if is_agent:
                    # agent 已在 workspace 内直接改了磁盘，无需 parse/apply diff。
                    # 记录 preimage 用于交付物；回滚改用 git checkout（见 _make_agent_rollback）。
                    parsed = ""
                    current_files = [
                        {
                            "path": t,
                            "preimage_hash": preimages.get(t, ""),
                            "postimage_hash": "",
                        }
                        for t in target_files
                    ]
                    rollback = self._make_agent_rollback(
                        target_files,
                        getattr(self.model, "cwd", None) or os.getcwd(),
                    )
                else:
                    # 解析模型输出为原始 unified diff（非法则视为本轮失败并重试）。
                    parsed = self._parse_diff(response.get("output", ""))

                    # 5) 事务化 apply_diff（乐观锁 + 可回滚）。
                    audit_event_count += 1
                    apply_result, rollback = write_tools._apply_diff_transactional(
                        json.dumps({"diff": parsed, "preimage_hashes": preimages})
                    )
                    current_files = [
                        {
                            "path": item["path"],
                            "preimage_hash": item["preimage_hash"],
                            "postimage_hash": item["postimage_hash"],
                        }
                        for item in apply_result.get("output", {}).get("files", [])
                    ]

                # 6) 跑测试；通过则成功跳出，否则回滚并进入下一轮。
                audit_event_count += 1
                test_exit_code, test_error = self._safe_run_test(
                    write_tools, test_command_id
                )
                if test_error is not None:
                    last_failure = f"test command failed (exit_code={test_exit_code})"
                    self._safe_rollback(rollback)
                    rollback = None
                    continue
                if test_exit_code == 0:
                    status = "succeeded"
                    files = current_files
                    break
                last_failure = f"test command failed (exit_code={test_exit_code})"
                self._safe_rollback(rollback)
                rollback = None

            except _RoundFailed:
                # 模型输出非法：仅本轮失败，无需回滚（尚未 apply）。
                if rollback is not None:
                    self._safe_rollback(rollback)
                    rollback = None
                last_failure = "model output was not a valid unified diff"
                continue
            except LocalRDToolError as error:
                # 工具拒绝：已 apply 则回滚；按错误类型分流。
                if rollback is not None:
                    self._safe_rollback(rollback)
                    rollback = None
                if error.failure_code == "command_failed":
                    # 测试失败：可重试，回滚后进入下一轮。
                    last_failure = (
                        f"test command failed (exit_code={getattr(error, 'exit_code', None)})"
                    )
                    continue
                if error.failure_code in _RETRYABLE_TOOL_ERRORS:
                    # diff 应用失败（上下文/preimage/格式）：尚未落盘或已回滚，
                    # 作为可恢复轮次重试，下一轮会重新读取文件并生成新 diff。
                    last_failure = f"diff application failed ({error.failure_code})"
                    continue
                # 其余（路径/敏感/配置/删除等结构性违规）一律视为致命，脱敏后抛出。
                if kernel_ctx is not None:
                    self._kernel_abort(kernel_ctx, "tool_rejected")
                raise RealRDExecutorError(
                    "tool_rejected"
                ) from error
            except RealRDExecutorError as error:
                if error.failure_code == "budget_exceeded":
                    # Issue C · 预算硬停：此时尚未 apply（rollback 为 None，安全空处理），
                    # 走既有 _safe_rollback + 落脱敏 a.budget.exceeded + 标准脱敏返回。
                    self._safe_rollback(rollback)
                    rollback = None
                    self._record_budget_event(
                        "a.budget.exceeded",
                        {
                            "scope": self._budget_guard._config.scope,
                            "status": "hard_stop",
                            "ratio": self._budget_guard._last_ratio,
                            "limit": self._budget_guard._config.max_tokens_per_run,
                        },
                        issue_id,
                    )
                    status = "budget_exceeded"
                    self._record_run_summary(
                        issue_id, run_id, tenant_id, status, total_tokens, estimated_cost, rounds
                    )
                    if kernel_ctx is not None:
                        self._kernel_finish(kernel_ctx, "budget_exceeded")
                    return {
                        "issue_id": issue_id,
                        "status": status,
                        "rounds": rounds,
                        "diff_text": "",
                        "test_exit_code": test_exit_code,
                        "files": files,
                        "total_tokens": total_tokens,
                        "estimated_cost": estimated_cost,
                        "audit_event_count": audit_event_count,
                        "model_gateway_id": model_gateway_id,
                        "model_name": model_name,
                    }
                raise
            except Exception as error:  # noqa: BLE001 - 兜底脱敏
                if rollback is not None:
                    self._safe_rollback(rollback)
                    rollback = None
                if kernel_ctx is not None:
                    self._kernel_abort(kernel_ctx, "unexpected_error")
                raise RealRDExecutorError(
                    "unexpected_error"
                ) from error

        # 成功分支：取真实 git diff 作为交付物；失败分支 diff_text 保持空。
        if status == "succeeded":
            try:
                audit_event_count += 1
                git_result = git_tools.git_read(json.dumps({"operation": "diff"}))
                diff_text = git_result["output"]["output"]
            except LocalRDToolError as error:
                if kernel_ctx is not None:
                    self._kernel_abort(kernel_ctx, "git_read_rejected")
                raise RealRDExecutorError(
                    "git_read_rejected"
                ) from error
            except Exception as error:  # noqa: BLE001
                if kernel_ctx is not None:
                    self._kernel_abort(kernel_ctx, "git_read_failed")
                raise RealRDExecutorError(
                    "git_read_failed"
                ) from error

        if kernel_ctx is not None:
            self._kernel_finish(kernel_ctx, status)
        self._record_run_summary(
            issue_id, run_id, tenant_id, status, total_tokens, estimated_cost, rounds
        )

        return {
            "issue_id": issue_id,
            "status": status,
            "rounds": rounds,
            "diff_text": diff_text,
            "test_exit_code": test_exit_code,
            "files": files,
            "total_tokens": total_tokens,
            "estimated_cost": estimated_cost,
            "audit_event_count": audit_event_count,
            "model_gateway_id": model_gateway_id,
            "model_name": model_name,
        }

    # ------------------------------------------------------------------ #
    # 单主占锁（借鉴 D1 _claim_once，无 database 时降级跳过）
    # ------------------------------------------------------------------ #
    def _claim_once(
        self,
        tenant_id: str,
        run_id: str,
        *,
        claim_id: str | None = None,
        workflow_step_id: str = "",
    ) -> None:
        database = getattr(self.event_log, "database", None)
        if database is None:
            return
        resolved_claim_id = claim_id or run_id
        try:
            with database.connect() as connection:
                connection.execute("begin immediate")
                existing = connection.execute(
                    "select 1 from evolution_events "
                    "where tenant_id=? and idempotency_key=? limit 1",
                    (tenant_id, f"{resolved_claim_id}:started"),
                ).fetchone()
                if existing is not None:
                    raise RealRDExecutorError(
                        "issue_already_running"
                    )
                connection.execute(
                    "insert into evolution_events "
                    "(correlation_id,event_type,payload,tenant_id,idempotency_key) "
                    "values (?,?,?,?,?)",
                    (
                        run_id,
                        REAL_RD_STARTED_EVENT,
                        json.dumps(
                            {
                                "run_id": run_id,
                                "workflow_run_id": run_id,
                                "workflow_step_id": workflow_step_id,
                                "tenant_id": tenant_id,
                                "outcome": "started",
                            }
                        ),
                        tenant_id,
                        f"{resolved_claim_id}:started",
                    ),
                )
        except RealRDExecutorError:
            raise
        except Exception as error:  # noqa: BLE001
            raise RealRDExecutorError(
                "lock_unavailable"
            ) from error

    # ------------------------------------------------------------------ #
    # 工具集构造
    # ------------------------------------------------------------------ #
    def _build_toolsets(
        self,
        tenant_id: str,
        project_id: str,
        task_id: str,
        run_id: str,
        target_files: list[str],
        test_command_id: str,
        test_command_argv: list[str],
        allow_paths: list[str],
        *,
        workflow_step_id: str = "",
    ) -> tuple[LocalRDToolset, LocalRDToolset, LocalRDToolset]:
        test_path = self._derive_test_path(test_command_argv)
        pytest_tuple = (*_PYTEST_COMMAND_PREFIX, test_path)
        read_scope = LocalRDToolScope(
            tenant_id, project_id, task_id, run_id, tuple(allow_paths), workflow_step_id
        )
        write_scope = LocalRDToolScope(
            tenant_id, project_id, task_id, run_id, tuple(allow_paths), workflow_step_id
        )
        git_scope = LocalRDToolScope(
            tenant_id, project_id, task_id, run_id, tuple(target_files), workflow_step_id
        )
        read_tools = self.toolset_cls(
            read_scope, self.event_log, sandbox_mode=self.sandbox_mode
        )
        write_tools = self.toolset_cls(
            write_scope,
            self.event_log,
            {test_command_id: pytest_tuple},
            sandbox_mode=self.sandbox_mode,
        )
        git_tools = self.toolset_cls(
            git_scope, self.event_log, sandbox_mode=self.sandbox_mode
        )
        return read_tools, write_tools, git_tools

    def _validate_persistent_scope(
        self,
        tenant_id: str,
        project_id: str,
        task_id: str,
        workflow_run_id: str,
        workflow_step_id: str,
        *,
        target_files: list[str],
        test_command_id: str,
        test_command_argv: list[str],
        allow_paths: list[str],
    ) -> None:
        database = getattr(self.event_log, "database", None)
        if database is None:
            raise RealRDExecutorError("usage_scope_invalid")
        try:
            with database.connect() as connection:
                rows = connection.execute(
                    """
                    select wr.task_id, wr.company_id, wr.project_id,
                           wr.created_from_template_id as run_source,
                           wr.department_id, wr.status as run_status,
                           ws.status as step_status,
                           ws.employee_role as step_employee_role,
                           t.tenant_id as task_tenant_id,
                           t.project_id as task_project_id,
                           t.company_id as task_company_id,
                           t.content as task_content,
                           sa.capability_binding_id,
                           sa.employee_id as assigned_employee_id,
                           sa.employee_role as assigned_employee_role,
                           sa.status as assignment_status,
                           ecb.tenant_id as binding_tenant_id,
                           ecb.employee_id as binding_employee_id,
                           ecb.capability_source,
                           ecb.capability_type,
                           ecb.capability_id,
                           ecb.enabled as binding_enabled,
                           ei.tenant_id as employee_tenant_id,
                           ei.company_id as employee_company_id,
                           ei.department_id as employee_department_id,
                           ei.role as employee_instance_role,
                           ei.status as employee_status,
                           ei.enabled as employee_enabled,
                           tools.type as tool_type,
                           tools.entry as tool_entry
                    from workflow_runs wr
                    join workflow_steps ws
                      on ws.tenant_id = wr.tenant_id
                     and ws.workflow_run_id = wr.workflow_run_id
                    left join tasks t on t.tenant_id = wr.tenant_id
                                     and t.task_id = wr.task_id
                    left join step_assignments sa
                      on sa.tenant_id = ws.tenant_id
                     and sa.workflow_step_id = ws.workflow_step_id
                    left join employee_capability_bindings ecb
                      on ecb.tenant_id = sa.tenant_id
                     and ecb.id = sa.capability_binding_id
                    left join employee_instances ei
                      on ei.tenant_id = ecb.tenant_id
                     and ei.id = ecb.employee_id
                    left join tools on tools.name = ecb.capability_id
                    where wr.tenant_id = ? and wr.workflow_run_id = ?
                      and ws.workflow_step_id = ?
                    """,
                    (tenant_id, workflow_run_id, workflow_step_id),
                ).fetchall()
                execution_count = connection.execute(
                    "select count(*) from executions where tenant_id = ? and task_id = ?",
                    (tenant_id, task_id),
                ).fetchone()[0]
                usage_count = connection.execute(
                    """
                    select count(*) from evolution_events
                    where tenant_id = ? and correlation_id = ?
                      and event_type in ('usage.model_call', 'usage.tool_call')
                    """,
                    (tenant_id, workflow_run_id),
                ).fetchone()[0]
                task_contents = connection.execute(
                    "select content from tasks where tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
        except Exception as error:  # noqa: BLE001
            raise RealRDExecutorError("usage_scope_invalid") from error

        if len(rows) != 1:
            raise RealRDExecutorError("usage_scope_invalid")
        row = rows[0]
        if (
            row["task_id"] != task_id
            or row["run_status"] != "running"
            or row["step_status"] != "running"
        ):
            raise RealRDExecutorError("usage_scope_invalid")

        if row["run_source"] != _EVIDENCE_RUN_SOURCE:
            return
        try:
            mapping = json.loads(row["task_content"])
        except (TypeError, json.JSONDecodeError) as error:
            raise RealRDExecutorError("fixture_scope_invalid") from error
        if not isinstance(mapping, dict) or mapping.get("schema") != _EVIDENCE_FIXTURE_SCHEMA:
            raise RealRDExecutorError("fixture_scope_invalid")

        if (
            row["project_id"] != project_id
            or row["task_tenant_id"] != tenant_id
            or row["task_project_id"] != project_id
            or row["task_company_id"] != row["company_id"]
            or row["assignment_status"] != "assigned"
            or row["binding_tenant_id"] != tenant_id
            or row["binding_employee_id"] != row["assigned_employee_id"]
            or row["binding_enabled"] != 1
            or row["capability_source"] != "official"
            or row["capability_type"] != "tool"
            or row["capability_id"] != _EVIDENCE_TOOL_ID
            or row["employee_tenant_id"] != tenant_id
            or row["employee_company_id"] != row["company_id"]
            or row["employee_department_id"] != row["department_id"]
            or row["employee_instance_role"] != row["step_employee_role"]
            or row["assigned_employee_role"] != row["step_employee_role"]
            or row["employee_enabled"] != 1
            or row["employee_status"] not in ("idle", "assigned", "active")
            or row["tool_type"] != "executor"
            or row["tool_entry"] != "real_rd_executor"
            or execution_count != 0
            or usage_count != 0
        ):
            raise RealRDExecutorError("usage_scope_invalid")
        if not isinstance(mapping, dict) or set(mapping) != _EVIDENCE_MAPPING_KEYS:
            raise RealRDExecutorError("fixture_scope_invalid")

        try:
            fixture_sha256 = _evidence_fixture_sha256()
        except (OSError, UnicodeError) as error:
            raise RealRDExecutorError("fixture_scope_invalid") from error
        expected_dynamic = {
            "schema": _EVIDENCE_FIXTURE_SCHEMA,
            "issue_id": _EVIDENCE_ISSUE_ID,
            "run_source": _EVIDENCE_RUN_SOURCE,
            "fixture_id": task_id,
            "fixture_sha256": fixture_sha256,
            "target_files": list(_EVIDENCE_TARGET_FILES),
            "test_command_id": _EVIDENCE_COMMAND_ID,
            "test_command_argv": list(_EVIDENCE_TEST_COMMAND_ARGV),
            "registered_argv": list(_EVIDENCE_REGISTERED_ARGV),
            "allow_paths": [*_EVIDENCE_TARGET_FILES, _EVIDENCE_TEST_FILE],
            "tenant_id": tenant_id,
            "company_id": row["company_id"],
            "department_id": row["department_id"],
            "project_id": project_id,
            "workflow_run_id": workflow_run_id,
            "workflow_step_id": workflow_step_id,
            "employee_id": row["assigned_employee_id"],
            "employee_role": row["step_employee_role"],
            "tool_binding_id": row["capability_binding_id"],
            "tool_capability_id": _EVIDENCE_TOOL_ID,
            "audit_fields": _EVIDENCE_AUDIT_FIELDS,
        }
        operation_id = mapping.get("operation_id")
        operation_id_valid = False
        if isinstance(operation_id, str) and operation_id.startswith("op-"):
            try:
                operation_id_valid = str(uuid.UUID(operation_id[3:])) == operation_id[3:]
            except ValueError:
                operation_id_valid = False
        if (
            not operation_id_valid
            or any(mapping.get(key) != value for key, value in expected_dynamic.items())
            or target_files != list(_EVIDENCE_TARGET_FILES)
            or test_command_id != _EVIDENCE_COMMAND_ID
            or test_command_argv != list(_EVIDENCE_TEST_COMMAND_ARGV)
            or allow_paths != [*_EVIDENCE_TARGET_FILES, _EVIDENCE_TEST_FILE]
        ):
            raise RealRDExecutorError("fixture_scope_invalid")

        matching_commands = 0
        for task_content in task_contents:
            try:
                candidate = json.loads(task_content["content"])
            except (TypeError, json.JSONDecodeError):
                continue
            if (
                isinstance(candidate, dict)
                and candidate.get("schema") == _EVIDENCE_FIXTURE_SCHEMA
                and candidate.get("test_command_id") == _EVIDENCE_COMMAND_ID
            ):
                matching_commands += 1
        if matching_commands != 1:
            raise RealRDExecutorError("fixture_scope_invalid")

    @staticmethod
    def _validated_model_usage(response: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(response, dict):
            raise RealRDExecutorError("usage_evidence_invalid")

        integer_fields = ("prompt_tokens", "completion_tokens", "total_tokens")
        price_fields = ("unit_price_input", "unit_price_output", "estimated_cost")
        text_fields = (
            "usage_record_id",
            "model_gateway_id",
            "model_name",
            "provider_id",
            "price_version",
            "currency",
            "cost_source",
        )
        if any(
            isinstance(response.get(key), bool)
            or not isinstance(response.get(key), int)
            or response[key] < 0
            for key in integer_fields
        ):
            raise RealRDExecutorError("usage_evidence_invalid")
        if (
            response["prompt_tokens"] <= 0
            or response["total_tokens"] <= 0
            or response["total_tokens"]
            != response["prompt_tokens"] + response["completion_tokens"]
        ):
            raise RealRDExecutorError("usage_evidence_invalid")
        if any(
            isinstance(response.get(key), bool)
            or not isinstance(response.get(key), (int, float))
            or not math.isfinite(float(response[key]))
            or float(response[key]) <= 0
            for key in price_fields
        ):
            raise RealRDExecutorError("usage_evidence_invalid")
        if any(
            not isinstance(response.get(key), str) or not response[key].strip()
            for key in text_fields
        ):
            raise RealRDExecutorError("usage_evidence_invalid")
        expected_cost = round(
            response["prompt_tokens"] * float(response["unit_price_input"])
            + response["completion_tokens"] * float(response["unit_price_output"]),
            8,
        )
        if (
            response.get("status") != "success"
            or response.get("outbound_attempted") is not True
            or not math.isclose(
                float(response["estimated_cost"]), expected_cost, rel_tol=0.0, abs_tol=1e-8
            )
        ):
            raise RealRDExecutorError("usage_evidence_invalid")
        return response

    def _record_model_usage(
        self,
        usage: dict[str, Any],
        *,
        tenant_id: str,
        project_id: str,
        task_id: str,
        workflow_run_id: str,
        workflow_step_id: str,
        round_index: int,
    ) -> None:
        payload = {
            "usage_record_id": usage["usage_record_id"],
            "run_id": workflow_run_id,
            "workflow_run_id": workflow_run_id,
            "workflow_step_id": workflow_step_id,
            "tenant_id": tenant_id,
            "project_id": project_id,
            "task_id": task_id,
            "status": "success",
            "outbound_attempted": True,
        }
        try:
            self.event_log.record(
                correlation_id=workflow_run_id,
                event_type="real_rd.model_call_linked",
                tenant_id=tenant_id,
                idempotency_key=(
                    f"{workflow_run_id}:{workflow_step_id}:model:{round_index}"
                ),
                payload=payload,
            )
        except Exception as error:  # noqa: BLE001
            raise RealRDExecutorError("usage_audit_failed") from error

    @staticmethod
    def _derive_test_path(test_command_argv: list[str]) -> str:
        if not test_command_argv:
            raise ValueError("test_command_argv is required")
        last = test_command_argv[-1]
        if not isinstance(last, str) or not last:
            raise ValueError("test_command_argv last element is invalid")
        if last.startswith("backend/"):
            return last
        return f"backend/{last.lstrip('/')}"

    # ------------------------------------------------------------------ #
    # prompt / diff 解析
    # ------------------------------------------------------------------ #
    @staticmethod
    def _build_prompt(
        instructions: str, contents: dict[str, str], last_failure: str
    ) -> str:
        parts = [instructions]
        for path, text in contents.items():
            # 给文件内容加行号前缀：LLM 生成精确 unified diff 的 `@@ -N,M @@`
            # 头高度依赖已知行号，否则极易猜错起始行导致上下文错位。
            numbered = "\n".join(
                f"{index:5d}: {line}" for index, line in enumerate(text.splitlines(), start=1)
            )
            parts.append(f"[FILE {path}]\n{numbered}")
        parts.append(
            "Return exactly one raw unified diff for the target file(s) above, "
            "beginning with '--- a/<path>' and '+++ b/<path>' and an '@@' hunk header. "
            "The '@@ -N,M +N,M @@' header must use the real line numbers shown above "
            "(the file content is prefixed with line numbers). Do not include the "
            "line-number prefixes inside the diff itself; output plain diff lines only. "
            "Do not wrap it in Markdown code fences and do not add any explanation."
        )
        if last_failure:
            parts.append(
                f"The previous attempt failed: {last_failure}. "
                "Correct it and return a new unified diff."
            )
        return "\n\n".join(parts)

    @staticmethod
    def _lines_to_text(lines: list[dict[str, Any]], ends_with_newline: bool) -> str:
        text = "\n".join(item.get("text", "") for item in lines)
        if ends_with_newline:
            text += "\n"
        return text

    @classmethod
    def _normalize_diff_counts(cls, diff: str) -> str:
        """归一模型产出 unified diff 的 hunk 行数计数。

        模型常把 old/new 行数（``@@ -N,M +N,M @@`` 中的 M）猜错，但起始行号
        （group(1) / group(3)）与 hunk body 内容基本正确。``_apply_hunks`` 只依赖
        ``old_start`` 定位并按 body 逐行匹配 context 来应用；``@@`` 计数仅用于末尾
        一次 ``consumed != old_count`` 校验。因此把计数重算为 body 真实长度即可让
        校验通过，且**不改变**任何实际增删的行，语义安全。

        规则：
        - 逐行扫描；命中 ``_HUNK_RE`` 的行视为 hunk 头，重算并重写。
        - 该 hunk 的 body = 头行之后、直到下一个以 ``"@@ "`` 或 ``"--- "`` 开头的
          行（不含）为止。
        - body 中每行：以 ``"\\ No newline at end of file"`` 开头则跳过计数；
          否则取 ``marker = line[0]``，``marker in {" ", "-"}`` 计入 old、
          ``marker in {" ", "+"}`` 计入 new。
        - 非 hunk 行原样保留。
        """
        lines = diff.splitlines(keepends=True)
        out: list[str] = []
        total = len(lines)
        index = 0
        while index < total:
            line = lines[index]
            match = cls._HUNK_RE.match(line)
            if not match:
                out.append(line)
                index += 1
                continue
            old_start = int(match.group(1))
            new_start = int(match.group(3))
            consumed = 0
            produced = 0
            body_index = index + 1
            while body_index < total:
                body_line = lines[body_index]
                if body_line.startswith("@@ ") or body_line.startswith("--- "):
                    break
                if body_line.startswith("\\ No newline at end of file"):
                    body_index += 1
                    continue
                if not body_line:
                    # 空行（通常为 diff 尾部无换行）不参与计数，但保留。
                    body_index += 1
                    continue
                marker = body_line[0]
                if marker in (" ", "-"):
                    consumed += 1
                if marker in (" ", "+"):
                    produced += 1
                body_index += 1
            out.append(f"@@ -{old_start},{consumed} +{new_start},{produced} @@\n")
            index += 1
        return "".join(out)

    @classmethod
    def _parse_diff(cls, text: str) -> str:
        """将模型输出解析为原始 unified diff（保留 diff 自身的换行）。

        仅剥离可选的 ```diff 围栏与收尾 ```，并裁剪首个 ``--- a/`` 之前的
        引导性说明文字；**不**对 diff 主体做 ``.strip()``，以免丢失文件尾换行导致
        落盘文件被错误截断。

        校验至少含 ``@@`` 或 ``--- a/`` + ``+++ b/``；非法则抛
        ``_RoundFailed``（视为本轮失败、回滚后重试）。
        """
        if not isinstance(text, str) or not text.strip():
            raise _RoundFailed("model output was empty")
        cleaned = text
        # 裁剪首个 diff 头（``--- a/``）之前的引导性文字（如模型附带的说明）。
        header = cleaned.find("--- a/")
        if header > 0:
            cleaned = cleaned[header:]
        # 裁剪收尾的 ``` 围栏（及其后的说明文字，如「Hope this helps!」）。
        fence_end = cleaned.find("```")
        if fence_end >= 0:
            cleaned = cleaned[:fence_end]
        # 归一 hunk 行数计数：模型起始行号正确但常数错 body 行数，导致
        # local_rd_toolset 末尾 ``consumed != old_count`` 校验失败。此处把
        # ``@@`` 计数重算为 body 真实长度，使校验通过且不影响语义。
        cleaned = cls._normalize_diff_counts(cleaned)
        has_hunk = "@@" in cleaned
        has_headers = ("--- a/" in cleaned) and ("+++ b/" in cleaned)
        if not (has_hunk or has_headers):
            raise _RoundFailed("model output was not a unified diff")
        return cleaned

    # ------------------------------------------------------------------ #
    # filesystem-mutating agent 专用分支
    # ------------------------------------------------------------------ #
    @staticmethod
    def _build_agent_prompt(
        instructions: str, target_files: list[str], last_failure: str
    ) -> str:
        """构造 filesystem-mutating agent 的 prompt。

        与 ``_build_prompt`` 不同，这里**不**注入文件内容/行号、也**不**要求
        返回 unified diff；而是告知 agent 拥有 workspace 写权限，应直接修改
        目标文件完成任务。
        """
        lines = [
            "You have write access to the workspace. Directly modify the "
            "following file(s) on disk to complete the task. Do NOT return a "
            "unified diff or any patch text; just change the files in place.",
            f"Task:\n{instructions}",
            "Target files:",
        ]
        for path in target_files:
            lines.append(f"- {path}")
        if last_failure:
            lines.append(
                f"The previous attempt failed: {last_failure}. "
                "Correct it by editing the files directly."
            )
        return "\n\n".join(lines)

    @staticmethod
    def _make_agent_rollback(
        target_files: list[str], cwd: str
    ) -> Callable[[], None]:
        """返回 agent 模式下的回滚闭包。

        agent 已在磁盘直接改文件，失败时无法用 diff 逆应用，只能
        ``git checkout -- <target_files>`` 把工作区还原到 HEAD。异常静默吞掉
        （与 ``_safe_rollback`` 风格一致）。
        """
        def _rollback() -> None:
            try:
                subprocess.run(
                    ["git", "checkout", "--", *target_files],
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
            except Exception:  # noqa: BLE001
                pass
        return _rollback

    # ------------------------------------------------------------------ #
    # 测试执行（安全包装，区分致命与可重试失败）
    # ------------------------------------------------------------------ #
    @staticmethod
    def _safe_run_test(
        write_tools: LocalRDToolset, test_command_id: str
    ) -> tuple[Any, Any]:
        """执行注册测试，返回 (exit_code, error)。

        - 成功：``(exit_code, None)``。
        - 测试失败（``command_failed``，带 ``exit_code``）：``(exit_code, error)``，
          调用方应回滚并进入下一轮重试。
        - 其它工具错误：``(None, error)``。
        """
        try:
            result = write_tools.run_test(json.dumps({"command_id": test_command_id}))
            return result["output"]["exit_code"], None
        except LocalRDToolError as error:
            if getattr(error, "exit_code", None) is not None:
                return error.exit_code, error
            return None, error

    @staticmethod
    def _safe_rollback(rollback: Any) -> None:
        if rollback is None:
            return
        try:
            rollback()
        except Exception:  # noqa: BLE001 - 回滚失败不影响脱敏抛出
            pass

    # ------------------------------------------------------------------ #
    # Issue A · 通用 Agent Execution Kernel 接线助手（default-off）
    # ------------------------------------------------------------------ #
    def _kernel_begin(
        self,
        issue_id: str,
        run_id: str,
        tenant_id: str,
        task_id: str,
        target_files: list[str],
        instructions: str,
        test_command_argv: list[str],
        allow_paths: list[str],
        max_rounds: int,
    ) -> "dict[str, Any] | None":
        """建立 wake→claim→session（单执行者保证 + 可恢复记录）。

        失败则降级跳过（fail-open：绝不阻断主流程）。返回 kernel 上下文
        dict（含 store / claim / wake / session / token / owner / scope /
        fingerprint / finished 标记），供后续 tick / finish / abort 复用。
        """
        database = getattr(self.event_log, "database", None)
        if database is None:
            return None
        try:
            run_config = RunConfig(
                model_gateway_id=str(getattr(self.model, "model_gateway_id", "") or ""),
                model_name=str(getattr(self.model, "model_name", "") or ""),
                tool_scope={
                    "sandbox_mode": str(self.sandbox_mode or ""),
                    "allow_paths": list(allow_paths),
                },
                prompt_spec={
                    "instructions": instructions,
                    "target_files": list(target_files),
                    "test_command_id": str(self._derive_test_path(test_command_argv)),
                },
                strategy={
                    "max_rounds": int(max_rounds),
                    "test_command_argv": list(test_command_argv),
                },
                component_versions={},
                extra={},
            )
            fingerprint = compute_fingerprint(run_config)
            scope = f"{tenant_id}:{run_id}"
            owner = f"real-rd:{tenant_id}:{run_id}"
            token = uuid.uuid4().hex
            idempotency_key = build_idempotency_key(scope, task_id, fingerprint)
            claim_store = ExecutionClaimStore(database)
            wake_store = WakeRequestStore(database)
            session_store = AgentTaskSessionStore(database)
            wake = wake_store.create(
                scope,
                "real-rd-executor",
                task_id,
                idempotency_key=idempotency_key,
                payload={"issue_id": issue_id},
                config_fingerprint=fingerprint,
                tenant_id=tenant_id,
                correlation_id=issue_id,
            )
            claim = claim_store.acquire(
                scope,
                owner,
                "real_rd.run",
                token=token,
                tenant_id=tenant_id,
                correlation_id=issue_id,
            )
            session_id = uuid.uuid4().hex
            session = session_store.create(
                scope,
                "real-rd-executor",
                task_id,
                config_fingerprint=fingerprint,
                execution_claim_id=claim.claim_id,
                wake_request_id=wake.request_id,
                owner=owner,
                checkpoint={},
                tenant_id=tenant_id,
                correlation_id=issue_id,
                session_id=session_id,
            )
            wake_store.claim(wake.request_id, session_id)
            session_store.start(session_id, owner)
        except Exception:  # noqa: BLE001 - 内核建立失败 → 降级跳过
            return None
        self._record_kernel_event(
            "a.kernel.wake.created",
            {"scope": scope, "fingerprint": fingerprint, "status": "created"},
            issue_id,
        )
        self._record_kernel_event(
            "a.kernel.claim.acquired",
            {"scope": scope, "status": "held"},
            issue_id,
        )
        self._record_kernel_event(
            "a.kernel.session.started",
            {"scope": scope, "status": "running", "fingerprint": fingerprint},
            issue_id,
        )
        return {
            "claim_store": claim_store,
            "wake_store": wake_store,
            "session_store": session_store,
            "claim": claim,
            "wake": wake,
            "session": session,
            "token": token,
            "owner": owner,
            "scope": scope,
            "fingerprint": fingerprint,
            "finished": False,
        }

    def _kernel_round_tick(self, kernel_ctx: "dict[str, Any]", rounds: int) -> "dict[str, Any]":
        """每轮续接 + 心跳（脱敏，失败静默）。"""
        if kernel_ctx is None or kernel_ctx.get("finished"):
            return kernel_ctx
        try:
            session = kernel_ctx["session"]
            kernel_ctx["session_store"].checkpoint(
                session.session_id,
                kernel_ctx["owner"],
                {"round": rounds, "status": "running"},
            )
            kernel_ctx["claim_store"].heartbeat(
                kernel_ctx["claim"].claim_id, kernel_ctx["token"]
            )
            self._record_kernel_event(
                "a.kernel.session.checkpoint",
                {"scope": kernel_ctx["scope"], "round": rounds},
                session.correlation_id or kernel_ctx["scope"],
            )
        except Exception:  # noqa: BLE001 - tick 失败不影响主流程
            pass
        return kernel_ctx

    def _kernel_finish(self, kernel_ctx: "dict[str, Any]", status: str) -> None:
        """收尾：complete session + release claim + complete wake（幂等、脱敏）。"""
        if kernel_ctx is None or kernel_ctx.get("finished"):
            return
        kernel_ctx["finished"] = True
        outcome = (
            "completed"
            if status == "succeeded"
            else ("cancelled" if status == "cancelled" else "failed")
        )
        error_code = "" if outcome == "completed" else "run_not_completed"
        correlation_id = kernel_ctx["session"].correlation_id or kernel_ctx["scope"]
        try:
            kernel_ctx["session_store"].complete(
                kernel_ctx["session"].session_id,
                kernel_ctx["owner"],
                outcome=outcome,
                error_code=error_code,
            )
            kernel_ctx["claim_store"].release(
                kernel_ctx["claim"].claim_id, kernel_ctx["token"]
            )
            kernel_ctx["wake_store"].complete(
                kernel_ctx["wake"].request_id, outcome=outcome
            )
            self._record_kernel_event(
                "a.kernel.session.completed",
                {
                    "scope": kernel_ctx["scope"],
                    "status": outcome,
                    "error_code": error_code,
                },
                correlation_id,
            )
            self._record_kernel_event(
                "a.kernel.claim.released",
                {"scope": kernel_ctx["scope"], "status": "released"},
                kernel_ctx["scope"],
            )
            self._record_kernel_event(
                "a.kernel.wake.completed",
                {"scope": kernel_ctx["scope"], "status": outcome},
                kernel_ctx["scope"],
            )
        except Exception:  # noqa: BLE001 - 收尾失败不影响脱敏返回
            pass

    def _kernel_abort(self, kernel_ctx: "dict[str, Any]", error_code: str) -> None:
        """异常中止：complete session(failed) + 释放 claim + 完成 wake（幂等）。"""
        if kernel_ctx is None or kernel_ctx.get("finished"):
            return
        kernel_ctx["finished"] = True
        try:
            kernel_ctx["session_store"].complete(
                kernel_ctx["session"].session_id,
                kernel_ctx["owner"],
                outcome="failed",
                error_code=error_code,
            )
            try:
                kernel_ctx["claim_store"].release(
                    kernel_ctx["claim"].claim_id, kernel_ctx["token"]
                )
            except Exception:  # noqa: BLE001 - 释放失败则强释放清孤儿
                try:
                    kernel_ctx["claim_store"].force_release(
                        kernel_ctx["claim"].claim_id
                    )
                except Exception:  # noqa: BLE001
                    pass
            kernel_ctx["wake_store"].complete(
                kernel_ctx["wake"].request_id, outcome="failed"
            )
        except Exception:  # noqa: BLE001
            pass

    def _record_kernel_event(
        self, event_type: str, payload: dict[str, Any], correlation_id: str
    ) -> None:
        """落 ``a.kernel.*`` 事件（脱敏：仅 scope / status / 指纹 / 范围键）。"""
        try:
            self.event_log.record(
                correlation_id=correlation_id or "",
                event_type=event_type,
                payload=payload,
                tenant_id=None,  # 由 EvolutionEventLog 自行解析 selfuse
                idempotency_key=f"{correlation_id}:{event_type}:{uuid.uuid4().hex[:8]}",
            )
        except Exception:  # noqa: BLE001 - 内核事件为尽力而为，绝不影响主流程
            pass

    def _record_budget_event(
        self, event_type: str, payload: dict[str, Any], correlation_id: str
    ) -> None:
        """落 ``a.budget.*`` 事件（脱敏：仅 scope / status / ratio / limit / 范围键）。

        与 ``_record_kernel_event`` 同构，仅事件前缀不同；与 ``b.governance.gate``
        并列独立追加写、不混。best-effort，绝不影响主流程。
        """
        try:
            self.event_log.record(
                correlation_id=correlation_id or "",
                event_type=event_type,
                payload=payload,
                tenant_id=None,  # 由 EvolutionEventLog 自行解析 selfuse
                idempotency_key=f"{correlation_id}:{event_type}:{uuid.uuid4().hex[:8]}",
            )
        except Exception:  # noqa: BLE001 - 预算事件为尽力而为，绝不影响主流程
            pass

    # ------------------------------------------------------------------ #
    # 汇总事件（脱敏，不含 diff 文本 / 路径 / 密钥）
    # ------------------------------------------------------------------ #
    def _record_run_summary(
        self,
        issue_id: str,
        run_id: str,
        tenant_id: str,
        status: str,
        total_tokens: int,
        estimated_cost: float,
        rounds: int,
    ) -> None:
        event_type = REAL_RD_SUMMARY_OK if status == "succeeded" else REAL_RD_SUMMARY_FAIL
        payload = {
            "run_id": run_id,
            "issue_id": issue_id,
            "status": status,
            "rounds": rounds,
            "total_tokens": total_tokens,
            "estimated_cost": estimated_cost,
        }
        try:
            self.event_log.record(
                correlation_id=run_id,
                event_type=event_type,
                payload=payload,
                tenant_id=tenant_id,
                idempotency_key=f"{run_id}:{issue_id}:summary",
            )
        except Exception:  # noqa: BLE001 - 汇总为尽力而为，绝不影响返回脱敏
            pass

    # ------------------------------------------------------------------ #
    # 规格校验
    # ------------------------------------------------------------------ #
    # ------------------------------------------------------------------ #
    # B 层运行时治理 · 决策评估与事件落点（脱敏，不含路径/Key/参数）
    # ------------------------------------------------------------------ #
    def _governance_evaluate(
        self,
        action_context: "ActionContext",
        decision_sink: Any,
        correlation_id: str,
        gate_label: str,
        *,
        pending_sink: Any = None,
    ) -> "str | PendingDecisionRaised":
        """B 层闸评估：返回决策字母 A/B/C/D，或 ``PendingDecisionRaised`` 信号。

        派发优先级（默认 ``pending_sink=None``、``decision_sink=None`` → fail-closed C）：
        ① 自治边界满足 → ``"A"``（放行，不落事件）；
        ② ``pending_sink`` 注入且需弹闸 → 持久化 + 记录 ``pending`` + 返
           ``PendingDecisionRaised``（动作未执行，等 resolver 回填后 resume，属未来编排层）；
        ③ 既有 ``decision_sink`` 注入 → 取字母并按中心映射落 outcome；
        ④ 默认（无 sink）→ fail-closed 默认 ``"C"``（取消），落 ``b.governance.gate=cancelled``。

        评估异常 → fail-closed 默认 ``"C"``，并落 ``b.governance.gate=cancelled``。
        """
        try:
            decision = evaluate(action_context, self._gov_config)
        except Exception:
            self._record_governance_gate(None, "evaluation_error", correlation_id, gate_label)
            return "C"
        if not decision.needs_gate:
            return "A"
        if pending_sink is not None:
            # 真实等用户拍板（非阻塞）：写入存储即返回 pending_id 信号。
            pending_id = pending_sink.ask(
                decision.gate,
                correlation_id=correlation_id,
                gate_label=gate_label,
            )
            self._record_governance_gate(decision, "pending", correlation_id, gate_label)
            return PendingDecisionRaised(
                pending_id=pending_id,
                gate_label=gate_label,
                gate_id=getattr(decision.gate, "gate_id", ""),
            )
        if decision_sink is None:
            # 无 sink → fail-closed 默认取消（循环不卡、闸不漏）。
            self._record_governance_gate(decision, "cancelled", correlation_id, gate_label)
            return "C"
        letter = decision_sink.ask(decision.gate)
        # 统一经中心映射（③）：B→simulated，A→allowed，C→cancelled，D→alternative。
        outcome = outcome_for_letter(letter)
        self._record_governance_gate(decision, outcome, correlation_id, gate_label)
        return letter

    def _record_governance_gate(
        self, decision: Any, outcome: str, correlation_id: str, gate_label: str
    ) -> None:
        """落 ``b.governance.gate`` 事件（脱敏：无路径 / Key / 参数）。"""
        try:
            self.event_log.record(
                correlation_id=correlation_id,
                event_type="b.governance.gate",
                payload={
                    "gate_label": gate_label,
                    "category": getattr(decision, "category", None),
                    "outcome": outcome,
                    "needs_gate": bool(getattr(decision, "needs_gate", True)),
                },
                tenant_id=None,  # 由 EvolutionEventLog 自行解析 selfuse
                idempotency_key=f"{correlation_id}:b-gov:{gate_label}:{outcome}",
            )
        except Exception:  # noqa: BLE001 - 治理事件为尽力而为，绝不影响主流程
            pass

    @staticmethod
    def _validate_spec(issue_spec: dict[str, Any]) -> None:
        if not isinstance(issue_spec, dict):
            raise RealRDExecutorError("spec_invalid")
        required = (
            "issue_id",
            "target_files",
            "test_command_id",
            "test_command_argv",
            "instructions",
            "allow_paths",
        )
        missing = [key for key in required if key not in issue_spec]
        if missing:
            raise RealRDExecutorError("spec_invalid")
        if not isinstance(issue_spec["target_files"], (list, tuple)) or not issue_spec["target_files"]:
            raise RealRDExecutorError("spec_invalid")
        if not isinstance(issue_spec["allow_paths"], (list, tuple)) or not issue_spec["allow_paths"]:
            raise RealRDExecutorError("spec_invalid")


__all__ = ["RealRDExecutor", "RealRDExecutorError"]
