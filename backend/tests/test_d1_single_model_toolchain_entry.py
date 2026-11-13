from __future__ import annotations

import hashlib
import inspect
import unittest

from app.d1_single_model_toolchain import (
    D1_ALLOWED_PATHS,
    D1_COMMAND_ARGV,
    D1_COMMAND_ID,
    D1_MAX_DIFF_BYTES,
    D1_PROJECT_ID,
    D1_RUN_ID,
    D1_TARGET_PATH,
    D1_TASK_ID,
    D1_TENANT_ID,
    D1_TEST_PATH,
    D1SingleModelToolchain,
    D1ToolchainError,
)
from app.local_rd_toolset import LocalRDToolScope
from app.model_gateway import R3_BASE_URL, R3_GATEWAY_ID, R3_MODEL_ID, R3_PROFILE, R3_PROVIDER_ID
from app.tenant_context import TenantContext


_DIFF = (
    f"--- a/{D1_TARGET_PATH}\n"
    f"+++ b/{D1_TARGET_PATH}\n"
    "@@ -1,1 +1,2 @@\n"
    " DEFAULT_TENANT = 'selfuse'\n"
    "+STORAGE_TENANT = 'default'\n"
)


class FakeModel:
    profile = R3_PROFILE
    base_url = R3_BASE_URL
    gateway_id = R3_GATEWAY_ID
    model_name = R3_MODEL_ID
    timeout = 60

    def __init__(self, output: str = _DIFF, api_key: str = "present") -> None:
        self.api_key = api_key
        self.output = output
        self.calls = 0

    def execute(self, _: str) -> dict:
        self.calls += 1
        return {
            "usage_record_id": "usage-d1-test",
            "output": self.output,
            "provider_id": R3_PROVIDER_ID,
            "model_gateway_id": R3_GATEWAY_ID,
            "model_name": R3_MODEL_ID,
            "prompt_tokens": 100,
            "completion_tokens": 40,
            "total_tokens": 140,
            "estimated_cost": 0.001,
            "status": "success",
            "http_status": 200,
            "latency_ms": 1,
            "outbound_attempted": True,
        }


class FakeEventLog:
    def __init__(self) -> None:
        self.database = object()
        self.events: list[dict] = []

    def record(self, **event: object) -> None:
        self.events.append(event)


class FakeTools:
    def __init__(self, paths: tuple[str, ...], commands: dict | None = None) -> None:
        self.scope = LocalRDToolScope(
            D1_TENANT_ID, D1_PROJECT_ID, D1_TASK_ID, D1_RUN_ID, paths
        )
        self.allowed_paths = frozenset(paths)
        self.command_registry = commands or {}
        self.calls: list[str] = []
        self.rolled_back = 0
        self.fail_test = False

    def read_file(self, raw: str) -> dict:
        path = D1_TARGET_PATH if D1_TARGET_PATH in raw else D1_TEST_PATH
        self.calls.append(f"read:{path}")
        content = "DEFAULT_TENANT = 'selfuse'\n" if path == D1_TARGET_PATH else "def test_d1(): pass\n"
        return {
            "output": {
                "path": path,
                "lines": [
                    {"line": index, "text": line, "truncated": False}
                    for index, line in enumerate(content.splitlines(), 1)
                ],
                "ends_with_newline": True,
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
            }
        }

    def search(self, _: str) -> dict:
        self.calls.append("search")
        return {"output": {"matches": []}}

    def _apply_diff_transactional(self, _: str):
        self.calls.append("write")

        def rollback() -> None:
            self.rolled_back += 1

        return {
            "output": {
                "files": [
                    {
                        "path": D1_TARGET_PATH,
                        "preimage_hash": "a" * 64,
                        "postimage_hash": "b" * 64,
                    }
                ]
            }
        }, rollback

    def run_test(self, _: str) -> dict:
        self.calls.append("test")
        if self.fail_test:
            raise RuntimeError("test failed")
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict:
        operation = "diff_check" if "diff_check" in raw else "diff"
        self.calls.append(f"git:{operation}")
        return {"output": {"exit_code": 0, "output_hash": "c" * 64}}


class D1SingleModelToolchainEntryTest(unittest.TestCase):
    def make_entry(self, model: FakeModel | None = None):
        events = FakeEventLog()
        reads = FakeTools(D1_ALLOWED_PATHS)
        writes = FakeTools(D1_ALLOWED_PATHS, {D1_COMMAND_ID: D1_COMMAND_ARGV})
        git = FakeTools((D1_TARGET_PATH,))
        entry = D1SingleModelToolchain(model or FakeModel(), reads, writes, git, events)
        entry._claim_once = lambda: reads.calls.append("claim")
        return entry, reads, writes, git, events

    def execute(
        self,
        entry: D1SingleModelToolchain,
        *,
        role: str = "owner",
        membership_status: str = "active",
    ):
        with TenantContext.scope(
            D1_TENANT_ID,
            subject_id="quality-member",
            ceo_id="ceo-d1",
            role=role,
            membership_status=membership_status,
            request_id="request-d1",
        ):
            return entry.execute()

    def test_fixed_chain_runs_once_without_planner_or_fallback(self) -> None:
        entry, reads, writes, git, events = self.make_entry()

        result = self.execute(entry)

        self.assertEqual(reads.calls, ["claim", f"read:{D1_TARGET_PATH}", f"read:{D1_TEST_PATH}", "search"])
        self.assertEqual(writes.calls, ["write", "test"])
        self.assertEqual(git.calls, ["git:diff", "git:diff_check"])
        self.assertEqual(entry.model.calls, 1)
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["command_id"], D1_COMMAND_ID)
        self.assertEqual([event["event_type"] for event in events.events], ["d1.model_call_linked", "d1.toolchain.succeeded"])
        self.assertEqual(events.events[0]["payload"]["usage_record_id"], "usage-d1-test")
        audit = repr(events.events)
        self.assertNotIn(_DIFF, audit)
        self.assertNotIn("DEFAULT_TENANT =", audit)

    def test_missing_key_or_scope_mismatch_rejects_before_tools_and_model(self) -> None:
        model = FakeModel(api_key="")
        entry, reads, writes, git, _ = self.make_entry(model)
        with self.assertRaisesRegex(D1ToolchainError, "rejected"):
            self.execute(entry)
        self.assertEqual(model.calls, 0)
        self.assertEqual(reads.calls + writes.calls + git.calls, [])

        entry, reads, writes, git, _ = self.make_entry()
        with TenantContext.scope("wrong-tenant"):
            with self.assertRaisesRegex(D1ToolchainError, "rejected"):
                entry.execute()
        self.assertEqual(entry.model.calls, 0)
        self.assertEqual(reads.calls + writes.calls + git.calls, [])

    def test_only_active_owner_or_ceo_can_claim(self) -> None:
        for role in ("owner", "ceo"):
            entry, reads, _, _, _ = self.make_entry()
            self.execute(entry, role=role)
            self.assertEqual(reads.calls[0], "claim")
            self.assertEqual(entry.model.calls, 1)

        for role, membership_status in (
            ("member", "active"),
            ("", "active"),
            ("owner", "revoked"),
        ):
            entry, reads, writes, git, _ = self.make_entry()
            with self.assertRaisesRegex(D1ToolchainError, "rejected"):
                self.execute(
                    entry,
                    role=role,
                    membership_status=membership_status,
                )
            self.assertEqual(entry.model.calls, 0)
            self.assertEqual(reads.calls + writes.calls + git.calls, [])

    def test_invalid_model_diff_stops_before_writer(self) -> None:
        entry, reads, writes, git, events = self.make_entry(FakeModel("```diff\nunsafe\n```"))
        with self.assertRaisesRegex(D1ToolchainError, "rejected"):
            self.execute(entry)
        self.assertEqual(entry.model.calls, 1)
        self.assertEqual(writes.calls + git.calls, [])
        self.assertEqual([event["event_type"] for event in events.events], ["d1.model_call_linked", "d1.toolchain.failed"])

    def test_failure_after_writer_rolls_back_and_stops(self) -> None:
        entry, _, writes, git, _ = self.make_entry()
        writes.fail_test = True
        with self.assertRaisesRegex(D1ToolchainError, "rejected"):
            self.execute(entry)
        self.assertEqual(writes.calls, ["write", "test"])
        self.assertEqual(writes.rolled_back, 1)
        self.assertEqual(git.calls, [])

    def test_contract_is_fixed_and_accepts_no_execute_parameters(self) -> None:
        self.assertEqual(D1_MAX_DIFF_BYTES, 4096)
        self.assertEqual(D1_ALLOWED_PATHS, (D1_TARGET_PATH, D1_TEST_PATH))
        self.assertEqual(
            D1_COMMAND_ARGV,
            (
                "backend/.venv/bin/python",
                "-m",
                "pytest",
                "-q",
                D1_TEST_PATH,
            ),
        )
        self.assertEqual(list(inspect.signature(D1SingleModelToolchain.execute).parameters), ["self"])


if __name__ == "__main__":
    unittest.main()
