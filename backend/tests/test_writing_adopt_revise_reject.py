"""T-010 决定一：离线持久化与受控模型证据。"""
import asyncio
import inspect
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.writing_chapter_service import WritingChapterService, WritingConflict
from app.database import Database
from app.runtime import RuntimeFoundation
from backend.tests import test_writing_chapter_vertical as vertical
from backend.tests.test_writing_selected_execution import ready, explicit_work, COMPANY, CEO, scope
from backend.tests.test_writing_chapter_vertical import command

@pytest.fixture
def writing(tmp_path, monkeypatch):
    monkeypatch.setattr(vertical, 'SOURCE', Path(vertical.__file__).resolve().parents[1] / 'app/bundled_workspace_packages/writing_authoring')
    return ready(tmp_path, monkeypatch)

def proposal(service,w,b,c,binding,text='新正文'):
    return command(service,w,b,c,'candidate.manual-recorded',{'selection':binding['selection'],'replacement':text},request='proposal-'+text)

def test_w08a_atomic_formal_idempotent_cold(writing):
    db,app,entry,s,calls,w,b,c,binding=writing
    with scope():
        candidate=proposal(s,w,b,c,binding)
        adopted=command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True})
        again=command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True},request='another-click')
        assert again==adopted
        events=WritingChapterService(Database(db.path)).chapter(COMPANY,w,b,c)['events']
        formal=[e for e in events if e['action']=='formal.confirmed']
        assert len(formal)==1 and formal[0]['ref']==adopted['formal_ref']
        assert formal[0]['snapshot']==adopted['draft']
        assert calls==[]

def test_w08c_rejected_retains_content_source_and_formal(writing):
    db,app,entry,s,calls,w,b,c,binding=writing
    with scope():
        candidate=proposal(s,w,b,c,binding)
        check=command(s,w,b,c,'inspection.recorded',{'mode':'AUTHOR_MANUAL','checks':['continuity','language','rights'],'note':''})
        command(s,w,b,c,'formal.confirmed',{'inspection_ref':check['ref'],'confirmed':True})
        before=s.chapter(COMPANY,w,b,c)
        rejected=command(s,w,b,c,'candidate.rejected',{'candidate_ref':candidate['ref'],'reason':'不符合要求'})
        assert rejected['status']=='REJECTED'
        after=WritingChapterService(db).chapter(COMPANY,w,b,c)
        assert after['draft']==before['draft']
        assert [e for e in after['events'] if e['ref']==candidate['ref']][0]['replacement']=='新正文'
        assert [e for e in after['events'] if e['action']=='formal.confirmed']==[e for e in before['events'] if e['action']=='formal.confirmed']
        with pytest.raises(WritingConflict):
            command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True})
        assert calls==[]

def test_w10a_latest_history_and_candidate_explicit(writing):
    db,app,entry,s,calls,w,b,c,binding=writing
    with scope():
        candidate=proposal(s,w,b,c,binding)
        events=s.chapter(COMPANY,w,b,c)['events']
        data={'source_ref':candidate['ref'],'requirements':'改善语气','confirmed':True}
        assert s.continuation_basis(events=events,data=data)['source_class']=='CANDIDATE'
        first=command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True})
        command(s,w,b,c,'draft.saved',{'text':'第二正式正文','knowledge':[]},request='second')
        check=command(s,w,b,c,'inspection.recorded',{'mode':'AUTHOR_MANUAL','checks':['continuity','language','rights'],'note':''})
        second=command(s,w,b,c,'formal.confirmed',{'inspection_ref':check['ref'],'confirmed':True})
        events=s.chapter(COMPANY,w,b,c)['events']
        latest=s.continuation_basis(events=events,data={**data,'source_ref':''})
        old=s.continuation_basis(events=events,data={**data,'source_ref':first['formal_ref']})
        assert latest['source_ref']==second['ref'] and latest['text']=='第二正式正文'
        assert old['text']==first['draft']['text'] and old['source_class']=='FORMAL'
        with pytest.raises(WritingConflict): s.continuation_basis(events=events,data=data)
        revision=s.continuation_basis(events=events,data={**data,'mode':'REVISE'})
        assert revision['source_ref']==candidate['ref'] and revision['source_class']=='CANDIDATE'

def test_w08b_w11a_confirm_work_cancel_and_source_prompt(writing):
    db,app,entry,s,calls,w,b,c,binding=writing
    # Publish the current responsibility workflow through the existing fixture.
    explicit_work(db,app,entry,s,w,b,c,binding)
    with scope():
        candidate=proposal(s,w,b,c,binding,'指定来源正文')
        assignment=entry.metadata(COMPANY,w)['assignment_ref']
        draft=s.chapter(COMPANY,w,b,c)['draft']
        initial=RuntimeFoundation(db).list('WORK',company_id=COMPANY,workspace_id=w)
    source={'kind':'writing','book_ref':b,'chapter_ref':c,'expected_draft_ref':draft['ref'],'selection':binding['selection'],
            'continuation':{'source_ref':candidate['ref'],'requirements':'改得简洁','confirmed':False}}
    payload={'request_id':'revision','problem':'改得简洁','expected_result':'人工采用前候选','model_key':'model.writing-entry','source':source}
    headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
    with TestClient(app) as client:
        url=f'/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work'
        response=client.post(url,json=payload,headers=headers)
        assert response.status_code==200,response.text
        assert response.json()['work'] is None and calls==[]
        with scope(): assert RuntimeFoundation(db).list('WORK',company_id=COMPANY,workspace_id=w)==initial
        source['continuation']['confirmed']=True
        response=client.post(url,json=payload,headers=headers)
        assert response.status_code==200,response.text
        work=response.json()['work']['entity_id']
        replay=client.post(url,json=payload,headers=headers)
        assert replay.status_code==200 and replay.json()['work']['entity_id']==work
    with scope():
        claim,created=s.prepare_message(COMPANY,w,b,c,binding_ref=binding['ref'],body='改得简洁',request_id='rev-exec',model_key='model.writing-entry',work_ref=work)
        assert created and calls==[]
        endpoint=next(r.endpoint for r in app.routes if getattr(r,'path','').endswith('/chapters/{chapter_ref}/messages'))
        executor=inspect.getclosurevars(endpoint).nonlocals['executor']
        asyncio.run(entry.conversations.execute(claim,executor))
        assert len(calls)==1
        prompt=json.dumps(calls[0],ensure_ascii=False)
        assert '指定来源正文' in prompt and '改得简洁' in prompt
        assert s.chapter(COMPANY,w,b,c)['draft']==draft
        assert not any(e['action']=='formal.confirmed' for e in s.chapter(COMPANY,w,b,c)['events'])
        assert RuntimeFoundation(db).get(work)['lifecycle_status']=='ACTIVE'


def test_w08a_formal_insert_rolls_back_with_adoption_failure(writing):
    db,app,entry,s,calls,w,b,c,binding=writing
    with scope():
        candidate=proposal(s,w,b,c,binding)
        before=s.chapter(COMPANY,w,b,c)
        with db.connect() as con:
            con.execute("create trigger fail_adoption before insert on evolution_events when new.event_type='writing.chapter.candidate.adopted' begin select raise(abort, 'controlled failure'); end")
        import sqlite3
        with pytest.raises(sqlite3.IntegrityError):
            command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True})
        after=WritingChapterService(db).chapter(COMPANY,w,b,c)
        assert after['draft']==before['draft'] and after['events']==before['events']
        assert calls==[]


def test_w08a_concurrent_clicks_one_formal(writing):
    from concurrent.futures import ThreadPoolExecutor
    db,app,entry,s,calls,w,b,c,binding=writing
    with scope():
        candidate=proposal(s,w,b,c,binding)
        base=s.chapter(COMPANY,w,b,c)['draft']['ref']
    def adopt(index):
        with scope():
            return command(s,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True},request='click-'+str(index),base=base)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(adopt,range(2)))
    assert results[0]==results[1]
    with scope():
        assert len([e for e in s.chapter(COMPANY,w,b,c)['events'] if e['action']=='formal.confirmed'])==1
