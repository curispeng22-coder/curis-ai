from __future__ import annotations

import json
import tempfile
import uuid
from pathlib import Path
from typing import Any

import pytest

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import LocalRDToolset
from app.real_rd_executor import (
    _EVIDENCE_AUDIT_FIELDS,
    _EVIDENCE_COMMAND_ID,
    _EVIDENCE_FIXTURE_SCHEMA,
    _EVIDENCE_ISSUE_ID,
    _EVIDENCE_REGISTERED_ARGV,
    _EVIDENCE_RUN_SOURCE,
    _EVIDENCE_TARGET_FILES,
    _EVIDENCE_TEST_COMMAND_ARGV,
    _EVIDENCE_TEST_FILE,
    _EVIDENCE_TOOL_ID,
    _evidence_fixture_sha256,
    RealRDExecutor,
    RealRDExecutorError,
)


RUN_ID = "wfr-focused-persistent-evidence"
STEP_ID = "wfs-focused-code-change"
TENANT_ID = "tenant-focused"
TASK_ID = "task-focused"
PROJECT_ID = "project-focused"
COMPANY_ID = "company-focused"
DEPARTMENT_ID = "department-focused"
EMPLOYEE_ID = "employee-focused"
BINDING_ID = "binding-focused"
TARGET = _EVIDENCE_TARGET_FILES[0]
DIFF = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -1,1 +1,1 @@\n"
    "-VALUE = 1\n"
    "+VALUE = 2\n"
)


class _Model:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response
        self.calls = 0

    def execute(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        return dict(self.response)


class _AuditedToolset:
    writes = 0

    def __init__(
        self,
        scope: Any,
        event_log: EvolutionEventLog,
        command_registry: dict[str, Any] | None = None,
        *,
        sandbox_mode: Any = None,
    ) -> None:
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}

    def _success(self, tool_id: str, fields: dict[str, Any]) -> None:
        LocalRDToolset._audit(
            self,
            tool_id,
            f"request-{uuid.uuid4()}",
            "succeeded",
            "",
            0,
            1,
            fields,
        )

    def read_file(self, raw: str) -> dict[str, Any]:
        self._success(
            "tl_ai_rd_file_reader",
            {"path_hash": "path-digest", "content_hash": "preimage-digest"},
        )
        return {
            "output": {
                "sha256": "preimage-digest",
                "lines": [{"text": "VALUE = 1"}],
                "ends_with_newline": True,
            }
        }

    def _apply_diff_transactional(self, raw: str) -> tuple[dict[str, Any], Any]:
        type(self).writes += 1
        self._success(
            "tl_ai_rd_file_writer",
            {
                "path_hash": "path-digest",
                "preimage_hash": "preimage-digest",
                "postimage_hash": "postimage-digest",
            },
        )
        return (
            {
                "output": {
                    "files": [
                        {
                            "path": TARGET,
                            "preimage_hash": "preimage-digest",
                            "postimage_hash": "postimage-digest",
                        }
                    ]
                }
            },
            lambda: None,
        )

    def run_test(self, raw: str) -> dict[str, Any]:
        command_id = json.loads(raw)["command_id"]
        self._success(
            "tl_ai_rd_test_runner",
            {"command_id": command_id, "exit_code": 0},
        )
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict[str, Any]:
        self._success(
            "tl_ai_rd_git_client",
            {"path_hash": "path-digest", "exit_code": 0},
        )
        return {"output": {"output": DIFF}}


def _usage_response() -> dict[str, Any]:
    return {
        "usage_record_id": "usage-real-rd-test",
        "status": "success",
        "output": DIFF,
        "prompt_tokens": 100,
        "completion_tokens": 20,
        "total_tokens": 120,
        "unit_price_input": 0.000001,
        "unit_price_output": 0.000002,
        "estimated_cost": 0.00014,
        "model_gateway_id": "newapi",
        "model_name": "focused-model",
        "provider_id": "openai",
        "price_version": "focused-v1",
        "currency": "USD",
        "cost_source": "model_gateway_adapter",
        "http_status": 200,
        "latency_ms": 5,
        "outbound_attempted": True,
    }


def _database() -> Database:
    root = Path(tempfile.mkdtemp(prefix="real-rd-evidence-"))
    database = Database(str(root / "focused.sqlite"))
    database.initialize()
    mapping = {
        "schema": _EVIDENCE_FIXTURE_SCHEMA,
        "issue_id": _EVIDENCE_ISSUE_ID,
        "run_source": _EVIDENCE_RUN_SOURCE,
        "operation_id": "op-00000000-0000-4000-8000-000000000001",
        "fixture_id": TASK_ID,
        "fixture_sha256": _evidence_fixture_sha256(),
        "target_files": list(_EVIDENCE_TARGET_FILES),
        "test_command_id": _EVIDENCE_COMMAND_ID,
        "test_command_argv": list(_EVIDENCE_TEST_COMMAND_ARGV),
        "registered_argv": list(_EVIDENCE_REGISTERED_ARGV),
        "allow_paths": [*_EVIDENCE_TARGET_FILES, _EVIDENCE_TEST_FILE],
        "tenant_id": TENANT_ID,
        "company_id": COMPANY_ID,
        "department_id": DEPARTMENT_ID,
        "project_id": PROJECT_ID,
        "workflow_run_id": RUN_ID,
        "workflow_step_id": STEP_ID,
        "employee_id": EMPLOYEE_ID,
        "employee_role": "backend_engineer",
        "tool_binding_id": BINDING_ID,
        "tool_capability_id": _EVIDENCE_TOOL_ID,
        "audit_fields": _EVIDENCE_AUDIT_FIELDS,
    }
    with database.connect() as connection:
        connection.execute(
            """
            insert into tasks (
              task_id, company_id, project_id, content, status, tenant_id
            ) values (?, ?, ?, ?, 'running', ?)
            """,
            (TASK_ID, COMPANY_ID, PROJECT_ID, json.dumps(mapping), TENANT_ID),
        )
        connection.execute(
            """
            insert into workflow_runs (
              workflow_run_id, tenant_id, company_id, project_id,
              created_from_template_id, workflow_instance_id,
              workflow_template_id, task_id,
              department_id, status
            ) values (?, ?, ?, ?, ?, 'wfi-focused', 'wt-focused', ?, ?, 'running')
            """,
            (
                RUN_ID,
                TENANT_ID,
                COMPANY_ID,
                PROJECT_ID,
                _EVIDENCE_RUN_SOURCE,
                TASK_ID,
                DEPARTMENT_ID,
            ),
        )
        connection.execute(
            """
            insert into workflow_steps (
              workflow_step_id, tenant_id, workflow_run_id, step_order,
              step_type, step_name, employee_role, status
            ) values (?, ?, ?, 1, 'code_change', 'code', 'backend_engineer', 'running')
            """,
            (STEP_ID, TENANT_ID, RUN_ID),
        )
        connection.execute(
            """
            insert into employee_instances (
              id, tenant_id, company_id, department_id, template_id,
              name, role, status, enabled
            ) values (?, ?, ?, ?, 'official.employee.backend_engineer',
                      'Focused Engineer', 'backend_engineer', 'idle', 1)
            """,
            (EMPLOYEE_ID, TENANT_ID, COMPANY_ID, DEPARTMENT_ID),
        )
        connection.execute(
            """
            insert into tools (name, type, description, entry)
            values (?, 'executor', 'focused', 'real_rd_executor')
            """,
            (_EVIDENCE_TOOL_ID,),
        )
        connection.execute(
            """
            insert into employee_capability_bindings (
              id, tenant_id, employee_id, capability_source,
              capability_type, capability_id, enabled
            ) values (?, ?, ?, 'official', 'tool', ?, 1)
            """,
            (BINDING_ID, TENANT_ID, EMPLOYEE_ID, _EVIDENCE_TOOL_ID),
        )
        connection.execute(
            """
            insert into step_assignments (
              step_assignment_id, tenant_id, workflow_step_id, employee_id,
              employee_role, capability_binding_id, status
            ) values ('assignment-focused', ?, ?, ?, 'backend_engineer', ?, 'assigned')
            """,
            (TENANT_ID, STEP_ID, EMPLOYEE_ID, BINDING_ID),
        )
    return database


def _spec(**overrides: Any) -> dict[str, Any]:
    spec = {
        "issue_id": "focused-persistent-evidence",
        "target_files": [TARGET],
        "test_command_id": _EVIDENCE_COMMAND_ID,
        "test_command_argv": list(_EVIDENCE_TEST_COMMAND_ARGV),
        "instructions": "sensitive prompt must never enter audit",
        "allow_paths": [*_EVIDENCE_TARGET_FILES, _EVIDENCE_TEST_FILE],
        "max_rounds": 1,
        "tenant_id": TENANT_ID,
        "project_id": PROJECT_ID,
        "task_id": TASK_ID,
        "workflow_run_id": RUN_ID,
        "workflow_step_id": STEP_ID,
    }
    spec.update(overrides)
    return spec


def test_same_run_links_tool_audit_and_model_usage_without_sensitive_text() -> None:
    database = _database()
    event_log = EvolutionEventLog(database)
    _AuditedToolset.writes = 0
    executor = RealRDExecutor(
        _Model(_usage_response()), event_log, toolset_cls=_AuditedToolset
    )

    result = executor.run(_spec())

    assert result["status"] == "succeeded"
    events = event_log.get_by_correlation_id(RUN_ID)
    model_events = [
        event for event in events if event["event_type"] == "real_rd.model_call_linked"
    ]
    tool_events = [event for event in events if event["event_type"] == "usage.tool_call"]
    assert len(model_events) == 1
    assert {
        event["payload"]["tool_id"] for event in tool_events
    } == {
        "tl_ai_rd_file_reader",
        "tl_ai_rd_file_writer",
        "tl_ai_rd_test_runner",
        "tl_ai_rd_git_client",
    }
    assert all(
        event["payload"]["workflow_run_id"] == RUN_ID
        and event["payload"]["workflow_step_id"] == STEP_ID
        for event in tool_events
    )
    assert all(
        not {"model_call", "total_tokens", "estimated_cost", "cost_source"}.intersection(
            event["payload"]
        )
        for event in tool_events
    )
    usage = model_events[0]["payload"]
    assert usage["workflow_run_id"] == RUN_ID
    assert usage["workflow_step_id"] == STEP_ID
    assert usage["usage_record_id"] == "usage-real-rd-test"
    assert not {
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "unit_price_input",
        "unit_price_output",
        "estimated_cost",
    }.intersection(usage)

    persisted = json.dumps(events, ensure_ascii=False)
    for forbidden in (
        "sensitive prompt",
        DIFF,
        "/Users/",
        "Authorization",
        "Cookie",
        "Bearer ",
        "sk-secret-value",
    ):
        assert forbidden not in persisted


@pytest.mark.parametrize("invalid_field", ["price_version", "estimated_cost"])
def test_missing_or_inconsistent_usage_fails_before_write(invalid_field: str) -> None:
    database = _database()
    event_log = EvolutionEventLog(database)
    response = _usage_response()
    if invalid_field == "price_version":
        response.pop(invalid_field)
    else:
        response[invalid_field] = 0.00015
    _AuditedToolset.writes = 0
    executor = RealRDExecutor(
        _Model(response), event_log, toolset_cls=_AuditedToolset
    )

    with pytest.raises(RealRDExecutorError) as caught:
        executor.run(_spec())

    assert caught.value.failure_code == "usage_evidence_invalid"
    assert _AuditedToolset.writes == 0
    assert not any(
        event["event_type"] == "real_rd.model_call_linked"
        for event in event_log.get_by_correlation_id(RUN_ID)
    )


def test_run_step_scope_mismatch_fails_before_model_or_tool() -> None:
    database = _database()
    event_log = EvolutionEventLog(database)
    model = _Model(_usage_response())
    executor = RealRDExecutor(model, event_log, toolset_cls=_AuditedToolset)

    with pytest.raises(RealRDExecutorError) as caught:
        executor.run(_spec(workflow_step_id="wfs-other"))

    assert caught.value.failure_code == "usage_scope_invalid"
    assert model.calls == 0
    assert event_log.get_by_correlation_id(RUN_ID) == []


@pytest.mark.parametrize(
    ("override", "expected_code"),
    [
        ({"test_command_id": "client-command"}, "fixture_scope_invalid"),
        ({"target_files": ["tools/other.py"]}, "fixture_scope_invalid"),
        ({"allow_paths": [TARGET]}, "fixture_scope_invalid"),
    ],
)
def test_client_fixture_override_fails_before_model_or_tool(
    override: dict[str, Any], expected_code: str
) -> None:
    database = _database()
    event_log = EvolutionEventLog(database)
    model = _Model(_usage_response())
    executor = RealRDExecutor(model, event_log, toolset_cls=_AuditedToolset)

    with pytest.raises(RealRDExecutorError) as caught:
        executor.run(_spec(**override))

    assert caught.value.failure_code == expected_code
    assert model.calls == 0
    assert event_log.get_by_correlation_id(RUN_ID) == []


def test_duplicate_registered_command_fails_before_model_or_tool() -> None:
    database = _database()
    with database.connect() as connection:
        content = connection.execute(
            "select content from tasks where task_id = ?", (TASK_ID,)
        ).fetchone()["content"]
        duplicate = json.loads(content)
        duplicate["fixture_id"] = "task-duplicate"
        connection.execute(
            """
            insert into tasks (
              task_id, company_id, project_id, content, status, tenant_id
            ) values ('task-duplicate', ?, ?, ?, 'pending', ?)
            """,
            (COMPANY_ID, PROJECT_ID, json.dumps(duplicate), TENANT_ID),
        )
    event_log = EvolutionEventLog(database)
    model = _Model(_usage_response())

    with pytest.raises(RealRDExecutorError) as caught:
        RealRDExecutor(model, event_log, toolset_cls=_AuditedToolset).run(_spec())

    assert caught.value.failure_code == "fixture_scope_invalid"
    assert model.calls == 0


def test_fixture_sha_mismatch_fails_before_model_or_tool() -> None:
    database = _database()
    with database.connect() as connection:
        mapping = json.loads(
            connection.execute(
                "select content from tasks where task_id = ?", (TASK_ID,)
            ).fetchone()["content"]
        )
        mapping["fixture_sha256"] = "0" * 64
        connection.execute(
            "update tasks set content = ? where task_id = ?",
            (json.dumps(mapping), TASK_ID),
        )
    event_log = EvolutionEventLog(database)
    model = _Model(_usage_response())

    with pytest.raises(RealRDExecutorError) as caught:
        RealRDExecutor(model, event_log, toolset_cls=_AuditedToolset).run(_spec())

    assert caught.value.failure_code == "fixture_scope_invalid"
    assert model.calls == 0


@pytest.mark.parametrize(
    "mutation",
    [
        "update employee_capability_bindings set enabled = 0 where id = 'binding-focused'",
        "update tasks set content = '{}' where task_id = 'task-focused'",
        """
        insert into executions (task_id, tool_name, prompt, output, tenant_id)
        values ('task-focused', 'real_rd_executor_tool', '', '', 'tenant-focused')
        """,
    ],
)
def test_inconsistent_preflight_state_fails_before_model_or_tool(
    mutation: str,
) -> None:
    database = _database()
    with database.connect() as connection:
        connection.execute(mutation)
    event_log = EvolutionEventLog(database)
    model = _Model(_usage_response())

    with pytest.raises(RealRDExecutorError):
        RealRDExecutor(model, event_log, toolset_cls=_AuditedToolset).run(_spec())

    assert model.calls == 0
    assert not any(
        event["event_type"] in {"usage.model_call", "usage.tool_call"}
        for event in event_log.get_by_correlation_id(RUN_ID)
    )
