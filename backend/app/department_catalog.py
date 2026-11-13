"""只读部门目录 facade（ADR-0017 D2 reservation）。

本模块暴露**纯查询**能力，所有公开方法只读、无副作用、不触外部 I/O
（除本地 SQLite 读）。部门实例化、外部平台接入与员工管理仅声明为 future hook，
在本 slice **不实现、不引用**，留作 D2.impl + 安全边界席 review。

禁止区（来自 ADR-0023 / issue 052）：
- 不建 ``departments`` / ``company_topology`` 表、不持久化拓扑；
- 不接外部平台、不碰凭证、不触合规面；
- 不实现 L6 经济 / ROI 统计、不接 BI / 可视化；
- 不做 Employee CRUD、不建员工层、不建角色 / 技能配置事实接口；
- 不解析 / 校验 / 消费 Manifest 去驱动工具路由或质量线；
- 不加按部门作用域的读路径过滤、不加任何 API endpoint。
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .database import Database
from .department_manifest import DepartmentManifest
from .tenant_context import DEFAULT_TENANT, TenantContext


@dataclass
class DepartmentType:
    """系统级部门类型目录中的一个条目（建一次、全员可用）。"""

    type_key: str
    category: str
    display_name: str
    description: str
    manifest: DepartmentManifest
    manifest_schema_version: str
    is_system: bool


@dataclass
class CompanyTopology:
    """CEO 从目录挑选子集组装的公司拓扑（纯内存投影，不持久化）。"""

    ceo_id: str
    selected_type_keys: list[str]
    manifests: list[DepartmentManifest]
    assembled_at: str


@dataclass
class Department:
    """部门实例聚合根（ADR-0026 D2.impl，issue 056）。

    对应 ``departments`` 表的一行；落库后由 DB 回填 ``created_at`` / ``updated_at``。
    单租户：``tenant_id`` 恒为 ``'default'``（由 ``TenantContext`` 解析）。
    """

    department_id: str
    tenant_id: str
    type_key: str
    display_name: str
    status: str
    created_at: str
    updated_at: str


class DepartmentCatalog:
    """部门目录只读 facade。

    所有方法仅读取系统级共享表 ``department_types`` 并返回占位 Manifest，
    不做任何写操作、不接外部平台、不管理员工。
    """

    def __init__(self, database: Database) -> None:
        self.database = database

    def list_types(self) -> list[DepartmentType]:
        """列出系统级部门类型目录（全员可用）。"""
        rows: list[dict[str, Any]] = []
        with self.database.connect() as connection:
            cursor = connection.execute(
                "select type_key, category, display_name, description, "
                "manifest_json, manifest_schema_version, is_system "
                "from department_types order by type_key"
            )
            for row in cursor:
                rows.append(dict(row))
        return [self._row_to_type(row) for row in rows]

    def get_manifest(self, type_key: str) -> DepartmentManifest | None:
        """取某类型的 Manifest 骨架（占位结构）。

        返回 ``None`` 表示该 type_key 不在目录中（本 slice 不做实例化）。
        """
        with self.database.connect() as connection:
            row = connection.execute(
                "select type_key, category, display_name, description, "
                "manifest_json, manifest_schema_version, is_system "
                "from department_types where type_key = ?",
                (type_key,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_type(dict(row)).manifest

    def assemble_company_topology(
        self, ceo_id: str, selected_type_keys: list[str]
    ) -> CompanyTopology:
        """CEO 从目录挑选子集，组装公司拓扑——纯内存投影，不持久化、不写 tenant。

        仅对已存在于目录的 type_key 投影出占位 Manifest；未知 key 被忽略。
        CEO 持久化其拓扑为未来 slice（D2.impl）职责。
        """
        catalog = {item.type_key: item for item in self.list_types()}
        manifests = [
            catalog[key].manifest
            for key in selected_type_keys
            if key in catalog
        ]
        return CompanyTopology(
            ceo_id=ceo_id,
            selected_type_keys=list(selected_type_keys),
            manifests=manifests,
            assembled_at=datetime.now(timezone.utc).isoformat(),
        )

    # ── ADR-0026 D2.impl (issue 056): 部门真实实例化 ──
    def create_department(
        self,
        type_key: str,
        display_name: str,
        tenant_id: str | None = None,
        department_id: str | None = None,
        status: str = "active",
    ) -> Department:
        """落库一个部门实例（聚合根）。

        - ``tenant_id`` 缺省取 ``TenantContext.current_tenant_id()``（部门为系统级，
          恒为 ``'default'``）；部门目录跨租户共享，不做租户隔离。
        - ``type_key`` 须经 ``get_manifest`` 校验存在性，未知 → 抛 ``KeyError``。
        - ``department_id`` 缺省用 ``uuid.uuid4().hex``（标准库，无新第三方依赖）。
        - INSERT 后由 DB 回填 ``created_at`` / ``updated_at``，返回完整 ``Department``。
        """
        # 部门为系统级共享目录（ADR-0023）：无论系统是否多租户，部门实例恒为
        # tenant_id=DEFAULT_TENANT，不做租户隔离。D1.impl (issue 057) 已放开
        # is_multi_tenant()，此处不再以多租户标志作为门禁，而是强制部门恒为系统级
        # （tenant_id 必须解析为 DEFAULT_TENANT），保持目录跨租户共享的语义。
        resolved_tenant_id = (
            tenant_id if tenant_id is not None else TenantContext.current_tenant_id()
        )
        assert resolved_tenant_id == DEFAULT_TENANT, (
            "departments are system-level (ADR-0023); tenant_id must resolve to "
            f"{DEFAULT_TENANT!r}"
        )

        # type_key 存在性校验（未知 → KeyError）。
        if self.get_manifest(type_key) is None:
            raise KeyError(
                f"未知部门类型 type_key={type_key!r}：须先存在于 department_types 目录"
            )

        resolved_department_id = (
            department_id if department_id is not None else uuid.uuid4().hex
        )

        with self.database.connect() as connection:
            connection.execute(
                "insert into departments "
                "(department_id, tenant_id, type_key, display_name, status) "
                "values (?, ?, ?, ?, ?)",
                (
                    resolved_department_id,
                    resolved_tenant_id,
                    type_key,
                    display_name,
                    status,
                ),
            )
            row = connection.execute(
                "select department_id, tenant_id, type_key, display_name, "
                "status, created_at, updated_at "
                "from departments where department_id = ?",
                (resolved_department_id,),
            ).fetchone()
        return self._row_to_department(dict(row))

    def list_departments(self, tenant_id: str | None = None) -> list[Department]:
        """列出部门实例（聚合根）。

        ``tenant_id`` 缺省取单租户哨兵值；本 slice 不做跨租户隔离。
        """
        resolved_tenant_id = tenant_id if tenant_id is not None else DEFAULT_TENANT
        with self.database.connect() as connection:
            cursor = connection.execute(
                "select department_id, tenant_id, type_key, display_name, "
                "status, created_at, updated_at "
                "from departments where tenant_id = ? "
                "order by type_key, display_name",
                (resolved_tenant_id,),
            )
            rows = [dict(row) for row in cursor]
        return [self._row_to_department(row) for row in rows]

    def get_department(
        self, department_id: str, tenant_id: str | None = None
    ) -> Department | None:
        """按主键取部门实例；不存在返回 ``None``。

        ``tenant_id`` 缺省取单租户哨兵值。
        """
        resolved_tenant_id = tenant_id if tenant_id is not None else DEFAULT_TENANT
        with self.database.connect() as connection:
            row = connection.execute(
                "select department_id, tenant_id, type_key, display_name, "
                "status, created_at, updated_at "
                "from departments where department_id = ? and tenant_id = ?",
                (department_id, resolved_tenant_id),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_department(dict(row))

    # ── ADR-0017 S3 D4.impl (issue 059): 部门启用/停用真实落地 ──
    def set_departments_status_by_type(self, type_key: str, status: str) -> list[Department]:
        """按 type_key 批量更新部门实例的 status（enabled/disabled 真实落地）。

        供 D4.impl ``CompanyGovernance.apply_proposal`` 调用：将某 type_key 下所有
        部门实例（系统级，tenant_id='default'）置为 ``status``（'active' = 启用，
        'disabled' = 停用）。返回被更新的 Department 列表（可能为空）。不触外部 I/O、
        不接平台、不碰员工层。
        """
        resolved_status = status if status else "active"
        with self.database.connect() as connection:
            connection.execute(
                "update departments set status = ?, updated_at = current_timestamp "
                "where type_key = ? and tenant_id = ?",
                (resolved_status, type_key, DEFAULT_TENANT),
            )
            rows = connection.execute(
                "select department_id, tenant_id, type_key, display_name, "
                "status, created_at, updated_at "
                "from departments where type_key = ? and tenant_id = ?",
                (type_key, DEFAULT_TENANT),
            ).fetchall()
        return [self._row_to_department(dict(row)) for row in rows]

    # ── future hook：instantiate_department 已落实为委派 create_department ──
    def instantiate_department(self, *args: Any, **kwargs: Any) -> Department:
        """部门实例化（L5）：委派至 ``create_department`` 落库真实部门实例。

        D2.impl 不再 NotImplementedError——CEO 可从此处真正创建部门聚合根。
        保留 ``*args/**kwargs`` 弹性签名以兼容 reservation 时期的调用点形态。
        """
        return self.create_department(*args, **kwargs)

    # ── 禁止区 future hook（绝对保留，绝不落实）──
    def connect_platform(self, *args: Any, **kwargs: Any) -> None:
        """Future hook: 外部平台凭证接入（安全边界席领地）。本 slice 不实现。"""
        raise NotImplementedError(
            "connect_platform 为 D2.impl 禁止区 future hook，本 slice 不实现"
        )

    def manage_employees(self, *args: Any, **kwargs: Any) -> None:
        """Future hook: Employee CRUD（L2/L5）。本 reservation slice 不实现。"""
        raise NotImplementedError(
            "manage_employees 为 D2.impl 禁止区 future hook，本 slice 不实现"
        )

    # ── 内部辅助 ──
    @staticmethod
    def _parse_manifest_json(raw: str | None) -> dict[str, Any]:
        """将占位 manifest_json 解析为 dict；解析失败时回退为空对象。"""
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _row_to_type(self, row: dict[str, Any]) -> DepartmentType:
        # 占位 Manifest：字段为空结构，不消费 manifest_json 中的任何真实数据。
        dept_manifest = DepartmentManifest(
            type_key=row["type_key"],
            category=row["category"],
            manifest_schema_version=row.get("manifest_schema_version", "0.0"),
        )
        return DepartmentType(
            type_key=row["type_key"],
            category=row["category"],
            display_name=row["display_name"],
            description=row.get("description") or "",
            manifest=dept_manifest,
            manifest_schema_version=row.get("manifest_schema_version", "0.0"),
            is_system=bool(row.get("is_system", 1)),
        )

    @staticmethod
    def _row_to_department(row: dict[str, Any]) -> Department:
        """将 ``departments`` 表行映射为 ``Department`` 聚合根。"""
        return Department(
            department_id=row["department_id"],
            tenant_id=row["tenant_id"],
            type_key=row["type_key"],
            display_name=row["display_name"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
