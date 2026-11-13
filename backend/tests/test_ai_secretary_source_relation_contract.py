from pathlib import Path

from app.database import Database


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = (
    REPO_ROOT
    / "issues"
    / "20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md"
)

RELATION_COLUMNS = {
    "workflow_runs": {
        "tenant_id",
        "workflow_run_id",
        "company_id",
        "project_id",
        "workflow_instance_id",
        "workflow_template_id",
        "department_id",
        "task_id",
    },
    "workflow_steps": {"tenant_id", "workflow_step_id", "workflow_run_id"},
    "step_results": {"tenant_id", "step_result_id", "workflow_step_id", "employee_id"},
    "content_publish_packages": {"tenant_id", "package_id", "source_workflow"},
    "content_workflow_runs": {"tenant_id", "run_id", "workflow_content_id", "department_id"},
}


def _contract() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8")


def test_relation_columns_match_fresh_database_schema(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "secretary-source-contract.sqlite"))
    database.initialize()
    with database.connect() as connection:
        for table, expected in RELATION_COLUMNS.items():
            actual = {row["name"] for row in connection.execute(f"pragma table_info({table})")}
            assert expected <= actual
        step_result_columns = {
            row["name"] for row in connection.execute("pragma table_info(step_results)")
        }
        assert "workflow_run_id" not in step_result_columns


def test_step_result_uses_only_the_real_tenant_scoped_run_path() -> None:
    text = _contract()
    assert "step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id)" in text
    assert "workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)" in text
    assert "`workflow_runs.id`" not in text
    assert "`step_results.workflow_run_id`" not in text


def test_content_sources_stay_source_local_and_fail_closed() -> None:
    text = _contract()
    assert "`source_workflow` 是本源文本，不是到 RD `workflow_runs` 的外键" in text
    assert "该 `run_id` 不关联 RD `workflow_runs.workflow_run_id`" in text
    assert text.count("请求要求证明本表没有的 project/company/RD workflow 关系时即 `403`") == 2


def test_inference_shortcuts_are_explicitly_forbidden() -> None:
    text = _contract()
    for forbidden in ("同名 `run_id`", "名称匹配", "字符串拼接", "默认值", "“最近一次”推断"):
        assert forbidden in text
    assert "任一错配即立即停止，不执行任何后续对象读取" in text
