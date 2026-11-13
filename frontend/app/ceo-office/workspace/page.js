"use client";

import Link from "next/link";
import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import TerraShell from "../../../components/terra/TerraShell.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import { TerraCard, TerraPageHead, TerraTag } from "../../../components/terra/TerraPrimitives.js";
import GeneralWorkspaceOperating from "../../../components/v1/GeneralWorkspaceOperating.js";
import { getCanonicalBusinesses, getRuntimeWorkspace, getWorkspaceParentPath, isLegacyOfficeType, runtimeErrorMessage, workspaceEntryHref, workspaceOfficeHref } from "../../../lib/runtimeApi.js";

const STATUS = { DRAFT: ["草拟中", "grey"], OPERATING: ["经营中", "green"], PAUSED: ["已暂停", "amber"], ARCHIVED: ["已归档", "grey"] };
const statusTag = (value) => STATUS[String(value || "").toUpperCase()] || ["状态未知", "grey"];

function WorkspaceEntry() {
  const runtime = useRuntime(), router = useRouter();
  const searchParams = useSearchParams();
  const workspaceId = searchParams.get("workspace_id") || "";
  const [view, setView] = useState({ status: "idle", businesses: [], detail: null, parent: null, error: "" });

  useEffect(() => {
    let active = true;
    if (runtime.status !== "ready" || !runtime.companyId) return () => { active = false; };
    setView({ status: "loading", businesses: [], detail: null, parent: null, error: "" });
    const request = workspaceId
      ? getRuntimeWorkspace(runtime.companyId, workspaceId).then(async (detail) => ({ businesses: [], detail, parent: await getWorkspaceParentPath(workspaceId) }))
      : getCanonicalBusinesses(runtime.companyId).then((payload) => ({ businesses: payload.businesses || [], detail: null, parent: null }));
    request
      .then((result) => active && setView({ status: "ready", error: "", ...result }))
      .catch((error) => active && setView({ status: error?.status === 403 || error?.status === 404 ? "forbidden" : "error", businesses: [], detail: null, parent: null, error: runtimeErrorMessage(error) }));
    return () => { active = false; };
  }, [runtime.companyId, runtime.status, workspaceId]);

  useEffect(() => {
    if (view.status !== "ready" || !workspaceId) return;
    const workspace = view.detail?.workspace, parent = view.parent?.parentPath;
    if (workspace?.workspace_id === workspaceId && workspace.company_id === runtime.companyId
      && view.parent?.status === "RESOLVED" && parent?.company?.company_id === runtime.companyId
      && parent?.workspace?.workspace_id === workspaceId && parent?.business?.business_id === workspace.business_id
      && workspace.business_type === "PACKAGE") router.replace(workspaceOfficeHref(workspace));
  }, [view, workspaceId, runtime.companyId, router]);

  if (["idle", "loading"].includes(runtime.status) || ["idle", "loading"].includes(view.status)) return <RuntimeLoading label="正在读取工作空间…" />;
  if (["error", "forbidden"].includes(runtime.status)) return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  if (["error", "forbidden"].includes(view.status)) return <RuntimeError message={view.status === "forbidden" ? "当前无法访问这个工作空间，请从业务空间重新选择。" : "暂时无法读取这个工作空间，请稍后重试。"} forbidden={view.status === "forbidden"} />;
  if (!runtime.snapshot?.company) return <RuntimeEmpty title="公司尚未建立" description="先完成公司创办，再进入工作空间。" action={<Link href="/onboarding" className="font-bold text-ui-primary">开始创办公司</Link>} />;

  if (!workspaceId) {
    const rows = view.businesses.flatMap((business) => (business.workspaces || []).map((workspace) => ({ business, workspace })));
    return <>
      <TerraPageHead title="工作空间" subtitle={`${runtime.snapshot.company.name} · 选择业务下的工作空间，继续工作`} facts={[{ value: view.businesses.length, label: "业务" }, { value: rows.length, label: "工作空间" }]} actions={<Link href="/ceo-office/workspace/studio" className="rounded-ui-sm bg-ui-primary px-3 py-2 text-ui-1 font-bold text-ui-primary-fg no-underline">搭建工作空间</Link>} />
      {rows.length ? <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{rows.map(({ business, workspace }) => { const [label, color] = statusTag(workspace.status); return <TerraCard key={workspace.workspace_id} hover><div className="flex items-start justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">{business.name}</p><h2 className="mt-1 text-ui-4 font-semibold text-ui-txt">{workspace.name}</h2></div><TerraTag color={color}>{label}</TerraTag></div><p className="mt-3 text-ui-1 text-ui-txt-3">所属部门：{business.parentPath?.department?.name || "未知"}</p><Link href={workspaceEntryHref(workspace.workspace_id)} className="mt-4 inline-flex text-ui-1 font-bold text-ui-primary no-underline">打开工作空间 →</Link></TerraCard>; })}</div> : <RuntimeEmpty title="还没有工作空间" description="建立业务后，可以在这里打开它的工作空间。" />}
    </>;
  }

  if (view.parent?.status !== "RESOLVED" || !view.detail?.workspace) {
    return <RuntimeEmpty title="工作空间归属尚未确认" description="暂时无法确认这个工作空间所属的业务，请返回目录重新选择。" action={<Link href="/ceo-office/workspace" className="font-bold text-ui-primary">返回工作空间目录</Link>} />;
  }

  const workspace = view.detail.workspace;
  const path = view.parent.parentPath;
  if (String(workspace.business_type || "").toUpperCase() === "GENERIC") {
    return <GeneralWorkspaceOperating
      companyId={runtime.companyId}
      workspaceId={workspace.workspace_id}
      parentPath={path}
      assistant={runtime.snapshot?.assistant}
    />;
  }
  const [label, color] = statusTag(workspace.status);
  const legacyOffice = isLegacyOfficeType(workspace.business_type);
  return <>
    <TerraPageHead title={workspace.name} subtitle={`${path.company.name} / ${path.department.name} / ${path.business.name}`} facts={[{ value: label, label: "当前状态" }]} actions={<Link href="/ceo-office/workspace" className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-bold text-ui-txt-2 no-underline">返回目录</Link>} />
    <TerraCard>
      <div className="flex items-start justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">工作空间入口</p><p className="mt-1 text-ui-2 text-ui-txt-2">继续当前业务的创作与工作</p></div><TerraTag color={color}>{label}</TerraTag></div>
      <p className="mt-3 text-ui-2 text-ui-txt-2">在这里核对所属业务，打开工作台后继续创作。</p>
      {legacyOffice ? (
        <p role="note" className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface-2 px-4 py-3 text-ui-1 leading-relaxed text-ui-txt-3">
          该工作空间属于研发（RD）/ 小红书旧业务 / 抖音电商等已冻结业务类型，不在 CURIS V1（内容增长、写作、音乐）范围内；专业工作面已冻结，历史数据在此只读保留，不再提供进入入口。
        </p>
      ) : (
        <div className="mt-5 flex flex-wrap gap-3"><Link href={workspaceOfficeHref(workspace)} className="rounded-ui-sm bg-ui-primary px-4 py-2 text-ui-1 font-bold text-ui-primary-fg no-underline">打开工作台</Link><Link href={`/ceo-office/business?business_id=${encodeURIComponent(path.business.business_id)}`} className="rounded-ui-sm border border-ui-line px-4 py-2 text-ui-1 font-bold text-ui-txt-2 no-underline">返回所属业务</Link></div>
      )}
    </TerraCard>
  </>;
}

export default function WorkspacePage() {
  return <TerraShell topCrumb="业务空间 · 工作空间" assistantContext={{ page: "workspace" }}><Suspense fallback={<RuntimeLoading label="正在打开工作空间…" />}><WorkspaceEntry /></Suspense></TerraShell>;
}
