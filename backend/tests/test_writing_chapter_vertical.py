"""Real local Package/event mechanics; fixtures never imply Provider acceptance."""
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from app.database import Database
from app.conversation_service import ConversationService
from app.evolution_event_log import EvolutionEventLog
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.knowledge_service import KnowledgeService
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from app.workspace_package_runtime import WorkspacePackageRuntime, validate_package
from app.writing_chapter_service import WritingChapterService, WritingConflict, PACKAGE_DIGEST, sha, utf16_slice, encode

COMPANY = "writing-test-company"
CEO = "writing-test-author"
SOURCE = Path(__file__).resolve().parents[2] / "artifacts/tasks/CURIS-V1-DELIVERY-WRITING-001/package-source"


def scope(**overrides):
    return TenantContext.scope(**{"tenant_id": "selfuse", "company_id": COMPANY, "ceo_id": CEO, "role": "ceo", **overrides})


def setup(path):
    db = Database(str(path / "writing.sqlite")); db.initialize()
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse',?,'受控写作测试公司','active')", (COMPANY, CEO))
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) "
            "values ('writing-test-department','selfuse',?,'writing-test-template','受控测试部门','TEST','active')", (COMPANY,))
    with scope():
        assert validate_package(SOURCE)["digest"] == PACKAGE_DIGEST
        runtime = WorkspacePackageRuntime(db, path / "package-store")
        installed = runtime.install(SOURCE, COMPANY, department_id="writing-test-department", business_id="writing-test-business", business_name="受控本地写作验证")
        workspace = installed["instance"]["workspace_id"]
        book = runtime.create_object(workspace, "core.domain-object.create", "WritingBook", {"title": "原创测试作品", "status": "DRAFT"})["object_id"]
        chapter = runtime.create_object(workspace, "core.domain-object.create", "WritingChapter", {"title": "第一章", "bookRef": book, "status": "DRAFT"})["object_id"]
    return db, runtime, workspace, book, chapter


def command(service, workspace, book, chapter, action, data, *, request=None, base=None):
    if base is None: base = service.chapter(COMPANY, workspace, book, chapter)["draft"]["ref"]
    return service.command(COMPANY, workspace, book, chapter, action, request or action, base, data)


def local_chain(service, workspace, book, chapter):
    draft = command(service, workspace, book, chapter, "draft.saved", {"text": "雨停以后，书桌上的信仍未打开。\n她把灯挪近，看见陌生的邮戳。", "knowledge": []})
    inspection = command(service, workspace, book, chapter, "inspection.recorded", {"mode": "AUTHOR_MANUAL", "checks": ["continuity", "language", "rights"], "note": "作者逐项核对"})
    formal = command(service, workspace, book, chapter, "formal.confirmed", {"inspection_ref": inspection["ref"], "confirmed": True})
    package = command(service, workspace, book, chapter, "package.prepared", {"formal_ref": formal["ref"], "introduction": "一封雨后的信", "credits": "测试作者原创", "rights_declared": True, "target": "LOCAL_DOWNLOAD"})
    return draft, inspection, formal, package


def test_real_carrier_local_chain_immutable_download_cold_read(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db); draft, inspection, formal, package = local_chain(service, w, b, c)
        before, digest = service.download(COMPANY, w, b, c, package["ref"])
        assert sha(before.decode()) == digest
        command(service, w, b, c, "draft.saved", {"text": "后续草稿", "knowledge": []}, request="later")
        cold = WritingChapterService(Database(db.path))
        assert cold.download(COMPANY, w, b, c, package["ref"]) == (before, digest)
        assert formal["snapshot"] == draft["draft"] and inspection["independent_review"] is False
        assert json.loads(before)["external_publication"] == "NOT_PUBLISHED"
        assert json.loads(before)["package_ref"] == package["ref"]
        assert cold.chapter(COMPANY, w, b, c)["draft"]["text"] == "后续草稿"


@pytest.mark.parametrize("identity", [{"tenant_id": "other"}, {"company_id": "other"}, {"ceo_id": "other"}, {"role": "employee"}])
def test_scope_rejects_without_append(tmp_path, identity):
    db, _, w, b, c = setup(tmp_path)
    with scope(**identity), pytest.raises(RuntimeScopeError):
        WritingChapterService(db).command(COMPANY, w, b, c, "draft.saved", "no", "ABSENT", {"text": "不应保存", "knowledge": []})
    with db.connect() as con: assert con.execute("select count(*) from evolution_events where event_type like 'writing.chapter.%'").fetchone()[0] == 0


def test_parent_exact_instance_and_empty_identity(tmp_path):
    db, runtime, w, b, c = setup(tmp_path)
    with scope():
        other = runtime.create_object(w, "core.domain-object.create", "WritingBook", {"title": "另一本"})["object_id"]
        for book, chapter in [(other, c), (b, "missing"), ("", ""), (c, b)]:
            with pytest.raises(RuntimeScopeError): WritingChapterService(db).chapter(COMPANY, w, book, chapter)


def test_two_clients_cas_and_payload_equal_replay(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    def save(index):
        with scope():
            try: return WritingChapterService(Database(db.path)).command(COMPANY, w, b, c, "draft.saved", f"client-{index}", "ABSENT", {"text": str(index), "knowledge": []})
            except WritingConflict: return None
    with ThreadPoolExecutor(max_workers=2) as pool: results = list(pool.map(save, [0, 1]))
    assert sum(value is not None for value in results) == 1
    winner = next(index for index, value in enumerate(results) if value)
    with scope():
        service = WritingChapterService(db)
        assert service.command(COMPANY, w, b, c, "draft.saved", f"client-{winner}", "ABSENT", {"text": str(winner), "knowledge": []}) == results[winner]
        with pytest.raises(WritingConflict): service.command(COMPANY, w, b, c, "draft.saved", f"client-{winner}", "ABSENT", {"text": "不同内容", "knowledge": []})


def test_utf16_duplicate_paragraph_anchor_and_knowledge_stale(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        knowledge = KnowledgeService(db).create_entry(title="人物资料", body="角色原设定", company_id=COMPANY, target_type="WORKSPACE", target_ref=w)
        values = [{"ref": knowledge["id"], "sha256": knowledge["content_sha256"]}]
        service = WritingChapterService(db)
        draft = command(service, w, b, c, "draft.saved", {"text": "重复😀\n重复😀", "knowledge": values})["draft"]
        selection = {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 5, "end": 9, "excerpt": "重复😀", "anchor": draft["ref"] + ":5:9", "knowledge": values}
        with db.connect() as con: _, _, lineage, _ = service._scope(con, COMPANY, w, b, c)
        assert service._selection(draft, selection, lineage) == selection
        with pytest.raises(ValueError): utf16_slice(draft["text"], 2, 3)
        with pytest.raises(WritingConflict): service._selection(draft, {**selection, "anchor": "wrong"}, lineage)
        with db.connect() as con:
            con.execute("update knowledge_entries set body=?,content_sha256=? where id=?", ("角色设定已变化", sha("角色设定已变化"), knowledge["id"]))
        with pytest.raises(WritingConflict): service._selection(draft, selection, lineage)
        KnowledgeService(db).archive_entry(knowledge["id"], actor=CEO)
        with pytest.raises(RuntimeScopeError): service._selection(draft, selection, lineage)


def test_limits_manual_check_stale_and_atomic_append_rollback(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db)
        with pytest.raises(ValueError): command(service, w, b, c, "draft.saved", {"text": "文" * 200001, "knowledge": []})
        with pytest.raises(ValueError): command(service, w, b, c, "draft.saved", {"text": "x" * 190000, "knowledge": [], "padding": "x" * 1000000})
        draft, check, _, _ = local_chain(service, w, b, c)
        command(service, w, b, c, "draft.saved", {"text": "更新后未检查", "knowledge": []}, request="later")
        with pytest.raises(WritingConflict): command(service, w, b, c, "formal.confirmed", {"inspection_ref": check["ref"], "confirmed": True}, request="stale")
        with db.connect() as con:
            before = con.execute("select count(*) from evolution_events").fetchone()[0]
            con.execute("create trigger writing_test_failure before insert on evolution_events when new.event_type='writing.chapter.draft.saved' begin select raise(abort,'controlled append failure'); end")
        with pytest.raises(Exception, match="controlled append failure"): command(service, w, b, c, "draft.saved", {"text": "不能留下半次保存", "knowledge": []}, request="rollback")
        with db.connect() as con: assert con.execute("select count(*) from evolution_events").fetchone()[0] == before
        assert service.chapter(COMPANY, w, b, c)["draft"]["text"] == "更新后未检查"


def test_disable_uninstall_retains_domain_events_and_download(tmp_path):
    db, runtime, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db); _, _, _, package = local_chain(service, w, b, c)
        before = encode(service.chapter(COMPANY, w, b, c)["events"]); payload = service.download(COMPANY, w, b, c, package["ref"])
        runtime.disable(w)
        with pytest.raises(WritingConflict): command(service, w, b, c, "draft.saved", {"text": "不可再写", "knowledge": []}, request="disabled")
        runtime.uninstall(w)
        cold = WritingChapterService(Database(db.path))
        assert sha(encode(cold.chapter(COMPANY, w, b, c)["events"])) == sha(before)
        assert cold.download(COMPANY, w, b, c, package["ref"]) == payload


def test_unverified_candidate_work_result_and_execution_unavailable(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db); local_chain(service, w, b, c)
        state = service.chapter(COMPANY, w, b, c)
        assert state["responsibility"]["status"] == state["business_result"]["status"] == "UNAVAILABLE"
        with pytest.raises(RuntimeScopeError): command(service, w, b, c, "candidate.recorded", {"binding_ref": "fake", "message_ref": "fake", "reply_start": 0, "reply_end": 1, "reply_excerpt": "伪"})
        with pytest.raises(RuntimeScopeError): command(service, w, b, c, "work.linked", {"work_ref": "fake", "basis_draft_ref": state["draft"]["ref"], "basis_sha256": state["draft"]["sha256"]})
        with pytest.raises(WritingConflict): service.prepare_message(COMPANY, w, b, c, binding_ref="fake", body="保留输入", request_id="no-model")


def team(db, w):
    db.save_tenant_private_capability(tenant_id="selfuse", capability_type="model", capability_id="writing.controlled.model", display_name="受控测试模型", metadata={"testOnly": True})
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) values ('writing-test-employee','selfuse',?,'writing-test-department','et_product_manager','受控测试员工','写作测试','idle')", (COMPANY,))
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('writing-test-binding','selfuse','writing-test-employee','tenant_private','model','writing.controlled.model')")
    foundation = RuntimeFoundation(db)
    role = foundation.create("ROLE_SLOT", company_id=COMPANY, workspace_id=w, data={"name": "受控写作责任"})
    employee = foundation.create("AI_EMPLOYEE", company_id=COMPANY, workspace_id=w, lifecycle_status="AVAILABLE", data={"name": "受控测试员工"})
    assignment = ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY, workspace_id=w, scope_type="WORKSPACE", scope_ref=w,
        role_ref=role["entity_id"], employee_ref=employee["entity_id"], responsibility_key="WRITING_CHAPTER_AUTHOR", responsibility="仅验证章节回复来源", output_contract={"requiresResult": False})
    EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=w, runtime_employee_ref=employee["entity_id"], company_employee_ref="writing-test-employee", employee_capability_binding_ref="writing-test-binding")
    return employee["entity_id"], assignment["entity_id"]


def test_legacy_execution_flag_cannot_authorize_professional_reply(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        employee, assignment = team(db, w)
        conversations = ConversationService(db)
        service = WritingChapterService(db, conversation_service=conversations, allow_execution=True)
        draft = command(service, w, b, c, "draft.saved", {"text": "旧句😀\n旧句😀", "knowledge": []})["draft"]
        selection = {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 5, "end": 9, "excerpt": "旧句😀", "anchor": draft["ref"] + ":5:9", "knowledge": []}
        topic = conversations.create(COMPANY, request_id="controlled-writing-topic", employee_ref=employee)
        with pytest.raises(WritingConflict):
            command(service, w, b, c, "discussion.bound", {"selection": selection, "assignment_ref": assignment, "conversation_ref": topic["conversation_id"]})
        assert conversations.read(COMPANY, conversation_id=topic["conversation_id"])["attempts"] == []
        with db.connect() as con:
            assert con.execute("select count(*) from tasks").fetchone()[0] == 0


def test_candidate_cannot_be_adopted_into_another_chapter(tmp_path):
    db, runtime, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db)
        draft = command(service, w, b, c, "draft.saved", {"text": "原章节正文", "knowledge": []})["draft"]
        selection = {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 0, "end": 3,
                     "excerpt": "原章节", "anchor": draft["ref"] + ":0:3", "knowledge": []}
        candidate = command(service, w, b, c, "candidate.manual-recorded", {"selection": selection, "replacement": "新的章节"})
        other = runtime.create_object(w, "core.domain-object.create", "WritingChapter", {"title": "第二章", "bookRef": b, "status": "DRAFT"})["object_id"]
        command(service, w, b, other, "draft.saved", {"text": "另一章正文", "knowledge": []})
        with pytest.raises(RuntimeScopeError):
            command(service, w, b, other, "candidate.adopted", {"candidate_ref": candidate["ref"], "confirmed": True})
        assert service.chapter(COMPANY, w, b, other)["draft"]["text"] == "另一章正文"
        assert service.chapter(COMPANY, w, b, c)["draft"]["text"] == "原章节正文"


def test_model_work_adoption_failure_rolls_back_chapter_and_acceptance(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from backend.tests.test_writing_selected_execution import ready, explicit_work
    from app.runtime.child_work import CanonicalChildWorkRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        response = client.post(root + "/messages", headers=headers, json={"binding_ref": binding["ref"],
            "body": "明确交办", "request_id": "adopt-rollback", "model_key": "model.writing-entry", "work_ref": work})
        assert response.status_code == 202, response.text
        reply = client.get(root + "/discussion/" + binding["ref"], headers=headers).json()["messages"][-1]
    with scope():
        before = service.chapter(COMPANY, w, b, c)["draft"]
        text = reply["body"]
        candidate = command(service, w, b, c, "candidate.recorded", {"binding_ref": binding["ref"],
            "message_ref": reply["message_id"], "reply_start": 0, "reply_end": len(text.encode("utf-16-le")) // 2, "reply_excerpt": text})
        original = CanonicalChildWorkRuntime.complete_work
        def interrupted(self, *args, **kwargs):
            original(self, *args, **kwargs)
            raise RuntimeError("synthetic failure after Work completion")
        monkeypatch.setattr(CanonicalChildWorkRuntime, "complete_work", interrupted)
        with pytest.raises(RuntimeError, match="synthetic failure"):
            command(service, w, b, c, "candidate.adopted", {"candidate_ref": candidate["ref"], "confirmed": True})
        assert service.chapter(COMPANY, w, b, c)["draft"] == before
        assert RuntimeFoundation(db).get(work)["lifecycle_status"] == "ACTIVE"
        with db.connect() as con:
            assert con.execute("select count(*) from runtime_entities where parent_id=? and entity_type in ('ACCEPTANCE','EVIDENCE')", (work,)).fetchone()[0] == 0
            assert con.execute("select count(*) from evolution_events where event_type='writing.chapter.candidate.adopted'").fetchone()[0] == 0
    assert len(calls) == 1


def test_author_check_without_accepted_work_is_not_a_followup_basis(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        service = WritingChapterService(db)
        _, inspection, _, _ = local_chain(service, w, b, c)
        state = service.chapter(COMPANY, w, b, c)
        with db.connect() as con:
            before = con.execute('select count(*) from evolution_events').fetchone()[0]
            with pytest.raises(WritingConflict, match='已明确采用的 Work 当前版本'):
                service.review_work_basis(con, state['scope'], state['draft'], inspection['ref'])
            assert con.execute('select count(*) from evolution_events').fetchone()[0] == before
            assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
