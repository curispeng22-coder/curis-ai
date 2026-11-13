"""Read-only ADR-0046 computer access projection for the conversation Composer.

No requested intent is accepted and no effective permission is ever claimed:
model executors are NOT_APPLICABLE, unbridged employees stay UNKNOWN/UNVERIFIED.
"""
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.conversation_router import build_conversation_router
from app.conversation_service import ConversationService
from backend.tests.test_v1_general_operating_contract import COMPANY, TENANT, EMPLOYEE
from backend.tests.test_employee_conversation import setup, scope, _bind_two_official_models

ACCESS_KEYS = {"slot", "state", "selectable", "requested_intent",
               "configured_state", "effective_state", "verification_state"}
MODEL_NOT_APPLICABLE = {
    "slot": "COMPUTER_ACCESS",
    "state": "MODEL_EXECUTOR_NOT_APPLICABLE",
    "selectable": False,
    "requested_intent": None,
    "configured_state": "NOT_APPLICABLE",
    "effective_state": "NOT_APPLICABLE",
    "verification_state": "NOT_APPLICABLE",
}
NO_BRIDGE = {
    "slot": "COMPUTER_ACCESS",
    "state": "NO_EXECUTION_BRIDGE",
    "selectable": False,
    "requested_intent": None,
    "configured_state": "UNKNOWN",
    "effective_state": "UNKNOWN",
    "verification_state": "UNVERIFIED",
}


def test_ceo_only_conversation_reports_model_not_applicable(tmp_path):
    db, _ = setup(tmp_path / "ceo-only.sqlite")
    with scope():
        access = ConversationService(db).computer_access(COMPANY)
    assert access == MODEL_NOT_APPLICABLE
    assert set(access) == ACCESS_KEYS


def test_unbridged_employee_reports_unknown_unverified(tmp_path):
    db, _ = setup(tmp_path / "unbridged.sqlite")
    with scope():
        access = ConversationService(db).computer_access(COMPANY, EMPLOYEE)
    assert access == NO_BRIDGE
    assert set(access) == ACCESS_KEYS


def test_bridged_employee_reports_model_not_applicable(tmp_path):
    db, _ = setup(tmp_path / "bridged.sqlite")
    _bind_two_official_models(db)
    with scope():
        access = ConversationService(db).computer_access(COMPANY, EMPLOYEE)
    assert access == MODEL_NOT_APPLICABLE
    assert set(access) == ACCESS_KEYS


def _client(db):
    app = FastAPI()

    @app.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo")):
            return await call_next(request)

    async def forbidden(task_id):
        raise AssertionError("read-only projection must not execute")

    app.include_router(build_conversation_router(db, forbidden))
    return TestClient(app)


def test_employee_conversation_payload_carries_read_only_access(tmp_path):
    db, _ = setup(tmp_path / "api-unbridged.sqlite")
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    with _client(db) as client:
        value = client.get(prefix, headers={"X-CEO": "ceo"}).json()
    assert value["computer_access"] == NO_BRIDGE
    assert value["execution_models"] == []

    db2, _ = setup(tmp_path / "api-bridged.sqlite")
    _bind_two_official_models(db2)
    with _client(db2) as client:
        value = client.get(prefix, headers={"X-CEO": "ceo"}).json()
    assert value["computer_access"] == MODEL_NOT_APPLICABLE
    assert {item["binding_id"] for item in value["execution_models"]} == {"binding-a", "binding-b"}
    # The picker payload shape is unchanged; access truth is a sibling field.
    assert set(value["execution_models"][0]) == {"binding_id", "source", "model_key", "label"}


def test_ceo_only_topic_payload_carries_model_not_applicable(tmp_path):
    db, _ = setup(tmp_path / "topic.sqlite")
    with scope():
        conversation_id = ConversationService(db).create(COMPANY, request_id="topic-1")["conversation_id"]
    with _client(db) as client:
        value = client.get(f"/api/workspace/v1/companies/{COMPANY}/conversations/{conversation_id}",
                           headers={"X-CEO": "ceo"}).json()
    assert value["employee"] is None
    assert value["computer_access"] == MODEL_NOT_APPLICABLE


def test_access_projection_respects_company_isolation(tmp_path):
    db, _ = setup(tmp_path / "isolation.sqlite")
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    with _client(db) as client:
        assert client.get(prefix, headers={"X-CEO": "other"}).status_code == 404
