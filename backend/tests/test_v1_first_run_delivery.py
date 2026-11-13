from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app


TENANT = "tenant-v1-first-run"
CEO = "ceo-v1-first-run"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}
PREFIX = "/api/workspace/runtime/foundation"


def _configure(monkeypatch, path) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    for key in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"):
        monkeypatch.setenv(key, str(path))


def _run(client: TestClient, *, confirmed: bool = True, headers=HEADERS, ceo=CEO) -> str:
    created = client.post(
        f"{PREFIX}/founding-runs",
        headers=headers,
        json={"owner_ref": ceo, "intent_ref": "intent:first-business"},
    )
    assert created.status_code == 201, created.text
    run_id = created.json()["entity_id"]
    if confirmed:
        for target, trigger in (
            ("INTENT_CAPTURED", "capture_intent"),
            ("CLARIFYING", "request_clarification"),
            ("PROPOSED", "propose_company"),
            ("CEO_CONFIRMED", "confirm_company"),
        ):
            moved = client.post(
                f"{PREFIX}/entities/{run_id}/transition",
                headers=headers,
                json={"target": target, "actor": "CEO", "trigger": trigger},
            )
            assert moved.status_code == 200, moved.text
    return run_id


def _payload(**overrides):
    payload = {
        "company_id": "company-v1-first-run",
        "ceo_id": CEO,
        "company_name": "第一家公司",
        "department_name": "业务部",
        "business_name": "客户成功业务",
        "goal": "在四周内完成第一批客户反馈闭环",
        "positioning": "服务首批真实客户",
        "workspace_name": "客户成功工作空间",
        "intent_summary": "建立一个持续处理客户反馈的业务",
        "recommendation_reason": "当前没有已验证的专业模板，从通用工作空间开始",
        "template_match_status": "NO_VERIFIED_MATCH",
        "blueprint": {"contractVersion": "generic-v1"},
    }
    payload.update(overrides)
    return payload


def _materialize(client: TestClient, run_id: str, **overrides):
    return client.post(
        f"{PREFIX}/founding-runs/{run_id}/materialize-first-general-workspace",
        headers=HEADERS,
        json=_payload(**overrides),
    )


def test_atomic_general_fallback_retry_restart_and_parent_path(tmp_path, monkeypatch):
    path = tmp_path / "first-run.sqlite"
    _configure(monkeypatch, path)
    with TestClient(create_app(str(path))) as client:
        run_id = _run(client)
        first = _materialize(client, run_id)
        assert first.status_code == 200, first.text
        payload = first.json()
        result = payload["creation_result"]
        assert payload["founding_run"]["lifecycle_status"] == "COMPANY_CREATED"
        assert payload["founding_run"]["first_business"]["workspace_id"] == result["workspace_id"]
        assert payload["assistant"]["company_id"] == "company-v1-first-run"
        assert payload["business"]["business_id"] == result["business_id"]
        assert payload["business"]["parentPath"]["department"]["id"] == result["department_id"]
        assert payload["business"]["workspaces"][0]["workspace_id"] == result["workspace_id"]
        assert payload["parent"]["parentPath"]["business"]["business_id"] == result["business_id"]
        assert result["template_match"]["status"] == "NO_VERIFIED_MATCH"
        retried = _materialize(client, run_id)
        assert retried.status_code == 200, retried.text
        assert retried.json()["creation_result"] == result

    with TestClient(create_app(str(path))) as restarted:
        recovered = _materialize(restarted, run_id)
        assert recovered.status_code == 200, recovered.text
        assert recovered.json()["creation_result"] == result
        resumed_run = restarted.get(f"{PREFIX}/founding-runs/{run_id}", headers=HEADERS)
        assert resumed_run.json()["first_business"]["workspace_id"] == result["workspace_id"]
        parent = restarted.get(
            f"{PREFIX}/workspaces/{result['workspace_id']}/parent-path", headers=HEADERS,
        )
        assert parent.status_code == 200
        assert parent.json()["parentPath"]["company"]["company_id"] == "company-v1-first-run"

    with Database(str(path)).connect() as connection:
        counts = {
            table: connection.execute(f"select count(*) from {table}").fetchone()[0]
            for table in (
                "companies", "department_instances", "canonical_businesses", "workspaces",
                "runtime_workspace_versions",
            )
        }
        assistant_count = connection.execute(
            "select count(*) from runtime_entities where entity_type='CEO_ASSISTANT'",
        ).fetchone()[0]
        workspace = connection.execute(
            "select blueprint_json, status, business_relation_status from workspaces",
        ).fetchone()
    assert counts == {
        "companies": 1,
        "department_instances": 3,
        "canonical_businesses": 1,
        "workspaces": 1,
        "runtime_workspace_versions": 1,
    }
    assert assistant_count == 1
    assert json.loads(workspace["blueprint_json"])["businessType"] == "GENERIC"
    assert tuple(workspace)[1:] == ("DRAFT", "RESOLVED")


def test_cancel_and_failed_validation_leave_no_partial_company_objects(tmp_path, monkeypatch):
    path = tmp_path / "first-run-failure.sqlite"
    _configure(monkeypatch, path)
    with TestClient(create_app(str(path))) as client:
        abandoned_id = _run(client, confirmed=False)
        abandoned = client.post(
            f"{PREFIX}/entities/{abandoned_id}/transition",
            headers=HEADERS,
            json={"target": "ABANDONED", "actor": "CEO", "trigger": "abandon"},
        )
        assert abandoned.status_code == 200
        cancelled = _materialize(client, abandoned_id)
        assert cancelled.status_code == 409

        failed_id = _run(client)
        failed = _materialize(client, failed_id, blueprint={"api_key": "must-not-persist"})
        assert failed.status_code == 422

    with Database(str(path)).connect() as connection:
        for table in ("companies", "department_instances", "canonical_businesses", "workspaces"):
            assert connection.execute(f"select count(*) from {table}").fetchone()[0] == 0
        failed_run = connection.execute(
            "select lifecycle_status, company_id from runtime_entities where entity_id=?",
            (failed_id,),
        ).fetchone()
        assert tuple(failed_run) == ("CEO_CONFIRMED", None)
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_fresh_company_normal_local_beta_catalog_and_both_package_workspaces(tmp_path, monkeypatch):
    path=tmp_path/'normal-local.sqlite';_configure(monkeypatch,path)
    monkeypatch.delenv('CURIS_DESKTOP_DATA_ROOT',raising=False)
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE',str(tmp_path/'packages'))
    company='ordinary-local-company';v1='/api/workspace/v1'
    ceo='selfuse-ceo';headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':ceo}
    monkeypatch.setenv('CURIS_IDENTITY_MODE','selfuse')
    with TestClient(create_app(str(path))) as client:
        run_id=_run(client,headers=headers,ceo=ceo)
        body={'company_id':company,'ceo_id':ceo,'name':'普通本地公司'}
        result=client.post(f'{PREFIX}/founding-runs/{run_id}/materialize-company',headers=headers,json=body)
        assert result.status_code==200,result.text
        assert client.post(f'{PREFIX}/founding-runs/{run_id}/materialize-company',headers=headers,json=body).status_code==200
        org=client.get(f'{PREFIX}/companies/{company}/organization',headers=headers).json()
        dept=org['departments'][0]['id']
        catalog=client.get(f'{v1}/companies/{company}/business-definitions',headers=headers)
        assert catalog.status_code==200,catalog.text
        definitions={d['package_id']:d for d in catalog.json()['definitions']}
        for package in ['com.curis.local.content-growth','com.curis.local.music']:
            assert definitions[package]['version']=='0.2.0'
            run=_run(client,confirmed=False,headers=headers,ceo=ceo)
            for target,trigger in [('INTENT_CAPTURED','capture_intent'),('CLARIFYING','request_clarification'),('PROPOSED','propose_company')]:
                move=client.post(f'{PREFIX}/entities/{run}/transition',headers=headers,json={'target':target,'actor':'CEO','trigger':trigger});assert move.status_code==200,move.text
            draft={'company_id':company,'package_id':package,'department_id':dept,'intent':'本地手工创作','business_name':package,'goal':'保存本地版本','positioning':'用户手工','workspace_name':'本地专业空间'}
            saved=client.put(f'{v1}/founding-runs/{run}/business-draft',headers=headers,json=draft)
            assert saved.status_code==200,saved.text
            proposal=saved.json()['data']['v1Proposal'];assert proposal['snapshot']['definition']['version']=='0.2.0'
            move=client.post(f'{PREFIX}/entities/{run}/transition',headers=headers,json={'target':'CEO_CONFIRMED','actor':'CEO','trigger':'confirm_company'});assert move.status_code==200,move.text
            command={'ceo_id':ceo,'business_name':draft['business_name'],'goal':draft['goal'],'positioning':draft['positioning'],'workspace_name':draft['workspace_name'],'intent_summary':draft['intent'],'package_id':package,'department_id':dept,'proposal_sha256':proposal['proposal_sha256']}
            route=f'{v1}/companies/{company}/founding-runs/{run}/business'
            created=client.post(route,headers=headers,json=command);assert created.status_code==200,created.text
            replay=client.post(route,headers=headers,json=command);assert replay.status_code==200,replay.text
            assert created.json()['creation_result']['workspace_id']==replay.json()['creation_result']['workspace_id']
    with Database(str(path)).connect() as con:
        assert con.execute('select count(*) from companies').fetchone()[0]==1
        assert con.execute('select count(*) from workspaces').fetchone()[0]==2
        assert con.execute("select count(*) from workspace_package_instances where package_version='0.2.0'").fetchone()[0]==2
