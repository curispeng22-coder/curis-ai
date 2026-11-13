"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { ConversationComposer } from "../../v1/SharedConversation.js";
import { d1Error } from "../../../lib/d1Api.js";
import { interactionKey, readDraft, saveDraft, messageRequest, pendingRequest, rememberRequest, isMatchingCompletion, remainingDraft, executionLabel } from "../../../lib/d1State.mjs";
import styles from "./D1.module.css";

const attemptCopy = { RUNNING: "员工正在处理这条消息", FAILED: "这次执行已失败，原消息保留", UNVERIFIED: "执行结果尚未核实，请先重新读取", COMPLETED: "员工回复已返回" };

export default function EmployeeConversationView({ companyId, entry, api, compact = false, onFull, onEntry, onResult, onEmployeeDetail }) {
  const key = interactionKey(companyId, entry);
  const [view, setView] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [recent, setRecent] = useState([]);
  const [employee, setEmployee] = useState(entry.employeeRef || "");
  const [title, setTitle] = useState("");
  const [assignment, setAssignment] = useState("");
  const [input, setInput] = useState(() => readDraft(key));
  const currentInput = useRef(input);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const request = useRef(pendingRequest(key));
  const createRequest = useRef(null);
  const lock = useRef(false);
  const alive = useRef(true);
  const changeInput = useCallback((value) => { currentInput.current = value; setInput(value); saveDraft(key, value); }, [key]);
  const clearSentDraft = useCallback((sent) => {
    const remaining = remainingDraft(currentInput.current, sent.body, sent.inputAtSend ?? sent.body);
    if (remaining !== currentInput.current) changeInput(remaining);
  }, [changeInput]);
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);

  useEffect(() => {
    let active = true;
    api.employees(companyId).then((payload) => { if (active) setEmployees(payload.employees || []); }).catch(() => { if (active) setError("员工目录暂未读取，请重试。"); });
    api.recent(companyId).then((payload) => { if (active) setRecent(payload.conversations || []); }).catch(() => { if (active) setRecent([]); });
    return () => { active = false; };
  }, [api, companyId]);

  useEffect(() => {
    let active = true;
    if (!entry.conversationId && !entry.employeeRef) { setLoading(false); return () => { active = false; }; }
    setLoading(true); setError("");
    api.conversation(companyId, entry).then((value) => {
      if (value.company_id !== companyId || (entry.conversationId && value.conversation_id !== entry.conversationId) || (entry.conversationId && entry.employeeRef && ![value.owner_ref, value.employee?.id].includes(entry.employeeRef))) throw new Error("会话身份不一致");
      if (!active) return;
      setView(value); setEmployee(value.owner_ref || "");
      setAssignment((current) => value.assignments?.some((item) => item.assignment_ref === current) ? current : value.assignments?.length === 1 ? value.assignments[0].assignment_ref : "");
      setLoading(false);
      if (isMatchingCompletion(value, request.current)) {
        clearSentDraft(request.current);
        request.current = null; rememberRequest(key, null);
      }
    }).catch((cause) => { if (active) { setLoading(false); setError(d1Error(cause)); } });
    return () => { active = false; };
  }, [api, companyId, entry, refresh, key, clearSentDraft]);

  const contextWorkspace = entry.workspaceId || view?.assignments?.find((item) => item.assignment_ref === assignment)?.workspace_id || "";
  useEffect(() => {
    let active = true;
    setProfile(null);
    if (view?.owner_ref && contextWorkspace) api.employeeDetail(companyId, view.owner_ref, contextWorkspace).then((value) => { if (active) setProfile(value); }).catch(() => {});
    return () => { active = false; };
  }, [api, companyId, view?.owner_ref, contextWorkspace]);

  const running = view?.attempts?.some((item) => item.status === "RUNNING");
  useEffect(() => {
    if (!running) return undefined;
    const timer = window.setInterval(() => setRefresh((value) => value + 1), 2000);
    return () => window.clearInterval(timer);
  }, [running]);

  async function start(event) {
    event.preventDefault();
    if (lock.current) return;
    lock.current = true; setBusy(true); setError("");
    try {
      if (entry.conversationId) {
        const value = await api.joinTopic(companyId, entry.conversationId, employee);
        if (!alive.current) return;
        setView(value); setAssignment(value.assignments?.length === 1 ? value.assignments[0].assignment_ref : "");
      } else {
        const signature = JSON.stringify([title, employee]);
        if (createRequest.current?.signature !== signature) createRequest.current = { signature, title, employee_ref: employee || null, request_id: crypto.randomUUID() };
        const { signature: _signature, ...payload } = createRequest.current;
        const value = await api.createTopic(companyId, payload);
        if (!alive.current) return;
        onEntry({ ...entry, conversationId: value.conversation_id, employeeRef: value.owner_ref || "", view: "conversation", explicit: false });
      }
    } catch (cause) { setError(d1Error(cause)); }
    finally { lock.current = false; setBusy(false); }
  }
  async function send(event, retry = false) {
    event.preventDefault();
    if (lock.current || running || !view || (!retry && !input.trim()) || (view.owner_ref && !assignment)) return;
    if (retry) {
      const latest = view.attempts?.at(-1);
      const original = view.messages?.find((item) => item.message_id === latest?.message_id);
      if (!original || latest.status !== "FAILED" || latest.retry_no || original.context?.assignment_ref !== assignment || original.references?.length) return;
      request.current = { body: original.body, assignment_ref: assignment, references: [], request_id: original.idempotency_key, retry_no: 1 };
    } else request.current = messageRequest(request.current, { body: input, assignment_ref: assignment }, () => crypto.randomUUID());
    request.current = { ...request.current, inputAtSend: currentInput.current };
    rememberRequest(key, request.current);
    const sent = request.current;
    lock.current = true; setBusy(true); setError("");
    try {
      const value = await api.send(companyId, entry, sent);
      if (!alive.current) return;
      if (value.company_id !== companyId || (entry.conversationId && value.conversation_id !== entry.conversationId)) throw new Error("会话身份不一致");
      setView(value);
      if (!value.owner_ref || isMatchingCompletion(value, sent)) {
        clearSentDraft(sent);
        if (request.current?.request_id === sent.request_id) { request.current = null; rememberRequest(key, null); }
      }
    } catch (cause) { setError(d1Error(cause)); }
    finally { lock.current = false; setBusy(false); }
  }

  const latest = view?.attempts?.at(-1);
  const original = view?.messages?.find((item) => item.message_id === latest?.message_id);
  const retryAllowed = latest?.status === "FAILED" && !latest.retry_no && original?.context?.assignment_ref === assignment && !original?.references?.length;
  const name = view?.employee?.name || employees.find((item) => item.employee_ref === (view?.owner_ref || entry.employeeRef))?.name || "员工讨论";
  return <section className={`${styles.conversation} ${compact ? styles.compact : ""}`} aria-label={compact ? "轻量员工讨论" : "完整员工讨论"} data-conversation-id={view?.conversation_id || ""}>
    <header className={styles.conversationHeader}><button className={styles.employeeIdentity} aria-label="查看讨论员工详情" disabled={!view?.owner_ref} onClick={() => onEmployeeDetail(view.owner_ref, contextWorkspace)}><span className={styles.avatar} aria-hidden="true">{name.slice(0, 1)}</span><span><strong>{name}</strong><small>{view?.title || "保留当时的工作范围"}</small></span></button>{compact && <button onClick={onFull}>打开完整讨论 ↗</button>}</header>
    {!view?.owner_ref && !entry.employeeRef && !loading && <form className={styles.form} onSubmit={start}>
      {!entry.conversationId && <label>想讨论什么？<input value={title} onChange={(event) => setTitle(event.target.value)} maxLength={120} placeholder="给这段讨论一个名称" /></label>}
      <label>与谁讨论<select value={employee} onChange={(event) => setEmployee(event.target.value)}><option value="">稍后选择员工</option>{employees.map((item) => <option key={item.employee_ref} value={item.employee_ref}>{item.name}</option>)}</select></label>
      <button className={styles.primary} disabled={busy || (Boolean(entry.conversationId) && !employee)}>{busy ? "正在保存…" : entry.conversationId ? "邀请员工继续" : "开始对话"}</button>
    </form>}
    {!compact && recent.length > 0 && <details className={styles.topics}><summary>其他话题 · 各自保留消息和输入</summary>{recent.map((item) => <button key={item.conversation_id} onClick={() => onEntry({ view: "conversation", conversationId: item.conversation_id, employeeRef: "", explicit: false })}>{item.title || "未命名话题"}</button>)}</details>}
    {loading ? <p className={styles.loading} role="status">正在读取原会话…</p> : <div className={styles.messages}>
      {view && !view.messages?.length && <p className={styles.subtle}>还没有消息。讨论不会自动创建工作或接受结果。</p>}
      {(view?.messages || []).map((message) => <article key={message.message_id} className={styles.message}><header><strong>{message.sender?.kind === "CEO" ? "你" : name}</strong><small>{{ COMPANY: "公司讨论", DEPARTMENT: "部门讨论", BUSINESS: "业务讨论", WORKSPACE: "工作讨论" }[message.context?.scope_type] || "公司讨论"}</small></header><p>{message.body}</p>{message.references?.map((ref, index) => <div className={styles.reference} key={`${ref.kind}:${ref.reference_id}:${index}`}><span>{ref.title || "来源名称未记录"} · 引用 {index + 1}</span>{["RESULT", "OUTCOME"].includes(ref.kind) && <button onClick={() => onResult(ref.reference_id, ref.workspace_id)}>打开结果</button>}<details className={styles.sourceDetails}><summary>查看引用来源详情</summary><p>{ref.kind} · {ref.reference_id}</p><p>用途：{ref.purpose || "未记录"} · 版本：{ref.result_version || "未记录"}</p></details></div>)}<details className={styles.sourceDetails}><summary>查看消息来源详情</summary><dl className={styles.meta}><dt>消息标识</dt><dd>{message.message_id}</dd><dt>当时范围</dt><dd>{message.context?.scope_type || "COMPANY"} · {message.context?.scope_ref || message.context?.company_id}</dd><dt>当时责任</dt><dd>{message.context?.assignment_ref || "未记录"}</dd></dl></details></article>)}
    </div>}
    {view && <ConversationComposer value={input} onChange={changeInput} onSubmit={send} placeholder="说说你想推进什么…" inputAriaLabel="讨论消息" maxLength={8000} showVoice={false} className={styles.composer} inputClassName={styles.composerInput} actionsClassName={styles.composerActions} busy={busy} disabled={running || loading || (Boolean(view.owner_ref) && !assignment)} submitLabel={running ? "等待员工回复" : "发送"}
      referenceControl={<button type="button" disabled title="当前尚不能核对资料版本，请从原工作空间处理">添加资料暂不可用</button>}
      access={profile?.composer?.computer_access || null}
      accessExecutor={{ modelBacked: Boolean(profile?.composer?.model_backed), agentBacked: Boolean(profile?.composer?.agent_backed) }}
      controls={<div className={styles.composerControls}><label>当前工作范围<select value={assignment} disabled={busy || running || !view.owner_ref} onChange={(event) => setAssignment(event.target.value)}><option value="">{view.owner_ref ? "请选择工作责任" : "员工尚未加入"}</option>{(view.assignments || []).map((item) => <option key={item.assignment_ref} value={item.assignment_ref}>{item.responsibility || "责任名称未记录"}</option>)}</select></label><p>{executionLabel(profile?.bindings)}</p><p>此对话暂不支持切换工作模式</p></div>}
      notice={<>添加资料需要先核对其版本，当前请回原工作空间处理。执行使用员工当前的绑定；绑定不代表执行已完成。需要核对能力时，可前往<Link href="/ceo-office/capabilities" prefetch={false}>人才与能力</Link>。</>} />}
    {latest && <p className={styles.attempt} role="status">{attemptCopy[latest.status] || "执行状态待核对"}</p>}
    {error && <p role="alert" className={styles.error}>{error}</p>}
    <div className={styles.actions}><button onClick={() => setRefresh((value) => value + 1)} disabled={busy}>重新读取会话</button>{retryAllowed && <button disabled={busy || running} onClick={(event) => send(event, true)}>重试已失败消息</button>}</div>
  </section>;
}
