"""Resumable local first launch over canonical Company and Package primitives."""
import hashlib
import json

from .resource_scope_policy import ResourceScopePolicy
from .runtime import RuntimeFoundation, RuntimeScopeError
from .runtime.first_run_delivery import FirstRunDelivery, FirstGeneralWorkspaceDraft
from .tenant_context import TenantContext
from .writing_entry_service import WritingEntryService, ASSETS
from .content_growth_entry_service import ContentGrowthEntryService
from .music_entry_service import MusicEntryService
from .workspace_package_runtime import WorkspacePackageRuntime


class FirstLaunchService:
    def __init__(self, database):
        self.db = database
        self.foundation = RuntimeFoundation(database)

    def _actor(self):
        identity = TenantContext.current_identity()
        if identity.get('role', '').lower() not in {'ceo', 'owner'} or not identity.get('ceo_id'):
            raise RuntimeScopeError('只有公司所有者可以初始化本地工作空间。')
        return identity

    def _run(self, con, run_id, ceo, data):
        con.execute("insert or ignore into runtime_entities(entity_id,tenant_id,entity_type,owner_ref,lifecycle_status,data_json,created_at,updated_at) "
                    "values (?,?,'FOUNDING_RUN',?,'CEO_CONFIRMED',?,current_timestamp,current_timestamp)",
                    (run_id, TenantContext.current_tenant_id(), ceo, json.dumps(data, ensure_ascii=False)))

    def ensure(self):
        identity = self._actor()
        tenant, ceo = TenantContext.current_tenant_id(), identity['ceo_id']
        suffix = hashlib.sha256(f'{tenant}:{ceo}'.encode()).hexdigest()[:24]
        company = identity.get('company_id')
        with self.db.connect() as con:
            con.execute('begin immediate')
            row = con.execute('select company_id from companies where tenant_id=? and ceo_id=? ' +
                              ('and company_id=? ' if company else '') + 'order by is_default desc,created_at,company_id limit 1',
                              (tenant, ceo, company) if company else (tenant, ceo)).fetchone()
            if company and not row:
                raise RuntimeScopeError('当前公司不存在或无权访问。')
            company = row['company_id'] if row else f'company-launch-{suffix}'
            if not row:
                run = f'founding-launch-{suffix}'
                self._run(con, run, ceo, {'origin': 'T-011_FIRST_LAUNCH'})
                self.foundation._materialize_company_in_connection(con, run, company_id=company, ceo_id=ceo, name='我的公司')
        suffix = hashlib.sha256(f'{tenant}:{ceo}:{company}'.encode()).hexdigest()[:24]
        teams = []
        with TenantContext.scope(tenant, **{k: identity[k] for k in ('subject_id','ceo_id','role','membership_status','request_id')}, company_id=company):
            runtime = WorkspacePackageRuntime(self.db)
            delivery = FirstRunDelivery(self.db)
            for kind, name, service, source in (
                ('content_growth', '内容增长', ContentGrowthEntryService(self.db), 'content_growth_v02'),
                ('writing', '写作', WritingEntryService(self.db), 'writing_authoring'),
                ('music', '音乐创作', MusicEntryService(self.db), 'music'),
            ):
                run = f'founding-launch-{suffix}-{kind}'
                package_id = service.publication()['package_id']
                with self.db.connect() as con:
                    founding_run = con.execute(
                        "select 1 from runtime_entities where tenant_id=? and entity_id=? and entity_type='FOUNDING_RUN'",
                        (tenant, run),
                    ).fetchone()
                    existing = None
                    if not founding_run:
                        workspaces = con.execute(
                            "select workspace_id from workspace_package_instances where tenant_id=? and company_id=? "
                            "and package_id=? and status='ACTIVE' order by workspace_id",
                            (tenant, company, package_id),
                        ).fetchall()
                        for workspace in workspaces:
                            try:
                                existing = ResourceScopePolicy.resolve_execution_scope(
                                    con, tenant_id=tenant, company_id=company,
                                    scope_type='WORKSPACE', scope_ref=workspace['workspace_id'],
                                )
                            except ValueError:
                                continue
                            break
                if existing:
                    created = {key: existing[key] for key in ('company_id', 'business_id', 'workspace_id')}
                    teams.append(self._team_status(kind, name, service, company, created))
                    continue
                with self.db.connect() as con:
                    department = con.execute('select id from department_instances where tenant_id=? and company_id=? and department_type=? and deleted_at is null', (tenant, company, kind)).fetchone()
                if not department:
                    with self.db.connect() as con:
                        con.execute('begin immediate')
                        department_id = f'department-launch-{suffix}-{kind}'
                        con.execute("insert or ignore into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values (?,?,?,?,?,?,'active')", (department_id, tenant, company, f'official.department.{kind}', name, kind))
                        department = {'id': department_id}
                values = dict(intent=f'{name}本地工作', business_name=name, goal=f'完成{name}工作', positioning='本地创作', workspace_name=f'{name}工作台', package_id=package_id, department_id=department['id'])
                proposal = service.proposal(company, values)
                with self.db.connect() as con:
                    con.execute('begin immediate')
                    self._run(con, run, ceo, {'v1Proposal': proposal, 'origin': 'T-011_FIRST_LAUNCH'})
                draft = FirstGeneralWorkspaceDraft(company, ceo, '我的公司', name, name, values['goal'], values['positioning'], values['workspace_name'], intent_summary=values['intent'])
                result = delivery.materialize_package_for_existing_company(run, draft, package_runtime=runtime, source=ASSETS/source, definition=proposal['snapshot']['definition'], department_id=department['id'], proposal_sha256=proposal['proposal_sha256'])
                if result['activation'].get('status') != 'COMPLETED':
                    raise ValueError(f'{name}初始化未完成，保留原记录。')
                teams.append(self._team_status(kind, name, service, company, result['creation_result']))
        return {'company_id': company, 'teams': teams, 'next_action': 'OPEN_HOME'}

    @staticmethod
    def _team_status(kind, name, service, company, created):
        policy = service.execution_policy(company, created['workspace_id']) if kind == 'writing' else {
            'status': 'UNAVAILABLE', 'reason': '尚未连接并验证执行能力',
        }
        return {'kind': kind, 'name': name, **created, 'organization_status': 'READY',
                'execution': policy, 'status_label': '就绪' if policy.get('status') == 'AVAILABLE' else '待连接能力'}

    def save_draft(self, company, workspace, draft_id, text, expected_revision):
        from .runtime.child_work import CanonicalChildWorkRuntime
        self._actor()
        entry = WritingEntryService(self.db)
        entry.actor(company, write=True)
        with self.db.connect() as con:
            entry.local._scope(con, company, workspace, write=True)
            assignments = entry.assignments(con, company, workspace)
        if len(assignments) != 1:
            raise ValueError('写作责任身份不完整。')
        result = CanonicalChildWorkRuntime(self.db).create_cycle_work(company_id=company, workspace_id=workspace,
            assignment_ref=assignments[0]['entity_id'], release_key=f'writing-draft:{draft_id}',
            contract={'kind': 'WRITING_MANUSCRIPT_DRAFT', 'draft_id': draft_id})
        work = result['work']
        with self.db.connect() as con:
            con.execute('begin immediate')
            row = con.execute('select data_json,lifecycle_status from runtime_entities where tenant_id=? and entity_id=?',
                              (TenantContext.current_tenant_id(), work['entity_id'])).fetchone()
            data = json.loads(row['data_json'])
            previous = data.get('writingDraft', {'revision': 0, 'text': ''})
            if row['lifecycle_status'] != 'PLANNED':
                raise ValueError('任务已经开始，不能覆盖草稿。')
            if previous['revision'] != expected_revision:
                if previous['text'] == text:
                    return self.read_draft(company, workspace, work['entity_id'])
                raise ValueError('草稿已更新，请重新读取。')
            data['writingDraft'] = {'text': text, 'revision': expected_revision + 1}
            con.execute('update runtime_entities set data_json=?,updated_at=current_timestamp where tenant_id=? and entity_id=?',
                        (json.dumps(data, ensure_ascii=False), TenantContext.current_tenant_id(), work['entity_id']))
        return self.read_draft(company, workspace, work['entity_id'])

    def read_draft(self, company, workspace, work_id):
        self._actor()
        entry = WritingEntryService(self.db)
        entry.actor(company)
        with self.db.connect() as con:
            entry.local._scope(con, company, workspace)
        work = self.foundation.get(work_id)
        if (work['entity_type'] != 'WORK' or work['company_id'] != company or work['workspace_id'] != workspace
                or 'writingDraft' not in work['data']):
            raise RuntimeScopeError('草稿不属于当前工作空间。')
        policy = entry.execution_policy(company, workspace)
        return {'work': work, 'draft': work['data']['writingDraft'], 'execution': policy,
                'next_action': 'CONTINUE_TASK' if policy.get('status') == 'AVAILABLE' else 'CONFIGURE_MODEL',
                'return_to': {'company_id': company, 'workspace_id': workspace, 'work_id': work_id}}
