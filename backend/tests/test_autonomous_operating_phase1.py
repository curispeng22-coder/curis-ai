from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json

import pytest

from app.database import Database
from app.runtime import AutonomousControlError, AutonomousOperatingControl, ResponsibilityRoutingRuntime, RuntimeFoundation
from app.tenant_context import TenantContext


TENANT = "tenant-autonomous-phase1"
COMPANY = "company-autonomous-phase1"
BUSINESS = "business-autonomous-phase1"
DEPARTMENT = "department-autonomous-phase1"


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-phase1.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))


def approved_inputs(version: str = "v1") -> tuple[dict, dict]:
    return (
        {
            "version": version,
            "status": "APPROVED",
            "body": {"hypothesis": "用小批量真实结果验证经营方法"},
            "approvedBy": "CEO",
            "approvedAt": "2026-08-21T09:00:00+00:00",
        },
        {
            "version": version,
            "status": "APPROVED",
            "body": {"allowed": ["hypothesis", "tactic", "cadence"], "protected": ["goal", "budget"]},
            "approvedBy": "CEO",
            "approvedAt": "2026-08-21T09:00:00+00:00",
        },
    )


def seed_scope(path, *, tenant: str = TENANT, workspace_id: str = "workspace-a", goal: str = "取得首轮真实业务结果"):
    database = Database(str(path))
    database.initialize()
    with TenantContext.scope(tenant, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        with database.connect() as connection:
            connection.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, 'ceo-phase1', 'Phase 1 Company', 'active')",
                (COMPANY, tenant),
            )
            connection.execute(
                "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
                "values (?, ?, ?, 'template-phase1', '经营部', 'GENERIC')",
                (DEPARTMENT, tenant, COMPANY),
            )
            connection.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
                "lifecycle_status, goal, positioning, created_at, updated_at) "
                "values (?, ?, ?, ?, 'Autonomous Business', 'ACTIVE', '持续改善经营结果', '真实结果优先', "
                "'2026-08-21T08:00:00+00:00', '2026-08-21T08:00:00+00:00')",
                (BUSINESS, tenant, COMPANY, DEPARTMENT),
            )
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
                "blueprint_version, status, business_relation_status, business_relation_reason, "
                "business_relation_owner, business_relation_source) values (?, ?, ?, ?, '经营空间', ?, 'workspace-v1', "
                "'DRAFT', 'RESOLVED', '', 'Phase 1 Test', 'CANONICAL')",
                (workspace_id, tenant, COMPANY, BUSINESS, json.dumps({"goal": goal}, ensure_ascii=False)),
            )
        foundation = RuntimeFoundation(database)
        role = foundation.create(
            "ROLE_SLOT",
            company_id=COMPANY,
            workspace_id=workspace_id,
            lifecycle_status="READY",
            data={"role": "Workspace Leader"},
        )
        employee = foundation.create(
            "AI_EMPLOYEE",
            company_id=COMPANY,
            workspace_id=workspace_id,
            lifecycle_status="AVAILABLE",
            data={"name": "经营负责人", "roleSlotRef": role["entity_id"]},
        )
        assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY,
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workspace_id=workspace_id,
            employee_ref=employee["entity_id"],
            role_ref=role["entity_id"],
            responsibility_key="workspace-leader",
            responsibility="持续负责当前 Workspace 的经营结果",
            is_leader=True,
        )
    return database, assignment["entity_id"]


def add_workspace_scope(database: Database, workspace_id: str, *, tenant: str = TENANT):
    with TenantContext.scope(tenant, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        with database.connect() as connection:
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
                "blueprint_version, status, business_relation_status, business_relation_reason, "
                "business_relation_owner, business_relation_source) values (?, ?, ?, ?, ?, ?, 'workspace-v1', "
                "'DRAFT', 'RESOLVED', '', 'Phase 1 Test', 'CANONICAL')",
                (workspace_id, tenant, COMPANY, BUSINESS, workspace_id, json.dumps({"goal": f"Goal for {workspace_id}"})),
            )
        foundation = RuntimeFoundation(database)
        role = foundation.create(
            "ROLE_SLOT", company_id=COMPANY, workspace_id=workspace_id,
            lifecycle_status="READY", data={"role": "Workspace Leader"},
        )
        employee = foundation.create(
            "AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace_id,
            lifecycle_status="AVAILABLE", data={"name": workspace_id, "roleSlotRef": role["entity_id"]},
        )
        assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY, scope_type="WORKSPACE", scope_ref=workspace_id,
            workspace_id=workspace_id, employee_ref=employee["entity_id"], role_ref=role["entity_id"],
            responsibility_key="workspace-leader", responsibility=f"负责 {workspace_id}", is_leader=True,
        )
    return assignment["entity_id"]


def create_series(database: Database, assignment_ref: str, workspace_id: str = "workspace-a"):
    strategy, envelope = approved_inputs()
    return AutonomousOperatingControl(database).create_series(
        company_id=COMPANY,
        workspace_id=workspace_id,
        leader_assignment_ref=assignment_ref,
        strategy=strategy,
        envelope=envelope,
        plan_pin={"status": "UNRESOLVED", "operatingDefinitionRef": None},
        evaluation_pin={"status": "UNRESOLVED", "contractRef": None},
    )


def test_series_persists_canonical_scope_goal_strategy_and_replays(tmp_path):
    path = tmp_path / "series.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        first = create_series(database, assignment_ref)
        replay = create_series(database, assignment_ref)
        assert replay["entity_id"] == first["entity_id"]
        assert replay["owner_ref"] == assignment_ref
        assert replay["data"]["workspaceGoalPin"]["scopeType"] == "WORKSPACE"
        assert replay["data"]["businessGoalPin"]["relation"] == "GOVERNING_DIRECTION"
        assert replay["data"]["workspaceGoalPin"]["ref"].startswith("workspace:workspace-a:")
        strategy = replay["data"]["strategyVersions"][0]
        assert strategy["version"] == "v1"
        assert strategy["bodyHash"]
        assert strategy["envelope"]["status"] == "APPROVED"
        assert strategy["envelope"]["approvedBy"] == "CEO"
        assert replay["data"]["planPin"]["status"] == "UNRESOLVED"
        assert replay["data"]["evaluationPin"]["status"] == "UNRESOLVED"
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='OPERATING_SERIES'",
                (TENANT,),
            ).fetchone()[0] == 1
        strategy_v2, envelope_v2 = approved_inputs("v2")
        with pytest.raises(AutonomousControlError, match="different canonical truth"):
            AutonomousOperatingControl(database).create_series(
                company_id=COMPANY,
                workspace_id="workspace-a",
                leader_assignment_ref=assignment_ref,
                strategy=strategy_v2,
                envelope=envelope_v2,
            )


def test_series_fails_closed_for_goal_assignment_and_approval_scope(tmp_path):
    path = tmp_path / "fail-closed.sqlite"
    database, assignment_ref = seed_scope(path, goal="")
    strategy, envelope = approved_inputs()
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(database)
        with pytest.raises(AutonomousControlError, match="own explicit Goal"):
            control.create_series(
                company_id=COMPANY,
                workspace_id="workspace-a",
                leader_assignment_ref=assignment_ref,
                strategy=strategy,
                envelope=envelope,
            )
        with database.connect() as connection:
            connection.execute(
                "update workspaces set blueprint_json=? where workspace_id='workspace-a'",
                (json.dumps({"goal": "真实 Workspace Goal"}),),
            )
        with pytest.raises(KeyError):
            control.create_series(
                company_id=COMPANY,
                workspace_id="workspace-a",
                leader_assignment_ref="assignment-missing",
                strategy=strategy,
                envelope=envelope,
            )
        with database.connect() as connection:
            row = connection.execute(
                "select data_json from runtime_entities where entity_id=?",
                (assignment_ref,),
            ).fetchone()
            data = json.loads(row["data_json"])
            data["isLeader"] = False
            connection.execute(
                "update runtime_entities set data_json=? where entity_id=?",
                (json.dumps(data), assignment_ref),
            )
        with pytest.raises(AutonomousControlError, match="Leader Assignment"):
            control.create_series(
                company_id=COMPANY,
                workspace_id="workspace-a",
                leader_assignment_ref=assignment_ref,
                strategy=strategy,
                envelope=envelope,
            )
        invalid_envelope = {**envelope, "approvedBy": ""}
        with pytest.raises(AutonomousControlError, match="approval provenance"):
            control.create_series(
                company_id=COMPANY,
                workspace_id="workspace-a",
                leader_assignment_ref=assignment_ref,
                strategy=strategy,
                envelope=invalid_envelope,
            )
        with pytest.raises(AutonomousControlError, match="resolved canonical Workspace"):
            control.create_series(
                company_id="company-other",
                workspace_id="workspace-a",
                leader_assignment_ref=assignment_ref,
                strategy=strategy,
                envelope=envelope,
            )


def test_three_trigger_types_replay_and_merge_into_one_existing_cycle(tmp_path):
    path = tmp_path / "triggers.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(database)
        series = create_series(database, assignment_ref)
        manual = control.claim_trigger(series_id=series["entity_id"], source_type="MANUAL", source_key="ceo:1")
        replay = control.claim_trigger(series_id=series["entity_id"], source_type="MANUAL", source_key="ceo:1")
        scheduled = control.claim_trigger(series_id=series["entity_id"], source_type="SCHEDULED", source_key="review:2026-08-22")
        result = control.claim_trigger(series_id=series["entity_id"], source_type="RESULT", source_key="result:accepted-1")
        assert manual["cycle"]["entity_type"] == "CYCLE"
        assert manual["cycle"]["lifecycle_status"] == "PLANNED"
        assert manual["cycle"]["data"]["executionStatus"] == "NOT_STARTED"
        assert manual["cycle"]["data"]["autonomousControl"]["successorCycleRef"] is None
        assert replay["replayed"] is True
        assert replay["claim"]["entity_id"] == manual["claim"]["entity_id"]
        assert scheduled["merged"] is result["merged"] is True
        assert scheduled["cycle"]["entity_id"] == result["cycle"]["entity_id"] == manual["cycle"]["entity_id"]
        assert len(control.list_cycles(series["entity_id"])) == 1
        with pytest.raises(AutonomousControlError, match="active Cycle"):
            control.set_series_state(series["entity_id"], "PAUSED")
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='TRIGGER_CLAIM'",
                (TENANT,),
            ).fetchone()[0] == 3


def test_concurrent_distinct_triggers_create_only_one_active_cycle(tmp_path):
    path = tmp_path / "concurrent.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        series = create_series(database, assignment_ref)

    def claim(key: str):
        with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
            return AutonomousOperatingControl(Database(str(path))).claim_trigger(
                series_id=series["entity_id"], source_type="RESULT", source_key=key,
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        values = list(pool.map(claim, ["result:one", "result:two"]))
    cycle_ids = {item["cycle"]["entity_id"] for item in values}
    assert len(cycle_ids) == 1
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(Database(str(path)))
        assert len(control.list_cycles(series["entity_id"])) == 1


@pytest.mark.parametrize("state", ["ACTIVE", "WAITING", "PAUSED", "STOPPED"])
def test_restart_preserves_series_state_without_hidden_continuation(tmp_path, state):
    path = tmp_path / f"restart-{state.lower()}.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(database)
        series = create_series(database, assignment_ref)
        if state != "ACTIVE":
            series = control.set_series_state(
                series["entity_id"], state,
                next_check_at="2026-08-22T09:00:00+00:00" if state == "WAITING" else None,
            )
        restarted = AutonomousOperatingControl(Database(str(path)))
        recovered = restarted.get_series(series["entity_id"])
        assert recovered["lifecycle_status"] == state
        claim = restarted.claim_trigger(
            series_id=series["entity_id"], source_type="MANUAL", source_key=f"restart:{state}",
        )
        if state == "ACTIVE":
            assert claim["claim"]["lifecycle_status"] == "APPLIED"
            assert claim["cycle"] is not None
        elif state == "STOPPED":
            assert claim["claim"]["lifecycle_status"] == "CANCELLED"
            assert claim["claim"]["data"]["cancelReason"] == "SERIES_STOPPED"
            assert claim["cycle"] is None
        else:
            assert claim["claim"]["lifecycle_status"] == "CLAIMED"
            assert claim["cycle"] is None
        replay = restarted.claim_trigger(
            series_id=series["entity_id"], source_type="MANUAL", source_key=f"restart:{state}",
        )
        assert replay["replayed"] is True
        assert replay["claim"]["entity_id"] == claim["claim"]["entity_id"]


def test_waiting_claim_can_be_cancelled_and_restart_replays_cancelled_truth(tmp_path):
    path = tmp_path / "cancel.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(database)
        series = create_series(database, assignment_ref)
        control.set_series_state(series["entity_id"], "WAITING", next_check_at="2026-08-22T09:00:00+00:00")
        claim = control.claim_trigger(series_id=series["entity_id"], source_type="SCHEDULED", source_key="wait:1")
        cancelled = control.cancel_claim(claim["claim"]["entity_id"], reason="计划已取消")
        assert cancelled["lifecycle_status"] == "CANCELLED"
        restarted = AutonomousOperatingControl(Database(str(path)))
        replay = restarted.claim_trigger(series_id=series["entity_id"], source_type="SCHEDULED", source_key="wait:1")
        assert replay["replayed"] is True
        assert replay["claim"]["lifecycle_status"] == "CANCELLED"
        assert replay["cycle"] is None


def test_workspace_tenant_isolation_and_independent_series(tmp_path):
    path_a = tmp_path / "scope.sqlite"
    database_a, assignment_a = seed_scope(path_a, workspace_id="workspace-a")
    assignment_b = add_workspace_scope(database_a, "workspace-b")
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        series_a = create_series(database_a, assignment_a, "workspace-a")
        series_b = create_series(database_a, assignment_b, "workspace-b")
        cycle_a = AutonomousOperatingControl(database_a).claim_trigger(
            series_id=series_a["entity_id"], source_type="MANUAL", source_key="same-key",
        )["cycle"]
        cycle_b = AutonomousOperatingControl(database_a).claim_trigger(
            series_id=series_b["entity_id"], source_type="MANUAL", source_key="same-key",
        )["cycle"]
        assert cycle_a["entity_id"] != cycle_b["entity_id"]
    with TenantContext.scope("tenant-other", company_id=COMPANY, role="test"):
        with pytest.raises(KeyError):
            AutonomousOperatingControl(database_a).get_series(series_a["entity_id"])


def test_cycle_close_is_not_series_stop_and_no_employee_or_successor_side_effect(tmp_path):
    path = tmp_path / "boundaries.sqlite"
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, role="test"):
        control = AutonomousOperatingControl(database)
        series = create_series(database, assignment_ref)
        cycle = control.claim_trigger(series_id=series["entity_id"], source_type="MANUAL", source_key="boundary:1")["cycle"]
        with database.connect() as connection:
            connection.execute(
                "update runtime_entities set lifecycle_status='CLOSED' where tenant_id=? and entity_id=?",
                (TENANT, cycle["entity_id"]),
            )
            assert connection.execute(
                "select count(*) from tasks where tenant_id=?",
                (TENANT,),
            ).fetchone()[0] == 0
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type in ('RESULT','EVIDENCE','ARTIFACT')",
                (TENANT,),
            ).fetchone()[0] == 0
        recovered = AutonomousOperatingControl(Database(str(path))).get_series(series["entity_id"])
        assert recovered["lifecycle_status"] == "ACTIVE"
        assert cycle["data"]["autonomousControl"]["successorCycleRef"] is None
        assert len(control.list_cycles(series["entity_id"])) == 1
