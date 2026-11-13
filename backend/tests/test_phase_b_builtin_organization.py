"""Fresh Company bootstrap, using only external pytest temporary databases."""
import json
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.database import Database
from app.employee_templates import EmployeeTemplateContract
from app.runtime import RuntimeFoundation
from app.organization_projection import department_assignments
from app.conversation_service import ConversationService
from app.runtime import RuntimeScopeError
from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
from app.tenant_context import TenantContext


def founding(db):
    foundation = RuntimeFoundation(db)
    run = foundation.create("FOUNDING_RUN", owner_ref="ceo-phase-b")
    for state, actor in (("INTENT_CAPTURED", "CEO"), ("CLARIFYING", "SYSTEM"),
                         ("PROPOSED", "SYSTEM"), ("CEO_CONFIRMED", "CEO")):
        run = foundation.transition(run["entity_id"], state, actor=actor, trigger="test")
    return run["entity_id"]


def create(db, run):
    return RuntimeFoundation(db).materialize_company(
        run, company_id="company-phase-b", ceo_id="ceo-phase-b", name="Phase B Company")


def test_fresh_no_key_concurrent_retry_restart_and_user_edits(tmp_path):
    db = Database(str(tmp_path / "bootstrap.sqlite"))
    db.initialize()
    run = founding(db)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: create(db, run), range(2)))
    assert results[0][1]["entity_id"] == results[1][1]["entity_id"]
    with db.connect() as con:
        assert con.execute("select count(*) from companies where company_id='company-phase-b'").fetchone()[0] == 1
        employees = con.execute("select * from employee_instances where company_id='company-phase-b'").fetchall()
        departments = con.execute("select * from department_instances where company_id='company-phase-b'").fetchall()
        assert len(employees) == 7 and len({r["id"] for r in employees}) == 7
        assert len(departments) == 2
        assert sorted(sum(e["department_id"] == d["id"] for e in employees) for d in departments) == [1, 6]
        assert con.execute("select count(*) from canonical_businesses where company_id='company-phase-b'").fetchone()[0] == 0
        assert con.execute("select count(*) from employee_capability_bindings where employee_id in "
                           "(select id from employee_instances where company_id='company-phase-b')").fetchone()[0] == 0
        assignments = con.execute("select data_json from runtime_entities where company_id='company-phase-b' "
                                  "and entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchall()
        assert len(assignments) == 7
        for row in assignments:
            data = json.loads(row[0])
            assert data["scopeType"] == "DEPARTMENT"
            assert data["scopeRef"] in {d["id"] for d in departments}
            assert data["employeeRef"] in {e["id"] for e in employees}
            assert data["capabilityBindingRefs"] == []
    service = EmployeeTemplateContract(db)
    edited = employees[0]["id"]
    service.update_employee_instance(edited, {"name": "用户编辑保留"})
    restarted = Database(db.path)
    create(restarted, run)
    assert EmployeeTemplateContract(restarted).get_employee_instance(edited)["name"] == "用户编辑保留"
    assert len(department_assignments(restarted, "company-phase-b")) == 7
    from app.runtime import ResponsibilityRoutingRuntime
    leader = next(a for a in department_assignments(restarted, "company-phase-b") if a["data"].get("isLeader"))
    replacement = next(e["id"] for e in employees if e["role"] == "行业研究专家")
    changed = ResponsibilityRoutingRuntime(restarted).update_assignment(leader["entity_id"], employee_ref=replacement)
    create(restarted, run)
    retained = RuntimeFoundation(restarted).get(leader["entity_id"])
    assert retained["data"]["employeeRef"] == replacement
    assert retained["data"]["revision"] == changed["data"]["revision"]
    with restarted.connect() as con:
        assert {r[0] for r in con.execute("select id from employee_instances where company_id='company-phase-b'")} == {e["id"] for e in employees}
    removed = next(e["id"] for e in employees if e["role"] == "质量验证专家")
    service.delete_employee_instance(removed)
    create(restarted, run)
    with restarted.connect() as con:
        assert con.execute("select count(*) from employee_instances where company_id='company-phase-b'").fetchone()[0] == 7
        assert con.execute("select enabled from employee_instances where id=?", (removed,)).fetchone()[0] == 0


def test_failure_rolls_back_company_and_organization(tmp_path, monkeypatch):
    db = Database(str(tmp_path / "failure.sqlite"))
    db.initialize()
    run = founding(db)
    original = EmployeeTemplateContract.materialize_builtin_organization

    def fail(self, connection, **kwargs):
        original(self, connection, **kwargs)
        raise RuntimeError("isolated failure injection")

    with monkeypatch.context() as patch:
        patch.setattr(EmployeeTemplateContract, "materialize_builtin_organization", fail)
        with pytest.raises(RuntimeError, match="isolated failure"):
            create(db, run)
    with db.connect() as con:
        for table in ("companies", "employee_instances", "department_instances"):
            assert con.execute(f"select count(*) from {table} where company_id='company-phase-b'").fetchone()[0] == 0
    assert RuntimeFoundation(db).get(run)["lifecycle_status"] == "CEO_CONFIRMED"
    create(db, run)


def test_department_context_and_work_without_synthetic_parent(tmp_path):
    """Scope readiness is independent of Provider configuration or autonomy acceptance."""
    db = Database(str(tmp_path / "scope-gate.sqlite"))
    db.initialize()
    run = founding(db)
    create(db, run)
    leader = next(item for item in department_assignments(db, "company-phase-b")
                  if item["data"].get("isLeader"))
    with TenantContext.scope("selfuse", company_id="company-phase-b", ceo_id="ceo-phase-b", role="ceo"):
        context = ConversationService(db).context("company-phase-b", leader["data"]["employeeRef"], leader["entity_id"])
        assert context["scope_type"] == "DEPARTMENT" and context["workspace_id"] is None
        with pytest.raises(ChildWorkError, match="explicit canonical execution scope"):
            CanonicalChildWorkRuntime(db).create_cycle_work(
                company_id="company-phase-b", workspace_id="", assignment_ref=leader["entity_id"],
                release_key="department-intent", contract={"problem": "提出新业务目标", "expectedResult": "建设建议"})
        created = CanonicalChildWorkRuntime(db).create_cycle_work(
            company_id="company-phase-b", scope_type="DEPARTMENT", scope_ref=context["scope_ref"],
            assignment_ref=leader["entity_id"], release_key="department-intent",
            contract={"problem": "提出新业务目标", "expectedResult": "建设建议"})
        assert created["work"]["workspace_id"] is None
    with db.connect() as con:
        assert con.execute("select count(*) from canonical_businesses where company_id='company-phase-b'").fetchone()[0] == 0
        assert con.execute("select count(*) from workspaces where company_id='company-phase-b'").fetchone()[0] == 0
        assert con.execute("select count(*) from runtime_entities where company_id='company-phase-b' and entity_type in ('WORK','CYCLE')").fetchone()[0] == 2


def test_delegation_endpoint_persists_without_key_and_replays(tmp_path):
    from fastapi import FastAPI, Request
    from fastapi.testclient import TestClient
    from app.api.team_operating_router import build_team_operating_router

    db = Database(str(tmp_path / "delegation.sqlite"))
    db.initialize()
    create(db, founding(db))
    leader = next(item for item in department_assignments(db, "company-phase-b") if item["data"].get("isLeader"))
    app = FastAPI()
    actor = {"role": "owner"}
    @app.middleware("http")
    async def identity(request: Request, call_next):
        with TenantContext.scope("selfuse", company_id="company-phase-b", ceo_id="ceo-phase-b", role=actor["role"]):
            return await call_next(request)
    app.include_router(build_team_operating_router(db))
    url = f"/team-operating/assignments/{leader['entity_id']}/work"
    payload = {"problem": "建设客户反馈业务", "expected_result": "建设建议", "request_id": "same"}
    with TestClient(app) as client:
        first = client.post(url, json=payload)
        assert first.status_code == 200, first.text
        assert client.post(url, json=payload).json()["work"]["entity_id"] == first.json()["work"]["entity_id"]
        assert client.post(url, json={**payload, "problem": "different"}).status_code == 422
        for role in ("employee", "admin", "test", ""):
            actor["role"] = role
            assert client.post(url, json={**payload, "request_id": role or "anonymous"}).status_code == 422
    db.initialize()
    persisted = RuntimeFoundation(db).get(first.json()["work"]["entity_id"])
    assert persisted["data"]["holderEmployeeRef"] == leader["data"]["employeeRef"]
    assert persisted["workspace_id"] is None
    with db.connect() as con:
        assert con.execute("select count(*) from tasks").fetchone()[0] == 0
        assert con.execute("select count(*) from canonical_businesses").fetchone()[0] == 0
