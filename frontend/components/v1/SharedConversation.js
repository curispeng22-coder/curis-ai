"use client";
import Link from "next/link";
import { computerAccessView } from "../../lib/computerAccess.mjs";
function ComposerUpcomingControl({ label }) {
  return <button type="button" disabled aria-disabled="true" title={`${label}即将推出，当前版本暂不可用`} className="rounded-lg border border-ui-line bg-ui-surface-2 px-2 py-1.5 text-xs text-ui-txt-3">{label} · 即将推出</button>;
}
export function ComputerAccessSlot({ access = null, accessExecutor = null }) {
  const view = computerAccessView(access, accessExecutor || {});
  return <button type="button" disabled aria-disabled="true" title={view.title}
    className="rounded-lg border border-ui-line bg-ui-surface-2 px-2 py-1.5 text-xs text-ui-txt-2">{view.label}</button>;
}
export function ConversationComposer({ value, onChange, onSubmit, placeholder, busy = false, disabled = false, submitLabel = "发送", referenceHref, referenceControl, controls, notice, className, inputClassName, actionsClassName, inputAriaLabel, maxLength, showVoice = true, showSubmit = true, access = null, accessExecutor = null }) {
  return <form onSubmit={onSubmit} className={className || "border-t border-ui-line p-3"}>
    <textarea aria-label={inputAriaLabel || placeholder || "输入消息"} maxLength={maxLength} value={value} onChange={(event) => onChange?.(event.target.value)} placeholder={placeholder} rows={2} className={inputClassName || "w-full resize-none bg-transparent px-2 py-1 text-sm text-ui-txt outline-none placeholder:text-ui-txt-3"} />
    <div className={actionsClassName || "mt-2 flex flex-wrap items-center gap-2"}>
      {referenceControl || (referenceHref ? <a href={referenceHref} className="rounded-lg border border-ui-line px-2.5 py-1.5 text-xs text-ui-txt-2">＋ 参考资料</a> : <button type="button" disabled title="此对话尚不支持添加资料；可从具体工作选择资料" className="rounded-lg px-2.5 py-1.5 text-xs text-ui-txt-3">参考资料未接入</button>)}
      <ComputerAccessSlot access={access} accessExecutor={accessExecutor} />
      <ComposerUpcomingControl label="工作模式" />
      {controls}
      <ComposerUpcomingControl label="Auto" />
      {showVoice && <button type="button" disabled title="语音输入尚未连接" className="rounded-lg px-2 py-1.5 text-xs text-ui-txt-3">语音</button>}
      {showSubmit && <button type="submit" disabled={busy || disabled || !value?.trim()} style={{ background: "var(--ui-action-primary-bg)", color: "var(--ui-action-primary-fg)" }} className="ml-auto rounded-lg bg-ui-primary px-4 py-2 text-xs font-semibold text-ui-primary-fg disabled:opacity-40">{busy ? "处理中…" : submitLabel}</button>}
    </div>
    {notice ? <p className="mt-2 px-2 text-xs text-ui-txt-2">{notice}</p> : null}
  </form>;
}

export default function SharedConversation({ employee, scopeKey = "", messages = [], children, value, onChange, onSubmit, placeholder = "说说你想推进什么…", submitLabel = "发送", allowWithoutModel = false, busy = false, referenceHref }) {
  const model = useConversationModel(scopeKey);
  const ready = model.status === "ready" && Boolean(model.selected);
  const selectedName = model.selected?.model_id || model.selected?.model_name || "";
  return <section data-conversation-owner={employee?.assistant_id || employee?.employee_ref || employee?.id || ""} className="overflow-hidden rounded-2xl border border-ui-line bg-ui-surface">
    <header className="flex items-center gap-3 border-b border-ui-line px-5 py-4">
      <EmployeeAvatar employee={{ ...employee, name: employee?.name || "CEO 助理" }} />
      <div><h2 className="text-sm font-semibold text-ui-txt">{employee?.name || "CEO 助理"}</h2><p className="text-xs text-ui-txt-2">{employee?.role || "公司级协调与经营跟进"}</p></div>
      <span className="ml-auto text-xs text-ui-txt-2">{ready ? "对话模型可用 · 员工执行以工作绑定为准" : "尚未连接模型"}</span>
    </header>
    <div className="max-h-[420px] min-h-[190px] space-y-4 overflow-y-auto px-5 py-5">
      {messages.map((message, index) => <div key={message.message_id || `${message.role}-${index}`} className={["ceo", "user"].includes(message.role) ? "ml-auto max-w-[80%] rounded-2xl bg-ui-primary-soft px-4 py-3 text-sm text-ui-txt" : "max-w-[88%] text-sm leading-6 text-ui-txt-2"}>
        {message.text}
        {message.references?.map((reference) => reference.href?.startsWith("/ceo-office") && !reference.href.startsWith("//") ? <a key={reference.reference_id} href={reference.href} className="mt-2 block text-ui-primary">{reference.title || "查看来源"} ▸</a> : null)}
      </div>)}
      {children}
    </div>
    <ConversationComposer value={value} onChange={onChange} onSubmit={(event) => onSubmit?.(event, model.selected)} placeholder={placeholder} busy={busy} disabled={!allowWithoutModel && !ready} submitLabel={submitLabel} referenceHref={referenceHref} access={{ state: "MODEL_EXECUTOR_NOT_APPLICABLE" }}
      controls={<select aria-label="当前对话模型" value={selectedName} onChange={(event) => { const selected = model.models.find((item) => item.model_name === event.target.value); if (selected) model.choose(selected); }} className="rounded-lg border border-ui-line bg-ui-surface px-2.5 py-1.5 text-xs text-ui-txt-2"><option value="">{model.status === "loading" ? "正在检查模型…" : "选择对话模型"}</option>{model.models.map((item) => <option key={`${item.provider_type}:${item.model_name}`} value={item.model_name}>{item.model_name}</option>)}</select>}
      notice={!ready ? allowWithoutModel ? "当前可提交人工内容；自动回复与后续执行仍需各自满足条件。" : "尚未连接可用模型。输入会保留；请到人才与能力连接模型后重试。业务草稿仍可整理。" : null} />
    {!ready ? <Link href="/ceo-office/capabilities" className="block px-5 pb-3 text-xs text-ui-primary">{allowWithoutModel ? "配置自动回复模型 →" : "检查模型连接 →"}</Link> : null}
  </section>;
}
import { useEffect, useRef, useState } from "react";
import { getAssignedAgentWorkflow, publishAssignedAgentWorkflow, createAssignedWork, continueOriginalAgentWork, getOriginalAgentWork, executeOriginalAgentWork, stopOriginalAgentWork, getAgentCandidateSource, createAgentCandidate, getResultDetail } from "../../lib/v1FrontendApi.js";
import ResultReferenceView, { resultSelection } from "./ResultReferenceView.js";
import { getEnabledModels, getModelPreference, recoverAIProvider } from "../../lib/v1FrontendApi.js";
import { EmployeeAvatar } from "./EmployeeAvatar.js";

export function AgentWorkControl({ companyId, workspaceId, tenantId, assignmentRef, agents = [], readiness, body,
  contextKey = "", source = null, disabled = false, returnHref = "", businessReturn = null, onCandidate }) {
  const [binding, setBinding] = useState(""), [expected, setExpected] = useState("提供与本次请求相关、可核验的成果与来源");
  const [browserHosts, setBrowserHosts] = useState("");
  const [snapshot, setSnapshot] = useState(null), [busy, setBusy] = useState(false), [error, setError] = useState("");
  const [result, setResult] = useState(null), [pending, setPending] = useState(null);
  const [hydration, setHydration] = useState({ key: "", state: "loading" });
  const [candidate, setCandidate] = useState(null), [excerpt, setExcerpt] = useState(null), [candidateNotice, setCandidateNotice] = useState("");
  const [draftExcerpt, setDraftExcerpt] = useState(null);
  const currentExcerpt = useRef(null), currentDraft = useRef(null);
  const [followupBasis, setFollowupBasis] = useState(null);
  const [candidateContext, setCandidateContext] = useState(null), [candidateLoading, setCandidateLoading] = useState(false);
  const candidateRequest = useRef(0);
  const [workflow, setWorkflow] = useState(null), [workflowConsent, setWorkflowConsent] = useState(false);
  const workflowSupported = ["content-growth", "writing", "music"].includes(pending?.payload?.source?.kind || source?.kind);
  const savedSource = pending?.payload?.source, savedSelection = savedSource?.selection;
  const savedAgent = agents.find((item) => item.binding_id === pending?.payload?.agent_binding_ref);
  const pendingBindingUnverified = Boolean(pending?.payload && !savedAgent);
  const originalValue = (value) => value === undefined || value === null || value === "" ? "原请求未提供" : typeof value === "object" ? JSON.stringify(value) : String(value);
  const generation = useRef(0), operation = useRef(false);
  const stored = useRef(null);
  const cacheKey = JSON.stringify(["curis.agent-work", tenantId, companyId, workspaceId, assignmentRef, contextKey]);
  const sourceIdentity = (value) => {
    if (!value || value.kind === "references") return value?.kind === "references" ? { kind: "references" } : null;
    const fields = { "content-growth": ["content_ref"], writing: ["book_ref", "chapter_ref"], music: ["song_ref"] }[value.kind];
    if (!fields || fields.some((field) => typeof value[field] !== "string" || !value[field])) return null;
    return Object.fromEntries([["kind", value.kind], ...fields.map((field) => [field, value[field]])]);
  };
  const identity = sourceIdentity(source);
  const contextMatchesSource = identity?.kind === "content-growth" ? contextKey === `content:${identity.content_ref}`
    : identity?.kind === "writing" ? contextKey === `chapter:${identity.book_ref}:${identity.chapter_ref}`
    : identity?.kind === "music" ? contextKey === `song:${identity.song_ref}` : identity?.kind === "references";
  const contextStamp = JSON.stringify([cacheKey, identity]);
  const liveKey = useRef(contextStamp); liveKey.current = contextStamp;
  const sourceStamp = JSON.stringify(source), liveSource = useRef(sourceStamp); liveSource.current = sourceStamp;
  function chooseExcerpt(value) { currentExcerpt.current = value; setExcerpt(value); }
  function prepareExcerpt(value) { currentDraft.current = value; setDraftExcerpt(value); }
  const scope = { tenantId, companyId, workspaceId, assignmentRef, contextKey, source: identity };
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const validSource = (payload) => !payload || (identity && same(sourceIdentity(payload.source), identity));
  const validPending = (saved) => saved && typeof saved === "object" && !Array.isArray(saved)
    && saved.scope?.version === 1 && same(saved.scope.binding, scope)
    && (saved.work_ref || saved.payload?.request_id) && validSource(saved.payload)
    && validSource(saved.followup_payload) && (!saved.followup_payload || (saved.work_ref && saved.predecessor_ref && saved.followup_payload.request_id));
  const ready = hydration.key === contextStamp && hydration.state === "ready" && liveKey.current === contextStamp && Boolean(identity) && contextMatchesSource;
  function checked(value) {
    if (value.tenant_id !== tenantId || value.work?.company_id !== companyId || value.work?.workspace_id !== workspaceId)
      throw new Error("原工作不属于当前公司与责任范围。");
    return value;
  }
  function verifiedWork(value, workRef) {
    checked(value);
    const work = value.work, proof = value.origin;
    return (value.root_work_ref || work?.entity_id) === workRef
      && proof?.status === "VERIFIED" && proof.assignment_ref === assignmentRef
      && identity && same(sourceIdentity(proof.source), identity)
      && (identity.kind !== "references" || proof.source?.conversation_id === contextKey);
  }
  useEffect(() => {
    const epoch = ++generation.current; operation.current = false;
    setSnapshot(null); setPending(null); setBinding(""); setError(""); setBusy(false);
    setBrowserHosts(""); setResult(null); setWorkflow(null); setWorkflowConsent(false);
    setCandidate(null); chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null); setCandidateNotice("");
    candidateRequest.current += 1; setCandidateContext(null); setCandidateLoading(false);
    setHydration({ key: contextStamp, state: "loading" });
    if (!tenantId || !companyId || !workspaceId || !assignmentRef || !contextKey || !identity || !contextMatchesSource) return;
    try {
      stored.current = localStorage.getItem(cacheKey);
      const saved = stored.current === null ? null : JSON.parse(stored.current);
      if (stored.current !== null) {
        if (!saved || typeof saved !== "object" || Array.isArray(saved)) throw new Error("原请求格式无效。");
        if (!saved.work_ref && !saved.payload?.request_id) throw new Error("原请求标识缺失。");
        setPending(saved);
        const legacyWork = !saved.scope && saved.work_ref && validSource(saved.payload) && validSource(saved.followup_payload)
          && (!saved.followup_payload || (saved.predecessor_ref && saved.followup_payload.request_id));
        if (!validPending(saved) && !legacyWork) {
          setHydration({ key: contextStamp, state: "review" });
          setError("本地原请求的身份或来源无法完整核验；记录已保留。请核对原工作，联系负责人处理后再继续。");
        }
        if (saved.payload) {
          setBinding(saved.payload.agent_binding_ref || ""); setExpected(saved.payload.expected_result || "");
          setBrowserHosts((saved.payload.browser_hosts || []).join(", "));
        }
        if (saved.work_ref) {
          setHydration({ key: contextStamp, state: "review" });
          setError("正在核对原工作的责任与来源；证据不足时将保留记录并等待负责人处理。");
          getOriginalAgentWork(saved.work_ref).then((value) => {
          if (epoch === generation.current && contextStamp === liveKey.current) {
            setSnapshot(checked(value));
            if ((validPending(saved) || legacyWork) && verifiedWork(value, saved.work_ref)
              && (!saved.followup_payload || saved.predecessor_ref === value.work?.entity_id)) {
              setHydration({ key: contextStamp, state: "ready" }); setError("");
            } else setError("原工作的责任或业务来源无法完整核验；记录已保留，请联系负责人处理。");
          }
        }).catch((reason) => { if (epoch === generation.current && contextStamp === liveKey.current) setError(reason.message); });
        } else {
          setHydration({ key: contextStamp, state: "review" });
          setError("原创建请求的结果尚未核验；记录已保留，请联系负责人处理，不会重复提交。");
        }
      }
      if (stored.current === null) setHydration({ key: contextStamp, state: "ready" });
    } catch { setPending({ unverified: true }); setHydration({ key: contextStamp, state: "review" }); setError("本地原请求无法核验，请保留现场并联系负责人处理。"); }
    return () => { generation.current += 1; };
  }, [cacheKey, contextStamp]);
  useEffect(() => { clearCandidateRead(); }, [sourceStamp]);
  const task = snapshot?.tasks?.at(-1);
  const historyTasks = (snapshot?.history || (snapshot ? [snapshot] : [])).flatMap((entry) =>
    (entry.tasks || []).map((item) => ({ ...item, work_ref: item.work_ref || entry.work.entity_id })));
  const localEvidence = task && Array.isArray(snapshot?.history)
    ? snapshot.history.flatMap((entry) => (entry.tasks || []).filter((item) => item.task_id === task.task_id)
      .map((item) => ({ state: item.local_process_state, sameWork: entry.work?.entity_id === snapshot.work?.entity_id &&
        (!item.work_ref || item.work_ref === snapshot.work.entity_id) }))) : [];
  const directChildReaped = task?.local_process_state === "DIRECT_CHILD_REAPED" && localEvidence.length > 0 &&
    localEvidence.every((item) => item.sameWork && item.state === "DIRECT_CHILD_REAPED");
  const outcomeUncertain = (snapshot?.tasks || []).some((item) =>
    ["outcome_unknown", "outcome_unverified"].includes(item.reason_code)) ||
    historyTasks.some((item) => item.work_ref === snapshot?.work?.entity_id &&
      ["outcome_unknown", "outcome_unverified"].includes(item.reason_code));
  const running = task && ["INIT", "PARSED", "RUNNING"].includes(task.status);
  useEffect(() => {
    if ((!running && !busy) || !snapshot?.work?.entity_id) return;
    const epoch = generation.current;
    const interval = setInterval(() => getOriginalAgentWork(snapshot.work.entity_id).then((value) => {
      if (epoch === generation.current && contextStamp === liveKey.current) setSnapshot(checked(value));
    }).catch(() => { if (epoch === generation.current && contextStamp === liveKey.current) setError("进度暂时无法读取；不会重新执行。"); }), 2000);
    return () => clearInterval(interval);
  }, [running, busy, snapshot?.work?.entity_id, cacheKey]);
  async function read() {
    if (hydration.key !== contextStamp || liveKey.current !== contextStamp || (!snapshot?.work?.entity_id && !pending?.work_ref)) return;
    const epoch = generation.current;
    try { const value = checked(await getOriginalAgentWork(snapshot?.work?.entity_id || pending.work_ref)); if (epoch === generation.current && contextStamp === liveKey.current) { setSnapshot(value); setError(""); } }
    catch (reason) { if (epoch === generation.current && contextStamp === liveKey.current) setError(reason.message); }
  }
  function checkedWorkflow(value) {
    if (value.tenant_id !== tenantId || value.company_id !== companyId || value.workspace_id !== workspaceId || value.assignment_ref !== assignmentRef)
      throw new Error("责任流程不属于当前公司与工作空间。");
    return value;
  }
  async function inspectWorkflow() {
    if (!ready || liveKey.current !== contextStamp || operation.current || busy || disabled || !tenantId || !assignmentRef) return;
    const epoch = generation.current; operation.current = true; setBusy(true); setError(""); setWorkflowConsent(false);
    try {
      const value = checkedWorkflow(await getAssignedAgentWorkflow(assignmentRef, companyId, workspaceId));
      if (epoch === generation.current && contextStamp === liveKey.current) setWorkflow(value);
    } catch (reason) { if (epoch === generation.current && contextStamp === liveKey.current) { setWorkflow(null); setError(reason.message); } }
    finally { if (epoch === generation.current && contextStamp === liveKey.current) { operation.current = false; setBusy(false); } }
  }
  async function publishWorkflow() {
    if (!ready || liveKey.current !== contextStamp || operation.current || busy || disabled || !workflowConsent || !workflow?.publication_allowed) return;
    const epoch = generation.current; operation.current = true; setBusy(true); setError("");
    try {
      const value = checkedWorkflow(await publishAssignedAgentWorkflow(assignmentRef, {
        company_id: companyId, workspace_id: workspaceId, expected_revision: workflow.assignment_revision,
        review_token: workflow.review_token, confirm: true,
      }));
      if (epoch === generation.current && contextStamp === liveKey.current) setWorkflow(value);
    } catch (reason) {
      if (epoch === generation.current && contextStamp === liveKey.current) {
        setWorkflow(null);
        setError((reason.message || "发布结果尚未核验。") + " 请重新核对责任流程；原创建请求仍保留。");
      }
    } finally { if (epoch === generation.current && contextStamp === liveKey.current) { setWorkflowConsent(false); operation.current = false; setBusy(false); } }
  }
  async function start(continueOriginal = false) {
    if (!ready || liveKey.current !== contextStamp || operation.current || busy || disabled || !tenantId || !assignmentRef) return;
    const epoch = generation.current; operation.current = true; setBusy(true); setError("");
    try {
      if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("本地原请求已变化，请重新打开并核对。");
      let request = pending;
      let workRef = snapshot?.work?.entity_id || request?.work_ref;
      if (!workRef) {
        if (request && !request.payload?.request_id) throw new Error("本地原请求无法核验，请保留现场。");
        if (request && !agents.some((item) => item.binding_id === request.payload.agent_binding_ref))
          throw new Error("原请求绑定的 Agent 当前无法核验，请核对该员工的原绑定；原请求保持不变。");
        if (!request) {
          if (!body?.trim() || !agents.some((item) => item.binding_id === binding)) throw new Error("请保留任务输入并选择当前员工的 Agent。");
          request = { scope: { version: 1, binding: scope }, payload: { request_id: crypto.randomUUID(), problem: body.trim(), expected_result: expected.trim(),
            agent_binding_ref: binding, browser_hosts: browserHosts.split(/[\s,，]+/).filter(Boolean),
            ...(source ? { source } : {}) } };
          stored.current = JSON.stringify(request); localStorage.setItem(cacheKey, stored.current); setPending(request);
        }
        if (["content-growth", "writing", "music"].includes(request.payload.source?.kind)) {
          const current = checkedWorkflow(await getAssignedAgentWorkflow(assignmentRef, companyId, workspaceId));
          if (epoch !== generation.current || contextStamp !== liveKey.current) return;
          setWorkflow(current); setWorkflowConsent(false);
          if (current.state !== "READY") throw new Error(current.reason);
        }
        if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("本地原请求已变化，请重新打开并核对。");
        const created = await createAssignedWork(assignmentRef, request.payload);
        if (epoch !== generation.current || contextStamp !== liveKey.current) return;
        if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("创建结果待核验，本地原请求已变化。");
        workRef = created.work.entity_id; request = { ...request, work_ref: workRef };
        stored.current = JSON.stringify(request); localStorage.setItem(cacheKey, stored.current); setPending(request);
      }
      const original = checked(await getOriginalAgentWork(workRef));
      if (epoch !== generation.current || contextStamp !== liveKey.current) return;
      if (!verifiedWork(original, request.work_ref)) throw new Error("原工作的责任或业务来源无法完整核验。");
      workRef = original.work.entity_id;
      setSnapshot(original);
      if ((original.tasks || []).some((item) => ["outcome_unknown", "outcome_unverified"].includes(item.reason_code)) ||
        (original.history || []).some((entry) => entry.work?.entity_id === workRef && (entry.tasks || []).some((item) =>
        ["outcome_unknown", "outcome_unverified"].includes(item.reason_code)))) {
        setError("执行状态和外部效果仍需核验，不能重复启动。");
        return;
      }
      const previous = original.tasks.at(-1);
      if (previous && !(continueOriginal && previous.status === "FAILED" && !previous.call_reserved)) return;
      await executeOriginalAgentWork(workRef);
      if (epoch === generation.current && contextStamp === liveKey.current) setSnapshot(checked(await getOriginalAgentWork(workRef)));
    } catch (reason) { if (epoch === generation.current && contextStamp === liveKey.current) setError((reason.message || "原工作结果待核验。") + " 输入与原请求保留，没有自动重试。"); }
    finally { if (epoch === generation.current && contextStamp === liveKey.current) { operation.current = false; setBusy(false); } }
  }
  async function followUp() {
    if (!ready || liveKey.current !== contextStamp || operation.current || busy || disabled || !snapshot || !body?.trim()
      || !verifiedWork(snapshot, pending?.work_ref) || pending?.followup_payload
      || !followupBasis || followupBasis.sourceStamp !== liveSource.current || followupBasis.workRef !== snapshot.work.entity_id || followupBasis.taskRef !== task?.task_id) return;
    const epoch = generation.current; operation.current = true; setBusy(true); setError("");
    try {
      if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("本地原请求已变化，请重新打开并核对。");
      const latest = checked(await getOriginalAgentWork(pending.work_ref));
      if (epoch !== generation.current || contextStamp !== liveKey.current || followupBasis.sourceStamp !== liveSource.current) return;
      const latestTask = latest.tasks?.at(-1);
      const uncertain = (latest.tasks || []).some((item) => ["outcome_unknown", "outcome_unverified"].includes(item.reason_code))
        || (latest.history || []).some((entry) => entry.work?.entity_id === latest.work?.entity_id && (entry.tasks || []).some((item) =>
          ["outcome_unknown", "outcome_unverified"].includes(item.reason_code)));
      if (!verifiedWork(latest, pending.work_ref) || latest.work?.entity_id !== snapshot.work.entity_id
        || latestTask?.task_id !== task?.task_id || latestTask?.status !== "COMPLETED" || uncertain)
        throw new Error("原工作、成果或来源已变化或尚未核验，请重新读取。");
      if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("本地原请求已变化，请重新打开并核对。");
      let request = pending;
      if (!request?.followup_payload) {
        request = { ...pending, scope: { version: 1, binding: scope }, work_ref: snapshot.root_work_ref || snapshot.work.entity_id,
          predecessor_ref: snapshot.work.entity_id, followup_payload: {
            request_id: crypto.randomUUID(), problem: body.trim(), expected_result: expected.trim(),
            accepted_task_ref: task.task_id, accept_result: true, source, prior_result: followupBasis.basis,
            browser_hosts: browserHosts.split(/[\s,，]+/).filter(Boolean) } };
        stored.current = JSON.stringify(request); localStorage.setItem(cacheKey, stored.current); setPending(request);
      }
      const created = await continueOriginalAgentWork(request.predecessor_ref, request.followup_payload);
      if (epoch !== generation.current || contextStamp !== liveKey.current) return;
      const value = checked(await getOriginalAgentWork(created.work.entity_id));
      if (epoch !== generation.current || contextStamp !== liveKey.current) return;
      if (!verifiedWork(value, request.work_ref)) throw new Error("续作的责任或业务来源无法完整核验。");
      if (localStorage.getItem(cacheKey) !== stored.current) throw new Error("续作结果待核验，本地原请求已变化。");
      request = { scope: { version: 1, binding: scope }, work_ref: value.root_work_ref || request.work_ref };
      stored.current = JSON.stringify(request); localStorage.setItem(cacheKey, stored.current); setPending(request); setSnapshot(value);
      setCandidate(null); chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null); setCandidateNotice("");
    candidateRequest.current += 1; setCandidateContext(null); setCandidateLoading(false);
      if (!value.tasks.length) await executeOriginalAgentWork(value.work.entity_id);
      if (epoch === generation.current && contextStamp === liveKey.current) setSnapshot(checked(await getOriginalAgentWork(request.work_ref)));
    } catch (reason) {
      if (epoch === generation.current && contextStamp === liveKey.current) setError(reason.message + " 原结果与续作请求保留，不会自动重放。");
    } finally { if (epoch === generation.current && contextStamp === liveKey.current) { operation.current = false; setBusy(false); } }
  }
  function clearCandidateRead() {
    candidateRequest.current += 1; setCandidate(null); chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null);
    setCandidateContext(null); setCandidateLoading(false); setCandidateNotice("");
  }
  async function readCandidate(context, artifact = null) {
    if (!ready || liveKey.current !== contextStamp) return;
    const epoch = generation.current, request = ++candidateRequest.current, sourceVersion = sourceStamp;
    setCandidate(null); chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null); setCandidateNotice(""); setCandidateLoading(true); setError("");
    const current = () => epoch === generation.current && contextStamp === liveKey.current && sourceVersion === liveSource.current && request === candidateRequest.current;
    try {
      const value = await getAgentCandidateSource(context.workRef, context.taskRef, artifact?.artifact_id);
      if (!current()) return;
      if (value.tenant_id !== tenantId || value.company_id !== companyId || value.workspace_id !== workspaceId
        || value.work_ref !== context.workRef || value.task_ref !== context.taskRef
        || typeof value.text !== "string" || !value.text.trim() || !/^[0-9a-f]{64}$/.test(value.text_sha256)
        || !/^[0-9a-f]{64}$/.test(value.task_output_sha256)
        || value.content_verification !== "UNVERIFIED") throw new Error("候选来源不属于原工作或正文无法核验。");
      if (artifact ? value.artifact_ref !== artifact.artifact_id || value.artifact_content_sha256 !== artifact.content_sha256
        || !/^[0-9a-f]{64}$/.test(value.file_sha256) || !/^[0-9a-f]{64}$/.test(value.task_output_sha256)
        || typeof value.filename !== "string" || !value.filename
        : Boolean(value.artifact_ref)) throw new Error("所选原文件或回执版本已经改变，请重新核对。");
      const bytes = new TextEncoder().encode(value.text);
      const sha = [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))].map((n) => n.toString(16).padStart(2, "0")).join("");
      if (!current()) return;
      if (sha !== value.text_sha256 || artifact && (sha !== value.file_sha256 || bytes.length !== value.file_bytes))
        throw new Error("成果正文与原文件摘要不一致。");
      setCandidate({ ...value, _selectionGeneration: request, _sourceStamp: sourceVersion });
    } catch (reason) { if (current()) setError(reason.message); }
    finally { if (current()) setCandidateLoading(false); }
  }
  async function prepareCandidate(taskId, workRef = snapshot.work.entity_id) {
    if (!ready || liveKey.current !== contextStamp || operation.current || busy || disabled) return;
    clearCandidateRead();
    const epoch = generation.current, request = candidateRequest.current, sourceVersion = sourceStamp;
    setCandidateLoading(true); setError("");
    const current = () => epoch === generation.current && contextStamp === liveKey.current && sourceVersion === liveSource.current && request === candidateRequest.current;
    try {
      const value = await getResultDetail(companyId, workspaceId, "task:" + taskId);
      if (!current()) return;
      if (value.tenant_id !== tenantId || value.company_id !== companyId || value.workspace_id !== workspaceId
        || value.reference_id !== "task:" + taskId || value.kind !== "RESULT" || value.source_work_ref !== workRef
        || !Array.isArray(value.artifacts)) throw new Error("原成果清单不属于当前工作。");
      const files = value.artifacts.filter((item) => item.artifact_type === "agent_file_receipt");
      if (new Set(files.map((item) => item.artifact_id)).size !== files.length
        || files.some((item) => typeof item.artifact_id !== "string" || !item.artifact_id
          || typeof item.title !== "string" || !/^[0-9a-f]{64}$/.test(item.content_sha256)))
        throw new Error("原成果文件清单无法完整核验。");
      const context = { workRef, taskRef: taskId, files, selected: "" };
      setCandidateContext(context);
      if (!files.length) await readCandidate(context);
    } catch (reason) { if (current()) setError(reason.message); }
    finally { if (current()) setCandidateLoading(false); }
  }
  async function saveCandidate() {
    if (!ready || liveKey.current !== contextStamp || disabled || busy || !candidate || candidate._sourceStamp !== liveSource.current || candidate._selectionGeneration !== candidateRequest.current || candidateLoading || excerpt !== currentExcerpt.current || !excerpt?.excerpt?.trim() || new TextEncoder().encode(excerpt.excerpt).length > 32768 || operation.current) return;
    const epoch = generation.current, request = candidateRequest.current, sourceVersion = sourceStamp;
    const current = () => epoch === generation.current && contextStamp === liveKey.current && sourceVersion === liveSource.current
      && request === candidateRequest.current && excerpt === currentExcerpt.current;
    operation.current = true; setBusy(true);
    try {
      const fileIdentity = candidate.artifact_ref ? Object.fromEntries(
        ["artifact_ref", "artifact_content_sha256", "file_sha256", "task_output_sha256"].map((key) => [key, candidate[key]])) : {};
      await createAgentCandidate(candidate.work_ref, { task_ref: candidate.task_ref, ...excerpt, text_sha256: candidate.text_sha256, ...fileIdentity });
      if (!current()) return;
      setCandidateNotice("已记录到原对象的候选列表；请回原工作核对并明确采用。");
      await onCandidate?.();
    } catch (reason) { if (current()) setError(reason.message + " 请读取原候选核对；不会重新执行 Agent。"); }
    finally { if (epoch === generation.current && contextStamp === liveKey.current) { operation.current = false; setBusy(false); } }
  }
  async function stop() {
    if (!ready || liveKey.current !== contextStamp || !snapshot?.work?.entity_id) return;
    const epoch = generation.current;
    clearCandidateRead();
    try { await stopOriginalAgentWork(snapshot.work.entity_id); if (epoch === generation.current && contextStamp === liveKey.current) await read(); }
    catch { if (epoch === generation.current && contextStamp === liveKey.current) setError("停止结果尚未核验，请读取原工作；不能据此判断远端效果已撤销。"); }
  }
  return <section className="space-y-2 border-t border-ui-line p-4" aria-label="交给 Agent 的正式工作">
    <h3>交给 Agent 的正式工作</h3>
    {hydration.key !== contextStamp && <p role="status">正在核对本地原请求，请稍候。</p>}
    {!snapshot && <>
      <label>执行 Agent<select value={binding} disabled={busy || Boolean(pending)} onChange={(event) => setBinding(event.target.value)}>
        <option value="">选择这位员工已绑定的 Agent</option>
        {pendingBindingUnverified && <option value={pending.payload.agent_binding_ref}>原请求 Agent（当前名称未核验）</option>}
        {agents.filter((item) => item.binding_id).map((item) => <option key={item.binding_id} value={item.binding_id}>{item.display_name}</option>)}
      </select></label>
      <label>期望成果<input value={expected} disabled={busy || Boolean(pending)} maxLength={1600} onChange={(event) => setExpected(event.target.value)} /></label>
      <label>本次允许读取的网站（可选）<input value={browserHosts} disabled={busy || Boolean(pending)} maxLength={1000}
        placeholder="例如 example.com，多个域名用逗号分开" onChange={(event) => setBrowserHosts(event.target.value)} /></label>
      {browserHosts && <p>仅支持读取已确认网站的公开页面；环境尚待独立验证，登录、实时接管、填写表单和发布不可用。</p>}
      {pending?.payload && <details>
        <summary>核对保留的原请求</summary>
        <p>{originalValue(pending.payload.problem)}</p>
        <dl>
          <dt>请求标识</dt><dd>{originalValue(pending.payload.request_id)}</dd>
          <dt>原执行 Agent</dt><dd>{savedAgent?.display_name || "当前绑定列表无法核验名称"} · {originalValue(pending.payload.agent_binding_ref)}</dd>
          <dt>原期望成果</dt><dd>{originalValue(pending.payload.expected_result)}</dd>
          <dt>原允许网站</dt><dd>{Array.isArray(pending.payload.browser_hosts) ? pending.payload.browser_hosts.join("、") || "未请求浏览器读取" : "原请求未提供"}</dd>
          <dt>原业务</dt><dd>{({ "content-growth": "内容增长", writing: "写作", music: "音乐" })[savedSource?.kind] || originalValue(savedSource?.kind)}</dd>
          <dt>原对象</dt><dd>{[savedSource?.content_ref, savedSource?.book_ref, savedSource?.chapter_ref, savedSource?.song_ref].filter(Boolean).join(" / ") || "原请求未提供"}</dd>
          <dt>原版本依据</dt><dd>{originalValue(savedSource?.expected_draft_ref || savedSource?.expected_version_ref || savedSource?.expected)}</dd>
          <dt>原选区</dt><dd>{savedSelection?.start !== undefined && savedSelection?.end !== undefined ? savedSelection.start + "–" + savedSelection.end : "原请求未提供字符范围"}</dd>
          <dt>原选段版本</dt><dd>{originalValue(savedSelection?.draft_ref || savedSelection?.version_ref || savedSelection?.basis)}</dd>
          <dt>原选段校验值</dt><dd>{originalValue(savedSelection?.sha256 || savedSelection?.text_sha256)}</dd>
          <dt>原业务包版本</dt><dd>{originalValue(savedSource?.package_version || savedSource?.packageVersion)}</dd>
        </dl>
        {typeof savedSelection?.excerpt === "string" && <p>原选段摘要：{savedSelection.excerpt.slice(0, 600)}</p>}
        <details><summary>查看完整原来源（只读）</summary><pre className="whitespace-pre-wrap break-all">{savedSource ? JSON.stringify(savedSource, null, 2) : "原请求未提供来源"}</pre></details>
        {pendingBindingUnverified && <p>请先核对该员工的原 Agent 绑定，再继续这份请求。</p>}
      </details>}
      {workflowSupported && <section aria-label="当前责任流程">
        <button type="button" disabled={!ready || busy || disabled || !tenantId || !assignmentRef} onClick={inspectWorkflow}>核对责任流程</button>
        {workflow && <>
          <p role="status">{workflow.reason}</p>
          <dl>
            <dt>员工与责任</dt><dd>{workflow.employee_name} · {workflow.role_name}：{workflow.responsibility}</dd>
            <dt>工作空间</dt><dd>{workflow.workspace_name}（{workflow.workspace_id}）</dd>
            <dt>责任范围</dt><dd>{workflow.scope_type} / {workflow.scope_ref}</dd>
            <dt>责任版本</dt><dd>{workflow.assignment_ref} / {workflow.assignment_revision}</dd>
            <dt>匹配的已发布流程</dt><dd>{workflow.matching_count}</dd>
          </dl>
          {workflow.publication_allowed && <>
            <p>将为当前员工的这项责任发布单步流程。发布后，请单独继续原创建请求。</p>
            <label><input type="checkbox" checked={workflowConsent} disabled={busy} onChange={(event) => setWorkflowConsent(event.target.checked)} />我已核对上述责任、范围与版本</label>
            <button type="button" disabled={!ready || busy || disabled || !workflowConsent} onClick={publishWorkflow}>确认发布当前责任流程</button>
            <button type="button" disabled={busy} onClick={() => { setWorkflow(null); setWorkflowConsent(false); }}>取消发布</button>
          </>}
        </>}
      </section>}
      <p>这会创建可追踪的工作并执行一次。普通讨论不会自动变成工作。</p>
      <button type="button" disabled={!ready || busy || disabled || pendingBindingUnverified || !tenantId || !assignmentRef || (!pending && (!binding || !body?.trim() || !expected.trim())) || readiness?.state !== "AVAILABLE"} onClick={() => start(false)}>{pending ? "核对并继续原创建请求" : "交给 Agent 执行"}</button>
      {readiness?.state !== "AVAILABLE" && <p>{readiness?.reason || "执行许可尚未核验。"} <a href="/ceo-office/capabilities">核对 Agent 许可</a></p>}
    </>}
    {snapshot && <>
      <p role="status">{outcomeUncertain ? "执行状态和外部效果仍需核验，不能重复启动。" : running || busy ? "员工正在处理原工作" : task?.status === "COMPLETED" ? "原执行已结束，请核对结果" : task?.status === "CANCELLED" ? "已请求停止；外部进程和效果仍需核验" : task?.status === "FAILED" ? (task?.reason_code === "codex_execution_held" ? "真实 Agent 执行暂不可用：停止安全机制尚未验证。" : "原执行未完成") : "原工作等待执行"}</p>
      {directChildReaped && <p role="status">受控直接子进程已退出；其他进程和外部效果仍待核验。</p>}
      {task?.stage && <p>已收到执行进度</p>}
      <button type="button" onClick={read}>读取原工作</button>
      {!task && <button type="button" disabled={!ready || busy || disabled || readiness?.state !== "AVAILABLE"} onClick={() => start(false)}>启动已创建的原工作</button>}
      {(running || busy) && <button type="button" disabled={!ready} onClick={stop}>停止原工作</button>}
      {task?.status === "FAILED" && task.reason_code !== "codex_execution_held" && !outcomeUncertain && !task.call_reserved && <button type="button" disabled={!ready || busy || disabled || readiness?.state !== "AVAILABLE"} onClick={() => start(true)}>修复后继续原工作</button>}
      {task?.status === "FAILED" && task.call_reserved && <p>这次调用已占用额度，效果尚未核验，不会自动重放。</p>}
      {historyTasks.filter((item) => item.result_ref).map((item, index) => <button type="button" key={item.task_id} onClick={() => setResult(resultSelection(workspaceId, item.result_ref))}>查看第 {index + 1} 次结果</button>)}
      {source && source.kind !== "references" && historyTasks.filter((item) => item.result_ref).map((item) =>
        <button type="button" key={"candidate-" + item.task_id} disabled={!ready || busy || disabled} onClick={() => prepareCandidate(item.task_id, item.work_ref)}>核对并回填原对象候选</button>)}
      {task?.status === "COMPLETED" && !busy && !outcomeUncertain && <>
        <label>本次续作期望成果<input value={expected} maxLength={1600} disabled={Boolean(pending?.followup_payload)} onChange={(event) => setExpected(event.target.value)} /></label>
        <label>本次续作允许读取的网站（可选）<input value={browserHosts} maxLength={1000} disabled={Boolean(pending?.followup_payload)} onChange={(event) => setBrowserHosts(event.target.value)} /></label>
        <p>先核对原成果文件或结果正文，选择本次续作要使用的文字。</p>
        {followupBasis && <div><p>已选续作依据 · {followupBasis.bytes} 字节 · 内容仍需核验</p><blockquote>{followupBasis.text}</blockquote></div>}
        {pending?.followup_payload && <p>原续作请求结果待核验，已保留，不会重复提交。</p>}
        <button type="button" disabled={!ready || disabled || Boolean(pending?.followup_payload) || !followupBasis || followupBasis.workRef !== snapshot.work.entity_id || followupBasis.taskRef !== task?.task_id || !body?.trim() || !expected.trim() || readiness?.state !== "AVAILABLE"} onClick={followUp}>认可所选成果并沿原工作继续</button>
      </>}
    </>}
    {(candidateContext || candidateLoading) && <section aria-label="回填原对象候选">
      {candidateContext?.files.length > 0 && <label>选择要回填的原成果文件<select aria-label="选择要回填的原成果文件"
        value={candidateContext.selected} disabled={busy || disabled} onChange={(event) => {
          const selected = event.target.value, file = candidateContext.files.find((item) => item.artifact_id === selected);
          setCandidateContext({ ...candidateContext, selected });
          if (file) return readCandidate(candidateContext, file);
          else { candidateRequest.current += 1; setCandidate(null); chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null); setCandidateLoading(false); setCandidateNotice(""); }
        }}>
        <option value="">请选择文件，不会自动使用执行摘要</option>
        {candidateContext.files.map((file) => <option key={file.artifact_id} value={file.artifact_id}>{file.title}</option>)}
      </select></label>}
      {candidateLoading && <p role="status">正在核验原成果正文…</p>}
      {candidate && <>
        <p>{candidate.artifact_ref ? "已核对所选文件：" + candidate.filename + "。文件完整性已核对，内容仍需你核验。" : "下方是原执行返回的文本，内容仍需你核验。"} 请选择片段或全文；不会自动采用或发布。</p>
        <textarea aria-label="原成果正文，可选择回填范围" readOnly value={candidate.text} className="w-full" rows={8}
          onSelect={(event) => { const { selectionStart: start, selectionEnd: end } = event.target;
            if (candidate._sourceStamp !== liveSource.current || candidate._selectionGeneration !== candidateRequest.current) return;
            if (end <= start) prepareExcerpt(null);
            else if (currentExcerpt.current?.start !== start || currentExcerpt.current?.end !== end) {
              prepareExcerpt({ start, end, excerpt: candidate.text.slice(start, end) }); chooseExcerpt(null); setFollowupBasis(null);
            } }} />
        <button type="button" disabled={busy || disabled || !draftExcerpt?.excerpt?.trim()} onClick={() => {
          if (candidate._sourceStamp !== liveSource.current || candidate._selectionGeneration !== candidateRequest.current || !draftExcerpt || draftExcerpt !== currentDraft.current) return;
          chooseExcerpt(draftExcerpt); prepareExcerpt(null); setFollowupBasis(null);
        }}>确认所选片段</button>
        <button type="button" disabled={busy || disabled} onClick={() => {
          if (candidate._sourceStamp !== liveSource.current || candidate._selectionGeneration !== candidateRequest.current) return;
          chooseExcerpt({ start: 0, end: candidate.text.length, excerpt: candidate.text }); prepareExcerpt(null); setFollowupBasis(null);
        }}>选择全文</button>
        <button type="button" disabled={busy || disabled || (!excerpt && !draftExcerpt)} onClick={() => { chooseExcerpt(null); prepareExcerpt(null); setFollowupBasis(null); }}>清除选择</button>
        {excerpt ? <div><p>已确认 {Array.from(excerpt.excerpt).length} 个字符，以下文字将保存为候选：</p><pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{excerpt.excerpt}</pre></div> : <p>尚未确认回填文字。</p>}
        {task?.status === "COMPLETED" && candidate.work_ref === snapshot?.work?.entity_id && candidate.task_ref === task?.task_id && <button type="button"
          disabled={busy || disabled || !excerpt?.excerpt?.trim() || new TextEncoder().encode(excerpt?.excerpt || "").length > 32768}
          onClick={() => {
            if (excerpt !== currentExcerpt.current || candidate._sourceStamp !== liveSource.current || candidate._selectionGeneration !== candidateRequest.current) return;
            const file = candidate.artifact_ref ? Object.fromEntries(["artifact_ref", "artifact_content_sha256", "file_sha256"].map((key) => [key, candidate[key]])) : {};
            setFollowupBasis({ workRef: candidate.work_ref, taskRef: candidate.task_ref, sourceStamp: candidate._sourceStamp, text: excerpt.excerpt,
              bytes: new TextEncoder().encode(excerpt.excerpt).length, basis: { mode: candidate.artifact_ref ? "file" : "result",
                start: excerpt.start, end: excerpt.end, text_sha256: candidate.text_sha256, task_output_sha256: candidate.task_output_sha256, ...file } });
          }}>使用所选文字作为续作依据</button>}
        {excerpt?.excerpt && new TextEncoder().encode(excerpt.excerpt).length > 32768 && <p role="alert">所选文字超过 32768 字节，请缩小范围。</p>}
      </>}
      <button type="button" disabled={busy || disabled || candidateLoading || !candidate || !excerpt?.excerpt?.trim() || new TextEncoder().encode(excerpt?.excerpt || "").length > 32768} onClick={saveCandidate}>保存为原对象候选</button>
      {candidateNotice && <p role="status">{candidateNotice} {returnHref && <a href={returnHref}>返回原工作</a>}</p>}
    </section>}
    {result && <ResultReferenceView companyId={companyId} selection={result} conversationReturn={returnHref} businessReturn={businessReturn} onClose={() => setResult(null)} />}
    {error && <p role="alert">{error}</p>}
  </section>;
}

export function useConversationModel(scopeKey = "", writing = null) {
  const [state, setState] = useState({ status: "loading", models: [], selected: null });
  useEffect(() => {
    if (writing) {
      const models = writing.models || [];
      const selected = writing.selected?.model || models.find((m) => m.model_key === writing.preference?.model_key) || null;
      const valid = selected && models.some((m) => m.model_key === selected.model_key && m.source === selected.source && m.updated_at === selected.updated_at);
      setState({ status: valid ? "ready" : "unavailable", models, selected: valid ? selected : null });
      return;
    }
    Promise.all([getEnabledModels(), getModelPreference()]).then(async ([privatePayload, preferencePayload]) => {
      const models = (privatePayload.models || []).filter((item) => item.enabled);
      let selected = null;
      try { selected = JSON.parse(sessionStorage.getItem(`curis.v1.conversationModel.${scopeKey}`) || "null"); } catch (_error) { selected = null; }
      const valid = selected && models.some((item) => item.provider_type === selected.provider_id && item.model_name === selected.model_id);
      const preferredProvider = (preferencePayload.available_models || []).find(
        (item) => item.model_key === preferencePayload.preference?.model_key
      )?.provider_id;
      const providerId = valid ? selected.provider_id : preferredProvider;
      const candidate = valid ? selected : preferencePayload.preference || null;
      if (!providerId || !candidate || !models.some((item) => item.provider_type === providerId)) {
        setState({ status: "unavailable", models, selected: null });
        return;
      }
      const recovered = await recoverAIProvider(providerId);
      const recoveredModels = recovered.models || [];
      const selectedCapabilityId = candidate.capability_id || candidate.model_key;
      const selectedModelName = candidate.model_id || candidate.model_name;
      const modelStillAvailable = recoveredModels.some((item) =>
        item.capability_id === selectedCapabilityId && item.model_id === selectedModelName
      );
      setState({
        status: recovered.health === "healthy" && modelStillAvailable ? "ready" : "unavailable",
        models,
        selected: recovered.health === "healthy" && modelStillAvailable ? candidate : null,
      });
    }).catch(() => setState({ status: "unavailable", models: [], selected: null }));
  }, [scopeKey, writing?.models, writing?.selected, writing?.preference]); // eslint-disable-line react-hooks/exhaustive-deps
  const choose = async (model) => {
    if (writing) {
      const current = (writing.models || []).find((m) => m.model_key === model.model_key && m.source === model.source);
      if (!current) throw new Error("所选模型已不可用。");
      const result = await writing.onChoose(current.model_key);
      setState({ status: "ready", models: result.models, selected: result.selected_model.model });
      return;
    }
    setState((current) => ({ ...current, status: "loading", selected: null }));
    try {
      const recovered = await recoverAIProvider(model.provider_type);
      if (recovered.health !== "healthy") throw new Error("provider not healthy");
      const recoveredModel = (recovered.models || []).find((item) => item.model_id === model.model_name);
      if (!recoveredModel) throw new Error("model not available");
      const selected = { provider_id: model.provider_type, model_id: model.model_name, capability_id: recoveredModel.capability_id };
      sessionStorage.setItem(`curis.v1.conversationModel.${scopeKey}`, JSON.stringify(selected));
      setState((current) => ({ ...current, status: "ready", selected }));
    } catch {
      setState((current) => ({ ...current, status: "unavailable", selected: null }));
    }
  };
  return { ...state, choose };
}
