"""Issue A · P0-4 恢复异常测试套件（纯离线 unittest + temp sqlite）。

覆盖 §8 全部异常用例：
1. 断点恢复（recover 同指纹 → recovered；指纹变化 → session_config_mismatch）。
2. 锁丢失（force_release 清孤儿后新 owner 可重领）。
3. 重复执行（acquire 同 (scope,owner,token) 幂等返回既有 claim_id）。
4. 指纹变化（两 config 不同 → 不同 fingerprint；Secret 真实值不进哈希）。
5. 会话过期（running 且过期 → reap_expired → expired）。
6. 终止释放（release 后 scope 释放，新 owner 可重领）。
7. Wake 合并（同 idempotency_key 仍 pending → coalesced_count+1）。
8. Secret 不进指纹 / 日志（归一化 JSON 仅含 "<redacted>"）。
9. 非 Git 降级边界（session 以 error_code="workspace_not_git" 收尾 + claim 释放）。

并断言：
- ``governance.LOCKED_ACTIONS`` 长度与内容不变。
- 不引入 ``budget_guard`` 模块。
- 内核新文件不 import / 不调用 ``auto_modify_code`` / ``lift_human_approval_gate``。
- 内核新文件不新增 FastAPI 路由（不 import app.main / 不定义 APIRouter）。
- real_rd_executor 既有 8 passed 零回归（default-off 路径）。

纯离线：仅 unittest + temp sqlite，不触真实 DB / 网络 / L2 写链路。
"""

from __future__ import annotations

import importlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

from app.agent_execution_kernel import ExecutionClaimError, ExecutionClaimStore
from app.agent_wakeup_session import (
    AgentTaskSessionError,
    AgentTaskSessionStore,
    WakeRequestError,
    WakeRequestStore,
)
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.governance import CompanyGovernance
from app.run_config_fingerprint import (
    RunConfig,
    build_idempotency_key,
    compute_fingerprint,
    config_changed,
    normalize_run_config,
)
from app.real_rd_executor import RealRDExecutor, RealRDExecutorError

_APP_DIR = Path(__file__).resolve().parents[1] / "app"
_KERNEL_FILES = [
    _APP_DIR / "run_config_fingerprint.py",
    _APP_DIR / "agent_execution_kernel.py",
    _APP_DIR / "agent_wakeup_session.py",
]

# 与 test_real_rd_executor.py 同款 fixture。
TARGET = "tools/real_rd_fixture/target_a.py"
VALID_DIFF_OK = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -1,2 +1,2 @@\n"
    " ALPHA = 1\n"
    "-BETA = 2\n"
    "+BETA = 3\n"
)


# ---------------------------------------------------------------------------
# 指纹（P0-3）
# ---------------------------------------------------------------------------
class FingerprintTest(unittest.TestCase):
    def test_compute_fingerprint_stable(self) -> None:
        cfg = {
            "model_gateway_id": "anthropic",
            "model_name": "claude-sonnet-4-20250514",
            "tool_scope": {"sandbox_mode": "git", "allow_paths": ["x"]},
            "prompt_spec": {"instructions": "do it"},
            "strategy": {"max_rounds": 3},
            "component_versions": {},
        }
        self.assertEqual(compute_fingerprint(cfg), compute_fingerprint(dict(cfg)))
        self.assertTrue(compute_fingerprint(cfg).startswith("sha256:"))

    def test_config_changed(self) -> None:
        a = compute_fingerprint({"model_name": "a"})
        b = compute_fingerprint({"model_name": "b"})
        self.assertTrue(config_changed(a, b))
        self.assertFalse(config_changed(a, a))

    def test_normalize_drops_noise(self) -> None:
        cfg = {
            "model_gateway_id": "x",
            "timestamp": "2026-07-20T00:00:00+00:00",
            "request_id": "r1",
            "run_id": "run9",
            "nonce": "abc",
            "path": "/tmp/x",
            "created_at": "2026-01-01",
            "ok": 1,
            "empty": "",
            "nothing": None,
        }
        norm = normalize_run_config(cfg)
        for noise in ("timestamp", "request_id", "run_id", "nonce", "path", "created_at", "empty", "nothing"):
            self.assertNotIn(noise, norm)
        self.assertEqual(norm["model_gateway_id"], "x")
        self.assertEqual(norm["ok"], 1)

    def test_secret_redacted_and_not_in_hash(self) -> None:
        cfg1 = {"model_gateway_id": "x", "api_key": "sk-secret-1"}
        cfg2 = {"model_gateway_id": "x", "api_key": "sk-secret-2"}
        fp1 = compute_fingerprint(cfg1)
        fp2 = compute_fingerprint(cfg2)
        # 真实 Secret 不进入哈希 → 两指纹相同。
        self.assertEqual(fp1, fp2)
        norm1 = normalize_run_config(cfg1)
        rendered = json.dumps(norm1)
        self.assertIn("<redacted>", rendered)
        self.assertNotIn("sk-secret-1", rendered)
        self.assertNotIn("sk-secret-1", fp1)
        self.assertNotIn("sk-secret-2", fp2)

    def test_runconfig_path(self) -> None:
        rc = RunConfig(
            model_gateway_id="anthropic",
            model_name="claude",
            tool_scope={},
            prompt_spec={},
            strategy={},
            component_versions={},
        )
        fp = compute_fingerprint(rc)
        self.assertTrue(fp.startswith("sha256:"))

    def test_build_idempotency_key(self) -> None:
        key = build_idempotency_key("Scope-A", "TASK1", "sha256:abc")
        self.assertEqual(key, "scope-a:task1:sha256:abc")
        # 空 part 跳过。
        self.assertEqual(
            build_idempotency_key("A", "", None, "B"), "a:b"
        )


# ---------------------------------------------------------------------------
# ExecutionClaim（P0-1）
# ---------------------------------------------------------------------------
def _make_claim_store() -> ExecutionClaimStore:
    tmp = tempfile.mkdtemp(prefix="aek-claim-")
    db = Database(os.path.join(tmp, "curis.sqlite"))
    return ExecutionClaimStore(db)


class ExecutionClaimTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = _make_claim_store()
        self.scope = "tenant:t1:real-rd:run-1"

    def test_acquire_idempotent_same_owner_token(self) -> None:
        c1 = self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        c2 = self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        self.assertEqual(c1.claim_id, c2.claim_id)
        self.assertEqual(c1.status, "held")

    def test_acquire_other_owner_held_raises(self) -> None:
        self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        with self.assertRaises(ExecutionClaimError) as ctx:
            self.store.acquire(self.scope, "owner-b", "reason", token="tok-2")
        self.assertEqual(ctx.exception.failure_code, "claim_already_held")

    def test_acquire_same_owner_wrong_token_raises(self) -> None:
        self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        with self.assertRaises(ExecutionClaimError) as ctx:
            self.store.acquire(self.scope, "owner-a", "reason", token="tok-X")
        self.assertEqual(ctx.exception.failure_code, "claim_token_mismatch")

    def test_release_wrong_token_raises(self) -> None:
        claim = self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        with self.assertRaises(ExecutionClaimError) as ctx:
            self.store.release(claim.claim_id, "wrong")
        self.assertEqual(ctx.exception.failure_code, "claim_token_mismatch")

    def test_release_then_scope_free(self) -> None:
        claim = self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        released = self.store.release(claim.claim_id, "tok-1")
        self.assertEqual(released.status, "released")
        self.assertFalse(self.store.is_held(self.scope))
        # 释放后他 owner 可重领（不双执行）。
        c2 = self.store.acquire(self.scope, "owner-b", "reason", token="tok-2")
        self.assertEqual(c2.status, "held")

    def test_force_release_clears_orphan(self) -> None:
        claim = self.store.acquire(self.scope, "owner-a", "reason", token="tok-1")
        freed = self.store.force_release(claim.claim_id)
        self.assertEqual(freed.status, "force_released")
        self.assertFalse(self.store.is_held(self.scope))
        c2 = self.store.acquire(self.scope, "owner-b", "reason", token="tok-2")
        self.assertEqual(c2.status, "held")

    def test_heartbeat_and_renew(self) -> None:
        claim = self.store.acquire(
            self.scope, "owner-a", "reason", token="tok-1", ttl_seconds=100
        )
        hb = self.store.heartbeat(claim.claim_id, "tok-1")
        renewed = self.store.renew(claim.claim_id, "tok-1", ttl_seconds=200)
        self.assertEqual(hb.status, "held")
        self.assertEqual(renewed.status, "held")
        self.assertNotEqual(renewed.expires_at, claim.expires_at)

    def test_reap_expired(self) -> None:
        # 制造一个已过期（TTL 为负）的 held 锁。
        self.store.acquire(
            self.scope, "owner-a", "reason", token="tok-1", ttl_seconds=-10
        )
        self.assertFalse(self.store.is_held(self.scope))
        self.assertEqual(self.store.reap_expired(), 1)
        self.assertEqual(self.store.list_active(scope=self.scope), [])


# ---------------------------------------------------------------------------
# Wake / Session（P0-2）
# ---------------------------------------------------------------------------
def _make_stores():
    tmp = tempfile.mkdtemp(prefix="aek-ws-")
    db = Database(os.path.join(tmp, "curis.sqlite"))
    return WakeRequestStore(db), AgentTaskSessionStore(db), db


class WakeSessionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wake, self.session, self.db = _make_stores()
        self.scope = "tenant:t1:real-rd:run-2"
        self.fp = "sha256:abc"

    def test_wake_coalesce(self) -> None:
        key = "scope:task:sha256:abc"
        w1 = self.wake.create(
            self.scope, "agent", "task", idempotency_key=key,
            payload={}, config_fingerprint=self.fp,
        )
        w2 = self.wake.create(
            self.scope, "agent", "task", idempotency_key=key,
            payload={}, config_fingerprint=self.fp,
        )
        self.assertEqual(w1.request_id, w2.request_id)
        self.assertEqual(w2.coalesced_count, 2)
        self.assertEqual(w2.status, "pending")

    def test_wake_claim_idempotent_same_session(self) -> None:
        w = self.wake.create(
            self.scope, "agent", "task", idempotency_key="k1",
            payload={}, config_fingerprint=self.fp,
        )
        c1 = self.wake.claim(w.request_id, "sess-1")
        c2 = self.wake.claim(w.request_id, "sess-1")
        self.assertEqual(c1.request_id, c2.request_id)
        self.assertEqual(c1.claimed_by, "sess-1")

    def test_wake_claim_other_session_raises(self) -> None:
        w = self.wake.create(
            self.scope, "agent", "task", idempotency_key="k2",
            payload={}, config_fingerprint=self.fp,
        )
        self.wake.claim(w.request_id, "sess-1")
        with self.assertRaises(WakeRequestError) as ctx:
            self.wake.claim(w.request_id, "sess-2")
        self.assertEqual(ctx.exception.failure_code, "wake_already_claimed")

    def test_session_lifecycle(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a",
        )
        self.assertEqual(sess.status, "pending")
        started = self.session.start(sess.session_id, "owner-a")
        self.assertEqual(started.status, "running")
        cp = self.session.checkpoint(sess.session_id, "owner-a", {"round": 1})
        self.assertIn("round", json.loads(cp.checkpoint))
        done = self.session.complete(
            sess.session_id, "owner-a", outcome="completed"
        )
        self.assertEqual(done.status, "completed")

    def test_session_owner_mismatch_raises(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a",
        )
        with self.assertRaises(AgentTaskSessionError) as ctx:
            self.session.checkpoint(sess.session_id, "owner-b", {"x": 1})
        self.assertEqual(ctx.exception.failure_code, "session_owner_mismatch")

    def test_session_recover_same_fingerprint(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a", checkpoint={"round": 3},
        )
        self.session.start(sess.session_id, "owner-a")
        recovered = self.session.recover(
            sess.session_id, "owner-b",
            checkpoint={"_config_fingerprint": self.fp, "round": 3},
        )
        self.assertEqual(recovered.status, "recovered")
        self.assertEqual(recovered.parent_session_id, sess.session_id)
        self.assertEqual(recovered.config_fingerprint, self.fp)
        # recover 产出的新会话可由 start 翻为 running。
        running = self.session.start(recovered.session_id, "owner-b")
        self.assertEqual(running.status, "running")

    def test_session_recover_config_mismatch(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a",
        )
        with self.assertRaises(AgentTaskSessionError) as ctx:
            self.session.recover(
                sess.session_id, "owner-b",
                checkpoint={"_config_fingerprint": "sha256:different"},
            )
        self.assertEqual(ctx.exception.failure_code, "session_config_mismatch")

    def test_session_expiry_reap(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a", ttl_seconds=-10,
        )
        self.session.start(sess.session_id, "owner-a")
        self.assertEqual(self.session.reap_expired(), 1)
        got = self.session.get(sess.session_id)
        self.assertEqual(got.status, "expired")

    def test_session_replay(self) -> None:
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id="claim-1", wake_request_id="wake-1",
            owner="owner-a", checkpoint={"round": 2},
        )
        replay = self.session.replay(sess.session_id)
        self.assertEqual(replay["config_fingerprint"], self.fp)
        self.assertEqual(replay["checkpoint"], {"round": 2})

    def test_non_git_degradation_boundary(self) -> None:
        """非 Git 工作区降级边界：session 以 error_code 收尾 + claim 释放。

        内核层仅做「错误码记录 + 释放」，真实 non-git 判定继续留给
        LocalRDToolset（既有测试复用，不重写）。
        """
        claim = ExecutionClaimStore(self.db).acquire(
            self.scope, "owner-a", "real_rd.run", token="tok-1"
        )
        sess = self.session.create(
            self.scope, "agent", "task",
            config_fingerprint=self.fp,
            execution_claim_id=claim.claim_id, wake_request_id="wake-1",
            owner="owner-a",
        )
        self.session.start(sess.session_id, "owner-a")
        done = self.session.complete(
            sess.session_id, "owner-a",
            outcome="failed", error_code="workspace_not_git",
        )
        self.assertEqual(done.status, "failed")
        self.assertEqual(done.error_code, "workspace_not_git")
        released = ExecutionClaimStore(self.db).release(
            claim.claim_id, "tok-1"
        )
        self.assertEqual(released.status, "released")

    def test_wake_reap_expired(self) -> None:
        w = self.wake.create(
            self.scope, "agent", "task", idempotency_key="kx",
            payload={}, config_fingerprint=self.fp, ttl_seconds=-10,
        )
        self.assertEqual(self.wake.reap_expired(), 1)
        got = self.wake.get(w.request_id)
        self.assertEqual(got.status, "cancelled")


# ---------------------------------------------------------------------------
# real_rd_executor 接线（T-A4，default-off + enabled 冒烟）
# ---------------------------------------------------------------------------
class _FakeModel:
    def __init__(self, scripted: list[dict[str, Any]]) -> None:
        self._scripted = list(scripted)
        self.calls = 0
        self.model_gateway_id = "fake-gateway"
        self.model_name = "fake-model"
        self.mutates_filesystem = False

    def execute(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        if not self._scripted:
            raise RuntimeError("no scripted model response")
        return dict(self._scripted.pop(0))


class _FakeToolset:
    def __init__(self, scope, event_log, command_registry=None, *, sandbox_mode=None):
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}
        self.sandbox_mode = sandbox_mode

    def read_file(self, raw: str) -> dict[str, Any]:
        return {"output": {
            "sha256": "pre-hash-abc",
            "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
            "ends_with_newline": True,
        }}

    def _apply_diff_transactional(self, raw: str):
        return ({"output": {"files": [
            {"path": TARGET, "preimage_hash": "pre-hash-abc", "postimage_hash": "post-hash-xyz"}
        ]}}, None)

    def run_test(self, raw: str) -> dict[str, Any]:
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict[str, Any]:
        return {"output": {"output": VALID_DIFF_OK}}


class _FailingToolset(_FakeToolset):
    """构造即失败的 toolset：触发 _build_toolsets 的 configuration_rejected
    致命分支（内核已建立 claim 后 fail-open 释放）。"""

    def __init__(self, scope, event_log, command_registry=None, *, sandbox_mode=None):
        raise ValueError("toolset construction rejected")


def _make_event_log():
    tmp = tempfile.mkdtemp(prefix="aek-rd-")
    db = Database(os.path.join(tmp, "evo.sqlite"))
    with db.connect() as conn:
        conn.execute(
            """
            create table if not exists evolution_events (
                event_id integer primary key autoincrement,
                correlation_id text not null,
                event_type text not null,
                payload text not null,
                tenant_id text,
                idempotency_key text,
                created_at text not null default current_timestamp
            )
            """
        )
    return EvolutionEventLog(db), db


class RealRDWiringTest(unittest.TestCase):
    def setUp(self) -> None:
        self.event_log, self.db = _make_event_log()

    def _spec(self, issue_id="aek-qa-1"):
        return {
            "issue_id": issue_id,
            "target_files": [TARGET],
            "test_command_id": "rd_verify",
            "test_command_argv": ["pytest", "tests/test_real_rd_verify.py"],
            "instructions": "Change BETA to 3.",
            "max_rounds": 3,
            "allow_paths": [TARGET, "backend/tests/test_real_rd_verify.py"],
        }

    def test_run_default_off_no_kernel_tables(self) -> None:
        """default-off：既不建内核表、也不落 a.kernel.* 事件（零回归）。"""
        model = _FakeModel([{"status": "success", "output": VALID_DIFF_OK,
                             "total_tokens": 12, "estimated_cost": 0.0,
                             "model_gateway_id": "fake-gateway",
                             "model_name": "fake-model"}])
        executor = RealRDExecutor(model, self.event_log, toolset_cls=_FakeToolset)
        result = executor.run(self._spec())
        self.assertEqual(result["status"], "succeeded")
        with self.db.connect() as conn:
            # 内核表不应被创建（default-off）。
            tables = [r[0] for r in conn.execute(
                "select name from sqlite_master where type='table'"
            ).fetchall()]
        self.assertNotIn("agent_execution_claims", tables)
        self.assertNotIn("agent_wakeup_requests", tables)
        self.assertNotIn("agent_task_sessions", tables)
        event_types = [e["event_type"] for e in self.event_log.get_all()]
        self.assertFalse(any(t.startswith("a.kernel.") for t in event_types))

    def test_run_kernel_enabled_creates_records_and_events(self) -> None:
        """enabled=True：建 wake→claim→session，收尾落 a.kernel.* 事件。"""
        model = _FakeModel([{"status": "success", "output": VALID_DIFF_OK,
                             "total_tokens": 12, "estimated_cost": 0.0,
                             "model_gateway_id": "fake-gateway",
                             "model_name": "fake-model"}])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=_FakeToolset,
            agent_kernel_enabled=True,
        )
        result = executor.run(self._spec())
        self.assertEqual(result["status"], "succeeded")

        with self.db.connect() as conn:
            claims = conn.execute(
                "select status from agent_execution_claims"
            ).fetchall()
            sessions = conn.execute(
                "select status from agent_task_sessions"
            ).fetchall()
            wakes = conn.execute(
                "select status from agent_wakeup_requests"
            ).fetchall()
        self.assertEqual([c[0] for c in claims], ["released"])
        self.assertEqual([s[0] for s in sessions], ["completed"])
        self.assertEqual([w[0] for w in wakes], ["completed"])

        event_types = [e["event_type"] for e in self.event_log.get_all()]
        for expected in (
            "a.kernel.wake.created",
            "a.kernel.claim.acquired",
            "a.kernel.session.started",
            "a.kernel.session.checkpoint",
            "a.kernel.session.completed",
            "a.kernel.claim.released",
            "a.kernel.wake.completed",
        ):
            self.assertIn(expected, event_types)

    def test_termination_release_on_exception(self) -> None:
        """异常终止：内核 fail-open 仍应释放 claim（abort 兜底清孤儿）。

        保持合法 ``test_command_argv``（使 ``_kernel_begin`` 成功建立
        claim），但令 toolset 构造失败 → ``_build_toolsets`` 抛
        ``ValueError`` → 被捕获为脱敏 ``RealRDExecutorError(
        configuration_rejected)``；内核在异常传播前调用 ``_kernel_abort``
        释放 claim / 收尾 wake+session。
        """
        model = _FakeModel([{
            "status": "success", "output": VALID_DIFF_OK,
            "total_tokens": 1, "estimated_cost": 0.0,
            "model_gateway_id": "fake-gateway", "model_name": "fake-model",
        }])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=_FailingToolset,
            agent_kernel_enabled=True,
        )
        spec = self._spec(issue_id="aek-qa-fail")
        with self.assertRaises(RealRDExecutorError):
            executor.run(spec)
        # 内核应已释放 scope（abort 内 release / force_release 兜底清孤儿）。
        claim_store = ExecutionClaimStore(self.db)
        self.assertFalse(
            claim_store.is_held("real-rd-tenant:real-rd:aek-qa-fail")
        )


# ---------------------------------------------------------------------------
# 红线守卫（不触 L2 / 不解除 LOCKED_ACTIONS / 无新路由）
# ---------------------------------------------------------------------------
class RedLineGuardTest(unittest.TestCase):
    def test_locked_actions_unchanged(self) -> None:
        self.assertEqual(
            CompanyGovernance.LOCKED_ACTIONS,
            ["lift_human_approval_gate", "auto_modify_code"],
        )

    def test_no_budget_guard_module(self) -> None:
        """Issue A 内核不引入 ``budget_guard``（与 Issue C 既有预算护栏独立）。

        注意：``app.budget_guard`` 是 Issue C 的既有模块（default-off），
        真实存在且可导入；不可依赖「模块不存在」来判定红线。
        正确做法：扫描内核三个新文件，断言不含 ``budget_guard`` 引用，
        从而验证 Issue A（T-A1~T-A4）未引入该依赖。
        """
        for path in _KERNEL_FILES:
            content = path.read_text(encoding="utf-8").lower()
            self.assertNotIn(
                "budget_guard",
                content,
                f"{path.name} 不应引入 budget_guard（Issue A 红线）",
            )

    def test_no_locked_action_references_in_kernel(self) -> None:
        for path in _KERNEL_FILES:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("auto_modify_code", content)
            self.assertNotIn("lift_human_approval_gate", content)

    def test_no_new_api_routes_in_kernel(self) -> None:
        for path in _KERNEL_FILES:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("APIRouter", content)
            self.assertNotIn("from app.main", content)
            self.assertNotIn("@app.", content)
            self.assertNotIn("FastAPI", content)

    def test_no_l2_logic_in_kernel(self) -> None:
        """内核不触碰 L2 冻结域：Marketplace / 真实计费 / 多租户 / Employee CRUD。

        扫描内核三个新文件，断言不含 L2 领域模块 / 函数引用（``tenant_id`` 等
        单租户 selfuse 字段属正常范围，不在此禁止集）。
        """
        _L2_MARKERS = (
            "marketplace",
            "billing_store",
            "usage_meter",
            "manage_employees",
            "connect_platform",
            "roi_schema",
            "employee_crud",
            "budget_guard",
        )
        for path in _KERNEL_FILES:
            content = path.read_text(encoding="utf-8").lower()
            for marker in _L2_MARKERS:
                self.assertNotIn(
                    marker,
                    content,
                    f"{path.name} 不应引入 L2 逻辑标记 {marker!r}",
                )


if __name__ == "__main__":
    unittest.main()
