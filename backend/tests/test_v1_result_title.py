import json

from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext
from backend.tests.test_shared_workspace_projection import _seed, TENANT, COMPANY, WORKSPACE, CEO


def test_result_title_uses_scoped_business_problem_not_execution_prompt(tmp_path):
    database, *_ = _seed(tmp_path / "titles.sqlite")
    with database.connect() as connection:
        connection.execute(
            "update tasks set workspace_id=?, work_ref='title-work', content=? where tenant_id=?",
            (WORKSPACE, '工作目标：测试\n业务上下文：{"private_ref":"internal"}', TENANT),
        )
        connection.execute(
            "insert into runtime_entities(entity_id, tenant_id, company_id, workspace_id, entity_type, "
            "parent_id, lifecycle_status, data_json, created_at, updated_at) "
            "values ('title-work',?,?,?,?,?,'PLANNED',?,current_timestamp,current_timestamp)",
            (TENANT, COMPANY, WORKSPACE, "WORK", "cycle-shared", json.dumps({"goal": "修复计算错误"})),
        )
        task = connection.execute("select task_id from tasks where tenant_id=? limit 1", (TENANT,)).fetchone()
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        result = SharedWorkspaceProjection(database).result(COMPANY, WORKSPACE, f"task:{task['task_id']}")
    assert result["title"] == "修复计算错误"
    assert "private_ref" not in result["title"]


def test_business_result_count_reuses_workspace_result_truth(tmp_path):
    from app.runtime.business_spine import CanonicalBusinessSpine
    database, *_ = _seed(tmp_path / "business-results.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        snapshot = SharedWorkspaceProjection(database).workspace(COMPANY, WORKSPACE)
        business = CanonicalBusinessSpine(database).get_business(COMPANY, snapshot["business"]["business_id"])
        assert snapshot["results"]
        assert business["operatingSummary"]["resultCount"] == len(snapshot["results"])


def test_meeting_workflow_does_not_change_general_readiness(tmp_path):
    from backend.tests.test_v1_general_operating_contract import seed, add_team, TENANT as tenant, COMPANY as company, WORKSPACE as workspace
    from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
    database = seed(tmp_path / "meeting-readiness.sqlite")
    add_team(database)
    with TenantContext.scope(tenant, company_id=company, ceo_id="ceo", role="test"):
        projection = SharedWorkspaceProjection(database)
        before = projection.general_workspace(company, workspace)
        workflow = RuntimeFoundation(database).list("RESPONSIBILITY_WORKFLOW", company_id=company, workspace_id=workspace)[0]
        ResponsibilityRoutingRuntime(database).publish_workflow(
            company_id=company, workspace_id=workspace, scope_type="WORKSPACE", scope_ref=workspace,
            workflow_key="meeting:projection-test", assignment_refs=[item["assignmentRef"] for item in workflow["data"]["assignments"]],
            default_flow=workflow["data"]["defaultFlow"],
        )
        after = projection.general_workspace(company, workspace)
        assert after["operating_readiness"] == before["operating_readiness"]
