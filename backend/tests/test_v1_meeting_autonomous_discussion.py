from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier

from fastapi.testclient import TestClient

from app.database import Database
from app.knowledge_service import KnowledgeService
from app.main import create_app
from app.meeting_service import MeetingService
from app.model_gateway import ModelGatewayAdapter
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from app.tenant_context import TenantContext


TENANT = "tenant-meeting-autonomous"
COMPANY = "company-meeting-autonomous"
DEPARTMENT = "department-meeting-autonomous"
BUSINESS = "business-meeting-autonomous"
WORKSPACE = "workspace-meeting-autonomous"
CAPABILITY = "agent.meeting.local"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo", "X-Company-Id": COMPANY}
PREFIX = f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings"


class MeetingProvider:
    def __init__(self, knowledge_ref: str):
        self.knowledge_ref = knowledge_ref
        self.speakers = 0
        self.leaders = 0
        self.gates = 0
        self.calls: list[str] = []
        # 员工自我判断门控的决策表：key = employeeRef。
        # 缺失时默认 SPEAK，以保持既有（门控前）用例的行为预期。
        self.gate_decisions: dict[str, bool] = {}
        # 可选的决策函数 (employee_ref, call_number, prompt) -> bool，
        # call_number 是该员工第几次被门控（1 起），用于验证"因新 Evidence 重新介入"。
        self.gate_decision_fn = None
        self.gate_counts: dict[str, int] = {}
        self.gate_calls: list[str] = []

    @staticmethod
    def _decision():
        fact = lambda value, provenance="EST": {"value": value, "provenance": provenance}
        return {
            "decisionKey": "meeting-autonomous-choice",
            "complexity": "LOW_RISK",
            "event": "需要选择客户反馈验证方案",
            "cannotDecideReason": "两个方案存在经营取舍，需要CEO确认",
            "options": [
                {"optionId": "FOCUS", "label": "先验证高频问题", "impact": fact("更快形成首个验证"),
                 "risk": fact("低频问题延后"), "cost": fact("当前成本未知", "UNK")},
                {"optionId": "BROAD", "label": "同时覆盖全部问题", "impact": fact("覆盖面更广"),
                 "risk": fact("首个结果可能更晚"), "cost": fact("当前成本未知", "UNK")},
            ],
            "recommendation": {"optionId": "FOCUS", "provenance": "EST"},
            "recommendationReason": fact("依据当前会议证据做出的员工估计"),
            "ceoChoicePrompt": "请选择验证方案",
            "continuationPlan": "整理高频问题并形成验证结果",
            "workContract": {
                "problem": "整理高频客户问题",
                "expectedResult": "形成一项有证据的验证结果",
                "constraints": ["只使用会议已引用事实"],
            },
        }

    def execute(self, prompt: str) -> dict:
        self.calls.append(prompt)
        if "meeting-leader-evaluation" in prompt:
            self.leaders += 1
            outcomes = ["REQUEST_EVIDENCE", "UPDATE_PROPOSAL", "NEEDS_CEO_DECISION", "DISCUSSION_SUFFICIENT"]
            outcome = outcomes[min(self.leaders - 1, len(outcomes) - 1)]
            payload = {
                "status": "ACCEPTED", "resultType": "meeting-leader-evaluation",
                "outcome": outcome, "summary": "推进负责人完成本轮判断",
                "requestedEmployeeRef": "", "evidenceRefs": [self.knowledge_ref] if outcome == "REQUEST_EVIDENCE" else [],
                "proposal": (
                    {"summary": "优先验证高频客户问题", "rationale": "来自会议发言和客户资料", "unknowns": ["实际成本"]}
                    if outcome in {"UPDATE_PROPOSAL", "NEEDS_CEO_DECISION"} else {}
                ),
                "decisionPacket": self._decision() if outcome == "NEEDS_CEO_DECISION" else None,
            }
        elif "meeting-contribution" in prompt:
            self.speakers += 1
            payload = {
                "status": "ACCEPTED", "resultType": "meeting-contribution",
                "summary": f"新增观点{self.speakers}",
                "response": f"基于当前合法资料，我补充第{self.speakers}项可验证判断。",
                "newFacts": [f"事实{self.speakers}"], "risk": "", "evidenceRefs": [],
                "proposalChange": "", "needsMoreEvidence": self.speakers == 1,
                "missingFact": "客户反馈资料" if self.speakers == 1 else "",
            }
        elif "meeting-self-judgment" in prompt:
            # 员工自我判断门控：从 prompt 内的上下文 JSON 取回被判断的员工，
            # 以便用例按 employeeRef 精确控制 SPEAK / STAY_SILENT。
            self.gates += 1
            match = re.search(r'"employeeRef"\s*:\s*"([^"]+)"', prompt)
            employee_ref = match.group(1) if match else ""
            self.gate_calls.append(employee_ref)
            call_number = self.gate_counts.get(employee_ref, 0) + 1
            self.gate_counts[employee_ref] = call_number
            if self.gate_decision_fn is not None:
                should_speak = bool(self.gate_decision_fn(employee_ref, call_number, prompt))
            else:
                should_speak = self.gate_decisions.get(employee_ref, True)
            payload = {
                "status": "ACCEPTED", "resultType": "meeting-self-judgment",
                "should_speak": should_speak,
                "contribution": "我补充一项基于当前合法资料的可验证判断。",
                "confidence": 0.8,
                "reason": "我对该议题有新增相关性。" if should_speak else "本轮我没有可补充的新事实或新判断。",
            }
        else:
            result_type = "general-business-result"
            payload = {
                "status": "ACCEPTED", "resultType": result_type,
                "summary": "已形成一项有证据的验证结果", "problem": "",
            }
        return {
            "output": json.dumps(payload, ensure_ascii=False), "status": "success",
            "session_id": f"meeting-session-{len(self.calls)}", "outbound_attempted": False,
            "total_tokens": 20, "estimated_cost": 0,
        }

    def http_post(self, _url: str, payload: dict, _headers: dict, _timeout: int) -> dict:
        result = self.execute(str(payload["messages"][-1]["content"]))
        return {
            "choices": [{"message": {"content": result["output"]}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        }

    def adapter(self) -> ModelGatewayAdapter:
        return ModelGatewayAdapter(
            base_url="https://meeting.local", api_key="not-a-real-secret",
            gateway_id="meeting-local", model_name="meeting-local-model", http_post=self.http_post,
        )


class FailingMeetingProvider(MeetingProvider):
    def http_post(self, _url: str, payload: dict, _headers: dict, _timeout: int) -> dict:
        self.calls.append(str(payload["messages"][-1]["content"]))
        raise TimeoutError("provider unavailable")


def seed(path):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id,tenant_id,ceo_id,name) values(?,?,?,'会议公司')",
            (COMPANY, TENANT, "ceo"),
        )
        connection.execute(
            "insert into department_instances(id,tenant_id,company_id,template_id,name,department_type) "
            "values(?,?,?,'official.department.software_rnd','业务部','business.general')",
            (DEPARTMENT, TENANT, COMPANY),
        )
        connection.execute(
            "insert into canonical_businesses(business_id,tenant_id,company_id,department_id,name,goal,lifecycle_status,created_at,updated_at) "
            "values(?,?,?,?,?,'验证客户反馈','ACTIVE',current_timestamp,current_timestamp)",
            (BUSINESS, TENANT, COMPANY, DEPARTMENT, "客户反馈业务"),
        )
        connection.execute(
            "insert into workspaces(workspace_id,tenant_id,company_id,business_id,name,blueprint_json,blueprint_version,"
            "status,business_relation_status,business_relation_reason,business_relation_source) "
            "values(?,?,?,?,?,?,'v1','OPERATING','RESOLVED','','TEST')",
            (WORKSPACE, TENANT, COMPANY, BUSINESS, "客户反馈办公室", json.dumps({"productForm": "GENERIC"})),
        )
    database.save_official_model(
        model_key=CAPABILITY, provider_id="meeting-local", display_name="Meeting local provider",
        supported_models=["meeting-local-model"], gateway_ref="meeting-local",
        default_model="meeting-local-model",
    )
    employees = {
        "leader": ("employee-meeting-leader", "王颖", "业务负责人", "推进经营判断"),
        "research": ("employee-meeting-research", "苏禾", "客户研究", "研究客户反馈资料"),
        "operations": ("employee-meeting-operations", "林舟", "财务支持", "处理发票归档"),
    }
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        foundation = RuntimeFoundation(database)
        routing = ResponsibilityRoutingRuntime(database)
        assignments = []
        for key, (employee_id, name, role_name, responsibility) in employees.items():
            with database.connect() as connection:
                connection.execute(
                    "insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) "
                    "values(?,?,?,?,?,?,?,'idle')",
                    (employee_id, TENANT, COMPANY, DEPARTMENT, "et_product_manager", name, role_name),
                )
                connection.execute(
                    "insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                    "values(?,?,?,'official','model',?)",
                    (f"binding-{key}", TENANT, employee_id, CAPABILITY),
                )
            foundation.create(
                "AI_EMPLOYEE", entity_id=employee_id, company_id=COMPANY, workspace_id=WORKSPACE,
                lifecycle_status="AVAILABLE", data={"name": name, "role": role_name},
            )
            role = foundation.create(
                "ROLE_SLOT", company_id=COMPANY, workspace_id=WORKSPACE,
                data={"role": role_name, "responsibility": responsibility},
            )
            assignment = routing.create_assignment(
                company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
                role_ref=role["entity_id"], employee_ref=employee_id,
                responsibility_key=key, responsibility=responsibility,
                output_contract={"requiresResult": True, "resultType": "general-business-result"},
                is_leader=key == "leader",
            )
            assignments.append(assignment["entity_id"])
        routing.publish_workflow(
            company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="general-operating", assignment_refs=assignments,
            default_flow=["research", "operations"],
        )
        knowledge = KnowledgeService(database).create_entry(
            title="客户反馈资料", body="访谈显示高频问题集中在首次使用成本。",
            company_id=COMPANY, target_type="WORKSPACE", target_ref=WORKSPACE, created_by="employee-meeting-research",
        )
    return database, employees, knowledge["id"]


def test_autonomous_discussion_evidence_proposal_decision_work_result_and_restart(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-autonomous.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    payload = {
        "title": "客户研究与执行方案",
        "background": "先确认客户事实，再形成验证方案",
        "business_id": BUSINESS, "workspace_id": WORKSPACE,
        "participant_refs": [item[0] for item in employees.values()],
        "leader_ref": employees["leader"][0], "ceo_participation_mode": "DECISION_ONLY",
        "context_refs": [{"type": "KNOWLEDGE", "ref": knowledge_ref}],
    }
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        created = client.post(PREFIX, headers=HEADERS, json=payload)
        assert created.status_code == 201, created.text
        meeting_id = created.json()["meeting_id"]
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
        assert detail["decision"]["lifecycle_status"] == "WAITING_CEO"
        assert detail["background_continuation"]["status"] == "AVAILABLE"
        assert detail["orchestration"]["proposal"]["artifactRef"].startswith("artifact-")
        assert any(item["kind"] == "EVIDENCE_REFERENCE" for item in detail["timeline"])
        visible_speakers = [item["actorRef"] for item in detail["timeline"] if item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE"]
        assert visible_speakers[0] == employees["research"][0]
        assert all(
            any(candidate["selected"] and candidate["employeeRef"] == turn["speakerRef"] for candidate in turn["candidates"])
            for turn in detail["orchestration"]["turns"]
        )
        # 旧断言 `operations 永不发言` 编码的正是 T1 判定的「确定性公式把低相关性员工
        # 结构性排除」行为。接入员工自我判断门控后（要求 #7），发言资格由员工自决，
        # 因此改为断言更强的契约：每个实际发言者都必须是本轮自我提名（SPEAK）的人。
        for turn in detail["orchestration"]["turns"]:
            assert turn["selfJudgments"][turn["speakerRef"]]["should_speak"] is True
        client.post(f"{PREFIX}/{meeting_id}/decision/review", headers=HEADERS)
        chosen = client.post(
            f"{PREFIX}/{meeting_id}/decision/choose", headers=HEADERS,
            json={"choice": detail["decision"]["data"]["recommendation"]["optionId"], "reason": "先验证高频问题"},
        )
        assert chosen.status_code == 200, chosen.text
        final = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
        assert final["works"] and final["results"]
        assert final["orchestration"]["lastOutcome"] == "DISCUSSION_SUFFICIENT"
        with database.connect() as connection:
            assert connection.execute("select count(*) from ai_usage_records").fetchone()[0] == len(provider.calls)
            assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 1
            assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"

    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        recovered = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
        tasks_before = len(provider.calls)
        assert recovered["conversation_id"] == detail["conversation_id"]
        assert recovered["orchestration"]["activeRunId"] == ""
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        assert len(provider.calls) == tasks_before


def test_explicit_employee_override_and_duplicate_no_progress_stop(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-override.sqlite"
    database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    provider.leaders = 3  # every leader evaluation is DISCUSSION_SUFFICIENT
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        created = client.post(PREFIX, headers=HEADERS, json={
            "title": "执行风险复核", "background": "只补充新的执行风险",
            "business_id": BUSINESS, "workspace_id": WORKSPACE,
            "participant_refs": [item[0] for item in employees.values()],
            "leader_ref": employees["leader"][0], "ceo_participation_mode": "JOIN", "context_refs": [],
        }).json()
        meeting_id = created["meeting_id"]
        response = client.post(
            f"{PREFIX}/{meeting_id}/messages", headers=HEADERS,
            json={"actor_type": "CEO", "actor_ref": "ceo", "text": "@林舟 请先评估执行风险"},
        )
        assert response.status_code == 200
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
        assert detail["orchestration"]["turns"][-1]["speakerRef"] == employees["operations"][0]
        assert detail["orchestration"]["turns"][-1]["candidates"][0]["reasons"][0] == "CEO或推进负责人明确点名"


def test_acknowledgement_needs_no_response_and_provider_failure_stays_failed(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "meeting-stop-truth.sqlite"
    _database, employees, knowledge_ref = seed(path)
    provider = MeetingProvider(knowledge_ref)
    provider.leaders = 3
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        meeting = client.post(PREFIX, headers=HEADERS, json={
            "title": "客户资料判断", "background": "判断现有资料是否已经充分",
            "business_id": BUSINESS, "workspace_id": WORKSPACE,
            "participant_refs": [item[0] for item in employees.values()],
            "leader_ref": employees["leader"][0], "ceo_participation_mode": "JOIN", "context_refs": [],
        }).json()
        calls = len(provider.calls)
        response = client.post(
            f"{PREFIX}/{meeting['meeting_id']}/messages", headers=HEADERS,
            json={"actor_type": "CEO", "actor_ref": "ceo", "text": "收到"},
        )
        assert response.status_code == 200
        assert len(provider.calls) == calls

    failed_path = tmp_path / "meeting-provider-failure.sqlite"
    failed_db, failed_employees, failed_knowledge = seed(failed_path)
    failing = FailingMeetingProvider(failed_knowledge)
    with TestClient(create_app(str(failed_path), model_gateway_adapter=failing.adapter())) as client:
        failed = client.post(PREFIX, headers=HEADERS, json={
            "title": "客户资料判断", "background": "必须基于真实模型结果",
            "business_id": BUSINESS, "workspace_id": WORKSPACE,
            "participant_refs": [item[0] for item in failed_employees.values()],
            "leader_ref": failed_employees["leader"][0], "ceo_participation_mode": "JOIN", "context_refs": [],
        }).json()
        detail = client.get(f"{PREFIX}/{failed['meeting_id']}", headers=HEADERS).json()
        assert detail["orchestration"]["status"] == "BLOCKED"
        assert not any(item["kind"] == "MESSAGE" and item["actorType"] == "EMPLOYEE" for item in detail["timeline"])
        with failed_db.connect() as connection:
            usage = connection.execute("select execution_status, metering_status from ai_usage_records").fetchall()
        assert len(usage) == 1
        assert usage[0]["execution_status"] != "success"
        assert usage[0]["metering_status"] == "unknown"


def test_single_advancement_claim_stale_restart_and_time_budget(tmp_path):
    path = tmp_path / "meeting-claim.sqlite"
    database, employees, _knowledge_ref = seed(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        meeting = service.create(
            company_id=COMPANY, business_id=BUSINESS, workspace_id=WORKSPACE,
            title="并发推进检查", background="同一会议只能有一个推进者",
            participant_refs=[item[0] for item in employees.values()], leader_ref=employees["leader"][0],
            ceo_participation_mode="JOIN", context_refs=[],
        )
        meeting_id = meeting["meeting_id"]

    gate = Barrier(2)

    def claim():
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            gate.wait()
            return MeetingService(database)._claim_advance(meeting_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        claims = list(pool.map(lambda _item: claim(), range(2)))
    assert sum(bool(item) for item in claims) == 1

    stale_at = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(timespec="seconds")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        service._update_orchestration(meeting_id, lambda state: state | {"runStartedAt": stale_at})
        assert service._claim_advance(meeting_id) is None
        stale = database.get_strategy_meeting(TENANT, meeting_id)["orchestration"]
        assert stale["activeRunId"] == ""
        assert stale["status"] == "BLOCKED"
        assert "无法证明" in stale["blockedReason"]
        assert service._claim_advance(meeting_id)
        assert "运行时间上限" in service._budget_reason(
            stale | {"currentCycle": stale["currentCycle"] | {"startedAt": stale_at}, "status": "RUNNING"}
        )
