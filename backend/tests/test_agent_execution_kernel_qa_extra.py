"""Issue A · 独立 QA 补充用例（严过关 / software-qa-engineer）。

对实现者自测套件的盲区做针对性独立验证（不改动其原文件，仅修正其中一处
错误红线守卫，见 test_agent_execution_kernel.py::test_no_budget_guard_module）：

1. 指纹去噪的「真·规范化」：不同键序 / dict vs RunConfig 同义 → 同一指纹。
   守卫 ``json.dumps(sort_keys=True)``，防止回归导致非确定性指纹
   （会让 ``recover`` 误判 ``session_config_mismatch``）。
2. Secret 脱敏深度：嵌套 dict 与 list 内的 secret 键亦被 ``"<redacted>"``
   替换、且真实值不进哈希（实现者仅测过顶层 ``api_key``）。
3. ``a.kernel.*`` 事件端到端脱敏：``enabled=True`` 跑通后，所有内核事件
   payload 仅含白名单键（scope/status/fingerprint/round/error_code），
   绝不含 path/key/secret/token/password/param/instruction 等。

纯离线（unittest + temp sqlite），不触真实 DB / 网络 / L2。
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.real_rd_executor import RealRDExecutor
from app.run_config_fingerprint import (
    RunConfig,
    compute_fingerprint,
    normalize_run_config,
)


TARGET = "tools/real_rd_fixture/target_a.py"
VALID_DIFF_OK = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -1,2 +1,2 @@\n"
    " ALPHA = 1\n"
    "-BETA = 2\n"
    "+BETA = 3\n"
)


class _FakeModel:
    def __init__(self, scripted):
        self._scripted = list(scripted)
        self.calls = 0
        self.model_gateway_id = "fake-gateway"
        self.model_name = "fake-model"

    def execute(self, prompt):
        self.calls += 1
        if not self._scripted:
            raise RuntimeError("no scripted response")
        return dict(self._scripted.pop(0))


class _FakeToolset:
    def __init__(self, scope, event_log, command_registry=None, *, sandbox_mode=None):
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}
        self.sandbox_mode = sandbox_mode

    def read_file(self, raw):
        return {"output": {
            "sha256": "pre-hash-abc",
            "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
            "ends_with_newline": True,
        }}

    def _apply_diff_transactional(self, raw):
        return ({"output": {"files": [
            {"path": TARGET, "preimage_hash": "pre-hash-abc",
             "postimage_hash": "post-hash-xyz"}
        ]}}, None)

    def run_test(self, raw):
        return {"output": {"exit_code": 0}}

    def git_read(self, raw):
        return {"output": {"output": VALID_DIFF_OK}}


def _make_event_log():
    tmp = tempfile.mkdtemp(prefix="aek-qa-")
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


class QaFingerprintFormTest(unittest.TestCase):
    def test_fingerprint_order_and_form_invariant(self) -> None:
        """同义配置（不同键序 / dict vs RunConfig）→ 同一指纹。

        守卫 ``json.dumps(sort_keys=True)`` 的规范化，防止回归导致
        非确定性指纹（会让 ``recover`` 误判 ``session_config_mismatch``）。
        """
        dict_cfg = {
            "model_gateway_id": "anthropic",
            "model_name": "claude",
            "tool_scope": {"allow_paths": ["x"], "sandbox_mode": "git"},
            "prompt_spec": {"instructions": "do it"},
            "strategy": {"max_rounds": 3},
            "component_versions": {},
        }
        # 键序打乱的等价 dict（含 list 内元素顺序无关）。
        shuffled = {
            "strategy": {"max_rounds": 3},
            "component_versions": {},
            "model_name": "claude",
            "model_gateway_id": "anthropic",
            "prompt_spec": {"instructions": "do it"},
            "tool_scope": {"sandbox_mode": "git", "allow_paths": ["x"]},
        }
        rc = RunConfig(
            model_gateway_id="anthropic",
            model_name="claude",
            tool_scope={"sandbox_mode": "git", "allow_paths": ["x"]},
            prompt_spec={"instructions": "do it"},
            strategy={"max_rounds": 3},
            component_versions={},
        )
        fp_dict = compute_fingerprint(dict_cfg)
        fp_shuffled = compute_fingerprint(shuffled)
        fp_rc = compute_fingerprint(rc)
        self.assertEqual(fp_dict, fp_shuffled)
        self.assertEqual(fp_dict, fp_rc)
        self.assertTrue(fp_dict.startswith("sha256:"))


class QaSecretRedactionTest(unittest.TestCase):
    def test_secret_redacted_nested_and_in_list(self) -> None:
        """嵌套 dict 与 list 内的 secret 键亦被脱敏且真实值不进哈希。

        实现者仅测过顶层 ``api_key``；此处补嵌套 / 列表深度用例。
        """
        cfg = {
            "model_gateway_id": "x",
            "credentials": {
                "api_key": "sk-top-secret",
                "nested": {"token": "tok-nested"},
            },
            "endpoints": [
                {"url": "https://a", "password": "pw-1"},
                {"url": "https://b", "password": "pw-2"},
            ],
        }
        fp = compute_fingerprint(cfg)
        norm = json.dumps(normalize_run_config(cfg), sort_keys=True)
        # 脱敏：所有 secret 值被占位符替换。
        self.assertIn("<redacted>", norm)
        # 真实秘密绝不出现在归一化 JSON 或指纹中。
        for leak in ("sk-top-secret", "tok-nested", "pw-1", "pw-2"):
            self.assertNotIn(leak, norm)
            self.assertNotIn(leak, fp)
        # 改变真实 secret 值 → 指纹不变（不计入哈希）。
        cfg2 = json.loads(json.dumps(cfg))
        cfg2["credentials"]["api_key"] = "sk-different"
        cfg2["endpoints"][0]["password"] = "pw-999"
        self.assertEqual(fp, compute_fingerprint(cfg2))


class QaKernelEventDesensitizationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.event_log, self.db = _make_event_log()

    def _spec(self):
        return {
            "issue_id": "aek-qa-desens",
            "target_files": [TARGET],
            "test_command_id": "rd_verify",
            "test_command_argv": ["pytest", "tests/test_real_rd_verify.py"],
            "instructions": "Change BETA to 3. SECRET_INSTRUCTION",
            "max_rounds": 3,
            "allow_paths": [TARGET, "backend/tests/test_real_rd_verify.py"],
        }

    def test_kernel_event_payload_whitelisted(self) -> None:
        """enabled=True 跑通后，所有 ``a.kernel.*`` 事件 payload 仅含白名单键，
        绝不含 path / key / secret / token / password / param / instruction。

        亦验证 spec 中的敏感文案（instructions 含 SECRET_*) 不泄漏进内核事件。
        """
        model = _FakeModel([{
            "status": "success", "output": VALID_DIFF_OK,
            "total_tokens": 12, "estimated_cost": 0.0,
            "model_gateway_id": "fake-gateway",
            "model_name": "fake-model",
        }])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=_FakeToolset,
            agent_kernel_enabled=True,
        )
        result = executor.run(self._spec())
        self.assertEqual(result["status"], "succeeded")

        events = [e for e in self.event_log.get_all()
                  if e["event_type"].startswith("a.kernel.")]
        self.assertGreater(len(events), 0)
        _ALLOWED = {
            "scope", "status", "fingerprint", "round", "error_code",
        }
        _FORBIDDEN = {
            "path", "file_path", "abs_path", "key", "secret", "token",
            "password", "param", "instruction", "instructions", "api_key",
            "allow_paths", "target_files", "test_command_argv",
        }
        for e in events:
            payload = e["payload"]
            if not isinstance(payload, dict):
                continue
            for k in payload.keys():
                self.assertIn(
                    k, _ALLOWED,
                    f"a.kernel 事件 {e['event_type']} 含白名单外键 {k!r}",
                )
            rendered = json.dumps(payload).lower()
            for bad in _FORBIDDEN:
                self.assertNotIn(bad, rendered)


if __name__ == "__main__":
    unittest.main()
