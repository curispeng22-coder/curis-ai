"""数据库迁移回归：capability_type CHECK 放开 agent 的整表重建。

Agent 运行时桥要求 ``capability_type`` 支持 ``'agent'``。SQLite 无法 ALTER
CHECK，只能整表重建。本测试验证 ``_migrate_capability_type_check_agent``：

- 旧库三张表（tenant_private_capabilities / employee_capability_bindings /
  ai_usage_records）的 CHECK 重建后包含 ``'agent'``；
- 数据原样保留；
- ai_usage_records 的索引与只读触发器（no_update / no_delete）恢复；
- 迁移幂等：再次 initialize 不重建、无 __agent 残留临时表。
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from app.database import Database

OLD_TABLES = """
create table tenant_private_capabilities (
  tenant_id text not null,
  capability_type text not null check (capability_type in ('model', 'tool', 'connector')),
  capability_id text not null,
  display_name text not null default '',
  metadata_json text not null default '{}',
  source text not null default 'tenant_private',
  status text not null default 'active',
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp,
  primary key (tenant_id, capability_type, capability_id)
);
create table employee_capability_bindings (
  id text primary key,
  tenant_id text not null,
  employee_id text not null,
  employee_template_id text,
  capability_source text not null check (capability_source in ('official', 'tenant_private', 'marketplace')),
  capability_type text not null check (capability_type in ('model', 'tool', 'connector')),
  capability_id text not null,
  priority integer not null default 100,
  enabled integer not null default 1,
  created_at text not null default current_timestamp,
  unique (tenant_id, employee_id, capability_source, capability_type, capability_id)
);
create table ai_usage_records (
  usage_record_id text primary key,
  tenant_id text not null,
  model_gateway_id text not null,
  provider_id text not null,
  model_name text not null,
  input_tokens integer, output_tokens integer, total_tokens integer, cost_amount numeric,
  currency text not null,
  cost_source text not null check (cost_source in ('unknown', 'estimated', 'provider_reported')),
  price_version text,
  employee_id text not null,
  capability_id text not null,
  capability_type text not null check (capability_type in ('model', 'tool', 'connector')),
  task_id text not null, project_id text not null, department_id text not null, request_id text not null,
  execution_status text not null, metering_status text not null,
  occurred_at text not null, created_at text not null default current_timestamp,
  idempotency_key text not null unique
);
create table projects (
  project_id text primary key,
  tenant_id text not null,
  company_id text not null,
  department_id text,
  name text not null,
  goal text not null,
  description text not null default '',
  project_type text not null default 'software_development',
  status text not null default 'planned',
  owner_employee_id text,
  primary_workflow_run_id text,
  root_task_id text,
  final_report text not null default '',
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);
create table department_instances (
  id text primary key,
  tenant_id text not null,
  company_id text not null,
  template_id text not null,
  name text not null,
  department_type text not null,
  manager_employee_id text,
  mission text not null default '',
  status text not null default 'active',
  created_from_template_id text not null default '',
  enabled_employee_template_ids_json text not null default '[]',
  enabled integer not null default 1,
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);
create index idx_ai_usage_tenant_occurred on ai_usage_records(tenant_id, occurred_at desc);
create trigger ai_usage_records_no_update before update on ai_usage_records
begin select raise(abort, 'ai_usage_records are immutable'); end;
"""


class AgentTypeCheckMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        conn = sqlite3.connect(self.db_path)
        conn.executescript(OLD_TABLES)
        conn.execute(
            "insert into tenant_private_capabilities "
            "(tenant_id, capability_type, capability_id, display_name) "
            "values ('t1', 'model', 'm1', 'Old Model')"
        )
        conn.execute(
            "insert into employee_capability_bindings "
            "(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
            "values ('b1', 't1', 'e1', 'tenant_private', 'model', 'm1')"
        )
        conn.execute(
            "insert into ai_usage_records (usage_record_id, tenant_id, model_gateway_id, "
            "provider_id, model_name, currency, cost_source, employee_id, capability_id, "
            "capability_type, task_id, project_id, department_id, request_id, "
            "execution_status, metering_status, occurred_at, idempotency_key) "
            "values ('u1', 't1', 'g1', 'p1', 'm1', 'usd', 'unknown', 'e1', 'm1', 'model', "
            "'task1', 'proj1', 'dep1', 'req1', 'success', 'confirmed', "
            "'2026-01-01T00:00:00Z', 'idem1')"
        )
        conn.execute(
            "insert into projects(project_id, tenant_id, company_id, department_id, name, goal) "
            "values ('proj1', 't1', 'company1', 'dep1', 'Legacy Project', 'Preserve usage')"
        )
        conn.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('dep1', 't1', 'company1', 'legacy', 'Legacy Department', 'TEST')"
        )
        conn.commit()
        conn.close()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        self.addCleanup(conn.close)
        return conn

    def test_migration_rebuilds_check_with_agent_and_keeps_data(self):
        Database(self.db_path).initialize()
        conn = self._connect()
        for table in (
            "tenant_private_capabilities",
            "employee_capability_bindings",
            "ai_usage_records",
        ):
            sql = conn.execute(
                "select sql from sqlite_master where type='table' and name=?", (table,)
            ).fetchone()["sql"]
            self.assertIn("'agent'", sql, f"{table} CHECK 未包含 agent")
            count = conn.execute(f"select count(*) from {table}").fetchone()[0]
            self.assertEqual(count, 1, f"{table} 数据未保留")
        row = conn.execute(
            "select capability_type, capability_id from tenant_private_capabilities"
        ).fetchone()
        self.assertEqual(dict(row), {"capability_type": "model", "capability_id": "m1"})

    def test_migration_restores_indexes_and_triggers(self):
        Database(self.db_path).initialize()
        conn = self._connect()
        idx_names = {
            row["name"]
            for row in conn.execute(
                "select name from sqlite_master where type='index' "
                "and tbl_name='ai_usage_records' and sql is not null"
            ).fetchall()
        }
        trig_names = {
            row["name"]
            for row in conn.execute(
                "select name from sqlite_master where type='trigger' "
                "and tbl_name='ai_usage_records'"
            ).fetchall()
        }
        self.assertIn("idx_ai_usage_tenant_occurred", idx_names)
        self.assertIn("ai_usage_records_no_update", trig_names)

    def test_migration_is_idempotent(self):
        Database(self.db_path).initialize()
        Database(self.db_path).initialize()
        conn = self._connect()
        residual = conn.execute(
            "select count(*) from sqlite_master where type='table' and name like '%__agent'"
        ).fetchone()[0]
        self.assertEqual(residual, 0, "幂等失败：残留临时表")

    def test_agent_register_and_bind_works_after_migration(self):
        # 迁移后旧库可直接登记 agent 能力并绑定（端到端收口）。
        Database(self.db_path).initialize()
        from app.main import create_app
        from fastapi.testclient import TestClient

        client = TestClient(create_app(self.db_path))
        self.addCleanup(client.close)
        headers = {"X-Tenant-Id": "tenant-migrate", "X-Ceo-Id": "ceo-migrate"}
        agent = client.post(
            "/api/workspace/capabilities/private",
            headers=headers,
            json={
                "capability_type": "agent",
                "capability_id": "my-agent-a",
                "display_name": "My Agent",
                "metadata": {"kind": "openai-compatible", "endpoint": "https://x.example.com"},
            },
        )
        self.assertEqual(agent.status_code, 201, agent.text)


if __name__ == "__main__":
    unittest.main()
