"""W-14 writing-scoped fee reservations, entirely offline."""
import json
from datetime import datetime, timedelta

import pytest
from app.company_execution_policy import CompanyExecutionPolicy, PRICE, RESERVE_MICRO_CNY
from app.model_preferences import TenantModelPreferenceResolver
from app.runtime import RuntimeScopeError
from backend.tests.test_writing_selected_execution import ready
from backend.tests.test_writing_chapter_vertical import scope, COMPANY

KEY = 'model.writing-entry'


def writing_policy(tmp_path, monkeypatch, *, return_values=False, fail=False, reservations=1):
    import app.company_execution_policy as policy_module
    monkeypatch.setattr(policy_module, 'now', lambda: datetime.fromisoformat(PRICE['checked_at']) + timedelta(hours=1))
    values = ready(tmp_path, monkeypatch, fail=fail)
    db, _, entry, _, calls, workspace, *_ = values
    entry.execution_grant = None
    monkeypatch.setenv('CURIS_T018_FAKE_KEY', 'offline-only')
    db.save_model_gateway('writing-entry-test', 'T018 offline provider', 'deepseek', 'https://api.deepseek.com',
        credential_ref='env:CURIS_T018_FAKE_KEY', default_model='deepseek-flash')
    with db.connect() as con:
        con.execute("update official_models set provider_id='deepseek',default_model='deepseek-flash',supported_models=? where model_key=?",
            ('["deepseek-flash"]', KEY))
    policy = CompanyExecutionPolicy(db)
    with scope():
        TenantModelPreferenceResolver(db).set_current(KEY)
        view = policy.read(COMPANY)
        policy.save(COMPANY, request_id='t018-consent', expected_revision='', enabled=True, consent=True,
            workspace_ids=[workspace], model_keys=[KEY], budget_cny=str(reservations * RESERVE_MICRO_CNY / 1000000),
            valid_hours=1, preview_token=view['preview_token'])
    if return_values:
        from app.model_gateway import ModelGatewayAdapter
        original_metadata = ModelGatewayAdapter.with_model_metadata
        def metadata(adapter, **kwargs):
            adapter.gateway_resolver = db.get_model_gateway
            return original_metadata(adapter, **kwargs)
        monkeypatch.setattr(ModelGatewayAdapter, 'with_model_metadata', metadata)
        return values
    return db, policy, workspace, calls


def reserve(policy, workspace, attempt):
    grant = policy.current_grant(COMPANY, workspace, KEY)
    with policy.db.connect() as con:
        con.execute('begin immediate')
        return policy.reserve(con, {'company_id': COMPANY, 'attempt_id': attempt, 'message_id': 'msg-' + attempt,
            'context': {'workspace_id': workspace}}, {'grant': grant, 'model': {'model_key': KEY}})


def test_w14_unknown_reservation_survives_restart_and_blocks_overspend(tmp_path, monkeypatch):
    db, policy, workspace, calls = writing_policy(tmp_path, monkeypatch)
    with scope():
        reserve(policy, workspace, 'uncertain')
        policy.settle(COMPANY, 'uncertain', '', launched=True, status='UNKNOWN')
        cold = CompanyExecutionPolicy(db)
        totals = cold.read(COMPANY)['totals']
        assert totals == {'reserved_micro_cny': RESERVE_MICRO_CNY, 'estimated_micro_cny': 0, 'actual_paid': None}
        with pytest.raises(RuntimeScopeError, match='预算不足'):
            reserve(cold, workspace, 'retry-must-not-spend')
        assert cold.read(COMPANY)['totals'] == totals
        with db.connect() as con: assert len(cold.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_w14_proven_no_launch_settlement_is_idempotent(tmp_path, monkeypatch):
    db, policy, workspace, calls = writing_policy(tmp_path, monkeypatch)
    with scope():
        reserve(policy, workspace, 'preflight-failure')
        for _ in range(2): policy.settle(COMPANY, 'preflight-failure', '', launched=False, status='FAILED')
        assert CompanyExecutionPolicy(db).read(COMPANY)['totals'] == {
            'reserved_micro_cny': 0, 'estimated_micro_cny': 0, 'actual_paid': None}
        reserve(policy, workspace, 'safe-second-attempt')
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'settled')) == 1
            assert len(policy.rows(con, COMPANY, 'reserved')) == 2
    assert calls == []


def test_w14_reservation_tampering_is_detected_before_new_permission(tmp_path, monkeypatch):
    db, policy, workspace, calls = writing_policy(tmp_path, monkeypatch)
    with scope():
        reserve(policy, workspace, 'original')
        with db.connect() as con:
            event = con.execute("select event_id,payload from evolution_events where event_type='company.text_policy.reserved'").fetchone()
            payload = json.loads(event['payload']); payload['amount_micro_cny'] = 0
            con.execute('update evolution_events set payload=? where event_id=?', (json.dumps(payload), event['event_id']))
        state = CompanyExecutionPolicy(db).read(COMPANY)
        assert state['continuity']['status'] == 'MISMATCH'
        assert state['totals']['reserved_micro_cny'] is None
        with pytest.raises(RuntimeScopeError): reserve(policy, workspace, 'must-not-reuse-corrupt-budget')
    assert calls == []
