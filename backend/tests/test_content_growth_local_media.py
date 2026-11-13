"""Real controlled bytes under a fresh private desktop root, never a user profile."""
import hashlib
import json
import os
import sqlite3
import struct
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from urllib.parse import quote
from app.database import Database
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from app.content_growth_media_service import ContentGrowthMediaService, inspect_media, backup_budget
from app.api.content_growth_router import build_content_growth_router
from backend.tests.test_cg_content_entry import setup
from backend.tests.test_cg_four_form_interaction import install_v02, create, draft, save
from backend.tests.test_writing_chapter_vertical import scope, COMPANY
from backend.tests.test_music_local_import import wav


def png():
    def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xff\0\0'))+chunk(b'IEND',b'')


def local_setup(path,monkeypatch):
    original,_,_=setup(path);w=install_v02(original,path)
    root=path/'desktop';(root/'data').mkdir(parents=True)
    dest=root/'data/curis.sqlite'
    with original.connect() as con,sqlite3.connect(dest) as target:con.backup(target)
    for key in ('CURIS_DB','CURIS_DB_PATH','CURIS_WORKSPACE_DB'):monkeypatch.setenv(key,str(dest))
    monkeypatch.setenv('CURIS_DESKTOP_DATA_ROOT',str(root))
    db=Database(str(dest));media=ContentGrowthMediaService(db,data_root=root);s=ContentGrowthService(db,media=media)
    return root,db,w,s,media


def payload(raw,mime='image/png',use='OUTPUT'):
    return {'title':'人工原文件','sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'mime':mime,'use':use}


def test_import_real_read_range_replay_adopt_and_stale(tmp_path,monkeypatch):
    root,db,w,s,m=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w,draft('graphic'));c=row['content']['entity_id'];v=row['version']['entity_id'];raw=png();data=payload(raw)
        before=s.content(COMPANY,w,c)['version']['entity_id']
        result=m.import_asset(s,COMPANY,w,c,'import',v,data,raw)
        assert m.import_asset(s,COMPANY,w,c,'import',v,data,raw)==result
        assert s.content(COMPANY,w,c)['version']['entity_id']==before
        returned,mime,status,headers=m.read(s,COMPANY,w,c,result['asset']['ref'],'bytes=0-7')
        assert returned==raw[:8] and mime=='image/png' and status==206
        receipt=m.adopt(s,COMPANY,w,c,'adopt',result['candidate']['ref'],True,True)
        assert m.adopt(s,COMPANY,w,c,'adopt',result['candidate']['ref'],True,True)==receipt
        saved=save(s,w,row,draft('graphic','新版正文'))
        with pytest.raises(ContentGrowthConflict):m.adopt(s,COMPANY,w,c,'stale',result['candidate']['ref'],True,True)
        with pytest.raises(ContentGrowthConflict):m.import_asset(s,COMPANY,w,c,'import',v,{**data,'title':'改名'},raw)
        assert m.read(s,COMPANY,w,c,result['asset']['ref'])[0]==raw
        path=root/'data/assets/content-growth-media'/f"{data['sha256']}.png"
        path.write_bytes(raw[:-1]+b'x')
        with pytest.raises(ValueError):m.read(s,COMPANY,w,c,result['asset']['ref'])


def test_signatures_actual_size_quotas_orphans_and_backup_budget(tmp_path,monkeypatch):
    root,db,w,s,m=local_setup(tmp_path,monkeypatch)
    with scope():
        row=create(s,w,draft('graphic'));c=row['content']['entity_id'];v=row['version']['entity_id'];raw=png()
        for bad in [b'<html>not an image</html>',raw[:-2]]:
            with pytest.raises(ValueError):m.import_asset(s,COMPANY,w,c,'bad',v,payload(bad),bad)
        with pytest.raises(ValueError):m.import_asset(s,COMPANY,w,c,'size',v,{**payload(raw),'size':len(raw)+1},raw)
        media=root/'data/assets/content-growth-media';media.mkdir(parents=True)
        orphan=media/('a'*64+'.mp4')
        with orphan.open('wb') as h:h.truncate(128*1024*1024)
        with pytest.raises(ValueError,match='128MiB'):m.import_asset(s,COMPANY,w,c,'quota',v,payload(raw),raw)
        orphan.unlink()
        large=root/'data/curis.sqlite.pre-restore-20261019T000000Z'
        with large.open('wb') as h:h.truncate(505*1024*1024)
        with pytest.raises(ValueError,match='备份容量'):m.import_asset(s,COMPANY,w,c,'budget',v,payload(raw),raw)
        assert list(media.iterdir())==[]


@pytest.mark.parametrize("content_length",[None,"1"])
def test_media_actual_stream_boundary_without_content_length(tmp_path,monkeypatch,content_length):
    root,db,w,s,m=local_setup(tmp_path,monkeypatch)
    with scope():row=create(s,w,draft('graphic'))
    from app import content_growth_media_service as module
    monkeypatch.setitem(module.MIME,'image/png',('png',64))
    app=FastAPI();app.include_router(build_content_growth_router(db,lambda *a:None,service=s));client=TestClient(app)
    url=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}/media'
    p={'request_id':'stream','expected_version_ref':row['version']['entity_id'],'data':payload(png())}
    with scope():
        response=client.post(url,headers={'X-CG-Import':quote(json.dumps(p)),**({'Content-Length':content_length} if content_length else {})},content=iter([png()[:40],png()[40:]]))
    assert response.status_code==413
    assert not (root/'data/assets/content-growth-media').exists()


def test_concurrent_imports_enforce_shared_retained_quota(tmp_path,monkeypatch):
    from app import content_growth_media_service as module
    root,db,w,s,m=local_setup(tmp_path,monkeypatch)
    a=png()
    def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    b=a[:-12]+chunk(b'tEXt',b'fixture\x00second')+a[-12:]
    monkeypatch.setattr(module,'MAX_TOTAL',max(len(a),len(b)))
    with scope():row=create(s,w,draft('graphic'))
    def import_one(pair):
        name,raw=pair
        with scope():
            try:return m.import_asset(s,COMPANY,w,row['content']['entity_id'],name,row['version']['entity_id'],payload(raw),raw)
            except ValueError as error:return str(error)
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(import_one,[('a',a),('b',b)]))
    assert sum(isinstance(v,dict) for v in results)==1
    assert len(list((root/'data/assets/content-growth-media').iterdir()))==1
    assert sum(p.stat().st_size for p in (root/'data/assets/content-growth-media').iterdir())<=module.MAX_TOTAL


def test_owner_pinned_real_inputs_import_read_and_invalid_refusal(tmp_path,monkeypatch):
    base=Path(__file__).resolve().parents[2]/'artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/QA_LOCAL_USE_CLOSURE_20261018/native-design-inputs-01'
    provenance=base/'INPUT_PROVENANCE.json'
    assert hashlib.sha256((base/'OUTPUT_MANIFEST.json').read_bytes()).hexdigest()=='a532aca2ae82ee912f147dda3dd2376fd16694f9fa334a09fd1cd0c118ddfbb2'
    assert hashlib.sha256(provenance.read_bytes()).hexdigest()=='f9e7b127dcc86dee5d0440b02866f22217315ed00efca00bc0c0197a4437d5b9'
    root,db,w,s,m=local_setup(tmp_path,monkeypatch)
    with scope():
        for item,mime,form in zip(json.loads(provenance.read_text())['inputs'],['image/png','audio/wav','video/mp4','audio/wav'],['graphic','speech','short_video','speech']):
            raw=Path(item['path']).read_bytes()
            assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
            row=create(s,w,draft(form),request='real-'+item['sha256']);c=row['content']['entity_id'];v=row['version']['entity_id']
            if item['path'].endswith('invalid-audio.wav'):
                with pytest.raises(ValueError):m.import_asset(s,COMPANY,w,c,'invalid-real',v,payload(raw,mime),raw)
            else:
                result=m.import_asset(s,COMPANY,w,c,item['sha256'],v,payload(raw,mime),raw)
                assert m.read(s,COMPANY,w,c,result['asset']['ref'])[0]==raw
                assert result['asset']['rights']=='LOCAL_USER_PROVIDED_UNVERIFIED'
