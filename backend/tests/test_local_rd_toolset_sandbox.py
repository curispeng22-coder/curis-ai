"""LocalRDToolset.run_test 的 sandbox 网络隔离三分支单元测试。

通过 fakes_rd.FakeLocalToolset 覆写 ``_run_process`` 捕获实际 argv，并配合
monkeypatch ``local_rd_toolset.Path("/usr/bin/sandbox-exec").is_file()`` 的存在性，
覆盖以下分支：
1. AUTO + sandbox 存在    → 走 sandbox（argv 含 sandbox-exec）。
2. OFF                    → 直跑（argv 不含 sandbox-exec）。
3. ENFORCE + sandbox 缺失 → 抛 sandbox_unavailable（fail-closed）。
4. AUTO + sandbox 缺失    → 直跑且审计字段 sandbox_degraded=True。
"""
from __future__ import annotations

import json
import pathlib
import sys
from pathlib import Path
from typing import Any

import pytest

# 使同目录的 fakes_rd 可导入（与既有测试一致的 sys.path 注入方式）。
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import local_rd_toolset  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.local_rd_toolset import LocalRDToolError, SandboxMode  # noqa: E402

import fakes_rd  # noqa: E402


# ---------------------------------------------------------------------------
# Path 替身：仅对 /usr/bin/sandbox-exec 的 is_file() 返回受控结果。
# 其余路径原样转发给真实 pathlib.Path。
# ---------------------------------------------------------------------------
class _ControlledPath:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._inner = pathlib.Path(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def __str__(self) -> str:
        return str(self._inner)

    def __fspath__(self) -> str:
        return self._inner.__fspath__()

    def is_file(self) -> bool:
        if str(self._inner) == "/usr/bin/sandbox-exec":
            return type(self)._sandbox_present
        return self._inner.is_file()

    _sandbox_present = True


def _set_sandbox_present(present: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    _ControlledPath._sandbox_present = present
    monkeypatch.setattr(local_rd_toolset, "Path", _ControlledPath)


class TestRunTestSandbox:
    def test_auto_with_sandbox_runs_under_sandbox(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_sandbox_present(True, monkeypatch)
        tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.AUTO)
        result = tools.run_test(json.dumps({"command_id": "rd_verify"}))
        assert result["status"] == "succeeded"
        argv = tools.captured_argv[-1]
        assert argv[0] == "/usr/bin/sandbox-exec"
        assert argv[1] == "-p"
        assert "deny network*" in argv[2]
        # 走 sandbox 时不应标记降级。
        degraded = [
            e["payload"].get("sandbox_degraded")
            for e in tools.event_log.get_all()
            if e["payload"].get("tool_id") == "tl_ai_rd_test_runner"
        ]
        assert True not in degraded

    def test_off_runs_directly(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # 即便 sandbox 存在，OFF 也直跑。
        _set_sandbox_present(True, monkeypatch)
        tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.OFF)
        result = tools.run_test(json.dumps({"command_id": "rd_verify"}))
        assert result["status"] == "succeeded"
        argv = tools.captured_argv[-1]
        assert "/usr/bin/sandbox-exec" not in argv
        assert argv == fakes_rd.FAKE_COMMAND_REGISTRY["rd_verify"]
        assert tools.captured_use_sandbox[-1] is False

    def test_enforce_without_sandbox_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_sandbox_present(False, monkeypatch)
        tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.ENFORCE)
        with pytest.raises(LocalRDToolError) as ctx:
            tools.run_test(json.dumps({"command_id": "rd_verify"}))
        assert ctx.value.failure_code == "sandbox_unavailable"

    def test_auto_without_sandbox_degrades(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_sandbox_present(False, monkeypatch)
        tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.AUTO)
        result = tools.run_test(json.dumps({"command_id": "rd_verify"}))
        assert result["status"] == "succeeded"
        argv = tools.captured_argv[-1]
        assert "/usr/bin/sandbox-exec" not in argv
        # 审计字段 sandbox_degraded=True（AUTO + 缺失）。
        degraded = [
            e["payload"].get("sandbox_degraded")
            for e in tools.event_log.get_all()
            if e["payload"].get("tool_id") == "tl_ai_rd_test_runner"
        ]
        assert True in degraded

    def test_unregistered_command_rejected_before_sandbox_check(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # command_not_registered 必须先于 sandbox 检查（fail-closed 不变）。
        _set_sandbox_present(False, monkeypatch)
        tools = fakes_rd.make_fake_local_toolset(sandbox_mode=SandboxMode.ENFORCE)
        with pytest.raises(LocalRDToolError) as ctx:
            tools.run_test(json.dumps({"command_id": "not-registered"}))
        assert ctx.value.failure_code == "command_not_registered"
        # 未注册命令不应触达 _run_process（sandbox 检查之前即拒绝）。
        assert tools.captured_argv == []


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
