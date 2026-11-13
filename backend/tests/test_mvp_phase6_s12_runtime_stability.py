import asyncio
import json

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.employee import AIEmployee
from app.main import create_app
from app.orchestrator import Orchestrator
from app.prompt_builder import PromptBuilder
from app.result_store import ResultStore
from app.tool_executor import ToolExecutor
from app.tool_registry import ToolRegistry
from app.tool_router import ToolRouter


def test_local_selfuse_execution_has_trusted_ceo_usage_context(tmp_path, monkeypatch):
    db_path = str(tmp_path / "selfuse.sqlite")
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "local")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "selfuse")
    app = create_app(
        db_path,
        tool_functions={"default_tool": lambda prompt: {"output": "done", "cost": 0.01}},
    )
    client = TestClient(app)
    headers = {"X-Tenant-Id": "selfuse"}
    task_id = client.post("/api/task", json={"content": "Summarize"}, headers=headers).json()[
        "task_id"
    ]

    response = client.post(f"/api/task/{task_id}/run", headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"
    database = Database(db_path)
    with database.connect() as connection:
        payload = json.loads(
            connection.execute(
                "select payload from evolution_events "
                "where correlation_id=? and event_type='usage.task_execution'",
                (task_id,),
            ).fetchone()["payload"]
        )
    assert payload["ceo_id"] == "selfuse-ceo"


def test_post_execution_failure_never_leaves_task_running(tmp_path):
    database = Database(str(tmp_path / "runtime.sqlite"))
    database.initialize()
    store = ResultStore(database)
    registry = ToolRegistry(database)
    registry.register(
        {"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"}
    )
    employee = AIEmployee(
        ToolRouter(),
        ToolExecutor(
            registry,
            {"default_tool": lambda prompt: {"output": "done", "cost": 0.01}},
        ),
    )
    task = store.create_task("Summarize")

    def fail_to_persist(*args, **kwargs):
        raise RuntimeError("result persistence failed")

    store.save_execution = fail_to_persist
    with pytest.raises(RuntimeError, match="result persistence failed"):
        asyncio.run(Orchestrator(store, PromptBuilder(), employee).run(task["task_id"]))

    assert store.get_task(task["task_id"])["status"] == "FAILED"
    assert store.get_workflow(task["task_id"])["status"] == "COMPLETED"
