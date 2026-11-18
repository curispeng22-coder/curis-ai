"use client";

import Link from "next/link";
import { Suspense, useEffect, useState, useRef, useLayoutEffect } from "react";
import { useSearchParams } from "next/navigation";

import TeamOperatingDefinitionEditor from "../../../components/workspace/TeamOperatingDefinitionEditor.js";
import TerraShell from "../../../components/terra/TerraShell.js";
import { CreateBusiness } from "../../../components/v1/CeoDeskOperating.js";
import BusinessCatalogSurface, { BusinessCatalogPaneContent, businessCatalogHref, businessCatalogSelection } from "../../../components/v1/BusinessCatalogSurface.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import { TerraCard, TerraPageHead, TerraTag } from "../../../components/terra/TerraPrimitives.js";
import { getCanonicalBusinesses, getOrganizationProjection, runtimeErrorMessage, workspaceOfficeHref } from "../../../lib/runtimeApi.js";
import { createAssignedWork, getBusinessDefinitions } from "../../../lib/v1FrontendApi.js";
import { buildOrganizationProjection } from "../../../lib/organizationProjection.js";

import { CEO_ID } from "../../../lib/api.js";
import { getInstalledWorkspace, completeInstalledWorkspaceInitialTeam } from "../../../lib/workspacePackageApi.js";
import { isMusicPackage } from "../../../lib/musicState.mjs";
import { isWritingPackage } from "../../../lib/writingState.mjs";
import { isContentGrowthPackage } from "../../../lib/contentGrowthState.mjs";

const STATUS = { DRAFT: ["草拟中", "grey"], ACTIVE: ["经营中", "green"], PAUSED: ["已暂停", "amber"], ARCHIVED: ["已归档", "grey"] };
const statusTag = (value) => STATUS[String(value || "").toUpperCase()] || ["状态未知", "grey"];

function BusinessSurface() {
  const runtime = useRuntime();
  const searchParams = useSearchParams();
  const [view, setView] = useState({ companyId: "", status: "idle", businesses: [], error: "" });
  const [definitionRead, setDefinitionRead] = useState({ companyId: "", status: "idle", payload: null });
  const [organization, setOrganization] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [engineeringLeader, setEngineeringLeader] = useState(null);
  const delegationLock = useRef(false);
  const [delegation, setDelegation] = useState({ companyId: runtime.companyId, goal: "", busy: false, work: null, error: "", request: "", pending: null, uncertain: false });
  const delegate = async (event) => {
    event.preventDefault();
    const leader = engineeringLeader;
    if (!leader || leader.entity_type !== "RESPONSIBILITY_ASSIGNMENT" || leader.company_id !== runtime.companyId || leader.lifecycle_status !== "ACTIVE" || !leader.data?.employeeRef || !leader.data?.companyEmployeeRef || !leader.data?.scopeType || !leader.data?.scopeRef || delegationLock.current || delegation.busy || delegation.work || delegation.pending || !delegation.goal.trim()) return;
    delegationLock.current = true;
    const payload = { problem: delegation.goal.trim(), expected_result: "形成可供 CEO 确认的业务与空间建设建议", request_id: delegation.request || crypto.randomUUID() };
    const companyId = runtime.companyId;
    setDelegation((current) => ({ ...current, busy: true, error: "", request: payload.request_id, pending: payload }));
    try {
      const created = await createAssignedWork(leader.entity_id, payload);
      const { cycle, work } = created || {};
      if (!cycle?.entity_id || !work?.entity_id || cycle.entity_type !== "CYCLE" || work.entity_type !== "WORK"
        || cycle.data?.kind !== "GENERAL_WORK_CYCLE" || work.data?.kind !== "CANONICAL_CHILD_WORK"
        || !leader.tenant_id || cycle.tenant_id !== leader.tenant_id || work.tenant_id !== leader.tenant_id
        || cycle.company_id !== companyId || work.company_id !== companyId || cycle.workspace_id !== work.workspace_id || cycle.workspace_id !== leader.workspace_id
        || work.parent_id !== cycle.entity_id || work.data?.cycleRef !== cycle.entity_id
        || cycle.data?.scopeType !== leader.data.scopeType || cycle.data?.scopeRef !== leader.data.scopeRef
        || work.data?.scopeType !== cycle.data.scopeType || work.data?.scopeRef !== cycle.data.scopeRef
        || cycle.data?.releaseKey !== payload.request_id || cycle.data?.contract?.problem !== payload.problem
        || cycle.data?.contract?.expectedResult !== payload.expected_result
        || !Array.isArray(cycle.data?.contract?.constraints) || cycle.data.contract.constraints.length
        || !Array.isArray(cycle.data?.contract?.references) || cycle.data.contract.references.length
        || work.data?.releaseKey !== "initial" || work.data?.responsibilityAssignmentRef !== leader.entity_id || work.data?.holderEmployeeRef !== leader.data.employeeRef
        || work.owner_ref !== leader.data.employeeRef || work.data?.responsibilityKey !== leader.data.responsibilityKey
        || work.data?.responsibility !== leader.data.responsibility || work.data?.assignmentRevision !== leader.data.revision) throw new Error("WORK_RECEIPT_UNVERIFIED");
      setDelegation((current) => current.companyId === companyId && current.pending?.request_id === payload.request_id
        ? { ...current, busy: false, work, error: "", uncertain: false } : current);
    } catch (error) {
      const rejected = [401, 403, 404, 422].includes(error?.status || error?.statusCode);
      setDelegation((current) => current.companyId === companyId && current.pending?.request_id === payload.request_id
        ? { ...current, busy: false, pending: rejected ? null : current.pending, request: rejected ? "" : current.request,
          uncertain: !rejected, error: rejected ? "当前委托未获受理；目标已保留，请核对负责人及范围。" : "委托记录结果尚未确认；原目标与请求已保留。请从合法工作入口核对，不要重复提交。" } : current);
    } finally { delegationLock.current = false; }
  };

  useEffect(() => {
    setEngineeringLeader(null); setOrganization(null);
    setDelegation({ companyId: runtime.companyId, goal: "", busy: false, work: null, error: "", request: "", pending: null, uncertain: false });
    if (!runtime.companyId) return;
    let active = true;
    getOrganizationProjection(runtime.companyId).then((payload) => {
      if (active) setOrganization(payload.company?.company_id === runtime.companyId ? payload : null);
      const holders = (payload.departmentAssignments || []).filter((item) =>
        item.company_id === runtime.companyId && item.lifecycle_status === "ACTIVE"
        && item.data?.scopeType === "DEPARTMENT" && item.data?.scopeRef
        && item.data?.responsibilityKey === "space.engineering.leadership" && item.data?.isLeader);
      if (active) setEngineeringLeader(payload.company?.company_id === runtime.companyId && holders.length === 1 ? holders[0] : null);
    }).catch(() => { if (active) { setEngineeringLeader(null); setOrganization(null); } });
    return () => { active = false; };
  }, [runtime.companyId, refreshKey]);

  useEffect(() => {
    let active = true;
    if (runtime.status !== "ready" || !runtime.companyId) return () => { active = false; };
    setView((current) => current.companyId === runtime.companyId && current.status === "ready"
      ? current : { companyId: runtime.companyId, status: "loading", businesses: [], error: "" });
    setDefinitionRead({ companyId: runtime.companyId, status: "loading", payload: null });
    getCanonicalBusinesses(runtime.companyId).then((payload) => {
      if (active) setView({ companyId: runtime.companyId, status: "ready", businesses: (payload.businesses || []).filter((item) => item.company_id === runtime.companyId), error: "" });
    }).catch((error) => {
      if (active) setView({ companyId: runtime.companyId, status: error?.status === 403 || error?.status === 404 ? "forbidden" : "error", businesses: [], error: runtimeErrorMessage(error) });
    });
    getBusinessDefinitions(runtime.companyId).then((payload) => {
      if (active) setDefinitionRead({ companyId: runtime.companyId, status: "ready", payload });
    }).catch(() => {
      if (active) setDefinitionRead({ companyId: runtime.companyId, status: "error", payload: null });
    });
    return () => { active = false; };
  }, [runtime.companyId, runtime.status, refreshKey]);

  if (["idle", "loading"].includes(runtime.status)) return <RuntimeLoading label="正在读取业务…" />;
  if (["error", "forbidden"].includes(runtime.status)) return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  if (!runtime.snapshot?.company) return <RuntimeEmpty title="公司尚未建立" description="先完成公司创办，再进入业务空间。" action={<Link href="/onboarding" className="font-bold text-ui-primary">开始创办公司</Link>} />;
  if (view.companyId !== runtime.companyId || ["idle", "loading"].includes(view.status)) return <RuntimeLoading label="正在读取业务…" />;
  if (["error", "forbidden"].includes(view.status)) return <RuntimeError message={view.error} forbidden={view.status === "forbidden"} />;
  const selection = businessCatalogSelection(searchParams, runtime.companyId, view.businesses);
  const directoryHref = businessCatalogHref(runtime.companyId);
  const recordRuns = searchParams.getAll("founding_run_id");
  const recordModes = searchParams.getAll("creation_record");
  const recordOnly = recordModes.length > 0;
  const records = organization?.company?.company_id === runtime.companyId
    ? (organization.businesses || []).filter((item) => item.company_id === runtime.companyId && item.creation_record && item.creation_record.founding_run_id === recordRuns[0]
      && item.creation_record.company_id === runtime.companyId && item.creation_record.business_id === item.business_id
      && item.workspaces?.some((workspace) => workspace.workspace_id === item.creation_record.workspace_id)) : [];
  const originalRecord = recordModes.length === 1 && recordModes[0] === "1" && recordRuns.length === 1 && records.length === 1 ? records[0].creation_record : null;
  const panes = <BusinessCatalogPaneContent company={runtime.snapshot.company} businesses={view.businesses} organization={organization} definitions={definitionRead.companyId === runtime.companyId ? definitionRead.payload : null} definitionStatus={definitionRead.companyId === runtime.companyId ? definitionRead.status : "loading"} selection={selection} />;
  if (selection.kind === "invalid") return <section><Link href={directoryHref} className="text-ui-primary">← 返回业务目录</Link><RuntimeEmpty title="无法确认原业务" description="当前公司或业务已经变化，请从目录重新选择。" /></section>;
  if (["directory", "definition"].includes(selection.kind)) return <>{panes}<BusinessCatalogSurface company={runtime.snapshot.company} businesses={view.businesses} organization={organization} definitions={definitionRead.companyId === runtime.companyId ? definitionRead.payload : null} definitionStatus={definitionRead.companyId === runtime.companyId ? definitionRead.status : "loading"} definitionId={selection.definitionId} /></>;
  if (selection.kind === "create") return <>{panes}<section>
    {recordOnly ? organization === null ? <RuntimeLoading label="正在查证原创建记录…" /> : !originalRecord ? <RuntimeEmpty title="无法确认原创建记录" description="当前公司没有唯一可查证的原业务记录，请从业务详情重新进入。" /> : <><Link href={businessCatalogHref(runtime.companyId, { businessId: originalRecord.business_id })} className="mb-4 inline-block text-ui-primary">← 返回原业务</Link><h1 className="mb-3 text-2xl font-semibold">本次创建记录</h1><CreateBusiness key={`${runtime.companyId}:${originalRecord.founding_run_id}`} company={runtime.snapshot.company} originalRecord={originalRecord} /></> : <>
    <Link href={directoryHref} className="mb-4 inline-block text-ui-primary">← 返回业务目录</Link>
    <h1 className="mb-3 text-2xl font-semibold">{view.businesses.length ? "创建业务" : "当前还没有经营业务"}</h1>
    <p className="mb-4 text-ui-txt-2">可以直接提出目标，确认后建立业务与第一个工作空间，具体类型以提案为准。</p>
    {engineeringLeader?.company_id === runtime.companyId && delegation.companyId === runtime.companyId && <details className="mb-4">
      <summary className="cursor-pointer text-ui-primary">委托空间工程团队</summary>
      <form onSubmit={delegate} className="mt-3 space-y-3">
        <label className="block text-sm">新业务或空间目标<input aria-label="委托空间工程的目标" value={delegation.goal}
          disabled={Boolean(delegation.work) || delegation.busy || delegation.uncertain} onChange={(event) => setDelegation((current) => ({ ...current, goal: event.target.value, request: "" }))}
          className="mt-2 block w-full rounded-lg border border-ui-line bg-ui-surface p-3" /></label>
        <button disabled={delegation.busy || delegation.uncertain || Boolean(delegation.work) || !delegation.goal.trim()} className="rounded-lg bg-ui-primary px-4 py-2 text-sm text-ui-primary-fg disabled:opacity-40">{delegation.busy ? "正在记录…" : "交给空间工程负责人"}</button>
        {delegation.work ? <div role="status" className="space-y-1 text-sm text-ui-txt-2"><strong>委托已记录</strong><p>目标：{delegation.pending?.problem}</p><p>当前责任：{delegation.work.data.responsibility || "空间工程负责人"}</p><p>工作状态：{{ PLANNED: "尚未执行", READY: "待执行", ACTIVE: "执行中", WAITING: "等待中", BLOCKED: "暂时受阻", PAUSED: "已暂停", COMPLETED: "已完成", FAILED: "执行失败", CANCELLED: "已取消", ARCHIVED: "已归档" }[delegation.work.lifecycle_status] || "状态待核对"}。本页回执仅保留在当前页面，实际进展以原工作为准。</p></div> : null}
        {delegation.error ? <p role="alert" className="text-sm text-ui-red">{delegation.error}</p> : null}
      </form>
      <Link className="mt-3 inline-block text-ui-primary" href={`/ceo-office/organization/employees/${encodeURIComponent(engineeringLeader.data.companyEmployeeRef)}`}>与负责人继续讨论 →</Link>
    </details>}
    <CreateBusiness key={`${runtime.companyId}:${selection.sourceDefinition || "generic"}`} sourceDefinition={selection.sourceDefinition || ""} company={runtime.snapshot.company} onCreated={() => setRefreshKey((value) => value + 1)} />
    </>}
  </section></>;

  const business = selection.business;
  const currentTeam = organization?.company?.company_id === runtime.companyId
    ? buildOrganizationProjection(organization).businessById.get(business.business_id) : null;
  const creationRecord = organization?.company?.company_id === runtime.companyId
    ? organization.businesses?.find((item) => item.company_id === runtime.companyId && item.business_id === business.business_id)?.creation_record : null;
  const [statusLabel, statusColor] = statusTag(business.lifecycle_status);

  return <>
    {panes}
    <Link href={directoryHref} className="mb-4 inline-block text-ui-primary">← 返回业务目录</Link>
    <TerraPageHead title={business.name} subtitle={`${business.parentPath?.department?.name || "所属部门未知"} · 业务经营说明`} facts={[
      { value: business.workspaces?.length || 0, label: "工作空间" },
      { value: business.operatingSummary?.resultCount ?? "未知", label: "已有结果" },
      { value: business.operatingSummary?.needsAttentionCount ?? "未知", label: "需要关注" },
    ]} actions={view.businesses.length > 1 ? <nav aria-label="切换业务" className="flex flex-wrap gap-2">{view.businesses.map((item) => <Link key={item.business_id} href={businessCatalogHref(runtime.companyId, { businessId: item.business_id })} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-bold text-ui-txt-2 no-underline">{item.name}</Link>)}</nav> : null} />

    <Link href={businessCatalogHref(runtime.companyId, { create: true })} className="mb-4 inline-block text-ui-primary">创建另一项业务</Link>
    {creationRecord?.company_id === runtime.companyId && creationRecord.business_id === business.business_id
      && business.workspaces?.some((workspace) => workspace.workspace_id === creationRecord.workspace_id)
      ? <Link href={`${businessCatalogHref(runtime.companyId, { create: true })}&${new URLSearchParams({ creation_record: "1", founding_run_id: creationRecord.founding_run_id })}`} className="mb-4 ml-4 inline-block text-ui-primary">查看创建记录</Link>
      : <p role="status" className="mb-4 text-sm text-ui-txt-3">原创建记录暂不可查证，请核对现有业务。</p>}
    <div className="grid gap-4">
      <TerraCard>
        <div className="flex items-start justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">业务定义</p><h2 className="mt-1 text-ui-5 font-semibold text-ui-txt">{business.definition?.name || business.name}</h2></div><TerraTag color={statusColor}>{statusLabel}</TerraTag></div>
        <dl className="mt-4 grid gap-3 md:grid-cols-2"><div><dt className="text-ui-1 text-ui-txt-3">整体目标</dt><dd className="mt-1 text-ui-2 text-ui-txt">{business.definition?.goal || "尚未形成"}</dd></div><div><dt className="text-ui-1 text-ui-txt-3">业务定位</dt><dd className="mt-1 text-ui-2 text-ui-txt">{business.definition?.positioning || "尚未形成"}</dd></div></dl>
      </TerraCard>

      <TerraCard>
        <p className="text-ui-1 font-bold text-ui-primary">经营状态</p>
        <div className="mt-3 grid gap-3 sm:grid-cols-3"><div><span className="text-ui-1 text-ui-txt-3">工作空间</span><strong className="mt-1 block text-ui-4 text-ui-txt">{business.operatingSummary?.workspaceCount ?? 0}</strong></div><div><span className="text-ui-1 text-ui-txt-3">结果</span><strong className="mt-1 block text-ui-4 text-ui-txt">{business.operatingSummary?.resultCount ?? "未知"}</strong></div><div><span className="text-ui-1 text-ui-txt-3">需要关注</span><strong className="mt-1 block text-ui-4 text-ui-txt">{business.operatingSummary?.needsAttentionCount ?? "未知"}</strong></div></div>
      </TerraCard>

      <TerraCard>
        <div className="flex items-center justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">工作空间目录</p><h2 className="mt-1 text-ui-4 font-semibold text-ui-txt">独立经营空间</h2></div><span className="text-ui-1 text-ui-txt-3">首个工作空间随业务建立；更多空间暂不支持创建</span></div>
        {business.workspaces?.length ? <ul className="mt-3 divide-y divide-ui-line">{business.workspaces.map((workspace) => <li key={workspace.workspace_id} className="flex flex-wrap items-center justify-between gap-3 py-3"><div><strong className="text-ui-2 text-ui-txt">{workspace.name}</strong><p className="mt-1 text-ui-1 text-ui-txt-3">{statusTag(workspace.status)[0]} · 更新于 {workspace.updated_at || "未知"}</p></div><Link href={workspaceOfficeHref(workspace)} className="text-ui-1 font-bold text-ui-primary no-underline">进入工作空间 →</Link></li>)}</ul> : <p className="mt-3 text-ui-2 text-ui-txt-3">关系中没有可用工作空间；不会从旧项目补造目录。</p>}
      </TerraCard>

      <TerraCard>
        <p className="text-ui-1 font-bold text-ui-primary">业务团队</p>
        {currentTeam && !currentTeam.assignments.length && <InitialTeamCompletion key={`${runtime.companyId}:${business.business_id}`} companyId={runtime.companyId} business={business} onChanged={() => setRefreshKey(value => value + 1)} />}
        {currentTeam?.assignments.length ? <><p className="mt-2 text-ui-1 text-ui-txt-3">{currentTeam.staffingCount} 名当前员工 · {currentTeam.roleCount} 项责任；责任安排不代表模型、工具或执行已可用。</p><ul className="mt-3 grid gap-2 md:grid-cols-2">{currentTeam.assignments.map((member) => <li key={member.assignmentRef} className="rounded-ui-sm bg-ui-surface-2 p-3"><strong className="text-ui-2 text-ui-txt">{member.employee ? <Link href={`/ceo-office/organization/employees/${encodeURIComponent(member.employeeRef)}?${new URLSearchParams({ company_id: runtime.companyId, business_id: business.business_id })}#employee-conversation`}>{member.employee.name} · {member.roleName}</Link> : "当前员工身份无法确认"}</strong><p className="mt-1 text-ui-1 text-ui-txt-3">{member.responsibility || "责任尚未记录"}</p>{!member.enabled && <p role="status" className="mt-1 text-ui-1 text-ui-txt-3">当前责任员工或岗位不可用，请核对安排。</p>}</li>)}</ul></> : <p className="mt-3 text-ui-2 text-ui-txt-3">{currentTeam ? "这项业务尚未设置团队责任。" : "当前团队资料暂不可读取，请重新读取。"}</p>}
      {currentTeam?.assignments.some(member => member.enabled && member.isLeader && member.scopeType === "BUSINESS" && member.scopeRef === business.business_id)
        && business.workspaces?.some(workspace => workspace.package_id === "com.curis.local.music" && !["ARCHIVED", "DISABLED"].includes(workspace.status))
        && <TeamOperatingDefinitionEditor key={`${runtime.companyId}:${business.business_id}`}
          companyId={runtime.companyId} musicBusinessRef={business.business_id} onPublished={() => setRefreshKey(value => value + 1)} />}
      </TerraCard>
    </div>
  </>;
}

export function InitialTeamCompletion({ companyId, business, onChanged }) {
  const workspaceId = business.workspaces?.length === 1 ? business.workspaces[0].workspace_id : "";
  const identity = JSON.stringify([companyId, business.business_id, workspaceId]), active = useRef(identity);
  useLayoutEffect(() => { active.current = identity; return () => { active.current = ""; }; }, [identity]);
  const storage = `curis.professional.team.${identity}`;
  const [detailRead, setDetail] = useState(null), [consent, setConsent] = useState(false), [pending, setPending] = useState(false), [notice, setNotice] = useState("");
  const detail = detailRead?.identity === identity ? detailRead.value : null;
  useEffect(() => {
    let current = true; setDetail(null); setConsent(false); setNotice("");
    try { setPending(Boolean(sessionStorage.getItem(storage))); } catch { setPending(true); setNotice("无法保留原请求，暂不能提交。"); }
    if (workspaceId) getInstalledWorkspace(workspaceId).then(value => {
      if (current && value.instance?.company_id === companyId && value.instance?.workspace_id === workspaceId && value.instance.status === "ACTIVE" && !value.read_only && (isMusicPackage(value) || isWritingPackage(value) || isContentGrowthPackage(value))) setDetail({identity,value});
    }).catch(() => { if (current) setNotice("专业工作空间资料暂不可读取。"); });
    return () => { current = false; };
  }, [companyId, workspaceId, storage, identity]);
  const complete = async () => {
    if (!consent || pending || !detail) return;
    const key = identity, payload = {company_id:companyId,ceo_id:CEO_ID,request_id:crypto.randomUUID(),expected:{business_id:business.business_id,package_id:detail.package.package_id,version:detail.package.version,digest:detail.package.digest,assignments:[]}};
    try { sessionStorage.setItem(storage,JSON.stringify(payload)); } catch { setNotice("无法保存原请求，未提交。"); return; }
    setPending(true); setNotice("正在确认初始团队…");
    try {
      await completeInstalledWorkspaceInitialTeam(workspaceId,payload);
      if (active.current !== key) return;
      sessionStorage.removeItem(storage); setNotice("已保留团队创建回执，正在读取当前安排。"); onChanged();
    } catch { if (active.current === key) setNotice("原请求未完成或结果待核验，请读取当前团队；不会重复提交。"); }
  };
  if (!detail) return notice ? <p role="status">{notice}</p> : null;
  return <section aria-label="补齐真实初始团队" className="mt-3"><p>为此专业业务建立一名真实负责人，兼业务负责人和工作空间创作职责。模型、工具及执行授权另需配置。</p><label className="mt-2 flex gap-2"><input type="checkbox" checked={consent} disabled={pending} onChange={e => setConsent(e.target.checked)} />我确认按已批准的初始职责补齐当前空团队，不改已有业务与正文。</label><button disabled={pending || !consent} onClick={complete}>确认补齐初始团队</button>{pending && <button onClick={onChanged}>只读查询当前团队</button>}{notice && <p role="status">{notice}</p>}</section>;
}

export default function BusinessPage() {
  return <TerraShell topCrumb="业务空间 · 业务" assistantContext={{ page: "business" }}><Suspense fallback={<RuntimeLoading label="正在打开业务…" />}><BusinessSurface /></Suspense></TerraShell>;
}
