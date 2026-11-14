from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import hashlib
import json
import os
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Sequence

from .tenant_context import DEFAULT_TENANT, TenantContext
from .catalog_constants import effect_class_for_capability


_VALID_TENANT_STATUSES = frozenset({"active", "inactive", "suspended"})
SCHEMA_VERSION = 1

# These tables are not owned by the integration baseline. The checked-in
# database contains empty remnants from earlier prototypes. Migration v1 only
# removes them when empty; a non-empty table fails closed.
_RETIRED_EMPTY_TABLES = (
    "action_proposals",
    "content_publish_attempts",
    "content_publish_claims",
    "content_routine_runs",
    "content_routines",
    "decision_audit_events",
    "decision_drafts",
    "decision_records",
    "employee_context_manifests",
    "employee_role_guard_audits",
    "employee_role_guard_claims",
    "employee_session_audit_events",
    "employee_session_step_bindings",
    "employee_session_step_claim_bindings",
    "employee_sessions",
    "employee_working_memory_audits",
    "employee_working_memory_checkpoints",
    "goal_achievement_confirmations",
    "goal_criterion_evidence",
    "goal_progress_snapshots",
    "project_memory_audit_events",
    "project_outcome_memories",
    "secretary_conversations",
    "secretary_messages",
    "secretary_mode_preferences",
    "secretary_profiles",
    "secretary_suggestions",
    "workflow_recovery_attempts",
    "workflow_recovery_risks",
    "workspace_goals",
)

# Business Runtime 流转留痕表（runtime_transition_log）的 DDL 已迁至
# app/runtime/store.py（A5 拆单体：runtime 关注点不再进入 Database God Class）。
# 表在 SQLiteTransitionRecorder.ensure_schema() 中按需创建，同库同租户、重启不丢。


def _validate_tenant_status(status: str) -> None:
    if status not in _VALID_TENANT_STATUSES:
        raise ValueError(
            f"无效的租户状态: {status!r}，允许值: "
            + ", ".join(sorted(_VALID_TENANT_STATUSES))
        )


# P1-1：tool_templates 安全治理字段回填映射（来自 docs/plan/p1-1-security-col-design.md §3.4）。
# 键为 tool_template_id，值为 (security_level, [规范部门中文名...])。
# 部门名已按 §2.2 受控词表归一：「全员（通用）」→「全员」，其余原样与 catalog 逐字可追溯。
# 数据来源：§3.1 高危 21 条（catalog §七）+ §3.2 ai_rd 内部 30 条（架构师建议值）+ §3.3 其余 64 条。
_SECURITY_BACKFILL: dict[str, tuple[str, list[str]]] = {
    # ── 高危 21（catalog §七）──
    "tl_github": ("high", ["研发部"]),
    "tl_gitlab": ("high", ["研发部"]),
    "tl_postgres": ("high", ["研发部", "数据部"]),
    "tl_supabase": ("high", ["研发部", "数据部"]),
    "tl_slack": ("high", ["全员", "运营部"]),
    "tl_zapier": ("high", ["运营部", "全员"]),
    "tl_n8n": ("high", ["运营部", "研发部"]),
    "tl_pipedream": ("high", ["运营部", "研发部"]),
    "tl_strix": ("high", ["安全部", "研发部"]),
    "tl_activepieces": ("high", ["运营部", "研发部"]),
    "tl_make": ("high", ["运营部"]),
    "tl_shopify": ("high", ["电商部", "运营部"]),
    "tl_stripe": ("high", ["财务部", "电商部"]),
    "tl_paypal": ("high", ["财务部", "电商部"]),
    "tl_alipay": ("high", ["财务部", "电商部"]),
    "tl_taobao_open": ("high", ["电商部", "运营部"]),
    "tl_jd_jos": ("high", ["电商部", "运营部"]),
    "tl_pinduoduo": ("high", ["电商部", "运营部"]),
    "tl_douyin_ecom": ("high", ["电商部", "内容部"]),
    "tl_woocommerce": ("high", ["电商部", "运营部"]),
    "tl_youzan": ("high", ["电商部", "运营部"]),
    # ── ai_rd 内部 30（架构师建议值）──
    "tl_ai_rd_code_executor": ("high", ["研发部"]),
    "tl_ai_rd_python_repl": ("high", ["研发部"]),
    "tl_ai_rd_shell_terminal": ("high", ["研发部", "运维部"]),
    "tl_ai_rd_docker_run": ("high", ["研发部", "运维部"]),
    "tl_ai_rd_kubernetes_ctl": ("high", ["研发部", "运维部"]),
    "tl_ai_rd_ci_runner": ("high", ["研发部", "运维部"]),
    "tl_ai_rd_cloud_deploy": ("high", ["研发部", "运维部"]),
    "tl_ai_rd_secret_resolver": ("high", ["安全部", "研发部"]),
    "tl_ai_rd_git_client": ("medium", ["研发部"]),
    "tl_ai_rd_github_api": ("medium", ["研发部"]),
    "tl_ai_rd_http_client": ("medium", ["研发部", "全员"]),
    "tl_ai_rd_graphql_client": ("medium", ["研发部"]),
    "tl_ai_rd_postgres_connector": ("medium", ["研发部", "数据部"]),
    "tl_ai_rd_sql_query_executor": ("medium", ["研发部", "数据部"]),
    "tl_ai_rd_vector_db_query": ("medium", ["研发部", "数据部"]),
    "tl_ai_rd_vector_db_upsert": ("medium", ["研发部", "数据部"]),
    "tl_ai_rd_log_aggregator": ("medium", ["研发部", "运维部"]),
    "tl_ai_rd_metric_monitor": ("medium", ["研发部", "运维部"]),
    "tl_ai_rd_alert_sender": ("medium", ["研发部", "运维部"]),
    "tl_ai_rd_file_reader": ("low", ["研发部"]),
    "tl_ai_rd_file_writer": ("low", ["研发部"]),
    "tl_ai_rd_directory_search": ("low", ["研发部"]),
    "tl_ai_rd_code_linter": ("low", ["研发部"]),
    "tl_ai_rd_test_runner": ("low", ["研发部"]),
    "tl_ai_rd_code_docs_search": ("low", ["研发部"]),
    "tl_ai_rd_csv_parser": ("low", ["研发部", "数据部"]),
    "tl_ai_rd_pandas_analyzer": ("low", ["研发部", "数据部"]),
    "tl_ai_rd_chart_plotter": ("low", ["研发部", "数据部"]),
    "tl_ai_rd_pdf_parser": ("low", ["研发部", "全员"]),
    "tl_ai_rd_docx_generator": ("low", ["研发部", "全员"]),
    # ── Pack A 非高危 8 ──
    "tl_docker": ("medium", ["研发部", "运维部"]),
    "tl_playwright": ("medium", ["测试部", "研发部"]),
    "tl_sentry": ("medium", ["研发部", "运维部"]),
    "tl_brave_search": ("low", ["全员"]),
    "tl_notion": ("medium", ["产品部", "全员"]),
    "tl_linear": ("medium", ["研发部"]),
    "tl_figma": ("low", ["设计部"]),
    "tl_hubspot": ("medium", ["市场部", "销售部"]),
    # ── Pack C 非高危 12 ──
    "tl_google_drive": ("medium", ["全员", "产品部"]),
    "tl_google_maps": ("low", ["全员"]),
    "tl_tavily": ("low", ["全员"]),
    "tl_exa": ("low", ["全员"]),
    "tl_desktopcommander": ("medium", ["研发部"]),
    "tl_cubesandbox": ("medium", ["研发部", "运维部"]),
    "tl_agent_memory": ("low", ["研发部"]),
    "tl_agency_agents": ("low", ["全员"]),
    "tl_superpowers": ("low", ["研发部"]),
    "tl_agent_skills": ("low", ["研发部"]),
    "tl_officecli": ("low", ["全员", "产品部"]),
    "tl_meetily": ("low", ["全员"]),
    # ── Pack D 14 ──
    "tl_midjourney": ("low", ["内容部", "设计部", "市场部"]),
    "tl_kling": ("low", ["内容部"]),
    "tl_runway": ("low", ["内容部", "设计部"]),
    "tl_suno": ("low", ["内容部"]),
    "tl_elevenlabs": ("low", ["内容部"]),
    "tl_capcut": ("low", ["内容部"]),
    "tl_descript": ("low", ["内容部"]),
    "tl_heygen": ("low", ["内容部", "市场部"]),
    "tl_canva": ("low", ["内容部", "市场部", "设计部"]),
    "tl_adobe_firefly": ("low", ["设计部", "内容部"]),
    "tl_ideogram": ("low", ["内容部", "设计部"]),
    "tl_wordpress": ("medium", ["内容部", "市场部"]),
    "tl_wechat_official": ("medium", ["内容部", "市场部"]),
    "tl_douyin_content": ("medium", ["内容部", "市场部"]),
    # ── Pack E 非高危 2 ──
    "tl_sf_express": ("medium", ["电商部", "运营部"]),
    "tl_aftership": ("medium", ["电商部", "运营部"]),
    # ── Pack F–J 28 ──
    "tl_pptx": ("low", ["全员", "市场部", "产品部"]),
    "tl_xlsx": ("low", ["全员", "财务部", "运营部"]),
    "tl_pdf": ("low", ["全员", "法务部"]),
    "tl_docx": ("low", ["全员", "产品部"]),
    "tl_product_manager_toolkit": ("low", ["产品部"]),
    "tl_ai_drawio": ("low", ["研发部", "产品部"]),
    "tl_frontend_design": ("low", ["研发部"]),
    "tl_nanobanana_ppt": ("low", ["市场部", "产品部"]),
    "tl_content_publisher": ("medium", ["内容部", "市场部"]),
    "tl_article_illustrator": ("low", ["内容部"]),
    "tl_url_to_markdown": ("low", ["内容部", "研发部"]),
    "tl_format_markdown": ("low", ["全员"]),
    "tl_post_to_x": ("medium", ["市场部"]),
    "tl_xhs_images": ("low", ["内容部", "市场部"]),
    "tl_video_suite": ("low", ["内容部"]),
    "tl_video_collaborator": ("low", ["内容部"]),
    "tl_video_recreation": ("low", ["内容部"]),
    "tl_video_frame_extractor": ("low", ["内容部", "研发部"]),
    "tl_viral_video_copy": ("low", ["内容部", "市场部"]),
    "tl_tts_voice": ("low", ["内容部"]),
    "tl_qwen_asr": ("low", ["内容部", "会议"]),
    "tl_infinitetalk": ("low", ["内容部"]),
    "tl_ecom_copywriter": ("low", ["电商部", "市场部"]),
    "tl_ecom_video_marketing": ("low", ["电商部", "内容部"]),
    "tl_product_copywriter": ("low", ["市场部"]),
    "tl_product_video": ("low", ["市场部", "电商部"]),
    "tl_paper_analysis": ("low", ["研发部", "研究部"]),
    "tl_contract_review": ("medium", ["法务部"]),
}


FIRST_LAUNCH_DEPARTMENT_TEMPLATES = {
    "content_growth": "dt_content_growth",
    "writing": "official.department.writing",
    "music": "dt_music",
}


class Database:
    def __init__(self, path: str = "curis.sqlite"):
        self.path = path

    def has_model_catalog_rows(self) -> bool:
        """Observe an existing catalog before initialization adds factory rows."""
        path = Path(self.path)
        if not path.exists():
            return False
        connection = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
        try:
            tables = {row[0] for row in connection.execute(
                "select name from sqlite_master where type='table' and name in ('model_gateways','official_models')"
            )}
            return any(connection.execute(f"select 1 from {table} limit 1").fetchone() for table in tables)
        finally:
            connection.close()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def current_tenant(self) -> str:
        """Return the active tenant id resolved from the request/context scope.

        Thin convenience over :class:`TenantContext` so callers that already hold
        a ``Database`` reference do not need a separate import to stamp/filter by
        tenant. ``tenant_context`` has no heavy deps, so there is no import cycle.
        """
        return TenantContext.current_tenant_id()

    def initialize(self, *, seed_model_catalog: bool = True) -> None:
        with self.connect() as connection:
            self._reset_legacy_tasks_table(connection)
            connection.executescript(
                """
                create table if not exists tasks (
                  task_id text primary key,
                  company_id text,
                  project_id text,
                  workspace_id text,
                  work_ref text,
                  execution_ref text,
                  content text not null,
                  status text not null,
                  state_flow text not null default '["INIT"]',
                  prompt text,
                  output text,
                  selected_tool text,
                  cost real not null default 0,
                  error text,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                create table if not exists system_settings (
                  key   text primary key,
                  value text not null,
                  updated_at text not null default current_timestamp
                );

                create table if not exists artifacts (
                  artifact_id   text primary key,
                  tenant_id     text not null,
                  task_id       text not null references tasks(task_id) on delete cascade,
                  title         text not null,
                  artifact_type text not null default 'execution_result',
                  status        text not null default 'generated'
                                check (status in ('generated', 'accepted', 'archived')),
                  content       text not null default '',
                  source_ref    text not null,
                  content_sha256 text not null,
                  created_at    text not null default current_timestamp,
                  updated_at    text not null default current_timestamp,
                  unique (tenant_id, task_id, source_ref)
                );
                create index if not exists idx_artifacts_tenant_task
                  on artifacts(tenant_id, task_id, created_at desc);

                create table if not exists tools (
                  name text primary key,
                  type text not null,
                  description text not null,
                  entry text not null,
                  created_from_template_id text,
                  created_at text not null default current_timestamp
                );

                create table if not exists executions (
                  execution_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  tool_name text not null,
                  prompt text not null,
                  output text not null,
                  cost real not null default 0,
                  created_at text not null default current_timestamp
                );

                create table if not exists tool_traces (
                  trace_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  step_index integer not null,
                  tool_name text not null,
                  input text not null,
                  output text not null default '',
                  error text,
                  timestamp text not null default current_timestamp
                );

                create table if not exists workflows (
                  task_id text primary key references tasks(task_id) on delete cascade,
                  workflow_plan text not null,
                  current_step integer not null default 0,
                  completed_steps text not null default '[]',
                  failed_steps text not null default '[]',
                  status text not null
                );

                create table if not exists auto_workflows (
                  task_id text primary key references tasks(task_id) on delete cascade,
                  generated_steps text not null,
                  status text not null,
                  adaptation_log text not null default '[]'
                );

                create table if not exists workflow_traces (
                  trace_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  step_index integer not null,
                  action text not null,
                  tool_used text not null,
                  input text not null,
                  output text not null default '',
                  timestamp text not null default current_timestamp
                );

                create table if not exists execution_patterns (
                  pattern_id integer primary key autoincrement,
                  task_signature text not null,
                  pattern_type text not null,
                  step_sequence text not null,
                  tool_chain text not null,
                  success_rate real not null default 0,
                  avg_step_count real not null default 0,
                  created_at text not null default current_timestamp
                );

                create table if not exists failure_logs (
                  failure_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  step_index integer not null default 0,
                  tool_name text not null,
                  failure_type text not null,
                  root_cause text not null,
                  correction_strategy text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists tool_performance (
                  tool_name text primary key,
                  success_count integer not null default 0,
                  failure_count integer not null default 0,
                  total_latency_ms real not null default 0,
                  avg_latency_ms real not null default 0,
                  total_cost real not null default 0,
                  priority_weight real not null default 0,
                  updated_at text not null default current_timestamp
                );

                create table if not exists workflow_metrics (
                  metric_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  task_signature text not null,
                  step_count integer not null,
                  status text not null,
                  total_cost real not null default 0,
                  tool_chain text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists execution_scores (
                  score_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  speed_score real not null,
                  correctness_score real not null,
                  efficiency_score real not null,
                  tool_usage_score real not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists development_strategies (
                  strategy_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  development_strategy text not null,
                  detected_inefficiencies text not null default '[]',
                  created_at text not null default current_timestamp
                );

                create table if not exists system_evolution_log (
                  log_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  target_module text not null,
                  optimization_decision text not null,
                  applied_change text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists meta_development_reports (
                  report_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  gap_analysis text not null,
                  planned_issues text not null,
                  verification_plan text not null,
                  source_of_truth_suggestions text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists architecture_locks (
                  lock_id integer primary key autoincrement,
                  module_name text not null unique,
                  reason text not null,
                  locked_by text not null,
                  active integer not null default 1,
                  created_at text not null default current_timestamp
                );

                create table if not exists evolution_simulations (
                  simulation_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  task_flow text not null,
                  tool_routing text not null,
                  workflow_graph text not null,
                  performance_impact text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists evolution_decisions (
                  decision_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  policy text not null,
                  decision text not null,
                  threshold_evaluation text not null,
                  proposal text,
                  risk_analysis text not null,
                  automatic_code_modification_allowed integer not null default 0,
                  created_at text not null default current_timestamp
                );

                create table if not exists rollback_records (
                  rollback_id integer primary key autoincrement,
                  task_id text not null references tasks(task_id) on delete cascade,
                  previous_architecture text not null,
                  stable_version text not null,
                  performance_comparison text not null,
                  created_at text not null default current_timestamp
                );

                create table if not exists evolution_events (
                  event_id integer primary key autoincrement,
                  correlation_id text not null,
                  event_type text not null,
                  payload text not null,
                  created_at text not null default current_timestamp
                );

                -- D1 execute() controlled-gate execution log (scope B). Minimal and
                -- desensitized: only the controlled outcome (status + error category),
                -- tenant id, task type, duration, and token count are stored. No path /
                -- stack / key / request-parameter is ever written to this table.
                create table if not exists d1_execution_log (
                  id integer primary key autoincrement,
                  tenant_id text not null default '',
                  task_type text not null,
                  status text not null,
                  error_category text,
                  duration_ms integer not null default 0,
                  token_count integer not null default 0,
                  created_at text not null default current_timestamp
                );

                -- ADR-0023 D2: 系统级共享部门类型目录（建一次、全员可用）。
                -- 不做 tenant_id 隔离（与 tools 表同层）。仅承载类型定义，不承载
                -- 部门实例；departments 聚合根表本 slice 不创建、不 CRUD。
                create table if not exists department_types (
                  type_key                text primary key,
                  category                text not null,
                  display_name            text not null,
                  description             text,
                  manifest_json           text not null default '{}',
                  manifest_schema_version text not null default '0.0',
                  is_system               integer not null default 1
                );

                -- ADR-0026 D2.impl (issue 056): 部门真实实例化聚合根表。
                -- 单租户：tenant_id 固定 'default'（与 tasks/evolution_events 同层，
                -- 不隔离）。无 FK、无 seed。部门类型为外键语义但本 slice 不强制约束，
                -- 仅由 DepartmentCatalog 在写路径校验 type_key 存在性。
                create table if not exists departments (
                  department_id   text primary key,
                  tenant_id       text not null default 'default',
                  type_key        text not null,
                  display_name    text not null,
                  status          text not null default 'active',
                  created_at      text not null default current_timestamp,
                  updated_at      text not null default current_timestamp
                );

                -- ADR-0017 S1 D1.impl (issue 057): tenants 注册表（additive）。
                -- 仅承载租户身份（tenant_id / name），绝不存储任何凭证/密钥
                -- （安全边界席 review 确认：本 slice 不做真实外部凭证持久化）。
                create table if not exists tenants (
                  tenant_id   text primary key,
                  name        text not null,
                  created_at  text not null default current_timestamp
                );

                create table if not exists tenant_memberships (
                  membership_id text primary key,
                  issuer text not null,
                  subject_id text not null,
                  tenant_id text not null,
                  company_id text not null,
                  ceo_id text,
                  role text not null,
                  status text not null check (status in ('active','revoked','expired')),
                  created_at text not null default current_timestamp,
                  expires_at text,
                  revoked_at text,
                  unique (issuer, subject_id, tenant_id, company_id)
                );
                create index if not exists idx_tenant_memberships_lookup
                  on tenant_memberships(issuer, subject_id, tenant_id, status);

                -- ADR-0017 S2 D3.impl (issue 058): 部门自观测快照 additive 表。
                -- 仅持久化观测快照（指标 + 建议），tenant-scoped（沿用 D1 tenant_id
                -- 作用域语义）。无 FK、无凭证列。默认不写 evolution_events
                -- （ADR-0016 D3 追加写不变式）。
                create table if not exists department_observations (
                  observation_id  text primary key,
                  tenant_id       text not null,
                  type_key        text not null,
                  metrics_json    text not null,
                  suggestion_json text not null,
                  created_at      text not null default current_timestamp
                );

                -- ADR-0017 S3 D4.impl (issue 059): 治理提案 additive 表（提案生命周期
                -- proposed → approved → applied）。tenant/CEO-scoped；无 FK、无凭证列。
                -- 治理事件经 EvolutionEventLog.record 单独留痕（ADR-0016 D3 追加写不变式）。
                create table if not exists governance_proposals (
                  proposal_id      text primary key,
                  tenant_id        text not null,
                  ceo_id           text not null,
                  type_key         text not null,
                  action           text not null,
                  proposed_enabled integer not null default 0,
                  proposed_at      text not null,
                  approved_by      text,
                  approved_at      text,
                  applied_at       text,
                  status           text not null default 'proposed'
                );

                -- ADR-0017 S3 D4.impl (issue 059): 公司部门启用态 additive 表
                -- （CEO 公司级治理落地结果）。tenant/CEO-scoped 持久化部门启用态；
                -- 无 FK、无凭证列。默认不写 evolution_events（治理事件经
                -- EvolutionEventLog.record 单独留痕，保持 ADR-0016 D3 追加写不变式）。
                create table if not exists company_department_state (
                  tenant_id    text not null,
                  ceo_id       text not null,
                  type_key     text not null,
                  enabled      integer not null default 0,
                  approved_by  text,
                  approved_at  text,
                  applied_at   text,
                  primary key (tenant_id, ceo_id, type_key)
                );

                -- ADR-0017 S4 D4.platform (issue 060): 跨公司策略 / 全局护栏 additive 表。
                -- policy_key 唯一（platform 级 guardrail 以 key 维度 upsert）；tenant_scope
                -- 描述适用租户（'all' = 全局护栏，或具体 tenant_id，依赖 S1 D1.impl 租户边界）；
                -- 无 FK、无凭证列。policy_set 经 EvolutionEventLog.record 单独留痕
                -- （ADR-0016 D3 追加写不变式；受控写仅 governance.policy_set）。
                create table if not exists platform_policies (
                  policy_id    text primary key,
                  policy_key   text not null unique,
                  policy_value text not null default '{}',
                  tenant_scope text not null default 'all',
                  enabled      integer not null default 1,
                  updated_at   text not null default current_timestamp
                );

                -- ADR-0017 S4 D4.platform (issue 060): 部门类型启用态 additive 表。
                -- department_types 在 D2 reservation 测试中固定为 7 列（不可改 DDL），
                -- 故「停用/启用」状态单独落库于此 additive 表（type_key 唯一）。停用/
                -- 启用即 upsert 此表；无 FK、无凭证列。仅承载启用态，不影响
                -- department_types 的只读契约列。
                create table if not exists department_type_status (
                  type_key   text primary key,
                  enabled    integer not null default 1,
                  updated_at text not null default current_timestamp
                );

                -- ADR-0028 Phase-2 / issue 066: official model catalog read
                -- model for Workspace. This table stores only catalog metadata:
                -- no API keys, no secrets, no gateway credentials.
                create table if not exists official_models (
                  model_key        text primary key,
                  provider_id      text not null,
                  display_name     text not null,
                  supported_models text not null default '[]',
                  auth_type        text not null default 'apikey',
                  source           text not null default 'official',
                  gateway_ref      text not null default 'newapi',
                  status           text not null default 'active',
                  created_at       text not null default current_timestamp,
                  updated_at       text not null default current_timestamp
                );

                -- ADR-0028 Phase-2 (issue 065): New API gateway config (GatewayConfig,
                -- R-01/R-02). Admin-only metadata; NO api_key / token / secret columns.
                -- credential_ref holds only an opaque 'scheme:reference' string.
                -- Step 5：type 由单值 'newapi' 放开为 N 个 OpenAI 兼容供应商方言。
                -- 本 CHECK 清单必须与 catalog_constants.GATEWAY_TYPE 逐项一致，
                -- 由 test_step5_multi_gateway 的 schema 同步用例守护（不允许漂移）。
                create table if not exists model_gateways (
                  gateway_id      text primary key,
                  name            text not null,
                  type            text not null default 'newapi'
                                    check (type in ('newapi', 'oneapi', 'openai',
                                      'openai_compatible', 'openrouter', 'deepseek',
                                      'moonshot', 'ollama', 'vllm')),
                  base_url        text not null,
                  status          text not null default 'active'
                                    check (status in ('active', 'inactive')),
                  credential_ref  text,
                  default_model   text,
                  created_at      text not null default current_timestamp
                );
                create index if not exists idx_model_gateways_status
                  on model_gateways(status, type);

                -- ADR-0030 / issue 072: Workspace tenant default model
                -- preference. Metadata only; no credential or token fields.
                create table if not exists tenant_model_preferences (
                  tenant_id   text primary key,
                  model_key   text not null,
                  gateway_ref text not null,
                  model_name  text not null,
                  source      text not null default 'official',
                  updated_at  text not null default current_timestamp
                );

                -- Global Assistant v1: tenant-owned presentation identity only.
                -- Business facts, conversations, prompts and credentials do not live here.
                create table if not exists assistant_identities (
                  tenant_id    text primary key,
                  name         text not null default '',
                  avatar       text not null default '',
                  role         text not null default '',
                  tone         text not null default '',
                  personality  text not null default '',
                  updated_at   text not null default current_timestamp
                );

                -- ADR-0032 / issue 083: Workspace tenant department activation.
                -- Metadata only: tenant selects active official department type
                -- references. No department instances, routing, staffing,
                -- permissions, secrets, billing, ROI, prompts, or outputs.
                create table if not exists tenant_department_activations (
                  tenant_id            text not null,
                  department_type_key  text not null,
                  source               text not null default 'official',
                  enabled              integer not null default 1,
                  display_order        integer not null default 0,
                  updated_at           text not null default current_timestamp,
                  primary key (tenant_id, department_type_key)
                );

                -- ADR-0028 Workspace/Admin contract: tenant-private capabilities.
                -- Workspace-owned private model/tool/connector metadata only;
                -- tenant-scoped, no credentials, no official catalog mutation.
                create table if not exists tenant_private_capabilities (
                  tenant_id        text not null,
                  capability_type  text not null
                                   check (capability_type in ('model', 'agent', 'tool', 'connector')),
                  capability_id    text not null,
                  display_name     text not null default '',
                  metadata_json    text not null default '{}',
                  source           text not null default 'tenant_private',
                  status           text not null default 'active',
                  created_at       text not null default current_timestamp,
                  updated_at       text not null default current_timestamp,
                  primary key (tenant_id, capability_type, capability_id)
                );

                -- Phase-5 G2: tenant-private credential metadata only.
                -- Plaintext secrets are never stored here. encrypted_metadata
                -- may contain only non-reversible metadata such as backend and
                -- digest values.
                create table if not exists credential_metadata (
                  credential_id       text primary key,
                  tenant_id           text not null,
                  name                text not null,
                  provider            text not null,
                  credential_type     text not null,
                  credential_ref      text not null,
                  status              text not null default 'active'
                                      check (status in ('active', 'disabled', 'deleted')),
                  encrypted_metadata  text not null default '{}',
                  created_at          text not null default current_timestamp,
                  updated_at          text not null default current_timestamp,
                  disabled_at         text
                );

                -- Phase-3.5: Employee / Department Template contract stubs.
                -- Contract reservation only: no task routing, no employee
                -- execution, no prompt injection, no credentials.
                create table if not exists employee_templates (
                  id                             text primary key,
                  slug                           text not null default '',
                  name                           text not null,
                  role                           text not null,
                  responsibility                 text not null default '',
                  description                    text not null default '',
                  department_type                text not null default '',
                  default_instructions           text not null default '',
                  default_capability_types_json  text not null default '[]',
                  default_model_policy_json      text not null default '{}',
                  default_workflow_step_types_json text not null default '[]',
                  guardrails_json                text not null default '[]',
                  source                         text not null default 'official'
                                                 check (source in ('official', 'tenant_private', 'marketplace')),
                  tenant_id                      text not null default 'platform',
                  enabled                        integer not null default 1,
                  created_at                     text not null default current_timestamp
                );

                create table if not exists employee_instances (
                  id                     text primary key,
                  tenant_id              text not null,
                  company_id             text not null,
                  department_id          text not null,
                  template_id            text not null,
                  created_from_template_id text not null default '',
                  name                   text not null,
                  role                   text not null,
                  avatar_ref             text not null default '',
                  instructions_override  text not null default '',
                  status                 text not null default 'draft',
                  enabled                integer not null default 1,
                  created_at             text not null default current_timestamp
                );

                create table if not exists employee_affiliations (
                  id              text primary key,
                  tenant_id       text not null,
                  employee_id     text not null,
                  department_id   text not null default '',
                  project_id      text not null default '',
                  created_at      text not null default current_timestamp,
                  unique (tenant_id, employee_id, department_id, project_id)
                );
                create index if not exists idx_aff_dept
                  on employee_affiliations(tenant_id, department_id);
                create index if not exists idx_aff_proj
                  on employee_affiliations(tenant_id, project_id);

                create table if not exists schema_migrations (
                  version      integer primary key,
                  name         text not null unique,
                  applied_at   text not null default current_timestamp
                );

                create table if not exists department_templates (
                  id                               text primary key,
                  slug                             text not null default '',
                  name                             text not null,
                  department_type                  text not null,
                  description                      text not null default '',
                  default_employee_templates_json  text not null default '[]',
                  default_workflow_template_id     text,
                  default_capability_types_json    text not null default '[]',
                  source                           text not null default 'official'
                                                   check (source in ('official', 'tenant_private', 'marketplace')),
                  tenant_id                        text not null default 'platform',
                  enabled                          integer not null default 1,
                  created_at                       text not null default current_timestamp
                );

                create table if not exists department_instances (
                  id                              text primary key,
                  tenant_id                       text not null,
                  company_id                      text not null default 'local-demo-company',
                  template_id                     text not null,
                  name                            text not null,
                  department_type                 text not null,
                  manager_employee_id             text,
                  mission                         text not null default '',
                  status                          text not null default 'active'
                                                  check (status in ('draft', 'active', 'disabled', 'archived')),
                  created_from_template_id        text not null default '',
                  enabled_employee_template_ids_json text not null default '[]',
                  enabled                         integer not null default 1,
                  created_at                      text not null default current_timestamp,
                  updated_at                      text not null default current_timestamp
                );

                create table if not exists employee_capability_bindings (
                  id                 text primary key,
                  tenant_id          text not null,
                  employee_id        text not null,
                  employee_template_id text,
                  capability_source  text not null
                                     check (capability_source in ('official', 'tenant_private', 'marketplace')),
                  capability_type    text not null
                                     check (capability_type in ('model', 'agent', 'tool', 'connector')),
                  capability_id      text not null,
                  priority           integer not null default 100,
                  enabled            integer not null default 1,
                  created_at         text not null default current_timestamp,
                  unique (tenant_id, employee_id, capability_source, capability_type, capability_id)
                );

                -- P1（T09）：员工 → official_models 能力组合桥接表。
                -- 与 employee_capability_bindings（skill/tool 绑定）并列、语义区分：
                -- 本表绑定的是 official_models.capability_key（可调用能力组合）。
                -- 复用 tenant_id 隔离（沿用 TenantContext.current_tenant_id()）。
                create table if not exists employee_capabilities (
                  id            integer primary key autoincrement,
                  tenant_id    text not null,
                  employee_id  text not null,
                  capability_key text not null,
                  is_preferred integer not null default 0,
                  sort_order   integer not null default 0,
                  created_at   text not null default current_timestamp,
                  unique (tenant_id, employee_id, capability_key)
                );

                create index if not exists idx_employee_capabilities_tenant
                  on employee_capabilities(tenant_id, employee_id);

                create table if not exists skill_templates (
                  skill_template_id             text primary key,
                  slug                          text not null,
                  name                          text not null,
                  description                   text not null default '',
                  skill_type                    text not null default 'analysis',
                  default_capability_types_json text not null default '["model"]',
                  instruction_excerpt           text not null default '',
                  source                        text not null default 'official'
                                                check (source in ('official', 'tenant_private', 'marketplace')),
                  tenant_id                     text not null default 'platform',
                  status                        text not null default 'active'
                                                check (status in ('draft', 'active', 'disabled', 'archived')),
                  created_from_template_id      text,
                  created_at                    text not null default current_timestamp,
                  updated_at                    text not null default current_timestamp,
                  unique (tenant_id, slug)
                );

                create table if not exists employee_skill_bindings (
                  binding_id                    text primary key,
                  tenant_id                     text not null,
                  employee_id                   text not null,
                  skill_template_id             text not null,
                  capability_binding_ids_json   text not null default '[]',
                  priority                      integer not null default 100,
                  enabled                       integer not null default 1,
                  created_at                    text not null default current_timestamp,
                  unique (tenant_id, employee_id, skill_template_id)
                );

                -- Phase-6: bounded Software R&D workflow runtime.
                -- Sequential-only MVP; tenant-scoped runtime records; no secrets.
                create table if not exists workflow_templates (
                  id            text primary key,
                  name          text not null,
                  description   text not null default '',
                  source        text not null default 'official'
                                check (source in ('official', 'tenant_private', 'marketplace')),
                  tenant_id     text not null default 'platform',
                  department_type text not null default 'software_rnd',
                  process_type  text not null default 'sequential',
                  steps_json    text not null default '[]',
                  status        text not null default 'active',
                  created_at    text not null default current_timestamp,
                  updated_at    text not null default current_timestamp
                );

                create table if not exists workflow_instances (
                  workflow_instance_id text primary key,
                  tenant_id            text not null,
                  company_id           text,
                  project_id           text,
                  workflow_template_id text not null,
                  created_from_template_id text not null default '',
                  name                 text not null,
                  status               text not null default 'active',
                  created_at           text not null default current_timestamp,
                  updated_at           text not null default current_timestamp
                );

                create table if not exists workflow_runs (
                  workflow_run_id      text primary key,
                  tenant_id            text not null,
                  company_id           text,
                  project_id           text,
                  created_from_template_id text not null default '',
                  workflow_instance_id text not null,
                  workflow_template_id text not null,
                  task_id              text not null,
                  department_id        text not null default '',
                  status               text not null default 'pending',
                  final_report         text not null default '',
                  started_at           text,
                  completed_at         text,
                  failed_at            text,
                  created_at           text not null default current_timestamp,
                  updated_at           text not null default current_timestamp
                );

                create table if not exists workflow_steps (
                  workflow_step_id text primary key,
                  tenant_id        text not null,
                  workflow_run_id  text not null,
                  step_order       integer not null,
                  step_type        text not null,
                  step_name        text not null,
                  employee_role    text not null,
                  status           text not null default 'pending',
                  input            text not null default '',
                  output           text not null default '',
                  error            text not null default '',
                  started_at       text,
                  completed_at     text,
                  created_at       text not null default current_timestamp,
                  updated_at       text not null default current_timestamp,
                  unique (tenant_id, workflow_run_id, step_order)
                );

                create table if not exists step_assignments (
                  step_assignment_id text primary key,
                  tenant_id          text not null,
                  workflow_step_id   text not null,
                  employee_id        text not null,
                  employee_role      text not null,
                  capability_binding_id text not null,
                  status             text not null default 'assigned',
                  created_at         text not null default current_timestamp
                );

                create table if not exists step_results (
                  step_result_id  text primary key,
                  tenant_id       text not null,
                  workflow_step_id text not null,
                  employee_id     text not null,
                  result          text not null default '',
                  status          text not null default 'succeeded',
                  created_at      text not null default current_timestamp
                );

                -- Phase-1A: Company is the Workspace product root and Project
                -- is the CEO-facing work container. Task remains an internal
                -- execution substrate and is intentionally not linked here yet.
                create table if not exists companies (
                  company_id                    text primary key,
                  tenant_id                     text not null,
                  ceo_id                        text not null default '',
                  name                          text not null,
                  description                   text not null default '',
                  company_type                  text not null default 'software_rnd_company',
                  status                        text not null default 'active'
                                                check (status in ('draft', 'active', 'disabled', 'archived')),
                  is_default                    integer not null default 0,
                  default_department_ids_json   text not null default '[]',
                  default_project_id            text,
                  created_from_template_id      text,
                  created_at                    text not null default current_timestamp,
                  updated_at                    text not null default current_timestamp
                );

                create unique index if not exists idx_companies_tenant_default
                  on companies(tenant_id) where is_default = 1;
                create index if not exists idx_companies_tenant_status
                  on companies(tenant_id, status);

                create table if not exists projects (
                  project_id                text primary key,
                  tenant_id                 text not null,
                  company_id                text not null,
                  department_id             text,
                  name                      text not null,
                  goal                      text not null,
                  description               text not null default '',
                  project_type              text not null default 'software_development',
                  status                    text not null default 'planned'
                                            check (status in ('planned', 'active', 'blocked', 'completed', 'archived')),
                  owner_employee_id         text,
                  primary_workflow_run_id   text,
                  root_task_id              text,
                  final_report              text not null default '',
                  created_at                text not null default current_timestamp,
                  updated_at                text not null default current_timestamp
                );

                create index if not exists idx_projects_tenant_company_status
                  on projects(tenant_id, company_id, status);

                create table if not exists ai_usage_records (
                  usage_record_id       text primary key,
                  tenant_id             text not null,
                  company_id            text not null,
                  model_gateway_id      text not null,
                  provider_id           text not null,
                  model_name            text not null,
                  input_tokens          integer check (input_tokens is null or input_tokens >= 0),
                  output_tokens         integer check (output_tokens is null or output_tokens >= 0),
                  total_tokens          integer check (total_tokens is null or total_tokens >= 0),
                  cost_amount           numeric check (cost_amount is null or cost_amount >= 0),
                  currency              text not null,
                  cost_source           text not null
                                        check (cost_source in ('unknown', 'estimated', 'provider_reported')),
                  price_version         text,
                  employee_id           text not null,
                  capability_id         text not null,
                  capability_type       text not null
                                        check (capability_type in ('model', 'agent', 'tool', 'connector')),
                  task_id               text not null,
                  project_id            text,
                  department_id         text not null,
                  business_id           text,
                  workspace_id          text,
                  work_ref              text,
                  execution_ref         text,
                  request_id            text not null,
                  execution_status      text not null,
                  metering_status       text not null
                                        check (metering_status in ('confirmed', 'unknown')),
                  occurred_at           text not null,
                  created_at            text not null
                                        default (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                  idempotency_key        text not null unique,
                  cache_read_tokens      integer check (cache_read_tokens is null or cache_read_tokens >= 0),
                  cache_write_tokens     integer check (cache_write_tokens is null or cache_write_tokens >= 0),
                  reasoning_tokens       integer check (reasoning_tokens is null or reasoning_tokens >= 0),
                  latency_ms             integer check (latency_ms is null or latency_ms >= 0),
                  workflow_run_id        text,
                  workflow_step_id       text,
                  capability_binding_id  text,
                  logical_call_id        text,
                  attempt_no             integer check (attempt_no is null or attempt_no >= 1),
                  fallback_from_model    text,
                  fallback_reason        text,
                  http_status            integer check (http_status is null or http_status >= 0),
                  check (
                    (
                      project_id is not null and trim(project_id) != ''
                      and business_id is null and workspace_id is null
                      and work_ref is null and execution_ref is null
                    )
                    or (
                      business_id is not null and trim(business_id) != ''
                      and workspace_id is not null and trim(workspace_id) != ''
                      and work_ref is not null and trim(work_ref) != ''
                      and execution_ref is not null and trim(execution_ref) != ''
                    )
                  )
                );

                create index if not exists idx_ai_usage_tenant_occurred
                  on ai_usage_records(tenant_id, occurred_at desc);
                create index if not exists idx_ai_usage_tenant_project
                  on ai_usage_records(tenant_id, project_id, occurred_at desc);
                create index if not exists idx_ai_usage_tenant_department
                  on ai_usage_records(tenant_id, department_id, occurred_at desc);
                create trigger if not exists ai_usage_records_no_update
                before update on ai_usage_records
                begin
                  select raise(abort, 'ai_usage_records are immutable');
                end;

                create trigger if not exists ai_usage_records_no_delete
                before delete on ai_usage_records
                begin
                  select raise(abort, 'ai_usage_records are immutable');
                end;

                -- MVP Phase 5 / S10: tenant-scoped external knowledge.
                -- Knowledge is source material, not Memory or an execution Artifact.
                create table if not exists knowledge_entries (
                  id             text primary key,
                  tenant_id      text not null,
                  company_id     text,
                  target_type    text,
                  target_ref     text,
                  title          text not null,
                  body           text not null,
                  summary        text not null default '',
                  source_type    text not null default 'manual'
                                 check (source_type in ('manual', 'local_file')),
                  connector_id   text not null default '',
                  source_label   text not null default '',
                  source_path    text not null default '',
                  project_id     text,
                  department_id  text,
                  tags_json      text not null default '[]',
                  content_sha256 text not null,
                  lifecycle_status text not null default 'ACTIVE',
                  archived_at    text,
                  created_by     text not null default '',
                  created_at     text not null default current_timestamp,
                  updated_at     text not null default current_timestamp
                );

                create index if not exists idx_knowledge_entries_tenant_updated
                  on knowledge_entries(tenant_id, updated_at desc);
                create unique index if not exists idx_knowledge_entries_local_source
                  on knowledge_entries(tenant_id, connector_id, source_path)
                  where source_type = 'local_file';

                -- Generic, typed object references. Knowledge is the first
                -- target; the relation remains reusable without becoming a
                -- second Work, Context or Citation system.
                create table if not exists typed_object_references (
                  reference_id  text primary key,
                  tenant_id     text not null,
                  company_id    text not null,
                  workspace_id  text not null default '',
                  source_type   text not null,
                  source_ref    text not null,
                  relation      text not null,
                  target_type   text not null,
                  target_ref    text not null,
                  created_by    text not null default '',
                  created_at    text not null default current_timestamp,
                  unique(tenant_id, source_type, source_ref, relation, target_type, target_ref)
                );
                create index if not exists idx_typed_object_references_source
                  on typed_object_references(tenant_id, source_type, source_ref, relation);
                create index if not exists idx_typed_object_references_target
                  on typed_object_references(tenant_id, target_type, target_ref, relation);

                create trigger if not exists knowledge_entries_referenced_no_delete
                before delete on knowledge_entries
                when exists (
                  select 1 from typed_object_references r
                  where r.tenant_id=old.tenant_id and r.target_type='KNOWLEDGE' and r.target_ref=old.id
                )
                begin
                  select raise(abort, 'referenced knowledge must be archived');
                end;

                -- MVP Phase 6 / S11: confirmed long-term experience.
                -- Memory is not a task log and remains distinct from Knowledge.
                create table if not exists memory_entries (
                  id             text primary key,
                  tenant_id      text not null,
                  memory_type    text not null
                                 check (memory_type in ('user', 'project', 'employee')),
                  memory_level   text not null
                                 check (memory_level in ('user', 'L2', 'L3')),
                  user_id        text not null default '',
                  project_id     text,
                  employee_id    text,
                  title          text not null,
                  content        text not null,
                  summary        text not null default '',
                  tags_json      text not null default '[]',
                  source_type    text not null default 'manual'
                                 check (source_type in ('manual', 'task')),
                  source_task_id text,
                  confidence     real not null default 1.0
                                 check (confidence >= 0 and confidence <= 1),
                  status         text not null default 'active'
                                 check (status in ('active', 'archived')),
                  use_count      integer not null default 0,
                  last_used_at   text,
                  created_by     text not null default '',
                  created_at     text not null default current_timestamp,
                  updated_at     text not null default current_timestamp
                );

                create index if not exists idx_memory_entries_tenant_type_updated
                  on memory_entries(tenant_id, memory_type, updated_at desc);
                create index if not exists idx_memory_entries_project
                  on memory_entries(tenant_id, project_id, status);
                create index if not exists idx_memory_entries_employee
                  on memory_entries(tenant_id, employee_id, status);

                -- One immutable snapshot per build; Task points to the package
                -- actually used by its latest execution attempt.
                create table if not exists context_packages (
                  id                      text primary key,
                  tenant_id               text not null,
                  task_id                 text not null,
                  project_id              text,
                  employee_id             text,
                  task_goal               text not null,
                  current_status          text not null,
                  relevant_memory_json    text not null default '[]',
                  relevant_knowledge_json text not null default '[]',
                  required_tools_json     text not null default '[]',
                  constraints_json        text not null default '[]',
                  output_requirement      text not null,
                  package_sha256          text not null,
                  created_at              text not null default current_timestamp
                );

                create index if not exists idx_context_packages_tenant_task
                  on context_packages(tenant_id, task_id, created_at desc);

                -- Phase-1 Asset Factory Consolidation (Gate C/D/E/F): 新增官方资产
                -- 目录表 + Widget Catalog 单一真相源 + 快照隔离表。全部 additive，
                -- 无 FK、无凭证列；Admin 写 / Workspace 读边界的唯一数据交换面
                -- （admin-workspace-template-boundary 两条铁律的物理落点）。

                -- 公司包（变体 C，聚合包，出目录）：独立 company_packages 表，
                -- 不并入 capability_packages；pricing_reference/quota_reference 仅
                -- 引用 plan_id，不持数值（严禁 cmcf_* 收费路径）。
                create table if not exists company_packages (
                  company_package_id text primary key,
                  name text not null,
                  description text not null default '',
                  version text not null default '1.0.0',
                  status text not null default 'draft'
                                  check (status in ('draft','active','disabled')),
                  source text not null default 'Curis internal',
                  pack text not null check (pack in ('ai_rd','ai_content','ai_commercial')),
                  company_template_ref text,
                  department_template_refs_json text not null default '[]',
                  employee_template_refs_json text not null default '[]',
                  persona_refs_json text not null default '[]',
                  skill_refs_json text not null default '[]',
                  tool_refs_json text not null default '[]',
                  workflow_refs_json text not null default '[]',
                  sub_package_refs_json text not null default '[]',
                  pricing_reference text,
                  quota_reference text,
                  availability text default 'public',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                -- Approved immutable Package -> executable Workflow bridge.
                -- The source workflow-content slot is explicit so package
                -- instantiation never guesses by name/default/latest.
                create table if not exists company_package_workflow_bridges (
                  bridge_id text primary key,
                  company_package_id text not null,
                  package_version text not null,
                  source_workflow_content_id text not null,
                  source_workflow_content_version text not null,
                  workflow_template_id text not null,
                  workflow_template_version text not null,
                  workflow_capability_status text not null
                    check (workflow_capability_status = 'structured_executable'),
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  status text not null default 'active'
                    check (status in ('active','revoked')),
                  created_at text not null default current_timestamp,
                  revoked_at text,
                  unique (
                    company_package_id, package_version,
                    workflow_template_id, workflow_template_version
                  )
                );

                create index if not exists idx_cpw_bridge_resolution
                  on company_package_workflow_bridges(
                    company_package_id, package_version, tenant_id, status
                  );

                -- CompanyTemplate 类型容器（Gate D company-templates，最小 schema）。
                create table if not exists company_templates (
                  company_template_id text primary key,
                  name text not null,
                  company_type text not null default 'ai_rd'
                                   check (company_type in ('ai_rd','ai_content','ai_content_ops','ai_commercial','generic')),
                  description text not null default '',
                  status text not null default 'draft'
                                  check (status in ('draft','active','disabled','archived')),
                  version text not null default '1.0.0',
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                -- PersonaTemplate 内容实例（Variant A，Gate E persona_ref 来源）。
                create table if not exists persona_templates (
                  persona_id text primary key,
                  slug text not null default '',
                  name text not null,
                  archetype text not null
                             check (archetype in ('supportive_coach','direct_executor','analytical_advisor','creative_explorer','balanced_facilitator','risk_aware_guardian')),
                  traits_json text not null default '[]',
                  communication_style_json text not null default '{}',
                  reporting_style_json text not null default '{}',
                  decision_style text not null default 'consultative',
                  collaboration_style_json text not null default '{}',
                  version text not null default '1.0.0',
                  status text not null default 'draft'
                                check (status in ('draft','active','disabled','archived')),
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                -- DashboardTemplate 内容实例（Variant A，dtpl_ 第 8+ 类目录项）。
                -- widget_ids_json 仅存规范 widget_id 引用（单一真相源），不内嵌定义。
                create table if not exists dashboard_templates (
                  dashboard_template_id text primary key,
                  name text not null,
                  company_type text not null default 'ai_rd'
                                   check (company_type in ('ai_rd','ai_content','ai_content_ops','ai_commercial','generic')),
                  role_visibility_json text not null default '["ceo"]',
                  widget_ids_json text not null default '[]',
                  layout_summary text not null default '',
                  data_source_refs_json text not null default '[]',
                  commercial_slot_ref_json text,
                  version text not null default '1.0.0',
                  status text not null default 'draft'
                                check (status in ('draft','active','disabled','archived')),
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                -- Workflow 内容实例（Variant B，wl_* 折叠进 catalog）。
                create table if not exists workflow_contents (
                  workflow_content_id text primary key,
                  name text not null,
                  workflow_template_ref text not null default '',
                  pack text not null default 'ai_rd'
                               check (pack in ('ai_rd','ai_content','ai_commercial')),
                  owner_roles_json text not null default '[]',
                  step_templates_json text not null default '[]',
                  source_attribution text not null default 'Curis internal',
                  version text not null default '1.0.0',
                  status text not null default 'active'
                                check (status in ('draft','active','disabled','archived')),
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1,
                  created_at text not null default current_timestamp,
                  updated_at text not null default current_timestamp
                );

                -- Gate C §2.2 Widget Catalog 单一真相源（Admin 拥有、写入）。
                -- 规范 widget_id 为稳定 snake_case；去重后仅存规范 id
                -- （token_cost→ai_cost / tech_risk→project_risk 别名由服务层归一）。
                create table if not exists dashboard_widget_catalog (
                  widget_id text primary key,
                  domain text not null
                                check (domain in ('company','department','project','employee','cost','value','capability','knowledge')),
                  data_class text,
                  title text not null default '',
                  description text not null default '',
                  source text not null default 'official',
                  tenant_id text not null default 'platform',
                  enabled integer not null default 1
                );

                -- Gate F / template-versioning-policy §5 快照隔离桶。
                -- follow_latest 默认 0（false）：升级单向向前，不影响已存在实例。
                create table if not exists template_version_snapshots (
                  id text primary key,
                  instance_id text not null,
                  template_type text not null,
                  template_id text not null,
                  snapshot_version text not null,
                  snapshot_metadata_json text not null default '{}',
                  snapshot_at text not null default current_timestamp,
                  follow_latest integer not null default 0
                );

                create index if not exists idx_tvs_instance
                  on template_version_snapshots(instance_id);
                create index if not exists idx_tvs_template
                  on template_version_snapshots(template_type, template_id);
                """
            )
            self._ensure_column(connection, "tasks", "selected_tool", "text")
            self._ensure_column(connection, "tasks", "output", "text")
            self._ensure_column(connection, "tasks", "requested_capability_source", "text")
            self._ensure_column(connection, "tasks", "requested_capability_type", "text")
            self._ensure_column(connection, "tasks", "requested_capability_id", "text")
            self._ensure_column(connection, "tasks", "employee_id", "text")
            self._ensure_column(connection, "tasks", "employee_role", "text")
            self._ensure_column(connection, "tasks", "employee_name", "text")
            self._ensure_column(connection, "tasks", "company_id", "text")
            self._ensure_column(connection, "tasks", "project_id", "text")
            self._ensure_column(connection, "tasks", "workspace_id", "text")
            self._ensure_column(connection, "tasks", "work_ref", "text")
            self._ensure_column(connection, "tasks", "execution_ref", "text")
            self._migrate_task_execution_scope(connection)
            self._ensure_column(connection, "tasks", "context_package_id", "text")
            self._ensure_column(connection, "tasks", "current_execution_step", "text not null default ''")
            self._ensure_column(connection, "tasks", "pending_question", "text not null default ''")
            self._ensure_column(connection, "tasks", "execution_context_summary", "text not null default ''")
            self._ensure_column(connection, "tasks", "handoff_assignee_id", "text not null default ''")
            self._ensure_column(connection, "tasks", "resume_parameters_json", "text not null default '{}'")
            self._ensure_column(connection, "tasks", "execution_state_changed_at", "text")
            self._ensure_column(connection, "knowledge_entries", "company_id", "text")
            self._ensure_column(connection, "knowledge_entries", "target_type", "text")
            self._ensure_column(connection, "knowledge_entries", "target_ref", "text")
            self._ensure_column(
                connection,
                "knowledge_entries",
                "lifecycle_status",
                "text not null default 'ACTIVE'",
            )
            self._ensure_column(connection, "knowledge_entries", "archived_at", "text")
            connection.execute(
                "create index if not exists idx_knowledge_entries_canonical_target "
                "on knowledge_entries(tenant_id, company_id, target_type, target_ref, lifecycle_status, updated_at desc)"
            )
            connection.execute(
                "update tasks set execution_state_changed_at = current_timestamp "
                "where execution_state_changed_at is null"
            )
            self._ensure_column(connection, "tools", "created_from_template_id", "text")
            self._ensure_column(connection, "executions", "tool_name", "text not null default ''")
            # ADR-0022 D1: reserve tenant scope on the two concrete aggregate
            # roots (Task, EvolutionLog). Additive, backfills existing rows to
            # the single-tenant sentinel. No read/write scoping yet.
            self._ensure_column(connection, "tasks", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "evolution_events", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "evolution_events", "idempotency_key", "text")
            self._ensure_column(connection, "tenant_memberships", "ceo_id", "text")
            self._ensure_column(
                connection,
                "credential_metadata",
                "account_id",
                "text not null default ''",
            )

            # ADR-0017 S1 D1.impl (issue 057): extend tenant scoping to every
            # task/execution aggregate root so reads can be filtered by tenant.
            # Additive + idempotent: backfills existing rows to the single-tenant
            # sentinel. The tenants registry is seeded with the default tenant.
            self._ensure_column(connection, "executions", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "tool_traces", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "workflows", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "auto_workflows", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "workflow_traces", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "meta_development_reports", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "evolution_decisions", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "evolution_simulations", "tenant_id", "text not null default 'selfuse'")
            self._ensure_column(connection, "rollback_records", "tenant_id", "text not null default 'selfuse'")

            # ADR-0017 S1 D1.impl (issue 063): additive extension of tenants
            # table for Admin platform management. plan_tier/contact_email/status/
            # description are metadata-only (zero credential columns).
            # Idempotent backfill for existing rows.
            self._ensure_column(connection, "tenants", "plan_tier", "text default 'free'")
            self._ensure_column(connection, "tenants", "contact_email", "text default ''")
            self._ensure_column(connection, "tenants", "status", "text default 'active'")
            self._ensure_column(connection, "tenants", "description", "text default ''")
            connection.execute(
                "update tenants set plan_tier = 'free' "
                "where plan_tier is null or plan_tier = ''"
            )
            connection.execute(
                "update tenants set status = 'active' "
                "where status is null or status = ''"
            )

            # ADR-0028 Phase-2 (issue 065): additive default_model column on
            # official_models so each catalog entry can carry its gateway-side
            # default model name. Backwards compatible with existing rows.
            self._ensure_column(connection, "official_models", "default_model", "text")

            # ADR-0028 Phase-2 (issue 070/071): additive `type` / `name` columns
            # on official_models so the single table can carry model / tool /
            # connector capabilities (unified "official capability catalog").
            # `type` defaults to 'model' so all pre-existing model rows stay
            # classified as models; `name` defaults to '' and is backfilled to
            # model_key for those rows. Both are additive + idempotent so
            # initialize() stays re-runnable against old or new databases.
            existing_model_columns = {row["name"] for row in connection.execute("pragma table_info(official_models)")}
            self._ensure_column(
                connection, "official_models", "type", "text not null default 'model'"
            )
            self._ensure_column(
                connection, "official_models", "name", "text not null default ''"
            )
            # P0 后端核心：official_models 增加 runtime_meta_json 列，承载能力运行态
            # 元数据（cost / permissions / io_schema / backup_chain / live_status /
            # credentials_ref）。additive + 幂等，向后兼容既有 model 行（无则 NULL，
            # 读取时按 {} 处理）。resolver 据此做可用性探活 + 降级链选路。
            self._ensure_column(
                connection, "official_models", "runtime_meta_json", "text"
            )
            # P0 后端核心：经验沉淀表 capability_lessons（租户隔离 + 复用既有范式）。
            # 持久化成功路径 / 失败原因 / 有效降级链，供后续任务检索复用（lesson_memory）。
            connection.execute(
                """
                create table if not exists capability_lessons (
                  lesson_id      integer primary key autoincrement,
                  tenant_id     text not null,
                  signature     text not null,
                  cap_path_json text not null default '[]',
                  outcome       text not null default 'unknown',
                  reason        text not null default '',
                  reused_count  integer not null default 0,
                  created_at    text not null default current_timestamp
                )
                """
            )
            connection.execute(
                "create index if not exists idx_capability_lessons_signature "
                "on capability_lessons(tenant_id, signature)"
            )
            # P0 后端核心：projects 增加 progress_json 列（additive，复用既有表结构，
            # 不新建表）。project_state 聚合进度/健康/成本后写回此处。
            self._ensure_column(
                connection, "projects", "progress_json",
                "text not null default '{}'",
            )
            self._ensure_column(connection, "employee_templates", "slug", "text not null default ''")
            self._ensure_column(connection, "employee_templates", "responsibility", "text not null default ''")
            self._ensure_column(
                connection,
                "employee_templates",
                "default_workflow_step_types_json",
                "text not null default '[]'",
            )
            self._ensure_column(connection, "employee_templates", "guardrails_json", "text not null default '[]'")
            # Phase-1 Gate E: Employee 注入扩展字段（persona_ref / default_skill /
            # default_tool / persona_overrides + 模板类 status/version/updated_at）。
            # additive + idempotent，向后兼容既有 official.* 种子行（不重命名）。
            self._ensure_column(connection, "employee_templates", "persona_ref", "text not null default ''")
            self._ensure_column(connection, "employee_templates", "default_skill", "text not null default ''")
            self._ensure_column(connection, "employee_templates", "default_tool", "text not null default ''")
            self._ensure_column(connection, "employee_templates", "persona_overrides_json", "text not null default '{}'")
            # V2 P0/P1（总控已批准自主推进；降级执行：框架故障期主理人直落，待架构师/QA 复核）。
            # P1-1：Persona「形象」字段（头像/昵称/身份描述）；不立新资产类（规避 L2 #7）。
            self._ensure_column(connection, "persona_templates", "image_ref_json", "text not null default '{}'")
            # P1-2：Skill 四件套之版本 + 分类（生命周期已由 status 覆盖）。
            self._ensure_column(connection, "skill_templates", "version", "text not null default '1.0.0'")
            self._ensure_column(connection, "skill_templates", "category", "text not null default ''")
            self._ensure_column(connection, "employee_templates", "version", "text not null default '1.0.0'")
            self._ensure_column(connection, "employee_templates", "status", "text not null default 'draft'")
            self._ensure_column(connection, "employee_templates", "updated_at", "text not null default current_timestamp")
            self._ensure_column(connection, "employee_instances", "persona_ref", "text not null default ''")
            self._ensure_column(connection, "employee_instances", "default_skill", "text not null default ''")
            self._ensure_column(connection, "employee_instances", "default_tool", "text not null default ''")
            self._ensure_column(connection, "employee_instances", "avatar_ref", "text not null default ''")
            self._ensure_column(connection, "department_templates", "slug", "text not null default ''")
            self._ensure_column(connection, "department_templates", "default_workflow_template_id", "text")
            self._ensure_column(
                connection,
                "department_templates",
                "version",
                "text not null default '1.0.0'",
            )
            self._ensure_column(
                connection,
                "department_templates",
                "status",
                "text not null default 'active'",
            )
            self._ensure_column(
                connection,
                "department_templates",
                "default_capability_types_json",
                "text not null default '[]'",
            )
            self._ensure_column(connection, "employee_capability_bindings", "employee_template_id", "text")
            self._ensure_column(connection, "employee_capability_bindings", "created_at", "text")
            self._ensure_column(connection, "employee_instances", "created_from_template_id", "text not null default ''")
            self._ensure_column(connection, "department_instances", "manager_employee_id", "text")
            self._ensure_column(connection, "department_instances", "mission", "text not null default ''")
            self._ensure_column(connection, "department_instances", "status", "text not null default 'active'")
            self._ensure_column(connection, "department_instances", "created_from_template_id", "text not null default ''")
            self._ensure_column(connection, "workflow_templates", "department_type", "text not null default 'software_rnd'")
            self._ensure_column(connection, "workflow_templates", "process_type", "text not null default 'sequential'")
            self._ensure_column(connection, "workflow_templates", "tenant_id", "text not null default 'platform'")
            self._ensure_column(connection, "workflow_templates", "version", "text not null default '1.0.0'")
            self._ensure_column(connection, "workflow_instances", "company_id", "text")
            self._ensure_column(connection, "workflow_instances", "project_id", "text")
            self._ensure_column(connection, "workflow_instances", "created_from_template_id", "text not null default ''")
            self._ensure_column(connection, "workflow_instances", "source_company_package_id", "text")
            self._ensure_column(connection, "workflow_instances", "source_package_version", "text")
            self._ensure_column(connection, "workflow_instances", "source_bridge_id", "text")
            self._ensure_column(connection, "workflow_instances", "source_workflow_template_id", "text")
            self._ensure_column(connection, "workflow_instances", "source_workflow_template_version", "text")
            self._ensure_column(connection, "workflow_runs", "department_id", "text not null default ''")
            self._ensure_column(connection, "workflow_runs", "final_report", "text not null default ''")
            self._ensure_column(connection, "workflow_runs", "company_id", "text")
            self._ensure_column(connection, "workflow_runs", "project_id", "text")
            self._ensure_column(connection, "workflow_runs", "created_from_template_id", "text not null default ''")
            self._ensure_column(connection, "workflow_runs", "source_company_package_id", "text")
            self._ensure_column(connection, "workflow_runs", "source_package_version", "text")
            self._ensure_column(connection, "workflow_runs", "source_bridge_id", "text")
            self._ensure_column(connection, "workflow_runs", "source_workflow_template_id", "text")
            self._ensure_column(connection, "workflow_runs", "source_workflow_template_version", "text")
            self._ensure_column(connection, "companies", "created_from_template_id", "text")
            self._ensure_column(connection, "companies", "source_company_package_id", "text")
            self._ensure_column(connection, "companies", "source_package_version", "text")
            self._ensure_column(connection, "companies", "source_bridge_id", "text")
            self._ensure_column(connection, "companies", "source_workflow_template_id", "text")
            self._ensure_column(connection, "companies", "source_workflow_template_version", "text")
            self._ensure_column(connection, "strategy_meetings", "company_id", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "business_id", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "workspace_id", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "background", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "leader_employee_id", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "ceo_participation_mode", "text not null default 'DECISION_ONLY'")
            self._ensure_column(connection, "strategy_meetings", "conversation_id", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "context_refs", "text not null default '[]'")
            self._ensure_column(connection, "strategy_meetings", "decision_ref", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "work_refs", "text not null default '[]'")
            self._ensure_column(connection, "strategy_meetings", "result_refs", "text not null default '[]'")
            self._ensure_column(connection, "strategy_meetings", "continuation_gap", "text not null default ''")
            self._ensure_column(connection, "strategy_meetings", "orchestration_json", "text not null default '{}'")
            self._ensure_column(connection, "strategy_meetings", "closed_at", "text")
            connection.execute(
                "update employee_instances set created_from_template_id = template_id "
                "where created_from_template_id is null or created_from_template_id = ''"
            )
            connection.execute(
                "update department_instances set created_from_template_id = template_id "
                "where created_from_template_id is null or created_from_template_id = ''"
            )
            # Idempotent backfill for rows created before this column existed.
            if "type" not in existing_model_columns:
                connection.execute(
                    "update official_models set type = 'model' "
                    "where type is null or type = ''"
                )
            if "name" not in existing_model_columns:
                connection.execute(
                    "update official_models set name = model_key "
                    "where name is null or name = ''"
                )
            connection.execute(
                "create index if not exists idx_official_models_type_status "
                "on official_models(type, status)"
            )

            # Idempotent seed: the default tenant always exists (no credentials).
            connection.execute(
                "insert or ignore into tenants (tenant_id, name) values (?, ?)",
                (DEFAULT_TENANT, "Default Tenant"),
            )

            # ADR-0023 D2: reserve the system-level department type catalog.
            # Additive, idempotent seed of the minimal canonical type set.
            # No read/write scoping; no department instantiation yet.
            self._seed_department_catalog(connection)
            if seed_model_catalog:
                self._seed_model_gateway(connection)
                self._seed_official_model_catalog(connection)
            existing_workflow_ids = {row[0] for row in connection.execute("select id from workflow_templates")}
            self._seed_employee_template_contract(connection)
            self._seed_skill_runtime_contract(connection)
            self._seed_workflow_runtime_contract(connection)
            # Phase-1 Asset Factory Consolidation (Gate C/D/E/F)：官方资产工厂内容
            # 种子（persona_templates / employee_templates(et_*) / department_templates(dt_*) /
            # company_templates(ct_*) / dashboard_templates(dtpl_*) / workflow_contents(wl_*) /
            # dashboard_widget_catalog / company_packages(ccp_*)）。幂等，可重复 initialize。
            self._seed_phase1_asset_factory(connection)
            # V2 P0/P1（降级执行）：补齐 ai_rd 线 Skill/Tool/Workflow 真实内容 + Persona 形象。
            self._seed_tool_templates(connection)
            # ── P1-1 起点（必须在 _seed_tool_templates 之后；否则 tool_templates 表尚不存在，_ensure_column 静默跳过）──
            self._ensure_column(
                connection,
                "tool_templates",
                "security_level",
                "TEXT NOT NULL DEFAULT 'low' CHECK(security_level IN ('high','medium','low'))",
            )
            self._ensure_column(
                connection,
                "tool_templates",
                "applicable_departments_json",
                "TEXT NOT NULL DEFAULT '[]'",
            )
            # ── R2 item7：Tool 能力态标记（C），幂等 _ensure_column 范式 ──
            # catalog_visible：目录可见（默认 1）；configured：凭证/环境变量就绪（默认 0）；
            # executable：可真实执行（默认 0）；mock_or_stub：Mock/Stub 占位（默认 1）。
            # 不变量：executable 与 mock_or_stub 互斥（NOT 同时为真）。当前全库默认
            # 「目录可见 + Mock/Stub、未配置未执行」，真实执行能力留作 L2 后钩子，不伪造。
            # enabled：对齐其它目录表（persona/dashboard/company/department），使只读投影
            # 助手 _list_catalog_rows 可统一选取（tool_templates 基线建表漏了该列）。
            self._ensure_column(
                connection, "tool_templates", "enabled",
                "INTEGER NOT NULL DEFAULT 1",
            )
            self._ensure_column(
                connection, "tool_templates", "catalog_visible",
                "INTEGER NOT NULL DEFAULT 1",
            )
            self._ensure_column(
                connection, "tool_templates", "configured",
                "INTEGER NOT NULL DEFAULT 0",
            )
            self._ensure_column(
                connection, "tool_templates", "executable",
                "INTEGER NOT NULL DEFAULT 0",
            )
            self._ensure_column(
                connection, "tool_templates", "mock_or_stub",
                "INTEGER NOT NULL DEFAULT 1",
            )
            self._annotate_tool_capability(connection)
            self._backfill_tool_security(connection)
            # ── P1-1 结束 ──
            self._seed_skill_templates_airnd(connection)
            self._seed_workflow_template_containers(connection)
            # ── P0-①: 研发部真实化：devops_engineer + wt_rd_pipeline + dt_rd_department ──
            self._seed_devops_engineer(connection)
            self._seed_rd_pipeline_workflow(connection)
            self._seed_rd_department(connection)
            # ── R2 item8：Workflow 能力态标记（D），幂等 _ensure_column 范式 ──
            # workflow_capability_status：structured_executable / design_only /
            # instantiation_forbidden（默认 design_only）。与生命周期态 status 区分。
            # enabled：对齐其它目录表（基线建表漏了该列），供只读投影助手统一选取。
            self._ensure_column(
                connection,
                "workflow_templates",
                "enabled",
                "INTEGER NOT NULL DEFAULT 1",
            )
            self._ensure_column(
                connection,
                "workflow_templates",
                "workflow_capability_status",
                "TEXT NOT NULL DEFAULT 'design_only' "
                "CHECK (workflow_capability_status IN "
                "('structured_executable','design_only','instantiation_forbidden'))",
            )
            self._annotate_workflow_capability(connection, existing_workflow_ids)
            self._seed_company_package_workflow_bridges(connection)
            self._seed_persona_image_refs(connection)

            # ── Workspace 员工目录 v1：employee_instances / department_instances 软删除列 ──
            self._ensure_column(connection, "employee_instances", "deleted_at", "text")
            self._ensure_column(connection, "department_instances", "deleted_at", "text")
            self._reconcile_legacy_orphan_instances(connection)
            self._migrate_projects_to_business_departments(connection)
            self._migrate_completed_task_artifacts(connection)
            self._migrate_model_gateways_multi_type(connection)
            self._migrate_capability_type_check_agent(connection)
            self._migrate_usage_attribution(connection)
            self._migrate_conversation_usage(connection)
            self._migrate_execution_scope_usage(connection)
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_company "
                "on ai_usage_records(tenant_id, company_id, occurred_at desc)"
            )
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_workspace "
                "on ai_usage_records(tenant_id, workspace_id, occurred_at desc)"
            )
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_work "
                "on ai_usage_records(tenant_id, work_ref, occurred_at desc)"
            )
            self._migrate_guide_sessions(connection)
            self._migrate_business_metrics(connection)
            self._migrate_runtime_trace_event(connection)
            self._migrate_position_authorization(connection)
            self._migrate_capability_ownership(connection)
            from .runtime.models import ensure_runtime_foundation_schema
            ensure_runtime_foundation_schema(connection)

            # ── Phase-8 Billing MVP (issue P8): 三张一等实体表 + 三档默认 Plan 幂等 seed ──
            # 不与任何 Workspace 表耦合；仅聚合读 usage_event/employee_instances/
            # workflow_runs（只读），零写。不修改 tenants 表结构（plan_id 留作 G1 后 additive）。
            connection.executescript(
                """
                create table if not exists plans (
                  plan_id           text primary key,
                  plan_code         text not null unique,
                  name              text not null,
                  tier              text not null check (tier in ('free','pro','enterprise')),
                  status            text not null default 'draft'
                                      check (status in ('draft','active','deprecated','archived')),
                  version           text not null default '1.0.0',
                  billing_interval  text not null default 'monthly'
                                      check (billing_interval in ('monthly','annual','custom')),
                  features_json     text not null default '[]',
                  quota_rules_json  text not null default '{}',
                  created_at        text not null default current_timestamp,
                  updated_at        text not null default current_timestamp
                );
                create index if not exists idx_plans_code on plans(plan_code);

                create table if not exists quotas (
                  quota_id        text primary key,
                  tenant_id       text not null,
                  plan_id         text not null,
                  plan_code       text not null default 'free',
                  quota_type      text not null
                                    check (quota_type in ('token','employee_seat','capability','workflow')),
                  limit_value     integer not null default 0,
                  is_unlimited    integer not null default 0,
                  current_usage   integer not null default 0,
                  period          text not null default 'monthly',
                  period_start    text not null default '',
                  period_end      text not null default '',
                  source_scope_json text not null default '[]',
                  status          text not null default 'active'
                                    check (status in ('active','exceeded','paused')),
                  created_at      text not null default current_timestamp,
                  updated_at      text not null default current_timestamp
                );
                create index if not exists idx_quotas_tenant on quotas(tenant_id, quota_type, period_start);

                create table if not exists billing_events (
                  billing_event_id text primary key,
                  tenant_id        text not null,
                  plan_id          text not null,
                  plan_code        text not null default 'free',
                  subject_type     text not null,
                  subject_id       text not null default '',
                  amount           real not null default 0,
                  currency         text not null default 'USD',
                  status           text not null default 'draft'
                                    check (status in ('draft','calculated','issued')),
                  period_start     text not null default '',
                  period_end       text not null default '',
                  breakdown_json   text not null default '{}',
                  created_at       text not null default current_timestamp,
                  updated_at       text not null default current_timestamp
                );
                create index if not exists idx_billing_events_tenant_period
                  on billing_events(tenant_id, period_start);
                """
            )
            # ── Phase-9A 迁移：quotas 新增 is_unlimited（additive，兼容既有库）──
            with connection:
                cols = {r["name"] for r in connection.execute("pragma table_info(quotas)")}
                if "is_unlimited" not in cols:
                    connection.execute("alter table quotas add column is_unlimited integer not null default 0")
                # 修正既有库中旧 seed（无 quota_mode 即旧版）：Enterprise 不再 0=无限、Pro 价格占位
                legacy_free = '{"token_monthly_limit":1000000,"seat_limit":3,"capability_sources":["official"],"workflow_monthly_limit":0,"overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},"currency":"USD"}'
                new_free = '{"quota_mode":"plan_default","is_unlimited":false,"token_monthly_limit":1000000,"seat_limit":3,"capability_sources":["official"],"workflow_monthly_limit":0,"overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},"currency":"USD"}'
                new_pro = '{"quota_mode":"plan_default","is_unlimited":false,"token_monthly_limit":50000000,"seat_limit":15,"capability_sources":["official","tenant_private"],"workflow_monthly_limit":50000,"overage":{"token_unit_price_per_1k":null,"seat_unit_price":null,"workflow_unit_price":null,"capability_unit_price":null},"currency":"USD"}'
                new_ent = '{"quota_mode":"custom","is_unlimited":false,"token_monthly_limit":null,"seat_limit":null,"capability_sources":["official","tenant_private","marketplace"],"workflow_monthly_limit":null,"overage":{"token_unit_price_per_1k":null,"seat_unit_price":null,"workflow_unit_price":null,"capability_unit_price":null},"currency":"USD"}'
                connection.execute("update plans set quota_rules_json = ? where plan_id = 'plan_free' and quota_rules_json not like '%quota_mode%'", (new_free,))
                connection.execute("update plans set quota_rules_json = ? where plan_id = 'plan_pro' and quota_rules_json not like '%quota_mode%'", (new_pro,))
                connection.execute("update plans set quota_rules_json = ? where plan_id = 'plan_enterprise' and quota_rules_json not like '%quota_mode%'", (new_ent,))

            # 幂等 seed 三档默认 Plan（plan_code = free/pro/enterprise，与 tenants.plan_tier 1:1 对齐）。
            # 已存在则 insert or ignore 跳过（seed 可重复执行）。
            # Phase-9A：quota_rules 新增 quota_mode/is_unlimited；Enterprise=custom（limit 由 Admin 按企业配置，不固定无限）；
            # Pro 超量单价占位 null（由总控决策席后续配置 $XX，非写死真实价格）。
            existing_plan_ids = {row[0] for row in connection.execute("select plan_id from plans")}
            connection.execute(
                """
                insert or ignore into plans
                  (plan_id, plan_code, name, tier, status, version, billing_interval, features_json, quota_rules_json)
                values
                  -- Free：plan_default，固定默认上限；超量价 0（免费档，真实 0）
                  ('plan_free', 'free', 'Free', 'free', 'active', '1.0.0', 'monthly', '["task_execution","tenant_private_capabilities"]',
                   '{"quota_mode":"plan_default","is_unlimited":false,"token_monthly_limit":1000000,"seat_limit":3,"capability_sources":["official"],"workflow_monthly_limit":0,"overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},"currency":"USD"}'),
                  -- Pro：plan_default；超量单价占位为 null（由总控决策席后续配置 $XX，非写死真实价格）
                  ('plan_pro', 'pro', 'Pro', 'pro', 'active', '1.0.0', 'monthly', '["task_execution","workflow_sop","tenant_private_capabilities","admin_usage_observability"]',
                   '{"quota_mode":"plan_default","is_unlimited":false,"token_monthly_limit":50000000,"seat_limit":15,"capability_sources":["official","tenant_private"],"workflow_monthly_limit":50000,"overage":{"token_unit_price_per_1k":null,"seat_unit_price":null,"workflow_unit_price":null,"capability_unit_price":null},"currency":"USD"}'),
                  -- Enterprise：custom quota（自定义配额，不固定为无限）；limit 留 null 待 Admin 按企业单独设置
                  ('plan_enterprise', 'enterprise', 'Enterprise', 'enterprise', 'active', '1.0.0', 'annual', '["task_execution","workflow_sop","tenant_private_capabilities","admin_usage_observability","team_management","priority_support"]',
                   '{"quota_mode":"custom","is_unlimited":false,"token_monthly_limit":null,"seat_limit":null,"capability_sources":["official","tenant_private","marketplace"],"workflow_monthly_limit":null,"overage":{"token_unit_price_per_1k":null,"seat_unit_price":null,"workflow_unit_price":null,"capability_unit_price":null},"currency":"USD"}');
                """
            )

            # ── Phase-9A P0：plans 新增订阅价镜像列（additive，兼容既有库）──
            # 仅展示/镜像，由 active pricing rule 派生写入；绝不作为价格权威。
            # 与 §0 的 is_unlimited 迁移使用完全相同的 pragma 探测 + alter 模式。
            with connection:
                plan_cols = {r["name"] for r in connection.execute("pragma table_info(plans)")}
                if "price" not in plan_cols:
                    connection.execute("alter table plans add column price real")
                if "price_currency" not in plan_cols:
                    connection.execute("alter table plans add column price_currency text")
                if "billing_cycle" not in plan_cols:
                    connection.execute("alter table plans add column billing_cycle text")

            # ── Phase-9A P0：pricing_rules 表（订阅价格权威来源）──
            # 与 plans / quotas / billing_events 同区；create table if not exists 保证幂等。
            # subject_type CHECK 预置 5 类（含未来 capability/employee/connector/template），
            # 本 Issue 仅写入 subscription，未来 Issue 无需再 ALTER。
            connection.executescript(
                """
                create table if not exists pricing_rules (
                  pricing_rule_id  text primary key,
                  subject_type     text not null
                                    check (subject_type in
                                      ('subscription','capability','employee','connector','template')),
                  pricing_type     text not null
                                    check (pricing_type in ('fixed','discount','override')),
                  plan_id          text not null,
                  amount           real not null default 0,
                  currency         text not null default 'USD',
                  billing_cycle    text not null default 'month'
                                    check (billing_cycle in ('month','year','one_time')),
                  effective_start  text not null,
                  effective_end    text,
                  status           text not null default 'draft'
                                    check (status in ('draft','active','expired','disabled')),
                  created_at       text not null default current_timestamp,
                  updated_at       text not null default current_timestamp
                );

                create index if not exists idx_pricing_rules_plan_status
                  on pricing_rules(plan_id, status);
                create index if not exists idx_pricing_rules_subject
                  on pricing_rules(subject_type);
                """
            )

            # ── Phase-9A P0：默认订阅价规则（idempotent insert or ignore）──
            # Free：固定价 0 USD/月，已生效，无结束（过去日期起生效）
            connection.execute(
                "insert or ignore into pricing_rules "
                "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
                " billing_cycle, effective_start, effective_end, status) "
                "values ('pr_default_free', 'subscription', 'fixed', 'plan_free', 0, 'USD', "
                " 'month', '2024-01-01T00:00:00Z', NULL, 'active')"
            )
            # Pro：固定价 99 USD/月，已生效（用户示例 $99/month）
            connection.execute(
                "insert or ignore into pricing_rules "
                "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, currency, "
                " billing_cycle, effective_start, effective_end, status) "
                "values ('pr_default_pro', 'subscription', 'fixed', 'plan_pro', 99, 'USD', "
                " 'month', '2024-01-01T00:00:00Z', NULL, 'active')"
            )
            # Enterprise：本 Issue 不设默认订阅价规则（Enterprise 为 custom 定价，
            #   未来由 TenantPricingPolicy 处理）。文档注明，不插入 subscription 规则。

            # 同步将 Free/Pro 的镜像写入 plans.price/price_currency/billing_cycle（仅展示用）
            if "plan_free" not in existing_plan_ids:
                connection.execute(
                    "update plans set price=0, price_currency='USD', billing_cycle='month', "
                    "updated_at=current_timestamp where plan_id='plan_free'"
                )
            if "plan_pro" not in existing_plan_ids:
                connection.execute(
                    "update plans set price=99, price_currency='USD', billing_cycle='month', "
                    "updated_at=current_timestamp where plan_id='plan_pro'"
                )

            # ── Phase-9A P1：quota_rules 表（计划级配额权威来源）──
            # 与 plans / quotas / pricing_rules 同区；create table if not exists 保证幂等。
            # quota_type CHECK 预置 5 类（含 connector_limit），未来无需再 ALTER。
            # 部分唯一索引强制「每 (plan_id, quota_type) 仅一条 active」，历史草稿/停用
            # 记录可并存（新覆盖旧，不物理删除，与 pricing_rules 一致）。
            connection.executescript(
                """
                create table if not exists quota_rules (
                  quota_rule_id     text primary key,
                  plan_id           text not null,
                  quota_type        text not null
                                     check (quota_type in
                                       ('token_limit','employee_seat_limit','workflow_limit',
                                        'capability_limit','connector_limit')),
                  limit_value       integer,                       -- NULL = 不限（配合 is_unlimited）
                  is_unlimited      integer not null default 0,   -- 0/1
                  period            text not null default 'monthly'
                                     check (period in ('daily','monthly','annual','none')),
                  enforcement_mode  text not null default 'notify'
                                     check (enforcement_mode in ('notify','throttle','block','billing_only')),
                  status            text not null default 'draft'
                                     check (status in ('draft','active','disabled')),
                  source_scope_json text not null default '[]',   -- 准入型专用白名单，数值型恒 '[]'
                  created_at        text not null default current_timestamp,
                  updated_at        text not null default current_timestamp
                );

                -- 每 (plan_id, quota_type) 仅一条 active（部分唯一索引，DB 层强制）
                create unique index if not exists idx_quota_rules_plan_type_active
                  on quota_rules(plan_id, quota_type) where status = 'active';

                -- 列表/按 plan 查询加速
                create index if not exists idx_quota_rules_plan on quota_rules(plan_id);
                create index if not exists idx_quota_rules_status on quota_rules(status);
                """
            )

            # ── Phase-9A P1：默认配额规则 seed（三档各 5 类，active，占位可被 Admin 改写）──
            # insert or ignore：已存在则跳过，可重复执行；部分唯一索引保证每 plan+type 仅一条 active。
            # 上表数值为合理占位（非真实业务数值）：Free/Pro 数值型为示例上限；
            # Enterprise 为 custom（limit_value=NULL + is_unlimited=1，Admin 按企业改写）。
            # 全部须经 Admin API 可改；无一处写死为不可改。
            _SEED_QUOTA_RULES = [
                # (quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, period, enforcement_mode, status, source_scope_json)
                # ── Free ──
                ("qr_free_token",       "plan_free", "token_limit",        1000000, 0, "monthly", "notify", "active", "[]"),
                ("qr_free_seat",        "plan_free", "employee_seat_limit",     3, 0, "monthly", "notify", "active", "[]"),
                ("qr_free_workflow",    "plan_free", "workflow_limit",        None, 1, "monthly", "notify", "active", "[]"),
                ("qr_free_capability",  "plan_free", "capability_limit",     None, 1, "monthly", "block",  "active", '["official"]'),
                ("qr_free_connector",   "plan_free", "connector_limit",         0, 0, "monthly", "block",  "active", "[]"),
                # ── Pro ──
                ("qr_pro_token",        "plan_pro", "token_limit",        50000000, 0, "monthly", "notify", "active", "[]"),
                ("qr_pro_seat",         "plan_pro", "employee_seat_limit",    15, 0, "monthly", "notify", "active", "[]"),
                ("qr_pro_workflow",     "plan_pro", "workflow_limit",       50000, 0, "monthly", "notify", "active", "[]"),
                ("qr_pro_capability",   "plan_pro", "capability_limit",      None, 1, "monthly", "block",  "active", '["official","tenant_private"]'),
                ("qr_pro_connector",    "plan_pro", "connector_limit",       None, 1, "monthly", "block",  "active", '["official","tenant_private"]'),
                # ── Enterprise（custom：占位 NULL，is_unlimited=1，Admin 按企业改写）──
                ("qr_ent_token",        "plan_enterprise", "token_limit",      None, 1, "annual", "notify", "active", "[]"),
                ("qr_ent_seat",         "plan_enterprise", "employee_seat_limit", None, 1, "annual", "notify", "active", "[]"),
                ("qr_ent_workflow",     "plan_enterprise", "workflow_limit",   None, 1, "annual", "notify", "active", "[]"),
                ("qr_ent_capability",   "plan_enterprise", "capability_limit", None, 1, "annual", "block",  "active", '["official","tenant_private","marketplace"]'),
                ("qr_ent_connector",    "plan_enterprise", "connector_limit",  None, 1, "annual", "block",  "active", '["official","tenant_private","marketplace"]'),
            ]
            for _rule in _SEED_QUOTA_RULES:
                connection.execute(
                    "insert or ignore into quota_rules "
                    "(quota_rule_id, plan_id, quota_type, limit_value, is_unlimited, "
                    " period, enforcement_mode, status, source_scope_json) "
                    "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    _rule,
                )

            # ── Phase-9A P2：capability_packages 表（官方能力包商业配置权威来源）──
            # 与 plans / quotas / pricing_rules / quota_rules 同区；create table if not exists 保证幂等。
            # 组成引用以 JSON 数组 TEXT 存 ID 列表（运行时不强制外键，Admin 配置时校验）；
            # pricing_reference / quota_reference 指向 plan_id（派生该 plan 的定价与配额）。
            connection.executescript(
                """
                create table if not exists capability_packages (
                  package_id            text primary key,
                  name                  text not null,
                  description           text not null default '',
                  capability_ids        text not null default '[]',   -- JSON 数组：能力 key 列表
                  connector_ids         text not null default '[]',   -- JSON 数组：连接器 key 列表
                  workflow_template_ids text not null default '[]',   -- JSON 数组：工作流模板 id 列表
                  employee_template_ids text not null default '[]',   -- JSON 数组：员工模板 id 列表
                  pricing_reference     text,                        -- 引用 plan_id（价格来自 pricing_rules）
                  quota_reference       text,                        -- 引用 plan_id（配额来自 quota_rules）
                  availability          text not null default 'public'
                                         check (availability in ('public','tenant_invite_only','enterprise_only')),
                  status                text not null default 'draft'
                                         check (status in ('draft','active','disabled')),
                  created_at            text not null default current_timestamp,
                  updated_at            text not null default current_timestamp
                );

                create index if not exists idx_capability_packages_status
                  on capability_packages(status);
                create index if not exists idx_capability_packages_availability
                  on capability_packages(availability);
                """
            )

            # ── Phase-9A P2：示例官方能力包 seed（active 占位、可改写，禁止硬编码不可改）──
            # insert or ignore：幂等可重复执行。引用 plan_id 派生价格/配额；工作流/员工模板
            # 数组初始为空，由 Admin 经 API 配置真实模板 id（本 Issue 不强制外键）。
            _SEED_CAPABILITY_PACKAGES = [
                # (package_id, name, description, capability_ids_json, connector_ids_json,
                #  workflow_template_ids_json, employee_template_ids_json,
                #  pricing_reference, quota_reference, availability, status)
                (
                    "cp_content_ops",
                    "内容运营包",
                    "面向内容生产与分发的官方能力包（模型/工具/连接器能力 + 内容运营 AI）",
                    '["task_execution","tenant_private_capabilities","workflow_sop"]',
                    "[]",
                    "[]",
                    "[]",
                    "plan_pro",
                    "plan_pro",
                    "public",
                    "active",
                ),
            ]
            for _pkg in _SEED_CAPABILITY_PACKAGES:
                connection.execute(
                    "insert or ignore into capability_packages "
                    "(package_id, name, description, capability_ids, connector_ids, "
                    " workflow_template_ids, employee_template_ids, pricing_reference, "
                    " quota_reference, availability, status) "
                    "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    _pkg,
                )
            connection.execute(
                "update capability_packages set connector_ids = '[]' "
                "where package_id = 'cp_content_ops'"
            )

            # ── Self-use v1 (Wave 2 · F2 成果展示中心): 内容发布包 + 内容工作流运行持久化 ──
            # additive 表，幂等；供 /api/results/* 与内容发布闭环（content_workflow_runtime）消费。
            # 单账号沿用 tenant_id='selfuse'；不建多租户隔离机械（与既有库一致）。
            connection.executescript(
                """
                create table if not exists content_publish_packages (
                  package_id          text primary key,
                  tenant_id           text not null,
                  source_workflow     text not null,
                  version             text not null default '1.0.0',
                  language            text not null default 'zh-CN',
                  brand_voice_ref     text not null default '',
                  platforms_targeted  text not null default '[]',
                  artifacts_json      text not null default '[]',
                  status              text not null default 'generated'
                                        check (status in ('generated','published','failed')),
                  published_platforms text not null default '[]',
                  created_at          text not null default current_timestamp,
                  updated_at          text not null default current_timestamp
                );
                create index if not exists idx_cpp_tenant on content_publish_packages(tenant_id, created_at);

                create table if not exists content_workflow_runs (
                  run_id              text primary key,
                  tenant_id           text not null,
                  department_id       text not null default '',
                  workflow_content_id text not null,
                  status              text not null default 'running'
                                        check (status in ('running','completed','failed')),
                  steps_total         integer not null default 0,
                  steps_done          integer not null default 0,
                  summary             text not null default '',
                  created_at          text not null default current_timestamp,
                  updated_at          text not null default current_timestamp
                );
                create index if not exists idx_cwr_tenant on content_workflow_runs(tenant_id, created_at);

                -- CEO 战略会议室（strategy-room）：仅会议元数据，租户隔离，
                -- 无任何密钥 / 凭据列（与 credential_metadata 同源的「不落明文」纪律）。
                create table if not exists strategy_meetings (
                  meeting_id   text primary key,
                  tenant_id    text not null,
                  company_id   text not null default '',
                  business_id  text not null default '',
                  workspace_id text not null default '',
                  title        text not null,
                  agenda       text not null default '',
                  background   text not null default '',
                  participants text not null default '[]',
                  leader_employee_id text not null default '',
                  ceo_participation_mode text not null default 'DECISION_ONLY',
                  conversation_id text not null default '',
                  context_refs text not null default '[]',
                  decision_ref text not null default '',
                  work_refs    text not null default '[]',
                  result_refs  text not null default '[]',
                  continuation_gap text not null default '',
                  orchestration_json text not null default '{}',
                  status       text not null default 'scheduled'
                                check (status in ('scheduled','active','closed')),
                  timeline     text not null default '[]',
                  closed_at    text,
                  created_at   text not null default current_timestamp,
                  updated_at   text not null default current_timestamp
                );
                create index if not exists idx_sm_tenant on strategy_meetings(tenant_id, created_at desc);
                """
            )
            self._apply_schema_governance(connection)

    @staticmethod
    def _apply_schema_governance(connection: sqlite3.Connection) -> None:
        current_version = connection.execute("pragma user_version").fetchone()[0]
        if current_version > SCHEMA_VERSION:
            raise RuntimeError(
                f"database schema version {current_version} is newer than supported "
                f"version {SCHEMA_VERSION}"
            )
        if current_version < 1:
            for table in _RETIRED_EMPTY_TABLES:
                exists = connection.execute(
                    "select 1 from sqlite_master where type = 'table' and name = ?",
                    (table,),
                ).fetchone()
                if exists is None:
                    continue
                count = connection.execute(
                    f'select count(*) from "{table}"'
                ).fetchone()[0]
                if count:
                    raise RuntimeError(
                        f"refusing to drop non-empty retired table: {table}"
                    )
                connection.execute(f'drop table "{table}"')
            connection.execute(
                "insert or ignore into schema_migrations(version, name) values (?, ?)",
                (1, "integration-v1-schema-baseline"),
            )
            connection.execute(f"pragma user_version = {SCHEMA_VERSION}")

    def _reset_legacy_tasks_table(self, connection: sqlite3.Connection) -> None:
        row = connection.execute(
            "select name from sqlite_master where type = 'table' and name = 'tasks'"
        ).fetchone()
        if row is None:
            return
        columns = {column["name"] for column in connection.execute("pragma table_info(tasks)")}
        if "content" not in columns or "task_id" not in columns:
            connection.executescript(
                """
                drop table if exists executions;
                drop table if exists execution_results;
                drop table if exists tasks;
                """
            )

    def _migrate_task_execution_scope(self, connection: sqlite3.Connection) -> None:
        """Add optional scope as one unit; never infer or rewrite historical ownership."""
        connection.execute("savepoint task_execution_scope")
        try:
            for column in ("scope_type", "scope_ref"):
                self._ensure_column(connection, "tasks", column, "text")
            connection.execute("release task_execution_scope")
        except Exception:
            connection.execute("rollback to task_execution_scope")
            connection.execute("release task_execution_scope")
            raise

    def _ensure_column(self, connection: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        # SQLite 仅允许常量默认值出现在 ``ALTER TABLE ADD COLUMN``；``current_timestamp``
        # 必须大写 ``CURRENT_TIMESTAMP`` 才会被识别为常量时间戳默认值（否则报
        # "Cannot add a column with non-constant default"）。统一在此归一，避免各调用点踩坑。
        definition = definition.replace("current_timestamp", "CURRENT_TIMESTAMP")
        row = connection.execute(
            "select name from sqlite_master where type = 'table' and name = ?",
            (table,),
        ).fetchone()
        if row is None:
            return
        columns = {item["name"] for item in connection.execute(f"pragma table_info({table})")}
        if column not in columns:
            connection.execute(f"alter table {table} add column {column} {definition}")

    @staticmethod
    def _migrate_projects_to_business_departments(connection: sqlite3.Connection) -> None:
        """Give every legacy Project a visible business-department parent."""
        scopes = connection.execute(
            """
            select distinct tenant_id, company_id
            from projects
            where department_id is null or trim(department_id) = ''
            """
        ).fetchall()
        for scope in scopes:
            department = connection.execute(
                """
                select id from department_instances
                where tenant_id = ? and company_id = ? and name = '待归属业务部'
                  and enabled = 1 and deleted_at is null
                limit 1
                """,
                (scope["tenant_id"], scope["company_id"]),
            ).fetchone()
            department_id = department["id"] if department else f"department-{uuid.uuid4()}"
            if department is None:
                connection.execute(
                    """
                    insert into department_instances (
                      id, tenant_id, company_id, template_id, name, department_type,
                      mission, status, created_from_template_id,
                      enabled_employee_template_ids_json, enabled, updated_at
                    ) values (?, ?, ?, 'official.department.software_rnd',
                              '待归属业务部', 'business.general',
                              '承接迁移前未归属业务部门的项目。', 'active',
                              'official.department.software_rnd', '[]', 1,
                              current_timestamp)
                    """,
                    (department_id, scope["tenant_id"], scope["company_id"]),
                )
            connection.execute(
                """
                update projects set department_id = ?, updated_at = current_timestamp
                where tenant_id = ? and company_id = ?
                  and (department_id is null or trim(department_id) = '')
                """,
                (department_id, scope["tenant_id"], scope["company_id"]),
            )

    @staticmethod
    def _migrate_model_gateways_multi_type(connection: sqlite3.Connection) -> None:
        """Step 5 迁移：把既有库里 ``type check (type in ('newapi'))`` 的旧表重建为多类型。

        SQLite 无法 ALTER CHECK，只能整表重建。判定条件是「旧 CHECK 里没有
        'oneapi'」，因此本迁移天然幂等：重建过一次后不会再触发。所有数据原样搬迁，
        无列增减、无默认值变化，不触碰任何凭证（表中只有 credential_ref 引用串）。
        """
        row = connection.execute(
            "select sql from sqlite_master where type = 'table' and name = 'model_gateways'"
        ).fetchone()
        if row is None:
            return
        schema_sql = str(row["sql"] or "")
        if "check" not in schema_sql.lower() or "oneapi" in schema_sql.lower():
            return  # 无 CHECK（更宽松）或已是新版：无需迁移
        connection.executescript(
            """
            create table if not exists model_gateways__step5 (
              gateway_id      text primary key,
              name            text not null,
              type            text not null default 'newapi'
                                check (type in ('newapi', 'oneapi', 'openai',
                                  'openai_compatible', 'openrouter', 'deepseek',
                                  'moonshot', 'ollama', 'vllm')),
              base_url        text not null,
              status          text not null default 'active'
                                check (status in ('active', 'inactive')),
              credential_ref  text,
              default_model   text,
              created_at      text not null default current_timestamp
            );
            insert or ignore into model_gateways__step5
              (gateway_id, name, type, base_url, status, credential_ref,
               default_model, created_at)
            select gateway_id, name, type, base_url, status, credential_ref,
                   default_model, created_at
            from model_gateways;
            drop table model_gateways;
            alter table model_gateways__step5 rename to model_gateways;
            create index if not exists idx_model_gateways_status
              on model_gateways(status, type);
            """
        )

    @staticmethod
    def _migrate_capability_type_check_agent(connection: sqlite3.Connection) -> None:
        """Agent 运行时桥迁移：把旧库里 ``capability_type in ('model','tool','connector')``
        的 CHECK 重建为含 ``'agent'`` 的版本。

        SQLite 无法 ALTER CHECK，只能整表重建。判定条件是旧建表 SQL 中含有
        旧 CHECK 标记（不含 ``'agent'``），因此天然幂等：重建过一次后不再触发。
        新表定义 = 旧表 SQL 仅替换该 CHECK（无列增减、无默认值变化），数据原样
        搬迁；``drop table`` 会连带删除索引与触发器，故先备份再恢复
        （``ai_usage_records`` 有 4 个索引 + 1 个只读触发器）。
        """
        old_marker = "('model', 'tool', 'connector')"
        new_marker = "('model', 'agent', 'tool', 'connector')"
        for table in (
            "tenant_private_capabilities",
            "employee_capability_bindings",
            "ai_usage_records",
        ):
            row = connection.execute(
                "select sql from sqlite_master where type = 'table' and name = ?",
                (table,),
            ).fetchone()
            if row is None:
                continue
            schema_sql = str(row["sql"] or "")
            if old_marker not in schema_sql:
                continue  # 无旧 CHECK 或已是新版：无需迁移
            temp_name = f"{table}__agent"
            indexes = [
                str(item["sql"])
                for item in connection.execute(
                    "select sql from sqlite_master where type = 'index' "
                    "and tbl_name = ? and sql is not null",
                    (table,),
                ).fetchall()
            ]
            triggers = [
                str(item["sql"])
                for item in connection.execute(
                    "select sql from sqlite_master where type = 'trigger' and tbl_name = ?",
                    (table,),
                ).fetchall()
            ]
            connection.execute(f"drop table if exists {temp_name}")
            connection.executescript(
                schema_sql.replace(table, temp_name).replace(old_marker, new_marker)
            )
            connection.execute(f"insert or ignore into {temp_name} select * from {table}")
            connection.execute(f"drop table {table}")
            connection.execute(f"alter table {temp_name} rename to {table}")
            for sql in indexes:
                connection.execute(sql)
            for sql in triggers:
                connection.execute(sql)

    @staticmethod
    def _migrate_conversation_usage(connection: sqlite3.Connection) -> None:
        """Extend the one immutable ledger; never reinterpret historical rows."""
        schema = connection.execute(
            "select sql from sqlite_master where type='table' and name='ai_usage_records'"
        ).fetchone()[0]
        columns = [row["name"] for row in connection.execute("pragma table_info(ai_usage_records)")]
        if "conversation_ref" in columns:
            if "canonical_employee_ref" not in columns:
                raise RuntimeError("Incomplete conversation usage schema")
            return
        old_work = "and work_ref is not null and trim(work_ref) != ''"
        old_legacy = "and work_ref is null and execution_ref is null"
        if schema.count(old_work) != 1 or schema.count(old_legacy) != 1:
            raise RuntimeError("Unrecognized usage attribution constraint; migration refused")
        target = re.sub(r'CREATE TABLE\s+"?ai_usage_records"?',
                        'CREATE TABLE ai_usage_records__conversation', schema, count=1, flags=re.I)
        target = target.replace('(', '(conversation_ref text, canonical_employee_ref text,', 1)
        target = target.replace(old_legacy, old_legacy +
            " and conversation_ref is null and canonical_employee_ref is null")
        target = target.replace(old_work, """and (
            (work_ref is not null and trim(work_ref) != ''
             and conversation_ref is null and canonical_employee_ref is null)
            or (work_ref is null and project_id is null
                and conversation_ref is not null and trim(conversation_ref) != ''
                and canonical_employee_ref is not null and trim(canonical_employee_ref) != '')
        )""")
        objects = [row[0] for row in connection.execute(
            "select sql from sqlite_master where tbl_name='ai_usage_records' "
            "and type in ('index','trigger') and sql is not null")]
        names = ','.join('"' + name.replace('"', '""') + '"' for name in columns)
        connection.execute("savepoint conversation_usage")
        try:
            connection.execute(target)
            connection.execute(f"insert into ai_usage_records__conversation ({names}) select {names} from ai_usage_records")
            for left, right in [('ai_usage_records', 'ai_usage_records__conversation'),
                                ('ai_usage_records__conversation', 'ai_usage_records')]:
                if connection.execute(f"select {names} from {left} except select {names} from {right}").fetchone():
                    raise RuntimeError("Usage migration did not preserve historical rows")
            connection.execute("drop table ai_usage_records")
            connection.execute("alter table ai_usage_records__conversation rename to ai_usage_records")
            for sql in objects:
                connection.execute(sql)
            connection.execute("release conversation_usage")
        except Exception:
            connection.execute("rollback to conversation_usage")
            connection.execute("release conversation_usage")
            raise

    @staticmethod
    def _migrate_execution_scope_usage(connection: sqlite3.Connection) -> None:
        """Extend the one immutable ledger without reinterpreting any historical row."""
        schema = connection.execute(
            "select sql from sqlite_master where type='table' and name='ai_usage_records'"
        ).fetchone()[0]
        columns = [row["name"] for row in connection.execute("pragma table_info(ai_usage_records)")]
        if "scope_type" in columns or "scope_ref" in columns:
            if not {"scope_type", "scope_ref"}.issubset(columns):
                raise RuntimeError("Incomplete execution scope usage schema")
            return
        marker = re.search(r"check\s*\(\s*\(\s*project_id is not null", schema, re.I)
        table_end = schema.rfind(")")
        check_end = schema.rfind(")", 0, table_end)
        if marker is None or "conversation_ref" not in columns or schema[check_end + 1:table_end].strip():
            raise RuntimeError("Unrecognized usage scope constraint; migration refused")
        opening = schema.index("(", marker.start())
        historical_check = schema[opening + 1:check_end]
        lineage = []
        fields = ("company_id", "department_id", "business_id", "workspace_id")
        from .resource_scope_policy import ResourceScopePolicy
        for index, kind in enumerate(ResourceScopePolicy.EXECUTION_SCOPES):
            conditions = [f"scope_type='{kind}'", f"scope_ref=coalesce({fields[index]}, '')"]
            conditions += [f"{field} is not null and trim({field})!=''" for field in fields[:index + 1]]
            conditions += [f"{field} is null" for field in fields[index + 1:]]
            lineage.append("(" + " and ".join(conditions) + ")")
        constraint = f"""check (
            (scope_type is null and scope_ref is null and department_id is not null and ({historical_check}))
            or (scope_type is not null and scope_ref is not null and trim(scope_ref)!=''
                and ({' or '.join(lineage)})
                and execution_ref is not null and trim(execution_ref)!=''
                and ((work_ref is not null and trim(work_ref)!='' and conversation_ref is null)
                    or (work_ref is null and project_id is null and conversation_ref is not null
                        and trim(conversation_ref)!='' and canonical_employee_ref is not null
                        and trim(canonical_employee_ref)!='')))
        )"""
        target = schema[:marker.start()] + constraint + schema[check_end + 1:]
        target, count = re.subn(r"department_id\s+text\s+not null", "department_id text", target, count=1, flags=re.I)
        if count != 1:
            raise RuntimeError("Unrecognized usage Department column; migration refused")
        target = re.sub(r'CREATE TABLE\s+"?ai_usage_records"?', 'CREATE TABLE ai_usage_records__scope', target, count=1, flags=re.I)
        target = target.replace('(', '(scope_type text, scope_ref text,', 1)
        objects = [row[0] for row in connection.execute(
            "select sql from sqlite_master where tbl_name='ai_usage_records' "
            "and type in ('index','trigger') and sql is not null")]
        names = ','.join('"' + name.replace('"', '""') + '"' for name in columns)
        connection.execute("savepoint execution_scope_usage")
        try:
            connection.execute(target)
            connection.execute(f"insert into ai_usage_records__scope ({names}) select {names} from ai_usage_records")
            for left, right in (("ai_usage_records", "ai_usage_records__scope"), ("ai_usage_records__scope", "ai_usage_records")):
                if connection.execute(f"select {names} from {left} except select {names} from {right}").fetchone():
                    raise RuntimeError("Execution scope migration changed historical usage")
            connection.execute("drop table ai_usage_records")
            connection.execute("alter table ai_usage_records__scope rename to ai_usage_records")
            for sql in objects:
                connection.execute(sql)
            connection.execute("release execution_scope_usage")
        except Exception:
            connection.execute("rollback to execution_scope_usage")
            connection.execute("release execution_scope_usage")
            raise

    @staticmethod
    def _migrate_usage_attribution(connection: sqlite3.Connection) -> None:
        """Replace Project-only usage ownership with canonical-or-legacy attribution."""
        row = connection.execute(
            "select sql from sqlite_master where type='table' and name='ai_usage_records'"
        ).fetchone()
        if row is None:
            return
        columns = {
            item["name"]: item
            for item in connection.execute("pragma table_info(ai_usage_records)").fetchall()
        }
        required = {"company_id", "business_id", "workspace_id", "work_ref", "execution_ref"}
        if required.issubset(columns) and not bool(columns["project_id"]["notnull"]):
            return

        unresolved = connection.execute(
            """
            select u.usage_record_id
            from ai_usage_records u
            left join projects p
              on p.tenant_id = u.tenant_id and p.project_id = u.project_id
            left join department_instances d
              on d.tenant_id = p.tenant_id and d.id = p.department_id
            where p.project_id is null
               or trim(coalesce(p.company_id, '')) = ''
               or trim(coalesce(p.department_id, '')) = ''
               or p.department_id != u.department_id
               or d.id is null
               or d.company_id != p.company_id
            limit 1
            """
        ).fetchone()
        if unresolved is not None:
            raise RuntimeError(
                "historical usage attribution cannot resolve Project → Company/Department: "
                f"{unresolved['usage_record_id']}"
            )

        indexes = [
            str(item["sql"])
            for item in connection.execute(
                "select sql from sqlite_master where type='index' "
                "and tbl_name='ai_usage_records' and sql is not null"
            ).fetchall()
        ]
        triggers = [
            str(item["sql"])
            for item in connection.execute(
                "select sql from sqlite_master where type='trigger' and tbl_name='ai_usage_records'"
            ).fetchall()
        ]
        before_count = connection.execute("select count(*) from ai_usage_records").fetchone()[0]
        connection.execute("savepoint canonical_usage_attribution")
        try:
            connection.execute("drop table if exists ai_usage_records__canonical")
            connection.execute(
                """
                create table ai_usage_records__canonical (
                  usage_record_id       text primary key,
                  tenant_id             text not null,
                  company_id            text not null,
                  model_gateway_id      text not null,
                  provider_id           text not null,
                  model_name            text not null,
                  input_tokens          integer check (input_tokens is null or input_tokens >= 0),
                  output_tokens         integer check (output_tokens is null or output_tokens >= 0),
                  total_tokens          integer check (total_tokens is null or total_tokens >= 0),
                  cost_amount           numeric check (cost_amount is null or cost_amount >= 0),
                  currency              text not null,
                  cost_source           text not null
                                        check (cost_source in ('unknown', 'estimated', 'provider_reported')),
                  price_version         text,
                  employee_id           text not null,
                  capability_id         text not null,
                  capability_type       text not null
                                        check (capability_type in ('model', 'agent', 'tool', 'connector')),
                  task_id               text not null,
                  project_id            text,
                  department_id         text not null,
                  business_id           text,
                  workspace_id          text,
                  work_ref              text,
                  execution_ref         text,
                  request_id            text not null,
                  execution_status      text not null,
                  metering_status       text not null
                                        check (metering_status in ('confirmed', 'unknown')),
                  occurred_at           text not null,
                  created_at            text not null
                                        default (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                  idempotency_key        text not null unique,
                  cache_read_tokens      integer check (cache_read_tokens is null or cache_read_tokens >= 0),
                  cache_write_tokens     integer check (cache_write_tokens is null or cache_write_tokens >= 0),
                  reasoning_tokens       integer check (reasoning_tokens is null or reasoning_tokens >= 0),
                  latency_ms             integer check (latency_ms is null or latency_ms >= 0),
                  workflow_run_id        text,
                  workflow_step_id       text,
                  capability_binding_id  text,
                  logical_call_id        text,
                  attempt_no             integer check (attempt_no is null or attempt_no >= 1),
                  fallback_from_model    text,
                  fallback_reason        text,
                  http_status            integer check (http_status is null or http_status >= 0),
                  check (
                    (
                      project_id is not null and trim(project_id) != ''
                      and business_id is null and workspace_id is null
                      and work_ref is null and execution_ref is null
                    )
                    or (
                      business_id is not null and trim(business_id) != ''
                      and workspace_id is not null and trim(workspace_id) != ''
                      and work_ref is not null and trim(work_ref) != ''
                      and execution_ref is not null and trim(execution_ref) != ''
                    )
                  )
                )
                """
            )
            historical = lambda name: f"u.{name}" if name in columns else "null"
            connection.execute(
                f"""
                insert into ai_usage_records__canonical (
                  usage_record_id, tenant_id, company_id, model_gateway_id, provider_id,
                  model_name, input_tokens, output_tokens, total_tokens, cost_amount,
                  currency, cost_source, price_version, employee_id, capability_id,
                  capability_type, task_id, project_id, department_id, business_id,
                  workspace_id, work_ref, execution_ref, request_id, execution_status,
                  metering_status, occurred_at, created_at, idempotency_key, cache_read_tokens,
                  cache_write_tokens, reasoning_tokens, latency_ms, workflow_run_id,
                  workflow_step_id, capability_binding_id, logical_call_id, attempt_no,
                  fallback_from_model, fallback_reason, http_status
                )
                select u.usage_record_id, u.tenant_id, p.company_id, u.model_gateway_id,
                       u.provider_id, u.model_name, u.input_tokens, u.output_tokens,
                       u.total_tokens, u.cost_amount, u.currency, u.cost_source,
                       u.price_version, u.employee_id, u.capability_id, u.capability_type,
                       u.task_id, u.project_id, u.department_id, null, null, null, null,
                       u.request_id, u.execution_status, u.metering_status, u.occurred_at,
                       u.created_at, u.idempotency_key, {historical('cache_read_tokens')},
                       {historical('cache_write_tokens')}, {historical('reasoning_tokens')},
                       {historical('latency_ms')}, {historical('workflow_run_id')},
                       {historical('workflow_step_id')}, {historical('capability_binding_id')},
                       {historical('logical_call_id')}, {historical('attempt_no')},
                       {historical('fallback_from_model')}, {historical('fallback_reason')},
                       {historical('http_status')}
                from ai_usage_records u
                join projects p
                  on p.tenant_id = u.tenant_id and p.project_id = u.project_id
                """
            )
            after_count = connection.execute(
                "select count(*) from ai_usage_records__canonical"
            ).fetchone()[0]
            if after_count != before_count:
                raise RuntimeError("historical usage migration row count mismatch")
            connection.execute("drop table ai_usage_records")
            connection.execute(
                "alter table ai_usage_records__canonical rename to ai_usage_records"
            )
            for sql in indexes:
                connection.execute(sql)
            for sql in triggers:
                connection.execute(sql)
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_company "
                "on ai_usage_records(tenant_id, company_id, occurred_at desc)"
            )
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_workspace "
                "on ai_usage_records(tenant_id, workspace_id, occurred_at desc)"
            )
            connection.execute(
                "create index if not exists idx_ai_usage_tenant_work "
                "on ai_usage_records(tenant_id, work_ref, occurred_at desc)"
            )
            connection.execute("release canonical_usage_attribution")
        except Exception:
            connection.execute("rollback to canonical_usage_attribution")
            connection.execute("release canonical_usage_attribution")
            raise

    @staticmethod
    def _migrate_completed_task_artifacts(connection: sqlite3.Connection) -> None:
        """Register only legacy outputs with an explicit completed Task parent."""
        rows = connection.execute(
            """
            select task_id, tenant_id, content, output
            from tasks
            where status = 'COMPLETED' and trim(coalesce(output, '')) != ''
            """
        ).fetchall()
        for row in rows:
            output = str(row["output"])
            connection.execute(
                """
                insert or ignore into artifacts (
                  artifact_id, tenant_id, task_id, title, artifact_type,
                  status, content, source_ref, content_sha256
                ) values (?, ?, ?, ?, 'execution_result', 'generated', ?,
                          'task.output', ?)
                """,
                (
                    f"artifact-migrated-{row['task_id']}",
                    row["tenant_id"],
                    row["task_id"],
                    str(row["content"])[:120] or "未命名成果",
                    output,
                    hashlib.sha256(output.encode("utf-8")).hexdigest(),
                ),
            )
    @staticmethod
    def _migrate_guide_sessions(connection: sqlite3.Connection) -> None:
        """业务工作台引导会话表（幂等建表 + 索引）。

        存储引导会话运行态（步骤游标 / 收集内容 / 蓝图草案）。设计见
        docs/plan/workbench-guide-backend-design.md §5。绝不存密钥：
        collected_json 写前经 secret 扫描；model_used 仅存脱敏摘要。
        """
        connection.executescript(
            """
            create table if not exists guide_sessions (
              session_id     text primary key,
              tenant_id      text not null,
              guide_id       text not null,
              guide_version  text not null,
              status         text not null
                             check (status in
                               ('INIT','COLLECTING','READY','CONFIRMED','DONE','ABANDONED')),
              current_step   integer not null default 1,
              collected_json text not null default '{}',
              blueprint_json text,
              model_used     text,
              created_at     text not null default current_timestamp,
              updated_at     text not null default current_timestamp
            );
            create index if not exists idx_guide_sessions_tenant
              on guide_sessions(tenant_id, status);
            """
        )

    @staticmethod
    def _migrate_business_metrics(connection: sqlite3.Connection) -> None:
        """经营指标事实源表（Phase-9 CEO Operating Day，幂等建表 + 唯一索引）。

        从现有实体（projects / tasks / artifacts / ai_usage_records /
        workflow_runs / employee_instances）聚合，按 (tenant, company, period,
        metric_key) 唯一 upsert。设计见 docs/plan/ceo-operating-day-design.md §2。
        """
        connection.executescript(
            """
            create table if not exists business_metrics (
              metric_id    text primary key,
              tenant_id    text not null,
              company_id   text not null,
              period       text not null,
              metric_key   text not null,
              value        real not null,
              unit         text not null default '',
              source       text not null default 'aggregated',
              computed_at  text not null default current_timestamp,
              updated_at   text not null default current_timestamp
            );
            create unique index if not exists uq_business_metrics
              on business_metrics(tenant_id, company_id, period, metric_key);
            """
        )

    @staticmethod
    def _migrate_runtime_trace_event(connection: sqlite3.Connection) -> None:
        """运行时 trace 事件表（EvoFlow 复用 A2，append-only 可观测）。

        把 TaskNode.trace（内存字段）升格为独立 append-only 事件表，记录执行
        管道事件（能力调用/token/缓存命中/延迟），供 CEO 侧只读查看执行过程。
        设计见 docs/plan/evoflow-verified-reuse-plan.md A2；不改变任务语义。
        """
        connection.executescript(
            """
            create table if not exists runtime_trace_event (
              id           text primary key,
              tenant_id    text not null,
              run_id       text not null,
              task_id      text,
              task_ref     text,
              event_type   text not null,
              capability   text not null default '',
              tokens_in    integer,
              tokens_out   integer,
              cache_hit    integer,
              latency_ms   integer,
              payload_json text not null default '{}',
              created_at   text not null default current_timestamp
            );
            create index if not exists idx_runtime_trace_run
              on runtime_trace_event(tenant_id, run_id, created_at);
            """
        )

    def _migrate_position_authorization(self, connection: sqlite3.Connection) -> None:
        """岗位级能力授权（Phase-10）：岗位模板 + 员工实例增授权白名单列。

        - employee_templates.allowed_effect_classes_json：岗位模板默认授权。
        - employee_instances.allowed_effect_classes_json：实例级覆盖（空 = 继承模板）。
        - 兼容策略：既有 et_* 官方模板回填「全开」（read/retrieve/write/exec）作为
          兼容基线（不破坏既有绑定/执行）；引导生成的新岗位必须显式声明（deny-by-default）。
          设计见 docs/plan/position-authorization-design.md §2。
        """
        template_has_column = any(row["name"] == "allowed_effect_classes_json" for row in connection.execute("pragma table_info(employee_templates)"))
        self._ensure_column(
            connection,
            "employee_templates",
            "allowed_effect_classes_json",
            "text not null default '[]'",
        )
        self._ensure_column(
            connection,
            "employee_instances",
            "allowed_effect_classes_json",
            "text not null default '[]'",
        )
        if not template_has_column:
            # Only a truly old schema needs the accepted one-time compatibility grant.
            connection.execute(
                """
                update employee_templates
                set allowed_effect_classes_json = '["read","retrieve","write","exec"]'
                where source = 'official'
                  and (allowed_effect_classes_json is null or allowed_effect_classes_json = '[]')
                """
            )

    def _migrate_capability_ownership(self, connection: sqlite3.Connection) -> None:
        """双轨能力供给（商业化预留）：official_models 增 owner_type / owner_id / visibility。

        官方供给（official / public）与租户自助（tenant / private）据此区分写权与消费面。
        既有行全为官方（建库早于本迁移），按默认 owner_type='official'、visibility='public'
        回填，天然幂等（列已存在则 ``_ensure_column`` 跳过）。_ensure_column 已归一
        current_timestamp → CURRENT_TIMESTAMP，常量默认值可用。
        """
        for column, definition in (
            ("owner_type", "text not null default 'official'"),
            ("owner_id", "text not null default ''"),
            ("visibility", "text not null default 'public'"),
        ):
            self._ensure_column(connection, "official_models", column, definition)

    def _seed_department_catalog(self, connection: sqlite3.Connection) -> None:
        """幂等种子：填充最小规范部门类型集（建一次、全员可用）。

        manifest_json 恒为占位结构（"{}"），不含任何真实平台凭证、ROI 数据
        或员工数据。使用 INSERT OR IGNORE，使 initialize() 可重复调用而安全。
        超出规范集的新增类型须走 gate + ADR（ADR-0017 D4），本 slice 不预设。
        """
        # CEO 2026-10-10: catalog supply only; never creates Company departments.
        connection.execute(
            "insert or ignore into department_templates "
            "(id,slug,name,department_type,description,version,status,source,tenant_id,enabled) "
            "values (?, 'writing', '写作部', 'writing', '本地写作与版本续做。', "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            (FIRST_LAUNCH_DEPARTMENT_TEMPLATES["writing"],),
        )
        content_growth = (
            "content_growth", "business", "内容增长部",
            "本地图文、长短视频及口播文本与脚本、来源版本自检、账号资料、人工核验、观察与经验；不保证真实媒体、平台连接发布、自动采集、独立审核或 Provider 执行。",
            "{}", "0.0", 1,
        )
        existing = connection.execute(
            "select type_key,category,display_name,description,manifest_json,manifest_schema_version,is_system "
            "from department_types where type_key=?", (content_growth[0],),
        ).fetchone()
        status = connection.execute(
            "select enabled from department_type_status where type_key=?", (content_growth[0],),
        ).fetchone()
        if ((existing is not None and tuple(existing) != content_growth)
                or (status is not None and not status[0])):
            raise ValueError("Content Growth department type conflicts with the approved catalog")
        music = (
            "music", "business", "音乐部",
            "本地歌词与制作依据、真实授权样本试听、人工选版与独立成品确认、未发布准备包、人工观察与经验；不保证音频生成、歌词演唱匹配、商业权利、平台发行或 Provider 执行。",
            "{}", "0.0", 1,
        )
        existing_music = connection.execute(
            "select type_key,category,display_name,description,manifest_json,manifest_schema_version,is_system "
            "from department_types where type_key=?", (music[0],),
        ).fetchone()
        music_status = connection.execute(
            "select enabled from department_type_status where type_key=?", (music[0],),
        ).fetchone()
        if ((existing_music is not None and tuple(existing_music) != music)
                or (music_status is not None and not music_status[0])):
            raise ValueError("Music department type conflicts with the approved catalog")
        canonical_types = [
            content_growth,
            music,
            (
                "business.general", "business", "业务部",
                "业务型（对外），平台通道留作 future hook",
                "{}", "0.0", 1,
            ),
            (
                "function.hr", "function", "人事部",
                "职能型（对内），员工层留作 future hook",
                "{}", "0.0", 1,
            ),
            (
                "function.admin", "function", "行政部",
                "职能型（对内），L6 ROI 度量留作 future hook",
                "{}", "0.0", 1,
            ),
            (
                "function.bi", "function", "BI 部",
                "职能型（对内），L6 可视化留作 future hook",
                "{}", "0.0", 1,
            ),
        ]
        connection.executemany(
            "insert or ignore into department_types "
            "(type_key, category, display_name, description, "
            "manifest_json, manifest_schema_version, is_system) "
            "values (?, ?, ?, ?, ?, ?, ?)",
            canonical_types,
        )

    def _seed_official_model_catalog(self, connection: sqlite3.Connection) -> None:
        model_name = os.getenv("CURIS_MODEL_GATEWAY_MODEL", "newapi-default")
        gateway_id = os.getenv("CURIS_MODEL_GATEWAY_ID", "newapi")
        connection.execute(
            "insert or ignore into official_models "
            "(model_key, provider_id, display_name, supported_models, auth_type, source, gateway_ref, status) "
            "values (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "official.newapi.default",
                "newapi",
                "New API Default Model",
                json.dumps([model_name], ensure_ascii=False),
                "apikey",
                "official",
                gateway_id,
                "active",
            ),
        )

    def _seed_model_gateway(self, connection: sqlite3.Connection) -> None:
        """Idempotent seed of the default New API gateway.

        gateway_id comes from env CURIS_MODEL_GATEWAY_ID (default 'newapi') to
        stay aligned with official_models.gateway_ref (also default 'newapi').
        No secret is stored: credential_ref / default_model are deliberately left
        NULL; the Admin configures the real metadata later. Admin never makes
        outbound calls.
        """
        gateway_id = os.getenv("CURIS_MODEL_GATEWAY_ID", "newapi")
        base_url = os.getenv("CURIS_MODEL_GATEWAY_BASE_URL", "")
        connection.execute(
            "insert or ignore into model_gateways "
            "(gateway_id, name, type, base_url, status, credential_ref, default_model) "
            "values (?, ?, ?, ?, ?, ?, ?)",
            (gateway_id, "New API Gateway", "newapi", base_url, "active", None, None),
        )

    def _seed_employee_template_contract(self, connection: sqlite3.Connection) -> None:
        """Seed the official Software R&D employee and department templates."""
        templates = [
            (
                "official.employee.tech_lead",
                "tech-lead",
                "Tech Lead",
                "tech_lead",
                "接收研发任务，拆解执行路径，并在任务结束后汇总交付证据。",
                "研发部任务负责人，默认接收未指定员工的研发任务。",
                "software_rnd",
                "按技术负责人职责拆解任务，优先保持范围清晰、风险可控、证据完整。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["task_breakdown", "report"],
            ),
            (
                "official.employee.product_manager",
                "product-manager",
                "Product Manager",
                "product_manager",
                "理解 CEO 需求，确认范围、验收标准和不做事项。",
                "研发部产品规划员工。",
                "software_rnd",
                "把任务转成清晰的产品范围和验收标准，发现范围冲突时停止升级。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["requirement_understanding"],
            ),
            (
                "official.employee.architect",
                "architect",
                "Architect",
                "architect",
                "定义系统边界、数据模型、API 和模块风险。",
                "研发部架构员工。",
                "software_rnd",
                "优先复用现有架构，避免未批准的执行链路和平台边界变更。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["architecture_design"],
            ),
            (
                "official.employee.frontend_engineer",
                "frontend-engineer",
                "Frontend Engineer",
                "frontend_engineer",
                "实现 Workspace 前端界面和交互状态。",
                "研发部前端员工。",
                "software_rnd",
                "在既有工作台内实现最小 UI，不新增复杂组织图或业务模块。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["coding"],
            ),
            (
                "official.employee.backend_engineer",
                "backend-engineer",
                "Backend Engineer",
                "backend_engineer",
                "实现 Workspace 后端数据模型、API 和测试。",
                "研发部后端员工。",
                "software_rnd",
                "保持租户隔离、usage_event 归因和模型网关适配器路径不漂移。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["coding"],
            ),
            (
                "official.employee.qa_engineer",
                "qa-engineer",
                "QA Engineer",
                "qa_engineer",
                "执行验证、回归测试、范围扫描和验收证据整理。",
                "研发部质量员工。",
                "software_rnd",
                "验证现有功能不回退，所有完成声明必须有新鲜证据。",
                ["model", "tool"],
                {"mode": "tenant_default"},
                ["testing"],
            ),
        ]
        connection.executemany(
            "insert or ignore into employee_templates "
            "(id, slug, name, role, responsibility, description, department_type, "
            "default_instructions, default_capability_types_json, default_model_policy_json, "
            "default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'official', 'platform', 1)",
            [
                (
                    template_id,
                    slug,
                    name,
                    role,
                    responsibility,
                    description,
                    department_type,
                    instructions,
                    json.dumps(capability_types, ensure_ascii=False),
                    json.dumps(model_policy, ensure_ascii=False),
                    json.dumps(step_types, ensure_ascii=False),
                    json.dumps([], ensure_ascii=False),
                )
                for (
                    template_id,
                    slug,
                    name,
                    role,
                    responsibility,
                    description,
                    department_type,
                    instructions,
                    capability_types,
                    model_policy,
                    step_types,
                ) in templates
            ],
        )
        connection.execute(
            "insert or ignore into department_templates "
            "(id, slug, name, department_type, description, default_employee_templates_json, "
            "default_workflow_template_id, default_capability_types_json, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, 'official', 'platform', 1)",
            (
                "official.department.software_rnd",
                "software-rnd",
                "研发部",
                "software_rnd",
                "第一版 AI 公司研发部，包含产品、架构、前端、后端、质量和技术负责人。",
                json.dumps([item[0] for item in templates], ensure_ascii=False),
                "official.workflow.software_rnd_sop",
                json.dumps(["model", "tool", "connector"], ensure_ascii=False),
            ),
        )
        content_growth = (
            "dt_content_growth", "content-growth", "内容增长部", "content_growth",
            "本地图文、长短视频及口播文本与脚本、来源版本自检、账号资料、人工核验、观察与经验；不保证真实媒体、平台连接发布、自动采集、独立审核或 Provider 执行。",
            "[]", None, "[]", "1.0.0", "active", "official", "platform", 1,
        )
        existing = connection.execute(
            "select id,slug,name,department_type,description,default_employee_templates_json,"
            "default_workflow_template_id,default_capability_types_json,version,status,source,tenant_id,enabled "
            "from department_templates where id=?", (content_growth[0],),
        ).fetchone()
        if existing is not None and tuple(existing) != content_growth:
            raise ValueError("Content Growth department template conflicts with the approved catalog")
        if existing is None:
            connection.execute(
                "insert into department_templates "
                "(id,slug,name,department_type,description,default_employee_templates_json,"
                "default_workflow_template_id,default_capability_types_json,version,status,source,tenant_id,enabled) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?)", content_growth,
            )

        music = (
            "dt_music", "music", "音乐部", "music",
            "本地歌词与制作依据、真实授权样本试听、人工选版与独立成品确认、未发布准备包、人工观察与经验；不保证音频生成、歌词演唱匹配、商业权利、平台发行或 Provider 执行。",
            "[]", None, "[]", "1.0.0", "active", "official", "platform", 1,
        )
        existing_music = connection.execute(
            "select id,slug,name,department_type,description,default_employee_templates_json,"
            "default_workflow_template_id,default_capability_types_json,version,status,source,tenant_id,enabled "
            "from department_templates where id=?", (music[0],),
        ).fetchone()
        if existing_music is not None and tuple(existing_music) != music:
            raise ValueError("Music department template conflicts with the approved catalog")
        if existing_music is None:
            connection.execute(
                "insert into department_templates "
                "(id,slug,name,department_type,description,default_employee_templates_json,"
                "default_workflow_template_id,default_capability_types_json,version,status,source,tenant_id,enabled) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?)", music,
            )

    def _seed_workflow_runtime_contract(self, connection: sqlite3.Connection) -> None:
        """Seed the official sequential Software R&D workflow template."""
        steps = [
            {
                "step_order": 1,
                "step_type": "tech_lead_breakdown",
                "step_name": "Tech Lead 接收并拆解",
                "employee_role": "tech_lead",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 2,
                "step_type": "requirement_clarification",
                "step_name": "Product Manager 补充需求",
                "employee_role": "product_manager",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 3,
                "step_type": "architecture_design",
                "step_name": "Architect 输出技术方案",
                "employee_role": "architect",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 4,
                "step_type": "frontend_execution",
                "step_name": "Frontend Engineer 执行前端任务",
                "employee_role": "frontend_engineer",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 5,
                "step_type": "backend_execution",
                "step_name": "Backend Engineer 执行后端任务",
                "employee_role": "backend_engineer",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 6,
                "step_type": "qa_verification",
                "step_name": "QA Engineer 验收",
                "employee_role": "qa_engineer",
                "required_capability_types": ["model"],
            },
            {
                "step_order": 7,
                "step_type": "final_report",
                "step_name": "Tech Lead 汇总结果",
                "employee_role": "tech_lead",
                "required_capability_types": ["model"],
            },
        ]
        connection.execute(
            """
            insert into workflow_templates (
              id, name, description, source, department_type, process_type,
              steps_json, status, updated_at
            ) values (?, ?, ?, 'official', 'software_rnd', 'sequential', ?, 'active', current_timestamp)
            on conflict(id) do nothing
            """,
            (
                "official.workflow.software_rnd_sop",
                "研发部最小 SOP",
                "Tech Lead、Product Manager、Architect、Frontend、Backend、QA 按顺序协作的最小研发流程。",
                json.dumps(steps, ensure_ascii=False),
            ),
        )

    def _seed_skill_runtime_contract(self, connection: sqlite3.Connection) -> None:
        """Seed bounded official R&D skills as prompt guidance metadata only."""
        skills = [
            (
                "official.skill.requirement_analysis",
                "requirement-analysis",
                "需求分析",
                "把 CEO 目标整理为范围、验收标准和风险。",
                "analysis",
                ["model"],
                "保持范围清晰；无法确认的事实应明确标注，而不是编造。",
            ),
            (
                "official.skill.architecture_design",
                "architecture-design",
                "架构设计",
                "为研发项目整理模块边界和实现约束。",
                "architecture",
                ["model", "tool"],
                "优先复用既有边界；不要绕过安全、租户或执行链约束。",
            ),
            (
                "official.skill.delivery_verification",
                "delivery-verification",
                "交付验证",
                "整理验证证据和已知限制。",
                "qa",
                ["model", "tool"],
                "先陈述可验证证据，再给出结论；不要暴露敏感配置。",
            ),
        ]
        connection.executemany(
            """
            insert or ignore into skill_templates (
              skill_template_id, slug, name, description, skill_type,
              default_capability_types_json, instruction_excerpt, source, tenant_id, status
            ) values (?, ?, ?, ?, ?, ?, ?, 'official', 'platform', 'active')
            """,
            [
                (
                    skill_id,
                    slug,
                    name,
                    description,
                    skill_type,
                    json.dumps(capability_types, ensure_ascii=False),
                    instruction,
                )
                for skill_id, slug, name, description, skill_type, capability_types, instruction in skills
            ],
        )

    # ── V2 P0/P1（总控已批准自主推进；降级执行：Agent 框架故障期主理人直落，待架构师/QA 复核）──
    # 目标：补齐 ai_rd 线 Skill / Tool / Workflow 真实内容，消除空壳与悬空引用。
    # 红线：不碰暂停四项（新商业包/Marketplace/收费/外部 Agent）与外部凭证/实例化/多 Agent/向量库/UI。

    def _seed_tool_templates(self, connection: sqlite3.Connection) -> None:
        """补齐 Tool Catalog（tl_*）ai_rd 包真实内容（tool-catalog-official-plan §7 表）。

        原 tool_templates 表缺失（空壳根因之一）；此处建表并 seed 30 个 ai_rd 工具，
        使 et_*/wl_* 引用的 tl_* 可解析。仅官方 ai_rd 包，不碰外部/市场内容。
        """
        connection.execute(
            """
            create table if not exists tool_templates (
              tool_template_id text primary key,
              slug text not null default '',
              name text not null,
              description text not null default '',
              tool_type text not null default 'code_execution',
              default_capability_types_json text not null default '["tool"]',
              instruction_excerpt text not null default '',
              source text not null default 'official'
                check (source in ('official','tenant_private','marketplace')),
              tenant_id text not null default 'platform',
              status text not null default 'active'
                check (status in ('draft','active','disabled','archived')),
              version text not null default '1.0.0',
              created_at text not null default current_timestamp,
              updated_at text not null default current_timestamp,
              unique (tenant_id, slug)
            )
            """
        )
        tools = [
            ("tl_ai_rd_code_executor", "code_executor", "代码执行器", "在受控沙箱中执行代码并返回结构化结果。", "code_execution"),
            ("tl_ai_rd_python_repl", "python_repl", "Python REPL", "提供交互式 Python 执行环境。", "code_execution"),
            ("tl_ai_rd_shell_terminal", "shell_terminal", "Shell 终端", "执行 shell 命令并捕获输出。", "code_execution"),
            ("tl_ai_rd_code_linter", "code_linter", "代码检查器", "静态检查代码风格与潜在缺陷。", "code_execution"),
            ("tl_ai_rd_test_runner", "test_runner", "测试运行器", "运行测试用例并汇总结果。", "code_execution"),
            ("tl_ai_rd_file_reader", "file_reader", "文件读取器", "按路径读取文件内容。", "file_io"),
            ("tl_ai_rd_file_writer", "file_writer", "文件写入器", "按路径写入文件内容。", "file_io"),
            ("tl_ai_rd_directory_search", "directory_search", "目录搜索器", "在目录树中按名/模式检索文件。", "file_io"),
            ("tl_ai_rd_git_client", "git_client", "Git 客户端", "执行 clone/commit/push 等版本操作。", "api_integration"),
            ("tl_ai_rd_github_api", "github_api", "GitHub API", "调用 GitHub REST API 管理仓库与 PR。", "api_integration"),
            ("tl_ai_rd_http_client", "http_client", "HTTP 客户端", "发起 HTTP 请求并解析响应。", "api_integration"),
            ("tl_ai_rd_graphql_client", "graphql_client", "GraphQL 客户端", "发起 GraphQL 查询与变更。", "api_integration"),
            ("tl_ai_rd_postgres_connector", "postgres_connector", "Postgres 连接器", "连接 Postgres 执行查询。", "database"),
            ("tl_ai_rd_sql_query_executor", "sql_query_executor", "SQL 执行器", "对关系库执行参数化 SQL。", "database"),
            ("tl_ai_rd_vector_db_query", "vector_db_query", "向量库查询", "执行向量相似度检索。", "vector_search"),
            ("tl_ai_rd_vector_db_upsert", "vector_db_upsert", "向量库写入", "写入/更新向量与元数据。", "vector_search"),
            ("tl_ai_rd_code_docs_search", "code_docs_search", "代码文档检索", "检索代码库与文档。", "vector_search"),
            ("tl_ai_rd_csv_parser", "csv_parser", "CSV 解析器", "解析 CSV 为结构化记录。", "data_processing"),
            ("tl_ai_rd_pandas_analyzer", "pandas_analyzer", "Pandas 分析器", "用 Pandas 做数据清洗与分析。", "data_processing"),
            ("tl_ai_rd_chart_plotter", "chart_plotter", "图表绘制器", "生成可视化图表。", "data_processing"),
            ("tl_ai_rd_pdf_parser", "pdf_parser", "PDF 解析器", "提取 PDF 文本与结构。", "document"),
            ("tl_ai_rd_docx_generator", "docx_generator", "Word 生成器", "生成 .docx 文档。", "document"),
            ("tl_ai_rd_docker_run", "docker_run", "Docker 运行器", "构建/运行容器。", "deployment"),
            ("tl_ai_rd_kubernetes_ctl", "kubernetes_ctl", "K8s 控制端", "操作 K8s 资源。", "deployment"),
            ("tl_ai_rd_ci_runner", "ci_runner", "CI 运行器", "触发并执行 CI 流水线。", "deployment"),
            ("tl_ai_rd_cloud_deploy", "cloud_deploy", "云部署器", "将产物部署到云环境。", "deployment"),
            ("tl_ai_rd_log_aggregator", "log_aggregator", "日志聚合器", "采集与聚合分散日志。", "observability"),
            ("tl_ai_rd_metric_monitor", "metric_monitor", "指标监控器", "采集与展示运行指标。", "observability"),
            ("tl_ai_rd_alert_sender", "alert_sender", "告警发送器", "按规则发送告警通知。", "observability"),
            ("tl_ai_rd_secret_resolver", "secret_resolver", "密钥解析器", "安全解析与注入密钥（不落盘明文）。", "secret"),
            # ── Pack A 研发公司工具包：外部系统连接器（P0-2 扩展，扫描自公开生态）──
            # 真实生态来源见 docs/research/domain/official-tool-catalog-v1.md；DB source 统一记 official（平台官方编目）
            ("tl_github", "github", "GitHub", "官方 GitHub MCP Server，将完整 GitHub API 暴露为工具，管理仓库/PR/Issue/Actions。", "api_integration"),
            ("tl_gitlab", "gitlab", "GitLab", "GitLab MCP Server，管理仓库、MR 与 CI 流水线。", "api_integration"),
            ("tl_postgres", "postgres", "PostgreSQL", "PostgreSQL MCP Server，自然语言查询与管理数据库（建议只读）。", "database"),
            ("tl_supabase", "supabase", "Supabase", "Supabase MCP Server，访问数据库/认证/存储等 BaaS 能力。", "database"),
            ("tl_docker", "docker", "Docker", "Docker MCP Server，管理容器与镜像生命周期。", "deployment"),
            ("tl_playwright", "playwright", "Playwright", "Playwright MCP Server，浏览器自动化与端到端测试。", "code_execution"),
            ("tl_sentry", "sentry", "Sentry", "Sentry MCP Server，获取并分析错误问题。", "observability"),
            ("tl_brave_search", "brave_search", "Brave Search", "Brave Search MCP Server，对外暴露网络检索能力。", "api_integration"),
            ("tl_slack", "slack", "Slack", "Slack MCP Server，读取/发送消息与管理频道。", "api_integration"),
            ("tl_notion", "notion", "Notion", "Notion MCP Server，读写页面/数据库/block。", "api_integration"),
            ("tl_linear", "linear", "Linear", "Linear MCP Server，管理 issue/项目/周期。", "api_integration"),
            ("tl_figma", "figma", "Figma", "Figma MCP Server，读取设计并导出资源。", "api_integration"),
            ("tl_zapier", "zapier", "Zapier", "Zapier MCP Server，连接 6000+ 应用自动化工作流。", "api_integration"),
            ("tl_n8n", "n8n", "n8n", "n8n MCP Server，可视化工作流自动化（可自托管）。", "api_integration"),
            ("tl_pipedream", "pipedream", "Pipedream", "Pipedream MCP Server，事件驱动连接 3000+ API。", "api_integration"),
            ("tl_hubspot", "hubspot", "HubSpot", "HubSpot API/Connector，CRM 与营销自动化。", "api_integration"),
            # ── Pack C 通用/基础设施/办公/框架扩展（第二轮生态扫描评估，15 条）──
            ("tl_google_drive", "google_drive", "Google Drive", "Google Drive MCP Server，访问/搜索/组织云端文件。", "knowledge"),
            ("tl_google_maps", "google_maps", "Google Maps", "Google Maps MCP Server，位置服务、路线与地点详情。", "geolocation"),
            ("tl_tavily", "tavily", "Tavily", "Tavily MCP Server，AI 原生语义搜索与结构化抽取。", "search"),
            ("tl_exa", "exa", "Exa", "Exa MCP Server，AI 搜索从非结构化网页抽取结构化数据。", "search"),
            ("tl_desktopcommander", "desktop_commander", "DesktopCommanderMCP", "终端控制、文件系统搜索与 diff 文件编辑。", "code_execution"),
            ("tl_cubesandbox", "cube_sandbox", "CubeSandbox", "AI Agent 安全沙箱，硬件级隔离执行生成代码。", "deployment"),
            ("tl_agent_memory", "agent_memory", "Agent Memory", "本地长期记忆（四层渐进管道，零外部 API 依赖）。", "memory"),
            ("tl_strix", "strix", "Strix", "AI 渗透测试，自动发现并修复应用安全漏洞。", "security"),
            ("tl_agency_agents", "agency_agents", "agency-agents", "AI 虚拟公司角色库，预定义人格/流程/交付的专家 Agent 集合。", "agent_framework"),
            ("tl_superpowers", "superpowers", "superpowers", "Agent 技能框架与软件开发方法论（可组合能力层）。", "agent_framework"),
            ("tl_agent_skills", "agent_skills", "agent-skills", "生产级 AI 编程技能库（需求到发布全流程）。", "agent_framework"),
            ("tl_officecli", "office_cli", "OfficeCLI", "Office 套件 CLI，无安装环境读写 Word/Excel/PPT。", "office"),
            ("tl_meetily", "meetily", "Meetily", "本地 AI 会议助手，实时转录与摘要（100% 本地）。", "office"),
            ("tl_activepieces", "activepieces", "Activepieces", "开源自动化平台（MIT，400+ pieces，可自托管）。", "api_integration"),
            ("tl_make", "make", "Make", "可视化多步自动化平台（1800+ 应用模块）。", "api_integration"),
            # ── Pack D 内容公司工具包（第三轮生态扫描，14 条，每条附中文介绍于目录文档）──
            ("tl_midjourney", "midjourney", "Midjourney", "AI 图像生成标杆，擅长艺术化/概念化视觉（v7）。", "content_generation"),
            ("tl_kling", "kling", "可灵 Kling", "国产文生/图生视频，4K 多镜头与人物动作自然度领先。", "content_generation"),
            ("tl_runway", "runway", "Runway", "专业 AI 视频生成与编辑（Gen-4.5、运动笔刷、合成）。", "content_generation"),
            ("tl_suno", "suno", "Suno", "文本生成完整原创歌曲（旋律+人声+编曲），含商用档。", "content_generation"),
            ("tl_elevenlabs", "elevenlabs", "ElevenLabs", "高拟真语音合成与声音克隆、多语种配音。", "content_generation"),
            ("tl_capcut", "capcut", "剪映 CapCut", "移动/桌面视频剪辑，内置 AI 字幕、抠像、节拍对齐。", "video_editing"),
            ("tl_descript", "descript", "Descript", "像编辑文字一样编辑音视频（转录即剪辑、配音替换）。", "video_editing"),
            ("tl_heygen", "heygen", "HeyGen", "数字人口播视频，多语种 Avatar 与形象定制。", "video_editing"),
            ("tl_canva", "canva", "Canva", "设计/排版与 AI 生成，品牌套件与社媒图文。", "design"),
            ("tl_adobe_firefly", "adobe_firefly", "Adobe Firefly", "商用安全的 AI 图像/视频生成，深度集成 Creative Cloud。", "content_generation"),
            ("tl_ideogram", "ideogram", "Ideogram", "含可读文字的图像生成，适合海报/卡片/社媒图。", "content_generation"),
            ("tl_wordpress", "wordpress", "WordPress", "内容发布与站点管理 CMS（文章/页面/媒体/评论）。", "cms"),
            ("tl_wechat_official", "wechat_official", "微信公众号", "图文/视频内容分发、粉丝触达与菜单管理。", "social_media"),
            ("tl_douyin_content", "douyin_content", "抖音内容", "短视频内容发布、数据看板与评论互动。", "social_media"),
            # ── Pack E 电商公司工具包（第三轮生态扫描，12 条）──
            ("tl_shopify", "shopify", "Shopify", "电商建站与店铺管理（商品/订单/客户/履约/结账）。", "ecommerce"),
            ("tl_stripe", "stripe", "Stripe", "支付网关与收单，跨 135+ 币种、强开发者 API。", "payment"),
            ("tl_paypal", "paypal", "PayPal", "国际支付与买家信任背书，覆盖广、接入简单。", "payment"),
            ("tl_alipay", "alipay", "支付宝", "国内支付、转账与商户服务能力（开放平台）。", "payment"),
            ("tl_taobao_open", "taobao_open", "淘宝开放平台", "商品/订单/物流/店铺数据接口，覆盖国内最大电商生态。", "ecommerce"),
            ("tl_jd_jos", "jd_jos", "京东 JOS", "商品/订单/库存/联盟接口，覆盖京东自营与 POP。", "ecommerce"),
            ("tl_pinduoduo", "pinduoduo", "拼多多开放平台", "商品/订单/营销/物流接口，覆盖下沉与社交电商。", "ecommerce"),
            ("tl_douyin_ecom", "douyin_ecom", "抖音电商", "商品/订单/视频/直播接口，内容电商一体化。", "ecommerce"),
            ("tl_woocommerce", "woocommerce", "WooCommerce", "基于 WordPress 的开店插件，REST API 管订单/商品/客户。", "ecommerce"),
            ("tl_youzan", "youzan", "有赞", "电商 SaaS，微商城/小程序/多渠道经营一体化。", "ecommerce"),
            ("tl_sf_express", "sf_express", "顺丰/快递100", "物流轨迹查询、电子面单与履约跟踪。", "logistics"),
            ("tl_aftership", "aftership", "Aftership", "跨承运商物流追踪与主动买家通知。", "logistics"),
            # ===== Pack F-J（第四轮，来源 curispeng22-coder/skill 仓库，去重后 28 条）=====
            ("tl_pptx", "pptx", "PPTX 文档处理", "生成/读取/编辑 PowerPoint 演示文稿。", "office"),
            ("tl_xlsx", "xlsx", "XLSX 表格处理", "生成/读取/编辑 Excel 表格与公式。", "office"),
            ("tl_pdf", "pdf", "PDF 文档处理", "生成/读取/拆分/合并 PDF 文档。", "office"),
            ("tl_docx", "docx", "DOCX 文档处理", "生成/读取/编辑 Word 文档。", "office"),
            ("tl_product_manager_toolkit", "product_manager_toolkit", "产品经理工具包", "需求拆解/PRD草拟/竞品梳理/路线图。", "product"),
            ("tl_ai_drawio", "ai_drawio", "AI Drawio 流程图", "自动绘制流程图/架构图/时序图。", "design"),
            ("tl_frontend_design", "frontend_design", "前端设计", "前端页面/UI 设计与代码生成。", "design"),
            ("tl_nanobanana_ppt", "nanobanana_ppt", "AI PPT 生成", "按主题自动生成带视觉的演示稿。", "ppt"),
            ("tl_content_publisher", "content_publisher", "内容创作发布器", "内容创作与发布全流程编排。", "content"),
            ("tl_article_illustrator", "article_illustrator", "文章配图", "为文章自动生成/匹配插图。", "content"),
            ("tl_url_to_markdown", "url_to_markdown", "URL 转 Markdown", "抓取网页并转为干净 Markdown。", "content"),
            ("tl_format_markdown", "format_markdown", "Markdown 格式化", "规范化/美化 Markdown 文档。", "content"),
            ("tl_post_to_x", "post_to_x", "发推助手", "将内容发布到 X（Twitter）。", "content"),
            ("tl_xhs_images", "xhs_images", "小红书配图", "生成适配小红书的图文卡片。", "content"),
            ("tl_video_suite", "video_suite", "视频创作套件", "原创/二创/分析三种模式的视频生产流。", "video"),
            ("tl_video_collaborator", "video_collaborator", "视频协作", "多人/多Agent协同视频制作。", "video"),
            ("tl_video_recreation", "video_recreation", "视频二创", "基于原视频做混剪/解说/改版。", "video"),
            ("tl_video_frame_extractor", "video_frame_extractor", "视频抽帧", "提取视频关键帧/批量截图。", "video"),
            ("tl_viral_video_copy", "viral_video_copy", "爆款视频文案", "生成高传播力短视频脚本/标题。", "content"),
            ("tl_tts_voice", "tts_voice", "语音合成", "音色克隆/拟人化配音/流式生成。", "audio"),
            ("tl_qwen_asr", "qwen_asr", "语音识别", "语音转文字/字幕生成。", "audio"),
            ("tl_infinitetalk", "infinitetalk", "数字人配音", "音频驱动的稀疏帧视频配音。", "digital_human"),
            ("tl_ecom_copywriter", "ecom_copywriter", "电商文案", "生成商品标题/详情/卖点文案。", "marketing"),
            ("tl_ecom_video_marketing", "ecom_video_marketing", "电商视频营销", "生成带货短视频脚本与分镜。", "marketing"),
            ("tl_product_copywriter", "product_copywriter", "产品营销文案", "针对单品的营销文案与卖点提炼。", "marketing"),
            ("tl_product_video", "product_video", "产品视频", "生成产品展示/功能演示视频。", "video"),
            ("tl_paper_analysis", "paper_analysis", "论文分析", "学术文献摘要与对比分析。", "analysis"),
            ("tl_contract_review", "contract_review", "合同审查", "合同条款风险点识别与摘要。", "analysis"),
        ]
        connection.executemany(
            """
            insert or ignore into tool_templates
              (tool_template_id, slug, name, description, tool_type,
               default_capability_types_json, instruction_excerpt, source, tenant_id, status, version)
            values (?, ?, ?, ?, ?, '["tool"]', ?, 'official', 'platform', 'active', '1.0.0')
            """,
            [(tid, slug, name, desc, ttype, desc) for (tid, slug, name, desc, ttype) in tools],
        )

    def _seed_skill_templates_airnd(self, connection: sqlite3.Connection) -> None:
        """补齐 Skill Catalog（skl_*）ai_rd 包完整 52 个技能真实内容（Pack A）。

        覆盖：员工模板/研发 SOP 直接引用的关键技能 + 其余 43 个同模式增量，
        消除 skl_* 空壳，使 ai_rd Skill Pack 达成 catalog v1 的 ≥50 数量目标。
        降级执行：Agent 框架故障期主理人直落，待架构师/QA 独立复核。
        """
        skills = [
            ("skl_ai_rd_requirement_analysis", "ai-rd-requirement-analysis", "需求分析", "将模糊的用户诉求拆解为结构化、可验证的产品需求。", "analysis", "产品"),
            ("skl_ai_rd_system_design", "system-design", "架构设计", "为研发项目整理模块边界、技术选型与实现约束。", "architecture", "架构"),
            ("skl_ai_rd_python_development", "python-development", "Python 开发", "使用 Python 实现后端与脚本功能，遵循可读、可测试、可维护实践。", "development", "开发"),
            ("skl_ai_rd_test_design", "test-design", "测试设计", "设计单元/集成测试用例与可验证的验收标准。", "qa", "测试"),
            ("skl_ai_rd_prd_design", "prd-design", "PRD 设计", "撰写产品需求文档，定义目标、范围与验收标准。", "analysis", "产品"),
            ("skl_ai_rd_release_planning", "release-planning", "发布规划", "规划发布节奏、回滚预案与上线检查单。", "release", "运维"),
            ("skl_ai_rd_api_design", "api-design", "API 设计", "设计 REST/GraphQL API 契约、版本与错误规范。", "architecture", "架构"),
            ("skl_ai_rd_database_design", "database-design", "数据库设计", "设计表结构、索引与迁移策略，保证一致性与性能。", "development", "开发"),
            ("skl_ai_rd_code_review", "ai-rd-code-review", "代码评审", "审查代码质量、可读性与潜在风险，给出可执行的改进建议。", "review", "架构"),
            # ── 以下 43 个补全 Pack A 全部 52 个 ai_rd 技能（P0-1 完整包）──
            ("skl_ai_rd_user_story_writing", "ai-rd-user-story-writing", "用户故事编写", "以「作为…我想要…以便…」格式编写可验收的用户故事。", "analysis", "产品"),
            ("skl_ai_rd_competitive_analysis", "ai-rd-competitive-analysis", "竞品分析", "研究竞品并产出竞争格局与差异化机会。", "analysis", "产品"),
            ("skl_ai_rd_product_roadmap", "ai-rd-product-roadmap", "产品路线图", "制定分版本的产品路线图与里程碑。", "analysis", "产品"),
            ("skl_ai_rd_acceptance_criteria_design", "ai-rd-acceptance-criteria-design", "验收标准设计", "为需求定义可测试的验收标准（DoD/AC）。", "analysis", "产品"),
            ("skl_ai_rd_feature_prioritization", "ai-rd-feature-prioritization", "功能优先级排序", "用结构化方法对功能需求做优先级排序。", "analysis", "产品"),
            ("skl_ai_rd_user_research", "ai-rd-user-research", "用户研究", "通过访谈/问卷/数据挖掘理解用户真实问题。", "analysis", "产品"),
            ("skl_ai_rd_product_metrics_definition", "ai-rd-product-metrics-definition", "产品指标定义", "定义北极星指标与分层产品度量体系。", "analysis", "产品"),
            ("skl_ai_rd_tech_selection", "ai-rd-tech-selection", "技术选型", "基于约束做技术栈与中间件选型。", "architecture", "架构"),
            ("skl_ai_rd_performance_design", "ai-rd-performance-design", "性能设计", "在设计阶段预留性能与容量方案。", "architecture", "架构"),
            ("skl_ai_rd_security_design", "ai-rd-security-design", "安全设计", "在设计阶段嵌入安全与合规控制。", "architecture", "安全"),
            ("skl_ai_rd_architecture_review", "ai-rd-architecture-review", "架构评审", "对方案做架构评审与质量门禁。", "architecture", "架构"),
            ("skl_ai_rd_microservice_design", "ai-rd-microservice-design", "微服务设计", "设计微服务边界、通信与治理。", "architecture", "架构"),
            ("skl_ai_rd_data_modeling", "ai-rd-data-modeling", "数据建模", "面向分析与应用设计数据模型与口径。", "development", "数据"),
            ("skl_ai_rd_integration_design", "ai-rd-integration-design", "集成设计", "设计第三方/内部系统对接方案。", "architecture", "架构"),
            ("skl_ai_rd_scalability_design", "ai-rd-scalability-design", "可扩展设计", "设计可水平扩展的架构方案。", "architecture", "架构"),
            ("skl_ai_rd_react_development", "ai-rd-react-development", "React 开发", "使用 React 实现前端组件与页面。", "development", "开发"),
            ("skl_ai_rd_backend_development", "ai-rd-backend-development", "后端开发", "实现服务端逻辑、接口与数据访问。", "development", "开发"),
            ("skl_ai_rd_frontend_development", "ai-rd-frontend-development", "前端开发", "实现前端页面、交互与性能优化。", "development", "开发"),
            ("skl_ai_rd_debugging", "ai-rd-debugging", "缺陷调试", "定位并修复缺陷与异常。", "development", "开发"),
            ("skl_ai_rd_refactoring", "ai-rd-refactoring", "代码重构", "在不改行为前提下改善代码结构。", "development", "开发"),
            ("skl_ai_rd_concurrency_programming", "ai-rd-concurrency-programming", "并发编程", "实现并发/并行与异步任务处理。", "development", "开发"),
            ("skl_ai_rd_algorithm_implementation", "ai-rd-algorithm-implementation", "算法实现", "实现与优化算法与数据结构。", "development", "开发"),
            ("skl_ai_rd_api_implementation", "ai-rd-api-implementation", "API 实现", "按契约实现并自测 API。", "development", "开发"),
            ("skl_ai_rd_sql_development", "ai-rd-sql-development", "SQL 开发", "编写高效、正确的 SQL 与数据访问层。", "development", "开发"),
            ("skl_ai_rd_test_driven_development", "ai-rd-test-driven-development", "测试驱动开发", "以测试先行驱动实现。", "development", "开发"),
            ("skl_ai_rd_typescript_development", "ai-rd-typescript-development", "TypeScript 开发", "使用 TypeScript 实现类型安全的应用。", "development", "开发"),
            ("skl_ai_rd_git_workflow", "ai-rd-git-workflow", "Git 工作流", "规范分支管理与协作提交。", "development", "开发"),
            ("skl_ai_rd_mobile_development", "ai-rd-mobile-development", "移动端开发", "实现移动端（iOS/Android）功能与适配。", "development", "开发"),
            ("skl_ai_rd_documentation_writing", "ai-rd-documentation-writing", "技术文档编写", "编写技术文档、README 与接口说明。", "development", "开发"),
            ("skl_ai_rd_data_pipeline_development", "ai-rd-data-pipeline-development", "数据管道开发", "开发数据采集、清洗与调度管道。", "development", "数据"),
            ("skl_ai_rd_automated_testing", "ai-rd-automated-testing", "自动化测试", "编写并执行自动化测试（单元/接口/UI）。", "qa", "测试"),
            ("skl_ai_rd_performance_testing", "ai-rd-performance-testing", "性能测试", "设计并执行性能/压测与容量验证。", "qa", "测试"),
            ("skl_ai_rd_integration_testing", "ai-rd-integration-testing", "集成测试", "验证多模块/多服务协作正确性。", "qa", "测试"),
            ("skl_ai_rd_regression_testing", "ai-rd-regression-testing", "回归测试", "回归验证避免改动引入退化。", "qa", "测试"),
            ("skl_ai_rd_test_retrospective", "ai-rd-test-retrospective", "测试复盘", "对测试过程与缺陷做复盘与改进。", "qa", "测试"),
            ("skl_ai_rd_dockerization", "ai-rd-dockerization", "容器化", "将应用容器化并优化镜像。", "release", "DevOps"),
            ("skl_ai_rd_cicd_pipeline", "ai-rd-cicd-pipeline", "CI/CD 流水线", "搭建持续集成与持续交付流水线。", "release", "DevOps"),
            ("skl_ai_rd_deployment", "ai-rd-deployment", "应用部署", "执行安全可控的应用部署。", "release", "DevOps"),
            ("skl_ai_rd_monitoring", "ai-rd-monitoring", "监控可观测", "建设指标/日志/链路三位一体可观测性。", "release", "DevOps"),
            ("skl_ai_rd_canary_release", "ai-rd-canary-release", "灰度发布", "以灰度发布控制上线风险。", "release", "DevOps"),
            ("skl_ai_rd_infrastructure_as_code", "ai-rd-infrastructure-as-code", "基础设施即代码", "用代码声明与管理基础设施。", "release", "DevOps"),
            ("skl_ai_rd_log_analysis", "ai-rd-log-analysis", "日志分析", "通过日志定位问题与异常模式。", "release", "DevOps"),
            ("skl_ai_rd_incident_response", "ai-rd-incident-response", "故障响应", "对线上故障做响应、止损与复盘。", "release", "DevOps"),
        ]
        connection.executemany(
            """
            insert or ignore into skill_templates
              (skill_template_id, slug, name, description, skill_type,
               default_capability_types_json, instruction_excerpt, source, tenant_id, status, version, category)
            values (?, ?, ?, ?, ?, '["model"]', ?, 'official', 'platform', 'active', '1.0.0', ?)
            """,
            [(sid, slug, name, desc, stype, desc, cat) for (sid, slug, name, desc, stype, cat) in skills],
        )

    def _annotate_tool_capability(self, connection: sqlite3.Connection) -> None:
        """R2 item7：Tool 能力态标注（C）。幂等 UPDATE。

        默认态：全部目录可见 + Mock/Stub、未配置未执行（与复盘「工具默认
        tool_functions=None、第三方连接器全 mock」一致）。真实执行能力
        （configured=1 时 executable=1、mock_or_stub=0）留作 L2 后钩子，本期
        不触发，确保 executable 与 mock_or_stub 互斥不变量。
        """
        connection.execute(
            """
            update tool_templates
            set catalog_visible = 1, configured = 0, executable = 0, mock_or_stub = 1
            where catalog_visible is null or mock_or_stub is null
            """
        )

    def _seed_workflow_template_containers(self, connection: sqlite3.Connection) -> None:
        """补齐 Workflow Template 容器（wt_*）ai_rd 线 16 个。

        wl_* 的 workflow_template_ref 已正确指向 wt_{workflow_name}，但 wt_* 容器
        此前缺失（空壳根因之二）。此处创建 ai_rd 线 16 个 wt_* 容器，使引用闭环。
        内容/商业线属暂停项（新商业包 L2 Gate），本批不创建。
        """
        containers = [
            ("wt_software_dev_sop", "软件研发 SOP", ["需求理解", "任务拆解", "架构设计", "编码", "测试", "交付"]),
            ("wt_requirement_to_prd", "需求转 PRD", ["需求澄清", "干系人对齐", "PRD 撰写"]),
            ("wt_system_design_sop", "系统设计方案", ["边界划分", "技术选型", "接口设计"]),
            ("wt_api_dev_sop", "API 开发 SOP", ["契约定义", "实现", "联调"]),
            ("wt_feature_dev_sop", "特性开发 SOP", ["拆解", "实现", "自测"]),
            ("wt_tdd_sop", "TDD SOP", ["红", "绿", "重构"]),
            ("wt_code_review_sop", "代码评审 SOP", ["静态检查", "逻辑评审", "结论"]),
            ("wt_bugfix_sop", "缺陷修复 SOP", ["复现", "定位", "修复", "验证"]),
            ("wt_ci_cd_sop", "CI/CD SOP", ["构建", "测试门禁", "部署"]),
            ("wt_data_pipeline_sop", "数据管道 SOP", ["抽取", "清洗", "加载"]),
            ("wt_database_migration_sop", "数据库迁移 SOP", ["备份", "变更", "校验"]),
            ("wt_security_review_sop", "安全评审 SOP", ["威胁建模", "审计", "加固"]),
            ("wt_incident_response_sop", "事件响应 SOP", ["检测", "遏制", "恢复"]),
            ("wt_performance_tuning_sop", "性能调优 SOP", ["度量", "瓶颈定位", "优化"]),
            ("wt_microservice_bootstrap_sop", "微服务启动 SOP", ["骨架", "治理", "联通"]),
            ("wt_tech_spike_sop", "技术预研 SOP", ["目标", "验证", "结论"]),
        ]
        connection.executemany(
            """
            insert into workflow_templates
              (id, name, description, source, department_type, process_type, steps_json, status, updated_at)
            values (?, ?, ?, 'official', 'software_rnd', 'sequential', ?, 'active', current_timestamp)
            on conflict(id) do nothing
            """,
            [
                (wid, name, f"{name}：标准研发流程资产（ai_rd）。", json.dumps(steps, ensure_ascii=False))
                for (wid, name, steps) in containers
            ],
        )

    def _seed_rd_pipeline_workflow(self, connection: sqlite3.Connection) -> None:
        """新增 wt_rd_pipeline：R&D 流水线，含 code_change 步骤元数据。"""
        steps = [
            {"step_order": 1, "step_type": "task_breakdown", "step_name": "任务拆解", "employee_role": "tech_lead",
             "required_capability_types": ["model"]},
            {"step_order": 2, "step_type": "architecture_design", "step_name": "架构设计", "employee_role": "architect",
             "required_capability_types": ["model"]},
            {"step_order": 3, "step_type": "code_change", "step_name": "编码", "employee_role": "backend_engineer",
             "required_capability_types": ["model", "tool"],
             "code_change_spec": {
                 "target_files": [],
                 "test_command_id": "",
                 "test_command_argv": [],
                 "allow_paths": [],
                 "max_rounds": 3,
             }},
            {"step_order": 4, "step_type": "qa_verification", "step_name": "测试", "employee_role": "qa_engineer",
             "required_capability_types": ["model", "tool"]},
            {"step_order": 5, "step_type": "code_review", "step_name": "代码审查", "employee_role": "tech_lead",
             "required_capability_types": ["model"]},
            {"step_order": 6, "step_type": "delivery", "step_name": "交付", "employee_role": "tech_lead",
             "required_capability_types": ["model"]},
        ]
        connection.execute(
            "insert into workflow_templates "
            "(id, name, description, source, department_type, process_type, steps_json, status, updated_at) "
            "values (?, ?, ?, 'official', 'software_rnd', 'sequential', ?, 'active', current_timestamp) "
            "on conflict(id) do nothing",
            ("wt_rd_pipeline", "R&D 流水线", "研发部完整流水线：任务拆解→架构→编码→测试→审查→交付。",
             json.dumps(steps, ensure_ascii=False)),
        )

    def _annotate_workflow_capability(self, connection: sqlite3.Connection, existing_ids: set[str]) -> None:
        """R2 item8：只标注本轮新增的 Workflow，保留既有授权状态。

        推导规则（对齐基线 item8）：steps_json 为带 step_type 的对象数组 →
        structured_executable；纯字符串壳 → design_only。当前 18 条实测：
        official.workflow.software_rnd_sop / official.workflow.content_growth_sop
        为结构化可执行（steps_json 含 step_type 对象数组），其余 16 条 wt_* 为
        字符串壳（design_only，列默认值已赋值）。

        注意：workflow_capability_status 列默认 'design_only'，故 16 条 wt_* 已就位；
        这里仅把本轮新插入的 2 条 official.workflow.* 显式提升为 structured_executable。
        """
        for workflow_id in ('official.workflow.software_rnd_sop', 'official.workflow.content_growth_sop', 'wt_rd_pipeline'):
            if workflow_id not in existing_ids:
                connection.execute(
                    "update workflow_templates set workflow_capability_status = 'structured_executable' where id = ?",
                    (workflow_id,),
                )

    def _seed_company_package_workflow_bridges(
        self, connection: sqlite3.Connection
    ) -> None:
        """Publish the approved immutable v1 package/workflow bridge.

        This controlled seed is the Admin-owned versioned asset publication
        path.  ``insert or ignore`` deliberately never rewrites a consumed
        bridge or an existing package/workflow version.
        """
        connection.execute(
            """
            insert or ignore into company_package_workflow_bridges (
              bridge_id, company_package_id, package_version,
              source_workflow_content_id, source_workflow_content_version,
              workflow_template_id, workflow_template_version,
              workflow_capability_status, source, tenant_id, status
            ) values (?, ?, ?, ?, ?, ?, ?, 'structured_executable',
                      'Curis internal', 'platform', 'active')
            """,
            (
                "bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0",
                "ccp_ai_software_company",
                "1.0.0",
                "wl_ai_rd_software_dev_sop",
                "1.0.0",
                "official.workflow.software_rnd_sop",
                "1.0.0",
            ),
        )

    def _reconcile_legacy_orphan_instances(self, connection: sqlite3.Connection) -> None:
        """Safely resolve legacy template aliases without deleting instance data."""
        employee_refs = (
            ("department_instances", "manager_employee_id"),
            ("employee_capability_bindings", "employee_id"),
            ("employee_context_manifests", "employee_id"),
            ("employee_role_guard_audits", "employee_id"),
            ("employee_session_audit_events", "employee_id"),
            ("employee_sessions", "employee_id"),
            ("employee_skill_bindings", "employee_id"),
            ("employee_working_memory_audits", "employee_id"),
            ("employee_working_memory_checkpoints", "employee_id"),
            ("step_assignments", "employee_id"),
            ("step_results", "employee_id"),
            ("tasks", "employee_id"),
            ("workflow_recovery_attempts", "employee_id"),
        )
        department_refs = (
            ("content_workflow_runs", "department_id"),
            ("projects", "department_id"),
            ("workflow_runs", "department_id"),
        )
        tables = {
            row["name"]
            for row in connection.execute(
                "select name from sqlite_master where type = 'table'"
            ).fetchall()
        }

        def is_referenced(refs: tuple[tuple[str, str], ...], instance_id: str) -> bool:
            return any(
                connection.execute(
                    f"select 1 from {table} where {column} = ? limit 1", (instance_id,)
                ).fetchone()
                for table, column in refs
                if table in tables
            )

        orphan_employees = connection.execute(
            "select ei.id, ei.role from employee_instances ei "
            "left join employee_templates et on et.id = ei.template_id "
            "where et.id is null"
        ).fetchall()
        for row in orphan_employees:
            matches = connection.execute(
                "select id from employee_templates "
                "where role = ? and status = 'active' and enabled = 1",
                (row["role"],),
            ).fetchall()
            if len(matches) == 1 and not is_referenced(employee_refs, row["id"]):
                connection.execute(
                    "update employee_instances set template_id = ? where id = ?",
                    (matches[0]["id"], row["id"]),
                )
            else:
                connection.execute(
                    "update employee_instances set status = 'deprecated', enabled = 0 where id = ?",
                    (row["id"],),
                )

        # Exact first-launch aliases are the same department identity. Preserve all
        # relationships and lifecycle flags, including any prior archive.
        for kind in ("content_growth", "music"):
            legacy_template = f"official.department.{kind}"
            target = FIRST_LAUNCH_DEPARTMENT_TEMPLATES[kind]
            candidates = connection.execute(
                "select di.id, di.tenant_id, di.company_id, c.ceo_id from department_instances di "
                "join companies c on c.company_id = di.company_id and c.tenant_id = di.tenant_id "
                "where di.template_id = ? and di.department_type = ? and di.deleted_at is null "
                "and not exists (select 1 from department_templates where id = ?) "
                "and exists (select 1 from department_templates where id = ? and enabled = 1)",
                (legacy_template, kind, legacy_template, target),
            ).fetchall()
            for row in candidates:
                identity = f"{row['tenant_id']}:{row['ceo_id']}:{row['company_id']}"
                suffix = hashlib.sha256(identity.encode()).hexdigest()[:24]
                if row["id"] == f"department-launch-{suffix}-{kind}":
                    connection.execute(
                        "update department_instances set template_id = ? where id = ?",
                        (target, row["id"]),
                    )

        legacy_departments = {
            "dt_ai_rd": "dt_engineering",
            "dt_ai_content": "official.department.content_growth",
        }
        orphan_departments = connection.execute(
            "select di.id, di.template_id from department_instances di "
            "left join department_templates dt on dt.id = di.template_id "
            "where dt.id is null"
        ).fetchall()
        for row in orphan_departments:
            target = legacy_departments.get(row["template_id"])
            target_exists = target and connection.execute(
                "select 1 from department_templates where id = ? and enabled = 1", (target,)
            ).fetchone()
            if target_exists and not is_referenced(department_refs, row["id"]):
                connection.execute(
                    "update department_instances set template_id = ? where id = ?",
                    (target, row["id"]),
                )
            else:
                connection.execute(
                    "update department_instances set status = 'archived', enabled = 0 where id = ?",
                    (row["id"],),
                )

    def _seed_persona_image_refs(self, connection: sqlite3.Connection) -> None:
        """P1-1：为 6 个官方 Persona 注入「形象」字段（头像/昵称/身份描述）。

        image_ref_json 由 _ensure_column 已加；此处填充内容。仅官方 6 原型，
        不立新资产类（规避 L2 #7）。avatar 留空（前端按昵称生成占位）。
        """
        images = {
            "pt_direct_executor": ("直行", "雷厉风行的执行者，说一不二。"),
            "pt_analytical_advisor": ("析言", "冷静缜密的分析者，用数据说话。"),
            "pt_balanced_facilitator": ("衡之", "居中调和的协调者，兼顾多方。"),
            "pt_supportive_coach": ("伴行", "耐心陪伴的教练，重在成长。"),
            "pt_creative_explorer": ("探创", "天马行空的探索者，敢想敢试。"),
            "pt_risk_aware_guardian": ("守垣", "审慎周全的守护者，先避风险。"),
        }
        for pid, (nickname, identity) in images.items():
            connection.execute(
                "update persona_templates set image_ref_json = ? where persona_id = ?",
                (json.dumps({"avatar": "", "nickname": nickname, "identity": identity}, ensure_ascii=False), pid),
            )

    # ── Phase-1 Asset Factory Consolidation (Gate C/D/E/F) 官方资产工厂目录 ──
    # 以下方法覆盖新增的 7 张表（company_packages / company_templates /
    # persona_templates / dashboard_templates / workflow_contents /
    # dashboard_widget_catalog / template_version_snapshots）的 seed、读取与
    # 快照写入。写路径由 catalog_authoring.py / company_instantiation.py 经
    # self.connect() 直接执行；此处仅提供幂等 seed 与只读投影 + 快照写入。

    def _seed_phase1_asset_factory(self, connection: sqlite3.Connection) -> None:
        """幂等种子：填充 Phase-1 官方资产工厂目录内容（Gate C/D/E/F 演示闭环）。

        所有官方 pt_*/et_*/dt_*/ct_*/dtpl_*/wl_*/ccp_* 真实 id 均来自各
        design-only plan（employee-persona-system-plan / workflow-official-content-plan /
        dashboard-official-content-plan / company-package-official-content-plan），无编造。
        现有 official.* 种子行保留兼容，新 Phase-1 行叠加写入（不重命名、不删除）。
        """
        self._seed_dashboard_widget_catalog(connection)
        self._seed_persona_templates(connection)
        self._seed_employee_templates_phase1(connection)
        self._seed_department_templates_phase1(connection)
        self._seed_company_templates_phase1(connection)
        self._seed_dashboard_templates(connection)
        self._seed_workflow_contents(connection)
        self._seed_company_packages(connection)

    def _seed_dashboard_widget_catalog(self, connection: sqlite3.Connection) -> None:
        """Gate C §2.2 Widget Catalog 单一真相源（16 类规范 widget）。

        仅存规范 widget_id（去重后）；token_cost→ai_cost / tech_risk→project_risk
        别名由服务层 normalize_widget_id 归一，目录本身不保留别名。
        """
        widgets = [
            ("company_health", "company", None, "公司健康", "Company 状态、活跃项目与阻塞事实"),
            ("department_overview", "department", None, "部门概览", "Department 状态与员工数量"),
            ("project_progress", "project", None, "项目进度", "Project / WorkflowRun 进度"),
            ("project_risk", "project", "tech", "项目风险", "blocked / failed 事实、缺失负责人或能力（含技术风险细分）"),
            ("employee_status", "employee", None, "员工状态", "创建、启用、工作、等待、停用状态"),
            ("employee_load", "employee", None, "员工负载", "活跃 Step / Task 数量"),
            ("token_usage", "cost", None, "Token 用量", "Token 消耗"),
            ("model_usage", "cost", None, "模型用量", "模型调用次数与 Token 分布"),
            ("ai_cost", "cost", None, "AI 成本", "estimated_cost 聚合；非账单（与 cmcf_* 严格隔离）"),
            ("operation_cost", "cost", None, "运营成本", "运营相关成本聚合"),
            ("value_event", "value", None, "价值事件", "已记录价值事件（契约预留）"),
            ("content_output", "value", None, "内容产出", "内容产出量度"),
            ("publish_metrics", "value", None, "发布指标", "发布相关指标"),
            ("viral_trend", "value", None, "传播趋势", "内容传播趋势"),
            ("capability_coverage", "capability", None, "能力覆盖", "官方能力覆盖度"),
            ("knowledge_index", "knowledge", None, "知识索引", "知识库索引状态"),
        ]
        connection.executemany(
            "insert or ignore into dashboard_widget_catalog "
            "(widget_id, domain, data_class, title, description, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, 'official', 'platform', 1)",
            [(w[0], w[1], w[2], w[3], w[4]) for w in widgets],
        )

    def _seed_persona_templates(self, connection: sqlite3.Connection) -> None:
        """PersonaTemplate 内容实例（employee-persona-system-plan §2.5 六原型）。"""
        personas = [
            (
                "pt_supportive_coach", "supportive-coach", "Supportive Coach", "supportive_coach",
                ["鼓励", "建设性反馈", "辅导"],
                {"tone": "encouraging", "format": "bullet_points"},
                {"format": "bullet_points", "frequency": "per-milestone"},
                "consultative",
                {"style": "collaborative", "decision": "consensus-oriented"},
                "以鼓励与建设性反馈为主，辅导/评审类岗位首选",
            ),
            (
                "pt_direct_executor", "direct-executor", "Direct Executor", "direct_executor",
                ["直接", "简洁", "重结果"],
                {"tone": "terse", "format": "bullet_points"},
                {"format": "bullet_points", "frequency": "on-demand"},
                "autonomous",
                {"style": "independent", "decision": "decisive"},
                "直接、简洁、重结果，少寒暄，交付导向",
            ),
            (
                "pt_analytical_advisor", "analytical-advisor", "Analytical Advisor", "analytical_advisor",
                ["数据驱动", "严谨", "证据优先"],
                {"tone": "neutral", "format": "data_driven"},
                {"format": "data_driven", "frequency": "per-analysis"},
                "evidence_based",
                {"style": "deliberative", "decision": "evidence-weighted"},
                "数据驱动、严谨、给结论前先给证据",
            ),
            (
                "pt_creative_explorer", "creative-explorer", "Creative Explorer", "creative_explorer",
                ["发散", "举例丰富", "鼓励尝试"],
                {"tone": "playful", "format": "narrative"},
                {"format": "narrative", "frequency": "per-iteration"},
                "exploratory",
                {"style": "brainstorming", "decision": "option-rich"},
                "发散、举例丰富、鼓励尝试，适合内容/增长",
            ),
            (
                "pt_balanced_facilitator", "balanced-facilitator", "Balanced Facilitator", "balanced_facilitator",
                ["平衡", "协商", "文档化"],
                {"tone": "neutral", "format": "bullet_points"},
                {"format": "bullet_points", "frequency": "per-handoff"},
                "consultative",
                {"style": "facilitative", "decision": "consensus-oriented"},
                "平衡各方、协商决策、文档化交接",
            ),
            (
                "pt_risk_aware_guardian", "risk-aware-guardian", "Risk Aware Guardian", "risk_aware_guardian",
                ["审慎", "风险优先", "合规"],
                {"tone": "cautious", "format": "risk_first"},
                {"format": "risk_first", "frequency": "per-change"},
                "conservative",
                {"style": "guarded", "decision": "risk-averse"},
                "审慎、风险优先、合规把关",
            ),
        ]
        connection.executemany(
            "insert or ignore into persona_templates "
            "(persona_id, slug, name, archetype, traits_json, communication_style_json, "
            "reporting_style_json, decision_style, collaboration_style_json, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, '1.0.0', 'active', 'official', 'platform', 1)",
            [
                (
                    pid, slug, name, archetype,
                    json.dumps(traits, ensure_ascii=False),
                    json.dumps(comm, ensure_ascii=False),
                    json.dumps(report, ensure_ascii=False),
                    decision,
                    json.dumps(collab, ensure_ascii=False),
                )
                for (pid, slug, name, archetype, traits, comm, report, decision, collab, _desc) in personas
            ],
        )

    def _seed_employee_templates_phase1(self, connection: sqlite3.Connection) -> None:
        """Phase-1 EmployeeTemplate（et_*）叠加种子，含 persona_ref / default_skill / default_tool 绑定。

        与既有 official.employee.* 行并存（不重命名）；department_type='software_rnd'
        以匹配 Gate F 实例化的 dt_engineering 部门。
        """
        employees = [
            (
                "et_backend_engineer", "backend-engineer", "Backend Engineer", "backend_engineer",
                "实现 Workspace 后端数据模型、API 和测试。",
                "et_backend_engineer：保持租户隔离、usage_event 归因和模型网关适配器路径不漂移；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_direct_executor", "skl_ai_rd_python_development", "tl_ai_rd_code_executor",
            ),
            (
                "et_frontend_engineer", "frontend-engineer", "Frontend Engineer", "frontend_engineer",
                "实现 Workspace 前端界面和交互状态。",
                "et_frontend_engineer：在既有工作台内实现最小 UI，不新增复杂组织图或业务模块；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_direct_executor", "skl_ai_rd_python_development", "tl_ai_rd_code_executor",
            ),
            (
                "et_architect", "architect", "Architect", "architect",
                "定义系统边界、数据模型、API 和模块风险。",
                "et_architect：优先复用现有架构，避免未批准的执行链路和平台边界变更；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_analytical_advisor", "skl_ai_rd_system_design", "tl_ai_rd_code_linter",
            ),
            (
                "et_tech_lead", "tech-lead", "Tech Lead", "tech_lead",
                "接收研发任务，拆解执行路径，并在任务结束后汇总交付证据。",
                "et_tech_lead：优先保持范围清晰、风险可控、证据完整；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_balanced_facilitator", "skl_ai_rd_requirement_analysis", "tl_ai_rd_git_client",
            ),
            (
                "et_product_manager", "product-manager", "Product Manager", "product_manager",
                "理解 CEO 需求，确认范围、验收标准和不做事项。",
                "et_product_manager：把任务转成清晰的产品范围和验收标准，发现范围冲突时停止升级；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_supportive_coach", "skl_ai_rd_requirement_analysis", "tl_ai_rd_git_client",
            ),
            (
                "et_qa_engineer", "qa-engineer", "QA Engineer", "qa_engineer",
                "执行验证、回归测试、范围扫描和验收证据整理。",
                "et_qa_engineer：验证现有功能不回退，所有完成声明必须有新鲜证据；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步（见 docs/ai-development-organization/ceo-reporting-standard.md）。",
                "pt_supportive_coach", "skl_ai_rd_test_design", "tl_ai_rd_test_runner",
            ),
        ]
        connection.executemany(
            "insert or ignore into employee_templates "
            "(id, slug, name, role, responsibility, department_type, "
            "default_instructions, default_capability_types_json, default_model_policy_json, "
            "default_workflow_step_types_json, guardrails_json, persona_ref, default_skill, default_tool, "
            "version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, 'software_rnd', ?, '[\"model\",\"tool\"]', '{}', '[]', '[]', ?, ?, ?, "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            [
                (
                    eid, slug, name, role, responsibility, instructions,
                    persona_ref, default_skill, default_tool,
                )
                for (eid, slug, name, role, responsibility, instructions, persona_ref, default_skill, default_tool) in employees
            ],
        )

    def _seed_devops_engineer(self, connection: sqlite3.Connection) -> None:
        """新增 et_devops_engineer 员工模板。"""
        connection.execute(
            "insert or ignore into employee_templates "
            "(id, slug, name, role, responsibility, department_type, "
            "default_instructions, default_capability_types_json, default_model_policy_json, "
            "default_workflow_step_types_json, guardrails_json, persona_ref, default_skill, default_tool, "
            "version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, 'software_rnd', ?, '[\"model\",\"tool\"]', '{}', '[]', '[]', ?, ?, ?, "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            (
                "et_devops_engineer", "devops-engineer", "DevOps Engineer", "devops_engineer",
                "维护 CI/CD 管道、部署环境和基础设施上下线。",
                "et_devops_engineer：确保 CI 门禁不退化、部署环境凭据不泄露；"
                "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，不堆技术术语与 Contract 引用，"
                "风险直说，需决策时给明确下一步。",
                "pt_direct_executor", "skl_ai_rd_cicd_pipeline", "tl_ai_rd_ci_runner",
            ),
        )

    def _seed_department_templates_phase1(self, connection: sqlite3.Connection) -> None:
        """Phase-1 DepartmentTemplate（dt_engineering）叠加种子，供 Gate F 实例化。"""
        employee_ids = [
            "et_backend_engineer", "et_frontend_engineer", "et_architect",
            "et_tech_lead", "et_product_manager", "et_qa_engineer",
        ]
        connection.execute(
            "insert or ignore into department_templates "
            "(id, slug, name, department_type, description, default_employee_templates_json, "
            "default_workflow_template_id, default_capability_types_json, version, status, source, tenant_id, enabled) "
            "values (?, 'engineering', 'Engineering Department', 'software_rnd', "
            "'第一版 AI 公司研发部，包含产品、架构、前端、后端、质量和技术负责人。', "
            "?, 'official.workflow.software_rnd_sop', '[\"model\",\"tool\",\"connector\"]', "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            ("dt_engineering", json.dumps(employee_ids, ensure_ascii=False)),
        )

    def _seed_rd_department(self, connection: sqlite3.Connection) -> None:
        """新增 dt_rd_department：研发部部门模板。"""
        employee_ids = [
            "et_tech_lead", "et_backend_engineer", "et_qa_engineer", "et_devops_engineer",
        ]
        connection.execute(
            "insert or ignore into department_templates "
            "(id, slug, name, department_type, description, default_employee_templates_json, "
            "default_workflow_template_id, default_capability_types_json, version, status, source, tenant_id, enabled) "
            "values (?, 'rd-department', 'R&D 研发部门', 'software_rnd', "
            "'研发部：技术负责人 + 后端工程师 + QA + DevOps。', "
            "?, 'wt_rd_pipeline', '[\"model\",\"tool\"]', "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            ("dt_rd_department", json.dumps(employee_ids, ensure_ascii=False)),
        )

    def _seed_company_templates_phase1(self, connection: sqlite3.Connection) -> None:
        """Phase-1 CompanyTemplate（ct_ai_software_company）类型容器种子。"""
        connection.execute(
            "insert or ignore into company_templates "
            "(company_template_id, name, company_type, description, version, status, source, tenant_id, enabled) "
            "values (?, 'AI 软件公司', 'ai_rd', 'AI 研发型公司的出厂类型容器（变体 C 引用的 ct_*）。', "
            "'1.0.0', 'active', 'official', 'platform', 1)",
            ("ct_ai_software_company",),
        )

    def _seed_dashboard_templates(self, connection: sqlite3.Connection) -> None:
        """DashboardTemplate 内容实例（dtpl_*，9 个）。widget_ids 仅引用规范 widget_id。"""
        dashboards = [
            (
                "dtpl_ai_rd_ceo_dashboard", "AI 研发公司 CEO 驾驶舱", "ai_rd", ["ceo"],
                ["project_progress", "employee_status", "ai_cost", "project_risk"],
                "研发公司 CEO 全局驾驶舱",
            ),
            (
                "dtpl_ai_rd_engineering_dashboard", "AI 研发公司研发交付看板", "ai_rd", ["ceo", "cto", "tech_lead"],
                ["project_progress", "employee_load", "project_risk", "ai_cost"],
                "研发交付进度与负载看板",
            ),
            (
                "dtpl_ai_rd_quality_dashboard", "AI 研发公司质量看板", "ai_rd", ["cto", "qa"],
                ["project_risk", "employee_load", "ai_cost"],
                "研发质量与风险看板",
            ),
            (
                "dtpl_ai_content_ops_ceo_dashboard", "AI 内容公司 CEO 驾驶舱", "ai_content", ["ceo"],
                ["content_output", "publish_metrics", "viral_trend", "operation_cost"],
                "内容公司 CEO 全局驾驶舱",
            ),
            (
                "dtpl_ai_content_ops_operations_dashboard", "AI 内容公司运营看板", "ai_content", ["ceo", "ops"],
                ["content_output", "publish_metrics", "operation_cost", "employee_load"],
                "内容运营看板",
            ),
            (
                "dtpl_ai_content_ops_growth_dashboard", "AI 内容公司增长看板", "ai_content", ["ceo", "growth"],
                ["viral_trend", "publish_metrics", "content_output", "token_usage"],
                "内容增长看板",
            ),
            (
                "dtpl_ai_commercial_revenue_dashboard", "AI 商业公司营收看板", "ai_commercial", ["ceo", "cfo"],
                ["ai_cost", "token_usage", "model_usage", "operation_cost"],
                "商业营收看板",
            ),
            (
                "dtpl_ai_commercial_customer_success_dashboard", "AI 商业公司客户看板", "ai_commercial", ["ceo", "cs"],
                ["company_health", "department_overview", "employee_status", "ai_cost"],
                "商业客户成功看板",
            ),
            (
                "dtpl_ai_rd_ceo_cockpit", "AI 研发公司 CEO 驾驶舱（Cockpit）", "ai_rd", ["ceo"],
                ["company_health", "project_progress", "ai_cost"],
                "研发公司 CEO 精简驾驶舱",
            ),
        ]
        connection.executemany(
            "insert or ignore into dashboard_templates "
            "(dashboard_template_id, name, company_type, role_visibility_json, widget_ids_json, "
            "layout_summary, data_source_refs_json, commercial_slot_ref_json, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, '[]', NULL, '1.0.0', 'active', 'official', 'platform', 1)",
            [
                (
                    dtpl_id, name, company_type,
                    json.dumps(roles, ensure_ascii=False),
                    json.dumps(widget_ids, ensure_ascii=False),
                    layout_summary,
                )
                for (dtpl_id, name, company_type, roles, widget_ids, layout_summary) in dashboards
            ],
        )

    def _seed_workflow_contents(self, connection: sqlite3.Connection) -> None:
        """Workflow 内容实例（wl_*，36 条真实 id，来自 workflow-official-content-plan §§370-405）。

        每个 wl_* 通过 workflow_template_ref 指向对应 wt_* 类型容器（变体 B 折叠）。
        """
        workflows = [
            ("wl_ai_rd_software_dev_sop", "软件研发 SOP", "wt_software_dev_sop", "ai_rd", ["PM", "Architect", "TechLead", "Engineer", "QA"], "MetaGPT SOP"),
            ("wl_ai_rd_requirement_to_prd", "需求转 PRD", "wt_requirement_to_prd", "ai_rd", ["Product Manager"], "MetaGPT SOP"),
            ("wl_ai_rd_system_design_sop", "系统设计方案", "wt_system_design_sop", "ai_rd", ["Architect"], "MetaGPT SOP"),
            ("wl_ai_rd_api_dev_sop", "API 开发 SOP", "wt_api_dev_sop", "ai_rd", ["Backend Engineer"], "ChatDev workflow"),
            ("wl_ai_rd_feature_dev_sop", "特性开发 SOP", "wt_feature_dev_sop", "ai_rd", ["Frontend/Backend Engineer"], "ChatDev workflow"),
            ("wl_ai_rd_tdd_sop", "TDD SOP", "wt_tdd_sop", "ai_rd", ["Backend Engineer"], "ChatDev workflow"),
            ("wl_ai_rd_code_review_sop", "代码评审 SOP", "wt_code_review_sop", "ai_rd", ["Architect/Tech Lead"], "AutoGen pattern"),
            ("wl_ai_rd_bugfix_sop", "缺陷修复 SOP", "wt_bugfix_sop", "ai_rd", ["Backend Engineer"], "industry SOP"),
            ("wl_ai_rd_ci_cd_sop", "CI/CD SOP", "wt_ci_cd_sop", "ai_rd", ["DevOps/SRE"], "industry SOP"),
            ("wl_ai_rd_data_pipeline_sop", "数据管道 SOP", "wt_data_pipeline_sop", "ai_rd", ["Data Engineer"], "Curis internal"),
            ("wl_ai_rd_database_migration_sop", "数据库迁移 SOP", "wt_database_migration_sop", "ai_rd", ["Backend/Data Engineer"], "industry SOP"),
            ("wl_ai_rd_security_review_sop", "安全评审 SOP", "wt_security_review_sop", "ai_rd", ["Security Engineer"], "Curis internal"),
            ("wl_ai_rd_incident_response_sop", "事件响应 SOP", "wt_incident_response_sop", "ai_rd", ["DevOps/SRE"], "industry SOP"),
            ("wl_ai_rd_performance_tuning_sop", "性能调优 SOP", "wt_performance_tuning_sop", "ai_rd", ["Backend/DevOps"], "industry SOP"),
            ("wl_ai_rd_microservice_bootstrap_sop", "微服务启动 SOP", "wt_microservice_bootstrap_sop", "ai_rd", ["Architect"], "Curis internal"),
            ("wl_ai_rd_tech_spike_sop", "技术预研 SOP", "wt_tech_spike_sop", "ai_rd", ["Tech Lead/Engineer"], "industry SOP"),
            ("wl_ai_content_content_production_sop", "内容生产 SOP", "wt_content_production_sop", "ai_content", ["Content Operator"], "industry SOP"),
            ("wl_ai_content_topic_research_sop", "选题研究 SOP", "wt_topic_research_sop", "ai_content", ["Content Researcher"], "CrewAI example"),
            ("wl_ai_content_script_writing_sop", "脚本撰写 SOP", "wt_script_writing_sop", "ai_content", ["Script Writer"], "industry SOP"),
            ("wl_ai_content_video_production_sop", "视频制作 SOP", "wt_video_production_sop", "ai_content", ["Video Producer"], "CrewAI example"),
            ("wl_ai_content_seo_optimization_sop", "SEO 优化 SOP", "wt_seo_optimization_sop", "ai_content", ["SEO Specialist"], "industry SOP"),
            ("wl_ai_content_editorial_calendar_sop", "编辑日历 SOP", "wt_editorial_calendar_sop", "ai_content", ["Content Planner"], "CrewAI example"),
            ("wl_ai_content_multichannel_distribution_sop", "多渠道分发 SOP", "wt_multichannel_distribution_sop", "ai_content", ["Distribution Operator"], "industry SOP"),
            ("wl_ai_content_content_audit_sop", "内容审核 SOP", "wt_content_audit_sop", "ai_content", ["Content Auditor"], "industry SOP"),
            ("wl_ai_content_livestream_sop", "直播 SOP", "wt_livestream_sop", "ai_content", ["Live Host"], "Curis internal"),
            ("wl_ai_content_ugc_campaign_sop", "UGC 活动 SOP", "wt_ugc_campaign_sop", "ai_content", ["Community Manager"], "CrewAI example"),
            ("wl_ai_content_viral_analysis_sop", "传播分析 SOP", "wt_viral_analysis_sop", "ai_content", ["Data Analyst"], "industry SOP"),
            ("wl_ai_content_brand_voice_sop", "品牌语气 SOP", "wt_brand_voice_sop", "ai_content", ["Brand Manager"], "Curis internal"),
            ("wl_ai_commercial_gtm_sop", "GTM SOP", "wt_gtm_sop", "ai_commercial", ["GTM Manager"], "industry SOP"),
            ("wl_ai_commercial_market_research_sop", "市场研究 SOP", "wt_market_research_sop", "ai_commercial", ["Market Analyst"], "CrewAI example"),
            ("wl_ai_commercial_sales_outreach_sop", "销售触达 SOP", "wt_sales_outreach_sop", "ai_commercial", ["Sales Rep"], "CrewAI example"),
            ("wl_ai_commercial_pricing_strategy_sop", "定价策略 SOP", "wt_pricing_strategy_sop", "ai_commercial", ["Pricing Manager"], "industry SOP"),
            ("wl_ai_commercial_crm_pipeline_sop", "CRM 管道 SOP", "wt_crm_pipeline_sop", "ai_commercial", ["Sales Ops"], "industry SOP"),
            ("wl_ai_commercial_customer_success_sop", "客户成功 SOP", "wt_customer_success_sop", "ai_commercial", ["CS Manager"], "industry SOP"),
            ("wl_ai_commercial_fundraising_sop", "融资 SOP", "wt_fundraising_sop", "ai_commercial", ["Founder/BD"], "industry SOP"),
            ("wl_ai_commercial_growth_experiment_sop", "增长实验 SOP", "wt_growth_experiment_sop", "ai_commercial", ["Growth Manager"], "industry SOP"),
        ]
        connection.executemany(
            "insert or ignore into workflow_contents "
            "(workflow_content_id, name, workflow_template_ref, pack, owner_roles_json, "
            "step_templates_json, source_attribution, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, '[]', ?, '1.0.0', 'active', 'official', 'platform', 1)",
            [
                (
                    wl_id, name, wt_ref, pack,
                    json.dumps(roles, ensure_ascii=False),
                    attribution,
                )
                for (wl_id, name, wt_ref, pack, roles, attribution) in workflows
            ],
        )

    def _seed_company_packages(self, connection: sqlite3.Connection) -> None:
        """Company Package（ccp_ai_software_company）旗舰闭环种子（company-package-official-content-plan §7.1）。"""
        connection.execute(
            "insert or ignore into company_packages "
            "(company_package_id, name, description, version, status, source, pack, "
            "company_template_ref, department_template_refs_json, employee_template_refs_json, "
            "persona_refs_json, skill_refs_json, tool_refs_json, workflow_refs_json, "
            "sub_package_refs_json, pricing_reference, quota_reference, availability, tenant_id, enabled) "
            "values (?, 'AI 软件公司出厂包', "
            "'从 ct_ai_software_company 到 dt_engineering 到 6 个 et_* 再到 pt_/skl_/tl_/wl_* 七类串联的出厂配置（变体 C 聚合包）。', "
            "'1.0.0', 'active', 'Curis internal', "
            "'ai_rd', 'ct_ai_software_company', ?, ?, ?, ?, ?, ?, ?, NULL, NULL, 'public', 'platform', 1)",
            (
                "ccp_ai_software_company",
                json.dumps(["dt_engineering"], ensure_ascii=False),
                json.dumps(
                    ["et_backend_engineer", "et_frontend_engineer", "et_architect",
                     "et_tech_lead", "et_product_manager", "et_qa_engineer"],
                    ensure_ascii=False,
                ),
                json.dumps(
                    ["pt_direct_executor", "pt_analytical_advisor", "pt_supportive_coach", "pt_balanced_facilitator"],
                    ensure_ascii=False,
                ),
                json.dumps(
                    ["skl_ai_rd_python_development", "skl_ai_rd_system_design",
                     "skl_ai_rd_requirement_analysis", "skl_ai_rd_test_design",
                     "skl_ai_rd_api_design", "skl_ai_rd_code_review"],
                    ensure_ascii=False,
                ),
                json.dumps(
                    ["tl_ai_rd_code_executor", "tl_ai_rd_test_runner", "tl_ai_rd_code_linter",
                     "tl_ai_rd_git_client", "tl_ai_rd_python_repl", "tl_ai_rd_file_reader"],
                    ensure_ascii=False,
                ),
                json.dumps(
                    ["wl_ai_rd_software_dev_sop", "wl_ai_rd_requirement_to_prd",
                     "wl_ai_rd_system_design_sop", "wl_ai_rd_api_dev_sop",
                     "wl_ai_rd_code_review_sop", "wl_ai_rd_ci_cd_sop"],
                    ensure_ascii=False,
                ),
                json.dumps(["cp_content_ops"], ensure_ascii=False),
            ),
        )
        connection.execute(
            "update company_packages set sub_package_refs_json = ? "
            "where company_package_id = 'ccp_ai_software_company'",
            (json.dumps(["cp_content_ops"], ensure_ascii=False),),
        )

    # ── 受控试点 B：Agent 拆解转换引擎 V1（agency-agents 范式 1）──────────────────────
    # 主理人裁定：opt-in seed，绝不挂默认 initialize()；不破坏既有 6 官方 et_* /
    # 115 工具 / 52 技能（仅复用/增强备注）。全部 candidate/draft 态、可回滚。
    def seed_agent_conversion_pilot_b(self) -> None:
        """opt-in：叠加写入 Pilot B 候选/草稿资产（不挂默认 initialize()）。

        调用前确保完整 schema 与既有官方资产已就位（幂等）：先 ``initialize()``
        再写入叠加层。所有写操作 ``INSERT OR IGNORE``，依赖主键幂等；candidate/draft
        态，可经 ``rollback_agent_conversion_pilot_b()`` 整批回滚。

        设计约束红线：
        - 不接入凭证、不建 marketplace、不 instantiation（ADR-0017 仍锁）；
        - 与既有 6 官方员工 / 115 工具 / 52 技能零命名冲突（候选 id 前缀 pilot_b_）；
        - 5 个 business.* department_type 必须注册（否则 et_*.department_type 无合法值）。
        """
        # 幂等：确保表结构 + 既有官方资产（6 et_* / 115 工具 / 52 技能）已 seed。
        self.initialize()
        with self.connect() as connection:
            self._seed_agent_conversion_pilot_b(connection)

    def _seed_agent_conversion_pilot_b(self, connection: sqlite3.Connection) -> None:
        """Pilot B 实际写通道（additive、INSERT OR IGNORE、按主键幂等）。

        数据来自 ``app.agent_conversion.seed.build_pilot_b_rows()``（§7.1 权威映射）。
        写入顺序：department_types → personas → employees → skills → tools →
        workflows → departments。
        """
        from app.agent_conversion.seed import build_pilot_b_rows

        rows = build_pilot_b_rows()

        # 1) 5 个 business.* department_types（idempotent，缺则补）
        connection.executemany(
            "insert or ignore into department_types "
            "(type_key, category, display_name, description, "
            "manifest_json, manifest_schema_version, is_system) "
            "values (?, ?, ?, ?, ?, ?, ?)",
            rows["department_types"],
        )

        # 2) persona_templates（pt_*，draft）
        connection.executemany(
            "insert or ignore into persona_templates "
            "(persona_id, slug, name, archetype, traits_json, "
            "communication_style_json, reporting_style_json, decision_style, "
            "collaboration_style_json, version, status, source, tenant_id, enabled, image_ref_json) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["personas"],
        )

        # 3) employee_templates（et_*，draft，department_type=business.*）
        connection.executemany(
            "insert or ignore into employee_templates "
            "(id, slug, name, role, responsibility, department_type, "
            "default_instructions, default_capability_types_json, default_model_policy_json, "
            "default_workflow_step_types_json, guardrails_json, persona_ref, "
            "default_skill, default_tool, persona_overrides_json, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["employees"],
        )

        # 4) skill_templates（skl_*，candidate；命中既有 52 则 INSERT OR IGNORE 跳过）
        connection.executemany(
            "insert or ignore into skill_templates "
            "(skill_template_id, slug, name, description, skill_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version, category) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["skills"],
        )

        # 5) tool_templates（tl_*，candidate；命中既有 115 则 INSERT OR IGNORE 跳过）
        connection.executemany(
            "insert or ignore into tool_templates "
            "(tool_template_id, slug, name, description, tool_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["tools"],
        )

        # 6) workflow_templates（wt_*，draft，pack 由 wt 容器语义承载）
        connection.executemany(
            "insert or ignore into workflow_templates "
            "(id, name, description, source, tenant_id, department_type, "
            "process_type, steps_json, status) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["workflows"],
        )

        # 7) department_templates（dt_*，draft，反向归集 et_*）
        connection.executemany(
            "insert or ignore into department_templates "
            "(id, slug, name, department_type, description, "
            "default_employee_templates_json, default_workflow_template_id, "
            "default_capability_types_json, source, tenant_id, enabled, version, status) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["departments"],
        )

    def rollback_agent_conversion_pilot_b(self) -> None:
        """整批回滚 Pilot B 候选/草稿资产（按 id 前缀范围 DELETE）。

        仅清除本次 pilot B 写入的行：含 12 个 business.* 的 official.employee.* 员工；
        保留基线 6 个 official.employee.*（department_type='software_rnd'，非 Pilot B 资产）/
        6 个 et_% 官方员工 / 115 工具 / 55 技能 / 6 官方 persona / business.general。
        可重复调用（幂等）。
        """
        with self.connect() as connection:
            # 仅清 Pilot B 的 12 个 business.* 员工；保留基线 6 个 official.employee.*
            # （software_rnd）—— 它们由 initialize() 创建，非 Pilot B 资产。
            connection.execute(
                "delete from employee_templates where id like 'official.employee.%' "
                "and department_type like 'business.%'"
            )
            connection.execute(
                "delete from persona_templates where persona_id like 'pt_%' "
                "and persona_id not in ("
                "'pt_supportive_coach','pt_direct_executor','pt_analytical_advisor',"
                "'pt_creative_explorer','pt_balanced_facilitator','pt_risk_aware_guardian')"
            )
            connection.execute(
                "delete from skill_templates where skill_template_id like 'skl_pilot_b_%'"
            )
            connection.execute(
                "delete from tool_templates where tool_template_id like 'tl_pilot_b_%'"
            )
            connection.execute(
                "delete from workflow_templates where id like 'wt_pilot_b_%'"
            )
            connection.execute(
                "delete from department_templates where id like 'dt_pilot_b_%'"
            )
            connection.execute(
                "delete from department_types where type_key in ("
                "'business.product','business.marketing','business.sales',"
                "'business.support','business.finance')"
            )

    # ── 受控试点 B：聚焦激活 4 个 ★5 高价值候选（元数据态，仅改 status，可逆）──
    # 激活仅改 employee_templates / persona_templates 的 status（draft→active），
    # 不 instantiation（ADR-0017 仍锁）、不接凭证、不建 marketplace。其余 8 个 et
    # 与全部 skl/tl/wt/dt 维持 draft/candidate，本组函数不触碰。
    _PILOT_B_HIGHVALUE_ET_IDS: tuple[str, ...] = (
        "official.employee.marketing_growth_hacker",
        "official.employee.marketing_content_creator",
        "official.employee.support_responder",
        "official.employee.finance_analyst",
    )
    _PILOT_B_HIGHVALUE_PT_IDS: tuple[str, ...] = (
        "pt_marketing_growth_hacker",
        "pt_marketing_content_creator",
        "pt_support_responder",
        "pt_finance_analyst",
    )

    def activate_pilot_b_highvalue(self) -> None:
        """opt-in：聚焦激活 4 个 ★5 高价值 Pilot B 候选（status → 'active'）。

        前置：Pilot B 候选资产须已以 draft 态落库（即已调用
        ``seed_agent_conversion_pilot_b()``，这是当前已提交状态）。本函数仅幂等
        保基线（``initialize()``）后，将 4 个 et_* 与对应 4 个 pt_* 的 status 由
        'draft' 改为 'active'。

        红线（绝对不可越）：
        - 仅激活这 4 个 et + 4 个 pt；其余 8 个 et 及所有 skl/tl/wt/dt 维持 draft；
        - 仅改模板 status 元数据，不 instantiation（ADR-0017 仍锁）、不接凭证、不建 marketplace；
        - 可逆：``deactivate_pilot_b_highvalue()`` 将 status 改回 'draft'。

        注意：本函数**仅**改已存在的行；若 Pilot B 候选尚未 seed，则 UPDATE 影响 0 行
        （不会新建资产）。不挂默认 ``initialize()`` 链——需激活时由调用方显式触发。
        """
        # 幂等保基线（schema + 既有 6 官方 et_* / 115 工具 / 55 技能）。
        self.initialize()
        with self.connect() as connection:
            self._activate_pilot_b_highvalue(connection)

    def _activate_pilot_b_highvalue(self, connection: sqlite3.Connection) -> None:
        """实际激活写通道：UPDATE 4 个 et_* + 4 个 pt_* 的 status 为 'active'。"""
        et_ids = self._PILOT_B_HIGHVALUE_ET_IDS
        pt_ids = self._PILOT_B_HIGHVALUE_PT_IDS
        placeholders = ",".join("?" * len(et_ids))
        connection.execute(
            f"update employee_templates set status = 'active' "
            f"where id in ({placeholders})",
            et_ids,
        )
        connection.execute(
            f"update persona_templates set status = 'active' "
            f"where persona_id in ({placeholders})",
            pt_ids,
        )

    def deactivate_pilot_b_highvalue(self) -> None:
        """opt-in 回滚：将 4 个 ★5 高价值候选 status 由 'active' 改回 'draft'。

        与 ``activate_pilot_b_highvalue()`` 对称、可逆；不改变其他任何行。其余 8
        个 et 及全部 skl/tl/wt/dt 始终维持 draft，本函数不触碰。可重复调用（幂等）。
        """
        self.initialize()
        with self.connect() as connection:
            self._deactivate_pilot_b_highvalue(connection)

    def _deactivate_pilot_b_highvalue(self, connection: sqlite3.Connection) -> None:
        """实际回滚写通道：UPDATE 4 个 et_* + 4 个 pt_* 的 status 为 'draft'。"""
        et_ids = self._PILOT_B_HIGHVALUE_ET_IDS
        pt_ids = self._PILOT_B_HIGHVALUE_PT_IDS
        placeholders = ",".join("?" * len(et_ids))
        connection.execute(
            f"update employee_templates set status = 'draft' "
            f"where id in ({placeholders})",
            et_ids,
        )
        connection.execute(
            f"update persona_templates set status = 'draft' "
            f"where persona_id in ({placeholders})",
            pt_ids,
        )

    # ── 多源扩展（CrewAI + MCP）：opt-in seed / rollback（设计 §T8，additive）──
    # 不挂默认 initialize() 链外的其他逻辑；各自先 initialize() 保基线再叠加。
    # 不新增 department_types（CrewAI 复用 business.general；MCP 仅写工具）。
    def seed_crewai(self) -> None:
        """opt-in：叠加写入 CrewAI 候选/草稿资产（不挂默认 initialize()）。

        写入 personas(pt_crew_*) / employees(official.employee.crew_*) /
        workflows(wt_crew_*) / tools(tl_crew_*)。复用 business.general，不新建
        department_types。所有写操作 INSERT OR IGNORE，依赖主键幂等；draft 态，
        可经 ``rollback_crewai()`` 整批回滚。与基线 6 官方员工 / 115 工具 / 55 技能
        零命名冲突（前缀 crew_）。
        """
        self.initialize()
        with self.connect() as connection:
            self._seed_crewai(connection)

    def _seed_crewai(self, connection: sqlite3.Connection, rows: dict | None = None) -> None:
        """CrewAI 实际写通道（additive、INSERT OR IGNORE、按主键幂等）。

        数据来自 ``app.agent_conversion.seed_multisource.build_multisource_rows()``
        的 crew_* 部分。写入顺序：personas → employees → workflows → tools。
        """
        from app.agent_conversion.seed_multisource import build_multisource_rows

        if rows is None:
            rows = build_multisource_rows()

        # 1) persona_templates（pt_crew_*，draft）
        connection.executemany(
            "insert or ignore into persona_templates "
            "(persona_id, slug, name, archetype, traits_json, "
            "communication_style_json, reporting_style_json, decision_style, "
            "collaboration_style_json, version, status, source, tenant_id, enabled, image_ref_json) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["crew_personas"],
        )
        # 2) employee_templates（official.employee.crew_*，draft，business.general）
        connection.executemany(
            "insert or ignore into employee_templates "
            "(id, slug, name, role, responsibility, department_type, "
            "default_instructions, default_capability_types_json, default_model_policy_json, "
            "default_workflow_step_types_json, guardrails_json, persona_ref, "
            "default_skill, default_tool, persona_overrides_json, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["crew_employees"],
        )
        # 3) workflow_templates（wt_crew_*，draft，business.general）
        connection.executemany(
            "insert or ignore into workflow_templates "
            "(id, name, description, source, tenant_id, department_type, "
            "process_type, steps_json, status) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["crew_workflows"],
        )
        # 4) tool_templates（tl_crew_*，draft）
        connection.executemany(
            "insert or ignore into tool_templates "
            "(tool_template_id, slug, name, description, tool_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows["crew_tools"],
        )

    def rollback_crewai(self) -> None:
        """整批回滚 CrewAI 候选/草稿资产（按 id 前缀范围 DELETE，幂等）。

        仅清除本次 CrewAI 写入的行：official.employee.crew_% / pt_crew_% /
        tl_crew_% / wt_crew_%。保留基线 6 个 official.employee.*（software_rnd）/
        6 个官方 persona / 115 工具 / 55 技能 / business.general / pilot_b 5 business.*。
        """
        with self.connect() as connection:
            connection.execute(
                "delete from employee_templates where id like 'official.employee.crew_%'"
            )
            connection.execute(
                "delete from persona_templates where persona_id like 'pt_crew_%'"
            )
            connection.execute(
                "delete from tool_templates where tool_template_id like 'tl_crew_%'"
            )
            connection.execute(
                "delete from workflow_templates where id like 'wt_crew_%'"
            )

    def seed_mcp(self) -> None:
        """opt-in：叠加写入 MCP Registry 工具候选（纯工具源，不挂默认 initialize()）。

        仅写 tool_templates（tl_mcp_*）。disposition=create → INSERT OR IGNORE；
        disposition=enhance_existing → UPDATE 既有工具富字段（description /
        instruction_excerpt / source_attribution，若列存在），不新建重复行；
        disposition=skip → 忽略。所有写操作依赖主键幂等；draft 态，可经
        ``rollback_mcp()`` 整批回滚。与基线 115 工具零命名冲突（前缀 mcp_）。
        """
        self.initialize()
        with self.connect() as connection:
            self._seed_mcp(connection)

    def _seed_mcp(self, connection: sqlite3.Connection, tool_rows: list | None = None) -> None:
        """MCP 实际写通道（additive；create/enhance_existing/skip 分支，幂等）。

        数据来自 ``app.agent_conversion.seed_multisource.build_multisource_rows()``
        的 mcp_tools 部分（或测试注入的等价行）。
        """
        from app.agent_conversion.seed_multisource import build_multisource_rows, SeedMapper

        if tool_rows is None:
            tool_rows = build_multisource_rows()["mcp_tools"]

        # 动态探测可更新列（tool_templates 无 source_attribution，故仅更新存在列）。
        cols = [r[1] for r in connection.execute("PRAGMA table_info(tool_templates)")]
        updatable = [c for c in ("description", "instruction_excerpt", "source_attribution") if c in cols]

        insert_sql = (
            "insert or ignore into tool_templates "
            "(tool_template_id, slug, name, description, tool_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )

        for row in tool_rows:
            tup = SeedMapper.map_tool(row)
            disp = str(row.get("disposition", "create") or "create")
            if disp == "skip":
                continue
            if disp == "enhance_existing":
                # 解析既有工具：先按 existing_id，再按 slug/name 兜底。
                target: str | None = None
                existing_id = str(row.get("existing_id", "") or "")
                if existing_id:
                    cur = connection.execute(
                        "select tool_template_id from tool_templates where tool_template_id = ?",
                        (existing_id,),
                    ).fetchone()
                    if cur:
                        target = cur[0]
                if not target:
                    cur = connection.execute(
                        "select tool_template_id from tool_templates where slug = ? or name = ?",
                        (str(row.get("slug", "")), str(row.get("name", ""))),
                    ).fetchone()
                    if cur:
                        target = cur[0]
                if target:
                    # 富字段 UPDATE（不新建重复行）。
                    desc = tup[3]
                    instr = tup[6]
                    attr = str(row.get("source_attribution", "") or "")
                    set_clause: list[str] = []
                    params: list[Any] = []
                    if "description" in updatable:
                        set_clause.append("description = ?")
                        params.append(desc)
                    if "instruction_excerpt" in updatable:
                        set_clause.append("instruction_excerpt = ?")
                        params.append(instr)
                    if "source_attribution" in updatable:
                        set_clause.append("source_attribution = ?")
                        params.append(attr)
                    if set_clause:
                        params.append(target)
                        connection.execute(
                            f"update tool_templates set {', '.join(set_clause)} "
                            f"where tool_template_id = ?",
                            params,
                        )
                    continue
                # 未命中既有 → 退回 create（健壮）。
            connection.execute(insert_sql, tup)

    def rollback_mcp(self) -> None:
        """整批回滚 MCP 工具候选（按 tl_mcp_ 前缀 DELETE，幂等）。

        仅清除本次 MCP 写入的 tl_mcp_* 工具行；保留基线 115 工具 / 6 员工 /
        55 技能 / pilot_b 资产 / business.general。
        """
        with self.connect() as connection:
            connection.execute(
                "delete from tool_templates where tool_template_id like 'tl_mcp_%'"
            )

    # ── 多源扩展：Skill 仓库（curispeng22-coder/skill）opt-in seed / rollback ──
    # 总控特批 harvest 该无 LICENSE 个人仓库为 draft 候选（不发布、不 instantiation）。
    # 写 skl_skill_*（净新增方法论技能）+ tl_skill_*（净新增工具）/ enhance_existing
    # （与 Pack F-J 基线工具重叠者 UPDATE 富字段，不新建重复行）。不写
    # et_*/pt_*/wt_*/dt_*。每函数各自先 initialize() 保基线再叠加；可经
    # rollback_skill_repo() 整批回滚（按 skl_skill_%/tl_skill_ 前缀 DELETE）。
    def seed_skill_repo(self) -> None:
        """opt-in：叠加写入 skill 仓库候选（不挂默认 initialize()）。

        写入 skill_templates（skl_skill_*，draft）+ tool_templates（tl_skill_* create /
        enhance_existing）。与基线 6 官方员工 / 115 工具 / 55 技能零命名冲突
        （前缀 skill_）；enhance_existing 走 UPDATE 不新建重复行。
        """
        self.initialize()
        with self.connect() as connection:
            self._seed_skill_repo(connection)

    def _seed_skill_repo(
        self,
        connection: sqlite3.Connection,
        skill_rows: list | None = None,
        tool_rows: list | None = None,
    ) -> None:
        """Skill 仓库实际写通道（additive；skills 全 create，tools 按 disposition 分支）。

        数据来自 ``app.agent_conversion.seed_multisource.build_multisource_rows()``
        的 skill_skills / skill_tools 部分（或测试注入的等价行）。
        """
        from app.agent_conversion.seed_multisource import build_multisource_rows, SeedMapper

        rows = build_multisource_rows()
        if skill_rows is None:
            skill_rows = rows["skill_skills"]
        if tool_rows is None:
            tool_rows = rows["skill_tools"]

        # 1) skill_templates（skl_skill_*，draft，全部 create / INSERT OR IGNORE）
        connection.executemany(
            "insert or ignore into skill_templates "
            "(skill_template_id, slug, name, description, skill_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version, category) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            skill_rows,
        )

        # 2) tool_templates（tl_skill_* create / enhance_existing / skip 分支）
        # 动态探测可更新列（tool_templates 无 source_attribution，故仅更新存在列）。
        cols = [r[1] for r in connection.execute("PRAGMA table_info(tool_templates)")]
        updatable = [c for c in ("description", "instruction_excerpt", "source_attribution") if c in cols]

        # 惰性建表：持久化 enhance_existing 命中的基线工具 seed 前原值，供跨进程
        # rollback 字节级还原（表随 DB 文件落盘，进程退出不丢；仅装 skill 仓库增强过的基线工具）。
        connection.execute(
            "create table if not exists multisource_baseline_backup ("
            "tool_template_id text primary key, description text, instruction_excerpt text)"
        )

        insert_sql = (
            "insert or ignore into tool_templates "
            "(tool_template_id, slug, name, description, tool_type, "
            "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )

        for row in tool_rows:
            tup = SeedMapper.map_tool(row)
            disp = str(row.get("disposition", "create") or "create")
            if disp == "skip":
                continue
            if disp == "enhance_existing":
                    # 解析既有工具：先按 existing_id，再按 slug/name 兜底（对齐基线 Pack F-J）。
                    target: str | None = None
                    existing_id = str(row.get("existing_id", "") or "")
                    if existing_id:
                        cur = connection.execute(
                            "select tool_template_id from tool_templates where tool_template_id = ?",
                            (existing_id,),
                        ).fetchone()
                        if cur:
                            target = cur[0]
                    if not target:
                        cur = connection.execute(
                            "select tool_template_id from tool_templates where slug = ? or name = ?",
                            (str(row.get("slug", "")), str(row.get("name", ""))),
                        ).fetchone()
                        if cur:
                            target = cur[0]
                    if target:
                        # 富字段 UPDATE（不新建重复行）。UPDATE 前先持久化 seed 前原值
                        # （INSERT OR IGNORE + NOT IN 守卫：重复 seed 不会把已增强版误存为原值）。
                        connection.execute(
                            "insert or ignore into multisource_baseline_backup "
                            "(tool_template_id, description, instruction_excerpt) "
                            "select tool_template_id, description, instruction_excerpt "
                            "from tool_templates where tool_template_id = ? "
                            "and tool_template_id not in ("
                            "select tool_template_id from multisource_baseline_backup)",
                            (target,),
                        )
                        desc = tup[3]
                    instr = tup[6]
                    attr = str(row.get("source_attribution", "") or "")
                    set_clause: list[str] = []
                    params: list[Any] = []
                    if "description" in updatable:
                        set_clause.append("description = ?")
                        params.append(desc)
                    if "instruction_excerpt" in updatable:
                        set_clause.append("instruction_excerpt = ?")
                        params.append(instr)
                    if "source_attribution" in updatable:
                        set_clause.append("source_attribution = ?")
                        params.append(attr)
                    if set_clause:
                        params.append(target)
                        connection.execute(
                            f"update tool_templates set {', '.join(set_clause)} "
                            f"where tool_template_id = ?",
                            params,
                        )
                    continue
                # 未命中既有 → 退回 create（健壮，避免丢失候选）。
            connection.execute(insert_sql, tup)

    def rollback_skill_repo(self) -> None:
        """整批回滚 skill 仓库候选（DELETE 新行 + 还原被富字段的基线工具，幂等）。

        1) 清除本次 skill 仓库写入的 skl_skill_* / tl_skill_* 行；
        2) 把被 enhance_existing 经 UPDATE 富字段的基线工具（description /
           instruction_excerpt）字节级还原为 seed 前原值，满足设计 §0『基线不变』
           铁律（不残留『增强』标记）。
        备份落盘于 ``multisource_baseline_backup`` 表（由 _seed_skill_repo 惰性建表
        并写入），故 seed 与 rollback 拆分到**不同进程/实例**（同文件）时仍能还原；
        还原后清空该表。
        保留基线 6 官方员工 / 115 工具（还原后三列 == seed 前）/ 55 技能 / 6 官方
        persona / business.general / pilot_b 5 business.*。
        """
        with self.connect() as connection:
            connection.execute(
                "delete from skill_templates where skill_template_id like 'skl_skill_%'"
            )
            connection.execute(
                "delete from tool_templates where tool_template_id like 'tl_skill_%'"
            )
            # 还原被 enhance_existing 改写的基线工具（description/instruction_excerpt），
            # 字节级恢复 seed 前原值，满足设计 §0『基线不变』铁律。备份随 DB 落盘，
            # 故跨进程 rollback 也能还原；还原后清空备份表（仅装 skill 增强过的基线工具）。
            connection.execute(
                "create table if not exists multisource_baseline_backup ("
                "tool_template_id text primary key, description text, instruction_excerpt text)"
            )
            connection.execute(
                "update tool_templates set description = b.description, "
                "instruction_excerpt = b.instruction_excerpt "
                "from multisource_baseline_backup b "
                "where tool_templates.tool_template_id = b.tool_template_id"
            )
            connection.execute("delete from multisource_baseline_backup")

    # ── Phase-1 只读投影 + 快照写入助手（供 catalog_authoring / catalog_fold / company_instantiation）──
    def list_persona_templates(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        """读取 PersonaTemplate 官方目录（tenant-scoped；platform 官方内容对所有租户可见）。"""
        return self._list_catalog_rows(
            "persona_templates", tenant_id,
            extra_cols=["persona_id", "slug", "name", "archetype", "traits_json",
                        "communication_style_json", "reporting_style_json",
                        "decision_style", "collaboration_style_json", "version", "status"],
        )

    def list_tool_templates(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        """读取 ToolTemplate 官方目录（tenant-scoped；含 R2 item7 能力态标记）。"""
        return self._list_catalog_rows(
            "tool_templates", tenant_id,
            extra_cols=["tool_template_id", "slug", "name", "tool_type", "source", "status",
                        "security_level", "applicable_departments_json",
                        "catalog_visible", "configured", "executable", "mock_or_stub",
                        "version"],
        )

    def list_workflow_templates(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        """读取 WorkflowTemplate 官方目录（tenant-scoped；含 R2 item8 能力态标记）。"""
        return self._list_catalog_rows(
            "workflow_templates", tenant_id,
            extra_cols=["id", "name", "description", "source", "department_type",
                        "process_type", "status", "workflow_capability_status"],
        )

    def get_persona_template(self, persona_id: str, tenant_id: str | None = None) -> dict[str, Any] | None:
        return self._get_catalog_row(
            "persona_templates", "persona_id", persona_id, tenant_id,
            extra_cols=["persona_id", "slug", "name", "archetype", "traits_json",
                        "communication_style_json", "reporting_style_json",
                        "decision_style", "collaboration_style_json", "version", "status"],
        )

    def list_dashboard_templates(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        return self._list_catalog_rows(
            "dashboard_templates", tenant_id,
            extra_cols=["dashboard_template_id", "name", "company_type", "role_visibility_json",
                        "widget_ids_json", "layout_summary", "data_source_refs_json",
                        "commercial_slot_ref_json", "version", "status"],
        )

    def get_dashboard_template(self, dashboard_template_id: str, tenant_id: str | None = None) -> dict[str, Any] | None:
        return self._get_catalog_row(
            "dashboard_templates", "dashboard_template_id", dashboard_template_id, tenant_id,
            extra_cols=["dashboard_template_id", "name", "company_type", "role_visibility_json",
                        "widget_ids_json", "layout_summary", "data_source_refs_json",
                        "commercial_slot_ref_json", "version", "status"],
        )

    def list_company_templates(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        return self._list_catalog_rows(
            "company_templates", tenant_id,
            extra_cols=["company_template_id", "name", "company_type", "description", "version", "status"],
        )

    def get_company_template(self, company_template_id: str, tenant_id: str | None = None) -> dict[str, Any] | None:
        return self._get_catalog_row(
            "company_templates", "company_template_id", company_template_id, tenant_id,
            extra_cols=["company_template_id", "name", "company_type", "description", "version", "status"],
        )

    def list_company_packages(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        return self._list_catalog_rows(
            "company_packages", tenant_id,
            extra_cols=["company_package_id", "name", "description", "version", "status", "pack",
                        "company_template_ref", "department_template_refs_json",
                        "employee_template_refs_json", "persona_refs_json", "skill_refs_json",
                        "tool_refs_json", "workflow_refs_json", "sub_package_refs_json",
                        "pricing_reference", "quota_reference", "availability"],
        )

    def get_company_package(self, company_package_id: str, tenant_id: str | None = None) -> dict[str, Any] | None:
        return self._get_catalog_row(
            "company_packages", "company_package_id", company_package_id, tenant_id,
            extra_cols=["company_package_id", "name", "description", "version", "status", "pack",
                        "company_template_ref", "department_template_refs_json",
                        "employee_template_refs_json", "persona_refs_json", "skill_refs_json",
                        "tool_refs_json", "workflow_refs_json", "sub_package_refs_json",
                        "pricing_reference", "quota_reference", "availability"],
        )

    def resolve_company_package_workflow_bridge(
        self,
        company_package_id: str,
        package_version: str,
        tenant_id: str,
    ) -> dict[str, Any]:
        """Resolve one exact, visible, executable package/workflow bridge.

        Resolution is ID-and-version only.  Missing, duplicate, cross-tenant,
        revoked, disabled, design-only, or version-drifted relations are
        rejected; there is intentionally no name/default/latest fallback.
        """
        with self.connect() as connection:
            package = connection.execute(
                """
                select * from company_packages
                where company_package_id = ? and version = ? and status = 'active'
                  and enabled = 1
                  and (
                    (tenant_id = 'platform' and source in ('official','Curis internal'))
                    or (tenant_id = ? and source in ('tenant_private','Curis internal'))
                  )
                """,
                (company_package_id, package_version, tenant_id),
            ).fetchone()
            if package is None:
                raise KeyError("company package version is not available")

            rows = connection.execute(
                """
                select * from company_package_workflow_bridges
                where company_package_id = ? and package_version = ?
                  and (
                    (tenant_id = 'platform' and source in ('official','Curis internal'))
                    or (tenant_id = ? and source in ('tenant_private','Curis internal'))
                  )
                """,
                (company_package_id, package_version, tenant_id),
            ).fetchall()
            active = [
                row
                for row in rows
                if row["status"] == "active" and row["revoked_at"] is None
            ]
            if len(active) != 1:
                raise ValueError("company package requires exactly one active workflow bridge")
            bridge = dict(active[0])

            try:
                workflow_refs = json.loads(package["workflow_refs_json"] or "[]")
            except (json.JSONDecodeError, TypeError) as error:
                raise ValueError("company package workflow references are invalid") from error
            if not isinstance(workflow_refs, list):
                raise ValueError("company package workflow references are invalid")
            if bridge["source_workflow_content_id"] not in workflow_refs:
                raise ValueError("workflow bridge source is not in the package version")
            source_content = self.get_workflow_content(
                bridge["source_workflow_content_id"], tenant_id
            )
            if (
                source_content is None
                or source_content.get("source") not in
                ("official", "tenant_private", "Curis internal")
                or source_content.get("version")
                != bridge["source_workflow_content_version"]
                or source_content.get("status") != "active"
                or not source_content.get("enabled")
            ):
                raise ValueError("workflow bridge source version is not available")

            workflow = self.get_official_workflow_template_version(
                bridge["workflow_template_id"],
                bridge["workflow_template_version"],
            )
            if workflow is None:
                raise ValueError("workflow bridge target version is not available")
            if (
                bridge["workflow_capability_status"] != "structured_executable"
                or workflow["workflow_capability_status"] != "structured_executable"
            ):
                raise ValueError("workflow bridge target is not structured executable")

        return bridge

    def list_company_package_workflow_bridges(
        self,
        company_package_id: str,
        package_version: str,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        """Return the sole validated bridge as a read-only catalog projection."""
        return [
            self.resolve_company_package_workflow_bridge(
                company_package_id, package_version, tenant_id
            )
        ]

    def list_workflow_contents(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        return self._list_catalog_rows(
            "workflow_contents", tenant_id,
            extra_cols=["workflow_content_id", "name", "workflow_template_ref", "pack",
                        "owner_roles_json", "step_templates_json", "source_attribution", "version", "status"],
        )

    def get_workflow_content(self, workflow_content_id: str, tenant_id: str | None = None) -> dict[str, Any] | None:
        return self._get_catalog_row(
            "workflow_contents", "workflow_content_id", workflow_content_id, tenant_id,
            extra_cols=["workflow_content_id", "name", "workflow_template_ref", "pack",
                        "owner_roles_json", "step_templates_json", "source_attribution", "version", "status"],
        )

    def get_official_workflow_template_version(
        self, workflow_template_id: str, version: str
    ) -> dict[str, Any] | None:
        """Return one active official Workflow by exact ID and version."""
        with self.connect() as connection:
            row = connection.execute(
                """
                select * from workflow_templates
                where id = ? and version = ? and status = 'active' and enabled = 1
                  and source = 'official'
                """,
                (workflow_template_id, version),
            ).fetchone()
        return None if row is None else dict(row)

    def get_employee_template_row(
        self, employee_id: str, tenant_id: str | None = None
    ) -> dict[str, Any] | None:
        """读取单条 EmployeeTemplate 行（含 persona_ref/default_skill/default_tool 加列）。"""
        with self.connect() as connection:
            row = connection.execute(
                "select id, slug, name, role, responsibility, description, department_type, "
                "default_instructions, default_capability_types_json, default_model_policy_json, "
                "default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled, "
                "persona_ref, default_skill, default_tool, version, status "
                "from employee_templates where id = ?",
                (employee_id,),
            ).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["default_capability_types"] = json.loads(item.pop("default_capability_types_json") or "[]")
        item["default_model_policy"] = json.loads(item.pop("default_model_policy_json") or "{}")
        item["default_workflow_step_types"] = json.loads(item.pop("default_workflow_step_types_json") or "[]")
        item["guardrails"] = json.loads(item.pop("guardrails_json") or "[]")
        item["enabled"] = bool(item["enabled"])
        return item

    def get_department_template_row(
        self, department_id: str, tenant_id: str | None = None
    ) -> dict[str, Any] | None:
        """读取单条 DepartmentTemplate 行。"""
        with self.connect() as connection:
            row = connection.execute(
                "select id, slug, name, department_type, description, "
                "default_employee_templates_json, default_workflow_template_id, "
                "default_capability_types_json, version, status, source, tenant_id, enabled "
                "from department_templates where id = ?",
                (department_id,),
            ).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["default_employee_templates"] = json.loads(item.pop("default_employee_templates_json") or "[]")
        item["default_capability_types"] = json.loads(item.pop("default_capability_types_json") or "[]")
        item["enabled"] = bool(item["enabled"])
        return item

    def save_department_template(
        self,
        *,
        id: str,
        slug: str = "",
        name: str,
        department_type: str = "software_rnd",
        description: str = "",
        default_employee_templates: list[str] | None = None,
        default_workflow_template_id: str | None = None,
        default_capability_types_json: str = '["model","tool","connector"]',
        version: str = "1.0.0",
        status: str = "active",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）DepartmentTemplate（dt_*）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into department_templates "
                "(id, slug, name, department_type, description, default_employee_templates_json, "
                "default_workflow_template_id, default_capability_types_json, version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    id, slug, name, department_type, description,
                    json.dumps(default_employee_templates or [], ensure_ascii=False),
                    default_workflow_template_id,
                    default_capability_types_json, version, status, source, tenant_id,
                ),
            )

    def list_widget_catalog(self) -> list[dict[str, Any]]:
        """读取 Widget Catalog 单一真相源（全平台官方，无租户隔离）。"""
        with self.connect() as connection:
            rows = connection.execute(
                "select widget_id, domain, data_class, title, description, source, tenant_id, enabled "
                "from dashboard_widget_catalog order by domain, widget_id"
            ).fetchall()
        return [self._widget_catalog_from_row(row) for row in rows]

    def get_widget(self, widget_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "select widget_id, domain, data_class, title, description, source, tenant_id, enabled "
                "from dashboard_widget_catalog where widget_id = ?",
                (widget_id,),
            ).fetchone()
        return None if row is None else self._widget_catalog_from_row(row)

    @staticmethod
    def _widget_catalog_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["enabled"] = bool(item["enabled"])
        return item

    def list_template_version_snapshots(self, instance_id: str | None = None) -> list[dict[str, Any]]:
        """读取快照隔离桶（Gate F 实例化产物）。可按 instance_id 过滤。"""
        with self.connect() as connection:
            if instance_id:
                rows = connection.execute(
                    "select * from template_version_snapshots where instance_id = ? order by snapshot_at",
                    (instance_id,),
                ).fetchall()
            else:
                rows = connection.execute(
                    "select * from template_version_snapshots order by snapshot_at"
                ).fetchall()
        return [self._snapshot_from_row(row) for row in rows]

    def create_template_version_snapshot(
        self,
        *,
        instance_id: str,
        template_type: str,
        template_id: str,
        snapshot_version: str,
        snapshot_metadata: dict[str, Any] | None = None,
        follow_latest: bool = False,
    ) -> dict[str, Any]:
        """写入一条模板版本快照（follow_latest 默认 0，快照隔离）。"""
        snapshot_id = f"tvs-{uuid.uuid4()}"
        with self.connect() as connection:
            connection.execute(
                """
                insert into template_version_snapshots (
                  id, instance_id, template_type, template_id, snapshot_version,
                  snapshot_metadata_json, snapshot_at, follow_latest
                ) values (?, ?, ?, ?, ?, ?, current_timestamp, ?)
                """,
                (
                    snapshot_id,
                    instance_id,
                    template_type,
                    template_id,
                    snapshot_version,
                    json.dumps(snapshot_metadata or {}, ensure_ascii=False),
                    1 if follow_latest else 0,
                ),
            )
        return self.get_template_version_snapshot(snapshot_id)

    def get_template_version_snapshot(self, snapshot_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "select * from template_version_snapshots where id = ?", (snapshot_id,)
            ).fetchone()
        return None if row is None else self._snapshot_from_row(row)

    @staticmethod
    def _snapshot_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["snapshot_metadata"] = json.loads(item.pop("snapshot_metadata_json") or "{}")
        item["follow_latest"] = bool(item["follow_latest"])
        return item

    @staticmethod
    def _catalog_row_from_json(row: Any) -> dict[str, Any]:
        """把含 *_json 列的目录行反序列化为 dict（通用）。"""
        item = dict(row)
        for key in list(item.keys()):
            if key.endswith("_json"):
                field = key[: -len("_json")]
                item[field] = json.loads(item.pop(key) or "[]" if field.endswith("s") else "{}")
        if "enabled" in item:
            item["enabled"] = bool(item["enabled"])
        item["source"] = item.get("source") or "official"
        return item

    def _list_catalog_rows(
        self, table: str, tenant_id: str | None, extra_cols: list[str]
    ) -> list[dict[str, Any]]:
        cols = ", ".join(["tenant_id", "enabled", *extra_cols])
        params: list[Any] = []
        query = f"select {cols} from {table} where 1=1"
        if tenant_id is not None:
            query += " and (source in ('official','marketplace') or " \
                     "(source in ('tenant_private','Curis internal') and tenant_id = ?) or " \
                     "(source = 'Curis internal' and tenant_id = 'platform'))"
            params.append(tenant_id)
        order_col = extra_cols[0] if extra_cols else "source"
        query += f" order by source, {order_col}"
        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._catalog_row_from_json(row) for row in rows]

    def _get_catalog_row(
        self, table: str, pk_col: str, pk_value: str, tenant_id: str | None, extra_cols: list[str]
    ) -> dict[str, Any] | None:
        cols = ", ".join(["tenant_id", "enabled", *extra_cols])
        query = f"select {cols} from {table} where {pk_col} = ?"
        params: list[Any] = [pk_value]
        if tenant_id is not None:
            query += " and (source in ('official','marketplace') or " \
                     "(source in ('tenant_private','Curis internal') and tenant_id = ?) or " \
                     "(source = 'Curis internal' and tenant_id = 'platform'))"
            params.append(tenant_id)
        with self.connect() as connection:
            row = connection.execute(query, params).fetchone()
        return None if row is None else self._catalog_row_from_json(row)

    # ── Phase-1 Gate C/D 官方资产目录写助手（Admin 供给侧，单一数据交换面）──
    def save_widget_catalog_entry(
        self,
        *,
        widget_id: str,
        domain: str,
        data_class: str = "",
        title: str = "",
        description: str = "",
        source: str = "official",
        tenant_id: str = "platform",
        enabled: bool = True,
    ) -> None:
        """幂等写入（insert or replace）一个规范 widget 到 Widget Catalog 单一真相源。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into dashboard_widget_catalog "
                "(widget_id, domain, data_class, title, description, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?)",
            (widget_id, domain, data_class, title, description, source, tenant_id, 1 if enabled else 0),
        )

    def save_persona_template(
        self,
        *,
        persona_id: str,
        slug: str = "",
        name: str,
        archetype: str,
        traits: list[Any] | None = None,
        communication_style: dict[str, Any] | None = None,
        reporting_style: dict[str, Any] | None = None,
        decision_style: str = "consultative",
        collaboration_style: dict[str, Any] | None = None,
        description: str = "",
        version: str = "1.0.0",
        status: str = "draft",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）PersonaTemplate（pt_*）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into persona_templates "
                "(persona_id, slug, name, archetype, traits_json, communication_style_json, "
                "reporting_style_json, decision_style, collaboration_style_json, version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    persona_id, slug, name, archetype,
                    json.dumps(traits or [], ensure_ascii=False),
                    json.dumps(communication_style or {}, ensure_ascii=False),
                    json.dumps(reporting_style or {}, ensure_ascii=False),
                    decision_style,
                    json.dumps(collaboration_style or {}, ensure_ascii=False),
                    version, status, source, tenant_id,
                ),
            )

    def save_dashboard_template(
        self,
        *,
        dashboard_template_id: str,
        name: str,
        company_type: str = "ai_rd",
        role_visibility: list[str] | None = None,
        widget_ids: list[str] | None = None,
        layout_summary: str = "",
        data_source_refs: list[str] | None = None,
        commercial_slot_ref: str | None = None,
        version: str = "1.0.0",
        status: str = "draft",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）DashboardTemplate（dtpl_*）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into dashboard_templates "
                "(dashboard_template_id, name, company_type, role_visibility_json, widget_ids_json, "
                "layout_summary, data_source_refs_json, commercial_slot_ref_json, version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    dashboard_template_id, name, company_type,
                    json.dumps(role_visibility or ["ceo"], ensure_ascii=False),
                    json.dumps(widget_ids or [], ensure_ascii=False),
                    layout_summary,
                    json.dumps(data_source_refs or [], ensure_ascii=False),
                    commercial_slot_ref,
                    version, status, source, tenant_id,
                ),
            )

    def save_company_package(
        self,
        *,
        company_package_id: str,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        status: str = "draft",
        source: str = "Curis internal",
        pack: str = "ai_rd",
        company_template_ref: str | None = None,
        department_template_refs: list[str] | None = None,
        employee_template_refs: list[str] | None = None,
        persona_refs: list[str] | None = None,
        skill_refs: list[str] | None = None,
        tool_refs: list[str] | None = None,
        workflow_refs: list[str] | None = None,
        sub_package_refs: list[str] | None = None,
        pricing_reference: str | None = None,
        quota_reference: str | None = None,
        availability: str = "public",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）CompanyPackage（ccp_* 聚合包，出目录）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into company_packages "
                "(company_package_id, name, description, version, status, source, pack, "
                "company_template_ref, department_template_refs_json, employee_template_refs_json, "
                "persona_refs_json, skill_refs_json, tool_refs_json, workflow_refs_json, "
                "sub_package_refs_json, pricing_reference, quota_reference, availability, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    company_package_id, name, description, version, status, source, pack,
                    company_template_ref,
                    json.dumps(department_template_refs or [], ensure_ascii=False),
                    json.dumps(employee_template_refs or [], ensure_ascii=False),
                    json.dumps(persona_refs or [], ensure_ascii=False),
                    json.dumps(skill_refs or [], ensure_ascii=False),
                    json.dumps(tool_refs or [], ensure_ascii=False),
                    json.dumps(workflow_refs or [], ensure_ascii=False),
                    json.dumps(sub_package_refs or [], ensure_ascii=False),
                    pricing_reference, quota_reference, availability, tenant_id,
                ),
            )

    def save_workflow_content(
        self,
        *,
        workflow_content_id: str,
        name: str,
        workflow_template_ref: str = "",
        pack: str = "ai_rd",
        owner_roles: list[str] | None = None,
        step_templates: list[str] | None = None,
        source_attribution: str = "Curis internal",
        version: str = "1.0.0",
        status: str = "active",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）WorkflowContent（wl_* 折叠进 catalog）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into workflow_contents "
                "(workflow_content_id, name, workflow_template_ref, pack, owner_roles_json, "
                "step_templates_json, source_attribution, version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    workflow_content_id, name, workflow_template_ref, pack,
                    json.dumps(owner_roles or [], ensure_ascii=False),
                    json.dumps(step_templates or [], ensure_ascii=False),
                    source_attribution, version, status, source, tenant_id,
                ),
            )

    def save_company_template(
        self,
        *,
        company_template_id: str,
        name: str,
        company_type: str = "ai_rd",
        description: str = "",
        version: str = "1.0.0",
        status: str = "draft",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """幂等写入（insert or replace）CompanyTemplate（ct_* 类型容器）。"""
        with self.connect() as connection:
            connection.execute(
                "insert or replace into company_templates "
                "(company_template_id, name, company_type, description, version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (company_template_id, name, company_type, description, version, status, source, tenant_id),
            )

    def upsert_employee_template(
        self,
        *,
        id: str,
        slug: str = "",
        name: str,
        role: str,
        responsibility: str = "",
        description: str = "",
        department_type: str = "software_rnd",
        default_instructions: str = "",
        default_capability_types_json: str = '["model","tool"]',
        default_model_policy_json: str = "{}",
        default_workflow_step_types_json: str = "[]",
        guardrails_json: str = "[]",
        persona_ref: str = "",
        default_skill: str = "",
        default_tool: str = "",
        version: str = "1.0.0",
        status: str = "draft",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> None:
        """Upsert（更新或插入）EmployeeTemplate（et_* 官方 catalog 内容补全）。

        既有行保留 ``created_at`` 与未托管列（persona_ref/default_skill/default_tool
        等随本次 payload 更新）；新行写入 ``created_at``。
        """
        with self.connect() as connection:
            existing = connection.execute(
                "select created_at from employee_templates where id = ?", (id,)
            ).fetchone()
            if existing is not None:
                connection.execute(
                    "update employee_templates set slug=?, name=?, role=?, responsibility=?, "
                    "description=?, department_type=?, default_instructions=?, "
                    "default_capability_types_json=?, default_model_policy_json=?, "
                    "default_workflow_step_types_json=?, guardrails_json=?, persona_ref=?, "
                    "default_skill=?, default_tool=?, version=?, status=?, source=?, "
                    "tenant_id=?, updated_at=current_timestamp where id=?",
                    (
                        slug, name, role, responsibility, description, department_type,
                        default_instructions, default_capability_types_json, default_model_policy_json,
                        default_workflow_step_types_json, guardrails_json, persona_ref,
                        default_skill, default_tool, version, status, source, tenant_id, id,
                    ),
                )
            else:
                connection.execute(
                    "insert into employee_templates "
                    "(id, slug, name, role, responsibility, description, department_type, "
                    "default_instructions, default_capability_types_json, default_model_policy_json, "
                    "default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled, "
                    "created_at, persona_ref, default_skill, default_tool, version, status, updated_at) "
                    "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, current_timestamp, "
                    "?, ?, ?, ?, ?, current_timestamp)",
                    (
                        id, slug, name, role, responsibility, description, department_type,
                        default_instructions, default_capability_types_json, default_model_policy_json,
                        default_workflow_step_types_json, guardrails_json, source, tenant_id,
                        persona_ref, default_skill, default_tool, version, status,
                    ),
                )

    def save_department_observation(
        self,
        observation_id: str,
        tenant_id: str,
        type_key: str,
        metrics_json: str,
        suggestion_json: str,
    ) -> None:
        """幂等无关的 additive 写：持久化一条部门自观测快照。

        供 D3.impl ``DepartmentObservability.suggest_self_improvement`` 调用。
        tenant-scoped（沿用 D1 ``tenant_id``）；不写 evolution_events（ADR-0016 D3
        追加写不变式）。``observation_id`` 由调用方用 uuid 生成，保证可重放幂等。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into department_observations "
                "(observation_id, tenant_id, type_key, metrics_json, suggestion_json) "
                "values (?, ?, ?, ?, ?)",
                (observation_id, tenant_id, type_key, metrics_json, suggestion_json),
            )

    def list_department_observations(
        self, tenant_id: str | None = None, type_key: str | None = None
    ) -> list[dict[str, Any]]:
        """读取部门自观测快照（tenant-scoped 实证 / 治理审计用）。

        默认读当前租户；可显式传 ``tenant_id`` / ``type_key`` 过滤。仅用于自反馈
        闭环的回读验证，不触外部 I/O。``WHERE tenant_id`` 为作用域过滤（允许），
        不引入 ``department_id`` 列。
        """
        resolved_tenant = (
            tenant_id if tenant_id is not None else TenantContext.current_tenant_id()
        )
        clauses = ["tenant_id = ?"]
        params: list[Any] = [resolved_tenant]
        if type_key is not None:
            clauses.append("type_key = ?")
            params.append(type_key)
        sql = (
            "select * from department_observations where "
            + " and ".join(clauses)
            + " order by created_at desc, observation_id desc"
        )
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    # ── ADR-0017 S3 D4.impl (issue 059): 治理提案持久化 ──
    def save_governance_proposal(
        self,
        proposal_id: str,
        tenant_id: str,
        ceo_id: str,
        type_key: str,
        action: str,
        proposed_enabled: bool,
        proposed_at: str,
        status: str = "proposed",
        approved_by: str | None = None,
        approved_at: str | None = None,
        applied_at: str | None = None,
    ) -> None:
        """幂等无关的 additive 写：持久化一条治理提案（proposed 态）。

        供 D4.impl ``CompanyGovernance.propose_department_toggle`` 调用。
        tenant/CEO-scoped；``proposal_id`` 由调用方用 uuid 生成。无 FK、无凭证列。
        治理事件写不在此处（经 EvolutionEventLog.record 单独留痕）。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into governance_proposals "
                "(proposal_id, tenant_id, ceo_id, type_key, action, "
                "proposed_enabled, proposed_at, approved_by, approved_at, "
                "applied_at, status) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    proposal_id,
                    tenant_id,
                    ceo_id,
                    type_key,
                    action,
                    1 if proposed_enabled else 0,
                    proposed_at,
                    approved_by,
                    approved_at,
                    applied_at,
                    status,
                ),
            )

    def get_governance_proposal(self, proposal_id: str) -> dict[str, Any] | None:
        """按主键取治理提案；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select proposal_id, tenant_id, ceo_id, type_key, action, "
                "proposed_enabled, proposed_at, approved_by, approved_at, "
                "applied_at, status "
                "from governance_proposals where proposal_id = ?",
                (proposal_id,),
            ).fetchone()
        if row is None:
            return None
        return dict(row)

    def update_governance_proposal_status(
        self,
        proposal_id: str,
        status: str,
        approved_by: str | None = None,
        approved_at: str | None = None,
        applied_at: str | None = None,
    ) -> None:
        """推进治理提案状态（proposed → approved → applied）。

        供 D4.impl ``approve_proposal`` / ``apply_proposal`` 调用。仅更新状态相关列；
        不触其他写路径（ADR-0016 D3 追加写不变式由治理事件单独留痕）。
        """
        with self.connect() as connection:
            connection.execute(
                "update governance_proposals set status = ?, "
                "approved_by = ?, approved_at = ?, applied_at = ? "
                "where proposal_id = ?",
                (status, approved_by, approved_at, applied_at, proposal_id),
            )

    # ── ADR-0017 S3 D4.impl (issue 059): 公司部门启用态持久化 ──
    def save_company_department_state(
        self,
        tenant_id: str,
        ceo_id: str,
        type_key: str,
        enabled: bool,
        approved_by: str | None = None,
        approved_at: str | None = None,
        applied_at: str | None = None,
    ) -> None:
        """幂等 upsert：持久化某 CEO 公司内某部门类型的启用态。

        供 D4.impl ``CompanyGovernance.apply_proposal`` 调用。tenant/CEO-scoped；
        (tenant_id, ceo_id, type_key) 为主键，重复 apply 以最新态覆盖。无 FK、
        无凭证列。默认不写 evolution_events（ADR-0016 D3 追加写不变式）。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into company_department_state "
                "(tenant_id, ceo_id, type_key, enabled, approved_by, "
                "approved_at, applied_at) "
                "values (?, ?, ?, ?, ?, ?, ?) "
                "on conflict(tenant_id, ceo_id, type_key) do update set "
                "enabled = excluded.enabled, "
                "approved_by = excluded.approved_by, "
                "approved_at = excluded.approved_at, "
                "applied_at = excluded.applied_at",
                (
                    tenant_id,
                    ceo_id,
                    type_key,
                    1 if enabled else 0,
                    approved_by,
                    approved_at,
                    applied_at,
                ),
            )

    def get_company_department_state(
        self, tenant_id: str, ceo_id: str, type_key: str
    ) -> dict[str, Any] | None:
        """读取某 CEO 公司内某部门类型的启用态；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select tenant_id, ceo_id, type_key, enabled, "
                "approved_by, approved_at, applied_at "
                "from company_department_state "
                "where tenant_id = ? and ceo_id = ? and type_key = ?",
                (tenant_id, ceo_id, type_key),
            ).fetchone()
        if row is None:
            return None
        return dict(row)

    def list_company_department_state(
        self, tenant_id: str | None = None, ceo_id: str | None = None
    ) -> list[dict[str, Any]]:
        """列出公司部门启用态（tenant/CEO-scoped 实证 / 治理视图投影用）。"""
        clauses: list[str] = []
        params: list[Any] = []
        if tenant_id is not None:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if ceo_id is not None:
            clauses.append("ceo_id = ?")
            params.append(ceo_id)
        sql = "select * from company_department_state"
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by ceo_id, type_key"
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    # ── ADR-0017 S4 D4.platform (issue 060): department_types 真实 CRUD（首个写入者）──
    def save_department_type(
        self,
        type_key: str,
        category: str,
        display_name: str,
        description: str,
        manifest_json: str,
        manifest_schema_version: str,
        is_system: bool = False,
    ) -> None:
        """新增部门类型（首个写入者）。type_key 为 PK；重复 → sqlite3.IntegrityError。

        供 D4.platform 部门类型新增（manage_department_types）调用。启用态落库于
        独立的 department_type_status additive 表（department_types 列固定为 7 列，
        不可改 DDL）。不消费 manifest_json 中的任何字段；无 FK、无凭证列。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into department_types "
                "(type_key, category, display_name, description, manifest_json, "
                "manifest_schema_version, is_system) "
                "values (?, ?, ?, ?, ?, ?, ?)",
                (
                    type_key,
                    category,
                    display_name,
                    description,
                    manifest_json,
                    manifest_schema_version,
                    1 if is_system else 0,
                ),
            )

    def update_department_type_fields(
        self,
        type_key: str,
        display_name: str | None = None,
        description: str | None = None,
        category: str | None = None,
    ) -> None:
        """编辑部门类型的可变更展示字段（display_name/description/category）。

        空字符串参数表示为「不修改」；仅对显式非空参数生成赋值。供
        manage_department_types 的 edit 动作调用。不触其他写路径、不写 evolution_events。
        """
        assignments: list[str] = []
        params: list[Any] = []
        if display_name is not None and display_name != "":
            assignments.append("display_name = ?")
            params.append(display_name)
        if description is not None and description != "":
            assignments.append("description = ?")
            params.append(description)
        if category is not None and category != "":
            assignments.append("category = ?")
            params.append(category)
        if not assignments:
            return
        params.append(type_key)
        with self.connect() as connection:
            connection.execute(
                f"update department_types set {', '.join(assignments)} "
                "where type_key = ?",
                params,
            )

    def set_department_type_enabled(self, type_key: str, enabled: bool) -> None:
        """停用/启用某部门类型（启用态落库于 department_type_status additive 表）。
        供 manage_department_types 的 'disable' / 'enable' 动作调用。不写
        evolution_events（受控写仅 type_created/type_removed/policy_set）。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into department_type_status (type_key, enabled, updated_at) "
                "values (?, ?, current_timestamp) "
                "on conflict(type_key) do update set enabled = excluded.enabled, "
                "updated_at = current_timestamp",
                (type_key, 1 if enabled else 0),
            )

    def remove_department_type(self, type_key: str) -> None:
        """移除部门类型（物理删除行）。供 manage_department_types 的 remove 动作调用；
        须经 human-approval 门控（approved_by 由调用方提供）。同步清理其启用态行；
        无 FK，不影响其他表。"""
        with self.connect() as connection:
            connection.execute(
                "delete from department_types where type_key = ?",
                (type_key,),
            )
            connection.execute(
                "delete from department_type_status where type_key = ?",
                (type_key,),
            )
        with self.connect() as connection:
            connection.execute(
                "delete from department_types where type_key = ?",
                (type_key,),
            )

    def get_department_type(self, type_key: str) -> dict[str, Any] | None:
        """按 PK 取部门类型（含 enabled 启用态，缺省 1）；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select dt.*, coalesce(dts.enabled, 1) as enabled "
                "from department_types dt "
                "left join department_type_status dts "
                "on dts.type_key = dt.type_key "
                "where dt.type_key = ?",
                (type_key,),
            ).fetchone()
        return dict(row) if row is not None else None

    def list_department_types(self) -> list[dict[str, Any]]:
        """列出全部部门类型（含 enabled 启用态，缺省 1）。供平台管理后台只读投影。"""
        with self.connect() as connection:
            rows = connection.execute(
                "select dt.*, coalesce(dts.enabled, 1) as enabled "
                "from department_types dt "
                "left join department_type_status dts "
                "on dts.type_key = dt.type_key "
                "order by dt.type_key"
            ).fetchall()
        return [dict(row) for row in rows]

    def list_official_models(self) -> list[dict[str, Any]]:
        """List active official model catalog rows for Workspace read-only catalog.

        Strictly returns only ``type = 'model'`` rows so that issue 070/071 tool /
        connector capabilities never leak into the model catalog (backward
        compatible: every pre-existing row is ``type = 'model'``).
        """
        with self.connect() as connection:
            rows = connection.execute(
                "select model_key, type, name, provider_id, display_name, "
                "supported_models, auth_type, source, gateway_ref, status, "
                "created_at, updated_at "
                "from official_models "
                "where source = 'official' and status = 'active' and type = 'model' "
                "and gateway_ref != 'freellmapi.experimental' "
                "order by model_key"
            ).fetchall()
        models = []
        for row in rows:
            item = dict(row)
            item["supported_models"] = json.loads(item["supported_models"])
            models.append(item)
        return models

    # ── 系统设置（system_settings）：键值持久化，供运行期开关使用 ──
    def get_setting(self, key: str, default: str | None = None) -> str | None:
        """读取单条系统设置；不存在时返回 ``default``。"""
        with self.connect() as connection:
            row = connection.execute(
                "select value from system_settings where key = ?", (key,)
            ).fetchone()
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> str:
        """写入/覆盖单条系统设置，返回写入后的值。"""
        with self.connect() as connection:
            connection.execute(
                "insert into system_settings (key, value, updated_at) "
                "values (?, ?, current_timestamp) "
                "on conflict(key) do update set "
                "value = excluded.value, updated_at = current_timestamp",
                (key, value),
            )
            connection.commit()
        return value

    def delete_setting(self, key: str) -> bool:
        """删除单条系统设置；返回是否确实删除了一行。"""
        with self.connect() as connection:
            cursor = connection.execute(
                "delete from system_settings where key = ?", (key,)
            )
            connection.commit()
        return cursor.rowcount > 0

    def list_settings(self, prefix: str = "") -> dict[str, str]:
        """按前缀列出系统设置（前缀为空时返回全部）。"""
        with self.connect() as connection:
            rows = connection.execute(
                "select key, value from system_settings "
                "where key like ? order by key",
                (f"{prefix}%",),
            ).fetchall()
        return {row["key"]: row["value"] for row in rows}

    # ── ADR-0028 Phase-2 (issue 065): New API 网关配置（GatewayConfig）仓储 ──
    def save_model_gateway(
        self,
        gateway_id: str,
        name: str,
        gateway_type: str,
        base_url: str,
        status: str = "active",
        credential_ref: str | None = None,
        default_model: str | None = None,
    ) -> None:
        """新增 / 覆盖写入一个网关配置。credential_ref 仅存不透明引用串，绝不存密钥值。

        供 ``GatewayCatalog.create`` 调用。无 FK、无凭证列。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into model_gateways "
                "(gateway_id, name, type, base_url, status, credential_ref, default_model) "
                "values (?, ?, ?, ?, ?, ?, ?)",
                (
                    gateway_id,
                    name,
                    gateway_type,
                    base_url,
                    status,
                    credential_ref,
                    default_model,
                ),
            )

    def get_model_gateway(self, gateway_id: str) -> dict[str, Any] | None:
        """按 PK 取网关配置；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select * from model_gateways where gateway_id = ?",
                (gateway_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def list_model_gateways(self) -> list[dict[str, Any]]:
        """列出全部网关配置（含启用态）。供平台管理后台只读投影。"""
        with self.connect() as connection:
            rows = connection.execute(
                "select * from model_gateways order by gateway_id"
            ).fetchall()
        return [dict(row) for row in rows]

    def set_model_gateway_status(self, gateway_id: str, status: str) -> None:
        """启停某网关（status ∈ active|inactive）。供 GatewayCatalog 状态机调用。"""
        with self.connect() as connection:
            connection.execute(
                "update model_gateways set status = ? where gateway_id = ?",
                (status, gateway_id),
            )

    def list_catalog_gateways(self) -> list[dict[str, Any]]:
        """Workspace 只读网关投影（catalog 供给）。

        **仅返回 gateway_id / name / type / base_url / status**；显式排除
        credential_ref 与 default_model，确保任何密钥引用串绝不外泄给 Workspace。
        """
        with self.connect() as connection:
            rows = connection.execute(
                "select gateway_id, name, type, base_url, status "
                "from model_gateways where gateway_id != 'freellmapi.experimental' "
                "order by gateway_id"
            ).fetchall()
        return [dict(row) for row in rows]

    # ── ADR-0028 Phase-2 (issue 065): 官方模型目录写路径（additive 扩展）──
    def save_official_model(
        self,
        model_key: str,
        provider_id: str,
        display_name: str,
        supported_models: list[str] | None,
        auth_type: str = "apikey",
        source: str = "official",
        gateway_ref: str = "newapi",
        status: str = "active",
        default_model: str | None = None,
        type: str = "model",
        name: str = "",
        runtime_meta_json: str | None = None,
        owner_type: str = "official",
        owner_id: str = "",
        visibility: str = "public",
    ) -> None:
        """新增官方能力目录条目（首个写入者）。model_key 为 PK；重复 → IntegrityError。

        供 ``ModelCatalog.create`` / ``CapabilityCatalog.create`` 调用。自 issue
        070/071 起统一承载 model / tool / connector / skill / mcp / api / cli /
        webhook / workflow：``type`` 区分能力类型（模型行 = 'model'），``name`` 为
        能力名（模型行缺省取 ``model_key``）。supported_models 以 JSON 落库（与读路径
        对齐）；source 默认 'official'；零凭证列。gateway_ref 为指向 GatewayConfig 的
        逻辑引用（写路径已校验存在性，无 DB FK 约束）。``runtime_meta_json`` 为能力
        运行态元数据（cost/permissions/io_schema/backup_chain/live_status/
        credentials_ref），由 CapabilityCatalog 序列化后传入（P0 后端核心）。
        """
        if gateway_ref == "freellmapi.experimental":
            raise ValueError("FreeLLMAPI 不允许登记为 Workspace 官方模型能力")
        resolved_name = name or model_key
        with self.connect() as connection:
            connection.execute(
                "insert into official_models "
                "(model_key, provider_id, display_name, supported_models, auth_type, "
                "source, gateway_ref, status, default_model, type, name, "
                "runtime_meta_json, owner_type, owner_id, visibility, updated_at) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)",
                (
                    model_key,
                    provider_id,
                    display_name,
                    json.dumps(supported_models or [], ensure_ascii=False),
                    auth_type,
                    source,
                    gateway_ref,
                    status,
                    default_model,
                    type,
                    resolved_name,
                    runtime_meta_json if runtime_meta_json is not None else "{}",
                    owner_type,
                    owner_id,
                    visibility,
                ),
            )

    @staticmethod
    def _parse_runtime_meta(raw: Any) -> dict[str, Any]:
        """把 official_models.runtime_meta_json 反序列化为 dict。

        缺失 / 非法 JSON 一律回退为空 dict（向后兼容既有无该列的库）。
        """
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def get_official_model(self, model_key: str) -> dict[str, Any] | None:
        """按 PK 取官方模型（含 default_model + runtime_meta）；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select * from official_models where model_key = ?",
                (model_key,),
            ).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["supported_models"] = json.loads(item["supported_models"])
        item["runtime_meta"] = self._parse_runtime_meta(item.get("runtime_meta_json"))
        return item

    def get_active_official_model(self, model_key: str) -> dict[str, Any] | None:
        """Return an active source=official catalog row for Workspace preference validation."""
        with self.connect() as connection:
            row = connection.execute(
                "select * from official_models "
                "where model_key = ? and source = 'official' and status = 'active' "
                "and gateway_ref != 'freellmapi.experimental'",
                (model_key,),
            ).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["supported_models"] = json.loads(item["supported_models"])
        item["runtime_meta"] = self._parse_runtime_meta(item.get("runtime_meta_json"))
        return item

    def list_all_official_models(
        self, include_inactive: bool = False
    ) -> list[dict[str, Any]]:
        """列出官方模型（additive 写路径全量视图）。

        默认仅 active；``include_inactive=True`` 时含 inactive（平台管理后台启用/
        停用开关需要看到全部）。supported_models 反序列化为列表；含 default_model。
        """
        clauses = ["1 = 1"]
        params: list[Any] = []
        if not include_inactive:
            clauses.append("status = 'active'")
        sql = (
            "select * from official_models where "
            + " and ".join(clauses)
            + " order by model_key"
        )
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        models = []
        for row in rows:
            item = dict(row)
            item["supported_models"] = json.loads(item["supported_models"])
            item["runtime_meta"] = self._parse_runtime_meta(item.get("runtime_meta_json"))
            models.append(item)
        return models

    def set_official_model_status(self, model_key: str, status: str) -> None:
        """启停某官方模型（status ∈ active|inactive）。供 ModelCatalog 状态机调用。"""
        with self.connect() as connection:
            connection.execute(
                "update official_models set status = ?, updated_at = current_timestamp "
                "where model_key = ?",
                (status, model_key),
            )

    # ── ADR-0028 Phase-2 (issue 070/071): 统一官方能力目录查询 ──
    def list_capabilities(
        self, type_filter: str | None = None, include_inactive: bool = False
    ) -> list[dict[str, Any]]:
        """Admin unified capability list (model / tool / connector in one table).

        ``type_filter`` narrows by capability type when given. ``include_inactive``
        defaults to False (active-only), matching the admin console's default view;
        pass True to surface disabled entries (needed for the enable/disable
        toggle). Returns full rows with ``capability_key`` aliased from
        ``model_key`` and ``supported_models`` deserialized.
        """
        clauses = ["1 = 1"]
        params: list[Any] = []
        if type_filter:
            clauses.append("type = ?")
            params.append(type_filter)
        if not include_inactive:
            clauses.append("status = 'active'")
        sql = (
            "select * from official_models where "
            + " and ".join(clauses)
            + " order by type, model_key"
        )
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        capabilities = []
        for row in rows:
            item = dict(row)
            item["capability_key"] = item["model_key"]
            item["supported_models"] = json.loads(item["supported_models"])
            item["runtime_meta"] = self._parse_runtime_meta(item.get("runtime_meta_json"))
            capabilities.append(item)
        return capabilities

    # ── 双轨能力供给（商业化预留）：按归属 / 可见性筛选 ──
    def list_capabilities_by_owner(
        self,
        owner_type: str | None = None,
        visibility: str | None = None,
        type_filter: str | None = None,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        """按 owner_type / visibility / type 筛选能力（官方目录浏览、租户私有筛选）。

        供 ``CapabilityCatalog.list_by_owner`` 调用；``select *`` 已含新增的
        owner_type / owner_id / visibility 列，调用方按需读取。
        """
        clauses = ["1 = 1"]
        params: list[Any] = []
        if owner_type:
            clauses.append("owner_type = ?")
            params.append(owner_type)
        if visibility:
            clauses.append("visibility = ?")
            params.append(visibility)
        if type_filter:
            clauses.append("type = ?")
            params.append(type_filter)
        if not include_inactive:
            clauses.append("status = 'active'")
        sql = (
            "select * from official_models where "
            + " and ".join(clauses)
            + " order by type, model_key"
        )
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        out = []
        for row in rows:
            item = dict(row)
            item["capability_key"] = item["model_key"]
            item["supported_models"] = json.loads(item["supported_models"])
            item["runtime_meta"] = self._parse_runtime_meta(item.get("runtime_meta_json"))
            out.append(item)
        return out

    # ── P0 后端核心：能力运行态元数据写回 + 经验沉淀 ──────────────────────────
    def update_capability_runtime_meta(
        self, model_key: str, runtime_meta: dict[str, Any]
    ) -> None:
        """把能力运行态元数据（含 live_status / 探活结果）写回 official_models。

        全量覆盖 runtime_meta_json 列（调用方负责合并旧值）。resolver 探活后调用，
        使后续解析可复用最新可用性，避免每次都真实探活。
        """
        payload = json.dumps(runtime_meta or {}, ensure_ascii=False)
        with self.connect() as connection:
            connection.execute(
                "update official_models set runtime_meta_json = ?, "
                "updated_at = current_timestamp where model_key = ?",
                (payload, model_key),
            )

    # ── P1（T09）：员工 → official_models 能力组合 ──────────────────────────
    def replace_employee_capabilities(
        self,
        tenant_id: str,
        employee_id: str,
        cap_keys: list[str],
        preferred: str | None = None,
    ) -> None:
        """幂等替换某员工的全部能力组合（按 sort_order 有序；preferred 标记首选）。"""
        with self.connect() as connection:
            connection.execute(
                "delete from employee_capabilities where tenant_id = ? and employee_id = ?",
                (tenant_id, employee_id),
            )
            for idx, key in enumerate(cap_keys):
                is_pref = 1 if (preferred and key == preferred) else 0
                connection.execute(
                    "insert into employee_capabilities "
                    "(tenant_id, employee_id, capability_key, is_preferred, sort_order, created_at) "
                    "values (?, ?, ?, ?, ?, current_timestamp)",
                    (tenant_id, employee_id, key, is_pref, idx),
                )

    def list_employee_capabilities(
        self, tenant_id: str, employee_id: str
    ) -> list[dict[str, Any]]:
        """返回某员工的全部能力 key（按 sort_order 升序）。"""
        with self.connect() as connection:
            rows = connection.execute(
                "select * from employee_capabilities "
                "where tenant_id = ? and employee_id = ? order by sort_order",
                (tenant_id, employee_id),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_employee_preferred_capability(
        self, tenant_id: str, employee_id: str
    ) -> dict[str, Any] | None:
        """返回某员工的首选能力行（is_preferred=1），无则返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select * from employee_capabilities "
                "where tenant_id = ? and employee_id = ? and is_preferred = 1 limit 1",
                (tenant_id, employee_id),
            ).fetchone()
        return dict(row) if row else None

    def save_capability_lesson(
        self,
        *,
        tenant_id: str,
        signature: str,
        cap_path: list[str] | None,
        outcome: str,
        reason: str,
        reused_count: int = 0,
    ) -> dict[str, Any]:
        """持久化一条经验（成功路径 / 失败原因 / 有效降级链）。

        ``signature`` 为任务类型指纹（如 sha256(task_type+cap_type)），``cap_path``
        为尝试过的能力 key 有序列表。幂等由上层 lesson_memory 控制（按 signature 合并
        reused_count）；此处为纯 INSERT。
        """
        with self.connect() as connection:
            cursor = connection.execute(
                "insert into capability_lessons "
                "(tenant_id, signature, cap_path_json, outcome, reason, reused_count) "
                "values (?, ?, ?, ?, ?, ?)",
                (
                    tenant_id,
                    signature,
                    json.dumps(cap_path or [], ensure_ascii=False),
                    outcome,
                    reason,
                    int(reused_count or 0),
                ),
            )
            row = connection.execute(
                "select * from capability_lessons where lesson_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._lesson_from_row(row)

    def update_capability_lesson_reuse(
        self, lesson_id: int, reused_count: int
    ) -> None:
        """更新某条经验的复用次数（reused_count 直接赋值，由上层累加）。"""
        with self.connect() as connection:
            connection.execute(
                "update capability_lessons set reused_count = ? where lesson_id = ?",
                (int(reused_count or 0), lesson_id),
            )

    def list_capability_lessons(
        self,
        signature: str | None = None,
        outcome: str | None = None,
        tenant_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """按 signature / outcome / tenant 过滤查询经验，按 reused_count DESC。"""
        clauses = ["1 = 1"]
        params: list[Any] = []
        if signature is not None:
            clauses.append("signature = ?")
            params.append(signature)
        if outcome is not None:
            clauses.append("outcome = ?")
            params.append(outcome)
        if tenant_id is not None:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        sql = (
            "select * from capability_lessons where "
            + " and ".join(clauses)
            + " order by reused_count desc, created_at desc"
        )
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._lesson_from_row(r) for r in rows]

    @staticmethod
    def _lesson_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        try:
            item["cap_path"] = json.loads(item["cap_path_json"])
        except (json.JSONDecodeError, TypeError, KeyError):
            item["cap_path"] = []
        return item

    def upsert_project_progress(
        self,
        project_id: str,
        tenant_id: str,
        *,
        status: str | None = None,
        progress_json: str | None = None,
        company_id: str = "local-demo-company",
        name: str | None = None,
        goal: str = "",
    ) -> None:
        """写回项目级聚合状态（progress_json）到 projects 表。

        复用既有 projects 表（不新建表）；若 project_id 不存在则插入最小项目行，
        满足 NOT NULL 约束。status 缺省不动（仅更新 progress_json）。
        """
        with self.connect() as connection:
            existing = connection.execute(
                "select project_id from projects where project_id = ?",
                (project_id,),
            ).fetchone()
            if existing is None:
                connection.execute(
                    "insert into projects "
                    "(project_id, tenant_id, company_id, name, goal, status, "
                    "progress_json, created_at, updated_at) "
                    "values (?, ?, ?, ?, ?, 'active', ?, current_timestamp, current_timestamp)",
                    (
                        project_id,
                        tenant_id,
                        company_id,
                        name or project_id,
                        goal,
                        progress_json if progress_json is not None else "{}",
                    ),
                )
            else:
                sets: list[str] = []
                params: list[Any] = []
                if progress_json is not None:
                    sets.append("progress_json = ?")
                    params.append(progress_json)
                if status is not None:
                    sets.append("status = ?")
                    params.append(status)
                if not sets:
                    return
                sets.append("updated_at = current_timestamp")
                params.append(project_id)
                connection.execute(
                    "update projects set " + ", ".join(sets) + " where project_id = ?",
                    params,
                )

    def list_catalog_capabilities(self) -> list[dict[str, Any]]:
        """Workspace read-only capability projection (catalog 供给).

        **Whitelist columns only** -- explicitly returns capability_key / type /
        name / provider_id / display_name / source / gateway_ref / auth_type /
        status / created_at / updated_at. The table carries NO secret columns by
        design, but the projection is contractually fixed to metadata only so it
        can never leak ``credential_ref`` / ``api_key`` / ``token`` /
        ``default_model`` (gateway_ref is only a logical reference key, never a
        secret). ``source = 'official'`` and ``status = 'active'`` are enforced.
        """
        with self.connect() as connection:
            rows = connection.execute(
                "select model_key as capability_key, type, name, provider_id, "
                "display_name, source, gateway_ref, auth_type, status, "
                "created_at, updated_at "
                "from official_models "
                "where source = 'official' and status = 'active' "
                "and gateway_ref != 'freellmapi.experimental' "
                "order by type, model_key"
            ).fetchall()
        capabilities = []
        for row in rows:
            item = dict(row)
            # effect_class（EvoFlow 复用 A1）：纯投影派生，不落库。
            # tool 按名称启发式，其余按类型默认；planning deny-by-default 见
            # docs/plan/evoflow-verified-reuse-plan.md A1。
            item["effect_class"] = effect_class_for_capability(
                item.get("type") or "", item.get("name") or ""
            )
            capabilities.append(item)
        return capabilities

    def save_tenant_private_capability(
        self,
        *,
        tenant_id: str,
        capability_type: str,
        capability_id: str,
        display_name: str = "",
        metadata: dict[str, Any] | None = None,
        status: str = "active",
    ) -> dict[str, Any]:
        if capability_type not in {"model", "agent", "tool", "connector"}:
            raise ValueError("capability_type must be model, agent, tool, or connector")
        if not capability_id:
            raise ValueError("capability_id is required")
        if self.get_official_model(capability_id) is not None:
            raise ValueError("tenant_private capability_id cannot reuse an official capability key")
        private_item = {
            "capability_type": capability_type,
            "metadata": metadata or {},
        }
        if self._is_freellmapi_private_model(private_item):
            raise ValueError("FreeLLMAPI 不允许登记为 Workspace 私有模型能力")
        with self.connect() as connection:
            connection.execute(
                """
                insert into tenant_private_capabilities (
                  tenant_id, capability_type, capability_id, display_name,
                  metadata_json, source, status, updated_at
                ) values (?, ?, ?, ?, ?, 'tenant_private', ?, current_timestamp)
                on conflict(tenant_id, capability_type, capability_id) do update set
                  display_name = excluded.display_name,
                  metadata_json = excluded.metadata_json,
                  source = 'tenant_private',
                  status = excluded.status,
                  updated_at = current_timestamp
                """,
                (
                    tenant_id,
                    capability_type,
                    capability_id,
                    display_name or capability_id,
                    json.dumps(metadata or {}, ensure_ascii=False),
                    status,
                ),
            )
        return self.get_tenant_private_capability(tenant_id, capability_type, capability_id)

    def get_tenant_private_capability(
        self, tenant_id: str, capability_type: str, capability_id: str
    ) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                select tenant_id, capability_type, capability_id, display_name,
                       metadata_json, source, status, created_at, updated_at
                from tenant_private_capabilities
                where tenant_id = ? and capability_type = ? and capability_id = ?
                """,
                (tenant_id, capability_type, capability_id),
            ).fetchone()
        if row is None:
            return None
        item = self._tenant_private_capability_from_row(row)
        return None if self._is_freellmapi_private_model(item) else item

    def list_tenant_private_capabilities(
        self,
        tenant_id: str,
        capability_type: str | None = None,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        clauses = ["tenant_id = ?", "source = 'tenant_private'"]
        params: list[Any] = [tenant_id]
        if not include_inactive:
            clauses.append("status = 'active'")
        if capability_type:
            clauses.append("capability_type = ?")
            params.append(capability_type)
        with self.connect() as connection:
            rows = connection.execute(
                "select tenant_id, capability_type, capability_id, display_name, "
                "metadata_json, source, status, created_at, updated_at "
                "from tenant_private_capabilities where "
                + " and ".join(clauses)
                + " order by capability_type, capability_id",
                params,
            ).fetchall()
        items = [self._tenant_private_capability_from_row(row) for row in rows]
        return [item for item in items if not self._is_freellmapi_private_model(item)]

    @staticmethod
    def _is_freellmapi_private_model(item: dict[str, Any]) -> bool:
        if item.get("capability_type") != "model":
            return False
        metadata = item.get("metadata") or {}
        base_url = str(metadata.get("base_url") or "").rstrip("/")
        return (
            metadata.get("provider_type") == "freellmapi.experimental"
            or metadata.get("credential_ref") == "env:FREELLMAPI_API_KEY"
            or base_url
            in {
                "http://127.0.0.1:3101",
                "http://localhost:3101",
                "http://freellmapi:3001",
            }
        )

    @staticmethod
    def _tenant_private_capability_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["metadata"] = json.loads(item.pop("metadata_json") or "{}")
        return item

    def _backfill_tool_security(self, connection: sqlite3.Connection) -> None:
        """P1-1：将 catalog 文档的安全等级/适用部门回填到 tool_templates。

        - additive + 幂等：重跑 initialize() 安全（同值覆盖）。
        - 仅对映射表内的官方 seed 行生效（by tool_template_id）；
          不在映射内的行（tenant_private / 未来扩展 / Pack B candidate）保持默认 'low'/'[]'。
        - applicable_departments_json 以 JSON 字符串落库（ensure_ascii=False 保留中文）。
        """
        mapping = _SECURITY_BACKFILL
        for tid, (level, depts) in mapping.items():
            connection.execute(
                "update tool_templates "
                "set security_level = ?, applicable_departments_json = ? "
                "where tool_template_id = ?",
                (level, json.dumps(depts, ensure_ascii=False), tid),
            )

    def save_credential_metadata(
        self,
        *,
        credential_id: str,
        tenant_id: str,
        name: str,
        provider: str,
        credential_type: str,
        credential_ref: str,
        status: str = "active",
        encrypted_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if status not in {"active", "disabled", "deleted"}:
            raise ValueError("credential status must be active, disabled, or deleted")
        with self.connect() as connection:
            connection.execute(
                """
                insert into credential_metadata (
                  credential_id, tenant_id, name, provider, credential_type,
                  credential_ref, status, encrypted_metadata, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
                on conflict(credential_id) do update set
                  name = excluded.name,
                  provider = excluded.provider,
                  credential_type = excluded.credential_type,
                  credential_ref = excluded.credential_ref,
                  status = excluded.status,
                  encrypted_metadata = excluded.encrypted_metadata,
                  updated_at = current_timestamp
                """,
                (
                    credential_id,
                    tenant_id,
                    name,
                    provider,
                    credential_type,
                    credential_ref,
                    status,
                    json.dumps(encrypted_metadata or {}, ensure_ascii=False),
                ),
            )
        row = self.get_credential_metadata(tenant_id, credential_id)
        if row is None:
            raise KeyError("credential metadata was not saved")
        return row

    def get_credential_metadata(
        self, tenant_id: str, credential_id: str
    ) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                select credential_id, tenant_id, name, provider, credential_type,
                       credential_ref, status, encrypted_metadata, created_at,
                       updated_at, disabled_at
                from credential_metadata
                where tenant_id = ? and credential_id = ?
                """,
                (tenant_id, credential_id),
            ).fetchone()
        return None if row is None else self._credential_metadata_from_row(row)

    def list_credential_metadata(self, tenant_id: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                select credential_id, tenant_id, name, provider, credential_type,
                       credential_ref, status, encrypted_metadata, created_at,
                       updated_at, disabled_at
                from credential_metadata
                where tenant_id = ? and status != 'deleted'
                order by created_at desc, credential_id
                """,
                (tenant_id,),
            ).fetchall()
        return [self._credential_metadata_from_row(row) for row in rows]

    # ── CEO 战略会议室（strategy-room）──
    def save_strategy_meeting(
        self,
        *,
        meeting_id: str,
        tenant_id: str,
        title: str,
        company_id: str = "",
        business_id: str = "",
        workspace_id: str = "",
        agenda: str = "",
        background: str = "",
        participants: list[str] | None = None,
        leader_employee_id: str = "",
        ceo_participation_mode: str = "DECISION_ONLY",
        conversation_id: str = "",
        context_refs: list[dict[str, str]] | None = None,
        decision_ref: str = "",
        work_refs: list[str] | None = None,
        result_refs: list[str] | None = None,
        continuation_gap: str = "",
        orchestration: dict[str, Any] | None = None,
        status: str = "scheduled",
        timeline: list[dict[str, Any]] | None = None,
        closed_at: str | None = None,
    ) -> dict[str, Any]:
        if status not in {"scheduled", "active", "closed"}:
            raise ValueError("meeting status must be scheduled, active, or closed")
        participants = participants or []
        timeline = timeline or []
        context_refs = context_refs or []
        work_refs = work_refs or []
        result_refs = result_refs or []
        orchestration = orchestration or {}
        with self.connect() as connection:
            connection.execute(
                """
                insert into strategy_meetings (
                  meeting_id, tenant_id, company_id, business_id, workspace_id,
                  title, agenda, background, participants, leader_employee_id,
                  ceo_participation_mode, conversation_id, context_refs, decision_ref,
                  work_refs, result_refs, continuation_gap, orchestration_json, status, timeline, closed_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
                on conflict(meeting_id) do update set
                  company_id = excluded.company_id,
                  business_id = excluded.business_id,
                  workspace_id = excluded.workspace_id,
                  title = excluded.title,
                  agenda = excluded.agenda,
                  background = excluded.background,
                  participants = excluded.participants,
                  leader_employee_id = excluded.leader_employee_id,
                  ceo_participation_mode = excluded.ceo_participation_mode,
                  conversation_id = excluded.conversation_id,
                  context_refs = excluded.context_refs,
                  decision_ref = excluded.decision_ref,
                  work_refs = excluded.work_refs,
                  result_refs = excluded.result_refs,
                  continuation_gap = excluded.continuation_gap,
                  orchestration_json = excluded.orchestration_json,
                  status = excluded.status,
                  timeline = excluded.timeline,
                  closed_at = excluded.closed_at,
                  updated_at = current_timestamp
                """,
                (
                    meeting_id,
                    tenant_id,
                    company_id,
                    business_id,
                    workspace_id,
                    title,
                    agenda,
                    background,
                    json.dumps(participants, ensure_ascii=False),
                    leader_employee_id,
                    ceo_participation_mode,
                    conversation_id,
                    json.dumps(context_refs, ensure_ascii=False),
                    decision_ref,
                    json.dumps(work_refs, ensure_ascii=False),
                    json.dumps(result_refs, ensure_ascii=False),
                    continuation_gap,
                    json.dumps(orchestration, ensure_ascii=False),
                    status,
                    json.dumps(timeline, ensure_ascii=False),
                    closed_at,
                ),
            )
            for reference in context_refs:
                connection.execute(
                    "insert or ignore into typed_object_references(reference_id, tenant_id, company_id, workspace_id, "
                    "source_type, source_ref, relation, target_type, target_ref, created_by) "
                    "values (?, ?, ?, ?, 'MEETING', ?, 'USES_REFERENCE', ?, ?, ?)",
                    (
                        f"meeting-reference-{uuid.uuid4()}", tenant_id, company_id, workspace_id,
                        meeting_id, reference["type"], reference["ref"], leader_employee_id,
                    ),
                )
        row = self.get_strategy_meeting(tenant_id, meeting_id)
        if row is None:
            raise KeyError("strategy meeting was not saved")
        return row

    def get_strategy_meeting(self, tenant_id: str, meeting_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                select meeting_id, tenant_id, company_id, business_id, workspace_id,
                       title, agenda, background, participants, leader_employee_id,
                       ceo_participation_mode, conversation_id, context_refs, decision_ref,
                       work_refs, result_refs, continuation_gap, status, timeline, closed_at,
                       orchestration_json,
                       created_at, updated_at
                from strategy_meetings
                where tenant_id = ? and meeting_id = ?
                """,
                (tenant_id, meeting_id),
            ).fetchone()
        return None if row is None else self._strategy_meeting_from_row(row)

    def list_strategy_meetings(self, tenant_id: str, company_id: str = "") -> list[dict[str, Any]]:
        with self.connect() as connection:
            company_filter = " and company_id = ?" if company_id else ""
            params = (tenant_id, company_id) if company_id else (tenant_id,)
            rows = connection.execute(
                f"""
                select meeting_id, tenant_id, company_id, business_id, workspace_id,
                       title, agenda, background, participants, leader_employee_id,
                       ceo_participation_mode, conversation_id, context_refs, decision_ref,
                       work_refs, result_refs, continuation_gap, status, timeline, closed_at,
                       orchestration_json,
                       created_at, updated_at
                from strategy_meetings
                where tenant_id = ?{company_filter}
                order by created_at desc, meeting_id
                """,
                params,
            ).fetchall()
        return [self._strategy_meeting_from_row(row) for row in rows]

    @staticmethod
    def _strategy_meeting_from_row(row: dict[str, Any]) -> dict[str, Any]:
        data = dict(row)
        for key in ("participants", "timeline", "context_refs", "work_refs", "result_refs", "orchestration_json"):
            try:
                data[key] = json.loads(data[key]) if data.get(key) else []
            except Exception:
                data[key] = {} if key == "orchestration_json" else []
        data["orchestration"] = data.pop("orchestration_json")
        return data

    def disable_credential_metadata(self, tenant_id: str, credential_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """
                update credential_metadata
                set status = 'disabled', disabled_at = current_timestamp,
                    updated_at = current_timestamp
                where tenant_id = ? and credential_id = ?
                """,
                (tenant_id, credential_id),
            )
        row = self.get_credential_metadata(tenant_id, credential_id)
        if row is None:
            raise KeyError("credential metadata not found")
        return row

    def delete_credential_metadata(self, tenant_id: str, credential_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """
                update credential_metadata
                set status = 'deleted', disabled_at = current_timestamp,
                    updated_at = current_timestamp
                where tenant_id = ? and credential_id = ?
                """,
                (tenant_id, credential_id),
            )
        row = self.get_credential_metadata(tenant_id, credential_id)
        if row is None:
            raise KeyError("credential metadata not found")
        return row

    @staticmethod
    def _credential_metadata_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["encrypted_metadata"] = json.loads(item["encrypted_metadata"] or "{}")
        return item

    # ── Self-use v1 (Wave 2 · F2 成果展示中心): content_publish_packages ──
    def save_content_publish_package(
        self,
        *,
        tenant_id: str,
        package_id: str,
        source_workflow: str,
        version: str,
        language: str,
        brand_voice_ref: str,
        platforms_targeted: list[str],
        artifacts: list[dict[str, Any]],
        status: str,
        published_platforms: list[str],
    ) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """
                insert or replace into content_publish_packages (
                  package_id, tenant_id, source_workflow, version, language,
                  brand_voice_ref, platforms_targeted, artifacts_json, status,
                  published_platforms, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
                """,
                (
                    package_id, tenant_id, source_workflow, version, language,
                    brand_voice_ref, json.dumps(platforms_targeted, ensure_ascii=False),
                    json.dumps(
                        [
                            a.model_dump() if hasattr(a, "model_dump")
                            else (a.to_dict() if hasattr(a, "to_dict") else a)
                            for a in artifacts
                        ],
                        ensure_ascii=False,
                    ),
                    status, json.dumps(published_platforms, ensure_ascii=False),
                ),
            )
        return self.get_content_publish_package(tenant_id, package_id)

    def get_content_publish_package(self, tenant_id: str, package_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "select * from content_publish_packages where tenant_id = ? and package_id = ?",
                (tenant_id, package_id),
            ).fetchone()
        if row is None:
            return None
        return self._content_publish_package_from_row(row)

    def list_content_publish_packages(self, tenant_id: str, limit: int = 50) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                "select * from content_publish_packages where tenant_id = ? "
                "order by created_at desc limit ?",
                (tenant_id, limit),
            ).fetchall()
        return [self._content_publish_package_from_row(r) for r in rows]

    def update_content_publish_package_status(
        self,
        *,
        tenant_id: str,
        package_id: str,
        status: str,
        published_platforms: list[str],
    ) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """
                update content_publish_packages set status = ?, published_platforms = ?,
                  updated_at = current_timestamp where tenant_id = ? and package_id = ?
                """,
                (status, json.dumps(published_platforms, ensure_ascii=False), tenant_id, package_id),
            )
        row = self.get_content_publish_package(tenant_id, package_id)
        if row is None:
            raise KeyError("content publish package not found")
        return row

    @staticmethod
    def _content_publish_package_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["platforms_targeted"] = json.loads(item["platforms_targeted"] or "[]")
        item["artifacts"] = json.loads(item["artifacts_json"] or "[]")
        item["published_platforms"] = json.loads(item["published_platforms"] or "[]")
        item.pop("artifacts_json", None)
        return item

    # ── Self-use v1 (Wave 2 · F2 成果展示中心): content_workflow_runs ──
    def list_content_workflow_runs(self, tenant_id: str, limit: int = 50) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                "select * from content_workflow_runs where tenant_id = ? "
                "order by created_at desc limit ?",
                (tenant_id, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def list_employee_templates(
        self,
        tenant_id: str,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        # Self-use v1（主理人裁定）：部门类型以 ``department_types`` 目录为单一真相源，
        # 不再硬编码 ``software_rnd``（含新增 tech.rd / content.growth）。
        allowed_types = [row["type_key"] for row in self.list_department_types()]
        if "software_rnd" not in allowed_types:
            allowed_types.append("software_rnd")
        clauses = [
            "(source = 'official' or (source = 'tenant_private' and tenant_id = ?))",
            f"department_type in ({','.join('?' for _ in allowed_types)})",
        ]
        params: list[Any] = [tenant_id, *allowed_types]
        if not include_inactive:
            clauses.append("enabled = 1")
        with self.connect() as connection:
            rows = connection.execute(
                "select id, slug, name, role, responsibility, description, department_type, "
                "default_instructions, default_capability_types_json, "
                "default_model_policy_json, default_workflow_step_types_json, "
                "guardrails_json, default_skill, default_tool, source, tenant_id, enabled, created_at "
                "from employee_templates where "
                + " and ".join(f"({clause})" for clause in clauses)
                + " order by source, id",
                params,
            ).fetchall()
        return [self._employee_template_from_row(row) for row in rows]

    def list_department_templates(
        self,
        tenant_id: str,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        # Self-use v1（主理人裁定）：部门类型以 ``department_types`` 目录为单一真相源，
        # 不再硬编码 ``software_rnd``。所有已注册类型（含新增 tech.rd / content.growth）
        # 都返回；``software_rnd`` 不在注册表时仍向下兼容。
        allowed_types = [row["type_key"] for row in self.list_department_types()]
        if "software_rnd" not in allowed_types:
            allowed_types.append("software_rnd")
        clauses = [
            "(source = 'official' or (source = 'tenant_private' and tenant_id = ?))",
            f"department_type in ({','.join('?' for _ in allowed_types)})",
        ]
        params: list[Any] = [tenant_id, *allowed_types]
        if not include_inactive:
            clauses.append("enabled = 1")
        with self.connect() as connection:
            rows = connection.execute(
                "select id, slug, name, department_type, description, "
                "default_employee_templates_json, default_workflow_template_id, "
                "default_capability_types_json, source, tenant_id, enabled, created_at "
                "from department_templates where "
                + " and ".join(f"({clause})" for clause in clauses)
                + " order by source, id",
                params,
            ).fetchall()
        return [self._department_template_from_row(row) for row in rows]

    @staticmethod
    def _employee_template_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["default_capability_types"] = json.loads(
            item.pop("default_capability_types_json") or "[]"
        )
        item["default_model_policy"] = json.loads(
            item.pop("default_model_policy_json") or "{}"
        )
        item["default_workflow_step_types"] = json.loads(
            item.pop("default_workflow_step_types_json") or "[]"
        )
        item["guardrails"] = json.loads(item.pop("guardrails_json") or "[]")
        item["enabled"] = bool(item["enabled"])
        return item

    @staticmethod
    def _department_template_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["default_employee_templates"] = json.loads(
            item.pop("default_employee_templates_json") or "[]"
        )
        item["default_capability_types"] = json.loads(
            item.pop("default_capability_types_json") or "[]"
        )
        item["enabled"] = bool(item["enabled"])
        return item

    def save_tenant_model_preference(
        self,
        *,
        tenant_id: str,
        model_key: str,
        gateway_ref: str,
        model_name: str,
        source: str = "official",
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                "insert into tenant_model_preferences "
                "(tenant_id, model_key, gateway_ref, model_name, source, updated_at) "
                "values (?, ?, ?, ?, ?, current_timestamp) "
                "on conflict(tenant_id) do update set "
                "model_key = excluded.model_key, "
                "gateway_ref = excluded.gateway_ref, "
                "model_name = excluded.model_name, "
                "source = excluded.source, "
                "updated_at = current_timestamp",
                (tenant_id, model_key, gateway_ref, model_name, source),
            )

    def get_tenant_model_preference(self, tenant_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "select tenant_id, model_key, gateway_ref, model_name, source, updated_at "
                "from tenant_model_preferences where tenant_id = ?",
                (tenant_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def delete_tenant_model_preference(self, tenant_id: str) -> None:
        with self.connect() as connection:
            connection.execute(
                "delete from tenant_model_preferences where tenant_id = ?",
                (tenant_id,),
            )

    def save_tenant_department_activations(
        self, tenant_id: str, department_type_keys: Sequence[str]
    ) -> None:
        """Replace tenant-local department activation references.

        Stores only official department type keys selected by Workspace. The
        caller validates catalog membership/status before invoking this method.
        """
        with self.connect() as connection:
            connection.execute(
                "delete from tenant_department_activations where tenant_id = ?",
                (tenant_id,),
            )
            connection.executemany(
                "insert into tenant_department_activations "
                "(tenant_id, department_type_key, source, enabled, display_order, updated_at) "
                "values (?, ?, 'official', 1, ?, current_timestamp)",
                [
                    (tenant_id, department_type_key, index)
                    for index, department_type_key in enumerate(department_type_keys)
                ],
            )

    def list_tenant_department_activations(self, tenant_id: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                "select tenant_id, department_type_key, source, enabled, display_order, updated_at "
                "from tenant_department_activations "
                "where tenant_id = ? and enabled = 1 "
                "order by display_order, department_type_key",
                (tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    # ── ADR-0017 S4 D4.platform (issue 060): 跨公司策略 / 全局护栏持久化 ──
    def save_platform_policy(
        self,
        policy_id: str,
        policy_key: str,
        policy_value: str,
        tenant_scope: str,
        enabled: bool = True,
    ) -> None:
        """Upsert 一条跨公司策略 / 全局护栏（policy_key 唯一维度，幂等）。

        供 D4.platform ``CompanyGovernance.cross_company_policy('set')`` 调用。
        不写 evolution_events（治理事件经 EvolutionEventLog.record 单独留痕）。
        """
        with self.connect() as connection:
            connection.execute(
                "insert into platform_policies "
                "(policy_id, policy_key, policy_value, tenant_scope, enabled, updated_at) "
                "values (?, ?, ?, ?, ?, current_timestamp) "
                "on conflict(policy_key) do update set "
                "policy_value = excluded.policy_value, "
                "tenant_scope = excluded.tenant_scope, "
                "enabled = excluded.enabled, "
                "updated_at = current_timestamp",
                (
                    policy_id,
                    policy_key,
                    policy_value,
                    tenant_scope,
                    1 if enabled else 0,
                ),
            )

    def get_platform_policy(self, policy_key: str) -> dict[str, Any] | None:
        """按 policy_key 取策略；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select * from platform_policies where policy_key = ?",
                (policy_key,),
            ).fetchone()
        return dict(row) if row is not None else None

    def list_platform_policies(
        self, tenant_scope: str | None = None
    ) -> list[dict[str, Any]]:
        """列出跨公司策略 / 全局护栏。

        可传 ``tenant_scope`` 过滤为「该租户专属 + 全局('all')」；不传则全量。
        依赖 S1 D1.impl 租户边界。供平台管理后台只读投影。
        """
        clauses: list[str] = []
        params: list[Any] = []
        if tenant_scope is not None:
            clauses.append("(tenant_scope = ? or tenant_scope = 'all')")
            params.append(tenant_scope)
        sql = "select * from platform_policies"
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by policy_key"
        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def set_platform_policy_enabled(self, policy_key: str, enabled: bool) -> None:
        """启停某策略（enabled 标志）。供 ``cross_company_policy`` 的 'disable' /
        'enable' 动作调用。不写 evolution_events（受控写仅 policy_set）。"""
        with self.connect() as connection:
            connection.execute(
                "update platform_policies set enabled = ?, updated_at = current_timestamp "
                "where policy_key = ?",
                (1 if enabled else 0, policy_key),
            )

    # ── ADR-0017 S1 D1.impl (issue 057): 租户注册表只读投影 ──
    def list_tenants(self) -> list[dict[str, Any]]:
        """列出已注册租户（tenant 注册表）。只读，供平台管理后台租户总览。

        仅承载租户身份（tenant_id / name），绝不返回任何凭证/密钥。
        """
        with self.connect() as connection:
            rows = connection.execute(
                "select * from tenants order by tenant_id"
            ).fetchall()
        return [dict(row) for row in rows]

    # ── ADR-0017 S1 D1.impl (issue 063): 租户扩展 CRUD ──
    def create_tenant(
        self,
        tenant_id: str,
        name: str,
        plan_tier: str = "free",
        contact_email: str = "",
        status: str = "active",
        description: str = "",
    ) -> dict[str, Any]:
        """新增租户。tenant_id 为 PK；重复 → IntegrityError。无凭证列。"""
        _validate_tenant_status(status)
        with self.connect() as connection:
            connection.execute(
                "insert into tenants "
                "(tenant_id, name, plan_tier, contact_email, status, description) "
                "values (?, ?, ?, ?, ?, ?)",
                (tenant_id, name, plan_tier, contact_email, status, description),
            )
        return self.get_tenant(tenant_id)

    def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        """按 PK 取租户；不存在返回 None。"""
        with self.connect() as connection:
            row = connection.execute(
                "select * from tenants where tenant_id = ?",
                (tenant_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def update_tenant(
        self,
        tenant_id: str,
        name: str | None = None,
        plan_tier: str | None = None,
        contact_email: str | None = None,
        status: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """编辑租户字段。仅对非 None 参数生成赋值。"""
        if status is not None:
            _validate_tenant_status(status)
        assignments: list[str] = []
        params: list[Any] = []
        if name is not None:
            assignments.append("name = ?")
            params.append(name)
        if plan_tier is not None:
            assignments.append("plan_tier = ?")
            params.append(plan_tier)
        if contact_email is not None:
            assignments.append("contact_email = ?")
            params.append(contact_email)
        if status is not None:
            assignments.append("status = ?")
            params.append(status)
        if description is not None:
            assignments.append("description = ?")
            params.append(description)
        if not assignments:
            return self.get_tenant(tenant_id)
        params.append(tenant_id)
        with self.connect() as connection:
            connection.execute(
                f"update tenants set {', '.join(assignments)} "
                "where tenant_id = ?",
                params,
            )
        return self.get_tenant(tenant_id)

    def set_tenant_status(self, tenant_id: str, status: str) -> dict[str, Any]:
        """租户状态机切换（active / inactive / suspended）。"""
        _validate_tenant_status(status)
        with self.connect() as connection:
            connection.execute(
                "update tenants set status = ? where tenant_id = ?",
                (status, tenant_id),
            )
        return self.get_tenant(tenant_id)

    # ── AuditEvent 只读投影 ──
    def list_audit_events(
        self,
        tenant_id: str | None = None,
        event_type: str | None = None,
        since: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """从 evolution_events 表查询受控命名空间审计事件。

        白名单命名空间：只暴露 capability.*、governance.*、credential.* 与 workflow.*，
        绝不泄漏 usage.* 或其他未授权事件类型。可选按 tenant_id / event_type /
        since 过滤；ORDER BY created_at DESC，LIMIT 可控。payload 保持 JSON
        字符串（不解包），由调用方按需解析。「零写」——纯 SELECT，绝不
        INSERT/UPDATE/DELETE。
        """
        clauses = [
            "(event_type like 'capability.%' or event_type like 'governance.%' or event_type like 'credential.%' or event_type like 'workflow.%')",
        ]
        params: list[Any] = []

        if tenant_id is not None:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)

        if event_type is not None:
            clauses.append("event_type = ?")
            params.append(event_type)

        if since is not None:
            clauses.append("created_at >= ?")
            params.append(since)

        sql = (
            "select * from evolution_events where "
            + " and ".join(clauses)
            + " order by created_at desc limit ?"
        )
        params.append(limit)

        with self.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
