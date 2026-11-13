from __future__ import annotations

import sqlite3

import pytest

from app.database import Database


OLD_COLUMNS = """
  usage_record_id, tenant_id, model_gateway_id, provider_id, model_name,
  input_tokens, output_tokens, total_tokens, cost_amount, currency,
  cost_source, price_version, employee_id, capability_id, capability_type,
  task_id, project_id, department_id, request_id, execution_status,
  metering_status, occurred_at, created_at, idempotency_key, cache_read_tokens,
  cache_write_tokens, reasoning_tokens, latency_ms, workflow_run_id,
  workflow_step_id, capability_binding_id, logical_call_id, attempt_no,
  fallback_from_model, fallback_reason, http_status
"""


def _legacy_fixture(path, *, resolvable: bool) -> Database:
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute("drop trigger ai_usage_records_no_update")
        connection.execute("drop trigger ai_usage_records_no_delete")
        connection.execute("alter table ai_usage_records rename to ai_usage_records__source")
        connection.execute(
            f"create table ai_usage_records as select {OLD_COLUMNS} "
            "from ai_usage_records__source where 0"
        )
        connection.execute("drop table ai_usage_records__source")
        connection.execute(
            "create unique index idx_usage_idempotency_fixture "
            "on ai_usage_records(idempotency_key)"
        )
        connection.execute(
            "create trigger usage_fixture_no_update before update on ai_usage_records "
            "begin select raise(abort, 'immutable fixture'); end"
        )
        if resolvable:
            connection.execute(
                "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
                "values ('department-old', 'tenant-old', 'company-old', 'test', 'Old', 'TEST')"
            )
            connection.execute(
                "insert into projects(project_id, tenant_id, company_id, department_id, name, goal) "
                "values ('project-old', 'tenant-old', 'company-old', 'department-old', 'Old', 'Preserve')"
            )
        connection.execute(
            f"insert into ai_usage_records ({OLD_COLUMNS}) values "
            "('usage-old', 'tenant-old', 'gateway', 'provider', 'model', 3, 2, 5, "
            "'0.01', 'USD', 'provider_reported', null, 'employee-old', 'model.old', "
            "'model', 'task-old', 'project-old', 'department-old', 'request-old', "
            "'success', 'confirmed', '2026-08-27T00:00:00Z', "
            "'2026-08-27T00:00:00Z', 'idem-old', null, null, null, 10, null, null, "
            "null, 'logical-old', 1, null, null, 200)"
        )
    return database


def test_resolvable_history_is_preserved_and_migration_is_idempotent(tmp_path):
    database = _legacy_fixture(tmp_path / "upgrade.sqlite", resolvable=True)

    database.initialize()
    database.initialize()

    with database.connect() as connection:
        row = dict(connection.execute("select * from ai_usage_records").fetchone())
        indexes = {
            item["name"] for item in connection.execute("pragma index_list(ai_usage_records)")
        }
        triggers = {
            item["name"] for item in connection.execute(
                "select name from sqlite_master where type='trigger' and tbl_name='ai_usage_records'"
            )
        }
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        with pytest.raises(sqlite3.DatabaseError):
            connection.execute(
                "update ai_usage_records set model_name='changed' where usage_record_id='usage-old'"
            )

    assert row["company_id"] == "company-old"
    assert row["project_id"] == "project-old"
    assert row["business_id"] is None
    assert row["workspace_id"] is None
    assert row["work_ref"] is None
    assert row["execution_ref"] is None
    assert row["idempotency_key"] == "idem-old"
    assert "idx_usage_idempotency_fixture" in indexes
    assert {"idx_ai_usage_tenant_company", "idx_ai_usage_tenant_workspace", "idx_ai_usage_tenant_work"} <= indexes
    assert "usage_fixture_no_update" in triggers


def test_unresolvable_history_aborts_without_partial_table_rebuild(tmp_path):
    database = _legacy_fixture(tmp_path / "unresolved.sqlite", resolvable=False)
    with database.connect() as connection:
        before_schema = connection.execute(
            "select sql from sqlite_master where type='table' and name='ai_usage_records'"
        ).fetchone()[0]
        before_row = tuple(connection.execute("select * from ai_usage_records").fetchone())

    with pytest.raises(RuntimeError, match="cannot resolve Project"):
        database.initialize()

    with database.connect() as connection:
        assert connection.execute(
            "select sql from sqlite_master where type='table' and name='ai_usage_records'"
        ).fetchone()[0] == before_schema
        assert tuple(connection.execute("select * from ai_usage_records").fetchone()) == before_row
        assert not connection.execute(
            "select 1 from sqlite_master where name='ai_usage_records__canonical'"
        ).fetchone()
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_fresh_ledger_rejects_incomplete_canonical_and_legacy_rows(tmp_path):
    database = Database(str(tmp_path / "fresh.sqlite"))
    database.initialize()
    insert = (
        "insert into ai_usage_records(usage_record_id, tenant_id, company_id, "
        "model_gateway_id, provider_id, model_name, currency, cost_source, employee_id, "
        "capability_id, capability_type, task_id, project_id, department_id, business_id, "
        "workspace_id, work_ref, execution_ref, request_id, execution_status, "
        "metering_status, occurred_at, idempotency_key) values "
        "(?, 'tenant', 'company', 'gateway', 'provider', 'model', 'USD', 'unknown', "
        "'employee', 'capability', 'model', 'task', ?, 'department', ?, ?, ?, ?, "
        "'request', 'success', 'unknown', '2026-08-27T00:00:00Z', ?)"
    )
    with database.connect() as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                insert,
                ("bad-legacy", None, None, None, None, None, "bad-legacy"),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                insert,
                ("bad-canonical", None, "business", "workspace", None, "execution", "bad-canonical"),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                insert,
                ("mixed-partial", "project", "business", None, None, None, "mixed-partial"),
            )
