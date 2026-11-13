from __future__ import annotations

import json

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.shared_workspace_router import build_shared_workspace_router
from app.database import Database
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext


def test_general_workspace_contract_is_truthful_and_restartable(tmp_path):
    path = tmp_path / "general.sqlite"
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values ('company', 'tenant', 'ceo', '公司')"
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department', 'tenant', 'company', 'official.department.software_rnd', '业务部', 'business.general')"
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, goal, "
            "lifecycle_status, created_at, updated_at) values "
            "('business', 'tenant', 'company', 'department', '客户反馈业务', '每周形成一个可验证改进', "
            "'DRAFT', current_timestamp, current_timestamp)"
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
            "blueprint_version, status, business_relation_status, business_relation_reason, business_relation_source) "
            "values ('workspace', 'tenant', 'company', 'business', '客户反馈办公室', ?, 'generic-v1', 'DRAFT', "
            "'RESOLVED', '', 'CANONICAL_TEST')",
            (json.dumps({"businessType": "GENERIC", "productForm": "GENERIC"}),),
        )

    with TenantContext.scope("tenant", company_id="company", ceo_id="ceo", role="test"):
        first = SharedWorkspaceProjection(database).general_workspace("company", "workspace")
    assert first["goal"] == "每周形成一个可验证改进"
    assert first["operating_readiness"] == {
        "status": "NEEDS_DECISION",
        "reason": "尚未形成唯一的团队责任安排",
        "workflow_key": None,
        "owner": "CEO",
        "next_action": "确认团队责任与员工",
    }
    assert first["team"]["employees"] == []
    assert first["current_work"] == []

    app = FastAPI()

    @app.middleware("http")
    async def tenant_scope(request: Request, call_next):
        with TenantContext.scope("tenant", company_id="company", ceo_id="ceo", role="test"):
            return await call_next(request)

    app.include_router(build_shared_workspace_router(database))
    with TestClient(app) as client:
        response = client.get("/companies/company/workspaces/workspace/shared/general")
        assert response.status_code == 200
        assert response.json()["operating_readiness"]["status"] == "NEEDS_DECISION"

    reopened = Database(str(path))
    with TenantContext.scope("tenant", company_id="company", ceo_id="ceo", role="test"):
        assert SharedWorkspaceProjection(reopened).general_workspace("company", "workspace") == first
    with reopened.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("select count(*) from runtime_entities").fetchone()[0] == 0
