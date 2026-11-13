"""TEST_ONLY ledger read fixtures; no Provider calls or real billing evidence."""
from fastapi.testclient import TestClient
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import seed, add_team, app, COMPANY, WORKSPACE, TENANT, BUSINESS


def test_scoped_usage_reads_empty_unknown_and_multiple_attempts_without_writes(tmp_path):
    database = seed(tmp_path / "work-usage.sqlite")
    add_team(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        ref = GeneralWorkspaceDelivery(database).create_work(company_id=COMPANY, workspace_id=WORKSPACE,
            problem="TEST_ONLY ledger view", expected_result="read only", constraints=[], references=[],
            idempotency_key="usage")["work"]["entity_id"]
    path = f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{ref}/usage"
    with TestClient(app(database)) as client:
        empty = client.get(path)
        assert empty.status_code == 200 and empty.json()["records"] == []
        with database.connect() as connection:
            for index, (work_ref, tenant, company, ws) in enumerate([
                (ref,TENANT,COMPANY,WORKSPACE), (ref,TENANT,COMPANY,WORKSPACE),
                ("other-work",TENANT,COMPANY,WORKSPACE), (ref,"foreign",COMPANY,WORKSPACE),
                (ref,TENANT,"other-company",WORKSPACE), (ref,TENANT,COMPANY,"other-ws"),
            ]):
                # Deliberate isolated read-model fixtures, not trusted record_call or live Usage acceptance.
                connection.execute("insert into ai_usage_records(usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,model_name,"
                    "currency,cost_source,employee_id,capability_id,capability_type,task_id,department_id,business_id,workspace_id,work_ref,"
                    "execution_ref,request_id,execution_status,metering_status,occurred_at,idempotency_key,logical_call_id,attempt_no) "
                    "values (?,?,?,'TEST_ONLY','TEST_ONLY','TEST_ONLY','USD','unknown','test-employee','test-capability','model',"
                    "'test-task','department',?,?,?,'test-execution',?,'failed','unknown','2026-10-16T00:00:00Z',?,'same-logical',?)",
                    (f"usage-{index}",tenant,company,BUSINESS,ws,work_ref,f"request-{index}",f"usage-key-{index}",index+1))
        records = client.get(path).json()["records"]
        assert len(records) == 2
        assert {x["attempt_no"] for x in records} == {1,2}
        assert all(x["total_tokens"] is None and x["cost_amount"] is None for x in records)
        assert client.get(path.replace(COMPANY,"other-company")).status_code == 404
        assert client.get(path.replace(WORKSPACE,"other-ws")).status_code == 404
        assert client.get(path.replace(ref,"missing")).status_code == 404
        assert client.get(path).json()["records"] == records
        with database.connect() as connection:
            assert connection.execute("select count(*) from ai_usage_records").fetchone()[0] == 6
