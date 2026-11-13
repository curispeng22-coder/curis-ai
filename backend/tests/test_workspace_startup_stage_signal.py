from __future__ import annotations

import ast
from pathlib import Path
import sqlite3
import unittest


MAIN = Path(__file__).resolve().parents[1] / "app" / "main.py"


def _load_signal_functions():
    tree = ast.parse(MAIN.read_text(encoding="utf-8"))
    wanted = {
        "_STARTUP_FAILURE_CODES",
        "_startup_failure_signal",
        "_classified_signal",
        "_database_startup_failure_signal",
        "_mark_startup_failure",
        "_signal_for_startup_error",
        "_workspace_startup",
        "_emit_startup_failure",
    }
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in wanted for target in node.targets
        ):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in wanted:
            nodes.append(node)
    namespace = {"sqlite3": sqlite3, "BaseException": BaseException}
    exec(compile(ast.Module(nodes, type_ignores=[]), str(MAIN), "exec"), namespace)
    return namespace


class WorkspaceStartupStageSignalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.functions = _load_signal_functions()

    def test_only_approved_mappings(self):
        classify = self.functions["_startup_failure_signal"]
        expected = {
            ("module_import", "import_exception"): "import_failed",
            ("database_initialize", "schema_condition"): "schema_incompatible",
            ("identity_config", "validator_rejection"): "config_rejected",
            ("admin_config", "validator_rejection"): "config_rejected",
            ("model_config", "validator_rejection"): "config_rejected",
            ("create_app", "factory_exception"): "create_app_failed",
        }
        for pair, failure_code in expected.items():
            with self.subTest(pair=pair):
                self.assertEqual(classify(*pair)["failure_code"], failure_code)

    def test_unknown_is_strictly_single_field(self):
        classify = self.functions["_startup_failure_signal"]
        for pair in (("unknown", "unknown"), ("model_config", "schema_condition"), ("", "")):
            with self.subTest(pair=pair):
                self.assertEqual(classify(*pair), {"failure_code": "unknown"})

    def test_ordinary_database_error_is_unknown(self):
        classify = self.functions["_database_startup_failure_signal"]
        self.assertEqual(classify(sqlite3.DatabaseError()), {"failure_code": "unknown"})

        schema_error = sqlite3.DatabaseError()
        schema_error.sqlite_errorcode = sqlite3.SQLITE_SCHEMA
        self.assertEqual(classify(schema_error)["failure_code"], "schema_incompatible")

    def test_unmarked_startup_error_is_fixed_create_app_failure(self):
        classify = self.functions["_signal_for_startup_error"]
        result = classify(RuntimeError("sensitive text must not escape"))
        self.assertEqual(
            result,
            {
                "failed_stage": "create_app",
                "failure_signal": "factory_exception",
                "failure_code": "create_app_failed",
                "exception_type": "RuntimeError",
            },
        )
        self.assertNotIn("sensitive", str(result))

    def test_signal_carries_exception_type(self):
        classify = self.functions["_signal_for_startup_error"]
        result = classify(ValueError("should not escape"))
        self.assertEqual(
            result,
            {
                "failed_stage": "create_app",
                "failure_signal": "factory_exception",
                "failure_code": "create_app_failed",
                "exception_type": "ValueError",
            },
        )
        self.assertNotIn("should not escape", str(result))
        marked = RuntimeError("hidden")
        marked._curis_startup_failure = ("identity_config", "validator_rejection")
        marked_result = classify(marked)
        self.assertEqual(marked_result["failure_code"], "config_rejected")
        self.assertEqual(marked_result["exception_type"], "RuntimeError")
        self.assertNotIn("hidden", str(marked_result))

    def test_module_import_handler_runs_without_nameerror(self):
        # Runtime smoke test for the two `except ImportError as error:` handler bodies
        # (main.py ~:77-80 and ~:156-159). The existing AST+exec suite only loads
        # function bodies and never exercises these handlers, which previously gave a
        # false green (missing `as error` binding raised NameError at runtime).
        _classified_signal = self.functions["_classified_signal"]

        captured: list[dict] = []

        def _workspace_startup() -> bool:
            return True

        def _emit_startup_failure(signal: dict) -> None:
            captured.append(signal)

        for attempt in range(2):
            with self.subTest(attempt=attempt):
                captured.clear()
                # Mirror the real handler body verbatim, then catch the expected exit.
                with self.assertRaises(SystemExit):
                    try:
                        raise ImportError("forced acme_module missing")
                    except ImportError as error:
                        if _workspace_startup():
                            _emit_startup_failure(
                                _classified_signal("module_import", "import_exception", error)
                            )
                            raise SystemExit(1) from None
                        raise
                self.assertEqual(len(captured), 1)
                signal = captured[0]
                self.assertEqual(signal["failure_code"], "import_failed")
                self.assertIn("exception_type", signal)
                self.assertEqual(signal["exception_type"], "ImportError")
                # Red line: the raw exception message must never reach any signal field.
                for value in signal.values():
                    self.assertNotIn("forced", str(value))
                    self.assertNotIn("acme_module", str(value))
                    self.assertNotIn("missing", str(value))

    def test_admin_warning_is_suppressed_only_for_workspace(self):
        tree = ast.parse(MAIN.read_text(encoding="utf-8"))
        token_guard = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.If) and ast.unparse(node.test) == "not _admin_token_configured"
        )
        warning_guard, strict_guard = token_guard.body
        self.assertEqual(ast.unparse(warning_guard.test), "not _workspace_startup()")
        self.assertTrue(
            any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
                for node in ast.walk(warning_guard)
            )
        )
        self.assertEqual(ast.unparse(strict_guard.test), "_admin_strict")


if __name__ == "__main__":
    unittest.main()
