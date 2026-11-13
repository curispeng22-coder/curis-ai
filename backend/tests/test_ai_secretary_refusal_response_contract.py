import json
import re
from pathlib import Path


ISSUE_PATH = (
    Path(__file__).resolve().parents[2]
    / "issues"
    / "20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md"
)

EXPECTED_RESPONSES = {
    401: {
        "error_code": "secretary_access_required",
        "message": "Access context is required.",
    },
    400: {
        "error_code": "secretary_request_invalid",
        "message": "Request is invalid.",
    },
    403: {
        "error_code": "secretary_source_forbidden",
        "message": "Source access is not allowed.",
    },
    404: {
        "error_code": "secretary_source_unavailable",
        "message": "Source is unavailable.",
    },
}


def _contract_text() -> str:
    return ISSUE_PATH.read_text(encoding="utf-8")


def _response_table() -> dict[int, dict[str, str]]:
    rows = re.findall(r'^\| (40[0134]) \| `({.*})` \|$', _contract_text(), re.MULTILINE)
    return {int(status): json.loads(body) for status, body in rows}


def test_exact_refusal_bodies_are_complete_and_unique() -> None:
    assert _response_table() == EXPECTED_RESPONSES


def test_refusal_bodies_expose_only_the_two_approved_fields() -> None:
    for body in _response_table().values():
        assert set(body) == {"error_code", "message"}


def test_same_status_body_cannot_vary_by_source_or_visibility() -> None:
    text = _contract_text()
    assert "同一 HTTP 类别下" in text
    assert "来源对象、ID、实体是否存在、状态不可读或关联失配" in text
    assert "响应体必须与上表完全一致" in text
    assert "四类来源对象的存在/不存在、状态不可读、作用域失配反例" in text


def test_rejection_precedence_and_query_short_circuit_are_fixed() -> None:
    text = _contract_text()
    assert "`401 > 400 > 403 > 404`" in text
    assert "仅输出一个状态码；拒绝后不得查询关联表" in text
