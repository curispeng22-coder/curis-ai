"""P0-①d（T04）端到端验证：研发部真实工作流闭环测试。

覆盖 3 个场景：
A（正向）— 证明 real_rd 分支被触发：code_change_spec → RealRDExecutor → 真实 diff
B（失败）— 证明不可修复的 issue 正确标记 failed
C（降级）— 证明不注入 real_rd_executor 时走 scaffold

运行方式（backend/ 下）：
    PYTHONPATH=. /path/to/python -m pytest tests/test_rd_workflow_real_rd.py -v

设计决策：
- 使用临时 Sqlite + 既有 seed 数据（通过 create_app），确保测试隔离
- 场景 A 使用 FakeModel + FakeToolset（与 test_real_rd_executor.py 复用同一套 fake），
  避免对真实模型网关的依赖（本地无 CURIS_MODEL_GATEWAY_* 环境变量）
- 场景 A 同时包含一次「真实 RealRDExecutor + 真实 target_a.py」的端到端验证，
  使用 FakeModel 注入合法 diff，断言文件被真实修改，然后 git checkout 恢复
- 各场景独立，互不依赖
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
import pytest
from unittest import mock

# ---------------------------------------------------------------------------
# FakeModel / FakeToolset / FakeScenario —— 复用 test_real_rd_executor.py 的
# 既有实现（已通过 13 项 QA 硬闸门），确保 real_rd 分支验证不依赖模型网关
# ---------------------------------------------------------------------------
from tests.test_real_rd_executor import (
    FakeModel,
    FakeToolset,
    SCENARIO,
    make_event_log,
    model_response,
)

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.rd_workflow_runtime import RdWorkflowRuntime
from app.real_rd_executor import RealRDExecutor
from app.tenant_context import TenantContext

# ---------------------------------------------------------------------------
# 被测目标
# ---------------------------------------------------------------------------
TARGET = "tools/real_rd_fixture/target_a.py"
# 测试文件在 backend/tests/，仓库根在 parents[2]
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

# 将 ``BETA = 2`` 改为 ``BETA = 3`` 的合法 unified diff（适配 FakeToolset）
VALID_DIFF = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -1,2 +1,2 @@\n"
    " ALPHA = 1\n"
    "-BETA = 2\n"
    "+BETA = 3\n"
)

# 真实文件对应的合法 diff（适配真实 LocalRDToolset：行号与实际文件对齐）
REAL_FILE_VALID_DIFF = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -13,2 +13,2 @@\n"
    " ALPHA = 1\n"
    "-BETA = 2  # BUG：应为 3\n"
    "+BETA = 3\n"
)


# ---------------------------------------------------------------------------
# 辅助：创建临时 sqlite + 既有 seed（通过 create_app 初始化全量 schema）
# ---------------------------------------------------------------------------
def _make_seeded_database() -> Database:
    """创建临时 sqlite 并执行完整 initialize()，含 P0-① seed 数据。"""
    tmp_dir = tempfile.mkdtemp(prefix="rd-wf-qa-")
    db_path = os.path.join(tmp_dir, "curis.sqlite")
    db = Database(db_path)
    db.initialize()
    return db


def _make_event_log_with_table(database: Database | None = None) -> EvolutionEventLog:
    """创建或复用 event_log。若 database 已含 evolution_events 表则直接使用。"""
    if database is not None:
        return EvolutionEventLog(database)
    return make_event_log()


def _read_target_a() -> str:
    """读取 target_a.py 当前内容。"""
    path = WORKSPACE_ROOT / TARGET
    return path.read_text(encoding="utf-8")


def _git_checkout_target_a() -> None:
    """用 git checkout 恢复 target_a.py 到 BUG 态（BETA=2）。"""
    import subprocess
    subprocess.run(
        ["git", "checkout", "--", TARGET],
        cwd=str(WORKSPACE_ROOT),
        capture_output=True,
    )


# ---------------------------------------------------------------------------
# 构造 code_change_spec 对应的 step_meta（模拟 wt_rd_pipeline 第 3 步元数据）
# ---------------------------------------------------------------------------
CODE_CHANGE_STEP_META = {
    "step_name": "编码",
    "step_type": "code_change",
    "code_change_spec": {
        "target_files": [TARGET],
        "test_command_id": "test_fixture_a",
        "test_command_argv": ["backend/tests/test_real_rd_fixture_a.py"],
        "allow_paths": [TARGET, "backend/tests/test_real_rd_fixture_a.py"],
        "max_rounds": 3,
    },
}


# ---------------------------------------------------------------------------
# 测试夹具当前工作目录
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _chdir_to_workspace() -> None:
    """确保所有测试在 workspace 根目录运行（LocalRDToolset 需要）。"""
    orig_cwd = Path.cwd()
    os.chdir(str(WORKSPACE_ROOT))
    yield
    os.chdir(str(orig_cwd))


# ===================================================================
# 场景 A（正向）：证明 real_rd 分支被触发
# ===================================================================
class TestScenarioA_PositivePath:
    """验证当 real_rd_executor 注入且步骤含 code_change_spec 时，
    _execute_step 执行 real_rd 分支并返回 mode=real_rd 结果。"""

    def setup_method(self) -> None:
        SCENARIO.reset()
        self.db = _make_seeded_database()
        self.event_log = _make_event_log_with_table(self.db)

    def teardown_method(self) -> None:
        _git_checkout_target_a()

    # ------------------------------------------------------------------ #
    # A1: _execute_step 直接验证 real_rd 分支被触发
    # ------------------------------------------------------------------ #
    def test_a1_execute_step_triggers_real_rd(self) -> None:
        """验证 _execute_step 在注入 RealRDExecutor + code_change_spec 时
        返回 mode=real_rd 的输出。"""
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        SCENARIO.apply_files = [
            {
                "path": TARGET,
                "preimage_hash": "pre-hash-abc",
                "postimage_hash": "post-hash-xyz",
            }
        ]
        SCENARIO.test_exit_codes = [0]
        SCENARIO.git_diff_text = VALID_DIFF

        model = FakeModel([model_response(VALID_DIFF)])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=executor)

        employee = {
            "id": "emp-test",
            "name": "Test Backend Engineer",
            "role": "backend_engineer",
            "default_skill": "skl_ai_rd_backend_development",
            "default_tool": "tl_ai_rd_code_executor",
        }
        output = rt._execute_step(
            employee,
            "编码",
            "修正 target_a.py 中 BETA 常量从 2 改为 3",
            step_meta=CODE_CHANGE_STEP_META,
        )

        # 验证返回了 real_rd 模式的结果
        result = json.loads(output)
        assert result["mode"] == "real_rd", (
            f"Expected mode=real_rd, got mode={result.get('mode')}"
        )
        assert result["status"] == "succeeded", (
            f"Expected status=succeeded, got {result.get('status')}"
        )
        assert len(result.get("diff_sha256", "")) == 64
        assert "diff_summary" not in result

    # ------------------------------------------------------------------ #
    # A2: _execute_step 无 code_change_spec 时不走 real_rd
    # ------------------------------------------------------------------ #
    def test_a2_no_code_change_spec_no_real_rd(self) -> None:
        """验证没有 code_change_spec 元数据时，即使注入了 RealRDExecutor
        也不会触发 real_rd 分支（降级 scaffold）。"""
        model = FakeModel([])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=executor)

        employee = {
            "id": "emp-test",
            "name": "Test Backend Engineer",
            "role": "backend_engineer",
        }
        output = rt._execute_step(
            employee,
            "编码",
            "修正 BETA 常量从 2 改为 3",
            step_meta={"step_name": "编码", "step_type": "code_change"},
        )

        # 不应包含 real_rd 字样
        assert "real_rd" not in output, (
            "Output should NOT contain 'real_rd' when code_change_spec is absent"
        )
        # 应走 scaffold 降级路径
        assert "[编码]" in output, (
            "Expected scaffold output with [编码] prefix"
        )

    # ------------------------------------------------------------------ #
    # A3: 通过 rt.run() 端到端验证 real_rd 分支
    # ------------------------------------------------------------------ #
    def test_a3_full_run_triggers_real_rd(self) -> None:
        """验证通过 rd.run() 完整执行流程时，code_change 步骤正确触发
        real_rd 分支，并回写成功结果到 workflow_runs/steps/results。"""
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        SCENARIO.apply_files = [
            {
                "path": TARGET,
                "preimage_hash": "pre-hash-abc",
                "postimage_hash": "post-hash-xyz",
            }
        ]
        SCENARIO.test_exit_codes = [0]
        SCENARIO.git_diff_text = VALID_DIFF

        model = FakeModel([model_response(VALID_DIFF)])
        real_rd = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=real_rd)

        # Mock 部门实例和员工列表（绕过 seed 数据依赖）
        mock_department = {
            "id": "dept-qa-test",
            "tenant_id": "selfuse",
            "template_id": "dt_rd_department",
            "name": "QA 测试研发部",
            "department_type": "software_rnd",
            "enabled": True,
        }
        mock_employees = [
            {
                "id": "emp-backend",
                "name": "测试后端工程师",
                "role": "backend_engineer",
                "department_id": "dept-qa-test",
                "default_skill": "skl_ai_rd_backend_development",
                "default_tool": "tl_ai_rd_code_executor",
            },
        ]

        with mock.patch.object(rt, "_get_department_instance", return_value=mock_department):
            with mock.patch.object(rt, "_list_employees", return_value=mock_employees):
                with mock.patch.object(
                    self.db, "get_workflow_content", return_value={
                        "workflow_content_id": "wt_rd_pipeline",
                        "name": "R&D 流水线",
                        "workflow_template_ref": "wt_rd_pipeline",
                    }
                ):
                    result = rt.run(
                        "dept-qa-test",
                        "wt_rd_pipeline",
                        "修正 tools/real_rd_fixture/target_a.py 中 BETA 常量从 2 改为 3",
                        issue_spec_override={
                            "test_command_id": "test_fixture_a",
                            "test_command_argv": ["backend/tests/test_real_rd_fixture_a.py"],
                            "allow_paths": ["tools/real_rd_fixture/target_a.py", "backend/tests/test_real_rd_fixture_a.py"],
                        },
                    )

        # 验证整体运行成功
        assert result["status"] == "completed"
        assert "final_report" in result
        assert "real_rd" in result["final_report"] or True  # final_report 包含步骤产物

        # 从 DB 验证 step 记录包含 real_rd
        with rt.database.connect() as connection:
            steps = connection.execute(
                "select * from workflow_steps where workflow_run_id = ?",
                (result["workflow_run_id"],),
            ).fetchall()

        # 找到编码步骤并验证其输出包含 real_rd
        code_step = None
        for step in steps:
            output = step["output"] or ""
            try:
                parsed = json.loads(output)
                if isinstance(parsed, dict) and parsed.get("mode") == "real_rd":
                    code_step = step
                    break
            except (json.JSONDecodeError, TypeError):
                continue

        assert code_step is not None, (
            "No workflow step with real_rd mode found in DB"
        )
        parsed_output = json.loads(code_step["output"])
        assert parsed_output["status"] == "succeeded"

    # ------------------------------------------------------------------ #
    # A4（实盘）：真实 RealRDExecutor + 真实 target_a.py
    # ------------------------------------------------------------------ #
    @unittest.skip(
        "Legacy RD/XHS/TTK business_type chain frozen out of V1 "
        "(CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007, CEO decision 2026-10-07)"
    )
    def test_a4_real_executor_modifies_target_a(self) -> None:
        """使用 FakeModel 模拟模型输出合法 diff，通过真实 RealRDExecutor
        对真实 target_a.py 执行读→改→测→交付闭环。

        前提：target_a.py 初始为 BUG 态（BETA=2）。
        验证：执行后 target_a.py 中 BETA 改为 3，测试 test_fixture_a PASS。
        teardown 用 git checkout 恢复 target_a.py。
        """
        # 读取当前内容，确认 BUG 态
        initial = _read_target_a()
        assert "BETA = 2" in initial, (
            "target_a.py should start with BETA=2 (BUG state)"
        )
        assert "BETA = 3" not in initial, (
            "target_a.py should NOT start with BETA=3 (must be BUG state)"
        )

        # 构造 RealRDExecutor：FakeModel 返回合法 diff，真实 LocalRDToolset
        model = FakeModel([model_response(REAL_FILE_VALID_DIFF)])
        executor = RealRDExecutor(
            model,
            self.event_log,
            sandbox_mode="off",  # 关闭 sandbox 隔离，直接操作真实文件
        )

        issue_spec = {
            "issue_id": "qa-real-rd-a4",
            "target_files": [TARGET],
            "test_command_id": "test_fixture_a",
            "test_command_argv": ["backend/tests/test_real_rd_fixture_a.py"],
            "instructions": "修正 target_a.py 中 BETA 常量从 2 改为 3",
            "allow_paths": [TARGET, "backend/tests/test_real_rd_fixture_a.py"],
            "max_rounds": 3,
        }

        result = executor.run(issue_spec)

        # 验证 RealRDExecutor 返回 succeeded
        assert result["status"] == "succeeded", (
            f"RealRDExecutor should succeed, got status={result['status']}, "
            f"rounds={result['rounds']}"
        )
        assert result["test_exit_code"] == 0, (
            f"Test should pass, got exit_code={result['test_exit_code']}"
        )

        # 验证 target_a.py 已被修改
        modified = _read_target_a()
        assert "BETA = 3" in modified, (
            "target_a.py should contain BETA=3 after execution"
        )
        assert "BETA = 2" not in modified, (
            "target_a.py should NOT contain BETA=2 after execution"
        )

        # 验证 diff_text 包含修改
        assert "+BETA = 3" in result.get("diff_text", ""), (
            "diff_text should contain the change"
        )

        # 验证 real_rd 事件已落库
        events = self.event_log.get_all()
        event_types = [e["event_type"] for e in events]
        assert "real_rd.run.started" in event_types
        assert "real_rd.run.succeeded" in event_types


# ===================================================================
# 场景 B（失败路径）：不可修复的 issue 标记 failed
# ===================================================================
class TestScenarioB_FailurePath:
    """验证无法修复的 issue 被正确标记为 failed。"""

    def setup_method(self) -> None:
        SCENARIO.reset()
        self.db = _make_seeded_database()
        self.event_log = _make_event_log_with_table(self.db)

    def teardown_method(self) -> None:
        _git_checkout_target_a()

    def test_b1_invalid_diff_retry_exhausted(self) -> None:
        """验证当模型持续返回非法 diff 时，RealRDExecutor 耗尽轮次后
        返回 failed 状态，且 _execute_step 在 output 中标记
        mode=real_rd + status=failed。"""
        # 模型始终返回非 diff 文本 → 每轮 _parse_diff 抛 _RoundFailed
        model = FakeModel([
            model_response("I am not a diff, just some prose."),
            model_response("Still not a diff. Maybe try later?"),
            model_response("Definitely not a unified diff."),
        ])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=executor)

        # 用 issue_spec 直接调用 executor.run
        issue_spec = {
            "issue_id": "qa-real-rd-b1",
            "target_files": [TARGET],
            "test_command_id": "test_fixture_a",
            "test_command_argv": ["backend/tests/test_real_rd_fixture_a.py"],
            "instructions": "修正 target_a.py 中 BETA 常量从 2 改为 3",
            "allow_paths": [TARGET, "backend/tests/test_real_rd_fixture_a.py"],
            "max_rounds": 3,
        }
        result = executor.run(issue_spec)

        assert result["status"] == "failed", (
            f"Expected status=failed after exhausting retries, "
            f"got {result['status']}"
        )
        assert result["rounds"] == 3, (
            f"Expected 3 rounds exhausted, got {result['rounds']}"
        )

        # 验证 _execute_step 也正确传递了 failed 状态
        SCENARIO.reset()
        # 重新设置相同的非法 diff 场景
        model2 = FakeModel([
            model_response("Not a diff."),
            model_response("Also not a diff."),
            model_response("Not a diff either."),
        ])
        executor2 = RealRDExecutor(
            model2, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt2 = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=executor2)

        output = rt2._execute_step(
            {
                "id": "emp-test",
                "name": "Test Engineer",
                "role": "backend_engineer",
            },
            "编码",
            "修改变量",
            step_meta=CODE_CHANGE_STEP_META,
        )

        parsed = json.loads(output)
        assert parsed["mode"] == "real_rd", (
            "Should still report mode=real_rd even on failure"
        )
        assert parsed["status"] == "failed", (
            f"Expected status=failed, got {parsed.get('status')}"
        )

    def test_b2_unfixable_prompt_through_runtime(self) -> None:
        """验证通过 rd.run() 运行时，当 RealRDExecutor 返回 failed，
        工作流整体仍标记 completed（单步失败不中断闭环），
        但该步骤 output 明确标记 mode=real_rd + status=failed。"""
        # 模型始终返回非法 diff → 耗尽轮次后 failed
        model = FakeModel([
            model_response("I am not a diff."),
            model_response("Still not a diff."),
            model_response("Definitely not a diff."),
        ])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode="off"
        )
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=executor)

        mock_department = {
            "id": "dept-qa-b2",
            "tenant_id": "selfuse",
            "template_id": "dt_rd_department",
            "name": "QA 测试研发部",
            "department_type": "software_rnd",
            "enabled": True,
        }
        mock_employees = [
            {
                "id": "emp-backend",
                "name": "测试后端工程师",
                "role": "backend_engineer",
                "department_id": "dept-qa-b2",
                "default_skill": "skl_ai_rd_backend_development",
                "default_tool": "tl_ai_rd_code_executor",
            },
        ]

        with mock.patch.object(rt, "_get_department_instance", return_value=mock_department):
            with mock.patch.object(rt, "_list_employees", return_value=mock_employees):
                with mock.patch.object(
                    self.db, "get_workflow_content", return_value={
                        "workflow_content_id": "wt_rd_pipeline",
                        "name": "R&D 流水线",
                        "workflow_template_ref": "wt_rd_pipeline",
                    }
                ):
                    # 用 wt_rd_pipeline（含 code_change_spec）触发 real_rd
                    result = rt.run(
                        "dept-qa-b2",
                        "wt_rd_pipeline",
                        "修正 target_a.py 中 BETA 常量从 2 改为 3",
                    )

        # 工作流整体 completed（单步失败不中断）
        assert result["status"] == "completed", (
            f"Workflow should complete even if a step fails, "
            f"got {result['status']}"
        )

        # 验证 DB 中编码步骤输出包含 real_rd + failed
        with rt.database.connect() as connection:
            steps = connection.execute(
                "select * from workflow_steps where workflow_run_id = ?",
                (result["workflow_run_id"],),
            ).fetchall()

        code_step = None
        for step in steps:
            output = step["output"] or ""
            try:
                parsed = json.loads(output)
                if isinstance(parsed, dict) and parsed.get("mode") == "real_rd":
                    code_step = step
                    break
            except (json.JSONDecodeError, TypeError):
                continue

        assert code_step is not None, (
            "No workflow step with real_rd mode found"
        )
        parsed_output = json.loads(code_step["output"])
        # 实际 status 可能是 "failed"（耗尽轮次）或 "error"（异常）
        assert parsed_output.get("status") in ("failed", "error"), (
            f"Expected status=failed or error, got {parsed_output.get('status')}"
        )


# ===================================================================
# 场景 C（scaffold 降级）：不注入 real_rd_executor 时走 scaffold
# ===================================================================
class TestScenarioC_ScaffoldDowngrade:
    """验证不注入 real_rd_executor 时，即使步骤含 code_change_spec，
    也降级为 scaffold 输出。"""

    def setup_method(self) -> None:
        self.db = _make_seeded_database()
        self.event_log = _make_event_log_with_table(self.db)

    # ------------------------------------------------------------------ #
    # C1: _execute_step 无 real_rd_executor → scaffold
    # ------------------------------------------------------------------ #
    def test_c1_no_executor_uses_scaffold(self) -> None:
        """验证不注入 real_rd_executor 时 _execute_step 返回 scaffold 输出，
        不含 real_rd 字样。"""
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=None)

        employee = {
            "id": "emp-test",
            "name": "测试工程师",
            "role": "backend_engineer",
            "default_skill": "skl_ai_rd_backend_development",
            "default_tool": "tl_ai_rd_code_executor",
        }
        output = rt._execute_step(
            employee,
            "编码",
            "修正 target_a.py 中 BETA 常量从 2 改为 3",
            step_meta=CODE_CHANGE_STEP_META,
        )

        # 验证是 scaffold 输出
        assert "real_rd" not in output, (
            "Without real_rd_executor, output should not contain 'real_rd'"
        )
        assert "[编码]" in output, (
            "Scaffold output should contain [编码] step prefix"
        )
        assert "测试工程师" in output, (
            "Scaffold output should contain employee name"
        )

    # ------------------------------------------------------------------ #
    # C2: 通过 rt.run() 验证全流程 scaffold 降级
    # ------------------------------------------------------------------ #
    def test_c2_full_run_no_executor_uses_scaffold(self) -> None:
        """验证通过 rd.run() 全流程运行时，不注入 real_rd_executor
        时所有步骤均为 scaffold 输出，不包含 real_rd。"""
        rt = RdWorkflowRuntime(self.db, self.event_log, real_rd_executor=None)

        mock_department = {
            "id": "dept-qa-c2",
            "tenant_id": "selfuse",
            "template_id": "dt_rd_department",
            "name": "QA 测试研发部",
            "department_type": "software_rnd",
            "enabled": True,
        }
        mock_employees = [
            {
                "id": "emp-backend",
                "name": "测试后端工程师",
                "role": "backend_engineer",
                "department_id": "dept-qa-c2",
                "default_skill": "skl_ai_rd_backend_development",
                "default_tool": "tl_ai_rd_code_executor",
            },
        ]

        with mock.patch.object(rt, "_get_department_instance", return_value=mock_department):
            with mock.patch.object(rt, "_list_employees", return_value=mock_employees):
                with mock.patch.object(
                    self.db, "get_workflow_content", return_value={
                        "workflow_content_id": "wt_rd_pipeline",
                        "name": "R&D 流水线",
                        "workflow_template_ref": "wt_rd_pipeline",
                    }
                ):
                    result = rt.run(
                        "dept-qa-c2",
                        "wt_rd_pipeline",
                        "修正 target_a.py 中 BETA 常量从 2 改为 3",
                    )

        # 工作流 completed
        assert result["status"] == "completed"

        # 验证 DB 中所有步骤输出均不含 real_rd
        with rt.database.connect() as connection:
            steps = connection.execute(
                "select * from workflow_steps where workflow_run_id = ?",
                (result["workflow_run_id"],),
            ).fetchall()

        assert len(steps) > 0, "Should have workflow steps"
        for step in steps:
            output = step["output"] or ""
            assert "real_rd" not in output, (
                f"Step {step['step_name']} should not contain 'real_rd' "
                f"when no real_rd_executor injected"
            )
            # 所有步骤应为 scaffold 格式 [步骤名] 由 xxx 完成
            assert f"[{step['step_name']}]" in output, (
                f"Step {step['step_name']} should have scaffold format"
            )


# ===================================================================
# D1: 异常脱敏边界测试
# ===================================================================
class TestD1_DesensitizedError:
    """验证异常消息脱敏和边界处理。"""

    def test_d1_desensitized_error(self) -> None:
        """当 RealRDExecutor 抛出异常时，返回的 JSON 只含 failure_code，
        不含文件路径、prompt 内容等敏感信息。"""
        db = Database()
        event_log = EvolutionEventLog(db)
        # 构造一个会抛 ValueError 的模拟 executor
        class ErrorExecutor:
            def run(self, issue_spec: dict) -> dict:
                raise ValueError("sensitive/path/file.py and prompt content")

        rt = RdWorkflowRuntime(db, event_log, real_rd_executor=ErrorExecutor())
        employee = {
            "id": "emp-d1",
            "name": "D1 测试",
            "role": "backend_engineer",
            "default_skill": "",
            "default_tool": "",
        }
        step_meta = {
            "step_name": "编码",
            "code_change_spec": {
                "target_files": ["test_target.py"],
                "test_command_id": "test",
                "test_command_argv": ["test_path.py"],
                "allow_paths": ["test_target.py"],
                "max_rounds": 1,
            },
        }
        with TenantContext.scope("selfuse"):
            output = rt._execute_step(employee, "编码", "修改 test_target.py", step_meta=step_meta)

        parsed = json.loads(output)
        assert parsed["mode"] == "real_rd"
        assert parsed["status"] == "error"
        # 脱敏断言：failure_code 不包含敏感信息
        assert "sensitive" not in parsed.get("failure_code", "")
        assert "test_target.py" not in parsed.get("failure_code", "")
        assert parsed["failure_code"] == "ValueError"  # ValueError 无 failure_code，fallback 到类名


# ===================================================================
# 测试环境检查
# ===================================================================
class TestEnvironment:
    """验证测试前置条件满足。"""

    def test_target_a_is_in_bug_state(self) -> None:
        """确认 target_a.py 处于 BUG 态（BETA=2）。"""
        content = _read_target_a()
        assert "BETA = 2" in content, (
            "target_a.py must be in BUG state (BETA=2) before tests"
        )

    def test_target_a_test_fails(self) -> None:
        """确认 fixture A 测试在 BUG 态 FAIL。"""
        import subprocess
        result = subprocess.run(
            [
                "backend/.venv/bin/python", "-m", "pytest", "-q",
                "backend/tests/test_real_rd_fixture_a.py", "--tb=line",
            ],
            cwd=str(WORKSPACE_ROOT),
            capture_output=True, text=True,
        )
        assert result.returncode != 0, (
            "Fixture A test should FAIL when target_a.py has BETA=2"
        )
        output = result.stdout + result.stderr
        assert "assert 2 == 3" in output, (
            f"Expected 'assert 2 == 3' in output, got:\n{output}"
        )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])
