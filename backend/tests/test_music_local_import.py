"""D206 synthetic ordinary local WAV; no old sample Root access or provider."""
import hashlib
import io
import json
import os
import wave
from pathlib import Path
from urllib.parse import quote
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.database import Database
from app.tenant_context import TenantContext
from app.workspace_package_runtime import WorkspacePackageRuntime
from app.music_entry_service import ASSETS, MusicEntryService
from app.music_media_service import MusicMediaService, inspect_audio
from app.music_service import MusicService
from app.runtime.music import MusicRuntime, MusicConflict
from app.runtime import RuntimeScopeError
from app.api.music_router import build_music_router

COMPANY = 'local-music-company'

def scope(**kw):
    return TenantContext.scope(**dict(tenant_id='selfuse', company_id=COMPANY, ceo_id='selfuse-ceo', role='ceo', **kw))

def wav(frames=16000, rate=8000):
    output=io.BytesIO()
    with wave.open(output,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b'\x01\x00'*frames)
    return output.getvalue()

def local_setup(path, monkeypatch):
    root=path/'desktop';(root/'data').mkdir(parents=True)
    dbpath=root/'data/curis.sqlite'
    for key in ('CURIS_DB','CURIS_DB_PATH','CURIS_WORKSPACE_DB'): monkeypatch.setenv(key,str(dbpath))
    monkeypatch.setenv('CURIS_DESKTOP_DATA_ROOT',str(root))
    db=Database(str(dbpath));db.initialize()
    with db.connect() as c:
        c.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse','selfuse-ceo','本地测试','active')",(COMPANY,))
        c.execute("insert into department_templates(id,slug,name,department_type,source,tenant_id) values ('local-test','local-test','本地部门模板','TEST','tenant_private','selfuse')")
        c.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values ('local-dept','selfuse',?,'local-test','本地部门','TEST','active')",(COMPANY,))
    with scope():
        runtime=WorkspacePackageRuntime(db,root/'assets/packages')
        installed=runtime.install(ASSETS/'music',COMPANY,department_id='local-dept',business_id='local-business',business_name='本地音乐')
    workspace=installed['instance']['workspace_id']
    media=MusicMediaService(db,data_root=str(root));entry=MusicEntryService(db);entry.media=media
    service=MusicService(db,entry=entry,media=media)
    return root,db,runtime,workspace,service

def basis(row):return {k:row['song']['data'][k] for k in ('lyrics_ref','production_ref','master_ref')}
def create(s,w):return s.command(COMPANY,w,'','create',request_id='song',data={'title':'用户歌曲','intention':'本地创作','lyrics':'原歌词','production':'原制作','draft_revision':'v1'})
def metadata(raw):return {'title':'用户提供音频','sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw)}
def upload(s,w,row,raw,key='import'):
    return s.command(COMPANY,w,row['song']['entity_id'],'import-audio',request_id=key,expected=basis(row),data=metadata(raw),raw_audio=raw)

def finish(s,w,row):
    a=row['assets'][-1];c=row['candidates'][-1];song=row['song']['entity_id']
    row=s.command(COMPANY,w,song,'choose',request_id='choose',expected=basis(row),data={'candidate_ref':c['entity_id'],'audition':{'asset_ref':a['entity_id'],'sha256':a['data']['sha256'],'duration':a['data']['duration'],'position':0.5,'source':'USER_REPORTED_PLAYBACK'}})
    row=s.command(COMPANY,w,song,'confirm-master',request_id='master',expected=basis(row),data={'choice_ref':row['choice']['entity_id'],'credits':'用户提供；商权未核验','confirmation':{'basis':True,'local_only':True}})
    return s.command(COMPANY,w,song,'prepare-release',request_id='prepare',expected=basis(row),data={'master_ref':row['master']['entity_id']})

def test_normal_import_replay_query_read_master_and_cold(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    assert not s.media.root.exists() # constructor creates no storage
    with scope():
        first=create(s,w);raw=wav();row=upload(s,w,first,raw)
        assert upload(s,w,first,raw)['result_ref']==row['result_ref']
        assert s.import_status(COMPANY,w,first['song']['entity_id'],'import')['result_ref']==row['result_ref']
        assert s.import_status(COMPANY,w,first['song']['entity_id'],'absent')['status']=='NOT_APPLIED'
        assert row['assets'][0]['data']['rights']=='LOCAL_USER_PROVIDED_UNVERIFIED'
        assert row['assets'][0]['data']['purpose']=='LOCAL_USE_ONLY'
        with db.connect() as c:
            received,status,_=s.media.read(c,COMPANY,w,row['song']['entity_id'],row['assets'][0]['entity_id'])
            assert received==raw and status==200
        final=finish(s,w,row)
        assert final['master']['data']['rights']==final['releases'][0]['data']['rights']=='LOCAL_USER_PROVIDED_UNVERIFIED'
        assert final['releases'][0]['data']['status']=='LOCAL_PREPARATION_NOT_PUBLISHED'
        cold=MusicService(Database(db.path),entry=s.entry,media=MusicMediaService(Database(db.path),data_root=str(root)))
        assert cold.content(COMPANY,w,row['song']['entity_id'])['master']==final['master']
        other=create(s,w)
        with pytest.raises(RuntimeScopeError),db.connect() as c:s.media.read(c,COMPANY,w,'foreign-song',row['assets'][0]['entity_id'])
        with pytest.raises(MusicConflict):upload(s,w,first,wav(8000),'import')
    assert len(list(s.media.root.glob('*.wav')))==1
    assert not list((root/'cache/tmp/music-import').iterdir())

@pytest.mark.parametrize('raw',[b'not wav',wav()[:-2],wav(rate=4000),b'x'*16000001])
def test_invalid_file_has_no_asset_or_candidate(tmp_path,monkeypatch,raw):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w)
        with pytest.raises(ValueError):upload(s,w,row,raw)
    with db.connect() as c:assert c.execute("select count(*) from runtime_entities where json_extract(data_json,'$.kind') in ('AudioAssetVersion','Candidate')").fetchone()[0]==0
    assert not s.media.root.exists()

def test_stale_basis_and_root_alias_refuse_before_file(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w)
        s.command(COMPANY,w,row['song']['entity_id'],'save-lyrics',request_id='new',expected={'lyrics_ref':row['lyrics']['entity_id']},data={'text':'新版','draft_revision':'v2'})
        with pytest.raises(MusicConflict):upload(s,w,row,wav())
    assert not s.media.root.exists()
    monkeypatch.setenv('CURIS_DB_PATH',str(root/'other.sqlite'))
    with pytest.raises(ValueError):MusicMediaService(db,data_root=str(root))

def test_registration_failure_retains_bounded_unserved_orphan(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    original=MusicRuntime.insert
    def fail(self,con,company,workspace,kind,*a,**kw):
        if kind=='Candidate':raise RuntimeError('injected registration failure')
        return original(self,con,company,workspace,kind,*a,**kw)
    with scope():
        row=create(s,w);monkeypatch.setattr(MusicRuntime,'insert',fail)
        with pytest.raises(RuntimeError):upload(s,w,row,wav())
        assert s.import_status(COMPANY,w,row['song']['entity_id'],'import')['status']=='NOT_APPLIED'
    assert len(list(s.media.root.glob('*.wav')))==1
    with db.connect() as c:assert c.execute("select count(*) from runtime_entities where json_extract(data_json,'$.kind')='AudioAssetVersion'").fetchone()[0]==0

def test_symlink_and_tamper_are_not_served(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    with scope():
        row=upload(s,w,create(s,w),wav());a=row['assets'][0];target=s.media.root/(a['data']['sha256']+'.wav')
        target.write_bytes(b'tamper')
        with pytest.raises(ValueError),db.connect() as c:s.media.verify(c,COMPANY,w,row['song']['entity_id'],a['entity_id'])
        target.unlink();other=root/'cache/other.wav';other.write_bytes(wav());target.symlink_to(other)
        with pytest.raises(OSError),db.connect() as c:s.media.verify(c,COMPANY,w,row['song']['entity_id'],a['entity_id'])

def test_staging_failure_closes_store_fd(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    import app.music_media_service as media
    original=media.ensure_directory;opened=[]
    def open_once(path):
        if opened:raise OSError('staging denied')
        fd=original(path);opened.append(fd);return fd
    monkeypatch.setattr(media,'ensure_directory',open_once)
    with pytest.raises(OSError):s.media.stage_user(wav())
    with pytest.raises(OSError):os.fstat(opened[0])

def test_raw_endpoint_uses_strict_scope_metadata_limits_and_query(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    app=FastAPI();app.include_router(build_music_router(db,None,service=s))
    with scope():row=create(s,w)
    base=f'/api/workspace/v1/companies/{COMPANY}/music/{w}/songs/{row["song"]["entity_id"]}'
    payload={'request_id':'http-import','expected':basis(row),'data':metadata(wav())}
    headers={'Content-Type':'audio/wav','X-Music-Import':quote(json.dumps(payload))}
    with scope(),TestClient(app) as c:
        response=c.post(base+'/audio-import',headers=headers,content=wav());assert response.status_code==200,response.text
        assert c.get(base+'/imports/http-import').json()['status']=='APPLIED'
        assert c.post(base+'/audio-import',headers=headers,content=b'changed').status_code==422
        assert c.post(base+'/audio-import',headers=headers,content=b'x'*16000001).status_code==413
        assert c.post(base+'/audio-import',headers={**headers,'X-Music-Import':'%bad'},content=wav()).status_code==422
    with TenantContext.scope(tenant_id='other',ceo_id='selfuse-ceo',role='ceo'),TestClient(app) as c:
        assert c.post(base+'/audio-import',headers=headers,content=wav()).status_code==404


def test_receiving_request_is_unknown_and_not_false_not_applied(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w)
        with s.receiving_import(COMPANY,w,row['song']['entity_id'],'pending'):
            assert s.import_status(COMPANY,w,row['song']['entity_id'],'pending')['status']=='UNKNOWN'
            with pytest.raises(MusicConflict):
                with s.receiving_import(COMPANY,w,row['song']['entity_id'],'pending'):pass
        assert s.import_status(COMPANY,w,row['song']['entity_id'],'pending')['status']=='NOT_APPLIED'


def test_absent_receipt_before_late_post_still_replays_one_candidate(tmp_path,monkeypatch):
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w)
        assert s.import_status(COMPANY,w,row['song']['entity_id'],'import')['status']=='NOT_APPLIED'
        original=upload(s,w,row,wav())
        retry=upload(s,w,row,wav())
        assert original['result_ref']==retry['result_ref']
        assert len(retry['assets'])==len(retry['candidates'])==1


def test_audio_store_retains_orphan_with_bound_and_rejects_cross_provenance(tmp_path,monkeypatch):
    import app.music_media_service as media
    root,db,_,w,s=local_setup(tmp_path,monkeypatch)
    s.media.stage_user(wav())
    monkeypatch.setattr(media,'MAX_AUDIO_FILES',1)
    with pytest.raises(ValueError):s.media.stage_user(wav(8000))
    assert len(list(s.media.root.glob('*.wav')))==1
    legacy=inspect_audio(wav())
    for rights,purpose in [('LOCAL_DESIGN_ONLY','LOCAL_USE_ONLY'),('LOCAL_USER_PROVIDED_UNVERIFIED','NONCOMMERCIAL_ISOLATED_TEST')]:
        with pytest.raises(ValueError):MusicRuntime(db).validate('AudioAssetVersion',{**legacy,'rights':rights,'purpose':purpose})
