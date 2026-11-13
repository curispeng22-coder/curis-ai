"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { CEO_ID } from "../../lib/api.js";
import {
  createInstalledWorkspaceObject,
  getInstalledWorkspace,
} from "../../lib/workspacePackageApi.js";
import WorkspacePaneShell from "./WorkspacePaneShell.js";
import ContentGrowthWorkspace from "../content-growth/ContentGrowthWorkspace.js";
import MusicWorkspace from "../music/MusicWorkspace.js";
import { isMusicPackage } from "../../lib/musicState.mjs";
import { isContentGrowthPackage } from "../../lib/contentGrowthState.mjs";
import WritingWorkspace from "../writing/WritingWorkspace.js";
import { isWritingPackage } from "../../lib/writingState.mjs";

const CORE_REFERENCE_FIELDS = new Set(["responsibilityRef", "evidenceRef"]);

function surfacePreferenceKey(workspaceId) {
  return `curis.workspace-surface.${CEO_ID}.${workspaceId}`;
}

function ProjectionList({ items, empty }) {
  if (!items?.length) return <p className="p-6 text-center text-ui-2 text-ui-txt-3">{empty}</p>;
  return (
    <div className="divide-y divide-ui-line rounded-ui-sm border border-ui-line bg-ui-surface">
      {items.map((item) => (
        <article key={item.object_ref || item.reference_id} className="p-4">
          <p className="text-ui-2 font-semibold text-ui-txt">{item.summary || item.activity || item.object_ref || item.reference_id}</p>
          <p className="mt-1 break-all text-ui-1 text-ui-txt-3">{item.object_type || item.kind} · {item.work_status || item.status}</p>
        </article>
      ))}
    </div>
  );
}

function DomainContext({ model, selectedKey, selectedSurface, selectedObject, schema, onSelect }) {
  return (
    <div className="space-y-4">
      <nav aria-label="Workspace Domain Navigation" className="space-y-1">
        {model.domainNavigation.map((item) => (
          <button
            key={item.key}
            type="button"
            onClick={() => onSelect(item.surfaceRef)}
            aria-current={selectedKey === item.surfaceRef ? "page" : undefined}
            className={`w-full rounded-ui-sm border px-3 py-2 text-left text-ui-2 ${selectedKey === item.surfaceRef ? "border-ui-primary bg-ui-surface text-ui-txt" : "border-transparent text-ui-txt-2 hover:bg-ui-surface"}`}
          >
            <span className="block font-semibold">{item.label}</span>
            <span className={`mt-1 block text-ui-1 ${item.eligible ? "text-ui-success" : "text-ui-danger"}`}>{item.status}</span>
          </button>
        ))}
      </nav>
      <div className="rounded-ui-sm border border-ui-line bg-ui-surface p-3">
        <p className="text-ui-1 font-bold uppercase tracking-wide text-ui-txt-3">Current Surface</p>
        <p className="mt-1 text-ui-2 font-semibold text-ui-txt">{selectedSurface?.purpose || "Workspace Gap"}</p>
        <p className="mt-1 text-ui-1 text-ui-txt-3">{selectedSurface?.status || "WORKSPACE_GAP"}</p>
      </div>
      {schema && <ObjectDetail object={selectedObject} schema={schema} />}
    </div>
  );
}

function ObjectDetail({ object, schema }) {
  if (!object) return <p className="p-4 text-ui-2 text-ui-txt-3">选择一条记录查看业务真相。</p>;
  return (
    <dl className="space-y-3 p-4">
      {Object.entries(schema?.properties || {}).map(([name, field]) => (
        <div key={name}>
          <dt className="text-ui-1 font-semibold text-ui-txt-3">{field.title}</dt>
          <dd className="mt-1 break-words text-ui-2 text-ui-txt">{object.data?.[name] || "未记录"}</dd>
        </div>
      ))}
      <div><dt className="text-ui-1 font-semibold text-ui-txt-3">对象 ID</dt><dd className="mt-1 break-all text-ui-1 text-ui-txt-2">{object.object_id}</dd></div>
      <div><dt className="text-ui-1 font-semibold text-ui-txt-3">责任引用</dt><dd className="mt-1 break-all text-ui-1 text-ui-txt-2">{object.owner_ref || "未分配"}</dd></div>
      <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
        <dt className="text-ui-1 font-semibold text-ui-txt-3">Company OS Integration</dt>
        <dd className="mt-2 space-y-1 break-all text-ui-1 text-ui-txt-2">
          <p>{object.company_integration?.status || "NOT_STARTED"} · {object.company_integration?.resolvable ? "Core refs resolved" : "等待 Core 关系"}</p>
          {object.company_integration?.responsibility?.roleSlotRef && <p>Responsibility: {object.company_integration.responsibility.roleSlotRef}</p>}
          {object.company_integration?.employee?.employeeRef && <p>Employee: {object.company_integration.employee.employeeRef}</p>}
          {object.company_integration?.capability?.bindingRef && <p>Capability: {object.company_integration.capability.bindingRef}</p>}
          {object.company_integration?.task?.task_id && <p>Task: {object.company_integration.task.task_id}</p>}
          {object.company_integration?.execution?.execution_id && <p>Execution: {object.company_integration.execution.execution_id}</p>}
          {object.company_integration?.evidenceRefs?.length > 0 && <p>Evidence: {object.company_integration.evidenceRefs.join(", ")}</p>}
          {object.company_integration?.resultRefs?.length > 0 && <p>Result: {object.company_integration.resultRefs.join(", ")}</p>}
        </dd>
      </div>
    </dl>
  );
}

function CreateForm({ schema, title, busy, error, onSubmit }) {
  const defaults = useMemo(() => Object.fromEntries(
    Object.entries(schema?.properties || {}).filter(([, field]) => "default" in field).map(([name, field]) => [name, field.default]),
  ), [schema]);
  const [values, setValues] = useState(defaults);

  useEffect(() => setValues(defaults), [defaults]);

  return (
    <form className="space-y-3 p-4" onSubmit={(event) => { event.preventDefault(); onSubmit(values); }}>
      <p className="text-ui-2 font-semibold text-ui-txt">{title}</p>
      {Object.entries(schema?.properties || {}).map(([name, field]) => {
        if (CORE_REFERENCE_FIELDS.has(name)) return (
          <label key={name} className="block text-ui-1 font-semibold text-ui-txt-2">
            {field.title}
            <input disabled value="由 Company OS 在解析真实关系后写入" className="mt-1 min-h-9 w-full rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2 text-ui-2 text-ui-txt-3" readOnly />
          </label>
        );
        const common = {
          id: `package-field-${name}`,
          required: schema.required?.includes(name),
          value: values[name] || "",
          onChange: (event) => setValues((current) => ({ ...current, [name]: event.target.value })),
          className: "mt-1 min-h-9 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-2 text-ui-txt outline-none focus:border-ui-accent",
        };
        return (
          <label key={name} htmlFor={common.id} className="block text-ui-1 font-semibold text-ui-txt-2">
            {field.title}
            {field.enum ? (
              <select {...common}><option value="">请选择</option>{field.enum.map((value) => <option key={value} value={value}>{value}</option>)}</select>
            ) : field.multiline ? (
              <textarea {...common} rows={5} maxLength={field.maxLength} />
            ) : (
              <input {...common} maxLength={field.maxLength} />
            )}
          </label>
        );
      })}
      {error && <p role="alert" className="text-ui-1 text-ui-danger">{error}</p>}
      <button type="submit" disabled={busy} className="min-h-9 w-full rounded-ui-sm bg-ui-primary px-4 text-ui-1 font-bold text-ui-primary-fg disabled:opacity-50">
        {busy ? "正在保存…" : "创建真实业务对象"}
      </button>
    </form>
  );
}

function MultiSurfaceMain({ detail, surface, viewRef, selectedId, onSelectObject, onSelectView }) {
  if (
    !surface?.eligible
    || !Array.isArray(surface?.viewRefs)
    || !Array.isArray(surface?.projectionRefs)
  ) return (
    <div className="rounded-ui-sm border border-ui-danger/30 bg-ui-surface p-6">
      <p className="text-ui-3 font-semibold text-ui-txt">{surface?.purpose || "Workspace 尚未 Operational"}</p>
      <p className="mt-2 text-ui-2 text-ui-danger">{surface?.status || "WORKSPACE_GAP"}</p>
      {surface?.gaps?.map((gap, index) => <p key={`${gap.status}-${index}`} className="mt-1 text-ui-1 text-ui-txt-3">{gap.status} · {gap.requirementRef || gap.condition || "Core resolution required"}</p>)}
    </div>
  );
  const views = new Map(detail.surfaceModel.objectViews.map((item) => [item.key, item]));
  const view = views.get(viewRef) || views.get(surface.primaryViewRef);
  const projectionRef = surface.projectionRefs.find((ref) => {
    const profile = detail.surfaceModel.projectionProfiles.find((item) => item.key === ref);
    return (
      (view?.component === "workspace-work-list" && profile?.type === "CORE_WORK")
      || (view?.component === "workspace-result-list" && profile?.type === "CORE_RESULT")
      || (view?.component === "workspace-evidence-list" && profile?.type === "CORE_EVIDENCE")
    );
  });
  return (
    <div className="min-h-full bg-ui-bg p-5">
      <p className="text-ui-1 font-bold uppercase tracking-wide text-ui-primary">Professional Surface · {surface.key}</p>
      <h1 className="mt-1 text-ui-6 font-semibold text-ui-txt">{surface.purpose}</h1>
      <div className="my-4 flex flex-wrap gap-2" role="tablist" aria-label="Object Views">
        {surface.viewRefs.map((ref) => (
          <button key={ref} type="button" role="tab" aria-selected={view?.key === ref} onClick={() => onSelectView(ref)} className={`rounded-ui-sm px-3 py-2 text-ui-1 font-semibold ${view?.key === ref ? "bg-ui-primary text-ui-primary-fg" : "border border-ui-line bg-ui-surface text-ui-txt-2"}`}>
            {views.get(ref)?.title || ref}
          </button>
        ))}
      </div>
      {view?.component === "object-list" && (
        <div className="divide-y divide-ui-line rounded-ui-sm border border-ui-line bg-ui-surface">
          {detail.objects?.length ? detail.objects.map((object) => (
            <button key={object.object_id} type="button" onClick={() => onSelectObject(object.object_id)} className={`block w-full p-4 text-left ${selectedId === object.object_id ? "bg-ui-surface-2" : "hover:bg-ui-surface-2"}`}>
              <span className="block text-ui-3 font-semibold text-ui-txt">{object.data?.title || object.object_id}</span>
              <span className="mt-1 block text-ui-1 text-ui-txt-3">{object.lifecycle_status} · {object.created_at}</span>
            </button>
          )) : <p className="p-6 text-center text-ui-2 text-ui-txt-3">No Package Domain Objects yet.</p>}
        </div>
      )}
      {view?.component === "workspace-work-list" && <ProjectionList items={detail.shared.projections[projectionRef]} empty="No shared Work in this Workspace." />}
      {view?.component === "workspace-result-list" && <ProjectionList items={detail.shared.projections[projectionRef]} empty="No shared Result in this Workspace." />}
      {view?.component === "workspace-evidence-list" && <ProjectionList items={detail.shared.projections[projectionRef]} empty="No shared Evidence in this Workspace." />}
      <p className="mt-4 text-ui-1 text-ui-txt-3">workspace_id: {detail.instance.workspace_id} · {detail.package.version} · {detail.surfaceModel.operationalStatus}</p>
    </div>
  );
}

export default function InstalledWorkspaceRuntime({ workspaceId }) {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [state, setState] = useState({ status: "loading", detail: null, error: "" });
  const [selectedId, setSelectedId] = useState("");
  const [selectedSurfaceKey, setSelectedSurfaceKey] = useState("");
  const [selectedViewRef, setSelectedViewRef] = useState("");
  const [utilityRequestKey, setUtilityRequestKey] = useState(0);
  const [submit, setSubmit] = useState({ busy: false, error: "" });

  const load = useCallback(async () => {
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const detail = await getInstalledWorkspace(workspaceId);
      setState({ status: "ready", detail, error: "" });
      setSelectedId((current) => current || detail.objects?.[0]?.object_id || "");
    } catch (error) {
      setState({ status: error?.status === 404 ? "missing" : "error", detail: null, error: error.message || "Workspace Package 暂时无法读取" });
    }
  }, [workspaceId]);

  useEffect(() => { load(); }, [load]);

  const detail = state.detail;
  const isV2 = detail?.package?.schema_version === "curis.workspace-package/v2";
  const surfaceModel = detail?.surfaceModel;
  const selectedSurface = surfaceModel?.surfaces?.find((item) => item.key === selectedSurfaceKey) || null;
  const utilityView = isV2 && selectedSurface?.utilityViewRef
    ? surfaceModel.objectViews.find((item) => item.key === selectedSurface.utilityViewRef)
    : null;
  const detailView = isV2 && selectedSurface?.detailViewRef
    ? surfaceModel.objectViews.find((item) => item.key === selectedSurface.detailViewRef)
    : null;
  const objectType = utilityView?.objectType || detail?.surfaces?.utility?.objectType || "";
  const schema = detail?.schemas?.[objectType];
  const selected = detail?.objects?.find((object) => object.object_id === selectedId) || null;

  useEffect(() => {
    if (!surfaceModel || selectedSurfaceKey) return;
    const explicit = searchParams.get("surface");
    let last = "";
    try { last = window.localStorage.getItem(surfacePreferenceKey(workspaceId)) || ""; } catch {}
    const byKey = new Map(surfaceModel.surfaces.map((item) => [item.key, item]));
    const resolved = (
      (byKey.has(explicit) && explicit)
      || (byKey.get(last)?.eligible && last)
      || (byKey.get(surfaceModel.defaultSurfaceRef)?.eligible && surfaceModel.defaultSurfaceRef)
      || surfaceModel.surfaces.find((item) => item.availability.mode === "REQUIRED" && item.eligible)?.key
      || surfaceModel.workspaceGap.key
    );
    setSelectedSurfaceKey(resolved);
  }, [searchParams, selectedSurfaceKey, surfaceModel, workspaceId]);

  useEffect(() => {
    if (!selectedSurface) return;
    if (!selectedSurface.viewRefs.includes(selectedViewRef)) setSelectedViewRef(selectedSurface.primaryViewRef);
  }, [selectedSurface, selectedViewRef]);

  const selectSurface = (key) => {
    const exists = surfaceModel?.surfaces?.some((item) => item.key === key);
    if (!exists) return;
    setSelectedSurfaceKey(key);
    try { window.localStorage.setItem(surfacePreferenceKey(workspaceId), key); } catch {}
    const params = new URLSearchParams(searchParams.toString());
    params.set("surface", key);
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const createObject = async (values) => {
    setSubmit({ busy: true, error: "" });
    try {
      const object = await createInstalledWorkspaceObject(
        workspaceId,
        utilityView?.action || detail.surfaces.utility.action,
        { ceo_id: CEO_ID, object_type: objectType, data: values },
      );
      setSelectedId(object.object_id);
      await load();
      setSelectedId(object.object_id);
      setSubmit({ busy: false, error: "" });
    } catch (error) {
      setSubmit({ busy: false, error: error.message || "保存失败" });
    }
  };

  if (state.status === "loading") return <div className="grid min-h-screen place-items-center bg-ui-bg text-ui-2 text-ui-txt-3">正在恢复 Workspace Package…</div>;
  if (!detail) return <div className="grid min-h-screen place-items-center bg-ui-bg p-8 text-center text-ui-2 text-ui-txt-2"><div><p>{state.error}</p><a href="/ceo-office/workspace" className="mt-4 inline-block font-bold text-ui-primary">返回 Workspace Portal</a></div></div>;
  if (isMusicPackage(detail)) return <MusicWorkspace key={`${detail.instance.company_id}:${workspaceId}:${detail.instance.instance_id}`} detail={detail} workspaceId={workspaceId} />;
  if (isContentGrowthPackage(detail)) return <ContentGrowthWorkspace key={`${detail.instance.company_id}:${workspaceId}:${detail.instance.instance_id}`} detail={detail} workspaceId={workspaceId} />;
  if (isWritingPackage(detail)) return <WritingWorkspace key={`${detail.instance.company_id}:${workspaceId}:${detail.instance.instance_id}`} detail={detail} workspaceId={workspaceId} />;
  if (isV2) {
    const selectedSchema = detail.schemas?.[detailView?.objectType || utilityView?.objectType];
    const context = (
      <DomainContext
        model={surfaceModel}
        selectedKey={selectedSurfaceKey}
        selectedSurface={selectedSurface}
        selectedObject={selected}
        schema={selectedSchema}
        onSelect={selectSurface}
      />
    );
    const utility = utilityView?.component === "object-create-form" ? (
      <CreateForm schema={schema} title={utilityView.title} busy={submit.busy} error={submit.error} onSubmit={createObject} />
    ) : null;
    return (
      <WorkspacePaneShell
        workspaceId={workspaceId}
        breadcrumb={`工作空间 / ${detail.workspace.name} / ${selectedSurface?.key || "gap"}`}
        contextAvailable
        utilityAvailable={Boolean(utility)}
        contextLabel="Domain Navigation"
        utilityLabel={utilityView?.title || "Utility"}
        contextPane={context}
        utilityPane={utility}
        utilityRequestKey={utilityRequestKey}
      >
        <MultiSurfaceMain
          detail={detail}
          surface={selectedSurface || surfaceModel.workspaceGap}
          viewRef={selectedViewRef}
          selectedId={selectedId}
          onSelectObject={setSelectedId}
          onSelectView={setSelectedViewRef}
        />
      </WorkspacePaneShell>
    );
  }
  if (
    detail.surfaces?.main?.component !== "object-list"
    || detail.surfaces?.context?.component !== "object-detail"
    || detail.surfaces?.utility?.component !== "object-create-form"
  ) return <div className="p-8 text-ui-danger">Core 不支持这个声明式 Surface。</div>;

  const main = (
    <div className="min-h-full bg-ui-bg p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-ui-1 font-bold uppercase tracking-wide text-ui-primary">Declarative Workspace Package</p>
          <h1 className="mt-1 font-ui-sans text-ui-6 font-semibold text-ui-txt">{detail.surfaces.main.title}</h1>
          <p className="mt-2 text-ui-2 text-ui-txt-3">{detail.package.package_id} · {detail.package.version} · {detail.package.digest.slice(0, 12)}</p>
        </div>
        <button type="button" onClick={() => setUtilityRequestKey((value) => value + 1)} className="min-h-9 rounded-ui-sm bg-ui-primary px-4 text-ui-1 font-bold text-ui-primary-fg">新增记录</button>
      </div>
      <div className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface">
        {detail.objects?.length ? detail.objects.map((object) => (
          <button key={object.object_id} type="button" onClick={() => setSelectedId(object.object_id)} className={`block w-full border-b border-ui-line p-4 text-left last:border-b-0 ${selectedId === object.object_id ? "bg-ui-surface-2" : "hover:bg-ui-surface-2"}`}>
            <span className="block text-ui-3 font-semibold text-ui-txt">{object.data?.title || object.object_id}</span>
            <span className="mt-1 block text-ui-1 text-ui-txt-3">{object.lifecycle_status} · {object.data?.channel || "来源未记录"} · {object.created_at}</span>
          </button>
        )) : <p className="p-6 text-center text-ui-2 text-ui-txt-3">还没有业务对象。点击“新增记录”创建第一条真实记录。</p>}
      </div>
      <p className="mt-4 text-ui-1 text-ui-txt-3">Activity {detail.activities?.length || 0} 条 · Capability requested 0 / granted 0</p>
    </div>
  );

  return (
    <WorkspacePaneShell
      workspaceId={workspaceId}
      breadcrumb={`工作空间 / ${detail.workspace.name}`}
      contextAvailable
      utilityAvailable
      contextLabel={detail.surfaces.context.title}
      utilityLabel={detail.surfaces.utility.title}
      contextPane={<ObjectDetail object={selected} schema={schema} />}
      utilityPane={<CreateForm schema={schema} title={detail.surfaces.utility.title} busy={submit.busy} error={submit.error} onSubmit={createObject} />}
      utilityRequestKey={utilityRequestKey}
    >
      {main}
    </WorkspacePaneShell>
  );
}
