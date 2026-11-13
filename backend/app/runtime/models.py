"""Curis Business Runtime —— 领域表 DDL（A5 + 第 2 步）。

Commitment / Workspace / Outcome / Attribution / BusinessDirection 的持久化。
ScheduledRun / Cadence 的表在 ``scheduler.py`` 内（A2 专属）。

所有表沿用 ``Database.connect()`` + 默认租户（``selfuse``）策略，与
``runtime_transition_log`` 同库、重启不丢。状态列的取值**只允许**来自
``app.runtime.states`` 枚举，更新一律走状态机（见 ``ceo_day_service``），
禁止业务代码直写 status 列。
"""

from __future__ import annotations

import json
from typing import Any

from ..database import Database

CEO_DAY_SCHEMA = """
create table if not exists business_directions (
  direction_id     text primary key,
  tenant_id        text not null default 'selfuse',
  name             text not null,
  template_type    text not null,
  opportunity       text not null default '',
  target_outcome   text not null default '',
  timebox_days     integer not null default 30,
  evidence_route   text not null default '',
  lifecycle_status text not null,
  verification_status text not null default 'UNVERIFIED',
  current_cycle    integer not null default 0,
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create table if not exists commitments (
  commitment_id    text primary key,
  tenant_id        text not null default 'selfuse',
  business_id      text not null,
  department_id    text not null default '',
  department_name  text not null default '',
  name             text not null,
  target_outcome   text not null default '',
  status           text not null,
  cycle            integer not null default 1,
  workspace_id     text,
  capacity_contract_json text not null default '{}',
  last_reported_at text,
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create table if not exists workspaces (
  workspace_id     text primary key,
  tenant_id        text not null default 'selfuse',
  business_id      text not null,
  name             text not null,
  blueprint_json   text not null default '{}',
  status           text not null,
  simulation_passed integer not null default 0,
  issues_resolved  integer not null default 0,
  external_agent_reviewed integer not null default 0,
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create table if not exists outcomes (
  outcome_id       text primary key,
  tenant_id        text not null default 'selfuse',
  business_id      text not null,
  commitment_id    text,
  run_id           text,
  route            text not null default '',
  value            real not null default 0,
  evidence_grade   text not null default 'UNVERIFIED',
  source           text not null default '',
  evidence_ref     text not null default '',
  evidence_type    text not null default '',
  captured_at      text not null default current_timestamp,
  attribution_status text not null default 'PENDING_REVIEW',
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create table if not exists attributions (
  attribution_id   text primary key,
  tenant_id        text not null default 'selfuse',
  outcome_id       text not null,
  agent            text not null default '',
  model            text not null default '',
  skills_json      text not null default '[]',
  tools_json       text not null default '[]',
  weight           real not null default 0,
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);
"""

RUNTIME_FOUNDATION_SCHEMA = """
create table if not exists canonical_businesses (
  business_id       text primary key,
  tenant_id         text not null,
  company_id        text not null,
  department_id     text not null,
  name              text not null,
  lifecycle_status  text not null default 'DRAFT'
                    check(lifecycle_status in ('DRAFT','ACTIVE','PAUSED','ARCHIVED')),
  goal              text not null default '',
  positioning       text not null default '',
  strategy_direction_ref text,
  created_at        text not null,
  updated_at        text not null,
  unique(tenant_id, company_id, business_id)
);
create index if not exists idx_canonical_business_scope
  on canonical_businesses(tenant_id, company_id, department_id, lifecycle_status);

create table if not exists workspaces (
  workspace_id     text primary key,
  tenant_id        text not null default 'selfuse',
  company_id       text,
  business_id      text not null,
  name             text not null,
  blueprint_json   text not null default '{}',
  blueprint_version text,
  operating_version integer not null default 0,
  status           text not null,
  business_relation_status text not null default 'UNRESOLVED',
  business_relation_reason text not null default 'LEGACY_REFERENCE_NOT_CLASSIFIED',
  business_relation_owner text not null default 'Business Spine Migration',
  business_relation_source text not null default 'LEGACY',
  business_relation_checked_at text,
  simulation_passed integer not null default 0,
  issues_resolved  integer not null default 0,
  external_agent_reviewed integer not null default 0,
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);

create table if not exists runtime_transition_log (
  log_id        integer primary key autoincrement,
  tenant_id     text not null default 'selfuse',
  entity_type   text not null,
  entity_id     text not null,
  source        text not null,
  target        text not null,
  trigger       text not null default '',
  actor         text not null,
  at            text not null,
  reason        text not null default '',
  company_id    text,
  workspace_id  text,
  evidence_refs_json text not null default '[]',
  next_check_at text,
  context_json  text not null default '{}'
);
create index if not exists idx_rtl_entity
  on runtime_transition_log(tenant_id, entity_type, entity_id);
create index if not exists idx_rtl_at on runtime_transition_log(tenant_id, at);

create table if not exists runtime_entities (
  entity_id             text primary key,
  tenant_id             text not null,
  entity_type           text not null,
  company_id            text,
  workspace_id          text,
  parent_id             text,
  owner_ref             text not null default '',
  lifecycle_status      text not null,
  exception_status      text not null default 'NONE',
  presence_state        text,
  org_version           text,
  blueprint_version     text,
  capability_ref        text,
  execution_ref         text,
  current_version_id    text,
  approved_version_id   text,
  published_version_id  text,
  verification_status   text not null default 'UNVERIFIED',
  evidence_condition    text not null default 'MISSING',
  next_check_at         text,
  data_json             text not null default '{}',
  created_at            text not null,
  updated_at            text not null
);
create index if not exists idx_runtime_entities_scope
  on runtime_entities(tenant_id, company_id, workspace_id, entity_type);
create unique index if not exists idx_runtime_one_ceo_assistant
  on runtime_entities(tenant_id, company_id)
  where entity_type = 'CEO_ASSISTANT';

create table if not exists runtime_links (
  link_id       text primary key,
  tenant_id     text not null,
  company_id    text,
  workspace_id  text,
  source_id     text not null,
  relation      text not null,
  target_id     text not null,
  created_at    text not null,
  unique(tenant_id, source_id, relation, target_id)
);
create index if not exists idx_runtime_links_source
  on runtime_links(tenant_id, source_id, relation);
create index if not exists idx_runtime_links_target
  on runtime_links(tenant_id, target_id, relation);

create table if not exists runtime_simulation_runs (
  simulation_run_id text primary key,
  tenant_id         text not null,
  company_id        text not null,
  ceo_id            text not null,
  workspace_id      text,
  blueprint_version text not null,
  scenario_id       text not null,
  lifecycle_status  text not null,
  pass_status       text not null default 'NOT_RUN',
  participants_json text not null default '[]',
  input_refs_json   text not null default '[]',
  state_transitions_json text not null default '[]',
  handoffs_json     text not null default '[]',
  receipts_json     text not null default '[]',
  evidence_refs_json text not null default '[]',
  failure_events_json text not null default '[]',
  ceo_decisions_json text not null default '[]',
  final_state       text,
  reviewer          text,
  review_notes      text not null default '',
  started_at        text,
  finished_at       text,
  reviewed_at       text,
  invalidated_at    text,
  invalidation_reason text,
  created_at        text not null,
  updated_at        text not null
);
create index if not exists idx_runtime_simulation_scope
  on runtime_simulation_runs(tenant_id, company_id, workspace_id, scenario_id);

create table if not exists runtime_workspace_versions (
  version_id          text primary key,
  tenant_id           text not null,
  company_id          text not null,
  workspace_id        text not null,
  blueprint_version   text not null,
  status              text not null,
  simulation_passed   integer not null default 0,
  operating_version   integer not null default 0,
  change_kind         text not null default '',
  data_json           text not null default '{}',
  created_at          text not null,
  updated_at          text not null,
  unique(tenant_id, workspace_id, blueprint_version)
);
"""


def ensure_ceo_day_schema(database: Database) -> None:
    with database.connect() as conn:
        conn.executescript(CEO_DAY_SCHEMA)


def ensure_runtime_foundation_schema(connection) -> None:
    """Additive, idempotent Runtime Foundation migration."""
    connection.executescript(RUNTIME_FOUNDATION_SCHEMA)
    workspace_columns = {row["name"] for row in connection.execute("pragma table_info(workspaces)")}
    for name, definition in (
        ("company_id", "text"),
        ("blueprint_version", "text"),
        ("operating_version", "integer not null default 0"),
        ("business_relation_status", "text not null default 'UNRESOLVED'"),
        ("business_relation_reason", "text not null default 'LEGACY_REFERENCE_NOT_CLASSIFIED'"),
        ("business_relation_owner", "text not null default 'Business Spine Migration'"),
        ("business_relation_source", "text not null default 'LEGACY'"),
        ("business_relation_checked_at", "text"),
    ):
        if name not in workspace_columns:
            connection.execute(f"alter table workspaces add column {name} {definition}")

    log_columns = {row["name"] for row in connection.execute("pragma table_info(runtime_transition_log)")}
    for name, definition in (
        ("company_id", "text"),
        ("workspace_id", "text"),
        ("evidence_refs_json", "text not null default '[]'"),
        ("next_check_at", "text"),
    ):
        if name not in log_columns:
            connection.execute(f"alter table runtime_transition_log add column {name} {definition}")
    simulation_columns = {row["name"] for row in connection.execute("pragma table_info(runtime_simulation_runs)")}
    if "state_transitions_json" not in simulation_columns:
        connection.execute(
            "alter table runtime_simulation_runs add column state_transitions_json text not null default '[]'"
        )

    connection.executescript(
        """
        create trigger if not exists trg_canonical_business_parent_insert
        before insert on canonical_businesses
        begin
          select case when not exists (
            select 1 from companies c
            where c.tenant_id = new.tenant_id and c.company_id = new.company_id
          ) then raise(abort, 'canonical business company missing') end;
          select case when not exists (
            select 1 from department_instances d
            where d.tenant_id = new.tenant_id and d.company_id = new.company_id
              and d.id = new.department_id and d.status != 'archived'
          ) then raise(abort, 'canonical business department missing') end;
        end;

        create trigger if not exists trg_canonical_business_parent_update
        before update of tenant_id, company_id, department_id on canonical_businesses
        begin
          select case when not exists (
            select 1 from companies c
            where c.tenant_id = new.tenant_id and c.company_id = new.company_id
          ) then raise(abort, 'canonical business company missing') end;
          select case when not exists (
            select 1 from department_instances d
            where d.tenant_id = new.tenant_id and d.company_id = new.company_id
              and d.id = new.department_id and d.status != 'archived'
          ) then raise(abort, 'canonical business department missing') end;
        end;

        create trigger if not exists trg_canonical_business_delete_guard
        before delete on canonical_businesses
        when exists (
          select 1 from workspaces w
          where w.tenant_id = old.tenant_id and w.company_id = old.company_id
            and w.business_id = old.business_id
            and w.business_relation_status = 'RESOLVED'
        )
        begin
          select raise(abort, 'canonical business still owns workspaces');
        end;

        create trigger if not exists trg_workspace_business_resolved_insert
        before insert on workspaces
        when new.business_relation_status = 'RESOLVED'
        begin
          select case when not exists (
            select 1 from canonical_businesses b
            where b.tenant_id = new.tenant_id and b.company_id = new.company_id
              and b.business_id = new.business_id and b.lifecycle_status != 'ARCHIVED'
          ) then raise(abort, 'resolved workspace business missing') end;
        end;

        create trigger if not exists trg_workspace_business_resolved_update
        before update of tenant_id, company_id, business_id, business_relation_status on workspaces
        when new.business_relation_status = 'RESOLVED'
        begin
          select case when not exists (
            select 1 from canonical_businesses b
            where b.tenant_id = new.tenant_id and b.company_id = new.company_id
              and b.business_id = new.business_id and b.lifecycle_status != 'ARCHIVED'
          ) then raise(abort, 'resolved workspace business missing') end;
        end;
        """
    )


def _json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return {}
