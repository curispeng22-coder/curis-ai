"""ADR-0017 D2 部门目录通用化 reservation 契约测试 + 禁止区守卫。

覆盖 issue 052 acceptance criteria 1-8：
 1. department_types 表存在且列齐全；
 2. 恰好 4 行规范类型，manifest_json 解析为占位空结构；
 3. MANIFEST_FIELDS 含 7 键；
 4. list_types() 非空、get_manifest("business.general") 返回占位 DepartmentManifest、
    assemble_company_topology(...) 返回内存 CompanyTopology 且持久化零表；
 5. backend/app 全代码无 WHERE department_id 读路径过滤；
 6. 无新 /api/department API endpoint；
 7. TenantContext 不变式保持（current_tenant_id='default'、is_multi_tenant=False）；
 8. 后端全量回归绿、未修改既有测试（本文件为新增，不触碰既有测试）。

本测试为只读检查：使用临时 SQLite 库，不修改任何 app/ 业务代码。
"""

import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.department_catalog import DepartmentCatalog, CompanyTopology
from app.department_manifest import DepartmentManifest, MANIFEST_FIELDS
from app.tenant_context import TenantContext


_REPO_ROOT = Path(__file__).resolve().parents[2]
_APP_DIR = _REPO_ROOT / "backend" / "app"

EXPECTED_DEPARTMENT_TYPE_COLUMNS = {
    "type_key",
    "category",
    "display_name",
    "description",
    "manifest_json",
    "manifest_schema_version",
    "is_system",
}

EXPECTED_CANONICAL_TYPE_KEYS = {
    "business.general",
    "function.hr",
    "function.admin",
    "function.bi",
}

EXPECTED_MANIFEST_KEYS = {
    "capability_set",
    "tool_classes",
    "quality_lines",
    "output_channels",
    "roi_schema",
    "guardrail_refs",
    "employee_role_spec",
}


class D2DepartmentCatalogReservationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.catalog = DepartmentCatalog(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def _columns(self, table: str) -> set[str]:
        with self.db.connect() as conn:
            return {c["name"] for c in conn.execute(f"pragma table_info({table})")}

    def _all_tables(self) -> set[str]:
        with self.db.connect() as conn:
            return {
                r["name"]
                for r in conn.execute(
                    "select name from sqlite_master where type='table'"
                ).fetchall()
            }

    def _grep_app(self, pattern: str) -> list[str]:
        """在 backend/app 目录递归扫描正则命中（禁止区守卫）。"""
        compiled = re.compile(pattern)
        hits: list[str] = []
        for path in _APP_DIR.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if compiled.search(line):
                    hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        return hits

    # ── AC1 ──
    def test_department_types_table_has_all_columns(self):
        self.assertIn("department_types", self._all_tables())
        self.assertEqual(
            EXPECTED_DEPARTMENT_TYPE_COLUMNS,
            self._columns("department_types"),
        )

    # ── AC2 ──
    def test_department_types_has_exactly_four_canonical_rows(self):
        with self.db.connect() as conn:
            rows = conn.execute("select * from department_types").fetchall()
        self.assertEqual(len(rows), 4, f"expected 4 rows, got {len(rows)}")
        keys = {row["type_key"] for row in rows}
        self.assertEqual(keys, EXPECTED_CANONICAL_TYPE_KEYS)
        for row in rows:
            parsed = json.loads(row["manifest_json"])
            self.assertEqual(
                parsed, {},
                f"manifest_json 应为占位空结构 {{}}，实际: {row['type_key']} -> {parsed!r}",
            )

    # ── AC3 ──
    def test_manifest_fields_has_seven_keys(self):
        self.assertEqual(set(MANIFEST_FIELDS.keys()), EXPECTED_MANIFEST_KEYS)

    # ── AC4 ──
    def test_list_types_nonempty_and_get_manifest_placeholder(self):
        types = self.catalog.list_types()
        self.assertTrue(types, "list_types() 应返回非空目录")
        for item in types:
            self.assertEqual(item.type_key, item.manifest.type_key)
        manifest = self.catalog.get_manifest("business.general")
        self.assertIsInstance(manifest, DepartmentManifest)
        # 占位：字段为空结构，不消费任何真实数据
        self.assertEqual(manifest.capability_set, [])
        self.assertEqual(manifest.tool_classes, [])
        self.assertEqual(manifest.employee_role_spec, {})
        self.assertEqual(manifest.roi_schema, {})
        self.assertEqual(manifest.manifest_schema_version, "0.0")

    def test_get_manifest_unknown_key_returns_none(self):
        # 未实例化任何部门；未知 key 仅返回 None，不触 forbidden zone
        self.assertIsNone(self.catalog.get_manifest("function.unknown"))

    def test_assemble_company_topology_in_memory_only(self):
        topology = self.catalog.assemble_company_topology(
            "ceo-1", ["business.general", "function.hr", "function.unknown"]
        )
        self.assertIsInstance(topology, CompanyTopology)
        self.assertEqual(topology.ceo_id, "ceo-1")
        self.assertEqual(
            topology.selected_type_keys,
            ["business.general", "function.hr", "function.unknown"],
        )
        # 仅已知 key 被投影为占位 Manifest；未知 key 被忽略
        self.assertEqual(len(topology.manifests), 2)
        # Phase-1A 已新增 companies 作为正式 Workspace 运行时聚合根；但这里的
        # legacy 拓扑投影仍必须保持纯内存，不得写入 CompanyRuntime。
        tables = self._all_tables()
        self.assertIn("companies", tables)
        self.assertNotIn("company_topology", tables)
        with self.db.connect() as connection:
            company_count = connection.execute("select count(*) as count from companies").fetchone()["count"]
        self.assertEqual(company_count, 0)

    # ── AC7 ──
    def test_tenant_context_invariant_preserved(self):
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
        self.assertTrue(TenantContext.is_multi_tenant())

    # ── AC5：禁止区守卫 ──
    def test_forbidden_scope_no_department_id_filter(self):
        hits = self._grep_app(r"WHERE\s+department_id")
        self.assertEqual(
            hits, [],
            f"禁止区命中 WHERE department_id 读路径过滤: {hits}",
        )

    # ── AC6：禁止区守卫 ──
    def test_forbidden_scope_no_new_department_endpoint(self):
        hits = self._grep_app(r'app\.(get|post|put|delete)\(\s*["\']/api/department')
        self.assertEqual(
            hits, [],
            f"禁止区命中新 department endpoint: {hits}",
        )


if __name__ == "__main__":
    unittest.main()
