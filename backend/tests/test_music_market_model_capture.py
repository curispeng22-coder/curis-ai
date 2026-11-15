"""Normal model Tasks and host receipts, with zero network/process/provider effects."""
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import agent_browser_runtime
from app.music_market_evidence import MusicMarketEvidence
from app.result_store import ResultStore
from backend.tests.test_music_market_evidence import (scope, fixture, replace_data, unstarted_leader,
    recommendation_fixture, TENANT, COMPANY, BUSINESS)

URL = 'https://example.org/report'
RELEASE = {'releaseSha256': 'a' * 64}


def fake_browser(identity, stopped, launches, *, close_ok=True):
    assert not stopped()
    launches.append(identity)
    return SimpleNamespace(identity=identity, session='fixture', browser_id='fixture', tab='fixture',
        call=lambda args, resources: {'url': URL, 'result': {'text': 'Synthetic study: video 31 percent, 2023.'}},
        close=lambda: None, shutdown_evidence={'normal_browser_close': close_ok, 'proxy_closed': True,
            'held_process': {'direct_child': 'EXITED' if close_ok else 'UNKNOWN'}})


def capture_context(tmp_path):
    db, _, _, _ = fixture(tmp_path / 'capture.sqlite')
    task = ResultStore(db).create_task('Synthetic model capture', company_id=COMPANY, scope_type='BUSINESS', scope_ref=BUSINESS,
        work_ref='child', execution_ref='leader:worker:capture', employee_id='company-worker',
        capability_source='tenant_private', capability_type='model', capability_id='model.fixture')
    ResultStore(db).transition(task['task_id'], 'RUNNING', {})
    with db.connect() as con:
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('capture-binding',?,'company-worker','tenant_private','model','model.fixture')", (TENANT,))
        con.execute("update employee_instances set allowed_effect_classes_json='[\"read\"]' where id='company-worker'")
    replace_data(db, 'child', lambda d: d.update(followupContract={'marketEvidenceBrowser': {'hosts': ['example.org'], 'sourceUrl': URL}},
        responsibilityRouting={'status': 'EXECUTING', 'executions': {'leader:worker:capture': {'status': 'RUNNING', 'taskRef': task['task_id']}}}))
    context = {'type': 'model', 'id': 'model.fixture', 'source': 'tenant_private', 'company_id': COMPANY, 'work_ref': 'child',
        'task_id': task['task_id'], 'employee_id': 'company-worker', 'binding_id': 'capture-binding', 'execution_ref': 'leader:worker:capture'}
    return db, context


@pytest.mark.parametrize('failure', [None, 'close', 'revoked', 'scope', 'release'])
def test_model_host_capture_stays_in_original_task_and_never_reopens(tmp_path, monkeypatch, failure):
    with scope():
        db, context = capture_context(tmp_path)
        launches = []
        if failure != 'release':
            monkeypatch.setattr(agent_browser_runtime, 'agent_browser_release', lambda **kw: RELEASE)
        if failure == 'revoked':
            with db.connect() as con: con.execute("update employee_capability_bindings set enabled=0 where id='capture-binding'")
        if failure == 'scope': context['work_ref'] = 'root'
        monkeypatch.setattr(agent_browser_runtime, 'open_agent_browser_for_work', lambda identity, stopped, **kw:
            fake_browser(identity, stopped, launches, close_ok=failure != 'close'))
        service = MusicMarketEvidence(db)
        if failure == 'scope':
            assert service.capture_for_model_task(context) is None
        elif failure:
            with pytest.raises((ValueError, PermissionError)): service.capture_for_model_task(context)
        else:
            captured = service.capture_for_model_task(context)
            assert captured['identity']['task_id'] == context['task_id']
            assert len(captured['artifact_receipts']) == 1 and URL in captured['source_text']
            assert captured['browser_tool_calls'][-1]['shutdown']['normal_browser_close']
        if failure in {None, 'close'}:
            with pytest.raises(PermissionError, match='领取过'): service.capture_for_model_task(context)
            assert len(launches) == 1
        else: assert launches == []
        with db.connect() as con:
            assert con.execute('select count(*) from tasks where task_id=?', (context['task_id'],)).fetchone()[0] == 1
            assert con.execute('select count(*) from ai_usage_records where task_id=?', (context['task_id'],)).fetchone()[0] == 0


@pytest.mark.parametrize('close_ok', [True, False])
def test_normal_model_entry_capture_analysis_evidence_and_original_summary(tmp_path, monkeypatch, close_ok):
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.model_gateway import ModelGatewayAdapter
    from app.runtime import RuntimeFoundation
    from app.runtime_capability_context import RuntimeCapabilityContext
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        db.save_tenant_private_capability(tenant_id=TENANT, capability_type='model', capability_id='model.fixture',
            display_name='Synthetic normal API', metadata={'provider_type': 'ollama', 'base_url': 'http://127.0.0.1:11434', 'model_name': 'synthetic'})
        with db.connect() as con:
            con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('worker-model',?,'company-worker','tenant_private','model','model.fixture')", (TENANT,))
            con.execute("update employee_instances set allowed_effect_classes_json='[\"read\"]' where id in ('leader','company-worker')")
        monkeypatch.setattr(agent_browser_runtime, 'agent_browser_release', lambda **kw: RELEASE)
        MusicMarketEvidence(db).browser_scope('root', ['example.org'], URL)
    launches, calls = [], []
    monkeypatch.setattr(agent_browser_runtime, 'open_agent_browser_for_work', lambda identity, stopped, **kw: fake_browser(identity, stopped, launches, close_ok=close_ok))
    monkeypatch.setattr(IdentityMembership, '_authorize_test', lambda self, tenant_id, request_id:
        AuthorizedMembership('synthetic-owner', TENANT, COMPANY, 'ceo', 'owner', 'active', request_id))
    def execute(self, prompt, **kw):
        calls.append(prompt)
        context = RuntimeCapabilityContext.current()
        output = {'status': 'ACCEPTED', 'resultType': 'market-summary', 'summary': 'Synthetic analysis, not actual public evidence'}
        if '额外返回 delegations' in prompt:
            output['delegations'] = [{'assignmentRef': assignments[1]['entity_id'], 'problem': 'Research source', 'expectedResult': 'Reviewed evidence'}]
        elif context['employee_id'] == 'company-worker':
            assert URL in prompt and 'Synthetic study' in prompt and len(launches) == 1
        else:
            with scope(), db.connect() as con:
                evidence = MusicMarketEvidence(db).accepted(con, RuntimeFoundation(db).get('root'))
            output['recommendation'] = recommendation_fixture(evidence['inputs'])
        return {'output': json.dumps(output), 'status': 'success', 'model_name': 'synthetic', 'model_gateway_id': 'fixture',
            'provider_id': 'fixture', 'prompt_tokens': 5, 'completion_tokens': 3, 'total_tokens': 8, 'estimated_cost': 0, 'metering_status': 'confirmed'}
    monkeypatch.setattr(ModelGatewayAdapter, 'execute', execute)
    app = create_app(db.path)
    headers = {'X-Tenant-Id': TENANT, 'X-Ceo-Id': 'ceo'}
    prefix = '/api/workspace/runtime/foundation/team-operating'
    with TestClient(app) as client:
        response = client.post(prefix + '/works/root/execute', headers=headers)
        assert response.status_code == 200, response.text
        if not close_ok:
            assert response.json()['delegation_status'] == 'FAILED', response.text
            assert len(calls) == 1 and len(launches) == 1
            return
        assert response.json()['delegation_status'] == 'AWAITING_MARKET_EVIDENCE_ACCEPTANCE', response.text
        child_ref = response.json()['child_work_refs'][0]
        sources = client.get(prefix + f'/works/{child_ref}/market-evidence/source', headers=headers).json()['sources']
        assert len(sources) == 1
        preview = client.get(prefix + f'/works/{child_ref}/market-evidence/source', headers=headers,
            params={k: sources[0][k] for k in ('task_ref', 'artifact_ref')}).json()
        payload = {k: preview[k] for k in ('task_ref', 'artifact_ref', 'result_version', 'snapshot_sha256')}
        payload.update(request_id='normal-accept', reviewed=True, metrics=[{'label': 'video', 'value': '31', 'unit': 'percent',
            'period': '2023', 'population': 'synthetic', 'source_quote': 'video 31 percent, 2023'}], limitations='Synthetic fixture only')
        accepted = client.post(prefix + f'/works/{child_ref}/market-evidence/accept', headers=headers, json=payload)
        assert accepted.status_code == 200, accepted.text
        summary = client.post(prefix + '/works/root/execute', headers=headers)
        assert summary.status_code == 200 and summary.json()['delegation_status'] == 'ACCEPTED', summary.text
        assert client.post(prefix + '/works/root/execute', headers=headers).json()['summary_work_ref'] == summary.json()['summary_work_ref']
    assert len(calls) == 3 and len(launches) == 1
    with scope(), db.connect() as con:
        assert con.execute('select requested_capability_type from tasks where task_id=?', (preview['task_ref'],)).fetchone()[0] == 'model'
        assert len(MusicMarketEvidence(db).accepted(con, f.get('root'))['inputs']) == 1
