"use client";

import { useEffect, useRef, useState } from "react";
import { TENANT_ID } from "../../lib/api.js";
import { getResultDetail, markResultViewed, getOriginalAgentFile } from "../../lib/v1FrontendApi.js";
import { workspaceEntryHref } from "../../lib/runtimeApi.js";
import { validateBusinessReturn } from "../../lib/businessReturnApi.js";
import { d1Href, readableResult } from "../../lib/d1State.mjs";
import { SharedResultUtility } from "../workspace/SharedEmployeeWorkArea.js";

// An explicit click selects with explicit=true. Refresh/deep-link restoration
// reads with explicit=false; list exposure and prefetch never create receipts.
export function resultSelection(workspaceId, referenceId, explicit = true) {
  return { workspaceId, referenceId, explicit };
}

export function restoreResultSelection() {
  const params = new URLSearchParams(window.location.search);
  return params.get("result_ref") && params.get("result_workspace")
    ? resultSelection(params.get("result_workspace"), params.get("result_ref"), false) : null;
}

export function rememberResultSelection(selection) {
  const url = new URL(window.location.href);
  for (const key of ["result_ref", "result_workspace"]) url.searchParams.delete(key);
  if (selection) {
    url.searchParams.set("result_ref", selection.referenceId);
    url.searchParams.set("result_workspace", selection.workspaceId);
  }
  window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
}

// General headings use only a public Work projection and an exact result binding.
// This context is in-memory presentation data, never a URL or a stored title.
export function generalResultTitleContext(companyId, workspaceId, data, selection) {
  const context = { companyId, workspaceId, referenceId: selection?.referenceId || "", source: null };
  if (!selection || selection.workspaceId !== workspaceId || data?.company?.company_id !== companyId
    || data?.workspace?.workspace_id !== workspaceId) return context;
  const matches = (data.current_work || []).flatMap((work) => (work.result_summaries || [])
    .filter((item) => item.reference_id === selection.referenceId).map((summary) => ({ work, summary })));
  if (matches.length !== 1) return context;
  const { work, summary } = matches[0];
  const typed = summary.kind === "ARTIFACT" ? (work.artifact_refs || []).includes(summary.reference_id)
    && summary.task_ref && (work.result_refs || []).includes(`task:${summary.task_ref}`)
    : summary.kind === "RESULT" && (work.result_refs || []).includes(summary.reference_id)
      && summary.source_work_ref === work.work_ref;
  if (!typed || !work.work_ref || typeof work.problem !== "string" || !work.problem.trim()) return context;
  return { ...context, source: { workRef: work.work_ref, kind: summary.kind,
    taskRef: summary.task_ref || "", goal: work.problem.trim().replace(/\s+/g, " ").slice(0, 120) } };
}

export function generalResultDisplayTitle(result, context, companyId, selection) {
  const label = { RESULT: "工作结果", ARTIFACT: "工作成果", EVIDENCE: "证据", OUTCOME: "业务结果" }[result?.kind] || "工作记录";
  const source = context?.source;
  if (!source || context.companyId !== companyId || context.workspaceId !== selection?.workspaceId
    || context.referenceId !== selection?.referenceId || result?.tenant_id !== TENANT_ID
    || result.company_id !== companyId || result.workspace_id !== selection.workspaceId
    || result.reference_id !== selection.referenceId || result.kind !== source.kind) return label;
  const bound = result.kind === "RESULT" ? result.source_work_ref === source.workRef
    : result.kind === "ARTIFACT" && result.task_ref === source.taskRef;
  return bound ? `${label} · ${source.goal}` : label;
}

export default function ResultReferenceView({ companyId, selection, onViewed, onClose, conversationReturn, businessReturn = null, generalTitleContext }) {
  const panel = useRef(null);
  const [state, setState] = useState({ result: null, error: "", loading: true, key: "" });
  const [retry, setRetry] = useState(0);
  const [receiptError, setReceiptError] = useState("");
  const [receiptRetry, setReceiptRetry] = useState(0);
  const workspaceId = selection.workspaceId;
  const referenceId = selection.referenceId;
  const key = JSON.stringify([companyId, workspaceId, referenceId]);
  const returnKind = typeof businessReturn?.kind === "string" ? businessReturn.kind : "";
  const returnHref = typeof businessReturn?.href === "string" ? businessReturn.href : "";
  const returnKey = JSON.stringify([key, returnKind, returnHref]);
  const [verifiedReturn, setVerifiedReturn] = useState(null);
  const resultScopeReady = !state.loading && !state.error && state.key === key
    && state.result?.tenant_id === TENANT_ID && state.result?.company_id === companyId
    && state.result?.workspace_id === workspaceId && state.result?.reference_id === referenceId;
  useEffect(() => {
    let active = true;
    setVerifiedReturn(null);
    if (!resultScopeReady || !["writing", "cg", "music"].includes(returnKind) || !returnHref) return () => { active = false; };
    Promise.resolve().then(() => active ? validateBusinessReturn(returnKind, returnHref, { employeeCompany: companyId }) : null)
      .then((target) => {
        if (active && target?.company === companyId && target.workspace === workspaceId && typeof target.href === "string")
          setVerifiedReturn({ key: returnKey, href: target.href });
      }).catch(() => { /* Preserve the existing workspace fallback; never navigate to an unchecked source. */ });
    return () => { active = false; };
  }, [companyId, workspaceId, returnKey, returnKind, returnHref, resultScopeReady]);

  const downloadContext = useRef(key);
  downloadContext.current = key;
  const [downloadError, setDownloadError] = useState("");
  const [downloading, setDownloading] = useState("");
  const previewScope = JSON.stringify([key, state.result?.result_version || ""]);
  const currentPreviewScope = useRef(previewScope);
  currentPreviewScope.current = previewScope;
  const previewUrl = useRef(null);
  const previewGeneration = useRef(0);
  const [preview, setPreview] = useState(null);
  useEffect(() => {
    previewGeneration.current += 1;
    if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
    previewUrl.current = null;
    setPreview(null);
    return () => {
      previewGeneration.current += 1;
      if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
      previewUrl.current = null;
    };
  }, [key, state.result?.result_version]);
  async function previewCapture(artifact) {
    const original = state.result, generation = ++previewGeneration.current, scope = previewScope;
    let workRef = original?.source_work_ref;
    if (original?.kind === "ARTIFACT") {
      try {
        const locator = JSON.parse(original.content);
        if (locator.tenant_id !== original.tenant_id || locator.company_id !== companyId
            || locator.task_id !== original.task_ref || !locator.work_ref) return;
        workRef = locator.work_ref;
      } catch { return; }
    }
    if (!workRef || !original.result_version || state.key !== key || original.tenant_id !== TENANT_ID
        || original.company_id !== companyId || original.workspace_id !== workspaceId
        || original.reference_id !== referenceId) return;
    if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
    previewUrl.current = null;
    setPreview(null);
    setDownloadError("");
    try {
      const value = await getOriginalAgentFile(workRef, artifact.artifact_id);
      if (previewGeneration.current !== generation || currentPreviewScope.current !== scope) return;
      const capture = value.browser_capture;
      if (value.tenant_id !== original.tenant_id || value.company_id !== companyId
          || value.workspace_id !== workspaceId || value.work_ref !== workRef
          || value.artifact_ref !== artifact.artifact_id || value.artifact_content_sha256 !== artifact.content_sha256
          || (original.kind === "ARTIFACT"
              ? original.reference_id !== value.artifact_ref || original.task_ref !== value.task_id
              : original.reference_id !== "task:" + value.task_id)
          || value.mime_type !== "image/png"
          || !capture || capture.tenant_id !== value.tenant_id || capture.company_id !== companyId
          || capture.work_ref !== value.work_ref || capture.task_id !== value.task_id
          || capture.sha256 !== value.sha256 || capture.bytes !== value.bytes
          || capture.mime_type !== "image/png" || !capture.session_id || !capture.tab_id
          || typeof capture.url !== "string" || !capture.url.startsWith("https://")
          || value.bytes <= 0 || value.bytes > 8 * 1024 * 1024) throw new Error("截图来源与原结果不一致。");
      const bytes = Uint8Array.from(atob(value.content_base64), (char) => char.charCodeAt(0));
      const signature = [137, 80, 78, 71, 13, 10, 26, 10];
      if (bytes.length !== value.bytes || !signature.every((v, i) => bytes[i] === v)) throw new Error("截图格式不合法。");
      const sha = [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))].map((n) => n.toString(16).padStart(2, "0")).join("");
      if (previewGeneration.current !== generation || currentPreviewScope.current !== scope) return;
      if (sha !== value.sha256) throw new Error("截图内容与原文件回执不一致。");
      const blob = new Blob([bytes], { type: "image/png" });
      const decoded = await createImageBitmap(blob);
      try {
        if (!decoded.width || !decoded.height || decoded.width > 4096 || decoded.height > 4096
            || decoded.width * decoded.height > 16000000) throw new Error("截图尺寸不符合范围。");
      } finally { decoded.close(); }
      if (previewGeneration.current !== generation || currentPreviewScope.current !== scope) return;
      const url = URL.createObjectURL(blob);
      if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
      previewUrl.current = url;
      setPreview({ url, source: capture.url, generation, scope });
    } catch (error) {
      if (previewGeneration.current === generation && currentPreviewScope.current === scope) setDownloadError(error.message || "无法核验截图。");
    }
  }
  async function download(artifact) {
    const original = state.result, captured = key;
    if (!original?.source_work_ref || downloading) return;
    setDownloading(artifact.artifact_id); setDownloadError("");
    try {
      const value = await getOriginalAgentFile(original.source_work_ref, artifact.artifact_id);
      if (downloadContext.current !== captured) return;
      if (value.tenant_id !== original.tenant_id || value.company_id !== companyId
        || value.work_ref !== original.source_work_ref || value.artifact_ref !== artifact.artifact_id) throw new Error("成果范围不一致。");
      const bytes = Uint8Array.from(atob(value.content_base64), (char) => char.charCodeAt(0));
      const sha = [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))].map((n) => n.toString(16).padStart(2, "0")).join("");
      if (bytes.length !== value.bytes || sha !== value.sha256) throw new Error("下载内容与原文件回执不一致。");
      if (downloadContext.current !== captured) return;
      const url = URL.createObjectURL(new Blob([bytes], { type: "application/octet-stream" }));
      const link = document.createElement("a"); link.href = url; link.download = value.filename;
      link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (error) { if (downloadContext.current === captured) setDownloadError(error.message || "无法核验原成果文件。"); }
    finally { setDownloading(""); }
  }
  useEffect(() => {
    let active = true;
    setState({ result: null, error: "", loading: true, key }); setReceiptError("");
    getResultDetail(companyId, workspaceId, referenceId).then((result) => {
      if (active) setState({ result, error: "", loading: false, key });
    }).catch(() => { if (active) setState({ result: null, error: "无法读取这份结果，请重新读取或返回原工作。", loading: false, key }); });
    return () => { active = false; };
  }, [companyId, workspaceId, referenceId, retry, key]);

  useEffect(() => {
    const result = state.result;
    if (state.key !== key || !selection.explicit || !result?.result_version || result.viewed) return;
    panel.current?.scrollIntoView({ block: "center" });
    // This effect runs only after the fetched detail has rendered, never in GET.
    let active = true;
    markResultViewed(companyId, workspaceId, result).then(() => {
      if (active) { setReceiptError(""); onViewed?.(); }
    }).catch(() => { if (active) setReceiptError("结果已打开，但查看记录尚未保存；不会影响结果或业务验收。"); });
    return () => { active = false; };
  }, [companyId, workspaceId, state.result, state.key, key, selection.explicit, receiptRetry, onViewed]);

  const previewArtifacts = state.result?.kind === "ARTIFACT" && state.result.artifact_type === "agent_file_receipt"
    ? [{ artifact_id: state.result.reference_id, title: state.result.title, content_sha256: state.result.content_sha256, artifact_type: "agent_file_receipt" }]
    : state.result?.artifacts?.filter((item) => item.artifact_type === "agent_file_receipt") || [];
  const fallbackReturnUrl = `${workspaceEntryHref(workspaceId)}&result_workspace=${encodeURIComponent(workspaceId)}&result_ref=${encodeURIComponent(referenceId)}${conversationReturn?.startsWith('/ceo-office/conversation?conversation_id=') ? `&return_to=${encodeURIComponent(conversationReturn)}` : ""}`;
  const returnUrl = resultScopeReady && verifiedReturn?.key === returnKey ? verifiedReturn.href : fallbackReturnUrl;
  return <section ref={panel} className="rounded-ui-md border border-ui-line bg-ui-surface p-4" aria-label="已打开的结果">
    {state.key === key && previewArtifacts.map((item) =>
      <span key={item.artifact_id}>{state.result?.source_work_ref && <button type="button" disabled={Boolean(downloading)} onClick={() => download(item)}>下载原成果：{item.title}</button>}
        <button type="button" onClick={() => previewCapture(item)}>核验并预览截图</button></span>)}
    {preview?.scope === previewScope && <figure><img src={preview.url} alt="原工作截图" /><figcaption>来源：{preview.source}；内容尚未验证。</figcaption></figure>}
    {downloadError && <p role="alert">{downloadError}</p>}
    <div className="mb-3 flex gap-4 text-ui-1"><a href={returnUrl} className="text-ui-primary">返回原工作空间</a><button type="button" onClick={onClose} className="ml-auto text-ui-txt-2">关闭结果</button></div>
    {state.loading || state.key !== key ? <div role="status" className="space-y-2"><p className="text-ui-2 text-ui-txt-2">正在读取结果…</p><div className="h-16 animate-pulse rounded-ui-md bg-ui-surface-2" /><div className="h-24 animate-pulse rounded-ui-md bg-ui-surface-2" /></div> : state.error ? <div role="alert" className="rounded-ui-md border border-ui-line bg-ui-surface-2 p-4"><p className="text-ui-2 text-ui-txt-2">{state.error}</p><button type="button" onClick={() => setRetry((value) => value + 1)} className="mt-3 rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-1 font-semibold text-ui-txt-2">重新读取</button></div> : <SharedResultUtility result={state.result} displayTitle={generalTitleContext ? generalResultDisplayTitle(state.result, generalTitleContext, companyId, selection) : undefined} />}
    {!state.loading && !state.error && state.key === key && state.result?.reference_id === referenceId && state.result?.tenant_id && state.result?.company_id === companyId && state.result?.workspace_id === workspaceId && readableResult(state.result).length > 0 && ["ELIGIBLE", "DECIDED"].includes(state.result?.response_eligibility?.status) && (state.result?.response_eligibility?.status !== "DECIDED" || state.result?.user_response?.result_version === state.result?.result_version && state.result?.user_response?.result_ref === referenceId && state.result?.user_response?.tenant_id === state.result?.tenant_id && state.result?.user_response?.company_id === companyId && state.result?.user_response?.workspace_id === workspaceId && state.result?.user_response?.source_work_ref === state.result?.source_work_ref && state.result?.user_response?.ceo_id === state.result?.response_actor_ref && ["ACCEPT", "REVISE", "REJECT"].includes(state.result?.user_response?.action) && Boolean(state.result?.user_response?.request_id) && Boolean(state.result?.user_response?.reason)) && state.result?.source_work_ref && state.result?.result_version && <a className="mt-3 block text-ui-primary" href={d1Href({ view: "result", resultRef: referenceId, workspaceId, workRef: state.result.source_work_ref, resultVersion: state.result.result_version, resultOrigin: "utility", originCompany: companyId })}>在主页面核对并选择此版本 →</a>}
    {receiptError ? <div role="alert" className="mt-3 rounded-ui-md border border-ui-line bg-ui-surface-2 p-4 text-ui-1"><p className="text-ui-txt-2">{receiptError}</p><button type="button" onClick={() => setReceiptRetry((value) => value + 1)} className="mt-2 rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 font-semibold text-ui-txt-2">重试保存查看记录</button></div> : null}
  </section>;
}
