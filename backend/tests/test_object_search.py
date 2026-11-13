"""Tests for company-wide object search (read-only)."""
from __future__ import annotations

import json
import os
import tempfile

import pytest

from app.database import Database
from app.object_search_service import ObjectSearchService
from app.tenant_context import TenantContext


TENANT = "tenant-search"
COMPANY = "company-search"
OTHER_COMPANY = "company-search-other"
CEO = "ceo-search"


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "search.sqlite"
    db = Database(str(path))
    db.initialize()
    _seed(db)
    return db


def _seed(db: Database) -> None:
    at = "2026-10-07T00:00:00+00:00"
    with TenantContext.scope(TENANT):
        with db.connect() as conn:
            conn.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name, status, created_at, updated_at) "
                "values (?, ?, ?, 'Search Co', 'active', ?, ?)",
                (COMPANY, TENANT, CEO, at, at),
            )
            conn.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name, status, created_at, updated_at) "
                "values (?, ?, ?, 'Other Co', 'active', ?, ?)",
                (OTHER_COMPANY, TENANT, CEO, at, at),
            )
            conn.execute(
                "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, status, created_at, updated_at) "
                "values ('dept-data', ?, ?, 'tpl-analytics', '数据分析部', 'analytics', 'active', ?, ?)",
                (TENANT, COMPANY, at, at),
            )
            conn.execute(
                "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, status, created_at, updated_at) "
                "values ('dept-data-other', ?, ?, 'tpl-analytics', '数据分析部', 'analytics', 'active', ?, ?)",
                (TENANT, OTHER_COMPANY, at, at),
            )
            # Business
            conn.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, created_at, updated_at) "
                "values ('biz-1', ?, ?, 'dept-data', '搜索业务·内容增长', 'ACTIVE', ?, ?)",
                (TENANT, COMPANY, at, at),
            )
            # Workspace
            conn.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, created_at, updated_at) "
                "values ('ws-1', ?, ?, 'biz-1', '搜索工作空间·内容增长', 'ACTIVE', ?, ?)",
                (TENANT, COMPANY, at, at),
            )
            # Employee
            conn.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, lifecycle_status, data_json, created_at, updated_at) "
                "values ('emp-1', ?, 'AI_EMPLOYEE', ?, 'ws-1', ?, 'ACTIVE', ?, ?, ?)",
                (TENANT, COMPANY, CEO, json.dumps({"name": "搜索员工·司衡", "role": "公司经营分析师"}, ensure_ascii=False), at, at),
            )
            # Business object (writing snapshot style)
            conn.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, lifecycle_status, data_json, created_at, updated_at) "
                "values ('obj-1', ?, 'PACKAGE_DOMAIN_OBJECT', ?, 'ws-1', ?, 'ACTIVE', ?, ?, ?)",
                (TENANT, COMPANY, CEO, json.dumps({"objectType": "MarketSnapshot", "kind": "市场快照", "title": "搜索对象·Q4 市场观察"}, ensure_ascii=False), at, at),
            )
            # Knowledge
            conn.execute(
                "insert into knowledge_entries(id, tenant_id, company_id, title, body, source_type, source_label, content_sha256, lifecycle_status, created_at, updated_at) "
                "values ('kn-1', ?, ?, '搜索资料·行业研究笔记', 'body', 'manual', '资料库', 'sha', 'ACTIVE', ?, ?)",
                (TENANT, COMPANY, at, at),
            )
            # Meeting
            conn.execute(
                "insert into strategy_meetings(meeting_id, tenant_id, company_id, title, status, created_at, updated_at) "
                "values ('mt-1', ?, ?, '搜索会议·季度战略会议', 'scheduled', ?, ?)",
                (TENANT, COMPANY, at, at),
            )
            # Decision
            conn.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, lifecycle_status, data_json, created_at, updated_at) "
                "values ('dec-1', ?, 'DECISION_PACKET', ?, 'ws-1', ?, 'WAITING_CEO', ?, ?, ?)",
                (TENANT, COMPANY, CEO, json.dumps({"problem": "搜索决策·是否调整投入", "workRef": "work-1"}, ensure_ascii=False), at, at),
            )
            # Task
            conn.execute(
                "insert into tasks(task_id, company_id, workspace_id, content, status, created_at, updated_at) "
                "values ('task-1', ?, 'ws-1', '搜索任务·撰写经营分析报告', 'IN_PROGRESS', ?, ?)",
                (COMPANY, at, at),
            )
            # Artifact (result)
            conn.execute(
                "insert into artifacts(artifact_id, tenant_id, task_id, title, artifact_type, status, content, source_ref, content_sha256, created_at, updated_at) "
                "values ('art-1', ?, 'task-1', '搜索结果·经营分析报告', 'execution_result', 'generated', '', 'ref-1', 'sha', ?, ?)",
                (TENANT, at, at),
            )
            # Other-company objects that must NOT leak
            conn.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, created_at, updated_at) "
                "values ('biz-other', ?, ?, 'dept-data-other', '搜索业务·其他公司', 'ACTIVE', ?, ?)",
                (TENANT, OTHER_COMPANY, at, at),
            )
            conn.execute(
                "insert into tasks(task_id, company_id, content, status, created_at, updated_at) "
                "values ('task-other', ?, '搜索任务·其他公司任务', 'IN_PROGRESS', ?, ?)",
                (OTHER_COMPANY, at, at),
            )


def test_search_returns_all_nine_groups(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        result = service.search(COMPANY, "搜索")
    types = {g["type"] for g in result["groups"]}
    assert types == {
        "business", "workspace", "employee", "business_object",
        "knowledge", "meeting", "decision", "task", "result",
    }
    for group in result["groups"]:
        assert group["items"], f"{group['type']} should have items"
        for item in group["items"]:
            assert item["id"] and item["title"]
            assert "context" in item


def test_search_empty_query_returns_empty_groups(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        result = service.search(COMPANY, "   ")
    assert result == {"query": "", "groups": []}


def test_search_unknown_company_raises(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        with pytest.raises(KeyError):
            service.search("company-nope", "增长")


def test_search_query_too_long_raises(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        with pytest.raises(ValueError):
            service.search(COMPANY, "x" * 65)


def test_search_like_wildcards_are_escaped(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        # "%" should not match everything; it should be treated literally.
        result = service.search(COMPANY, "%")
        flat = [item["title"] for g in result["groups"] for item in g["items"]]
        assert not flat


def test_cross_company_isolation(database):
    with TenantContext.scope(TENANT):
        service = ObjectSearchService(database)
        result = service.search(COMPANY, "搜索")
    ids = {item["id"] for g in result["groups"] for item in g["items"]}
    assert "biz-other" not in ids
    assert "task-other" not in ids
    # Confirm other-company objects exist by querying them directly.
    with TenantContext.scope(TENANT):
        other = service.search(OTHER_COMPANY, "搜索")
    other_ids = {item["id"] for g in other["groups"] for item in g["items"]}
    assert "biz-other" in other_ids
    assert "task-other" in other_ids


def test_search_group_limit_capped(database):
    at = "2026-10-07T00:00:00+00:00"
    with TenantContext.scope(TENANT):
        with database.connect() as conn:
            for i in range(12):
                conn.execute(
                    "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, created_at, updated_at) "
                    "values (?, ?, ?, 'dept-data', ?, 'ACTIVE', ?, ?)",
                    (f"biz-cap-{i}", TENANT, COMPANY, f"搜索业务 {i}", at, at),
                )
        service = ObjectSearchService(database)
        result = service.search(COMPANY, "搜索")
    business_group = next(g for g in result["groups"] if g["type"] == "business")
    assert len(business_group["items"]) <= 8


def test_no_new_tables_created(database):
    with TenantContext.scope(TENANT):
        with database.connect() as conn:
            before = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
        service = ObjectSearchService(database)
        service.search(COMPANY, "搜索")
        with database.connect() as conn:
            after = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
    assert before == after
