"""Actual manual operating graph, source/version/permission and compatibility evidence."""
import copy
import hashlib
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pytest
from app.music_service import MusicService
from app.runtime.music import MusicConflict, MusicRuntime, digest
from app.runtime import RuntimeScopeError
from app.music_media_service import MusicMediaService, APPROVED_ROOT, OPERATING_ROOT
from app.tenant_context import TenantContext
from backend.tests.test_music_canonical_entry import setup, audio, choose, master, basis, data
from backend.tests.test_writing_chapter_vertical import scope, COMPANY

PERIOD = {'start': '2026-10-01', 'end': '2026-10-02', 'timezone': 'Asia/Shanghai'}
SOURCE = {'label': '人工来源说明', 'locator': 'local:original-note-1', 'note': '用户提供的原始观察说明；未联网核验', 'captured_at': '2026-10-05T01:00:00+00:00'}
METRIC = {'metric': 'plays', 'definition': '指定作品在该期间的记录次数', 'unit': '次', 'value': 0, 'account': None, 'currency': None, 'coverage': '单作品手工记录', 'method': 'MANUAL', 'period': PERIOD}

def op(s, w, action, d, key, expected=''):
    return s.operating_command(COMPANY, w, action, request_id=key, expected_ref=expected, data=d)

def chain(s, w):
    a = op(s, w, 'save-scope', {'title': '观察范围', 'body': '人工市场依据', 'platform': '用户指定平台', 'keywords': '用户创作兴趣', 'period': PERIOD}, 'scope')['record']
    b = op(s, w, 'save-snapshot', {'title': '原始观察', 'body': '保存人工原数据', 'scope_ref': a['entity_id'], 'source': SOURCE, 'metrics': [METRIC]}, 'snapshot')['record']
    c = op(s, w, 'save-reference', {'title': '参考依据', 'body': '用户的结构判断，效果未验证', 'scope_ref': a['entity_id'], 'snapshot_ref': b['entity_id'], 'purpose': 'PATTERN', 'locator': '原记录的节奏说明', 'material_available': False}, 'reference')['record']
    d = op(s, w, 'save-direction', {'title': '创作方向', 'body': '基于明确原参考的意图', 'scope_ref': a['entity_id'], 'reference_refs': [c['entity_id']], 'learning_ref': '', 'confirmed': True}, 'direction')['record']
    return a, b, c, d

def song_payload(direction, title='明确第一首'):
    return {**data(), 'title': title, 'direction_ref': direction['entity_id'], 'confirmed': True, 'historical': False}

def completed(s, w, direction):
    row = op(s, w, 'create-song', song_payload(direction), 'song-creation-1')
    row = master(s, w, choose(s, w, audio(s, w, row)))
    row = s.command(COMPANY, w, row['song']['entity_id'], 'prepare-release', request_id='package-1', expected=basis(row), data={'master_ref': row['master']['entity_id']})
    return row

def observation(scope_row, song, value=0):
    return {'title': '作品原观察', 'body': '人工提供，未发布，未联网核验', 'scope_ref': scope_row['entity_id'], 'song_ref': song['song']['entity_id'], 'master_ref': song['master']['entity_id'], 'release_ref': song['releases'][0]['entity_id'], 'platform': '用户指定平台', **METRIC, 'value': value, 'source': SOURCE}

def test_full_manual_graph_and_historical_learning_next_song(tmp_path):
    db, _, w, s = setup(tmp_path)
    with scope():
        a,b,c,d = chain(s,w); song = completed(s,w,d)
        obs = op(s,w,'save-observation',observation(a,song), 'observation')['record']
        report = op(s,w,'create-report',{'title':'原周期报告','body':'事实整理，不声称因果','selection':{'scope_ref':a['entity_id'],'song_ref':'','period':'all'}},'report')['record']
        report = op(s,w,'confirm-report',{'report_ref':report['entity_id'],'confirmed':True},'confirm',report['entity_id'])['record']
        ld = {'title':'有限经验','body':'用户的初步判断','scope_ref':a['entity_id'],'report_ref':report['entity_id'],'counterexample':'其他平台与样本不足不能泛化','applicability':'仅原平台原作品原期间','accepted':True}
        learning = op(s,w,'save-learning',ld,'learning')['record']
        changed = op(s,w,'save-observation',observation(a,song,1),'observation-v2',obs['entity_id'])['record']
        assert changed['data']['identity_ref'] == obs['entity_id']
        old = s.operating_content(COMPANY,w,report['entity_id'])
        assert old['record']['data']['rows'][0]['data']['value'] == 0 and not old['report_current']
        with pytest.raises(MusicConflict): op(s,w,'confirm-report',{'report_ref':report['entity_id'],'confirmed':True},'lateconfirm',report['entity_id'])
        adoption = {'learning_ref': learning['entity_id'],'title':'下一首方向','body':'明确采用原版限定经验','confirmed':True,'historical':False}
        with pytest.raises(MusicConflict): op(s,w,'use-learning',adoption,'adopt-current')
        nxt = op(s,w,'use-learning',{**adoption,'historical':True},'adopt-old')['record']
        assert '反例与限制' in nxt['data']['body'] and '待验证' in nxt['data']['body']
        assert nxt['data']['learning_ref'] == learning['entity_id']
        second = op(s,w,'create-song',{**song_payload(nxt,'下一首'),'historical':True},'next-intent-1')
        repeat = op(s,w,'create-song',{**song_payload(nxt,'下一首'),'historical':True},'next-intent-1')
        assert second['song']['entity_id'] == repeat['song']['entity_id'] != song['song']['entity_id']
        assert learning['data']['validation'] == 'UNVERIFIED'
        assert s.operating_collection(COMPANY,w)['records']
        assert MusicService(db,media=MusicMediaService(db,root=OPERATING_ROOT)).operating_content(COMPANY,w,report['entity_id'])['record']==old['record']
    with db.connect() as con:
        assert con.execute('select count(*) from tasks').fetchone()[0] == 0
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 0
        assert con.execute('select count(*) from workspace_package_objects').fetchone()[0] == 0


def test_same_direction_explicit_two_songs_and_concurrent_one_intent(tmp_path):
    db,_,w,s=setup(tmp_path)
    with scope(): _,_,_,direction=chain(s,w)
    def create_once(_):
        with scope(): return op(s,w,'create-song',song_payload(direction),'same-explicit-intent')['song']['entity_id']
    with ThreadPoolExecutor(max_workers=4) as pool: ids=list(pool.map(create_once,range(4)))
    assert len(set(ids))==1
    with scope():
        second=op(s,w,'create-song',song_payload(direction,'明确第二首'),'different-explicit-intent')
        assert second['song']['entity_id']!=ids[0]
        with pytest.raises(MusicConflict):op(s,w,'create-song',song_payload(direction,'改写原请求'),'same-explicit-intent')


def test_scope_version_cas_source_tamper_and_foreign_basis(tmp_path):
    db,runtime,w,s=setup(tmp_path)
    with scope():
        a,b,c,d=chain(s,w)
        payload={'title':'新版范围','body':'变更关键词','platform':'用户指定平台','keywords':'另一范围','period':PERIOD}
        newer=op(s,w,'save-scope',payload,'scope2',a['entity_id'])['record']
        with pytest.raises(MusicConflict):op(s,w,'save-scope',payload,'scope3',a['entity_id'])
        assert s.operating_content(COMPANY,w,c['entity_id'])['record']['data']['snapshot_ref']==b['entity_id']
        assert b['data']['scope_ref']==a['entity_id']!=newer['entity_id']
        with pytest.raises(RuntimeScopeError):op(s,w,'save-reference',{'title':'错范围','body':'不应保存','scope_ref':newer['entity_id'],'snapshot_ref':b['entity_id'],'purpose':'PATTERN','locator':'原记录','material_available':False},'bad')
        with pytest.raises(RuntimeScopeError):s.operating_content('foreign-company',w,a['entity_id'])
    with TenantContext.scope(tenant_id='foreign-tenant',company_id=COMPANY,ceo_id='other',role='owner'), pytest.raises((RuntimeScopeError,PermissionError,ValueError)):
        s.operating_content(COMPANY,w,a['entity_id'])
    with db.connect() as con:
        value=copy.deepcopy(b['data']);value['source']['note']='tampered'
        con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(value),b['entity_id']))
    with scope(),pytest.raises(ValueError):s.operating_content(COMPANY,w,c['entity_id'])


def test_unknown_zero_and_foreign_master_preserved(tmp_path):
    _,_,w,s=setup(tmp_path)
    with scope():
        a,b,c,d=chain(s,w);song=completed(s,w,d)
        known=op(s,w,'save-observation',observation(a,song,0),'zero')['record'];unknown=op(s,w,'save-observation',observation(a,song,None),'unknown')['record']
        assert known['data']['value']==0 and unknown['data']['value'] is None
        another=op(s,w,'create-song',song_payload(d,'另一首'),'another')
        with pytest.raises(RuntimeScopeError):op(s,w,'save-observation',{**observation(a,song),'song_ref':another['song']['entity_id']},'badmaster')
        with pytest.raises(ValueError):op(s,w,'save-observation',{**observation(a,song),'unit':''},'nounit')
        with pytest.raises(ValueError):op(s,w,'save-observation',{**observation(a,song),'source':{**SOURCE,'locator':''}},'nosource')
        with pytest.raises(ValueError):op(s,w,'save-observation',{**observation(a,song),'verification':'VERIFIED'},'upgrade')
        assert known['data']['verification']=='UNVERIFIED'


def test_exact_legacy_package_reader_commands_bytes_and_receipts(tmp_path):
    db,runtime,_,s=setup(tmp_path)
    old=tmp_path/'old-package';pre=Path('artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-001/preimages/backend/app/bundled_workspace_packages/music')
    shutil.copytree(pre,old)
    with scope():
        installed=runtime.install(old,COMPANY,department_id='cg-dept',business_id='legacy-music',business_name='原版歌曲')
        w=installed['instance']['workspace_id']
        row=s.command(COMPANY,w,'','create',request_id='legacy',data=data())
        assert row['song']['data']['schemaVersion']=='0.1.0' and 'direction_ref' not in row['song']['data']
        original=row['lyrics'];oldid=row['song']['entity_id']
        with db.connect() as con: before=con.execute("select payload from evolution_events where correlation_id=?",(oldid,)).fetchall()
        updated=s.command(COMPANY,w,oldid,'save-lyrics',request_id='legacy-edit',expected={'lyrics_ref':original['entity_id']},data={'text':'原版用户编辑','draft_revision':'legacy2'})
        assert updated['lyrics']['data']['schemaVersion']=='0.1.0' and original in updated['versions']
        with db.connect() as con: assert [x[0] for x in con.execute("select payload from evolution_events where correlation_id=?",(oldid,)).fetchall()][:len(before)]==[x[0] for x in before]
        assert s.entry.authoring_scope(COMPANY,w)['definition']['version']=='0.1.0'
        with pytest.raises(RuntimeScopeError):s.operating_collection(COMPANY,w)


def test_media_exact_two_roots_no_arbitrary_root(tmp_path):
    assert MusicMediaService(None,root=APPROVED_ROOT).root==APPROVED_ROOT
    assert MusicMediaService(None,root=OPERATING_ROOT).root==OPERATING_ROOT
    with pytest.raises(ValueError):MusicMediaService(None,root=tmp_path)


def test_sole_usage_real_ledger_rows_dedup_null_and_frozen_report(tmp_path):
    """Inserted isolated ledger fixtures prove projection, not external Provider metering."""
    db,_,w,s=setup(tmp_path)
    with scope():
        a,b,c,d=chain(s,w);song=completed(s,w,d)
        def add_usage(key, company=COMPANY, workspace=w):
            with db.connect() as con:
                con.execute("insert into ai_usage_records(usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,model_name,input_tokens,output_tokens,total_tokens,cost_amount,currency,cost_source,employee_id,capability_id,capability_type,task_id,department_id,business_id,workspace_id,work_ref,execution_ref,request_id,execution_status,metering_status,occurred_at,idempotency_key) values (?,'selfuse',?,'fixture-gateway','fixture-provider','fixture-model',5,6,11,null,'USD','unknown','fixture-employee','fixture-model','model',?,'cg-dept','music-business',?,?,?,?,'success','unknown','2026-09-01T00:00:00Z',?)", (key,company,'fixture-task-'+key,workspace,'fixture-work-'+key,'fixture-execution-'+key,'fixture-request-'+key,'fixture-idempotency-'+key))
                s.runtime.insert(con,COMPANY,w,'Candidate',{'title':'fixture来源用量','suggestion':'仅验证已有账本来源投影','lyrics_ref':song['lyrics']['entity_id'],'production_ref':song['production']['entity_id'],'asset_ref':'','source':'CONTROLLED_EXECUTOR','provenance':{'fixture':True,'usage':{'usage_record_id':key}}},'fixture-owner',song=song['song']['entity_id'])
        add_usage('usage-one')
        op(s,w,'save-observation',observation(a,song,0),'o-one');op(s,w,'save-observation',observation(a,song,2),'o-two')
        report=op(s,w,'create-report',{'title':'累计创作用量','body':'原观察不是期间成本','selection':{'scope_ref':a['entity_id'],'song_ref':'','period':'all'}},'usage-report')['record']
        assert report['data']['usage_basis']=='SONG_CUMULATIVE_CREATIVE_CALLS'
        assert len(report['data']['rows'])==2 and len(report['data']['usage'])==1
        assert report['data']['usage'][0]['usage_record_id']=='usage-one' and report['data']['usage'][0]['cost_amount'] is None
        add_usage('usage-two')
        saved=s.operating_content(COMPANY,w,report['entity_id'])
        assert saved['record']==report and not saved['report_current']
        assert len(saved['record']['data']['usage'])==1
        add_usage('foreign-usage',company='other-company')
        with pytest.raises(RuntimeScopeError):s.operating_collection(COMPANY,w)


def test_period_bad_types_mixed_timezone_are_input_errors():
    for invalid in [{'start':1,'end':'2026-10-02','timezone':'Asia/Shanghai'}, {'start':'2026-10-01T00:00:00+00:00','end':'2026-10-02','timezone':'Asia/Shanghai'}, {'start':'2026-10-01','end':'2026-10-02','timezone':None}]:
        with pytest.raises(ValueError):MusicRuntime.period(invalid)


def test_user_provided_local_rights_propagate_without_provider(tmp_path, monkeypatch):
    from backend.tests.test_music_local_import import local_setup, scope as local_scope, create, wav, upload, finish
    root, db, runtime, w, service = local_setup(tmp_path, monkeypatch)
    with local_scope():
        row = finish(service, w, upload(service, w, create(service, w), wav()))
        assert row['master']['data']['rights'] == row['releases'][0]['data']['rights'] == 'LOCAL_USER_PROVIDED_UNVERIFIED'
        assert row['releases'][0]['data']['status'] == 'LOCAL_PREPARATION_NOT_PUBLISHED'
    with db.connect() as con:
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 0
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
