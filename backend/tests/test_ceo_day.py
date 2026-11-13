"""第 2 步端到端验收：CEO 的一天（7 步 + 至少一条失败路径）。

依据 docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md §8。
中间不允许人工改库——全部走 CeoDayService 的领域方法（状态机统一入口）。

ADR-0041 硬要求：至少一条失败路径必须跑通。本文件覆盖：
- 正常 7 步连续闭环；
- 失败路径：无授权 → Outcome 强制 UNVERIFIED → 业务方向「扩大」被冻结并给出原因；
- 失败路径：贡献权重合计 != 100% → 确认被拒绝。
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from app.database import Database
from app.runtime.ceo_day_service import CeoDayService
from app.runtime.scheduler import RuntimeScheduler, SimulatedExecutor
from app.runtime.state_machine import GuardRejectedError

os.environ.setdefault("CURIS_IDENTITY_MODE", "test")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _past_iso() -> str:
    return (_utcnow() - timedelta(hours=1)).astimezone(timezone.utc).isoformat(timespec="seconds")


def _new_service() -> CeoDayService:
    d = Path(tempfile.mkdtemp()) / "ceo_day.sqlite"
    db = Database(str(d))
    # 执行器：节奏配置了 escalation 即升级（命中升级契约 → WAITING_CEO）
    sched = RuntimeScheduler(
        db, SimulatedExecutor(escalate_when=lambda c: bool(c.get("escalation")))
    )
    return CeoDayService(db, scheduler=sched)


def _seed_active_direction(svc: CeoDayService) -> str:
    did = svc.create_business_direction(
        name="小红书增长", template_type="xhs",
        opportunity="o", target_outcome="t",
    )
    svc.submit_direction_brief(did)
    svc.approve_direction(did, authorized=True)
    return did


# --------------------------------------------------------------------------
# 正常 7 步闭环
# --------------------------------------------------------------------------


def test_ceo_day_full_loop() -> None:
    svc = _new_service()

    # 前置：业务方向 → ACTIVE
    did = _seed_active_direction(svc)
    assert svc.get_direction(did)["lifecycle_status"] == "ACTIVE"

    # 承诺 → ACTIVE（AI 回报首条结果）
    cid = svc.create_commitment(
        did, department_name="增长组", name="每周研究", target_outcome="t"
    )
    svc.report_commitment_first_result(cid)
    assert svc.get_commitment(cid)["status"] == "ACTIVE"

    # 工作空间 → OPERATING（三级门禁）
    wid = svc.create_workspace(did, name="小红书工作空间")
    svc.start_blueprint(wid)
    svc.pass_simulation(wid)
    svc.submit_workspace_for_approval(
        wid, issues_resolved=True, external_agent_reviewed=True
    )
    svc.approve_and_launch_workspace(wid)
    assert svc.get_workspace(wid)["status"] == "OPERATING"

    # 第 1 步：定节奏（可查询下次触发时间）
    cad_id = svc.create_cadence(
        did, "每日研究", "daily 08:00", escalation={"reason": "需要 CEO 拍板"}
    )
    svc.enable_cadence(cad_id, next_fire_at=_past_iso())
    cad = svc._scheduler._get_cadence(cad_id)
    assert cad["next_fire_at"]

    # 第 2 步：到点自动开跑（无人操作）→ 命中升级转 WAITING_CEO
    spawned = svc.fire_due_runs(_utcnow())
    assert len(spawned) == 1
    run = svc.get_run(spawned[0])
    assert run["status"] == "WAITING_CEO"  # 升级契约生效

    # 第 3 + 4 步：CEO 处理 → ACKNOWLEDGED → RESOLVED，留痕记录响应
    svc.ceo_open_run(run["run_id"])
    assert svc.get_run(run["run_id"])["status"] == "ACKNOWLEDGED"
    svc.ceo_resolve_run(run["run_id"], reason="已拍板")
    assert svc.get_run(run["run_id"])["status"] == "RESOLVED"
    hist = svc.run_history(run["run_id"])
    assert any(h["target"] == "ACKNOWLEDGED" for h in hist)
    assert any(h["target"] == "RESOLVED" for h in hist)

    # 第 5 步：外部数据回流 → Outcome（VERIFIED）
    oid = svc.record_outcome(
        did, run_id=run["run_id"], commitment_id=cid, value=1200.0,
        evidence_grade="VERIFIED", source="api",
        contributors=[
            {"agent": "researcher", "model": "gpt", "skills": ["s1"], "tools": ["t1"], "weight": 60},
            {"agent": "writer", "model": "claude", "weight": 40},
        ],
    )
    assert svc.get_outcome(oid)["evidence_grade"] == "VERIFIED"

    # 第 6 步：收束成果（权重合计 100% → REVIEWED，可追溯到 run_id）
    svc.confirm_attribution(oid)
    assert svc.get_outcome(oid)["attribution_status"] == "REVIEWED"

    # 第 7 步：记账归因 → 验证结论更新 → 「扩大业务」权限开启
    svc.set_direction_verification(did, "VERIFIED")
    svc.scale_direction(did)
    assert svc.get_direction(did)["lifecycle_status"] == "SCALING"


# --------------------------------------------------------------------------
# 失败路径 1：无授权 → UNVERIFIED → 扩大被冻结
# --------------------------------------------------------------------------


def test_failure_path_unauthorized_freezes_scaling() -> None:
    svc = _new_service()
    did = _seed_active_direction(svc)

    # 第 5 步：无外部授权 → 结果只能手动补录且强制 UNVERIFIED
    oid = svc.record_outcome(
        did, evidence_grade="UNVERIFIED", value=0.0,
        contributors=[{"agent": "a", "weight": 100}],
    )
    assert svc.get_outcome(oid)["evidence_grade"] == "UNVERIFIED"

    # 第 7 步：验证结论非 VERIFIED → 「扩大业务」被冻结并给原因
    svc.set_direction_verification(did, "UNVERIFIED")
    with pytest.raises(GuardRejectedError) as exc:
        svc.scale_direction(did)
    assert "VERIFIED" in str(exc.value)
    # 状态仍停在 ACTIVE，未被非法推进
    assert svc.get_direction(did)["lifecycle_status"] == "ACTIVE"


# --------------------------------------------------------------------------
# 失败路径 2：贡献权重合计 != 100% → 确认被拒绝
# --------------------------------------------------------------------------


def test_attribution_weight_must_sum_100() -> None:
    svc = _new_service()
    did = _seed_active_direction(svc)
    oid = svc.record_outcome(
        did, evidence_grade="VERIFIED",
        contributors=[{"agent": "a", "weight": 50}, {"agent": "b", "weight": 30}],
    )
    with pytest.raises(ValueError):
        svc.confirm_attribution(oid)
    # 未确认，仍 PENDING_REVIEW
    assert svc.get_outcome(oid)["attribution_status"] == "PENDING_REVIEW"


# --------------------------------------------------------------------------
# 硬门禁：未勾选授权 → 启动被拒绝（不静默放行）
# --------------------------------------------------------------------------


def test_direction_approve_requires_authorization() -> None:
    svc = _new_service()
    did = svc.create_business_direction(
        name="x", template_type="xhs", opportunity="o", target_outcome="t"
    )
    svc.submit_direction_brief(did)
    with pytest.raises(GuardRejectedError):
        svc.approve_direction(did, authorized=False)
    assert svc.get_direction(did)["lifecycle_status"] == "PENDING_APPROVAL"


# --------------------------------------------------------------------------
# HTTP 层（A5 信封 + 路由真实可达，Step 3 前端接入口）
# --------------------------------------------------------------------------


def _client_with_escalation():
    from fastapi.testclient import TestClient

    from app.main import create_app

    d = Path(tempfile.mkdtemp()) / "http_ceo_day.sqlite"
    db = Database(str(d))
    sched = RuntimeScheduler(
        db, SimulatedExecutor(escalate_when=lambda c: bool(c.get("escalation")))
    )
    app = create_app(db_path=db.path)
    # 用带升级执行器的服务覆盖默认装配
    app.state.ceo_day_service = CeoDayService(db, scheduler=sched)
    return TestClient(app), app


def test_http_envelope_create_and_approve_direction() -> None:
    client, _ = _client_with_escalation()
    r = client.post(
        "/api/ceo-day/business-directions",
        json={"name": "小红书增长", "template_type": "xhs",
              "opportunity": "o", "target_outcome": "t"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == 0  # A5 信封
    assert body["data"]["name"] == "小红书增长"
    did = body["data"]["direction_id"]

    client.post(f"/api/ceo-day/business-directions/{did}/submit-brief")
    r2 = client.post(
        f"/api/ceo-day/business-directions/{did}/approve",
        json={"authorized": True},
    )
    assert r2.json()["data"]["lifecycle_status"] == "ACTIVE"


def test_http_escalation_loop() -> None:
    client, app = _client_with_escalation()
    svc = app.state.ceo_day_service
    # 业务方向 → ACTIVE
    did = client.post(
        "/api/ceo-day/business-directions",
        json={"name": "小红书增长", "template_type": "xhs",
              "opportunity": "o", "target_outcome": "t"},
    ).json()["data"]["direction_id"]
    client.post(f"/api/ceo-day/business-directions/{did}/submit-brief")
    client.post(
        f"/api/ceo-day/business-directions/{did}/approve",
        json={"authorized": True},
    )
    # 节奏（含升级声明）
    cid = client.post(
        "/api/ceo-day/cadences",
        json={"business_id": did, "name": "每日研究",
              "schedule_text": "daily 08:00",
              "escalation": {"reason": "需要 CEO 拍板"}},
    ).json()["data"]["cadence_id"]
    client.post(
        f"/api/ceo-day/cadences/{cid}/enable",
        json={"next_fire_at": _past_iso()},
    )
    # 到点自动开跑 → WAITING_CEO
    fired = client.post("/api/ceo-day/fire").json()["data"]["spawned"]
    assert len(fired) == 1
    run_id = fired[0]
    assert svc.get_run(run_id)["status"] == "WAITING_CEO"
    # CEO 处理 → RESOLVED
    client.post(f"/api/ceo-day/runs/{run_id}/open")
    r = client.post(
        f"/api/ceo-day/runs/{run_id}/resolve", json={"reason": "已拍板"}
    )
    assert r.json()["code"] == 0
    assert svc.get_run(run_id)["status"] == "RESOLVED"
