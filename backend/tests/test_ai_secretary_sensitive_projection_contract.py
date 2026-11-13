import json
import re
from pathlib import Path

from app.database import Database


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = (
    REPO_ROOT
    / "issues"
    / "20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md"
)

DIRECT_ALLOWLISTS = {
    "workflow_runs": {
        "tenant_id",
        "workflow_run_id",
        "company_id",
        "project_id",
        "workflow_instance_id",
        "workflow_template_id",
        "department_id",
        "task_id",
        "created_at",
        "status",
    },
    "step_results": {
        "tenant_id",
        "step_result_id",
        "workflow_step_id",
        "employee_id",
        "created_at",
        "status",
    },
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


def _allowlist_section() -> str:
    return _contract().split("## 分来源可返回最小字段", 1)[1].split("## 结果", 1)[0]


def test_each_source_allowlist_uses_real_schema_fields(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "secretary-sensitive-projection.sqlite"))
    database.initialize()
    with database.connect() as connection:
        for table, expected in DIRECT_ALLOWLISTS.items():
            actual = {row["name"] for row in connection.execute(f"pragma table_info({table})")}
            assert expected <= actual


def test_exact_source_specific_allowlists_are_fixed() -> None:
    text = _allowlist_section()
    assert "`tenant_id`、`workflow_run_id`、`company_id`、`project_id`、`workflow_instance_id`、`workflow_template_id`、`department_id`、`task_id`、`created_at`、`status`" in text
    assert "`tenant_id`、`step_result_id`、`workflow_step_id`、`employee_id`、`created_at`、`status`" in text
    assert "`tenant_id`、`package_id`、`created_at`、`status`" in text
    assert "`tenant_id`、`run_id`、`workflow_content_id`、`department_id`、`created_at`、`status`" in text


def test_only_verified_step_chain_can_add_workflow_run_id() -> None:
    text = _allowlist_section()
    assert "step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id)" in text
    assert "workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)" in text
    assert "该 `run_id` 只代表内容状态机，不得改名或推断为 RD `workflow_run_id`" in text


def test_generic_aliases_hashes_and_bare_text_are_not_allowlisted() -> None:
    text = _allowlist_section()
    assert "不允许通用 `source_run_id`、`source_step_id`、`source_result_hash`" in text
    assert "`result`、`final_report`、`summary`、`artifacts`、`source_workflow`、`next_step_hint` 均不在本最小 allowlist" in text
    assert "不得以现场哈希、摘要、默认值或裸文本替代来源引用" in text


def test_denylist_hit_reuses_the_global_two_field_403_response() -> None:
    text = _contract()
    body_match = re.search(r"固定响应体：`({.*})`", text)
    assert body_match is not None
    assert json.loads(body_match.group(1)) == {
        "error_code": "secretary_source_forbidden",
        "message": "Source access is not allowed.",
    }
    assert "唯一 HTTP 状态为 `403`" in text
    assert "响应体只允许 `error_code`、`message`" in text
    assert "不得剔除后继续，不得返回 partial、空对象、`summary` 或 `next_step_hint`" in text


def test_security_log_and_template_boundaries_are_exact() -> None:
    text = _contract()
    assert "`SENSITIVE_PROJECTION_REJECTED` 仅作为内部固定日志 `fail_code`" in text
    assert "不得进入对外响应" in text
    assert "日志只允许 `timestamp`、`tenant_id`、`project_id`、`run_id`、`task_id`、`fail_code`、`step` 七个字段" in text
    assert "任意字段、嵌套字段或敏感文本伪装命中 denylist" in text
    assert "内容来自预定义非敏感状态模板" in text
    assert "无法证明模板来源或安全性时省略该字段" in text
