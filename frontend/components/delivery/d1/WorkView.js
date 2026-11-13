"use client";

import { useRef, useState } from "react";
import { d1Error } from "../../../lib/d1Api.js";
import { lifecycleActions, workControlKey, readWorkControl, saveWorkControl, controlTarget, controlReadbackMatches } from "../../../lib/d1State.mjs";
import { workState } from "./CeoMatterView.js";
import styles from "./D1.module.css";
import { workspaceEntryHref } from "../../../lib/runtimeApi.js";

const labels = { pause: "暂停工作", resume: "恢复原工作", cancel: "停止工作", archive: "归档工作", restore: "恢复查看" };
function requestExpired(value) { return value && (!Number.isFinite(Date.parse(value)) || Date.parse(value) <= Date.now()); }
// A fresh object or unchanged revision is not evidence that an unknown command took effect.
const humanOriginKeys = ["requestId", "kind", "targetRef", "workRef", "cycleRef", "workflowRef", "workflowVersion",
  "assignmentRef", "holderRef", "sourceTaskRef", "sourceExecutionKey", "sourceOutputSha256", "inputFingerprint", "actionVersion"];
function sameHumanOrigin(fresh, pending) {
  const request = pending.request, next = fresh?.human_input;
  return Boolean(fresh?.companyId === pending.companyId && fresh.workspaceId === pending.workspaceId && fresh.work_ref === pending.workRef
    && next && humanOriginKeys.every((key) => next[key] === request[key])
    && (!next.companyId || next.companyId === pending.companyId) && (!next.workspaceId || next.workspaceId === pending.workspaceId));
}
function humanReadbackInvalidated(fresh, pending) {
  const next = fresh?.human_input;
  return sameHumanOrigin(fresh, pending) && next.state === "INVALIDATED" && Number.isInteger(next.revision)
    && next.revision > pending.request.revision && Number.isFinite(Date.parse(next.invalidatedAt))
    && ["CANCELLED", "COMPLETED", "ARCHIVED"].includes(fresh.lifecycle_status);
}
function humanReadbackMatches(fresh, pending) {
  const request = pending.request, next = fresh?.human_input;
  if (!sameHumanOrigin(fresh, pending) || !Number.isInteger(next.revision) || next.report?.submissionId !== pending.submissionId) return false;
  const local = request.kind === "LOCAL_INFORMATION";
  const steps = pending.command === "report"
    ? (local ? { LOCAL_REPORTED: 1, READY: 2, CLAIMED: 3, CLOSED: 4 } : { EXTERNAL_REPORTED_UNKNOWN: 1 })
    : pending.command === "review" ? { READY: 1, CLAIMED: 2, CLOSED: 3 } : { CLAIMED: 1, CLOSED: 2 };
  if (!steps[next.state] || next.revision !== request.revision + steps[next.state]) return false;
  const report = pending.report;
  if (["text", "source", "actor", "at"].some((key) => report[key] !== undefined && next.report[key] !== report[key])
    || JSON.stringify(next.report.referenceRefs || []) !== JSON.stringify(report.referenceRefs || [])) return false;
  if (["READY", "CLAIMED", "CLOSED"].includes(next.state) && (!local || !Number.isFinite(Date.parse(next.reviewedAt)))) return false;
  if (["CLAIMED", "CLOSED"].includes(next.state)) {
    const prefix = `responsibility:${pending.workRef}:${request.assignmentRef}:`;
    if (!request.assignmentRef || !next.continuationKey?.startsWith(prefix)
      || !/^[1-9][0-9]*$/.test(next.continuationKey.slice(prefix.length)) || !Number.isFinite(Date.parse(next.claimedAt))) return false;
  }
  return next.state !== "CLOSED" || Number.isFinite(Date.parse(next.closedAt));
}
function humanReadbackError(fresh, pending) {
  const next = fresh?.human_input;
  const same = fresh?.companyId === pending.companyId && fresh.workspaceId === pending.workspaceId
    && fresh.work_ref === pending.workRef && next?.requestId === pending.request.requestId;
  return same && (next.state === "INVALIDATED" || requestExpired(next.expiresAt)
    || ["PAUSED", "CANCELLED", "COMPLETED", "ARCHIVED"].includes(fresh.lifecycle_status))
    ? "原请求已失效或当前不可操作；提交是否完成仍未确认。草稿已保留，请返回原工作核对。"
    : "提交结果尚未确认。草稿已保留，须读到原请求的实际处理结果后才能继续；不会再次提交。";
}
export default function WorkView({ work, api, companyId, onResult, onDiscuss, onRefresh, onEmployeeDetail, discussionSlot, discussionOpen = false }) {
  const controlKey = workControlKey(companyId, work);
  const saved = readWorkControl(controlKey);
  const [action, setAction] = useState(saved?.action || "");
  const [reason, setReason] = useState(saved?.reason || "");
  const [controlPending, setControlPending] = useState(saved?.pending || null);
  const [usage, setUsage] = useState({ records: null, loading: false, error: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [humanText, setHumanText] = useState("");
  const [humanRefs, setHumanRefs] = useState("");
  const [submissionId, setSubmissionId] = useState("");
  const [pendingReadback, setPendingReadback] = useState(null);
  const [invalidatedHuman, setInvalidatedHuman] = useState(null);
  const [mountedAt] = useState(() => Date.now());
  const lock = useRef(false);
  const human = work.human_input;
  const expiresAt = human?.expiresAt ? Date.parse(human.expiresAt) : null;
  const renderTime = typeof mountedAt === "function" ? mountedAt() : mountedAt;
  const expired = expiresAt !== null && (!Number.isFinite(expiresAt) || expiresAt <= renderTime);
  const currentRequest = Boolean(human && Number.isInteger(human.revision) && human.revision > 0
    && (!human.targetRef || human.targetRef === work.work_ref)
    && (!human.companyId || human.companyId === companyId)
    && (!human.workspaceId || human.workspaceId === work.workspaceId)
    && (!work.lifecycle_status || work.lifecycle_status === "ACTIVE")
    && !expired && !(invalidatedHuman?.companyId === companyId && invalidatedHuman.workspaceId === work.workspaceId
      && invalidatedHuman.workRef === work.work_ref && invalidatedHuman.request.requestId === human.requestId));
  const awaitingReadback = Boolean(pendingReadback);
  const humanBlocked = busy || awaitingReadback || Boolean(controlPending) || !currentRequest;
  const sameWork = (fresh) => fresh?.companyId === companyId && fresh.workspaceId === work.workspaceId && fresh.work_ref === work.work_ref;
  function rememberControl(nextAction, nextReason, pending = controlPending) {
    saveWorkControl(controlKey, { action: nextAction, reason: nextReason, pending });
  }
  function reconcileHuman(fresh, pending) {
    if (humanReadbackMatches(fresh, pending)) { setPendingReadback(null); return true; }
    if (humanReadbackInvalidated(fresh, pending)) {
      // Retire only the old human command; preserve its draft and permit lawful Work controls.
      setInvalidatedHuman(pending); setPendingReadback(null);
    }
    setError(humanReadbackError(fresh, pending));
    return false;
  }
  const reportBytes = new TextEncoder().encode(humanText.trim()).length;
  const humanState = {
    WAITING_INPUT: "等待你补充", LOCAL_REPORTED: "已收到本地补充，等待核对",
    EXTERNAL_REPORTED_UNKNOWN: "已收到人工报告，外部事实未知",
    READY: "本地补充已核对，等待续接", CLAIMED: "原工作已领取续接",
  }[human?.state] || "状态待重新读取";
  async function humanAction(event, command) {
    event.preventDefault();
    if (lock.current || humanBlocked || !human) return;
    if (requestExpired(human.expiresAt)) {
      setError("请求已过期，请重新读取原工作。");
      await refreshOriginal();
      return;
    }
    if ((command === "report" && (human.state !== "WAITING_INPUT" || reportBytes > 2000))
      || (command === "review" && (human.state !== "LOCAL_REPORTED" || !human.report?.submissionId))
      || (command === "continue" && (human.state !== "READY" || !human.report?.submissionId))) return;
    const submission = command === "report" ? submissionId || crypto.randomUUID() : human.report.submissionId;
    const references = humanRefs.split(/[,，\s]+/).filter(Boolean);
    const pending = { companyId, workspaceId: work.workspaceId, workRef: work.work_ref, command, submissionId: submission,
      request: { ...human }, report: command === "report"
        ? { text: humanText.trim(), referenceRefs: human.kind === "LOCAL_INFORMATION" ? references : [] }
        : { ...human.report, referenceRefs: [...(human.report.referenceRefs || [])] } };
    if (command === "report" && !submissionId) setSubmissionId(submission);
    lock.current = true; setBusy(true); setError(""); setPendingReadback(pending);
    try {
      try {
        if (command === "report") await api.reportHumanInput(companyId, work, {
          revision: human.revision, submission_id: submission, kind: human.kind,
          local_text: human.kind === "LOCAL_INFORMATION" ? humanText.trim() : "",
          reference_refs: human.kind === "LOCAL_INFORMATION" ? references : [],
          manual_source: human.kind === "EXTERNAL_ACTION_REPORT" ? humanText.trim() : "",
        });
        else if (command === "review") await api.reviewHumanInput(companyId, work);
        else await api.continueHumanInput(work);
      } catch { /* The POST outcome is unknown; only authoritative GET can reconcile it. */ }
      const fresh = await onRefresh();
      reconcileHuman(fresh, pending);
    } catch (cause) {
      setError(`原工作重新读取未成功：${d1Error(cause)}。草稿已保留，核对完成前不能再次提交。`);
    } finally { lock.current = false; setBusy(false); }
  }
  async function control(event) {
    event.preventDefault();
    if (lock.current || controlPending || awaitingReadback || !reason.trim() || !lifecycleActions(work).includes(action)) return;
    lock.current = true; setBusy(true); setError("");
    const pending = { action, reason: reason.trim(), target: controlTarget(work, action) };
    setControlPending(pending); rememberControl(action, reason, pending);
    try {
      await api.controlWork(companyId, work, action, pending.reason);
      const fresh = await onRefresh();
      if (!controlReadbackMatches(companyId, work, fresh, pending)) throw new Error("原工作状态尚未匹配");
      setControlPending(null); setAction(""); setReason(""); saveWorkControl(controlKey, null);
    }
    catch (cause) { setError(`控制结果尚未确认：${d1Error(cause)}。仅重新读取原工作，不会再次提交。`); }
    finally { lock.current = false; setBusy(false); }
  }
  async function refreshOriginal() {
    if (lock.current) return;
    lock.current = true; setBusy(true);
    try {
      const fresh = await onRefresh();
      if (!sameWork(fresh)) throw new Error("原工作范围尚未确认");
      if (pendingReadback && !reconcileHuman(fresh, pendingReadback)) return;
      if (controlPending) {
        if (!controlReadbackMatches(companyId, work, fresh, controlPending)) throw new Error("原控制效果尚未匹配");
        setControlPending(null); setAction(""); setReason(""); saveWorkControl(controlKey, null);
      }
      setPendingReadback(null); setError("");
    }
    catch { setError("原工作重新读取未成功，请稍后重试。草稿仍保留。"); }
    finally { lock.current = false; setBusy(false); }
  }
  async function loadUsage() {
    if (usage.loading) return;
    setUsage({ records: null, loading: true, error: "" });
    try { setUsage({ records: await api.usage(companyId, work), loading: false, error: "" }); }
    catch { setUsage({ records: null, loading: false, error: "使用记录暂不可读取；无法据此判断费用。" }); }
  }
  return <div className={styles.workReading}>
    <header className={styles.pageTitle}><div><p className={styles.crumb}>当前工作</p><h1>{work.problem || "原工作"}</h1></div><span className={styles.badge}>{workState(work.status)}</span></header>
    <div className={styles.employeeBar}><button className={styles.employeeIdentity} disabled={!work.responsibility_holder_ref} aria-label="查看负责人详情" onClick={() => onEmployeeDetail(work.responsibility_holder_ref, work.workspaceId)}><span className={styles.avatar} aria-hidden="true">{(work.responsibility_holder_name || "员").slice(0, 1)}</span><span><strong>{work.responsibility_holder_name || "负责人姓名未记录"}</strong><small>当前负责人</small></span></button><button aria-expanded={discussionOpen} aria-controls="d1-work-discussion" disabled={!work.responsibility_holder_ref} onClick={() => onDiscuss(work.responsibility_holder_ref, work.workspaceId)}>{discussionOpen ? "收起讨论 ⌃" : "一起讨论 ⌄"}</button></div>
    {discussionSlot}
    {human && human.state !== "CLOSED" && human.state !== "INVALIDATED" && <section className={styles.readingSection} aria-label="原工作必要输入">
      <h2>这项工作需要你补充</h2>
      <p className={styles.subtle}>{human.kind === "LOCAL_INFORMATION" ? "本地信息可在核对后续接原工作。" : "外部动作只能由你报告；目前没有独立核验，原工作仍等待。"}</p>
      <dl className={styles.meta}>
        <dt>员工报告的进展</dt><dd>{human.aiCompleted}（来自员工报告，尚未独立核实）</dd>
        <dt>为什么需要你</dt><dd>{human.whyUser}</dd>
        <dt>你需要做什么</dt><dd>{human.userAction}</dd>
        <dt>去哪里处理</dt><dd>{human.destination}</dd>
        <dt>怎样算完成</dt><dd>{human.doneCriterion}</dd>
        <dt>之后如何继续</dt><dd>{human.resumePlan}</dd>
        <dt>当前责任</dt><dd>{work.responsibility_holder_name || "负责人姓名未记录"}</dd>
        <dt>等待条件</dt><dd>{human.waitCondition === "USER_REPORT_AND_RECHECK" ? "你补充后由原工作重新核对" : "请返回原工作核对"}</dd>
        <dt>有效期</dt><dd>{human.expiresAt || "未设统一截止时间；范围变化时失效"}</dd>
        <dt>核实状态</dt><dd>{human.verification === "UNKNOWN" || !human.verification ? "尚未独立核实" : "请返回原工作核对"}</dd>
        <dt>当前状态</dt><dd>{humanState}</dd>
      </dl>
      <details className={styles.sourceDetails}><summary>查看请求来源标识</summary><dl className={styles.meta}><dt>原工作标识</dt><dd>{human.targetRef || work.work_ref}</dd><dt>来源 Task 标识</dt><dd>{human.sourceTaskRef || "未记录"}</dd><dt>负责人标识</dt><dd>{human.holderRef || "未记录"}</dd></dl></details>
      {!currentRequest && <p role="status">这项请求已过期或范围发生变化，请重新读取原工作。</p>}
      {awaitingReadback && <p role="status">正在核对原工作中的提交结果；核对完成前不能再次提交。</p>}
      {(awaitingReadback || !currentRequest) && <button type="button" disabled={busy} onClick={refreshOriginal}>重新读取原工作</button>}
      {human.state === "WAITING_INPUT" && <form className={styles.form} onSubmit={(event) => humanAction(event, "report")}>
        <label>{human.kind === "LOCAL_INFORMATION" ? "补充本地信息" : "填写外部动作报告来源"}<textarea value={humanText} onChange={(event) => setHumanText(event.target.value)} maxLength={2000} required /></label>
        {human.kind === "LOCAL_INFORMATION" && <label>已有参考资料标识（可选，用逗号分隔）<input value={humanRefs} onChange={(event) => setHumanRefs(event.target.value)} /></label>}
        {reportBytes > 2000 && <p role="alert">报告超过 2000 字节，请缩短后提交。</p>}
        <div className={styles.actions}><button className={styles.primary} disabled={humanBlocked || !humanText.trim() || reportBytes > 2000}>提交到原工作</button><button type="button" disabled={busy || awaitingReadback} onClick={() => { setHumanText(""); setHumanRefs(""); setSubmissionId(""); }}>清空草稿</button></div>
      </form>}
      {human.report && <p>用户报告：{human.report.text}。{human.kind === "EXTERNAL_ACTION_REPORT" ? "此报告不等于外部完成核验。" : "待按原工作核对。"}</p>}
      {human.state === "LOCAL_REPORTED" && <button disabled={humanBlocked} onClick={(event) => humanAction(event, "review")}>核对本地补充</button>}
      {human.state === "READY" && <button disabled={humanBlocked || !human.report?.submissionId} onClick={(event) => humanAction(event, "continue")}>续接原工作一次</button>}
      {human.state === "CLAIMED" && <p role="status">续接已领取；请刷新原工作核对结果，不要重复提交。</p>}
    </section>}
    <section className={styles.readingSection}><h2>目标与当前进展</h2><p>{work.expected_result || "预期交付未记录"}</p><p>{work.reason || "进展说明尚未记录。"}</p><dl className={styles.meta}><dt>执行</dt><dd>{{ NONE: "尚无执行记录", SUBMITTING: "正在提交执行", RUNNING: "正在执行", ACCEPTED: "执行结果已验收", PARTIAL: "部分返回，待核对", REJECTED: "执行结果未通过", CANCELLED: "执行已取消", COMPLETED: "已完成", FAILED: "执行失败", UNVERIFIED: "执行情况待核实" }[work.execution_status] || "执行情况待确认"}</dd><dt>下一步</dt><dd>{work.recovery_action || "返回原责任核对"}</dd></dl></section>
    <section className={styles.readingSection}><h2>关联结果</h2>{(work.result_refs || []).length ? work.result_refs.map((ref, index) => <button key={ref} className={styles.matterRow} onClick={() => onResult(ref, work.workspaceId)}><span><strong>{work.result_summaries?.find((item) => item.reference_id === ref)?.title || "工作结果名称未记录"}</strong><small>查看结果 {index + 1}</small></span><span aria-hidden="true">↗</span></button>) : <p className={styles.subtle}>尚未返回结果。当前工作与责任继续保留。</p>}</section>
    <section className={styles.readingSection}><h2>下一步处理</h2><div className={styles.actions}><a href={workspaceEntryHref(work.workspaceId)}>返回原工作空间</a>{lifecycleActions(work).map((item) => <button key={item} disabled={busy || awaitingReadback || Boolean(controlPending)} onClick={() => { setAction(item); rememberControl(item, reason); setError(""); }}>{labels[item]}</button>)}</div>
      {action && <form className={styles.form} onSubmit={control}><label>{labels[action]}的原因<textarea value={reason} disabled={Boolean(controlPending)} onChange={(event) => { setReason(event.target.value); rememberControl(action, event.target.value); }} maxLength={2000} required /></label><div className={styles.actions}><button className={styles.primary} disabled={busy || Boolean(controlPending) || !reason.trim()}>{busy ? "正在确认…" : `确认${labels[action]}`}</button><button type="button" disabled={busy || Boolean(controlPending)} onClick={() => { setAction(""); rememberControl("", reason); }}>取消</button></div></form>}
      {invalidatedHuman?.companyId === companyId && invalidatedHuman.workspaceId === work.workspaceId
        && invalidatedHuman.workRef === work.work_ref && !error && <p role="status">原人工请求已失效；该次提交是否完成仍未确认。草稿仍保留，当前可按原工作状态处理。</p>}
      {controlPending && <p role="status">控制结果尚未确认。原因与原对象已保留，核对完成前不能再次提交。</p>}
      <button type="button" disabled={busy} onClick={refreshOriginal}>重新读取原工作</button>
      {error && <p role="alert" className={styles.error}>{error}</p>}
      <p className={styles.limit}>工作状态以原 Work 为准；外部动作报告仍需独立核实。</p>
    </section>
    <section className={styles.readingSection} aria-label="工作使用记录"><h2>这项工作的使用记录</h2>
      <p className={styles.subtle}>显示当前来源返回的最近至多 200 条记录；缺少记录不能推断费用。</p>
      <button type="button" disabled={usage.loading} onClick={loadUsage}>{usage.loading ? "正在读取…" : "查看使用记录"}</button>
      {usage.error && <p role="alert">{usage.error}</p>}
      {usage.records?.length === 0 && <p>当前来源未返回使用记录；不能据此判断费用。</p>}
      {usage.records?.map((record) => <dl key={record.usage_record_id} className={styles.meta}>
        <dt>记录时间</dt><dd>{record.occurred_at || "未记录"}</dd><dt>执行状态</dt><dd>{record.execution_status || "未知"}</dd>
        <dt>Token</dt><dd>{record.metering_status === "confirmed" ? record.total_tokens ?? "未知" : "未知"}</dd>
        <dt>费用</dt><dd>{record.cost_amount === null || record.cost_amount === undefined ? "未知" : `${record.cost_amount} ${record.currency || ""}`} · {record.cost_source === "estimated" ? "估算" : record.cost_source === "provider_reported" ? "Provider 回报" : "来源未知"}</dd>
        <dt>原执行 / Task / 尝试</dt><dd>{record.execution_ref || "未记录"} / {record.task_id || "未记录"} / {record.attempt_no ?? "未记录"}</dd>
      </dl>)}
    </section>
    <details className={styles.sourceDetails}><summary>查看工作来源详情</summary><dl className={styles.meta}><dt>工作标识</dt><dd>{work.work_ref}</dd><dt>工作空间标识</dt><dd>{work.workspaceId}</dd><dt>负责人标识</dt><dd>{work.responsibility_holder_ref || "未记录"}</dd><dt>责任标识</dt><dd>{work.responsibility_key || "未记录"}</dd><dt>工作来源状态</dt><dd>{work.lifecycle_status || "未记录"}</dd><dt>执行来源状态</dt><dd>{work.execution_status || "未记录"}</dd><dt>结果来源</dt><dd>{(work.result_refs || []).join(" / ") || "未记录"}</dd></dl></details>
  </div>;
}
