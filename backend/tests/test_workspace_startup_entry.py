from __future__ import annotations

from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from backend.app import workspace_startup


ROOT = Path(__file__).resolve().parents[2]


class WorkspaceStartupEntryTest(unittest.TestCase):
    def _run_failure(self, error: BaseException) -> tuple[int, dict[str, str]]:
        output = io.StringIO()
        with patch.object(workspace_startup, "_load_workspace_app", side_effect=error), redirect_stderr(output):
            result = workspace_startup.main()
        return result, json.loads(output.getvalue())

    def test_import_failure_uses_existing_fixed_mapping(self):
        result, signal = self._run_failure(ImportError("must not escape"))
        self.assertEqual(result, 1)
        self.assertEqual(
            signal,
            {
                "failed_stage": "module_import",
                "failure_signal": "import_exception",
                "failure_code": "import_failed",
            },
        )

    def test_unknown_is_strictly_single_field(self):
        result, signal = self._run_failure(RuntimeError("must not escape"))
        self.assertEqual(result, 1)
        self.assertEqual(signal, {"failure_code": "unknown"})

    def test_existing_main_signal_is_not_duplicated(self):
        output = io.StringIO()
        with patch.object(workspace_startup, "_load_workspace_app", side_effect=SystemExit(1)), redirect_stderr(output):
            with self.assertRaisesRegex(SystemExit, "1"):
                workspace_startup.main()
        self.assertEqual(output.getvalue(), "")

    def test_uvicorn_start_failure_is_unknown_without_original_text(self):
        class FailedUvicorn:
            @staticmethod
            def run(*args, **kwargs):
                raise RuntimeError("must not escape")

        output = io.StringIO()
        with patch.object(workspace_startup, "_load_workspace_app", return_value=(FailedUvicorn, object())), redirect_stderr(output):
            self.assertEqual(workspace_startup.main(), 1)
        self.assertEqual(json.loads(output.getvalue()), {"failure_code": "unknown"})

    def test_workspace_entry_remains_after_legacy_admin_entry_removal(self):
        dockerfile = (ROOT / "deploy/curis/gateway/Dockerfile.workspace").read_text(encoding="utf-8")
        start_local = (ROOT / "deploy/curis/start-local.sh").read_text(encoding="utf-8")
        compose = (ROOT / "deploy/curis/gateway/docker-compose.yml").read_text(encoding="utf-8")
        workspace = (ROOT / "deploy/curis/run-workspace-backend.sh").read_text(encoding="utf-8")
        self.assertIn('CMD ["python", "-m", "backend.app.workspace_startup"]', dockerfile)
        self.assertIn("uvicorn backend.app.main:app", workspace)
        self.assertFalse((ROOT / "deploy/curis/run-admin-backend.sh").exists())
        self.assertIn('[ "$workspace_db" = "$sentinel_data/sentinel.sqlite" ]', start_local)
        for name in (
            "CURIS_MODEL_GATEWAY_PROFILE",
            "CURIS_MODEL_GATEWAY_BASE_URL",
            "CURIS_MODEL_GATEWAY_API_KEY",
            "CURIS_MODEL_GATEWAY_ID",
            "CURIS_MODEL_GATEWAY_MODEL",
        ):
            self.assertIn(f"{name}: ${{{name}:-}}", compose)


if __name__ == "__main__":
    unittest.main()
