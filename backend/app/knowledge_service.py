from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from .database import Database
from .tenant_context import TenantContext


class KnowledgeService:
    """Canonical Knowledge records plus bounded, typed Work references."""

    ALLOWED_SUFFIXES = {".md", ".txt"}
    CANONICAL_TARGETS = {"COMPANY", "BUSINESS", "WORKSPACE"}
    MAX_FILE_BYTES = 2 * 1024 * 1024
    MAX_MANUAL_BYTES = 200 * 1024
    MAX_FILES = 200
    MAX_BATCH = 50
    MAX_CONTEXT = 3

    def __init__(self, database: Database) -> None:
        self.database = database

    def list_local_roots(self) -> dict[str, Any]:
        roots = self._roots()
        return {
            "connector": {
                "capability_id": "connector.local_files",
                "capability_type": "connector",
                "name": "Obsidian / 本地文件",
                "status": "configured" if roots else "unconfigured",
            },
            "roots": [
                {"root_id": root_id, "label": root.name or "资料根目录"}
                for root_id, root in roots.items()
            ],
        }

    def list_local_files(self, root_id: str, query: str = "") -> dict[str, Any]:
        root = self._root(root_id)
        needle = query.strip().lower()
        if len(needle) > 200:
            raise ValueError("file query is too long")
        files: list[dict[str, Any]] = []
        for current, dirnames, filenames in os.walk(root, followlinks=False):
            current_path = Path(current)
            dirnames[:] = [
                name
                for name in dirnames
                if not name.startswith(".") and not (current_path / name).is_symlink()
            ]
            for filename in sorted(filenames):
                candidate = current_path / filename
                if (
                    filename.startswith(".")
                    or candidate.is_symlink()
                    or candidate.suffix.lower() not in self.ALLOWED_SUFFIXES
                ):
                    continue
                relative = candidate.relative_to(root).as_posix()
                if needle and needle not in relative.lower():
                    continue
                stat = candidate.stat()
                if stat.st_size > self.MAX_FILE_BYTES:
                    continue
                files.append({
                    "relative_path": relative,
                    "title": candidate.stem,
                    "size_bytes": stat.st_size,
                    "modified_at": self._timestamp(stat.st_mtime),
                })
                if len(files) >= self.MAX_FILES:
                    return {"root_id": root_id, "files": files, "truncated": True}
        return {"root_id": root_id, "files": files, "truncated": False}

    def import_local_file(
        self,
        *,
        root_id: str,
        relative_path: str,
        title: str = "",
        tags: list[str] | None = None,
        company_id: str | None = None,
        target_type: str | None = None,
        target_ref: str | None = None,
        project_id: str | None = None,
        department_id: str | None = None,
        created_by: str = "",
    ) -> dict[str, Any]:
        root = self._root(root_id)
        candidate, relative = self._safe_file(root, relative_path)
        body = candidate.read_text(encoding="utf-8")
        return self._save(
            title=title.strip() or self._title_from_text(body, candidate.stem),
            body=body,
            summary=self._summary(body),
            source_type="local_file",
            connector_id=root_id,
            source_label=root.name or "资料根目录",
            source_path=relative,
            tags=tags,
            company_id=company_id,
            target_type=target_type,
            target_ref=target_ref,
            project_id=project_id,
            department_id=department_id,
            created_by=created_by,
        )

    def create_entry(
        self,
        *,
        title: str,
        body: str,
        summary: str = "",
        tags: list[str] | None = None,
        company_id: str | None = None,
        target_type: str | None = None,
        target_ref: str | None = None,
        project_id: str | None = None,
        department_id: str | None = None,
        created_by: str = "",
    ) -> dict[str, Any]:
        if len(body.encode("utf-8")) > self.MAX_MANUAL_BYTES:
            raise ValueError("knowledge body is too large")
        return self._save(
            title=title,
            body=body,
            summary=summary.strip() or self._summary(body),
            source_type="manual",
            connector_id="",
            source_label="手工录入",
            source_path="",
            tags=tags,
            company_id=company_id,
            target_type=target_type,
            target_ref=target_ref,
            project_id=project_id,
            department_id=department_id,
            created_by=created_by,
        )

    def list_entries(
        self,
        *,
        query: str = "",
        scope: str = "all",
        project_id: str = "",
        company_id: str = "",
        target_type: str = "",
        target_ref: str = "",
        source_type: str = "",
        lifecycle_status: str = "ACTIVE",
        sort: str = "updated",
        limit: int = 30,
        offset: int = 0,
        work_ref: str = "",
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        needle = query.strip()
        if len(needle) > 200:
            raise ValueError("knowledge query is too long")
        if scope not in {"all", "company", "project", "department"}:
            raise ValueError("knowledge scope is invalid")
        if target_type and target_type.upper() not in self.CANONICAL_TARGETS:
            raise ValueError("knowledge target type is invalid")
        if source_type and source_type not in {"manual", "local_file"}:
            raise ValueError("knowledge source type is invalid")
        if lifecycle_status not in {"ACTIVE", "ARCHIVED", "all"}:
            raise ValueError("knowledge lifecycle status is invalid")
        if sort not in {"updated", "recent_used"}:
            raise ValueError("knowledge sort is invalid")
        if limit < 1 or limit > self.MAX_BATCH or offset < 0:
            raise ValueError("knowledge batch is invalid")

        clauses = ["ke.tenant_id = ?"]
        params: list[Any] = [tenant_id]
        if lifecycle_status != "all":
            clauses.append("ke.lifecycle_status = ?")
            params.append(lifecycle_status)
        if company_id:
            clauses.append("ke.company_id = ?")
            params.append(company_id)
        if target_type:
            clauses.append("ke.target_type = ?")
            params.append(target_type.upper())
        if target_ref:
            clauses.append("ke.target_ref = ?")
            params.append(target_ref)
        if source_type:
            clauses.append("ke.source_type = ?")
            params.append(source_type)
        if scope == "company":
            clauses.append("((ke.target_type='COMPANY') or (ke.target_type is null and ke.project_id is null and ke.department_id is null))")
        elif scope == "project":
            clauses.append("ke.project_id is not null")
        elif scope == "department":
            clauses.append("ke.department_id is not null")
        if project_id:
            clauses.append("ke.project_id = ?")
            params.append(project_id)
        if work_ref:
            work = self._work_scope(work_ref)
            clauses.append(
                "ke.company_id=? and ((ke.target_type='COMPANY' and ke.target_ref=?) "
                "or (ke.target_type='BUSINESS' and ke.target_ref=?) "
                "or (ke.target_type='WORKSPACE' and ke.target_ref=?))"
            )
            params.extend([work["company_id"], work["company_id"], work["business_id"], work["workspace_id"]])
        if needle:
            like = f"%{needle}%"
            clauses.append("(ke.title like ? or ke.summary like ? or ke.body like ? or ke.tags_json like ?)")
            params.extend([like, like, like, like])

        where = " and ".join(clauses)
        order = (
            "case when exists (select 1 from typed_object_references r where r.tenant_id=ke.tenant_id "
            "and r.target_type='KNOWLEDGE' and r.target_ref=ke.id) then 0 else 1 end, "
            "coalesce((select max(r.created_at) from typed_object_references r where r.tenant_id=ke.tenant_id "
            "and r.target_type='KNOWLEDGE' and r.target_ref=ke.id), ke.updated_at) desc, ke.id"
            if sort == "recent_used"
            else "ke.updated_at desc, ke.id"
        )
        with self.database.connect() as connection:
            total = connection.execute(
                f"select count(*) from knowledge_entries ke where {where}", params
            ).fetchone()[0]
            rows = connection.execute(
                f"{self._select_sql()} where {where} order by {order} limit ? offset ?",
                [*params, limit + 1, offset],
            ).fetchall()
        return {
            "tenant_id": tenant_id,
            "entries": [self._entry(row, include_body=False, query=needle) for row in rows[:limit]],
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": len(rows) > limit,
        }

    def get_entry(self, entry_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                self._select_sql() + " where ke.tenant_id = ? and ke.id = ?",
                (tenant_id, entry_id),
            ).fetchone()
        if row is None:
            raise KeyError("knowledge entry not found")
        return self._entry(row, include_body=True)

    def archive_entry(self, entry_id: str, *, actor: str) -> dict[str, Any]:
        if not actor:
            raise PermissionError("CEO identity is required")
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                "update knowledge_entries set lifecycle_status='ARCHIVED', archived_at=current_timestamp, "
                "updated_at=current_timestamp where tenant_id=? and id=? and lifecycle_status='ACTIVE'",
                (tenant_id, entry_id),
            )
            if cursor.rowcount == 0 and not connection.execute(
                "select 1 from knowledge_entries where tenant_id=? and id=?",
                (tenant_id, entry_id),
            ).fetchone():
                raise KeyError("knowledge entry not found")
        return self.get_entry(entry_id)

    def add_work_references(
        self, work_ref: str, knowledge_ids: list[str], *, actor: str
    ) -> dict[str, Any]:
        if not actor:
            raise PermissionError("CEO identity is required")
        unique_ids = list(dict.fromkeys(str(item).strip() for item in knowledge_ids if str(item).strip()))
        if not unique_ids or len(unique_ids) > 20:
            raise ValueError("select between 1 and 20 knowledge entries")
        tenant_id = TenantContext.current_tenant_id()
        work = self._work_scope(work_ref)
        identity_company = TenantContext.current_identity().get("company_id")
        if identity_company and identity_company != work["company_id"]:
            raise PermissionError("Work is outside the current Company")
        entries = [self.get_entry(entry_id) for entry_id in unique_ids]
        for entry in entries:
            if entry["lifecycle_status"] != "ACTIVE":
                raise ValueError("archived knowledge cannot be selected")
            if not self._compatible(entry, work):
                raise ValueError("knowledge is outside the Work scope")
        with self.database.connect() as connection:
            for entry in entries:
                identity = f"{tenant_id}|WORK|{work_ref}|USES_REFERENCE|KNOWLEDGE|{entry['id']}"
                reference_id = "reference-" + hashlib.sha256(identity.encode()).hexdigest()[:32]
                connection.execute(
                    "insert or ignore into typed_object_references(reference_id,tenant_id,company_id,workspace_id,"
                    "source_type,source_ref,relation,target_type,target_ref,created_by) values(?,?,?,?,?,?,?,?,?,?)",
                    (
                        reference_id,
                        tenant_id,
                        work["company_id"],
                        work["workspace_id"],
                        "WORK",
                        work_ref,
                        "USES_REFERENCE",
                        "KNOWLEDGE",
                        entry["id"],
                        actor,
                    ),
                )
        return self.list_work_references(work_ref)

    def list_work_references(self, work_ref: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        work = self._work_scope(work_ref)
        with self.database.connect() as connection:
            rows = connection.execute(
                self._select_sql()
                + " join typed_object_references r on r.tenant_id=ke.tenant_id "
                "and r.target_type='KNOWLEDGE' and r.target_ref=ke.id "
                "where r.tenant_id=? and r.source_type='WORK' and r.source_ref=? "
                "and r.relation='USES_REFERENCE' order by r.created_at, r.reference_id",
                (tenant_id, work_ref),
            ).fetchall()
        return {
            "work_ref": work_ref,
            "work": {
                "problem": work.get("problem", ""),
                "expected_result": work.get("expected_result", ""),
                "workspace_id": work["workspace_id"],
            },
            "references": [self._entry(row, include_body=False) for row in rows],
        }

    def used_by(self, entry_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self.get_entry(entry_id)
        with self.database.connect() as connection:
            rows = connection.execute(
                "select r.*,e.lifecycle_status,e.data_json,c.data_json as cycle_data_json "
                "from typed_object_references r "
                "join runtime_entities e on e.tenant_id=r.tenant_id and e.entity_id=r.source_ref "
                "join runtime_entities c on c.tenant_id=e.tenant_id and c.entity_id=e.parent_id "
                "and c.entity_type='CYCLE' "
                "where r.tenant_id=? and r.target_type='KNOWLEDGE' and r.target_ref=? "
                "and r.relation='USES_REFERENCE' order by r.created_at desc",
                (tenant_id, entry_id),
            ).fetchall()
        works = []
        for row in rows:
            data = json.loads(row["data_json"] or "{}")
            cycle_data = json.loads(row["cycle_data_json"] or "{}")
            contract = cycle_data.get("contract") or {}
            route = data.get("responsibilityRouting") or {}
            works.append({
                "work_ref": row["source_ref"],
                "status": route.get("status") or row["lifecycle_status"],
                "title": contract.get("problem") or data.get("goal") or data.get("kind") or "工作",
                "responsibility": data.get("responsibility") or route.get("currentResponsibilityKey") or "",
                "workspace_id": row["workspace_id"],
                "used_at": row["created_at"],
            })
        return {"knowledge_id": entry_id, "works": works}

    def related_results(self, entry_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        used = self.used_by(entry_id)["works"]
        results: list[dict[str, Any]] = []
        with self.database.connect() as connection:
            for used_work in used:
                row = connection.execute(
                    "select data_json from runtime_entities where tenant_id=? and entity_id=?",
                    (tenant_id, used_work["work_ref"]),
                ).fetchone()
                data = json.loads(row["data_json"] or "{}") if row else {}
                route = data.get("responsibilityRouting") or {}
                for kind, refs in (
                    ("RESULT", [*data.get("resultRefs", []), *route.get("resultRefs", [])]),
                    ("ARTIFACT", [*data.get("artifactRefs", []), *route.get("artifactRefs", [])]),
                    ("EVIDENCE", [*data.get("evidenceRefs", []), *route.get("evidenceRefs", [])]),
                ):
                    for ref in refs:
                        if not any(item["reference_id"] == ref for item in results):
                            results.append({"reference_id": ref, "kind": kind, "work_ref": used_work["work_ref"]})
        return {"knowledge_id": entry_id, "results": results}

    def context_for_work(
        self, work_ref: str, *, query: str = "", limit: int = MAX_CONTEXT
    ) -> dict[str, Any]:
        limit = max(1, min(int(limit), self.MAX_CONTEXT))
        work = self._work_scope(work_ref)
        explicit = self.list_work_references(work_ref)["references"]
        selected = explicit[:limit]
        needle = query.strip()
        if len(selected) < limit and needle:
            existing = {item["id"] for item in selected}
            # Search the complete Work text through the existing bounded, scoped query API.
            for start in range(0, len(needle), 200):
                segment = needle[start:start + 200]
                if not segment.strip():
                    continue
                automatic = self.list_entries(
                    query=segment, company_id=work["company_id"], work_ref=work_ref, limit=limit
                )["entries"]
                for item in automatic:
                    if item["id"] not in existing and len(selected) < limit:
                        selected.append(item)
                        existing.add(item["id"])
        selected = selected[:limit]
        explicit_ids = {item["id"] for item in explicit}
        return {
            "work_ref": work_ref,
            "references": [
                {
                    "ref": f"knowledge:{item['id']}",
                    "title": item["title"],
                    "summary": item["summary"] or item["excerpt"],
                    "source": item["source_label"] or item["source_path"] or "手工录入",
                    "source_status": item["source_status"],
                    "scope": item["scope_name"],
                    "selection": "EXPLICIT" if item["id"] in explicit_ids else "BOUNDED_RETRIEVAL",
                    "lifecycle_status": item["lifecycle_status"],
                }
                for item in selected
            ],
            "bounded": True,
            "limit": limit,
            "hydrated_bodies": 0,
        }

    def _save(
        self,
        *,
        title: str,
        body: str,
        summary: str,
        source_type: str,
        connector_id: str,
        source_label: str,
        source_path: str,
        tags: list[str] | None,
        company_id: str | None,
        target_type: str | None,
        target_ref: str | None,
        project_id: str | None,
        department_id: str | None,
        created_by: str,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        clean_title = title.strip()
        clean_body = body.strip()
        if not clean_title or len(clean_title) > 200:
            raise ValueError("knowledge title is required and must be at most 200 characters")
        if not clean_body:
            raise ValueError("knowledge body is required")
        clean_tags = self._tags(tags or [])
        canonical = self._validate_scope(company_id, target_type, target_ref, project_id, department_id)
        digest = hashlib.sha256(clean_body.encode("utf-8")).hexdigest()
        entry_id = f"knowledge-{uuid.uuid4()}"
        with self.database.connect() as connection:
            existing = None
            if source_type == "local_file":
                existing = connection.execute(
                    "select id from knowledge_entries where tenant_id=? and connector_id=? and source_path=?",
                    (tenant_id, connector_id, source_path),
                ).fetchone()
            if existing:
                entry_id = existing["id"]
                connection.execute(
                    "update knowledge_entries set title=?,body=?,summary=?,source_label=?,company_id=?,target_type=?,"
                    "target_ref=?,project_id=?,department_id=?,tags_json=?,content_sha256=?,created_by=?,"
                    "lifecycle_status='ACTIVE',archived_at=null,updated_at=current_timestamp where tenant_id=? and id=?",
                    (
                        clean_title, clean_body, summary[:500], source_label,
                        canonical["company_id"], canonical["target_type"], canonical["target_ref"],
                        project_id, department_id, json.dumps(clean_tags, ensure_ascii=False),
                        digest, created_by, tenant_id, entry_id,
                    ),
                )
            else:
                connection.execute(
                    "insert into knowledge_entries(id,tenant_id,title,body,summary,source_type,connector_id,source_label,"
                    "source_path,company_id,target_type,target_ref,project_id,department_id,tags_json,content_sha256,created_by) "
                    "values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        entry_id, tenant_id, clean_title, clean_body, summary[:500], source_type,
                        connector_id, source_label, source_path, canonical["company_id"],
                        canonical["target_type"], canonical["target_ref"], project_id, department_id,
                        json.dumps(clean_tags, ensure_ascii=False), digest, created_by,
                    ),
                )
        return self.get_entry(entry_id)

    def _validate_scope(
        self,
        company_id: str | None,
        target_type: str | None,
        target_ref: str | None,
        project_id: str | None,
        department_id: str | None,
    ) -> dict[str, str | None]:
        if project_id and department_id:
            raise ValueError("knowledge entry can belong to one legacy scope only")
        canonical_values = [company_id, target_type, target_ref]
        if any(canonical_values) and not all(canonical_values):
            raise ValueError("canonical knowledge scope requires company, target type and target")
        if all(canonical_values) and (project_id or department_id):
            raise ValueError("canonical and legacy knowledge scopes cannot be mixed")
        tenant_id = TenantContext.current_tenant_id()
        identity_company = TenantContext.current_identity().get("company_id")
        if company_id and identity_company and company_id != identity_company:
            raise PermissionError("Knowledge scope is outside the current Company")
        if not all(canonical_values):
            with self.database.connect() as connection:
                if project_id and not connection.execute(
                    "select 1 from projects where tenant_id=? and project_id=?",
                    (tenant_id, project_id),
                ).fetchone():
                    raise ValueError("project is not available")
                if department_id and not connection.execute(
                    "select 1 from department_instances where tenant_id=? and id=? and deleted_at is null",
                    (tenant_id, department_id),
                ).fetchone():
                    raise ValueError("department is not available")
            return {"company_id": None, "target_type": None, "target_ref": None}

        kind = str(target_type).upper()
        if kind not in self.CANONICAL_TARGETS:
            raise ValueError("knowledge target type is invalid")
        with self.database.connect() as connection:
            if kind == "COMPANY":
                valid = target_ref == company_id and connection.execute(
                    "select 1 from companies where tenant_id=? and company_id=?",
                    (tenant_id, company_id),
                ).fetchone()
            elif kind == "BUSINESS":
                valid = connection.execute(
                    "select 1 from canonical_businesses b join department_instances d "
                    "on d.tenant_id=b.tenant_id and d.company_id=b.company_id and d.id=b.department_id "
                    "where b.tenant_id=? and b.company_id=? and b.business_id=? and d.deleted_at is null",
                    (tenant_id, company_id, target_ref),
                ).fetchone()
            else:
                valid = connection.execute(
                    "select 1 from workspaces w join canonical_businesses b "
                    "on b.tenant_id=w.tenant_id and b.company_id=w.company_id and b.business_id=w.business_id "
                    "join department_instances d on d.tenant_id=b.tenant_id and d.company_id=b.company_id and d.id=b.department_id "
                    "where w.tenant_id=? and w.company_id=? and w.workspace_id=? "
                    "and w.business_relation_status='RESOLVED' and d.deleted_at is null",
                    (tenant_id, company_id, target_ref),
                ).fetchone()
        if not valid:
            raise ValueError("canonical knowledge scope is not available")
        return {"company_id": company_id, "target_type": kind, "target_ref": target_ref}

    def _work_scope(self, work_ref: str) -> dict[str, Any]:
        from .resource_scope_policy import ResourceScopePolicy
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select e.*,c.data_json as cycle_data_json "
                "from runtime_entities e "
                "join runtime_entities c on c.tenant_id=e.tenant_id and c.entity_id=e.parent_id "
                "and c.entity_type='CYCLE' and c.company_id=e.company_id "
                "where e.tenant_id=? and e.entity_id=? and e.entity_type='WORK'",
                (tenant_id, work_ref),
            ).fetchone()
            if row is None:
                raise ValueError("Work does not have a resolved canonical scope")
            result = {**dict(row), **ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=tenant_id, record=dict(row))}
            parent = connection.execute("select * from runtime_entities where tenant_id=? and entity_id=?",
                (tenant_id, row["parent_id"])).fetchone()
            ResourceScopePolicy.require_same_execution_scope(result,
                ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=tenant_id, record=dict(parent)))
        cycle_data = json.loads(result.pop("cycle_data_json") or "{}")
        contract = cycle_data.get("contract") or {}
        result["problem"] = str(contract.get("problem") or "")
        result["expected_result"] = str(contract.get("expectedResult") or "")
        return result

    @staticmethod
    def _compatible(entry: dict[str, Any], work: dict[str, str]) -> bool:
        if entry.get("company_id") != work["company_id"]:
            return False
        return (
            (entry.get("target_type") == "COMPANY" and entry.get("target_ref") == work["company_id"])
            or (entry.get("target_type") == "BUSINESS" and entry.get("target_ref") == work["business_id"])
            or (entry.get("target_type") == "WORKSPACE" and entry.get("target_ref") == work["workspace_id"])
        )

    def _roots(self) -> dict[str, Path]:
        roots: dict[str, Path] = {}
        for raw in os.getenv("CURIS_KNOWLEDGE_ROOTS", "").split(os.pathsep):
            if not raw.strip():
                continue
            try:
                root = Path(raw).expanduser().resolve(strict=True)
            except OSError:
                continue
            if root.is_dir():
                roots[hashlib.sha256(str(root).encode()).hexdigest()[:16]] = root
        return roots

    def _root(self, root_id: str) -> Path:
        root = self._roots().get(root_id)
        if root is None:
            raise ValueError("knowledge root is not configured")
        return root

    def _source_available(self, item: dict[str, Any]) -> bool:
        if item.get("source_type") == "manual":
            return True
        root = self._roots().get(str(item.get("connector_id") or ""))
        if root is None:
            return False
        try:
            self._safe_file(root, str(item.get("source_path") or ""))
            return True
        except ValueError:
            return False

    def _safe_file(self, root: Path, relative_path: str) -> tuple[Path, str]:
        pure = PurePosixPath(relative_path.strip())
        if (
            not relative_path.strip()
            or pure.is_absolute()
            or any(part in {"", ".", ".."} or part.startswith(".") for part in pure.parts)
        ):
            raise ValueError("knowledge file path is invalid")
        try:
            candidate = root.joinpath(*pure.parts).resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as error:
            raise ValueError("knowledge file is outside the configured root") from error
        if not candidate.is_file():
            raise ValueError("knowledge file is not available")
        if candidate.suffix.lower() not in self.ALLOWED_SUFFIXES:
            raise ValueError("knowledge file type is not supported")
        if candidate.stat().st_size > self.MAX_FILE_BYTES:
            raise ValueError("knowledge file is too large")
        return candidate, pure.as_posix()

    @staticmethod
    def _tags(tags: list[str]) -> list[str]:
        clean: list[str] = []
        for tag in tags:
            value = str(tag).strip()
            if value and value not in clean:
                if len(value) > 50:
                    raise ValueError("knowledge tag is too long")
                clean.append(value)
        if len(clean) > 10:
            raise ValueError("knowledge entry supports at most 10 tags")
        return clean

    @staticmethod
    def _summary(body: str) -> str:
        return re.sub(r"\s+", " ", body).strip()[:240]

    @staticmethod
    def _title_from_text(body: str, fallback: str) -> str:
        for line in body.splitlines():
            value = line.strip().lstrip("#").strip()
            if value:
                return value[:200]
        return fallback[:200]

    @staticmethod
    def _timestamp(value: float) -> str:
        return datetime.fromtimestamp(value, timezone.utc).isoformat()

    @staticmethod
    def _select_sql() -> str:
        return (
            "select ke.*,p.name project_name,d.name department_name,c.name company_name,"
            "b.name business_name,w.name workspace_name,"
            "(select count(*) from typed_object_references ur where ur.tenant_id=ke.tenant_id "
            "and ur.target_type='KNOWLEDGE' and ur.target_ref=ke.id and ur.relation='USES_REFERENCE') used_count "
            "from knowledge_entries ke "
            "left join projects p on p.tenant_id=ke.tenant_id and p.project_id=ke.project_id "
            "left join department_instances d on d.tenant_id=ke.tenant_id and d.id=ke.department_id "
            "left join companies c on c.tenant_id=ke.tenant_id and c.company_id=ke.company_id "
            "left join canonical_businesses b on b.tenant_id=ke.tenant_id and b.company_id=ke.company_id "
            "and ke.target_type='BUSINESS' and b.business_id=ke.target_ref "
            "left join workspaces w on w.tenant_id=ke.tenant_id and w.company_id=ke.company_id "
            "and ke.target_type='WORKSPACE' and w.workspace_id=ke.target_ref"
        )

    def _entry(self, row: Any, *, include_body: bool, query: str = "") -> dict[str, Any]:
        item = dict(row)
        item["tags"] = json.loads(item.pop("tags_json") or "[]")
        if item.get("target_type") in self.CANONICAL_TARGETS:
            item["scope"] = item["target_type"].lower()
            item["scope_status"] = "CANONICAL"
            item["scope_name"] = {
                "COMPANY": item.get("company_name"),
                "BUSINESS": item.get("business_name"),
                "WORKSPACE": item.get("workspace_name"),
            }.get(item["target_type"]) or "归属未知"
        else:
            item["scope"] = "project" if item.get("project_id") else "department" if item.get("department_id") else "company"
            item["scope_status"] = "LEGACY_UNMAPPED"
            item["scope_name"] = item.get("project_name") or item.get("department_name") or "旧公司资料"
        compact = re.sub(r"\s+", " ", item["body"]).strip()
        item["excerpt"] = self._match_excerpt(compact, query)
        item["source_available"] = self._source_available(item)
        item["source_status"] = "AVAILABLE" if item["source_available"] else "UNAVAILABLE"
        for name in ("project_name", "department_name", "company_name", "business_name", "workspace_name"):
            item.pop(name, None)
        if not include_body:
            item.pop("body", None)
            item.pop("content_sha256", None)
        return item

    @staticmethod
    def _match_excerpt(body: str, query: str) -> str:
        if not query:
            return body[:180]
        index = body.lower().find(query.lower())
        if index < 0:
            return body[:180]
        start = max(0, index - 60)
        return ("…" if start else "") + body[start : start + 180] + ("…" if start + 180 < len(body) else "")
