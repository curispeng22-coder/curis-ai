from __future__ import annotations

import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.knowledge_service import KnowledgeService
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import (
    BUSINESS,
    COMPANY,
    TENANT,
    WORKSPACE,
    add_team,
    app,
    seed,
)


def create_work(database: Database, key: str = "knowledge-work") -> str:
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        return GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            problem="依据客户访谈整理改进建议",
            expected_result="形成一项有来源的建议",
            constraints=["只使用已选择资料"],
            references=[],
            idempotency_key=key,
        )["work"]["entity_id"]


def test_canonical_knowledge_reference_context_result_archive_and_restart(tmp_path):
    path = tmp_path / "knowledge-productization.sqlite"
    database = seed(path)
    add_team(database)
    work_ref = create_work(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        company_entry = service.create_entry(
            title="客户访谈原则",
            body="优先处理重复出现且有原始访谈记录的问题。",
            company_id=COMPANY,
            target_type="COMPANY",
            target_ref=COMPANY,
            created_by="ceo",
        )
        workspace_entry = service.create_entry(
            title="本轮反馈摘录",
            body="三位客户反馈首次使用时不知道下一步。",
            company_id=COMPANY,
            target_type="WORKSPACE",
            target_ref=WORKSPACE,
            created_by="ceo",
        )
        first = service.add_work_references(
            work_ref, [company_entry["id"], workspace_entry["id"]], actor="ceo"
        )
        replay = service.add_work_references(
            work_ref, [workspace_entry["id"], company_entry["id"]], actor="ceo"
        )
        assert [item["id"] for item in first["references"]] == [item["id"] for item in replay["references"]]
        assert first["work"]["problem"] == "依据客户访谈整理改进建议"
        assert first["work"]["expected_result"] == "形成一项有来源的建议"
        prioritized = service.list_entries(company_id=COMPANY, sort="recent_used", limit=1)
        assert prioritized["entries"][0]["used_count"] == 1
        context = service.context_for_work(work_ref, query="客户反馈")
        assert [item["selection"] for item in context["references"]] == ["EXPLICIT", "EXPLICIT"]
        assert context["hydrated_bodies"] == 0
        assert all("body" not in item for item in context["references"])

    calls = []

    async def employee_execution(payload):
        calls.append(payload)
        if payload["mode"] == "submit":
            return {"task_ref": "task-knowledge-productization"}
        return {
            "output": json.dumps({
                "status": "ACCEPTED",
                "resultType": "general-business-result",
                "summary": "已形成有来源的改进建议",
                "problem": "",
            }, ensure_ascii=False),
            "task_status": "COMPLETED",
            "session_ref": "session-knowledge-productization",
            "artifact_refs": [],
            "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}},
        }

    with TestClient(app(database, employee_execution)) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
    assert response.status_code == 200, response.text
    prompt = next(item["prompt"] for item in calls if item["mode"] == "submit")
    assert "客户访谈原则" in prompt
    assert "本轮反馈摘录" in prompt
    assert "优先处理重复出现" in prompt
    assert "whole conversation" not in prompt.lower()

    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(reopened)
        used_by = service.used_by(company_entry["id"])["works"][0]
        assert used_by["work_ref"] == work_ref
        assert used_by["title"] == "依据客户访谈整理改进建议"
        results = service.related_results(company_entry["id"])["results"]
        assert {item["reference_id"] for item in results} == {"task:task-knowledge-productization"}
        archived = service.archive_entry(company_entry["id"], actor="ceo")
        assert archived["lifecycle_status"] == "ARCHIVED"
        assert service.used_by(company_entry["id"])["works"]
        with pytest.raises(ValueError, match="archived"):
            service.add_work_references(create_work(reopened, "second-work"), [company_entry["id"]], actor="ceo")
        with pytest.raises(sqlite3.IntegrityError, match="must be archived"):
            with reopened.connect() as connection:
                connection.execute("delete from knowledge_entries where id=?", (company_entry["id"],))
        assert reopened.connect


def test_scope_isolation_and_bounded_batches(tmp_path):
    database = seed(tmp_path / "knowledge-scale.sqlite")
    add_team(database)
    work_ref = create_work(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        for index in range(101):
            service.create_entry(
                title=f"规模资料 {index:03d}",
                body=f"可检索事实 {index:03d}",
                company_id=COMPANY,
                target_type="BUSINESS",
                target_ref=BUSINESS,
                created_by="ceo",
            )
        first = service.list_entries(company_id=COMPANY, target_type="BUSINESS", limit=50)
        second = service.list_entries(company_id=COMPANY, target_type="BUSINESS", limit=50, offset=50)
        last = service.list_entries(company_id=COMPANY, target_type="BUSINESS", limit=50, offset=100)
        assert (first["total"], len(first["entries"]), first["has_more"]) == (101, 50, True)
        assert (len(second["entries"]), second["has_more"]) == (50, True)
        assert (len(last["entries"]), last["has_more"]) == (1, False)
        assert len({item["id"] for item in [*first["entries"], *second["entries"], *last["entries"]]}) == 101

        with database.connect() as connection:
            connection.execute(
                "insert into companies(company_id,tenant_id,ceo_id,name) values('foreign-company',?,'ceo','Foreign')",
                (TENANT,),
            )
    with TenantContext.scope(TENANT, company_id="foreign-company", ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        foreign = service.create_entry(
            title="Foreign",
            body="outside",
            company_id="foreign-company",
            target_type="COMPANY",
            target_ref="foreign-company",
            created_by="ceo",
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        with pytest.raises(ValueError, match="outside"):
            service.add_work_references(work_ref, [foreign["id"]], actor="ceo")

    with TenantContext.scope("other-tenant", company_id="other-company", ceo_id="other", role="test"):
        with pytest.raises(KeyError):
            KnowledgeService(database).get_entry(foreign["id"])

    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


@pytest.mark.parametrize("scenario", ["unreferenced_match", "explicit_match", "no_match"])
def test_general_synthetic_knowledge_boundary_at_employee_submit(tmp_path, scenario):
    database = seed(tmp_path / "synthetic-context.sqlite")
    add_team(database)
    work_ref = create_work(database)
    query = "依据客户访谈整理改进建议 形成一项有来源的建议"
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        matched = None
        if scenario != "no_match":
            matched = service.create_entry(title="MATCHED_SYNTHETIC", body=query,
                summary="MATCHED_SUMMARY_SYNTHETIC", company_id=COMPANY,
                target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        if scenario == "explicit_match":
            service.create_entry(title="UNASSOCIATED_SYNTHETIC", body=query,
                summary="UNASSOCIATED_SUMMARY_SYNTHETIC", company_id=COMPANY,
                target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        service.create_entry(title="UNMATCHED_SYNTHETIC", body="unrelated words",
            summary="UNMATCHED_SUMMARY_SYNTHETIC", company_id=COMPANY,
            target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        with database.connect() as connection:
            connection.execute("insert into companies(company_id,tenant_id,ceo_id,name) values('foreign-company',?,'ceo','Foreign')", (TENANT,))
        if scenario == "explicit_match":
            service.add_work_references(work_ref, [matched["id"]], actor="ceo")
    with TenantContext.scope(TENANT, company_id="foreign-company", ceo_id="ceo", role="test"):
        KnowledgeService(database).create_entry(title="FOREIGN_SYNTHETIC", body=query,
            summary="FOREIGN_SUMMARY_SYNTHETIC", company_id="foreign-company",
            target_type="COMPANY", target_ref="foreign-company", created_by="ceo")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        context = KnowledgeService(database).context_for_work(work_ref, query=query)
        selections = [r["selection"] for r in context["references"]]
        assert selections == (["BOUNDED_RETRIEVAL"] if scenario == "unreferenced_match" else
            ["EXPLICIT", "BOUNDED_RETRIEVAL"] if scenario == "explicit_match" else [])
        assert "FOREIGN_SYNTHETIC" not in json.dumps(context)
        assert "UNMATCHED_SYNTHETIC" not in json.dumps(context)

    calls = []
    async def fake_execution(payload):
        calls.append(payload)
        if payload["mode"] == "submit":
            return {"task_ref": "task-synthetic-context"}
        return {"output": json.dumps({"status": "ACCEPTED", "resultType": "general-business-result",
                "summary": "synthetic", "problem": ""}), "task_status": "COMPLETED",
                "artifact_refs": [], "session_ref": "synthetic-session",
                "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}}}
    with TestClient(app(database, fake_execution)) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
    assert response.status_code == 200, response.text
    prompt = next(call["prompt"] for call in calls if call["mode"] == "submit")
    assert ("MATCHED_SUMMARY_SYNTHETIC" in prompt) == (scenario == "explicit_match")
    assert ("\"selection\":\"EXPLICIT\"" in prompt) == (scenario == "explicit_match")
    assert "UNASSOCIATED_SUMMARY_SYNTHETIC" not in prompt
    assert "UNMATCHED_SUMMARY_SYNTHETIC" not in prompt
    assert "FOREIGN_SUMMARY_SYNTHETIC" not in prompt


@pytest.mark.parametrize("invalid", ["archived", "missing", "wrong_workspace", "wrong_company", "wrong_tenant"])
def test_general_invalid_explicit_knowledge_fails_before_submit(tmp_path, invalid):
    database = seed(tmp_path / "invalid-context.sqlite")
    add_team(database)
    work_ref = create_work(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        item = service.create_entry(title="Synthetic", body="Synthetic content", company_id=COMPANY,
            target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        service.add_work_references(work_ref, [item["id"]], actor="ceo")
        if invalid == "archived":
            service.archive_entry(item["id"], actor="ceo")
        else:
            with database.connect() as connection:
                if invalid == "missing":
                    connection.execute("update typed_object_references set target_ref='missing-synthetic' where source_ref=?", (work_ref,))
                elif invalid == "wrong_workspace":
                    connection.execute("update knowledge_entries set target_type='WORKSPACE',target_ref='outside-synthetic' where id=?", (item["id"],))
                elif invalid == "wrong_company":
                    connection.execute("update typed_object_references set company_id='outside-synthetic' where source_ref=?", (work_ref,))
                else:
                    connection.execute("update knowledge_entries set tenant_id='outside-synthetic' where id=?", (item["id"],))
    calls = []
    async def fake_execution(payload):
        calls.append(payload)
        return {}
    with TestClient(app(database, fake_execution)) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
    assert response.status_code == 422, response.text
    assert calls == []


def test_general_explicit_knowledge_is_bounded_and_excludes_unassociated(tmp_path):
    database = seed(tmp_path / "bounded-context.sqlite")
    add_team(database)
    work_ref = create_work(database)
    query = "依据客户访谈整理改进建议 形成一项有来源的建议"
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        entries = [service.create_entry(title=f"EXPLICIT_SYNTHETIC_{n}", body="selected", company_id=COMPANY,
            target_type="COMPANY", target_ref=COMPANY, created_by="ceo") for n in range(4)]
        service.add_work_references(work_ref, [item["id"] for item in entries], actor="ceo")
        service.create_entry(title="AUTOMATIC_SYNTHETIC", body=query, company_id=COMPANY,
            target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
    calls = []
    async def fake_execution(payload):
        calls.append(payload)
        if payload["mode"] == "submit": return {"task_ref": "task-bounded-synthetic"}
        return {"output": json.dumps({"status": "ACCEPTED", "resultType": "general-business-result", "summary": "synthetic", "problem": ""}),
            "task_status": "COMPLETED", "artifact_refs": [], "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}}}
    with TestClient(app(database, fake_execution)) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
    assert response.status_code == 200, response.text
    prompt = next(call["prompt"] for call in calls if call["mode"] == "submit")
    assert sum(f"EXPLICIT_SYNTHETIC_{n}" in prompt for n in range(4)) == 3
    assert "AUTOMATIC_SYNTHETIC" not in prompt


@pytest.mark.parametrize("ref_location", ["contract", "inputRefs"])
@pytest.mark.parametrize("agent_bound", [False, True])
@pytest.mark.parametrize("revoked", [False, True])
def test_general_contract_reference_requires_current_association(tmp_path, monkeypatch, ref_location, agent_bound, revoked):
    from fastapi import FastAPI, Request
    from app.api.team_operating_router import build_team_operating_router
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.conversation_service import ConversationService
    from app.runtime import RuntimeFoundation

    database = seed(tmp_path / "revoked-reference.sqlite")
    add_team(database)
    work_ref = create_work(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="owner"):
        service = KnowledgeService(database)
        item = service.create_entry(title="REVOKED_SYNTHETIC", body="synthetic", company_id=COMPANY,
            target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        service.add_work_references(work_ref, [item["id"]], actor="ceo")
        work = RuntimeFoundation(database).get(work_ref)
        cycle_ref = work["data"]["cycleRef"]
        with database.connect() as connection:
            cycle_data = json.loads(connection.execute("select data_json from runtime_entities where tenant_id=? and entity_id=?", (TENANT, cycle_ref)).fetchone()[0])
            work_data = json.loads(connection.execute("select data_json from runtime_entities where tenant_id=? and entity_id=?", (TENANT, work_ref)).fetchone()[0])
            reference = "knowledge:" + item["id"]
            if ref_location == "contract": cycle_data["contract"]["references"] = [reference]
            else: work_data["inputRefs"] = [reference]
            if agent_bound: cycle_data["contract"]["agentBinding"] = {"bindingRef": "synthetic-binding"}
            connection.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?", (json.dumps(cycle_data), TENANT, cycle_ref))
            connection.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?", (json.dumps(work_data), TENANT, work_ref))
            if revoked:
                connection.execute("delete from typed_object_references where tenant_id=? and source_ref=? and target_ref=?", (TENANT, work_ref, item["id"]))
    checked = []
    if agent_bound:
        def fake_agent_source(self, current):
            checked.append(current["entity_id"])
            return {"context": {"assignment_ref": current["data"]["responsibilityAssignmentRef"],
                "employee_ref": current["data"]["holderEmployeeRef"]}}
        monkeypatch.setattr(ConversationService, "validate_agent_work_source", fake_agent_source)
        monkeypatch.setattr(CompanyExecutionPolicy, "require_unreserved_agent_work", lambda *_args: None)
    calls = []
    async def fake_execution(payload):
        calls.append(payload)
        if payload["mode"] == "submit": return {"task_ref": "task-reference-synthetic"}
        return {"output": json.dumps({"status": "ACCEPTED", "resultType": "general-business-result", "summary": "synthetic", "problem": ""}),
            "task_status": "COMPLETED", "artifact_refs": [], "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}}}
    application = FastAPI()
    @application.middleware("http")
    async def owner_scope(request: Request, call_next):
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="owner"):
            return await call_next(request)
    application.include_router(build_team_operating_router(database, fake_execution))
    with TestClient(application) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
    if revoked:
        assert response.status_code == 422, response.text
        assert "Knowledge reference is not selected for this Work" in response.text
        assert calls == []
    else:
        assert response.status_code == 200, response.text
        assert "REVOKED_SYNTHETIC" in next(call["prompt"] for call in calls if call["mode"] == "submit")
    if agent_bound: assert checked == [work_ref, work_ref]


@pytest.mark.parametrize("size", [200, 201, 3201, 4001])
def test_full_work_query_scoped_segments_tail_deduplication_and_original_guard(tmp_path, monkeypatch, size):
    database = seed(tmp_path / "long-knowledge.sqlite")
    add_team(database)
    work_ref = create_work(database)
    # Unique characters make a tail-only hit distinguishable from any earlier segment.
    query = "".join(chr(0x4e00 + i) for i in range(size))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        explicit = service.create_entry(title="Explicit", body=query,
            company_id=COMPANY, target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        tail = service.create_entry(title="Tail", body=query[(size - 1) // 200 * 200:],
            company_id=COMPANY, target_type="WORKSPACE", target_ref=WORKSPACE, created_by="ceo")
        service.add_work_references(work_ref, [explicit["id"]], actor="ceo")
        with database.connect() as con:
            con.execute("insert into workspaces(workspace_id,tenant_id,company_id,business_id,name,blueprint_json,"
                "blueprint_version,status,business_relation_status,business_relation_reason,business_relation_source) "
                "select 'other-workspace',tenant_id,company_id,business_id,'Other',blueprint_json,blueprint_version,"
                "status,business_relation_status,business_relation_reason,business_relation_source "
                "from workspaces where workspace_id=?", (WORKSPACE,))
        foreign = service.create_entry(title="Wrong workspace", body=query,
            company_id=COMPANY, target_type="WORKSPACE", target_ref="other-workspace", created_by="ceo")
        real_list = service.list_entries
        calls = []
        def observed_list(**kwargs):
            calls.append(dict(kwargs))
            return real_list(**kwargs)
        monkeypatch.setattr(service, "list_entries", observed_list)
        context = service.context_for_work(work_ref, query=query, limit=50)
        assert "".join(call["query"] for call in calls) == query
        assert all(1 <= len(call["query"]) <= 200 and call["company_id"] == COMPANY
                   and call["work_ref"] == work_ref and call["limit"] == 3 for call in calls)
        refs = context["references"]
        assert [r["ref"] for r in refs] == ["knowledge:" + explicit["id"], "knowledge:" + tail["id"]]
        assert [r["selection"] for r in refs] == ["EXPLICIT", "BOUNDED_RETRIEVAL"]
        assert "knowledge:" + foreign["id"] not in {r["ref"] for r in refs}
        assert context["limit"] == 3 and context["hydrated_bodies"] == 0
        assert all("body" not in item for item in refs)
        with pytest.raises(ValueError, match="knowledge query is too long"):
            real_list(query="x" * 201, company_id=COMPANY, work_ref=work_ref)
        with pytest.raises(ValueError, match="outside"):
            service.add_work_references(work_ref, [foreign["id"]], actor="ceo")
    with TenantContext.scope("other-tenant", company_id=COMPANY, ceo_id="ceo", role="test"):
        with pytest.raises((KeyError, ValueError)):
            KnowledgeService(database).context_for_work(work_ref, query=query)


def test_long_work_query_keeps_global_limit_and_skips_empty_segments(tmp_path, monkeypatch):
    database = seed(tmp_path / "bounded-long-knowledge.sqlite")
    add_team(database)
    work_ref = create_work(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = KnowledgeService(database)
        explicit = service.create_entry(title="Explicit", body="fixed",
            company_id=COMPANY, target_type="COMPANY", target_ref=COMPANY, created_by="ceo")
        service.add_work_references(work_ref, [explicit["id"]], actor="ceo")
        for index in range(7):
            service.create_entry(title=str(index), body="head tail",
                company_id=COMPANY, target_type="WORKSPACE", target_ref=WORKSPACE, created_by="ceo")
        real_list = service.list_entries
        calls = []
        def observed_list(**kwargs):
            assert kwargs["query"].strip(), "blank segments must not become unfiltered searches"
            calls.append(kwargs)
            return real_list(**kwargs)
        monkeypatch.setattr(service, "list_entries", observed_list)
        result = service.context_for_work(work_ref, query="head" + " " * 596 + "tail")
        assert len(calls) == 2
        assert result["references"][0]["ref"] == "knowledge:" + explicit["id"]
        assert len({r["ref"] for r in result["references"]}) == len(result["references"]) == 3


@pytest.mark.parametrize("field_size", [1600, 2000])
def test_complete_long_general_work_reaches_real_context_and_terminal_submit(tmp_path, field_size):
    database = seed(tmp_path / "full-general-work.sqlite")
    add_team(database)
    problem = "P" * (field_size - 12) + "PROBLEM-END!"
    expected = "E" * (field_size - 13) + "EXPECTED-END!"
    # Exact endpoint maxima, with distinct tails that a prefix-only repair loses.
    problem = problem.ljust(field_size, "!")
    expected = expected.ljust(field_size, "!")
    assert len(problem) == len(expected) == field_size
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        work = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE, problem=problem, expected_result=expected,
            constraints=[], references=[], idempotency_key="same-long-original-work")["work"]
    calls = []
    async def terminal_execution(payload):
        calls.append(payload)
        if payload["mode"] == "submit":
            assert problem in payload["prompt"] and expected in payload["prompt"]
            return {"task_ref": "task-full-long-general"}
        return {"output": json.dumps({"status": "ACCEPTED", "resultType": "general-business-result",
                "summary": "Full input", "problem": ""}), "task_status": "COMPLETED",
                "artifact_refs": [], "session_ref": "offline-long-general",
                "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}}}
    with TestClient(app(database, terminal_execution)) as client:
        route = f"/team-operating/works/{work['entity_id']}/execute?max_executions=1"
        response = client.post(route)
        assert response.status_code == 200, response.text
        assert [c["mode"] for c in calls] == ["submit", "run"]
        repeated = client.post(route)
        assert repeated.status_code == 200 and len(calls) == 2, repeated.text
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        from app.runtime import RuntimeFoundation
        foundation = RuntimeFoundation(database)
        assert len(foundation.list("WORK", company_id=COMPANY, workspace_id=WORKSPACE)) == 1
        cycle = foundation.get(work["data"]["cycleRef"])
        assert cycle["data"]["contract"]["problem"] == problem
        assert cycle["data"]["contract"]["expectedResult"] == expected
