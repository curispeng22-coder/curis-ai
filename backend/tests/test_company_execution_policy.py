"""Fresh, sandboxed policy fixtures: HTTP is injected; no real provider acceptance."""
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from threading import Barrier

import pytest
from fastapi.testclient import TestClient
from app.company_execution_policy import CompanyExecutionPolicy, RESERVE_MICRO_CNY, PRICE
from app.model_preferences import TenantModelPreferenceResolver
from app.runtime import RuntimeScopeError
from backend.tests.test_cg_selected_execution import ready
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO

KEY = 'model.cg-test'
HEADERS = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}


def policy_ready(path, monkeypatch, fail=False):
    fixture = ready(path, monkeypatch, fail)
    db, app, entry = fixture[:3]
    entry.execution_grant = None
    from app.model_gateway import ModelGatewayAdapter
    original_metadata = ModelGatewayAdapter.with_model_metadata
    def resolved_metadata(adapter, **values):
        adapter.gateway_resolver = db.get_model_gateway
        resolved = original_metadata(adapter, **values)
        if not getattr(resolved.http_post, '_rc4_counted', False):
            original_post = resolved.http_post
            def numbered_post(*args, **kwargs):
                response = original_post(*args, **kwargs)
                response['choices'][0]['message']['content'] += f' 第{len(fixture[4])}轮建议。'
                return response
            numbered_post._rc4_counted = True
            resolved.http_post = numbered_post
        app.state.rc4_fixture_executor = resolved
        return resolved
    monkeypatch.setattr(ModelGatewayAdapter, 'with_model_metadata', resolved_metadata)
    monkeypatch.setenv('CURIS_RC4_FIXTURE_KEY', 'fixture-no-network')
    db.save_model_gateway('cg-test-gateway', 'Offline DeepSeek fixture', 'deepseek', 'https://api.deepseek.com',
                          credential_ref='env:CURIS_RC4_FIXTURE_KEY', default_model='deepseek-flash')
    with db.connect() as con:
        con.execute("update official_models set provider_id='deepseek',default_model='deepseek-flash',supported_models=? where model_key=?", ('["deepseek-flash"]', KEY))
    with scope():
        TenantModelPreferenceResolver(db).set_current(KEY)
    return fixture


def consent(policy, workspace, **overrides):
    current = policy.read(COMPANY)
    values = dict(request_id='consent-1', expected_revision=(current['policy'] or {}).get('revision', ''), enabled=True,
                  consent=True, workspace_ids=[workspace], model_keys=[KEY], budget_cny='0.1', valid_hours=1,
                  preview_token=current['preview_token'])
    values.update(overrides)
    return policy.save(COMPANY, **values)


def reserve(policy, workspace, attempt):
    with scope():
        grant = policy.current_grant(COMPANY, workspace, KEY)
        with policy.db.connect() as con:
            con.execute('begin immediate')
            return policy.reserve(con, {'company_id': COMPANY, 'attempt_id': attempt, 'message_id': 'message-' + attempt,
                'context': {'workspace_id': workspace}}, {'grant': grant, 'model': {'model_key': KEY}})


def test_explicit_consent_price_scope_replay_and_revoke(tmp_path, monkeypatch):
    db, app, entry, service, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        assert policy.read(COMPANY)['policy'] is None
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        with pytest.raises(ValueError): consent(policy, workspace, consent=False)
        with pytest.raises(RuntimeScopeError): consent(policy, 'foreign-workspace')
        with pytest.raises(ValueError): consent(policy, workspace, budget_cny='NaN')
        initial_preview = policy.read(COMPANY)["preview_token"]
        first = consent(policy, workspace)
        args = dict(request_id='consent-1', expected_revision='', enabled=True, consent=True, workspace_ids=[workspace],
                    model_keys=[KEY], budget_cny='0.1', valid_hours=1, preview_token=initial_preview)
        assert policy.save(COMPANY, **args)['policy'] == first['policy']
        with pytest.raises(ValueError): policy.save(COMPANY, **{**args, 'budget_cny': '1'})
        grant = reserve(policy, workspace, 'original')
        assert grant['budget_currency'] == 'CNY' and grant['max_cost_usd'] != grant['max_cost_cny']
        policy.settle(COMPANY, 'original', '', launched=True, status='UNKNOWN')
        assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['reserved_micro_cny'] == RESERVE_MICRO_CNY
        policy.save(COMPANY, request_id='revoke', expected_revision=first['policy']['revision'], enabled=False)
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        assert policy.read(COMPANY)['totals']['reserved_micro_cny'] == RESERVE_MICRO_CNY
    with scope(tenant_id='other'):
        with pytest.raises(RuntimeScopeError): policy.read(COMPANY)
    with scope(role='employee'):
        with pytest.raises(RuntimeScopeError): policy.save(COMPANY, request_id='illegal', expected_revision='', enabled=False)
    assert calls == []


def test_first_company_permission_guides_without_creating_authorization(tmp_path, monkeypatch):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        before = policy.read(COMPANY)
        assert before['continuity']['status'] == 'FRESH' and before['policy'] is None
        with pytest.raises(RuntimeScopeError) as error:
            policy.current_grant(COMPANY, workspace, KEY)
        assert str(error.value) == '尚未设置公司文字使用许可；请到公司设置明确同意本工作空间的文字外发与预算，原输入会保留。'
        assert policy.read(COMPANY) == before
        assert not anchor_file(policy).exists()
    assert calls == []


@pytest.mark.parametrize('status,old_policy', [
    ('MISSING', None), ('MISMATCH', None), ('UNVERIFIABLE', None),
    ('MISSING', {'revision': 'old'}), ('MISMATCH', {'revision': 'old'}),
    ('FRESH', {'revision': 'old'}), ('VALID', {'revision': 'old'}),
])
def test_unknown_or_old_permission_keeps_strong_rejection(tmp_path, monkeypatch, status, old_policy):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    monkeypatch.setattr(policy, 'continuity', lambda *_: {'status': status, 'needs_reconfirmation': True})
    monkeypatch.setattr(policy, 'latest', lambda *_: old_policy)
    with scope(), pytest.raises(RuntimeScopeError) as error:
        policy.current_grant(COMPANY, workspace, KEY)
    assert str(error.value) == '资料状态变化或许可无法核验，旧费用授权已失效；请到公司设置重新核对，原输入会保留。'
    assert calls == []


def test_concurrent_budget_and_restarts_do_not_reset_occupancy(tmp_path, monkeypatch):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope(): consent(policy, workspace, budget_cny=str(RESERVE_MICRO_CNY / 1000000))
    barrier = Barrier(2)
    def claim(number):
        barrier.wait()
        try: return reserve(policy, workspace, 'attempt-' + str(number))
        except RuntimeScopeError: return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, [1, 2]))
    assert sum(value is not None for value in results) == 1
    with scope():
        assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['reserved_micro_cny'] == RESERVE_MICRO_CNY
        active = next(value for value in results if value)
        attempt = active['grant_ref'].split(':', 1)[1]
        policy.settle(COMPANY, attempt, '', launched=False, status='FAILED')
        policy.settle(COMPANY, attempt, '', launched=False, status='FAILED')
        assert policy.read(COMPANY)['totals'] == {'reserved_micro_cny': 0, 'estimated_micro_cny': 0, 'actual_paid': None}
    assert calls == []


def test_destination_price_expiry_and_revision_invalidate_permission(tmp_path, monkeypatch):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace)
        with db.connect() as con: con.execute("update model_gateways set base_url='https://changed.invalid' where gateway_id='cg-test-gateway'")
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        with db.connect() as con: con.execute("update model_gateways set base_url='https://api.deepseek.com' where gateway_id='cg-test-gateway'")
        import app.company_execution_policy as module
        original = module.now()
        monkeypatch.setattr(module, 'now', lambda: original + timedelta(hours=2))
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        monkeypatch.setattr(module, 'now', lambda: original + timedelta(days=10))
        assert not policy.read(COMPANY)['models']
    assert calls == []


@pytest.mark.parametrize("outbound", [False, True])
def test_ordinary_company_reply_requires_proven_failure_to_retry_after_renewal(tmp_path, monkeypatch, outbound):
    import app.company_execution_policy as module
    from app.result_store import ResultStore

    clock = [datetime.fromisoformat(PRICE["checked_at"]) + timedelta(hours=1)]
    monkeypatch.setattr(module, "now", lambda: clock[0])
    db, app, _, _, calls, workspace, row, bound, _ = policy_ready(tmp_path, monkeypatch)
    service = app.state.writing_entry_service.conversations
    policy = CompanyExecutionPolicy(db)
    context = bound["context"]
    version = row["version"]["entity_id"]
    reference = {"reference_id": version, "version_ref": version, "workspace_id": workspace,
                 "kind": "CONTENT_VERSION", "purpose": "BACKGROUND", "locator": "原选段"}
    args = dict(body="原文和原引用", request_id="renewal-original", assignment_ref=context["assignment_ref"],
                conversation_id=bound["conversation_id"], references=[reference])
    employee = context["employee_ref"]
    with scope():
        original_revision = consent(policy, workspace)["policy"]["revision"]
        original, created = service.prepare(COMPANY, employee, **args)
        assert created
        assert service.conversation_metadata(COMPANY, employee)["execution_readiness"] == [
            {"assignment_ref": args["assignment_ref"], "status": "AVAILABLE", "company_text": True}]
        async def fail_at_dispatch(task_id):
            clock[0] += timedelta(hours=2)
            if outbound:
                service.events.record(correlation_id=task_id, event_type="conversation.outbound.claimed",
                                      payload={"attempt_id": original["attempt_id"]})
            with pytest.raises(RuntimeScopeError):
                policy.current_grant(COMPANY, workspace, KEY, attempt_id=original["attempt_id"])
            return ResultStore(db).transition(task_id, "FAILED")

        asyncio.run(service.execute(original, fail_at_dispatch))
        before = service.read_request(COMPANY, bound["conversation_id"], args["request_id"])
        first, = before["attempts"]
        assert first["status"] == ("UNKNOWN" if outbound else "FAILED")
        with pytest.raises(RuntimeScopeError):
            service.prepare(COMPANY, employee, **{**args, "request_id": "new-while-expired"})
        with pytest.raises(RuntimeScopeError):
            service.prepare(COMPANY, employee, **args, retry_no=1)
        assert service.read_request(COMPANY, bound["conversation_id"])["messages"] == before["messages"]
        old_totals = policy.read(COMPANY)["totals"]
        renewed_revision = consent(policy, workspace, request_id="renewed")["policy"]["revision"]
        assert renewed_revision != original_revision
        assert policy.read(COMPANY)["totals"] == old_totals
        if outbound:
            with pytest.raises(RuntimeScopeError):
                service.prepare(COMPANY, employee, **args, retry_no=1)
        else:
            with pytest.raises(ValueError):
                service.prepare(COMPANY, employee, **{**args, "body": "不同的原请求"}, retry_no=1)
            with pytest.raises(ValueError):
                service.prepare(COMPANY, employee, **{**args, "references": []}, retry_no=1)
            wrong_model = {"purpose": "CONVERSATION_REPLY", "scope": {"company_id": COMPANY, "workspace_id": workspace},
                           "model": {"source": "official", "model_key": KEY}, "binding_id": "different"}
            with pytest.raises(RuntimeScopeError):
                service.prepare(COMPANY, employee, **args, retry_no=1, execution_selection=wrong_model)
            barrier = Barrier(2)
            def retry():
                with scope():
                    barrier.wait(timeout=5)
                    return service.prepare(COMPANY, employee, **args, retry_no=1)
            with ThreadPoolExecutor(2) as pool:
                futures = [pool.submit(retry) for _ in range(2)]
                results = [future.result(timeout=15) for future in futures]
            assert sorted(created for _, created in results) == [False, True]
            new, _ = results[0]
            assert new == results[1][0] and new["attempt_id"] != original["attempt_id"]
            assert new["message_id"] == original["message_id"] and new["context"] == original["context"]
            assert new["execution_selection"] == {**original["execution_selection"], "grant": new["execution_selection"]["grant"]}
            assert new["execution_selection"]["grant"]["policy_revision"] == renewed_revision
            assert policy.read(COMPANY)["totals"]["reserved_micro_cny"] == old_totals["reserved_micro_cny"] + RESERVE_MICRO_CNY
            clock[0] += timedelta(hours=2)
            assert service.prepare(COMPANY, employee, **args, retry_no=1) == (new, False)
        after = service.read_request(COMPANY, bound["conversation_id"], args["request_id"])
        assert after["messages"] == before["messages"] and after["attempts"][0] == first
        with db.connect() as con:
            reservations = policy.rows(con, COMPANY, "reserved")
            assert len(reservations) == (1 if outbound else 2)
            assert reservations[0]["grant"] == original["execution_selection"]["grant"]
            assert len(policy.rows(con, COMPANY, "settled")) == (0 if outbound else 1)
            assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
    assert calls == []


def test_company_api_no_client_grant_or_foreign_policy(tmp_path, monkeypatch):
    db, app, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    path = f'/api/workspace/v1/companies/{COMPANY}/text-execution-policy'
    with TestClient(app) as client:
        view = client.get(path, headers=HEADERS); assert view.status_code == 200, view.text
        body = dict(request_id='api-consent', expected_revision='', enabled=True, consent=True, workspace_ids=[workspace],
                    model_keys=[KEY], budget_cny='0.1', valid_hours=1, preview_token=view.json()['preview_token'])
        assert client.put(path, headers=HEADERS, json={**body, 'effective_system_authorization': True}).status_code == 422
        saved = client.put(path, headers=HEADERS, json=body); assert saved.status_code == 200, saved.text
        assert client.put(path, headers=HEADERS, json=body).json() == saved.json()
        assert client.get(path, headers={**HEADERS, 'X-Tenant-Id': 'other'}).status_code in {401, 403, 404}
    assert calls == []


def anchor_file(policy):
    from pathlib import Path
    root, parts, name, _ = policy.anchor_location(COMPANY)
    return root.joinpath(*parts, name)


@pytest.mark.parametrize("mode", ["same_inode", "replace", "missing_anchor"])
def test_restored_or_missing_continuity_needs_new_explicit_future_budget(tmp_path, monkeypatch, mode):
    import sqlite3
    import os
    from pathlib import Path
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        preview = policy.read(COMPANY)["preview_token"]
        first = consent(policy, workspace, budget_cny=str(RESERVE_MICRO_CNY / 1000000))
        state = anchor_file(policy)
        snapshot = tmp_path / "own-before-reservation.sqlite"
        with sqlite3.connect(db.path) as current, sqlite3.connect(snapshot) as saved:
            current.backup(saved)
        reserve(policy, workspace, "before-restore")
        assert policy.read(COMPANY)["totals"]["reserved_micro_cny"] == RESERVE_MICRO_CNY
        inode = Path(db.path).stat().st_ino
        if mode == "same_inode":
            with sqlite3.connect(snapshot) as saved, sqlite3.connect(db.path) as current:
                saved.backup(current)
            assert Path(db.path).stat().st_ino == inode
        elif mode == "replace":
            os.replace(snapshot, db.path)
            assert Path(db.path).stat().st_ino != inode
        else:
            state.unlink()  # Exact synthetic state created by this test only.
        before = state.read_bytes() if state.exists() else None
        cold = CompanyExecutionPolicy(db)
        view = cold.read(COMPANY)
        assert view["continuity"]["needs_reconfirmation"] and view["continuity"]["history_incomplete"]
        assert view["totals"]["reserved_micro_cny"] is None and view["totals"]["estimated_micro_cny"] is None
        assert (state.read_bytes() if state.exists() else None) == before
        with pytest.raises(RuntimeScopeError): cold.current_grant(COMPANY, workspace, KEY)
        with pytest.raises(RuntimeScopeError):
            cold.save(COMPANY, request_id="consent-1", expected_revision="", enabled=True, consent=True,
                workspace_ids=[workspace], model_keys=[KEY], budget_cny=str(RESERVE_MICRO_CNY / 1000000),
                valid_hours=1, preview_token=preview)
        with pytest.raises(ValueError): consent(cold, workspace, request_id="future", history_acknowledged=False)
        renewed = consent(cold, workspace, request_id="future", history_acknowledged=True)
        assert renewed["policy"]["budget_epoch"] != first["policy"]["budget_epoch"]
        assert renewed["policy"]["history_incomplete"]
        reserve(cold, workspace, "after-new-explicit-consent")
        assert cold.read(COMPANY)["totals"]["reserved_micro_cny"] == RESERVE_MICRO_CNY
        assert calls == []


@pytest.mark.parametrize("fault", ["json", "symlink", "permissions", "hardlink", "directory_permissions", "directory_symlink", "scope"])
def test_bad_anchor_is_preserved_and_cannot_be_silently_repaired(tmp_path, monkeypatch, fault):
    import os
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace)
        state = anchor_file(policy)
        if fault == "json": state.write_text("broken")
        elif fault == "symlink":
            held = state.with_suffix(".held"); state.rename(held); state.symlink_to(held)
        elif fault == "permissions": state.chmod(0o644)
        elif fault == "hardlink": os.link(state, state.with_suffix(".held"))
        elif fault == "directory_symlink":
            held = state.parent.with_name(state.parent.name + "-held")
            state.parent.rename(held); state.parent.symlink_to(held)
        elif fault == "scope":
            value = json.loads(state.read_text()); value["scope"] = "other-scope"; state.write_text(json.dumps(value))
        else: state.parent.chmod(0o755)
        before = state.lstat()
        view = policy.read(COMPANY)
        assert view["continuity"]["status"] == "UNVERIFIABLE" and not view["continuity"]["can_confirm"]
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        with pytest.raises(RuntimeScopeError): consent(policy, workspace, request_id="no-repair", history_acknowledged=True)
        assert state.lstat().st_ino == before.st_ino
        assert calls == []


def test_anchor_write_failure_and_db_rollback_fail_closed(tmp_path, monkeypatch):
    import os
    import stat
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace)
        state = anchor_file(policy); before = state.read_bytes()
        original = os.fsync
        with monkeypatch.context() as patch:
            patch.setattr(os, "fsync", lambda fd: (_ for _ in ()).throw(OSError("synthetic file persistence failure")))
            with pytest.raises(RuntimeScopeError): reserve(policy, workspace, "before-publish-failure")
        assert state.read_bytes() == before
        assert policy.read(COMPANY)["totals"]["reserved_micro_cny"] == 0
        with monkeypatch.context() as patch:
            def fail_directory(fd):
                if stat.S_ISDIR(os.fstat(fd).st_mode): raise OSError("synthetic post-rename persistence failure")
                return original(fd)
            patch.setattr(os, "fsync", fail_directory)
            with pytest.raises(RuntimeScopeError): reserve(policy, workspace, "after-publish-failure")
        assert policy.read(COMPANY)["continuity"]["needs_reconfirmation"]
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        consent(policy, workspace, request_id="explicit-after-failure", history_acknowledged=True)
        grant = policy.current_grant(COMPANY, workspace, KEY)
        with pytest.raises(RuntimeError):
            with db.connect() as con:
                con.execute("begin immediate")
                policy.reserve(con, {"company_id": COMPANY, "attempt_id": "db-rollback", "message_id": "rollback-msg", "context": {"workspace_id": workspace}}, {"grant": grant, "model": {"model_key": KEY}})
                raise RuntimeError("synthetic DB transaction rollback after anchor publication")
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
        assert calls == []


def test_other_legitimate_reservations_do_not_invalidate_pending_grants(tmp_path, monkeypatch):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace, budget_cny="0.2")
        first = reserve(policy, workspace, "first-valid")
        second = reserve(policy, workspace, "second-valid")
        cold = CompanyExecutionPolicy(db)
        assert cold.current_grant(COMPANY, workspace, KEY, attempt_id="first-valid") == first
        assert cold.current_grant(COMPANY, workspace, KEY, attempt_id="second-valid") == second
        assert cold.read(COMPANY)["totals"]["reserved_micro_cny"] == 2 * RESERVE_MICRO_CNY
        assert calls == []


def test_profile_anchor_is_exact_private_and_wrong_profile_never_falls_back(tmp_path, monkeypatch):
    import sqlite3
    import stat
    from app.database import Database
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    root = tmp_path / 'own-desktop-profile'
    (root / 'data').mkdir(parents=True)
    target = root / 'data/curis.sqlite'
    with sqlite3.connect(db.path) as source, sqlite3.connect(target) as copy:
        source.backup(copy)
    monkeypatch.setenv('CURIS_DESKTOP_DATA_ROOT', str(root))
    policy = CompanyExecutionPolicy(Database(str(target)))
    with scope():
        assert policy.read(COMPANY)['continuity']['status'] == 'FRESH'
        assert not (root / 'recovery').exists(), 'metadata does not create authorization state'
        consent(policy, workspace)
        state = anchor_file(policy)
        assert state.parent == root / 'recovery/company-text-policy'
        assert stat.S_IMODE(state.stat().st_mode) == 0o600
        assert stat.S_IMODE(state.parent.stat().st_mode) == 0o700
        assert set(json.loads(state.read_text())) == {'version', 'scope', 'ledger'}
        foreign = CompanyExecutionPolicy(db)
        assert foreign.read(COMPANY)['continuity']['status'] == 'UNVERIFIABLE'
        with pytest.raises(RuntimeScopeError): consent(foreign, workspace, request_id='wrong-profile', history_acknowledged=True)
        assert calls == []


@pytest.mark.parametrize("with_codex_history", [False, True])
def test_acp_separate_explicit_grant_never_inherits_codex_counts(tmp_path, monkeypatch, with_codex_history):
    from app.tenant_context import TenantContext
    from app.result_store import ResultStore
    from test_employee_execution_identity import _seed, TENANT, COMPANY as CO, COMPANY_EMPLOYEE, BINDING
    from test_ai_capability_registry import _synthetic_acp_installation
    import app.ai_capability_registry as registry
    database, _, _ = _seed(tmp_path / "acp-policy.sqlite")
    _synthetic_acp_installation(tmp_path, monkeypatch)
    row, = registry.discover_local_agents()
    metadata, _ = registry.local_agent_registration({"local_agent_ref": row["discovery_ref"]}, row["capability_id"])
    database.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id="agent.codex", metadata={"kind": "codex-cli"})
    database.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id=row["capability_id"], metadata=metadata)
    with database.connect() as con:
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('acp-binding',?,?,'tenant_private','agent',?)", (TENANT,COMPANY_EMPLOYEE,row["capability_id"]))
    with TenantContext.scope(TENANT, company_id=CO, ceo_id="ceo-trust", role="ceo"):
        policy = CompanyExecutionPolicy(database); store = ResultStore(database)
        initial = policy.agent_readiness(CO)
        if with_codex_history:
            initial = policy.save_agent_allowance(CO, request_id="codex-grant", expected_revision="", enabled=True, consent=True, binding_refs=[BINDING])
            task = store.create_task("synthetic codex", company_id=CO, employee_id=COMPANY_EMPLOYEE, work_ref="old-codex-work")
            store.transition(task["task_id"], "RUNNING")
            policy.reserve_agent_call(CO, BINDING, task["task_id"], "old-codex-work", initial["revision"])
            initial = policy.agent_readiness(CO)
        old_ref = initial["authorization_ref"]
        with pytest.raises(RuntimeScopeError):
            policy.save_agent_allowance(CO, request_id="wrong-reuse", expected_revision=initial["revision"], enabled=True,
                consent=True, binding_refs=["acp-binding"], authorization_ref=old_ref)
        arguments = dict(request_id="new-acp", previous_authorization_ref=old_ref, expected_revision=initial["revision"], binding_refs=["acp-binding"], consent=True)
        grant = policy.new_agent_authorization(CO, **arguments)
        assert grant["authorization_ref"] != old_ref and grant["used_calls"] == 0
        assert grant["authorization_subject"]["agent_kind"] == "acp-stdio"
        assert grant["authorization"]["billing_basis"] == "AGENT_ACCOUNT_COST_UNVERIFIED"
        assert policy.new_agent_authorization(CO, **arguments)["authorization_ref"] == grant["authorization_ref"]
        with pytest.raises(RuntimeScopeError): policy.require_agent_execution(CO, BINDING)
        assert policy.require_agent_execution(CO, "acp-binding")["state"] == "AVAILABLE"
        task = store.create_task("synthetic acp", company_id=CO, employee_id=COMPANY_EMPLOYEE, work_ref="new-acp-work")
        store.transition(task["task_id"], "RUNNING")
        with pytest.raises(RuntimeScopeError): policy.reserve_agent_call(CO,"acp-binding",task["task_id"],"new-acp-work",grant["revision"],old_ref)
        policy.reserve_agent_call(CO,"acp-binding",task["task_id"],"new-acp-work",grant["revision"],grant["authorization_ref"])
        current = policy.agent_readiness(CO)
        assert current["used_calls"] == 1
        assert next(item for item in current["authorization_history"] if item["authorization_ref"] == old_ref)["used_calls"] == (1 if with_codex_history else 0)
        restarted = CompanyExecutionPolicy(type(database)(database.path))
        assert restarted.agent_readiness(CO)["used_calls"] == 1
        with pytest.raises(RuntimeScopeError): policy.reserve_agent_call(CO,"acp-binding",task["task_id"],"new-acp-work",grant["revision"],grant["authorization_ref"])
        with pytest.raises(RuntimeScopeError): policy.new_agent_authorization("other-company", **arguments)
        def reserve_parallel(number):
            with TenantContext.scope(TENANT, company_id=CO, ceo_id="ceo-trust", role="ceo"):
                work = "acp-parallel-" + str(number)
                child_task = store.create_task("synthetic",company_id=CO,employee_id=COMPANY_EMPLOYEE,work_ref=work)
                store.transition(child_task["task_id"],"RUNNING")
                try:
                    policy.reserve_agent_call(CO,"acp-binding",child_task["task_id"],work,grant["revision"],grant["authorization_ref"])
                    return True
                except RuntimeScopeError: return False
        with ThreadPoolExecutor(max_workers=4) as pool:
            assert sum(pool.map(reserve_parallel, range(4))) == 3
        assert restarted.agent_readiness(CO)["used_calls"] == 4
        definition = registry.ACP_INSTALLATIONS["deepseek_harness"]
        Path = __import__('pathlib').Path
        (Path(definition["application"])/definition["launcher"]).write_bytes(b"drift")
        with pytest.raises(RuntimeScopeError): policy.require_agent_execution(CO,"acp-binding")


def test_trial_two_reservations_survive_settlement_reconsent_and_rebuild(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        first = consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        assert first['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        for attempt in ('trial-one', 'trial-two'):
            grant = reserve(policy, workspace, attempt)
            assert grant['trial_authorization_ref'] == TRIAL_AUTHORIZATION
            policy.settle(COMPANY, attempt, '', launched=False, status='FAILED')
        assert policy.read(COMPANY)['totals']['reserved_micro_cny'] == 0
        policy.save(COMPANY, request_id='trial-off', expected_revision=first['policy']['revision'], enabled=False)
        # Omitting the opt-in on later saves cannot remove the original limits.
        renewed = consent(policy, workspace, request_id='trial-on')
        assert renewed['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        with pytest.raises(RuntimeScopeError, match='最多两次'):
            reserve(CompanyExecutionPolicy(db), workspace, 'trial-three')
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 2
    assert calls == []


@pytest.mark.parametrize('outcome', ['pending', 'unknown', 'estimated_success'])
def test_trial_unknown_actual_cost_blocks_new_requests_but_original_remains_readable(tmp_path, monkeypatch, outcome):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        original = reserve(policy, workspace, 'original-trial')
        if outcome == 'unknown':
            policy.settle(COMPANY, 'original-trial', '', launched=True, status='UNKNOWN')
        elif outcome == 'estimated_success':
            # Existing success receipts have a verified estimate but no actual-paid proof.
            with db.connect() as con:
                con.execute('begin immediate')
                policy.events.record_in_connection(con, correlation_id=COMPANY,
                    event_type='company.text_policy.settled', idempotency_key='synthetic-estimate',
                    payload={'attempt_id': 'original-trial', 'estimated_micro_cny': 20,
                             'currency': 'CNY', 'actual_paid': None,
                             'basis': 'VERIFIED_USAGE_AT_APPROVED_PRICE', 'price_version': original['price_version']})
                policy.publish_anchor(con, COMPANY)
            assert policy.read(COMPANY)['totals']['reserved_micro_cny'] == 0
        assert policy.current_grant(COMPANY, workspace, KEY, attempt_id='original-trial') == original
        consent(policy, workspace, request_id='trial-reconfirm')
        with pytest.raises(RuntimeScopeError, match='实际费用未知'):
            reserve(CompanyExecutionPolicy(db), workspace, 'must-not-launch')
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_trial_concurrent_claims_are_serialized_before_outbound(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope(): consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
    gate = Barrier(2)
    def claim(number):
        gate.wait(timeout=5)
        try:
            return reserve(policy, workspace, 'concurrent-trial-' + str(number))
        except RuntimeScopeError as error:
            assert '实际费用未知' in str(error)
            return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(claim, number) for number in (1, 2)]
        results = [future.result(timeout=10) for future in futures]
    assert sum(value is not None for value in results) == 1
    with scope(), db.connect() as con:
        assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_trial_budget_and_authorization_cannot_be_expanded(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        with pytest.raises(ValueError, match='0.10'):
            consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION, budget_cny='0.100001')
        with pytest.raises(ValueError, match='未知的本轮试用授权'):
            consent(policy, workspace, trial_authorization_ref='client-invented')
        assert policy.read(COMPANY)['policy'] is None
        consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        with pytest.raises(ValueError, match='0.10'):
            consent(policy, workspace, request_id='increase', budget_cny='1')
    assert calls == []


def test_ordinary_permission_has_no_trial_call_limit(tmp_path, monkeypatch):
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        saved = consent(policy, workspace)
        assert 'trial_authorization_ref' not in saved['policy']
        for number in range(3):
            attempt = 'ordinary-' + str(number)
            grant = reserve(policy, workspace, attempt)
            assert 'trial_authorization_ref' not in grant
            policy.settle(COMPANY, attempt, '', launched=False, status='FAILED')
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 3
    assert calls == []


def test_trial_cannot_adopt_old_calls(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace)
        reserve(policy, workspace, 'old-call')
        with pytest.raises(RuntimeScopeError, match='独立合成公司'):
            consent(policy, workspace, request_id='retrofit-trial', trial_authorization_ref=TRIAL_AUTHORIZATION)
    assert calls == []


def test_refreshed_price_remains_expiring_and_fails_closed(tmp_path, monkeypatch):
    from datetime import datetime
    import app.company_execution_policy as module
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace)
        monkeypatch.setattr(module, 'now', lambda: datetime.fromisoformat(PRICE['valid_until']))
        with pytest.raises(RuntimeScopeError, match='价格依据已过期'):
            policy.model_snapshot(KEY)
    assert calls == []


def test_trial_unknown_history_cannot_reset_but_can_revoke(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        first = consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        reserve(policy, workspace, 'retained-trial')
        anchor_file(policy).unlink()  # Only the anchor created in this synthetic fixture.
        with pytest.raises(RuntimeScopeError, match='本轮试用历史无法核验'):
            consent(policy, workspace, request_id='reset-trial', history_acknowledged=True)
        revoked = policy.save(COMPANY, request_id='revoke-broken-trial',
            expected_revision=first['policy']['revision'], enabled=False)
        assert revoked['policy']['enabled'] is False
        assert revoked['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_trial_validation_does_not_enter_agent_allowance_contract(tmp_path, monkeypatch):
    db, _, _, _, calls, _, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        # Agent validation must retain its own error rather than reference a text-trial variable.
        with pytest.raises(ValueError, match='许可请求不完整'):
            policy.save_agent_allowance(COMPANY, request_id='', expected_revision='',
                enabled=False, binding_refs=[])
        with db.connect() as con:
            assert policy.agent_rows(con, 'changed') == []
            assert policy.rows(con, COMPANY, 'changed') == []
    assert calls == []


def test_http_trial_mode_saves_reads_revokes_and_cannot_remove_limits(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION
    db, app, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    path = f'/api/workspace/v1/companies/{COMPANY}/text-execution-policy'
    with TestClient(app) as client:
        view = client.get(path, headers=HEADERS)
        assert view.status_code == 200, view.text
        payload = dict(request_id='visible-trial', expected_revision='', enabled=True, consent=True,
            workspace_ids=[workspace], model_keys=[KEY], budget_cny='0.1', valid_hours=1,
            preview_token=view.json()['preview_token'], authorization_mode='synthetic_trial')
        assert client.put(path, headers=HEADERS, json={**payload, 'authorization_mode': 'invented'}).status_code == 422
        assert client.put(path, headers=HEADERS, json={**payload, 'trial_authorization_ref': TRIAL_AUTHORIZATION}).status_code == 422
        assert client.put(path, headers=HEADERS, json={**payload, 'budget_cny': '0.100001'}).status_code == 409
        assert client.put(path, headers=HEADERS, json={**payload, 'consent': False}).status_code == 409
        saved = client.put(path, headers=HEADERS, json=payload)
        assert saved.status_code == 200, saved.text
        assert saved.json()['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        assert client.put(path, headers=HEADERS, json=payload).json() == saved.json()
        readback = client.get(path, headers=HEADERS)
        assert readback.json()['policy'] == saved.json()['policy']
        revoked = client.put(path, headers=HEADERS, json={'request_id': 'http-trial-off',
            'expected_revision': saved.json()['policy']['revision'], 'enabled': False})
        assert revoked.status_code == 200, revoked.text
        assert revoked.json()['policy']['enabled'] is False
        assert revoked.json()['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        view = client.get(path, headers=HEADERS).json()
        restored = client.put(path, headers=HEADERS, json={**payload, 'request_id': 'http-trial-on',
            'authorization_mode': 'standard', 'expected_revision': view['policy']['revision'],
            'preview_token': view['preview_token']})
        assert restored.status_code == 200, restored.text
        assert restored.json()['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
    with scope(), db.connect() as con:
        assert len(CompanyExecutionPolicy(db).rows(con, COMPANY, 'reserved')) == 0
        assert con.execute('select count(*) from tasks').fetchone()[0] == 0
    assert calls == []


def synthetic_settlement(policy, attempt, estimate):
    with policy.db.connect() as con:
        con.execute('begin immediate')
        policy.events.record_in_connection(con, correlation_id=COMPANY,
            event_type='company.text_policy.settled', idempotency_key='synthetic-settled:' + attempt,
            payload={'attempt_id': attempt, 'estimated_micro_cny': estimate, 'currency': 'CNY',
                     'actual_paid': None, 'basis': 'VERIFIED_USAGE_AT_APPROVED_PRICE'})
        policy.publish_anchor(con, COMPANY)


def test_continuous_explicit_upgrade_preserves_old_trial_history_and_estimates(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION, CONTINUOUS_TEST_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        old = consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        reserve(policy, workspace, 'first-real-shaped-fixture')
        synthetic_settlement(policy, 'first-real-shaped-fixture', 5392)
        with pytest.raises(RuntimeScopeError, match='实际费用未知'):
            reserve(policy, workspace, 'blocked-old')
        with pytest.raises(ValueError):
            consent(policy, workspace, request_id='unconfirmed', consent=False,
                    test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        updated = consent(policy, workspace, request_id='explicit-upgrade',
            test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        assert updated['policy']['budget_epoch'] == old['policy']['budget_epoch']
        assert updated['policy']['trial_authorization_ref'] == TRIAL_AUTHORIZATION
        assert updated['policy']['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
        assert updated['totals']['estimated_micro_cny'] == 5392
        for number in range(3):
            attempt = f'continuous-{number}'
            grant = reserve(policy, workspace, attempt)
            assert grant['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
            synthetic_settlement(policy, attempt, 100)
        cold = CompanyExecutionPolicy(db)
        assert cold.read(COMPANY)['totals']['estimated_micro_cny'] == 5692
        assert cold.read(COMPANY)['totals']['actual_paid'] is None
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 4
            assert policy.rows(con, COMPANY, 'changed')[0] == old['policy']
        # Omission cannot revert to ordinary permission or reset the old ledger.
        renewed = consent(policy, workspace, request_id='renewed', budget_cny='0.000001')
        assert renewed['policy']['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
        assert renewed['policy']['budget_epoch'] == old['policy']['budget_epoch']
        reserve(cold, workspace, 'past-reference')
    assert calls == []


def test_continuous_reference_is_not_a_ten_yuan_hard_stop(tmp_path, monkeypatch):
    from app.company_execution_policy import CONTINUOUS_TEST_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace, test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        # Synthetic ledger receipts, not actual paid calls.
        for number in range(10_000_000 // RESERVE_MICRO_CNY + 1):
            attempt = f'bounded-{number}'
            reserve(policy, workspace, attempt)
            synthetic_settlement(policy, attempt, RESERVE_MICRO_CNY)
        assert policy.read(COMPANY)['totals']['estimated_micro_cny'] > 10_000_000
        reserve(CompanyExecutionPolicy(db), workspace, 'after-ten')
    assert calls == []


@pytest.mark.parametrize('problem', ['unresolved', 'over-bound', 'negative'])
def test_continuous_stops_unresolved_or_abnormal_chain(tmp_path, monkeypatch, problem):
    from app.company_execution_policy import CONTINUOUS_TEST_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace, test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        original = reserve(policy, workspace, 'affected')
        if problem != 'unresolved':
            synthetic_settlement(policy, 'affected', RESERVE_MICRO_CNY + 1 if problem == 'over-bound' else -1)
        with pytest.raises(RuntimeScopeError): reserve(policy, workspace, 'no-retry')
        assert policy.current_grant(COMPANY, workspace, KEY, attempt_id='affected') == original
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_http_continuous_upgrade_is_explicit_idempotent_and_keeps_scope(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION, CONTINUOUS_TEST_AUTHORIZATION
    db, app, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    with scope():
        policy = CompanyExecutionPolicy(db)
        old = consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        reserve(policy, workspace, 'original-http')
        synthetic_settlement(policy, 'original-http', 5392)
    path = f'/api/workspace/v1/companies/{COMPANY}/text-execution-policy'
    with TestClient(app) as client:
        view = client.get(path, headers=HEADERS).json()
        payload = dict(request_id='explicit-continuous-http', expected_revision=view['policy']['revision'],
            enabled=True, consent=True, workspace_ids=[workspace], model_keys=[KEY], budget_cny='10',
            valid_hours=1, preview_token=view['preview_token'], authorization_mode='synthetic_continuous')
        assert client.put(path, headers=HEADERS, json={**payload, 'consent': False}).status_code == 409
        assert client.put(path, headers=HEADERS, json={**payload, 'expected_revision': 'stale'}).status_code == 409
        assert client.put(path, headers=HEADERS, json={**payload, 'workspace_ids': ['foreign']}).status_code == 403
        saved = client.put(path, headers=HEADERS, json=payload)
        assert saved.status_code == 200, saved.text
        assert saved.json()['policy']['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
        assert saved.json()['policy']['budget_epoch'] == old['policy']['budget_epoch']
        assert saved.json()['totals']['estimated_micro_cny'] == 5392
        assert client.put(path, headers=HEADERS, json=payload).json() == saved.json()
        revoked = client.put(path, headers=HEADERS, json={'request_id': 'continuous-off',
            'expected_revision': saved.json()['policy']['revision'], 'enabled': False})
        assert revoked.status_code == 200, revoked.text
        assert revoked.json()['policy']['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
    with scope():
        with pytest.raises(RuntimeScopeError): policy.current_grant(COMPANY, workspace, KEY)
    assert calls == []


def test_continuous_concurrent_reservations_admit_only_one_unresolved_chain(tmp_path, monkeypatch):
    from app.company_execution_policy import CONTINUOUS_TEST_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        consent(policy, workspace, test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
    gate = Barrier(2)
    def claim(number):
        gate.wait()
        try:
            reserve(CompanyExecutionPolicy(db), workspace, f'parallel-{number}')
            return 'reserved'
        except RuntimeScopeError:
            return 'blocked'
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, range(2)))
    assert sorted(results) == ['blocked', 'reserved']
    with scope(), db.connect() as con:
        assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_continuous_broken_history_cannot_reset_but_can_revoke(tmp_path, monkeypatch):
    from app.company_execution_policy import CONTINUOUS_TEST_AUTHORIZATION
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        first = consent(policy, workspace, test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        reserve(policy, workspace, 'retained-continuous')
        anchor_file(policy).unlink()  # Synthetic fixture only.
        with pytest.raises(RuntimeScopeError, match='验收历史无法核验'):
            consent(policy, workspace, request_id='cannot-reset', history_acknowledged=True)
        revoked = policy.save(COMPANY, request_id='revoke-continuous',
            expected_revision=first['policy']['revision'], enabled=False)
        assert revoked['policy']['test_authorization_ref'] == CONTINUOUS_TEST_AUTHORIZATION
        assert revoked['policy']['budget_epoch'] == first['policy']['budget_epoch']
        assert revoked['policy']['enabled'] is False
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []


def test_explicit_continuous_workspace_extension_preserves_first_consumption(tmp_path, monkeypatch):
    from app.company_execution_policy import TRIAL_AUTHORIZATION, CONTINUOUS_TEST_AUTHORIZATION
    from app.workspace_package_runtime import WorkspacePackageRuntime
    from app.music_entry_service import ASSETS
    db, _, _, _, calls, workspace, *_ = policy_ready(tmp_path, monkeypatch)
    policy = CompanyExecutionPolicy(db)
    with scope():
        first = consent(policy, workspace, trial_authorization_ref=TRIAL_AUTHORIZATION)
        reserve(policy, workspace, 'first-before-extension')
        synthetic_settlement(policy, 'first-before-extension', 5392)
        installed = WorkspacePackageRuntime(db, tmp_path / 'music-store').install(ASSETS / 'music', COMPANY,
            department_id='cg-dept', business_id='continuous-music', business_name='合成音乐验证')
        music = installed['instance']['workspace_id']
        saved = consent(policy, workspace, request_id='explicit-workspace-extension',
            workspace_ids=[workspace, music], test_authorization_ref=CONTINUOUS_TEST_AUTHORIZATION, budget_cny='10')
        assert saved['policy']['budget_epoch'] == first['policy']['budget_epoch']
        assert saved['totals']['estimated_micro_cny'] == 5392
        assert policy.current_grant(COMPANY, music, KEY)['workspace_id'] == music
        with pytest.raises(RuntimeScopeError):
            consent(policy, workspace, request_id='foreign-space', workspace_ids=[workspace, 'foreign'], budget_cny='10')
        with db.connect() as con:
            assert len(policy.rows(con, COMPANY, 'reserved')) == 1
    assert calls == []
