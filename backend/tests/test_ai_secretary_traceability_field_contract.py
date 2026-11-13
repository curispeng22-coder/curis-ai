from pathlib import Path

from app.database import Database


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = (
    REPO_ROOT
    / "issues"
    / "20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md"
)

TRACE_FIELDS = {
    "workflow_runs": {
        "tenant_id",
        "workflow_run_id",
        "company_id",
        "project_id",
        "workflow_instance_id",
        "workflow_template_id",
        "department_id",
        "task_id",
        "status",
        "created_at",
        "updated_at",
        "started_at",
        "completed_at",
        "failed_at",
    },
    "step_results": {
        "tenant_id",
        "step_result_id",
        "workflow_step_id",
        "employee_id",
        "status",
        "created_at",
    },
    "workflow_steps": {"tenant_id", "workflow_step_id", "workflow_run_id"},
    "content_publish_packages": {
        "tenant_id",
        "package_id",
        "source_workflow",
        "status",
        "created_at",
        "updated_at",
    },
    "content_workflow_runs": {
        "tenant_id",
        "run_id",
        "workflow_content_id",
        "department_id",
        "status",
        "created_at",
        "updated_at",
    },
}


def _contract() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8")


def test_traceability_fields_exist_in_fresh_database_schema(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "secretary-traceability-contract.sqlite"))
    database.initialize()
    with database.connect() as connection:
        for table, expected in TRACE_FIELDS.items():
            actual = {row["name"] for row in connection.execute(f"pragma table_info({table})")}
            assert expected <= actual
            assert "source_result_hash" not in actual


def test_required_trace_fields_are_source_specific() -> None:
    text = _contract()
    for fields in (
        "`tenant_id`、`workflow_run_id`、`created_at`",
        "`tenant_id`、`step_result_id`、`workflow_step_id`、`created_at`",
        "`tenant_id`、`package_id`、`created_at`",
        "`tenant_id`、`run_id`、`created_at`",
    ):
        assert f"必选直出：{fields}" in text
    assert "`source_result_hash`，因此它不是必选或默认返回字段" in text


def test_only_step_results_can_follow_the_verified_run_path() -> None:
    text = _contract()
    assert "step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id)" in text
    assert "workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)" in text
    assert "`source_workflow` 是本源文本，不是 RD Run/Step/Result 外键" in text
    assert "该 `run_id` 是内容状态机本源 ID，不等于 RD `workflow_runs.workflow_run_id`" in text


def test_missing_relations_cannot_be_inferred_from_text_or_ids() -> None:
    text = _contract()
    for forbidden in (
        "同名 ID",
        "字符串拼接",
        "默认值",
        "“最近一次”推断",
        "禁止现场哈希裸 `result`、`final_report`、`summary` 或 `artifacts`",
    ):
        assert forbidden in text
    assert "关系无法由上述路径证明，立即拒绝且不返回部分追溯字段" in text
