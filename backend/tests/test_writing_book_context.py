"""Scoped real companion state and old-book compatibility, never a live profile."""
import copy
import json
import pytest
from app.writing_book_service import WritingBookService, empty_context
from app.writing_chapter_service import WritingChapterService, WritingConflict
from app.runtime import RuntimeScopeError
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, command


def context(chapter):
    return {"setup": {"reader":"成年读者", "genre":"悬疑", "premise":"信的来历", "style":"克制", "conflict":"是否打开信"}, "items": [
        {"id":"outline", "kind":"outline", "title":"全书", "goal":"寻找来源", "order":0},
        {"id":"v1", "kind":"volume", "title":"第一卷", "parent":"outline", "order":0},
        {"id":"c1", "kind":"chapter", "title":"第一章", "chapter_ref":chapter, "parent":"v1", "goal":"发现信", "order":0, "character_refs":["person"], "world_refs":["world"]},
        {"id":"n1", "kind":"node", "title":"发现来信", "parent":"c1", "order":0},
        {"id":"world", "kind":"world", "title":"山谷", "category":"地点", "body":"不能穿越河流", "order":0},
        {"id":"person", "kind":"character", "title":"林澄", "role":"主角", "order":0},
        {"id":"person2", "kind":"character", "title":"来客", "role":"配角", "order":1},
        {"id":"rel", "kind":"relationship", "title":"尚未信任", "from_character":"person", "to_character":"person2", "order":0}]}


def test_old_book_no_lazy_write_revision_cas_replay_and_scope(tmp_path):
    db, runtime, w, b, c = setup(tmp_path)
    chapters = WritingChapterService(db); service = WritingBookService(db, chapters=chapters)
    with scope():
        with db.connect() as con: before = con.execute('select count(*) from runtime_entities').fetchone()[0]
        original = service.read(COMPANY, w, b)
        assert original['record'] is None and original['chapters'][0]['ref'] == c
        assert original['context'] == empty_context()
        with db.connect() as con: assert con.execute('select count(*) from runtime_entities').fetchone()[0] == before
        data = context(c)
        first = service.save(COMPANY, w, b, 'first', '', data)
        assert service.save(COMPANY, w, b, 'first', '', data) == first
        changed = copy.deepcopy(data);changed['items'][0]['goal'] = '新的目标'
        with pytest.raises(WritingConflict): service.save(COMPANY, w, b, 'first', '', changed)
        second = service.save(COMPANY, w, b, 'second', first['ref'], changed)
        with pytest.raises(WritingConflict): service.save(COMPANY, w, b, 'late', first['ref'], data)
        assert service.read(COMPANY, w, b, first['ref'])['context'] == data
        assert service.read(COMPANY, w, b)['record']['ref'] == second['ref']
        assert WritingBookService(db, chapters=WritingChapterService(db)).read(COMPANY, w, b)['record'] == second
        foreign = runtime.create_object(w, 'core.domain-object.create', 'WritingBook', {'title':'另一书','status':'DRAFT'})['object_id']
        with pytest.raises(RuntimeScopeError): service.save(COMPANY, w, foreign, 'foreign', '', data)


def test_typed_validation_and_failed_write_atomicity(tmp_path):
    db, _, w, b, c = setup(tmp_path); service = WritingBookService(db, chapters=WritingChapterService(db))
    with scope():
        for mutate in [lambda d:d['items'][3].update(parent='world'),lambda d:d['items'][7].update(to_character='person'),lambda d:d['items'][2].update(character_refs=['missing']),lambda d:d['items'][1].update(parent='c1'),lambda d:d['items'][4].update(order=-1),lambda d:d['setup'].update(unknown='no'),lambda d:d['items'][0].update(kind=[]),lambda d:d['items'][0].update(id={}),lambda d:d['items'][4].update(chapter_ref='foreign'),lambda d:d['items'][0].update(id='../bad')]:
            data = context(c);mutate(data)
            with pytest.raises((ValueError, RuntimeScopeError)): service.save(COMPANY, w, b, 'invalid', '', data)
            assert service.read(COMPANY, w, b)['record'] is None


def test_pinned_basis_manual_candidate_formal_and_stale_context(tmp_path):
    db, _, w, b, c = setup(tmp_path); chapters = WritingChapterService(db); service = WritingBookService(db, chapters=chapters)
    with scope():
        ctx = service.save(COMPANY, w, b, 'context', '', context(c))
        saved = command(chapters,w,b,c,'draft.saved',{'text':'她发现了来信。','knowledge':[]})
        basis = command(chapters,w,b,c,'context.bound',{'context_ref':ctx['ref'],'item_ids':['n1'],'confirmed':True})
        state = chapters.chapter(COMPANY,w,b,c)
        assert state['book_context_status']['status'] == 'CURRENT'
        assert {i['id'] for i in state['draft']['book_context_basis']['items']} >= {'c1','n1','world','person','v1','outline'}
        for ids in [[{}],[[]],['missing']]:
            with pytest.raises((ValueError,WritingConflict)):
                command(chapters,w,b,c,'context.bound',{'context_ref':ctx['ref'],'item_ids':ids,'confirmed':True},request='bad-items')
        selection={'draft_ref':saved['draft']['ref'],'sha256':saved['draft']['sha256'],'start':0,'end':1,'excerpt':'她','anchor':saved['draft']['ref']+':0:1','knowledge':[]}
        candidate=command(chapters,w,b,c,'candidate.manual-recorded',{'selection':selection,'replacement':'林澄'})
        assert candidate['source_class']=='CEO_MANUAL' and 'task_ref' not in candidate
        adopted=command(chapters,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True})
        command(chapters,w,b,c,'draft.saved',{'text':'林澄打开了信。','knowledge':[]},request='save-after-binding1')
        command(chapters,w,b,c,'draft.saved',{'text':'林澄读完了信。','knowledge':[]},request='save-after-binding2')
        assert chapters.chapter(COMPANY,w,b,c)['draft']['book_context_basis']==basis['book_context_basis']
        assert adopted['draft']['text']=='林澄发现了来信。' and adopted['draft']['book_context_basis']==basis['book_context_basis']
        inspection=command(chapters,w,b,c,'inspection.recorded',{'mode':'AUTHOR_MANUAL','checks':['continuity','language','rights'],'note':''})
        formal=command(chapters,w,b,c,'formal.confirmed',{'inspection_ref':inspection['ref'],'confirmed':True})
        pack=command(chapters,w,b,c,'package.prepared',{'formal_ref':formal['ref'],'introduction':'来信','credits':'作者','rights_declared':True,'target':'LOCAL_DOWNLOAD'})
        before=chapters.download(COMPANY,w,b,c,pack['ref'])
        updated=context(c);updated['items'][4]['body']='河流可以涉水'
        service.save(COMPANY,w,b,'revised',ctx['ref'],updated)
        assert chapters.chapter(COMPANY,w,b,c)['book_context_status']['status']=='STALE'
        with pytest.raises(WritingConflict): command(chapters,w,b,c,'formal.confirmed',{'inspection_ref':inspection['ref'],'confirmed':True},request='staleformal')
        with pytest.raises(WritingConflict): command(chapters,w,b,c,'inspection.recorded',{'mode':'AUTHOR_MANUAL','checks':['continuity','language','rights'],'note':''},request='stalecheck')
        assert chapters.download(COMPANY,w,b,c,pack['ref'])==before
        assert json.loads(before[0])['snapshot']['book_context_basis']['schema_version']=='writing.book-context/v1'


def test_actual_creation_source_dto_for_compiled_consumer(tmp_path):
    import os
    from pathlib import Path
    from app.writing_operating_service import WritingOperatingService
    db, _, w, b, c = setup(tmp_path)
    service = WritingChapterService(db)
    operating = WritingOperatingService(db, chapter_service=service)
    with scope():
        source = operating.learning_command(COMPANY,w,'save-learning',request_id='dto-learning',data={'title':'原经验版本','body':'在新章节检验明确冲突','basis_refs':[b],'applicability':'原创章节','counterexample':'人工经验未核验效果','accepted':True})['record']
        created = operating.learning_command(COMPANY,w,'use-learning',request_id='dto-use',data={'learning_ref':source['entity_id'],'book_ref':b,'title':'经验创建的新章','confirmed':True,'historical':False})
        chapter = service.chapter(COMPANY,w,b,created['chapter_ref'])
        record = operating.learning_content(COMPANY,w,source['entity_id'])['record']
        assert chapter['creation_source']['status']=='AVAILABLE'
    destination=os.getenv('CURIS_TEST_CREATION_SOURCE_OUTPUT')
    if destination:
        with Path(destination).open('x',encoding='utf-8') as output:
            json.dump({'chapter':chapter,'source_record':record},output,ensure_ascii=False,indent=2)


def test_discussion_and_employee_candidate_basis_cannot_follow_rebind(tmp_path,monkeypatch):
    """Isolate basis guard before employee proof; never manufacture verified execution."""
    db,_,w,b,c=setup(tmp_path);service=WritingChapterService(db,allow_execution=True)
    with scope():
        draft=command(service,w,b,c,'draft.saved',{'text':'她发现了信。','knowledge':[]})['draft']
        selection={'draft_ref':draft['ref'],'sha256':draft['sha256'],'start':0,'end':1,'excerpt':'她','anchor':draft['ref']+':0:1','knowledge':[]}
        topic={'conversation_id':'unit-only-topic'}
        monkeypatch.setattr(service.conversations,'read',lambda *args,**kwargs:{'messages':[]})
        responsibility={'status':'AVAILABLE','assignment_ref':'controlled-unit-assignment','context':{},'employee_ref':'unit-only'}
        monkeypatch.setattr(service,'responsibility',lambda *args, **kwargs:responsibility)
        monkeypatch.setattr(service.conversations,'owner',lambda *args:{'owner_ref':'unit-only'})
        binding=command(service,w,b,c,'discussion.bound',{'selection':selection,'assignment_ref':responsibility['assignment_ref'],'conversation_ref':topic['conversation_id']})
        assert binding['book_context_basis'] is None
        # The unchanged absent-basis chain reaches, and cannot bypass, strict employee provenance.
        data={'binding_ref':binding['ref'],'message_ref':'not-verified','reply_start':0,'reply_end':1,'reply_excerpt':'林'}
        with pytest.raises(RuntimeScopeError,match='已验证员工回复'):command(service,w,b,c,'candidate.recorded',data,request='unverified')
        books=WritingBookService(db,chapters=service);ctx=books.save(COMPANY,w,b,'basis-current','',context(c))
        command(service,w,b,c,'context.bound',{'context_ref':ctx['ref'],'item_ids':['n1'],'confirmed':True})
        with pytest.raises(WritingConflict,match='作品依据已变化'):command(service,w,b,c,'candidate.recorded',data,request='rebound-candidate')
        with pytest.raises(WritingConflict,match='作品依据已变化'):service.prepare_message(COMPANY,w,b,c,binding_ref=binding['ref'],body='请修改',request_id='rebound-message')
        state=service.chapter(COMPANY,w,b,c)
        with db.connect() as con:
            scoped,author,lineage,_=service._scope(con,COMPANY,w,b,c,write=True)
            old={'ref':'unit-candidate','action':'candidate.recorded',**data,'selection':selection,'draft_ref':draft['ref']}
            with pytest.raises(WritingConflict,match='原作品依据已变化'):
                service._apply(con,scoped,lineage,author,[*state['events'],old],state['draft'],'candidate.adopted',{'candidate_ref':old['ref'],'confirmed':True},'unit-adopt')
        assert service.chapter(COMPANY,w,b,c)['draft']['ref']==draft['ref']


def test_new_direction_revision_invalidates_fixed_basis_without_replacing_snapshot(tmp_path):
    from app.writing_operating_service import WritingOperatingService
    db,_,w,b,c=setup(tmp_path);service=WritingChapterService(db);books=WritingBookService(db,chapters=service);ops=WritingOperatingService(db,chapter_service=service)
    with scope():
        original={'title':'作品方向','body':'从来信开始','scope_ref':b,'reference_refs':[],'learning_ref':'','confirmed':True}
        direction=ops.direction_command(COMPANY,w,'save-direction',request_id='original',data=original)['record']
        data=context(c);data['items'][2]['direction_refs']=[direction['entity_id']]
        ctx=books.save(COMPANY,w,b,'direction-context','',data)
        command(service,w,b,c,'draft.saved',{'text':'她打开来信。','knowledge':[]})
        command(service,w,b,c,'context.bound',{'context_ref':ctx['ref'],'item_ids':['c1'],'confirmed':True})
        fixed=service.chapter(COMPANY,w,b,c)['draft']['book_context_basis']
        ops.direction_command(COMPANY,w,'save-direction',request_id='revised',expected_ref=direction['entity_id'],data={**original,'body':'新的方向'})
        state=service.chapter(COMPANY,w,b,c)
        assert state['draft']['book_context_basis']==fixed and state['book_context_status']['status']=='STALE'
        with pytest.raises(WritingConflict):command(service,w,b,c,'inspection.recorded',{'mode':'AUTHOR_MANUAL','checks':['continuity','language','rights'],'note':''})
