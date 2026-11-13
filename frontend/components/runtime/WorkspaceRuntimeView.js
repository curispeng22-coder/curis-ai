"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import { getRuntimeWorkspace, getWorkspaceParentPath, runtimeErrorMessage } from "../../lib/runtimeApi.js";
import TerraShell from "../terra/TerraShell.js";
import { TerraCard, TerraPageHead, TerraTag } from "../terra/TerraPrimitives.js";
import { useRuntime } from "./RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "./RuntimeStates.js";


/**
 * Compatibility entry for the not-yet-accepted TTK professional instance.
 * RD and XHS own their domain components and must not return to this adapter.
 */
export default function WorkspaceRuntimeView({ businessType }) {
  const runtime = useRuntime();
  const workspaceId = useSearchParams().get("workspace_id") || "";
  const [view, setView] = useState({ status: "idle", detail: null, parent: null, error: "" });

  useEffect(() => {
    let active = true;
    if (runtime.status !== "ready" || !runtime.companyId || !workspaceId) return () => { active = false; };
    setView({ status: "loading", detail: null, parent: null, error: "" });
    Promise.all([getRuntimeWorkspace(runtime.companyId, workspaceId), getWorkspaceParentPath(workspaceId)])
      .then(([detail, parent]) => active && setView({ status: "ready", detail, parent, error: "" }))
      .catch((error) => active && setView({ status: error?.status === 403 || error?.status === 404 ? "forbidden" : "error", detail: null, parent: null, error: runtimeErrorMessage(error) }));
    return () => { active = false; };
  }, [runtime.companyId, runtime.status, workspaceId]);

  const context = { page: "workspace", company_id: runtime.companyId, workspace_id: workspaceId, business_type: businessType };
  let body;
  if (!workspaceId) {
    body = <RuntimeEmpty title="没有选择工作空间" description="请从 canonical 工作空间目录进入。" action={<Link href="/ceo-office/workspace" className="font-bold text-ui-primary">返回工作空间目录</Link>} />;
  } else if (["idle", "loading"].includes(runtime.status) || ["idle", "loading"].includes(view.status)) {
    body = <RuntimeLoading label="正在读取工作空间…" />;
  } else if (["error", "forbidden"].includes(runtime.status)) {
    body = <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  } else if (["error", "forbidden"].includes(view.status)) {
    body = <RuntimeError message={view.error} forbidden={view.status === "forbidden"} />;
  } else if (view.parent?.status !== "RESOLVED") {
    body = <RuntimeEmpty title="工作空间归属尚未确认" description={view.parent?.reason || "Parent Resolver 尚未返回 canonical 归属。"} action={<Link href="/ceo-office/workspace" className="font-bold text-ui-primary">返回工作空间目录</Link>} />;
  } else {
    const workspace = view.detail?.workspace;
    const path = view.parent.parentPath;
    body = <>
      <TerraPageHead title={workspace?.name || "抖音 / TikTok 工作空间"} subtitle={`${path.department.name} / ${path.business.name}`} facts={[{ value: workspace?.status || "未知", label: "当前状态" }, { value: workspace?.blueprint_version || "未记录", label: "蓝图版本" }]} actions={<Link href="/ceo-office/workspace" className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-bold text-ui-txt-2 no-underline">返回目录</Link>} />
      <TerraCard>
        <div className="flex items-start justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">专业工作面迁移状态</p><h2 className="mt-1 text-ui-5 font-semibold text-ui-txt">抖音 / TikTok 专业工作面尚未验收</h2></div><TerraTag color="amber">等待 Domain 实现</TerraTag></div>
        <p className="mt-3 text-ui-2 text-ui-txt-2">canonical Workspace identity 与归属已经确认；当前不会用旧的 RD/XHS 通用运行卡片冒充短视频专业工作面，也不会生成发布或分析结果。</p>
      </TerraCard>
    </>;
  }

  return <TerraShell topCrumb="工作空间 · 抖音 / TikTok" assistantContext={context}>{body}</TerraShell>;
}
