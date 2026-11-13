"""Canonical ordinary conversation with real Task/Usage persistence and injected HTTP only."""
from fastapi.testclient import TestClient
import pytest
from app.company_execution_policy import CompanyExecutionPolicy, RESERVE_MICRO_CNY
from backend.tests.test_company_execution_policy import policy_ready, consent, HEADERS, KEY
from backend.tests.test_writing_chapter_vertical import scope, COMPANY

_LONG_PROBLEM = ("Review the saved original selection and its evidence. Keep the original work and source boundaries. " * 5)[:347] + " ORIGINAL-PROBLEM-END!!"
_LONG_EXPECTED = ("Return complete suggestions and scoped sources without changing the original artifact. " * 20)[:1585] + " EXPECTED-END!!"
_LONG_SELECTION = ("雨后的街道安静下来，来信仍放在书桌上，原文和依据应完整保留。" * 6)[:144]
assert len(_LONG_PROBLEM) == 370 and len(_LONG_EXPECTED) == 1600 and len(_LONG_SELECTION) == 144


def _agent_professional_source(direction, db, app, tmp_path, long_input=False):
    from app.workspace_package_runtime import WorkspacePackageRuntime
    from app.music_entry_service import ASSETS
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
    from app.employee_execution_identity import EmployeeExecutionIdentity
    runtime = WorkspacePackageRuntime(db, tmp_path / "agent-extra-store")
    with scope():
        installed = runtime.install(ASSETS / ("writing_authoring" if direction == "writing" else "music"),
            COMPANY, department_id="cg-dept", business_id=direction + "-agent-business", business_name="隔离Agent链")
        workspace = installed["instance"]["workspace_id"]
        if direction == "writing":
            entry = app.state.writing_entry_service
            entry.assign(COMPANY, workspace, "cg-employee", entry.metadata(COMPANY, workspace)["assignment_revision"])
            with db.connect() as con:
                assignment = entry.assignments(con, COMPANY, workspace)[0]
            from app.writing_chapter_service import WritingChapterService
            service = WritingChapterService(db)
            book = runtime.create_object(workspace, "core.domain-object.create", "WritingBook", {"title": "原作品", "status": "DRAFT"})["object_id"]
            chapter = runtime.create_object(workspace, "core.domain-object.create", "WritingChapter",
                {"title": "原章节", "bookRef": book, "status": "DRAFT"})["object_id"]
            service.command(COMPANY, workspace, book, chapter, "draft.saved", "agent-initial", "ABSENT",
                {"text": _LONG_SELECTION if long_input else "原来的正文。", "knowledge": []})
            if long_input:
                from app.writing_book_service import WritingBookService
                from backend.tests.test_writing_book_context import context as book_context
                books = WritingBookService(db, chapters=service)
                current = service.chapter(COMPANY, workspace, book, chapter)["draft"]
                saved_context = books.save(COMPANY, workspace, book, "long-context", "", book_context(chapter))
                service.command(COMPANY, workspace, book, chapter, "context.bound", "long-basis", current["ref"],
                    {"context_ref": saved_context["ref"], "item_ids": ["c1"], "confirmed": True})
            draft = service.chapter(COMPANY, workspace, book, chapter)["draft"]
            source = {"kind": direction, "book_ref": book, "chapter_ref": chapter, "expected_draft_ref": draft["ref"],
                "selection": {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 0, "end": 144 if long_input else 1,
                              "excerpt": _LONG_SELECTION if long_input else "原",
                              "anchor": draft["ref"] + (":0:144" if long_input else ":0:1"), "knowledge": []}}
            if long_input:
                assert len(draft["book_context_basis"]["items"]) == 5
        else:
            foundation = RuntimeFoundation(db)
            role = foundation.create("ROLE_SLOT", company_id=COMPANY, workspace_id=workspace, data={"name": "歌曲作者"})
            employee = foundation.create("AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace,
                lifecycle_status="AVAILABLE", data={"name": "原歌曲员工"})
            assignment = ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY, workspace_id=workspace,
                scope_type="WORKSPACE", scope_ref=workspace, role_ref=role["entity_id"], employee_ref=employee["entity_id"],
                responsibility_key="MUSIC_SONG_AUTHOR", responsibility="核验原歌词并提供建议", output_contract={"requiresResult": True})
            EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=workspace,
                runtime_employee_ref=employee["entity_id"], company_employee_ref="cg-employee",
                employee_capability_binding_ref="cg-model-binding")
            from backend.tests.test_music_canonical_entry import data, basis, lyrics_selection
            values = data()
            if long_input:
                values["lyrics"] = _LONG_SELECTION
            song = app.state.music_service.command(COMPANY, workspace, "", "create", request_id="agent-song", data=values)
            selected = ({"kind": "lyrics", "version_ref": song["lyrics"]["entity_id"],
                         "draft_revision": song["lyrics"]["data"]["draft_revision"],
                         "start": 0, "end": 144, "excerpt": _LONG_SELECTION, "locator": "lyrics"}
                        if long_input else lyrics_selection(song))
            source = {"kind": direction, "song_ref": song["song"]["entity_id"], "expected": basis(song),
                      "selection": selected, "references": []}
    return workspace, {"context": {"assignment_ref": assignment["entity_id"],
                                  "employee_ref": assignment["data"]["employeeRef"]}}, source


@pytest.mark.parametrize("long_input", [False, True])
@pytest.mark.parametrize("stale_workflow", [False, True])
@pytest.mark.parametrize("closed_cycle", [False, True])
@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
def test_original_agent_work_persists_task_usage_files_and_explicit_candidate(tmp_path, monkeypatch, closed_cycle, direction, stale_workflow, long_input, file_mode="single", candidate_check=None, browser_check=None, trusted_fixture=False, tamper_before_launch=False):
    import json
    import os
    from pathlib import Path
    from types import SimpleNamespace
    from app.employee_execution_identity import EmployeeExecutionIdentity
    import app.agent_executor_dispatch as dispatch
    import app.agent_adapter as agent_adapter
    monkeypatch.setattr(agent_adapter, "require_codex_execution_available", lambda: None)
    monkeypatch.setenv("CURIS_AGENT_TMP_ROOT", os.environ["CURIS_TEST_ROOT"])
    if trusted_fixture:
        # The fixture exercises gateway authorization without the separate
        # Workspace startup/catalog probe, which uses SQLite URI access.
        monkeypatch.delenv("CURIS_PRODUCT", raising=False)
        monkeypatch.setenv("CURIS_ENV", "test")
        monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
        monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "https://fixture-issuer.example")
        monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "127.0.0.1/32")
        monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "fixture-audit-key")
        monkeypatch.setitem(HEADERS, "X-Curis-Gateway-Subject", "fixture-subject")
        monkeypatch.setitem(HEADERS, "X-Curis-Gateway-Issuer", "https://fixture-issuer.example")
        monkeypatch.setitem(HEADERS, "X-Curis-Gateway-Auth-Time", "1720000000")
    db, app, _, content_service, model_calls, workspace, row, binding, payload = policy_ready(tmp_path, monkeypatch)
    if trusted_fixture:
        with db.connect() as connection:
            connection.execute("insert into tenant_memberships "
                "(membership_id,issuer,subject_id,tenant_id,company_id,ceo_id,role,status) "
                "values (?,?,?,?,?,?,?,?)", ("fixture-membership", "https://fixture-issuer.example",
                "fixture-subject", "selfuse", COMPANY, HEADERS["X-Ceo-Id"], "owner", "active"))
    if long_input and direction == "content-growth":
        from backend.tests.test_cg_content_entry import data as content_data
        with scope():
            row = content_service.command(COMPANY, workspace, row["content"]["entity_id"], "save",
                request_id="long-original", expected_version_ref=row["version"]["entity_id"], data=content_data(_LONG_SELECTION))
        payload["selection"] = {"version_ref": row["version"]["entity_id"], "start": 0, "end": 144,
                                "excerpt": _LONG_SELECTION, "locator": "body"}
    source = {"kind": "content-growth", "content_ref": row["content"]["entity_id"],
              "expected_version_ref": row["version"]["entity_id"], "selection": payload["selection"],
              "references": payload["references"]}
    if direction != "content-growth":
        workspace, binding, source = _agent_professional_source(direction, db, app, tmp_path, long_input=long_input)
    problem = _LONG_PROBLEM if long_input else "处理已选原文"
    expected_result = _LONG_EXPECTED if long_input else "建议与来源文件"
    if long_input:
        assert source["selection"]["excerpt"] == _LONG_SELECTION
    assignment = binding["context"]["assignment_ref"]
    called = []
    tamper_checkpoints = []
    file_payloads = [("sources.csv", "source,value\nfixture,1\n")]
    if file_mode in {"multiple", "unicode"}:
        file_payloads = [("revision-notes.md", _FILE_NOTES), ("chapter-candidate.md", _FILE_BODY + ("😀尾" if file_mode == "unicode" else ""))]
    elif file_mode == "binary":
        file_payloads = [("sources.csv", b"\xff\xfe")]
    elif file_mode == "oversize":
        file_payloads = [("sources.csv", "x" * 200001)]
    elif file_mode == "none":
        file_payloads = []
    with scope():
        from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
        original_assignment = RuntimeFoundation(db).get(assignment)
        data = original_assignment["data"]
        identity = EmployeeExecutionIdentity(db).resolve(company_id=COMPANY, workspace_id=workspace,
            runtime_employee_ref=binding["context"]["employee_ref"])
        db.save_tenant_private_capability(tenant_id="selfuse", capability_type="agent", capability_id="agent.fixture",
            display_name="Offline original Agent", metadata={"kind": "codex-cli", "computer_access_intent": "ASK_WHEN_NEEDED"})
        with db.connect() as con:
            con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_type,capability_source,capability_id) "
                        "values ('agent-fixture-binding','selfuse',?,'agent','tenant_private','agent.fixture')",
                        (identity["company_employee_ref"],))
        CompanyExecutionPolicy(db).save_agent_allowance(COMPANY, request_id="fixture-grant", expected_revision="",
            enabled=True, consent=True, binding_refs=["agent-fixture-binding"])
    def factory(metadata, **kwargs):
        context = kwargs["execution_context"]
        def execute(prompt):
            if long_input and not called:
                assert problem in prompt and expected_result in prompt and _LONG_SELECTION in prompt
            if tamper_before_launch and called:
                if tamper_before_launch is True or tamper_before_launch == "deleted":
                    from app.agent_work_resources import AgentWorkResources
                    resources = AgentWorkResources(Path(db.path).absolute().parent / "agent-work", tenant_id="selfuse",
                        company_id=COMPANY, work_ref=root_work, task_id=task)
                    source_file = resources.path / "output" / "sources.csv"
                    if tamper_before_launch == "deleted":
                        source_file.unlink()
                    else:
                        source_file.write_text("changed synthetic file")
                elif tamper_before_launch == "scope":
                    with db.connect() as con:
                        changed_rows = con.execute("update artifacts set tenant_id = ? where task_id = ? and artifact_type = ?",
                            ("foreign-synthetic-tenant", task, "agent_file_receipt"))
                        assert changed_rows.rowcount == 1
                else:
                    with db.connect() as con:
                        row = con.execute("select data_json from runtime_entities where tenant_id = ? and entity_id = ?", ("selfuse", work)).fetchone()
                        changed = json.loads(row[0])
                        if tamper_before_launch == "predecessor":
                            changed.pop("predecessorWorkRef")
                        else:
                            changed["followupContract"].pop("agentBinding")
                        con.execute("update runtime_entities set data_json = ? where tenant_id = ? and entity_id = ?", (json.dumps(changed), "selfuse", work))
            if tamper_before_launch and called:
                tamper_checkpoints.append("mutation-complete-and-callback-entered")
            try:
                context["before_launch"]()
            except Exception as error:
                if tamper_before_launch == "deleted":
                    assert isinstance(error.__cause__, FileNotFoundError)
                    tamper_checkpoints.append("missing-file-rejected")
                elif tamper_before_launch == "scope":
                    from app.runtime import RuntimeScopeError
                    assert isinstance(error.__cause__, RuntimeScopeError)
                    assert str(error.__cause__) == "原执行附件回执缺失、重复或不属于本次执行。"
                    tamper_checkpoints.append("foreign-receipt-rejected")
                raise
            called.append(prompt)
            tool_headers = {"Authorization": "Bearer " + context["environment"]["CURIS_AGENT_TOOL_TOKEN"]}
            for index, (name, body) in enumerate(file_payloads):
                rpc = {"jsonrpc": "2.0", "id": index + 1, "method": "tools/call",
                       "params": {"name": "write_output", "arguments": {"name": name,
                           "encoding": "base64" if isinstance(body, bytes) else "utf8",
                           "content": __import__("base64").b64encode(body).decode() if isinstance(body, bytes) else body}}}
                denied = client.post("/api/workspace/agent-tools", headers={**tool_headers, "X-Tenant-Id": "foreign"}, json=rpc)
                assert denied.status_code == 403
                written = client.post("/api/workspace/agent-tools", headers=tool_headers, json=rpc)
                assert written.status_code == 200 and not written.json()["result"]["isError"], written.text
            progress = client.get(root + f"/works/{work}", headers=HEADERS)
            assert progress.status_code == 200 and progress.json()["work"]["entity_id"] == work
            return {"output": json.dumps({"status": "ACCEPTED", "summary": "原工作建议文字", "resultType": "content-candidate",
                    "problem": "", "deliverable": {"kind": "TEXT", "content": "原工作建议文字"}}),
                    "status": "success", "outbound_attempted": True, "cost": 0, "estimated_cost": 0,
                    "ledger_cost_source": "unknown", "metering_status": "unknown", "provider_id": "openai_codex",
                    "model_gateway_id": "codex-cli", "model_name": "agent.fixture", "session_id": f"fixture-session-{len(called)}",
                    "http_status": 200, "latency_ms": 1}
        return SimpleNamespace(execute=execute)
    monkeypatch.setattr(dispatch, "build_agent_executor", factory)
    root = "/api/workspace/runtime/foundation/team-operating"
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        workflow_path = root + f"/assignments/{assignment}/agent-workflow"
        reviewed = client.get(workflow_path, headers=HEADERS,
            params={"company_id": COMPANY, "workspace_id": workspace})
        assert reviewed.status_code == 200, reviewed.text
        basis = reviewed.json()
        if basis["state"] == "NEEDS_PUBLICATION":
            published = client.post(workflow_path, headers=HEADERS, json={
                "company_id": COMPANY, "workspace_id": workspace,
                "expected_revision": basis["assignment_revision"],
                "review_token": basis["review_token"], "confirm": True})
            assert published.status_code == 200 and published.json()["state"] == "READY", published.text
        else:
            assert basis["state"] == "READY", basis
        with scope():
            assert RuntimeFoundation(db).get(assignment) == original_assignment
            assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 0
        assert called == [] and model_calls == []
        with scope():
            before_works = RuntimeFoundation(db).list("WORK", company_id=COMPANY, workspace_id=workspace)
            before_cycles = RuntimeFoundation(db).list("CYCLE", company_id=COMPANY, workspace_id=workspace)
            if stale_workflow:
                ResponsibilityRoutingRuntime(db).update_assignment(assignment, responsibility="核对后已修改的责任")
        created = client.post(root + f"/assignments/{assignment}/work", headers=HEADERS,
            json={"request_id": "explicit-original-request", "problem": problem, "expected_result": expected_result,
                  "agent_binding_ref": "agent-fixture-binding", "source": source})
        if stale_workflow:
            assert created.status_code == 422, created.text
            with scope():
                assert RuntimeFoundation(db).list("WORK", company_id=COMPANY, workspace_id=workspace) == before_works
                assert RuntimeFoundation(db).list("CYCLE", company_id=COMPANY, workspace_id=workspace) == before_cycles
                assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 0
            assert called == [] and model_calls == []
            return
        assert created.status_code == 200, created.text
        work = created.json()["work"]["entity_id"]
        with scope():
            cycle_ref = RuntimeFoundation(db).get(work)["data"]["cycleRef"]
            original_contract = RuntimeFoundation(db).get(cycle_ref)["data"]["contract"]
            assert original_contract["problem"] == problem and original_contract["expectedResult"] == expected_result
            assert original_contract["agentSource"]["input"] == source
        if long_input:
            # Corrupt only this fresh fixture's saved source scope; no product guard is mocked.
            with db.connect() as con:
                original_cycle_json = con.execute("select data_json from runtime_entities where entity_id=?", (cycle_ref,)).fetchone()[0]
                invalid = json.loads(original_cycle_json)
                snapshot = invalid["contract"]["agentSource"]["snapshot"]
                snapshot["scope"] = {**snapshot.get("scope", {}), "company_id": "foreign-company"}
                con.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(invalid), cycle_ref))
            try:
                denied = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
                assert denied.status_code == 422 and called == [] and model_calls == [], denied.text
                same = client.get(root + f"/works/{work}", headers=HEADERS).json()
                assert same["work"]["entity_id"] == work and same["tasks"] == []
                with scope():
                    assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 0
            finally:
                with db.connect() as con:
                    con.execute("update runtime_entities set data_json=? where entity_id=?", (original_cycle_json, cycle_ref))
        if browser_check is not None:
            browser_check(locals())
            return
        outcome = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert outcome.status_code == 200, outcome.text
        original = client.get(root + f"/works/{work}", headers=HEADERS)
        assert original.status_code == 200, original.text
        tasks = original.json()["tasks"]
        assert len(tasks) == 1 and tasks[0]["status"] == "COMPLETED", original.text
        assert len(called) == 1 and model_calls == []
        with scope():
            assert RuntimeFoundation(db).get(cycle_ref)["data"]["contract"] == original_contract
            assert len(RuntimeFoundation(db).list("WORK", company_id=COMPANY, workspace_id=workspace)) == len(before_works) + 1
            assert len(RuntimeFoundation(db).list("CYCLE", company_id=COMPANY, workspace_id=workspace)) == len(before_cycles) + 1
        task = tasks[0]["task_id"]
        with db.connect() as con:
            file_rows = con.execute("select * from artifacts where task_id=? and artifact_type='agent_file_receipt' order by created_at", (task,)).fetchall()
        chosen = next((r for r in file_rows if r["title"] == ("chapter-candidate.md" if file_mode in {"multiple", "unicode"} else "sources.csv")), None)
        selection_query = {"artifact_ref": chosen["artifact_id"]} if chosen else {}
        preview = client.get(root + f"/works/{work}/candidate-source/{task}", headers=HEADERS, params=selection_query)
        if file_mode in {"binary", "oversize"}:
            assert preview.status_code == 422, preview.text
            assert len(called) == 1 and model_calls == []
            return
        assert preview.status_code == 200, preview.text
        text = preview.json()["text"]
        if file_mode in {"multiple", "unicode"}:
            assert text == _FILE_BODY + ("😀尾" if file_mode == "unicode" else ""), "selected file body must never be replaced by the completion summary or notes"
        selected = {"task_ref": task, "start": 0, "end": len(text.encode("utf-16-le")) // 2,
                    "excerpt": text, "text_sha256": preview.json()["text_sha256"]}
        if chosen:
            selected.update({k: preview.json()[k] for k in ("artifact_ref", "artifact_content_sha256", "file_sha256", "task_output_sha256") if preview.json().get(k) is not None})
        if candidate_check:
            candidate_check("before", locals())
        candidate = client.post(root + f"/works/{work}/candidate", headers=HEADERS, json=selected)
        assert candidate.status_code == 200, candidate.text
        duplicate = client.post(root + f"/works/{work}/candidate", headers=HEADERS, json=selected)
        assert duplicate.status_code == 200 and duplicate.json() == candidate.json()
        replay = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert replay.status_code == 422 and len(called) == 1
        with db.connect() as con:
            rows = con.execute("select artifact_id from artifacts where task_id=? and artifact_type='agent_file_receipt'", (task,)).fetchall()
            assert len(rows) == len(file_payloads)
            usage_events = con.execute("select payload from evolution_events where tenant_id='selfuse' "
                "and correlation_id=? and event_type='usage.task_execution'", (task,)).fetchall()
            assert len(usage_events) == 1
            assert json.loads(usage_events[0]["payload"])["agent_authorization_ref"] == "curis-existing-codex-allowance-v1"
        if rows:
            download = client.get(root + f"/works/{work}/files/{chosen['artifact_id']}", headers=HEADERS)
            assert download.status_code == 200, download.text
        if candidate_check:
            candidate_check("after", locals())
            return
        with db.connect() as con:
            prior_event_id = con.execute("select coalesce(max(event_id), 0) from evolution_events").fetchone()[0]
        root_work = work
        with scope():
            foundation = RuntimeFoundation(db)
            parent = foundation.get(work)
            cycle = foundation.get(parent["data"]["cycleRef"])
            if closed_cycle:
                # The existing Work was explicitly accepted before its Cycle closed.
                from app.conversation_service import ConversationService
                from app.runtime.child_work import CanonicalChildWorkRuntime
                service = ConversationService(db)
                proof = service.agent_result_proof(COMPANY, root_work, task)
                acceptance_proof = service.agent_acceptance_evidence(COMPANY, root_work, proof)
                with db.connect() as con:
                    con.execute("begin immediate")
                    CanonicalChildWorkRuntime(db)._accept_agent_result_locked(con, parent,
                        "task:" + task, acceptance_proof, "prior-explicit-human-acceptance")
                parent = foundation.get(root_work)
                with db.connect() as con:
                    con.execute("update runtime_entities set lifecycle_status='CLOSED' where tenant_id='selfuse' and entity_id=?",
                        (cycle["entity_id"],))
                cycle = foundation.get(cycle["entity_id"])
        followup = {"request_id": "explicit-linked-followup", "problem": "在原工作基础上补充一个建议",
                    "expected_result": "补充建议与来源", "accepted_task_ref": task, "accept_result": True, "source": source,
                    "prior_result": {"mode": "file" if chosen else "result", "start": selected["start"], "end": selected["end"],
                        **{k: preview.json()[k] for k in ("text_sha256", "task_output_sha256", "artifact_ref", "artifact_content_sha256", "file_sha256") if preview.json().get(k) is not None}}}
        expected_prior = text
        if file_mode == "unicode":
            start = len(text[:text.index("😀")].encode("utf-16-le")) // 2
            followup["prior_result"].update(start=start, end=start + 2)
            expected_prior = "😀"
        cold = client.get(root + f"/works/{root_work}", headers=HEADERS)
        assert cold.status_code == 200 and len(called) == 1
        wrong_basis = {**followup["prior_result"], "text_sha256": "0" * 64}
        bad_requests = [{k: v for k, v in followup.items() if k != "prior_result"},
                        {**followup, "prior_result": wrong_basis},
                        {**followup, "accepted_task_ref": "foreign-task"},
                        {**followup, "prior_result": {**followup["prior_result"], "end": 200000}}]
        if chosen:
            bad_requests += [{**followup, "prior_result": {**followup["prior_result"], "artifact_ref": "foreign-file"}},
                             {**followup, "prior_result": {"mode": "result", "start": 0, "end": selected["end"],
                                 "text_sha256": selected["text_sha256"], "task_output_sha256": preview.json()["task_output_sha256"]}}]
        for bad in bad_requests:
            assert client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS, json=bad).status_code == 422
            assert len(called) == 1
        rejected = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS,
            json={**followup, "accept_result": False})
        assert rejected.status_code == 422
        for bad_receipt in (("missing", "tampered", "foreign") if rows else ()):
            with db.connect() as con:
                receipt = dict(con.execute("select * from artifacts where artifact_id=?", (rows[0]["artifact_id"],)).fetchone())
                if bad_receipt == "missing":
                    con.execute("update artifacts set artifact_type='unknown' where artifact_id=?", (receipt["artifact_id"],))
                elif bad_receipt == "tampered":
                    con.execute("update artifacts set content_sha256='wrong' where artifact_id=?", (receipt["artifact_id"],))
                else:
                    import hashlib
                    changed = json.loads(receipt["content"]); changed["tenant_id"] = "foreign"
                    content = json.dumps(changed)
                    con.execute("update artifacts set content=?,content_sha256=? where artifact_id=?",
                        (content, hashlib.sha256(content.encode()).hexdigest(), receipt["artifact_id"]))
            denied = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS, json=followup)
            assert denied.status_code == 422 and len(called) == 1, denied.text
            with db.connect() as con:
                con.execute("update artifacts set artifact_type=?,content=?,content_sha256=? where artifact_id=?",
                    (receipt["artifact_type"], receipt["content"], receipt["content_sha256"], receipt["artifact_id"]))
            with scope():
                assert foundation.get(root_work) == parent
        from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
        with db.connect() as con:
            counts_before = dict(con.execute("select entity_type,count(*) from runtime_entities group by entity_type").fetchall())
        def fail_after_parent_acceptance(_runtime, con, **_arguments):
            assert con.execute("select lifecycle_status from runtime_entities where entity_id=?", (root_work,)).fetchone()[0] == "COMPLETED"
            assert con.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE' and parent_id=?",
                (root_work,)).fetchone()[0] == 1
            raise ChildWorkError("injected after human acceptance and before child insert")
        with monkeypatch.context() as patch:
            patch.setattr(CanonicalChildWorkRuntime, "_create_work_locked", fail_after_parent_acceptance)
            interrupted = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS, json=followup)
        assert interrupted.status_code == 422 and "injected after human acceptance" in interrupted.text
        with db.connect() as con:
            assert dict(con.execute("select entity_type,count(*) from runtime_entities group by entity_type").fetchall()) == counts_before
        with scope():
            assert foundation.get(root_work) == parent
        assert len(called) == 1
        released = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS, json=followup)
        assert released.status_code == 200, released.text
        work = released.json()["work"]["entity_id"]
        assert work != root_work and len(called) == 1
        with scope():
            accepted_parent = foundation.get(root_work)
            assert accepted_parent["lifecycle_status"] == "COMPLETED"
            assert accepted_parent["data"]["responsibilityRouting"] == parent["data"]["responsibilityRouting"]
            acceptance = foundation.get(accepted_parent["data"]["acceptanceRefs"][0])
            evidence = foundation.get(accepted_parent["data"]["evidenceRefs"][0])
            assert acceptance["lifecycle_status"] == "CLOSED" and acceptance["data"]["contentVerification"] == "UNVERIFIED"
            assert evidence["data"]["file_receipt_count"] == len(file_payloads) and evidence["data"]["content_verification"] == "UNVERIFIED"
        repeated = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS, json=followup)
        assert repeated.status_code == 200 and repeated.json()["work"]["entity_id"] == work, repeated.text
        conflict = client.post(root + f"/works/{root_work}/follow-up", headers=HEADERS,
            json={**followup, "problem": "same key changed intent"})
        assert conflict.status_code == 422 and len(called) == 1
        with scope():
            child = foundation.get(work)
            assert child["data"]["rootWorkRef"] == root_work
            assert child["data"]["predecessorWorkRef"] == root_work
            assert (child["data"]["cycleRef"] != cycle["entity_id"]) == closed_cycle
            assert foundation.get(root_work) == accepted_parent
            assert foundation.get(cycle["entity_id"]) == cycle
        cold_read = client.get(root + f"/works/{root_work}", headers=HEADERS)
        assert cold_read.status_code == 200 and cold_read.json()["work"]["entity_id"] == work
        assert len(cold_read.json()["history"]) == 2 and len(called) == 1
        continued = client.post(root + f"/works/{work}/execute", headers=HEADERS)
        if tamper_before_launch:
            assert len(called) == 1, continued.text
            expected_checkpoint = {"deleted": "missing-file-rejected", "scope": "foreign-receipt-rejected"}.get(tamper_before_launch)
            assert tamper_checkpoints == ["mutation-complete-and-callback-entered"] + ([expected_checkpoint] if expected_checkpoint else [])
            with scope():
                assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 1
                assert foundation.get(root_work) == accepted_parent
            return
        assert continued.status_code == 200 and len(called) == 2, continued.text
        context_line = next(line for line in called[-1].splitlines() if line.startswith("业务上下文："))
        actual_context = json.loads(context_line.removeprefix("业务上下文："))
        assert "priorResult" not in actual_context["work"]
        prior_line = next(line for line in called[-1].splitlines() if line.startswith("用户明确选择的上次成果（内容未验证）："))
        actual_prior = json.loads(prior_line.removeprefix("用户明确选择的上次成果（内容未验证）："))
        assert actual_prior["text"] == expected_prior
        assert actual_prior["content_verification"] == "UNVERIFIED"
        assert actual_context["work"]["problem"] == followup["problem"]
        if file_mode in {"multiple", "unicode"}:
            assert _FILE_NOTES not in called[-1]
        current = client.get(root + f"/works/{root_work}", headers=HEADERS).json()
        assert current["tasks"][0]["status"] == "COMPLETED", current
        assert current["tasks"][0]["task_id"] != task and current["history"][0]["tasks"][0]["task_id"] == task
        if file_mode == "multiple":
            with db.connect() as con:
                stored = con.execute("select content, prompt, output from tasks where task_id = ?", (current["tasks"][0]["task_id"],)).fetchone()
                sentinels = (expected_prior, json.dumps(expected_prior, ensure_ascii=False)[1:-1])
                assert all(sentinel not in (value or "") for sentinel in sentinels for value in stored)
                events = con.execute("select payload from evolution_events where event_id > ?", (prior_event_id,)).fetchall()
                assert all(sentinel not in event[0] for sentinel in sentinels for event in events)
                traces = con.execute("select payload_json from runtime_trace_event where task_id = ? or task_ref = ?", (current["tasks"][0]["task_id"], current["tasks"][0]["task_id"])).fetchall()
                assert all(sentinel not in trace[0] for sentinel in sentinels for trace in traces)
        assert client.get(root + f"/works/{root_work}/candidate-source/{task}", headers=HEADERS, params=selection_query).status_code == 200
        assert len(called) == 2 and model_calls == []
        if direction == "content-growth" and not closed_cycle:
            allowance_url = f"/api/workspace/v1/companies/{COMPANY}/agent-allowance"
            authorization_url = f"/api/workspace/v1/companies/{COMPANY}/agent-authorizations"
            allowance = client.get(allowance_url, headers=HEADERS).json()
            revoked = client.post(allowance_url + "/revoke", headers=HEADERS, json={
                "request_id": "explicit-api-revoke", "expected_revision": allowance["revision"],
                "authorization_ref": allowance["authorization_ref"], "enabled": False}).json()
            new_request = {"request_id": "explicit-api-new-authorization", "expected_revision": revoked["revision"],
                "previous_authorization_ref": revoked["authorization_ref"],
                "binding_refs": ["agent-fixture-binding"], "consent": False}
            refused = client.post(authorization_url, headers=HEADERS, json=new_request)
            assert refused.status_code == 422
            new_request["consent"] = True
            authorized = client.post(authorization_url, headers=HEADERS, json=new_request)
            assert authorized.status_code == 200, authorized.text
            fresh = authorized.json()
            assert fresh["authorization_ref"] != allowance["authorization_ref"]
            assert fresh["used_calls"] == 0 and fresh["total_reserved_calls"] == 2
            assert client.post(authorization_url, headers=HEADERS, json=new_request).json() == fresh
            assert client.get(root + f"/works/{root_work}/candidate-source/{task}", headers=HEADERS, params=selection_query).status_code == 200
            assert client.post(root + f"/works/{work}/execute", headers=HEADERS).status_code == 422
            assert len(called) == 2 and model_calls == []

@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
@pytest.mark.parametrize("file_mode", ["multiple", "none", "unicode"])
def test_followup_basis_real_prompt_selected_file_or_result(tmp_path, monkeypatch, direction, file_mode):
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, direction, False, False, file_mode=file_mode)


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
def test_followup_basis_before_launch_rejects_changed_file_without_reservation(tmp_path, monkeypatch, direction):
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, direction, False, False, tamper_before_launch=True)


@pytest.mark.parametrize("tamper", ["predecessor", "binding", "deleted", "scope"])
def test_followup_basis_missing_link_cannot_reserve_or_launch(tmp_path, monkeypatch, tamper):
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, "writing", False, False, tamper_before_launch=tamper)


def test_agent_source_is_original_saved_content_and_rejects_changed_scope_or_version(tmp_path, monkeypatch):
    from copy import deepcopy
    from app.conversation_service import ConversationService
    from app.runtime import RuntimeScopeError
    db, _, _, _, calls, workspace, row, binding, payload = policy_ready(tmp_path, monkeypatch)
    service = ConversationService(db)
    source = {"kind": "content-growth", "content_ref": row["content"]["entity_id"],
              "expected_version_ref": row["version"]["entity_id"], "selection": payload["selection"],
              "references": payload["references"]}
    assignment = binding["context"]["assignment_ref"]
    with scope():
        original = service.agent_work_source(COMPANY, workspace, assignment, source)
        assert original["selection"] == source["selection"]
        assert original["version_ref"] == row["version"]["entity_id"]
        assert original["context"]["assignment_ref"] == assignment
        assert original["saved_content"] == row["version"]["data"]
        changed = deepcopy(source)
        changed["expected_version_ref"] = "another-version"
        with pytest.raises(ValueError, match="版本"):
            service.agent_work_source(COMPANY, workspace, assignment, changed)
        with pytest.raises(RuntimeScopeError, match="范围"):
            service.agent_work_source(COMPANY, "other-workspace", assignment, source)
        with pytest.raises(ValueError, match="原对象"):
            service.agent_work_source(COMPANY, workspace, assignment, {"kind": "references", "references": []})
        changed = deepcopy(source)
        changed["selection"]["excerpt"] = "forged selected text"
        with pytest.raises(ValueError, match="选段"):
            service.agent_work_source(COMPANY, workspace, assignment, changed)
    assert calls == []


@pytest.mark.parametrize('state', ['active', 'first', 'revoked', 'expired', 'other_model', 'missing_anchor', 'revoked_after_read'])
def test_cg_collection_policy_projection_to_selected_send_without_injected_grant(tmp_path, monkeypatch, state):
    from datetime import timedelta
    from backend.tests.test_company_execution_policy import anchor_file
    import app.company_execution_policy as policy_module
    db, app, entry, service, calls, workspace, row, binding, payload = policy_ready(tmp_path, monkeypatch)
    assert entry.execution_grant is None
    policy = CompanyExecutionPolicy(db)
    with scope():
        if state != 'first':
            saved = consent(policy, workspace)
        if state == 'revoked':
            policy.save(COMPANY, request_id='revoke-projection', expected_revision=saved['policy']['revision'], enabled=False)
        if state == 'expired':
            current = policy_module.now()
            monkeypatch.setattr(policy_module, 'now', lambda: current + timedelta(hours=2))
        if state == 'missing_anchor':
            anchor_file(policy).unlink()  # Only the anchor created in this test's fresh fixture.
        anchor = anchor_file(policy)
    key = KEY
    if state == 'other_model':
        key = 'model.cg-other'
        with db.connect() as con:
            con.execute("insert into official_models(model_key,provider_id,display_name,supported_models,gateway_ref,status,default_model,type,name) "
                        "values (?,'deepseek','Other fixture','[\"deepseek-flash\"]','cg-test-gateway','active','deepseek-flash','model','Other fixture')", (key,))
    root = f'/api/workspace/v1/companies/{COMPANY}/content-growth/{workspace}'
    def snapshot():
        with db.connect() as con:
            return list(con.iterdump()), anchor.read_bytes() if anchor.exists() else None
    with TestClient(app) as client:
        before = snapshot()
        response = client.get(root, headers=HEADERS)
        assert response.status_code == 200, response.text
        collection = response.json()
        assert snapshot() == before, 'GET must not write events, tasks, usage, bindings, occupancy or anchor'
        assert calls == []
        assignment = next(a for a in collection['entry']['assignments'] if a['assignment_ref'] == binding['context']['assignment_ref'])
        selected_model = next(m for m in assignment['models'] if m['model_key'] == key)
        assert selected_model['execution_authorized'] is (state in {'active', 'revoked_after_read'})
        assert selected_model['execution_notice']
        assert not {'grant', 'grant_ref', 'policy_revision', 'budget_epoch'} & selected_model.keys()
        assert collection['execution_authorized'] is (state in {'active', 'other_model', 'revoked_after_read'})
        if state == 'other_model':
            assert next(m for m in assignment['models'] if m['model_key'] == KEY)['execution_authorized'] is True
        if state == 'revoked_after_read':
            with scope():
                policy.save(COMPANY, request_id='revoke-after-get', expected_revision=saved['policy']['revision'], enabled=False)
            before = snapshot()
        sent = client.post(root + f"/contents/{row['content']['entity_id']}/messages", headers=HEADERS,
                           json={**payload, 'model_key': selected_model['model_key']})
        if state == 'active':
            assert sent.status_code == 202, sent.text
            assert len(calls) == 1
            with scope():
                result = service.query_request(COMPANY, workspace, row['content']['entity_id'], binding['binding_ref'])
                assert result['attempts'][-1]['status'] == 'COMPLETED'
                assert policy.read(COMPANY)['totals']['reserved_micro_cny'] == 0
        else:
            assert sent.status_code == 404, sent.text  # Existing scoped router maps permission rejection to 404.
            if state != 'revoked_after_read':
                assert sent.json()['detail'] == selected_model['execution_notice']
            else:
                assert '明确同意' in sent.json()['detail']
            assert calls == []
            assert snapshot() == before, 'Denied selected send must not manufacture an authorization or occupancy'


@pytest.mark.parametrize('direction', ['content-growth', 'writing', 'music'])
@pytest.mark.parametrize('fail', [False, True])
def test_ordinary_reply_requires_no_selection_and_unknown_is_never_replayed(tmp_path, monkeypatch, fail, direction):
    db, app, entry, service, calls, workspace, row, binding, _ = policy_ready(tmp_path, monkeypatch, fail)
    object_ref = row['content']['entity_id']
    if direction != 'content-growth':
        from app.workspace_package_runtime import WorkspacePackageRuntime
        from app.music_entry_service import ASSETS
        from app.runtime import RuntimeFoundation
        from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
        from app.employee_execution_identity import EmployeeExecutionIdentity
        with scope():
            installed = WorkspacePackageRuntime(db, tmp_path / 'extra-store').install(ASSETS / ('writing_authoring' if direction == 'writing' else 'music'),
                COMPANY, department_id='cg-dept', business_id=direction+'-business', business_name='受控'+direction)
            workspace = installed['instance']['workspace_id']
            if direction == 'writing':
                writing = app.state.writing_entry_service
                meta = writing.metadata(COMPANY, workspace)
                writing.assign(COMPANY, workspace, 'cg-employee', meta['assignment_revision'])
                with db.connect() as con:
                    actual = writing.assignments(con, COMPANY, workspace)[0]
                binding = {'context': {'employee_ref': actual['data']['employeeRef'], 'assignment_ref': actual['entity_id']}}
            else:
                foundation = RuntimeFoundation(db)
                role = foundation.create('ROLE_SLOT', company_id=COMPANY, workspace_id=workspace, data={'name': '负责作者'})
                employee = foundation.create('AI_EMPLOYEE', company_id=COMPANY, workspace_id=workspace, lifecycle_status='AVAILABLE', data={'name': '真实负责作者'})
                assignment = ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY, workspace_id=workspace,
                    scope_type='WORKSPACE', scope_ref=workspace, role_ref=role['entity_id'], employee_ref=employee['entity_id'],
                    responsibility_key='WRITING_CHAPTER_AUTHOR' if direction == 'writing' else 'MUSIC_SONG_AUTHOR',
                    responsibility='只提供当前工作的文字建议', output_contract={'requiresResult': False})
                EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=workspace, runtime_employee_ref=employee['entity_id'],
                    company_employee_ref='cg-employee', employee_capability_binding_ref='cg-model-binding')
                binding = {'context': {'employee_ref': employee['entity_id'], 'assignment_ref': assignment['entity_id']}}
            if direction == 'writing':
                from app.writing_chapter_service import WritingChapterService
                runtime = WorkspacePackageRuntime(db, tmp_path / 'extra-store')
                book = runtime.create_object(workspace, 'core.domain-object.create', 'WritingBook', {'title': '连续对话作品', 'status': 'DRAFT'})['object_id']
                object_ref = runtime.create_object(workspace, 'core.domain-object.create', 'WritingChapter', {'title': '当前章节', 'bookRef': book, 'status': 'DRAFT'})['object_id']
                local = WritingChapterService(db)
                local.command(COMPANY, workspace, book, object_ref, 'draft.saved', 'initial-draft', 'ABSENT', {'text': '原来的正文。', 'knowledge': []})
                writing_draft = local.chapter(COMPANY, workspace, book, object_ref)['draft']
            else:
                from backend.tests.test_music_canonical_entry import data as song_data, basis
                row = app.state.music_service.command(COMPANY, workspace, '', 'create', request_id='ordinary-song', data=song_data())
                object_ref = row['song']['entity_id']
                binding = app.state.music_service.bind_discussion(COMPANY, workspace, object_ref, request_id='ordinary-song-binding',
                    expected=basis(row), assignment_ref=binding['context']['assignment_ref'])
    with scope(): consent(CompanyExecutionPolicy(db), workspace)
    base = f'/api/workspace/v1/companies/{COMPANY}/conversations'
    with TestClient(app) as client:
        topic = client.post(base, headers=HEADERS, json={'request_id': 'ordinary-topic', 'title': '当前正文的讨论',
            'employee_ref': binding['context']['employee_ref'], 'discussion_scope': {'workspace_id': workspace,
            'assignment_ref': binding['context']['assignment_ref'], 'object_ref': object_ref}})
        assert topic.status_code == 201, topic.text
        topic_id = topic.json()['conversation_id']
        payload = {'body': '请讨论这一篇文章的结构，不修改正式正文。', 'request_id': 'ordinary-message',
                   'assignment_ref': binding['context']['assignment_ref'], 'references': []}
        response = client.post(base + '/' + topic_id + '/messages', headers=HEADERS, json=payload)
        assert response.status_code == 202, response.text
        if not calls:
            with db.connect() as con:
                errors = [dict(r) for r in con.execute('select status,error from tasks where workspace_id=?', (workspace,))]
            pytest.fail(str(errors))
        assert calls[0]['max_tokens'] == 2048
        for _ in range(2):
            client.get(base + '/' + topic_id, headers=HEADERS)
            replay = client.post(base + '/' + topic_id + '/messages', headers=HEADERS, json=payload)
            assert replay.status_code == 202, replay.text
        assert len(calls) == 1
        result = client.get(base + '/' + topic_id, headers=HEADERS).json()
        assert result['attempts'][-1]['status'] == ('UNKNOWN' if fail else 'COMPLETED'), result
        if not fail: assert any(message['sender']['kind'] == 'EMPLOYEE' and message.get('task_ref') for message in result['messages'])
        with db.connect() as con:
            usage = con.execute('select * from ai_usage_records where workspace_id=?', (workspace,)).fetchall()
            assert len(usage) == 1 and usage[0]['fallback_from_model'] is None
        with scope():
            totals = CompanyExecutionPolicy(db).read(COMPANY)['totals']
            assert totals['actual_paid'] is None
            assert totals['reserved_micro_cny'] == (RESERVE_MICRO_CNY if fail else 0)
            if not fail: assert totals['estimated_micro_cny'] == 8 * 2 + 7 * 8
        if not fail:
            reply = next(message for message in result['messages'] if message['sender']['kind'] == 'EMPLOYEE')
            detail = client.get(f'/api/workspace/v1/companies/{COMPANY}/result-detail', headers=HEADERS,
                                params={'workspace_id': workspace, 'result_ref': 'task:' + reply['task_ref']})
            assert detail.status_code == 404  # A conversation reply is not promoted to a business Result.
            second = client.post(base + '/' + topic_id + '/messages', headers=HEADERS,
                                 json={**payload, 'body': '继续说明刚才的建议。', 'request_id': 'next-message'})
            assert second.status_code == 202, second.text
            assert len(calls) == 2
            assert '请讨论这一篇文章的结构' in calls[1]['messages'][0]['content']
            assert '第1轮建议。' in calls[1]['messages'][0]['content']
            with scope():
                assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['estimated_micro_cny'] == 144
            ordinary_attempt = result['attempts'][-1]['attempt_id']
            if direction == 'writing':
                selected_root = f'/api/workspace/v1/companies/{COMPANY}/writing/{workspace}/books/{book}/chapters/{object_ref}'
                selection = {'draft_ref': writing_draft['ref'], 'sha256': writing_draft['sha256'], 'start': 0, 'end': 1,
                             'excerpt': '原', 'anchor': writing_draft['ref'] + ':0:1', 'knowledge': []}
                bound = client.post(selected_root + '/discussion', headers=HEADERS,
                    json={'request_id': 'selected-binding', 'expected_draft_ref': writing_draft['ref'], 'data': {'selection': selection}})
                assert bound.status_code == 200, bound.text
                selected_binding = bound.json(); assert selected_binding['conversation_ref'] == topic_id
                selected_payload = {'binding_ref': selected_binding['ref'], 'body': '依据刚才的建议修改选段。', 'model_key': KEY, 'request_id': 'selected-message'}
                candidate_path = selected_root + '/commands/candidate.recorded'
                candidate_payload = {'request_id': 'illegal-ordinary-candidate', 'expected_draft_ref': writing_draft['ref'], 'data': {
                    'binding_ref': selected_binding['ref'], 'message_ref': reply['message_id'], 'reply_start': 0, 'reply_end': 1, 'reply_excerpt': reply['body'][0]}}
            elif direction == 'music':
                from backend.tests.test_music_canonical_entry import basis, lyrics_selection
                selected_root = f'/api/workspace/v1/companies/{COMPANY}/music/{workspace}/songs/{object_ref}'
                assert binding['conversation_id'] == topic_id
                selected_payload = {'binding_ref': binding['binding_ref'], 'body': '依据刚才的建议修改选段。', 'model_key': KEY, 'request_id': 'selected-message',
                                    'expected': basis(row), 'selection': lyrics_selection(row), 'references': []}
                candidate_path = selected_root + '/reply-candidate'
                candidate_payload = {'binding_ref': binding['binding_ref'], 'attempt_id': ordinary_attempt, 'request_id': 'illegal-ordinary-candidate'}
            else:
                from backend.tests.test_cg_content_entry import selected
                selected_root = f'/api/workspace/v1/companies/{COMPANY}/content-growth/{workspace}/contents/{object_ref}'
                assert binding['conversation_id'] == topic_id
                selected_payload = {'binding_ref': binding['binding_ref'], 'body': '依据刚才的建议修改选段。', 'model_key': KEY, 'request_id': 'selected-message',
                                    'expected_version_ref': row['version']['entity_id'], 'selection': selected(row), 'references': []}
                candidate_path = selected_root + '/reply-candidate'
                candidate_payload = {'binding_ref': binding['binding_ref'], 'attempt_id': ordinary_attempt, 'request_id': 'illegal-ordinary-candidate'}
            assert client.post(candidate_path, headers=HEADERS, json=candidate_payload).status_code in {404, 409}
            chosen = client.post(selected_root + '/messages', headers=HEADERS, json=selected_payload)
            assert chosen.status_code == 202, chosen.text
            assert len(calls) == 3, chosen.text
            assert '继续说明刚才的建议。' in calls[2]['messages'][0]['content']
            assert '第2轮建议。' in calls[2]['messages'][0]['content']
            full = client.get(base + '/' + topic_id, headers=HEADERS).json()
            selected_attempt = next(a for a in full['attempts'] if a['attempt_id'] == chosen.json()['attempt']['attempt_id'])
            assert selected_attempt['status'] == 'COMPLETED', selected_attempt
            selected_reply = next(m for m in full['messages'] if m.get('idempotency_key') == selected_attempt['attempt_id'])
            if direction == 'writing':
                candidate_payload['data']['message_ref'] = selected_reply['message_id']
                candidate_payload['request_id'] = 'selected-candidate'
            else:
                candidate_payload.update(attempt_id=selected_attempt['attempt_id'], request_id='selected-candidate')
            candidate = client.post(candidate_path, headers=HEADERS, json=candidate_payload)
            assert candidate.status_code == 200, candidate.text
            after = client.post(base + '/' + topic_id + '/messages', headers=HEADERS,
                                json={**payload, 'body': '继续解释这次选段建议，不修改正文。', 'request_id': 'after-selection'})
            assert after.status_code == 202, after.text
            assert len(calls) == 4
            assert '依据刚才的建议修改选段。' in calls[3]['messages'][0]['content']
            assert '第3轮建议。' in calls[3]['messages'][0]['content']
            # A cold service sees the same object ledger without moving or rewriting history.
            from app.conversation_service import ConversationService
            with scope():
                cold = ConversationService(db).read(COMPANY, conversation_id=topic_id)
                assert len(cold['messages']) == 8
                assert cold['discussion_scope']['object_ref'] == object_ref
            from app.main import create_app
            cold_app = create_app(str(db.path), model_gateway_adapter=app.state.rc4_fixture_executor)
            with TestClient(cold_app) as reopened:
                continued = reopened.post(base + '/' + topic_id + '/messages', headers=HEADERS,
                    json={**payload, 'body': '重新打开后接着讨论上一条建议。', 'request_id': 'after-cold-start'})
                assert continued.status_code == 202, continued.text
                assert len(calls) == 5
                assert '第4轮建议。' in calls[4]['messages'][0]['content']
                restored = reopened.get(base + '/' + topic_id, headers=HEADERS).json()
                assert len(restored['messages']) == 10 and restored['attempts'][-1]['status'] == 'COMPLETED'





def test_revoked_after_reservation_before_execution_never_launches(tmp_path, monkeypatch):
    from app.conversation_service import ConversationService
    db, app, _, _, calls, workspace, row, binding, _ = policy_ready(tmp_path, monkeypatch)
    with scope(): consent(CompanyExecutionPolicy(db), workspace)
    original = ConversationService.execute
    async def revoke_before_launch(service, claim, executor):
        policy = CompanyExecutionPolicy(db)
        current = policy.read(COMPANY)['policy']
        policy.save(COMPANY, request_id='revoke-before-launch', expected_revision=current['revision'], enabled=False)
        return await original(service, claim, executor)
    monkeypatch.setattr(ConversationService, 'execute', revoke_before_launch)
    base = f'/api/workspace/v1/companies/{COMPANY}/conversations'
    with TestClient(app) as client:
        topic = client.post(base, headers=HEADERS, json={'request_id': 'revoke-topic', 'employee_ref': binding['context']['employee_ref'],
            'discussion_scope': {'workspace_id': workspace, 'object_ref': row['content']['entity_id'], 'assignment_ref': binding['context']['assignment_ref']}})
        assert topic.status_code == 201, topic.text
        response = client.post(base + '/' + topic.json()['conversation_id'] + '/messages', headers=HEADERS,
            json={'body': '尚未开始外发前撤销', 'request_id': 'revoke-message', 'assignment_ref': binding['context']['assignment_ref'], 'references': []})
        assert response.status_code == 202, response.text
    assert calls == []
    with scope():
        assert CompanyExecutionPolicy(db).read(COMPANY)['totals'] == {'reserved_micro_cny': 0, 'estimated_micro_cny': 0, 'actual_paid': None}


def test_cg_v02_explicit_save_basis_then_reselect_before_real_prepare_send(tmp_path, monkeypatch):
    """Normal v0.2 API saves; only HTTP is injected, never the production basis guard."""
    from app.runtime import RuntimeFoundation, RuntimeScopeError
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    from app.employee_execution_identity import EmployeeExecutionIdentity
    from backend.tests.test_cg_four_form_interaction import install_v02, draft
    from backend.tests.test_cg_content_entry import selected
    from backend.tests.test_company_execution_policy import anchor_file
    db, app, entry, service, calls, _, _, legacy_binding, _ = policy_ready(tmp_path, monkeypatch)
    workspace = install_v02(db, tmp_path)
    with scope():
        foundation = RuntimeFoundation(db)
        role = foundation.create('ROLE_SLOT', company_id=COMPANY, workspace_id=workspace, data={'name': '保存依据责任'})
        employee = foundation.create('AI_EMPLOYEE', company_id=COMPANY, workspace_id=workspace,
                                     lifecycle_status='AVAILABLE', data={'name': '保存依据员工'})
        assignment = ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY, workspace_id=workspace,
            scope_type='WORKSPACE', scope_ref=workspace, role_ref=role['entity_id'], employee_ref=employee['entity_id'],
            responsibility_key='CONTENT_AUTHOR', responsibility='本地测试正文建议', output_contract={'requiresResult': False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=workspace,
            runtime_employee_ref=employee['entity_id'], company_employee_ref='cg-employee', employee_capability_binding_ref='cg-model-binding')
    policy = CompanyExecutionPolicy(db)
    root = f'/api/workspace/v1/companies/{COMPANY}/content-growth/{workspace}'
    values = draft('graphic', '雨后😀，书桌上的信仍未打开。')
    with TestClient(app) as client:
        created = client.post(root + '/contents', headers=HEADERS, json={'request_id': 'empty-basis-create', 'data': values})
        assert created.status_code == 200, created.text
        row = created.json(); content = root + '/contents/' + row['content']['entity_id']
        # No model grant is needed for ordinary local text saving.
        local = client.post(content + '/commands/save', headers=HEADERS, json={
            'request_id': 'empty-basis-local-save', 'expected_version_ref': row['version']['entity_id'], 'data': values})
        assert local.status_code == 200, local.text
        row = local.json()
        assert all(row['version']['data']['work'][k] == '' for k in ['assignment_ref', 'recipient_ref', 'model_key'])
        assert calls == []
        # A saved Agent responsibility does not require a separate text model grant.
        agent_values = {**values, 'work': {**values['work'], 'assignment_ref': assignment['entity_id'],
                                          'recipient_ref': 'cg-employee', 'model_key': ''}}
        agent_create = client.post(root + '/contents', headers=HEADERS,
                                   json={'request_id': 'agent-no-text-model', 'data': agent_values})
        assert agent_create.status_code == 200, agent_create.text
        agent_row = agent_create.json()
        source = {'kind': 'content-growth', 'content_ref': agent_row['content']['entity_id'],
                  'expected_version_ref': agent_row['version']['entity_id'], 'selection': selected(agent_row), 'references': []}
        with scope():
            agent_basis = service.agent_work_source(COMPANY, workspace, assignment['entity_id'], source)
            assert agent_basis['saved_content']['work']['model_key'] == ''
            with pytest.raises(RuntimeScopeError, match='本次员工与原保存责任不一致'):
                service.agent_work_source(COMPANY, workspace, 'different-assignment', source)
        assert calls == []
        with scope():
            assert policy.read(COMPANY)['policy'] is None
            consent(policy, workspace)
            anchor = anchor_file(policy)
        collection = client.get(root, headers=HEADERS).json()
        assert collection['entry']['definition']['version'] == '0.2.0'
        current = next(a for a in collection['entry']['assignments'] if a['assignment_ref'] == assignment['entity_id'])
        chosen = next(m for m in current['models'] if m['model_key'] == KEY)
        assert chosen['execution_authorized'] is True and entry.execution_grant is None
        bound = client.post(content + '/discussion', headers=HEADERS, json={
            'request_id': 'empty-basis-binding', 'expected_version_ref': row['version']['entity_id'], 'assignment_ref': current['assignment_ref']})
        assert bound.status_code == 200, bound.text
        binding = bound.json()
        payload = {'binding_ref': binding['binding_ref'], 'body': '请修改这个明确选段', 'request_id': 'empty-basis-send',
                   'model_key': chosen['model_key'], 'expected_version_ref': row['version']['entity_id'], 'selection': selected(row), 'references': []}
        def snapshot():
            with db.connect() as con:
                return list(con.iterdump()), anchor.read_bytes()
        before = snapshot()
        denied = client.post(content + '/messages', headers=HEADERS, json=payload)
        assert denied.status_code == 409 and '先保存本次责任员工与模型依据' in denied.json()['detail']
        assert snapshot() == before and calls == [], 'Empty basis refusal must append no message/attempt/task/usage/reservation'
        valid_work = {**values['work'], 'assignment_ref': current['assignment_ref'],
                      'recipient_ref': current['company_employee_ref'], 'model_key': chosen['model_key']}
        for label, changes in [
            ('missing-employee', {'assignment_ref': '', 'recipient_ref': ''}),
            ('foreign-workspace-assignment', {'assignment_ref': legacy_binding['context']['assignment_ref']}),
            ('stale-assignment', {'assignment_ref': 'missing-assignment'}),
            ('foreign-recipient', {'recipient_ref': 'foreign-employee'}),
            ('stale-model', {'model_key': 'missing-model'}),
        ]:
            before = snapshot()
            rejected = client.post(content + '/commands/save', headers=HEADERS, json={
                'request_id': 'invalid-basis-' + label, 'expected_version_ref': row['version']['entity_id'],
                'data': {**values, 'work': {**valid_work, **changes}}})
            assert rejected.status_code == (422 if label in {'missing-employee', 'stale-model'} else 404), (label, rejected.text)
            assert snapshot() == before and calls == [], label
        saved = client.post(content + '/commands/save', headers=HEADERS, json={
            'request_id': 'explicit-save-current-basis', 'expected_version_ref': row['version']['entity_id'],
            'data': {**values, 'work': valid_work}})
        assert saved.status_code == 200, saved.text
        fresh = saved.json()
        assert fresh['version']['entity_id'] != row['version']['entity_id']
        assert fresh['version']['data']['work'] == valid_work
        assert next(v for v in fresh['versions'] if v['entity_id'] == row['version']['entity_id'])['data']['work'] == values['work']
        assert calls == []
        before = snapshot()
        for old_selection_payload in [payload, {**payload, 'expected_version_ref': fresh['version']['entity_id']}]:
            stale = client.post(content + '/messages', headers=HEADERS, json={**old_selection_payload, 'request_id': 'old-selection-refused'})
            assert stale.status_code == 409, stale.text
            assert snapshot() == before and calls == [], 'Saving must not silently rebase old selection'
        sent = client.post(content + '/messages', headers=HEADERS, json={**payload, 'request_id': 'explicit-new-selection',
            'expected_version_ref': fresh['version']['entity_id'], 'selection': selected(fresh)})
        assert sent.status_code == 202, sent.text
        assert len(calls) == 1
        query = client.get(content + '/discussion/' + binding['binding_ref'], headers=HEADERS,
                           params={'attempt_id': sent.json()['attempt']['attempt_id']}).json()
        assert query['attempt']['status'] == 'COMPLETED'
        assert query['attempt']['execution_selection']['basis_version_ref'] == fresh['version']['entity_id']
        with scope(): assert policy.read(COMPANY)['totals']['reserved_micro_cny'] == 0
        with db.connect() as con:
            assert con.execute('select count(*) from tasks where workspace_id=?', (workspace,)).fetchone()[0] == 1
            assert con.execute('select count(*) from ai_usage_records where workspace_id=?', (workspace,)).fetchone()[0] == 1
            assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'


def test_original_agent_creation_is_atomic_against_new_workflow_version_and_failed_routing(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    from app.employee_execution_identity import EmployeeExecutionIdentity
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime, RuntimeScopeError
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from backend.tests.test_employee_agent_execution import _publication_preserved_state
    db, app, _, _, model_calls, workspace, row, binding, payload = policy_ready(tmp_path, monkeypatch)
    assignment = binding["context"]["assignment_ref"]
    source = {"kind": "content-growth", "content_ref": row["content"]["entity_id"],
        "expected_version_ref": row["version"]["entity_id"], "selection": payload["selection"],
        "references": payload["references"]}
    with scope():
        identity = EmployeeExecutionIdentity(db).resolve(company_id=COMPANY, workspace_id=workspace,
            runtime_employee_ref=binding["context"]["employee_ref"])
        db.save_tenant_private_capability(tenant_id="selfuse", capability_type="agent", capability_id="agent.fixture",
            display_name="Offline Agent", metadata={"kind": "codex-cli", "computer_access_intent": "ASK_WHEN_NEEDED"})
        with db.connect() as connection:
            connection.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_type,capability_source,capability_id) "
                "values ('agent-fixture-binding','selfuse',?,'agent','tenant_private','agent.fixture')", (identity["company_employee_ref"],))
        CompanyExecutionPolicy(db).save_agent_allowance(COMPANY, request_id="atomic-grant", expected_revision="",
            enabled=True, consent=True, binding_refs=["agent-fixture-binding"])
    root = "/api/workspace/runtime/foundation/team-operating/assignments/" + assignment
    query = {"company_id": COMPANY, "workspace_id": workspace}
    request = {"request_id": "atomic-original-request", "problem": "原请求", "expected_result": "原成果",
        "agent_binding_ref": "agent-fixture-binding", "source": source}
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(root + "/agent-workflow", params=query, headers=HEADERS).json()
        published = client.post(root + "/agent-workflow", headers=HEADERS, json=query | {
            "expected_revision": basis["assignment_revision"], "review_token": basis["review_token"], "confirm": True})
        assert published.status_code == 200, published.text
        before = _publication_preserved_state(db)
        original_start = ResponsibilityRoutingRuntime.start_work
        def fail_after_routing(self, *args, **kwargs):
            original_start(self, *args, **kwargs)
            raise RuntimeScopeError("synthetic interruption after routing")
        with monkeypatch.context() as patch:
            patch.setattr(ResponsibilityRoutingRuntime, "start_work", fail_after_routing)
            failed = client.post(root + "/work", headers=HEADERS, json=request)
            assert failed.status_code == 422, failed.text
        assert _publication_preserved_state(db) == before, "failed creation left a Cycle, Work or event"
        inserted, publisher_started, publisher_finished = Event(), Event(), Event()
        original_create = CanonicalChildWorkRuntime.create_cycle_work
        def create(self, **kwargs):
            value = original_create(self, **kwargs)
            inserted.set()
            assert publisher_started.wait(3)
            assert not publisher_finished.wait(0.1), "workflow publication escaped Work creation transaction"
            return value
        def publish_next_version():
            assert inserted.wait(3)
            publisher_started.set()
            with scope():
                value = ResponsibilityRoutingRuntime(db).publish_workflow(**query,
                    scope_type=basis["scope_type"], scope_ref=basis["scope_ref"],
                    workflow_key=basis["workflow_key"], assignment_refs=[assignment],
                    default_flow=[basis["responsibility_key"]])
            publisher_finished.set()
            return value
        with monkeypatch.context() as patch:
            patch.setattr(CanonicalChildWorkRuntime, "create_cycle_work", create)
            with ThreadPoolExecutor(max_workers=2) as pool:
                next_version = pool.submit(publish_next_version)
                created = pool.submit(lambda: client.post(root + "/work", headers=HEADERS, json=request))
                response = created.result(timeout=10)
                newer = next_version.result(timeout=10)
        assert response.status_code == 200, response.text
        original_work = response.json()["work"]
        assert original_work["data"]["responsibilityRouting"]["workflowVersion"] == 1
        assert newer["data"]["version"] == 2
        repeated = client.post(root + "/work", headers=HEADERS, json=request)
        assert repeated.status_code == 200, repeated.text
        assert repeated.json()["work"]["entity_id"] == original_work["entity_id"]
        assert repeated.json()["work"]["data"]["responsibilityRouting"]["workflowVersion"] == 1
        with scope():
            assert len(RuntimeFoundation(db).list("WORK", **query)) == 1
            assert len(RuntimeFoundation(db).list("CYCLE", **query)) == 1
            assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 0
        assert model_calls == []


# Owner-authored public output evidence only; no live Work identity or private data.
_FILE_BODY = '林澄沿编号调出旧档，发现补录页的日期比原卷晚了三天。阿岚戴上棉手套，指着页角一圈淡盐渍：“它曾离开过档案室。”窗外潮声压近，旧信仍未拆封。林澄把缺页登记为待核，又将信锁进临时柜。关门前，她看见便条背面浮出半枚蓝印，却没有问阿岚从哪里得来。'
_FILE_NOTES = '# 依据\n- 仅依据当前保存选文与绑定故事基础续写。\n- 保留林澄、阿岚、档案室、旧信、档案编号、补录日期与缺页核查线索。\n- 旧信保持未拆，未揭示或推断写信人身份。\n\n# 未知与处理\n- 写信人、旧信内容、缺页原因、阿岚便条来源均未记录，正文不作定论。\n- “淡盐渍”“半枚蓝印”为氛围与后续悬念，不指向确定身份。\n- 本稿仅为章节候选，未采纳、未发布。'


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
@pytest.mark.parametrize("file_mode", ["multiple", "none", "unicode"])
def test_original_file_candidate_body_and_text_only_compatibility(tmp_path, monkeypatch, direction, file_mode):
    def check(stage, env):
        _check_file_candidate(stage, env)
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, direction, False, False, file_mode=file_mode, candidate_check=check)

def _check_file_candidate(stage, env):
    import json
    import hashlib
    from pathlib import Path
    from app.agent_work_resources import AgentWorkResources
    from app.runtime import RuntimeFoundation
    from app.writing_chapter_service import WritingChapterService
    client, root, work, task = (env[key] for key in ("client", "root", "work", "task"))
    selected, db, source = (env[key] for key in ("selected", "db", "source"))
    preview_url = root + f"/works/{work}/candidate-source/{task}"
    candidate_url = root + f"/works/{work}/candidate"
    query = env["selection_query"]
    file_mode, direction, workspace = (env[key] for key in ("file_mode", "direction", "workspace"))
    file = None
    if env["chosen"]:
        receipt = json.loads(env["chosen"]["content"])
        resources = AgentWorkResources(Path(db.path).absolute().parent / "agent-work",
            tenant_id="selfuse", company_id=COMPANY, work_ref=work, task_id=task)
        file = resources.path / "output" / receipt["relative_path"]
    def rejected(response):
        assert response.status_code in {403, 404, 422}, response.text
    if stage == "before":
        if file_mode != "none":
            value = env["preview"].json()
            assert value["artifact_ref"] == env["chosen"]["artifact_id"]
            assert value["artifact_content_sha256"] == env["chosen"]["content_sha256"]
            assert value["file_sha256"] == hashlib.sha256(file.read_bytes()).hexdigest()
            assert value["artifact_content_sha256"] != value["file_sha256"]
            assert value["content_verification"] == "UNVERIFIED"
            if file_mode == "multiple":
                assert value["file_sha256"] == "1a427fc9044be0d076bbf9e2e9590e0a7553321ff6b1e9b858ee68ad8faaf4f3"
            rejected(client.get(preview_url, headers=HEADERS))
            # Legacy completion text is not a file selection, even with a valid text hash.
            rejected(client.post(candidate_url, headers=HEADERS, json={
                "task_ref": task, "start": 0, "end": 7, "excerpt": "原工作建议文字",
                "text_sha256": hashlib.sha256("原工作建议文字".encode()).hexdigest()}))
            for key in ["artifact_ref", "artifact_content_sha256", "file_sha256", "task_output_sha256", "text_sha256"]:
                invalid = {**selected, key: "foreign-file" if key == "artifact_ref" else "0" * 64}
                rejected(client.post(candidate_url, headers=HEADERS, json=invalid))
            for change in [{"start": True}, {"end": selected["end"] + 1}, {"excerpt": _FILE_NOTES}]:
                rejected(client.post(candidate_url, headers=HEADERS, json={**selected, **change}))
            raw = file.read_bytes()
            file.write_bytes(b"x" * len(raw))
            try:
                rejected(client.get(preview_url, headers=HEADERS, params=query))
                rejected(client.post(candidate_url, headers=HEADERS, json=selected))
            finally:
                file.write_bytes(raw)
            with db.connect() as con:
                con.execute("update artifacts set content_sha256=? where artifact_id=?", ("0" * 64, env["chosen"]["artifact_id"]))
            try:
                rejected(client.get(preview_url, headers=HEADERS, params=query))
                rejected(client.post(candidate_url, headers=HEADERS, json=selected))
            finally:
                with db.connect() as con:
                    con.execute("update artifacts set content_sha256=? where artifact_id=?",
                        (env["chosen"]["content_sha256"], env["chosen"]["artifact_id"]))
            if file_mode == "unicode":
                invalid = {**selected, "start": len(_FILE_BODY), "end": len(_FILE_BODY) + 1, "excerpt": "😀"}
                rejected(client.post(candidate_url, headers=HEADERS, json=invalid))
                selected.update(start=len(_FILE_BODY), end=len(_FILE_BODY) + 2, excerpt="😀")
        rejected(client.get(preview_url, headers={**HEADERS, "X-Tenant-Id": "foreign"}, params=query))
        rejected(client.post(candidate_url, headers={**HEADERS, "X-Tenant-Id": "foreign"}, json=selected))
        rejected(client.get(root + f"/works/{work}/candidate-source/foreign-task", headers=HEADERS, params=query))
        rejected(client.get(root + f"/works/foreign-work/candidate-source/{task}", headers=HEADERS, params=query))
        # A completed task cannot be relabelled as another workspace or cancelled
        # and still authorize a candidate. Only this fresh fixture is modified.
        for column, value in [("workspace_id", None), ("status", "CANCELLED")]:
            with db.connect() as con:
                old = con.execute(f"select {column} from tasks where task_id=?", (task,)).fetchone()[0]
                con.execute(f"update tasks set {column}=? where task_id=?", (value, task))
            try:
                rejected(client.get(preview_url, headers=HEADERS, params=query))
                rejected(client.post(candidate_url, headers=HEADERS, json=selected))
            finally:
                with db.connect() as con:con.execute(f"update tasks set {column}=? where task_id=?", (old, task))
        return
    assert len(env["called"]) == 1 and env["model_calls"] == []
    # A fresh service/API read of the same stored Work/Task/file proves cold
    # reconstruction; actual cross-package Native acceptance remains Owner's gate.
    again = client.get(preview_url, headers=HEADERS, params=query)
    assert again.status_code == 200
    assert again.json() == env["preview"].json()
    with scope():
        if direction == "writing":
            service = WritingChapterService(db)
            book, chapter = source["book_ref"], source["chapter_ref"]
            before = service.chapter(COMPANY, workspace, book, chapter)["draft"]
            candidate = env["candidate"].json()
            assert candidate["replacement"] == selected["excerpt"]
            provenance = candidate["provenance"]
            args = (COMPANY, workspace, book, chapter, "candidate.adopted", "source14-explicit-adopt", before["ref"])
            if file:
                raw = file.read_bytes();file.write_bytes(b"x" * len(raw))
                try:
                    with pytest.raises(ValueError):
                        service.command(*args, {"candidate_ref": candidate["ref"], "confirmed": True})
                finally:
                    file.write_bytes(raw)
            with pytest.raises(ValueError):
                service.command(*args, {"candidate_ref": candidate["ref"], "confirmed": False})
            adopted = service.command(*args, {"candidate_ref": candidate["ref"], "confirmed": True})
            assert selected["excerpt"] in adopted["draft"]["text"]
            assert service.command(*args, {"candidate_ref": candidate["ref"], "confirmed": True}) == adopted
        elif direction == "content-growth":
            service = env["content_service"]
            ref = env["candidate"].json()["candidate_ref"]
            candidate = RuntimeFoundation(db).get(ref)["data"];provenance = candidate["provenance"]
            assert candidate["body"] == selected["excerpt"]
            adopted = service.command(COMPANY, workspace, source["content_ref"], "adopt",
                request_id="source14-explicit-adopt", expected_version_ref=source["expected_version_ref"],
                data={"candidate_ref": ref, "checks": {"content": True, "references": True, "account": True}})
            assert adopted["version"]["data"]["body"] == selected["excerpt"]
        else:
            service = env["app"].state.music_service
            candidate = RuntimeFoundation(db).get(env["candidate"].json()["candidate_ref"])["data"]
            provenance = candidate["provenance"]
            assert candidate["suggestion"] == selected["excerpt"] and not candidate["asset_ref"]
            # Existing manual lyric editing, not fabricated audio audition/master acceptance.
            adopted = service.command(COMPANY, workspace, source["song_ref"], "save-lyrics",
                request_id="source14-explicit-lyrics", expected={"lyrics_ref": source["expected"]["lyrics_ref"]},
                data={"text": selected["excerpt"], "draft_revision": "source14-manual"})
            assert adopted["lyrics"]["data"]["text"] == selected["excerpt"]
            assert not adopted["song"]["data"]["choice_ref"]
        if file:
            for key in ["artifact_ref", "artifact_content_sha256", "file_sha256", "task_output_sha256"]:
                assert provenance[key] == selected[key]
            assert provenance["content_verification"] == "UNVERIFIED"
    # Saving against the old business basis must fail after explicit adoption/edit.
    rejected(client.post(candidate_url, headers=HEADERS, json=selected))
    assert len(env["called"]) == 1 and env["model_calls"] == []


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
@pytest.mark.parametrize("file_mode", ["binary", "oversize"])
def test_original_file_candidate_rejects_nontext_or_oversize_without_truncating(tmp_path, monkeypatch, direction, file_mode):
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, direction, False, False, file_mode=file_mode)


@pytest.mark.parametrize("mode", ["unavailable", "registration_failure", "no_hosts", "followup_priority", "executor_failure", "execution_failure"])
def test_original_work_browser_bridge_fails_closed_and_cleans_up(tmp_path, monkeypatch, mode):
    import json
    from types import SimpleNamespace
    import app.agent_browser_runtime as reader
    import app.agent_executor_dispatch as dispatch
    from app.agent_tool_server import AgentToolSessions
    calls, closed = [], []
    original_open = reader.open_reader_for_work
    def check(context):
        db, client, work, cycle_ref, root = (context[k] for k in ("db", "client", "work", "cycle_ref", "root"))
        with db.connect() as connection:
            def load(entity):
                raw = connection.execute("select data_json from runtime_entities where entity_id=?", (entity,)).fetchone()
                return json.loads(raw["data_json"])
            def save(entity, data):
                connection.execute("update runtime_entities set data_json=? where entity_id=?",
                                   (json.dumps(data), entity))
            cycle = load(cycle_ref)
            work_data = load(work)
            if mode == "followup_priority":
                cycle["contract"]["agentBrowser"] = {"hosts": ["cycle.example.com"]}
                followup = dict(work_data.get("followupContract") or cycle["contract"])
                followup["agentBrowser"] = {"hosts": ["followup.example.com"]}
                work_data["followupContract"] = followup
                save(cycle_ref, cycle)
                save(work, work_data)
            else:
                for entity, data in ((work, work_data), (cycle_ref, cycle)):
                    target = data.get("followupContract") if entity == work else data.get("contract")
                    if isinstance(target, dict):
                        target["agentBrowser"] = {"hosts": [] if mode == "no_hosts" else ["example.com"]}
                        save(entity, data)
        class FakeBrowser:
            def close(self): closed.append(True)
        def open_bridge(identity, hosts, should_stop):
            calls.append((dict(identity), list(hosts), should_stop()))
            if mode == "unavailable":
                from hashlib import sha256
                from pathlib import Path
                raw = Path(reader.__file__).with_name("reader_runtime_lock.json").read_bytes()
                assert sha256(raw).hexdigest() == reader.READER_LOCK_SHA256
                lock = json.loads(raw)
                assert lock["complete"] is False and lock["executionAuthorized"] is False
                try:
                    return original_open(identity, hosts, should_stop)
                except ValueError as error:
                    assert "尚未完成独立验证" in str(error)
                    raise
            return FakeBrowser()
        monkeypatch.setattr(reader, "open_reader_for_work", open_bridge)
        if mode == "registration_failure":
            def fail_registration(*args, **kwargs): raise ValueError("fixture registration failed")
            monkeypatch.setattr(AgentToolSessions, "register", fail_registration)
        if mode in {"executor_failure", "execution_failure"}:
            def fail_executor(*args, **kwargs):
                if mode == "executor_failure":
                    raise ValueError("fixture executor construction failed")
                def fail_execute(prompt):
                    raise ValueError("fixture execution failed")
                return SimpleNamespace(execute=fail_execute)
            monkeypatch.setattr(dispatch, "build_agent_executor", fail_executor)
        result = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        if mode == "no_hosts":
            assert calls == [] and closed == []
            assert result.status_code == 200 and len(context["called"]) == 1
        else:
            assert len(calls) == 1, result.text
            identity, hosts, stopped = calls[0]
            assert identity["work_ref"] == work and identity["tenant_id"] == "selfuse"
            assert identity["company_id"] == COMPANY and identity["binding_ref"] == "agent-fixture-binding"
            expected_hosts = ["followup.example.com"] if mode == "followup_priority" else ["example.com"]
            assert identity["task_id"] and identity["employee_id"] and hosts == expected_hosts and stopped is False
            assert closed == ([] if mode == "unavailable" else [True])
            if mode == "followup_priority":
                assert result.status_code == 200 and len(context["called"]) == 1
            else:
                assert context["called"] == []
        assert context["model_calls"] == []
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, "content-growth", False, False,
        browser_check=check, trusted_fixture=True)


@pytest.mark.parametrize('failure', ['reservation', 'usage_audit'])
def test_original_agent_record_failure_does_not_trigger_fallback(tmp_path, monkeypatch, failure):
    from types import SimpleNamespace
    import app.agent_executor_dispatch as dispatch
    from app.ai_usage import AIUsageService

    def check(context):
        client, root, work, db = (context[k] for k in ('client', 'root', 'work', 'db'))
        calls = []

        def factory(_metadata, **kwargs):
            execution = kwargs['execution_context']
            def execute(_prompt):
                execution['before_launch']()
                calls.append('synthetic only')
                return {'output': 'synthetic result', 'status': 'success', 'outbound_attempted': True,
                        'cost': 0, 'estimated_cost': 0, 'ledger_cost_source': 'unknown',
                        'metering_status': 'unknown', 'provider_id': 'openai_codex',
                        'model_gateway_id': 'codex-cli', 'model_name': 'agent.fixture'}
            return SimpleNamespace(execute=execute)

        monkeypatch.setattr(dispatch, 'build_agent_executor', factory)
        if failure == 'reservation':
            def fail_reservation(*_args, **_kwargs):
                raise OSError('synthetic reservation failure')
            monkeypatch.setattr(CompanyExecutionPolicy, 'reserve_agent_call', fail_reservation)
        else:
            def fail_usage(*_args, **_kwargs):
                raise OSError('synthetic usage persistence failure')
            monkeypatch.setattr(AIUsageService, 'record_call', fail_usage)

        result = client.post(root + f'/works/{work}/execute?max_executions=1', headers=HEADERS)
        assert result.status_code == 200, result.text
        snapshot = client.get(root + f'/works/{work}', headers=HEADERS).json()
        assert len(snapshot['tasks']) == 1 and snapshot['tasks'][0]['status'] == 'FAILED'
        assert context['model_calls'] == []
        assert calls == ([] if failure == 'reservation' else ['synthetic only'])
        assert snapshot['tasks'][0]['call_reserved'] is (failure == 'usage_audit')
        if failure == 'usage_audit':
            repeated = client.post(root + f'/works/{work}/execute?max_executions=1', headers=HEADERS)
            assert repeated.status_code == 422
            assert calls == ['synthetic only'] and context['model_calls'] == []
            with scope():
                with pytest.raises(Exception, match='不能重复'):
                    CompanyExecutionPolicy(db).require_unreserved_agent_work(COMPANY, work)

    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, 'content-growth', False, False, browser_check=check)


def test_codex_hold_projects_only_scoped_trusted_event_before_resources(tmp_path, monkeypatch):
    from app.agent_adapter import CodexExecutionHeld
    import app.agent_adapter as agent_adapter
    from app.agent_work_resources import AgentWorkResources
    from app.agent_tool_server import AgentToolSessions
    import app.agent_browser_runtime as reader

    def check(context):
        monkeypatch.setattr(agent_adapter, "require_codex_execution_available",
                            lambda: (_ for _ in ()).throw(CodexExecutionHeld()))
        def forbidden(*args, **kwargs):
            pytest.fail("held Codex prepared resources or called an executor")
        monkeypatch.setattr(AgentWorkResources, "prepare", forbidden)
        monkeypatch.setattr(AgentToolSessions, "register", forbidden)
        monkeypatch.setattr(reader, "open_reader_for_work", forbidden)
        client, root, work, db = (context[k] for k in ("client", "root", "work", "db"))
        response = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert response.status_code == 200, response.text
        original = client.get(root + f"/works/{work}", headers=HEADERS)
        assert original.status_code == 200, original.text
        tasks = original.json()["tasks"]
        assert len(tasks) == 1 and tasks[0]["status"] == "FAILED"
        assert tasks[0]["reason_code"] == "codex_execution_held"
        assert tasks[0]["call_reserved"] is False and context["called"] == []
        foreign = client.get(root + f"/works/{work}", headers={**HEADERS, "X-Tenant-Id": "foreign"})
        assert foreign.status_code != 200
        import json
        task_id = tasks[0]["task_id"]
        def reason():
            result = client.get(root + f"/works/{work}", headers=HEADERS)
            assert result.status_code == 200, result.text
            return result.json()["tasks"][0]["reason_code"]
        with db.connect() as connection:
            event = connection.execute("select event_id,payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='agent.execution.codex_held'", ("selfuse", task_id)).fetchone()
            task = connection.execute("select state_flow from tasks where tenant_id=? and task_id=?",
                ("selfuse", task_id)).fetchone()
        assert event is not None
        saved_event = json.loads(event["payload"])
        for field in ("task_id", "work_ref", "company_id", "workspace_id", "nonce"):
            forged = {**saved_event, field: "foreign-value"}
            with db.connect() as connection:
                connection.execute("update evolution_events set payload=? where event_id=?",
                    (json.dumps(forged), event["event_id"]))
            assert reason() is None
        with db.connect() as connection:
            connection.execute("update evolution_events set payload=? where event_id=?", ("{bad json", event["event_id"]))
        assert reason() is None
        with db.connect() as connection:
            connection.execute("update evolution_events set payload=? where event_id=?", (event["payload"], event["event_id"]))
            changed_flow = json.loads(task["state_flow"]) + ["RUNNING", "FAILED"]
            connection.execute("update tasks set state_flow=? where tenant_id=? and task_id=?",
                (json.dumps(changed_flow), "selfuse", task_id))
        assert reason() is None
        with db.connect() as connection:
            connection.execute("update tasks set state_flow=?, status='CANCELLED' where tenant_id=? and task_id=?",
                (task["state_flow"], "selfuse", task_id))
        assert reason() is None
        with db.connect() as connection:
            connection.execute("update tasks set status='FAILED' where tenant_id=? and task_id=?", ("selfuse", task_id))
            connection.execute("insert into evolution_events(correlation_id,event_type,payload,tenant_id) values (?,?,?,?)",
                (task_id, "agent.execution.codex_held", event["payload"], "selfuse"))
        assert reason() is None
        with db.connect() as connection:
            connection.execute("delete from evolution_events where tenant_id=? and correlation_id=? "
                               "and event_type='agent.execution.codex_held'", ("selfuse", task_id))
        assert reason() is None

    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, "content-growth", False, False, browser_check=check)


def test_original_work_unknown_blocks_retry_without_a_reservation(tmp_path, monkeypatch):
    from app.agent_adapter import AgentExecutionError
    import app.agent_adapter as agent_adapter
    from app.agent_work_resources import AgentWorkResources

    def check(context):
        def unknown():
            raise AgentExecutionError("synthetic uncertainty", status="outcome_unknown", outbound_attempted=False)
        monkeypatch.setattr(agent_adapter, "require_codex_execution_available", unknown)
        monkeypatch.setattr(AgentWorkResources, "prepare", lambda *a, **k: pytest.fail("resources prepared"))
        client, root, work, db = (context[k] for k in ("client", "root", "work", "db"))
        first = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert first.status_code == 200, first.text
        snapshot = client.get(root + f"/works/{work}", headers=HEADERS)
        assert snapshot.status_code == 200, snapshot.text
        tasks = snapshot.json()["tasks"]
        assert len(tasks) == 1 and tasks[0]["reason_code"] == "outcome_unknown"
        assert tasks[0]["call_reserved"] is False and context["called"] == []
        replay = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert replay.status_code == 422 and "执行状态未确认" in replay.text and context["called"] == []
        with db.connect() as connection:
            connection.execute("update evolution_events set payload='{}' where event_type=? and correlation_id=?",
                               ("agent.execution.outcome_unknown", tasks[0]["task_id"]))
        corrupt = client.get(root + f"/works/{work}", headers=HEADERS)
        assert corrupt.status_code == 200 and corrupt.json()["tasks"][0]["reason_code"] == "outcome_unverified"
        blocked = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert blocked.status_code == 422 and "执行状态未确认" in blocked.text

    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, "content-growth", False, False, browser_check=check, trusted_fixture=True)


def test_supervisor_unavailable_does_not_mark_new_work_unknown(tmp_path, monkeypatch):
    from app.agent_adapter import AgentExecutionError
    from app.agent_work_resources import AgentWorkResources
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    import app.agent_adapter as agent_adapter

    def check(context):
        client, root, work, db = (context[k] for k in ("client", "root", "work", "db"))
        with scope():
            store = ResultStore(db, EvolutionEventLog(db))
            old = store.create_task("older fixture", company_id=COMPANY, work_ref="older-work")
            store.record_agent_outcome_unknown(old["task_id"])
        def unavailable():
            raise AgentExecutionError("supervisor unavailable", status="supervisor_unavailable", outbound_attempted=False)
        monkeypatch.setattr(agent_adapter, "require_codex_execution_available", unavailable)
        monkeypatch.setattr(AgentWorkResources, "prepare", lambda *a, **k: pytest.fail("resources prepared"))
        response = client.post(root + f"/works/{work}/execute?max_executions=1", headers=HEADERS)
        assert response.status_code == 200, response.text
        snapshot = client.get(root + f"/works/{work}", headers=HEADERS)
        assert snapshot.status_code == 200, snapshot.text
        tasks = snapshot.json()["tasks"]
        assert len(tasks) == 1 and tasks[0]["reason_code"] is None and context["called"] == []
        with db.connect() as connection:
            rows = connection.execute("select correlation_id from evolution_events where event_type=?",
                                      ("agent.execution.outcome_unknown",)).fetchall()
        assert [row["correlation_id"] for row in rows] == [old["task_id"]]

    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, "content-growth", False, False, browser_check=check, trusted_fixture=True)


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
def test_agent_atomic_result_returns_to_original_work(tmp_path, monkeypatch, direction):
    test_original_agent_work_persists_task_usage_files_and_explicit_candidate(
        tmp_path, monkeypatch, False, direction, False, False, trusted_fixture=True)
