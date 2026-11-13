"""真实研发闭环 hardening 测试替身与共享夹具。

提供：
- ``make_fake_event_log`` ：构造临时 sqlite + EvolutionEventLog（含 evolution_events
  表），供本地工具测试真实走完审计路径。
- ``make_fake_local_toolset`` ：构造仅含受验测试命令的 ``FakeLocalToolset``。
- ``FakeLocalToolset`` ：``LocalRDToolset`` 的测试替身，覆写 ``_run_process`` 以捕获
  实际传给 subprocess 的 argv（含是否带 sandbox-exec 前缀），不触碰真实文件系统 /
  sandbox-exec，使 run_test 的 sandbox 三分支可被断言。

用法（见 test_local_rd_toolset_sandbox.py）：
    tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.OFF)
    tools.run_test(json.dumps({"command_id": "rd_verify"}))
    assert "/usr/bin/sandbox-exec" not in tools.captured_argv[-1]
"""
from __future__ import annotations

import os
import tempfile
from typing import Any

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import (
    LocalRDToolScope,
    LocalRDToolset,
    SandboxMode,
)


def make_fake_event_log() -> EvolutionEventLog:
    """创建临时 sqlite + EvolutionEventLog（含 evolution_events 表）。"""
    tmp_dir = tempfile.mkdtemp(prefix="real-rd-fake-")
    db_path = os.path.join(tmp_dir, "evo.sqlite")
    db = Database(db_path)
    with db.connect() as conn:
        conn.execute(
            """
            create table if not exists evolution_events (
                event_id integer primary key autoincrement,
                correlation_id text not null,
                event_type text not null,
                payload text not null,
                tenant_id text,
                idempotency_key text,
                created_at text not null default current_timestamp
            )
            """
        )
    return EvolutionEventLog(db)


# 与 LocalRDToolset._validate_command_registry 对齐的受验测试命令。
_FAKE_TEST_PATH = "backend/tests/test_real_rd_verify.py"
FAKE_COMMAND_REGISTRY: dict[str, tuple[str, ...]] = {
    "rd_verify": ("backend/.venv/bin/python", "-m", "pytest", "-q", _FAKE_TEST_PATH),
}


def make_fake_local_toolset(
    sandbox_mode: SandboxMode | str | None = None,
) -> "FakeLocalToolset":
    """构造一个仅含受验测试命令的 FakeLocalToolset（run_test 可用）。"""
    scope = LocalRDToolScope(
        tenant_id="fake-tenant",
        project_id="fake-project",
        task_id="fake-task",
        run_id="real-rd:fake",
        allowed_paths=(_FAKE_TEST_PATH,),
    )
    return FakeLocalToolset(
        scope, make_fake_event_log(), FAKE_COMMAND_REGISTRY, sandbox_mode=sandbox_mode
    )


class FakeLocalToolset(LocalRDToolset):
    """LocalRDToolset 替身：捕获 ``_run_process`` 的 argv，模拟成功执行。

    不触发真实 sandbox-exec / 真实文件 I/O；``_run_process`` 返回 ``(rc=0, b"", b"")``，
    使 run_test 走完 "注册命令成功" 分支，从而断言 argv 是否含 sandbox-exec 前缀、
    以及审计字段 ``sandbox_degraded``。
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.captured_argv: list[tuple[str, ...]] = []
        self.captured_use_sandbox: list[bool] = []

    def _run_process(
        self, command: tuple[str, ...], temp_dir: str, use_sandbox: bool = True
    ) -> tuple[int, bytes, bytes]:
        self.captured_argv.append(tuple(command))
        self.captured_use_sandbox.append(use_sandbox)
        # 不触碰真实 sandbox / 文件系统：模拟注册命令执行成功（rc=0，无输出）。
        return (0, b"", b"")
