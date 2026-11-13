"use client";

import { useEffect, useRef, useState } from "react";
import { d1Error } from "../../../lib/d1Api.js";
import { readableResult, receiptEligible, resultResponseKey, restoreResultResponse, saveResultResponse, clearResultResponse, resultReceiptMatches, validResultBridge } from "../../../lib/d1State.mjs";
import styles from "./D1.module.css";
import { workspaceEntryHref } from "../../../lib/runtimeApi.js";

// Presentation copy only: automatic artifact names may contain internal Task context.
export function resultDisplayCopy(result) {
  return { ...result, title: result.kind === "ARTIFACT" ? "工作成果" : result.title,
    ...(Array.isArray(result.artifacts) ? { artifacts: result.artifacts.map((item) => ({ ...item, title: "关联成果" })) } : {}) };
}

// Read a known complete envelope for presentation only; never rewrite the DTO.
export function resultReadingProjection(result) {
  if (result?.kind === "RESULT" && typeof result.content === "string") {
    try {
      const envelope = JSON.parse(result.content);
      if (envelope && !Array.isArray(envelope) && envelope.resultType === "general-business-result"
        && typeof envelope.summary === "string" && envelope.summary.trim()) {
        return { material: [{ text: envelope.summary }], isSummary: true };
      }
    } catch { /* Incomplete or unknown text retains the existing reader behavior. */ }
  }
  return { material: readableResult(result), isSummary: false };
}

export default function ResultView({ companyId, selection, api, onBack, backLabel = "返回 CEO 工作台", onWork, onViewed }) {
  const [state, setState] = useState({ loading: true, result: null, error: "" });
  const [reload, setReload] = useState(0);
  const [receipt, setReceipt] = useState({ status: "idle", error: "" });
  const receiptAttempt = useRef(null);
  const responseIdentity = useRef("");
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const [choice, setChoice] = useState({ action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice: "" });
  const selectionKey = JSON.stringify([companyId, selection.workspaceId, selection.resultRef]);
  useEffect(() => {
    let active = true;
    setState({ loading: true, result: null, error: "" }); setReceipt({ status: "idle", error: "" });
    Promise.resolve().then(() => api.result(companyId, selection.workspaceId, selection.resultRef)).then((result) => {
      if (result.reference_id !== selection.resultRef || !result.tenant_id || result.company_id !== companyId || result.workspace_id !== selection.workspaceId) throw new Error("结果来源不一致");
      if (active) setState({ loading: false, result, error: "" });
    }).catch((error) => { if (active) setState({ loading: false, result: null, error: error.code === "RESULT_READ_SCOPE_GAP" ? error.message : d1Error(error) }); });
    return () => { active = false; };
  }, [api, companyId, selection.workspaceId, selection.resultRef, reload]);

  const result = state.result;
  const responseActor = result?.response_actor_ref || "";
  const responseContext = [result?.tenant_id, companyId, selection.workspaceId, result?.reference_id, result?.result_version, result?.source_work_ref, responseActor];
  const responseStorage = resultResponseKey(companyId, selection.workspaceId, result, responseActor);
  responseIdentity.current = JSON.stringify(responseContext);
  useEffect(() => {
    if (!result || !responseActor) return;
    let saved = null, raw = null, storageError = false;
    try { raw = sessionStorage.getItem(responseStorage); saved = restoreResultResponse(raw, responseContext); }
    catch { storageError = true; }
    setChoice(saved ? { action: saved.action, reason: saved.reason, confirmed: false, pending: saved.pending || null, busy: false, error: "", notice: "原输入已恢复；请重新确认。" }
      : { action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", storageBlocked: Boolean(raw),
        notice: raw ? "原暂存请求的身份或格式无法核验；已停止新提交，请回原入口核对。" : storageError ? "暂存空间不可用；本次输入仍保留在页面。" : "" });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [responseStorage, responseActor]);
  useEffect(() => {
    if (!result || !responseActor || !choice.action && !choice.reason && !choice.pending) return;
    try { saveResultResponse(sessionStorage, responseStorage, { context: responseContext, at: Date.now(),
      action: choice.action, reason: choice.reason, request_id: choice.pending?.request_id || "", pending: choice.pending }); }
    catch { setChoice((value) => ({ ...value, notice: "暂存空间不可用；请保留当前页面和输入。" })); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [choice.action, choice.reason, choice.pending, responseStorage]);
  const bridge = selection.resultOrigin === "utility";
  const bridgeValid = !selection.resultBridgeInvalid && (!bridge || validResultBridge(selection, companyId, result));
  const utilityReturn = bridgeValid && bridge ? `${workspaceEntryHref(selection.workspaceId)}&result_workspace=${encodeURIComponent(selection.workspaceId)}&result_ref=${encodeURIComponent(selection.resultRef)}` : "";
  const currentResponse = result?.user_response;
  async function submitChoice() {
    if (!result || !bridgeValid || !responseActor || currentResponse || result.response_eligibility?.status !== "ELIGIBLE"
        || choice.storageBlocked || !choice.confirmed || !choice.action || !choice.reason.trim() || new TextEncoder().encode(choice.reason.trim()).length > 2000 || choice.busy) return;
    const pending = choice.pending || { request_id: crypto.randomUUID(), action: choice.action, reason: choice.reason.trim() };
    if (pending.action !== choice.action || pending.reason !== choice.reason.trim()) return;
    const identity = responseIdentity.current;
    const expected = { tenant_id: result.tenant_id, company_id: companyId, workspace_id: selection.workspaceId,
      reference_id: result.reference_id, result_version: result.result_version,
      source_work_ref: result.source_work_ref, response_actor_ref: responseActor };
    const current = () => mounted.current && responseIdentity.current === identity;
    const sameSource = (fresh) => Boolean(fresh && Object.entries(expected).every(([key, value]) => value && fresh[key] === value));
    const finish = (fresh, notice) => {
      if (!current()) return;
      try { clearResultResponse(sessionStorage, responseStorage); } catch { /* A saved receipt remains canonical. */ }
      setState({ loading: false, result: fresh, error: "" });
      setChoice({ action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice });
    };
    setChoice((value) => ({ ...value, pending, busy: true, error: "", notice: "" }));
    try {
      if (choice.pending) {
        const recovered = await api.result(companyId, selection.workspaceId, result.reference_id);
        if (!current()) return;
        if (resultReceiptMatches(recovered, pending, expected)) { finish(recovered, "已核实原请求保存成功。"); return; }
        if (!sameSource(recovered) || recovered.user_response || recovered.response_eligibility?.status !== "ELIGIBLE")
          throw new Error("原请求状态或来源已变化，请保留输入并重新核对。");
      }
      await api.respond(companyId, selection.workspaceId, result, pending.action, pending.reason, pending.request_id);
      if (!current()) return;
      const fresh = await api.result(companyId, selection.workspaceId, result.reference_id);
      if (!resultReceiptMatches(fresh, pending, expected)) throw new Error("写入结果尚未核实，请用原请求重新核对。");
      finish(fresh, "人类选择已保存；未自动继续执行。");
    } catch (cause) {
      if (!current()) return;
      try {
        const fresh = await api.result(companyId, selection.workspaceId, result.reference_id);
        if (resultReceiptMatches(fresh, pending, expected)) { finish(fresh, "已核实原请求保存成功。"); return; }
      } catch { /* Keep the exact pending request for cold read or retry. */ }
      if (!current()) return;
      setChoice((value) => ({ ...value, busy: false, confirmed: false, error: d1Error(cause) + "；原输入和请求已保留，请先核对再重试。" }));
    }
  }
  async function recordViewed() {
    if (!receiptEligible(selection, result)) return;
    const key = `${selectionKey}:${result.result_version}`;
    if (receiptAttempt.current?.key === key && receiptAttempt.current.status !== "error") return;
    const attempt = { key, status: "saving" }; receiptAttempt.current = attempt;
    setReceipt({ status: "saving", error: "" });
    try { await api.viewed(companyId, selection.workspaceId, result); if (!mounted.current) return; attempt.status = "saved"; setReceipt({ status: "saved", error: "" }); onViewed?.(); }
    catch (error) { if (!mounted.current) return; attempt.status = "error"; setReceipt({ status: "error", error: d1Error(error) }); }
  }
  useEffect(() => {
    if (!result || !receiptEligible(selection, result)) return;
    // Opening only: route restoration and list exposure never enter this branch.
    // The server makes retries of this version's receipt idempotent.
    recordViewed();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result, selection.explicit]);

  if (state.loading) return <section className={styles.loading} role="status">正在读取结果与原始版本…</section>;
  if (state.error) return <section className={styles.panel} role="alert"><p>{state.error}</p><button onClick={() => setReload((value) => value + 1)}>重新读取结果</button><button onClick={onBack}>{backLabel}</button></section>;
  if (!bridgeValid) return <section className={styles.panel} role="alert"><p>原 Utility 入口的公司、工作或固定结果版本已变化，请返回原工作空间重新打开。</p><a href={workspaceEntryHref(selection.workspaceId)}>返回原工作空间</a></section>;
  const displayed = resultDisplayCopy(result);
  const { material, isSummary } = resultReadingProjection(displayed);
  const readable = material.length > 0;
  return <div className={styles.resultReading}>
    <header className={styles.pageTitle}><div><p className={styles.crumb}>工作结果</p><h1>{displayed.title || ({ RESULT: "工作结果", EVIDENCE: "证据", OUTCOME: "业务结果" }[result.kind] || "工作记录")}</h1></div><span className={styles.badge}>{isSummary ? "结果摘要" : result.kind === "ARTIFACT" ? "来源产物" : "结果原文"}</span></header>
    <div className={styles.resultStrip}>{!readable ? "当前尚无可读结果 · 未新增查看记录" : receipt.status === "saved" || result.viewed ? "已记录此版本的查看" : selection.explicit ? "结果材料已打开" : "由链接恢复 · 未自动记录查看"}<span>查看不会接受结果或应用决定。</span></div>
    <section className={styles.readingSection}><h2>{isSummary ? "结果摘要" : "结果内容"}</h2>{readable ? <div className={styles.resultBody}>{material.map((part, index) => <div key={index}>{part.title && <h3>{part.title}</h3>}<p>{part.text}</p></div>)}</div> : <div role="status"><p>当前页面尚无可阅读的结果材料。内容可能为空，或其格式暂不支持。</p><p className={styles.limit}>查看记录不会新增。请重新读取，或回原工作核对结果。</p><button onClick={() => setReload((value) => value + 1)}>重新读取结果</button></div>}</section>
    <section className={styles.readingSection}><h2>来源与核验</h2><dl className={styles.meta}><dt>来源工作</dt><dd>{result.source_work_ref ? "已关联原工作" : "未记录"}</dd><dt>结果版本</dt><dd className={styles.identifier}>{result.result_version || "未记录"}</dd><dt>核验</dt><dd>{{ VERIFIED: "已核实", UNVERIFIED: "尚未核实", FAILED: "核验未通过" }[result.verification_status] || "核验情况未记录"}</dd></dl>{(displayed.artifacts || []).map((item) => <p key={item.artifact_id}>{item.title || "关联材料名称未记录"}</p>)}</section>
    <section className={styles.readingSection}><h2>对这份交付作选择</h2>{currentResponse ? <p role="status">已保存：{{ ACCEPT: "认可结果", REVISE: "要求修改", REJECT: "不认可结果" }[currentResponse.action]}。理由：{currentResponse.reason}。这不会自动继续工作。</p> : result.response_eligibility?.status === "ELIGIBLE" && responseActor ? <div className={styles.responseForm}><p>本次只记录 CEO 对原结果版本的选择；要求修改仍需核对后续责任，不会自动派发。</p><div className={styles.actions}>{[["ACCEPT", "认可结果"], ["REVISE", "要求修改"], ["REJECT", "不认可结果"]].map(([value, label]) => <label key={value}><input type="radio" name={`result-choice-${result.reference_id}`} checked={choice.action === value} disabled={Boolean(choice.pending) || choice.busy || choice.storageBlocked} onChange={() => setChoice((old) => ({ ...old, action: value, confirmed: false }))} />{label}</label>)}</div><label>选择理由<textarea value={choice.reason} disabled={Boolean(choice.pending) || choice.busy || choice.storageBlocked} onChange={(event) => setChoice((old) => ({ ...old, reason: event.target.value, confirmed: false }))} /></label><label><input type="checkbox" checked={choice.confirmed} disabled={choice.busy || choice.storageBlocked} onChange={(event) => setChoice((old) => ({ ...old, confirmed: event.target.checked }))} />我已核对来源工作、结果版本、理由及记录效果</label><button disabled={choice.busy || choice.storageBlocked || !choice.confirmed || !choice.action || !choice.reason.trim() || new TextEncoder().encode(choice.reason.trim()).length > 2000} onClick={submitChoice}>保存此版本的人类选择</button>{choice.error && <p role="alert">{choice.error}</p>}{choice.notice && <p role="status">{choice.notice}</p>}</div> : <p className={styles.limit}>{result.response_eligibility?.reason || "此来源尚不能记录选择。"}</p>}</section>
    <section className={styles.readingSection}><h2>继续查看</h2><div className={styles.actions}>{result.source_work_ref && <button className={styles.returnToWork} onClick={() => onWork(result.source_work_ref, selection.workspaceId)}>回原工作核对</button>}{utilityReturn ? <a href={utilityReturn}>返回原结果 Utility</a> : <button onClick={onBack}>{backLabel}</button>}<a href={workspaceEntryHref(selection.workspaceId)}>返回原工作空间</a></div></section>
    <details className={styles.sourceDetails}><summary>查看结果来源详情</summary><dl className={styles.meta}><dt>结果标识</dt><dd>{result.reference_id}</dd><dt>来源工作标识</dt><dd>{result.source_work_ref || "未记录"}</dd><dt>结果版本</dt><dd className={styles.identifier}>{result.result_version || "未记录"}</dd><dt>核验来源状态</dt><dd>{result.verification_status || "未记录"}</dd></dl>{(displayed.artifacts || []).map((item) => <p key={item.artifact_id}>{item.title || "关联材料"} · {item.artifact_id}</p>)}</details>
    {receipt.error && <section className={styles.panel} role="alert"><p>结果正文已打开，查看记录尚未确认。{receipt.error}</p><button onClick={recordViewed}>重试保存查看记录</button></section>}
  </div>;
}
