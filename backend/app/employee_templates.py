from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any

from .database import Database
from .tenant_context import TenantContext


EMPLOYEE_AVATAR_PRESETS = frozenset(
    {
        "iris",
        "sage",
        "coral",
        "amber",
        "sky",
        "plum",
        "mint",
        "slate",
    }
)
MAX_EMPLOYEE_AVATAR_BYTES = 2 * 1024 * 1024
_AVATAR_ASSET_RE = re.compile(r"^asset:([0-9a-f]{64})\.(png|jpg|webp)$")
_AVATAR_MEDIA = {
    "image/png": ("png", lambda data: data.startswith(b"\x89PNG\r\n\x1a\n")),
    "image/jpeg": ("jpg", lambda data: data.startswith(b"\xff\xd8\xff")),
    "image/webp": (
        "webp",
        lambda data: len(data) >= 12 and data.startswith(b"RIFF") and data[8:12] == b"WEBP",
    ),
}

# Creation definitions only: the existing catalog and Company instances own
# persisted truth. Never use this list to repair headcount after bootstrap.
BUILTIN_EMPLOYEE_DEFINITIONS = (
    ("space.engineering", "空间工程部", "leadership", "空间工程负责人", "空间工程负责人", "目标理解、团队领导、CEO沟通、决策门、整合与交付责任"),
    ("space.engineering", "空间工程部", "industry_research", "行业研究专家", "行业研究专家", "行业、用户、竞品与经营实践研究；来源和证据"),
    ("space.engineering", "空间工程部", "operating_method", "经营方法专家", "经营方法专家", "经营模型、经营策略、工作方法与设计翻译输入"),
    ("space.engineering", "空间工程部", "spatial_design", "空间设计专家", "空间设计专家", "业务、工作空间、专业工作面、上下文与责任交互设计"),
    ("space.engineering", "空间工程部", "implementation", "搭建实施专家", "搭建实施专家", "工作空间包、配置、能力集成、安装与实施"),
    ("space.engineering", "空间工程部", "quality", "质量验证专家", "质量验证专家", "测试、证据验证、缺陷反馈与交付验收支持"),
    ("data.analytics", "数据分析部", "company_analysis", "公司经营分析师", "司衡", "公司经营分析、数据可信度、报告与证据、决策支持"),
)

# Bounded delivery-owner decision; identities do not grant execution capability.
PROFESSIONAL_TEAM_DEFINITIONS = {
    "content_growth": ("official.employee.content_growth.author", "内容创作负责人",
        "目标与合法账号上下文中的创作、事实与规格自检、Publishing交付准备与真实回执、Analytics口径与缺失事实复盘；自检不是独立审核"),
    "writing": ("official.employee.writing.author", "章节作者",
        "按作者正文与选文依据创作讨论、一致性与差异自检、建议及版本依据交付、问题与后续修改复盘；正式稿由作者手动决定"),
    "music": ("official.employee.music.author", "歌曲创作负责人",
        "按歌曲与合法材料创作讨论、版本与约束自检、候选与来源事实交付、方案与后续创作复盘；不授予音频生成或发行能力"),
}
PROFESSIONAL_TEAM_PACKAGES = {
    ("com.curis.local.writing-authoring", "0.1.0"): ("writing", "WRITING_CHAPTER_AUTHOR", "2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e"),
    ("com.curis.local.content-growth", "0.1.0"): ("content_growth", "CONTENT_GRAPHIC_AUTHOR", "aec85f973ca864f581c8fe6f800b68a1b9c23dc25ad5e194ca4e61e9edddcc0d"),
    ("com.curis.local.content-growth", "0.2.0"): ("content_growth", "CONTENT_AUTHOR", "90cc938b70d64a4888385ec40a6844879881409511e9544dec354ef91882a0a6"),
    ("com.curis.local.music", "0.2.0"): ("music", "MUSIC_SONG_AUTHOR", "cb05fd21e4237d046e20f0b96a81f6894e71caee95c2b0c6559b91ecf56ec802"),
}


def professional_team_contract(package_id, version, digest):
    match = PROFESSIONAL_TEAM_PACKAGES.get((package_id, version))
    if match is None:
        if package_id in {key[0] for key in PROFESSIONAL_TEAM_PACKAGES}:
            raise ValueError("Professional team package version is not approved")
        return None
    kind, author_key, expected_digest = match
    if digest != expected_digest:
        raise ValueError("Professional team package digest changed")
    template_id, name, responsibility = PROFESSIONAL_TEAM_DEFINITIONS[kind]
    contract = {"version": "1", "decisionSourceSHA256": "74225e91d143f877f708bd5b209bbffd989f2fe07f0f211fa7b926d12c445ce6",
        "packageId": package_id, "packageVersion": version, "packageDigest": digest,
        "templateId": template_id, "departmentType": kind, "displayName": name,
        "authorKey": author_key, "responsibility": responsibility,
        "leaderKey": "BUSINESS_LEADER", "leaderResponsibility": "接收业务目标、统筹责任与证据交付、向CEO沟通进展风险与下一步；权限成本和外部效果门交CEO决定",
        "coverage": ["CREATION", "SELF_CHECK", "DELIVERY", "RETROSPECTIVE"] + (["PUBLISHING", "ANALYTICS"] if kind == "content_growth" else [])}
    contract["sha256"] = hashlib.sha256(json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return contract


class EmployeeTemplateContract:
    """Phase-4 Workspace employee/department metadata service."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def materialize_professional_team_in_connection(self, connection, *, company_id,
            business_id, workspace_id, contract):
        from .resource_scope_policy import ResourceScopePolicy
        from .runtime.responsibility_routing import ResponsibilityRoutingRuntime
        tenant = TenantContext.current_tenant_id()
        expected = professional_team_contract(contract["packageId"], contract["packageVersion"], contract["packageDigest"])
        if expected is None or contract != expected or not connection.in_transaction:
            raise ValueError("Approved professional team requires its caller-owned transaction")
        scope = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant,
            company_id=company_id, scope_type="WORKSPACE", scope_ref=workspace_id)
        if scope["business_id"] != business_id:
            raise ValueError("Initial team Workspace is outside the Business")
        instance = connection.execute("select package_id,package_version,package_digest from workspace_package_instances "
            "where tenant_id=? and company_id=? and workspace_id=? and status='ACTIVE'",
            (tenant, company_id, workspace_id)).fetchall()
        if len(instance) != 1 or tuple(instance[0]) != (contract["packageId"], contract["packageVersion"], contract["packageDigest"]):
            raise ValueError("Initial team contract is outside the installed Package identity")
        template_id = contract["templateId"]
        values = (template_id, template_id.removeprefix("official.employee."), contract["displayName"],
                  contract["displayName"], contract["responsibility"], contract["departmentType"])
        connection.execute("insert or ignore into employee_templates(id,slug,name,role,responsibility,department_type,source,tenant_id) "
            "values (?,?,?,?,?,?,'official','platform')", values)
        template = connection.execute("select * from employee_templates where id=?", (template_id,)).fetchone()
        if (any(template[key] != value for key, value in zip(("id", "slug", "name", "role", "responsibility", "department_type"), values))
                or template["source"] != "official" or template["tenant_id"] != "platform" or not template["enabled"]
                or any(template[key] for key in ("persona_ref", "default_skill", "default_tool", "default_instructions"))
                or any(json.loads(template[key]) for key in ("default_capability_types_json", "default_model_policy_json", "default_workflow_step_types_json", "guardrails_json"))):
            raise ValueError("Professional Employee definition conflicts with the approved catalog")
        employee_id = f"emp-{uuid.uuid4()}"
        connection.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,created_from_template_id,name,role,status) "
            "values (?,?,?,'',?,?,?,?,'idle')", (employee_id, tenant, company_id, template_id, template_id, contract["displayName"], contract["displayName"]))
        def entity(entity_id, kind, status, data, workspace=None, owner=""):
            connection.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,owner_ref,lifecycle_status,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,?,?,?,?,?,'UNVERIFIED','MISSING',?,current_timestamp,current_timestamp)",
                (entity_id, tenant, kind, company_id, workspace, owner, status, json.dumps(data, ensure_ascii=False)))
        entity(employee_id, "AI_EMPLOYEE", "AVAILABLE", {"companyEmployeeRef": employee_id,
            "officialDefinitionRef": template_id, "name": contract["displayName"], "role": contract["displayName"]})
        assignments = []
        routing = ResponsibilityRoutingRuntime(self.database)
        for leader in (True, False):
            role_id = str(uuid.uuid4())
            key = contract["leaderKey"] if leader else contract["authorKey"]
            responsibility = contract["leaderResponsibility"] if leader else contract["responsibility"]
            entity(role_id, "ROLE_SLOT", "ASSIGNED", {"name": "业务负责人" if leader else contract["displayName"],
                "responsibility": responsibility, "officialDefinitionRef": template_id}, None if leader else workspace_id, employee_id)
            assignment = routing.create_assignment_in_connection(connection, company_id=company_id,
                scope_type="BUSINESS" if leader else "WORKSPACE", scope_ref=business_id if leader else workspace_id,
                workspace_id=None if leader else workspace_id, role_ref=role_id, employee_ref=employee_id,
                responsibility_key=key, responsibility=responsibility, is_leader=leader,
                output_contract={} if leader else {"coverage": contract["coverage"], "independentReview": False})
            assignments.append({"roleRef": role_id, "assignmentRef": assignment["entity_id"],
                "scopeType": "BUSINESS" if leader else "WORKSPACE", "scopeRef": business_id if leader else workspace_id})
        return {"contractVersion": contract["version"], "contractSHA256": contract["sha256"],
            "templateRef": template_id, "employeeRef": employee_id, "leaderRef": employee_id,
            "businessRef": business_id, "workspaceRef": workspace_id, "assignments": assignments,
            "coverage": contract["coverage"], "executionVerification": "UNVERIFIED"}

    def professional_team_state_in_connection(self, connection, *, company_id, business_id, workspace_id, contract):
        """Read current canonical arrangements; never repair a partial or disabled team."""
        tenant = TenantContext.current_tenant_id()
        rows = connection.execute(
            "select * from runtime_entities where tenant_id=? and company_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT' "
            "and (workspace_id=? or (json_extract(data_json,'$.scopeType')='BUSINESS' and json_extract(data_json,'$.scopeRef')=?)) order by entity_id",
            (tenant, company_id, workspace_id, business_id),
        ).fetchall()
        basis = [{"ref": row["entity_id"], "revision": json.loads(row["data_json"]).get("revision"),
                  "employee_ref": json.loads(row["data_json"]).get("employeeRef")} for row in rows]
        if not rows:
            return {"basis": basis, "team": None}
        if len(rows) != 2:
            raise ValueError("Existing team requires explicit arrangement review")
        assignments = [json.loads(row["data_json"]) for row in rows]
        expected = {(contract["leaderKey"], "BUSINESS", business_id), (contract["authorKey"], "WORKSPACE", workspace_id)}
        if {(a.get("responsibilityKey"), a.get("scopeType"), a.get("scopeRef")) for a in assignments} != expected:
            raise ValueError("Existing team responsibilities differ from the approved initial composition")
        if any(a.get("isLeader") is not (a["scopeType"] == "BUSINESS") for a in assignments):
            raise ValueError("Existing team leader arrangement requires review")
        refs = {a.get("employeeRef") for a in assignments}
        if len(refs) != 1 or not all(row["lifecycle_status"] == "ACTIVE" for row in rows):
            raise ValueError("Existing team is disabled or independently arranged")
        employee_ref = next(iter(refs))
        employee = connection.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type='AI_EMPLOYEE'",
            (tenant, company_id, employee_ref)).fetchone()
        if employee is None or employee["workspace_id"] not in (None, workspace_id) or employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
            raise ValueError("Current team Employee is unavailable")
        company_ref = json.loads(employee["data_json"]).get("companyEmployeeRef")
        person = connection.execute("select * from employee_instances where tenant_id=? and company_id=? and id=? and enabled=1 and deleted_at is null and status in ('idle','assigned')",
            (tenant, company_id, company_ref)).fetchone()
        if person is None:
            raise ValueError("Current team has no available canonical Company Employee")
        for row, assignment in zip(rows, assignments):
            role = connection.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type='ROLE_SLOT'",
                (tenant, company_id, assignment.get("roleRef"))).fetchone()
            required_workspace = workspace_id if assignment["scopeType"] == "WORKSPACE" else None
            if role is None or role["workspace_id"] != required_workspace or row["workspace_id"] != required_workspace or role["lifecycle_status"] not in {"ASSIGNED", "OPERATING"}:
                raise ValueError("Current team Role is unavailable or out of scope")
            for relation, target in [("ASSIGNED_EMPLOYEE", employee_ref), ("USES_ROLE", assignment["roleRef"])]:
                links = connection.execute("select target_id from runtime_links where tenant_id=? and company_id=? and source_id=? and relation=?",
                    (tenant, company_id, row["entity_id"], relation)).fetchall()
                if len(links) != 1 or links[0][0] != target:
                    raise ValueError("Current team canonical links differ from its Assignment")
        return {"basis": basis, "team": {"employeeRef": employee_ref, "companyEmployeeRef": company_ref, "name": person["name"],
            "businessRef": business_id, "workspaceRef": workspace_id, "assignments": basis, "executionVerification": "UNVERIFIED"}}

    def materialize_builtin_organization(self, connection, *, company_id: str) -> None:
        """Called only in the fresh Company transaction, never on startup/retry.

        Reuses catalog, Employee and Runtime tables. No execution authorization
        is implied by materialization, and no capability binding is created.
        """
        tenant_id = TenantContext.current_tenant_id()
        if connection.execute(
            "select 1 from companies where tenant_id=? and company_id=?",
            (tenant_id, company_id),
        ).fetchone() is None:
            raise ValueError("Built-in organization requires its Company transaction")
        departments = {}
        for kind, department_name, key, role, name, responsibility in BUILTIN_EMPLOYEE_DEFINITIONS:
            template_id = f"official.employee.{kind}.{key}"
            department_template = f"official.department.{kind}"
            connection.execute(
                "insert or ignore into employee_templates(id, slug, name, role, responsibility, "
                "department_type, source, tenant_id) values (?, ?, ?, ?, ?, ?, 'official', 'platform')",
                (template_id, f"{kind}.{key}", name, role, responsibility, kind),
            )
            template = connection.execute(
                "select * from employee_templates where id=?", (template_id,),
            ).fetchone()
            if (template["source"] != "official" or template["tenant_id"] != "platform"
                    or template["department_type"] != kind or not template["enabled"]):
                raise ValueError("Built-in Employee definition conflicts with the official catalog")
            if kind not in departments:
                connection.execute(
                    "insert or ignore into department_types(type_key, category, display_name, is_system) "
                    "values (?, 'company', ?, 1)", (kind, department_name),
                )
                connection.execute(
                    "insert or ignore into department_templates(id, name, department_type, source, tenant_id) "
                    "values (?, ?, ?, 'official', 'platform')",
                    (department_template, department_name, kind),
                )
                department_id = f"dept-{uuid.uuid4()}"
                departments[kind] = department_id
                connection.execute(
                    "insert into department_instances(id, tenant_id, company_id, template_id, name, "
                    "department_type, created_from_template_id) values (?, ?, ?, ?, ?, ?, ?)",
                    (department_id, tenant_id, company_id, department_template, department_name, kind, department_template),
                )
            department_id = departments[kind]
            employee_id, role_id, assignment_id = (str(uuid.uuid4()) for _ in range(3))
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, "
                "created_from_template_id, name, role, status) values (?, ?, ?, ?, ?, ?, ?, ?, 'idle')",
                (employee_id, tenant_id, company_id, department_id, template_id, template_id, template["name"], template["role"]),
            )
            assignment = {
                "scopeType": "DEPARTMENT", "scopeRef": department_id,
                "roleRef": role_id, "employeeRef": employee_id,
                "responsibilityKey": f"{kind}.{key}", "responsibility": template["responsibility"],
                "isLeader": key == "leadership", "capabilityBindingRefs": [],
                "inputContract": {}, "outputContract": {}, "revision": 1,
            }
            for entity_id, entity_type, status, owner, data in (
                (employee_id, "AI_EMPLOYEE", "AVAILABLE", "", {
                    "companyEmployeeRef": employee_id, "officialDefinitionRef": template_id,
                    "departmentRef": department_id,
                }),
                (role_id, "ROLE_SLOT", "ASSIGNED", employee_id, {
                    "name": template["role"], "responsibility": template["responsibility"],
                    "officialDefinitionRef": template_id,
                }),
                (assignment_id, "RESPONSIBILITY_ASSIGNMENT", "ACTIVE", employee_id, assignment),
            ):
                connection.execute(
                    "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, "
                    "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                    "values (?, ?, ?, ?, ?, ?, 'UNVERIFIED', 'MISSING', ?, current_timestamp, current_timestamp)",
                    (entity_id, tenant_id, entity_type, company_id, owner, status, json.dumps(data, ensure_ascii=False)),
                )
            for relation, target in (("ASSIGNED_EMPLOYEE", employee_id), ("USES_ROLE", role_id)):
                connection.execute(
                    "insert into runtime_links(link_id, tenant_id, company_id, source_id, relation, target_id, created_at) "
                    "values (?, ?, ?, ?, ?, ?, current_timestamp)",
                    (str(uuid.uuid4()), tenant_id, company_id, assignment_id, relation, target),
                )
            if key == "leadership":
                connection.execute(
                    "update department_instances set manager_employee_id=? where tenant_id=? and id=?",
                    (employee_id, tenant_id, department_id),
                )

    def list_employee_templates(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        return {
            "tenant_id": tenant_id,
            "employee_templates": self.database.list_employee_templates(tenant_id),
        }

    def list_department_templates(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        return {
            "tenant_id": tenant_id,
            "department_templates": self.database.list_department_templates(tenant_id),
        }

    def list_workflow_templates(self) -> dict[str, Any]:
        return {
            "workflow_templates": [
                {
                    "id": "official.workflow.software_rnd_minimal",
                    "slug": "software-rnd-minimal",
                    "name": "研发部最小 SOP",
                    "department_type": "software_rnd",
                    "process_type": "sequential",
                    "source": "official",
                    "enabled": True,
                    "step_templates": [
                        "requirement_understanding",
                        "task_breakdown",
                        "architecture_design",
                        "coding",
                        "testing",
                        "report",
                    ],
                }
            ]
        }

    def create_department_instance(
        self,
        *,
        template_id: str,
        name: str,
        company_id: str | None = None,
        enabled_employee_template_ids: list[str] | None = None,
        enabled: bool = True,
        manager_employee_id: str | None = None,
        mission: str = "",
        status: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        template = self._get_department_template(template_id, tenant_id)
        if template is None or not template["enabled"]:
            raise ValueError("department template is not available")
        # Self-use v1：允许已注册的部门类型（含新增 tech.rd / content.growth）
        # 与历史 software_rnd（既有 dt_engineering 兼容）。department_types
        # 是类型目录的单一真相源，不再硬编码单一值。
        allowed = {row["type_key"] for row in self.database.list_department_types()}
        allowed.add("software_rnd")  # 历史 RD 类型，向下兼容
        if template["department_type"] not in allowed:
            raise ValueError("department type is not registered in department_types")
        resolved_company_id = self._resolve_company_id(company_id)
        if manager_employee_id:
            self._validate_department_manager(resolved_company_id, None, manager_employee_id)
        status = status or ("active" if enabled else "disabled")
        if status not in {"draft", "active", "disabled", "archived"}:
            raise ValueError("department status must be draft, active, disabled, or archived")
        selected_templates = enabled_employee_template_ids or template["default_employee_templates"]
        allowed_templates = {item["id"] for item in self.database.list_employee_templates(tenant_id)}
        if any(template_id not in allowed_templates for template_id in selected_templates):
            raise ValueError("enabled_employee_template_ids must reference available employee templates")
        department_id = f"dept-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into department_instances (
                  id, tenant_id, company_id, template_id, name, department_type,
                  manager_employee_id, mission, status, created_from_template_id,
                  enabled_employee_template_ids_json, enabled, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
                """,
                (
                    department_id,
                    tenant_id,
                    resolved_company_id,
                    template["id"],
                    name or template["name"],
                    template["department_type"],
                    manager_employee_id,
                    mission or "",
                    status,
                    template["id"],
                    json.dumps(selected_templates, ensure_ascii=False),
                    1 if enabled and status == "active" else 0,
                ),
            )
        return self.get_department_instance(department_id)

    def list_department_instances(self, company_id: str | None = None) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        query = "select * from department_instances where tenant_id = ? and deleted_at is null"
        params: list[str] = [tenant_id]
        if company_id:
            self._assert_company_exists(company_id)
            query += " and company_id = ?"
            params.append(company_id)
        query += " order by created_at desc"
        with self.database.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return {"tenant_id": tenant_id, "departments": [self._department_instance_from_row(row) for row in rows]}

    def get_department_instance(self, department_id: str) -> dict[str, Any] | None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from department_instances where tenant_id = ? and id = ?"
                " and deleted_at is null",
                (tenant_id, department_id),
            ).fetchone()
        return None if row is None else self._department_instance_from_row(row)

    def ensure_engineering_department(self, company_id: str) -> dict[str, Any]:
        self._assert_company_exists(company_id)
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from department_instances
                where tenant_id = ? and company_id = ? and department_type = 'software_rnd'
                order by created_at asc limit 1
                """,
                (tenant_id, company_id),
            ).fetchone()
        if row is not None:
            return self._department_instance_from_row(row)
        return self.create_department_instance(
            template_id="official.department.software_rnd",
            company_id=company_id,
            name="Engineering Department",
        )

    def update_department_instance(self, department_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        department = self.get_department_instance(department_id)
        if department is None:
            raise KeyError("department not found")
        updates: dict[str, Any] = {}
        if "name" in changes and changes["name"] is not None:
            name = str(changes["name"]).strip()
            if not name:
                raise ValueError("department name is required")
            updates["name"] = name
        if "mission" in changes and changes["mission"] is not None:
            updates["mission"] = str(changes["mission"]).strip()
        if "manager_employee_id" in changes:
            manager_employee_id = changes["manager_employee_id"]
            if manager_employee_id:
                self._validate_department_manager(department["company_id"], department_id, manager_employee_id)
            updates["manager_employee_id"] = manager_employee_id
        if "status" in changes and changes["status"] is not None:
            status = str(changes["status"])
            if status not in {"draft", "active", "disabled", "archived"}:
                raise ValueError("department status must be draft, active, disabled, or archived")
            updates["status"] = status
            updates["enabled"] = 1 if status == "active" else 0
        if not updates:
            return department
        assignments = ", ".join(f"{field} = ?" for field in updates)
        with self.database.connect() as connection:
            connection.execute(
                f"update department_instances set {assignments}, updated_at = current_timestamp "
                "where tenant_id = ? and id = ?",
                (*updates.values(), TenantContext.current_tenant_id(), department_id),
            )
        return self.get_department_instance(department_id) or department

    def update_employee_instance(self, employee_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            raise KeyError("employee not found")
        updates: dict[str, Any] = {}
        if "name" in changes and changes["name"] is not None:
            name = str(changes["name"]).strip()
            if not name:
                raise ValueError("employee name is required")
            updates["name"] = name
        if "instructions_override" in changes:
            updates["instructions_override"] = str(changes["instructions_override"]).strip()
        status_provided = "status" in changes and changes["status"] is not None
        enabled_provided = "enabled" in changes and changes["enabled"] is not None
        if status_provided:
            status = str(changes["status"])
            if status not in {"idle", "assigned", "disabled"}:
                raise ValueError("status must be idle, assigned, or disabled")
            updates["status"] = status
            updates["enabled"] = 1 if status != "disabled" else 0
        elif enabled_provided:
            enabled = bool(changes["enabled"])
            updates["enabled"] = 1 if enabled else 0
            if not enabled:
                updates["status"] = "disabled"
            elif employee.get("status") == "disabled":
                updates["status"] = "idle"
        if not updates:
            return employee
        assignments = ", ".join(f"{field} = ?" for field in updates)
        with self.database.connect() as connection:
            connection.execute(
                f"update employee_instances set {assignments} "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (*updates.values(), TenantContext.current_tenant_id(), employee_id),
            )
        return self.get_employee_instance(employee_id) or employee

    def delete_employee_instance(self, employee_id: str) -> None:
        tenant_id = TenantContext.current_tenant_id()
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            raise KeyError("employee not found")
        # 校验员工不是任何部门的 manager_employee_id
        with self.database.connect() as connection:
            mgr_row = connection.execute(
                "select 1 from department_instances "
                "where tenant_id = ? and deleted_at is null and manager_employee_id = ?",
                (tenant_id, employee_id),
            ).fetchone()
        if mgr_row is not None:
            raise ValueError("employee is a department manager; reassign first")
        with self.database.connect() as connection:
            connection.execute(
                "update employee_instances set deleted_at = current_timestamp, enabled = 0 "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (tenant_id, employee_id),
            )
            connection.execute(
                "delete from employee_affiliations "
                "where tenant_id = ? and employee_id = ?",
                (tenant_id, employee_id),
            )

    def delete_department_instance(self, department_id: str) -> None:
        tenant_id = TenantContext.current_tenant_id()
        department = self.get_department_instance(department_id)
        if department is None:
            raise KeyError("department not found")
        # 非空守卫（ADR-0017 / Q3）：禁止删除非空部门。
        # 检查 3 个来源：在职员工（employee_instances）、多归属（employee_affiliations）、项目（projects）。
        with self.database.connect() as connection:
            emp_count = connection.execute(
                "select count(*) from employee_instances "
                "where tenant_id = ? and deleted_at is null and enabled = 1 and department_id = ?",
                (tenant_id, department_id),
            ).fetchone()[0]
            aff_count = connection.execute(
                "select count(*) from employee_affiliations "
                "where tenant_id = ? and department_id = ?",
                (tenant_id, department_id),
            ).fetchone()[0]
            proj_count = connection.execute(
                "select count(*) from projects where tenant_id = ? and department_id = ?",
                (tenant_id, department_id),
            ).fetchone()[0]
        if emp_count or aff_count or proj_count:
            # 前端据该 detail 二次确认 + 提示先转移/清空。
            raise ValueError(
                f"department not empty: {emp_count} active employees, "
                f"{aff_count} affiliations, {proj_count} projects"
            )
        with self.database.connect() as connection:
            connection.execute(
                "update department_instances set deleted_at = current_timestamp, enabled = 0 "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (tenant_id, department_id),
            )

    def create_employee_instance(
        self,
        *,
        department_id: str | None,
        template_id: str,
        name: str,
        company_id: str | None = None,
        avatar_ref: str = "",
        instructions_override: str = "",
        status: str = "idle",
        enabled: bool = True,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        department = self.get_department_instance(department_id) if department_id else None
        if department_id and (department is None or not department["enabled"]):
            raise ValueError("department instance is not available")
        template = self._get_employee_template(template_id, tenant_id)
        if template is None or not template["enabled"]:
            raise ValueError("employee template is not available")
        if department and template["department_type"] != department["department_type"]:
            raise ValueError("employee template department_type does not match department")
        if status not in {"idle", "assigned", "disabled"}:
            raise ValueError("status must be idle, assigned, or disabled")
        avatar_ref = self._normalize_avatar_ref(avatar_ref)
        # Gate E：从官方模板全行快照 persona_ref / default_skill / default_tool
        # （list_employee_templates 的只读投影不含这 3 列，需走 get_employee_template_row）。
        full_template = self.database.get_employee_template_row(template_id) or {}
        persona_ref = full_template.get("persona_ref", "") or ""
        default_skill = full_template.get("default_skill", "") or ""
        default_tool = full_template.get("default_tool", "") or ""
        employee_id = f"emp-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into employee_instances (
                  id, tenant_id, company_id, department_id, template_id, name,
                  created_from_template_id, role, avatar_ref, instructions_override, status, enabled,
                  persona_ref, default_skill, default_tool
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    tenant_id,
                    self._resolve_employee_company_id(
                        company_id,
                        department["company_id"] if department else self._resolve_company_id(company_id),
                    ),
                    department_id or "",
                    template["id"],
                    name or template["name"],
                    template["id"],
                    template["role"],
                    avatar_ref,
                    instructions_override or "",
                    status,
                    1 if enabled else 0,
                    persona_ref,
                    default_skill,
                    default_tool,
                ),
            )
        return self.get_employee_instance(employee_id)

    def save_employee_avatar(
        self, employee_id: str, media_type: str, payload: bytes,
    ) -> dict[str, Any]:
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            raise KeyError("employee not found")
        if not payload:
            raise ValueError("avatar file is empty")
        if len(payload) > MAX_EMPLOYEE_AVATAR_BYTES:
            raise ValueError("avatar file is too large")
        media = _AVATAR_MEDIA.get(media_type.lower().split(";", 1)[0].strip())
        if media is None or not media[1](payload):
            raise ValueError("avatar file type is not supported")

        extension = media[0]
        digest = hashlib.sha256(payload).hexdigest()
        target = self._avatar_directory(employee_id) / f"{digest}.{extension}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target_was_present = target.is_file()
        temporary = target.with_suffix(f".{extension}.tmp-{uuid.uuid4().hex}")
        try:
            if not target_was_present:
                with temporary.open("xb") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, target)
            avatar_ref = f"asset:{digest}.{extension}"
            with self.database.connect() as connection:
                connection.execute(
                    "update employee_instances set avatar_ref=? "
                    "where tenant_id=? and id=? and deleted_at is null",
                    (avatar_ref, TenantContext.current_tenant_id(), employee_id),
                )
        except Exception:
            temporary.unlink(missing_ok=True)
            if not target_was_present:
                target.unlink(missing_ok=True)
            raise
        return self.get_employee_instance(employee_id) or employee

    def get_employee_avatar_asset(self, employee_id: str) -> tuple[Path, str] | None:
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            raise KeyError("employee not found")
        match = _AVATAR_ASSET_RE.fullmatch(str(employee.get("avatar_ref") or ""))
        if match is None:
            return None
        extension = match.group(2)
        path = self._avatar_directory(employee_id) / f"{match.group(1)}.{extension}"
        if not path.is_file():
            return None
        return path, {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}[extension]

    @staticmethod
    def _normalize_avatar_ref(value: str) -> str:
        avatar_ref = str(value or "").strip()
        if not avatar_ref:
            return ""
        if avatar_ref.startswith("preset:") and avatar_ref.removeprefix("preset:") in EMPLOYEE_AVATAR_PRESETS:
            return avatar_ref
        raise ValueError("avatar preset is not available")

    def _avatar_directory(self, employee_id: str) -> Path:
        tenant_key = hashlib.sha256(TenantContext.current_tenant_id().encode()).hexdigest()[:20]
        employee_key = hashlib.sha256(employee_id.encode()).hexdigest()[:24]
        return Path(self.database.path).resolve().parent / "assets" / "employee-avatars" / tenant_key / employee_key

    def list_employee_instances(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from employee_instances where tenant_id = ? and deleted_at is null"
                " order by created_at desc",
                (tenant_id,),
            ).fetchall()
        return {"tenant_id": tenant_id, "employees": [self._employee_instance_from_row(row) for row in rows]}

    def get_employee_instance(self, employee_id: str) -> dict[str, Any] | None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from employee_instances where tenant_id = ? and id = ?"
                " and deleted_at is null",
                (tenant_id, employee_id),
            ).fetchone()
        return None if row is None else self._employee_instance_from_row(row)

    def default_employee_for_task(self, company_id: str | None = None) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        company_clause = " and company_id = ?" if company_id else ""
        params: list[str] = [tenant_id]
        if company_id:
            params.append(company_id)
        with self.database.connect() as connection:
            row = connection.execute(
                f"""
                select * from employee_instances
                where tenant_id = ? and enabled = 1 and role = 'tech_lead'{company_clause}
                order by created_at asc limit 1
                """,
                params,
            ).fetchone()
        if row is not None:
            return self._employee_instance_from_row(row)
        return {
            "id": None,
            "name": "Tech Lead",
            "role": "tech_lead",
            "enabled": True,
        }

    def _professional_execution_context(self, connection, employee):
        """Validate existing canonical arrangements; never materialize or grant here."""
        from .resource_scope_policy import ResourceScopePolicy
        if employee["template_id"] not in {row[0] for row in PROFESSIONAL_TEAM_DEFINITIONS.values()}:
            return []
        tenant, company = TenantContext.current_tenant_id(), employee["company_id"]
        packages = connection.execute(
            "select workspace_id,package_id,package_version,package_digest from workspace_package_instances "
            "where tenant_id=? and company_id=? and status='ACTIVE' order by workspace_id",
            (tenant, company),
        ).fetchall()
        proofs = []
        for package in packages:
            try:
                contract = professional_team_contract(package["package_id"], package["package_version"], package["package_digest"])
                if not contract or contract["templateId"] != employee["template_id"]:
                    continue
                template = connection.execute("select * from employee_templates where id=?",
                                              (employee["template_id"],)).fetchone()
                expected = {"source": "official", "tenant_id": "platform", "name": contract["displayName"],
                            "role": contract["displayName"], "responsibility": contract["responsibility"],
                            "department_type": contract["departmentType"]}
                if (template is None or not template["enabled"]
                        or any(template[key] != value for key, value in expected.items())
                        or employee["created_from_template_id"] != employee["template_id"]):
                    continue
                scope = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant,
                    company_id=company, scope_type="WORKSPACE", scope_ref=package["workspace_id"])
                state = self.professional_team_state_in_connection(connection, company_id=company,
                    business_id=scope["business_id"], workspace_id=package["workspace_id"], contract=contract)
                if state["team"] and state["team"]["companyEmployeeRef"] == employee["id"]:
                    proofs.append({"workspace_id": package["workspace_id"], "contract": contract["sha256"],
                                   "basis": state["basis"]})
            except ValueError:
                continue
        return proofs

    def _execution_permission(self, connection, employee):
        from .capability_authorizer import CapabilityAuthorizer
        tenant = TenantContext.current_tenant_id()
        template = connection.execute("select allowed_effect_classes_json from employee_templates where id=?",
                                      (employee["template_id"],)).fetchone()
        raw_template = template[0] if template else None
        effective = CapabilityAuthorizer(self.database).allowed_classes_for_employee(employee["id"], connection=connection)
        proofs = self._professional_execution_context(connection, employee)
        company = connection.execute("select ceo_id,status from companies where tenant_id=? and company_id=?",
                                    (tenant, employee["company_id"])).fetchone()
        actor = TenantContext.current_identity()
        owner = bool(company and company["status"] in {"draft", "active"}
            and actor.get("role") in {"owner", "ceo"} and actor.get("ceo_id") == company["ceo_id"]
            and actor.get("company_id") in {None, "", employee["company_id"]})
        rows = connection.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? "
                                  "order by priority,capability_type,capability_id,id", (tenant, employee["id"])).fetchall()
        basis = {"tenant": tenant, "employee": {key: employee[key] for key in
                 ("id", "company_id", "template_id", "allowed_effect_classes_json", "enabled", "status")},
                 "template": raw_template, "company": dict(company) if company else None,
                 "proofs": proofs, "bindings": [dict(row) for row in rows]}
        revision = hashlib.sha256(json.dumps(basis, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        template_exec = "exec" in CapabilityAuthorizer._parse(raw_template)
        return {"company_id": employee["company_id"], "employee_id": employee["id"],
                "manageable": bool(owner and proofs and effective is not None),
                "enabled": bool(effective is not None and "exec" in effective),
                "effective_classes": sorted(effective) if effective is not None else None,
                "can_revoke": bool(effective is not None and (effective - {"exec"} or not template_exec)),
                "revision": revision}

    def _write_capability_bindings(self, connection, employee, normalized):
        tenant = TenantContext.current_tenant_id()
        existing = connection.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=?",
                                      (tenant, employee["id"])).fetchall()
        key = lambda row: (row["capability_source"], row["capability_type"], row["capability_id"])
        if len({key(item) for item in normalized}) != len(normalized):
            raise ValueError("Duplicate employee capability binding")
        retained = {key(row): row for row in existing}
        connection.execute("delete from employee_capability_bindings where tenant_id=? and employee_id=?",
                           (tenant, employee["id"]))
        connection.executemany(
            "insert into employee_capability_bindings (id,tenant_id,employee_id,employee_template_id,"
            "capability_source,capability_type,capability_id,priority,enabled,created_at) "
            "values (?,?,?,?,?,?,?,?,?,coalesce(?,current_timestamp))",
            [(retained[key(item)]["id"] if key(item) in retained else item["id"],
              tenant, employee["id"], employee["template_id"], *key(item), item["priority"],
              1 if item["enabled"] else 0, retained[key(item)]["created_at"] if key(item) in retained else None)
             for item in normalized],
        )

    def add_employee_agent_binding(self, employee_id: str, company_id: str, capability_id: str) -> dict[str, Any]:
        """Append one Agent under the existing write lock, preserving other writers' rows."""
        from .capability_authorizer import CapabilityAuthorizer
        tenant = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute("select * from employee_instances where tenant_id=? and company_id=? "
                "and id=? and enabled=1 and deleted_at is null and status in ('idle','assigned')",
                (tenant, company_id, employee_id)).fetchone()
            if row is None:
                raise ValueError("employee instance is not available in this company")
            employee = dict(row)
            item = self._normalize_binding(employee, {"capability_source": "tenant_private",
                "capability_type": "agent", "capability_id": capability_id, "priority": 100, "enabled": True})
            allowed, _ = CapabilityAuthorizer(self.database).authorize(employee_id, "agent", capability_id, connection=connection)
            if not allowed:
                raise ValueError("capability is not authorized for this position")
            existing = connection.execute("select * from employee_capability_bindings where tenant_id=? "
                "and employee_id=? and capability_source='tenant_private' and capability_type='agent' and capability_id=?",
                (tenant, employee_id, capability_id)).fetchall()
            if len(existing) > 1:
                raise ValueError("Duplicate employee capability binding")
            if existing and not existing[0]["enabled"]:
                raise ValueError("已有绑定已禁用，请在员工资料中明确处理；不会自动重新启用。")
            if not existing:
                connection.execute("insert into employee_capability_bindings "
                    "(id,tenant_id,employee_id,employee_template_id,capability_source,capability_type,capability_id,priority,enabled) "
                    "values (?,?,?,?,'tenant_private','agent',?,100,1)",
                    (item["id"], tenant, employee_id, employee["template_id"], capability_id))
        return self.list_employee_capability_bindings(employee_id)

    def set_employee_capability_bindings(self, employee_id: str, bindings: list[dict[str, Any]],
                                        *, execution_permission=None) -> dict[str, Any]:
        from .capability_authorizer import CapabilityAuthorizer
        from .catalog_constants import effect_class_for_capability
        tenant = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute("select * from employee_instances where tenant_id=? and id=? and deleted_at is null",
                                     (tenant, employee_id)).fetchone()
            if row is None:
                raise ValueError("employee instance is not available")
            employee = dict(row)
            normalized = [self._normalize_binding(employee, item) for item in bindings]
            if execution_permission is not None:
                permission = self._execution_permission(connection, employee)
                if (not permission["manageable"]
                        or execution_permission.get("company_id") != employee["company_id"]
                        or execution_permission.get("expected_revision") != permission["revision"]
                        or type(execution_permission.get("enabled")) is not bool):
                    raise ValueError("员工执行授权不可修改或资料已变化，请重新读取当前配置。")
                classes = set(permission["effective_classes"])
                if execution_permission["enabled"]:
                    classes.add("exec")
                else:
                    if not permission["can_revoke"]:
                        raise ValueError("岗位模板仍授予执行许可，无法以空实例覆盖撤销；请先处理岗位授权。")
                    classes.discard("exec")
                    old = connection.execute("select capability_source,capability_type,capability_id from "
                        "employee_capability_bindings where tenant_id=? and employee_id=?", (tenant, employee_id)).fetchall()
                    keys = {tuple(item) for item in old}
                    for item in normalized:
                        if (effect_class_for_capability(item["capability_type"], item["capability_id"]) == "exec"
                                and (item["capability_source"], item["capability_type"], item["capability_id"]) not in keys):
                            raise ValueError("撤销执行许可时不能新增执行类能力。")
                    # Explicit revoke also removes execution bindings; other classes keep their state.
                    normalized = [item for item in normalized
                        if effect_class_for_capability(item["capability_type"], item["capability_id"]) != "exec"]
                connection.execute("update employee_instances set allowed_effect_classes_json=? "
                    "where tenant_id=? and company_id=? and id=?",
                    (json.dumps(sorted(classes)), tenant, employee["company_id"], employee_id))
            # All writers, including legacy API/internal callers, recheck inside this transaction.
            authorizer = CapabilityAuthorizer(self.database)
            for item in normalized:
                allowed, _ = authorizer.authorize(employee_id, item["capability_type"], item["capability_id"], connection=connection)
                if not allowed:
                    raise ValueError("capability is not authorized for this position")
            self._write_capability_bindings(connection, employee, normalized)
        return self.list_employee_capability_bindings(employee_id)

    def require_agent_execution_permission(self, employee_id, company_id):
        """Re-read immediately before real work and on running/continuation checks."""
        from .capability_authorizer import CapabilityAuthorizer
        with self.database.connect() as connection:
            row = connection.execute("select template_id from employee_instances where tenant_id=? and company_id=? "
                "and id=? and enabled=1 and deleted_at is null and status in ('idle','assigned')",
                (TenantContext.current_tenant_id(), company_id, employee_id)).fetchone()
            authorizer = CapabilityAuthorizer(self.database)
            if (row is None or authorizer.allowed_classes_for_employee(employee_id, connection=connection) is None
                    or not authorizer.authorize(employee_id, "agent", connection=connection)[0]):
                raise ValueError("员工当前没有有效执行许可，请核对员工授权。")

    def list_employee_capability_bindings(self, employee_id: str) -> dict[str, Any]:
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            raise ValueError("employee instance is not available")
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin")
            rows = connection.execute(
                """
                select * from employee_capability_bindings
                where tenant_id = ? and employee_id = ?
                order by priority, capability_type, capability_id
                """,
                (tenant_id, employee_id),
            ).fetchall()
            # Read the instance again in this same snapshot; a stale UI cannot authorize a write.
            current = connection.execute("select * from employee_instances where tenant_id=? and id=? and deleted_at is null",
                                         (tenant_id, employee_id)).fetchone()
            if current is None:
                raise ValueError("employee instance is not available")
            permission = self._execution_permission(connection, dict(current))
        return {"tenant_id": tenant_id, "employee_id": employee_id,
                "bindings": [self._binding_from_row(row) for row in rows], "execution_permission": permission}

    def list_employee_tool_bindings(self, employee_id: str) -> dict[str, Any]:
        bindings = self.list_employee_capability_bindings(employee_id)["bindings"]
        tools = [
            {**item, "tool_runtime_id": f"{item['capability_source']}:{item['capability_id']}"}
            for item in bindings
            if item["capability_type"] == "tool"
        ]
        return {"tenant_id": TenantContext.current_tenant_id(), "employee_id": employee_id, "bindings": tools}

    def set_employee_tool_bindings(self, employee_id: str, bindings: list[dict[str, Any]]) -> dict[str, Any]:
        existing = self.list_employee_capability_bindings(employee_id)["bindings"]
        normalized_tools = [
            {
                "capability_source": item.get("capability_source"),
                "capability_type": "tool",
                "capability_id": item.get("capability_id"),
                "priority": item.get("priority", 100),
                "enabled": item.get("enabled", True),
            }
            for item in bindings
        ]
        retained = [item for item in existing if item["capability_type"] != "tool"]
        self.set_employee_capability_bindings(employee_id, [*retained, *normalized_tools])
        return self.list_employee_tool_bindings(employee_id)

    def preferred_capability_for_employee(self, employee_id: str) -> dict[str, Any] | None:
        employee = self.get_employee_instance(employee_id)
        if employee is None or not employee["enabled"]:
            raise ValueError("employee instance is not available")
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from employee_capability_bindings
                where tenant_id = ? and employee_id = ? and enabled = 1
                order by priority, capability_type, capability_id
                limit 1
                """,
                (tenant_id, employee_id),
            ).fetchone()
        return None if row is None else self._binding_from_row(row)

    def _normalize_binding(self, employee: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
        source = item.get("capability_source")
        capability_type = item.get("capability_type")
        capability_id = item.get("capability_id")
        if source not in {"official", "tenant_private"}:
            raise ValueError("capability_source must be official or tenant_private")
        if capability_type not in {"model", "agent", "tool", "connector"}:
            raise ValueError("capability_type must be model, agent, tool, or connector")
        if not capability_id:
            raise ValueError("capability_id is required")
        if source == "official":
            official_ids = {
                capability["capability_key"]
                for capability in self.database.list_catalog_capabilities()
                if capability["type"] == capability_type
            }
            if capability_type == "tool":
                official_ids.update(tool["name"] for tool in self.database_tools())
            if capability_id not in official_ids:
                raise ValueError("official capability is not available")
        if source == "tenant_private":
            private = self.database.get_tenant_private_capability(
                TenantContext.current_tenant_id(), capability_type, capability_id
            )
            if private is None or private.get("status") != "active":
                raise ValueError("tenant_private capability is not available")
        return {
            "id": item.get("id") or f"bind-{uuid.uuid4()}",
            "capability_source": source,
            "capability_type": capability_type,
            "capability_id": capability_id,
            "priority": int(item.get("priority", 100) or 100),
            "enabled": bool(item.get("enabled", True)),
        }

    def database_tools(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select name, type, description, entry from tools order by name").fetchall()
        return [dict(row) for row in rows]

    def _resolve_company_id(self, company_id: str | None) -> str:
        if company_id and company_id != "local-demo-company":
            self._assert_company_exists(company_id)
            return company_id
        from .company_project_runtime import CompanyProjectRuntime

        companies = CompanyProjectRuntime(self.database).list_companies()["companies"]
        return next(item["company_id"] for item in companies if item["is_default"])

    def _assert_company_exists(self, company_id: str) -> None:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from companies where tenant_id = ? and company_id = ?",
                (TenantContext.current_tenant_id(), company_id),
            ).fetchone()
        if row is None:
            raise ValueError("company is not available")

    @staticmethod
    def _resolve_employee_company_id(company_id: str | None, department_company_id: str) -> str:
        if company_id and company_id not in {"local-demo-company", department_company_id}:
            raise ValueError("employee company_id must match the department company")
        return department_company_id

    def _validate_department_manager(
        self,
        company_id: str,
        department_id: str | None,
        employee_id: str,
    ) -> None:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id, department_id from employee_instances where tenant_id = ? and id = ? and enabled = 1",
                (TenantContext.current_tenant_id(), employee_id),
            ).fetchone()
        if row is None or row["company_id"] != company_id:
            raise ValueError("department manager must be an enabled employee of the company")
        if department_id and row["department_id"] != department_id:
            raise ValueError("department manager must belong to the department")

    def _get_employee_template(self, template_id: str, tenant_id: str) -> dict[str, Any] | None:
        templates = self.database.list_employee_templates(tenant_id, include_inactive=True)
        return next((item for item in templates if item["id"] == template_id), None)

    def _get_department_template(self, template_id: str, tenant_id: str) -> dict[str, Any] | None:
        templates = self.database.list_department_templates(tenant_id, include_inactive=True)
        return next((item for item in templates if item["id"] == template_id), None)

    @staticmethod
    def _department_instance_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["enabled_employee_template_ids"] = json.loads(item.pop("enabled_employee_template_ids_json") or "[]")
        item["enabled"] = bool(item["enabled"])
        # P1: DB 值为 NULL 时直接返回 None，不 fallback
        created = item.get("created_from_template_id")
        item["created_from_template_id"] = created if created else None
        # P0: source 根据 template_id 前缀动态解析
        item["source"] = "official" if item["template_id"].startswith(("et_", "dt_", "official.")) else "tenant_private"
        return item

    @staticmethod
    def _employee_instance_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["enabled"] = bool(item["enabled"])
        # P1: DB 值为 NULL 时直接返回 None，不 fallback
        created = item.get("created_from_template_id")
        item["created_from_template_id"] = created if created else None
        # P0: source 根据 template_id 前缀动态解析
        item["source"] = "official" if item["template_id"].startswith(("et_", "dt_", "official.")) else "tenant_private"
        # Gate E 快照字段（实例化时冻结，供运行时 Prompt 组装读取）
        item["persona_ref"] = item.get("persona_ref", "") or ""
        item["default_skill"] = item.get("default_skill", "") or ""
        item["default_tool"] = item.get("default_tool", "") or ""
        item["avatar_ref"] = item.get("avatar_ref", "") or ""
        return item

    def get_employee_persona(self, employee_id: str) -> dict[str, Any] | None:
        """解析 employee_id → persona_ref → persona_templates 行（Gate E §4.2）。

        供运行时 Prompt 组装使用；本阶段仅返回解析结果，不实现调用方。
        employee 不存在或 persona_ref 为空 → 返回 None。
        """
        employee = self.get_employee_instance(employee_id)
        if employee is None:
            return None
        persona_ref = employee.get("persona_ref") or ""
        if not persona_ref:
            return None
        return self.database.get_persona_template(persona_ref)

    @staticmethod
    def _binding_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["enabled"] = bool(item["enabled"])
        return item
