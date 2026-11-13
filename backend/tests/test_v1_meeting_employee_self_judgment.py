"""T8 单元验证：Meeting 员工自我 Speak / Stay-Silent 判断门控。

覆盖设计稿 `docs/reviews/CURIS_V1_MEETING_EMPLOYEE_SELF_JUDGMENT_DESIGN_2026-09-04.md`
中 (d.1) 的单元用例，以及用户 9 条硬约束里与门控直接相关的几条：

- #2 门控 True  → 进入候选并发言
- #5 门控 False → 被过滤，且沉默理由落库（STAY_SILENT 是一等合法结果）
- #6 达到全局 budget 后安全停止，绝不继续调用
- 失败真值：门控 accepted=False → BLOCKED，且不产生任何假发言 / 假 Work
- Leader 安全边界：连发保护仍然生效
- 要求 #6（产品）：因他人新 Evidence 重新介入
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
    """门控用量替身：结构与 `_usage_for_task` 一致，供 `_merge_usage` 消费。"""
    return {"confirmedTokens": 0, "confirmedCost": "0", "unknownMetering": False}


def _judgment(*, should_speak: bool, accepted: bool = True, reason: str = "") -> dict:
    return {
        "should_speak": should_speak,
        "contribution": "我补充一项基于当前合法资料的可验证判断。",
        "confidence": 0.9,
        "reason": reason or ("我对该议题有新增相关性。" if should_speak else "本轮我没有可补充的新事实。"),
        "usage": _gate_usage(), "taskRef": "task-self-judgment",
        "workRef": "work-self-judgment", "accepted": accepted,
    }


def _create_meeting(database, employees, *, context_refs=None, title="客户研究与执行方案"):
    """直接建会（不经 HTTP），避免建会即自动推进，保证 advance 可显式控制。"""
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
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        if {"providerCallCount", "noProgressCount", "usage"} & patch.keys():
            # Seed consumption inside a real claimed cycle, not lifetime totals.
            service._claim_advance(meeting_id)

            def apply(state):
                state.update(patch)
                if state.get("currentCycle"):
                    state["currentCycle"].update({key: patch[key] for key in ("providerCallCount", "usage") if key in patch})
                state.update(activeRunId="", runStartedAt=None)
                return state

            service._update_orchestration(meeting_id, apply)
        else:
            service._update_orchestration(meeting_id, lambda state: state | patch)


def test_stay_silent_is_filtered_and_recorded(tmp_path, monkeypatch):
    """门控 False 的员工被过滤，沉默理由写入 turn.silences 与 state.silences（要求 #5）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-silent.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    provider.leaders = 3  # 每轮 leader 都判 DISCUSSION_SUFFICIENT，一次 advance 只跑一轮
    research = employees["research"][0]
    operations = employees["operations"][0]
    provider.gate_decisions = {research: True, operations: False}

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}])
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    turns = detail["orchestration"]["turns"]
    assert turns, "应至少完成一个回合"
    turn = turns[0]
    # SPEAK → 进入候选并成为发言者
    assert turn["selfJudgments"][research]["should_speak"] is True
    assert turn["speakerRef"] == research
    # STAY_SILENT → 被过滤出候选，并记录沉默理由
    assert turn["selfJudgments"][operations]["should_speak"] is False
    assert operations not in [item["employeeRef"] for item in turn["candidates"]]
    assert [item["employeeRef"] for item in turn["silences"]] == [operations]
    assert turn["silences"][0]["reason"], "沉默必须带理由"
    assert turn["silences"][0]["eventId"]
    # 沉默只在回合 COMPLETED 时落库
    assert [item["employeeRef"] for item in detail["orchestration"]["silences"]] == [operations]
    # STAY_SILENT 不是异常：会议正常收敛，没有被 BLOCKED
    assert detail["orchestration"]["status"] != "BLOCKED"


def test_all_stay_silent_stops_as_legal_no_progress(tmp_path, monkeypatch):
    """全体员工沉默 → noProgressCount++，达到 maxNoProgress 后 NO_PROGRESS 停止（要求 #5）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-all-silent.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    provider.gate_decisions = {
        employees["research"][0]: False, employees["operations"][0]: False,
    }
    meeting_id = _create_meeting(database, employees)
    # 预置 noProgressCount = maxNoProgress - 1，使本轮沉默即触发终止
    _patch_orchestration(database, meeting_id, {"noProgressCount": 1})

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    assert orchestration["status"] == "NO_PROGRESS"
    assert orchestration["lastOutcome"] == "DISCUSSION_SUFFICIENT"
    assert orchestration["noProgressCount"] >= 2
    # 没有任何人发言，且没有伪造发言
    assert not any(
        item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE" for item in detail["timeline"]
    )
    # 门控确实被调用过（沉默是员工判断出来的，不是被跳过的）
    assert provider.gates >= 1
    # 未完成的回合不落库沉默记录（Restart 幂等）
    assert orchestration.get("silences", []) == []


def test_employee_reenters_after_new_evidence(tmp_path, monkeypatch):
    """轮1 沉默的员工，在出现新 Evidence 后重新介入发言（产品要求 #6）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-reentry.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    research = employees["research"][0]
    operations = employees["operations"][0]

    def decide(employee_ref: str, call_number: int, _prompt: str) -> bool:
        # 第1轮 research 选择沉默；拿到新 Evidence 后（第2轮起）重新介入。
        if employee_ref == research:
            return call_number >= 2
        return call_number == 1  # operations 只在第1轮发言，制造"他人新观点"

    provider.gate_decision_fn = decide
    meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}])

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    turns = detail["orchestration"]["turns"]
    assert len(turns) >= 2, f"需要至少两个回合验证重新介入，实际 {len(turns)}"
    # 第1轮：research 沉默（被记录），operations 发言
    assert turns[0]["selfJudgments"][research]["should_speak"] is False
    assert turns[0]["speakerRef"] == operations
    assert [item["employeeRef"] for item in turns[0]["silences"]] == [research]
    # 第2轮：research 因新 Evidence 重新介入并成为发言者
    assert turns[1]["selfJudgments"][research]["should_speak"] is True
    assert turns[1]["speakerRef"] == research
    assert turns[1]["silences"] == [] or research not in [
        item["employeeRef"] for item in turns[1]["silences"]
    ]


def test_gate_budget_stop_is_safe_and_makes_no_further_calls(tmp_path, monkeypatch):
    """达到全局 maxProviderCalls 后安全停止：不再发起任何门控调用（约束 #6）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-budget.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    calls = {"count": 0}

    async def fake_gate(self, meeting, assignment, event, context):  # noqa: ARG001
        calls["count"] += 1
        return _judgment(should_speak=True)

    monkeypatch.setattr(MeetingService, "_employee_self_judgment", fake_gate)
    meeting_id = _create_meeting(database, employees)
    # 预算只剩 1 次：第一次门控用掉后，第二次门控前必须安全停止
    _patch_orchestration(database, meeting_id, {"providerCallCount": 29})

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    # 只发起了 1 次门控调用，随后在预算闸门前停住，没有继续调用
    assert calls["count"] == 1, f"预算耗尽后仍发起了 {calls['count']} 次门控调用"
    assert orchestration["status"] == "BLOCKED"
    assert orchestration["blockedReason"] == "模型调用已达到本次会议安全上限"
    assert orchestration["providerCallCount"] == 30
    # 安全停止：没有伪造发言、没有产生回合
    assert not any(
        item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE" for item in detail["timeline"]
    )
    assert orchestration["turns"] == []


def test_gate_contract_failure_blocks_without_fake_speech(tmp_path, monkeypatch):
    """门控 accepted=False → BLOCKED，且不产生假发言 / 假 Work / 假回合。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-failed.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)

    async def fake_gate(self, meeting, assignment, event, context):  # noqa: ARG001
        return _judgment(should_speak=True, accepted=False)

    monkeypatch.setattr(MeetingService, "_employee_self_judgment", fake_gate)
    meeting_id = _create_meeting(database, employees)

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    orchestration = detail["orchestration"]
    assert orchestration["status"] == "BLOCKED"
    assert orchestration["blockedReason"] == "员工自我判断模型调用或结果合同验证失败。"
    assert not any(
        item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE" for item in detail["timeline"]
    )
    assert orchestration["turns"] == []
    assert orchestration["turnCount"] == 0


def test_consecutive_protection_still_applies_after_gate(tmp_path, monkeypatch):
    """门控不破坏 Leader 安全边界：maxConsecutiveTurns 连发保护依然生效（要求 #1）。"""
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-gate-consecutive.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    research = employees["research"][0]
    operations = employees["operations"][0]

    def fake_candidate_evaluation(self, meeting, event, assignments):  # noqa: ARG001
        # 两名员工都给正分，使连发保护的"换人"分支可达（真实公式下 operations 恒为 0）
        return [
            {
                "employeeRef": ref, "runtimeEmployeeRef": assignments[ref]["runtimeEmployeeRef"],
                "assignmentRef": assignments[ref]["assignmentRef"], "score": score,
                "reasons": ["测试替身"], "selected": False,
            }
            for ref, score in ((research, 50), (operations, 40))
        ]

    monkeypatch.setattr(MeetingService, "_candidate_evaluation", fake_candidate_evaluation)

    async def fake_gate(self, meeting, assignment, event, context):  # noqa: ARG001
        return _judgment(should_speak=True)

    monkeypatch.setattr(MeetingService, "_employee_self_judgment", fake_gate)
    # 必须带上 context_refs：leader 首轮判 REQUEST_EVIDENCE 时需要可合法引用的 Evidence
    # 才能追加 EVIDENCE_ADDED 事件，从而产生验证连发保护所必需的第 2 个回合。
    meeting_id = _create_meeting(
        database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}],
    )

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()

    turns = detail["orchestration"]["turns"]
    assert len(turns) >= 2, f"需要至少两个回合验证连发保护，实际 {len(turns)}"
    # 第1轮取最高分；第2轮因连发保护（maxConsecutiveTurns=1）换到另一名自荐者
    assert turns[0]["speakerRef"] == research
    assert turns[1]["speakerRef"] == operations
    # 被换上的发言者同样必须是自我提名过的
    assert turns[1]["selfJudgments"][operations]["should_speak"] is True
