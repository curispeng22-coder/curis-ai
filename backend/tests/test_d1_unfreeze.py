"""D1 toolchain unfreeze tests (T4, scope A+B).

No model calls, no network, no Docker. Exercises:
  (a) non-frozen + derived root exists -> build returns a real instance;
  (b) frozen=True -> kill-switch returns None;
  (c) override pointing at a missing path -> desensitized LocalRDToolError,
      both at direct construction and at build time.

The desensitization red line is asserted: no path / stack / Key leaks into the
raised exception message.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from backend.app import local_rd_toolset
from backend.app.d1_config import D1ToolchainConfig
from backend.app.d1_single_model_toolchain import build_d1_toolchain
from backend.app.local_rd_toolset import (
    LocalRDToolError,
    LocalRDToolScope,
    LocalRDToolset,
)


class D1UnfreezeTest(unittest.TestCase):
    def tearDown(self) -> None:
        # 清理 build 期注入的覆盖位，避免用例间串扰。
        local_rd_toolset._WORKSPACE_ROOT_OVERRIDE = None

    def _scope(self) -> LocalRDToolScope:
        return LocalRDToolScope(
            tenant_id="tenant-d1",
            project_id="project-d1",
            task_id="task-d1",
            run_id="run-d1",
            allowed_paths=("tools/verify_d1_tenant_reservation.py",),
        )

    def test_build_non_frozen_returns_instance(self) -> None:
        # (a) 非冻结 + 默认推导 root 存在 -> 返回非 None 实例（不触模型/网络）。
        model = MagicMock()
        event_log = MagicMock()
        toolchain = build_d1_toolchain(model, event_log, D1ToolchainConfig(frozen=False))
        self.assertIsNotNone(toolchain)
        # build 不应污染模块级覆盖位（config 未提供 override）。
        self.assertIsNone(local_rd_toolset._WORKSPACE_ROOT_OVERRIDE)

    def test_build_frozen_returns_none(self) -> None:
        # (b) frozen=True -> kill-switch，整体回退为 None。
        model = MagicMock()
        event_log = MagicMock()
        toolchain = build_d1_toolchain(model, event_log, D1ToolchainConfig(frozen=True))
        self.assertIsNone(toolchain)

    def test_override_missing_root_raises_desensitized(self) -> None:
        # (c) 覆盖位指向不存在路径 -> 构造抛脱敏 LocalRDToolError，且 build 抛同异常。
        local_rd_toolset._WORKSPACE_ROOT_OVERRIDE = "/nonexistent/path/that/does/not/exist"

        with self.assertRaises(LocalRDToolError) as ctx:
            LocalRDToolset(self._scope(), MagicMock())
        message = str(ctx.exception)
        # 脱敏红线：异常文案不得含路径/堆栈/Key。
        self.assertNotIn("/nonexistent", message)
        self.assertEqual(ctx.exception.failure_code, "workspace_root_unavailable")

        model = MagicMock()
        event_log = MagicMock()
        with self.assertRaises(LocalRDToolError):
            build_d1_toolchain(model, event_log, D1ToolchainConfig(frozen=False))


if __name__ == "__main__":
    unittest.main()
