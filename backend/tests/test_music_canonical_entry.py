"""Scoped holder/media evidence; fixtures are not ordinary publication acceptance."""
import json
from concurrent.futures import ThreadPoolExecutor
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.runtime.music import MusicConflict, MusicRuntime
from app.music_entry_service import MusicEntryService, ASSETS
from app.music_service import MusicService
from app.music_media_service import MusicMediaService, OPERATING_ROOT as APPROVED_ROOT, SAMPLES
from app.workspace_package_runtime import validate_package, PackageValidationError
from backend.tests.test_cg_content_entry import setup as cg_setup
from backend.tests.test_writing_chapter_vertical import scope, COMPANY


@pytest.fixture(autouse=True)
def isolated_media(tmp_path, monkeypatch):
    """Fresh generated WAV fixtures; never reuse a previous delivery's media root."""
    import wave, hashlib, sys
    from app import music_media_service
    root = tmp_path / "media-fixture"
    for name in ("inputs", "media", "evidence", "staging"):
        (root / name).mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(music_media_service, "OPERATING_ROOT", root)
    monkeypatch.setattr(sys.modules[__name__], "APPROVED_ROOT", root)
    for i, name in enumerate(SAMPLES):
        path = root / "inputs" / name
        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000)
            audio.writeframes(bytes([i, 0]) * (8000 * 32))
        monkeypatch.setitem(SAMPLES, name, hashlib.sha256(path.read_bytes()).hexdigest())


def setup(path):
    db, runtime, _ = cg_setup(path)
    with scope():
        installed = runtime.install(ASSETS/'music', COMPANY, department_id='cg-dept', business_id='music-business', business_name='内部音乐验证')
    w = installed['instance']['workspace_id']
    media = MusicMediaService(db, root=APPROVED_ROOT); entry = MusicEntryService(db); entry.media = media
    return db, runtime, w, MusicService(db, entry=entry, media=media)


def data(): return dict(title='第一首歌', intention='雨后的回忆', lyrics='你的名字😀，留在雨中。', production='轻快节奏，留白', draft_revision='lyrics-1')
def create(s,w): return s.command(COMPANY,w,'','create',request_id='song-1',data=data())
def basis(row): return {k:row['song']['data'][k] for k in ('lyrics_ref','production_ref','master_ref')}
def lyrics_selection(row): return dict(kind='lyrics',version_ref=row['lyrics']['entity_id'],draft_revision=row['lyrics']['data']['draft_revision'],start=4,end=6,excerpt='😀',locator='lyrics')
def audio(s,w,row,name='demo-a.wav'):
    return s.command(COMPANY,w,row['song']['entity_id'],'local-sample',request_id=name,expected=basis(row),data={'sample':name,'title':name})
def choose(s,w,row):
    candidate=row['candidates'][-1]; asset=next(a for a in row['assets'] if a['entity_id']==candidate['data']['asset_ref'])
    audition=dict(asset_ref=asset['entity_id'],sha256=asset['data']['sha256'],position=8.0,duration=32.0,source='USER_REPORTED_PLAYBACK')
    return s.command(COMPANY,w,row['song']['entity_id'],'choose',request_id='choose',expected=basis(row),data={'candidate_ref':candidate['entity_id'],'audition':audition})
def master(s,w,row):
    return s.command(COMPANY,w,row['song']['entity_id'],'confirm-master',request_id='master',expected=basis(row),data={'choice_ref':row['choice']['entity_id'],'credits':'本地原创设计样本；演唱匹配未验证','confirmation':{'basis':True,'local_only':True}})


def test_sole_holder_no_generic_copy_and_no_publication(tmp_path):
    db,runtime,w,s=setup(tmp_path)
    with scope():
        row=create(s,w); assert create(s,w)['song']['entity_id']==row['song']['entity_id']
        assert s.entry.definitions(COMPANY)['available'] is True
        assert s.entry.publication()['version']=='0.2.0'
        with pytest.raises(PackageValidationError): runtime.create_object(w,'core.domain-object.create','MusicSong',{'title':'copy','intention':'copy'})
    with db.connect() as con:
        assert con.execute('select count(*) from workspace_package_objects').fetchone()[0]==0
        assert con.execute("select count(*) from runtime_entities where entity_type='PACKAGE_DOMAIN_OBJECT'").fetchone()[0]==3
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0]==0


def test_independent_heads_utf16_and_cold_restart(tmp_path):
    db,_,w,s=setup(tmp_path)
    with scope():
        row=create(s,w);sel=lyrics_selection(row); assert s.selection(COMPANY,w,row['song']['entity_id'],sel)==sel
        updated=s.command(COMPANY,w,row['song']['entity_id'],'save-production',request_id='prod2',expected={'production_ref':row['production']['entity_id']},data={'brief':'新的节奏','draft_revision':'production-2'})
        assert updated['lyrics']==row['lyrics']; assert s.selection(COMPANY,w,row['song']['entity_id'],sel)==sel
        updated=s.command(COMPANY,w,row['song']['entity_id'],'save-lyrics',request_id='lyr2',expected={'lyrics_ref':row['lyrics']['entity_id']},data={'text':'你的回忆，留在雨中。','draft_revision':'lyrics-2'})
        with pytest.raises(MusicConflict):s.selection(COMPANY,w,row['song']['entity_id'],sel)
        assert row['lyrics'] in updated['versions']
        cold=MusicService(Database(db.path),media=MusicMediaService(Database(db.path),root=APPROVED_ROOT)).content(COMPANY,w,row['song']['entity_id'])
        assert cold['lyrics']==updated['lyrics'] and cold['production']==updated['production']


def test_media_range_actual_duration_scope_and_fixed_master(tmp_path):
    db,_,w,s=setup(tmp_path)
    with scope():
        row=audio(s,w,create(s,w)); song=row['song']['entity_id'];asset=row['assets'][0]
        with db.connect() as con:
            raw,status,headers=s.media.read(con,COMPANY,w,song,asset['entity_id'],'bytes=0-43')
            assert status==206 and raw[:4]==b'RIFF' and len(raw)==44 and headers['Content-Range'].startswith('bytes 0-43/')
            assert s.media.verify(con,COMPANY,w,song,asset['entity_id'])['data']['duration']==32.0
            with pytest.raises(ValueError):s.media.read(con,COMPANY,w,song,asset['entity_id'],'bytes=99999999-')
            other=s.command(COMPANY,w,'','create',request_id='other-song',data=data())
            with pytest.raises(RuntimeScopeError):s.media.read(con,COMPANY,w,other['song']['entity_id'],asset['entity_id'])
        chosen=choose(s,w,row);assert chosen['master'] is None
        final=master(s,w,chosen);assert final['master']['data']['asset_ref']==asset['entity_id']
        original=final['master']
        changed=s.command(COMPANY,w,song,'save-lyrics',request_id='new-lyrics',expected={'lyrics_ref':final['lyrics']['entity_id']},data={'text':'你的回忆，留在雨中。','draft_revision':'lyrics-2'})
        assert changed['master']==original and original['data']['lyrics_ref']==row['lyrics']['entity_id']
        release=s.command(COMPANY,w,song,'prepare-release',request_id='release',expected=basis(changed),data={'master_ref':original['entity_id']})
        assert release['releases'][0]['data']['master_ref']==original['entity_id'] and release['releases'][0]['data']['status']=='LOCAL_PREPARATION_NOT_PUBLISHED'
        assert master(s,w,chosen)['result_ref']==original['entity_id'] # retry returns original receipt despite newer lyrics


@pytest.mark.parametrize('mutation', ['parent','scope','rights','hash','duration'])
def test_corrupt_asset_fail_closed(tmp_path,mutation):
    db,_,w,s=setup(tmp_path)
    with scope():row=audio(s,w,create(s,w))
    asset=row['assets'][0];payload=dict(asset['data'])
    with db.connect() as con:
        if mutation=='parent': con.execute('update runtime_entities set parent_id=? where entity_id=?',(w,asset['entity_id']))
        elif mutation=='scope':con.execute('update runtime_entities set company_id=? where entity_id=?',('other',asset['entity_id']))
        else:
            payload[{'rights':'rights','hash':'sha256','duration':'duration'}[mutation]]={'rights':'COMMERCIAL','hash':'0'*64,'duration':40}[mutation]
            con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(payload),asset['entity_id']))
    with scope(),db.connect() as con,pytest.raises((ValueError,RuntimeScopeError)):
        s.media.read(con,COMPANY,w,row['song']['entity_id'],asset['entity_id'])


def test_cas_concurrent_and_receipt_conflict_no_partial_versions(tmp_path):
    db,_,w,s=setup(tmp_path)
    with scope():row=create(s,w)
    def save(i):
        with scope():
            try:return s.command(COMPANY,w,row['song']['entity_id'],'save-lyrics',request_id=f'save-{i}',expected={'lyrics_ref':row['lyrics']['entity_id']},data={'text':f'版本{i}','draft_revision':f'v{i}'})
            except MusicConflict:return None
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(save,[0,1]))
    assert sum(r is not None for r in results)==1
    with scope(),pytest.raises(MusicConflict):s.command(COMPANY,w,'','create',request_id='song-1',data={**data(),'title':'偷偷改名'})
    with db.connect() as con:assert con.execute("select count(*) from runtime_entities where json_extract(data_json,'$.kind')='LyricsVersion'").fetchone()[0]==2


def test_atomic_domain_and_receipt_rollback_orphan_unreadable(tmp_path,monkeypatch):
    db,_,w,s=setup(tmp_path)
    original=MusicRuntime.insert
    def failing(self,con,*args,**kwargs):
        ref=original(self,con,*args,**kwargs)
        if args[2]=='Candidate': raise RuntimeError('injected registration failure after bytes')
        return ref
    with scope():row=create(s,w)
    monkeypatch.setattr(MusicRuntime,'insert',failing)
    with scope(),pytest.raises(RuntimeError):audio(s,w,row)
    assert (APPROVED_ROOT/'media'/f'{SAMPLES["demo-a.wav"]}.wav').exists()
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where json_extract(data_json,'$.kind') in ('Candidate','AudioAssetVersion')").fetchone()[0]==0
        assert con.execute('select count(*) from evolution_events where event_type=?',('music.command.completed',)).fetchone()[0]==1
    with scope(),db.connect() as con,pytest.raises(RuntimeScopeError):s.media.read(con,COMPANY,w,row['song']['entity_id'],SAMPLES['demo-a.wav'])


def test_audio_selection_does_not_retarget_or_exceed_duration(tmp_path):
    db,_,w,s=setup(tmp_path)
    with scope():
        row=audio(s,w,create(s,w));c=row['candidates'][0];a=row['assets'][0]
        sel=dict(kind='audio',song_ref=row['song']['entity_id'],candidate_ref=c['entity_id'],candidate_version_ref=c['entity_id'],asset_ref=a['entity_id'],sha256=a['data']['sha256'],start=8,end=16,duration=32,anchor='candidate-audio')
        assert s.selection(COMPANY,w,row['song']['entity_id'],sel)==sel
        for changed in ({'end':40},{'end':float('nan')},{'candidate_version_ref':'other'},{'asset_ref':'other'}):
            with pytest.raises((ValueError,RuntimeScopeError)):s.selection(COMPANY,w,row['song']['entity_id'],{**sel,**changed})
        row=audio(s,w,row,'demo-b.wav');assert s.selection(COMPANY,w,row['song']['entity_id'],sel)==sel
        assert sel['asset_ref']==a['entity_id'] # UI switching marks selection stale separately, no server retarget


def test_symlink_missing_and_rights_inputs_rejected(tmp_path):
    from app.music_media_service import read_file
    assert not MusicMediaService(None).root
    with pytest.raises(RuntimeScopeError):MusicMediaService(None).stage_sample('demo-a.wav')
    with pytest.raises(ValueError):MusicMediaService(None,root=tmp_path)
    with pytest.raises(RuntimeScopeError):MusicMediaService(None,root=APPROVED_ROOT).stage_sample('https://remote/audio.wav')
    # Test-owned links remain in approved evidence, never touch canonical media.
    link=APPROVED_ROOT/'evidence'/('symlink-'+__import__('uuid').uuid4().hex);link.symlink_to(APPROVED_ROOT/'inputs/demo-a.wav')
    with pytest.raises(OSError):read_file(link.parent,link.name)


def test_local_admission_rejects_changed_or_missing_decision(tmp_path,monkeypatch):
    from pathlib import Path
    db, *_ = setup(tmp_path)
    original=Path.read_text
    def changed(path,*a,**kw):
        raw=original(path,*a,**kw)
        if path == ASSETS/'music_release.json':
            value=json.loads(raw);value['decision']['sha256']='0'*64;return json.dumps(value)
        return raw
    monkeypatch.setattr(Path,'read_text',changed)
    with scope(),pytest.raises(ValueError):MusicEntryService(db).publication()
