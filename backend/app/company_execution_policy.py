"""Explicit Company text permission and bounded budget over existing event receipts."""
from __future__ import annotations
import hashlib
import json
import os
import stat
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
from .evolution_event_log import EvolutionEventLog
from .model_preferences import TenantModelPreferenceResolver
from .resource_scope_policy import ResourceScopePolicy
from .result_attention import ResultAttention
from .runtime import RuntimeScopeError
from .tenant_context import TenantContext

# Official CNY/USD pricing pages rechecked at checked_at; retain the seven-day expiry fence.
PRICE = {"model_name": "deepseek-flash", "model_version": "DeepSeek-V4.1-Flash-1017",
         "checked_at": "2026-11-05T11:52:26+00:00", "valid_until": "2026-11-12T11:52:26+00:00",
         "source_cny": "https://api-docs.deepseek.com/zh-cn/quick_start/pricing/",
         "source_usd": "https://api-docs.deepseek.com/quick_start/pricing/",
         "input_cny_per_million": 2, "output_cny_per_million": 8,
         "input_usd_per_million": 0.3, "output_usd_per_million": 1.2,
         "basis": "PEAK_CACHE_MISS_ESTIMATE_NOT_ACTUAL_PAYMENT"}
TRIAL_AUTHORIZATION = "ceo-deepseek-synthetic-20261105-two-calls-cny-0.10"
TRIAL_BUDGET_MICRO_CNY = 100000
CONTINUOUS_TEST_AUTHORIZATION = "ceo-v1-continuous-synthetic-20261106"

PACKAGES = {"com.curis.local.writing-authoring", "com.curis.local.content-growth", "com.curis.local.music"}
PREFIX = "company.text_policy."
AGENT_PREFIX = "company.agent_allowance."
AGENT_LEDGER = "curis-existing-codex-allowance-v1"
DATA_SCOPE = "CURRENT_DISCUSSION_SENT_TEXT_EMPLOYEE_REPLIES_AND_EXPLICIT_REFERENCES_V1"
MAX_INPUT = 16384
MAX_OUTPUT = 2048
FRAMING_ALLOWANCE = 256
RESERVE_MICRO_CNY = ((MAX_INPUT + FRAMING_ALLOWANCE) * PRICE["input_cny_per_million"]
                     + MAX_OUTPUT * PRICE["output_cny_per_million"])


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc)


def agent_work_claim_active(connection, *, tenant_id, company_id, work_ref, task_id, execution_ref):
    if not execution_ref:
        return False
    work = connection.execute(
        "select w.data_json,w.lifecycle_status,t.execution_ref from runtime_entities w join tasks t "
        "on t.tenant_id=w.tenant_id and t.company_id=w.company_id and t.workspace_id is w.workspace_id "
        "and t.work_ref=w.entity_id where w.tenant_id=? and w.company_id=? and w.entity_type='WORK' "
        "and w.entity_id=? and t.task_id=? and t.execution_ref=?",
        (tenant_id, company_id, work_ref, task_id, execution_ref),
    ).fetchone()
    route = (json.loads(work["data_json"]).get("responsibilityRouting") or {}) if work else {}
    claim = (route.get("executions") or {}).get(execution_ref) or {}
    return bool(work and work["lifecycle_status"] not in {"PAUSED", "CANCELLED", "ARCHIVED"}
                and route.get("status") == "EXECUTING" and claim.get("status") == "RUNNING"
                and claim.get("taskRef") == task_id)


class CompanyExecutionPolicy:
    def __init__(self, database):
        self.db = database
        self.events = EvolutionEventLog(database)
        self.models = TenantModelPreferenceResolver(database)

    def actor(self, company):
        actor = ResultAttention(self.db).actor(company)
        identity = TenantContext.current_identity()
        if identity.get("role", "").lower() not in {"ceo", "owner"} or identity.get("company_id") not in {None, "", company}:
            raise RuntimeScopeError("只有当前公司的所有者可管理文字外发许可。")
        return actor

    def agent_readiness(self, company):
        actor = self.actor(company)
        with self.db.connect() as con:
            authorization = self.agent_authorization(con)
            reference = authorization["authorization_ref"]
            policies = self.agent_rows(con, "changed", reference)
            policy = policies[-1] if policies else {}
            used = len(self.agent_rows(con, "reserved", reference))
            all_reserved = self.agent_rows(con, "reserved")
            history_refs = [AGENT_LEDGER, *[row["authorization_ref"] for row in self.agent_rows(con, "authorization.created")]]
            history = [{"authorization_ref": ref, "used_calls": sum(
                row.get("authorization_ref", AGENT_LEDGER) == ref for row in all_reserved)}
                for ref in history_refs if ref != reference]
            continuity = self.continuity(con, AGENT_LEDGER)
            rows = con.execute("select b.id,e.name from employee_capability_bindings b join employee_instances e "
                "on e.tenant_id=b.tenant_id and e.id=b.employee_id where b.tenant_id=? and e.company_id=? "
                "and b.capability_type='agent' and b.enabled=1", (TenantContext.current_tenant_id(), company)).fetchall()
            options = []
            for row in rows:
                try:
                    snapshot = self.agent_binding_snapshot(con, company, row["id"])
                    capability = self.db.get_tenant_private_capability(TenantContext.current_tenant_id(), "agent", snapshot["capability_id"])
                    options.append({"binding_ref": row["id"], "employee_name": row["name"], "agent_name": capability["display_name"],
                                    "agent_kind": snapshot.get("agent_kind", "codex-cli"),
                                    "authorization_subject": self.agent_subject([snapshot])})
                except (ValueError, RuntimeScopeError):
                    continue
        scoped = policy.get("actor") == actor and policy.get("company_id") == company
        mode = policy.get("limit_mode", "FOUR_CALLS") if scoped else "FOUR_CALLS"
        unlimited = mode == "UNLIMITED"
        available = (policy.get("enabled") and scoped and mode in {"FOUR_CALLS", "UNLIMITED"} and (unlimited or used < 4)
                     and continuity["status"] == "VALID")
        return {"state": "AVAILABLE" if available else "BLOCKED", "authorization_ref": reference,
                "authorization_subject": authorization.get("authorization_subject", self.agent_subject([])),
                "authorization": {"authorization_ref": authorization["authorization_ref"],
                                  "original_max_calls": authorization["max_calls"],
                                  "max_calls": None if unlimited else 4,
                                  "max_seconds": authorization["max_seconds"],
                                  "billing_basis": authorization.get("billing_basis", "EXISTING_SUBSCRIPTION_OR_PREPAID_CREDITS")},
                "authorization_history": history, "total_reserved_calls": len(all_reserved),
                "new_authorization_allowed": bool(policy) and policy.get("actor") == actor and not bool(os.environ.get("CURIS_AGENT_AUTHORIZATION_REF"))
                    and continuity["status"] == "VALID" and ((mode == "FOUR_CALLS" and used >= 4) or not policy.get("enabled")),
                "policy": policy if policy.get("company_id") == company else None,
                "revision": policy.get("revision", ""), "used_calls": used, "remaining_calls": None if unlimited else max(0, 4-used),
                "limit_mode": mode, "effective_max_calls": None if unlimited else 4,
                "max_seconds": 90, "actual_paid": None, "resume_allowed": False,
                "reason": "已允许所选 Agent 在原工作中使用已明确确认的额度；结果未知的调用仍占用次数。" if available
                    else "请确认所选 Agent 的独立额度使用许可；每次最多 90 秒，不自动重试、购买或充值。",
                "continuity": continuity["status"], "binding_options": options}

    def agent_rows(self, con, kind, authorization_ref=None):
        values = [json.loads(row[0]) for row in con.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? and event_type=? order by event_id",
            (TenantContext.current_tenant_id(), AGENT_LEDGER, AGENT_PREFIX + kind))]
        return [value for value in values if authorization_ref is None
                or value.get("authorization_ref", AGENT_LEDGER) == authorization_ref]

    def agent_authorization(self, con):
        grants = self.agent_rows(con, "authorization.created")
        current = grants[-1] if grants else {"authorization_ref": AGENT_LEDGER, "max_calls": 4, "max_seconds": 90}
        pinned = os.environ.get("CURIS_AGENT_AUTHORIZATION_REF", "")
        if pinned and pinned != current["authorization_ref"]:
            raise RuntimeScopeError("当前许可与受管启动的明确授权不一致，不能切换或重置。")
        return current

    @staticmethod
    def agent_subject(snapshots):
        subjects = [{"agent_kind": item.get("agent_kind", "codex-cli"),
                     "agent_id": item.get("agent_id", "codex"),
                     **({"installation_ref": item["installation_ref"]} if item.get("agent_kind") == "acp-stdio" else {})}
                    for item in snapshots]
        if not subjects:
            return {"agent_kind": "codex-cli", "agent_id": "codex"}
        if any(subject != subjects[0] for subject in subjects):
            raise ValueError("一次授权只能选择同一 Agent 类型和安装版本。")
        return subjects[0]

    def new_agent_authorization(self, company, *, request_id, previous_authorization_ref,
                                expected_revision, binding_refs, consent=False):
        actor = self.actor(company)
        if os.environ.get("CURIS_AGENT_AUTHORIZATION_REF"):
            raise RuntimeScopeError("本次受管执行仅允许已指定的授权，不能增加新额度。")
        if (consent is not True or not isinstance(request_id, str) or not 0 < len(request_id) <= 128
                or not 1 <= len(binding_refs) <= 16):
            raise ValueError("新授权需要明确确认四次新调用、员工范围与独立请求。")
        incoming = {"company": company, "actor": actor, "previous_authorization_ref": previous_authorization_ref,
            "expected_revision": expected_revision, "binding_refs": sorted(set(binding_refs)), "consent": True}
        with self.db.connect() as con:
            con.execute("begin immediate")
            current = self.agent_authorization(con)
            created = self.agent_rows(con, "authorization.created")
            previous_request = next((row for row in created if row["request_id"] == request_id), None)
            if previous_request:
                if previous_request["input_hash"] != digest(incoming):
                    raise ValueError("同一新授权请求不能更换内容。")
                if current["authorization_ref"] != previous_request["authorization_ref"]:
                    raise RuntimeScopeError("该历史授权已被后续明确授权替代；不能重新激活。")
            else:
                policies = self.agent_rows(con, "changed", current["authorization_ref"])
                old = policies[-1] if policies else {}
                used = len(self.agent_rows(con, "reserved", current["authorization_ref"]))
                if current["authorization_ref"] != previous_authorization_ref or old.get("revision", "") != expected_revision:
                    raise RuntimeScopeError("原许可已变化，请先读取当前许可。")
                snapshots = [self.agent_binding_snapshot(con, company, ref) for ref in incoming["binding_refs"]]
                subject = self.agent_subject(snapshots)
                old_subject = current.get("authorization_subject", self.agent_subject([]))
                continuity = self.continuity(con, AGENT_LEDGER)["status"]
                fresh_acp = (not old and current["authorization_ref"] == AGENT_LEDGER
                    and not self.agent_rows(con, "reserved") and not created
                    and subject["agent_kind"] == "acp-stdio" and continuity == "FRESH")
                if not fresh_acp and (not old or old.get("actor") != actor or old.get("company_id") != company or continuity != "VALID"):
                    raise RuntimeScopeError("原许可所有者或完整历史无法核验，不能开启新授权。")
                if subject == old_subject and old.get("enabled") and (old.get("limit_mode", "FOUR_CALLS") != "FOUR_CALLS" or used < 4):
                    raise RuntimeScopeError("原授权仍有效，请先使用或明确撤销；不能叠加活跃许可。")
                reference = "agent-authorization-" + uuid4().hex
                grant = {"authorization_ref": reference, "previous_authorization_ref": previous_authorization_ref,
                    "company_id": company, "actor": actor, "request_id": request_id, "input_hash": digest(incoming),
                    "authorization_subject": subject, "max_calls": 4, "max_seconds": 90, "created_at": now().isoformat(),
                    "billing_basis": "AGENT_ACCOUNT_COST_UNVERIFIED" if subject["agent_kind"] == "acp-stdio" else "EXISTING_SUBSCRIPTION_OR_PREPAID_CREDITS", "no_purchase_or_topup": True}
                self.events.record_in_connection(con, correlation_id=AGENT_LEDGER,
                    event_type=AGENT_PREFIX + "authorization.created", payload=grant,
                    idempotency_key="agent-new-authorization:" + request_id)
                policy = {**grant, "revision": uuid4().hex, "enabled": True, "bindings": snapshots}
                self.events.record_in_connection(con, correlation_id=AGENT_LEDGER,
                    event_type=AGENT_PREFIX + "changed", payload=policy,
                    idempotency_key="agent-new-authorization-policy:" + request_id)
                self.publish_anchor(con, AGENT_LEDGER)
        return self.agent_readiness(company)

    def agent_binding_snapshot(self, con, company, binding_ref):
        binding = con.execute("select b.* from employee_capability_bindings b join employee_instances e "
            "on e.tenant_id=b.tenant_id and e.id=b.employee_id where b.tenant_id=? and e.company_id=? "
            "and b.id=? and b.enabled=1 and e.enabled=1 and e.deleted_at is null "
            "and b.capability_type='agent' and b.capability_source='tenant_private'",
            (TenantContext.current_tenant_id(), company, binding_ref)).fetchone()
        if binding is None:
            raise RuntimeScopeError("Agent 绑定不属于当前公司的有效员工。")
        capability = self.db.get_tenant_private_capability(TenantContext.current_tenant_id(), "agent", binding["capability_id"])
        if not capability or capability.get("status") != "active":
            raise RuntimeScopeError("所选 Agent 配置不可用。")
        metadata = capability.get("metadata") or {}
        kind = metadata.get("kind")
        snapshot = {"binding_ref": binding_ref, "capability_id": binding["capability_id"],
                    "employee_ref": binding["employee_id"], "capability_sha256": digest(capability)}
        if kind == "codex-cli":
            return snapshot  # Preserve historical Codex snapshot/authorization identity.
        if kind == "acp-stdio":
            from .ai_capability_registry import acp_installation
            try: installation = acp_installation(metadata.get("agent_id", ""))
            except (OSError, ValueError) as error:
                raise RuntimeScopeError("ACP 安装无法核验。") from error
            if metadata.get("installation_ref") != installation["installation_ref"]:
                raise RuntimeScopeError("ACP 安装已变化，请重新登记和授权。")
            return {**snapshot, "agent_kind": kind, "agent_id": installation["agent_id"],
                    "installation_ref": installation["installation_ref"]}
        raise RuntimeScopeError("所选 Agent 类型尚不支持额度许可。")

    def save_agent_allowance(self, company, *, request_id, expected_revision, enabled, binding_refs, consent=False,
                             authorization_ref=None, unlimited_consent=False):
        actor = self.actor(company)
        if not request_id or len(request_id) > 128 or type(enabled) is not bool:
            raise ValueError("许可请求不完整。")
        if enabled and (consent is not True or not 1 <= len(binding_refs) <= 16):
            raise ValueError("请明确确认既有额度使用范围。")
        if type(unlimited_consent) is not bool or (unlimited_consent and (not enabled or consent is not True)):
            raise ValueError("不限次数需要明确确认员工与使用范围。")
        incoming = dict(company=company, enabled=enabled, binding_refs=sorted(set(binding_refs)), consent=consent)
        if unlimited_consent:
            incoming["unlimited_consent"] = True
        with self.db.connect() as con:
            con.execute("begin immediate")
            reference = self.agent_authorization(con)["authorization_ref"]
            if authorization_ref != reference and not (authorization_ref is None and reference == AGENT_LEDGER):
                raise RuntimeScopeError("请明确当前授权，不能隐式切换额度。")
            policies = self.agent_rows(con, "changed", reference)
            if any(row["request_id"] == request_id and row.get("authorization_ref", AGENT_LEDGER) != reference
                   for row in self.agent_rows(con, "changed")):
                raise RuntimeScopeError("旧授权请求不能转移到新授权。")
            old = policies[-1] if policies else {}
            if old and old.get("actor") != actor:
                raise RuntimeScopeError("不能更换其他所有者的额度许可。")
            if old and old.get("company_id") != company:
                raise RuntimeScopeError("当前额度许可属于其他公司，不能覆盖。")
            if self.continuity(con, AGENT_LEDGER)["status"] not in {"VALID", "FRESH"}:
                raise RuntimeScopeError("额度记录与本机状态不一致，不能恢复或重置剩余次数。")
            previous = next((p for p in policies if p["request_id"] == request_id), None)
            if previous:
                if previous["input_hash"] != digest(incoming):
                    raise ValueError("同一许可请求不能更换内容。")
            else:
                if old.get("revision", "") != expected_revision:
                    raise ValueError("许可已更新，请读取最新状态。")
                snapshots = [self.agent_binding_snapshot(con, company, ref) for ref in incoming["binding_refs"]] if enabled else []
                if enabled and self.agent_subject(snapshots) != self.agent_authorization(con).get("authorization_subject", self.agent_subject([])):
                    raise RuntimeScopeError("所选 Agent 不属于当前授权；请明确另行授权，不能沿用 Codex 或其他 Agent 额度。")
                policy = {"authorization_ref": reference, "company_id": company, "actor": actor,
                    "request_id": request_id, "input_hash": digest(incoming), "revision": uuid4().hex,
                    "enabled": enabled, "bindings": snapshots, "max_calls": 4, "max_seconds": 90,
                    "billing_basis": self.agent_authorization(con).get("billing_basis", "EXISTING_SUBSCRIPTION_OR_PREPAID_CREDITS"), "no_purchase_or_topup": True}
                if unlimited_consent:
                    policy.update(limit_mode="UNLIMITED", max_calls=None)
                self.events.record_in_connection(con, correlation_id=AGENT_LEDGER, event_type=AGENT_PREFIX+"changed",
                    payload=policy, idempotency_key="agent-allowance:"+request_id)
                self.publish_anchor(con, AGENT_LEDGER)
        return self.agent_readiness(company)

    def require_agent_execution(self, company, binding_ref=None):
        readiness = self.agent_readiness(company)
        if readiness["state"] != "AVAILABLE":
            raise RuntimeScopeError(readiness["reason"])
        if binding_ref:
            with self.db.connect() as con:
                snapshot = self.agent_binding_snapshot(con, company, binding_ref)
            if snapshot not in readiness["policy"]["bindings"]:
                raise RuntimeScopeError("所选 Agent 或版本已变化，未包含在当前许可中。")
        return readiness

    def require_unreserved_agent_work(self, company, work_ref, *, connection=None):
        def check(con):
            unresolved = con.execute(
                "select 1 from evolution_events e join tasks t on t.task_id=e.correlation_id "
                "and t.tenant_id=e.tenant_id where e.tenant_id=? and t.company_id=? "
                "and t.work_ref=? and e.event_type='agent.execution.outcome_unknown' limit 1",
                (TenantContext.current_tenant_id(), company, work_ref),
            ).fetchone()
            if unresolved:
                raise RuntimeScopeError("原工作执行状态未确认，不能重复启动。")
            if any(row["company_id"] == company and row["work_ref"] == work_ref
                   for row in self.agent_rows(con, "reserved")):
                raise RuntimeScopeError("原工作已发起过 Agent 调用，效果未核验前不能重复启动。")
        if connection is not None:
            check(connection)
        else:
            self.actor(company)
            with self.db.connect() as con:
                check(con)

    def reserve_agent_call(self, company, binding_ref, task_id, work_ref, revision, authorization_ref=None):
        actor = self.actor(company)
        with self.db.connect() as con:
            con.execute("begin immediate")
            reference = self.agent_authorization(con)["authorization_ref"]
            if authorization_ref != reference and not (authorization_ref is None and reference == AGENT_LEDGER):
                raise RuntimeScopeError("执行许可不属于原明确授权。")
            policies = self.agent_rows(con, "changed", reference)
            policy = policies[-1] if policies else {}
            reserved = self.agent_rows(con, "reserved", reference)
            if (not policy.get("enabled") or policy.get("actor") != actor or policy.get("company_id") != company or policy.get("revision") != revision
                    or self.continuity(con, AGENT_LEDGER)["status"] != "VALID"):
                raise RuntimeScopeError("执行前许可已撤销、变化或无法核验。")
            if self.agent_binding_snapshot(con, company, binding_ref) not in policy["bindings"]:
                raise RuntimeScopeError("执行前 Agent 绑定发生变化。")
            task = con.execute("select task_id,status,workspace_id,execution_ref from tasks where tenant_id=? and company_id=? and task_id=? and work_ref=?",
                (TenantContext.current_tenant_id(), company, task_id, work_ref)).fetchone()
            if not task or task["status"] not in {"PENDING", "PARSED", "RUNNING", "RESUMED"} or any(row["task_id"] == task_id for row in reserved):
                raise RuntimeScopeError("原工作不存在或已经占用过调用次数，不能重复启动。")
            if task["execution_ref"]:
                if not agent_work_claim_active(con, tenant_id=TenantContext.current_tenant_id(), company_id=company,
                                               work_ref=work_ref, task_id=task_id, execution_ref=task["execution_ref"]):
                    raise RuntimeScopeError("原工作已停止或执行关联发生变化，不能发起 Agent 调用。")
            self.require_unreserved_agent_work(company, work_ref, connection=con)
            mode = policy.get("limit_mode", "FOUR_CALLS")
            if mode not in {"FOUR_CALLS", "UNLIMITED"}:
                raise RuntimeScopeError("执行许可的次数范围无法核验。")
            if mode == "FOUR_CALLS" and len(reserved) >= 4:
                raise RuntimeScopeError("本轮 4 次额度已用尽，未知结果不返还次数。")
            value = {"authorization_ref": reference, "task_id": task_id, "work_ref": work_ref, "company_id": company, "binding_ref": binding_ref,
                     "revision": revision, "max_seconds": 90, "effect": "UNKNOWN", "actual_paid": None}
            self.events.record_in_connection(con, correlation_id=AGENT_LEDGER, event_type=AGENT_PREFIX+"reserved",
                payload=value, idempotency_key="agent-call:"+task_id)
            self.publish_anchor(con, AGENT_LEDGER)
        return value

    def rows(self, con, company, kind):
        return [json.loads(row[0]) for row in con.execute(
            "select payload from evolution_events where tenant_id=? and event_type=? and correlation_id=? order by event_id",
            (TenantContext.current_tenant_id(), PREFIX + kind, company)).fetchall()]

    def latest(self, con, company):
        rows = self.rows(con, company, "changed")
        return rows[-1] if rows else None

    def anchor_location(self, company):
        database = Path(os.path.abspath(self.db.path))
        info = database.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid():
            raise ValueError("当前资料文件不能核验。")
        for parent in database.parents:
            if stat.S_ISLNK(parent.lstat().st_mode):
                raise ValueError("当前资料路径不允许链接。")
        configured = os.environ.get("CURIS_DESKTOP_DATA_ROOT")
        if configured:
            root = Path(configured)
            if not root.is_absolute() or database != root / "data/curis.sqlite":
                raise ValueError("当前资料路径不能核验。")
            parts = ("recovery", "company-text-policy")
        else:
            root = database.parent
            parts = ("recovery", "company-text-policy", digest(str(database)))
        name = digest([TenantContext.current_tenant_id(), company]) + ".json"
        scope = digest([str(database), TenantContext.current_tenant_id(), company])
        return root, parts, name, scope

    @contextmanager
    def anchor_directory(self, company, *, create=False):
        root, parts, name, scope = self.anchor_location(company)
        # Never follow a parent alias into another profile. No directory enumeration.
        for parent in (root, *root.parents):
            info = parent.lstat()
            if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
                raise ValueError("资料状态目录不安全。")
        info = root.lstat()
        if info.st_uid != os.getuid() or info.st_mode & 0o022:
            raise ValueError("当前资料目录权限不能核验。")
        descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for index, part in enumerate(parts):
                if create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=descriptor)
                        os.fsync(descriptor)
                    except FileExistsError:
                        pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
                info = os.fstat(child)
                safe = info.st_uid == os.getuid() and not info.st_mode & 0o022
                if index >= 1:
                    safe = safe and stat.S_IMODE(info.st_mode) == 0o700
                if not safe:
                    os.close(child)
                    raise ValueError("资料状态目录权限不能核验。")
                os.close(descriptor)
                descriptor = child
            yield descriptor, name, scope
        finally:
            os.close(descriptor)

    def ledger_fingerprint(self, con, company):
        if company == AGENT_LEDGER:
            rows = con.execute("select event_type,payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type in (?,?,?) order by event_id", (TenantContext.current_tenant_id(), AGENT_LEDGER,
                AGENT_PREFIX+"changed", AGENT_PREFIX+"reserved", AGENT_PREFIX+"authorization.created")).fetchall()
            return digest([[row[0], json.loads(row[1])] for row in rows]), bool(rows)
        rows = con.execute("select event_type,payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type in (?,?,?) order by event_id", (TenantContext.current_tenant_id(), company,
            PREFIX + "changed", PREFIX + "reserved", PREFIX + "settled")).fetchall()
        return digest([[row[0], json.loads(row[1])] for row in rows]), bool(rows)

    def continuity(self, con, company):
        fingerprint, has_history = self.ledger_fingerprint(con, company)
        policy = self.latest(con, company) or {}
        anchor = None
        try:
            with self.anchor_directory(company) as (directory, name, scope):
                descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
                try:
                    info = os.fstat(descriptor)
                    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid()
                            or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 4096):
                        raise ValueError("许可状态文件不能核验。")
                    anchor = json.loads(os.read(descriptor, 4097))
                    if (not isinstance(anchor, dict) or set(anchor) != {"version", "scope", "ledger"}
                            or anchor["version"] != 1 or anchor["scope"] != scope
                            or not isinstance(anchor["ledger"], str) or len(anchor["ledger"]) != 64
                            or any(c not in "0123456789abcdef" for c in anchor["ledger"])):
                        raise ValueError("许可状态内容不能核验。")
                finally:
                    os.close(descriptor)
            status = "VALID" if anchor["ledger"] == fingerprint else "MISMATCH"
        except FileNotFoundError:
            status = "MISSING" if has_history else "FRESH"
        except (OSError, ValueError, TypeError):
            status = "UNVERIFIABLE"
        required = status not in {"VALID", "FRESH"} or bool(policy.get("history_reconfirmation_required"))
        return {"status": status, "needs_reconfirmation": required,
                "history_incomplete": required or bool(policy.get("history_incomplete")),
                "can_confirm": status != "UNVERIFIABLE",
                "token": digest([status, policy.get("budget_epoch"),
                    [fingerprint, anchor] if required else None])}

    def publish_anchor(self, con, company):
        fingerprint, _ = self.ledger_fingerprint(con, company)
        temporary, identity = None, None
        try:
            with self.anchor_directory(company, create=True) as (directory, name, scope):
                try:
                    existing = os.stat(name, dir_fd=directory, follow_symlinks=False)
                    if (not stat.S_ISREG(existing.st_mode) or existing.st_nlink != 1
                            or existing.st_uid != os.getuid() or stat.S_IMODE(existing.st_mode) != 0o600):
                        raise ValueError("既有许可状态文件不安全。")
                except FileNotFoundError:
                    pass
                temporary = name + "." + uuid4().hex + ".tmp"
                descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
                identity = os.fstat(descriptor)
                try:
                    with os.fdopen(descriptor, "wb") as stream:
                        stream.write(json.dumps({"version": 1, "scope": scope, "ledger": fingerprint}, sort_keys=True).encode())
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
                    temporary = None
                    os.fsync(directory)
                finally:
                    if temporary:
                        current = os.stat(temporary, dir_fd=directory, follow_symlinks=False)
                        if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino):
                            os.unlink(temporary, dir_fd=directory)
        except (OSError, ValueError) as error:
            raise RuntimeScopeError("本机许可状态未能持久保存，执行已停止；请保留现场并重新核验。") from error

    def preview(self, options, continuity):
        return {**options, "continuity": continuity,
                "preview_token": digest([options["preview_token"], continuity["token"]])}

    def model_snapshot(self, key):
        model = self.models._require_eligible_model(TenantContext.current_tenant_id(), key)
        if model["source"] == "tenant_private":
            metadata = self.db.get_tenant_private_capability(TenantContext.current_tenant_id(), "model", key)["metadata"]
            base = str(metadata.get("base_url") or "").rstrip("/")
            protocol, chat_path = metadata.get("provider_protocol"), metadata.get("chat_path")
        else:
            gateway = self.db.get_model_gateway(model["gateway_ref"]) or {}
            if gateway.get("status") != "active":
                raise RuntimeScopeError("模型连接已停用。")
            base = str(gateway.get("base_url") or "").rstrip("/")
            protocol, chat_path = "openai_chat", "/v1/chat/completions"
        url = urlsplit(base)
        if (model["model_name"] != PRICE["model_name"] or base not in {"https://api.deepseek.com", "https://api.deepseek.com/v1"}
                or url.username or url.password or protocol != "openai_chat" or chat_path not in {"/chat/completions", "/v1/chat/completions"}):
            raise RuntimeScopeError("当前模型或发送目的地没有经核验的适用价格依据。")
        if not datetime.fromisoformat(PRICE["checked_at"]) <= now() < datetime.fromisoformat(PRICE["valid_until"]):
            raise RuntimeScopeError("模型价格依据已过期或时间不可确认，请先更新经核验的价格。")
        return {**model, "destination": base, "protocol": protocol, "chat_path": chat_path, "price": PRICE.copy()}

    def options(self, company):
        self.actor(company)
        with self.db.connect() as con:
            rows = con.execute("select workspace_id,name,blueprint_json from workspaces where tenant_id=? and company_id=? "
                "and business_relation_status='RESOLVED' and status!='ARCHIVED'", (TenantContext.current_tenant_id(), company)).fetchall()
        workspaces = []
        for row in rows:
            try:
                blueprint = json.loads(row["blueprint_json"])
            except (ValueError, TypeError):
                continue
            if isinstance(blueprint, dict) and isinstance(blueprint.get("packageId"), str) and blueprint.get("packageId") in PACKAGES:
                workspaces.append({"workspace_id": row["workspace_id"], "name": row["name"], "package_id": blueprint["packageId"]})
        models = []
        for item in self.models.available_models():
            try:
                models.append(self.model_snapshot(item["model_key"]))
            except (ValueError, RuntimeScopeError):
                pass
        value = {"company_id": company, "workspaces": workspaces, "models": models, "price": PRICE.copy(),
                 "max_input_bytes": MAX_INPUT, "max_output_tokens": MAX_OUTPUT,
                 "per_request_ceiling_cny": str(Decimal(RESERVE_MICRO_CNY) / 1000000), "data_scope": DATA_SCOPE}
        return {**value, "preview_token": digest(value)}

    def totals(self, con, company):
        policy = self.latest(con, company) or {}
        epoch = policy.get("budget_epoch")
        settlements = {s["attempt_id"]: s for s in self.rows(con, company, "settled")}
        charged = reserved = 0
        for reservation in self.rows(con, company, "reserved"):
            if epoch and reservation["grant"].get("budget_epoch") != epoch:
                continue
            settled = settlements.get(reservation["attempt_id"])
            if settled is None:
                reserved += reservation["amount_micro_cny"]
            else:
                charged += settled["estimated_micro_cny"]
        return {"reserved_micro_cny": reserved, "estimated_micro_cny": charged, "actual_paid": None}

    def read(self, company):
        options = self.options(company)
        with self.db.connect() as con:
            con.execute("begin immediate")
            policy, totals = self.latest(con, company), self.totals(con, company)
            continuity = self.continuity(con, company)
            if continuity["needs_reconfirmation"]:
                totals = {"reserved_micro_cny": None, "estimated_micro_cny": None, "actual_paid": None}
        return {**self.preview(options, continuity), "policy": policy, "totals": totals}

    def save(self, company, *, request_id, expected_revision, enabled, consent=False, workspace_ids=None,
             model_keys=None, budget_cny="", valid_hours=24, preview_token="", history_acknowledged=False, trial_authorization_ref="", test_authorization_ref=""):
        actor = self.actor(company)
        incoming = dict(request_id=request_id, expected_revision=expected_revision, enabled=enabled, consent=consent,
                        workspace_ids=workspace_ids or [], model_keys=model_keys or [], budget_cny=budget_cny,
                        valid_hours=valid_hours, preview_token=preview_token, history_acknowledged=history_acknowledged)
        if test_authorization_ref not in ("", CONTINUOUS_TEST_AUTHORIZATION):
            raise ValueError("未知的持续验收授权。")
        if test_authorization_ref:
            incoming["test_authorization_ref"] = test_authorization_ref
        if trial_authorization_ref not in ("", TRIAL_AUTHORIZATION):
            raise ValueError("未知的本轮试用授权。")
        if trial_authorization_ref:
            incoming["trial_authorization_ref"] = trial_authorization_ref
        if not request_id or len(request_id) > 128 or type(enabled) is not bool:
            raise ValueError("许可请求不完整。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            old = self.latest(con, company)
            continuity = self.continuity(con, company)
            if not continuity["can_confirm"]:
                raise RuntimeScopeError("本机许可状态无法核验，已停止文字执行；请保留现场，不会自动修复许可。")
            previous = next((p for p in self.rows(con, company, "changed") if p["request_id"] == request_id), None)
            if previous:
                if continuity["needs_reconfirmation"]:
                    raise RuntimeScopeError("资料状态变化，旧保存请求不能恢复费用许可；请重新读取并明确确认新的后续额度。")
                if previous["input_hash"] != digest(incoming):
                    raise ValueError("同一许可请求不能更换内容。")
                return {"policy": previous, "totals": self.totals(con, company)}
            if (old or {}).get("revision", "") != expected_revision:
                raise ValueError("公司许可已更新，请读取最新版本后确认。")
            policy = {"tenant_id": TenantContext.current_tenant_id(), "company_id": company, "actor": actor,
                      "revision": digest([TenantContext.current_tenant_id(), company, request_id]), "request_id": request_id,
                      "input_hash": digest(incoming), "enabled": enabled, "created_at": now().isoformat(),
                      "budget_epoch": (old or {}).get("budget_epoch") or uuid4().hex,
                      "history_incomplete": continuity["history_incomplete"],
                      "history_reconfirmation_required": continuity["needs_reconfirmation"] and not enabled}
            continuous = (old or {}).get("test_authorization_ref") or test_authorization_ref
            if continuous:
                if continuous != CONTINUOUS_TEST_AUTHORIZATION:
                    raise RuntimeScopeError("持续验收授权无法核验。")
                policy["test_authorization_ref"] = continuous
                if enabled and continuity["needs_reconfirmation"]:
                    raise RuntimeScopeError("验收历史无法核验，不能通过重新授权重置记录。")
                if not enabled:
                    policy.update(workspace_ids=(old or {}).get("workspace_ids", []), models=(old or {}).get("models", []))
            trial = (old or {}).get("trial_authorization_ref") or trial_authorization_ref
            if trial:
                policy["trial_authorization_ref"] = trial
                if not enabled:
                    policy.update(workspace_ids=(old or {}).get("workspace_ids", []), models=(old or {}).get("models", []))
                if enabled and continuity["needs_reconfirmation"]:
                    raise RuntimeScopeError("本轮试用历史无法核验，不能通过重新授权恢复次数或费用额度。")
            if enabled:
                if continuity["needs_reconfirmation"]:
                    if history_acknowledged is not True:
                        raise ValueError("历史费用不可完整核实，旧许可已失效；请明确确认新的后续预算和文字外发范围。")
                    policy["budget_epoch"] = uuid4().hex
                options = self.preview(self.options(company), continuity)
                if consent is not True or preview_token != options["preview_token"]:
                    raise ValueError("请重新核对工作范围、模型目的地与价格，并明确同意文字外发。")
                if not workspace_ids or not model_keys or len(set(workspace_ids)) != len(workspace_ids) or len(set(model_keys)) != len(model_keys):
                    raise ValueError("请选择准确工作空间和模型。")
                if set(workspace_ids) - {w["workspace_id"] for w in options["workspaces"]} or set(model_keys) - {m["model_key"] for m in options["models"]}:
                    raise RuntimeScopeError("所选工作空间或模型不在当前可授权范围。")
                try:
                    amount = Decimal(str(budget_cny))
                    if not amount.is_finite() or amount <= 0 or amount > 100000 or amount * 1000000 != (amount * 1000000).to_integral_value():
                        raise InvalidOperation
                    budget = int(amount * 1000000)
                except (InvalidOperation, ValueError):
                    raise ValueError("请填写准确的人民币累计预算，最多六位小数。") from None
                if trial and not continuous and (len(workspace_ids) != 1 or len(model_keys) != 1
                        or ((old or {}).get("trial_authorization_ref") or (old or {}).get("test_authorization_ref")) and
                            (workspace_ids != old.get("workspace_ids") or model_keys != [m["model_key"] for m in old.get("models", [])])):
                    raise ValueError("本轮试用只允许原独立工作空间和单一模型。")
                if continuous and (len(model_keys) != 1 or ((old or {}).get("models") and
                        model_keys != [m["model_key"] for m in old["models"]])):
                    raise ValueError("持续验收仅允许原批准模型；新增工作空间仍须明确授权。")
                if continuous and not ((old or {}).get("trial_authorization_ref") or (old or {}).get("test_authorization_ref")) and self.rows(con, company, "reserved"):
                    raise RuntimeScopeError("持续验收仅可延续原合成授权，不能接管其他历史调用。")
                if trial and not (old or {}).get("trial_authorization_ref") and self.rows(con, company, "reserved"):
                    raise RuntimeScopeError("本轮试用必须使用没有既有调用记录的独立合成公司。")
                if trial and not continuous and budget > TRIAL_BUDGET_MICRO_CNY:
                    raise ValueError("本轮试用累计预算不得超过人民币0.10元。")
                if type(valid_hours) is not int or not 1 <= valid_hours <= 168:
                    raise ValueError("许可有效期应在1小时至7天内。")
                expiry = now() + timedelta(hours=valid_hours)
                if expiry > datetime.fromisoformat(PRICE["valid_until"]):
                    raise ValueError("所选有效期超过当前价格依据的有效期。")
                totals = {"reserved_micro_cny": 0, "estimated_micro_cny": 0} if continuity["needs_reconfirmation"] else self.totals(con, company)
                if not continuous and budget < sum(totals[k] for k in ("reserved_micro_cny", "estimated_micro_cny")):
                    raise ValueError("预算不能低于已占额与已有估算；可直接撤销未来执行。")
                policy.update(workspace_ids=workspace_ids, models=[m for m in options["models"] if m["model_key"] in model_keys],
                              budget_micro_cny=budget, currency="CNY", expires_at=expiry.isoformat(), consent=True, data_scope=DATA_SCOPE,
                              execution_limits={"max_input_bytes": MAX_INPUT, "max_output_tokens": MAX_OUTPUT, "reserve_micro_cny": RESERVE_MICRO_CNY})
            self.events.record_in_connection(con, correlation_id=company, event_type=PREFIX + "changed", payload=policy,
                idempotency_key="company-text-policy:" + policy["revision"])
            self.publish_anchor(con, company)
            return {"policy": policy, "totals": self.totals(con, company)}

    def require_trial_available(self, con, company, policy, *, attempt_id=None):
        if policy.get("test_authorization_ref"):
            if policy["test_authorization_ref"] != CONTINUOUS_TEST_AUTHORIZATION:
                raise RuntimeScopeError("持续验收授权无法核验。")
            settlements = {s["attempt_id"]: s for s in self.rows(con, company, "settled")}
            for reservation in self.rows(con, company, "reserved"):
                if reservation["attempt_id"] == attempt_id:
                    continue
                settled = settlements.get(reservation["attempt_id"])
                # One unresolved outbound chain at a time; estimates do not require actual billing.
                if not settled:
                    raise RuntimeScopeError("存在未核实的执行占额，停止后续调用并查询原请求。")
                estimate = settled.get("estimated_micro_cny")
                if (type(estimate) is not int or not 0 <= estimate <= reservation["amount_micro_cny"]
                        or settled.get("basis") not in {"VERIFIED_USAGE_AT_APPROVED_PRICE", "NO_EXECUTOR_LAUNCH"}):
                    raise RuntimeScopeError("发现异常费用记录，停止本调用链。")
            return
        reference = policy.get("trial_authorization_ref")
        if not reference:
            return
        if reference != TRIAL_AUTHORIZATION or not 0 < policy.get("budget_micro_cny", 0) <= TRIAL_BUDGET_MICRO_CNY:
            raise RuntimeScopeError("本轮试用授权或预算无法核验。")
        reservations = [r for r in self.rows(con, company, "reserved")
                        if r["grant"].get("trial_authorization_ref") == reference]
        if attempt_id is None and len(reservations) >= 2:
            raise RuntimeScopeError("本轮试用最多两次，已占用次数不会因结算或重新授权恢复。")
        settlements = {s["attempt_id"]: s for s in self.rows(con, company, "settled")}
        for reservation in reservations:
            if reservation["attempt_id"] == attempt_id:
                continue  # The original Task may validate its own persisted permission.
            settled = settlements.get(reservation["attempt_id"])
            if not settled or settled.get("basis") != "NO_EXECUTOR_LAUNCH" or settled.get("estimated_micro_cny") != 0:
                # Current receipts contain estimates, never verified actual payment.
                raise RuntimeScopeError("本轮试用存在执行中或实际费用未知的请求，停止后续调用。")

    def current_grant(self, company, workspace, model_key, *, attempt_id=None, connection=None):
        self.actor(company)
        def read(con):
            if not con.in_transaction:
                con.execute("begin immediate")
            continuity = self.continuity(con, company)
            if continuity["status"] != "VALID" or continuity["needs_reconfirmation"]:
                if continuity["status"] == "FRESH" and not self.latest(con, company):
                    raise RuntimeScopeError("尚未设置公司文字使用许可；请到公司设置明确同意本工作空间的文字外发与预算，原输入会保留。")
                raise RuntimeScopeError("资料状态变化或许可无法核验，旧费用授权已失效；请到公司设置重新核对，原输入会保留。")
            ResourceScopePolicy.resolve_execution_scope(con, tenant_id=TenantContext.current_tenant_id(), company_id=company,
                scope_type="WORKSPACE", scope_ref=workspace)
            policy = self.latest(con, company)
            if not policy or not policy["enabled"] or now() >= datetime.fromisoformat(policy["expires_at"]):
                raise RuntimeScopeError("请到公司设置明确同意本工作空间的文字外发与预算；输入会保留。")
            model = self.model_snapshot(model_key)
            if policy.get("data_scope") != DATA_SCOPE or policy.get("execution_limits") != {"max_input_bytes": MAX_INPUT, "max_output_tokens": MAX_OUTPUT, "reserve_micro_cny": RESERVE_MICRO_CNY}:
                raise RuntimeScopeError("文字外发范围或单次执行上限已变化，请重新确认公司许可。")
            if workspace not in policy["workspace_ids"] or model not in policy["models"]:
                raise RuntimeScopeError("当前工作空间、模型目的地或价格已超出原许可，请重新确认。")
            self.require_trial_available(con, company, policy, attempt_id=attempt_id)
            if attempt_id:
                reserved = next((r for r in self.rows(con, company, "reserved") if r["attempt_id"] == attempt_id), None)
                if reserved is None or reserved["grant"]["policy_revision"] != policy["revision"] or reserved["grant"]["workspace_id"] != workspace or reserved["grant"]["model_key"] != model_key:
                    raise RuntimeScopeError("原请求许可已撤销、变更或未占额。")
                return reserved["grant"]
            return {**({"test_authorization_ref": policy["test_authorization_ref"]} if policy.get("test_authorization_ref") else {}),
                    **({"trial_authorization_ref": policy["trial_authorization_ref"]} if policy.get("trial_authorization_ref") else {}),
                    "tenant_id": TenantContext.current_tenant_id(), "company_id": company, "workspace_id": workspace,
                    "model_key": model_key, "grant_ref": "company-policy-preview:" + policy["revision"],
                    "policy_revision": policy["revision"], "budget_epoch": policy["budget_epoch"], "effective_system_authorization": True,
                    "max_input_bytes": MAX_INPUT, "max_output_tokens": MAX_OUTPUT,
                    "max_cost_cny": float(Decimal(RESERVE_MICRO_CNY) / 1000000), "budget_currency": "CNY",
                    "max_cost_usd": (MAX_INPUT + FRAMING_ALLOWANCE) * PRICE["input_usd_per_million"] / 1000000 + MAX_OUTPUT * PRICE["output_usd_per_million"] / 1000000,
                    "price_version": digest(PRICE), "price_upper_bound_usd_per_input_byte": PRICE["input_usd_per_million"] / 1000000,
                    "price_upper_bound_usd_per_output_token": PRICE["output_usd_per_million"] / 1000000, "destination": model["destination"],
                    "source_class": "PROVIDER_EXECUTOR", "model_name": model["model_name"],
                    "protocol": model["protocol"], "chat_path": model["chat_path"], "price_cny": dict(PRICE)}
        if connection is not None:
            return read(connection)
        with self.db.connect() as con:
            return read(con)

    def reserve(self, con, claim, selection):
        original = selection["grant"]
        grant = self.current_grant(claim["company_id"], claim["context"]["workspace_id"], selection["model"]["model_key"], connection=con)
        if original != grant:
            raise RuntimeScopeError("执行前许可已变化，请重新核对。")
        policy, totals = self.latest(con, claim["company_id"]), self.totals(con, claim["company_id"])
        if not policy.get("test_authorization_ref") and totals["reserved_micro_cny"] + totals["estimated_micro_cny"] + RESERVE_MICRO_CNY > policy["budget_micro_cny"]:
            raise RuntimeScopeError("文字执行预算不足；未知结果仍保留占额，请先查询原请求。")
        grant = {**grant, "grant_ref": "company-text-attempt:" + claim["attempt_id"]}
        value = {"attempt_id": claim["attempt_id"], "grant": grant, "context": claim["context"],
                 "message_id": claim["message_id"], "amount_micro_cny": RESERVE_MICRO_CNY}
        self.events.record_in_connection(con, correlation_id=claim["company_id"], event_type=PREFIX + "reserved", payload=value,
                                        idempotency_key=grant["grant_ref"])
        self.publish_anchor(con, claim["company_id"])
        return grant

    def settle(self, company, attempt_id, task_id, *, launched, status):
        # Unknown metering is retained in full, including after restart; there is no retry release.
        with self.db.connect() as con:
            con.execute("begin immediate")
            continuity = self.continuity(con, company)
            if continuity["status"] != "VALID" or continuity["needs_reconfirmation"]:
                raise RuntimeScopeError("资料状态无法核验，旧执行占额保持未知，不自动结算或恢复许可。")
            reservation = next((r for r in self.rows(con, company, "reserved") if r["attempt_id"] == attempt_id), None)
            if reservation is None or any(s["attempt_id"] == attempt_id for s in self.rows(con, company, "settled")):
                return
            if launched and task_id and status != "COMPLETED":
                outbound = con.execute("select 1 from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type in ('conversation.outbound.claimed','writing.outbound.claimed','cg.outbound.claimed','music.outbound.claimed') "
                    "and json_extract(payload,'$.attempt_id')=? limit 1", (TenantContext.current_tenant_id(), task_id, attempt_id)).fetchone()
                if outbound is None:
                    launched = False
            if not launched:
                estimate = 0
            elif status == "COMPLETED":
                usage = con.execute("select input_tokens,output_tokens from ai_usage_records where tenant_id=? and company_id=? "
                    "and task_id=? and execution_ref=? and execution_status='success'", (TenantContext.current_tenant_id(), company, task_id, attempt_id)).fetchall()
                if len(usage) != 1 or any(type(usage[0][k]) is not int or usage[0][k] < 0 for k in ("input_tokens", "output_tokens")):
                    return
                price = reservation["grant"]["price_cny"]
                estimate = usage[0]["input_tokens"] * price["input_cny_per_million"] + usage[0]["output_tokens"] * price["output_cny_per_million"]
            else:
                return
            self.events.record_in_connection(con, correlation_id=company, event_type=PREFIX + "settled",
                payload={"attempt_id": attempt_id, "estimated_micro_cny": estimate, "currency": "CNY", "actual_paid": None,
                         "basis": "VERIFIED_USAGE_AT_APPROVED_PRICE" if launched else "NO_EXECUTOR_LAUNCH", "price_version": reservation["grant"]["price_version"]},
                idempotency_key="company-text-settled:" + attempt_id)
            self.publish_anchor(con, company)
