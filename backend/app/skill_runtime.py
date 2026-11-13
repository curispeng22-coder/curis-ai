from __future__ import annotations

import json
import re
import uuid
import hashlib
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from .database import Database
from .tenant_context import TenantContext


_SKILL_TYPES = frozenset({"planning", "analysis", "architecture", "frontend", "backend", "qa", "tool_operation"})
_CAPABILITY_TYPES = frozenset({"model", "tool", "connector"})
_SECRET_LIKE = re.compile(
    r"(?:api[ _-]?key|secret|token|password|authorization)\s*[:=]|"
    r"(?:local-dev|vault|kms)://|bearer\s+",
    re.IGNORECASE,
)
_RUNTIME_OVERRIDE = re.compile(
    r"(?:tool_required|model_gateway_tool|select\s+(?:a\s+)?tool|credential_ref|config_ref)",
    re.IGNORECASE,
)


class SkillRuntime:
    """Bounded employee skill metadata and guidance service.

    Skills never select a tool, resolve a credential, or execute on their own.
    """

    def __init__(self, database: Database) -> None:
        self.database = database

    def list_templates(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select * from skill_templates
                where status = 'active' and (
                  source = 'official' or (source = 'tenant_private' and tenant_id = ?)
                )
                order by source, name, skill_template_id
                """,
                (tenant_id,),
            ).fetchall()
        skills = [self._template_from_row(row) for row in rows]
        for skill in skills:
            package = self.package_receipt(skill["skill_template_id"])
            skill["package"] = ({key: package[key] for key in ("repo_url", "commit", "subdirectory", "package_sha256", "license_sha256")}
                                if package else None)
            skill["installation_kind"] = "FULL_PACKAGE" if package else "GUIDANCE_METADATA"
            skill["dependency_status"] = self.dependency_status(package) if package else None
        return {"tenant_id": tenant_id, "skills": skills}

    def package_root(self) -> Path:
        tenant = hashlib.sha256(TenantContext.current_tenant_id().encode()).hexdigest()
        return Path(self.database.path).absolute().parent / "skill-packages" / tenant

    def package_receipt(self, skill_id: str) -> dict | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "select payload from evolution_events where tenant_id=? and event_type='skill.package.installed' "
                "and correlation_id=? order by event_id desc limit 1",
                (TenantContext.current_tenant_id(), skill_id),
            ).fetchone()
        return json.loads(row["payload"])["manifest"] if row else None

    def preview_package(self, repo_url: str, commit: str | None = None, subdirectory: str = "", *, fetch=None) -> dict:
        from .skill_package import inspect_package, resolve_link
        discover = commit is None
        if discover:
            repo_url, commit, inferred = resolve_link(repo_url, fetch=fetch)
            subdirectory = subdirectory or inferred
        manifest, _ = inspect_package(repo_url, commit, subdirectory, discover=discover,
                                      **({"fetch": fetch} if fetch else {}))
        if not manifest.get("selection_required"):
            manifest["dependency_status"] = self.dependency_status(manifest)
        return manifest

    def install_repository(self, *, repo_url: str, commit: str | None = None, subdirectory: str = "",
                           expected_package_sha256: str, license_accepted: bool, fetch=None) -> dict:
        from .skill_package import inspect_package, install_package, resolve_link
        from .evolution_event_log import EvolutionEventLog
        if license_accepted is not True:
            raise ValueError("请先核对来源、版本和许可并明确确认。")
        discover = commit is None
        if discover:
            repo_url, commit, inferred = resolve_link(repo_url, fetch=fetch)
            subdirectory = subdirectory or inferred
        manifest, files = inspect_package(repo_url, commit, subdirectory, discover=discover,
                                          **({"fetch": fetch} if fetch else {}))
        if manifest.get("selection_required"):
            raise ValueError("请选择要安装的技能。")
        if manifest["package_sha256"] != expected_package_sha256:
            raise ValueError("技能来源或文件已变化，请重新核对，未安装。")
        install_package(self.package_root(), manifest, files)
        slug = "package-" + manifest["package_sha256"]
        with self.database.connect() as connection:
            row = connection.execute("select * from skill_templates where tenant_id=? and slug=?",
                                     (TenantContext.current_tenant_id(), slug)).fetchone()
        if row is not None and row["status"] != "active":
            with self.database.connect() as connection:
                connection.execute("update skill_templates set status='active', updated_at=current_timestamp "
                                   "where skill_template_id=? and tenant_id=?", (row["skill_template_id"], TenantContext.current_tenant_id()))
            row = {**dict(row), "status": "active"}
        skill = self._template_from_row(row) if row else self.create_private_template(
            slug=slug, name=manifest["name"],
            description="完整开源技能包；使用仍需当前员工的执行授权。", skill_type="tool_operation")
        EvolutionEventLog(self.database).record(correlation_id=skill["skill_template_id"],
            event_type="skill.package.installed", payload={"manifest": manifest, "license_accepted": True},
            idempotency_key="skill-package:" + TenantContext.current_tenant_id() + ":" + manifest["package_sha256"])
        return {**skill, "package": manifest, "installation_kind": "FULL_PACKAGE",
                "dependency_status": self.dependency_status(manifest)}

    @staticmethod
    def dependency_status(manifest: dict) -> dict:
        requirements = manifest.get("dependencies")
        if requirements is None:
            # Old package receipts have no dependency proof; never silently upgrade them.
            return {"state": "UNKNOWN", "ready": False, "requirements": [],
                    "message": "原安装未记录依赖，请重新核对来源与运行条件。"}
        if not requirements:
            return {"state": "READY", "ready": True, "requirements": [],
                    "message": "完整指导技能已安装，未发现额外声明的运行依赖；使用仍遵循员工当前授权。"}
        browser_only = all(item.get("preparation") == "existing_browser_connection" for item in requirements)
        return {"state": "PREPARATION_REQUIRED" if browser_only else "UNSUPPORTED_REQUIREMENTS",
                "ready": False, "requirements": requirements,
                "message": ("技能包已安装；官方 BrowserSkill 连接与扩展需沿现有浏览器授权流程准备，尚未证明可执行。"
                            if browser_only else "技能包已安装；声明的运行依赖尚无已核验的自动准备方式，未执行安装脚本。"),
                "preparation": "existing_browser_connection" if browser_only else None}

    def remove_template(self, skill_template_id: str, company_id: str = "") -> dict:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            template = self._get_template(skill_template_id, connection=connection)
            if template["source"] != "tenant_private":
                raise ValueError("只能移除已纳入公司的技能，不能修改官方目录。")
            # The existing catalog is tenant-wide, not a second per-company Skill store.
            # Never retire a shared resource while another company's employee uses it.
            companies = connection.execute(
                "select distinct e.company_id from employee_skill_bindings b join employee_instances e "
                "on e.id=b.employee_id and e.tenant_id=b.tenant_id where b.tenant_id=? and b.skill_template_id=?",
                (tenant_id, skill_template_id)).fetchall()
            if any(row[0] != company_id for row in companies):
                raise ValueError("其他公司员工仍绑定此共享技能，请先核对并解绑；尚未移除。")
            count = connection.execute("select count(*) from employee_skill_bindings where tenant_id=? and skill_template_id=?",
                                       (tenant_id, skill_template_id)).fetchone()[0]
            connection.execute("delete from employee_skill_bindings where tenant_id=? and skill_template_id=?",
                               (tenant_id, skill_template_id))
            connection.execute("update skill_templates set status='disabled', updated_at=current_timestamp "
                               "where tenant_id=? and skill_template_id=?", (tenant_id, skill_template_id))
        return {"skill_template_id": skill_template_id, "status": "disabled", "unbound_employees": count,
                "history_retained": True, "package_retained": True,
                "message": "已从公司资源移除并解绑；历史成果和包凭据保留。已开始的任务请回原工作核对或停止。"}

    def execution_packages(self, employee_id: str, capability_binding_id: str) -> list[dict]:
        from .skill_package import verify_package
        self._get_employee(employee_id)
        with self.database.connect() as connection:
            binding = connection.execute("select id from employee_capability_bindings where tenant_id=? "
                "and employee_id=? and id=? and capability_type='agent' and enabled=1",
                (TenantContext.current_tenant_id(), employee_id, capability_binding_id)).fetchone()
        if binding is None:
            raise ValueError("当前员工的 Agent 执行绑定不可用。")
        result = []
        for skill in self.list_employee_bindings(employee_id)["bindings"]:
            if not skill["enabled"] or skill["skill_status"] != "active":
                continue
            allowed = skill["capability_binding_ids"]
            if allowed and capability_binding_id not in allowed:
                continue
            manifest = self.package_receipt(skill["skill_template_id"])
            if manifest:
                state = self.dependency_status(manifest)
                if not state["ready"]:
                    raise ValueError(state["message"])
                path = self.package_root() / manifest["package_sha256"]
                verify_package(path, manifest)
                result.append({"skill_template_id": skill["skill_template_id"], "path": str(path), "manifest": manifest})
        return result

    def create_private_template(
        self,
        *,
        slug: str,
        name: str,
        description: str = "",
        skill_type: str = "analysis",
        instruction_excerpt: str = "",
        default_capability_types: list[str] | None = None,
        created_from_template_id: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        slug = slug.strip()
        name = name.strip()
        if not slug or not name:
            raise ValueError("skill slug and name are required")
        if skill_type not in _SKILL_TYPES:
            raise ValueError("skill_type is not supported")
        types = default_capability_types or ["model"]
        if not set(types).issubset(_CAPABILITY_TYPES):
            raise ValueError("default_capability_types must contain model, tool, or connector")
        excerpt = self._normalize_excerpt(instruction_excerpt)
        skill_id = f"skill-{uuid.uuid4()}"
        try:
            with self.database.connect() as connection:
                connection.execute(
                    """
                    insert into skill_templates (
                      skill_template_id, slug, name, description, skill_type,
                      default_capability_types_json, instruction_excerpt, source,
                      tenant_id, status, created_from_template_id, updated_at
                    ) values (?, ?, ?, ?, ?, ?, ?, 'tenant_private', ?, 'active', ?, current_timestamp)
                    """,
                    (
                        skill_id,
                        slug,
                        name,
                        description.strip(),
                        skill_type,
                        json.dumps(types, ensure_ascii=False),
                        excerpt,
                        tenant_id,
                        created_from_template_id or None,
                    ),
                )
        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                raise ValueError("skill slug already exists for this tenant") from error
            raise
        return self._get_template(skill_id)

    def install_template(self, skill_template_id: str) -> dict[str, Any]:
        """纳入一个官方 Skill，形成当前租户的可撤回副本。"""
        tenant_id = TenantContext.current_tenant_id()
        source = self._get_template(skill_template_id)
        if source["source"] == "tenant_private" and source.get("tenant_id") == tenant_id:
            return source
        if source["source"] != "official" or source["status"] != "active":
            raise ValueError("only active official skills can be installed")
        with self.database.connect() as connection:
            existing = connection.execute(
                """
                select * from skill_templates
                where tenant_id = ? and source = 'tenant_private'
                  and created_from_template_id = ? and status = 'active'
                order by created_at asc limit 1
                """,
                (tenant_id, skill_template_id),
            ).fetchone()
        if existing is not None:
            return self._template_from_row(existing)
        slug = f"installed-{source['slug']}"
        return self.create_private_template(
            slug=slug,
            name=source["name"],
            description=source.get("description", ""),
            skill_type=source["skill_type"],
            instruction_excerpt=source.get("instruction_excerpt", ""),
            default_capability_types=source.get("default_capability_types", ["model"]),
            created_from_template_id=skill_template_id,
        )

    def list_employee_bindings(self, employee_id: str) -> dict[str, Any]:
        self._get_employee(employee_id)
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select b.*, s.name as skill_name, s.skill_type, s.source as skill_source, s.status as skill_status
                from employee_skill_bindings b
                join skill_templates s on s.skill_template_id = b.skill_template_id
                where b.tenant_id = ? and b.employee_id = ?
                order by b.priority, b.created_at
                """,
                (tenant_id, employee_id),
            ).fetchall()
        return {
            "tenant_id": tenant_id,
            "employee_id": employee_id,
            "bindings": [self._binding_from_row(row) for row in rows],
        }

    def set_employee_bindings(self, employee_id: str, bindings: list[dict[str, Any]]) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            self._get_employee(employee_id, connection=connection)
            normalized = [self._normalize_binding(employee_id, item, connection=connection) for item in bindings]
            if len({item["skill_template_id"] for item in normalized}) != len(normalized):
                raise ValueError("同一员工不能重复绑定相同技能。")
            connection.execute(
                "delete from employee_skill_bindings where tenant_id = ? and employee_id = ?",
                (tenant_id, employee_id),
            )
            connection.executemany(
                """
                insert into employee_skill_bindings (
                  binding_id, tenant_id, employee_id, skill_template_id,
                  capability_binding_ids_json, priority, enabled
                ) values (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        item["binding_id"],
                        tenant_id,
                        employee_id,
                        item["skill_template_id"],
                        json.dumps(item["capability_binding_ids"], ensure_ascii=False),
                        item["priority"],
                        1 if item["enabled"] else 0,
                    )
                    for item in normalized
                ],
            )
        return self.list_employee_bindings(employee_id)

    def change_employee_binding(self, employee_id: str, skill_template_id: str, *, remove: bool = False) -> dict:
        """Single-item mutations never overwrite a client-side snapshot of other skills."""
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            self._get_employee(employee_id, connection=connection)
            if remove:
                connection.execute("delete from employee_skill_bindings where tenant_id=? and employee_id=? and skill_template_id=?",
                                   (tenant_id, employee_id, skill_template_id))
            else:
                item = self._normalize_binding(employee_id, {"skill_template_id": skill_template_id, "priority": 50}, connection=connection)
                connection.execute("insert into employee_skill_bindings (binding_id,tenant_id,employee_id,skill_template_id,"
                    "capability_binding_ids_json,priority,enabled) values (?,?,?,?,?,50,1) "
                    "on conflict(tenant_id,employee_id,skill_template_id) do nothing",
                    (item["binding_id"], tenant_id, employee_id, skill_template_id, "[]"))
        return self.list_employee_bindings(employee_id)

    def prompt_excerpt(self, employee_id: str | None) -> str:
        if not employee_id:
            return ""
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select s.name, s.instruction_excerpt
                from employee_skill_bindings b
                join skill_templates s on s.skill_template_id = b.skill_template_id
                where b.tenant_id = ? and b.employee_id = ? and b.enabled = 1
                  and s.status = 'active'
                  and (s.source = 'official' or (s.source = 'tenant_private' and s.tenant_id = ?))
                order by b.priority, b.created_at
                """,
                (tenant_id, employee_id, tenant_id),
            ).fetchall()
        parts = [f"{row['name']}: {self._normalize_excerpt(row['instruction_excerpt'])}" for row in rows]
        return "\n".join(part for part in parts if part)[:1200]

    def _normalize_binding(self, employee_id: str, item: dict[str, Any], *, connection=None) -> dict[str, Any]:
        binding_id = item.get("binding_id")
        if binding_id:
            with (nullcontext(connection) if connection is not None else self.database.connect()) as connection:
                existing = connection.execute("select skill_template_id from employee_skill_bindings "
                    "where tenant_id=? and employee_id=? and binding_id=?",
                    (TenantContext.current_tenant_id(), employee_id, binding_id)).fetchone()
            if existing is None or existing["skill_template_id"] != item.get("skill_template_id"):
                raise ValueError("技能绑定身份与当前员工不一致。")
        skill_template_id = str(item.get("skill_template_id") or "")
        template = self._get_template(skill_template_id, connection=connection)
        if template["status"] != "active":
            raise ValueError("skill template is not active")
        capability_binding_ids = list(item.get("capability_binding_ids") or [])
        if capability_binding_ids:
            with (nullcontext(connection) if connection is not None else self.database.connect()) as connection:
                rows = connection.execute(
                    """
                    select id from employee_capability_bindings
                    where tenant_id = ? and employee_id = ? and id in ({})
                    """.format(",".join("?" for _ in capability_binding_ids)),
                    (TenantContext.current_tenant_id(), employee_id, *capability_binding_ids),
                ).fetchall()
            if {row["id"] for row in rows} != set(capability_binding_ids):
                raise ValueError("skill capability_binding_ids must belong to the employee")
        return {
            "binding_id": str(item.get("binding_id") or f"skill-bind-{uuid.uuid4()}"),
            "skill_template_id": skill_template_id,
            "capability_binding_ids": capability_binding_ids,
            "priority": int(item.get("priority", 100) or 100),
            "enabled": bool(item.get("enabled", True)),
        }

    def _get_template(self, skill_template_id: str, *, connection=None) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with (nullcontext(connection) if connection is not None else self.database.connect()) as connection:
            row = connection.execute(
                """
                select * from skill_templates
                where skill_template_id = ? and (
                  source = 'official' or (source = 'tenant_private' and tenant_id = ?)
                )
                """,
                (skill_template_id, tenant_id),
            ).fetchone()
        if row is None:
            raise ValueError("skill template is not available")
        return self._template_from_row(row)

    def _get_employee(self, employee_id: str, *, connection=None) -> dict[str, Any]:
        with (nullcontext(connection) if connection is not None else self.database.connect()) as connection:
            row = connection.execute(
                "select id from employee_instances where tenant_id = ? and id = ?",
                (TenantContext.current_tenant_id(), employee_id),
            ).fetchone()
        if row is None:
            raise ValueError("employee instance is not available")
        return dict(row)

    @staticmethod
    def _normalize_excerpt(value: str) -> str:
        text = " ".join(str(value or "").split())[:800]
        if _SECRET_LIKE.search(text):
            raise ValueError("skill instruction_excerpt cannot contain credential-like data")
        if _RUNTIME_OVERRIDE.search(text):
            raise ValueError("skill instruction_excerpt cannot contain runtime selection directives")
        return text

    @staticmethod
    def _template_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["default_capability_types"] = json.loads(item.pop("default_capability_types_json") or "[]")
        return item

    @staticmethod
    def _binding_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["capability_binding_ids"] = json.loads(item.pop("capability_binding_ids_json") or "[]")
        item["enabled"] = bool(item["enabled"])
        return item
