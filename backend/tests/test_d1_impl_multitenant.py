"""ADR-0017 S1 D1.impl (issue 057 / ADR-0027) — real multi-tenant isolation.

验收焦点（task isolation 为本 slice 的 acceptance criterion）：
  1. ``TenantContext.is_multi_tenant()`` 为 ``True``（D1 预留已落地为真实隔离）。
  2. ``scope()`` 在块内设置 contextvar、块后还原。
  3. ``parse_tenant_from_request`` 读取 ``X-Tenant-Id`` 头，缺省回退哨兵。
  4. 租户 A 创建的任务对租户 B 不可见（list_tasks / get_task 隔离）。
  5. ``initialize()`` 后 ``tenants`` 表存在且含 ``default`` 行，且无任何凭证列。

实现要点：
  - ``Database.connect()`` 每次调用新开连接，故 ``:memory:`` 无法跨 ResultStore
    方法持久化；本测试使用文件型临时库（与 test_d1_tenant.py 一致），等价验证隔离。
  - 不触碰 evolution_events 写路径；不引入任何凭证持久化。
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.result_store import ResultStore
from app.tenant_context import DEFAULT_TENANT, TenantContext


class _FakeRequest:
    """极简请求替身：仅暴露 ``headers`` 映射（与 FastAPI/Starlette 一致）。"""

    def __init__(self, headers: dict[str, str] | None = None):
        self.headers = headers or {}


class D1ImplMultitenantTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()

    def tearDown(self):
        self.tmp.cleanup()

    # ── AC1：多租户开关已开启 ──
    def test_is_multi_tenant_is_true(self):
        self.assertTrue(TenantContext.is_multi_tenant(), "S1 D1.impl 应使 is_multi_tenant() 为 True")

    # ── AC2：scope 注入与还原 ──
    def test_scope_sets_and_restores(self):
        self.assertEqual(TenantContext.current_tenant_id(), DEFAULT_TENANT)
        with TenantContext.scope("tenant-x"):
            self.assertEqual(TenantContext.current_tenant_id(), "tenant-x")
        self.assertEqual(TenantContext.current_tenant_id(), DEFAULT_TENANT)

    # ── AC3：请求级租户解析 ──
    def test_parse_tenant_from_request_uses_header(self):
        request = _FakeRequest({"X-Tenant-Id": "acme-corp"})
        self.assertEqual(TenantContext.parse_tenant_from_request(request), "acme-corp")

    def test_parse_tenant_from_request_falls_back_to_default(self):
        self.assertEqual(
            TenantContext.parse_tenant_from_request(_FakeRequest({})),
            DEFAULT_TENANT,
        )
        self.assertEqual(
            TenantContext.parse_tenant_from_request(_FakeRequest({"X-Tenant-Id": ""})),
            DEFAULT_TENANT,
        )

    # ── AC4：任务跨租户隔离 ──
    def test_task_created_for_tenant_a_invisible_to_tenant_b(self):
        store = ResultStore(self.db)

        with TenantContext.scope("tenant-a"):
            task = store.create_task("task for A")
            task_id = task["task_id"]
            # 落库行应被打上 tenant-a 标记。
            with self.db.connect() as conn:
                row = conn.execute(
                    "select tenant_id from tasks where task_id = ?", (task_id,)
                ).fetchone()
            self.assertEqual(row["tenant_id"], "tenant-a")

        # 租户 B 看不到 A 的任务。
        with TenantContext.scope("tenant-b"):
            self.assertEqual(store.list_tasks(), [])
            with self.assertRaises(KeyError):
                store.get_task(task_id)

        # 租户 A 仍能看到自己的任务。
        with TenantContext.scope("tenant-a"):
            self.assertEqual(len(store.list_tasks()), 1)
            self.assertEqual(store.get_task(task_id)["task_id"], task_id)

    # ── AC4（延伸）：执行记录同样按租户隔离 ──
    def test_executions_isolated_across_tenants(self):
        store = ResultStore(self.db)
        with TenantContext.scope("tenant-a"):
            task = store.create_task("task for A")
            store.save_execution(task["task_id"], "codex_tool", "p", "o", 0.0)
        with TenantContext.scope("tenant-b"):
            self.assertEqual(store.list_executions(task["task_id"]), [])
        with TenantContext.scope("tenant-a"):
            self.assertEqual(len(store.list_executions(task["task_id"])), 1)

    # ── AC5：tenants 表存在、含 default 行、无凭证列 ──
    def test_tenants_table_exists_with_default_row_and_no_credentials(self):
        with self.db.connect() as conn:
            tables = {
                r["name"]
                for r in conn.execute("select name from sqlite_master where type='table'")
            }
            self.assertIn("tenants", tables)

            columns = {c["name"] for c in conn.execute("pragma table_info(tenants)")}
            self.assertIn("tenant_id", columns)
            self.assertIn("name", columns)

            # 安全边界：绝不允许凭证列存在。
            for credential in ("api_key", "token", "secret", "password"):
                self.assertNotIn(
                    credential,
                    columns,
                    f"tenants 表不得包含凭证列 {credential}",
                )

            default_row = conn.execute(
                "select * from tenants where tenant_id = ?", (DEFAULT_TENANT,)
            ).fetchone()
            self.assertIsNotNone(default_row, "initialize() 应种子化 default 租户")
            self.assertEqual(default_row["name"], "Default Tenant")


if __name__ == "__main__":
    unittest.main()
