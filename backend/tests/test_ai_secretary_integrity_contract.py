import json
import re
from pathlib import Path

from app.database import Database


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = (
    REPO_ROOT
    / "issues"
    / "20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md"
)

INTEGRITY_FIELDS = {
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
    },
    "workflow_steps": {"tenant_id", "workflow_step_id", "workflow_run_id"},
    "step_results": {"tenant_id", "step_result_id", "workflow_step_id", "status"},
    "content_publish_packages": {"tenant_id", "package_id", "created_at", "status"},
    "content_workflow_runs": {
        "tenant_id",
        "run_id",
        "workflow_content_id",
        "department_id",
        "created_at",
        "status",
    },
}


def _contract() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8")


def test_integrity_fields_exist_in_fresh_database_schema(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "secretary-integrity-contract.sqlite"))
    database.initialize()
    with database.connect() as connection:
        for table, expected in INTEGRITY_FIELDS.items():
            actual = {row["name"] for row in connection.execute(f"pragma table_info({table})")}
            assert expected <= actual


def test_step_result_uses_only_the_verified_tenant_scoped_run_path() -> None:
    text = _contract()
    assert "step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id)" in text
    assert "workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)" in text
    assert "不存在 `step_results.workflow_run_id`" in text
    assert "不得补 `source_run_id/source_step_id/source_result_id` 通用别名" in text


def test_content_sources_remain_source_local() -> None:
    text = _contract()
    assert "`source_workflow` 是本源文本，不是 RD Run/Step/Result 外键" in text
    assert "该 `run_id` 只属于内容状态机，不等于 RD `workflow_runs.workflow_run_id`" in text
    assert "本表没有可证路径的关系为 `403`" in text
    assert "请求关系没有可证路径为 `403`" in text


def test_relationship_response_categories_match_8a() -> None:
    text = _contract()
    assert "schema 无法证明请求所需关系为 `403`" in text
    assert "任一必经对象或中间行缺失/不可见为 `404`" in text
    assert "对象均存在但 tenant、Step→Run 或 Run 作用域值错配为 `403`" in text


def test_mismatch_and_missing_rows_use_global_fixed_responses() -> None:
    bodies = {
        int(status): json.loads(body)
        for status, body in re.findall(r"：`(40[34])`，固定体 `({.*})`", _contract())
    }
    assert bodies == {
        403: {"error_code": "secretary_source_forbidden", "message": "Source access is not allowed."},
        404: {"error_code": "secretary_source_unavailable", "message": "Source is unavailable."},
    }


def test_conflict_and_stale_context_are_internal_404_fail_codes() -> None:
    text = _contract()
    for fail_code in ("CONFLICT", "STALE_CONTEXT"):
        assert f"`{fail_code}`" in text
    assert text.count("仅写内部 `fail_code`，对外映射 `404`") == 2
    assert "不得对外使用 `409`、`423`" in text
    assert "对外响应只允许 `error_code`、`message`" in text


def test_tampered_text_templates_and_fallback_attempts_fail_closed() -> None:
    text = _contract()
    assert "8a.3b 安全批准的预定义非敏感状态模板" in text
    assert "来源、模板或完整性验证失败时优先省略" in text
    for forbidden in (
        "现场哈希",
        "同名 ID",
        "字符串拼接",
        "默认值",
        "“最近一次”",
        "裸文本",
        "篡改文本",
        "历史版本替代",
        "自动 fallback",
    ):
        assert forbidden in text
    assert "拒绝后不继续查询关联对象" in text
    assert "在 Adapter/模型调用/出网前完成" in text
    assert "日志不得包含 prompt、payload、token、credential" in text
