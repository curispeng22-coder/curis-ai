"use client";

import { useEffect, useState } from "react";
import TerraShell from "../../../components/terra/TerraShell.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import { getCompanyAttention } from "../../../lib/v1FrontendApi.js";
import { workspaceEntryHref } from "../../../lib/runtimeApi.js";
import { d1Href } from "../../../lib/d1State.mjs";

export default function DecisionRoomPage() {
  const runtime = useRuntime();
  const [state, setState] = useState({ companyId: "", status: "loading", items: [] });
  const [reload, setReload] = useState(0);
  useEffect(() => {
    let active = true;
    if (runtime.status !== "ready" || !runtime.companyId) return () => { active = false; };
    setState({ companyId: runtime.companyId, status: "loading", items: [] });
    getCompanyAttention(runtime.companyId).then((value) => {
      if (value?.company?.company_id !== runtime.companyId) throw new Error("公司来源不一致");
      if (active) setState({ companyId: runtime.companyId, status: "ready", items: (value.items || []).filter((item) => item.source_type === "DECISION_PACKET" && item.status === "WAITING_CEO") });
    }).catch(() => { if (active) setState({ companyId: runtime.companyId, status: "error", items: [] }); });
    return () => { active = false; };
  }, [runtime.status, runtime.companyId, reload]);
  let content;
  if (["idle", "loading"].includes(runtime.status)) content = <RuntimeLoading label="正在确认当前公司…" />;
  else if (["error", "forbidden"].includes(runtime.status)) content = <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  else if (!runtime.companyId) content = <RuntimeEmpty title="先建立公司" description="决定属于当前公司的经营工作。" />;
  else if (state.companyId !== runtime.companyId || state.status === "loading") content = <RuntimeLoading label="正在读取待决策事项…" />;
  else if (state.status === "error") content = <RuntimeError message="待决策事项暂不可读取，请重试。" onRetry={() => setReload((value) => value + 1)} />;
  else content = <main className="mx-auto max-w-[1100px] text-ui-txt"><header className="border-b border-ui-line pb-5"><h1 className="text-2xl font-semibold">待决策事项</h1><p className="mt-2 text-sm text-ui-txt-2">查看当前公司等待你判断的决定，回到原工作处理。</p></header><div className="divide-y divide-ui-line">{state.items.length ? state.items.map((item) => <article key={item.source_ref} className="py-5"><h2 className="text-base font-semibold">{item.summary}</h2><p className="mt-2 text-sm text-ui-txt-2">等待你决定 · {item.updated_at || "时间未记录"}</p><div className="mt-3 flex flex-wrap gap-4 text-sm text-ui-primary"><a href={d1Href({ view: "matter", sourceRef: item.source_ref, sourceType: item.source_type, workspaceId: item.workspace_id })}>查看事项来源 →</a>{item.workspace_id ? <a href={workspaceEntryHref(item.workspace_id)}>回原工作处理 →</a> : <span className="text-ui-txt-2">原工作入口尚未提供</span>}</div></article>) : <p className="py-10 text-sm text-ui-txt-2">当前公司没有已返回的待决策事项。</p>}</div></main>;
  return <TerraShell topCrumb="待决策事项" assistantContext={{ page: "decisions", company_id: runtime.companyId }}>{content}</TerraShell>;
}
