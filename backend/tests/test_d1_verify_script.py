"""Regression shell for the ADR-0017 D1 tenant_id reservation verify script.

This does NOT re-test backend logic (see ``test_d1_tenant.py`` for that). It
invokes ``tools/verify_d1_tenant_reservation.py`` as a real subprocess — using
the same interpreter that runs these tests — and asserts the script's
end-to-end contract so the verification is locked into CI:

  * process exit code is 0 (PASS),
  * stdout contains the ``PASS: ADR-0017 D1 tenant_id 预留验证通过`` line,
  * the trailing JSON's ``checks`` array contains all 7 expected invariants.

This is a read-only check: the script uses a temporary SQLite database and the
subprocess leaves no artifacts behind. No ``app/`` business code is modified and
D2 (department multi-tenancy) is intentionally NOT implemented here.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

# backend/tests/test_d1_verify_script.py -> repo root is parents[2].
_REPO_ROOT = Path(__file__).resolve().parents[2]
_VERIFY_SCRIPT = _REPO_ROOT / "tools" / "verify_d1_tenant_reservation.py"

_EXPECTED_CHECKS = (
    "preexisting_row_backfilled",
    "department_not_implemented",
    "tasks_has_tenant_id_column",
    "evolution_events_has_tenant_id_column",
    "new_row_default_tenant",
    "context_tenant_aware",
    "scope_set_and_restore",
)


class D1VerifyScriptRegressionTest(unittest.TestCase):
    def _run_script(self) -> subprocess.CompletedProcess[str]:
        self.assertTrue(
            _VERIFY_SCRIPT.exists(),
            f"verify script not found at {_VERIFY_SCRIPT}",
        )
        # Use the same interpreter running pytest so backend deps resolve.
        return subprocess.run(
            [sys.executable, str(_VERIFY_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(_REPO_ROOT),
        )

    def test_script_exits_zero(self):
        result = self._run_script()
        self.assertEqual(
            result.returncode,
            0,
            f"verify script exited {result.returncode}; "
            f"stdout={result.stdout!r} stderr={result.stderr!r}",
        )

    def test_script_prints_pass_line(self):
        result = self._run_script()
        self.assertIn(
            "PASS: ADR-0017 D1 tenant_id 预留验证通过",
            result.stdout,
            f"PASS line missing from stdout; stderr={result.stderr!r}",
        )

    def test_script_reports_seven_checks(self):
        result = self._run_script()
        report = None
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    report = json.loads(line)
                except json.JSONDecodeError:
                    continue
        self.assertIsNotNone(report, f"no JSON report line in stdout: {result.stdout!r}")
        checks = report.get("checks", [])
        self.assertEqual(
            len(checks),
            len(_EXPECTED_CHECKS),
            f"expected {len(_EXPECTED_CHECKS)} checks, got {checks!r}",
        )
        for expected in _EXPECTED_CHECKS:
            self.assertIn(
                expected,
                checks,
                f"missing expected check {expected!r} in {checks!r}",
            )


if __name__ == "__main__":
    unittest.main()
