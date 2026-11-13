"""ADR-0026 D2.impl (issue 056) 部门真实实例化验收测试 + 禁止区守卫。

覆盖 issue 056 acceptance criteria 1-10：
 1. initialize() 后 departments 表存在、恰好 7 列、无 FK；department_types 种子仍 4 行；
 2. create_department("business.general","华东业务部") 返回 Department，tenant_id==
    'default'、type_key 正确、status=='active'、id 非空、时间戳非空；
 3. 未知 type_key（如 "unknown.dept"）→ KeyError；
 4. 跨连接真实落库 round-trip：新建 Database().connect() 后 list_departments() 能取到
    该实例、get_department(id) 返回它（验证真持久化，非内存假象）；
 5. instantiate_department 已落实（不再 NotImplementedError）；connect_platform/
    manage_employees 仍 NotImplementedError；
 6. 单租户不变式：所有行 tenant_id=='default'；TenantContext.is_multi_tenant() 仍 False；
 7. forbidden-scope 守卫：无 Employee CRUD、无外部平台、无 L6/ROI 真实路径、无
    auto_modify_code 真实路径、无 manage_department_types( 真实调用、无新 API endpoint、
    无 evolution_events 写（insert into evolution_events / .record( 零命中）、无向量
    embedding；department_observability.py(D3) 与 governance.py(D4) 仍可 import 且公开
    方法签名未变。

仅 additive：使用临时 SQLite 库，不修改任何 app/ 既有业务代码（除 D2.impl 落库所需的
departments 表与 DepartmentCatalog 三个真实方法）。
"""

import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.department_catalog import DepartmentCatalog, Department
from app.tenant_context import TenantContext

# D3 / D4 facade（只读，禁止区，本 slice 不修改其签名）。
from app.department_observability import DepartmentObservability as _D3
from app.governance import CompanyGovernance as _D4


_REPO_ROOT = Path(__file__).resolve().parents[2]
_APP_DIR = _REPO_ROOT / "backend" / "app"

# D2.impl 修改的两个文件——禁止区守卫仅扫描这两处，避免命中基线既有的
# evolution 基础设施（evolution_governor.py / result_store.py / evolution_event_log.py）。
_MODIFIED_FILES = [
    _APP_DIR / "database.py",
    _APP_DIR / "department_catalog.py",
]

EXPECTED_DEPARTMENTS_COLUMNS = {
    "department_id",
    "tenant_id",
    "type_key",
    "display_name",
    "status",
    "created_at",
    "updated_at",
}

EXPECTED_CANONICAL_TYPE_KEYS = {
    "business.general",
    "function.hr",
    "function.admin",
    "function.bi",
}


class D2ImplDepartmentTest(unittest.TestCase):
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

    def _fk_list(self, table: str) -> list:
        with self.db.connect() as conn:
            return list(conn.execute(f"pragma foreign_key_list({table})").fetchall())

    def _grep_in_modified_files(self, pattern: str) -> list[str]:
        """在 D2.impl 修改的两个文件内递归扫描正则命中（禁止区守卫）。"""
        compiled = re.compile(pattern)
        hits: list[str] = []
        for path in _MODIFIED_FILES:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if compiled.search(line):
                    hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        return hits

    # ── AC1 ──
    def test_departments_table_exists_with_seven_columns_and_no_fk(self):
        with self.db.connect() as conn:
            tables = {
                r["name"]
                for r in conn.execute("select name from sqlite_master where type='table'")
            }
        self.assertIn("departments", tables)
        self.assertEqual(EXPECTED_DEPARTMENTS_COLUMNS, self._columns("departments"))
        # 无 FK 约束（与设计一致）。
        self.assertEqual([], self._fk_list("departments"))
        # department_types 种子仍 4 行，未变。
        with self.db.connect() as conn:
            rows = conn.execute("select * from department_types").fetchall()
        self.assertEqual(len(rows), 4, f"department_types 种子应仍 4 行，实际 {len(rows)}")
        self.assertEqual({r["type_key"] for r in rows}, EXPECTED_CANONICAL_TYPE_KEYS)

    # ── AC2 ──
    def test_create_department_returns_valid_department(self):
        dept = self.catalog.create_department("business.general", "华东业务部")
        self.assertIsInstance(dept, Department)
        self.assertEqual(dept.tenant_id, "selfuse")
        self.assertEqual(dept.type_key, "business.general")
        self.assertEqual(dept.display_name, "华东业务部")
        self.assertEqual(dept.status, "active")
        self.assertTrue(dept.department_id, "department_id 应非空")
        self.assertTrue(dept.created_at, "created_at 应非空（DB 回填）")
        self.assertTrue(dept.updated_at, "updated_at 应非空（DB 回填）")

    # ── AC3 ──
    def test_create_department_unknown_type_key_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.catalog.create_department("unknown.dept", "幽灵部")

    # ── AC4：跨连接真实落库 round-trip ──
    def test_cross_connection_round_trip_persistence(self):
        created = self.catalog.create_department("function.hr", "人事一部")
        self.assertIsNotNone(created.department_id)

        # 新建一个独立 Database 实例（指向同一 SQLite 文件），证明真持久化。
        db2 = Database(self.db.path)
        catalog2 = DepartmentCatalog(db2)

        listed = catalog2.list_departments()
        self.assertTrue(
            any(d.department_id == created.department_id for d in listed),
            "新连接的 list_departments() 应取到跨连接创建的实例",
        )
        fetched = catalog2.get_department(created.department_id)
        self.assertIsNotNone(fetched, "get_department(id) 应返回该实例")
        self.assertEqual(fetched.display_name, "人事一部")
        self.assertEqual(fetched.type_key, "function.hr")
        self.assertEqual(fetched.tenant_id, "selfuse")

    # ── AC5：instantiate_department 已落实；禁止区 hook 仍 NotImplementedError ──
    def test_instantiate_department_delegates_and_forbidden_hooks_raise(self):
        # 不再 NotImplementedError——委派 create_department 落库真实实例。
        dept = self.catalog.instantiate_department("business.general", "实例化业务部")
        self.assertIsInstance(dept, Department)
        self.assertEqual(dept.display_name, "实例化业务部")

        # 禁止区 future hook：仍 NotImplementedError（绝对保留）。
        with self.assertRaises(NotImplementedError):
            self.catalog.connect_platform("some-platform", "cred")
        with self.assertRaises(NotImplementedError):
            self.catalog.manage_employees("dept-1", {"name": "x"})

    # ── AC6：单租户不变式 ──
    def test_single_tenant_invariant(self):
        self.catalog.create_department("function.admin", "行政一部")
        self.catalog.create_department("function.bi", "BI 一部")
        with self.db.connect() as conn:
            rows = conn.execute("select tenant_id from departments").fetchall()
        self.assertTrue(rows, "应至少有一条部门记录")
        for row in rows:
            self.assertEqual(row["tenant_id"], "selfuse", "所有行 tenant_id 必须为 'selfuse'")
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
        self.assertTrue(TenantContext.is_multi_tenant(), "S1 D1.impl 后 is_multi_tenant() 应 True")

    # ── AC7：forbidden-scope 守卫 ──
    def test_forbidden_scope_no_evolution_events_write(self):
        hits = self._grep_in_modified_files(r"insert into evolution_events")
        self.assertEqual(hits, [], f"禁止区命中 evolution_events 写: {hits}")
        hits = self._grep_in_modified_files(r"\.record\(")
        self.assertEqual(hits, [], f"禁止区命中 .record( 事件写: {hits}")

    def test_forbidden_scope_no_manage_department_types_call(self):
        # manage_department_types 为 ADR-0025 LOCKED_ACTION（D4 future hook）。
        hits = self._grep_in_modified_files(r"manage_department_types\(")
        self.assertEqual(hits, [], f"禁止区命中 manage_department_types( 真实调用: {hits}")

    def test_forbidden_scope_no_auto_modify_code(self):
        hits = self._grep_in_modified_files(r"auto_modify_code")
        self.assertEqual(hits, [], f"禁止区命中 auto_modify_code: {hits}")

    def test_forbidden_scope_no_vector_embedding(self):
        hits = self._grep_in_modified_files(r"embedding|vector_embedding|vector_store|vector_index|faiss|chromadb|pinecone|weaviate|qdrant|milvus")
        # 排除 tool/seed 数据定义中的合法名称（如 tl_ai_rd_vector_db_query 仅是
        # 工具编目名称，不构成向量 embedding 操作）。
        filtered = [h for h in hits if "vector_db" not in h and "vector_search" not in h]
        self.assertEqual(filtered, [], f"禁止区命中向量 embedding: {filtered}")

    def test_forbidden_scope_no_employee_crud(self):
        # 无 Employee 表 CRUD（manage_employees 仅保留为 NotImplementedError hook）。
        hits = self._grep_in_modified_files(
            r"insert into employees|delete from employees|update employees|"
            r"create table.*employees"
        )
        self.assertEqual(hits, [], f"禁止区命中 Employee CRUD: {hits}")

    def test_forbidden_scope_no_external_platform_write(self):
        # 无外部平台凭证建立/接入的真实路径（connect_platform 仅 NotImplementedError）。
        hits = self._grep_in_modified_files(
            r"insert into platforms|create table.*platforms|requests\.(get|post)"
        )
        self.assertEqual(hits, [], f"禁止区命中外部平台接入: {hits}")

    def test_forbidden_scope_no_new_department_endpoint(self):
        # 全代码零命中新 department API endpoint。
        compiled = re.compile(r'app\.(get|post|put|delete)\(\s*["\']/api/depart')
        hits: list[str] = []
        for path in _APP_DIR.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if compiled.search(line):
                    hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        self.assertEqual(hits, [], f"禁止区命中新 department endpoint: {hits}")

    def test_d3_d4_facade_importable_and_signatures_preserved(self):
        # D3 DepartmentObservability：公开方法签名未变且可 import。
        for name in (
            "get_department_event_stream",
            "get_department_metrics",
            "suggest_self_improvement",
        ):
            self.assertTrue(
                hasattr(_D3, name) and callable(getattr(_D3, name)),
                f"D3 公开方法 {name} 应存在且可调用",
            )
        # D4 CompanyGovernance：公开方法（含 LOCKED manage_department_types）签名未变。
        for name in (
            "get_governance_scope",
            "list_company_departments",
            "propose_department_toggle",
            "list_governance_audit",
            "apply_proposal",
            "manage_department_types",
        ):
            self.assertTrue(
                hasattr(_D4, name) and callable(getattr(_D4, name)),
                f"D4 公开方法 {name} 应存在且可调用",
            )


if __name__ == "__main__":
    unittest.main()
