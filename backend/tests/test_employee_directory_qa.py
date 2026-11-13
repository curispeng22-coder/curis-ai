"""QA 验收测试：Workspace 员工目录最小版本（P0 T1-T6）

覆盖新 3 API 端点：
- PATCH /api/workspace/employees/{employee_id}
- DELETE /api/workspace/employees/{employee_id}
- DELETE /api/workspace/departments/{department_id}

运行方式（backend/ 下）：
    PYTHONPATH=. /path/to/python -m pytest tests/test_employee_directory_qa.py -v
"""
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app

TENANT = "selfuse"
ALT_TENANT = "other-tenant"

# 已知的官方模板 ID（由 seed 确保）
DEPT_TEMPLATE_ID = "official.department.software_rnd"
EMP_TEMPLATE_ID = "official.employee.tech_lead"


def _create_dept(client, template_id=DEPT_TEMPLATE_ID, name="测试研发部"):
    """辅助：创建部门实例并返回其 id。"""
    resp = client.post(
        "/api/workspace/departments",
        headers={"X-Tenant-Id": TENANT},
        json={"template_id": template_id, "name": name},
    )
    assert resp.status_code == 201, f"创建部门失败: {resp.status_code} {resp.text}"
    return resp.json()["id"]


def _create_emp(client, department_id, template_id=EMP_TEMPLATE_ID, name="测试员工"):
    """辅助：创建员工实例并返回其 id。"""
    resp = client.post(
        "/api/workspace/employees",
        headers={"X-Tenant-Id": TENANT},
        json={
            "department_id": department_id,
            "template_id": template_id,
            "name": name,
            "instructions_override": "初始指令",
            "status": "idle",
            "enabled": True,
        },
    )
    assert resp.status_code == 201, f"创建员工失败: {resp.status_code} {resp.text}"
    return resp.json()["id"]


class TestEmployeePatch(unittest.TestCase):
    """PATCH /api/workspace/employees/{id} 测试"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))
        # 准备测试数据
        self.dept_id = _create_dept(self.client)
        self.emp_id = _create_emp(self.client, self.dept_id)

    def tearDown(self):
        self.tmp.cleanup()

    def _get_employee_from_db(self, emp_id):
        """直接查 DB 获取员工记录（因无 GET /employees/{id} 端点）"""
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "select * from employee_instances where id = ?", (emp_id,)
            ).fetchone()
        return dict(row) if row else None

    def test_patch_employee_success_update_all_fields(self):
        """成功更新所有可编辑字段"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={
                "name": "新名字",
                "instructions_override": "新指令覆盖",
                "status": "assigned",
                "enabled": True,
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["name"], "新名字")
        self.assertEqual(body["instructions_override"], "新指令覆盖")
        self.assertEqual(body["status"], "assigned")
        self.assertTrue(body["enabled"])

        # 验证 DB 持久化
        db_emp = self._get_employee_from_db(self.emp_id)
        self.assertEqual(db_emp["name"], "新名字")
        self.assertEqual(db_emp["instructions_override"], "新指令覆盖")
        self.assertEqual(db_emp["status"], "assigned")
        self.assertEqual(db_emp["enabled"], 1)

    def test_patch_employee_partial_update(self):
        """部分更新：只传 name，其他字段不变"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"name": "部分更新名"},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["name"], "部分更新名")

        # 验证 DB：instructions_override 保持原值，status=enabled 未变
        db_emp = self._get_employee_from_db(self.emp_id)
        self.assertEqual(db_emp["name"], "部分更新名")
        self.assertEqual(db_emp["instructions_override"], "初始指令")
        self.assertEqual(db_emp["status"], "idle")
        self.assertEqual(db_emp["enabled"], 1)

    def test_patch_employee_404_not_found(self):
        """不存在的 id → 404"""
        resp = self.client.patch(
            "/api/workspace/employees/nonexistent-id",
            headers={"X-Tenant-Id": TENANT},
            json={"name": "任何人"},
        )
        self.assertEqual(resp.status_code, 404)

    def test_patch_employee_status_to_disabled_sets_enabled_0(self):
        """status→disabled 时 enabled 自动派生为 0"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"status": "disabled"},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["status"], "disabled")
        self.assertFalse(body["enabled"])

        db_emp = self._get_employee_from_db(self.emp_id)
        self.assertEqual(db_emp["status"], "disabled")
        self.assertEqual(db_emp["enabled"], 0)

    def test_patch_employee_enabled_to_false_sets_status_disabled(self):
        """enabled→false 时 status 自动派生为 disabled"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"enabled": False},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertFalse(body["enabled"])
        self.assertEqual(body["status"], "disabled")

    def test_patch_employee_invalid_status_422(self):
        """非法 status 值 → 422"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"status": "invalid_status"},
        )
        self.assertEqual(resp.status_code, 422)

    def test_patch_employee_empty_name_422(self):
        """空 name → 422"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"name": "   "},
        )
        self.assertEqual(resp.status_code, 422)

    def test_patch_employee_tenant_isolation(self):
        """用非 selfuse tenant 头 → 404（隔离生效）"""
        resp = self.client.patch(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": ALT_TENANT},
            json={"name": "跨租户"},
        )
        self.assertEqual(resp.status_code, 404)


class TestEmployeeDelete(unittest.TestCase):
    """DELETE /api/workspace/employees/{id} 测试"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))
        self.dept_id = _create_dept(self.client)
        self.emp_id = _create_emp(self.client, self.dept_id)

    def tearDown(self):
        self.tmp.cleanup()

    def _get_employee_from_db(self, emp_id):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "select * from employee_instances where id = ?", (emp_id,)
            ).fetchone()
        return dict(row) if row else None

    def test_delete_employee_success(self):
        """成功删除员工后 get 应返回 404"""
        resp = self.client.delete(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 204)

        # 直查 DB：deleted_at 非空
        db_emp = self._get_employee_from_db(self.emp_id)
        self.assertIsNotNone(db_emp["deleted_at"])
        self.assertEqual(db_emp["enabled"], 0)

        # 列表不应包含已删员工
        list_resp = self.client.get(
            "/api/workspace/employees",
            headers={"X-Tenant-Id": TENANT},
        )
        emp_ids = [e["id"] for e in list_resp.json().get("employees", [])]
        self.assertNotIn(self.emp_id, emp_ids)

    def test_delete_employee_404_not_found(self):
        """不存在的 id → 404"""
        resp = self.client.delete(
            "/api/workspace/employees/nonexistent-id",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_employee_is_manager_422(self):
        """员工是某部门 manager_employee_id → 422"""
        # 创建第二个普通员工
        emp2_id = _create_emp(self.client, self.dept_id, name="普通员工")
        # 将部门 manager 设置为 emp2_id
        patch_resp = self.client.patch(
            f"/api/workspace/departments/{self.dept_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"manager_employee_id": emp2_id},
        )
        self.assertEqual(patch_resp.status_code, 200)

        # 尝试删除作为 manager 的员工
        resp = self.client.delete(
            f"/api/workspace/employees/{emp2_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 422)
        self.assertIn("manager", resp.text.lower())

    def test_delete_employee_tenant_isolation(self):
        """用非 selfuse tenant 头 → 404"""
        resp = self.client.delete(
            f"/api/workspace/employees/{self.emp_id}",
            headers={"X-Tenant-Id": ALT_TENANT},
        )
        self.assertEqual(resp.status_code, 404)


class TestDepartmentDelete(unittest.TestCase):
    """DELETE /api/workspace/departments/{id} 测试"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))
        self.dept_id = _create_dept(self.client)

    def tearDown(self):
        self.tmp.cleanup()

    def _get_department_from_db(self, dept_id):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "select * from department_instances where id = ?", (dept_id,)
            ).fetchone()
        return dict(row) if row else None

    def test_delete_department_success(self):
        """成功删除部门后列表和 DB 应反映删除"""
        resp = self.client.delete(
            f"/api/workspace/departments/{self.dept_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 204)

        db_dept = self._get_department_from_db(self.dept_id)
        self.assertIsNotNone(db_dept["deleted_at"])
        self.assertEqual(db_dept["enabled"], 0)

        # 列表不应包含
        list_resp = self.client.get(
            "/api/workspace/departments",
            headers={"X-Tenant-Id": TENANT},
        )
        dept_ids = [d["id"] for d in list_resp.json().get("departments", [])]
        self.assertNotIn(self.dept_id, dept_ids)

    def test_delete_department_has_active_employees_422(self):
        """部门有在职员工 → 422"""
        _create_emp(self.client, self.dept_id, name="在职员工")
        resp = self.client.delete(
            f"/api/workspace/departments/{self.dept_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 422)
        self.assertIn("active", resp.text.lower())

    def test_delete_department_only_disabled_employees_ok(self):
        """部门只有 disabled 员工时允许删除"""
        emp_id = _create_emp(self.client, self.dept_id, name="已禁用员工")
        self.client.patch(
            f"/api/workspace/employees/{emp_id}",
            headers={"X-Tenant-Id": TENANT},
            json={"enabled": False},
        )
        resp = self.client.delete(
            f"/api/workspace/departments/{self.dept_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        self.assertEqual(resp.status_code, 204)

    def test_delete_department_tenant_isolation(self):
        """用非 selfuse tenant 头 → 404"""
        resp = self.client.delete(
            f"/api/workspace/departments/{self.dept_id}",
            headers={"X-Tenant-Id": ALT_TENANT},
        )
        self.assertEqual(resp.status_code, 404)


class TestSoftDeleteSemantics(unittest.TestCase):
    """软删除语义验证"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_deleted_employee_not_in_list(self):
        """已删员工不在列表中"""
        dept_id = _create_dept(self.client)
        emp_id = _create_emp(self.client, dept_id)
        self.client.delete(
            f"/api/workspace/employees/{emp_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        list_resp = self.client.get(
            "/api/workspace/employees",
            headers={"X-Tenant-Id": TENANT},
        )
        emp_ids = [e["id"] for e in list_resp.json().get("employees", [])]
        self.assertNotIn(emp_id, emp_ids)

    def test_deleted_department_not_in_list(self):
        """已删部门（无在职员工时）不在列表中"""
        dept_id = _create_dept(self.client)
        # 注意：不创建员工，直接删除部门
        self.client.delete(
            f"/api/workspace/departments/{dept_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        list_resp = self.client.get(
            "/api/workspace/departments",
            headers={"X-Tenant-Id": TENANT},
        )
        dept_ids = [d["id"] for d in list_resp.json().get("departments", [])]
        self.assertNotIn(dept_id, dept_ids)

    def test_deleted_employee_has_deleted_at_and_enabled_0(self):
        """已删记录的 deleted_at 不为 null，enabled=0"""
        dept_id = _create_dept(self.client)
        emp_id = _create_emp(self.client, dept_id)
        self.client.delete(
            f"/api/workspace/employees/{emp_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        with closing(sqlite3.connect(self.db_path)) as conn:
            row = conn.execute(
                "select deleted_at, enabled from employee_instances where id = ?",
                (emp_id,),
            ).fetchone()
        self.assertIsNotNone(row[0], "deleted_at 不应为 NULL")
        self.assertEqual(row[1], 0, "enabled 应为 0")

    def test_deleted_department_has_deleted_at_and_enabled_0(self):
        """已删部门（无在职员工）的 deleted_at 不为 null，enabled=0"""
        dept_id = _create_dept(self.client)
        # 注意：不创建员工，确保删除成功
        self.client.delete(
            f"/api/workspace/departments/{dept_id}",
            headers={"X-Tenant-Id": TENANT},
        )
        with closing(sqlite3.connect(self.db_path)) as conn:
            row = conn.execute(
                "select deleted_at, enabled from department_instances where id = ?",
                (dept_id,),
            ).fetchone()
        self.assertIsNotNone(row[0], "deleted_at 不应为 NULL")
        self.assertEqual(row[1], 0, "enabled 应为 0")


if __name__ == "__main__":
    unittest.main()
