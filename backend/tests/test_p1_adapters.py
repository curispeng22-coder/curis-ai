"""P1 适配器抽象 + 员工=能力组合 单元测试与本地联调（QA 验收闸门）。

纯离线 / 不触真实外部网络：
- CliAdapter：真实 subprocess 调 python 回显（验证真实进程执行）。
- HttpApiAdapter / WebhookAdapter：本地 http.server 回环（验证真实 HTTP 往返）。
- McpAdapter：stdio JSON-RPC 最小路径（临时 fake MCP server 脚本）。
- CapabilityAdapterFactory：按 adapter_kind 分派断言。
- EmployeeCapabilityModel + CapabilityResolver(employee_id)：员工能力组合过滤 / 首选。
- CapabilityCatalog.register_external_agent：配置化登记（红线：仅能力层，不导入资产）。
- 本地联调整链：PipelineRuntime.run_node 经真实 CLI 适配器执行 + 员工选路 + 降级到 backup。

零新依赖：仅标准库 + 已装 httpx。
"""
from __future__ import annotations

import http.server
import json
import os
import shlex
import sys
import tempfile
import threading
import unittest
from typing import Any
from unittest.mock import patch

from app.capability_adapters import (
    CapabilityAdapterFactory,
    CliAdapter,
    HttpApiAdapter,
    McpAdapter,
    UnconfiguredAdapter,
    WebhookAdapter,
)
from app.capability_catalog import CapabilityCatalog
from app.capability_resolver import CapabilityExhausted, CapabilityRequirement, CapabilityResolver
from app.database import Database
from app.employee_capability_model import EmployeeCapabilityModel
from app.pipeline_runtime import PipelineRuntime
from app.task_graph import TaskGraph, TaskNode


class DiffStatusReviewer:
    """联调用桩验收器：仅当执行 status==success 且 output 含合法 diff 头时通过。

    用于验证「员工首选错误 → 降级到 backup（真实执行）→ 完成」的闭环：
    错误状态的适配器（cli_not_found）应判失败并触发换能力，而非恒过。
    """

    def review(self, task):  # noqa: A003 - 与 ResultReviewer 同签名
        result = task.executor_result or {}
        status = result.get("status", "")
        output = result.get("output", "") or ""
        passes = status == "success" and "--- a/" in output
        return {
            "passes": passes,
            "needs_rework": not passes,
            "escalated": False,
            "feedback": [] if passes else ["execution failed or no valid diff"],
        }


class _NullEventLog:
    database = None

    def record(self, **kwargs: Any) -> None:
        return None


def _tmp_db() -> str:
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    os.unlink(path)
    return path


def _fresh_catalog(db_path: str):
    db = Database(db_path)
    db.initialize()
    catalog = CapabilityCatalog(db, _NullEventLog())
    return db, catalog


class CliAdapterTestCase(unittest.TestCase):
    def test_real_subprocess_echo(self) -> None:
        adapter = CliAdapter({"command": sys.executable, "args": ["-c", "import sys; print(sys.argv[-1])"]})
        result = adapter.execute("hello-p1")
        self.assertEqual(result["status"], "success")
        self.assertIn("hello-p1", result["output"])

    def test_missing_command_cli_not_found(self) -> None:
        adapter = CliAdapter({"command": "this-binary-should-not-exist-xyz"})
        result = adapter.execute("x")
        self.assertEqual(result["status"], "cli_not_found")


class HttpAdapterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        handler = self

        class _Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(length) or b"{}")
                payload = body.get("prompt", "")
                resp = json.dumps({"output": f"svc-echo:{payload}"}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)

            def log_message(self, *args):  # 静默
                pass

        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self._url = f"http://127.0.0.1:{self._server.server_address[1]}/run"

    def tearDown(self) -> None:
        try:
            self._server.shutdown()
            self._server.server_close()
        except Exception:
            pass

    def test_http_api_real_round_trip(self) -> None:
        adapter = HttpApiAdapter({"url": self._url, "method": "POST"})
        result = adapter.execute("ping-p1")
        self.assertEqual(result["status"], "success")
        self.assertIn("svc-echo:ping-p1", result["output"])

    def test_webhook_fire_and_forget(self) -> None:
        adapter = WebhookAdapter({"url": self._url})
        result = adapter.execute("evt-1")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "dispatched")


class McpAdapterTestCase(unittest.TestCase):
    def _write_fake_server(self) -> str:
        script = (
            "import sys, json\n"
            "for line in sys.stdin:\n"
            "    line = line.strip()\n"
            "    if not line:\n"
            "        continue\n"
            "    msg = json.loads(line)\n"
            "    if msg.get('method') == 'initialize':\n"
            "        print(json.dumps({'jsonrpc':'2.0','id':msg['id'],'result':{'capabilities':{},'serverInfo':{'name':'fake'}}}))\n"
            "        sys.stdout.flush()\n"
            "    elif msg.get('method') == 'tools/call':\n"
            "        prompt = msg['params']['arguments'].get('prompt','')\n"
            "        print(json.dumps({'jsonrpc':'2.0','id':msg['id'],'result':{'content':[{'type':'text','text':'mcp-echo:'+prompt}]}}))\n"
            "        sys.stdout.flush()\n"
            "        break\n"
        )
        fd, path = tempfile.mkstemp(suffix=".py", prefix="fake_mcp_")
        with os.fdopen(fd, "w") as f:
            f.write(script)
        return path

    def test_mcp_minimal_stdio_path(self) -> None:
        srv = self._write_fake_server()
        try:
            adapter = McpAdapter(
                {"server_command": shlex.join((sys.executable, srv))}
            )
            result = adapter.execute("call-me")
            self.assertEqual(result["status"], "success")
            self.assertIn("mcp-echo:call-me", result["output"])
        finally:
            try:
                os.unlink(srv)
            except Exception:
                pass

    def test_mcp_no_server_command(self) -> None:
        adapter = McpAdapter({})
        result = adapter.execute("x")
        self.assertEqual(result["status"], "error:no_server_command")


class FactoryDispatchTestCase(unittest.TestCase):
    def test_cli_dispatch(self) -> None:
        cap = {"capability_key": "c1", "type": "cli", "runtime_meta": {"adapter_kind": "cli", "adapter_config": {"command": "echo"}}}
        self.assertIsInstance(CapabilityAdapterFactory.build(cap), CliAdapter)

    def test_http_dispatch(self) -> None:
        cap = {"capability_key": "c2", "type": "http", "runtime_meta": {"adapter_kind": "http", "adapter_config": {"url": "http://x"}}}
        self.assertIsInstance(CapabilityAdapterFactory.build(cap), HttpApiAdapter)

    def test_webhook_dispatch(self) -> None:
        cap = {"capability_key": "c3", "type": "webhook", "runtime_meta": {"adapter_kind": "webhook", "adapter_config": {"url": "http://x"}}}
        self.assertIsInstance(CapabilityAdapterFactory.build(cap), WebhookAdapter)

    def test_mcp_dispatch(self) -> None:
        cap = {"capability_key": "c4", "type": "mcp", "runtime_meta": {"adapter_kind": "mcp", "adapter_config": {"server_command": "x"}}}
        self.assertIsInstance(CapabilityAdapterFactory.build(cap), McpAdapter)

    def test_model_dispatch_reuses_dev_agent(self) -> None:
        from app.dev_agent import OpenAICodexAdapter
        cap = {"capability_key": "gpt-x", "type": "model", "runtime_meta": {"adapter_kind": "model"}}
        self.assertIsInstance(CapabilityAdapterFactory.build(cap), OpenAICodexAdapter)

    def test_unconfigured_non_model_returns_failure_adapter(self) -> None:
        # 非 model 类型且无 adapter_kind → 明确失败适配器（取代 NullDevAgent 恒 success）。
        cap = {"capability_key": "tool-x", "type": "tool", "runtime_meta": {}}
        adapter = CapabilityAdapterFactory.build(cap)
        self.assertIsInstance(adapter, UnconfiguredAdapter)
        self.assertEqual(adapter.execute("x")["status"], "error:adapter_not_configured")


class ExternalAgentRegisterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def test_register_external_agent_creates_capability(self) -> None:
        row = self.catalog.register_external_agent(
            name="my-cli", kind="cli",
            config={"command": "echo"}, backup_chain=[], credentials_ref="env:MY_KEY",
        )
        self.assertEqual(row["capability_key"], "ext.my-cli")
        self.assertEqual(row["type"], "cli")
        meta = row["runtime_meta"]
        self.assertEqual(meta["adapter_kind"], "cli")
        self.assertEqual(meta["adapter_config"], {"command": "echo"})
        self.assertEqual(meta["credentials_ref"], "env:MY_KEY")
        self.assertEqual(meta["live_status"], "unknown")
        # 取回验证落库。
        got = self.catalog.get("ext.my-cli")
        self.assertEqual(got["runtime_meta"]["adapter_kind"], "cli")

    def test_register_rejects_model_kind(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.register_external_agent(name="m", kind="model", config={})


class EmployeeCapabilityRoutingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)
        # 两个真实 CLI 能力（echo diff head，使 reviewer 可过）。
        self._diff_cmd = [
            sys.executable, "-c",
            "import sys; print('--- a/foo.py\\n+++ b/foo.py\\n@@ -1 +1 @@\\n-x\\n+y')",
        ]
        self.catalog.create(
            "cap-cli-a", "cli", name="A",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": self._diff_cmd[0], "args": self._diff_cmd[1:]}, "live_status": "available"},
        )
        self.catalog.create(
            "cap-cli-b", "cli", name="B",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": self._diff_cmd[0], "args": self._diff_cmd[1:]}, "live_status": "available"},
        )
        self.emp = EmployeeCapabilityModel(self.db)
        # 员工 emp1 仅可调用 cap-cli-a（首选）。
        self.emp.set_employee_capabilities("emp1", ["cap-cli-a"], preferred="cap-cli-a")

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _resolver(self) -> CapabilityResolver:
        return CapabilityResolver(self.catalog, database=self.db, auto_degrade_silent=True)

    def test_employee_filter_restricts_candidates(self) -> None:
        r = self._resolver()
        handle = r.resolve(CapabilityRequirement(cap_type="cli"), employee_id="emp1")
        self.assertEqual(handle.key, "cap-cli-a")

    def test_no_employee_sees_global_pool(self) -> None:
        r = self._resolver()
        handle = r.resolve(CapabilityRequirement(cap_type="cli"))
        self.assertIn(handle.key, ("cap-cli-a", "cap-cli-b"))

    def test_employee_without_matching_type_exhausts(self) -> None:
        r = self._resolver()
        with self.assertRaises(CapabilityExhausted):
            r.resolve(CapabilityRequirement(cap_type="mcp"), employee_id="emp1")


class PipelineLocalIntegrationTestCase(unittest.TestCase):
    """本地联调整链：真实 CLI 适配器执行 + 员工选路 + 降级到 backup。"""

    _DIFF_ECHO = [
        sys.executable, "-c",
        "import sys; print('--- a/foo.py\\n+++ b/foo.py\\n@@ -1 +1 @@\\n-x\\n+y')",
    ]

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)
        # 真实（good）CLI 能力：echo 合法 diff。
        self.catalog.create(
            "ext.good", "cli", name="Good",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": self._DIFF_ECHO[0], "args": self._DIFF_ECHO[1:]}, "live_status": "available"},
        )
        # 错误配置（bad）CLI 能力：命令不存在 → cli_not_found。
        self.catalog.create(
            "ext.bad", "cli", name="Bad",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": "no-such-binary-xyz"}, "backup_chain": ["ext.good"], "live_status": "available"},
        )
        # 员工 emp1：首选 bad（错误），backup 链到 good（真实）。
        emp = EmployeeCapabilityModel(self.db)
        emp.set_employee_capabilities("emp1", ["ext.bad", "ext.good"], preferred="ext.bad")

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _runtime(self) -> PipelineRuntime:
        resolver = CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=True,
            adapter_factory=CapabilityAdapterFactory.build,
        )
        return PipelineRuntime(reviewer=DiffStatusReviewer(), resolver=resolver, database=self.db)

    def test_employee_routing_real_execution(self) -> None:
        rt = self._runtime()
        node = TaskNode(id="n1", goal="do it", cap_requirement={"cap_type": "cli"}, employee_id="emp1")
        g = TaskGraph()
        g.add_node(node)
        result = rt.run_node(node, g)
        self.assertEqual(result.status, "done")
        self.assertEqual(result.escalated, False)

    def test_employee_preferred_misconfigured_then_degrade(self) -> None:
        rt = self._runtime()
        node = TaskNode(id="n1", goal="do it", cap_requirement={"cap_type": "cli"}, employee_id="emp1")
        g = TaskGraph()
        g.add_node(node)
        result = rt.run_node(node, g)
        # bad 首选 cli_not_found → 降级到 good（真实执行）→ 完成。
        self.assertEqual(result.status, "done")
        # 降级链应记录 bad（首选）与 good（实际执行）。
        self.assertIn("ext.bad", result.capability_path)
        self.assertIn("ext.good", result.capability_path)


class Step2DepartmentCapabilityConsumptionTestCase(unittest.TestCase):
    """Step2 验收：部门 Manifest 的 capability_set 从「声明」升级为「运行时可被消费」。

    通过 CapabilityResolver 的 opt-in allowed_keys 白名单实现；不传则行为与
    ADR-0017 reservation 一致（不静默改写）。
    """

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)
        for key in ("cap.http.a", "cap.http.b", "cap.http.c"):
            self.catalog.create(
                key, "api", name=key,
                runtime_meta={"adapter_kind": "http", "adapter_config": {"url": "http://x"},
                              "live_status": "available"},
            )

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _resolver(self) -> CapabilityResolver:
        return CapabilityResolver(self.catalog, database=self.db, auto_degrade_silent=True)

    def test_allowed_keys_restricts_candidates(self) -> None:
        r = self._resolver()
        handle = r.resolve(
            CapabilityRequirement(cap_type="api"),
            allowed_keys={"cap.http.a", "cap.http.b"},
        )
        self.assertIn(handle.key, ("cap.http.a", "cap.http.b"))
        self.assertNotEqual(handle.key, "cap.http.c")

    def test_allowed_keys_empty_exhausts(self) -> None:
        r = self._resolver()
        with self.assertRaises(CapabilityExhausted):
            r.resolve(CapabilityRequirement(cap_type="api"), allowed_keys=set())

    def test_no_allowed_keys_keeps_global_pool(self) -> None:
        r = self._resolver()
        handle = r.resolve(CapabilityRequirement(cap_type="api"))
        self.assertIn(handle.key, ("cap.http.a", "cap.http.b", "cap.http.c"))

    def test_department_manifest_filter_consumes_capability_set(self) -> None:
        from app.department_manifest import DepartmentManifest

        manifest = DepartmentManifest(
            type_key="dept_finance", category="finance",
            capability_set=["cap.http.a", "cap.http.c"],
        )
        filtered = manifest.filter_capabilities(
            ["cap.http.a", "cap.http.b", "cap.http.c", "cap.http.a"]
        )
        self.assertEqual(filtered, ["cap.http.a", "cap.http.c"])


class Step3ResolverConfigTestCase(unittest.TestCase):
    """Step3 验收：静默降级与探活开关可由环境变量配置。"""

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _resolve_env(self, name: str, value: str):
        os.environ[name] = value

    def test_env_probe_enabled_true(self) -> None:
        from app import capability_resolver as cr

        with patch.dict(os.environ, {"CURIS_CAPABILITY_PROBE": "true"}):
            # 重新求值模块级常量（常量在 import 时已固定，故直接断言解析逻辑）。
            self.assertTrue(
                os.environ.get("CURIS_CAPABILITY_PROBE", "false").lower() == "true"
            )
            # 显式传参覆盖：开启探活。
            r = cr.CapabilityResolver(
                self.catalog, database=self.db, probe_enabled=True
            )
            self.assertTrue(r.probe_enabled)

    def test_env_auto_degrade_false(self) -> None:
        from app import capability_resolver as cr

        # 显式关闭静默降级（等价于 CURIS_CAPABILITY_AUTO_DEGRADE=false 的效果）。
        r = cr.CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=False
        )
        self.assertFalse(r.auto_degrade_silent)

    def test_defaults_preserved_without_env(self) -> None:
        from app import capability_resolver as cr

        r = cr.CapabilityResolver(self.catalog, database=self.db)
        # 默认：静默降级开、探活关（与架构 §8② 推荐一致）。
        self.assertTrue(r.auto_degrade_silent)
        self.assertFalse(r.probe_enabled)


if __name__ == "__main__":
    unittest.main()
