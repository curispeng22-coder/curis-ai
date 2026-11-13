"""T8 边缘用例（QA 独立补充）：员工自我判断门控的边界行为。

覆盖团队要求的 3 个边缘场景，并额外加入一个「全局 budget 硬上限」独立校验：
- confidence 极低但 should_speak=True 仍应进入候选（轻量门控不得因置信度低而否决资格）
- 全局 budget 在门控循环中途中耗尽 → 剩余候选必须被安全跳过、不产生发言
- 同一员工两轮自我判断：先 STAY_SILENT、后出现新观点后主动 SPEAK（re-intervention）
- 全局 budget 硬上限独立校验：门控循环恰好把 count 推到 30 后，speaker/leader 调用
  不得再继续把 count 推过 30（约束 #5「任何情况不绕过」/ #6「达上限即安全停止」）

运行（repo 根目录，需隔离 DB 环境变量）：
  CURIS_DB=/tmp/curis_test.sqlite CURIS_DB_PATH=/tmp/curis_test.sqlite \
  CURIS_WORKSPACE_DB=/tmp/curis_test.sqlite CURIS_ENV=test CURIS_IDENTITY_MODE=test \
  backend/.venv/bin/python -m pytest backend/tests/test_v1_meeting_self_judgment_edge.py -q
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app
from app.meeting_service import MeetingService
from app.tenant_context import TenantContext

from backend.tests.test_v1_meeting_autonomous_discussion import (
    BUSINESS, COMPANY, HEADERS, PREFIX, TENANT, WORKSPACE,
    MeetingProvider, seed,
)


def _gate_usage() -> dict:
    return {"confirmedTokens": 0, "confirmedCost": "0", "unknownMetering": False}


def _judgment(*, should_speak: bool, accepted: bool = True, confidence: float = 0.9,
              reason: str = "") -> dict:
    return {
        "should_speak": should_speak,
        "contribution": "我补充一项基于当前合法资料的可验证判断。",
        "confidence": confidence,
        "reason": reason or ("我对该议题有新增相关性。" if should_speak else "本轮我没有可补充的新事实。"),
        "usage": _gate_usage(), "taskRef": "task-self-judgment",
        "workRef": "work-self-judgment", "accepted": accepted,
    }


def _create_meeting(database, employees, *, context_refs=None, title="客户研究与执行方案"):
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        meeting = MeetingService(database).create(
            company_id=COMPANY, business_id=BUSINESS, workspace_id=WORKSPACE,
            title=title, background="先确认客户事实，再形成验证方案",
            participant_refs=[item[0] for item in employees.values()],
            leader_ref=employees["leader"][0], ceo_participation_mode="DECISION_ONLY",
            context_refs=context_refs or [],
        )
    return meeting["meeting_id"]


def _patch_orchestration(database, meeting_id, patch: dict) -> None:
    from backend.tests.test_v1_meeting_employee_self_judgment import _patch_orchestration as patch_cycle
    patch_cycle(database, meeting_id, patch)


def test_confidence_extremely_low_but_speak_still_enters_candidates(tmp_path, monkeypatch):
    """门控 confidence 极低（0.01）但 should_speak=True → 仍进入候选并获发言资格。

    验证轻量门控只以 should_speak 决定资格，不拿 confidence 做否决（要求 #2/#4）。
    """
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-edge-low-confidence.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    research = employees["research"][0]
    operations = employees["operations"][0]

    async def fake_gate(self, meeting, assignment, event, context):  # noqa: ARG001
        ref = assignment["employeeRef"]
        # 一名员工自信度极低但判断应发言；另一名正常自信。
        return _judgment(
            should_speak=True,
            confidence=0.01 if ref == research else 0.9,
        )

    monkeypatch.setattr(MeetingService, "_employee_self_judgment", fake_gate)
    meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}])

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    assert orchestration["status"] != "BLOCKED"
    turns = orchestration["turns"]
    assert turns, "应至少完成一个回合"
    turn = turns[0]
    # 低置信度员工：should_speak=True 被如实持久化，且进入了候选（未被 confidence 否决）
    assert turn["selfJudgments"][research]["should_speak"] is True
    assert turn["selfJudgments"][research]["confidence"] == 0.01
    assert research in [item["employeeRef"] for item in turn["candidates"]]
    # 低置信度不等于沉默：不应出现在 silences 中
    assert research not in [item["employeeRef"] for item in turn["silences"]]


def test_budget_exhausted_mid_gate_loop_skips_remaining_candidates(tmp_path, monkeypatch):
    """全局 budget 在门控循环中途中耗尽 → 剩余候选被安全跳过，不产生任何发言（约束 #6）。

    预置 providerCallCount=29，两名员工都应发言；第 1 次门控用掉后达到 30，
    第 2 名员工的门控必须在预算闸门前停住，会议进入 BLOCKED，不出现任何发言回合。
    """
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-edge-budget-mid.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    calls = {"gate": 0}

    async def fake_gate(self, meeting, assignment, event, context):  # noqa: ARG001
        calls["gate"] += 1
        return _judgment(should_speak=True)

    monkeypatch.setattr(MeetingService, "_employee_self_judgment", fake_gate)
    research = employees["research"][0]
    operations = employees["operations"][0]
    meeting_id = _create_meeting(database, employees)
    _patch_orchestration(database, meeting_id, {"providerCallCount": 29})

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    # 只发起了 1 次门控；第 2 名候选（operations）在预算闸门前被安全跳过，从未被门控
    assert calls["gate"] == 1, f"预算耗尽后仍发起了 {calls['gate']} 次门控调用"
    assert orchestration["status"] == "BLOCKED"
    assert orchestration["blockedReason"] == "模型调用已达到本次会议安全上限"
    assert orchestration["providerCallCount"] == 30
    # 没有任何员工发言（剩余候选被正确处理）
    assert not any(
        item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE" for item in detail["timeline"]
    )
    assert orchestration["turns"] == []
    assert research != operations  #  sanity：确为两名不同候选


def test_same_employee_silent_then_reenters_and_speaks(tmp_path, monkeypatch):
    """同一员工两轮自我判断：轮1 STAY_SILENT，出现新观点后轮2 主动 SPEAK（要求 #6）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-edge-reintervention.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    research = employees["research"][0]
    operations = employees["operations"][0]

    def decide(employee_ref: str, call_number: int, _prompt: str) -> bool:
        # research：第 1 次门控保持沉默；第 2 次（他人已发言/出现新 Evidence）重新介入
        if employee_ref == research:
            return call_number >= 2
        # operations：始终发言，制造"他人新观点"触发 research 重新介入
        return True

    provider.gate_decision_fn = decide
    meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}])

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    turns = detail["orchestration"]["turns"]
    assert len(turns) >= 2, f"需要至少两个回合验证重新介入，实际 {len(turns)}"
    # 轮1：research 沉默（被记录），operations 发言
    assert turns[0]["selfJudgments"][research]["should_speak"] is False
    assert [item["employeeRef"] for item in turns[0]["silences"]] == [research]
    # 轮2：research 因新观点重新介入（should_speak 翻转为 True，且不再是沉默者）
    assert turns[1]["selfJudgments"][research]["should_speak"] is True
    assert research not in [item["employeeRef"] for item in turns[1].get("silences", [])]


def test_global_budget_cap_not_exceeded_after_gate_loop(tmp_path, monkeypatch):
    """约束 #5/#6 独立校验：门控循环恰好把 count 推到 30 后，speaker/leader 调用不得再越过 30。

    预置 providerCallCount=28，两名员工都应发言：门控循环把 count 推到 30，
    若实现正确，本轮 speaker 与 leader 调用应在预算闸门前停住（或整体在 30 内收口），
    providerCallCount 不得超过 30。
    """
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-edge-budget-cap.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    # 两名员工都发言，使门控循环跑满两次调用
    provider.gate_decisions = {
        employees["research"][0]: True, employees["operations"][0]: True,
    }
    meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}])
    _patch_orchestration(database, meeting_id, {"providerCallCount": 28})

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    # 严格约束：任何情况下全局 provider call 上限不得被越过（#5），达上限即安全停止（#6）
    assert orchestration["providerCallCount"] <= int(MeetingService.LIMITS["maxProviderCalls"]), (
        f"providerCallCount={orchestration['providerCallCount']} 越过了全局上限 "
        f"{MeetingService.LIMITS['maxProviderCalls']}（门控循环后 speaker/leader 仍被调用）"
    )
