"""真实系统时钟的公司许可回归；只登记合成元数据，不调用网关。"""
from datetime import datetime, timedelta, timezone

import pytest

from app import company_execution_policy as module
from app.runtime import RuntimeScopeError
from backend.tests.test_position_authorization import writing_model_position, scope, COMPANY


def test_shipped_expired_price_saves_pending_without_paid_execution(tmp_path):
    assert datetime.now(timezone.utc) >= datetime.fromisoformat(module.PRICE['valid_until'])
    db, _, _, key, workspace = writing_model_position(tmp_path)
    with scope():
        policy = module.CompanyExecutionPolicy(db)
        view = policy.read(COMPANY)
        assert view['price_status'] == 'VERIFICATION_REQUIRED'
        assert key in [m['model_key'] for m in view['models']]
        assert view['policy']['execution_state'] == 'AWAITING_PRICE_VERIFICATION'
        assert view['policy']['price_notice'] == view['price_notice']
        assert view['policy']['models'][0]['price'] == module.PRICE
        with pytest.raises(RuntimeScopeError, match='价格待核实'):
            policy.current_grant(COMPANY, workspace, key)
        with db.connect() as con:
            assert con.execute('select count(*) from tasks').fetchone()[0] == 0
            assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 0
            assert not policy.rows(con, COMPANY, 'reserved')
        assert view['totals']['actual_paid'] is None


def test_price_refresh_requires_new_explicit_consent(tmp_path, monkeypatch):
    db, _, _, key, workspace = writing_model_position(tmp_path)
    with scope():
        policy = module.CompanyExecutionPolicy(db)
        old = policy.read(COMPANY)
        real = datetime.now(timezone.utc)
        # 合成新价格证据测试恢复流程；不修改时钟，不宣称重新核价。
        monkeypatch.setitem(module.PRICE, 'checked_at', (real - timedelta(minutes=1)).isoformat())
        monkeypatch.setitem(module.PRICE, 'valid_until', (real + timedelta(days=7)).isoformat())
        with pytest.raises(RuntimeScopeError, match='价格待核实'):
            policy.current_grant(COMPANY, workspace, key)
        current = policy.read(COMPANY)
        args = dict(request_id='verified-price-consent', expected_revision=old['policy']['revision'],
                    enabled=True, consent=True, workspace_ids=[workspace], model_keys=[key],
                    budget_cny='0.1', valid_hours=1)
        with pytest.raises(ValueError, match='重新核对'):
            policy.save(COMPANY, **args, preview_token=old['preview_token'])
        policy.save(COMPANY, **args, preview_token=current['preview_token'])
        assert policy.current_grant(COMPANY, workspace, key)['price_cny'] == module.PRICE
        # 授权后证据再过期：仍然拒绝执行，不能继承已保存的有效状态。
        monkeypatch.setitem(module.PRICE, 'valid_until', (real - timedelta(seconds=1)).isoformat())
        with pytest.raises(RuntimeScopeError, match='价格依据已过期'):
            policy.current_grant(COMPANY, workspace, key)


@pytest.mark.parametrize('change', ['future', 'malformed', 'naive'])
def test_uncertain_price_time_saves_pending_and_blocks_execution(tmp_path, monkeypatch, change):
    real = datetime.now(timezone.utc)
    value = {'future': (real + timedelta(days=1)).isoformat(), 'malformed': 'unknown',
             'naive': real.replace(tzinfo=None).isoformat()}[change]
    monkeypatch.setitem(module.PRICE, 'checked_at', value)
    db, _, _, key, workspace = writing_model_position(tmp_path)
    with scope():
        policy = module.CompanyExecutionPolicy(db)
        assert policy.read(COMPANY)['policy']['price_status'] == 'VERIFICATION_REQUIRED'
        with pytest.raises(RuntimeScopeError, match='价格待核实'):
            policy.current_grant(COMPANY, workspace, key)


def test_pending_permission_still_rejects_foreign_scope_and_revocation(tmp_path):
    db, _, _, key, workspace = writing_model_position(tmp_path)
    policy = module.CompanyExecutionPolicy(db)
    with scope(tenant_id='foreign'), pytest.raises((ValueError, RuntimeScopeError)):
        policy.current_grant(COMPANY, workspace, key)
    with scope():
        current = policy.read(COMPANY)
        policy.save(COMPANY, request_id='revoke-pending', expected_revision=current['policy']['revision'], enabled=False)
        with pytest.raises(RuntimeScopeError):
            policy.current_grant(COMPANY, workspace, key)


@pytest.mark.parametrize('overrides', [
    {'consent': False}, {'preview_token': 'stale-preview'}, {'workspace_ids': ['foreign']},
    {'model_keys': ['unapproved-model']}, {'budget_cny': 'NaN'}, {'valid_hours': 169},
])
def test_pending_price_does_not_bypass_consent_scope_budget_or_duration(tmp_path, overrides):
    db, _, _, key, workspace = writing_model_position(tmp_path)
    with scope():
        policy = module.CompanyExecutionPolicy(db)
        before = policy.read(COMPANY)
        values = dict(request_id='invalid-renewal', expected_revision=before['policy']['revision'], enabled=True,
                      consent=True, workspace_ids=[workspace], model_keys=[key], budget_cny='0.1', valid_hours=1,
                      preview_token=before['preview_token'])
        values.update(overrides)
        with pytest.raises((ValueError, RuntimeScopeError)):
            policy.save(COMPANY, **values)
        assert policy.read(COMPANY)['policy'] == before['policy']
