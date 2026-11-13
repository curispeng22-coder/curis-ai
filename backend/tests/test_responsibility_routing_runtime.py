from __future__ import annotations

import json

import pytest

from app.database import Database
from app.runtime import ResponsibilityRoutingError, ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.models import ensure_ceo_day_schema
from app.tenant_context import TenantContext


TENANT = "tenant-routing"
COMPANY = "company-routing"
WORKSPACE = "workspace-routing"
BUSINESS = "business-routing"
BUSINESS_ONLY = "business-without-workspace"


def _seed(path) -> tuple[Database, RuntimeFoundation, ResponsibilityRoutingRuntime]:
    database = Database(str(path))
    database.initialize()
    ensure_ceo_day_schema(database)
    with database.connect() as conn:
        conn.execute(
            "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
            "values (?, ?, 'Routing Business', 'CUSTOM', 'Verified result', 'ACTIVE')",
            (BUSINESS, TENANT),
        )
        conn.execute(
            "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
            "values (?, ?, 'No Workspace Business', 'CUSTOM', 'Verified result', 'ACTIVE')",
            (BUSINESS_ONLY, TENANT),
        )
        conn.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo-routing', 'Routing Company')",
            (COMPANY, TENANT),
        )
        conn.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, status) "
            "values ('department-routing', ?, ?, 'test-department-template', 'Routing Department', 'TEST', 'active')",
            (TENANT, COMPANY),
        )
        for business_id, name in ((BUSINESS, "Routing Business"), (BUSINESS_ONLY, "No Workspace Business")):
            conn.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, "
                "created_at, updated_at) "
                "values (?, ?, ?, 'department-routing', ?, 'ACTIVE', current_timestamp, current_timestamp)",
                (business_id, TENANT, COMPANY, name),
            )
        conn.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version, "
            "business_relation_status, business_relation_source) "
            "values (?, ?, ?, ?, 'Routing Workspace', 'OPERATING', 'v1', 'RESOLVED', 'CANONICAL')",
            (WORKSPACE, TENANT, COMPANY, BUSINESS),
        )
    return database, RuntimeFoundation(database), ResponsibilityRoutingRuntime(database)


def _assignments(foundation, router, names):
    result = {}
    for key, is_leader in names:
        employee = foundation.create(
            "AI_EMPLOYEE", entity_id=f"employee-{key}", company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="AVAILABLE", data={"name": key},
        )
        role = foundation.create(
            "ROLE_SLOT", entity_id=f"role-{key}", company_id=COMPANY,
            workspace_id=WORKSPACE, data={"role": key},
        )
        result[key] = router.create_assignment(
            assignment_id=f"assignment-{key}", company_id=COMPANY,
            workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            role_ref=role["entity_id"], employee_ref=employee["entity_id"],
            responsibility_key=key, responsibility=f"负责{key}", is_leader=is_leader,
            input_contract={"requiredRefs": [f"input:{key}"]},
            output_contract={"requiresResult": True},
        )
    return result


def _current(work):
    return work["data"]["responsibilityRouting"]


def test_content_growth_default_deviation_return_result_and_restart(tmp_path):
    database, foundation, router = _seed(tmp_path / "content-routing.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-routing", role="test"):
        assignments = _assignments(
            foundation, router,
            [("leader", True), ("topic", False), ("research", False), ("copy", False), ("visual", False), ("publish", False)],
        )
        workflow = router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="content-growth", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["topic", "research", "copy", "visual", "publish"],
        )
        work = foundation.create(
            "CYCLE", entity_id="cycle-content", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "AI 科技内容增长"},
        )
        with database.connect() as conn:
            task_count = conn.execute("select count(*) from tasks").fetchone()[0]

        work = router.start_work(work["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="content-growth")
        assert _current(work)["workflowRef"] == workflow["entity_id"]
        assert _current(work)["responsibilityHolderRef"] == "employee-topic"
        assert _current(work)["currentExecutorRef"] is None

        routed = router.route(work["entity_id"], signal="COMPLETED", result_refs=["result:topic"])
        assert _current(routed["work"])["responsibilityHolderRef"] == "employee-research"
        assert routed["handoff"]["lifecycle_status"] == "COMPLETED"

        with database.connect() as conn:
            handoffs_before_consult = conn.execute(
                "select count(*) from runtime_entities where entity_type='HANDOFF' and parent_id=?", (work["entity_id"],)
            ).fetchone()[0]
        leader = router.route(
            work["entity_id"], signal="CONSULT", responsibility_key="leader",
            problem="研究方向是否继续", interaction_key="content-leader-consult",
            bounded_summary="只需要方向判断", result_refs=["result:leader-advice"],
        )
        assert _current(leader["work"])["responsibilityHolderRef"] == "employee-research"
        assert leader["consult"]["status"] == "COMPLETED"
        assert leader["handoff"] is None
        with database.connect() as conn:
            assert conn.execute(
                "select count(*) from runtime_entities where entity_type='HANDOFF' and parent_id=?", (work["entity_id"],)
            ).fetchone()[0] == handoffs_before_consult

        router.route(work["entity_id"], signal="COMPLETED", result_refs=["result:research"])
        router.route(work["entity_id"], signal="COMPLETED", result_refs=["result:copy"])
        returned = router.route(
            work["entity_id"], signal="RETURN", responsibility_key="copy", problem="视觉要求文案修订"
        )
        assert _current(returned["work"])["responsibilityHolderRef"] == "employee-copy"
        router.route(work["entity_id"], signal="NEED_RESPONSIBILITY", responsibility_key="visual", result_refs=["result:copy-v2"])
        router.route(work["entity_id"], signal="NEED_RESPONSIBILITY", responsibility_key="publish", result_refs=["result:visual"])
        completed = router.route(work["entity_id"], signal="COMPLETED", result_refs=["result:published"])
        assert _current(completed["work"])["status"] == "COMPLETED"
        assert "result:published" in _current(completed["work"])["resultRefs"]

        with database.connect() as conn:
            assert conn.execute("select count(*) from tasks").fetchone()[0] == task_count
            assert conn.execute(
                "select count(*) from runtime_entities where entity_type='HANDOFF' and parent_id=?",
                (work["entity_id"],),
            ).fetchone()[0] >= 5
            first_handoff = conn.execute(
                "select entity_id, data_json from runtime_entities where entity_type='HANDOFF' and parent_id=? order by created_at limit 1",
                (work["entity_id"],),
            ).fetchone()
            path = conn.execute(
                "select source, target from runtime_transition_log where entity_id=? order by log_id",
                (first_handoff["entity_id"],),
            ).fetchall()
            assert [(row["source"], row["target"]) for row in path] == [
                ("CREATED", "SENT"), ("SENT", "ACKNOWLEDGED"), ("ACKNOWLEDGED", "COMPLETED"),
            ]
            assert json.loads(first_handoff["data_json"])["acknowledgement"]["manualConfirmationRequired"] is False

        restarted = ResponsibilityRoutingRuntime(Database(database.path))
        persisted = restarted.foundation.get(work["entity_id"])
        assert _current(persisted)["status"] == "COMPLETED"
        assert _current(persisted)["currentExecutorRef"] is None


def test_rd_dynamic_routes_version_pinning_binding_and_contracts(tmp_path):
    database, foundation, router = _seed(tmp_path / "rd-routing.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-routing", role="test"):
        assignments = _assignments(
            foundation, router,
            [("leader", True), ("product", False), ("architecture", False), ("development", False), ("test", False)],
        )
        v1 = router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="rd", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["product", "architecture", "development", "test"],
        )
        work1 = foundation.create(
            "CYCLE", entity_id="cycle-rd-v1", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "修复受控函数"},
        )
        work1 = router.start_work(work1["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="rd")
        router.route(work1["entity_id"], signal="COMPLETED", result_refs=["result:product"])
        router.route(work1["entity_id"], signal="COMPLETED", result_refs=["result:architecture"])
        with database.connect() as conn:
            handoffs_before_consults = conn.execute(
                "select count(*) from runtime_entities where entity_type='HANDOFF' and parent_id=?", (work1["entity_id"],)
            ).fetchone()[0]
        clarification = router.route(
            work1["entity_id"], signal="CONSULT", responsibility_key="product",
            problem="requirement clarification", interaction_key="rd-product-consult",
            result_refs=["result:clarified"],
        )
        assert _current(clarification["work"])["responsibilityHolderRef"] == "employee-development"
        architecture = router.route(
            work1["entity_id"], signal="CONSULT", responsibility_key="architecture",
            problem="architecture question", interaction_key="rd-architecture-consult",
            result_refs=["result:architecture-answer"],
        )
        assert _current(architecture["work"])["responsibilityHolderRef"] == "employee-development"
        stayed = router.route(work1["entity_id"], signal="STAY_AND_CONTINUE")
        assert stayed["action"] == "STAY_AND_CONTINUE"
        with database.connect() as conn:
            assert conn.execute(
                "select count(*) from runtime_entities where entity_type='HANDOFF' and parent_id=?", (work1["entity_id"],)
            ).fetchone()[0] == handoffs_before_consults
        router.route(work1["entity_id"], signal="COMPLETED", result_refs=["result:development"])
        defect = router.route(
            work1["entity_id"], signal="RETURN_OR_REVISION", responsibility_key="development", problem="test failed"
        )
        assert _current(defect["work"])["responsibilityHolderRef"] == "employee-development"
        assert defect["handoff"]["lifecycle_status"] == "COMPLETED"
        fixed = router.route(work1["entity_id"], signal="COMPLETED", result_refs=["result:fixed"])
        assert _current(fixed["work"])["responsibilityHolderRef"] == "employee-test"

        replacement = foundation.create(
            "AI_EMPLOYEE", entity_id="employee-test-v2", company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="AVAILABLE", data={"name": "test-v2"},
        )
        router.update_assignment(
            assignments["test"]["entity_id"], employee_ref=replacement["entity_id"],
            responsibility="负责回归与质量结论", input_contract={"requiredRefs": ["diff", "build"]},
            output_contract={"requiresResult": False},
        )
        v2 = router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="rd", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["product", "development", "architecture", "test"],
        )
        assert v2["data"]["version"] == 2
        assert _current(router.foundation.get(work1["entity_id"]))["workflowRef"] == v1["entity_id"]

        work2 = foundation.create(
            "CYCLE", entity_id="cycle-rd-v2", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "验证新绑定"},
        )
        work2 = router.start_work(work2["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="rd")
        assert _current(work2)["workflowRef"] == v2["entity_id"]
        router.route(work2["entity_id"], signal="COMPLETED", result_refs=["result:product-v2"])
        assert _current(router.foundation.get(work2["entity_id"]))["responsibilityHolderRef"] == "employee-development"
        router.route(work2["entity_id"], signal="NEED_RESPONSIBILITY", responsibility_key="test")
        assert _current(router.foundation.get(work2["entity_id"]))["responsibilityHolderRef"] == "employee-test-v2"

        context = router.build_execution_context(
            work2["entity_id"], current_truth_refs=[f"ref:{index}" for index in range(50)],
            compact_context="x" * 1400,
        )
        assert context["assignment"]["responsibility"] == "负责回归与质量结论"
        assert context["assignment"]["inputContract"] == {"requiredRefs": ["diff", "build"]}
        assert len(context["truthRefs"]) == 32
        assert len(context["compactResponsibilityContext"]) == 1000
        assert "conversation" not in context

        work3 = foundation.create(
            "CYCLE", entity_id="cycle-rd-contract", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "验证结果契约"},
        )
        router.start_work(work3["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="rd")
        with pytest.raises(ResponsibilityRoutingError, match="requires a Result"):
            router.route(work3["entity_id"], signal="TERMINAL")


def test_business_scope_decision_reuses_packet_and_restores_same_holder(tmp_path):
    _, foundation, router = _seed(tmp_path / "business-routing.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-routing", role="test"):
        employee = foundation.create(
            "AI_EMPLOYEE", entity_id="employee-business-leader", company_id=COMPANY,
            lifecycle_status="AVAILABLE", data={"name": "Business Leader"},
        )
        role = foundation.create("ROLE_SLOT", entity_id="role-business-leader", company_id=COMPANY)
        assignment = router.create_assignment(
            company_id=COMPANY, scope_type="BUSINESS", scope_ref=BUSINESS_ONLY,
            role_ref=role["entity_id"], employee_ref=employee["entity_id"],
            responsibility_key="business-leader", responsibility="经营负责人", is_leader=True,
        )
        router.publish_workflow(
            company_id=COMPANY, scope_type="BUSINESS", scope_ref=BUSINESS_ONLY,
            workflow_key="business", assignment_refs=[assignment["entity_id"]], default_flow=["business-leader"],
        )
        work = foundation.create("CYCLE", entity_id="cycle-business", company_id=COMPANY, lifecycle_status="RUNNING")
        work = router.start_work(work["entity_id"], scope_type="BUSINESS", scope_ref=BUSINESS_ONLY, workflow_key="business")
        waiting = router.route(work["entity_id"], signal="WAIT")
        assert _current(waiting["work"])["status"] == "WAITING"
        resumed_wait = router.route(work["entity_id"], signal="STAY_AND_CONTINUE")
        assert _current(resumed_wait["work"])["status"] == "ACTIVE"
        first = router.route(work["entity_id"], signal="DECISION_GATE", problem="需要 CEO 经营取舍")
        second = router.route(work["entity_id"], signal="DECISION_GATE", problem="重复请求")
        assert first["decision"]["entity_id"] == second["decision"]["entity_id"]
        assert first["decision"]["lifecycle_status"] == "WAITING_CEO"
        resumed = router.apply_decision(work["entity_id"], choice="CONTINUE", reason="继续验证")
        assert resumed["decision"]["lifecycle_status"] == "APPLIED"
        assert _current(resumed["work"])["status"] == "ACTIVE"
        assert _current(resumed["work"])["responsibilityHolderRef"] == employee["entity_id"]


def test_consult_review_duplicate_restart_version_and_revision_truth(tmp_path):
    database, foundation, router = _seed(tmp_path / "collaboration-routing.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-routing", role="test"):
        assignments = _assignments(
            foundation, router,
            [("development", False), ("reviewer", False), ("test", False)],
        )
        v1 = router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="review-flow", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["development", "test"],
        )
        work = foundation.create(
            "CYCLE", entity_id="cycle-collaboration", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "验证协作"},
        )
        work = router.start_work(
            work["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="review-flow"
        )
        with database.connect() as conn:
            tasks_before = conn.execute("select count(*) from tasks").fetchone()[0]
            cycles_before = conn.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0]
            handoffs_before = conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0]

        consult = router.route(
            work["entity_id"], signal="CONSULT", responsibility_key="reviewer",
            problem="请给出一个边界意见", interaction_key="consult-stable",
            bounded_summary="摘要" * 500,
            artifact_refs=[f"artifact:{index}" for index in range(30)],
        )
        duplicate = router.route(
            work["entity_id"], signal="CONSULT", responsibility_key="reviewer",
            problem="请给出一个边界意见", interaction_key="consult-stable",
            bounded_summary="摘要" * 500,
            artifact_refs=[f"artifact:{index}" for index in range(30)],
        )
        assert consult["consult"]["interactionRef"] == duplicate["consult"]["interactionRef"]
        assert consult["consult"]["status"] == "WAITING"
        assert _current(consult["work"])["responsibilityHolderRef"] == "employee-development"
        cost = consult["consult"]["context"]["cost"]
        assert cost["chars"] == len("请给出一个边界意见") + 600
        assert cost["bytes"] == len(("请给出一个边界意见" + ("摘要" * 300)).encode("utf-8"))
        assert cost["refsCount"] == 16
        assert cost["hydratedBodiesCount"] == 0
        assert cost["providerTaskCreatedByRouter"] is False
        assert cost["providerSessionCreatedByRouter"] is False
        assert consult["handoff"] is None

        replacement = foundation.create(
            "AI_EMPLOYEE", entity_id="employee-reviewer-v2", company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="AVAILABLE", data={"name": "reviewer-v2"},
        )
        router.update_assignment(assignments["reviewer"]["entity_id"], employee_ref=replacement["entity_id"])
        v2 = router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="review-flow", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["development", "test"],
        )
        assert v2["data"]["version"] == 2

        restarted = ResponsibilityRoutingRuntime(Database(database.path))
        completed = restarted.complete_consult(
            work["entity_id"], interaction_key="consult-stable", response="边界可行",
            result_refs=["result:consult"], evidence_refs=["evidence:consult"],
        )
        repeated = restarted.complete_consult(
            work["entity_id"], interaction_key="consult-stable", response="边界可行",
            result_refs=["result:consult"], evidence_refs=["evidence:consult"],
        )
        assert completed["consult"]["status"] == repeated["consult"]["status"] == "COMPLETED"
        assert _current(completed["work"])["workflowRef"] == v1["entity_id"]
        assert _current(completed["work"])["responsibilityHolderRef"] == "employee-development"

        review = restarted.route(
            work["entity_id"], signal="REVIEW", responsibility_key="reviewer",
            problem="审核开发结果", interaction_key="review-approve",
            artifact_refs=["artifact:diff"], evidence_refs=["evidence:test"],
        )
        assert review["review"]["targetEmployeeRef"] == "employee-reviewer"
        assert _current(review["work"])["responsibilityHolderRef"] == "employee-development"
        approved = restarted.resolve_review(
            work["entity_id"], interaction_key="review-approve", outcome="APPROVE",
            response="审核通过", result_refs=["result:development-reviewed"], continue_default=True,
        )
        assert _current(approved["work"])["responsibilityHolderRef"] == "employee-test"
        with database.connect() as conn:
            after_approve = conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0]
        repeated_approve = restarted.resolve_review(
            work["entity_id"], interaction_key="review-approve", outcome="APPROVE",
            response="审核通过", result_refs=["result:development-reviewed"], continue_default=True,
        )
        assert repeated_approve["review"]["routeApplied"] == "HANDOFF"
        with database.connect() as conn:
            assert conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0] == after_approve

        restarted.request_review(
            work["entity_id"], reviewer_responsibility="reviewer", question="缺陷复核",
            interaction_key="review-revision", context_refs=["result:test-failure"],
        )
        revised = restarted.resolve_review(
            work["entity_id"], interaction_key="review-revision", outcome="REQUEST_REVISION",
            response="需要开发修复", evidence_refs=["evidence:defect"], revision_responsibility="development",
        )
        assert _current(revised["work"])["responsibilityHolderRef"] == "employee-development"
        assert revised["routing"]["handoff"]["lifecycle_status"] == "COMPLETED"

        before_same_holder = len(_current(revised["work"])["handoffRefs"])
        restarted.request_review(
            work["entity_id"], reviewer_responsibility="reviewer", question="修订是否仍由开发承担",
            interaction_key="review-same-holder",
        )
        same_holder = restarted.resolve_review(
            work["entity_id"], interaction_key="review-same-holder", outcome="REQUEST_REVISION",
            response="开发继续修订", revision_responsibility="development",
        )
        assert _current(same_holder["work"])["responsibilityHolderRef"] == "employee-development"
        assert len(_current(same_holder["work"])["handoffRefs"]) == before_same_holder

        with database.connect() as conn:
            assert conn.execute("select count(*) from tasks").fetchone()[0] == tasks_before
            assert conn.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == cycles_before
            assert conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0] == handoffs_before + 2
        persisted = ResponsibilityRoutingRuntime(Database(database.path)).foundation.get(work["entity_id"])
        assert set(_current(persisted)["collaborations"]) == {
            "consult-stable", "review-approve", "review-revision", "review-same-holder",
        }


def test_missing_or_ambiguous_assignment_fails_closed(tmp_path):
    database, foundation, router = _seed(tmp_path / "ambiguous-routing.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-routing", role="test"):
        assignments = _assignments(
            foundation, router,
            [("development", False), ("leader-one", True), ("leader-two", True)],
        )
        router.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="ambiguous", assignment_refs=[item["entity_id"] for item in assignments.values()],
            default_flow=["development"],
        )
        work = foundation.create(
            "CYCLE", entity_id="cycle-ambiguous", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING",
        )
        router.start_work(work["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="ambiguous")
        with pytest.raises(ResponsibilityRoutingError, match="not in pinned workflow"):
            router.route(work["entity_id"], signal="CONSULT", responsibility_key="missing", problem="missing")
        with pytest.raises(ResponsibilityRoutingError, match="no Operating Leader"):
            router.route(work["entity_id"], signal="ESCALATE", problem="ambiguous leader")
        with database.connect() as conn:
            assert conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0] == 0

@pytest.mark.parametrize('invalid', [None, 'foreign_scope', 'foreign_role', 'foreign_binding', 'disabled_employee'])
def test_initial_team_connection_helper_checks_uncommitted_scope_and_rolls_back(tmp_path, monkeypatch, invalid):
    from app.runtime import RuntimeScopeError
    database, foundation, router = _seed(tmp_path / 'initial-team-routing.sqlite')
    original = database.connect
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-routing', role='test'):
        with pytest.raises(RuntimeError, match='rollback fixture'):
            with original() as con:
                con.execute('begin immediate')
                con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status,enabled) values ('initial-holder',?,?,'','official.employee.writing.author','章节作者','章节作者','idle',?)", (TENANT, COMPANY, 0 if invalid == 'disabled_employee' else 1))
                for ref, kind, company, data in [('initial-holder','AI_EMPLOYEE',COMPANY,{'companyEmployeeRef':'initial-holder'}), ('initial-role','ROLE_SLOT',COMPANY if invalid != 'foreign_role' else 'foreign',{}), ('foreign-capability','CAPABILITY_BINDING','foreign',{})]:
                    con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,lifecycle_status,data_json,created_at,updated_at) values (?,?,?,?,?,?,current_timestamp,current_timestamp)", (ref,TENANT,kind,company,'AVAILABLE' if kind == 'AI_EMPLOYEE' else 'ASSIGNED',json.dumps(data)))
                # The helper must see uncommitted entities and never open another connection.
                monkeypatch.setattr(database, 'connect', lambda: (_ for _ in ()).throw(AssertionError('second connection forbidden')))
                args = dict(company_id=COMPANY, scope_type='WORKSPACE', scope_ref='foreign' if invalid == 'foreign_scope' else WORKSPACE,
                    workspace_id=WORKSPACE, role_ref='initial-role', employee_ref='initial-holder', responsibility_key='WRITING_CHAPTER_AUTHOR', responsibility='创作、自检、交付、复盘', capability_binding_refs=['foreign-capability'] if invalid == 'foreign_binding' else [])
                if invalid:
                    with pytest.raises(RuntimeScopeError): router.create_assignment_in_connection(con, **args)
                else:
                    result = router.create_assignment_in_connection(con, **args)
                    assert con.execute('select entity_id from runtime_entities where entity_id=?', (result['entity_id'],)).fetchone()
                    assert len(con.execute('select * from runtime_links where source_id=?', (result['entity_id'],)).fetchall()) == 2
                raise RuntimeError('rollback fixture')
    monkeypatch.setattr(database, 'connect', original)
    with original() as con:
        assert con.execute("select count(*) from employee_instances where id='initial-holder'").fetchone()[0] == 0
        assert con.execute("select count(*) from runtime_entities where entity_id='initial-role' or entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchone()[0] == 0
        assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'


@pytest.mark.parametrize("terminal", ["COMPLETED", "CANCELLED", "ARCHIVED"])
def test_legacy_active_route_on_terminal_work_cannot_continue(tmp_path, terminal):
    database, foundation, router = _seed(tmp_path / "terminal.sqlite")
    with TenantContext.scope(TENANT):
        work = foundation.create("CYCLE", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "synthetic"})
        with database.connect() as con:
            data = dict(work["data"], responsibilityRouting={"status": "ACTIVE", "currentExecutorRef": "old-executor"})
            con.execute("update runtime_entities set lifecycle_status=?,data_json=? where tenant_id=? and entity_id=?",
                (terminal, json.dumps(data), TENANT, work["entity_id"]))
        before = foundation.get(work["entity_id"])
        with pytest.raises(ResponsibilityRoutingError, match="no active responsibility route"):
            router.route(work["entity_id"], signal="CONTINUE")
        assert foundation.get(work["entity_id"]) == before
