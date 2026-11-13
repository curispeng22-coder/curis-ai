"""Bounded Music entry over existing Package, scope, Assignment and model services."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from .runtime import RuntimeFoundation, RuntimeScopeError
from .resource_scope_policy import ResourceScopePolicy
from .tenant_context import TenantContext
from .result_attention import ResultAttention
from .model_preferences import TenantModelPreferenceResolver
from .employee_execution_identity import EmployeeExecutionIdentity
from .employee_templates import professional_team_contract
from .workspace_package_runtime import validate_package

PACKAGE_ID = "com.curis.local.music"
VERSION = "0.2.0"
LEGACY_VERSION = "0.1.0"
LEGACY_DIGEST = "5d9f36c36c2461f4540ad59277b56447a1a67cb2953759f43c52afbe5ed2cf76"
BINDINGS = {"MusicSong": "PACKAGE_DOMAIN_OBJECT", "MusicOperatingScope": "PACKAGE_DOMAIN_OBJECT"}
PURPOSE = "MUSIC_SONG_REPLY"
ASSETS = Path(__file__).resolve().parent / "bundled_workspace_packages"

class MusicEntryService:
    def __init__(self, database, *, execution_grant=None):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.models = TenantModelPreferenceResolver(database)
        self.execution_grant = execution_grant  # Server-owned; no client setter.

    def publication(self, *, candidate=False):
        release = json.loads((ASSETS / "music_release.json").read_text())
        package = validate_package(ASSETS / "music")
        if (release.get("packageId"), release.get("version"), release.get("digest")) != (PACKAGE_ID, VERSION, package["digest"]):
            raise ValueError("歌曲组件与版本依据不一致，不能启用。")
        if package["manifest"].get("canonicalEntityBindings") != BINDINGS:
            raise ValueError("歌曲组件缺少合法歌曲绑定。")
        published = release.get("published") is True
        decision = release.get("decision")
        if published:
            if (not isinstance(decision, dict) or decision.get("digest") != package["digest"]
                    or decision.get("kind") != "MUSIC_DEFINITION_PUBLICATION"
                    or not decision.get("sha256") or not decision.get("owner")):
                raise ValueError("缺少准确限定的歌曲定义发行决定。")
            relative = Path(decision.get("path", ""))
            if relative.is_absolute() or ".." in relative.parts or relative.parts[:2] != ("docs", "reviews"):
                raise ValueError("发行决定来源不合法。")
            source = ASSETS.parents[2] / relative
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != decision["sha256"]:
                raise ValueError("发行决定来源已改变。")
        if not published and not candidate:
            raise ValueError("音乐创作定义尚未正式发行，暂不能从普通入口启用。")
        return {"package_id": PACKAGE_ID, "version": VERSION, "digest": package["digest"],
                "name": "音乐创作工作空间", "published": published,
                "initial_team_contract": professional_team_contract(PACKAGE_ID, VERSION, package["digest"]),
                "scope": release["scope"], "notice": release["notice"]}

    def definitions(self, company):
        ResultAttention(self.db).actor(company)
        try:
            return {"available": True, "definition": self.publication()}
        except (ValueError, OSError) as error:
            return {"available": False, "definition": None, "notice": str(error)}

    def proposal(self, company, values):
        ResultAttention(self.db).actor(company)
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有公司所有者可以确认业务。")
        definition = self.publication()
        if values.get("package_id") != PACKAGE_ID:
            raise ValueError("组件与提案不一致。")
        with self.db.connect() as con:
            row = con.execute("select id from department_instances where tenant_id=? and company_id=? and id=? "
                "and deleted_at is null and enabled=1 and status!='archived'",
                (TenantContext.current_tenant_id(), company, values.get("department_id"))).fetchone()
        if not row:
            raise RuntimeScopeError("所属部门不在当前公司。")
        snapshot = {key: str(values.get(key) or "").strip() for key in
                    ("intent", "business_name", "goal", "positioning", "workspace_name")}
        snapshot.update(company_id=company, department_id=row["id"], package_id=PACKAGE_ID, definition=definition)
        digest = hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        return {**values, "snapshot": snapshot, "proposal_sha256": digest}

    def authoring_scope(self, company, workspace, *, connection=None, write=False):
        actor = ResultAttention(self.db).actor(company)
        if write and TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有公司所有者可以修改歌曲。")
        definition = self.publication(candidate=True)
        def read(con):
            scope = ResourceScopePolicy.resolve_execution_scope(con, tenant_id=TenantContext.current_tenant_id(),
                company_id=company, scope_type="WORKSPACE", scope_ref=workspace)
            department = con.execute("select id from department_instances where tenant_id=? and company_id=? and id=? "
                "and deleted_at is null and status!='archived' and enabled=1",
                (scope["tenant_id"], company, scope["department_id"])).fetchone()
            if not department:
                raise RuntimeScopeError("歌曲所属部门已停用或归档。")
            row = con.execute("select * from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (scope["tenant_id"], company, workspace)).fetchone()
            package = con.execute("select i.*,p.manifest_json,p.status definition_status from workspace_package_instances i "
                "join installed_workspace_packages p on p.tenant_id=i.tenant_id and p.package_id=i.package_id and p.version=i.package_version "
                "where i.tenant_id=? and i.company_id=? and i.workspace_id=?",
                (scope["tenant_id"], company, workspace)).fetchone()
            if not row or not package or package["status"] != "ACTIVE" or package["definition_status"] != "ACTIVE":
                raise RuntimeScopeError("歌曲工作空间不存在或已停用。")
            blueprint = json.loads(row["blueprint_json"])
            installed_version = package["package_version"]
            expected_digest = {VERSION: definition["digest"], LEGACY_VERSION: LEGACY_DIGEST}.get(installed_version)
            if (package["package_id"], package["package_digest"]) != (PACKAGE_ID, expected_digest):
                raise RuntimeScopeError("工作空间不属于当前准确歌曲组件。")
            if (blueprint.get("businessType"), blueprint.get("packageId"), blueprint.get("packageVersion"), blueprint.get("packageDigest")) != (
                    "PACKAGE", PACKAGE_ID, installed_version, expected_digest) or row["blueprint_version"] != installed_version:
                raise RuntimeScopeError("歌曲工作空间的版本或父级依据不一致。")
            if json.loads(package["manifest_json"]).get("canonicalEntityBindings") != (BINDINGS if installed_version == VERSION else {"MusicSong": "PACKAGE_DOMAIN_OBJECT"}):
                raise RuntimeScopeError("歌曲绑定不一致。")
            options = []
            rows = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and entity_type='RESPONSIBILITY_ASSIGNMENT' and lifecycle_status='ACTIVE'",
                (scope["tenant_id"], company, workspace)).fetchall()
            for assignment in rows:
                data = json.loads(assignment["data_json"])
                if data.get("responsibilityKey") != "MUSIC_SONG_AUTHOR":
                    continue
                context = ResourceScopePolicy.authorize_assignment(con, tenant_id=scope["tenant_id"], company_id=company,
                    assignment_ref=assignment["entity_id"], employee_ref=data.get("employeeRef"), scope=scope)
                identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace,
                    runtime_employee_ref=context["employee_ref"])
                if identity["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE":
                    options.append({**context, "name": identity["employee"]["name"],
                                    "company_employee_ref": identity["company_employee_ref"]})
            installed_definition = definition if installed_version == VERSION else {**definition, "version": LEGACY_VERSION, "digest": LEGACY_DIGEST, "published": False, "scope": "BOUNDED_FIRST_SONG_LOCAL_MEDIA_TEXT_DISCUSSION", "notice": "原版歌曲创作；经营依据需要准确新版本授权，未迁移历史。"}
            if installed_version == LEGACY_VERSION:
                installed_definition.pop("initial_team_contract", None)
            return {"scope": scope, "actor": actor, "definition": installed_definition, "blueprint_version": row["blueprint_version"],
                    "assignments": options, "publication_status": "PUBLISHED" if definition["published"] else "INTERNAL_CANDIDATE_NO_PUBLICATION"}
        if connection is not None:
            return read(connection)
        with self.db.connect() as con:
            return read(con)

    def prepare_model(self, company, workspace, assignment_ref, model_key):
        info = self.authoring_scope(company, workspace, write=True)
        assignment = next((a for a in info["assignments"] if a["assignment_ref"] == assignment_ref), None)
        if assignment is None:
            raise RuntimeScopeError("当前专业责任已变化。")
        return self.models.prepare_employee_model(company, workspace, assignment["employee_ref"], model_key, self.models.professional_grant(self.execution_grant, company, workspace, model_key))

    def execution_policy(self, company, workspace, assignment_ref, model_key, *, connection=None, attempt_id=None):
        info = self.authoring_scope(company, workspace, connection=connection, write=True)
        assignment = next((item for item in info["assignments"] if item["assignment_ref"] == assignment_ref), None)
        if not assignment:
            raise RuntimeScopeError("请先核对当前合法歌曲责任员工。")
        model = self.models._require_eligible_model(TenantContext.current_tenant_id(), model_key)
        def read(con):
            rows = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? "
                "and enabled=1 and capability_type='model' and capability_source=? and capability_id=?",
                (TenantContext.current_tenant_id(), assignment["company_employee_ref"], model["source"], model["model_key"])).fetchall()
            if len(rows) != 1:
                raise RuntimeScopeError("所选模型没有唯一有效的员工能力授权。")
            return dict(rows[0])
        if connection is not None:
            binding = read(connection)
        else:
            with self.db.connect() as con:
                binding = read(con)
        grant = self.models.professional_grant(self.execution_grant, company, workspace, model_key, attempt_id=attempt_id, connection=connection)
        if (not isinstance(grant, dict) or grant.get("tenant_id") != TenantContext.current_tenant_id()
                or grant.get("company_id") != company or grant.get("workspace_id") != workspace
                or grant.get("model_key") != model_key or not grant.get("grant_ref")
                or grant.get("effective_system_authorization") is not True
                or type(grant.get("max_output_tokens")) is not int or not 1 <= grant["max_output_tokens"] <= 2048
                or type(grant.get("max_input_bytes")) is not int or not 1 <= grant["max_input_bytes"] <= 50000
                or any(type(grant.get(k)) not in {int, float} or not math.isfinite(grant[k]) or grant[k] < 0 for k in
                       ("max_cost_usd", "price_upper_bound_usd_per_input_byte", "price_upper_bound_usd_per_output_token"))
                or not grant.get("price_version")):
            raise RuntimeScopeError("本地编辑可继续；员工建议尚未获本次费用与系统授权。")
        with self.db.connect() as con:
            rows = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.execution_bound' "
                "and json_extract(payload,'$.execution_selection.grant.grant_ref')=?",
                (TenantContext.current_tenant_id(), grant["grant_ref"])).fetchall()
        if any(json.loads(row["payload"])["attempt_id"] != attempt_id for row in rows):
            raise RuntimeScopeError("这次单次授权已使用，请核验原请求。")
        return {"context": assignment, "model": model, "binding": binding, "grant": dict(grant)}

    def validate_execution_selection(self, selection, *, attempt_id=None, connection=None):
        if selection.get('purpose') != PURPOSE:
            raise RuntimeScopeError('歌曲执行用途不合法。')
        from .music_service import MusicService
        service = MusicService(self.db, entry=self, media=getattr(self, 'media', None))
        scope = selection['scope']
        def validate(con):
            service.conversations.validate_model_work(con, selection, attempt_id=attempt_id)
            info = self.authoring_scope(scope['company_id'], scope['workspace_id'], connection=con, write=True)
            if info['scope'] != scope:
                raise RuntimeScopeError('原请求范围已改变。')
            if service.pending(scope, connection=con, except_attempt=attempt_id):
                raise RuntimeScopeError('工作空间有原请求待核验，不能换歌、员工或模型重新执行。')
            row = service.content(scope['company_id'], scope['workspace_id'], selection['song_ref'], connection=con)
            service.basis(con, scope['company_id'], scope['workspace_id'], row['song'], selection['expected'])
            service.selection(scope['company_id'], scope['workspace_id'], selection['song_ref'], selection['selection'], connection=con)
            if service.resolve_references(scope, selection['references']) != selection['references']:
                raise RuntimeScopeError('原请求引用资格已改变。')
            policy = self.execution_policy(scope['company_id'], scope['workspace_id'], selection['context']['assignment_ref'], selection['model']['model_key'], connection=con, attempt_id=attempt_id)
            if policy['binding']['id'] != selection['binding_id'] or policy['model'] != selection['model'] or policy['grant'] != selection['grant']:
                raise RuntimeScopeError('原请求模型或授权已改变。')
            if {k:policy['context'][k] for k in selection['context']} != selection['context']:
                raise RuntimeScopeError('原请求责任已改变。')
        if connection is not None:
            validate(connection)
        else:
            with self.db.connect() as con:
                validate(con)
