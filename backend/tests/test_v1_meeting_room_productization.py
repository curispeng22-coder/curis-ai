from __future__ import annotations

import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.meeting_router import build_meeting_router
from app.database import Database
from app.meeting_service import MeetingService
from app.result_store import ResultStore
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.foundation import RuntimeScopeError
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import (
    BUSINESS,
    COMPANY,
    EMPLOYEE,
    TENANT,
    WORKSPACE,
    add_team,
    seed,
)


def app(database: Database) -> FastAPI:
    value = FastAPI()

    @value.middleware("http")
    async def scope(request: Request, call_next):
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            return await call_next(request)

    value.include_router(build_meeting_router(database))
    return value


def packet() -> dict:
    fact = lambda value, provenance="UNK": {"value": value, "provenance": provenance}
    return {
        "decisionKey": "meeting-growth-choice",
        "complexity": "LOW_RISK",
        "event": "需要选择下一步客户反馈整理方式",
        "cannotDecideReason": "两种方案影响不同，需要CEO确认",
        "options": [
            {
                "optionId": "FOCUS",
                "label": "先聚焦高频问题",
                "impact": fact("优先形成一项可验证改进", "EST"),
                "risk": fact("低频问题会延后", "EST"),
                "cost": fact("当前没有可靠成本数据"),
            },
            {
                "optionId": "BROAD",
                "label": "同时整理全部问题",
                "impact": fact("覆盖面更广", "EST"),
                "risk": fact("首个结果可能更晚", "EST"),
                "cost": fact("当前没有可靠成本数据"),
            },
        ],
        "recommendation": {"optionId": "FOCUS", "provenance": "EST"},
        "recommendationReason": fact("推进员工根据当前会议信息做出的建议", "EST"),
        "ceoChoicePrompt": "选择下一步整理方式",
        "continuationPlan": "由业务负责人形成一项有证据的改进建议",
        "workContract": {
            "problem": "整理高频客户反馈",
            "expectedResult": "形成一项有证据的改进建议",
            "constraints": ["只使用已提供事实"],
        },
    }


def test_meeting_persists_canonical_people_decision_work_result_and_restart(tmp_path):
    path = tmp_path / "meeting.sqlite"
    database = seed(path)
    add_team(database)
    with database.connect() as connection:
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('employee-review', ?, ?, 'department', 'et_product_manager', '小研', '研究员工', 'idle')",
            (TENANT, COMPANY),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        evidence = RuntimeFoundation(database).create(
            "EVIDENCE", company_id=COMPANY, workspace_id=WORKSPACE,
            data={"summary": "客户反馈来源已登记"},
        )

    payload = {
        "title": "客户反馈改进会",
        "background": "确认下一项可验证改进",
        "business_id": BUSINESS,
        "workspace_id": WORKSPACE,
        "participant_refs": [EMPLOYEE, "employee-review"],
        "leader_ref": EMPLOYEE,
        "ceo_participation_mode": "DECISION_ONLY",
        "context_refs": [{"type": "EVIDENCE", "ref": evidence["entity_id"]}],
    }
    with TestClient(app(database)) as client:
        created = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings", json=payload,
        )
        assert created.status_code == 201, created.text
        meeting = created.json()
        meeting_id = meeting["meeting_id"]
        assert meeting["conversation_id"].startswith("conversation-")
        assert [item["id"] for item in meeting["participants_detail"]] == [EMPLOYEE, "employee-review"]
        message = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings/{meeting_id}/messages",
            json={"actor_type": "CEO", "actor_ref": "ceo", "text": "先看事实，再形成方案。"},
        )
        assert message.status_code == 200
        requested = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings/{meeting_id}/decision",
            json=packet(),
        )
        assert requested.status_code == 200, requested.text
        decision_ref = requested.json()["decision"]["entity_id"]
        assert requested.json()["decision"]["lifecycle_status"] == "WAITING_CEO"
        chosen = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings/{meeting_id}/decision/choose",
            json={"choice": "FOCUS", "reason": "先拿到一个真实结果"},
        )
        assert chosen.status_code == 200, chosen.text
        work_ref = chosen.json()["works"][0]["entity_id"]
        replay = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings/{meeting_id}/decision/choose",
            json={"choice": "FOCUS", "reason": "重复提交应读取同一决定"},
        )
        assert replay.status_code == 200
        assert [item["entity_id"] for item in replay.json()["works"]] == [work_ref]

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        store = ResultStore(database)
        task = store.create_task(
            "整理客户反馈", company_id=COMPANY, workspace_id=WORKSPACE, work_ref=work_ref,
            employee_id=EMPLOYEE,
        )
        task = store.transition(task["task_id"], "COMPLETED", {"output": "已形成一项有证据的改进建议"})
        artifact = store.list_artifacts(task_id=task["task_id"])[0]
        ResponsibilityRoutingRuntime(database).route(
            work_ref, signal="COMPLETED",
            result_refs=[f"task:{task['task_id']}"], artifact_refs=[artifact["artifact_id"]],
            evidence_refs=[evidence["entity_id"]],
        )
        synced = MeetingService(database).sync(COMPANY, meeting_id)
        assert synced["operating_state"] == "DISCUSSING"
        assert f"task:{task['task_id']}" in synced["result_refs"]
        assert any(item["kind"] == "RESULT_RETURNED" for item in synced["timeline"])
        closed = MeetingService(database).close(COMPANY, meeting_id)
        assert closed["status"] == "closed"

    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        recovered = MeetingService(reopened).get(COMPANY, meeting_id)
        assert recovered["conversation_id"] == meeting["conversation_id"]
        assert recovered["decision"]["entity_id"] == decision_ref
        assert recovered["decision"]["lifecycle_status"] == "APPLIED"
        assert [item["entity_id"] for item in recovered["works"]] == [work_ref]
        assert recovered["status"] == "closed"
        assert MeetingService(reopened).list(COMPANY)["history"][0]["meeting_id"] == meeting_id
        with reopened.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where entity_type='DECISION_PACKET'",
            ).fetchone()[0] == 1
            assert connection.execute(
                "select count(*) from runtime_entities where entity_type='WORK'",
            ).fetchone()[0] == 1
            assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_meeting_fails_closed_for_cross_company_participant_and_high_risk_layer_zero(tmp_path):
    database = seed(tmp_path / "meeting-scope.sqlite")
    add_team(database)
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values ('other-company', ?, 'ceo', '另一公司')",
            (TENANT,),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('outside-employee', ?, 'other-company', 'outside', 'et_product_manager', '外部员工', '员工', 'idle')",
            (TENANT,),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        with pytest.raises(RuntimeScopeError):
            service.create(
                company_id=COMPANY, business_id=BUSINESS, workspace_id=WORKSPACE,
                title="越权会议", background="", participant_refs=[EMPLOYEE, "outside-employee"],
                leader_ref=EMPLOYEE, ceo_participation_mode="JOIN", context_refs=[],
            )
        meeting = service.create(
            company_id=COMPANY, business_id=BUSINESS, workspace_id=WORKSPACE,
            title="高风险决定", background="", participant_refs=[EMPLOYEE], leader_ref=EMPLOYEE,
            ceo_participation_mode="JOIN", context_refs=[],
        )
        high_risk = packet() | {"decisionKey": "high-risk", "complexity": "HIGH_RISK"}
        requested = service.request_decision(COMPANY, meeting["meeting_id"], high_risk)
        assert requested["decision"]["data"]["layer0Actions"] == ["VIEW_OPTIONS", "DEFER"]
        with pytest.raises(ValueError, match="requires review"):
            service.choose_decision(COMPANY, meeting["meeting_id"], choice="FOCUS", reason="不能在Layer 0批准")
        service.review_decision(COMPANY, meeting["meeting_id"])
        chosen = service.choose_decision(COMPANY, meeting["meeting_id"], choice="FOCUS", reason="已查看完整方案")
        assert chosen["decision"]["lifecycle_status"] == "APPLIED"
