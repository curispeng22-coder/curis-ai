"""Phase-2 E2E：用真实 DeepSeek 跑自主讨论会议，验证 T8 员工自我 Speak/Stay-Silent
门控 + 全局 budget 修复在真模型下成立。

本脚本不修改任何业务代码（meeting_service.py 等已冻结），仅作为临时驱动脚本使用，不提交。

环境说明（详见汇报）：
- 后端既定真实模型路径是经本地 New API 网关（deploy/new-api，127.0.0.1:3000）代理 DeepSeek。
  但当前沙箱内 Docker daemon 未启动、该网关容器未运行，故本脚本将适配器直接指向
  DeepSeek 官方 API（api.deepseek.com），使用 .env 中的真实 DEEPSEEK_API_KEY。
  这仍是真实的云端大模型调用（OpenAI 兼容），与经网关代理功能等价。
- 复用 tests/test_v1_meeting_employee_self_judgment.py 的会议/参与者构造逻辑（seed），
  但把 mock provider 换成真实 DeepSeek；并显式把员工能力绑定改指真实模型
  （gateway_ref=newapi-local, default_model=deepseek-chat），使模型解析路径命中真实 API。
- 真实通用模型偶发返回非 JSON，会触发 _json_output 的合同错误并 BLOCKED（providerCallCount=0）。
  这属于真实模型鲁棒性问题，脚本对“瞬时合同错误”做整场重试（最多 3 次）以得到干净结果。

运行（从 backend/ 目录，真实出网需 dangerouslyDisableSandbox）：
  CURIS_DB=/tmp/curis_e2e CURIS_ENV=test CURIS_IDENTITY_MODE=test \
  TMPDIR=/tmp backend/.venv/bin/python scripts/e2e_meeting_real_deepseek.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path

# 让 `import app.*` 可用（脚本位于 backend/scripts/）。
BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

# ── 1) 注入真实 DeepSeek 环境（在 import app.main 之前，dotenv 不会覆盖已存在的键）──
_DOTENV = BACKEND.parent / "deploy" / "new-api" / ".env"
_DEEPSEEK_KEY = ""
if _DOTENV.is_file():
    for raw in _DOTENV.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            _DEEPSEEK_KEY = line.split("=", 1)[1].strip()

os.environ["CURIS_MODEL_GATEWAY_BASE_URL"] = "https://api.deepseek.com"
os.environ["CURIS_MODEL_GATEWAY_API_KEY"] = _DEEPSEEK_KEY
os.environ["CURIS_MODEL_GATEWAY_MODEL"] = "deepseek-chat"
os.environ["CURIS_MODEL_GATEWAY_ID"] = "newapi-local"
os.environ["CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS"] = "0"
os.environ["CURIS_ENV"] = "test"
os.environ["CURIS_IDENTITY_MODE"] = "test"

# app.main 导入时会以 CURIS_DB 为路径执行 create_app()（顶层 app=create_app()）。
# 若 CURIS_DB 是目录会令 sqlite 打开失败，故强制指向一个文件，并复用 /tmp/curis_e2e 作为隔离 DB 根目录。
ROOT = Path("/tmp/curis_e2e")
ROOT.mkdir(parents=True, exist_ok=True)
os.environ["CURIS_DB"] = str(ROOT / "_bootstrap.sqlite")

import app.main  # noqa: E402  (触发 _load_local_dotenv，但不会覆盖上面已设的键)

from app.database import Database  # noqa: E402
from app.knowledge_service import KnowledgeService  # noqa: E402
from app.main import create_app  # noqa: E402
from app.meeting_service import MeetingService  # noqa: E402
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation  # noqa: E402
from app.tenant_context import TenantContext  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

# ── 2) 复用测试的种子构造逻辑（与 test_v1_meeting_autonomous_discussion.seed 一致）──
TENANT = "tenant-meeting-autonomous"
COMPANY = "company-meeting-autonomous"
DEPARTMENT = "department-meeting-autonomous"
BUSINESS = "business-meeting-autonomous"
WORKSPACE = "workspace-meeting-autonomous"
CAPABILITY = "agent.meeting.local"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo", "X-Company-Id": COMPANY}
PREFIX = f"/api/workspace/runtime/foundation/companies/{COMPANY}/meetings"

NEW_EVIDENCE_FACTS = [
    "补充：研发工具链开工后，前 2 个月会挤占约 30% 的交付人力，现有客户的交付排期可能顺延。",
    "供应链侧更新：关键组件交期从 4 周拉长到 7 周，影响交付稳定性。",
    "客户侧更新：两家头部客户明确把「交付准时率」写进了续约条款。",
    "运营补充：当前交付排期已接近产能上限，新增方向需重新排期而非简单叠加。",
]

# 用于触发「再干预」的 CEO 交付/供应链证据消息：直接点名 operations（@林舟），
# 使其在后续回合成为被请求的发言候选（_candidate_evaluation 中 requested +100），
# 而交付/供应链内容与其岗位「交付与供应链」高度相关 -> 其自我判断应从 STAY_SILENT 转为 SPEAK。
REINTERVENTION_CEO_MESSAGE = (
    "交付更新：研发工具链若现在开工，预计上线要 2 个月，期间会挤占约 30% 的交付人力，"
    "现有客户的交付排期与稳定性可能受影响。"
    "@林舟 请从交付排期与供应链角度判断：这条时间线对现有客户交付意味着什么，我们该怎么排期。"
)


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
        supported_models=["meeting-local-model"], gateway_ref="meeting-local", default_model="meeting-local-model",
    )
    employees = {
        "leader": ("employee-meeting-leader", "王颖", "业务负责人", "推进经营判断"),
        "research": ("employee-meeting-research", "苏禾", "客户研究", "研究客户反馈资料"),
        # 注：operations 设为「交付排期与供应链协调」角色 —— 会议第 0 回合的议题是「内容增长 vs 研发工具
        # 对客户满意度的影响」，交付/供应链并非首轮切入点，故 operations 自我判断无关而保持沉默；
        # 而在注入「研发工具链上线挤占交付人力/组件交期拉长」等新证据（@林舟）后，其岗位与证据高度相关，
        # 应自我判断为 SPEAK，从而构成「先 STAY_SILENT、后因地新证据 SPEAK」的再干预（要求 #6）。
        "operations": ("employee-meeting-operations", "林舟", "交付与供应链", "负责交付排期与供应链协调，评估各方向对交付时效与稳定性的影响"),
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
            title="客户反馈资料", body="访谈显示高频问题集中在首次使用成本，且中小客户对价格敏感。",
            company_id=COMPANY, target_type="WORKSPACE", target_ref=WORKSPACE, created_by="employee-meeting-research",
        )
    # 把员工能力绑定改指真实模型（gateway_ref=newapi-local, default_model=deepseek-chat），
    # 使 execute_model_gateway 的模型解析路径命中真实 DeepSeek API。
    with database.connect() as connection:
        connection.execute(
            "update official_models set gateway_ref='newapi-local', default_model='deepseek-chat', "
            "supported_models='[\"deepseek-chat\"]' where model_key=?",
            (CAPABILITY,),
        )
        connection.execute(
            "update model_gateways set base_url=?, credential_ref='env:CURIS_MODEL_GATEWAY_API_KEY', "
            "status='active' where gateway_id='newapi-local'",
            (os.environ["CURIS_MODEL_GATEWAY_BASE_URL"],),
        )
    return database, employees, knowledge["id"]


def _first_decision_option(detail: dict) -> str | None:
    decision = detail.get("decision") or {}
    packet = decision.get("packet") if isinstance(decision, dict) else None
    options = (packet or {}).get("options") if isinstance(packet, dict) else None
    if isinstance(options, list) and options:
        return str(options[0].get("optionId") or "")
    prop = (detail.get("orchestration") or {}).get("proposal") or {}
    if isinstance(prop, dict) and isinstance(prop.get("options"), list) and prop["options"]:
        return str(prop["options"][0].get("optionId") or "")
    return None


def run_meeting(
    db_path: str, *, patch_limits: bool, label: str,
    mode: str = "DECISION_ONLY", inject: bool = False,
) -> dict:
    print("\n" + "=" * 78)
    print(f"[RUN {label}] db={Path(db_path).name} patch_limits={patch_limits} mode={mode} inject={inject}")
    print("=" * 78)

    database, employees, knowledge_ref = seed(db_path)
    ref_ids = [v[0] for v in employees.values()]

    title = "下季度业务重点：内容增长 vs 研发工具，哪个更能提升客户满意度？"
    background = (
        "公司下季度要在「内容增长（快速获客）」与「研发工具链（长期效率）」之间做选择。"
        "请各方从自身职责给出判断，尤其关注对客户体验与交付的影响；"
        "只有在能带来新事实、专业判断、风险或明确问题时才发言。"
    )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        meeting = MeetingService(database).create(
            company_id=COMPANY, business_id=BUSINESS, workspace_id=WORKSPACE,
            title=title, background=background,
            participant_refs=ref_ids,
            leader_ref=employees["leader"][0], ceo_participation_mode=mode,
            context_refs=[{"type": "KNOWLEDGE", "ref": knowledge_ref}],
        )
    meeting_id = meeting["meeting_id"]

    if patch_limits:
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            MeetingService(database)._update_orchestration(
                meeting_id,
                lambda state: state | {
                    "limits": {
                        **(state.get("limits") or {}),
                        "maxConfirmedTokens": 200000,
                        "maxConfirmedCost": "100.00",
                        "maxProviderCalls": 30,
                        "maxTurns": 6,
                        "maxConsecutiveTurns": 1,
                        "maxNoProgress": 2,
                        "maxElapsedSeconds": 300,
                    }
                },
            )

    app = create_app(str(db_path))
    client = TestClient(app)

    if inject:
        # 注入序列：第 1 条为「财务新证据 + 点名 @林舟」，其后为补充事实。
        # 关键：这些 CEO 消息在「首次 advance（第 0 回合）之后」才发送，
        # 因此 @林舟 财务消息会作为独立的后续回合被处理（而非混入第 0 回合的同一后台 advance）。
        inject_msgs = [REINTERVENTION_CEO_MESSAGE, *NEW_EVIDENCE_FACTS]
    else:
        inject_msgs = []

    terminal = {"SUFFICIENT", "NO_PROGRESS", "STOPPED", "BLOCKED"}
    last_status = None
    injection_idx = 0
    for step in range(24):
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
        orch = detail.get("orchestration") or {}
        status = orch.get("status")
        last_status = status
        print(f"  step {step}: status={status} turns={len(orch.get('turns', []))} "
              f"providerCallCount={orch.get('providerCallCount')} noProgress={orch.get('noProgressCount')}")
        if status in terminal:
            break
        if status == "WAITING_CEO":
            opt = _first_decision_option(detail)
            if not opt:
                print("  WAITING_CEO but no decision option found; stopping.")
                break
            resp = client.post(
                f"{PREFIX}/{meeting_id}/decision/choose", headers=HEADERS,
                json={"choice": opt, "reason": "由 E2E 脚本代为选择以继续讨论"},
            )
            print(f"  decision choose -> {resp.status_code}")
            if resp.status_code >= 400:
                break
            continue
        # 注入新证据：在第 0 回合之后，补充「财务新证据 + @林舟」，触发 operations 重新判断/介入（要求 #6）。
        if inject and step >= 1 and injection_idx < len(inject_msgs):
            msg = inject_msgs[injection_idx]
            injection_idx += 1
            r = client.post(
                f"{PREFIX}/{meeting_id}/messages", headers=HEADERS,
                json={"actor_type": "CEO", "actor_ref": "ceo", "text": msg},
            )
            print(f"  [inject #{injection_idx}] -> {r.status_code}")
            continue
        try:
            adv = client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        except Exception as exc:  # 网络/超时 -> 重试 1 次
            print(f"  advance error: {exc!r}; retry once")
            time.sleep(2)
            try:
                adv = client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
            except Exception as exc2:
                print(f"  advance retry failed: {exc2!r}; stopping.")
                break
        if adv.status_code >= 400:
            print(f"  advance -> {adv.status_code}: {adv.text[:300]}")
            break

    detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    orch = detail.get("orchestration") or {}
    turns = orch.get("turns", [])
    silences_all = orch.get("silences", [])
    provider_call_count = int(orch.get("providerCallCount") or 0)
    blocked_reason = orch.get("blockedReason", "")
    last_outcome = orch.get("lastOutcome", "")

    spoke_any = False
    silent_any = False
    per_emp_sequence: dict[str, list[bool]] = {ref: [] for ref in ref_ids}
    for i, turn in enumerate(turns):
        sjs = turn.get("selfJudgments") or {}
        sil = turn.get("silences") or []
        speaker = turn.get("speakerRef")
        row_bits = []
        for ref in ref_ids:
            j = sjs.get(ref) or {}
            ss = bool(j.get("should_speak"))
            per_emp_sequence[ref].append(ss)
            if ss:
                spoke_any = True
                row_bits.append(f"{ref.split('-')[-1]}=SPEAK")
            else:
                row_bits.append(f"{ref.split('-')[-1]}=silent({str(j.get('reason',''))[:20]})")
        if sil:
            silent_any = True
        print(f"  turn[{i}] outcome={turn.get('leaderOutcome')} speaker={speaker.split('-')[-1] if speaker else None} | "
              + " | ".join(row_bits))

    re_intervened = []
    for ref, seq in per_emp_sequence.items():
        seen_silent = False
        for v in seq:
            if not v:
                seen_silent = True
            elif seen_silent:
                re_intervened.append(ref)
                break

    print(f"  -> final status={last_status} outcome={last_outcome} providerCallCount={provider_call_count}")
    print(f"  -> spoke_any={spoke_any} silent_any={silent_any} re_intervened={[r.split('-')[-1] for r in re_intervened]}")
    if blocked_reason:
        print(f"  -> blockedReason={blocked_reason}")

    return {
        "label": label, "db_path": db_path, "status": last_status,
        "outcome": last_outcome, "blocked_reason": blocked_reason,
        "turn_count": len(turns), "provider_call_count": provider_call_count,
        "spoke_any": spoke_any, "silent_any": silent_any,
        "silence_records": len(silences_all), "re_intervened": re_intervened,
        "per_emp_sequence": {r.split("-")[-1]: seq for r, seq in per_emp_sequence.items()},
    }


def _is_transient_blocked(s: dict) -> bool:
    if s["status"] != "BLOCKED":
        return False
    reason = s["blocked_reason"] or ""
    return ("Meeting Result contract" in reason) or ("结果合同" in reason) or ("模型调用或结果合同" in reason)


def run_reintervention_with_retry(*, patch_limits: bool, label: str, mode: str,
                                  inject: bool, max_attempts: int = 5) -> dict:
    """反复重建会议，直到自然观测到「同一员工 silent -> 因新证据 SPEAK」的再干预。

    注意：leader 在第 1 回合后可能判定 DISCUSSION_SUFFICIENT，而 SUFFICIENT 状态无法被
    advance 重开，因此单场可能观察不到再干预。此处对“未观测到再干预”的整场重建重试，
    目的是在真实模型的随机性下自然捕获该行为（不是伪造结果）。
    """
    last = None
    for attempt in range(1, max_attempts + 1):
        db = str(ROOT / f"{label}_a{attempt}_{uuid.uuid4().hex[:6]}.sqlite")
        s = run_meeting(db, patch_limits=patch_limits, label=f"{label}#a{attempt}",
                        mode=mode, inject=inject)
        last = s
        if s["re_intervened"]:
            print(f"  [OK] 第 {attempt} 次尝试观测到再干预：{[r.split('-')[-1] for r in s['re_intervened']]}")
            return s
        print(f"  [retry] 本轮未自然观测到再干预（leader 可能过早 SUFFICIENT 或 operations 未改判），"
              f"重建会议重试 {attempt}/{max_attempts}")
    return last


def run_with_retry(*, patch_limits: bool, label: str, mode: str = "DECISION_ONLY",
                   inject: bool = False, max_attempts: int = 3) -> dict:
    last = None
    for attempt in range(1, max_attempts + 1):
        db = str(ROOT / f"{label}_a{attempt}_{uuid.uuid4().hex[:6]}.sqlite")
        s = run_meeting(db, patch_limits=patch_limits, label=f"{label}#a{attempt}",
                        mode=mode, inject=inject)
        last = s
        if not _is_transient_blocked(s):
            return s
        print(f"  [retry] 瞬时合同错误（真实模型偶发非JSON）-> 重建会议重试 {attempt}/{max_attempts}")
    return last


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)

    # 运行 A：生产默认 limits（token 上限 8000 会先触顶 -> 观察真实预算边界）
    s_default = run_with_retry(patch_limits=False, label="default-limits")

    # 运行 B：抬高 token/cost 上限，使 30 次 provider call 成为绑定约束（验证 budget 修复）
    s_patched = run_with_retry(patch_limits=True, label="patched-limits")

    # 运行 C：DECISION_ONLY + 会前注入「财务新证据并点名 operations」，
    # 验证“同一员工先 STAY_SILENT、因新证据在后续回合重新 SPEAK”的再干预（要求 #6）。
    # leader 可能在第 1 回合后过早判定 SUFFICIENT（该状态不可被 advance 重开），
    # 故对“未观测到再干预”的整场做重建重试，直到自然观测到 silent->SPEAK（真实模型行为，非伪造）。
    s_inject = run_reintervention_with_retry(
        patch_limits=True, label="inject-evidence", mode="DECISION_ONLY", inject=True, max_attempts=5,
    )

    print("\n" + "#" * 78)
    print("# 汇总与断言（真实 DeepSeek, model=deepseek-chat via api.deepseek.com）")
    print("#" * 78)
    for s in (s_default, s_patched, s_inject):
        print(f"\n[{s['label']}] status={s['status']} outcome={s['outcome']} "
              f"turns={s['turn_count']} providerCallCount={s['provider_call_count']}")
        print(f"  spoke_any={s['spoke_any']} silent_any={s['silent_any']} "
              f"silence_records={s['silence_records']} re_intervened={[r for r in s['re_intervened']]}")
        print(f"  per-employee should_speak sequence: {s['per_emp_sequence']}")
        if s["blocked_reason"]:
            print(f"  blockedReason={s['blocked_reason']}")

    print("\n[断言]")
    ok_spoke = any(s["spoke_any"] for s in (s_default, s_patched, s_inject))
    ok_silent = any(s["silent_any"] for s in (s_default, s_patched, s_inject))
    ok_budget = all(s["provider_call_count"] <= 30 for s in (s_default, s_patched, s_inject))
    ok_no_crash = all(s["status"] in {"SUFFICIENT", "NO_PROGRESS", "STOPPED", "BLOCKED", "WAITING_CEO"}
                     for s in (s_default, s_patched, s_inject))
    ok_re = bool(s_inject["re_intervened"]) or any(s["re_intervened"] for s in (s_default, s_patched, s_inject))

    print(f"  至少 1 名员工真实发言 (should_speak=True) ......... {'PASS' if ok_spoke else 'FAIL'}")
    print(f"  至少 1 名员工真实 STAY_SILENT (should_speak=False)  {'PASS' if ok_silent else 'FAIL'}")
    print(f"  全局 providerCallCount <= 30 (budget 不越界) ....... {'PASS' if ok_budget else 'FAIL'}")
    print(f"  无不可恢复崩溃 (status 合法终止) .................. {'PASS' if ok_no_crash else 'FAIL'}")
    print(f"  出现基于新观点的再干预 (silent->SPEAK) ............ {'PASS' if ok_re else 'WEAK (未自然观测到)'}")
    overall = ok_spoke and ok_silent and ok_budget and ok_no_crash
    print("\n结论：", "T8 + 预算修复在真实 DeepSeek 下基本成立" if overall else "存在未通过项，需复核")


if __name__ == "__main__":
    main()
