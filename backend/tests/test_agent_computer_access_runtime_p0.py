from __future__ import annotations

import asyncio
import json

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.result_store import ResultStore
from app.tenant_context import TenantContext
from app.tool_executor import ToolExecutor
from app.tool_registry import ToolRegistry


def test_tool_executor_keeps_computer_access_snapshot(tmp_path):
    database = Database(str(tmp_path / "tool-access.sqlite"))
    database.initialize()
    registry = ToolRegistry(database)
    registry.register({"name": "codex_tool", "type": "agent"})
    snapshot = {
        "requested_intent": "ASK_WHEN_NEEDED",
        "native_mapping": {"state": "APPLIED", "sandbox": "read-only"},
        "configured_state": "CONFIGURED",
        "effective_state": "UNKNOWN",
        "verification_state": "UNVERIFIED",
        "evidence": {"kind": "COMMAND_ARGUMENT_ACCEPTED"},
        "verified_at": None,
    }
    executor = ToolExecutor(
        registry,
        {
            "codex_tool": lambda prompt: {
                "output": "done",
                "cost": 0,
                "computer_access": snapshot,
            }
        },
    )

    result = asyncio.run(executor.execute("codex_tool", "work"))
    assert result["computer_access"] == snapshot


def test_access_snapshot_persists_requested_history_without_resuming_effective_state(tmp_path):
    database_path = tmp_path / "computer-access.sqlite"
    database = Database(str(database_path))
    database.initialize()
    store = ResultStore(database, EvolutionEventLog(database))
    new_snapshot = {
        "requested_intent": "AUTO_WITHIN_BOUNDARY",
        "native_mapping": {"state": "APPLIED", "sandbox": "workspace-write"},
        "configured_state": "CONFIGURED",
        "effective_state": "UNKNOWN",
        "verification_state": "UNVERIFIED",
        "evidence": {"kind": "COMMAND_ARGUMENT_ACCEPTED"},
        "verified_at": None,
        "session_id": "thread-new",
    }
    resume_snapshot = {
        "requested_intent": "AUTO_WITHIN_BOUNDARY",
        "native_mapping": {"state": "NOT_CONFIGURABLE"},
        "configured_state": "NOT_CONFIGURABLE",
        "effective_state": "UNKNOWN",
        "verification_state": "UNVERIFIED",
        "evidence": {"kind": "PROVIDER_LIMITATION"},
        "verified_at": None,
        "drift": "RESUME_ACCESS_UNVERIFIED",
        "session_id": "thread-new",
    }

    with TenantContext.scope("tenant-a", company_id="company-a", ceo_id="ceo-a"):
        store._record_usage_events(
            "task-a",
            "codex_tool",
            0,
            {"workflow_run_id": "new", "computer_access": new_snapshot},
        )
        store._record_usage_events(
            "task-a",
            "codex_tool",
            0,
            {"workflow_run_id": "resume", "computer_access": resume_snapshot},
        )

    restarted = Database(str(database_path))
    with restarted.connect() as connection:
        rows = connection.execute(
            "select payload from evolution_events where event_type = 'usage.tool_call' order by event_id"
        ).fetchall()
    persisted = [json.loads(row[0])["computer_access"] for row in rows]
    assert persisted[0]["requested_intent"] == "AUTO_WITHIN_BOUNDARY"
    assert persisted[0]["effective_state"] == "UNKNOWN"
    assert persisted[1]["native_mapping"]["state"] == "NOT_CONFIGURABLE"
    assert persisted[1]["configured_state"] == "NOT_CONFIGURABLE"
    assert persisted[1]["effective_state"] == "UNKNOWN"
    assert persisted[1]["verification_state"] == "UNVERIFIED"
    assert persisted[1]["drift"] == "RESUME_ACCESS_UNVERIFIED"
