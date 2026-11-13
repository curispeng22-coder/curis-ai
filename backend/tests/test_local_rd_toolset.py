from __future__ import annotations

import asyncio
import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import (
    LOCAL_RD_TOOL_IDS,
    WORKSPACE_ROOT,
    LocalRDToolError,
    LocalRDToolScope,
    LocalRDToolset,
)
from app.tool_executor import ToolExecutionError, ToolExecutor
from app.tool_registry import ToolRegistry


class FailAfterStartAudit:
    def __init__(self) -> None:
        self.calls = 0

    def record(self, **_: object) -> None:
        self.calls += 1
        if self.calls > 1:
            raise RuntimeError("audit unavailable")


class LocalRDToolsetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.case_dir = Path(tempfile.mkdtemp(prefix=".curis-rd-test-", dir=WORKSPACE_ROOT))
        self.relative_dir = self.case_dir.relative_to(WORKSPACE_ROOT).as_posix()
        self.source = self.case_dir / "source.txt"
        self.notes = self.case_dir / "notes.md"
        self.source.write_text("alpha\nbeta\n", encoding="utf-8")
        self.notes.write_text("alpha documentation\n", encoding="utf-8")
        self.allowed = (
            f"{self.relative_dir}/source.txt",
            f"{self.relative_dir}/notes.md",
        )
        self.db_dir = tempfile.TemporaryDirectory()
        self.database = Database(str(Path(self.db_dir.name) / "audit.sqlite"))
        self.database.initialize()
        self.event_log = EvolutionEventLog(self.database)
        self.scope = LocalRDToolScope(
            tenant_id="tenant-rd",
            project_id="project-rd",
            task_id="task-rd",
            run_id="run-rd",
            allowed_paths=self.allowed,
        )
        self.toolset = LocalRDToolset(self.scope, self.event_log)
        self.registry = ToolRegistry(self.database)
        for tool_id in LOCAL_RD_TOOL_IDS:
            self.registry.register(
                {"name": tool_id, "type": "local", "description": "controlled local tool", "entry": tool_id}
            )
        self.executor = ToolExecutor(self.registry, self.toolset.functions())

    def tearDown(self) -> None:
        self.db_dir.cleanup()
        shutil.rmtree(self.case_dir, ignore_errors=True)

    def execute(self, tool_id: str, payload: dict[str, object]) -> dict[str, object]:
        return asyncio.run(self.executor.execute(tool_id, json.dumps(payload)))

    def test_reader_search_writer_and_git_are_real_local_actions(self) -> None:
        reader = self.execute("tl_ai_rd_file_reader", {"path": self.allowed[0]})
        self.assertEqual(
            reader["output"]["lines"][1],
            {"line": 2, "text": "beta", "truncated": False},
        )

        search = self.execute("tl_ai_rd_code_docs_search", {"query": "alpha"})
        self.assertEqual(len(search["output"]["matches"]), 2)

        before = self.source.read_bytes()
        patch = (
            f"--- a/{self.allowed[0]}\n"
            f"+++ b/{self.allowed[0]}\n"
            "@@ -1,2 +1,2 @@\n"
            " alpha\n"
            "-beta\n"
            "+gamma\n"
        )
        written = self.execute(
            "tl_ai_rd_file_writer",
            {"diff": patch, "preimage_hashes": {self.allowed[0]: hashlib.sha256(before).hexdigest()}},
        )
        self.assertEqual(self.source.read_text(encoding="utf-8"), "alpha\ngamma\n")
        self.assertEqual(written["output"]["files"][0]["path"], self.allowed[0])

        for operation in ("status", "diff", "diff_check"):
            git_result = self.execute("tl_ai_rd_git_client", {"operation": operation})
            self.assertEqual(git_result["output"]["exit_code"], 0)
            self.assertEqual(git_result["outbound_attempted"], False)

        usage = self.event_log.list_usage_events("tenant-rd", capability_type="tool")
        self.assertGreaterEqual(len(usage), 6)
        self.assertTrue(all(item["total_tokens"] is None for item in usage))
        self.assertTrue(all(item["estimated_cost"] is None for item in usage))
        raw_audit = json.dumps(self.event_log.get_by_correlation_id("run-rd"))
        self.assertNotIn(patch, raw_audit)
        self.assertNotIn("alpha documentation", raw_audit)

    def test_paths_content_and_diff_fail_closed(self) -> None:
        with self.assertRaisesRegex(LocalRDToolError, "relative path"):
            self.execute("tl_ai_rd_file_reader", {"path": "../source.txt"})
        with self.assertRaisesRegex(LocalRDToolError, "sensitive path"):
            self.execute("tl_ai_rd_file_reader", {"path": "data/curis.sqlite"})

        leak = self.case_dir / "leak.txt"
        leak.write_text("Authorization: Bearer abcdefghijklmnopqrstuvwxyz\n", encoding="utf-8")
        leak_scope = LocalRDToolScope(
            "tenant-rd", "project-rd", "task-rd", "run-rd-leak",
            (f"{self.relative_dir}/leak.txt",),
        )
        leak_tool = LocalRDToolset(leak_scope, self.event_log)
        with self.assertRaisesRegex(LocalRDToolError, "sensitive value"):
            leak_tool.read_file(json.dumps({"path": f"{self.relative_dir}/leak.txt"}))

        bad_patch = f"--- a/{self.allowed[0]}\n+++ /dev/null\n@@ -1,1 +0,0 @@\n-alpha\n"
        with self.assertRaisesRegex(LocalRDToolError, "delete"):
            self.execute(
                "tl_ai_rd_file_writer",
                {"diff": bad_patch, "preimage_hashes": {self.allowed[0]: hashlib.sha256(self.source.read_bytes()).hexdigest()}},
            )
        self.assertEqual(self.source.read_text(encoding="utf-8"), "alpha\nbeta\n")

    def test_symlink_and_hardlink_are_rejected(self) -> None:
        symlink = self.case_dir / "link.txt"
        symlink.symlink_to(self.source)
        hardlink = self.case_dir / "hard.txt"
        os.link(self.source, hardlink)
        scope = LocalRDToolScope(
            "tenant-rd", "project-rd", "task-rd", "run-rd-links",
            (f"{self.relative_dir}/link.txt", f"{self.relative_dir}/hard.txt"),
        )
        tools = LocalRDToolset(scope, self.event_log)
        with self.assertRaisesRegex(LocalRDToolError, "Symbolic|symbolic"):
            tools.read_file(json.dumps({"path": f"{self.relative_dir}/link.txt"}))
        with self.assertRaisesRegex(LocalRDToolError, "hard links"):
            tools.read_file(json.dumps({"path": f"{self.relative_dir}/hard.txt"}))

    def test_unregistered_or_arbitrary_commands_and_git_writes_are_rejected(self) -> None:
        with self.assertRaisesRegex(LocalRDToolError, "not registered"):
            self.execute("tl_ai_rd_test_runner", {"command_id": "not-approved"})
        with self.assertRaisesRegex(LocalRDToolError, "input is invalid"):
            self.execute(
                "tl_ai_rd_test_runner",
                {"command_id": "not-approved", "command": "python -c 'print(1)'"},
            )
        with self.assertRaisesRegex(LocalRDToolError, "not allowed"):
            self.execute("tl_ai_rd_git_client", {"operation": "commit"})
        with self.assertRaisesRegex(ValueError, "approved command families"):
            LocalRDToolset(self.scope, self.event_log, {"shell": ("/bin/sh", "-c", "echo unsafe")})

    def test_writer_rolls_back_when_final_audit_fails(self) -> None:
        toolset = LocalRDToolset(self.scope, FailAfterStartAudit())
        before = self.source.read_bytes()
        patch = (
            f"--- a/{self.allowed[0]}\n"
            f"+++ b/{self.allowed[0]}\n"
            "@@ -1,2 +1,2 @@\n"
            " alpha\n"
            "-beta\n"
            "+gamma\n"
        )
        with self.assertRaisesRegex(LocalRDToolError, "audit is unavailable"):
            toolset.apply_diff(
                json.dumps(
                    {"diff": patch, "preimage_hashes": {self.allowed[0]: hashlib.sha256(before).hexdigest()}}
                )
            )
        self.assertEqual(self.source.read_bytes(), before)

    def test_local_tools_never_fallback_or_trace_input_output(self) -> None:
        calls: list[str] = []

        def fail(_: str) -> dict[str, object]:
            raise LocalRDToolError("rejected", "rejected")

        def fallback(_: str) -> dict[str, object]:
            calls.append("fallback")
            return {"output": "should not run"}

        executor = ToolExecutor(
            self.registry,
            {"tl_ai_rd_file_reader": fail, "default_tool": fallback},
        )
        with self.assertRaises(ToolExecutionError) as raised:
            asyncio.run(executor.execute_chain(["tl_ai_rd_file_reader"], '{"path":"secret"}'))
        self.assertEqual(calls, [])
        self.assertEqual(len(raised.exception.trace), 1)
        self.assertEqual(raised.exception.trace[0]["input"], "")
        self.assertEqual(raised.exception.trace[0]["output"], "")


if __name__ == "__main__":
    unittest.main()
